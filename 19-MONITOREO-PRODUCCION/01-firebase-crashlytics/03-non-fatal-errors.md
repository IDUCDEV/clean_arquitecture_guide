# 03 - Non-Fatal Errors

## Que son los errores no fatales?

Los errores no fatales **no cierran la app**, pero afectan la funcionalidad. El usuario puede seguir navegando, pero algo no funciono correctamente.

```
App ejecutando normalmente
  └── Usuario toca "Cargar productos"
    └── API falla (timeout)
      └── Error no fatal reportado
        └── UI muestra "Error al cargar"
          └── Usuario puede seguir usando la app
```

---

## Cuando usar non-fatal vs fatal

| Escenario | Tipo | Ejemplo |
|---|---|---|
| API timeout | Non-fatal | `SocketException` |
| Form validation fail | Non-fatal | `FormatException` |
| Image load fail | Non-fatal | `NetworkImage` error |
| Parse error | Non-fatal | `FormatException` |
| Auth error | Non-fatal | `AuthException` |
| Null reference | Fatal | `LateInitializationError` |
| Index out of bounds | Fatal | `RangeError` |

---

## Basico: recordError

```dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

try {
  final response = await http.get(Uri.parse('https://api.example.com/data'));
  if (response.statusCode != 200) {
    throw Exception('Failed to load data: ${response.statusCode}');
  }
} catch (e, stack) {
  // Reportar error no fatal
  await FirebaseCrashlytics.instance.recordError(
    e,
    stack,
    reason: 'API request failed',
  );
  
  // Mostrar UI de error
  showErrorUI('No se pudieron cargar los datos');
}
```

---

## Con contexto adicional

```dart
try {
  final user = await authService.login(email, password);
  return user;
} catch (e, stack) {
  await FirebaseCrashlytics.instance.recordError(
    e,
    stack,
    reason: 'Login failed',
    information: [
      'email: $email',
      'timestamp: ${DateTime.now().toIso8601String()}',
      'attempt: $loginAttempts',
    ],
  );
  
  // Re-throw si necesitas manejar arriba
  throw AuthException('Login failed');
}
```

---

## Patrones por tipo de error

### 1. Errores de Red

```dart
class ApiClient {
  final http.Client _client;
  final FirebaseCrashlytics _crashlytics;

  Future<Map<String, dynamic>> get(String endpoint) async {
    try {
      final response = await _client.get(
        Uri.parse('https://api.example.com$endpoint'),
      ).timeout(Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      }
      
      throw HttpException(
        'Request failed with status ${response.statusCode}',
      );
    } on TimeoutException catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'API timeout',
        information: ['endpoint: $endpoint', 'timeout: 10s'],
      );
      throw ApiException('Request timed out');
    } on SocketException catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Network error',
        information: ['endpoint: $endpoint'],
      );
      throw ApiException('No internet connection');
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Unexpected API error',
        information: ['endpoint: $endpoint'],
      );
      rethrow;
    }
  }
}
```

### 2. Errores de Parsing

```dart
class UserRepository {
  final FirebaseCrashlytics _crashlytics;

  Future<User> getUser(String id) async {
    try {
      final response = await _apiClient.get('/users/$id');
      return UserMapper.fromMap(response);
    } on FormatException catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Failed to parse user data',
        information: ['user_id: $id', 'raw_data: $response'],
      );
      throw ParsingException('Invalid user data format');
    }
  }
}

class UserMapper {
  static User fromMap(Map<String, dynamic> map) {
    try {
      return User(
        id: map['id'] as String,
        name: map['name'] as String,
        email: map['email'] as String,
      );
    } catch (e) {
      throw FormatException('Invalid user map: $map');
    }
  }
}
```

### 3. Errores de Autenticacion

```dart
class AuthService {
  final FirebaseCrashlytics _crashlytics;

  Future<User> login(String email, String password) async {
    try {
      final response = await _supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );
      
      if (response.user == null) {
        throw AuthException('User not found');
      }
      
      return UserMapper.fromSupabaseUser(response.user!);
    } on AuthException catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Authentication failed',
        information: [
          'email: $email',
          'error_code: ${e.message}',
        ],
      );
      throw AuthException(e.message);
    }
  }
}
```

### 4. Errores de UI

