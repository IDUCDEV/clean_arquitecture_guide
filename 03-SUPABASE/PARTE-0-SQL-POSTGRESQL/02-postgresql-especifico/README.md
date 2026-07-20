# Submodulo 2: PostgreSQL Especifico

> **PostgreSQL es el motor de bases de datos detras de Supabase.** Estos son los conceptos que van mas alla del SQL estandar.

---

## Por que este submodulo importa

Supabase no usa SQL generico: usa **PostgreSQL**. Esto significa que tienes acceso a funcionalidades que no existen en otros motores de BD. Dominarlas es la diferencia entre un proyecto basico y uno profesional.

---

## Contenido

| # | Archivo | Tema | Tiempo estimado |
|---|---------|------|-----------------|
| 1 | `01-postgresql-vs-sql-estandar.md` | Que agrega PostgreSQL al SQL estandar | 25 min |
| 2 | `02-constraints-restricciones.md` | Restricciones: NOT NULL a EXCLUDE | 40 min |
| 3 | `03-indexes-rendimiento.md` | Indexes y optimizacion de consultas | 40 min |
| 4 | `04-plpgsql-funciones.md` | PL/pgSQL: lenguaje procedural | 45 min |
| 5 | `05-triggers-automatizacion.md` | Triggers: automatizacion en la BD | 35 min |
| 6 | `06-jsonb-busqueda-texto.md` | JSONB y busqueda de texto full-text | 35 min |
| 7 | `07-rpc-para-supabase.md` | RPC: funciones PostgreSQL desde Flutter | 45 min |
| 8 | `08-cheatsheet-postgresql.md` | Referencia rapida y templates | 20 min |

**Tiempo total estimado: ~4 horas**

---

## Prerequisitos

- Haber completado el **Submodulo 1 (Fundamentos SQL)**
- Conocimientos basicos de SELECT, INSERT, UPDATE, DELETE
- Supabase CLI configurado (opcional pero recomendado)

---

## Fases de aprendizaje

```
┌─────────────────────────────────────────────────────┐
│  FASE 1: Fundamentos PostgreSQL                     │
│  Archivos 01-02                                     │
│  -> Que es diferente y como restringir datos        │
├─────────────────────────────────────────────────────┤
│  FASE 2: Rendimiento y Logica                       │
│  Archivos 03-05                                     │
│  -> Indexes, funciones y triggers                   │
├─────────────────────────────────────────────────────┤
│  FASE 3: Datos Avanzados y Supabase                 │
│  Archivos 06-07                                     │
│  -> JSONB, full-text search y RPC                   │
├─────────────────────────────────────────────────────┤
│  FASE 4: Referencia                                 │
│  Archivo 08                                         │
│  -> Cheatsheet para consulta rapida                 │
└─────────────────────────────────────────────────────┘
```

---

## Recursos oficiales

- [PostgreSQL 18 Documentation](https://www.postgresql.org/docs/18/)
- [Supabase SQL Reference](https://supabase.com/docs/guides/database)
- [Supabase RPC](https://supabase.com/docs/guides/database/calling-postgres-stored-procedures)
