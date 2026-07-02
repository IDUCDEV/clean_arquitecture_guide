# 04 - Migración de Local a Producción

> Aprende a migrar tu esquema y datos desde el entorno de desarrollo local de Supabase hacia tu instancia de producción, con estrategias de zero-downtime y rollback.

---

## 🎯 Objetivos de este archivo

- Comparar schemas entre local y producción con `supabase db diff`
- Usar branches (preview environments) para cambios seguros
- Estrategias de migración zero-downtime
- Resolver conflictos de migraciones
- Rollback y recuperación ante fallos

---

## 1. Flujo de migración completo

```
DESARROLLO                STAGING                  PRODUCCIÓN
┌──────────┐    push      ┌──────────┐    link     ┌──────────┐
│  Local   │ ──────────►  │ Branch   │ ──────────► │   Prod   │
│ supabase │              │ (preview)│              │  Cloud   │
│ start    │              │          │              │          │
└──────────┘              └──────────┘              └──────────┘
     │                          │                        │
     │ db diff                  │ db diff                 │ db push
     │ (antes de push)          │ (vs prod)               │ (después
     ▼                          ▼                         ▼  de review)
  migration/               validación                esquema
  archivo.sql              + tests                   actualizado
```

### Herramientas disponibles

| Comando | Propósito |
|---------|-----------|
| `supabase db diff` | Comparar schema actual contra migraciones |
| `supabase db push` | Aplicar migraciones a linked project |
| `supabase link` | Vincular proyecto local con remoto |
| `supabase branch` | Crear/administrar preview branches |

---

## 2. Comparar schemas con `supabase db diff`

El comando `db diff` es tu mejor aliado. Te muestra qué cambió antes de aplicar.

### Diff contra migraciones locales

```bash
# ¿Qué cambiaría si ejecuto las migraciones pendientes?
supabase db diff --local

# Ver diff de una tabla específica
supabase db diff --local --schema public --table users

# Diff desde linked project
supabase db diff --linked

# Diff entre dos migraciones
supabase db diff --from 20240101000000 --to 20240102000000
```

### Ejemplo de output

```sql
-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
-- Supabase CLI: Database diff (local)
-- * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

-- Nuevas tablas
CREATE TABLE IF NOT EXISTS "public"."profiles" (
    "id" uuid NOT NULL DEFAULT gen_random_uuid(),
    "username" text NOT NULL,
    "avatar_url" text,
    "created_at" timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT "profiles_pkey" PRIMARY KEY ("id")
);

-- Nuevas políticas
CREATE POLICY "Users can view own profile" ON "public"."profiles"
    AS PERMISSIVE FOR SELECT
    TO authenticated
    USING (auth.uid() = id);
```

### Integrar en CI/CD

```yaml
# .github/workflows/check-migrations.yml
name: Check Migration Drift

on:
  pull_request:
    paths: [supabase/migrations/**]

jobs:
  check-drift:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1
      
      - name: Start local Supabase
        run: supabase start
      
      - name: Check for drift
        run: |
          DRIFT=$(supabase db diff --local)
          if [ -n "$DRIFT" ]; then
            echo "⚠️ Migration drift detected:"
            echo "$DRIFT"
            exit 1
          fi
          echo "✅ No drift detected"
```

---

## 3. Branch Workflow (Preview Environments)

`supabase branch` permite crear bases de datos temporales para tests.

### Crear y usar branches

```bash
# Crear branch local (basada en producción)
supabase branch create feature-x

# Cambiar a la branch
supabase branch switch feature-x

# Aplicar migraciones en esta branch
supabase migration up

# Ver branches
supabase branch list

# Eliminar branch
supabase branch delete feature-x
```

### Flujo recomendado

```bash
# 1. Crear branch para feature
supabase branch create feature-orders

# 2. Crear migración
supabase migration new add_orders_table

# 3. Editar migrations/<timestamp>_add_orders_table.sql

# 4. Probar localmente
supabase migration up
supabase db lint --local
supabase test db

# 5. Ver diff contra producción (linked project)
supabase link --project-ref $PROJECT_REF
supabase db diff --linked

# 6. Push a producción
supabase db push --linked --password $DB_PASSWORD

# 7. Limpiar
supabase branch delete feature-orders
```

