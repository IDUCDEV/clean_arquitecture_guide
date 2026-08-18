# 04 - Almacenamiento Local con Isar

> Aprende a implementar almacenamiento local embebido con Isar Community en Flutter, siguiendo Clean Architecture.

---

## Prerrequisitos

- **Flutter** instalado (3.x o superior)
- Conocimiento básico de Clean Architecture (completar `01-CLEAN-ARCHITECTURE` antes)
- Comprensión de la estructura de un monorepo Flutter
- Supabase configurado (completar `02-MONOREPO-STRUCTURE` y `03-AUTH-SUPABASE` antes)

---

## 📋 Índice

| Archivo | Descripción |
|---------|-------------|
| [01-isar-introduccion.md](./01-isar-introduccion.md) | ¿Qué es Isar? Diferencias entre `isar`, `isar_community` y `isar v4`. Setup y code generation |
| [02-modelos-operaciones.md](./02-modelos-operaciones.md) | Colecciones, anotaciones, CRUD, queries, filtros, TTL pattern con ejemplos reales |
| [03-implementacion-local-datasource.md](./03-implementacion-local-datasource.md) | IsarService singleton, LocalDataSource pattern, CacheManager, UserSessionImpl |

---

## 🎯 Contenido

### 1. Introducción a Isar
- ¿Qué es Isar? Base de datos embebida NoSQL para Flutter
- `isar` (original, abandonado) vs `isar_community` (fork mantenido, v3.x) vs `isar v4` (rewrite en Rust)
- Instalación, `pubspec.yaml`, code generation con `build_runner`
- Arquitectura: colecciones, esquemas, índices

### 2. Modelos y Operaciones
- Definición de colecciones con `@Collection()`, `@Index()`, `@enumerated`, `@embedded`
- CRUD: `put()`, `putAll()`, `get()`, `delete()` dentro de `writeTxn`
- Queries: `where()`, `filter()`, `sortBy()`, `offset()`, `limit()`
- Patrón TTL (Time-To-Live): `cachedAt` / `expiresAt` + validación al leer
- Ejemplos basados en `CachedUser`, `CachedToken`, `CachedProfile`, `CachedPaymentMethod`

### 3. Implementación de Local DataSource
- `IsarService`: singleton, lazy initialization, `clear()`
- `CacheException` para errores de cache (vs `ServerException` para remoto)
- LocalDataSource pattern: abstract + impl con Isar injectado
- Cache strategies: reemplazar todo (deleteAll + put), TTL expiry
- `CacheManager`: registro centralizado de funciones de limpieza
- `UserSessionImpl`: acceso síncrono al usuario autenticado desde Isar

---

## 🚀 Siguiente paso

Continue with [01-isar-introduccion.md](./01-isar-introduccion.md) to understand what Isar is and how to set it up.

---

**Nivel:** Intermedio  
**Tiempo estimado:** 3-4 horas
