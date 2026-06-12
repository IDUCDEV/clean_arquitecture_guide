# 🏋️ 04a: Práctica - Cubits con bloc_test

> **¿De qué trata esta práctica?** De testear Cubits usando `bloc_test` + **Mocktail** para los UseCases. Esta combinación permite verificar tanto los estados emitidos como las llamadas a los UseCases.

---

## 📋 Ejercicios

- [Ejercicio 1: Configurar Mocks con Mocktail](#ejercicio-1-configurar-mocks-con-mocktail)
- [Ejercicio 2: Testear estado inicial](#ejercicio-2-testear-estado-inicial)
- [Ejercicio 3: Testear transición exitosa](#ejercicio-3-testear-transición-exitosa)
- [Ejercicio 4: Testear transición de error](#ejercicio-4-testear-transición-de-error)
- [Ejercicio 5: Testear verify](#ejercicio-5-testear-verify)

---

## 🎬 Antes de Empezar

Asegúrate de tener las dependencias necesarias:

```yaml
dev_dependencies:
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
```

```bash
flutter pub get
```

---

## Ejercicio 1: Configurar Mocks con Mocktail

### 📝 Tu Misión

Crear los Mocks de los UseCases usando Mocktail.

### ✅ Paso 1: Crear el archivo de test

```bash
mkdir -p test/features/auth/presentation/cubit
touch test/features/auth/presentation/cubit/auth_cubit_test.dart
```

### ✅ Paso 2: Configurar los Mocks

```dart
// test/features/auth/presentation/cubit/auth_cubit_test.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/core/usecases/usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/register_usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/logout_usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/check_auth_status_usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/cubit/auth_cubit.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/cubit/auth_state.dart';

// Mock classes
class MockLoginUseCase extends Mock implements LoginUseCase {}
class MockRegisterUseCase extends Mock implements RegisterUseCase {}
class MockLogoutUseCase extends Mock implements LogoutUseCase {}
class MockCheckAuthStatusUseCase extends Mock implements CheckAuthStatusUseCase {}

void main() {
  late AuthCubit authCubit;
  late MockLoginUseCase mockLoginUseCase;
  late MockRegisterUseCase mockRegisterUseCase;
  late MockLogoutUseCase mockLogoutUseCase;
  late MockCheckAuthStatusUseCase mockCheckAuthStatusUseCase;

  setUp(() {
    mockLoginUseCase = MockLoginUseCase();
    mockRegisterUseCase = MockRegisterUseCase();
    mockLogoutUseCase = MockLogoutUseCase();
    mockCheckAuthStatusUseCase = MockCheckAuthStatusUseCase();
    
    authCubit = AuthCubit(
      loginUseCase: mockLoginUseCase,
      registerUseCase: mockRegisterUseCase,
      logoutUseCase: mockLogoutUseCase,
      checkAuthStatusUseCase: mockCheckAuthStatusUseCase,
    );
  });

  tearDown(() {
    authCubit.close();
  });

  // Datos de prueba
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

---

## Ejercicio 2: Testear estado inicial

### 📝 Tu Misión

Verificar que el Cubit comienza con el estado correcto.

### ✅ Test - Estado inicial

```dart
  group('Estado Inicial', () {
    test('debería tener AuthInitial como estado inicial', () {
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

### ✅ Paso 1: Test - Login exitoso

```dart
  group('login', () {
    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, Authenticated] cuando login es exitoso',
      build: () {
        when(() => mockLoginUseCase(any())).thenAnswer(
          (_) async => Either.right(tUser),
        );
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      expect: () => [
        const AuthLoading(),
        const AuthAuthenticated(user: tUser),
      ],
    );
  });
```

### ✅ Paso 2: Test - Register exitoso

```dart
  group('register', () {
    const tName = 'Jane';
    const tLastName = 'Smith';

    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, Authenticated] cuando registro es exitoso',
      build: () {
        when(() => mockRegisterUseCase(any())).thenAnswer(
          (_) async => Either.right(tUser),
        );
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
        const AuthAuthenticated(user: tUser),
      ],
    );
  });
```

### ✅ Paso 3: Test - Logout

```dart
  group('logout', () {
    blocTest<AuthCubit, AuthState>(
      'debería emitir [AuthLoading, Unauthenticated] cuando logout es exitoso',
      build: () {
        when(() => mockLogoutUseCase(any())).thenAnswer(
          (_) async => const Right(null),
        );
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
        when(() => mockLoginUseCase(any())).thenAnswer(
          (_) async => const Left(ServerFailure('Credenciales inválidas')),
        );
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
        when(() => mockLoginUseCase(any())).thenAnswer(
          (_) async => const Left(NetworkFailure()),
        );
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
        when(() => mockCheckAuthStatusUseCase(any())).thenAnswer(
          (_) async => Either.right(tUser),
        );
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
        when(() => mockCheckAuthStatusUseCase(any())).thenAnswer(
          (_) async => const Right(null),
        );
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
        when(() => mockLoginUseCase(any())).thenAnswer(
          (_) async => Either.right(tUser),
        );
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      expect: () => [
        const AuthLoading(),
        const AuthAuthenticated(user: tUser),
      ],
      verify: (_) {
        // Verificar que se llamó con los parámetros exactos
        verify(() => mockLoginUseCase(const LoginParams(
          email: tEmail,
          password: tPassword,
        ))).called(1);
      },
    );

    blocTest<AuthCubit, AuthState>(
      'debería llamar al UseCase exactamente una vez',
      build: () {
        when(() => mockLoginUseCase(any())).thenAnswer(
          (_) async => Either.right(tUser),
        );
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      verify: (_) {
        verify(() => mockLoginUseCase(any())).called(1);
        verifyNoMoreInteractions(mockLoginUseCase);
      },
    );

    blocTest<AuthCubit, AuthState>(
      'no debería llamar a logout durante login',
      build: () {
        when(() => mockLoginUseCase(any())).thenAnswer(
          (_) async => Either.right(tUser),
        );
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      verify: (_) {
        verifyNever(() => mockLogoutUseCase(any()));
      },
    );

    blocTest<AuthCubit, AuthState>(
      'debería verificar que se llamaron los UseCases correctos',
      build: () {
        when(() => mockLoginUseCase(any())).thenAnswer(
          (_) async => Either.right(tUser),
        );
        return authCubit;
      },
      act: (cubit) => cubit.login(tEmail, tPassword),
      verify: (_) {
        // Verificar que SÍ se llamó login
        verify(() => mockLoginUseCase(any())).called(1);
        // Verificar que NO se llamó register
        verifyNever(() => mockRegisterUseCase(any()));
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
00:00 +10: All tests passed!
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Mocks de UseCases creados con Mocktail
- [ ] Ejercicio 2: Test estado inicial (2 tests)
- [ ] Ejercicio 3: Tests transición exitosa (3 tests)
- [ ] Ejercicio 4: Tests transición de error (4 tests)
- [ ] Ejercicio 5: Tests de verificación (4 tests)
- [ ] **Total: 13+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Configurar el entorno de testing con bloc_test + Mocktail
- ✅ Crear Mocks de UseCases con `extends Mock implements`
- ✅ Testear el estado inicial del Cubit
- ✅ Testear transiciones exitosas (Loading → Authenticated)
- ✅ Testear transiciones de error (Loading → AuthError)
- ✅ Usar `verify()` y `verifyNever()` para confirmar llamadas a UseCases
- ✅ Usar `verifyNoMoreInteractions()` para verificar que no hay llamadas extra

---

## 🚀 Siguiente Paso

**Práctica:** [04b-practica-widgets.md](./04b-practica-widgets.md)

> En esta práctica aprenderás a testear **Widgets** con interacciones reales.

---

## 📚 Resumen: bloc_test + Mocktail

| Herramienta | Uso |
|------------|-----|
| **bloc_test** | Verificar estados emitidos por el Cubit |
| **Mocktail** | Mockear los UseCases inyectados |
| **verify()** | Verificar que se llamó al UseCase |
| **verifyNever()** | Verificar que NO se llamó |
| **verifyNoMoreInteractions()** | Verificar que no hubo llamadas extra |

### Ejemplo completo de la combinación:

```dart
blocTest<AuthCubit, AuthState>(
  'debería emitir estados correctos y llamar al UseCase',
  build: () {
    when(() => mockLoginUseCase(any())).thenAnswer(
      (_) async => Either.right(tUser),
    );
    return authCubit;
  },
  act: (cubit) => cubit.login(tEmail, tPassword),
  expect: () => [
    const AuthLoading(),
    const AuthAuthenticated(user: tUser),
  ],
  verify: (_) {
    verify(() => mockLoginUseCase(const LoginParams(
      email: tEmail,
      password: tPassword,
    ))).called(1);
  },
);
```
