# 07 — Prácticas y Ejercicios de Debugging en VS Code

> Escenarios reales de debugging con BLoC/Cubit, Supabase, GoRouter y UI, más un ejercicio integrador de pagos y un checklist.

---

## 1. Escenario 1: Debugging de BLoC/Cubit con estado

### 1.1 Contexto

Tienes un `AuthCubit` que maneja login de usuarios. El estado no se actualiza correctamente después del login.

### 1.2 Setup del proyecto

**`lib/features/auth/presentation/cubit/auth_cubit.dart`**

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

part 'auth_state.dart';

class AuthCubit extends Cubit<AuthState> {
  final LoginUseCase _loginUseCase;

  AuthCubit(this._loginUseCase) : super(AuthInitial());

  Future<void> login(String email, String password) async {
    emit(AuthLoading());
    try {
      final user = await _loginUseCase(email, password);
      emit(AuthSuccess(user));  // ← Breakpoint aquí
    } catch (e) {
      emit(AuthFailure(e.toString()));  // ← Y aquí
    }
  }

  void logout() {
    emit(AuthInitial());  // ← Y aquí
  }
}
```

**`lib/features/auth/presentation/cubit/auth_state.dart`**

```dart
part of 'auth_cubit.dart';

sealed class AuthState extends Equatable {
  @override
  List<Object?> get props => [];
}

final class AuthInitial extends AuthState {}
final class AuthLoading extends AuthState {}

final class AuthSuccess extends AuthState {
  final dynamic user;
  AuthSuccess(this.user);
  @override
  List<Object?> get props => [user];
}

final class AuthFailure extends AuthState {
  final String message;
  AuthFailure(this.message);
  @override
  List<Object?> get props => [message];
}
```

### 1.3 Ejercicio paso a paso

#### Paso 1: Configurar launch.json

```json
{
  "name": "Debug Auth Flow",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "dartDefine": ["ENV=debug"]
}
```

#### Paso 2: Breakpoints condicionales

En `auth_cubit.dart`, sobre el `emit(AuthLoading())`:
- Click derecho → Add Conditional Breakpoint → Expression
- Expresión: `email.isEmpty || password.isEmpty`
- **Resultado**: solo pausa si intentan loguear sin credenciales

#### Paso 3: Agregar watches

En el panel WATCH, agregar:

```
email
password
state
state.runtimeType
```

#### Paso 4: Ejecutar y depurar

1. `F5` para iniciar
2. Intentar login con email vacío → debe pausar en el breakpoint condicional
3. `F10` (Step Over) para ver la transición de estados
4. En Debug Console: `state.props` para ver los datos del estado actual

#### Paso 5: Detectar el bug

Si el estado queda en `AuthLoading()` y nunca llega a `AuthSuccess`, usar:
- `F11` (Step Into) en `await _loginUseCase(email, password)` para entrar al use case
- Verificar si la excepción se está lanzando correctamente
- Verificar que `emit(AuthSuccess(user))` se ejecuta

---

## 2. Escenario 2: Debugging de llamada API con error inesperado

### 2.1 Contexto

Una llamada HTTP a Supabase retorna status 200 pero el body está vacío o en formato inesperado.

### 2.2 Setup del proyecto

**`lib/features/products/data/datasources/product_remote_datasource.dart`**

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ProductRemoteDatasource {
  final String baseUrl;
  final String apiKey;

  ProductRemoteDatasource({required this.baseUrl, required this.apiKey});

  Future<List<ProductModel>> getProducts() async {
    final response = await http.get(
      Uri.parse('$baseUrl/rest/v1/products'),
      headers: {
        'apikey': apiKey,
        'Authorization': 'Bearer $apiKey',
        'Content-Type': 'application/json',
      },
    );

    // ← Breakpoint aquí

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = json.decode(response.body);
      return jsonList.map((json) => ProductModel.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load products: ${response.statusCode}');
    }
  }
}
```

### 2.3 Ejercicio paso a paso

#### Paso 1: Agregar breakpoint condicional

En la línea `if (response.statusCode == 200)`:
- Click derecho → Add Conditional Breakpoint → Expression
- Expresión: `response.statusCode != 200 || response.body.isEmpty`
- **Resultado**: pausa si status no es 200 O si el body está vacío

#### Paso 2: Logpoint (alternativa)

- Click derecho → Add Logpoint
- Mensaje: `Status: {response.statusCode}, Body length: {response.body.length}`
- No pausa la ejecución pero loggea en Debug Console

#### Paso 3: Ejecutar y diagnosticar

1. `F5` para iniciar
2. El logpoint muestra: `Status: 200, Body length: 0`
3. Agregar watch: `response.body`
4. En Debug Console:
   ```dart
   response.body.isEmpty  // true
   response.headers       // ver content-type
   ```

