# 22 — Rendering Complejo: Listas, Slivers e Imágenes

> Optimizar listas largas, scrolls complejos con Slivers, imágenes y rendering pesado.

---

## 1. ListView.builder vs ListView

La diferencia más crítica en listas Flutter: **`ListView` construye todos los items de una vez**, mientras que **`ListView.builder` solo construye los visibles**.

### 1.1 ListView (sin builder)

```dart
// ❌ CONSTRUYE TODOS LOS ITEMS de una vez
ListView(
  children: items.map((item) => ItemWidget(
    key: ValueKey(item.id),
    item: item,
  )).toList(),
)
```

```
Items totales: 1000
Items construidos: 1000  ← TODOS
Items visibles: 15
Memoria usada: MUCHA
```

### 1.2 ListView.builder (lazy loading)

```dart
// ✅ SOLO CONSTRUYE los items visibles
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ItemWidget(
      key: ValueKey(items[index].id),
      item: items[index],
    );
  },
)
```

```
Items totales: 1000
Items construidos: ~20  ← Solo visibles + buffer
Items visibles: 15
Memoria usada: MÍNIMA
```

### 1.3 Comparación

| Característica | ListView | ListView.builder |
|---|---|---|
| Items construidos | Todos | Solo visibles |
| Memoria | Lineal con items | Constante |
| Scroll inicial | Instantáneo | Puede tener micro-lag |
| Ideal para | < 20 items | > 20 items |
| Performance | O(n) | O(1) |

### 1.4 Cuándo usar cada uno

```
¿Cuántos items tiene tu lista?
├── < 10 items → ListView (simple, no hay diferencia)
├── 10-50 items → ListView.builder (precaución)
├── > 50 items → ListView.builder (obligatorio)
└── Items de tamaño variable → ListView.builder + SliverList
```

---

## 2. Slivers: layouts de scroll complejos

Los **Slivers** permiten crear layouts de scroll donde diferentes secciones tienen diferentes comportamientos.

### 2.1 CustomScrollView

```dart
CustomScrollView(
  slivers: [
    // Header fijo
    SliverAppBar(
      expandedHeight: 200,
      floating: true,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Mi App'),
        background: Image.network(url, fit: BoxFit.cover),
      ),
    ),

    // Lista de items
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ListTile(
          title: Text('Item $index'),
        ),
        childCount: 100,
      ),
    ),

    // Grid de productos
    SliverGrid(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ProductCard(product: products[index]),
        childCount: products.length,
      ),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: 0.75,
      ),
    ),

    // Footer
    const SliverToBoxAdapter(
      child: FooterWidget(),
    ),
  ],
)
```

### 2.2 Slivers disponibles

| Sliver | Uso | Performance |
|---|---|---|
| `SliverList` | Lista vertical lazy | ✅ Excelente |
| `SliverGrid` | Grid lazy | ✅ Excelente |
| `SliverAppBar` | AppBar con scroll | ✅ Excelente |
| `SliverFixedExtentList` | Lista con items de alto fijo | ✅✅ Mejor que SliverList |
| `SliverPrototypeExtentList` | Lista con prototype de alto | ✅✅ Muy rápido |
| `SliverFillRemaining` | Contenido que llena el espacio restante | ✅ |
| `SliverToBoxAdapter` | Widget normal dentro de CustomScrollView | ✅ |

### 2.3 SliverFixedExtentList: la versión rápida

```dart
// SliverList: calcula constraints por cada item
SliverList(
  delegate: SliverChildBuilderDelegate(
    (context, index) => ListTile(title: Text('Item $index')),
    childCount: 1000,
  ),
)

// SliverFixedExtentList: sabe el alto exacto, más rápido
SliverFixedExtentList(
  delegate: SliverChildBuilderDelegate(
    (context, index) => ListTile(title: Text('Item $index')),
    childCount: 1000,
  ),
  itemExtent: 56.0,  // ← Alto fijo en pixels
)
```

