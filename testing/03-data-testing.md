# 🧪 Parte 3: Testing Data (Models, Repositories, DataSources)

## 📋 Índice
1. [Introducción a la Capa Data](#introducción-a-la-capa-data)
2. [Fixtures JSON](#fixtures-json)
3. [Testing de Models](#testing-de-models)
4. [Testing de Remote DataSources](#testing-de-remote-datasources)
5. [Testing de Local DataSources](#testing-de-local-datasources)
6. [Testing de Repository Implementation](#testing-de-repository-implementation)
7. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Introducción a la Capa Data

La capa **Data** es responsable de:
- **Models**: Mapeo de datos JSON a objetos Dart
- **DataSources**: Comunicación con APIs y almacenamiento local
- **Repository Implementation**: Lógica de decisión (online/offline)

### 🎯 Por qué es más compleja de testear:

- ✅ **Dependencias externas**: HTTP, SharedPreferences, SQLite
- ✅ **Manejo de errores**: Timeouts, parsing errors, network errors
- ✅ **Async/await**: Código asíncrono complejo
- ✅ **Estados de red**: Online vs Offline

### 📦 Arquitectura de la capa Data:

```
Data Layer
├── Models          ← Mapeo JSON ↔ Dart
│   └── user_model.dart
├── DataSources     ← Origen de datos
│   ├── Remote      ← HTTP/Supabase
│   └── Local       ← SharedPreferences/SQLite
└── Repositories    ← Lógica de negocio + cache
    └── auth_repository_impl.dart
```

---

## Fixtures JSON

Los **fixtures** son archivos JSON con datos de prueba reutilizables.

### 📁 Estructura de carpetas

```
test/
├── fixtures/
│   ├── user.json              ← Usuario individual
│   ├── users_list.json        ← Lista de usuarios
│   └── auth_response.json     ← Respuesta de login
└── helpers/
    └── fixture_reader.dart    ← Helper para leer fixtures
```

### 📝 Paso 1: Crear archivos de fixtures

**`test/fixtures/user.json`**
```json
{
  "id": "123",
  "email": "test@example.com",
  "name": "John",
  "last_name": "Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**`test/fixtures/users_list.json`**
```json
[
  {
    "id": "123",
    "email": "user1@example.com",
    "name": "John",
    "last_name": "Doe"
  },
  {
    "id": "456",
    "email": "user2@example.com",
    "name": "Jane",
    "last_name": "Smith"
  }
]
```

**`test/fixtures/auth_response.json`**
```json
{
  "user": {
    "id": "789",
    "email": "new@example.com",
    "name": "Alice",
    "last_name": "Johnson"
  },
  "token": "jwt_token_here",
  "expires_at": "2024-12-31T23:59:59Z"
}
```

### 📝 Paso 2: Crear el helper

**`test/helpers/fixture_reader.dart`**
```dart
import 'dart:io';

/// Lee un archivo fixture JSON de la carpeta test/fixtures/
/// 
/// Uso: 
/// ```dart
/// final jsonString = fixture('user');
/// final jsonMap = json.decode(jsonString);
/// ```
String fixture(String name) {
  final file = File('test/fixtures/$name.json');
  if (!file.existsSync()) {
    throw Exception('Fixture not found: test/fixtures/$name.json');
  }
  return file.readAsStringSync();
}

/// Lee un fixture y lo decodifica como Map
Map<String, dynamic> fixtureAsMap(String name) {
  final content = fixture(name);
  return json.decode(content) as Map<String, dynamic>;
}

/// Lee un fixture y lo decodifica como List
List<dynamic> fixtureAsList(String name) {
  final content = fixture(name);
  return json.decode(content) as List<dynamic>;
}
```

---

## Testing de Models

### 📁 Archivo fuente: `lib/clean/features/auth/data/models/user_model.dart`

```dart
import 'package:sereni/clean/features/auth/domain/entities/user.dart';

class UserModel extends User {
  const UserModel({
    required String id,
    required String email,
    required String name,
    required String lastName,
  }) : super(
          id: id,
          email: email,
          name: name,
          lastName: lastName,
        );

  /// Deserializa desde JSON
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String,
      lastName: json['last_name'] as String,
    );
  }

  /// Serializa a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'last_name': lastName,
    };
  }

  /// Convierte a Entity (Domain)
  User toEntity() {
    return User(
      id: id,
      email: email,
      name: name,
      lastName: lastName,
    );
  }

  /// Crea desde Entity (Domain)
  factory UserModel.fromEntity(User user) {
    return UserModel(
      id: user.id,
      email: user.email,
      name: user.name,
      lastName: user.lastName,
    );
  }
}
```

### 🧪 Tests completos del Model

**`test/features/auth/data/models/user_model_test.dart`**

```dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/features/auth/data/models/user_model.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';

import '../../../../helpers/fixture_reader.dart';

void main() {
  const tUserModel = UserModel(
    id: '123',
    email: 'test@example.com',
    name: 'John',
    lastName: 'Doe',
  );

  group('UserModel', () {
    test('should be a subclass of User entity', () {
      // ASSERT
      expect(tUserModel, isA<User>());
    });

    group('fromJson', () {
      test('should return valid model from JSON', () {
        // ARRANGE
        final Map<String, dynamic> jsonMap = 
            json.decode(fixture('user')) as Map<String, dynamic>;

        // ACT
        final result = UserModel.fromJson(jsonMap);

        // ASSERT
        expect(result, equals(tUserModel));
      });

      test('should return valid model with different data', () {
        // ARRANGE
        final jsonMap = {
          'id': '456',
          'email': 'jane@example.com',
          'name': 'Jane',
          'last_name': 'Smith',
        };

        // ACT
        final result = UserModel.fromJson(jsonMap);

        // ASSERT
        expect(result.id, '456');
        expect(result.email, 'jane@example.com');
        expect(result.name, 'Jane');
        expect(result.lastName, 'Smith');
      });

      test('should throw when required field is missing', () {
        // ARRANGE
        final jsonMap = {
          'id': '123',
          'email': 'test@example.com',
          // Falta 'name' y 'last_name'
        };

        // ACT & ASSERT
        expect(
          () => UserModel.fromJson(jsonMap),
          throwsA(isA<TypeError>()),
        );
      });

      test('should handle extra fields gracefully', () {
        // ARRANGE
        final jsonMap = {
          'id': '123',
          'email': 'test@example.com',
          'name': 'John',
          'last_name': 'Doe',
          'extra_field': 'ignored',
        };

        // ACT
        final result = UserModel.fromJson(jsonMap);

        // ASSERT
        expect(result, equals(tUserModel));
      });
    });

    group('toJson', () {
      test('should return a valid JSON map', () {
        // ARRANGE - tUserModel definido arriba

        // ACT
        final result = tUserModel.toJson();

        // ASSERT
        final expectedMap = {
          'id': '123',
          'email': 'test@example.com',
          'name': 'John',
          'last_name': 'Doe',
        };
        expect(result, equals(expectedMap));
      });

      test('toJson and fromJson should be inverse operations', () {
        // ARRANGE
        final original = tUserModel;

        // ACT
        final json = original.toJson();
        final recreated = UserModel.fromJson(json);

        // ASSERT
        expect(recreated, equals(original));
      });
    });

    group('toEntity', () {
      test('should return a User entity with correct data', () {
        // ARRANGE
        const model = UserModel(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );

        // ACT
        final result = model.toEntity();

        // ASSERT
        expect(result, isA<User>());
        expect(result.id, '123');
        expect(result.email, 'test@example.com');
        expect(result.name, 'John');
        expect(result.lastName, 'Doe');
      });

      test('should create User that is equal to expected entity', () {
        // ARRANGE
        const model = tUserModel;
        const expectedEntity = User(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );

        // ACT
        final result = model.toEntity();

        // ASSERT
        expect(result, equals(expectedEntity));
      });
    });

    group('fromEntity', () {
      test('should return UserModel from User entity', () {
        // ARRANGE
        const entity = User(
          id: '789',
          email: 'entity@example.com',
          name: 'Entity',
          lastName: 'User',
        );

        // ACT
        final result = UserModel.fromEntity(entity);

        // ASSERT
        expect(result, isA<UserModel>());
        expect(result.id, '789');
        expect(result.email, 'entity@example.com');
      });

      test('fromEntity and toEntity should preserve data', () {
        // ARRANGE
        const originalModel = tUserModel;

        // ACT
        final entity = originalModel.toEntity();
        final recreatedModel = UserModel.fromEntity(entity);

        // ASSERT
        expect(recreatedModel, equals(originalModel));
      });
    });

    group('equality', () {
      test('should be equal when all fields match', () {
        // ARRANGE
        const model1 = UserModel(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );
        const model2 = UserModel(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );

        // ASSERT
        expect(model1, equals(model2));
      });

      test('should not be equal when fields differ', () {
        // ARRANGE
        const model1 = UserModel(
          id: '123',
          email: 'test1@example.com',
          name: 'John',
          lastName: 'Doe',
        );
        const model2 = UserModel(
          id: '123',
          email: 'test2@example.com',
          name: 'John',
          lastName: 'Doe',
        );

        // ASSERT
        expect(model1, isNot(equals(model2)));
      });
    });
  });
}
```

### 🎓 Qué testear en Models:

1. **fromJson**: Deserialización correcta, campos faltantes, campos extra
2. **toJson**: Serialización correcta, inversión con fromJson
3. **toEntity**: Conversión a Domain, preservación de datos
4. **fromEntity**: Creación desde Domain, round-trip
5. **Equality**: Comparación de modelos

---

## Testing de Remote DataSources

Los **Remote DataSources** se comunican con APIs externas (HTTP/Supabase).

### 📁 Archivo fuente: `lib/clean/features/auth/data/datasources/auth_remote_data_source.dart`

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:sereni/clean/core/error/exceptions.dart';
import 'package:sereni/clean/features/auth/data/models/user_model.dart';

abstract class AuthRemoteDataSource {
  Future<UserModel> login(String email, String password);
  Future<UserModel> register({
    required String email,
    required String password,
    required String name,
    required String lastName,
  });
  Future<void> logout();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final http.Client client;
  final String baseUrl;

  AuthRemoteDataSourceImpl({
    required this.client,
    required this.baseUrl,
  });

  @override
  Future<UserModel> login(String email, String password) async {
    final response = await client.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      return UserModel.fromJson(
        json.decode(response.body) as Map<String, dynamic>,
      );
    } else {
      throw ServerException(
        message: 'Login failed: ${response.statusCode}',
        statusCode: response.statusCode,
      );
    }
  }

  @override
  Future<UserModel> register({
    required String email,
    required String password,
    required String name,
    required String lastName,
  }) async {
    final response = await client.post(
      Uri.parse('$baseUrl/auth/register'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'email': email,
        'password': password,
        'name': name,
        'last_name': lastName,
      }),
    );

    if (response.statusCode == 201) {
      return UserModel.fromJson(
        json.decode(response.body) as Map<String, dynamic>,
      );
    } else {
      throw ServerException(
        message: 'Registration failed: ${response.statusCode}',
        statusCode: response.statusCode,
      );
    }
  }

  @override
  Future<void> logout() async {
    final response = await client.post(
      Uri.parse('$baseUrl/auth/logout'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode != 200) {
      throw ServerException(
        message: 'Logout failed: ${response.statusCode}',
        statusCode: response.statusCode,
      );
    }
  }
}
```

### 🧪 Paso 1: Crear Fake del HTTP Client

**`test/helpers/fake_http_client.dart`**
```dart
import 'package:http/http.dart' as http;

/// Fake HTTP Client para testing
class FakeHttpClient extends http.BaseClient {
  http.Response? responseToReturn;
  Exception? exceptionToThrow;
  
  Uri? lastUri;
  Map<String, String>? lastHeaders;
  String? lastBody;
  String? lastMethod;

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    throw UnimplementedError('Use get/post/put/delete methods');
  }

  @override
  Future<http.Response> get(Uri url, {Map<String, String>? headers}) async {
    lastUri = url;
    lastHeaders = headers;
    lastMethod = 'GET';
    
    if (exceptionToThrow != null) throw exceptionToThrow!;
    return responseToReturn!;
  }

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

### 🧪 Paso 2: Tests del Remote DataSource

**`test/features/auth/data/datasources/auth_remote_data_source_test.dart`**

```dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/error/exceptions.dart';
import 'package:sereni/clean/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:sereni/clean/features/auth/data/models/user_model.dart';

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
    final tUserModel = UserModel.fromJson(tUserJson);

    test('should return UserModel when response is 200', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        200,
        headers: {'content-type': 'application/json'},
      );

      // ACT
      final result = await dataSource.login(tEmail, tPassword);

      // ASSERT
      expect(result, equals(tUserModel));
    });

    test('should call correct endpoint with POST', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        200,
      );

      // ACT
      await dataSource.login(tEmail, tPassword);

      // ASSERT
      expect(fakeClient.lastMethod, 'POST');
      expect(
        fakeClient.lastUri,
        Uri.parse('$baseUrl/auth/login'),
      );
    });

    test('should send correct body', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        200,
      );

      // ACT
      await dataSource.login(tEmail, tPassword);

      // ASSERT
      final bodyJson = json.decode(fakeClient.lastBody!) as Map<String, dynamic>;
      expect(bodyJson['email'], tEmail);
      expect(bodyJson['password'], tPassword);
    });

    test('should send Content-Type header', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        200,
      );

      // ACT
      await dataSource.login(tEmail, tPassword);

      // ASSERT
      expect(
        fakeClient.lastHeaders?['Content-Type'],
        'application/json',
      );
    });

    test('should throw ServerException when response is 401', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        json.encode({'error': 'Unauthorized'}),
        401,
      );

      // ACT & ASSERT
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

    test('should throw ServerException when response is 500', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        'Internal Server Error',
        500,
      );

      // ACT & ASSERT
      expect(
        () => dataSource.login(tEmail, tPassword),
        throwsA(isA<ServerException>()),
      );
    });

    test('should throw Exception on network error', () async {
      // ARRANGE
      fakeClient.exceptionToThrow = Exception('No internet');

      // ACT & ASSERT
      expect(
        () => dataSource.login(tEmail, tPassword),
        throwsA(isA<Exception>()),
      );
    });
  });

  group('register', () {
    const tEmail = 'new@example.com';
    const tPassword = 'pass123';
    const tName = 'Jane';
    const tLastName = 'Doe';
    final tUserJson = fixtureAsMap('user');

    test('should return UserModel when response is 201', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        201,
      );

      // ACT
      final result = await dataSource.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      );

      // ASSERT
      expect(result, isA<UserModel>());
    });

    test('should send all required fields', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        json.encode(tUserJson),
        201,
      );

      // ACT
      await dataSource.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      );

      // ASSERT
      final bodyJson = json.decode(fakeClient.lastBody!) as Map<String, dynamic>;
      expect(bodyJson['email'], tEmail);
      expect(bodyJson['password'], tPassword);
      expect(bodyJson['name'], tName);
      expect(bodyJson['last_name'], tLastName);
    });

    test('should throw ServerException when email already exists (409)', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        json.encode({'error': 'Email already exists'}),
        409,
      );

      // ACT & ASSERT
      expect(
        () => dataSource.register(
          email: tEmail,
          password: tPassword,
          name: tName,
          lastName: tLastName,
        ),
        throwsA(isA<ServerException>()),
      );
    });
  });

  group('logout', () {
    test('should complete when response is 200', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response('', 200);

      // ACT & ASSERT
      expect(
        dataSource.logout(),
        completes,
      );
    });

    test('should throw ServerException when response is not 200', () async {
      // ARRANGE
      fakeClient.responseToReturn = http.Response(
        'Unauthorized',
        401,
      );

      // ACT & ASSERT
      expect(
        () => dataSource.logout(),
        throwsA(isA<ServerException>()),
      );
    });
  });
}
```

---

## Testing de Local DataSources

Los **Local DataSources** usan almacenamiento local (SharedPreferences, SQLite).

### 📁 Archivo fuente: `lib/clean/features/auth/data/datasources/auth_local_data_source.dart`

```dart
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sereni/clean/core/error/exceptions.dart';
import 'package:sereni/clean/features/auth/data/models/user_model.dart';

