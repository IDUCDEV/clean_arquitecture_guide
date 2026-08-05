# Descomposición de Features: Framework FADER

> Aprende a diseccionar cualquier feature en piezas atómicas antes de escribir una línea de código.

---

## Paso 0: Define el Alcance

Antes de descomponer, fija los límites de la feature. Una feature puede estar perfectamente descompuesta y aun así crecer sin control si el alcance es ambiguo.

```
Feature: Gestión de compradores (Buyers)

Incluye:
- Listar compradores.
- Buscar por nombre o teléfono.
- Aprobar tickets seleccionados.
- Liberar tickets no seleccionados.

No incluye:
- Enviar notificaciones.
- Procesar pagos.
- Editar datos del comprador.

Dependencias:
- Autenticación (identidad del organizador).
- Feature de rifas (tabla raffles).

Suposiciones:
- Un comprador pertenece a una sola rifa.

Preguntas abiertas:
- ¿Puede aprobarse un ticket ya aprobado?
- ¿La aprobación debe ser atómica?
```

**Regla:** cada operación que descubras en FADER debe caber en "Incluye". Si descubres algo que no cabe, o amplía el alcance (y se negocia), o es otra feature.

Consulta la teoría completa y la plantilla en [00-alcance-feature.md](./00-alcance-feature.md).

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

Captura todas las **reglas**. Una regla es una condición que debe cumplirse siempre, independientemente de la interfaz de usuario o la tecnología.

**Clasifica las reglas en 3 tipos.** No todas pertenecen al dominio:

| Tipo | Código | Qué es | Ejemplo | Dónde vive |
|------|--------|--------|---------|------------|
| **Negocio** | `RN` | Regla del negocio, independiente de la tecnología | Un ticket aprobado no vuelve a aprobarse | UseCase (dominio) |
| **Técnica** | `RT` | Requisito de implementación con el stack | La búsqueda debe estar paginada | Contrato con el backend / DataSource |
| **Seguridad** | `RS` | Restricción de acceso y permisos | Impedir acceder a rifas ajenas | Autorización del servidor (RLS en Supabase / middleware en REST) |

**Categorías de reglas de negocio (RN):**

| Categoría | Ejemplo |
|-----------|---------|
| **Restricción** | No se pueden agregar más de 50 productos distintos al carrito |
| **Cálculo** | El impuesto es del 16% sobre el total bruto menos descuentos |
| **Validación** | El cupón de descuento no puede estar expirado |
| **Flujo** | Si el stock es menor a la cantidad solicitada, mostrar error |
| **Consistencia** | Si se aplica un cupón, el descuento no puede exceder el 50% del total |

**Reglas técnicas (RT) y de seguridad (RS):**

```
RT001 - La consulta de productos debe estar paginada
RT002 - La búsqueda debe tener debounce
RT003 - La operación de aprobar+liberar debe ser atómica (RPC)

RS001 - Solo el organizador puede leer su rifa (RLS)
RS002 - Solo el organizador puede modificar sus tickets
```

> Estas reglas NO van al dominio ni a la UI. Se diseñan en [05e-diseno-supabase.md](./05e-diseno-supabase.md) y se implementan en DATA (DataSource + migración SQL).

**Formato para documentar reglas:**

