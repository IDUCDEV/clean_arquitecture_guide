# Práctica: Flujo de Datos del Carrito de Compras

> Diagrama el flujo completo del Carrito de Compras a través de todas las capas de Clean Architecture.

---

## Instrucciones

1. Toma tus contratos de la práctica anterior
2. En papel, dibuja el flujo de datos para cada operación del carrito
3. Incluye: tipos de datos, transformaciones entre capas, manejo de errores
4. Al final, compara con las soluciones sugeridas

---

## Enunciado

Para cada una de estas operaciones del Carrito, dibuja el flujo completo desde la UI hasta la API y de vuelta:

1. **Agregar producto** (`addProduct`)
2. **Quitar producto** (`removeProduct`)
3. **Aplicar cupón** (`applyCoupon`)
4. **Ver resumen** (`getCartSummary`)

Para cada flujo, incluye:
- El tipo de dato que viaja en cada paso
- Dónde se transforman los datos (Model → Entity, etc.)
- Dónde se manejan los errores
- Los estados del Cubit que se emiten

---

## Paso a Paso

### ✏️ Paso 1: Flujo Agregar Producto

Dibuja la secuencia desde que el usuario presiona "Agregar" hasta que ve el resultado.

**Incluye:**
1. Widget → Cubit (evento y estado inicial)
2. Cubit → UseCase (llamada y parámetros)
3. UseCase → Repository (validaciones y delegación)
4. Repository → DataSources (remoto y local)
5. DataSource → API (serialización)
6. API → DataSource → Repository → UseCase → Cubit (respuesta y transformaciones)
7. Cubit → Widget (nuevo estado)

**Marca en el diagrama:**
- ✅ Dónde se validan las reglas RN002 (stock) y RN003 (cantidad)
- ❌ Dónde se manejan los errores
- 🔄 Dónde se transforman los tipos

### ✏️ Paso 2: Flujo Quitar Producto

Similar al paso 1 pero para `removeProduct`. Nota las diferencias:

- ¿Qué validaciones aplican? (o no aplican)
- ¿El flujo es más simple? ¿Por qué?
- ¿Qué pasa si el producto no existe en el carrito?

### ✏️ Paso 3: Flujo Aplicar Cupón

Dibuja el flujo de `applyCoupon`. Incluye:

1. ¿Dónde se valida que el cupón no esté expirado? (RN005)
2. ¿Dónde se valida el descuento máximo? (RN006)
3. ¿El cupón se valida localmente o contra la API?
4. ¿Qué pasa si el cupón es inválido?

### ✏️ Paso 4: Flujo Ver Resumen

Para `getCartSummary`:

- ¿Este flujo usa remoto, local o ambos?
- ¿Cómo sería una estrategia offline-first para este caso?
- ¿Qué estados del Cubit aplican?

---

## Solución Sugerida

### ✅ Flujo Agregar Producto (detallado)

```
CAPA              TIPO                        QUÉ PASA
────              ────                        ────────
USUARIO           Tap en "Agregar"            Presiona botón en ProductCard

WIDGET            Product, int qty            onTap: cubit.addProduct(product, 1)

CUBIT             CartActionLoading           emit(CartActionLoading(cart: current))
                  (estado con cart actual)

                  AddProductToCart.call(
                    userId: u,                Llama al UseCase con parámetros
                    product: p,
                    quantity: 1
                  )

USECASE           VALIDA REGLAS:              RN002: product.stock > 0
                                               RN003: quantity > 0
                                               RN001: cart.items.length < 50

                  Si alguna falla:
                  → Left(InvalidQuantity|ProductOutOfStock|CartLimitExceeded)

                  Si todo ok:
                  → repository.addProduct(...)

REPOSITORY (INT)  CartRepository.addProduct(  Interface (no implementa nada)
                    userId, product, qty)

REPOSITORY (IMPL) CartEntity                  1. remoteDS.addItem(userId, itemData)
                                              2. localDS.cacheCart(userId, model)
                                              3. model.toEntity() → Cart
                                              4. Right(cart)

DATASOURCE        CartModel                   remoteDS.addItem() → POST a Supabase
(REMOTE)                                       CartModel.fromJson(response)

DATASOURCE        void                        localDS.cacheCart(userId, model)
(LOCAL)                                        Guarda en SQLite/Hive

API SUPABASE      JSON                        POST /carts/{userId}/items
                                               Retorna CartModel como JSON

  ────────────────── VUELTA ──────────────────

DATASOURCE        CartModel                   Modelo deserializado

REPOSITORY        Cart (Entity)               cartModel.toEntity()

USECASE           Right(Cart)                 Propaga el Cart al Cubit

CUBIT             CartLoaded(cart: updated)   fold(): éxito → CartLoaded
                                               error → CartError(mensaje)

WIDGET            Rebuild con                  Muestra item en lista,
                  CartLoaded.cart              actualiza totales

USUARIO           Ve el producto               UI actualizada
                  en su carrito
```