#### Paso 4: El bug está en...

Response viene vacío → verificar:
- API key correcta
- RLS policies en Supabase (¡causa común!)
- Filtros en la query

#### Paso 5: Fix y verificación

```dart
// Agregar verificación explícita
if (response.statusCode == 200) {
  if (response.body.isEmpty) {
    throw Exception('Empty response - check RLS policies');
  }
  final List<dynamic> jsonList = json.decode(response.body);
  return jsonList.map((json) => ProductModel.fromJson(json)).toList();
}
```

---

## 3. Escenario 3: Debugging de GoRouter y navegación

### 3.1 Contexto

La navegación con GoRouter no funciona como se espera. El usuario hace click en un botón pero la ruta no cambia.

### 3.2 Setup del proyecto

**`lib/core/router/app_router.dart`**

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

final goRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/products/:id',
      builder: (context, state) {
        final productId = state.pathParameters['id']!;
        // ← Breakpoint aquí
        return ProductScreen(productId: productId);
      },
    ),
    GoRoute(
      path: '/products/:id/reviews',
      builder: (context, state) {
        final productId = state.pathParameters['id']!;
        final filter = state.uri.queryParameters['filter'] ?? 'all';
        // ← Breakpoint aquí
        return ReviewsScreen(productId: productId, filter: filter);
      },
    ),
  ],
);
```

### 3.3 Ejercicio paso a paso

#### Paso 1: Breakpoint condicional

En la ruta `/products/:id`:
- Click derecho → Add Conditional Breakpoint → Expression
- Expresión: `productId.isEmpty || productId == "null"`
- **Resultado**: pausa si el ID no se extrae correctamente

#### Paso 2: Usar Log Message para debug no intrusivo

```dart
// En el builder de las rutas (solo en debug):
if (kDebugMode) {
  debugPrint('[GoRouter] Navegando a: ${state.uri}');
  debugPrint('[GoRouter] Path params: ${state.pathParameters}');
  debugPrint('[GoRouter] Query params: ${state.queryParameters}');
}
```

#### Paso 3: Watches útiles

```
state.uri
state.pathParameters
state.queryParameters
state.matchedLocation
state.name
```

#### Paso 4: Diagnóstico típico

Si `productId` es `"null"` (string):
- El parámetro `:id` no se está pasando en la navegación
- Verificar `context.go('/products/${product.id}')` en el widget que navega
- Verificar que el `id` no sea null en el modelo

---

## 4. Escenario 4: Debugging de UI y layouts

### 4.1 Contexto

Un widget se renderiza con tamaños incorrectos. Necesitas ver las dimensiones exactas.

### 4.2 Setup

**`lib/features/home/presentation/widgets/product_card.dart`**

```dart
class ProductCard extends StatelessWidget {
  final Product product;

