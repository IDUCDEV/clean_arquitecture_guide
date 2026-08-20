# 04 — Análisis del Makefile Real del Proyecto

> Recorrido **línea por línea** de las secciones clave del Makefile del monorepo rifa-gestion-app. Abre el archivo real junto a este documento.

---

## 1. Variables del proyecto

```makefile
MOBILE_DIR := apps/mobile
WEB_DIR := apps/web
SUPABASE_DIR := supabase
```

**¿Por qué?** El proyecto es un monorepo (varias apps en un repo). En lugar de escribir `apps/mobile` cada vez, se usan variables. Si cambia la estructura, solo cambias aquí.

---

## 2. Colores para output

```makefile
BOLD := $(shell tput bold 2>/dev/null)
GREEN := $(shell tput setaf 2 2>/dev/null)
YELLOW := $(shell tput setaf 3 2>/dev/null)
CYAN := $(shell tput setaf 6 2>/dev/null)
RESET := $(shell tput sgr0 2>/dev/null)
```

**¿Por qué?** Para que la salida de `make` sea legible visualmente. `tput` genera códigos de color ANSI. El `2>/dev/null` evita errores si el terminal no soporta colores.

---

## 3. Comandos de desarrollo

```makefile
.PHONY: dev-start
dev-start:
	@cd $(SUPABASE_DIR) && supabase start
```

**¿Qué hace?**
- `.PHONY` → no es un archivo, siempre ejecuta
- `@` → no imprime el comando
- `cd $(SUPABASE_DIR) && supabase start` → entra a la carpeta supabase y ejecuta `supabase start`
- **¿Por qué `cd &&` en vez de `supabase start` directo?** Porque `supabase` busca archivos de configuración en el directorio actual. Debe ejecutarse desde `supabase/`.

```makefile
.PHONY: dev
dev:
	@cd $(MOBILE_DIR) && flutter run --flavor development
```

**¿Por qué `--flavor development`?** El proyecto usa flavors de Flutter (development/production) para diferentes configuraciones de entorno.

---

## 4. Comandos de calidad

```makefile
.PHONY: check
check: format analyze test
```

**¿Qué hace?** Ejecuta 3 targets en orden: format, analyze, test. Si alguno falla, se detiene.

```makefile
.PHONY: format
format:
	@echo "${CYAN}🎨 Formateando código Dart...${RESET}"
	@cd $(MOBILE_DIR) && dart format .
```

**Nota:** Usa `dart format` (no `flutter format`). `dart format` es más rápido y hace lo mismo.

---

## 5. Storage y Edge Functions

```makefile
.PHONY: deploy-storage
deploy-storage:
	@cd $(SUPABASE_DIR) && supabase db push
	@echo "${GREEN}✅ Storage desplegado (bucket raffa-assets + policies)${RESET}"
```

```makefile
.PHONY: deploy-cleanup
deploy-cleanup:
	@cd $(SUPABASE_DIR) && supabase db push
	@cd $(SUPABASE_DIR) && supabase functions deploy raffle-cleanup
	@echo "${YELLOW}📅 Configura el cron trigger (solo una vez):${RESET}"
	@echo "   supabase functions cron create raffle-cleanup --schedule \"0 3 * * *\""
```

**¿Por qué separados?** `deploy-storage` solo despliega migraciones de BD. `deploy-cleanup` además despliega una Edge Function y recuerda configurar el cron. Separación de responsabilidades.

---

## 6. Utilidades de entorno

```makefile
.PHONY: env-local
env-local:
	@sed -i "s|^SUPABASE_URL=.*|SUPABASE_URL=http://127.0.0.1:54321|" apps/mobile/.env; \
	echo "${GREEN}✅ SUPABASE_URL=http://127.0.0.1:54321 (modo local)${RESET}"; \
	echo "📄 SUPABASE_URL=$$(grep ^SUPABASE_URL apps/mobile/.env | cut -d= -f2)"
```

**Análisis línea por línea:**
1. `sed -i "s|...|...|"` → busca y reemplaza SUPABASE_URL en el .env
2. `echo "✅ ..."` → confirma el cambio
3. `grep ^SUPABASE_URL ... | cut -d= -f2` → extrae el nuevo valor y lo muestra (verificación visual)

```makefile
.PHONY: env-usb
env-usb:
	@adb reverse tcp:54321 tcp:54321 && \
	sed -i "s|^SUPABASE_URL=.*|SUPABASE_URL=http://127.0.0.1:54321|" apps/mobile/.env && \
	echo "${GREEN}✅ adb reverse listo + SUPABASE_URL=http://127.0.0.1:54321 (modo USB)${RESET}" || \
	echo "${YELLOW}⚠️  adb reverse falló. ¿El teléfono está conectado por USB?${RESET}"
```

**¿Qué hace `adb reverse`?** Crea un túnel desde el teléfono Android a tu PC. El teléfono puede acceder a `localhost:54321` de tu PC (donde corre Supabase). Esto permite probar en un dispositivo físico.

---

## 7. Conventional Commits

```makefile
.PHONY: commit
commit:
	@npm run commit
```

Delega en commitizen (configurado en package.json). `npm run commit` inicia una UI interactiva para escribir commits con el formato correcto.

**Flujo completo del target `make commit`:**

```
make commit
    │
    ├── 1. npm run commit → ejecuta Commitizen (npx cz)
    │       └── Muestra formulario interactivo:
    │           ? Tipo de cambio: [feat/fix/docs/...]
    │           ? Alcance (opcional):
    │           ? Descripcion:
    │           ? Breaking change:
    │
    ├── 2. Husky ejecuta pre-commit
    │       └── lint-staged → dart format + flutter analyze
    │
    ├── 3. Husky ejecuta commit-msg
    │       └── commitlint → valida formato Conventional Commits
    │
    └── 4. Commit creado: feat(raffles): agregar filtro por fecha
```

**¿Por qué no hacer `git commit -m "..."` directamente?**
- Humanos olvidan el formato correcto
- El alcance (scope) se pierde
- Los breaking changes no se marcan
- El CHANGELOG no se genera automáticamente

### Target: make release

```makefile
.PHONY: release
release: ## Crear release (SemVer + CHANGELOG auto)
	@npm run release
	@git push --follow-tags
	@echo "${GREEN}✅ Release publicado con tags${RESET}"
```

**Flujo:**
1. `standard-version` detecta tipo de cambio desde último tag
2. Incrementa versión según SemVer 2.0.0 (feat→minor, fix→patch, breaking→major)
3. Genera/actualiza `CHANGELOG.md`
4. Crea commit `chore(release): vX.Y.Z`
5. Crea tag `vX.Y.Z`
6. Push con tags a origin

```bash
# Ejemplo:
# Version actual: v1.2.0
# Si hay feat desde el último tag:
make release
# → v1.2.0 → v1.3.0
# → CHANGELOG.md actualizado
# → Tag v1.3.0 creado
```

---

## 📊 Mapa de dependencias entre targets

```
help               → (autónomo)
setup              → deps → mocks
dev                → check → run
dev-start          → supabase-up → dev
dev-stop           → supabase-down
check              → format → analyze → test
validate           → check ✓
build-apk          → env-prod-check ✓
deploy-storage     → supabase db push
deploy-cleanup     → deploy-storage + functions deploy
```

---

## 📚 Referencias

- [GNU | Make manual](https://www.gnu.org/software/make/manual/) — Documentación oficial de GNU Make

---

**Siguiente**: [05-creacion-personalizada.md](./05-creacion-personalizada.md) — Crear Makefiles desde cero