---

## 3. Optimización de imágenes

### 3.1 cacheWidth y cacheHeight

Cuando cargas una imagen de red, Flutter la decodifica a su tamaño original. Si la imagen es de 4000x3000 pero solo necesitas 200x150, estás desperdiciando memoria y CPU.

```dart
// ❌ IMAGEN COMPLETA decodificada (4000x3000 = 12M pixels)
Image.network(
  'https://example.com/photo.jpg',
)

// ✅ IMAGEN REDIMENSIONADA al tamaño real de display (200x150 = 30K pixels)
Image.network(
  'https://example.com/photo.jpg',
  width: 200,
  height: 150,
  cacheWidth: 200,  // ← Decodifica a este tamaño
  cacheHeight: 150, // ← Ahorra ~99% de memoria
)
```

```
Memoria de imagen:

Sin cacheWidth/Height:
  4000 × 3000 × 4 bytes = 48 MB  ← Desperdicio

Con cacheWidth/Height (display: 200x150):
  200 × 150 × 4 bytes = 120 KB   ← 400x menos memoria
```

### 3.2 AssetImage vs NetworkImage

| Tipo | Carga | Cache | Uso ideal |
|---|---|---|---|
| `AssetImage` | Local, rápida | En memoria | Iconos, logos, backgrounds |
| `NetworkImage` | Remota, lenta | Disco + memoria | Fotos de usuario, contenido |
| `FileImage` | Local, rápida | En memoria | Fotos tomadas con cámara |

### 3.3 precacheImage: cargar imágenes antes de necesitarlas

```dart
@override
void initState() {
  super.initState();

  // Precargar la imagen para que aparezca instantáneamente
  precacheImage(
    NetworkImage('https://example.com/hero.jpg'),
    context,
  );
}

@override
Widget build(BuildContext context) {
  return Image.network('https://example.com/hero.jpg');
  // ↑ La imagen ya está en cache, carga instantánea
}
```

### 3.4 Patrón completo de imagen optimizada

```dart
class OptimizedImage extends StatelessWidget {
  final String url;
  final double width;
  final double height;

  const OptimizedImage({
    super.key,
    required this.url,
    required this.width,
    required this.height,
  });

  @override
  Widget build(BuildContext context) {
    final dpr = MediaQuery.devicePixelRatioOf(context);
    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: Image.network(
        url,
        width: width,
        height: height,
        cacheWidth: (width * dpr).toInt(),
        cacheHeight: (height * dpr).toInt(),
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) {
          return Container(
            width: width,
            height: height,
            color: Colors.grey[300],
            child: const Icon(Icons.error),
          );
        },
      ),
    );
  }
}
```

---

## 4. ShaderMask y ClipRect: consideraciones de performance

### 4.1 ShaderMask

```dart
// ShaderMask aplica un gradiente sobre el contenido
// Cada frame: lee el widget hijo + aplica el shader
ShaderMask(
  shaderCallback: (Rect bounds) {
    return LinearGradient(
      colors: [Colors.white, Colors.transparent],
    ).createShader(bounds);
  },
  blendMode: BlendMode.dstIn,
  child: Image.network(url),
)
```

| Impacto | Causa |
|---|---|
| Medio | Calcula shader por cada frame |
| Alto si hay animación | Shader se recalcula continuamente |
| Bajo si es estático | Una sola vez al renderizar |

### 4.2 ClipRect

```dart
// ClipRect recorta el contenido a los límites del padre
// Impide que los hijos se dibujen fuera del área
ClipRect(
  child: SizedBox(
    width: 100,
    height: 100,
    child: LargeWidget(),  // ← Solo se dibuja lo visible
  ),
)
```

| Impacto | Causa |
|---|---|
| Bajo-Medio | Crea una capa de composición |
| Alto si anidados | Múltiples clip layers = GPU work |

