# 🚀 Nivel Experto: Retrofit - Clientes HTTP Generados

> Retrofit genera automáticamente clientes HTTP a partir de anotaciones. Es el estándar para consumir APIs REST en Flutter profesional.

---

## 1. ¿Por qué Retrofit?

### 1.1 Sin Retrofit (Manual)

```dart
class UserApiClient {
  final http.Client client;
  final String baseUrl;

  UserApiClient({required this.client, required this.baseUrl});

  Future<UserDto> getUser(String id) async {
    final response = await client.get(
      Uri.parse('$baseUrl/users/$id'),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return UserDto.fromJson(jsonDecode(response.body));
    } else if (response.statusCode == 404) {
      throw NotFoundException('User not found');
    } else {
      throw ApiException('Error: ${response.statusCode}');
    }
  }

  // 10+ métodos más... todo boilerplate repetitivo
}
```

**Problemas:**
- Cada endpoint = repetir URI, headers, parsing
- Errores tipográficos en URIs (solo se detectan en runtime)
- El manejo de errores se vuelve inconsistente
- Mucho código duplicado

### 1.2 Con Retrofit

```dart
@RestApi(baseUrl: 'https://api.example.com')
abstract class UserApiClient {
  factory UserApiClient(Dio dio, {String baseUrl}) = _UserApiClient;

  @GET('/users/{id}')
  Future<UserDto> getUser(@Path('id') String id);

  @GET('/users')
  Future<List<UserDto>> getUsers();

  @POST('/users')
  Future<UserDto> createUser(@Body() CreateUserDto dto);
}
```

**Genera automáticamente:** el `_UserApiClient` con toda la implementación.

---

## 2. Configuración

### 2.1 Dependencias

```yaml
# pubspec.yaml
dependencies:
  dio: ^5.4.0
  retrofit: ^4.1.0
  json_annotation: ^4.9.0

dev_dependencies:
  build_runner: ^2.4.8
  retrofit_generator: ^8.1.0
  json_serializable: ^6.8.0
```

### 2.2 build.yaml

```yaml
# build.yaml
targets:
  $default:
    builders:
      retrofit_generator:
        options:
          nullable: true
          named_parameters: false
```

### 2.3 Cliente Básico

```dart
import 'package:dio/dio.dart';
import 'package:retrofit/retrofit.dart';
import 'package:json_annotation/json_annotation.dart';

part 'api_client.g.dart';

@RestApi(baseUrl: 'https://api.example.com/v1')
abstract class ApiClient {
  factory ApiClient(Dio dio, {String baseUrl}) = _ApiClient;
}
```

```dart
// main.dart
final dio = Dio(BaseOptions(
  connectTimeout: const Duration(seconds: 10),
  receiveTimeout: const Duration(seconds: 10),
));

final api = ApiClient(dio);
```

---

## 3. Anotaciones

### 3.1 Métodos HTTP

| Anotación | HTTP | Ejemplo |
|-----------|------|---------|
| `@GET('path')` | GET | `@GET('/users')` |
| `@POST('path')` | POST | `@POST('/users')` |
| `@PUT('path')` | PUT | `@PUT('/users/{id}')` |
| `@PATCH('path')` | PATCH | `@PATCH('/users/{id}')` |
| `@DELETE('path')` | DELETE | `@DELETE('/users/{id}')` |
| `@HEAD('path')` | HEAD | `@HEAD('/health')` |
| `@HTTP(method: 'OPTIONS', path: '/users')` | Custom | Para métodos no estándar |

### 3.2 Parámetros

| Anotación | Uso | Descripción |
|-----------|-----|-------------|
| `@Path('id')` | `@GET('/users/{id}')` | Variable en URL |
| `@Query('page')` | `@GET('/users')` | Query param `?page=1` |
| `@QueryMap()` | `@GET('/users')` | Múltiples query params |
| `@Body()` | `@POST('/users')` | Cuerpo de la petición |
| `@Header('Authorization')` | `@GET('/users')` | Header específico |
| `@Headers({'X-Api-Key': 'value'})` | `@GET('/users')` | Múltiples headers |
| `@Field('name')` | `@POST('/users')` | Form field (para FormData) |
| `@Part()` | `@POST('/upload')` | Parte de multipart |