---

## 4. Migración Zero-Downtime

En producción no puedes permitirte downtime. Sigue estas estrategias:

### 4.1 Agregar columna (safe)

```sql
-- ✅ SEGURO: sin defaults que lockeen la tabla
ALTER TABLE public.orders ADD COLUMN IF NOT EXISTS notes TEXT;

-- ⚠️ RIESGO: default en columna NOT NULL lockea la tabla completa
-- En tablas grandes (>100k rows) usa este approach:
ALTER TABLE public.orders ADD COLUMN IF NOT EXISTS notes TEXT;
-- Luego en otro deploy:
-- ALTER TABLE public.orders ALTER COLUMN notes SET DEFAULT '';
-- ALTER TABLE public.orders ALTER COLUMN notes SET NOT NULL;
```

### 4.2 Renombrar columna (safe)

```sql
-- ❌ PELIGRO: renombrar rompe queries en producción
ALTER TABLE public.orders RENAME COLUMN status TO order_status;

-- ✅ SEGURO: migración en 3 fases
-- FASE 1: Agregar nueva columna
ALTER TABLE public.orders ADD COLUMN order_status TEXT;
UPDATE public.orders SET order_status = status;

-- FASE 2 (deploy código): app usa ambas columnas, escribe en ambas

-- FASE 3 (después de deploy): eliminar columna vieja
ALTER TABLE public.orders DROP COLUMN status;
```

### 4.3 Agregar índice con CONCURRENTLY

```sql
-- ✅ SEGURO: no lockea escritura
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_id ON public.orders(user_id);

-- ❌ PELIGRO: lockea la tabla
CREATE INDEX idx_orders_user_id ON public.orders(user_id);
```

### 4.4 Migraciones con datos grandes

```sql
-- Para tablas con millones de filas:
-- 1. Agregar columna nullable
ALTER TABLE public.products ADD COLUMN search_vector tsvector;

-- 2. Poblar en batches (no en transacción)
-- Ejecutar varias veces hasta cubrir todo:
UPDATE public.products 
SET search_vector = to_tsvector('spanish', name || ' ' || description)
WHERE search_vector IS NULL
LIMIT 10000;

-- 3. Agregar índice
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_products_search ON public.products USING gin(search_vector);
```

### 4.5 Deploy de código vs schema

Siempre separa en fases:

```
FASE 1 (solo schema)
├── Agregar nuevas columnas (nullable)
├── Crear índices (CONCURRENTLY)
├── Crear nuevas tablas
└── No modificar columnas existentes

FASE 2 (deploy app)
├── Nuevo código deployado
├── App escribe en columnas nuevas
└── Rolling update (sin downtime)

FASE 3 (cleanup)
├── Eliminar columnas viejas
├── Agregar NOT NULL a nuevas columnas
└── Eliminar índices viejos
```

---

## 5. Conflictos de migraciones

### Causas comunes

| Causa | Síntoma | Solución |
|-------|---------|----------|
| **Reordenamiento** | Dos developers crean migraciones con timestamp similar | Renombrar archivo con timestamp correcto |
| **Merge conflict** | Git conflict en migraciones | Editar archivo SQL directamente |
| **State drift** | Schema local difiere del remoto | `supabase db diff --linked` para ver diferencias |
| **Migration ya aplicada** | Error "relation already exists" | No re-aplicar migraciones existentes |

### Resolver conflictos

```bash
# 1. Ver migraciones aplicadas en remoto
supabase migration list

# 2. Ver estado actual
supabase db diff --linked

# 3. Si hay drift, crear migration de reparación
supabase migration new fix_drift

# 4. Verificar que todo está en sync
supabase db diff --linked  # debe dar empty
```

### Reparación manual

```sql
-- Si una migración falló a medio camino:
-- 1. Marcar como aplicada sin ejecutar
supabase migration repair <status|timestamp>

-- 2. O forzar re-ejecución
supabase migration repair --status reverted <timestamp>
supabase migration up
```

---

## 6. Migrar datos con pg_dump/pg_restore

