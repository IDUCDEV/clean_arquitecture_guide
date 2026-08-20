# 05 — Creación Personalizada de Makefiles

---

## 1. Template mínimo

```makefile
# ==============================================================================
# MAKEFILE - Template mínimo para Flutter + Supabase
# ==============================================================================

PROJECT_NAME := mi-proyecto
MOBILE_DIR := .
SUPABASE_DIR := supabase

SHELL := /bin/bash
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "📋 $(PROJECT_NAME) - Comandos disponibles"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'

.PHONY: setup
setup: deps mocks ## Instalar dependencias y generar código

.PHONY: deps
deps: ## Instalar dependencias
	cd $(MOBILE_DIR) && flutter pub get

.PHONY: mocks
mocks: ## Generar código (build_runner)
	cd $(MOBILE_DIR) && dart run build_runner build --delete-conflicting-outputs

.PHONY: dev
dev: check run ## Ejecutar app en modo desarrollo

.PHONY: check
check: format analyze test ## Verificación completa

.PHONY: format
format: ## Formatear código
	cd $(MOBILE_DIR) && dart format .

.PHONY: analyze
analyze: ## Análisis estático
	cd $(MOBILE_DIR) && flutter analyze

.PHONY: test
test: ## Ejecutar tests
	cd $(MOBILE_DIR) && flutter test

.PHONY: run
run: ## Ejecutar app
	cd $(MOBILE_DIR) && flutter run

.PHONY: clean
clean: ## Limpiar
	cd $(MOBILE_DIR) && flutter clean
	rm -rf $(MOBILE_DIR)/coverage
```

---

## 2. Cómo añadir un nuevo comando

```makefile
# 1. Decide el nombre (kebab-case, descriptivo)
# 2. Decide prerequisitos (si los hay)
# 3. Escribe la receta (indentada con TAB)
# 4. Añade descripción con ##

.PHONY: docker-clean
docker-clean: ## Limpiar imágenes Docker no usadas
	docker system prune -af
```

---

## 3. Cómo adaptar para diferentes proyectos

### Proyecto Flutter simple (sin monorepo)

```makefile
# Solo cambia MOBILE_DIR
MOBILE_DIR := .
```

### Proyecto solo Supabase (sin Flutter)

```makefile
# Elimina toda la sección de Flutter
# Deja solo:
.PHONY: supabase-up
supabase-up:
	supabase start

.PHONY: db-push
db-push:
	supabase db push
```

### Proyecto con múltiples flavors

```makefile
.PHONY: run-dev
run-dev: ## Ejecutar en modo development
	cd $(MOBILE_DIR) && flutter run --flavor development

.PHONY: run-prod
run-prod: ## Ejecutar en modo producción
	cd $(MOBILE_DIR) && flutter run --flavor production
```

---

## 4. Targets cross-module (Git Flow + SemVer)

Estos targets conectan Make con las herramientas del módulo 12 (Git Flow + Conventional Commits + SemVer).

### make commit

```makefile
.PHONY: commit
commit: ## Crear commit (Conventional Commits via Commitizen)
	@npm run commit
```

**Uso:**
```bash
make commit
# → Formulario interactivo de Commitizen
# → Husky valida formato (pre-commit + commit-msg)
# → Commit creado con formato correcto
```

### make release

```makefile
.PHONY: release
release: ## Crear release (SemVer + CHANGELOG auto)
	@npm run release
	@git push --follow-tags
	@echo "${GREEN}✅ Release publicado con tags${RESET}"
```

**Uso:**
```bash
make release
# → standard-version detecta tipo de cambio
# → Incrementa versión (feat→minor, fix→patch, breaking→major)
# → Genera CHANGELOG.md
# → Crea commit + tag vX.Y.Z
# → Push con tags a origin
```

### make branch

```makefile
.PHONY: branch
branch: ## Crear rama feature (Conventional Branch)
	@read -p "Nombre de la feature: " name; \
	git checkout develop && \
	git pull && \
	git checkout -b feature/$$name
	@echo "${GREEN}✅ Rama feature/$$name creada desde develop${RESET}"
```

**Uso:**
```bash
make branch
# → Pide nombre de la feature
# → git checkout develop && git pull
# → git checkout -b feature/agregar-filtro

# O con variable:
make branch FEATURE=agregar-filtro
```

### make hotfix

```makefile
.PHONY: hotfix
hotfix: ## Crear rama hotfix
	@read -p "Descripcion del fix: " name; \
	git checkout main && \
	git pull && \
	git checkout -b hotfix/$$name
	@echo "${GREEN}✅ Rama hotfix/$$name creada desde main${RESET}"
```

**Uso:**
```bash
make hotfix
# → Pide descripción del fix
# → git checkout main && git pull
# → git checkout -b hotfix/corregir-crash
```

### make validate

```makefile
.PHONY: validate
validate: check ## Validar código completo (format + analyze + test)
	@echo "${GREEN}✅ Validación completa: código listo para commit${RESET}"
```

---

## 5. Buenas prácticas

| Práctica | Por qué |
|----------|---------|
| `cd $(DIR) && comando` | No afecta el shell padre; el `cd` solo aplica al comando |
| `@echo "mensaje"` | Feedback visual sin ruido |
| `command -v herramienta` | Verificar existencia de herramienta |
| `|| { echo "error"; exit 1; }` | Error handling explícito |
| Variables para directorios | DRY: cambiar en un solo lugar |
| `.PHONY` en todos los targets | Evita falsos "up to date" |
| `##` para descripciones | Auto-documentación con `help` |

---

## 📚 Referencias

- [GNU | Make manual](https://www.gnu.org/software/make/manual/) — Documentación oficial de GNU Make

---

**Siguiente**: [06-make-en-ci.md](./06-make-en-ci.md) — Make en GitHub Actions
