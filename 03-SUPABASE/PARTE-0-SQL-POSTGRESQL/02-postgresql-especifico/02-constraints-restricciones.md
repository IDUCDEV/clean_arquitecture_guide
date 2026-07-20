# 02 - Constraints / Restricciones

> Las restricciones garantizan la integridad de tus datos a nivel de base de datos. Son la primera linea de defensa contra datos invalidos.

---

## Que son las restricciones

Una **constraint** es una regla que PostgreSQL aplica automaticamente a los datos de una tabla. Si los datos violan la regla, la operacion (INSERT, UPDATE) falla.

```
┌─────────────────────────────────────────────────┐
│  INSERT INTO users (email) VALUES (NULL)        │
│                                                 │
│  PostgreSQL verifica:                           │
│  ┌─────────────────────────────────────────┐    │
│  │ email NOT NULL constraint               │    │
│  │ ¿Es NULL? -> SI -> ERROR                │    │
│  └─────────────────────────────────────────┘    │
│                                                 │
│  Resultado: ERROR violates not-null constraint  │
└─────────────────────────────────────────────────┘
```

**Fuente:** PostgreSQL 18 Documentation, Cap. 5.5 Constraints

---

## NOT NULL

Asegura que una columna nunca contenga NULL:

```sql
-- Forma inline (column-level)
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Forma de tabla (table-level)
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name TEXT,
    email TEXT,
    CONSTRAINT users_name_not_null CHECK (name IS NOT NULL),
    CONSTRAINT users_email_not_null CHECK (email IS NOT NULL)
);
```

**En tablas existentes:**

```sql
-- Agregar NOT NULL a columna existente
ALTER TABLE users ALTER COLUMN name SET NOT NULL;

-- Quitar NOT NULL
ALTER TABLE users ALTER COLUMN name DROP NOT NULL;
```

---

## UNIQUE

Asegura que todos los valores en una columna (o combinacion de columnas) sean unicos:

```sql
-- Unique en una sola columna
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE
);

-- Unique en multiples columnas (table-level)
CREATE TABLE reservations (
    id UUID PRIMARY KEY,
    room_id UUID NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    CONSTRAINT unique_room_dates UNIQUE (room_id, check_in, check_out)
);
```

**Que crea PostgreSQL internamente:**
- Un **indice unico automaticamente** para cada constraint UNIQUE
- Permite NULLs (a diferencia de PRIMARY KEY)

---

## PRIMARY KEY

Combina **UNIQUE + NOT NULL** y crea un indice B-tree automaticamente:

```sql
-- Unica forma: table-level (no se puede inline)
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- Primary key compuesta
CREATE TABLE order_items (
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

**Reglas de PRIMARY KEY:**
| Regla | Descripcion |
|-------|-------------|
| Unica por tabla | Solo puede haber UNA primary key |
| Unico | No permite valores duplicados |
| NOT NULL | No permite NULLs |
| Indice automatico | Crea un B-tree index |

**Alternativa: GENERATED ALWAYS AS IDENTITY**

```sql
-- Auto-incrementing integer (recomendado sobre SERIAL)
CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

-- El id se genera automaticamente: 1, 2, 3...
INSERT INTO users (name) VALUES ('Ana');  -- id = 1
INSERT INTO users (name) VALUES ('Luis'); -- id = 2
```

---

## FOREIGN KEY

Enlaza una columna con la primary key de otra tabla:

```sql
-- Sintaxis completa
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

### ON DELETE: que pasa cuando se elimina el registro padre

| Opcion | Comportamiento | Ejemplo |
|--------|----------------|---------|
| `CASCADE` | Elimina los registros hijos tambien | Eliminar usuario elimina sus ordenes |
| `SET NULL` | Pone NULL en la columna FK | Eliminar usuario, user_id = NULL |
| `SET DEFAULT` | Pone el valor default | Eliminar usuario, user_id = DEFAULT |
| `RESTRICT` | Bloquea la eliminacion | No deja eliminar usuario si tiene ordenes |
| `NO ACTION` | Igual a RESTRICT pero evalua al final de la transaccion | Como RESTRICT pero posterga la verificacion |

```sql
-- Ejemplo con ON DELETE CASCADE
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE
);

-- Si elimino un usuario, todas sus ordenes se eliminan automaticamente

-- Ejemplo con ON DELETE SET NULL
CREATE TABLE comments (
    id UUID PRIMARY KEY,
    author_id UUID REFERENCES users(id) ON DELETE SET NULL
);

-- Si elimino el usuario, el comment queda pero author_id = NULL
```

### ON UPDATE: que pasa cuando cambia la PK del padre

```sql
-- Si el id del usuario cambia, actualizar en la tabla orders
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON UPDATE CASCADE
);
```

---

## CHECK

Valida que los datos cumplan una condicion expresada como booleana:

