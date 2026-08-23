# Proposal: add-delivery-seguimiento

> Deriva del caso "App de Delivery". Ejemplo Complejo: multi-actor, realtime (GPS) y geolocalización.

## Impacto (Impact Report)
- Features afectadas: ninguna; feature nueva `delivery` (se asume catálogo restaurantes/menú existente)
- Reutilizable: auth por roles, patrón Either
- Supabase: tabla `orders` con máquina de estados amplia; Realtime Broadcast para GPS
- DI / rutas: +3 cubits (cliente, restaurante, repartidor), +4 páginas
- Riesgos: batería por frecuencia GPS; fugas de ubicación entre pedidos

## Why (Problema)
Los pedidos se coordinan por teléfono y el cliente no sabe dónde está su comida.

## What Changes (Solución)
Ciclo de pedido con estados (pendiente→…→entregado), aceptación/rechazo del restaurante con timeout 3 min, asignación de repartidor cercano, tarifa PostGIS y tracking GPS en tiempo real.

## Capabilities
### New Capabilities
- `order-lifecycle`: creación y transiciones de estado del pedido
- `delivery-tracking`: asignación y seguimiento GPS en vivo

## Scope (Alcance)
**Incluye:** hacer/cancelar pedido, flujo restaurante (aceptar/preparar/listo), flujo repartidor (aceptar/recoger/entregar), tarifa $1.5/km, tracking cada 3s.
**No incluye:** pasarela de pagos real (mock), calificaciones (RN008/009 → MODIFIED futuro), re-asignación automática completa (solo alerta RN010).
**Dependencias:** autenticación multi-rol, mapa (google_maps ya en pubspec).
**Suposiciones:** radio de entrega 5 km; repartidor emite GPS solo durante pedido activo.
**Preguntas abiertas:** ~~¿offline del repartidor?~~ → v1 requiere conexión.

## Actores y permisos
| Actor | Puede | No puede | Mapeo RLS |
|-------|-------|----------|-----------|
| Cliente | Pedir, cancelar en estados iniciales, rastrear SU pedido | Ver otros pedidos | `auth.uid() = customer_id` |
| Restaurante | Gestionar SU menú y pedidos entrantes | Cambiar estados post-recogido | `restaurant_id = auth.uid()` |
| Repartidor | Aceptar entregas, actualizar SU ubicación | Tener 2 pedidos activos (RN001) | locations: `auth.uid() = courier_id` |

## Impact
- Código: ~20 ficheros en `lib/features/delivery/`
- Datos: orders, order_items, courier_locations + RPC tarifa/asignación; channel realtime
- Breaking changes: ninguno
