# Práctica 2: Dashboard de Ventas

> Diseña un dashboard analítico con sidebar, cards de métricas, tabla de datos y variables de diseño. Dominarás Layers Panel, Variables, iconos y flex layout.

---

## Instrucciones

1. Abre Pencil
2. Crea un archivo nuevo: `dashboard.pen`
3. Sigue cada paso en orden
4. No uses IA — todo se hace con mouse y teclado

**Tiempo estimado:** 40-50 minutos

---

## Enunciado

Diseña un dashboard de ventas para una tienda online con:

- Sidebar de navegación (con iconos)
- Header (avatar, nombre, búsqueda)
- 4 cards de métricas (Ventas hoy, Usuarios nuevos, Pedidos, Ingresos)
- Tabla de últimas transacciones

---

## Paso a Paso

### ✏️ Paso 1: Crear Variables de Diseño

Antes de dibujar, define las variables que usarás en todo el dashboard.

1. Abre el **Variables Panel** (icono en la toolbar)
2. Crea las siguientes variables:

| Nombre | Light | Dark (opcional) |
|---|---|---|
| `color-primary` | `#3B82F6` | `#60A5FA` |
| `color-primary-light` | `#EFF6FF` | `#1E3A5F` |
| `color-success` | `#10B981` | `#34D399` |
| `color-warning` | `#F59E0B` | `#FBBF24` |
| `color-text` | `#1F2937` | `#F9FAFB` |
| `color-text-secondary` | `#6B7280` | `#9CA3AF` |
| `color-bg` | `#F3F4F6` | `#111827` |
| `color-white` | `#FFFFFF` | `#1F2937` |
| `spacing-xs` | `4px` | `4px` |
| `spacing-sm` | `8px` | `8px` |
| `spacing-md` | `16px` | `16px` |
| `spacing-lg` | `24px` | `24px` |
| `radius-sm` | `4px` | `4px` |
| `radius-md` | `8px` | `8px` |
| `radius-lg` | `12px` | `12px` |

Ahora, cada vez que asignes un color en el Properties Panel, escribe `$color-primary` en lugar del código HEX. Pencil lo reemplazará automáticamente por el valor de la variable.

### ✏️ Paso 2: Crear el Frame Principal

1. Presiona `A` (Frame tool)
2. Arrastra para crear un frame de **1440×900** (escritorio)
3. Renómbralo: `Dashboard` en el Layers Panel

### ✏️ Paso 3: Sidebar

1. Presiona `R`
2. Dibuja un rectángulo:
   - Width: `240`, Height: `900`
   - X: `0`, Y: `0`
   - **Fill:** `$color-white`
   - **Stroke:** right border `1px`, `$color-bg`
3. Renómbralo: `Sidebar` en Layers Panel

#### Logo en Sidebar

1. Presiona `R`
2. Dibuja un rectángulo de **40×40**, X `20`, Y `24`
3. **Fill:** `$color-primary`, **Corner Radius:** `8px`
4. Presiona `T`, escribe "D"
5. **Size:** `20px`, **Weight:** Bold, **Color:** `#FFFFFF`
6. Centra sobre el rectángulo azul

#### Ítems de Navegación

Crea 5 ítems. Cada uno es: un icono + texto.

**Primero, añade iconos desde la biblioteca incorporada:**

1. Desde la **Toolbar**, haz clic en el chevron bajo Rectangle
2. No necesitas importar — Pencil trae Material Symbols y Lucide por defecto
3. Para insertar un icono, puedes pegar un SVG o usar el que viene en la biblioteca
4. Alternativa: dibuja un rectángulo de **24×24** como placeholder del icono

**Primer ítem (Dashboard — activo):**
1. Presiona `R`, dibuja un rectángulo de **200×40**
2. X `20`, Y `~100`
3. **Fill:** `$color-primary-light`
4. **Corner Radius:** `8px`
5. Presiona `T`, escribe "Dashboard"
6. **Size:** `14px`, **Weight:** Semibold, **Color:** `$color-primary`
7. Agrupa como `Nav Dashboard`

