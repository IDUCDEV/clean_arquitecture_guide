# Caso Práctico: App de Delivery

> Aplica FADER + Mapeo + Contratos + Flujo para diseñar una app de delivery con múltiples actores, geolocalización y tiempo real.

---

## Enunciado

Somos el equipo de ingeniería de una startup de delivery de comida. El equipo de producto nos pide:

> Los clientes deben poder ver restaurantes cercanos, hacer pedidos, rastrear a su repartidor en tiempo real, y pagar online o en efectivo. Los restaurantes deben poder gestionar su menú, aceptar o rechazar pedidos, y marcar pedidos como listos. Los repartidores deben poder ver pedidos disponibles cercanos, aceptar entregas, y actualizar el estado del pedido (en camino, entregado). Los administradores deben poder gestionar usuarios, comisiones, y ver reportes de operaciones.

---

## Instrucciones

1. Trabaja en papel y lápiz. No abras el editor de código.
2. Sigue cada sección en orden.
3. Al final, compara con la solución sugerida.

---

## Sección 1: FADER

### ✏️ Paso 1: Formular

Escribe al menos 4 enunciados "Como [actor], quiero [acción] para [valor]".

**Pregúntate:**
- ¿El delivery es solo de comida o de cualquier producto?
- ¿El cliente paga al restaurante, a la plataforma, o al repartidor?
- ¿Los precios varían por zona o por distancia?
- ¿El repartidor puede aceptar múltiples pedidos a la vez?

### ✏️ Paso 2: Actorizar

Identifica todos los actores y sus permisos:

| Actor | Tipo | ¿Qué puede hacer? |
|-------|------|-------------------|
| Cliente | Primario | |
| Restaurante | Secundario | |
| Repartidor | Secundario | |
| Admin | Terciario | |
| Pasarela de Pagos | Externo | |
| API de Mapas | Externo | |
| ? | ? | |

**Pregúntate:**
- ¿El restaurante puede ver la ubicación del repartidor asignado?
- ¿El cliente puede ver la ubicación del restaurante Y del repartidor?
- ¿El repartidor puede rechazar un pedido después de aceptarlo?
- ¿Hay un modo "invitado" o siempre requiere registro?

### ✏️ Paso 3: Descomponer

Enumera todas las operaciones atómicas.

**Considera operaciones como:**

**Cliente:**
- Ver restaurantes cercanos (geolocalización)
- Ver menú de un restaurante
- Agregar items al pedido
- Hacer pedido (con pago)
- Rastrear pedido en tiempo real
- Calificar restaurante y repartidor

**Restaurante:**
- Gestionar menú (items, precios, disponibilidad)
- Recibir pedido entrante
- Aceptar/rechazar pedido
- Marcar pedido como "en preparación"
- Marcar pedido como "listo para recoger"

**Repartidor:**
- Ver pedidos disponibles cercanos
- Aceptar pedido (asignación)
- Marcar "en camino al restaurante"
- Marcar "recogido"
- Marcar "en camino al cliente"
- Marcar "entregado"

**Sistema:**
- Asignar repartidor automáticamente
- Calcular tarifa de envío
- Estimar tiempo de entrega
- Actualizar ubicación en tiempo real (WebSockets/streams)

**Máquina de estados de un pedido:**

```
Pendiente → Confirmado → En preparación → Listo → En camino → Entregado
    │           │              │
    │           ▼              │
    └────→ Cancelado (cliente) │
                │              │
                ▼              ▼
         Cancelado (resto)  Cancelado (repartidor no asignado)
```

**Identifica dependencias:**
- ¿Qué pasa si no hay repartidores disponibles?
- ¿El pago se cobra al hacer el pedido o al entregarlo?
- ¿El cliente puede cancelar después de que el restaurante aceptó?

### ✏️ Paso 4: Entidades

Define las entidades de negocio:

