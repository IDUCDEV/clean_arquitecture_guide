# 08 - Practicas Crashlytics

## Ejercicios Practicos

### Ejercicio 1: Login Fallido

**Objetivo**: Reportar errores de autenticacion sin crashear la app.

**Escenario**: Un usuario intenta hacer login pero la API falla.

**Codigo**:

```dart
// lib/features/auth/presentation/bloc/auth_bloc.dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUseCase loginUseCase;
  final FirebaseCrashlytics _crashlytics;

  AuthBloc({
    required this.loginUseCase,
    required FirebaseCrashlytics crashlytics,
  })  : _crashlytics = crashlytics,
        super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    try {
      emit(AuthLoading());
      
      // Agregar custom keys antes del intento
      await _crashlytics.setCustomKey('login_email', event.email);
      await _crashlytics.setCustomKey('login_attempt', DateTime.now().toIso8601String());
      
      _crashlytics.log('Attempting login for: ${event.email}');
      
      final user = await loginUseCase(
        email: event.email,
        password: event.password,
      );
      
      // Actualizar user ID despues del exito
      await _crashlytics.setUserIdentifier(user.id);
      await _crashlytics.setCustomKey('user_plan', user.plan);
      
      _crashlytics.log('Login successful for user: ${user.id}');
      
      emit(AuthAuthenticated(user));
    } on AuthException catch (e, stack) {
      // Error de autenticacion conocido
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Authentication failed',
        information: [
          'email: ${event.email}',
          'error_code: ${e.code}',
          'error_message: ${e.message}',
        ],
      );
      
      _crashlytics.log('Login failed: ${e.message}');
      
      emit(AuthError(e.message));
    } catch (e, stack) {
      // Error inesperado
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Unexpected login error',
        information: [
          'email: ${event.email}',
          'stack_trace: ${stack.toString()}',
        ],
      );
      
      emit(AuthError('Error inesperado. Intenta de nuevo.'));
    }
  }
}
```

**Verificacion**:
1. Ir a Firebase Console → Crashlytics
2. Verificar que el error aparece con contexto
3. Verificar custom keys (email, attempt)
4. Verificar user ID

---

### Ejercicio 2: API Timeout

**Objetivo**: Capturar errores de red con contexto completo.

**Escenario**: La API de productos tarda demasiado en responder.

**Codigo**:

```dart
// lib/features/products/data/repositories/product_repository_impl.dart
class ProductRepositoryImpl implements ProductRepository {
  final ProductRemoteDataSource remoteDataSource;
  final FirebaseCrashlytics _crashlytics;

  ProductRepositoryImpl({
    required this.remoteDataSource,
    required FirebaseCrashlytics crashlytics,
  }) : _crashlytics = crashlytics;

  @override
  Future<List<Product>> getProducts({int page = 1, int limit = 20}) async {
    final stopwatch = Stopwatch()..start();
    
    try {
      _crashlytics.log('Fetching products: page=$page, limit=$limit');
      
      final products = await remoteDataSource.getProducts(
        page: page,
        limit: limit,
      ).timeout(
        Duration(seconds: 10),
        onTimeout: () {
          throw TimeoutException('Products API timeout');
        },
      );
      
      stopwatch.stop();
      
      // Log exito con tiempo
      await _crashlytics.setCustomKey('api_response_time', stopwatch.elapsedMilliseconds);
      _crashlytics.log('Products fetched successfully in ${stopwatch.elapsedMilliseconds}ms');
      
      return products;
    } on TimeoutException catch (e, stack) {
      stopwatch.stop();
      
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Products API timeout',
        information: [
          'page: $page',
          'limit: $limit',
          'response_time: ${stopwatch.elapsedMilliseconds}ms',
          'timeout: 10s',
        ],
      );
      
      throw ServerException('Request timed out');
    } on SocketException catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Network error fetching products',
        information: [
          'page: $page',
          'limit: $limit',
          'error: ${e.toString()}',
        ],
      );
      
      throw ServerException('No internet connection');
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Unexpected error fetching products',
        information: [
          'page: $page',
          'limit: $limit',
        ],
      );
      
      rethrow;
    }
  }
}
```

