# 🧪 Parte 2: Testing Domain (Entities y UseCases)

> **¿De qué trata esta parte?** De testear la capa más importante de Clean Architecture: **Domain**. Esta capa contiene la lógica de negocio pura, sin dependencias externas.

---

## 📋 Índice

1. [Introducción a la Capa Domain](#introducción-a-la-capa-domain)
2. [Testing de Entities](#testing-de-entities)
3. [Creando Mocks con Mocktail](#creando-mocks-con-mocktail)
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
// lib/features/features/auth/domain/entities/user.dart
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
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';

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

## 3. Creando Mocks con Mocktail

### 🤔 ¿Por qué necesitamos Mocks?

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

**Solución:** Usar **Mocktail** para crear mocks sin generación de código.

### 🎬 La Analogía del Director

Con Mocktail, es como tener un **director de cine** que entrena actores:

| Concepto | Analogía del Director |
|----------|----------------------|
| `when()` | "Cuando te pregunten X, responde Y" |
| `verify()` | "¿Realmente llamaste a ese método?" |
| `any()` | "No me importa el valor, solo responde" |

### 📁 Estructura con Mocktail Paso a Paso

#### Paso 1: Añadir dependencias

En tu `pubspec.yaml`:

```yaml
dev_dependencies:
  mocktail: ^1.0.4
```

#### Paso 2: Crear el test con Mocktail

```dart
// test/features/auth/domain/usecases/login_usecase_test.dart
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/repositories/auth_repository.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';

// Creamos el Mock manualmente (una sola línea, sin build_runner)
class MockIAuthRepository extends Mock implements IAuthRepository {}

void main() {
  late LoginUseCase useCase;
  late MockIAuthRepository mockRepository;

  setUp(() {
    // Crear el mock directamente
    mockRepository = MockIAuthRepository();
    // Inyectar el mock en el UseCase
    useCase = LoginUseCase(repository: mockRepository);
  });

  // Tests van aquí...
}
```

> **Nota:** Con Mocktail no necesitas `build_runner`, ni `@GenerateMocks`, ni archivos `.mocks.dart` generados. Simplemente declaras la clase mock con `extends Mock implements`.

### 🎓 ¿Por qué usar Mocktail?

| Aspecto | Sin mocks | Con Mocktail |
|---------|----------|-------------|
| **Código a escribir** | Mucho (implementar toda la clase) | Poco (solo `extends Mock implements`) |
| **Verificación** | Manual (contadores) | Automática (verify) |
| **Mantenimiento** | Actualizar manualmente | Sin cambios (refleja la interfaz) |
| **Verificación de argumentos** | Manual (guardar last*) | Automática (captureAny) |

---

## 4. Testing de UseCases

### 🤔 ¿Qué es un UseCase?

Un **UseCase** representa una acción que el usuario puede realizar. Ejemplos:
- `LoginUseCase` - Iniciar sesión
- `RegisterUseCase` - Registrarse
- `GetTasksUseCase` - Obtener tareas

### 📁 Archivo Fuente: LoginUseCase

```dart
// lib/features/features/auth/domain/usecases/login_usecase.dart
import 'package:fpdart/fpdart.dart';
import 'package:equatable/equatable.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/core/usecases/usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/repositories/auth_repository.dart';

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

#### Estructura Base con Mocktail

```dart
// test/features/auth/domain/usecases/login_usecase_test.dart
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/repositories/auth_repository.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';

class MockIAuthRepository extends Mock implements IAuthRepository {}

void main() {
  late LoginUseCase useCase;
  late MockIAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockIAuthRepository();
    useCase = LoginUseCase(repository: mockRepository);
  });

  const tEmail = 'test@example.com';
  const tPassword = 'password123';
  const tUser = User(
    id: '123',
    email: tEmail,
    name: 'John',
    lastName: 'Doe',
  );

  // Tests van aquí...
}
```

#### Test 1: Caso de Éxito

```dart
group('LoginUseCase', () {
  test('should return User when login is successful', () async {
    // ARRANGE - Configurar el Mock para éxito
    when(() => mockRepository.login(any(), any()))
        .thenAnswer((_) async => Either.right(tUser));

    // ACT - Ejecutar el UseCase
    final result = await useCase(const LoginParams(
      email: tEmail,
      password: tPassword,
    ));

    // ASSERT - Verificar resultado
    expect(result, equals(Either.right(tUser)));
    
    // ASSERT - Verificar que se llamó al repositorio
    verify(() => mockRepository.login(tEmail, tPassword)).called(1);
  });
});
```

#### Test 2: Caso de Error

```dart
  test('should return ServerFailure when login fails', () async {
    // ARRANGE - Configurar el Mock para fallar
    when(() => mockRepository.login(any(), any())).thenAnswer(
      (_) async => Either.left(ServerFailure('Invalid credentials')),
    );

    // ACT
    final result = await useCase(const LoginParams(
      email: tEmail,
      password: tPassword,
    ));

    // ASSERT
    expect(result, equals(Either.left(ServerFailure('Invalid credentials'))));
    verify(() => mockRepository.login(tEmail, tPassword)).called(1);
  });
```

#### Test 3: Verificar que solo se llama una vez

```dart
  test('should call repository only once', () async {
    // ARRANGE
    when(() => mockRepository.login(any(), any()))
        .thenAnswer((_) async => Either.right(tUser));

    // ACT
    await useCase(const LoginParams(email: tEmail, password: tPassword));

    // ASSERT
    verify(() => mockRepository.login(tEmail, tPassword)).called(1);
    verifyNoMoreInteractions(mockRepository);
  });
```

#### Test 4: Capturar argumentos

```dart
  test('should capture arguments passed to repository', () async {
    // ARRANGE
    when(() => mockRepository.login(any(), any()))
        .thenAnswer((_) async => Either.right(tUser));

    // ACT
    await useCase(const LoginParams(
      email: tEmail,
      password: tPassword,
    ));

    // ASSERT - Capturar los argumentos
    final captured = verify(() => mockRepository.login(
      captureAny(),
      captureAny(),
    )).captured;

    expect(captured[0], tEmail);
    expect(captured[1], tPassword);
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
// lib/features/core/error/failures.dart
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
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';

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
- [ ] Comprender qué es un Mock y por qué lo necesitamos
- [ ] Crear Mocks con Mocktail (`extends Mock implements`)
- [ ] Configurar comportamiento de Mocks (`when() + thenAnswer`)
- [ ] Testear UseCases con éxito y fallo
- [ ] Verificar llamadas con `verify()`
- [ ] Capturar argumentos con `captureAny()`
- [ ] Entender Either<Failure, Success>
- [ ] Testear diferentes tipos de Failure

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 3: Testing Data](./03-data-testing.md)

**Práctica:** [02a-practica-mocktail.md](./02a-practica-mocktail.md) ← ¡Practica con Mocktail!

---

## 💡 Tips Adicionales

### Comandos útiles
```bash
# Ejecutar todos los tests de domain
flutter test test/features/auth/domain/

# Ejecutar con coverage
flutter test --coverage test/features/auth/domain/

# Ver reporte de coverage
genhtml coverage/lcov.info -o coverage/html
```

### API de Mocktail resumida

```dart
// Stubbing
when(() => mock.method(any())).thenAnswer((_) async => value);
when(() => mock.method(any())).thenThrow(Exception('error'));

// Verificación
verify(() => mock.method(args)).called(1);
verifyNever(() => mock.method(any()));
verifyZeroInteractions(mock);
verifyNoMoreInteractions(mock);

// Matchers
any(), any(named: 'param'), any(that: matcher)

// Captura
verify(() => mock.method(captureAny())).captured;
```
