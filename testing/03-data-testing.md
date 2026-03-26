# 🧪 Parte 3: Testing Data (Models, Repositories, DataSources)

> **¿De qué trata esta parte?** De testear la capa **Data** que maneja la comunicación con el exterior: APIs, bases de datos locales, y la lógica de decidir cuándo usar datos remotos vs locales.

---

## 📋 Índice

1. [Introducción a la Capa Data](#introducción-a-la-capa-data)
2. [Fixtures JSON - Datos de Prueba](#fixtures-json---datos-de-prueba)
3. [Testing de Models](#testing-de-models)
4. [Testing de Remote DataSources](#testing-de-remote-datasources)
5. [Testing de Local DataSources](#testing-de-local-datasources)
6. [Testing de Repository Implementation](#testing-de-repository-implementation)
7. [ Checklist](#-checklist)

---

## 1. Introducción a la Capa Data

### 🤔 ¿Qué es la Capa Data?

La capa **Data** es responsable de:
- **Models**: Transformar datos JSON a objetos Dart
- **DataSources**: Comunicarse con APIs y almacenamiento local
- **Repository Implementation**: Decidir cuándo usar datos remotos vs locales (lógica de cache)

### 📊 Arquitectura de la Capa Data

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────┐    ┌─────────────┐    ┌───────────────────┐      │
│   │ MODELS  │ ←→ │  DATASOURCES │ ←→ │ REPOSITORY IMPL  │      │
│   └─────────┘    └─────────────┘    └───────────────────┘      │
│       ↑                ↑                      ↑                 │
│       │                │                      │                 │
│   JSON ↔ Dart     HTTP / Cache           Coordina todo          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 ¿Por qué es Más Compleja de Testear?

| Aspecto | Domain | Data |
|---------|--------|------|
| **Dependencias externas** | ❌ Ninguna | ✅ HTTP, SharedPreferences |
| **Manejo de errores** | Simple | ✅ Timeouts, parsing, red |
| **Async/await** | Básico | ✅ Complejo |
| **Estados de red** | ❌ No aplica | ✅ Online vs Offline |

---

## 2. Fixtures JSON - Datos de Prueba

### 🤔 ¿Qué son los Fixtures?

Los **fixtures** son archivos JSON que contienen datos de prueba reutilizables. Son como "actores secundarios" en nuestros tests.

### 📁 Estructura de Carpetas

```
test/
├── fixtures/                    ← Archivos JSON de prueba
│   ├── user.json               ← Un usuario
│   ├── users_list.json         ← Lista de usuarios
│   └── auth_response.json      ← Respuesta de login
└── helpers/
    └── fixture_reader.dart     ← Helper para leer fixtures
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

### 📝 Paso 2: Crear el helper de fixtures

```dart
// test/helpers/fixture_reader.dart
import 'dart:convert';
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

## 3. Testing de Models

### 🤔 ¿Qué es un Model?

Un **Model** es la versión "data" de un Entity. Mientras el Entity solo tiene datos de negocio, el Model sabe cómo convertirlos a/from JSON.

### 📁 Archivo Fuente: UserModel

```dart
// lib/features/features/auth/data/models/user_model.dart
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';

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

  /// Deserializa desde JSON → Dart
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String,
      lastName: json['last_name'] as String,  // nota: snake_case en JSON
    );
  }

  /// Serializa a JSON → String
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'last_name': lastName,  // nota: snake_case en JSON
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

### 🎓 Patrones Comunes en Models

```
JSON (snake_case)  ↔  Dart (camelCase)

last_name (JSON)   →  lastName (Dart)
created_at (JSON)  →  createdAt (Dart)
```

### 🧪 Tests de Model: Paso a Paso

#### Test 1: fromJson - básico

```dart
group('fromJson', () {
  test('should return valid model from JSON', () {
    // Arrange - leer fixture
    final Map<String, dynamic> jsonMap = 
        json.decode(fixture('user')) as Map<String, dynamic>;

    // Act
    final result = UserModel.fromJson(jsonMap);

    // Assert
    expect(result.id, '123');
    expect(result.email, 'test@example.com');
    expect(result.name, 'John');
    expect(result.lastName, 'Doe');
  });
});
```

#### Test 2: fromJson - campos faltantes

```dart
  test('should throw when required field is missing', () {
    // Arrange
    final jsonMap = {
      'id': '123',
      'email': 'test@example.com',
      // Falta 'name' y 'last_name'
    };

    // Act & Assert
    expect(
      () => UserModel.fromJson(jsonMap),
      throwsA(isA<TypeError>()),
    );
  });
```

#### Test 3: fromJson - campos extra

```dart
  test('should handle extra fields gracefully', () {
    // Arrange
    final jsonMap = {
      'id': '123',
      'email': 'test@example.com',
      'name': 'John',
      'last_name': 'Doe',
      'extra_field': 'ignored',  // Campo extra
    };

    // Act
    final result = UserModel.fromJson(jsonMap);

    // Assert
    expect(result.id, '123');
    // Los campos extra se ignoran silenciosamente
  });
```

#### Test 4: toJson

```dart
group('toJson', () {
  test('should return a valid JSON map', () {
    // Arrange
    const model = UserModel(
      id: '123',
      email: 'test@example.com',
      name: 'John',
      lastName: 'Doe',
    );

    // Act
    final result = model.toJson();

    // Assert
    expect(result['id'], '123');
    expect(result['email'], 'test@example.com');
    expect(result['name'], 'John');
    expect(result['last_name'], 'Doe');  // snake_case
  });
});
```

#### Test 5: toJson + fromJson = roundtrip

```dart
  test('toJson and fromJson should be inverse operations', () {
    // Arrange
    const original = UserModel(
      id: '123',
      email: 'test@example.com',
      name: 'John',
      lastName: 'Doe',
    );

    // Act
    final json = original.toJson();
    final recreated = UserModel.fromJson(json);

    // Assert
    expect(recreated.id, original.id);
    expect(recreated.email, original.email);
    expect(recreated.name, original.name);
    expect(recreated.lastName, original.lastName);
  });
```

#### Test 6: toEntity / fromEntity

```dart
group('toEntity', () {
  test('should return User entity with correct data', () {
    // Arrange
    const model = UserModel(
      id: '123',
      email: 'test@example.com',
      name: 'John',
      lastName: 'Doe',
    );

    // Act
    final result = model.toEntity();

    // Assert
    expect(result, isA<User>());  // Es un User
    expect(result.id, '123');
  });
});
```

---

## 4. Testing de Remote DataSources

### 🤔 ¿Qué es un Remote DataSource?

Un **Remote DataSource** se comunica con APIs externas (HTTP/Supabase/Firebase). Es como un "traductor" entre tu app y el servidor.

### 📁 Archivo Fuente: AuthRemoteDataSource

```dart
// lib/features/features/auth/data/datasources/auth_remote_data_source.dart
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:mi_proyecto_flutter/clean/core/error/exceptions.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';

abstract class AuthRemoteDataSource {
  Future<UserModel> login(String email, String password);
  Future<UserModel> register({...});
  Future<void> logout();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final http.Client client;
  final String baseUrl;

  AuthRemoteDataSourceImpl({required this.client, required this.baseUrl});

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
  // ... más métodos
}
```

### 🧪 Fake del HTTP Client

Para testear el DataSource, necesitamos un Fake del HTTP Client:

```dart
// test/helpers/fake_http_client.dart
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

### 🧪 Tests del Remote DataSource

```dart
group('login', () {
  const tEmail = 'test@example.com';
  const tPassword = 'password123';
  final tUserJson = fixtureAsMap('user');

  test('should return UserModel when response is 200', () async {
    // Arrange
    fakeClient.responseToReturn = http.Response(
      json.encode(tUserJson),
      200,
      headers: {'content-type': 'application/json'},
    );

    // Act
    final result = await dataSource.login(tEmail, tPassword);

    // Assert
    expect(result.id, '123');
    expect(result.email, 'test@example.com');
  });

  test('should call correct endpoint with POST', () async {
    // Arrange
    fakeClient.responseToReturn = http.Response(json.encode(tUserJson), 200);

    // Act
    await dataSource.login(tEmail, tPassword);

    // Assert
    expect(fakeClient.lastMethod, 'POST');
    expect(fakeClient.lastUri, Uri.parse('$baseUrl/auth/login'));
  });

  test('should throw ServerException when response is 401', () async {
    // Arrange
    fakeClient.responseToReturn = http.Response('Unauthorized', 401);

    // Act & Assert
    expect(
      () => dataSource.login(tEmail, tPassword),
      throwsA(isA<ServerException>()),
    );
  });
});
```

---

## 5. Testing de Local DataSources

### 🤔 ¿Qué es un Local DataSource?

Un **Local DataSource** usa almacenamiento local (SharedPreferences, SQLite). Es la "memoria" de tu app.

### 📁 Archivo Fuente: AuthLocalDataSource

```dart
// lib/features/features/auth/data/datasources/auth_local_data_source.dart
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mi_proyecto_flutter/clean/core/error/exceptions.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';

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

### 🧪 Fake de SharedPreferences

```dart
// test/helpers/fake_shared_preferences.dart
class FakeSharedPreferences {
  final Map<String, Object> _storage = {};
  bool shouldFail = false;

  String? getString(String key) => _storage[key] as String?;

  Future<bool> setString(String key, String value) async {
    if (shouldFail) return false;
    _storage[key] = value;
    return true;
  }

  Future<bool> remove(String key) async {
    _storage.remove(key);
    return true;
  }

  bool containsKey(String key) => _storage.containsKey(key);

  void clear() {
    _storage.clear();
    shouldFail = false;
  }
}
```

---

## 6. Testing de Repository Implementation

### 🤔 ¿Qué es el Repository Implementation?

El **Repository Implementation** es el "cerebro" de la capa Data. Decide:
- ¿Tenemos internet? → Usar datos remotos
- ¿No tenemos internet? → Usar datos locales (cache)
- ¿El servidor falló? → Retornar error

### 📁 Archivo Fuente: AuthRepositoryImpl

```dart
// lib/features/features/auth/data/repositories/auth_repository_impl.dart
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
    // 1. ¿Tenemos internet?
    if (await networkInfo.isConnected) {
      try {
        // 2. Llamar al servidor
        final user = await remoteDataSource.login(email, password);
        // 3. Guardar en cache
        await localDataSource.cacheUser(user);
        return Either.right(user);
      } on ServerException catch (e) {
        return Either.left(ServerFailure(e.message));
      }
    } else {
      // Sin internet
      return Either.left(NetworkFailure());
    }
  }
}
```

### 🧪 Fakes Necesarios

Para testear el Repository, necesitamos:
1. **FakeAuthRemoteDataSource** - Simula el servidor
2. **FakeAuthLocalDataSource** - Simula el cache local
3. **FakeNetworkInfo** - Simula el estado de red

### 🧪 Tests del Repository

```dart
group('login', () {
  group('device is online', () {
    setUp(() {
      fakeNetwork.isOnline = true;
    });

    test('should return user when remote call succeeds', () async {
      // Arrange
      fakeRemote.userToReturn = tUserModel;

      // Act
      final result = await repository.login(tEmail, tPassword);

      // Assert
      expect(result.isRight(), true);
    });

    test('should cache user locally when remote call succeeds', () async {
      // Arrange
      fakeRemote.userToReturn = tUserModel;

      // Act
      await repository.login(tEmail, tPassword);

      // Assert
      expect(fakeLocal.lastCachedUser, isNotNull);
    });

    test('should return ServerFailure when remote call fails', () async {
      // Arrange
      fakeRemote.shouldThrow = true;
      fakeRemote.exceptionToThrow = const ServerException(message: 'Login failed');

      // Act
      final result = await repository.login(tEmail, tPassword);

      // Assert
      expect(result.isLeft(), true);
    });
  });

  group('device is offline', () {
    setUp(() {
      fakeNetwork.isOnline = false;
    });

    test('should return NetworkFailure when offline', () async {
      // Act
      final result = await repository.login(tEmail, tPassword);

      // Assert
      expect(result.isLeft(), true);
    });

    test('should not call remote when offline', () async {
      // Act
      await repository.login(tEmail, tPassword);

      // Assert
      expect(fakeRemote.lastEmail, isNull);  // No se llamó
    });
  });
});
```

---

## ✅ Checklist

Antes de pasar a la siguiente parte, asegúrate de:

- [ ] Entender la estructura de la capa Data (Models, DataSources, Repositories)
- [ ] Crear fixtures JSON reutilizables
- [ ] Entender el helper fixture_reader
- [ ] Testear Models (fromJson, toJson, toEntity)
- [ ] Testear Remote DataSources con HTTP mock
- [ ] Testear Local DataSources con SharedPreferences mock
- [ ] Testear Repository (online/offline/fallback)
- [ ] Verificar interacciones entre DataSources
- [ ] Manejar errores (ServerException, CacheException)

---

## 🚀 Siguiente Paso

**Práctica:**
- [03a-practica-fixtures-models.md](./03a-practica-fixtures-models.md) ← Fixtures y Models
- [03b-practica-datasources.md](./03b-practica-datasources.md) ← DataSources
- [03c-practica-repositories.md](./03c-practica-repositories.md) ← Repositories

---

## 💡 Tips Adicionales

### Organización
```dart
// test/helpers/all_fakes.dart
export 'fake_repositories.dart';
export 'fake_datasources.dart';
export 'fake_network_info.dart';
export 'fake_http_client.dart';
export 'fake_shared_preferences.dart';
```

### Comandos útiles
```bash
# Tests de data completo
flutter test test/features/auth/data/

# Con coverage
flutter test --coverage test/features/auth/data/
```