```sql
-- Ejemplos de CHECK constraints
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    email TEXT,
    age INTEGER,
    start_date DATE,
    end_date DATE,
    status TEXT,

    -- Precio debe ser positivo
    CONSTRAINT chk_price_positive CHECK (price > 0),

    -- Email debe contener @
    CONSTRAINT chk_email_format CHECK (email ILIKE '%@%.%'),

    -- Edad entre 0 y 150
    CONSTRAINT chk_age_range CHECK (age >= 0 AND age <= 150),

    -- La fecha fin debe ser posterior a la fecha inicio
    CONSTRAINT chk_dates_valid CHECK (end_date > start_date),

    -- Status debe ser uno de los valores permitidos
    CONSTRAINT chk_status_valid CHECK (status IN ('active', 'inactive', 'pending'))
);
```

**CHECK con subqueries (PostgreSQL 17+):**

```sql
-- CHECK con referencia a otra tabla (solo PostgreSQL 17+)
CREATE TABLE enrollments (
    id UUID PRIMARY KEY,
    course_id UUID NOT NULL,
    max_students INTEGER,

    CONSTRAINT chk_enrollment_limit
        CHECK (max_students <= (SELECT max_capacity FROM courses WHERE id = course_id))
);
```

---

## EXCLUDE

Excluye combinaciones de valores que se superponen. Ideal para reservas de tiempo o espacios:

```sql
-- Instalar la extension btree_gist (necesaria para EXCLUDE)
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- Evitar reservas superpuestas en una habitacion
CREATE TABLE room_reservations (
    id UUID PRIMARY KEY,
    room_id INTEGER NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,

    -- No puede haber dos reservas superpuestas en la misma habitacion
    CONSTRAINT excl_room_dates
        EXCLUDE USING gist (
            room_id WITH =,
            daterange(check_in, check_out, '[]') WITH &&
        )
);

-- Intentar insertar una reserva superpuesta FALLA:
INSERT INTO room_reservations (room_id, check_in, check_out)
VALUES (1, '2026-07-10', '2026-07-15');
-- OK

INSERT INTO room_reservations (room_id, check_in, check_out)
VALUES (1, '2026-07-12', '2026-07-18');
-- ERROR: violates exclusion constraint
```

**Operadores de EXCLUDE:**

| Operador | Tipo | Descripcion |
|----------|------|-------------|
| `=` | Igual | Mismo valor exacto |
| `&&` | Solapa | Rangos que se superponen |
| `<>` | Diferente | Valores distintos |

---

## DEFAULT

Asigna un valor automaticamente cuando no se especifica:

```sql
CREATE TABLE posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    content TEXT DEFAULT '',
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    view_count INTEGER DEFAULT 0,

    -- Default con funcion
    search_vector tsvector DEFAULT to_tsvector('spanish', '')
);
```

**Valores DEFAULT permitidos:**
- Literales: `'valor'`, `42`, `TRUE`
- Funciones: `NOW()`, `gen_random_uuid()`
- Expressiones: `CURRENT_TIMESTAMP`
- No se permiten subqueries (excepto en GENERATED ALWAYS AS)

---

## GENERATED ALWAYS AS IDENTITY

Alternativa moderna a SERIAL para columnas auto-incrementables:

```sql
-- GENERATED ALWAYS AS IDENTITY (recomendado)
CREATE TABLE users (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

-- Con valores iniciales y paso
CREATE TABLE orders (
    id INTEGER GENERATED ALWAYS AS IDENTITY (START WITH 1000 INCREMENT BY 1) PRIMARY KEY,
    total DECIMAL(10,2) NOT NULL
);

-- Opciones disponibles
-- START WITH: valor inicial
-- INCREMENT BY: paso entre valores
-- MINVALUE: valor minimo
-- MAXVALUE: valor maximo
-- NO MINVALUE / NO MAXVALUE: sin limite
-- CACHE: cuantos valores pre-generar
-- CYCLE / NO CYCLE: que pasa al llegar al maximo
```

**GENERATED ALWAYS AS IDENTITY vs SERIAL:**

| Caracteristica | GENERATED ALWAYS AS IDENTITY | SERIAL |
|----------------|:---------------------------:|:------:|
| Estandar SQL | Si | No (PostgreSQL specific) |
| Valor editable | Solo con OVERRIDING SYSTEM VALUE | Siempre editable |
| Claro en metadata | Si | No |
| Reversible | ALTER COLUMN ... DROP IDENTITY | ALTER COLUMN ... DROP DEFAULT |
| Recomendado | Si | No (legacy) |

---

## Constraint Naming

Siempre nombra tus constraints para facilitar el debugging:

```sql
-- Convencion: <tabla>_<columna>_<tipo>
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT NOT NULL,

    CONSTRAINT users_email_unique UNIQUE (email),
    CONSTRAINT users_email_not_null CHECK (email IS NOT NULL),
    CONSTRAINT users_email_format CHECK (email ILIKE '%@%.%')
);

-- PostgreSQL genera nombres automaticos si no los especificas:
-- users_email_key (para UNIQUE)
-- users_email_check (para CHECK)

-- Esto es MAL para debugging porque no sabes que es que
```

