# 🏋️ 04a: Práctica - Cubits con bloc_test

> **¿De qué trata esta práctica?** De testear Cubits usando `bloc_test`, una herramienta especializada que facilita verificar los estados que emite el Cubit.

---

## 📋 Ejercicios

- [Ejercicio 1: Preparar el entorno](#ejercicio-1-preparar-el-entorno)
- [Ejercicio 2: Testear estado inicial](#ejercicio-2-testear-estado-inicial)
- [Ejercicio 3: Testear transición exitosa](#ejercicio-3-testear-transición-exitosa)
- [Ejercicio 4: Testear transición de error](#ejercicio-4-testear-transición-de-error)
- [Ejercicio 5: Testear verify](#ejercicio-5-testear-verify)

---

## 🎬 Antes de Empezar

Asegúrate de tener `bloc_test` en pubspec.yaml:

```yaml
dev_dependencies:
  bloc_test: ^9.1.0
```

```bash
flutter pub get
```

---

## Ejercicio 1: Preparar el entorno

### 📝 Tu Misión

Preparar los Fakes necesarios para testear el Cubit.

### ✅ Paso 1: Crear el Fake del UseCase

```bash
touch test/helpers/fake_usecases.dart
```

```dart
// test/helpers/fake_usecases.dart
import 'package:fpdart/fpdart.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/register_usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/logout_usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/check_auth_status_usecase.dart';

/// Fake LoginUseCase
class FakeLoginUseCase implements LoginUseCase {
  final IAuthRepository repository;
  
  FakeLoginUseCase({required this.repository});
  
  @override
  Future<Either<Failure, User>> call(LoginParams params) async {
    return await repository.login(params.email, params.password);
  }
}

/// Fake RegisterUseCase  
class FakeRegisterUseCase implements RegisterUseCase {
  final IAuthRepository repository;
  
  FakeRegisterUseCase({required this.repository});
  
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

/// Fake LogoutUseCase
class FakeLogoutUseCase implements LogoutUseCase {
  final IAuthRepository repository;
  
  FakeLogoutUseCase({required this.repository});
  
  @override
  Future<Either<Failure, void>> call(NoParams params) async {
    return await repository.logout();
  }
}

/// Fake CheckAuthStatusUseCase
class FakeCheckAuthStatusUseCase implements CheckAuthStatusUseCase {
  final IAuthRepository repository;
  
  FakeCheckAuthStatusUseCase({required this.repository});
  
  @override
  Future<Either<Failure, User?>> call(NoParams params) async {
    return await repository.checkAuthStatus();
  }
}
```

---

## Ejercicio 2: Testear estado inicial

### 📝 Tu Misión

Verificar que el Cubit comienza con el estado correcto.

### ✅ Paso 1: Crea el archivo de test

```bash
mkdir -p test/features/auth/presentation/cubit
touch test/features/auth/presentation/cubit/auth_cubit_test.dart
```

### ✅ Paso 2: Configura el test base

```dart
// test/features/auth/presentation/cubit/auth_cubit_test.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/cubit/auth_cubit.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/cubit/auth_state.dart';

import '../../../../helpers/fake_auth_repository.dart';

void main() {
  late AuthCubit authCubit;
  late FakeAuthRepository fakeRepository;

  setUp(() {
    fakeRepository = FakeAuthRepository();
    authCubit = AuthCubit(
      loginUseCase: FakeLoginUseCase(repository: fakeRepository),
      registerUseCase: FakeRegisterUseCase(repository: fakeRepository),
      logoutUseCase: FakeLogoutUseCase(repository: fakeRepository),
      checkAuthStatusUseCase: FakeCheckAuthStatusUseCase(repository: fakeRepository),
    );
  });

  tearDown(() {
    authCubit.close();
    fakeRepository.reset();
  });

  // Tests van aquí...
}
```

### ✅ Paso 3: Test - Estado inicial

```dart
  group('Estado Inicial', () {
    test('debería tener AuthInitial como estado inicial', () {
      // El Cubit ya se crea en setUp, verificamos su estado
      expect(authCubit.state, equals(const AuthInitial()));
    });

    blocTest<AuthCubit, AuthState>(
      'debería emitir el estado inicial inmediatamente',
      build: () => authCubit,
      expect: () => [], // No se emite ningún estado adicional
    );
  });
```

---

## Ejercicio 3: Testear transición exitosa

### 📝 Tu Misión

Verificar que el Cubit emite los estados correctos cuando el login es exitoso.

### ✅ Paso 1: Añade datos de prueba

```dart
  // Datos de prueba
  const tEmail = 'test@example.com';
  const tPassword = 'password123';
  const tUser = User(
    id: '123',
    email: tEmail,
    name: 'John',
    lastName: 'Doe',
  );
```

### ✅ Paso 2: Test - Login exitoso

```dart
  group('login', () {
    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, Authenticated] cuando login es exitoso',
      build: () {
        // Configurar el Fake para éxito
        fakeRepository.userToReturn = tUser;
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      expect: () => [
        const AuthLoading(),
        const Authenticated(user: tUser),
      ],
    );
  });
```

### ✅ Paso 3: Test - Register exitoso

```dart
  group('register', () {
    const tName = 'Jane';
    const tLastName = 'Smith';

    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, Authenticated] cuando registro es exitoso',
      build: () {
        fakeRepository.userToReturn = tUser;
        return authCubit;
      },
      act: (cubit) => cubit.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      ),
      expect: () => [
        const AuthLoading(),
        const Authenticated(user: tUser),
      ],
    );
  });
```

### ✅ Paso 4: Test - Logout

```dart
  group('logout', () {
    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, Unauthenticated] cuando logout es exitoso',
      build: () {
        return authCubit;
      },
      act: (cubit) => cubit.logout(),
      expect: () => [
        const AuthLoading(),
        const Unauthenticated(),
      ],
    );
  });
```

---

## Ejercicio 4: Testear transición de error

### 📝 Tu Misión

Verificar que el Cubit maneja correctamente los errores.

### ✅ Paso 1: Test - Login fallido

```dart
  group('login - error', () {
    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, AuthError] cuando login falla',
      build: () {
        fakeRepository.shouldFail = true;
        fakeRepository.failureToReturn = const ServerFailure('Credenciales inválidas');
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      expect: () => [
        const AuthLoading(),
        const AuthError(message: 'Credenciales inválidas'),
      ],
    );

    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, AuthError] cuando no hay conexión',
      build: () {
        fakeRepository.shouldFail = true;
        fakeRepository.failureToReturn = const NetworkFailure();
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      expect: () => [
        const AuthLoading(),
        const AuthError(message: 'No internet connection'),
      ],
    );
  });
```

### ✅ Paso 2: Test - CheckAuthStatus

```dart
  group('checkAuthStatus', () {
    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, Authenticated] cuando hay usuario',
      build: () {
        fakeRepository.userToReturn = tUser;
        return authCubit;
      },
      act: (cubit) => cubit.checkAuthStatus(),
      expect: () => [
        const AuthLoading(),
        const AuthAuthenticated(user: tUser),
      ],
    );

    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, Unauthenticated] cuando no hay usuario',
      build: () {
        fakeRepository.userToReturn = null;
        return authCubit;
      },
      act: (cubit) => cubit.checkAuthStatus(),
      expect: () => [
        const AuthLoading(),
        const Unauthenticated(),
      ],
    );
  });
```

---

## Ejercicio 5: Testear verify

### 📝 Tu Misión

Verificar que el Cubit llama a los UseCases con los parámetros correctos.

### ✅ Paso 1: Test - Verificar parámetros

```dart
  group('Verificación de llamadas', () {
    blocTest<AuthCubit, AuthState>(
      'debería llamar a login con parámetros correctos',
      build: () {
        fakeRepository.userToReturn = tUser;
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      expect: () => [
        const AuthLoading(),
        const AuthAuthenticated(user: tUser),
      ],
      verify: (_) {
        // Verificar parámetros
        expect(fakeRepository.lastEmail, tEmail);
        expect(fakeRepository.lastPassword, tPassword);
      },
    );

    blocTest<AuthCubit, AuthState>(
      'debería incrementar contador de llamadas',
      build: () {
        fakeRepository.userToReturn = tUser;
        return authCubit;
      },
      act: (cubit) async {
        await cubit.login(tEmail, tPassword);
        await cubit.login(tEmail, tPassword);
      },
      verify: (_) {
        expect(fakeRepository.loginCallCount, 2);
      },
    );

    blocTest<AuthCubit, AuthState>(
      'no debería llamar a logout durante login',
      build: () {
        fakeRepository.userToReturn = tUser;
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      verify: (_) {
        expect(fakeRepository.logoutCallCount, 0);
      },
    );
  });
```

---

## 🧪 Ejecuta todos los tests

```bash
flutter test test/features/auth/presentation/cubit/auth_cubit_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +8: All tests passed!
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Fakes de UseCases creados
- [ ] Ejercicio 2: Test estado inicial (2 tests)
- [ ] Ejercicio 3: Tests transición exitosa (3 tests)
- [ ] Ejercicio 4: Tests transición de error (4 tests)
- [ ] Ejercicio 5: Tests de verificación (3 tests)
- [ ] **Total: 12+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Configurar el entorno de testing con bloc_test
- ✅ Testear el estado inicial del Cubit
- ✅ Testear transiciones exitosas (Loading → Authenticated)
- ✅ Testear transiciones de error (Loading → AuthError)
- ✅ Usar `verify` para confirmar llamadas a UseCases

---

## 🚀 Siguiente Paso

**Práctica:** [04b-practica-widgets.md](./04b-practica-widgets.md)

> En esta práctica aprenderás a testear **Widgets** con interacciones reales.
