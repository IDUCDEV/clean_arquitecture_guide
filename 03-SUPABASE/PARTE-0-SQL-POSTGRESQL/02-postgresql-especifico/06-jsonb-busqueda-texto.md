# 06 - JSONB y Busqueda de Texto

> JSONB es el tipo nativo de PostgreSQL para datos JSON. Full-text search permite busquedas linguisticas avanzadas. Ambos son fundamentales para Supabase.

---

## JSONB en PostgreSQL

**JSONB** (JSON Binary) es un tipo de dato que almacena JSON en formato binario, optimizado para busquedas y modificaciones.

```
┌─────────────────────────────────────────────────┐
│  JSON vs JSONB                                  │
├─────────────────────────────────────────────────┤
│  JSON: texto literal, sin indexado              │
│  JSONB: binario, indexable, mas rapido para     │
│         busquedas y actualizaciones             │
└─────────────────────────────────────────────────┘

Siempre usa JSONB en PostgreSQL moderno.
```

**Fuente:** PostgreSQL 18 Documentation, Cap. 9.16 JSON

---

## Crear una columna JSONB

```sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- El JSONB puede contener cualquier estructura valida
INSERT INTO products (name, price, metadata) VALUES (
    'Laptop',
    999.99,
    '{
        "brand": "Dell",
        "specs": {
            "ram": "16GB",
            "storage": "512GB SSD"
        },
        "tags": ["electronics", "computers"],
        "in_stock": true
    }'
);
```

---

## Insertar datos JSONB

```sql
-- Insertar JSON directo
INSERT INTO products (name, price, metadata) VALUES (
    'Mouse',
    29.99,
    '{"brand": "Logitech", "wireless": true}'::jsonb
);

-- Insertar con funciones de construccion
INSERT INTO products (name, price, metadata) VALUES (
    'Teclado',
    79.99,
    jsonb_build_object(
        'brand', 'Razer',
        'type', 'mechanical',
        'rgb', true
    )
);

-- Insertar array
INSERT INTO products (name, price, metadata) VALUES (
    'Monitor',
    349.99,
    jsonb_build_object(
        'brand', 'Samsung',
        'features', jsonb_build_array('4K', 'HDR', '144Hz')
    )
);
```

---

## Operadores JSONB

### Obtener valores

| Operador | Descripcion | Tipo retorno | Ejemplo |
|----------|-------------|:------------:|---------|
| `->` | Campo por nombre/indice | JSONB | `data->'name'` |
| `->>` | Campo como texto | TEXT | `data->>'name'` |
| `#>` | Ruta por indices | JSONB | `data#>'{specs,ram}'` |
| `#>>` | Ruta como texto | TEXT | `data#>>'{specs,ram}'` |

```sql
-- Obtener campo como JSONB
SELECT metadata->'brand' FROM products;
-- "Dell"

-- Obtener campo como TEXT
SELECT metadata->>'brand' FROM products;
-- Dell

-- Obtener de nested object
SELECT metadata#>'{specs,ram}' FROM products;
-- "16GB"

SELECT metadata#>>'{specs,ram}' FROM products;
-- 16GB

-- Obtener elemento de array
SELECT metadata->'tags'->0 FROM products;
-- "electronics"

-- Obtener longitud de array
SELECT jsonb_array_length(metadata->'tags') FROM products;
-- 2
```

### Busqueda

| Operador | Descripcion | Ejemplo |
|----------|-------------|---------|
| `@>` | Contiene | `data @> '{"brand": "Dell"}'` |
| `<@` | Contenido en | `'{"brand": "Dell"}' <@ data` |
| `?` | Key existe | `data ? 'brand'` |
| `?\|` | Cualquier key existe | `data ?\| ARRAY['brand','model']` |
| `?&` | Todas las keys existen | `data ?& ARRAY['brand','model']` |

