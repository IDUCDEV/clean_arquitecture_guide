# Práctica 3: Sistema de Diseño — Componente Tarjeta de Producto

> Crea un componente reutilizable, añádele slots, conviértelo en Design Library y úsalo en múltiples pantallas. Aquí dominarás componentes, slots, librerías y assets.

---

## Instrucciones

1. Abre Pencil
2. Crea un archivo nuevo: `product-card.pen`
3. Sigue cada paso en orden

**Tiempo estimado:** 40-50 minutos

---

## Enunciado

Diseña un **sistema de tarjetas de producto** que puedas reutilizar en todo un e-commerce:

1. Una **Tarjeta de Producto** componente con slots para imagen intercambiable
2. Una **Design Library** (`.lib.pen`) que contenga el componente
3. Un archivo de **catálogo** que importe la librería y use el componente con diferentes productos
4. Exportar a PDF

---

## Paso a Paso

### ✏️ Paso 1: Crear Variables del E-commerce

Antes de diseñar, define las variables de tu tienda.

1. Abre el **Variables Panel**
2. Crea:

| Nombre | Valor |
|---|---|
| `color-primary` | `#F97316` (naranja) |
| `color-primary-light` | `#FFF7ED` |
| `color-accent` | `#10B981` |
| `color-text` | `#1F2937` |
| `color-text-secondary` | `#6B7280` |
| `color-white` | `#FFFFFF` |
| `spacing-xs` | `4px` |
| `spacing-sm` | `8px` |
| `spacing-md` | `12px` |
| `spacing-lg` | `16px` |
| `radius-sm` | `4px` |
| `radius-md` | `8px` |
| `radius-lg` | `12px` |

### ✏️ Paso 2: Crear el Frame del Catálogo

1. Presiona `A`
2. Frame de **1200×800**
3. Renómbralo: `Catalogo Productos`

### ✏️ Paso 3: Diseñar la Tarjeta de Producto

Este es el paso más importante. Diseñarás el componente Tarjeta de Producto completo.

#### 3a: Fondo de la tarjeta

1. Presiona `R`
2. Rectángulo de **240×360**
3. **Fill:** `$color-white`
4. **Corner Radius:** `$radius-lg`
5. **Effects:** + Shadow (suave, preset "Card")
6. Renómbralo: `Card Bg`

#### 3b: Área de imagen

1. Presiona `R`
2. Rectángulo de **240×180**
3. X: `0` (dentro de la card), Y: `0`
4. **Corner Radius:** Top-left y Top-right = `12px`, Bottom = `0`
   - En Properties Panel → Corner Radius, desvincula los 4 radios (icono 🔗)
   - Ajusta TL `12`, TR `12`, BR `0`, BL `0`
5. **Fill:** `#F3F4F6` (gris claro como placeholder de imagen)
6. Renómbralo: `Imagen Placeholder`

#### 3c: Nombre del producto

1. Presiona `T`
2. Escribe "Nombre del Producto"
3. **Size:** `14px`, **Weight:** Semibold, **Color:** `$color-text`
4. Posición: X `12`, Y `196`
5. Renómbralo: `Titulo Producto`

#### 3d: Precio

1. Presiona `T`
2. Escribe "$99.99"
3. **Size:** `20px`, **Weight:** Bold, **Color:** `$color-primary`
4. Posición: X `12`, Y `~220`
5. Renómbralo: `Precio`

#### 3e: Rating (estrellas)

1. Presiona `T`
2. Escribe "★★★★★" (5 estrellas unicode)
3. **Size:** `14px`, **Color:** `#FBBF24` (amarillo)
4. Posición: X `12`, Y `~250`

Opcional: crea 5 estrellas individuales para más detalle.

#### 3f: Botón "Agregar al carrito"

1. Presiona `R`
2. Rectángulo de **216×36**
3. X `12`, Y `~310`
4. **Fill:** `$color-primary`
5. **Corner Radius:** `$radius-md`
6. Presiona `T`, escribe "Agregar al carrito"
7. **Size:** `13px`, **Weight:** Semibold, **Color:** `#FFFFFF`
8. Centra en el botón
9. Agrupa botón + texto: `Btn Comprar`

### ✏️ Paso 4: Agrupar y Verificar la Tarjeta

1. Selecciona todos los elementos de la tarjeta (arrastra o `Shift + clic`)
2. Presiona `Cmd/Ctrl + G` para agruparlos
3. Renombra el grupo: `Product Card Template`

