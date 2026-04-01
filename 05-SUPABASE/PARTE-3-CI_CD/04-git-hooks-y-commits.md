# 04 - Git Hooks y Commits

> Aprende a configurar git hooks y conventional commits para mantener un historial limpio y automatizado.

---

## 1. Conventional Commits

### Formato

```
<tipo>(<alcance>): <descripción>

[opcional: cuerpo]
[opcional: pie]
```

### Tipos válidos

| Tipo | Descripción |
|------|-------------|
| `feat` | Nueva feature |
| `fix` | Bug fix |
| `docs` | Documentación |
| `style` | Formateo |
| `refactor` | Refactorización |
| `perf` | Performance |
| `test` | Tests |
| `build` | Build/CI/CD |
| `ci` | Changes a CI |
| `chore` | Mantenimiento |
| `revert` | Revertir commit |

### Ejemplos

```bash
git commit -m "feat(auth): add login with Google"
git commit -m "fix(ui): fix button not responding"
git commit -m "docs: update README"
```

---

## 2. Instalar commitlint

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

### commitlint.config.js

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert']]
  }
};
```

---

## 3. Git Hooks con Makefile

```makefile
.PHONY: git-hooks
git-hooks:
	@echo "==> Instalando git hooks..."
	@mkdir -p .git/hooks
	@echo '#!/bin/bash\nmake check' > .git/hooks/pre-commit
	@chmod +x .git/hooks/pre-commit
```

---

## 4. Husky (opcional)

```bash
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "make check"
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit ${1}'
```

---

## 5. CI/CD Enforcement

```yaml
# .github/workflows/commitlint.yml
name: CI - Commit Lint
on: push

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: wagoid/commitlint-github-action@v5
```

---

## 6. Resumen

| Herramienta | Propósito |
|-------------|-----------|
| commitlint | Validar mensajes de commit |
| husky | Manejar git hooks |
| conventional commits | Formato estándar |
| Makefile git-hooks | Pre-commit checks |

---

**Fin de la Guía de Supabase**  
**[Volver al inicio](../../README.md)**