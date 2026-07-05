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

Estructura base de una pantalla.

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
  bottomNavigationBar: BottomNavigationBar(
    items: const [
      BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Inicio'),
      BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Buscar'),
      BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Perfil'),
    ],
  ),
  drawer: Drawer(
    child: ListView(
      children: const [
        DrawerHeader(child: Text('Menú')),
        ListTile(leading: Icon(Icons.settings), title: Text('Ajustes')),
      ],
    ),
  ),
);
```

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

## Navigator 2.0 con GoRouter

Navegación declarativa basada en rutas (recomendada para apps reales).

```dart
// pubspec.yaml: go_router: ^14.0.0

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

// Parámetros extra
context.push('/productos/42?source=home');
```

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

Información del tamaño y orientación de la pantalla.

```dart
@override
Widget build(BuildContext context) {
  final size = MediaQuery.of(context).size;
  final isMobile = size.width < 600;

  return isMobile ? const _MobileLayout() : const _TabletLayout();
}
```

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


---

## 📚 Referencias

- [Flutter | Widget catalog](https://docs.flutter.dev/ui/widgets) — Catálogo completo de widgets por categoría
- [Flutter | API reference](https://api.flutter.dev/) — Documentación de la API de Flutter
- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter

---

## Lo que sigue

Pasamos a interacción del usuario: gestos, formularios y manejo de entrada.