  const ProductCard({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    // ← Breakpoint aquí
    return Container(
      width: double.infinity,
      height: 120,
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          Expanded(
            flex: 2,
            child: Image.network(product.imageUrl),
          ),
          Expanded(
            flex: 3,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(product.name, style: Theme.of(context).textTheme.titleLarge),
                Text(product.description),
                Text('\$${product.price}'),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### 4.3 Ejercicio paso a paso

#### Paso 1: Usar el Widget Inspector para entender el árbol

1. Poner breakpoint en `build`
2. `F5` hasta que pare
3. En VARIABLES, expandir `this` → ver propiedades del widget
4. Abrir DevTools → Widget Inspector para ver el árbol completo

#### Paso 2: Debug Console para inspeccionar

```dart
// En Debug Console durante el breakpoint
product.name              // ver nombre
product.imageUrl          // ver URL
product.price             // ver precio
product.description.length  // ver longitud
```

#### Paso 3: Verificar constraints

Agregar temporalmente:

```dart
LayoutBuilder(
  builder: (context, constraints) {
    // ← Breakpoint aquí
    debugPrint('Constraints: $constraints');
    return Container(/* ... */);
  },
)
```

En Debug Console:

```
constraints.maxWidth   // ancho máximo disponible
constraints.minWidth   // ancho mínimo
constraints.maxHeight  // alto máximo
```

#### Paso 4: Usar Flutter DevTools Inspector

1. Abrir DevTools desde VS Code (`Ctrl+Shift+D` → DevTools)
2. Seleccionar el widget en el árbol
3. Ver propiedades de layout: width, height, constraints
4. Activar "Toggle Debug Paint" (Toggle Repaint Rainbow / Debug Paint) para ver borders

---

## 5. Escenario 5: Debugging de Supabase Realtime

### 5.1 Contexto

Las actualizaciones en tiempo real no llegan al widget.

### 5.2 Setup

**`lib/features/chat/data/datasources/chat_realtime_datasource.dart`**

```dart
import 'dart:async';
import 'package:supabase_flutter/supabase_flutter.dart';

class ChatRealtimeDatasource {
  final SupabaseClient _client;
  final _messagesController = StreamController<Map<String, dynamic>>.broadcast();

  Stream<Map<String, dynamic>> get messagesStream => _messagesController.stream;

  ChatRealtimeDatasource(this._client) {
    _subscribeToMessages();
  }

  void _subscribeToMessages() {
    _client
        .from('messages')
        .stream(primaryKey: ['id'])
        .order('created_at', ascending: false)
        .limit(50)
        .listen((data) {
      // ← Breakpoint aquí
      _messagesController.add(data);
    }, onError: (error) {
      // ← Breakpoint aquí también
      _messagesController.addError(error);
    });

    // ← Breakpoint aquí para verificar la suscripción
  }

  Future<void> sendMessage(String content) async {
    await _client.from('messages').insert({
      'content': content,
      'user_id': _client.auth.currentUser?.id,
      'created_at': DateTime.now().toIso8601String(),
    });
  }

  void dispose() {
    _client.channel('messages').unsubscribe();
    _messagesController.close();
  }
}
```

### 5.3 Ejercicio paso a paso

#### Paso 1: Verificar conexión

Poner breakpoint en el `.listen((data) {...})`:
- ¿Se ejecuta alguna vez? Si no → problema de suscripción
- ¿Se ejecuta con error? → problema de conexión/RLS

#### Paso 2: Watches para diagnóstico

```
data
data.length
data.isEmpty
_client.auth.currentUser?.id
```

#### Paso 3: Logs detallados

```dart
_client
    .from('messages')
    .stream(primaryKey: ['id'])
    .order('created_at', ascending: false)
    .limit(50)
    .listen((data) {
  debugPrint('=== REALTIME UPDATE ===');
  debugPrint('Records: ${data.length}');
  debugPrint('First record: ${data.firstOrNull}');
  debugPrint('Channel status: ${_client.channel('messages').status}');
  _messagesController.add(data);
}, onError: (error) {
  debugPrint('=== REALTIME ERROR ===');
  debugPrint('Error: $error');
  debugPrint('Type: ${error.runtimeType}');
  _messagesController.addError(error);
});
```

#### Paso 4: Diagnóstico común

1. ¿Las RLS policies permiten SELECT? → `supabase.from('messages').select()`
2. ¿La tabla tiene replica identity? → `ALTER TABLE messages REPLICA IDENTITY FULL;`
3. ¿El channel se suscribió correctamente?
4. ¿Hay errores en Supabase Dashboard → Database → Replication?

---

## 6. Ejercicio Integrador: Debug completo de feature de pagos

### 6.1 Contexto

App Flutter con arquitectura limpia que integra pasarela de pagos. Los usuarios reportan que el pago "se queda cargando" sin completarse.

### 6.2 Archivos del ejercicio

**`lib/features/payments/presentation/bloc/payment_bloc.dart`**

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

part 'payment_event.dart';
part 'payment_state.dart';

class PaymentBloc extends Bloc<PaymentEvent, PaymentState> {
  final ProcessPaymentUseCase _processPayment;
  final VerifyPaymentUseCase _verifyPayment;

  PaymentBloc(this._processPayment, this._verifyPayment)
      : super(PaymentInitial()) {
    on<ProcessPayment>(_onProcessPayment);
    on<VerifyPaymentStatus>(_onVerifyPayment);
  }

  Future<void> _onProcessPayment(
    ProcessPayment event,
    Emitter<PaymentState> emit,
  ) async {
    emit(PaymentProcessing());

    try {
      // ← Breakpoint 1: ¿Se llega aquí?
      final result = await _processPayment(PaymentParams(
        amount: event.amount,
        currency: event.currency,
        productId: event.productId,
      ));

      // ← Breakpoint 2: ¿Se obtiene resultado?

      if (result.requires3DS) {
        emit(Payment3DSRequired(result.paymentUrl));
        // ← Breakpoint 3: ¿Se emite este estado?
        return;
      }

      if (result.status == PaymentStatus.success) {
        emit(PaymentSuccess(result.transactionId));
      } else {
        emit(PaymentFailure(result.errorMessage ?? 'Unknown error'));
      }
    } catch (e, stackTrace) {
      // ← Breakpoint 4: ¿Se captura error?
      emit(PaymentFailure(e.toString()));
    }
  }

  Future<void> _onVerifyPayment(
    VerifyPaymentStatus event,
    Emitter<PaymentState> emit,
  ) async {
    emit(PaymentVerifying());
    try {
      final status = await _verifyPayment(event.transactionId);
      // ← Breakpoint 5
      if (status == PaymentStatus.success) {
        emit(PaymentSuccess(event.transactionId));
      } else if (status == PaymentStatus.pending) {
        // ← Breakpoint 6: ¿Se queda en loop aquí?
        emit(PaymentVerifying());
      } else {
        emit(PaymentFailure('Payment failed'));
      }
    } catch (e) {
      emit(PaymentFailure(e.toString()));
    }
  }
}
```

### 6.3 Ejercicio paso a paso

#### Paso 1: Mapear los breakpoints

Agregar breakpoints en los 6 puntos marcados con comentarios.

#### Paso 2: Configurar watches iniciales

```
event.amount
event.currency
event.productId
state
state.runtimeType
```

#### Paso 3: Ejecutar escenarios

**Escenario A — Pago exitoso:**
1. Iniciar debugging
2. Llenar formulario de pago
3. Verificar: ¿Pasa por Breakpoint 1? ¿2? ¿Resultado?
4. Si falla en 2 → el use case lanza excepción

**Escenario B — Pago 3DS:**
1. Usar tarjeta que requiere 3DS
2. Verificar: ¿Se emite `Payment3DSRequired`?
3. Después de 3DS → verificar `VerifyPaymentStatus`

**Escenario C — Pago quedando en "cargando":**
1. Usar tarjeta que causa timeout
2. Verificar: ¿Llega a Breakpoint 3 o 4?
3. Si se queda en `PaymentProcessing()` → problema en el use case

#### Paso 4: Diagnosticar causa raíz

**Causa más común: el verify loop**

```dart
// BUG: Si el verify retorna pending, se re-emite PaymentVerifying
// pero NO se re-intenta el verify → loop infinito de UI
if (status == PaymentStatus.pending) {
  emit(PaymentVerifying());
  // ← FALTA: await Future.delayed(...) y re-enviar el evento
}
```

**Fix:**

```dart
if (status == PaymentStatus.pending) {
  emit(PaymentVerifying());
  // Re-verificar después de 3 segundos
  await Future.delayed(const Duration(seconds: 3));
  if (!isClosed) {
    add(VerifyPaymentStatus(event.transactionId));
  }
}
```

#### Paso 5: Verificar con Debug Console

```dart
// Durante el debugging, en Debug Console:
state.runtimeType          // Ver estado actual
event.amount               // Ver monto
event.productId            // Ver producto
result.transactionId       // Ver ID de transacción
result.requires3DS         // Ver si requiere 3DS
result.errorMessage        // Ver mensaje de error
```

---

## 7. Checklist de debugging

Antes de depurar cualquier bug:
- [ ] ¿Puedo reproducir el bug consistentemente?
- [ ] ¿Entiendo el flujo de datos? (BLoC → UseCase → DataSource)
- [ ] ¿Los breakpoints están en los puntos correctos del flujo?
- [ ] ¿Tengo watches configurados para variables clave?
- [ ] ¿Verifiqué los logs en Debug Console?
- [ ] ¿Revisé el estado del BLoC/Cubit?
- [ ] ¿Verifiqué la respuesta de la API (Network en DevTools)?
- [ ] ¿Revisé las RLS policies si uso Supabase?

---

## Resumen

- Depurar con **breakpoints + watches** siguiendo el flujo completo: BLoC/Cubit → UseCase → DataSource → UI.
- Usar **DevTools (Network view)** para validar respuestas de Supabase y revisar las **RLS policies** cuando hay datos inesperados.
- En layouts, usar el **Inspector** para detectar sobreflujo (`RenderFlex overflowed`) y revisar constraints.
- Con **Realtime**, verificar suscripción, canal y políticas RLS antes de tocar la UI.
- El ejercicio integrador de **pagos** combina todos los escenarios; el **checklist** es la puerta de entrada antes de depurar cualquier bug.

---

## 📚 Referencias

- [Flutter | DevTools](https://docs.flutter.dev/tools/devtools) — Widget Inspector, Network view y más
- [Supabase | Realtime](https://supabase.com/docs/guides/realtime) — Postgres Changes y suscripciones
- [GoRouter | API](https://pub.dev/documentation/go_router/latest/) — Path y query parameters
- [flutter_bloc | API](https://pub.dev/documentation/flutter_bloc/latest/) — Bloc y Cubit

---

> 📖 **Siguiente:** [08-fundamentos-devtools.md](./08-fundamentos-devtools.md) — Introducción a Flutter DevTools y sus vistas
