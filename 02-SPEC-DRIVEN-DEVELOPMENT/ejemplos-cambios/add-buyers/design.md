# Design: add-buyers

## Context
Cambio pequeño sobre el módulo raffles existente. Complejidad Intermedia: design ligero, una puerta combinada.

## Goals / Non-Goals
- Goals: aprobación atómica e idempotente; búsqueda sin traer todo al cliente
- Non-Goals: notificaciones, pagos, edición de compradores

## Decisions
### D1: Aprobación y liberación vía RPC transaccional
- Decisión: `rpc.aprobar_tickets(buyer_id, ticket_ids[])` y `rpc.liberar_no_seleccionados(raffle_id)`
- Por qué: atomicidad (spec lo exige) y RLS respetada en servidor

### D2: Búsqueda con ilike en RPC
- Decisión: filtrado server-side (`nombre ilike %q% or telefono ilike %q%`)
- Por qué: consistencia con RT del módulo histórico — nunca filtrar listas grandes en cliente

## Ficheros afectados
| Elemento | Capa | Archivo |
|----------|------|---------|
| Buyer, TicketStatus | domain/entities | lib/features/buyers/domain/entities/buyer.dart |
| BuyerRepository | domain/repositories | …/domain/repositories/buyer_repository.dart |
| GetBuyers, ApproveTickets, ReleaseUnselected | domain/usecases | …/domain/usecases/ |
| BuyerModel | data/model | …/data/models/buyer_model.dart |
| BuyerRemoteDataSource | data/datasource | … |
| BuyerRepositoryImpl | data/repositories | … |
| BuyersCubit + BuyersState | presentation/cubit | … |
| BuyersPage (+search bar) | presentation/pages | …/presentation/pages/buyers_page.dart |
| DI + ruta anidada bajo raffles | core | service_locator.dart · app_router.dart |
| Migración 0012 (buyers + RPCs) | supabase/migrations | … |

## Contratos Dart clave
```dart
abstract interface class BuyerRepository {
  Future<Either<Failure, List<Buyer>>> getBuyers({required String raffleId, String? query});
  Future<Either<Failure, Unit>> approveTickets({required String buyerId, required List<String> ticketIds});
  Future<Either<Failure, Unit>> releaseUnselected({required String raffleId});
}
sealed class BuyersState {}
class BuyersLoaded extends BuyersState { final List<Buyer> buyers; const BuyersLoaded(this.buyers); }
```

## Flujo de datos (aprobar)
```
BuyersPage ──► BuyersCubit.approve(buyerId, ids)
      ▼
ApproveTickets ──► rpc.aprobar_tickets ──► UPDATE ... WHERE id = ANY(...) (transacción)
      ▼
Either.right(Unit) ──► recarga listado ──► BuyersLoaded
```

## Backend Supabase
- buyers(id, raffle_id→raffles, nombre, telefono)
- tickets ya existente: +estado enum(libre,vendido,aprobado); FK buyer opcional
- RPCs ×2 security definer; RLS organizador por join a raffles

## Boundaries
No tocar la feature raffles salvo la columna de estado indicada.
