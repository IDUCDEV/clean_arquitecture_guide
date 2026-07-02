# 03 - Configuración de Producción

> Aprende a configurar Supabase para producción: seguridad, rendimiento, monitoreo, rate limiting y más.

---

## 🎯 Objetivos de este archivo

- Configurar variables de producción con secrets management
- Implementar connection pooling con PgBouncer
- Rate limiting y seguridad a nivel Kong/Nginx
- SSL/TLS con auto-renewal
- Monitoreo con Prometheus + Grafana
- Optimización de base de datos (autovacuum, índices)
- Hardening de seguridad (RLS, SQL injection)

---

## 1. Variables de entorno de producción

```bash
# ==============================================================================
# GENERAR NUEVAS CLAVES PARA PRODUCCIÓN (NUNCA reusar las de desarrollo)
# ==============================================================================

# JWT Secret (crítico - afecta todos los tokens)
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# API keys formato publishable/secret
PUBLISHABLE_KEY=$(python3 -c "import secrets; print('sb_publishable_' + secrets.token_urlsafe(32))")
SECRET_KEY=$(python3 -c "import secrets; print('sb_secret_' + secrets.token_urlsafe(48))")

# Postgres
POSTGRES_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# URLs
SITE_URL=https://tu-dominio.com
ADDITIONAL_REDIRECT_URLS=
API_EXTERNAL_URL=https://tu-dominio.com

# SMTP
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=tu-password
SMTP_SENDER_NAME=Mi App
```

### Gestión de secrets (producción)

**Nunca** pongas claves reales en archivos .env dentro del repositorio. Usa uno de estos métodos:

| Método | Cómo funciona | Cuándo usarlo |
|--------|--------------|---------------|
| **Docker secrets** | Archivos montados en `/run/secrets/` | Self-hosted con Docker Swarm |
| **Vault (Hashicorp)** | API de secrets con rotación automática | Equipos grandes, compliance |
| **SOPS (Mozilla)** | Archivos cifrados con age/pgp en el repo | GitOps, CI/CD |
| **1Password CLI** | `op inject` en scripts CI/CD | Equipos pequeños/medianos |
| **GitHub Secrets** | CI/CD env vars cifradas | Solo para GitHub Actions |

Ejemplo con Docker secrets:

```yaml
# docker-compose.yml
services:
  db:
    image: supabase/postgres:15.6.1.147
    secrets:
      - postgres_password

secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt
```

---

## 2. Connection Pooling (PgBouncer)

PgBouncer es obligatorio en producción. Sin él, cada conexión crea un proceso PostgreSQL independiente (hasta 500MB c/u).

### Arquitectura

```
Cliente ──► Kong ──► PostgREST ──► PgBouncer ──► PostgreSQL
App ──────► Gotrue ──► PgBouncer ──► PostgreSQL
```

### Configuración recomendada

```ini
# pgbouncer.ini
[databases]
postgres = host=db port=5432 dbname=postgres

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = scram-sha-256
auth_file = /etc/pgbouncer/userlist.txt

# Pool settings
pool_mode = transaction
default_pool_size = 40
max_client_conn = 200
max_db_connections = 80

# Timeouts
server_idle_timeout = 300
client_idle_timeout = 600
query_timeout = 30

# Logging
log_connections = 0
log_disconnections = 0
stats_period = 60
verbose = 0
```

### Cálculo del pool size

| Servicio | Conexiones estimadas |
|----------|---------------------|
| PostgREST (10 workers × 2) | 20 |
| GoTrue (5 workers × 2) | 10 |
| Realtime (slots replicación) | 3 |
| Studio / Admin | 2 |
| **Total base** | **35** |
| Margen de seguridad (20%) | 7 |
| **Pool size recomendado** | **40-50** |

### Monitoreo de pools

```sql
-- Consultas útiles desde psql a PgBouncer
SHOW POOLS;      -- pools activos por database
SHOW STATS;      -- estadísticas de queries
SHOW CLIENTS;    -- clientes conectados
SHOW SERVERS;    -- conexiones a PostgreSQL
SHOW DATABASES;  -- bases de datos configuradas
```

---

## 3. Rate Limiting

Protege tu API contra abusos. Implementalo en dos capas:

### Capa 1: Kong (API Gateway)

```yaml
# kong.yml (agregar a cada service)
plugins:
  - name: rate-limiting
    config:
      minute: 60          # 60 requests/minuto
      hour: 2000          # 2000 requests/hora
      policy: local       # o "redis" si tienes múltiples Kong
      fault_tolerant: true
      hide_client_headers: false
```

