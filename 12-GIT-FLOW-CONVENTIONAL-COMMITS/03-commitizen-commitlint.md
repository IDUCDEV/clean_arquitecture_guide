# 03 - Commitizen y commitlint

> Commitizen guía al desarrollador para escribir commits válidos. commitlint los valida automáticamente. Juntos eliminan los mensajes de commit inconsistentes.

---

## 1. Commitizen: CLI Interactivo

Commitizen presenta un formulario interactivo para construir commits válidos.

### 1.1 Instalación

```bash
# Global
npm install -g commitizen

# Local en el proyecto
npm install --save-dev commitizen

# Inicializar con cz-conventional-changelog
npx commitizen init cz-conventional-changelog --save-dev --save-exact
```

### 1.2 Configuración

```json
// package.json
{
  "config": {
    "commitizen": {
      "path": "./node_modules/cz-conventional-changelog"
    }
  }
}
```

### 1.3 Uso

```bash
# En lugar de git commit
npx cz

# O con script en package.json
npm run commit
# package.json: "commit": "cz"
```

### 1.4 Flujo Interactivo

```bash
$ npx cz

? Selecciona el tipo de cambio: (Use arrow keys)
❯ feat:     Una nueva funcionalidad
  fix:      Una corrección de bug
  docs:     Cambios en documentación
  style:    Formato, espacios, puntos y coma
  refactor: Refactorización sin cambios funcionales
  perf:     Mejora de rendimiento
  test:     Agregar o corregir tests
  build:    Cambios en el build system
  ci:       Cambios en CI/CD
  chore:    Tareas de mantenimiento
  revert:   Revertir un commit

? ¿Cuál es el alcance? (ej: auth, payments, raffles)
 raffles

? Escribe una descripción breve (imperativo presente):
 agregar filtro por fecha en lista de rifas

? ¿Hay algún cambio importante?
 No

? ¿Este cambio afecta a algún issue? (opcional)
 Closes #45
```

**Genera:**
```
feat(raffles): agregar filtro por fecha en lista de rifas

Closes #45
```

---

## 2. commitlint: Validador Automático

### 2.1 Instalación

```bash
# Instalar commitlint + config convencional
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

### 2.2 Configuración

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor',
       'perf', 'test', 'build', 'ci', 'chore', 'revert'],
    ],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-case': [2, 'never', ['sentence-case', 'start-case', 'pascal-case']],
    'subject-empty': [2, 'never'],
    'type-empty': [2, 'never'],
    'header-max-length': [2, 'always', 72],
    'scope-empty': [1, 'never'],
    'subject-full-stop': [2, 'never', '.'],
  },
};
```

### 2.3 Reglas Comunes

| Regla | Valor | Descripción |
|-------|-------|-------------|
| `type-enum` | `[2, 'always', [...]]` | Tipos permitidos |
| `type-case` | `[2, 'always', 'lower-case']` | Tipo en minúscula |
| `type-empty` | `[2, 'never']` | Tipo requerido |
| `subject-case` | `[2, 'never', [...]]` | Descripción: sin mayúscula inicial |
| `subject-empty` | `[2, 'never']` | Descripción requerida |
| `subject-full-stop` | `[2, 'never', '.']` | Sin punto final |
| `header-max-length` | `[2, 'always', 72]` | Máximo 72 caracteres |
| `scope-case` | `[2, 'always', 'lower-case']` | Alcance en minúscula |

### 2.4 Integración con Husky

```bash
# .husky/commit-msg
#!/usr/bin/env sh
. "$(dirname "$0")/_/husky.sh"

npx --no -- commitlint --edit $1
```

---

## 3. Adapter Personalizado para Flutter

Para proyectos Flutter con necesidades específicas:

