# 13. Concurrencia de Eventos y Transformers

> Referencia oficial: [bloc_concurrency](https://pub.dev/packages/bloc_concurrency)

## El problema

Cuando el usuario interactúa rápido, los eventos pueden acumularse:

```dart
// Sin transformer: cada tap encola un evento
// Si el primer evento tarda 2s, los taps se acumulan
on<BuscarProducto>((event, emit) async {
  final results = await repo.buscar(event.query);
  emit(SearchResult(results));
});
```

Los transformers resuelven esto.

## Transformers disponibles

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';
```

| Transformer | Comportamiento | Ideal para |
|---|---|---|
| `concurrent()` | Procesa todos en paralelo | Operaciones independientes |
| `sequential()` | Uno tras otro, en orden | Operaciones ordenadas |
| `droppable()` | Ignora si ya hay uno activo | Refresh, paginación |
| `restartable()` | Cancela el activo y empieza el nuevo | Búsqueda, filtros |
| `debounce(Duration)` | Espera inactividad antes de ejecutar | Búsqueda en tiempo real |

## sequential

```dart
on<GuardarDatos>(
  _onGuardar,
  transformer: sequential(),
);
// Primer guardado: ejecuta
// Segundo guardado: espera a que termine el primero
// Garantiza orden FIFO
```

## droppable

```dart
on<CargarMas>(
  _onCargarMas,
  transformer: droppable(),
);
// Primer load more: ejecuta
// Segundo load more (mientras el primero corre): ignorado
// El usuario hace scroll rápido pero solo carga una página a la vez
```

## restartable

```dart
on<BuscarProducto>(
  _onBuscar,
  transformer: restartable(),
);
// Primer búsqueda: ejecuta (tarda 500ms)
// Segunda búsqueda (100ms después): cancela la primera
// Solo el resultado más reciente importa
```

## debounce

```dart
on<TextoCambiado>(
  _onBuscar,
  transformer: debounce(const Duration(milliseconds: 400)),
);
// Usuario escribe "flu" → timer 400ms
// Usuario escribe "flutter" → resetea timer
// A los 400ms sin escribir → ejecuta búsqueda con "flutter"
// Esto evita llamadas innecesarias mientras el usuario escribe
```

## Combinación: debounce + restartable

Para búsqueda en tiempo real con repositorio:

```dart
class BusquedaBloc extends Bloc<BusquedaEvent, BusquedaState> {
  BusquedaBloc({required ProductoRepository repo}) : super(BusquedaInitial()) {
    on<QueryCambiada>(
      _onQuery,
      transformer: restartable() + debounce(const Duration(milliseconds: 300)),
    );
  }

  Future<void> _onQuery(QueryCambiada event, Emitter<BusquedaState> emit) async {
    if (event.query.isEmpty) {
      emit(const BusquedaInitial());
      return;
    }

    emit(BusquedaCargando());

    try {
      final results = await repo.buscar(event.query);
      emit(BusquedaCompletada(results));
    } catch (e) {
      emit(BusquedaError(e.toString()));
    }
  }
}

// `restartable() + debounce(300ms)` significa:
// 1. El usuario escribe → debounce espera 300ms
// 2. Si escribe más antes de 300ms, reinicia el timer
// 3. A los 300ms sin escribir, ejecuta la búsqueda
// 4. Si el usuario escribe OTRA cosa mientras la búsqueda corre,
//    se cancela la anterior y se programa la nueva
```

## Custom transformer

```dart
// Ejemplo: throttle (un evento cada X tiempo)
EventTransformer<E> throttle<E>(Duration duration) {
  return (events, mapper) {
    return events.throttle(duration).flatMap(mapper);
  };
}

// Uso:
on<ActualizarPosicion>(
  _onActualizar,
  transformer: throttle(const Duration(milliseconds: 100)),
);
```

## ¿Cómo elegir?

| Escenario | Transformer |
|---|---|
| Búsqueda en tiempo real | `debounce(300ms)` |
| Load more / paginación | `droppable()` |
| Filtros dinámicos | `restartable()` |
| Guardar datos secuenciales | `sequential()` |
| Logging / analytics | `concurrent()` |
| Autocompletado | `debounce + restartable` |

## Ejemplo completo

```dart
class ProductoBloc extends Bloc<ProductoEvent, ProductoState> {
  ProductoBloc({required ProductoRepository repo}) : super(ProductoEmpty()) {
    // Carga inicial: sequential (ordenada)
    on<CargarProductos>(
      _onCargar,
      transformer: sequential(),
    );

    // Paginación: droppable (ignora dobles)
    on<CargarMas>(
      _onCargarMas,
      transformer: droppable(),
    );

    // Búsqueda: debounce + restartable
    on<BuscarProducto>(
      _onBuscar,
      transformer: restartable() + debounce(const Duration(milliseconds: 400)),
    );

    // Pull-to-refresh: restartable (cancela si usuario jala varias veces)
    on<RecargarProductos>(
      _onRecargar,
      transformer: restartable(),
    );
  }
}
```
