# 05 - Alertas y Notificaciones

## Tipos de alertas

Firebase Crashlytics ofrece tres tipos principales de alertas:

1. **Velocity Alerts** - Detectan spikes de crashes
2. **Issue Alerts** - Alertan por nuevos issues
3. **Crash Rate Alerts** - Alertan cuando el crash-free rate baja

---

## Velocity Alerts

Detectan cuando un crash afecta a muchos usuarios en poco tiempo.

### Configurar Velocity Alert

1. Ir a Firebase Console → Crashlytics → Alerts
2. Clic "Add alert"
3. Seleccionar "Velocity"
4. Configurar:
   - **Issue**: Seleccionar el issue especifico
   - **Threshold**: Numero de usuarios afectados
   - **Time window**: Ventana de tiempo (1h, 6h, 24h)
   - **Notifications**: Email, Slack, PagerDuty

### Ejemplo de configuracion

```
Alerta: Login crash spike
├── Issue: FormatException in AuthService.login
├── Threshold: 100 usuarios
├── Time window: 1 hora
├── Notifications:
│   ├── Email: team@company.com
│   ├── Slack: #alerts-production
│   └── PagerDuty: on-call
└── Auto-resolve: Si el rate baja
```

### Programaticamente (no disponible directamente, pero se puede simular)

```dart
class CrashMonitor {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;
  final int _threshold = 100;
  final Duration _window = Duration(hours: 1);
  
  DateTime? _lastCheck;
  int _errorCount = 0;

  void recordError(dynamic error, StackTrace stack, {String? reason}) {
    _crashlytics.recordError(error, stack, reason: reason);
    
    _errorCount++;
    _checkThreshold();
  }

  void _checkThreshold() {
    final now = DateTime.now();
    
    if (_lastCheck == null || now.difference(_lastCheck!) > _window) {
      _errorCount = 0;
      _lastCheck = now;
    }
    
    if (_errorCount >= _threshold) {
      _sendAlert();
      _errorCount = 0;
    }
  }

  void _sendAlert() {
    // Enviar alerta personalizada
    print('ALERT: Error threshold reached!');
    // Integrar con tu sistema de alertas
  }
}
```

---

## Issue Alerts

Alertan cuando aparece un **nuevo issue** o un issue existente tiene muchas ocurrencias.

### Configurar Issue Alert

1. Firebase Console → Crashlytics → Alerts
2. "Add alert" → "Issue"
3. Configurar:
   - **New issues**: Alertar por issues nuevos
   - **Regressed issues**: Alertar por issues que reaparecen
   - **Top issues**: Alertar por los mas frecuentes
   - **Notifications**: Email, Slack, PagerDuty

### Tipos de issue alerts

| Tipo | Cuando alerta |
|---|---|
| New issue | Un crash nuevo aparece |
| Regressed issue | Un crash que estaba arreglado vuelve |
| Top issue | Un crash esta en el top N |
| Issue count | Un crash tiene N+ ocurrencias |

---

## Crash Rate Alerts

Alertan cuando el **crash-free rate** baja de un umbral.

### Configurar Crash Rate Alert

1. Firebase Console → Crashlytics → Alerts
2. "Add alert" → "Crash rate"
3. Configurar:
   - **Threshold**: Porcentaje minimo de crash-free (ej: 98%)
   - **Comparison**: Comparar con version anterior
   - **Notifications**: Email, Slack, PagerDuty

### Ejemplo

```
Alerta: Crash rate increase
├── Metric: Crash-free sessions
├── Threshold: < 98%
├── Comparison: vs previous version
├── Time window: 24 horas
└── Notifications:
    ├── Email: team@company.com
    └── Slack: #alerts-production
```

---

## Integraciones de notificaciones

### Email

1. Firebase Console → Crashlytics → Alerts
2. Seleccionar "Email"
3. Agregar destinatarios
4. Configurar frecuencia (instant, hourly, daily)

### Slack

