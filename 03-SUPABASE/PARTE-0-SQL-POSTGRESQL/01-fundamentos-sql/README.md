# Submodulo 1: Fundamentos de SQL

> **SQL es el lenguaje universal de las bases de datos relacionales.** Antes de usar Supabase, necesitas dominar estos fundamentos.

```
┌─────────────────────────────────────────────────────────────┐
│                  FUNDAMENTOS DE SQL                         │
│                                                             │
│  Tu necesitas SQL → Supabase usa PostgreSQL                 │
│  PostgreSQL es un RDBMS → SQL es su lenguaje                │
│                                                             │
│  Aprende SQL primero → Luego Supabase sera facil            │
└─────────────────────────────────────────────────────────────┘
```

## Indice de contenidos

| #  | Archivo                                        | Tema                                        | Tiempo estimado |
|----|------------------------------------------------|---------------------------------------------|-----------------|
| 01 | [01-que-es-sql-rdbms.md](01-que-es-sql-rdbms.md)               | Que es SQL y que es un RDBMS                | 20 min          |
| 02 | [02-tipos-de-datos.md](02-tipos-de-datos.md)                   | Tipos de datos en PostgreSQL                | 30 min          |
| 03 | [03-ddl-create-alter.md](03-ddl-create-alter.md)               | DDL: CREATE, ALTER, DROP                    | 25 min          |
| 04 | [04-dml-select-insert-update-delete.md](04-dml-select-insert-update-delete.md) | DML: INSERT, SELECT, UPDATE, DELETE         | 30 min          |
| 05 | [05-where-orden-filtros.md](05-where-orden-filtros.md)         | WHERE, ORDER BY, LIMIT, filtros             | 25 min          |
| 06 | [06-join-relaciones.md](06-join-relaciones.md)                 | JOINs: INNER, LEFT, RIGHT, FULL, CROSS      | 35 min          |
| 07 | [07-agrupaciones-funciones.md](07-agrupaciones-funciones.md)   | GROUP BY, HAVING, funciones de agregacion   | 35 min          |
| 08 | [08-cheatsheet-sql.md](08-cheatsheet-sql.md)                   | Cheatsheet rapida de SQL                    | 10 min          |

**Tiempo total estimado: ~3.5 horas**

## Fases de aprendizaje

```
┌────────────────────────────────────────────────────────────────────────┐
│  FASE 1: BASE           FASE 2: ACCION          FASE 3: AVANZADO     │
│  ─────────────          ──────────────          ────────────────      │
│  Archivos 01-02         Archivos 03-05          Archivos 06-07        │
│                                                                     │
│  Que es SQL             Crear tablas            JOINs entre tablas    │
│  Tipos de datos         Consultar datos         Agrupaciones         │
│  Conceptos              Modificar datos         Funciones de ventana  │
│                                                                     │
│  Tiempo: ~50 min        Tiempo: ~80 min         Tiempo: ~70 min      │
└────────────────────────────────────────────────────────────────────────┘
```

## Lo que aprenderas

- **Que es SQL** y como se relaciona con PostgreSQL y Supabase
- **Tipos de datos** disponibles en PostgreSQL y cual elegir para cada caso
- **Crear y modificar** tablas con DDL (CREATE TABLE, ALTER TABLE)
- **Consultar, insertar, actualizar y eliminar** datos con DML
- **Filtrar y ordenar** resultados con WHERE, ORDER BY, LIMIT
- **Relacionar tablas** con los diferentes tipos de JOIN
- **Agrupar datos** con GROUP BY y usar funciones de agregacion
- **Referencia rapida** con un cheatsheet de SQL completo

## Prerequisitos

- Terminal o consola basica
- Un navegador web (para usar el SQL Editor de Supabase)
- Ganas de aprender

## Como usar estos archivos

1. **Lee en orden** (del 01 al 08). Cada archivo construye sobre el anterior.
2. **Ejecuta el codigo SQL** en el SQL Editor de Supabase o en `psql`.
3. **No te saltes el cheatsheet** (08). Usalo como referencia rapida despues de completar el modulo.

---

> **Siguiente paso**: [01 - Que es SQL y que es un RDBMS](01-que-es-sql-rdbms.md)
