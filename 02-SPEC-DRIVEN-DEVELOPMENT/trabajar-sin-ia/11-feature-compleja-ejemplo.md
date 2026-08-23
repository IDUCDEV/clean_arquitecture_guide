# Feature Compleja: Pasarela de Pagos con Stripe

> Ejemplo de feature compleja con múltiples servicios externos, estados de máquina, manejo de errores críticos y seguridad.

---

## Contexto

**Feature:** Sistema de pagos con Stripe para una app de suscripciones
**Complejidad:** Alta
**Tiempo estimado:** 8-12 horas

---

## FASE 1: Investigar (1 hora)

### User Story

```
**Como** usuario de la app,
**quiero** comprar suscripciones con tarjeta de crédito/débito,
**para** acceder a contenido premium de forma segura.

**Como** administrador,
**quiero** ver el estado de las transacciones,
**para** gestionar reembolsos y problemas de pago.
```

### Investigación de herramientas

```markdown
## Investigación: Pagos con Stripe

### Arquitectura de pagos
┌─────────────────────────────────────────────────────────────────┐
│                    FLUJO DE PAGO STRIPE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  App Flutter → Stripe SDK → Stripe API → Tarjeta               │
│       ↓                                                         │
│  Backend (Supabase Edge Function) → Webhook → Actualizar BD    │
│                                                                 │
│  IMPORTANTE: La app NUNCA toca datos de tarjeta directamente   │
│  El token de pago se genera en el cliente, se envía al backend │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

### Documentación oficial
- Stripe Docs: https://stripe.com/docs
- Stripe Flutter: https://pub.dev/packages/stripe_flutter
- Stripe API: https://stripe.com/docs/api
- Webhooks: https://stripe.com/docs/webhooks

### Dependencias nuevas
- stripe_flutter: ^3.0.0
- http: (para Edge Functions)

### Seguridad (CRÍTICO)
- NUNCA guardar datos de tarjeta en tu servidor
- NUNCA exponer tu Stripe Secret Key en el cliente
- SIEMPRE usar HTTPS
- SIEMPRE verificar pagos con webhooks, no solo con respuestas del cliente
- Implementar idempotency keys para evitar cargos duplicados

### Complejidad: Alta
- Múltiples servicios (Stripe, Supabase, Edge Functions)
- Estados de máquina complejos (pendiente → procesando → exitoso/fallido/reembolsado)
- Seguridad crítica (datos financieros)
- Webhooks asíncronos
- Manejo de errores críticos
```

### Preguntas que te haces

1. ¿Cómo funciona el tokenizado de tarjetas en Stripe?
2. ¿Cuándo debo crear un PaymentIntent vs un Subscription?
3. ¿Cómo verifico que el pago realmente se procesó (webhook)?
4. ¿Qué pasa si el usuario cierra la app durante el pago?
5. ¿Cómo manejo reembolsos?
6. ¿Cómo pruebo sin cobrar dinero real?

---

## FASE 2: Diseñar (1 hora)

### Descomposición (FADER)

| Paso | Qué hago | Resultado |
|------|----------|-----------|
| **F**ormular | User Stories definidas | ✅ |
| **A**ctorizar | 2 actores: usuario, administrador + sistemas (Stripe, Supabase) | ✅ |
| **D**escomponer | Seleccionar plan, ingresar datos, procesar pago, confirmar, mostrar historial | ✅ |
| **E**ntidades | Plan, Pago, Transaccion, MetodoPago | ✅ |
| **R**eglas | Pago atómico (éxito o fallo completo), verificación con webhook, no cobrar dos veces | ✅ |

### Entidades

```dart
// lib/domain/entities/plan.dart

class Plan {
  final String id;
  final String nombre;
  final double precio;
  final String moneda;
  final String intervalo; // 'month', 'year'
  final List<String> features;

  const Plan({
    required this.id,
    required this.nombre,
    required this.precio,
    required this.moneda,
    required this.intervalo,
    required this.features,
  });
}
```

```dart
// lib/domain/entities/transaccion.dart

class Transaccion {
  final String id;
  final String usuarioId;
  final String planId;
  final double monto;
  final String moneda;
  final TransaccionEstado estado;
  final String? stripePaymentIntentId;
  final String? errorMensaje;
  final DateTime fechaCreacion;
  final DateTime? fechaCompletada;

  const Transaccion({
    required this.id,
    required this.usuarioId,
    required this.planId,
    required this.monto,
    required this.moneda,
    required this.estado,
    this.stripePaymentIntentId,
    this.errorMensaje,
    required this.fechaCreacion,
    this.fechaCompletada,
  });
}

enum TransaccionEstado {
  pendiente,
  procesando,
  exitoso,
  fallido,
  reembolsado,
  cancelado,
}
```

### Máquina de estados

