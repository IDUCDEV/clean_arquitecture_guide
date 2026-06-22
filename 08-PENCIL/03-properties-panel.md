# Properties Panel

> El panel de propiedades es donde controlas cada aspecto visual de tus elementos. Aprenderás alignment, flex layout, fills, strokes, efectos, blend modes y más.

---

## Índice

- [Apertura y Estructura](#apertura-y-estructura)
- [Alignment](#alignment)
- [Auto Layout (Flex)](#auto-layout-flex)
- [Fill (Relleno)](#fill-relleno)
- [Stroke (Borde)](#stroke-borde)
- [Corner Radius](#corner-radius)
- [Effects (Efectos)](#effects-efectos)
- [Blend Modes](#blend-modes)
- [Opacity](#opacity)
- [Constraints](#constraints)
- [Mini-práctica](#mini-práctica)

---

## Apertura y Estructura

El Properties Panel aparece en el **lado derecho** cuando seleccionas uno o más elementos.

```
Properties
┌─────────────────────────┐
│ Alignment               │
│ [←] [↔] [↑] [↓] [⛶]   │
├─────────────────────────┤
│ Auto Layout             │
│ ○ None  ● Flex         │
│ Direction: Row │ Column │
│ Gap: 8px               │
│ Padding: 16px           │
│ Wrap: ○ ●              │
├─────────────────────────┤
│ Fill                    │
│ ■ #3B82F6              │
│ [Solid] [Gradient] [Image]│
│ + Add fill              │
├─────────────────────────┤
│ Stroke                  │
│ Border: 1px            │
│ Color: #E5E7EB          │
│ Style: Solid │ Dashed   │
│ + Add stroke            │
├─────────────────────────┤
│ Corner Radius           │
│ 8px   🔗 (all)        │
│ TL:8 TR:8 BR:8 BL:8    │
├─────────────────────────┤
│ Effects                 │
│ ● Drop Shadow           │
│   X:0 Y:2 Blur:4 Spread│
│ ○ Layer Blur            │
│   Radius: 8px           │
│ + Add effect            │
├─────────────────────────┤
│ Blend Mode              │
│ Normal ▼                │
├─────────────────────────┤
│ Opacity                 │
│ 100% ─────────●──      │
└─────────────────────────┘
```

---

## Alignment

Controla la posición y distribución de elementos.

### Sección de Alignment

Cuando seleccionas **un solo elemento**:

| Botón | Acción |
|---|---|
| ← → ↑ ↓ | Alinear a izquierda, centro, derecha, arriba, abajo dentro del padre |
| ⛶ (centrar) | Centrar horizontal y verticalmente |

Cuando seleccionas **múltiples elementos**:

| Botón | Acción |
|---|---|
| Distribuir horizontalmente | Espaciado igual entre elementos en X |
| Distribuir verticalmente | Espaciado igual entre elementos en Y |

---

## Auto Layout (Flex)

El auto layout permite que los elementos se distribuyan automáticamente. Es equivalente a **flexbox** en CSS.

### Activar Flex

1. Selecciona un frame o grupo
2. En el Properties Panel, cambia Layout de **None** a **Flex**
3. Aparecen las opciones de flex

### Propiedades de Flex

| Propiedad | Opciones | Qué hace |
|---|---|---|
| **Direction** | Row / Column | Dirección del flujo: horizontal o vertical |
| **Gap** | número (px) | Espacio entre elementos hijos |
| **Padding** | número (px) | Espacio interno entre el borde y los hijos |
| **Wrap** | On / Off | Si los hijos se envuelven a la siguiente línea |
| **Align Items** | Start / Center / End / Stretch | Alineación en el eje transversal |
| **Justify Content** | Start / Center / End / Space Between / Space Evenly | Distribución en el eje principal |

### Ejemplos de Flex

```
Direction: Row, Gap: 16px
┌──────────────────────────────────┐
│ [A]        [B]        [C]        │
│ ←── 16px ──→ ←── 16px ──→       │
└──────────────────────────────────┘

Direction: Column, Gap: 12px
┌──────────────────────────────────┐
│ [A]                              │
│ ←── 12px ──→                     │
│ [B]                              │
│ ←── 12px ──→                     │
│ [C]                              │
└──────────────────────────────────┘
```

### Atajo rápido

- `Cmd/Ctrl + Option/Alt + G` — Aplica flex layout a la selección
- Los elementos existentes se colocan automáticamente en row

---

## Fill (Relleno)

Controla el color de relleno de un elemento.

### Fill Sólido

1. Selecciona el elemento
2. En la sección **Fill**, haz clic en el cuadrado de color
3. Elige un color del selector, o escribe un HEX directamente

**Usar variables:**
En lugar de un HEX, escribe `$nombre-variable` (ej: `$color-primary`).

### Fill Gradiente

Pencil soporta 3 tipos de gradiente:

| Tipo | Cómo se ve | Para qué usarlo |
|---|---|---|
| **Linear** | De un color a otro en línea recta | Fondos degradados, barras de progreso |
| **Radial** | De un color central hacia afuera | Efectos de foco, brillos |
| **Angular** | Colores alrededor de un punto | Ruedas de color, indicadores circulares |

**Crear gradiente:**
1. En Fill, cambia de **Solid** a **Gradient**
2. Elige el tipo (Linear, Radial, Angular)
3. Haz clic en los stops de color para cambiarlos
4. Arrastra los stops para ajustar la transición
5. En linear: arrastra el handle en el canvas para cambiar dirección

### Múltiples Fills

Puedes añadir **más de un fill** al mismo elemento:
1. Haz clic en **+ Add fill**
2. Aparece una segunda capa de fill encima de la primera
3. Arrastra los fills para reordenarlos (el de arriba se superpone)
4. Usa la opacidad de cada fill y los blend modes para combinarlos

### Image Fill

1. En Fill, selecciona **Image**
2. Arrastra una imagen o selecciona del disco
3. Ajusta el **fit**: Fill, Fit, Stretch, Tile

---

## Stroke (Borde)

Controla los bordes de un elemento.

### Stroke Simple

| Propiedad | Qué hace |
|---|---|
| **Weight** (px) | Grosor del borde |
| **Color** | Color del borde |
| **Position** | Inside / Center / Outside | Posición relativa al borde del elemento |

### Estilos de Stroke

| Estilo | Cómo se ve |
|---|---|
| **Solid** | Línea continua |
| **Dashed** | Línea con guiones |
| **Dotted** | Puntos |

### Múltiples Strokes

Igual que con fills, puedes añadir **+ Add stroke** para tener múltiples bordes.

Ejemplo: un borde exterior de 2px negro + un borde interior de 1px gris.

---

## Corner Radius

Controla las esquinas redondeadas.

### Radio Uniforme

Por defecto, todas las esquinas tienen el mismo valor.

1. Selecciona el elemento
2. Ajusta el slider o escribe el valor en px

### Radios Independientes

Para redondear solo algunas esquinas:

1. Haz clic en el icono **🔗** (cadena) para desvincular
2. Aparecen 4 campos: TL (top-left), TR (top-right), BR (bottom-right), BL (bottom-left)
3. Ajusta cada uno independientemente

**Usos comunes:**

```
TL: 12, TR: 12, BR: 0, BL: 0
→ Una imagen con esquinas redondeadas arriba, planas abajo (como una card)

TL: 999, TR: 999, BR: 999, BL: 999
→ Un rectángulo completamente redondeado (pill shape)
```

---

## Effects (Efectos)

Pencil soporta dos tipos de efectos:

### Drop Shadow (Sombra)

| Propiedad | Qué controla |
|---|---|
| **X** | Desplazamiento horizontal de la sombra (negativo = izquierda) |
| **Y** | Desplazamiento vertical de la sombra (negativo = arriba) |
| **Blur** | Cuán difusa es la sombra (mayor valor = más borrosa) |
| **Spread** | Cuánto se expande la sombra (mayor valor = más grande) |
| **Color** | Color de la sombra |
| **Opacity** | Transparencia de la sombra |

**Presets comunes:**
- **Card shadow:** X:0 Y:2 Blur:8 Spread:0 Color: rgba(0,0,0,0.1)
- **Elevated shadow:** X:0 Y:8 Blur:24 Spread:0 Color: rgba(0,0,0,0.12)
- **Modal shadow:** X:0 Y:16 Blur:48 Spread:0 Color: rgba(0,0,0,0.2)

### Layer Blur (Desenfoque)

| Propiedad | Qué controla |
|---|---|
| **Radius** | Cantidad de desenfoque |

Útil para: fondos modales, efectos de profundidad, estados de carga.

### Múltiples Efectos

Puedes añadir varios efectos con **+ Add effect**. Se aplican en orden, de arriba a abajo.

Ejemplo: una sombra exterior + una sombra interior + blur.

---

## Blend Modes

Los blend modes determinan cómo se combina visualmente un elemento con los que están detrás de él.

| Modo | Efecto |
|---|---|
| **Normal** | Sin mezcla (opacidad normal) |
| **Multiply** | Oscurece: útil para sombras, texturas sobre fondos |
| **Screen** | Aclara: útil para reflejos, brillos |
| **Overlay** | Combina multiply y screen según el brillo de fondo |
| **Darken** | Muestra el color más oscuro de cada canal |
| **Lighten** | Muestra el color más claro de cada canal |
| **Color Dodge** | Aclara el fondo según el color del elemento |
| **Color Burn** | Oscurece el fondo según el color del elemento |
| **Difference** | Muestra la diferencia absoluta entre colores |

Los blend modes se usan para: efectos de iluminación, texturas superpuestas, corrección de color, máscaras.

---

## Opacity

Controla la transparencia del elemento.

- **100%** → completamente opaco
- **50%** → semi-transparente
- **0%** → invisible (pero sigue ocupando espacio en flex layout)

**Diferencia entre Fill opacity y Element opacity:**
- **Fill opacity** (en la sección Fill): solo afecta al relleno, el stroke y los hijos se mantienen opacos
- **Element opacity** (la general): afecta al elemento completo incluyendo strokes, efectos e hijos

---

## Constraints

Las constraints controlan cómo se comporta un elemento cuando su padre se redimensiona.

(Nota: esta funcionalidad puede variar según la versión de Pencil. Cuando está disponible, permite fijar distancias a los bordes del padre.)

---

## Mini-práctica

### Ejercicio 1: Crear un Layout Flex de 4 Cards

1. Presiona `A`, crea un frame de 600×400
2. Nómbralo "Card Grid"
3. Con el frame seleccionado, en Properties → Layout, cambia a **Flex**
4. **Direction:** Row, **Gap:** 16px, **Wrap:** On, **Padding:** 16px
5. Presiona `R`, dibuja un rectángulo de 130×180 dentro del frame
6. Duplícalo 3 veces (`Cmd/Ctrl + D` tres veces)
7. Las 4 cards se distribuyen automáticamente con flex layout
8. Selecciona cada card y asígnale un color de fill diferente

### Ejercicio 2: Aplicar un Gradiente

1. Presiona `R`, dibuja un rectángulo de 300×200
2. En Properties → Fill, cambia de **Solid** a **Gradient**
3. Elige **Linear**
4. Cambia el primer stop a `#3B82F6` (azul) y el segundo a `#8B5CF6` (púrpura)
5. Arrastra el handle en el canvas para cambiar la dirección del gradiente (diagonal)
6. Cambia el tipo a **Radial** — nota la diferencia

### Ejercicio 3: Múltiples Efectos de Sombra

1. Presiona `R`, dibuja un rectángulo de 200×100
2. Fill blanco, Corner Radius 12px
3. En Effects: + **Drop Shadow**
4. Configura: X:0, Y:4, Blur:12, Spread:0, Color: rgba(0,0,0,0.15)
5. Añade otro **+ Drop Shadow**
6. Configura el segundo: X:0, Y:1, Blur:3, Spread:0, Color: rgba(0,0,0,0.1)
7. Tienes una sombra doble (más realista)

### Ejercicio 4: Blend Mode

1. Presiona `R`, dibuja un rectángulo de 200×200, Fill `#3B82F6`
2. Presiona `R`, dibuja otro rectángulo de 100×100 encima, Fill blanco
3. Con el rectángulo blanco seleccionado, en Properties → **Blend Mode**, cambia a **Multiply**
4. Nota cómo el blanco se vuelve transparente y se mezcla con el azul
5. Prueba **Screen**, **Overlay**, **Difference** y observa los cambios

### Ejercicio 5: Corner Radius Independiente

1. Presiona `R`, dibuja un rectángulo de 200×100
2. En Corner Radius, haz clic en **🔗** para desvincular
3. Pon TL: 16, TR: 16, BR: 0, BL: 0
4. Deberías ver un rectángulo con bordes redondeados arriba y planos abajo
5. Ahora pon TL: 999 — el lado izquierdo se vuelve un semicírculo

---

## Checklist

- [ ] Alineo elementos con los botones de alignment
- [ ] Aplico flex layout con Row/Column, Gap y Wrap
- [ ] Cambio fills entre sólido, gradiente y image fill
- [ ] Creo gradientes lineales y radiales
- [ ] Añado múltiples fills al mismo elemento
- [ ] Configuro strokes con grosor, color y estilo dashed
- [ ] Añado múltiples strokes
- [ ] Redondeo esquinas independientes (desvinculando 🔗)
- [ ] Aplico drop shadow con X, Y, Blur, Spread
- [ ] Añado múltiples efectos al mismo elemento
- [ ] Uso blend modes (Multiply, Screen, Overlay)
- [ ] Diferencio fill opacity de element opacity

---

**Siguiente:** [Variables y Themes](./04-variables-themes.md)
