# 08 - Cheatsheet PostgreSQL

> Referencia rapida de todo lo esencial de PostgreSQL para Supabase. Imprime esto o guardalo como bookmark.

---

## Funciones especificas de PostgreSQL

| Funcion | Descripcion | Ejemplo |
|---------|-------------|---------|
| `gen_random_uuid()` | UUID v4 aleatorio | `DEFAULT gen_random_uuid()` |
| `NOW()` | Fecha/hora actual | `WHERE created_at > NOW() - INTERVAL '7 days'` |
| `ILIKE` | Busqueda case-insensitive | `WHERE name ILIKE '%ana%'` |
| `GREATEST(a, b)` | Valor maximo | `GREATEST(price, 0)` |
| `LEAST(a, b)` | Valor minimo | `LEAST(score, 100)` |
| `COALESCE(a, b)` | Primer no-NULL | `COALESCE(name, 'Sin nombre')` |
| `NULLIF(a, b)` | NULL si son iguales | `NULLIF(divisor, 0)` |
| `date_trunc('month', f)` | Truncar fecha | `date_trunc('month', NOW())` |
| `extract(YEAR FROM f)` | Componente de fecha | `extract(YEAR FROM created_at)` |
| `age(f1, f2)` | Diferencia fechas | `age(NOW(), birth_date)` |
| `interval '7 days'` | Intervalo de tiempo | `NOW() - INTERVAL '30 days'` |
| `generate_series(1, n)` | Serie de numeros | `FROM generate_series(1, 10)` |

---

## Operadores JSONB

| Operador | Descripcion | Ejemplo |
|----------|-------------|---------|
| `->` | Obtener campo (JSONB) | `data->'name'` |
| `->>` | Obtener campo (TEXT) | `data->>'name'` |
| `@>` | Contiene | `data @> '{"a":1}'` |
| `<@` | Contenido en | `'{"a":1}' <@ data` |
| `?` | Key existe | `data ? 'name'` |
| `?\|` | Cualquier key | `data ?\| ARRAY['a','b']` |
| `?&` | Todas las keys | `data ?& ARRAY['a','b']` |
| `\|\|` | Merge | `data \|\| '{"b":2}'` |
| `-` | Eliminar key | `data - 'name'` |
| `#-` | Eliminar por ruta | `data #- ARRAY['a','b']` |
| `jsonb_set()` | Actualizar valor | `jsonb_set(d, '{a}', '"x"')` |
| `jsonb_build_object()` | Construir objeto | `jsonb_build_object('k','v')` |
| `jsonb_array_elements()` | Expandir array | `jsonb_array_elements(data->'arr')` |
| `jsonb_object_keys()` | Obtener keys | `jsonb_object_keys(data)` |

---

## Full-text Search

| Elemento | Funcion | Ejemplo |
|----------|---------|---------|
| tsvector | Texto a searchable | `to_tsvector('spanish', 'hola mundo')` |
| tsquery | Construir busqueda | `to_tsquery('spanish', 'hola & mundo')` |
| plainto_tsquery | Query simple | `plainto_tsquery('spanish', 'hola mundo')` |
| phraseto_tsquery | Buscar frase | `phraseto_tsquery('spanish', 'hola mundo')` |
| @@ | Matching | `tsvector @@ tsquery` |
| ts_rank | Ranking | `ts_rank(vector, query)` |
| ts_rank_cd | Ranking cobertura | `ts_rank_cd(vector, query)` |
| similarity | pg_trgm | `similarity('hola', 'holamundo')` |
| `%` | Operador pg_trgm | `WHERE name % 'hola'` |

---

## Templates PL/pgSQL

### Funcion basica

```sql
CREATE OR REPLACE FUNCTION nombre_funcion(param1 TIPO, param2 TIPO)
RETURNS TIPO_RETORNO AS $$
DECLARE
    variable TIPO;
BEGIN
    -- Logica aqui
    SELECT columna INTO variable FROM tabla WHERE condicion;
    RETURN variable;
END;
$$ LANGUAGE plpgsql;
```

### Trigger function

```sql
CREATE OR REPLACE FUNCTION nombre_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        -- Logica para INSERT
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        -- Logica para UPDATE
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        -- Logica para DELETE
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### RPC function (Supabase)

```sql
CREATE OR REPLACE FUNCTION nombre_rpc(param1 TIPO DEFAULT valor)
RETURNS JSONB AS $$
BEGIN
    -- Logica de negocio
    RETURN jsonb_build_object(
        'success', true,
        'data', resultado
    );

EXCEPTION
    WHEN OTHERS THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', SQLERRM
        );
