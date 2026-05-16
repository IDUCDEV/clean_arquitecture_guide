# 🏋️ 03b: Práctica - DataSources (Remote y Local)

> **¿De qué trata esta práctica?** De testear los DataSources usando **Mocktail** para simular HTTP Client y SharedPreferences sin hacer llamadas reales.

---

## 📋 Ejercicios

- [Ejercicio 1: Testear Remote DataSource con Mocktail](#ejercicio-1-testear-remote-datasource-con-mocktail)
- [Ejercicio 2: Testear Local DataSource con Mocktail](#ejercicio-2-testear-local-datasource-con-mocktail)

---

## 🎬 Antes de Empezar

Asegúrate de tener estas dependencias en pubspec.yaml:

```yaml
dependencies:
  http: ^1.0.0
  shared_preferences: ^2.0.0

dev_dependencies:
  mocktail: ^1.0.4
```

```bash
flutter pub get
```

---

## Ejercicio 1: Testear Remote DataSource con Mocktail

### 📝 Tu Misión

Testear el Remote DataSource usando Mocktail para simular el HTTP Client.

### ✅ Paso 1: Crea la estructura

```bash
mkdir -p test/features/auth/data/datasources
touch test/features/auth/data/datasources/auth_remote_data_source_test.dart
```

### ✅ Paso 2: Configura el test base con Mocktail

```dart
// test/features/auth/data/datasources/auth_remote_data_source_test.dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mocktail/mocktail.dart';
import 'package:mi_proyecto_flutter/clean/core/error/exceptions.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';

import '../../../../helpers/fixture_reader.dart';

class MockClient extends Mock implements http.Client {}

void main() {
  late AuthRemoteDataSourceImpl dataSource;
  late MockClient mockClient;
  const baseUrl = 'https://api.example.com';

  setUp(() {
    mockClient = MockClient();
    dataSource = AuthRemoteDataSourceImpl(
      client: mockClient,
      baseUrl: baseUrl,
    );
  });

  group('login', () {
    const tEmail = 'test@example.com';
    const tPassword = 'password123';
    final tUserJson = fixtureAsMap('user');

    // Tests van aquí...
  });
}
```

### ✅ Paso 3: Test - Respuesta exitosa (200)

```dart
    test('should return UserModel when response is 200', () async {
      // ═══════════════════════════════════════════════════════════
      // ARRANGE: Configurar el Mock para retornar éxito
      // ═══════════════════════════════════════════════════════════
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response(
        json.encode(tUserJson),
        200,
      ));

      // ═══════════════════════════════════════════════════════════
      // ACT: Llamar al DataSource
      // ═══════════════════════════════════════════════════════════
      final result = await dataSource.login(tEmail, tPassword);

      // ═══════════════════════════════════════════════════════════
      // ASSERT: Verificar resultado
      // ═══════════════════════════════════════════════════════════
      expect(result.id, '123');
      expect(result.email, 'test@example.com');
      expect(result.name, 'John');
    });
```

### ✅ Paso 4: Test - Verificar endpoint y método

```dart
    test('should call correct endpoint with POST', () async {
      // Arrange
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response(
        json.encode(tUserJson),
        200,
      ));

      // Act
      await dataSource.login(tEmail, tPassword);

      // Assert
      verify(() => mockClient.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).called(1);
    });
```

### ✅ Paso 5: Test - Error 401 (Unauthorized)

```dart
    test('should throw ServerException when response is 401', () async {
      // Arrange
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response(
        json.encode({'error': 'Unauthorized'}),
        401,
      ));

      // Act & Assert
      expect(
        () => dataSource.login(tEmail, tPassword),
        throwsA(
          isA<ServerException>().having(
            (e) => e.statusCode,
            'statusCode',
            401,
          ),
        ),
      );
    });
```

### ✅ Paso 6: Test - Error 500 (Server Error)

```dart
    test('should throw ServerException when response is 500', () async {
      // Arrange
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response('Internal Server Error', 500));

      // Act & Assert
      expect(
        () => dataSource.login(tEmail, tPassword),
        throwsA(isA<ServerException>()),
      );
    });
```

### ✅ Paso 7: Test - Error de red

```dart
    test('should throw Exception on network error', () async {
      // Arrange
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenThrow(Exception('No internet'));

      // Act & Assert
      expect(
        () => dataSource.login(tEmail, tPassword),
        throwsA(isA<Exception>()),
      );
    });
```

### 🧪 Ejecuta los tests

```bash
flutter test test/features/auth/data/datasources/auth_remote_data_source_test.dart
```

---

## Ejercicio 2: Testear Local DataSource con Mocktail

### 📝 Tu Misión

Testear el Local DataSource usando Mocktail para simular SharedPreferences.

### ✅ Paso 1: Crea el test

```bash
touch test/features/auth/data/datasources/auth_local_data_source_test.dart
```

### ✅ Paso 2: Configura el test base con Mocktail

```dart
// test/features/auth/data/datasources/auth_local_data_source_test.dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mi_proyecto_flutter/clean/core/error/exceptions.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';

class MockSharedPreferences extends Mock implements SharedPreferences {}

void main() {
  late AuthLocalDataSourceImpl dataSource;
  late MockSharedPreferences mockPreferences;

  setUp(() {
    mockPreferences = MockSharedPreferences();
    dataSource = AuthLocalDataSourceImpl(preferences: mockPreferences);
  });

  const tUserModel = UserModel(
    id: '123',
    email: 'test@example.com',
    name: 'John',
    lastName: 'Doe',
  );

  // Tests van aquí...
}
```

### ✅ Paso 3: Test - Guardar usuario en cache

```dart
  group('cacheUser', () {
    test('should store user in SharedPreferences', () async {
      // Arrange
      when(() => mockPreferences.setString(any(), any()))
          .thenAnswer((_) async => true);

      // Act
      await dataSource.cacheUser(tUserModel);

      // Assert
      verify(() => mockPreferences.setString(
        'CACHED_USER',
        any(),
      )).called(1);
    });

    test('should throw CacheException when storage fails', () async {
      // Arrange
      when(() => mockPreferences.setString(any(), any()))
          .thenAnswer((_) async => false);

      // Act & Assert
      expect(
        () => dataSource.cacheUser(tUserModel),
        throwsA(isA<CacheException>()),
      );
    });
  });
```

### ✅ Paso 4: Test - Obtener usuario de cache

```dart
  group('getUser', () {
    test('should return UserModel when user is cached', () async {
      // Arrange
      when(() => mockPreferences.getString(any())).thenAnswer(
        (_) async => json.encode(tUserModel.toJson()),
      );

      // Act
      final result = await dataSource.getUser();

      // Assert
      expect(result, equals(tUserModel));
    });

    test('should return null when no user is cached', () async {
      // Arrange
      when(() => mockPreferences.getString(any())).thenAnswer(
        (_) async => null,
      );

      // Act
      final result = await dataSource.getUser();

      // Assert
      expect(result, isNull);
    });

    test('should throw CacheException when JSON is invalid', () async {
      // Arrange
      when(() => mockPreferences.getString(any())).thenAnswer(
        (_) async => 'invalid json',
      );

      // Act & Assert
      expect(
        () => dataSource.getUser(),
        throwsA(isA<CacheException>()),
      );
    });
  });
```

### ✅ Paso 5: Test - Limpiar cache

```dart
  group('clearUser', () {
    test('should remove user from storage', () async {
      // Arrange
      when(() => mockPreferences.remove(any())).thenAnswer(
        (_) async => true,
      );

      // Act
      await dataSource.clearUser();

      // Assert
      verify(() => mockPreferences.remove('CACHED_USER')).called(1);
    });
  });

  group('hasUser', () {
    test('should return true when user is cached', () async {
      // Arrange
      when(() => mockPreferences.containsKey(any())).thenAnswer(
        (_) async => true,
      );

      // Act
      final result = await dataSource.hasUser();

      // Assert
      expect(result, isTrue);
    });

    test('should return false when no user is cached', () async {
      // Arrange
      when(() => mockPreferences.containsKey(any())).thenAnswer(
        (_) async => false,
      );

      // Act
      final result = await dataSource.hasUser();

      // Assert
      expect(result, isFalse);
    });
  });
```

### 🧪 Ejecuta los tests

```bash
flutter test test/features/auth/data/datasources/auth_local_data_source_test.dart
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Tests Remote DataSource con Mocktail (6 tests)
- [ ] Ejercicio 2: Tests Local DataSource con Mocktail (7 tests)
- [ ] **Total: 13 tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:

- ✅ Usar Mocktail para simular HTTP Client en tests de Remote DataSource
- ✅ Usar Mocktail para simular SharedPreferences en tests de Local DataSource
- ✅ Testear casos de éxito, error HTTP y error de red
- ✅ Testear guardado, obtención y limpieza de cache local
- ✅ Verificar interacciones con `verify()` y `verifyNever()`

---

## 🚀 Siguiente Paso

**Práctica:** [03c-practica-repositories.md](./03c-practica-repositories.md)

> En esta práctica aprenderás a testear el **Repository Implementation** que coordina todo.
