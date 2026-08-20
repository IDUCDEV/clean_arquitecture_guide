# 02 - Husky + lint-staged

> Automatiza la calidad del código antes de cada commit: ejecuta análisis, tests y formateo solo en los archivos modificados.

---

## 1. ¿Qué es Husky?

Husky ejecuta scripts automáticos en los hooks de Git (pre-commit, pre-push, commit-msg). Ejemplo:

```bash
# Sin Husky: te acuerdas de ejecutar flutter analyze antes de commitear
# Con Husky: se ejecuta automáticamente y te bloquea si falla
```

### 1.1 Instalación

```bash
# Inicializar Husky
npx husky init

# Agregar hook de pre-commit
npx husky add .husky/pre-commit "npx lint-staged"
```

### 1.2 Estructura

```
.husky/
├── pre-commit      # Se ejecuta antes del commit
├── commit-msg      # Valida el mensaje de commit
└── pre-push        # Se ejecuta antes del push
```

### 1.3 Instalación en monorepo

```bash
# En la raíz del monorepo
npx husky init

# Los hooks se comparten para todos los paquetes
# Pero lint-staged puede ejecutar comandos por paquete
```

---

## 2. Hook pre-commit con lint-staged

### 2.1 ¿Qué es lint-staged?

Ejecuta formateo y análisis SOLO en los archivos que están en staging. En lugar de analizar todo el proyecto (~200 archivos), analiza solo los 3-5 archivos modificados.

### 2.2 Configuración para Flutter

```json
// package.json
{
  "lint-staged": {
    "*.dart": [
      "dart format --set-exit-if-changed",
      "flutter analyze --fatal-infos"
    ],
    "*.{json,yaml}": [
      "prettier --check"
    ]
  }
}
```

### 2.3 .husky/pre-commit

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Ejecutar lint-staged solo en archivos staged
npx lint-staged
```

### 2.4 Comportamiento

```bash
# Usuario intenta commitear con código sin formatear
git commit -m "feat: agregar nueva feature"

# Husky ejecuta lint-staged
# lint-staged ejecuta dart format solo en archivos modificados
# Si dart format cambia algo → exit code != 0 → commit BLOQUEADO

# El usuario debe:
# 1. Ejecutar dart format manualmente
# 2. O permitir que lint-staged formatee y re-stage automáticamente
# 3. Re-ejecutar git commit
```

### 2.5 Configuración avanzada con auto-fix

```json
{
  "lint-staged": {
    "*.dart": [
      "dart format",
      "dart analyze --fatal-infos"
    ],
    "*.yaml": [
      "prettier --write"
    ],
    "*.json": [
      "prettier --write"
    ],
    "*.arb": [
      "prettier --write"
    ],
    "*.md": [
      "prettier --write"
    ]
  }
}
```

> **Nota:** Cuando usas `dart format` sin `--set-exit-if-changed`, lint-staged formatea automáticamente y agrega los cambios al staging.

---

## 3. Hook commit-msg

### 3.1 Configuración

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Validar mensaje de commit con commitlint
npx --no -- commitlint --edit $1
```

### 3.2 Comportamiento

```bash
# ❌ Commit inválido
git commit -m "cambios varios"
# ⚠️  commitlint: subject must not be sentence-case

# ✅ Commit válido
git commit -m "feat: agregar paginación en lista de rifas"
# ✔️  commit exitoso
```

### 3.3 Reglas que valida commitlint

| Regla | Descripción | Ejemplo correcto | Ejemplo incorrecto |
|-------|-------------|------------------|-------------------|
| `type-enum` | Tipo permitido | `feat`, `fix`, `docs` | `feature`, `update` |
| `type-empty` | Tipo requerido | `feat: ...` | `: agregar algo` |
| `subject-empty` | Descripción requerida | `feat: algo` | `feat:` |
| `subject-full-stop` | Sin punto final | `feat: algo` | `feat: algo.` |
| `header-max-length` | Máximo 72 chars | `feat: agregar filtro` | `feat: agregar un filtro muy largo que...` |

---

## 4. Hook pre-push

Ejecuta antes de enviar código al remoto. Ideal para tests completos:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Ejecutar tests antes de push
cd apps/mobile
flutter test

