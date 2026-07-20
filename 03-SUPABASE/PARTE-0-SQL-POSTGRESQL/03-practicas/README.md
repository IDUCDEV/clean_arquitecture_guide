# Submodulo 3: Practicas de SQL y PostgreSQL

> Pone en practica todo lo aprendido en los Submodulos 1 y 2 con ejercicios reales. Construiras esquemas completos, resolveras problemas de modelado y conectaras tu conocimiento SQL con Supabase.

```
┌──────────────────────────────────────────────────────────────┐
│                      SUBMODULO 3                             │
│                                                              │
│  Submodulo 1 (Fundamentos) ──┐                               │
│                               ├──▶ Submodulo 3 (Practicas)  │
│  Submodulo 2 (Postgres) ──────┘                               │
│                                                              │
│  Las practicas integran todo el conocimiento previo          │
│  y lo conectan con Supabase.                                 │
└──────────────────────────────────────────────────────────────┘
```

## Indice de contenidos

| #  | Archivo | Tema | Tiempo estimado |
|----|---------|------|-----------------|
| 01 | [01-practica-crud-completo.md](01-practica-crud-completo.md) | CRUD completo E-commerce (creacion, consultas, constraints) | 60 min |
| 02 | [02-practica-modelado-relacional.md](02-practica-modelado-relacional.md) | Modelado sistema de reservas (entidades, relaciones, normalizacion) | 60 min |
| 03 | [03-puente-supabase.md](03-puente-supabase.md) | Puente hacia Supabase (migrations, RLS, SQL Editor) | 30 min |

**Tiempo total estimado: ~2.5 horas**

## Lo que practicarás

- **Crear** un esquema de base de datos desde cero con SQL.
- **Escribir** consultas CRUD completas (INSERT, SELECT, UPDATE, DELETE).
- **Relacionar** tablas con JOINs y disenar llaves foraneas.
- **Agrupar, filtrar y ordenar** grandes conjuntos de datos.
- **Usar** funciones de ventana (RANK, ROW_NUMBER) para analisis avanzados.
- **Implementar** constraints, indices y llaves compuestas.
- **Modelar** sistemas del mundo real con diagramas entidad-relacion.
- **Normalizar** un esquema a 3FN (primera, segunda y tercera forma normal).
- **Conectar** tu conocimiento SQL con conceptos de Supabase (migrations, RLS, policies).
- **Leer** archivos de migracion y comprender el flujo de trabajo de Supabase.

## Prerequisitos

- Haber completado los **Submodulos 1 y 2**
   - Fundamentos de SQL (tipos, DDL, DML, JOINs, agregaciones)
   - PostgreSQL especifico (constraints, indices, funciones, triggers, JSONB)
- Tener acceso a un entorno SQL (Supabase SQL Editor, psql, etc.)

## Como usar este submodulo

1. **Haz las practicas en orden.** La practica 1 es la mas basica, la 2 es modelado, y la 3 es el puente conceptual.
2. **No leas las soluciones primero.** Intenta resolver los ejercicios por tu cuenta antes de mirar las respuestas.
3. **Escribe cada consulta tu mismo.** Copiar y pegar no sirve para aprender. Ejecuta el SQL en un editor real.
4. **Despues de la practica 3**, estas listo para la PARTE 1 de Supabase.

## Resultado esperado

Al completar este submodulo seras capaz de:

- Disenar y crear un esquema relacional complejo desde cero
- Escribir consultas SQL con joins, subconsultas, CTEs y funciones de ventana
- Normalizar un esquema hasta la tercera forma normal
- Leer un archivo de migracion de Supabase y entenderlo
- Conectar los conceptos SQL con RLS y policies de Supabase

---

> **Siguiente paso:** [Practica 1: CRUD Completo -- E-commerce](01-practica-crud-completo.md)
