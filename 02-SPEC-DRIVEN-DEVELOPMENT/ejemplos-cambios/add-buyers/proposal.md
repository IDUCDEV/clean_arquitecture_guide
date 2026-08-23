# Proposal: add-buyers

> Deriva del ejemplo "Gestión de compradores (Buyers)" del módulo histórico (contexto: app de rifas). Ejemplo **Simple→Intermedia**: CRUD con una regla de negocio.

## Impacto (Impact Report)
- Features afectadas: ninguna; feature nueva `buyers` sobre módulo `raffles`
- Reutilizable: patrón listado+search existente; auth organizador
- Supabase: tablas `buyers`, `tickets` (ya existe `raffles`)
- DI / rutas: +1 cubit, +1 página, +1 ruta `/raffles/:id/buyers`
- Riesgos: bajo — aprobación de tickets debe ser idempotente

## Why (Problema)
El organizador no puede gestionar quién compró tickets ni aprobar participantes seleccionados; todo vive en chats y notas sueltas.

## What Changes (Solución)
Listado de compradores por rifa con búsqueda por nombre/teléfono, aprobación de tickets seleccionados y liberación de los no seleccionados.

## Capabilities
### New Capabilities
- `buyers-management`: gestión de compradores y estados de ticket

## Scope (Alcance)
**Incluye:** listar compradores, buscar por nombre o teléfono, aprobar tickets, liberar no seleccionados.
**No incluye:** notificaciones, pagos, edición de datos del comprador.
**Dependencias:** autenticación (identidad del organizador), feature raffles.
**Suposiciones:** un comprador pertenece a una sola rifa.
**Preguntas abiertas:** ~~¿reaprobar un aprobado?~~ → idempotente, sin efecto; ~~¿aprobación atómica?~~ → SÍ, RPC transaccional.

## Actores y permisos
| Actor | Puede | No puede | Mapeo RLS |
|-------|-------|----------|-----------|
| Organizador | Ver/approbar/liberar tickets de SUS rifas | Ver rifas ajenas | `raffle.owner_id = auth.uid()` |
| Comprador | — (fuera de alcance v1) | — | — |

## Impact
- Código: ~9 ficheros en `lib/features/buyers/`
- Datos: buyers + FK a raffles; RPC aprobar/lote liberar
- Breaking changes: ninguno
