# Submodulo 2: Sentry

## Descripcion

Domina Sentry para monitoreo avanzado de produccion. Aprende a configurar el SDK, manejar errores con contexto, implementar performance tracing, session replay, integraciones con Jira/GitHub y release health.

---

## Contenido

| # | Archivo | Tema | Tiempo |
|---|---|---|---|
| 01 | [01-fundamentos-sentry.md](./01-fundamentos-sentry.md) | Que es Sentry, ventajas, pricing | 45 min |
| 02 | [02-setup-sentry.md](./02-setup-sentry.md) | Setup completo: SDK, configuracion, verificacion | 60 min |
| 03 | [03-error-handling-avanzado.md](./03-error-handling-avanzado.md) | captureException, withScope, tags, extras | 60 min |
| 04 | [04-performance-tracing.md](./04-performance-tracing.md) | Transactions, spans, instrumentacion | 75 min |
| 05 | [05-session-replay.md](./05-session-replay.md) | Configuracion, privacy, sampling | 45 min |
| 06 | [06-integraciones-jira-github.md](./06-integraciones-jira-github.md) | Integraciones bidireccionales | 60 min |
| 07 | [07-release-health.md](./07-release-health.md) | Crash-free sessions, adoption | 45 min |
| 08 | [08-cheatsheet-sentry.md](./08-cheatsheet-sentry.md) | Cheat sheet completo | 20 min |
| 09 | [09-practicas-sentry.md](./09-practicas-sentry.md) | 6 escenarios practicos + ejercicio integrador | 150 min |

---

## Que aprenderas

- Configurar Sentry para Flutter
- Manejar errores con contexto avanzado
- Implementar performance tracing
- Configurar session replay
- Integrar con Jira y GitHub
- Rastrear release health
- Crear dashboards personalizados

---

## Dependencias

| Paquete | Proposito |
|---|---|
| `sentry_flutter` | SDK principal de Sentry |
| `sentry_dio` | Interceptor para Dio (opcional) |

---

## Pricing

| Tier | Precio | Errores/mes | Features |
|---|---|---|---|
| Developer | Gratis | 5K | Error monitoring, Performance |
| Team | $26/user/mes | 50K | + Session replay, Feature flags |
| Business | $80/user/mes | 500K | + Advanced analytics, SLA |

---

## Verificacion de setup

```dart
// Verificar que Sentry esta activo
import 'package:sentry_flutter/sentry_flutter.dart';

final hub = Sentry.currentHub;
print('Sentry enabled: ${hub.options.dsn != null}');
print('Environment: ${hub.options.environment}');
```
