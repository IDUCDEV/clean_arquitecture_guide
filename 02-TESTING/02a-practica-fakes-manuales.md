# 🏋️ 02a: Práctica - Mockito Paso a Paso

> **¿De qué trata esta práctica?** De crear tu primer **Mock** con Mockito desde cero usando generación automática de código. Vamos paso a paso, construyendo los conocimientos ladrillo por ladrillo.

---

## 📋 Ejercicios

- [Ejercicio 1: Configurar el entorno](#ejercicio-1-configurar-el-entorno)
- [Ejercicio 2: Generar el Mock automáticamente](#ejercicio-2-generar-el-mock-automáticamente)
- [Ejercicio 3: Configurar respuestas con when()](#ejercicio-3-configurar-respuestas-con-when)
- [Ejercicio 4: Testear un UseCase con el Mock](#ejercicio-4-testear-un-usecase-con-el-mock)

---

## 🎬 Antes de Empezar

### 📦 Dependencias necesarias

Asegúrate de tener en tu `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

```bash
flutter pub get
```

### 📝 Interfaz del Repository

Necesitas tener la interfaz del repository. Si no la tienes, aquí está:

```dart
// lib/features/auth/domain/repositories/auth_repository.dart
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

## Ejercicio 1: Configurar el Entorno

### 📝 Tu Misión

Crear la estructura de carpetas y el archivo de test con las anotaciones necesarias.

### ✅ Paso 1: Crea la estructura de carpetas

```bash
mkdir -p test/features/auth/domain/usecases
```

### ✅ Paso 2: Crea el archivo de test con anotaciones

Abre `test/features/auth/domain/usecases/login_usecase_test.dart` y escribe:

```dart
// test/features/auth/domain/usecases/login_usecase_test.dart
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/repositories/auth_repository.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';

/// Esta anotación le dice a Mockito que genere un mock para IAuthRepository
@GenerateMocks([IAuthRepository])
import 'login_usecase_test.mocks.dart';

void main() {
  // Tests irán aquí...
}
```

### 🤔 ¿Qué es @GenerateMocks?

| Elemento | Descripción |
|----------|-------------|
| `@GenerateMocks([IAuthRepository])` | Le dice a Mockito qué interfaz mockear |
| `part 'login_usecase_test.mocks.dart'` | Archivo que se generará automáticamente |

### 🧪 Verifica

Ejecuta este comando para generar el mock:

```bash
dart run build_runner build --delete-conflicting-outputs
```

**Resultado esperado:** Se crea el archivo `login_usecase_test.mocks.dart`

---

## Ejercicio 2: Generar el Mock Automáticamente

### 📝 Tu Misión

Ejecutar build_runner y verificar que el mock se generó correctamente.

### ✅ Paso 1: Genera el Mock

```bash
dart run build_runner build --delete-conflicting-outputs
```

### ✅ Paso 2: Verifica que se generó

```bash
ls test/features/auth/domain/usecases/
```

**Resultado esperado:**
```
login_usecase_test.dart
login_usecase_test.mocks.dart  ← ¡Generado automáticamente!
```

### ✅ Paso 3: Verifica el contenido generado

El archivo `.mocks.dart` debería contener:

```dart
// Generated file - NO MODIFICAR MANUALMENTE
class MockIAuthRepository extends Mock implements IAuthRepository {}
```

---

## Ejercicio 3: Configurar Respuestas con when()

### 📝 Tu Misión

Aprender a configurar el comportamiento del Mock con `when()` y `thenAnswer()`.

### ✅ Paso 1: Añadir configuración básica

En el mismo archivo de test, añade el setup:

```dart
void main() {
  late LoginUseCase useCase;
  late MockIAuthRepository mockRepository;

  setUp(() {
    // Crear el mock automáticamente generado
    mockRepository = MockIAuthRepository();
    // Inyectar el mock en el UseCase
    useCase = LoginUseCase(repository: mockRepository);
  });

  // Tests irán aquí...
}
```

### ✅ Paso 2: Configurar respuesta de éxito

```dart
// Configurar que cuando se llame a login con CUALQUIER argumento, retorne el usuario
when(mockRepository.login(any, any))
    .thenAnswer((_) async => Either.right(tUser));
```

### ✅ Paso 3: Configurar respuesta de error

```dart
// Configurar que retorne un Failure
when(mockRepository.login(any, any)).thenAnswer(
  (_) async => Either.left(ServerFailure('Invalid credentials')),
);
```

### ✅ Paso 4: Configurar excepción

```dart
// Configurar que lance una excepción
when(mockRepository.login(any, any))
    .thenThrow(Exception('Network error'));
```

### 🤔 ¿Por qué any()?

| Matcher | Uso | Ejemplo |
|---------|-----|---------|
| `any()` | Cualquier valor posicional | `login(any, any)` |
| `anyNamed('param')` | Cualquier valor para argumento nombrado | `updateProduct(id: anyNamed('id'))` |
| `argThat(matcher)` | Valor que cumple condición | `argThat(equals('123'))` |

### 📊 Tabla de thenAnswer vs thenThrow

| Método | Cuándo usarlo | Ejemplo |
|--------|---------------|---------|
| `thenAnswer()` | Retornar un valor (éxito o error) | `thenAnswer((_) => Either.right(user))` |
| `thenThrow()` | Lanzar una excepción | `thenThrow(Exception('error'))` |

---

## Ejercicio 4: Testear un UseCase con el Mock

### 📝 Tu Misión

Crear tests completos para `LoginUseCase` usando el Mock.

### ✅ Paso 1: Crea el archivo de test completo

```dart
// test/features/auth/domain/usecases/login_usecase_test.dart
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/repositories/auth_repository.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/usecases/login_usecase.dart';

@GenerateMocks([IAuthRepository])
import 'login_usecase_test.mocks.dart';

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
      // ═══════════════════════════════════════════════════════════
      // ARRANGE: Configurar el Mock para éxito
      // ═══════════════════════════════════════════════════════════
      when(mockRepository.login(any, any))
          .thenAnswer((_) async => Either.right(tUser));

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
      verify(mockRepository.login(tEmail, tPassword)).called(1);
    });
  });
}
```

### ✅ Paso 2: Añade el test de caso de error

```dart
    test('should return ServerFailure when login fails', () async {
      // ARRANGE: Configurar el Mock para fallar
      when(mockRepository.login(any, any)).thenAnswer(
        (_) async => Either.left(ServerFailure('Invalid credentials')),
      );

      // ACT
      final result = await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ASSERT
      expect(result, equals(Either.left(ServerFailure('Invalid credentials'))));
      verify(mockRepository.login(tEmail, tPassword)).called(1);
    });
```

### ✅ Paso 3: Añade el test de verificación de parámetros

```dart
    test('should pass correct parameters to repository', () async {
      // ARRANGE
      when(mockRepository.login(any, any))
          .thenAnswer((_) async => Either.right(tUser));
      const customEmail = 'custom@example.com';
      const customPassword = 'customPass';

      // ACT
      await useCase(const LoginParams(
        email: customEmail,
        password: customPassword,
      ));

      // ASSERT - Verificar que se llamó con los parámetros exactos
      verify(mockRepository.login(customEmail, customPassword)).called(1);
    });
```

### ✅ Paso 4: Añade el test de llamada única

```dart
    test('should call repository only once', () async {
      // ARRANGE
      when(mockRepository.login(any, any))
          .thenAnswer((_) async => Either.right(tUser));

      // ACT
      await useCase(const LoginParams(email: tEmail, password: tPassword));

      // ASSERT - Verificar exactamente 1 llamada
      verify(mockRepository.login(tEmail, tPassword)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });
```

### ✅ Paso 5: Añade el test de excepción

```dart
    test('should throw exception when repository throws', () async {
      // ARRANGE: Configurar el Mock para lanzar excepción
      when(mockRepository.login(any, any))
          .thenThrow(Exception('Network error'));

      // ACT & ASSERT
      expect(
        () => useCase(const LoginParams(email: tEmail, password: tPassword)),
        throwsException,
      );
    });
```

### ✅ Paso 6: Añade el test con captura de argumentos

```dart
    test('should capture arguments passed to repository', () async {
      // ARRANGE
      when(mockRepository.login(any, any))
          .thenAnswer((_) async => Either.right(tUser));

      // ACT
      await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ASSERT - Capturar los argumentos
      final captured = verify(mockRepository.login(
        captureAny,
        captureAny,
      )).captured;

      expect(captured[0], tEmail);
      expect(captured[1], tPassword);
    });
```

### 🧪 Ejecuta los tests

```bash
flutter test test/features/auth/domain/usecases/login_usecase_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +6: All tests passed!
```

---

## 🎉 ¡Felicitaciones!

Has creado tu primer Mock con Mockito y lo has usado en tests. Ahora entiendes:

- ✅ Configurar `@GenerateMocks` para generar mocks automáticamente
- ✅ Ejecutar `build_runner` para crear los mocks
- ✅ Configurar respuestas con `when()` y `thenAnswer()`
- ✅ Manejar errores y excepciones
- ✅ Verificar llamadas con `verify()`
- ✅ Capturar argumentos con `captureAny`
- ✅ Usar el Mock en tests de UseCase

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Configurar entorno - dependencias y estructura
- [ ] Ejercicio 2: Generar Mock con build_runner
- [ ] Ejercicio 3: Configurar when() + thenAnswer() + thenThrow()
- [ ] Ejercicio 4: Tests de UseCase - 6 tests ejecutándose

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 3: Testing Data](./03-data-testing.md)

**Práctica:** 
- [03a-practica-fixtures-models.md](./03a-practica-fixtures-models.md)
- [03b-practica-datasources.md](./03b-practica-datasources.md)

> En la siguiente práctica aprenderás a testear la capa **Data**: Models, DataSources y Repositories.

---

## 📚 Resumen: API de Mockito

### Stubbing (Configurar comportamiento)

```dart
// Éxito
when(mock.method(any)).thenAnswer((_) async => Either.right(tUser));

// Error
when(mock.method(any)).thenAnswer((_) async => Either.left(Failure()));

// Excepción
when(mock.method(any)).thenThrow(Exception('error'));
```

### Verificación

```dart
verify(mock.method(args)).called(1);      // Exactamente 1 vez
verify(mock.method(args)).called(n);      // n veces
verify(mock.method(args)).called(never); // Nunca
verify(mock.method(args)).called(greaterThan(0)); // Al menos 1

verifyZeroInteractions(mock);             // Ninguna interacción
verifyNoMoreInteractions(mock);           // No más interacciones
```

### Matchers

```dart
any()                    // Cualquier valor
anyNamed('param')        // Cualquier valor para argumento nombrado
argThat(matcher)         // Valor que cumple condición
```

### Captura

```dart
final captured = verify(mock.method(captureAny())).captured;
final value = captured.first;
```
