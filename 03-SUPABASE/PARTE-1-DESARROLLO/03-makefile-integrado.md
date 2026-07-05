# 03 - Makefile Integrado

> El Makefile es el centro de comando de tu proyecto. Aprende a usarlo y a personalizarlo para cualquier proyecto Flutter + Supabase.

---

## 🎯 Objetivos de este archivo

- Entender la estructura del Makefile
- Conocer todos los comandos disponibles
- Personalizar el Makefile para nuevos proyectos

---

## 1. Estructura del Makefile

El Makefile organiza los comandos en secciones lógicas:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ESTRUCTURA DEL MAKEFILE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  HELPER                                                         │
│  └─ help: Muestra todos los comandos disponibles               │
│                                                                  │
│  DEVELOPMENT                                                    │
│  └─ setup, dev, deps, format, lint, watch, clean              │
│                                                                  │
│  TESTING                                                        │
│  └─ test, coverage, integration                                 │
│                                                                  │
│  BUILD & RUN                                                    │
│  └─ run, build-apk, build-appbundle, build-web, build-linux   │
│                                                                  │
│  SUPABASE                                                       │
│  └─ supabase-up, supabase-down, db-push, db-reset, db-lint     │
│                                                                  │
│  VALIDATION                                                     │
│  └─ validate, env-check, deps-check, git-hooks                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Makefile completo (plantilla)

Copia este Makefile en la raíz de tu proyecto y personaliza las variables.