**Posibles entidades:**
- `Usuario` (User) — con roles: cliente, restaurante, repartidor, admin
- `Restaurante` (Restaurant)
- `ItemMenu` (MenuItem)
- `Pedido` (Order)
- `ItemPedido` (OrderItem)
- `Repartidor` (DeliveryPerson)
- `Ubicacion` (Location) — value object
- `Calificacion` (Rating)
- `Pago` (Payment)
- `Comision` (Commission)

**Pregúntate:**
- `Repartidor` y `Restaurante` son subtipos de `Usuario` o entidades separadas?
- `Ubicacion` es un value object (inmutable, sin identidad propia)?
- `Pedido` contiene la dirección de entrega o es un valor calculado?
- ¿`ItemMenu` tiene precio variable por zona?

### ✏️ Paso 5: Reglas

Enuncia al menos 10 reglas de negocio.

**Áreas a cubrir:**
- Asignación de repartidores (distancia máxima, capacidad)
- Tiempo máximo de espera para aceptar pedido
- Cancelaciones (quién puede cancelar y en qué estados)
- Pagos (contra entrega vs online)
- Tarifas de envío (distancia, hora del día, demanda)
- Calificaciones (solo pedidos entregados, período de 7 días)
- Comisiones de la plataforma
- Disponibilidad de items (no pedir items agotados)

---

## Sección 2: Mapeo a Capas

### ✏️ Paso 1: Estructura DOMAIN

Dibuja el árbol de `domain/`:

```
domain/
├── entities/
│   ├── user.dart
│   ├── restaurant.dart
│   ├── menu_item.dart
│   ├── order.dart
│   ├── order_item.dart
│   ├── delivery_person.dart
│   ├── rating.dart
│   └── payment.dart
├── value_objects/
│   ├── location.dart
│   └── money.dart
├── usecases/
│   ├── browse_restaurants.dart
│   ├── place_order.dart
│   ├── accept_order.dart
│   ├── assign_delivery.dart
│   ├── track_order.dart
│   ├── cancel_order.dart
│   ├── update_location.dart
│   ├── complete_delivery.dart
│   └── rate_order.dart
├── repositories/
│   ├── restaurant_repository.dart
│   ├── order_repository.dart
│   ├── delivery_repository.dart
│   └── payment_repository.dart
├── services/
│   ├── location_service.dart (interface)
│   └── payment_service.dart (interface)
└── core/
    └── failures.dart
```

**Pregúntate:**
- ¿`Location` es value object porque dos ubicaciones con mismas coordenadas son iguales?
- ¿`track_order` es un UseCase o es parte del Cubit vía Stream?
- ¿`browse_restaurants` necesita geolocalización o recibe lat/lng como parámetro?

### ✏️ Paso 2: Estructura DATA

Dibuja el árbol de `data/`:

```
data/
├── datasources/
│   ├── restaurant_remote_datasource.dart
│   ├── order_remote_datasource.dart
│   ├── order_realtime_datasource.dart  ← WebSockets/Streams
│   └── location_datasource.dart        ← GPS del dispositivo
├── models/
│   ├── restaurant_model.dart
│   ├── order_model.dart
│   ├── user_model.dart
│   └── location_model.dart
└── repositories/
    ├── restaurant_repository_impl.dart
    ├── order_repository_impl.dart
    ├── delivery_repository_impl.dart
    └── payment_repository_impl.dart
```

**Pregúntate:**
- La actualización en tiempo real de ubicación, ¿va por WebSocket o polling?
- ¿La ubicación GPS es un DataSource o un Service?
- ¿Necesitas un DataSource especial para streams o con el remoto alcanza?

### ✏️ Paso 3: Estructura PRESENTATION

Dibuja el árbol de `presentation/`:

