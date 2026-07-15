# 07 - Prácticas y Ejercicios - VSCode Debugging

## Escenario 1: Debugging de BLoC/Cubit con estado

### Contexto
Tienes un `AuthCubit` que maneja login de usuarios. El estado no se actualiza correctamente después del login.

### Setup del proyecto

**`lib/features/auth/presentation/cubit/auth_cubit.dart`**
```dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';

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

### Ejercicio paso a paso

#### Paso 1: Configurar launch.json
```json
{
  "name": "Debug Auth Flow",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "args": ["--dart-define=ENV=debug"]
}
```

#### Paso 2: Breakpoints condicionales
En `auth_cubit.dart` línea del `emit(AuthLoading())`:
- Right-click → Breakpoint → Expression
- Expresión: `email.isEmpty || password.isEmpty`
- **Resultado**: Solo pausa si intentan loguear sin credenciales

#### Paso 3: Agregar watches
En el panel VARIABLES/WATCH, agregar:
```
email
password
state
state.runtimeType
```

#### Paso 4: Ejecutar y depurar
1. `F5` para iniciar
2. Intentar login con email vacío → Debe pausar en breakpoint condicional
3. `F10` (Step Over) para ver transición de estados
4. En Debug Console: `state.props` para ver datos del estado actual

#### Paso 5: Detectar el bug
Si el estado queda en `AuthLoading()` y nunca llega a `AuthSuccess`, usar:
- `F11` (Step Into) en `await _loginUseCase(email, password)` para entrar al use case
- Verificar si la excepción se está lanzando correctamente
- Verificar que `emit(AuthSuccess(user))` se ejecuta

---

## Escenario 2: Debugging de llamada API con error inesperado

### Contexto
Una llamada HTTP a Supabase retorna status 200 pero el body está vacío o en formato inesperado.

### Setup del proyecto

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

### Ejercicio paso a paso

#### Paso 1: Agregar breakpoint condicional
En la línea `if (response.statusCode == 200)`:
- Right-click → Breakpoint → Expression
- Expresión: `response.statusCode != 200 || response.body.isEmpty`
- **Resultado**: Pausa si status no es 200 O si body está vacío

#### Paso 2: Log Message breakpoint (alternativa)
- Right-click → Breakpoint → Log Message
- Message: `Status: ${response.statusCode}, Body length: ${response.body.length}`
- No pausa la ejecución pero loggea en Debug Console

#### Paso 3: Ejecutar y diagnosticar
1. `F5` para iniciar
2. Log Message muestra: `Status: 200, Body length: 0`
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

## Escenario 3: Debugging de GoRouter y navegación

### Contexto
La navegación con GoRouter no funciona como se espera. El usuario hace click en un botón pero la ruta no cambia.

### Setup del proyecto

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

### Ejercicio paso a paso

#### Paso 1: Breakpoint condicional
En la ruta `/products/:id`:
- Right-click → Breakpoint → Expression
- Expresión: `productId.isEmpty || productId == "null"`
- **Resultado**: Pausa si el ID no se extrae correctamente

#### Paso 2: Usar Log Message para debug no intrusivo
```json
{
  "name": "Debug GoRouter",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "args": ["--dart-define=GO_ROUTER_DEBUG=true"]
}
```

```dart
// En router, agregar log condicional
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
Si `productId` es "null" (string):
- El parámetro `:id` no se está pasando en la navegación
- Verificar `context.go('/products/${product.id}')` en el widget que navega
- Verificar que el `id` no sea null en el modelo

---

## Escenario 4: Debugging de UI y layouts

### Contexto
Un widget se renderiza con tamaños incorrectos. Necesitas ver las dimensiones exactas.

### Setup

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

### Ejercicio paso a paso

#### Paso 1: Usar Widget Inspector para entender el árbol
1. Poner breakpoint en `build`
2. `F5` hasta que pare
3. En Variables, expandir `this` → ver propiedades del widget
4. Abrir DevTools → Widget Inspector para ver el árbol completo

#### Paso 2: Debug Console para inspeccionar
```dart
// En Debug Console durante el breakpoint
product.name          // ver nombre
product.imageUrl      // ver URL
product.price         // ver precio
product.description.length  // ver longitud
```

