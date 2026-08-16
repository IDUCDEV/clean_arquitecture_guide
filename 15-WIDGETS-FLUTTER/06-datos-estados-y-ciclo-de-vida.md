# 6. Datos, Estados y Ciclo de Vida

## Flujo de datos en Flutter

Los datos viajan **hacia abajo** por el árbol de widgets (vía constructores o `InheritedWidget`). Las notificaciones (callbacks) viajan **hacia arriba**.

```
Datos    → Widget Padre → Widget Hijo
Callback → Hijo → Padre
```

Este flujo unidireccional se conoce como *lifting state up*: el estado se eleva al ancestro común que lo necesita, y baja a los hijos que solo lo muestran.

## StatefulWidget ciclo de vida

```dart
class MiWidget extends StatefulWidget {
  const MiWidget({super.key});

  @override
  State<MiWidget> createState() => _MiWidgetState();
}

class _MiWidgetState extends State<MiWidget> {
  @override
  void initState() {
    super.initState();
    // 1. Inicializar controladores, suscribirse a streams, cargar datos
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // 2. Se llama después de initState.
    // También se llama cuando cambia un InheritedWidget usado en build.
  }

  @override
  void didUpdateWidget(covariant MiWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    // 3. Se llama cuando el padre reconstruye con nuevas configuraciones.
  }

  @override
  void dispose() {
    // 4. Liberar controladores, cancelar suscripciones.
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Se llama después de cada setState, didChangeDependencies,
    // didUpdateWidget.
    return const Text('Ciclo de vida');
  }
}
```

Orden en montaje: `constructor` → `initState` → `didChangeDependencies` → `build`

Orden en cambio de padre: `didUpdateWidget` → `build`

Orden en desmontaje: `dispose`

## FutureBuilder

Widget reactivo que construye UI basada en el estado de un `Future`.

```dart
FutureBuilder<List<Producto>>(
  future: _cargarProductos(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const Center(child: CircularProgressIndicator());
    }

    if (snapshot.hasError) {
      return Center(
        child: Column(
          children: [
            Text('Error: ${snapshot.error}'),
            FilledButton(
              onPressed: () => setState(() {}), // reintentar
              child: const Text('Reintentar'),
            ),
          ],
        ),
      );
    }

    if (!snapshot.hasData || snapshot.data!.isEmpty) {
      return const Center(child: Text('Sin datos'));
    }

    return ListView.builder(
      itemCount: snapshot.data!.length,
      itemBuilder: (context, index) {
        return ListTile(title: Text(snapshot.data![index].nombre));
      },
    );
  },
);
```

> Almacena el `Future` en una variable/estado si quieres que el reintento cree uno nuevo. Si lo creas directamente en `future:`, cada rebuild lanza una nueva petición.

## StreamBuilder

Widget reactivo que se actualiza con cada emisión de un `Stream`.

```dart
StreamBuilder<int>(
  stream: contadorStream,
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const Text('Esperando...');
    }

    if (snapshot.hasError) {
      return Text('Error: ${snapshot.error}');
    }

    return Text(
      'Valor: ${snapshot.data}',
      style: const TextStyle(fontSize: 32),
    );
  },
);
```

Puedes pasar `initialData` para pintar algo antes de la primera emisión.

## ValueListenableBuilder y ListenableBuilder

Widgets reactivos para `ValueNotifier` y cualquier `Listenable` — estado local simple sin streams.

```dart
final _contador = ValueNotifier<int>(0);

ValueListenableBuilder<int>(
  valueListenable: _contador,
  builder: (context, value, child) {
    return Column(
      children: [
        Text('$value', style: const TextStyle(fontSize: 32)),
        FilledButton(
          onPressed: () => _contador.value++,
          child: const Text('+'),
        ),
      ],
    );
  },
);
```

`ListenableBuilder` es la versión genérica (acepta `ChangeNotifier`, `Animation`, etc. sin desempacar valores):

```dart
ListenableBuilder(
  listenable: _modelo, // un ChangeNotifier
  builder: (context, child) => Text(_modelo.titulo),
);
```

`ValueNotifier` + `ValueListenableBuilder` es ideal para estado local que no requiere BLoC. `ChangeNotifier` + `ListenableBuilder` sirve cuando el estado es un objeto completo.

## TickerProvider

Necesario para animaciones. Provee el `Ticker` que sincroniza con el refresh rate.

```dart
class _AnimacionState extends State<AnimacionWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this, // TickerProvider
      duration: const Duration(seconds: 1),
    );
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }
}
```

Usa `TickerProviderStateMixin` (en vez de `SingleTickerProviderStateMixin`) si necesitas más de un controller.

## Patrones de carga de datos en initState

```dart
class _PaginaState extends State<PaginaWidget> {
  @override
  void initState() {
    super.initState();
    _cargar();
  }

  Future<void> _cargar() async {
    // Con Future: iniciar carga
    final data = await servicio.fetch();
    // setState seguro porque el widget está montado
    if (!mounted) return;
    setState(() => _data = data);
  }
}
```

Cuando tu capa de estado viva en otra parte (Cubit/BLoC, módulo 16), `initState` solo dispara la intención:

```dart
@override
void initState() {
  super.initState();
  // Adelanto del módulo 16: con BLoC se dispara un evento,
  // el cubit emite el estado y la UI reacciona.
  context.read<MiCubit>().cargarDatos();
}
```

## mounted y context.mounted

`mounted` indica si el `State` sigue en el árbol. Úsalo antes de tocar el estado después de un `await`.

```dart
@override
Widget build(BuildContext context) {
  return FilledButton(
    onPressed: () async {
      await Future.delayed(const Duration(seconds: 3));
      // Si el widget ya no está montado, no tocar el estado
      if (!mounted) return;
      setState(() { /* ... */ });
    },
    child: const Text('Click'),
  );
}
```

Desde Flutter 3.7 también existe `context.mounted`, útil en funciones que reciben un `BuildContext` sin `State` (por ejemplo, un método de una clase helper):

```dart
Future<void> irADetalle(BuildContext context) async {
  await obtenerAlgo();
  if (!context.mounted) return; // evita usar un context desmontado
  Navigator.of(context).push(...);
}
```

> Diferencia: `mounted` (en el `State`) protege `setState`; `context.mounted` (en el `BuildContext`) protege operaciones que usan el context (navegación, SnackBars, `context.read`).


---

## 📚 Referencias

- [Flutter | StatefulWidget lifecycle](https://docs.flutter.dev/ui/interactivity) — Ciclo de vida y manejo de estado
- [Flutter | FutureBuilder](https://api.flutter.dev/flutter/widgets/FutureBuilder-class.html) — API de FutureBuilder
- [Flutter | StreamBuilder](https://api.flutter.dev/flutter/widgets/StreamBuilder-class.html) — API de StreamBuilder
- [Flutter | ListenableBuilder](https://api.flutter.dev/flutter/widgets/ListenableBuilder-class.html) — Builder reactivo genérico
- [Flutter | BuildContext.mounted](https://api.flutter.dev/flutter/widgets/BuildContext/mounted.html) — Proteger usos asíncronos de context

---

## Lo que sigue

El siguiente capítulo cubre animaciones y cómo agregar movimiento a las interfaces.
