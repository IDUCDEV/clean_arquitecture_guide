# 15. HydratedBloc — Persistencia Automática

> Referencia: [pub.dev/packages/hydrated_bloc](https://pub.dev/packages/hydrated_bloc)

## ¿Qué resuelve?

Sin persistencia: al reiniciar la app, el estado se pierde.

Con `HydratedBloc`: el estado se guarda automáticamente en el disco y se restaura al iniciar.

## Configuración

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

## HydratedCubit

```dart
class TemaCubit extends HydratedCubit<TemaState> {
  TemaCubit() : super(TemaClaro());

  void toggle() {
    emit(state is TemaClaro ? TemaOscuro() : TemaClaro());
  }

  @override
  TemaState? fromJson(Map<String, dynamic> json) {
    return json['modo'] == 'oscuro' ? TemaOscuro() : TemaClaro();
  }

  @override
  Map<String, dynamic>? toJson(TemaState state) {
    return {'modo': state is TemaOscuro ? 'oscuro' : 'claro'};
  }
}
```

## HydratedBloc

```dart
class CarritoBloc extends HydratedBloc<CarritoEvent, CarritoState> {
  CarritoBloc() : super(const CarritoState([])) {
    on<AgregarAlCarrito>(_onAgregar);
    on<QuitarDelCarrito>(_onQuitar);
    on<VaciarCarrito>(_onVaciar);
  }

  Future<void> _onAgregar(
      AgregarAlCarrito event, Emitter<CarritoState> emit) async {
    emit(CarritoState([...state.items, event.producto]));
  }

  Future<void> _onQuitar(
      QuitarDelCarrito event, Emitter<CarritoState> emit) async {
    emit(CarritoState(
      state.items.where((p) => p.id != event.productoId).toList(),
    ));
  }

  void _onVaciar(VaciarCarrito event, Emitter<CarritoState> emit) {
    emit(const CarritoState([]));
  }

  @override
  CarritoState? fromJson(Map<String, dynamic> json) {
    final items = (json['items'] as List)
        .map((e) => Producto.fromJson(e as Map<String, dynamic>))
        .toList();
    return CarritoState(items);
  }

  @override
  Map<String, dynamic>? toJson(CarritoState state) {
    return {'items': state.items.map((p) => p.toJson()).toList()};
  }
}
```

## ¿Qué se debe persistir?

- **Sí**: tema oscuro/claro, carrito de compras, favoritos, onboarding completado, preferencias
- **No**: datos de sesión (usa SecureStorage), datos de API (usa caché local), contraseñas

## Custom Storage

Por defecto usa `HydratedStorage.build` con el sistema de archivos. Puedes usar alternativas:

```dart
// Para web
final storage = await HydratedStorage.build(
  storageDirectory: HydratedStorage.webStorageDirectory,
);

// Para testing (no escribe en disco)
final storage = await HydratedStorage.build(
  storageDirectory: MemoryStorage().storageDirectory,
);
```

## Testing con HydratedStorage mock

```dart
void main() {
  late FavoritoCubit cubit;

  setUp(() {
    HydratedBloc.storage = MockHydratedStorage();
    cubit = FavoritoCubit();
  });

  test('inicia con estado vacío', () {
    expect(cubit.state.items, []);
  });

  blocTest<FavoritoCubit, FavoritoState>(
    'persiste en disco al hacer toggle',
    build: () => cubit,
    act: (cubit) => cubit.toggle(producto),
    verify: (_) {
      verify(() => HydratedBloc.storage.write(
            'FavoritoCubit',
            any(),
          )).called(1);
    },
  );
}
```

## Reglas

- El ID de almacenamiento es el nombre del Cubit/Bloc (ej: `FavoritoCubit`)
- Si cambias el nombre de la clase, se pierde la persistencia previa
- `fromJson` debe manejar `null` (primera ejecución)
- No persistas objetos con referencias circulares
- El tamaño máximo recomendado por Cubit es ~100KB
