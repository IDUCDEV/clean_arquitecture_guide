# 05 - Triggers y Automatizacion

> Los triggers ejecutan codigo automaticamente cuando ocurre un evento en una tabla. Son el sistema de automatizacion nativo de PostgreSQL.

---

## Que es un trigger

Un **trigger** es una funcion que se ejecuta automaticamente en respuesta a ciertos eventos en una tabla (INSERT, UPDATE, DELETE).

```
┌─────────────────────────────────────────────────┐
│  EVENTO: INSERT INTO users (...) VALUES (...)   │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  BEFORE INSERT TRIGGER                  │    │
│  │  -> Validar datos                       │    │
│  │  -> Modificar NEW                       │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  PostgreSQL ejecuta el INSERT           │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  AFTER INSERT TRIGGER                   │    │
│  │  -> Actualizar otra tabla               │    │
│  │  -> Enviar notificacion                 │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

**Fuente:** PostgreSQL 18 Documentation, Cap. 41.10 Trigger Functions

---

## Crear un trigger: 2 pasos

### Paso 1: Crear la funcion trigger

```sql
-- La funcion DEBE retornar TRIGGER
CREATE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Paso 2: Crear el trigger

```sql
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();
```

**Componentes de CREATE TRIGGER:**

```sql
CREATE TRIGGER nombre_trigger
    {BEFORE | AFTER | INSTEAD OF}
    {INSERT | UPDATE | DELETE}
    ON nombre_tabla
    [FOR EACH ROW | FOR EACH STATEMENT]
    [WHEN (condicion)]
    EXECUTE FUNCTION nombre_funcion();
```

---

## BEFORE vs AFTER

| Momento | Cuando se ejecuta | Puede modificar datos | Uso comun |
|---------|-------------------|:--------------------:|-----------|
| `BEFORE` | Antes de la operacion | Si (modificar `NEW`) | Validacion, sanitizacion |
| `AFTER` | Despues de la operacion | No | Auditoria, notificaciones |
| `INSTEAD OF` | Reemplaza la operacion | No (en vistas) | Vistas updatable |

```sql
-- BEFORE: puede modificar los datos antes de insertar
CREATE FUNCTION sanitize_email()
RETURNS TRIGGER AS $$
BEGIN
    NEW.email = LOWER(TRIM(NEW.email));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sanitize_email
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION sanitize_email();
```

---

## ROW-level vs STATEMENT-level

| Nivel | Se ejecuta | Ejemplo |
|-------|-----------|---------|
| `FOR EACH ROW` | Una vez por fila afectada | 10 INSERTs = 10 ejecuciones |
| `FOR EACH STATEMENT` | Una vez por sentencia SQL | 10 INSERTs = 1 ejecucion |

```sql
-- ROW-level (default para BEFORE/AFTER)
CREATE TRIGGER trg_row_level
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION log_change();

-- STATEMENT-level
CREATE TRIGGER trg_stmt_level
AFTER INSERT ON users
FOR EACH STATEMENT
EXECUTE FUNCTION log_batch_change();
```

---

## Variables especiales

### NEW y OLD

```sql
CREATE FUNCTION audit_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- NEW: la nueva fila (INSERT y UPDATE)
    -- OLD: la fila anterior (UPDATE y DELETE)

    IF TG_OP = 'INSERT' THEN
        RAISE NOTICE 'Nueva fila: %', NEW;
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        RAISE NOTICE 'Antes: %, Despues: %', OLD, NEW;
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        RAISE NOTICE 'Fila eliminada: %', OLD;
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### TG_OP, TG_TABLE_NAME, TG_ARGV

| Variable | Descripcion | Tipo |
|----------|-------------|------|
| `NEW` | Fila nueva (INSERT/UPDATE) | RECORD |
| `OLD` | Fila anterior (UPDATE/DELETE) | RECORD |
| `TG_OP` | Operacion: 'INSERT', 'UPDATE', 'DELETE' | TEXT |
| `TG_TABLE_NAME` | Nombre de la tabla | TEXT |
| `TG_TABLE_SCHEMA` | Schema de la tabla | TEXT |
| `TG_ARGV` | Argumentos pasados al trigger | TEXT[] |

```sql
-- TG_ARGV: pasar argumentos al trigger
CREATE FUNCTION log_with_prefix()
RETURNS TRIGGER AS $$
BEGIN
    RAISE NOTICE '[%] % en tabla %',
        TG_ARGV[0],  -- Primer argumento
        TG_OP,
        TG_TABLE_NAME;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger con argumentos
