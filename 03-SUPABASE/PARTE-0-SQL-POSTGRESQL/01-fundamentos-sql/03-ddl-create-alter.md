# 03 - DDL: CREATE, ALTER, DROP

> DDL (Data Definition Language) te permite crear, modificar y eliminar la estructura de tu base de datos. Es el primer paso antes de poder almacenar datos.

```
┌──────────────────────────────────────────────────────────────┐
│                    RESUMEN RAPIDO                             │
│                                                              │
│  CREATE TABLE → Crear una nueva tabla                        │
│  ALTER TABLE  → Modificar tabla existente                    │
│  DROP TABLE   → Eliminar una tabla                           │
│                                                              │
│  Siempre: IF EXISTS / IF NOT EXISTS para evitar errores      │
│  Siempre: snake_case para nombres                           │
│  Siempre: NOT NULL en columnas importantes                   │
└──────────────────────────────────────────────────────────────┘
```

## Indice

1. [CREATE TABLE](#create-table)
2. [Column constraints](#column-constraints)
3. [Ejemplo completo](#ejemplo-completo-de-create-table)
4. [ALTER TABLE](#alter-table)
5. [DROP TABLE](#drop-table)
6. [CREATE y DROP DATABASE](#create-y-drop-database)
7. [Buenas practicas](#buenas-practicas)

---

## CREATE TABLE

**Sintaxis basica:**

```sql
CREATE TABLE nombre_tabla (
    columna1 TIPO DE DATO CONSTRAINTS,
    columna2 TIPO DE DATO CONSTRAINTS,
    ...
);
```

**Sintaxis completa con todas las opciones:**

```sql
CREATE TABLE IF NOT EXISTS nombre_tabla (
    columna1 TIPO DE DATO NOT NULL DEFAULT valor,
    columna2 TIPO DE DATO UNIQUE,
    columna3 TIPO DE DATO PRIMARY KEY,
    columna4 TIPO DE DATO REFERENCES otra_tabla(otra_columna),
    columna5 TIPO DE DATO CHECK (condicion),
    PRIMARY KEY (columna1, columna2),           -- Primary key compuesta
    CONSTRAINT nombre_constraint UNIQUE (a, b), -- Unique compuesta
    CONSTRAINT nombre_check CHECK (condicion)   -- Check a nivel tabla
) WITH (OIDS = false);                         -- Opcional: sin OID
```

**Ejemplo basico:**

```sql
-- Crear tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ver la tabla creada
\d usuarios  -- En psql
```

**Crear tabla con IF NOT EXISTS:**

```sql
-- No falla si la tabla ya existe
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC(10, 2) NOT NULL
);
```

---

## Column constraints

Las constraints (restricciones) garantizan la **integridad** de los datos.

### NOT NULL

No permite valores nulos en la columna.

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,    -- Siempre debe tener valor
    email TEXT NOT NULL      -- Siempre debe tener valor
);

-- Esto FALLA:
INSERT INTO usuarios (nombre, email) VALUES (NULL, 'test@email.com');
-- Error: null value in column "nombre" violates not-null constraint
```

### DEFAULT

Asigna un valor por defecto cuando no se especifica uno.

```sql
CREATE TABLE tareas (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    completada BOOLEAN DEFAULT false,      -- Por defecto: false
    prioridad INTEGER DEFAULT 1,           -- Por defecto: 1
    created_at TIMESTAMPTZ DEFAULT NOW(),  -- Por defecto: fecha actual
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- No especificar completada usa el default
INSERT INTO tareas (titulo) VALUES ('Mi tarea');
-- completada = false, created_at = ahora
```

### PRIMARY KEY

Identificador unico de cada fila. Implica `NOT NULL` y `UNIQUE`.

```sql
-- Primary key simple
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL
);

-- Primary key compuesta (dos columnas forman la PK)
CREATE TABLE usuario_roles (
    usuario_id UUID REFERENCES usuarios(id),
    rol_id INTEGER REFERENCES roles(id),
    PRIMARY KEY (usuario_id, rol_id)  -- Combinacion unica
);
```

### UNIQUE

Asegura que no haya valores duplicados en la columna.

```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,     -- No puede haber dos emails iguales
    username TEXT UNIQUE NOT NULL   -- No puede haber dos usernames iguales
);

-- Esto FALLA si ya existe el email:
INSERT INTO usuarios (email, username) VALUES ('ana@email.com', 'ana');
INSERT INTO usuarios (email, username) VALUES ('ana@email.com', 'otra');
-- Error: duplicate key value violates unique constraint
```

### CHECK

Valida que el valor cumpla una condicion.

```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0),       -- Precio debe ser positivo
    stock INTEGER NOT NULL CHECK (stock >= 0),                -- Stock no puede ser negativo
    descuento NUMERIC(5, 2) CHECK (descuento BETWEEN 0 AND 100), -- Entre 0 y 100
    CONSTRAINT nombre_no_vacio CHECK (LENGTH(nombre) > 0)     -- Nombre con al menos 1 caracter
);

-- Esto FALLA:
INSERT INTO productos (nombre, precio, stock) VALUES ('Laptop', -100, 5);
-- Error: new row violates check constraint for table "productos"
```

### REFERENCES (Foreign Key)

Establece una relacion con otra tabla.

```sql
-- Tabla padre
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

-- Tabla hijo con foreign key
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Con acciones en cascada
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
        ON DELETE CASCADE          -- Si se borra la categoria, se borran los productos
        ON UPDATE CASCADE          -- Si se actualiza el ID, se actualiza en productos
);
```

**Acciones de foreign key:**

| Accion           | Que hace                                                         |
|------------------|------------------------------------------------------------------|
| `CASCADE`        | Propaga la eliminacion/actualizacion a los registros hijos       |
| `SET NULL`       | Pone el FK en NULL cuando se elimina el registro padre           |
| `SET DEFAULT`    | Pone el FK en el valor default cuando se elimina el padre        |
| `RESTRICT`       | **Impide** eliminar el padre si tiene hijos (comportamiento default) |
| `NO ACTION`      | Similar a RESTRICT pero se verifica al final de la transaccion   |

---

## Ejemplo completo de CREATE TABLE

```sql
-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- TABLA: categorias
-- ============================================
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    activa BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================
-- TABLA: usuarios
-- ============================================
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL CHECK (LENGTH(nombre) >= 2),
    email TEXT NOT NULL UNIQUE,
    telefono TEXT,
    rol TEXT NOT NULL DEFAULT 'user' CHECK (rol IN ('admin', 'user', 'moderator')),
    activo BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================
-- TABLA: productos
-- ============================================
CREATE TABLE IF NOT EXISTS productos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL CHECK (LENGTH(nombre) > 0),
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    categoria_id INTEGER NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_producto_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categorias(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ============================================
-- TABLA: pedidos
-- ============================================
CREATE TABLE IF NOT EXISTS pedidos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario_id UUID NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'procesando', 'enviado', 'entregado', 'cancelado')),
    total NUMERIC(12, 2) NOT NULL CHECK (total >= 0),
    direccion_envio TEXT NOT NULL,
    notas TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_pedido_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE RESTRICT
);