abstract class AuthLocalDataSource {
  Future<UserModel?> getUser();
  Future<void> cacheUser(UserModel user);
  Future<void> clearUser();
  Future<bool> hasUser();
}

class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  final SharedPreferences preferences;
  static const String _userKey = 'CACHED_USER';

  AuthLocalDataSourceImpl({required this.preferences});

  @override
  Future<UserModel?> getUser() async {
    final jsonString = preferences.getString(_userKey);
    if (jsonString == null) return null;
    
    try {
      return UserModel.fromJson(
        json.decode(jsonString) as Map<String, dynamic>,
      );
    } catch (e) {
      throw CacheException('Failed to parse cached user');
    }
  }

  @override
  Future<void> cacheUser(UserModel user) async {
    final success = await preferences.setString(
      _userKey,
      json.encode(user.toJson()),
    );
    
    if (!success) {
      throw CacheException('Failed to cache user');
    }
  }

  @override
  Future<void> clearUser() async {
    await preferences.remove(_userKey);
  }

  @override
  Future<bool> hasUser() async {
    return preferences.containsKey(_userKey);
  }
}
```

### 🧪 Paso 1: Crear Fake de SharedPreferences

**`test/helpers/fake_shared_preferences.dart`**
```dart
class FakeSharedPreferences {
  final Map<String, Object> _storage = {};
  bool shouldFail = false;

