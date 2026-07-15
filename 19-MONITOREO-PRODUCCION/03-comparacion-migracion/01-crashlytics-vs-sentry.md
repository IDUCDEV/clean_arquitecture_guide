# 01 - Crashlytics vs Sentry

## Comparacion detallada

### Error Monitoring

| Feature | Crashlytics | Sentry |
|---|---|---|
| Fatal errors | Automatico | Automatico |
| Non-fatal errors | Manual (recordError) | Automatico |
| Stack traces | Basico | Detallado |
| Breadcrumbs | Basico | Avanzado |
| Custom keys | Si | Si |
| Custom logs | Si | Si |
| User context | Si | Si |
| Device info | Si | Si |
| App info | Si | Si |
| grouping | Basico | Avanzado |
| Deduplicacion | Automatica | Automatica |

### Performance

| Feature | Crashlytics | Sentry |
|---|---|---|
| Performance tracing | No nativo | Si |
| Transactions | No | Si |
| Spans | No | Si |
| HTTP monitoring | No | Si |
| Cold start detection | No | Si |
| Profiling | No | Si (iOS/macOS) |
| Memory profiling | No | Si |
| CPU profiling | No | Si |

### Session Replay

| Feature | Crashlytics | Sentry |
|---|---|---|
| Session replay | No | Si |
| Privacy controls | No | Si |
| Network recording | No | Si |
| Screenshot on error | No | Si |

### Integraciones

| Feature | Crashlytics | Sentry |
|---|---|---|
| Jira | Unidireccional | Bidireccional |
| GitHub | No nativa | Bidireccional |
| Slack | Si | Si |
| PagerDuty | Si | Si |
| Linear | No | Si |
| Discord | No | Si |
| Teams | No | Si |

### Release Health

| Feature | Crashlytics | Sentry |
|---|---|---|
| Crash-free sessions | Basico | Avanzado |
| Crash-free users | Basico | Avanzado |
| Adoption | Basico | Avanzado |
| Regression detection | No | Si |
| Auto-resolve | No | Si |

### Feature Flags

| Feature | Crashlytics | Sentry |
|---|---|---|
| Feature flags | No | Si |
| A/B testing | No | Si |
| Flag tracking | No | Si |

### User Feedback

| Feature | Crashlytics | Sentry |
|---|---|---|
| User feedback | No | Si |
| Feedback widget | No | Si |
| Feedback context | No | Si |

### Precio

| Feature | Crashlytics | Sentry |
|---|---|---|
| Precio base | Gratis | Gratis |
| Errores/mes | Ilimitado | 5K (gratis) |
| Transacciones/mes | N/A | 10K (gratis) |
| Almacenamiento | Gratis | 1 GB (gratis) |
| Retencion | 90 dias | 30 dias (gratis) |
| Precio Team | N/A | $26/user/mes |
| Precio Business | N/A | $80/user/mes |

### Analisis

| Feature | Crashlytics | Sentry |
|---|---|---|
| Dashboard basico | Si | Si |
| Dashboards custom | No | Si |
| Export SQL | BigQuery (gratis) | No nativo |
| Export Data Studio | Si | No |
| API REST | Si | Si |
| Webhooks | Si | Si |

### Configuracion

| Feature | Crashlytics | Sentry |
|---|---|---|
| Setup basico | Facil | Facil |
| Setup avanzado | Medio | Medio |
| Debug symbols | Automatico | Manual |
| ProGuard | Automatico | Manual |
| dSYM upload | Automatico | Manual |

---

## Pros y contras

### Firebase Crashlytics

**Pros:**
- Gratis y sin limite de errores
- Integracion nativa con Firebase
- Export a BigQuery gratis
- Setup automatico de debug symbols
- Integracion con Firebase Analytics

**Contras:**
- Sin performance tracing
- Sin session replay
- Integraciones limitadas
- Release health basico
- Sin feature flags

### Sentry

**Pros:**
- Performance tracing avanzado
- Session replay
- Integraciones bidireccionales
- Release health avanzado
- Feature flags
- User feedback

**Contras:**
- Precio elevado a escala
- Debug symbols manuales
- Configuracion mas compleja
- Limite de errores en tier gratis

---

## Casos de uso

### Usa Crashlytics si:

- Presupuesto limitado
- No necesitas performance tracing
- No necesitas session replay
- Quieres integracion con Firebase
- Quieres export a BigQuery
- App basica sin necesidades avanzadas

### Usa Sentry si:

- Necesitas performance tracing
- Necesitas session replay
- Necesitas integraciones Jira/GitHub
- Necesitas release health avanzado
- Necesitas feature flags
- App compleja con muchas features
- Equipo grande que necesita colaboracion

### Combina ambas si:

- Quieres lo mejor de ambos mundos
- Presupuesto permite ambas
- Necesitas features de ambas
- Quieres redundancia

---

## Siguiente paso

[02 - Combinar Herramientas](./02-combinar-herramientas.md) - Como usar ambas juntas