**Segundo ítem (Productos):**
1. Duplica el grupo anterior (`Cmd/Ctrl + D`)
2. Muévelo abajo: Y `~150`
3. Cambia el texto a "Productos"
4. Cambia **Fill** del fondo a transparente (`No fill`)
5. Cambia **Color** del texto a `$color-text-secondary`

**Tercer ítem (Pedidos):**
1. Duplica y coloca Y `~200`
2. Texto: "Pedidos"

**Cuarto ítem (Usuarios):**
1. Duplica y coloca Y `~250`
2. Texto: "Usuarios"

**Quinto ítem (Configuración):**
1. Duplica y coloca Y `~300`
2. Texto: "Configuración"

**Organiza en Layers Panel:**
```
Sidebar
├── Sidebar Bg
├── Logo
│   ├── Logo Rect
│   └── Logo Text
├── Nav Dashboard (activo)
├── Nav Productos
├── Nav Pedidos
├── Nav Usuarios
└── Nav Configuración
```

### ✏️ Paso 4: Layout del Contenido

El área de contenido principal empieza en X `240` (después del sidebar).

#### Header

1. Presiona `R`
2. Width: `1200`, Height: `64`
3. X `240`, Y `0`
4. **Fill:** `$color-white`
5. Añade un borde inferior: **Stroke bottom** `1px`, `$color-bg`

**Barra de búsqueda:**
1. Presiona `R`
2. Width: `320`, Height: `36`
3. X `280`, Y `14`
4. **Fill:** `$color-bg`, **Corner Radius:** `8px`
5. Presiona `T`, escribe "Buscar..."
6. **Size:** `13px`, **Color:** `$color-text-secondary`
7. Coloca el texto dentro

**Avatar de usuario (derecha):**
1. Presiona `O`, mantén `Shift`
2. Círculo de **36×36**
3. X `1360`, Y `14`
4. **Fill:** `$color-primary`
5. Presiona `T`, escribe "JD"
6. **Size:** `12px`, **Weight:** Bold, **Color:** `#FFFFFF`
7. Grupo con nombre del usuario al lado

#### Título de página

1. Presiona `T`, escribe "Panel de Control"
2. **Size:** `24px`, **Weight:** Bold, **Color:** `$color-text`
3. X `280`, Y `~100`

### ✏️ Paso 5: Cards de Métricas (Flex Layout)

Vas a crear 4 tarjetas usando **flex layout** para distribuirlas automáticamente.

1. Presiona `R`, dibuja un rectángulo de **1200×100**
2. X `280`, Y `~150`
3. **Fill:** transparente (esto será el contenedor flex)
4. Selecciona el rectángulo
5. Presiona `Cmd/Ctrl + Option/Alt + G` para aplicar flex layout
6. En el **Properties Panel**, configura:
   - **Direction:** Row
   - **Gap:** `$spacing-md`
   - **Padding:** `0`

**Ahora crea una tarjeta de métrica:**

1. Presiona `R`, dibuja **278×100**
2. **Fill:** `$color-white`
3. **Corner Radius:** `$radius-lg`
4. **Effects:** + Shadow (elige preset suave)
5. Presiona `T`, escribe "Ventas Hoy"
6. **Size:** `13px`, **Color:** `$color-text-secondary`
7. Presiona `T`, escribe "$12,450"
8. **Size:** `28px`, **Weight:** Bold, **Color:** `$color-text`
9. Presiona `T`, escribe "+15% vs ayer"
10. **Size:** `12px`, **Color:** `$color-success`
11. Agrupa todo: `Card Ventas`

**Duplica la tarjeta 3 veces más:**

| Card | Título | Valor | Cambio |
|---|---|---|---|
| Card Ventas | Ventas Hoy | $12,450 | +15% |
| Card Usuarios | Usuarios Nuevos | 843 | +8% |
| Card Pedidos | Pedidos | 156 | -3% (color rojo `#EF4444`) |
| Card Ingresos | Ingresos | $48,200 | +12% |

Coloca las 4 cards dentro del contenedor flex. Se alinearán automáticamente en fila con el gap que definiste.

### ✏️ Paso 6: Tabla de Últimas Transacciones

1. Presiona `T`, escribe "Últimas Transacciones"
2. **Size:** `18px`, **Weight:** Semibold, **Color:** `$color-text`
3. X `280`, Y `~300`

