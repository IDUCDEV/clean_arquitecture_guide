# 🚀 Nivel Experto: Flutter Gen - Assets, Splash, Iconos y Localización

> Flutter tiene un sistema de generación de código integrado para assets, localización y configuración visual. Este archivo cubre las 4 herramientas esenciales que todo proyecto profesional usa.

---

## 1. `flutter: generate: true` y Asset Manifest

### 1.1 El Sistema de Assets de Flutter

Flutter tiene un sistema built-in de generación de código para assets. Se activa con una línea:

```yaml
# pubspec.yaml
flutter:
  generate: true   # Activa la generación automática
```

Esto hace que Flutter genere automáticamente:
- Asset manifest (para imágenes, fuentes, etc.)
- Soporte para `flutter gen-l10n` (localización)

### 1.2 Cómo Funciona

```yaml
# pubspec.yaml
flutter:
  generate: true

  assets:
    - assets/images/
    - assets/fonts/
    - assets/icons/
    - assets/data/
```

Con `generate: true`, Flutter genera un `AssetManifest` interno que permite acceder a assets de forma tipada.

### 1.3 flutter_gen (Terceros)

El paquete `flutter_gen` de la comunidad va un paso más allá: genera clases Dart con referencias tipadas a cada asset.

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_gen_runner: ^5.4.0
```

```yaml
# flutter_gen.yaml (raíz del proyecto)
flutter_gen:
  output: lib/core/gen/
  line_length: 120

  integrations:
    flutter_svg: true
    flare_flutter: true
    rive: true
    lottie: true
```

**Uso:**

```dart
// Sin flutter_gen (strings mágicas)
Image.asset('assets/images/logo.png');

// Con flutter_gen (tipado, autocompletado)
Image.asset(Assets.images.logo);
```

### 1.4 Estructura de Assets Recomendada

```
assets/
├── images/
│   ├── logo.png
│   ├── logo@2x.png
│   └── background.jpg
├── icons/
│   ├── home.svg
│   └── settings.svg
├── fonts/
│   ├── Inter-Regular.ttf
│   └── Inter-Bold.ttf
├── animations/
│   ├── loading.json        # Lottie
│   └── splash.riv          # Rive
└── data/
    └── default_config.json
```

---

## 2. flutter_native_splash

### 2.1 ¿Qué es?

Genera la pantalla de splash nativa (Android/iOS) desde una configuración YAML, sin código manual.

### 2.2 Instalación y Configuración

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_native_splash: ^2.4.0
```

```yaml
# flutter_native_splash.yaml
flutter_native_splash:
  # Colores
  color: "#FFFFFF"
  background_image: "assets/images/splash_background.png"

  # Logo
  image: "assets/images/splash_logo.png"
  image_dark: "assets/images/splash_logo_dark.png"

  # Modo oscuro
  color_dark: "#121212"
  android_dark: true
  ios_dark: true

  # Branding (texto debajo del logo)
  branding: "Powered by YourCompany"
  branding_color: "#666666"
  branding_bottom: 30

  # Android
  android: true
  android_gravity: center
  android_screen_orientation: portrait

  # iOS
  ios: true  # Usa LaunchScreen.storyboard automáticamente
  ios_content_mode: center

  # Web
  web: false

  # Fullscreen
  fullscreen: true
```

### 2.3 Comandos

```bash
# Generar splash
dart run flutter_native_splash:create

# Eliminar splash
dart run flutter_native_splash:remove
```

### 2.4 Integración con Makefile

```makefile
.PHONY: splash

splash:
	@echo "Generando splash screen..."
	@dart run flutter_native_splash:create
```

---

## 3. flutter_launcher_icons

### 3.1 ¿Qué es?

Genera los iconos de launcher para todas las plataformas desde una imagen fuente.

