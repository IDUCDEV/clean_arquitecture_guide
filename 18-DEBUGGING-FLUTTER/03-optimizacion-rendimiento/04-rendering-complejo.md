# 04 - Rendering Complejo: Optimizacion de Listas, Slivers e Imagenes

## ListView.builder vs ListView

La diferencia mas critica en listas Flutter: **ListView construye todos los items de una vez**, mientras que **ListView.builder solo construye los visibles**.

### ListView (sin builder)

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

### ListView.builder (lazy loading)

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
Memoria usada: MINIMA
```

### Comparacion

| Caracteristica | ListView | ListView.builder |
|---|---|---|
| Items construidos | Todos | Solo visibles |
| Memoria | Lineal con items | Constante |
| Scroll inicial | Instantaneo | Puede tener micro-lag |
| Ideal para | < 20 items | > 20 items |
| Performance | O(n) | O(1) |

### Cuando usar cada uno

```
Cuantos items tiene tu lista?
├── < 10 items → ListView (simple, no hay diferencia)
├── 10-50 items → ListView.builder (precaucion)
├── > 50 items → ListView.builder (obligatorio)
└── Items de tamano variable → ListView.builder + SliverList
```

---

## Slivers: layouts de scroll complejos

Los **Slivers** permiten crear layouts de scroll donde diferentes secciones tienen diferentes comportamientos.

### CustomScrollView

```dart
CustomScrollView(
  slivers: [
    // Header fijo
    SliverAppBar(
      expandedHeight: 200,
      floating: true,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: Text('Mi App'),
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
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: 0.75,
      ),
    ),

    // Footer
    SliverToBoxAdapter(
      child: FooterWidget(),
    ),
  ],
)
```

### Slivers disponibles

| Sliver | Uso | Performance |
|---|---|---|
| `SliverList` | Lista vertical lazy | ✅ Excelente |
| `SliverGrid` | Grid lazy | ✅ Excelente |
| `SliverAppBar` | AppBar con scroll | ✅ Excelente |
| `SliverFixedExtentList` | Lista con items de alto fijo | ✅✅ Mejor que SliverList |
| `SliverPrototypeExtentList` | Lista con prototype de alto | ✅✅ Muy rapido |
| `SliverFillRemaining` | Contenido que llena el espacio restante | ✅ |
| `SliverToBoxAdapter` | Widget normal dentro de CustomScrollView | ✅ |

### SliverFixedExtentList: la version rapida

```dart
// SliverList: calcula constraints por cada item
SliverList(
  delegate: SliverChildBuilderDelegate(
    (context, index) => ListTile(title: Text('Item $index')),
    childCount: 1000,
  ),
)

// SliverFixedExtentList: sabe el alto exacto, mas rapido
SliverFixedExtentList(
  delegate: SliverChildBuilderDelegate(
    (context, index) => ListTile(title: Text('Item $index')),
    childCount: 1000,
  ),
  itemExtent: 56.0,  // ← Alto fijo en pixels
)
```

---

## Optimizacion de imagenes

### cacheWidth y cacheHeight

Cuando cargas una imagen de red, Flutter la decodifica a su tamano original. Si la imagen es de 4000x3000 pero solo necesitas 200x150, estas desperdiciando memoria y CPU.

```dart
// ❌ IMAGEN COMPLETA decodificada (4000x3000 = 12M pixels)
Image.network(
  'https://example.com/photo.jpg',
)

// ✅ IMAGEN REDIMENSIONADA al tamano real de display (200x150 = 30K pixels)
Image.network(
  'https://example.com/photo.jpg',
  width: 200,
  height: 150,
  cacheWidth: 200,  // ← Decodifica a este tamano
  cacheHeight: 150, // ← Ahorra 99% de memoria
)
```

```
Memoria de imagen:

Sin cacheWidth/Height:
  4000 × 3000 × 4 bytes = 48 MB  ← Desperdicio

Con cacheWidth/Height (display: 200x150):
  200 × 150 × 4 bytes = 120 KB   ← 400x menos memoria
```

### AssetImage vs NetworkImage

| Tipo | Carga | Cache | Uso ideal |
|---|---|---|---|
| `AssetImage` | Local, rapida | En memoria | Iconos, logos, backgrounds |
| `NetworkImage` | Remota, lenta | Disco + memoria | Fotos de usuario, contenido |
| `FileImage` | Local, rapida | En memoria | Fotos tomadas con camara |

### precacheImage: cargar imagenes antes de necesitarlas

```dart
@override
void initState() {
  super.initState();

  // Precargar imagen para que aparezca instantaneamente
  precacheImage(
    NetworkImage('https://example.com/hero.jpg'),
    context,
  );
}

@override
Widget build(BuildContext context) {
  return Image.network('https://example.com/hero.jpg');
  // ↑ La imagen ya esta en cache, carga instantanea
}
```

### Patron completo de imagen optimizada

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
    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: Image.network(
        url,
        width: width,
        height: height,
        cacheWidth: (width * MediaQuery.of(context).devicePixelRatio).toInt(),
        cacheHeight: (height * MediaQuery.of(context).devicePixelRatio).toInt(),
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

## ShaderMask y ClipRect: consideraciones de performance

### ShaderMask

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
| Alto si hay animacion | Shader se recalcula continuamente |
| Bajo si es estatico | Una sola vez al renderizar |

### ClipRect

```dart
// ClipRect recorta el contenido a los limits del padre
// Impide que los hijos se dibujen fuera del area
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
| Bajo-Medio | Crea una capa de composicion |
| Alto si anidados | Multiples clip layers = GPU work |

