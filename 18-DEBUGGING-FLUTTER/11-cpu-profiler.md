# 11 — CPU Profiler: Funciones Costosas

> Grabar y leer un perfil de CPU para identificar qué funciones consumen más tiempo y causan lentitud o jank.

---

## 1. ¿Qué es el CPU Profiler?

Herramienta que muestra qué parte del código está consumiendo más tiempo de CPU. Permite identificar funciones costosas que causan jank o lentitud.

---

## 2. Pestañas del CPU Profiler

| Pestaña | Propósito |
|---|---|
| **Flame Chart** | Call tree visual con tiempos |
| **Call Tree** | Árbol de llamadas con tiempos |
| **Bottom Up** | Funciones más costosas primero |
| **Source Code** | Código fuente con highlights |

---

## 3. Grabar un perfil de CPU

### 3.1 Pasos

1. Ir a CPU Profiler en DevTools
2. Click en **Record** (🔴)
3. Interactuar con la app (reproducir el problema)
4. Click en **Stop** para detener la grabación
5. Analizar resultados

### 3.2 Configuración de grabación

| Opción | Descripción |
|---|---|
| **Include dartsdk** | Incluir frames internos del Dart SDK |
| **Include Flutter** | Incluir frames del framework Flutter |
| **Sample rate** | Frecuencia de muestreo por defecto del VM |

> El profiler usa **sampling**: muestrea el stack periódicamente (p. ej. cada pocos ms) y estima el tiempo por función con esas muestras. No es una medición exacta de nanosegundos, sino una distribución aproximada.

---

## 4. Interpretando resultados

### 4.1 Profile View (resumen)

```
Total sample count: 1234

Top functions:
┌─────────────────────────────┬───────────┬──────────┐
│ Function                    │ Samples   │ % Total  │
├─────────────────────────────┼───────────┼──────────┤
│ buildScope                  │ 342       │ 27.7%    │
│ paint                       │ 218       │ 17.7%    │
│ layout                      │ 189       │ 15.3%    │
│ _InkResponsePainter.paint   │ 156       │ 12.6%    │
│ TextPainter.layout          │ 134       │ 10.9%    │
│ ImageCache.putIfAbsent      │ 98        │ 7.9%     │
│ Other                       │ 97        │ 7.9%     │
└─────────────────────────────┴───────────┴──────────┘
```

### 4.2 Call Tree (árbol de llamadas)

```
root (1234 samples)
├── WidgetBase.build (342)
│   ├── Column.build (120)
│   │   ├── Text.build (45)
│   │   ├── Icon.build (30)
│   │   └── Container.build (45)
│   └── ListView.builder.build (222)
│       └── _ListViewBuilderState.build (222)
├── RenderObject.layout (189)
│   ├── RenderFlex.performLayout (98)
│   └── RenderParagraph.performLayout (91)
└── Canvas.drawParagraph (218)
    └── [native] (218)
```

### 4.3 Bottom Up (funciones costosas primero)

```
┌─────────────────────────────┬───────────┬──────────┬──────────┐
│ Function                    │ Self      │ Children │ Total    │
├─────────────────────────────┼───────────┼──────────┼──────────┤
│ TextPainter.layout          │ 134       │ 0        │ 134      │
│ ImageCache.putIfAbsent      │ 98        │ 0        │ 98       │
│ RenderFlex.performLayout    │ 56        │ 42       │ 98       │
│ _ListViewBuilderState.build │ 45        │ 177      │ 222      │
└─────────────────────────────┴───────────┴──────────┴──────────┘
```

- **Self time**: tiempo en la función misma (sin contar hijos)
- **Total time**: tiempo total (función + hijos)

---

## 5. Causas comunes de alto uso de CPU

### 5.1 Build methods costosos

**Problema:**

```dart
@override
Widget build(BuildContext context) {
  // ❌ Cálculo costoso en cada build
  final items = List.generate(10000, (i) => computeExpensiveItem(i));
  return ListView.builder(
    itemCount: items.length,
    itemBuilder: (context, i) => items[i],
  );
}
```

**El CPU Profiler muestra:**

```
buildScope: 890 samples (72%)
└── MyWidget.build: 890
    └── List.generate: 650
        └── computeExpensiveItem: 650
```

