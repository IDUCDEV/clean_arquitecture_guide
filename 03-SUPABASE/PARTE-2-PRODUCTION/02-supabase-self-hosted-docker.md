# 02 - Supabase Self-Hosted con Docker

> Aprende a instalar y configurar Supabase en tu propio servidor usando Docker. Esta guía cubre desde la preparación del servidor hasta el despliegue completo.

---

## 🎯 Objetivos de este archivo

- Preparar el servidor para Supabase
- Configurar Docker y Docker Compose
- Desplegar Supabase con docker-compose
- Verificar que todo funciona correctamente

---

## 1. Preparación del servidor

### Requisitos del sistema

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| RAM | 4 GB | 8 GB |
| CPU | 2 cores | 4 cores |
| Almacenamiento | 25 GB | 50+ GB SSD |
| OS | Ubuntu 20.04+ | Ubuntu 22.04 LTS |

### Inicializar el servidor

```bash
# Conectar al servidor (ejemplo con IP)
ssh root@tu-servidor-ip

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias básicas
apt install -y curl wget git vim ufw fail2ban

# Crear usuario no-root (recomendado)
adduser supabase
usermod -aG sudo supabase
```

### Configurar firewall

```bash
# Habilitar firewall
ufw enable

# Permitir SSH
ufw allow 22/tcp

# Permitir HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Verificar
ufw status
```

---

## 2. Instalar Docker

```bash
# Actualizar apt
apt update
apt install -y ca-certificates curl gnupg lsb-release

# Añadir clave GPG de Docker
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Añadir repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verificar instalación
docker --version
docker compose version
```

---

## 3. Descargar Supabase

```bash
cd /opt
git clone https://github.com/supabase/supabase.git
cd supabase/docker
ls -la
```

---

## 4. Configuración de producción

### Archivo .env

