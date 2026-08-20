# 01 - Conventional Commits

> Un estándar ligero para mensajes de commit que permite generar CHANGELOGs y versionado semántico automático.

---

## 1. ¿Qué es Conventional Commits?

Conventional Commits es una especificación (v1.0.0) que添加 un conjunto de reglas simples para crear un historial de commits explícito. Esto hace más fácil escribir herramientas automatizadas encima del historial.

### Formato del mensaje

```
<tipo>[<ámbito opcional>][<! opcional>]: <descripción>

[cuerpo opcional]

[nota(s) al pie opcional(es)]
```

### Elementos estructurales

| Elemento | Descripción | Relación SemVer |
|----------|-------------|-----------------|
| `fix` | Corrige un error en la base del código | **PATCH** |
| `feat` | Introduce una nueva funcionalidad | **MINOR** |
| `BREAKING CHANGE` | Cambio incompatible con versiones anteriores | **MAJOR** |

### Ejemplos reales en Flutter

```
feat: agregar sistema de suscripción a resultados de rifas

Implementa notificaciones push cuando un número resulta ganador.
Se usa Firebase Cloud Messaging con topics por sorteo.

Closes #123
```

```
feat(auth): agregar login con huella digital

BREAKING CHANGE: Se eliminó el login con PIN.
Los usuarios deben migrar a biometría.
```

```
fix: corregir cálculo de premio cuando hay múltiples ganadores

El porcentaje se dividía por el total de boletos en lugar de
solo los boletos ganadores.
```

```
docs(api): actualizar endpoints de pagos en la documentación
```

```
refactor(raffles): extraer lógica de validación de números

Se movió la validación a un helper separado para reutilizarlo
en la pantalla de compra y la de resultados.
```

```
feat!: cambiar API de pagos a versión v2

BREAKING CHANGE: Los endpoints de pagos v1 serán eliminados en 3 meses.
Los clientes deben migrar a /api/v2/payments.
```

---

## 2. Tipos de Commit

### Tipos Principales

| Tipo | Descripción | Versión | Cuándo usar |
|------|-------------|---------|-------------|
| `feat` | Nueva funcionalidad | Minor | Cuando agregas algo nuevo al proyecto |
| `fix` | Corrección de bug | Patch | Cuando corriges un error existente |
| `BREAKING CHANGE` | Cambio incompatible | Major | Cuando modificas el API de forma no retrocompatible |

### Tipos Adicionales (según @commitlint/config-conventional)

| Tipo | Cuándo Usar | Ejemplo en Flutter |
|------|-------------|-------------------|
| `build` | Cambios en build system | `build: upgrade gradle a 8.0` |
| `chore` | Tareas de mantenimiento | `chore: limpiar dependencias no usadas` |
| `ci` | Cambios en CI/CD | `ci: agregar step de codegen en pipeline` |
| `docs` | Documentación | `docs: actualizar README con setup` |
| `perf` | Mejora de rendimiento | `perf: cachear consultas de catálogo` |
| `refactor` | Refactorización sin cambio funcional | `refactor: extraer widget de tarjeta` |
| `revert` | Revertir un commit | `revert: feat: agregar suscripción` |
| `style` | Formato/estilo (sin cambio de lógica) | `style: aplicar dart format` |
| `test` | Agregar o corregir tests | `test: cubrir caso de sorteo sin boletos` |

### Relación con Versionado Semántico

```
1.2.3 → 1.2.4 (patch) → fix
1.2.0 → 1.3.0 (minor) → feat
1.0.0 → 2.0.0 (major) → BREAKING CHANGE
```

> **Nota:** Los tipos adicionales (chore, ci, docs, etc.) NO afectan el versionado semántico a menos que incluyan un BREAKING CHANGE.

---

## 3. Reglas de Oro

### 3.1 Descripción

```bash
# ✅ Buenos
feat: agregar generación de PDF de resultados
fix: corregir crash al abrir sorteo sin conexión
refactor(auth): simplificar flujo de recuperación

# ❌ Malos
feat: cambios varios
fix: bug
refactor: mejorar código
chore: cositas
```

**Reglas:**
- Imperativo presente ("agregar", no "agregué" ni "agrega")
- Sin punto final
- Máximo 72 caracteres
- Primera letra minúscula

### 3.2 Alcance

El alcance es opcional pero recomendado para proyectos grandes:

```bash
# Sin alcance
feat: agregar exportación a Excel

# Con alcance (feature específica)
feat(raffles): agregar exportación de resultados a Excel
feat(payments): integrar Mercado Pago
feat(auth): agregar verificación en dos pasos

# Comunicar a capa específica
feat(api): nuevo endpoint de estadísticas
feat(ui): rediseñar tarjeta de sorteo
feat(db): migración a Isar v3
```

### 3.3 Ámbito en el proyecto real

En un monorepo Flutter, el ámbito puede indicar:
- **Feature:** `feat(raffles): ...`
- **Capa:** `feat(api): ...`, `feat(ui): ...`
- **Paquete:** `feat(mobile): ...`, `feat(web): ...`

---

## 4. Breaking Changes

Los BREAKING CHANGE signaling que el commit requiere cambios en el código existente que pueden romper compatibilidad.

### Opción 1: `!` después del tipo/ámbito

```bash
refactor!(auth): cambiar respuesta de login a JWT
feat!(payments): migrar de REST a GraphQL
```

### Opción 2: `BREAKING CHANGE` en la nota al pie

```bash
feat: migrar de SQLite a Isar

BREAKING CHANGE: Se eliminó la base de datos local anterior.
Los usuarios deben sincronizar sus datos nuevamente.
```

