# 02 - Inspector y Debug Layout

## Flutter Inspector - Vista general

### Pestañas principales

| Pestaña | Propósito |
|---------|-----------|
| **Widget Tree** | Árbol jerárquico de widgets |
| **Details Panel** | Propiedades del widget seleccionado |
| **Layout Explorer** | Visualización de constraints y flex |
| **Performance Overlay** | Gráfico de rendimiento integrado |

---

## Widget Tree

### Navegación por el árbol

```
MaterialApp
  └─ Navigator
       └─ Scaffold
            ├─ AppBar
            │    └─ Text ("Mi App")
            └─ Body
                 └─ Column
                      ├─ Padding
                      │    └─ Text ("Hello")
                      └─ Expanded
                           └─ ListView
                                └─ ListTile
                                     └─ Text ("Item 1")
```

### Iconos de widgets

| Icono | Tipo |
|-------|------|
| 🟦 | Widget normal |
| 🟨 | Widget con children (expanded) |
| 🟩 | Widget leaf (sin children) |
| 🟪 | Widget de plataforma |
| 🔵 | Widget seleccionado |

### Filtrar widgets
1. Barra de búsqueda arriba del Widget Tree
2. Filtrar por nombre de widget
3. `Ctrl+F` para buscar texto específico

---

## Layout Explorer - Entender constraints

### ¿Qué muestra?

Visualiza los **constraints** (tamaños que el padre impone) y el **size** (tamaño real del widget).

### Ejemplo visual: Column con hijos

```
Parent constraints: 0 ≤ width ≤ 411, 0 ≤ height ≤ ∞

Column {
  ┌─────────────────────────────────┐
  │  Padding (0, 0, 0, 8)          │  ← Height: 48
  │  ┌───────────────────────────┐  │
  │  │  Text "Title"             │  │
  │  └───────────────────────────┘  │
  ├─────────────────────────────────┤
  │  Expanded (flex: 1)             │  ← Height: ∞ (flex)
  │  ┌───────────────────────────┐  │
  │  │  ListView                 │  │
  │  │  ┌─────────────────────┐  │  │
  │  │  │  ListTile           │  │  │
  │  │  ├─────────────────────┤  │  │
  │  │  │  ListTile           │  │  │
  │  │  └─────────────────────┘  │  │
  │  └───────────────────────────┘  │
  └─────────────────────────────────┘
}
```

### Herramientas de Layout Explorer

| Herramienta | Descripción |
|-------------|-------------|
| **Select Widget** | Click en Widget Tree para ver layout |
| **Toggle Debug Paint** | Muestra bordes y constraints |
| **Refresh Tree** | Actualiza después de hot reload |

---

## Debug Paint - Visualización de boundaries

### Qué muestra cada color

| Color | Significado |
|-------|-------------|
| 🟦 Azul | Bounds del widget |
| 🟩 Verde | Overflow indicator |
| 🟨 Amarillo | Padding/margin |
| 🔴 Rojo | Error de layout |

### Activar Debug Paint

```dart
// Temporalmente en código
MaterialApp(
  debugShowCheckedModeBanner: true,
  showPerformanceOverlay: true,  // ← Overlay de rendimiento
  // Debug paint se activa desde DevTools o:
  // flutter run --debug --enable-software-rendering
)
```

### Desde DevTools:
1. Inspector → Click en "Toggle Debug Paint" (icono 🎨)
2. Navegar por la app → ver boundaries en tiempo real
3. Desactivar al terminar

---

## Propiedades de widgets comunes

### Container
```
Container {
  width: 300.0,
  height: 200.0,
  padding: EdgeInsets(16.0),
  margin: EdgeInsets(8.0),
  decoration: BoxDecoration {
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8.0)
  }
}
```

### Row/Column (Flex)
```
Row {
  direction: horizontal,
  mainAxisAlignment: start,
  crossAxisAlignment: center,
  mainAxisSize: max,
  children: 3
}
```

### Expanded
```
Expanded {
  flex: 2,
  child: Text("Content")
}
```

### Padding
```
Padding {
  padding: EdgeInsets.all(16.0),
  child: Text("Padded content")
}
```

---

## Layout debugging paso a paso

### Problema común: Widget no aparece

**Caso:** Un widget no se muestra en pantalla

**Paso 1:** Verificar en Inspector que el widget existe en el árbol
- Si no existe → problema de lógica (condicional, null check)

**Paso 2:** Verificar constraints
- `width: 0` o `height: 0` → widget tiene tamaño cero
- Causa: Padding incorrecto,父亲 con constraints restrictivos

**Paso 3:** Verificar Overflow
- Layout Explorer muestra 🟩 verde → contenido desbordado
- Fix: Usar SingleChildScrollView o ajustar tamaños

### Problema común: Widget desbordado

**Caso:** Layout overflow error

**Paso 1:** Activar Debug Paint en DevTools
**Paso 2:** Identificar widget que causa overflow
**Paso 3:** Verificar si es Flex (Row/Column) con hijos que exceden espacio

**Solución típica:**
```dart
// Antes (overflow)
Row(
  children: [
    Text("Very long text that exceeds screen width"),
    Icon(Icons.star),
  ],
)

// Después (wrap)
Wrap(
  children: [
    Text("Very long text that exceeds screen width"),
    Icon(Icons.star),
  ],
)
```

---

## Ejercicios prácticos

### Ejercicio 1: Layout Explorer con ListView

1. Crear app con ListView que tiene 100 items
2. Abrir DevTools → Inspector
3. Seleccionar ListView en Widget Tree
4. En Layout Explorer ver:
   - Viewport height (cuánto espacio visible)
   - Content height (cuánto contenido total)
   - Scroll offset (dónde estamos scrolleando)
5. Scroll en la app → ver cómo cambia el offset en tiempo real

### Ejercicio 2: Debug Paint con Stack

```dart
Stack(
  children: [
    Container(width: 200, height: 200, color: Colors.red),
    Positioned(
      top: 50,
      left: 50,
      child: Container(width: 100, height: 100, color: Colors.blue),
    ),
  ],
)
```

1. Activar Debug Paint
2. Ver cómo `Positioned` afecta el layout
3. Verificar que el Stack toma el tamaño del hijo más grande

### Ejercicio 3: Performance Overlay

```dart
MaterialApp(
  showPerformanceOverlay: true,  // ← Activar
  home: MyHome(),
)
```

1. Ver overlay con两条 gráficas:
   - **Shader compilation**: Tiempo de compilar shaders
   - **Frame rendering**: Tiempo de renderizar frames
2. Identificar frames que toman >16ms (causan jank)
3. Usar Performance view para más detalles

---
→ Siguiente: `03-performance-view.md`
