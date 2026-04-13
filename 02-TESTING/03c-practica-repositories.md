# 🏋️ 03c: Práctica - Repository Implementation

> **¿De qué trata esta práctica?** De testear el Repository que es el "cerebro" de la capa Data - decide cuándo usar datos remotos vs locales. Usaremos **Mockito** para crear los mocks de los DataSources.

---

## 📋 Ejercicios

- [Ejercicio 1: Configurar Mocks con Mockito](#ejercicio-1-configurar-mocks-con-mockito)
- [Ejercicio 2: Testear flujo online exitoso](#ejercicio-2-testear-flujo-online-exitoso)
- [Ejercicio 3: Testear flujo offline](#ejercicio-3-testear-flujo-offline)
- [Ejercicio 4: Testear manejo de errores](#ejercicio-4-testear-manejo-de-errores)

---

## 🎬 Antes de Empezar

Necesitas tener:
1. ✅ Dependencias configuradas (mockito, build_runner)
2. ✅ UserModel
3. ✅ AuthRemoteDataSource
4. ✅ AuthLocalDataSource
5. ✅ NetworkInfo

### Dependencias necesarias

```yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

---

## Ejercicio 1: Configurar Mocks con Mockito

### 📝 Tu Misión

Crear los Mocks necesarios para el Repository usando Mockito.

### ✅ Paso 1: Crea el archivo de test con anotaciones

```bash
mkdir -p test/features/auth/data/repositories
touch test/features/auth/data/repositories/auth_repository_impl_test.dart
```

### ✅ Paso 2: Configura los Mocks

```dart
// test/features/auth/data/repositories/auth_repository_impl_test.dart
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:mi_proyecto_flutter/clean/core/error/exceptions.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/core/network/network_info.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/repositories/auth_repository_impl.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';

/// Generar mocks para: RemoteDataSource, LocalDataSource, NetworkInfo
@GenerateMocks([
  AuthRemoteDataSource,
  AuthLocalDataSource,
  NetworkInfo,
])
import 'auth_repository_impl_test.mocks.dart';

void main() {
  late AuthRepositoryImpl repository;
  late MockAuthRemoteDataSource mockRemoteDataSource;
  late MockAuthLocalDataSource mockLocalDataSource;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockRemoteDataSource = MockAuthRemoteDataSource();
    mockLocalDataSource = MockAuthLocalDataSource();
    mockNetworkInfo = MockNetworkInfo();
    repository = AuthRepositoryImpl(
      remoteDataSource: mockRemoteDataSource,
      localDataSource: mockLocalDataSource,
      networkInfo: mockNetworkInfo,
    );
  });

  // Datos de prueba
  const tEmail = 'test@example.com';
  const tPassword = 'password123';
  const tUserModel = UserModel(
    id: '123',
    email: tEmail,
    name: 'John',
    lastName: 'Doe',
  );
  const tUser = User(
    id: '123',
    email: tEmail,
    name: 'John',
    lastName: 'Doe',
  );

  // Tests van aquí...
}
```

### ✅ Paso 3: Genera los Mocks

```bash
dart run build_runner build --delete-conflicting-outputs
```

### ✅ Paso 4: Verifica que se generaron

```bash
ls test/features/auth/data/repositories/
```

**Resultado esperado:**
```
auth_repository_impl_test.dart
auth_repository_impl_test.mocks.dart  ← ¡Generado!
```

---

## Ejercicio 2: Testear flujo online exitoso

### 📝 Tu Misión

Escribir tests que verifiquen el comportamiento cuando el dispositivo tiene internet.

### ✅ Paso 1: Test - Login exitoso

```dart
  group('login', () {
    test('should return user when device is online and login succeeds', () async {
      // ═══════════════════════════════════════════════════════════
      // ARRANGE: Configurar online + éxito
      // ═══════════════════════════════════════════════════════════
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRemoteDataSource.login(any, any))
          .thenAnswer((_) async => tUserModel);

      // ═══════════════════════════════════════════════════════════
      // ACT: Llamar al repository
      // ═══════════════════════════════════════════════════════════
      final result = await repository.login(tEmail, tPassword);

      // ═══════════════════════════════════════════════════════════
      // ASSERT: Verificar resultado
      // ═══════════════════════════════════════════════════════════
      expect(result, equals(Either.right(tUser)));
    });
  });
```

### ✅ Paso 2: Test - Verificar cache después de login exitoso

```dart
    test('should cache user locally when remote login succeeds', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRemoteDataSource.login(any, any))
          .thenAnswer((_) async => tUserModel);
      when(mockLocalDataSource.cacheUser(any))
          .thenAnswer((_) async => {});

      // Act
      await repository.login(tEmail, tPassword);

      // Assert - Verificar que se guardó en cache
      verify(mockLocalDataSource.cacheUser(tUserModel)).called(1);
    });
```

### ✅ Paso 3: Test - Verificar que se usó la red

```dart
    test('should check network connectivity first', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRemoteDataSource.login(any, any))
          .thenAnswer((_) async => tUserModel);

      // Act
      await repository.login(tEmail, tPassword);

      // Assert - Se consultó la red
      verify(mockNetworkInfo.isConnected).called(1);
    });