```
┌─────────────────────────────────────────────────────────────────┐
│                MÁQUINA DE ESTADOS DE PAGO                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                 │
│  │ PENDIENTE│ →  │PROCESANDO│ →  │ EXITOSO  │                 │
│  └──────────┘    └──────────┘    └──────────┘                 │
│       │               │               │                         │
│       │               ↓               │                         │
│       │         ┌──────────┐         │                         │
│       │         │  FALLIDO │         │                         │
│       │         └──────────┘         │                         │
│       │                              │                         │
│       ↓                              ↓                         │
│  ┌──────────┐                ┌──────────┐                     │
│  │CANCELADO │                │REEMBOLSADO│                    │
│  └──────────┘                └──────────┘                     │
│                                                                 │
│  Transiciones:                                                 │
│  pendiente → procesando (usuario confirma pago)                │
│  procesando → exitoso (webhook confirma)                       │
│  procesando → fallido (webhook reporta error)                  │
│  exitoso → reembolsado (admin reembolsa)                       │
│  pendiente → cancelado (usuario cancela)                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Contratos

```dart
// lib/domain/repositories/pago_repository.dart

abstract class PagoRepository {
  /// Obtiene los planes disponibles
  Future<Either<Failure, List<Plan>>> obtenerPlanes();

  /// Crea un PaymentIntent en el servidor
  Future<Either<Failure, String>> crearPaymentIntent({
    required String planId,
    required String usuarioId,
  });

  /// Confirma el pago con el PaymentIntent
  Future<Either<Failure, Transaccion>> confirmarPago({
    required String paymentIntentId,
  });

  /// Obtiene el historial de transacciones del usuario
  Future<Either<Failure, List<Transaccion>>> obtenerHistorial({
    required String usuarioId,
  });

  /// Verifica el estado de una transacción (polling como backup)
  Future<Either<Failure, Transaccion>> verificarEstado({
    required String transaccionId,
  });
}
```

### Flujo de datos (crítico)

```
Flujo completo de pago:

1. Usuario selecciona plan
   UI → PlanSelectionPage

2. Usuario confirma compra
   UI → PaymentService.crearPaymentIntent()
   → Edge Function → Stripe API → Retorna client_secret

3. Usuario ingresa datos de tarjeta
   Stripe SDK (tokeniza localmente, NUNCA toca tu servidor)
   → Retorna PaymentMethod

4. Se confirma el pago
   PaymentService → confirmPayment(client_secret, payment_method)
   → Stripe procesa
   → UI muestra resultado

5. Webhook verifica (asíncrono)
   Stripe → Webhook → Edge Function → Verifica firma
   → Actualiza BD (transaccion.exitoso)

6. Usuario recibe confirmación
   BD ( Supabase Realtime) → UI → Muestra confirmación
```

### Excecciones a manejar

| Excepción | Cuándo ocurre | Qué mostrar |
|-----------|---------------|-------------|
| Tarjeta rechazada | Banco rechaza | "Pago rechazado. Verifica tus datos." |
| Fondos insuficientes | Saldo no alcanza | "Fondos insuficientes" |
| Tarjeta expirada | Fecha vencida | "Tarjeta expirada" |
| Error de red | Sin conexión | "Error de conexión. Intenta de nuevo." |
| Webhook falla | No se verifica pago | Intentar verificar con polling |
| Pago duplicado | Idempotency key falla | No procesar dos veces |

---

## FASE 3: Implementar (4-6 horas)

### Orden de implementación

```
1. Dominio
   ├── plan.dart (entidad)
   ├── transaccion.dart (entidad)
   └── pago_repository.dart (contrato)

2. Data
   ├── pago_repository_impl.dart (implementación)
   └── models/ (modelos para Stripe)

3. Edge Functions (Supabase)
   ├── create-payment-intent.ts
   └── stripe-webhook.ts

4. Presentation
   ├── plan_selection_page.dart
   ├── payment_page.dart
   ├── payment_controller.dart
   └── transaction_history_page.dart
```

### Implementación clave

**Edge Function: Crear PaymentIntent**
```typescript
// supabase/functions/create-payment-intent/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import Stripe from "https://esm.sh/stripe@12.0.0"

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY') ?? '')

serve(async (req) => {
  try {
    const { planId, usuarioId } = await req.json()

    // Crear PaymentIntent
    const paymentIntent = await stripe.paymentIntents.create({
      amount: 1999, // $19.99 en centavos
      currency: 'usd',
      metadata: {
        usuarioId,
        planId,
      },
    })

    return new Response(
      JSON.stringify({ clientSecret: paymentIntent.client_secret }),
      { headers: { 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    )
  }
})
```

**Edge Function: Webhook**
```typescript
// supabase/functions/stripe-webhook/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import Stripe from "https://esm.sh/stripe@12.0.0"

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY') ?? '')
const webhookSecret = Deno.env.get('STRIPE_WEBHOOK_SECRET') ?? ''

serve(async (req) => {
  const signature = req.headers.get('stripe-signature')!
  const body = await req.text()

  let event: Stripe.Event

  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret)
  } catch (err) {
    return new Response(`Webhook signature verification failed`, { status: 400 })
  }

  if (event.type === 'payment_intent.succeeded') {
    const paymentIntent = event.data.object as Stripe.PaymentIntent

    // Actualizar transacción en Supabase
    const supabase = createClient(/* ... */)
    await supabase
      .from('transacciones')
      .update({ estado: 'exitoso', fecha_completada: new Date() })
      .eq('stripe_payment_intent_id', paymentIntent.id)
  }

  return new Response('OK', { status: 200 })
})
```

**Flutter: Servicio de pagos**
```dart
// lib/data/services/pago_service.dart