-- ============================================
-- TABLA: detalle_pedido (relacion many-to-many)
-- ============================================
CREATE TABLE IF NOT EXISTS detalle_pedido (
    pedido_id UUID NOT NULL,
    producto_id UUID NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10, 2) NOT NULL CHECK (precio_unitario > 0),
    subtotal NUMERIC(12, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    PRIMARY KEY (pedido_id, producto_id),
    CONSTRAINT fk_detalle_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedidos(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_detalle_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(id)
        ON DELETE RESTRICT
);
```

---

## ALTER TABLE

Modifica una tabla existente despues de haberla creado.

### Agregar columna

```sql
-- Agregar una columna
ALTER TABLE usuarios ADD COLUMN telefono TEXT;

-- Agregar con valor default
ALTER TABLE usuarios ADD COLUMN bio TEXT DEFAULT 'Sin descripcion';

-- Agregar con constraint
ALTER TABLE usuarios ADD COLUMN edad SMALLINT CHECK (edad >= 0 AND edad <= 150);
```

### Eliminar columna

```sql
-- Eliminar una columna
ALTER TABLE usuarios DROP COLUMN bio;

-- Eliminar si existe (sin error)
ALTER TABLE usuarios DROP COLUMN IF EXISTS bio;
```

### Renombrar columna

```sql
-- Renombrar una columna
ALTER TABLE usuarios RENAME COLUMN telefono TO numero_telefono;
```

### Cambiar tipo de dato

```sql
-- Cambiar el tipo de dato de una columna
ALTER TABLE productos
    ALTER COLUMN precio TYPE NUMERIC(12, 2);

-- Cambiar tipo con USING (cuando hay conversion de datos)
ALTER TABLE productos
    ALTER COLUMN stock TYPE BIGINT USING stock::BIGINT;
```

### Modificar default

```sql
-- Agregar un default
ALTER TABLE usuarios
    ALTER COLUMN activo SET DEFAULT true;

-- Eliminar un default
ALTER TABLE usuarios
    ALTER COLUMN activo DROP DEFAULT;
```

### Modificar NOT NULL

```sql
-- Hacer una columna NOT NULL
ALTER TABLE usuarios
    ALTER COLUMN nombre SET NOT NULL;

-- Permitir NULL
ALTER TABLE usuarios
    ALTER COLUMN telefono DROP NOT NULL;
```

### Agregar constraint

```sql
-- Agregar UNIQUE
ALTER TABLE usuarios
    ADD CONSTRAINT uk_usuario_email UNIQUE (email);

-- Agregar CHECK
ALTER TABLE productos
    ADD CONSTRAINT ck_precio_positivo CHECK (precio > 0);

-- Agregar FOREIGN KEY
ALTER TABLE productos
    ADD CONSTRAINT fk_producto_categoria
    FOREIGN KEY (categoria_id) REFERENCES categorias(id);

-- Eliminar una constraint
ALTER TABLE usuarios
    DROP CONSTRAINT uk_usuario_email;

-- Eliminar si existe
ALTER TABLE usuarios
    DROP CONSTRAINT IF EXISTS uk_usuario_email;
```

### Renombrar tabla

```sql
-- Renombrar una tabla
ALTER TABLE usuarios RENAME TO clientes;

-- Renombrar de vuelta
ALTER TABLE clientes RENAME TO usuarios;
```

### Resumen de ALTER TABLE

| Operacion               | Sintaxis                                           |
|-------------------------|----------------------------------------------------|
| Agregar columna         | `ALTER TABLE t ADD COLUMN c TIPO;`                 |
| Eliminar columna        | `ALTER TABLE t DROP COLUMN c;`                     |
| Renombrar columna       | `ALTER TABLE t RENAME COLUMN c1 TO c2;`            |
| Cambiar tipo            | `ALTER TABLE t ALTER COLUMN c TYPE nuevo_tipo;`     |
| Agregar default         | `ALTER TABLE t ALTER COLUMN c SET DEFAULT valor;`   |
| Eliminar default        | `ALTER TABLE t ALTER COLUMN c DROP DEFAULT;`        |
| Hacer NOT NULL          | `ALTER TABLE t ALTER COLUMN c SET NOT NULL;`        |
| Permitir NULL           | `ALTER TABLE t ALTER COLUMN c DROP NOT NULL;`       |
| Agregar constraint      | `ALTER TABLE t ADD CONSTRAINT nombre CONSTRAINT;`  |
| Eliminar constraint     | `ALTER TABLE t DROP CONSTRAINT nombre;`             |
| Renombrar tabla         | `ALTER TABLE t1 RENAME TO t2;`                     |

---

## DROP TABLE

Elimina una tabla y **todos sus datos permanentemente**.

```sql
-- Eliminar una tabla
DROP TABLE usuarios;

-- Eliminar sin error si no existe
DROP TABLE IF EXISTS usuarios;

-- Eliminar multiple
DROP TABLE IF EXISTS usuarios, productos, pedidos;

-- Eliminar en cascada (elimina tambien objetos dependientes)
DROP TABLE IF EXISTS productos CASCADE;
```

> **Advertencia:** `DROP TABLE` es **irreversible**. En Supabase, primero crea un backup antes de eliminar tablas en produccion.

**Tabla de comportamiento:**

| Comando                        | Que hace                                           |
|--------------------------------|----------------------------------------------------|
| `DROP TABLE t;`               | Elimina la tabla. Error si no existe.              |
| `DROP TABLE IF EXISTS t;`     | Elimina la tabla. Silencioso si no existe.         |
| `DROP TABLE t CASCADE;`       | Elimina tabla + objetos dependientes (views, etc.) |
| `DROP TABLE t RESTRICT;`      | Impide eliminar si hay dependencias (default).     |

---

## CREATE y DROP DATABASE

```sql
-- Crear una base de datos (solo disponible en terminal psql, no en SQL Editor)
-- CREATE DATABASE mi_base_datos;

-- En Supabase, las bases de datos se crean desde el Dashboard
-- o via: supabase db create

-- Eliminar una base de datos (solo en terminal)
-- DROP DATABASE mi_base_datos;
-- DROP DATABASE IF EXISTS mi_base_datos;
```

> **Nota:** En Supabase no puedes crear/eliminar databases desde el SQL Editor. Esto se hace desde el Dashboard o la CLI de Supabase.

---

## Buenas practicas

### Convenciones de nomenclatura

```
┌──────────────────────────────────────────────────────────────┐
│                  CONVENCIONES DE NOMBRE                       │
│                                                              │
│  ✅ snake_case para todo                                     │
│     tabla: usuario_rol                                       │
│     columna: fecha_creacion                                  │
│     constraint: fk_producto_categoria                        │
│                                                              │
│  ❌ Evitar                                                   │
│     camelCase: usuarioRol                                    │
│     PascalCase: UsuarioRol                                   │
│     espacios: "Usuario Rol"                                  │
│     palabras reservadas: select, table, order                │
└──────────────────────────────────────────────────────────────┘
```

| Elemento          | Convencion              | Ejemplo                         |
|-------------------|-------------------------|----------------------------------|
| Tabla             | `snake_case` plural     | `usuarios`, `productos_pedido`  |
| Columna           | `snake_case` singular   | `nombre`, `fecha_creacion`      |
| Primary Key       | `id`                    | `id` (siempre)                  |
| Foreign Key       | `tabla_ref_id`          | `usuario_id`, `categoria_id`    |
| Unique Constraint | `uk_tabla_columna`      | `uk_usuario_email`              |
| Check Constraint  | `ck_tabla_descripcion`  | `ck_producto_precio_positivo`   |
| Foreign Key Constraint | `fk_tabla_ref`    | `fk_producto_categoria`         |
| Index             | `idx_tabla_columna`     | `idx_usuario_email`             |

### Reglas importantes

```sql
-- 1. Siempre usa IF NOT EXISTS / IF EXISTS
CREATE TABLE IF NOT EXISTS usuarios (...);
DROP TABLE IF EXISTS usuarios;

-- 2. Siempre agrega NOT NULL a columnas obligatorias
CREATE TABLE usuarios (
    nombre TEXT NOT NULL,  -- ✅
    email TEXT             -- ❌ Falta NOT NULL
);

-- 3. Siempre agrega DEFAULT cuando tenga sentido
created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()  -- ✅
created_at TIMESTAMPTZ NOT NULL               -- ❌ Sin default

-- 4. Usa UUID como primary key en Supabase
id UUID PRIMARY KEY DEFAULT gen_random_uuid()  -- ✅
id SERIAL PRIMARY KEY                          -- ⚠️ Funciona pero no recomendado

-- 5. Usa NUMERIC para dinero
precio NUMERIC(10, 2) NOT NULL                -- ✅
precio FLOAT                                  -- ❌ Errores de redondeo

-- 6. Usa TIMESTAMPTZ para fechas
created_at TIMESTAMPTZ DEFAULT NOW()          -- ✅
created_at TIMESTAMP                          -- ❌ Sin zona horaria
```

---

## Fuentes

- [PostgreSQL 18 Documentation - Chapter 5: Data Definition](https://www.postgresql.org/docs/18/ddl.html)
- [PostgreSQL Documentation - CREATE TABLE](https://www.postgresql.org/docs/18/sql-createtable.html)
- [PostgreSQL Documentation - ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html)
- [PostgreSQL Documentation - Constraints](https://www.postgresql.org/docs/18/ddl-constraints.html)

---

> **Siguiente archivo:** [04 - DML: SELECT, INSERT, UPDATE, DELETE](04-dml-select-insert-update-delete.md)
