# 9. Patrones de Renderización

## Renderizado condicional

Tres patrones comunes para mostrar/ocultar widgets.

```dart
// 1. Operador ternario (más común)
child: estado == Estado.cargando
    ? const CircularProgressIndicator()
    : const Text('Listo'),

// 2. if-else en collection (Colecciones)
children: [
  const Text('Items'),
  if (items.isEmpty)
    const Text('No hay items')
  else
    for (final item in items)
      Text(item.nombre),
];

// 3. Visibility widget
Visibility(
  visible: _mostrar,
  child: const Text('Visible'),
  // Mantiene el espacio ocupado si se desea
  maintainState: false,
  maintainSize: false,
);
```

`Visibility` te permite elegir si el widget conserva espacio (`maintainSize`), estado (`maintainState`) o si se descarta del árbol por completo.

## Patrón Loaded / Error / Empty / Loading

Estado visual completo, modelado con un enum o clase sellada.

```dart
sealed class AsyncState<T> {}

class AsyncLoading<T> extends AsyncState<T> {}
class AsyncError<T> extends AsyncState<T> {
  final String message;
  AsyncError(this.message);
}
class AsyncData<T> extends AsyncState<T> {
  final T data;
  AsyncData(this.data);
}

class EstadoVisual<T> extends StatelessWidget {
  final AsyncState<T> estado;
  final Widget Function(T data) builder;

  const EstadoVisual({super.key, required this.estado, required this.builder});

  @override
  Widget build(BuildContext context) {
    return switch (estado) {
      AsyncLoading() => const Center(child: CircularProgressIndicator()),
      AsyncError(:final message) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Error: $message'),
              FilledButton(
                onPressed: () => {}, // reintentar (dispara nueva carga)
                child: const Text('Reintentar'),
              ),
            ],
          ),
        ),
      AsyncData(:final data) when data is List && (data as List).isEmpty =>
        const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.inbox, size: 64, color: Colors.grey),
              SizedBox(height: 16),
              Text('Sin datos'),
            ],
          ),
        ),
      AsyncData(:final data) => builder(data),
    };
  }
}
```

Uso (aquí con una clase de estado propia; en el módulo 16 la misma idea se aplica sobre `BlocBuilder`):

```dart
class ProductosBody extends StatelessWidget {
  final AsyncState<List<Producto>> estado;

  const ProductosBody({super.key, required this.estado});

  @override
  Widget build(BuildContext context) {
    return EstadoVisual(
      estado: estado,
      builder: (productos) => ListView.builder(
        itemCount: productos.length,
        itemBuilder: (context, index) => ListTile(
          title: Text(productos[index].nombre),
        ),
      ),
    );
  }
}
```

## Patrón Shimmer / Skeleton

Placeholder animado mientras carga.

```dart
// pubspec.yaml: shimmer: ^3.0.0

Shimmer.fromColors(
  baseColor: Colors.grey[300]!,
  highlightColor: Colors.grey[100]!,
  child: Column(
    children: [
      _SkeletonLine(width: double.infinity, height: 16),
      const SizedBox(height: 8),
      _SkeletonLine(width: 200, height: 16),
    ],
  ),
);
```

Sin dependencias externas:

```dart
Container(
  width: double.infinity,
  height: 16,
  decoration: BoxDecoration(
    color: Colors.grey[300],
    borderRadius: BorderRadius.circular(4),
  ),
);
```

## Patrón Sliver (scroll dinámico)

Combina listas, grids y headers en un solo scroll.

```dart
CustomScrollView(
  slivers: [
    SliverAppBar.large(
      title: const Text('Galería'),
      pinned: true,
    ),
    SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Text('Últimos productos',
            style: Theme.of(context).textTheme.titleLarge),
      ),
    ),
    SliverGrid(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        mainAxisSpacing: 8,
        crossAxisSpacing: 8,
      ),
      delegate: SliverChildBuilderDelegate(
        (context, index) => _ProductCard(producto: productos[index]),
        childCount: productos.length,
      ),
    ),
  ],
);
```

## Patrón NestedScrollView

Header que colapsa mientras el contenido interno hace scroll.

```dart
NestedScrollView(
  headerSliverBuilder: (context, innerIsScrolled) => [
    SliverAppBar(
      title: const Text('Perfil'),
      expandedHeight: 200,
      flexibleSpace: FlexibleSpaceBar(
        background: Image.network('cover.jpg', fit: BoxFit.cover),
      ),
    ),
    SliverToBoxAdapter(
      child: _InfoTab(),
    ),
  ],
  body: TabBarView(
    children: [
      _PublicacionesTab(),
      _FotosTab(),
      _AmigosTab(),
    ],
  ),
);
```

## Patrón IndexedStack / PageView

Navegación entre vistas sin perder estado.

```dart
// IndexedStack: mantiene todas las vistas montadas
IndexedStack(
  index: _tabIndex,
  children: const [
    HomePage(),
    SearchPage(),
    ProfilePage(),
  ],
);

// PageView: swipe entre páginas
PageView(
  controller: _pageCtrl,
  children: const [
    OnboardingPage1(),
    OnboardingPage2(),
    OnboardingPage3(),
  ],
);
```

## Patrón Overlay / Popup

Superponer widgets sobre la UI actual.

```dart
// Modal bottom sheet
showModalBottomSheet(
  context: context,
  builder: (_) => Wrap(
    children: [
      ListTile(leading: const Icon(Icons.photo), title: const Text('Galería'), onTap: () {}),
      ListTile(leading: const Icon(Icons.camera), title: const Text('Cámara'), onTap: () {}),
    ],
  ),
);

// Tooltip
const Tooltip(
  message: 'Información adicional',
  child: Icon(Icons.info),
);

// PopupMenuButton
PopupMenuButton<String>(
  itemBuilder: (context) => [
    const PopupMenuItem(value: 'edit', child: Text('Editar')),
    const PopupMenuItem(value: 'delete', child: Text('Eliminar')),
  ],
  onSelected: (value) => print(value),
);
```

## Patrón Builder / Callback

Inversión de control: el hijo llama al padre.

```dart
class AccionLista extends StatelessWidget {
  final String itemId;
  final VoidCallback onEdit;
  final VoidCallback onDelete;

  const AccionLista({
    super.key,
    required this.itemId,
    required this.onEdit,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        IconButton(icon: const Icon(Icons.edit), onPressed: onEdit),
        IconButton(icon: const Icon(Icons.delete), onPressed: onDelete),
      ],
    );
  }
}
```


---

## 📚 Referencias

- [Flutter | Widget catalog](https://docs.flutter.dev/ui/widgets) — Catálogo completo de widgets por categoría
- [Flutter | Slivers](https://docs.flutter.dev/ui/layout/scrolling/slivers) — Slivers y scroll dinámico
- [Dart | Pattern matching](https://dart.dev/language/patterns) — `sealed` + `switch` para estados (3.10+)

---

## Lo que sigue

El capítulo 10 cubre rendimiento y buenas prácticas al trabajar con widgets.
