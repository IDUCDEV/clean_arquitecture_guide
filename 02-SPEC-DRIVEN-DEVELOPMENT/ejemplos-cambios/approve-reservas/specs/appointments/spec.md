# Spec: appointments

## WHY
Sin agenda digital hay colas, ausencias y doctores sin visibilidad de su día.

## Purpose
Garantizar citas únicas por slot (sin dobles reservas), con reglas de antelación y aislamiento estricto entre dueños.

## ADDED Requirements

### Requirement: Agendar cita (REQ-001)
El sistema creará citas validando disponibilidad, antelación y límites.

#### Scenario: Slot libre con antelación suficiente
- **WHEN** el dueño agenda un slot libre con ≥4h de antelación
- **THEN** la cita DEBERÁ quedar `scheduled` con duración según tipo de consulta

#### Scenario: Doble reserva concurrente
- **IF** dos dueños agendan el mismo slot simultáneamente
- **THEN** el RPC DEBERÁ aceptar solo el primero y rechazar al segundo con "slot_ocupado"

#### Scenario: Antelación insuficiente
- **IF** faltan menos de 4 horas para el slot
- **THEN** el sistema DEBERÁ mostrar "Debes agendar con al menos 4 horas de antelación"

#### Scenario: Límite diario del doctor
- **IF** el doctor ya tiene 8 citas ese día
- **THEN** el sistema DEBERÁ mostrar "El doctor alcanzó su límite de citas diarias"

#### Scenario: Dos consultas el mismo día
- **IF** la mascota ya tiene una cita ese día
- **THEN** el sistema DEBERÁ mostrar "Ya existe una consulta para esta mascota ese día"

### Requirement: Cancelar cita (REQ-002)
#### Scenario: Cancelación con antelación
- **WHEN** el dueño cancela con ≥2h de antelación
- **THEN** la cita pasa a `cancelled`, se libera el slot y se notifica al doctor

#### Scenario: Fuera de plazo
- **IF** faltan menos de 2 horas
- **THEN** el sistema DEBERÁ mostrar "Solo puedes cancelar hasta 2 horas antes"

### Requirement: Gestión del día del doctor (REQ-003)
#### Scenario: Marcar completada / no-show
- **WHEN** el doctor marca la cita como `completed` o `no_show` (pasados 15 min)
- **THEN** la transición DEBERÁ registrarse con timestamp del actor

#### Scenario: Agenda en vivo
- **MIENTRAS** el doctor tiene la agenda abierta
- **EL SISTEMA DEBERÁ** reflejar nuevas citas/cancelaciones vía realtime

### Requirement: Aislamiento de datos (REQ-004)
#### Scenario: Dueño consulta sus citas
- **GIVEN** un dueño autenticado
- **WHEN** lista sus citas
- **THEN** solo recibe las de mascotas donde `owner_id = auth.uid()` (RLS)

### Requirement: Recordatorio 24h (REQ-005)
#### Scenario: Recordatorio enviado
- **CUANDO** falten 24h para una cita `scheduled`
- **EL SISTEMA DEBERÁ** enviar notificación al dueño y marcar el recordatorio como enviado
