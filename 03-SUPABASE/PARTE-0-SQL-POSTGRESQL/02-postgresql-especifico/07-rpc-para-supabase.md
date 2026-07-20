# 07 - RPC para Supabase

> RPC (Remote Procedure Call) permite ejecutar funciones PostgreSQL directamente desde Flutter. Es la forma de ejecutar logica compleja en la BD sin crear endpoints REST.

---

## Que es RPC en Supabase

**RPC** en Supabase es simplemente llamar a una funcion PostgreSQL usando `supabase.rpc()`. No es un concepto nuevo: es una funcion PostgreSQL normal que Supabase expone via HTTP.

```
┌─────────────────────────────────────────────────────┐
│  ARQUITECTURA RPC EN SUPABASE                       │
│                                                     │
│  ┌─────────┐    HTTP     ┌──────────┐    SQL        │
│  │ Flutter │ ──────────> │ Supabase │ ──────────>   │
│  │   App   │  .rpc()     │   API    │  PostgreSQL   │
│  └─────────┘             └──────────┘    Function   │
│                                                     │
│  1. Flutter llama a supabase.rpc('funcion')         │
│  2. Supabase envia la llamada via HTTP               │
│  3. PostgreSQL ejecuta la funcion                    │
│  4. Resultado regresa a Flutter                      │
└─────────────────────────────────────────────────────┘
```

**Fuente:** Supabase Docs - Calling PostgreSQL Stored Procedures

---

## Crear funciones RPC

### 1. Funcion simple: get_user_count

```sql
-- Funcion que retorna un entero
CREATE OR REPLACE FUNCTION get_user_count()
RETURNS INTEGER AS $$
DECLARE
    total INTEGER;
BEGIN
    SELECT COUNT(*) INTO total FROM users;
    RETURN total;
END;
$$ LANGUAGE plpgsql;
```

**Llamar desde Flutter:**

```dart
final response = await supabase.rpc('get_user_count');
final count = response as int;
print('Total usuarios: $count');
```

### 2. Funcion con parametros: search_products

```sql
-- Funcion con parametros
CREATE OR REPLACE FUNCTION search_products(
    search_query TEXT,
    category_id UUID DEFAULT NULL,
    max_results INTEGER DEFAULT 10
)
RETURNS TABLE(
    id UUID,
    name TEXT,
    price DECIMAL,
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
      AND (category_id IS NULL OR p.category_id = category_id)
    ORDER BY p.name
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;
```

**Llamar desde Flutter:**

```dart
final response = await supabase.rpc('search_products', params: {
  'search_query': 'laptop',
  'category_id': 'uuid-aqui',
  'max_results': 5,
});

final products = (response as List).map((p) => Product.fromJson(p)).toList();
```

### 3. Funcion retornando JSON/JSONB: get_user_profile

```sql
-- Funcion que retorna JSONB
CREATE OR REPLACE FUNCTION get_user_profile(user_id UUID)
RETURNS JSONB AS $$
DECLARE
    result JSONB;
BEGIN
    SELECT jsonb_build_object(
        'id', u.id,
        'name', u.name,
        'email', u.email,
        'order_count', (SELECT COUNT(*) FROM orders o WHERE o.user_id = u.id),
        'total_spent', (SELECT COALESCE(SUM(o.total), 0) FROM orders o WHERE o.user_id = u.id),
        'last_order', (SELECT MAX(created_at) FROM orders o WHERE o.user_id = u.id)
    )
    INTO result
    FROM users u
    WHERE u.id = user_id;

    IF result IS NULL THEN
        RAISE EXCEPTION 'Usuario no encontrado';
    END IF;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

**Llamar desde Flutter:**

```dart
final response = await supabase.rpc('get_user_profile', params: {
  'user_id': currentUser.id,
});

