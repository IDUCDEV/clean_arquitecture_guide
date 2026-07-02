# 4. Bloc con Eventos y Pantalla Completa

## Diferencia clave con Cubit

```dart
// Cubit: llamas a una función
cubit.incrementar();

// Bloc: agregas un evento
bloc.add(IncrementarEvent());
```

La ventaja del Bloc sobre Cubit es que **cada evento queda registrado** y puedes aplicar transformadores de concurrencia.

## Productos con Bloc

### Eventos

```dart
// lib/features/productos/presentation/bloc/producto_event.dart
import 'package:equatable/equatable.dart';

sealed class ProductoEvent extends Equatable {
  const ProductoEvent();

  @override
  List<Object?> get props => [];
}

final class CargarProductos extends ProductoEvent {
  const CargarProductos();
}

final class CargarMasProductos extends ProductoEvent {
  const CargarMasProductos();
}

final class BuscarProductos extends ProductoEvent {
  final String query;

  const BuscarProductos(this.query);

  @override
  List<Object?> get props => [query];
}

final class RecargarProductos extends ProductoEvent {
  const RecargarProductos();
}
```

### Estados

```dart
// lib/features/productos/presentation/bloc/producto_state.dart
sealed class ProductoState extends Equatable {
  const ProductoState();

  @override
  List<Object?> get props => [];
}

final class ProductoInitial extends ProductoState {
  const ProductoInitial();
}

final class ProductoLoading extends ProductoState {
  const ProductoLoading();
}

final class ProductoLoaded extends ProductoState {
  final List<Producto> items;
  final bool hasMore;
  final bool isLoadingMore;

  const ProductoLoaded({
    required this.items,
    this.hasMore = true,
    this.isLoadingMore = false,
  });

  ProductoLoaded copyWith({
    List<Producto>? items,
    bool? hasMore,
    bool? isLoadingMore,
  }) {
    return ProductoLoaded(
      items: items ?? this.items,
      hasMore: hasMore ?? this.hasMore,
      isLoadingMore: isLoadingMore ?? this.isLoadingMore,
    );
  }

  @override
  List<Object?> get props => [items, hasMore, isLoadingMore];
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

  @override
  List<Object?> get props => [mensaje];
}
```

### Bloc

```dart
// lib/features/productos/presentation/bloc/producto_bloc.dart
import 'package:bloc/bloc.dart';
import 'package:bloc_concurrency/bloc_concurrency.dart';
import 'producto_event.dart';
import 'producto_state.dart';

class ProductoBloc extends Bloc<ProductoEvent, ProductoState> {
  final ProductoRepository _repo;
  int _page = 1;
  static const _limit = 20;

  ProductoBloc({required ProductoRepository repo})
      : _repo = repo,
        super(const ProductoInitial()) {
    on<CargarProductos>(_onCargar);
    on<CargarMasProductos>(_onCargarMas, transformer: droppable());
    on<BuscarProductos>(
      _onBuscar,
      transformer: debounce(const Duration(milliseconds: 400)),
    );
    on<RecargarProductos>(_onRecargar);
  }

  Future<void> _onCargar(
    CargarProductos event,
    Emitter<ProductoState> emit,
  ) async {
    _page = 1;
    emit(const ProductoLoading());

    final result = await _repo.obtenerTodo(page: _page, limit: _limit);

    result.fold(
      (error) => emit(ProductoError(error.mensaje)),
      (items) => emit(ProductoLoaded(
        items: items,
        hasMore: items.length >= _limit,
      )),
    );
  }

  Future<void> _onCargarMas(
    CargarMasProductos event,
    Emitter<ProductoState> emit,
  ) async {
    if (state is! ProductoLoaded) return;
    final current = state as ProductoLoaded;
    if (!current.hasMore || current.isLoadingMore) return;

    _page++;
    emit(current.copyWith(isLoadingMore: true));

    final result = await _repo.obtenerTodo(page: _page, limit: _limit);

    result.fold(
      (error) {
        _page--;
        emit(current.copyWith(isLoadingMore: false));
      },
      (items) {
        emit(current.copyWith(
          items: [...current.items, ...items],
          hasMore: items.length >= _limit,
          isLoadingMore: false,
        ));
      },
    );
  }

  Future<void> _onBuscar(
    BuscarProductos event,
    Emitter<ProductoState> emit,
  ) async {
    if (event.query.isEmpty) {
      add(const CargarProductos());
      return;
    }

    emit(const ProductoLoading());

    final result = await _repo.buscar(event.query);

    result.fold(
      (error) => emit(ProductoError(error.mensaje)),
      (items) => emit(ProductoSearchResult(items: items, query: event.query)),
    );
  }

  Future<void> _onRecargar(
    RecargarProductos event,
    Emitter<ProductoState> emit,
  ) async {
    add(const CargarProductos());
  }
}
```

