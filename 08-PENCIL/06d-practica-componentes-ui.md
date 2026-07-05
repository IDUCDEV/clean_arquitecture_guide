# Práctica 4: Biblioteca de Componentes UI Estándar

> Construye desde cero los componentes de interfaz más comunes que todo diseñador necesita: botones, inputs, cards, navegación, feedback, avatares y más. Al final tendrás tu propio sistema de componentes reutilizable.

---

## Instrucciones

1. Abre Pencil
2. Crea un archivo nuevo: `componentes-ui.pen`
3. Sigue cada bloque. Todos son independientes — puedes hacerlos en cualquier orden.

**Tiempo estimado:** 50-70 minutos

---

## Enunciado

Construye una biblioteca con los 7 grupos de componentes UI estándar:

1. Botones (6 variantes)
2. Inputs (6 variantes)
3. Cards (4 variantes)
4. Navegación (4 variantes)
5. Feedback (5 variantes)
6. Data Display (5 variantes)
7. Listas (3 variantes)

---

## Variables Base

Antes de empezar, define estas variables. Las usarás en todos los componentes del archivo.

| Nombre | Valor |
|---|---|
| `color-primary` | `#3B82F6` |
| `color-primary-dark` | `#2563EB` |
| `color-secondary` | `#8B5CF6` |
| `color-success` | `#10B981` |
| `color-warning` | `#F59E0B` |
| `color-error` | `#EF4444` |
| `color-info` | `#06B6D4` |
| `color-text` | `#1F2937` |
| `color-text-secondary` | `#6B7280` |
| `color-bg` | `#F9FAFB` |
| `color-border` | `#E5E7EB` |
| `color-white` | `#FFFFFF` |
| `spacing-xs` | `4px` |
| `spacing-sm` | `8px` |
| `spacing-md` | `12px` |
| `spacing-lg` | `16px` |
| `spacing-xl` | `24px` |
| `radius-sm` | `4px` |
| `radius-md` | `8px` |
| `radius-lg` | `12px` |
| `radius-full` | `999px` |

---

## Bloque 1: Botones

Crea un frame **600×400** llamado `Botones`. Dentro, diseña cada botón como componente.

### 1a — Botón Primario

1. Presiona `R`, dibuja un rectángulo de **160×44**
2. **Fill:** `$color-primary`, **Corner Radius:** `$radius-md`
3. Presiona `T`, escribe "Primary"
4. **Size:** `14px`, **Weight:** Semibold, **Color:** `$color-white`
5. Centra el texto en el botón
6. Agrupa y convierte a componente: `Btn Primary`
7. Crea una **copia** con **hover state**: cambia Fill a `$color-primary-dark`

### 1b — Botón Secundario

1. Rectángulo **160×44**, **Fill:** `$color-secondary`, **Radius:** `$radius-md`
2. Texto "Secondary", **Size:** `14px`, **Semibold**, **Color:** `white`
3. Componente: `Btn Secondary`

### 1c — Botón Outline

1. Rectángulo **160×44**, **Fill:** transparente, **Stroke:** `2px` `$color-primary`
2. **Corner Radius:** `$radius-md`
3. Texto "Outline", **Color:** `$color-primary`
4. Componente: `Btn Outline`

### 1d — Botón Ghost

1. Rectángulo **160×44**, **Fill:** transparente, sin stroke
2. Texto "Ghost", **Color:** `$color-primary`
3. Componente: `Btn Ghost`

### 1e — Botón con Icono

1. Rectángulo **160×44**, **Fill:** `$color-primary`, **Radius:** `$radius-md`
2. Texto "→" (flecha unicode) + texto "Button"
3. Alinea el icono a la izquierda y el texto centrado
4. Componente: `Btn With Icon`

### 1f — Botón Redondo (Icon Button)

1. Presiona `O`, mantén `Shift` para un círculo perfecto de **44×44**
2. **Fill:** `$color-primary`
3. Texto "+", **Size:** `20px`, **Weight:** Bold, **Color:** white
4. Centra el texto en el círculo
5. Componente: `Btn Icon`

**Distribuye** los 6 botones en fila con flex layout (Direction: Row, Gap: `$spacing-lg`).

---

## Bloque 2: Inputs

Crea un frame **600×500** llamado `Inputs`. Son las entradas de datos más comunes.

### 2a — Text Input

