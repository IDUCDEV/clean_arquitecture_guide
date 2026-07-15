# 03 - Performance View

## Frame rendering en Flutter

### ¿Cómo funciona?

Flutter renderiza a 60 FPS (16.67ms por frame) o 120 FPS (8.33ms) en dispositivos de alta tasa.

```
Frame Timeline:
|---- 16ms ----|---- 16ms ----|---- 16ms ----|
   Frame 1         Frame 2         Frame 3
```

### Etapas de un frame

```
┌─────────────────┐
│   Build          │  Construir árbol de widgets ( Dart)
├─────────────────┤
│   Layout         │  Calcular positions y sizes
├─────────────────┤
│   Paint          │  Dibujar pixels en pantalla
├─────────────────┤
│   Composit       │  Combinar capas (GPU)
└─────────────────┘
```

### Frame budget

| Dispositivo | Target FPS | Budget por frame |
|-------------|------------|------------------|
| Mobile 60Hz | 60 FPS | 16.67ms |
| Mobile 120Hz | 120 FPS | 8.33ms |
| Desktop | 60 FPS | 16.67ms |
| Web | Variable | Depende del browser |

---

## Performance View en DevTools

### Pestañas disponibles

| Pestaña | Propósito |
|---------|-----------|
| **Frame Chart** | Gráfico de frames en tiempo real |
| **Frame Analysis** | Análisis detallado de frames seleccionados |
| **Timeline** | Grabación de timeline completa |
| **Enhanced Tracing** | Añadir tracing events específicos |

---

## Frame Chart

### Qué muestra

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

### Colores y su significado

| Color | Significado |
|-------|-------------|
| 🟦 Azul claro | UI thread (build/layout/paint) |
| 🟦 Azul oscuro | Raster thread (GPU rendering) |
| 🔴 Rojo | Frame超过budget (jank) |
| 🟩 Verde | Frame dentro del budget |

### Interacción con el gráfico
1. **Click en frame** → seleccionar para análisis detallado
2. **Drag** → hacer zoom en un rango de frames
3. **Double click** → resetear zoom
4. **Hover** → ver stats del frame (UI time, Raster time, Total)

---

## Frame Analysis (detallado)

### Seleccionar un frame
1. Click en un frame en el Frame Chart
2. Se abre el panel de análisis

### Información mostrada

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

### Métricas clave

| Métrica | Valor ideal | Acción si no se cumple |
|---------|-------------|------------------------|
| Widget rebuilds | < 100 | Reducir using const |
| Stateful rebuilds | < 20 | Usar Selective rebuild |
| Layout time | < 5ms | Simplificar widget tree |
| Paint time | < 5ms | Reducir complejidad visual |
| Total frame time | < 16ms | Investigar bottleneck |

---

## Identificando Jank

### Causas comunes de jank

| Causa | Síntoma en Performance | Solución |
|-------|------------------------|----------|
| **Build excesivo** | UI time alto | const widgets, RepaintBoundary |
| **Layout complejo** | Layout time alto | Simplificar widget tree |
| **Paint costoso** | Paint time alto | Imágenes cacheadas, opacidad |
| **Shaders** | Picos aleatorios | Precaching shaders |
| **Isolate bloqueado** | UI thread freeze | Mover a compute isolate |
| **GC pressure** | Picos frecuentes | Reducir allocaciones |

### Ejemplo: Build excesivo

**Problema:**
```dart
// ❌ Mal: reconstruye todo el widget tree en cada frame
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

## Enhanced Tracing

### Qué es
Añadir eventos personalizados al timeline para debugging específico.

### Tipos de tracing disponibles

| Trace | Propósito |
|-------|-----------|
| **Widget Builds** | Ver qué widgets se reconstruyen |
| **Layout** | Ver operaciones de layout |
| **Paint** | Ver operaciones de paint |
| **Semantics** | Ver cálculos de accesibilidad |
| **Animations** | Ver frames de animación |

### Cómo activar
1. Performance → Enhanced Tracing
2. Click en el trace que quieras activar
3. Grabar profiling session
4. Ver eventos en Timeline

### Uso de Timeline
```dart
import 'dart:developer';

// Marcar inicio de operación
Timeline.startSync('MyOperation');

// ... código costoso ...

// Marcar fin
Timeline.finishSync();
```

---

## Flame Chart

### ¿Qué es?
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

### Interacción
- **Click** → seleccionar evento
- **Double click** → hacer zoom
- **Hover** → ver duración exacta
- **Scroll** → navegar entre frames

### Eventos típicos en Flame Chart

| Evento | Thread | Qué significa |
|--------|--------|---------------|
| `buildScope` | UI | Construcción de widgets |
| `layout` | UI | Cálculo de posiciones |
| `paint` | UI | Dibujado |
| `intrinsic` | UI | Cálculo de tamaños intrínsecos |
| `animate` | UI | Animaciones en curso |
| `GPURasterizer` | Raster | Renderizado GPU |
| `GrFragmentProcess` | Raster | Procesamiento de fragmentos |

---

## Ejercicios prácticos

### Ejercicio 1: Medir impacto de ListView.builder vs ListView

```dart
// Versión 1: ListView (construye TODO)
ListView(
  children: List.generate(10000, (i) => ListTile(title: Text('Item $i'))),
)

// Versión 2: ListView.builder (construye solo visible)
ListView.builder(
  itemCount: 10000,
  itemBuilder: (context, i) => ListTile(title: Text('Item $i')),
)
```

1. Medir ambas versiones en Performance
2. Comparar frame times
3. Documentar diferencia

### Ejercicio 2: Impacto de RepaintBoundary

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

1. Medir sin RepaintBoundary
2. Agregar RepaintBoundary
3. Comparar paint time

### Ejercicio 3: Shaders compilation jank

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

1. Ejecutar app en profile mode
2. Navegar a pantalla con efecto blur
3. Observar primer frame (shader compilation)
4. Usar `ShaderBuilder` para pre-copilar

---
→ Siguiente: `04-cpu-profiler.md`
