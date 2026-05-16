# Flujo de Datos entre Capas

> Diseña cómo viajan los datos a través de las capas de Clean Architecture. De la UI a la base de datos y de vuelta.

---

## El Viaje de los Datos

Cada operación en Clean Architecture sigue un flujo en forma de **U**:

```
                        ┌──────────────────┐
                        │     USUARIO      │
                        │   (interacción)  │
                        └────────┬─────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────┐
│                PRESENTATION                       │
│  ┌──────────┐    ┌──────────┐                    │
│  │  Widget  │───▶│  Cubit   │                    │
│  │ (tap)    │    │ (evento) │                    │
│  └──────────┘    └────┬─────┘                    │
└───────────────────────┼──────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────┐
│                   DOMAIN                          │
│  ┌──────────┐    ┌──────────┐    ┌────────────┐  │
│  │ UseCase  │───▶│  Entity  │    │ Repository │  │
│  │(orquesta)│    │(modela)  │    │ (interface)│  │
│  └──────────┘    └──────────┘    └─────┬──────┘  │
└───────────────────────────────────────┼──────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────┐
│                     DATA                          │
│  ┌──────────────┐    ┌────────────────────┐      │
│  │  Repository  │───▶│  DataSource(s)     │      │
│  │  (impl)      │    │  ┌──────┐┌──────┐  │      │
│  │              │    │  │Remote││Local │  │      │
│  │              │    │  └──┬───┘└──┬───┘  │      │
│  └──────────────┘    └─────┼───────┼──────┘      │
└────────────────────────────┼───────┼──────────────┘
                             │       │
                             ▼       ▼
                     ┌──────────┐ ┌──────────┐
                     │   API    │ │  Caché   │
                     │Supabase  │ │  SQLite  │
                     └──────────┘ └──────────┘
```

---

## Secuencia Completa: Agregar Producto al Carrito

```
USUARIO                  PRESENTATION              DOMAIN                    DATA                  SUPABASE
  │                          │                       │                        │                      │
  │  Tap "Agregar"           │                       │                        │                      │
  │─────────────────────────▶│                       │                        │                      │
  │                          │                       │                        │                      │
  │                          │  cubit.addProduct()   │                        │                      │
  │                          │──────────────────────▶│                        │                      │
  │                          │                       │                        │                      │
  │                          │         ¡VALIDACIONES DEL USECASE!             │                      │
  │                          │  quantity > 0         │                        │                      │
  │                          │  product.stock > 0    │                        │                      │
  │                          │  cart.items < 50      │                        │                      │
  │                          │                       │                        │                      │
  │                          │  repository.addProduct()                       │                      │
  │                          │───────────────────────────────────────────────▶│                      │
  │                          │                       │                        │                      │
  │                          │                       │  remoteDS.addItem()    │                      │
  │                          │                       │───────────────────────────────────────────────▶│
  │                          │                       │                        │                      │
  │                          │                       │                        │            POST /cart
  │                          │                       │                        │                      │
  │                          │                       │              CartModel ←───────── JSON ──────│
  │                          │                       │                        │                      │
  │                          │                       │  localDS.cacheCart()   │                      │
  │                          │                       │───────────────────────▶│                      │
  │                          │                       │                        │                      │
  │                          │    Right(Cart)        │                        │                      │
  │                          │◀──────────────────────────────────────────────│                      │
  │                          │                       │                        │                      │
  │                          │  emit(CartLoaded)     │                        │                      │
  │                          │                       │                        │                      │
  │     UI actualizada       │                       │                        │                      │
  │◀─────────────────────────│                       │                        │                      │
  │                          │                       │                        │                      │
```

---

## Mapeo de Tipos entre Capas

Cada capa usa sus propios tipos. Nunca pasa un `Model` a la UI ni una `Entity` al DataSource.

```
CAPA             TIPO DE ENTRADA      TIPO DE SALIDA
─────────────────────────────────────────────────────
Widget           UserAction           Event (a Cubit)
Cubit            Event                Call UseCase
UseCase          Input params         Either<Failure, Entity>
Repository       Domain params        Either<Failure, Entity>
  (interface)
RepositoryImpl   Domain params        Either<Failure, Entity>
DataSource       Model params         Model
API/DB           JSON/SQL             JSON/Row
```

**Regla de transformación:**

```
PRESENTATION                          DOMAIN                           DATA
┌─────────┐                          ┌────────┐                      ┌─────────┐
│  Cart   │                          │  Cart  │                      │  Cart   │
│  State  │                          │Entity  │                      │  Model  │
└─────────┘                          └────────┘                      └─────────┘
     │                                    │                               │
     │  state.cart.total                  │                               │
     │                                    │                               │
     │           Entity → Model           │                               │
     │    ┌───────────────────────────────┘                               │
     │    │   CartModel.fromEntity(cart)                                  │
     │    │                                                               │
     │    │                    Model → Entity                             │
     │    │          ┌────────────────────────────────────────────────────┘
     │    │          │  cartModel.toEntity()
     │    │          │
     ▼    ▼          ▼
  UI lee       UseCase opera         DataSource serializa
  atributos    con objetos           a JSON para la API
  de Entity    de negocio puros
```