```javascript
// cz-flutter-adapter.js
module.exports = {
  prompter: (cz, commit) => {
    cz.prompt([
      {
        type: 'list',
        name: 'type',
        message: 'Tipo de cambio:',
        choices: [
          { name: 'feat:     Nueva funcionalidad', value: 'feat' },
          { name: 'fix:      Corrección de bug', value: 'fix' },
          { name: 'refactor: Refactorización', value: 'refactor' },
          { name: 'test:     Tests', value: 'test' },
          { name: 'build:    Build system', value: 'build' },
          { name: 'ci:       CI/CD', value: 'ci' },
          { name: 'docs:     Documentación', value: 'docs' },
          { name: 'style:    Formato/código', value: 'style' },
          { name: 'chore:    Mantenimiento', value: 'chore' },
        ],
      },
      {
        type: 'input',
        name: 'scope',
        message: 'Alcance (feature o capa):',
      },
      {
        type: 'input',
        name: 'subject',
        message: 'Descripción breve:',
        validate: (input) => input.length <= 72,
      },
      {
        type: 'confirm',
        name: 'isBreaking',
        message: '¿Breaking change?',
        default: false,
      },
    ]).then((answers) => {
      const scope = answers.scope ? `(${answers.scope})` : '';
      const breaking = answers.isBreaking ? '!' : '';
      commit(`${answers.type}${breaking}${scope}: ${answers.subject}`);
    });
  },
};
```

---

## 4. Standard Version: CHANGELOG Automático

```bash
npm install --save-dev standard-version
```

```json
// package.json
{
  "scripts": {
    "release": "standard-version",
    "release:minor": "standard-version --release-as minor",
    "release:major": "standard-version --release-as major"
  }
}
```

**Uso:**

```bash
# Genera CHANGELOG.md, actualiza versión, crea tag
npm run release
```

**Resultado:**

```markdown
# Changelog

## [1.2.0] - 2026-06-15

### Features
- Exportación de resultados a PDF
- Notificaciones push por sorteo

### Bug Fixes
- Crash al abrir sorteo sin conexión

### Refactoring
- Separar lógica de validación de números
```

### 4.1 Configuración avanzada

```json
// .versionrc
{
  "header": "# Changelog\n\nTodas las versiones notables de este proyecto se documentarán en este archivo.\n",
  "types": [
    { "type": "feat", "section": "Features" },
    { "type": "fix", "section": "Bug Fixes" },
    { "type": "perf", "section": "Performance" },
    { "type": "refactor", "section": "Refactoring" },
    { "type": "docs", "section": "Documentation" },
    { "type": "test", "section": "Tests" },
    { "type": "chore", "hidden": true },
    { "type": "style", "hidden": true }
  ],
  "commitUrlFormat": "{{host}}/{{owner}}/{{repository}}/commit/{{hash}}",
  "compareUrlFormat": "{{host}}/{{owner}}/{{repository}}/compare/{{previousTag}}...{{currentTag}}"
}
```

### 4.2 Flujo completo con standard-version

```bash
# 1. Hacer cambios y commits convencionales
git add .
git commit -m "feat: agregar exportación a PDF"
git commit -m "fix: corregir crash en Android 12"

# 2. Ejecutar release (automático)
npm run release

# Esto hace:
# - Lee los commits desde el último tag
# - Determina el tipo de bump (patch/minor/major)
# - Actualiza package.json
# - Genera/actualiza CHANGELOG.md
# - Crea un commit con los cambios
# - Crea un tag (v1.2.0)

# 3. Push con tags
git push --follow-tags
```

---

## 5. Flujo de Trabajo Completo

```bash
# 1. Hacer cambios en el código

# 2. Staging
git add .

# 3. Commit asistido (husky ejecuta lint-staged + commitlint)
npx cz

# 4. commitlint valida el mensaje
# 5. Si pasa → commit creado
# 6. Si no pasa → error, reintentar
```

---

## 6. Resumen

| Herramienta | Rol | Cuándo se ejecuta |
|-------------|-----|-------------------|
| **Commitizen** | Asistente interactivo | Al escribir el commit |
| **commitlint** | Validador | Hook commit-msg |
| **standard-version** | CHANGELOG + versión | En release |

---

## Recursos

- [Commitizen](http://commitizen.github.io/cz-cli/)
- [commitlint](https://commitlint.js.org/)
- [standard-version](https://github.com/conventional-changelog/standard-version)
- [@commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/@commitlint/config-conventional)

---

## 📚 Referencias

- [Conventional Commits](https://www.conventionalcommits.org/) — Especificación de mensajes de commit
- [Husky](https://typicode.github.io/husky/) — Git hooks modernos para Node.js
- [Commitlint](https://commitlint.js.org/) — Linter para mensajes de commit
- [Git | Documentation](https://git-scm.com/doc) — Documentación oficial de Git
