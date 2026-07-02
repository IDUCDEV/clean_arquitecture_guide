# 1. Fundamentos de Widgets

## Qué es un widget

En Flutter, **todo es un widget**. No hay separación entre "vistas", "layout" y "controles" como en otros frameworks. Un widget es una descripción inmutable de una parte de la UI.

```dart
// Esto ES la UI. No hay XML, no hay templates separados.
const Text('Hola mundo');
const Icon(Icons.star);
```

## Widget = configuración + elemento + objeto render

Cada widget pasa por tres fases:

1. **Widget** — la configuración (lo que escribes en el árbol)
2. **Element** — la instancia mutable que gestiona el ciclo de vida
3. **RenderObject** — el objeto que pinta en la pantalla

No necesitas manipular `Element` ni `RenderObject` directamente, pero entender que existen te ayuda a comprender por qué ciertos patrones funcionan.

## StatelessWidget vs StatefulWidget

### StatelessWidget

No tiene estado mutable. Se construye una vez y solo se reconstruye si sus configuraciones externas cambian.

```dart
class MiAvatar extends StatelessWidget {
  final String nombre;
  final double tamaño;

  const MiAvatar({super.key, required this.nombre, this.tamaño = 48});

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      radius: tamaño / 2,
      child: Text(nombre[0].toUpperCase()),
    );
  }
}
```

Usa `StatelessWidget` cuando: el widget depende solo de sus propiedades y del contexto (`Theme`, `MediaQuery`, etc.).

### StatefulWidget

Tiene estado mutable que puede cambiar durante la vida del widget.

```dart
class ContadorWidget extends StatefulWidget {
  const ContadorWidget({super.key});

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
          child: const Text('Incrementar'),
        ),
      ],
    );
  }
}
```

Cada vez que llamas `setState()`, Flutter programa una reconstrucción del subárbol de este widget.

## El árbol de widgets

Los widgets se anidan formando un árbol:

```
MaterialApp
└── Scaffold
    ├── AppBar
    └── body: Column
        ├── Text
        ├── SizedBox
        └── ElevatedButton
```

Cada `child` o `children` crea un nivel en el árbol. Este anidamiento es normal y esperado.

## BuildContext

`BuildContext` es el "lugar" de un widget en el árbol. Se usa para:

- Acceder al tema: `Theme.of(context)`
- Navegar: `Navigator.of(context)`
- Obtener herencia: `context.read<T>()`, `context.watch<T>()`

```dart
@override
Widget build(BuildContext context) {
  // context te da acceso a todo el árbol hacia arriba
  final theme = Theme.of(context);
  final screenWidth = MediaQuery.of(context).size.width;

  return Container(
    color: theme.colorScheme.primary,
    width: screenWidth * 0.9,
    child: const Text('Responsive'),
  );
}
```

## const y las reconstrucciones

Siempre que puedas, declara widgets como `const`:

```dart
// MAL: se crea un nuevo widget en cada build
child: Text('Hola');

// BIEN: se reusa la misma instancia constant
child: const Text('Hola');

// MEJOR: constructores const
class MiWidget extends StatelessWidget {
  const MiWidget({super.key});
  // ...
}
```

Los widgets `const` permiten a Flutter saltarse la reconstrucción de ese subárbol porque sabe que nunca cambia.

## Keys

Las keys ayudan a Flutter a identificar widgets cuando el árbol se reordena.

```dart
ListView(children: [
  // Sin key, Flutter no sabe qué elemento es cuál al reordenar
  TodoItem(tarea: tareas[0]),
  TodoItem(tarea: tareas[1]),
])

// Con ValueKey, Flutter preserva el estado correcto
ListView(children: [
  TodoItem(key: ValueKey(tareas[0].id), tarea: tareas[0]),
  TodoItem(key: ValueKey(tareas[1].id), tarea: tareas[1]),
])
```

Usa `ValueKey` para identificar elementos únicos. Usa `ObjectKey` cuando el identificador es un objeto completo. Usa `UniqueKey` solo cuando necesites garantizar que el widget se re-cree siempre.

## Regla de oro

> Pregúntate siempre: ¿este widget necesita cambiar con el tiempo?
>
> - No → `StatelessWidget`
> - Sí, pero solo por datos externos → `StatelessWidget` + BLoC / Stream
> - Sí, y necesita estado interno efímero → `StatefulWidget`

## Lo que sigue

En el próximo capítulo veremos los widgets básicos de UI, cómo se agrupan en componentes reutilizables y el patrón de atomización.
