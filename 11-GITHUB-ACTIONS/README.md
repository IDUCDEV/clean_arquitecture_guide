# 11 — GitHub Actions + Automatización

> Entiende cómo funciona GitHub Actions y cómo automatizar tu pipeline Flutter + Supabase. **Deja de copiar YAML sin entenderlo.**

---

## 🎯 Objetivos

- Entender la arquitectura de GitHub Actions (workflow, job, step, runner)
- Leer y modificar cualquier workflow YAML con confianza
- Crear pipelines de CI/CD para Flutter + Supabase desde cero

---

## 📋 Índice

| Archivo | Descripción | Nivel |
|---------|-------------|-------|
| [01-conceptos.md](./01-conceptos.md) | Workflows, jobs, steps, runners, eventos trigger | 🔤 Básico |
| [02-sintaxis-yaml.md](./02-sintaxis-yaml.md) | Anatomía de un workflow: `on:`, `jobs:`, `steps:`, `uses:`, `run:` | 🔤 Básico |
| [03-actions-esenciales.md](./03-actions-esenciales.md) | `subosito/flutter-action`, `supabase/setup-cli`, `actions/cache` | 📦 Medio |
| [04-workflows-analisis.md](./04-workflows-analisis.md) | Recorrido de los 6 workflows reales del proyecto | 🔍 Medio |
| [05-secrets-envs-matrix.md](./05-secrets-envs-matrix.md) | Secrets, entornos, matrix builds, path filtering | 🔐 Medio |
| [06-monorepo-avanzado.md](./06-monorepo-avanzado.md) | Estrategias para monorepo, reutilización, caching | 🏗️ Alto |
| [07-ejercicios.md](./07-ejercicios.md) | Práctica: crear workflows desde cero | 🏋️ Práctica |

---

## 🔗 Siguiente paso

Después de dominar GitHub Actions, revisa [10-MAKEFILE/06-make-en-ci.md](../10-MAKEFILE/06-make-en-ci.md) para ver cómo Make y Actions se complementan.

---

**Nivel:** Básico → Avanzado  
**Tiempo estimado:** 4-6 horas  
**Ejercicios:** 4+
