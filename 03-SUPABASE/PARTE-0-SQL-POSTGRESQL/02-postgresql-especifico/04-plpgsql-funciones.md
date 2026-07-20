# 04 - PL/pgSQL y Funciones

> PL/pgSQL es el lenguaje procedural de PostgreSQL. Permite crear funciones que ejecutan logica compleja dentro de la base de datos.

---

## Que es PL/pgSQL

**PL/pgSQL** (Procedural Language/PostgreSQL) es un lenguaje de programacion que se ejecuta dentro de PostgreSQL. Combina SQL con estructuras de control como IF, LOOP y manejo de errores.

```
┌─────────────────────────────────────────────────┐
│  FLUTTER (Dart)                                 │
│  ┌─────────────────────────────────────────┐    │
│  │  Widget  ->  State  ->  Service  ->  DB │    │
│  └─────────────────────────────────────────┘    │
│                    |                            │
│                    v                            │
│  ┌─────────────────────────────────────────┐    │
│  │  PostgreSQL + PL/pgSQL                  │    │
│  │  Functions, Triggers, Logic             │    │
│  └─────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

**Fuente:** PostgreSQL 18 Documentation, Cap. 41 PL/pgSQL

---

## CREATE FUNCTION: sintaxis basica

```sql
-- Funcion mas simple
CREATE FUNCTION greet() RETURNS TEXT AS $$
BEGIN
    RETURN 'Hola mundo';
END;
$$ LANGUAGE plpgsql;

-- Ejecutar
SELECT greet();  -- 'Hola mundo'
```

**Componentes de una funcion:**

```sql
CREATE FUNCTION nombre(
    param1 TIPO,           -- Parametros de entrada
    param2 TIPO DEFAULT valor  -- Con valor por defecto
) RETURNS TIPO_RETORNO    -- Tipo que retorna
AS $$                     -- Inicio del cuerpo
DECLARE                   -- Declaracion de variables (opcional)
    variable TIPO;
BEGIN                     -- Cuerpo de la funcion
    -- Logica aqui
    RETURN resultado;
END;                      -- Fin del cuerpo
$$ LANGUAGE plpgsql;      -- Lenguaje
```

---

## Parametros de funcion

### IN, OUT, INOUT

```sql
-- IN: solo entrada (default)
CREATE FUNCTION get_user_name(user_id UUID) RETURNS TEXT AS $$
DECLARE
    result TEXT;
BEGIN
    SELECT name INTO result FROM users WHERE id = user_id;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- OUT: solo salida
CREATE FUNCTION get_user_info(
    user_id UUID,
    OUT user_name TEXT,
    OUT user_email TEXT
) AS $$
BEGIN
    SELECT name, email INTO user_name, user_email
    FROM users WHERE id = user_id;
END;
$$ LANGUAGE plpgsql;

-- Ejecutar con OUT
SELECT * FROM get_user_info('uuid-aqui');

-- INOUT: entrada y salida
CREATE FUNCTION double_value(INOUT val INTEGER) AS $$
BEGIN
    val := val * 2;
END;
$$ LANGUAGE plpgsql;

