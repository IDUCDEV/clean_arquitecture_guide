# 6. Datos, Estados y Ciclo de Vida

## Flujo de datos en Flutter

Los datos viajan **hacia abajo** por el árbol de widgets. Las notificaciones (callbacks) viajan **hacia arriba**.

```
Datos → Provider/Cubit → Widget Padre → Widget Hijo
Callback: Hijo → Padre → Provider/Cubit
```

Este flujo unidireccional se conoce como *lifting state up*.

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

## ValueListenableBuilder

Widget reactivo para `ValueNotifier` — estado local simple sin streams.

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

`ValueNotifier` + `ValueListenableBuilder` es ideal para estado local que no requiere BLoC.

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

## Patrones de carga de datos en initState

```dart
class _PaginaState extends State<PaginaWidget> {
  @override
  void initState() {
    super.initState();
    // Con BLoC: disparar evento
    context.read<MiCubit>().cargarDatos();

    // Con Future: iniciar carga
    _initAsync();
  }

  Future<void> _initAsync() async {
    // setState seguro porque el widget está montado
    if (!mounted) return;
    // ...
  }
}
```

## mounted

La propiedad `mounted` indica si el `State` sigue en el árbol.

```dart
@override
Widget build(BuildContext context) {
  return ElevatedButton(
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


---

## 📚 Referencias

- [Flutter | Widget catalog](https://docs.flutter.dev/ui/widgets) — Catálogo completo de widgets por categoría
- [Flutter | API reference](https://api.flutter.dev/) — Documentación de la API de Flutter
- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter

---

## Lo que sigue

El siguiente capítulo cubre animaciones y cómo agregar movimiento a las interfaces.