```

---

## Ejercicio 3: Testear flujo offline

### 📝 Tu Misión

Escribir tests que verifiquen el comportamiento cuando el dispositivo no tiene internet.

### ✅ Paso 1: Añade grupo offline

```dart
    group('device is offline', () {
      setUp(() {
        when(mockNetworkInfo.isConnected).thenAnswer((_) async => false);
      });

      test('should return NetworkFailure when offline', () async {
        // Act
        final result = await repository.login(tEmail, tPassword);

        // Assert - Debe retornar NetworkFailure
        expect(result.isLeft(), true);
        result.match(
          (failure) => expect(failure, isA<NetworkFailure>()),
          (_) => fail('Should return failure'),
        );
      });

      test('should not call remote when offline', () async {
        // Act
        await repository.login(tEmail, tPassword);

        // Assert - No se llamó al remote
        verifyNever(mockRemoteDataSource.login(any, any));
      });

      test('should not access cache when offline', () async {
        // Act
        await repository.login(tEmail, tPassword);

        // Assert - No se intentó obtener de cache
        verifyNever(mockLocalDataSource.getUser());
      });
    });
```

---

## Ejercicio 4: Testear manejo de errores

### 📝 Tu Misión

Escribir tests que verifiquen cómo el Repository maneja diferentes tipos de errores.

### ✅ Paso 1: Test - Error del servidor

```dart
    group('server error handling', () {
      setUp(() {
        when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      });

      test('should return ServerFailure when remote call fails', () async {
        // Arrange
        when(mockRemoteDataSource.login(any, any)).thenThrow(
          const ServerException(
            message: 'Invalid credentials',
            statusCode: 401,
          ),
        );

        // Act
        final result = await repository.login(tEmail, tPassword);

        // Assert
        expect(result.isLeft(), true);
        result.match(
          (failure) => expect(failure, isA<ServerFailure>()),
          (_) => fail('Should return failure'),
        );
      });

      test('should not cache user when remote call fails', () async {
        // Arrange
        when(mockRemoteDataSource.login(any, any)).thenThrow(
          ServerException(message: 'Error'),
        );

        // Act
        await repository.login(tEmail, tPassword);

        // Assert - No se guardó nada en cache
        verifyNever(mockLocalDataSource.cacheUser(any));
      });
    });
```

### ✅ Paso 2: Test - Verificar parámetros

```dart
      test('should pass correct parameters to remote data source', () async {
        // Arrange
        when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
        when(mockRemoteDataSource.login(any, any))
            .thenAnswer((_) async => tUserModel);
        const customEmail = 'custom@example.com';
        const customPassword = 'customPass';

        // Act
        await repository.login(customEmail, customPassword);

        // Assert - Verificar parámetros exactos
        verify(mockRemoteDataSource.login(customEmail, customPassword)).called(1);
      });
```

### ✅ Paso 3: Test - Register exitoso

```dart
  group('register', () {
    const tName = 'Jane';
    const tLastName = 'Doe';

    test('should return user when registration succeeds', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRemoteDataSource.register(
        email: anyNamed('email'),
        password: anyNamed('password'),
        name: anyNamed('name'),
        lastName: anyNamed('lastName'),
      )).thenAnswer((_) async => tUserModel);

      // Act
      final result = await repository.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      );

      // Assert
      expect(result.isRight(), true);
    });

    test('should cache user after successful registration', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRemoteDataSource.register(
        email: anyNamed('email'),
        password: anyNamed('password'),
        name: anyNamed('name'),
        lastName: anyNamed('lastName'),
      )).thenAnswer((_) async => tUserModel);
      when(mockLocalDataSource.cacheUser(any))
          .thenAnswer((_) async => {});

      // Act
      await repository.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      );

      // Assert
      verify(mockLocalDataSource.cacheUser(tUserModel)).called(1);
    });
  });
```

### ✅ Paso 4: Test - Logout

```dart
  group('logout', () {
    test('should clear local cache on logout', () async {
      // Arrange
      when(mockLocalDataSource.clearUser()).thenAnswer((_) async => {});

      // Act
      await repository.logout();

      // Assert
      verify(mockLocalDataSource.clearUser()).called(1);
    });
  });
```

### ✅ Paso 5: Test - Check Auth Status

```dart
  group('checkAuthStatus', () {
    test('should return user from cache', () async {
      // Arrange
      when(mockLocalDataSource.getUser())
          .thenAnswer((_) async => tUserModel);

      // Act
      final result = await repository.checkAuthStatus();

      // Assert
      expect(result, equals(Either.right(tUser)));
    });

    test('should return null when no user cached', () async {
      // Arrange
      when(mockLocalDataSource.getUser())
          .thenAnswer((_) async => null);

      // Act
      final result = await repository.checkAuthStatus();

      // Assert
      expect(result.isRight(), true);
    });
  });
```

---

## 🧪 Ejecuta todos los tests

```bash
dart run build_runner build --delete-conflicting-outputs
flutter test test/features/auth/data/repositories/auth_repository_impl_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +12: All tests passed!
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Mocks generados con @GenerateMocks
- [ ] Ejercicio 2: Tests flujo online exitoso (3 tests)
- [ ] Ejercicio 3: Tests flujo offline (3 tests)
- [ ] Ejercicio 4: Tests manejo de errores (6 tests)
- [ ] **Total: 12+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Crear Mocks de Remote y Local DataSources con Mockito
- ✅ Crear Mock de NetworkInfo
- ✅ Testear el flujo completo de login (online/offline)
- ✅ Testear el manejo de errores del servidor
- ✅ Testear la coordinación entre DataSources
- ✅ Verificar llamadas con verify() y verifyNever()
- ✅ Testear register, logout y checkAuthStatus

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 4: Testing Presentation](./04-presentation-testing.md)

**Práctica:** 
- [04a-practica-cubits-bloc-test.md](./04a-practica-cubits-bloc-test.md)

> En la siguiente práctica aprenderás a testear **Cubits** usando bloc_test.
