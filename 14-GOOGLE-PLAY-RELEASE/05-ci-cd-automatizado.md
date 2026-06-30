# 05 - CI/CD Automatizado

> Automatiza todo el pipeline de release: test → build → firma → subida a Play Console → publicación.

---

## 1. GitHub Actions para Release

### 1.1 Workflow Completo

```yaml
# .github/workflows/release.yml

name: Build and Release

on:
  push:
    tags:
      - 'v*'  # Ej: v1.2.0, v1.3.1

jobs:
  build-and-release:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version-file: apps/mobile/.fvm/flutter_sdk_version

      - name: Get dependencies
        working-directory: apps/mobile
        run: flutter pub get

      - name: Run tests
        working-directory: apps/mobile
        run: flutter test

      - name: Decode keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode \
            > apps/mobile/android/app/upload-keystore.jks

      - name: Create key.properties
        run: |
          echo "storePassword=${{ secrets.KEYSTORE_PASSWORD }}" \
            > apps/mobile/android/key.properties
          echo "keyPassword=${{ secrets.KEY_PASSWORD }}" \
            >> apps/mobile/android/key.properties
          echo "keyAlias=upload" \
            >> apps/mobile/android/key.properties
          echo "storeFile=upload-keystore.jks" \
            >> apps/mobile/android/key.properties

      - name: Build AAB
        working-directory: apps/mobile
        run: flutter build appbundle --release

      - name: Sign AAB
        uses: r0adkll/sign-android-release@v1
        with:
          releaseDirectory: apps/mobile/build/app/outputs/bundle/release
          signingKeyBase64: ${{ secrets.KEYSTORE_BASE64 }}
          alias: ${{ secrets.KEY_ALIAS }}
          keyStorePassword: ${{ secrets.KEYSTORE_PASSWORD }}
          keyPassword: ${{ secrets.KEY_PASSWORD }}

      - name: Upload to Play Console
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}
          packageName: com.tuapp.rifagestion
          releaseFiles: apps/mobile/build/app/outputs/bundle/release/app-release.aab
          track: production
          status: completed
          inAppUpdatePriority: 2
          whatsNewDirectory: apps/mobile/android/whatsnew
```

### 1.2 Secrets Necesarios

| Secret | Descripción |
|--------|-------------|
| `KEYSTORE_BASE64` | Keystore codificado en base64 |
| `KEYSTORE_PASSWORD` | Contraseña del keystore |
| `KEY_PASSWORD` | Contraseña de la clave |
| `KEY_ALIAS` | Alias de la clave |
| `PLAY_SERVICE_ACCOUNT_JSON` | JSON de cuenta de servicio de Google Play |

---

## 2. Configurar Service Account

### 2.1 Crear Cuenta de Servicio

```
Google Cloud Console > IAM > Cuentas de servicio
├── Crear cuenta de servicio
│   ├── Nombre: "github-actions-release"
│   └── Rol: "Service Account User"
└── Crear clave JSON
    └── Descargar JSON (guardar como secret)
```

### 2.2 Vincular con Play Console

```
Play Console > Configuración > Usuarios y permisos
├── Invitar usuario (email de la service account)
├── Rol: "Administrador de versiones"
└── Acceso a: app específica
```

### 2.3 Agregar JSON como Secret

```bash
cat service-account.json | pbcopy  # Copiar contenido
# GitHub > Repo > Settings > Secrets > New secret
# Name: PLAY_SERVICE_ACCOUNT_JSON
# Value: pegar contenido JSON
```

---

## 3. Automatización Incremental de Versión

### 3.1 Script de Versión

```bash
#!/bin/bash
# scripts/bump_version.sh

# Leer versión actual de pubspec.yaml
VERSION=$(grep 'version:' apps/mobile/pubspec.yaml | awk '{print $2}')
BUILD_NUMBER=$(echo $VERSION | cut -d'+' -f2)
NEW_BUILD=$((BUILD_NUMBER + 1))
NEW_VERSION=$(echo $VERSION | cut -d'+' -f1)+$NEW_BUILD

# Actualizar pubspec.yaml
sed -i "s/version: $VERSION/version: $NEW_VERSION/" apps/mobile/pubspec.yaml

echo "Version bumped: $VERSION → $NEW_VERSION"
```