### Exportar datos seleccionados (no schema)

```bash
# Exportar solo datos de tablas específicas
docker exec -t supabase-db pg_dump \
  -U postgres \
  -d postgres \
  --data-only \
  --table=public.orders \
  --table=public.products \
  --table=public.categories \
  -F c \
  > migrations/data_dump.dump
```

### Migrar con transformación

```sql
-- Si el schema de producción es diferente, transforma durante la migración:
INSERT INTO public.orders_new (id, user_id, total, status, created_at)
SELECT 
    id, 
    customer_id AS user_id, 
    amount AS total, 
    CASE WHEN paid THEN 'completed' ELSE 'pending' END AS status,
    created_at
FROM public.orders_old
ON CONFLICT (id) DO NOTHING;
```

### Verificar integridad post-migración

```sql
-- Comparar conteos
SELECT 'orders' AS tbl, count(*) FROM public.orders_old
UNION ALL
SELECT 'orders' AS tbl, count(*) FROM public.orders_new;

-- Verificar checksum (opcional)
SELECT count(*) AS total, sum(hashtextextended(row()::text, 0)) AS checksum 
FROM public.orders_old;
SELECT count(*) AS total, sum(hashtextextended(row()::text, 0)) AS checksum 
FROM public.orders_new;
```

---

## 7. Rollback

### Rollback de migración

```bash
# Ver migraciones aplicadas
supabase migration list

# Revertir la última migración
supabase db push --linked --password $DB_PASSWORD --version <timestamp-anterior>

# O hacerlo manual en psql
# 1. Crear SQL de reversión
# 2. Ejecutar en producción
# 3. Ajustar la tabla de migraciones
```

### Escribir migraciones reversibles

```sql
-- migrations/20240101000000_add_orders_table.up.sql
-- UP
CREATE TABLE public.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    total DECIMAL(10,2) NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- migrations/20240101000000_add_orders_table.down.sql
-- DOWN (rollback)
DROP TABLE IF EXISTS public.orders;
```

### Makefile con rollback

```makefile
.PHONY: db-rollback
db-rollback: ## Revertir última migración
	$(SUPABASE) db push --linked --password $(SUPABASE_DB_PASSWORD) --version $(shell ls -1 supabase/migrations/ | tail -2 | head -1 | cut -d'_' -f1)

.PHONY: db-diff
db-diff: ## Ver diff contra linked project
	$(SUPABASE) db diff --linked

.PHONY: db-check
db-check: ## Verificar que no hay drift
	@DRIFT=$$($(SUPABASE) db diff --linked); \
	if [ -n "$$DRIFT" ]; then \
		echo "⚠️ Drift detectado:"; \
		echo "$$DRIFT"; \
		exit 1; \
	fi; \
	echo "✅ Sin drift"
```

---

## 8. Plan de release con migraciones

### Release checklist

```yaml
PRE-RELEASE (24h antes)
├── [ ] Run db diff contra producción → sin drift
├── [ ] Run supabase test db → todos pasando
├── [ ] Run supabase db lint --linked → 0 errores
├── [ ] Backup de producción (pg_dump + WAL-G)
├── [ ] Review de migration SQL por otro developer

DEPLOY
├── [ ] Aplicar migraciones en transacción
├── [ ] Verificar conectividad de servicios
├── [ ] Deploy de app (rolling update)
├── [ ] Monitorear errores (5 min)
├── [ ] Verificar health endpoints

POST-RELEASE (1h después)
├── [ ] Confirmar que no hay deadlocks
├── [ ] Revisar logs de errores
├── [ ] Monitorear métricas de rendimiento
└── [ ] ¿Necesario rollback?
```

---

## ✅ Checklist de migración

- [ ] `supabase db diff --linked` verificado
- [ ] Migraciones probadas localmente
- [ ] `supabase test db` pasando
- [ ] `supabase db lint` sin errores
- [ ] Backup de producción previo
- [ ] Rollback planeado (down migration)
- [ ] Release en fases (schema → app → cleanup)
- [ ] Monitoreo post-deploy activo

---

**Siguiente**: [05-backup-y-mantenimiento.md](./05-backup-y-mantenimiento.md)