  String? getString(String key) {
    return _storage[key] as String?;
  }

  Future<bool> setString(String key, String value) async {
    if (shouldFail) return false;
    _storage[key] = value;
    return true;
  }

  Future<bool> remove(String key) async {
    _storage.remove(key);
    return true;
  }

  bool containsKey(String key) {
    return _storage.containsKey(key);
  }

  void clear() {
    _storage.clear();
    shouldFail = false;
  }
}
```

### 🧪 Paso 2: Tests del Local DataSource

**`test/features/auth/data/datasources/auth_local_data_source_test.dart`**

```dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/error/exceptions.dart';
import 'package:sereni/clean/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:sereni/clean/features/auth/data/models/user_model.dart';

import '../../../../helpers/fake_shared_preferences.dart';

void main() {
  late AuthLocalDataSourceImpl dataSource;
  late FakeSharedPreferences fakePreferences;

  setUp(() {
    fakePreferences = FakeSharedPreferences();
    dataSource = AuthLocalDataSourceImpl(
      preferences: fakePreferences as dynamic,  // Cast temporal
    );
  });

  tearDown(() {
    fakePreferences.clear();
  });

  const tUserModel = UserModel(
    id: '123',
    email: 'test@example.com',
    name: 'John',
    lastName: 'Doe',
  );

  group('cacheUser', () {
    test('should store user in SharedPreferences', () async {
      // ACT
      await dataSource.cacheUser(tUserModel);

      // ASSERT
      final jsonString = fakePreferences.getString('CACHED_USER');
      expect(jsonString, isNotNull);
      
      final jsonMap = json.decode(jsonString!) as Map<String, dynamic>;
      expect(jsonMap['id'], tUserModel.id);
      expect(jsonMap['email'], tUserModel.email);
    });

    test('should throw CacheException when storage fails', () async {
      // ARRANGE
      fakePreferences.shouldFail = true;

      // ACT & ASSERT
      expect(
        () => dataSource.cacheUser(tUserModel),
        throwsA(isA<CacheException>()),
      );
    });
  });

  group('getUser', () {
    test('should return UserModel when user is cached', () async {
      // ARRANGE
      await fakePreferences.setString(
        'CACHED_USER',
        json.encode(tUserModel.toJson()),
      );

      // ACT
      final result = await dataSource.getUser();

      // ASSERT
      expect(result, equals(tUserModel));
    });

    test('should return null when no user is cached', () async {
      // ACT
      final result = await dataSource.getUser();

      // ASSERT
      expect(result, isNull);
    });

    test('should throw CacheException when JSON is invalid', () async {
      // ARRANGE
      await fakePreferences.setString(
        'CACHED_USER',
        'invalid json',
      );

      // ACT & ASSERT
      expect(
        () => dataSource.getUser(),
        throwsA(isA<CacheException>()),
      );
    });
  });

  group('clearUser', () {
    test('should remove user from storage', () async {
      // ARRANGE
      await fakePreferences.setString(
        'CACHED_USER',
        json.encode(tUserModel.toJson()),
      );

      // ACT
      await dataSource.clearUser();

      // ASSERT
      expect(fakePreferences.containsKey('CACHED_USER'), isFalse);
    });
  });

  group('hasUser', () {
    test('should return true when user is cached', () async {
      // ARRANGE
      await fakePreferences.setString(
        'CACHED_USER',
        json.encode(tUserModel.toJson()),
      );

      // ACT
      final result = await dataSource.hasUser();

      // ASSERT
      expect(result, isTrue);
    });

    test('should return false when no user is cached', () async {
      // ACT
      final result = await dataSource.hasUser();

      // ASSERT
      expect(result, isFalse);
    });
  });
}
```

---

## Testing de Repository Implementation

El **Repository** es el cerebro de la capa Data. Decide entre local y remoto.

### 📁 Archivo fuente: `lib/clean/features/auth/data/repositories/auth_repository_impl.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:sereni/clean/core/error/exceptions.dart';
import 'package:sereni/clean/core/error/failures.dart';
import 'package:sereni/clean/core/network/network_info.dart';
import 'package:sereni/clean/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:sereni/clean/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';
import 'package:sereni/clean/features/auth/domain/repositories/auth_repository.dart';

