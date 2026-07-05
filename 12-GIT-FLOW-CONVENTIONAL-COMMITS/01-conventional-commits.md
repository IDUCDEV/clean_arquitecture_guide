# 01 - Conventional Commits

> Un estándar ligero para mensajes de commit que permite generar CHANGELOGs y versionado semántico automático.

---

## 1. ¿Qué es Conventional Commits?

```
<tipo>(<alcance opcional>): <descripción breve>

<cuerpo opcional>

<pie opcional con breaking changes o issues>
```

### Ejemplos

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

---

## 2. Tipos de Commit

### Tipos Principales

| Tipo | Descripción | Versión |
|------|-------------|---------|
| `feat` | Nueva funcionalidad | Minor |
| `fix` | Corrección de bug | Patch |
| `BREAKING CHANGE` | Cambio incompatible | Major |

### Tipos Adicionales

| Tipo | Cuándo Usar | Ejemplo |
|------|-------------|---------|
| `build` | Cambios en build system | `build: upgrade gradle a 8.0` |
| `chore` | Tareas de mantenimiento | `chore: limpiar dependencias no usadas` |
| `ci` | Cambios en CI/CD | `ci: agregar step de codegen en pipeline` |
| `docs` | Documentación | `docs: actualizar README con setup` |
| `perf` | Mejora de rendimiento | `perf: cachear consultas de catálogo` |
| `refactor` | Refactorización | `refactor: extraer widget de tarjeta` |
| `revert` | Revertir commit | `revert: feat: agregar suscripción` |
| `style` | Formato/estilo | `style: aplicar dart format` |
| `test` | Tests | `test: cubrir caso de sorteo sin boletos` |

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

---

## 4. Breaking Changes

Señalan que el commit requiere cambios en el código existente:

```bash
# Opción 1: ! después del tipo
refactor!(auth): cambiar respuesta de login a JWT

# Opción 2: BREAKING CHANGE en el pie
feat: migrar de SQLite a Isar

BREAKING CHANGE: Se eliminó la base de datos local anterior.
Los usuarios deben sincronizar sus datos nuevamente.
```

---

## 5. Integración con Versionado Semántico

```
1.2.3 → 1.2.4 (patch) → fix
1.2.0 → 1.3.0 (minor) → feat
1.0.0 → 2.0.0 (major) → BREAKING CHANGE
```

### Ejemplo de CHANGELOG Generado

```markdown
# Changelog

## 2.1.0 (2026-06-15)

### Features
- Exportación de resultados a PDF
- Notificaciones push por sorteo

### Bug Fixes
- Crash al abrir sorteo sin conexión
- Cálculo incorrecto de premios compartidos

### Refactoring
- Separar lógica de validación de números
```

---

## 6. Gitmoji (Opcional)

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

---

## 7. Convenciones en el Proyecto Real

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

## 8. Resumen

1. **`<tipo>(alcance): descripción`** es el formato estándar
2. **`feat`** y **`fix`** son los tipos principales
3. **`BREAKING CHANGE`** señala cambios incompatibles
4. **Alcance** ayuda a identificar la feature afectada
5. **Commitlint** valida automáticamente cada commit
6. **Gitmoji** es opcional pero visualmente útil

---

## Recursos

- [Conventional Commits especificación](https://www.conventionalcommits.org/)
- [Gitmoji](https://gitmoji.dev/)
- [Semantic Versioning](https://semver.org/)

---

## 📚 Referencias

- [Conventional Commits](https://www.conventionalcommits.org/) — Especificación de mensajes de commit
- [Husky](https://typicode.github.io/husky/) — Git hooks modernos para Node.js
- [Commitlint](https://commitlint.js.org/) — Linter para mensajes de commit
- [Git | Documentation](https://git-scm.com/doc) — Documentación oficial de Git

---
