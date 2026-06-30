# 05 — Secrets, Entornos y Matrix Builds

---

## 1. Secrets

Los secrets son variables **encriptadas** que no aparecen en logs.

### Cómo se crean

```
GitHub → Settings → Secrets and variables → Actions
```

### Cómo se usan

```yaml
steps:
  - name: Build APK
    run: |
      flutter build apk --release \
        --dart-define=SUPABASE_URL=${{ secrets.SUPABASE_URL }} \
        --dart-define=SUPABASE_ANON_KEY=${{ secrets.SUPABASE_ANON_KEY }}
```

> **⚠️ Regla de seguridad**: los secrets NUNCA se muestran en los logs. GitHub los enmascara automáticamente.

### Secrets del proyecto

| Secret | Dónde obtenerlo | Para qué se usa |
|--------|----------------|-----------------|
| `SUPABASE_URL` | Dashboard Supabase → Settings → API | Conectar app a Supabase |
| `SUPABASE_ANON_KEY` | Dashboard Supabase → Settings → API | Clave anónima de Supabase |
| `SUPABASE_ACCESS_TOKEN` | `supabase auth token` (CLI) | Autenticar Supabase CLI |
| `SUPABASE_PROJECT_ID` | Dashboard Supabase → Settings → General | Referencia al proyecto |
| `SUPABASE_DB_PASSWORD` | Al crear el proyecto | Acceso a la BD |
| `SONAR_TOKEN` | SonarCloud | Reportes de calidad |

---

## 2. Variables de entorno

Las variables de entorno (`vars`) son como secrets pero **no encriptadas**. Visibles en logs.

```yaml
env:
  FLUTTER_VERSION: '3.24.0'  # variable global a todo el workflow

jobs:
  test:
    env:
      SUPABASE_URL: ${{ secrets.SUPABASE_URL }}  # por job

    steps:
      - name: Run tests
        env:
          CI: true  # solo para este step
        run: flutter test
```

---

## 3. Matrix builds

Ejecutar el mismo job con diferentes configuraciones:

```yaml
jobs:
  test:
    strategy:
      matrix:
        flutter_version: ['3.22.0', '3.24.0']
        device: ['android', 'ios']
        exclude:
          - device: ios  # iOS no se puede testear en ubuntu

    runs-on: ${{ matrix.device == 'ios' && 'macos-latest' || 'ubuntu-latest' }}

    steps:
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ matrix.flutter_version }}

      - run: flutter test
```

**¿Qué genera?** 4 ejecuciones:
1. Flutter 3.22.0 + ubuntu
2. Flutter 3.22.0 + macos
3. Flutter 3.24.0 + ubuntu
4. Flutter 3.24.0 + macos

---

## 4. Path filtering

Ejecutar workflows solo cuando cambian ciertos archivos:

```yaml
on:
  push:
    paths:
      - 'supabase/**'
      - '.github/workflows/supabase-*'
      - '!supabase/seed.sql'  # excluir seeds
```

**Útil para monorepos:** No ejecutar tests de Flutter cuando solo cambia la web.

---

## 5. Entornos (deployment environments)

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # requiere aprobación manual
    steps:
      - run: make deploy
```

Los entornos permiten:
- **Aprobación manual** antes de deploy a producción
- **Protección de branches** (solo main puede deployar)
- **Variables y secrets por entorno** (staging vs production)

---

**Siguiente**: [06-monorepo-avanzado.md](./06-monorepo-avanzado.md) — Estrategias para monorepo