1. Rectángulo **320×44**
2. **Fill:** `$color-white`, **Stroke:** `1px` `$color-border`
3. **Corner Radius:** `$radius-md`
4. Texto "Placeholder..." dentro, **Size:** `14px`, **Color:** `$color-text-secondary`
5. Agrupa: `Input Text`

**Variante enfocada:**
1. Duplica el input
2. Cambia **Stroke** a `2px` `$color-primary`
3. El texto cambia a valor escrito, ej: "correo@ejemplo.com"
4. Agrupa: `Input Text Focused`

**Variante con error:**
1. Duplica el input
2. Cambia **Stroke** a `2px` `$color-error`
3. Añade texto de error debajo: "Este campo es obligatorio"
4. **Size:** `12px`, **Color:** `$color-error`
5. Agrupa: `Input Text Error`

### 2b — Input con Icono Izquierdo

1. Rectángulo **320×44**, **Fill:** `$color-white`, **Stroke:** `1px` `$color-border`
2. **Corner Radius:** `$radius-md`
3. Icono de búsqueda (🔍) o texto a la izquierda
4. Texto "Buscar..." a la derecha del icono
5. Agrupa: `Input With Icon`

### 2c — Select / Dropdown

1. Rectángulo **320×44**, **Fill:** `$color-white`, **Stroke:** `1px` `$color-border`
2. **Corner Radius:** `$radius-md`
3. Texto "Selecciona una opción" a la izquierda
4. Texto "▼" (triángulo) a la derecha, **Color:** `$color-text-secondary`
5. Agrupa: `Select`

### 2d — Checkbox

1. Rectángulo **20×20**, **Corner Radius:** `$radius-sm`
2. **Fill:** `$color-white`, **Stroke:** `2px` `$color-border`
3. Texto "Acepto términos y condiciones" al lado
4. Agrupa: `Checkbox`

**Variante marcada:**
1. Duplica el checkbox
2. **Fill:** `$color-primary`, **Stroke:** `$color-primary`
3. Añade texto "✓" blanco dentro
4. Agrupa: `Checkbox Checked`

### 2e — Toggle Switch

1. Rectángulo **44×24**, **Corner Radius:** `$radius-full`
2. **Fill:** `#D1D5DB` (gris inactivo)
3. Círculo dentro: **20×20**, **Fill:** `$color-white`
4. Agrupa: `Toggle Off`

**Variante activado:**
1. Duplica el toggle
2. **Fill:** `$color-primary`
3. Mueve el círculo a la derecha
4. Agrupa: `Toggle On`

### 2f — Textarea

1. Rectángulo **320×100**
2. **Fill:** `$color-white`, **Stroke:** `1px` `$color-border`
3. **Corner Radius:** `$radius-md`
4. Texto "Escribe tu mensaje..." dentro, arriba a la izquierda
5. Agrupa: `Textarea`

---

## Bloque 3: Cards

Crea un frame **700×400** llamado `Cards`. Construye 4 tipos de tarjetas.

### 3a — Card de Producto Simple

1. Rectángulo **200×280**, **Fill:** `$color-white`
2. **Corner Radius:** `$radius-lg`, **Effects:** + Shadow
3. Rectángulo superior **200×140**, **Radius:** TL/TR `12px`, BR/BL `0`
4. **Fill:** `#F3F4F6` (imagen placeholder)
5. Texto "Producto" debajo de la imagen, **Size:** `14px`, **Semibold**
6. Texto "$29.99", **Size:** `18px`, **Bold**, **Color:** `$color-primary`
7. Rating: "★★★★☆", **Size:** `12px`
8. Botón "Comprar", pequeño
9. Agrupa: `Card Producto`

### 3b — Card de Perfil

1. Rectángulo **280×160**, **Fill:** `$color-white`
2. **Corner Radius:** `$radius-lg`, **Effects:** + Shadow
3. Círculo **60×60** arriba-centro, **Fill:** `$color-primary`
4. Texto "María García", **Size:** `16px`, **Weight:** Bold
5. Texto "maria@ejemplo.com", **Size:** `13px`, **Color:** `$color-text-secondary`
6. Texto "Desarrolladora Flutter", **Size:** `13px`, **Color:** `$color-text-secondary`
7. Agrupa: `Card Perfil`

### 3c — Card de Estadística

