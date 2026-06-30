# 06 — Estrategias Avanzadas para Monorepo

---

## 1. Path filtering en monorepo

```yaml
# .github/workflows/flutter-ci.yml
name: Flutter CI
on:
  push:
    paths:
      - 'apps/mobile/**'
      - '.github/workflows/flutter-*'
  pull_request:
    paths:
      - 'apps/mobile/**'

# .github/workflows/nextjs-ci.yml
name: Next.js CI
on:
  push:
    paths:
      - 'apps/web/**'
      - '.github/workflows/nextjs-*'
```

**¿Por qué?** Si solo cambias la web, no ejecutas los tests de Flutter (y viceversa). Ahorra minutos de CI.

---

## 2. Reutilizar workflows con `workflow_call`

```yaml
# .github/workflows/flutter-quality.yml (workflow reutilizable)
name: Flutter Quality Gate
on:
  workflow_call:
    inputs:
      working-dir:
        required: true
        type: string
      flutter-version:
        required: false
        type: string
        default: '3.24.0'
    secrets:
      SUPABASE_URL:
        required: false

jobs:
  quality:
    defaults:
      run:
        working-directory: ${{ inputs.working-dir }}
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ inputs.flutter-version }}
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test
```

```yaml
# .github/workflows/mobile-ci.yml (workflow que lo llama)
name: Mobile CI
on: push

jobs:
  quality:
    uses: ./.github/workflows/flutter-quality.yml
    with:
      working-dir: apps/mobile
    secrets:
      SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
```

---

## 3. Caching en monorepo

```yaml
- uses: actions/cache@v4
  with:
    path: |
      apps/mobile/.dart_tool
      ~/.pub-cache
    key: ${{ runner.os }}-flutter-${{ hashFiles('apps/mobile/pubspec.lock') }}
    restore-keys: |
      ${{ runner.os }}-flutter-
```

**Pro tip**: usa `hashFiles` con la ruta exacta del `pubspec.lock` de cada subproyecto para evitar invalidar caches innecesariamente.

---

## 4. Detectar cambios en subdirectorios

```yaml
jobs:
  detect:
    runs-on: ubuntu-latest
    outputs:
      mobile: ${{ steps.filter.outputs.mobile }}
      web: ${{ steps.filter.outputs.web }}
      supabase: ${{ steps.filter.outputs.supabase }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # necesario para git diff

      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            mobile:
              - 'apps/mobile/**'
            web:
              - 'apps/web/**'
            supabase:
              - 'supabase/**'

  test-mobile:
    needs: detect
    if: needs.detect.outputs.mobile == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing mobile..."
```

---

## 5. Estrategia de naming para workflows

```
.github/workflows/
├── flutter-ci.yml          # Quality gate para Flutter
├── nextjs-ci.yml           # Quality gate para Next.js
├── supabase-tests.yml      # Tests de BD
├── supabase-dev-sync.yml   # Sync a dev remoto
├── flutter-android-release.yml  # Release Android
└── pr-title-lint.yml       # Validación de PRs
```

**Convención:** `<framework>-<accion>.yml`

---

**Siguiente**: [07-ejercicios.md](./07-ejercicios.md)
