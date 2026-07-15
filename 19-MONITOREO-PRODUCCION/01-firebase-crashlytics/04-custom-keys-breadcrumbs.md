# 04 - Custom Keys y Breadcrumbs

## Custom Keys

Los custom keys son **pares de clave-valor** que se agregan a cada crash o error reportado. Ayudan a entender el contexto del error.

---

## Que son los custom keys?

```
Error: SocketException
├── device: Pixel 7
├── os: Android 13
├── app_version: 1.2.3
├── user_id: 12345
├── screen: checkout
├── payment_method: credit_card
└── last_action: submit_payment
```

---

## Como usar custom keys

### Configurar keys globales

```dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Firebase.initializeApp();

  // Custom keys globales (aplican a todos los errores)
  await FirebaseCrashlytics.instance.setCustomKey('app_version', '1.0.0');
  await FirebaseCrashlytics.instance.setCustomKey('environment', 'production');
  await FirebaseCrashlytics.instance.setCustomKey('flavor', 'free');
  
  runApp(MyApp());
}
```

### Actualizar keys dinamicamente

```dart
class AuthProvider extends ChangeNotifier {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  Future<void> login(String email, String password) async {
    try {
      final user = await _authService.login(email, password);
      
      // Actualizar keys cuando cambia el estado
      await _crashlytics.setCustomKey('user_id', user.id);
      await _crashlytics.setCustomKey('user_plan', user.plan);
      await _crashlytics.setCustomKey('is_authenticated', 'true');
      
      notifyListeners();
    } catch (e) {
      await _crashlytics.setCustomKey('last_login_error', e.toString());
      rethrow;
    }
  }

  Future<void> logout() async {
    await _authService.logout();
    
    await _crashlytics.setCustomKey('user_id', 'anonymous');
    await _crashlytics.setCustomKey('user_plan', 'none');
    await _crashlytics.setCustomKey('is_authenticated', 'false');
    
    notifyListeners();
  }
}
```

### Keys por pantalla

```dart
class CheckoutScreen extends StatefulWidget {
  @override
  _CheckoutScreenState createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  String _selectedPaymentMethod = 'credit_card';
  String _selectedShipping = 'standard';

  @override
  void initState() {
    super.initState();
    _setScreenKeys();
  }

  void _setScreenKeys() async {
    await FirebaseCrashlytics.instance.setCustomKey('screen', 'checkout');
    await FirebaseCrashlytics.instance.setCustomKey('payment_method', _selectedPaymentMethod);
    await FirebaseCrashlytics.instance.setCustomKey('shipping_method', _selectedShipping);
  }

  void _onPaymentMethodChanged(String method) {
    setState(() {
      _selectedPaymentMethod = method;
    });
    FirebaseCrashlytics.instance.setCustomKey('payment_method', method);
  }
}
```

---

## Limitaciones de custom keys

| Limite | Valor |
|---|---|
| Maximo de keys | 64 por crash |
| Maximo por key | 1024 caracteres |
| Maximo por value | 1024 caracteres |
| Tipos permitidos | String, int, double, bool |

---

## Custom Logs

Los custom logs son **mensajes de texto** que se agregan al crash report. Son utiles para rastrear la secuencia de eventos.

```dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

class OrderService {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  Future<Order> createOrder(OrderRequest request) async {
    // Log cada paso del proceso
    _crashlytics.log('Starting order creation');
    _crashlytics.log('Validating order items: ${request.items.length}');
    
    try {
      _crashlytics.log('Items validated successfully');
      _crashlytics.log('Calculating total: ${request.total}');
      
      final order = await _apiClient.post('/orders', body: request.toJson());
      
      _crashlytics.log('Order created: ${order.id}');
      _crashlytics.log('Processing payment: ${order.paymentId}');
      
      await _processPayment(order.paymentId);
      
      _crashlytics.log('Payment processed successfully');
      _crashlytics.log('Order completed: ${order.id}');
      
      return order;
    } catch (e) {
      _crashlytics.log('ERROR: Order creation failed');
      _crashlytics.log('Error details: $e');
      rethrow;
    }
  }
}
```

### Resultado en Firebase Console

```
Order creation failed
├── Logs:
│   ├── Starting order creation
│   ├── Validating order items: 3
│   ├── Items validated successfully
│   ├── Calculating total: 150.00
│   ├── ERROR: Order creation failed
│   └── Error details: SocketException
```

---

## User Identifier

El user identifier permite **agrupar errores por usuario**. Esto ayuda a entender si un error afecta a muchos usuarios o solo a uno.

