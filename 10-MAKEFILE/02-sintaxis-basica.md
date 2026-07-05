# 02 — Sintaxis Básica de Makefile

---

## 1. Estructura de una regla

```makefile
target: prerequisites
	recipe
```

| Parte | Qué es | Ejemplo |
|-------|--------|---------|
| **target** | El nombre del comando | `test:` |
| **prerequisites** | Lo que debe ejecutarse antes | `format analyze` |
| **recipe** | Lo que realmente hace (indentado con TAB) | `flutter test` |

### Ejemplo real:

```makefile
check: format analyze test
	@echo "✅ Todo listo!"
```

Ejecutar `make check` hará:
1. Ejecutar `make format`
2. Ejecutar `make analyze`
3. Ejecutar `make test`
4. Ejecutar `echo "✅ Todo listo!"`

---

## 2. `.PHONY` — La regla más importante

```makefile
.PHONY: test clean setup
```

**¿Por qué es necesaria?** Make asume que cada target es un **archivo**. Si existiera un archivo llamado `test` en el proyecto, Make diría "test ya está actualizado" y no ejecutaría nada.

`.PHONY` le dice a Make: "esto no es un archivo, siempre ejecútalo".

> **💡 Regla**: TODO target que no genere un archivo debe ser `.PHONY`.

---

## 3. Variables

```makefile
# Asignación simple (= evaluación perezosa)
PROJECT_NAME = mi-proyecto

# Asignación inmediata (:= evaluación al momento)
MOBILE_DIR := apps/mobile

# Asignación condicional (?= solo si no está definida)
DEVICE ?= emulator-5554

# Uso
deploy:
	@echo "Desplegando $(PROJECT_NAME)"
	@cd $(MOBILE_DIR) && flutter build apk
```

### ¿`=` vs `:=`?

```makefile
# = evaluación perezosa (cada vez que se usa, se evalúa)
DATE = $(shell date)
# := evaluación inmediata (se evalúa una sola vez)
DATE2 := $(shell date)

all:
	@echo $(DATE)   # fecha actual
	@sleep 2
	@echo $(DATE)   # fecha distinta (se re-evaluó)
	@echo $(DATE2)  # misma fecha (se evaluó al definir)
```

---

## 4. El `@` — Silenciar comandos

```makefile
test:
	@echo "🧪 Ejecutando tests..."
	flutter test
```

Sin `@`, Make imprime el comando antes de ejecutarlo:

```bash
$ make test
echo "🧪 Ejecutando tests..."
🧪 Ejecutando tests...
flutter test   # y aquí empiezan los tests
```

Con `@`:

```bash
$ make test
🧪 Ejecutando tests...
# (solo se ve la salida del comando)
```

---

## 5. Target por defecto

```makefile
.DEFAULT_GOAL := help
```

Cuando ejecutas solo `make` (sin target), ejecuta `help`. Así siempre ves la lista de comandos disponibles.

---

## 6. Comentarios

```makefile
# Esto es un comentario (línea completa)

clean: ## Limpiar artifacts (comentario inline visible en help)
	rm -rf build/
```

Los comentarios con `##` (doble) son usados por el target `help` para generar la documentación:

```makefile
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "  %-25s %s\n", $$1, $$2}'
```

---

## 🏋️ Mini-ejercicio

```makefile
# Dado este Makefile:
.PHONY: saludar despedir
.DEFAULT_GOAL := saludar

NAME := Mundo

saludar: despedir
	@echo "¡Hola $(NAME)!"

despedir:
	@echo "Adiós $(NAME)!"
```

**Preguntas:**
1. ¿Qué pasa si ejecuto `make`?
2. ¿Qué pasa si ejecuto `make saludar`?
3. ¿Qué pasa si ejecuto `make despedir`?

<details>
<summary>🔍 Solución</summary>

1. `make` → ejecuta `saludar` (target default). Pero `saludar` requiere `despedir`, así que: `Adiós Mundo!` → `¡Hola Mundo!`
2. `make saludar` → igual que arriba (despedir se ejecuta como prerequisito)
3. `make despedir` → solo `Adiós Mundo!`
</details>

---

## 📚 Referencias

- [GNU | Make manual](https://www.gnu.org/software/make/manual/) — Documentación oficial de GNU Make

---

**Siguiente**: [03-variables-y-shell.md](./03-variables-y-shell.md) — Variables avanzadas y funciones shell
