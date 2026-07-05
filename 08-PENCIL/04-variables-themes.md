# Variables y Themes

> Aprende a usar design tokens en Pencil: define colores, spacing, tipografía y radios como variables reutilizables. Crea themes (light, dark, contraste) y sincroniza con tu código Flutter.

---

## Índice

- [¿Qué son las Variables?](#qué-son-las-variables)
- [Crear Variables Manualmente](#crear-variables-manualmente)
- [Aplicar Variables a Elementos](#aplicar-variables-a-elementos)
- [Themes (Temas)](#themes-temas)
- [Importar Variables desde CSS](#importar-variables-desde-css)
- [Sincronizar con Código Flutter](#sincronizar-con-código-flutter)
- [Mini-práctica](#mini-práctica)

---

## ¿Qué son las Variables?

Las variables en Pencil son **design tokens**: valores reutilizables que puedes aplicar a cualquier propiedad (color, spacing, font, border radius).

**Analogía:** Funcionan como las variables en CSS (`--color-primary: #3B82F6`) o los tokens en Tailwind (`primary-500`).

### Beneficios

- **Consistencia:** Un solo valor para todo el diseño
- **Mantenibilidad:** Cambias una vez, se actualiza en todos lados
- **Theming:** Un mismo diseño puede tener múltiples temas (light, dark)
- **Sync con código:** Las variables pueden exportarse a CSS o importarse desde código

---

## Crear Variables Manualmente

### Abrir el Variables Panel

Haz clic en el **icono de variables** en la toolbar (sección superior).

### Añadir una Variable

El panel de variables tiene una estructura de tabla:

```
Variables
┌──────────────────────┬──────────┐
│ Name                 │ Value    │
├──────────────────────┼──────────┤
│ color-primary        │ #3B82F6  │
│ color-secondary      │ #10B981  │
│ spacing-md           │ 16px     │
│ font-heading         │ Inter    │
│ radius-md            │ 8px      │
└──────────────────────┴──────────┘
```

1. Haz clic en **+** para añadir una nueva fila
2. Escribe el **nombre** (sin espacios, usa guiones: `color-primary`)
3. Escribe el **valor** según el tipo:
   - Color: `#HEX`, `rgb(r,g,b)`, `rgba(r,g,b,a)`
   - Número: `8px`, `16px`, `24px`
   - String: nombre de fuente, cualquier texto

### Tipos de Variables

| Tipo | Ejemplo de valor | Para qué se usa |
|---|---|---|
| **Color** | `#3B82F6`, `rgba(0,0,0,0.1)` | Colores de UI, texto, bordes, fondos |
| **Number** | `16px`, `8px`, `24px` | Spacing, border radius, gap, padding |
| **String** | `Inter`, `SF Pro` | Nombres de fuentes, etiquetas |

### Convención de Nombres

```
color-{rol}           → color-primary, color-error, color-text
spacing-{tamaño}      → spacing-xs, spacing-sm, spacing-md, spacing-lg
radius-{tamaño}       → radius-sm, radius-md, radius-lg, radius-full
font-{rol}            → font-heading, font-body, font-mono
```

---

## Aplicar Variables a Elementos

Una vez que tienes variables definidas, aplicarlas es simple:

1. Selecciona un elemento
2. En el Properties Panel, busca la propiedad que quieras cambiar (Fill, Stroke, Gap, etc.)
3. En lugar de escribir un valor fijo, escribe `$nombre-de-la-variable`

**Ejemplos:**
- `$color-primary` → asigna el color primario
- `$spacing-md` → asigna 16px de spacing
- `$radius-md` → asigna 8px de border radius
- `$font-heading` → asigna la fuente de headings

### Auto-completado

Cuando empiezas a escribir `$`, Pencil te muestra un dropdown con las variables disponibles. Puedes navegar con las flechas y seleccionar con Enter.

### Propagación

Cuando cambias el valor de una variable en el Variables Panel:
1. Todos los elementos que usan esa variable se actualizan **automáticamente**
2. No importa si son 5 o 500 elementos — el cambio se propaga al instante
3. No necesitas guardar ni recargar

---

## Themes (Temas)

Los themes permiten que un mismo conjunto de variables tenga **diferentes valores** según el contexto.

### Concepto

```
Variables con Themes
┌──────────────────────┬──────────┬──────────┬──────────────┐
│ Name                 │ Light    │ Dark     │ High Contrast│
├──────────────────────┼──────────┼──────────┼──────────────┤
│ color-primary        │ #3B82F6  │ #60A5FA  │ #1D4ED8      │
│ color-background     │ #FFFFFF  │ #1F2937  │ #000000      │
│ color-text           │ #1F2937  │ #F9FAFB  │ #FFFFFF      │
│ spacing-md           │ 16px     │ 16px     │ 20px         │
└──────────────────────┴──────────┴──────────┴──────────────┘
```

### Crear una Columna de Tema

1. Abre el Variables Panel
2. Haz clic en **+ Theme** o **+ Column**
3. Nombra la nueva columna (ej: "Dark")
4. Para cada variable, asigna el valor que debe tener en ese tema

### Cambiar entre Temas

- En el Properties Panel, hay un selector de tema en la parte superior
- Cambia de "Light" a "Dark" y observa cómo todos los elementos se actualizan
- Los elementos que usan variables cambian de color automáticamente

### Qué Variables Deberían Cambiar por Tema

| Variable | Light | Dark |
|---|---|---|
| `color-background` | #FFFFFF | #1F2937 |
| `color-text` | #1F2937 | #F9FAFB |
| `color-text-secondary` | #6B7280 | #9CA3AF |
| `color-border` | #E5E7EB | #374151 |
| `color-primary` | #3B82F6 | #60A5FA |

**Qué NO debería cambiar:**
- `spacing-*` (el espaciado es el mismo en ambos temas)
- `radius-*` (el border radius es estructural, no visual)
- `font-*` (la tipografía es la misma)

---

## Importar Variables desde CSS

Pencil puede crear variables automáticamente a partir de un archivo CSS.

### Desde CSS

1. Abre el AI chat (`Cmd/Ctrl + K`)
2. Pega el contenido de tu `globals.css` o `theme.css`
3. Pide: "Create variables from this CSS"
4. Pencil extrae automáticamente colores, spacing y fonts como variables

### Desde Figma

1. Toma un screenshot de la tabla de variables de Figma
2. Pégalo en el chat de Pencil
3. Pide: "Create these variables in Pencil"
4. Pencil reconoce los valores y los crea

---

## Sincronizar con Código Flutter

Las variables de Pencil pueden sincronizarse con tu código.

### Exportar a Flutter

1. Define todas tus variables de diseño en Pencil
2. Pide al chat: "Export these variables as Flutter ThemeData"
3. Obtienes un `ThemeData` de Flutter con tus colores, textos y spacing

### Mantener Sincronizado

Flujo recomendado:

1. Define variables en Pencil (diseño primero)
2. Exporta a código Flutter
3. Si cambian los requisitos, cambia en Pencil y re-exporta
4. Los cambios se reflejan sin tener que buscar y reemplazar en código

---

## Mini-práctica

### Ejercicio 1: Definir Variables Base

1. Abre Pencil con un archivo nuevo
2. Abre el Variables Panel (icono en toolbar)
3. Crea estas variables:

| Nombre | Valor |
|---|---|
| `color-primary` | `#3B82F6` |
| `color-primary-light` | `#EFF6FF` |
| `color-text` | `#1F2937` |
| `color-text-secondary` | `#6B7280` |
| `color-bg` | `#F9FAFB` |
| `color-white` | `#FFFFFF` |
| `spacing-sm` | `8px` |
| `spacing-md` | `16px` |
| `spacing-lg` | `24px` |
| `radius-md` | `8px` |
| `radius-lg` | `12px` |

### Ejercicio 2: Aplicar Variables

1. Presiona `A`, crea un frame de 400×500
2. Asigna su Fill como `$color-bg`
3. Presiona `R`, dibuja un rectángulo de 360×100 dentro
4. Asigna su Fill como `$color-white`, Radius como `$radius-lg`
5. Presiona `T`, escribe "Título de ejemplo"
6. Asigna su Color como `$color-text`
7. Presiona `T`, escribe "Descripción del ejemplo"
8. Asigna su Color como `$color-text-secondary`
9. Presiona `R`, dibuja un botón de 120×44
10. Asigna su Fill como `$color-primary`, Radius como `$radius-md`

### Ejercicio 3: Probar Propagación

1. Vuelve al Variables Panel
2. Cambia `color-primary` de `#3B82F6` a `#8B5CF6` (púrpura)
3. Observa que el botón cambia de color automáticamente
4. Cambia `radius-md` de `8px` a `16px`
5. Observa que el botón cambia de radio automáticamente
6. Vuelve a los valores originales

### Ejercicio 4: Crear un Tema Dark

1. En el Variables Panel, añade una nueva columna de tema llamada "Dark"
2. Asigna estos valores para Dark:

| Variable | Light | Dark |
|---|---|---|
| `color-primary` | #3B82F6 | #60A5FA |
| `color-primary-light` | #EFF6FF | #1E3A5F |
| `color-text` | #1F2937 | #F9FAFB |
| `color-text-secondary` | #6B7280 | #9CA3AF |
| `color-bg` | #F9FAFB | #111827 |
| `color-white` | #FFFFFF | #1F2937 |

3. En el Properties Panel, cambia el selector de tema de "Light" a "Dark"
4. Observa cómo todos los elementos cambian de color instantáneamente
5. Vuelve a "Light"

### Ejercicio 5: Exportar Variables

1. Con el chat (`Cmd/Ctrl + K`), pregunta: "Show me the current variables in this file"
2. Pide: "Generate Flutter ThemeData from these variables"
3. Copia el código generado (es un punto de partida para tu tema de Flutter)

---

## Checklist

- [ ] Defino variables de color, spacing, border radius y fuentes
- [ ] Aplico variables a elementos con `$nombre-variable`
- [ ] Uso el auto-completado de variables
- [ ] Cambio una variable y veo que se propaga a todos los elementos
- [ ] Creo columnas de temas (Light, Dark, High Contrast)
- [ ] Alterno entre temas y verifico los cambios visuales
- [ ] Diferencio qué variables cambian por tema y cuáles no
- [ ] Exporto variables a código Flutter

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

> 📖 **Siguiente:** [Componentes y Slots](./05-componentes-slots.md)