```bash
# ==============================================================================
# CONFIGURACIÓN DE PRODUCCIÓN - COMPLETAR ESTOS VALORES
# ==============================================================================

# ──────────────────────────────────────────────────────────────────────────────
# POSTGRES
# ──────────────────────────────────────────────────────────────────────────────
POSTGRES_PASSWORD=tu-contraseña-segura-aqui
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_CONFIG_FILE=/etc/postgresql/postgresql.conf

# ──────────────────────────────────────────────────────────────────────────────
# JWT - GENERAR NUEVA CLAVE (python3 -c "import secrets; print(secrets.token_hex(32))")
# ──────────────────────────────────────────────────────────────────────────────
JWT_SECRET=tu-jwt-secret-aqui-muy-largo-y-seguro
JWT_EXPIRY=3600

# ──────────────────────────────────────────────────────────────────────────────
# API KEYS (formato publishable / secret, ver PARTE-1)
# ──────────────────────────────────────────────────────────────────────────────
PUBLISHABLE_KEY=sb_publishable_tu-key-aqui
SECRET_KEY=sb_secret_tu-key-aqui

# ──────────────────────────────────────────────────────────────────────────────
# POSTGREST (REST API)
# ──────────────────────────────────────────────────────────────────────────────
PGRST_DB_SCHEMAS=public,storage,graphql_public
PGRST_DB_ANON_ROLE=anon
PGRST_DB_USE_LEGACY_GUCS=off
PGRST_JWT_SECRET=${JWT_SECRET}

# ──────────────────────────────────────────────────────────────────────────────
# GOTRUE (Auth)
# ──────────────────────────────────────────────────────────────────────────────
GOTRUE_SITE_URL=https://tu-dominio.com
GOTRUE_ADDITIONAL_REDIRECT_URLS=
GOTRUE_DISABLE_SIGNUP=false
GOTRURE_RATE_LIMIT_EMAIL_SENT=5
GOTRUE_RATE_LIMIT_SMS_SENT=3
GOTRUE_EXTERNAL_EMAIL_ENABLED=true
GOTRUE_EXTERNAL_PHONE_ENABLED=true
GOTRUE_MAILER_AUTOCONFIRM=false
GOTRUE_SMS_AUTOCONFIRM=false
GOTRUE_LOG_LEVEL=warn
GOTRUE_OPERATOR_TOKEN=tu-operator-token-aqui

# ──────────────────────────────────────────────────────────────────────────────
# SMTP
# ──────────────────────────────────────────────────────────────────────────────
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=tu-smtp-password
SMTP_SENDER_EMAIL=noreply@tu-dominio.com
SMTP_SENDER_NAME=Mi App

# ──────────────────────────────────────────────────────────────────────────────
# STORAGE
# ──────────────────────────────────────────────────────────────────────────────
STORAGE_BACKEND=file
FILE_SIZE_LIMIT=52428800
STORAGE_IMAGE_TRANSFORMATION_ENABLED=true
STORAGE_IMAGE_TRANSFORMATION_ORIGIN_ALLOW_REGEX=.*
STORAGE_S3_BUCKET=mi-bucket
STORAGE_S3_REGION=us-east-1
STORAGE_S3_ENDPOINT=https://s3.amazonaws.com
STORAGE_S3_ACCESS_KEY_ID=
STORAGE_S3_SECRET_ACCESS_KEY=

# ──────────────────────────────────────────────────────────────────────────────
# REALTIME
# ──────────────────────────────────────────────────────────────────────────────
REALTIME_PORT=4000
REALTIME_POLL_INTERVAL=100
REALTIME_POLL_INTERVAL_DELTA_MULTIPLIER=500
REALTIME_MAX_ROWS_PER_PUBLISH=1000

# ──────────────────────────────────────────────────────────────────────────────
# STUDIO
# ──────────────────────────────────────────────────────────────────────────────
STUDIO_DEFAULT_ORGANIZATION=Mi Org
STUDIO_DEFAULT_PROJECT=Mi Proyecto

# ──────────────────────────────────────────────────────────────────────────────
# PGBOUNCER (Connection Pooling)
# ──────────────────────────────────────────────────────────────────────────────
PGBOUNCER_DEFAULT_POOL_SIZE=20
PGBOUNCER_MAX_CLIENT_CONN=100
PGBOUNCER_POOL_MODE=transaction

# ──────────────────────────────────────────────────────────────────────────────
# EXTERNAL
# ──────────────────────────────────────────────────────────────────────────────
SITE_URL=https://tu-dominio.com
ADDITIONAL_REDIRECT_URLS=
API_EXTERNAL_URL=https://tu-dominio.com

# ──────────────────────────────────────────────────────────────────────────────
# LOGGING (Vector + Logflare - opcional)
# ──────────────────────────────────────────────────────────────────────────────
LOGFLARE_LOGGER_BACKEND_API_KEY=tu-logflare-key
LOGFLARE_SOURCE_ID=tu-source-id
DISABLE_VECTOR=false
```

### Generar claves

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"

# Para las API keys (formato publishable/secret):
# Usar el dashboard de Supabase Cloud o generarlas manualmente.
# Ver PARTE-1-DESARROLLO/04-variables-entorno.md
```

---

## 5. docker-compose.yml completo

> ⚠️ **Producción real:** clona el repositorio oficial [`supabase/infras`](https://github.com/supabase/infras) que contiene el docker-compose actualizado con todas las imágenes versionadas. El ejemplo siguiente es educativo para entender cada servicio.

```yaml
# ==============================================================================
# docker-compose.yml - Supabase Self-Hosted (Educativo)
# ==============================================================================
# Servicios incluidos:
#   db (PostgreSQL + pgvector)   → base de datos
#   pgbouncer                    → connection pooling
#   gotrue                       → autenticación
#   postgrest                    → API REST
#   realtime                     → WebSocket en tiempo real
#   storage                      → almacenamiento de archivos
#   meta                         → introspection de esquemas
#   studio                       → panel de administración
#   kong                         → API gateway
#   imgproxy                     → transformación de imágenes
# ==============================================================================

version: '3.8'

