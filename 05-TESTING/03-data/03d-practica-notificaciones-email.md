# 🧪 03d: Práctica - Testing de Notificaciones y Email

> **¿Qué vas a practicar?** Testing de servicios de notificaciones push y envío de emails en una app Flutter con Supabase, usando Mocktail para aislar dependencias externas.

---

## 📋 Índice

1. [Introducción](#1-introducción)
2. [Setup](#2-setup)
3. [Ejercicio 1: Notification Service](#3-ejercicio-1-notification-service)
4. [Ejercicio 2: Email Service](#4-ejercicio-2-email-service)
5. [Ejercicio 3: Notification Preferences Repository](#5-ejercicio-3-notification-preferences-repository)
6. [Ejercicio 4: Integration with Supabase Functions](#6-ejercicio-4-integration-with-supabase-functions)

---

## 1. Introducción

### 🎯 ¿Qué vamos a testear?

| Componente | Responsabilidad | Dependencia externa |
|------------|----------------|---------------------|
| `NotificationService` | Enviar notificaciones push | Firebase Cloud Messaging (FCM) |
| `EmailService` | Enviar emails transaccionales | Supabase Edge Functions / SendGrid |
| `NotificationPreferencesRepository` | Guardar preferencias del usuario | SharedPreferences / Supabase DB |
| `Supabase Functions` | Backend para notificaciones | Supabase Edge Functions API |

### 🎭 Estrategia de mocking

```dart
// Mock de Firebase Messaging (no podemos instanciarlo en tests unitarios)
class MockFirebaseMessaging extends Mock implements FirebaseMessaging {}

// Mock de HTTP Client (para llamadas a Edge Functions)
class MockHttpClient extends Mock implements http.Client {}

// Mock de SharedPreferences
class MockSharedPreferences extends Mock implements SharedPreferences {}
```

---

## 2. Setup

### 📦 pubspec.yaml

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.4
```

### 📁 Mocks compartidos

```dart
// test/helpers/mocks.dart
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mocktail/mocktail.dart';

class MockFirebaseMessaging extends Mock implements FirebaseMessaging {}
class MockHttpClient extends Mock implements http.Client {}
class MockSharedPreferences extends Mock implements SharedPreferences {}
```

---

## 3. Ejercicio 1: Notification Service

### 🎯 Objetivo

Testear el servicio que maneja tokens FCM y envía notificaciones locales.

### 📝 Código fuente

```dart
// lib/clean/core/notifications/notification_service.dart
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  final FirebaseMessaging messaging;
  final FlutterLocalNotificationsPlugin localNotifications;

  NotificationService({
    required this.messaging,
    required this.localNotifications,
  });

  Future<String?> getToken() async {
    return await messaging.getToken();
  }

  Future<void> requestPermission() async {
    final settings = await messaging.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );
    if (settings.authorizationStatus != AuthorizationStatus.authorized) {
      throw NotificationPermissionDenied();
    }
  }

  Future<void> showLocalNotification({
    required String title,
    required String body,
  }) async {
    await localNotifications.show(
      0,
      title,
      body,
      const NotificationDetails(
        android: AndroidNotificationDetails('channel_id', 'channel_name'),
        iOS: DarwinNotificationDetails(),
      ),
    );
  }
}
```

### 🧪 Tests

```dart
// test/core/notifications/notification_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:mi_proyecto_flutter/clean/core/notifications/notification_service.dart';
import '../../helpers/mocks.dart';

// Necesitamos mocks adicionales
class MockFlutterLocalNotificationsPlugin extends Mock
    implements FlutterLocalNotificationsPlugin {}

void main() {
  late NotificationService service;
  late MockFirebaseMessaging mockMessaging;
  late MockFlutterLocalNotificationsPlugin mockLocalNotifications;

  setUp(() {
    mockMessaging = MockFirebaseMessaging();
    mockLocalNotifications = MockFlutterLocalNotificationsPlugin();
    service = NotificationService(
      messaging: mockMessaging,
      localNotifications: mockLocalNotifications,
    );
  });

  group('getToken', () {
    test('should return FCM token', () async {
      when(() => mockMessaging.getToken())
          .thenAnswer((_) async => 'fcm-token-123');

      final token = await service.getToken();

      expect(token, equals('fcm-token-123'));
      verify(() => mockMessaging.getToken()).called(1);
    });

    test('should return null when token unavailable', () async {
      when(() => mockMessaging.getToken())
          .thenAnswer((_) async => null);

      final token = await service.getToken();

      expect(token, isNull);
    });
  });

  group('requestPermission', () {
    test('should succeed when authorized', () async {
      when(() => mockMessaging.requestPermission(
        alert: any(named: 'alert'),
        badge: any(named: 'badge'),
        sound: any(named: 'sound'),
      )).thenAnswer((_) async => NotificationSettings(
        authorizationStatus: AuthorizationStatus.authorized,
        alert: AppleNotificationSetting.enabled,
        badge: AppleNotificationSetting.enabled,
        sound: AppleNotificationSetting.enabled,
        lockScreen: AppleNotificationSetting.enabled,
        notificationCenter: AppleNotificationSetting.enabled,
        criticalAlert: AppleNotificationSetting.enabled,
        timeSensitive: AppleNotificationSetting.enabled,
        providesAppNotificationSettings: false,
        carPlay: AppleNotificationSetting.enabled,
        announcement: AppleNotificationSetting.enabled,
      ));

      await expectLater(service.requestPermission(), completes);
    });

    test('should throw when denied', () async {
      when(() => mockMessaging.requestPermission(
        alert: any(named: 'alert'),
        badge: any(named: 'badge'),
        sound: any(named: 'sound'),
      )).thenAnswer((_) async => NotificationSettings(
        authorizationStatus: AuthorizationStatus.denied,
        alert: AppleNotificationSetting.disabled,
        badge: AppleNotificationSetting.disabled,
        sound: AppleNotificationSetting.disabled,
        lockScreen: AppleNotificationSetting.disabled,
        notificationCenter: AppleNotificationSetting.disabled,
        criticalAlert: AppleNotificationSetting.disabled,
        timeSensitive: AppleNotificationSetting.disabled,
        providesAppNotificationSettings: false,
        carPlay: AppleNotificationSetting.disabled,
        announcement: AppleNotificationSetting.disabled,
      ));

      expect(
        () => service.requestPermission(),
        throwsA(isA<NotificationPermissionDenied>()),
      );
    });
  });

  group('showLocalNotification', () {
    test('should show local notification', () async {
      await service.showLocalNotification(
        title: 'Test Title',
        body: 'Test Body',
      );

      verify(() => mockLocalNotifications.show(
        0,
        'Test Title',
        'Test Body',
        any<NotificationDetails>(),
      )).called(1);
    });
  });
}
```

---

## 4. Ejercicio 2: Email Service

### 🎯 Objetivo

Testear el servicio que envía emails a través de Supabase Edge Functions.

### 📝 Código fuente

```dart
// lib/clean/core/notifications/email_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class EmailService {
  final http.Client client;
  final String supabaseUrl;
  final String anonKey;

  EmailService({
    required this.client,
    required this.supabaseUrl,
    required this.anonKey,
  });

  Future<void> sendWelcomeEmail({
    required String to,
    required String name,
  }) async {
    final response = await client.post(
      Uri.parse('$supabaseUrl/functions/v1/send-welcome-email'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $anonKey',
      },
      body: json.encode({
        'to': to,
        'name': name,
      }),
    );

    if (response.statusCode != 200) {
      throw EmailSendFailure('Failed to send welcome email');
    }
  }

  Future<void> sendPasswordReset({
    required String to,
    required String resetLink,
  }) async {
    final response = await client.post(
      Uri.parse('$supabaseUrl/functions/v1/send-password-reset'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $anonKey',
      },
      body: json.encode({
        'to': to,
        'reset_link': resetLink,
      }),
    );

    if (response.statusCode != 200) {
      throw EmailSendFailure('Failed to send password reset email');
    }
  }
}
```

### 🧪 Tests

```dart
// test/core/notifications/email_service_test.dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mocktail/mocktail.dart';
import 'package:mi_proyecto_flutter/clean/core/notifications/email_service.dart';
import '../../helpers/mocks.dart';

void main() {
  late EmailService service;
  late MockHttpClient mockClient;

  setUp(() {
    mockClient = MockHttpClient();
    service = EmailService(
      client: mockClient,
      supabaseUrl: 'https://test.supabase.co',
      anonKey: 'test-anon-key',
    );
  });

  group('sendWelcomeEmail', () {
    test('should send welcome email successfully', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response('OK', 200));

      await service.sendWelcomeEmail(
        to: 'user@test.com',
        name: 'John',
      );

      verify(() => mockClient.post(
        Uri.parse('https://test.supabase.co/functions/v1/send-welcome-email'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer test-anon-key',
        },
        body: json.encode({'to': 'user@test.com', 'name': 'John'}),
      )).called(1);
    });

    test('should throw when API fails', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response('Error', 500));

      expect(
        () => service.sendWelcomeEmail(to: 'user@test.com', name: 'John'),
        throwsA(isA<EmailSendFailure>()),
      );
    });
  });

  group('sendPasswordReset', () {
    test('should send password reset email', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response('OK', 200));

      await service.sendPasswordReset(
        to: 'user@test.com',
        resetLink: 'https://app.com/reset?token=abc',
      );

      verify(() => mockClient.post(
        Uri.parse('https://test.supabase.co/functions/v1/send-password-reset'),
        headers: any(named: 'headers'),
        body: json.encode({
          'to': 'user@test.com',
          'reset_link': 'https://app.com/reset?token=abc',
        }),
      )).called(1);
    });
  });
}
```

---

## 5. Ejercicio 3: Notification Preferences Repository

### 🎯 Objetivo

Testear el repositorio que gestiona las preferencias de notificaciones del usuario (almacenadas localmente y en Supabase).

### 📝 Código fuente

```dart
// lib/clean/core/notifications/notification_preferences_repository.dart
import 'package:shared_preferences/shared_preferences.dart';

