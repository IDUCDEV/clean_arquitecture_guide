# 🧪 Parte 7: Migración a Mockito

## 📋 Índice
1. [¿Cuándo Migrar?](#cuándo-migrar)
2. [Configuración de Mockito](#configuración-de-mockito)
3. [Comparación: Fakes vs Mocks](#comparación-fakes-vs-mocks)
4. [Migración Paso a Paso](#migración-paso-a-paso)
5. [Verificación con verify()](#verificación-con-verify)
6. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## ¿Cuándo Migrar?

### 🎯 Señales de que necesitas migrar:

1. **Proyecto grande** (>50 tests con Fakes)
2. **Múltiples desarrolladores** necesitan consistencia
3. **CI/CD lento** - Fakes requieren mucho mantenimiento
4. **Necesitas verificación estricta** de llamadas
5. **Interfaces cambian frecuentemente**

### 📊 Comparación rápida:

| Característica | Fakes Manuales | Mockito @GenerateMocks |
|----------------|----------------|------------------------|
| **Setup** | Inmediato | Requiere build_runner |
| **Tiempo de escritura** | Alto | Bajo (generado) |
| **Tiempo de ejecución** | Rápido | Rápido |
| **Verificación de llamadas** | Manual (contadores) | Automática (verify) |
| **Mantenimiento** | Alto | Bajo |
| **Curva de aprendizaje** | Baja | Media |
| **Ideal para** | Proyectos pequeños | Proyectos grandes/enterprise |

---

## Configuración de Mockito

### 📦 Instalación

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

### 📝 Configuración de build_runner

**`build.yaml`** (opcional, configuración avanzada):

```yaml
targets:
  $default:
    builders:
      mockito|mockBuilder:
        generate_for:
          - test/**/*_test.dart
```

---

## Comparación: Fakes vs Mocks

### 📁 Ejemplo: Testing de LoginUseCase

#### **VERSIÓN CON FAKES MANUALES** (Tu estilo actual)

```dart
// test/helpers/fake_repositories.dart
class FakeAuthRepository implements IAuthRepository {
  bool shouldFail = false;
  User? userToReturn;
  Failure? failureToReturn;
  int loginCallCount = 0;
  String? lastEmail;
  String? lastPassword;

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    loginCallCount++;
    lastEmail = email;
    lastPassword = password;
    
    if (shouldFail) {
      return Either.left(failureToReturn ?? const ServerFailure('Login failed'));
    }
    return Either.right(userToReturn!);
  }
}

// test/features/auth/domain/usecases/login_usecase_test.dart
void main() {
  late LoginUseCase useCase;
  late FakeAuthRepository fakeRepository;

  setUp(() {
    fakeRepository = FakeAuthRepository();
    useCase = LoginUseCase(repository: fakeRepository);
  });

  test('should return User when login succeeds', () async {
    // ARRANGE
    fakeRepository.userToReturn = tUser;

    // ACT
    final result = await useCase(const LoginParams(
      email: tEmail,
      password: tPassword,
    ));

    // ASSERT
    expect(result, equals(Either.right(tUser)));
    expect(fakeRepository.loginCallCount, 1);
    expect(fakeRepository.lastEmail, tEmail);
  });
}
```

#### **VERSIÓN CON MOCKITO** (Después de migrar)

```dart
// test/features/auth/domain/usecases/login_usecase_test.dart
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

// Genera mocks automáticamente
@GenerateMocks([IAuthRepository])
import 'login_usecase_test.mocks.dart';

void main() {
  late LoginUseCase useCase;
  late MockIAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockIAuthRepository();
    useCase = LoginUseCase(repository: mockRepository);
  });

  test('should return User when login succeeds', () async {
    // ARRANGE
    when(mockRepository.login(any, any))
        .thenAnswer((_) async => Either.right(tUser));

    // ACT
    final result = await useCase(const LoginParams(
      email: tEmail,
      password: tPassword,
    ));

    // ASSERT
    expect(result, equals(Either.right(tUser)));
    verify(mockRepository.login(tEmail, tPassword)).called(1);
    verifyNoMoreInteractions(mockRepository);
  });
}
```

### 🔧 Generar el Mock

```bash
# Generar mocks
flutter pub run build_runner build

# O en modo watch (se regenera automáticamente)
flutter pub run build_runner watch
```

Esto genera: `test/features/auth/domain/usecases/login_usecase_test.mocks.dart`

---

## Migración Paso a Paso

### Paso 1: Actualizar pubspec.yaml

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

### Paso 2: Agregar anotaciones a tests existentes

```dart
import 'package:mockito/annotations.dart';

// Agrega esta anotación arriba del main()
@GenerateMocks([
  IAuthRepository,
  AuthRemoteDataSource,
  AuthLocalDataSource,
  NetworkInfo,
])

void main() {
  // ... tests existentes
}
```

### Paso 3: Reemplazar Fakes por Mocks

**ANTES:**
```dart
setUp(() {
  fakeRepository = FakeAuthRepository();
  useCase = LoginUseCase(repository: fakeRepository);
});
```

**DESPUÉS:**
```dart
setUp(() {
  mockRepository = MockIAuthRepository();
  useCase = LoginUseCase(repository: mockRepository);
});
```

### Paso 4: Reemplazar configuración de Fakes

**ANTES:**
```dart
fakeRepository.userToReturn = tUser;
fakeRepository.shouldFail = true;
```

**DESPUÉS:**
```dart
// Para éxito
when(mockRepository.login(any, any))
    .thenAnswer((_) async => Either.right(tUser));

// Para fallo
when(mockRepository.login(any, any))
    .thenAnswer((_) async => Either.left(ServerFailure('Error')));

// Para excepciones
when(mockRepository.login(any, any))
    .thenThrow(Exception('Network error'));
```

### Paso 5: Reemplazar verificación manual

**ANTES:**
```dart
expect(fakeRepository.loginCallCount, 1);
expect(fakeRepository.lastEmail, tEmail);
```

**DESPUÉS:**
```dart
verify(mockRepository.login(tEmail, tPassword)).called(1);
verifyNoMoreInteractions(mockRepository);
```

---

## Verificación con verify()

### 📚 Métodos de verificación

```dart
// Verificar que se llamó exactamente 1 vez
verify(mockRepository.login(any, any)).called(1);

// Verificar que se llamó exactamente N veces
verify(mockRepository.login(any, any)).called(3);

// Verificar que se llamó al menos 1 vez
verify(mockRepository.login(any, any)).called(greaterThan(0));

// Verificar que nunca se llamó
verifyNever(mockRepository.login(any, any));

// Verificar que no hubo más interacciones
verifyNoMoreInteractions(mockRepository);

// Verificar que no se interactuó en absoluto
verifyZeroInteractions(mockRepository);

// Capturar argumentos pasados
final captured = verify(mockRepository.login(
  captureAny,
  captureAny,
)).captured;

expect(captured[0], tEmail);      // Primer argumento
expect(captured[1], tPassword);   // Segundo argumento
```

### 🎯 Matchers especiales de Mockito

```dart
// Cualquier valor
when(mockRepository.login(any, any))...

// Argumentos específicos
when(mockRepository.login('specific@email.com', any))...

// Matcher compuesto
when(mockRepository.login(
  argThat(contains('@')),
  argThat(hasLength(greaterThan(5))),
))...

// Capturar argumentos
final List<dynamic> captured = verify(
  mockRepository.register(
    email: captureAnyNamed('email'),
    password: captureAnyNamed('password'),
  ),
).captured;
```

---

## Ejemplo Completo Migrado

### 📁 Archivo completo con Mockito

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

// Genera los mocks
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
      // ARRANGE
      when(mockRepository.login(any, any))
          .thenAnswer((_) async => Either.right(tUser));

      // ACT
      final result = await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ASSERT
      expect(result, equals(Either.right(tUser)));
      verify(mockRepository.login(tEmail, tPassword));
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return ServerFailure when login fails', () async {
      // ARRANGE
      when(mockRepository.login(any, any)).thenAnswer(
        (_) async => Either.left(ServerFailure('Invalid credentials')),
      );

      // ACT
      final result = await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ASSERT
      expect(result, isA<Left<Failure, User>>());
      result.match(
        (failure) => expect(failure, isA<ServerFailure>()),
        (_) => fail('Should not return User'),
      );
      verify(mockRepository.login(tEmail, tPassword));
    });

    test('should pass correct parameters to repository', () async {
      // ARRANGE
      when(mockRepository.login(any, any))
          .thenAnswer((_) async => Either.right(tUser));

      // ACT
      await useCase(const LoginParams(
        email: tEmail,
        password: tPassword,
      ));

      // ASSERT
      final captured = verify(mockRepository.login(
        captureAny,
        captureAny,
      )).captured;

      expect(captured[0], tEmail);
      expect(captured[1], tPassword);
    });

    test('should call repository only once', () async {
      // ARRANGE
      when(mockRepository.login(any, any))
          .thenAnswer((_) async => Either.right(tUser));

      // ACT
      await useCase(const LoginParams(email: tEmail, password: tPassword));

      // ASSERT
      verify(mockRepository.login(tEmail, tPassword)).called(1);
    });
  });

  group('LoginParams', () {
    test('should create LoginParams with correct values', () {
      const params = LoginParams(
        email: 'test@test.com',
        password: 'pass123',
      );

      expect(params.email, 'test@test.com');
      expect(params.password, 'pass123');
    });

    test('should be equal when properties are equal', () {
      const params1 = LoginParams(email: 'test@test.com', password: 'pass');
      const params2 = LoginParams(email: 'test@test.com', password: 'pass');

      expect(params1, equals(params2));
    });
  });
}
```

---

## Ejercicios Prácticos

### Ejercicio 1: Migrar Repository Test

Migra el siguiente test de Fakes a Mockito:

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
// DESPUÉS (con Mockito)
@GenerateMocks([
  AuthRemoteDataSource,
  AuthLocalDataSource,
  NetworkInfo,
])

test('should cache user after successful login', () async {
  // ARRANGE
  when(mockNetwork.isConnected).thenAnswer((_) async => true);
  when(mockRemote.login(any, any))
      .thenAnswer((_) async => tUserModel);
  when(mockLocal.cacheUser(any))
      .thenAnswer((_) async => {});

  // ACT
  await repository.login(tEmail, tPassword);

  // ASSERT
  verify(mockLocal.cacheUser(tUserModel)).called(1);
});
```
</details>