```
RN001 - Restricción de cantidad máxima
  Descripción: Un carrito no puede tener más de 50 items distintos
  Actor: Cliente
  Severidad: Error
  Mensaje: "Has alcanzado el límite de 50 productos por carrito"

RN002 - Validación de stock
  Descripción: No se puede agregar un producto si el stock es 0
  Actor: Cliente
  Severidad: Error
  Mensaje: "El producto {nombre} no tiene stock disponible"

RN003 - Cálculo de impuesto
  Descripción: El impuesto se calcula como 16% del subtotal
  Actor: Sistema
  Severidad: Información

RN004 - Cupón no expirado
  Descripción: No se puede aplicar un cupón cuya fecha de expiración haya pasado
  Actor: Cliente
  Severidad: Error
  Mensaje: "El cupón {codigo} ha expirado"

RN005 - Descuento máximo
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
║  [0] ALCANCE:                                             ║
║  Incluye: gestionar items, cupones y resumen              ║
║  No incluye: pagos, envíos, fidelización                  ║
║  Dependencias: catálogo de productos, inventario          ║
║  Suposiciones: cliente con sesión iniciada                ║
║  Preguntas abiertas: ¿cupones combinables?                ║
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
║  RN001: Máximo 50 items por carrito                       ║
║  RN002: Stock > 0 para agregar                            ║
║  RN003: Impuesto 16% del subtotal                         ║
║  RN004: Cupón no expirado                                 ║
║  RN005: Descuento máximo 50%                              ║
║  RT001: Búsqueda paginada                                 ║
║  RS001: RLS impide carritos ajenos                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Técnicas Complementarias

FADER no vive solo. Existen otras técnicas de descomposición que puedes usar dentro de cada paso. No son competencia, son herramientas que enriquecen pasos específicos.

### Event Storming — Alberto Brandolini

**Qué es:** Una dinámica de grupo donde se escriben eventos del negocio en post-its naranjas y se colocan en una línea de tiempo.

**Dónde encaja en FADER:**

| Paso FADER | Cómo ayuda Event Storming |
|------------|--------------------------|
| **D**escomponer | Los eventos ("Producto agregado al carrito", "Cupón aplicado") son operaciones atómicas |
| **R**eglas | Los eventos revelan restricciones ("No se puede agregar si no hay stock") |
| **E**ntidades | Los objetos que aparecen en los eventos son candidatos a entidad |

**Cómo usarlo individualmente:**

```
1. Escribe todos los eventos que pueden ocurrir:
   "Producto agregado al carrito"
   "Cantidad actualizada"
   "Cupón aplicado"
   "Stock validado"
   "Carrito limpiado después del checkout"

2. Ordénalos en una línea de tiempo:
   Antes del checkout  → [Agregar → Actualizar → Validar stock → Aplicar cupón]
   Checkout            → [Calcular total → Procesar pago]
   Después             → [Limpiar carrito → Confirmar pedido]

3. Cada post-it es una operación atómica → lo pasas a tu [D]escomposición
```

**Ventaja:** Revela operaciones que no habías considerado (ej: "Carrito abandonado después de 24h" es un evento que no está en los requisitos originales).

---

### User Story Mapping — Jeff Patton

**Qué es:** Técnica para organizar historias de usuario en un mapa de dos dimensiones: actividades principales (eje horizontal) y pasos específicos (eje vertical).

**Dónde encaja en FADER:**

| Paso FADER | Cómo ayuda User Story Mapping |
|------------|-------------------------------|
| **F**ormular | Las actividades principales del mapa son tus enunciados "Como... quiero..." |
| **A**ctorizar | Cada columna del mapa suele corresponder a un actor |
| **D**escomponer | Los pasos verticales son tus operaciones atómicas |

**Ejemplo para Carrito:**

```
                   ANTES                      DURANTE                     DESPUES
                  ┌─────────────┐           ┌──────────────┐          ┌──────────────┐
                  │ Explorar    │           │ Gestionar    │          │ Finalizar    │
                  │ productos   │           │ carrito      │          │ compra       │
                  ├─────────────┤           ├──────────────┤          ├──────────────┤
                  │ Ver catalogo│           │ Agregar prod │          │ Ir a checkout│
                  │ Buscar prod │           │ Quitar prod  │          │ Confirmar    │
                  │ Filtrar     │           │ Actualizar   │          │ Pago         │
                  │             │           │ Aplicar cupon│          │ Confirmacion │
                  └─────────────┘           └──────────────┘          └──────────────┘
```

---

### Example Mapping — Cucumber/BDD

**Qué es:** Técnica para descomponer una historia en ejemplos concretos usando tarjetas de colores.

**Dónde encaja en FADER:**

| Paso FADER | Como ayuda Example Mapping |
|------------|-----------------------------|
| **R**eglas | Cada regla se ilustra con un ejemplo concreto de entrada -> salida |

**Formato:**

```
Historia: Aplicar cupon de descuento