Límites recomendados por servicio:

| Servicio | Límite | Razonamiento |
|----------|--------|-------------|
| REST API | 60 req/min, 2000/hora | Operaciones CRUD normales |
| Auth (login) | 10 req/min | Prevenir brute force |
| Auth (signup) | 5 req/min | Prevenir registros masivos |
| Auth (magic link) | 3 req/min | Costo de email |
| Storage (upload) | 10 req/min | Ancho de banda |
| Storage (download) | 30 req/min | Uso normal de archivos |

### Capa 2: Nginx (antes de Kong)

```nginx
# /etc/nginx/conf.d/rate-limit.conf

# Zona compartida para rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/s;
limit_req_zone $http_apikey zone=by_key:10m rate=100r/s;

server {
    # Rate limit global por IP
    location /rest/v1/ {
        limit_req zone=api burst=50 nodelay;
        proxy_pass http://kong_backend;
    }

    location /auth/v1/ {
        limit_req zone=auth burst=10 nodelay;
        proxy_pass http://kong_backend;
    }
}
```

### Rate limiting por usuario (PostgREST)

```sql
-- Crear tabla para tracking
CREATE TABLE IF NOT EXISTS rate_limits (
    user_id UUID REFERENCES auth.users(id),
    endpoint TEXT NOT NULL,
    window_start TIMESTAMPTZ NOT NULL DEFAULT now(),
    request_count INT NOT NULL DEFAULT 1,
    PRIMARY KEY (user_id, endpoint, window_start)
);

-- Función RLS-safe para checkear límites
CREATE OR REPLACE FUNCTION public.check_rate_limit(
    p_endpoint TEXT,
    p_max_requests INT DEFAULT 60,
    p_window_minutes INT DEFAULT 1
) RETURNS BOOLEAN LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE
    v_user_id UUID := auth.uid();
    v_count INT;
BEGIN
    IF v_user_id IS NULL THEN
        RETURN false;
    END IF;
    
    DELETE FROM rate_limits 
    WHERE window_start < now() - (p_window_minutes || ' minutes')::INTERVAL;
    
    INSERT INTO rate_limits (user_id, endpoint)
    VALUES (v_user_id, p_endpoint)
    ON CONFLICT (user_id, endpoint, window_start)
    DO UPDATE SET request_count = rate_limits.request_count + 1;
    
    SELECT request_count INTO v_count
    FROM rate_limits
    WHERE user_id = v_user_id 
      AND endpoint = p_endpoint
      AND window_start >= now() - (p_window_minutes || ' minutes')::INTERVAL;
    
    RETURN v_count <= p_max_requests;
END;
$$;
```

---

## 4. SSL/TLS

### Certificado Let's Encrypt con auto-renewal

```bash
# Instalar certbot
apt install -y certbot python3-certbot-nginx

# Obtener certificado
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com \
  --non-interactive \
  --agree-tos \
  -m admin@tu-dominio.com

# Verificar auto-renewal
systemctl status certbot.timer
certbot renew --dry-run
```

### Configuración SSL óptima

```nginx
server {
    listen 443 ssl http2;
    server_name tu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;

    # Versiones TLS
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 1.1.1.1 8.8.8.8 valid=300s;
    resolver_timeout 5s;

    # HSTS (HTTP Strict Transport Security)
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
}
```

### Verificar configuración SSL

```bash
# Test SSL con curl
curl -sI https://tu-dominio.com

# Test con openssl
openssl s_client -connect tu-dominio.com:443 -servername tu-dominio.com 2>/dev/null | openssl x509 -noout -dates

# Análisis completo
# https://www.ssllabs.com/ssltest/
```

---

## 5. Monitoreo con Prometheus + Grafana

### Stack recomendado

