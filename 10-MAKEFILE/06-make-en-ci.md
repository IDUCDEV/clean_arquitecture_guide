# 06 — Make en GitHub Actions

> Make y GitHub Actions son **complementarios**: Actions orquesta los runners, Make ejecuta la lógica del proyecto.

---

## 1. ¿Por qué usar Make en CI?

```yaml
# ❌ SIN Make: acciones repetitivas y difíciles de mantener
steps:
  - name: Install deps
    run: cd apps/mobile && flutter pub get
  - name: Format
    run: cd apps/mobile && dart format --output=none --set-exit-if-changed .
  - name: Analyze
    run: cd apps/mobile && flutter analyze
  - name: Test
    run: cd apps/mobile && flutter test

# ✅ CON Make: un solo comando
steps:
  - name: Quality check
    run: make check   # format + analyze + test en un comando
```

**Ventajas:**
- **DRY**: la lógica está en el Makefile, no duplicada en YAML
- **Consistencia**: local y CI ejecutan exactamente lo mismo
- **Mantenibilidad**: cambiar la lógica en un solo lugar

---

## 2. Workflow CI típico con Make

```yaml
name: CI
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: apps/mobile  # evita cd repetitivos

    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.0'

      - name: Cache pub
        uses: actions/cache@v4
        with:
          path: ~/.pub-cache
          key: ${{ runner.os }}-flutter-${{ hashFiles('apps/mobile/pubspec.lock') }}

      - name: Setup
        run: make setup

      - name: Quality gate
        run: make check

      - name: Coverage
        run: make coverage
```

---

## 3. Comandos de Make usados en CI/CD

| Comando | En CI hace |
|---------|------------|
| `make setup` | `flutter pub get` + `build_runner` |
| `make check` | `format` + `analyze` + `test` |
| `make coverage` | Tests con reporte de cobertura |
| `make build-apk` | Compila APK release |
| `make supabase-up` | Inicia Supabase para tests |
| `make db-push` | Aplica migraciones en producción |

---

## 4. Make con condiciones en CI

```makefile
# El Makefile puede adaptarse según el entorno
ifdef CI
  FLUTTER := flutter  # en CI no hay FVM
  EXTRA_FLAGS := --no-sound-null-safety
else
  FLUTTER := $(shell [ -d .fvm ] && echo fvm flutter || echo flutter)
endif

test:
	$(FLUTTER) test $(EXTRA_FLAGS)
```

```yaml
# En GitHub Actions:
- name: Test
  run: make test
  env:
    CI: true
```

---

## 5. Patrón: Make + matrix builds

```yaml
strategy:
  matrix:
    flutter_version: ['3.22.0', '3.24.0']

steps:
  - uses: subosito/flutter-action@v2
    with:
      flutter-version: ${{ matrix.flutter_version }}

  - run: make check
```

---

## 📚 Referencias

- [GNU | Make manual](https://www.gnu.org/software/make/manual/) — Documentación oficial de GNU Make

---

**Siguiente**: [07-ejercicios.md](./07-ejercicios.md) — Práctica con Makefiles
