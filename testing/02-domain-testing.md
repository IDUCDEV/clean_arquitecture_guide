# 🧪 Parte 2: Testing Domain (Entities y UseCases)

> **¿De qué trata esta parte?** De testear la capa más importante de Clean Architecture: **Domain**. Esta capa contiene la lógica de negocio pura, sin dependencias externas.

---

## 📋 Índice

1. [Introducción a la Capa Domain](#introducción-a-la-capa-domain)
2. [Testing de Entities](#testing-de-entities)
3. [Creando Fakes Manuales (Explicación Paso a Paso)](#creando-fakes-manuales-explicación-paso-a-paso)
4. [Testing de UseCases](#testing-de-usecases)
5. [Testing de Failures](#testing-de-failures)
6. [ Checklist](#-checklist)

---

## 1. Introducción a la Capa Domain

### 🤔 ¿Qué es la Capa Domain?

La capa **Domain** es el corazón de Clean Architecture. Contiene:

```
┌─────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  Entities        → Objetos de negocio puros               │
│  UseCases        → Acciones que el usuario puede realizar │
│  Repositories    → Contratos (interfaces) que otras       │
│                   capas deben implementar                 │
│  Failures        → Objetos que representan errores        │
└─────────────────────────────────────────────────────────────┘
```

### 📊 Ejemplo: Feature de Auth

```dart
// Entity: representa el objeto de negocio
class User { ... }

// UseCase: una acción que el usuario puede hacer
class LoginUseCase { ... }

// Repository Interface: el contrato
abstract class IAuthRepository { ... }

// Failure: un error possível
class ServerFailure { ... }
```

### 🎯 ¿Por qué es Fácil de Testear?

```
✅ SIN DEPENDENCIAS EXTERNAS   → No usa Flutter, HTTP, ni Base de Datos
✅ LÓGICA PURA                → Solo Dart estándar
✅ TESTS RÁPIDOS              → Milisegundos por test
✅ SIN MOCKS COMPLEJOS        → Solo lógica de negocio
```

> **Comparación:** Un test de Domain puede ejecutarse en **menos de 1ms**, mientras que un test de UI puede tomar **100-500ms**.

---

## 2. Testing de Entities

### 🤔 ¿Qué es un Entity?

Un **Entity** es un objeto de negocio que representa algo en tu dominio. Ejemplos:
- `User` - Un usuario del sistema
- `Task` - Una tarea
- `Product` - Un producto en una tienda

### 📁 Archivo Fuente: Entity User

```dart
// lib/clean/features/auth/domain/entities/user.dart
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

### 🎓 ¿Por qué usamos Equatable?

`Equatable` nos permite comparar objetos fácilmente:

```dart
// Sin Equatable - compara referencias (¿son el mismo objeto en memoria?)
user1 == user2  // false (aunque tengan los mismos datos)

// Con Equatable - compara valores (¿tienen los mismos datos?)
user1 == user2  // true (si tienen los mismos valores)
```

### 🧪 Tests de Entity: Paso a Paso

#### Test 1: Creación básica del Entity

```dart
// test/features/auth/domain/entities/user_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';

void main() {
  group('User Entity', () {
    
    test('should create User with all required fields', () {
      // ARRANGE - Preparar los datos
      const id = '456';
      const email = 'jane@example.com';
      const name = 'Jane';
      const lastName = 'Smith';

      // ACT - Crear el usuario
      const user = User(
        id: id,
        email: email,
        name: name,
        lastName: lastName,
      );

      // ASSERT - Verificar
      expect(user.id, '456');
      expect(user.email, 'jane@example.com');
      expect(user.name, 'Jane');
      expect(user.lastName, 'Smith');
    });

  });
}
```

#### Test 2: Verificar igualdad (Equatable)

```dart
group('Equatable', () {
  test('should be equal when properties are equal', () {
    // Arrange - Dos usuarios con los mismos datos
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

    // Act & Assert
    expect(user1, equals(user2));  // ✅ Son iguales con Equatable
  });

  test('should not be equal when properties differ', () {
    // Arrange
    const user1 = User(id: '123', email: 'test@example.com', name: 'John', lastName: 'Doe');
    const user2 = User(id: '456', email: 'test@example.com', name: 'John', lastName: 'Doe');

    // Act & Assert
    expect(user1, isNot(equals(user2)));
  });
});
```

#### Test 3: Verificar copyWith

```dart
group('copyWith', () {
  test('should update only specified field (name)', () {
    // Arrange
    const original = User(
      id: '123',
      email: 'test@example.com',
      name: 'John',
      lastName: 'Doe',
    );

    // Act
    final updated = original.copyWith(name: 'Jane');

    // Assert
    expect(updated.name, 'Jane');           // ✅ Cambió
    expect(updated.id, original.id);       // ✅ Sin cambios
    expect(updated.email, original.email);  // ✅ Sin cambios
    expect(updated.lastName, original.lastName);  // ✅ Sin cambios
  });

  test('should return same instance when no parameters provided', () {
    // Arrange
    const original = User(
      id: '123',
      email: 'test@example.com',
      name: 'John',
      lastName: 'Doe',
    );

    // Act
    final updated = original.copyWith();

    // Assert
    expect(updated, equals(original));  // ✅ Son iguales
  });
});
```

---

## 3. Creando Fakes Manuales (Explicación Paso a Paso)

### 🤔 ¿Por qué necesitamos Fakes?

Imagina que quieres testear un `LoginUseCase`:

```dart
class LoginUseCase {
  final IAuthRepository repository;
  
  LoginUseCase({required this.repository});
  
  Future<Either<Failure, User>> call(LoginParams params) async {
    return await repository.login(params.email, params.password);
  }
}
```

**Problema:** `LoginUseCase` depende de `IAuthRepository`. No podemos llamarlo directamente porque necesitamos una implementación.

**Solución:** Creamos un **Fake** - una implementación falsa de la interfaz que controla el comportamiento.

### 🎬 La Analogía del Actor

Un Fake es como un **actor** que sigue un guión:

| Concepto | Analogía del Actor |
|----------|---------------------|
| `shouldFail` | "Actor, hoy haz de fallar" |
| `userToReturn` | "Actor, cuando te pregunten, entrega este usuario" |
| `loginCallCount` | "Actor, cuenta cuántas veces te preguntan" |

### 📁 Estructura de un Fake Paso a Paso

#### Paso 1: Copia la Interfaz

Primero, mira tu interfaz original:

```dart
// lib/clean/features/auth/domain/repositories/auth_repository.dart
abstract class IAuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
  Future<Either<Failure, void>> logout();
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    required String name,
    required String lastName,
  });
  Future<Either<Failure, User?>> checkAuthStatus();
}
```

#### Paso 2: Crea la Clase Fake

```dart
// test/helpers/fake_repositories.dart
import 'package:dartz/dartz.dart';
import 'package:sereni/clean/core/error/failures.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';
import 'package:sereni/clean/features/auth/domain/repositories/auth_repository.dart';

/// Fake implementation of IAuthRepository for testing
/// 
/// This is like an actor following a script - you control what it returns
class FakeAuthRepository implements IAuthRepository {
  // ═══════════════════════════════════════════════════════════════
  // CONTROL FLAGS - Like telling the actor what to do
  // ═══════════════════════════════════════════════════════════════
  
  /// When true, all methods will return a failure
  bool shouldFail = false;
  
  /// When true, methods will throw an exception
  bool shouldThrowException = false;
  
  // ═══════════════════════════════════════════════════════════════
  // DATA TO RETURN - What the actor should give back
  // ═══════════════════════════════════════════════════════════════
  
  /// User to return on successful login/register
  User? userToReturn;
  
  /// Failure to return when shouldFail is true
  Failure? failureToReturn;
  
  // ═══════════════════════════════════════════════════════════════
  // TRACKING - Counting how many times the actor is called
  // ═══════════════════════════════════════════════════════════════
  
  int loginCallCount = 0;
  int logoutCallCount = 0;
  int registerCallCount = 0;
  int checkAuthStatusCallCount = 0;
  
  // ═══════════════════════════════════════════════════════════════
  // TRACKING PARAMETERS - What was passed to the actor
  // ═══════════════════════════════════════════════════════════════
  
  String? lastEmail;
  String? lastPassword;
  String? lastName;
  String? lastLastName;

  // ═══════════════════════════════════════════════════════════════
  // IMPLEMENTATION - The actual "acting"
  // ═══════════════════════════════════════════════════════════════

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    // Track the call
    loginCallCount++;
    lastEmail = email;
    lastPassword = password;
    
    // Check if we should throw exception
    if (shouldThrowException) {
      throw Exception('Network error');
    }
    
    // Check if we should fail
    if (shouldFail) {
      return Left(failureToReturn ?? const ServerFailure('Login failed'));
    }
    
    // Success case
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
  /// Like resetting the actor for the next scene
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

### 🎓 ¿Por qué cada parte del Fake?

| Sección | Propósito | ¿Cuándo usarla? |
|---------|-----------|-----------------|
| `shouldFail` | Controlar si retorna error | Test de casos de error |
| `shouldThrowException` | Simular excepciones | Test de manejo de errores |
| `userToReturn` | Qué retornar en éxito | Test de casos exitosos |
| `failureToReturn` | Qué error retornar | Test de tipos específicos de error |
| `*CallCount` | Verificar que se llamó | Test de interacciones |
| `last*` | Verificar parámetros | Test de que se pasaron datos correctos |
| `reset()` | Limpiar estado | En `tearDown()` |

---

## 4. Testing de UseCases

### 🤔 ¿Qué es un UseCase?

Un **UseCase** representa una acción que el usuario puede realizar. Ejemplos:
- `LoginUseCase` - Iniciar sesión
- `RegisterUseCase` - Registrarse
- `GetTasksUseCase` - Obtener tareas

### 📁 Archivo Fuente: LoginUseCase

```dart
// lib/clean/features/auth/domain/usecases/login_usecase.dart
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

### 🧪 Tests del UseCase: Paso a Paso

#### Estructura Base

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
    // Create fresh instances for each test
    fakeRepository = FakeAuthRepository();
    useCase = LoginUseCase(repository: fakeRepository);
  });

  tearDown(() {
    // Reset state after each test
    fakeRepository.reset();
  });

  // Tests go here...
}
```

#### Test 1: Caso de Éxito

```dart
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
    // ARRANGE - Configurar el Fake para éxito
    fakeRepository.userToReturn = tUser;

    // ACT - Ejecutar el UseCase
    final result = await useCase(const LoginParams(
      email: tEmail,
      password: tPassword,
    ));

    // ASSERT - Verificar resultado
    expect(result, equals(const Right(tUser)));
    
    // ASSERT - Verificar que se llamó al repositorio
    expect(fakeRepository.loginCallCount, 1);
    
    // ASSERT - Verificar parámetros
    expect(fakeRepository.lastEmail, tEmail);
    expect(fakeRepository.lastPassword, tPassword);
  });
});
```

#### Test 2: Caso de Error

```dart
  test('should return ServerFailure when login fails', () async {
    // ARRANGE - Configurar el Fake para fallar
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
```

#### Test 3: Verificar que solo se llama una vez

```dart
  test('should call repository only once', () async {
    // ARRANGE
    fakeRepository.userToReturn = tUser;

    // ACT - Llamar múltiples veces
    await useCase(const LoginParams(email: tEmail, password: tPassword));

    // ASSERT
    expect(fakeRepository.loginCallCount, 1);
  });
```

---

## 5. Testing de Failures

### 🤔 ¿Qué es un Failure?

Un **Failure** representa un error en la aplicación. Ejemplos:
- `ServerFailure` - Error del servidor
- `NetworkFailure` - Sin conexión a internet
- `CacheFailure` - Error de caché
- `AuthFailure` - Error de autenticación

### 📁 Archivo Fuente: Failures

```dart
// lib/clean/core/error/failures.dart
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

## ✅ Checklist

Antes de pasar a la siguiente parte, asegúrate de:

- [ ] Entender qué es un Entity y por qué usar Equatable
- [ ] Saber testear `copyWith` e igualdad de objetos
- [ ] Comprender qué es un Fake y por qué lo necesitamos
- [ ] Crear Fakes manuales implementando interfaces
- [ ] Configurar comportamiento de Fakes (shouldFail, userToReturn)
- [ ] Testear UseCases con éxito y fallo
- [ ] Verificar parámetros pasados a repositorios
- [ ] Entender Either<Failure, Success>
- [ ] Testear diferentes tipos de Failure

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 3: Testing Data](./03-data-testing.md)

**Práctica:** [02a-practica-fakes-manuales.md](./02a-practica-fakes-manuales.md) ← ¡Practica creando Fakes!

---

## 💡 Tips Adicionales

### Organización de Fakes
Mantén todos tus Fakes en `test/helpers/`:

```dart
// test/helpers/fakes.dart
export 'fake_repositories.dart';
// export 'fake_datasources.dart';  // Cuando los tengas
// export 'fake_services.dart';     // Cuando los tengas
```

### Datos de prueba consistentes
Define constantes para datos de prueba reutilizables:

```dart
// test/helpers/test_constants.dart
const tEmail = 'test@example.com';
const tPassword = 'password123';
const tUser = User(id: '123', email: tEmail, name: 'John', lastName: 'Doe');
```

### Comandos útiles
```bash
# Ejecutar todos los tests de domain
flutter test test/features/auth/domain/

# Ejecutar con coverage
flutter test --coverage test/features/auth/domain/

# Ver reporte de coverage
genhtml coverage/lcov.info -o coverage/html
```
