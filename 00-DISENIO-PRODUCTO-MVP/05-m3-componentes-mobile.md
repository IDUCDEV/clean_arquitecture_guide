# 05 — Componentes M3 Clave para Mobile

**El arsenal de UI para construir tu MVP**

---

M3 clasifica sus componentes en 5 categorías. Aquí cubrimos los que más usarás en un MVP mobile.

## 1. Navegación

### NavigationBar (antes BottomNavigationBar)

El estándar para navegación principal en mobile.

```dart
NavigationBar(
  selectedIndex: 0,
  onDestinationSelected: (index) {},
  destinations: const [
    NavigationDestination(icon: Icon(Icons.home), label: 'Inicio'),
    NavigationDestination(icon: Icon(Icons.search), label: 'Buscar'),
    NavigationDestination(icon: Icon(Icons.favorite), label: 'Favoritos'),
    NavigationDestination(icon: Icon(Icons.person), label: 'Perfil'),
  ],
)
```

**Reglas M3:**
- Máximo 5 destinos
- Destino activo usa `primary` + tonal surface
- Muestra el label siempre (excepto en pantallas muy angostas)

### NavigationDrawer

Para navegación secundaria o apps con muchas secciones.

```dart
Drawer(
  child: NavigationDrawer(
    selectedIndex: 0,
    onDestinationSelected: (index) {},
    children: [
      NavigationDrawerDestination(
        icon: Icon(Icons.inbox),
        label: Text('Inbox'),
      ),
    ],
  ),
)
```

### TopAppBar

La barra superior. M3 tiene 3 variantes:

| Variante | Uso |
|---|---|
| `AppBar` (centerTitle) | Pantallas principales |
| `AppBar` (small/leading) | Pantallas de detalle |
| `SliverAppBar` | Scroll con colapso |

## 2. Contenido

### Card

Contenedor para información agrupada.

```dart
Card(
  child: Column(
    children: [
      ListTile(
        leading: CircleAvatar(child: Icon(Icons.tennis)),
        title: Text('Cancha de Tenis'),
        subtitle: Text('Club Deportivo'),
      ),
      Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          TextButton(onPressed: {}, child: Text('Reservar')),
        ],
      ),
    ],
  ),
)
```

Variantes: `Card` (elevated), `Card.outlined`, `Card.filled`.

### ListTile

Ítem estándar para listas.

```dart
ListTile(
  leading: Icon(Icons.location_on),
  title: Text('Club Deportivo'),
  subtitle: Text('A 2.3 km'),
  trailing: Chip(label: Text('\$15/h')),
)
```

## 3. Acción

### Buttons

M3 tiene una jerarquía clara:

| Tipo | Énfasis | Uso |
|---|---|---|
| `FilledButton` | Alto | Acción principal (Continuar, Pagar) |
| `FilledTonalButton` | Medio | Acción secundaria importante |
| `OutlinedButton` | Medio | Acción alternativa |
| `TextButton` | Bajo | Acción menos importante (Cancelar) |

```dart
FilledButton(onPressed: () {}, child: Text('Reservar ahora'))
FilledButton.icon(
  icon: Icon(Icons.shopping_cart),
  label: Text('Agregar al carrito'),
)
```

### FAB (FloatingActionButton)

Para la acción principal de la pantalla.

```dart
FloatingActionButton(
  onPressed: () {},
  child: Icon(Icons.add),
)
// Variante extendida (con texto):
FloatingActionButton.extended(
  onPressed: () {},
  icon: Icon(Icons.add),
  label: Text('Nueva reserva'),
)
```

### SegmentedButton

Alternativa moderna a RadioButton / ToggleButtons.

```dart
SegmentedButton<String>(
  segments: [
    ButtonSegment(value: 'day', label: Text('Día')),
    ButtonSegment(value: 'week', label: Text('Semana')),
    ButtonSegment(value: 'month', label: Text('Mes')),
  ],
  selected: selected,
  onSelectionChanged: (v) {},
)
```

## 4. Entrada de texto

### TextField

```dart
TextField(
  decoration: InputDecoration(
    labelText: 'Buscar canchas',
    prefixIcon: Icon(Icons.search),
    filled: true,
  ),
)
```

### SearchBar

Nuevo en M3. Más moderno que TextField para búsquedas.

```dart
SearchBar(
  leading: Icon(Icons.search),
  hintText: 'Buscar canchas...',
  onSubmitted: (v) {},
)
```

## 5. Feedback

### SnackBar

Notificaciones temporales.

```dart
ScaffoldMessenger.of(context).showSnackBar(
  SnackBar(content: Text('Reserva confirmada')),
)
```

### Badge

Indicadores de notificaciones o conteo.

```dart
Badge(
  label: Text('3'),
  child: IconButton(icon: Icon(Icons.notifications)),
)
```

### AlertDialog

Diálogos de confirmación.

```dart
AlertDialog(
  title: Text('Confirmar reserva'),
  content: Text('¿Reservar cancha por \$15/h?'),
  actions: [
    TextButton(onPressed: () {}, child: Text('Cancelar')),
    FilledButton(onPressed: () {}, child: Text('Confirmar')),
  ],
)
```

## Mapa de componentes para tu MVP

Usa esta tabla para decidir qué componente usar en cada parte de tu app:

| Necesidad | Componente M3 |
|---|---|
| Navegación principal | `NavigationBar` (inferior) o `NavigationDrawer` (lateral) |
| Barra superior | `TopAppBar` |
| Lista de ítems | `Card` + `ListTile` |
| Acción principal | `FilledButton` o `FAB` |
| Acción secundaria | `FilledTonalButton` |
| Selección única | `SegmentedButton` o `ChoiceChip` |
| Selección múltiple | `FilterChip` |
| Búsqueda | `SearchBar` |
| Formulario | `TextField` + `FilledButton` |
| Fecha | `DatePickerDialog` |
| Hora | `TimePickerDialog` |
| Confirmación | `AlertDialog` o `BottomSheet` |
| Feedback breve | `SnackBar` |
| Notificación | `Badge` |
| Progreso | `LinearProgressIndicator` o `CircularProgressIndicator` |
| Vacío / Error | `Center` + `Icon` + `Text` (diseño propio) |

## Regla de oro

> Para cada pantalla del storyboard (del Design Sprint), identifica primero **qué necesidad de UI tiene** y luego ve a la tabla de arriba para elegir el componente M3.

---

**Siguiente: [06 — Prototipado y Validación](06-prototipado-validacion.md)**
