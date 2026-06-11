# 🧪 4. Testing de Local DataSource con Isar

> **¿De qué trata esta guía?** De aprender a testear Local DataSources que usan Isar, con instancias reales de la base de datos en memoria, sin mocks. Cubre setup, patrones, manejo de errores, y ejercicios prácticos basados en `AuthLocalDataSourceImpl`, `ProfileLocalDataSourceImpl` y `PaymentMethodLocalDataSourceImpl`.

---

## 📋 Índice

1. [¿Por qué testear Isar con instancias reales?](#1-por-qué-testear-isar-con-instancias-reales)
2. [Setup del test](#2-setup-del-test)
3. [Patrones de testing](#3-patrones-de-testing)
4. [Error testing](#4-error-testing)
5. [Ejercicio 1: AuthLocalDataSourceImpl](#5-ejercicio-1-authlocaldatasourceimpl)
6. [Ejercicio 2: ProfileLocalDataSourceImpl](#6-ejercicio-2-profilelocaldatasourceimpl)
7. [Ejercicio 3: PaymentMethodLocalDataSourceImpl](#7-ejercicio-3-paymentmethodlocaldatasourceimpl)
8. [Ejercicio 4: CacheManager](#8-ejercicio-4-cachemanager)
9. [Ejercicio 5: UserSessionImpl](#9-ejercicio-5-usersessionimpl)
10. [Checklist](#10-checklist)

---

## 1. ¿Por qué testear Isar con instancias reales?

### 🤔 La decisión: ¿Mock o real?

En la [Parte 3](../02-TESTING/03-data-testing.md) de la guía de testing, los Local DataSources con SharedPreferences se testean con **Mocks de Mocktail**:

```dart
class MockSharedPreferences extends Mock implements SharedPreferences {}

when(() => mockPreferences.setString(any(), any()))
    .thenAnswer((_) async => true);
```

Con Isar, la recomendación es diferente: **usar instancias reales de Isar en lugar de mocks**. ¿Por qué?

| Aspecto | Mock de Isar | Isar real |
|---------|-------------|-----------|
| **Configuración** | Crear Mock de cada método | Isar.open con `Directory.systemTemp` |
| **Velocidad** | Máxima | Muy rápida (no necesita servidor) |
| **Confianza** | Baja — el mock puede no reflejar el comportamiento real | Alta — pruebas con la BD real |
| **Queries** | Hay que mockear cada combinación de where/filter | Funcionan naturalmente |
| **Índices** | No se prueban | Se prueban (unicidad, etc.) |
| **Transacciones** | No se prueban | Se prueban (rollback, atomicidad) |
| **Mantenimiento** | Alto (cambia API → actualizar mocks) | Bajo |

### 🎯 Conclusión

> **Usa Isar real en los tests.** Es rápido, fácil de configurar, y te da confianza real en que tu código funciona con la BD verdadera. No hay ventaja significativa en mockear Isar.

---

## 2. Setup del test

### 📁 Estructura

```
test/features/
├── auth/data/datasources/
│   └── auth_local_data_source_test.dart
├── profile/data/datasources/
│   ├── profile_local_data_source_test.dart
│   └── payment_method_local_data_source_test.dart
```

### 🏗️ Esqueleto base

Todo test de Local DataSource con Isar sigue esta estructura:

```dart
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:isar_community/isar.dart';

void main() {
  late Isar isar;
  late YourLocalDataSourceImpl dataSource;
  var instanceCounter = 0;       // Para nombres únicos de BD

  Future<void> openIsar() async {
    instanceCounter++;
    isar = await Isar.open(
      [RequiredSchema],           // Solo los esquemas necesarios
      directory: Directory.systemTemp.path,
      name: 'test_$instanceCounter',  // Nombre único por instancia
    );
  }

  Future<void> reopenForErrorTest() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);
    }
    await openIsar();
  }

  setUpAll(() async {
    await openIsar();
  });

  setUp(() async {
    if (!isar.isOpen) {
      await openIsar();           // Reabrir si se cerró en un error test
    }
    // Limpiar datos antes de cada test
    await isar.writeTxn(() async {
      await isar.yourCollection.where().deleteAll();
    });
    dataSource = YourLocalDataSourceImpl(isar);
  });

  tearDownAll(() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);  // Limpiar archivo temporal
    }
  });

  // ... tests
}
```

### 🔑 Componentes clave

| Componente | Propósito |
|------------|-----------|
| `instanceCounter` | Evita colisiones entre tests de diferentes archivos |
| `Directory.systemTemp` | Directorio temporal. Se borra al reiniciar el sistema |
| `openIsar()` | Abre una instancia fresca de Isar con esquemas específicos |
| `reopenForErrorTest()` | Cierra y reabre Isar después de un test que lo cerró intencionalmente |
| `setUp` cleanup | Asegura que cada test empieza con datos limpios |
| `deleteFromDisk: true` | Elimina el archivo de BD al cerrar, sin dejar residuos |

### 💡 ¿Por qué `instanceCounter`?

Cada archivo de test puede ejecutarse en paralelo. Si dos tests abren Isar con el mismo `name`, compiten por el mismo archivo. El contador asegura nombres únicos:

```
auth_local_data_source_test.dart → 'auth_test_1', 'auth_test_2', ...
profile_local_data_source_test.dart → 'profile_local_test_1', 'profile_local_test_2', ...
```

---

## 3. Patrones de testing

### 📝 Patrón 1: Seed de datos con `writeTxn`

Para probar lecturas, primero siembras datos en Isar usando `writeTxn`:

```dart
test('should return cached data when available', () async {
  // Arrange: sembrar datos
  await isar.writeTxn(() async {
    await isar.cachedUsers.put(
      CachedUser()
        ..userId = 'test-id'
        ..email = 'test@example.com'
        ..cachedAt = DateTime.now()
        ..expiresAt = DateTime.now().add(const Duration(days: 30)),
    );
  });

  // Act
  final result = await dataSource.getCachedUser();

  // Assert
  expect(result, isNotNull);
  expect(result!.id, 'test-id');
});
```

### 📝 Patrón 2: Assert con `findFirstSync()`

Para verificar que se escribió correctamente, lees directamente de Isar con `findFirstSync()` (síncrono, sin esperar):

```dart
test('should store data in Isar', () async {
  // Act
  await dataSource.cacheUser(tUserModel);

  // Assert: leer directamente de Isar, no del DataSource
  final cached = isar.cachedUsers.where().findFirstSync();
  expect(cached, isNotNull);
  expect(cached!.userId, tUserModel.id);
  expect(cached.email, tUserModel.email);
});
```

### 📝 Patrón 3: TTL (Time-To-Live)

Para probar que el TTL funciona, siembras datos con `expiresAt` en el pasado:

```dart
test('should return null when data is expired', () async {
  // Arrange: sembrar datos expirados
  await isar.writeTxn(() async {
    await isar.cachedTokens.put(
      CachedToken()
        ..token = 'old-token'
        ..cachedAt = DateTime.now()
        ..expiresAt = DateTime.now().subtract(const Duration(days: 1)),
    );
  });

  // Act
  final result = dataSource.getCachedToken();

  // Assert: debe retornar null (expirado)
  expect(result, isNull);
});
```

### 📝 Patrón 4: Estado vacío

```dart
test('should return null when no data exists', () async {
  // Act (no hay datos sembrados)
  final result = await dataSource.getCachedUser();

  // Assert
  expect(result, isNull);
});
```

---

## 4. Error testing

### 🧠 La técnica

Para simular errores de Isar (disco lleno, BD corrupta, etc.), **cierras la instancia de Isar** y luego intentas operar. El DataSource debe envolver el error en `CacheException`.

```dart
test('should throw CacheException on write error', () async {
  // Arrange: cerrar Isar para simular error
  await isar.close();
  dataSource = AuthLocalDataSourceImpl(isar);  // ← Isar cerrado

  // Act & Assert
  await expectLater(
    () => dataSource.cacheToken('token'),
    throwsA(isA<CacheException>()),
  );

  // Limpiar: reabrir Isar para el siguiente test
  await reopenForErrorTest();
});
```

### 🔄 El helper `reopenForErrorTest()`

```dart
Future<void> reopenForErrorTest() async {
  if (isar.isOpen) {
    await isar.close(deleteFromDisk: true);
  }
  await openIsar();  // Crea una nueva instancia
}
```

### ⚠️ Consideraciones importantes

1. **El contador de instancias sigue incrementándose** — cada `openIsar()` usa un nombre único.
2. **La instancia cerrada queda inservible** — por eso se reasigna `dataSource` después de cerrar.
3. **El cleanup de `setUp` reabre si es necesario** — el `if (!isar.isOpen) await openIsar()` protege contra tests que dejan Isar cerrado.

### 📊 Casos de error cubiertos

| Escenario | Cómo se simula | Excepción esperada |
|-----------|----------------|-------------------|
| Error de escritura | Cerrar Isar antes de escribir | `CacheException('cache_write_error: ...')` |
| Error de lectura | Cerrar Isar antes de leer | `CacheException('cache_read_error: ...')` |
| Error en getter síncrono | Cerrar Isar antes del getter | `CacheException('cache_read_error: ...')` |

---

## 5. Ejercicio 1: AuthLocalDataSourceImpl

### 📋 Escenario

Testear el `AuthLocalDataSourceImpl` que maneja `CachedToken` y `CachedUser`. Es el DataSource más completo porque tiene métodos síncronos (`getCachedToken`, `hasCachedUser`, `hasCachedToken`) y asíncronos, además de TTL en las lecturas.

### 🧪 Tests a implementar

| Grupo | Tests |
|-------|-------|
| `cacheToken` | Almacena token en Isar, Lanza CacheException en error de escritura |
| `getCachedToken` | Retorna token cuando está cacheado y no expirado, Retorna null sin token, Retorna null cuando expiró, Lanza CacheException en error de lectura |
| `cacheUser` | Almacena usuario en Isar, Lanza CacheException en error de escritura |
| `getCachedUser` | Retorna UserModel cuando está cacheado, Retorna null sin datos, Retorna null cuando expiró, Lanza CacheException en error de lectura |
| `hasCachedUser` | True cuando existe, False cuando no, Lanza CacheException en error |
| `hasCachedToken` | True cuando existe, False cuando no, Lanza CacheException en error |
| `clearCache` | Limpia todos los datos, Lanza CacheException en error de escritura |

### 💻 Código completo del test

```dart
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:isar_community/isar.dart';
import 'package:mobile/core/data/local/isar_models/cached_token.dart';
import 'package:mobile/core/data/local/isar_models/cached_user.dart';
import 'package:mobile/core/error/exceptions.dart';
import 'package:mobile/features/auth/data/datasources/auth_local_data_source.dart';
import 'package:mobile/features/auth/data/models/user_model.dart';

void main() {
  late Isar isar;
  late AuthLocalDataSourceImpl dataSource;
  var instanceCounter = 0;

  Future<void> openIsar() async {
    instanceCounter++;
    isar = await Isar.open(
      [CachedTokenSchema, CachedUserSchema],
      directory: Directory.systemTemp.path,
      name: 'auth_test_$instanceCounter',
    );
  }

  Future<void> reopenForErrorTest() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);
    }
    await openIsar();
  }

  setUpAll(() async {
    await openIsar();
  });

  setUp(() async {
    if (!isar.isOpen) {
      await openIsar();
    }
    await isar.writeTxn(() async {
      await isar.cachedTokens.where().deleteAll();
      await isar.cachedUsers.where().deleteAll();
    });
    dataSource = AuthLocalDataSourceImpl(isar);
  });

  tearDownAll(() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);
    }
  });

  const tToken = 'jwt_token_abc123';
  const tUserModel = UserModel(
    id: '550e8400-e29b-41d4-a716-446655440000',
    email: 'test@example.com',
    fullName: 'Test User',
    phoneNumber: '+584141234567',
    avatarUrl: 'https://example.com/avatar.jpg',
  );

  group('cacheToken', () {
    test('should store token in Isar', () async {
      await dataSource.cacheToken(tToken);

      final cached = isar.cachedTokens.where().findFirstSync();
      expect(cached, isNotNull);
      expect(cached!.token, tToken);
    });

    test('should throw CacheException on write error', () async {
      await isar.close();
      dataSource = AuthLocalDataSourceImpl(isar);

      await expectLater(
        () => dataSource.cacheToken(tToken),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('getCachedToken', () {
    test('should return token when cached and not expired', () async {
      await isar.writeTxn(() async {
        await isar.cachedTokens.put(
          CachedToken()
            ..token = tToken
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().add(const Duration(days: 30)),
        );
      });

      final result = dataSource.getCachedToken();

      expect(result, tToken);
    });

    test('should return null when no token cached', () async {
      final result = dataSource.getCachedToken();

      expect(result, isNull);
    });

    test('should return null when token is expired', () async {
      await isar.writeTxn(() async {
        await isar.cachedTokens.put(
          CachedToken()
            ..token = tToken
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().subtract(const Duration(days: 1)),
        );
      });

      final result = dataSource.getCachedToken();

      expect(result, isNull);
    });

    test('should throw CacheException on read error', () async {
      await isar.close();
      dataSource = AuthLocalDataSourceImpl(isar);

      expect(
        () => dataSource.getCachedToken(),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('cacheUser', () {
    test('should store user in Isar', () async {
      await dataSource.cacheUser(tUserModel);

      final cached = isar.cachedUsers.where().findFirstSync();
      expect(cached, isNotNull);
      expect(cached!.userId, tUserModel.id);
      expect(cached.email, tUserModel.email);
    });

    test('should throw CacheException on write error', () async {
      await isar.close();
      dataSource = AuthLocalDataSourceImpl(isar);

      await expectLater(
        () => dataSource.cacheUser(tUserModel),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('getCachedUser', () {
    test('should return UserModel when user is cached', () async {
      await isar.writeTxn(() async {
        await isar.cachedUsers.put(
          CachedUser()
            ..userId = tUserModel.id
            ..email = tUserModel.email
            ..fullName = tUserModel.fullName
            ..phone = tUserModel.phoneNumber
            ..avatarUrl = tUserModel.avatarUrl
            ..createdAt = tUserModel.createdAt
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().add(const Duration(days: 30)),
        );
      });

      final result = await dataSource.getCachedUser();

      expect(result, equals(tUserModel));
    });

    test('should return null when no user cached', () async {
      final result = await dataSource.getCachedUser();

      expect(result, isNull);
    });

    test('should return null when user is expired', () async {
      await isar.writeTxn(() async {
        await isar.cachedUsers.put(
          CachedUser()
            ..userId = tUserModel.id
            ..email = tUserModel.email
            ..fullName = tUserModel.fullName
            ..phone = tUserModel.phoneNumber
            ..avatarUrl = tUserModel.avatarUrl
            ..createdAt = tUserModel.createdAt
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().subtract(const Duration(days: 1)),
        );
      });

      final result = await dataSource.getCachedUser();

      expect(result, isNull);
    });

    test('should throw CacheException on read error', () async {
      await isar.close();
      dataSource = AuthLocalDataSourceImpl(isar);

      expect(
        () => dataSource.getCachedUser(),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('hasCachedUser', () {
    test('should return true when user exists in cache', () async {
      await isar.writeTxn(() async {
        await isar.cachedUsers.put(
          CachedUser()
            ..userId = tUserModel.id
            ..expiresAt = DateTime.now().add(const Duration(days: 30)),
        );
      });

      final result = dataSource.hasCachedUser;

      expect(result, true);
    });

    test('should return false when no user exists', () async {
      final result = dataSource.hasCachedUser;

      expect(result, false);
    });

    test('should throw CacheException on read error', () async {
      await isar.close();
      dataSource = AuthLocalDataSourceImpl(isar);

      expect(
        () => dataSource.hasCachedUser,
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('hasCachedToken', () {
    test('should return true when token exists in cache', () async {
      await isar.writeTxn(() async {
        await isar.cachedTokens.put(
          CachedToken()
            ..token = tToken
            ..expiresAt = DateTime.now().add(const Duration(days: 30)),
        );
      });

      final result = dataSource.hasCachedToken;

      expect(result, true);
    });

    test('should return false when no token exists', () async {
      final result = dataSource.hasCachedToken;

      expect(result, false);
    });

    test('should throw CacheException on read error', () async {
      await isar.close();
      dataSource = AuthLocalDataSourceImpl(isar);

      expect(
        () => dataSource.hasCachedToken,
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('clearCache', () {
    test('should clear all cached data', () async {
      await isar.writeTxn(() async {
        await isar.cachedTokens.put(CachedToken()..token = tToken);
        await isar.cachedUsers.put(CachedUser()..userId = tUserModel.id);
      });

      await dataSource.clearCache();

      expect(isar.cachedTokens.where().countSync(), 0);
      expect(isar.cachedUsers.where().countSync(), 0);
    });

    test('should throw CacheException on write error', () async {
      await isar.close();
      dataSource = AuthLocalDataSourceImpl(isar);

      await expectLater(
        () => dataSource.clearCache(),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });
}
```

### 🏃 Ejecución

```bash
flutter test test/features/auth/data/datasources/auth_local_data_source_test.dart
```

---

## 6. Ejercicio 2: ProfileLocalDataSourceImpl

### 📋 Escenario

Testear el `ProfileLocalDataSourceImpl` que maneja `CachedProfile`. Es más simple que Auth (no tiene getters síncronos ni doble colección).

### 🧪 Tests a implementar

| Grupo | Tests |
|-------|-------|
| `cacheProfile` | Almacena perfil en Isar, Lanza CacheException en error de escritura |
| `getCachedProfile` | Retorna perfil cuando está cacheado, Retorna null sin datos, Retorna null cuando expiró, Lanza CacheException en error de lectura |
| `clearCache` | Elimina todos los perfiles, Lanza CacheException en error de escritura |

### 💻 Código del test

```dart
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:isar_community/isar.dart';
import 'package:mobile/core/data/local/isar_models/cached_profile.dart';
import 'package:mobile/core/error/exceptions.dart';
import 'package:mobile/features/profile/data/datasources/profile_local_data_source.dart';
import 'package:mobile/features/profile/data/models/user_profile_model.dart';

void main() {
  late Isar isar;
  late ProfileLocalDataSourceImpl dataSource;
  var instanceCounter = 0;

  final tProfileModel = UserProfileModel(
    id: '550e8400-e29b-41d4-a716-446655440000',
    userId: '550e8400-e29b-41d4-a716-446655440000',
    fullName: 'John Doe',
    phoneNumber: '+584141234567',
    email: 'john.doe@example.com',
    avatarUrl: 'https://example.com/avatar.jpg',
    preferredLanguage: 'es',
    notificationsEnabled: true,
    createdAt: DateTime(2024, 1, 15, 10, 30),
    updatedAt: DateTime(2024, 1, 15, 10, 35),
  );

  Future<void> openIsar() async {
    instanceCounter++;
    isar = await Isar.open(
      [CachedProfileSchema],
      directory: Directory.systemTemp.path,
      name: 'profile_local_test_$instanceCounter',
    );
  }

  Future<void> reopenForErrorTest() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);
    }
    await openIsar();
  }

  setUpAll(() async {
    await openIsar();
  });

  setUp(() async {
    if (!isar.isOpen) {
      await openIsar();
    }
    await isar.writeTxn(() async {
      await isar.cachedProfiles.where().deleteAll();
    });
    dataSource = ProfileLocalDataSourceImpl(isar);
  });

  tearDownAll(() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);
    }
  });

  group('cacheProfile', () {
    test('should store profile in Isar', () async {
      await dataSource.cacheProfile(tProfileModel);

      final cached = isar.cachedProfiles.where().findFirstSync();
      expect(cached, isNotNull);
      expect(cached!.userId, tProfileModel.userId);
      expect(cached.fullName, tProfileModel.fullName);
      expect(cached.email, tProfileModel.email);
    });

    test('should throw CacheException on write error', () async {
      await isar.close();
      dataSource = ProfileLocalDataSourceImpl(isar);

      await expectLater(
        () => dataSource.cacheProfile(tProfileModel),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('getCachedProfile', () {
    test('should return profile when cached', () async {
      await isar.writeTxn(() async {
        await isar.cachedProfiles.put(
          CachedProfile()
            ..userId = tProfileModel.userId
            ..fullName = tProfileModel.fullName
            ..phoneNumber = tProfileModel.phoneNumber
            ..email = tProfileModel.email
            ..avatarUrl = tProfileModel.avatarUrl
            ..preferredLanguage = tProfileModel.preferredLanguage
            ..notificationsEnabled = tProfileModel.notificationsEnabled
            ..createdAt = tProfileModel.createdAt
            ..updatedAt = tProfileModel.updatedAt
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().add(const Duration(days: 30)),
        );
      });

      final result = await dataSource.getCachedProfile();

      expect(result, isNotNull);
      expect(result!.userId, tProfileModel.userId);
      expect(result.fullName, tProfileModel.fullName);
    });

    test('should return null when no profile', () async {
      final result = await dataSource.getCachedProfile();

      expect(result, isNull);
    });

    test('should return null when expired', () async {
      await isar.writeTxn(() async {
        await isar.cachedProfiles.put(
          CachedProfile()
            ..userId = tProfileModel.userId
            ..fullName = tProfileModel.fullName
            ..email = tProfileModel.email
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().subtract(const Duration(days: 1)),
        );
      });

      final result = await dataSource.getCachedProfile();

      expect(result, isNull);
    });

    test('should throw CacheException on read error', () async {
      await isar.close();
      dataSource = ProfileLocalDataSourceImpl(isar);

      expect(
        () => dataSource.getCachedProfile(),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('clearCache', () {
    test('should delete all cached profiles', () async {
      await isar.writeTxn(() async {
        await isar.cachedProfiles.put(
          CachedProfile()
            ..userId = tProfileModel.userId
            ..email = tProfileModel.email,
        );
      });

      await dataSource.clearCache();

      expect(isar.cachedProfiles.where().countSync(), 0);
    });

    test('should throw CacheException on write error', () async {
      await isar.close();
      dataSource = ProfileLocalDataSourceImpl(isar);

      await expectLater(
        () => dataSource.clearCache(),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });
}
```

---

## 7. Ejercicio 3: PaymentMethodLocalDataSourceImpl

### 📋 Escenario

Testear el `PaymentMethodLocalDataSourceImpl` que maneja `CachedPaymentMethod`. Es diferente porque:
- Almacena **listas** de métodos de pago, no un solo objeto
- Usa `userIdEqualTo(userId)` para filtrar por usuario
- Debe probar que los datos de un usuario no afectan a otro

### 🧪 Tests a implementar

| Grupo | Tests |
|-------|-------|
| `cachePaymentMethods` | Almacena métodos en Isar, Reemplaza métodos existentes del mismo usuario, Lanza CacheException en error |
| `getCachedPaymentMethods` | Retorna métodos cuando están cacheados, Retorna null sin datos, Retorna null cuando expiró, Filtra por userId, Lanza CacheException en error |
| `clearCache` | Elimina todos los métodos, Lanza CacheException en error |

### 💻 Código del test

```dart
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:isar_community/isar.dart';
import 'package:mobile/core/data/local/isar_models/cached_payment_method.dart';
import 'package:mobile/core/error/exceptions.dart';
import 'package:mobile/features/profile/data/datasources/payment_method_local_data_source.dart';
import 'package:mobile/features/profile/data/models/payment_method_model.dart';

void main() {
  late Isar isar;
  late PaymentMethodLocalDataSourceImpl dataSource;
  var instanceCounter = 0;

  const tUserId = '550e8400-e29b-41d4-a716-446655440000';
  const tOtherUserId = '660e8400-e29b-41d4-a716-446655440099';

  final tPaymentMethods = [
    PaymentMethodModel(
      id: '660e8400-e29b-41d4-a716-446655440001',
      userId: '550e8400-e29b-41d4-a716-446655440000',
      type: 'mobile',
      name: 'Pago Móvil',
      bankName: 'Banco de Venezuela',
      accountHolder: 'John Doe',
      accountNumber: '0134-0123-45-1234567890',
      phone: '+584141234567',
      cedula: 'V-12345678',
      bankCode: '0102',
      isActive: true,
      isDefault: true,
      createdAt: DateTime(2024, 1, 15, 10, 30),
      updatedAt: DateTime(2024, 1, 15, 10, 35),
    ),
    PaymentMethodModel(
      id: '660e8400-e29b-41d4-a716-446655440002',
      userId: '550e8400-e29b-41d4-a716-446655440000',
      type: 'bank',
      name: 'Transferencia Bancaria',
      bankName: 'Banco Provincial',
      accountHolder: 'John Doe',
      accountNumber: '0108-0456-78-9876543210',
      isActive: true,
      isDefault: false,
      createdAt: DateTime(2024, 1, 16, 14, 0),
      updatedAt: DateTime(2024, 1, 16, 14, 0),
    ),
  ];

  Future<void> openIsar() async {
    instanceCounter++;
    isar = await Isar.open(
      [CachedPaymentMethodSchema],
      directory: Directory.systemTemp.path,
      name: 'pm_local_test_$instanceCounter',
    );
  }

  Future<void> reopenForErrorTest() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);
    }
    await openIsar();
  }

  setUpAll(() async {
    await openIsar();
  });

  setUp(() async {
    if (!isar.isOpen) {
      await openIsar();
    }
    await isar.writeTxn(() async {
      await isar.cachedPaymentMethods.where().deleteAll();
    });
    dataSource = PaymentMethodLocalDataSourceImpl(isar);
  });

  tearDownAll(() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);
    }
  });

  group('cachePaymentMethods', () {
    test('should store methods in Isar', () async {
      await dataSource.cachePaymentMethods(tUserId, tPaymentMethods);

      final cached = await isar.cachedPaymentMethods.where().findAll();
      expect(cached.length, 2);
      expect(cached[0].paymentMethodId, tPaymentMethods[0].id);
      expect(cached[1].paymentMethodId, tPaymentMethods[1].id);
    });

    test('should replace existing methods for same user', () async {
      await dataSource.cachePaymentMethods(tUserId, tPaymentMethods);
      await dataSource.cachePaymentMethods(
        tUserId,
        [tPaymentMethods[0]],
      );

      final cached = await isar.cachedPaymentMethods.where().findAll();
      expect(cached.length, 1);
      expect(cached[0].paymentMethodId, tPaymentMethods[0].id);
    });

    test('should throw CacheException on write error', () async {
      await isar.close();
      dataSource = PaymentMethodLocalDataSourceImpl(isar);

      await expectLater(
        () => dataSource.cachePaymentMethods(tUserId, tPaymentMethods),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('getCachedPaymentMethods', () {
    test('should return methods when cached', () async {
      await _seedPaymentMethods(isar);

      final result = await dataSource.getCachedPaymentMethods(tUserId);

      expect(result, isNotNull);
      expect(result!.length, 2);
      expect(result[0].name, tPaymentMethods[0].name);
    });

    test('should return null when no data', () async {
      final result = await dataSource.getCachedPaymentMethods(tUserId);

      expect(result, isNull);
    });

    test('should return null when expired', () async {
      await isar.writeTxn(() async {
        await isar.cachedPaymentMethods.put(
          CachedPaymentMethod()
            ..paymentMethodId = tPaymentMethods[0].id
            ..userId = tUserId
            ..type = tPaymentMethods[0].type
            ..name = tPaymentMethods[0].name
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().subtract(const Duration(days: 1)),
        );
      });

      final result = await dataSource.getCachedPaymentMethods(tUserId);

      expect(result, isNull);
    });

    test('should filter by userId', () async {
      await _seedPaymentMethods(isar);

      final result = await dataSource.getCachedPaymentMethods(tOtherUserId);

      expect(result, isNull);
    });

    test('should throw CacheException on read error', () async {
      await isar.close();
      dataSource = PaymentMethodLocalDataSourceImpl(isar);

      expect(
        () => dataSource.getCachedPaymentMethods(tUserId),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });

  group('clearCache', () {
    test('should delete all cached payment methods', () async {
      await _seedPaymentMethods(isar);

      await dataSource.clearCache();

      expect(
        isar.cachedPaymentMethods.where().countSync(),
        0,
      );
    });

    test('should throw CacheException on write error', () async {
      await isar.close();
      dataSource = PaymentMethodLocalDataSourceImpl(isar);

      await expectLater(
        () => dataSource.clearCache(),
        throwsA(isA<CacheException>()),
      );

      await reopenForErrorTest();
    });
  });
}

Future<void> _seedPaymentMethods(Isar isar) async {
  await isar.writeTxn(() async {
    await isar.cachedPaymentMethods.put(
      CachedPaymentMethod()
        ..paymentMethodId = '660e8400-e29b-41d4-a716-446655440001'
        ..userId = '550e8400-e29b-41d4-a716-446655440000'
        ..type = 'mobile'
        ..name = 'Pago Móvil'
        ..cachedAt = DateTime.now()
        ..expiresAt = DateTime.now().add(const Duration(days: 30)),
    );
    await isar.cachedPaymentMethods.put(
      CachedPaymentMethod()
        ..paymentMethodId = '660e8400-e29b-41d4-a716-446655440002'
        ..userId = '550e8400-e29b-41d4-a716-446655440000'
        ..type = 'bank'
        ..name = 'Transferencia Bancaria'
        ..cachedAt = DateTime.now()
        ..expiresAt = DateTime.now().add(const Duration(days: 30)),
    );
  });
}
```

---

## 8. Ejercicio 4: CacheManager

### 📋 Escenario

Testear el `CacheManager` que gestiona la limpieza centralizada de todas las caches.

### 💡 Estrategia

Como `CacheManager` es un registro de funciones, lo testeas registrando funciones espía (que registren si fueron llamadas):

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/core/services/cache_manager.dart';

void main() {
  late CacheManager cacheManager;

  setUp(() {
    cacheManager = CacheManager();
  });

  group('register', () {
    test('should execute registered function on clearAll', () async {
      var called = false;
      cacheManager.register(() async {
        called = true;
      });

      await cacheManager.clearAll();

      expect(called, true);
    });

    test('should execute multiple registered functions', () async {
      var callCount = 0;
      cacheManager.register(() async {
        callCount++;
      });
      cacheManager.register(() async {
        callCount++;
      });

      await cacheManager.clearAll();

      expect(callCount, 2);
    });

    test('should handle functions that throw', () async {
      cacheManager.register(() async {
        throw Exception('Cache error');
      });

      // clearAll debe propagar la excepción
      await expectLater(
        () => cacheManager.clearAll(),
        throwsA(isA<Exception>()),
      );
    });
  });
}
```

---

## 9. Ejercicio 5: UserSessionImpl

### 📋 Escenario

Testear el `UserSessionImpl` que lee el userId desde Isar sincrónicamente.

### 💻 Código del test

```dart
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:isar_community/isar.dart';
import 'package:mobile/core/data/local/isar_models/cached_user.dart';
import 'package:mobile/core/session/user_session_impl.dart';

void main() {
  late Isar isar;
  late UserSessionImpl userSession;
  var instanceCounter = 0;

  Future<void> openIsar() async {
    instanceCounter++;
    isar = await Isar.open(
      [CachedUserSchema],
      directory: Directory.systemTemp.path,
      name: 'session_test_$instanceCounter',
    );
  }

  setUp(() async {
    await openIsar();
    userSession = UserSessionImpl(isar);
  });

  tearDown(() async {
    if (isar.isOpen) {
      await isar.close(deleteFromDisk: true);
    }
  });

  group('userId', () {
    test('should return userId when user is cached', () async {
      await isar.writeTxn(() async {
        await isar.cachedUsers.put(
          CachedUser()
            ..userId = 'test-user-id'
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().add(const Duration(days: 30)),
        );
      });

      final result = userSession.userId;

      expect(result, 'test-user-id');
    });

    test('should return null when no user is cached', () async {
      final result = userSession.userId;

      expect(result, isNull);
    });

    test('should be synchronous (not return a Future)', () {
      // Si esto compila, es síncrono
      final result = userSession.userId;
      expect(result, isA<String?>());
    });
  });
}
```

### 🔑 Punto clave

El último test (`should be synchronous`) no es un test funcional sino estructural: verifica que `userId` no es un `Future`. Si la firma cambiara a `Future<String?>`, este test no compilaría (porque `expect` espera `String?` no `Future<String?>`).

---

## 10. Checklist

### Para cada LocalDataSource test

- [ ] Setup con `Isar.open` + `Directory.systemTemp`
- [ ] `instanceCounter` para nombres únicos de BD
- [ ] `setUp`: limpiar datos antes de cada test
- [ ] `tearDownAll`: cerrar Isar con `deleteFromDisk: true`
- [ ] `reopenForErrorTest()` helper para tests de error
- [ ] Tests de escritura: verificar con `findFirstSync()`
- [ ] Tests de lectura: seed con `writeTxn`
- [ ] Tests de TTL: seed con `expiresAt` en pasado
- [ ] Tests de error: cerrar Isar y esperar `CacheException`
- [ ] Tests para todos los estados: datos, vacío, error

### Para CacheManager

- [ ] Registrar funciones espía
- [ ] Verificar que se ejecutan en `clearAll()`
- [ ] Probar múltiples registros

### Para UserSessionImpl

- [ ] Probar con usuario en cache
- [ ] Probar sin usuario en cache
- [ ] Verificar que es síncrono

---

**Nivel:** Avanzado  
**Tiempo estimado:** 3-4 horas  
**Anterior:** [03-implementacion-local-datasource.md](./03-implementacion-local-datasource.md)
