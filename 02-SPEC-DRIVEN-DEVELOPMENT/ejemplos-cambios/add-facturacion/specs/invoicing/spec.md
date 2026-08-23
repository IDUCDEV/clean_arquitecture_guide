# Spec: invoicing

## WHY
Cobrar exige documentos trazables con estados claros y pagos conciliados.

## Purpose
Garantizar que cada transición de estado cumpla sus reglas y que la numeración sea secuencial e inmutable.

## ADDED Requirements

### Requirement: Crear y emitir factura (REQ-001)
#### Scenario: Emisión válida
- **WHEN** el emisor emite un borrador con ≥1 item y vencimiento posterior a emisión
- **THEN** recibe número secuencial FFF-000001 (RN001, RT001) y pasa a `emitida`

#### Scenario: Sin items
- **IF** el borrador no tiene items
- **THEN** el sistema DEBERÁ mostrar "No se puede emitir una factura sin items" (RN002)

#### Scenario: Vencimiento inválido
- **IF** fechaVencimiento ≤ fechaEmision
- **THEN** el sistema DEBERÁ mostrar "La fecha de vencimiento debe ser posterior" (RN003)

### Requirement: Transiciones de estado (REQ-002)
#### Scenario: Editar no-borrador
- **IF** la factura no está en `borrador`
- **THEN** el sistema DEBERÁ rechazar la edición (RN004)

#### Scenario: Pagar solo lo pagable
- **MIENTRAS** el estado sea `emitida` o `enviada`
- **EL SISTEMA DEBERÁ** aceptar pagos; cualquier otro estado los rechaza (RN006)

### Requirement: Pagos y saldo (REQ-003)
#### Scenario: Pago parcial
- **WHEN** se registra un pago menor al total
- **THEN** la factura permanece con saldo pendiente visible

#### Scenario: Pago total
- **WHEN** Σ pagos ≥ total
- **THEN** el estado pasa a `pagada` (RN008)…

#### Scenario: Sobrepago
- **IF** Σ pagos > total
- **THEN** se genera nota de crédito por el excedente (RN009) referenciando factura emitida (RN010)

### Requirement: Vencimiento automático (REQ-004)
#### Scenario: Marcar vencida
- **CUANDO** fechaVencimiento < hoy y estado ∈ {emitida, enviada}
- **EL SISTEMA DEBERÁ** transicionar a `vencida` (cron diario, RN007)

### Requirement: Anulación (REQ-005)
#### Scenario: Anular factura
- **WHEN** el emisor anula una factura emitida/enviada/vencida
- **THEN** queda `anulada` y el monto como crédito a favor del cliente (RN011)

### Requirement: Aislamiento (REQ-006)
- **ENTONCES** cada emisor SOLO ve sus facturas (RS001); el número es columna protegida no editable por frontend (RS002)
