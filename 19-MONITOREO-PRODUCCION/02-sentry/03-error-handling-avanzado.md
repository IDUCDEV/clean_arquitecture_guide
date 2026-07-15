# 03 - Error Handling Avanzado

## captureException

El metodo principal para reportar errores en Sentry.

```dart
import 'package:sentry_flutter/sentry_flutter.dart';

try {
  await riskyOperation();
} catch (e, stack) {
  await Sentry.captureException(
    e,
    stackTrace: stack,
  );
}
```

---

## withScope

Permite agregar contexto detallado a cada error.

```dart
try {
  await riskyOperation();
} catch (e, stack) {
  await Sentry.captureException(
    e,
    stackTrace: stack,
    hint: Hint.withMap({
      'operation': 'riskyOperation',
      'user_id': '12345',
    }),
  );
}
```

### Scope personalizado

```dart
await Sentry.configureScope((scope) {
  scope.setTag('screen', 'checkout');
  scope.setTag('payment_method', 'credit_card');
  scope.setUser(SentryUser(
    id: '12345',
    email: 'user@example.com',
    username: 'johndoe',
  ));
  scope.level = SentryLevel.error;
});
```

---

## Tags vs Extras

### Tags (para filtrar y buscar)

```dart
await Sentry.captureException(
  error,
  stackTrace: stack,
  hint: Hint.withMap({
    'screen': 'checkout',
    'payment_method': 'credit_card',
    'error_type': 'validation',
  }),
);
```

### Extras (para contexto detallado)

```dart
await Sentry.captureException(
  error,
  stackTrace: stack,
  hint: Hint.withMap({
    'request_body': requestBody,
    'response_status': response.statusCode,
    'response_body': response.body,
  }),
);
```

---

## Breadcrumbs

Los breadcrumbs son **registros de eventos** que ayudan a reconstruir la secuencia de acciones.

### Breadcrumbs automaticos

Sentry registra automaticamente:
- Navegacion (si usas SentryNavigatorObserver)
- HTTP requests (si usas sentry_dio)
- Lifecycle events

### Breadcrumbs manuales

```dart
// Agregar breadcrumb
Sentry.addBreadcrumb(Breadcrumb(
  message: 'User clicked checkout button',
  category: 'ui',
  data: {
    'screen': 'cart',
    'items_count': cart.items.length,
  },
));

// Agregar breadcrumb de navegacion
Sentry.addBreadcrumb(Breadcrumb(
  message: 'Navigated to checkout',
  category: 'navigation',
  data: {
    'from': 'cart',
    'to': 'checkout',
  },
));

// Agregar breadcrumb de HTTP
Sentry.addBreadcrumb(Breadcrumb(
  message: 'POST /api/payments',
  category: 'http',
  data: {
    'method': 'POST',
    'url': '/api/payments',
    'status_code': 200,
    'duration_ms': 1234,
  },
));
```

---

## captureMessage

Para errores que no son exceptions.

```dart
// Capturar mensaje informativo
await Sentry.captureMessage(
  'User completed checkout',
  level: SentryLevel.info,
  hint: Hint.withMap({
    'order_id': '12345',
    'total': 99.99,
  }),
);

// Capturar warning
await Sentry.captureMessage(
  'Slow API response detected',
  level: SentryLevel.warning,
  hint: Hint.withMap({
    'endpoint': '/api/products',
    'duration_ms': 5000,
  }),
);

// Capturar error
await Sentry.captureMessage(
  'Cache corruption detected',
  level: SentryLevel.error,
  hint: Hint.withMap({
    'cache_key': 'products_list',
    'error': 'Invalid JSON',
  }),
);
```

---

## Ejemplo completo: Auth Service