class NotificationPreferencesRepository {
  final SharedPreferences prefs;

  NotificationPreferencesRepository({required this.prefs});

  static const _keyPushEnabled = 'push_enabled';
  static const _keyEmailEnabled = 'email_enabled';
  static const _keyQuietHoursStart = 'quiet_hours_start';
  static const _keyQuietHoursEnd = 'quiet_hours_end';

  bool get pushEnabled => prefs.getBool(_keyPushEnabled) ?? true;
  bool get emailEnabled => prefs.getBool(_keyEmailEnabled) ?? true;
  String? get quietHoursStart => prefs.getString(_keyQuietHoursStart);
  String? get quietHoursEnd => prefs.getString(_keyQuietHoursEnd);

  Future<void> setPushEnabled(bool value) async {
    await prefs.setBool(_keyPushEnabled, value);
  }

  Future<void> setEmailEnabled(bool value) async {
    await prefs.setBool(_keyEmailEnabled, value);
  }

  Future<void> setQuietHours({
    required String start,
    required String end,
  }) async {
    await prefs.setString(_keyQuietHoursStart, start);
    await prefs.setString(_keyQuietHoursEnd, end);
  }

  Future<void> resetToDefaults() async {
    await prefs.remove(_keyPushEnabled);
    await prefs.remove(_keyEmailEnabled);
    await prefs.remove(_keyQuietHoursStart);
    await prefs.remove(_keyQuietHoursEnd);
  }
}
```

### 🧪 Tests

```dart
// test/core/notifications/notification_preferences_repository_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mi_proyecto_flutter/clean/core/notifications/notification_preferences_repository.dart';
import '../../helpers/mocks.dart';