class AuthRepositoryImpl implements IAuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    if (await networkInfo.isConnected) {
      try {
        final user = await remoteDataSource.login(email, password);
        await localDataSource.cacheUser(user);
        return Right(user);
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      return Left(NetworkFailure());
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      await remoteDataSource.logout();
      await localDataSource.clearUser();
      return const Right(null);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message));
    }
  }

  @override
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    required String name,
    required String lastName,
  }) async {
    if (await networkInfo.isConnected) {
      try {
        final user = await remoteDataSource.register(
          email: email,
          password: password,
          name: name,
          lastName: lastName,
        );
        await localDataSource.cacheUser(user);
        return Right(user);
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      return Left(NetworkFailure());
    }
  }

  @override
  Future<Either<Failure, User?>> checkAuthStatus() async {
    try {
      final user = await localDataSource.getUser();
      return Right(user);
    } on CacheException catch (e) {
      return Left(CacheFailure(e.message));
    }
  }
}
```

### 🧪 Paso 1: Crear Fakes de DataSources y NetworkInfo

**`test/helpers/fake_datasources.dart`**
```dart
import 'package:sereni/clean/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:sereni/clean/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:sereni/clean/features/auth/data/models/user_model.dart';

class FakeAuthRemoteDataSource implements AuthRemoteDataSource {
  bool shouldThrow = false;
  UserModel? userToReturn;
  Exception? exceptionToThrow;
  