```yaml
# Agregar al docker-compose.yml

  # ────────────────────────────────────────────────────────────────────────────
  # Prometheus - Métricas
  # ────────────────────────────────────────────────────────────────────────────
  prometheus:
    image: prom/prometheus:v2.53.0
    container_name: supabase-prometheus
    restart: unless-stopped
    volumes:
      - ./volumes/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.retention.time=30d"
    logging: *default-logging

  # ────────────────────────────────────────────────────────────────────────────
  # Grafana - Dashboards
  # ────────────────────────────────────────────────────────────────────────────
  grafana:
    image: grafana/grafana:11.0.0
    container_name: supabase-grafana
    restart: unless-stopped
    ports:
      - "3001:3000"
    volumes:
      - ./volumes/grafana/dashboards:/var/lib/grafana/dashboards:ro
      - grafana-data:/var/lib/grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:-admin}
      GF_INSTALL_PLUGINS: grafana-piechart-panel
    depends_on:
      - prometheus
    logging: *default-logging

  # ────────────────────────────────────────────────────────────────────────────
  # PostgreSQL Exporter
  # ────────────────────────────────────────────────────────────────────────────
  postgres-exporter:
    image: prometheuscommunity/postgres-exporter:v0.15.0
    container_name: supabase-pgexporter
    restart: unless-stopped
    environment:
      DATA_SOURCE_NAME: "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@pgbouncer:6432/${POSTGRES_DB}?sslmode=disable"
      PG_EXPORTER_AUTO_DISCOVER_DATABASES: "true"
    depends_on:
      - pgbouncer
    logging: *default-logging

volumes:
  prometheus-data:
  grafana-data:
```

### Prometheus config

```yaml
# volumes/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
  
  - job_name: 'kong'
    static_configs:
      - targets: ['kong:8001']
  
  - job_name: 'gotrue'
    static_configs:
      - targets: ['gotrue:9999']
  
  - job_name: 'realtime'
    static_configs:
      - targets: ['realtime:4000']
  
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

### Qué monitorear

| Métrica | Qué indica | Alerta si |
|---------|-----------|-----------|
| `pg_stat_activity.count` | Conexiones activas | > 80% del pool |
| `pg_stat_database.xact_commit` | Transacciones commiteadas | Caída repentina |
| `pg_stat_database.deadlocks` | Deadlocks | > 0 en 5 min |
| `pg_replication_lag` | Lag de replicación | > 10 segundos |
| `pg_stat_user_tables.n_dead_tup` | Tuplas muertas (autovacuum) | > 20% de filas vivas |
| `kong_http_requests_total` | Requests totales | Pico anómalo |
| `gotrue_request_duration` | Latencia auth | p99 > 2s |
| Disk usage | Espacio en disco | > 85% |

**Dashboards recomendados:**

- [Supabase Self-Hosted Dashboard](https://grafana.com/grafana/dashboards/) - busca dashboards PostgreSQL + Kong
- [PostgreSQL Database](https://grafana.com/grafana/dashboards/9628) - dashboard oficial Postgres

---

## 6. Optimización de base de datos

### Autovacuum

En producción el autovacuum debe estar finamente ajustado:

```ini
# postgresql.conf (montado como volumen en db)
# ──────────────────────────────────────────────
# AUTOVACUUM
# ──────────────────────────────────────────────
autovacuum = on
autovacuum_max_workers = 4                   # 1-2 por core
autovacuum_naptime = 30s                     # frecuencia de chequeo
autovacuum_vacuum_threshold = 50             # mínimo de tuplas muertas
autovacuum_vacuum_scale_factor = 0.05        # 5% de la tabla
autovacuum_vacuum_cost_limit = 1000          # más agresivo
autovacuum_vacuum_cost_delay = 5ms           # delay entre operaciones

