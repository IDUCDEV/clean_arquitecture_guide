# 06 - BigQuery y Analytics

## Que es BigQuery?

BigQuery es un servicio de analisis de datos de Google que permite ejecutar **queries SQL** sobre grandes volumenes de datos. Firebase Crashlytics exporta automaticamente todos los datos de crashes a BigQuery.

---

## Por que usar BigQuery?

| Ventaja | Descripcion |
|---|---|
| SQL queries | Analizar datos con queries potentes |
| Custom dashboards | Crear dashboards personalizados |
| Exportacion | Exportar a otras herramientas |
| Costo | Gratis hasta 1TB de queries/mes |
| Historico | Conservar datos indefinidamente |

---

## Paso 1: Habilitar exportacion

1. Ir a Firebase Console → Crashlytics
2. Clic "Integrations"
3. Seleccionar "BigQuery"
4. Clic "Enable"
5. Seleccionar ubicacion (us-central1 recomendado)

---

## Paso 2: Entender el esquema

### Tabla principal: `firebase_crashlytics.firebase_crashlytics`

```
firebase_crashlytics.firebase_crashlytics
├── event_id (STRING) - ID unico del crash
├── issue_id (STRING) - ID del issue agrupado
├── issue_title (STRING) - Titulo del issue
├── timestamp (TIMESTAMP) - Cuando ocurrio
├── device (RECORD) - Info del dispositivo
│   ├── brand (STRING)
│   ├── model (STRING)
│   ├── manufacturer (STRING)
│   └── ...
├── app (RECORD) - Info de la app
│   ├── display_version (STRING)
│   ├── build_identifier (STRING)
│   └── ...
├── log (RECORD) - Logs del crash
│   └── contents (STRING)
├── exception (RECORD) - Exception info
│   ├── exception_type (STRING)
│   └── exception (STRING)
├── binary_images (RECORD) - Info de simbolos
│   └── ...
└── ...
```

---

## Paso 3: Queries basicas

### Top 10 crashes por ocurrencias

```sql
SELECT
  issue_id,
  issue_title,
  COUNT(*) as crash_count,
  COUNT(DISTINCT user.id) as affected_users
FROM
  `firebase_crashlytics.firebase_crashlytics`
WHERE
  DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY
  issue_id, issue_title
ORDER BY
  crash_count DESC
LIMIT 10;
```

### Crashes por version

```sql
SELECT
  app.display_version as version,
  COUNT(*) as crash_count,
  COUNT(DISTINCT user.id) as affected_users,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM
  `firebase_crashlytics.firebase_crashlytics`
WHERE
  DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY
  app.display_version
ORDER BY
  crash_count DESC;
```

### Crashes por dispositivo

```sql
SELECT
  device.brand,
  device.model,
  COUNT(*) as crash_count
FROM
  `firebase_crashlytics.firebase_crashlytics`
WHERE
  DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
GROUP BY
  device.brand, device.model
ORDER BY
  crash_count DESC
LIMIT 10;
```

---

## Paso 4: Queries avanzadas

### Crash-free rate por dia

```sql
WITH daily_crashes AS (
  SELECT
    DATE(timestamp) as date,
    COUNT(DISTINCT event_id) as crashes,
    COUNT(DISTINCT user.id) as total_users
  FROM
    `firebase_crashlytics.firebase_crashlytics`
  WHERE
    DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY
    date
),
daily_sessions AS (
  SELECT
    DATE(timestamp) as date,
    COUNT(DISTINCT session.id) as total_sessions
  FROM
    `firebase_analytics.events_*`
  WHERE
    _TABLE_SUFFIX >= FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY))
  GROUP BY
    date
)
SELECT
  dc.date,
  dc.crashes,
  ds.total_sessions,
  ROUND((1 - dc.crashes / ds.total_sessions) * 100, 2) as crash_free_rate
FROM
  daily_crashes dc
JOIN
  daily_sessions ds ON dc.date = ds.date
ORDER BY
  dc.date DESC;
```

### Top issues por version

