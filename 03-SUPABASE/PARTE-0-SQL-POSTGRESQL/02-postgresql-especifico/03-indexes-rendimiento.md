# 03 - Indexes y Rendimiento

> Los indexes son la herramienta mas importante para hacer tus consultas rapidas. Sin ellos, PostgreSQL escanea cada fila de la tabla.

---

## Que es un index

Un **index** es una estructura de datos que permite a PostgreSQL encontrar filas sin escaneo secuencial. Piensa en el indice de un libro:

```
Sin index:                    Con index:
┌──────────────────┐          ┌──────────────────┐
│ Leer cap 1...   │          │ Buscar en indice │
│ Leer cap 2...   │          │ -> Pagina 45     │
│ Leer cap 3...   │          │ Ir directo       │
│ ...             │          └──────────────────┘
│ Leer cap 50     │
│ Encontrado!     │          ~2x mas rapido
└──────────────────┘
   ~50 paginas leidas          ~3 paginas leidas
```

**Fuente:** PostgreSQL 18 Documentation, Cap. 11 Index Types

---

## Tipos de indexes

### B-tree (default)

El index por defecto en PostgreSQL. Funciona para:
- **Igualdad** (`=`, `<>`)
- **Rangos** (`<`, `>`, `<=`, `>=`)
- **ORDER BY**
- **IS NULL / IS NOT NULL**

```sql
-- Crear un B-tree index (implicito por defecto)
CREATE INDEX idx_users_email ON users (email);

-- Equivalente explicito
CREATE INDEX idx_users_email ON users USING btree (email);

-- Cuando buscaras con =
SELECT * FROM users WHERE email = 'ana@test.com';
-- PostgreSQL usa el index automaticamente
```

**Arbol B-tree:**

```
                    [50]
                   /    \
              [25]        [75]
             /    \      /    \
          [10]  [30]  [60]  [80]
          / \    |     |    / \
        [5][15] [28] [55] [70][90]
```

### Hash

Optimizado solo para **igualdad** (`=`). Mas rapido que B-tree para esta operacion:

```sql
-- Crear un Hash index
CREATE INDEX idx_users_email_hash ON users USING hash (email);

-- Solo funciona con =
SELECT * FROM users WHERE email = 'ana@test.com'; -- Usa el index
-- NO funciona con rangos:
SELECT * FROM users WHERE email > 'a'; -- NO usa el index
```

**Comparacion B-tree vs Hash:**

| Operacion | B-tree | Hash |
|-----------|:------:|:----:|
| `=` | Si | Si (mas rapido) |
| `<`, `>`, `<=`, `>=` | Si | No |
| `ORDER BY` | Si | No |
| `IS NULL` | Si | Si |
| Rango de valores | Si | No |

### GIN (Generalized Inverted Index)

Para datos complejos: arrays, JSONB, full-text search:

```sql
-- GIN en JSONB
CREATE INDEX idx_products_data ON products USING gin (data);

-- GIN en arrays
CREATE INDEX idx_products_tags ON products USING gin (tags);

-- GIN en full-text search
CREATE INDEX idx_posts_search ON posts USING gin (search_vector);
```

**Cuando usar GIN:**
- Columnas **JSONB** con consultas `@>` (contains)
- Columnas **array** con consultas `@>` (contains)
- **Full-text search** con `@@` (match)
- Busqueda difusa con `pg_trgm` y `%` (similarity)

### GiST (Generalized Search Tree)

Para datos geometricos, rangos y full-text:

```sql
-- GiST para rangos de tiempo
CREATE INDEX idx_reservations_dates
    ON reservations
    USING gist (daterange(check_in, check_out));

-- GiST para busqueda full-text
CREATE INDEX idx_posts_content
    ON posts
    USING gist (to_tsvector('spanish', content));
```

### BRIN (Block Range Index)

Para tablas **muy grandes** donde los datos tienen un orden natural (timestamps):

```sql
-- BRIN para tablas grandes con timestamps
CREATE INDEX idx_logs_created_brin
    ON logs
    USING brin (created_at);

-- Comparacion de tamano de index:
-- B-tree en tabla de 10M filas: ~200MB
-- BRIN en tabla de 10M filas: ~100KB
```

**BRIN vs B-tree:**