x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:

  # ────────────────────────────────────────────────────────────────────────────
  # PostgreSQL + pgvector
  # ────────────────────────────────────────────────────────────────────────────
  db:
    image: supabase/postgres:15.6.1.147
    container_name: supabase-db
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_CONFIG_FILE: ${POSTGRES_CONFIG_FILE}
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./custom-config/postgresql.conf:/etc/postgresql/postgresql.conf:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    logging: *default-logging
    labels:
      - "supabase.service=db"

  # ────────────────────────────────────────────────────────────────────────────
  # PgBouncer - Connection Pooling
  # ────────────────────────────────────────────────────────────────────────────
  pgbouncer:
    image: bitnami/pgbouncer:1.23
    container_name: supabase-pgbouncer
    restart: unless-stopped
    ports:
      - "6432:6432"
    environment:
      POSTGRESQL_HOST: db
      POSTGRESQL_PORT: "5432"
      POSTGRESQL_USERNAME: ${POSTGRES_USER}
      POSTGRESQL_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRESQL_DATABASE: ${POSTGRES_DB}
      PGBOUNCER_DEFAULT_POOL_SIZE: ${PGBOUNCER_DEFAULT_POOL_SIZE:-20}
      PGBOUNCER_MAX_CLIENT_CONN: ${PGBOUNCER_MAX_CLIENT_CONN:-100}
      PGBOUNCER_POOL_MODE: ${PGBOUNCER_POOL_MODE:-transaction}
      PGBOUNCER_AUTH_TYPE: scram-sha-256
    depends_on:
      db:
        condition: service_healthy
    logging: *default-logging
    labels:
      - "supabase.service=pgbouncer"

  # ────────────────────────────────────────────────────────────────────────────
  # Kong - API Gateway
  # ────────────────────────────────────────────────────────────────────────────
  kong:
    image: kong:3.4
    container_name: supabase-kong
    restart: unless-stopped
    ports:
      - "80:8000/tcp"
      - "443:8443/tcp"
      - "54321:8000/tcp"   # rest
      - "54322:8001/tcp"   # admin (local only en prod)
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /var/lib/kong/kong.yml
      KONG_DNS_ORDER: LAST, A, CNAME
      KONG_LOG_LEVEL: warn
      KONG_NGINX_WORKER_PROCESSES: "4"
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
    volumes:
      - ./volumes/kong/kong.yml:/var/lib/kong/kong.yml:ro
    depends_on:
      - gotrue
      - postgrest
      - realtime
      - storage
      - meta
    logging: *default-logging
    labels:
      - "supabase.service=kong"

  # ────────────────────────────────────────────────────────────────────────────
  # GoTrue - Auth Service
  # ────────────────────────────────────────────────────────────────────────────
  gotrue:
    image: supabase/gotrue:v2.163.0
    container_name: supabase-gotrue
    restart: unless-stopped
    environment:
      GOTRUE_API_HOST: "0.0.0.0"
      GOTRUE_API_PORT: "9999"
      PORT: "9999"
      GOTRUE_SITE_URL: ${GOTRUE_SITE_URL}
      GOTRUE_ADDITIONAL_REDIRECT_URLS: ${GOTRUE_ADDITIONAL_REDIRECT_URLS}
      GOTRUE_DISABLE_SIGNUP: ${GOTRUE_DISABLE_SIGNUP}
      GOTRURE_RATE_LIMIT_EMAIL_SENT: ${GOTRURE_RATE_LIMIT_EMAIL_SENT}
      GOTRUE_RATE_LIMIT_SMS_SENT: ${GOTRUE_RATE_LIMIT_SMS_SENT}
      GOTRUE_JWT_SECRET: ${JWT_SECRET}
      GOTRUE_JWT_EXP: ${JWT_EXPIRY}
      GOTRUE_DB_DRIVER: postgres
      GOTRUE_DB_DATABASE_URL: "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@pgbouncer:6432/${POSTGRES_DB}?sslmode=disable"
      GOTRUE_EXTERNAL_EMAIL_ENABLED: ${GOTRUE_EXTERNAL_EMAIL_ENABLED}
      GOTRUE_EXTERNAL_PHONE_ENABLED: ${GOTRUE_EXTERNAL_PHONE_ENABLED}
      GOTRUE_MAILER_AUTOCONFIRM: ${GOTRUE_MAILER_AUTOCONFIRM:-false}
      GOTRUE_SMS_AUTOCONFIRM: ${GOTRUE_SMS_AUTOCONFIRM:-false}
      GOTRUE_SMTP_HOST: ${SMTP_HOST}
      GOTRUE_SMTP_PORT: ${SMTP_PORT}
      GOTRUE_SMTP_USER: ${SMTP_USER}
      GOTRUE_SMTP_PASS: ${SMTP_PASSWORD}
      GOTRUE_SMTP_SENDER_NAME: ${SMTP_SENDER_NAME}
      GOTRUE_MAILER_URLPATHS_CONFIRMATION: "/auth/v1/verify"
      GOTRUE_LOG_LEVEL: ${GOTRUE_LOG_LEVEL:-warn}
      GOTRUE_OPERATOR_TOKEN: ${GOTRUE_OPERATOR_TOKEN}
    depends_on:
      pgbouncer:
        condition: service_started
    logging: *default-logging
    labels:
      - "supabase.service=auth"

  # ────────────────────────────────────────────────────────────────────────────
  # PostgREST - REST API
  # ────────────────────────────────────────────────────────────────────────────
  postgrest:
    image: postgrest/postgrest:v12.2.3
    container_name: supabase-postgrest
    restart: unless-stopped
    environment:
      PGRST_DB_URI: "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@pgbouncer:6432/${POSTGRES_DB}"
      PGRST_DB_SCHEMAS: ${PGRST_DB_SCHEMAS}
      PGRST_DB_ANON_ROLE: ${PGRST_DB_ANON_ROLE:-anon}
      PGRST_DB_USE_LEGACY_GUCS: ${PGRST_DB_USE_LEGACY_GUCS:-off}
      PGRST_JWT_SECRET: ${JWT_SECRET}
      PGRST_OPENAPI_SECURITY_ACTIVE: "false"
      PGRST_DB_ROOT_SPEC: "home"
      PGRST_LOG_LEVEL: warn
    depends_on:
      pgbouncer:
        condition: service_started
    logging: *default-logging
    labels:
      - "supabase.service=postgrest"

  # ────────────────────────────────────────────────────────────────────────────
  # Realtime - WebSocket
  # ────────────────────────────────────────────────────────────────────────────
  realtime:
    image: supabase/realtime:v2.34.10
    container_name: supabase-realtime
    restart: unless-stopped
    ports:
      - "4000:4000"
    environment:
      PORT: "4000"
      DB_HOST: pgbouncer
      DB_PORT: "6432"
      DB_USER: ${POSTGRES_USER}
      DB_PASSWORD: ${POSTGRES_PASSWORD}
      DB_NAME: ${POSTGRES_DB}
      DB_AFTER_CONNECT_QUERY: "SET search_path TO _realtime"
      DB_ENC_KEY: "supabase_realtime_${JWT_SECRET}"
      JWT_SECRET: ${JWT_SECRET}
      REPLICATION_MODE: "stream"
      REPLICATION_POLL_INTERVAL: ${REALTIME_POLL_INTERVAL}
      SECURE_CHANNELS: "true"
      SLOT_NAME: "supabase_realtime_replication_slot"
      TEMPORARY_SLOT: "true"
      LOG_LEVEL: warn
    depends_on:
      pgbouncer:
        condition: service_started
    logging: *default-logging
    labels:
      - "supabase.service=realtime"

  # ────────────────────────────────────────────────────────────────────────────
  # Storage - File Storage
  # ────────────────────────────────────────────────────────────────────────────
  storage:
    image: supabase/storage-api:v1.14.6
    container_name: supabase-storage
    restart: unless-stopped
    environment:
      ANON_KEY: ${PUBLISHABLE_KEY}
      SERVICE_KEY: ${SECRET_KEY}
      POSTGREST_URL: "http://postgrest:3000"
      PGRST_JWT_SECRET: ${JWT_SECRET}
      DATABASE_URL: "postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@pgbouncer:6432/${POSTGRES_DB}"
      PGOPTIONS: "-c search_path=storage"
      FILE_SIZE_LIMIT: ${FILE_SIZE_LIMIT:-52428800}
      STORAGE_BACKEND: ${STORAGE_BACKEND:-file}
      FILE_STORAGE_BACKEND_PATH: /var/lib/storage
      TENANT_ID: "public"
      REGION: us-east-1
      GLOBAL_S3_BUCKET: ${STORAGE_S3_BUCKET:-storage}
      AWS_ACCESS_KEY_ID: ${STORAGE_S3_ACCESS_KEY_ID}
      AWS_SECRET_ACCESS_KEY: ${STORAGE_S3_SECRET_ACCESS_KEY}
      AWS_DEFAULT_REGION: ${STORAGE_S3_REGION}
    volumes:
      - storage-data:/var/lib/storage
    depends_on:
      - postgrest
    logging: *default-logging
    labels:
      - "supabase.service=storage"

  # ────────────────────────────────────────────────────────────────────────────
  # pg-meta - Schema Introspection
  # ────────────────────────────────────────────────────────────────────────────
  meta:
    image: supabase/postgres-meta:v0.84.2
    container_name: supabase-meta
    restart: unless-stopped
    environment:
      PG_META_PORT: "8080"
      PG_META_DB_HOST: pgbouncer
      PG_META_DB_PORT: "6432"
      PG_META_DB_NAME: ${POSTGRES_DB}
      PG_META_DB_USER: ${POSTGRES_USER}
      PG_META_DB_PASSWORD: ${POSTGRES_PASSWORD}
      PG_META_DB_SCHEMA: "public"
    depends_on:
      pgbouncer:
        condition: service_started
    logging: *default-logging
    labels:
      - "supabase.service=meta"

  # ────────────────────────────────────────────────────────────────────────────
  # Studio - Admin UI
  # ────────────────────────────────────────────────────────────────────────────
  studio:
    image: supabase/studio:20250101
    container_name: supabase-studio
    restart: unless-stopped
    environment:
      STUDIO_PG_META_URL: "http://meta:8080"
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      DEFAULT_ORGANIZATION_NAME: ${STUDIO_DEFAULT_ORGANIZATION}
      DEFAULT_PROJECT_NAME: ${STUDIO_DEFAULT_PROJECT}
      SUPABASE_URL: "http://kong:8000"
      SUPABASE_ANON_KEY: ${PUBLISHABLE_KEY}
      SUPABASE_SERVICE_KEY: ${SECRET_KEY}
      SUPABASE_PUBLISHABLE_KEY: ${PUBLISHABLE_KEY}
      AUTH_ENDPOINT: "http://kong:8000/auth/v1"
      LOGFLARE_ENABLED: "false"
    depends_on:
      - meta
    logging: *default-logging
    labels:
      - "supabase.service=studio"

  # ────────────────────────────────────────────────────────────────────────────
  # imgproxy - Image Transformation (opcional)
  # ────────────────────────────────────────────────────────────────────────────
  imgproxy:
    image: darthsim/imgproxy:v3.8.0
    container_name: supabase-imgproxy
    restart: unless-stopped
    environment:
      IMGPROXY_BIND: ":5001"
      IMGPROXY_LOCAL_FILESYSTEM_ROOT: /
      IMGPROXY_USE_ETAG: "true"
      IMGPROXY_ENABLE_WEBP_DETECTION: "true"
    volumes:
      - storage-data:/var/lib/storage:ro
    logging: *default-logging
    labels:
      - "supabase.service=imgproxy"

