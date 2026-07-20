# 02 - Tipos de datos en PostgreSQL

> Cada columna de una tabla debe tener un tipo de dato. Elegir el tipo correcto afecta el rendimiento, la integridad y como Supabase genera los tipos en tu app Flutter.

```
┌──────────────────────────────────────────────────────────────────┐
│                    RESUMEN RAPIDO                                 │
│                                                                  │
│  TEXT     → Cadenas de texto (recomendado en vez de VARCHAR)     │
│  INTEGER  → Numeros enteros                                      │
│  BIGINT   → Numeros enteros muy grandes                          │
│  UUID     → Identificadores unicos (recomendado para PKs)        │
│  TIMESTAMPTZ → Fechas con zona horaria (recomendado)            │
│  BOOLEAN  → true / false / null                                  │
│  JSONB    → JSON nativo con busqueda (recomendado sobre JSON)    │
└──────────────────────────────────────────────────────────────────┘
```

## Indice

1. [Numericos](#tipos-numericos)
2. [Texto](#tipos-de-texto)
3. [Fecha y hora](#tipos-de-fecha-y-hora)
4. [Booleano](#tipo-booleano)
5. [UUID](#tipo-uuid)
6. [JSON](#tipos-json)
7. [Binario](#tipo-binario)
8. [Red](#tipos-de-red)
9. [Tabla resumen completa](#tabla-resumen-completa)
10. [Guia de decision](#guia-de-decision)

---

## Tipos Numericos

### Enteros

| Tipo          | Tamaño en disco | Rango                                              | Cuando usarlo                      |
|---------------|-----------------|-----------------------------------------------------|-------------------------------------|
| `SMALLINT`    | 2 bytes         | -32,768 a 32,767                                   | Edad, calificaciones, prioridades  |
| `INTEGER`     | 4 bytes         | -2,147,483,648 a 2,147,483,647                     | IDs generales, contadores          |
| `BIGINT`      | 8 bytes         | -9.2 x 10^18 a 9.2 x 10^18                        | Contadores muy grandes, timestamps |
| `SERIAL`      | 4 bytes         | 1 a 2,147,483,647 (auto-increment)                 | IDs auto-increment en MySQL/PostgreSQL |
| `BIGSERIAL`   | 8 bytes         | 1 a 9.2 x 10^18 (auto-increment)                  | IDs auto-increment grandes          |

```sql
-- Crear tabla con diferentes tipos de enteros
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,              -- ID auto-increment
    codigo SMALLINT NOT NULL,           -- Codigo corto (max 32767)
    stock INTEGER NOT NULL DEFAULT 0,   -- Stock actual
    ventas_total BIGINT NOT NULL DEFAULT 0 -- Total de ventas acumuladas
);

-- Insertar datos
INSERT INTO productos (codigo, stock, ventas_total)
VALUES (101, 50, 1000000);

-- Consultar
SELECT * FROM productos;
```

### Numeros decimales

| Tipo                 | Tamaño  | Precision | Rango aprox.                    | Cuando usarlo                    |
|----------------------|---------|-----------|----------------------------------|-----------------------------------|
| `NUMERIC(p,s)`       | Variable| Exacta    | Hasta 131,072 digitos           | **Dinero**, calculos exactos      |
| `REAL`               | 4 bytes | ~6 digitos| -3.4 x 10^38 a 3.4 x 10^38     | Coordenadas, mediciones          |
| `DOUBLE PRECISION`   | 8 bytes | ~15 digitos| -1.7 x 10^308 a 1.7 x 10^308  | Calculos cientificos             |

```sql
-- Precios y montos: SIEMPRE usar NUMERIC
CREATE TABLE facturas (
    id SERIAL PRIMARY KEY,
    subtotal NUMERIC(10, 2) NOT NULL,     -- 10 digitos total, 2 decimales
    impuesto NUMERIC(5, 2) NOT NULL,      -- Porcentaje de impuesto
    total NUMERIC(12, 2) NOT NULL         -- Monto total
);

INSERT INTO facturas (subtotal, impuesto, total)
VALUES (150.50, 16.00, 174.58);

-- Usar DOUBLE PRECISION para coordenadas geograficas
CREATE TABLE ubicaciones (
    id SERIAL PRIMARY KEY,
    latitud DOUBLE PRECISION NOT NULL,
    longitud DOUBLE PRECISION NOT NULL
);
```

> **Regla de oro para dinero:** Usa `NUMERIC(precision, scale)` **nunca** `FLOAT` o `DOUBLE PRECISION`. Los floating point tienen errores de redondeo.

---

## Tipos de Texto

| Tipo            | Tamaño                    | Cuando usarlo                          |
|-----------------|---------------------------|----------------------------------------|
| `TEXT`          | Variable (hasta 1GB)      | **Recomendado.** La mayoria de casos   |
| `VARCHAR(n)`    | Variable (hasta n chars)  | Cuando necesitas limitar longitud      |
| `CHAR(n)`       | Siempre n chars           | Casi nunca usar (ISO codes fijos)      |

```sql
-- Comparacion de tipos de texto
CREATE TABLE comparacion_texto (
    campo_text    TEXT NOT NULL,              -- Sin limite, recomendado
    campo_varchar VARCHAR(100) NOT NULL,     -- Maximo 100 caracteres
    campo_char    CHAR(3) NOT NULL           -- Siempre 3 caracteres (rellena con espacios)
);

-- TEXT es flexible y mas rapido en PostgreSQL
INSERT INTO comparacion_texto (campo_text, campo_varchar, campo_char)
VALUES ('Hola mundo', 'Hola', 'ABC');

-- CHAR rellena con espacios
SELECT campo_char, LENGTH(campo_char) FROM comparacion_texto;
-- Resultado: campo_char = 'ABC ', LENGTH = 4
```

> **Recomendacion:** Usa `TEXT` para todo. PostgreSQL no tiene diferencia de rendimiento entre `TEXT` y `VARCHAR`. Si necesitas limitar la longitud, usa un `CHECK` constraint.

---

## Tipos de Fecha y Hora

| Tipo                           | Tamaño | Rango                          | Recomendado? |
|--------------------------------|--------|--------------------------------|--------------|
| `DATE`                         | 4 bytes| 4713 AC a 5874897 AC           | Si (solo fecha) |
| `TIME`                         | 8 bytes| 00:00:00 a 24:00:00            | Raro         |
| `TIMESTAMP`                    | 8 bytes| 4713 AC a 294276 AC            | No           |
| **`TIMESTAMPTZ`**              | 8 bytes| 4713 AC a 294276 AC            | **Si siempre** |
| `TIMESTAMP WITHOUT TIME ZONE`  | 8 bytes| Igual que TIMESTAMP             | No           |
| `INTERVAL`                     | 16 bytes| -178,000,000 a 178,000,000 anos| Duraciones   |

### Formatos de fecha en PostgreSQL

| Formato                 | Ejemplo                    | Descripcion                |
|-------------------------|----------------------------|----------------------------|
| ISO 8601                | `'2025-01-15'`            | Formato estandar           |
| Con hora                | `'2025-01-15 14:30:00'`   | Fecha + hora               |
| Con zona horaria        | `'2025-01-15 14:30:00-05'`| Con offset                 |
| Formato americano       | `'01/15/2025'`            | Mes/Dia/Ano                |

```sql
-- Crear tabla con tipos de fecha
CREATE TABLE eventos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    fecha_evento DATE NOT NULL,
    hora_inicio TIME,
    fecha_hora_completa TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    duracion INTERVAL
);

-- Insertar datos
INSERT INTO eventos (nombre, fecha_evento, hora_inicio, fecha_hora_completa, duracion)
VALUES (
    'Reunion de equipo',
    '2025-03-20',
    '14:30:00',
    '2025-03-20T14:30:00-05:00',
    '2 hours 30 minutes'
);

-- Consultar con funciones de fecha
SELECT
    nombre,
    fecha_evento,
    fecha_hora_completa,
    AGE(fecha_hora_completa) AS tiempo_transcurrido
FROM eventos;
```

> **Regla de oro:** Usa `TIMESTAMPTZ` (con zona horaria) para **siempre**. La zona horaria se guarda automaticamente y se convierte correctamente al consultar.

---

## Tipo Booleano

```sql
-- BOOLEAN: true, false, o null
CREATE TABLE tareas (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    completada BOOLEAN NOT NULL DEFAULT false
);

-- Insertar datos
INSERT INTO tareas (titulo, completada) VALUES
('Aprender SQL', false),
('Configurar Supabase', true);

-- Consultar
SELECT * FROM tareas WHERE completada = true;
SELECT * FROM tareas WHERE completada;          -- Igual que = true
SELECT * FROM tareas WHERE NOT completada;     -- Igual que = false
```

**Valores de BOOLEAN:**

| Valor de entrada | Almacenado como |
|------------------|-----------------|
| `true`, `'t'`, `'yes'`, `'y'`, `'1'` | `true` |
| `false`, `'f'`, `'no'`, `'n'`, `'0'` | `false` |
| `null` (sin valor)                    | `NULL` |

---

## Tipo UUID

**UUID** (Universally Unique Identifier) es un identificador de 128 bits que es unico en todo el mundo.

```sql
-- Extension para generar UUIDs
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Crear tabla con UUID como primary key
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Insertar (el ID se genera automaticamente)
INSERT INTO usuarios (nombre, email) VALUES ('Ana', 'ana@email.com');

-- Resultado:
-- id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
-- nombre: 'Ana'
-- email: 'ana@email.com'
-- created_at: '2025-01-15 10:30:00-05'
```

### UUID vs SERIAL para Primary Keys

| Caracteristica    | SERIAL (Integer)                     | UUID                                  |
|-------------------|--------------------------------------|---------------------------------------|
| Tamaño            | 4 bytes                             | 16 bytes                              |
| Formato           | 1, 2, 3, 4...                       | a1b2c3d4-e5f6-7890-abcd-ef1234567890 |
| Unico globalmente | No (solo en la tabla)                | Si                                    |
| Predictible       | Si (secuencial)                     | No (aleatorio)                        |
| Visible en URL    | Si (/users/42)                      | No (/users/a1b2c3d4-e5f6...)         |
| Supabase          | Funciona                            | **Recomendado**                       |
| Rendimiento en PK | Mas rapido (4 bytes)                | Un poco mas lento (16 bytes)          |
| Merge de datos    | Posibles conflictos de ID           | Sin conflictos                        |

> **En Supabase, usa UUID.** La generacion con `gen_random_uuid()` es criptograficamente segura y sin conflictos. Las tablas de `auth.users` de Supabase ya usan UUID.

---

## Tipos JSON

| Tipo    | Almacenamiento | Busqueda索引 | Recomendado? |
|---------|----------------|-------------|--------------|
| `JSON`  | Texto plano    | No          | No           |
| **`JSONB`** | Binario comprimido | **Si** (GIN index) | **Si** |

```sql
-- Diferencia entre JSON y JSONB
CREATE TABLE configuraciones (
    id SERIAL PRIMARY KEY,
    config_json  JSON NOT NULL,
    config_jsonb JSONB NOT NULL
);

-- Insertar datos JSON
INSERT INTO configuraciones (config_json, config_jsonb)
VALUES (
    '{"tema": "oscuro", "idioma": "es", "notificaciones": true}',
    '{"tema": "oscuro", "idioma": "es", "notificaciones": true}'
);

-- JSONB permite busqueda eficiente con GIN index
CREATE INDEX idx_config_jsonb ON configuraciones USING GIN (config_jsonb);

-- Consultar con operadores JSONB
SELECT
    config_jsonb->>'tema' AS tema,              -- Extraer como texto
    config_jsonb->'notificaciones' AS notif,    -- Extraer como JSON
    config_jsonb @> '{"idioma": "es"}' AS es_espanol  -- Contiene valor
FROM configuraciones;
```

**Operadores JSONB:**

| Operador | Funcion                    | Ejemplo                                      |
|----------|----------------------------|-----------------------------------------------|
| `->`     | Extraer campo (JSON)       | `config->'tema'`                             |
| `->>`    | Extraer campo (texto)      | `config->>'tema'`                            |
| `#>`     | Ruta como array            | `config#>'{nested,key}'`                     |
| `#>>`    | Ruta como texto            | `config#>>'{nested,key}'`                    |
| `@>`     | Contiene                   | `config @> '{"a": 1}'`                       |
| `<@`     | Contenido en               | `'{"a": 1}' <@ config`                       |
| `?`      | Existe clave               | `config ? 'tema'`                            |
| `?|`     | Existe alguna clave        | `config ?| ARRAY['a','b']`                   |
| `?&`     | Existen todas las claves   | `config ?& ARRAY['a','b']`                   |

---

## Tipo Binario

```sql
-- BYTEA: datos binarios (imagenes, archivos, etc.)
CREATE TABLE archivos (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    contenido BYTEA NOT NULL,
    mime_type TEXT NOT NULL
);

-- Insertar un archivo binario
INSERT INTO archivos (nombre, contenido, mime_type)
VALUES ('logo.png', decode('iVBORw0KGgo...', 'base64'), 'image/png');
```

> **Nota:** En Supabase, para archivos grandes usa **Supabase Storage** en vez de `BYTEA`. BYTEA es para datos binarios pequenos.

---

## Tipos de Red

| Tipo       | Ejemplo                    | Uso                                    |
|------------|----------------------------|----------------------------------------|
| `INET`     | `'192.168.1.1'`           | Direccion IP con mascara              |
| `CIDR`     | `'192.168.1.0/24'`        | Bloque de direcciones IP              |
| `MACADDR`  | `'08:00:2b:01:02:03'`     | Direccion MAC de red                  |

```sql
CREATE TABLE conexiones (
    id SERIAL PRIMARY KEY,
    ip_cliente INET NOT NULL,
    mascara CIDR,
    mac_address MACADDR,
    conectado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Insertar
INSERT INTO conexiones (ip_cliente, mascara)
VALUES ('192.168.1.100', '192.168.1.0/24');

-- Buscar IPs en un rango
SELECT * FROM conexiones
WHERE ip_cliente <<= '192.168.1.0/24';  -- Direccion dentro del bloque
```

---

## Tabla resumen completa

| Tipo             | Disco     | Ejemplo de valor                        | Uso recomendado en Supabase           |
|------------------|-----------|-----------------------------------------|---------------------------------------|
| `SMALLINT`       | 2 bytes   | `42`                                   | Edad, prioridad, calificacion         |
| `INTEGER`        | 4 bytes   | `123456`                               | IDs, contadores, enteros generales    |
| `BIGINT`         | 8 bytes   | `9007199254740991`                     | Contadores grandes, timestamps epoch  |
| `SERIAL`         | 4 bytes   | `1, 2, 3...` (auto)                   | PKs auto-increment (legacy)           |
| `BIGSERIAL`      | 8 bytes   | `1, 2, 3...` (auto)                   | PKs auto-increment grandes            |
| `NUMERIC(p,s)`   | Variable  | `999999.99`                            | **Dinero, precios, montos**           |
| `REAL`           | 4 bytes   | `3.14`                                 | Coordenadas, mediciones aproximadas   |
| `DOUBLE PRECISION`| 8 bytes  | `3.14159265358979`                     | Calculos cientificos                  |
| `TEXT`           | Variable  | `'Hola mundo'`                         | **Nombres, emails, descripciones**    |
| `VARCHAR(n)`     | Variable  | `'Hola'` (max n chars)                 | Cuando necesitas limitar longitud     |
| `CHAR(n)`        | n bytes   | `'AB'` (siempre n chars)               | ISO codes fijos (raro usar)           |
| `DATE`           | 4 bytes   | `'2025-01-15'`                         | Solo fecha (sin hora)                 |
| `TIMESTAMPTZ`    | 8 bytes   | `'2025-01-15 14:30:00-05'`            | **Fechas con zona horaria**           |
| `INTERVAL`       | 16 bytes  | `'2 hours 30 minutes'`                 | Duraciones, edades                    |
| `BOOLEAN`        | 1 byte    | `true` / `false` / `NULL`              | Flags, estados, activo/inactivo       |
| `UUID`           | 16 bytes  | `'a1b2c3d4-e5f6-...'`                 | **Primary keys**                      |
| `JSONB`          | Variable  | `'{"key": "value"}'`                   | **Datos flexibles, configuraciones**  |
| `BYTEA`          | Variable  | `'\x89504e47...'`                      | Archivos binarios pequenos            |
| `INET`           | 7-19 bytes| `'192.168.1.1'`                        | IPs de clientes, auditing             |

---

## Guia de decision

```
¿Que tipo de dato debo usar?
│
├─ ¿Es un identificador unico?
│   ├─ Si, PK de tabla ──────────────────▶ UUID
│   ├─ Si, ID secuencial ────────────────▶ SERIAL / BIGSERIAL
│   └─ Si, codigo corto ────────────────▶ SMALLINT / INTEGER
│
├─ ¿Es texto?
│   ├─ Nombre, email, descripcion ────────▶ TEXT
│   ├─ ISO code fijo (ej: "US") ──────────▶ CHAR(2)
│   └─ Con limite estricto ───────────────▶ VARCHAR(n) o CHECK
│
├─ ¿Es un numero?
│   ├─ Dinero / precios ──────────────────▶ NUMERIC(p,s)
│   ├─ Entero ────────────────────────────▶ INTEGER / BIGINT
│   └─ Decimal aproximado ────────────────▶ REAL / DOUBLE PRECISION
│
├─ ¿Es una fecha?
│   ├─ Solo fecha ────────────────────────▶ DATE
│   ├─ Fecha + hora (con zona) ───────────▶ TIMESTAMPTZ
│   ├─ Solo hora ─────────────────────────▶ TIME
│   └─ Duracion ──────────────────────────▶ INTERVAL
│
├─ ¿Es true/false?
│   └─ Si ────────────────────────────────▶ BOOLEAN
│
├─ ¿Es JSON flexible?
│   ├─ Necesitas busqueda ────────────────▶ JSONB
│   └─ Solo guardar ──────────────────────▶ JSONB (mejor siempre)
│
├─ ¿Es una IP?
│   └─ Si ────────────────────────────────▶ INET
│
└─ ¿Es un archivo binario?
    ├─ Pequeno (< 1MB) ───────────────────▶ BYTEA
    └─ Grande (> 1MB) ────────────────────▶ Supabase Storage
```

---

## Fuentes

- [PostgreSQL 18 Documentation - Chapter 8: Data Types](https://www.postgresql.org/docs/18/datatype.html)
- [PostgreSQL Documentation - Numeric Types](https://www.postgresql.org/docs/18/datatype-numeric.html)
- [PostgreSQL Documentation - Date/Time Types](https://www.postgresql.org/docs/18/datetime-datatypes.html)
- [PostgreSQL Documentation - JSONB](https://www.postgresql.org/docs/18/datatype-json.html)

---

> **Siguiente archivo:** [03 - DDL: CREATE, ALTER, DROP](03-ddl-create-alter.md)