---

## Ejemplo: Flujo de ApplyCoupon

### 1. Widget detecta acción

```dart
// El usuario escribe un código de cupón y presiona "Aplicar"
onPressed: () => cubit.applyCoupon(codeController.text)
```

### 2. Cubit orquesta

```dart
void applyCoupon(String code) async {
  emit(CartActionLoading(cart: state.cart));

  final result = await _applyCouponUseCase(
    userId: userId,
    couponCode: code,
  );

  result.fold(
    (failure) => emit(CartError(_mapFailureToMessage(failure))),
    (cart) => emit(CartLoaded(cart: cart)),
  );
}
```

### 3. UseCase valida reglas

```dart
Future<Either<Failure, Cart>> call({
  required String userId,
  required String couponCode,
}) async {
  // R005: Cupón vigente
  if (couponCode.isEmpty) return Left(InvalidCoupon());

  // Delega la validación de expiración al repositorio
  return repository.applyCoupon(
    userId: userId,
    couponCode: couponCode,
  );
}
```

### 4. RepositoryImpl orquesta fuentes

```dart
Future<Either<Failure, Cart>> applyCoupon({
  required String userId,
  required String couponCode,
}) async {
  try {
    // 1. Llama al remoto
    final cartModel = await remoteDataSource.applyCoupon(userId, couponCode);

    // 2. Actualiza caché local
    await localDataSource.cacheCart(userId, cartModel);

    // 3. Convierte a entidad y retorna
    return Right(cartModel.toEntity());
  } on CartException catch (e) {
    return Left(CouponError(e.message));
  }
}
```

### 5. DataSource llama a la API

```dart
Future<CartModel> applyCoupon(String userId, String couponCode) async {
  final response = await supabase
    .from('carts')
    .update({'coupon_code': couponCode})
    .eq('user_id', userId)
    .select()
    .single();

  return CartModel.fromJson(response);
}
```

---

## Flujo de Errores

Los errores también fluyen de abajo arriba:

```
API/Supabase
    │
    │   Lanza excepción (formato inválido, 500, etc.)
    ▼
DataSource
    │
    │   Captura excepción → Retorna Failure del dominio
    ▼
RepositoryImpl
    │
    │   Propaga el Failure (puede agregar contexto)
    ▼
UseCase
    │
    │   Propaga el Failure (puede enriquecer con reglas)
    ▼
Cubit
    │
    │   fold() → Mapea Failure a mensaje de UI
    ▼
Widget
    │
    │   Muestra SnackBar/Dialog con el mensaje
    ▼
Usuario
```

**Regla:** Nunca dejes que una excepción técnica (HTTP 500, timeout, SQL error) llegue a la UI. Cada capa traduce el error al nivel de abstracción correspondiente.

---

## Estrategias de Flujo

### Flujo Síncrono (lectura de caché)

```
Widget → Cubit → UseCase → Repository → LocalDataSource → SQLite
                                                              │
                                                              ▼
Widget ← Cubit ← UseCase ← Repository ← LocalDataSource  ← Datos
```

### Flujo con Red (escritura remota + caché)

```
Widget → Cubit → UseCase → Repository ──→ RemoteDataSource ──→ API
                                        │                        │
                                        │                        ▼
                                        │ ←─── Cache local ←── Éxito
                                        │
                                        └──→ LocalDataSource → SQLite
```

### Flujo Offline-First

```
Widget → Cubit → UseCase → Repository ──→ LocalDataSource ──→ Caché
                                        │                        │
                                        │                        ▼
                                        │ ←─── Data local  ←── Datos
                                        │
                                        └──→ RemoteDataSource → API (en background)
```

---

## Diagrama de Estados del Carrito

```
                  ┌──────────────┐
                  │  CartInitial │
                  └──────┬───────┘
                         │
                    fetchCart()
                         │
                         ▼
                  ┌──────────────┐
           ┌──────│  CartLoading │──────┐
           │      └──────┬───────┘      │
           │             │              │
           │        éxito│              │error
           │             ▼              │
           │      ┌───────────┐         ▼
           │      │CartLoaded │   ┌──────────┐
           │      │           │   │CartError │
           │      └──────┬────┘   └──────────┘
           │             │              │
           │     acción  │              │ reintentar
           │             ▼              │
           │      ┌──────────────┐      │
           └──────│CartAction    │──────┘
                  │Loading       │
                  └──────────────┘
```

---

## 🚀 Siguiente paso

Ve a la [práctica de flujo de datos](./04a-practica-carrito-flujo.md) y diagrama el flujo completo del Carrito de Compras.

---

**Tiempo estimado de lectura:** 25 minutos  
**Tiempo estimado de práctica:** 30 minutos