1. Rectángulo **220×120**, **Fill:** `$color-white`
2. **Corner Radius:** `$radius-lg`, **Effects:** + Shadow
3. Icono o rectángulo decorativo a la izquierda, **Fill:** `$color-primary-light`
4. Texto "Ventas Hoy", **Size:** `13px`, **Color:** `$color-text-secondary`
5. Texto "$12,450", **Size:** `24px`, **Weight:** Bold
6. Texto "+15% vs ayer", **Size:** `12px`, **Color:** `$color-success`
7. Agrupa: `Card Estadistica`

### 3d — Card de Notificación

1. Rectángulo **320×72**, **Fill:** `$color-white`
2. **Corner Radius:** `$radius-md`, **Effects:** + Shadow
3. Círculo **40×40** a la izquierda, **Fill:** `$color-info`
4. Texto "¡Nueva actualización!", **Size:** `14px`, **Weight:** Semibold
5. Texto "Hace 5 minutos", **Size:** `12px`, **Color:** `$color-text-secondary`
6. Agrupa: `Card Notificacion`

---

## Bloque 4: Navegación

Crea un frame **700×400** llamado `Navegacion`.

### 4a — Navbar Superior

1. Rectángulo **600×56**, **Fill:** `$color-white`
2. **Effects:** + Shadow bottom (suave)
3. Logo/Texto "MiApp" a la izquierda, **Weight:** Bold, **Size:** `18px`
4. Links de navegación: "Inicio", "Productos", "Precios", "Contacto"
5. **Size:** `14px`, **Color:** `$color-text-secondary`
6. Botón "Login" a la derecha (rectángulo pequeño con outline)
7. Agrupa: `Navbar`

### 4b — Tabs

1. Rectángulo **400×36** como contenedor de tabs
2. **Fill:** `$color-bg`, **Corner Radius:** `$radius-md`
3. Crea 3 tabs dentro como rectángulos:
   - Tab activo: **120×36**, **Fill:** `$color-white`, **Radius:** `$radius-md`, **Shadow**
   - Tab inactivo 1: **120×36**, sin fill
   - Tab inactivo 2: **120×36**, sin fill
4. Texto "General", "Seguridad", "Notificaciones"
5. Componente: `Tabs`

### 4c — Bottom Navigation (Mobile)

1. Rectángulo **390×64**, **Fill:** `$color-white`
2. **Stroke top:** `1px` `$color-border`
3. Crea 4 ítems con icono + texto:
   - 🏠 Inicio (activo: color primary)
   - 🔍 Buscar (inactivo: gris)
   - 🛒 Carrito (inactivo)
   - 👤 Perfil (inactivo)
4. Usa texto emoji o rectángulos como placeholder de iconos
5. Agrupa: `Bottom Nav`

### 4d — Breadcrumbs

1. Texto "Inicio > Productos > Electrónicos > Laptops"
2. "Inicio" en `$color-primary`, el resto en `$color-text-secondary`
3. El último (Laptops) en `$color-text` (negro, activo)
4. **Size:** `13px`
5. Agrupa: `Breadcrumbs`

---

## Bloque 5: Feedback

Crea un frame **600×400** llamado `Feedback`.

### 5a — Alert

1. Rectángulo **400×56**, **Corner Radius:** `$radius-md`
2. **Fill:** `#ECFDF5` (verde claro), **Stroke:** `1px` `#A7F3D0`
3. Icono "✓" a la izquierda, **Color:** `$color-success`
4. Texto "Operación exitosa", **Size:** `14px`, **Weight:** Semibold
5. Texto "Los cambios se guardaron.", **Size:** `13px`, **Color:** `$color-text-secondary`
6. Agrupa: `Alert Success`

**Variantes (duplica y cambia colores):**
- **Error:** Fill `#FEF2F2`, Stroke `#FECACA`, icono ✗, Color `$color-error`
- **Warning:** Fill `#FFFBEB`, Stroke `#FDE68A`, icono ⚠, Color `$color-warning`
- **Info:** Fill `#ECFEFF`, Stroke `#A5F3FC`, icono ℹ, Color `$color-info`

### 5b — Badge

1. Rectángulo horizontal: alto **24px**, ancho variable
2. **Corner Radius:** `$radius-full`
3. **Fill:** `$color-primary-light`, **Stroke:** none
4. Texto "Nuevo", **Size:** `12px`, **Weight:** Semibold, **Color:** `$color-primary`
5. Agrupa: `Badge Default`