**Fix:**

```dart
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late final List<Widget> _items;

  @override
  void initState() {
    super.initState();
    _items = List.generate(10000, (i) => computeExpensiveItem(i));
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: _items.length,
      itemBuilder: (context, i) => _items[i],
    );
  }
}
```

### 5.2 Imágenes sin cache

**Problema:**

```dart
// ❌ Descarga la imagen en cada build
Image.network(
  'https://example.com/image.jpg',
  // Sin cache, se vuelve a descargar
)
```

**Fix:**

```dart
// ✅ Usa cache implícito de Flutter (ImageCache) y evita re-descargas
Image.network(
  'https://example.com/image.jpg',
  cacheWidth: 500,  // Decodifica a menor resolución
)
```

> Si necesitas control fino de cache, usa `cached_network_image`, que guarda también en disco.

### 5.3 Text rendering excesivo

**El CPU Profiler muestra:**

```
TextPainter.layout: 450 samples (36%)
├── Text.computeMaxIntrinsicWidth: 200
└── TextPainter: 250
```

**Fix:**

```dart
// ❌ Textos largos sin límites
Text(
  'Very very very long text that needs to compute width...',
  style: TextStyle(fontSize: 16),
)

// ✅ Con límites explícitos
Text(
  'Very very very long text...',
  maxLines: 2,
  overflow: TextOverflow.ellipsis,
)

// ✅ O mejor aún: con constraints claros
ConstrainedBox(
  constraints: BoxConstraints(maxWidth: 300),
  child: Text('Long text...'),
)
```

### 5.4 Animaciones sin optimizar

**Problema:**

```dart
// ❌ Animación que reconstruye todo el árbol
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Transform.rotate(
      angle: _controller.value * 2 * 3.14159,
      child: ExpensiveWidget(),  // Se reconstruye cada frame
    );
  },
)
```

**Fix:**

```dart
// ✅ Solo animar lo que cambia
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Transform.rotate(
      angle: _controller.value * 2 * 3.14159,
      child: child,  // ← Pasar child como parámetro
    );
  },
  child: ExpensiveWidget(),  // No se reconstruye
)
```

---

## 6. Ejercicios prácticos

### 6.1 Ejercicio 1: identificar widget costoso

1. Crear lista con 1000 items
2. Cada item tiene imagen + texto + botón
3. Grabar CPU profile
4. Identificar qué parte consume más CPU
5. Optimizar y re-medir

### 6.2 Ejercicio 2: medir impacto de const

```dart
// Versión 1: Sin const
Column(
  children: [
    Text('Hello'),  // Se reconstruye cada build
    Icon(Icons.star),
    Text('World'),
  ],
)

// Versión 2: Con const
Column(
  children: [
    const Text('Hello'),  // Se reutiliza la instancia
    const Icon(Icons.star),
    const Text('World'),
  ],
)
```

1. Medir ambas versiones
2. Comparar samples de `buildScope`

### 6.3 Ejercicio 3: Flame Chart de animación

1. Crear animación compleja (múltiples animaciones simultáneas)
2. Grabar CPU profile durante 3 segundos de animación
3. Identificar cuánto tiempo consume cada animación
4. Verificar si alguna animación causa jank

---

## Resumen

| Concepto | Punto clave |
|---|---|
| Sampling | El profiler muestrea, no mide exacto |
| Call Tree | Muestra la jerarquía de llamadas |
| Bottom Up | Funciones más costosas primero |
| Self vs Total | Self = solo la función; Total = función + hijos |
| Optimización típica | `const`, cache, límites en Text, `child` en AnimatedBuilder |

---

## 📚 Referencias

- [Flutter | CPU Profiler](https://docs.flutter.dev/tools/devtools/cpu-profiler) — Documentación oficial del CPU Profiler
- [Flutter | Performance best practices](https://docs.flutter.dev/perf/best-practices) — Buenas prácticas de rendimiento
- [Flutter | Const performance](https://docs.flutter.dev/perf/const) — Uso de `const` para rendimiento

---

> 📖 **Siguiente:** [12-memory-profiler.md](./12-memory-profiler.md) — Memory Profiler: leaks y uso de memoria