```
presentation/
├── cubit/
│   ├── restaurant_list_cubit.dart
│   ├── menu_cubit.dart
│   ├── cart_cubit.dart
│   ├── checkout_cubit.dart
│   ├── order_tracking_cubit.dart
│   ├── delivery_cubit.dart
│   └── ratings_cubit.dart
├── pages/
│   ├── home_page.dart
│   ├── restaurant_detail_page.dart
│   ├── cart_page.dart
│   ├── order_tracking_page.dart
│   ├── delivery_home_page.dart
│   └── restaurant_orders_page.dart
└── widgets/
    ├── restaurant_card.dart
    ├── menu_item_tile.dart
    ├── order_status_timeline.dart
    ├── delivery_map.dart
    └── rating_widget.dart
```

**Pregúntate:**
- ¿Cuántos Cubits necesitas realmente?
- El mapa de rastreo, ¿es un widget o una página?
- ¿El flujo del repartidor es una app separada o la misma app con otro rol?

---

## Sección 3: Contratos

### ✏️ Paso 1: Contrato OrderRepository

```dart
abstract class OrderRepository {
  // CRUD de pedidos
  // Transiciones de estado
  // Consultas con filtros
  // Streams para actualizaciones en tiempo real
}
```

### ✏️ Paso 2: Contrato DeliveryRepository

```dart
abstract class DeliveryRepository {
  // Asignar repartidor
  // Obtener pedidos disponibles cercanos
  // Actualizar ubicación del repartidor
  // Stream de ubicación del repartidor
}
```

### ✏️ Paso 3: Contrato LocationService

```dart
abstract class LocationService {
  // Obtener ubicación actual del dispositivo
  // Stream de ubicación en tiempo real
  // Calcular distancia entre dos puntos
}
```

### ✏️ Paso 4: Contrato para Realtime

El tracking en tiempo real es un caso especial. Necesitas contratos que retornen Streams:

```dart
abstract class OrderRealtimeDataSource {
  // Stream que emite cambios del pedido en tiempo real
  Stream<OrderModel> watchOrder(String orderId);

  // Stream que emite ubicación del repartidor
  Stream<LocationModel> watchDeliveryLocation(String deliveryPersonId);

  // Emitir nueva ubicación del repartidor
  Future<void> updateLocation(String deliveryPersonId, LocationModel location);
}
```

**Pregúntate:**
- ¿El Stream se cierra cuando el pedido se entrega?
- ¿Cómo manejas la reconexión si se pierde el WebSocket?
- ¿El UseCase retorna un Stream o el Cubit se suscribe directamente?

### ✏️ Paso 5: ADR

Escribe al menos un ADR. Ejemplos:
- ¿La asignación de repartidores es automática (algoritmo) o manual (repartidor elige)?
- ¿La tarifa de envío se calcula por distancia fija o por demanda (surge pricing)?
- ¿El tracking en tiempo real usa WebSockets (Supabase Realtime) o polling?

---

## Sección 4: Flujo de Datos

### ✏️ Paso 1: Flujo Completar Pedido (Cliente → Restaurante → Repartidor → Cliente)

Dibuja la secuencia completa del ciclo de vida de un pedido:

```
Cliente                       Restaurante              Repartidor                Cliente
  │                              │                        │                        │
  │── Pedido ──────────────────▶ │                        │                        │
  │                              │── Aceptar ────────────▶│                        │
  │                              │                        │── En camino al resto ──▶│
  │                              │── Preparando           │                        │
  │                              │── Listo ──────────────▶│                        │
  │                              │                        │── Recogido             │
  │                              │                        │── En camino ──────────▶│
  │                              │                        │                        │
  │◀───────────────────────────────────────────────────── Entregado ─────────────│
  │                              │                        │                        │
  │── Calificar ───────────────▶│────────────────────────▶│                        │
```

**Incluye:**
- Para cada flecha, identifica qué capa procesa la acción
- Dónde se emiten los eventos de cambio de estado
- Dónde se actualiza la UI en tiempo real
- Manejo de errores (repartidor no acepta, restaurante rechaza, pago falla)

### ✏️ Paso 2: Flujo de Asignación de Repartidor

