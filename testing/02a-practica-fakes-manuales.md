# 🏋️ 02a: Práctica - Fakes Manuales Paso a Paso

> **¿De qué trata esta práctica?** De crear tu primer **Fake Manual** desde cero. Vamos paso a paso, construyendo el Fake ladrillo por ladrillo.

---

## 📋 Ejercicios

- [Ejercicio 1: Copiar la Interfaz del Repository](#ejercicio-1-copiar-la-interfaz-del-repository)
- [Ejercicio 2: Añadir Banderas de Control](#ejercicio-2-añadir-banderas-de-control)
- [Ejercicio 3: Implementar los Métodos](#ejercicio-3-implementar-los-métodos)
- [Ejercicio 4: Testear un UseCase con el Fake](#ejercicio-4-testear-un-usecase-con-el-fake)

---

## 🎬 Antes de Empezar

Necesitas tener la interfaz del repository. Si no la tienes, aquí está:

```dart
// lib/features/features/auth/domain/repositories/auth_repository.dart
import 'package:fpdart/fpdart.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';

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

---

## Ejercicio 1: Copiar la Interfaz del Repository

### 📝 Tu Misión

Crear una clase que implemente `IAuthRepository`. Por ahora, solo la estructura sin lógica.

### ✅ Paso 1: Crea la estructura de carpetas

```bash
mkdir -p test/helpers
touch test/helpers/fake_auth_repository.dart
```

### ✅ Paso 2: Escribe la clase vacía

Abre `test/helpers/fake_auth_repository.dart` y escribe:

```dart
// test/helpers/fake_auth_repository.dart
import 'package:fpdart/fpdart.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/repositories/auth_repository.dart';

/// Fake implementation of IAuthRepository for testing
/// 
/// This is like an actor that follows our script - we control what it returns
class FakeAuthRepository implements IAuthRepository {
  // We'll add the implementation here...
  
  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    // TODO: Implement later
    throw UnimplementedError();
  }

  @override
  Future<Either<Failure, void>> logout() async {
    // TODO: Implement later
    throw UnimplementedError();
  }

  @override
  Future<Either<Failure, User>> register({
    required String email,
    required String password,
    required String name,
    required String lastName,
  }) async {
    // TODO: Implement later
    throw UnimplementedError();
  }

  @override
  Future<Either<Failure, User?>> checkAuthStatus() async {
    // TODO: Implement later
    throw UnimplementedError();
  }
}
```

### 🧪 Verifica

Ejecuta este comando para verificar que compila:

```bash
dart analyze test/helpers/fake_auth_repository.dart
```

**Resultado esperado:** Sin errores

---

## Ejercicio 2: Añadir Banderas de Control

### 📝 Tu Misión

Añadir **banderas de control** (flags) que nos permitan decidir el comportamiento del Fake. Es como configurar un actor antes de una escena.

### ✅ Paso 1: Añade las propiedades al Fake

Modifica `test/helpers/fake_auth_repository.dart`:

```dart
class FakeAuthRepository implements IAuthRepository {
  // ═══════════════════════════════════════════════════════════
  // BANDERAS DE CONTROL - Configuran el comportamiento
  // ═══════════════════════════════════════════════════════════
  
  /// Cuando es true, los métodos retornarán un Failure
  bool shouldFail = false;
  
  /// Cuando es true, los métodos lanzarán una excepción
  bool shouldThrowException = false;
  
  // ═══════════════════════════════════════════════════════════
  // DATOS A RETORNAR - Qué debe devolver el Fake
  // ═══════════════════════════════════════════════════════════
  
  /// Usuario a retornar en caso de éxito
  User? userToReturn;
  
  /// Failure a retornar en caso de error
  Failure? failureToReturn;
  
  // ═══════════════════════════════════════════════════════════
  // SEGUIMIENTO - Para verificar llamadas
  // ═══════════════════════════════════════════════════════════
  
  /// Cuántas veces se llamó login
  int loginCallCount = 0;
  
  /// Cuántas veces se llamó logout
  int logoutCallCount = 0;
  
  /// Cuántas veces se llamó register
  int registerCallCount = 0;
  
  /// Cuántas veces se llamó checkAuthStatus
  int checkAuthStatusCallCount = 0;
  
  // ═══════════════════════════════════════════════════════════
  // PARÁMETROS RECIBIDOS - Para verificar qué nos pasaron
  // ═══════════════════════════════════════════════════════════
  
  String? lastEmail;
  String? lastPassword;
  String? lastName;
  String? lastLastName;

  // Los métodos van aquí...
}
```

### 🤔 ¿Por qué cada propiedad?

| Propiedad | Propósito | Cuándo usarla en test |
|-----------|-----------|----------------------|
| `shouldFail` | Simular error | `fake.shouldFail = true` |
| `shouldThrowException` | Simular crash | `fake.shouldThrowException = true` |
| `userToReturn` | Qué返回 en éxito | `fake.userToReturn = tUser` |
| `failureToReturn` | Qué返回 en fallo | `fake.failureToReturn = ServerFailure(...)` |
| `loginCallCount` | Verificar que se llamó | `expect(fake.loginCallCount, 1)` |
| `lastEmail` | Verificar parámetros | `expect(fake.lastEmail, 'test@...')` |

---

## Ejercicio 3: Implementar los Métodos

### 📝 Tu Misión

Implementar cada método del Fake con la lógica de las banderas.

### ✅ Paso 1: Implementa el método login

```dart
@override
Future<Either<Failure, User>> login(String email, String password) async {
  // 1. Registrar la llamada (para verificación)
  loginCallCount++;
  
  // 2. Guardar los parámetros (para verificación)
  lastEmail = email;
  lastPassword = password;
  
  // 3. Verificar si debemos lanzar excepción
  if (shouldThrowException) {
    throw Exception('Network error');
  }
  
  // 4. Verificar si debemos fallar
  if (shouldFail) {
    return Either.left(failureToReturn ?? const ServerFailure('Login failed'));
  }
  
  // 5. Éxito - retornar el usuario
  return Either.right(userToReturn!);
}
```

### ✅ Paso 2: Implementa el método logout

```dart
@override
Future<Either<Failure, void>> logout() async {
  // Registrar llamada
  logoutCallCount++;
  
  // Verificar si debemos fallar
  if (shouldFail) {
    return Either.left(failureToReturn ?? const ServerFailure('Logout failed'));
  }
  
  // Éxito
  return Either.right(null);
}
```

### ✅ Paso 3: Implementa el método register

```dart
@override
Future<Either<Failure, User>> register({
  required String email,
  required String password,
  required String name,
  required String lastName,
}) async {
  // Registrar llamada
  registerCallCount++;
  
  // Guardar parámetros
  lastEmail = email;
  lastPassword = password;
  lastName = name;
  lastLastName = lastName;
  
  // Verificar si debemos fallar
  if (shouldFail) {
    return Either.left(failureToReturn ?? const ServerFailure('Registration failed'));
  }
  
  // Éxito
  return Either.right(userToReturn!);
}
```

### ✅ Paso 4: Implementa el método checkAuthStatus

```dart
@override
Future<Either<Failure, User?>> checkAuthStatus() async {
  // Registrar llamada
  checkAuthStatusCallCount++;
  
  // Verificar si debemos fallar
  if (shouldFail) {
    return Either.left(failureToReturn ?? const ServerFailure('Auth check failed'));
  }
  
  // Éxito - puede retornar null si no hay usuario
  return Either.right(userToReturn);
}
```

### ✅ Paso 5: Añade el método reset()

Añade un método para resetear el estado entre tests:

```dart
/// Reset all state for fresh test
/// Como preparar al actor para una nueva escena
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
```

### 🧪 Verifica el Fake completo

Tu archivo debería verse así:

```dart
// test/helpers/fake_auth_repository.dart
import 'package:fpdart/fpdart.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/repositories/auth_repository.dart';

class FakeAuthRepository implements IAuthRepository {
  bool shouldFail = false;
  bool shouldThrowException = false;
  User? userToReturn;
  Failure? failureToReturn;
  
  int loginCallCount = 0;
  int logoutCallCount = 0;
  int registerCallCount = 0;
  int checkAuthStatusCallCount = 0;
  
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
      return Either.left(failureToReturn ?? const ServerFailure('Login failed'));
    }
    
    return Either.right(userToReturn!);
  }

  @override
  Future<Either<Failure, void>> logout() async {
    logoutCallCount++;
    
    if (shouldFail) {
      return Either.left(failureToReturn ?? const ServerFailure('Logout failed'));
    }
    
    return Either.right(null);
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
      return Either.left(failureToReturn ?? const ServerFailure('Registration failed'));
    }
    
    return Either.right(userToReturn!);
  }

  @override
  Future<Either<Failure, User?>> checkAuthStatus() async {
    checkAuthStatusCallCount++;
    
    if (shouldFail) {
      return Either.left(failureToReturn ?? const ServerFailure('Auth check failed'));
    }
    
    return Either.right(userToReturn);
  }
  
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

---

## Ejercicio 4: Testear un UseCase con el Fake

### 📝 Tu Misión

Crear tests para `LoginUseCase` usando el Fake que acabas de crear.

### ✅ Paso 1: Crea el archivo de test

```bash
mkdir -p test/features/auth/domain/usecases
touch test/features/auth/domain/usecases/login_usecase_test.dart
```

### ✅ Paso 2: Escribe el test de caso exitoso

```dart
// test/features/auth/domain/usecases/login_usecase_test.dart
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';

import '../../../../helpers/fake_auth_repository.dart';

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
      // ═══════════════════════════════════════════════════════════
      // ARRANGE: Configurar el Fake para éxito
      // ═══════════════════════════════════════════════════════════
      fakeRepository.userToReturn = tUser;

      // ═══════════════════════════════════════════════════════════
      // ACT: Ejecutar el UseCase
      // ═══════════════════════════════════════════════════════════
      final result = await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ═══════════════════════════════════════════════════════════
      // ASSERT: Verificar resultados
      // ═══════════════════════════════════════════════════════════
      
      // 1. Verificar que retornó el usuario correcto
      expect(result, equals(Either.right(tUser)));
      
      // 2. Verificar que se llamó al repositorio
      expect(fakeRepository.loginCallCount, 1);
      
      // 3. Verificar que se pasaron los parámetros correctos
      expect(fakeRepository.lastEmail, tEmail);
      expect(fakeRepository.lastPassword, tPassword);
    });
  });
}
```

### ✅ Paso 3: Añade el test de caso de error

```dart
    test('should return ServerFailure when login fails', () async {
      // ARRANGE: Configurar el Fake para fallar
      fakeRepository.shouldFail = true;
      fakeRepository.failureToReturn = const ServerFailure('Invalid credentials');

      // ACT
      final result = await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ASSERT
      expect(result, equals(Either.left(ServerFailure('Invalid credentials'))));
      expect(fakeRepository.loginCallCount, 1);
    });
```

### ✅ Paso 4: Añade el test de verificación de parámetros

```dart
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
```

### ✅ Paso 5: Añade el test de llamada única

```dart
    test('should call repository only once', () async {
      // ARRANGE
      fakeRepository.userToReturn = tUser;

      // ACT
      await useCase(const LoginParams(email: tEmail, password: tPassword));

      // ASSERT
      expect(fakeRepository.loginCallCount, 1);
    });
```

### 🧪 Ejecuta los tests

```bash
flutter test test/features/auth/domain/usecases/login_usecase_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +4: All tests passed!
```

---

## 🎉 ¡Felicitaciones!

Has creado tu primer Fake Manual y lo has usado en tests. Ahora entiendes:

- ✅ Copiar una interfaz para crear un Fake
- ✅ Añadir banderas de control (`shouldFail`, `shouldThrowException`)
- ✅ Añadir propiedades para datos de retorno (`userToReturn`)
- ✅ Añadir contadores para verificar llamadas (`*CallCount`)
- ✅ Guardar parámetros recibidos (`lastEmail`, etc.)
- ✅ Implementar métodos con toda la lógica
- ✅ Usar el Fake en tests de UseCase

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Estructura básica del Fake - 4 líneas
- [ ] Ejercicio 2: Banderas de control añadidas - 10+ propiedades
- [ ] Ejercicio 3: Métodos implementados - 4 métodos + reset
- [ ] Ejercicio 4: Tests de UseCase - 4 tests ejecutándose

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 3: Testing Data](./03-data-testing.md)

**Práctica:** 
- [03a-practica-fixtures-models.md](./03a-practica-fixtures-models.md)
- [03b-practica-datasources.md](./03b-practica-datasources.md)

> En la siguiente práctica aprenderás a testear la capa **Data**: Models, DataSources y Repositories.
