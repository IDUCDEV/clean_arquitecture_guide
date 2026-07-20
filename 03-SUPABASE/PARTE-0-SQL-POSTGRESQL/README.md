# PARTE 0: SQL y PostgreSQL -- Fundamentos para Supabase

> Supabase usa PostgreSQL como motor de bases de datos. Este modulo te ensena SQL y PostgreSQL desde cero para que puedas aprovechar al maximo Supabase.

```
┌─────────────────────────────────────────────────────────────────────┐
│                          ARQUITECTURA                               │
│                                                                     │
│  ┌──────────┐       ┌──────────────┐       ┌──────────────┐        │
│  │  Flutter   │       │  Supabase    │       │  PostgreSQL  │        │
│  │  App       │──────▶│  SDK         │──────▶│  (Base de    │        │
│  │            │       │              │       │   Datos)      │        │
│  │  .from('X')│       │  Queries /   │       │              │        │
│  │  .select() │       │  Mutations   │       │  SQL Queries │        │
│  └────────────┘       └──────────────┘       └──────────────┘        │
│                                                                     │
│  Tu escribes:       La SDK traduce:        El RDBMS ejecuta:        │
│  await supabase     a una request HTTP     la consulta SQL real      │
│  .from('orders')    con tu query SQL        y devuelve resultados    │
│  .select('*')                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Por que existe esta Parte 0?

La PARTE 1 de este modulo (Desarrollo Local) asume que ya sabes SQL y como funciona PostgreSQL. Sin esa base, los conceptos de migraciones, RLS, funciones, triggers y esquemas te resultaran incomprensibles.

Esta Parte 0 llena ese vacio. Es un curso intensivo desde cero para que llegues a la PARTE 1 con los fundamentos claros.

## Contenido

| Submodulo | Archivos | Tiempo |
|-----------|----------|--------|
| **Submodulo 1** [Fundamentos SQL](01-fundamentos-sql/) | 8 archivos | 4-6 horas |
| **Submodulo 2** [Postgres Especifico](02-postgresql-especifico/) | 8 archivos | 4-6 horas |
| **Submodulo 3** [Practicas](03-practicas/) | 3 archivos | 2-3 horas |

## Fases de aprendizaje

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FASE 1: SQL Basics         FASE 2: PostgreSQL Features                │
│  ────────────────────        ──────────────────────                     │
│  Submodulo 1                 Submodulo 2                                │
│                                                                         │
│  Tipos de datos              Constraints (PK, FK, CHECK, UNIQUE)         │
│  DDL (CREATE TABLE, ALTER)  Indexes for performance                      │
│  DML (INSERT, SELECT)       Functions & triggers                         │
│  Queries (WHERE, ORDER BY)  JSONB & operators                            │
│  JOINs (INNER, LEFT, ..)    Full-text search                             │
│  Group By / Aggregations    RPC                                        │
│  Window functions                                                       │
│  CTEs                                                                   │
│                                                                         │
│  FASE 3: Practice                                                       │
│  ────────────────                                                        │
│  Submodulo 3                                                            │
│                                                                         │
│  CRUD completo (E-commerce)                                              │
│  Modelado relacional (Reservas)                                           │
│  Puente hacia Supabase (migrations, RLS, SQL Editor)                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Despues de este modulo

Una vez que completes estas 3 fases, estaras listo para abordar la PARTE 1: DESARROLLO LOCAL que cubre:

- Configuracion de Supabase local con Docker
- Creacion de migraciones y seeds
- Implementacion de RLS policies
- Edge Functions
- Integracion con Flutter

Dirigete a [PARTE 1: Desarrollo Local](../PARTE-1-DESARROLLO/) cuando hayas terminado.

## Prerequisitos

| Requisito        | Estado           |
|------------------|------------------|
| Conocimientos SQL previos | Ninguno |
| Flutter o backend  | No necesario |
| Navegador web   | Si (terminal tambien) |
| Ganas de aprender| Imprescindible |

## Herramientas que necesitas

| Herramienta | Uso | Gratuita? |
|-------------|-----|-----------|
| Supabase SQL Editor (via Dashboard) | Ejecutar consultas, ver resultados | Si (navegador) |
| psql (PostgreSQL client) | Alternativa en terminal | Si |
| Supabase CLI (opcional) | Migraciones y RLS | Si |

No es necesario que instales nada a nivel local. Puedes usar el SQL Editor de Supabase en tu navegador.

## Nivel

**Principiante absoluto** -- no se requieren conocimientos previos de SQL o bases de datos.

## Tiempo estimado total

| Submodulo | Tiempo |
|-----------|--------|
| Submodulo 1: Fundamentos SQL | 4 - 6 horas |
| Submodulo 2: Postgres Especifico | 4 - 6 horas |
| Submodulo 3: Practicas | 2 - 3 horas |
| **Total** | **10 - 14 horas** |

## Fuentes de referencia

- [PostgreSQL 18 Documentation](https://www.postgresql.org/docs/18/index.html)
- [W3Schools SQL Tutorial](https://www.w3schools.com/sql/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

## Flujo de navegacion

```
START: Submodulo 1 (Fundamentos SQL) → leer 01 a 08 en orden
           ↓
       Submodulo 2 (PostgreSQL) → leer 01 a 08 en orden
           ↓
       Submodulo 3 (Practicas) → 01, 02, 03 en orden
           ↓
       PARTE 1 (Desarrollo Local)
```

## Resumen

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  PARTE 0: SQL y PostgreSQL                                              │
│                                                                         │
│  ├── Submodulo 1: Fundamentos SQL       (4-6 h)                        │
│  │   Tipos de datos, DDL, DML, JOINs, Agregaciones, Window Functions   │
│  │                                                                     │
│  ├── Submodulo 2: PostgreSQL Especifico   (4-6 h)                      │
│  │   Constraints, Indexes, Functions, Triggers, JSONB, Full-text, RPC  │
│  │                                                                     │
│  └── Submodulo 3: Practicas             (2-3 h)                       │
│      CRUD E-commerce, Modelado Reservas, Puente Supabase              │
│                                                                         │
│  Siguiente: PARTE 1 -- Desarrollo Local con Supabase                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

> **Siguiente paso:** [Submodulo 1: Fundamentos de SQL](01-fundamentos-sql/README.md)