volumes:
  db-data:
  storage-data:
  kong-data:
```

---

## 6. Kong: configuración declarativa

Kong funciona como API Gateway enrutando cada servicio bajo la misma URL. Crea `volumes/kong/kong.yml`:

```yaml
# ==============================================================================
# kong.yml - Configuración declarativa de Kong
# ==============================================================================
# Formato: decK (declarative Kong config)
# ==============================================================================

_format_version: "3.0"
_transform: true

services:

  # ────────────────────────────────────────────────────────────────────────────
  # Auth (GoTrue)
  # ────────────────────────────────────────────────────────────────────────────
  - name: auth-service
    url: http://gotrue:9999
    routes:
      - name: auth-route
        paths:
          - /auth/v1
        strip_path: false
        methods:
          - GET
          - POST
          - PUT
          - DELETE
          - OPTIONS
        protocols:
          - http
          - https
    plugins:
      - name: cors
        config:
          origins:
            - "*"
          methods:
            - GET
            - POST
            - PUT
            - DELETE
            - OPTIONS
          headers:
            - Accept
            - Authorization
            - Content-Type
            - apikey
            - X-Client-Info
          exposed_headers:
            - Content-Range
            - X-Total-Count
          preflight_continue: false

  # ────────────────────────────────────────────────────────────────────────────
  # REST API (PostgREST)
  # ────────────────────────────────────────────────────────────────────────────
  - name: rest-service
    url: http://postgrest:3000
    routes:
      - name: rest-route
        paths:
          - /rest/v1
        strip_path: true
        methods:
          - GET
          - POST
          - PATCH
          - PUT
          - DELETE
          - OPTIONS
        protocols:
          - http
          - https
    plugins:
      - name: cors
        config:
          origins:
            - "*"
          methods:
            - GET
            - POST
            - PATCH
            - PUT
            - DELETE
            - OPTIONS
          headers:
            - Accept
            - Authorization
            - Content-Type
            - apikey
            - X-Client-Info
            - Prefer
          exposed_headers:
            - Content-Range
            - X-Total-Count
          preflight_continue: false
      - name: rate-limiting
        config:
          minute: 60
          hour: 2000
          policy: local

  # ────────────────────────────────────────────────────────────────────────────
  # Realtime (WebSocket)
  # ────────────────────────────────────────────────────────────────────────────
  - name: realtime-service
    url: http://realtime:4000
    routes:
      - name: realtime-route
        paths:
          - /realtime/v1
        strip_path: true
        methods:
          - GET
          - POST
          - OPTIONS
        protocols:
          - http
          - https
    plugins:
      - name: cors
        config:
          origins:
            - "*"
          methods:
            - GET
            - POST
            - OPTIONS
          headers:
            - Accept
            - Authorization
            - Content-Type
            - apikey
          preflight_continue: false

  # ────────────────────────────────────────────────────────────────────────────
  # Storage API
  # ────────────────────────────────────────────────────────────────────────────
  - name: storage-service
    url: http://storage:5000
    routes:
      - name: storage-route
        paths:
          - /storage/v1
        strip_path: false
        methods:
          - GET
          - POST
          - PUT
          - DELETE
          - OPTIONS
        protocols:
          - http
          - https
    plugins:
      - name: cors
        config:
          origins:
            - "*"
          methods:
            - GET
            - POST
            - PUT
            - DELETE
            - OPTIONS
          headers:
            - Accept
            - Authorization
            - Content-Type
            - apikey
            - X-Client-Info
          exposed_headers:
            - Content-Range
            - X-Total-Count
          preflight_continue: false
      - name: rate-limiting
        config:
          minute: 30
          hour: 1000
          policy: local

  # ────────────────────────────────────────────────────────────────────────────
  # Studio (Admin UI)
  # ────────────────────────────────────────────────────────────────────────────
  - name: studio-service
    url: http://studio:3000
    routes:
      - name: studio-route
        paths:
          - /
        strip_path: true
        methods:
          - GET
          - POST
          - PUT
          - DELETE
          - OPTIONS
        protocols:
          - http
          - https
    plugins:
      - name: cors
        config:
          origins:
            - "*"
          methods:
            - GET
            - POST
            - PUT
            - DELETE
            - OPTIONS
          headers:
            - Accept
            - Authorization
            - Content-Type
          preflight_continue: false

  # ────────────────────────────────────────────────────────────────────────────
  # pg-meta (schema API, usado internamente por Studio)
  # ────────────────────────────────────────────────────────────────────────────
  - name: meta-service
    url: http://meta:8080
    routes:
      - name: meta-route
        paths:
          - /pg
        strip_path: true
        methods:
          - GET
          - POST
          - OPTIONS
        protocols:
          - http
          - https
    plugins:
      - name: cors
        config:
          origins:
            - "*"
          methods:
            - GET
            - POST
            - OPTIONS
          headers:
            - Accept
            - Authorization
            - Content-Type
          preflight_continue: false