REGLA: Cupon debe estar vigente

  -> Ejemplo valido: Cupon "DESC10", fecha expiracion > hoy
     Resultado: Descuento aplicado

  -> Ejemplo invalido: Cupon "DESC10", fecha expiracion < hoy
     Resultado: Error "El cupon ha expirado"
```

**Ventaja:** Los ejemplos concretos son la mejor manera de validar que entendiste la regla. Si no puedes escribir 3 ejemplos de una regla, no la entiendes bien.

---

## Criterio de Granularidad

Uno de los problemas mas comunes al aplicar FADER es **no saber cuando parar**. Usa el test de la atomicidad.

### El test de la atomicidad

Una operacion atomica debe pasar **las 3 pruebas**:

| # | Prueba | Pregunta | Si falla... |
|---|--------|----------|-------------|
| 1 | **Un solo verbo** | La operacion hace una sola cosa? | Dividela |
| 2 | **Un solo resultado** | Produce un unico cambio en el sistema? | Dividela |
| 3 | **Valor independiente** | Tiene sentido por si sola para el usuario? | Combinala o eliminala |

**Ejemplos:**

```
"Gestionar carrito" -> Falla prueba 1 (tiene multiples verbos implicitos)
   Correcto: "Agregar producto", "Quitar producto", "Actualizar cantidad"

"Agregar producto y aplicar cupon" -> Falla prueba 1 y 2
   Correcto: "Agregar producto" y "Aplicar cupon" son operaciones separadas

"Validar formato del codigo del cupon" -> Falla prueba 3
   Sin valor para el usuario por si sola, es parte de "Aplicar cupon"
```

### Guia por tipo de feature

| Tipo de feature | Tamano tipico de [D]escomposicion | Ejemplo |
|-----------------|-----------------------------------|---------|
| Hotfix / bug | 1-2 operaciones | Corregir calculo de impuesto |
| Feature pequena | 3-6 operaciones | Agregar filtro de busqueda |
| Feature mediana | 7-15 operaciones | Carrito de compras |
| Feature grande | 16-30 operaciones | Sistema de facturacion recurrente |
| Epic | 30+ (dividir en sub-features) | Modulo completo de pagos |

**Regla practica:** Si tu [D]escomposicion supera las 20 operaciones, probablemente no es una feature sino un conjunto de features. Dividelo.

### Senales de granularidad incorrecta

```
Demasiado grueso:
  - "Gestionar usuarios" -> no sabes que incluye
  - "Procesar pedido" -> puede ser 10 operaciones distintas

Demasiado fino:
  - "Validar que el campo email no este vacio" -> es parte de un UseCase
  - "Convertir string a mayusculas" -> detalle tecnico, no operacion de negocio

El punto justo:
  - "Registrar usuario" -> operacion completa con validaciones + persistencia
  - "Crear pedido" -> operacion que puede fallar pero se entiende como unidad
```

---

## Antipatrones de FADER

A veces es mas facil reconocer lo que esta mal. Aqui tienes FADER bien hecho vs mal hecho para la misma feature.

### Feature: Filtro de busqueda de productos

**FADER MAL HECHO:**

```
[F] Como usuario, quiero buscar productos (demasiado vago)

[A] Cliente, Admin (el admin aparecio porque si, no tiene accion real)

[D] - Buscar productos (una sola operacion que lo abarca todo)
    - Ver resultados (no es una operacion, es el resultado de buscar)

[E] Producto (solo esta entidad, pero faltan Categoria, Marca, etc.)

[R] - El producto debe existir (regla tecnica RT, no de negocio)
    - Mostrar resultados (eso no es una regla, es un comportamiento)
```

**Problemas:**
- No distingue tipos de busqueda (texto libre, por categoria, por precio)
- Actor inventado sin proposito
- Operaciones demasiado gruesas
- Reglas que no son reglas de negocio (o no están clasificadas: las técnicas y de seguridad van como RT/RS)
- Entidades incompletas

---

**FADER BIEN HECHO:**

```
[F] F1: Como cliente, quiero buscar productos por nombre o categoria
        para encontrar lo que necesito rapidamente.
    F2: Como cliente, quiero filtrar productos por rango de precio
        para ajustarme a mi presupuesto.

