# 09 — Flutter Inspector y Debug de Layout

> Explorar el árbol de widgets, entender constraints con el Layout Explorer y visualizar boundaries con Debug Paint.

---

## 1. Vista general del Flutter Inspector

### 1.1 Pestañas principales

| Pestaña | Propósito |
|---|---|
| **Widget Tree** | Árbol jerárquico de widgets |
| **Details Panel** | Propiedades del widget seleccionado |
| **Layout Explorer** | Visualización de constraints y flex |

---

## 2. Widget Tree

### 2.1 Navegación por el árbol

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

### 2.2 Filtrar widgets

1. Usa la barra de búsqueda arriba del Widget Tree
2. Filtra por nombre de widget
3. `Ctrl+F` para buscar texto específico

### 2.3 Select widget

Haz click en cualquier widget del árbol para ver sus **propiedades** en el Details Panel y su layout en el Layout Explorer. También puedes usar el modo **Select Widget** para elegir el widget directamente en la app.

---

## 3. Layout Explorer — Entender constraints

### 3.1 ¿Qué muestra?

Visualiza los **constraints** (tamaños que el padre impone) y el **size** (tamaño real del widget).

### 3.2 Ejemplo visual: Column con hijos

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

### 3.3 Herramientas del Layout Explorer

| Herramienta | Descripción |
|---|---|
| **Select Widget** | Elegir un widget en el árbol o en la app |
| **Toggle Debug Paint** | Muestra borders y constraints |
| **Refresh Tree** | Actualiza después de hot reload |

---

## 4. Debug Paint — Visualización de boundaries

### 4.1 Qué muestra cada color

| Color | Significado |
|---|---|
| 🟦 Azul | Bounds del widget |
| 🟩 Verde | Overflow indicator |
| 🟨 Amarillo | Padding/margin |
| 🔴 Rojo | Error de layout |

### 4.2 Activar Debug Paint

Desde DevTools:
1. Inspector → click en **Toggle Debug Paint** (icono 🎨)
2. Navegar por la app → ver boundaries en tiempo real
3. Desactivar al terminar

> También puedes activarlo en código con `debugPaintSizeEnabled` (desde `package:flutter/rendering.dart`), pero desde DevTools no requieres tocar el código.

---

## 5. Propiedades de widgets comunes

### 5.1 Container

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

### 5.2 Row/Column (Flex)

```
Row {
  direction: horizontal,
  mainAxisAlignment: start,
  crossAxisAlignment: center,
  mainAxisSize: max,
  children: 3
}
```

### 5.3 Expanded

```
Expanded {
  flex: 2,
  child: Text("Content")
}
```

### 5.4 Padding

```
Padding {
  padding: EdgeInsets.all(16.0),
  child: Text("Padded content")
}
```

---

## 6. Layout debugging paso a paso

### 6.1 Problema común: widget no aparece

**Caso:** un widget no se muestra en pantalla

**Paso 1:** Verificar en Inspector que el widget existe en el árbol
- Si no existe → problema de lógica (condicional, null check)

**Paso 2:** Verificar constraints
- `width: 0` o `height: 0` → el widget tiene tamaño cero
- Causa: padding incorrecto, o un padre con constraints restrictivos

**Paso 3:** Verificar overflow
- Layout Explorer muestra 🟩 verde → contenido desbordado
- Fix: usar `SingleChildScrollView`, `Wrap` o ajustar tamaños

### 6.2 Problema común: widget desbordado

**Caso:** layout overflow error

**Paso 1:** Activar Debug Paint en DevTools
**Paso 2:** Identificar el widget que causa overflow
**Paso 3:** Verificar si es un Flex (Row/Column) con hijos que exceden el espacio

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

## 7. Ejercicios prácticos

### 7.1 Ejercicio 1: Layout Explorer con ListView

1. Crear app con ListView que tiene 100 items
2. Abrir DevTools → Inspector
3. Seleccionar ListView en Widget Tree
4. En Layout Explorer ver:
   - Viewport height (cuánto espacio visible)
   - Content height (cuánto contenido total)
   - Scroll offset (dónde estamos scrolleando)
5. Scroll en la app → ver cómo cambia el offset en tiempo real

### 7.2 Ejercicio 2: Debug Paint con Stack

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

### 7.3 Ejercicio 3: Performance Overlay

```dart
MaterialApp(
  showPerformanceOverlay: true,  // ← Activar
  home: MyHome(),
)
```

1. Ver el overlay con las dos gráficas:
   - **Shader compilation**: tiempo de compilar shaders
   - **Frame rendering**: tiempo de renderizar frames
2. Identificar frames que toman >16 ms (causan jank)
3. Usar la Performance view para más detalles

---

## Resumen

| Herramienta | Para qué |
|---|---|
| Widget Tree | Navegar la jerarquía de widgets |
| Details Panel | Ver propiedades del widget |
| Layout Explorer | Entender constraints y size |
| Debug Paint | Ver boundaries y overflows visualmente |
| Select Widget | Elegir widgets directamente en la app |

---

## 📚 Referencias

- [Flutter | Flutter Inspector](https://docs.flutter.dev/tools/devtools/inspector) — Documentación oficial del Inspector
- [Flutter | Understanding constraints](https://docs.flutter.dev/ui/layout/constraints) — Cómo funcionan los constraints en Flutter
- [Flutter | Performance overlay](https://docs.flutter.dev/perf/ui-performance) — Cómo leer el Performance Overlay

---

> 📖 **Siguiente:** [10-performance-view.md](./10-performance-view.md) — La Performance view: FPS, frames y jank
