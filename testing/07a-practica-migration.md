# 🏋️ 07a: Práctica - Migración a Mockito

> **¿De qué trata esta práctica?** De aprender a migrar de Fakes manuales a Mocks automáticos cuando sea necesario.

---

## 📋 Ejercicios

- [Ejercicio 1: Identificar cuándo migrar](#ejercicio-1-identificar-cuándo-migrar)
- [Ejercicio 2: Generar Mocks con Mockito](#ejercicio-2-generar-mocks-con-mockito)
- [Ejercicio 3: Comparar Fakes vs Mocks](#ejercicio-3-comparar-fakes-vs-mocks)

---

## 🎬 Antes de Empezar

Asegúrate de tener las dependencias:

```yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.10.2

flutter pub get
```

---

## Ejercicio 1: Identificar cuándo migrar

### 📝 Tu Misión

Aprender a reconocer cuándo tiene sentido usar Mocks en lugar de Fakes.

### ✅ Cuándo usar Fakes

| Escenario | Ejemplo | ¿Fake o Mock? |
|----------|---------|---------------|
| Interfaz simple | `IAuthRepository` con 2-3 métodos | ✅ **Fake** |
| Lógica de negocio en el fake | Cache con verificación | ✅ **Fake** |
| Dependencias muy estables | Interfaces que raramente cambian | ✅ **Fake** |
| Equipo junior | Facilidad de debugging | ✅ **Fake** |

### ✅ Cuándo usar Mocks

| Escenario | Ejemplo | ¿Fake o Mock? |
|----------|---------|---------------|
| Muchas dependencias | Repository con 10+ métodos | ✅ **Mock** |
| Interfaces de terceros | Paquetes externos | ✅ **Mock** |
| Verificación precisa | Verificar argumentos exactos | ✅ **Mock** |
| Tests rápidos de escritura | Mucho boilerplate | ✅ **Mock** |

### ✅ Ejemplo de decisión

```dart
// ✅ FAKE - Interfaz simple y estable
abstract class IAuthRepository {
  Future<User> login(String email, String password);
  Future<void> logout();
}
// → Un Fake es suficiente

// ✅ MOCK - Interfaz compleja de tercero
abstract class IPaymentGateway {
  Future<PaymentResult> charge(ChargeRequest request);
  Future<RefundResult> refund(String transactionId);
  Future<bool> verifyStatus(String transactionId);
  Future<List<Transaction>> getTransactions(DateTime from, DateTime to);
  // ... 10+ métodos
}
// → Un Mock puede ser más práctico
```

---

## Ejercicio 2: Generar Mocks con Mockito

### 📝 Tu Misión

Crear un Mock usando las anotaciones de Mockito.

### ✅ Paso 1: Crear archivo con anotaciones

Crea `test/helpers/mock_auth_repository.dart`:

```dart
// test/helpers/mock_auth_repository.dart
import 'package:mockito/annotations.dart';
import 'package:sereni/clean/features/auth/domain/repositories/auth_repository.dart';

@GenerateMocks([IAuthRepository])
void main() {
  // Generate with: dart run build_runner build
}
```

### ✅ Paso 2: Generar el Mock

```bash
dart run build_runner build --delete-conflicting-outputs
```

### ✅ Paso 3: Usar el Mock en tests

```dart
// test/features/auth/domain/usecases/login_usecase_mock_test.dart
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:dartz/dartz.dart';
import 'package:sereni/clean/core/error/failures.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';
import 'package:sereni/clean/features/auth/domain/usecases/login_usecase.dart';
import 'package:sereni/clean/features/auth/domain/repositories/auth_repository.dart';

import 'login_usecase_mock_test.mocks.dart';

@GenerateMocks([IAuthRepository])
void main() {
  late LoginUseCase useCase;
  late MockIAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockIAuthRepository();
    useCase = LoginUseCase(repository: mockRepository);
  });

  test('should return user when login is successful', () async {
    // Arrange
    const tUser = User(id: '123', email: 'test@example.com', name: 'John', lastName: 'Doe');
    when(mockRepository.login(any, any)).thenAnswer((_) async => const Right(tUser));

    // Act
    final result = await useCase(const LoginParams(email: 'test@example.com', password: 'password'));

    // Assert
    expect(result, equals(const Right(tUser)));
    verify(mockRepository.login('test@example.com', 'password'));
  });

  test('should return failure when login fails', () async {
    // Arrange
    when(mockRepository.login(any, any)).thenAnswer(
      (_) async => const Left(ServerFailure('Invalid credentials')),
    );

    // Act
    final result = await useCase(const LoginParams(email: 'test@example.com', password: 'wrong'));

    // Assert
    expect(result.isLeft(), true);
    verify(mockRepository.login('test@example.com', 'wrong'));
  });
}
```

---

## Ejercicio 3: Comparar Fakes vs Mocks

### 📝 Tu Misión

Entender las diferencias prácticas entre ambos enfoques.

### ✅ Ejemplo comparativo

**Con Fake:**
```dart
// test/helpers/fake_auth_repository.dart
class FakeAuthRepository implements IAuthRepository {
  bool shouldFail = false;
  User? userToReturn;
  
  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    if (shouldFail) return Left(ServerFailure('Error'));
    return Right(userToReturn!);
  }
}

// Uso en test
fake.userToReturn = tUser;
await useCase(...);
expect(fake.loginCallCount, 1);  // ✓ Verificación manual
```

**Con Mock:**
```dart
// test/helpers/mock_auth_repository.dart (generado)
class MockIAuthRepository extends Mock implements IAuthRepository {}

// Uso en test
when(mock.login(any, any)).thenAnswer((_) async => Right(tUser));
await useCase(...);
verify(mock.login('test@example.com', 'password')).called(1);  // ✓ Verificación automática
```

### ✅ Comparación directa

| Aspecto | Fake | Mock |
|---------|------|------|
| **Código a escribir** | Más (implementar todo) | Menos (anotaciones) |
| **Debugging** | Fácil (código visible) | Difícil (código generado) |
| **Verificación** | Manual (`callCount`) | Automática (`verify`) |
| **Flexibilidad** | Alta (lógica personalizada) | Limitada (API de mockito) |
| **Mantenimiento** | Actualizar manualmente | Regenerar con build_runner |

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Entiendo cuándo usar Fakes vs Mocks
- [ ] Ejercicio 2: He generado un Mock con Mockito
- [ ] Ejercicio 3: He comparado ambos enfoques

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Identificar cuándo migrar de Fakes a Mocks
- ✅ Generar Mocks automáticamente con Mockito
- ✅ Comparar ambos enfoques y elegir el correcto

---

## 🚀 ¡Fin de la Guía!

Has completado todos los ejercicios de la guía de testing. Ahora eres capaz de:

✅ Escribir tests con patrón AAA  
✅ Crear Fakes manuales para cualquier interfaz  
✅ Testear Entities, UseCases, Models  
✅ Testear DataSources (Remote y Local)  
✅ Testear Repositories (lógica online/offline)  
✅ Testear Cubits con bloc_test  
✅ Testear Widgets con interacciones  
✅ Medir coverage y configurar CI/CD  
✅ Decidir cuándo usar Fakes o Mocks  

---

## 📚 Resumen de la Guía

| Parte | Archivos |
|-------|----------|
| Fundamentos | 01-fundamentos.md + 01a-practica-primeros-tests.md |
| Domain | 02-domain-testing.md + 02a-practica-fakes-manuales.md |
| Data | 03-data-testing.md + 03a-practica-fixtures.md + 03b-practica-datasources.md + 03c-practica-repositories.md |
| Presentation | 04-presentation-testing.md + 04a-practica-cubits.md + 04b-practica-widgets.md |
| Core | 05-core-testing.md + 05a-practica-core-services.md |
| Avanzado | 06-advanced-testing.md + 06a-practica-coverage-ci.md |
| Migración | 07-migration-to-mockito.md + 07a-practica-migration.md |

---

**¡Sigue practicando y buena suerte con tus tests! 🚀**