### Reglas de uso

| Widget | Usar cuando... | Evitar cuando... |
|---|---|---|
| `ShaderMask` | Efecto visual necesario | Decoracion sin valor real |
| `ClipRect` | Overflow controlado | Se puede evitar con `overflow: hidden` en Container |
| `ClipRRect` | Bordes redondeados | Usar `Decoration` con `borderRadius` |

---

## RepaintBoundary en listas con animaciones

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
    return RepaintBoundary(  // ← Limita repintado a este item
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

## shouldRepaint en CustomPainter

### Patron basico

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
    // ✅ SOLO repintar si el progress cambio
    return oldDelegate.progress != progress;
  }
}
```

### shouldRepaint: que retornar

| Escenario | Retorno | Razon |
|---|---|---|
| Widget completamente estatico | `return false` | Nunca cambia |
| Depende de un solo campo | `return old.field != field` | Solo repinta si cambia |
| Siempre cambia | `return true` | No hay forma de evitarlo |
| Depende de multiples campos | Comparar todos los campos | Granularidad maxima |

### Ejemplo estatico

```dart
class BackgroundPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    // Dibuja un patron estatico
    final paint = Paint()..color = Colors.grey[200]!;
    for (double i = 0; i < size.width; i += 20) {
      canvas.drawLine(Offset(i, 0), Offset(i, size.height), paint);
    }
  }

  @override
  bool shouldRepaint(BackgroundPainter oldDelegate) {
    return false;  // ← NUNCA repinta, es estatico
  }
}
```

---

## Animaciones: AnimatedContainer vs AnimatedBuilder

### AnimatedContainer

```dart
// ✅ SIMPLE: animacion implicita de propiedades
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  width: isExpanded ? 200 : 100,
  color: isExpanded ? Colors.blue : Colors.red,
  child: Text('Animated'),
)
```

### AnimatedBuilder

```dart
// ✅ COMPLEJO: animacion personalizada
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

### Comparacion

| Caracteristica | AnimatedContainer | AnimatedBuilder |
|---|---|---|
| Complejidad | Baja | Media-Alta |
| Propiedades | Limitadas (width, height, color, etc.) | Cualquier propiedad |
| Performance | Buena | Excelente (con child) |
| Uso ideal | Animaciones de layout | Animaciones custom |

---

## Widgets pesados: splitting build methods

### Patron: extraccion de widgets

```dart
// ❌ MAL: Todo en un solo build method gigante
class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Header (100 lineas de codigo)
        // ...
        // Chart (200 lineas de codigo)
        // ...
        // Table (150 lineas de codigo)
        // ...
        // Footer (50 lineas de codigo)
        // ...
      ],
    );
  }
}

// ✅ BIEN: Widgets extraidos
class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: const [
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
    // Header logic aqui
  }
}

class DashboardChart extends StatelessWidget {
  const DashboardChart({super.key});

  @override
  Widget build(BuildContext context) {
    // Chart logic aqui
  }
}
```

### Beneficios

| Beneficio | Descripcion |
|---|---|
| **Rebuild selectivo** | Cada widget se reconstruye independientemente |
| **Reutilizacion** | Puedes reusar widgets en otras partes |
| **Testeabilidad** | Tests mas faciles por widget aislado |
| **Legibilidad** | Cada widget tiene una responsabilidad |

---

## Costo de performance de widgets comunes

| Widget | Costo | Alternativa mas liviana |
|---|---|---|
| `Stack` | Medio | `Column` / `Row` si es posible |
| `Positioned` (en Stack) | Medio | `Align` en un Container |
| `Opacity` | Alto | `AnimatedOpacity` o `ColorFiltered` |
| `ClipRRect` | Medio | `Decoration` con `borderRadius` |
| `ShaderMask` | Alto | Pre-renderizar el efecto |
| `BackdropFilter` | Muy alto | Evitar o usar imagen pre-renderizada |
| `Table` | Medio | `Column` con `Row` custom |
| `RichText` | Bajo | Mejor que multiples `Text` widget |
| `Wrap` | Medo | `Row` con `Expanded` si es posible |
| `LayoutBuilder` | Medo | Constraints conocidos = sin LayoutBuilder |

### Opacity: el villano silencioso

```dart
// ❌ MAL: Opacity crea una capa separada en GPU
Opacity(
  opacity: 0.5,
  child: ExpensiveWidget(),
)

// ✅ BIEN: ColorFiltered es mas eficiente
ColorFiltered(
  colorFilter: ColorFilter.mode(
    Colors.black.withOpacity(0.5),
    BlendMode.modulate,
  ),
  child: ExpensiveWidget(),
)

// ✅ O mejor: si es para deshabilitar, usar IgnorePointer + opacidad en el painter
IgnorePointer(
  child: ExpensiveWidget(),  // Sin interaccion
)
```

---

## Resumen

| Tema | Tecnica clave |
|---|---|
| **Listas largas** | `ListView.builder` obligatorio |
| **Scrolls complejos** | `CustomScrollView` + Slivers |
| **Listas con alto fijo** | `SliverFixedExtentList` |
| **Imagenes** | `cacheWidth` + `cacheHeight` siempre |
| **Carga de imagenes** | `precacheImage` en initState |
| **Animaciones en listas** | `RepaintBoundary` por item |
| **CustomPainter** | `shouldRepaint` con comparacion |
| **Widgets pesados** | Extraccion a StatelessWidget |
| **Opacity** | Evitar, usar alternativas |