**Variantes:**
- **Success:** Fill `#D1FAE5`, texto `$color-success`
- **Error:** Fill `#FEE2E2`, texto `$color-error`
- **Warning:** Fill `#FEF3C7`, texto `$color-warning`
- **Número:** Fill `$color-error`, texto blanco (ej: "99+")

### 5c — Chip / Tag

1. Rectángulo con radius full: **variable×28**
2. **Fill:** `$color-bg`, **Stroke:** `1px` `$color-border`
3. Texto "Flutter", **Size:** `12px`
4. Texto "✕" (cerrar) a la derecha, **Size:** `12px`, **Color:** `$color-text-secondary`
5. Agrupa: `Chip`

### 5d — Toast

1. Rectángulo **300×48**, **Corner Radius:** `$radius-lg`
2. **Fill:** `#1F2937` (fondo oscuro)
3. **Effects:** + Shadow (elevada)
4. Texto "Mensaje enviado", **Size:** `14px`, **Color:** `#FFFFFF`
5. Agrupa: `Toast`

---

## Bloque 6: Data Display

Crea un frame **600×400** llamado `DataDisplay`.

### 6a — Avatar

1. Círculo **40×40**, **Fill:** `$color-primary`
2. Texto "JD" dentro, **Size:** `14px`, **Weight:** Bold, **Color:** white
3. Agrupa: `Avatar`

**Variantes:**
- **Small:** 24×24
- **Medium:** 40×40 (default)
- **Large:** 64×64
- **With image:** rectángulo en vez de texto (foto placeholder)

### 6b — Avatar Group (solapados)

1. Círculo 1: **40×40**, X `0`, **Fill:** `$color-primary`
2. Círculo 2: **40×40**, X `-12`, **Fill:** `$color-secondary`
3. Círculo 3: **40×40**, X `-24`, **Fill:** `$color-success`
4. Círculo 4: **40×40**, X `-36`, **Fill:** `$color-bg`, texto "+3"
5. Agrupa: `Avatar Group`

### 6c — Barra de Progreso

1. Rectángulo de fondo: **300×8**, **Fill:** `$color-bg`
2. **Corner Radius:** `$radius-full`
3. Rectángulo de progreso: **200×8**, **Fill:** `$color-primary`
4. **Corner Radius:** `$radius-full` (solo visible si no está al 100%)
5. Texto "66%" a la derecha, **Size:** `12px`, **Color:** `$color-text-secondary`
6. Agrupa: `Progress Bar`

### 6d — Rating Stars

1. Texto "★★★★★", **Size:** `20px`
2. Las estrellas llenas en `#FBBF24` (amarillo), las vacías en `#D1D5DB` (gris)
3. Para simularlo, usa 3 textos separados:
   - "★★★" amarillo
   - "★★" gris
4. Texto "(128 reseñas)" al lado, **Size:** `12px`, **Color:** `$color-text-secondary`
5. Agrupa: `Rating`

### 6e — Skeleton Loader (placeholder de carga)

1. Rectángulo **300×16**, **Corner Radius:** `$radius-full`, **Fill:** `$color-bg`
2. Rectángulo **240×16**, **Corner Radius:** `$radius-full`, **Fill:** `$color-bg`
3. Rectángulo **160×16**, **Corner Radius:** `$radius-full`, **Fill:** `$color-bg`
4. Rectángulo **300×120**, **Corner Radius:** `$radius-md`, **Fill:** `$color-bg`
5. Agrupa: `Skeleton`

---

## Bloque 7: Listas

Crea un frame **500×400** llamado `Listas`.

### 7a — Lista Simple

1. Frame contenedor: **320×200**, **Fill:** `$color-white`
2. **Corner Radius:** `$radius-lg`, **Effects:** + Shadow
3. Crea 4 filas, cada una:
   - Rectángulo **320×44**
   - **Stroke bottom:** `1px` `$color-border` (excepto la última)
   - Texto "Elemento 1", etc., **Size:** `14px`
4. Agrupa: `List Simple`

### 7b — Lista con Avatar

1. Frame contenedor: **360×240**, **Fill:** `$color-white`
2. **Corner Radius:** `$radius-lg`, **Effects:** + Shadow
3. Crea 3 filas, cada una:
   - Rectángulo **360×64**
   - Círculo **40×40** a la izquierda, diferente color por fila
   - Texto "Nombre" (bold) + "Descripción" (secondary) a la derecha
   - Flecha "›" a la derecha