### Opción 3: Ambos

```bash
refactor!: drop support for Node 6

BREAKING CHANGE: refactor to use JavaScript features not available in Node 6.
```

### Reglas de la especificación

1. Los cambios de ruptura DEBEN ser indicados en el prefijo de tipo/ámbito, o como una nota al pie
2. Si se incluye como nota al pie, DEBE usar `BREAKING CHANGE:` en mayúsculas
3. Si se usa `!`, `BREAKING CHANGE:` PUEDE ser omitido de la nota al pie
4. `BREAKING-CHANGE` DEBE ser sinónimo de `BREAKING CHANGE`

---

## 5. Notas al Pie (Footer)

Las notas al pie permiten asociar commits con issues o agregar metadatos:

```bash
# Referenciar issues
fix: corregir crash en Android 12

Closes #456
Fixes #789

# Referenciar otros commits
revert: feat: agregar suscripción

Refs: 676104e, a215868

# Reviewed-by (usado en flujos con code review)
fix: correct minor typos in code

Reviewed-by: Z
Refs #133
```

### Reglas

- Cada nota al pie DEBE consistir de una palabra clave seguida de `:<espacio>` o `<espacio>#`
- La palabra clave DEBE usar `-` en lugar de espacios (ej: `Acked-by`)
- Se permite `BREAKING CHANGE` como excepción

---

## 6. Integración con Versionado Semántico

### CHANGELOG generado automáticamente

```markdown
# Changelog

## [2.1.0] - 2026-06-15

### Features
- Exportación de resultados a PDF
- Notificaciones push por sorteo

### Bug Fixes
- Crash al abrir sorteo sin conexión
- Cálculo incorrecto de premios compartidos

### Refactoring
- Separar lógica de validación de números
```

### Cómo se determina la versión

| Commit | Tipo | Versión |
|--------|------|---------|
| `fix: corregir crash` | fix | patch (1.0.0 → 1.0.1) |
| `feat: agregar filtro` | feat | minor (1.0.1 → 1.1.0) |
| `feat!: cambiar API` | BREAKING | major (1.1.0 → 2.0.0) |

---

## 7. Gitmoji (Opcional)

Gitmoji añade emojis a los commits para identificarlos visualmente:

```bash
✨ feat: agregar nuevo diseño de tarjeta
🐛 fix: corregir crash en Android 12
📝 docs: actualizar guía de instalación
♻️ refactor: extraer lógica de pagos
✅ test: agregar tests de integración
🚀 ci: optimizar pipeline de release
💄 style: rediseñar pantalla de perfil
🔧 chore: actualizar dependencias
```

**Ventaja:** Identificación visual rápida en logs.
**Desventaja:** No es compatible con parseo automático en CI/CD.

> **Recomendación:** Si usas Gitmoji, no lo combines con commitlint estricto, ya que el emoji no es parseable.

---

## 8. Convenciones en el Proyecto Real

En el monorepo se usa `@commitlint/config-conventional`:

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'perf',
       'test', 'build', 'ci', 'chore', 'revert'],
    ],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-case': [2, 'never', ['sentence-case', 'start-case']],
    'subject-empty': [2, 'never'],
    'type-empty': [2, 'never'],
    'header-max-length': [2, 'always', 72],
  },
};
```

---

## 9. Preguntas Frecuentes (FAQ)

### ¿Cómo trabajar en desarrollo inicial?
Recomienda trabajar como si ya hubieras lanzado. Alguien está usando tu software y querrá saber qué se arregló, qué se dañó, etc.

### ¿Mayúsculas o minúsculas en los tipos?
Se puede usar cualquiera, pero sé coherente. La especificación recomienda minúsculas.

### ¿Qué hago si un commit aplica a varios tipos?
Haz múltiples commits. Parte del beneficio es mantener el historial organizado.

### ¿Desalienta el desarrollo rápido?
Desalienta el desarrollo rápido desorganizado. Te ayuda a moverte rápido a largo plazo.

### ¿Cómo se relaciona con SemVer?
- `fix` → PATCH
- `feat` → MINOR
- `BREAKING CHANGE` (cualquier tipo) → MAJOR

### ¿Qué pasa si uso un tipo equivocado?
Si es un tipo de la especificación pero equivocado (ej: `fix` en vez de `feat`), usa `git rebase -i` antes de combinar. Si es un tipo no especificado (ej: `feet`), será ignorado por las herramientas.

### ¿Cómo manejar reverts?
```bash
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

---

## 10. Resumen

1. **`<tipo>(ámbito): descripción`** es el formato estándar
2. **`feat`** y **`fix`** son los tipos principales
3. **`BREAKING CHANGE`** señala cambios incompatibles (usa `!` o nota al pie)
4. **Ámbito** ayuda a identificar la feature/capa afectada
5. **Commitlint** valida automáticamente cada commit
6. **Gitmoji** es opcional pero visualmente útil
7. **Relación con SemVer:** fix→patch, feat→minor, breaking→major

---

## Recursos

- [Conventional Commits especificación](https://www.conventionalcommits.org/)
- [Gitmoji](https://gitmoji.dev/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Branch](https://github.com/debitoor/conventional-branch)

---

## 📚 Referencias

- [Conventional Commits](https://www.conventionalcommits.org/) — Especificación de mensajes de commit
- [Husky](https://typicode.github.io/husky/) — Git hooks modernos para Node.js
- [Commitlint](https://commitlint.js.org/) — Linter para mensajes de commit
- [Git | Documentation](https://git-scm.com/doc) — Documentación oficial de Git