### 3.2 GitHub Actions con Bump Automático

```yaml
name: Create Release

on:
  workflow_dispatch:
    inputs:
      version_type:
        description: 'Tipo de versión'
        required: true
        default: 'patch'
        type: choice
        options:
          - patch  # 1.0.0 → 1.0.1
          - minor  # 1.0.0 → 1.1.0
          - major  # 1.0.0 → 2.0.0

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Bump version
        run: |
          git config user.email "ci@example.com"
          git config user.name "CI Bot"
          npm run release -- --release-as ${{ inputs.version_type }}
          git push --follow-tags

      # ... build + sign + upload steps ...
```

---

## 4. What's New Automático

### 4.1 Script para Generar Novedades

```bash
#!/bin/bash
# scripts/generate_whatsnew.sh

# Obtener commits desde el último tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD~10")
echo "Generando novedades desde $LAST_TAG..."

git log $LAST_TAG..HEAD --pretty=format:"%s" | while read line; do
  case $line in
    feat*)
      echo "✨ $line" ;;
    fix*)
      echo "🐛 $line" ;;
    perf*)
      echo "⚡ $line" ;;
    *)
      echo "🔧 $line" ;;
  esac
done
```

### 4.2 Estructura de what's new

```
android/whatsnew/
├── whatsnew-en-US      # Inglés
└── whatsnew-es-ES      # Español
```

```
# whatsnew-es-ES
✨ Nueva función: exportación de resultados a PDF
🐛 Corregido: crash al abrir sorteo sin conexión
⚡ Mejora: carga 40% más rápida en listas grandes
```

---

## 5. CI/CD para Internal Testing

```yaml
name: Internal Test

on:
  push:
    branches: [develop]

jobs:
  internal-test:
    runs-on: ubuntu-latest
    steps:
      # ... setup, test, build ...

      - name: Upload to Internal Track
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}
          packageName: com.tuapp.rifagestion
          releaseFiles: build/app/outputs/bundle/release/app-release.aab
          track: internal
          status: completed
```

**Cada push a develop crea un build interno automático.** El equipo siempre tiene la última versión para probar.

---

## 6. Fastlane (Alternativa)

```ruby
# fastlane/Fastfile
default_platform(:android)

platform :android do
  desc "Build and deploy to internal testing"
  lane :internal do
    gradle(task: "clean")
    gradle(task: "bundleRelease")
    upload_to_play_store(
      track: 'internal',
      release_status: 'completed',
    )
  end

  desc "Deploy to production"
  lane :production do
    gradle(task: "clean")
    gradle(task: "bundleRelease")
    upload_to_play_store(
      track: 'production',
      release_status: 'inProgress',
      rollout: '0.2',  # 20% rollout
    )
  end
end
```

---

## 7. Monitoreo de Releases

### 7.1 Crashlytics

```yaml
# pubspec.yaml
dependencies:
  firebase_crashlytics: ^4.0.0
  firebase_analytics: ^11.0.0
```

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  // Configurar Crashlytics
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;

  runApp(const MyApp());
}
```

### 7.2 Performance Monitoring

```yaml
dependencies:
  firebase_performance: ^0.10.0
```

### 7.3 Alertas de Crash

```
Firebase Console > Crashlytics > Alertas
├── Configurar alerta por email
│   ├── Crash rate > 0.01% en la última hora
│   └── Nuevo crash en release reciente
└── Notificar a: equipo@email.com, Slack webhook
```

---

## 8. Resumen

1. **GitHub Actions** automatiza test + build + firma + subida
2. **Secrets** guardan keystore y cuentas de servicio
3. **Service Account** permite subir a Play Console desde CI
4. **Internal track** para cada push a develop
5. **Production** con rollout gradual (20% → 100%)
6. **Crashlytics** para monitorear releases en producción
7. **Fastlane** es alternativa a GitHub Actions

---

## Recursos

- [r0adkll/sign-android-release](https://github.com/r0adkll/sign-android-release)
- [r0adkll/upload-google-play](https://github.com/r0adkll/upload-google-play)
- [Fastlane Android](https://docs.fastlane.tools/getting-started/android/setup/)
- [Google Play Publisher API](https://developers.google.com/android-publisher)
- [Firebase Crashlytics](https://firebase.google.com/docs/crashlytics)