### 3.2 Configuración

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_launcher_icons: ^0.13.0
```

```yaml
# flutter_launcher_icons.yaml
flutter_launcher_icons:
  android: true
  ios: true
  image_path: "assets/icons/app_icon.png"

  # Android específico
  adaptive_icon_background: "assets/icons/icon_background.png"
  adaptive_icon_foreground: "assets/icons/icon_foreground.png"
  adaptive_icon_foreground_inset: 20
  adaptive_icon_monochrome: "assets/icons/icon_monochrome.png"

  # iOS específico
  remove_alpha_ios: true
  image_path_ios: "assets/icons/app_icon_ios.png"

  # Web
  web:
    generate: true
    image_path: "assets/icons/app_icon.png"
    favicon: true

  # Windows
  windows:
    generate: true
    image_path: "assets/icons/app_icon.png"
    icon_size: 48

  # MacOS
  macos:
    generate: true
    image_path: "assets/icons/app_icon.png"
```

### 3.3 Comandos

```bash
# Generar iconos
dart run flutter_launcher_icons

# Con archivo de configuración específico
dart run flutter_launcher_icons -f flutter_launcher_icons.yaml
```

### 3.4 Múltiples Flavors

```yaml
# flutter_launcher_icons-dev.yaml
flutter_launcher_icons:
  image_path: "assets/icons/app_icon_dev.png"
  android: true
  ios: true

# flutter_launcher_icons-prod.yaml
flutter_launcher_icons:
  image_path: "assets/icons/app_icon_prod.png"
  android: true
  ios: true
```

```bash
# Generar para cada flavor
dart run flutter_launcher_icons -f flutter_launcher_icons-dev.yaml
dart run flutter_launcher_icons -f flutter_launcher_icons-prod.yaml
```

---

## 4. Flutter Gen-L10n (Localización)

### 4.1 Configuración

```yaml
# l10n.yaml
arb-dir: lib/l10n/arb
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-dir: lib/l10n/gen
nullable-getter: false
header: "// dart format off\n// coverage:ignore-file"
```

```yaml
# pubspec.yaml (necesario para que l10n.yaml sea detectado)
flutter:
  generate: true
```

### 4.2 Archivos ARB

**app_en.arb** (template):
```json
{
  "@@locale": "en",
  "appName": "Rifa Gestion",
  "@appName": {
    "description": "The application name"
  },

  "welcome": "Welcome to {appName}",
  "@welcome": {
    "description": "Welcome message",
    "placeholders": {
      "appName": {
        "type": "String"
      }
    }
  },

  "itemsCount": "{count, plural, =0{No items} one{1 item} other{{count} items}}",
  "@itemsCount": {
    "description": "Item count with pluralization",
    "placeholders": {
      "count": {
        "type": "int"
      }
    }
  },

  "greeting": "{gender, select, male{Hello sir} female{Hello madam} other{Hello}}",
  "@greeting": {
    "description": "Gender-based greeting",
    "placeholders": {
      "gender": {
        "type": "String"
      }
    }
  }
}
```

**app_es.arb** (traducción):
```json
{
  "@@locale": "es",
  "appName": "Rifa Gestion",

  "welcome": "Bienvenido a {appName}",

  "itemsCount": "{count, plural, =0{Sin items} one{1 item} other{{count} items}}",

  "greeting": "{gender, select, male{Hola señor} female{Hola señora} other{Hola}}"
}
```

### 4.3 Uso en Código

```dart
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(title: Text(l10n.appName)),
      body: Center(
        child: Column(
          children: [
            Text(l10n.welcome('Rifa Gestion')),
            Text(l10n.itemsCount(5)),  // "5 items"
            Text(l10n.greeting('male')),  // "Hola señor"
          ],
        ),
      ),
    );
  }
}
```

### 4.4 Extension para Conveniencia

```dart
// lib/core/extensions/localization_ext.dart
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

extension AppLocalizationsX on BuildContext {
  AppLocalizations get l10n => AppLocalizations.of(this)!;
}

// Uso: context.l10n.appName
```

### 4.5 Estructura de ARB Files

```
lib/l10n/
├── arb/
│   ├── app_en.arb        # Template (obligatorio)
│   ├── app_es.arb        # Español
│   ├── app_pt.arb        # Portugués
│   └── app_fr.arb        # Francés
├── gen/                   # GENERADO (en .gitignore)
│   ├── app_localizations.dart
│   ├── app_localizations_en.dart
│   └── app_localizations_es.dart
└── extensions/
    └── localization_ext.dart
