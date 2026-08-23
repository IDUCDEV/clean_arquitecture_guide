# Design: add-facturacion

## Context
Máquina de estados regulada. La fuente de verdad de las transiciones es la BD; el dominio las replica para validación temprana y tests.

## Goals / Non-Goals
- Goals: cero estados inválidos; numeración sin huecos ni duplicados
- Non-Goals: recurrentes, plantillas, reportes

## Decisions
### D1: Transiciones en RPC transaccional
- Decisión: `rpc.emitir_factura`, `rpc.registrar_pago`, `rpc.anular` validan estado+reglas atómicamente; constraint CHECK de enum en BD
- Alternativa descartada: transiciones solo en Cubit (doble tap = doble pago)
- Por qué: concurrencia y auditoría

### D2: Número secuencial con contador por emisor
- Decisión: tabla `invoice_sequences(issuer_id, next_number)` actualizada dentro del mismo RPC; columna `number` generada server-side
- Por qué: RN001 + RT001 + RS002 (no editable desde cliente)

### D3: Estados como sealed class en domain
- Decisión: `InvoiceStatus` enum + guard `canTransitionTo()` puro
- Por qué: UI deshabilita acciones inválidas sin roundtrip

## Ficheros afectados (resumen)
| Elemento | Capa | Archivo |
|----------|------|---------|
| Invoice, InvoiceItem, Payment, CreditNote (+InvoiceStatus) | domain/entities | lib/features/invoicing/domain/entities/ |
| InvoiceRepository | domain/repositories | … |
| CreateInvoice, UpdateDraft, IssueInvoice, SendInvoice, RegisterPayment, CancelInvoice, ListInvoices | domain/usecases | … |
| Models, RemoteDataSource, Impl | data | … |
| InvoiceEditorCubit, InvoiceListCubit (+states) | presentation/cubit | … |
| InvoiceEditorPage, InvoiceListPage, InvoiceDetailPage | presentation/pages | … |
| Migración 0010 (tablas + sequences + RPCs + RLS + cron vencidas) | supabase/migrations | … |

## Contratos Dart clave
```dart
abstract interface class InvoiceRepository {
  Future<Either<Failure, Invoice>> createDraft(CreateInvoiceParams params);
  Future<Either<Failure, Invoice>> updateDraft(String id, UpdateInvoiceParams params);
  Future<Either<Failure, Invoice>> issue(String invoiceId);
  Future<Either<Failure, Invoice>> send(String invoiceId);
  Future<Either<Failure, PaymentResult>> registerPayment(RegisterPaymentParams params);
  Future<Either<Failure, Invoice>> cancel(String invoiceId, String reason);
  Future<Either<Failure, List<Invoice>>> listByIssuer({InvoiceStatus? status});
}
```

## Flujo de datos (registrar pago)
```
InvoiceDetailPage ──► InvoiceEditorCubit.pay(amount)
      ▼
RegisterPayment ──► rpc.registrar_pago(factura_id, monto)
      │ valida RN006 → insert payment → recalcula saldo
      ├─ saldo > 0 → Either.right(PartiallyPaid(saldo))
      └─ saldo ≤ 0 → pasa 'pagada'; si sobra crea credit_note (RN009/RN010)
      ▼
UI refresca estado y lista de pagos
```

## Backend Supabase
- invoices(+status enum check), invoice_items(check cantidad>0), payments, credit_notes, invoice_sequences
- RPC transaccionales ×3 + función cron `marcar_vencidas()`
- RLS issuer/cliente según tabla; number protegido (RS002)

## Boundaries
No implementar recurrentes ni plantillas en este cambio; no exponer número editable.