**Nombres de constraints:**

| Tipo | Convencion | Ejemplo |
|------|-----------|---------|
| PRIMARY KEY | `<tabla>_pkey` | `users_pkey` |
| UNIQUE | `<tabla>_<columna>_unique` | `users_email_unique` |
| CHECK | `<tabla>_<descripcion>_check` | `users_age_check` |
| FOREIGN KEY | `<tabla>_<columna>_fk` | `orders_user_id_fk` |
| NOT NULL | `<tabla>_<columna>_not_null` | `users_name_not_null` |

---

## Deferrable Constraints

Las constraints pueden evaluarse al final de la transaccion en lugar de inmediatamente:

```sql
-- Constraint deferrable
CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    balance DECIMAL(10,2) NOT NULL CHECK (balance >= 0)
);

-- Esto FALLA inmediatamente:
BEGIN;
UPDATE accounts SET balance = -100 WHERE id = '...'; -- ERROR
ROLLBACK;

-- Con DEFERRABLE, se evalua al COMMIT:
CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    balance DECIMAL(10,2 NOT NULL,
    CONSTRAINT chk_balance_positive CHECK (balance >= 0) DEFERRABLE INITIALLY DEFERRED
);

-- Ahora esto funciona temporalmente:
BEGIN;
UPDATE accounts SET balance = -100 WHERE id = '...'; -- OK
UPDATE accounts SET balance = 200 WHERE id = '...';  -- OK
COMMIT; -- Aqui se verifica la constraint
```

**Sintaxis:**

```sql
-- DEFERRABLE INITIALLY DEFERRED: evaluada al COMMIT
-- DEFERRABLE INITIALLY IMMEDIATE: evaluada inmediatamente (default)
-- NOT DEFERRABLE: nunca se posterga (default)

-- Cambiar el comportamiento de una constraint existente
ALTER TABLE accounts
    ALTER CONSTRAINT chk_balance_positive
    DEFERRABLE INITIALLY DEFERRED;
```

---

## Ejemplo completo: tabla users con todas las constraints

```sql
-- Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla con todas las constraint types
CREATE TABLE users (
    -- PRIMARY KEY con GENERATED ALWAYS AS IDENTITY
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    -- UNIQUE + NOT NULL + CHECK
    email TEXT NOT NULL,
    username TEXT NOT NULL,

    -- CHECK con multiples condiciones
    age INTEGER CHECK (age >= 13 AND age <= 150),

    -- DEFAULT con funcion
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- STATUS con CHECK para valores permitidos
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'banned')),

    -- Constraints nombradas
    CONSTRAINT users_email_unique UNIQUE (email),
    CONSTRAINT users_username_unique UNIQUE (username),
    CONSTRAINT users_email_format CHECK (email ILIKE '%@%.%'),
    CONSTRAINT users_username_min_length CHECK (length(username) >= 3)
);

-- Tabla con FOREIGN KEY
CREATE TABLE posts (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    published_at TIMESTAMPTZ,

    -- FOREIGN KEY con ON DELETE y ON UPDATE
    CONSTRAINT posts_author_fk
        FOREIGN KEY (author_id)
        REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    -- CHECK para fechas
    CONSTRAINT posts_published_after_creation CHECK (
        published_at IS NULL OR published_at >= created_at
    )
);

-- Ver constraints de una tabla
SELECT
    conname AS constraint_name,
    contype AS constraint_type,
    pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'users'::regclass;
```

**Referencia de tipos de constraint:**

| `contype` | Tipo |
|-----------|------|
| `p` | PRIMARY KEY |
| `u` | UNIQUE |
| `f` | FOREIGN KEY |
| `c` | CHECK |
| `x` | EXCLUDE |
| `t` | TRIGGER |

---

## Resumen de restricciones

```
┌────────────────────────────────────────────────────┐
│              RESTICCIONES EN POSTGRESQL            │
├────────────────────────────────────────────────────┤
│  NOT NULL        -> Columna no puede ser NULL      │
│  UNIQUE          -> Valores unicos                 │
│  PRIMARY KEY     -> UNIQUE + NOT NULL + indice     │
│  FOREIGN KEY     -> Referencia a otra tabla        │
│  CHECK           -> Condicion booleana custom      │
│  EXCLUDE         -> Excluir superposiciones        │
│  DEFAULT         -> Valor automatico               │
│  IDENTITY        -> Auto-increment moderno         │
│  DEFERRABLE      -> Evaluar al COMMIT              │
└────────────────────────────────────────────────────┘
```

---

**Siguiente:** [03 - Indexes y Rendimiento](03-indexes-rendimiento.md)