  String? lastEmail;
  String? lastPassword;

  @override
  Future<UserModel> login(String email, String password) async {
    lastEmail = email;
    lastPassword = password;
    if (shouldThrow) throw exceptionToThrow ?? Exception('Login error');
    return userToReturn!;
  }

  @override
  Future<UserModel> register({
    required String email,
    required String password,
    required String name,
    required String lastName,
  }) async {
    if (shouldThrow) throw exceptionToThrow ?? Exception('Register error');
    return userToReturn!;
  }

  @override
  Future<void> logout() async {
    if (shouldThrow) throw exceptionToThrow ?? Exception('Logout error');
  }
}

class FakeAuthLocalDataSource implements AuthLocalDataSource {
  UserModel? cachedUser;
  bool shouldThrow = false;
  
  UserModel? lastCachedUser;

  @override
  Future<UserModel?> getUser() async {
    if (shouldThrow) throw Exception('Cache error');
    return cachedUser;
  }

  @override
  Future<void> cacheUser(UserModel user) async {
    if (shouldThrow) throw Exception('Cache error');
    lastCachedUser = user;
    cachedUser = user;
  }

  @override
  Future<void> clearUser() async {
    cachedUser = null;
  }

  @override
  Future<bool> hasUser() async {
    return cachedUser != null;
  }
}
```

**`test/helpers/fake_network_info.dart`**
```dart
import 'package:sereni/clean/core/network/network_info.dart';

