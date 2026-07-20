# 08 - Cheatsheet SQL

> Referencia rapida de todos los comandos, tipos de datos, funciones y patrones de SQL para PostgreSQL 18.

```
┌──────────────────────────────────────────────────────────────┐
│                    CHEATSHEET SQL                             │
│                    PostgreSQL 18                              │
│                                                              │
│  Guarda este archivo como referencia rapida                  │
│  Consulta esto cuando tengas dudas sobre sintaxis            │
└──────────────────────────────────────────────────────────────┘
```

## Comandos SQL por categoria

### DDL (Data Definition Language)

| Comando                                    | Funcion                              |
|--------------------------------------------|---------------------------------------|
| `CREATE TABLE t (...)`                     | Crear tabla                           |
| `CREATE TABLE IF NOT EXISTS t (...)`       | Crear si no existe                    |
| `ALTER TABLE t ADD COLUMN c TIPO`          | Agregar columna                       |
| `ALTER TABLE t DROP COLUMN c`              | Eliminar columna                      |
| `ALTER TABLE t RENAME COLUMN c1 TO c2`    | Renombrar columna                     |
| `ALTER TABLE t ALTER COLUMN c TYPE TIPO`   | Cambiar tipo de dato                  |
| `ALTER TABLE t ALTER COLUMN c SET DEFAULT v` | Establecer default                 |
| `ALTER TABLE t ALTER COLUMN c SET NOT NULL` | Hacer NOT NULL                      |
| `ALTER TABLE t ADD CONSTRAINT n CONDICION` | Agregar constraint                    |
| `DROP TABLE t`                             | Eliminar tabla                        |
| `DROP TABLE IF EXISTS t`                   | Eliminar si existe                    |
| `CREATE INDEX idx ON t (c)`                | Crear indice                          |
| `CREATE EXTENSION IF NOT EXISTS "ext"`     | Instalar extension                    |

### DML (Data Manipulation Language)

| Comando                                              | Funcion                        |
|------------------------------------------------------|--------------------------------|
| `SELECT c1, c2 FROM t`                              | Consultar columnas especificas |
| `SELECT * FROM t`                                   | Consultar todas las columnas   |
| `SELECT * FROM t WHERE c = v`                       | Consultar con filtro           |
| `INSERT INTO t (c1, c2) VALUES (v1, v2)`           | Insertar una fila              |
| `INSERT INTO t (c1, c2) VALUES (v1,v2), (v3,v4)`  | Insertar multiples filas       |
| `UPDATE t SET c1 = v1 WHERE c = v`                 | Actualizar registros           |
| `DELETE FROM t WHERE c = v`                         | Eliminar registros             |
| `INSERT ... RETURNING *`                            | Insertar y devolver datos      |
| `UPDATE ... RETURNING *`                            | Actualizar y devolver datos    |
| `DELETE ... RETURNING *`                            | Eliminar y devolver datos      |
| `INSERT ... ON CONFLICT DO UPDATE SET ...`          | Upsert                         |
| `INSERT ... ON CONFLICT DO NOTHING`                 | Insertar o ignorar             |

### Clauses

| Clause        | Funcion                        | Ejemplo                              |
|---------------|--------------------------------|---------------------------------------|
| `WHERE`       | Filtrar filas                  | `WHERE precio > 100`                  |
| `AND`         | Ambas condiciones verdaderas   | `WHERE a > 1 AND b < 10`             |
| `OR`          | Al menos una verdadera         | `WHERE a = 1 OR b = 2`               |
| `NOT`         | Negar condicion                | `WHERE NOT activo`                    |
| `IN`          | Valor en lista                 | `WHERE rol IN ('a', 'b')`            |
| `LIKE/ILIKE`  | Patron de texto                | `WHERE nombre ILIKE '%ana%'`          |
| `BETWEEN`     | Dentro de rango                | `WHERE p BETWEEN 10 AND 50`           |
| `IS NULL`     | Es nulo                        | `WHERE c IS NULL`                     |
| `IS NOT NULL` | No es nulo                     | `WHERE c IS NOT NULL`                 |
| `ORDER BY`    | Ordenar                        | `ORDER BY c DESC`                     |
| `GROUP BY`    | Agrupar                        | `GROUP BY c1, c2`                     |
| `HAVING`      | Filtrar grupos                 | `HAVING COUNT(*) > 5`                 |
| `LIMIT`       | Limitar resultados             | `LIMIT 10`                            |
| `OFFSET`      | Saltar registros               | `OFFSET 20`                           |
| `DISTINCT`    | Sin duplicados                 | `SELECT DISTINCT c`                   |
| `AS`          | Alias                          | `SELECT c AS alias`                   |
| `JOIN`        | Combinar tablas                | `INNER JOIN t ON a.id = b.id`         |
| `UNION`       | Combinar resultados            | `SELECT ... UNION SELECT ...`         |
| `RETURNING`   | Devolver datos modificados     | `INSERT ... RETURNING *`              |