```makefile
# ==============================================================================
# CONFIGURACIÓN DEL PROYECTO
# ==============================================================================

# Nombre del proyecto (cambiar para cada proyecto)
PROJECT_NAME := mi-proyecto-flutter

# Default shell
SHELL := /bin/bash

# Binarios - detectar automáticamente Flutter y Supabase
FLUTTER := $(shell [ -d .fvm ] && command -v fvm >/dev/null 2>&1 && echo fvm flutter || command -v flutter 2>/dev/null || echo flutter)
SUPABASE := $(shell command -v supabase 2>/dev/null || echo supabase)

# Dispositivo por defecto (Android)
DEFAULT_ANDROID = $(shell flutter devices 2>/dev/null | awk -F "•" '/android/ {gsub(/ /,"",$$2); print $$2; exit}')
DEVICE ?= $(DEFAULT_ANDROID)

# Objetivo por defecto
.DEFAULT_GOAL := help

# ==============================================================================
# HELPER - Comandos de utilidad
# ==============================================================================

.PHONY: help
help: ## Mostrar todos los comandos disponibles
	@echo "📋 Comandos disponibles para $(PROJECT_NAME)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'

# ==============================================================================
# DEVELOPMENT - Entorno de desarrollo
# ==============================================================================

.PHONY: setup
setup: deps mocks ## Instalar dependencias y generar mocks
	@echo "==> Setup completo para $(PROJECT_NAME)"

.PHONY: dev
dev: check run ## Lanzar app en modo desarrollo

.PHONY: dev-start
dev-start: supabase-up dev ## Iniciar entorno completo (Supabase + app)

.PHONY: dev-stop
dev-stop: supabase-down ## Detener entorno de desarrollo

.PHONY: deps
deps: ## Instalar dependencias de Flutter
	@echo "==> Instalando dependencias de Flutter"
	$(FLUTTER) pub get

.PHONY: outdated
outdated: ## Verificar dependencias obsoletas
	$(FLUTTER) pub outdated

.PHONY: upgrade
upgrade: ## Actualizar todas las dependencias
	$(FLUTTER) pub upgrade

.PHONY: format
format: ## Formatear código Dart
	@echo "==> Formateando código Dart"
	dart format .

.PHONY: fix
fix: ## Aplicar correcciones automáticas
	@echo "==> Aplicando correcciones"
	$(FLUTTER) fix --apply

.PHONY: analyze
analyze: ## Ejecutar análisis estático
	@echo "==> Ejecutando análisis estático"
	$(FLUTTER) analyze

.PHONY: lint
lint: analyze ## Alias para analyze

.PHONY: watch
watch: ## Ejecutar build_runner en modo watch
	@echo "==> Ejecutando build_runner watcher"
	$(FLUTTER) pub run build_runner watch --delete-conflicting-outputs

.PHONY: mocks
mocks: ## Generar archivos de mocks (una vez)
	@echo "==> Generando archivos de mocks"
	$(FLUTTER) pub run build_runner build --delete-conflicting-outputs

.PHONY: clean
clean: ## Limpiar artifacts de build
	@echo "==> Limpiando artifacts de build"
	$(FLUTTER) clean
	rm -rf coverage/
	rm -rf .dart_tool/build

.PHONY: check
check: format lint test ## Ejecutar format, lint y tests (listo para CI)
	@echo "✅ Verificación completa exitosa"

# ==============================================================================
# TESTING - Pruebas
# ==============================================================================

.PHONY: test
test: ## Ejecutar tests unitarios y de widgets
	@echo "==> Ejecutando suite de tests"
	$(FLUTTER) test

.PHONY: coverage
coverage: ## Ejecutar tests con reporte de coverage
	@echo "==> Ejecutando tests con coverage"
	$(FLUTTER) test --coverage
	@echo "Coverage escrito en coverage/"

.PHONY: integration
integration: env-test-check ## Ejecutar tests de integración (.env.test)
	@echo "==> Ejecutando tests de integración (.env.test)"
	@set -euo pipefail; \
	backup=.env.bak.integration; \
	[ -f .env ] && cp .env $$backup; \
	cp .env.test .env; \
	trap '[ -f $$backup ] && mv $$backup .env || rm -f .env' EXIT; \
	$(FLUTTER) test integration_test/app_test_suite.dart

.PHONY: integration-supabase
integration-supabase: deps-check env-test-check ## Tests de integración con Supabase local
	@echo "==> Ejecutando tests de integración con Supabase local (.env.test)"
	@set -euo pipefail; \
	backup=.env.bak.integration; \
	[ -f .env ] && cp .env $$backup; \
	cp .env.test .env; \
	cleanup() { \
		[ -f $$backup ] && mv $$backup .env || rm -f .env; \
		$(SUPABASE) stop; \
	}; \
	trap cleanup EXIT; \
	$(SUPABASE) start; \
	$(FLUTTER) test integration_test/app_test_suite.dart

.PHONY: integration-android
integration-android: env-test-check ## Tests de integración en dispositivo Android
	@if [ -z "$(DEVICE)" ]; then \
		echo "ERROR: Necesitas DEVICE=<id> (ej: emulator-5554)"; \
		exit 1; \
	fi
	@echo "==> Ejecutando tests de integración en $(DEVICE) (.env.test)"
	@set -euo pipefail; \
	backup=.env.bak.integration; \
	[ -f .env ] && cp .env $$backup; \
	cp .env.test .env; \
	trap '[ -f $$backup ] && mv $$backup .env || rm -f .env' EXIT; \
	$(FLUTTER) test integration_test/app_test_suite.dart -d $(DEVICE)

.PHONY: integration-android-supabase
integration-android-supabase: env-test-check ## Tests en Android con Supabase local
	@if [ -z "$(DEVICE)" ]; then \
		echo "ERROR: Necesitas DEVICE=<id>"; \
		exit 1; \
	fi
	@echo "==> Ejecutando tests en Android con Supabase local"
	@set -euo pipefail; \
	backup=.env.bak.integration; \
	[ -f .env ] && cp .env $$backup; \
	cp .env.test .env; \
	cleanup() { \
		[ -f $$backup ] && mv $$backup .env || rm -f .env; \
		adb -s $(DEVICE) reverse --remove tcp:54321 >/dev/null 2>&1 || true; \
		$(SUPABASE) stop; \
	}; \
	trap cleanup EXIT; \
	$(SUPABASE) start; \
	adb -s $(DEVICE) reverse tcp:54321 tcp:54321; \
	$(FLUTTER) test integration_test/app_test_suite.dart -d $(DEVICE)

# ==============================================================================
# BUILD & RUN - Construcción y ejecución
# ==============================================================================

.PHONY: run
run: env-check ## Lanzar app (usa DEVICE si está configurado)
	@echo "==> Lanzando app $(if $(DEVICE),en $(DEVICE),en dispositivo por defecto)"
	$(FLUTTER) run $(if $(DEVICE),-d $(DEVICE))

.PHONY: build-apk
build-apk: env-check ## Construir APK de Android (release)
	@echo "==> Construyendo APK release"
	$(FLUTTER) build apk --release

.PHONY: build-appbundle
build-appbundle: env-check ## Construir Android App Bundle (AAB)
	@echo "==> Construyendo AAB release"
	$(FLUTTER) build appbundle --release

.PHONY: build-web
build-web: env-check ## Construir aplicación web
	@echo "==> Construyendo aplicación web"
	$(FLUTTER) build web --release

.PHONY: build-linux
build-linux: env-check ## Construir aplicación Linux
	@echo "==> Construyendo aplicación Linux"
	$(FLUTTER) build linux --release

.PHONY: build-ios
build-ios: env-check ## Construir aplicación iOS (requiere macOS)
	@echo "==> Construyendo aplicación iOS"
	$(FLUTTER) build ios --release

# ==============================================================================
# SUPABASE - Comandos de Supabase
# ==============================================================================

.PHONY: supabase-up
supabase-up: deps-check ## Iniciar Supabase local
	$(SUPABASE) start

.PHONY: supabase-down
supabase-down: deps-check ## Detener Supabase local
	$(SUPABASE) stop

.PHONY: db-push
db-push: deps-check ## Enviar cambios locales al remoto
	$(SUPABASE) db push

.PHONY: db-reset
db-reset: deps-check ## Resetear base de datos local
	$(SUPABASE) db reset

.PHONY: db-lint
db-lint: deps-check ## Verificar esquema de base de datos
	$(SUPABASE) db lint

.PHONY: db-status
db-status: deps-check ## Mostrar estado de la base de datos
	$(SUPABASE) status

.PHONY: db-new-migration
db-new-migration: deps-check ## Crear nueva migración (interactive o name=foo)
	@if [ -z "$(name)" ]; then \
		read -p "Nombre de la migración: " name; \
		$(SUPABASE) migration new $$name; \
	else \
		$(SUPABASE) migration new $(name); \
	fi

.PHONY: db-test
db-test: deps-check ## Ejecutar tests de base de datos (pgTAP)
	$(SUPABASE) test db

.PHONY: studio
studio: deps-check ## Abrir Supabase Studio en navegador
	$(SUPABASE) studio

# ==============================================================================
# VALIDATION - Verificaciones
# ==============================================================================

.PHONY: validate
validate: check deps-check ## Verificar que todo está listo
	@echo "==> Verificando que Supabase esté corriendo..."
	@$(SUPABASE) status | grep -q "API URL" || $(SUPABASE) start
	@echo "✅ Validación completa: Código limpio y Supabase activo"

.PHONY: env-check
env-check: ## Verificar variables de entorno
	@./scripts/check_env.sh .env

.PHONY: env-test-check
env-test-check: ## Verificar variables de entorno de test
	@./scripts/check_env.sh .env.test

.PHONY: deps-check
deps-check: ## Verificar herramientas requeridas
	@echo "==> Verificando herramientas requeridas"
	@command -v docker >/dev/null 2>&1 || { echo "❌ Docker no está instalado"; exit 1; }
	@docker info >/dev/null 2>&1 || { echo "❌ Docker está instalado pero no está corriendo"; exit 1; }
	@command -v $(SUPABASE) >/dev/null 2>&1 || { echo "❌ Supabase CLI no está instalado"; exit 1; }
	@echo "✅ Docker y Supabase CLI listos"

.PHONY: git-hooks
git-hooks: ## Instalar git hooks para ejecutar checks antes de commit
	@echo "==> Instalando git hooks"
	@echo "#!/bin/bash\nmake check" > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
	@echo "✅ Git hooks instalados. 'make check' se ejecutará antes de cada commit"
```