class FakeNetworkInfo implements NetworkInfo {
  bool isOnline = true;

  @override
  Future<bool> get isConnected async => isOnline;
}
```

### 🧪 Paso 2: Tests del Repository

**`test/features/auth/data/repositories/auth_repository_impl_test.dart`**

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/error/exceptions.dart';
import 'package:sereni/clean/core/error/failures.dart';
import 'package:sereni/clean/features/auth/data/models/user_model.dart';
import 'package:sereni/clean/features/auth/data/repositories/auth_repository_impl.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';

import '../../../../helpers/fake_datasources.dart';
import '../../../../helpers/fake_network_info.dart';

void main() {
  late AuthRepositoryImpl repository;
  late FakeAuthRemoteDataSource fakeRemote;
  late FakeAuthLocalDataSource fakeLocal;
  late FakeNetworkInfo fakeNetwork;

  setUp(() {
    fakeRemote = FakeAuthRemoteDataSource();
    fakeLocal = FakeAuthLocalDataSource();
    fakeNetwork = FakeNetworkInfo();
    repository = AuthRepositoryImpl(
      remoteDataSource: fakeRemote,
      localDataSource: fakeLocal,
      networkInfo: fakeNetwork,
    );
  });

  const tEmail = 'test@example.com';
  const tPassword = 'password123';
  const tUserModel = UserModel(
    id: '123',
    email: tEmail,
    name: 'John',
    lastName: 'Doe',
  );
  const tUser = User(
    id: '123',
    email: tEmail,
    name: 'John',
    lastName: 'Doe',
  );

  group('login', () {
    test('should check network connectivity first', () async {
      // ARRANGE
      fakeNetwork.isOnline = true;
      fakeRemote.userToReturn = tUserModel;

      // ACT
      await repository.login(tEmail, tPassword);

      // ASSERT - NetworkInfo se usó
      expect(fakeNetwork.isOnline, isTrue);
    });

    group('device is online', () {
      setUp(() {
        fakeNetwork.isOnline = true;
      });

      test('should return user when remote call succeeds', () async {
        // ARRANGE
        fakeRemote.userToReturn = tUserModel;

        // ACT
        final result = await repository.login(tEmail, tPassword);

        // ASSERT
        expect(result, equals(const Right(tUser)));
      });

      test('should cache user locally when remote call succeeds', () async {
        // ARRANGE
        fakeRemote.userToReturn = tUserModel;

        // ACT
        await repository.login(tEmail, tPassword);

        // ASSERT
        expect(fakeLocal.lastCachedUser, equals(tUserModel));
      });

      test('should return ServerFailure when remote call fails', () async {
        // ARRANGE
        fakeRemote.shouldThrow = true;
        fakeRemote.exceptionToThrow = const ServerException(
          message: 'Login failed',
          statusCode: 401,
        );

        // ACT
        final result = await repository.login(tEmail, tPassword);

        // ASSERT
        expect(result, isA<Left<Failure, User>>());
        result.fold(
          (failure) => expect(failure, isA<ServerFailure>()),
          (_) => fail('Should return failure'),
        );
      });

      test('should not cache user when remote call fails', () async {
        // ARRANGE
        fakeRemote.shouldThrow = true;

        // ACT
        await repository.login(tEmail, tPassword);

        // ASSERT
        expect(fakeLocal.lastCachedUser, isNull);
      });
    });

    group('device is offline', () {
      setUp(() {
        fakeNetwork.isOnline = false;
      });

      test('should return NetworkFailure when offline', () async {
        // ACT
        final result = await repository.login(tEmail, tPassword);

        // ASSERT
        expect(result, isA<Left<Failure, User>>());
        result.fold(
          (failure) => expect(failure, isA<NetworkFailure>()),
          (_) => fail('Should return failure'),
        );
      });

      test('should not call remote when offline', () async {
        // ACT
        await repository.login(tEmail, tPassword);

        // ASSERT
        expect(fakeRemote.lastEmail, isNull);
      });
    });
  });

  group('register', () {
    const tName = 'Jane';
    const tLastName = 'Doe';

    test('should return user when online and registration succeeds', () async {
      // ARRANGE
      fakeNetwork.isOnline = true;
      fakeRemote.userToReturn = tUserModel;

      // ACT
      final result = await repository.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      );

      // ASSERT
      expect(result, equals(const Right(tUser)));
    });

    test('should cache user after successful registration', () async {
      // ARRANGE
      fakeNetwork.isOnline = true;
      fakeRemote.userToReturn = tUserModel;

      // ACT
      await repository.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      );

      // ASSERT
      expect(fakeLocal.lastCachedUser, equals(tUserModel));
    });

    test('should return NetworkFailure when offline', () async {
      // ARRANGE
      fakeNetwork.isOnline = false;

      // ACT
      final result = await repository.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      );

      // ASSERT
      expect(result, isA<Left<Failure, User>>());
    });
  });

  group('logout', () {
    test('should clear local cache on logout', () async {
      // ARRANGE
      fakeLocal.cachedUser = tUserModel;

      // ACT
      await repository.logout();

      // ASSERT
      expect(fakeLocal.cachedUser, isNull);
    });

    test('should call remote logout', () async {
      // ACT
      await repository.logout();

      // ASSERT - No debería lanzar excepción
      expect(true, isTrue);
    });

    test('should return failure when remote logout fails', () async {
      // ARRANGE
      fakeRemote.shouldThrow = true;
      fakeRemote.exceptionToThrow = const ServerException(
        message: 'Logout failed',
      );

      // ACT
      final result = await repository.logout();

      // ASSERT
      expect(result, isA<Left<Failure, void>>());
    });
  });

  group('checkAuthStatus', () {
    test('should return user from cache', () async {
      // ARRANGE
      fakeLocal.cachedUser = tUserModel;

      // ACT
      final result = await repository.checkAuthStatus();

      // ASSERT
      expect(result, equals(const Right(tUser)));
    });

    test('should return null when no user cached', () async {
      // ARRANGE
      fakeLocal.cachedUser = null;

      // ACT
      final result = await repository.checkAuthStatus();

      // ASSERT
      expect(result, equals(const Right<Failure, User?>(null)));
    });

    test('should return CacheFailure on error', () async {
      // ARRANGE
      fakeLocal.shouldThrow = true;

      // ACT
      final result = await repository.checkAuthStatus();

      // ASSERT
      expect(result, isA<Left<Failure, User?>>());
      result.fold(
        (failure) => expect(failure, isA<CacheFailure>()),
        (_) => fail('Should return failure'),
      );
    });
  });
}
```

