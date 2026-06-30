# 04 — Análisis de los Workflows del Proyecto

> Recorrido de los 6 workflows reales del proyecto rifa-gestion-app.

---

## Workflow 1: CI Quality Gate

**Archivo:** `.github/workflows/ci-quality.yml`

```yaml
name: CI - Quality Gate

on:
  push:
    branches: [dev, main]
  pull_request:
    types: [opened, synchronize, reopened]
```

**¿Cuándo se ejecuta?**
- Push a `dev` o `main`
- Cuando se abre, actualiza o reabre un PR

**Jobs:**
- `quality-gate` en `ubuntu-latest`
  1. Checkout código
  2. Setup Flutter 3.24.0
  3. Cache de dependencias
  4. `dart format --output=none --set-exit-if-changed` (formato)
  5. `flutter analyze` (análisis estático)
  6. `flutter test --coverage` (tests + cobertura)
  7. SonarCloud (solo si hay token)

**¿Por qué es importante?** Es la puerta de entrada. Si este workflow falla, el PR no debería mergearse.

---

## Workflow 2: Supabase Tests

**Archivo:** `.github/workflows/supabase-tests.yml`

```yaml
on:
  pull_request:
    paths: [supabase/**]
  push:
    branches: [dev, main]
    paths: [supabase/**]
```

**¿Cuándo se ejecuta?** Solo cuando cambian archivos en `supabase/`. Esto ahorra ejecuciones innecesarias.

**Jobs:**
- `supabase-test` en `ubuntu-latest`
  1. Checkout
  2. Instalar Supabase CLI
  3. `supabase start` (levanta Supabase local con Docker)
  4. `supabase db lint --local` (lint de migraciones)
  5. `supabase test db` (ejecuta tests pgTAP)
  6. `supabase stop` (siempre, incluso si falla)

**Patrón importante:** El step 6 usa `if: always()` para asegurar que Supabase se detenga incluso si los tests fallan.

---

## Workflow 3: Supabase Dev Sync

**Archivo:** `.github/workflows/supabase-dev.yml`

```yaml
on:
  push:
    branches: [dev]
```

**¿Qué hace?** Cuando se pushea a `dev`, detecta si hay cambios en `supabase/migrations/` y si los hay, los aplica al proyecto de Supabase Cloud vinculado.

**Jobs:**
1. Detecta cambios con `git diff`
2. Si hay cambios: linkea el proyecto, lintea migraciones, pushea

**Secretos que necesita:**
- `SUPABASE_ACCESS_TOKEN`
- `SUPABASE_PROJECT_ID`
- `SUPABASE_DB_PASSWORD`

---

## Workflow 4: Flutter Android Release

**Archivo:** `.github/workflows/flutter-android-release.yml`

```yaml
on:
  push:
    tags: ["v*"]
```

**¿Cuándo se ejecuta?** Cuando se crea un tag que empieza con `v` (ej: `v1.2.0`).

**Jobs:**
1. Setup Flutter
2. Build APK con `--dart-define` para las variables de Supabase
3. Build AAB
4. Crear GitHub Release con los archivos compilados

---

## Workflow 5: Next.js CI

**Archivo:** `.github/workflows/nextjs-ci.yml`

```yaml
on:
  push:
    branches: [dev, main]
    paths: [apps/web/**]
```

Para la app web independiente. Usa `npm ci`, `npm run lint`, `npm test`, `npm run build`.

---

## Workflow 6: PR Title Lint

**Archivo:** `.github/workflows/pr-title-lint.yml`

```yaml
on: pull_request
```

Usa `amannn/action-semantic-pull-request` para validar que el título del PR siga Conventional Commits.

---

## 📊 Mapa de workflows

| Workflow | Trigger | Tiempo estimado | ¿Bloqueante? |
|----------|---------|----------------|-------------|
| CI Quality Gate | Push/PR a dev, main | ~5 min | ✅ Sí |
| Supabase Tests | Cambios en supabase/ | ~3 min | ✅ Sí |
| Supabase Dev Sync | Push a dev | ~2 min | ❌ No (automático) |
| Flutter Android Release | Tag v* | ~10 min | ❌ No (bajo demanda) |
| Next.js CI | Cambios en apps/web | ~3 min | ✅ Sí |
| PR Title Lint | Cualquier PR | ~10 seg | ✅ Sí |

---

**Siguiente**: [05-secrets-envs-matrix.md](./05-secrets-envs-matrix.md) — Secrets, entornos y matrix builds