### 4.3 Reglas de uso

| Widget | Usar cuando... | Evitar cuando... |
|---|---|---|
| `ShaderMask` | Efecto visual necesario | Decoración sin valor real |
| `ClipRect` | Overflow controlado | Se puede evitar con constraints en el hijo |
| `ClipRRect` | Bordes redondeados | Usar `Decoration` con `borderRadius` |

---

## 5. RepaintBoundary en listas con animaciones

```dart
class AnimatedListItem extends StatefulWidget {
  final Item item;

  const AnimatedListItem({super.key, required this.item});

  @override
  State<AnimatedListItem> createState() => _AnimatedListItemState();
}

class _AnimatedListItemState extends State<AnimatedListItem>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 300),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(  // ← Limita el repintado a este item
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Opacity(
            opacity: _controller.value,
            child: child,
          );
        },
        child: ListTile(
          title: Text(widget.item.name),
          leading: CircleAvatar(child: Text(widget.item.name[0])),
        ),
      ),
    );
  }
}
```

---

## 6. shouldRepaint en CustomPainter

### 6.1 Patrón básico

```dart
class MyPainter extends CustomPainter {
  final double progress;

  MyPainter(this.progress);

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blue
      ..strokeWidth = 2;

    canvas.drawLine(
      Offset(0, size.height * progress),
      Offset(size.width, size.height * progress),
      paint,
    );
  }

  @override
  bool shouldRepaint(MyPainter oldDelegate) {
    // ✅ SOLO repintar si el progress cambió
    return oldDelegate.progress != progress;
  }
}
```

### 6.2 shouldRepaint: qué retornar

| Escenario | Retorno | Razón |
|---|---|---|
| Widget completamente estático | `return false` | Nunca cambia |
| Depende de un solo campo | `return old.field != field` | Solo repinta si cambia |
| Siempre cambia | `return true` | No hay forma de evitarlo |
| Depende de múltiples campos | Comparar todos los campos | Granularidad máxima |

### 6.3 Ejemplo estático

```dart
class BackgroundPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    // Dibuja un patrón estático
    final paint = Paint()..color = Colors.grey[200]!;
    for (double i = 0; i < size.width; i += 20) {
      canvas.drawLine(Offset(i, 0), Offset(i, size.height), paint);
    }
  }

  @override
  bool shouldRepaint(BackgroundPainter oldDelegate) {
    return false;  // ← NUNCA repinta, es estático
  }
}
```

---

## 7. Animaciones: AnimatedContainer vs AnimatedBuilder

### 7.1 AnimatedContainer

```dart
// ✅ SIMPLE: animación implícita de propiedades
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  width: isExpanded ? 200 : 100,
  color: isExpanded ? Colors.blue : Colors.red,
  child: const Text('Animated'),
)
```

### 7.2 AnimatedBuilder

```dart
// ✅ COMPLEJO: animación personalizada
AnimatedBuilder(
  animation: _controller,
  builder: (context, child) {
    return Transform.rotate(
      angle: _controller.value * 2 * math.pi,
      child: child,  // ← El child NO se reconstruye
    );
  },
  child: Icon(Icons.refresh, size: 48),  // ← Construido una sola vez
)
```

### 7.3 Comparación

| Característica | AnimatedContainer | AnimatedBuilder |
|---|---|---|
| Complejidad | Baja | Media-Alta |
| Propiedades | Limitadas (width, height, color, etc.) | Cualquier propiedad |
| Performance | Buena | Excelente (con child) |
| Uso ideal | Animaciones de layout | Animaciones custom |

---

## 8. Widgets pesados: splitting build methods

### 8.1 Patrón: extracción de widgets

