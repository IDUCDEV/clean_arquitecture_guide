# 07 - Agrupaciones y funciones de agregacion

> GROUP BY te permite agrupar filas y calcular resumenes. Las funciones de agregacion (COUNT, SUM, AVG, etc.) son las herramientas que usas con GROUP BY para obtener estadisticas de tus datos.

```
┌──────────────────────────────────────────────────────────────┐
│                    RESUMEN RAPIDO                             │
│                                                              │
│  COUNT   → Contar filas                                     │
│  SUM     → Sumar valores numericos                          │
│  AVG     → Promedio                                         │
│  MIN/MAX → Valor minimo/maximo                              │
│  GROUP BY → Agrupar por columna(s)                          │
│  HAVING  → Filtrar grupos (despues de GROUP BY)             │
│  CASE WHEN → Logica condicional en SQL                      │
│  Window functions → Funciones sobre grupos sin colapsar     │
└──────────────────────────────────────────────────────────────┘
```

## Indice

1. [Funciones de agregacion](#funciones-de-agregacion)
2. [GROUP BY](#group-by)
3. [HAVING](#having)
4. [Ejemplos completos](#ejemplos-completos)
5. [CASE WHEN](#case-when)
6. [Subqueries](#subqueries)
7. [Window functions](#window-functions)
8. [Patrones comunes](#patrones-comunes)

---

## Funciones de agregacion

| Funcion   | Que hace                       | Ejemplo                              | Ignora NULLs |
|-----------|--------------------------------|--------------------------------------|--------------|
| `COUNT(*)`| Contar todas las filas         | `COUNT(*)`                          | No           |
| `COUNT(c)`| Contar valores no-NULL         | `COUNT(email)`                      | **Si**       |
| `SUM(c)`  | Sumar todos los valores        | `SUM(precio)`                       | **Si**       |
| `AVG(c)`  | Promedio de los valores        | `AVG(precio)`                       | **Si**       |
| `MIN(c)`  | Valor minimo                   | `MIN(precio)`                       | **Si**       |
| `MAX(c)`  | Valor maximo                   | `MAX(precio)`                       | **Si**       |

```sql
-- COUNT: contar registros
SELECT COUNT(*) AS total_usuarios FROM usuarios;
-- Resultado: 4

SELECT COUNT(telefono) AS usuarios_con_telefono FROM usuarios;
-- Solo cuenta los que tienen telefono (no NULL)

-- SUM: sumar valores
SELECT SUM(total) AS total_ventas FROM pedidos;
-- Resultado: 425.00

-- AVG: promedio
SELECT AVG(total) AS promedio_pedido FROM pedidos;
-- Resultado: 141.67

-- MIN y MAX
SELECT
    MIN(precio) AS precio_minimo,
    MAX(precio) AS precio_maximo
FROM productos;
-- Resultado: precio_minimo = 25.00, precio_maximo = 999.99
```

**COUNT(*) vs COUNT(columna):**

```sql
-- COUNT(*) cuenta TODAS las filas (incluye NULLs)
SELECT COUNT(*) FROM usuarios;
-- Resultado: 4 (todos los usuarios)

-- COUNT(columna) solo cuenta valores NO-NULL
SELECT COUNT(telefono) FROM usuarios;
-- Resultado: 2 (solo los que tienen telefono)
```

---

## GROUP BY

Agrupa filas que tienen los mismos valores en una o mas columnas.

### Sintaxis

```sql
SELECT columna, funcion_agregacion(columna)
FROM tabla
GROUP BY columna;
```

### Ejemplos basicos

```sql
-- Contar usuarios por rol
SELECT
    rol,
    COUNT(*) AS total_usuarios
FROM usuarios
GROUP BY rol;

-- Resultado:
-- rol       | total_usuarios
-- ----------|---------------
-- admin     |      1
-- user      |      2
-- moderator |      1

-- Sumar ventas por usuario
SELECT
    usuario_id,
    SUM(total) AS total_gastado,
    COUNT(*) AS numero_pedidos
FROM pedidos
GROUP BY usuario_id;

-- Resultado:
-- usuario_id | total_gastado | numero_pedidos
-- -----------|---------------|---------------
--     1      |    350.00     |      2
--     3      |     75.00     |      1
```

### GROUP BY con multiples columnas

```sql
-- Contar productos por categoria y estado
SELECT
    categoria_id,
    activo,
    COUNT(*) AS total,
    AVG(precio) AS precio_promedio
FROM productos
GROUP BY categoria_id, activo;

-- Resultado:
-- categoria_id | activo | total | precio_promedio
-- -------------|--------|-------|----------------
--      1       | true   |   5   |    89.99
--      1       | false  |   2   |    45.00
--      2       | true   |   3   |   150.00
```

### Reglas de GROUP BY

```
┌──────────────────────────────────────────────────────────────┐
│  REGLA: Todo lo que esta en SELECT sin funcion de agregacion │
│  DEBE estar en GROUP BY                                     │
│                                                              │
│  SELECT rol, COUNT(*)    → GROUP BY rol ✅                   │
│  SELECT rol, nombre      → GROUP BY rol, nombre ✅          │
│  SELECT rol, precio      → GROUP BY rol ❌ ERROR            │
│  (precio no esta agregado ni en GROUP BY)                   │
└──────────────────────────────────────────────────────────────┘
```

```sql
-- ✅ Correcto
SELECT rol, COUNT(*)
FROM usuarios
GROUP BY rol;

-- ❌ Error: "nombre" no esta en GROUP BY ni en funcion de agregacion
SELECT rol, nombre, COUNT(*)
FROM usuarios
GROUP BY rol;
-- ERROR: column "nombre" must appear in the GROUP BY clause

-- ✅ Corregido
SELECT rol, nombre, COUNT(*)
FROM usuarios
GROUP BY rol, nombre;
```

---

## HAVING

Filtra **grupos** despues de GROUP BY. A diferencia de `WHERE`, que filtra **filas antes** de agrupar.

**Diferencia clave:**

```
┌──────────────────────────────────────────────────────────────┐
│  WHERE  → Filtra FILAS (antes de GROUP BY)                   │
│  HAVING → Filtra GRUPOS (despues de GROUP BY)                │
└──────────────────────────────────────────────────────────────┘
```

```sql
-- WHERE: filtrar filas ANTES de agrupar
SELECT
    usuario_id,
    SUM(total) AS total_gastado
FROM pedidos
WHERE total > 50          -- Solo pedidos mayores a 50
GROUP BY usuario_id;

-- HAVING: filtrar grupos DESPUES de agrupar
SELECT
    usuario_id,
    SUM(total) AS total_gastado
FROM pedidos
GROUP BY usuario_id
HAVING SUM(total) > 100;  -- Solo usuarios que gastaron mas de 100

-- Combinar WHERE y HAVING
SELECT
    usuario_id,
    SUM(total) AS total_gastado,
    COUNT(*) AS num_pedidos
FROM pedidos
WHERE total > 50              -- Filtrar pedidos individuales
GROUP BY usuario_id
HAVING COUNT(*) >= 2;         -- Solo usuarios con 2+ pedidos
```

**Resumen de ejecucion:**

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
  1      2         3          4        5          6         7
```

---

## Ejemplos completos

```sql
-- ============================================
-- EJEMPLO 1: Estadisticas de ventas por mes
-- ============================================
SELECT
    DATE_TRUNC('month', created_at) AS mes,
    COUNT(*) AS total_pedidos,
    SUM(total) AS ingresos,
    ROUND(AVG(total), 2) AS ticket_promedio,
    MIN(total) AS pedido_minimo,
    MAX(total) AS pedido_maximo
FROM pedidos
WHERE estado != 'cancelado'
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY mes DESC;

-- ============================================
-- EJEMPLO 2: Productos mas vendidos
-- ============================================
SELECT
    pr.nombre,
    pr.precio,
    SUM(dp.cantidad) AS unidades_vendidas,
    SUM(dp.subtotal) AS ingresos_totales
FROM productos pr
INNER JOIN detalle_pedido dp ON pr.id = dp.producto_id
GROUP BY pr.id, pr.nombre, pr.precio
ORDER BY ingresos_totales DESC
LIMIT 10;

-- ============================================
-- EJEMPLO 3: Usuarios con mas pedidos
-- ============================================
SELECT
    u.nombre,
    u.email,
    COUNT(p.id) AS total_pedidos,
    SUM(p.total) AS total_gastado,
    MAX(p.created_at) AS ultimo_pedido
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
GROUP BY u.id, u.nombre, u.email
HAVING COUNT(p.id) > 0
ORDER BY total_gastado DESC;
```

---

## CASE WHEN

Expresion condicional en SQL. Funciona como un "if-else" dentro de una consulta.

### CASE WHEN simple

```sql
-- Asignar etiquetas basadas en una condicion
SELECT
    nombre,
    precio,
    CASE
        WHEN precio < 50 THEN 'Economico'
        WHEN precio < 200 THEN 'Medio'
        WHEN precio < 500 THEN 'Caro'
        ELSE 'Premium'
    END AS categoria_precio
FROM productos;
```

### CASE WHEN searched

```sql
-- Con multiples condiciones
SELECT
    nombre,
    stock,
    CASE
        WHEN stock = 0 THEN 'Sin stock'
        WHEN stock <= 5 THEN 'Poco stock'
        WHEN stock <= 20 THEN 'Stock normal'
        ELSE 'Mucho stock'
    END AS estado_stock
FROM productos;
```

### CASE en SELECT

```sql
-- Contar por condicion
SELECT
    COUNT(*) AS total,
    COUNT(CASE WHEN activo = true THEN 1 END) AS activos,
    COUNT(CASE WHEN activo = false THEN 1 END) AS inactivos
FROM usuarios;
```

### CASE en ORDER BY

```sql
-- Ordenar con logica personalizada
SELECT nombre, precio
FROM productos
ORDER BY
    CASE
        WHEN nombre ILIKE '%oferta%' THEN 0  -- Primero los de oferta
        WHEN stock > 10 THEN 1               -- Luego los con stock
        ELSE 2                                -- Al final los demas
    END,
    precio ASC;
```

### CASE en GROUP BY

```sql
-- Contar por rangos de precio
SELECT
    CASE
        WHEN precio < 50 THEN '0-50'
        WHEN precio < 100 THEN '50-100'
        WHEN precio < 500 THEN '100-500'
        ELSE '500+'
    END AS rango_precio,
    COUNT(*) AS total_productos
FROM productos
GROUP BY
    CASE
        WHEN precio < 50 THEN '0-50'
        WHEN precio < 100 THEN '50-100'
        WHEN precio < 500 THEN '100-500'
        ELSE '500+'
    END
ORDER BY rango_precio;
```

---

## Subqueries

Una subquery (consulta interna) es una SELECT dentro de otra SELECT.

### Subquery en WHERE

```sql
-- Productos mas caros que el promedio
SELECT nombre, precio
FROM productos
WHERE precio > (SELECT AVG(precio) FROM productos);

-- Usuarios que tienen pedidos
SELECT *
FROM usuarios
WHERE id IN (SELECT DISTINCT usuario_id FROM pedidos);
```

### Subquery en FROM

```sql
-- Usar una subquery como tabla temporal
SELECT
    sub.usuario_id,
    sub.total_gastado,
    u.nombre
FROM (
    SELECT usuario_id, SUM(total) AS total_gastado
    FROM pedidos
    GROUP BY usuario_id
) sub
INNER JOIN usuarios u ON sub.usuario_id = u.id
WHERE sub.total_gastado > 100;
```

### Subquery en SELECT

```sql
-- Mostrar el total de pedidos junto con los datos del usuario
SELECT
    u.nombre,
    u.email,
    (SELECT COUNT(*) FROM pedidos p WHERE p.usuario_id = u.id) AS total_pedidos,
    (SELECT SUM(total) FROM pedidos p WHERE p.usuario_id = u.id) AS total_gastado
FROM usuarios u;
```

### EXISTS

Verifica si la subquery retorna **al menos un registro**.

```sql
-- Usuarios que tienen al menos un pedido
SELECT *
FROM usuarios u
WHERE EXISTS (
    SELECT 1 FROM pedidos p WHERE p.usuario_id = u.id
);

-- Usuarios que NO tienen pedidos
SELECT *
FROM usuarios u
WHERE NOT EXISTS (
    SELECT 1 FROM pedidos p WHERE p.usuario_id = u.id
);
```

**EXISTS vs IN:**

| Operador | Cuando usar                                              | Rendimiento                    |
|----------|----------------------------------------------------------|--------------------------------|
| `IN`     | Subquery pequena, pocos valores                          | Bueno                           |
| `EXISTS` | Subquery grande, muchos registros, o con JOINs complejos | **Mejor para tablas grandes**  |

---

## Window functions

Las window functions realizan calculos sobre un **conjunto de filas** relacionadas con la fila actual, **sin colapsar** las filas como GROUP BY.

### Sintaxis basica

```sql
 funcion_ventana() OVER (
    PARTITION BY columna    -- Opcional: agrupar por
    ORDER BY columna        -- Opcional: ordenar dentro del grupo
 )
```

### ROW_NUMBER()

Asigna un numero secuencial unico a cada fila dentro de un grupo.

```sql
-- Numerar pedidos por usuario (1, 2, 3...)
SELECT
    u.nombre,
    p.total,
    p.created_at,
    ROW_NUMBER() OVER (
        PARTITION BY p.usuario_id
        ORDER BY p.created_at ASC
    ) AS numero_pedido
FROM pedidos p
INNER JOIN usuarios u ON p.usuario_id = u.id;

-- Resultado:
-- nombre | total  | created_at          | numero_pedido
-- -------|--------|---------------------|---------------
-- Ana    | 150.00 | 2025-01-15 10:00    |      1
-- Ana    | 200.00 | 2025-01-20 15:30    |      2
-- Luis   |  75.00 | 2025-01-18 12:00    |      1
```

### RANK()

Asigna un ranking con **huecos** en caso de empate.

```sql
-- Ranking de productos por precio
SELECT
    nombre,
    precio,
    RANK() OVER (ORDER BY precio DESC) AS ranking
FROM productos;

-- Resultado:
-- nombre     | precio  | ranking
-- -----------|---------|--------
-- Laptop     | 999.99  |   1
-- Tablet     | 499.99  |   2
-- Monitor    | 299.99  |   3
-- Teclado    |  79.99  |   4
```

### D_RANK()

Igual que RANK() pero **sin huecos**.

```sql
SELECT
    nombre,
    precio,
    RANK() OVER (ORDER BY precio DESC) AS ranking,
    DENSE_RANK() OVER (ORDER BY precio DESC) AS ranking_denso
FROM productos;

-- Con empates:
-- nombre  | precio | ranking | ranking_denso
-- --------|--------|---------|---------------
-- A       | 100.00 |    1    |      1
-- B       | 100.00 |    1    |      1
-- C       |  50.00 |    3    |      2    ← RANK salta al 3, DENSE_RANK va al 2
```

### Comparacion de funciones de ranking

| Funcion         | Empate      | Huecos     | Ejemplo con empate          |
|-----------------|-------------|------------|------------------------------|
| `ROW_NUMBER()`  | Siempre unico| Nunca      | 1, 2, 3, 4 (sin empates)   |
| `RANK()`        | Mismo ranking| **Si**     | 1, 1, 3, 4 (salta el 2)    |
| `DENSE_RANK()`  | Mismo ranking| **No**     | 1, 1, 2, 3 (sin saltos)    |

### NTILE()

Divide los resultados en N grupos (buckets) iguales.

```sql
-- Dividir productos en 4 grupos de precio
SELECT
    nombre,
    precio,
    NTILE(4) OVER (ORDER BY precio ASC) AS cuartil
FROM productos;

-- Resultado:
-- nombre     | precio  | cuartil
-- -----------|---------|--------
-- Mouse      |  25.00  |   1     ← 25% mas baratos
-- Teclado    |  79.99  |   1
-- Monitor    | 299.99  |   2     ← 25%-50%
-- Tablet     | 499.99  |   3     ← 50%-75%
-- Laptop     | 999.99  |   4     ← 25% mas caros
```

### Funciones de ventana comunes

| Funcion              | Que hace                                    | Ejemplo                                      |
|----------------------|---------------------------------------------|----------------------------------------------|
| `ROW_NUMBER()`       | Numero secuencial unico                     | `ROW_NUMBER() OVER (ORDER BY fecha DESC)`    |
| `RANK()`             | Ranking con huecos en empates               | `RANK() OVER (ORDER BY precio DESC)`         |
| `DENSE_RANK()`       | Ranking sin huecos                          | `DENSE_RANK() OVER (ORDER BY precio DESC)`   |
| `NTILE(n)`           | Divide en n grupos iguales                  | `NTILE(4) OVER (ORDER BY precio)`            |
| `LAG(col, n)`        | Valor de la fila anterior (n filas atras)   | `LAG(total, 1) OVER (ORDER BY fecha)`        |
| `LEAD(col, n)`       | Valor de la fila siguiente                  | `LEAD(total, 1) OVER (ORDER BY fecha)`       |
| `FIRST_VALUE(col)`   | Primer valor del grupo                      | `FIRST_VALUE(precio) OVER (...)`             |
| `LAST_VALUE(col)`    | Ultimo valor del grupo                      | `LAST_VALUE(precio) OVER (...)`              |
| `SUM() OVER()`       | Suma acumulada                              | `SUM(total) OVER (ORDER BY fecha)`           |
| `AVG() OVER()`       | Promedio movil                              | `AVG(total) OVER (ORDER BY fecha ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` |

---

## Patrones comunes

### Top N por grupo

```sql
-- Los 3 productos mas caros por categoria
SELECT *
FROM (
    SELECT
        nombre,
        precio,
        categoria_id,
        ROW_NUMBER() OVER (
            PARTITION BY categoria_id
            ORDER BY precio DESC
        ) AS rn
    FROM productos
) ranked
WHERE rn <= 3;
```

### Running total (total acumulado)

```sql
-- Total acumulado de ventas por dia
SELECT
    created_at::DATE AS dia,
    total,
    SUM(total) OVER (
        ORDER BY created_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS total_acumulado
FROM pedidos
ORDER BY created_at;
```

### Diferencia con la fila anterior

```sql
-- Cambio de precio respecto al dia anterior
SELECT
    created_at::DATE AS dia,
    total,
    total - LAG(total, 1) OVER (ORDER BY created_at) AS cambio
FROM pedidos
ORDER BY created_at;
```

### Porcentaje del total

```sql
-- Cada venta como porcentaje del total
SELECT
    u.nombre,
    p.total,
    ROUND(
        p.total / SUM(p.total) OVER () * 100,
        2
    ) AS porcentaje
FROM pedidos p
INNER JOIN usuarios u ON p.usuario_id = u.id
ORDER BY porcentaje DESC;
```

---

## Fuentes

- [PostgreSQL 18 Documentation - Chapter 9: Functions and Operators](https://www.postgresql.org/docs/18/functions.html)
- [PostgreSQL Documentation - Aggregate Functions](https://www.postgresql.org/docs/18/functions-aggregate.html)
- [PostgreSQL Documentation - Window Functions](https://www.postgresql.org/docs/18/tutorial-window.html)
- [W3Schools - SQL GROUP BY](https://www.w3schools.com/sql/sql_groupby.asp)
- [W3Schools - SQL HAVING](https://www.postgresql.org/docs/18/queries-table-expressions.html#QUERIES-GROUPING)

---

> **Siguiente archivo:** [08 - Cheatsheet SQL](08-cheatsheet-sql.md)
