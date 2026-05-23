# 🏋️ 02b: Mocktail - Guía Completa

> **¿De qué trata esta guía?** De dominar Mocktail: desde los conceptos básicos hasta ejercicios prácticos por capa de Clean Architecture, incluyendo migración desde Fakes.

---

## 📋 Índice

1. [Introducción: ¿Qué es Mocktail?](#1-introducción-qué-es-mocktail)
2. [Configuración](#2-configuración)
3. [Creación de Mocks](#3-creación-de-mocks)
4. [Stubbing con when()](#4-stubbing-con-when)
5. [Verificación con verify()](#5-verificación-con-verify)
6. [Matchers: any() y captureAny()](#6-matchers-any-y-captureany)
7. [Errores Comunes](#7-errores-comunes)
8. [Práctica por Capa](#8-práctica-por-capa)
9. [Fakes vs Mocks - ¿Cuándo usar cada uno?](#9-fakes-vs-mocks---cuándo-usar-cada-uno)
10. [Migración de Fakes a Mocks](#10-migración-de-fakes-a-mocks)
11. [Resumen Cheatsheet](#11-resumen-cheatsheet)

---

## 1. Introducción: ¿Qué es Mocktail?

### 🎭 La Analogía del Actor de Reparto

Imagina que estás rodando una película. Sin Mocktail, escribes el guión completo de cada actor. Con Mocktail, contratas un actor entrenado: le das instrucciones generales ("cuando te pregunten X, responde Y") y él improvisa.

Mocktail es una biblioteca que **crea implementaciones falsas de interfaces** sin necesidad de generación de código:

```dart
// Una línea - sin build_runner, sin @GenerateMocks
class MockIAuthRepository extends Mock implements IAuthRepository {}
```

### ✨ Ventajas frente a Mockito

| Ventaja | Mockito | Mocktail |
|---------|---------|----------|
| `build_runner` | ✅ Requerido | ❌ No necesario |
| `@GenerateMocks` | ✅ Requerido | ❌ No necesario |
| Archivos `.mocks.dart` | ✅ Generados | ❌ No existen |
| Null safety nativo | ⚠️ Desde v5 | ✅ Desde inicio |
| Sintaxis | `when(mock.method(any))` | `when(() => mock.method(any()))` |

### 📊 ¿Por qué usar Mocks?

| Aspecto | Sin Mocks (implementación real) | Con Mocktail |
|---------|-------------------------------|--------------|
| **Setup inicial** | Escribes toda la implementación | Una línea: `extends Mock implements` |
| **Verificación de llamadas** | No disponible | Automática (`verify`) |
| **Verificación de argumentos** | Manual | Automática |
| **Mantenimiento** | Alto (actualizar implementación) | Bajo (refleja la interfaz) |
| **Ideal para** | Tests de integración | Tests unitarios |

---

## 2. Configuración

### 📦 pubspec.yaml

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.4
```

```bash
flutter pub get
```

No necesitas `build.yaml`, `build_runner`, ni configuración adicional.

---

## 3. Creación de Mocks

### 📝 La Sintaxis

```dart
import 'package:mocktail/mocktail.dart';

class MockIAuthRepository extends Mock implements IAuthRepository {}
```

### 🔍 Cómo funciona

| Elemento | Descripción |
|----------|-------------|
| `class MockIAuthRepository` | Nombre de la clase mock (convención: `Mock` + nombre interfaz) |
| `extends Mock` | Le dice a Mocktail que esta clase es un mock |
| `implements IAuthRepository` | Implementa la interfaz automáticamente |

### ⚠️ Fallback Values

Cuando usas `any()` con tipos personalizados, Mocktail necesita un "fallback value":

```dart
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});
```

Esto solo es necesario para tipos que no son `String`, `int`, `bool`, etc.

---

## 4. Stubbing con when()

### 🎯 Concepto: "Cuando ocurra X, retorna Y"

> **Importante:** En Mocktail, `when()` recibe siempre una función anónima: `when(() => mock.metodo(...))`

### 📚 Métodos de Stubbing

#### thenAnswer() - Respuesta asíncrona (la más usada)

```dart
when(() => mockRepository.login(any(), any()))
    .thenAnswer((_) async => Either.right(tUser));

// También para síncrono
when(() => mockRepository.getCount()).thenAnswer((_) => 42);
```

#### thenReturn() - Respuesta directa (síncrono)

```dart
when(() => mockRepository.isReady()).thenReturn(true);
```

#### thenThrow() - Lanzar excepción

```dart
when(() => mockRepository.login(any(), any()))
    .thenThrow(Exception('Network error'));
```

### 🔗 Encadenar respuestas

```dart
when(() => mockRepository.getProduct(any()))
    .thenAnswer((_) async => Either.right(tProduct))
    .thenAnswer((_) async => Either.left(ServerFailure()));
```

### 📊 thenAnswer vs thenReturn

| Método | Cuándo usarlo |
|--------|---------------|
| `thenAnswer()` | Métodos async o cuando necesitas acceder a los argumentos |
| `thenReturn()` | Valores síncronos ya disponibles |

---

## 5. Verificación con verify()

### 🎯 Concepto: "¿Realmente se llamó?"

```dart
verify(() => mockRepository.login(tEmail, tPassword)).called(1);
```

### 📚 Métodos de Verificación

```dart
// Exactamente N veces
verify(() => mock.method(args)).called(1);
verify(() => mock.method(args)).called(3);

// Nunca se llamó
verifyNever(() => mock.method(any()));

// No hubo más interacciones
verifyNoMoreInteractions(mock);

// Ninguna interacción en absoluto
verifyZeroInteractions(mock);
```

---

## 6. Matchers: any() y captureAny()

### 📚 any()

```dart
// Cualquier valor posicional
when(() => mock.getProduct(any())).thenAnswer(...);
verify(() => mock.getProduct(any())).called(1);

// Cualquier valor para argumento nombrado
when(() => mock.updateProduct(
  id: any(named: 'id'),
  product: any(named: 'product'),
)).thenAnswer(...);

// Con condición personalizada
when(() => mock.getProduct(any(that: startsWith('PROD-'))))
    .thenAnswer(...);
```

### 📚 captureAny()

```dart
final captured = verify(() => mock.getProduct(captureAny())).captured;
expect(captured.first, '123');

// Múltiples argumentos
final captured = verify(() => mock.updateProduct(
  id: captureAny(named: 'id'),
  product: captureAny(named: 'product'),
)).captured;
```

### 📊 Tabla de Matchers

| Matcher | Uso | Ejemplo |
|---------|-----|---------|
| `any()` | Cualquier valor posicional | `getProduct(any())` |
| `any(named: 'x')` | Cualquier valor para argumento 'x' | `updateProduct(id: any(named: 'id'))` |
| `any(that: matcher)` | Valor que cumple condición | `any(that: equals('123'))` |
| `captureAny()` | Capturar cualquier valor | `captureAny()` |

---

## 7. Errores Comunes

### ❌ "MissingStubError"

**Causa:** Llamaste a un método del mock sin configurarlo con `when()`.

```dart
// ❌ FALLA
when(() => mock.getProduct('123')).thenAnswer(...);
final result = await mock.getProduct('999'); // ¡No stubbed!

// ✅ CORRECTO
when(() => mock.getProduct(any())).thenAnswer(...);
```

### ❌ "No matching invocation"

**Causa:** Verificaste un método que nunca fue llamado.

```dart
// ❌ FALLA - getProduct nunca fue llamado
verify(() => mock.getProduct('123'));

// ✅ CORRECTO - Llama primero al método en el test
await useCase('123');
verify(() => mock.getProduct('123'));
```

### ❌ Fallback values no registrados

**Causa:** Usas `any()` con un tipo personalizado sin registrar fallback.

```dart
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});
```

---

## 8. Práctica por Capa

### 🏗️ ¿Qué mockear en cada capa?

| Capa | Qué Mockear | Ejemplo |
|------|-------------|---------|
| **Domain** | Repository Interfaces | `MockIAuthRepository` |
| **Data** | DataSources | `MockAuthRemoteDataSource` |
| **Presentation** | UseCases en Cubits | `MockLoginUseCase` |
| **Core** | NetworkInfo, Storage | `MockNetworkInfo` |

> **Regla de Oro:** Mockea las **dependencias externas** de cada capa, nunca la lógica interna.

---

### 🎯 CAPA DOMAIN: Repository + UseCase

#### Ejercicio: LoginUseCase

Prepara el entorno:

```bash
mkdir -p test/features/auth/domain/usecases
```

**`test/helpers/mocks.dart`** (mocks compartidos):
```dart
import 'package:mocktail/mocktail.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/repositories/auth_repository.dart';

class MockIAuthRepository extends Mock implements IAuthRepository {}
```

**`test/features/auth/domain/usecases/login_usecase_test.dart`:**

```dart
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';
import '../../../../helpers/mocks.dart';

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

  group('LoginUseCase', () {
    test('should return User when login is successful', () async {
      // Arrange
      when(() => mockRepository.login(any(), any()))
          .thenAnswer((_) async => Either.right(tUser));

      // Act
      final result = await useCase(
        const LoginParams(email: tEmail, password: tPassword),
      );

      // Assert
      expect(result, equals(Either.right(tUser)));
      verify(() => mockRepository.login(tEmail, tPassword)).called(1);
    });

    test('should return ServerFailure when login fails', () async {
      when(() => mockRepository.login(any(), any())).thenAnswer(
        (_) async => Either.left(ServerFailure('Invalid credentials')),
      );

      final result = await useCase(
        const LoginParams(email: tEmail, password: tPassword),
      );

      expect(result, equals(Either.left(ServerFailure('Invalid credentials'))));
      verify(() => mockRepository.login(tEmail, tPassword)).called(1);
    });

    test('should call repository only once', () async {
      when(() => mockRepository.login(any(), any()))
          .thenAnswer((_) async => Either.right(tUser));

      await useCase(const LoginParams(email: tEmail, password: tPassword));

      verify(() => mockRepository.login(tEmail, tPassword)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should capture arguments passed to repository', () async {
      when(() => mockRepository.login(any(), any()))
          .thenAnswer((_) async => Either.right(tUser));

      await useCase(const LoginParams(email: tEmail, password: tPassword));

      final captured = verify(() => mockRepository.login(
        captureAny(),
        captureAny(),
      )).captured;

      expect(captured[0], tEmail);
      expect(captured[1], tPassword);
    });
  });
}
```

```bash
flutter test test/features/auth/domain/usecases/login_usecase_test.dart
```

---

### 🎯 CAPA DATA: DataSources (Remote/Local)

#### Ejercicio: AuthRemoteDataSource

**`test/helpers/mocks.dart`** (añadir):
```dart
class MockClient extends Mock implements http.Client {}
```

**`test/features/auth/data/datasources/auth_remote_data_source_test.dart`:**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mocktail/mocktail.dart';
import 'dart:convert';
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';
import '../../../../helpers/mocks.dart';

void main() {
  late AuthRemoteDataSourceImpl dataSource;
  late MockClient mockClient;

  setUp(() {
    mockClient = MockClient();
    dataSource = AuthRemoteDataSourceImpl(
      client: mockClient,
      baseUrl: 'https://api.example.com',
    );
  });

  group('login', () {
    const tEmail = 'test@example.com';
    const tPassword = 'password123';
    final tUserJson = {'id': '123', 'email': tEmail, 'name': 'John', 'last_name': 'Doe'};

    test('should return UserModel when response is 200', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response(json.encode(tUserJson), 200));

      final result = await dataSource.login(tEmail, tPassword);

      expect(result, isA<UserModel>());
      expect(result.email, tEmail);
    });

    test('should throw ServerException when response is 401', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response('Unauthorized', 401));

      expect(
        () => dataSource.login(tEmail, tPassword),
        throwsA(isA<ServerException>()),
      );
    });

    test('should call correct endpoint', () async {
      when(() => mockClient.post(
        any(),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).thenAnswer((_) async => http.Response(json.encode(tUserJson), 200));

      await dataSource.login(tEmail, tPassword);

      verify(() => mockClient.post(
        Uri.parse('https://api.example.com/auth/login'),
        headers: any(named: 'headers'),
        body: any(named: 'body'),
      )).called(1);
    });
  });
}
```

```bash
flutter test test/features/auth/data/datasources/
```

---

### 🎯 CAPA PRESENTATION: Cubits + Mocktail

#### Ejercicio: AuthCubit con bloc_test + Mocktail

**`test/helpers/mocks.dart`** (añadir):
```dart
class MockLoginUseCase extends Mock implements LoginUseCase {}
```

**`test/features/auth/presentation/cubit/auth_cubit_test.dart`:**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/cubit/auth_cubit.dart';
import '../../../../helpers/mocks.dart';

void main() {
  late MockLoginUseCase mockLoginUseCase;

  setUp(() {
    mockLoginUseCase = MockLoginUseCase();
  });

  const tEmail = 'test@example.com';
  const tPassword = 'password123';
  const tUser = User(
    id: '123', email: tEmail, name: 'John', lastName: 'Doe',
  );

  group('AuthCubit', () {
    blocTest<AuthCubit, AuthState>(
      'should emit [AuthLoading, Authenticated] when login succeeds',
      build: () => AuthCubit(loginUseCase: mockLoginUseCase),
      act: (cubit) => cubit.login(tEmail, tPassword),
      setUp: () {
        when(() => mockLoginUseCase(any()))
            .thenAnswer((_) async => const Either.right(tUser));
      },
      expect: () => [
        const AuthLoading(),
        const Authenticated(user: tUser),
      ],
    );

    blocTest<AuthCubit, AuthState>(
      'should emit [AuthLoading, AuthError] when login fails',
      build: () => AuthCubit(loginUseCase: mockLoginUseCase),
      act: (cubit) => cubit.login(tEmail, tPassword),
      setUp: () {
        when(() => mockLoginUseCase(any()))
            .thenAnswer((_) async => Either.left(ServerFailure('Error')));
      },
      expect: () => [
        const AuthLoading(),
        const AuthError(message: 'Error'),
      ],
    );
  });
}
```

```bash
flutter test test/features/auth/presentation/cubit/
```

---

### 🎯 CAPA CORE: NetworkInfo

**`test/helpers/mocks.dart`** (añadir):
```dart
class MockInternetConnectionChecker extends Mock
    implements InternetConnectionCheckerPlus {}
```

**`test/core/network/network_info_test.dart`:**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:internet_connection_checker_plus/internet_connection_checker_plus.dart';
import 'package:mi_proyecto_flutter/clean/core/network/network_info.dart';
import '../../helpers/mocks.dart';

void main() {
  late NetworkInfoImpl networkInfo;
  late MockInternetConnectionChecker mockChecker;

  setUp(() {
    mockChecker = MockInternetConnectionChecker();
    networkInfo = NetworkInfoImpl(connectionChecker: mockChecker);
  });

  group('isConnected', () {
    test('should return true when connected', () async {
      when(() => mockChecker.hasConnection).thenAnswer((_) async => true);
      final result = await networkInfo.isConnected;
      expect(result, isTrue);
    });

    test('should return false when not connected', () async {
      when(() => mockChecker.hasConnection).thenAnswer((_) async => false);
      final result = await networkInfo.isConnected;
      expect(result, isFalse);
    });

    test('should call connection checker', () async {
      when(() => mockChecker.hasConnection).thenAnswer((_) async => true);
      await networkInfo.isConnected;
      verify(() => mockChecker.hasConnection).called(1);
    });
  });
}
```

---

## 9. Fakes vs Mocks - ¿Cuándo usar cada uno?

### 📊 Comparación directa

| Aspecto | Fake | Mock (Mocktail) |
|---------|------|----------------|
| **Código a escribir** | Mucho (implementar toda la interfaz) | Poco (`extends Mock implements`) |
| **Verificación** | Manual (contadores) | Automática (`verify()`) |
| **Debugging** | Fácil (código visible) | Regular (API de Mocktail) |
| **Mantenimiento** | Actualizar manualmente | Sin cambios (refleja interfaz) |
| **Flexibilidad** | Alta (lógica personalizada) | Limitada a la API de Mocktail |
| **build_runner** | No necesita | No necesita |

### ✅ Guía de decisión

```
¿Interfaz simple (2-3 métodos) y estable?  →  Usa FAKE
  └── Ej: IAuthRepository.login/logout

¿Interfaz compleja (5+ métodos) o de terceros?  →  Usa MOCK
  └── Ej: IPaymentGateway con 10 métodos

¿Necesitas verificar argumentos exactos?  →  Usa MOCK
  └── verify(() => mock.login('email', 'pass')).called(1)

¿Necesitas lógica interna compleja?  →  Usa FAKE
  └── Ej: FakeCacheRepository con lógica de invalidación

¿Proyecto pequeño (<30 tests)?  →  Usa FAKE
¿Proyecto mediano/grande?  →  Usa MOCK (consistencia)
```

### 📝 Ejemplo comparativo lado a lado

**Con Fake:**
```dart
class FakeAuthRepository implements IAuthRepository {
  bool shouldFail = false;
  User? userToReturn;
  int loginCallCount = 0;
  String? lastEmail;

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    loginCallCount++;
    lastEmail = email;
    if (shouldFail) return Either.left(ServerFailure('Error'));
    return Either.right(userToReturn!);
  }
}

// Test
fake.userToReturn = tUser;
await useCase(...);
expect(fake.loginCallCount, 1);
expect(fake.lastEmail, tEmail);
```

**Con Mocktail:**
```dart
class MockIAuthRepository extends Mock implements IAuthRepository {}

// Test
when(() => mock.login(any(), any())).thenAnswer((_) async => Either.right(tUser));
await useCase(...);
verify(() => mock.login(tEmail, tPassword)).called(1);
verifyNoMoreInteractions(mock);
```

---

## 10. Migración de Fakes a Mocks

### 🎯 Señales de que necesitas migrar

1. **Proyecto grande** (>50 tests con Fakes)
2. **Múltiples desarrolladores** necesitan consistencia
3. **Interfaces cambian frecuentemente** (mantener Fakes es costoso)
4. **Necesitas verificación estricta** de llamadas

### 📝 Migración Paso a Paso

#### Paso 1: Añadir mocktail a pubspec.yaml

```yaml
dev_dependencies:
  mocktail: ^1.0.4
```

#### Paso 2: Crear mock classes

```dart
// test/helpers/mocks.dart
import 'package:mocktail/mocktail.dart';

class MockIAuthRepository extends Mock implements IAuthRepository {}
class MockAuthRemoteDataSource extends Mock implements AuthRemoteDataSource {}
class MockNetworkInfo extends Mock implements NetworkInfo {}
```

#### Paso 3: Reemplazar inyección

```dart
// ANTES
setUp(() {
  fakeRepository = FakeAuthRepository();
  useCase = LoginUseCase(repository: fakeRepository);
});

// DESPUÉS
setUp(() {
  mockRepository = MockIAuthRepository();
  useCase = LoginUseCase(repository: mockRepository);
});
```

#### Paso 4: Reemplazar configuración

```dart
// ANTES
fakeRepository.userToReturn = tUser;
fakeRepository.shouldFail = true;

// DESPUÉS
when(() => mockRepository.login(any(), any()))
    .thenAnswer((_) async => Either.right(tUser));
when(() => mockRepository.login(any(), any()))
    .thenAnswer((_) async => Either.left(ServerFailure('Error')));
```

#### Paso 5: Reemplazar verificación

```dart
// ANTES
expect(fakeRepository.loginCallCount, 1);
expect(fakeRepository.lastEmail, tEmail);

// DESPUÉS
verify(() => mockRepository.login(tEmail, tPassword)).called(1);
```

### 📝 Ejercicio de Migración

Migra este test de Fake a Mocktail:

```dart
// ANTES (con Fakes)
test('should cache user after successful login', () async {
  fakeRemote.userToReturn = tUserModel;
  fakeNetwork.isOnline = true;

  await repository.login(tEmail, tPassword);

  expect(fakeLocal.lastCachedUser, equals(tUserModel));
});
```

<details>
<summary>Ver solución</summary>

```dart
// DESPUÉS (con Mocktail)
test('should cache user after successful login', () async {
  when(() => mockNetwork.isConnected).thenAnswer((_) async => true);
  when(() => mockRemote.login(any(), any()))
      .thenAnswer((_) async => tUserModel);
  when(() => mockLocal.cacheUser(any()))
      .thenAnswer((_) async => {});

  await repository.login(tEmail, tPassword);

  verify(() => mockLocal.cacheUser(tUserModel)).called(1);
});
```
</details>

---

## 11. Resumen Cheatsheet

### Configuración

```yaml
# pubspec.yaml
dev_dependencies:
  mocktail: ^1.0.4
```

```dart
// test file
import 'package:mocktail/mocktail.dart';

class MockIAuthRepository extends Mock implements IAuthRepository {}
```

### Stubbing

```dart
when(() => mock.method(args)).thenAnswer((_) => value);
when(() => mock.method(args)).thenThrow(Exception('error'));
when(() => mock.method(args))
    .thenAnswer((_) => value1)
    .thenAnswer((_) => value2);
```

### Verificación

```dart
verify(() => mock.method(args)).called(1);
verify(() => mock.method(args)).called(n);
verifyNever(() => mock.method(any()));
verifyNoMoreInteractions(mock);
verifyZeroInteractions(mock);
```

### Matchers

```dart
any()                    // Cualquier valor
any(named: 'param')      // Cualquier valor para argumento nombrado
any(that: matcher)       // Valor que cumple condición
captureAny()             // Capturar cualquier valor
```

### Fallback Values

```dart
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});
```

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 3: Testing Data](./03-data-testing.md)

**Práctica:**
- [03a-practica-fixtures-models.md](./03a-practica-fixtures-models.md)
- [03b-practica-datasources.md](./03b-practica-datasources.md)
