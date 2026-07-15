# 03 - Guia de Migracion

## Cuando migrar

Migra de Crashlytics a Sentry si:

- Necesitas performance tracing
- Necesitas session replay
- Necesitas integraciones Jira/GitHub
- Necesitas release health avanzado
- Necesitas feature flags
- Crashlytics no cubre tus necesidades

---

## Fases de migracion

### Fase 1: Preparacion (1-2 dias)

1. Crear cuenta en Sentry
2. Crear proyecto en Sentry
3. Instalar dependencias
4. Configurar Sentry en paralelo

### Fase 2: Implementacion (2-3 dias)

1. Configurar error handlers
2. Migrar custom keys
3. Migrar user context
4. Migrar breadcrumbs

### Fase 3: Testing (1-2 dias)

1. Verificar que Sentry recibe errores
2. Verificar performance tracking
3. Verificar session replay
4. Verificar integraciones

### Fase 4: Despliegue (1 dia)

1. Desplegar con ambas herramientas
2. Monitorear ambas durante 1 semana
3. Verificar que no hay errores faltantes
4. Desactivar Crashlytics (opcional)

---

## Paso 1: Crear proyecto Sentry

1. Ir a [sentry.io](https://sentry.io)
2. Crear cuenta
3. "Create Project"
4. Seleccionar "Flutter"
5. Copiar DSN

---

## Paso 2: Instalar dependencias

```yaml
# pubspec.yaml
dependencies:
  sentry_flutter: ^8.14.2
```

```bash
flutter pub get
```

---

## Paso 3: Configurar Sentry

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp();

  await SentryFlutter.init(
    (options) {
      options.dsn = 'your-sentry-dsn';
      options.tracesSampleRate = 1.0;
    },
    appRunner: () => runApp(MyApp()),
  );
}
```

---

## Paso 4: Migrar error handlers

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
      // Flutter error handler
      FlutterError.onError = (details) {
        // Mantener Crashlytics temporalmente
        FirebaseCrashlytics.instance.recordFlutterFatalError(details);
        
        // Agregar Sentry
        Sentry.captureException(
          details.exception,
          stackTrace: details.stack,
        );
      };

      // Async error handler
      runZonedGuarded(() {
        runApp(MyApp());
      }, (error, stack) {
        // Mantener Crashlytics temporalmente
        FirebaseCrashlytics.instance.recordError(error, stack);
        
        // Agregar Sentry
        Sentry.captureException(error, stackTrace: stack);
      });
    },
  );
}
```

---

## Paso 5: Migrar custom keys

```dart
// Antes (solo Crashlytics)
await FirebaseCrashlytics.instance.setCustomKey('screen', 'checkout');

// Despues (ambas)
await FirebaseCrashlytics.instance.setCustomKey('screen', 'checkout');
Sentry.setTag('screen', 'checkout');
```

---

## Paso 6: Migrar user context

```dart
// Antes (solo Crashlytics)
await FirebaseCrashlytics.instance.setUserIdentifier(user.id);

// Despues (ambas)
await FirebaseCrashlytics.instance.setUserIdentifier(user.id);
await Sentry.configureScope((scope) {
  scope.setUser(SentryUser(
    id: user.id,
    email: user.email,
  ));
});
```

---

## Paso 7: Migrar breadcrumbs

```dart
// Antes (solo Crashlytics)
FirebaseCrashlytics.instance.log('User clicked checkout');

// Despues (ambas)
FirebaseCrashlytics.instance.log('User clicked checkout');
Sentry.addBreadcrumb(Breadcrumb(
  message: 'User clicked checkout',
  category: 'ui',
));
```

---

## Paso 8: Migrar non-fatal errors

```dart
// Antes (solo Crashlytics)
try {
  await riskyOperation();
} catch (e, stack) {
  await FirebaseCrashlytics.instance.recordError(e, stack);
}

// Despues (ambas)
try {
  await riskyOperation();
} catch (e, stack) {
  await FirebaseCrashlytics.instance.recordError(e, stack);
  await Sentry.captureException(e, stackTrace: stack);
}
```

---

## Paso 9: Testing

### Verificar errores

1. Forzar error en la app
2. Ir a Firebase Console → Crashlytics
3. Verificar que el error aparece
4. Ir a Sentry → Issues
5. Verificar que el error aparece

### Verificar performance

1. Ir a Sentry → Performance
2. Verificar transacciones
3. Verificar spans

### Verificar session replay

1. Ir a Sentry → Replays
2. Verificar sesiones grabadas

---

## Paso 10: Desactivar Crashlytics (opcional)

Si decides usar solo Sentry:

```dart
// lib/main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp();

  // Desactivar Crashlytics
  await FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(false);

  await SentryFlutter.init(
    (options) {
      options.dsn = 'your-sentry-dsn';
    },
    appRunner: () => runApp(MyApp()),
  );
}
```

---

## Rollback

Si necesitas volver a Crashlytics:

1. Desactivar Sentry
2. Activar Crashlytics
3. Desplegar version anterior
4. Verificar que Crashlytics recibe errores

---

## Timeline recomendada

| Fase | Duracion | Actividades |
|---|---|---|
| Preparacion | 1-2 dias | Setup Sentry, instalar dependencias |
| Implementacion | 2-3 dias | Migrar error handlers, custom keys |
| Testing | 1-2 dias | Verificar errores, performance |
| Despliegue | 1 dia | Desplegar, monitorear |
| **Total** | **5-8 dias** | |

---

## Tips de migracion

1. **Migrar gradualmente**: No desactives Crashlytics inmediatamente
2. **Monitorear ambas**: Durante 1-2 semanas
3. **Verificar cobertura**: Asegurar que todos los errores se capturan
4. **Documentar cambios**: Mantener registro de lo que se cambio
5. **Testear en staging**: Antes de produccion

---

## Siguiente paso

[04 - Cheatsheet Comparacion](./04-cheatsheet-comparacion.md) - Referencia rapida
