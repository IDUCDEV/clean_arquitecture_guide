# Tasks: add-delivery-seguimiento

## 1. Dominio y datos base
- [ ] 1.1 Entities + OrderStatus (9 estados) con transiciones por actor
- [ ] 1.2 Interfaces OrderRepository/DeliveryRepository (incl. Streams)
- [ ] 1.3 Migración 0011: tablas, RPCs tarifa/asignación, RLS, cron timeout

## 2. Capa de datos
- [ ] 2.1 Models roundtrip (Location VO ↔ PostGIS lat/lng)
- [ ] 2.2 RealtimeDataSource (watch order + broadcast GPS) y RemoteDataSource
- [ ] 2.3 UseCases ×10

## 3. Implementaciones y estado
- [ ] 3.1 RepositoryImpls
- [ ] 3.2 CustomerOrderCubit, RestaurantOrdersCubit, TrackingCubit
      Éxito: TrackingLive actualiza <3s; cancelación de streams al entregar

## 4. Presentación e integración
- [ ] 4.1 CheckoutPage, RestaurantOrdersPage, AvailableDeliveriesPage, TrackingMapPage
      Restricción: geolocator con permisos y battery-aware (pausa en background)
- [ ] 4.2 DI + rutas por rol

## 5. Tests
- [ ] 5.1 Unit: máquina de estados por actor; RN001/RN002/RN005/RN006/RN011/RN012
- [ ] 5.2 SQL: asignación concurrente (2 couriers), timeout cron, tarifa PostGIS
- [ ] 5.3 Widget: mapa con ubicación mock; estados del pedido

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 1.1, 1.3, 2.3 | unit+SQL |
| REQ-002 | 1.3 (cron) | integration |
| REQ-003 | 1.3, 2.3 | SQL asignación concurrente |
| REQ-004 | 2.2, 3.2, 4.1 | cubit+widget streams |
