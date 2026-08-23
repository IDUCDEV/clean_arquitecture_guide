# Spec: order-lifecycle + delivery-tracking

## WHY
El pedido necesita estados claros entre tres actores y el cliente necesita ver el avance en vivo.

## Purpose
Transiciones válidas por actor con timeouts regulados y streaming de ubicación privado.

## ADDED Requirements

### Requirement: Hacer y cancelar pedido (REQ-001)
#### Scenario: Pedido válido
- **WHEN** el cliente hace checkout con items disponibles dentro del radio de 5 km (RN011/RN012)
- **THEN** el pedido queda `pendiente` con tarifa = 1.5 €/km calculada server-side (RN005, RT002)

#### Scenario: Item no disponible
- **IF** algún item no está disponible
- **THEN** el sistema DEBERÁ mostrar "Producto no disponible" sin crear el pedido

#### Scenario: Cancelación tardía
- **IF** el estado ya no es `pendiente` ni `confirmado`
- **THEN** la cancelación DEBERÁ rechazarse (RN002)

### Requirement: Timeout del restaurante (REQ-002)
#### Scenario: Aceptación a tiempo
- **WHEN** el restaurante acepta dentro de los 3 minutos
- **THEN** el pedido pasa a `confirmado`

#### Scenario: Sin respuesta
- **IF** pasan 3 min en `pendiente`
- **THEN** el cron DEBERÁ cancelarlo automáticamente (RN004)

### Requirement: Asignación de repartidor (REQ-003)
#### Scenario: Repartidor acepta
- **WHEN** un repartidor a <2 km acepta (RN006) sin pedido activo (RN001)
- **THEN** queda asignado y el pedido pasa al flujo de entrega

#### Scenario: Doble pedido
- **IF** el repartidor tiene un pedido activo
- **THEN** el sistema DEBERÁ ocultar nuevos pedidos disponibles

### Requirement: Tracking GPS (REQ-004)
#### Scenario: Emisión periódica
- **MIENTRAS** haya pedido activo asignado
- **EL REPARTIDOR DEBERÁ** publicar su ubicación cada 3s vía Realtime Broadcast (RT001)

#### Scenario: Privacidad de ubicación
- **ENTONCES** solo el cliente de ESE pedido ve esa ubicación (RS001); el repartidor solo escribe la suya (RS002)

#### Scenario: Entrega
- **WHEN** se marca `entregado`
- **THEN** cesa la emisión GPS y se cierra el canal