**Verificacion**:
1. Simular timeout (usar proxy o limitar red)
2. Verificar que el error aparece con tiempo de respuesta
3. Verificar custom keys (page, limit, response_time)

---

### Ejercicio 3: BLoC Error State

**Objetivo**: Manejar errores en el state management.

**Escenario**: Un BLoC falla al cargar datos.

**Codigo**:

```dart
// lib/features/home/presentation/bloc/products_bloc.dart
class ProductsBloc extends Bloc<ProductsEvent, ProductsState> {
  final GetProductsUseCase getProductsUseCase;
  final FirebaseCrashlytics _crashlytics;

  ProductsBloc({
    required this.getProductsUseCase,
    required FirebaseCrashlytics crashlytics,
  })  : _crashlytics = crashlytics,
        super(ProductsInitial()) {
    on<LoadProducts>(_onLoadProducts);
    on<RefreshProducts>(_onRefreshProducts);
    on<LoadMoreProducts>(_onLoadMoreProducts);
  }

  Future<void> _onLoadProducts(
    LoadProducts event,
    Emitter<ProductsState> emit,
  ) async {
    try {
      emit(ProductsLoading());
      
      await _crashlytics.setCustomKey('products_action', 'load');
      _crashlytics.log('Loading products...');
      
      final products = await getProductsUseCase(
        page: 1,
        limit: 20,
      );
      
      await _crashlytics.setCustomKey('products_count', products.length);
      _crashlytics.log('Products loaded: ${products.length} items');
      
      emit(ProductsLoaded(
        products: products,
        hasReachedMax: products.length < 20,
      ));
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Failed to load products',
        information: ['action: load', 'page: 1'],
      );
      
      emit(ProductsError(
        message: 'Error al cargar productos',
        onRetry: () => add(LoadProducts()),
      ));
    }
  }

  Future<void> _onRefreshProducts(
    RefreshProducts event,
    Emitter<ProductsState> emit,
  ) async {
    try {
      await _crashlytics.setCustomKey('products_action', 'refresh');
      _crashlytics.log('Refreshing products...');
      
      final products = await getProductsUseCase(
        page: 1,
        limit: 20,
      );
      
      _crashlytics.log('Products refreshed: ${products.length} items');
      
      emit(ProductsLoaded(
        products: products,
        hasReachedMax: products.length < 20,
      ));
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Failed to refresh products',
        information: ['action: refresh'],
      );
      
      // No cambiar el estado actual, solo loguear
      _crashlytics.log('Refresh failed, keeping current state');
    }
  }

  Future<void> _onLoadMoreProducts(
    LoadMoreProducts event,
    Emitter<ProductsState> emit,
  ) async {
    final currentState = state;
    if (currentState is! ProductsLoaded || currentState.hasReachedMax) {
      return;
    }

    try {
      await _crashlytics.setCustomKey('products_action', 'load_more');
      _crashlytics.log('Loading more products...');
      
      final products = await getProductsUseCase(
        page: currentState.products.length ~/ 20 + 1,
        limit: 20,
      );
      
      emit(ProductsLoaded(
        products: [...currentState.products, ...products],
        hasReachedMax: products.length < 20,
      ));
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Failed to load more products',
        information: ['action: load_more', 'current_count: ${currentState.products.length}'],
      );
      
      emit(ProductsError(
        message: 'Error al cargar mas productos',
        onRetry: () => add(LoadMoreProducts()),
      ));
    }
  }
}
```

**Verificacion**:
1. Forzar error en la API
2. Verificar que el BLoC emite ProductsError
3. Verificar que el error aparece en Crashlytics con contexto

---

### Ejercicio 4: Formulario de Validacion

**Objetivo**: Reportar errores de validacion con contexto.

**Escenario**: Un formulario de registro falla la validacion.

**Codigo**:

```dart
// lib/features/auth/presentation/bloc/register_bloc.dart
class RegisterBloc extends Bloc<RegisterEvent, RegisterState> {
  final RegisterUseCase registerUseCase;
  final FirebaseCrashlytics _crashlytics;

  RegisterBloc({
    required this.registerUseCase,
    required FirebaseCrashlytics crashlytics,
  })  : _crashlytics = crashlytics,
        super(RegisterInitial()) {
    on<RegisterSubmitted>(_onRegisterSubmitted);
    on<FieldChanged>(_onFieldChanged);
  }

  void _onFieldChanged(FieldChanged event, Emitter<RegisterState> emit) {
    // No reportar errores de validacion, son esperados
    final currentState = state;
    if (currentState is RegisterValidationError) {
      emit(RegisterInitial());
    }
  }

  Future<void> _onRegisterSubmitted(
    RegisterSubmitted event,
    Emitter<RegisterState> emit,
  ) async {
    try {
      emit(RegisterLoading());
      
      // Validar campos
      final errors = _validateFields(event);
      if (errors.isNotEmpty) {
        await _crashlytics.setCustomKey('validation_errors', errors.join(', '));
        _crashlytics.log('Validation failed: ${errors.join(', ')}');
        
        emit(RegisterValidationError(errors));
        return;
      }
      
      await _crashlytics.setCustomKey('register_email', event.email);
      _crashlytics.log('Attempting registration for: ${event.email}');
      
      final user = await registerUseCase(
        email: event.email,
        password: event.password,
        name: event.name,
      );
      
      await _crashlytics.setUserIdentifier(user.id);
      _crashlytics.log('Registration successful');
      
      emit(RegisterSuccess(user));
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Registration failed',
        information: [
          'email: ${event.email}',
          'name: ${event.name}',
          'error: ${e.toString()}',
        ],
      );
      
      emit(RegisterError('Error al registrar usuario'));
    }
  }

  List<String> _validateFields(RegisterSubmitted event) {
    final errors = <String>[];
    
    if (event.email.isEmpty || !event.email.contains('@')) {
      errors.add('email_invalid');
    }
    
    if (event.password.length < 8) {
      errors.add('password_too_short');
    }
    
    if (event.name.isEmpty) {
      errors.add('name_empty');
    }
    
    return errors;
  }
}
```

---

### Ejercicio 5: Pago Fallido

**Objetivo**: Manejar errores criticos con contexto completo.

**Escenario**: Un pago falla durante el checkout.

**Codigo**:

```dart
// lib/features/checkout/presentation/bloc/payment_bloc.dart
class PaymentBloc extends Bloc<PaymentEvent, PaymentState> {
  final ProcessPaymentUseCase processPaymentUseCase;
  final FirebaseCrashlytics _crashlytics;

  PaymentBloc({
    required this.processPaymentUseCase,
    required FirebaseCrashlytics crashlytics,
  })  : _crashlytics = crashlytics,
        super(PaymentInitial()) {
    on<ProcessPayment>(_onProcessPayment);
    on<RetryPayment>(_onRetryPayment);
  }

  Future<void> _onProcessPayment(
    ProcessPayment event,
    Emitter<PaymentState> emit,
  ) async {
    try {
      emit(PaymentProcessing());
      
      // Contexto completo del pago
      await _crashlytics.setCustomKey('payment_amount', event.amount);
      await _crashlytics.setCustomKey('payment_method', event.method);
      await _crashlytics.setCustomKey('payment_currency', event.currency);
      await _crashlytics.setCustomKey('order_id', event.orderId);
      
      _crashlytics.log('Processing payment: ${event.orderId}');
      _crashlytics.log('Amount: ${event.amount} ${event.currency}');
      _crashlytics.log('Method: ${event.method}');
      
      final result = await processPaymentUseCase(
        orderId: event.orderId,
        amount: event.amount,
        method: event.method,
        currency: event.currency,
      ).timeout(
        Duration(seconds: 30),
        onTimeout: () {
          throw TimeoutException('Payment processing timeout');
        },
      );
      
      await _crashlytics.setCustomKey('payment_status', 'success');
      await _crashlytics.setCustomKey('payment_id', result.paymentId);
      
      _crashlytics.log('Payment successful: ${result.paymentId}');
      
      emit(PaymentSuccess(result));
    } on PaymentException catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Payment failed',
        information: [
          'order_id: ${event.orderId}',
          'amount: ${event.amount}',
          'method: ${event.method}',
          'error_code: ${e.code}',
          'error_message: ${e.message}',
        ],
      );
      
      await _crashlytics.setCustomKey('payment_status', 'failed');
      _crashlytics.log('Payment failed: ${e.message}');
      
      emit(PaymentError(
        message: e.message,
        orderId: event.orderId,
        canRetry: e.isRetryable,
      ));
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Unexpected payment error',
        information: [
          'order_id: ${event.orderId}',
          'amount: ${event.amount}',
          'method: ${event.method}',
        ],
      );
      
      emit(PaymentError(
        message: 'Error inesperado en el pago',
        orderId: event.orderId,
        canRetry: false,
      ));
    }
  }

  Future<void> _onRetryPayment(
    RetryPayment event,
    Emitter<PaymentState> emit,
  ) async {
    add(ProcessPayment(
      orderId: event.orderId,
      amount: event.amount,
      method: event.method,
      currency: event.currency,
    ));
  }
}
```

