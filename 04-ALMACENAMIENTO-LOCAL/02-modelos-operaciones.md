# 🗄️ 2. Modelos y Operaciones con Isar

> **¿De qué trata esta guía?** De aprender a definir colecciones Isar con anotaciones, realizar operaciones CRUD dentro de transacciones, construir queries con filtros y ordenamiento, e implementar el patrón TTL (Time-To-Live) para cache expiration.

---

## 📋 Índice

1. [Definición de colecciones](#1-definición-de-colecciones)
2. [Anotaciones principales](#2-anotaciones-principales)
3. [CRUD básico](#3-crud-básico)
4. [Transacciones (writeTxn)](#4-transacciones-writetxn)
5. [Queries con where()](#5-queries-con-where)
6. [Filtros avanzados con filter()](#6-filtros-avanzados-con-filter)
7. [Ordenamiento, offset y límite](#7-ordenamiento-offset-y-límite)
8. [Patrón TTL (Time-To-Live)](#8-patrón-ttl-time-to-live)
9. [Casos reales del monorepo](#9-casos-reales-del-monorepo)
10. [Checklist](#10-checklist)

---

## 1. Definición de colecciones

Toda colección Isar es una clase Dart anotada con `@Collection()`. Cada instancia de la clase es un "documento" en la colección.

### 📁 Estructura de archivos

```
lib/core/data/local/isar_models/
├── cached_user.dart
├── cached_user.g.dart
├── cached_token.dart
├── cached_token.g.dart
├── cached_profile.dart
├── cached_profile.g.dart
├── cached_payment_method.dart
└── cached_payment_method.g.dart    ← generado
```

### 🧱 Reglas fundamentales

1. Toda colección debe tener un campo `Id id` (puede ser autoincremental o asignado)
2. Los tipos soportados son: `bool`, `int`, `double`, `String`, `DateTime`, `Uint8List`, `List<String>`, objetos anidados con `@embedded`
3. Todos los campos deben ser nullable (`String?`, `DateTime?`) a menos que tengan valor por defecto
4. Se requiere `part 'nombre.g.dart';` al inicio del archivo

---

## 2. Anotaciones principales

### `@Collection()`

Marca una clase como colección Isar. Opcionalmente puede especificar `inheritance: true/false` para incluir campos de superclases.

### `@Index()`

Crea un índice en el campo para acelerar queries. Opciones:

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `unique: true` | Valores únicos (como PRIMARY KEY) | `@Index(unique: true)` |
| `type: IndexType.hash` | Índice hash (solo igualdad, más rápido) | `@Index(type: IndexType.hash)` |
| `composite: [...]` | Índice compuesto (varios campos) | `@Index(composite: ['campo1', 'campo2'])` |

### `@enumerated`

Almacena un enum como su índice entero (0, 1, 2...) en lugar de string.

### `@embedded`

Marca una clase como objeto embebido (se almacena dentro del documento padre, no como colección separada).

### `Id`

Tipo especial para la clave primaria. `Isar.autoIncrement` asigna automáticamente.

### 💡 Regla de oro para `@Index`

Usar `@Index(unique: true)` en el **business key** (el ID del negocio, no el `Id` interno). Esto permite:
- Buscar por `userId`, `token`, `paymentMethodId` de forma eficiente
- Evitar duplicados a nivel de BD
- Hacer `upsert` implícito con `put()` (si el índice único ya existe, se actualiza)

---

## 3. CRUD básico

### ✍️ Crear / Actualizar (`put`)

```dart
// put inserta si no existe, actualiza si ya existe (por Id o índice único)
await isar.writeTxn(() async {
  final cached = CachedUser()
    ..userId = '550e8400-e29b-41d4-a716-446655440000'
    ..email = 'test@example.com'
    ..fullName = 'Test User'
    ..cachedAt = DateTime.now()
    ..expiresAt = DateTime.now().add(const Duration(days: 30));

  await isar.cachedUsers.put(cached);
});
```

### 📖 Leer (`get`, `findFirst`, `findAll`)

```dart
// Por Id interno
final user = await isar.cachedUsers.get(1);

// Primer resultado de la colección
final first = await isar.cachedUsers.where().findFirst();

// Todos los documentos
final all = await isar.cachedUsers.where().findAll();

// Síncrono (solo para where().findFirstSync/ findAllSync)
final syncResult = isar.cachedUsers.where().findFirstSync();
```

### 🗑️ Eliminar (`delete`, `deleteAll`)

```dart
await isar.writeTxn(() async {
  // Por Id interno
  await isar.cachedUsers.delete(1);

  // Todos los documentos
  await isar.cachedUsers.where().deleteAll();

  // Por condición
  await isar.cachedUsers.where().userIdEqualTo(userId).deleteAll();
});
```

---

## 4. Transacciones (`writeTxn`)

### 🤔 ¿Por qué son necesarias?

Toda operación de escritura (`put`, `delete`, `clear`) **debe** ejecutarse dentro de una transacción. Las lecturas no requieren transacción.

### 📝 Patrón básico

```dart
await isar.writeTxn(() async {
  await isar.cachedTokens.where().deleteAll();
  await isar.cachedTokens.put(newToken);
  // Si algo falla aquí, todo se revierte automáticamente
});
```

### 🎯 Ventajas

| Ventaja | Descripción |
|---------|-------------|
| **Atomicidad** | Si algo falla, todo se revierte |
| **Aislamiento** | Las lecturas no ven cambios a medio escribir |
| **Rendimiento** | Múltiples operaciones en una sola transacción son más rápidas |

### ⚠️ Error común

```dart
// ❌ Error: put fuera de writeTxn
await isar.cachedUsers.put(user);  // Lanza IsarError

// ✅ Correcto
await isar.writeTxn(() async {
  await isar.cachedUsers.put(user);
});
```

---

## 5. Queries con `where()`

El método `where()` inicia una query construida con los índices disponibles. Es la forma más rápida de consultar.

### 🔍 Operadores por tipo de índice

| Operador | Descripción | Ejemplo |
|----------|-------------|---------|
| `userIdEqualTo(value)` | Igualdad exacta | `isar.cachedUsers.where().userIdEqualTo(id)` |
| `userIdIsNull()` | Es null | `isar.cachedUsers.where().userIdIsNull()` |
| `tokenStartsWith('jwt_')` | Empieza con | — |
| `tokenContains('abc')` | Contiene | — |
| `cachedAtBetween(a, b)` | Rango de fechas | — |
| `cachedAtGreaterThan(date)` | Mayor que | — |
| `cachedAtLessThan(date)` | Menor que | — |

### 🏃‍♂️ Ejemplo real: PaymentMethod por userId

```dart
// Buscar métodos de pago de un usuario específico
final methods = await isar.cachedPaymentMethods
    .where()
    .userIdEqualTo('550e8400-e29b-41d4-a716-446655440000')
    .findAll();

// Conteo síncrono (no requiere await)
final count = isar.cachedPaymentMethods
    .where()
    .userIdEqualTo('550e8400-e29b-41d4-a716-446655440000')
    .countSync();
```

### ⚡ Síncrono vs Asíncrono

Isar ofrece versiones síncronas de algunas operaciones de lectura. Son útiles para getters que deben ser síncronos:

```dart
// Asíncrono (retorna Future)
final user = await isar.cachedUsers.where().findFirst();

// Síncrono (retorna directamente)
final user = isar.cachedUsers.where().findFirstSync();
final count = isar.cachedUsers.where().countSync();
```

> **¿Cuándo usar síncrono?** En getters síncronos como `hasCachedUser` o `userId` de `UserSessionImpl`, donde no quieres cambiar la firma del método a async.

---

## 6. Filtros avanzados con `filter()`

Mientras `where()` usa índices, `filter()` permite filtrar por cualquier campo, aunque no tenga índice. Es más lento pero más flexible.

```dart
// Combinar where + filter
final result = await isar.cachedPaymentMethods
    .where()                                    // Usa índice de userId
    .userIdEqualTo(userId)
    .filter()                                   // Filtro adicional
    .isActiveEqualTo(true)
    .sortByType()                               // Ordenar
    .findAll();
```

### Operadores de filter

| Categoría | Operadores |
|-----------|------------|
| **Igualdad** | `equalTo()`, `notEqualTo()` |
| **Texto** | `contains()`, `startsWith()`, `endsWith()` |
| **Nulos** | `isNull()`, `isNotNull()` |
| **Booleanos** | `isTrue()`, `isFalse()` |
| **Rangos** | `between()`, `greaterThan()`, `lessThan()` |
| **Grupos** | `and()`, `or()` |

---

## 7. Ordenamiento, offset y límite

```dart
final result = await isar.cachedPaymentMethods
    .where()
    .userIdEqualTo(userId)
    .sortByCreatedAt()        // Ascendente por defecto
    .thenByType()             // Segundo criterio
    .findAll();

// Descendente
final recent = await isar.cachedPaymentMethods
    .where()
    .sortByCreatedAtDesc()    // Más reciente primero
    .limit(10)
    .findAll();

// Paginación
final page = await isar.cachedPaymentMethods
    .where()
    .offset(20)
    .limit(10)
    .findAll();
```

---

## 8. Patrón TTL (Time-To-Live)

### 🧠 El problema

Cuando guardas datos localmente, no quieres que sean eternos. El perfil del usuario puede cambiar, los tokens pueden expirar, etc. Necesitas una forma de invalidar la cache automáticamente.

### 📐 La solución

Cada colección incluye dos campos:

```dart
DateTime? cachedAt;    // Cuándo se guardó
DateTime? expiresAt;   // Cuándo expira
```

### ⏰ Validación al leer

```dart
Future<UserModel?> getCachedUser() async {
  try {
    final cached = await isar.cachedUsers.where().findFirst();
    if (cached == null) return null;

    // ❌ Si expiró, limpiar y retornar null
    if (cached.expiresAt != null &&
        cached.expiresAt!.isBefore(DateTime.now())) {
      await clearCache();
      return null;
    }

    // ✅ Válido, convertir a modelo
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
```

### 📊 Estrategias de TTL

| Estrategia | Cuándo usarla | Tiempo típico |
|------------|---------------|---------------|
| **30 días** | Datos de perfil que rara vez cambian | `Duration(days: 30)` |
| **7 días** | Datos semi-estáticos (métodos de pago) | `Duration(days: 7)` |
| **1 día** | Datos que cambian a menudo | `Duration(hours: 24)` |
| **Token session** | Mientras el JWT sea válido | Matchear con `exp` del JWT |

### 💡 Ventajas del TTL sobre "siempre fresco"

1. **Sin llamadas innecesarias** a la API si los datos están en cache y son válidos
2. **Offline-first parcial** — el usuario ve datos aunque no tenga internet (mientras no hayan expirado)
3. **Auto-limpieza** — no acumulas datos obsoletos

---

## 9. Casos reales del monorepo

### 📦 CachedUser

```dart
@Collection()
class CachedUser {
  Id id = Isar.autoIncrement;

  @Index(unique: true)
  String? userId;

  String? email;
  String? fullName;
  String? phone;
  String? avatarUrl;
  DateTime? createdAt;
  DateTime? emailConfirmedAt;
  DateTime? cachedAt;
  DateTime? expiresAt;
}
```

**Uso:** Cache del perfil del usuario autenticado. Se guarda al hacer login/signup y se lee para mostrar datos básicos sin llamar a la API.

### 📦 CachedToken

```dart
@Collection()
class CachedToken {
  Id id = Isar.autoIncrement;

  @Index(unique: true)
  String? token;

  DateTime? cachedAt;
  DateTime? expiresAt;
}
```

**Uso:** Cache del JWT. Permite mantener la sesión abierta entre reinicios de la app.

### 📦 CachedProfile

```dart
@Collection()
class CachedProfile {
  Id id = Isar.autoIncrement;

  @Index(unique: true)
  String? userId;

  String? fullName;
  String? phoneNumber;
  String? email;
  String? avatarUrl;
  String? preferredLanguage;
  bool? notificationsEnabled;
  DateTime? createdAt;
  DateTime? updatedAt;
  DateTime? cachedAt;
  DateTime? expiresAt;
}
```

**Uso:** Cache del perfil detallado del perfil de usuario. Se guarda al editar el perfil y se lee para mostrar datos completos.

### 📦 CachedPaymentMethod

```dart
@Collection()
class CachedPaymentMethod {
  Id id = Isar.autoIncrement;

  @Index()                      // Índice simple (no único — varios métodos por usuario)
  String? userId;

  @Index(unique: true)
  String? paymentMethodId;

  String? type;
  String? name;
  String? bankName;
  String? accountHolder;
  String? accountNumber;
  String? phone;
  String? email;
  String? walletAddress;
  String? qrCodeUrl;
  String? instructions;
  String? cedula;
  String? bankCode;
  String? blockchainNetwork;
  bool? isActive;
  bool? isDefault;
  DateTime? createdAt;
  DateTime? updatedAt;
  DateTime? cachedAt;
  DateTime? expiresAt;
}
```

**Uso:** Cache de los métodos de pago de un usuario. Notar que `userId` tiene `@Index()` (no único) porque un usuario puede tener varios métodos de pago, mientras que `paymentMethodId` es único.

### 🎯 Resumen de índices

| Colección | Business Key | Índice único | Uso |
|-----------|-------------|--------------|-----|
| `CachedUser` | `userId` | `@Index(unique: true)` | Solo un usuario por sesión |
| `CachedToken` | `token` | `@Index(unique: true)` | Solo un token activo |
| `CachedProfile` | `userId` | `@Index(unique: true)` | Solo un perfil por usuario |
| `CachedPaymentMethod` | `paymentMethodId` | `@Index(unique: true)` | Múltiples métodos por usuario |

---

## 10. Checklist

- [ ] Definí las colecciones con `@Collection()`
- [ ] Agregué `@Index(unique: true)` en los business keys
- [ ] Incluí los campos `cachedAt` y `expiresAt` para TTL
- [ ] Ejecuté `build_runner` y los `.g.dart` se generaron
- [ ] Todas las escrituras están dentro de `writeTxn`
- [ ] Uso `where().findFirstSync()` para lecturas síncronas
- [ ] Implementé validación de TTL antes de retornar datos cacheados
- [ ] Uso `filter()` solo cuando el campo no tiene índice

---

## 📚 Referencias

- [isar_community | pub.dev](https://pub.dev/packages/isar_community) — Paquete activo de Isar para Dart/Flutter
- [Isar | Documentación original](https://isar.dev) — Referencia de operaciones y queries (legacy)

---

**Nivel:** Intermedio  
**Siguiente:** [03-implementacion-local-datasource.md](./03-implementacion-local-datasource.md)