final profile = UserProfile.fromJson(response);
```

### 4. Funcion con resultados de tabla: get_orders_with_items

```sql
-- Funcion que retorna multiples filas como JSON
CREATE OR REPLACE FUNCTION get_orders_with_items(user_id UUID)
RETURNS JSONB AS $$
BEGIN
    RETURN (
        SELECT jsonb_agg(
            jsonb_build_object(
                'id', o.id,
                'total', o.total,
                'status', o.status,
                'created_at', o.created_at,
                'items', (
                    SELECT jsonb_agg(
                        jsonb_build_object(
                            'product_name', p.name,
                            'quantity', oi.quantity,
                            'unit_price', oi.unit_price
                        )
                    )
                    FROM order_items oi
                    JOIN products p ON p.id = oi.product_id
                    WHERE oi.order_id = o.id
                )
            )
        )
        FROM orders o
        WHERE o.user_id = user_id
        ORDER BY o.created_at DESC
    );
END;
$$ LANGUAGE plpgsql;
```

**Llamar desde Flutter:**

```dart
final response = await supabase.rpc('get_orders_with_items', params: {
  'user_id': currentUser.id,
});

final orders = (response as List)
    .map((o) => OrderWithItems.fromJson(o))
    .toList();
```

### 5. Funcion con transacciones: purchase_product

```sql
-- Funcion que ejecuta transacciones
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
    -- Verificar stock
    SELECT stock, price INTO v_stock, v_price
    FROM products WHERE id = p_product_id
    FOR UPDATE;

    IF v_stock IS NULL THEN
        RAISE EXCEPTION 'Producto no encontrado';
    END IF;

    IF v_stock < p_quantity THEN
        RAISE EXCEPTION 'Stock insuficiente';
    END IF;

    -- Crear orden
    v_total := v_price * p_quantity;
    INSERT INTO orders (user_id, total, status)
    VALUES (p_user_id, v_total, 'pending')
    RETURNING id INTO v_order_id;

    -- Agregar items
    INSERT INTO order_items (order_id, product_id, quantity, unit_price)
    VALUES (v_order_id, p_product_id, p_quantity, v_price);

    -- Actualizar stock
    UPDATE products SET stock = stock - p_quantity WHERE id = p_product_id;

    RETURN jsonb_build_object(
        'order_id', v_order_id,
        'total', v_total,
        'status', 'pending'
    );
END;
$$ LANGUAGE plpgsql;
```

**Llamar desde Flutter:**

```dart
try {
  final response = await supabase.rpc('purchase_product', params: {
    'p_user_id': currentUser.id,
    'p_product_id': productId,
    'p_quantity': 2,
  });

  final order = Order.fromJson(response);
  print('Orden creada: ${order.id}');
} catch (e) {
  print('Error: $e');
}
```

---

## Seguridad: SECURITY DEFINER vs SECURITY INVOKER

```sql
-- SECURITY DEFINER: la funcion corre con permisos del CREADOR
-- Ideal para funciones que necesitan bypass RLS
CREATE OR REPLACE FUNCTION admin_get_all_users()
RETURNS SETOF users
SECURITY DEFINER  -- <-- Accede a todas las filas
AS $$
BEGIN
    RETURN QUERY SELECT * FROM users;
END;
$$ LANGUAGE plpgsql;

-- SECURITY INVOKER: la funcion corre con permisos del QUE LLAMA (default)
-- Respeta RLS normalmente
CREATE OR REPLACE FUNCTION get_my_profile()
RETURNS JSONB
SECURITY INVOKER  -- <-- Default, opcional
AS $$
BEGIN
    RETURN (
        SELECT jsonb_build_object(
            'id', id, 'name', name, 'email', email
        )
        FROM users
        WHERE id = auth.uid()  -- Solo el usuario actual
    );
