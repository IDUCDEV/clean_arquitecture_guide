# 09: Observabilidad, Monitoreo y Resiliencia

> Si no puedes medirlo, no puedes arreglarlo. Logs, métricas, tracing y alerts: el sistema debe decirte cuándo y por qué falla — y cómo recuperarse solo.

---

## Observabilidad vs Monitoreo

- **Monitoreo:** saber si un sistema está "sano" (dashboards, checks).
- **Observabilidad:** poder **preguntarle al sistema** qué está pasando ante cualquier condición, incluso las imprevistas.

La observabilidad se logra con **tres pilares**: logs, métricas y tracing.

---

## Los tres pilares

| Pilar | Qué es | Pregunta que responde |
|---|---|---|
| **Logs** | Registro de eventos discretos | *¿Qué pasó exactamente?* |
| **Métricas** | Medidas agregadas numéricas | *¿Cuánto / con qué frecuencia?* |
| **Tracing** | Recorrido de un request a través de componentes | *¿Dónde se tardó/fracturó?* |

### Logs
- Estructurados (JSON) para poder filtrarlos.
- Niveles: debug / info / warn / error.
- **Cuidado:** logs con PII o secrets = fuga de seguridad (ver archivo 08).

### Métricas (con el acrónimo USE)
- **U**tilization: % de recurso usado (CPU, memoria, conexiones de DB).
- **S**aturation: qué tan lleno está (colas, conexiones pool).
- **E**rrors: tasa de fallos, excepciones, 5xx.

### Tracing
- Un **trace** sigue un request desde la app hasta la DB pasando por Edge Functions.
- Componentes: **spans** (cada tramo), **trace id** (identificador único del request).

---

## Supabase: lo que ya tienes (sin montar infraestructura)

Supabase gestionado expone sus propios logs y métricas (dashboard + API de logs) para:

- **Postgres:** queries lentas, errores, conexiones.
- **Auth:** eventos de login/registro fallidos.
- **Realtime:** conexiones y mensajes.
- **Storage:** requests a los buckets.
- **Edge Functions:** invocaciones, errores, duración.

*Fuente: [Supabase Docs — Logging](https://supabase.com/docs/guides/telemetry/logging) y [Supabase Docs — Metrics](https://supabase.com/docs/guides/telemetry/metrics).*

**Decisión de diseño:** para el MVP usas los logs gestionados de Supabase + analytics de la app. No inventas un stack de observabilidad hasta que el tráfico/errores lo justifiquen.

---

## Analytics y métricas en Flutter (lado cliente)

En la app necesitas saber cómo se comportan **tus usuarios**:

| Herramienta | Para qué |
|---|---|
| Crash reporting | Stacktraces de errores en producción |
| Analytics de eventos | Qué feature se usa, donde se quedan los usuarios |
| Custom events | Métricas de negocio (registro completado, post publicado) |
| Screen view | Navegación y embudos |

---

## Alerting: las reglas correctas

Alertar **también es diseño**: alertas mal definidas generan ruido y desensibilizan.

### Alertas en 4 pasos
1. **Métrico correcto:** lo que importa al usuario (error rate, latencia p95), no solo del servidor.
2. **Umbral realista:** alertar antes de que sea un incidente, sin alertar por ruido.
3. **Alerta accionable:** siempre con el link al log/trace del incidente.
4. **On-call limitado:** no alertes cosas que nadie puede arreglar.

### Ejemplo para el feed del repo
```
ALERTA "Error rate en GET /api/feed > 5% durante 5 min"
LINK: Logs filtrados por status_code 5xx + trace_id
ACCIÓN: revisar Edge Function / query de feed o saturación de la DB
```

---

## Resiliencia y self-healing

El sistema debe **recuperarse solo** de fallos transitorios:

| Técnica | Qué hace | Dónde aplica |
|---|---|---|
| **Retries** | Reintenta requests fallidos | Network de la app, Edge Functions |
| **Backoff exponencial** | Cada retry espera más (evita sobrecargar al servidor caído) | Igual que retries |
| **Timeouts** | Una llamada no puede colgarse para siempre | Todos los requests de red |
| **Circuit breaker** | Tras N fallos, "abre el circuito" y falla rápido en vez de seguir pegándole al servicio | SDK de red, Edge Functions |
| **Fallbacks** | Si la fuente falla, servir otra cosa (cache, datos locales) | App con offline-first |

*Fuente: [ByteByteGo — Timeouts, Retries and Backoff](https://bytebytego.com/guides/timeouts-retries-and-backoff).*

### El patrón básico
```
request → timeout (ej. 10s)
        → falla → retry con backoff (1s, 2s, 4s...)
        → sigue fallando → circuit breaker abre → falla rápido
        → app usa fallback (cache local) → reporta métrica de error
```

---

## Diseño del plan de observabilidad (para tus casos de estudio)

Cada diseño debe responder:

1. **¿Qué mides?** Error rate, latencia, QPS, saturación de DB.
2. **¿Dónde?** App (crash + analytics) y Supabase (logs gestionados).
3. **¿Qué alertas?** Las 3-5 más importantes con umbral accionable.
4. **¿Cómo se diagnostica?** Cada error debe llevarte del dashboard → log → trace.
5. **¿Cómo se recupera?** Retries + backoff + circuit breaker + fallback offline.

---

## Errores comunes de diseño de observabilidad

| Error | Fix |
|---|---|
| Alertas por todo → ruido | Solo alertas accionables |
| Solo metrics sin logs/traces | Los 3 pilares juntos |
| Sin timeouts ni retries | Timeouts siempre; retries con backoff |
| Logs sin estructura | Logs JSON con trace_id |
| Sin fallback | Cache/offline como plan B de toda lectura |

---

## Fuentes

- [ByteByteGo — Observability (logs, metrics, tracing)](https://bytebytego.com/guides/observability-logs-metrics-tracing)
- [ByteByteGo — Timeouts, Retries and Backoff](https://bytebytego.com/guides/timeouts-retries-and-backoff)
- [Supabase Docs — Logging](https://supabase.com/docs/guides/telemetry/logging)
- [Supabase Docs — Metrics](https://supabase.com/docs/guides/telemetry/metrics)
- [Brendan Gregg — USE Method](https://www.brendangregg.com/usemethod.html)

---

**Siguiente:** [10-offline-first.md](./10-offline-first.md)
