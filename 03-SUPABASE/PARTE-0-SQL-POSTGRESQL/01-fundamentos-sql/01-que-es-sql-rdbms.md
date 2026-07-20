# 01 - Que es SQL y que es un RDBMS

> SQL (Structured Query Language) es el lenguaje estandar para interactuar con bases de datos relacionales. Aprenderlo es el paso fundamental antes de usar Supabase.

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESUMEN RAPIDO                                │
│                                                                 │
│  SQL   = Lenguaje para hablar con la base de datos              │
│  RDBMS = El software que almacena y ejecuta las consultas SQL   │
│  PostgreSQL = El RDBMS que usa Supabase                         │
└─────────────────────────────────────────────────────────────────┘
```

## Indice

1. [Que es SQL](#que-es-sql)
2. [Que es un RDBMS](#que-es-un-rdbms)
3. [Categorias de SQL](#categorias-de-sql)
4. [Como funciona una base de datos](#como-funciona-una-base-de-datos)
5. [SQL vs NoSQL](#sql-vs-nosql)
6. [Herramientas para ejecutar SQL](#herramientas-para-ejecutar-sql)

---

## Que es SQL

**SQL** significa **Structured Query Language** (Lenguaje de Consulta Estructurado). Es el lenguaje estandar para comunicarse con bases de datos relacionales.

**Datos clave:**

| Propiedad        | Valor                                                  |
|------------------|--------------------------------------------------------|
| Nombre completo  | Structured Query Language                              |
| Estandar         | ANSI/ISO (1986/1987)                                   |
| Primera version  | 1986 (SQL-86)                                          |
| Version actual   | SQL:2023                                               |
| Uso              | Leer, escribir, modificar y eliminar datos             |
| PostgreSQL       | Implementacion avanzada del estandar SQL               |

**Ejemplo basico:**

```sql
-- Consulta simple: obtener todos los usuarios
SELECT * FROM usuarios;

-- Consulta con filtro: obtener usuario por email
SELECT nombre, email FROM usuarios WHERE email = 'ana@email.com';

