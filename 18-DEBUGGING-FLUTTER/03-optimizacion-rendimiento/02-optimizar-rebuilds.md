# 02 - Optimizar Rebuilds

## Por que los rebuilds innecesarios son el problema #1

En Flutter, **cada vez que un widget se reconstruye, todos sus hijos tambien se reconstruyen**. Si tu widget tree es profundo y un widget padre llama a `setState()` frecuentemente, puedes estar reconstruyendo cientos de widgets sin necesidad.

```
Widget Tree con rebuild innecesario:

  HomePage (setState)
  ├── Header ──────────── Reconstruido (innecesario)
  ├── Sidebar ─────────── Reconstruido (innecesario)
  ├── Content
  │   ├── ListWidget ──── Reconstruido (innecesario)
  │   │   ├── Item 1
  │   │   ├── Item 2
  │   │   └── Item 3
  │   └── Footer ──────── Reconstruido (innecesario)
  └── BottomBar ───────── Reconstruido (innecesario)

Solo ListWidget cambio, pero TODO se reconstruyo.
```

---

## El keyword `const`: la optimizacion mas simple

### Que hace `const`

Cuando marcas un widget como `const`, Flutter **reutiliza la misma instancia** en su lugar de crear una nueva. No se ejecuta `build()` para ese widget ni sus hijos.

### Sin const

```dart
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      Text('Hola'),           // ← Nuevo widget cada rebuild
      Icon(Icons.star),       // ← Nuevo widget cada rebuild
      Text('Mundo'),          // ← Nuevo widget cada rebuild
      ElevatedButton(         // ← Nuevo widget cada rebuild
        onPressed: () {},
        child: Text('Click'),
      ),
    ],
  );
}
```

### Con const

```dart
@override
Widget build(BuildContext context) {
  return Column(
    children: const [
      Text('Hola'),           // ← Reutilizado, sin rebuild
      Icon(Icons.star),       // ← Reutilizado, sin rebuild
      Text('Mundo'),          // ← Reutilizado, sin rebuild
      ElevatedButton(         // ← Reutilizado, sin rebuild
        onPressed: null,
        child: Text('Click'),
      ),
    ],
  );
}
```

### Reglas de const

| Regla | Ejemplo | Resultado |
|---|---|---|
| Todos los parametros deben ser compile-time | `Text('literal')` | OK |
| Parametros dinamicos | `Text(variable)` | NO puedes usar const |
| Sub-widgets const | `const [Text('a'), Text('b')]` | OK |
| Solo algunos hijos son const | Individuales: `const Text('a')` | OK |
| Widget con `key` | `const Text('a', key: ValueKey(1))` | OK |

### Cuando NO usar const

```dart
// ❌ NO puedes usar const aqui
Text(someVariable)
Image.network('$imageUrl')
Text('${user.name}')

// ✅ Usa const cuando todos los valores son literales
const Text('static text')
const Icon(Icons.home)
const SizedBox(height: 16)
const Padding(
  padding: EdgeInsets.all(8.0),
  child: Text('static'),
)
```

---

## Keys: controlar el matching de widgets

Las **Keys** le dicen a Flutter como emparejar widgets entre rebuilds. Sin la key correcta, Flutter puede reutilizar el widget equivocado.

### Tipos de Keys

| Key | Que hace | Cuando usar |
|---|---|---|
| **ValueKey** | Identifica por un valor (String, int, etc.) | Items de lista con ID unico |
| **ObjectKey** | Identifica por referencia a objeto | Objetos que pueden no ser == |
| **UniqueKey** | Identifica por identidad unica | Forzar recreacion completa |
| **GlobalKey** | Acceso al estado del widget desde cualquier lugar | Formularios, navegacion |

### Ejemplo: ValueKey en listas

```dart
// ❌ Sin key: Flutter puede mezclar items al reordenar
ListView(
  children: items.map((item) => ItemWidget(item)).toList(),
)

// ✅ Con ValueKey: Flutter sabe que item es cada widget
ListView(
  children: items.map((item) => ItemWidget(
    key: ValueKey(item.id),
    item: item,
  )).toList(),
)
```

