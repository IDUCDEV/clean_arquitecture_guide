# 05 - Backup y Mantenimiento

> Aprende a implementar estrategias de backup con WAL-G (Point-in-Time Recovery), verificar restauraciones, mantener Supabase actualizado y planificar recuperación ante desastres.

---

## 🎯 Objetivos

- Implementar WAL-G para continuous archiving y PITR
- Automatizar backups con verificación
- Ejecutar Point-in-Time Recovery
- Mantener Supabase actualizado sin downtime
- Plan de recuperación ante desastres (DR)

---

## 1. Estrategia de backups

| Tipo | Frecuencia | Retención | Uso |
|------|------------|-----------|-----|
| **WAL-G full** | Diario | 7 días | Restauración completa |
| **WAL-G incremental (WAL)** | Continuo (cada 5 min) | 24 horas | PITR (minuto exacto) |
| **WAL-G full semanal** | Semanal | 90 días | Archivado |
| **pg_dump (schema-only)** | Diario | 30 días | Migración, diff |
| **Export SQL** | Semanal | 90 días | Compatibilidad cross-version |

### Esquema de directorio

```
/opt/supabase/
├── backups/
│   ├── wal-g/           ← backups WAL-G
│   ├── pg_dump/         ← backups pg_dump tradicionales
│   └── exports/         ← exports SQL semanales
├── scripts/
│   ├── backup-walg.sh
│   ├── backup-pgdump.sh
│   ├── verify-backup.sh
│   └── restore-pitr.sh
```

---

## 2. WAL-G: Continuous Archiving

