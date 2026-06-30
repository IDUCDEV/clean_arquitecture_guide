# 02 — Sintaxis YAML de GitHub Actions

---

## 1. Anatomía completa de un workflow

```yaml
# .github/workflows/ci.yml

name: CI - Quality Gate        # Nombre visible en GitHub
run-name: "CI en ${{ github.ref_name }}"  # Nombre de la ejecución

# ─── TRIGGERS ─────────────────────────────────────
on:
  push:
    branches: [dev, main]
  pull_request:
    types: [opened, synchronize]

# ─── VARIABLES GLOBALES ──────────────────────────
env:
  FLUTTER_VERSION: '3.24.0'

# ─── JOBS ─────────────────────────────────────────
jobs:
  quality:                     # ID del job (único)
    name: Quality Gate         # Nombre visible
    runs-on: ubuntu-latest     # Runner
    timeout-minutes: 20        # Timeout máximo
    defaults:                  # Defaults para steps
      run:
        working-directory: apps/mobile

    # ─── STEPS ──────────────────────────────────
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ env.FLUTTER_VERSION }}

      - name: Cache pub
        uses: actions/cache@v4
        with:
          path: ~/.pub-cache
          key: ${{ runner.os }}-flutter-${{ hashFiles('apps/mobile/pubspec.lock') }}

      - name: Install deps
        run: flutter pub get

      - name: Run tests
        run: flutter test --coverage
```

---

## 2. Elementos clave

### `uses:` — Reutilizar actions

```yaml
# Action oficial de GitHub
- uses: actions/checkout@v4

# Action de la comunidad
- uses: subosito/flutter-action@v2

# Action local (en .github/actions/)
- uses: ./.github/actions/setup-flutter-env

# Action con versión específica
- uses: actions/cache@v4
```

### `run:` — Comandos directos

```yaml
- run: flutter test

- run: |
    flutter format --set-exit-if-changed .
    flutter analyze
    flutter test

- run: make check  # delega en el Makefile
```

### `with:` — Parámetros de la action

```yaml
- uses: subosito/flutter-action@v2
  with:
    flutter-version: '3.24.0'
    channel: 'stable'
```

### `env:` — Variables de entorno

```yaml
- name: Test
  run: flutter test --coverage
  env:
    SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
```

---

## 3. Condicionales con `if:`

```yaml
steps:
  - name: Deploy
    if: github.ref == 'refs/heads/main'
    run: make deploy

  - name: Notify
    if: always()  # se ejecuta incluso si falla
    run: echo "done"

  - name: Solo si cambió supabase/
    if: github.event_name == 'pull_request' ||
        (github.event_name == 'push' && contains(github.event.head_commit.modified, 'supabase/'))
```

---

## 4. Outputs entre steps

```yaml
steps:
  - id: changes
    run: |
      if git diff --quiet HEAD~1 -- supabase/; then
        echo "changed=false" >> "$GITHUB_OUTPUT"
      else
        echo "changed=true" >> "$GITHUB_OUTPUT"
      fi

  - name: Deploy DB
    if: steps.changes.outputs.changed == 'true'
    run: supabase db push
```

---

## 🏋️ Mini-ejercicio

```yaml
# ¿Cuántos jobs tiene este workflow?
# ¿Qué hace cada step?
# ¿Dónde se ejecuta?

name: Test
on: pull_request

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter test
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
```

<details>
<summary>🔍 Solución</summary>

- 1 job (`test`)
- Step 1: descarga el código del repo
- Step 2: instala Flutter
- Step 3: ejecuta tests con la URL de Supabase como variable de entorno
- Se ejecuta en `ubuntu-latest` (Linux)
</details>

---

**Siguiente**: [03-actions-esenciales.md](./03-actions-esenciales.md) — Actions esenciales para Flutter + Supabase
