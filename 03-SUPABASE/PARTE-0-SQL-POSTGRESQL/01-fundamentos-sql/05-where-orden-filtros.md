# 05 - WHERE, ORDER BY, LIMIT, filtros

> Los filtros te permiten seleccionar exactamente los registros que necesitas. Sin filtros, cada SELECT devolveria todos los registros de la tabla.

```
┌──────────────────────────────────────────────────────────────┐
│                    RESUMEN RAPIDO                             │
│                                                              │
│  WHERE      → Filtrar registros por condicion                │
│  ORDER BY   → Ordenar resultados (ASC o DESC)                │
│  LIMIT      → Limitar cantidad de resultados                 │
│  OFFSET     → Saltar N registros (para paginacion)           │
│  DISTINCT   → Eliminar duplicados                            │
│  LIKE/ILIKE → Busqueda por patron de texto                   │
└──────────────────────────────────────────────────────────────┘
```

## Indice

1. [WHERE basico](#where-basico)
2. [Operadores de comparacion](#operadores-de-comparacion)
3. [AND, OR, NOT](#and-or-not)
4. [LIKE e ILIKE](#like-e-ilike)
5. [IN](#in)
6. [BETWEEN](#between)
7. [IS NULL / IS NOT NULL](#is-null--is-not-null)
8. [ORDER BY](#order-by)
9. [LIMIT y OFFSET](#limit-y-offset)
10. [DISTINCT](#distinct)
11. [Aliases](#aliases)

---

## WHERE basico

Filtra registros basandose en una condicion.

```sql
-- Obtener solo usuarios activos
SELECT * FROM usuarios
WHERE activo = true;

-- Obtener productos con precio mayor a 100
SELECT nombre, precio FROM productos
WHERE precio > 100;

-- Obtener usuario por ID
SELECT * FROM usuarios
WHERE id = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
```

---

## Operadores de comparacion

| Operador | Significado                | Ejemplo                                       |
|----------|----------------------------|-------------------------------------------------|
| `=`      | Igual a                    | `WHERE nombre = 'Ana'`                         |
| `!=`     | No igual a                 | `WHERE rol != 'admin'`                         |
| `<>`     | No igual a (estandar SQL)  | `WHERE rol <> 'admin'`                         |
| `<`      | Menor que                  | `WHERE precio < 100`                           |
| `>`      | Mayor que                  | `WHERE precio > 100`                           |
| `<=`     | Menor o igual que          | `WHERE stock <= 10`                            |
| `>=`     | Mayor o igual que          | `WHERE stock >= 5`                             |

```sql
-- Ejemplos de uso
SELECT * FROM productos WHERE precio > 50;
SELECT * FROM productos WHERE precio >= 50 AND precio <= 200;
SELECT * FROM usuarios WHERE rol = 'admin';
SELECT * FROM usuarios WHERE activo != false;
```

---

## AND, OR, NOT

Combina multiples condiciones con operadores logicos.

| Operador | Significado        | Ejemplo                                              |
|----------|--------------------|-------------------------------------------------------|
| `AND`    | Ambas deben ser verdaderas | `WHERE precio > 50 AND stock > 0`              |
| `OR`     | Al menos una verdadera    | `WHERE rol = 'admin' OR rol = 'moderator'`     |
| `NOT`    | Niega la condicion        | `WHERE NOT activo`                              |

```sql
-- AND: ambas condiciones deben cumplirse
SELECT * FROM productos
WHERE precio > 50 AND stock > 0;

-- OR: al menos una condicion se cumple
SELECT * FROM usuarios
WHERE rol = 'admin' OR rol = 'moderator';

-- NOT: niega la condicion
SELECT * FROM usuarios
WHERE NOT activo;

-- Combinaciones
SELECT * FROM productos
WHERE (precio > 50 OR stock > 10) AND activo = true;
```

**Orden de precedencia:**

```
┌──────────────────────────────────────────────────────────┐
│  PRECEDENCIA DE OPERADORES (de mayor a menor)            │
│                                                          │
│  1. NOT                                                  │
│  2. AND                                                  │
│  3. OR                                                   │
│                                                          │
│  Usa parentesis para forzar el orden deseado             │
└──────────────────────────────────────────────────────────┘
```

---

## LIKE e ILIKE

Busqueda por patron de texto.

| Operador | Case-sensitive | Ejemplo                                      |
|----------|----------------|-----------------------------------------------|
| `LIKE`   | Si             | `WHERE nombre LIKE '%ana%'` (encuentra "Ana") |
| `ILIKE`  | **No** (PostgreSQL) | `WHERE nombre ILIKE '%ana%'` (encuentra "ana", "ANA", "Ana") |

**Patrones:**

| Patron     | Significado                        | Ejemplo                                       |
|------------|-------------------------------------|------------------------------------------------|
| `%`        | Cualquier conjunto de caracteres    | `'%@gmail.com'` = termina en @gmail.com       |
| `_`        | Un solo caracter                    | `'A_'` = A seguido de un caracter             |
| `LIKE`     | Busqueda exacta (case-sensitive)    | `'Ana%'` = empieza con Ana (case-sensitive)   |
| `ILIKE`    | Busqueda insensible a mayusculas    | `'ana%'` = empieza con ana (cualquier caso)   |

```sql
-- Buscar emails de Gmail
SELECT * FROM usuarios
WHERE email ILIKE '%@gmail.com%';

-- Buscar nombres que empiezan con 'A'
SELECT * FROM usuarios
WHERE nombre LIKE 'A%';

-- Buscar nombres que terminan con 'ez'
SELECT * FROM usuarios
WHERE nombre ILIKE '%ez';

-- Buscar nombres con exactamente 5 caracteres
SELECT * FROM usuarios
WHERE nombre LIKE '_____';

-- Buscar que contiene 'tech'
SELECT * FROM productos
WHERE nombre ILIKE '%tech%';
```

**Escapar caracteres especiales:**

```sql
-- Buscar literalmente un % (usar ESCAPE)
SELECT * FROM productos
WHERE descripcion LIKE '100%%' ESCAPE '\';
```

---

## IN

Verifica si un valor esta dentro de una lista o subquery.

### IN con lista

```sql
-- Obtener usuarios con ciertos roles
SELECT * FROM usuarios
WHERE rol IN ('admin', 'moderator');

-- Lo mismo que multiples OR
SELECT * FROM usuarios
WHERE rol = 'admin' OR rol = 'moderator';

-- Obtener productos con ciertos IDs
SELECT * FROM productos
WHERE id IN (
    'uuid-1', 'uuid-2', 'uuid-3'
);
```

### IN con subquery

```sql
-- Obtener productos de categorias activas
SELECT * FROM productos
WHERE categoria_id IN (
    SELECT id FROM categorias WHERE activa = true
);

-- Obtener usuarios que tienen pedidos
SELECT * FROM usuarios
WHERE id IN (
    SELECT DISTINCT usuario_id FROM pedidos
);
```

### NOT IN

```sql
-- Obtener usuarios que NO son admin
SELECT * FROM usuarios
WHERE rol NOT IN ('admin');

-- Obtener productos sin pedidos
SELECT * FROM productos
WHERE id NOT IN (
    SELECT DISTINCT producto_id FROM detalle_pedido
);
```

> **Cuidado con NOT IN y NULLs:** Si la subquery devuelve NULLs, `NOT IN` puede fallar. Usa `NOT EXISTS` en su lugar.

---

## BETWEEN

Filtra valores dentro de un rango (inclusivo en ambos extremos).

```sql
-- Productos con precio entre 50 y 200
SELECT * FROM productos
WHERE precio BETWEEN 50 AND 200;

-- Lo mismo que:
SELECT * FROM productos
WHERE precio >= 50 AND precio <= 200;

-- Fechas en un rango
SELECT * FROM pedidos
WHERE created_at BETWEEN '2025-01-01' AND '2025-12-31';

-- NOT BETWEEN: fuera del rango
SELECT * FROM productos
WHERE precio NOT BETWEEN 50 AND 200;
```

---

## IS NULL / IS NOT NULL

Verifica si un valor es NULL (no tiene valor).

```sql
-- Usuarios sin telefono
SELECT * FROM usuarios
WHERE telefono IS NULL;

-- Usuarios CON telefono
SELECT * FROM usuarios
WHERE telefono IS NOT NULL;

-- ⚠️ ERROR: no usar = NULL o != NULL
SELECT * FROM usuarios WHERE telefono = NULL;     -- ❌ WRONG
SELECT * FROM usuarios WHERE telefono IS NULL;    -- ✅ CORRECT
```

> **Importante:** `NULL = NULL` retorna `NULL`, no `true`. Siempre usa `IS NULL` o `IS NOT NULL` para comparar con NULL.

---

## ORDER BY

Ordena los resultados por una o mas columnas.

```sql
-- Ordenar por nombre (A-Z)
SELECT * FROM usuarios
ORDER BY nombre ASC;

-- Ordenar por precio (mayor a menor)
SELECT * FROM productos
ORDER BY precio DESC;

-- Ordenar por multiples columnas
SELECT * FROM productos
ORDER BY categoria_id ASC, precio DESC;

-- Ordenar por columna numerica (posicion)
SELECT nombre, email, rol FROM usuarios
ORDER BY 3;  -- Ordena por la 3er columna (rol)
```

**ASC vs DESC:**

| Valor   | Significado                  | Ejemplo                          |
|---------|------------------------------|------------------------------------|
| `ASC`   | Ascendente (A-Z, 0-9)       | `ORDER BY nombre ASC` (default)   |
| `DESC`  | Descendente (Z-A, 9-0)      | `ORDER BY precio DESC`            |

**Ordenar con NULLs:**

```sql
-- NULLs al final
SELECT * FROM usuarios
ORDER BY telefono ASC NULLS LAST;

-- NULLs al inicio
SELECT * FROM usuarios
ORDER BY telefono ASC NULLS FIRST;
```

---

## LIMIT y OFFSET

Controla la cantidad de resultados y la paginacion.

### LIMIT

```sql
-- Obtener los primeros 10 usuarios
SELECT * FROM usuarios
LIMIT 10;

-- Obtener el usuario mas reciente
SELECT * FROM usuarios
ORDER BY created_at DESC
LIMIT 1;
```

### OFFSET (paginacion)

```sql
-- Paginacion: pagina 1 (registros 1-10)
SELECT * FROM usuarios
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;

-- Paginacion: pagina 2 (registros 11-20)
SELECT * FROM usuarios
ORDER BY created_at DESC
LIMIT 10 OFFSET 10;

-- Paginacion: pagina 3 (registros 21-30)
SELECT * FROM usuarios
ORDER BY created_at DESC
LIMIT 10 OFFSET 20;
```

**Formula de paginacion:**

```
OFFSET = (pagina - 1) * LIMIT

Pagina 1: OFFSET = (1 - 1) * 10 = 0
Pagina 2: OFFSET = (2 - 1) * 10 = 10
Pagina 3: OFFSET = (3 - 1) * 10 = 20
```

**En Supabase (Dart):**

```dart
// Supabase maneja la paginacion automaticamente
final response = await supabase
    .from('usuarios')
    .select()
    .range(0, 9);  // Pagina 1: registros 0-9

final response2 = await supabase
    .from('usuarios')
    .select()
    .range(10, 19); // Pagina 2: registros 10-19
```

> **Nota:** `LIMIT ... OFFSET` es simple pero ineficiente para paginas lejanas. Para paginacion avanzada usa **cursor-based pagination** con `WHERE id > ultimo_id`.

---

## DISTINCT

Elimina filas duplicadas del resultado.

```sql
-- Obtener roles unicos
SELECT DISTINCT rol FROM usuarios;

-- Contar roles unicos
SELECT COUNT(DINCT rol) AS total_roles FROM usuarios;

-- Combinacion unica de columnas
SELECT DISTINCT nombre, email FROM usuarios;

-- Contar usuarios unicos que hicieron pedidos
SELECT COUNT(DISTINCT usuario_id) AS total_usuarios_con_pedidos
FROM pedidos;
```

---

## Aliases

Renombra columnas o tablas temporalmente en la consulta.

### Aliases de columna

```sql
-- Renombrar columnas en el resultado
SELECT
    nombre AS nombre_usuario,
    email AS correo,
    created_at AS fecha_registro
FROM usuarios;

-- Calcular y renombrar
SELECT
    nombre,
    precio,
    stock,
    precio * stock AS valor_inventario
FROM productos;

-- Sin AS tambien funciona (pero es menos claro)
SELECT
    nombre nombre_usuario,
    email correo
FROM usuarios;
```

### Aliases de tabla

```sql
-- Abreviar nombres de tablas
SELECT u.nombre, u.email
FROM usuarios u;

-- En JOINs (esencial)
SELECT
    u.nombre AS usuario,
    p.total AS monto_pedido
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id;

-- Subqueries con alias
SELECT *
FROM (SELECT nombre, email FROM usuarios WHERE activo = true) AS usuarios_activos;
```

---

## Resumen

| Clave         | Funcion                        | Ejemplo                                         |
|---------------|--------------------------------|--------------------------------------------------|
| `WHERE`       | Filtrar registros              | `WHERE precio > 100`                             |
| `AND`         | Ambas condiciones verdaderas   | `WHERE precio > 50 AND stock > 0`               |
| `OR`          | Al menos una verdadera         | `WHERE rol = 'admin' OR rol = 'mod'`             |
| `NOT`         | Negar condicion                | `WHERE NOT activo`                               |
| `LIKE/ILIKE`  | Patron de texto                | `WHERE nombre ILIKE '%ana%'`                     |
| `IN`          | Valor en lista                 | `WHERE rol IN ('admin', 'mod')`                  |
| `BETWEEN`     | Dentro de rango                | `WHERE precio BETWEEN 50 AND 200`                |
| `IS NULL`     | Es nulo                        | `WHERE telefono IS NULL`                         |
| `ORDER BY`    | Ordenar                        | `ORDER BY precio DESC`                           |
| `LIMIT`       | Limitar resultados             | `LIMIT 10`                                      |
| `OFFSET`      | Saltar registros               | `OFFSET 20`                                     |
| `DISTINCT`    | Sin duplicados                 | `SELECT DISTINCT rol`                            |
| `AS`          | Alias                          | `SELECT nombre AS nombre_usuario`                |

---

## Fuentes

- [PostgreSQL 18 Documentation - Chapter 7: Queries](https://www.postgresql.org/docs/18/queries.html)
- [PostgreSQL Documentation - WHERE](https://www.postgresql.org/docs/18/functions-comparison.html)
- [W3Schools - SQL WHERE](https://www.w3schools.com/sql/sql_where.asp)
- [PostgreSQL Documentation - LIMIT/OFFSET](https://www.postgresql.org/docs/18/queries-limit.html)

---

> **Siguiente archivo:** [06 - JOIN y relaciones](06-join-relaciones.md)
