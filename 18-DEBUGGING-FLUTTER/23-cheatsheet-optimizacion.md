# 23 — Cheatsheet de Optimización de Rendimiento

> Referencia rápida: problemas comunes → causa → solución → vista de DevTools, métricas saludables, anti-patrones, comandos y mitos.

---

## 1. Problema → Causa → Solución → DevTools View

| Problema | Causa probable | Solución | DevTools View |
|---|---|---|---|
| Jank en scroll | Build time > 8ms por item | `ListView.builder` + `const` | Performance |
| Jank en animación | Muchos widgets en el subtree | `RepaintBoundary` + `AnimatedBuilder` | Performance |
| Memoria crece sin parar | Stream/Controller sin dispose | Agregar `dispose()` correcto | Memory |
| Frame rojo en DevTools | UI thread lento | Reducir trabajo en `build()` | Performance |
| Frame morado en DevTools | Raster thread lento | Menos capas, menos opacidad | Performance |
| App consume mucha RAM | Imágenes sin cacheWidth/Height | Agregar `cacheWidth`/`cacheHeight` | Memory |
| Transición lenta | Demasiados widgets en pantalla | Extraer widgets, usar `const` | Performance |
| Rebuilds excesivos | BlocBuilder sin filtro | `BlocSelector` o `buildWhen` | Performance > Enhance Tracing |
| Texto parpadea | Rebuild completo del subtree | `const` + extracción de widgets | Performance |
| App lenta en inicio | Work pesado en `initState` | Lazy loading, `Isolate` | CPU Profiler |

---

## 2. Rangos saludables de métricas

| Métrica | Excelente | Aceptable | Necesita acción |
|---|---|---|---|
| FPS | 60 (120 ProMotion) | 55-59 | < 55 |
| Build time | < 4ms | 4-8ms | > 8ms |
| Raster time | < 4ms | 4-8ms | > 8ms |
| Memory (idle) | < 100MB | 100-200MB | > 200MB |
| Memory growth | 0 MB/min | < 1 MB/min | > 1 MB/min |
| GC frequency | < 1/min | 1-5/min | > 5/min |
| App startup | < 1s | 1-3s | > 3s |
| Widget tree depth | < 15 niveles | 15-25 | > 25 |

---

## 3. Checklist pre-optimización

```
1. Ejecutar en profile
   └── flutter run --profile

2. Habilitar Performance Overlay
   └── Ver frames rojos/morados en pantalla

3. Abrir DevTools Performance
   └── Grabar frame timeline (5-10 segundos de interacción)

4. Identificar el frame más lento
   └── Buscar el frame con mayor tiempo total

5. Analizar el flame chart
   └── ¿Qué función consume más tiempo?

6. Verificar memory baseline
   └── Tomar heap snapshot base

7. Repetir interacción 5x
   └── Tomar diff snapshot

8. Clasificar el problema
   ├── Build lento → Optimizar rebuilds
   ├── Raster lento → Optimizar rendering
   ├── Memory leak → Buscar dispose faltante
   └── Todo bien → No optimizar aún
```

---

## 4. Anti-patrones

| Patrón Incorrecto | Por qué es malo | Mejor enfoque |
|---|---|---|
| `ListView` con 100+ items | Construye todo de una vez | `ListView.builder` |
| `BlocBuilder` sin filtro | Reconstruye todo el subtree | `BlocSelector` |
| `setState` en loop | N rebuilds por N iteraciones | Un solo `setState` agrupado |
| `Opacity` widget | Crea capa GPU separada | `AnimatedOpacity`, `IgnorePointer` o painter |
| `Image.network` sin sizes | Decodifica imagen completa | `cacheWidth` + `cacheHeight` |
| `TextEditingController` sin dispose | Memory leak | Cerrar en `dispose()` |
| `Timer.periodic` sin cancel | CPU + memoria leak | Cerrar en `dispose()` |
| Widget sin `const` constante | Reconstrucción innecesaria | Agregar `const` |
| `setState` en `didChangeDependencies` | Rebuilds potencialmente infinitos | `initState` + carga async |
| `Key` sin razón | Overhead innecesario | Solo usar Key cuando es necesario |

---

## 5. Atajos y comandos de profiling

### 5.1 CLI

```bash
# Ejecutar en profile (OBLIGATORIO para mediciones)
flutter run --profile

# Analizar tamaño del build
flutter build apk --analyze-size
flutter build ios --analyze-size

# Ver dependencias
flutter pub deps

# Clean y rebuild
flutter clean && flutter pub get

# Ver información del dispositivo
flutter devices
flutter emulators
```

### 5.2 DevTools Views