```sql
SELECT
  issue_id,
  issue_title,
  app.display_version,
  COUNT(*) as crash_count,
  COUNT(DISTINCT user.id) as affected_users
FROM
  `firebase_crashlytics.firebase_crashlytics`
WHERE
  DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  AND app.display_version IN ('1.0.0', '1.0.1', '1.0.2')
GROUP BY
  issue_id, issue_title, app.display_version
HAVING
  crash_count > 10
ORDER BY
  crash_count DESC;
```

### Analisis de regresiones

```sql
WITH current_week AS (
  SELECT
    issue_id,
    COUNT(*) as current_count
  FROM
    `firebase_crashlytics.firebase_crashlytics`
  WHERE
    DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  GROUP BY
    issue_id
),
previous_week AS (
  SELECT
    issue_id,
    COUNT(*) as previous_count
  FROM
    `firebase_crashlytics.firebase_crashlytics`
  WHERE
    DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
    AND DATE(timestamp) < DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  GROUP BY
    issue_id
)
SELECT
  cw.issue_id,
  cw.current_count,
  pw.previous_count,
  cw.current_count - pw.previous_count as increase,
  ROUND((cw.current_count - pw.previous_count) / pw.previous_count * 100, 2) as increase_percentage
FROM
  current_week cw
LEFT JOIN
  previous_week pw ON cw.issue_id = pw.issue_id
WHERE
  cw.current_count > pw.previous_count
  AND cw.current_count > 10
ORDER BY
  increase_percentage DESC;
```

---

## Paso 5: Custom Dashboards

### Crear dashboard en Looker Studio

1. Ir a [Looker Studio](https://lookerstudio.google.com/)
2. Crear nuevo report
3. Conectar BigQuery
4. Seleccionar tabla `firebase_crashlytics`
5. Crear visualizaciones

### Metricas para el dashboard

```
Dashboard de Crashlytics
├── Crash-free rate (line chart)
├── Top 10 issues (bar chart)
├── Crashes by version (pie chart)
├── Crashes by device (table)
├── Timeline of crashes (line chart)
└── New issues (counter)
```

---

## Paso 6: Exportacion a otras herramientas

### Exportar a Data Studio

```sql
-- Query para Data Studio
SELECT
  DATE(timestamp) as date,
  issue_title,
  COUNT(*) as count,
  device.brand,
  app.display_version
FROM
  `firebase_crashlytics.firebase_crashlytics`
WHERE
  DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY
  date, issue_title, device.brand, app.display_version
```

### Exportar a Sheets

1. En BigQuery Console, ejecutar query
2. Clic "Export" → "Export to Google Sheets"
3. Seleccionar destino
4. Abrir en Sheets

---

## Paso 7: Automatizar reports

### Cloud Function para reporte diario

```javascript
// functions/index.js
const functions = require('firebase-functions');
const admin = require('firebase-admin');

exports.dailyCrashReport = functions.pubsub
  .schedule('every 24 hours')
  .onRun(async (context) => {
    const bigquery = admin.bigquery();
    
    const query = `
      SELECT
        COUNT(*) as total_crashes,
        COUNT(DISTINCT user.id) as affected_users
      FROM
        \`firebase_crashlytics.firebase_crashlytics\`
      WHERE
        DATE(timestamp) = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
    `;
    
    const [rows] = await bigquery.query({
      query: query,
      location: 'us-central1',
    });
    
    const report = rows[0];
    
    // Enviar email con reporte
    await sendEmail({
      to: 'team@company.com',
      subject: 'Daily Crash Report',
      body: `
        Total crashes: ${report.total_crashes}
        Affected users: ${report.affected_users}
      `,
    });
    
    return null;
  });
```

---

## Resumen

| Herramienta | Uso | Costo |
|---|---|---|
| BigQuery | SQL queries | Gratis hasta 1TB/mes |
| Looker Studio | Dashboards | Gratis |
| Cloud Functions | Automatizar reports | Gratis tier |
| Sheets | Exportar datos | Gratis |

---

## Siguiente paso

[07 - Cheatsheet Crashlytics](./07-cheatsheet-crashlytics.md) - Referencia rapida