### 3.3 Ejemplos Completos

```dart
@RestApi(baseUrl: 'https://api.example.com/v1')
abstract class ApiClient {
  factory ApiClient(Dio dio, {String baseUrl}) = _ApiClient;

  // Path param
  @GET('/users/{id}')
  Future<UserDto> getUser(@Path('id') String id);

  // Query params
  @GET('/users')
  Future<List<UserDto>> getUsers({
    @Query('page') int? page,
    @Query('limit') int? limit,
    @Query('search') String? query,
  });

  // Query map
  @GET('/users')
  Future<List<UserDto>> searchUsers(@QueryMap() Map<String, dynamic> filters);

  // POST con body
  @POST('/users')
  Future<UserDto> createUser(@Body() CreateUserDto user);

  // PUT con path + body
  @PUT('/users/{id}')
  Future<UserDto> updateUser(
    @Path('id') String id,
    @Body() UpdateUserDto user,
  );

  // DELETE
  @DELETE('/users/{id}')
  Future<void> deleteUser(@Path('id') String id);

  // Headers estáticos
  @GET('/admin/users')
  @Headers({
    'X-Admin-Role': 'true',
    'X-Request-Source': 'mobile',
  })
  Future<List<UserDto>> getAdminUsers();

  // Header dinámico
  @GET('/users/me')
  Future<UserDto> getCurrentUser(
    @Header('Authorization') String token,
  );

  // Form fields
  @POST('/auth/login')
  Future<AuthTokenDto> login(
    @Field('email') String email,
    @Field('password') String password,
  );

  // Multipart upload
  @POST('/files/upload')
  @MultiPart()
  Future<FileDto> uploadFile(@Part() FileParam file);

  // Respuesta sin procesar
  @GET('/raw')
  Future<HttpResponse<String>> getRawResponse();
}
```

---

## 4. Manejo de Errores

### 4.1 Interceptors de Dio

```dart
// lib/core/network/error_interceptor.dart
class ErrorInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    switch (err.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        throw NetworkTimeoutException();
      case DioExceptionType.badResponse:
        switch (err.response?.statusCode) {
          case 400:
            throw BadRequestException(err.response?.data['message']);
          case 401:
            throw UnauthorizedException();
          case 403:
            throw ForbiddenException();
          case 404:
            throw NotFoundException();
          case 500:
            throw ServerException();
        }
      case DioExceptionType.cancel:
        throw RequestCancelledException();
      default:
        throw NetworkException(err.message);
    }
  }
}
```

### 4.2 Wrapper con Either

```dart
class ApiClientWrapper {
  final ApiClient apiClient;

  ApiClientWrapper(this.apiClient);

  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final dto = await apiClient.getUser(id);
      return Right(dto.toDomain());
    } on NotFoundException {
      return Left(UserNotFoundFailure());
    } on UnauthorizedException {
      return Left(AuthFailure());
    } on ServerException {
      return Left(ServerFailure('Server error'));
    } on NetworkException {
      return Left(NetworkFailure());
    }
  }
}
```

### 4.3 Logging Interceptor

```dart
class LoggingInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    print('${options.method}: ${options.path}');
    print('Headers: ${options.headers}');
    print('Body: ${options.data}');
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    print('${response.statusCode}: ${response.requestOptions.path}');
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    print('ERROR: ${err.type} - ${err.message}');
    handler.next(err);
  }
}
```

---

## 5. Configuración Avanzada de Dio

### 5.1 Cliente Configurable