```dart
class ProductPage extends StatefulWidget {
  @override
  _ProductPageState createState() => _ProductPageState();
}

class _ProductPageState extends State<ProductPage> {
  late Future<List<Product>> _productsFuture;

  @override
  void initState() {
    super.initState();
    _productsFuture = _loadProducts();
  }

  Future<List<Product>> _loadProducts() async {
    try {
      return await ProductRepository.getProducts();
    } catch (e, stack) {
      await FirebaseCrashlytics.instance.recordError(
        e,
        stack,
        reason: 'Failed to load products',
        information: ['page: ProductPage'],
      );
      rethrow;
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Product>>(
      future: _productsFuture,
      builder: (context, snapshot) {
        if (snapshot.hasError) {
          return ProductErrorWidget(
            onRetry: () {
              setState(() {
                _productsFuture = _loadProducts();
              });
            },
          );
        }
        
        if (snapshot.hasData) {
          return ProductList(products: snapshot.data!);
        }
        
        return ProductLoadingWidget();
      },
    );
  }
}
```

---

## Errores en BLoC/Cubit

```dart
class ProductCubit extends Cubit<ProductState> {
  final GetProductsUseCase getProductsUseCase;
  final FirebaseCrashlytics _crashlytics;

  ProductCubit({
    required this.getProductsUseCase,
    required FirebaseCrashlytics crashlytics,
  })  : _crashlytics = crashlytics,
        super(ProductInitial());

  Future<void> loadProducts() async {
    try {
      emit(ProductLoading());
      
      final products = await getProductsUseCase();
      emit(ProductLoaded(products));
    } on ServerException catch (e) {
      emit(ProductError(e.message));
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Unexpected error in ProductCubit',
        information: ['state: ${state.runtimeType}'],
      );
      emit(ProductError('Error inesperado'));
    }
  }

  Future<void> deleteProduct(String id) async {
    try {
      emit(ProductDeleting());
      
      await deleteProductUseCase(id);
      emit(ProductDeleted());
      
      // Recargar lista
      await loadProducts();
    } catch (e, stack) {
      await _crashlytics.recordError(
        e,
        stack,
        reason: 'Failed to delete product',
        information: ['product_id: $id'],
      );
      emit(ProductError('Error al eliminar producto'));
    }
  }
}
```

---

## Errores con try-catch en UI

### Patron 1: Error con retry

```dart
class DataWidget extends StatefulWidget {
  @override
  _DataWidgetState createState() => _DataWidgetState();
}

class _DataWidgetState extends State<DataWidget> {
  late Future<Data> _dataFuture;

  @override
  void initState() {
    super.initState();
    _dataFuture = _fetchData();
  }

  Future<Data> _fetchData() async {
    try {
      return await DataRepository.getData();
    } catch (e, stack) {
      await FirebaseCrashlytics.instance.recordError(
        e,
        stack,
        reason: 'Data fetch failed',
      );
      rethrow;
    }
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Data>(
      future: _dataFuture,
      builder: (context, snapshot) {
        if (snapshot.hasError) {
          return ErrorWidget(
            message: 'Error al cargar datos',
            onRetry: () {
              setState(() {
                _dataFuture = _fetchData();
              });
            },
          );
        }
        
        if (snapshot.connectionState == ConnectionState.done) {
          return DataDisplay(data: snapshot.data!);
        }
        
        return LoadingWidget();
      },
    );
  }
}
```

### Patron 2: Error con fallback

```dart
class ImageLoader extends StatelessWidget {
  final String url;
  final String fallbackUrl;

  const ImageLoader({
    required this.url,
    required this.fallbackUrl,
  });

  @override
  Widget build(BuildContext context) {
    return Image.network(
      url,
      errorBuilder: (context, error, stackTrace) {
        // Reportar error no fatal
        FirebaseCrashlytics.instance.recordError(
          error,
          stackTrace,
          reason: 'Image load failed',
          information: ['url: $url', 'fallback: $fallbackUrl'],
        );
        
        // Mostrar imagen de fallback
        return Image.network(fallbackUrl);
      },
    );
  }
}
```

---

## Metricas importantes

### Crash Rate

```
Crash rate = (Crashes / Sessions) * 100
```

### Non-Fatal Rate

```
Non-fatal rate = (Non-fatal errors / Sessions) * 100
```

### User Impact

```
User impact = (Affected users / Total users) * 100
```

---

## Resumen

| Tipo | Metodo | Cuando usar |
|---|---|---|
| Fatal | `FlutterError.onError` | Errores del framework |
| No fatal | `recordError` | Errores de negocio |
| Async | `runZonedGuarded` | Errores en Futures |
| UI | `errorBuilder` | Errores de rendering |

---

## Siguiente paso

[04 - Custom Keys y Breadcrumbs](./04-custom-keys-breadcrumbs.md) - Agregar contexto a tus errores
