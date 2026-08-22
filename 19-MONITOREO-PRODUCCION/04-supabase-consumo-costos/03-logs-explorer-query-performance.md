# 03 - Logs Explorer y Query Performance

> Una alerta te dice QUE metrica subio. Este archivo te ensena a encontrar QUIEN la subio: que endpoint, que query, que archivo de Storage, que function. Todo con SQL copiar-pegar sobre los logs de tu propio proyecto.

---

## Objetivos de este archivo

- Usar el Logs Explorer para investigar consumo y errores por endpoint
- Encontrar las queries lentas reales con Query Performance / pg_stat_statements
- Usar los Advisors como revision semanal automatizada
- Tener un metodo de investigacion: alerta -> hipotesis -> evidencia -> fix

---

## 1. Los dos lugares de investigacion

```
Alerta dispara (egreso al 80%, errores, lentitud)
  ├── Es un problema de TRAFICO/API?
  |     └── Logs Explorer (logs de edge/api/auth/storage/functions)
  └── Es un problema de BASE DE DATOS?
        └── Query Performance + Advisors
```

---

## 2. Logs Explorer

### Donde

```
Dashboard -> Tu proyecto -> Logs -> Explorer
```

Los logs se consultan con SQL (dialeto propio de Supabase, basado en BigQuery). Hay templates prehechos en `Logs -> Explorer -> Templates` — empieza por ahi.

### Anatomia de una query tipica

```sql
select
  timestamp,
  event_message,
  metadata
from edge_logs
where ... -- filtros
order by timestamp desc
limit 100;
```

Las tablas principales: `edge_logs` (todo lo que pasa por Kong/API), y segun el servicio hay campos anidados en `metadata` que se expanden con `unnest`.

### Queries de investigacion listas para usar

#### A. Endpoints mas solicitados (y con mas errores)

```sql
-- Top endpoints por volumen y tasa de error (ultimas 24h)
select
  request.method as metodo,
  request.path as endpoint,
  count(*) as requests,
  count(*) filter (
    where response.status_code >= 400
  ) as errores,
  round(
    100.0 * count(*) filter (where response.status_code >= 400) / count(*)
  , 1) as pct_error
from edge_logs
  cross join unnest(metadata) as metadata
  cross join unnest(metadata.request) as request
  cross join unnest(metadata.response) as response
where timestamp > now() - interval '24 hours'
group by 1, 2
order by requests desc
limit 25;
```

**Como leerlo:** un endpoint con miles de requests es tu candidato a consumidor de egresos. Un endpoint con pct_error alto es un bug o un problema de RLS/permisos.

#### B. Egresos por archivo de Storage (template oficial)

Esta es la query template oficial de Supabase para auditar trafico de Storage:

```sql
select
  request.method as http_verb,
  request.path as filepath,
  (responseHeaders.cf_cache_status = 'HIT') as cached,
  count(*) as num_requests
from edge_logs
  cross join unnest(metadata) as metadata
  cross join unnest(metadata.request) as request
  cross join unnest(metadata.response) as response
  cross join unnest(response.headers) as responseHeaders
where
  (
    path like '%storage/v1/object/%'
    or path like '%storage/v1/render/%'
  )
  and request.method = 'GET'
group by 1, 2, 3
order by num_requests desc
limit 100;
```

**Como leerlo:** multiplica `num_requests` x tamano del archivo para estimar egreso. La columna `cached` es clave: los HIT de CDN no golpean el origen igual que los MISS. Si ves un GIF de 3 MB servido 500 veces sin cache, ahi tienes ~1.5 GB de egreso en un solo archivo.

```text
Ejemplo real del output:
| filepath                    | cached | num_requests |
|-----------------------------|--------|--------------|
| /object/public/avatars/...  | false  | 168          |
| /object/sign/uploads/...gif | true   | 100          |

168 x 570KB = 95 MB sin cachear  <- aqui atacas primero
```

#### C. Invocaciones de Edge Functions

```sql
-- Volumen y errores por function
select
  request.path as function_name,
  count(*) as invocaciones,
  count(*) filter (where response.status_code >= 400) as errores,
  avg(response_time_ms)::int as latencia_promedio_ms
from edge_logs
  cross join unnest(metadata) as metadata
  cross join unnest(metadata.request) as request
  cross join unnest(metadata.response) as response
where path like '%functions/v1/%'
  and timestamp > now() - interval '24 hours'
group by 1
order by invocaciones desc;
```

Si una function acumula decenas de miles de invocaciones diarias, revisa si el cliente la llama en loop o si conviene batchear (ver playbook 04).

#### D. Errores de Auth (intentos fallidos, tokens)

```sql
select
  event_message,
  count(*) as ocurrencias
from edge_logs
where path like '%auth/v1%'
  and response_status_code >= 400
  and timestamp > now() - interval '7 days'
group by 1
order by ocurrencias desc
limit 20;
```