END;
$$ LANGUAGE plpgsql;
```

---

## EXPLAIN: flags y lectura

### Flags disponibles

| Flag | Descripcion |
|------|-------------|
| `ANALYZE` | Ejecutar la consulta y mostrar tiempos reales |
| `BUFFERS` | Mostrar uso de buffers (con ANALYZE) |
| `VERBOSE` | Mostrar informacion adicional |
| `COSTS` | Mostrar costos estimados (default: on) |
| `FORMAT` | Formato: TEXT, JSON, XML, YAML |

### Ejemplos

```sql
-- Basico
EXPLAIN SELECT * FROM users WHERE id = '123';

-- Con analisis real
EXPLAIN ANALYZE SELECT * FROM users WHERE id = '123';

-- Con buffers (muestra memoria)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT * FROM users WHERE id = '123';

-- En formato JSON (para parsing programatico)
EXPLAIN (ANALYZE, FORMAT JSON) SELECT * FROM users WHERE id = '123';
```

### Interpretar salida

```
Index Scan using users_pkey on users  (cost=0.43..8.45 rows=1 width=128)
                                      ^^^^^^^^^^^^^^^^^^^^
                                      costo_estimado..costo_final rows=filas width=bytes

  Index Cond: (id = '123'::uuid)
              ^^^^^^^^^^^^^^^^
              condicion que usa el index

Planning Time: 0.085 ms       -- Tiempo de planificacion
Execution Time: 0.124 ms      -- Tiempo de ejecucion real
```

**Tipos de escaneo:**

| Tipo | Significado | Velocidad |
|------|-------------|-----------|
| `Seq Scan` | Escanea toda la tabla | Lento |
| `Index Scan` | Usa un index B-tree | Rapido |
| `Index Only Scan` | Todo en el index | Muy rapido |
| `Bitmap Index Scan` | Multiples matches del index | Rapido |
| `Bitmap Heap Scan` | Recuperacion por bitmap | Rapido |

---

## Extensiones utiles

| Extension | Proposito | Instalar |
|-----------|-----------|----------|
| `pg_trgm` | Busqueda difusa (% similarity) | `CREATE EXTENSION pg_trgm` |
| `unaccent` | Quitar tildes | `CREATE EXTENSION unaccent` |
| `pgcrypto` | Hash, encriptacion | `CREATE EXTENSION pgcrypto` |
| `uuid-ossp` | UUIDs (alternativa a gen_random_uuid) | `CREATE EXTENSION "uuid-ossp"` |
| `btree_gist` | Necesaria para EXCLUDE | `CREATE EXTENSION btree_gist` |
| `pg_stat_statements` | Estadisticas de queries | `CREATE EXTENSION pg_stat_statements` |
| `pg_partman` | particionamiento automatico | `CREATE EXTENSION pg_partman` |

---

## System catalogs utiles

### pg_stat_activity: conexiones activas

```sql
-- Ver conexiones activas
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    LEFT(query, 80) AS query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY query_start;
```

### pg_indexes: todos los indexes

```sql
-- Indexes de una tabla
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users';

-- Todos los indexes del schema public
SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename;
```

### pg_policies: politicas RLS

```sql
-- Politicas de una tabla
SELECT
    policyname,
    permissive,
    roles,
    cmd,
    qual AS using_expression,
    with_check AS check_expression
FROM pg_policies
WHERE tablename = 'users';
```

---

## Queries utiles

### Tamano de tablas

```sql
-- Tamano de todas las tablas
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_indexes_size(schemaname||'.'||tablename::regclass)) AS index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Queries lentos

```sql
-- Queries mas lentas (requiere pg_stat_statements)
SELECT
    LEFT(query, 100) AS query,
    calls,
    total_exec_time AS total_ms,
    mean_exec_time AS avg_ms,
    rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

### Conexiones activas

```sql
-- Conexiones por usuario
SELECT
    usename,
    COUNT(*) AS connections,
    state
FROM pg_stat_activity
GROUP BY usename, state
ORDER BY connections DESC;
```

### locks

```sql
-- Bloqueos activos
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.relation = blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

---

## Supabase-specific

### auth.uid(): ID del usuario actual

```sql
-- Obtener el ID del usuario autenticado
SELECT auth.uid();

-- Usar en una funcion
CREATE OR REPLACE FUNCTION get_my_profile()
RETURNS JSONB AS $$
BEGIN
    RETURN (
        SELECT jsonb_build_object('id', id, 'name', name, 'email', email)
        FROM users
        WHERE id = auth.uid()
    );
END;
$$ LANGUAGE plpgsql SECURITY INVOKER;
```