```

### 4.6 analysis_options.yaml

```yaml
analyzer:
  exclude:
    - lib/l10n/gen/*
```

### 4.7 .gitignore

```gitignore
# Generated l10n files
lib/l10n/gen/
```

---

## 5. Integración en el Proyecto Real

En el monorepo, la configuración de localización está activa:

```yaml
# l10n.yaml
arb-dir: lib/l10n/arb
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-dir: lib/l10n/gen
nullable-getter: false
header: "// dart format off\n// coverage:ignore-file"
```

Con `flutter: generate: true` en pubspec.yaml, el sistema:
1. Lee los archivos `.arb` en `lib/l10n/arb/`
2. Genera clases Dart tipadas en `lib/l10n/gen/`
3. Provee `AppLocalizations.of(context)` con autocompletado
4. Soporta pluralización y género
5. Cambia idioma automáticamente según el locale del dispositivo

---

## 6. Flujo de Trabajo Completo

### 6.1 Setup Inicial

```bash
# 1. Activar generación de assets
# Agregar a pubspec.yaml:
#   flutter:
#     generate: true

# 2. Configurar l10n
touch l10n.yaml

# 3. Crear estructura de ARB
mkdir -p lib/l10n/arb
touch lib/l10n/arb/app_en.arb

# 4. Agregar flutter_native_splash
flutter pub add dev:flutter_native_splash
touch flutter_native_splash.yaml
dart run flutter_native_splash:create

# 5. Agregar flutter_launcher_icons
flutter pub add dev:flutter_launcher_icons
touch flutter_launcher_icons.yaml
dart run flutter_launcher_icons

# 6. (Opcional) flutter_gen para assets tipados
flutter pub add dev:flutter_gen_runner
touch flutter_gen.yaml
```

### 6.2 Día a Día

```bash
# Agregar nuevo texto
# 1. Editar app_en.arb y app_es.arb
# 2. Ejecutar:
flutter gen-l10n
# 3. Usar en código: context.l10n.nuevoTexto
```

---

## 7. Resumen Ejecutivo

| Herramienta | Archivo Config | Comando | Genera |
|-------------|---------------|---------|--------|
| Assets | `pubspec.yaml` | `flutter build` | AssetManifest |
| flutter_gen | `flutter_gen.yaml` | `build_runner` | Clases tipadas |
| Splash | `flutter_native_splash.yaml` | `dart run flutter_native_splash:create` | Native screens |
| Iconos | `flutter_launcher_icons.yaml` | `dart run flutter_launcher_icons` | App icons |
| Localización | `l10n.yaml` | `flutter gen-l10n` | Clases de traducción |

**Reglas de oro:**
1. `generate: true` activa todo el ecosistema
2. Los ARB files son el estándar de localización
3. Los archivos generados (`gen/`) van en `.gitignore`
4. El splash nativo es configuración, no código

---

## Recursos Adicionales

- [flutter_native_splash pub.dev](https://pub.dev/packages/flutter_native_splash)
- [flutter_launcher_icons pub.dev](https://pub.dev/packages/flutter_launcher_icons)
- [flutter_gen pub.dev](https://pub.dev/packages/flutter_gen)
- [Flutter Internationalization Guide](https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization)
- [ARB Format Specification](https://github.com/google/app-resource-bundle)

---

## Ver también

- [`07-retrofit-api-client.md`](./07-retrofit-api-client.md) — Clientes HTTP con Retrofit
- [`15-DISEÑO-RESPONSIVO`](../15-DISEÑO-RESPONSIVO/README.md) — Diseño responsivo y adaptativo

---

## En el siguiente módulo

**→ [09-dart3-pattern-matching-nativo.md](./09-dart3-pattern-matching-nativo.md)** — Dart 3 Pattern Matching nativo
