# 16. Buenas Prácticas y Anti-Patrones

## BlocObserver: trazabilidad global

```dart
class AppBlocObserver extends BlocObserver {
  @override
  void onCreate(BlocBase bloc) {
    log('📦 Creado: ${bloc.runtimeType}');
    super.onCreate(bloc);
  }

  @override
  void onChange(BlocBase bloc, Change change) {
    log('🔄 ${bloc.runtimeType}: ${change.nextState}');
    super.onChange(bloc, change);
  }

  @override
  void onTransition(Bloc bloc, Transition transition) {
    log('⚡️ ${bloc.runtimeType}: ${transition.event} → ${transition.nextState}');
    super.onTransition(bloc, transition);
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    log('❌ ${bloc.runtimeType}: $error');
    super.onError(bloc, error, stackTrace);
  }

  @override
  void onClose(BlocBase bloc) {
    log('🗑 Cerrado: ${bloc.runtimeType}');
    super.onClose(bloc);
  }
}

void main() {
  Bloc.observer = AppBlocObserver();
  runApp(const MyApp());
}
```

## Estructura de archivos

```
presentation/
├── cubit/              # o bloc/
│   ├── feature_cubit.dart
│   └── feature_state.dart
└── pages/
    └── feature_page.dart
```

Un solo estado por archivo de estado. Un solo Cubit/Bloc por archivo.

## Naming

| Elemento | Convención | Ejemplo |
|---|---|---|
| Archivo estado | `snake_case_state.dart` | `login_state.dart` |
| Archivo cubit | `snake_case_cubit.dart` | `login_cubit.dart` |
| Clase estado | `LoginState` | `sealed class LoginState` |
| Sub-estados | `LoginInitial`, `LoginLoading`, `LoginSuccess` | |
| Clase cubit | `LoginCubit` | |
| Eventos | `LoginEmailChanged`, `LoginSubmitted` | |

## Estados: sealed class con pattern matching

```dart
// Obliga a manejar todos los casos en la UI
sealed class ProductoState extends Equatable {
  const ProductoState();
}

final class ProductoInitial extends ProductoState {
  const ProductoInitial();
}

final class ProductoLoading extends ProductoState {
  const ProductoLoading();
}

// En la UI:
builder: (context, state) => switch (state) {
  ProductoInitial() => ...,
  ProductoLoading() => ...,
  ProductoLoaded() => ...,
  ProductoError() => ...,
};
```

## Anti-patrones

### 1. Emitir en el constructor

```dart
// MAL
class MiCubit extends Cubit<MiState> {
  MiCubit() : super(MiInitial()) {
    emit(MiLoading()); // ⚠️ emitir en constructor es sospechoso
  }
}

// BIEN: el estado inicial es suficiente
class MiCubit extends Cubit<MiState> {
  MiCubit() : super(MiInitial());

  void cargar() => emit(MiLoading());
}
```

### 2. Llamar al Cubit desde la UI sin Provider

```dart
// MAL
class _MyWidget extends StatelessWidget {
  final MiCubit cubit;
  // Esto obliga a pasar el cubit manualmente
}

// BIEN
class _MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // El cubit viene del BlocProvider en el árbol
    context.read<MiCubit>().accion();
  }
}
```

### 3. Estado mutable

```dart
// MAL
class ProductoLoaded extends ProductoState {
  List<Producto> items; // mutable!
}

// BIEN
class ProductoLoaded extends ProductoState {
  final List<Producto> items; // final
}
```

### 4. Lógica de negocio en la UI

```dart
// MAL
BlocBuilder<LoginCubit, LoginState>(
  builder: (context, state) {
    if (!_validarEmail(email)) return Text('Email inválido');
    // La validación debería estar en el Cubit
  },
);

// BIEN: el Cubit expone los errores
BlocBuilder<LoginCubit, LoginState>(
  builder: (context, state) {
    if (state.emailError != null) return Text(state.emailError);
  },
);
```

### 5. BlocBuilder innecesario

```dart
// MAL: todo el Scaffold se reconstruye
BlocBuilder<MiCubit, MiState>(
  builder: (context, state) => Scaffold(/* ... */),
);

// BIEN: solo la parte que cambia
Scaffold(
  body: BlocBuilder<MiCubit, MiState>(
    builder: (context, state) => _Contenido(state),
  ),
);
```

### 6. Olvidar dispose

```dart
// MAL: controladores no dispuestos
class _FormState extends State<FormWidget> {
  final _ctrl = TextEditingController();
  // falta dispose
}

// BIEN
class _FormState extends State<FormWidget> {
  final _ctrl = TextEditingController();

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }
}
```

### 7. Streams sin cancelar en Bloc

```dart
// MAL: stream subscription nunca se cancela
class ChatBloc extends Bloc<ChatEvent, ChatState> {
  StreamSubscription? _sub;
  // falta cancelar en close()
}

// BIEN
@override
Future<void> close() {
  _sub?.cancel();
  return super.close();
}
```

## Reglas de arquitectura

1. **Un Cubit por feature** (o un Bloc si necesitas eventos)
2. **Un Cubit no conoce a otro Cubit**
3. **La UI coordina**: usa `BlocListener` para orquestar comunicación
4. **Testing obligatorio**: toda la lógica del Cubit debe tener test
5. **Estado inmutable**: nunca modificas, siempre reemplazas
6. **No emitas null**: el estado siempre tiene un valor significativo
7. **BlocProvider en el nivel correcto**: no pongas todo en `main()`, ponlo donde se necesita

## Concurrencia por defecto

| Escenario | Por defecto |
|---|---|
| Bloc sin transformer | `sequential` |
| Load more | `droppable` |
| Búsqueda | `debounce + restartable` |
| Pull-to-refresh | `restartable` |
| Guardar datos | `sequential` |

## DevTools integration

```bash
# Flutter DevTools muestra:
# - Bloc/Cubit instancias activas
# - Transiciones en tiempo real
# - Estado actual de cada instancia
```

En VS Code: extensión "Bloc" para snippets y DevTools integrados.
