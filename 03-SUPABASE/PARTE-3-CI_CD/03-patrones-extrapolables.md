# 03 - Patrones Extrapolables

> Aprende a extraer y adaptar los patrones de automatización de sereni-app a cualquier nuevo proyecto Flutter.

---

## 1. Elementos extraíbles

| Elemento | Origen | Cómo adaptar |
|----------|-------|--------------|
| **Makefile** | sereni-app/Makefile | Cambiar PROJECT_NAME |
| **check_env.sh** | scripts/check_env.sh | Mismo script, siempre funciona |
| **Workflows** | .github/workflows/ | Actualizar project ID, secrets |
| **AGENTS.md** | AGENTS.md | Adaptar al nuevo proyecto |
| **supabase/** | supabase/ | Copiar estructura |

---

## 2. Proceso para nuevo proyecto

```bash
# 1. Crear proyecto
flutter create mi-proyecto
cd mi-proyecto

# 2. Copiar estructura Supabase
mkdir supabase/
cp -r /guia/supabase/* supabase/

# 3. Copiar Makefile
cp /guia/01-CLEAN-ARCHITECTURE/../Makefile ./
# Editar PROJECT_NAME

# 4. Copiar scripts
mkdir scripts
cp /guia/scripts/check_env.sh scripts/

# 5. Copiar workflows
mkdir -p .github/workflows
cp /guia/.github/workflows/* .github/workflows/

# 6. Instalar dependencias
make setup
```

---

## 3. Adaptar Makefile

```makefile
# Cambiar esto:
PROJECT_NAME := mi-nuevo-proyecto

# Esto puede variar:
FLUTTER_SDK := flutter  # o 'fvm flutter'
```

---

## 4. Adaptar workflows

```yaml
# Secrets en GitHub → Settings → Secrets
SUPABASE_URL: "https://tu-proyecto.supabase.co"
SUPABASE_PUBLISHABLE_KEY: "sb_publishable_..."
SUPABASE_PROJECT_ID: "abc123"
```

---

## 5. AGENTS.md template

```markdown
# AGENTS.md - Guidance for AI Coding Agents

## Project Overview
**Tu Proyecto** es una app Flutter con Clean Architecture y Supabase.

## Architecture
- Clean Architecture en lib/src/
- Legacy en lib/src_old/ (mantener solo)

## Setup
- make setup
- make dev-start
- make watch

## Testing
- Tests en test/
- make test
- make coverage
```

---

## 6. Mantenimiento de templates

Cuando encuentres mejoras, actualiza la guía:

```bash
# Actualizar Makefile con mejores prácticas
# Actualizar workflows
# Añadir nuevos patrones
```

---

**Siguiente**: [04-git-hooks-y-commits.md](./04-git-hooks-y-commits.md)