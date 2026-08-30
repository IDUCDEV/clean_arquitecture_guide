# Tasks: add-buyers

> Complejidad Intermedia: una sola puerta combinada antes de implementar (proposal+spec+design+tasks revisados juntos).

## 1. Dominio
- [ ] 1.1 Entity Buyer + TicketStatus enum
- [ ] 1.2 Interface BuyerRepository
- [ ] 1.3 UseCases ×3

## 2. Capa de datos + Backend Supabase
- [ ] 2.1 Migración 0012: tabla buyers + RPCs ×2 + RLS por organizador
- [ ] 2.2 BuyerModel roundtrip
- [ ] 2.3 RemoteDataSource (RPC + query con búsqueda server-side)
- [ ] 2.4 BuyerRepositoryImpl (mapeo excepciones → Failure)

## 3. Estado y presentación
- [ ] 3.1 BuyersState sealed + BuyersCubit
- [ ] 3.2 BuyersPage con search bar y acciones aprobar/liberar

## 4. Integración
- [ ] 4.1 DI + ruta anidada /raffles/:id/buyers

## 5. Tests
- [ ] 5.1 Unit usecases (query vacía, ids vacíos → failure)
- [ ] 5.2 SQL: idempotencia de aprobación; RLS rifa ajena
- [ ] 5.3 Widget: listado, búsqueda, snackbars de resultado

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 2.1, 3.2 | SQL RLS |
| REQ-002 | 2.1, 2.3 | unit datasource |
| REQ-003 | 2.1, 1.3 | SQL idempotencia |
| REQ-004 | 2.1, 1.3 | SQL liberación |