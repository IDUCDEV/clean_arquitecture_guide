# 🧪 07c — Práctica: Local DataSources con Isar Community

> **¿De qué trata esta práctica?** De testear Local DataSources que usan Isar Community como base de datos local embebida, usando instancias reales de Isar sin mocks.

---

## 📋 Contenido completo

Esta práctica se desarrolla en la sección **[06-ALMACENAMIENTO-LOCAL](../06-ALMACENAMIENTO-LOCAL/)** de la guía. Aquí tienes un resumen de los patrones y un acceso directo a los ejercicios.

---

## 🎯 Patrón general

| Componente | Código |
|------------|--------|
| **Setup** | `Isar.open([Schemas], directory: Directory.systemTemp.path, name: 'unique_name')` |
| **Limpieza** | `isar.writeTxn(() async { await isar.collection.where().deleteAll(); })` |
| **Seed de datos** | `isar.writeTxn(() async { await isar.collection.put(obj); })` |
| **Assert** | `isar.collection.where().findFirstSync()` |
| **Error test** | `isar.close()` → operación → espera `CacheException` → `reopenForErrorTest()` |
| **Teardown** | `isar.close(deleteFromDisk: true)` |

### 🔑 Diferencia clave vs SharedPreferences

| Aspecto | SharedPreferences (Parte 3) | Isar (esta práctica) |
|---------|----------------------------|---------------------|
| **Mock** | `MockSharedPreferences` con Mocktail | No se mockea — se usa Isar real |
| **Setup** | `MockSharedPreferences()` | `Isar.open()` con `Directory.systemTemp` |
| **Verificación** | `verify(() => mock.setString(...))` | `findFirstSync()` leyendo directamente de Isar |
| **Datos** | Strings serializados | Objetos Dart directamente |

---

## 📁 Ejercicios

| # | Ejercicio | Archivo completo |
|---|-----------|-----------------|
| 1 | `AuthLocalDataSourceImpl` — token y usuario, métodos síncronos, TTL | [Ver código](../06-ALMACENAMIENTO-LOCAL/04-testing-local-datasource.md#5-ejercicio-1-authlocaldatasourceimpl) |
| 2 | `ProfileLocalDataSourceImpl` — perfil con cache-profile y TTL | [Ver código](../06-ALMACENAMIENTO-LOCAL/04-testing-local-datasource.md#6-ejercicio-2-profilelocaldatasourceimpl) |
| 3 | `PaymentMethodLocalDataSourceImpl` — listas, filtro por userId, reemplazo parcial | [Ver código](../06-ALMACENAMIENTO-LOCAL/04-testing-local-datasource.md#7-ejercicio-3-paymentmethodlocaldatasourceimpl) |
| 4 | `CacheManager` — registro centralizado de limpieza | [Ver código](../06-ALMACENAMIENTO-LOCAL/04-testing-local-datasource.md#8-ejercicio-4-cachemanager) |
| 5 | `UserSessionImpl` — acceso síncrono al userId desde Isar | [Ver código](../06-ALMACENAMIENTO-LOCAL/04-testing-local-datasource.md#9-ejercicio-5-usersessionimpl) |

---

## 🧠 Conceptos cubiertos

- **Setup**: `Isar.open()` con esquemas específicos, `instanceCounter` para nombres únicos
- **Escritura**: `cacheToken()`, `cacheUser()`, `cacheProfile()`, `cachePaymentMethods()`
- **Lectura**: `getCachedToken()` (síncrono), `getCachedUser()`, `getCachedProfile()`, `getCachedPaymentMethods()`
- **TTL**: seed con `expiresAt` en pasado → esperar `null`
- **Errores**: cerrar Isar → esperar `CacheException('cache_write_error: ...')`
- **Limpieza**: `clearCache()` + verificación con `countSync()`

---

## 🚀 Siguiente paso

Ve al contenido completo en [06-ALMACENAMIENTO-LOCAL/04-testing-local-datasource.md](../06-ALMACENAMIENTO-LOCAL/04-testing-local-datasource.md).

---

**Nivel:** Intermedio  
**Tiempo estimado:** 2-3 horas  
**Requiere:** [06-ALMACENAMIENTO-LOCAL](../06-ALMACENAMIENTO-LOCAL/) — leer antes los conceptos de Isar y LocalDataSource