### auth.jwt(): JWT del usuario actual

```sql
-- Obtener claims del JWT
SELECT auth.jwt();

-- Obtener un claim especifico
SELECT auth.jwt() ->> 'email';
SELECT auth.jwt() ->> 'role';

-- Usar en una politica RLS
CREATE POLICY "users_select_own" ON users
FOR SELECT USING (id = auth.uid());

-- Usar en una funcion
CREATE OR REPLACE FUNCTION get_my_email()
RETURNS TEXT AS $$
BEGIN
    RETURN auth.jwt() ->> 'email';
END;
$$ LANGUAGE plpgsql;
```

### storage helpers

```sql
-- Crear bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);

-- Politica: usuario puede subir a su propia carpeta
CREATE POLICY "avatar_upload" ON storage.objects
FOR INSERT WITH CHECK (
    bucket_id = 'avatars'
    AND (storage.foldername(name))[1] = auth.uid()::text
);

-- Politica: cualquiera puede ver avatares
CREATE POLICY "avatar_read" ON storage.objects
FOR SELECT USING (bucket_id = 'avatars');
```

---

## Performance tuning basico

### autovacuum

```sql
-- Ver estado de autovacuum
SELECT
    relname,
    n_dead_tup,
    last_autovacuum,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY n_dead_tup DESC;

-- Forzar vacuum en una tabla
VACUUM ANALYZE users;
```

### work_mem

```sql
-- Ver work_mem actual
SHOW work_mem;

-- Aumentar para una sesion (no global)
SET work_mem = '256MB';

-- Para consultas con sort/hash grandes
SET LOCAL work_mem = '512MB';
```

### shared_buffers

```sql
-- Ver shared_buffers actual
SHOW shared_buffers;

-- Recomendado: 25% de la RAM del servidor
-- Ejemplo: servidor con 8GB RAM -> shared_buffers = 2GB
-- Esto se configura en postgresql.conf, no se puede cambiar en runtime
```

---

## Operadores de comparacion utiles

| Operador | Descripcion | Ejemplo |
|----------|-------------|---------|
| `=` | Igual | `WHERE id = 1` |
| `<>` o `!=` | Diferente | `WHERE status <> 'deleted'` |
| `>` / `<` | Mayor / Menor | `WHERE price > 100` |
| `>=` / `<=` | Mayor/Menor igual | `WHERE age >= 18` |
| `BETWEEN` | Rango | `WHERE price BETWEEN 10 AND 50` |
| `IN` | Lista | `WHERE status IN ('a','b','c')` |
| `NOT IN` | No en lista | `WHERE id NOT IN (1,2,3)` |
| `IS NULL` | Es NULL | `WHERE deleted_at IS NULL` |
| `IS NOT NULL` | No es NULL | `WHERE email IS NOT NULL` |
| `LIKE` | Patron (case-sensitive) | `WHERE name LIKE '%ana%'` |
| `ILIKE` | Patron (case-insensitive) | `WHERE name ILIKE '%ana%'` |
| `~` | Regex (case-sensitive) | `WHERE email ~ '@gmail'` |
| `~*` | Regex (case-insensitive) | `WHERE email ~* '@gmail'` |
| `ANY` | Cualquier elemento | `WHERE id = ANY(ARRAY[1,2,3])` |

---

## Quick reference: LIMIT / OFFSET / ORDER BY

```sql
-- Paginacion basica
SELECT * FROM users ORDER BY created_at DESC
LIMIT 20 OFFSET 0;    -- Pagina 1

SELECT * FROM users ORDER BY created_at DESC
LIMIT 20 OFFSET 20;   -- Pagina 2;

-- Cursor-based (mas eficiente para paginas altas)
SELECT * FROM users
WHERE created_at < '2026-07-01'
ORDER BY created_at DESC
LIMIT 20;
```

---

## Resumen

```
┌──────────────────────────────────────────────────────┐
│           CHEATSHEET POSTGRESQL                      │
├──────────────────────────────────────────────────────┤
│  Funciones:  gen_random_uuid, NOW, ILIKE, GREATEST  │
│  JSONB:      ->, ->>, @>, ?, jsonb_set               │
│  FTS:        to_tsvector, @@, ts_rank                 │
│  EXPLAIN:    ANALYZE BUFFERS FORMAT TEXT              │
│  Auth:       auth.uid(), auth.jwt()                   │
│  Catalogs:   pg_stat_activity, pg_indexes             │
│  Tuning:     VACUUM ANALYZE, work_mem                │
└──────────────────────────────────────────────────────┘
```

---

**Fin del Submodulo 2: PostgreSQL Especifico**