| Caracteristica | B-tree | BRIN |
|----------------|--------|------|
| Tamano del index | Grande | Muy pequeno |
| Velocidad de busqueda | Muy rapida | Rapida (si datos ordenados) |
| Mejor para | Cualquier consulta | Tablas grandes con orden natural |
| Overhead de INSERT | Moderado | Bajo |
| Ideal para | Tablas pequenas/medianas | Tablas de log, time-series |

---

## Composite indexes (multiples columnas)

Un index en multiples columnas. **El orden importa:**

```sql
-- Index compuesto
CREATE INDEX idx_users_email_name ON users (email, name);

-- Esto USA el index (empieza con email):
SELECT * FROM users WHERE email = 'ana@test.com';
SELECT * FROM users WHERE email = 'ana@test.com' AND name = 'Ana';

-- Esto NO usa el index (saltando email):
SELECT * FROM users WHERE name = 'Ana';

-- Regla: las columnas mas usadas en WHERE van primero
```

**Reglas de orden en composite indexes:**

```
┌─────────────────────────────────────────────────┐
│  Composite Index: (email, name, created_at)     │
├─────────────────────────────────────────────────┤
│  Si WHERE usa:       | El index funciona:       │
│  email               | SI (primer columna)      │
│  email + name        | SI (primeras dos)        │
│  email + name + date | SI (todas)               │
│  name                | NO (salta la primera)    │
│  name + email        | PARCIAL (reordena)       │
│  created_at          | NO                       │
└─────────────────────────────────────────────────┘
```

---

## Partial indexes

Un index que solo incluye filas que cumplen una condicion:

```sql
-- Index solo para usuarios activos
CREATE INDEX idx_users_active ON users (email)
    WHERE status = 'active';

-- Index solo para ordenes pendientes
CREATE INDEX idx_orders_pending ON orders (user_id, created_at)
    WHERE status = 'pending';

-- Consulta que usa el partial index:
SELECT * FROM users WHERE status = 'active' AND email = 'ana@test.com';
-- PostgreSQL usa el index porque la condicion WHERE coincide
```

**Ventajas:**
- Index mas pequeno (menos espacio en disco)
- Mantenimiento mas rapido
- Consultas mas rapidas para el caso de uso comun

---

## Unique indexes

Garantiza que los valores sean unicos:

```sql
-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users (email);

-- Unique index compuesto
CREATE UNIQUE INDEX idx_users_username_tenant
    ON users (username, tenant_id);

-- Intentar insertar duplicado FALLA:
INSERT INTO users (email) VALUES ('ana@test.com');
INSERT INTO users (email) VALUES ('ana@test.com');
-- ERROR: duplicate key value violates unique constraint
```

---

## CREATE INDEX CONCURRENTLY

Crear un index **sin bloquear** la tabla. En tablas grandes, un index normal bloquea las operaciones de escritura durante minutos o horas:

```sql
-- Sin CONCURRENTLY: bloquea la tabla
CREATE INDEX idx_users_email ON users (email);
-- Mientras crea, no se pueden hacer INSERT/UPDATE/DELETE

-- Con CONCURRENTLY: no bloquea
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);
-- La tabla sigue funcionando normalmente
```

**Restricciones de CONCURRENTLY:**
- No se puede ejecutar dentro de una transaccion
- Puede fallar y dejar un index "INVALIDO"
- Toma mas tiempo que un index normal

```sql
-- Verificar si un index es invalido
SELECT indexrelname, indisvalid
FROM pg_index
JOIN pg_class ON pg_class.oid = indexrelid
WHERE relname LIKE 'idx_%';

-- Eliminar un index concurrently
DROP INDEX CONCURRENTLY idx_users_email;
```

---

## Ver los indexes existentes

### Usando pg_indexes

```sql
-- Todos los indexes de una tabla
SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'users';
```

### Usando psql

```
-- En psql:
\di users    -- Lista indexes de la tabla 'users'
\di *        -- Todos los indexes
```

### Informacion detallada

```sql
-- Tamano de los indexes
SELECT
    indexrelname AS index_name,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE relname = 'users'
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## EXPLAIN ANALYZE: leer planes de consulta

```sql
-- Plan basico
EXPLAIN SELECT * FROM users WHERE email = 'ana@test.com';

-- Plan real (ejecuta la consulta)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'ana@test.com';

