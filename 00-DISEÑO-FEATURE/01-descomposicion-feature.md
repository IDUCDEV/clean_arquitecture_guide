# Descomposición de Features: Framework FADER

> Aprende a diseccionar cualquier feature en piezas atómicas antes de escribir una línea de código.

---

## ¿Por qué descomponer?

Cuando te dan una feature como "agregar carrito de compras", el 80% del trabajo no es escribir el código del carrito. El trabajo real es entender:

- ¿Qué es un carrito en este negocio? (no todos los carritos funcionan igual)
- ¿Qué puede hacer el usuario con él?
- ¿Qué reglas de negocio aplican?
- ¿Qué bordes y excepciones existen?

La descomposición sistemática responde todo eso **antes** de abrir el editor.

---

## Framework FADER

```
 ┌─────────────────────────────────────────────────────────────┐
 │                      F A D E R                             │
 │                                                             │
 │  Formular → Actorizar → Descomponer → Entidades → Reglas  │
 │                                                             │
 │  De lo general → A lo específico                           │
 │  De lo externo → A lo interno                              │
 └─────────────────────────────────────────────────────────────┘
```

### Paso 1: Formular

Define el problema con la mayor precisión posible. Una feature bien formulada es media solución.

**Formato:**
> Como **[actor]**, quiero **[acción]** para **[beneficio/valor]**.

**Contraejemplos:**
- ❌ "Hay que hacer un carrito de compras"
- ❌ "El usuario necesita agregar productos"

**Bien formulados:**
- ✅ "Como **cliente registrado**, quiero **agregar productos a un carrito** para **revisarlos antes de comprar**."
- ✅ "Como **cliente**, quiero **ver el total actualizado del carrito** para **saber cuánto gastaré**."

**Plantilla de preguntas:**

| Pregunta | Lo que descubres |
|----------|------------------|
| ¿Qué necesidad real resuelve? | El propósito de la feature |
| ¿Qué pasa si NO existe? | La urgencia/impacto real |
| ¿Quién se beneficia? | Los actores involucrados |
| ¿Cómo se usa hoy sin esta feature? | El workaround actual |
| ¿Qué expectativas tiene el usuario? | Criterios de éxito |

---

### Paso 2: Actorizar

Identifica **quién** interactúa con la feature. Cada actor tiene intereses y permisos distintos.

**Tipos de actores:**

| Actor | Definición | Ejemplo |
|-------|------------|---------|
| **Usuario primario** | Quien inicia la acción | Cliente que compra |
| **Usuario secundario** | Quien provee soporte | Administrador que gestiona inventario |
| **Sistema externo** | API, servicio, BD | Pasarela de pagos, Supabase |
| **Sistema interno** | Otra feature de la app | Módulo de notificaciones, módulo de usuarios |

**Ejercicio: hoja de actores**

```
Feature: Carrito de Compras

┌──────────────────────────────────────────────────┐
│ ACTORES                                          │
│                                                  │
│  1. Cliente (usuario primario)                   │
│     - Puede ver su carrito                       │
│     - Puede agregar/quitar productos             │
│     - Puede modificar cantidades                 │
│     - Puede iniciar el checkout                  │
│                                                  │
│  2. Administrador (usuario secundario)           │
│     - Puede ver carritos abandonados             │
│     - Puede ajustar precios en carrito           │
│                                                  │
│  3. Pasarela de Pagos (sistema externo)          │
│     - Recibe el total del carrito                │
│     - Devuelve confirmación/rechazo              │
│                                                  │
│  4. Módulo de Inventario (sistema interno)       │
│     - Verifica stock disponible                  │
│     - Reserva productos temporalmente            │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Reglas de oro:**
- Cada actor tiene una **razón de ser** (no inventes actores)
- Un actor puede ser una persona o un sistema
- Un mismo usuario puede ser múltiples actores (ej: cliente y admin)

---

### Paso 3: Descomponer

Divide la feature en **operaciones atómicas**. Cada operación debe ser:

- **Independiente** (se puede probar sola)
- **Concreta** (hace una sola cosa)
- **Valiosa** (aporta algo al usuario o al sistema)

**Técnica: la tormenta de post-its**

Imagina que tienes post-its y escribes cada acción mínima en uno. Luego los agrupas.

```
Carrito de Compras → Operaciones Atómicas:

┌──────────────────────┐  ┌──────────────────────┐
│ Agregar producto     │  │ Quitar producto      │
│ al carrito           │  │ del carrito          │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│ Actualizar cantidad  │  │ Ver resumen          │
│ de un producto       │  │ del carrito          │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│ Aplicar cupón        │  │ Calcular total       │
│ de descuento         │  │ con impuestos        │
└──────────────────────┘  └──────────────────────┘

┌──────────────────────┐  ┌──────────────────────┐
│ Validar stock        │  │ Limpiar carrito      │
│ antes del checkout   │  │ (after checkout)     │
└──────────────────────┘  └──────────────────────┘
```

**Clasificación de operaciones:**

| Tipo | Definición | Ejemplo |
|------|------------|---------|
| **C**reate | Crear un nuevo recurso | Agregar producto al carrito |
| **R**ead | Leer/consultar datos | Ver resumen del carrito |
| **U**pdate | Actualizar un recurso | Cambiar cantidad |
| **D**elete | Eliminar un recurso | Quitar producto |
| **Validación** | Verificar reglas de negocio | Validar stock, validar cupón |
| **Cálculo** | Procesar datos para obtener resultado | Calcular total con impuestos |
| **Transición** | Cambiar estado | Iniciar checkout |

---

### Paso 4: Entidades

Identifica los **conceptos del mundo real** que aparecen en tu feature. No pienses en tablas de BD ni en clases de Dart. Piensa en objetos de negocio.

**Ejercicio: tarjeta de entidad**

Para cada entidad, llena esta tarjeta:

```
┌─────────────────────────────────────────────┐
│  ENTIDAD: Producto                          │
├─────────────────────────────────────────────┤
│                                              │
│  Descripción:                               │
│  Un bien o servicio que se puede comprar    │
│                                              │
│  Atributos esenciales:                      │
│  - id: string                               │
│  - nombre: string                           │
│  - precio: double                           │
│  - stock: int                               │
│                                              │
│  NO es atributo:                            │
│  - cantidadEnCarrito (eso es del Carrito,   │
│    no del Producto)                         │
│                                              │
│  Se relaciona con:                          │
│  - Carrito (a través de ItemCarrito)        │
│  - Categoría (clasificación)                │
│                                              │
└─────────────────────────────────────────────┘
```

**Entidades típicas para un Carrito de Compras:**

```
┌────────────────────────────────────────────────────────────┐
│ ENTIDADES DEL DOMINIO                                      │
│                                                            │
│  Producto                                                   │
│  ├── id: String                                            │
│  ├── nombre: String                                        │
│  ├── precio: double                                        │
│  ├── stock: int                                            │
│  └── categoria: Categoria                                  │
│                                                            │
│  ItemCarrito                                                │
│  ├── producto: Producto                                     │
│  ├── cantidad: int                                         │
│  └── precioUnitario: double (precio al momento de agregar) │
│                                                            │
│  Carrito                                                    │
│  ├── id: String                                            │
│  ├── items: List<ItemCarrito>                              │
│  ├── totalBruto: double                                    │
│  ├── descuento: double?                                    │
│  ├── impuesto: double                                      │
│  └── totalNeto: double                                     │
│                                                            │
│  CuponDescuento                                             │
│  ├── codigo: String                                        │
│  ├── tipo: Porcentaje | MontoFijo                          │
│  ├── valor: double                                         │
│  └── expiracion: DateTime                                  │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Pregunta clave:** ¿Esta entidad existe en el mundo real del negocio o solo existe en mi base de datos?

- ✅ `Producto` → Existe en el mundo real
- ❌ `ProductoTable` → Existe solo en la BD (eso va en la capa DATA)

---

### Paso 5: Reglas

Captura todas las **reglas de negocio**. Una regla es una condición que debe cumplirse siempre, independientemente de la interfaz de usuario o la tecnología.