```dart
class ApiService {
  late final Dio _dio;
  late final ApiClient _apiClient;

  ApiService({required String baseUrl, required String? token}) {
    _dio = Dio(BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    // Interceptors
    _dio.interceptors.addAll([
      AuthInterceptor(token: token),
      LoggingInterceptor(),
      ErrorInterceptor(),
      RetryInterceptor(dio: _dio),
    ]);

    _apiClient = ApiClient(_dio, baseUrl: baseUrl);
  }
}
```

### 5.2 Interceptor de Autenticación

```dart
class AuthInterceptor extends Interceptor {
  String? _token;

  AuthInterceptor({String? token}) : _token = token;

  void updateToken(String token) => _token = token;

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (_token != null) {
      options.headers['Authorization'] = 'Bearer $_token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      // Token expirado
      _onTokenExpired();
    }
    handler.next(err);
  }

  void _onTokenExpired() {
    // Emitir evento para refrescar token
    // o redirigir al login
  }
}
```

### 5.3 Retry Interceptor

```dart
class RetryInterceptor extends Interceptor {
  final Dio dio;
  final int maxRetries;
  final Duration retryDelay;

  RetryInterceptor({
    required this.dio,
    this.maxRetries = 3,
    this.retryDelay = const Duration(seconds: 2),
  });

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (_shouldRetry(err)) {
      final retries = (err.requestOptions.extra['retries'] as int?) ?? 0;
      if (retries < maxRetries) {
        await Future.delayed(retryDelay * (retries + 1));
        err.requestOptions.extra['retries'] = retries + 1;
        try {
          final response = await dio.fetch(err.requestOptions);
          handler.resolve(response);
          return;
        } catch (e) {
          // Continuar con el error original si falla
        }
      }
    }
    handler.next(err);
  }

  bool _shouldRetry(DioException err) {
    return err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout ||
        err.type == DioExceptionType.connectionError ||
        (err.response?.statusCode ?? 0) >= 500;
  }
}
```

---

## 6. Integración con Clean Architecture

### 6.1 Estructura

```
lib/
├── core/
│   └── network/
│       ├── api_client.dart           # Anotaciones @RestApi
│       ├── api_client.g.dart         # GENERADO
│       ├── interceptors/
│       │   ├── auth_interceptor.dart
│       │   ├── error_interceptor.dart
│       │   ├── logging_interceptor.dart
│       │   └── retry_interceptor.dart
│       └── api_service.dart          # Configuración de Dio
└── features/
    └── users/
        ├── data/
        │   ├── models/
        │   │   └── user_dto.dart
        │   ├── datasources/
        │   │   └── user_remote_datasource.dart  # Usa api_client
        │   └── repositories/
        │       └── user_repository_impl.dart
        └── domain/...
```

### 6.2 Inyección con Injectable

```dart
// core/di/modules/network_module.dart
@module
abstract class NetworkModule {
  @lazySingleton
  Dio get dio => Dio(BaseOptions(
    connectTimeout: const Duration(seconds: 15),
    receiveTimeout: const Duration(seconds: 15),
  ));

  @lazySingleton
  ApiClient get apiClient => ApiClient(dio);

  @lazySingleton
  AuthInterceptor get authInterceptor => AuthInterceptor();
}
```

### 6.3 DataSource con Retrofit

```dart
// features/users/data/datasources/user_remote_datasource.dart
@lazySingleton
class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final ApiClient apiClient;

  UserRemoteDataSourceImpl(this.apiClient);

  @override
  Future<UserDto> getUser(String id) async {
    return apiClient.getUser(id);
  }

  @override
  Future<List<UserDto>> getUsers({int? page, int? limit}) async {
    return apiClient.getUsers(page: page, limit: limit);
  }
}
```

---

## 7. Testing con Retrofit

### 7.1 Mock de ApiClient