Dibuja el flujo cuando un pedido está listo y se necesita asignar un repartidor.

**Pregúntate:**
- ¿El sistema asigna automáticamente al repartidor más cercano?
- ¿O los repartidores ven una lista de pedidos disponibles y aceptan?
- ¿Qué pasa si ningún repartidor acepta en X minutos?
- ¿Cómo se actualiza la UI del cliente mientras se asigna un repartidor?

### ✏️ Paso 3: Flujo de Tracking en Tiempo Real

Dibuja el flujo de datos desde que el repartidor se mueve hasta que el cliente ve su ubicación en el mapa.

**Considera:**
- GPS del repartidor → DataSource → Supabase Realtime → Stream en Cubit → Widget de mapa
- Frecuencia de actualización de ubicación
- Manejo de pérdida de conexión
- Actualización de tiempo estimado de llegada

---

## Solución Sugerida

> ⚠️ Resuelve cada sección en papel primero. La solución sugerida es para comparar después.

### ✅ FADER Completo

```
╔═══════════════════════════════════════════════════════════════╗
║  FEATURE: App de Delivery                                     ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [F]ormular:                                                  ║
║  F1: Como cliente, quiero pedir comida de restaurantes       ║
║      cercanos para recibirla en mi casa.                      ║
║  F2: Como restaurante, quiero gestionar pedidos entrantes    ║
║      para prepararlos a tiempo.                               ║
║  F3: Como repartidor, quiero ver pedidos disponibles         ║
║      cercanos para elegir los que me convengan.              ║
║  F4: Como cliente, quiero rastrear a mi repartidor en        ║
║      tiempo real para saber cuándo llega mi pedido.          ║
║                                                               ║
║  [A]ctorizar:                                                 ║
║  1. Cliente (primario)                                        ║
║     - Ver restaurantes, menú, hacer pedido, rastrear,         ║
║       calificar, historial                                     ║
║  2. Restaurante (secundario)                                  ║
║     - Gestionar menú, aceptar/rechazar pedidos,               ║
║       marcar estados, ver historial                            ║
║  3. Repartidor (secundario)                                   ║
║     - Ver pedidos disponibles, aceptar, actualizar estados,   ║
║       compartir ubicación                                      ║
║  4. Admin (terciario)                                         ║
║     - Gestionar usuarios, comisiones, reportes               ║
║  5. Pasarela de Pagos (externa)                               ║
║  6. API de Mapas (externa) — Google Maps, Mapbox             ║
║                                                               ║
║  [D]escomponer:                                               ║
║  Cliente:                                                     ║
║  - [R] Ver restaurantes cercanos (geolocalización)           ║
║  - [R] Ver menú del restaurante                               ║
║  - [C] Agregar item al carrito                                ║
║  - [C] Hacer pedido (checkout)                               ║
║  - [R] Rastrear pedido (stream en tiempo real)                ║
║  - [U] Cancelar pedido (solo en estados iniciales)           ║
║  - [C] Calificar (restaurante + repartidor)                  ║
║                                                               ║
║  Restaurante:                                                 ║
║  - [CRUD] Gestionar items del menú                           ║
║  - [R] Ver pedidos entrantes (stream en tiempo real)         ║
║  - [U] Aceptar pedido                                         ║
║  - [U] Rechazar pedido (con motivo)                          ║
║  - [U] Marcar "en preparación"                                ║
║  - [U] Marcar "listo"                                         ║
║                                                               ║
║  Repartidor:                                                  ║
║  - [R] Ver pedidos disponibles cercanos                       ║
║  - [U] Aceptar entrega                                        ║
║  - [U] Marcar "en camino al restaurante"                     ║
║  - [U] Marcar "recogido"                                      ║
║  - [U] Marcar "en camino al cliente"                          ║
║  - [U] Marcar "entregado"                                     ║
║  - [C] Compartir ubicación (stream de GPS)                   ║
║                                                               ║
║  Sistema:                                                     ║
║  - [Cálculo] Calcular tarifa de envío (distancia)            ║
║  - [Cálculo] Estimar tiempo de entrega                       ║
║  - [Validación] Validar cobertura (¿el restaurante           ║
║    entrega en esa zona?)                                      ║
║  - [Transición] Re-asignar si repartidor no avanza           ║
║  - [Transición] Notificar cambios de estado                  ║
║                                                               ║
║  [E]ntidades:                                                 ║
║  Usuario: id, nombre, email, telefono, rol,                   ║
║           ubicacionActual, activo                              ║
║  Restaurante: id, nombre, direccion, ubicacion,               ║
║               categoria, rating, tiempoEstimado,              ║
║               activo, fotoUrl                                  ║
║  ItemMenu: id, restauranteId, nombre, descripcion,            ║
║            precio, categoria, disponible, fotoUrl              ║
║  Pedido: id, clienteId, restauranteId, repartidorId?,        ║
║          items, estado, subtotal, tarifaEnvio, total,          ║
║          direccionEntrega, ubicacionEntrega,                  ║
║          metodoPago, tiempoEstimado,                           ║
║          fechaCreacion, fechaEntregado                        ║
║  ItemPedido: productoId, nombre, cantidad, precioUnitario    ║
║  EstadoPedido (enum): pendiente, confirmado,                 ║
║    enPreparacion, listo, enCaminoAlResto, recogido,          ║
║    enCaminoAlCliente, entregado, cancelado                    ║
║  Pago: id, pedidoId, monto, metodo, estado,                  ║
║        referenciaExterna                                       ║
║  Calificacion: id, pedidoId, usuarioId,                       ║
║                puntuacion, comentario, fecha                  ║
║  Ubicacion (value object): latitud, longitud                 ║
║                                                               ║
║  [R]eglas:                                                    ║
║  R001: El repartidor no puede tener más de 1 pedido          ║
║        activo a la vez                                        ║
║  R002: El cliente puede cancelar solo si estado es            ║
║        pendiente o confirmado                                 ║
║  R003: El restaurante tiene 3 minutos para aceptar            ║
║        o rechazar un pedido entrante                          ║
║  R004: Si el restaurante no responde en 3 min,               ║
║        el pedido se cancela automáticamente                   ║
║  R005: La tarifa de envío es $1.5/km desde el                ║
║        restaurante al cliente                                 ║
║  R006: El repartidor solo puede ser asignado si está         ║
║        a menos de 2km del restaurante                         ║
║  R007: El pago se procesa al hacer el pedido si es           ║
║        online; al entregar si es efectivo                     ║
║  R008: Solo se puede calificar si el pedido fue              ║
║        entregado                                              ║
║  R009: La calificación debe hacerse dentro de los 7          ║
║        días posteriores a la entrega                         ║
║  R010: Si el repartidor no se mueve por 5 minutos,          ║
║        notificar al admin para re-asignación                 ║
║  R011: No se puede pedir un item no disponible               ║
║  R012: El restaurante solo entrega en un radio               ║
║        máximo de 5km                                          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### ✅ Contrato OrderRepository

```dart
abstract class OrderRepository {
  // Comandos
  Future<Either<Failure, Order>> placeOrder(PlaceOrderParams params);
  Future<Either<Failure, Order>> cancelOrder(
    String orderId, String reason);
  Future<Either<Failure, Order>> acceptOrder(String orderId);
  Future<Either<Failure, Order>> rejectOrder(
    String orderId, String reason);