### Pantalla: lista con búsqueda e infinite scroll

```dart
// lib/features/productos/presentation/pages/productos_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../bloc/producto_bloc.dart';
import '../bloc/producto_event.dart';
import '../bloc/producto_state.dart';

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
      context.read<ProductoBloc>().add(const CargarMasProductos());
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Productos')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: _busquedaCtrl,
              decoration: InputDecoration(
                hintText: 'Buscar productos...',
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
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
              onChanged: (query) {
                context
                    .read<ProductoBloc>()
                    .add(BuscarProductos(query));
              },
            ),
          ),
          Expanded(
            child: BlocBuilder<ProductoBloc, ProductoState>(
              builder: (context, state) {
                return switch (state) {
                  ProductoInitial() => const SizedBox.shrink(),
                  ProductoLoading() => const Center(
                      child: CircularProgressIndicator(),
                    ),
                  ProductoError(:final mensaje) => _ErrorView(
                      mensaje: mensaje,
                      onRetry: () =>
                          context.read<ProductoBloc>().add(const CargarProductos()),
                    ),
                  ProductoLoaded(:final items, :final isLoadingMore) =>
                    _ListaProductos(
                      items: items,
                      isLoadingMore: isLoadingMore,
                      scrollCtrl: _scrollCtrl,
                    ),
                  ProductoSearchResult(:final items) => _ListaProductos(
                      items: items,
                      isLoadingMore: false,
                      scrollCtrl: _scrollCtrl,
                      esBusqueda: true,
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

class _ErrorView extends StatelessWidget {
  final String mensaje;
  final VoidCallback onRetry;

  const _ErrorView({required this.mensaje, required this.onRetry});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            Text(mensaje, textAlign: TextAlign.center),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: const Text('Reintentar'),
            ),
          ],
        ),
      ),
    );
  }
}

class _ListaProductos extends StatelessWidget {
  final List<Producto> items;
  final bool isLoadingMore;
  final ScrollController scrollCtrl;
  final bool esBusqueda;

  const _ListaProductos({
    required this.items,
    required this.isLoadingMore,
    required this.scrollCtrl,
    this.esBusqueda = false,
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
        padding: const EdgeInsets.symmetric(horizontal: 16),
        itemBuilder: (context, index) {
          if (index >= items.length) {
            return const Padding(
              padding: EdgeInsets.all(16),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          return ProductoListTile(producto: items[index]);
        },
      ),
    );
  }
}
```

## Event flows: cómo se conectan

Cuando el usuario escribe en el buscador:

```
1. onChanged → ProductoBloc.add(BuscarProductos('iphone'))
2. Bloc recibe el evento
3. BuscarProductos entra en el handler con debounce(400ms)
4. Si el usuario escribe otra letra antes de 400ms, se reinicia el timer
5. A los 400ms sin escritura, se ejecuta _onBuscar
6. Se emite ProductoSearchResult
7. BlocBuilder reconstruye la UI
```

Esta trazabilidad es imposible con Cubit o Provider.

## Bloc con IDs únicos

```dart
class DetalleBloc extends Bloc<DetalleEvent, DetalleState> {
  DetalleBloc({required ProductoRepository repo, required String productoId})
      : super(DetalleInitial()) {
    on<CargarDetalle>((event, emit) async {
      emit(DetalleLoading());
      final result = await repo.obtenerPorId(productoId);
      result.fold(
        (error) => emit(DetalleError(error.mensaje)),
        (producto) => emit(DetalleLoaded(producto)),
      );
    });
  }
}

// En la UI:
BlocProvider(
  create: (_) => DetalleBloc(repo: getIt(), productoId: widget.id)
    ..add(CargarDetalle()),
  child: const _DetalleView(),
);
```
