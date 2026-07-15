# 05 - Session Replay

## Que es Session Replay?

Session replay **graba la pantalla del usuario** antes, durante y despues de un error. Permite ver exactamente que vio el usuario y que acciones tomo.

---

## Por que usar Session Replay?

| Ventaja | Descripcion |
|---|---|
| Reproducir bugs | Ver exactamente que vio el usuario |
| Entender contexto | Ver la UI antes del error |
| Diagnosticar problemas | Identificar problemas de UX |
| Validar fixes | Verificar que el fix funciona |

---

## Configuracion basica

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await SentryFlutter.init(
    (options) {
      options.dsn = 'https://your-dsn@sentry.io/project-id';
      
      // Session Replay
      options.replay.sessionSampleRate = 0.1;  // 10% de sesiones
      options.replay.onErrorSampleRate = 1.0;   // 100% de errores
    },
    appRunner: () => runApp(
      SentryWidget(child: MyApp()),
    ),
  );
}
```

---

## Configuracion avanzada

```dart
await SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    
    // Session Replay
    options.replay.sessionSampleRate = 0.1;  // 10% de sesiones
    options.replay.onErrorSampleRate = 1.0;   // 100% de errores
    
    // Privacy
    options.replay.maskAllText = true;        // Enmascarar texto
    options.replay.maskAllImages = true;      // Enmascarar imagenes
    
    // Network
    options.replay.recordHttp = true;         // Grabar requests HTTP
    options.replay.maskHttpRequests = true;   // Enmascarar URLs
  },
  appRunner: () => runApp(
    SentryWidget(child: MyApp()),
  ),
);
```

---

## Sampling

### Session Sample Rate

Porcentaje de sesiones completas que se graban.

```dart
options.replay.sessionSampleRate = 0.1;  // 10% de sesiones
```

### On Error Sample Rate

Porcentaje de errores que incluyen replay.

```dart
options.replay.onErrorSampleRate = 1.0;  // 100% de errores
```

### Estrategia recomendada

```dart
if (kDebugMode) {
  // En debug: grabar todo
  options.replay.sessionSampleRate = 1.0;
  options.replay.onErrorSampleRate = 1.0;
} else if (kProfileMode) {
  // En profile: grabar mucho
  options.replay.sessionSampleRate = 0.5;
  options.replay.onErrorSampleRate = 1.0;
} else {
  // En release: grabar poco
  options.replay.sessionSampleRate = 0.1;
  options.replay.onErrorSampleRate = 1.0;
}
```

---

## Privacy Controls

### Enmascarar texto

```dart
options.replay.maskAllText = true;
```

### Enmascarar imagenes

```dart
options.replay.maskAllImages = true;
```

### Enmascarar URLs

```dart
options.replay.maskHttpRequests = true;
```

### Widgets especificos

```dart
// Enmascarar widget especifico
SentryReplayMask(
  child: TextField(
    controller: passwordController,
  ),
)

// No enmascarar widget especifico
SentryReplayUnmask(
  child: Text('Safe to show'),
)
```

---

## Ejemplo completo

```dart
// lib/main.dart
import 'package:flutter/foundation.dart';
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
      if (kDebugMode) {
        options.replay.sessionSampleRate = 1.0;
        options.replay.onErrorSampleRate = 1.0;
      } else {
        options.replay.sessionSampleRate = 0.1;
        options.replay.onErrorSampleRate = 1.0;
      }
      
      // Privacy
      options.replay.maskAllText = true;
      options.replay.maskAllImages = true;
      
      // Debug
      options.debug = kDebugMode;
    },
    appRunner: () => runApp(
      SentryWidget(child: MyApp()),
    ),
  );
}

// En pantallas con datos sensibles
class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          // Este campo sera enmascarado
          TextField(
            controller: emailController,
          ),
          
          // Este campo sera enmascarado
          TextField(
            controller: passwordController,
            obscureText: true,
          ),
          
          // Este texto sera enmascarado
          Text('Email: user@example.com'),
        ],
      ),
    );
  }
}
```

---

## Ver replay en Sentry

1. Ir a [sentry.io](https://sentry.io)
2. Seleccionar proyecto
3. Ir a "Replays"
4. Seleccionar una sesion
5. Ver el replay del usuario

---

## Limitaciones

| Limitacion | Descripcion |
|---|---|
| Plataforma | iOS, Android, Web |
| Tamaño | Maximo 10MB por replay |
| Duracion | Maximo 60 segundos |
| Performance | Impacto minimo en UI |

---

## Resumen

| Configuracion | Valor recomendado | Descripcion |
|---|---|---|
| sessionSampleRate | 0.1 | 10% de sesiones |
| onErrorSampleRate | 1.0 | 100% de errores |
| maskAllText | true | Enmascarar texto |
| maskAllImages | true | Enmascarar imagenes |

---

## Siguiente paso

[06 - Integraciones Jira/GitHub](./06-integraciones-jira-github.md) - Conectar Sentry con tus herramientas
