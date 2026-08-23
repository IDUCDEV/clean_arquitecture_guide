# Tasks: add-buyers

> Complejidad Intermedia: una sola puerta combinada antes de implementar (proposal+spec+design+tasks revisados juntos).

## 1. Dominio y datos base
- [ ] 1.1 Entity Buyer + TicketStatus enum
- [ ] 1.2 Interface BuyerRepository
- [ ] 1.3 Migración 0012: tabla buyers + RPCs ×2 + RLS por organizador

## 2. Capa de datos
- [ ] 2.1 BuyerModel roundtrip
- [ ] 2.2 RemoteDataSource (RPC + query con búsqueda server-side)
- [ ] 2.3 UseCases ×3

## 3. Implementación y estado
- [ ] 3.1 RepositoryImpl + BuyersCubit/State

## 4. Presentación e integración
- [ ] 4.1 BuyersPage con search bar y acciones aprobar/liberar
- [ ] 4.2 DI + ruta anidada /raffles/:id/buyers

## 5. Tests
- [ ] 5.1 Unit usecases (query vacía, ids vacíos → failure)
- [ ] 5.2 SQL: idempotencia de aprobación; RLS rifa ajena
- [ ] 5.3 Widget: listado, búsqueda, snackbars de resultado

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 1.3, 4.1 | SQL RLS |
| REQ-002 | 1.3, 2.2 | unit datasource |
| REQ-003 | 1.3, 2.3 | SQL idempotencia |
| REQ-004 | 1.3, 2.3 | SQL liberación |