### Cuando usar cada Key

```
Necesitas Key?
├── Lista de items con ID unico → ValueKey(item.id)
├── Lista de objetos sin ID estable → UniqueKey()
├── Necesitas acceder al estado de un widget → GlobalKey()
├── Widget se mueve entre padres → GlobalKey()
└── No hay problemas de matching → Sin key (default)
```

---

## BlocSelector vs BlocBuilder: reconstruccion selectiva

### El problema con BlocBuilder

```dart
// ❌ BlocBuilder reconstruye TODO cuando el estado cambia
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) {
    return Column(
      children: [
        Text('User: ${state.user.name}'),  // ← Solo esto cambia
        Text('Email: ${state.user.email}'), // ← Pero todo se reconstruye
        // ... 50 widgets mas ...
        BigExpensiveWidget(),               // ← Incluido este
      ],
    );
  },
)
```

### La solucion: BlocSelector

```dart
// ✅ BlocSelector solo reconstruye cuando el valor seleccionado cambia
BlocSelector<AuthBloc, AuthState, String>(
  selector: (state) => state.user.name,  // ← Solo monitorea esto
  builder: (context, name) {
    return Text('User: $name');           // ← Solo este widget se rebuild
  },
)
```

### Comparacion BlocBuilder vs BlocSelector

| Caracteristica | BlocBuilder | BlocSelector |
|---|---|---|
| Reconstruye cuando... | Cualquier cambio de estado | Solo cuando el selector cambia |
| Granularidad | Todo el subtree | Widget especifico |
| Uso de memoria | Mas alto | Mas bajo |
| Complejidad | Simple | Requiere definir selector |
| Mejor para... | Widgets pequenos, estados simples | Estados grandes, widgets criticos |

### Ejemplo completo: Login form

```dart
// ❌ BlocBuilder reconstruye todo el form en cada tecla
BlocBuilder<LoginBloc, LoginState>(
  builder: (context, state) {
    return Form(
      child: Column(
        children: [
          TextField(
            onChanged: (v) => context.read<LoginBloc>().add(
              EmailChanged(v),
            ),
          ),
          TextField(
            onChanged: (v) => context.read<LoginBloc>().add(
              PasswordChanged(v),
            ),
          ),
          // ... mas campos
          ElevatedButton(
            onPressed: state.isValid ? () { /* login */ } : null,
            child: Text('Entrar'),
          ),
        ],
      );
    );
  },
)

// ✅ BlocSelector solo reconstruye el boton cuando isValid cambia
Column(
  children: [
    // Cada TextField tiene su propio BlocSelector o usa BlocBuilder
    // con buildWhen especifico
    TextField(
      onChanged: (v) => context.read<LoginBloc>().add(EmailChanged(v)),
    ),
    TextField(
      onChanged: (v) => context.read<LoginBloc>().add(PasswordChanged(v)),
    ),
    // Solo el boton usa BlocSelector
    BlocSelector<LoginBloc, LoginState, bool>(
      selector: (state) => state.isValid,
      builder: (context, isValid) {
        return ElevatedButton(
          onPressed: isValid ? () { /* login */ } : null,
          child: Text('Entrar'),
        );
      },
    ),
  ],
)
```

---

## buildWhen en BlocBuilder

Si necesitas mas control que BlocSelector, usa `buildWhen`:

```dart
BlocBuilder<LoginBloc, LoginState>(
  // Solo reconstruye cuando isValid o isLoading cambian
  buildWhen: (previous, current) {
    return previous.isValid != current.isValid ||
           previous.isLoading != current.isLoading;
  },
  builder: (context, state) {
    return Column(
      children: [
        if (state.isLoading) CircularProgressIndicator(),
        ElevatedButton(
          onPressed: state.isValid ? () {} : null,
          child: Text('Entrar'),
        ),
      ],
    );
  },
)
```

