# 05 - Backup y Mantenimiento

> Aprende a implementar estrategias de backup, restaurar datos y mantener tu instancia de Supabase en producción de forma segura.

---

## 🎯 Objetivos

- Implementar estrategia de backups automatizados
- Crear scripts de restore
- Mantener Supabase actualizado
- Monitorear salud del sistema

---

## 1. Estrategias de backup

| Tipo | Frecuencia | Retención | Uso |
|------|------------|-----------|-----|
| **Full** | Diario | 30 días | Restauración completa |
| **Incremental** | Cada 6 horas | 7 días | Recuperación rápida |
| **Export** | Semanal | 90 días | Archivado |

---

## 2. Script de backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/opt/supabase/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_CONTAINER="supabase-db"

mkdir -p $BACKUP_DIR
docker exec $DB_CONTAINER pg_dump -U postgres -Fc postgres > $BACKUP_DIR/full_backup_$DATE.dump
gzip $BACKUP_DIR/full_backup_$DATE.dump
find $BACKUP_DIR -name "*.dump.gz" -mtime +30 -delete
```

Programar con cron:
```bash
crontab -e
0 2 * * * /opt/supabase/scripts/backup.sh
```

---

## 3. Script de restore

```bash
#!/bin/bash
# restore.sh

if [ -z "$1" ]; then
    echo "Usage: $0 <backup-file>"
    exit 1
fi

docker exec -i supabase-db pg_restore -U postgres -d postgres -c <(gunzip -c $1)
```

---

## 4. Monitoreo

```bash
# Ver estado
docker ps
docker exec -it supabase-db psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

---

**Siguiente**: [06-alternativas-externas.md](./06-alternativas-externas.md)