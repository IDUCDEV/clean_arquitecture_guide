# 02 - Workflows de GitHub Actions

> Colección de templates de workflows de GitHub Actions para automatizar tu flujo de desarrollo Flutter + Supabase.

---

## 1. CI Quality (Análisis + Tests)

```yaml
# .github/workflows/ci-quality.yml
name: CI - Quality Gate

on:
  push:
    branches: [dev, main]
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  quality-gate:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.24.0'
      
      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.pub-cache
          key: ${{ runner.os }}-flutter-${{ hashFiles('**/pubspec.lock') }}
      
      - name: Check Formatting
        run: dart format --output=none --set-exit-if-changed .
      
      - name: Analyze
        run: flutter analyze
      
      - name: Test with Coverage
        run: flutter test --coverage
      
      - name: SonarCloud
        if: ${{ env.SONAR_TOKEN != '' }}
        uses: SonarSource/sonarcloud-github-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

---

## 2. Supabase Tests

```yaml
# .github/workflows/supabase-tests.yml
name: CI - Supabase Tests

on:
  pull_request:
    paths: [supabase/**]
  push:
    branches: [dev, main]
    paths: [supabase/**]

jobs:
  supabase-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Supabase CLI
        uses: supabase/setup-cli@v1
        with:
          version: latest
      
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

## 3. Supabase Dev Sync

```yaml
# .github/workflows/supabase-dev.yml
name: CI - Supabase Dev Sync

on:
  push:
    branches: [dev]

jobs:
  apply-migrations:
    runs-on: ubuntu-latest
    
    env:
      SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
      SUPABASE_PROJECT_ID: ${{ secrets.SUPABASE_PROJECT_ID }}
      SUPABASE_DB_PASSWORD: ${{ secrets.SUPABASE_DB_PASSWORD }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Detect changes
        id: changes
        run: |
          if git diff --quiet "${{ github.event.before }}" "${{ github.sha }}" -- supabase/migrations/; then
            echo "changed=false" >> "$GITHUB_OUTPUT"
          else
            echo "changed=true" >> "$GITHUB_OUTPUT"
          fi
      
      - name: Install CLI
        uses: supabase/setup-cli@v1
        if: steps.changes.outputs.changed == 'true'
      
      - name: Link project
        run: supabase link --project-ref "$SUPABASE_PROJECT_ID" --password "$SUPABASE_DB_PASSWORD"
        if: steps.changes.outputs.changed == 'true'
      
      - name: Lint
        run: supabase db lint --linked --fail-on error
        if: steps.changes.outputs.changed == 'true'
      
      - name: Push
        run: supabase db push --linked --password "$SUPABASE_DB_PASSWORD" --yes
        if: steps.changes.outputs.changed == 'true'
```

---

## 4. Android Release

```yaml
# .github/workflows/flutter-android-release.yml
name: Release - Android Build

on:
  push:
    tags: ["v*"]

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
      
      - name: Build APK
        run: |
          flutter build apk --release \
            --dart-define=SUPABASE_URL=${{ secrets.SUPABASE_URL }} \
            --dart-define=SUPABASE_PUBLISHABLE_KEY=${{ secrets.SUPABASE_PUBLISHABLE_KEY }}
      
      - name: Build AAB
        run: flutter build appbundle --release
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            build/app/outputs/flutter-apk/app-release.apk
            build/app/outputs/bundle/release/app-release.aab
```

---

## 5. PR Title Lint

```yaml
# .github/workflows/pr-title-lint.yml
name: CI - PR Title Lint

on: pull_request

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: amannn/action-semantic-pull-request@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 6. Secrets requeridos

| Secret | Dónde obtenerlo |
|--------|-----------------|
| `SUPABASE_URL` | Dashboard → Settings → General |
| `SUPABASE_PUBLISHABLE_KEY` | Dashboard → Settings → API → Publishable Key (antes `anon key`) |
| `SUPABASE_ACCESS_TOKEN` | `supabase auth token` |
| `SUPABASE_PROJECT_ID` | Dashboard → Settings → General |
| `SUPABASE_DB_PASSWORD` | Al crear proyecto |
| `SONAR_TOKEN` | SonarCloud |

---

**Siguiente**: [03-patrones-extrapolables.md](./03-patrones-extrapolables.md)