# 2. BLoC vs Otros State Management

## Tabla comparativa

| Enfoque | Boilerplate | Curva | Escalabilidad | Testing | Ideal para |
|---|---|---|---|---|---|
| `setState` | Mínimo | Baja | Mala | Difícil | Widgets aislados, animaciones |
| `ValueNotifier` | Bajo | Baja | Media | Fácil | Estado local compartido |
| `InheritedWidget` | Medio | Media | Media | Media | Temas, locale, dependencias |
| **Provider** | Bajo | Baja | Media | Fácil | Apps pequeñas, prototipos |
| **Riverpod** | Bajo | Media | Alta | Fácil | Apps medianas/grandes |
| **BLoC/Cubit** | Medio | Media | Alta | Muy fácil | Apps enterprise, multi-equipo |
| **RxDart** | Alto | Alta | Alta | Media | Streams complejos |
| **GetX** | Bajo | Baja | Baja | Difícil | Prototipos rápidos |

## setState

```dart
class ContadorWidget extends StatefulWidget {
  @override
  State<ContadorWidget> createState() => _ContadorWidgetState();
}

class _ContadorWidgetState extends State<ContadorWidget> {
  int _contador = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('$_contador'),
        FilledButton(
          onPressed: () => setState(() => _contador++),
          child: const Text('+'),
        ),
      ],
    );
  }
}
```

**Pros**: Simple, no dependencias.
**Contras**: Acopla estado a UI, difícil compartir estado, reconstruye todo el widget.

Usa `setState` para: estado efímero local (toggle, animación interna).

## ValueNotifier + ValueListenableBuilder

```dart
final contador = ValueNotifier<int>(0);

ValueListenableBuilder<int>(
  valueListenable: contador,
  builder: (context, valor, child) {
    return Text('$valor');
  },
);
```

**Pros**: Sin dependencias externas, fácil de compartir.
**Contras**: Sin estructura para lógica compleja.

Usa `ValueNotifier` para: un solo valor que cambia, preferencias simples.

## Provider

```dart
class ContadorProvider extends ChangeNotifier {
  int _valor = 0;
  int get valor => _valor;

  void incrementar() {
    _valor++;
    notifyListeners();
  }
}

// Consumo
final provider = context.watch<ContadorProvider>();
```

**Pros**: Simple, conocido, oficial (al menos lo fue).
**Contras**: `ChangeNotifier` no es reactivo, falta de inmutabilidad forzada, sin trazabilidad.

## BLoC/Cubit (nuestra elección)

```dart
class ContadorCubit extends Cubit<int> {
  ContadorCubit() : super(0);

  void incrementar() => emit(state + 1);
}

// Consumo
BlocBuilder<ContadorCubit, int>(
  builder: (context, valor) => Text('$valor'),
);
```

**Pros**: Inmutable por diseño, streams reactivos, trazabilidad total (BlocObserver), testeable (blocTest), escalable, separación forzada UI/lógica, soporte oficial del equipo de Flutter en google3.

**Contras**: Más boilerplate que Provider, requiere entender streams.

## ¿Por qué BLoC para este curso?

1. **Testing nativo**: `blocTest` es una de las mejores DX de testing en Flutter
2. **Separación forzada**: No puedes "accidentalmente" poner lógica en la UI
3. **Trazabilidad**: BlocObserver + DevTools = sabes exactamente qué pasó
4. **Escalabilidad**: Usado por Google, Sony, BMW,阿里巴巴
5. **Coexiste con Clean Architecture**: Los cubits son la capa de presentación ideal

## ¿Cuándo NO usar BLoC?

- Prototipos de 1 día → Provider o Riverpod
- Widget con estado puramente local → `ValueNotifier`
- App ya en producción con GetX → migrar gradualmente, no reescribir
- Equipo que recién empieza Flutter → aprender con setState primero

## Regla práctica

```dart
// Estado local de un widget → ValueNotifier
final toggle = ValueNotifier(false);

// Estado compartido simple → Cubit
class TemaCubit extends Cubit<Tema> { ... }

// Lógica con eventos → Bloc
class BusquedaBloc extends Bloc<BusquedaEvent, BusquedaState> { ... }
```

En los siguientes capítulos trabajaremos exclusivamente con BLoC/Cubit.