END;
$$ LANGUAGE plpgsql;
```

**Regla de oro:**
- Usa `SECURITY INVOKER` (default) cuando la funcion debe respetar RLS
- Usa `SECURITY DEFINER` solo cuando necesitas acceso elevado

---

## Error handling en RPC

```sql
-- Funcion con manejo de errores claro
CREATE OR REPLACE FUNCTION safe_update_user(
    p_user_id UUID,
    p_name TEXT DEFAULT NULL,
    p_email TEXT DEFAULT NULL
) RETURNS JSONB AS $$
BEGIN
    -- Verificar que el usuario existe
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = p_user_id) THEN
        RAISE EXCEPTION 'Usuario no encontrado'
            USING ERRCODE = 'P0002';
    END IF;

    -- Verificar email unico
    IF p_email IS NOT NULL AND EXISTS (
        SELECT 1 FROM users WHERE email = p_email AND id != p_user_id
    ) THEN
        RAISE EXCEPTION 'El email ya esta en uso: %', p_email
            USING ERRCODE = 'P0003';
    END IF;

    -- Actualizar
    UPDATE users SET
        name = COALESCE(p_name, name),
        email = COALESCE(p_email, email)
    WHERE id = p_user_id;

    RETURN jsonb_build_object(
        'success', true,
        'message', 'Usuario actualizado'
    );

EXCEPTION
    WHEN OTHERS THEN
        RETURN jsonb_build_object(
            'success', false,
            'error', SQLERRM,
            'code', SQLSTATE
        );
END;
$$ LANGUAGE plpgsql;
```

**Llamar desde Flutter y manejar errores:**

```dart
final response = await supabase.rpc('safe_update_user', params: {
  'p_user_id': userId,
  'p_name': 'Nuevo Nombre',
});

if (response['success'] == true) {
  // Exito
} else {
  // Error: response['error'] contiene el mensaje
  print('Error: ${response['error']}');
}
```

---

## Llamar RPC desde Flutter

### Sintaxis basica

```dart
// Sin parametros
final response = await supabase.rpc('get_user_count');

// Con parametros posicionales
final response = await supabase.rpc('search_products', params: {
  'search_query': 'laptop',
});

// Con multiples parametros
final response = await supabase.rpc('get_orders_with_items', params: {
  'user_id': 'uuid-aqui',
  'status_filter': 'pending',
  'limit': 20,
});
```

### Manejar respuesta

```dart
// Respuesta simple (INTEGER, TEXT)
final count = await supabase.rpc('get_user_count') as int;

// Respuesta como lista (SETOF)
final users = await supabase.rpc('get_active_users') as List;
final userList = users.map((u) => User.fromJson(u)).toList();

// Respuesta como JSONB
final profile = await supabase.rpc('get_user_profile', params: {
  'user_id': userId,
});
final userProfile = UserProfile.fromJson(profile);

// Manejar error
try {
  final response = await supabase.rpc('purchase_product', params: {
    'p_user_id': userId,
    'p_product_id': productId,
    'p_quantity': 1,
  });
} on PostgrestException catch (e) {
  print('Error de Supabase: ${e.message}');
} catch (e) {
  print('Error inesperado: $e');
}
```

### Type safety: mapear a Dart models

```dart
// Modelo Dart
class UserProfile {
  final String id;
  final String name;
  final String email;
  final int orderCount;
  final double totalSpent;

  UserProfile({
    required this.id,
    required this.name,
    required this.email,
    required this.orderCount,
    required this.totalSpent,
  });

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      orderCount: json['order_count'],
      totalSpent: (json['total_spent'] as num).toDouble(),
    );
  }
}

// Llamar RPC con tipo seguro
Future<UserProfile> getUserProfile(String userId) async {
  final response = await supabase.rpc('get_user_profile', params: {
    'user_id': userId,
  });
  return UserProfile.fromJson(response);
}
```

---

## Patrones comunes de RPC

### 1. Aggregation queries

```sql
-- Contar, sumar, promediar
CREATE OR REPLACE FUNCTION get_dashboard_stats()
RETURNS JSONB AS $$
BEGIN
    RETURN jsonb_build_object(
        'total_users', (SELECT COUNT(*) FROM users),
        'total_orders', (SELECT COUNT(*) FROM orders),
        'total_revenue', (SELECT COALESCE(SUM(total), 0) FROM orders),
        'avg_order_value', (SELECT COALESCE(AVG(total), 0) FROM orders),
        'active_users', (SELECT COUNT(*) FROM users WHERE status = 'active')
    );