```dart
// ❌ MAL: Todo en un solo build method gigante
class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Header (100 líneas de código)
        // Chart (200 líneas de código)
        // Table (150 líneas de código)
        // Footer (50 líneas de código)
      ],
    );
  }
}

// ✅ BIEN: Widgets extraídos
class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        DashboardHeader(),
        DashboardChart(),
        DashboardTable(),
        DashboardFooter(),
      ],
    );
  }
}

class DashboardHeader extends StatelessWidget {
  const DashboardHeader({super.key});

  @override
  Widget build(BuildContext context) {
    // Header logic aquí
  }
}

class DashboardChart extends StatelessWidget {
  const DashboardChart({super.key});

  @override
  Widget build(BuildContext context) {
    // Chart logic aquí
  }
}
```

### 8.2 Beneficios

| Beneficio | Descripción |
|---|---|
| **Rebuild selectivo** | Cada widget se reconstruye independientemente |
| **Reutilización** | Puedes reusar widgets en otras partes |
| **Testeabilidad** | Tests más fáciles por widget aislado |
| **Legibilidad** | Cada widget tiene una responsabilidad |

---

## 9. Costo de performance de widgets comunes

| Widget | Costo | Alternativa más liviana |
|---|---|---|
| `Stack` | Medio | `Column` / `Row` si es posible |
| `Positioned` (en Stack) | Medio | `Align` en un Container |
| `Opacity` | Medio-Alto | `AnimatedOpacity` si cambia |
| `ClipRRect` | Medio | `Decoration` con `borderRadius` |
| `ShaderMask` | Alto | Pre-renderizar el efecto |
| `BackdropFilter` | Muy alto | Evitar o usar imagen pre-renderizada |
| `Table` | Medio | `Column` con `Row` custom |
| `RichText` | Bajo | Mejor que múltiples widgets `Text` |
| `Wrap` | Medio | `Row` con `Expanded` si es posible |
| `LayoutBuilder` | Medio | Constraints conocidos = sin LayoutBuilder |

### 9.1 Opacity: el villano silencioso

`Opacity` crea una capa de composición separada en la GPU. No hay problema si es estático, pero **evita aplicarlo sobre subtrees grandes o animarlo con `setState`**.

```dart
// ❌ MAL: Opacity sobre un subtree grande
Opacity(
  opacity: 0.5,
  child: ExpensiveWidget(),
)

// ✅ BIEN: Solo aplica opacidad cuando el valor cambia
AnimatedOpacity(
  opacity: isVisible ? 1 : 0,
  duration: const Duration(milliseconds: 300),
  child: ExpensiveWidget(),
)

// ✅ Si es para deshabilitar interacción, no uses opacidad:
IgnorePointer(
  child: ExpensiveWidget(),  // Sin interacción
)
```

---

## Resumen

| Tema | Técnica clave |
|---|---|
| **Listas largas** | `ListView.builder` obligatorio |
| **Scrolls complejos** | `CustomScrollView` + Slivers |
| **Listas con alto fijo** | `SliverFixedExtentList` |
| **Imágenes** | `cacheWidth` + `cacheHeight` siempre |
| **Carga de imágenes** | `precacheImage` en initState |
| **Animaciones en listas** | `RepaintBoundary` por item |
| **CustomPainter** | `shouldRepaint` con comparación |
| **Widgets pesados** | Extracción a StatelessWidget |
| **Opacity** | Evitar sobre subtrees grandes |

---

## 📚 Referencias

- [Flutter | Slivers](https://docs.flutter.dev/ui/layout/scrolling) — Scrolls avanzados con Slivers
- [Flutter | Imágenes y memoria](https://docs.flutter.dev/perf/images) — `cacheWidth`/`cacheHeight` y cache de imágenes
- [Flutter | CustomPainter](https://api.flutter.dev/flutter/rendering/CustomPainter-class.html) — API de CustomPainter y shouldRepaint

---

> 📖 **Siguiente:** [23-cheatsheet-optimizacion.md](./23-cheatsheet-optimizacion.md) — Cheatsheet de optimización de rendimiento