```sql
-- @>: el JSONB contiene el valor
SELECT * FROM products WHERE metadata @> '{"brand": "Dell"}';
-- Retorna productos con brand = "Dell"

-- Buscar en nested
SELECT * FROM products WHERE metadata @> '{"specs": {"ram": "16GB"}}';

-- ?: key existe
SELECT * FROM products WHERE metadata ? 'wireless';

-- ?|: cualquiera de las keys existe
SELECT * FROM products WHERE metadata ?| ARRAY['wireless', 'bluetooth'];

-- ?&: todas las keys existen
SELECT * FROM products WHERE metadata ?& ARRAY['brand', 'type'];
```

### Modificar

| Operador | Descripcion | Ejemplo |
|----------|-------------|---------|
| `\|\|` | Merge (unir) | `data \|\| '{"color": "red"}'` |
| `#-` | Eliminar key | `data #- ARRAY['brand']` |
| `-` | Eliminar key | `data - 'brand'` |
| `- TEXT[]` | Eliminar multiples keys | `data - ARRAY['brand','type']` |
| `#>` | Asignar en ruta | `jsonb_set(data, '{specs,ram}', '"32GB"')` |

```sql
-- Merge: agregar campo
UPDATE products
SET metadata = metadata || '{"color": "silver"}'::jsonb
WHERE id = '...';

-- Eliminar un campo
UPDATE products
SET metadata = metadata - 'wireless'
WHERE id = '...';

-- Eliminar multiples campos
UPDATE products
SET metadata = metadata - ARRAY['brand', 'type']
WHERE id = '...';

-- Eliminar usando ruta
UPDATE products
SET metadata = metadata #- '{specs,ram}'
WHERE id = '...';

-- Modificar valor anidado con jsonb_set
UPDATE products
SET metadata = jsonb_set(
    metadata,
    '{specs,ram}',
    '"32GB"'
)
WHERE id = '...';
```

### Funciones JSONB utiles

```sql
-- jsonb_build_object: construir objeto
SELECT jsonb_build_object('name', 'Ana', 'age', 30);
-- {"name": "Ana", "age": 30}

-- jsonb_build_array: construir array
SELECT jsonb_build_array(1, 2, 3);
-- [1, 2, 3]

-- jsonb_array_elements: expandir array a filas
SELECT jsonb_array_elements('["a","b","c"]'::jsonb);
-- a
-- b
-- c

-- jsonb_array_elements_text: expandir array como text
SELECT jsonb_array_elements_text('["a","b","c"]'::jsonb);
-- a
-- b
-- c

-- jsonb_object_keys: obtener keys del objeto
SELECT jsonb_object_keys('{"name":"Ana","age":30}'::jsonb);
-- name
-- age

-- jsonb_typeof: tipo de un valor
SELECT jsonb_typeof('{"name":"Ana"}'::jsonb->'name');
-- string

-- jsonb_pretty: formatear JSON
SELECT jsonb_pretty('{"name":"Ana","age":30}'::jsonb);
```

---

## GIN index en JSONB

Sin index, PostgreSQL escanea cada fila. Con GIN, las busquedas son instantaneas:

```sql
-- Crear GIN index
CREATE INDEX idx_products_metadata ON products USING gin (metadata);

-- Busqueda con @> (usa el index)
SELECT * FROM products WHERE metadata @> '{"brand": "Dell"}';
-- Rapido con GIN index

-- Busqueda con ? (usa el index)
SELECT * FROM products WHERE metadata ? 'wireless';
-- Rapido con GIN index
```

**Tipos de GIN para JSONB:**

```sql
-- GIN default (todas las operaciones)
CREATE INDEX idx_metadata ON products USING gin (metadata);

-- GIN con jsonb_ops (busquedas con @>, ?, ?|, ?&)
CREATE INDEX idx_metadata_ops ON products USING gin (metadata jsonb_ops_path_ops);

-- jsonb_ops_path_ops es mas eficiente para @> pero no soporta ?
-- jsonb_ops soporta todo pero es mas grande
```

---

## JSONB: cuando usar vs columnas separadas