-- Ejecutar
SELECT double_value(5);  -- 10
```

**Tabla de modos de parametros:**

| Modo | Descripcion | Ejemplo |
|------|-------------|---------|
| `IN` | Solo entrada (default) | `user_id UUID` |
| `OUT` | Solo salida | `OUT result TEXT` |
| `INOUT` | Entrada y salida | `INOUT value INTEGER` |

### Valores por defecto

```sql
CREATE FUNCTION search_users(
    search_term TEXT DEFAULT '%',
    max_results INTEGER DEFAULT 10,
    status_filter TEXT DEFAULT 'active'
) RETURNS TABLE(name TEXT, email TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT users.name, users.email
    FROM users
    WHERE users.name ILIKE search_term
      AND users.status = status_filter
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- Ejecutar con valores por defecto
SELECT * FROM search_users();

-- Ejecutar con parametros personalizados
SELECT * FROM search_users('ana%', 5, 'active');
```

---

## Declaracion de variables: DECLARE

```sql
CREATE FUNCTION example_function() RETURNS TEXT AS $$
DECLARE
    -- Variable simple
    total INTEGER;

    -- Variable con tipo explicito
    user_name TEXT;

    -- Variable con valor por defecto
    counter INTEGER := 0;

    -- Variable con tipo de columna (%TYPE)
    user_email users.email%TYPE;

    -- Variable con tipo de fila (%ROWTYPE)
    user_record users%TYPE;

    -- Variable RECORD (resultado de query)
    row_result RECORD;

    -- Constante
    MAX_ITEMS CONSTANT INTEGER := 100;
BEGIN
    -- Asignar valor
    total := 0;

    -- Asignar con SELECT INTO
    SELECT name INTO user_name FROM users LIMIT 1;

    -- Asignar con SELECT INTO RECORD
    SELECT * INTO row_result FROM users LIMIT 1;

    RETURN user_name;
END;
$$ LANGUAGE plpgsql;
```

**Tipos de variables:**

| Tipo | Descripcion | Ejemplo |
|------|-------------|---------|
| `TIPO` | Tipo simple | `INTEGER`, `TEXT`, `UUID` |
| `tabla.columna%TYPE` | Tipo de una columna | `users.email%TYPE` |
| `tabla%TYPE` | Tipo de toda la fila | `users%TYPE` |
| `RECORD` | Fila dinamica | `SELECT * INTO rec FROM...` |
| `CONSTANTE` | Valor inmutable | `MAX CONSTANT INTEGER := 100` |

---

## Control estructurado

### IF / ELSIF / ELSE / END IF

```sql
CREATE FUNCTION get_user_role(user_id UUID) RETURNS TEXT AS $$
DECLARE
    user_status TEXT;
    user_age INTEGER;
BEGIN
    SELECT status, age INTO user_status, user_age
    FROM users WHERE id = user_id;

    IF user_status = 'admin' THEN
        RETURN 'Administrador';
    ELSIF user_status = 'moderator' THEN
        RETURN 'Moderador';
    ELSIF user_status = 'active' AND user_age >= 18 THEN
        RETURN 'Usuario adulto';
    ELSIF user_status = 'active' THEN
        RETURN 'Usuario menor';
    ELSE
        RETURN 'Desconocido';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### CASE WHEN

```sql
CREATE FUNCTION get_discount(membership TEXT) RETURNS DECIMAL AS $$
BEGIN
    RETURN CASE membership
        WHEN 'gold' THEN 0.20
        WHEN 'silver' THEN 0.10
        WHEN 'bronze' THEN 0.05
        ELSE 0.00
    END;
END;
$$ LANGUAGE plpgsql;

-- CASE con condicion compleja
CREATE FUNCTION get_shipping_cost(weight DECIMAL) RETURNS DECIMAL AS $$
BEGIN
    RETURN CASE
        WHEN weight <= 1 THEN 5.00
        WHEN weight <= 5 THEN 10.00
        WHEN weight <= 20 THEN 20.00
        ELSE 50.00
    END;
END;
$$ LANGUAGE plpgsql;
```

---

## Loops

### LOOP basico con EXIT WHEN

```sql
CREATE FUNCTION count_up_to(n INTEGER) RETURNS TEXT AS $$
DECLARE
    i INTEGER := 1;
    result TEXT := '';
BEGIN
    LOOP
        result := result || i || ' ';
        EXIT WHEN i >= n;
        i := i + 1;
    END LOOP;
    RETURN TRIM(result);
END;
$$ LANGUAGE plpgsql;

SELECT count_up_to(5);  -- '1 2 3 4 5'
```

### WHILE LOOP

```sql
CREATE FUNCTION fibonacci(n INTEGER) RETURNS INTEGER AS $$
DECLARE
    a INTEGER := 0;
    b INTEGER := 1;
    temp INTEGER;
    i INTEGER := 1;
BEGIN
    WHILE i <= n LOOP
        temp := b;
        b := a + b;
        a := temp;
        i := i + 1;
    END LOOP;
    RETURN a;
END;
$$ LANGUAGE plpgsql;

SELECT fibonacci(10);  -- 55
```

### FOR IN LOOP

```sql
-- FOR con rango numerico
CREATE FUNCTION sum_numbers(max_val INTEGER) RETURNS INTEGER AS $$
DECLARE
    total INTEGER := 0;
BEGIN
    FOR i IN 1..max_val LOOP
        total := total + i;
    END LOOP;
    RETURN total;
END;
$$ LANGUAGE plpgsql;

-- FOR con query
CREATE FUNCTION get_all_user_names() RETURNS SETOF TEXT AS $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN SELECT name FROM users ORDER BY name LOOP
        RETURN NEXT rec.name;
    END LOOP;
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- FOR con REVERSE
CREATE FUNCTION count_down(n INTEGER) RETURNS TEXT AS $$
DECLARE
    result TEXT := '';
BEGIN
    FOR i IN REVERSE n..1 LOOP
        result := result || i || ' ';
    END LOOP;
    RETURN TRIM(result);
END;
$$ LANGUAGE plpgsql;

-- FOR con STEP
CREATE FUNCTION even_numbers(max_val INTEGER) RETURNS SETOF INTEGER AS $$
BEGIN
    FOR i IN 0..max_val BY 2 LOOP
        RETURN NEXT i;
    END LOOP;
    RETURN;
END;
$$ LANGUAGE plpgsql;
```

---

## RETURN: valores y tablas

### RETURN single value

```sql
CREATE FUNCTION get_user_count() RETURNS INTEGER AS $$
DECLARE
    count INTEGER;
BEGIN
    SELECT COUNT(*) INTO count FROM users;
    RETURN count;
END;
$$ LANGUAGE plpgsql;
```

### RETURN NEXT (retorna filas)

```sql
CREATE FUNCTION search_products(query TEXT) RETURNS SETOF products AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM products
    WHERE name ILIKE '%' || query || '%'
       OR description ILIKE '%' || query || '%';
    RETURN;
END;
$$ LANGUAGE plpgsql;
```

### RETURN QUERY (alternativa mas limpia)

```sql
CREATE FUNCTION get_active_users() RETURNS SETOF users AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM users WHERE status = 'active';
END;
$$ LANGUAGE plpgsql;
```

### Retorna TABLE

```sql
CREATE FUNCTION get_user_summary()
RETURNS TABLE(
    user_name TEXT,
    order_count BIGINT,
    total_spent DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        u.name,
        COUNT(o.id)::BIGINT,
        COALESCE(SUM(o.total), 0)::DECIMAL
    FROM users u
    LEFT JOIN orders o ON o.user_id = u.id
    GROUP BY u.id, u.name;
END;
$$ LANGUAGE plpgsql;
```

---

## Exception Handling: BEGIN / EXCEPTION

```sql
CREATE FUNCTION safe_divide(
    numerator DECIMAL,
    denominator DECIMAL
) RETURNS DECIMAL AS $$
BEGIN
    RETURN numerator / denominator;
EXCEPTION
    WHEN division_by_zero THEN
        RETURN 0;
    WHEN OTHERS THEN
        RAISE NOTICE 'Error: %', SQLERRM;
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Ejemplo mas robusto
CREATE FUNCTION transfer_funds(
    from_account UUID,
    to_account UUID,
    amount DECIMAL
) RETURNS BOOLEAN AS $$
DECLARE
    from_balance DECIMAL;
BEGIN
    -- Verificar saldo
    SELECT balance INTO from_balance
    FROM accounts WHERE id = from_account
    FOR UPDATE;  -- Bloquear fila

    IF from_balance < amount THEN
        RAISE EXCEPTION 'Saldo insuficiente: % < %', from_balance, amount;
    END IF;

    -- Realizar transferencia
    UPDATE accounts SET balance = balance - amount WHERE id = from_account;
    UPDATE accounts SET balance = balance + amount WHERE id = to_account;

    RETURN TRUE;

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error en transferencia: %', SQLERRM;
        RETURN FALSE;
END;
$$ LANGUAGE plpgsql;
```

**Tipos de excepcion comunes:**

| Excepcion | Descripcion |
|-----------|-------------|
| `division_by_zero` | Division por cero |
| `unique_violation` | Duplicate key value |
| `foreign_key_violation` | FK constraint violation |
| `not_null_violation` | NOT NULL constraint violation |
| `check_violation` | CHECK constraint violation |
| `no_data_found` | SELECT INTO sin resultados |
| `too_many_rows` | SELECT INTO con mas de 1 fila |
| `OTHERS` | Cualquier otra excepcion |

---

## SECURITY DEFINER vs SECURITY INVOKER

```sql
-- SECURITY DEFINER: la funcion se ejecuta con permisos del CREADOR
CREATE FUNCTION admin_delete_user(user_id UUID)
RETURNS VOID
SECURITY DEFINER  -- <-- Clave
AS $$
BEGIN
    DELETE FROM users WHERE id = user_id;
END;
$$ LANGUAGE plpgsql;

-- SECURITY INVOKER: la funcion se ejecuta con permisos del QUE LLAMA (default)
CREATE FUNCTION regular_user_view()
RETURNS SETOF users
SECURITY INVOKER  -- <-- Default, opcional
AS $$
BEGIN
    RETURN QUERY SELECT * FROM users;
END;
$$ LANGUAGE plpgsql;
```

**Cuando usar SECURITY DEFINER:**
- Funciones que necesitan acceder a tablas que el usuario no tiene permiso
- Funciones administrativas
- Funciones de Supabase RPC que bypass RLS

---

## Volatilidad: IMMUTABLE, STABLE, VOLATILE

```sql
-- IMMUTABLE: siempre retorna el mismo resultado para los mismos argumentos
CREATE FUNCTION add(a INTEGER, b INTEGER) RETURNS INTEGER IMMUTABLE AS $$
BEGIN
    RETURN a + b;
END;
$$ LANGUAGE plpgsql;

-- STABLE: resultado consistente dentro de una transaccion
CREATE FUNCTION get_current_user() RETURNS UUID STABLE AS $$
BEGIN
    RETURN auth.uid();  -- No cambia dentro de la transaccion
END;
$$ LANGUAGE plpgsql;

-- VOLATILE: puede retornar diferentes resultados (default)
CREATE FUNCTION get_random_number() RETURNS INTEGER VOLATILE AS $$
BEGIN
    RETURN floor(random() * 100)::INTEGER;
END;
$$ LANGUAGE plpgsql;
```

**Tabla de volatilidad:**

| Nivel | Descripcion | Ejemplo | Optimizacion |
|-------|-------------|---------|--------------|
| `IMMUTABLE` | Mismo resultado siempre | `2 + 2` | Maxima (puede pre-calcularse) |
| `STABLE` | Consistente en transaccion | `NOW()`, `auth.uid()` | Moderada |
| `VOLATILE` | Puede cambiar | `random()`, `nextval()` | Ninguna |

---

## Ejemplo completo: funcion simple

```sql
-- Funcion: buscar usuario por email
CREATE OR REPLACE FUNCTION get_user_by_email(user_email TEXT)
RETURNS TABLE(
    id UUID,
    name TEXT,
    email TEXT,
    created_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT u.id, u.name, u.email, u.created_at
    FROM users u
    WHERE u.email = user_email;

    -- Si no encontro nada, lanzar excepcion
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Usuario no encontrado: %', user_email;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Ejecutar
SELECT * FROM get_user_by_email('ana@test.com');
```

---

## Ejemplo completo: funcion con TABLE

```sql
-- Funcion: buscar productos con filtros
CREATE OR REPLACE FUNCTION search_products(
    search_query TEXT DEFAULT '',
    min_price DECIMAL DEFAULT 0,
    max_price DECIMAL DEFAULT 999999,
    category_filter UUID DEFAULT NULL
)
RETURNS TABLE(
    product_id UUID,
    product_name TEXT,
    product_price DECIMAL,
    category_name TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.name,
        p.price,
        c.name
    FROM products p
    LEFT JOIN categories c ON c.id = p.category_id
    WHERE (search_query = '' OR p.name ILIKE '%' || search_query || '%')
      AND p.price >= min_price
      AND p.price <= max_price
      AND (category_filter IS NULL OR p.category_id = category_filter)
    ORDER BY p.name;
END;
$$ LANGUAGE plpgsql;
```

---

## Ejemplo completo: funcion con transacciones

```sql
-- Funcion: registrar compra con logica de negocio
CREATE OR REPLACE FUNCTION purchase_product(
    p_user_id UUID,
    p_product_id UUID,
    p_quantity INTEGER
) RETURNS JSONB AS $$
DECLARE
    v_stock INTEGER;
    v_price DECIMAL;
    v_total DECIMAL;
    v_order_id INTEGER;
BEGIN
    -- 1. Verificar stock
    SELECT stock, price INTO v_stock, v_price
    FROM products WHERE id = p_product_id
    FOR UPDATE;

    IF v_stock IS NULL THEN
        RAISE EXCEPTION 'Producto no encontrado';
    END IF;

    IF v_stock < p_quantity THEN
        RAISE EXCEPTION 'Stock insuficiente: % disponible, % solicitado',
            v_stock, p_quantity;
    END IF;

    -- 2. Calcular total
    v_total := v_price * p_quantity;

    -- 3. Crear orden
    INSERT INTO orders (user_id, total, status)
    VALUES (p_user_id, v_total, 'pending')
    RETURNING id INTO v_order_id;

    -- 4. Agregar items
    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    VALUES (v_order_id, p_product_id, p_quantity, v_price);

    -- 5. Actualizar stock
    UPDATE products SET stock = stock - p_quantity WHERE id = p_product_id;

    -- 6. Retornar resumen
    RETURN jsonb_build_object(
        'order_id', v_order_id,
        'total', v_total,
        'quantity', p_quantity,
        'status', 'pending'
    );
END;
$$ LANGUAGE plpgsql;
```

---

## Ejemplo completo: funcion con exception handling

```sql
-- Funcion: division segura con manejo de errores
CREATE OR REPLACE FUNCTION safe_divide(
    p_numerator DECIMAL,
    p_denominator DECIMAL,
    p_precision INTEGER DEFAULT 2
) RETURNS JSONB AS $$
DECLARE
    v_result DECIMAL;
BEGIN
    -- Validar entrada
    IF p_denominator = 0 THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Division por cero',
            'code', 'DIVISION_BY_ZERO'
        );
    END IF;

    -- Calcular resultado
    v_result := round(p_numerator / p_denominator, p_precision);

    RETURN jsonb_build_object(
        'success', true,
        'result', v_result,
        'numerator', p_numerator,
        'denominator', p_denominator
    );

EXCEPTION
    WHEN numeric_value_out_of_range THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', 'Resultado fuera de rango',
            'code', 'NUMERIC_OUT_OF_RANGE'
        );
    WHEN OTHERS THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', SQLERRM,
            'code', SQLSTATE
        );
END;
$$ LANGUAGE plpgsql;
```

---

## Resumen

```
┌──────────────────────────────────────────────────────┐
│              PL/pgSQL - RESUMEN                      │
├──────────────────────────────────────────────────────┤
│  CREATE FUNCTION -> Definir funcion                  │
│  DECLARE         -> Variables locales                │
│  %TYPE / %ROWTYPE -> Tipos derivados                 │
│  IF/ELSIF/ELSE   -> Condicionales                   │
│  LOOP/WHILE/FOR  -> Iteracion                        │
│  RETURN          -> Valor de salida                  │
│  EXCEPTION       -> Manejo de errores                │
│  SECURITY DEFINER -> Permisos del creador            │
│  VOLATILE        -> Comportamiento de cache          │
└──────────────────────────────────────────────────────┘
```

---

**Siguiente:** [05 - Triggers y Automatizacion](05-triggers-automatizacion.md)
