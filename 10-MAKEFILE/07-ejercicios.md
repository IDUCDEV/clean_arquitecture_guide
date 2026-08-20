# 07 — Ejercicios de Makefile

---

## Ejercicio 1: Leer y entender

```makefile
# Dado este fragmento del Makefile real:
.PHONY: env-ip
env-ip:
	@echo "${CYAN}🔍 Detectando IP local...${RESET}"
	@IP=$$(ip -4 addr show | grep -oP '(?<=inet\s)\d+\.\d+\.\d+\.\d+' | grep -v '127.0.0.1' | head -1); \
	if [ -z "$$IP" ]; then \
		echo "${YELLOW}⚠️  No se pudo detectar IP automáticamente${RESET}"; \
		exit 1; \
	fi; \
	sed -i "s|^SUPABASE_URL=.*|SUPABASE_URL=http://$$IP:54321|" apps/mobile/.env; \
	echo "${GREEN}✅ SUPABASE_URL=http://$$IP:54321 (modo WiFi)${RESET}"
```

**Preguntas:**
1. ¿Qué hace `grep -v '127.0.0.1'`?
2. ¿Qué pasa si `head -1` no encuentra ninguna IP?
3. ¿Por qué usa `$$IP` y no `$IP`?

---

## Ejercicio 2: Depurar un target

```makefile
# Este target tiene un error. ¿Cuál?
.PHONY: test-all
test-all: test-mobile test-web

.PHONY: test-mobile
test-mobile:
	cd apps/mobile
	flutter test

.PHONY: test-web
test-web:
	cd apps/web
	npm test
```

<details>
<summary>🔍 Solución</summary>

El error está en la indentación de `test-mobile` y `test-web`: la receta está separada en dos líneas. En Make, cada línea de la receta se ejecuta en un subshell diferente. El `cd apps/mobile` se ejecuta en su propio shell y no afecta al `flutter test`.

**Solución:** Usar `&&` o `;`:

```makefile
test-mobile:
	cd apps/mobile && flutter test

# O mejor, usar working-directory en CI o variables
MOBILE_DIR := apps/mobile
test-mobile:
	cd $(MOBILE_DIR) && flutter test
```
</details>

---

## Ejercicio 3: Añadir un nuevo target

```makefile
# Añade un target "seed" que ejecute el seed.sql de Supabase:
# supabase db reset (para limpiar datos)
# psql -f supabase/seed.sql (para cargar datos de prueba)

# 👇 Implementa el target aquí
.PHONY: seed
seed: db-reset ## Resetear BD y cargar datos de prueba
	@echo "🌱 Cargando datos de prueba..."
	@cd $(SUPABASE_DIR) && psql -f seed.sql
	@echo "${GREEN}✅ Datos de prueba cargados${RESET}"
```

---

## Ejercicio 4: Target con variable condicional

```makefile
# Crea un target "run" que:
# - Si se define DEVICE, ejecuta: flutter run -d $(DEVICE)
# - Si no, ejecuta: flutter run
# - Si DEVICE es "web", ejecuta: flutter run -d chrome

.PHONY: run
run: ## Ejecutar app (usa DEVICE si está definido)
	@if [ "$(DEVICE)" = "web" ]; then \
		cd $(MOBILE_DIR) && flutter run -d chrome; \
	elif [ -n "$(DEVICE)" ]; then \
		cd $(MOBILE_DIR) && flutter run -d $(DEVICE); \
	else \
		cd $(MOBILE_DIR) && flutter run; \
	fi
```

---

## Ejercicio 5: Crear un Makefile desde cero

```dart
// Imagina que empiezas un proyecto Flutter simple (no monorepo).
// Crea un Makefile mínimo con:
// - help (target default)
// - setup (deps + mocks)
// - dev (check + run)
// - check (format + analyze + test)
// - build-apk
// - clean

// Escribe el Makefile completo aquí (mentalmente o en un archivo)
```

<details>
<summary>🔍 Solución propuesta</summary>

```makefile
PROJECT_NAME := mi-app
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "$(PROJECT_NAME) - Comandos"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

.PHONY: setup
setup: deps mocks ## Setup completo

.PHONY: deps
deps: ## Instalar dependencias
	flutter pub get

.PHONY: mocks
mocks: ## Generar código
	dart run build_runner build --delete-conflicting-outputs

.PHONY: dev
dev: check run ## Modo desarrollo

.PHONY: check
check: format analyze test ## Quality gate

.PHONY: format
format: ## Formatear
	dart format .

.PHONY: analyze
analyze: ## Análisis
	flutter analyze

.PHONY: test
test: ## Tests
	flutter test

.PHONY: run
run: ## Ejecutar
	flutter run

.PHONY: build-apk
build-apk: ## Build APK
	flutter build apk --release

.PHONY: clean
clean: ## Limpiar
	flutter clean
	rm -rf coverage/
```
</details>

## Ejercicio 6: Targets cross-module (Git Flow + SemVer)

Crea los siguientes targets en tu Makefile. Cada uno conecta Make con herramientas del módulo 12 (Git Flow + Conventional Commits + SemVer).

**Requisitos previos:**
- Haber instalado commitizen, commitlint y standard-version (módulo 12)
- Tener configurado `npm run commit` y `npm run release` en `package.json`