END;
$$ LANGUAGE plpgsql;
```

### 2. Busquedas complejas con filtros

```sql
-- Busqueda avanzada con multiples filtros
CREATE OR REPLACE FUNCTION advanced_search(
    p_query TEXT DEFAULT '',
    p_min_price DECIMAL DEFAULT 0,
    p_max_price DECIMAL DEFAULT 999999,
    p_category UUID DEFAULT NULL,
    p_in_stock BOOLEAN DEFAULT NULL,
    p_sort_by TEXT DEFAULT 'name',
    p_sort_order TEXT DEFAULT 'asc',
    p_limit INTEGER DEFAULT 20,
    p_offset INTEGER DEFAULT 0
)
RETURNS TABLE(
    id UUID,
    name TEXT,
    price DECIMAL,
    category_name TEXT,
    in_stock BOOLEAN,
    total_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH filtered AS (
        SELECT
            p.id,
            p.name,
            p.price,
            c.name AS category_name,
            (p.stock > 0) AS in_stock
        FROM products p
        LEFT JOIN categories c ON c.id = p.category_id
        WHERE (p_query = '' OR p.name ILIKE '%' || p_query || '%')
          AND p.price BETWEEN p_min_price AND p_max_price
          AND (p_category IS NULL OR p.category_id = p_category)
          AND (p_in_stock IS NULL OR (p.stock > 0) = p_in_stock)
    )
    SELECT
        f.*,
        (SELECT COUNT(*) FROM filtered)::BIGINT AS total_count
    FROM filtered f
    ORDER BY
        CASE WHEN p_sort_by = 'name' AND p_sort_order = 'asc' THEN f.name END ASC,
        CASE WHEN p_sort_by = 'name' AND p_sort_order = 'desc' THEN f.name END DESC,
        CASE WHEN p_sort_by = 'price' AND p_sort_order = 'asc' THEN f.price END ASC,
        CASE WHEN p_sort_by = 'price' AND p_sort_order = 'desc' THEN f.price END DESC
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
```

### 3. Batch operations

```sql
-- Actualizar multiples registros en lote
CREATE OR REPLACE FUNCTION bulk_update_status(
    p_ids UUID[],
    p_status TEXT
) RETURNS JSONB AS $$
DECLARE
    updated_count INTEGER;
BEGIN
    UPDATE users SET status = p_status WHERE id = ANY(p_ids);
    GET DIAGNOSTICS updated_count = ROW_COUNT;

    RETURN jsonb_build_object(
        'success', true,
        'updated_count', updated_count
    );
END;
$$ LANGUAGE plpgsql;
```

### 4. Validacion cross-table

```sql
-- Validar datos en multiples tablas antes de insertar
CREATE OR REPLACE FUNCTION create_order_with_validation(
    p_user_id UUID,
    p_items JSONB  -- [{"product_id": "...", "quantity": 2}]
)
RETURNS JSONB AS $$
DECLARE
    v_order_id INTEGER;
    v_item JSONB;
    v_product RECORD;
    v_total DECIMAL := 0;
BEGIN
    -- Verificar usuario activo
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = p_user_id AND status = 'active') THEN
        RAISE EXCEPTION 'Usuario no activo';
    END IF;

    -- Crear orden
    INSERT INTO orders (user_id, status)
    VALUES (p_user_id, 'pending')
    RETURNING id INTO v_order_id;

    -- Procesar cada item
    FOR v_item IN SELECT * FROM jsonb_array_elements(p_items)
    LOOP
        SELECT * INTO v_product
        FROM products WHERE id = (v_item->>'product_id')::UUID
        FOR UPDATE;

        IF v_product IS NULL THEN
            RAISE EXCEPTION 'Producto no encontrado: %', v_item->>'product_id';
        END IF;

        IF v_product.stock < (v_item->>'quantity')::INTEGER THEN
            RAISE EXCEPTION 'Stock insuficiente para: %', v_product.name;
        END IF;

        -- Insertar item
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (
            v_order_id,
            v_product.id,
            (v_item->>'quantity')::INTEGER,
            v_product.price
        );

        -- Actualizar stock
        UPDATE products
        SET stock = stock - (v_item->>'quantity')::INTEGER
        WHERE id = v_product.id;

        v_total := v_total + (v_product.price * (v_item->>'quantity')::INTEGER);
    END LOOP;

    -- Actualizar total
    UPDATE orders SET total = v_total WHERE id = v_order_id;

    RETURN jsonb_build_object(
        'order_id', v_order_id,
        'total', v_total,
        'items_count', jsonb_array_length(p_items)
    );