```dart
class AuthService {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  Future<void> login(String email, String password) async {
    final user = await _authService.login(email, password);
    
    // Establecer user identifier
    await _crashlytics.setUserIdentifier(user.id);
    
    // Otras configuraciones
    await _crashlytics.setCustomKey('user_email', user.email);
    await _crashlytics.setCustomKey('user_plan', user.plan);
  }

  Future<void> logout() async {
    await _authService.logout();
    
    // Limpiar user identifier
    await _crashlytics.setUserIdentifier('anonymous');
    await _crashlytics.setCustomKey('user_email', 'none');
    await _crashlytics.setCustomKey('user_plan', 'none');
  }
}
```

---

## Breadcrumbs

Los breadcrumbs son **registros de eventos** que ayudan a reconstruir la secuencia de acciones del usuario antes del error.

### Breadcrumbs automaticos

Firebase Crashlytics registra automaticamente:
- Navegacion entre pantallas
- Lifecycle events (resume, pause)
- HTTP requests (si usas paquetes compatibles)

### Breadcrumbs manuales

```dart
class NavigationService {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  void navigateTo(String screen) {
    // Agregar breadcrumb manual
    _crashlytics.log('Navigated to: $screen');
    
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => screen),
    );
  }
}

class PaymentService {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  Future<void> processPayment(PaymentRequest request) async {
    _crashlytics.log('Processing payment: ${request.method}');
    _crashlytics.log('Amount: ${request.amount}');
    
    try {
      await _paymentGateway.charge(request);
      _crashlytics.log('Payment successful');
    } catch (e) {
      _crashlytics.log('Payment failed: ${e.toString()}');
      rethrow;
    }
  }
}
```

### Breadcrumbs con contexto

```dart
class ShoppingCart {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  void addItem(Product product) {
    _crashlytics.log('Added item: ${product.name} (${product.id})');
    _crashlytics.log('Cart total: ${_calculateTotal()}');
  }

  void removeItem(String productId) {
    _crashlytics.log('Removed item: $productId');
    _crashlytics.log('Cart total: ${_calculateTotal()}');
  }

  Future<void> checkout() async {
    _crashlytics.log('Starting checkout');
    _crashlytics.log('Items in cart: ${items.length}');
    _crashlytics.log('Total: ${_calculateTotal()}');
    
    try {
      await _createOrder();
      _crashlytics.log('Checkout completed');
    } catch (e) {
      _crashlytics.log('Checkout failed: ${e.toString()}');
      rethrow;
    }
  }
}
```

---

## Ejemplo completo: E-commerce

```dart
class EcommerceApp {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  Future<void> initialize() async {
    // Keys globales
    await _crashlytics.setCustomKey('app_version', '2.0.0');
    await _crashlytics.setCustomKey('environment', 'production');
    await _crashlytics.setCustomKey('store', 'main');
    
    // User identifier
    await _crashlytics.setUserIdentifier('anonymous');
  }

  Future<void> onUserLogin(User user) async {
    // Actualizar keys
    await _crashlytics.setUserIdentifier(user.id);
    await _crashlytics.setCustomKey('user_plan', user.plan);
    await _crashlytics.setCustomKey('user_country', user.country);
    
    // Log evento
    _crashlytics.log('User logged in: ${user.id}');
  }

  Future<void> onProductView(Product product) async {
    _crashlytics.log('Product viewed: ${product.id}');
    await _crashlytics.setCustomKey('last_product_viewed', product.id);
  }

  Future<void> onAddToCart(Product product) async {
    _crashlytics.log('Added to cart: ${product.id}');
    await _crashlytics.setCustomKey('cart_items', _cart.items.length);
  }

  Future<void> onCheckout() async {
    _crashlytics.log('Checkout started');
    await _crashlytics.setCustomKey('checkout_step', 'started');
  }

  Future<void> onPaymentSuccess(String orderId) async {
    _crashlytics.log('Payment successful: $orderId');
    await _crashlytics.setCustomKey('checkout_step', 'completed');
    await _crashlytics.setCustomKey('last_order_id', orderId);
  }

  Future<void> onError(String context, dynamic error) async {
    _crashlytics.log('ERROR in $context: ${error.toString()}');
    await _crashlytics.setCustomKey('error_context', context);
  }
}
```

---

## Resumen

| Feature | Uso | Ejemplo |
|---|---|---|
| Custom Keys | Contexto continuo | `user_id`, `screen`, `app_version` |
| Custom Logs | Secuencia de eventos | `Processing payment...` |
| User Identifier | Agrupar por usuario | `user.id` |
| Breadcrumbs | Reconstruir acciones | `Navigated to checkout` |

---

## Siguiente paso

[05 - Alertas y Notificaciones](./05-alertas-notificaciones.md) - Configurar alertas automatizadas
