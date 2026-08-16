# 20 — Optimizando Rebuilds Innecesarios

> `const`, Keys, reconstrucción selectiva y `RepaintBoundary` para evitar que tu widget tree se reconstruya sin necesidad.

---

## 1. Por qué los rebuilds innecesarios son el problema #1

En Flutter, **cada vez que un widget se reconstruye, todos sus hijos también se reconstruyen**. Si tu widget tree es profundo y un widget padre llama a `setState()` frecuentemente, puedes estar reconstruyendo cientos de widgets sin necesidad.

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

Solo ListWidget cambió, pero TODO se reconstruyó.
```

---

## 2. El keyword `const`: la optimización más simple

### 2.1 Qué hace `const`

Cuando marcas un widget como `const`, Flutter **reutiliza la misma instancia** en lugar de crear una nueva. No se ejecuta `build()` para ese widget ni sus hijos.

### 2.2 Sin const

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

### 2.3 Con const

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

### 2.4 Reglas de const

| Regla | Ejemplo | Resultado |
|---|---|---|
| Todos los parámetros deben ser compile-time | `Text('literal')` | OK |
| Parámetros dinámicos | `Text(variable)` | NO puedes usar const |
| Sub-widgets const | `const [Text('a'), Text('b')]` | OK |
| Solo algunos hijos son const | Individuales: `const Text('a')` | OK |
| Widget con `key` | `const Text('a', key: ValueKey(1))` | OK |

### 2.5 Cuándo NO usar const

```dart
// ❌ NO puedes usar const aquí
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

## 3. Keys: controlar el matching de widgets

Las **Keys** le dicen a Flutter cómo emparejar widgets entre rebuilds. Sin la key correcta, Flutter puede reutilizar el widget equivocado.

### 3.1 Tipos de Keys

| Key | Qué hace | Cuándo usar |
|---|---|---|
| **ValueKey** | Identifica por un valor (String, int, etc.) | Items de lista con ID único |
| **ObjectKey** | Identifica por referencia a objeto | Objetos que pueden no ser `==` |
| **UniqueKey** | Identifica por identidad única | Forzar recreación completa |
| **GlobalKey** | Acceso al estado del widget desde cualquier lugar | Formularios, navegación |

### 3.2 Ejemplo: ValueKey en listas

```dart
// ❌ Sin key: Flutter puede mezclar items al reordenar
ListView(
  children: items.map((item) => ItemWidget(item)).toList(),
)

// ✅ Con ValueKey: Flutter sabe qué item es cada widget
ListView(
  children: items.map((item) => ItemWidget(
    key: ValueKey(item.id),
    item: item,
  )).toList(),
)
```

### 3.3 Cuándo usar cada Key

```
Necesitas Key?
├── Lista de items con ID único → ValueKey(item.id)
├── Lista de objetos sin ID estable → UniqueKey()
├── Necesitas acceder al estado de un widget → GlobalKey()
├── Widget se mueve entre padres → GlobalKey()
└── No hay problemas de matching → Sin key (default)
```

---

## 4. BlocSelector vs BlocBuilder: reconstrucción selectiva

### 4.1 El problema con BlocBuilder

```dart
// ❌ BlocBuilder reconstruye TODO cuando el estado cambia
BlocBuilder<AuthBloc, AuthState>(
  builder: (context, state) {
    return Column(
      children: [
        Text('User: ${state.user.name}'),  // ← Solo esto cambia
        Text('Email: ${state.user.email}'), // ← Pero todo se reconstruye
        // ... 50 widgets más ...
        BigExpensiveWidget(),               // ← Incluido este
      ],
    );
  },
)
```

### 4.2 La solución: BlocSelector

```dart
// ✅ BlocSelector solo reconstruye cuando el valor seleccionado cambia
BlocSelector<AuthBloc, AuthState, String>(
  selector: (state) => state.user.name,  // ← Solo monitorea esto
  builder: (context, name) {
    return Text('User: $name');           // ← Solo este widget se rebuild
  },
)
```

### 4.3 Comparación BlocBuilder vs BlocSelector