  // Transiciones de estado
  Future<Either<Failure, Order>> markPreparing(String orderId);
  Future<Either<Failure, Order>> markReady(String orderId);
  Future<Either<Failure, Order>> markPickedUp(String orderId);
  Future<Either<Failure, Order>> markDelivered(String orderId);

  // Consultas
  Future<Either<Failure, Order>> getOrder(String orderId);
  Future<Either<Failure, List<Order>>> getOrdersByStatus(
    String userId, OrderStatus status);

  // Streams en tiempo real
  Stream<Either<Failure, Order>> watchOrder(String orderId);
  Stream<Either<Failure, List<Order>>> watchRestaurantOrders(
    String restaurantId);
}
```

### ✅ Contrato DeliveryRepository

```dart
abstract class DeliveryRepository {
  Future<Either<Failure, List<Order>>> getAvailableOrders(
    Location nearLocation, double radiusKm);

  Future<Either<Failure, Order>> acceptDelivery(
    String orderId, String deliveryPersonId);

  Future<Either<Failure, void>> updateLocation(
    String deliveryPersonId, Location location);

  Stream<Location> watchDeliveryLocation(String deliveryPersonId);

  Future<Either<Failure, double>> calculateDeliveryFee(
    Location restaurantLocation, Location customerLocation);
}
```

### ✅ ADR Sugerido

```markdown
# ADR-006: Tracking en Tiempo Real con Supabase Realtime

