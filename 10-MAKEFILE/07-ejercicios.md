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
