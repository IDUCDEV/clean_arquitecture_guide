# 8. Ejemplo: Lista con Búsqueda y Filtros

## Funcionalidad

- Lista de productos paginada
- Búsqueda en tiempo real con debounce
- Filtros por categoría
- Pull-to-refresh
- LEER states completos

## Bloc con eventos

```dart
// presentation/bloc/producto_event.dart
sealed class ProductoEvent extends Equatable {
  const ProductoEvent();
  @override List<Object?> get props => [];
}

final class CargarProductos extends ProductoEvent {
  const CargarProductos();
}

final class CargarMas extends ProductoEvent {
  const CargarMas();
}

final class BuscarProducto extends ProductoEvent {
  final String query;
  const BuscarProducto(this.query);
  @override List<Object?> get props => [query];
}

final class FiltrarCategoria extends ProductoEvent {
  final String? categoria;
  const FiltrarCategoria(this.categoria);
  @override List<Object?> get props => [categoria];
}

final class RecargarProductos extends ProductoEvent {
  const RecargarProductos();
}
```

```dart
// presentation/bloc/producto_state.dart
sealed class ProductoState extends Equatable {
  const ProductoState();
  @override List<Object?> get props => [];
}

final class ProductoEmpty extends ProductoState {
  const ProductoEmpty();
}

final class ProductoLoading extends ProductoState {
  const ProductoLoading();
}

final class ProductoLoaded extends ProductoState {
  final List<Producto> items;
  final List<String> categorias;
  final String? categoriaActiva;
  final bool hasMore;
  final bool isLoadingMore;

  const ProductoLoaded({
    required this.items,
    this.categorias = const [],
    this.categoriaActiva,
    this.hasMore = true,
    this.isLoadingMore = false,
  });

  List<Producto> get filtrados => categoriaActiva == null
      ? items
      : items.where((p) => p.categoria == categoriaActiva).toList();

  ProductoLoaded copyWith({
    List<Producto>? items,
    List<String>? categorias,
    String? Function()? categoriaActiva,
    bool? hasMore,
    bool? isLoadingMore,
  }) {
    return ProductoLoaded(
      items: items ?? this.items,
      categorias: categorias ?? this.categorias,
      categoriaActiva: categoriaActiva != null
          ? categoriaActiva()
          : this.categoriaActiva,
      hasMore: hasMore ?? this.hasMore,
      isLoadingMore: isLoadingMore ?? this.isLoadingMore,
    );
  }

  @override
  List<Object?> get props =>
      [items, categorias, categoriaActiva, hasMore, isLoadingMore];
}

final class ProductoSearchResult extends ProductoState {
  final List<Producto> items;
  final String query;

  const ProductoSearchResult({required this.items, required this.query});

  @override
  List<Object?> get props => [items, query];
}

final class ProductoError extends ProductoState {
  final String mensaje;
  const ProductoError(this.mensaje);
  @override List<Object?> get props => [mensaje];
}
```

```dart
// presentation/bloc/producto_bloc.dart
import 'package:bloc_concurrency/bloc_concurrency.dart';

class ProductoBloc extends Bloc<ProductoEvent, ProductoState> {
  final ProductoRepository _repo;
  int _page = 1;
  static const _limit = 20;

  ProductoBloc({required ProductoRepository repo})
      : _repo = repo,
        super(const ProductoEmpty()) {
    on<CargarProductos>(_onCargar);
    on<CargarMas>(_onCargarMas, transformer: droppable());
    on<BuscarProducto>(
      _onBuscar,
      transformer: debounce(const Duration(milliseconds: 400)),
    );
    on<FiltrarCategoria>(_onFiltrar);
    on<RecargarProductos>(_onRecargar);
  }

  Future<void> _onCargar(
      CargarProductos event, Emitter<ProductoState> emit) async {
    _page = 1;
    emit(const ProductoLoading());
    final result = await _repo.obtenerTodo(page: _page, limit: _limit);
    result.fold(
      (e) => emit(ProductoError(e.mensaje)),
      (items) {
        final cats = items.map((p) => p.categoria).toSet().toList()..sort();
        emit(ProductoLoaded(items: items, categorias: cats));
      },
    );
  }

  Future<void> _onCargarMas(
      CargarMas event, Emitter<ProductoState> emit) async {
    if (state is! ProductoLoaded) return;
    final current = state as ProductoLoaded;
    if (!current.hasMore || current.isLoadingMore) return;
    _page++;
    emit(current.copyWith(isLoadingMore: true));
    final result = await _repo.obtenerTodo(page: _page, limit: _limit);
    result.fold(
      (e) {
        _page--;
        emit(current.copyWith(isLoadingMore: false));
      },
      (items) => emit(current.copyWith(
        items: [...current.items, ...items],
        hasMore: items.length >= _limit,
        isLoadingMore: false,
      )),
    );
  }

  Future<void> _onBuscar(
      BuscarProducto event, Emitter<ProductoState> emit) async {
    if (event.query.isEmpty) {
      add(const CargarProductos());
      return;
    }
    emit(const ProductoLoading());
    final result = await _repo.buscar(event.query);
    result.fold(
      (e) => emit(ProductoError(e.mensaje)),
      (items) => emit(ProductoSearchResult(items: items, query: event.query)),
    );
  }

  void _onFiltrar(FiltrarCategoria event, Emitter<ProductoState> emit) {
    if (state is! ProductoLoaded) return;
    final current = state as ProductoLoaded;
    emit(current.copyWith(
      categoriaActiva: () =>
          current.categoriaActiva == event.categoria ? null : event.categoria,
    ));
  }

  Future<void> _onRecargar(
      RecargarProductos event, Emitter<ProductoState> emit) async {
    add(const CargarProductos());
  }
}
```