Tu tarjeta debería verse así:

```
Product Card Template
├── Card Bg (240×360, sombra)
├── Imagen Placeholder (240×180)
├── Titulo Producto
├── Precio
├── Rating (estrellas)
└── Btn Comprar
    ├── Botón Rect
    └── Texto "Agregar al carrito"
```

### ✏️ Paso 5: Convertir a Componente

1. Selecciona el grupo `Product Card Template`
2. Presiona `Cmd/Ctrl + Option/Alt + K`
3. El grupo se convierte en componente
4. Nota que el borde ahora es **magenta** → indica que este es el **origen**

### ✏️ Paso 6: Crear un Slot para la Imagen

Queremos que la imagen del producto sea intercambiable. Para eso creamos un slot.

1. Dentro del componente, selecciona el elemento `Imagen Placeholder`
2. En el **Properties Panel**, en la parte superior, haz clic en **"Make a slot"**
3. El área de imagen se marca con líneas diagonales
4. Renombra el slot: `Slot Imagen`

**Probar el slot:**

1. Crea una instancia del componente: selecciona el origen y presiona `Cmd/Ctrl + D`
2. Arrastra la instancia a un lado — notarás que el borde es **violeta**
3. Arrastra un rectángulo de imagen dentro del área del slot (las líneas diagonales)
4. El rectángulo se coloca automáticamente en el slot

### ✏️ Paso 7: Crear Variantes del Componente

Un componente puede tener múltiples instancias con diferentes configuraciones.

#### 7a: Producto con descuento

1. Duplica el componente origen
2. Cambia el precio: escribe "$49.99"
3. Añade un texto "30% OFF" como badge:
   - Rectángulo pequeño: **56×24**
   - **Fill:** rojo `#EF4444`
   - **Corner Radius:** `12px`
   - Texto: "30% OFF", **Size:** `11px`, **Weight:** Bold, **Color:** `#FFFFFF`
   - Posición: sobre la imagen, X `8`, Y `8`

#### 7b: Producto sin stock

1. Duplica el componente origen
2. Cambia el botón:
   - **Fill:** `#D1D5DB` (gris)
   - Texto: "Sin stock"
   - **Color:** `#6B7280`

### ✏️ Paso 8: Crear Instancias (Catálogo de Productos)

Ahora vas a crear un catálogo con 6 productos usando el componente.

1. Selecciona el **componente origen** y presiona `Cmd/Ctrl + D` para crear instancias
2. Crea **6 instancias** en total
3. Colócalas en el frame `Catalogo Productos`

**Distribuir con flex layout:**

1. Selecciona todas las instancias
2. Presiona `Cmd/Ctrl + Option/Alt + G`
3. **Direction:** Row, **Wrap:** Wrap, **Gap:** `$spacing-lg`
4. Las tarjetas se distribuirán automáticamente

**Personalizar cada instancia:**

En cada slot de imagen, arrastra un rectángulo de color diferente para simular productos distintos:

| Instancia | Título | Precio | Color Imagen |
|---|---|---|---|
| Producto 1 | "Auriculares Bluetooth" | $89.99 | `#3B82F6` (azul) |
| Producto 2 | "Teclado Mecánico" | $129.99 | `#10B981` (verde) |
| Producto 3 | "Mouse Inalámbrico" | $49.99 | `#F59E0B` (amarillo) |
| Producto 4 | "Monitor 4K" | $399.99 | `#8B5CF6` (púrpura) |
| Producto 5 | "Webcam HD" | $69.99 | `#EC4899` (rosa) |
| Producto 6 | "Base para Laptop" | $39.99 | `#6B7280` (gris) |

**Editar el texto de cada instancia:**
- Selecciona el texto `Titulo Producto` dentro de cada instancia y cámbialo por el nombre real

### ✏️ Paso 9: Convertir a Design Library

Ahora vas a convertir este archivo en una biblioteca reutilizable.

1. En el **Layers Panel**, haz clic en el icono **"Libraries"** (junto a Layers)
2. En la parte inferior, haz clic en **"Turn this file into a library"**
3. El archivo se convierte a `product-card.lib.pen`

> **Importante:** Una vez que marcas un archivo como biblioteca, no se puede deshacer. El sufijo `.lib.pen` indica que es una biblioteca.

### ✏️ Paso 10: Usar la Library en Otro Archivo

