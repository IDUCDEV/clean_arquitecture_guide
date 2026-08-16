# 3. Layout y Navegación

## Row y Column

Los dos layouts fundamentales.

```dart
Row(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly, // eje horizontal
  crossAxisAlignment: CrossAxisAlignment.center,     // eje vertical
  children: const [
    Icon(Icons.star, color: Colors.amber),
    Text('4.5'),
    Text('(120 reseñas)'),
  ],
);

Column(
  mainAxisAlignment: MainAxisAlignment.start,
  crossAxisAlignment: CrossAxisAlignment.stretch,
  children: [
    const Text('Título'),
    const SizedBox(height: 8),
    const Text('Contenido'),
  ],
);
```

| Propiedad | Row | Column |
|---|---|---|
| `mainAxisAlignment` | horizontal | vertical |
| `crossAxisAlignment` | vertical | horizontal |
| `mainAxisSize` | ancho | alto |

## Flex y Expanded

Distribución proporcional del espacio.

```dart
Row(
  children: [
    Expanded(flex: 2, child: Container(color: Colors.red)),
    Expanded(flex: 1, child: Container(color: Colors.blue)),
    // La primera ocupa 2/3, la segunda 1/3
  ],
);
```

Usa `Flexible` cuando quieras que un hijo pueda ser más pequeño que su flex:

```dart
Row(
  children: [
    Flexible(child: Text(largoTexto, overflow: TextOverflow.ellipsis)),
    const Icon(Icons.arrow_forward),
  ],
);
```

## Stack

Superposición de widgets. Ideal para badges, capas, overlays.

```dart
Stack(
  children: [
    Image.network('https://ejemplo.com/fondo.jpg'),
    const Positioned(
      bottom: 16,
      left: 16,
      child: Text('Texto sobre imagen',
        style: TextStyle(color: Colors.white, fontSize: 24)),
    ),
    const Positioned(
      top: 8,
      right: 8,
      child: CircleAvatar(child: Text('A')),
    ),
  ],
);
```

## Scaffold

Estructura base de una pantalla. Con Material 3, la barra inferior recomendada es `NavigationBar`.

```dart
Scaffold(
  appBar: AppBar(
    title: const Text('Mi App'),
    actions: [
      IconButton(icon: const Icon(Icons.search), onPressed: () {}),
    ],
  ),
  body: const Center(child: Text('Contenido')),
  floatingActionButton: FloatingActionButton(
    onPressed: () {},
    child: const Icon(Icons.add),
  ),
  bottomNavigationBar: NavigationBar(
    selectedIndex: _tabIndex,
    onDestinationSelected: (index) => setState(() => _tabIndex = index),
    destinations: const [
      NavigationDestination(icon: Icon(Icons.home), label: 'Inicio'),
      NavigationDestination(icon: Icon(Icons.search), label: 'Buscar'),
      NavigationDestination(icon: Icon(Icons.person), label: 'Perfil'),
    ],
  ),
  drawer: NavigationDrawer(
    children: const [
      DrawerHeader(child: Text('Menú')),
      ListTile(leading: Icon(Icons.settings), title: Text('Ajustes')),
    ],
  ),
);
```

> `BottomNavigationBar` y `Drawer` siguen funcionando pero son estilos de Material 2. En Material 3 usa `NavigationBar` y `NavigationDrawer`.

## Navigator 1.0 (push/pop)

Navegación imperativa clásica.

```dart
// Ir a otra pantalla
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => const DetallePage(id: 42),
  ),
);

// Regresar
Navigator.pop(context);

// Recibir resultado
final resultado = await Navigator.push<String>(
  context,
  MaterialPageRoute(builder: (_) => const SeleccionPage()),
);
```

## Navegación con GoRouter (recomendada)

Navegación declarativa basada en rutas. Es el estándar actual para apps reales y lo usaremos a lo largo de la guía.

```dart
// pubspec.yaml: go_router: ^17.5.0

final router = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (_, __) => const HomePage(),
    ),
    GoRoute(
      path: '/productos',
      builder: (_, __) => const ProductosPage(),
      routes: [
        GoRoute(
          path: ':id',
          builder: (_, state) => DetalleProductoPage(
            id: state.pathParameters['id']!,
          ),
        ),
      ],
    ),
  ],
);
```

Uso en `MaterialApp.router`:

```dart
MaterialApp.router(
  routerConfig: router,
  // ...
);
```

Navegación con GoRouter:

```dart
// context.go reemplaza la ruta actual
context.go('/productos');

// context.push agrega al historial
context.push('/productos/42');

// context.pop regresa
context.pop();

// Parámetros extra (query)
context.push('/productos/42?source=home');
```

Con `go_router` también puedes proteger rutas con `redirect` (por ejemplo, redirigir a login si no hay sesión). Veremos esto en profundidad en los módulos de arquitectura.

## SafeArea

Asegura que el contenido no se superponga con áreas del sistema (notch, barra de estado, etc.).

```dart
SafeArea(
  child: Column(
    children: [
      // Este contenido respeta las áreas seguras
    ],
  ),
);
```

## MediaQuery

Información del tamaño y orientación de la pantalla. Usa los accesores `xOf` para reconstruir solo cuando cambie lo que te interesa.

```dart
@override
Widget build(BuildContext context) {
  final ancho = MediaQuery.sizeOf(context).width;   // solo cambia con el tamaño
  final alto = MediaQuery.heightOf(context);         // solo cambia con el alto
  final isMobile = ancho < 600;

  return isMobile ? const _MobileLayout() : const _TabletLayout();
}
```

> `MediaQuery.of(context).size` (forma anterior) reconstruía el widget ante *cualquier* cambio de MediaQuery (tema, padding, etc.). Desde Flutter 3.35 prefiere `MediaQuery.sizeOf` / `widthOf` / `heightOf`.

## LayoutBuilder

Adaptación al espacio disponible del padre (no de la pantalla).

```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth < 400) {
      return const _VerticalLayout();
    }
    return const _HorizontalLayout();
  },
);
```

## PopScope (reemplaza WillPopScope)

Para interceptar el botón de retroceso del sistema. `WillPopScope` está deprecado desde Flutter 3.24.

```dart
PopScope(
  canPop: false, // bloquea el pop
  onPopInvokedWithResult: (didPop, result) {
    if (!didPop) {
      // Confirmar salida antes de permitir el pop
      _mostrarConfirmacion();
    }
  },
  child: const Scaffold(body: Text('Edición pendiente')),
);
```

En versiones futuras, `onPopInvokedWithResult` reemplaza por completo a `onPopInvoked` (deprecado en 3.29).


---

## 📚 Referencias

- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter
- [Flutter | Understanding constraints](https://docs.flutter.dev/ui/layout/constraints) — Cómo funcionan las restricciones
- [Flutter | Navigation and routing](https://docs.flutter.dev/ui/navigation) — Navegación declarativa e imperativa
- [go_router | pub.dev](https://pub.dev/packages/go_router) — Documentación de go_router
- [Flutter | PopScope](https://api.flutter.dev/flutter/widgets/PopScope-class.html) — Interceptar el retroceso del sistema

---

## Lo que sigue

Pasamos a interacción del usuario: gestos, formularios y manejo de entrada.
