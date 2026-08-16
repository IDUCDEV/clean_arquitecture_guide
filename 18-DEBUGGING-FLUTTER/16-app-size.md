# 16 — App Size: Analizando el Tamaño del Bundle

> Medir el tamaño de tu app por plataforma, cargar el reporte en DevTools y reducir los principales contribuyentes.

---

## 1. ¿Qué es App Size Analysis?

Herramienta para analizar el tamaño de tu app Flutter en diferentes plataformas. Ayuda a identificar qué paquetes, assets y código contribuyen al tamaño final.

---

## 2. ¿Por qué importa el tamaño?

| Impacto | Descripción |
|---|---|
| **Google Play** | Límite de 200 MB por AAB |
| **App Store** | Binario hasta 2 GB; >200 MB no se descarga por datos móviles |
| **Primera impresión** | Los usuarios borran apps grandes |
| **Velocidad de descarga** | Apps grandes tardan más en descargar |
| **Almacenamiento** | Usuarios con poco espacio prefieren apps ligeras |

---

## 3. Cómo generar el análisis de tamaño

### 3.1 Android (AAB)

```bash
# Build app bundle
flutter build appbundle --analyze-size

# El reporte se genera en:
# build/app/outputs/bundle/release/app-release.aab
# build/app/outputs/flutter-size/snapshot-size.json
```

### 3.2 iOS

```bash
# Build IPA
flutter build ipa --analyze-size

# El reporte se genera en:
# build/ios/ipa/Runner.ipa
# build/app/outputs/flutter-size/snapshot-size.json
```

### 3.3 Web / Desktop

```bash
# Build web
flutter build web --analyze-size

# Build desktop
flutter build linux --analyze-size
flutter build windows --analyze-size
flutter build macos --analyze-size
```

---

## 4. App Size View en DevTools

### 4.1 Cargar el reporte

1. DevTools → App Size
2. Click en **Load Report**
3. Seleccionar `snapshot-size.json`
4. Ver el análisis visual

### 4.2 Estructura del reporte

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

## 5. Análisis por categorías

### 5.1 Código Dart (AOT)

**Qué incluye:**
- Tu código (`lib/`)
- Dependencias (`packages/`)
- Dart SDK

**Cómo optimizar:**

```yaml
# pubspec.yaml - Solo incluir lo que usas
dependencies:
  # ❌ No importar paquetes completos si no los usas
  # ✅ Usar packages ligeros y específicos
```

### 5.2 Assets (imágenes)

**Qué incluye:**
- Imágenes en `assets/`
- Imágenes de paquetes
- Iconos

**Cómo optimizar:**

```yaml
# pubspec.yaml
flutter:
  assets:
    # ❌ No incluir directorios enteros
    # - assets/images/

    # ✅ Incluir solo las necesarias
    - assets/images/logo.png
    - assets/images/splash.png
```

```dart
// ✅ Usar imágenes de red en lugar de locales cuando no son críticas
Image.network('https://cdn.example.com/product.jpg')

// ✅ Para imágenes críticas, usar formatos modernos
// Convertir PNGs a WebP (mejor compresión)
// Reducir resolución al tamaño real necesario
```

### 5.3 Fonts (fuentes)

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

### 5.4 Native Libraries

**Qué incluye:**
- `libflutter.so` (Flutter engine)
- `libapp.so` (tu app compilada)
- Librerías nativas de plugins

**Optimización:**
- Poco que optimizar: es el runtime de Flutter
- Usar release mode para tamaño mínimo
- No usar plugins innecesarios

---

## 6. Estrategias de reducción de tamaño

### 6.1 Tree shaking (eliminación de código no usado)

Flutter elimina automáticamente el código no usado en release. Para maximizarlo:

```dart
// ❌ Importar todo el paquete
import 'package:flutter/material.dart';

// ✅ Importar solo lo necesario
import 'package:flutter/widgets.dart';
import 'package:flutter/painting.dart';
```

### 6.2 Deferred loading (carga diferida)

```dart
// Cargar librerías pesadas solo cuando se necesitan (soporte en web)
import 'package:heavy_feature/heavy_feature.dart' deferred as heavy;

ElevatedButton(
  onPressed: () async {
    await heavy.loadLibrary();  // Carga bajo demanda
    Navigator.push(context, MaterialPageRoute(
      builder: (_) => heavy.HeavyScreen(),
    ));
  },
  child: const Text('Open Heavy Feature'),
)
```

> Los `deferred` imports solo aplican para web; en Android/iOS el código se compila completo (AOT).

### 6.3 Shrinking (Android)

```groovy
// android/app/build.gradle
android {
    buildTypes {
        release {
            minifyEnabled true    // Shrink Java/Kotlin code
            shrinkResources true  // Shrink unused resources
            proguardFiles getDefaultProguardFile(
                'proguard-android-optimize.txt'
            ), 'proguard-rules.pro'
        }
    }
}
```

---

## 7. Comparar versiones

### 7.1 Antes vs Después

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

### 7.2 Cómo comparar

1. Generar `snapshot-size.json` de la versión A
2. Generar `snapshot-size.json` de la versión B
3. Cargar ambos en DevTools
4. Comparar visualmente qué cambió

---

## 8. Monitoreo continuo

### 8.1 CI/CD pipeline

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
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - name: Build and analyze size
        run: |
          flutter pub get
          flutter build appbundle --analyze-size
      - name: Check size limit
        run: |
          SIZE=$(stat -c%s build/app/outputs/flutter-size/snapshot-size.json)
          if [ $SIZE -gt 20000000 ]; then
            echo "⚠️ App size increased! Current: $SIZE bytes"
            exit 1
          fi
```

### 8.2 Métricas a monitorear

| Métrica | Objetivo | Alerta si |
|---|---|---|
| Total size | < 15 MB | > 20 MB |
| Dart AOT | < 8 MB | > 10 MB |
| Assets | < 5 MB | > 8 MB |
| Imágenes | < 3 MB | > 5 MB |
| Paquetes | < 3 MB | > 5 MB |

---

## 9. Ejercicios prácticos

### 9.1 Ejercicio 1: análisis de tu app

1. Build con `--analyze-size`
2. Cargar en DevTools
3. Identificar el top 3 de contribuyentes al tamaño
4. Proponer estrategias de reducción

### 9.2 Ejercicio 2: optimización de imágenes

1. Tomar todas las imágenes PNG del proyecto
2. Convertir a WebP con `cwebp`
3. Medir la reducción de tamaño
4. Reemplazar en el proyecto

### 9.3 Ejercicio 3: análisis de dependencias

1. Ejecutar `dart pub deps`
2. Identificar los paquetes más pesados
3. Evaluar si todos son necesarios
4. Eliminar los no esenciales

---

## Resumen

| Concepto | Punto clave |
|---|---|
| `--analyze-size` | Genera `snapshot-size.json` |
| Reporte | Código AOT, assets, fuentes, librerías nativas |
| Estrategias | Tree shaking, WebP, fuentes mínimas, plugins justos |
| Deferred | Solo web (no Android/iOS) |
| Monitoreo | CI con umbral de tamaño |

---

## 📚 Referencias

- [Flutter | App size view](https://docs.flutter.dev/tools/devtools/app-size) — Documentación oficial de App Size
- [Flutter | Building your app](https://docs.flutter.dev/deployment/build) — Comandos de build por plataforma
- [Flutter | Optimizing performance](https://docs.flutter.dev/perf/rendering) — Reducción de tamaño y rendimiento

---

> 📖 **Siguiente:** [17-cheatsheet-devtools.md](./17-cheatsheet-devtools.md) — Cheatsheet de DevTools
