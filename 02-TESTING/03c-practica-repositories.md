# 🏋️ 03c: Práctica - Repository Implementation

> **¿De qué trata esta práctica?** De testear el Repository que es el "cerebro" de la capa Data - decide cuándo usar datos remotos vs locales.

---

## 📋 Ejercicios

- [Ejercicio 1: Crear Fakes necesarios](#ejercicio-1-crear-fakes-necesarios)
- [Ejercicio 2: Testear flujo online exitoso](#ejercicio-2-testear-flujo-online-exitoso)
- [Ejercicio 3: Testear flujo offline](#ejercicio-3-testear-flujo-offline)
- [Ejercicio 4: Testear manejo de errores](#ejercicio-4-testear-manejo-de-errores)

---

## 🎬 Antes de Empezar

Necesitas tener:
1. ✅ Fixtures JSON (del ejercicio anterior)
2. ✅ UserModel
3. ✅ Remote DataSource
4. ✅ Local DataSource

---

## Ejercicio 1: Crear Fakes necesarios

### 📝 Tu Misión

Crear los Fakes que necesita el Repository para testear.

### ✅ Paso 1: Crea el archivo de Fakes

```bash
touch test/helpers/fake_datasources.dart
```

### ✅ Paso 2: Implementa FakeAuthRemoteDataSource

```dart
// test/helpers/fake_datasources.dart
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_remote_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';

/// Fake Remote DataSource - Simula el servidor
class FakeAuthRemoteDataSource implements AuthRemoteDataSource {
  /// Cuando es true, el método lanzará excepción
  bool shouldThrow = false;
  
  /// Usuario a retornar en caso de éxito
  UserModel? userToReturn;
  
  /// Excepción a lanzar
  Exception? exceptionToThrow;
  
  /// Parámetros recibidos
  String? lastEmail;
  String? lastPassword;

  @override
  Future<UserModel> login(String email, String password) async {
    lastEmail = email;
    lastPassword = password;
    
    if (shouldThrow) {
      throw exceptionToThrow ?? Exception('Login error');
    }
    return userToReturn!;
  }

  @override
  Future<UserModel> register({
    required String email,
    required String password,
    required String name,
    required String lastName,
  }) async {
    if (shouldThrow) {
      throw exceptionToThrow ?? Exception('Register error');
    }
    return userToReturn!;
  }

  @override
  Future<void> logout() async {
    if (shouldThrow) {
      throw exceptionToThrow ?? Exception('Logout error');
    }
  }
}

/// Fake Local DataSource - Simula el cache
class FakeAuthLocalDataSource implements AuthLocalDataSource {
  /// Usuario actualmente en cache
  UserModel? cachedUser;
  
  /// Cuando es true, los métodos lanzarán excepción
  bool shouldThrow = false;
  
  /// Último usuario guardado (para verificación)
  UserModel? lastCachedUser;

  @override
  Future<UserModel?> getUser() async {
    if (shouldThrow) throw Exception('Cache error');
    return cachedUser;
  }

  @override
  Future<void> cacheUser(UserModel user) async {
    if (shouldThrow) throw Exception('Cache error');
    lastCachedUser = user;
    cachedUser = user;
  }

  @override
  Future<void> clearUser() async {
    cachedUser = null;
    lastCachedUser = null;
  }

  @override
  Future<bool> hasUser() async {
    return cachedUser != null;
  }
}
```

### ✅ Paso 3: Crea FakeNetworkInfo

```bash
touch test/helpers/fake_network_info.dart
```

```dart
// test/helpers/fake_network_info.dart
import 'package:mi_proyecto_flutter/clean/core/network/network_info.dart';

/// Fake NetworkInfo - Simula el estado de conexión
class FakeNetworkInfo implements NetworkInfo {
  /// Cuando es true, simula que hay conexión
  bool isOnline = true;

  @override
  Future<bool> get isConnected async => isOnline;
}
```

---

## Ejercicio 2: Testear flujo online exitoso

### 📝 Tu Misión

Escribir tests que verifiquen el comportamiento cuando el dispositivo tiene internet.

### ✅ Paso 1: Crea el archivo de test

```bash
mkdir -p test/features/auth/data/repositories
touch test/features/auth/data/repositories/auth_repository_impl_test.dart
```

### ✅ Paso 2: Configura el test base

```dart
// test/features/auth/data/repositories/auth_repository_impl_test.dart
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/error/exceptions.dart';
import 'package:mi_proyecto_flutter/clean/core/error/failures.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/repositories/auth_repository_impl.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/domain/entities/user.dart';

import '../../../../helpers/fake_datasources.dart';
import '../../../../helpers/fake_network_info.dart';

void main() {
  late AuthRepositoryImpl repository;
  late FakeAuthRemoteDataSource fakeRemote;
  late FakeAuthLocalDataSource fakeLocal;
  late FakeNetworkInfo fakeNetwork;

  setUp(() {
    fakeRemote = FakeAuthRemoteDataSource();
    fakeLocal = FakeAuthLocalDataSource();
    fakeNetwork = FakeNetworkInfo();
    repository = AuthRepositoryImpl(
      remoteDataSource: fakeRemote,
      localDataSource: fakeLocal,
      networkInfo: fakeNetwork,
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

### ✅ Paso 3: Test - Login exitoso

```dart
  group('login', () {
    test('should return user when device is online and login succeeds', () async {
      // ═══════════════════════════════════════════════════════════
      // ARRANGE: Configurar online + éxito
      // ═══════════════════════════════════════════════════════════
      fakeNetwork.isOnline = true;
      fakeRemote.userToReturn = tUserModel;

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

### ✅ Paso 4: Test - Verificar cache después de login exitoso

```dart
    test('should cache user locally when remote login succeeds', () async {
      // Arrange
      fakeNetwork.isOnline = true;
      fakeRemote.userToReturn = tUserModel;

      // Act
      await repository.login(tEmail, tPassword);

      // Assert - Verificar que se guardó en cache
      expect(fakeLocal.lastCachedUser, isNotNull);
      expect(fakeLocal.lastCachedUser?.id, '123');
    });
```

### ✅ Paso 5: Test - Verificar que se usó la red

```dart
    test('should check network connectivity first', () async {
      // Arrange
      fakeNetwork.isOnline = true;
      fakeRemote.userToReturn = tUserModel;

      // Act
      await repository.login(tEmail, tPassword);

      // Assert - La red se consultó (isOnline es true)
      expect(fakeNetwork.isOnline, isTrue);
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
        fakeNetwork.isOnline = false;
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
        expect(fakeRemote.lastEmail, isNull);
      });

      test('should not access cache when offline', () async {
        // Act
        await repository.login(tEmail, tPassword);

        // Assert - No se intentó obtener de cache
        // (el repository debería retornar NetworkFailure directamente)
        expect(fakeLocal.cachedUser, isNull);  // Sin cambios
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
        fakeNetwork.isOnline = true;
      });

      test('should return ServerFailure when remote call fails', () async {
        // Arrange
        fakeRemote.shouldThrow = true;
        fakeRemote.exceptionToThrow = const ServerException(
          message: 'Invalid credentials',
          statusCode: 401,
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
        fakeRemote.shouldThrow = true;

        // Act
        await repository.login(tEmail, tPassword);

        // Assert - No se guardó nada en cache
        expect(fakeLocal.lastCachedUser, isNull);
      });
    });
```

### ✅ Paso 2: Test - Verificar parámetros

```dart
      test('should pass correct parameters to remote data source', () async {
        // Arrange
        fakeNetwork.isOnline = true;
        fakeRemote.userToReturn = tUserModel;
        const customEmail = 'custom@example.com';
        const customPassword = 'customPass';

        // Act
        await repository.login(customEmail, customPassword);

        // Assert
        expect(fakeRemote.lastEmail, customEmail);
        expect(fakeRemote.lastPassword, customPassword);
      });
```

### ✅ Paso 3: Test - Register exitoso

```dart
  group('register', () {
    const tName = 'Jane';
    const tLastName = 'Doe';

    test('should return user when registration succeeds', () async {
      // Arrange
      fakeNetwork.isOnline = true;
      fakeRemote.userToReturn = tUserModel;

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
      fakeNetwork.isOnline = true;
      fakeRemote.userToReturn = tUserModel;

      // Act
      await repository.register(
        email: tEmail,
        password: tPassword,
        name: tName,
        lastName: tLastName,
      );

      // Assert
      expect(fakeLocal.lastCachedUser, isNotNull);
    });
  });
```

### ✅ Paso 4: Test - Logout

```dart
  group('logout', () {
    test('should clear local cache on logout', () async {
      // Arrange
      fakeLocal.cachedUser = tUserModel;

      // Act
      await repository.logout();

      // Assert
      expect(fakeLocal.cachedUser, isNull);
    });
  });
```

### ✅ Paso 5: Test - Check Auth Status

```dart
  group('checkAuthStatus', () {
    test('should return user from cache', () async {
      // Arrange
      fakeLocal.cachedUser = tUserModel;

      // Act
      final result = await repository.checkAuthStatus();

      // Assert
      expect(result, equals(Either.right(tUser)));
    });

    test('should return null when no user cached', () async {
      // Arrange
      fakeLocal.cachedUser = null;

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
flutter test test/features/auth/data/repositories/auth_repository_impl_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +12: All tests passed!
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Fakes de DataSources y NetworkInfo creados
- [ ] Ejercicio 2: Tests flujo online exitoso (3 tests)
- [ ] Ejercicio 3: Tests flujo offline (3 tests)
- [ ] Ejercicio 4: Tests manejo de errores (6 tests)
- [ ] **Total: 12+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Crear Fakes de Remote y Local DataSources
- ✅ Crear Fake de NetworkInfo
- ✅ Testear el flujo completo de login (online/offline)
- ✅ Testear el manejo de errores del servidor
- ✅ Testear la coordinación entre DataSources
- ✅ Testear register, logout y checkAuthStatus

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 4: Testing Presentation](./04-presentation-testing.md)

**Práctica:** 
- [04a-practica-cubits-bloc-test.md](./04a-practica-cubits-bloc-test.md)

> En la siguiente práctica aprenderás a testear **Cubits** usando bloc_test.
