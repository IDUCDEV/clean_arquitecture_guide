# Mapeo a Capas de Clean Architecture

> Cómo traducir tu descomposición FADER a las capas de Clean Architecture. El puente entre el problema y la solución técnica.

---

## La Matriz de Responsabilidades

Cada pieza de tu descomposición FADER cae en una capa específica. Esta matriz te dice dónde va cada cosa:

```
┌────────────────────────────────────────────────────────────┐
│                     MAPEO FADER → CLEAN                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  FADER           │  CAPA           │  EJEMPLO              │
│──────────────────┼─────────────────┼───────────────────────│
│  Entidades       │  DOMAIN         │  Producto, Carrito    │
│                  │  (entities/)    │                       │
│──────────────────┼─────────────────┼───────────────────────│
│  Reglas          │  DOMAIN         │  R001, R002, R004     │
│  (validación)    │  (usecases/)    │                       │
│──────────────────┼─────────────────┼───────────────────────│
│  Operaciones     │  DOMAIN         │  AgregarProducto      │
│  (casos de uso)  │  (usecases/)    │  CalcularTotal        │
│──────────────────┼─────────────────┼───────────────────────│
│  Contratos       │  DOMAIN         │  CarritoRepository    │
│  (interfaces)    │  (repositories/)│  PagoService          │
│──────────────────┼─────────────────┼───────────────────────│
│  Fuentes de      │  DATA           │  CarritoRemoteDS      │
│  datos           │  (datasources/) │  CarritoLocalDS       │
│──────────────────┼─────────────────┼───────────────────────│
│  Modelos         │  DATA           │  CarritoModel         │
│  (DTOs/JSON)     │  (models/)      │  ProductoModel        │
│──────────────────┼─────────────────┼───────────────────────│
│  Implementación  │  DATA           │  CarritoRepositoryImpl│
│  de contratos    │  (repositories/)│                       │
│──────────────────┼─────────────────┼───────────────────────│
│  Estados de UI   │  PRESENTATION   │  CarritoState         │
│                  │  (cubit/)       │                       │
│──────────────────┼─────────────────┼───────────────────────│
│  Widgets         │  PRESENTATION   │  CarritoPage          │
│                  │  (pages/)       │  ItemCarritoTile      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Regla Fundamental

Cada elemento de FADER se mapea a **UNA Y SOLO UNA** capa. Si algo podría ir en dos capas, es señal de que tu descomposición no es precisa.

```
❌ MAL: "La validación de stock se hace en el UseCase y también en el Widget"
    → La lógica de negocio siempre pertenece a DOMAIN. La UI solo muestra el resultado.

✅ BIEN: "La validación de stock ocurre en el UseCase. El Widget muestra el error si ocurre."
```

---

## Proceso de Mapeo

### Paso 1: Entidades y Reglas → Domain

Todo lo que es **regla de negocio** o **concepto del mundo real** va a DOMAIN. Esta capa no depende de nada externo.

```
┌─────────────────────────────────────────────────────┐
│  DOMAIN                                              │
│                                                      │
│  entities/                                           │
│  ├── product.dart          ← De tu tarjeta Producto  │
│  ├── cart.dart             ← De tu tarjeta Carrito   │
│  ├── cart_item.dart        ← De tu tarjeta Item      │
│  └── coupon.dart           ← De tu tarjeta Cupón     │
│                                                      │
│  usecases/                                           │
│  ├── add_product_to_cart      ← R002, R003           │
│  ├── remove_product_from_cart ← sin reglas extra     │
│  ├── update_product_qty       ← R003                 │
│  ├── get_cart_summary         ← R004                 │
│  ├── apply_coupon             ← R005, R006           │
│  └── validate_stock           ← R002                 │
│                                                      │
│  repositories/  ← INTERFACES (contratos)            │
│  └── cart_repository.dart                            │
│                                                      │
│  services/  ← INTERFACES (contratos)                │
│  └── payment_service.dart                            │
│                                                      │
│  core/                                               │
│  └── failures.dart   ← Errores del dominio           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Pregunta de validación:** ¿Podría este código vivir en un proyecto Dart sin Flutter?
- ✅ Sí → Va en DOMAIN
- ❌ No (usa contexto de Flutter, depends de paquetes externos) → Va en otra capa

### Paso 2: Contratos → Domain (interfaces)

Los **repositorios y servicios** se definen como interfaces abstractas en DOMAIN. Esto es clave: DOMAIN define qué necesita, DATA lo implementa.

```dart
// DOMAIN define el contrato
abstract class CartRepository {
  Future<Either<Failure, Cart>> getCart(String userId);
  Future<Either<Failure, Cart>> addProduct(Product product, int quantity);
  Future<Either<Failure, Cart>> removeProduct(String productId);
  Future<Either<Failure, Cart>> updateQuantity(String productId, int quantity);
  Future<Either<Failure, Cart>> applyCoupon(String couponCode);
}
```

**Regla:** El `CartRepository` es una interface. DOMAIN no sabe ni le importa si los datos vienen de Supabase, Firebase, SQLite o un archivo JSON.

