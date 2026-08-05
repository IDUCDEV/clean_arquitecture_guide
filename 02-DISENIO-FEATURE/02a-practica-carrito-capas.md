# Práctica: Mapear Carrito de Compras a Clean Architecture

> Traduce tu descomposición FADER del Carrito a la estructura de carpetas y capas de Clean Architecture.

---

## Instrucciones

1. Toma la hoja FADER que completaste en la práctica anterior
2. Sin abrir el editor, dibuja el árbol de carpetas en papel
3. Identifica qué archivos van en cada capa
4. Al final, compara con la solución sugerida

---

## Enunciado

Usando la descomposición FADER del Carrito de Compras, mapea cada elemento a las capas de Clean Architecture.

---

## Paso a Paso

### ✏️ Paso 1: Identifica qué va en DOMAIN

Revisa tu hoja FADER. Separa:

- **Entidades:** ¿Cuáles son los conceptos de negocio puros?
- **UseCases (operaciones + reglas):** ¿Cada operación atómica de la descomposición es un UseCase?
- **Interfaces (repositories/services):** ¿Qué contratos necesita tu dominio?

Dibuja el árbol de la carpeta `domain/`.

**Pregúntate:**
- ¿Esta entidad necesita saber de Flutter? → No → Va en DOMAIN ✓
- ¿Este UseCase podría testearse sin conexión a internet? → Sí → Va en DOMAIN ✓
- ¿Esta interface expone lo necesario sin atarse a una tecnología? → Sí → Va en DOMAIN ✓

### ✏️ Paso 2: Identifica qué va en DATA

Revisa los actores externos de tu FADER:

- **Fuentes de datos:** ¿De dónde vienen los datos? (API, BD local, cache)
- **Modelos:** ¿Cómo se serializan/deserializan las entidades?
- **Implementaciones:** ¿Quién implementa los contratos de DOMAIN?

Dibuja el árbol de la carpeta `data/`.

**Pregúntate:**
- ¿Esto cambia si cambio de Supabase a Firebase? → Sí → Va en DATA ✓
- ¿Esto es un detalle de implementación? → Sí → Va en DATA ✓

### ✏️ Paso 3: Identifica qué va en PRESENTATION

Revisa los actores humanos de tu FADER:

- **Estados:** ¿Qué estados visuales puede tener la feature? (cargando, datos, error, vacío)
- **Cubits/BLoCs:** ¿Quién orquesta la lógica de UI?
- **Widgets:** ¿Qué pantallas y componentes necesita el usuario?

Dibuja el árbol de la carpeta `presentation/`.

**Pregúntate:**
- ¿Esto es específico de Flutter? → Sí → Va en PRESENTATION ✓
- ¿Esto cambia si paso de mobile a web? → Sí → Va en PRESENTATION ✓

---

## Solución Sugerida

### ✅ Estructura DOMAIN

```
lib/
└── cart/
    └── domain/
        ├── entities/
        │   ├── product.dart
        │   ├── cart_item.dart
        │   ├── cart.dart
        │   └── coupon.dart
        ├── usecases/
        │   ├── add_product_to_cart.dart       ← RN002, RN003
        │   ├── remove_product_from_cart.dart
        │   ├── update_product_quantity.dart   ← RN003
        │   ├── get_cart_summary.dart          ← RN004
        │   ├── apply_coupon.dart              ← RN005, RN006
        │   └── validate_stock.dart            ← RN002 (useCase separado)
        ├── repositories/
        │   └── cart_repository.dart           ← interface
        └── core/
            └── failures.dart                  ← Errores del dominio
```

**Detalle de failures:**

```dart
// failures.dart
sealed class Failure {}

final class CartLimitExceeded extends Failure {}
final class ProductOutOfStock extends Failure {}
final class InvalidQuantity extends Failure {}
final class ExpiredCoupon extends Failure {}
final class DiscountLimitExceeded extends Failure {}
final class CartNotFound extends Failure {}
final class UnknownFailure extends Failure {}
```

**Detalle de entidad Cart:**

```
Cart
├── id: String
├── items: List<CartItem>
├── subtotal: double        → calculado: suma de (precioUnitario * cantidad)
├── discount: double        → 0 si no hay cupón
├── tax: double             → 16% de (subtotal - discount)
├── total: double           → subtotal - discount + tax
└── couponCode: String?     → cupón aplicado (si hay)
```

### ✅ Estructura DATA

```
lib/
└── cart/
    └── data/
        ├── datasources/
        │   ├── cart_remote_data_source.dart   ← Supabase
        │   └── cart_local_data_source.dart    ← Cache local
        ├── models/
        │   ├── cart_model.dart                ← fromJson/toJson
        │   ├── product_model.dart
        │   ├── cart_item_model.dart
        │   └── coupon_model.dart
        └── repositories/
            └── cart_repository_impl.dart      ← Implementa CartRepository
```

