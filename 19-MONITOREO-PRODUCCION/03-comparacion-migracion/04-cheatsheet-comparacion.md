# 04 - Cheatsheet Comparacion

## Crashlytics vs Sentry

| Feature | Crashlytics | Sentry |
|---|---|---|
| **Precio** | Gratis (ilimitado) | Gratis (5K errores/mes) |
| **Crash reporting** | Automatico | Automatico |
| **Non-fatal errors** | Manual | Automatico |
| **Performance tracing** | No | Si |
| **Session replay** | No | Si |
| **Profiling** | No | Si (iOS/macOS) |
| **Integracion Jira** | Unidireccional | Bidireccional |
| **Integracion GitHub** | No nativa | Bidireccional |
| **Release health** | Basico | Avanzado |
| **Feature flags** | No | Si |
| **User feedback** | No | Si |
| **Analytics** | Firebase Analytics | Sentry Analytics |
| **Export SQL** | BigQuery (gratis) | No nativo |
| **Alertas** | Email, Slack, PagerDuty | Email, Slack, PagerDuty, Jira |
| **Debug symbols** | Automatico | Manual |
| **Setup** | Facil | Medio |

---

## Cuando usar que

| Necesidad | Herramienta |
|---|---|
| Crash reporting basico | Crashlytics |
| Performance tracing | Sentry |
| Session replay | Sentry |
| Integracion Jira | Sentry |
| Release health | Sentry |
| Analytics | Crashlytics |
| Export SQL | Crashlytics |
| Budget limitado | Crashlytics |
| Features avanzadas | Sentry |

---

## Combinar ambas

```dart
// Error handler - ambas
FlutterError.onError = (details) {
  FirebaseCrashlytics.instance.recordFlutterFatalError(details);
  Sentry.captureException(details.exception, stackTrace: details.stack);
};

// Custom keys - ambas
await FirebaseCrashlytics.instance.setCustomKey('key', 'value');
Sentry.setTag('key', 'value');

// User context - ambas
await FirebaseCrashlytics.instance.setUserIdentifier(user.id);
Sentry.configureScope((scope) => scope.setUser(SentryUser(id: user.id)));
```

---

## Migracion rapida

```dart
// 1. Instalar Sentry
// pubspec.yaml: sentry_flutter: ^8.14.2

// 2. Configurar
await SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    options.tracesSampleRate = 1.0;
  },
);

// 3. Migrar error handlers
FlutterError.onError = (details) {
  FirebaseCrashlytics.instance.recordFlutterFatalError(details);
  Sentry.captureException(details.exception, stackTrace: details.stack);
};

// 4. Migrar custom keys
await FirebaseCrashlytics.instance.setCustomKey('key', 'value');
Sentry.setTag('key', 'value');

// 5. Migrar user context
await FirebaseCrashlytics.instance.setUserIdentifier(user.id);
Sentry.configureScope((scope) => scope.setUser(SentryUser(id: user.id)));
```

---

## Links utiles

- [Firebase Crashlytics](https://firebase.google.com/docs/crashlytics?hl=es-419)
- [Sentry Flutter SDK](https://docs.sentry.io/platforms/dart/guides/flutter/)
- [Sentry Pricing](https://sentry.io/pricing/)
