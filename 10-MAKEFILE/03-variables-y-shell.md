# 03 — Variables Avanzadas y Funciones Shell

---

## 1. `$(shell ...)` — Ejecutar comandos

La función más poderosa: ejecuta un comando de shell y usa su salida como valor.

```makefile
# Detectar Flutter (FVM o global)
FLUTTER := $(shell [ -d .fvm ] && echo fvm flutter || echo flutter)

# Detectar dispositivo Android conectado
DEFAULT_ANDROID = $(shell flutter devices 2>/dev/null \
	| awk -F "•" '/android/ {gsub(/ /,"",$$2); print $$2; exit}')

# Obtener IP local
LOCAL_IP := $(shell ip -4 addr show \
	| grep -oP '(?<=inet\s)\d+\.\d+\.\d+\.\d+' \
	| grep -v '127.0.0.1' \
	| head -1)
```

### ¿Cómo leer esto?

```makefile
# 1. [ -d .fvm ] → prueba si existe la carpeta .fvm
# 2. && echo "fvm flutter" → si existe, retorna "fvm flutter"
# 3. || echo "flutter" → si no existe, retorna "flutter"
# 4. $(shell ...) → asigna el resultado a la variable FLUTTER
FLUTTER := $(shell [ -d .fvm ] && echo fvm flutter || command -v flutter 2>/dev/null || echo flutter)
```

---

## 2. Variables automáticas

```makefile
all: file1.txt file2.txt
	@echo "Target: $@"    # "all"
	@echo "Primer: $<"    # "file1.txt"
	@echo "Todos: $^"     # "file1.txt file2.txt"
	@echo "Ruta: $(@D)"   # "." (directorio del target)
	@echo "Arch: $(@F)"   # "all" (archivo del target)
```

| Variable | Significado |
|----------|-------------|
| `$@` | Nombre del target actual |
| `$<` | Primer prerequisito |
| `$^` | Todos los prerequisitos |
| `$?` | Prerequisitos más nuevos que el target |
| `$(@D)` | Directorio del target |
| `$(@F)` | Archivo del target |

---

## 3. Condicionales

```makefile
# Ejecutar según condiciones
run:
	$(if $(DEVICE),\
		flutter run -d $(DEVICE),\
		flutter run\
	)

# Verificar herramientas
deps-check:
	@command -v docker >/dev/null 2>&1 \
		|| { echo "❌ Docker no instalado"; exit 1; }
	@command -v supabase >/dev/null 2>&1 \
		|| { echo "❌ Supabase CLI no instalado"; exit 1; }
```

---

## 4. `awk` y `sed` en el Makefile

Estos comandos aparecen frecuentemente. Aquí lo que necesitas saber:

### `awk -F "•" '/android/ {gsub(/ /,"",$$2); print $$2; exit}'`

```bash
# Entrada: salida de "flutter devices"
# 2 connected devices:
# Pixel 6 (mobile) • 192.168.1.5 • android-arm64  • Android 14
# sdk gphone (mobile) • emulator-5554 • android-x64 • Android 14

# -F "•"         → separador es " • "
# /android/      → solo líneas con "android"
# gsub(/ /,"")   → quita espacios
# print $$2      → imprime el segundo campo (la IP/ID)
# exit           → solo el primero
```

### `sed -i "s|^SUPABASE_URL=.*|SUPABASE_URL=http://$IP:54321|" .env`

```bash
# s|regex|reemplazo| → substitución
# ^SUPABASE_URL=.*   → línea que empieza con SUPABASE_URL=
# SUPABASE_URL=http://$IP:54321 → nuevo valor
# -i                 → editar in-place (modificar el archivo)
```

---

## 5. Debugging

```makefile
# Imprimir el valor de una variable (útil para depurar)
$(info FLUTTER = $(FLUTTER))
$(warning CUIDADO: dispositivo no encontrado)
$(error ERROR: Flutter no instalado)
```

```bash
# Ejecutar make sin ejecutar (solo muestra lo que haría)
make -n [target]

# Ejecutar mostrando todos los comandos (sin @)
make [target]  # normalmente los comandos con @ no se muestran
```

---

## 🏋️ Mini-ejercicio

```makefile
# ¿Qué hace esta línea?
DEFAULT_ANDROID = $(shell flutter devices 2>/dev/null | awk -F "•" '/android/ {gsub(/ /,"",$$2); print $$2; exit}')

# 1. ¿Por qué 2>/dev/null?
# 2. ¿Qué hace awk -F "•"?
# 3. ¿Qué hace gsub(/ /,"")?
# 4. ¿Por qué $$2 y no $2?
```

<details>
<summary>🔍 Solución</summary>

1. `2>/dev/null` → descarta errores (si no hay flutter, no muestra error feo)
2. `-F "•"` → usa "•" como separador de campos
3. `gsub(/ /,"")` → elimina espacios alrededor del campo
4. `$$2` → en Make, `$2` sería interpretado como variable de Make. `$$2` escapa el `$` y pasa `$2` al shell (que sí es el segundo campo de awk)
</details>

---

## 📚 Referencias

- [GNU | Make manual](https://www.gnu.org/software/make/manual/) — Documentación oficial de GNU Make

---

**Siguiente**: [04-analisis-makefile-real.md](./04-analisis-makefile-real.md) — Análisis del Makefile del proyecto