```
┌─────────────────────────────────────────────────────┐
│  JSONB vs COLUMNAS SEPARADAS                       │
├───────────────────┬─────────────────────────────────┤
│  Usa JSONB cuando:│  Usa columnas cuando:           │
├───────────────────┼─────────────────────────────────┤
│  Datos variables  │  Datos fijos                    │
│  Schema dinamico  │  Schema conocido                │
│  Datos anidados   │  Relaciones planas              │
│  Metadata extra   │  Columnas en WHERE frecuente    │
│  Polimorfismo     │  JOINs frecuentes               │
└───────────────────┴─────────────────────────────────┘
```

| Criterio | JSONB | Columnas |
|----------|-------|----------|
| Rendimiento de busqueda | Lento (sin index) / Rapido (con GIN) | Muy rapido (B-tree) |
| Flexibilidad | Maxima | Limitada |
| Integridad de datos | None (validar en app) | Constraints nativos |
| Uso de espacio | Mayor | Menor |
| Facilidad de consulta | Mas compleja | Mas simple |

---

## Full-text Search

PostgreSQL tiene busqueda de texto completa integrada:

```
┌─────────────────────────────────────────────────────┐
│  FLUTTER -> Supabase RPC -> PostgreSQL FTS          │
│                                                     │
│  "buscar laptops gaming"                            │
│        |                                            │
│        v                                            │
│  to_tsquery('laptop & gaming')                      │
│        |                                            │
│        v                                            │
│  to_tsvector(content) @@ to_tsquery(...)            │
│        |                                            │
│        v                                            │
│  Filas que matchean, rankeadas                      │
└─────────────────────────────────────────────────────┘
```

**Fuente:** PostgreSQL 18 Documentation, Cap. 12 Text Search

---

## tsvector y tsquery

### tsvector: convertir texto a forma searchable

```sql
-- Convertir texto a tsvector
SELECT to_tsvector('english', 'The quick brown fox jumps over the lazy dog');
-- 'brown':3 'dog':9 'fox':4 'jump':5 'lazi':8 'quick':2

-- Nota: las palabras estan lematizadas (jumps -> jump, lazy -> lazi)
SELECT to_tsvector('spanish', 'Los gatos rapidos cazan ratones');
-- 'cason':5 'gato':2 'raton':7 'rapido':3
```

### tsquery: construir busquedas

```sql
-- Operadores de tsquery
SELECT to_tsquery('english', 'quick & fox');      -- AND
SELECT to_tsquery('english', 'quick | fox');      -- OR
SELECT to_tsquery('english', 'quick & !lazy');    -- AND NOT
SELECT to_tsquery('english', 'quick <-> fox');    -- Proximidad (secuencial)
SELECT to_tsquery('english', 'quick <2> fox');    -- Proximidad (2 palabras)

-- plainto_tsquery: mas simple, ignora operadores
SELECT plainto_tsquery('english', 'quick fox');
-- 'fox' & 'quick'

-- phraseto_tsquery: busca la frase exacta
SELECT phraseto_tsquery('english', 'quick brown fox');
-- 'brown' <-> 'fox' <-> 'quick'
```

### @@ operator: matching

```sql
-- Buscar documentos que contengan 'quick' Y 'fox'
SELECT * FROM articles
WHERE to_tsvector('english', content) @@ to_tsquery('english', 'quick & fox');

-- Buscar con plainto_tsquery (mas simple)
SELECT * FROM articles
WHERE to_tsvector('english', content) @@ plainto_tsquery('english', 'quick fox');

-- Buscar en multiples campos
SELECT * FROM products
WHERE to_tsvector('english', name || ' ' || description)
    @@ plainto_tsquery('english', 'laptop gaming');
```

---

## Ranking: ts_rank y ts_rank_cd

```sql
-- ts_rank: basado en frecuencia de terminos
SELECT
    name,
    ts_rank(
        to_tsvector('english', name || ' ' || description),
        plainto_tsquery('english', 'laptop gaming')
    ) AS rank
FROM products
WHERE to_tsvector('english', name || ' ' || description)
    @@ plainto_tsquery('english', 'laptop gaming')
ORDER BY rank DESC;

-- ts_rank_cd: basado en cobertura de documento
SELECT
    name,
    ts_rank_cd(
        to_tsvector('english', name || ' ' || description),
        plainto_tsquery('english', 'laptop gaming')
    ) AS rank_cd
FROM products
WHERE to_tsvector('english', name || ' ' || description)
    @@ plainto_tsquery('english', 'laptop gaming')
ORDER BY rank_cd DESC;
```

