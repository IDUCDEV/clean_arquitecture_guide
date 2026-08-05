# Práctica: Contratos del Carrito de Compras

> Diseña los contratos (interfaces) del Carrito de Compras antes de implementar cualquier cosa.

---

## Instrucciones

1. Toma tu estructura de capas de la práctica anterior
2. En papel, diseña **las interfaces** de cada capa
3. No escribas implementaciones. Solo contratos
4. Al final, escribe un ADR para la decisión más importante
5. Compara con la solución sugerida

---

## Enunciado

Usando la descomposición FADER y la estructura de capas que definiste, diseña:

1. El contrato de `CartRepository` (Domain)
2. El contrato de `CartRemoteDataSource` y `CartLocalDataSource` (Data)
3. Los contratos de `AddProductToCartUseCase` y `ApplyCouponUseCase` (Domain)
4. El contrato del `CartState` (Presentation)
5. Un ADR para justificar por qué el UseCase retorna `Either<Failure, Cart>` en vez de lanzar excepciones

---

## Paso a Paso

### ✏️ Paso 1: Contrato del Repositorio

Diseña la interfaz de `CartRepository`. Considera:

- ¿Qué métodos necesita?
- ¿Qué parámetros recibe cada método?
- ¿Qué retorna?
- ¿Qué failures puede producir?

Recuerda: esto es un contrato, no una implementación. **No menciones HTTP, SQL, ni ninguna tecnología.**

### ✏️ Paso 2: Contratos de DataSources

Diseña `CartRemoteDataSource` y `CartLocalDataSource`. Considera:

- El DataSource remoto habla con una API (REST/GraphQL)
- El DataSource local habla con SQLite, Hive o SharedPreferences
- ¿Usan los mismos tipos de datos?
- ¿Cómo separas responsabilidades entre remoto y local?

### ✏️ Paso 3: Contratos de UseCases

Diseña al menos:

- `AddProductToCartUseCase`: ¿Qué validaciones incluye?
- `ApplyCouponUseCase`: ¿Qué reglas de negocio aplica?

Usa el patrón de `call()` para que el Cubit pueda invocarlos directamente.

### ✏️ Paso 4: Contrato del Estado

Diseña los estados del Cubit:

- ¿Qué estados puede tener el carrito?
- ¿Qué datos lleva cada estado?
- ¿Cómo evitas estados inválidos?

### ✏️ Paso 5: Escribe un ADR

Redacta un ADR para la decisión más relevante de tus contratos.

---

## Solución Sugerida

### ✅ CartRepository

```dart
// domain/repositories/cart_repository.dart

/// Contrato para la gestión de datos del carrito.
///
/// Define las operaciones que el dominio necesita para persistir
/// y recuperar datos del carrito, independientemente de la fuente.
///
/// Responsabilidades:
/// - Persistir items del carrito
/// - Aplicar cupones de descuento
/// - Recuperar el estado actual del carrito
///
/// No responsabilidades:
/// - Validar reglas de negocio (eso es responsabilidad del UseCase)
/// - Conocer la fuente de datos (API, BD local, etc.)
///
abstract class CartRepository {
  /// Obtiene el carrito de un usuario.
  Future<Either<Failure, Cart>> getCart(String userId);

  /// Agrega un producto al carrito.
  Future<Either<Failure, Cart>> addProduct({
    required String userId,
    required Product product,
    required int quantity,
  });

  /// Elimina un producto del carrito.
  Future<Either<Failure, Cart>> removeProduct({
    required String userId,
    required String productId,
  });

  /// Actualiza la cantidad de un producto en el carrito.
  Future<Either<Failure, Cart>> updateQuantity({
    required String userId,
    required String productId,
    required int quantity,
  });

  /// Aplica un cupón de descuento al carrito.
  Future<Either<Failure, Cart>> applyCoupon({
    required String userId,
    required String couponCode,
  });
}
```

### ✅ CartRemoteDataSource

```dart
// data/datasources/cart_remote_data_source.dart

/// Fuente de datos remota para el carrito.
///
/// Se comunica con Supabase (REST API) para operaciones CRUD.
/// Los modelos retornados ya vienen serializados de la API.
///
abstract class CartRemoteDataSource {
  Future<CartModel> fetchCart(String userId);
  Future<CartModel> addItem(String userId, Map<String, dynamic> itemData);
  Future<CartModel> removeItem(String userId, String productId);
  Future<CartModel> updateItemQuantity(
    String userId, String productId, int quantity);
  Future<CartModel> applyCoupon(String userId, String couponCode);
}
```

