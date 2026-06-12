### 5.2 Data Layer (La Cocina)

#### Model (con Isar)

> **Isar** es una base de datos NoSQL de código abierto, extremadamente rápida y fácil de usar. A diferencia de Hive, Isar ofrece:
> - Queries reactivos con streams
> - Índices compuestos y multi-entrada
> - Búsqueda de texto completo
> - Completamente asíncrono con soporte multi-isolate
> 
> Es la opción recomendada para aplicaciones que necesitan alto rendimiento con datos locales complejos.

**Archivo**: `lib/features/user/data/models/user_model.dart`

```dart
import 'package:isar_community/isar_community.dart';
import 'package:my_app/features/user/domain/entities/user.dart';

part 'user_model.g.dart';

@collection
class UserModel {
  UserModel({
    this.id = Isar.autoIncrement,
    required this.name,
    required this.email,
    this.isActive = true,
    this.createdAt,
    this.avatarUrl,
  });

  Id id;

  @Index()
  String name;

  @Index(unique: true)
  String email;

  bool isActive;

  DateTime? createdAt;

  String? avatarUrl;

  User toEntity() {
    return User(
      id: id.toString(),
      name: name,
      email: email,
      isActive: isActive,
      createdAt: createdAt,
      avatarUrl: avatarUrl,
    );
  }

  factory UserModel.fromEntity(User entity) {
    return UserModel(
      id: entity.id.isNotEmpty ? int.tryParse(entity.id) ?? Isar.autoIncrement : Isar.autoIncrement,
      name: entity.name,
      email: entity.email,
      isActive: entity.isActive,
      createdAt: entity.createdAt,
      avatarUrl: entity.avatarUrl,
    );
  }
}
```

**Diferencias clave Hive vs Isar:**

| Aspecto | Hive | Isar 3.x |
|---------|------|----------|
| Anotaciones | `@HiveType(typeId: 5)` | `@collection` |
| Campo ID | `String id` | `Id id = Isar.autoIncrement` |
| Índices | No tiene | `@Index()`, `@Index(unique: true)` |
| Herencia | Extiende `HiveObject` | No extiende nada |
| Serialización | Genera adapter | Genera schema |

#### Model Nativo (API REST)

> Cuando usas comunicación con APIs REST (JSON), no necesitas Isar para el modelo remote. Solo necesitas serialización con `fromJson`/`toJson`.

**Archivo**: `lib/features/user/data/models/user_model.dart`

```dart
import 'package:my_app/features/user/domain/entities/user.dart';

class UserModel extends User {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
    super.isActive,
    super.createdAt,
    super.avatarUrl,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      email: json['email'] ?? '',
      isActive: json['is_active'] ?? true,
      createdAt: json['created_at'] != null
          ? DateTime.parse(json['created_at'])
          : null,
      avatarUrl: json['avatar_url'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'is_active': isActive,
      'created_at': createdAt?.toIso8601String(),
      'avatar_url': avatarUrl,
    };
  }

  factory UserModel.fromEntity(User entity) {
    return UserModel(
      id: entity.id,
      name: entity.name,
      email: entity.email,
      isActive: entity.isActive,
      createdAt: entity.createdAt,
      avatarUrl: entity.avatarUrl,
    );
  }

  User toEntity() {
    return User(
      id: id,
      name: name,
      email: email,
      isActive: isActive,
      createdAt: createdAt,
      avatarUrl: avatarUrl,
    );
  }
}
```

**Diferencias clave entre Isar y API REST:**

| Aspecto | Isar | API REST |
|---------|------|----------|
| Serialización | `@collection` + generación de schema | `fromJson()` / `toJson()` |
| Persistencia | Local en dispositivo | Remoto en servidor |
| Sincronización | No requiere red | Requiere conexión a internet |
| Offline | Soportado nativamente | Necesita caché local |
| Queries | Rich query language con índices | Limitado a endpoints del servidor |
| Reactivo | Streams para cambios | Polling o websockets |

#### Remote DataSource (API REST)

**Archivo**: `lib/features/user/data/datasources/user_remote_data_source.dart`

