# Proposal: add-facturacion

> Deriva del caso "Sistema de Facturación". Ejemplo Complejo: máquina de estados con transiciones reguladas.

## Impacto (Impact Report)
- Features afectadas: ninguna; feature nueva `invoicing`
- Reutilizable: patrón CRUD; formato de moneda en core
- Supabase: tablas `invoices`, `invoice_items`, `payments`, `credit_notes`; contador secuencial atómico
- DI / rutas: +2 cubits (editor, listado), +3 páginas
- Riesgos: números duplicados por concurrencia (RT001); estados inválidos por doble tap

## Why (Problema)
El negocio cobra sin trazabilidad: facturas manuales, pagos sin registro y vencimientos que nadie controla.

## What Changes (Solución)
Emisión de facturas con máquina de estados (borrador→emitida→enviada→pagada/vencida/anulada), pagos totales/parciales, notas de crédito por excedente y numeración secuencial por emisor.

## Capabilities
### New Capabilities
- `invoicing`: ciclo de vida completo de facturas y pagos

## Scope (Alcance)
**Incluye:** crear/editar borrador, emitir, enviar, registrar pagos parciales, vencimiento automático, anular con nota de crédito.
**No incluye:** facturas recurrentes (RN012 → MODIFIED futuro), plantillas, reportes financieros, validación fiscal externa.
**Dependencias:** catálogo de clientes, autenticación.
**Suposiciones:** IVA 21% nacional / 0% exportación (RN013).
**Preguntas abiertas:** ~~¿moneda múltiple?~~ → una sola moneda v1.

## Actores y permisos
| Actor | Puede | No puede | Mapeo RLS |
|-------|-------|----------|-----------|
| Emisor | CRUD SUS facturas/pagos | Ver facturas ajenas; editar número (RS002) | `auth.uid() = issuer_id` |
| Cliente | Ver estado de SUS facturas | Editar nada | `client_id = auth.uid()` |
| Cron | Marcar vencidas | — | security definer |

## Impact
- Código: ~16 ficheros en `lib/features/invoicing/`
- Datos: 4 tablas + RPC emitir/registrar_pago/marcar_vencidas
- Breaking changes: ninguno
