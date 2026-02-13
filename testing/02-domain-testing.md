# 🧪 Parte 2: Testing Domain (Entities y UseCases)

## 📋 Índice
1. [Introducción a la Capa Domain](#introducción-a-la-capa-domain)
2. [Testing de Entities](#testing-de-entities)
3. [Testing de UseCases](#testing-de-usecases)
4. [Creando Fakes Manuales](#creando-fakes-manuales)
5. [Testing de Failures](#testing-de-failures)
6. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Introducción a la Capa Domain

La capa **Domain** es el corazón de Clean Architecture. Contiene:

- **Entities**: Objetos de negocio puros (User, Task, etc.)
- **UseCases**: Acciones que el usuario puede realizar
- **Repository Interfaces**: Contratos que deben implementar otras capas
- **Failures**: Objetos que representan errores

### 🎯 Por qué es fácil de testear:

✅ **Sin dependencias externas** - No usa Flutter, HTTP, ni BD
✅ **Lógica pura** - Solo Dart puro
✅ **Tests rápidos** - Milisegundos por test
✅ **Sin mocks complejos** - Solo lógica de negocio

---

## Testing de Entities

### 📁 Archivo fuente: `lib/clean/features/auth/domain/entities/user.dart`

```dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String name;
  final String lastName;

  const User({
    required this.id,
    required this.email,
    required this.name,
    required this.lastName,
  });

  @override
  List<Object?> get props => [id, email, name, lastName];

  User copyWith({
    String? id,
    String? email,
    String? name,
    String? lastName,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      name: name ?? this.name,
      lastName: lastName ?? this.lastName,
    );
  }
}
```

### 🧪 Paso 1: Crear el archivo de test

```bash
touch test/features/auth/domain/entities/user_test.dart
```

### 🧪 Paso 2: Escribir tests completos

```dart
// test/features/auth/domain/entities/user_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';

void main() {
  group('User Entity', () {
    // Datos de prueba reutilizables
    const tUser = User(
      id: '123',
      email: 'test@example.com',
      name: 'John',
      lastName: 'Doe',
    );

    test('should create User with all required fields', () {
      // ARRANGE & ACT
      const user = User(
        id: '456',
        email: 'jane@example.com',
        name: 'Jane',
        lastName: 'Smith',
      );

      // ASSERT
      expect(user.id, '456');
      expect(user.email, 'jane@example.com');
      expect(user.name, 'Jane');
      expect(user.lastName, 'Smith');
    });

    group('Equatable', () {
      test('should be equal when properties are equal', () {
        // ARRANGE
        const user1 = User(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );
        const user2 = User(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );

        // ACT & ASSERT
        expect(user1, equals(user2));
      });

      test('should not be equal when properties differ', () {
        // ARRANGE
        const user1 = User(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );
        const user2 = User(
          id: '456',  // Diferente id
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );

        // ACT & ASSERT
        expect(user1, isNot(equals(user2)));
      });

      test('should not be equal when email differs', () {
        // ARRANGE
        const user1 = User(
          id: '123',
          email: 'test1@example.com',
          name: 'John',
          lastName: 'Doe',
        );
        const user2 = User(
          id: '123',
          email: 'test2@example.com',  // Diferente email
          name: 'John',
          lastName: 'Doe',
        );

        // ACT & ASSERT
        expect(user1, isNot(equals(user2)));
      });

      test('props should contain all fields', () {
        // ARRANGE
        const user = User(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );

        // ACT
        final props = user.props;

        // ASSERT
        expect(props, [
          '123',
          'test@example.com',
          'John',
          'Doe',
        ]);
      });
    });

    group('copyWith', () {
      test('should update only specified field (name)', () {
        // ARRANGE
        const original = User(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          lastName: 'Doe',
        );

        // ACT
        final updated = original.copyWith(name: 'Jane');

        // ASSERT
        expect(updated.id, original.id);        // Igual
        expect(updated.email, original.email);  // Igual
        expect(updated.name, 'Jane');           // Cambió
        expect(updated.lastName, original.lastName);  // Igual
      });

      test('should update only specified field (email)', () {
        // ARRANGE
        const original = tUser;

        // ACT
        final updated = original.copyWith(email: 'new@example.com');

        // ASSERT
        expect(updated.id, original.id);
        expect(updated.email, 'new@example.com');
        expect(updated.name, original.name);
        expect(updated.lastName, original.lastName);
      });

      test('should return same instance when no parameters provided', () {
        // ARRANGE
        const original = tUser;

        // ACT
        final updated = original.copyWith();

        // ASSERT
        expect(updated, equals(original));
      });

      test('should update multiple fields at once', () {
        // ARRANGE
        const original = tUser;

        // ACT
        final updated = original.copyWith(
          name: 'Jane',
          lastName: 'Smith',
        );

        // ASSERT
        expect(updated.name, 'Jane');
        expect(updated.lastName, 'Smith');
        expect(updated.id, original.id);
        expect(updated.email, original.email);
      });
    });

    test('should maintain immutability', () {
      // ARRANGE
      const user = tUser;

      // ACT - Intentar modificar (esto no compilaría si no fuera inmutable)
      final updated = user.copyWith(name: 'Jane');

      // ASSERT - Original no cambió
      expect(user.name, 'John');
      expect(updated.name, 'Jane');
    });
  });
}
```

### ✅ Conceptos clave en tests de Entities:

1. **Equatable**: Verifica que `==` funciona correctamente
2. **copyWith**: Asegura que solo cambia lo que pedimos
3. **Inmutabilidad**: Confirma que los objetos originales no se modifican
4. **Props**: Verifica que todos los campos son considerados en la igualdad

---

## Creando Fakes Manuales

Antes de testear UseCases, necesitamos crear **Fakes** de los Repositories. Un Fake es una implementación de prueba de una interfaz.

### 📁 Archivo: `test/helpers/fake_repositories.dart`

```dart
// test/helpers/fake_repositories.dart
import 'package:dartz/dartz.dart';
import 'package:sereni/clean/core/error/failures.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';
import 'package:sereni/clean/features/auth/domain/repositories/auth_repository.dart';

/// Fake implementation of IAuthRepository for testing
/// 
/// Allows controlling behavior to test success and failure scenarios
class FakeAuthRepository implements IAuthRepository {
  // Control flags
  bool shouldFail = false;
  bool shouldThrowException = false;
  
  // Data to return
  User? userToReturn;
  List<User> usersListToReturn = [];
  
  // Failures to return
  Failure? failureToReturn;
  
  // Track method calls
  int loginCallCount = 0;
  int logoutCallCount = 0;
  int registerCallCount = 0;
  int checkAuthStatusCallCount = 0;
  
  // Store last parameters
  String? lastEmail;
  String? lastPassword;
  String? lastName;
  String? lastLastName;

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    loginCallCount++;
    lastEmail = email;
    lastPassword = password;
    
    if (shouldThrowException) {
      throw Exception('Network error');
    }
    
    if (shouldFail) {
      return Left(failureToReturn ?? const ServerFailure('Login failed'));
    }
    
    return Right(userToReturn!);
  }

  @override
  Future<Either<Failure, void>> logout() async {
    logoutCallCount++;
    
    if (shouldFail) {
      return Left(failureToReturn ?? const ServerFailure('Logout failed'));
    }
    
    return const Right(null);
  }

  @override
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    required String name,
    required String lastName,
  }) async {
    registerCallCount++;
    lastEmail = email;
    lastPassword = password;
    lastName = name;
    lastLastName = lastName;
    
    if (shouldFail) {
      return Left(failureToReturn ?? const ServerFailure('Registration failed'));
    }
    
    return Right(userToReturn!);
  }

  @override
  Future<Either<Failure, User?>> checkAuthStatus() async {
    checkAuthStatusCallCount++;
    
    if (shouldFail) {
      return Left(failureToReturn ?? const ServerFailure('Auth check failed'));
    }
    
    return Right(userToReturn);
  }
  
  /// Reset all state for fresh test
  void reset() {
    shouldFail = false;
    shouldThrowException = false;
    userToReturn = null;
    failureToReturn = null;
    loginCallCount = 0;
    logoutCallCount = 0;
    registerCallCount = 0;
    checkAuthStatusCallCount = 0;
    lastEmail = null;
    lastPassword = null;
    lastName = null;
    lastLastName = null;
  }
}
```

### 🎓 Características de un buen Fake:

1. **Implementa la interfaz real**: `implements IAuthRepository`
2. **Flags de control**: `shouldFail`, `shouldThrowException`
3. **Datos configurables**: `userToReturn`, `failureToReturn`
4. **Tracking de llamadas**: Contadores para verificar interacciones
5. **Reset method**: Limpia estado entre tests

---

## Testing de UseCases

### 📁 Archivo fuente: `lib/clean/features/auth/domain/usecases/login_usecase.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import 'package:sereni/clean/core/error/failures.dart';
import 'package:sereni/clean/core/usecases/usecase.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';
import 'package:sereni/clean/features/auth/domain/repositories/auth_repository.dart';

class LoginUseCase implements UseCase<User, LoginParams> {
  final IAuthRepository repository;

  LoginUseCase({required this.repository});

  @override
  Future<Either<Failure, User>> call(LoginParams params) async {
    return await repository.login(params.email, params.password);
  }
}

class LoginParams extends Equatable {
  final String email;
  final String password;

  const LoginParams({required this.email, required this.password});

  @override
  List<Object?> get props => [email, password];
}
```

### 🧪 Paso 1: Crear archivo de test

```bash
touch test/features/auth/domain/usecases/login_usecase_test.dart
```

### 🧪 Paso 2: Tests completos del UseCase

```dart
// test/features/auth/domain/usecases/login_usecase_test.dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/error/failures.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';
import 'package:sereni/clean/features/auth/domain/usecases/login_usecase.dart';

import '../../../../helpers/fake_repositories.dart';

void main() {
  late LoginUseCase useCase;
  late FakeAuthRepository fakeRepository;

  setUp(() {
    fakeRepository = FakeAuthRepository();
    useCase = LoginUseCase(repository: fakeRepository);
  });

  tearDown(() {
    fakeRepository.reset();
  });

  group('LoginUseCase', () {
    const tEmail = 'test@example.com';
    const tPassword = 'password123';
    const tUser = User(
      id: '123',
      email: tEmail,
      name: 'John',
      lastName: 'Doe',
    );

    test('should return User when login is successful', () async {
      // ARRANGE
      fakeRepository.userToReturn = tUser;

      // ACT
      final result = await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ASSERT
      expect(result, equals(const Right(tUser)));
      expect(fakeRepository.loginCallCount, 1);
      expect(fakeRepository.lastEmail, tEmail);
      expect(fakeRepository.lastPassword, tPassword);
    });

    test('should return ServerFailure when login fails', () async {
      // ARRANGE
      fakeRepository.shouldFail = true;
      fakeRepository.failureToReturn = const ServerFailure('Invalid credentials');

      // ACT
      final result = await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ASSERT
      expect(result, equals(const Left(ServerFailure('Invalid credentials'))));
      expect(fakeRepository.loginCallCount, 1);
    });

    test('should pass correct parameters to repository', () async {
      // ARRANGE
      fakeRepository.userToReturn = tUser;
      const customEmail = 'custom@example.com';
      const customPassword = 'customPass';

      // ACT
      await useCase(const LoginParams(
        email: customEmail,
        password: customPassword,
      ));

      // ASSERT
      expect(fakeRepository.lastEmail, customEmail);
      expect(fakeRepository.lastPassword, customPassword);
    });

    test('should call repository only once', () async {
      // ARRANGE
      fakeRepository.userToReturn = tUser;

      // ACT
      await useCase(const LoginParams(email: tEmail, password: tPassword));

      // ASSERT
      expect(fakeRepository.loginCallCount, 1);
    });
  });

  group('LoginParams', () {
    test('should create LoginParams with correct values', () {
      // ARRANGE & ACT
      const params = LoginParams(
        email: 'test@example.com',
        password: 'pass123',
      );

      // ASSERT
      expect(params.email, 'test@example.com');
      expect(params.password, 'pass123');
    });

    test('should be equal when properties are equal', () {
      // ARRANGE
      const params1 = LoginParams(email: 'test@test.com', password: 'pass');
      const params2 = LoginParams(email: 'test@test.com', password: 'pass');

      // ACT & ASSERT
      expect(params1, equals(params2));
    });

    test('should not be equal when email differs', () {
      // ARRANGE
      const params1 = LoginParams(email: 'test1@test.com', password: 'pass');
      const params2 = LoginParams(email: 'test2@test.com', password: 'pass');

      // ACT & ASSERT
      expect(params1, isNot(equals(params2)));
    });

    test('props should contain email and password', () {
      // ARRANGE
      const params = LoginParams(email: 'test@test.com', password: 'pass');

      // ACT
      final props = params.props;

      // ASSERT
      expect(props, ['test@test.com', 'pass']);
    });
  });
}
```

### 🎓 Conceptos clave en tests de UseCases:

1. **Crear Fake en setUp**: Cada test tiene un repository fresco
2. **Configurar comportamiento**: Setear `userToReturn` o `shouldFail`
3. **Verificar resultado**: `expect(result, equals(Right/Left(...)))`
4. **Verificar interacciones**: Contadores de llamadas
5. **Probar parámetros**: Asegurar que se pasan correctamente

---

## Testing de Failures

### 📁 Archivo fuente: `lib/clean/core/error/failures.dart`

```dart
import 'package:equatable/equatable.dart';

abstract class Failure extends Equatable {
  final String message;
  
  const Failure(this.message);
  
  @override
  List<Object?> get props => [message];
}

class ServerFailure extends Failure {
  const ServerFailure([String message = 'Server error']) : super(message);
}

class NetworkFailure extends Failure {
  const NetworkFailure([String message = 'No internet connection']) : super(message);
}

class CacheFailure extends Failure {
  const CacheFailure([String message = 'Cache error']) : super(message);
}

class AuthFailure extends Failure {
  const AuthFailure([String message = 'Authentication failed']) : super(message);
}
```

### 🧪 Tests de Failures

```dart
// test/core/error/failures_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/error/failures.dart';

void main() {
  group('Failures', () {
    group('ServerFailure', () {
      test('should create with default message', () {
        const failure = ServerFailure();
        expect(failure.message, 'Server error');
      });

      test('should create with custom message', () {
        const failure = ServerFailure('Custom server error');
        expect(failure.message, 'Custom server error');
      });

      test('should be equal when message is equal', () {
        const failure1 = ServerFailure('Error');
        const failure2 = ServerFailure('Error');
        expect(failure1, equals(failure2));
      });
    });

    group('NetworkFailure', () {
      test('should create with default message', () {
        const failure = NetworkFailure();
        expect(failure.message, 'No internet connection');
      });

      test('should not be equal to ServerFailure', () {
        const networkFailure = NetworkFailure('Error');
        const serverFailure = ServerFailure('Error');
        expect(networkFailure, isNot(equals(serverFailure)));
      });
    });

    test('different failure types should not be equal even with same message', () {
      const serverFailure = ServerFailure('Error');
      const cacheFailure = CacheFailure('Error');
      const authFailure = AuthFailure('Error');

      expect(serverFailure, isNot(equals(cacheFailure)));
      expect(serverFailure, isNot(equals(authFailure)));
      expect(cacheFailure, isNot(equals(authFailure)));
    });
  });
}
```

---

## Ejercicios Prácticos

### Ejercicio 1: Test RegisterUseCase

Crea tests para `RegisterUseCase` que recibe email, password, name y lastName.

**Archivo fuente:** `lib/clean/features/auth/domain/usecases/register_usecase.dart`

<details>
<summary>Ver estructura del UseCase</summary>

```dart
class RegisterUseCase implements UseCase<User, RegisterParams> {
  final IAuthRepository repository;

  RegisterUseCase({required this.repository});

  @override
  Future<Either<Failure, User>> call(RegisterParams params) async {
    return await repository.register(
      email: params.email,
      password: params.password,
      name: params.name,
      lastName: params.lastName,
    );
  }
}

class RegisterParams extends Equatable {
  final String email;
  final String password;
  final String name;
  final String lastName;

  const RegisterParams({
    required this.email,
    required this.password,
    required this.name,
    required this.lastName,
  });

  @override
  List<Object?> get props => [email, password, name, lastName];
}
```
</details>

**Tests a escribir:**
1. Success: should return User when registration succeeds
2. Failure: should return ServerFailure when registration fails
3. Params: should pass all parameters to repository
4. Params equality test

<details>
<summary>Ver solución completa</summary>

```dart
// test/features/auth/domain/usecases/register_usecase_test.dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/error/failures.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';
import 'package:sereni/clean/features/auth/domain/usecases/register_usecase.dart';

import '../../../../helpers/fake_repositories.dart';

void main() {
  late RegisterUseCase useCase;
  late FakeAuthRepository fakeRepository;

  setUp(() {
    fakeRepository = FakeAuthRepository();
    useCase = RegisterUseCase(repository: fakeRepository);
  });

  tearDown(() {
    fakeRepository.reset();
  });

  group('RegisterUseCase', () {
    const tEmail = 'new@example.com';
    const tPassword = 'pass123';
    const tName = 'Jane';
    const tLastName = 'Doe';
    const tUser = User(
      id: '456',
      email: tEmail,
      name: tName,
      lastName: tLastName,
    );

    test('should return User when registration is successful', () async {
      // ARRANGE
      fakeRepository.userToReturn = tUser;

      // ACT
      final result = await useCase(const RegisterParams(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      ));

      // ASSERT
      expect(result, equals(const Right(tUser)));
    });

    test('should return ServerFailure when registration fails', () async {
      // ARRANGE
      fakeRepository.shouldFail = true;

      // ACT
      final result = await useCase(const RegisterParams(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      ));

      // ASSERT
      expect(result, isA<Left<Failure, User>>());
    });

    test('should pass all parameters to repository', () async {
      // ARRANGE
      fakeRepository.userToReturn = tUser;

      // ACT
      await useCase(const RegisterParams(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      ));

      // ASSERT
      expect(fakeRepository.lastEmail, tEmail);
      expect(fakeRepository.lastPassword, tPassword);
      expect(fakeRepository.lastName, tName);
      expect(fakeRepository.lastLastName, tLastName);
    });

    test('should call register on repository', () async {
      // ARRANGE
      fakeRepository.userToReturn = tUser;

      // ACT
      await useCase(const RegisterParams(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      ));

      // ASSERT
      expect(fakeRepository.registerCallCount, 1);
    });
  });

  group('RegisterParams', () {
    test('should create with all required fields', () {
      const params = RegisterParams(
        email: 'test@test.com',
        password: 'pass',
        name: 'John',
        lastName: 'Doe',
      );

      expect(params.email, 'test@test.com');
      expect(params.password, 'pass');
      expect(params.name, 'John');
      expect(params.lastName, 'Doe');
    });

    test('should be equal when all properties equal', () {
      const params1 = RegisterParams(
        email: 'test@test.com',
        password: 'pass',
        name: 'John',
        lastName: 'Doe',
      );
      const params2 = RegisterParams(
        email: 'test@test.com',
        password: 'pass',
        name: 'John',
        lastName: 'Doe',
      );

      expect(params1, equals(params2));
    });
  });
}
```
</details>

---

## ✅ Checklist de Domain Testing

Antes de pasar a la siguiente parte, asegúrate de:

- [ ] Entender qué es un Entity y por qué usar Equatable
- [ ] Saber testear `copyWith` e igualdad de objetos
- [ ] Crear Fakes manuales implementando interfaces
- [ ] Configurar comportamiento de Fakes (shouldFail, userToReturn)
- [ ] Testear UseCases con éxito y fallo
- [ ] Verificar parámetros pasados a repositorios
- [ ] Entender Either<Failure, Success>
- [ ] Testear diferentes tipos de Failure

---

## 🚀 Siguiente Paso

➡️ **Parte 3: Testing Data (Models, Repositories, DataSources)**

Aprenderás a:
- Testear Models con fromJson/toJson
- Testear Repository Implementation (lógica online/offline)
- Testear Remote DataSources con HTTP
- Testear Local DataSources con SharedPreferences
- Crear Fixtures JSON

---

## 💡 Tips Adicionales

### 1. **Organización de Fakes**
Mantén todos tus Fakes en `test/helpers/` para reutilización:

```dart
// test/helpers/fakes.dart
export 'fake_repositories.dart';
// export 'fake_datasources.dart';  // Cuando los tengas
// export 'fake_services.dart';     // Cuando los tengas
```

### 2. **Datos de prueba consistentes**
Define constantes para datos de prueba reutilizables:

```dart
// test/helpers/test_constants.dart
const tEmail = 'test@example.com';
const tPassword = 'password123';
const tUser = User(id: '123', email: tEmail, name: 'John', lastName: 'Doe');
```

### 3. **Comandos útiles**
```bash
# Ejecutar todos los tests de domain
flutter test test/features/auth/domain/

# Ejecutar con coverage
flutter test --coverage test/features/auth/domain/

# Ver reporte de coverage
genhtml coverage/lcov.info -o coverage/html
```
