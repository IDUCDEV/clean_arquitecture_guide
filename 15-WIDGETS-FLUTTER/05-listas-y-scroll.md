# 5. Listas y Scroll

## ListView

El widget base para listas desplazables.

```dart
// Lista finita con hijos conocidos
ListView(
  children: const [
    ListTile(title: Text('Item 1')),
    ListTile(title: Text('Item 2')),
    ListTile(title: Text('Item 3')),
  ],
);

// Lista infinita (solo construye los visibles)
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(
      title: Text(items[index].nombre),
      subtitle: Text(items[index].descripcion),
      leading: CircleAvatar(child: Text('${index + 1}')),
      onTap: () => _onItemTap(items[index]),
    );
  },
);
```

## ListTile

Widget optimizado para filas de lista.

```dart
ListTile(
  leading: CircleAvatar(
    backgroundImage: NetworkImage(usuario.avatarUrl),
  ),
  title: Text(usuario.nombre),
  subtitle: Text(usuario.email),
  trailing: IconButton(
    icon: const Icon(Icons.more_vert),
    onPressed: () {},
  ),
  onTap: () => _abrirPerfil(usuario),
  selected: usuario.id == seleccionadoId,
);
```

## ListView.separated

Con separadores entre ítems.

```dart
ListView.separated(
  itemCount: productos.length,
  separatorBuilder: (_, __) => const Divider(height: 1),
  itemBuilder: (context, index) {
    return ListTile(title: Text(productos[index].nombre));
  },
);
```

## GridView

Para layouts de cuadrícula.

```dart
// Con número fijo de columnas
GridView.count(
  crossAxisCount: 2,
  mainAxisSpacing: 8,
  crossAxisSpacing: 8,
  padding: const EdgeInsets.all(8),
  children: [
    for (final item in items)
      Card(child: Center(child: Text(item.nombre))),
  ],
);

// Con tamaño dinámico
GridView.builder(
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 2,
    childAspectRatio: 0.8,
  ),
  itemCount: items.length,
  itemBuilder: (context, index) => _ItemCard(item: items[index]),
);
```

## CustomScrollView + Slivers

Scroll avanzado con efectos combinados.

```dart
CustomScrollView(
  slivers: [
    SliverAppBar(
      title: const Text('Mi App'),
      pinned: true,
      expandedHeight: 200,
      flexibleSpace: FlexibleSpaceBar(
        background: Image.network('https://ejemplo.com/banner.jpg',
          fit: BoxFit.cover),
      ),
    ),
    SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Text('Sección especial'),
      ),
    ),
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => ListTile(title: Text('Item $index')),
        childCount: 50,
      ),
    ),
    SliverGrid(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
      ),
      delegate: SliverChildBuilderDelegate(
        (context, index) => Card(child: Center(child: Text('$index'))),
        childCount: 12,
      ),
    ),
  ],
);
```

> Nota: en la vista scrollable, `cacheExtent` está deprecado desde Flutter 3.44 (los viewports ahora calculan su caché automáticamente). No lo declares.

## CarouselView (3.35+)

Carrusel de tarjetas con scroll por páginas, construido sobre la familia de scroll.

```dart
CarouselView(
  itemSnapping: true,
  itemExtent: 280,
  children: [
    for (final banner in banners)
      _BannerCard(banner: banner),
  ],
);
```

## Pull to refresh

```dart
Future<void> _recargar() async {
  // Carga tu data; RefreshIndicator muestra el spinner mientras espera
  final data = await cargarProductos();
  if (mounted) setState(() => _productos = data);
}

RefreshIndicator(
  onRefresh: _recargar,
  child: ListView.builder(
    itemCount: _productos.length,
    itemBuilder: (context, index) => ListTile(
      title: Text(_productos[index].nombre),
    ),
  ),
);
```

## Infinite scroll (paginación)

Con un `StatefulWidget` + `ScrollController`, sin librerías externas.

