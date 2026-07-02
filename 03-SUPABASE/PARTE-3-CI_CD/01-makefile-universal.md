# 01 - Makefile Universal

> Una plantilla de Makefile reutilizable que puedes copiar y adaptar para cualquier proyecto Flutter con Supabase.

---

## 🎯 Objetivos

- Proporcionar un Makefile completo como plantilla
- Explicar cada sección para personalización
- Dar ejemplos de uso para diferentes flujos de trabajo

---

## 1. Makefile completo (plantilla)

```makefile
# ==============================================================================
# MAKEFILE UNIVERSAL PARA FLUTTER + SUPABASE
# ==============================================================================

PROJECT_NAME := mi-proyecto-flutter
FLUTTER_SDK := flutter
SUPABASE_CLI := supabase

DEFAULT_ANDROID := $(shell $(FLUTTER_SDK) devices 2>/dev/null | awk -F "•" '/android/ {gsub(/ /,"",$$2); print $$2; exit}')
DEVICE ?= $(DEFAULT_ANDROID)

SHELL := /bin/bash
.DEFAULT_GOAL := help

# ==============================================================================
# HELP
# ==============================================================================
.PHONY: help
help: ## Mostrar todos los comandos disponibles
	@echo "📋 $(PROJECT_NAME) - Comandos disponibles"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'

# ==============================================================================
# SETUP
# ==============================================================================
.PHONY: setup
setup: deps mocks ## Instalar dependencias y generar mocks

.PHONY: deps
deps: ## Instalar dependencias
	$(FLUTTER_SDK) pub get

.PHONY: mocks
mocks: ## Generar mocks
	$(FLUTTER_SDK) pub run build_runner build --delete-conflicting-outputs

# ==============================================================================
# DESARROLLO
# ==============================================================================
.PHONY: dev
dev: check run ## Ejecutar app en modo desarrollo

.PHONY: dev-start
dev-start: supabase-up dev ## Iniciar Supabase y app

.PHONY: dev-stop
dev-stop: supabase-down ## Detener Supabase

.PHONY: watch
watch: ## Regenerar código automáticamente
	$(FLUTTER_SDK) pub run build_runner watch --delete-conflicting-outputs

.PHONY: clean
clean: ## Limpiar build
	$(FLUTTER_SDK) clean && rm -rf coverage/ .dart_tool/build

# ==============================================================================
# CALIDAD
# ==============================================================================
.PHONY: format
format: ## Formatear código
	dart format .

.PHONY: analyze
analyze: ## Análisis estático
	$(FLUTTER_SDK) analyze

.PHONY: lint
lint: analyze

.PHONY: test
test: ## Ejecutar tests
	$(FLUTTER_SDK) test

.PHONY: coverage
coverage: ## Tests con coverage
	$(FLUTTER_SDK) test --coverage

.PHONY: check
check: format lint test ## Verificación completa

# ==============================================================================
# BUILD
# ==============================================================================
.PHONY: run
run: env-check ## Ejecutar app
	$(FLUTTER_SDK) run $(if $(DEVICE),-d $(DEVICE))

.PHONY: build-apk
build-apk: env-check ## Generar APK
	$(FLUTTER_SDK) build apk --release

.PHONY: build-appbundle
build-appbundle: env-check ## Generar AAB
	$(FLUTTER_SDK) build appbundle --release

# ==============================================================================
# SUPABASE
# ==============================================================================
.PHONY: supabase-up
supabase-up: deps-check ## Iniciar Supabase
	$(SUPABASE_CLI) start

.PHONY: supabase-down
supabase-down: ## Detener Supabase
	$(SUPABASE_CLI) stop

.PHONY: db-reset
db-reset: deps-check ## Resetear BD
	$(SUPABASE_CLI) db reset

.PHONY: db-push
db-push: deps-check ## Push migraciones
	$(SUPABASE_CLI) db push

.PHONY: db-test
db-test: deps-check ## Tests de BD
	$(SUPABASE_CLI) test db

.PHONY: db-new-migration
db-new-migration: deps-check ## Nueva migración
	@if [ -z "$(name)" ]; then \
		read -p "Nombre: " name; \
		$(SUPABASE_CLI) migration new $$name; \
	fi

# ==============================================================================
# VALIDACIÓN
# ==============================================================================
.PHONY: validate
validate: check deps-check ## Validar entorno

.PHONY: env-check
env-check:
	@./scripts/check_env.sh .env

.PHONY: deps-check
deps-check: ## Verificar herramientas
	@command -v docker >/dev/null 2>&1 || { echo "❌ Docker no instalado"; exit 1; }
	@command -v $(SUPABASE_CLI) >/dev/null 2>&1 || { echo "❌ Supabase CLI no instalado"; exit 1; }

.PHONY: git-hooks
git-hooks: ## Instalar git hooks
	@echo "#!/bin/bash\nmake check" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
```

---

## 2. Scripts complementarios

### check_env.sh

```bash
#!/bin/bash
set -e

ENV_FILE=$${1:-.env}
[ -f "$ENV_FILE" ] || { echo "❌ $ENV_FILE no existe"; exit 1; }
grep -q "^SUPABASE_URL=" "$ENV_FILE" || { echo "❌ Falta SUPABASE_URL"; exit 1; }
grep -q "^SUPABASE_PUBLISHABLE_KEY=" "$ENV_FILE" || { echo "❌ Falta SUPABASE_PUBLISHABLE_KEY"; exit 1; }
echo "✅ $ENV_FILE válido"
```

```bash
chmod +x scripts/check_env.sh
```

---

## 3. Adaptar a nuevo proyecto

1. Copiar Makefile a la raíz del proyecto
2. Cambiar `PROJECT_NAME`
3. Ajustar `FLUTTER_SDK` si usas FVM

---

**Siguiente**: [02-workflows-github-actions.md](./02-workflows-github-actions.md)