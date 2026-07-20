# Practica 3: Puente hacia Supabase

> Conecta todo el conocimiento SQL que adquiriste con los conceptos que usaras en Supabase. Esta practica es el puente entre SQL puro y el desarrollo real con Supabase.

```
+---------------------------------------------------------------+
|                        EL PUENTE                                |
|                                                                 |
|  SQL Aprendido                     Supabase                     |
|  =============                     ========                     |
|                                                                 |
|  CREATE TABLE        ------>    migraciones SQL en Supabase     |
|  INSERT/SELECT      ------>    Supabase SDK (Flutter)          |
|  RLS Policies        ------>    Dashboard > Auth > Policies     |
|  Functions           ------>    Edge Functions / DB Functions   |
|  Indexes             ------>    Dashboard > Database > Indexes  |
|                                                                 |
|  SQL es la base ---> Supabase es la plataforma que la usa       |
+---------------------------------------------------------------+
## Concept Mapping Table

Esta tabla es la referencia rapida. Cuando veas un concepto en Supabase, recuerda su equivalente SQL.

| SQL Concept | Supabase Equivalent | Donde se configura |
|------------|-------------------|-------------------|
| CREATE TABLE | Migraciones SQL en `/supabase/migrations/` | CLI: `supabase migration new` |
| INSERT/SELECT | SDK: `supabase.from('t').insert()` / `select()` | Codigo Flutter |
| JOINs | SDK: `supabase.from('t').select('*, relacion:tabla(*)')` | Codigo Flutter |
| RLS Policy (WHERE) | Policy en Dashboard SQL | Dashboard > Auth > Policies |
| GRANT/REVOKE | RLS Policies + role check | Policies |
| Functions | Edge Functions (Deno/TS) o Database Functions | CLI: `supabase functions new` |
| Triggers | Database Triggers (Dashboard SQL) | Dashboard > Database > Triggers |
| Indexes | Dashboard > Database > Indexes | Dashboard SQL: CREATE INDEX |
| Full-Text Search | `textSearch()` en SDK o consulta directa | Consultas SQL o SDK |
| JSONB | `jsonb` type + `->>` operator | Dashboard SQL |
| LIMIT/OFFSET | SDK: `.limit(10).offset(20)` | Codigo Flutter |
| INNER JOIN | SDK: `.select('*, tabla!inner(*)')` | Codigo Flutter |

## How to read a Supabase Migration File

Cuando ejecutes `supabase migration new nombre_de_migracion`, se crea un archivo SQL en:

```
supabase/
  migrations/
    20260720001_nombre.sql
```

Veamos un ejemplo real de lo que encontraras:

```sql
-- 20260720001_create_products.sql