void main() {
  late NotificationPreferencesRepository repository;
  late MockSharedPreferences mockPrefs;

  setUp(() {
    mockPrefs = MockSharedPreferences();
    repository = NotificationPreferencesRepository(prefs: mockPrefs);
  });

  group('pushEnabled', () {
    test('should return true when preference is set', () {
      when(() => mockPrefs.getBool('push_enabled')).thenReturn(true);

      expect(repository.pushEnabled, isTrue);
    });

    test('should return true by default when not set', () {
      when(() => mockPrefs.getBool('push_enabled')).thenReturn(null);

      expect(repository.pushEnabled, isTrue);
    });
  });

  group('setPushEnabled', () {
    test('should save preference', () async {
      when(() => mockPrefs.setBool(any(), any()))
          .thenAnswer((_) async => true);

      await repository.setPushEnabled(false);

      verify(() => mockPrefs.setBool('push_enabled', false)).called(1);
    });
  });

  group('resetToDefaults', () {
    test('should remove all notification preferences', () async {
      when(() => mockPrefs.remove(any())).thenAnswer((_) async => true);

      await repository.resetToDefaults();

      verify(() => mockPrefs.remove('push_enabled')).called(1);
      verify(() => mockPrefs.remove('email_enabled')).called(1);
      verify(() => mockPrefs.remove('quiet_hours_start')).called(1);
      verify(() => mockPrefs.remove('quiet_hours_end')).called(1);
    });
  });

  group('quietHours', () {
    test('should return saved quiet hours', () {
      when(() => mockPrefs.getString('quiet_hours_start'))
          .thenReturn('22:00');
      when(() => mockPrefs.getString('quiet_hours_end'))
          .thenReturn('08:00');

      expect(repository.quietHoursStart, equals('22:00'));
      expect(repository.quietHoursEnd, equals('08:00'));
    });

    test('should save quiet hours', () async {
      when(() => mockPrefs.setString(any(), any()))
          .thenAnswer((_) async => true);

      await repository.setQuietHours(start: '23:00', end: '07:00');

      verify(() => mockPrefs.setString('quiet_hours_start', '23:00')).called(1);
      verify(() => mockPrefs.setString('quiet_hours_end', '07:00')).called(1);
    });
  });
}
```

---

## 6. Ejercicio 4: Integration with Supabase Functions

### 🎯 Objetivo

Testear el servicio que se comunica con Edge Functions de Supabase para enviar notificaciones.

### 📝 Código fuente

```dart
// lib/clean/core/notifications/supabase_notification_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class SupabaseNotificationService {
  final http.Client client;
  final String supabaseUrl;
  final String anonKey;

  SupabaseNotificationService({
    required this.client,
    required this.supabaseUrl,
    required this.anonKey,
  });

  Future<void> sendNotification({
    required String userId,
    required String title,
    required String body,
    Map<String, dynamic>? data,
  }) async {
    final response = await client.post(
      Uri.parse('$supabaseUrl/functions/v1/send-notification'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $anonKey',
      },
      body: json.encode({
        'user_id': userId,
        'title': title,
        'body': body,
        if (data != null) 'data': data,
      }),
    );

    if (response.statusCode != 200) {
      throw NotificationSendFailure('Failed to send notification');
    }
  }

  Future<void> sendBulkNotification({
    required List<String> userIds,
    required String title,
    required String body,
  }) async {
    final response = await client.post(
      Uri.parse('$supabaseUrl/functions/v1/send-bulk-notification'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $anonKey',
      },
      body: json.encode({
        'user_ids': userIds,
        'title': title,
        'body': body,
      }),
    );

    if (response.statusCode != 200) {
      throw NotificationSendFailure('Failed to send bulk notification');
    }
  }
}
```

### 🧪 Tests

```dart
// test/core/notifications/supabase_notification_service_test.dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mocktail/mocktail.dart';
import 'package:mi_proyecto_flutter/clean/core/notifications/supabase_notification_service.dart';
import '../../helpers/mocks.dart';

