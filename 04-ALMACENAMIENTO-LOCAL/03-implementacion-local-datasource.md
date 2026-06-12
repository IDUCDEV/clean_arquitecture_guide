# 🗄️ 3. Implementación de Local DataSource

> **¿De qué trata esta guía?** De implementar el patrón LocalDataSource con Isar en Clean Architecture, incluyendo el IsarService singleton, las implementaciones concretas para Auth, Profile y PaymentMethod, el CacheManager como registro centralizado de limpieza, y el UserSessionImpl para acceso síncrono al usuario autenticado.

---

## 📋 Índice

1. [IsarService: singleton y ciclo de vida](#1-isarservice-singleton-y-ciclo-de-vida)
2. [Patrón LocalDataSource](#2-patrón-localdatasource)
3. [CacheException: errores de cache](#3-cacheexception-errores-de-cache)
4. [AuthLocalDataSourceImpl](#4-authlocaldatasourceimpl)
5. [ProfileLocalDataSourceImpl](#5-profilelocaldatasourceimpl)
6. [PaymentMethodLocalDataSourceImpl](#6-paymentmethodlocaldatasourceimpl)
7. [CacheManager: limpieza centralizada](#7-cachemanager-limpieza-centralizada)
8. [UserSessionImpl: acceso síncrono al usuario](#8-usersessionimpl-acceso-síncrono-al-usuario)
9. [Integración con Repository](#9-integración-con-repository)
10. [Checklist](#10-checklist)

---

## 1. IsarService: singleton y ciclo de vida

### 🏗️ El patrón

IsarService es un **singleton** que gestiona la conexión a Isar. Se inicializa una vez al arrancar la app y se cierra al cerrar la app.

```dart
// lib/core/data/local/isar_service.dart
import 'package:isar_community/isar.dart';
import 'package:path_provider/path_provider.dart';
import 'isar_models/cached_user.dart';
import 'isar_models/cached_token.dart';
import 'isar_models/cached_profile.dart';
import 'isar_models/cached_payment_method.dart';

class IsarService {
  static Isar? _instance;

  static Isar get instance {
    if (_instance == null) {
      throw Exception(
        'Isar not initialized. Call IsarService.initialize() first.',
      );
    }
    return _instance!;
  }

  static Future<void> initialize() async {
    if (_instance != null) return;

    final dir = await getApplicationDocumentsDirectory();

    _instance = await Isar.open(
      [
        CachedUserSchema,
        CachedTokenSchema,
        CachedProfileSchema,
        CachedPaymentMethodSchema,
      ],
      directory: dir.path,
      name: 'rifame',
    );
  }

  static Future<void> close() async {
    await _instance?.close();
    _instance = null;
  }

  static Future<void> clear() async {
    await _instance?.writeTxn(() async {
      await _instance!.clear();
    });
  }
}
```

### 🔄 Ciclo de vida

```
App start
    │
    ▼
IsarService.initialize()  ← se llama en main() antes de runApp()
    │
    ▼
Los LocalDataSources usan IsarService.instance
    │
    ▼
App close → IsarService.close()
```

### 🧪 En tests

En tests no se usa `IsarService`. Se crea una instancia de Isar directamente con `Directory.systemTemp` y un nombre único. Esto se cubre en detalle en [03e-practica-local-datasource-isar.md](../05-TESTING/03-data/03e-practica-local-datasource-isar.md).

---

## 2. Patrón LocalDataSource

### 📐 Estructura

Cada LocalDataSource sigue el mismo patrón:

```dart
abstract class FeatureLocalDataSource {
  // Escribir en cache
  Future<void> cacheData(...);

  // Leer de cache (retorna null si no hay datos o expiró)
  Future<Model?> getCachedData(...);

  // Limpiar cache
  Future<void> clearCache();
}

class FeatureLocalDataSourceImpl implements FeatureLocalDataSource {
  final Isar _isar;

  FeatureLocalDataSourceImpl(this._isar);

  // ... implementaciones
}
```

### 🎯 Características comunes

1. **Constructor recibe `Isar` directamente** — sin wrapper, sin mock. Isar se inyecta.
2. **Toda escritura va dentro de `writeTxn`** — si falla, se revierte.
3. **Toda operación se envuelve en try/catch** — los errores se convierten a `CacheException`.
4. **Patrón replace-all** — antes de escribir nuevo data, se borra lo anterior del mismo tipo.
5. **Validación TTL** — al leer, si expiró se limpia y retorna null.

---

## 3. CacheException: errores de cache

Los errores de Isar se convierten a `CacheException` para mantener la capa de Data independiente de la implementación concreta:

```dart
// lib/core/error/exceptions.dart
class CacheException implements Exception {
  const CacheException({required this.message});
  final String message;

  @override
  String toString() => message;
}
```

Luego en el Repository, `CacheException` se mapea a `CacheFailure`:

```dart
// lib/core/error/failures.dart
class CacheFailure extends Failure {
  const CacheFailure({super.message = 'Cache failure', super.code});
}
```

### 🔄 Flujo de error completo

```
Isar.writeTxn lanza excepción
    │
    ▼
catch → CacheException(message: 'cache_write_error: $e')
    │
    ▼
Repository catch → CacheFailure(message: 'Cache failure')
    │
    ▼
Cubit/BLoC → state con error message
```

---

## 4. AuthLocalDataSourceImpl

### 📋 Interfaz

```dart
abstract class AuthLocalDataSource {
  Future<void> cacheToken(String token);
  String? getCachedToken();                    // Síncrono
  Future<void> cacheUser(UserModel user);
  Future<UserModel?> getCachedUser();
  bool get hasCachedUser;                      // Getter síncrono
  bool get hasCachedToken;                     // Getter síncrono
  Future<void> clearCache();
}
```

### 🧩 Implementación

```dart
class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  final Isar _isar;

  AuthLocalDataSourceImpl(this._isar);

  @override
  Future<void> cacheToken(String token) async {
    try {
      await _isar.writeTxn(() async {
        // Replace-all: borrar token anterior
        await _isar.cachedTokens.where().deleteAll();

        final cached = CachedToken()
          ..token = token
          ..cachedAt = DateTime.now()
          ..expiresAt = DateTime.now().add(const Duration(days: 30));

        await _isar.cachedTokens.put(cached);
      });
    } catch (e) {
      throw CacheException(message: 'cache_write_error: $e');
    }
  }

  @override
  String? getCachedToken() {
    try {
      final cached = _isar.cachedTokens.where().findFirstSync();
      if (cached == null) return null;

      // Validación TTL
      if (cached.expiresAt != null &&
          cached.expiresAt!.isBefore(DateTime.now())) {
        clearCache();
        return null;
      }

      return cached.token;
    } catch (e) {
      throw CacheException(message: 'cache_read_error: $e');
    }
  }

  @override
  Future<void> cacheUser(UserModel user) async {
    try {
      await _isar.writeTxn(() async {
        await _isar.cachedUsers.where().deleteAll();

        final cached = CachedUser()
          ..userId = user.id
          ..email = user.email
          ..fullName = user.fullName
          ..phone = user.phoneNumber
          ..avatarUrl = user.avatarUrl
          ..createdAt = user.createdAt
          ..emailConfirmedAt = user.emailConfirmedAt
          ..cachedAt = DateTime.now()
          ..expiresAt = DateTime.now().add(const Duration(days: 30));

        await _isar.cachedUsers.put(cached);
      });
    } catch (e) {
      throw CacheException(message: 'cache_write_error: $e');
    }
  }

  @override
  Future<UserModel?> getCachedUser() async {
    try {
      final cached = await _isar.cachedUsers.where().findFirst();
      if (cached == null) return null;

      if (cached.expiresAt != null &&
          cached.expiresAt!.isBefore(DateTime.now())) {
        await clearCache();
        return null;
      }

      return UserModel(
        id: cached.userId ?? '',
        email: cached.email ?? '',
        fullName: cached.fullName,
        phoneNumber: cached.phone,
        avatarUrl: cached.avatarUrl,
        createdAt: cached.createdAt,
        emailConfirmedAt: cached.emailConfirmedAt,
      );
    } catch (e) {
      throw CacheException(message: 'cache_read_error: $e');
    }
  }

  @override
  Future<void> clearCache() async {
    try {
      await _isar.writeTxn(() async {
        await _isar.cachedUsers.where().deleteAll();
        await _isar.cachedTokens.where().deleteAll();
      });
    } catch (e) {
      throw CacheException(message: 'cache_write_error: $e');
    }
  }

  @override
  bool get hasCachedUser {
    try {
      return _isar.cachedUsers.where().countSync() > 0;
    } catch (e) {
      throw CacheException(message: 'cache_read_error: $e');
    }
  }

  @override
  bool get hasCachedToken {
    try {
      return _isar.cachedTokens.where().countSync() > 0;
    } catch (e) {
      throw CacheException(message: 'cache_read_error: $e');
    }
  }
}
```

### 🔑 Puntos clave

| Método | Tipo | Síncrono? | TTL? | Replace-all? |
|--------|------|-----------|------|-------------|
| `cacheToken` | Escritura | Async | — | ✅ Antes de insertar |
| `getCachedToken` | Lectura | **Síncrono** | ✅ Si expiró → limpiar y null |
| `cacheUser` | Escritura | Async | — | ✅ Antes de insertar |
| `getCachedUser` | Lectura | Async | ✅ Si expiró → limpiar y null |
| `hasCachedUser` | Getter | **Síncrono** (countSync) | ❌ No | — |
| `hasCachedToken` | Getter | **Síncrono** (countSync) | ❌ No | — |
| `clearCache` | Escritura | Async | — | Borra ambas colecciones |

> `getCachedToken()` y los getters `hasCachedUser`/`hasCachedToken` son **síncronos** para poder usarlos en contextos donde no se puede usar `await` (ej: `UserSessionImpl.userId`).

---

## 5. ProfileLocalDataSourceImpl

### 📋 Interfaz

```dart
abstract class ProfileLocalDataSource {
  Future<void> cacheProfile(UserProfileModel profile);
  Future<UserProfileModel?> getCachedProfile();
  Future<void> clearCache();
}
```

### 🧩 Implementación

```dart
class ProfileLocalDataSourceImpl implements ProfileLocalDataSource {
  final Isar _isar;

  ProfileLocalDataSourceImpl(this._isar);

  @override
  Future<void> cacheProfile(UserProfileModel profile) async {
    try {
      await _isar.writeTxn(() async {
        // Replace-all: borrar perfil anterior
        await _isar.cachedProfiles.where().deleteAll();

        final cached = CachedProfile()
          ..userId = profile.userId
          ..fullName = profile.fullName
          ..phoneNumber = profile.phoneNumber
          ..email = profile.email
          ..avatarUrl = profile.avatarUrl
          ..preferredLanguage = profile.preferredLanguage
          ..notificationsEnabled = profile.notificationsEnabled
          ..createdAt = profile.createdAt
          ..updatedAt = profile.updatedAt
          ..cachedAt = DateTime.now()
          ..expiresAt = DateTime.now().add(const Duration(days: 30));

        await _isar.cachedProfiles.put(cached);
      });
    } catch (e) {
      throw CacheException(message: 'cache_write_error: $e');
    }
  }

  @override
  Future<UserProfileModel?> getCachedProfile() async {
    try {
      final cached = await _isar.cachedProfiles.where().findFirst();
      if (cached == null) return null;

      if (cached.expiresAt != null &&
          cached.expiresAt!.isBefore(DateTime.now())) {
        await clearCache();
        return null;
      }

      return UserProfileModel(
        id: cached.userId ?? '',
        userId: cached.userId ?? '',
        fullName: cached.fullName,
        phoneNumber: cached.phoneNumber,
        email: cached.email ?? '',
        avatarUrl: cached.avatarUrl,
        preferredLanguage: cached.preferredLanguage,
        notificationsEnabled: cached.notificationsEnabled,
        createdAt: cached.createdAt,
        updatedAt: cached.updatedAt,
      );
    } catch (e) {
      throw CacheException(message: 'cache_read_error: $e');
    }
  }

  @override
  Future<void> clearCache() async {
    try {
      await _isar.writeTxn(() async {
        await _isar.cachedProfiles.where().deleteAll();
      });
    } catch (e) {
      throw CacheException(message: 'cache_write_error: $e');
    }
  }
}
```

---

## 6. PaymentMethodLocalDataSourceImpl

### 🎯 Diferencia clave

A diferencia de Auth y Profile (que tienen una sola entrada por usuario), PaymentMethod tiene **múltiples entradas por usuario**. Por eso:

- Usa `userIdEqualTo(userId).deleteAll()` en lugar de `deleteAll()` simple
- La TTL se valida con `cached.first.expiresAt`
- Convierte la lista de `CachedPaymentMethod` a `PaymentMethodModel` con un mapper

### 📋 Interfaz

```dart
abstract class PaymentMethodLocalDataSource {
  Future<void> cachePaymentMethods(
    String userId,
    List<PaymentMethodModel> methods,
  );
  Future<List<PaymentMethodModel>?> getCachedPaymentMethods(String userId);
  Future<void> clearCache();
}
```

### 🧩 Implementación

```dart
class PaymentMethodLocalDataSourceImpl implements PaymentMethodLocalDataSource {
  final Isar _isar;

  PaymentMethodLocalDataSourceImpl(this._isar);

  @override
  Future<void> cachePaymentMethods(
    String userId,
    List<PaymentMethodModel> methods,
  ) async {
    try {
      await _isar.writeTxn(() async {
        // Borrar solo los métodos de ESTE usuario
        await _isar.cachedPaymentMethods
            .where()
            .userIdEqualTo(userId)
            .deleteAll();

        for (final m in methods) {
          final cached = CachedPaymentMethod()
            ..paymentMethodId = m.id
            ..userId = userId
            ..type = m.type
            ..name = m.name
            ..bankName = m.bankName
            ..accountHolder = m.accountHolder
            ..accountNumber = m.accountNumber
            ..phone = m.phone
            ..email = m.email
            ..walletAddress = m.walletAddress
            ..qrCodeUrl = m.qrCodeUrl
            ..instructions = m.instructions
            ..cedula = m.cedula
            ..bankCode = m.bankCode
            ..blockchainNetwork = m.blockchainNetwork
            ..isActive = m.isActive
            ..isDefault = m.isDefault
            ..createdAt = m.createdAt
            ..updatedAt = m.updatedAt
            ..cachedAt = DateTime.now()
            ..expiresAt = DateTime.now().add(const Duration(days: 30));

          await _isar.cachedPaymentMethods.put(cached);
        }
      });
    } catch (e) {
      throw CacheException(message: 'cache_write_error: $e');
    }
  }

  @override
  Future<List<PaymentMethodModel>?> getCachedPaymentMethods(
    String userId,
  ) async {
    try {
      final cached = await _isar.cachedPaymentMethods
          .where()
          .userIdEqualTo(userId)
          .findAll();

      if (cached.isEmpty) return null;

      if (cached.first.expiresAt != null &&
          cached.first.expiresAt!.isBefore(DateTime.now())) {
        await clearCache();
        return null;
      }

      return cached.map(_toModel).toList();
    } catch (e) {
      throw CacheException(message: 'cache_read_error: $e');
    }
  }

  @override
  Future<void> clearCache() async {
    try {
      await _isar.writeTxn(() async {
        await _isar.cachedPaymentMethods.where().deleteAll();
      });
    } catch (e) {
      throw CacheException(message: 'cache_write_error: $e');
    }
  }

  PaymentMethodModel _toModel(CachedPaymentMethod c) {
    return PaymentMethodModel(
      id: c.paymentMethodId ?? '',
      userId: c.userId ?? '',
      type: c.type ?? '',
      name: c.name ?? '',
      bankName: c.bankName,
      accountHolder: c.accountHolder,
      accountNumber: c.accountNumber,
      phone: c.phone,
      email: c.email,
      walletAddress: c.walletAddress,
      qrCodeUrl: c.qrCodeUrl,
      instructions: c.instructions,
      cedula: c.cedula,
      bankCode: c.bankCode,
      blockchainNetwork: c.blockchainNetwork,
      isActive: c.isActive,
      isDefault: c.isDefault,
      createdAt: c.createdAt,
      updatedAt: c.updatedAt,
    );
  }
}
```

---

## 7. CacheManager: limpieza centralizada

### 🧠 El problema

Cuando el usuario cierra sesión, es necesario limpiar **todas** las caches locales: tokens, usuarios, perfiles, métodos de pago. Si cada feature limpia su propia cache por separado, es fácil olvidar una.

### 💡 La solución: Registry pattern

```dart
// lib/core/services/cache_manager.dart
class CacheManager {
  final List<Future<void> Function()> _clearFns = [];

  void register(Future<void> Function() clearFn) {
    _clearFns.add(clearFn);
  }

  Future<void> clearAll() async {
    await Future.wait(_clearFns.map((fn) => fn()));
  }
}
```

### 🔌 Integración

```dart
// En la inyección de dependencias
final cacheManager = CacheManager();

// Cada feature registra su función de limpieza
cacheManager.register(() => sl<AuthLocalDataSource>().clearCache());
cacheManager.register(() => sl<ProfileLocalDataSource>().clearCache());
cacheManager.register(() => sl<PaymentMethodLocalDataSource>().clearCache());
```

### 🎯 Uso al cerrar sesión

```dart
Future<void> signOut() async {
  await cacheManager.clearAll();  // Limpia TODO de una vez
  await supabase.auth.signOut();
}
```

### Ventajas

| Ventaja | Descripción |
|---------|-------------|
| **Centralizado** | Un solo `clearAll()` limpia todo |
| **Extensible** | Nuevas features solo llaman a `register()` |
| **Independiente** | Cada DataSource expone su `clearCache()` |
| **Paralelo** | `Future.wait` ejecuta todas las limpiezas en paralelo |

---

## 8. UserSessionImpl: acceso síncrono al usuario

### 🧠 El problema

Muchos componentes necesitan saber el ID del usuario autenticado: para filtrar datos, para construir queries, para decidir si mostrar cierta UI. Pedir el token al backend cada vez es ineficiente. Usar `async` en getters simples es incómodo.

### 💡 La solución: leer desde Isar sincrónicamente

```dart
// lib/core/session/user_session.dart
abstract class UserSession {
  String? get userId;
}
```

```dart
// lib/core/session/user_session_impl.dart
import 'package:isar_community/isar.dart';
import 'package:mobile/core/data/local/isar_models/cached_user.dart';
import 'package:mobile/core/session/user_session.dart';

class UserSessionImpl implements UserSession {
  final Isar _isar;

  UserSessionImpl(this._isar);

  @override
  String? get userId {
    final cached = _isar.cachedUsers.where().findFirstSync();
    return cached?.userId;
  }
}
```

### 🔑 ¿Por qué funciona?

- `where().findFirstSync()` es una operación **síncrona** en Isar (no bloquea el thread porque Isar usa isolates internamente)
- `CachedUser` se guarda en Isar al hacer login
- `UserSessionImpl` se inyecta como `UserSession` en toda la app

### 🎯 Uso típico

```dart
class GetCachedProfile {
  final ProfileLocalDataSource localDataSource;
  final UserSession userSession;

  Future<UserProfileModel?> call() async {
    final userId = userSession.userId;
    if (userId == null) return null;
    return localDataSource.getCachedProfile();
  }
}
```

```dart
class ProfileCubit extends Cubit<ProfileState> {
  final UserSession userSession;

  String get _userId => userSession.userId!;  // Síncrono, sin await
  // ...
}
```

---

## 9. Integración con Repository

### 🎯 Cache-first vs Online-first

En Clean Architecture, el Repository decide la estrategia de cache:

```
┌──────────────────────────────────────────────┐
│            Repository Implementation          │
├──────────────────────────────────────────────┤
│                                              │
│   ┌─────────────────┐    ┌────────────────┐  │
│   │ RemoteDataSource │    │ LocalDataSource│  │
│   │ (Supabase)       │    │ (Isar)         │  │
│   └─────────────────┘    └────────────────┘  │
│                                              │
│   Estrategias:                               │
│   ├── Cache-first: Local → Remote → Actualizar│
│   ├── Online-first: Remote → Cache → Retornar │
│   └── Offline: Local-only                     │
└──────────────────────────────────────────────┘
```

### 📝 Ejemplo: Online-first para perfil

```dart
class ProfileRepositoryImpl implements ProfileRepository {
  final ProfileRemoteDataSource remoteDataSource;
  final ProfileLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  @override
  Future<Either<Failure, UserProfileModel>> getProfile() async {
    try {
      if (await networkInfo.isConnected) {
        final remote = await remoteDataSource.getProfile();
        await localDataSource.cacheProfile(remote);
        return Right(remote);
      } else {
        final local = await localDataSource.getCachedProfile();
        if (local != null) return Right(local);
        return Left(NetworkFailure());
      }
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } on CacheException catch (e) {
      return Left(CacheFailure(message: e.message));
    }
  }
}
```

### 📝 Ejemplo: Cache-first para auth

```dart
class AuthRepositoryImpl implements AuthRepository {
  final AuthLocalDataSource localDataSource;

  @override
  bool get isLoggedIn => localDataSource.hasCachedUser;  // Síncrono

  @override
  Future<Either<Failure, UserModel>> getCachedUser() async {
    try {
      final user = await localDataSource.getCachedUser();
      if (user != null) return Right(user);
      return Left(CacheFailure(message: 'No cached user'));
    } on CacheException catch (e) {
      return Left(CacheFailure(message: e.message));
    }
  }
}
```

---

## 10. Checklist

- [ ] `IsarService` implementado como singleton con `initialize()` / `close()`
- [ ] Todos los LocalDataSources reciben `Isar` en el constructor
- [ ] Toda escritura usa `writeTxn`
- [ ] Toda operación envuelta en try/catch → `CacheException`
- [ ] Validación TTL implementada en todas las lecturas
- [ ] `CacheManager` registra la función `clearCache()` de cada feature
- [ ] `UserSessionImpl` implementa `UserSession` con lectura síncrona desde Isar
- [ ] Repository usa `localDataSource.clearCache()` al hacer signOut
- [ ] Los errores `CacheException` se mapean a `CacheFailure` en el Repository

---

**Nivel:** Avanzado  
**Siguiente:** [03e-practica-local-datasource-isar.md](../05-TESTING/03-data/03e-practica-local-datasource-isar.md)