---

### Ejercicio 6: Offline Mode

**Objetivo**: Manejar errores cuando no hay conexion.

**Escenario**: La app intenta sincronizar datos sin conexion.

**Codigo**:

```dart
// lib/core/network/network_info.dart
class NetworkInfo {
  final FirebaseCrashlytics _crashlytics;
  final Connectivity _connectivity;

  NetworkInfo({
    required FirebaseCrashlytics crashlytics,
    required Connectivity connectivity,
  })  : _crashlytics = crashlytics,
        _connectivity = connectivity;

  Future<bool> get isConnected async {
    try {
      final result = await _connectivity.checkConnectivity();
      final isConnected = result != ConnectivityResult.none;
      
      await _crashlytics.setCustomKey('network_status', 
        isConnected ? 'online' : 'offline');
      
      return isConnected;
    } catch (e) {
      await _crashlytics.setCustomKey('network_status', 'unknown');
      return false;
    }
  }

  Stream<bool> get onConnectivityChanged {
    return _connectivity.onConnectivityChanged.map((result) {
      final isConnected = result != ConnectivityResult.none;
      
      _crashlytics.log('Network status changed: ${isConnected ? "online" : "offline"}');
      
      return isConnected;
    });
  }
}

// lib/features/sync/presentation/bloc/sync_bloc.dart
class SyncBloc extends Bloc<SyncEvent, SyncState> {
  final SyncDataUseCase syncDataUseCase;
  final NetworkInfo networkInfo;
  final FirebaseCrashlytics _crashlytics;

  SyncBloc({
    required this.syncDataUseCase,
    required this.networkInfo,
    required FirebaseCrashlytics crashlytics,
  })  : _crashlytics = crashlytics,
        super(SyncInitial()) {
    on<StartSync>(_onStartSync);
    on<SyncCompleted>(_onSyncCompleted);
  }

  Future<void> _onStartSync(
    StartSync event,
    Emitter<SyncState> emit,
  ) async {
    try {
      emit(SyncLoading());
      
      await _crashlytics.setCustomKey('sync_started', DateTime.now().toIso8601String());
      _crashlytics.log('Starting sync...');
      
      if (!await networkInfo.isConnected) {
        await _crashlytics.setCustomKey('sync_status', 'offline');
        _crashlytics.log('No internet connection, queuing sync');
        
        emit(SyncOffline(
          message: 'Sin conexion. Los datos se sincronizaran cuando haya internet.',
        ));
        return;
      }
      
      final result = await syncDataUseCase();
      
      await _crashlytics.setCustomKey('sync_status', 'success');
      await _crashlytics.setCustomKey('sync_items_synced', result.itemsSynced);
      
      _crashlytics.log('Sync completed: ${result.itemsSynced} items');
      
      emit(SyncSuccess(result));
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Sync failed',
        information: [
          'is_connected: ${await networkInfo.isConnected}',
        ],
      );
      
      await _crashlytics.setCustomKey('sync_status', 'failed');
      
      emit(SyncError(
        message: 'Error al sincronizar datos',
        canRetry: true,
      ));
    }
  }

  void _onSyncCompleted(SyncCompleted event, Emitter<SyncState> emit) {
    _crashlytics.log('Sync completed via connectivity change');
    add(StartSync());
  }
}
```

