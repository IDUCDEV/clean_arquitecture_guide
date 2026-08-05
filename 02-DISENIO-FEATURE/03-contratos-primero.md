# Contract-First Design: Primero los Contratos

> Aprende a diseñar las interfaces (contratos) entre capas antes de implementar cualquier funcionalidad. El arte de definir el "qué" antes del "cómo".

---

## ¿Qué es Contract-First Design?

Es la práctica de **definir las interfaces públicas** de cada capa **antes** de escribir cualquier implementación. Así como un contrato legal define qué debe hacer cada parte sin decir cómo lo hará.

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   ❌ ENFOQUE TRADICIONAL:                                │
│   "Ya sé cómo voy a implementar el carrito, empiezo     │
│    por el DataSource y subo"                             │
│   → Terminas con código acoplado y difícil de testear   │
│                                                          │
│   ✅ CONTRACT-FIRST:                                     │
│   "Primero defino cómo se comunican las capas, luego    │
│    implemento cada una"                                  │
│   → Terminas con código desacoplado y testeable          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Los 3 Contratos Clave

En Clean Architecture hay 3 contratos principales que debes diseñar primero:

### 1. Contrato de Repositorio (Domain → Data)

Define **qué datos necesita el dominio**, sin importar de dónde vengan.

```dart
// 🎯 CONTRATO: Lo que el DOMINIO necesita
abstract class CartRepository {
  Future<Either<Failure, Cart>> getCart(String userId);
  Future<Either<Failure, Cart>> addProduct({
    required String userId,
    required Product product,
    required int quantity,
  });
  Future<Either<Failure, Cart>> removeProduct({
    required String userId,
    required String productId,
  });
  Future<Either<Failure, Cart>> updateQuantity({
    required String userId,
    required String productId,
    required int quantity,
  });
  Future<Either<Failure, Cart>> applyCoupon({
    required String userId,
    required String couponCode,
  });
}
```

> **Alternativa con UserSession:** Inyectando `UserSession` en `CartRepositoryImpl`, el contrato puede omitir `userId` — el repository lo obtiene internamente: `getCart()` en vez de `getCart(String userId)`. Esto simplifica el contrato cuando el userId pertenece siempre al usuario autenticado. La contraparte: los tests deben asegurar que `UserSession` retorne el userId correcto.

**Preguntas para diseñar este contrato:**

| Pregunta | Decisión de diseño |
|----------|-------------------|
| ¿El método retorna el `Cart` completo o solo el cambio? | Retornar el Cart completo mantiene la UI consistente |
| ¿Parámetros individuales o un objeto ValueObject? | Para 3+ parámetros, usa named parameters |
| ¿Manejo de errores con excepciones o Either? | Either es más explícito (como se usa en fpdart) |
| ¿El userId se pasa siempre o se obtiene del contexto? | Depende: si el userId lo necesita el contrato (Domain), inyecta `UserSession` en el RepositoryImpl y el contrato no lo recibe. Si el userId lo necesita el negocio (UseCase), pásalo como parámetro. En general, el contrato del Repository no debe recibir userId porque es un detalle de implementación — el RepositoryImpl lo obtiene de `UserSession`. |

### 2. Contrato de DataSource (Data → API/DB)

Define **qué operaciones de bajo nivel** necesita el repositorio.

```dart
// 🎯 CONTRATO: Lo que DATA necesita del mundo exterior
abstract class CartRemoteDataSource {
  Future<CartModel> fetchCart(String userId);
  Future<CartModel> addItem(String userId, Map<String, dynamic> itemData);
  Future<CartModel> removeItem(String userId, String productId);
  Future<CartModel> updateItemQuantity(
    String userId, String productId, int quantity);
  Future<CartModel> applyCoupon(String userId, String couponCode);
}

abstract class CartLocalDataSource {
  Future<CartModel> getCachedCart(String userId);
  Future<void> cacheCart(String userId, CartModel cart);
  Future<void> clearCart(String userId);
}
```

### 3. Contrato del UseCase (Presentation → Domain)

Define **qué operaciones de negocio** están disponibles para la UI.

```dart
// 🎯 CONTRATO: Lo que PRESENTATION necesita del DOMINIO
abstract class AddProductToCartUseCase {
  Future<Either<Failure, Cart>> call({
    required String userId,
    required Product product,
    required int quantity,
  });
}

abstract class GetCartSummaryUseCase {
  Future<Either<Failure, Cart>> call(String userId);
}

abstract class ApplyCouponUseCase {
  Future<Either<Failure, Cart>> call({
    required String userId,
    required String couponCode,
  });
}
```

---

## El Proceso Contract-First en 4 pasos

### Paso 1: Identifica los puntos de comunicación

Dibuja las flechas de comunicación entre capas:

```
PRESENTATION  ──llama──>  DOMAIN (UseCase)
DOMAIN        ──llama──>  DOMAIN (Repository interface)
DATA (Repo)   ──llama──>  DATA (DataSource interface)
DATA (DS)     ──llama──>  Sistema externo (API, DB)
```

Cada flecha es un **contrato** que debes diseñar.

### Paso 2: Diseña la interface ideal

Sin pensar en la implementación, responde:

- **¿Qué método expone?** → Cada operación atómica del FADER
- **¿Qué parámetros recibe?** → Lo mínimo indispensable
- **¿Qué retorna?** → El tipo de dato o un Result/Either
- **¿Qué errores puede producir?** → Los failures del dominio

### Paso 3: Valida el contrato

Revisa que el contrato sea:

- **Independiente de tecnología:** No menciones HTTP, Supabase, SQL, etc.
- **Completo:** Cubre todas las operaciones de la descomposición FADER
- **Consistente:** Sigue el mismo patrón en todos los métodos
- **Testeable:** Puedes crear un Fake/Mock fácilmente

### Paso 4: Congela el contrato

Una vez definido, el contrato NO cambia por decisiones de implementación.

```
❌ "Necesito agregar un parámetro 'cacheKey' al contrato porque en la
    implementación me conviene tenerlo"

✅ "Necesito que el contrato reciba 'userId' para identificar el carrito.
    Cómo se cachea internamente es problema de la implementación."
```

---

## Architecture Decision Records (ADR)

Los ADR son documentos cortos que registran las decisiones de arquitectura importantes. Úsalos para congelar tus contratos.

**Formato de un ADR:**

```markdown
# ADR-001: Contrato del Repositorio de Carrito

## Contexto
Necesitamos definir cómo el dominio accede a los datos del carrito.

## Decisión
Usaremos una interfaz abstracta `CartRepository` en domain/repositories/.
Cada método retorna `Future<Either<Failure, Cart>>`.
El carrito completo se retorna siempre, no solo el cambio.

## Consecuencias
Positivas:
- El dominio no depende de la fuente de datos
- Fácil de testear con fakes
- Podemos cambiar de Supabase a Firebase sin tocar el dominio

Negativas:
- Retornar el carrito completo puede ser ineficiente en carritos muy grandes
- Más boilerplate inicial

## Alternativas consideradas
1. Retornar solo el item cambiado → Descartado: inconsistencia de estado
2. Usar excepciones en vez de Either → Descartado: menos explícito
3. No usar interface → Descartado: viola Clean Architecture
```

**¿Cuándo escribir un ADR?**

- Cuando defines un contrato nuevo
- Cuando cambias un contrato existente
- Cuando eliges entre alternativas de diseño
- Cuando hay trade-offs involucrados

---

## Ejemplo: ADR del Carrito

```markdown
# ADR-002: Modelo de Estados del Cubit

## Contexto
El Cubit del carrito necesita representar los estados de la UI.

## Decisión
Usaremos un sealed class con 5 estados:
- CartInitial
- CartLoading
- CartLoaded (contiene cart + isCheckingOut)
- CartError (contiene message)
- CartActionLoading (contiene cart anterior + loadingItemId)

## Consecuencias
Positivas:
- Cada estado posible está tipado
- La UI no puede renderizar un estado inválido
- Fácil de testear cada estado por separado

Negativas:
- Más clases que un solo estado genérico con flags

## Alternativas consideradas
1. Un solo estado con `isLoading`, `error`, etc. → Descartado: estados inválidos posibles
2. Freezed → Descartado: preferimos explícito sobre generado
```

---

## Plantilla de Contrato

Usa esta plantilla para diseñar cualquier contrato:

```dart
/// [DESCRIPCIÓN DEL CONTRATO]
///
/// Define cómo [CAPA_ORIGEN] se comunica con [CAPA_DESTINO].
///
/// Responsabilidades:
/// - [RESPONSABILIDAD_1]
/// - [RESPONSABILIDAD_2]
///
/// No responsabilidades:
/// - [NO_RESPONSABILIDAD_1]
///
abstract class [NombreContrato] {
  /// [DESCRIPCIÓN DEL MÉTODO]
  ///
  /// [QUÉ HACE]
  /// [QUÉ RETORNA EN ÉXITO]
  /// [QUÉ RETORNA EN ERROR]
  Future<Either<Failure, [TipoExitoso]>> [metodo]({
    required [param1Type] [param1Name],
    required [param2Type] [param2Name],
  });
}
```

---

## Errores comunes

| Error | Síntoma | Solución |
|-------|---------|----------|
| Contrato atado a tecnología | `fetchCartFromSupabase()` | Renómbralo a `fetchCart()` |
| Contrato con demasiados métodos | 15 métodos en un repositorio | Divide en repositorios más pequeños |
| Contrato que cambia por la implementación | Agregas params que solo usa un DataSource | El contrato es del dominio, no del DataSource |
| Reglas técnicas/seguridad en el contrato de dominio | `fetchCartPaginado(page, limit)` en el Repository | La paginación es RT: va en el DataSource, no en el dominio |
| No documentar decisiones | "¿Por qué retornamos el carrito completo?" | Escribe un ADR |
| Contrato sin manejo de errores | Retorna `Cart?` en vez de `Either` | Define failures explícitos |
| Contrato sin trazabilidad | Operaciones sin UseCase o UseCase sin test | Regístralo en la [matriz de trazabilidad](./05f-criterios-aceptacion-trazabilidad.md) |

---

## 🚀 Siguiente paso

Ve a la [práctica de contratos](./03a-practica-carrito-contratos.md) y diseña los contratos del Carrito de Compras usando lo aprendido aquí.

---

**Tiempo estimado de lectura:** 20 minutos  
**Tiempo estimado de práctica:** 30 minutos
