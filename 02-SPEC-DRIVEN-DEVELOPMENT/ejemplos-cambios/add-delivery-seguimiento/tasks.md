# Tasks: add-delivery-seguimiento

## 1. Dominio
- [ ] 1.1 Entities + OrderStatus (9 estados) con transiciones por actor
- [ ] 1.2 Interfaces OrderRepository/DeliveryRepository (incl. Streams)
- [ ] 1.3 UseCases ×10

## 2. Capa de datos + Backend Supabase
- [ ] 2.1 Migración 0011: tablas, RPCs tarifa/asignación, RLS, cron timeout
- [ ] 2.2 Models roundtrip (Location VO ↔ PostGIS lat/lng)
- [ ] 2.3 RealtimeDataSource (watch order + broadcast GPS) y RemoteDataSource
- [ ] 2.4 RepositoryImpls

## 3. Estado y presentación
- [ ] 3.1 CustomerOrderCubit, RestaurantOrdersCubit, TrackingCubit
      Éxito: TrackingLive actualiza <3s; cancelación de streams al entregar
- [ ] 3.2 CheckoutPage, RestaurantOrdersPage, AvailableDeliveriesPage, TrackingMapPage
      Restricción: geolocator con permisos y battery-aware (pausa en background)

## 4. Integración
- [ ] 4.1 DI + rutas por rol

## 5. Tests
- [ ] 5.1 Unit: máquina de estados por actor; RN001/RN002/RN005/RN006/RN011/RN012
- [ ] 5.2 SQL: asignación concurrente (2 couriers), timeout cron, tarifa PostGIS
- [ ] 5.3 Widget: mapa con ubicación mock; estados del pedido

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 1.1, 1.3, 2.1 | unit+SQL |
| REQ-002 | 2.1 (cron) | integration |
| REQ-003 | 2.1, 1.3 | SQL asignación concurrente |
| REQ-004 | 2.3, 3.1, 3.2 | cubit+widget streams |