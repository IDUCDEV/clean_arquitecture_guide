# 10 — La Performance View: FPS, Frames y Jank

> Entender cómo Flutter renderiza frames, leer el Frame Chart y el Frame Analysis, y diagnosticar el jank.

---

## 1. Frame rendering en Flutter

### 1.1 ¿Cómo funciona?

Flutter renderiza a 60 FPS (16.67 ms por frame) o 120 FPS (8.33 ms) en dispositivos de alta tasa de refresco.

```
Frame Timeline:
|---- 16ms ----|---- 16ms ----|---- 16ms ----|
   Frame 1         Frame 2         Frame 3
```

### 1.2 Etapas de un frame

```
┌─────────────────┐
│   Build         │  Construir árbol de widgets (Dart)
├─────────────────┤
│   Layout        │  Calcular positions y sizes
├─────────────────┤
│   Paint         │  Dibujar pixels en pantalla
├─────────────────┤
│   Composite     │  Combinar capas (GPU)
└─────────────────┘
```

### 1.3 Frame budget

| Dispositivo | Target FPS | Budget por frame |
|---|---|---|
| Mobile 60 Hz | 60 FPS | 16.67 ms |
| Mobile 120 Hz | 120 FPS | 8.33 ms |
| Desktop | 60 FPS | 16.67 ms |
| Web | Variable | Depende del browser |

---

## 2. Performance View en DevTools

### 2.1 Pestañas disponibles

| Pestaña | Propósito |
|---|---|
| **Frame Chart** | Gráfico de frames en tiempo real |
| **Frame Analysis** | Análisis detallado de frames seleccionados |
| **Timeline** | Grabación de timeline completa |
| **Enhanced Tracing** | Añadir tracing events específicos |

> La vista actual de DevTools fusiona lo que antes eran **Timeline** y **Performance** en una sola pantalla con pestañas. El **Performance Overlay** in-app (banda verde/roja arriba) es el primer filtro rápido.

---

## 3. Frame Chart

### 3.1 Qué muestra

```
UI Time (ms)
    ▲
 50 │           ██
 40 │     ██    ██
 30 │     ██    ██ ██
 20 │  ██ ██ ██ ██ ██ ██
 16 │──██─██─██─██─██─██── ← Target (16ms)
 10 │  ██ ██ ██ ██ ██ ██
  0 └──────────────────────→ Time
     F1 F2 F3 F4 F5 F6

█ = UI thread time
░ = Raster thread time
```

### 3.2 Colores y su significado

| Color | Significado |
|---|---|
| Azul claro | UI thread (build/layout/paint) |
| Azul oscuro | Raster thread (GPU rendering) |
| Rojo | Frame que supera el budget (jank) |
| Verde | Frame dentro del budget |

### 3.3 Interacción con el gráfico

1. **Click en frame** → seleccionar para análisis detallado
2. **Drag** → hacer zoom en un rango de frames
3. **Double click** → resetear zoom
4. **Hover** → ver stats del frame (UI time, Raster time, Total)

---

## 4. Frame Analysis (detallado)

### 4.1 Seleccionar un frame

1. Click en un frame en el Frame Chart
2. Se abre el panel de análisis

### 4.2 Información mostrada

```
Frame #1234
├── Build Phase
│   ├── Widget rebuilds: 47
│   ├── Stateful rebuilds: 12
│   └── Time: 8.2ms
├── Layout Phase
│   ├── Layout calls: 23
│   └── Time: 2.1ms
├── Paint Phase
│   ├── Layers painted: 15
│   └── Time: 3.4ms
└── Total: 13.7ms ✓
```

### 4.3 Métricas clave

| Métrica | Valor ideal | Acción si no se cumple |
|---|---|---|
| Widget rebuilds | < 100 | Reducir usando `const` |
| Stateful rebuilds | < 20 | Usar reconstrucción selectiva |
| Layout time | < 5 ms | Simplificar el widget tree |
| Paint time | < 5 ms | Reducir complejidad visual |
| Total frame time | < 16 ms | Investigar el bottleneck |

---

## 5. Identificando Jank

### 5.1 Causas comunes de jank

| Causa | Síntoma en Performance | Solución |
|---|---|---|
| **Build excesivo** | UI time alto | Widgets `const`, `RepaintBoundary` |
| **Layout complejo** | Layout time alto | Simplificar el widget tree |
| **Paint costoso** | Paint time alto | Imágenes cacheadas, menos capas |
| **Shaders** | Picos aleatorios | Impeller / precaching |
| **Isolate bloqueado** | UI thread freeze | Mover a `compute`/isolate |
| **GC pressure** | Picos frecuentes | Reducir allocaciones |

### 5.2 Ejemplo: build excesivo

**Problema:**

```dart
// ❌ Mal: reconstruye en cada frame
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Text('${DateTime.now()}');  // Se reconstruye constantemente
  }
}
```

**Fix:**

```dart
// ✅ Bien: usar Timer para actualizar solo el texto
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late Timer _timer;
  String _time = '';

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(Duration(seconds: 1), (_) {
      setState(() => _time = DateTime.now().toString());
    });
  }

  @override
  Widget build(BuildContext context) {
    return Text(_time);  // Solo reconstruye este widget
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }
}
```