END;
$$ LANGUAGE plpgsql;
```

---

## RPC vs Edge Functions

| Criterio | RPC (PostgreSQL Functions) | Edge Functions (Deno) |
|----------|---------------------------|----------------------|
| **Donde corre** | En la BD | En CDN (edge) |
| **Latencia** | Minima (sin network roundtrip) | Network roundtrip |
| **Acceso a DB** | Directo, sin overhead | Via HTTP (supabase client) |
| **Lenguaje** | PL/pgSQL | JavaScript/TypeScript |
| **Librerias** | Solo PostgreSQL | NPM completo |
| **Complejidad** | Logica de BD | Logica de negocio externa |
| **RLS** | Puede bypass (SECURITY DEFINER) | Usa client auth |
| **Uso ideal** | Consultas complejas, validaciones, batch | Webhooks, APIs externas, email |

```
┌─────────────────────────────────────────────────────┐
│  USA RPC CUANDO:                                   │
│  - Consulta involucra multiples tablas              │
│  - Necesitas atomicidad (transacciones)             │
│  - Operaciones batch (muchos registros)             │
│  - Validacion cross-table                           │
│  - Aggregation queries                              │
│                                                     │
│  USA EDGE FUNCTIONS CUANDO:                         │
│  - Necesitas llamar APIs externas                   │
│  - Enviar emails, SMS, notificaciones push          │
│  - Webhooks de Stripe, MercadoPago                  │
│  - Logica que no accede directamente a la BD        │
│  - Procesamiento de imagenes/archivos               │
└─────────────────────────────────────────────────────┘
```

---

## Performance de RPC

```sql
-- 1. Usa LIMIT dentro de la funcion
CREATE OR REPLACE FUNCTION search_products_fast(query TEXT)
RETURNS SETOF products AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM products
    WHERE name ILIKE '%' || query || '%'
    LIMIT 50;  -- <-- Siempre limita
END;
$$ LANGUAGE plpgsql;

-- 2. Usa EXPLAIN ANALYZE para optimizar
EXPLAIN ANALYZE SELECT * FROM search_products_fast('laptop');

-- 3. Evita SELECT * en funciones que retornan TABLE
-- MAL: retorna todas las columnas
SELECT * FROM users WHERE ...

-- BIEN: retorna solo las necesarias
SELECT id, name, email FROM users WHERE ...

-- 4. Usa indexes en las columnas que filtras
-- Ya viste esto en 03-indexes-rendimiento.md

-- 5. Connection pooling: Supabase maneja esto automaticamente
-- No necesitas preocuparte por el pool de conexiones
```

---

## Resumen

```
┌──────────────────────────────────────────────────────┐
│              RPC EN SUPABASE                         │
├──────────────────────────────────────────────────────┤
│  Flutter -> supabase.rpc() -> PostgreSQL function    │
│                                                      │
│  Crear: CREATE FUNCTION ... RETURNS ... LANGUAGE pl  │
│  Llamar: supabase.rpc('nombre', params: {...})       │
│  Seguridad: SECURITY DEFINER / INVOKER              │
│  Errores: RAISE EXCEPTION + try/catch en Dart       │
│                                                      │
│  Usar RPC para: consultas complejas, batch,         │
│  validaciones, atomicidad                           │
│  Usar Edge Functions para: APIs externas, webhooks  │
└──────────────────────────────────────────────────────┘
```

---

**Siguiente:** [08 - Cheatsheet PostgreSQL](08-cheatsheet-postgresql.md)