**Ejemplo de modelo:**

```dart
// cart_model.dart (solo estructura, sin implements)
class CartModel {
  final String id;
  final List<CartItemModel> items;
  final String? couponCode;

  CartModel({
    required this.id,
    required this.items,
    this.couponCode,
  });

  factory CartModel.fromJson(Map<String, dynamic> json) =>
    CartModel(
      id: json['id'] as String,
      items: (json['items'] as List)
        .map((e) => CartItemModel.fromJson(e as Map<String, dynamic>))
        .toList(),
      couponCode: json['coupon_code'] as String?,
    );

  Map<String, dynamic> toJson() => {
    'id': id,
    'items': items.map((e) => e.toJson()).toList(),
    'coupon_code': couponCode,
  };
}
```

### ✅ Estructura PRESENTATION

```
lib/
└── cart/
    └── presentation/
        ├── cubit/
        │   ├── cart_cubit.dart
        │   └── cart_state.dart
        ├── pages/
        │   └── cart_page.dart
        └── widgets/
            ├── cart_item_tile.dart
            ├── cart_summary_card.dart
            ├── coupon_input.dart
            └── empty_cart_placeholder.dart
```

**Estados del Cubit:**

```
CartState
├── CartInitial         → No hay datos aún
├── CartLoading         → Cargando desde la fuente
├── CartLoaded          → Datos disponibles
│   ├── cart: Cart
│   └── isCheckingOut: bool
├── CartError           → Error
│   └── message: String
└── CartActionLoading   → Acción en curso (agregar, quitar, etc.)
    ├── cart: Cart      → Estado anterior (para no perder UI)
    └── loadingItemId: String?
```

### ✅ Matriz de trazabilidad

Conecta operación → UseCase → regla → contrato → test (teoría en [05f-criterios-aceptacion-trazabilidad.md](./05f-criterios-aceptacion-trazabilidad.md)):

| Operación | UseCase | Regla | Contrato | Test |
|-----------|---------|-------|----------|------|
| Agregar producto | `AddProductToCart` | RN002, RN003 | `cartRepository.addProduct()` | Unit + integration |
| Quitar producto | `RemoveProductFromCart` | — | `cartRepository.removeProduct()` | Unit |
| Actualizar cantidad | `UpdateProductQuantity` | RN003 | `cartRepository.updateQuantity()` | Unit |
| Ver resumen | `GetCartSummary` | RN004 | `cartRepository.getCart()` | Unit + widget |
| Aplicar cupón | `ApplyCoupon` | RN005, RN006 | `cartRepository.applyCoupon()` | Unit + integration |
| Validar stock | `ValidateStock` | RN002 | `cartRepository.addProduct()` | Unit |
| Acceso al carrito | — | RS001 | `cartRepository.getCart()` (RLS) | Integration |
| Lectura paginada | — | RT001 | `cartRemoteDataSource` | — |

> **Nota:** RT001 y RS001 no generan UseCase ni archivo en DOMAIN. Se implementan en DATA (datasource + RLS/migración) — ver [05e-diseno-supabase.md](./05e-diseno-supabase.md).

---

## Verificación: Lista de chequeo

Al terminar, verifica:

- [ ] ¿Cada entidad de FADER tiene su archivo en `domain/entities/`?
- [ ] ¿Cada operación atómica tiene su UseCase en `domain/usecases/`?
- [ ] ¿Las interfaces de repositorio están en `domain/repositories/`?
- [ ] ¿Los errores del dominio están tipados en `domain/core/failures.dart`?
- [ ] ¿Los modelos tienen `fromJson`/`toJson` en `data/models/`?
- [ ] ¿Las fuentes de datos están separadas (remota/local) en `data/datasources/`?
- [ ] ¿La implementación del repo está en `data/repositories/`?
- [ ] ¿Los estados del Cubit reflejan todas las situaciones de UI?
- [ ] ¿Cada operación, regla y contrato está en la matriz de trazabilidad?
- [ ] ¿Las reglas RT/RS están en DATA (datasource/RLS) y no en el dominio?
- [ ] ¿No hay código de DOMAIN dependiendo de DATA o PRESENTATION?
- [ ] ¿No hay código de DATA o PRESENTATION en DOMAIN?

---

## 🚀 Siguiente paso

Ahora que tienes la estructura de capas definida, ve a [03-contratos-primero.md](./03-contratos-primero.md) para aprender a diseñar los contratos (interfaces) antes de implementar.

---

**Tiempo:** 30-40 minutos  
**Material:** Papel y lápiz + tu hoja FADER de la práctica anterior
