# 02 — Flujo de Actualización

> Cómo actualizar dependencias Flutter y npm de forma segura, sin romper el proyecto.

---

## 1. `dart pub outdated`

### 1.1 Leer la Salida

```bash
dart pub outdated
```

```
Showing outdated packages.
[*] indicates versions that are not mutually compatible.

Package Name       Current  Upgradable  Resolvable  Latest
dio                5.9.0    5.11.0      5.11.0      5.11.0
equatable          2.0.5    2.1.0       2.1.0       2.1.0
flutter_bloc       9.1.0    9.1.1       9.1.1       9.1.1
go_router          17.4.1   17.5.0      17.5.0      17.5.0
```

| Columna | Significado |
|---|---|
| **Current** | Lo que tienes instalado |
| **Upgradable** | Versión a la que puedes subir con `dart pub upgrade` (solo patch/minor) |
| **Resolvable** | Versión máxima que pub puede resolver sin cambiar `pubspec.yaml` |
| **Latest** | Última versión publicada (puede ser major) |

### 1.2 Priorizar Actualizaciones

1. **Patch** (3.0.0 → 3.0.1) — seguras, merge automático
2. **Minor** (3.0.0 → 3.1.0) — revisar changelog
3. **Major** (3.0.0 → 4.0.0) — planificar migración

---

## 2. `dart pub upgrade`

### 2.1 Upgrade Normal

```bash
# Actualiza todo a la versión resolvable
dart pub upgrade

# Actualiza un paquete específico
dart pub upgrade flutter_bloc
```

Esto actualiza solo **dentro de la constraint**. Si tienes `^9.1.0`, subirá a `9.x.x` pero nunca a `10.0.0`.

### 2.2 Upgrade con Major Versions

```bash
# Activar explícitamente major versions
dart pub upgrade --major-versions

# Para un solo paquete
dart pub upgrade flutter_bloc --major-versions
```

Esto **modifica `pubspec.yaml`** para actualizar la constraint: `^9.1.0` → `^10.0.0`.

> **⚠️ Precaución:** No ejecutes `--major-versions` en todos los paquetes a la vez. Hazlo de uno en uno, revisando breaking changes.

### 2.3 Equivalente npm

```bash
# Mostrar desactualizados
npm outdated

# Actualizar dentro de semver
npm update

# Actualizar a latest (cambia package.json)
npm install next@latest

# Auditoría de seguridad
npm audit
```

---

## 3. Proceso Seguro de Upgrade

### 3.1 Flujo

```
1. Leer CHANGELOG del paquete
       ↓
2. Buscar migration guide (GitHub releases / docs)
       ↓
3. dart pub upgrade <paquete>
       ↓
4. dart pub outdated (verificar que todo esté bien)
       ↓
5. dart fix --apply --dry-run
   dart fix --apply
       ↓
6. Ejecutar tests: flutter test -j 1
       ↓
7. Ejecutar build_runner si aplica
       ↓
8. Compilar: flutter analyze
       ↓
9. Commit separado con mensaje semántico
```

### 3.2 Ejemplo Real: `supabase_flutter`

```bash
# 1. Ver versión actual
grep supabase_flutter pubspec.lock

# 2. Revisar changelog
# https://github.com/supabase/supabase-flutter/releases

# 3. Actualizar
dart pub upgrade supabase_flutter

# 4. Migrar si hay breaking changes
# - Revisar cambios en supabase_flutter (ej: nueva inicialización)
dart fix --apply

# 5. Testear
flutter analyze
flutter test -j 1

# 6. Commit
git add pubspec.yaml pubspec.lock lib/
git commit -m "fix(deps): update supabase_flutter to 2.17.2"
```

### 3.3 Casos Especiales por Paquete

| Paquete | Qué revisar post-upgrade |
|---|---|
| `supabase_flutter` | Cambios en inicialización, nuevas tablas de auth |
| `flutter_bloc` / `bloc` | Nuevos métodos en BlocObserver, cambios en HydratedBloc |
| `fpdart` | Cambios en Either/TaskEither API (Dart 3 pattern matching) |
| `go_router` | Cambios en ShellRoute, StatefulShellRoute, redirect |
| `dio` | Interceptors, cancelación de requests, multipart |
| `isar_community` | Regenerar archivos `.g.dart` con build_runner |

---

## 4. `dart fix --apply`

```bash
# Ver qué cambios haría
dart fix --dry-run

# Aplicar cambios automáticos
dart fix --apply
```

`dart fix` aplica migraciones automáticas del SDK de Dart. Es el **primer paso** después de cualquier upgrade. No cubre migraciones de paquetes de terceros.

---

## 5. Build Runner y Code Generation

Después de actualizar paquetes que usan code generation:

```bash
# Limpiar caché primero
dart run build_runner clean

# Regenerar todo
dart run build_runner build --delete-conflicting-outputs
```

Problema común: `build_runner` queda en versión incompatible. Si falla, actualiza `build_runner` primero.

---

## 6. npm: Upgrade en Web

```bash
# Ver todo
npm outdated

# Actualizar todo
npm update

# Paquete específico
npm install next@latest

# Verificar vulnerabilidades
npm audit

# Fix automático (solo patch)
npm audit fix
```

**Convención del monorepo:** Next.js y React están exact-pinned. Se actualizan manualmente revisando el migration guide.

---

## 7. Ejercicio

Escenario: Acaban de publicar `fpdart 2.0.0` con breaking changes. Tu proyecto usa `^1.2.0`.

1. Revisa el changelog de fpdart en GitHub
2. Ejecuta `dart pub upgrade fpdart --major-versions`
3. Corre `dart fix --dry-run` y `dart fix --apply`
4. Si fallan los tests, identifica qué cambió
5. Actualiza el código para la nueva API
6. Commit con mensaje semántico

---

## Resumen

1. **`dart pub outdated`** — diagnóstico, no acción
2. **`dart pub upgrade`** — actualiza dentro de constraints
3. **`--major-versions`** — solo para un paquete a la vez
4. **Siempre** leer CHANGELOG antes de actualizar
5. **Siempre** correr `dart fix --apply` después
6. **Siempre** tests + analyze antes de commitear

---

## 📚 Referencias

- [Dart | Pub outdated](https://dart.dev/tools/pub/cmd/pub-outdated) — Comando `dart pub outdated`
- [Dart | Pub upgrade](https://dart.dev/tools/pub/cmd/pub-upgrade) — Comando `dart pub upgrade`
- [Dart | dart fix](https://dart.dev/tools/dart-fix) — Migraciones automáticas de código
- [npm Docs | npm-outdated](https://docs.npmjs.com/cli/v12/commands/npm-outdated) — Comando `npm outdated`
- [npm Docs | npm-audit](https://docs.npmjs.com/cli/v12/commands/npm-audit) — Comando `npm audit`

---

> 📖 **Siguiente:** [03-automatizacion-dependabot-renovate.md](./03-automatizacion-dependabot-renovate.md) — Automatizar actualizaciones con Dependabot y Renovate