### buildWhen vs BlocSelector

| Cuando usar | buildWhen | BlocSelector |
|---|---|---|
| Filtrar por multiples campos del estado | ✅ Mejor | Requiere combinar en un solo valor |
| Seleccionar un solo campo simple | Puede | ✅ Mejor |
| Control granular con logica compleja | ✅ Mejor | Limitado |
| Codigo conciso y declarativo | Mas verbose | ✅ Mas limpio |

---

## RepaintBoundary: limitar el area de repintado

Un `RepaintBoundary` le dice a Flutter: **"si este widget no cambio, no repintes nada dentro de el"**.

### Sin RepaintBoundary

```
Animacion en un widget hijo:
  ┌─────────────────────┐
  │ Padre (repintado)    │  ← Se repinta todo
  │ ┌─────────────────┐ │
  │ │ Hermano (repint) │ │  ← Innecesario
  │ ├─────────────────┤ │
  │ │ Hijo animado     │ │  ← El que realmente cambia
  │ ├─────────────────┤ │
  │ │ Hermano (repint) │ │  ← Innecesario
  │ └─────────────────┘ │
  └─────────────────────┘
```

### Con RepaintBoundary

```
Animacion en un widget hijo:
  ┌─────────────────────┐
  │ Padre (NO repintado) │  ← Se mantiene
  │ ┌─────────────────┐ │
  │ │ Hermano (NO)     │ │  ← Se mantiene
  │ ├─────────────────┤ │
  │ │ Hijo animado     │ │  ← Solo esto se repinta
  │ ├─────────────────┤ │
  │ │ Hermano (NO)     │ │  ← Se mantiene
  │ └─────────────────┘ │
  └─────────────────────┘
```

### Ejemplo

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return RepaintBoundary(  // ← Envuelve cada item
      child: ItemWidget(
        item: items[index],
        onAnimate: () { /* animacion */ },
      ),
    );
  },
)
```

### Cuando usar RepaintBoundary

| Escenario | Usar? |
|---|---|
| Lista con items que tienen animaciones independientes | **Si** |
| Widget con CustomPainter que se redibuja frecuentemente | **Si** |
| Texto que cambia raramente dentro de un area animada | **Si** |
| Widget simple sin animaciones | No necesario |
| Toda la pantalla como RepaintBoundary | Raramente util |

---

## Anti-patrones de setState

### Anti-patron 1: setState en loop

```dart
// ❌ MAL: setState se llama multiples veces
for (var item in items) {
  setState(() {
    item.selected = !item.selected;
  });
}
// Resultado: N rebuilds, uno por cada item

// ✅ BIEN: Un solo setState para todos los cambios
setState(() {
  for (var item in items) {
    item.selected = !item.selected;
  }
});
// Resultado: 1 solo rebuild
```

### Anti-patron 2: setState en didChangeDependencies

```dart
// ❌ MAL: didChangeDependencies puede llamarse muchas veces
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  setState(() {  // ← Causa rebuilds infinitos potencialmente
    _data = fetchData(context);
  });
}

// ✅ BIEN: Usar una bandera o inicializar en initState
@override
void initState() {
  super.initState();
  _loadData();
}

Future<void> _loadData() async {
  final data = await fetchData(context);
  if (mounted) {
    setState(() {
      _data = data;
    });
  }
}
```

### Anti-patron 3: setState sin cambios reales

```dart
// ❌ MAL: setState aunque nada haya cambiado
void onPressed() {
  setState(() {
    // No hay cambios en el estado
  });
}

// ✅ BIEN: Solo setState si hay cambios
void onPressed() {
  if (_counter < _max) {
    setState(() {
      _counter++;
    });
  }
}
```

### Anti-patron 4: Reasignar objetos mutables

```dart
// ❌ MAL: Flutter no detecta cambios en objetos mutables
final List<String> _items = [];

void addItem(String item) {
  _items.add(item);
  setState(() {});  // Flutter no sabe que _items cambio
}