### 6.1 Target `make commit`

```makefile
.PHONY: commit
commit: ## Crear commit (Conventional Commits via Commitizen)
	@npm run commit
```

**Preguntas:**
1. ¿Qué pasa si el usuario escribe un commit que no cumple el formato?
2. ¿Qué papel juega Husky en este target?

<details>
<summary>🔍 Solución</summary>

1. Husky ejecuta `commit-msg` hook → commitlint rechaza el commit si no cumple el formato (ej: sin tipo, sin descripción, con punto final)
2. Husky ejecuta `pre-commit` hook → lint-staged formatea y analiza el código ANTES de crear el commit

**Flujo completo:**
```
make commit
    → npm run commit (Commitizen formulario)
    → pre-commit hook (lint-staged: dart format + flutter analyze)
    → commit-msg hook (commitlint: valida formato)
    → Commit creado: feat(raffles): agregar filtro
```
</details>

### 6.2 Target `make release`

```makefile
.PHONY: release
release: ## Crear release (SemVer + CHANGELOG auto)
	@npm run release
	@git push --follow-tags
	@echo "${GREEN}✅ Release publicado con tags${RESET}"
```

**Preguntas:**
1. ¿Cómo determina `standard-version` si debe incrementar minor, patch o major?
2. ¿Qué archivos genera `standard-version`?
3. ¿Por qué `--follow-tags` en el push?

<details>
<summary>🔍 Solución</summary>

1. Analiza los commits desde el último tag:
   - Si hay `feat` → incrementa MINOR (1.2.0 → 1.3.0)
   - Si hay solo `fix` → incrementa PATCH (1.2.0 → 1.2.1)
   - Si hay `BREAKING CHANGE` o `!` → incrementa MAJOR (1.2.0 → 2.0.0)

2. Genera:
   - `CHANGELOG.md` (o lo actualiza)
   - Commit: `chore(release): v1.3.0`
   - Tag: `v1.3.0`

3. `--follow-tags` push también los tags a origin (sin esto, solo se push el commit, no el tag)
</details>

### 6.3 Target `make branch`

```makefile
.PHONY: branch
branch: ## Crear rama feature (Conventional Branch)
	@read -p "Nombre de la feature: " name; \
	git checkout develop && \
	git pull && \
	git checkout -b feature/$$name
	@echo "${GREEN}✅ Rama feature/$$name creada desde develop${RESET}"
```

**Preguntas:**
1. ¿Por qué se usa `$$name` en lugar de `$name`?
2. ¿Qué pasaría si no se ejecuta `git pull` antes de crear la rama?

<details>
<summary>🔍 Solución</summary>

1. En Make, `$name` se interpreta como variable de Make (que no existe). `$$name` escapa el `$` y pasa `$name` al shell, que sí lee la variable de `read`

2. Sin `git pull`, la rama se crearía desde un develop desactualizado. Si otros desarrolladores han hecho push a develop, tu rama no tendría esos cambios → conflictos futuros
</details>

### 6.4 Target `make hotfix`

```makefile
.PHONY: hotfix
hotfix: ## Crear rama hotfix
	@read -p "Descripcion del fix: " name; \
	git checkout main && \
	git pull && \
	git checkout -b hotfix/$$name
	@echo "${GREEN}✅ Rama hotfix/$$name creada desde main${RESET}"
```

**Preguntas:**
1. ¿Por qué hotfix se crea desde `main` y no desde `develop`?
2. ¿Cuál es la diferencia entre `make branch` y `make hotfix`?

<details>
<summary>🔍 Solución</summary>

1. Los hotfix corrigen bugs críticos en producción. `main` refleja lo que está en producción, así que el fix se aplica directamente donde está el problema

2. `make branch` → crea desde `develop` (feature/xxx) para funcionalidades nuevas
   `make hotfix` → crea desde `main` (hotfix/xxx) para correcciones urgentes
</details>

### 6.5 Ejercicio completo: Integrar todo

Añade estos targets a tu Makefile y verifica que funcionan:

```makefile
# Verificar que Commitizen está instalado
check-tools:
	@command -v npx >/dev/null 2>&1 || { echo "❌ npx no encontrado"; exit 1; }
	@test -f package.json || { echo "❌ package.json no encontrado"; exit 1; }
	@echo "${GREEN}✅ Herramientas cross-module listas${RESET}"

# Flujo completo: validate → commit
full-commit: validate commit ## Validar código y crear commit
	@echo "${GREEN}✅ Commit creado con validación completa${RESET}"
```

---

## ✅ Checklist

- [ ] Entiendo la sintaxis básica: target, prerequisites, recipe
- [ ] Sé qué es `.PHONY` y por qué es necesario
- [ ] Puedo leer `$(shell ...)` y sé qué hace
- [ ] Entiendo `awk` y `sed` cuando aparecen en un Makefile
- [ ] Sé depurar con `make -n` y `$(info ...)`
- [ ] Puedo añadir un nuevo target
- [ ] Puedo crear un Makefile desde cero
- [ ] Entiendo cómo Make se integra con GitHub Actions

---

## 📚 Referencias

- [GNU | Make manual](https://www.gnu.org/software/make/manual/) — Documentación oficial de GNU Make

---
