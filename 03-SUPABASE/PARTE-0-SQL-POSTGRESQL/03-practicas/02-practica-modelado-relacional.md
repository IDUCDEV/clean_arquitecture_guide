# Practica 2: Modelado Relacional -- Sistema de Reservas

> Vamos a modelar un sistema de reservas para una estetica/beauty salon. Utilizaras el mismo caso de negocio del Modulo 02 (Diseno de feature) pero desde la perspectiva de base de datos: entidades, relaciones, normalizacion y SQL puro.

Objetivo: Pasar del analisis en lenguaje natural a un esquema SQL normalizado y listo para produccion.

```
+--------------------------------------------------------------------------+
|              SISTEMA DE RESERVAS - BEAUTY SALON                           |
|                                                                           |
|  +========+    +============+    +=============+    +===========+        |
|  |  client  |    |  reservation |    |  payment    |    | review   |        |
|  |  (PK)   |--->| client_id    |--->| reserv_id   |    | (PK)     |
|  |  name   | |  | id(PK)      | |  | id(PK)      |    | reservation_id
|  |  email   | |  | stylist_id | |  | amount      |    | rating   |
|  +========+ |  | date         | |  | method      |    | comment  |
|             |  | time         | |  | status      |    | date     |
|             |  | status       | |  | date        |    +=========+
|             |  | total        | |  +===========+
|             |  | notes        | |
|             |  +============+  |         +=========+
|             |                  |         | stylist_services | (M: M)
|             |                  |----->| service_id (FK)    |
|             |                  +----->| stylist_id (FK)     |
|             |                  |       | price_surcharge   |
|             |                  |       +=========+
|  +========+                     |
|  | service |                     |
|  | id(PK) |<--------------------+
|  | name   |                     |
|  | desc   |                     |
|  | price  |                     |
|  | duration |                     |
|  +========+                     |
|  +========+                     |
|  | stylist |                     |
|  | id(PK) |<--------------------+
|  | name   |                     |
|  | email  |                     |
|  | speciality |                  |
|  +=========+                     |
+--------------------------------------------------------------------------+
## Step 1: Entities

Partiendo de la descripcion del sistema:

- **client**: persona que realiza la reserva, tiene datos personales y de contacto.
- **service**: servicio ofrecido (Corte de cabello, Manicura, Pedicura, etc.) con precio y duracin.
- **stylist**: el profesional que realiza el servicio, con su especialidad.
- **reservation**: es el cor del modelo, une client, stylist y services. contiene la fecha, hora, estado, total.
- **payment**: registro de pago asociado a una reserva (pueden ser multiples pagos sorpresa).

| Entity | Description | Identified by |
|------|-------------|---------------|
| client | persona que solicita el servicio | ID del cliente |
| service | tipo de atelier ofrecido | ID del servicio |
| stylist | el profesional encargado | ID del estilista |
| reservation | la cita o reservacion | ID de la reserva |
| payment | Informacion del pago | ID del paso |
| reservation_service | union de reserva y servicio (N:M) | composite |

## Step 2: Relaciones

Analizamos las relaciones entre entidades:

| Entidad A | Relacion | Entidad B | Cardinalidad | Explicacion |
|-----------|----------|-----------|--------------|-------------|
| client | tiene | reservation | 1:N | Un cliente puede tener muchas reservas |
| reservation | es pagada por | payment | N:N? | Una reserva puede tener un pago, pero un pago cubre una reserva (1:N) |
| reservation | contiene | reservation_service | 1:N | Una reserva contiene una linea de reserva |
| reservation_service | es sobre | service | N:1 | Una linea refiere a un servicio |
| reservation_service | asignada a | stylist | N:1 | Una linea es atendida por un estilista |

## Step 3: Crear tablas con constraints

### 3.1 clients

```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    auth_user_id UUID,              -- Para Supabase, se rellena mas tarde
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),
    birth_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

Por qué auth_user_id está aquí: cuando conectes Supabase, guardarás la referencia al usuario autenticado (auth.users) en esta columna. Lo veremos en Step 7.

### 3.2 services

