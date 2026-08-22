# 01 - Cuotas y Dashboard

> Cada metrica que Supabase mide, como se calcula exactamente, donde verla en el dashboard y como leer tu factura. Sin entender esto, cualquier decision de costo es una apuesta.

---

## Objetivos de este archivo

- Entender las 6 metricas facturables y que cuenta exactamente cada una
- Saber donde mirar el consumo en el dashboard
- Leer tu factura mensual sin sorpresas
- Identificar cual metrica explota primero segun tu tipo de app

---

## 1. Donde ver tu consumo

### Organization -> Usage (la pagina principal)

```
Dashboard Supabase
  └── Selector de organizacion (arriba a la izquierda)
    └── Usage
      ├── Vista de TODA la organizacion (default)
      ├── Filtro por proyecto (dropdown)
      └── Filtro por periodo de tiempo
```

Esta pagina muestra **cada metrica del ciclo de facturacion actual** contra su cuota. Es tu primera parada siempre.

> La cuota aplica a **toda la organizacion**, no por proyecto. Si tienes 2 proyectos Pro en la misma org, suman contra la misma cuota.

### Reports (tendencias por dia)

```
Dashboard -> Tu proyecto -> Reports
  ├── API: requests por endpoint, errores, latencia
  ├── Database: CPU, conexiones activas, cache hit ratio
  ├── Auth: logins, usuarios
  └── Storage: trafico de buckets
```

Usage te dice CUANTO llevas gastado del ciclo. Reports te dice COMO se comporta el sistema dia a dia.

### Billing & Usage

```
Dashboard -> Organization -> Billing & Usage
  ├── Suscripcion actual y plan
  ├── Spend Cap ON/OFF
  └── Invoices (facturas historicas descargables)
```

---

## 2. Las 6 metricas, explicadas

### 2.1 Egresos (la mas peligrosa)

**Que es:** TODO byte que sale de los servidores de Supabase hacia tus clientes:

```
Egresos = filas de Postgres servidas
        + archivos descargados de Storage
        + respuestas de Edge Functions
        + payloads de Auth/Realtime
```

**Lo que NO es:** datos que SUBES (los inserts/uploads no cuentan como egreso), ni trafico entre servicios internos.

**Por que es peligrosa:** crece con (usuarios x sesiones x peso de datos). Una app con imagenes sin optimizar puede quemar 5 GB de Free con pocos cientos de usuarios.

**Como se factura:** Free incluye ~5 GB. En Pro, el egreso cacheado (CDN HIT) se trata distinto al no cacheado — verifica la tabla vigente. Excedente Pro: $0.09/GB.

**Regla mental:** cada fila que traes a la app es egreso. Traer 10,000 filas para mostrar 20 es regalar dinero.

### 2.2 Database Size

**Que es:** espacio en disco ocupado por tu base de datos: tablas, indices, TOAST (datos comprimidos), logs de WAL.

**Trampa comun:** borrar filas NO reduce inmediatamente el tamaño. Postgres marca espacio como reutilizable (autovacuum lo gestiona). El disco solo encoge tras operaciones de mantenimiento (`VACUUM FULL`, que Supabase ejecuta en ventanas programadas o bajo demanda).

**Que pasa si excedes:** en Free, al llegar a 500 MB **se bloquean las ESCRITURAS** (la app deja de poder crear cuentas, guardar, etc.). Lecturas siguen funcionando. Es un modo "read-only" que rompe tu app parcialmente.

**Como monitorearla desde SQL:**

```sql
-- Tamaño total de la base de datos
SELECT pg_size_pretty(pg_database_size(current_database()));

-- Top 15 tablas + indices por tamaño
SELECT
  relname AS objeto,
  pg_size_pretty(pg_total_relation_size(relid)) AS tamano,
  n_live_tup AS filas_estimadas
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 15;
```

Guarda esta query. Ejecutarla semanalmente te da la curva de crecimiento antes de llegar al limite.

### 2.3 MAU (Monthly Active Users)

**Definicion oficial:** usuario DISTINTO que hace login O refresca su token durante el ciclo de facturacion. Cuenta UNA vez por ciclo, use la app 1 vez o 30 veces.

```
Ciclo de facturacion: 1 al 31 de enero

Usuario A: login el 3, logout el 4, login el 17  -> 1 MAU
Usuario B: abrio la app el 5 con sesion persistente
           (su token se refresco)                -> 1 MAU
Usuario C: no abrio la app todo enero            -> 0 MAU
Total: 2 MAU
```

**Matices criticos:**

- Sesiones persistentes SIEMPRE refrescan token cuando el usuario abre la app -> cuenta MAU.
- Usuarios anonimos TAMBIEN son MAU. Si creas un `signInAnonymously` por instalacion "para probar", cada instalacion es un MAU.
- Reset total al inicio de cada ciclo.
- SSO MAU (login corporativo SAML) es una metrica separada con cuota minima.

**Como verlo desde SQL (aproximacion operativa):**

```sql
-- Usuarios con actividad reciente en auth (no es el conteo oficial
-- de facturacion, pero sirve como termometo diario)
SELECT count(*) AS usuarios_con_sesion_activa
FROM auth.sessions
WHERE updated_at > now() - interval '30 days';
```

El numero oficial de facturacion vive SOLO en Organization -> Usage.

**Referencia de escala:** 50K MAU gratis es MUCHO para una primera app. Salvo apps con login anonimo descontrolado, MAU casi nunca es tu primer cuello de botella. Egreso y DB size llegan antes.

### 2.4 Storage Size