-- 1. Crear tabla products
CREATE TABLE IF NOT EXISTS products (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    -- BIGINT en vez de SERIAL? Supabase usa BIGINT para manejar m datos
    name TEXT NOT NULL,
    description TEXT,
    price NUMERIC (10, 2) NOT NULL DEFAULT 0.0,
    category_id BIGINT REFERENCES categories(id) ON DELETE SET NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Agregar RLS (Row Level Security)
ALTER TABLE products ALTER COLUMN category_id DROP DEFAULT;

-- 3. Habilitar RLS (por defecto todo esta bloqueado)
ALTER TABLE products FORCE ROW LEVEL SECURITY;
-- Sin policies, NADIE puede hacer SELECT, ni siquiera el usuario de la app.

-- 4. Crear una policy basica (para usuarios autenticados)
CREATE POLICY "Los usuarios autenticados pueden leer productos"
ON products FOR SELECT
USING (auth.role() = 'authenticated');

-- 5. (opcional) policy para admins
CREATE POLICY "Solo los admins pueden insertar"
ON products FOR INSERT
WITH CHECK (auth.jwt() ->> 'role' = 'admin');
```

**Preguntas guia para leer una migracion:**
1. Que tablas crea? (CREATE TABLE)
2. Que relaciones define? (REFERENCES / FOREIGN KEY)
3. Que tipos de datos usa? (BIGINT, TEXT, NUMERIC, TIMESTAMPTZ, etc.)
4. Que restricciones aplica? (NOT NULL, DEFAULT, UNIQUE, CHECK)
5. Habilito RLS? Necesitas leer las policies.

## How Supabase Dashboard Muestra Tu Schema

El Dashboard tiene una seccion **Database > Tables** que te muestra:

```
+-------------------------------------------------------------+
|  Database > Tables                                           |
|                                                               |
|  products                                                     |
|  +-------+--------+---------+-------------+                  |
|  | id    | name   | price   | created_at  |                  |
|  |-------+--------+---------+-------------|                  |
|  | 1     | Laptop | 1299.99 | 2026-07-20 |                  |
|  | 2     | Mouse  | 29.99   | 2026-07-20 |                  |
|  +-------+--------+---------+-------------+                  |
|                                                               |
|  Primary Key: "id"                                           |
|  Foreign Keys:                                               |
|    "category_id" -> categories(id)                           |
|  Indexes: [idx_products_name]                                |
|  RLS enabled: YES                                            |
|  Policies: [CAN_READ, CAN_INSERT...]                          |
+-------------------------------------------------------------+
```

El Dashboard te da:
- Vista visual de las tablas y sus columnas
- Indices existentes
- Constraints (Primary/Foreign Key, NOT NULL, etc.)
- Estado del RLS (activado o desactivado)
- Policies asignadas

## The SQL Editor in Supabase

El SQL Editor es tu herramienta principal para practicar SQL en Supabase:

```
+-------------------------------------------------------------+
|  SQL Editor | New Query                                      |
|                                                               |
|  CREATE TABLE test (id INT);                                  |
|  |                                                           |
|  [RUN] [Explain] [Save]                                      |
|                                                               |
|  Output:                                                      |
|  +---------------------------------------------------------+|
|  | CREATE TABLE                                              ||
|  | Time: 12ms                                                ||
|  +---------------------------------------------------------+|
|        |
|  ✗ No rows affected                                         |
+-------------------------------------------------------------+
```

**Ventajas de usar el SQL Editor:**
- No necesitas instalar nada (es web)
- Historial de consultas
- Boton **Explain** que muestra el plan de ejecucion
- Puedes guardar consultas para reutilizar
- Resultados en tabla interactiva

**En tu proyecto de Supabase:**
1. Abre el Dashboard
2. Navega a **SQL Editor**
3. Alli puedes escribir y ejecutar TODO el SQL que aprendiste en los submodulos 1 y 2.

## Preview de PARTE 1: Desarrollo Local

Ahora que sabes SQL, el siguiente paso es montar Supabase localmente con Docker y empezar a trabajar con un flujo profesional.

### Lo que cubre PARTE 1:

| Tema | Descripcion |
|------|-------------|
| Configuracion con Docker | `docker compose up` para levantar Supabase |
| Supabase CLI | `supabase init`, `supabase start`, `supabase stop` |
| Migraciones SQL | `supabase migration new` + escribir SQL |
| Seeds | Poblar BD con datos de prueba |
| RLS Policies | Seguridad a nivel de fila |
| Integracion con Flutter | `supabase_flutter` client SDK |
| Edge Functions | Deno + TypeScript |
| Testing con pgTAP | Tests para tu base de datos |

### Premium importante: Ya sabes SQL!

La mitad de PARTE 1 es SQL. Migraciones, seeds, RLS policies y triggers son SQL que escribes tu mismo. Al completar esta PARTE 0, tendras el 100% del conocimiento necesario para avanzar sin tropiezos.

**Siguiente paso:** Ve a [PARTE 1: Desarrollo Local](../../PARTE-1-DESARROLLO/).

## How auth.uid() Conects to Your Tables

Supabase tiene un concepto central para la seguridad: el usuario autentcado.

### El flujo simplificado

```
+-------------------------------------------------------------+
|        FLUJO DE AUTENTICACION Y RLS                          |
|                                                               |
|  1. Usuario se loguea en Flutter                               |
|     supabase.auth.signIn(email, password)                     |
|                                                               |
|  2. Supabase devuelve un JWT con user_id                     |
|                                                               |
|  3. Flutter hace una query:                                   |
|     supabase.from('reservations').select('*')                 |
|                                                               |
|  4. PostgreSQL ve el JWT y extrae user_id:                   |
|     auth.user_id()                                            |
|                                                               |
|  5. RLS policy chequea si la fila pertenece al usuario:      |
|     client_id IN (                                             |
|       SELECT id FROM clients WHERE auth_user_id = auth.uid() |
|     )                                                         |
|                                                               |
|  6. Si pasa, devuelve datos. Si no, fila vacia.              |
+-------------------------------------------------------------+
```

### Ejemplo de policy con RLS

```sql
-- Policy que permite a un cliente ver solo sus reservas
CREATE POLICY "Clientes pueden ver propias reservas"
ON reservations
FOR SELECT
USING (
    client_id IN (
        SELECT id FROM clients
        WHERE auth_user_id = auth.uid()
    )
);

-- Policy que permite a un cliente insertar reservas
CREATE POLICY "Clientes pueden crear reservas"
ON reservations
FOR INSERT
WITH CHECK (
    client_id IN (
        SELECT id FROM clients
        WHERE auth_user_id = auth.uid()
    )
);
```

### Relación de tu schema con auth.uid()

Tu tabla **clients** tiene una columna `auth_user_id UUID`. Cuando un usuario se registra en Supabase:

1. Supabase crea una fila en `auth.users` con su UUID.
2. Tú debes crear una fila en `clients` con `auth_user_id` igual al UUID del `auth.users`.
3. Las RLS policies comparan `auth.uid()` con `clients.auth_user_id` para determinar acceso.

```

auth.users (Supabase internal)       tus tablas (public schema)
+----------------------------+       +----------------------------+
| id (UUID)                  |       | clients                    |
| email                      |       | id (SERIAL)                |
| created_at                 |       | auth_user_id  (UUID)       |
+----------------------------+       | full_name                   |
       |                              +----------------------------+
       | Se relaciona via
       | auth_user_id en tu tabla
       v
       +-- clients.auth_user_id = auth.uid()

 ej: supabase.auth.getUser() -> UUID = 'abc-123'

 query:
   SELECT * FROM reservations r
   INNER JOIN clients c ON c.id = r.client_id
   WHERE c.auth_user_id = 'abc-123';
```

## Quick Test: Run a Query in the SQL Editor

Como ultimo ejercicio, abre tu proyecto de Supabase (o crea uno gratuitamente en [supabase.com](https://supabase.com)) y ejecuta este query completo para verificar que todo funciona:

```sql
-- Test: Verifica que entiendes SQL y Supabase

-- 1. Crear una tabla temporal
CREATE TABLE IF NOT EXISTS test_supabase (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Insertar algunos registros
INSERT INTO test_supabase (message) VALUES
    ('SQL funciona en Supabase!'),
    ('Listo para PARTE 1'),
    ('auth.uid() es la clave para RLS');

-- 3. Consultar los resultados
SELECT * FROM test_supabase;

-- 4. Bonus: Verificar que auth.uid() existe
SELECT auth.uid();
-- Nota: Si no estas autenticado, devuelve NULL. Eso es normal.
```

### Interpretacion del resultado

| id | message | created_at |
|----|---------|-----------|
| 1 | SQL funciona en Supabase! | 2026-07-20 ... |
| 2 | Listo para PARTE 1 | 2026-07-20 ... |
| 3 | auth.uid() es la clave para RLS | 2026-07-20 ... |

Y `SELECT auth.uid()` devuelve NULL (porque no hay sesion activa en el SQL Editor). En Flutter, con el SDK, auth.uid() tendra el ID del usuario autenticado.

## Resumen

```
+-------------------------------------------------------------------+
|                   PUENTE COMPLETADO!                                |
|                                                                     |
|  Ya puedes:                                                         |
|                                                                     |
|  1. Leer un archivo de migracion de Supabase y entenderlo           |
|  2. Usar el SQL Editor de Supabase                                  |
|  3. Entender como auth.uid() se relaciona con tus tablas            |
|  4. Reconocer conceptos SQL en el Dashboard de Supabase            |
|                                                                     |
|  Lo que viene:                                                      |
|  - PARTE 1: Desarrollo Local con Docker + CLI                       |
|  - PARTE 2: Produccion (supabase self-hosted)                      |
|  - PARTE 3: CI/CD + Automatizaciones                                |
|                                                                     |
+-------------------------------------------------------------------+
|

> **Siguiente paso:** [PARTE 1: Desarrollo Local](../../PARTE-1-DESARROLLO/)
