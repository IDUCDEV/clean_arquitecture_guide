# Spec: buyers-management

## WHY
El organizador necesita una vista única de compradores para decidir qué tickets quedan confirmados.

## Purpose
Listado filtrable con acciones de aprobación/liberación seguras e idempotentes.

## ADDED Requirements

### Requirement: Listar compradores (REQ-001)
#### Scenario: Listado por rifa
- **WHEN** el organizador abre los compradores de su rifa
- **THEN** ve nombre, teléfono, cantidad de tickets y estado

#### Scenario: Rifa ajena
- **IF** la rifa no pertenece al organizador autenticado
- **THEN** Supabase DEBERÁ devolver vacío vía RLS

### Requirement: Buscar compradores (REQ-002)
#### Scenario: Búsqueda por prefijo
- **CUANDO** el organizador escribe ≥3 caracteres
- **EL SISTEMA DEBERÁ** filtrar por nombre o teléfono (búsqueda delegada al backend)

### Requirement: Aprobar tickets (REQ-003)
#### Scenario: Aprobación exitosa
- **WHEN** el organizador aprueba los tickets seleccionados de un comprador
- **THEN** pasan a `aprobado` en una transacción atómica (RPC)

#### Scenario: Re-aprobación idempotente
- **IF** el ticket ya estaba aprobado
- **THEN** la operación DEBERÁ no tener efecto ni error

### Requirement: Liberar tickets (REQ-004)
#### Scenario: Liberación masiva
- **WHEN** el organizador libera los tickets NO seleccionados
- **THEN** solo esos pasan a `libre` y quedan disponibles para venta
