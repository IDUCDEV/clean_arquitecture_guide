# 06 - JOIN y relaciones

> Los JOINs te permiten combinar datos de dos o mas tablas en una sola consulta. Son la base de las bases de datos relacionales y lo que hace a SQL tan poderoso.

```
┌──────────────────────────────────────────────────────────────┐
│                    RESUMEN RAPIDO                             │
│                                                              │
│  INNER JOIN   → Solo registros que coinciden en AMBAS tablas │
│  LEFT JOIN    → Todos de la izquierda + coincidencias        │
│  RIGHT JOIN   → Todos de la derecha + coincidencias          │
│  FULL JOIN    → Todos de AMBAS tablas                        │
│  CROSS JOIN   → Combinacion cartesianica (todo con todo)     │
│  SELF JOIN    → Una tabla con si misma                        │
│  NATURAL JOIN → Automatico por columnas con mismo nombre     │
└──────────────────────────────────────────────────────────────┘
```

## Indice

1. [Que es un JOIN](#que-es-un-join)
2. [INNER JOIN](#inner-join)
3. [LEFT JOIN](#left-join)
4. [RIGHT JOIN](#right-join)
5. [FULL OUTER JOIN](#full-outer-join)
6. [CROSS JOIN](#cross-join)
7. [SELF JOIN](#self-join)
8. [NATURAL JOIN](#natural-join)
9. [Tabla de decision](#tabla-de-decision)
10. [Errores comunes](#errores-comunes)

---

## Que es un JOIN

Un JOIN combina filas de dos o mas tablas basandose en una **condicion de relacion** (generalmente una foreign key).

**Ejemplo visual con datos:**

```
TABLA: usuarios                 TABLA: pedidos
┌────┬─────────┬───────────┐   ┌────┬────────────┬────────┐
│ id │ nombre  │ email     │   │ id │ usuario_id │ total  │
├────┼─────────┼───────────┤   ├────┼────────────┼────────┤
│  1 │ Ana     │ a@m.com   │   │ 10 │     1      │ 150.00 │
│  2 │ Carlos  │ c@m.com   │   │ 11 │     1      │ 200.00 │
│  3 │ Luis    │ l@m.com   │   │ 12 │     3      │ 75.00  │
└────┴─────────┴───────────┘   └────┴────────────┴────────┘

INNER JOIN (usuarios + pedidos):
┌─────────┬────────┬────────────┬────────┐
│ nombre  │ email  │ pedido_id  │ total  │
├─────────┼────────┼────────────┼────────┤
│ Ana     │ a@m.com│    10      │ 150.00 │  ← Ana tiene pedidos
│ Ana     │ a@m.com│    11      │ 200.00 │  ← Ana tiene 2 pedidos
│ Luis    │ l@m.com│    12      │  75.00 │  ← Luis tiene 1 pedido
└─────────┴────────┴────────────┴────────┘
  Carlos NO aparece (no tiene pedidos)
```

---

## INNER JOIN

Devuelve **solo** los registros que tienen coincidencia en **ambas** tablas.

```
┌────────────────────┐
│                    │
│   A       B        │
│    ╲     ╱         │
│     ╲   ╱          │
│      ╲ ╱           │
│       ╳            │
│      ╱ ╲           │
│     ╱   ╲          │
│    ╱     ╲         │
│                    │
│  Solo el area      │
│  sombreada (A ∩ B) │
└────────────────────┘
```

### Sintaxis

```sql
-- Sintaxis ANSI (recomendada)
SELECT a.columna1, b.columna2
FROM tabla_a a
INNER JOIN tabla_b b ON a.id = b.tabla_a_id;

-- Sintaxis con WHERE (igua a la anterior)
SELECT a.columna1, b.columna2
FROM tabla_a a, tabla_b b
WHERE a.id = b.tabla_a_id;
```

### Ejemplo completo

```sql
-- Crear tablas de ejemplo
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    total NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insertar datos
INSERT INTO usuarios (nombre, email) VALUES
    ('Ana', 'ana@email.com'),
    ('Carlos', 'carlos@email.com'),
    ('Luis', 'luis@email.com'),
    ('Maria', 'maria@email.com');

INSERT INTO pedidos (usuario_id, total) VALUES
    (1, 150.00),
    (1, 200.00),
    (3, 75.00);

-- INNER JOIN: solo usuarios CON pedidos
SELECT
    u.nombre,
    u.email,
    p.id AS pedido_id,
    p.total
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id;

-- Resultado:
-- nombre  | email          | pedido_id | total
-- --------|----------------|-----------|-------
-- Ana     | ana@email.com  |     1     | 150.00
-- Ana     | ana@email.com  |     2     | 200.00
-- Luis    | luis@email.com |     3     |  75.00
-- Carlos y Maria NO aparecen (sin pedidos)
```

### INNER JOIN con multiples tablas

```sql
-- Pedidos con usuario y categoria del producto
SELECT
    u.nombre AS usuario,
    p.id AS pedido_id,
    pr.nombre AS producto,
    c.nombre AS categoria,
    dp.cantidad,
    dp.precio_unitario
FROM pedidos p
INNER JOIN usuarios u ON p.usuario_id = u.id
INNER JOIN detalle_pedido dp ON p.id = dp.pedido_id
INNER JOIN productos pr ON dp.producto_id = pr.id
INNER JOIN categorias c ON pr.categoria_id = c.id;
```

---

## LEFT JOIN

Devuelve **todos** los registros de la tabla izquierda, y las coincidencias de la derecha. Si no hay coincidencia, retorna NULL en las columnas de la derecha.

```
┌────────────────────┐
│                    │
│   A       B        │
│   ████████╲        │
│   █████████╲       │
│   ██████████ ╲     │
│   ███████████  ╲   │
│   ████████████  ╲  │
│   █████████████╲   │
│   ████████████     │
│                    │
│  Todo A + A ∩ B    │
└────────────────────┘
```

### Sintaxis

```sql
SELECT a.columna1, b.columna2
FROM tabla_a a
LEFT JOIN tabla_b b ON a.id = b.tabla_a_id;
```

### Ejemplo completo

```sql
-- LEFT JOIN: TODOS los usuarios, con sus pedidos si existen
SELECT
    u.nombre,
    u.email,
    p.id AS pedido_id,
    p.total
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id;

-- Resultado:
-- nombre  | email          | pedido_id | total
-- --------|----------------|-----------|-------
-- Ana     | ana@email.com  |     1     | 150.00
-- Ana     | ana@email.com  |     2     | 200.00
-- Carlos  | carlos@email.com|  NULL    |  NULL   ← Sin pedidos
-- Luis    | luis@email.com |     3     |  75.00
-- Maria   | maria@email.com|  NULL    |  NULL   ← Sin pedidos
```

### LEFT JOIN con WHERE (filtrar solo los que NO tienen relacion)

```sql
-- Usuarios SIN pedidos
SELECT
    u.nombre,
    u.email
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
WHERE p.id IS NULL;

-- Resultado:
-- nombre  | email
-- --------|----------------
-- Carlos  | carlos@email.com
-- Maria   | maria@email.com

-- Lo mismo con NOT IN (alternativa)
SELECT nombre, email
FROM usuarios
WHERE id NOT IN (SELECT DISTINCT usuario_id FROM pedidos);
```

---

## RIGHT JOIN

Devuelve **todos** de la tabla derecha + coincidencias de la izquierda. Es el espejo de LEFT JOIN.

```
┌────────────────────┐
│                    │
│   A       B        │
│         ╱████████  │
│        ╱█████████  │
│      ╱ ███████████ │
│    ╱   ████████████│
│   ╱    ████████████│
│    ╲   ████████████│
│       ██████████   │
│                    │
│  Todo B + A ∩ B    │
└────────────────────┘
```

### Sintaxis

```sql
SELECT a.columna1, b.columna2
FROM tabla_a a
RIGHT JOIN tabla_b b ON a.id = b.tabla_a_id;
```

### Ejemplo

```sql
-- RIGHT JOIN: todos los pedidos, con el usuario si existe
SELECT
    u.nombre,
    u.email,
    p.id AS pedido_id,
    p.total
FROM usuarios u
RIGHT JOIN pedidos p ON u.id = p.usuario_id;

-- Resultado: todos los pedidos aparecen, con su usuario
-- (En este ejemplo todos los pedidos tienen usuario)
```

> **Tip:** En la practica, `RIGHT JOIN` se puede reescribir como `LEFT JOIN` invirtiendo el orden de las tablas. La mayoria de los desarrolladores usa `LEFT JOIN` casi exclusivamente.

---

## FULL OUTER JOIN

Devuelve **todos** los registros de **ambas** tablas. Si no hay coincidencia, rellena con NULL.

```
┌────────────────────┐
│                    │
│   A       B        │
│   ██████████████   │
│   ███████████████  │
│   ████████████████ │
│   ███████████████  │
│   ██████████████   │
│                    │
│  Todo A ∪ Todo B   │
└────────────────────┘
```

### Sintaxis

```sql
SELECT a.columna1, b.columna2
FROM tabla_a a
FULL OUTER JOIN tabla_b b ON a.id = b.tabla_a_id;
```

### Ejemplo

```sql
-- FULL OUTER JOIN: todos los usuarios y todos los pedidos
SELECT
    u.nombre,
    p.id AS pedido_id,
    p.total
FROM usuarios u
FULL OUTER JOIN pedidos p ON u.id = p.usuario_id;

-- Resultado:
-- nombre  | pedido_id | total
-- --------|-----------|-------
-- Ana     |     1     | 150.00
-- Ana     |     2     | 200.00
-- Carlos  |  NULL     |  NULL
-- Luis    |     3     |  75.00
-- Maria   |  NULL     |  NULL
```

> **Nota:** PostgreSQL soporta `FULL OUTER JOIN`. MySQL y SQLite **NO** lo soportan. En esas bases de datos, tienes que simularlo con `UNION` de `LEFT JOIN` y `RIGHT JOIN`.

---

## CROSS JOIN

Devuelve el **producto cartesiano**: cada fila de la tabla A se combina con cada fila de la tabla B.

```
┌────────────────────┐
│                    │
│   A       B        │
│   ██████████████   │
│   ███████████████  │
│   ████████████████ │
│   ███████████████  │
│   ██████████████   │
│   (combinacion     │
│    de todo con     │
│    todo)           │
└────────────────────┘
```

### Sintaxis

```sql
-- Sintaxis con CROSS JOIN
SELECT a.columna1, b.columna2
FROM tabla_a a
CROSS JOIN tabla_b b;

-- Sintaxis equivalente (sin JOIN)
SELECT a.columna1, b.columna2
FROM tabla_a a, tabla_b b;
```

### Ejemplo

```sql
-- Tallas y colores para un producto
CREATE TABLE tallas (
    id SERIAL PRIMARY KEY,
    talla TEXT NOT NULL
);

CREATE TABLE colores (
    id SERIAL PRIMARY KEY,
    color TEXT NOT NULL
);

INSERT INTO tallas (talla) VALUES ('S'), ('M'), ('L'), ('XL');
INSERT INTO colores (color) VALUES ('Rojo'), ('Azul'), ('Negro');

-- CROSS JOIN: cada talla con cada color
SELECT t.talla, c.color
FROM tallas t
CROSS JOIN colores c;

-- Resultado (12 filas: 4 tallas × 3 colores):
-- talla | color
-- -------|-------
-- S     | Rojo
-- S     | Azul
-- S     | Negro
-- M     | Rojo
-- M     | Azul
-- M     | Negro
-- L     | Rojo
-- L     | Azul
-- L     | Negro
-- XL    | Rojo
-- XL    | Azul
-- XL    | Negro
```

**Cuando usar CROSS JOIN:**

- Generar **todas las combinaciones** posibles (tallas × colores)
- Calcular **todas las parejas** de empleados
- **Testing** y generacion de datos de prueba
- **Reportes** que necesitan todas las combinaciones

---

## SELF JOIN

Une una tabla consigo misma. Es util cuando una tabla tiene una referencia a si misma (como empleados y gerentes).

### Ejemplo

```sql
-- Tabla de empleados con gerente
CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    gerente_id INTEGER REFERENCES empleados(id)
);

INSERT INTO empleados (nombre, gerente_id) VALUES
    ('Director', NULL),
    ('Gerente A', 1),
    ('Gerente B', 1),
    ('Empleado 1', 2),
    ('Empleado 2', 2),
    ('Empleado 3', 3);

-- SELF JOIN: empleados con su gerente
SELECT
    e.nombre AS empleado,
    g.nombre AS gerente
FROM empleados e
LEFT JOIN empleados g ON e.gerente_id = g.id;

-- Resultado:
-- empleado   | gerente
-- -----------|----------
-- Director   | NULL
-- Gerente A  | Director
-- Gerente B  | Director
-- Empleado 1 | Gerente A
-- Empleado 2 | Gerente A
-- Empleado 3 | Gerente B
```

---

## NATURAL JOIN

Une tablas automaticamente por **columnas con el mismo nombre**. No necesita `ON`.

```sql
-- NATURAL JOIN automaticamente usa id y usuario_id
SELECT *
FROM usuarios
NATURAL JOIN pedidos;
```

> **Advertencia:** `NATURAL JOIN` es peligroso porque si agregas una columna con el mismo nombre a ambas tablas, la relacion cambia implicitamente. **No se recomienda** en codigo de produccion. Usa siempre `INNER JOIN ... ON` explicitamente.

---

## Tabla de decision: Que JOIN debo usar?

| Escenario                                        | JOIN a usar                    | Ejemplo                                    |
|--------------------------------------------------|--------------------------------|---------------------------------------------|
| Solo registros que coinciden en ambas tablas     | **INNER JOIN**                 | Usuarios CON pedidos                        |
| Todos de la izquierda, con relacion si existe   | **LEFT JOIN**                  | Todos los usuarios, con pedidos si hay      |
| Todos de la izquierda, sin relacion             | LEFT JOIN + WHERE IS NULL      | Usuarios SIN pedidos                        |
| Todos de la derecha, con relacion si existe     | **RIGHT JOIN**                 | Todos los pedidos, con usuario si existe    |
| Todos de ambas tablas                           | **FULL OUTER JOIN**            | Inventario + ventas (sin perder ninguno)    |
| Combinacion de todo con todo                     | **CROSS JOIN**                 | Tallas × colores                           |
| Relacion consigo misma                           | **SELF JOIN**                  | Empleados con sus gerentes                  |
| Relacion automatica por nombre de columna       | NATURAL JOIN (no recomendado)  | Solo en prototipos rapidos                  |
| Unir multiples tablas                           | JOIN encadenados               | Pedidos + Usuarios + Productos + Categorias |
| Buscar registros sin coincidencia               | LEFT JOIN WHERE IS NULL        | Productos sin ventas                        |
| Verificar si existe al menos una relacion       | EXISTS con subquery            | Usuarios que tienen al menos un pedido     |

### Ejemplo de LEFT JOIN para buscar sin relacion

```sql
-- Productos que NUNCA se vendieron
SELECT p.nombre, p.precio
FROM productos p
LEFT JOIN detalle_pedido dp ON p.id = dp.producto_id
WHERE dp.producto_id IS NULL;

-- Usuarios que NO tienen pedidos
SELECT u.nombre, u.email
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
WHERE p.id IS NULL;
```

---

## Errores comunes

### 1. Olvidar la condicion ON

```sql
-- ❌ CROSS JOIN implicito (producto cartesiano)
SELECT u.nombre, p.total
FROM usuarios u
INNER JOIN pedidos p;

-- ✅ JOIN con condicion explicita
SELECT u.nombre, p.total
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id;
```

### 2. Usar el JOIN incorrecto

```sql
-- ❌ INNER JOIN cuando quieres TODOS los usuarios
SELECT u.nombre, p.total
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id;
-- Carlos y Maria desaparecen

-- ✅ LEFT JOIN para incluir todos
SELECT u.nombre, p.total
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id;
-- Todos los usuarios aparecen
```

### 3. Columnas ambiguas

```sql
-- ❌ Ambiguo: ambas tablas tienen "id"
SELECT id, nombre, total
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id;

-- ✅ Especificar la tabla
SELECT u.id, u.nombre, p.total
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id;
```

### 4. Multiplicacion de filas con JOINs multiples

```sql
-- ⚠️ Puede producir mas filas de lo esperado
-- Si un pedido tiene 3 productos, y cada producto tiene 2 variantes
SELECT *
FROM pedidos p
INNER JOIN detalle_pedido dp ON p.id = dp.pedido_id
INNER JOIN productos pr ON dp.producto_id = pr.id
INNER JOIN variantes v ON pr.id = v.producto_id;
-- Resultado: pedidos × detalle × variantes (multiplicacion)
```

---

## Fuentes

- [PostgreSQL 18 Documentation - Chapter 5: Data Definition - Joins](https://www.postgresql.org/docs/18/queries-table-expressions.html)
- [PostgreSQL Documentation - JOIN](https://www.postgresql.org/docs/18/queries-joins.html)
- [W3Schools - SQL JOINs](https://www.w3schools.com/sql/sql_join.asp)
- [PostgreSQL Documentation - Explicit JOIN](https://www.postgresql.org/docs/18/sql-select.html)

---

> **Siguiente archivo:** [07 - Agrupaciones y funciones de agregacion](07-agrupaciones-funciones.md)