---

## 6. Enhanced Tracing

### 6.1 Qué es

Añade eventos personalizados al timeline para debugging específico.

### 6.2 Tipos de tracing disponibles

| Trace | Propósito |
|---|---|
| **Widget Builds** | Ver qué widgets se reconstruyen |
| **Layout** | Ver operaciones de layout |
| **Paint** | Ver operaciones de paint |
| **Semantics** | Ver cálculos de accesibilidad |
| **Animations** | Ver frames de animación |

### 6.3 Cómo activar

1. Performance → Enhanced Tracing
2. Click en el trace que quieras activar
3. Grabar la profiling session
4. Ver eventos en el Timeline

### 6.4 Trazado desde código

```dart
import 'dart:developer';

// Marcar inicio de operación
Timeline.startSync('MyOperation');

// ... código costoso ...

// Marcar fin
Timeline.finishSync();
```

---

## 7. Flame Chart

### 7.1 ¿Qué es?

Visualización de qué función/tarea está consumiendo tiempo en cada frame.

```
|--- Frame 1234 ---|
├── UI Thread
│   ├── buildScope    ████░░░░░░  4.2ms
│   ├── layout        ██░░░░░░░░  1.8ms
│   ├── paint         ███░░░░░░░  2.9ms
│   └── composite     █░░░░░░░░░  0.8ms
├── Raster Thread
│   ├── GPURasterizer ████████░░  8.1ms
│   └── SurfaceFrame █░░░░░░░░░  1.2ms
```

### 7.2 Interacción

- **Click** → seleccionar evento
- **Double click** → hacer zoom
- **Hover** → ver duración exacta
- **Scroll** → navegar entre frames

### 7.3 Eventos típicos en el Flame Chart

| Evento | Thread | Qué significa |
|---|---|---|
| `buildScope` | UI | Construcción de widgets |
| `layout` | UI | Cálculo de posiciones |
| `paint` | UI | Dibujado |
| `intrinsic` | UI | Cálculo de tamaños intrínsecos |
| `animate` | UI | Animaciones en curso |
| `GPURasterizer` | Raster | Renderizado GPU |
| `GrFragmentProcess` | Raster | Procesamiento de fragmentos |

---

## 8. Ejercicios prácticos

### 8.1 Ejercicio 1: ListView vs ListView.builder

```dart
// Versión 1: ListView (construye TODO)
ListView(
  children: List.generate(10000, (i) => ListTile(title: Text('Item $i'))),
)

// Versión 2: ListView.builder (construye solo lo visible)
ListView.builder(
  itemCount: 10000,
  itemBuilder: (context, i) => ListTile(title: Text('Item $i')),
)
```

1. Medir ambas versiones en Performance
2. Comparar frame times
3. Documentar la diferencia

### 8.2 Ejercicio 2: Impacto de RepaintBoundary

```dart
// Sin RepaintBoundary
Column(
  children: [
    AnimatedWidget(),  // Se reconstruye frecuentemente
    StaticWidget(),    // No cambia pero se repinta igual
  ],
)

// Con RepaintBoundary
Column(
  children: [
    RepaintBoundary(
      child: AnimatedWidget(),  // Solo repinta este subtree
    ),
    RepaintBoundary(
      child: StaticWidget(),    // No se repinta
    ),
  ],
)
```

1. Medir sin `RepaintBoundary`
2. Agregar `RepaintBoundary`
3. Comparar paint time

### 8.3 Ejercicio 3: Shader compilation jank

```dart
// Primera vez que se usa un efecto visual complejo
ClipRRect(
  borderRadius: BorderRadius.circular(20),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
    child: Container(color: Colors.black26),
  ),
)
```

1. Ejecutar la app en profile mode
2. Navegar a la pantalla con el efecto blur
3. Observar el primer frame (shader compilation)
4. En Android/iOS con **Impeller** (default desde Flutter 3.10+) este jank se elimina casi por completo; en Web sigue siendo relevante precargar los shaders navegando por todas las pantallas antes del release.

---

## Resumen

| Concepto | Punto clave |
|---|---|
| Frame budget | 16.67 ms @60 Hz, 8.33 ms @120 Hz |
| Frame Chart | Verde = bien, rojo = jank |
| Frame Analysis | Desglosa build/layout/paint del frame |
| Jank | Causas: build, layout, paint, shaders, isolates, GC |
| Flame Chart | Muestra qué función consume cada frame |

---

## 📚 Referencias

- [Flutter | Performance view](https://docs.flutter.dev/tools/devtools/performance) — Documentación oficial de la Performance view
- [Flutter | Performance best practices](https://docs.flutter.dev/perf/best-practices) — Buenas prácticas de rendimiento
- [Flutter | Impeller](https://docs.flutter.dev/perf/impeller) — Renderer por defecto y shader compilation

---

> 📖 **Siguiente:** [11-cpu-profiler.md](./11-cpu-profiler.md) — CPU Profiler: identificando funciones costosas
