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

#### Remote DataSource — Dos opciones

> El RemoteDataSource se implementa según el backend. Usa **Dio** para APIs REST externas, **SupabaseClient** cuando el backend es Supabase. El patrón es el mismo: el repositorio recibe un `remoteDataSource` y no sabe ni le importa cuál usa.

##### Opción 1: Dio (APIs REST externas)

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
      await client.delete('$baseUrl/users/$id');
    } on DioException catch (e) {
      throw ServerException('Network error: ${e.message}');
    }
  }
}
```

##### Opción 2: SupabaseClient (backend Supabase)

**Archivo**: `lib/features/user/data/datasources/user_remote_data_source.dart`

```dart
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:my_app/core/error/exceptions.dart';
import 'package:my_app/features/user/data/models/user_model.dart';

abstract class UserRemoteDataSource {
  Future<List<UserModel>> getUsers();
  Future<UserModel> getUser(String id);
  Future<UserModel> createUser(UserModel user);
  Future<void> deleteUser(String id);
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final SupabaseClient supabase;

  UserRemoteDataSourceImpl({required this.supabase});

  @override
  Future<List<UserModel>> getUsers() async {
    try {
      final response = await supabase
          .from('users')
          .select()
          .order('created_at', ascending: false);
      return (response as List)
          .map((json) => UserModel.fromJson(json))
          .toList();
    } on PostgrestException catch (e) {
      throw ServerException(e.message);
    }
  }

  @override
  Future<UserModel> getUser(String id) async {
    try {
      final response = await supabase
          .from('users')
          .select()
          .eq('id', id)
          .maybeSingle();
      if (response == null) throw ServerException('User not found');
      return UserModel.fromJson(response);
    } on PostgrestException catch (e) {
      throw ServerException(e.message);
    }
  }

  @override
  Future<UserModel> createUser(UserModel user) async {
    try {
      final response = await supabase
          .from('users')
          .insert(user.toJson())
          .select()
          .single();
      return UserModel.fromJson(response);
    } on PostgrestException catch (e) {
      throw ServerException(e.message);
    }
  }

  @override
  Future<void> deleteUser(String id) async {
    try {
      await supabase.from('users').delete().eq('id', id);
    } on PostgrestException catch (e) {
      throw ServerException(e.message);
    }
  }
}
```

**¿Cuál usar?**

| Criterio | Dio | SupabaseClient |
|----------|-----|----------------|
| Backend propio (REST API) | ✅ | ❌ |
| Backend Supabase | ❌ | ✅ |
| Microservicios externos | ✅ | ❌ |
| Auth + DB + Storage + Realtime | ❌ | ✅ |
| Control fino de headers/cache | ✅ | ⚠️ Limitado |
| Testeo con mocks | Dio Mock | supabase mocks |

#### NetworkInfo

> Para manejar la lógica online/offline, necesitas verificar si hay conexión a internet.

**Archivo**: `lib/core/network/network_info.dart`

```dart
import 'package:internet_connection_checker_plus/internet_connection_checker_plus.dart';

abstract class NetworkInfo {
  Future<bool> get isConnected;
}

class NetworkInfoImpl implements NetworkInfo {
  final InternetConnection connectionChecker;

  NetworkInfoImpl(this.connectionChecker);

  @override
  Future<bool> get isConnected => connectionChecker.hasInternetAccess;

  @override
  Stream<bool> get onConnectivityChanged =>
      connectionChecker.onStatusChange.map(
        (status) => status == InternetStatus.connected,
      );
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

class AuthException implements Exception {
  final String message;
  final int? statusCode;

  AuthException({required this.message, this.statusCode});

