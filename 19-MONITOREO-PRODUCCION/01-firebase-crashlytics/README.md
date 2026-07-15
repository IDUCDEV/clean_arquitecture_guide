# Submodulo 1: Firebase Crashlytics

## Descripcion

Domina Firebase Crashlytics para monitorear crashes y errores en produccion. Aprende a configurar el SDK, reportar errores no fatales, usar custom keys y breadcrumbs, configurar alertas automatizadas y exportar datos a BigQuery para analisis avanzado.

---

## Contenido

| # | Archivo | Tema | Tiempo |
|---|---|---|---|
| 01 | [01-fundamentos-crashes.md](./01-fundamentos-crashes.md) | Que son los crashes, tipos de errores, metricas clave | 45 min |
| 02 | [02-setup-crashlytics.md](./02-setup-crashlytics.md) | Setup completo: Firebase project, SDK, error handlers | 60 min |
| 03 | [03-non-fatal-errors.md](./03-non-fatal-errors.md) | recordError, try/catch patterns, errores en BLoC | 45 min |
| 04 | [04-custom-keys-breadcrumbs.md](./04-custom-keys-breadcrumbs.md) | Custom keys, logs, user ID, breadcrumbs | 45 min |
| 05 | [05-alertas-notificaciones.md](./05-alertas-notificaciones.md) | Velocity alerts, custom alerts, integraciones | 45 min |
| 06 | [06-bigquery-analytics.md](./06-bigquery-analytics.md) | Exportacion a BigQuery, queries SQL, dashboards | 60 min |
| 07 | [07-cheatsheet-crashlytics.md](./07-cheatsheet-crashlytics.md) | Cheat sheet completo | 15 min |
| 08 | [08-practicas-crashlytics.md](./08-practicas-crashlytics.md) | 6 escenarios practicos + ejercicio integrador | 120 min |

---

## Que aprenderas

- Configurar Firebase Crashlytics para Flutter
- Distinguir entre errores fatales y no fatales
- Usar `FlutterError.onError` y `PlatformDispatcher.onError`
- Capturar errores en `runZonedGuarded`
- Aplicar custom keys y custom logs para contexto
- Configurar velocity alerts y custom alerts
- Exportar datos a BigQuery y crear queries SQL
- Crear dashboards personalizados en Firebase Console

---

## Dependencias

| Servicio/Paquete | Proposito |
|---|---|
| `firebase_core` | SDK base de Firebase |
| `firebase_crashlytics` | SDK de Crashlytics |
| `firebase_analytics` | Analytics integrado (opcional) |

---

## Verificacion de setup

```dart
// Verificar que Crashlytics esta activo
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

if (kDebugMode) {
  print('Crashlytics deshabilitado en debug');
} else {
  print('Crashlytics activo en produccion');
}

// Forzar un crash de prueba (solo en debug)
FirebaseCrashlytics.instance.crash();
```