[A] 1. Cliente (primario) -> busca, filtra, navega resultados
    2. Sistema de inventario (interno) -> provee datos de stock

[D] Cliente:
    - [R] Buscar por texto libre (nombre del producto)
    - [R] Filtrar por categoria
    - [R] Filtrar por rango de precio
    - [R] Ordenar resultados (precio, nombre, popularidad)
    - [R] Ver paginacion de resultados

[E] Producto (id, nombre, precio, categoriaId, marcaId, stock)
    Categoria (id, nombre)
    Marca (id, nombre)
    FiltroBusqueda (VO: texto, categoriaId?, precioMin?,
                    precioMax?, ordenarPor?, pagina)

[R] RN001: Busqueda por texto libre coincide con nombre o descripcion
    RN002: Los filtros se aplican en AND (categoria Y precio Y texto)
    RN003: Sin resultados -> mensaje "No se encontraron productos"
    RN004: Producto sin stock aparece al final con marca "Agotado"
    RT001: Resultados paginados de a 20 items
    RS001: Solo clientes autenticados pueden buscar (RLS/catálogo público)
```

**Aciertos:**
- Dos formulaciones para dos necesidades distintas
- Actor con proposito claro
- Operaciones con clasificacion CRUD
- Value Object explicito para el filtro
- Reglas especificas y bordes contemplados

---

## Second Pass: Iterar el FADER

El primer FADER nunca es perfecto. La descomposicion es un proceso iterativo.

### Cuando revisitar cada paso

| Paso | Disparador de revision |
|------|----------------------|
| **F**ormular | Cuando encuentras un actor que no formulaste. Ej: "Ah, el admin tambien necesita aprobar cupones" |
| **A**ctorizar | Cuando una operacion no tiene actor claro. Ej: "Quien dispara el calculo de impuestos?" |
| **D**escomponer | Cuando una regla revela operaciones que faltan. Ej: "RN004 dice que el cupon expira... -> falta 'Validar vigencia de cupon'" |
| **E**ntidades | Cuando una regla menciona conceptos sin entidad. Ej: "RN005 habla de 'limite de descuento' -> falta entidad LimiteDescuento" |
| **R**eglas | Cuando modelas entidades y ves bordes. Ej: "Que pasa si el precio es 0? y si es negativo?" |

### Ciclo de refinamiento recomendado

```
1er pase: F A D E R (rapido, 15 min)
    |
Revisas [D]escomponer -> falta algo?
    |
Revisas [R]eglas -> revelan nuevas operaciones o entidades?
    |
2do pase: ajustas donde hizo falta (10 min)
    |
Revision cruzada: cada regla tiene operacion?
                  cada operacion tiene actor?
                  cada entidad se usa en alguna regla?
```

**Senales de que necesitas un second pass:**
- Una regla menciona un concepto que no esta en tus entidades
- Una operacion no tiene a quien asignarle la responsabilidad
- Descubres que dos actores hacen lo mismo pero con reglas distintas
- Al escribir el UseCase, te das cuenta de que la operacion deberia ser dos

---

## FADER para Features Grandes vs Pequenas

No todas las features merecen el mismo nivel de descomposicion. Aplicar FADER completo a un hotfix es sobreingenieria. Aplicar solo dos pasos a un epic es negligencia.

### Matriz de esfuerzo

```
                    Hotfix     Pequena     Mediana     Grande      Epic
                    (1-2 op)   (3-6 op)    (7-15 op)   (16-30 op)  (30+ op)

[F]ormular            Rapido     Completo   Completo    Completo    Multiples
[A]ctorizar           Opcional   Rapido     Completo    Completo    Completo
[D]escomponer         Rapido     Completo   Completo    Completo    Por feature
[E]ntidades           Opcional   Rapido     Completo    Completo    Completo
[R]eglas              Las clave  Las clave  Completo    Completo    Completo
```

**Donde esta el limite?**

- **Hotfix:** Solo formula y las reglas clave. 5 minutos. No hagas una tesis.
- **Feature pequena:** FADER completo pero rapido. 15-20 minutos.
- **Feature mediana:** FADER completo con second pass. 30-45 minutos.
- **Feature grande:** FADER completo mas ADR. 1-2 horas.
- **Epic:** Divide en features medianas y aplica FADER a cada una.

### Ejemplo: Hotfix vs Feature completa

**Hotfix:** "Corregir que el calculo de IVA use 16% en vez de 21%"

```
[F] Como sistema, quiero usar la tasa de IVA correcta (16%)
    para cumplir con la normativa fiscal.

