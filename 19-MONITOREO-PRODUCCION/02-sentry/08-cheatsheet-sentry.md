# 08 - Cheatsheet Sentry

## Setup Rapido

```dart
// pubspec.yaml
dependencies:
  sentry_flutter: ^8.14.2

// main.dart
await SentryFlutter.init(
  (options) {
    options.dsn = 'https://your-dsn@sentry.io/project-id';
    options.tracesSampleRate = 1.0;
    options.profilesSampleRate = 1.0;
    options.replay.sessionSampleRate = 0.1;
    options.replay.onErrorSampleRate = 1.0;
  },
  appRunner: () => runApp(
    SentryWidget(child: MyApp()),
  ),
);
```

---

## Comandos Esenciales

| Comando | Descripcion |
|---|---|
| `Sentry.captureException(error, stackTrace: stack)` | Capturar exception |
| `Sentry.captureMessage('message')` | Capturar mensaje |
| `Sentry.startTransaction('name', 'type')` | Iniciar transaccion |
| `Sentry.configureScope((scope) => ...)` | Configurar scope |
| `Sentry.addBreadcrumb(Breadcrumb(...))` | Agregar breadcrumb |
| `Sentry.setTag('key', 'value')` | Agregar tag |
| `Sentry.setUser(SentryUser(...))` | Establecer usuario |
| `Sentry.clearBreadcrumbs()` | Limpiar breadcrumbs |

---

## Error Handling

```dart
// Basico
try {
  await riskyOperation();
} catch (e, stack) {
  await Sentry.captureException(
    e,
    stackTrace: stack,
  );
}

// Con contexto
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

---

## Performance Tracing

```dart
// Transaction
final transaction = await Sentry.startTransaction(
  'checkout',
  'task',
  bindToScope: true,
);

try {
  await processPayment();
  transaction.status = SpanStatus.ok();
} catch (e) {
  transaction.status = SpanStatus.internalError();
} finally {
  await transaction.finish();
}

// Span
final span = transaction.startChild(
  'http.client',
  description: 'POST /api/payments',
);
try {
  await dio.post('/api/payments');
  span.status = SpanStatus.ok();
} catch (e) {
  span.status = SpanStatus.internalError();
} finally {
  await span.finish();
}
```

---

## Session Replay

```dart
await SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    
    // Session Replay
    options.replay.sessionSampleRate = 0.1;
    options.replay.onErrorSampleRate = 1.0;
    options.replay.maskAllText = true;
    options.replay.maskAllImages = true;
  },
);
```

---

## Scope Configuration

```dart
// Tags
Sentry.setTag('screen', 'checkout');
Sentry.setTag('payment_method', 'credit_card');

// User
Sentry.setUser(SentryUser(
  id: '12345',
  email: 'user@example.com',
  username: 'johndoe',
));

// Level
Sentry.setLevel(SentryLevel.error);

// Context
Sentry.setExtra('request_body', requestBody);
Sentry.setExtra('response_status', response.statusCode);
```

---

## Breadcrumbs

```dart
// Manual
Sentry.addBreadcrumb(Breadcrumb(
  message: 'User clicked checkout',
  category: 'ui',
  data: {
    'screen': 'cart',
    'items_count': 5,
  },
));

// Navegacion
Sentry.addBreadcrumb(Breadcrumb(
  message: 'Navigated to checkout',
  category: 'navigation',
  data: {
    'from': 'cart',
    'to': 'checkout',
  },
));
```

---

## Integracion con Dio

```dart
import 'package:sentry_dio/sentry_dio.dart';

class ApiClient {
  final Dio _dio = Dio();

  ApiClient() {
    _dio.addSentryInterceptor(
      maxRequestBodySize: MaxRequestBodySize.always,
      maxResponseBodySize: MaxResponseBodySize.always,
    );
  }
}
```

---

## Integracion con GoRouter

```dart
import 'package:sentry_flutter/sentry_flutter.dart';

final router = GoRouter(
  routes: [...],
  observers: [
    SentryNavigatorObserver(),
  ],
);
```

---

## Build Commands

```bash
# Upload dSYM (iOS)
sentry-cli upload-dif --org your-org --project your-project build/ios/archive/MyApp.xcarchive/dSYMs

# Upload ProGuard (Android)
sentry-cli upload-proguard --org your-org --project your-project build/app/outputs/mapping/release/mapping.txt

# Create release
sentry-cli releases --org your-org --project your-project new 1.0.0

# Finalize release
sentry-cli releases --org your-org --project your-project finalize 1.0.0
```

---

## Troubleshooting

| Problema | Solucion |
|---|---|
| Eventos no llegan | Verificar DSN |
| Debug symbols no suben | Usar Sentry CLI |
| Performance no funciona | Verificar tracesSampleRate |
| Session replay no graba | Verificar replay config |
| Integracion Jira no funciona | Verificar permisos |

---

## Metricas Clave

| Metrica | Meta | Formula |
|---|---|---|
| Crash-free sessions | > 98% | (sessions - crashes) / sessions * 100 |
| Crash-free users | > 98% | (users - affected users) / users * 100 |
| Top issues | < 5 | Issues con mas de 100 ocurrencias |
| Regressions | 0 | Issues que reaparecen |

---

## Links Utiles

- [Sentry Flutter SDK](https://docs.sentry.io/platforms/dart/guides/flutter/)
- [Sentry Performance](https://docs.sentry.io/platforms/dart/guides/flutter/performance/)
- [Sentry Session Replay](https://docs.sentry.io/platforms/dart/guides/flutter/session-replay/)
- [Sentry Dashboard](https://sentry.io)