| Característica | BlocBuilder | BlocSelector |
|---|---|---|
| Reconstruye cuando... | Cualquier cambio de estado | Solo cuando el selector cambia |
| Granularidad | Todo el subtree | Widget específico |
| Uso de memoria | Más alto | Más bajo |
| Complejidad | Simple | Requiere definir selector |
| Mejor para... | Widgets pequeños, estados simples | Estados grandes, widgets críticos |

### 4.4 Ejemplo completo: Login form

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
          // ... más campos
          ElevatedButton(
            onPressed: state.isValid ? () { /* login */ } : null,
            child: const Text('Entrar'),
          ),
        ],
      ),
    );
  },
)

// ✅ Cada TextField usa context.read y solo el botón escucha el estado
Column(
  children: [
    TextField(
      onChanged: (v) => context.read<LoginBloc>().add(EmailChanged(v)),
    ),
    TextField(
      onChanged: (v) => context.read<LoginBloc>().add(PasswordChanged(v)),
    ),
    // Solo el botón usa BlocSelector
    BlocSelector<LoginBloc, LoginState, bool>(
      selector: (state) => state.isValid,
      builder: (context, isValid) {
        return ElevatedButton(
          onPressed: isValid ? () { /* login */ } : null,
          child: const Text('Entrar'),
        );
      },
    ),
  ],
)
```

---

## 5. buildWhen en BlocBuilder

Si necesitas más control que `BlocSelector`, usa `buildWhen`:

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
        if (state.isLoading) const CircularProgressIndicator(),
        ElevatedButton(
          onPressed: state.isValid ? () {} : null,
          child: const Text('Entrar'),
        ),
      ],
    );
  },
)
```

### 5.1 buildWhen vs BlocSelector

| Cuándo usar | buildWhen | BlocSelector |
|---|---|---|
| Filtrar por múltiples campos del estado | ✅ Mejor | Requiere combinar en un solo valor |
| Seleccionar un solo campo simple | Puede | ✅ Mejor |
| Control granular con lógica compleja | ✅ Mejor | Limitado |
| Código conciso y declarativo | Más verbose | ✅ Más limpio |

---

## 6. RepaintBoundary: limitar el área de repintado

Un `RepaintBoundary` le dice a Flutter: **"si este widget no cambió, no repintes nada dentro de él"**.

### 6.1 Sin RepaintBoundary

```
Animación en un widget hijo:
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

### 6.2 Con RepaintBoundary

```
Animación en un widget hijo:
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

### 6.3 Ejemplo

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return RepaintBoundary(  // ← Envuelve cada item
      child: ItemWidget(
        item: items[index],
        onAnimate: () { /* animación */ },
      ),
    );
  },
)
```

### 6.4 Cuándo usar RepaintBoundary

| Escenario | ¿Usar? |
|---|---|
| Lista con items que tienen animaciones independientes | **Sí** |
| Widget con CustomPainter que se redibuja frecuentemente | **Sí** |
| Texto que cambia raramente dentro de un área animada | **Sí** |
| Widget simple sin animaciones | No necesario |
| Toda la pantalla como RepaintBoundary | Raramente útil |

---

## 7. Anti-patrones de setState

### 7.1 Anti-patrón 1: setState en loop

```dart
// ❌ MAL: setState se llama múltiples veces
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

### 7.2 Anti-patrón 2: setState en didChangeDependencies

```dart
// ❌ MAL: didChangeDependencies puede llamarse muchas veces
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  setState(() {  // ← Causa rebuilds potencialmente infinitos
    _data = fetchData(context);
  });
}

// ✅ BIEN: Inicializar en initState con una carga async
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

### 7.3 Anti-patrón 3: setState sin cambios reales

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

### 7.4 Anti-patrón 4: reasignar objetos mutables

```dart
// ❌ MAL: Flutter no detecta cambios en objetos mutables
final List<String> _items = [];

void addItem(String item) {
  _items.add(item);
  setState(() {});  // Flutter no sabe que _items cambió
}

// ✅ BIEN: Crear una nueva referencia
final List<String> _items = [];

