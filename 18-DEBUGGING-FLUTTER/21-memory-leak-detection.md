# 21 — Detección y Prevención de Memory Leaks

> Qué es un memory leak, cómo detectarlo con DevTools Memory y qué patrones aplicar para prevenirlo.

---

## 1. ¿Qué es un memory leak en Flutter?

Un **memory leak** ocurre cuando tu app asigna memoria pero nunca la libera, aunque ya no la necesita. En Flutter, esto sucede cuando los recursos (streams, controllers, suscripciones) no se cierran correctamente en `dispose()`.

```
Memoria normal:
  Asignada ──────┐
                 │
  Liberada ──────┘  ← La memoria se recicla

Memory leak:
  Asignada ─────────────────────────────────────
                  ↑ Nunca se libera
  Liberada: (nunca)
```

---

## 2. Tipos de memory leaks en Flutter

| Tipo | Causa | Síntoma |
|---|---|---|
| **Stream abierto** | `StreamSubscription` no cancelada | Memoria crece con cada evento |
| **Controller no disposed** | `TextEditingController` sin dispose | Memoria no liberada al salir |
| **Timer/Animation sin cancel** | `Timer.periodic` o `AnimationController` sin detener | CPU + memoria creciente |
| **Listener no removido** | `WidgetsBindingObserver` sin remove | Referencia circular |
| **Closure que captura context** | Lambda que mantiene referencia al widget | Widget no se destruye |
| **GlobalKey no removida** | GlobalKey en widget temporal | Estado se mantiene en memoria |

### 2.1 Cómo se manifiestan

```
Memory leak creciente:
  Memoria (MB)
  300 │                                    ╱╲╱╲╱╲
  250 │                            ╱╲╱╲╱╲╱
  200 │                    ╱╲╱╲╱╲╱
  150 │            ╱╲╱╲╱╲╱
  100 │    ╱╲╱╲╱╲╱
   50 │╱╲╱╱
      └──────────────────────────────────────── Time
      Navegas entre pantallas →

  La memoria sube pero NUNCA baja → LEAK
```

---

## 3. Detección con DevTools Memory

### 3.1 Paso 1: tomar un heap snapshot

1. Abre DevTools → **Memory** view
2. Navega a la pantalla que sospechas
3. Presiona **"Take heap snapshot"** (icono de cámara 📸)
4. Este es tu snapshot base

### 3.2 Paso 2: tomar un diff snapshot

1. Navega fuera de la pantalla y de vuelta (repite 3-5 veces)
2. Presiona **"Take heap snapshot"** de nuevo
3. Los objetos que **aumentan** entre snapshots son candidatos a leak

### 3.3 Paso 3: allocation sampling

1. Activa **Allocation sampling** (botón de grabar)
2. Interactúa con la app normalmente
3. Detén el sampling
4. Revisa las clases con **mayor crecimiento** de instancias

### 3.4 Flujo de detección

```
┌─────────────────────────────────────────────┐
│           DETECCIÓN DE MEMORY LEAKS         │
│                                             │
│  1. Tomar snapshot base                     │
│     │                                       │
│     ▼                                       │
│  2. Navegar 5x a la pantalla sospechosa     │
│     │                                       │
│     ▼                                       │
│  3. Tomar diff snapshot                     │
│     │                                       │
│     ▼                                       │
│  4. Buscar clases con crecimiento           │
│     │                                       │
│     ├── Sin crecimiento → No hay leak       │
│     └── Con crecimiento → Investigar:       │
│         ├── StreamSubscription?             │
│         ├── TextEditingController?          │
│         ├── AnimationController?            │
│         └── Timer.periodic?                 │
│                                             │
│  5. Verificar que dispose() cierre todo     │
└─────────────────────────────────────────────┘
```

---

## 4. Patrón correcto de dispose() en StatefulWidget

```dart
class _MyWidgetState extends State<MyWidget> {
  // Controllers que necesitan dispose
  late TextEditingController _textController;
  late ScrollController _scrollController;
  late AnimationController _animController;
  late StreamSubscription _subscription;

  @override
  void initState() {
    super.initState();

    // Inicializar controllers
    _textController = TextEditingController();
    _scrollController = ScrollController();
    _animController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    );

    // Suscribirse a streams
    _subscription = myStream.listen((data) {
      // Manejar datos
    });
  }

  @override
  void dispose() {
    // ❗ Cerrar TODOS los recursos en orden inverso
    _subscription.cancel();
    _animController.dispose();
    _scrollController.dispose();
    _textController.dispose();

    super.dispose();
  }
}
```

### 4.1 Regla de oro