**Que es:** suma de archivos en tus buckets. Se cobra por almacenamiento, NO por descargas (las descargas son egresos).

**Donde duele:** avatares, fotos subidas por usuarios, PDFs, videos. Un bucket de fotos de perfil con usuarios subiendo fotos de 5 MB crece rapido.

**SQL de termometo:**

```sql
SELECT sum(metadata->>'size')::bigint / 1024 / 1024 AS mb_totales
FROM storage.objects;
```

### 2.5 Edge Function Invocations

**Que es:** cada llamada HTTP a una Edge Function, exitosa o fallida.

**Trampas comunes:**

- Un loop mal hecho en Flutter llamando una function por item = invocaciones multiplicadas.
- Retries automaticos ante timeouts duplican invocaciones.
- Cron jobs que llaman functions cuentan tambien.

**Patron eficiente:** una function que procesa un batch de 100 items = 1 invocacion. Cien funciones con 1 item cada una = 100 invocaciones. Prefiere batch.

### 2.6 Realtime Messages y Peak Connections

**Messages:** cada evento entregado por canales realtime (Postgres Changes, Broadcast, Presence). Un canal con 100 clientes suscritos donde ocurre 1 cambio = ~100 mensajes entregados.

**Peak Connections:** maximo de conexiones simultaneas a realtime en el mes.

**El error clasico:** suscribirse a `postgres_changes` de una tabla entera (`*`) en cada pantalla, sin darse de baja al salir. Con 500 usuarios activos, cada INSERT dispara cientos de mensajes a quien ya no mira esa pantalla.

**Regla de oro:** subscribe al entrar a la pantalla, `unsubscribe` al salir. Siempre.

---

## 3. Tabla completa de cuotas (verificada agosto 2026)

| Metrica | Free | Pro incluido | Sobrecosto Pro |
|---|---|---|---|
| Egresos | 5 GB | 250 GB | $0.09 / GB |
| Database Size | 500 MB por proyecto | 8 GB por proyecto | $0.125 / GB |
| MAU | 50,000 | 100,000 | $0.00325 / MAU |
| Storage Size | 1 GB | 100 GB | $0.021 / GB |
| Edge Function Invocations | 500,000 | 2 millones | $2 / millon |
| Realtime Messages | 2 millones | 5 millones | $2.5 / millon |
| Realtime Peak Connections | 200 | 500 | $10 / 1000 |
| Storage Images Transformed | No disponible | 100 | $5 / 1000 |

Ademas del consumo variable pagas:
- Plan Pro: $25/mes fijo
- Compute (instancia de base de datos): desde ~$10/mes en Small
- Add-ons opcionales: Read Replicas, PITR, dominio propio, IPv4 dedicado

> Verifica siempre: [tabla oficial de billing](https://supabase.com/docs/guides/platform/billing-on-supabase). Los numeros cambian; el metodo de monitoreo de este modulo no.

---

## 4. Como leer tu factura

Una factura tipica de Pro dentro de cuota:

```
| Linea                  | Unidades      | Costo   |
|------------------------|---------------|---------|
| Pro Plan               | 1             | $25     |
| Compute Hours Small    | 730 horas     | $10     |
| Egress                 | 180 GB        | $0      |
| Monthly Active Users   | 23,000        | $0      |
| Subtotal               |               | $35     |
| Total                  |               | $35     |
```

La misma org con Spend Cap OFF y 160K MAU:

```
| Linea                  | Unidades      | Costo                    |
|------------------------|---------------|--------------------------|
| Pro Plan               | 1             | $25                      |
| Compute Hours Small    | 730 horas     | $10                      |
| Monthly Active Users   | 160,000       | $195                     |
|                        | (60K sobre    | (60,000 x $0.00325)      |
|                        |  la cuota)    |                          |
| Subtotal               |               | $230                     |
| Total                  |               | $230                     |
```

Lectura: la cuota es "incluido", no "tope". Solo el excedente genera linea de cobro (si Spend Cap lo permite).

---

## 5. Cual metrica explota primero? Depende de tu app

```
App con feed de imagenes (red social, marketplace)
  └── Egresos explota primero
    └── Monitorear: Usage egress diario + logs de storage

App de productividad offline-first (notas, tareas)
  └── DB size y egresos moderados, crecimiento lento
    └── Monitorear: db size semanal

App con chat o colaboracion en tiempo real
  └── Realtime messages y peak connections
    └── Monitorear: mensajes por canal, conexiones pico

App con IA / procesamiento pesado via Edge Functions
  └── Function invocations
    └── Monitorear: invocaciones por function en logs

App con login anonimo o trial sin friccion
  └── MAU
    └── Monitorear: auth.users growth + sessions activas
```

Identifica TU metrica critica ANTES del lanzamiento y ponle alerta (siguiente archivo).

---

## Cheatsheet: rutina de consulta

```text
DIARIO (2 min, mientras dure el crecimiento fuerte):
[ ] Organization -> Usage: barrer las 6 metricas vs cuota

SEMANAL (10 min):
[ ] Reports -> API: endpoints con mas requests y errores
[ ] Query SQL de db size (top tablas)
[ ] Advisors (security + performance): 0 issues nuevos

MENSUAL (pre-factura):
[ ] Comparar consumo proyectado vs cuota
[ ] Revisar invoice del ciclo anterior linea por linea
[ ] Actualizar proyeccion del siguiente mes
```

---

## Siguiente paso

Ya sabes medir. Ahora configura las alarmas para que Supabase te avise antes de que algo reviente: [02-alertas-y-spend-cap](./02-alertas-y-spend-cap.md).