**Diferencia entre ranking:**

| Funcion | Basado en | Mejor para |
|---------|-----------|------------|
| `ts_rank` | Frecuencia del termino | Busquedas generales |
| `ts_rank_cd` | Cobertura del documento | Busquedas de frases |

---

## GIN index para full-text search

```sql
-- Agregar columna tsvector
ALTER TABLE products ADD COLUMN search_vector tsvector;

-- Llenar la columna
UPDATE products SET search_vector =
    to_tsvector('spanish', name || ' ' || COALESCE(description, ''));

-- Crear GIN index
CREATE INDEX idx_products_search ON products USING gin (search_vector);

-- Buscar (usa el index)
SELECT name, ts_rank(search_vector, plainto_tsquery('spanish', 'laptop gaming')) AS rank
FROM products
WHERE search_vector @@ plainto_tsquery('spanish', 'laptop gaming')
ORDER BY rank DESC;
```

---

## Trigger para auto-actualizar tsvector

Mantener la columna search_vector sincronizada automaticamente:

```sql
-- Funcion trigger
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('spanish',
        NEW.name || ' ' || COALESCE(NEW.description, '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER trg_products_search_vector
BEFORE INSERT OR UPDATE OF name, description ON products
FOR EACH ROW
EXECUTE FUNCTION update_search_vector();

-- Ahora search_vector se actualiza automaticamente
```

---

## Ejemplo completo: busqueda de productos

```sql
-- 1. Tabla con soporte completo
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('spanish',
            name || ' ' || COALESCE(description, '') || ' ' || COALESCE(category, '')
        )
    ) STORED
);

-- 2. Indexes
CREATE INDEX idx_products_metadata ON products USING gin (metadata);
CREATE INDEX idx_products_search ON products USING gin (search_vector);
CREATE INDEX idx_products_price ON products (price);
CREATE INDEX idx_products_category ON products (category);

-- 3. Busqueda full-text
SELECT
    name,
    ts_rank(search_vector, plainto_tsquery('spanish', 'laptop gaming')) AS rank
FROM products
WHERE search_vector @@ plainto_tsquery('spanish', 'laptop gaming')
ORDER BY rank DESC
LIMIT 10;

-- 4. Busqueda con filtros combinados
SELECT
    name,
    price,
    ts_rank(search_vector, plainto_tsquery('spanish', 'laptop gaming')) AS rank
FROM products
WHERE search_vector @@ plainto_tsquery('spanish', 'laptop gaming')
  AND price BETWEEN 500 AND 1500
  AND metadata @> '{"in_stock": true}'
ORDER BY rank DESC;

-- 5. Busqueda con sugerencias (similarity)
SELECT
    name,
    similarity(name, 'laptob gamming') AS sim
FROM products
WHERE name % 'laptob gamming'  -- Busqueda difusa con pg_trgm
ORDER BY sim DESC
LIMIT 5;
```

---

## Resumen

```
┌──────────────────────────────────────────────────────┐
│          JSONB + FULL-TEXT SEARCH                    │
├──────────────────────────────────────────────────────┤
│  JSONB                                               │
│  ->  Almacenar datos flexibles/variables             │
│  ->  Busquedas con @>, ?, ?|, ?&                     │
│  ->  Modificar con jsonb_set, #- ||                  │
│  ->  Indexar con GIN                                 │
├──────────────────────────────────────────────────────┤
│  FULL-TEXT SEARCH                                    │
│  ->  to_tsvector: texto a searchable                 │
│  ->  to_tsquery: construir busqueda                  │
│  ->  @@: matching                                    │
│  ->  ts_rank: scoring                                │
│  ->  GIN index para rendimiento                      │
└──────────────────────────────────────────────────────┘
```

---

**Siguiente:** [07 - RPC para Supabase](07-rpc-para-supabase.md)