1. Crea un nuevo archivo: `tienda.pen`
2. Abre el **Layers Panel** → icono **"Libraries"**
3. Selecciona `product-card.lib.pen` de la lista
4. Ahora haz clic en el icono **"Assets"**
5. Verás el componente `Product Card Template` en la cuadrícula
6. Arrástralo al canvas — se crea una instancia

### ✏️ Paso 11: Modificar el Origen y Ver los Cambios

Vuelve a `product-card.lib.pen` y modifica el componente origen:

1. Cambia el color del botón de naranja a púrpura: `#8B5CF6`
2. Guarda (`Cmd/Ctrl + S`)
3. Vuelve a `tienda.pen`
4. Observa que todas las instancias se actualizaron automáticamente

Este es el poder de los componentes: **cambias una vez, se actualiza en todos lados.**

### ✏️ Paso 12: Exportar a PDF

1. Selecciona el frame `Catalogo Productos`
2. Properties Panel → Export
3. Formato: **PDF**
4. Haz clic en "Export layer"
5. Guarda como `catalogo-productos.pdf`

También puedes exportar a **código Flutter**:
1. Presiona `Cmd/Ctrl + K` (opcional, solo si quieres probar la generación)
2. Pide: "Generate Flutter code for this product card"
3. Recibirás un widget StatelessWidget

---

## Diagrama de Flujo Completo

```
┌─────────────────────────────────────────────────────────┐
│                DESIGN SYSTEM WORKFLOW                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Crear variables → $color-primary, $spacing-md       │
│                                                         │
│  2. Diseñar la tarjeta (rect, text, button)             │
│                                                         │
│  3. Agrupar: Cmd+G                                      │
│                                                         │
│  4. Convertir a Componente: Cmd+Option+K                │
│     → Borde MAGENTA (origen)                            │
│                                                         │
│  5. Crear Slot para imagen (Make a slot)                │
│     → Área marcada con diagonales                       │
│                                                         │
│  6. Convertir archivo a Design Library (.lib.pen)       │
│                                                         │
│  7. En otro archivo: Importar Library → Assets          │
│                                                         │
│  8. Arrastrar componente al canvas                      │
│     → Borde VIOLETA (instancia)                         │
│                                                         │
│  9. Cambiar contenido del slot                          │
│                                                         │
│  10. Modificar origen → todas las instancias cambian    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Desafíos Extra

- [ ] Crea un **componente anidado**: dentro del slot de imagen, pon otro componente (ej: "Badge de descuento")
- [ ] Añade un **segundo slot** para acciones personalizadas (ej: botón de "Ver detalle")
- [ ] Define **suggested slot components**: marca el badge como sugerido para el slot de imagen
- [ ] Crea una **tercera pantalla** que importe la librería y muestre los productos en una cuadrícula 3×3
- [ ] Exporta el catálogo como **WebP** (formato más liviano que PNG)
- [ ] Importa un archivo **Figma** existente y conviértelo en Design Library

---

## Lo que has practicado

| Herramienta/Panel | Lo usaste en |
|---|---|
| Variables Panel | Paso 1 |
| Componentes (`Cmd+Option+K`) | Paso 5 — origen (magenta) |
| Slots (Make a slot) | Paso 6 |
| Instancias (`Cmd+D`) | Pasos 6, 8 — instancia (violeta) |
| Badge de descuento | Paso 7 — variantes |
| Flex layout con wrap | Paso 8 |
| Design Library (`.lib.pen`) | Paso 9 |
| Importar Library | Paso 10 |
| Assets Panel | Paso 10 |
| Component anidado | Desafío extra |
| Export a PDF | Paso 12 |

---

## Conclusión

Con estas tres prácticas has cubierto **todos los paneles y herramientas** de Pencil:

| Práctica | Toolbar | Layers | Properties | Variables | Icons | Components | Slots | Libraries | Export |
|---|---|---|---|---|---|---|---|---|---|
| **1. Login** | ✅ | ✅ | ✅ básico | — | — | — | — | — | ✅ PNG |
| **2. Dashboard** | ✅ | ✅ | ✅ completo | ✅ | ✅ | — | — | — | ✅ PNG |
| **3. Design System** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ PDF |

Ya puedes diseñar cualquier interfaz en Pencil sin depender de IA — solo con tu criterio visual, el mouse y los paneles.

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

**Referencia:** [Componentes y Slots](./05-componentes-slots.md)