---

## 3. Script de validación de entorno

El Makefile depende del script `scripts/check_env.sh`. Créalo si no existe:

```bash
#!/bin/bash
set -e

ENV_FILE=$1

if [ -z "$ENV_FILE" ]; then
    echo "Usage: $0 <env_file>"
    exit 1
fi

echo "==> Validando variables de entorno en $ENV_FILE"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Missing $ENV_FILE file in root."
    exit 1
fi

if ! grep -q "^SUPABASE_URL=" "$ENV_FILE"; then
    echo "Error: Missing SUPABASE_URL in $ENV_FILE"
    exit 1
fi

if ! grep -q "^SUPABASE_ANON_KEY=" "$ENV_FILE"; then
    echo "Error: Missing SUPABASE_ANON_KEY in $ENV_FILE"
    exit 1
fi

if grep -q "^REST_API_BASE_URL=" "$ENV_FILE"; then
    echo "Info: REST_API_BASE_URL presente en $ENV_FILE"
else
    echo "Info: REST_API_BASE_URL no encontrada (opcional)"
fi

echo "✅ Environment $ENV_FILE listo"
```

```bash
chmod +x scripts/check_env.sh
```

---

## 4. Cómo personalizar para un nuevo proyecto

### Paso 1: Copiar el Makefile

