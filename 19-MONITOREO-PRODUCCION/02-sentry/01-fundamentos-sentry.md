# 01 - Fundamentos de Sentry

## Que es Sentry?

Sentry es una plataforma de **monitoreo de errores y performance** que ayuda a detectar, diagnosticar y resolver problemas en tiempo real. A diferencia de Crashlytics, Sentry ofrece:

- **Performance tracing** - Medir tiempos de ejecucion
- **Session replay** - Ver que vio el usuario antes del error
- **Integraciones bidireccionales** - Jira, GitHub, Slack
- **Release health** - Comparar estabilidad entre versiones
- **Feature flags** - Rastrear features por release

---

## Sentry vs Crashlytics

| Feature | Sentry | Crashlytics |
|---|---|---|
| **Error monitoring** | Avanzado | Basico |
| **Performance tracing** | Si | No nativo |
| **Session replay** | Si | No |
| **Profiling** | Si (iOS/macOS) | No |
| **Integraciones** | Bidireccionales | Unidireccionales |
| **Release health** | Avanzado | Basico |
| **Feature flags** | Si | No |
| **User feedback** | Si | No |
| **Precio** | Gratis hasta 5K | Gratis ilimitado |
| **Debug symbols** | Manual upload | Automatico |

---

## Arquitectura de Sentry

```
Tu App Flutter
  └── Sentry SDK
    └── Captura errores y performance
      └── Envía a Sentry Backend
        └── Sentry procesa y agrupa
          └── Dashboard en web
            └── Tu equipo revisa
              └── Resuelve problemas
```

---

## Pricing Detallado

### Developer (Gratis)

- 5,000 errores/mes
- 10,000 transacciones/mes
- 1 GB de almacenamiento
- 30 dias de retencion
- Email notifications

### Team ($26/user/mes)

- 50,000 errores/mes
- 100,000 transacciones/mes
- 10 GB de almacenamiento
- 90 dias de retencion
- Session replay
- Feature flags
- Jira integration

### Business ($80/user/mes)

- 500,000 errores/mes
- 1,000,000 transacciones/mes
- 100 GB de almacenamiento
- 90 dias de retencion
- Advanced analytics
- SLA 99.9%
- Priority support

---

## Features Principales

### 1. Error Monitoring

Captura errores automaticamente y con contexto detallado.

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

### 2. Performance Tracking

Mide el tiempo de operaciones criticas.

```dart
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
```

### 3. Session Replay

Graba la pantalla del usuario antes del error.

```dart
SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    options.replay.sessionSampleRate = 0.1;
    options.replay.onErrorSampleRate = 1.0;
  },
);
```

### 4. Release Health

Compara estabilidad entre versiones.

```dart
Sentry.configureScope((scope) {
  scope.setTag('release', '1.0.0');
  scope.setTag('environment', 'production');
});
```

### 5. Feature Flags

Rastrea features por release.

```dart
final flagEnabled = await Sentry.getFeatureFlag('new-checkout');
if (flagEnabled) {
  // Nueva feature
} else {
  // Feature antigua
}
```

---

## Requisitos

| Requisito | Version minima |
|---|---|
| Flutter | 3.24.0+ |
| Dart | 3.5.0+ |
| sentry_flutter | 8.0.0+ |

---

## Cuando usar Sentry

| Escenario | Por que Sentry |
|---|---|
| Necesitas performance tracing | Sentry es superior |
| Quieres session replay | Solo Sentry lo ofrece |
| Integracion bidireccional Jira | Sentry es mejor |
| Necesitas release health | Sentry es mas detallado |
| Feature flags | Solo Sentry lo ofrece |
| Budget limitado | Crashlytics es gratis |

---

## Siguiente paso

[02 - Setup Sentry](./02-setup-sentry.md) - Configurar Sentry en tu proyecto Flutter
