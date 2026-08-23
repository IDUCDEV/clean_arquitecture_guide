# Tasks: add-facturacion

## 1. Dominio y datos base
- [ ] 1.1 Entities + InvoiceStatus con canTransitionTo() (máquina de estados pura)
      Éxito: todas las transiciones válidas/inválidas cubiertas por unit test
- [ ] 1.2 Interface InvoiceRepository
- [ ] 1.3 Migración 0010: tablas, sequences, RPCs ×3, RLS, cron vencidas

## 2. Capa de datos
- [ ] 2.1 Models roundtrip (money como num; enums)
- [ ] 2.2 RemoteDataSource (RPC-first; sin UPDATE directo de estado desde cliente)
- [ ] 2.3 UseCases ×7

## 3. Implementaciones y estado
- [ ] 3.1 RepositoryImpl (mapeo errores SQL → Failure con mensajes RN00x)
- [ ] 3.2 EditorCubit/ListCubit + states sealed
      Éxito: doble tap en "pagar" no duplica pago (debounce + RPC idempotente)

## 4. Presentación e integración
- [ ] 4.1 Pages: editor (borrador), listado con filtros por estado, detalle con pagos
- [ ] 4.2 DI + rutas

## 5. Tests
- [ ] 5.1 Unit: máquina de estados completa + cálculo saldo/sobrepago
- [ ] 5.2 SQL: numeración concurrente (dos emisiones paralelas), pagos parciales→total
- [ ] 5.3 Widget: editor valida antes de emitir; detalle muestra saldo

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 1.1, 1.3 | unit+SQL numeración |
| REQ-002 | 1.1, 2.3 | unit transiciones |
| REQ-003 | 1.3, 2.3 | SQL pagos parciales/sobrepago |
| REQ-004 | 1.3 (cron) | integration |
| REQ-005 | 1.3, 2.3 | unit anulación |
| REQ-006 | 1.3 | SQL RLS |