## Contexto
El cliente debe ver la ubicación del repartidor en tiempo real
y los cambios de estado del pedido sin recargar la página.

## Decisión
Usaremos Supabase Realtime (WebSockets) para:
1. Suscribirse a cambios en la tabla `orders` (cambios de estado)
2. Suscribirse a cambios en la tabla `delivery_locations` (ubicación)
   usando la capacidad de Broadcast de Supabase Realtime
3. El repartidor emite su ubicación cada 3 segundos desde el GPS
4. El cliente recibe actualizaciones vía Stream en el Cubit

## Consecuencias
Positivas:
- Sin servidor propio de WebSockets
- Escalable (Supabase maneja la conexión)
- Integración directa con Flutter (supabase_flutter)

Negativas:
- Costo de suscripción Realtime en producción
- Latencia de 1-3 segundos (suficiente para tracking)
- Dependencia de conectividad a internet

## Alternativas consideradas
1. Polling HTTP cada 5 segundos:
   Descartado: mayor latencia, más requests, peor experiencia.
2. Firebase Realtime Database:
   Descartado: ya usamos Supabase, no queremos dos backends.
3. WebSocket propio con server-sent events:
   Descartado: sobreingeniería, Supabase Realtime ya resuelve esto.
```

### ✅ Flujo de Asignación de Repartidor (diagrama)

```
PEDIDO CONFIRMADO (restaurante aceptó, comida en preparación)
         │
         ▼
┌──────────────────────────────────────────┐
│  SISTEMA: Buscar repartidores            │
│  disponibles en un radio de 2km          │
│  del restaurante (R006)                  │
└──────────────────────────────────────────┘
         │
         ├── ¿Hay repartidores? ──Sí──▶ Notificar a repartidores
         │                                   cercanos con el pedido
         │                                   │
         │                                   ▼
         │                           ┌────────────────────┐
         │                           │  REPARTIDOR        │
         │                           │  Ve pedido en      │
         │                           │  lista disponibles │
         │                           └────────┬───────────┘
         │                                    │
         │                            ┌───────┴────────┐
         │                            │  ¿Acepta?      │
         │                            └───────┬────────┘
         │                           ┌───────┴────────┐
         │                           │  Sí ──▶ Asignado│
         │                           │  No  ──▶ Sigue  │
         │                           │         buscando│
         │                           └────────────────┘
         │
         └── No hay repis ──▶ Esperar 30s y reintentar
                              │
                              ├── 3 intentos sin éxito ──▶
                              │   Cancelar pedido con motivo
                              │   "No hay repartidores disponibles"
                              │
                              └── Aparece repi ──▶ Asignar
```

---

## 🚀 Siguiente paso

Con estos casos completados, tienes un repertorio sólido de patrones de diseño. Vuelve a aplicar FADER a cualquier feature que enfrentes en tu trabajo real.

---

**Tiempo estimado:** 2-3 horas  
**Material:** Papel y lápiz