### ✅ Flujo Quitar Producto (simplificado)

```
USUARIO     → Tap "Eliminar" en item del carrito
WIDGET      → cubit.removeProduct(productId)
CUBIT       → emit(CartActionLoading(cart: current, loadingItemId: id))
USECASE     → RemoveProductFromCart.call(userId, productId)
               → Sin reglas extra (cualquier producto se puede quitar)
REPOSITORY  → repository.removeProduct(userId, productId)
REPO IMPL   → remoteDS.removeItem(userId, productId)
               → localDS.cacheCart(userId, updatedModel)
               → model.toEntity()
CUBIT       → fold()
               → éxito: CartLoaded(cart: cartWithoutItem)
               → error: CartError("No se pudo eliminar el producto")
WIDGET      → Rebuild sin el item
```

**Diferencia clave:** Al quitar un producto no hay validaciones de negocio. El flujo es más directo.

### ✅ Flujo Aplicar Cupón

```
USUARIO     → Escribe código de cupón → Tap "Aplicar"
WIDGET      → cubit.applyCoupon(code)
CUBIT       → emit(CartActionLoading(cart: current))
USECASE     → ApplyCoupon.call(userId, code)
               → Valida: couponCode no vacío
               → repository.applyCoupon(userId, code)
REPO IMPL   → remoteDS.applyCoupon(userId, code)   ← La API valida el cupón
               → La API retorna error si expiró (RN005)
               → La API retorna error si descuento > 50% (RN006)
               → localDS.cacheCart(userId, model)
               → model.toEntity()
CUBIT       → fold()
               → éxito: CartLoaded(cart: cartWithDiscount)
               → error: CartError(mensaje: "Cupón expirado" | "Cupón inválido")
WIDGET      → Muestra descuento aplicado y total actualizado
```

**Nota importante:** Las reglas RN005 y RN006 se validan del lado del servidor (API). El UseCase podría también tener una validación local del formato del código como precaución.

### ✅ Flujo Ver Resumen (Offline-First)

```
USUARIO     → Navega a la pantalla del carrito
WIDGET      → CartPage.initState() → cubit.fetchCart()
CUBIT       → emit(CartLoading)
USECASE     → GetCartSummary.call(userId)
REPO IMPL   → ESTRATEGIA OFFLINE-FIRST:
               1. localDS.getCachedCart(userId)  ← Responde inmediato
               2. En paralelo: remoteDS.fetchCart(userId)
               3. Si remote ok → localDS.cacheCart() → retorna remoto
               4. Si remote fail → retorna lo que tenía del caché
CUBIT       → fold()
               → éxito: CartLoaded(cart)
               → error: CartError("No se pudo cargar el carrito")
WIDGET      → Muestra lista de items, totales, input de cupón
```

---

## Verificación: Lista de chequeo

- [ ] ¿Cada flujo muestra el tipo de dato en cada paso?
- [ ] ¿Las transformaciones Model ↔ Entity están marcadas?
- [ ] ¿El manejo de errores está cubierto en cada capa?
- [ ] ¿Los estados del Cubit se emiten en los momentos correctos?
- [ ] ¿Las validaciones de negocio están en el UseCase (no en otra capa)?
- [ ] ¿El DataSource remoto usa Models, no Entities?
- [ ] ¿El flujo offline-first está considerado donde aplica?
- [ ] ¿Se evaluó si la pantalla necesita realtime (Streams)? (ver [05e-diseno-supabase.md](./05e-diseno-supabase.md))
- [ ] ¿Los diagramas son claros para alguien que no conoce el código?

---

## 🚀 Siguiente paso

Ahora que dominas el flujo de datos, enfrenta el [caso completo](./05-caso-completo-reservas.md): diseña desde cero un Sistema de Reservas aplicando todo lo aprendido.

---

**Tiempo:** 30 minutos  
**Material:** Papel y lápiz + contratos de la práctica anterior
