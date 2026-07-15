# 04 - Performance Tracing

## Que es Performance Tracing?

Performance tracking permite medir el **tiempo de ejecucion** de operaciones criticas. Ayuda a identificar cuellos de botella y optimizar la performance de tu app.

---

## Conceptos basicos

### Transaction

Una operacion de alto nivel (ej: "checkout", "load products").

```dart
final transaction = await Sentry.startTransaction(
  'checkout',  // Nombre
  'task',      // Tipo
);
```

### Span

Un paso dentro de una transaccion (ej: "process payment", "validate cart").

```dart
final span = transaction.startChild(
  'http.client',
  description: 'POST /api/payments',
);
```

---

## Basico: Transaction

```dart
import 'package:sentry_flutter/sentry_flutter.dart';

Future<Order> checkout(Cart cart) async {
  final transaction = await Sentry.startTransaction(
    'checkout',
    'task',
    bindToScope: true,
  );

  try {
    // Paso 1: Validar carrito
    final validationSpan = transaction.startChild(
      'validation',
      description: 'Validate cart',
    );
    
    await validateCart(cart);
    validationSpan.status = SpanStatus.ok();
    await validationSpan.finish();

    // Paso 2: Procesar pago
    final paymentSpan = transaction.startChild(
      'payment',
      description: 'Process payment',
    );
    
    final paymentResult = await processPayment(cart.total);
    paymentSpan.status = SpanStatus.ok();
    await paymentSpan.finish();

    // Paso 3: Crear orden
    final orderSpan = transaction.startChild(
      'order',
      description: 'Create order',
    );
    
    final order = await createOrder(cart, paymentResult);
    orderSpan.status = SpanStatus.ok();
    await orderSpan.finish();

    transaction.status = SpanStatus.ok();
    return order;
  } catch (e) {
    transaction.status = SpanStatus.internalError();
    rethrow;
  } finally {
    await transaction.finish();
  }
}
```

---

## Avanzado: Spans anidados

```dart
Future<void> loadProducts() async {
  final transaction = await Sentry.startTransaction(
    'load_products',
    'task',
    bindToScope: true,
  );

  try {
    // Span: Check cache
    final cacheSpan = transaction.startChild(
      'cache.check',
      description: 'Check local cache',
    );
    
    final cachedProducts = await cache.get('products');
    cacheSpan.setData('cache_hit', cachedProducts != null);
    await cacheSpan.finish();

    if (cachedProducts != null) {
      transaction.setData('source', 'cache');
      transaction.status = SpanStatus.ok();
      return;
    }

    // Span: Fetch from API
    final apiSpan = transaction.startChild(
      'http.client',
      description: 'GET /api/products',
    );
    
    final response = await http.get(
      Uri.parse('https://api.example.com/products'),
    );
    apiSpan.setData('status_code', response.statusCode);
    await apiSpan.finish();

    // Span: Parse response
    final parseSpan = transaction.startChild(
      'parse',
      description: 'Parse JSON response',
    );
    
    final products = jsonDecode(response.body);
    parseSpan.setData('products_count', products.length);
    await parseSpan.finish();

    // Span: Save to cache
    final saveCacheSpan = transaction.startChild(
      'cache.save',
      description: 'Save to local cache',
    );
    
    await cache.set('products', products);
    await saveCacheSpan.finish();

    transaction.setData('source', 'api');
    transaction.status = SpanStatus.ok();
  } catch (e) {
    transaction.status = SpanStatus.internalError();
    rethrow;
  } finally {
    await transaction.finish();
  }
}
```

---

## Integracion con BLoC

```dart
// lib/features/products/presentation/bloc/products_bloc.dart
class ProductsBloc extends Bloc<ProductsEvent, ProductsState> {
  final GetProductsUseCase getProductsUseCase;
  
  ProductsBloc({required this.getProductsUseCase}) : super(ProductsInitial()) {
    on<LoadProducts>(_onLoadProducts);
  }

  Future<void> _onLoadProducts(
    LoadProducts event,
    Emitter<ProductsState> emit,
  ) async {
    final transaction = await Sentry.startTransaction(
      'load_products',
      'bloc',
      bindToScope: true,
    );

    try {
      emit(ProductsLoading());
      
      final products = await getProductsUseCase();
      
      transaction.setData('products_count', products.length);
      transaction.status = SpanStatus.ok();
      
      emit(ProductsLoaded(products));
    } catch (e) {
      transaction.status = SpanStatus.internalError();
      emit(ProductsError('Failed to load products'));
    } finally {
      await transaction.finish();
    }
  }
}
```

---

## Integracion con UseCase