# Si falla, el push se cancela
```

### 4.1 Pre-push para monorepo

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Solo ejecutar tests del paquete afectado
CHANGED_FILES=$(git diff --name-only HEAD@{1} HEAD)

if echo "$CHANGED_FILES" | grep -q "^apps/mobile/"; then
  echo "📱 Cambios en mobile - ejecutando tests..."
  cd apps/mobile && flutter test
fi

if echo "$CHANGED_FILES" | grep -q "^packages/"; then
  echo "📦 Cambios en packages - ejecutando tests..."
  cd packages/shared && dart test
fi
```

---

## 5. Configuración en el Proyecto Real

En el monorepo se usa `lint-staged` para mantener calidad consistente:

```bash
.husky/
├── pre-commit          # lint-staged
├── commit-msg          # commitlint
└── .gitignore
```

### 5.1 Anular Hooks

```bash
# Temporalmente (para emergencias)
git commit --no-verify -m "fix: corregir crash crítico"

# Permanente (no recomendado)
git config --unset core.hooksPath
```

---

## 6. lint-staged para Proyectos Flutter

### 6.1 Configuración Completa

```json
{
  "lint-staged": {
    "*.dart": [
      "dart format --set-exit-if-changed",
      "dart analyze --fatal-infos",
      "dart run custom_lint"
    ],
    "*.yaml": [
      "prettier --write"
    ],
    "*.json": [
      "prettier --write"
    ],
    "*.arb": [
      "prettier --write"
    ],
    "*.md": [
      "prettier --write"
    ]
  }
}
```

### 6.2 Monorepo

```json
{
  "lint-staged": {
    "apps/mobile/**/*.dart": [
      "cd apps/mobile && dart format --set-exit-if-changed",
      "cd apps/mobile && flutter analyze --fatal-infos"
    ],
    "apps/web/**/*.{ts,tsx,css}": [
      "cd apps/web && npm run lint:fix"
    ],
    "*.{yaml,json,md}": [
      "prettier --write"
    ]
  }
}
```

### 6.3 Hooks por paquete

```bash
# Si necesitas hooks diferentes por paquete
# usa Husky en la raíz + lint-staged con paths específicos

# Ejemplo: solo formatear dart en apps/mobile
"apps/mobile/**/*.dart": ["dart format"]

# Ejemplo: solo analizar en packages/core
"packages/core/**/*.dart": ["dart analyze"]
```

---

## 7. Troubleshooting

### 7.1 Husky no se ejecuta

```bash
# Verificar que los hooks están instalados
ls -la .husky/

# Reinstalar
npx husky init

# Verificar que el directorio .git/hooks existe
ls -la .git/hooks/
```

### 7.2 lint-staged falla en Windows

```bash
# Husky en Windows requiere git bash
# Configurar en VS Code:
#   "terminal.integrated.shell.windows": "C:\\Program Files\\Git\\bin\\bash.exe"

# O usar WSL
```

### 7.3 lint-staged es muy lento

```bash
# 1. Verificar que solo analiza archivos staged
# 2. Reducir el número de comandos por archivo
# 3. Usar --concurrency para ejecutar en paralelo

# En package.json:
"lint-staged": {
  "*.dart": ["prettier --write", "--concurrency=4"]
}
```

### 7.4 Quiero saltar hooks para un commit específico

```bash
git commit --no-verify -m "fix: hotfix crítico en producción"
```

### 7.5 Hooks se ejecutan en fusiones de rama

```bash
# Si no quieres hooks en merges:
# En .husky/pre-commit:
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Saltar si es un merge
if [ -f "$(git rev-parse --git-dir)/MERGE_HEAD" ]; then
  echo "Skipping hooks during merge"
  exit 0
fi

npx lint-staged
```

---

## 8. Resumen

1. **Husky** ejecuta scripts en hooks de Git
2. **lint-staged** analiza solo archivos modificados (rápido)
3. **pre-commit**: formateo + análisis
4. **commit-msg**: validación de mensaje
5. **pre-push**: tests completos
6. **`--no-verify`** para emergencias
7. **Monorepo**: configurar paths específicos por paquete

---

## Recursos

- [Husky](https://typicode.github.io/husky/)
- [lint-staged](https://github.com/okonet/lint-staged)

---

## 📚 Referencias

- [Conventional Commits](https://www.conventionalcommits.org/) — Especificación de mensajes de commit
- [Husky](https://typicode.github.io/husky/) — Git hooks modernos para Node.js
- [Commitlint](https://commitlint.js.org/) — Linter para mensajes de commit
- [Git | Documentation](https://git-scm.com/doc) — Documentación oficial de Git