```

> La configuración incluye **rate-limiting** (60 req/min en REST, 30 en Storage) y **CORS** global. Ajusta según tu carga esperada.

---

## 7. Iniciar Supabase

```bash
cd /opt/supabase/docker

# Crear directorio para Kong config
mkdir -p volumes/kong

# Iniciar servicios (db primero, luego el resto)
docker compose up -d

# Ver estado
docker compose ps

# Ver logs (Ctrl+C para salir)
docker compose logs -f
```

### Orden de inicio

Los servicios dependen unos de otros, Docker Compose los arranca en este orden:

```
db ──► pgbouncer ──► gotrue / postgrest / realtime / meta ──► storage / studio ──► kong
```

### Verificar cada servicio

```bash
# PostgreSQL
docker exec -it supabase-db psql -U postgres -c "SELECT version();"

# PgBouncer
docker exec supabase-pgbouncer psql -U postgres -h localhost -p 6432 -c "SHOW POOLS;"

# Auth (GoTrue)
curl -s http://localhost:9999/health | python3 -m json.tool

# REST API
curl -s http://localhost:54321/rest/v1/ -H "apikey: ${PUBLISHABLE_KEY}" | head

# Realtime
curl -s http://localhost:4000/ | head

# Storage
curl -s http://localhost:5000/status | python3 -m json.tool

