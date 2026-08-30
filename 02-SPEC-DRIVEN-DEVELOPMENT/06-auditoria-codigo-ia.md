# 06 · Auditoría de código generado por IA (Modo completo)

> Escenario: la IA escribe **todo** el código y tú solo verificas. Este documento es el manual del nuevo rol: **de autor a auditor**. Complementa Fase 4 de [02-sdd-flutter-supabase.md](./02-sdd-flutter-supabase.md) y se aplica con los ejemplos de [`ejemplos-cambios/`](./ejemplos-cambios/).

---

## El cambio de rol

En el Modo `andamiaje` implementas y entiendes cada línea porque la escribiste. En el Modo `completo` tu valor ya no está en escribir sino en **dos momentos que no se delegan**:

| Momento | Qué haces | Por qué no se delega |
|---|---|---|
| **Puerta 1** | Apruebas proposal + spec EARS + design | La spec es el contrato; una spec ambigua produce código incorrecto *con total confianza* |
| **Puerta 3** | Auditas el código contra la spec | La IA optimiza para "que compile y pase"; tú vela por "que cumpla el contrato" |

Todo lo demás (escribir, tests, commits, refactors) lo ejecuta el agente con `/opsx-apply-change`.

---

## El ciclo de auditoría por oleada

```
Agente: ejecuta oleada N (commit atómico por tarea)
  ↓
Tú: audita el diff de la oleada contra specs/*/spec.md + design.md   ← este documento
  ↓
├─ Cumple → siguiente oleada
└─ No cumple → pide fix citando REQ + escenario exacto
       ├─ El código estaba mal → fix puntual
       └─ La spec era ambigua → corrige la spec PRIMERO (/opsx-update-change),
          luego re-aplica. (Clarity Gate: sigue siendo barato aquí)
```

Regla práctica: **nunca aceptes "ya funciona" sin el requisito citado**. Cada línea de código debe poder responder "¿qué REQ y qué escenario me obligan a existir?".

---

## Checklist de auditoría

Úsalo al cierre de cada oleada. Los ejemplos citan el cambio [`add-cart`](./ejemplos-cambios/add-cart/) como referencia de cómo debería verse.

### 1 · Contratos intactos

- [ ] Las firmas del repository interface coinciden **verbatim** con `design.md` §Contratos Dart clave (nombres, tipos, named params). Ejemplo: si design dice `Future<Either<Failure, Cart>> getCart()`, no existe un `Cart?` ni un `Future<Cart>` "por simplicidad"
- [ ] Todo método de repository/usecase retorna `Either<Failure, T>` — cero excepciones lanzadas hacia arriba, cero `return null`
- [ ] Cero `try/catch` que traga errores (catch vacío o que loguea y continúa); los errores se convierten en `Failure` en el datasource/repository impl, nunca antes
- [ ] No se inventaron métodos fuera del alcance: si `design.md` §Ficheros afectados no lista `deleteCart()`, ese método no debe existir
- [ ] Los archivos creados corresponden 1:1 con la tabla de ficheros afectados (rutas literales)

### 2 · Sealed states exhaustivos y mensajes exactos

- [ ] El state sealed tiene todas sus subclases construidas en el cubit y consumidas en la UI. Ejemplo: `sealed class CartState` con `Initial/Loading/Loaded/Error` — ningún `switch` con caso `_` que oculte estados olvidados
- [ ] Cada transición visible en el flujo de datos de design.md tiene su `emit`. Ejemplo: `addItem` emite `CartLoading` → luego `CartLoaded(cart recalculado)` o `CartError(...)`
- [ ] **Los mensajes de error son los literales exactos de los escenarios EARS**, no paráfrasis. Ejemplos reales de add-cart:
  - `"Producto {nombre} sin stock disponible"` (REQ-001) — no vale `"Stock insuficiente"`
  - `"Has alcanzado el límite de 50 productos"` (REQ-001) — el 50 viene de la regla, no está hardcodeado en la UI
  - `"La cantidad debe ser mayor a 0"` (REQ-001)
  - `"El cupón {codigo} ha expirado"` (REQ-004)
  - `"El descuento supera el límite permitido"` (REQ-004, RN tope 50%)
- [ ] Los mensajes nacen de domain (usecase/failure), no se componen strings en la UI

### 3 · Reglas en la capa correcta

- [ ] Las reglas de negocio (RN) viven en **domain**: entity o usecases. Si encuentras `if (descuento > subtotal * 0.5)` dentro del cubit o de un widget → mal ubicada (en add-cart ese tope se evalúa al aplicar cupón, en `ApplyCoupon`)
- [ ] Sin duplicación inconsistente cliente/servidor: si la validación de stock vive en el RPC `add_cart_item` (Decisión D3 de design.md), NO debe existir además un `if (product.stock <= 0)` en Dart que pueda divergir. Puede haber guardas de UX, pero la fuente de verdad es una sola
- [ ] Los cálculos económicos están donde dice design.md. Ejemplo: Decisión D1 pone subtotal/impuesto/total como métodos puros de la entity `Cart` — verificar que no terminaron en el datasource
- [ ] Decisiones D1–D4 (o las que haya) respetadas; cada archivo clave puede citar su decisión en un comentario

