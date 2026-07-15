# 09 - App Size Analysis

## ¿Qué es App Size Analysis?

Herramienta para analizar el tamaño de tu app Flutter en diferentes plataformas. Ayuda a identificar qué paquetes, assets, y código contribuyen al tamaño final.

---

## ¿Por qué importa el tamaño?

| Impacto | Descripción |
|---------|-------------|
| **Google Play** | Límite de 150MB para APKs descargables |
| **App Store** | Límite de 200MB para apps celulares |
| **First impression** | Usuarios borran apps grandes |
| **Download speed** | Apps grandes tardan más en descargar |
| **Storage** | Usuarios con poco espacio prefieren apps ligeras |

---

## Cómo generar App Size Analysis

### Android (AAB)
```bash
# Build app bundle
flutter build appbundle --analyze-size

# El reporte se genera en:
# build/app/outputs/bundle/release/app-release.aab
# build/app/outputs/flutter-size/snapshot-size.json
```

### iOS
```bash
# Build IPA
flutter build ipa --analyze-size

# El reporte se genera en:
# build/ios/ipa/Runner.ipa
# build/app/outputs/flutter-size/snapshot-size.json
```

### Web
```bash
# Build web
flutter build web --analyze-size
```

---

## App Size View en DevTools

### Cargar reporte
1. DevTools → App Size
2. Click en "Load Report"
3. Seleccionar `snapshot-size.json`
4. Ver análisis visual

### Estructura del reporte

```
Total App Size: 18.5 MB

├── Dart AOT (compiled code)
│   ├── lib (tu código): 3.2 MB (17.3%)
│   ├── packages (dependencias): 4.5 MB (24.3%)
│   │   ├── flutter: 1.8 MB
│   │   ├── supabase_flutter: 1.2 MB
│   │   ├── bloc: 0.3 MB
│   │   ├── go_router: 0.4 MB
│   │   ├── cached_network_image: 0.6 MB
│   │   └── other packages: 0.2 MB
│   └── dart SDK: 2.1 MB (11.4%)
├── Assets
│   ├── Images: 5.2 MB (28.1%)
│   │   ├── logo.png: 1.2 MB
│   │   ├── splash.png: 0.8 MB
│   │   └── product_images/: 3.2 MB
│   ├── Fonts: 1.8 MB (9.7%)
│   └── Other assets: 0.5 MB
└── Native libraries
    ├── libflutter.so: 1.2 MB (6.5%)
    └── libapp.so: 0.0 MB
```

---

## Análisis por categorías

### 1. Código Dart (AOT)

**Qué incluye:**
- Tu código (`lib/`)
- Dependencias (`packages/`)
- Dart SDK

**Cómo optimizar:**
```yaml
# pubspec.yaml - Solo incluir lo que usas
dependencies:
  # ❌ No importar paquetes completos
  # flutter/material.dart incluye TODO de Material
  
  # ✅ Importar solo lo necesario
  flutter:
    sdk: flutter
  
  # ✅ Usar packages ligeros
  # En lugar de http, usar dio con features específicas
```

### 2. Assets (imágenes)

**Qué incluye:**
- Imágenes en `assets/`
- Imágenes de paquetes
- Iconos

**Cómo optimizar:**
```yaml
# pubspec.yaml
flutter:
  assets:
    # ❌ No incluir directorio entero
    # - assets/images/  (incluye TODAS las imágenes)
    
    # ✅ Incluir solo las necesarias
    - assets/images/logo.png
    - assets/images/splash.png
```

```dart
// ✅ Usar imágenes de red en lugar de locales
// cuando no son críticas
Image.network('https://cdn.example.com/product.jpg')

// ✅ Para imágenes críticas, usar formato moderno
// Convertir PNGs a WebP (mejor compresión)
// Reducir resolución al tamaño real necesario
```

### 3. Fonts (fuentes)

**Qué incluye:**
- Fuentes en `assets/fonts/`
- Fuentes de paquetes

**Cómo optimizar:**
```yaml
# pubspec.yaml
flutter:
  fonts:
    # ❌ No incluir todas las variantes
    - family: Roboto
      fonts:
        - asset: assets/fonts/Roboto-Regular.ttf
        - asset: assets/fonts/Roboto-Medium.ttf
        - asset: assets/fonts/Roboto-Bold.ttf
        # 3 variantes × 200KB = 600KB
    
    # ✅ Solo incluir las que usas
    - family: Roboto
      fonts:
        - asset: assets/fonts/Roboto-Regular.ttf
        # 1 variante = 200KB
```