```dart
import 'package:dio/dio.dart';
import 'package:my_app/core/error/exceptions.dart';
import 'package:my_app/features/user/data/models/user_model.dart';

abstract class UserRemoteDataSource {
  Future<List<UserModel>> getUsers();
  Future<UserModel> getUser(String id);
  Future<UserModel> createUser(UserModel user);
  Future<void> deleteUser(String id);
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final Dio client;
  final String baseUrl;

  UserRemoteDataSourceImpl({
    required this.client,
    this.baseUrl = 'https://api.example.com',
  });

  @override
  Future<List<UserModel>> getUsers() async {
    try {
      final response = await client.get('$baseUrl/users');

      if (response.statusCode == 200) {
        final List<dynamic> jsonList = response.data;
        return jsonList.map((json) => UserModel.fromJson(json)).toList();
      } else {
        throw ServerException('Failed to load users: ${response.statusCode}');
      }
    } on DioException catch (e) {
      throw ServerException('Network error: ${e.message}');
    }
  }

  @override
  Future<UserModel> getUser(String id) async {
    try {
      final response = await client.get('$baseUrl/users/$id');

      if (response.statusCode == 200) {
        return UserModel.fromJson(response.data);
      } else {
        throw ServerException('User not found');
      }
    } on DioException catch (e) {
      throw ServerException('Network error: ${e.message}');
    }
  }

  @override
  Future<UserModel> createUser(UserModel user) async {
    try {
      final response = await client.post(
        '$baseUrl/users',
        data: user.toJson(),
      );

      if (response.statusCode == 201) {
        return UserModel.fromJson(response.data);
      } else {
        throw ServerException('Failed to create user');
      }
    } on DioException catch (e) {
      throw ServerException('Network error: ${e.message}');
    }
  }

  @override
  Future<void> deleteUser(String id) async {
    try {
      final response = await client.delete('$baseUrl/users/$id');

      if (response.statusCode != 200 && response.statusCode != 204) {
        throw ServerException('Failed to delete user');
      }
    } on DioException catch (e) {
      throw ServerException('Network error: ${e.message}');
    }
  }
}
```

#### NetworkInfo

> Para manejar la lógica online/offline, necesitas verificar si hay conexión a internet.

**Archivo**: `lib/core/network/network_info.dart`

```dart
import 'package:internet_connection_checker/internet_connection_checker.dart';

abstract class NetworkInfo {
  Future<bool> get isConnected;
}

class NetworkInfoImpl implements NetworkInfo {
  final InternetConnectionChecker connectionChecker;

  NetworkInfoImpl(this.connectionChecker);

  @override
  Future<bool> get isConnected async {
    return await connectionChecker.hasConnection;
  }
}
```

#### Exceptions

**Archivo**: `lib/core/error/exceptions.dart`

```dart
class ServerException implements Exception {
  final String message;
  ServerException(this.message);

  @override
  String toString() => message;
}

class CacheException implements Exception {
  final String message;
  CacheException(this.message);

  @override
  String toString() => message;
}
```

#### DataSource (con Isar)

**Archivo**: `lib/features/user/data/datasources/user_local_data_source.dart`

```dart
import 'package:isar_community/isar_community.dart';
import 'package:my_app/features/user/data/models/user_model.dart';

abstract class UserLocalDataSource {
  Future<List<UserModel>> getUsers();
  Future<UserModel?> getUser(int id);
  Future<int> saveUser(UserModel user);
  Future<void> deleteUser(int id);
}

class UserLocalDataSourceImpl implements UserLocalDataSource {
  final Isar _isar;
  
  UserLocalDataSourceImpl(this._isar);
  
  @override
  Future<List<UserModel>> getUsers() async {
    return _isar.userModels.where().findAll();
  }
  
  @override
  Future<UserModel?> getUser(int id) async {
    return _isar.userModels.get(id);
  }
  
  @override
  Future<int> saveUser(UserModel user) async {
    return _isar.writeTxn(() async {
      return _isar.userModels.put(user);
    });
  }
  
  @override
  Future<void> deleteUser(int id) async {
    await _isar.writeTxn(() async {
      await _isar.userModels.delete(id);
    });
  }
}
```

**Diferencias clave entre Hive Box e Isar:**

| Aspecto | Hive Box | Isar |
|---------|----------|------|
| Obtener todos | `_box.values.toList()` | `_isar.userModels.where().findAll()` |
| Obtener uno | `_box.get(id)` | `_isar.userModels.get(id)` |
| Guardar | `_box.put(key, value)` | `_isar.writeTxn(() => isar.collection.put(value))` |
| Eliminar | `_box.delete(key)` | `_isar.writeTxn(() => isar.collection.delete(id))` |
| Tipo ID | String | int (Id) |

#### Repository Implementation (con lógica Online/Offline)

> Este repository decide automáticamente si usar datos remotos (API) o locales (caché) según la conexión.

