# 🧪 Parte 5: Testing Core y Servicios

## 📋 Índice
1. [Introducción a Core](#introducción-a-core)
2. [Testing de NetworkInfo](#testing-de-networkinfo)
3. [Testing de Servicios](#testing-de-servicios)
4. [Testing de Storage](#testing-de-storage)
5. [Testing de Utils](#testing-de-utils)
6. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Introducción a Core

La capa **Core** contiene utilidades y servicios compartidos por toda la aplicación.

### 🎯 Componentes típicos de Core:

- **NetworkInfo**: Información de conectividad
- **Services**: Servicios globales (auth monitor, notificaciones)
- **Storage**: Abstracción de almacenamiento local
- **Utils**: Funciones de utilidad
- **Error Handling**: Excepciones y Failures

### 📦 Arquitectura:

```
Core Layer
├── error/           ← Excepciones y Failures
│   ├── exceptions.dart
│   └── failures.dart
├── network/         ← Conectividad
│   └── network_info.dart
├── services/        ← Servicios globales
│   └── auth_state_monitor.dart
├── storage/         ← Almacenamiento
│   └── storage_service.dart
└── utils/           ← Utilidades
    └── validators.dart
```

---

## Testing de NetworkInfo

NetworkInfo verifica si el dispositivo tiene conexión a internet.

### 📁 Archivo fuente: `lib/clean/core/network/network_info.dart`

```dart
import 'package:internet_connection_checker_plus/internet_connection_checker_plus.dart';

abstract class NetworkInfo {
  Future<bool> get isConnected;
}

class NetworkInfoImpl implements NetworkInfo {
  final InternetConnectionCheckerPlus connectionChecker;

  NetworkInfoImpl({required this.connectionChecker});

  @override
  Future<bool> get isConnected => connectionChecker.hasConnection;
}
```

### 🧪 Tests de NetworkInfo

**`test/core/network/network_info_test.dart`**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/network/network_info.dart';

// Fake del connection checker
class FakeInternetConnectionChecker {
  bool hasConnectionValue = true;
  
  Future<bool> get hasConnection async => hasConnectionValue;
}

void main() {
  late NetworkInfoImpl networkInfo;
  late FakeInternetConnectionChecker fakeChecker;

  setUp(() {
    fakeChecker = FakeInternetConnectionChecker();
    networkInfo = NetworkInfoImpl(
      connectionChecker: fakeChecker as dynamic,
    );
  });

  group('isConnected', () {
    test('should return true when connected', () async {
      // ARRANGE
      fakeChecker.hasConnectionValue = true;

      // ACT
      final result = await networkInfo.isConnected;

      // ASSERT
      expect(result, isTrue);
    });

    test('should return false when not connected', () async {
      // ARRANGE
      fakeChecker.hasConnectionValue = false;

      // ACT
      final result = await networkInfo.isConnected;

      // ASSERT
      expect(result, isFalse);
    });

    test('should call connection checker', () async {
      // ARRANGE
      var wasCalled = false;
      fakeChecker.hasConnectionValue = true;

      // ACT
      await networkInfo.isConnected;
      wasCalled = true;

      // ASSERT
      expect(wasCalled, isTrue);
    });
  });
}
```

---

## Testing de Servicios

### 📁 Ejemplo: AuthStateMonitor

```dart
// lib/clean/core/services/auth_state_monitor.dart
import 'dart:async';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';

abstract class IAuthStateMonitor {
  Stream<User?> get authStateChanges;
  void dispose();
}

class AuthStateMonitor implements IAuthStateMonitor {
  final StreamController<User?> _controller = StreamController<User?>.broadcast();

  @override
  Stream<User?> get authStateChanges => _controller.stream;

  void emitUser(User? user) {
    _controller.add(user);
  }

  @override
  void dispose() {
    _controller.close();
  }
}
```

### 🧪 Tests de AuthStateMonitor

**`test/core/services/auth_state_monitor_test.dart`**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/services/auth_state_monitor.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';

void main() {
  late AuthStateMonitor monitor;

  setUp(() {
    monitor = AuthStateMonitor();
  });

  tearDown(() {
    monitor.dispose();
  });

  group('authStateChanges', () {
    test('should emit user when authenticated', () async {
      // ARRANGE
      const tUser = User(
        id: '123',
        email: 'test@example.com',
        name: 'John',
        lastName: 'Doe',
      );

      // ACT & ASSERT
      expectLater(
        monitor.authStateChanges,
        emits(tUser),
      );

      monitor.emitUser(tUser);
    });

    test('should emit null when not authenticated', () async {
      // ACT & ASSERT
      expectLater(
        monitor.authStateChanges,
        emits(null),
      );

      monitor.emitUser(null);
    });

    test('should emit multiple states in order', () async {
      // ARRANGE
      const user1 = User(
        id: '123',
        email: 'user1@example.com',
        name: 'User1',
        lastName: 'Test',
      );
      const user2 = User(
        id: '456',
        email: 'user2@example.com',
        name: 'User2',
        lastName: 'Test',
      );

      // ACT & ASSERT
      expectLater(
        monitor.authStateChanges,
        emitsInOrder([user1, null, user2]),
      );

      monitor.emitUser(user1);
      monitor.emitUser(null);
      monitor.emitUser(user2);
    });

    test('should allow multiple listeners', () async {
      // ARRANGE
      const tUser = User(
        id: '123',
        email: 'test@example.com',
        name: 'John',
        lastName: 'Doe',
      );

      final listener1 = <User?>[];
      final listener2 = <User?>[];

      // ACT
      monitor.authStateChanges.listen((user) => listener1.add(user));
      monitor.authStateChanges.listen((user) => listener2.add(user));

      monitor.emitUser(tUser);
      await Future.delayed(const Duration(milliseconds: 100));

      // ASSERT
      expect(listener1, [tUser]);
      expect(listener2, [tUser]);
    });
  });

  group('dispose', () {
    test('should close the stream controller', () {
      // ACT
      monitor.dispose();

      // ASSERT
      expect(
        () => monitor.emitUser(null),
        throwsA(isA<StateError>()),
      );
    });

    test('should complete authStateChanges stream', () async {
      // ARRANGE
      var isCompleted = false;

      monitor.authStateChanges.listen(
        (_) {},
        onDone: () => isCompleted = true,
      );

      // ACT
      monitor.dispose();
      await Future.delayed(const Duration(milliseconds: 100));

      // ASSERT
      expect(isCompleted, isTrue);
    });
  });
}
```

---

## Testing de Storage

### 📁 Archivo fuente: `lib/clean/core/storage/storage_service.dart`

```dart
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

abstract class StorageService {
  Future<void> setString(String key, String value);
  String? getString(String key);
  Future<void> setObject(String key, Map<String, dynamic> value);
  Map<String, dynamic>? getObject(String key);
  Future<void> remove(String key);
  Future<void> clear();
}

class StorageServiceImpl implements StorageService {
  final SharedPreferences preferences;

  StorageServiceImpl({required this.preferences});

  @override
  Future<void> setString(String key, String value) async {
    await preferences.setString(key, value);
  }

  @override
  String? getString(String key) {
    return preferences.getString(key);
  }

  @override
  Future<void> setObject(String key, Map<String, dynamic> value) async {
    await preferences.setString(key, json.encode(value));
  }

  @override
  Map<String, dynamic>? getObject(String key) {
    final string = preferences.getString(key);
    if (string == null) return null;
    return json.decode(string) as Map<String, dynamic>;
  }

  @override
  Future<void> remove(String key) async {
    await preferences.remove(key);
  }

  @override
  Future<void> clear() async {
    await preferences.clear();
  }
}
```

### 🧪 Tests de StorageService

**`test/core/storage/storage_service_test.dart`**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/storage/storage_service.dart';

// Fake de SharedPreferences
class FakeSharedPreferences {
  final Map<String, Object> _storage = {};

  Future<bool> setString(String key, String value) async {
    _storage[key] = value;
    return true;
  }

  String? getString(String key) {
    return _storage[key] as String?;
  }

  Future<bool> remove(String key) async {
    _storage.remove(key);
    return true;
  }

  Future<bool> clear() async {
    _storage.clear();
    return true;
  }
}

void main() {
  late StorageServiceImpl storage;
  late FakeSharedPreferences fakePrefs;

  setUp(() {
    fakePrefs = FakeSharedPreferences();
    storage = StorageServiceImpl(
      preferences: fakePrefs as dynamic,
    );
  });

  group('setString & getString', () {
    test('should store and retrieve string', () async {
      // ARRANGE
      const key = 'test_key';
      const value = 'test_value';

      // ACT
      await storage.setString(key, value);
      final result = storage.getString(key);

      // ASSERT
      expect(result, value);
    });

    test('should return null for non-existent key', () {
      // ACT
      final result = storage.getString('non_existent');

      // ASSERT
      expect(result, isNull);
    });

    test('should overwrite existing value', () async {
      // ARRANGE
      const key = 'test_key';
      await storage.setString(key, 'old_value');

      // ACT
      await storage.setString(key, 'new_value');
      final result = storage.getString(key);

      // ASSERT
      expect(result, 'new_value');
    });
  });

  group('setObject & getObject', () {
    test('should store and retrieve object', () async {
      // ARRANGE
      const key = 'user';
      final value = {
        'id': '123',
        'name': 'John',
        'email': 'john@example.com',
      };

      // ACT
      await storage.setObject(key, value);
      final result = storage.getObject(key);

      // ASSERT
      expect(result, value);
    });

    test('should handle nested objects', () async {
      // ARRANGE
      const key = 'complex';
      final value = {
        'user': {
          'id': '123',
          'profile': {
            'age': 25,
            'country': 'US',
          },
        },
        'settings': {
          'theme': 'dark',
        },
      };

      // ACT
      await storage.setObject(key, value);
      final result = storage.getObject(key);

      // ASSERT
      expect(result, value);
    });
  });

  group('remove', () {
    test('should remove key from storage', () async {
      // ARRANGE
      const key = 'to_remove';
      await storage.setString(key, 'value');

      // ACT
      await storage.remove(key);
      final result = storage.getString(key);

      // ASSERT
      expect(result, isNull);
    });
  });

  group('clear', () {
    test('should remove all keys', () async {
      // ARRANGE
      await storage.setString('key1', 'value1');
      await storage.setString('key2', 'value2');

      // ACT
      await storage.clear();

      // ASSERT
      expect(storage.getString('key1'), isNull);
      expect(storage.getString('key2'), isNull);
    });
  });
}
```

---

## Testing de Utils

### 📁 Archivo fuente: `lib/clean/core/utils/validators.dart`

```dart
class Validators {
  static bool isValidEmail(String email) {
    final regex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return regex.hasMatch(email);
  }

  static bool isValidPassword(String password) {
    return password.length >= 6;
  }

  static bool isNotEmpty(String? value) {
    return value != null && value.trim().isNotEmpty;
  }

  static String? validateEmail(String? email) {
    if (!isNotEmpty(email)) {
      return 'Email is required';
    }
    if (!isValidEmail(email!)) {
      return 'Invalid email format';
    }
    return null;
  }

  static String? validatePassword(String? password) {
    if (!isNotEmpty(password)) {
      return 'Password is required';
    }
    if (!isValidPassword(password!)) {
      return 'Password must be at least 6 characters';
    }
    return null;
  }
}
```

### 🧪 Tests de Validators

**`test/core/utils/validators_test.dart`**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/utils/validators.dart';

void main() {
  group('isValidEmail', () {
    test('should return true for valid email', () {
      expect(Validators.isValidEmail('test@example.com'), isTrue);
      expect(Validators.isValidEmail('user.name@domain.co.uk'), isTrue);
    });

    test('should return false for invalid email', () {
      expect(Validators.isValidEmail('invalid'), isFalse);
      expect(Validators.isValidEmail('test@'), isFalse);
      expect(Validators.isValidEmail('@example.com'), isFalse);
      expect(Validators.isValidEmail('test@.com'), isFalse);
    });

    test('should return false for empty string', () {
      expect(Validators.isValidEmail(''), isFalse);
    });
  });

  group('isValidPassword', () {
    test('should return true for password with 6+ characters', () {
      expect(Validators.isValidPassword('123456'), isTrue);
      expect(Validators.isValidPassword('password123'), isTrue);
    });

    test('should return false for short password', () {
      expect(Validators.isValidPassword('12345'), isFalse);
      expect(Validators.isValidPassword(''), isFalse);
    });
  });

  group('isNotEmpty', () {
    test('should return true for non-empty string', () {
      expect(Validators.isNotEmpty('hello'), isTrue);
      expect(Validators.isNotEmpty('  hello  '), isTrue);
    });

    test('should return false for null', () {
      expect(Validators.isNotEmpty(null), isFalse);
    });

    test('should return false for empty string', () {
      expect(Validators.isNotEmpty(''), isFalse);
      expect(Validators.isNotEmpty('   '), isFalse);
    });
  });

  group('validateEmail', () {
    test('should return null for valid email', () {
      expect(Validators.validateEmail('test@example.com'), isNull);
    });

    test('should return error for empty email', () {
      expect(Validators.validateEmail(''), 'Email is required');
      expect(Validators.validateEmail(null), 'Email is required');
    });

    test('should return error for invalid format', () {
      expect(Validators.validateEmail('invalid'), 'Invalid email format');
    });
  });

  group('validatePassword', () {
    test('should return null for valid password', () {
      expect(Validators.validatePassword('password123'), isNull);
    });

    test('should return error for empty password', () {
      expect(Validators.validatePassword(''), 'Password is required');
      expect(Validators.validatePassword(null), 'Password is required');
    });

    test('should return error for short password', () {
      expect(
        Validators.validatePassword('12345'),
        'Password must be at least 6 characters',
      );
    });
  });
}
```

---

## Ejercicios Prácticos

### Ejercicio 1: Test de DateUtils

Crea tests para una clase `DateUtils` que formatee fechas:

```dart
class DateUtils {
  static String formatDate(DateTime date) => // Implementa
  static bool isToday(DateTime date) => // Implementa
  static DateTime addDays(DateTime date, int days) => // Implementa
}
```

### Ejercicio 2: Test de NotificationService

Escribe tests para un servicio que maneje notificaciones locales:

```dart
abstract class NotificationService {
  Future<void> showNotification(String title, String body);
  Future<void> scheduleNotification(DateTime when, String title, String body);
  Future<void> cancelAll();
}
```

### Ejercicio 3: Test de Logger

Crea tests para un logger simple:

```dart
class Logger {
  void log(String message);
  List<String> get logs;
  void clear();
}
```

---

## ✅ Checklist de Core Testing

- [ ] Testear NetworkInfo (online/offline)
- [ ] Testear Streams y eventos
- [ ] Testear Storage (CRUD completo)
- [ ] Testear funciones puras (validators)
- [ ] Testear servicios con estado
- [ ] Cerrar recursos en tearDown
- [ ] Testear edge cases (null, vacío)

---

## 🚀 Siguiente Paso

➡️ **Parte 6: Testing Avanzado (Fixtures, Integration, Coverage)**

Aprenderás a:
- Organizar fixtures reutilizables
- Escribir integration tests
- Medir cobertura de código
- Automatizar tests con CI/CD

---

## 💡 Tips Adicionales

### 1. **Streams en Tests**
```dart
// Testear múltiples emisiones
expectLater(
  stream,
  emitsInOrder([1, 2, 3]),
);

// Testear que se completa
expectLater(
  stream,
  emitsDone,
);
```

### 2. **Async/Await**
```dart
// Testear Future
expectLater(
  future,
  completion(equals(expected)),
);

// Testear timeout
timeout: const Duration(seconds: 5)
```

### 3. **Comandos útiles**
```bash
# Tests de core
flutter test test/core/

# Con coverage
flutter test --coverage test/core/
```