// ✅ BIEN: Crear nueva referencia o usar List.from
final List<String> _items = [];

void addItem(String item) {
  setState(() {
    _items = [..._items, item];  // Nueva referencia
  });
}
```

---

## Reglas de oro para la optimizacion de rebuilds

| # | Regla | Herramienta |
|---|---|---|
| 1 | **Usa const** en todos los widgets que puedan serlo | `const` keyword |
| 2 | **Mueve widgets costosos** a su propio StatelessWidget | Extraccion de widgets |
| 3 | **Usa BlocSelector** para estados grandes | `BlocSelector` |
| 4 | **Agrega buildWhen** cuando BlocSelector no baste | `buildWhen` param |
| 5 | **Usa RepaintBoundary** en listas con animaciones | `RepaintBoundary` |
| 6 | **Usa Keys** en listas dinamicas | `ValueKey`, `UniqueKey` |
| 7 | **Un solo setState** por ciclo de actualizacion | Agrupar cambios |
| 8 | **Nunca mutar** el estado sin crear nueva referencia | Inmutabilidad |
| 9 | **Extrae widgets** que no dependen del estado | `StatelessWidget` |
| 10 | **Mide antes de optimizar** | DevTools Performance |

---

## Ejemplos: antes vs despues

### Ejemplo 1: Lista con items constantes

**Antes:**
```dart
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      Text('Titulo de seccion'),       // No const
      Icon(Icons.settings),             // No const
      Divider(),                        // No const
      ...items.map((i) => ItemWidget(i)),
    ],
  );
}
```

**Despues:**
```dart
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      const Text('Titulo de seccion'), // Const
      const Icon(Icons.settings),       // Const
      const Divider(),                  // Const
      ...items.map((i) => ItemWidget(
        key: ValueKey(i.id),           // Key
        item: i,
      )),
    ],
  );
}
```

### Ejemplo 2: Widget hijo innecesario

**Antes:**
```dart
class ParentWidget extends StatefulWidget {
  @override
  State<ParentWidget> createState() => _ParentWidgetState();
}

class _ParentWidgetState extends State<ParentWidget> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ExpensiveChild(),  // ← Se reconstruye cada vez
        Text('Counter: $_counter'),
        ElevatedButton(
          onPressed: () => setState(() => _counter++),
          child: Text('Increment'),
        ),
      ],
    );
  }
}

class ExpensiveChild extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Construccion costosa...
    return ComplexWidget();
  }
}
```

**Despues:**
```dart
class ParentWidget extends StatefulWidget {
  @override
  State<ParentWidget> createState() => _ParentWidgetState();
}

class _ParentWidgetState extends State<ParentWidget> {
  int _counter = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: const [
        ExpensiveChild(),  // Const, no se reconstruye
      ],
    )..add(
        // Los widgets que cambian se separan
        Column(
          children: [
            Text('Counter: $_counter'),
            ElevatedButton(
              onPressed: () => setState(() => _counter++),
              child: Text('Increment'),
            ),
          ],
        ),
      );
  }
}
```

---

## Matriz de decision: cual tecnica para que escenario

| Escenario | Tecnica principal | Tecnica secundaria |
|---|---|---|
| Textos, iconos, espaciados estaticos | `const` | - |
| Lista de items con ID | `ValueKey` | `ListView.builder` |
| Estado BLoC con 1 campo relevante | `BlocSelector` | - |
| Estado BLoC con multiples campos | `buildWhen` | `BlocSelector` multiple |
| Animacion en un item de lista | `RepaintBoundary` | `AnimatedBuilder` |
| Widget complejo que rara vez cambia | `StatelessWidget` extraccion | `const` |
| setState con multiples cambios | Agrupar en un solo `setState` | - |
| Objeto mutable que cambia | Nueva referencia (`List.from`) | Inmutabilidad |
| Widget con painter custom | `shouldRepaint: false` | `RepaintBoundary` |
| Texto que cambia en area animada | `RepaintBoundary` + `const` | Extraccion |