[R] RN001: El IVA para productos nacionales es 16%
    (era 21% por error)

-- Esto es suficiente. No necesitas actores, entidades, ni descomposicion.
-- Arreglas la constante y listo.
```

**Feature completa:** "Modulo de configuracion de impuestos por pais"

```
[F] Como administrador, quiero configurar tasas de impuesto
    por pais y tipo de producto para cumplir con regulaciones locales.

[A] Admin, Sistema de Facturacion, API de impuestos externa

[D] - [C] Crear configuracion de impuesto
    - [R] Listar configuraciones
    - [U] Editar tasa de impuesto
    - [D] Eliminar configuracion (si no tiene facturas asociadas)
    - [Validacion] Validar que la tasa este dentro del rango legal

[E] ConfiguracionImpuesto (pais, tipoProducto, porcentaje,
    fechaInicio, fechaFin, codigoFiscal)
    HistorialCambio (configuracionId, fecha, usuario, valorAnterior, valorNuevo)

[R] RN001: La tasa de IVA no puede ser negativa
    RN002: No se puede eliminar una configuracion con facturas emitidas
    RN003: Los cambios quedan registrados en historial
    RT001: El calculo de impuestos se hace en un RPC (precision decimal)
```

---

## Conexion con Ceremonias Agiles

FADER no es solo para vos en tu escritorio. Funciona en dinamicas de equipo.

### En Refinement

```
Antes: "Vamos a ver la historia #42: Carrito de compras"
       -> discusion vaga de 30 minutos sin conclusion

Con FADER: "Vamos a aplicar FADER a la historia #42"
   Paso 1: Todos escriben [F]ormular en post-its (5 min)
   Paso 2: Comparten y consolidan (5 min)
   Paso 3: [D]escomponer en pizarron (10 min)
   Paso 4: Identificar [R]eglas dudosas (5 min)

Resultado: 25 minutos, todos alineados, lista de operaciones clara
```

### En Planning

Usa la [D]escomposicion como fuente de truth para estimar:

```
Historia: Carrito de compras

Operaciones (de FADER):
  - Agregar producto       -> 2 puntos
  - Quitar producto        -> 1 punto
  - Actualizar cantidad    -> 1 punto
  - Ver resumen            -> 2 puntos
  - Aplicar cupon          -> 3 puntos
  - Calcular total         -> 2 puntos
  - Validar stock          -> 2 puntos
  - Limpiar carrito        -> 1 punto

Total: 14 puntos (feature mediana)
```

Cada operacion se estima individualmente, no la feature entera. Esto elimina las estimaciones "adivinadas".

### En un Spike tecnico

Cuando no sabes si algo es posible, FADER te ayuda a definir el alcance del spike:

```
[F] Queremos saber si podemos integrar la pasarela de pagos X

[D] Dentro del spike:
    - Investigar documentacion de la API
    - Crear prototipo de un pago exitoso
    - Probar manejo de errores (rechazo, timeout, expirado)
    - Medir latencia promedio

[R] Reglas del spike:
    - Maximo 2 dias de investigacion
    - Al terminar: decision de seguir o no + riesgos identificados
