# 01 - PostgreSQL vs SQL Estandar

> PostgreSQL no es solo un motor SQL: es un ecosistema completo con funcionalidades que el SQL estandar no define.

---

## Que agrega PostgreSQL al SQL estandar

El SQL estandar (ISO/IEC 9075) define la sintaxis basica. PostgreSQL lo superconjunta con extensiones propias que lo hacen mas potente:

| Funcionalidad | SQL Estandar | PostgreSQL |
|---------------|:------------:|:----------:|
| `ILIKE` (case-insensitive) | No | Si |
| `gen_random_uuid()` | No | Si |
| Dollar quoting `$$` | No | Si |
| `EXPLAIN ANALYZE` | No | Si |
| Extensiones (`pg_trgm`, etc.) | No | Si |
| JSONB nativo | No | Si |
| Full-text search | No | Si |
| `GREATEST` / `LEAST` | Parcial | Si |
| `date_trunc` | No | Si |
| Operador `\|\|` | Parcial | Si |

**Fuente:** PostgreSQL 18 Tutorial, Cap. 1

---

## ILIKE: busqueda case-insensitive

`LIKE` es case-sensitive por defecto. `ILIKE` ignora mayusculas/minusculas:

```sql
-- LIKE: solo coincide con 'PostgreSQL' exacto
SELECT * FROM users WHERE name LIKE '%postgres%';

-- ILIKE: coincide con 'PostgreSQL', 'POSTGRESQL', 'postgresql', etc.
SELECT * FROM users WHERE name ILIKE '%postgres%';
```

**Nota:** `ILIKE` es una extension de PostgreSQL, no parte del SQL estandar. Para portabilidad, puedes usar `LOWER(column) LIKE '%postgres%'`, pero `ILIKE` es mas limpio y rapido.

---

## gen_random_uuid(): UUIDs nativos

PostgreSQL genera UUIDs v4 (aleatorios) sin necesidad de bibliotecas externas:

```sql
-- Genera un UUID v4 aleatorio
SELECT gen_random_uuid();

-- Ejemplo de uso en una tabla
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL
);

INSERT INTO users (name) VALUES ('Ana');
-- 'id' se genera automaticamente
```

**Comparacion con alternativas:**

| Metodo | Ventaja | Desventaja |
|--------|---------|------------|
| `gen_random_uuid()` | Nativo, sin extension | PostgreSQL 13+ |
| `uuid-ossp` extension | Funciona en versiones viejas | Requiere instalacion |
| Aplicacion (Dart) | Control total | Mas codigo, roundtrip |

---

## NOW() vs CURRENT_TIMESTAMP

Ambos retornan la fecha/hora actual, pero tienen diferencias sutiles:

```sql
-- Ambos funcionan igual en la mayoria de casos
SELECT NOW();
SELECT CURRENT_TIMESTAMP;

-- NOW() retorna el timestamp al inicio de la transaccion
-- CURRENT_TIMESTAMP es el estandar SQL
```

| Funcion | Tipo de retorno | Evalua |
|---------|----------------|--------|
| `NOW()` | `timestamp with time zone` | Inicio de transaccion |
| `CURRENT_TIMESTAMP` | `timestamp with time zone` | Inicio de transaccion |
| `CURRENT_DATE` | `date` | Inicio de transaccion |
| `CURRENT_TIME` | `time with time zone` | Inicio de transaccion |

**Consejo pratique:** Usa `NOW()` en PostgreSQL. Es mas corto y todo el mundo lo entiende.

---

## Dollar Quoting: `$$ ... $$`

El dollar quoting permite escribir cadenas de texto sin preocuparte por comillas internas:

```sql
-- Sin dollar quoting: necesitas escapar comillas
CREATE FUNCTION greet() RETURNS TEXT AS '
BEGIN
    RETURN ''Hola mundo'';
END;
' LANGUAGE plpgsql;

-- Con dollar quoting: mas limpio
CREATE FUNCTION greet() RETURNS TEXT AS $$
BEGIN
    RETURN 'Hola mundo';
END;
$$ LANGUAGE plpgsql;
```

**Regla:** `$$` es el delimiter mas comun. Puedes usar etiquetas personalizadas:

```sql
CREATE FUNCTION example() RETURNS TEXT AS $function$
BEGIN
    RETURN 'con etiqueta';
END;
$function$ LANGUAGE plpgsql;
```

---

## EXPLAIN y EXPLAIN ANALYZE

Estas sentencias muestran como PostgreSQL ejecuta una consulta:

```sql
-- EXPLAIN: muestra el plan estimado
EXPLAIN SELECT * FROM users WHERE email = 'ana@test.com';

-- EXPLAIN ANALYZE: ejecuta la consulta y muestra el plan real
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'ana@test.com';
```

**Ejemplo de salida:**

```
Seq Scan on users  (cost=0.00..35.50 rows=1 width=64)
  Filter: (email = 'ana@test.com'::text)
Planning Time: 0.085 ms
Execution Time: 0.124 ms
```

| Elemento | Significado |
|----------|-------------|
| `Seq Scan` | Escaneo secuencial (sin index) |
| `Index Scan` | Usa un index (mas rapido) |
| `cost=0.00..35.50` | Costo estimado (inicio..fin) |
| `rows=1` | Filas estimadas |
| `width=64` | Ancho promedio de fila en bytes |
| `Execution Time` | Tiempo real de ejecucion |

**Cuando usar:**
- `EXPLAIN`: antes de crear un index para ver si es necesario
- `EXPLAIN ANALYZE`: para optimizar consultas lentas

---

## Extensiones de PostgreSQL

Las extensiones son paquetes de funcionalidad adicional:

### Instalar extensiones

