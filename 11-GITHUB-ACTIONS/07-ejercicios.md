# 07 — Ejercicios de GitHub Actions

---

## Ejercicio 1: Identificar problemas en un workflow

```yaml
name: CI
on: push

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: flutter test
      - run: make build-apk
```

**Preguntas:**
1. ¿Falta algo para que `flutter test` funcione?
2. ¿`make build-apk` debería ejecutarse en cada push?
3. ¿Qué le agregarías?

<details>
<summary>🔍 Solución</summary>

1. Falta `subosito/flutter-action` para instalar Flutter
2. No, build-apk debería ejecutarse solo con tags (usa `on: push: tags: ["v*"]`)
3. Agregaría: setup Flutter, cache, separaría test y build en diferentes jobs/workflows
</details>

---

## Ejercicio 2: Crear un workflow desde cero

```dart
// Imagina un proyecto Flutter simple (no monorepo).
// Crea un workflow CI que:
// 1. Se ejecute en push y PR a main
// 2. Setup Flutter 3.24.0
// 3. Cachee dependencias
// 4. Ejecute: dart format, flutter analyze, flutter test
// 5. Si falla algún paso, que todo el workflow falle

// Escribe el YAML completo
```

<details>
<summary>🔍 Solución</summary>

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.0'

      - uses: actions/cache@v4
        with:
          path: ~/.pub-cache
          key: ${{ runner.os }}-flutter-${{ hashFiles('**/pubspec.lock') }}

      - run: dart format --output=none --set-exit-if-changed .
      - run: flutter analyze
      - run: flutter test
```
</details>

---

## Ejercicio 3: Workflow con matrix

```yaml
# Crea un workflow que ejecute los tests con
# Flutter 3.22.0 y 3.24.0 en ubuntu-latest
# Además, que construya el APK solo con la versión 3.24.0

jobs:
  test:
    strategy:
      matrix:
        flutter_version: ['3.22.0', '3.24.0']

    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ matrix.flutter_version }}
      - run: flutter test

  build:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.0'
      - run: flutter build apk --release
```

---

## Ejercicio 4: Workflow con Supabase

```yaml
# Crea un workflow que:
# 1. Se ejecute cuando cambien archivos en supabase/
# 2. Instale Supabase CLI
# 3. Inicie Supabase
# 4. Ejecute db lint y db test
# 5. Siempre detenga Supabase al final

name: Supabase Tests
on:
  push:
    paths: [supabase/**]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1

      - name: Start Supabase
        run: supabase start

      - name: Lint migrations
        run: supabase db lint --local

      - name: Run pgTAP tests
        run: supabase test db

      - name: Stop Supabase
        if: always()
        run: supabase stop
```

---

## ✅ Checklist

- [ ] Entiendo la arquitectura: workflow → job → step → runner
- [ ] Sé diferenciar `on: push` vs `on: pull_request` vs `on: schedule`
- [ ] Sé usar `uses:`, `run:`, `with:`, `env:`
- [ ] Sé usar `needs:` para dependencias entre jobs
- [ ] Sé usar `if:` para condicionales
- [ ] Sé usar matrix builds
- [ ] Sé usar `actions/cache` para dependencias
- [ ] Sé configurar secrets en GitHub
- [ ] Entiendo path filtering para monorepo
- [ ] Puedo crear un workflow CI completo desde cero

---

**Siguiente**: Vuelve al [README de la guía](../README.md) para ver el índice completo.
