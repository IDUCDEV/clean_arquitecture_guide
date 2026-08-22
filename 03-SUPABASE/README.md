# 03 - Supabase

> Aprende a configurar Supabase, auto-hospedarlo y automatizar tu flujo de desarrollo Flutter.

---

## 📋 Índice

### PARTE 0: SQL Y POSTGRESQL (Prerequisito)

| Submodulo | Archivos | Descripcion | Tiempo |
|-----------|----------|-------------|--------|
| [01-fundamentos-sql](./PARTE-0-SQL-POSTGRESQL/01-fundamentos-sql/) | 8 archivos | SQL desde cero: tipos, DDL, DML, joins, agregaciones | 4-6h |
| [02-postgresql-especifico](./PARTE-0-SQL-POSTGRESQL/02-postgresql-especifico/) | 8 archivos | Constraints, indexes, PL/pgSQL, triggers, JSONB, RPC | 4-6h |
| [03-practicas](./PARTE-0-SQL-POSTGRESQL/03-practicas/) | 3 archivos | CRUD completo, modelado relacional, puente a Supabase | 2-3h |

> **Nivel:** Principiante | **Tiempo total:** 10-14h

### PARTE 1: DESARROLLO LOCAL

| Archivo | Descripción |
|---------|-------------|
| [01-configuracion-inicial.md](./PARTE-1-DESARROLLO/01-configuracion-inicial.md) | Docker, Supabase CLI, inicialización |
| [02-estructura-proyecto-supabase.md](./PARTE-1-DESARROLLO/02-estructura-proyecto-supabase.md) | Archivos y carpetas |
| [03-makefile-integrado.md](./PARTE-1-DESARROLLO/03-makefile-integrado.md) | Makefile completo |
| [04-variables-entorno.md](./PARTE-1-DESARROLLO/04-variables-entorno.md) | Gestión .env |
| [05-migraciones-y-seeds.md](./PARTE-1-DESARROLLO/05-migraciones-y-seeds.md) | Migraciones de BD |
| [06-integracion-flutter.md](./PARTE-1-DESARROLLO/06-integracion-flutter.md) | Supabase en Flutter |
| [07-testing-local-supabase.md](./PARTE-1-DESARROLLO/07-testing-local-supabase.md) | Tests con pgTAP |

### PARTE 2: PRODUCCIÓN

| Archivo | Descripción |
|---------|-------------|
| [01-opciones-hosting.md](./PARTE-2-PRODUCTION/01-opciones-hosting.md) | Comparativa VPS |
| [02-supabase-self-hosted-docker.md](./PARTE-2-PRODUCTION/02-supabase-self-hosted-docker.md) | Docker deployment |
| [03-configuracion-produccion.md](./PARTE-2-PRODUCTION/03-configuracion-produccion.md) | Producción y seguridad |
| [04-migracion-local-a-produccion.md](./PARTE-2-PRODUCTION/04-migracion-local-a-produccion.md) | Schema migration |
| [05-backup-y-mantenimiento.md](./PARTE-2-PRODUCTION/05-backup-y-mantenimiento.md) | Backups, updates |
| [06-alternativas-externas.md](./PARTE-2-PRODUCTION/06-alternativas-externas.md) | Firebase, Appwrite |

> **Supabase Cloud:** si usas Supabase Cloud (plan Free/Pro), revisa tambien [19-MONITOREO-PRODUCCION/04-supabase-consumo-costos](../19-MONITOREO-PRODUCCION/04-supabase-consumo-costos/) para monitorear consumo, configurar alertas y optimizar costos.

### PARTE 3: CI/CD

| Archivo | Descripción |
|---------|-------------|
| [01-makefile-universal.md](./PARTE-3-CI_CD/01-makefile-universal.md) | Template Makefile |
| [02-workflows-github-actions.md](./PARTE-3-CI_CD/02-workflows-github-actions.md) | GitHub Actions |
| [03-patrones-extrapolables.md](./PARTE-3-CI_CD/03-patrones-extrapolables.md) | Adaptar a nuevos proyectos |
| [04-git-hooks-y-commits.md](./PARTE-3-CI_CD/04-git-hooks-y-commits.md) | commitlint, hooks |

---

## 🎯 Contenido

### PARTE 1: Desarrollo Local
- Configurar Supabase desde cero (Docker + CLI)
- Edge Functions (Deno + TypeScript)
- Makefile de desarrollo
- Variables de entorno (API keys legacy y nuevo formato)
- Migraciones, seeds y RLS avanzado
- Integración con Flutter:
  - Auth (email, OAuth, Magic Link, teléfono, sesiones)
  - CRUD con Clean Architecture
  - Realtime (Broadcast, Presence, Postgres Changes)
  - Storage (upload, download, RLS en buckets)
  - Edge Functions desde Flutter
- Testing con pgTAP y basejump helpers

### PARTE 2: Auto-hospedaje
- Elegir hosting (DigitalOcean, Hetzner, etc.)
- Deploy con Docker
- Configuración de producción
- Backups y mantenimiento
- Alternativas (Firebase, Appwrite)

### PARTE 3: Automatizaciones
- Makefile universal
- GitHub Actions workflows
- Patrones reutilizables
- Git hooks y conventional commits

---

## 🚀 Orden sugerido de aprendizaje

```
PARTE 0 → PARTE 1 → PARTE 2 → PARTE 3
SQL/PostgreSQL → Desarrollo → Producción → CI/CD
```

---

**Nivel:** Principiante a Avanzado  
**Tiempo estimado:** 20-29 horas (incluyendo PARTE 0)