CREATE TRIGGER trg_log
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION log_with_prefix('AUDIT');
```

---

## Patron 1: Auto-update updated_at

El trigger mas comun en Supabase:

```sql
-- Funcion
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para la tabla users
CREATE TRIGGER set_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Trigger para la tabla posts
CREATE TRIGGER set_posts_updated_at
BEFORE UPDATE ON posts
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Ahora updated_at se actualiza automaticamente
UPDATE users SET name = 'Ana' WHERE id = '...';
-- updated_at se actualiza sin que lo especifiques
```

---

## Patron 2: Audit trail (registro de cambios)

```sql
-- Tabla de auditoria
CREATE TABLE audit_log (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id UUID NOT NULL,
    action TEXT NOT NULL,  -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by UUID DEFAULT auth.uid(),
    changed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Funcion de auditoria
CREATE OR REPLACE FUNCTION audit_trigger_func()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (table_name, record_id, action, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW));
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (table_name, record_id, action, old_data)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Aplicar a multiples tablas
CREATE TRIGGER audit_users
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

CREATE TRIGGER audit_orders
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();

CREATE TRIGGER audit_products
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION audit_trigger_func();
```

---

## Patron 3: Validar datos antes de insertar

```sql
-- Funcion: validar email antes de insertar
CREATE OR REPLACE FUNCTION validate_user_email()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar formato basico
    IF NEW.email !~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' THEN
        RAISE EXCEPTION 'Formato de email invalido: %', NEW.email;
    END IF;

    -- Verificar que no este en lista de emails prohibidos
    IF EXISTS (SELECT 1 FROM forbidden_emails WHERE email = LOWER(NEW.email)) THEN
        RAISE EXCEPTION 'Email no permitido: %', NEW.email;
    END IF;

    -- Sanitizar
    NEW.email = LOWER(TRIM(NEW.email));

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_email
BEFORE INSERT OR UPDATE OF email ON users
FOR EACH ROW
EXECUTE FUNCTION validate_user_email();
```

---

## Patron 4: Prevenir operaciones

```sql
-- Funcion: prevenir DELETE en tablas criticas
CREATE OR REPLACE FUNCTION prevent_delete()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Operacion DELETE no permitida en tabla %', TG_TABLE_NAME;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Aplicar a tablas criticas
CREATE TRIGGER trg_prevent_delete_users
BEFORE DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION prevent_delete();

-- Ahora intentar eliminar un usuario falla:
DELETE FROM users WHERE id = '...';
-- ERROR: Operacion DELETE no permitida en tabla users
```

**Variante: prevenir DELETE solo en ciertas condiciones:**

```sql
CREATE OR REPLACE FUNCTION prevent_delete_critical()
RETURNS TRIGGER AS $$
BEGIN
    -- Solo prevenir si el registro tiene dependencias
    IF EXISTS (SELECT 1 FROM orders WHERE user_id = OLD.id) THEN
        RAISE EXCEPTION 'No se puede eliminar usuario con ordenes activas';
    END IF;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_delete_user_with_orders
BEFORE DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION prevent_delete_critical();
```

---

## Transition Tables: REFERENCING

Disponible desde PostgreSQL 10+. Permite acceder a todas las filas afectadas en un trigger STATEMENT-level:

```sql
-- Funcion que usa transition tables
CREATE OR REPLACE FUNCTION log_bulk_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- NEW_TABLE: todas las filas nuevas
    -- OLD_TABLE: todas las filas anteriores

    INSERT INTO bulk_audit (table_name, action, affected_count)
    SELECT TG_TABLE_NAME, TG_OP, COUNT(*)
    FROM NEW_TABLE;

    RETURN NULL;  -- Para AFTER triggers, RETURN NULL
END;
$$ LANGUAGE plpgsql;