```sql
-- pg_trgm: busqueda difusa (fuzzy search)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- unaccent: quitar acentos de texto
CREATE EXTENSION IF NOT EXISTS unaccent;

-- pgcrypto: funciones criptograficas
CREATE EXTENSION IF NOT EXISTS pgcrypto;
```

### Extensiones mas usadas

| Extension | Funcion | Ejemplo de uso |
|-----------|---------|----------------|
| `pg_trgm` | Busqueda difusa con `LIKE` y `ILIKE` | Buscar "hola" matchea "holamundo" |
| `unaccent` | Quitar tildes y acentos | "cafe" matchea "cafe" |
| `pgcrypto` | Hash de contraseñas, encriptacion | `crypt('pass', gen_salt('bf'))` |
| `uuid-ossp` | Generar UUIDs (alternativa a `gen_random_uuid`) | `uuid_generate_v4()` |
| `pg_stat_statements` | Estadisticas de consultas | Encontrar queries lentos |

### pg_trgm en accion

```sql
-- Instalar la extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Busqueda difusa: encontrar nombres similares
SELECT name FROM users
WHERE name % 'Jonh';  -- Matchea 'John', 'Jon', 'Jonh'

-- Operador de similaridad
SELECT name, similarity(name, 'Jonh') AS sim
FROM users
WHERE name % 'Jonh'
ORDER BY sim DESC;
```

---

## Operador de concatenacion `||`

PostgreSQL usa `||` para concatenar cadenas y arrays:

```sql
-- Concatenar strings
SELECT 'Hola' || ' ' || 'Mundo';  -- 'Hola Mundo'

-- Concatenar con NULL
SELECT 'Hola' || NULL;  -- NULL (cualquier operacion con NULL es NULL)

-- Concatenar arrays
SELECT ARRAY[1,2] || ARRAY[3,4];  -- {1,2,3,4}

-- En UPDATE
UPDATE users SET full_name = first_name || ' ' || last_name;
```

**Alternativa:** `CONCAT()` es mas seguro con NULLs:

```sql
SELECT CONCAT('Hola', ' ', NULL);  -- 'Hola  ' (no NULL)
SELECT 'Hola' || ' ' || NULL;      -- NULL
```

---

## GREATEST y LEAST

Retornan el valor maximo o minimo de una lista:

```sql
-- GREATEST: el valor mas alto
SELECT GREATEST(10, 20, 30);  -- 30

-- LEAST: el valor mas bajo
SELECT LEAST(10, 20, 30);  -- 10

-- Uso practical: limitar un valor entre rangos
SELECT GREATEST(0, LEAST(100, score + 10));  -- Nunca menor a 0 ni mayor a 100

-- Con NULLs (ignora NULLs por defecto)
SELECT GREATEST(10, NULL, 30);  -- 30
```

---

## Funciones de fecha especificas de PostgreSQL

### date_trunc

Trunca una fecha a la precision especificada:

```sql
-- Primer dia del mes actual
SELECT date_trunc('month', NOW());

-- Primer dia del año actual
SELECT date_trunc('year', NOW());

-- Inicio de la semana (lunes)
SELECT date_trunc('week', NOW());

-- GROUP BY por mes
SELECT date_trunc('month', created_at) AS mes, COUNT(*)
FROM orders
GROUP BY mes
ORDER BY mes;
```

### extract

Extrae partes especificas de una fecha:

```sql
-- Extraer el año
SELECT EXTRACT(YEAR FROM NOW());  -- 2026

-- Extraer el mes
SELECT EXTRACT(MONTH FROM NOW());  -- 7

-- Extraer el dia de la semana (0=domingo, 6=sabado)
SELECT EXTRACT(DOW FROM NOW());

-- Extraer la hora
SELECT EXTRACT(HOUR FROM NOW());
```

### age

Calcula la diferencia entre dos fechas:

```sql
-- Edad desde una fecha de nacimiento
SELECT age(NOW(), '1990-05-15');

-- Resultado: 36 años 2 meses 5 dias

-- Edad en años solamente
SELECT EXTRACT(YEAR FROM age(NOW(), '1990-05-15'));
```

**Tabla resumen de funciones de fecha:**

| Funcion | Descripcion | Ejemplo | Resultado |
|---------|-------------|---------|-----------|
| `date_trunc('month', fecha)` | Inicio del mes | `date_trunc('month', '2026-07-15')` | `2026-07-01` |
| `extract(YEAR FROM fecha)` | Componente especifico | `extract(YEAR FROM '2026-07-15')` | `2026` |
| `age(fecha1, fecha2)` | Diferencia entre fechas | `age('2026-07-15', '1990-05-15')` | `36 años...` |
| `NOW()` | Fecha/hora actual | `NOW()` | `2026-07-15 10:30:00` |
| `CURRENT_DATE` | Fecha actual | `CURRENT_DATE` | `2026-07-15` |

---

## Resumen

```
┌──────────────────────────────────────────────────┐
│           PostgreSQL vs SQL Estandar             │
├──────────────────────────────────────────────────┤
│  ILIKE          -> Busqueda case-insensitive     │
│  gen_random_uuid -> UUIDs nativos                │
│  $$...$$        -> Dollar quoting para funciones │
│  EXPLAIN        -> Analizar planes de consulta   │
│  Extensiones    -> Funcionalidad modular         │
│  ||             -> Concatenacion                 │
│  GREATEST/LEAST -> Valores extremos              │
│  date_trunc     -> Truncar fechas                │
│  extract        -> Componentes de fecha          │
│  age            -> Diferencia entre fechas       │
└──────────────────────────────────────────────────┘
```

---

**Siguiente:** [02 - Constraints / Restricciones](02-constraints-restricciones.md)