**Archivo**: `lib/features/user/data/repositories/user_repository_impl.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:my_app/core/error/exceptions.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/core/network/network_info.dart';
import 'package:my_app/features/user/data/datasources/user_local_data_source.dart';
import 'package:my_app/features/user/data/datasources/user_remote_data_source.dart';
import 'package:my_app/features/user/data/models/user_model.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

abstract class UserRepositoryImplBase implements UserRepository {
  Future<Either<Failure, List<User>>> getUsers() async {
    if (await networkInfo.isConnected) {
      try {
        final remoteUsers = await remoteDataSource.getUsers();
        await localDataSource.cacheUsers(remoteUsers);
        return Either.right(remoteUsers.map((m) => m.toEntity()).toList());
      } on ServerException {
        return Either.left(ServerFailure('Error loading from server'));
      }
    } else {
      try {
        final localUsers = await localDataSource.getUsers();
        return Either.right(localUsers.map((m) => m.toEntity()).toList());
      } catch (e) {
        return Either.left(CacheFailure('No cached data available'));
      }
    }
  }
}

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  UserRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    if (await networkInfo.isConnected) {
      try {
        final remoteUsers = await remoteDataSource.getUsers();
        await _cacheUsers(remoteUsers);
        return Either.right(remoteUsers.map((m) => m.toEntity()).toList());
      } on ServerException catch (e) {
        return Either.left(ServerFailure(e.message));
      }
    } else {
      return await _getUsersFromCache();
    }
  }

  Future<Either<Failure, List<User>>> _getUsersFromCache() async {
    try {
      final localUsers = await localDataSource.getUsers();
      return Either.right(localUsers.map((m) => m.toEntity()).toList());
    } catch (e) {
      return Either.left(CacheFailure('No cached data available'));
    }
  }

  Future<void> _cacheUsers(List<UserModel> users) async {
    for (final user in users) {
      await localDataSource.saveUser(user);
    }
  }

  @override
  Future<Either<Failure, User>> getUser(String id) async {
    if (await networkInfo.isConnected) {
      try {
        final remoteUser = await remoteDataSource.getUser(id);
        await localDataSource.saveUser(remoteUser);
        return Either.right(remoteUser);
      } on ServerException catch (e) {
        return Either.left(ServerFailure(e.message));
      }
    } else {
      try {
        final localUser = await localDataSource.getUser(id);
        if (localUser == null) {
          return Either.left(CacheFailure('User not found in cache'));
        }
        return Either.right(localUser);
      } catch (e) {
        return Either.left(CacheFailure(e.toString()));
      }
    }
  }

  @override
  Future<Either<Failure, void>> createUser(User user) async {
    if (await networkInfo.isConnected) {
      try {
        final userModel = UserModel.fromEntity(user);
        await remoteDataSource.createUser(userModel);
        await localDataSource.saveUser(userModel);
        return Either.right(null);
      } on ServerException catch (e) {
        return Either.left(ServerFailure(e.message));
      }
    } else {
      return Either.left(NetworkFailure('Cannot create user offline'));
    }
  }

  @override
  Future<Either<Failure, void>> updateUser(User user) async {
    if (await networkInfo.isConnected) {
      try {
        final userModel = UserModel.fromEntity(user);
        await remoteDataSource.createUser(userModel);
        await localDataSource.saveUser(userModel);
        return Either.right(null);
      } on ServerException catch (e) {
        return Either.left(ServerFailure(e.message));
      }
    } else {
      return Either.left(NetworkFailure('Cannot update user offline'));
    }
  }

  @override
  Future<Either<Failure, void>> deleteUser(String id) async {
    if (await networkInfo.isConnected) {
      try {
        await remoteDataSource.deleteUser(id);
        await localDataSource.deleteUser(id);
        return Either.right(null);
      } on ServerException catch (e) {
        return Either.left(ServerFailure(e.message));
      }
    } else {
      return Either.left(NetworkFailure('Cannot delete user offline'));
    }
  }
}
```

**Lógica de decisión del Repository:**

```
┌─────────────────────────────────────────────────────────────┐
│                    ¿Hay conexión?                            │
└─────────────────────────────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
           SÍ                          NO
            │                           │
            ▼                           ▼
┌───────────────────────┐   ┌───────────────────────────┐
│   USAR API REMOTA     │   │    USAR CACHÉ LOCAL      │
│                       │   │                           │
│ • Llama a RemoteData  │   │ • Llama a LocalData      │
│ • Guarda en caché     │   │ • Si falla → Failure     │
│ • Retorna Entity      │   │ • Retorna Entity         │
└───────────────────────┘   └───────────────────────────┘
            │                           │
            └─────────────┬─────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   Either<Failure, T>  │
              └───────────────────────┘
```

**Flujo completo de getUsers():**

```
getUsers()
    │
    ├─► ¿isConnected?
    │       │
    │      SÍ → remoteDataSource.getUsers()
    │       │       │
    │       │      ÉXITO → cacheUsers() → return Either.right(users)
    │       │       │
    │       │      ERROR → return Either.left(ServerFailure)
    │       │
    │      NO → localDataSource.getUsers()
    │       │       │
    │       │      ÉXITO → return Either.right(users)
    │       │       │
    │       │      ERROR → return Either.left(CacheFailure)
    │       │
    └──────┘
```

> **Nota**: Con Isar, puedes aprovechar sus streams reactivos para observadores en tiempo real de los datos locales, lo cual simplifica la sincronización con la UI.

---
