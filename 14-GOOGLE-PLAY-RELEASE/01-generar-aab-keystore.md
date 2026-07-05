# 01 - Generar AAB y Keystore

> El Android App Bundle (AAB) es el formato de publicación oficial de Google Play. Aquí te enseño a generarlo con la firma correcta.

---

## 1. ¿Qué es un AAB?

| Formato | Propósito | Tamaño | Play Store |
|---------|-----------|--------|------------|
| **APK** | Instalación directa | Grande | Obsoleto para nuevas apps |
| **AAB** | Publicación en Play Store | 60% más pequeño | Requerido desde 2021 |
| **APK universal** | Testing manual | Mediano | No para producción |

**El AAB permite que Google Play genere APKs optimizadas para cada dispositivo:**
- Solo los recursos necesarios para esa densidad de pantalla
- Solo el código nativo para esa arquitectura (arm64, x86)
- Hasta 60% menos tamaño de descarga

---

## 2. Generar Keystore

### 2.1 ¿Qué es un Keystore?

Es el archivo que contiene la clave privada para firmar tu app. **Si lo pierdes, no puedes actualizar tu app en Play Store.**

### 2.2 Crear Keystore

```bash
# Generar keystore (una sola vez, guardarlo para siempre)
keytool -genkey -v -keystore upload-keystore.jks \
  -storetype JKS \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias upload

# Te pedirá:
# - Contraseña del keystore (GUARDAR)
# - Contraseña de la clave (GUARDAR)
# - Nombre, organización, ubicación
```

### 2.3 Alternativa: Android Studio

1. Build → Generate Signed App Bundle / APK
2. Crear nuevo keystore
3. Guardar en lugar seguro (no en el repo)

---

## 3. Configurar Firma en el Proyecto

### 3.1 key.properties

```properties
# android/key.properties
storePassword=tu-contraseña-keystore
keyPassword=tu-contraseña-clave
keyAlias=upload
storeFile=../upload-keystore.jks
```

### 3.2 build.gradle (Module: app)

```gradle
// android/app/build.gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    // ... config existente ...

    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            // ...
        }
    }
}
```

---

## 4. Generar AAB

### 4.1 Comando Básico

```bash
# Generar AAB firmado para release
flutter build appbundle --release

# Output:
# build/app/outputs/bundle/release/app-release.aab
```

### 4.2 Con Flavor

```bash
# Si usas flavors
flutter build appbundle --release --flavor production
flutter build appbundle --release --flavor development

# Output:
# build/app/outputs/bundle/productionRelease/app-production-release.aab
# build/app/outputs/bundle/developmentRelease/app-development-release.aab
```

### 4.3 Verificar el AAB

```bash
# Verificar que el AAB está firmado
jarsigner -verify -verbose -certs build/app/outputs/bundle/release/app-release.aab

# Verificar versión
aapt2 dump badging build/app/outputs/bundle/release/app-release.aab | grep version
```

### 4.4 Makefile

```makefile
.PHONY: build-aab build-apk

build-aab:
	@echo "Generando AAB de producción..."
	@cd apps/mobile && flutter build appbundle --release

build-aab-dev:
	@echo "Generando AAB de desarrollo..."
	@cd apps/mobile && flutter build appbundle --release --flavor development

build-apk:
	@echo "Generando APK universal..."
	@cd apps/mobile && flutter build apk --release

build-apk-split:
	@echo "Generando APKs por abi..."
	@cd apps/mobile && flutter build apk --release --split-per-abi
```

---

## 5. Generar APK Universal (para Testing)

```bash
# APK universal (contiene todas las arquitecturas)
flutter build apk --release

# APKs divididas por arquitectura
flutter build apk --release --split-per-abi
# Output:
#   app-arm64-v8a-release.apk
#   app-armeabi-v7a-release.apk
#   app-x86_64-release.apk
```

---

## 6. Seguridad del Keystore

### 6.1 Qué NO hacer

```bash
# ❌ NO comitar el keystore en el repo
git add upload-keystore.jks  # MAL

# ❌ NO comitar key.properties con contraseñas
git add android/key.properties  # MAL

# ❌ NO poner contraseñas en build.gradle
```

### 6.2 Qué SÍ hacer

```gitignore
# .gitignore
android/key.properties
*.jks
*.keystore
```

```bash
# Guardar keystore en:
# 1. Gestor de contraseñas (1Password, Bitwarden)
# 2. Backup en disco externo
# 3. CI/CD secrets (GitHub Actions secrets)
```

### 6.3 CI/CD con Secrets

```yaml
# .github/workflows/release.yml
- name: Decode keystore
  run: |
    echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > android/app/upload-keystore.jks
    echo "storePassword=${{ secrets.KEYSTORE_PASSWORD }}" > android/key.properties
    echo "keyPassword=${{ secrets.KEY_PASSWORD }}" >> android/key.properties
    echo "keyAlias=upload" >> android/key.properties
    echo "storeFile=upload-keystore.jks" >> android/key.properties
```

---

## 7. Actualizar Versión

### 7.1 pubspec.yaml

```yaml
version: 1.2.0+3
#       ^^^^^ ^
#       |     +-- build number (siempre incrementar)
#       +-------- version name (visible al usuario)
```

### 7.2 Incrementar Build Number

```bash
# Script para incrementar build number automáticamente
# En pubspec.yaml: version: 1.2.0+3
# Después del script: version: 1.2.0+4
```

---

## 8. Resumen

1. **Keystore** = la llave de tu app. NUNCA perderla
2. **AAB** es el formato obligatorio para Play Store
3. **`flutter build appbundle --release`** genera el archivo
4. **key.properties** configura la firma (no comitar)
5. **Build number** incrementar en cada release
6. **Guardar keystore** en gestor de contraseñas + CI/CD

---

## Recursos

- [Android App Bundle](https://developer.android.com/platform/technology/app-bundle)
- [Flutter Build Guide](https://docs.flutter.dev/deployment/android)
- [keytool documentation](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/keytool.html)

---

## 📚 Referencias

- [Flutter | Android deployment](https://docs.flutter.dev/deployment/android) — Guía oficial para publicar en Play Store
- [Google Play | Console Help](https://support.google.com/googleplay/android-developer) — Centro de ayuda de Google Play Console
- [Flutter | Build and release](https://docs.flutter.dev/deployment) — Compilación para múltiples plataformas

---