-- Insertar un nuevo usuario
INSERT INTO usuarios (nombre, email) VALUES ('Carlos', 'carlos@email.com');
```

> **Nota:** SQL no distingue entre mayusculas y minusculas en sus comandos (`SELECT` = `select`), pero es convencion escribir las palabras clave en **MAYUSCULAS**.

---

## Que es un RDBMS

Un **RDBMS** (Relational Database Management System) es el software que almacena, administra y ejecuta consultas SQL sobre bases de datos relacionales.

**Ejemplos de RDBMS:**

| RDBMS       | Tipo       | Usado por Supabase? | Licencia       |
|-------------|------------|----------------------|----------------|
| PostgreSQL  | Open Source | **Si**              | PostgreSQL/Liberal |
| MySQL       | Open Source | No                  | GPL            |
| SQLite      | Open Source | No                  | Public Domain  |
| Oracle DB   | Comercial  | No                  | Propietaria    |
| SQL Server  | Comercial  | No                  | Propietaria    |

### Conceptos fundamentales

```
┌──────────────────────────────────────────────────────────────┐
│                     BASE DE DATOS                            │
│                                                              │
│  ┌─────────────────────┐  ┌─────────────────────┐           │
│  │     SCHEMA          │  │     SCHEMA          │           │
│  │   "public"          │  │   "auth"            │           │
│  │                     │  │                     │           │
│  │  ┌───────────────┐  │  │  ┌───────────────┐  │           │
│  │  │   TABLA       │  │  │  │   TABLA       │  │           │
│  │  │  usuarios     │  │  │  │  users        │  │           │
│  │  │               │  │  │  │               │  │           │
│  │  │ id │ nombre   │  │  │  │ id │ email    │  │           │
│  │  │────┼──────────│  │  │  │────┼──────────│  │           │
│  │  │ 1  │ Ana      │  │  │  │ 1  │ a@b.com  │  │           │
│  │  │ 2  │ Carlos   │  │  │  │ 2  │ c@d.com  │  │           │
│  │  └───────────────┘  │  │  └───────────────┘  │           │
│  └─────────────────────┘  └─────────────────────┘           │
└──────────────────────────────────────────────────────────────┘
```

**Terminos clave:**

| Termino     | Definicion                                                       |
|-------------|------------------------------------------------------------------|
| **Base de datos**   | Contenedor principal de todas las tablas y datos            |
| **Schema**          | Organizador dentro de la base de datos (por defecto: `public`) |
| **Tabla**           | Estructura que almacena datos en filas (rows) y columnas (columns) |
| **Fila (Row)**      | Un registro individual en la tabla (tambien llamado "tupla")    |
| **Columna (Column)**| Un campo o atributo de la tabla (tambien llamado "atributo")    |
| **Primary Key**     | Columna unica que identifica cada fila                         |
| **Foreign Key**     | Columna que referencia a otra tabla                            |

---

## Categorias de SQL

SQL se divide en **4 categorias** principales:

```
┌──────────────────────────────────────────────────────────────────────┐
│                     CATEGORIAS DE SQL                                │
│                                                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                │
│  │   DDL   │  │   DML   │  │   DCL   │  │   TCL   │                │
│  │         │  │         │  │         │  │         │                │
│  │ Definir │  │ Datos   │  │ Control │  │ Transac.│                │
│  │ datos   │  │         │  │ acceso  │  │         │                │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘                │
└──────────────────────────────────────────────────────────────────────┘
```

### DDL - Data Definition Language

Define y modifica la **estructura** de la base de datos.

| Comando     | Funcion                              | Ejemplo                              |
|-------------|--------------------------------------|--------------------------------------|
| `CREATE`    | Crear objetos (tablas, databases)    | `CREATE TABLE usuarios (id INT);`    |
| `ALTER`     | Modificar estructura existente       | `ALTER TABLE usuarios ADD COLUMN email TEXT;` |
| `DROP`      | Eliminar objetos                     | `DROP TABLE usuarios;`               |
| `TRUNCATE`  | Eliminar todos los registros (rapido)| `TRUNCATE TABLE usuarios;`           |
| `RENAME`    | Renombrar objetos                    | `ALTER TABLE usuarios RENAME TO clientes;` |
| `COMMENT`   | Agregar comentarios a objetos        | `COMMENT ON TABLE usuarios IS 'Tabla de usuarios del sistema';` |

### DML - Data Manipulation Language

Manipula los **datos** dentro de las tablas.

| Comando   | Funcion                     | Ejemplo                                    |
|-----------|-----------------------------|--------------------------------------------|
| `SELECT`  | Consultar datos             | `SELECT * FROM usuarios WHERE id = 1;`     |
| `INSERT`  | Insertar nuevos registros   | `INSERT INTO usuarios (nombre) VALUES ('Ana');` |
| `UPDATE`  | Modificar registros         | `UPDATE usuarios SET nombre = 'Ana M.' WHERE id = 1;` |
| `DELETE`  | Eliminar registros          | `DELETE FROM usuarios WHERE id = 1;`       |

### DCL - Data Control Language

Controla el **acceso** y permisos a los datos.

| Comando    | Funcion                       | Ejemplo                                         |
|------------|-------------------------------|--------------------------------------------------|
| `GRANT`    | Conceder permisos             | `GRANT SELECT ON usuarios TO usuario_anon;`      |
| `REVOKE`   | Revocar permisos              | `REVOKE DELETE ON usuarios FROM usuario_anon;`   |

### TCL - Transaction Control Language

Gestiona **transacciones** (operaciones atomicas).

| Comando     | Funcion                                | Ejemplo                  |
|-------------|----------------------------------------|--------------------------|
| `BEGIN`     | Iniciar una transaccion                | `BEGIN;`                 |
| `COMMIT`    | Confirmar todos los cambios            | `COMMIT;`                |
| `ROLLBACK`  | Revertir todos los cambios             | `ROLLBACK;`              |
| `SAVEPOINT` | Crear un punto de restauracion         | `SAVEPOINT mi_punto;`    |

**Ejemplo de transaccion:**

```sql
BEGIN;
  UPDATE cuentas SET saldo = saldo - 100 WHERE id = 1;
  UPDATE cuentas SET saldo = saldo + 100 WHERE id = 2;
COMMIT;
-- Si algo falla: ROLLBACK;
```

---

## Como funciona una base de datos

```
┌──────────┐       ┌──────────┐       ┌──────────┐       ┌──────────┐
│          │       │          │       │          │       │          │
│  TU APLI │──────▶│   SQL    │──────▶│  RDBMS   │──────▶│ DISCO    │
│  CACION  │       │  QUERY   │       │ POSTGRES │       │ DURO     │
│          │       │          │       │          │       │          │
└──────────┘       └──────────┘       └──────────┘       └──────────┘
   Flutter           Texto SQL          Motor              Archivos
   / App             SELECT *           que ejecuta         donde se
                     FROM tabla         las consultas       guardan
                                        y gestiona         los datos
                                        los datos