# Studio
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/

# Kong (health check global)
curl -s http://localhost:54321/rest/v1/ -H "apikey: ${PUBLISHABLE_KEY}" -o /dev/null -w "%{http_code}"
```

---

## 8. Configurar Nginx como reverse proxy

```nginx
# /etc/nginx/sites-available/supabase

upstream kong_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;

    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

    # Rate limiting por IP
    limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
    limit_req zone=api burst=50 nodelay;

    # Tamaño máximo de subida para Storage
    client_max_body_size 50M;

    # Proxy a Kong
    location / {
        proxy_pass http://kong_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400s;  # WebSocket long-polling
    }
}
```

### SSL con Let's Encrypt (auto-renewal)

```bash
# Instalar certbot
apt install -y certbot python3-certbot-nginx

# Obtener certificado (configura Nginx automáticamente)
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Verificar auto-renewal
certbot renew --dry-run

# El renewal es automático vía systemd timer
systemctl list-timers | grep certbot
```

---

## 9. Connection Pooling (PgBouncer)

PgBouncer es crítico en producción. Sin él, cada conexión de gotrue, postgrest o realtime consume un proceso PostgreSQL completo.

### Cómo funciona en este stack

```
App ──► Kong ──► PostgREST ──► PgBouncer (6432) ──► PostgreSQL (5432)
                              │
                 GoTrue ──────┤
                 Realtime ────┤
