# 9. Ejemplo: Favoritos Persistidos con HydratedCubit

## Funcionalidad

- Marcar/desmarcar favoritos
- Persistencia automática (al cerrar app, se restauran)
- Animación al cambiar estado
- Contador en AppBar
- Pantalla de favoritos

## Estado

```dart
// presentation/cubit/favorito_state.dart
class FavoritoState extends Equatable {
  final List<Producto> items;

  const FavoritoState(this.items);

  Set<String> get ids => items.map((p) => p.id).toSet();
  bool esFavorito(String id) => ids.contains(id);
  int get cantidad => items.length;

  FavoritoState toggle(Producto producto) {
    if (esFavorito(producto.id)) {
      return FavoritoState(items.where((p) => p.id != producto.id).toList());
    }
    return FavoritoState([...items, producto]);
  }

  @override
  List<Object?> get props => [items];
}
```

## HydratedCubit

```dart
// presentation/cubit/favorito_cubit.dart
import 'package:hydrated_bloc/hydrated_bloc.dart';

class FavoritoCubit extends HydratedCubit<FavoritoState> {
  FavoritoCubit() : super(const FavoritoState([]));

  void toggle(Producto producto) {
    emit(state.toggle(producto));
  }

  bool esFavorito(String id) => state.esFavorito(id);

  void eliminarTodos() => emit(const FavoritoState([]));

  @override
  FavoritoState? fromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List)
        .map((e) => Producto.fromJson(e as Map<String, dynamic>))
        .toList();
    return FavoritoState(items);
  }

  @override
  Map<String, dynamic>? toJson(FavoritoState state) {
    return {'items': state.items.map((p) => p.toJson()).toList()};
  }
}
```

Configuración en `main.dart`:

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final storage = await HydratedStorage.build(
    storageDirectory: await getApplicationDocumentsDirectory(),
  );
  HydratedBloc.storage = storage;
  runApp(const MyApp());
}
```

## Botón de favorito con animación

```dart
// presentation/widgets/boton_favorito.dart
class BotonFavorito extends StatelessWidget {
  final Producto producto;

  const BotonFavorito({super.key, required this.producto});

  @override
  Widget build(BuildContext context) {
    return BlocSelector<FavoritoCubit, FavoritoState, bool>(
      selector: (state) => state.esFavorito(producto.id),
      builder: (context, esFav) {
        return IconButton(
          icon: AnimatedSwitcher(
            duration: const Duration(milliseconds: 250),
            transitionBuilder: (child, anim) => ScaleTransition(
              scale: anim,
              child: child,
            ),
            child: esFav
                ? const Icon(Icons.favorite,
                    key: ValueKey('filled'), color: Colors.red, size: 28)
                : const Icon(Icons.favorite_border,
                    key: ValueKey('border'), color: Colors.grey, size: 28),
          ),
          onPressed: () =>
              context.read<FavoritoCubit>().toggle(producto),
        );
      },
    );
  }
}
```

## Pantalla de producto con favorito

```dart
class ProductoDetallePage extends StatelessWidget {
  final Producto producto;

  const ProductoDetallePage({super.key, required this.producto});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => FavoritoCubit(),
      child: Scaffold(
        appBar: AppBar(
          title: Text(producto.nombre),
          actions: [BotonFavorito(producto: producto)],
        ),
        body: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Image.network(
                  producto.imagenUrl,
                  height: 250,
                  fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) => Container(
                    height: 250,
                    color: Colors.grey[200],
                    child: const Icon(Icons.image, size: 64),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Text(producto.nombre,
                  style: Theme.of(context).textTheme.headlineSmall),
              const SizedBox(height: 8),
              Text('\$${producto.precio}',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                        color: Theme.of(context).colorScheme.primary,
                      )),
              const SizedBox(height: 16),
              Text(producto.descripcion),
            ],
          ),
        ),
      ),
    );
  }
}
```

## Pantalla de favoritos

```dart
class FavoritosPage extends StatelessWidget {
  const FavoritosPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mis Favoritos'),
        actions: [
          BlocSelector<FavoritoCubit, FavoritoState, int>(
            selector: (s) => s.cantidad,
            builder: (context, cant) {
              if (cant == 0) return const SizedBox.shrink();
              return IconButton(
                icon: const Icon(Icons.delete_sweep),
                tooltip: 'Eliminar todos',
                onPressed: () => showDialog(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: const Text('Eliminar favoritos'),
                    content: const Text(
                        '¿Eliminar todos los favoritos?'),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(ctx),
                        child: const Text('Cancelar'),
                      ),
                      TextButton(
                        onPressed: () {
                          context
                              .read<FavoritoCubit>()
                              .eliminarTodos();
                          Navigator.pop(ctx);
                        },
                        child: const Text('Eliminar',
                            style: TextStyle(color: Colors.red)),
                      ),
                    ],
                  ),
                ),
              );
            },
          ),
        ],
      ),
      body: BlocBuilder<FavoritoCubit, FavoritoState>(
        builder: (context, state) {
          if (state.items.isEmpty) {
            return Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.favorite_border,
                      size: 80, color: Colors.grey[400]),
                  const SizedBox(height: 16),
                  Text('Sin favoritos aún',
                      style: TextStyle(
                          fontSize: 18, color: Colors.grey[600])),
                  const SizedBox(height: 8),
                  TextButton(
                    onPressed: () => context.go('/'),
                    child: const Text('Explorar productos'),
                  ),
                ],
              ),
            );
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: state.items.length,
            itemBuilder: (context, index) {
              final producto = state.items[index];
              return Dismissible(
                key: ValueKey(producto.id),
                direction: DismissDirection.endToStart,
                background: Container(
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.only(right: 16),
                  color: Colors.red,
                  child: const Icon(Icons.delete, color: Colors.white),
                ),
                onDismissed: (_) =>
                    context.read<FavoritoCubit>().toggle(producto),
                child: Card(
                  margin: const EdgeInsets.only(bottom: 8),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundImage: NetworkImage(producto.imagenUrl),
                      onBackgroundImageError: (_, __) =>
                          const Icon(Icons.image),
                    ),
                    title: Text(producto.nombre),
                    subtitle: Text('\$${producto.precio}'),
                    trailing: BotonFavorito(producto: producto),
                    onTap: () => context.push('/productos/${producto.id}'),
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
```

## Persistencia en acción

Cuando el usuario cierra la app y la vuelve a abrir:

1. `HydratedBloc.storage` carga el JSON guardado
2. `fromJson` reconstruye `FavoritoState(items: [...])`
3. El Cubit emite el estado restaurado
4. La UI se pinta con los favoritos previos

Sin `HydratedCubit`, los favoritos se perderían al reiniciar la app.

---

## 📚 Referencias

- [bloc | Documentación oficial](https://bloclibrary.dev/) — Guías, tutoriales y API reference
- [flutter_bloc | pub.dev](https://pub.dev/packages/flutter_bloc) — Paquete Flutter de BLoC
- [Bloc Concurrency](https://pub.dev/packages/bloc_concurrency) — Event transformers y concurrencia

---