```dart
// lib/features/products/domain/usecases/get_products_use_case.dart
class GetProductsUseCase {
  final ProductRepository repository;

  GetProductsUseCase(this.repository);

  Future<List<Product>> call({int page = 1, int limit = 20}) async {
    final span = Sentry.currentHub.startTransaction(
      'get_products',
      'usecase',
      bindToScope: true,
    );

    try {
      span.setData('page', page);
      span.setData('limit', limit);
      
      final products = await repository.getProducts(page: page, limit: limit);
      
      span.setData('result_count', products.length);
      span.status = SpanStatus.ok();
      
      return products;
    } catch (e) {
      span.status = SpanStatus.internalError();
      rethrow;
    } finally {
      await span.finish();
    }
  }
}
```

---

## Integracion con HTTP Client

### Con Dio

```dart
// lib/core/network/dio_client.dart
import 'package:dio/dio.dart';
import 'package:sentry_dio/sentry_dio.dart';

class DioClient {
  late final Dio _dio;

  DioClient() {
    _dio = Dio();
    
    // Agregar interceptor de Sentry
    _dio.addSentryInterceptor(
      maxRequestBodySize: MaxRequestBodySize.always,
      maxResponseBodySize: MaxResponseBodySize.always,
    );
  }
}
```

### Con http

```dart
// lib/core/network/http_client.dart
import 'package:http/http.dart' as http;
import 'package:sentry_flutter/sentry_flutter.dart';

class HttpClient {
  final http.Client _client = http.Client();

  Future<http.Response> get(Uri url) async {
    final transaction = Sentry.currentHub.startTransaction(
      'HTTP GET ${url.path}',
      'http.client',
      bindToScope: true,
    );

    try {
      final response = await _client.get(url);
      
      transaction.setData('status_code', response.statusCode);
      transaction.setData('url', url.toString());
      
      if (response.statusCode >= 400) {
        transaction.status = SpanStatus.internalError();
      } else {
        transaction.status = SpanStatus.ok();
      }
      
      return response;
    } catch (e) {
      transaction.status = SpanStatus.internalError();
      rethrow;
    } finally {
      await transaction.finish();
    }
  }
}
```

---

## Integracion con Supabase

```dart
// lib/features/products/data/repositories/product_repository_impl.dart
class ProductRepositoryImpl implements ProductRepository {
  final SupabaseClient _supabase;

  ProductRepositoryImpl(this._supabase);

  @override
  Future<List<Product>> getProducts({int page = 1, int limit = 20}) async {
    final transaction = Sentry.currentHub.startTransaction(
      'get_products',
      'repository',
      bindToScope: true,
    );

    try {
      final span = transaction.startChild(
        'supabase.query',
        description: 'Query products from Supabase',
      );
      
      final response = await _supabase
          .from('products')
          .select()
          .range(page * limit, (page + 1) * limit - 1);
      
      span.setData('query', 'products');
      span.setData('result_count', response.length);
      span.status = SpanStatus.ok();
      await span.finish();

      transaction.status = SpanStatus.ok();
      
      return response.map((json) => ProductMapper.fromMap(json)).toList();
    } catch (e) {
      transaction.status = SpanStatus.internalError();
      rethrow;
    } finally {
      await transaction.finish();
    }
  }
}
```

---

## Cold Start Detection

```dart
// lib/main.dart
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  final appStart = DateTime.now();
  
  WidgetsFlutterBinding.ensureInitialized();

  await SentryFlutter.init(
    (options) {
      options.dsn = 'your-dsn';
      options.tracesSampleRate = 1.0;
      
      // Agregar cold start
      options.onAppStart = (appStart);
    },
    appRunner: () => runApp(MyApp()),
  );
}
```

---

## Custom Transactions

```dart
// Transaccion personalizada
final transaction = await Sentry.startTransaction(
  'image_processing',
  'task',
  bindToScope: true,
);

try {
  // Procesar imagen
  final span = transaction.startChild(
    'image.resize',
    description: 'Resize image to 800x600',
  );
  
  await resizeImage(image, 800, 600);
  span.status = SpanStatus.ok();
  await span.finish();

  // Comprimir imagen
  final compressSpan = transaction.startChild(
    'image.compress',
    description: 'Compress image to 80% quality',
  );
  
  await compressImage(image, quality: 0.8);
  compressSpan.status = SpanStatus.ok();
  await compressSpan.finish();

  transaction.status = SpanStatus.ok();
} catch (e) {
  transaction.status = SpanStatus.internalError();
  rethrow;
} finally {
  await transaction.finish();
}
```

---

## Resumen

| Concepto | Descripcion | Ejemplo |
|---|---|---|
| Transaction | Operacion principal | `checkout`, `load_products` |
| Span | Paso dentro de transaction | `validate_cart`, `process_payment` |
| Status | Resultado del span | `ok`, `internal_error` |
| Data | Contexto adicional | `products_count`, `status_code` |

---

## Siguiente paso

[05 - Session Replay](./05-session-replay.md) - Ver que vio el usuario antes del error