```dart
// lib/features/auth/data/services/auth_service.dart
import 'package:sentry_flutter/sentry_flutter.dart';

class AuthService {
  final SupabaseClient _supabase;

  AuthService(this._supabase);

  Future<User> login(String email, String password) async {
    // Agregar breadcrumb
    Sentry.addBreadcrumb(Breadcrumb(
      message: 'Login attempt',
      category: 'auth',
      data: {'email': email},
    ));

    try {
      final response = await _supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );

      if (response.user == null) {
        throw AuthException('User not found');
      }

      // Configurar scope con usuario
      await Sentry.configureScope((scope) {
        scope.setUser(SentryUser(
          id: response.user!.id,
          email: response.user!.email,
        ));
        scope.setTag('user_plan', response.user!.userMetadata?['plan'] ?? 'free');
      });

      Sentry.addBreadcrumb(Breadcrumb(
        message: 'Login successful',
        category: 'auth',
        data: {'user_id': response.user!.id},
      ));

      return UserMapper.fromSupabaseUser(response.user!);
    } on AuthException catch (e, stack) {
      await Sentry.captureException(
        e,
        stackTrace: stack,
        hint: Hint.withMap({
          'email': email,
          'error_code': e.message,
        }),
      );
      rethrow;
    } catch (e, stack) {
      await Sentry.captureException(
        e,
        stackTrace: stack,
        hint: Hint.withMap({
          'email': email,
          'error_type': 'unexpected',
        }),
      );
      rethrow;
    }
  }

  Future<void> logout() async {
    Sentry.addBreadcrumb(Breadcrumb(
      message: 'Logout',
      category: 'auth',
    ));

    await _supabase.auth.signOut();

    // Limpiar scope
    await Sentry.configureScope((scope) {
      scope.clearUser();
      scope.removeTag('user_plan');
    });
  }
}
```

---

## Ejemplo completo: HTTP Client

```dart
// lib/core/network/http_client.dart
import 'package:dio/dio.dart';
import 'package:sentry_dio/sentry_dio.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

class ApiClient {
  late final Dio _dio;

  ApiClient() {
    _dio = Dio();
    
    // Agregar interceptor de Sentry
    _dio.addSentryInterceptor(
      maxRequestBodySize: MaxRequestBodySize.always,
      maxResponseBodySize: MaxResponseBodySize.always,
    );
  }

  Future<Map<String, dynamic>> get(String endpoint) async {
    final transaction = await Sentry.startTransaction(
      'GET $endpoint',
      'http.client',
      bindToScope: true,
    );

    try {
      final response = await _dio.get(
        'https://api.example.com$endpoint',
      );

      transaction.setData('response_status', response.statusCode);

      return response.data;
    } on DioException catch (e, stack) {
      transaction.setData('error_type', e.type.toString());
      
      await Sentry.captureException(
        e,
        stackTrace: stack,
        hint: Hint.withMap({
          'endpoint': endpoint,
          'method': 'GET',
          'status_code': e.response?.statusCode,
        }),
      );
      
      rethrow;
    } finally {
      await transaction.finish();
    }
  }

  Future<Map<String, dynamic>> post(
    String endpoint, {
    required Map<String, dynamic> data,
  }) async {
    final transaction = await Sentry.startTransaction(
      'POST $endpoint',
      'http.client',
      bindToScope: true,
    );

    try {
      final response = await _dio.post(
        'https://api.example.com$endpoint',
        data: data,
      );

      transaction.setData('response_status', response.statusCode);

      return response.data;
    } on DioException catch (e, stack) {
      transaction.setData('error_type', e.type.toString());
      
      await Sentry.captureException(
        e,
        stackTrace: stack,
        hint: Hint.withMap({
          'endpoint': endpoint,
          'method': 'POST',
          'request_data': data,
          'status_code': e.response?.statusCode,
        }),
      );
      
      rethrow;
    } finally {
      await transaction.finish();
    }
  }
}
```

---

## Resumen

| Metodo | Uso | Ejemplo |
|---|---|---|
| `captureException` | Errores con stack trace | `try/catch` |
| `captureMessage` | Mensajes informativos | Logs de negocio |
| `configureScope` | Contexto global | User ID, tags |
| `addBreadcrumb` | Secuencia de eventos | Navegacion, HTTP |

---

## Siguiente paso

[04 - Performance Tracing](./04-performance-tracing.md) - Medir tiempos de ejecucion