| Vista | Acceso rápido | Para qué |
|---|---|---|
| Performance | `Ctrl+Shift+P` → "Performance" | Frames, jank, timeline |
| Memory | `Ctrl+Shift+P` → "Memory" | Leaks, heap, GC |
| CPU Profiler | `Ctrl+Shift+P` → "CPU Profiler" | Flame chart, sampling |
| Inspector | `Ctrl+Shift+P` → "Inspector" | Widget tree, layout |
| Network | `Ctrl+Shift+P` → "Network" | HTTP requests |

---

## 6. Flujo de investigación de memoria (ASCII)

```
App consume mucha memoria?
│
├── 1. DevTools > Memory > Tomar snapshot base
│
├── 2. Navegar a pantalla sospechosa (5x)
│
├── 3. Tomar diff snapshot
│
├── 4. Buscar clases con crecimiento
│   │
│   ├── StreamSubscription con crecimiento
│   │   └── ✅ Fix: Guardar y cancelar en dispose()
│   │
│   ├── TextEditingController con crecimiento
│   │   └── ✅ Fix: Agregar dispose()
│   │
│   ├── AnimationController con crecimiento
│   │   └── ✅ Fix: Agregar dispose()
│   │
│   ├── Timer con crecimiento
│   │   └── ✅ Fix: Guardar referencia y cancel()
│   │
│   └── Clase desconocida con crecimiento
│       └── 🔍 Investigar: ¿qué la instancia?
│           └── Buscar en código: new ClassName()
│
└── 5. Repetir hasta que no haya crecimiento
```

---

## 7. Mitos comunes de rendimiento desmentidos

| Mito | Realidad |
|---|---|
| "Flutter es lento porque usa Dart" | Dart AOT compila a código nativo, rendimiento similar a Kotlin/Swift |
| "Debo usar keys en todos los widgets" | Keys solo son necesarios cuando Flutter necesita distinguir widgets |
| "setState es malo, siempre usa BLoC" | setState es perfecto para estado local simple |
| "Más widgets = más lento" | El número de widgets no importa, importa el trabajo en build/paint |
| "DevTools en debug sirve para medir" | **FALSO**: siempre medir en profile, debug tiene overhead JIT |
| "Las imágenes siempre son lentas" | Con `cacheWidth`/`cacheHeight` y precache, son eficientes |
| "Debo optimizar todo el código" | Solo optimiza donde tengas un problema medible |
| "const no hace diferencia" | const puede reducir rebuilds un 50-80% en UIs estáticas |
| "RepaintBoundary siempre ayuda" | Agregar RepaintBoundary incorrectamente puede empeorar performance |
| "Los Slivers son siempre mejores" | Para listas simples, ListView.builder es suficiente |

---

## 8. Comandos rápidos de referencia

```bash
# === EJECUCIÓN ===
flutter run --profile           # Profile mode (mediciones)
flutter run --release           # Release mode (producción)
flutter run -d chrome           # Web
flutter run -d <device-id>      # Dispositivo específico

# === ANÁLISIS ===
flutter analyze                 # Análisis estático
flutter build apk --analyze-size  # Tamaño del APK
flutter build ios --analyze-size  # Tamaño del IPA

# === DEPENDENCIAS ===
flutter pub get                 # Instalar dependencias
flutter pub upgrade             # Actualizar dependencias
flutter pub outdated            # Ver dependencias desactualizadas

# === LIMPIEZA ===
flutter clean                   # Limpiar build cache
flutter pub cache repair        # Reparar cache global

# === PERFORMANCE ===
flutter drive --target=test_driver/perf_test.dart  # Performance test
```

---

## 9. Referencia rápida de const

```dart
// ✅ PUEDES usar const
const Text('literal')
const Icon(Icons.star)
const SizedBox(height: 16)
const Padding(
  padding: EdgeInsets.all(8.0),
  child: Text('estático'),
)
const [Text('a'), Text('b'), Text('c')]

// ❌ NO puedes usar const
Text(dynamicVariable)
Text('${user.name}')
Image.network('$url')
ElevatedButton(
  onPressed: () {},  // Closure no es const
  child: Text('Click'),
)
```

---

## Resumen

| Sección | Clave |
|---|---|
| **Diagnóstico** | Asocia cada síntoma a su causa y vista de DevTools |
| **Métricas** | Build/raster < 4ms, sin crecimiento de memoria |
| **Pre-optimización** | Medir siempre en profile mode |
| **Anti-patrones** | builder + const + dispose cubren el 90% de los casos |
| **Mitos** | Optimiza solo donde haya un problema medible |

---

## 📚 Referencias

- [Flutter | Performance best practices](https://docs.flutter.dev/perf/best-practices) — Guía oficial de buenas prácticas
- [Flutter | Profiling modes](https://docs.flutter.dev/perf/profiling) — Por qué medir en profile
- [Flutter | Performance debugging](https://docs.flutter.dev/perf/ui-performance) — Depuración de rendimiento de UI

---

> 📖 **Siguiente:** [24-practicas-optimizacion.md](./24-practicas-optimizacion.md) — Prácticas de optimización de rendimiento