1. Firebase Console → Integrations → Slack
2. Conectar workspace de Slack
3. Seleccionar canal (#alerts-production)
4. Configurar filtros (solo issues criticos)

### PagerDuty

1. Firebase Console → Integrations → PagerDuty
2. Conectar PagerDuty
3. Seleccionar servicio
4. Configurar severidad

### Jira

```dart
// Configurar integracion con Jira
// (requiere configuracion en Firebase Console)

class CrashlyticsIntegration {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  Future<void> reportToJira(dynamic error, StackTrace stack) async {
    // Crashlytics puede crear tickets automaticamente
    // Configurar en Firebase Console → Integrations → Jira
    
    await _crashlytics.recordError(
      error,
      stack,
      reason: 'Auto-reported to Jira',
    );
  }
}
```

---

## Alertas personalizadas

### Patron 1: Alerta por contexto

```dart
class AlertService {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  Future<void> reportCriticalError(
    dynamic error,
    StackTrace stack, {
    required String context,
    required String severity,
  }) async {
    // Agregar contexto al error
    await _crashlytics.recordError(
      error,
      stack,
      reason: 'Critical error: $context',
    );

    // Configurar custom keys para alertas
    await _crashlytics.setCustomKey('alert_severity', severity);
    await _crashlytics.setCustomKey('alert_context', context);
    
    // Enviar notificacion adicional si es critico
    if (severity == 'critical') {
      _sendCriticalNotification(context, error);
    }
  }

  void _sendCriticalNotification(String context, dynamic error) {
    // Integrar con tu sistema de notificaciones
    // Ejemplo: Firebase Cloud Messaging
    print('CRITICAL ALERT: $context - $error');
  }
}
```

### Patron 2: Alerta por usuario

```dart
class UserAlertService {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;
  final Set<String> _affectedUsers = {};

  Future<void> reportError(
    dynamic error,
    StackTrace stack, {
    required String userId,
  }) async {
    await _crashlytics.recordError(
      error,
      stack,
      reason: 'Error affecting user $userId',
    );

    _affectedUsers.add(userId);
    
    // Alertar si muchos usuarios afectados
    if (_affectedUsers.length >= 10) {
      _sendBulkAlert();
    }
  }

  void _sendBulkAlert() {
    print('BULK ALERT: ${_affectedUsers.length} users affected!');
    _affectedUsers.clear();
  }
}
```

---

## Dashboard de monitoreo

### Metricas clave

```dart
class CrashDashboard {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  void logDashboardMetrics({
    required int totalSessions,
    required int crashFreeSessions,
    required int topIssueCount,
  }) async {
    await _crashlytics.setCustomKey('total_sessions', totalSessions);
    await _crashlytics.setCustomKey('crash_free_sessions', crashFreeSessions);
    await _crashlytics.setCustomKey('crash_free_rate', 
      (crashFreeSessions / totalSessions * 100).toStringAsFixed(2));
    await _crashlytics.setCustomKey('top_issue_count', topIssueCount);
  }
}
```

### Reporte diario

```dart
class DailyReport {
  final FirebaseCrashlytics _crashlytics = FirebaseCrashlytics.instance;

  Future<void> sendDailyReport() async {
    final stats = await _getCrashStats();
    
    await _crashlytics.setCustomKey('daily_crashes', stats.crashes);
    await _crashlytics.setCustomKey('daily_sessions', stats.sessions);
    await _crashlytics.setCustomKey('daily_crash_rate', 
      stats.crashRate.toStringAsFixed(2));
    
    _crashlytics.log('Daily report sent: ${stats.toJson()}');
  }
}
```

---

## Resumen

| Tipo de Alerta | Cuándo usar | Umbral comun |
|---|---|---|
| Velocity | Crash afecta muchos usuarios rapido | 100 usuarios/hora |
| Issue | Nuevo issue o regresion | 1+ ocurrencias |
| Crash Rate | Crash-free rate baja | < 98% |

---

## Siguiente paso

[06 - BigQuery y Analytics](./06-bigquery-analytics.md) - Exportar y analizar datos de crashes