---

## Ejercicio Integrador: App de E-commerce

**Objetivo**: Crear un sistema completo de monitoreo para una app de e-commerce.

### Componentes a implementar

1. **Auth monitoring**
2. **Product catalog monitoring**
3. **Cart monitoring**
4. **Checkout monitoring**
5. **Payment monitoring**

### Codigo base

```dart
// lib/core/monitoring/crashlytics_service.dart
class CrashlyticsService {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  // Auth monitoring
  Future<void> logLoginAttempt(String email) async {
    await _crashlytics.setCustomKey('auth_email', email);
    _crashlytics.log('Login attempt: $email');
  }

  Future<void> logLoginSuccess(String userId, String plan) async {
    await _crashlytics.setUserIdentifier(userId);
    await _crashlytics.setCustomKey('user_plan', plan);
    _crashlytics.log('Login success: $userId');
  }

  Future<void> logLoginError(String email, String error) async {
    await _crashlytics.setCustomKey('auth_error', error);
    _crashlytics.log('Login error: $error');
  }

  // Product monitoring
  Future<void> logProductView(String productId, String category) async {
    await _crashlytics.setCustomKey('last_product_viewed', productId);
    await _crashlytics.setCustomKey('last_category', category);
    _crashlytics.log('Product viewed: $productId');
  }

  Future<void> logAddToCart(String productId, int quantity) async {
    await _crashlytics.setCustomKey('cart_action', 'add');
    _crashlytics.log('Added to cart: $productId x$quantity');
  }

  // Checkout monitoring
  Future<void> logCheckoutStart(String orderId, double total) async {
    await _crashlytics.setCustomKey('checkout_order_id', orderId);
    await _crashlytics.setCustomKey('checkout_total', total);
    _crashlytics.log('Checkout started: $orderId');
  }

  Future<void> logPaymentMethod(String method) async {
    await _crashlytics.setCustomKey('payment_method', method);
    _crashlytics.log('Payment method: $method');
  }

  Future<void> logCheckoutComplete(String orderId, String paymentId) async {
    await _crashlytics.setCustomKey('checkout_status', 'completed');
    _crashlytics.log('Checkout completed: $orderId, payment: $paymentId');
  }

  Future<void> logCheckoutError(String orderId, String error) async {
    await _crashlytics.setCustomKey('checkout_status', 'failed');
    _crashlytics.log('Checkout error: $error');
  }

  // Error reporting
  Future<void> reportError(
    dynamic error,
    StackTrace stack, {
    required String context,
    Map<String, dynamic>? additionalInfo,
  }) async {
    await _crashlytics.recordError(
      error,
      stack,
      reason: context,
      information: additionalInfo?.entries
          .map((e) => '${e.key}: ${e.value}')
          .toList(),
    );
  }
}
```

### Verificacion final

1. Ejecutar la app en release
2. Realizar un flujo completo (login → products → cart → checkout)
3. Forzar errores en cada paso
4. Verificar en Firebase Console que todos los errores aparecen con contexto
5. Verificar custom keys en cada error
6. Verificar user ID en los errores

---

## Siguiente paso

[Comparacion Crashlytics vs Sentry](../03-comparacion-migracion/01-crashlytics-vs-sentry.md)