### 4. Native Libraries

**Qué incluye:**
- `libflutter.so` (Flutter engine)
- `libapp.so` (tu app compilada)
- Librerías nativas de plugins

**Optimización:**
- No se puede optimizar mucho (es el runtime de Flutter)
- Usar release mode para tamaño mínimo
- No usar plugins innecesarios

---

## Estrategias de reducción de tamaño

### Tree Shaking (eliminación de código no usado)

Flutter automáticamente elimina código no usado. Para maximizar:

```dart
// ❌ Importar todo el paquete
import 'package:flutter/material.dart';

// ✅ Importar solo lo necesario
import 'package:flutter/widgets.dart';
import 'package:flutter/painting.dart';
```

### Deferred Loading (carga diferida)

```dart
// Cargar pantallas pesadas solo cuando se necesitan
import 'package:heavy_feature/heavy_feature.dart' deferred as heavy;

ElevatedButton(
  onPressed: () async {
    await heavy.loadLibrary();  // Carga bajo demanda
    Navigator.push(context, MaterialPageRoute(
      builder: (_) => heavy.HeavyScreen(),
    ));
  },
  child: Text('Open Heavy Feature'),
)
```

### Shrinking (Android)

```groovy
// android/app/build.gradle
android {
    buildTypes {
        release {
            minifyEnabled true    // Shrink Java code
            shrinkResources true  // Shrink unused resources
            proguardFiles getDefaultProguardFile(
                'proguard-android-optimize.txt'
            ), 'proguard-rules.pro'
        }
    }
}
```

---

## Comparar versiones

### Antes vs Después

```
Version 1.0 (18.5 MB):
├── Dart AOT: 9.8 MB
├── Assets: 7.5 MB
└── Native: 1.2 MB

Version 1.1 (12.3 MB) - Optimizada:
├── Dart AOT: 6.2 MB (-3.6 MB)
│   └── Eliminados paquetes no usados
├── Assets: 4.9 MB (-2.6 MB)
│   ├── Imágenes convertidas a WebP
│   └── Fuentes reducidas
└── Native: 1.2 MB

Reducción: 33%
```

### Cómo comparar
1. Generar snapshot-size.json de versión A
2. Generar snapshot-size.json de versión B
3. Cargar ambos en DevTools
4. Comparar visualmente qué cambió

---

## Monitoreo continuo

### CI/CD pipeline

```yaml
# .github/workflows/size-check.yml
name: App Size Check

on:
  pull_request:
    branches: [main]

jobs:
  size-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - name: Build and analyze size
        run: |
          flutter pub get
          flutter build appbundle --analyze-size
      - name: Check size limit
        run: |
          SIZE=$(stat -f%z build/app/outputs/flutter-size/snapshot-size.json)
          if [ $SIZE -gt 20000000 ]; then
            echo "⚠️ App size increased! Current: $SIZE bytes"
            exit 1
          fi
```

### Métricas a trackear

| Métrica | Objetivo | Alerta si |
|---------|----------|-----------|
| Total size | < 15 MB | > 20 MB |
| Dart AOT | < 8 MB | > 10 MB |
| Assets | < 5 MB | > 8 MB |
| Imágenes | < 3 MB | > 5 MB |
| Paquetes | < 3 MB | > 5 MB |

---

## Ejercicios prácticos

### Ejercicio 1: Análisis de tu app

1. Build con `--analyze-size`
2. Cargar en DevTools
3. Identificar top 3 contribuyentes al tamaño
4. Proponer estrategias de reducción

### Ejercicio 2: Optimización de imágenes

1. Tomar todas las imágenes PNG del proyecto
2. Convertir a WebP con `cwebp`
3. Medir reducción de tamaño
4. Reemplazar en el proyecto

### Ejercicio 3: Análisis de dependencias

1. Ejecutar `dart pub deps`
2. Identificar paquetes más pesados
3. Evaluar si todos son necesarios
4. Eliminar los no esenciales

---
→ Siguiente: `10-cheatsheet-devtools.md`