> **Si creaste un controller o te suscribiste a un stream, DEBES cerrarlo en dispose().**

---

## 5. Gestión de StreamSubscription

### 5.1 Patrón básico

```dart
class _ChatState extends State<Chat> {
  StreamSubscription? _messagesSubscription;

  @override
  void initState() {
    super.initState();
    _messagesSubscription = Supabase.instance.client
        .from('messages')
        .stream(primaryKey: ['id'])
        .order('created_at')
        .listen((messages) {
          setState(() {
            _messages = messages;
          });
        });
  }

  @override
  void dispose() {
    _messagesSubscription?.cancel();  // ← Cancelar suscripción
    super.dispose();
  }
}
```

### 5.2 Patrón con BLoC

```dart
class ChatBloc extends Bloc<ChatEvent, ChatState> {
  final ChatRepository _repository;
  StreamSubscription? _messagesSubscription;

  ChatBloc(this._repository) : super(ChatInitial()) {
    on<StartListening>(_onStartListening);
    on<StopListening>(_onStopListening);
    on<MessageReceived>(_onMessageReceived);
  }

  void _onStartListening(StartListening event, Emitter<ChatState> emit) {
    _messagesSubscription = _repository.getMessages().listen(
      (messages) => add(MessageReceived(messages)),
    );
  }

  @override
  Future<void> close() {
    _messagesSubscription?.cancel();  // ← Cerrar en close()
    return super.close();
  }
}
```

---

## 6. Ciclo de vida de controllers comunes

### 6.1 TextEditingController

```dart
// ✅ Patrón correcto
late TextEditingController _controller;

@override
void initState() {
  super.initState();
  _controller = TextEditingController(text: 'initial');
}

@override
void dispose() {
  _controller.dispose();  // ← Siempre dispose
  super.dispose();
}
```

### 6.2 ScrollController

```dart
// ✅ Patrón correcto
late ScrollController _scrollController;

@override
void initState() {
  super.initState();
  _scrollController = ScrollController();
  _scrollController.addListener(_onScroll);
}

void _onScroll() {
  if (_scrollController.position.pixels ==
      _scrollController.position.maxScrollExtent) {
    _loadMore();
  }
}

@override
void dispose() {
  _scrollController.removeListener(_onScroll);  // ← Primero remover listener
  _scrollController.dispose();                   // ← Luego dispose
  super.dispose();
}
```

### 6.3 AnimationController

```dart
// ✅ Patrón correcto
late AnimationController _controller;

@override
void initState() {
  super.initState();
  _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 500),
  );
}

@override
void dispose() {
  _controller.dispose();  // ← Siempre dispose
  super.dispose();
}
```

### 6.4 Timer

```dart
// ❌ MAL: Timer.periodic sin cancelar
Timer.periodic(const Duration(seconds: 5), (timer) {
  _fetchData();
});

// ✅ BIEN: Guardar referencia y cancelar
late Timer _timer;

@override
void initState() {
  super.initState();
  _timer = Timer.periodic(const Duration(seconds: 5), (timer) {
    _fetchData();
  });
}

@override
void dispose() {
  _timer.cancel();  // ← Cancelar timer
  super.dispose();
}
```

---

## 7. Patrón de cancelación segura

```dart
// Patrón para streams con posibles errores
StreamSubscription? _subscription;
bool _isDisposed = false;

@override
void initState() {
  super.initState();
  _subscription = myStream.listen(
    (data) {
      if (!_isDisposed) {
        setState(() { _data = data; });
      }
    },
    onError: (error) {
      if (!_isDisposed) {
        handleError(error);
      }
    },
  );
}

@override
void dispose() {
  _isDisposed = true;
  _subscription?.cancel();
  super.dispose();
}
```

---

## 8. Patrones comunes de leak y sus soluciones

### 8.1 Patrón 1: stream en initState sin dispose

```dart
// ❌ LEAK: Stream nunca se cancela
@override
void initState() {
  super.initState();
  Supabase.instance.client
      .from('posts')
      .stream(primaryKey: ['id'])
      .listen((posts) {
        setState(() { _posts = posts; });
      });
  // ← No hay cancelación
}

// ✅ FIX: Guardar y cancelar
StreamSubscription? _postsSubscription;

@override
void initState() {
  super.initState();
  _postsSubscription = Supabase.instance.client
      .from('posts')
      .stream(primaryKey: ['id'])
      .listen((posts) {
        if (mounted) {
          setState(() { _posts = posts; });
        }
      });
}

@override
void dispose() {
  _postsSubscription?.cancel();
  super.dispose();
}
```

### 8.2 Patrón 2: closure con referencia al contexto

