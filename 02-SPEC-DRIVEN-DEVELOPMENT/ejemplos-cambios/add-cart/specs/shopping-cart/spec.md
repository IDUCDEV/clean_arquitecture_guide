# Spec: shopping-cart

## WHY
Los clientes necesitan acumular productos y ver el coste real antes de pagar. Sin carrito, cada compra es unitaria y no existen descuentos.

## Purpose
Garantizar un carrito por cliente autenticado con integridad económica (precios congelados, impuesto 16%, cupones validados) y aislamiento total entre clientes (RLS).

## ADDED Requirements

### Requirement: Agregar producto al carrito (REQ-001)
El sistema agregará productos al carrito del cliente validando stock y límites.

#### Scenario: Producto con stock disponible
- **WHEN** el cliente agrega un producto con stock > 0
- **THEN** el sistema DEBERÁ agregarlo con cantidad inicial 1 y congelar su precio unitario
- **AND** recalcular subtotal, impuesto y total

#### Scenario: Producto sin stock
- **IF** el stock del producto es 0
- **THEN** el sistema DEBERÁ mostrar "Producto {nombre} sin stock disponible" sin modificar el carrito

#### Scenario: Límite de items alcanzado
- **IF** el carrito ya contiene 50 productos distintos
- **THEN** el sistema DEBERÁ mostrar "Has alcanzado el límite de 50 productos"

#### Scenario: Cantidad inválida al actualizar
- **IF** la cantidad indicada es ≤ 0
- **THEN** el sistema DEBERÁ mostrar "La cantidad debe ser mayor a 0"

### Requirement: Quitar producto del carrito (REQ-002)
El cliente eliminará items de su carrito.

#### Scenario: Item existente
- **WHEN** el cliente quita un item del carrito
- **THEN** el sistema DEBERÁ eliminarlo y recalcular los totales

### Requirement: Ver resumen económico (REQ-003)
El sistema calculará subtotal, impuesto y total.

#### Scenario: Carrito con items
- **MIENTRAS** el carrito tenga items
- **EL SISTEMA DEBERÁ** mostrar subtotal = Σ(precioUnitario × cantidad), impuesto = 16% × (subtotal − descuento) y total = subtotal − descuento + impuesto

#### Scenario: Carrito vacío
- **MIENTRAS** el carrito no tenga items
- **EL SISTEMA DEBERÁ** mostrar estado vacío sin totales calculados

### Requirement: Aplicar cupón de descuento (REQ-004)
El cliente aplicará un cupón válido a su carrito.

#### Scenario: Cupón vigente aplicable
- **WHEN** el cliente aplica un cupón no expirado con usos disponibles
- **THEN** el sistema DEBERÁ recalcular el descuento según tipo (porcentaje o monto fijo)

#### Scenario: Cupón expirado
- **IF** la fechaExpiracion del cupón ya pasó
- **THEN** el sistema DEBERÁ mostrar "El cupón {codigo} ha expirado"

#### Scenario: Descuento sobre límite
- **IF** el descuento resultante supera el 50% del subtotal
- **THEN** el sistema DEBERÁ mostrar "El descuento supera el límite permitido"

### Requirement: Aislamiento entre carritos (REQ-005)
Cada cliente accederá únicamente a su propio carrito.

#### Scenario: Lectura propia
- **GIVEN** un cliente autenticado
- **WHEN** consulta su carrito
- **THEN** solo recibe filas donde `auth.uid() = user_id`

#### Scenario: Intento de acceso ajeno
- **IF** un cliente intenta leer/escribir el carrito de otro usuario
- **THEN** Supabase DEBERÁ devolver conjunto vacío/denegación vía RLS

### Requirement: Estados UI del carrito (REQ-006)
La interfaz reflejará cada estado del flujo.

#### Scenario: Carga inicial
- **WHEN** la página del carrito se abre
- **THEN** se muestra `CartLoading` hasta recibir datos

#### Scenario: Error de red
- **SI** falla la comunicación con Supabase
- **ENTONCES** se muestra "Error de conexión" con opción de reintentar