---

## Tipos de datos (compacto)

| Tipo            | Disco    | Ejemplo                        | Uso principal              |
|-----------------|----------|--------------------------------|----------------------------|
| `SMALLINT`      | 2 bytes  | `42`                          | Edad, prioridad            |
| `INTEGER`       | 4 bytes  | `123456`                      | IDs, contadores            |
| `BIGINT`        | 8 bytes  | `9007199254740991`            | Contadores grandes         |
| `SERIAL`        | 4 bytes  | `1,2,3...` (auto)            | PKs auto-increment         |
| `BIGSERIAL`     | 8 bytes  | `1,2,3...` (auto)            | PKs auto-increment grandes |
| `NUMERIC(p,s)`  | Variable | `999999.99`                   | Dinero, precios            |
| `REAL`          | 4 bytes  | `3.14`                        | Coordenadas                |
| `DOUBLE PREC`   | 8 bytes  | `3.14159265358979`            | Calculos cientificos       |
| `TEXT`          | Variable | `'Hola'`                      | Nombres, emails, todo      |
| `VARCHAR(n)`    | Variable | `'Hola'` (max n)              | Cuando necesitas limite    |
| `CHAR(n)`       | n bytes  | `'AB'` (siempre n)            | ISO codes fijos            |
| `DATE`          | 4 bytes  | `'2025-01-15'`                | Solo fecha                 |
| `TIMESTAMPTZ`   | 8 bytes  | `'2025-01-15 14:30:00-05'`   | Fechas con zona horaria    |
| `INTERVAL`      | 16 bytes | `'2 hours'`                   | Duraciones                 |
| `BOOLEAN`       | 1 byte   | `true`/`false`/`NULL`         | Flags, estados             |
| `UUID`          | 16 bytes | `'a1b2c3d4-e5f6-...'`        | Primary keys               |
| `JSONB`         | Variable | `'{"key":"value"}'`           | Datos flexibles            |
| `INET`          | 7-19 B   | `'192.168.1.1'`               | Direcciones IP             |

---

## JOINs: mini diagramas

```
INNER JOIN (A ∩ B):          LEFT JOIN (A + A∩B):         FULL OUTER JOIN (A ∪ B):
┌───────────┐                ┌───────────┐                ┌───────────┐
│ A    B    │                │ A    B    │                │ A    B    │
│  ╲  ╱     │                │ █████╲    │                │ ██████████│
│   ╲╱      │                │ ██████╲   │                │ ██████████│
│   ╱╲      │                │ ███████╲  │                │ ██████████│
│  ╱  ╲     │                │ ████████  │                │ ██████████│
└───────────┘                └───────────┘                └───────────┘
Solo coinciden                Todos A + coincidencia       Todos A y B

RIGHT JOIN (B + A∩B):        CROSS JOIN (A × B):          SELF JOIN:
┌───────────┐                ┌───────────┐                ┌───────────┐
│ A    B    │                │ A    B    │                │ A    B    │
│    ╱█████ │                │ ██████████│                │ A←→A      │
│   ╱██████ │                │ ██████████│                │ (relacion │
│  ╱███████ │                │ ██████████│                │  consigo  │
│   ████████│                │ ██████████│                │  misma)   │
└───────────┘                └───────────┘                └───────────┘
Todos B + coincidencia       Todo con todo                 Tabla consigo misma
```

| JOIN            | Que devuelve                                         |
|-----------------|------------------------------------------------------|
| `INNER JOIN`    | Solo registros que coinciden en AMBAS tablas         |
| `LEFT JOIN`     | Todos de la izquierda + coincidencias de la derecha  |
| `RIGHT JOIN`    | Todos de la derecha + coincidencias de la izquierda  |
| `FULL OUTER`    | Todos de AMBAS tablas                                |
| `CROSS JOIN`    | Producto cartesiano (todo con todo)                  |
| `SELF JOIN`     | Tabla unida consigo misma                            |
| `NATURAL JOIN`  | Automatico por columnas con mismo nombre             |

---

## Funciones de agregacion

| Funcion     | Que hace                       | Ejemplo                            | Ignora NULLs |
|-------------|--------------------------------|-------------------------------------|--------------|
| `COUNT(*)`  | Contar todas las filas         | `COUNT(*)`                         | No           |
| `COUNT(c)`  | Contar valores no-NULL         | `COUNT(email)`                     | Si           |
| `SUM(c)`    | Sumar valores                  | `SUM(precio)`                      | Si           |
| `AVG(c)`    | Promedio                       | `ROUND(AVG(precio), 2)`            | Si           |
| `MIN(c)`    | Valor minimo                   | `MIN(precio)`                      | Si           |
| `MAX(c)`    | Valor maximo                   | `MAX(precio)`                      | Si           |

