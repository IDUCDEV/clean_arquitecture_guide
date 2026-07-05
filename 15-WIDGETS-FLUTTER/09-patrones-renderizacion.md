# 9. Patrones de Renderización

## Renderizado condicional

Tres patrones comunes para mostrar/ocultar widgets.

```dart
// 1. Operador ternario (más común)
child: state.isLoading
    ? const CircularProgressIndicator()
    : const Text('Listo'),

// 2. if-else en collection if (Colecciones)
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

## Patrón Loaded / Error / Empty / Loading

Estado visual completo.

```dart
class EstadoVisual extends StatelessWidget {
  final String? error;
  final bool isLoading;
  final List<dynamic> data;
  final Widget Function() builder;

  const EstadoVisual({
    super.key,
    this.error,
    required this.isLoading,
    required this.data,
    required this.builder,
  });

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (error != null) {
      return Center(child: Text('Error: $error'));
    }
    if (data.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.inbox, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('Sin datos'),
          ],
        ),
      );
    }
    return builder();
  }
}
```

Uso:

```dart
BlocBuilder<MiCubit, MiState>(
  builder: (context, state) {
    return EstadoVisual(
      isLoading: state is Loading,
      error: state is Error ? state.message : null,
      data: state is Data ? state.items : [],
      builder: () => ListView(/* ... */),
    );
  },
);
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

Combina lists, grids y headers en un solo scroll.

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
- [Flutter | API reference](https://api.flutter.dev/) — Documentación de la API de Flutter
- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter

---

## Lo que sigue

El capítulo 10 cubre rendimiento y buenas prácticas al trabajar con widgets.