### ✅ CartLocalDataSource

```dart
// data/datasources/cart_local_data_source.dart

/// Fuente de datos local (caché) para el carrito.
///
/// Almacena el carrito en SQLite/Hive para acceso offline.
///
abstract class CartLocalDataSource {
  Future<CartModel?> getCachedCart(String userId);
  Future<void> cacheCart(String userId, CartModel cart);
  Future<void> clearCache(String userId);
}
```

### ✅ UseCases

```dart
// domain/usecases/add_product_to_cart.dart

/// Agrega un producto al carrito.
///
/// Valida:
/// - Que el producto tenga stock disponible (RN002)
/// - Que la cantidad sea mayor a 0 (RN003)
/// - Que el carrito no exceda 50 items (RN001)
///
class AddProductToCart {
  final CartRepository repository;

  const AddProductToCart(this.repository);

  Future<Either<Failure, Cart>> call({
    required String userId,
    required Product product,
    required int quantity,
  }) {
    // Las validaciones se hacen aquí, en el dominio
    if (quantity <= 0) return Left(InvalidQuantity());
    if (product.stock <= 0) return Left(ProductOutOfStock());

    return repository.addProduct(
      userId: userId,
      product: product,
      quantity: quantity,
    );
  }
}
```

```dart
// domain/usecases/apply_coupon.dart

/// Aplica un cupón de descuento al carrito.
///
/// Valida:
/// - Que el cupón no esté expirado (RN005)
/// - Que el descuento no exceda el 50% (RN006)
///
class ApplyCoupon {
  final CartRepository repository;

  const ApplyCoupon(this.repository);

  Future<Either<Failure, Cart>> call({
    required String userId,
    required String couponCode,
  }) {
    return repository.applyCoupon(
      userId: userId,
      couponCode: couponCode,
    );
  }
}
```

### ✅ CartState

```dart
// presentation/cubit/cart_state.dart

sealed class CartState {}

final class CartInitial extends CartState {}

final class CartLoading extends CartState {}

final class CartLoaded extends CartState {
  final Cart cart;
  final bool isCheckingOut;

  const CartLoaded({
    required this.cart,
    this.isCheckingOut = false,
  });
}

final class CartError extends CartState {
  final String message;

  const CartError(this.message);
}

final class CartActionLoading extends CartState {
  final Cart cart;
  final String? loadingItemId;

  const CartActionLoading({
    required this.cart,
    this.loadingItemId,
  });
}
```

### ✅ ADR-001

```markdown
# ADR-001: Uso de Either en Contract-First

## Contexto
Necesitamos definir cómo los contratos del dominio manejan errores.

## Decisión
Todos los métodos de repositorio y usecases retornarán
`Future<Either<Failure, T>>` en vez de lanzar excepciones.

## Consecuencias
Positivas:
- El tipo de retorno es explícito: el llamante sabe que puede fallar
- Los failures están tipados: se puede reaccionar distinto a cada error
- No hay excepciones inesperadas en tiempo de ejecución
- La UI puede mapear cada Failure a un mensaje distinto

Negativas:
- Más código que con excepciones
- Curva de aprendizaje para desarrolladores nuevos en Either

## Alternativas consideradas
1. Lanzar excepciones → Descartado: no son explícitas en el tipo de retorno
2. Retornar null en error → Descartado: perdemos información del error
3. Callbacks onSuccess/onError → Descartado: menos composable
```

---

## Verificación: Lista de chequeo

- [ ] ¿Cada contrato tiene un nombre descriptivo?
- [ ] ¿Los contratos de dominio no mencionan tecnologías específicas?
- [ ] ¿Cada método retorna un tipo explícito (Either)?
- [ ] ¿Los failures están tipados y son específicos?
- [ ] ¿Los parámetros son los mínimos necesarios?
- [ ] ¿El DataSource remoto usa modelos en vez de entidades?
- [ ] ¿Las reglas técnicas/seguridad (RT/RS) no se colaron en el contrato de dominio?
- [ ] ¿El ADR documenta la decisión más importante?
- [ ] ¿Los estados del Cubit cubren todos los escenarios?
- [ ] ¿Cada contrato está registrado en la matriz de trazabilidad?

---

## 🚀 Siguiente paso

Ahora que tienes los contratos definidos, ve a [04-flujo-datos.md](./04-flujo-datos.md) para aprender a diseñar el flujo de datos entre las capas.

---

**Tiempo:** 30 minutos  
**Material:** Papel y lápiz + estructura de capas de la práctica anterior
