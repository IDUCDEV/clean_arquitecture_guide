# Tasks: add-cart

## 1. Dominio
- [ ] 1.1 Crear entities Cart, CartItem, Coupon con cálculos puros (subtotal, impuesto 16%, descuento tope 50%, total)
      Rol: experto Flutter/Dart + Clean Architecture
      Éxito: RN004/RN006 cubiertos por unit test de invariantes
      Req: REQ-003 · Commit: `feat(cart): add cart entities with pricing rules`

- [ ] 1.2 Definir interface CartRepository (Either<Failure,T>, 5 métodos)
      Éxito: firmas idénticas a design.md · Compila en main sin impl
      Req: REQ-001..005 · Commit: `feat(cart): add repository contract`

- [ ] 1.3 UseCases: GetCart, AddItemToCart, RemoveItem, UpdateQuantity, ApplyCoupon
      Restricciones: un UseCase = una operación; validaciones de entrada aquí
      Éxito: mensajes exactos de los escenarios (RN001-RN006) en failures de dominio
      Req: REQ-001..004 · Commit: `feat(cart): add usecases`

## 2. Capa de datos
- [ ] 2.1 CartModel/CouponModel (snake_case ↔ camelCase, roundtrip fromJson/toJson)
      Éxito: roundtrip cubierto en test
      Req: REQ-001..004 · Commit: `feat(cart): add data models`

- [ ] 2.2 CartRemoteDataSource (supabase.rpc / .from, manejo AuthException/SocketException)
      Éxito: cada método lanza excepciones mapeables a Failure
      Req: REQ-001..005 · Commit: `feat(cart): add remote data source`

- [ ] 2.3 CartRepositoryImpl (mapeo excepciones → Failure, delega datasource)
      Éxito: test con mock datasource pasa
      Req: REQ-001..005 · Commit: `feat(cart): implement repository`

## 3. Estado y presentación
- [ ] 3.1 CartState sealed class (Initial/Loading/Loaded/Error)
      Commit: `feat(cart): add cart state`

- [ ] 3.2 CartCubit (transiciones + mensajes EXACTOS de los escenarios)
      Éxito: cada escenario REQ-001..006 tiene su transición probada
      Req: REQ-006 · Commit: `feat(cart): add cart cubit`

- [ ] 3.3 CartPage + widgets (un render por estado; SnackBar para errores)
      Éxito: widget test renderiza Loaded y Error correctamente
      Req: REQ-006 · Commit: `feat(cart): add cart page`

## 4. Integración
- [ ] 4.1 Migración 0007_carts_rls.sql (3 tablas + RPC add_cart_item + RLS)
      Restricciones: idempotente; no editar migraciones previas; RLS enable SIEMPRE
      Éxito: `supabase db reset` OK; políticas citan escenarios REQ-005
      Req: REQ-005 · Commit: `db(cart): add carts tables, rpc and rls`

- [ ] 4.2 Registros en service_locator.dart (datasource, repo, usecases ×5, cubit — lazy singletons/factory según patrón)
      Commit: `chore(di): register cart dependencies`

- [ ] 4.3 Ruta /cart en app_router.dart con guard de sesión
      Commit: `feat(router): add cart route`

## 5. Tests
- [ ] 5.1 Unit tests entities (bordes: stock 0, cantidad ≤0, cupón expirado, descuento >50%)
- [ ] 5.2 Test repository impl (mocks datasource; éxito + failure)
- [ ] 5.3 Widget test CartPage (estados Loading/Loaded/Error/vacío)

## Trazabilidad
| Req | Tarea(s) | Test | Cubre escenario |
|-----|----------|------|-----------------|
| REQ-001 | 1.1, 4.1, 2.2, 1.3 | entity_test | feliz/sin stock/límite/cantidad |
| REQ-002 | 1.2, 1.3 | repo_test | quitar item |
| REQ-003 | 1.1 | entity_test | resumen y vacío |
| REQ-004 | 1.3, 3.2 | cubit_test | cupón vigente/expirado/tope |
| REQ-005 | 4.1 | (política RLS) | aislamiento |
| REQ-006 | 3.1, 3.2, 3.3 | widget_test | estados UI |