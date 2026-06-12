# Práctica: Descomponer Feature Carrito de Compras

> Aplica el framework FADER a una feature real de Carrito de Compras. Papel y lápiz en mano.

---

## Instrucciones

1. Consigue una **hoja de papel y un lápiz** (o un pizarrón, o una tablet)
2. No abras ningún editor de código. **Cero código.**
3. Sigue cada paso FADER en orden
4. Al final, compara tus respuestas con las soluciones sugeridas

---

## Enunciado

Somos parte del equipo de una tienda online. El equipo de producto nos pide:

> **Feature:** Los clientes deben poder agregar productos a un carrito de compras, ver el resumen con precios actualizados, y aplicar cupones de descuento antes de iniciar el proceso de pago.

---

## Paso a Paso

### ✏️ Paso 1: Formular

Escribe en tu hoja:

1. ¿Cuál es la necesidad real del cliente?
2. ¿Qué pasa si esta feature no existe?
3. Tres enunciados tipo "Como [actor]..."

**Reflexiona:**
- No es lo mismo un carrito "de tienda física" donde puedes tocar los productos, que uno "de e-commerce"
- No es lo mismo un carrito "para una tienda de zapatos" que "para un supermercado mayorista"
- ¿Qué matices aplican a nuestro caso?

### ✏️ Paso 2: Actorizar

Dibuja una tabla de actores:

1. Identifica al menos 3 actores
2. Para cada actor, escribe qué puede y qué NO puede hacer
3. Define los límites: ¿dónde termina el carrito y empieza otro sistema?

**Pregúntate:**
- ¿El administrador puede modificar el carrito de un cliente?
- ¿El sistema de pagos necesita conocer los items del carrito o solo el total?

### ✏️ Paso 3: Descomponer

Enumera todas las operaciones atómicas usando post-its imaginarios:

1. Opera por operación, pregúntate: ¿esto hace una sola cosa?
2. Clasifícalas en: CRUD, Validación, Cálculo
3. Agrúpalas por actor
4. Identifica dependencias: ¿qué operaciones deben ejecutarse antes que otras?

### ✏️ Paso 4: Entidades

Dibuja las tarjetas de entidad:

1. ¿Qué objetos de negocio existen?
2. ¿Cuáles son sus atributos esenciales?
3. ¿Cómo se relacionan entre sí?
4. ¿Qué NO pertenece a cada entidad?

### ✏️ Paso 5: Reglas

Enuncia al menos 5 reglas de negocio:

1. Usa el formato R001, R002...
2. Clasifica cada una: Restricción, Cálculo, Validación, Flujo
3. Define el mensaje de error para el usuario donde aplique
4. Piensa en bordes: ¿qué pasa si el precio es 0? ¿si la cantidad es negativa?

---

## Solución Sugerida

Compara después de hacerlo tú mismo. No mires antes de terminar.

### ✅ Formular

> Como **cliente con sesión iniciada**, quiero **gestionar mi carrito de compras (agregar, quitar, modificar productos, aplicar cupones y ver el resumen económico)** para **revisar mi pedido antes de pagar**.

**Tres enunciados:**
- "Como cliente, quiero agregar productos al carrito para acumular mi pedido."
- "Como cliente, quiero ver el total actualizado del carrito para saber cuánto gastaré."
- "Como cliente, quiero aplicar un cupón de descuento para obtener un mejor precio."

### ✅ Actorizar

| Actor | Rol | Permisos |
|-------|-----|----------|
| Cliente | Primario | CRUD items, aplicar cupón, ver resumen |
| Admin | Secundario | Ver carritos abandonados, ajustar precios |
| Módulo de Inventario | Sistema interno | Validar stock |
| Pasarela de Pagos | Sistema externo | Solo recibe total y items del checkout |

### ✅ Descomponer

```
Cliente:
  [C] Agregar producto al carrito
  [D] Quitar producto del carrito
  [U] Actualizar cantidad de un producto
  [R] Ver resumen del carrito (items + totales)
  [Validación] Aplicar cupón de descuento
  [Cálculo] Calcular subtotal
  [Cálculo] Calcular impuesto
  [Cálculo] Calcular total neto

Sistema (automático):
  [Validación] Validar stock antes de agregar
  [Validación] Validar cupón (vigencia, aplicabilidad)
  [Acción] Limpiar carrito después del checkout

Flujo de dependencias:
  1. Validar stock → Agregar producto
  2. Agregar producto → Calcular subtotal → Calcular impuesto → Calcular total
  3. Aplicar cupón → Validar cupón → Recalcular descuento → Recalcular total
```

### ✅ Entidades

```
Producto:
  id, nombre, precio, stock, categoria

ItemCarrito:
  producto (ref Producto), cantidad, precioUnitario

Carrito:
  id, items (List<ItemCarrito>), cuponAplicado, subtotal, descuento, impuesto, total

CuponDescuento:
  codigo, tipo (porcentaje/montoFijo), valor, fechaExpiracion, usoMaximo, usosActuales
```

### ✅ Reglas

| Código | Descripción | Tipo | Mensaje |
|--------|-------------|------|---------|
| R001 | Máximo 50 items distintos por carrito | Restricción | "Has alcanzado el límite de 50 productos" |
| R002 | Stock debe ser > 0 para agregar | Validación | "Producto {nombre} sin stock disponible" |
| R003 | Cantidad a agregar debe ser > 0 | Validación | "La cantidad debe ser mayor a 0" |
| R004 | Impuesto = 16% (subtotal - descuento) | Cálculo | — |
| R005 | Cupón debe estar vigente (no expirado) | Validación | "El cupón {codigo} ha expirado" |
| R006 | Descuento máximo 50% del subtotal | Restricción | "El descuento supera el límite permitido" |
| R007 | Precio unitario se congela al agregar | Consistencia | — |

---

## ¿Qué sigue?

Antes de seguir, revisa tu hoja. ¿Identificaste algo que no está en la solución? ¿La solución tiene algo que se te escapó?

Si encuentras diferencias, no significa que esté mal. El diseño no tiene una única respuesta correcta. Lo importante es el **proceso de pensamiento**.

Cuando estés satisfecho con tu descomposición, continúa con [02-mapeo-capas.md](./02-mapeo-capas.md) para traducir esto a Clean Architecture.

---

**Tiempo:** 30-40 minutos  
**Material:** Papel, lápiz, goma de borrar
