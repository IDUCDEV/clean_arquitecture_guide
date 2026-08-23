# Design: add-delivery-seguimiento

## Context
Realtime-first. El GPS usa Broadcast (efímero, sin persistir cada punto); la asignación usa RPC transaccional.

## Goals / Non-Goals
- Goals: tracking fluido y privado; transiciones imposibles de corromper
- Non-Goals: pagos reales, calificaciones, re-asignación automática

## Decisions
### D1: Broadcast para GPS, tabla solo para "última ubicación"
- Decisión: canal `order:{id}` con Broadcast; `courier_locations` guarda el último punto para reconexiones
- Por qué: RT001 — Broadcast evita write-amplification en BD

### D2: Tarifa vía RPC PostGIS
- Decisión: `rpc.calcular_tarifa(origin, destination)` con `ST_DWithin/ST_Distance`
- Por qué: RT002 + RN005/RN012 en servidor (no manipulable)

### D3: Timeout con pg_cron + campo deadline
- Decisión: `accept_deadline` al crear; cron cada minuto cancela vencidos
- Por qué: RN003/RN004 sin dependencias externas

## Ficheros afectados (resumen)
| Elemento | Capa | Archivo |
|----------|------|---------|
| Order, OrderItem, Location (VO), CourierLocation | domain/entities | lib/features/delivery/domain/entities/ |
| OrderRepository, DeliveryRepository (con Streams) | domain/repositories | … |
| PlaceOrder, CancelOrder, AcceptOrder, MarkX ×4, WatchOrder, WatchRestaurantOrders, AcceptDelivery, UpdateLocation, CalculateFee | domain/usecases | … |
| Models, Remote+RealtimeDataSource, Impls | data | … |
| CustomerOrderCubit, RestaurantOrdersCubit, TrackingCubit (+states) | presentation/cubit | … |
| CheckoutPage, RestaurantOrdersPage, AvailableDeliveriesPage, TrackingMapPage | presentation/pages | … |
| Migración 0011 (orders + locations + RPCs + RLS + cron) | supabase/migrations | … |

## Contratos Dart clave
```dart
abstract interface class OrderRepository {
  Future<Either<Failure, Order>> placeOrder(PlaceOrderParams params);
  Future<Either<Failure, Order>> transition({required String orderId, required OrderEvent event});
  Stream<Either<Failure, Order>> watchOrder(String orderId);
}
abstract interface class DeliveryRepository {
  Future<Either<Failure, double>> calculateDeliveryFee(Location a, Location b);
  Future<Either<Failure, Unit>> updateLocation(String orderId, Location loc);
  Stream<Location> watchCourierLocation(String orderId);
}
sealed class TrackingState {}
class TrackingLive extends TrackingState { final Location courier; const TrackingLive(this.courier); }
```

## Flujo de datos (tracking)
```
TrackingCubit.start(orderId)
      ├─► watchOrder (Realtime: cambios de estado del pedido)
      └─► watchCourierLocation (Broadcast channel order:{id})
Repartidor: geolocator stream (3s) ──► UpdateLocation ──► broadcast + upsert último punto
Cliente: mapa pinta TrackingLive(courier) ──► entregado → cancelar suscripciones
```

## Backend Supabase
- orders(+status enum amplio, accept_deadline), order_items(check disponible), courier_locations
- RLS: cliente lee SU pedido; restaurante los SUyos; courier_locations write owner-only, read solo clientes con pedido activo de ese courier (policy por join)
- Realtime: habilitar broadcast; cron timeout

## Boundaries
No integrar pasarela real ni calificaciones aquí; GPS nunca persiste histórico completo (privacidad).