4. Agrupa: `List Avatar`

### 7c — Lista con Acciones

1. Frame contenedor: **360×200**, **Fill:** `$color-white`
2. **Corner Radius:** `$radius-lg`, **Effects:** + Shadow
3. Crea 3 filas con:
   - Texto principal a la izquierda
   - Botón pequeño o toggle a la derecha
   - Ej: "Notificaciones" + Toggle, "Modo oscuro" + Toggle
4. Agrupa: `List Actions`

---

## Organización Final en Layers Panel

```
Pages
└── Page 1
    ├── Botones (frame 600×400)
    │   ├── Btn Primary [component]
    │   ├── Btn Secondary [component]
    │   ├── Btn Outline [component]
    │   ├── Btn Ghost [component]
    │   ├── Btn With Icon [component]
    │   └── Btn Icon [component]
    ├── Inputs (frame 600×500)
    │   ├── Input Text [component]
    │   ├── Input Text Focused
    │   ├── Input Text Error
    │   ├── Input With Icon [component]
    │   ├── Select [component]
    │   ├── Checkbox [component]
    │   ├── Checkbox Checked
    │   ├── Toggle Off [component]
    │   ├── Toggle On
    │   └── Textarea [component]
    ├── Cards (frame 700×400)
    │   ├── Card Producto [component]
    │   ├── Card Perfil [component]
    │   ├── Card Estadistica [component]
    │   └── Card Notificacion [component]
    ├── Navegacion (frame 700×400)
    │   ├── Navbar [component]
    │   ├── Tabs [component]
    │   ├── Bottom Nav [component]
    │   └── Breadcrumbs [component]
    ├── Feedback (frame 600×400)
    │   ├── Alert Success [component]
    │   ├── Alert Error
    │   ├── Alert Warning
    │   ├── Alert Info
    │   ├── Badge Default [component]
    │   ├── Badge Success
    │   ├── Badge Error
    │   ├── Badge Number
    │   ├── Chip [component]
    │   └── Toast [component]
    ├── DataDisplay (frame 600×400)
    │   ├── Avatar [component]
    │   ├── Avatar Group [component]
    │   ├── Progress Bar [component]
    │   ├── Rating [component]
    │   └── Skeleton [component]
    └── Listas (frame 500×400)
        ├── List Simple [component]
        ├── List Avatar [component]
        └── List Actions [component]
```

---

## Convertir a Design Library

Cuando termines todos los componentes:

1. En el Layers Panel, haz clic en **Libraries**
2. Haz clic en **"Turn this file into a library"**
3. El archivo se convierte a `componentes-ui.lib.pen`

Ahora puedes importar esta biblioteca en cualquier otro diseño y arrastrar los componentes desde **Assets**.

---

## Desafíos Extra

- [ ] Convierte **todos** los componentes a componentes (origen magenta), no solo los indicados
- [ ] Añade **slots** a la Card de Producto (slot para imagen intercambiable)
- [ ] Crea un **formulario completo** combinando inputs + botón
- [ ] Diseña un **Modal/Dialog** con overlay (fondo semi-transparente + card centrada)
- [ ] Crea un **stepper** (paso 1 → paso 2 → paso 3)
- [ ] Añade un **Tooltip** (rectángulo pequeño con flecha hacia abajo)
- [ ] Diseña un **Pagination** (‹ 1 2 3 ... 10 ›)
- [ ] Crea una **Dropdown Menu** (lista que aparece al hacer clic)

---

## Lo que has practicado

| Grupo | Componentes | Paneles nuevos |
|---|---|---|
| Botones | 6 variantes | Fill, Radius, Stroke, Componentes |
| Inputs | 8 variantes | Estados (focus, error, checked) |
| Cards | 4 variantes | Shadow, Layout compuesto |
| Navegación | 4 variantes | Flex Row, organización |
| Feedback | 9 variantes | Colores semánticos, Pill shape |
| Data Display | 5 variantes | Tamaños, superposición |
| Listas | 3 variantes | Jerarquía, acciones |

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

**Anterior:** [Práctica 3: Sistema de Diseño](./06c-practica-design-system.md)  
**Referencia:** [Canvas y Toolbar](./01-canvas-toolbar.md)
