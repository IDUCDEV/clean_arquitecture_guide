# 01 — Conceptos Fundamentales

---

## 1. Arquitectura

```
GitHub Actions
│
├── Workflow  (archivo .yml en .github/workflows/)
│   ├── Job 1 (runs-on: ubuntu-latest)
│   │   ├── Step 1 (uses: actions/checkout@v4)
│   │   ├── Step 2 (run: make setup)
│   │   └── Step 3 (run: make check)
│   │
│   └── Job 2 (runs-on: macos-latest)
│       ├── Step 1 (uses: actions/checkout@v4)
│       └── Step 2 (run: make build-ios)
│
└── Event (push, pull_request, schedule...)
```

### Conceptos clave

| Concepto | Qué es | Ejemplo |
|----------|--------|---------|
| **Workflow** | Archivo YAML que define la automatización | `ci-quality.yml` |
| **Job** | Conjunto de pasos que se ejecutan en el mismo runner | `quality-gate` |
| **Step** | Un comando o action individual | `make test` |
| **Runner** | Máquina donde se ejecuta el job | `ubuntu-latest` |
| **Event** | Lo que dispara el workflow | `push`, `pull_request` |
| **Action** | Código reutilizable (puede ser un paso) | `actions/checkout@v4` |

---

## 2. Eventos (triggers)

```yaml
# Push a cualquier rama
on: push

# Push solo a ramas específicas
on:
  push:
    branches: [dev, main]

# Pull request
on:
  pull_request:
    types: [opened, synchronize, reopened]

# Programado (cron)
on:
  schedule:
    - cron: '0 3 * * *'  # todos los días a las 3am

# Manual
on:
  workflow_dispatch:

# Evento compuesto
on:
  push:
    branches: [dev, main]
    paths: [supabase/**]  # solo si cambian archivos en supabase/
  pull_request:
    branches: [main]
```

---

## 3. Jobs y dependencias

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: make lint

  test:
    runs-on: ubuntu-latest
    needs: lint  # espera a que lint termine
    steps:
      - run: make test

  deploy:
    runs-on: ubuntu-latest
    needs: [lint, test]  # espera a ambos
    if: github.ref == 'refs/heads/main'  # solo en main
    steps:
      - run: make deploy
```

**Gráfico de ejecución:**
```
lint ──> test ──> deploy
```

---

## 4. Runners

```yaml
jobs:
  test-linux:
    runs-on: ubuntu-latest  # Linux, gratuito

  test-macos:
    runs-on: macos-latest   # macOS (necesario para iOS)

  test-windows:
    runs-on: windows-latest # Windows
```

| Runner | Gratuito | Usos comunes |
|--------|----------|-------------|
| `ubuntu-latest` | ✅ 2000 min/mes | Tests, lint, build Android |
| `macos-latest` | ❌ (cuota aparte) | Build iOS, Flutter desktop |
| `windows-latest` | ✅ 2000 min/mes | Build Windows |

---

## 🏋️ Mini-ejercicio

```yaml
# Dado este workflow, ¿en qué orden se ejecutan los jobs?
# ¿Qué jobs se ejecutan en paralelo?
# ¿Qué jobs esperan a otros?

name: test
on: push

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "lint"

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - run: echo "test"

  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "build"
```

<details>
<summary>🔍 Solución</summary>

Orden:
- `lint` y `build` empiezan en paralelo (no tienen `needs`)
- `test` espera a `lint` (tiene `needs: lint`)
- `build` no espera a nadie

```
lint ──> test
build ──> (independiente, paralelo)
```
</details>

---

**Siguiente**: [02-sintaxis-yaml.md](./02-sintaxis-yaml.md) — Anatomía de un workflow
