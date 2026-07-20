# 05 - Cheatsheet de Optimizacion de Rendimiento

## Problema → Causa → Solucion → DevTools View

| Problema | Causa probable | Solucion | DevTools View |
|---|---|---|---|
| Jank en scroll | Build time > 8ms por item | `ListView.builder` + `const` | Performance |
| Jank en animacion | Muchos widgets en el subtree | `RepaintBoundary` + `AnimatedBuilder` | Performance |
| Memoria crece sin parar | Stream/Controller sin dispose | Agregar `dispose()` correcto | Memory |
| Frame rojo en DevTools | UI thread lento | Reducir trabajo en `build()` | Performance |
| Frame morado en DevTools | Raster thread lento | Menos capas, menos opacidad | Performance |
| App consume mucha RAM | Imagenes sin cacheWidth/Height | Agregar `cacheWidth`/`cacheHeight` | Memory |
| Transicion lenta | Demasiados widgets en pantalla | Extraer widgets, usar `const` | Performance |
| Rebuilds excesivos | BlocBuilder sin filtro | `BlocSelector` o `buildWhen` | Performance > Enhance Tracing |
| Texto parpadea | Rebuild completo del subtree | `const` + extraccion de widgets | Performance |
| App lenta en inicio | Work pesado en `initState` | Lazy loading, `Isolate` | CPU Profiler |

---

## Rangos saludables de metricas

| Metrica | Excelente | Aceptable | Necesita accion |
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

## Checklist pre-optimizacion

```
1. Ejecutar en profile
   └── flutter run --profile

2. Habilitar Performance Overlay
   └── Ver frames rojos/morados en pantalla

3. Abrir DevTools Performance
   └── Grabar frame timeline (5-10 segundos de interaccion)

4. Identificar el frame mas lento
   └── Buscar el frame con mayor tiempo total

5. Analizar el flame chart
   └── Que funcion consume mas tiempo?

6. Verificar memory baseline
   └── Tomar heap snapshot base

7. Repetir interaccion 5x
   └── Tomar diff snapshot

8. Clasificar el problema
   ├── Build lento → Optimizar rebuilds
   ├── Raster lento → Optimizar rendering
   ├── Memory leak → Buscar dispose faltante
   └── Todo bien → No optimizar aun
```

---

## Anti-patrones

| Patron Incorrecto | Por que es malo | Mejor enfoque |
|---|---|---|
| `ListView` con 100+ items | Construye todo de una vez | `ListView.builder` |
| `BlocBuilder` sin filtro | Reconstruye todo el subtree | `BlocSelector` |
| `setState` en loop | N rebuilds por N iteraciones | Un solo `setState` agrupado |
| `Opacity` widget | Crea capa GPU separada | `ColorFiltered` o painter |
| `Image.network` sin sizes | Decodifica imagen completa | `cacheWidth` + `cacheHeight` |
| `TextEditingController` sin dispose | Memory leak | Cerrar en `dispose()` |
| `Timer.periodic` sin cancel | CPU + memoria leak | Cerrar en `dispose()` |
| Widget sin `const` constante | Reconstruccion innecesaria | Agregar `const` |
| `setState` en `didChangeDependencies` | Rebuilds potencialmente infinitos | `initState` + carga async |
| `Key` sin razon | Overhead innecesario | Solo usar Key cuando es necesario |

---

## Atajos y comandos de profiling

### CLI

```bash
# Ejecutar en profile (OBLIGATORIO para mediciones)
flutter run --profile

# Analizar tamano del build
flutter build apk --analyze-size
flutter build ios --analyze-size

# Ver dependencias
flutter pub deps

# Ver tamano de assets
flutter pub cache list

# Clean y rebuild
flutter clean && flutter pub get

# Ver informacion del dispositivo
flutter devices
flutter emulators
```

### DevTools Views

| Vista | Acceso rapido | Para que |
|---|---|---|
| Performance | `Ctrl+Shift+P` → "Performance" | Frames, jank, timeline |
| Memory | `Ctrl+Shift+P` → "Memory" | Leaks, heap, GC |
| CPU Profiler | `Ctrl+Shift+P` → "CPU Profiler" | Flame chart, sampling |
| Inspector | `Ctrl+Shift+P` → "Inspector" | Widget tree, layout |
| Network | `Ctrl+Shift+P` → "Network" | HTTP requests |

---

## Flujo de investigacion de memoria (ASCII)

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
│       └── 🔍 Investigar: que la instancia?
│           └── Buscar en codigo: new ClassName()
│
└── 5. Repetir hasta que no haya crecimiento
```

---

## Mitos comunes de rendimiento desmentidos

| Mitos | Realidad |
|---|---|
| "Flutter es lento porque usa Dart" | Dart AOT compila a codigo nativo, rendimiento similar a Kotlin/Swift |
| "Debo usar keys en todos los widgets" | Keys solo son necesarios cuando Flutter necesita distinguir widgets |
| "setState es malo, siempre usa BLoC" | setState es perfecto para estado local simple |
| "Mas widgets = mas lento" | El numero de widgets no importa, importa el trabajo en build/paint |
| "DevTools en debug sirve para medir" | **FALSO**: siempre medir en profile, debug tiene overhead JIT |
| "Las imagenes siempre son lentas" | Con `cacheWidth`/`cacheHeight` y precache, son eficientes |
| "Debo optimizar todo el codigo" | Solo optimiza donde tengas un problema medible |
| "const no hace diferencia" | const puede reducir rebuilds un 50-80% en UIs estaticas |
| "RepaintBoundary siempre ayuda" | Agregar RepaintBoundary incorrectamente puede empeorar performance |
| "Los Slivers son siempre mejores" | Para listas simples, ListView.builder es suficiente |

---

## Comandos rapidos de referencia

```bash
# === EJECUCION ===
flutter run --profile           # Profile mode (mediciones)
flutter run --release           # Release mode (produccion)
flutter run -d chrome           # Web
flutter run -d <device-id>      # Dispositivo especifico

# === ANALISIS ===
flutter analyze                 # Analisis estatico
flutter build apk --analyze-size  # Tamano del APK
flutter build ios --analyze-size  # Tamano del IPA

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

## Referencia rapida de const

```dart
// ✅ PUEDES usar const
const Text('literal')
const Icon(Icons.star)
const SizedBox(height: 16)
const Padding(
  padding: EdgeInsets.all(8.0),
  child: Text('estatico'),
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