void main() {
  late SupabaseNotificationService service;
  late MockHttpClient mockClient;

  setUp(() {
    mockClient = MockHttpClient();
    service = SupabaseNotificationService(
      client: mockClient,
      supabaseUrl: 'https://test.supabase.co',
      anonKey: 'test-anon-key',
    );
  });

  group('sendNotification', () {
    test('should send single notification successfully', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response('OK', 200));

      await service.sendNotification(
        userId: 'user-123',
        title: 'New message',
        body: 'You have a new message',
        data: {'type': 'chat', 'chat_id': 'chat-456'},
      );

      final captured = verify(() => mockClient.post(
        Uri.parse('https://test.supabase.co/functions/v1/send-notification'),
        headers: any(named: 'headers'),
        body: captureAny(named: 'body'),
      )).captured;

      final body = json.decode(captured.first as String);
      expect(body['user_id'], equals('user-123'));
      expect(body['title'], equals('New message'));
      expect(body['data']['type'], equals('chat'));
    });

    test('should throw on failure', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response('Error', 500));

      expect(
        () => service.sendNotification(
          userId: 'user-123',
          title: 'Test',
          body: 'Test',
        ),
        throwsA(isA<NotificationSendFailure>()),
      );
    });
  });

  group('sendBulkNotification', () {
    test('should send to multiple users', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response('OK', 200));

      await service.sendBulkNotification(
        userIds: ['user-1', 'user-2', 'user-3'],
        title: 'Broadcast',
        body: 'Message to all',
      );

      final captured = verify(() => mockClient.post(
        Uri.parse('https://test.supabase.co/functions/v1/send-bulk-notification'),
        headers: any(named: 'headers'),
        body: captureAny(named: 'body'),
      )).captured;

      final body = json.decode(captured.first as String);
      expect((body['user_ids'] as List).length, equals(3));
    });
  });
}
```

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 4: Presentation Testing](../04-presentation/04-presentation-testing.md)

**Práctica:**
- [03a-practica-fixtures-models.md](./03a-practica-fixtures-models.md) ← Fixtures y Models
- [03b-practica-datasources.md](./03b-practica-datasources.md) ← DataSources
- [03c-practica-repositories.md](./03c-practica-repositories.md) ← Repositories

---

## ✅ Checklist

- [ ] Testear obtención de FCM token
- [ ] Testear permisos de notificaciones
- [ ] Testear notificaciones locales
- [ ] Testear envío de emails (welcome, password reset)
- [ ] Testear preferencias de notificaciones (SharedPreferences)
- [ ] Testear Edge Functions de Supabase
- [ ] Testear notificaciones bulk
- [ ] Verificar manejo de errores (HTTP 500, permisos denegados)
