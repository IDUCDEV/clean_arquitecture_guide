### 5.1 Domain Layer (La Receta)

#### Entity

**Archivo**: `lib/features/user/domain/entities/user.dart`

```dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  const User({
    required this.id,
    required this.name,
    required this.email,
    this.isActive = true,
    this.createdAt,
    this.avatarUrl,
  });

  final String id;
  final String name;
  final String email;
  final bool isActive;
  final DateTime? createdAt;
  final String? avatarUrl;

  bool get hasAvatar => avatarUrl != null && avatarUrl!.isNotEmpty;

  bool get isNew {
    if (createdAt == null) return false;
    final daysSinceCreated = DateTime.now().difference(createdAt!).inDays;
    return daysSinceCreated < 7;
  }

  User copyWith({
    String? id,
    String? name,
    String? email,
    bool? isActive,
    DateTime? createdAt,
    String? avatarUrl,
  }) {
    return User(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      avatarUrl: avatarUrl ?? this.avatarUrl,
    );
  }

  @override
  List<Object?> get props => [id, name, email, isActive, createdAt, avatarUrl];

  @override
  String toString() => 'User(id: $id, name: $name)';
}
```

#### Repository Interface

**Archivo**: `lib/features/user/domain/repositories/user_repository.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/entities/user.dart';

abstract class UserRepository {
  Future<Either<Failure, List<User>>> getUsers();
  Future<Either<Failure, User>> getUser(String id);
  Future<Either<Failure, void>> createUser(User user);
  Future<Either<Failure, void>> updateUser(User user);
  Future<Either<Failure, void>> deleteUser(String id);
}
```

#### UseCases

**Archivo**: `lib/features/user/domain/usecases/get_users.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

class GetUsers extends UseCase<List<User>, NoParams> {
  final UserRepository repository;
  
  GetUsers(this.repository);
  
  @override
  Future<Either<Failure, List<User>>> call(NoParams params) async {
    return await repository.getUsers();
  }
}
```

**Archivo**: `lib/features/user/domain/usecases/get_user.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

class GetUser extends UseCase<User, GetUserParams> {
  final UserRepository repository;
  
  GetUser(this.repository);
  
  @override
  Future<Either<Failure, User>> call(GetUserParams params) async {
    return await repository.getUser(params.id);
  }
}

class GetUserParams extends Equatable {
  final String id;
  
  const GetUserParams(this.id);
  
  @override
  List<Object?> get props => [id];
}
```

**Archivo**: `lib/features/user/domain/usecases/create_user.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

class CreateUser extends UseCase<void, CreateUserParams> {
  final UserRepository repository;
  
  CreateUser(this.repository);
  
  @override
  Future<Either<Failure, void>> call(CreateUserParams params) async {
    final user = User(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: params.name,
      email: params.email,
      createdAt: DateTime.now(),
    );
    
    return await repository.createUser(user);
  }
}

class CreateUserParams extends Equatable {
  final String name;
  final String email;
  
  const CreateUserParams({required this.name, required this.email});
  
  @override
  List<Object?> get props => [name, email];
}
```

**Archivo**: `lib/features/user/domain/usecases/delete_user.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

class DeleteUser extends UseCase<void, DeleteUserParams> {
  final UserRepository repository;
  
  DeleteUser(this.repository);
  
  @override
  Future<Either<Failure, void>> call(DeleteUserParams params) async {
    return await repository.deleteUser(params.id);
  }
}

class DeleteUserParams extends Equatable {
  final String id;
  
  const DeleteUserParams(this.id);
  
  @override
  List<Object?> get props => [id];
}
```

### 5.1.1 Comparación: Future<Either> vs TaskEither

> `fpdart` ofrece dos formas de manejar operaciones asíncronas con errores. Aquí te mostramos ambas para que elijas la que prefieras.

#### Opción A: `Future<Either>` (Más Familiar)

Esta es la forma tradicional, similar a lo que ya conoces. Funciona exactamente igual con `fpdart`.

```dart
import 'package:fpdart/fpdart.dart';

class GetUsers extends UseCase<List<User>, NoParams> {
  final UserRepository repository;
  
  GetUsers(this.repository);
  
  @override
  Future<Either<Failure, List<User>>> call(NoParams params) async {
    return await repository.getUsers();
  }
}
```

**Uso en el Cubit:**
```dart
final result = await _getUsers(NoParams());
result.match(
  (failure) => emit(UserError(failure.toString())),
  (users) => emit(UsersLoaded(users)),
);
```

**Pros:**
- ✅ Más familiar para quienes vienen de `dartz`
- ✅ Fácil de entender
- ✅ Similar al manejo tradicional de Futures

**Contras:**
- ❌ Menos composable
- ❌ Difícil de encadenar múltiples operaciones asíncronas

---

#### Opción B: `TaskEither` (Más Funcional)

`TaskEither` es un tipo que representa una operación asíncrona que puede fallar. Es más poderoso y composable.

```dart
import 'package:fpdart/fpdart.dart';

class GetUsers extends UseCase<List<User>, NoParams> {
  final UserRepository repository;
  
  GetUsers(this.repository);
  
  @override
  TaskEither<Failure, List<User>> call(NoParams params) {
    return TaskEither(() => repository.getUsers());
  }
}
```

**Uso en el Cubit:**
```dart
final result = await _getUsers(NoParams()).run();
result.match(
  (failure) => emit(UserError(failure.toString())),
  (users) => emit(UsersLoaded(users)),
);
```

**Pros:**
- ✅ Más composable
- ✅ Fácil de encadenar con `.andThen()`
- ✅ Mejor para operaciones complejas
- ✅ Más idiomático en programación funcional

**Contras:**
- ❌ Curva de aprendizaje más alta
- ❌ Puede ser overkill para casos simples

---

#### Ejemplo de Encadenamiento con TaskEither

```dart
// Encadenar múltiples operaciones
final program = _validateUser(id)
    .andThen((user) => _checkPermissions(user))
    .andThen((user) => _fetchUserDetails(user));

final result = await program.run();
```

#### Recomendación

| Situación | Recomendación |
|-----------|---------------|
| Proyecto simple o aprendizaje | `Future<Either>` |
| Proyecto complejo con múltiples operaciones asíncronas | `TaskEither` |
| Equipo con experiencia en FP | `TaskEither` |
| Necesitas compatibilidad con código existente | `Future<Either>` |

**En esta guía usamos `Future<Either>`** por ser más accesible, pero puedes migrar a `TaskEither` cuando te sientas cómodo.

---