**Header de tabla:**
1. Presiona `R`, Width `1200`, Height `40`
2. X `280`, Y `~340`
3. **Fill:** `$color-bg`
4. Crea 4 textos como columnas: "Cliente", "Producto", "Monto", "Estado"
5. **Size:** `12px`, **Weight:** Semibold, **Color:** `$color-text-secondary`

**Filas de datos:**

Crea 5 filas, cada una:

1. Rectángulo Width `1200`, Height `48`
2. **Fill:** `$color-white`
3. **Stroke bottom:** `1px`, `$color-bg`
4. Textos: Cliente (ej: "María García"), Producto (ej: "Laptop Pro"), Monto (ej: "$1,299"), Estado (ej: "Completado")

Para el **Estado**, usa un badge:
1. Rectángulo pequeño: Width `80`, Height `24`
2. **Corner Radius:** `12px` (pill shape)
3. **Fill:** verde claro `#D1FAE5` para "Completado", amarillo `#FEF3C7` para "Pendiente"
4. Texto dentro, **Size:** `12px`

**Capas finales de la tabla:**
```
Tabla Transacciones
├── Titulo Tabla
├── Header Tabla
├── Fila 1 (María García)
│   ├── Badge Completado
│   └── Textos...
├── Fila 2 (Carlos López)
├── Fila 3 (Ana Martínez)
├── Fila 4 (Pedro Ramírez)
└── Fila 5 (Lucía Fernández)
```

### ✏️ Paso 7: Organización Final en Layers Panel

```
Pages
└── Page 1
    └── Dashboard (frame 1440×900)
        ├── Sidebar
        │   ├── Sidebar Bg
        │   ├── Logo
        │   ├── Nav Dashboard (activo)
        │   ├── Nav Productos
        │   ├── Nav Pedidos
        │   ├── Nav Usuarios
        │   └── Nav Configuración
        └── Contenido (grupo)
            ├── Header
            │   ├── Header Bg
            │   ├── Buscar Input
            │   └── Avatar
            ├── Titulo "Panel de Control"
            ├── Cards Container (flex)
            │   ├── Card Ventas
            │   ├── Card Usuarios
            │   ├── Card Pedidos
            │   └── Card Ingresos
            └── Tabla Transacciones
                ├── Titulo Tabla
                ├── Header Tabla
                ├── Fila 1
                ├── ...
                └── Fila 5
```

### ✏️ Paso 8: Probar Variables

1. Abre el **Variables Panel**
2. Cambia `color-primary` de `#3B82F6` a otro color, ej: `#7C3AED` (púrpura)
3. Observa cómo el logo, el nav activo y otros elementos se actualizan automáticamente
4. Vuelve al azul original

### ✏️ Paso 9: Exportar

1. Selecciona el frame `Dashboard`
2. Properties Panel → Export → **PNG** → Export layer
3. Guarda como `dashboard-panel.png`

---

## Desafíos Extra

- [ ] Duplica el dashboard y conviértelo a **dark mode** cambiando las variables
- [ ] Añade un **gráfico de barras** simulado con rectángulos de diferentes alturas
- [ ] Crea un **dropdown** de notificaciones (campana con badge rojo)
- [ ] Convierte la **Card Ventas** en un componente (`Cmd+Option+K`) y crea variantes
- [ ] Aplica **flex layout column** a la tabla para que los textos se alineen en columnas

---

## Lo que has practicado

| Herramienta/Panel | Lo usaste en |
|---|---|
| Variables Panel | Paso 1 — definir design tokens |
| Frame tool (`A`) | Paso 2 |
| Rectangle tool (`R`) | Pasos 3, 4, 5, 6 |
| Properties: Variables (`$var`) | Pasos 3, 4, 5, 6 |
| Flex layout (`Cmd+Option+G`) | Paso 5 |
| Effects (Shadow) | Paso 5 |
| Layers Panel (organización) | Pasos 3, 7 |
| Ellipse tool (`O`) | Paso 4 |
| Duplicar (`Cmd+D`) | Pasos 3, 5 |

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

> 📖 **Siguiente:** [Práctica 3: Sistema de Diseño — Tarjeta de Producto](./06c-practica-design-system.md)
