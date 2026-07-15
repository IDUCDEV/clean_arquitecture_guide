# 02 - Setup Sentry

## Prerrequisitos

1. Cuenta en [sentry.io](https://sentry.io)
2. Proyecto creado en Sentry
3. DSN del proyecto

---

## Paso 1: Crear proyecto en Sentry

1. Ir a [sentry.io](https://sentry.io)
2. Crear cuenta o login
3. "Create Project"
4. Seleccionar "Flutter"
5. Nombre del proyecto
6. Copiar el DSN

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

### Opcion A: Configuracion basica

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await SentryFlutter.init(
    (options) {
      options.dsn = 'https://your-dsn@sentry.io/project-id';
      options.tracesSampleRate = 1.0;
      options.profilesSampleRate = 1.0;
      options.debug = true; // Solo en debug
    },
    appRunner: () => runApp(MyApp()),
  );
}
```

### Opcion B: Configuracion avanzada

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await SentryFlutter.init(
    (options) {
      options.dsn = 'https://your-dsn@sentry.io/project-id';
      
      // Performance
      options.tracesSampleRate = 1.0;
      options.profilesSampleRate = 1.0;
      
      // Session Replay
      options.replay.sessionSampleRate = 0.1;
      options.replay.onErrorSampleRate = 1.0;
      
      // Logging
      options.enableLogs = true;
      
      // Debug
      options.debug = kDebugMode;
      
      // Environment
      options.environment = kDebugMode ? 'development' : 'production';
      
      // Release
      options.release = '1.0.0';
      
      // Before send
      options.beforeSend = (event, hint) {
        // Filtrar eventos en debug
        if (kDebugMode) return null;
        
        // Filtrar eventos no criticos
        if (event.level == SentryLevel.info) return null;
        
        return event;
      };
    },
    appRunner: () => runApp(
      SentryWidget(child: MyApp()),
    ),
  );
}
```

---

## Paso 4: Configurar error handlers

```dart
// lib/main.dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Configurar Sentry
  await SentryFlutter.init(
    (options) {
      options.dsn = 'https://your-dsn@sentry.io/project-id';
      options.tracesSampleRate = 1.0;
    },
    appRunner: () => runZonedGuarded(() {
      runApp(MyApp());
    }, (error, stack) {
      // Capturar errores asincronos
      Sentry.captureException(
        error,
        stackTrace: stack,
      );
    }),
  );

  // Error handler para Flutter errors
  FlutterError.onError = (FlutterErrorDetails details) {
    Sentry.captureException(
      details.exception,
      stackTrace: details.stack,
    );
  };
}
```

---

## Paso 5: Configurar Scope

```dart
// lib/main.dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await SentryFlutter.init(
    (options) {
      options.dsn = 'https://your-dsn@sentry.io/project-id';
      options.tracesSampleRate = 1.0;
    },
    appRunner: () async {
      // Configurar scope global
      Sentry.configureScope((scope) {
        scope.setTag('app_version', '1.0.0');
        scope.setTag('environment', 'production');
        scope.setLevel(SentryLevel.error);
      });

      runApp(MyApp());
    },
  );
}
```

---

## Paso 6: Integracion con GoRouter

```dart
// lib/core/router/app_router.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

class AppRouter {
  late final GoRouter router;

  AppRouter() {
    router = GoRouter(
      initialLocation: '/',
      routes: [
        GoRoute(
          path: '/',
          builder: (context, state) => HomeScreen(),
        ),
        GoRoute(
          path: '/products',
          builder: (context, state) => ProductsScreen(),
        ),
      ],
      observers: [
        SentryNavigatorObserver(), // Agregar observer
      ],
    );
  }
}

// En main.dart
await SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    options.tracesSampleRate = 1.0;
    options.navigatorKey = navigatorKey; // Tu navigator key
  },
);
```

---

## Paso 7: Verificar Setup

### En Debug

```dart
// Boton de prueba
ElevatedButton(
  onPressed: () async {
    try {
      throw Exception('Test error from Flutter!');
    } catch (e, stack) {
      final eventId = await Sentry.captureException(
        e,
        stackTrace: stack,
      );
      print('Event ID: $eventId');
    }
  },
  child: Text('Test Sentry'),
),
```

### Verificar en Sentry Dashboard

1. Ir a [sentry.io](https://sentry.io)
2. Seleccionar proyecto
3. Ir a "Issues"
4. Verificar que el error aparece

---

## Paso 8: Upload Debug Symbols

### Android (ProGuard)

```android/app/build.gradle
android {
    buildTypes {
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

// proguard-rules.pro
-keep class io.sentry.** { *; }
```

### iOS (dSYM)

```bash
# Instalar Sentry CLI
npm install -g @sentry/cli

# Upload dSYM
sentry-cli upload-dif --org your-org --project your-project build/ios/archive/MyApp.xcarchive/dSYMs
```

### Automatico con CI/CD

```yaml
# .github/workflows/build.yml
- name: Upload Debug Symbols
  run: |
    curl -sL https://sentry.io/get-cli/ | bash
    sentry-cli upload-dif --org your-org --project your-project build/ios/archive/MyApp.xcarchive/dSYMs
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
```

---

## Troubleshooting

| Problema | Solucion |
|---|---|
| Eventos no llegan | Verificar DSN |
| Debug symbols no suben | Usar Sentry CLI |
| Performance no funciona | Verificar tracesSampleRate |
| Session replay no graba | Verificar replay config |

---

## Siguiente paso

[03 - Error Handling Avanzado](./03-error-handling-avanzado.md) - Manejar errores con contexto detallado