### 4 · Supabase y seguridad ⚠️ (la categoría más crítica)

- [ ] RLS habilitada en TODAS las tablas nuevas de la migración (`alter table ... enable row level security`)
- [ ] Policies por tabla × actor × operación, y coinciden con design.md §Backend Supabase. Ejemplo add-cart: `USING (auth.uid() = user_id)` para `carts`; acceso a `cart_items` vía join con el carrito propio
- [ ] RPCs `security definer` revisados línea por línea: validaciones internas (stock, límites), transacción atómica, y que NO bypaseen RLS más de lo declarado
- [ ] Migración idempotente si design lo declara (add-cart: `create policy if not exists`)
- [ ] Cero `service_role` key en código cliente; cero `.rpc()` que escriba tablas sensibles sin validar ownership interno
- [ ] Columnas de la migración = columnas declaradas en design.md §Backend (ni faltantes ni extra)
- [ ] El datasource usa exactamente las tablas/RPCs del design (ej.: `supabase.rpc('add_cart_item', params: {...})`) y no queries ad-hoc inventadas

### 5 · Tests contra la spec

- [ ] Existe **al menos un test por Scenario** de cada Requirement ADDED (los escenarios son la especificación de pruebas)
- [ ] Los nombres de test citan el REQ: `test('REQ-001: producto sin stock muestra mensaje y no modifica carrito')`
- [ ] Los asserts usan los literales exactos de los mensajes (si cambias el texto en la spec, el test debe romper)
- [ ] Tests de regla: mutar la entrada viola la salida esperada. Ejemplo: aplicar cupón con descuento > 50% del subtotal DEBE retornar Failure con el mensaje del escenario
- [ ] Cero tests siempre-verdes (assert trivial, mock que devuelve lo mismo que se pasa)
- [ ] Test de roundtrip JSON para cada model (add-cart: `CartModel.fromJson(toJson)` preserva montos)

### 6 · Trazabilidad completa

- [ ] Matriz Req ↔ tarea ↔ test de tasks.md llena, sin huecos
- [ ] Cero `UnimplementedError()` sobrevivientes (o los que queden tienen tarea abierta explícita)
- [ ] Los TODOs generados citan el REQ correcto (un TODO de REQ-003 dentro de `applyCoupon` es señal de copia-pega)
- [ ] Commits atómicos: un commit por tarea, mensaje convencional referenciando la tarea (`feat(cart): RPC add_cart_item (task 2.3, REQ-001)`)

### 7 · Red flags generales

- [ ] El diff no toca archivos fuera de la tabla de ficheros afectados (scope creep silencioso)
- [ ] No hay dependencias nuevas en pubspec.yaml sin justificación en design.md (add-cart declara "no añadir paquetes")
- [ ] Sin over-engineering: abstracciones, interfaces o genéricos que nadie pidió
- [ ] Sin código muerto, imports sin usar, ni comentarios que expliquen decisiones NO tomadas
- [ ] Los boundaries del change folder (§Boundaries en design.md) se respetan. Ejemplo: "No desactivar RLS bajo ninguna circunstancia"

---

## Ejemplo de auditoría real (REQ-001, escenario "Producto sin stock")

1. **Spec dice** ([spec.md](./ejemplos-cambios/add-cart/specs/shopping-cart/spec.md)): *"IF el stock del producto es 0 THEN mostrar 'Producto {nombre} sin stock disponible' sin modificar el carrito"*
2. **Design dice**: la validación es del RPC `add_cart_item` dentro de una transacción (D3)
3. **Auditar**:
   - [ ] El SQL del RPC valida stock y hace `raise exception` con ese mensaje exacto
   - [ ] El failure llega como `Either.left(Failure("Producto {nombre} sin stock disponible"))`, no como excepción
   - [ ] El cubit lo emite como `CartError(mensaje)` y la UI lo muestra tal cual
   - [ ] Hay test que inserta producto con stock 0 y afirma el mensaje + que `cart_items` no cambió
   - [ ] La transacción revierte si algo falla a mitad (atomicidad de D3)

Si las cinco casillas pasan, ese escenario está auditado. Repite por escenario; un Requirement con 4 escenarios son 4 mini-auditorías.

---

## Señales de que NO deberías estar en Modo completo

Sé honesto contigo mismo:

- Leíste el checklist y más de la mitad de los términos te suenan vagos (`Either`, sealed, RLS, security definer…)
- No sabrías distinguir un `try/catch` tragador de un manejo legítimo de errores
- Firmarías el diff "porque compila y los tests pasan"

→ Cambia a **Modo andamiaje** (implementas tú sobre scaffold) hasta que el checklist sea lectura natural. Ahí es exactamente donde entra [`trabajar-sin-ia/`](./trabajar-sin-ia/): criterio de auditoría se construye escribiendo código, no leyendo diffs.

---

## Resumen en una línea

> La IA puede escribir todo el código, pero el contrato (spec) lo apruebas tú al inicio y el cumplimiento (auditoría) lo certificas tú al final. Entre esos dos momentos, delega sin culpa.

---

**Siguiente paso:** aplica este checklist sobre [`ejemplos-cambios/add-cart/`](./ejemplos-cambios/add-cart/) simulando que otro agente lo implementó — es el mejor entrenamiento antes de usarlo en producción.