### Paso 3: Fuentes de Datos → Data

Lo que en FADER identificaste como **sistemas externos** (APIs, BD local, etc.) se convierte en DataSources en la capa DATA.

```
┌─────────────────────────────────────────────────────┐
│  DATA                                                │
│                                                      │
│  datasources/                                        │
│  ├── cart_remote_data_source.dart  ← API/Supabase   │
│  └── cart_local_data_source.dart   ← SQLite/Hive    │
│                                                      │
│  models/  ← DTOs que mapean desde/hacia JSON        │
│  ├── cart_model.dart                                 │
│  ├── product_model.dart                              │
│  └── coupon_model.dart                               │
│                                                      │
│  repositories/  ← Implementaciones                  │
│  └── cart_repository_impl.dart                       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

**Regla:** DATA implementa las interfaces de DOMAIN. DATA depende de DOMAIN, no al revés.

### Paso 4: Estados y Widgets → Presentation

Lo que en FADER identificaste como **interacción del usuario** se mapea a Presentation.

```
┌─────────────────────────────────────────────────────┐
│  PRESENTATION                                        │
│                                                      │
│  cubit/                                              │
│  ├── cart_cubit.dart                                 │
│  └── cart_state.dart   ← Estados de la UI           │
│                                                      │
│  pages/                                              │
│  ├── cart_page.dart                                  │
│  └── cart_summary_page.dart                          │
│                                                      │
│  widgets/                                            │
│  ├── cart_item_tile.dart                             │
│  ├── coupon_input.dart                               │
│  └── cart_total_card.dart                            │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Ejemplo Completo de Mapeo

```
FADER: "Como cliente, quiero agregar un producto al carrito"

DOMAIN
├── entity: Product (id, name, price, stock)
├── entity: CartItem (product, quantity, unitPrice)
├── entity: Cart (items, subtotal, discount, tax, total)
├── usecase: AddProductToCart
│   ├── Llama a CartRepository.addProduct()
│   ├── Valida R002 (stock)
│   └── Valida R003 (cantidad > 0)
├── interface: CartRepository
│   └── Future<Either<Failure, Cart>> addProduct(Product, int qty)
└── failure: AddProductFailure

DATA
├── model: CartModel (fromJson, toJson)
├── model: ProductModel (fromJson, toJson)
├── datasource: CartRemoteDataSource
│   └── Llama a Supabase REST API
├── repository: CartRepositoryImpl
│   └── Implementa CartRepository usando CartRemoteDataSource

PRESENTATION
├── state: CartState (loading, loaded, error, addingProduct)
├── cubit: CartCubit
│   └── addProduct() → Llama a AddProductToCart → Emite nuevo estado
├── page: CartPage
│   └── Botón "Agregar" → CartCubit.addProduct()
└── widget: ProductCard
    └── onTap → CartCubit.addProduct(product)
```

---

## Errores comunes de mapeo

| Error | Síntoma | Solución |
|-------|---------|----------|
| Entidad con lógica de serialización | `Producto.fromJson()` en DOMAIN | `fromJson` va en Model (DATA) |
| UseCase que llama a la API directamente | `supabaseClient.from(...)` en UseCase | El UseCase no sabe de dónde vienen los datos. Usa Repository. |
| Estado del Cubit que contiene widgets | `buttonEnabled`, `showSuccessDialog` en Estado | El estado describe datos, no widgets |
| Regla de negocio en el Widget | if(product.stock == 0) dentro de un Text | Las reglas van en UseCase, no en UI |
| Interfaz de Repository en DATA | `abstract class CartRepository` en DATA | La interface pertenece a DOMAIN |

---

## Plantilla de Mapeo Rápido

Usa esta tabla para mapear cualquier feature:

| Elemento FADER | Capa | Archivo destino |
|----------------|------|-----------------|
| Entidad tal | DOMAIN entities/ | `entidad.dart` |
| Operación tal | DOMAIN usecases/ | `operacion.dart` |
| Regla tal | DOMAIN usecases/ | (dentro de su UseCase) |
| Interface de repositorio | DOMAIN repositories/ | `repo.dart` |
| Modelo/DTO | DATA models/ | `modelo_model.dart` |
| Fuente de datos remota | DATA datasources/ | `remote_ds.dart` |
| Fuente de datos local | DATA datasources/ | `local_ds.dart` |
| Implementación de repo | DATA repositories/ | `repo_impl.dart` |
| Estado de UI | PRESENTATION cubit/ | `feature_state.dart` |
| Lógica de UI | PRESENTATION cubit/ | `feature_cubit.dart` |
| Pantalla | PRESENTATION pages/ | `feature_page.dart` |
| Componente | PRESENTATION widgets/ | `componente_widget.dart` |

---

## 🚀 Siguiente paso

Ve a la [práctica de mapeo](./02a-practica-carrito-capas.md) y traduce tu descomposición del Carrito a la estructura de carpetas de Clean Architecture.

---

**Tiempo estimado de lectura:** 20 minutos  
**Tiempo estimado de práctica:** 30-40 minutos