```sql
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price NUMERIC(10) NOT NULL CHECK (price > 0),
    duration INTERVAL NOT NULL,  -- duración estimada, e.g. "45 minutes"
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

duration es un tipo INTERVAL de PostgreSQL que puede almacenar inamente una longitud de tiempo. value de ejemplo: INTERVAL '45 minutes'.

### 3.3 stylists

```sql
CREATE TABLE stylists (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    specialty VARCHAR(200),   -- e.g., "colorista", "corte"
    bio TEXT,
    start_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

### 3.4 stylist_services (junction many-to-many)

Un estilista puede ofrecer muchos servicios, y un servicio puede ser ofrecido por muchos estilistas.

```sql
CREATE TABLE stylist_services (
    stylist_id INTEGER REFERENCES stylists(id) ON DELETE CASCADE,
    service_id INTEGER REFERENCES services(id) ON DELETE CASCADE,
    price_surcharge NUMERIC(10) DEFAULT 0 CHECK (price_surcharge >= 0),
    estimated_duration INTERVAL,
    PRIMARY KEY (stylist_price, service_id)  -- llave compuesta natural
);
```

llave primaria compuesta: (stylist_id, service_id). Esto significa que un estilista solo puede ofrecer cada servicio una vez.

### 3.5 reservations

Esta tabla es el core. Relaciona clientes, servicios y barberos.

```sql
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id) ON DELETE RESTRICT,
    reservation_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    notes TEXT,
    total_amount NUMERIC(10) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

| Columna | Values | Significado |
|---------|--------|-------------|
| status | pending, confirmed, completed, cancelled | Estado del flujo |
| start_time | e.g. "14:30" | Hora de inicio |
| end_time | e.g., "15:30" | Hora de fin|
| total_amount | e.g., 150.00 |  Total de la reserva (actualizado via trigger/backend) |

### 3.6 reservation_services

Detalle de servicios por reserva. Una reserva puede incluir varios servicios realizados por diferentes barberos.

```sql
CREATE TABLE reservation_services (
    id SERIAL PRIMARY KEY,
    reservation_id INTEGER NOT NULL REFERENCES reservations(id) ON DELETE CASCADE,
    service_id INTEGER NOT NULL REFERENCES services(id) ON DELETE RESTRICT,
    stylist_id INTEGER NOT NULL REFERENCES stylists(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price NUMERIC(10) NOT NULL,
    total_line NUMERIC(10) GENERATED ALWAYS AS (unit_price * quantity) STORED,
    CONSTRAINT unique_reservation_service UNIQUE (reservation_id, service_id)
);
```

Por qué ON DELETE CASCADE en reservation_id: si se borra la reserva, todos sus items deben borrarse (no tienen sentido por separado). En cambio, service_id y stylist_id tienen ON DELETE RESTRICT: no puedes borrar un servicio si alguien lo tiene en una reserva.

### 3.7 payments

```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    reservation_id INTEGER NOT NULL REFERENCES reservations(id) ON DELETE RESTRICT,
    amount NUMERIC(10) NOT NULL CHECK (amount > 0),
    payment_method VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    evidence_url TEXT,
    paid_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

payment_method ejemplos: credit_card, debit_ard, cash, transfer.

payment_status: pending, completed, refund, failed.

### 3.8 reviews (post-service)

Permite calificar la experiencia. seed data de revisión después de que se completa la reserva.

```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    reservation_id INTEGER REFERENCES reservations(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

## Step 4: Normalizacion (Formas Normales)

Vamos a evaluar nuestro diseo y aplicar las formas normales.

### 4.1 Primera Forma Normal (1NF)

Definicion: Cada celda contiene un unico valor (escalar), no listas ni arregs.

Problema potencial a la 1NF (no en nuestro esquema pero ilustrativo):  
Suponte que en clients tuvieras una columna `phone_numbers TEXT` que contuviera "123, 456, 789". Esto violaria la 1NF.

Correcto para la 1NF: clients.phone contiene un solo nmero. si hay ms de uno, se crea una tabla hija aparte.

Nuestro esquema cumple la 1NF (todas las celdas son escalares).

### 4.2 Segunda Forma Normal (2NF)

Definicion: Estar en 1NF . cada columna no clave de la tabla debe depender de la totalidad de la clave primaria.

aplicación: en la junction table stylist_services, la clave es compuesta (stylist_prima, service_id). price_surcharge depende de la combinacin del estilista y el servicio (OK). si price_surcharge dependiera nicamente del servicio, tendramos redundancia.

Nuestro esquema cumple la 2NF.

### 4.3 Tercera Forma Normal (3NF)

Definicion: Estar en 2NF. No debe existir dependencia transitiva entre las columnas no clave.

Ejemplo de violacin en supuestas: si en la tabla reservation, includiramos el nombre del cliente repetido (full_name) en vez de slo client_id. full_name se repite a travs del client_id, lo que provoca una dependencia transitiva (full_name est fuera de client_id). 
Siempre mantener los detalles del cliente en la tabla client y usar FK.

Nuestro esquema cumple la 3NF.

### 4.4 Ejemplo visual de desnormalizacion

No siguas este ejemplo, es lo que hay que evitar:

```
reservations_desnormalizada:
| client_name | client_email | service_name | stylist_name | reservation_date | price |
|-------------|--------------|--------------|--------------|------------------|-------|
| Ana Garcia  | ana@email   | Corte |Paula        | 2026-07-20| 45   |
| Ana Garcia  | ana@email   | Manicura |Paola      | 2026-07-20| 35   |
| Ana Garcia  | ana@email   | barber_shave |Paula   | 2026-07-21| 50   |

Problemas:
- El nombre y email de Ana estn repetidos 3 veces (redundancia)
- Si Ana cambi de email, hay que modificar 3 filas (infra a la 2NF)
- Si la direccion Paula cambi de nombre, hay que modificar 2 filas
- Waste de espacio y riesgo de incoherencia
- Cumple POS 1NF pero est en PESIMA 2NF y 3NF
```

## Step 5: ER Diagram (ASCII)

```
+---------------------+         +--------------------+       +---------------------+
|       clients       |         |      services      |       |      stylists       |
|--------------------|         |--------------------|       |---------------------|
| id (PK)             |         | id (PK)            |       | id (PK)             |
| full_name            |         | name                |       | full_name            |
| email                |         | price               |       | email                |
| phone                |         | availability        |       | phone                |
| auth_user_id        |         | active              |       | specialty            |
|==============|         |--------------------|       | start_date          |
|__|            |                                   | active              |
|  |            |  +-----------------------+         | is_active           |     
|  |            +->| stylist_services       |<-------+==================+
|  |            |  |=======================|         |   
|  |            |  | stylist_id (FK)        |         +========+
|  v             |  | service_id (FK)        |         =st|-reservations- services
|  +==========+  |  | price_surcharge        |          |   |
|  | reservations|  | duration              |          v   |       
|================|  +-----------------------+       +======+=======+
| id (PK)             |  |          | reservation_services |
| client_id (FK)------->|          |=======================|
| reservation_date    |  |          | reservation_id (FK) |
| start_time          |  |          | service_id (FK)     |
| end_time            |  |          | stylists_id (FK)    |
| status              |  |          | quantity             |
| total               |  |          | unit_price          |
| notes               |  |          | total_line           |
|================|  |          +======================-+
|__|                 |                            |
|  |                 |                            |  
|  v                 |                            v
|  +========+        |                     +========+
|  | payments |        |                     | reviews   | 
|  | id (PK)  |        |                     | id(PK)   |
|  |            |        |                     | reservation_id |
|  | reservation_id |  ----->+                  | rating      |
|  | (+)          |        |                     | commentary   |
|  | payment_method |        |                     | created_at  |
|  | status        |        |                     +========+
|  | amount        |        |
|  | paid_at        |        |
|  +========+        |
+-------------------+
> (see Step 5 as an ER ASCII diagram above)

## Step 6: Common queries

### 6.1. Obtener todas las reservas para una fecha específica

```sql
SELECT r.id, c.full_name AS cliente, r.start_time, r.end_time, r.status
FROM reservations r
INNER JOIN clients c ON r.client_id = c.id
WHERE r.reservation_date = '2026-07-21'
ORDER BY r.start_time;
```

| id | cliente | start_time | end_time | status |
|----|---------|------------|----------|--------|
| 1 | Ana Garcia | 09:00 | 09:45 | confirmed |
| 3 | Maria Lopez | 11:00 | 11:30 | pending |

### 6.2. Obtener disponibilidad de estilistas

Problema: Quieres saber si un estilista est disponible en un da y horario determinados.

```sql
SELECT
    s.full_name AS estilista,
    r.id AS reserva_id
FROM stylists s
LEFT JOIN reservations r ON r.id IN (
    SELECT reservation_id
    FROM reservation_services rs
    INNER JOIN reservations res ON rs.reservation_id = res.id
    WHERE rs.stylist_id = s.id
    AND res.reservation_date = '2026-07-21'
    AND res.status NOT IN ('cancelled', 'completed')
    AND res.start_time < TIME '11:30'
    AND res.end_time > TIME '10:00'
)
WHERE s.is_active = TRUE AND s.id = 1;
```

Este query verifica si hay reservas superpuestas. Si LEFT JOIN devuelve NULL, el estilist est libre.

### 6.3. Ingresos por servicio

Problema: Quieres saber cul servicio gener ms ingresos.

```sql
SELECT
    sv.name AS servicio,
    COUNT(rs.id) AS veces_realizado,
    SUM(rs.total_line) AS ingresos_totales
FROM reservation_services rs
INNER JOIN services sv ON rs.service_id = sv.id
INNER JOIN reservations r ON rs.reservation_id = r.id
WHERE r.status = 'completed'
GROUP BY sv.name
ORDER BY ingresos_totales DESC;
```

| servicio | veces_realizado | ingresos_totales |
|----------|-------|------------------|
| Corte Cabello | 8 | 480 |
| Manicura | 5 | 300 |
| Barber Shave | 3 | 135 |

### 6.4. Historial de un cliente

Problema: Ver todas las reservas de un cliente con sus servicios.

```sql
SELECT
    r.id AS reserva,
    r.reservation_date,
    r.total_amount,
    r.status,
    string_agg(sv.name, ', ' ORDER BY sv.name) AS servicios -- aggregate services
FROM reservations r
INNER JOIN reservation_services rs ON r.id = reservation_id
INNER JOIN services sv ON rs.service_id = sv.id
WHERE r.client_id = 1
GROUP BY r.id
ORDER BY r.reservation_date DESC;
```

| reserva | reservation_date | total_amount | servicios |
|---------|-----------------|--------------|-----------|
| 3       | 2026-07-21      | 80 | Corte Cabello, Manicura |
| 1       | 2026-06-15      | 50 | Corte Cabello |

string_agg es una funcin PostgreSQL que concatena los valores de una columna en un string con separador.


## Step 7: un listado con RLS-ready

RLS significa Row-Level Safety y es el modelo de seguridad de Supabase. Para que nuestras tablas sean compatibles con RLS, necesitamos:

1. Una referencia al usuario autenticado.
2. Polticas que restrinjan el acceso a las filas basadas en esta referencia.

### Agregar auth_user_id a clients

Ya tenemos una columna auth_user_id UUID en clients:

```sql
ALTER TABLE clients ADD COLUMN auth_user_id UUID;
CREATE INDEX idx_clients_auth_user ON clients(auth_user_id);

COMMENT ON COLUMN clients.auth_user_id IS 'Reference to auth.users in Supabase';
```

### Previsualización RLS

```
+------------------------------------------------------------+
|  RLS en accin:                                              |
|                                                              |
|  Usuario en Flutter accede a las reservas:                    |
|  supabase.auth.user() -> user_id                              |
|                                                              |
|  Flutter hace:                                               |
|  supabase.from('reservations').select('*')                   |
|                                                              |
|  PostgreSQL verifica la RLS policy:                          |
|  client_id IN (SELECT id FROM clients WHERE auth_user_id =   |
|    current_setting('app.user_id') ?? el ID del usuario)   |
+------------------------------------------------------------+
|
|  Sin RLS: Flutter podria ver TODAS las reservas de todos.
|  Con RLS: Flutter solo ve las reservas que le corresponden.
+------------------------------------------------------------+
```

El RLS es un tema extenso. Cubriremos su implementacin completa en la PARTE 1.


## Step 8: Comparacin con el modelo de entidad modulo 02

El Modulo 02 (Dise de feature) define un modelo conceptual. Lo sencillo que modelamos ac es la realizacin SQL de ese mismo concepto.

| Modulo 02 (conceptual) | Modulo 03-Parte 0 (SQL) |
|------------------------|------------------------|
| Entidad Cliente | Tabla clients |
| Entidad Servicio | Tabla services |
| Entidad Estilista | Tabla stylists |
| Entidad Reserva | Tabla reservations (core) |
| Entidad Pago | Tabla payments |
| Relacin M:N Servicios-Estilistas | Junction table stylist_services |
| Atributo multivaluado | Se resuelve con tablas hijas |
| cardinalidad N:M | Tablas de interseccin (junctions) |

```
Modulo 02 (General)                  Modulo 03 (Implementation de BD)
+------------------------+            +-------------------------+
|   Diagrama ER conceptual   |            |   Esquema SQL real      |
|   Entidad: cliente     |            |   CREATE TABLE client    |
|   Atributos: nombre, email|            |   full_name, email     |
|   Relacon: 1:N con reservas |            |   one-to-many reservations |
+------------------------+            +-------------------------+
```



## Resumen

```
+------------------------------------------------------------------------+
|                           RESUMEN DE PRACTICA                           |
|                                                                          |
|  Step 1: 6 entidades identificadas                                       |
|  Step 2: Anlisi de relaciones, siempre product; todav a conjuntos N:M   |
|  Step 3: Creación de tabla con tipos apropiados                         |
|  Step 4: Normalizacin; este quema ya cumple 3NF                         |
|  Step 5: Diagram ER ASCII                                                |
|  Step 6: Consultas comunes (disponibilidad, ingresos, hist client)    |
|  Step 7: Preparacin para RLS (auth_user_id columna)                     |
|  Step 8: Puente con el modelo de entidad Modulo 02                      |
|                                                                          |
|  Tiempo total: ~60 min                                                   |
|                                                                          |
|  Siguiente paso: Practica 3 - Puente hacia Supabase                     |
+------------------------------------------------------------------------+
|
> **Siguiente paso:** [Practica 3: Puente hacia Supabase](03-puente-supabase.md)
