# Canvas y Toolbar

> Domina el lienzo infinito de Pencil y todas las herramientas de dibujo. Aprenderás a navegar, crear frames, dibujar formas, insertar texto y usar cada herramienta de la toolbar.

---

## Índice

- [El Canvas (Lienzo)](#el-canvas-lienzo)
- [Frames](#frames)
- [Toolbar: Herramientas de Dibujo](#toolbar-herramientas-de-dibujo)
- [Toolbar: Importación](#toolbar-importación)
- [Mini-práctica](#mini-práctica)

---

## El Canvas (Lienzo)

El canvas de Pencil es **infinito**. No hay límites de tamaño ni de posición. Puedes tener múltiples frames, componentes y anotaciones dispersos por el espacio sin restricciones.

### Navegación

| Acción | Cómo |
|---|---|
| **Pan (desplazar)** | Space + Arrastrar con el mouse |
| **Pan alternativo** | Herramienta Hand (H) + Arrastrar |
| **Zoom in** | `Cmd/Ctrl` + Scroll hacia arriba, o `=` |
| **Zoom out** | `Cmd/Ctrl` + Scroll hacia abajo, o `-` |
| **Scroll horizontal** | Shift + Scroll |
| **Zoom 100%** | `0` |
| **Zoom to fit (ver todo)** | `1` |
| **Zoom to selection** | `2` |

### Canvas Settings

| Atajo | Acción |
|---|---|
| `Cmd/Ctrl + '` | Toggle pixel grid |
| `Cmd/Ctrl + Shift + '` | Toggle snap to pixel grid |

### Selection Highlighting

Cuando seleccionas elementos en el canvas, los bounding boxes tienen colores que indican el tipo:

- **Azul** → Elemento normal (frame, rect, text, etc.)
- **Magenta** → Origen de componente (la fuente de verdad)
- **Violeta** → Instancia de componente (copia vinculada al origen)

---

## Frames

Los frames son **contenedores** que agrupan elementos. Son el equivalente a las Artboards de Sketch o las Pages de Figma.

### Para qué sirven

- Definir los límites de una pantalla (ej: 390×844 para iPhone 14)
- Agrupar una sección de diseño (header, hero, footer)
- Establecer un viewport para exportar

### Crear un Frame

1. Presiona `A` o `F` (Frame tool)
2. Haz clic y arrastra en el canvas
3. Suelta cuando tengas el tamaño deseado

### Ajustar Tamaño

Con el frame seleccionado, en el Properties Panel puedes:
- Escribir valores exactos de **W** (width) e **H** (height)
- Cambiar **X** e **Y** para posicionar

### Frames vs Grupos

| Frame | Grupo |
|---|---|
| Tiene dimensiones propias | Se ajusta al contenido |
| Puede tener fondo propio | No tiene fondo |
| Se exporta individualmente | Se exporta como conjunto |
| Ideal para pantallas completas | Ideal para agrupar elementos relacionados |

---

## Toolbar: Herramientas de Dibujo

La toolbar está en la parte superior del editor. Cada herramienta tiene un **atajo de teclado** de una sola letra.

### Move Tool (V)

La herramienta más usada. Con ella puedes:

- **Seleccionar** un elemento haciendo clic
- **Mover** elementos arrastrando
- **Redimensionar** desde los handles de las esquinas
- **Selección múltiple** arrastrando un rectángulo alrededor de varios elementos

### Hand Tool (H)

Alternativa a Space+Drag para desplazar el canvas. Útil cuando quieres navegar sin mantener presionada la barra espaciadora.

### Frame Tool (A / F)

Crea frames. Ya cubierto en detalle arriba.

### Rectangle Tool (R)

Dibuja rectángulos y cuadrados.

- Arrastra libremente para rectángulos
- Mantén `Shift` mientras arrastras para **cuadrados perfectos**
- Úsalo para: fondos, botones, inputs, cards, imágenes placeholder

### Ellipse Tool (O)

Dibuja círculos y elipses.

- Arrastra libremente para elipses
- Mantén `Shift` para **círculos perfectos**
- Úsalo para: avatares, botones redondos, badges, indicadores

### Text Tool (T)

Inserta texto en el canvas.

1. Presiona `T`
2. Haz clic en el canvas donde quieras el texto
3. Escribe
4. Ajusta propiedades en el panel derecho (font, size, weight, color, alignment)

**Tipos de texto:**
- **Point text** (haces clic, escribes, se expande horizontalmente)
- **Paragraph text** (arrastras para crear un área de texto con width fijo y wrap)

### Sticky Note (N)

Notas adhesivas para anotaciones, comentarios y documentación dentro del diseño.

- Útil para: explicar decisiones de diseño, dejar tareas pendientes, documentar flujos alternativos
- No se exportan en la exportación normal de elementos

---

## Toolbar: Importación

En el chevron (▼) debajo del icono de Rectangle en la toolbar:

| Opción | Qué hace |
|---|---|
| **Import Figma** | Seleccionar un archivo `.fig` completo e importarlo |
| **Import Image or SVG...** | Seleccionar PNG, JPEG o SVG desde el disco |

También puedes **arrastrar imágenes** directamente desde tu computadora al canvas, o **copiar y pegar** desde el portapapeles.

---

## Mini-práctica

### Ejercicio 1: Navegar el Canvas

1. Abre Pencil con un archivo `.pen` nuevo
2. Practica pan con Space + Arrastrar — recorre el canvas en las 4 direcciones
3. Haz zoom in y out con `Cmd/Ctrl` + Scroll
4. Presiona `0` para zoom 100%
5. Presiona `1` para zoom to fit
6. Presiona `2` (aún no hay selección, pero familiarízate con el atajo)

### Ejercicio 2: Crear Frames de Distintos Dispositivos

Crea 3 frames que representen dispositivos comunes:

1. Presiona `A`, arrastra y crea un frame
2. En el Properties Panel, ajusta a **390×844** (iPhone 14)
3. Presiona `A` de nuevo y crea otro frame de **1440×900** (Desktop)
4. Presiona `A` y crea un tercero de **768×1024** (Tablet)
5. En el Layers Panel, renombra cada frame: "iPhone", "Desktop", "Tablet"

### Ejercicio 3: Dibujar Formas

Dentro del frame "iPhone":

1. Presiona `R` y dibuja un rectángulo — suelta en cualquier tamaño
2. Presiona `O`, mantén `Shift` y dibuja un círculo perfecto
3. Presiona `T` y haz clic dentro del frame — escribe "Hola Pencil"
4. Presiona `N` y haz clic cerca — escribe "Este es un diseño mobile"

### Ejercicio 4: Mover y Redimensionar

1. Presiona `V` (Move tool)
2. Selecciona el círculo que dibujaste
3. Arrástralo a otra posición
4. Tira de las esquinas para hacerlo más grande o más pequeño
5. Mantén `Shift` mientras redimensionas para mantener proporción

### Ejercicio 5: Shortcuts de Zoom

1. Crea un elemento pequeño (un rectángulo de 50×50)
2. Selecciónalo y presiona `2` — zoom directo a la selección
3. Presiona `1` — vuelve a ver todo el canvas
4. Presiona `0` — zoom al 100%

---

## Checklist

- [ ] Navego el canvas con Space+Drag
- [ ] Uso zoom con `Cmd/Ctrl` + Scroll
- [ ] Conozco los shortcuts `0`, `1`, `2`
- [ ] Creo frames con `A` y ajusto tamaño exacto
- [ ] Dibujo rectángulos con `R` (y `Shift` para cuadrados)
- [ ] Dibujo círculos con `O` (y `Shift` para círculos perfectos)
- [ ] Inserto texto con `T`
- [ ] Creo sticky notes con `N`
- [ ] Distingo azul (normal), magenta (origen componente), violeta (instancia)
- [ ] Importo imágenes arrastrando o desde toolbar

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

> 📖 **Siguiente:** [Layers Panel](./02-layers-panel.md)