**Categorías de reglas:**

| Categoría | Ejemplo |
|-----------|---------|
| **Restricción** | No se pueden agregar más de 50 productos distintos al carrito |
| **Cálculo** | El impuesto es del 16% sobre el total bruto menos descuentos |
| **Validación** | El cupón de descuento no puede estar expirado |
| **Flujo** | Si el stock es menor a la cantidad solicitada, mostrar error |
| **Consistencia** | Si se aplica un cupón, el descuento no puede exceder el 50% del total |

**Formato para documentar reglas:**

```
R001 - Restricción de cantidad máxima
  Descripción: Un carrito no puede tener más de 50 items distintos
  Actor: Cliente
  Severidad: Error
  Mensaje: "Has alcanzado el límite de 50 productos por carrito"

R002 - Validación de stock
  Descripción: No se puede agregar un producto si el stock es 0
  Actor: Cliente
  Severidad: Error
  Mensaje: "El producto {nombre} no tiene stock disponible"

R003 - Cálculo de impuesto
  Descripción: El impuesto se calcula como 16% del subtotal
  Actor: Sistema
  Severidad: Información

R004 - Cupón no expirado
  Descripción: No se puede aplicar un cupón cuya fecha de expiración haya pasado
  Actor: Cliente
  Severidad: Error
  Mensaje: "El cupón {codigo} ha expirado"

R005 - Descuento máximo
  Descripción: El descuento total no puede exceder el 50% del subtotal
  Actor: Sistema
  Severidad: Error
  Mensaje: "El descuento supera el límite permitido"
```

---

## La hoja FADER completa

Así se ve una feature completamente descompuesta:

```
╔═══════════════════════════════════════════════════════════╗
║  FEATURE: Carrito de Compras                             ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  [F]ormular:                                              ║
║  Como cliente, quiero gestionar productos en un carrito  ║
║  para revisarlos antes de comprar.                        ║
║                                                           ║
║  [A]ctorizar:                                             ║
║  1. Cliente (primario)                                    ║
║  2. Admin (secundario)                                    ║
║  3. Pasarela de Pagos (externo)                           ║
║  4. Módulo de Inventario (interno)                        ║
║                                                           ║
║  [D]escomponer:                                           ║
║  - Agregar producto (C)                                   ║
║  - Quitar producto (D)                                    ║
║  - Actualizar cantidad (U)                                ║
║  - Ver resumen (R)                                        ║
║  - Aplicar cupón (Validación)                             ║
║  - Calcular total (Cálculo)                               ║
║  - Validar stock (Validación)                             ║
║                                                           ║
║  [E]ntidades:                                             ║
║  - Producto, ItemCarrito, Carrito, CuponDescuento         ║
║                                                           ║
║  [R]eglas:                                                ║
║  R001: Máximo 50 items por carrito                        ║
║  R002: Stock > 0 para agregar                             ║
║  R003: Impuesto 16% del subtotal                          ║
║  R004: Cupón no expirado                                  ║
║  R005: Descuento máximo 50%                               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Errores comunes

| Error | Por qué duele | Cómo evitarlo |
|-------|---------------|---------------|
| Pensar en código demasiado pronto | Te casas con una implementación antes de entender el problema | Termina FADER completo antes de pensar en clases |
| Mezclar actores | Lógica de admin + cliente en el mismo lugar | Separa por actor desde el principio |
| Reglas implícitas | "Obviamente" el stock se valida... hasta que en producción falla | Escribe CADA regla, aunque te parezca obvia |
| Entidades hinchadas | Producto termina con 30 campos que no necesita | Solo atributos esenciales del negocio |
| Descomposición vaga | "Gestionar carrito" no es una operación atómica | Si tiene "y" en el nombre, divídelo |

---

## 🚀 Siguiente paso

Ahora que entiendes FADER, ve a la [práctica de descomposición](./01a-practica-carrito.md) y aplica el framework a una feature real de Carrito de Compras.

---

**Tiempo estimado de lectura:** 20 minutos  
**Tiempo estimado de práctica:** 30-40 minutos  
**Herramientas:** Papel y lápiz