---

## Operadores

### Comparacion

| Operador | Significado                |
|----------|----------------------------|
| `=`      | Igual a                    |
| `!=`/`<>`| No igual a                 |
| `<`      | Menor que                  |
| `>`      | Mayor que                  |
| `<=`     | Menor o igual que          |
| `>=`     | Mayor o igual que          |

### Logicos

| Operador   | Significado                  |
|------------|------------------------------|
| `AND`      | Ambos verdaderos             |
| `OR`       | Al menos uno verdadero       |
| `NOT`      | Negar                        |
| `IN`       | Valor en lista               |
| `BETWEEN`  | Dentro de rango (inclusivo)  |
| `LIKE`     | Patron (case-sensitive)      |
| `ILIKE`    | Patron (case-insensitive)    |
| `IS NULL`  | Es nulo                      |
| `EXISTS`   | Subquery retorna resultados  |

### Aritmeticos

| Operador | Significado              |
|----------|--------------------------|
| `+`      | Suma                     |
| `-`      | Resta                    |
| `*`      | Multiplicacion           |
| `/`      | Division                 |
| `%`      | Modulo                   |

---

## Patrones comunes

### Paginacion

```sql
-- Pagina N, tamano P
SELECT * FROM tabla
ORDER BY columna
LIMIT P OFFSET (N - 1) * P;

-- Ejemplo: pagina 3, 10 registros por pagina
SELECT * FROM usuarios
ORDER BY created_at DESC
LIMIT 10 OFFSET 20;
```

### Upsert (insertar o actualizar)

```sql
INSERT INTO tabla (columna1, columna2)
VALUES ('valor1', 'valor2')
ON CONFLICT (columna_unica)
DO UPDATE SET
    columna2 = EXCLUDED.columna2;
```

### Conteos condicionales

```sql
SELECT
    COUNT(*) AS total,
    COUNT(CASE WHEN condicion THEN 1 END) AS con_condicion,
    COUNT(CASE WHEN NOT condicion THEN 1 END) AS sin_condicion
FROM tabla;
```

### Top N por grupo (window function)

```sql
SELECT * FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY columna_grupo
            ORDER BY columna_orden DESC
        ) AS rn
    FROM tabla
) ranked
WHERE rn <= N;
```

### Total acumulado

```sql
SELECT
    columna,
    SUM(columna) OVER (
        ORDER BY columna_orden
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS acumulado
FROM tabla;
```

### Diferencia con fila anterior

```sql
SELECT
    columna,
    columna - LAG(columna, 1) OVER (ORDER BY columna_orden) AS diferencia
FROM tabla;
```

### Buscar sin relacion

```sql
-- Registros de A que NO tienen relacion en B
SELECT a.*
FROM tabla_a a
LEFT JOIN tabla_b b ON a.id = b.tabla_a_id
WHERE b.id IS NULL;
```

### Contar por grupos de precio

```sql
SELECT
    CASE
        WHEN precio < 50 THEN 'Barato'
        WHEN precio < 200 THEN 'Medio'
        ELSE 'Caro'
    END AS rango,
    COUNT(*) AS total
FROM productos
GROUP BY
    CASE
        WHEN precio < 50 THEN 'Barato'
        WHEN precio < 200 THEN 'Medio'
        ELSE 'Caro'
    END;
```

---

## Palabras reservadas SQL

Estas palabras **no puedes usar** como nombres de tablas o columnas sin comillas dobles:

```
ALL, ANALYZE, AND, ANY, ARRAY, AS, ASC, ASYMMETRIC, BOTH, CASE, CAST,
CHECK, COLLATE, COLUMN, CONSTRAINT, CREATE, CROSS, CURRENT_DATE,
CURRENT_TIME, CURRENT_TIMESTAMP, CURRENT_USER, DEFAULT, DEFERRABLE,
DESC, DISTINCT, DO, ELSE, EXCEPT, FALSE, FETCH, FOR, FOREIGN, FROM,
FULL, GRANT, GROUP, HAVING, ILIKE, IN, INITIALLY, INNER, INOUT, INSERT,
INTERSECT, INTO, IS, ISNULL, JOIN, LEFT, LIKE, LIMIT, LOCALTIME,
LOCALTIMESTAMP, NATURAL, NOT, NOTNULL, NULL, OFFSET, ON, ONLY, OR,
ORDER, OUTER, OVERLAPS, PLACING, PRIMARY, REFERENCES, RETURNING, RIGHT,
SELECT, SESSION_USER, SIMILAR, SOME, SYMMETRIC, TABLE, THEN, TO, TRIGGER,
TRUE, UNION, UNIQUE, USER, USING, VARIADIC, VERBOSE, WHEN, WHERE, WINDOW,
WITH
```

