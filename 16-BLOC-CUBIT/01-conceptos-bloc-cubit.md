# 1. Conceptos: BLoC y Cubit

> Referencia oficial: [bloclibrary.dev](https://bloclibrary.dev)

## ¿Qué es BLoC?

**BLoC** (Business Logic Component) es un patrón de manejo de estado que separa la lógica de negocio de la UI usando **streams**. Fue creado por Felix Angelov y Google Ads para manejar estado complejo de forma predecible.

### Principio fundamental

```
Evento → BLoC/Cubit → Estado (vía Stream) → UI
```

La UI **nunca** modifica el estado directamente. Solo notifica al BLoC (evento o llamada a función) y este emite un nuevo estado a través de un stream.

## Streams

Un `Stream` es una secuencia de datos asíncronos. BLoC se apoya completamente en streams.

```dart
// Un stream es así de simple:
final stream = Stream<int>.fromIterable([1, 2, 3]);
stream.listen((valor) => print(valor)); // 1, 2, 3

// BLoC envuelve esta lógica:
// - Cubit emite estados con emit()
// - Bloc emite estados usando Emitter
```

## Cubit

**Cubit** es la variante más simple de BLoC. No usa eventos, solo funciones que emiten estados.

```
Llamada a función → Cubit → emit(NuevoEstado)
```

```dart
class ContadorCubit extends Cubit<int> {
  ContadorCubit() : super(0); // estado inicial

  void incrementar() => emit(state + 1); // emite nuevo estado
  void decrementar() => emit(state - 1);
}
```

Usa `Cubit` cuando:
- La lógica es simple (CRUD básico, toggle, contador)
- Cada "acción" se traduce directamente a un estado
- No necesitas tracear eventos

## Bloc

**Bloc** usa eventos como entrada. Cada evento se mapea a cero o más estados.

```
Evento (add) → Bloc → on<Evento> → emit(NuevoEstado)
```

```dart
sealed class ContadorEvent {}

final class Incrementar extends ContadorEvent {}
final class Decrementar extends ContadorEvent {}

class ContadorBloc extends Bloc<ContadorEvent, int> {
  ContadorBloc() : super(0) {
    on<Incrementar>((event, emit) => emit(state + 1));
    on<Decrementar>((event, emit) => emit(state - 1));
  }
}
```

Usa `Bloc` cuando:
- Necesitas tracear cada acción (auditoría, debugging)
- Tienes múltiples fuentes de entrada
- Necesitas control de concurrencia (droppable, restartable, debounce)

## Comparación rápida

| Aspecto | Cubit | Bloc |
|---|---|---|
| Entrada | Llamada a función | Evento (`bloc.add(Evento)`) |
| Código | Menos boilerplate | Más verboso, más control |
| Trazabilidad | Solo estados | Eventos + estados |
| Concurrencia | No nativa | Event transformers |
| Testing | `blocTest` | `blocTest` |
| Ideal para | CRUD, formularios, toggles | Búsquedas, paginación, streams externos |

## Estado inmutable

Siempre los estados deben ser **inmutables**. Nunca modifiques el estado actual, crea uno nuevo.

```dart
// MAL
emit(state..items.add(nuevoItem));

// BIEN
emit(ProductoLoaded(items: [...state.items, nuevoItem]));
```

## Transiciones

Cada cambio de estado es una **transición**. BLoC la registra automáticamente:

```
{ currentState: 0, event: Incrementar, nextState: 1 }
```

Esto permite herramientas como `BlocObserver` y `BlocDevTools` para depuración.

## Flujo completo

```
1. UI: user tap → context.read<MiCubit>().accion()
2. Cubit: función → emit(NuevoEstado())
3. Stream: NuevoEstado viaja por el stream
4. UI: BlocBuilder se actualiza con NuevoEstado
```

En los próximos capítulos veremos cada pieza en detalle con ejemplos prácticos.