-- Trigger con transition tables
CREATE TRIGGER trg_bulk_audit
AFTER INSERT ON orders
REFERENCING NEW TABLE AS NEW_TABLE
FOR EACH STATEMENT
EXECUTE FUNCTION log_bulk_changes();
```

---

## WHEN clause: ejecucion condicional

```sql
-- Solo ejecutar el trigger cuando se cumpla una condicion
CREATE TRIGGER trg_log_price_change
AFTER UPDATE OF price ON products
FOR EACH ROW
WHEN (OLD.price IS DISTINCT FROM NEW.price)  -- Solo si el precio cambio
EXECUTE FUNCTION log_price_change();

-- Solo para usuarios activos
CREATE TRIGGER trg_validate_active_user
BEFORE INSERT ON orders
FOR EACH ROW
WHEN (NEW.status = 'active')  -- Solo para ordenes activas
EXECUTE FUNCTION validate_user_for_order();
```

---

## Gestion de triggers

```sql
-- Listar triggers de una tabla
SELECT
    trigger_name,
    event_manipulation,
    action_timing,
    action_statement
FROM information_schema.triggers
WHERE event_object_table = 'users';

-- Deshabilitar un trigger
ALTER TABLE users DISABLE TRIGGER trg_validate_email;

-- Habilitar un trigger
ALTER TABLE users ENABLE TRIGGER trg_validate_email;

-- Deshabilitar TODOS los triggers de una tabla
ALTER TABLE users DISABLE TRIGGER ALL;

-- Eliminar un trigger
DROP TRIGGER IF EXISTS trg_validate_email ON users;

-- Eliminar la funcion trigger
DROP FUNCTION IF EXISTS validate_user_email();
```

---

## Ejemplo completo: sistema de auditoria

```sql
-- 1. Tabla de auditoria
CREATE TABLE audit_trail (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_data JSONB,
    new_data JSONB,
    user_id UUID DEFAULT auth.uid(),
    ip_address INET,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Index para busquedas rapidas
CREATE INDEX idx_audit_table ON audit_trail (table_name);
CREATE INDEX idx_audit_record ON audit_trail (record_id);
CREATE INDEX idx_audit_created ON audit_trail (created_at);

-- 3. Funcion de auditoria generica
CREATE OR REPLACE FUNCTION generic_audit_func()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_trail (table_name, record_id, action, new_data)
        VALUES (TG_TABLE_NAME, NEW.id::TEXT, 'INSERT', to_jsonb(NEW));
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_trail (table_name, record_id, action, old_data, new_data)
        VALUES (TG_TABLE_NAME, NEW.id::TEXT, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW));
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO audit_trail (table_name, record_id, action, old_data)
        VALUES (TG_TABLE_NAME, OLD.id::TEXT, 'DELETE', to_jsonb(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 4. Aplicar a multiples tablas
CREATE TRIGGER audit_users
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW EXECUTE FUNCTION generic_audit_func();

CREATE TRIGGER audit_orders
AFTER INSERT OR UPDATE OR DELETE ON orders
FOR EACH ROW EXECUTE FUNCTION generic_audit_func();

CREATE TRIGGER audit_products
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION generic_audit_func();

-- 5. Query para ver historial de un registro
SELECT * FROM audit_trail
WHERE table_name = 'users' AND record_id = 'uuid-del-usuario'
ORDER BY created_at DESC;

-- 6. Query para ver todos los cambios de un usuario
SELECT * FROM audit_trail
WHERE user_id = 'uuid-del-usuario'
ORDER BY created_at DESC;
```

---

## Resumen de triggers

```
┌──────────────────────────────────────────────────────┐
│              TRIGGERS EN POSTGRESQL                  │
├──────────────────────────────────────────────────────┤
│  BEFORE  -> Antes de la operacion (modificar NEW)   │
│  AFTER   -> Despues (auditoria, notificaciones)     │
│  ROW     -> Una vez por fila                         │
│  STATEMENT -> Una vez por sentencia                  │
│  WHEN    -> Condicion de ejecucion                   │
│  NEW/OLD -> Acceso a filas                           │
│  TG_OP   -> Tipo de operacion                       │
│  TRANSITION TABLES -> Acceso a multiples filas      │
└──────────────────────────────────────────────────────┘
```

---

**Siguiente:** [06 - JSONB y Busqueda de Texto](06-jsonb-busqueda-texto.md)