#### Paso 3: Verificar constrains
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
1. Abrir DevTools (Ctrl+Shift+D → DevTools icon)
2. Seleccionar widget en el árbol
3. Ver propiedades de layout: width, height, constraints
4. Activar "Toggle Debug Paint" para ver borders

---

## Escenario 5: Debugging de Supabase Realtime

### Contexto
Las actualizaciones en tiempo real no llegan al widget.

### Setup

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
    
    // ← Breakpoint aquí para verificar suscripción
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

### Ejercicio paso a paso

#### Paso 1: Verificar conexión
Poner breakpoint en `.listen((data) {...})`:
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
.client
    .from('messages')
    .stream(primaryKey: ['id'])
    .order('created_at', ascending: false)
    .limit(50)
    .listen((data) {
  print('=== REALTIME UPDATE ===');
  print('Records: ${data.length}');
  print('First record: ${data.firstOrNull}');
  print('Channel status: ${_client.channel('messages').status}');
  _messagesController.add(data);
}, onError: (error) {
  print('=== REALTIME ERROR ===');
  print('Error: $error');
  print('Type: ${error.runtimeType}');
  _messagesController.addError(error);
});
```

#### Paso 4: Diagnóstico común
1. ¿RLS policies permiten SELECT? → `supabase.from('messages').select()`
2. ¿La tabla tiene replica identity? → `ALTER TABLE messages REPLICA IDENTITY FULL;`
3. ¿El channel se suscribió correctamente?
4. ¿Hay errores en Supabase Dashboard → Database → Replication?

---

## Ejercicio Integrador: Debug completo de feature de pagos

### Contexto
App Flutter con arquitectura limpia que integra pasarela de pagos. Los usuarios reportan que el pago "se queda cargando" sin completarse.

### Archivos del ejercicio

**`lib/features/payments/presentation/bloc/payment_bloc.dart`**
```dart
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';

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
    Emitter<PaymentState> emit
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
    Emitter<PaymentState> emit
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

### Ejercicio paso a paso

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

**Escenario A - Pago exitoso:**
1. Iniciar debugging
2. Llenar formulario de pago
3. Verificar: ¿Pasa por Breakpoint 1? ¿2? ¿Resultado?
4. Si falla en 2 → el use case lanza excepción

**Escenario B - Pago 3DS:**
1. Usar tarjeta que requiere 3DS
2. Verificar: ¿Se emite `Payment3DSRequired`?
3. Después de 3DS → verificar `VerifyPaymentStatus`

**Escenario C - Pago quedando en "cargando":**
1. Usar tarjeta que causa timeout
2. Verificar: ¿Llega a Breakpoint 3 o 4?
3. Si se queda en `PaymentProcessing()` → problema en use case

#### Paso 4: Diagnosticar causa raíz

**Causa más común: El verify loop**
```dart
// BUG: Si el verify retorna pending, se re-emite PaymentVerifying
// pero NO se re-intenta el verify → loop infinito de UI
if (status == PaymentStatus.pending) {
  emit(PaymentVerifying());
  // ← FALTA: await Future.delayed(Duration(seconds: 3));
  //          add(VerifyPaymentStatus(event.transactionId)); // Retry
}
```

**Fix:**
```dart
if (status == PaymentStatus.pending) {
  emit(PaymentVerifying());
  // Re-verificar después de 3 segundos
  await Future.delayed(Duration(seconds: 3));
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

## Checklist de debugging

Antes de depurar cualquier bug:
- [ ] ¿Puedo reproducir el bug consistentemente?
- [ ] ¿Entiendo el flujo de datos? (BLoC → UseCase → DataSource)
- [ ] ¿Los breakpoints están en los puntos correctos del flujo?
- [ ] ¿Tengo watches configurados para variables clave?
- [ ] ¿Verifiqué los logs en Debug Console?
- [ ] ¿Revisé el estado del BLoC/Cubit?
- [ ] ¿Verifiqué la respuesta de la API (Network en DevTools)?
- [ ] ¿Revisé RLS policies si uso Supabase?

---
→ Siguiente: `02-flutter-devtools/README.md`