```

---

## Validacion del FADER

### Checklist de autoevaluacion

Al terminar tu hoja FADER, responde estas preguntas:

**Sobre el [0] ALCANCE:**
- [ ] Definiste Incluye, No incluye, Dependencias, Suposiciones y Preguntas abiertas
- [ ] Cada operacion de FADER cabe en "Incluye"
- [ ] Las preguntas abiertas criticas se resolvieron antes de descomponer

**Sobre [F]ormular:**
- [ ] Cada enunciado sigue "Como [actor], quiero [accion] para [valor]"
- [ ] No hay dos enunciados que digan lo mismo
- [ ] Sabes cual es la diferencia entre lo que SI hace la feature y lo que NO hace

**Sobre [A]ctorizar:**
- [ ] Cada actor tiene al menos una operacion que le pertenece
- [ ] Ningun actor esta ahi "porque sí"
- [ ] Los sistemas externos estan identificados
- [ ] Sabes donde terminan los permisos de cada actor

**Sobre [D]escomponer:**
- [ ] Cada operacion pasa el test de atomicidad (1 verbo, 1 resultado, valor independiente)
- [ ] No hay operaciones con "y" en el nombre
- [ ] Las operaciones estan clasificadas (CRUD, Validacion, Calculo, Transicion)
- [ ] Las dependencias entre operaciones estan claras

**Sobre [E]ntidades:**
- [ ] Cada entidad existe en el mundo real del negocio
- [ ] Los atributos son esenciales, no tecnicos
- [ ] Las relaciones entre entidades estan definidas
- [ ] No hay atributos que pertenezcan a otra entidad

**Sobre [R]eglas:**
- [ ] Cada regla tiene un codigo unico (RN001, RT001, RS001...)
- [ ] Clasificaste cada regla: RN (negocio), RT (tecnica), RS (seguridad)
- [ ] No hay reglas tecnicas o de seguridad mezcladas con las de negocio
- [ ] No hay reglas "obvias" sin escribir
- [ ] Cada regla RN tiene una categoria (Restriccion, Calculo, Validacion, Flujo, Consistencia)
- [ ] Las reglas tienen mensaje de error donde aplica

**Revision cruzada:**
- [ ] Cada regla se relaciona con al menos una operacion
- [ ] Cada operacion tiene un actor responsable
- [ ] Cada entidad aparece en al menos una regla
- [ ] No hay contradicciones entre reglas

### Ejercicio: Autoevaluacion de un FADER real

Toma la hoja FADER del Carrito de Compras y aplica este checklist. Marca lo que cumple y lo que no. Si algo no cumple, revisa si falta ajustar.

```
Feature: Carrito de Compras

[F] "Como cliente, quiero gestionar productos en un carrito
     para revisarlos antes de comprar."

  -> Cumple: "Como [cliente], quiero [gestionar productos en un carrito]
     para [revisarlos antes de comprar]."
  -> NO cumple: no diferencia entre agregar, quitar, y actualizar
     (el verbo "gestionar" es muy amplio para [F]ormular)

  Mejora: dividir en 3 enunciados mas especificos
```

**Nota:** El checklist es para que lo uses, no para que lo cumplas al 100% siempre. Un hotfix no necesita todas las preguntas. Una feature critica sí.

---

## Errores comunes

| Error | Por qué duele | Cómo evitarlo |
|-------|---------------|---------------|
| Empezar sin alcance | La feature crece durante la implementación | Define Incluye/No incluye antes (Paso 0) |
| Pensar en código demasiado pronto | Te casas con una implementación antes de entender el problema | Termina FADER completo antes de pensar en clases |
| Mezclar actores | Lógica de admin + cliente en el mismo lugar | Separa por actor desde el principio |
| Reglas implícitas | "Obviamente" el stock se valida... hasta que en producción falla | Escribe CADA regla, aunque te parezca obvia |
| Mezclar tipos de reglas | Paginación/RLS entran como reglas de negocio | Clasifica RN / RT / RS |
| Entidades hinchadas | Producto termina con 30 campos que no necesita | Solo atributos esenciales del negocio |
| Descomposición vaga | "Gestionar carrito" no es una operación atómica | Si tiene "y" en el nombre, divídelo |

---

## 🚀 Siguiente paso

Ahora que entiendes FADER, ve a la [práctica de descomposición](./01a-practica-carrito.md) y aplica el framework a una feature real de Carrito de Compras. Cuando termines el FADER, conviértelo en pruebas verificables con los [criterios de aceptación y la matriz de trazabilidad](./05f-criterios-aceptacion-trazabilidad.md).

---

**Tiempo estimado de lectura:** 40 minutos  
**Tiempo estimado de práctica:** 30-40 minutos  
**Herramientas:** Papel y lápiz