[WAL-G](https://github.com/wal-g/wal-g) es la herramienta estándar para backups PostgreSQL en producción. Permite **Point-in-Time Recovery** (restaurar a cualquier minuto).

### Instalación

```bash
# Descargar binary
wget -O /usr/local/bin/wal-g https://github.com/wal-g/wal-g/releases/latest/download/wal-g-pg-ubuntu-22.04-amd64
chmod +x /usr/local/bin/wal-g

# Verificar
wal-g --version
```

### Configuración

```bash
# /etc/wal-g.env
export WALG_COMPRESSION_METHOD=brotli
export WALG_DELTA_MAX_STEPS=6
export WALG_FILE_PREFIX=/opt/supabase/backups/wal-g

# AWS S3 (alternativa)
# export WALG_S3_PREFIX=s3://mi-bucket/supabase-backups/
# export AWS_ACCESS_KEY_ID=...
# export AWS_SECRET_ACCESS_KEY=...
# export AWS_REGION=us-east-1
```

### Configurar PostgreSQL para archiving

```ini
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = '/usr/local/bin/wal-g wal-push "%p"'
archive_timeout = 300       # 5 minutos
```

### Script de backup full

```bash
#!/bin/bash
# /opt/supabase/scripts/backup-walg.sh
set -e

source /etc/wal-g.env
BACKUP_DIR="/opt/supabase/backups/wal-g"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${BACKUP_DIR}/logs/backup_${DATE}.log"

mkdir -p "${BACKUP_DIR}/logs"

echo "[$(date)] Iniciando backup WAL-G..." | tee -a "$LOG_FILE"

# Backup full con delta
wal-g backup-push /var/lib/postgresql/data \
  --full \
  2>&1 | tee -a "$LOG_FILE"

# Backup de schema (pg_dump complementario)
docker exec supabase-db pg_dump \
  -U postgres \
  -d postgres \
  --schema-only \
  --no-owner \
  --no-privileges \
  -F c \
  > "${BACKUP_DIR}/schema_${DATE}.dump" \
  2>> "$LOG_FILE"

# Limpiar backups viejos (retener 7 fulls)
wal-g delete retain FULL 7 --confirm 2>&1 | tee -a "$LOG_FILE"

# Limpiar WALs de más de 24h
# (wal-g lo maneja automáticamente si usas retention)

echo "[$(date)] Backup completado ✅" | tee -a "$LOG_FILE"
```

### Programar en cron

```bash
# /etc/cron.d/supabase-backup
# Backup full diario a las 2:00 AM
0 2 * * * root /opt/supabase/scripts/backup-walg.sh

# Verificación de backups (lunes 6 AM)
0 6 * * 1 root /opt/supabase/scripts/verify-backup.sh

# pg_dump semanal (domingo 3 AM)
0 3 * * 0 root /opt/supabase/scripts/backup-pgdump.sh
```

---

## 3. Verificación de backups

Un backup que no se prueba no es un backup. Automatiza la verificación:

```bash
#!/bin/bash
# /opt/supabase/scripts/verify-backup.sh
set -e

source /etc/wal-g.env
LOG_FILE="/opt/supabase/backups/logs/verify_$(date +%Y%m%d).log"

echo "[$(date)] Verificando backups..." | tee -a "$LOG_FILE"

# 1. Listar backups disponibles
echo "Backups disponibles:" | tee -a "$LOG_FILE"
wal-g backup-list 2>&1 | tee -a "$LOG_FILE"

# 2. Verificar integridad del último backup
LATEST=$(wal-g backup-list 2>/dev/null | tail -1 | awk '{print $1}')
if [ -n "$LATEST" ]; then
    echo "Verificando backup: $LATEST" | tee -a "$LOG_FILE"
    wal-g backup-show "$LATEST" 2>&1 | tee -a "$LOG_FILE"
fi

# 3. Verificar que pg_dump no está corrupto
LATEST_DUMP=$(ls -t /opt/supabase/backups/wal-g/schema_*.dump 2>/dev/null | head -1)
if [ -n "$LATEST_DUMP" ]; then
    echo "Verificando schema dump: $LATEST_DUMP" | tee -a "$LOG_FILE"
    pg_restore -l "$LATEST_DUMP" > /dev/null 2>&1 \
        && echo "✅ Dump válido" \
        || echo "❌ Dump corrupto"
fi

# 4. Probar restore en contenedor temporal (opcional, requiere recursos)
# docker run --rm -v wal-g-backup:/backup postgres:15 ...

echo "[$(date)] Verificación completada ✅" | tee -a "$LOG_FILE"
```

---

## 4. Point-in-Time Recovery (PITR)

Restaurar la base de datos a un minuto específico (ej: justo antes de un `DROP TABLE`).

### Script de restore

```bash
#!/bin/bash
# /opt/supabase/scripts/restore-pitr.sh
set -e

source /etc/wal-g.env

if [ -z "$1" ]; then
    echo "Uso: $0 <timestamp>"
    echo "Ejemplo: $0 '2024-12-25 14:30:00.000-05'"
    exit 1
fi

TARGET_TIME="$1"
RESTORE_DIR="/opt/supabase/restore/pitr_$(date +%Y%m%d_%H%M%S)"

echo "==> Restaurando a: $TARGET_TIME"
echo "==> Directorio: $RESTORE_DIR"

mkdir -p "$RESTORE_DIR"

# 1. Descargar backup y WALs hasta el timestamp
wal-g backup-fetch "$RESTORE_DIR" LATEST

# 2. Configurar recovery.conf
cat > "$RESTORE_DIR/recovery.conf" << EOF
restore_command = '/usr/local/bin/wal-g wal-fetch "%f" "%p"'
recovery_target_time = '$TARGET_TIME'
recovery_target_action = 'promote'
EOF

# 3. Iniciar PostgreSQL temporal para recovery
docker run --name supabase-restore \
    -v "$RESTORE_DIR:/var/lib/postgresql/data" \
    -e POSTGRES_PASSWORD=temp \
    -d supabase/postgres:15.6.1.147 \
    -c 'config_file=/var/lib/postgresql/data/postgresql.conf'

# 4. Esperar a que termine recovery
echo "==> Esperando recovery..."
sleep 10

# 5. Exportar datos recuperados
docker exec supabase-restore pg_dump \
    -U postgres \
    -d postgres \
    -F c \
    > "${RESTORE_DIR}/recovered_$(date +%Y%m%d).dump"

# 6. Limpiar
docker stop supabase-restore
docker rm supabase-restore

echo "==> Restore completado: ${RESTORE_DIR}/recovered_*.dump"
```

### Escenarios de recovery

| Escenario | Estrategia | RPO (pérdida máxima) | RTO (tiempo recuperación) |
|-----------|-----------|---------------------|--------------------------|
| Drop table accidental | PITR a timestamp anterior | ~5 min | 30-60 min |
| Corrupción de datos | PITR + restore a nuevo contenedor | ~5 min | 1-2 hrs |
| Falla de disco | Restaurar desde backup full en nuevo servidor | 24h (full) | 2-4 hrs |
| Desastre total (región) | Restaurar desde backup S3 en otra región | 24h | 4-8 hrs |

---

## 5. Plan de Recuperación ante Desastres (DR)

### Checkpoints por severidad

#### 🟢 Leve (error de un usuario)

```bash
# 1. Identificar el problema
# 2. Si es data corruption, restaurar solo esa fila desde backup
# 3. No requiere downtime
```

#### 🟡 Moderado (tabla corrupta)

```bash
# 1. Detener servicio que escribe en esa tabla
# 2. Restaurar tabla específica desde backup
pg_restore -U postgres -d postgres \
    -t public.orders \
    -c \
    latest_backup.dump
# 3. Re-aplicar cambios desde logs de aplicación
# 4. Reactivar servicio
```

#### 🔴 Crítico (base de datos caída)

```bash
# 1. Detener todos los servicios
docker compose down

# 2. Restaurar backup más reciente
wal-g backup-fetch /var/lib/postgresql/data LATEST

# 3. Configurar recovery
echo "restore_command = '/usr/local/bin/wal-g wal-fetch \"%f\" \"%p\"'" \
    > /var/lib/postgresql/data/recovery.conf
echo "recovery_target_time = '2024-12-25 14:30:00'" >> recovery.conf
echo "recovery_target_action = 'promote'" >> recovery.conf

# 4. Iniciar solo DB
docker compose up -d db
sleep 30

# 5. Verificar integridad
docker exec supabase-db psql -U postgres -c "SELECT count(*) FROM orders;"

# 6. Iniciar resto de servicios
docker compose up -d

# 7. Notificar al equipo
```

### DR Plan documentado

Crea un archivo `DR_PLAN.md` en el servidor:

```markdown
# DR Plan - Supabase Production

## Contactos
- DBA: +1-555-0100
- DevOps: +1-555-0101
- CTO: +1-555-0102

## Servidores
- Producción: 203.0.113.10 (Hetzner CPX31)
- Backup: 203.0.113.11 (Hetzner CPX21, réplica)
- DNS: Cloudflare

## Credenciales de emergencia
- Postgres: LastPass #postgres-emergencia
- Servidor: LastPass #server-root

## Pasos de recovery
1. Conectar al servidor de backup
2. Ejecutar: /opt/supabase/scripts/restore-pitr.sh "2024-12-25 14:30:00"
3. Si backup server caído: provisionar nuevo VPS desde snapshot
4. Restaurar DNS a backup IP
5. Verificar health endpoints
6. Notificar en #incidents

## Tiempos
- RPO objetivo: 5 minutos
- RTO objetivo: 2 horas
```

---

## 6. Mantenimiento de Supabase

### Script de actualización

```bash
#!/bin/bash
# /opt/supabase/scripts/update-supabase.sh
set -e

cd /opt/supabase/docker
DATE=$(date +%Y%m%d_%H%M%S)

echo "==> $(date) - Iniciando actualización..."

# 1. Backup preventivo
echo "==> Backup preventivo..."
/opt/supabase/scripts/backup-walg.sh

# 2. Pull de nuevas imágenes
echo "==> Descargando nuevas imágenes..."
docker compose pull

# 3. Recrear servicios (uno por uno para evitar downtime total)
echo "==> Actualizando servicios..."
docker compose up -d --no-deps --force-recreate pgbouncer
sleep 5
docker compose up -d --no-deps --force-recreate gotrue
sleep 5
docker compose up -d --no-deps --force-recreate postgrest
sleep 5
docker compose up -d --no-deps --force-recreate realtime
sleep 5
docker compose up -d --no-deps --force-recreate storage
sleep 5
docker compose up -d --no-deps --force-recreate meta studio
sleep 5
docker compose up -d --no-deps --force-recreate kong

# 4. Limpieza
echo "==> Limpiando imágenes viejas..."
docker image prune -f

# 5. Verificar
echo "==> Verificando servicios..."
docker compose ps

echo "==> $(date) - Actualización completada ✅"
```

### Chequeo de salud periódico

```bash
#!/bin/bash
# /opt/supabase/scripts/health-check.sh

check_endpoint() {
    local name=$1
    local url=$2
    local status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    if [ "$status" -ge 200 ] && [ "$status" -lt 500 ]; then
        echo "✅ $name: $status"
    else
        echo "❌ $name: $status"
    fi
}

echo "=== Health Check: $(date) ==="

# Verificar contenedores
for container in supabase-db supabase-pgbouncer supabase-gotrue supabase-postgrest supabase-realtime supabase-storage supabase-meta supabase-studio supabase-kong; do
    if docker ps --format '{{.Names}}' | grep -q "$container"; then
        echo "✅ $container: running"
    else
        echo "❌ $container: STOPPED"
    fi
done

# Verificar endpoints
check_endpoint "PostgreSQL" "pg://localhost:5432"
check_endpoint "PgBouncer" "pg://localhost:6432"
check_endpoint "Kong" "http://localhost:8000"
check_endpoint "REST API" "http://localhost:54321/rest/v1/"
check_endpoint "Auth" "http://localhost:9999/health"
check_endpoint "Realtime" "http://localhost:4000/"
check_endpoint "Storage" "http://localhost:5000/status"
```

### Alertas recomendadas

| Alerta | Condición | Acción |
|--------|-----------|--------|
| Disk > 85% | Uso de disco | Limpiar logs, expandir volumen |
| WAL-G backup falló | Último backup > 24h | Revisar logs de WAL-G |
| Conexiones DB > 80% pool | `SHOW POOLS` | Aumentar pool size |
| Replication lag > 10s | Diferencia WAL | Revisar realtime |
| Certificado expira < 30d | Fecha de expiración | `certbot renew` |
| Servicio caído | Container stopped | `docker compose up -d` |

---

## 7. Backup del sistema completo

Además de la base de datos, respalda:

```bash
#!/bin/bash
# /opt/supabase/scripts/backup-full-system.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="/opt/supabase/backups/full_system_$DATE"

mkdir -p "$BACKUP_DIR"

# 1. Configuración de Docker
cp /opt/supabase/docker/.env "$BACKUP_DIR/"
cp /opt/supabase/docker/docker-compose.yml "$BACKUP_DIR/"

# 2. Kong config
cp /opt/supabase/docker/volumes/kong/kong.yml "$BACKUP_DIR/"

# 3. Nginx config
cp -r /etc/nginx/sites-available/ "$BACKUP_DIR/nginx/"
cp -r /etc/nginx/sites-enabled/ "$BACKUP_DIR/nginx/"

# 4. Scripts
cp -r /opt/supabase/scripts/ "$BACKUP_DIR/"

# 5. Archivos de storage (si es backend local)
# tar -czf "$BACKUP_DIR/storage.tar.gz" -C /var/lib/storage .

# 6. Comprimir
tar -czf "${BACKUP_DIR}.tar.gz" -C /opt/supabase/backups "full_system_$DATE"
rm -rf "$BACKUP_DIR"

echo "✅ Backup de sistema: ${BACKUP_DIR}.tar.gz"
```

---

## ✅ Checklist de backup y mantenimiento

- [ ] WAL-G instalado y configurado (continuous archiving)
- [ ] Backup full diario automático (cron)
- [ ] Verificación de backups programada (semanal)
- [ ] PITR probado y documentado
- [ ] DR Plan escrito y accesible
- [ ] Script de actualización de Supabase probado
- [ ] Health check automático cada 5 minutos
- [ ] Alertas configuradas (disco, backups, certificados)
- [ ] Backup de sistema (config + scripts) semanal
- [ ] Prueba de restore completa cada mes


---

## 📚 Referencias

- [Supabase | Documentación oficial](https://supabase.com/docs) — Guías, API reference y arquitectura
- [Supabase | CLI reference](https://supabase.com/docs/reference/cli) — Comandos de la CLI de Supabase
- [Supabase | Flutter SDK](https://pub.dev/packages/supabase_flutter) — SDK oficial para Flutter
- [Supabase | Migraciones](https://supabase.com/docs/guides/local-development/migrations) — Gestión de migraciones locales

---

> 📖 **Siguiente:** [06-alternativas-externas.md](./06-alternativas-externas.md)