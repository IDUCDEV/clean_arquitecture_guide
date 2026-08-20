# 01 — ¿Qué es Make y por qué lo usamos?

---

## 1. ¿Qué es Make?

Make es una herramienta de automatización de los años 70 (sí, anterior a internet) que **sigue siendo el estándar** para gestionar proyectos de software. Lee un archivo llamado `Makefile` y ejecuta comandos según reglas que tú defines.

### La analogía

```
Makefile = una lista de recetas de cocina

make setup     → "Prepara los ingredientes" (instalar dependencias)
make test      → "Prueba que la sopa no esté salada" (ejecutar tests)
make build-apk → "Cocina el plato final" (compilar APK)
```

---

## 2. ¿Por qué Makefile y no scripts sueltos?

| Aspecto | Scripts sueltos (`setup.sh`, `test.sh`, etc.) | Makefile |
|---------|----------------------------------------------|----------|
| **Número de archivos** | 10+ scripts | 1 archivo |
| **Dependencias entre comandos** | Manual (tú encadenas) | Automático (`target: dependency`) |
| **Documentación** | La escribes aparte | `make help` genera la lista |
| **Variables** | Variables de shell | Variables de Make + shell |
| **Solo ejecutar lo necesario** | No | Sí (solo si cambió la dependencia) |
| **Estándar** | Depende del proyecto | Universal en DevOps |

### Ejemplo: sin Makefile

```bash
# Tienes que recordar:
cd apps/mobile && flutter pub get
cd apps/mobile && dart run build_runner build --delete-conflicting-outputs
cd apps/mobile && flutter test
cd supabase && supabase start
```

### Con Makefile

```bash
make setup   # hace todo lo de arriba
```

---

## 3. ¿Qué hace el Makefile en tu proyecto?

El Makefile del monorepo rifa-gestion-app organiza los comandos en:

| Sección | Propósito |
|---------|-----------|
| **Desarrollo** | Iniciar/Detener Supabase, correr app, regenerar código |
| **Calidad** | Formatear, analizar, testear |
| **Dependencias** | Instalar, actualizar |
| **Supabase** | Migraciones, tests de BD, deploy |
| **Build** | APK, AAB, web, Linux |
| **Utilidades** | Cambiar entorno (.env), validar, limpiar |
| **Git** | Conventional commits, hooks |

> **🎯 Objetivo final**: Cuando termines este módulo, podrás leer el Makefile de tu proyecto y entender **qué hace cada línea, por qué está ahí y cómo modificarla**.

---

## 4. Make como orquestador entre módulos

Make no solo ejecuta comandos aislados: **conecta todas las herramientas del proyecto en una interfaz unificada**. Aquí es donde brilla en proyectos reales.

| Target | Módulo que usa | Qué hace |
|--------|----------------|----------|
| `make commit` | 12-GIT-FLOW | Ejecuta Commitizen (Conventional Commits) |
| `make release` | 12-GIT-FLOW | Ejecuta standard-version (SemVer + CHANGELOG) |
| `make branch` | 12-GIT-FLOW | Crea rama con nomenclatura Conventional Branch |
| `make check` | Quality gate | format + analyze + test |
| `make ci` | 11-GITHUB-ACTIONS | Simula pipeline CI local |

### Ejemplo: hacer un commit

```bash
# SIN Makefile: tienes que recordar el formato exacto
npx cz

# CON Makefile: un solo comando
make commit
```

### Ejemplo: crear una release

```bash
# SIN Makefile: ejecutar comandos de git manualmente
npm run release
git push --follow-tags

# CON Makefile: un solo comando
make release
```

### Ejemplo: crear una rama feature

```bash
# SIN Makefile: 4 comandos
git checkout develop
git pull
git checkout -b feature/agregar-filtro

# CON Makefile: un solo comando
make branch FEATURE=agregar-filtro
```

> **💡 Filosofía**: Make es la "capa de abstracción" que conecta Git, Flutter, Supabase y herramientas de calidad en una interfaz unificada. Cuando cambias una herramienta, solo cambias el Makefile, no todos los scripts de CI.

---

## 📚 Referencias

- [GNU | Make manual](https://www.gnu.org/software/make/manual/) — Documentación oficial de GNU Make

---

**Siguiente**: [02-sintaxis-basica.md](./02-sintaxis-basica.md) — Targets, dependencias y recipes
