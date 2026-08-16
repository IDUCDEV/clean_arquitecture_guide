# 1. Fundamentos de Widgets

> Versión objetivo: **Flutter 3.44+ / 3.47 (estable)** — Material 3 por defecto. La documentación oficial de referencia está en [docs.flutter.dev](https://docs.flutter.dev/).

## Qué es un widget

En Flutter, **todo es un widget**. No hay separación entre "vistas", "layout" y "controles" como en otros frameworks. Un widget es una **descripción inmutable de una parte de la UI**.

```dart
// Esto ES la UI. No hay XML, no hay templates separados.
const Text('Hola mundo');
const Icon(Icons.star);
```

Como los widgets son inmutables, Flutter no los modifica: los **reemplaza** por otros. Es un modelo **declarativo**: describes *cómo debería verse* la UI para un estado dado, y Flutter se encarga de llevarla a ese estado.

## Los tres árboles (widget / element / render)

Cada widget que escribes participa en tres árboles paralelos:

1. **Widget tree** — la configuración que escribes (barato de crear y descartar).
2. **Element tree** — las instancias mutables que gestionan el ciclo de vida y que Flutter *reutiliza* al reconstruir (la clave del rendimiento).
3. **Render tree** — los `RenderObject` que calculan layout y pintan en pantalla (`RenderBox`, `RenderParagraph`, etc.).

```
MaterialApp ── Widget ──▶ Element ──▶ RenderView
   └─ Scaffold  ─────────▶ Element ──▶ RenderBox (layout + paint)
```

No necesitas manipular `Element` ni `RenderObject` directamente, pero entender que existen te ayuda a comprender por qué ciertos patrones (como las `key`) funcionan y por qué reconstruir un widget es barato mientras el `Element` se conserve.

## StatelessWidget vs StatefulWidget

### StatelessWidget

No tiene estado mutable. Se construye y solo se reconstruye si su configuración (propiedades) cambia.

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

Tiene estado mutable que puede cambiar durante la vida del widget. El estado vive en la clase `State`, **no** en el widget (el widget sigue siendo inmutable).

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

Cada vez que llamas `setState()`, Flutter programa una **reconstrucción** del subárbol de este widget. El patrón es siempre: cambia el dato → `setState` → `build` se llama de nuevo.

## El árbol de widgets

Los widgets se anidan formando un árbol:

```
MaterialApp
└── Scaffold
    ├── AppBar
    └── body: Column
        ├── Text
        ├── SizedBox
        └── FilledButton
```

Cada `child` o `children` crea un nivel en el árbol. Este anidamiento es normal y esperado — Flutter lo maneja de forma eficiente.

## BuildContext

`BuildContext` es el "lugar" de un widget en el árbol: un **handle** al `Element`. Se usa para:

- Acceder al tema: `Theme.of(context)`
- Navegar: `Navigator.of(context)`
- Leer dependencias del árbol: `MediaQuery.sizeOf(context)`, `context.read<T>()`, `context.watch<T>()` (estos dos últimos vienen de los paquetes `provider` / `flutter_bloc`, no del núcleo)

```dart
@override
Widget build(BuildContext context) {
  // context te da acceso a todo el árbol hacia arriba
  final theme = Theme.of(context);
  final screenWidth = MediaQuery.sizeOf(context).width;

  return Container(
    color: theme.colorScheme.primary,
    width: screenWidth * 0.9,
    child: const Text('Responsive'),
  );
}
```

> `MediaQuery.sizeOf(context)` solo reconstruye el widget cuando cambia el **tamaño** de la pantalla. `MediaQuery.of(context).size` (vieja forma) reconstruía ante *cualquier* cambio de MediaQuery (tema, padding, etc.). Desde Flutter 3.35 también existen `MediaQuery.widthOf` y `MediaQuery.heightOf`. **Prefiere los accesores `xOf`.**
>
> `context.read<T>()` y `context.watch<T>()` pertenecen al módulo [16-BLOC-CUBIT](../16-BLOC-CUBIT/). Aquí los mencionamos porque aparecerán en ejemplos de la guía como adelanto.

## const y las reconstrucciones

Siempre que puedas, declara widgets como `const`:

```dart
// MAL: se crea un nuevo widget en cada build
child: Text('Hola');

// BIEN: se reusa la misma instancia constante
child: const Text('Hola');

// MEJOR: constructores const en tus propios widgets
class MiWidget extends StatelessWidget {
  const MiWidget({super.key});
  // ...
}
```

Los widgets `const` permiten a Flutter **saltarse por completo** la reconstrucción de ese subárbol: como la instancia nunca cambia, el `Element` se conserva sin necesidad de reconciliar.

## Keys

Las keys ayudan a Flutter a identificar widgets cuando el árbol cambia de posición o de tipo. Sin una key, Flutter compara por *posición* y tipo; con key, por *identidad*.

```dart
ListView(children: [
  // Sin key, al reordenar Flutter no sabe qué elemento es cuál
  // y puede conservar el estado equivocado (ej. texto escrito)
  TodoItem(tarea: tareas[0]),
  TodoItem(tarea: tareas[1]),
])

// Con ValueKey, Flutter preserva el estado correcto al reordenar
ListView(children: [
  TodoItem(key: ValueKey(tareas[0].id), tarea: tareas[0]),
  TodoItem(key: ValueKey(tareas[1].id), tarea: tareas[1]),
])
```

| Key | Cuándo usarla |
|---|---|
| `ValueKey<T>(valor)` | El identificador es un valor (`id`, `String`, `int`) — la más común |
| `ObjectKey(objeto)` | El identificador es un objeto completo sin `==` propio |
| `UniqueKey()` | Solo cuando quieras *forzar* que el widget se re-cree siempre |
| `GlobalKey<...>()` | Para acceder al `State` o `RenderObject` desde fuera (ej. `Form`, `AnimatedList`) — úsala con moderación |

## Regla de oro

> Pregúntate siempre: ¿este widget necesita cambiar con el tiempo?
>
> - No → `StatelessWidget`
> - Sí, pero solo por datos externos → `StatelessWidget` + `Stream` / `Future` / `InheritedWidget`
> - Sí, y necesita estado interno efímero → `StatefulWidget`

---

## 📚 Referencias

- [Flutter | Introduction to widgets](https://docs.flutter.dev/ui/widgets-intro) — Arquitectura de los 3 árboles y el modelo declarativo
- [Flutter | Understanding constraints](https://docs.flutter.dev/ui/layout/constraints) — Cómo el layout fluye por el árbol (widget/element/render)
- [Flutter | API reference — Widget](https://api.flutter.dev/flutter/widgets/Widget-class.html) — Clase base de todos los widgets
- [Flutter | API reference — BuildContext](https://api.flutter.dev/flutter/widgets/BuildContext-class.html) — API del contexto (dependOn/read/watch, maybeOf)
- [Flutter | Keys](https://docs.flutter.dev/ui/widgets-intro#keys) — Cuándo y por qué usar keys

---

## Lo que sigue

En el próximo capítulo veremos los widgets básicos de UI, cómo se agrupan en componentes reutilizables y el patrón de atomización.