## Pantalla completa

```dart
// presentation/pages/productos_page.dart
class ProductosPage extends StatelessWidget {
  const ProductosPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => ProductoBloc(repo: getIt())..add(const CargarProductos()),
      child: const _ProductosView(),
    );
  }
}

class _ProductosView extends StatefulWidget {
  const _ProductosView();

  @override
  State<_ProductosView> createState() => _ProductosViewState();
}

class _ProductosViewState extends State<_ProductosView> {
  final _scrollCtrl = ScrollController();
  final _busquedaCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _scrollCtrl.addListener(_onScroll);
  }

  @override
  void dispose() {
    _scrollCtrl.removeListener(_onScroll);
    _scrollCtrl.dispose();
    _busquedaCtrl.dispose();
    super.dispose();
  }

  void _onScroll() {
    if (_scrollCtrl.position.pixels >=
        _scrollCtrl.position.maxScrollExtent - 200) {
      context.read<ProductoBloc>().add(const CargarMas());
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Productos')),
      body: Column(
        children: [
          // Barra de búsqueda
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
            child: TextField(
              controller: _busquedaCtrl,
              decoration: InputDecoration(
                hintText: 'Buscar...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _busquedaCtrl.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _busquedaCtrl.clear();
                          context
                              .read<ProductoBloc>()
                              .add(const CargarProductos());
                        },
                      )
                    : null,
                border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12)),
              ),
              onChanged: (v) =>
                  context.read<ProductoBloc>().add(BuscarProducto(v)),
            ),
          ),
          // Filtros de categoría
          BlocSelector<ProductoBloc, ProductoState, List<String>>(
            selector: (s) =>
                s is ProductoLoaded ? s.categorias : [],
            builder: (context, cats) {
              if (cats.isEmpty) return const SizedBox.shrink();
              return SizedBox(
                height: 48,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.all(8),
                  children: [
                    for (final cat in cats)
                      Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: BlocSelector<ProductoBloc, ProductoState, bool>(
                          selector: (s) =>
                              s is ProductoLoaded &&
                              s.categoriaActiva == cat,
                          builder: (context, activo) {
                            return FilterChip(
                              label: Text(cat),
                              selected: activo,
                              onSelected: (_) => context
                                  .read<ProductoBloc>()
                                  .add(FiltrarCategoria(cat)),
                            );
                          },
                        ),
                      ),
                  ],
                ),
              );
            },
          ),
          // Lista
          Expanded(
            child: BlocBuilder<ProductoBloc, ProductoState>(
              builder: (context, state) {
                return switch (state) {
                  ProductoEmpty() => const SizedBox.shrink(),
                  ProductoLoading() => const Center(
                      child: CircularProgressIndicator()),
                  ProductoError(:final mensaje) => Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(mensaje),
                          FilledButton(
                            onPressed: () => context
                                .read<ProductoBloc>()
                                .add(const CargarProductos()),
                            child: const Text('Reintentar'),
                          ),
                        ],
                      ),
                    ),
                  ProductoLoaded(:final filtrados, :final isLoadingMore) =>
                    _Lista(
                      items: filtrados,
                      isLoadingMore: isLoadingMore,
                      scrollCtrl: _scrollCtrl,
                    ),
                  ProductoSearchResult(:final items) =>
                    items.isEmpty
                        ? const Center(child: Text('Sin resultados'))
                        : _Lista(
                            items: items,
                            isLoadingMore: false,
                            scrollCtrl: _scrollCtrl,
                          ),
                };
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _Lista extends StatelessWidget {
  final List<Producto> items;
  final bool isLoadingMore;
  final ScrollController scrollCtrl;

  const _Lista({
    required this.items,
    required this.isLoadingMore,
    required this.scrollCtrl,
  });

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: () async {
        context.read<ProductoBloc>().add(const RecargarProductos());
      },
      child: ListView.builder(
        controller: scrollCtrl,
        itemCount: items.length + (isLoadingMore ? 1 : 0),
        padding: const EdgeInsets.all(16),
        itemBuilder: (context, index) {
          if (index >= items.length) {
            return const Padding(
              padding: EdgeInsets.all(16),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          return Card(
            margin: const EdgeInsets.only(bottom: 8),
            child: ListTile(
              leading: CircleAvatar(child: Text(items[index].nombre[0])),
              title: Text(items[index].nombre),
              subtitle: Text('\$${items[index].precio}'),
              trailing: Chip(label: Text(items[index].categoria)),
              onTap: () => context.push('/productos/${items[index].id}'),
            ),
          );
        },
      ),
    );
  }
}
```