Patrones tipicos: refresh tokens vencidos en masa (sesiones mal manejadas), rate limiting de OTPs, credenciales invalidas repetidas (posible ataque).

### Guarda tus queries

En Logs Explorer puedes **guardar snippets** con nombre. Recomendado: guarda las queries A-D como `ops-endpoints`, `ops-storage-egress`, `ops-functions`, `ops-auth-errors`. Tu yo del futuro (a las 2 AM de un incidente) lo agradecera.

---

## 3. Query Performance

### Donde

```
Dashboard -> Tu proyecto -> Query Performance
```

Supabase instrumenta Postgres con `pg_stat_statements`: estadisticas agregadas de TODAS las queries ejecutadas. La pagina te ofrece vistas ordenadas por tiempo total, tiempo promedio y llamadas.

### Las 3 columnas que importan

| Columna | Significado | Por que importa |
|---|---|---|
| `calls` | Veces ejecutada | Muchas llamadas de una query "barata" tambien cuesta |
| `mean_exec_time` | Promedio ms por ejecucion | >100ms sostenido merece revision |
| `total_exec_time` | Tiempo acumulado | La carga REAL sobre tu instancia (y tu compute) |

### SQL equivalente (si prefieres el editor SQL)

```sql
-- Top queries por carga total (requiere pg_stat_statements activo)
SELECT
  calls,
  round(mean_exec_time::numeric, 1) AS ms_promedio,
  round(total_exec_time::numeric / 1000, 1) AS seg_totales,
  rows,
  left(query, 120) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 15;
```

### Diagnostico clasico: el seq scan

```sql
-- Tablas donde Postgres hace full scans frecuentemente
SELECT
  relname AS tabla,
  seq_scan,          -- lecturas secuenciales (sin indice)
  seq_tup_read,      -- filas leidas en esos scans
  idx_scan           -- lecturas por indice
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 10;
```

`seq_scan` alto + tabla grande + `idx_scan` bajo = te falta un indice. Solucion tipica:

```sql
CREATE INDEX idx_orders_usuario_fecha
ON orders (usuario_id, created_at DESC);
```

(Profundidad completa de indices en [03-SUPABASE/PARTE-0/03-indexes-rendimiento](../../03-SUPABASE/PARTE-0-SQL-POSTGRESQL/02-postgresql-especifico/03-indexes-rendimiento.md).)

---

## 4. Advisors: linters automaticos

```
Dashboard -> Tu proyecto -> Advisors
  ├── Security: RLS sin policies, funciones con search_path mutable, etc.
  └── Performance: indices duplicados, FKs sin indice, queries no parametrizadas
```

Ejecutalos **semanalmente**. Cada finding trae link a documentacion con el fix exacto. Un proyecto sano debe converger a 0 findings recurrentes; si uno reaparece tras cada deploy, metelo al checklist de PR.

---

## 5. Metodo de investigacion completo

Cuando una alerta dispara, sigue este protocolo:

```
1. CONFIRMA el sintoma (5 min)
   Usage page: cual metrica, cuanto, velocidad de crecimiento

2. FORMA la hipotesis
   "El egreso crecio desde el release X"
   "La tabla Y crece 50MB/dia"

3. BUSCA la evidencia
   - Trafico:      query A (endpoints) + query B (storage egress)
   - Functions:    query C (invocaciones)
   - Errores:      query A filtrando >= 400
   - DB size:      top tablas por tamano (archivo 01)
   - Lentitud:     Query Performance + seq scans

4. CUANTIFICA el impacto
   "endpoint /feed devuelve 40KB promedio x 30K req/dia = 1.2 GB/dia"

5. ATACA con el playbook correspondiente
   -> 04-optimizacion-por-metrica.md

6. VERIFICA
   Misma query 48h despues: la metrica debe bajar.
   Si no bajo, la hipotesis estaba mal -> vuelve a 3.
```

---

## Cheatsheet de investigacion

```text
Sintoma                          Primera herramienta
-------------------------------  --------------------------------------
Egresos disparados               Query B (storage) + Query A (endpoints)
App lenta reportada por usuarios Query Performance + Reports->API latencia
DB size creciendo rapido         Top tablas por tamano + autovacuum stats
Errores intermitentes            Query A con filtro >=400 + auth errors
Factura inesperada               Usage page + queries A/B/C para atribuir
Proyecto pausado                 Runbook 02 -> luego investigar causa aqui
```

---

## Siguiente paso

Sabes diagnosticar. Ahora el arsenal de soluciones: tecnicas concretas Flutter + Supabase para bajar cada metrica: [04-optimizacion-por-metrica](./04-optimizacion-por-metrica.md).