---

## Templates rapidos

### CREATE TABLE (template estandar)

```sql
CREATE TABLE IF NOT EXISTS mi_tabla (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT NOT NULL DEFAULT 'activo'
        CHECK (estado IN ('activo', 'inactivo', 'borrador')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### INSERT (template)

```sql
INSERT INTO mi_tabla (nombre, descripcion, estado)
VALUES ('Mi nombre', 'Mi descripcion', 'activo')
RETURNING *;
```

### SELECT (template)

```sql
SELECT
    t.id,
    t.nombre,
    t.descripcion,
    t.estado,
    t.created_at
FROM mi_tabla t
WHERE t.estado = 'activo'
ORDER BY t.created_at DESC
LIMIT 20 OFFSET 0;
```

### UPDATE (template)

```sql
UPDATE mi_tabla
SET
    nombre = 'Nuevo nombre',
    updated_at = NOW()
WHERE id = 'uuid-aqui'
RETURNING *;
```

### DELETE (template)

```sql
DELETE FROM mi_tabla
WHERE id = 'uuid-aqui'
RETURNING *;
```

### UPSERT (template)

```sql
INSERT INTO mi_tabla (nombre, descripcion)
VALUES ('Nombre', 'Descripcion')
ON CONFLICT (id)
DO UPDATE SET
    nombre = EXCLUDED.nombre,
    descripcion = EXCLUDED.descripcion,
    updated_at = NOW()
RETURNING *;
```

---

## Funciones utiles

| Funcion                        | Que hace                           | Ejemplo                                    |
|--------------------------------|-------------------------------------|---------------------------------------------|
| `NOW()`                        | Fecha y hora actual                 | `DEFAULT NOW()`                            |
| `gen_random_uuid()`            | Generar UUID v4                     | `DEFAULT gen_random_uuid()`                |
| `ROUND(valor, decimales)`      | Redondear                           | `ROUND(AVG(precio), 2)`                    |
| `AGE(fecha)`                   | Diferencia de tiempo                | `AGE(NOW(), created_at)`                   |
| `DATE_TRUNC('month', fecha)`   | Truncar a mes                       | `DATE_TRUNC('month', NOW())`               |
| `LENGTH(texto)`                | Longitud del texto                  | `LENGTH(nombre)`                           |
| `LOWER(texto)`                 | Convertir a minusculas              | `LOWER(email)`                             |
| `UPPER(texto)`                 | Convertir a mayusculas              | `UPPER(nombre)`                            |
| `TRIM(texto)`                  | Eliminar espacios                   | `TRIM(nombre)`                             |
| `COALESCE(v1, v2)`            | Primer valor no-NULL                | `COALESCE(telefono, 'N/A')`                |
| `GREATEST(v1, v2)`            | Valor maximo                        | `GREATEST(a, b)`                           |
| `LEAST(v1, v2)`               | Valor minimo                        | `LEAST(a, b)`                              |
| `EXTRACT(part FROM fecha)`     | Extraer parte de fecha              | `EXTRACT(MONTH FROM NOW())`                |
| `CONCAT(a, b)`                | Concatenar textos                   | `CONCAT(nombre, ' ', apellido)`            |
| `ILIKE '%patron%'`            | Busqueda case-insensitive           | `WHERE nombre ILIKE '%ana%'`               |

---

## Resumen final

```
┌──────────────────────────────────────────────────────────────────┐
│  SQL BASICO → SELECT, INSERT, UPDATE, DELETE, WHERE, ORDER BY   │
│  SQL INTERMEDIO → JOIN, GROUP BY, HAVING, SUBQUERIES            │
│  SQL AVANZADO → WINDOW FUNCTIONS, CTEs, UPSERT                  │
│                                                                  │
│  PostgreSQL → RDBMS que usa Supabase                             │
│  Tipos recomendados → UUID, TEXT, NUMERIC, TIMESTAMPTZ, JSONB   │
│  Siempre → NOT NULL, DEFAULT, CHECK, IF NOT EXISTS              │
└──────────────────────────────────────────────────────────────────┘
```

## Fuentes

- [PostgreSQL 18 Documentation](https://www.postgresql.org/docs/18/)
- [W3Schools SQL Reference](https://www.w3schools.com/sql/sql_ref_keywords.asp)
- [PostgreSQL Cheat Sheet](https://www.postgresql.org/docs/18/sql-commands.html)

---

> **Fin del Submodulo 1: Fundamentos de SQL** | Vuelve al [README](README.md)