### Ejercicio 2: Uso de verify()

Escribe tests que verifiquen:
1. Que se llamó exactamente 2 veces a un método
2. Que nunca se llamó a un método bajo ciertas condiciones
3. Que se pasaron argumentos específicos

### Ejercicio 3: Migración Incremental

Selecciona un archivo de test existente y:
1. Agrega @GenerateMocks
2. Ejecuta build_runner
3. Reemplaza un test de Fake por Mock
4. Verifica que ambos tests pasan

---

## ✅ Checklist de Migración

- [ ] Evaluar si el proyecto necesita migrar (>50 tests?)
- [ ] Configurar mockito y build_runner
- [ ] Agregar @GenerateMocks a tests
- [ ] Ejecutar build_runner para generar mocks
- [ ] Reemplazar Fakes por Mocks gradualmente
- [ ] Usar verify() para verificar interacciones
- [ ] Actualizar documentación
- [ ] Entrenar al equipo en el nuevo enfoque

---

## 🎓 Resumen: Cuándo usar cada enfoque

### **Usa FAKES MANUALES cuando:**
- Proyecto pequeño (<30 tests)
- Necesitas control total del comportamiento
- Quieres entender qué pasa en cada test
- Prefieres código explícito sobre generado

### **Usa MOCKITO cuando:**
- Proyecto grande (>50 tests)
- Múltiples desarrolladores trabajan en testing
- Necesitas verificación estricta de llamadas
- Interfaces cambian frecuentemente
- CI/CD automatizado requiere consistencia

