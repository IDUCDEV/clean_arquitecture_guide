# 🏋️ 03b: Práctica - DataSources (Remote y Local)

> **¿De qué trata esta práctica?** De testear los DataSources: el Remote que se conecta a APIs y el Local que guarda datos en caché.

---

## 📋 Ejercicios

- [Ejercicio 1: Crear Fake HTTP Client](#ejercicio-1-crear-fake-http-client)
- [Ejercicio 2: Testear Remote DataSource](#ejercicio-2-testear-remote-datasource)
- [Ejercicio 3: Crear Fake SharedPreferences](#ejercicio-3-crear-fake-sharedpreferences)
- [Ejercicio 4: Testear Local DataSource](#ejercicio-4-testear-local-datasource)

---

## 🎬 Antes de Empezar

Asegúrate de tener estas dependencias en pubspec.yaml:

```yaml
dependencies:
  http: ^1.0.0
  shared_preferences: ^2.0.0
```

```bash
flutter pub get
```

---

## Ejercicio 1: Crear Fake HTTP Client

### 📝 Tu Misión

Crear un Fake del HTTP Client para simular respuestas del servidor.

### ✅ Paso 1: Crea el archivo

```bash
touch test/helpers/fake_http_client.dart
```

### ✅ Paso 2: Implementa el Fake

```dart
// test/helpers/fake_http_client.dart
import 'package:http/http.dart' as http;

/// Fake HTTP Client para testing
/// Simula las respuestas del servidor sin hacer llamadas reales
class FakeHttpClient extends http.BaseClient {
  /// Respuesta que retornará el próximo request
  http.Response? responseToReturn;
  
  /// Excepción que lanzará el próximo request
  Exception? exceptionToThrow;
  
  // ═══════════════════════════════════════════════════════════
  // SEGUIMIENTO - Para verificar qué se llamó
  // ═══════════════════════════════════════════════════════════
  
  /// Última URL llamada
  Uri? lastUri;
  
  /// Últimos headers enviados
  Map<String, String>? lastHeaders;
  
  /// Último body enviado
  String? lastBody;
  
  /// Último método usado (GET, POST, etc.)
  String? lastMethod;

  /// Simula una request GET
  @override
  Future<http.Response> get(Uri url, {Map<String, String>? headers}) async {
    lastUri = url;
    lastHeaders = headers;
    lastMethod = 'GET';
    
    if (exceptionToThrow != null) throw exceptionToThrow!;
    return responseToReturn!;
  }

  /// Simula una request POST
  @override
  Future<http.Response> post(
    Uri url, {
    Map<String, String>? headers,
    Object? body,
    Encoding? encoding,
  }) async {
    lastUri = url;
    lastHeaders = headers;
    lastBody = body as String?;
    lastMethod = 'POST';
    
    if (exceptionToThrow != null) throw exceptionToThrow!;
    return responseToReturn!;
  }

  /// Simula una request PUT
  @override
  Future<http.Response> put(
    Uri url, {
    Map<String, String>? headers,
    Object? body,
    Encoding? encoding,
  }) async {
    lastUri = url;
    lastHeaders = headers;
    lastBody = body as String?;
    lastMethod = 'PUT';
    
    if (exceptionToThrow != null) throw exceptionToThrow!;
    return responseToReturn!;
  }

  /// Simula una request DELETE
  @override
  Future<http.Response> delete(Uri url, {Map<String, String>? headers}) async {
    lastUri = url;
    lastHeaders = headers;
    lastMethod = 'DELETE';
    
    if (exceptionToThrow != null) throw exceptionToThrow!;
    return responseToReturn!;
  }

  /// Reset del estado
  void reset() {
    responseToReturn = null;
    exceptionToThrow = null;
    lastUri = null;
    lastHeaders = null;
    lastBody = null;
    lastMethod = null;
  }
}
```

### 🧪 Verifica

```bash
dart analyze test/helpers/fake_http_client.dart
```

---

## Ejercicio 2: Testear Remote DataSource

### 📝 Tu Misión

Escribir tests para el Remote DataSource usando el Fake HTTP Client.

### ✅ Paso 1: Crea la estructura

```bash
mkdir -p test/features/auth/data/datasources
touch test/features/auth/data/datasources/auth_remote_data_source_test.dart
```

### ✅ Paso 2: Configura el test base

```dart
// test/features/auth/data/datasources/auth_remote_data_source_test.dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mi_proyecto_flutter/clean/core/error/exceptions.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';

import '../../../../helpers/fake_http_client.dart';
import '../../../../helpers/fixture_reader.dart';

void main() {
  late AuthRemoteDataSourceImpl dataSource;
  late FakeHttpClient fakeClient;
  const baseUrl = 'https://api.example.com';

  setUp(() {
    fakeClient = FakeHttpClient();
    dataSource = AuthRemoteDataSourceImpl(
      client: fakeClient,
      baseUrl: baseUrl,
    );
  });

  tearDown(() {
    fakeClient.reset();
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
      // ARRANGE: Configurar el Fake para retornar éxito
      // ═══════════════════════════════════════════════════════════
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        200,
        headers: {'content-type': 'application/json'},
      );

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
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        200,
      );

      // Act
      await dataSource.login(tEmail, tPassword);

      // Assert
      expect(fakeClient.lastMethod, 'POST');
      expect(fakeClient.lastUri, Uri.parse('$baseUrl/auth/login'));
    });
```

### ✅ Paso 5: Test - Verificar body enviado

```dart
    test('should send correct body', () async {
      // Arrange
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        200,
      );

      // Act
      await dataSource.login(tEmail, tPassword);

      // Assert
      final bodyJson = json.decode(fakeClient.lastBody!) as Map<String, dynamic>;
      expect(bodyJson['email'], tEmail);
      expect(bodyJson['password'], tPassword);
    });
```

### ✅ Paso 6: Test - Verificar headers

```dart
    test('should send Content-Type header', () async {
      // Arrange
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        200,
      );

      // Act
      await dataSource.login(tEmail, tPassword);

      // Assert
      expect(fakeClient.lastHeaders?['Content-Type'], 'application/json');
    });
```

### ✅ Paso 7: Test - Error 401 (Unauthorized)

```dart
    test('should throw ServerException when response is 401', () async {
      // Arrange
      fakeClient.responseToReturn = http.Response(
        json.encode({'error': 'Unauthorized'}),
        401,
      );

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

### ✅ Paso 8: Test - Error 500 (Server Error)

```dart
    test('should throw ServerException when response is 500', () async {
      // Arrange
      fakeClient.responseToReturn = http.Response('Internal Server Error', 500);

      // Act & Assert
      expect(
        () => dataSource.login(tEmail, tPassword),
        throwsA(isA<ServerException>()),
      );
    });
```

### ✅ Paso 9: Test - Error de red

```dart
    test('should throw Exception on network error', () async {
      // Arrange
      fakeClient.exceptionToThrow = Exception('No internet');

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

## Ejercicio 3: Crear Fake SharedPreferences

### 📝 Tu Misión

Crear un Fake de SharedPreferences para simular almacenamiento local.

### ✅ Paso 1: Crea el archivo

```bash
touch test/helpers/fake_shared_preferences.dart
```

### ✅ Paso 2: Implementa el Fake

```dart
// test/helpers/fake_shared_preferences.dart

/// Fake SharedPreferences para testing
/// Simula el almacenamiento local sin necesidad de permisos
class FakeSharedPreferences {
  /// Almacenamiento interno (como un Map)
  final Map<String, Object> _storage = {};
  
  /// Cuando es true, setString retornará false
  bool shouldFail = false;

  /// Obtiene un String del almacenamiento
  String? getString(String key) {
    return _storage[key] as String?;
  }

  /// Guarda un String en el almacenamiento
  Future<bool> setString(String key, String value) async {
    if (shouldFail) return false;
    _storage[key] = value;
    return true;
  }

  /// Elimina una clave
  Future<bool> remove(String key) async {
    _storage.remove(key);
    return true;
  }

  /// Verifica si existe una clave
  bool containsKey(String key) {
    return _storage.containsKey(key);
  }

  /// Limpia todo el almacenamiento
  void clear() {
    _storage.clear();
    shouldFail = false;
  }
}
```

---

## Ejercicio 4: Testear Local DataSource

### 📝 Tu Misión

Escribir tests para el Local DataSource usando el Fake SharedPreferences.

### ✅ Paso 1: Crea el test

```bash
touch test/features/auth/data/datasources/auth_local_data_source_test.dart
```

### ✅ Paso 2: Configura el test base

```dart
// test/features/auth/data/datasources/auth_local_data_source_test.dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/error/exceptions.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';

import '../../../../helpers/fake_shared_preferences.dart';

void main() {
  late AuthLocalDataSourceImpl dataSource;
  late FakeSharedPreferences fakePreferences;

  setUp(() {
    fakePreferences = FakeSharedPreferences();
    // Nota: En un test real, necesitarás un wrapper o cast
    dataSource = AuthLocalDataSourceImpl(
      preferences: _FakePreferencesAdapter(fakePreferences),
    );
  });

  tearDown(() {
    fakePreferences.clear();
  });

  // Tests van aquí...
}
```

> **Nota:** Necesitarás un adapter simple para usar FakeSharedPreferences con SharedPreferences:

```dart
// Helper para adaptar FakeSharedPreferences
class _FakePreferencesAdapter implements SharedPreferences {
  final FakeSharedPreferences _fake;
  
  _FakePreferencesAdapter(this._fake);
  
  @override
  String? getString(String key) => _fake.getString(key);
  
  @override
  Future<bool> setString(String key, String value) => _fake.setString(key, value);
  
  @override
  Future<bool> remove(String key) => _fake.remove(key);
  
  @override
  bool containsKey(String key) => _fake.containsKey(key);
  
  // Implementa otros métodos si son necesarios...
}
```

### ✅ Paso 3: Test - Guardar usuario en cache

```dart
  const tUserModel = UserModel(
    id: '123',
    email: 'test@example.com',
    name: 'John',
    lastName: 'Doe',
  );

  group('cacheUser', () {
    test('should store user in SharedPreferences', () async {
      // Act
      await dataSource.cacheUser(tUserModel);

      // Assert
      final jsonString = fakePreferences.getString('CACHED_USER');
      expect(jsonString, isNotNull);
      
      final jsonMap = json.decode(jsonString!) as Map<String, dynamic>;
      expect(jsonMap['id'], tUserModel.id);
      expect(jsonMap['email'], tUserModel.email);
    });

    test('should throw CacheException when storage fails', () async {
      // Arrange
      fakePreferences.shouldFail = true;

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
      await fakePreferences.setString(
        'CACHED_USER',
        json.encode(tUserModel.toJson()),
      );

      // Act
      final result = await dataSource.getUser();

      // Assert
      expect(result, equals(tUserModel));
    });

    test('should return null when no user is cached', () async {
      // Act
      final result = await dataSource.getUser();

      // Assert
      expect(result, isNull);
    });

    test('should throw CacheException when JSON is invalid', () async {
      // Arrange
      await fakePreferences.setString('CACHED_USER', 'invalid json');

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
      await fakePreferences.setString(
        'CACHED_USER',
        json.encode(tUserModel.toJson()),
      );

      // Act
      await dataSource.clearUser();

      // Assert
      expect(fakePreferences.containsKey('CACHED_USER'), isFalse);
    });
  });

  group('hasUser', () {
    test('should return true when user is cached', () async {
      // Arrange
      await fakePreferences.setString(
        'CACHED_USER',
        json.encode(tUserModel.toJson()),
      );

      // Act
      final result = await dataSource.hasUser();

      // Assert
      expect(result, isTrue);
    });

    test('should return false when no user is cached', () async {
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

- [ ] Ejercicio 1: Fake HTTP Client creado
- [ ] Ejercicio 2: Tests Remote DataSource (9 tests)
- [ ] Ejercicio 3: Fake SharedPreferences creado
- [ ] Ejercicio 4: Tests Local DataSource (6 tests)
- [ ] **Total: 15+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Crear un Fake HTTP Client para simular APIs
- ✅ Testear Remote DataSource (éxito, errores, parámetros)
- ✅ Crear un Fake de SharedPreferences para simular cache
- ✅ Testear Local DataSource (guardar, obtener, limpiar)
- ✅ Testear manejo de errores (excepciones)

---

## ⚡ Alternativa: Testear Local DataSource con Isar

> Esta sección muestra cómo testear un Local DataSource usando **Isar** en lugar de SharedPreferences.

### 📝 Diferencias Clave

| Aspecto | SharedPreferences | Isar |
|---------|-------------------|------|
| Tipo de datos | Solo strings/primitivos | Objetos complejos |
| Queries | No | Sí, con filtros |
| Streams reactivos | No | Sí |
| Tests | Fake manual | Isar.inMemory |

### ✅ Paso 1: Setup para Tests con Isar

```dart
// test/helpers/isar_test_helper.dart
import 'package:isar_community/isar_community.dart';
import 'package:mi_proyecto_flutter/features/user/data/models/user_model.dart';

/// Helper para crear Isar en memoria para testing
class IsarTestHelper {
  static Future<Isar> createIsar() async {
    await Isar.initializeIsarCore(download: true);
    
    return await Isar.open(
      [UserModelSchema],
      directory: '',
      name: 'test_${DateTime.now().millisecondsSinceEpoch}',
    );
  }
}
```

### ✅ Paso 2: Test del Local DataSource con Isar

```dart
// test/features/user/data/datasources/user_local_data_source_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:isar_community/isar_community.dart';
import 'package:mi_proyecto_flutter/features/user/data/datasources/user_local_data_source.dart';
import 'package:mi_proyecto_flutter/features/user/data/models/user_model.dart';

import '../../../../helpers/isar_test_helper.dart';

void main() {
  late UserLocalDataSourceImpl dataSource;
  late Isar isar;

  setUpAll(() async {
    await Isar.initializeIsarCore(download: true);
  });

  setUp(() async {
    isar = await IsarTestHelper.createIsar();
    dataSource = UserLocalDataSourceImpl(isar);
  });

  tearDown(() async {
    await isar.close(deleteFromDisk: true);
  });

  group('UserLocalDataSource with Isar', () {
    final tUserModel = UserModel(
      name: 'John',
      email: 'john@example.com',
      isActive: true,
    );

    group('saveUser', () {
      test('should save user to Isar database', () async {
        // Act
        final id = await dataSource.saveUser(tUserModel);

        // Assert
        expect(id, isPositive);
        final savedUser = await isar.userModels.get(id);
        expect(savedUser?.name, 'John');
        expect(savedUser?.email, 'john@example.com');
      });

      test('should update existing user', () async {
        // Arrange
        final id = await dataSource.saveUser(tUserModel);
        final updatedUser = UserModel(
          id: id,
          name: 'Jane',
          email: 'jane@example.com',
        );

        // Act
        await dataSource.saveUser(updatedUser);

        // Assert
        final savedUser = await isar.userModels.get(id);
        expect(savedUser?.name, 'Jane');
      });
    });

    group('getUser', () {
      test('should return user by id', () async {
        // Arrange
        final id = await dataSource.saveUser(tUserModel);

        // Act
        final result = await dataSource.getUser(id);

        // Assert
        expect(result, isNotNull);
        expect(result?.name, 'John');
      });

      test('should return null for non-existent id', () async {
        // Act
        final result = await dataSource.getUser(999999);

        // Assert
        expect(result, isNull);
      });
    });

    group('getUsers', () {
      test('should return all users', () async {
        // Arrange
        await dataSource.saveUser(tUserModel);
        await dataSource.saveUser(UserModel(
          name: 'Jane',
          email: 'jane@example.com',
        ));

        // Act
        final result = await dataSource.getUsers();

        // Assert
        expect(result.length, 2);
      });

      test('should return empty list when no users', () async {
        // Act
        final result = await dataSource.getUsers();

        // Assert
        expect(result, isEmpty);
      });
    });

    group('deleteUser', () {
      test('should delete user by id', () async {
        // Arrange
        final id = await dataSource.saveUser(tUserModel);

        // Act
        await dataSource.deleteUser(id);

        // Assert
        final result = await isar.userModels.get(id);
        expect(result, isNull);
      });
    });
  });
}
```

### 🧪 Ejecuta los tests

```bash
flutter test -j 1 test/features/user/data/datasources/user_local_data_source_test.dart
```

> **Nota**: Usa `-j 1` para evitar problemas con la descarga automática de Isar Core en paralelo.

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Fake HTTP Client creado
- [ ] Ejercicio 2: Tests Remote DataSource (9 tests)
- [ ] Ejercicio 3: Fake SharedPreferences creado
- [ ] Ejercicio 4: Tests Local DataSource (6 tests)
- [ ] Alternativa Isar: Tests Local DataSource con Isar
- [ ] **Total: 15+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Crear un Fake HTTP Client para simular APIs
- ✅ Testear Remote DataSource (éxito, errores, parámetros)
- ✅ Crear un Fake de SharedPreferences para simular cache
- ✅ Testear Local DataSource (guardar, obtener, limpiar)
- ✅ Testear Local DataSource con Isar (alternativa moderna)
- ✅ Testear manejo de errores (excepciones)

---

## 🚀 Siguiente Paso

**Práctica:** [03c-practica-repositories.md](./03c-practica-repositories.md)

> En esta práctica aprenderás a testear el **Repository Implementation** que coordina todo.