```dart
// ❌ LEAK: Closure mantiene referencia al widget
Timer.periodic(const Duration(seconds: 1), (timer) {
  Navigator.of(context).push(...);  // context capturado
});

// ✅ FIX: Verificar mounted antes de usar context
Timer.periodic(const Duration(seconds: 1), (timer) {
  if (mounted) {
    Navigator.of(context).push(...);
  }
});
```

### 8.3 Patrón 3: listener sin remover

```dart
// ❌ LEAK: Listener nunca se remueve
@override
void initState() {
  super.initState();
  WidgetsBinding.instance.addObserver(this);
  // ← No se remueve en dispose
}

// ✅ FIX: Agregar y remover simétricamente
@override
void initState() {
  super.initState();
  WidgetsBinding.instance.addObserver(this);
}

@override
void dispose() {
  WidgetsBinding.instance.removeObserver(this);  // ← Remover
  super.dispose();
}
```

---

## 9. Checklist de detección de memory leaks

```
Paso 1: Identificar la pantalla sospechosa
  └── ¿Qué pantalla muestra crecimiento de memoria?

Paso 2: Auditar initState()
  └── ¿Qué controllers/streams/timers se crean aquí?
  └── Por cada uno: ¿tiene su correspondiente dispose()?

Paso 3: Auditar dispose()
  └── ¿Todos los recursos tienen close/cancel/dispose?
  └── ¿Se llama super.dispose() al final?

Paso 4: Verificar patrones de suscripción
  └── StreamSubscription: ¿se cancela en dispose?
  └── Timer: ¿se cancela en dispose?
  └── WidgetsBindingObserver: ¿se remueve en dispose?

Paso 5: Probar con DevTools Memory
  └── Tomar snapshot base
  └── Navegar 5x a la pantalla
  └── Tomar diff snapshot
  └── Buscar clases con crecimiento de instancias

Paso 6: Verificar BLoC/Cubit
  └── ¿close() cancela todas las suscripciones?
  └── ¿BlocObserver reporta correctamente?
```

---

## 10. BLoC/Cubit: cuándo cerrar streams

### 10.1 En Cubit

```dart
class ChatCubit extends Cubit<ChatState> {
  final ChatRepository _repository;
  StreamSubscription? _messagesSub;

  ChatCubit(this._repository) : super(ChatInitial());

  void startListening() {
    _messagesSub = _repository.getMessages().listen(
      (messages) => emit(ChatLoaded(messages)),
    );
  }

  @override
  void close() {
    _messagesSub?.cancel();  // ← Cerrar suscripción
    return super.close();
  }
}
```

### 10.2 BlocObserver para tracking de memoria

```dart
class AppBlocObserver extends BlocObserver {
  @override
  void onCreate(BlocBase bloc) {
    super.onCreate(bloc);
    debugPrint('BLoC created: ${bloc.runtimeType}');
  }

  @override
  void onClose(BlocBase bloc) {
    debugPrint('BLoC closed: ${bloc.runtimeType}');
    super.onClose(bloc);
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    debugPrint('BLoC error: ${bloc.runtimeType} - $error');
    super.onError(bloc, error, stackTrace);
  }
}

// En main.dart
void main() {
  Bloc.observer = AppBlocObserver();
  runApp(MyApp());
}
```

---

## 11. Comandos para investigación de memoria

```bash
# Ejecutar en profile para mediciones reales
flutter run --profile

# Ver memoria en tiempo real con DevTools
# Abrir DevTools > Memory view

# Analizar el uso de memoria del build
flutter build apk --analyze-size
```

---

## Resumen

| Concepto | Acción |
|---|---|
| **Stream sin cancelar** | Guardar `StreamSubscription` y cancelar en `dispose()` |
| **Controller sin dispose** | Siempre llamar `.dispose()` en `dispose()` |
| **Timer sin cancel** | Guardar referencia y `.cancel()` en `dispose()` |
| **Listener sin remove** | `removeObserver` simétrico a `addObserver` |
| **Closure con context** | Verificar `mounted` antes de usar |
| **BLoC sin close** | Cancelar suscripciones en `close()` |
| **Detección** | DevTools Memory → heap snapshots → diff |

---

## 📚 Referencias

- [Flutter | Memory view](https://docs.flutter.dev/tools/devtools/memory) — Documentación oficial de la Memory view
- [Flutter | Memory](https://docs.flutter.dev/perf/memory) — Conceptos de memoria en Flutter
- [Dart | Streams](https://dart.dev/tutorials/language/streams) — Manejo de streams en Dart

---

> 📖 **Siguiente:** [22-rendering-complejo.md](./22-rendering-complejo.md) — Rendering complejo: shaders y rasterización
