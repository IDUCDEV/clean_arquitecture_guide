# Practica 1: CRUD Completo -- E-commerce

> Construye el esquema de una plataforma de e-commerce desde cero: crearas tablas, insertaras datos, resolveras consultas progresivas y agregaras constraints e indices. Todo en SQL puro.

Objetivo: Ser capaz de disenar, crear y consultar un esquema relacional completo para un sistema de comercio electronico.

```
+-----------------------------------------------------------------+
|                        ESQUEMA E-COMMERCE                       |
|                                                                 |
|  +========+       +========+       +============+             |
|  |  users  |       |  orders |       | order_items |             |
|  | id(PK)  |------>|user_id|------>| order_id   |---+         |
|  | name    |       | id(PK) |       | product_id |   |         |
|  | email   |       | total  |       | quantity   |   |         |
|  +========+       | status |       | unit_price  |   |         |
|                   +========+       +============+   |         |
|  +========+       +========+                        |         |
|  |categories|       |products|                       |         |
|  | id(PK)  |------>|cat_id(FK)|                       |         |
|  | name    |       | id(PK)  |<----------------------+         |
|  | desc    |       | price   |                                  |
|  +========+       +========+                                  |
+-----------------------------------------------------------------+
## Fase 1: Crear tablas y poblar datos

DDL para las tablas del e-commerce, luego insertaremos datos de ejemplo.

### 1.1 Crear tabla users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|--------------|--------------|
| id | SERIAL | PRIMARY KEY | Identificador unico autoincremental |
| name | VARCHAR(100) | NOT NULL | Nombre completo del usuario |
| email | VARCHAR(255) | NOT NULL, UNIQUE | Correo electronico, sin duplicados |
| password_hash | VARCHAR(255) | NOT NULL | Hash del password (nunca texto plano) |
| phone | VARCHAR(20) | | Telefono de contacto |
| address | TEXT | | Direccion postal |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | Fecha de creacion |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | Ultima modificacion |

### 1.2 Crear tabla categories

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 1.3 Crear tabla products

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    image_url VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|--------------|--------------|
| category_id | INTEGER | NOT NULL, FK -> categories(id) | Llave foranea a categoria |
| price | NUMERIC(10,2) | NOT NULL | Precio con 2 decimales |
| stock | INTEGER | NOT NULL, DEFAULT 0 | Unidades disponibles en inventario |
| is_active | BOOLEAN | DEFAULT TRUE | Producto activo/desactivado |

### 1.4 Crear tabla orders

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    order_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    total NUMERIC(12, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    shipping_address TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### 1.5 Crear tabla order_items

```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,
    total_price NUMERIC(10, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|--------------|--------------|
| order_id | INTEGER | FK -> orders(id) | Pedido al que pertenece |
| product_id | INTEGER | FK -> products(id) | Producto seleccionado |
| quantity | INTEGER | CHECK(quantity > 0) | Cantidad adquirida |
| unit_price | NUMERIC(10,2) | NOT NULL | Precio del producto al momento de compra |
| total_price | NUMERIC(10,2) | GENERATED ALWAYS AS | Columna calculada: qty * unit_price |

### 1.6 Insertar datos de ejemplo

```sql
-- categories
INSERT INTO categories (name, description) VALUES
('Electronica', 'Dispositivos y gadgets electronicos'),
('Ropa', 'Prendas de vestir'),
('Libros', 'Libros fisicos y digitales'),
('Hogar', 'Articulos para el hogar'),
('Deportes', 'Equipamiento deportivo');

-- products
INSERT INTO products (category_id, name, description, price, stock) VALUES
(1, 'Smartphone X10', 'Smartphone de ultima generacion', 799.99, 50),
(1, 'Audifonos Bluetooth', 'Audifonos inalambricos con cancelacion de ruido', 149.99, 200),
(2, 'Camiseta Algodon', 'Camiseta clasica de algodon organico', 29.99, 500),
(2, 'Zapatillas Running', 'Zapatillas ligeras para running', 129.99, 150),
(3, 'Clean Code', 'Robert C. Martin - guia de buenas practicas', 45.00, 300),
(4, 'Lampara LED', 'Lampara de escritorio LED ajustable', 59.99, 100),
(5, 'Balon Futbol', 'Balon oficial para futbol', 35.00, 200),
(1, 'Laptop Zbook', 'Laptop para desarrollo y diseno', 1299.99, 30);

-- users
INSERT INTO users (name, email, password_hash, phone, address) VALUES
('Ana Garcia', 'ana@email.com', 'hash_001', '123456789', 'Calle 1, Lima'),
('Carlos Perez', 'carlos@email.com', 'hash_002', '987654321', 'Calle 2, Medellin'),
('Maria Lopez', 'maria@email.com', 'hash_003', '555555555', 'Calle 3, Mexico');

-- orders (total se actualizara con triggers/backend)
INSERT INTO orders (user_id, total, status) VALUES
(1, 0, 'completed'),
(2, 0, 'pending'),
(3, 0, 'completed'),
(1, 0, 'pending');

-- order_items
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 799.99),
(1, 2, 1, 149.99),
(2, 6, 1, 59.99),
(3, 8, 1, 1299.99),
(3, 2, 1, 149.99),
(3, 5, 2, 45.00),
(4, 7, 1, 35.00);
```

## Fase 2: Consultas progresivas

8 ejercicios. Intenta resolverlos por tu cuenta antes de ver la solucion.

---

### Ejercicio 1: Listar productos con nombre de categoria

**Problema:** Quieres un listado de productos donde aparezca el nombre de la categoria.

**Solucion (INNER JOIN):**

```sql
SELECT p.name AS producto, c.name AS categoria, p.price, p.stock
FROM products p
INNER JOIN categories c ON p.category_id = c.id
ORDER BY categoria, p.name;
```

**Resultado esperado:**

| producto | categoria | price | stock |
|----------|-----------|-------|-------|
| Balon Futbol | Deportes | 35.00 | 200 |
| Audifonos Bluetooth | Electronica | 149.99 | 200 |
| Laptop Zbook | Electronica | 1299.99 | 30 |
| Smartphone X10 | Electronica | 799.99 | 50 |
| Lampara LED | Hogar | 59.99 | 100 |
| Clean Code | Libros | 45.00 | 300 |
| Camiseta Algodon | Ropa | 29.99 | 500 |
| Zapatillas Running | Ropa | 129.99 | 150 |

Conceptos: INNER JOIN, ALIAS, ORDER BY.

---

### Ejercicio 2: Contar productos por categoria

**Problema:** Cuantos productos hay en cada categoria.

**Solucion (LEFT JOIN + GROUP BY):**

```sql
SELECT c.name AS categoria, COUNT(p.id) AS cantidad
FROM categories c
LEFT JOIN products p ON p.category_id = c.id
GROUP BY c.name
ORDER BY cantidad DESC;
```

| categoria | cantidad |
|-----------|----------|
| Electronica | 3 |
| Ropa | 2 |
| Deportes | 1 |
| Hogar | 1 |
| Libros | 1 |

Conceptos: LEFT JOIN (no elimina categorias vacias), GROUP BY, COUNT.

---

### Ejercicio 3: Pedidos con total acumulado

**Problema:** Reporte con cada pedido, cliente, items y total.

**Solucion (3-table JOIN + GROUP BY + SUM):**

```sql
SELECT
    o.id AS pedido,
    u.name AS cliente,
    COUNT(oi.id) AS items,
    SUM(oi.total_price) AS total
FROM orders o
INNER JOIN users u ON o.user_id = u.id
INNER JOIN order_items oi ON oi.order_id = o.id
GROUP BY o.id, u.name
ORDER BY total DESC;
```

| pedido | cliente | items | total |
|--------|---------|-------|-------|
| 3 | Maria Lopez | 4 | 1539.97 |
| 1 | Ana Garcia | 2 | 949.98 |
| 2 | Carlos Perez | 1 | 59.99 |
| 4 | Ana Garcia | 1 | 35.00 |

Conceptos: JOIN de 3 tablas, COUNT + SUM con GROUP BY.

---

### Ejercicio 4: Busqueda por nombre (coincidencia parcial)

**Problema:** Productos cuyo nombre contenga "cam" (case-insensitive).

**Solucion (ILIKE):**

```sql
SELECT name, price, description
FROM products
WHERE name ILIKE '%cam%' OR description ILIKE '%cam%';
```

| name | price | description |
|------|-------|-------------|
| Camiseta Algodon | 29.99 | Camiseta clasica de algodon organico |
| Lampara LED | 59.99 | Lampara de escritorio LED ajustable |

ILIKE = LIKE que ignora mayusculas/minusculas. % es comodin (cualquier secuencia).

---

### Ejercicio 5: producto mas caro por categoria

**Problema:** Encuentra el producto mas caro dentro de cada categoria.

**Solucion (ventana ROW_NUMBER + CTE):**

```sql
WITH ranked AS (
    SELECT
        p.name AS producto,
        p.price,
        c.name AS categoria,
        ROW_NUMBER() OVER (
            PARTITION BY p.category_id
            ORDER BY p.price DESC
        ) AS rn
    FROM products p
    INNER JOIN categories c ON p.category_id = c.id
)
SELECT producto, price, categoria
FROM ranked
WHERE rn = 1
ORDER BY price DESC;
```

| producto | price | categoria |
|----------|-------|-----------|
| Laptop Zbook | 1299.99 | Electronica |
| Zapatillas Running | 129.99 | Ropa |
| Lampara LED | 59.99 | Hogar |
| Clean Code | 45.00 | Libros |
| Balon Futbol | 35.00 | Deportes |

ROW_NUMBER() numera dentro de cada PARTITION BY categoria, ordenado por price DESC. rn=1 es el mas caro.

---

### Ejercicio 6: Paginacion de resultados

**Problema:** Productos de 2 en 2, salta los dos primeros.

**Solucion (LIMIT/OFFSET):**

```sql
SELECT name, price
FROM products
ORDER BY name
LIMIT 2 OFFSET 2;
```

| name | price |
|------|-------|
| Balon Futbol | 35.00 |
| Camiseta Algodon | 29.99 |

Pagina 1: LIMIT 2 OFFSET 0. Pagina 2: LIMIT 2 OFFSET 2. Pagina N: LIMIT 2 OFFSET (N-1)*2.

---

### Ejercicio 7: Upsert de un producto

**Problema:** Insertar o actualizar un producto si ya existe (name unico).

**Paso previo: agregar UNIQUE en name**

```sql
CREATE UNIQUE INDEX products_name_uniq ON products(name);
```

**Solucion (INSERT ... ON CONFLICT):**

```sql
INSERT INTO products (category_id, name, description, price, stock)
VALUES (1, 'Smartphone X10', 'Smartphone actualizado', 749.99, 90)
ON CONFLICT (name)
DO UPDATE SET
    price = EXCLUDED.price,
    stock = EXCLUDED.stock,
    updated_at = NOW();
```

Smartphone X10 existia, ahora su precio bajo de 799.99 a 749.99 y stock subio de 50 a 90.

Conceptos: ON CONFLICT, EXCLUDED, DO UPDATE vs DO NOTHING.

---

### Ejercicio 8: Eliminar item y actualizar total

**Problema:** Eliminar el Smartphone del pedido 1 y actualizar el total.

**Solucion (transaccion):**

```sql
BEGIN;

DELETE FROM order_items
WHERE order_id = 1 AND product_id = 1;

UPDATE orders
SET total = (
    SELECT COALESCE(SUM(total_price), 0)
    FROM order_items
    WHERE order_id = 1
),
updated_at = NOW()
WHERE id = 1;

COMMIT;
```

Antes: pedido 1 tenia 2 items (Smartphone 799.99 + Audifonos 149.99 = 949.98).
Despues: queda Audifonos, total actualizado a 149.99.

Conceptos: DELETE con WHERE, subconsulta, COALESCE(SUM(...), 0), transaccion.

## Fase 3: Agregar constraints e indices

### 3.1 CHECK para precio positivo

```sql
ALTER TABLE products
ADD CONSTRAINT check_precio_positivo
CHECK (price > 0);
```

### 3.2 Indice compuesto para busquedas comunes

```sql
CREATE INDEX idx_products_cat_active
ON products(category_id, is_active);
```

Las busquedas que usan ambas columnas se beneficiaran de este indice:

```sql
SELECT name, price FROM products
WHERE category_id = 1 AND is_active = TRUE
ORDER BY price;
```

### 3.3 Foreign key con ON DELETE CASCADE

```sql
-- Eliminar constraint existente
ALTER TABLE products DROP CONSTRAINT products_category_id_fkey;

-- Re-crear con CASCADE
ALTER TABLE products
ADD CONSTRAINT products_category_id_fkey
FOREIGN KEY (category_id) REFERENCES categories(id)
ON DELETE CASCADE;
```

**Tipos de ON DELETE:**

| Opcion | Comportamiento |
|--------|---------------|
| RESTRICT (default) | Impide borrar la categoria si tiene productos |
| CASCADE | Borra automaticamente los productos de la categoria |
| SET NULL | Pone category_id = NULL en los productos afectados |
| SET DEFAULT | Pone el valor default definido en la columna |

**Recomendacion:** Usa RESTRICT (el default) para la mayoria de casos. CASCADE solo cuando estes seguro de que quieres borrar en cascada.

## Resumen

```
+----------------------------------------------------------------+
|                       RESUMEN DE LA PRACTICA                    |
|                                                                  |
|  Fase 1: DDL + seed data                                        |
|   - 5 tablas con FK, CHECK, GENERATED COLUMNS                   |
|                                                                  |
|  Fase 2: 8 ejercicios progresivos                               |
|   - JOIN, LEFT JOIN, GROUP BY, ILIKE, ROW_NUMBER                |
|   - LIMIT/OFFSET, ON CONFLICT, transacciones                    |
|                                                                  |
|  Fase 3: Constraints finales                                     |
|   - CHECK, indices compuestos, ON DELETE CASCADE                |
|                                                                  |
|  Tiempo: ~60 min                                                 |
+----------------------------------------------------------------+
```

> **Siguiente paso:** [Practica 2: Modelado Relacional](02-practica-modelado-relacional.md)


## Bonus Exercises

### Bonus 1: Top 3 productos mas vendidos

**Problema:** Necesitas un ranking de los 3 productos mas vendidos (por cantidad total de items).

**Solucion (GROUP BY + ORDER BY + LIMIT):**

```sql
SELECT p.name AS producto, SUM(oi.quantity) AS cantidad_vendida
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.id
GROUP BY p.id, p.name
ORDER BY cantidad_vendida DESC
LIMIT 3;
```

| producto | cantidad_vendida |
|----------|------------------|
| Clean Code | 2 |
| Audifonos Bluetooth | 2 |
| Smartphone X10 | 1 |

### Bonus 2: Clientes con mas pedidos

**Problema:** Muestra los clientes que tienen mas de 1 pedido, ordenados por cantidad de pedidos.

**Solucion (HAVING):**

```sql
SELECT u.name AS cliente, COUNT(o.id) AS cantidad_pedidos, SUM(o.total) AS total_gastado
FROM users u
INNER JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 1
ORDER BY total_gastado DESC;
```

| cliente | cantidad_pedidos | total_gastado |
|---------|------------------|---------------|
| Ana Garcia | 2 | 984.98 |

Ana tiene 2 pedidos: el 1 (completado) y el 4 (pendiente). Carlos y Maria solo tienen 1 cada uno, por lo que son filtrados por HAVING.

### Bonus 3: Dias entre pedidos

**Problema:** Para un cliente (Ana), calcular cuantos dias pasaron entre su primer pedido y el segundo.

**Solucion (funciones de ventana LEAD/LAG):**

```sql
WITH pedidos_ordenados AS (
    SELECT
        o.id,
        u.name AS cliente,
        o.order_date,
        LAG(o.order_date) OVER (ORDER BY o.order_date) AS fecha_pedido_anterior
    FROM orders o
    INNER JOIN users u ON o.user_id = u.id
    WHERE u.id = 1
)
SELECT
    id AS pedido,
    cliente,
    order_date AS fecha_pedido,
    fecha_pedido_anterior,
    COALESCE(DATE(order_date) - DATE(fecha_pedido_anterior), 0) AS dias_desde_anterior
FROM pedidos_ordenados;
```

Este query usa la funcin de ventana LAG() para acceder al valor de la fila anterior sin agrupar ni self-join. La diferencia de fechas se calcula directamente restando los valores de DATE.

### Bonus 4: Comparacin de precio de producto vs precio promedio de su categora

**Problema:** Quieres saber si un producto es ms caro o ms barato que el promedio de su categora.

**Solucion (funcin de ventana AVG OVER + PARTITION):**

```sql
SELECT p.name, p.price, c.name AS categoria,
       AVG(p.price) OVER (PARTITION BY p.category_id) AS precio_promedio_categoria,
       ROUND(p.price - AVG(p.price) OVER (PARTITION BY p.category_id), 2) AS diferencia
FROM products p
INNER JOIN categories c ON p.category_id = c.id
ORDER BY c.name, p.name;
```

| name | price | categoria | precio_promedio_categoria | diferencia |
|------|-------|-----------|---------------------------|------------|
| Audifonos Bluetooth | 149.99 | Electronica | 749.99 | -600.00 |
| Laptop Zbook | 1299.99 | Electronica | 749.99 | 550.00 |
| Smartphone X10 | 799.99 | Electronica | 749.99 | 50.00 |

Con AVG() OVER (PARTITION BY category_id) podemos calcular promedios por categora sin usar GROUP BY.


**Tiempo total con bonuses: ~75 min**

> **Siguiente paso:** [Practica 2: Modelado Relacional](02-practica-modelado-relacional.md)