# Para tablas grandes (>10GB), ajusta individualmente:
# ALTER TABLE mi_tabla SET (autovacuum_vacuum_scale_factor = 0.01);
```

### Monitorear autovacuum

```sql
-- Tablas que necesitan vacuum
SELECT
    schemaname || '.' || relname AS table,
    n_dead_tup AS dead_tuples,
    n_live_tup AS live_tuples,
    round(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
    last_autovacuum,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Actividad actual de autovacuum
SELECT pid, datname, usename, application_name, query, state
FROM pg_stat_activity
WHERE query LIKE '%autovacuum%';
```

### Índices recomendados

Supabase crea índices automáticos para foreign keys y auth, pero debes agregar:

```sql
-- Índices para queries comunes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_id ON public.orders(user_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_created_at ON public.orders(created_at DESC);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_status ON public.orders(status) WHERE status = 'pending';

-- Índices compuestos para reports
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_status_date 
    ON public.orders(user_id, status, created_at DESC);

-- Índices para búsqueda de texto (si usas pg_trgm)
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_name_trgm 
    ON public.products USING gin (name gin_trgm_ops);
```

### Identificar queries lentas

```sql
-- Queries lentas en ejecución
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity
WHERE state != 'idle' 
  AND query_start < now() - interval '1 second'
ORDER BY duration DESC;

-- Estadísticas de tablas (sequential scans = falta índice)
SELECT schemaname, tablename, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch
FROM pg_stat_user_tables
WHERE seq_scan > 1000 AND idx_scan = 0
ORDER BY seq_scan DESC;

-- Explicar plan de una query
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = '...';
```

### Configuración memoria PostgreSQL

```ini
# postgresql.conf - Ajustar según RAM disponible
# RAM total: 8GB | 16GB | 32GB
shared_buffers = 2GB       | 4GB   | 8GB      # 25% de RAM
effective_cache_size = 6GB | 12GB  | 24GB     # 75% de RAM
work_mem = 32MB            | 64MB  | 128MB    # por operación
maintenance_work_mem = 256MB | 512MB | 1GB    # para VACUUM, índices
```

---

## 7. Hardening de seguridad

### RLS obligatorio

Todas las tablas públicas deben tener RLS habilitado:

```sql
-- Verificar tablas sin RLS
SELECT schemaname, tablename 
FROM pg_tables 
WHERE schemaname = 'public'
  AND tablename NOT IN (SELECT tablename FROM pg_policies WHERE schemaname = 'public');

-- Script de hardening
DO $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN 
        SELECT schemaname, tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
          AND tablename NOT IN (
              SELECT DISTINCT tablename 
              FROM pg_policies 
              WHERE schemaname = 'public'
          )
          AND tablename NOT IN ('_prisma_migrations', 'schema_migrations')
    LOOP
        EXECUTE format('ALTER TABLE %I.%I ENABLE ROW LEVEL SECURITY;', rec.schemaname, rec.tablename);
        RAISE NOTICE 'RLS enabled on: %.%', rec.schemaname, rec.tablename;
    END LOOP;
END $$;
```

### Prevención de SQL injection

PostgREST y el SDK de Supabase previenen injection por diseño, pero ten en cuenta:

```dart
// ✅ SEGURO: Usar el SDK de Supabase
final data = await supabase
    .from('products')
    .select()
    .eq('name', userInput);  // sanitizado automáticamente

// ❌ PELIGRO: SQL crudo sin sanitizar
final data = await supabase.rpc('dynamic_query', params: {
    'input': userInput,  // depende de la implementación de la función
});

// ✅ SEGURO: SQL crudo con parámetros
await supabase.rpc('search_products', params: {
    'search_term': userInput,  // función plpgsql usa parámetros
});
```

En funciones plpgsql:

```sql
-- ❌ PELIGRO: concatenación de strings
CREATE OR REPLACE FUNCTION public.search_products_bad(search_term TEXT)
RETURNS SETOF products 
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY EXECUTE format('SELECT * FROM products WHERE name ILIKE ''%%%s%%''', search_term);
END;
$$;

-- ✅ SEGURO: usar parámetros
CREATE OR REPLACE FUNCTION public.search_products(search_term TEXT)
RETURNS SETOF products 
LANGUAGE plpgsql STABLE AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM products 
    WHERE name ILIKE '%' || search_term || '%';  -- parámetro, no concatenación SQL
END;
$$;
```

### Docker resource limits

```yaml
# docker-compose.yml - límites por servicio
services:
  db:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          memory: 2G
  
  postgrest:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
  
  gotrue:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
  
  realtime:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
  
  storage:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
  
  studio:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
```

### Firewall rules

```bash
# Solo puertos necesarios
ufw default deny incoming
ufw default allow outgoing

# SSH
ufw allow 22/tcp

# HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Monitoreo (solo desde IP interna)
ufw allow from 10.0.0.0/8 to any port 9090  # Prometheus
ufw allow from 10.0.0.0/8 to any port 3001  # Grafana

# Denegar acceso directo a PostgreSQL
ufw deny 5432
ufw deny 6432

ufw enable
```

---

## ✅ Checklist de producción

- [ ] Claves únicas generadas (JWT, publishable, secret, Postgres)
- [ ] Secrets gestionados de forma segura (no en repo)
- [ ] PgBounter configurado con pool size calculado
- [ ] Rate limiting en Kong y Nginx
- [ ] SSL con Let's Encrypt y auto-renewal verificado
- [ ] Prometheus + Grafana desplegados y configurados
- [ ] Autovacuum ajustado para tamaño de datos
- [ ] Índices creados para queries frecuentes
- [ ] RLS habilitado en TODAS las tablas públicas
- [ ] Docker resource limits configurados
- [ ] Firewall configurado (solo puertos necesarios)
- [ ] Alertas configuradas (discount, conexiones, deadlocks)

---

**Siguiente**: [04-migracion-local-a-produccion.md](./04-migracion-local-a-produccion.md)