  @override
  String toString() => 'AuthException: $message (status: $statusCode)';
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

> Este repository decide automáticamente si usar datos remotos (API) o locales (caché) según la conexión. Recibe **4 dependencias estándar**: `remoteDataSource`, `localDataSource`, `networkInfo` y `userSession`.

**Archivo**: `lib/features/user/data/repositories/user_repository_impl.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:my_app/core/error/exceptions.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/core/network/network_info.dart';
import 'package:my_app/core/session/user_session.dart';
import 'package:my_app/features/user/data/datasources/user_local_data_source.dart';
import 'package:my_app/features/user/data/datasources/user_remote_data_source.dart';
import 'package:my_app/features/user/data/models/user_model.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  final NetworkInfo networkInfo;
  final UserSession userSession;

  UserRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
    required this.userSession,
  });

  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    if (await networkInfo.isConnected) {
      try {
        final remoteUsers = await remoteDataSource.getUsers();
        await _cacheUsers(remoteUsers);
        return Right(remoteUsers.map((m) => m.toEntity()).toList());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      return _getUsersFromCache();
    }
  }

  Future<Either<Failure, List<User>>> _getUsersFromCache() async {
    try {
      final localUsers = await localDataSource.getUsers();
      return Right(localUsers.map((m) => m.toEntity()).toList());
    } catch (e) {
      return Left(CacheFailure('No cached data available'));
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
        return Right(remoteUser);
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      try {
        final localUser = await localDataSource.getUser(id);
        if (localUser == null) {
          return Left(CacheFailure('User not found in cache'));
        }
        return Right(localUser);
      } catch (e) {
        return Left(CacheFailure(e.toString()));
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
        return Right(null);
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      return Left(NetworkFailure('Cannot create user offline'));
    }
  }

  @override
  Future<Either<Failure, void>> deleteUser(String id) async {
    if (await networkInfo.isConnected) {
      try {
        await remoteDataSource.deleteUser(id);
        await localDataSource.deleteUser(id);
        return Right(null);
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      return Left(NetworkFailure('Cannot delete user offline'));
    }
  }
}
```

> **Uso de `userSession`**: El `userId` se usa para filtrar datos del usuario autenticado. Ejemplo: `final userId = userSession.userId;` (síncrono).

##### Variante: Repositorio con múltiples Remote DataSources

> A veces un repositorio necesita combinar **dos o más** fuentes remotas. Por ejemplo, un repositorio de sorteos que necesita datos de `RaffleRemoteDataSource` y `TicketRemoteDataSource`:

```dart
class RaffleRepositoryImpl implements RaffleRepository {
  final RaffleRemoteDataSource remoteDataSource;
  final TicketRemoteDataSource ticketRemoteDataSource;
  final NetworkInfo networkInfo;
  final UserSession userSession;

  RaffleRepositoryImpl({
    required this.remoteDataSource,
    required this.ticketRemoteDataSource,
    required this.networkInfo,
    required this.userSession,
  });

  @override
  Future<Either<Failure, Raffle>> createRaffle(Raffle raffle) async {
    final userId = userSession.userId;
    if (userId == null) return Left(AuthFailure());

    if (await networkInfo.isConnected) {
      try {
        final model = await remoteDataSource.createRaffle(
          RaffleModel.fromEntity(raffle),
        );
        return Right(model.toEntity());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      return Left(NetworkFailure('Cannot create raffle offline'));
    }
  }

  @override
  Future<Either<Failure, List<Ticket>>> getTickets(String raffleId) async {
    if (await networkInfo.isConnected) {
      try {
        final tickets = await ticketRemoteDataSource.getTickets(raffleId);
        return Right(tickets.map((m) => m.toEntity()).toList());
      } on ServerException catch (e) {
        return Left(ServerFailure(e.message));
      }
    } else {
      return Left(NetworkFailure('Cannot load tickets offline'));
    }
  }
}
```

##### ¿Cuándo incluir `UserSession`?

| Repositorio | ¿Necesita UserSession? | Motivo |
|-------------|----------------------|--------|
| User/Profile | ✅ Sí | Filtra datos por `userId` |
| PaymentMethod | ✅ Sí | Asocia métodos de pago al usuario |
| Raffle (sorteo) | ✅ Sí | Crea recursos pertenecientes al usuario |
| Ticket | ✅ Sí | Reserva/compra asociada al usuario |
| Auth | ❌ No | Usa `localDataSource.hasCachedUser` directamente |
| Winner (público) | ❌ No | Consulta pública sin dueño |

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