Copia el template a la raíz del nuevo proyecto.

### Paso 2: Cambiar PROJECT_NAME

```makefile
PROJECT_NAME := mi-nuevo-proyecto
```

### Paso 3: Ajustar variables según necesidad

Puedes eliminar comandos que no necesites:

- ¿Solo Android? → Elimina `build-ios`, `build-linux`, `build-web`
- ¿No usas tests de integración? → Elimina los comandos `integration-*`
- ¿No usas Supabase? → Elimina toda la sección SUPABASE

### Paso 4: Verificar que funciona

```bash
make help
make setup
make dev-start
```

---

## 5. Comandos esenciales por flujo de trabajo

### Flujo de desarrollo diario

```bash
# Mañana: Iniciar entorno
make dev-start

# Durante el día
make watch          # Regenerar código automáticamente
make test           # Verificar tests
make lint           # Verificar código

# Tarde: Detener entorno
make dev-stop
```

### Flujo de release

```bash
# Pre-release
make check                  # Verificar todo
make coverage               # Coverage > 80%

# Build
make build-apk             # Generar APK
make build-appbundle       # Generar AAB (Play Store)

# Validar APK
# (subir a Play Store o分发)
```

### Flujo de migraciones

```bash
# Crear nueva migración
make db-new-migration name=add_users_table

# Editar migración en supabase/migrations/

# Aplicar localmente
make db-reset

# Probar en local
make db-test

# Enviar a producción
make db-push
```

---

## 6. Integración con GitHub Actions

El Makefile se integra con los workflows de CI/CD. Ejemplo de integración:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-flutter-env
      
      - name: Verificar código
        run: make check
      
      - name: Tests con coverage
        run: make coverage
```

---

## ✅ Checklist de Makefile

- [ ] Makefile copiado en la raíz del proyecto
- [ ] `PROJECT_NAME` actualizado
- [ ] `scripts/check_env.sh` creado y con permisos de ejecución
- [ ] `make help` funciona correctamente
- [ ] `make setup` funciona correctamente
- [ ] `make dev-start` inicia Supabase y la app

---

## 📚 Recursos

- [Makefile Tutorial](https://makefiletutorial.com/)
- [Flutter Makefile Best Practices](https://example.com)
- [Supabase CLI Commands](https://supabase.com/docs/reference/cli/overview)


---

## 📚 Referencias

- [Supabase | Documentación oficial](https://supabase.com/docs) — Guías, API reference y arquitectura
- [Supabase | CLI reference](https://supabase.com/docs/reference/cli) — Comandos de la CLI de Supabase
- [Supabase | Flutter SDK](https://pub.dev/packages/supabase_flutter) — SDK oficial para Flutter
- [Supabase | Migraciones](https://supabase.com/docs/guides/local-development/migrations) — Gestión de migraciones locales

---

> 📖 **Siguiente:** [04-variables-entorno.md](./04-variables-entorno.md)