---

## Ejercicios Prácticos

### Ejercicio 1: Completa los tests para checkAuthStatus

Añade tests para verificar:
1. Que se llama a localDataSource.getUser()
2. Que no se llama a remoteDataSource
3. Que maneja correctamente un UserModel null

### Ejercicio 2: Test de Error Handling

Crea un test que verifique que el Repository maneja correctamente cuando:
1. NetworkInfo lanza una excepción
2. LocalDataSource lanza CacheException en login (caso edge)

### Ejercicio 3: Extensión del Model

Añade un campo opcional `avatarUrl` al UserModel y escribe tests para:
1. fromJson con y sin avatarUrl
2. toJson con y sin avatarUrl
3. toEntity preserva avatarUrl

---

## ✅ Checklist de Data Testing

Antes de pasar a la siguiente parte, asegúrate de:

- [ ] Crear fixtures JSON reutilizables
- [ ] Testear Models (fromJson, toJson, toEntity)
- [ ] Testear Remote DataSources con HTTP mock
- [ ] Testear Local DataSources con SharedPreferences mock
- [ ] Testear Repository (online/offline/fallback)
- [ ] Verificar interacciones entre DataSources
- [ ] Manejar errores (ServerException, CacheException)
- [ ] Usar Fakes manuales correctamente

