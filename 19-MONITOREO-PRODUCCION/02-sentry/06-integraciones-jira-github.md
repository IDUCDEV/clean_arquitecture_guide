# 06 - Integraciones Jira/GitHub

## Integraciones disponibles

Sentry ofrece integraciones bidireccionales con las herramientas mas populares:

| Herramienta | Tipo | Funcionalidad |
|---|---|---|
| Jira | Bidireccional | Crear/actualizar tickets automaticamente |
| GitHub | Bidireccional | Crear issues, linked commits |
| Slack | Notificaciones | Alertas en canales |
| PagerDuty | Notificaciones | Alertas criticas |
| Linear | Bidireccional | Crear issues |

---

## Integracion con Jira

### Configuracion

1. Ir a Sentry → Settings → Integrations
2. Buscar "Jira"
3. Clic "Install"
4. Conectar con tu cuenta de Jira
5. Seleccionar proyecto

### Crear issue automaticamente

```dart
// Configurar en Sentry Dashboard:
// Settings → Integrations → Jira → Auto-create issues

// En tu codigo, agregar contexto para Jira
await Sentry.captureException(
  error,
  stackTrace: stack,
  hint: Hint.withMap({
    'jira_project': 'MOBILE',
    'jira_issue_type': 'Bug',
    'jira_priority': 'High',
    'jira_labels': ['flutter', 'production'],
  }),
);
```

### Crear issue manualmente

```dart
// Desde Sentry Dashboard:
// 1. Ir al issue
// 2. Clic "Create Jira Issue"
// 3. Seleccionar proyecto
// 4. Llenar campos
// 5. Crear

// El issue se crea con:
// - Titulo del error
// - Stack trace
// - Reproduction steps
// - Device info
// - User info
```

### Sync bidireccional

```
Sentry Issue → Jira Issue
  └── Cuando se crea issue en Sentry
    └── Se crea issue en Jira automaticamente
      └── Con link de vuelta a Sentry

Jira Issue → Sentry Issue
  └── Cuando se actualiza issue en Jira
    └── Se actualiza estado en Sentry
      └── Cuando se cierra issue en Jira
        └── Se resuelve issue en Sentry
```

---

## Integracion con GitHub

### Configuracion

1. Ir a Sentry → Settings → Integrations
2. Buscar "GitHub"
3. Clic "Install"
4. Autorizar acceso a GitHub
5. Seleccionar repositorio

### Linked commits

```dart
// Configurar release con commits
await SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    options.release = '1.0.0';
    options.environment = 'production';
    
    // GitHub integration
    options.sendDefaultPii = false;
  },
);
```

### Crear issue automaticamente

```dart
// Configurar en Sentry Dashboard:
// Settings → Integrations → GitHub → Auto-create issues

// En tu codigo
await Sentry.captureException(
  error,
  stackTrace: stack,
  hint: Hint.withMap({
    'github_repo': 'owner/repo',
    'github_labels': ['bug', 'flutter'],
    'github_assignees': ['developer1'],
  }),
);
```

### Linked issues en commits

```yaml
# En tu commit message
fix: resolve login crash

Fixes PROJ-123
Closes #456

# Sentry automaticamente:
# 1. Vincula el commit al issue de Sentry
# 2. Cierra el issue cuando se despliega
# 3. Agrega link al commit en el issue
```

---

## Integracion con Slack

### Configuracion

1. Ir a Sentry → Settings → Integrations
2. Buscar "Slack"
3. Clic "Install"
4. Autorizar acceso a Slack
5. Seleccionar canal (#alerts)

### Configurar alertas

```dart
// Configurar en Sentry Dashboard:
// Settings → Integrations → Slack → Alert rules

// Tipos de alertas:
// - New issues
// - Regressed issues
// - Issue count above threshold
// - Crash rate above threshold
```

### Ejemplo de notificacion

```
🔥 New Issue in Sentry
├── Title: FormatException in AuthService.login
├── First seen: 2 minutes ago
├── Events: 15
├── Users affected: 12
├── Link: https://sentry.io/organizations/.../issues/...
└── Assignee: @developer1
```

---

## Integracion con PagerDuty

### Configuracion

1. Ir a Sentry → Settings → Integrations
2. Buscar "PagerDuty"
3. Clic "Install"
4. Conectar con PagerDuty
5. Seleccionar servicio

### Configurar severidad

```dart
// Configurar en Sentry Dashboard:
// Settings → Integrations → PagerDuty → Alert rules

// Mapeo de severidad:
// - fatal → Critical
// - error → Error
// - warning → Warning
// - info → Info
```

---

## Ejemplo completo: Integracion multi-herramienta

```dart
// lib/core/monitoring/sentry_service.dart
class SentryService {
  final FirebaseCrashlytics _crashlytics;

  SentryService(this._crashlytics);

  Future<void> reportError(
    dynamic error,
    StackTrace stack, {
    required String context,
    required String severity,
    Map<String, dynamic>? additionalInfo,
  }) async {
    // Reportar a Sentry
    await Sentry.captureException(
      error,
      stackTrace: stack,
      hint: Hint.withMap({
        'context': context,
        'severity': severity,
        ...?additionalInfo,
      }),
    );

    // Reportar a Crashlytics
    await _crashlytics.recordError(
      error,
      stack,
      reason: context,
      information: additionalInfo?.entries
          .map((e) => '${e.key}: ${e.value}')
          .toList(),
    );
  }

  Future<void> createJiraIssue({
    required String title,
    required String description,
    required String project,
    String? assignee,
    List<String>? labels,
  }) async {
    // Crear issue en Jira via Sentry
    await Sentry.captureMessage(
      title,
      level: SentryLevel.error,
      hint: Hint.withMap({
        'jira_project': project,
        'jira_description': description,
        'jira_assignee': assignee,
        'jira_labels': labels,
        'create_jira_issue': true,
      }),
    );
  }
}
```

---

## CODEOWNERS

Sentry puede usar CODEOWNERS para asignar issues automaticamente.

### Configurar CODEOWNERS

```
# .github/CODEOWNERS
# Archivos de auth
/lib/features/auth/ @team-auth

# Archivos de pagos
/lib/features/checkout/ @team-payments

# Archivos de productos
/lib/features/products/ @team-products
```

### Resultado en Sentry

```
Issue: FormatException in AuthService.login
├── Auto-assigned to: @team-auth
├── Based on CODEOWNERS: /lib/features/auth/
└── Notification sent to: #team-auth channel
```

---

## Ownership Routing

Sentry puede routing issues basado en el stack trace.

### Configurar

1. Ir a Sentry → Settings → Issue Owners
2. Definir reglas:
   - `path:/lib/features/auth/** -> @team-auth`
   - `path:/lib/features/checkout/** -> @team-payments`
   - `path:/lib/features/products/** -> @team-products`

### Resultado

```
Issue en /lib/features/auth/login.dart
├── Auto-assigned to: @team-auth
├── Slack notification: #team-auth
└── Jira project: AUTH
```

---

## Resumen

| Integracion | Tipo | Configuracion |
|---|---|---|
| Jira | Bidireccional | Settings → Integrations → Jira |
| GitHub | Bidireccional | Settings → Integrations → GitHub |
| Slack | Notificaciones | Settings → Integrations → Slack |
| PagerDuty | Notificaciones | Settings → Integrations → PagerDuty |

---

## Siguiente paso

[07 - Release Health](./07-release-health.md) - Comparar estabilidad entre versiones