```

### Modos de pool

| Modo | Descripción | Recomendado para |
|------|-------------|------------------|
| `session` | Una conexión por sesión | Sesiones largas, NOTIFY/LISTEN |
| `transaction` | Conexión se libera al terminar transacción | **API REST** (PostgREST) ✅ |
| `statement` | Conexión se libera tras cada sentencia | Carga muy alta, queries simples |

Para Supabase usa `transaction` (el default). PostgREST y GoTrue abren/cierran transacciones rápidamente.

### Ajustar pool size

```bash
# Ejemplo de cálculo:
# PostgREST: 10 workers x 2 conexiones c/u = 20
# GoTrue: 5 workers x 2 conexiones c/u = 10
# Realtime: 3 slots de replicación = 3
# Total ≈ 33 conexiones simultáneas

PGBOUNCER_DEFAULT_POOL_SIZE=40   # un poco de margen
PGBOUNCER_MAX_CLIENT_CONN=200    # conexiones entrantes totales
```

### Monitorear pools

```bash
# Ver estado de pools
docker exec supabase-pgbouncer psql -U postgres -h localhost -p 6432 -d pgbouncer -c "SHOW POOLS;"

# Ver estadísticas
docker exec supabase-pgbouncer psql -U postgres -h localhost -p 6432 -d pgbouncer -c "SHOW STATS;"

