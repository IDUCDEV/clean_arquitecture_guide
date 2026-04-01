# 04 - Migración de Local a Producción

> Aprende a migrar tu esquema y datos desde el entorno de desarrollo local de Supabase hacia tu instancia de producción.

---

## 🎯 Objetivos de este archivo

- Exportar schema desde local
- Aplicar migraciones a producción
- Migrar datos existentes

---

## 1. Flujo de migración

```
LOCAL ──► PRODUCCIÓN
  │           │
  │  1. push  │
  └───────────►│
              │ 2. aplicar
```

---

## 2. Aplicar migraciones a Supabase Cloud

```bash
# Link al proyecto
supabase link --project-ref tu-project-ref

# Push migraciones
supabase db push --password tu-db-password
```

### Makefile

```makefile
.PHONY: db-push
db-push:
	$(SUPABASE) db push
```

---

## 3. Aplicar a Supabase Self-Hosted

```bash
# Copiar migraciones al servidor
scp supabase/migrations/*.sql tu-servidor:/tmp/

# Aplicar
docker exec -i supabase-db psql -U postgres -d postgres < migration.sql
```

---

## 4. Migrar datos

### Exportar de local

```bash
docker exec -it supabase-db pg_dump -U postgres -t public.users --data-only > users_data.sql
```

### Importar a producción

```bash
docker exec -i supabase-db psql -U postgres -d postgres < users_data.sql
```

---

## ✅ Checklist

- [ ] Migrations exportadas
- [ ] Verificadas sin duplicados
- [ ] Aplicadas a producción
- [ ] Datos migrados (si aplica)

---

**Siguiente**: [05-backup-y-mantenimiento.md](./05-backup-y-mantenimiento.md)