---

## 🚀 Siguiente Paso

➡️ **Parte 4: Testing Presentation (Cubits y Widgets)**

Aprenderás a:
- Testear Cubits con bloc_test
- Testear estados y transiciones
- Testear Widgets con interacciones
- Mock providers en widget tests

---

## 💡 Tips Adicionales

### 1. **Organización de Fakes**
Agrupa todos los Fakes en `test/helpers/`:

```dart
// test/helpers/all_fakes.dart
export 'fake_repositories.dart';
export 'fake_datasources.dart';
export 'fake_network_info.dart';
export 'fake_http_client.dart';
export 'fake_shared_preferences.dart';
```

### 2. **Datos de prueba consistentes**
Define datos de prueba globales:

```dart
// test/helpers/test_data.dart
const tUserModel = UserModel(...);
const tUser = User(...);
const tEmail = 'test@example.com';
const tPassword = 'password123';
```

### 3. **Comandos útiles**
```bash
# Tests de data completo
flutter test test/features/auth/data/

# Con coverage específico
flutter test --coverage test/features/auth/data/

# Solo un archivo
flutter test test/features/auth/data/models/user_model_test.dart
```

### 4. **Estructura recomendada de tests**
```
test/features/auth/data/
├── models/
│   └── user_model_test.dart
├── datasources/
│   ├── auth_remote_data_source_test.dart
│   └── auth_local_data_source_test.dart
└── repositories/
    └── auth_repository_impl_test.dart
```