```dart
@mock
abstract class MockApiClient extends Mock implements ApiClient {}

void main() {
  late MockApiClient mockApiClient;
  late UserRemoteDataSource dataSource;

  setUp(() {
    mockApiClient = MockApiClient();
    dataSource = UserRemoteDataSourceImpl(mockApiClient);
  });

  test('getUser returns UserDto', () async {
    const userDto = UserDto(id: '1', name: 'Test', email: 'test@test.com');

    when(() => mockApiClient.getUser('1')).thenAnswer((_) async => userDto);

    final result = await dataSource.getUser('1');

    expect(result, equals(userDto));
    verify(() => mockApiClient.getUser('1')).called(1);
  });
}
```

### 7.2 Mock de Dio

```dart
void main() {
  late Dio mockDio;
  late ApiClient apiClient;

  setUp(() {
    mockDio = MockDio();
    apiClient = ApiClient(mockDio);
  });

  test('getUser handles 404', () async {
    when(() => mockDio.get<dynamic>('/users/999'))
        .thenThrow(DioException(
      requestOptions: RequestOptions(path: '/users/999'),
      response: Response(
        statusCode: 404,
        requestOptions: RequestOptions(path: '/users/999'),
      ),
    ));

    expect(
      () => apiClient.getUser('999'),
      throwsA(isA<DioException>()),
    );
  });
}
```

---

## 8. Buenas Prácticas

### 8.1 Versionado de API

```dart
@RestApi(baseUrl: 'https://api.example.com')
abstract class ApiV1 {
  factory ApiV1(Dio dio) = _ApiV1;

  @GET('/v1/users')
  Future<List<UserDto>> getUsers();
}

@RestApi(baseUrl: 'https://api.example.com')
abstract class ApiV2 {
  factory ApiV2(Dio dio) = _ApiV2;

  @GET('/v2/users')
  Future<List<UserDto>> getUsers();
}
```

### 8.2 Paginación

```dart
@RestApi(baseUrl: 'https://api.example.com')
abstract class ApiClient {
  factory ApiClient(Dio dio) = _ApiClient;

  @GET('/users')
  Future<HttpResponse<List<UserDto>>> getUsers(
    @Query('page') int page,
    @Query('limit') int limit,
  );
  // HttpResponse permite acceder a headers (X-Total-Count, etc.)
}
```

### 8.3 Cancelación de Requests

```dart
class UserCubit extends Cubit<UserState> {
  final ApiClient apiClient;
  CancelToken? _cancelToken;

  UserCubit(this.apiClient);

  Future<void> loadUsers() async {
    _cancelToken?.cancel('Nueva carga');
    _cancelToken = CancelToken();

    try {
      emit(Loading());
      final users = await apiClient.getUsers(cancelToken: _cancelToken);
      emit(Loaded(users));
    } on CancelException {
      // Request cancelada intencionalmente
    }
  }

  @override
  Future<void> close() {
    _cancelToken?.cancel('Cubit cerrado');
    return super.close();
  }
}
```

---

## 9. Resumen Ejecutivo

1. **Retrofit elimina el boilerplate** de clientes HTTP usando anotaciones
2. **Dio** es el motor HTTP subyacente (interceptors, cancelación, timeouts)
3. **Interceptors** separan concerns: auth, logging, retry, errores
4. **Integración natural** con json_serializable + injectable + freezed
5. **Testing** se simplifica con mocks tipados
6. **Código generado** es predecible y fácil de debuggear

---

## Recursos Adicionales

- [Retrofit pub.dev](https://pub.dev/packages/retrofit)
- [Dio pub.dev](https://pub.dev/packages/dio)
- [Retrofit Generator](https://pub.dev/packages/retrofit_generator)
- [Dio Interceptors Guide](https://docs.flutter.dev/data-and-backend/networking)

---

## Ver también

- [`08-HTTP`](../08-HTTP/README.md) — Conceptos básicos de HTTP y Dio
- [`04-ALMACENAMIENTO-LOCAL`](../04-ALMACENAMIENTO-LOCAL/README.md) — Persistencia local con drift, Hive

---

## En el siguiente módulo

**→ [08-flutter-gen-assets.md](./08-flutter-gen-assets.md)** — Flutter Gen: assets, splash, iconos y localización