Ejemplo concreto en Supabase:
┌──────────┐       ┌──────────────────┐       ┌──────────────┐
│          │       │                  │       │              │
│  Flutter │──────▶│  Supabase Client │──────▶│  PostgreSQL  │
│   App    │       │                  │       │  (tu DB)     │
│          │       │  .from('users')  │       │              │
│          │       │  .select('*')    │       │  SELECT *    │
│          │       │                  │       │  FROM users; │
└──────────┘       └──────────────────┘       └──────────────┘
```

**Flujo de una consulta:**

1. **Tu aplicacion** envia una consulta SQL al RDBMS
2. **El RDBMS** analiza y optimiza la consulta
3. **El motor de ejecucion** procesa la consulta
4. **El gestor de almacenamiento** lee/escribe datos en disco
5. **Los resultados** se devuelven a tu aplicacion

---

## SQL vs NoSQL

| Caracteristica    | SQL (PostgreSQL)                    | NoSQL (MongoDB, etc.)                 |
|-------------------|-------------------------------------|---------------------------------------|
| **Estructura**    | Tablas con filas y columnas fijas   | Documentos JSON flexibles             |
| **Esquema**       | Rigido (schema definido)            | Flexible (schema dinamico)            |
| **Relaciones**    | JOINs entre tablas                  | Anidamiento o referencias             |
| **ACID**          | Si (Atomicidad, Consistencia)       | No siempre (BASE, eventual)           |
| **Lenguaje**      | SQL (estandar ANSI)                 | Varias APIs proprietary               |
| **Escalabilidad** | Vertical (mas RAM/CPU)              | Horizontal (mas nodos)                |
| **Consistencia**  | Fuerte (siempre correcto)           | Eventual (puede tener datos viejos)   |
| **Ideal para**    | Datos relacionados, transacciones  | Datos flexibles, escalabilidad masiva |
| **Supabase**      | **PostgreSQL** (si aplica)          | No aplica                             |

**Cuando elegir SQL:**

- Tu datos tienen **relaciones** (usuarios tienen pedidos, pedidos tienen productos)
- Necesitas **integridad referencial** (no puedes tener pedidos de usuarios inexistentes)
- Requieres **transacciones** ACID (transferencias bancarias, pagos)
- Quieres un lenguaje **estandar** y ampliamente conocido

**Ejemplo de relacion en SQL:**

```sql
-- Un usuario tiene muchos pedidos
-- Un pedido pertenece a un usuario

SELECT u.nombre, p.total
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id
WHERE u.id = 1;
```

---

## Herramientas para ejecutar SQL

| Herramienta                | Tipo              | Ventaja                                    | Desventaja                     |
|----------------------------|-------------------|--------------------------------------------|--------------------------------|
| **Supabase SQL Editor**    | Web (Dashboard)   | Integrado, visual, historial de consultas  | Depende de internet            |
| **psql**                   | Terminal (CLI)    | Rapido, scripteable, potente               | Sin interfaz grafica           |
| **pgAdmin**                | Desktop (GUI)     | Visual completo, inspeccion de esquemas    | Peso, requiere instalacion     |
| **DBeaver**                | Desktop (GUI)     | Multi-DB, gratuito, profesional            | Complejo para empezar          |
| **DataGrip**               | Desktop (GUI)     | IDE potente, autocomplete avanzado         | De pago (licencia)             |

### Ejecutar SQL en el Supabase Dashboard

1. Ve a tu proyecto en [supabase.com](https://supabase.com)
2. En el menu lateral, selecciona **SQL Editor**
3. Escribe tu consulta SQL
4. Haz clic en **Run** (o presiona `Ctrl + Enter`)

### Ejecutar SQL con psql (terminal)

```bash
# Conectar a tu base de datos de Supabase
psql "postgresql://postgres:[TU_PASSWORD]@db.[TU_PROJECT_REF].supabase.co:5432/postgres"

# Ejecutar un archivo SQL
psql -f mi_consulta.sql

# Ejecutar un comando SQL directo
psql -c "SELECT * FROM usuarios LIMIT 10;"
```

---

## Resumen

```
┌──────────────────────────────────────────────────────────────────────┐
│  SQL  → Lenguaje estandar para bases de datos relacionales          │
│  RDBMS → Software que ejecuta SQL y almacena datos (PostgreSQL)     │
│  4 categorias → DDL (estructura), DML (datos), DCL (permisos),     │
│                  TCL (transacciones)                                 │
│  PostgreSQL → El RDBMS que usa Supabase                             │
│  SQL Editor → Herramienta web en Supabase para ejecutar consultas   │
└──────────────────────────────────────────────────────────────────────┘
```

## Fuentes

- [PostgreSQL 18 Documentation - Chapter 1: Introduction](https://www.postgresql.org/docs/18/tutorial-intro.html)
- [W3Schools - SQL Introduction](https://www.w3schools.com/sql/sql_intro.asp)
- [PostgreSQL Documentation - SQL Syntax](https://www.postgresql.org/docs/18/sql-syntax-lexical.html)

---

> **Siguiente archivo:** [02 - Tipos de datos](02-tipos-de-datos.md)
