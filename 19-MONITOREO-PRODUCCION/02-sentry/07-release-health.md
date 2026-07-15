# 07 - Release Health

## Que es Release Health?

Release health monitorea la **estabilidad de tu app** entre versiones. Permite comparar crash-free rates, errores por sesion, y adopcion de versiones.

---

## Metricas clave

### Crash-free Sessions

El porcentaje de sesiones que no tuvieron crashes.

```
Sesiones totales: 10,000
Sesiones con crash: 150
Crash-free rate: 98.5%
```

### Crash-free Users

El porcentaje de usuarios unicos que no experimentaron crashes.

```
Usuarios totales: 5,000
Usuarios con crash: 100
Crash-free users: 98%
```

### Adoption

El porcentaje de usuarios que actualizaron a la nueva version.

```
Usuarios totales: 10,000
Usuarios en v1.2.0: 8,000
Adoption: 80%
```

---

## Configurar Release Health

```dart
// lib/main.dart
import 'package:flutter/foundation.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await SentryFlutter.init(
    (options) {
      options.dsn = 'your-dsn';
      
      // Release info
      options.release = '1.0.0';
      options.environment = 'production';
      
      // Performance
      options.tracesSampleRate = 1.0;
    },
    appRunner: () => runApp(MyApp()),
  );

  // Configurar release info
  await Sentry.configureScope((scope) {
    scope.setTag('release', '1.0.0');
    scope.setTag('environment', 'production');
  });
}
```

---

## Verificar en Sentry Dashboard

1. Ir a Sentry → Releases
2. Ver releases recientes
3. Seleccionar un release
4. Ver metricas:
   - Crash-free sessions
   - Crash-free users
   - New issues
   - Regressed issues

---

## Comparar versiones

### En Dashboard

1. Ir a Sentry → Releases
2. Seleccionar dos versiones
3. Clic "Compare"
4. Ver diferencias:
   - Crash rate
   - Error count
   - Performance

### Con Codigo

```dart
// Comparar releases en tu codigo
class ReleaseComparator {
  final SentryApi _api;

  ReleaseComparator(this._api);

  Future<Map<String, dynamic>> compareReleases(
    String release1,
    String release2,
  ) async {
    final metrics1 = await _api.getReleaseMetrics(release1);
    final metrics2 = await _api.getReleaseMetrics(release2);

    return {
      'release1': {
        'crash_free_rate': metrics1.crashFreeRate,
        'error_count': metrics1.errorCount,
      },
      'release2': {
        'crash_free_rate': metrics2.crashFreeRate,
        'error_count': metrics2.errorCount,
      },
      'diff': {
        'crash_free_rate': metrics2.crashFreeRate - metrics1.crashFreeRate,
        'error_count': metrics2.errorCount - metrics1.errorCount,
      },
    };
  }
}
```

---

## Auto-resolve issues

Sentry puede resolver issues automaticamente cuando se despliega una nueva version sin el error.

### Configurar

1. Ir a Sentry → Settings → General Settings
2. Habilitar "Auto-resolve issues"
3. Configurar:
   - Resolve when: New release
   - Or: After X days without events

### Resultado

```
Issue: FormatException in AuthService.login
├── Status: Resolved
├── Resolved in: 1.2.0
├── Last seen: 1.1.0
└── Auto-resolved: Yes
```

---

## Health check

```dart
// lib/core/monitoring/health_check.dart
class HealthCheck {
  final SentryApi _api;

  HealthCheck(this._api);

  Future<HealthStatus> check(String release) async {
    try {
      final metrics = await _api.getReleaseMetrics(release);
      
      if (metrics.crashFreeRate < 95) {
        return HealthStatus.critical(
          'Crash-free rate below 95%: ${metrics.crashFreeRate}%',
        );
      }
      
      if (metrics.crashFreeRate < 98) {
        return HealthStatus.warning(
          'Crash-free rate below 98%: ${metrics.crashFreeRate}%',
        );
      }
      
      return HealthStatus.healthy(
        'Crash-free rate: ${metrics.crashFreeRate}%',
      );
    } catch (e) {
      return HealthStatus.unknown('Unable to check health');
    }
  }
}
```

---

## Resumen

| Metrica | Meta | Descripcion |
|---|---|---|
| Crash-free sessions | > 98% | Sesiones sin crashes |
| Crash-free users | > 98% | Usuarios sin crashes |
| Adoption | > 80% | Usuarios en ultima version |
| Regressed issues | 0 | Issues que reaparecen |

---

## Siguiente paso

[08 - Cheatsheet Sentry](./08-cheatsheet-sentry.md) - Referencia rapida