# Client connections activas
docker exec supabase-pgbouncer psql -U postgres -h localhost -p 6432 -d pgbouncer -c "SHOW CLIENTS;"
```

---

## 10. Storage: backend local vs S3

### Backend local (file system)

Ideal para desarrollo o volúmenes bajos. Los archivos se guardan en el volumen `storage-data`.

```bash
# .env
STORAGE_BACKEND=file
FILE_SIZE_LIMIT=52428800  # 50 MB
```

### Backend S3 (producción)

Para escalar, usa S3 compatible (AWS, Backblaze B2, MinIO):

```yaml
# .env
STORAGE_BACKEND=s3
STORAGE_S3_BUCKET=mi-bucket
STORAGE_S3_REGION=us-east-1
STORAGE_S3_ENDPOINT=https://s3.us-east-1.amazonaws.com
STORAGE_S3_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
STORAGE_S3_SECRET_ACCESS_KEY=...
```

> ⚠️ **Nunca** expongas claves S3 en el .env en repositorios. Úsalas como secrets de Docker o variables de entorno del servidor.

**Proveedores S3 recomendados:**

| Proveedor | Costo almacenamiento | Costo egress | Latencia |
|-----------|---------------------|--------------|----------|
| AWS S3 | $0.023/GB | $0.09/GB | Baja (US/EU) |
| Backblaze B2 | $0.006/GB | $0.01/GB (CDN) | Media |
| Cloudflare R2 | $0.015/GB | $0 (sin egress) | Baja (global CDN) |
| MinIO (self-hosted) | $0 (tu storage) | $0 | Depende del hosting |

---

## 11. Orquestación y actualizaciones

### Script de actualización

```bash
#!/bin/bash
# update-supabase.sh
set -e

cd /opt/supabase/docker

echo "==> Actualizando imágenes..."
docker compose pull

echo "==> Recreando servicios..."
docker compose up -d --remove-orphans

echo "==> Limpiando imágenes viejas..."
docker image prune -f

echo "✅ Supabase actualizado"
```

### Programar actualizaciones automáticas

```bash
# /etc/cron.weekly/supabase-update
#!/bin/bash
/opt/supabase/scripts/update-supabase.sh
```

O usa Watchtower para actualización automática de contenedores:

```yaml
# Agregar al docker-compose.yml
  watchtower:
    image: containrrr/watchtower
    container_name: supabase-watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      WATCHTOWER_CLEANUP: "true"
      WATCHTOWER_SCHEDULE: "0 0 4 * * *"  # 4 AM daily
      WATCHTOWER_INCLUDE_STOPPED: "false"
    logging: *default-logging
```

---

## ✅ Checklist de instalación

- [ ] Servidor preparado (RAM ≥ 8GB, Docker, firewall)
- [ ] Docker y Docker Compose instalados
- [ ] Claves JWT, API keys (publishable/secret) generadas
- [ ] .env completo con todos los servicios
- [ ] docker-compose.yml configurado (con pgBouncer)
- [ ] Kong config (kong.yml) con CORS y rate limiting
- [ ] Nginx + SSL configurado con Let's Encrypt
- [ ] PgBouncer pool size ajustado
- [ ] Storage backend elegido (local / S3)
- [ ] Servicios iniciados y verificados
- [ ] Script de actualización programado

---

## 📚 Recursos

- [Supabase Self-Hosting Docs](https://supabase.com/docs/guides/self-hosting)
- [Repositorio oficial supabase/infras](https://github.com/supabase/infras)
- [Supabase Docker (legacy)](https://github.com/supabase/supabase/tree/master/docker)
- [Kong Gateway](https://konghq.com)
- [PgBouncer Documentation](https://www.pgbouncer.org/config.html)
- [Let's Encrypt](https://letsencrypt.org)

---

**Siguiente**: [03-configuracion-produccion.md](./03-configuracion-produccion.md)