---

## 💡 Tips Adicionales

### 1. **build_runner optimizado**
```bash
# Solo generar mocks necesarios
flutter pub run build_runner build --delete-conflicting-outputs

# Watch mode para desarrollo
flutter pub run build_runner watch --delete-conflicting-outputs
```

### 2. **Excluir archivos generados de git**
```gitignore
# .gitignore
*.mocks.dart
generated_plugin_registrant.dart
```

### 3. **Debug de Mocks**
```dart
// Imprimir todas las interacciones
print(mockRepository.log);

// Verificar estado del mock
print(verify(mockRepository.login(any, any)).callCount);
```

### 4. **Combinar ambos enfoques**
```dart
// Puedes usar ambos en el mismo proyecto!
group('with fakes', () {
  // Tests con Fakes manuales
});

group('with mocks', () {
  // Tests con Mockito
});
```

---

## 🎉 ¡Guía Completada!

Has llegado al final de la guía completa de Testing para Clean Architecture.

### Lo que aprendiste:

1. ✅ **Fundamentos**: Patrón AAA, matchers, estructura
2. ✅ **Domain**: Entities, UseCases, Fakes manuales
3. ✅ **Data**: Models, DataSources, Repositories, Fixtures
4. ✅ **Presentation**: Cubits con bloc_test, Widgets
5. ✅ **Core**: NetworkInfo, Services, Storage, Utils
6. ✅ **Avanzado**: Integration tests, Coverage, CI/CD
7. ✅ **Migración**: Fakes a Mockito cuando sea necesario

### Siguientes pasos:

- 🎯 **Practica**: Escribe tests para tus features
- 📊 **Mide**: Monitorea tu coverage
- 🚀 **Automatiza**: Configura CI/CD
- 📚 **Aprende**: Explora testing de widgets complejos

---

**¡Felicitaciones! Ahora eres capaz de testear cualquier aplicación Flutter con Clean Architecture.** 🎊