```dart
class _ProductosListaState extends State<ProductosLista> {
  final _scrollCtrl = ScrollController();
  final _items = <Producto>[];
  bool _isLoadingMore = false;

  @override
  void initState() {
    super.initState();
    _scrollCtrl.addListener(_onScroll);
    _cargarPagina();
  }

  @override
  void dispose() {
    _scrollCtrl.removeListener(_onScroll);
    _scrollCtrl.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollCtrl.position.pixels >=
        _scrollCtrl.position.maxScrollExtent - 200) {
      _cargarPagina();
    }
  }

  Future<void> _cargarPagina() async {
    if (_isLoadingMore) return;
    _isLoadingMore = true;
    final nuevos = await cargarProductos(
      offset: _items.length,
    );
    if (mounted) {
      setState(() {
        _items.addAll(nuevos);
        _isLoadingMore = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: _scrollCtrl,
      itemCount: _items.length + (_isLoadingMore ? 1 : 0),
      itemBuilder: (context, index) {
        if (index >= _items.length) {
          return const Center(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: CircularProgressIndicator(),
            ),
          );
        }
        return ListTile(title: Text(_items[index].nombre));
      },
    );
  }
}
```

## ScrollController utilidades

```dart
// Scroll a posición específica
_scrollCtrl.animateTo(
  0, // tope
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
);

// Detectar si está en el tope
bool get estaEnTope => _scrollCtrl.position.pixels <= 0;

// Scroll infinito con ScrollNotification
NotificationListener<ScrollNotification>(
  onNotification: (notification) {
    if (notification is ScrollEndNotification &&
        _scrollCtrl.position.pixels >=
            _scrollCtrl.position.maxScrollExtent) {
      _cargarPagina();
    }
    return false;
  },
  child: ListView.builder(/* ... */),
);
```

## SingleChildScrollView

Para contenido que no es lista pero puede desbordar.

```dart
SingleChildScrollView(
  padding: const EdgeInsets.all(16),
  child: Column(
    children: [
      _FormularioCompleto(),
      const SizedBox(height: 24),
      _TerminosYCondiciones(),
    ],
  ),
);
```

## AnimatedList

Lista con animaciones de inserción/eliminación.

```dart
final _listKey = GlobalKey<AnimatedListState>();

AnimatedList(
  key: _listKey,
  initialItemCount: items.length,
  itemBuilder: (context, index, animation) {
    return SizeTransition(
      sizeFactor: animation,
      child: ListTile(title: Text(items[index])),
    );
  },
);

// Insertar
_listKey.currentState!.insertItem(
  index,
  duration: const Duration(milliseconds: 300),
);

// Eliminar
_listKey.currentState!.removeItem(
  index,
  (context, animation) => SizeTransition(
    sizeFactor: animation,
    child: ListTile(title: Text(items[index])),
  ),
);
```

Existe la variante sliver `SliverAnimatedList` para usarla dentro de un `CustomScrollView`.

## ReorderableListView

Lista reordenable por drag & drop.

```dart
ReorderableListView(
  onReorder: (oldIndex, newIndex) {
    setState(() {
      if (newIndex > oldIndex) newIndex--;
      final item = _items.removeAt(oldIndex);
      _items.insert(newIndex, item);
    });
  },
  children: [
    for (final item in _items)
      ListTile(
        key: ValueKey(item.id), // key obligatoria
        title: Text(item.nombre),
      ),
  ],
);
```


---

## 📚 Referencias

- [Flutter | ListView](https://api.flutter.dev/flutter/widgets/ListView-class.html) — API de ListView y variantes
- [Flutter | Slivers](https://docs.flutter.dev/ui/layout/scrolling/slivers) — Guía de slivers y CustomScrollView
- [Flutter | CarouselView](https://api.flutter.dev/flutter/material/CarouselView-class.html) — Carrusel de contenido (3.35+)
- [Flutter | AnimatedList](https://api.flutter.dev/flutter/widgets/AnimatedList-class.html) — Listas con animaciones

---

## Lo que sigue

El capítulo 6 cubre datos, estados y ciclo de vida: cómo fluye la información en una app Flutter.