void addItem(String item) {
  setState(() {
    _items = [..._items, item];  // Nueva referencia
  });
}
```

---

## 8. Reglas de oro para la optimización de rebuilds

| # | Regla | Herramienta |
|---|---|---|
| 1 | **Usa const** en todos los widgets que puedan serlo | `const` keyword |
| 2 | **Mueve widgets costosos** a su propio StatelessWidget | Extracción de widgets |
| 3 | **Usa BlocSelector** para estados grandes | `BlocSelector` |
| 4 | **Agrega buildWhen** cuando BlocSelector no baste | `buildWhen` param |
| 5 | **Usa RepaintBoundary** en listas con animaciones | `RepaintBoundary` |
| 6 | **Usa Keys** en listas dinámicas | `ValueKey`, `UniqueKey` |
| 7 | **Un solo setState** por ciclo de actualización | Agrupar cambios |
| 8 | **Nunca mutar** el estado sin crear nueva referencia | Inmutabilidad |
| 9 | **Extrae widgets** que no dependen del estado | `StatelessWidget` |
| 10 | **Mide antes de optimizar** | DevTools Performance |

---

## 9. Ejemplos: antes vs después

### 9.1 Ejemplo 1: lista con items constantes

**Antes:**

```dart
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      Text('Titulo de seccion'),       // No const
      Icon(Icons.settings),            // No const
      const Divider(),                 // No const
      ...items.map((i) => ItemWidget(i)),
    ],
  );
}
```

**Después:**

```dart
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      const Text('Titulo de seccion'), // Const
      const Icon(Icons.settings),      // Const
      const Divider(),                 // Const
      ...items.map((i) => ItemWidget(
        key: ValueKey(i.id),           // Key
        item: i,
      )),
    ],
  );
}
```

### 9.2 Ejemplo 2: extraer el subtree que cambia

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
        const ExpensiveChild(),  // Se reconstruye cada vez
        Text('Counter: $_counter'),
        ElevatedButton(
          onPressed: () => setState(() => _counter++),
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

**Después:** extraer el bloque que cambia a su propio widget con estado:

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
        const ExpensiveChild(),  // const → no se reconstruye
        _CounterSection(
          counter: _counter,
          onIncrement: () => setState(() => _counter++),
        ),
      ],
    );
  }
}

class _CounterSection extends StatelessWidget {
  const _CounterSection({required this.counter, required this.onIncrement});

  final int counter;
  final VoidCallback onIncrement;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Counter: $counter'),
        ElevatedButton(
          onPressed: onIncrement,
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

---

## 10. Matriz de decisión: qué técnica para qué escenario

| Escenario | Técnica principal | Técnica secundaria |
|---|---|---|
| Textos, iconos, espaciados estáticos | `const` | – |
| Lista de items con ID | `ValueKey` | `ListView.builder` |
| Estado BLoC con 1 campo relevante | `BlocSelector` | – |
| Estado BLoC con múltiples campos | `buildWhen` | Múltiples `BlocSelector` |
| Animación en un item de lista | `RepaintBoundary` | `AnimatedBuilder` |
| Widget complejo que rara vez cambia | Extracción `StatelessWidget` | `const` |
| setState con múltiples cambios | Agrupar en un solo `setState` | – |
| Objeto mutable que cambia | Nueva referencia (`[...]`) | Inmutabilidad |
| Widget con painter custom | `shouldRepaint: false` | `RepaintBoundary` |
| Texto que cambia en área animada | `RepaintBoundary` + `const` | Extracción |

---

## Resumen

| Concepto | Clave |
|---|---|
| **`const`** | Reutiliza la instancia, sin `build()` |
| **Keys** | Emparejamiento correcto de widgets |
| **BlocSelector** | Rebuild solo cuando el selector cambia |
| **buildWhen** | Control fino sobre cuándo reconstruir |
| **RepaintBoundary** | Limita el área de repintado |
| **setState** | Un solo call por ciclo, sin mutar el estado |

---

## 📚 Referencias

- [Flutter | const performance](https://docs.flutter.dev/perf/const) — Uso de `const` para rendimiento
- [Bloc | BlocSelector y buildWhen](https://bloclibrary.dev) — Documentación oficial de bloc
- [Flutter | RepaintBoundary](https://api.flutter.dev/flutter/widgets/RepaintBoundary-class.html) — API de RepaintBoundary

---

> 📖 **Siguiente:** [21-memory-leak-detection.md](./21-memory-leak-detection.md) — Detección y prevención de memory leaks
