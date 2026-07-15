# 02 - Combinar Herramientas

## Por que combinar ambas?

Combinar Firebase Crashlytics y Sentry te da lo mejor de ambos mundos:

- **Crashlytics**: Crash reporting basico, analytics, BigQuery
- **Sentry**: Performance tracing, session replay, integraciones

---

## Arquitectura

```
Tu App Flutter
  ├── Firebase Crashlytics
  │   ├── Crash reporting automatico
  │   ├── Analytics basico
  │   └── Export a BigQuery
  └── Sentry
      ├── Performance tracing
      ├── Session replay
      ├── Integraciones Jira/GitHub
      └── Release health
```

---

## Setup basico

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:sentry_flutter/sentry_flutter.dart';
import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Firebase
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // Sentry
  await SentryFlutter.init(
    (options) {
      options.dsn = 'your-sentry-dsn';
      options.tracesSampleRate = 1.0;
    },
    appRunner: () => runApp(
      SentryWidget(child: MyApp()),
    ),
  );
}
```

---

## Error handlers

```dart
// lib/main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp();
  await SentryFlutter.init(
    (options) {
      options.dsn = 'your-sentry-dsn';
    },
    appRunner: () {
      // Flutter error handler - ambos
      FlutterError.onError = (details) {
        // Crashlytics
        FirebaseCrashlytics.instance.recordFlutterFatalError(details);
        
        // Sentry
        Sentry.captureException(
          details.exception,
          stackTrace: details.stack,
        );
      };

      // Async error handler
      runZonedGuarded(() {
        runApp(MyApp());
      }, (error, stack) {
        // Crashlytics
        FirebaseCrashlytics.instance.recordError(error, stack);
        
        // Sentry
        Sentry.captureException(error, stackTrace: stack);
      });
    },
  );
}
```

---

## Servicio de monitoreo

```dart
// lib/core/monitoring/monitoring_service.dart
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

class MonitoringService {
  final FirebaseCrashlytics _crashlytics;

  MonitoringService(this._crashlytics);

  // Reportar error a ambas herramientas
  Future<void> reportError(
    dynamic error,
    StackTrace stack, {
    required String context,
    Map<String, dynamic>? additionalInfo,
  }) async {
    // Crashlytics
    await _crashlytics.recordError(
      error,
      stack,
      reason: context,
      information: additionalInfo?.entries
          .map((e) => '${e.key}: ${e.value}')
          .toList(),
    );

    // Sentry
    await Sentry.captureException(
      error,
      stackTrace: stack,
      hint: Hint.withMap({
        'context': context,
        ...?additionalInfo,
      }),
    );
  }

  // Performance tracking (solo Sentry)
  Future<T> trackPerformance<T>(
    String name,
    String operation,
    Future<T> Function() task,
  ) async {
    final transaction = await Sentry.startTransaction(
      name,
      operation,
      bindToScope: true,
    );

    try {
      final result = await task();
      transaction.status = SpanStatus.ok();
      return result;
    } catch (e) {
      transaction.status = SpanStatus.internalError();
      rethrow;
    } finally {
      await transaction.finish();
    }
  }

  // Custom keys (ambas)
  Future<void> setCustomKey(String key, String value) async {
    // Crashlytics
    await _crashlytics.setCustomKey(key, value);
    
    // Sentry
    Sentry.setTag(key, value);
  }

  // User context (ambas)
  Future<void> setUser(User user) async {
    // Crashlytics
    await _crashlytics.setUserIdentifier(user.id);
    
    // Sentry
    await Sentry.configureScope((scope) {
      scope.setUser(SentryUser(
        id: user.id,
        email: user.email,
      ));
    });
  }

  // Breadcrumbs (solo Sentry)
  void addBreadcrumb({
    required String message,
    required String category,
    Map<String, dynamic>? data,
  }) {
    Sentry.addBreadcrumb(Breadcrumb(
      message: message,
      category: category,
      data: data,
    ));
  }
}
```

---

## Ejemplo: Auth Service

```dart
// lib/features/auth/data/services/auth_service.dart
class AuthService {
  final SupabaseClient _supabase;
  final MonitoringService _monitoring;

  AuthService(this._supabase, this._monitoring);

  Future<User> login(String email, String password) async {
    // Breadcrumb (solo Sentry)
    _monitoring.addBreadcrumb(
      message: 'Login attempt',
      category: 'auth',
      data: {'email': email},
    );

    try {
      final response = await _supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );

      if (response.user == null) {
        throw AuthException('User not found');
      }

      // User context (ambas)
      final user = UserMapper.fromSupabaseUser(response.user!);
      await _monitoring.setUser(user);

      return user;
    } catch (e, stack) {
      // Error reporting (ambas)
      await _monitoring.reportError(
        e,
        stack,
        context: 'Login failed',
        additionalInfo: {
          'email': email,
          'error': e.toString(),
        },
      );
      rethrow;
    }
  }
}
```

---

## Ejemplo: Product Repository

```dart
// lib/features/products/data/repositories/product_repository_impl.dart
class ProductRepositoryImpl implements ProductRepository {
  final SupabaseClient _supabase;
  final MonitoringService _monitoring;

  ProductRepositoryImpl(this._supabase, this._monitoring);

  @override
  Future<List<Product>> getProducts({int page = 1, int limit = 20}) async {
    // Performance tracking (solo Sentry)
    return _monitoring.trackPerformance(
      'get_products',
      'repository',
      () async {
        try {
          final response = await _supabase
              .from('products')
              .select()
              .range(page * limit, (page + 1) * limit - 1);

          return response.map((json) => ProductMapper.fromMap(json)).toList();
        } catch (e, stack) {
          // Error reporting (ambas)
          await _monitoring.reportError(
            e,
            stack,
            context: 'Failed to get products',
            additionalInfo: {
              'page': page,
              'limit': limit,
            },
          );
          rethrow;
        }
      },
    );
  }
}
```

---

## Ventajas de combinar

| Ventaja | Descripcion |
|---|---|
| Redundancia | Si una falla, la otra captura |
| Complemento | Cada una cubre debilidades de la otra |
| Flexibilidad | Usar la mejor herramienta para cada caso |
| Migracion gradual | Migrar paso a paso |

---

## Desventajas de combinar

| Desventaja | Descripcion |
|---|---|
| Duplicidad | Errores reportados en ambos lugares |
| Complejidad | Mantener dos integraciones |
| Costo | Sentry cobra por uso |
| Consistencia | Mantener configuracion sincronizada |

---

## Cuando NO combinar

- Presupuesto muy limitado
- App simple sin necesidades avanzadas
- Equipo pequeño sin recursos para mantener ambas
- No necesitas features de una de ellas

---

## Siguiente paso

[03 - Guia de Migracion](./03-migracion-guia.md) - Como migrar de Crashlytics a Sentry