-- Plan conBuffers (muestra uso de memoria)
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'ana@test.com';
```

**Tipos de escaneo:**

```
┌─────────────────────────────────────────────────┐
│           TIPOS DE ESCANEO                      │
├─────────────────────────────────────────────────┤
│                                                 │
│  Seq Scan (Sequential)                          │
│  ┌─────────────────────────────────────────┐    │
│  │ Lee CADA fila de la tabla               │    │
│  │ O(n) - lento en tablas grandes          │    │
│  │ Usado cuando: no hay index, tabla chica  │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  Index Scan                                     │
│  ┌─────────────────────────────────────────┐    │
│  │ Usa el index para encontrar filas       │    │
│  │ O(log n) - rapido                       │    │
│  │ Usado cuando: WHERE usa columna indexada│    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  Index Only Scan                                │
│  ┌─────────────────────────────────────────┐    │
│  │ Todo esta en el index (covering index)  │    │
│  │ Mas rapido que Index Scan               │    │
│  │ Usado cuando: SELECT solo columnas del  │    │
│  │ index                                   │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  Bitmap Index Scan + Bitmap Heap Scan           │
│  ┌─────────────────────────────────────────┐    │
│  │ Combina multiples matches del index     │    │
│  │ Usado cuando: matching parcial          │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

## Cuando crear un index

### SI crear un index cuando:

| Escenario | Razon |
|-----------|-------|
| Columna en `WHERE` frecuente | Reduce escaneos |
| Columna en `JOIN` (FK) | Acelera joins |
| Columna en `ORDER BY` | Evita sorting |
| Columna con alta cardinalidad | Muchos valores unicos |
| Tabla grande (>10K filas) | Seq Scan es lento |

### NO crear un index cuando:

| Escenario | Razon |
|-----------|-------|
| Tabla pequena (<1K filas) | Seq Scan ya es rapido |
| Columna con poca cardinalidad | Muchos duplicados (ej: `genero`) |
| Tabla con muchas escrituras | Overhead de mantenimiento |
| Consulta que retorna >15% de filas | Seq Scan es mas barato |

---

## Ejemplo completo: optimizacion paso a paso

```sql
-- 1. Tabla sin index
CREATE TABLE logs (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    level TEXT NOT NULL,
    message TEXT NOT NULL,
    user_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insertar 1M de registros
INSERT INTO logs (level, message, user_id)
SELECT
    CASE (random() * 3)::INTEGER
        WHEN 0 THEN 'ERROR'
        WHEN 1 THEN 'WARN'
        WHEN 2 THEN 'INFO'
        ELSE 'DEBUG'
    END,
    'Message ' || i,
    gen_random_uuid()
FROM generate_series(1, 1000000) AS i;

-- 2. Medir sin index
EXPLAIN ANALYZE SELECT * FROM logs WHERE level = 'ERROR';
-- Seq Scan on logs (cost=0.00..16932.00 rows=250000 width=88)
-- Planning Time: 0.085 ms
-- Execution Time: 45.234 ms

-- 3. Crear index
CREATE INDEX CONCURRENTLY idx_logs_level ON logs (level);

-- 4. Medir con index
EXPLAIN ANALYZE SELECT * FROM logs WHERE level = 'ERROR';
-- Index Scan using idx_logs_level on logs (cost=0.43..67323.75 rows=250000 width=88)
-- Planning Time: 0.125 ms
-- Execution Time: 12.567 ms

-- 5. Ver tamano del index
SELECT pg_size_pretty(pg_relation_size('idx_logs_level'));
-- ~21 MB
```

---

## Resumen

```
┌──────────────────────────────────────────────────────┐
│                TIPOS DE INDEX                        │
├──────────────┬───────────────────────────────────────┤
│ B-tree       │ Default. Igualdad + Rangos            │
│ Hash         │ Solo igualdad, mas rapido             │
│ GIN          │ JSONB, arrays, full-text               │
│ GiST         │ Geometria, rangos, full-text          │
│ BRIN         │ Tablas grandes con datos ordenados    │
├──────────────┴───────────────────────────────────────┤
│  Composite: multiples columnas, orden importa        │
│  Partial: WHERE en definicion del index              │
│  Unique: valores unicos                              │
│  CONCURRENTLY: sin bloquear tabla                    │
└──────────────────────────────────────────────────────┘
```

---

**Siguiente:** [04 - PL/pgSQL y Funciones](04-plpgsql-funciones.md)
