# 04 - DML: SELECT, INSERT, UPDATE, DELETE

> DML (Data Manipulation Language) es el conjunto de comandos que usas para consultar, crear, modificar y eliminar datos en tus tablas. Es el SQL que mas usaras.

```
┌──────────────────────────────────────────────────────────────┐
│                    RESUMEN RAPIDO                             │
│                                                              │
│  SELECT  → Consultar datos (READ)                            │
│  INSERT  → Crear nuevos registros (CREATE)                   │
│  UPDATE  → Modificar registros existentes (UPDATE)           │
│  DELETE  → Eliminar registros (DELETE)                       │
│  RETURNING → Devolver datos afectados por INSERT/UPDATE/DELETE │
│  ON CONFLICT → Upsert (insertar o actualizar)               │
└──────────────────────────────────────────────────────────────┘
```

## Indice

1. [SELECT](#select)
2. [INSERT](#insert)
3. [UPDATE](#update)
4. [DELETE](#delete)
5. [RETURNING](#returning)
6. [ON CONFLICT (Upsert)](#on-conflict-upsert)

---

## SELECT

La sentencia mas usada en SQL. Consulta datos de una o mas tablas.

### Sintaxis basica

```sql
SELECT columna1, columna2, ...
FROM nombre_tabla;
```

### SELECT * (todas las columnas)

```sql
-- Obtener todas las columnas de la tabla
SELECT * FROM usuarios;

-- Obtener todas las columnas de un registro especifico
SELECT * FROM usuarios WHERE id = 1;
```

### Seleccionar columnas especificas

```sql
-- Solo las columnas que necesitas (recomendado)
SELECT nombre, email FROM usuarios;

-- Con alias de columna
SELECT
    nombre AS nombre_usuario,
    email AS correo_electronico
FROM usuarios;
```

### INSERT

Crea nuevos registros en una tabla.

### INSERT una fila

```sql
INSERT INTO usuarios (nombre, email, rol)
VALUES ('Carlos Perez', 'carlos@email.com', 'user');
```

### INSERT multiples filas

```sql
INSERT INTO usuarios (nombre, email, rol) VALUES
    ('Ana Garcia', 'ana@email.com', 'admin'),
    ('Luis Rodriguez', 'luis@email.com', 'user'),
    ('Maria Lopez', 'maria@email.com', 'moderator');
```

### INSERT con columnas especificas

```sql
-- Solo insertar en las columnas que quieras
-- Las demas usan el DEFAULT o quedan NULL
INSERT INTO usuarios (nombre, email)
VALUES ('Pedro Sanchez', 'pedro@email.com');

-- Esto es lo mismo que:
-- INSERT INTO usuarios (nombre, email, rol, activo, created_at)
-- VALUES ('Pedro Sanchez', 'pedro@email.com', 'user', true, NOW());
```

### INSERT con DEFAULT

```sql
-- Especificar el DEFAULT explicitamente
INSERT INTO usuarios (nombre, email, rol, created_at)
VALUES ('Elena Martinez', 'elena@email.com', 'user', DEFAULT);

-- O simplemente omitir la columna (usa el DEFAULT automaticamente)
INSERT INTO usuarios (nombre, email)
VALUES ('Elena Martinez', 'elena@email.com');
```

### INSERT ... SELECT (copiar datos)

```sql
-- Copiar datos de una tabla a otra
INSERT INTO usuarios_backup (nombre, email)
SELECT nombre, email
FROM usuarios
WHERE activo = true;

-- Copiar todos los datos
INSERT INTO usuarios_backup
SELECT * FROM usuarios;
```

---

## UPDATE

Modifica registros existentes.

### Sintaxis basica

```sql
UPDATE nombre_tabla
SET columna1 = valor1, columna2 = valor2, ...
WHERE condicion;
```

### UPDATE basico

```sql
-- Actualizar una columna
UPDATE usuarios
SET nombre = 'Carlos M. Perez'
WHERE id = 1;

-- Actualizar multiples columnas
UPDATE usuarios
SET
    nombre = 'Carlos M. Perez',
    email = 'carlos.nuevo@email.com',
    rol = 'admin'
WHERE id = 1;
```

### UPDATE con expresiones

```sql
-- Incrementar stock en 10
UPDATE productos
SET stock = stock + 10
WHERE id = 5;

-- Actualizar con condicion
UPDATE productos
SET
    precio = precio * 0.9,  -- 10% de descuento
    updated_at = NOW()
WHERE categoria_id = 3;
```

### UPDATE sin WHERE (PELIGRO)

```sql
-- ⚠️ ACTUALIZA TODAS LAS FILAS - CUIDADO
UPDATE usuarios SET rol = 'user';

-- ✅ USA SIEMPRE WHERE para ser especifico
UPDATE usuarios SET rol = 'user' WHERE id = 1;
```

> **Advertencia:** Un `UPDATE` sin `WHERE` modifica **TODOS** los registros de la tabla. Siempre verifica tu consulta con un `SELECT` primero.

---

## DELETE

Elimina registros de una tabla.

### Sintaxis basica

```sql
DELETE FROM nombre_tabla
WHERE condicion;
```

### DELETE basico

```sql
-- Eliminar un registro especifico
DELETE FROM usuarios
WHERE id = 1;

-- Eliminar multiples registros
DELETE FROM usuarios
WHERE activo = false;
```

### DELETE sin WHERE (PELIGRO)

```sql
-- ⚠️ ELIMINA TODAS LAS FILAS - CUIDADO
DELETE FROM usuarios;

-- ✅ USA SIEMPRE WHERE para ser especifico
DELETE FROM usuarios WHERE id = 1;
```

> **Advertencia:** Un `DELETE` sin `WHERE` elimina **TODOS** los registros de la tabla. Siempre verifica tu consulta con un `SELECT` primero.

---

## RETURNING

La clausula `RETURNING` te permite obtener los datos afectados por un INSERT, UPDATE o DELETE. Es **muy util** en Supabase porque te devuelve los datos directamente.

### RETURNING con INSERT

```sql
-- Insertar y obtener el registro creado
INSERT INTO usuarios (nombre, email)
VALUES ('Nuevo Usuario', 'nuevo@email.com')
RETURNING *;

-- Retornar solo columnas especificas
INSERT INTO usuarios (nombre, email)
VALUES ('Otro Usuario', 'otro@email.com')
RETURNING id, nombre, created_at;
```

### RETURNING con UPDATE

```sql
-- Actualizar y obtener el registro modificado
UPDATE usuarios
SET nombre = 'Nombre Actualizado'
WHERE id = 1
RETURNING *;

-- Obtener solo columnas especificas
UPDATE usuarios
SET rol = 'admin'
WHERE id = 1
RETURNING id, nombre, rol;
```

### RETURNING con DELETE

```sql
-- Eliminar y obtener el registro eliminado
DELETE FROM usuarios
WHERE id = 1
RETURNING *;

-- Obtener solo columnas especificas
DELETE FROM usuarios
WHERE activo = false
RETURNING id, nombre, email;
```

> **Tip para Supabase:** `RETURNING *` es lo que Supabase usa internamente. Cuando haces `.insert().select()` en el cliente Dart, se ejecuta internamente un `INSERT ... RETURNING *`.

---

## ON CONFLICT (Upsert)

**Upsert** = INSERT o UPDATE (si el registro ya existe). Es una de las operaciones mas comunes en aplicaciones reales.

### Sintaxis

```sql
INSERT INTO nombre_tabla (columnas)
VALUES (valores)
ON CONFLICT (columna_unica)
DO UPDATE SET
    columna = valor;
```

### ON CONFLICT DO NOTHING

```sql
-- Si ya existe un usuario con ese email, no hacer nada
INSERT INTO usuarios (nombre, email)
VALUES ('Ana', 'ana@email.com')
ON CONFLICT (email)
DO NOTHING;
```

### ON CONFLICT DO UPDATE (upsert)

```sql
-- Si el email ya existe, actualizar el nombre
INSERT INTO usuarios (nombre, email)
VALUES ('Ana Actualizada', 'ana@email.com')
ON CONFLICT (email)
DO UPDATE SET
    nombre = EXCLUDED.nombre,
    updated_at = NOW();
```

**Que es `EXCLUDED`?**

`EXCLUDED` es una tabla especial que contiene los valores que se intentaron insertar.

| Valor                 | Que es                                               |
|-----------------------|-------------------------------------------------------|
| `EXCLUDED.nombre`     | El valor de `nombre` que se intento insertar          |
| `EXCLUDED.email`      | El valor de `email` que se intento insertar           |
| `EXCLUDED.*`          | Todos los valores que se intentaron insertar          |

### Ejemplo completo de upsert

```sql
-- Crear tabla de productos
CREATE TABLE productos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

-- Insertar producto
INSERT INTO productos (nombre, precio, stock)
VALUES ('Laptop', 999.99, 10);

-- Intentar insertar de nuevo (upsert: actualizar stock)
INSERT INTO productos (nombre, precio, stock)
VALUES ('Laptop', 999.99, 5)
ON CONFLICT (nombre)  -- O en la PK: ON CONFLICT (id)
DO UPDATE SET
    stock = productos.stock + EXCLUDED.stock;  -- Sumar 5 al stock existente

-- Resultado: stock = 15 (10 + 5)
```

### ON CONFLICT con condicion (WHERE)

```sql
-- Solo actualizar si el nuevo precio es mayor
INSERT INTO productos (nombre, precio)
VALUES ('Laptop', 1299.99)
ON CONFLICT (nombre)
DO UPDATE SET
    precio = GREATEST(productos.precio, EXCLUDED.precio)
WHERE productos.precio < EXCLUDED.precio;  -- Solo si el nuevo es mayor
```

### Supabase y ON CONFLICT

En el cliente Dart de Supabase, el upsert se usa asi:

```dart
// En Flutter con Supabase
final response = await supabase
    .from('productos')
    .upsert({
      'nombre': 'Laptop',
      'precio': 999.99,
      'stock': 5,
    });

// Internamente ejecuta:
// INSERT INTO productos (nombre, precio, stock)
// VALUES ('Laptop', 999.99, 5)
// ON CONFLICT (nombre)
// DO UPDATE SET precio = EXCLUDED.precio, stock = EXCLUDED.stock;
```

---

## Resumen de DML

| Operacion   | Que hace                         | Ejemplo                                          |
|-------------|----------------------------------|--------------------------------------------------|
| `SELECT`    | Consultar datos                  | `SELECT * FROM usuarios WHERE id = 1;`           |
| `INSERT`    | Crear registros                  | `INSERT INTO usuarios (nombre) VALUES ('Ana');`  |
| `INSERT...SELECT` | Copiar datos de otra tabla | `INSERT INTO backup SELECT * FROM usuarios;`     |
| `UPDATE`    | Modificar registros              | `UPDATE usuarios SET nombre = 'X' WHERE id = 1;` |
| `DELETE`    | Eliminar registros               | `DELETE FROM usuarios WHERE id = 1;`             |
| `RETURNING` | Devolver datos afectados         | `INSERT ... RETURNING *;`                        |
| `ON CONFLICT` | Upsert (insert o update)       | `INSERT ... ON CONFLICT DO UPDATE SET ...;`      |

### Errores comunes

| Error                               | Solucion                                              |
|--------------------------------------|-------------------------------------------------------|
| `UPDATE` sin `WHERE`                | Siempre agrega `WHERE` o verifica primero con SELECT  |
| `DELETE` sin `WHERE`                | Siempre agrega `WHERE` o verifica primero con SELECT  |
| `INSERT` sin columnas               | Especifica las columnas: `INSERT INTO t (c1, c2)`    |
| `INSERT` con tipos incorrectos      | Asegurate que los valores coincidan con el tipo de dato|
| `ON CONFLICT` sin constraint        | La columna en `ON CONFLICT` debe tener UNIQUE o PK    |

---

## Fuentes

- [PostgreSQL 18 Documentation - Chapter 2: SQL Language](https://www.postgresql.org/docs/18/sql.html)
- [PostgreSQL Documentation - INSERT](https://www.postgresql.org/docs/18/sql-insert.html)
- [PostgreSQL Documentation - UPDATE](https://www.postgresql.org/docs/18/sql-update.html)
- [PostgreSQL Documentation - DELETE](https://www.postgresql.org/docs/18/sql-delete.html)
- [PostgreSQL Documentation - SELECT](https://www.postgresql.org/docs/18/sql-select.html)

---

> **Siguiente archivo:** [05 - WHERE, ORDER BY, LIMIT, filtros](05-where-orden-filtros.md)