class PagoService {
  final Stripe _stripe;

  Future<Either<Failure, Transaccion>> procesarPago({
    required Plan plan,
    required String usuarioId,
  }) async {
    try {
      // 1. Crear PaymentIntent en el servidor
      final paymentIntentResult = await _pagoRepository.crearPaymentIntent(
        planId: plan.id,
        usuarioId: usuarioId,
      );

      if (paymentIntentResult.isLeft()) {
        return Left(paymentIntentResult.getLeft()!);
      }

      final clientSecret = paymentIntentResult.getOrElse(() => '');

      // 2. Inicializar pago con Stripe
      await _stripe.initPaymentSheet(
        paymentSheetParameters: SetupPaymentSheetParameters(
          paymentIntentClientSecret: clientSecret,
          merchantDisplayName: 'Mi App',
          style: ThemeMode.system,
        ),
      );

      // 3. Presentar hoja de pago
      await _stripe.presentPaymentSheet();

      // 4. Confirmar pago
      final result = await _pagoRepository.confirmarPago(
        paymentIntentId: clientSecret.split('_secret_')[0],
      );

      return result;
    } on StripeException catch (e) {
      if (e.error.code == PaymentCompletionAction.canceled) {
        return const Left(PagoCanceladoFailure());
      }
      return Left(PagoFallidoFailure(e.error.message ?? 'Error de pago'));
    } catch (e) {
      return Left(PagoFallidoFailure('Error inesperado'));
    }
  }
}
```

---

## FASE 4: Verificar (45 min)

### Tests críticos

```dart
// test/data/services/pago_service_test.dart

void main() {
  test('Pago exitoso', () async {
    // Arrange
    final repository = MockPagoRepository();
    when(repository.crearPaymentIntent(
      planId: 'plan_123',
      usuarioId: 'user_123',
    )).thenAnswer((_) async => const Right('pi_secret_123'));

    when(repository.confirmarPago(
      paymentIntentId: 'pi_secret_123',
    )).thenAnswer((_) async => Right(transaccionExitosa));

    // Act
    final result = await service.procesarPago(
      plan: planEjemplo,
      usuarioId: 'user_123',
    );

    // Assert
    expect(result.isRight(), true);
    expect(result.getOrElse(() => throw Exception()).estado, TransaccionEstado.exitoso);
  });

  test('Pago cancelado por usuario', () async {
    // Simular cancelación de Stripe
    when(_stripe.presentPaymentSheet())
        .thenThrow(StripeException(error: ...));

    final result = await service.procesarPago(...);
    expect(result.isLeft(), true);
  });

  test('Pago rechazado por banco', () async {
    when(repository.confirmarPago(...))
        .thenAnswer((_) async => const Left(PagoFallidoFailure('Card declined')));

    final result = await service.procesarPago(...);
    expect(result.isLeft(), true);
  });
}
```

### Pruebas de seguridad

```
✅ La Secret Key NUNCA aparece en el código cliente
✅ Los datos de tarjeta NUNCA se envían a tu servidor
✅ Los webhooks verifican la firma de Stripe
✅ Se usa idempotency key para evitar duplicados
✅ Los montos se validan en el servidor, no solo en el cliente
```

---

## FASE 5: Refactor (30 min)

### Verificaciones

- [ ] Secret Key está en variables de entorno
- [ ] Webhook verifica firma correctamente
- [ ] Idempotency key se usa en todas las operaciones
- [ ] Estados de máquina están bien definidos
- [ ] No hay código que exponga datos sensibles

---

## FASE 6: Validar con IA (20 min)

### Prompt

```
Revisa mi implementación de pagos con Stripe.
¿La seguridad está correctamente implementada?
¿El manejo de estados de la máquina de transacciones es completo?
¿Cómo manejo los edge cases (usuario cierra app durante pago)?
¿Los webhooks están configurados correctamente?
NO reescribas el código, solo dame feedback sobre seguridad y edge cases.
```

### Qué buscar en la respuesta

- ¿Detecta problemas de seguridad?
- ¿Identifica edge cases que olvidaste?
- ¿Su feedback es específico y accionable?

---

## Tiempo total: 8-12 horas

| Fase | Tiempo |
|------|--------|
| Investigar | 1 hora |
| Diseñar | 1 hora |
| Implementar | 4-6 horas |
| Verificar | 45 min |
| Refactor | 30 min |
| Validar | 20 min |

---

**Siguiente:** [12-ejercicios-practica.md](./12-ejercicios-practica.md) — 6 ejercicios para practicar sin IA
