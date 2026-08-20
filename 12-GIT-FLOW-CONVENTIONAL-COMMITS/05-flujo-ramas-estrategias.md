# 05 - Estrategias de Ramas y Releases

> Define cómo organizar el trabajo en equipo: qué ramas existen, cómo se integran, y cómo se hacen los releases. Basado en la especificación Conventional Branch.

---

## 1. Conventional Branch

Conventional Branch es una especificación para agregar significado legible por humanos y máquinas a las ramas Git. Basada en la [especificación oficial](https://github.com/debitoor/conventional-branch).

### 1.1 Formato

```
<tipo>/<descripción>
```

### 1.2 Prefijos estándar

| Prefijo | Propósito | Ejemplo |
|---------|-----------|---------|
| `main` / `master` | Rama principal de desarrollo | `main` |
| `feature/` o `feat/` | Nuevas funcionalidades | `feature/agregar-login` |
| `bugfix/` o `fix/` | Corregir errores | `bugfix/corregir-crash-pagos` |
| `hotfix/` | Correcciones urgentes | `hotfix/parche-seguridad` |
| `release/` | Preparar una liberación | `release/v1.2.0` |
| `chore/` | Tareas sin código (docs, deps) | `chore/actualizar-dependencias` |

### 1.3 Reglas de nomenclatura

1. **Alfanuméricos, guiones y puntos en minúsculas:** Usar siempre letras minúsculas (az), números (0-9) y guiones (-) para separar palabras
2. **Sin guiones o puntos consecutivos:** No usar `feature/nuevo--login` ni `release/v1.-2.0`
3. **Sin guiones/puntos al inicio o final:** No usar `feature/-nuevo-login` ni `release/v1.2.0.`
4. **Claro y conciso:** El nombre debe ser descriptivo pero breve
5. **Incluir números de ticket:** Si aplica, incluir el número de ticket para seguimiento

### 1.4 Ejemplos

```bash
# ✅ Buenos
feature/agregar-pagina-login
bugfix/corregir-encabezado-error
hotfix/parche-seguridad
release/v1.2.0
chore/actualizar-dependencias

# ❌ Malos
Feature/Nuevo-Login         # Mayúsculas
feature/nuevo__login        # Guiones dobles
feature/nuevo-login.        # Punto al final
hotfix/                     # Sin descripción
```

---

## 2. Git Flow vs GitHub Flow

| Aspecto | Git Flow | GitHub Flow |
|---------|----------|-------------|
| Ramas | `main`, `develop`, `feature/*`, `release/*`, `hotfix/*` | `main`, `feature/*` |
| Complejidad | Alta | Baja |
| Releases | Programados | Continuos |
| Equipo | 5+ personas | 1-3 personas |
| Proyecto | App con versiones semánticas | Web/API con deploys continuos |

**Para apps Flutter:** Git Flow (o una versión simplificada) es más adecuado porque:
- Los releases son versionados (1.0.0, 1.1.0, 2.0.0)
- App stores requieren builds específicos
- Las features pueden tardar semanas en completarse

---

## 3. Git Flow Simplificado

### 3.1 Estructura de Ramas

```
main ──── M1 ────────── M2 ────────── M3 (producción)
          │              │              │
develop ─ D1 ─ D2 ─ D3 ─ D4 ─ D5 ─ D6 ─ D7 (integración)
          │    │    │         │         │
feature/  │    │    └─ feat1   │         └─ feat3
          │    └─ feat2        │
          │                    └─ feat4
          │
hotfix/   └────────────────── H1 (emergencia)
```

### 3.2 Convención de Nombres (Conventional Branch)

```bash
# Features
feature/descripcion-corta
feature/agregar-filtro-rifas
feature/exportar-pdf-resultados

# Hotfixes (desde main)
hotfix/descripcion-corta
hotfix/corregir-crash-pagos

# Releases
release/version
release/1.2.0

# Bugfixes (desde develop)
bugfix/descripcion-corta
bugfix/calculo-premios

# Chores
chore/descripcion
chore/actualizar-dependencias
```

---

## 4. Flujo de Trabajo

### 4.1 Nueva Feature

```bash
# 1. Crear rama desde develop
git checkout develop
git pull
git checkout -b feature/agregar-filtro-rifas

# 2. Trabajar en la feature
# ... commits ...
git add .
git commit -m "feat(raffles): agregar filtro por fecha"

# 3. Mantener actualizada con develop
git fetch origin
git rebase origin/develop

# 4. Crear PR a develop
# ... revisión de código ...

# 5. Merge a develop
git checkout develop
git merge feature/agregar-filtro-rifas
```

### 4.2 Release

```bash
# 1. Crear rama de release desde develop
git checkout develop
git pull
git checkout -b release/1.2.0

# 2. Ajustes finales (solo fixes)
git commit -m "fix: corregir texto en pantalla de pago"

# 3. Merge a main (con tag)
git checkout main
git merge release/1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags

# 4. Merge de vuelta a develop
git checkout develop
git merge release/1.2.0

# 5. Eliminar rama de release
git branch -d release/1.2.0
```

### 4.3 Hotfix

```bash
# 1. Crear desde main
git checkout main
git pull
git checkout -b hotfix/corregir-crash-pagos

# 2. Fix
git commit -m "fix(payments): corregir crash al procesar pago"

# 3. Merge a main
git checkout main
git merge hotfix/corregir-crash-pagos
git tag -a v1.2.1 -m "Hotfix v1.2.1"

# 4. Merge a develop también
git checkout develop
git merge hotfix/corregir-crash-pagos
```

---

## 5. Pull Requests y Code Review

### 5.1 Template de PR

```markdown
## Descripción
<!-- Qué hace este PR -->

## Cambios
- [x] Nueva feature: filtro por fecha en lista de rifas
- [x] Tests unitarios agregados
- [ ] Documentación actualizada

## Screenshots
<!-- Si aplica -->

## Testing
- [x] Unit tests
- [x] Widget tests
- [x] Prueba manual en Android
- [ ] Prueba manual en iOS

## Checklist
- [x] Código sigue el estilo del proyecto
- [x] No hay warnings de análisis
- [x] Tests pasan
```

### 5.2 Reglas de Code Review

| Qué revisar | Por qué |
|-------------|---------|
| Lógica de negocio | ¿Resuelve el problema correcto? |
| Manejo de errores | ¿Qué pasa si la API falla? |
| Tests | ¿Cubren casos borde? |
| Nombres | ¿Son claros y consistentes? |
| Side effects | ¿Afecta otras features? |

---

## 6. Versionado Semántico

### 6.1 Esquema (SemVer 2.0.0)

```
v<major>.<minor>.<patch>

v1.0.0  → Primer release estable
v1.1.0  → Nueva feature
v1.1.1  → Bug fix
v2.0.0  → Breaking change
```

### 6.2 Reglas de incremento

| Versión | Cuándo incrementar | Ejemplo |
|---------|-------------------|---------|
| **Major (X)** | Cambios incompatibles con API anterior | `1.0.0` → `2.0.0` |
| **Minor (Y)** | Nueva funcionalidad compatible | `1.0.0` → `1.1.0` |
| **Patch (Z)** | Corrección de bug compatible | `1.1.0` → `1.1.1` |

### 6.3 Tags en Git

```bash
# Annotated tag (recomendado)
git tag -a v1.2.0 -m "Release v1.2.0: Exportación PDF"

# Lightweight tag (simple)
git tag v1.2.0

# Push tags
git push origin --tags
```

### 6.4 Versiones de pre-lanzamiento

```bash
# Formato: v<major>.<minor>.<patch>-<identificador>
v1.0.0-alpha
v1.0.0-alpha.1
v1.0.0-beta.1
v1.0.0-rc.1
```

### 6.5 Metadatos de compilación

```bash
# Formato: v<major>.<minor>.<patch>+<metadata>
v1.0.0+20260615
v1.0.0-alpha+exp.sha.5114f85
```

---

## 7. CHANGELOG

### 7.1 Formato estándar

```markdown
# Changelog

## [1.2.0] - 2026-06-15

### Added
- Exportación de resultados a PDF
- Notificaciones push por sorteo

### Fixed
- Crash al abrir sorteo sin conexión
- Cálculo incorrecto de premios

### Changed
- Migración de SQLite a Isar

### Deprecated
- API v1 (será eliminada en v2.0.0)

### Removed
- Login con PIN (reemplazado por biometría)

### Fixed
- Memory leak en pantalla de perfil

### Security
- Actualización de dependencias con CVE
```

### 7.2 Generación automática con standard-version

```bash
# Instalar
npm install --save-dev standard-version

# Ejecutar
npm run release

# Esto genera:
# - CHANGELOG.md actualizado
# - package.json con versión bump
# - Commit con los cambios
# - Tag v1.2.0
```

---

## 8. Buenas Prácticas

### 8.1 Commits Atómicos

```bash
# ✅ Cada commit es una unidad lógica independiente
feat(raffles): agregar filtro por fecha
feat(raffles): agregar exportación a PDF
fix(raffles): corregir cálculo de premios

# ❌ Commits que mezclan cambios no relacionados
feat: agregar filtros y corregir bugs varios
```

### 8.2 Ramas Cortas

```bash
# Una feature por rama
# Máximo 2-3 días de trabajo
# PRs pequeños (< 400 líneas)
```

### 8.3 Rebase vs Merge

```bash
# En ramas de feature usa rebase (historia lineal)
git rebase origin/develop

# En ramas compartidas usa merge (preserva contexto)
git merge feature/agregar-filtro
```

### 8.4 Reglas para la rama main

```bash
# main SIEMPRE debe ser estable
# Solo se mergea desde release/ o hotfix/
# Nunca hacer commits directos en main
# Siempre taggear cada merge a main
```

---

## 9. Resumen

1. **Conventional Branch** para nomenclatura de ramas
2. **Git Flow** para apps Flutter con releases versionados
3. **`main`** = producción, **`develop`** = integración
4. **Features** en ramas separadas, merge a develop
5. **Releases** desde develop, merge a main con tag
6. **Hotfixes** desde main, merge a ambas
7. **PRs pequeños** con code review obligatorio
8. **Tags semánticos** para cada release
9. **CHANGELOG** generado automáticamente con standard-version

---

## Recursos

- [Git Flow original (Vincent Driessen)](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow Guide](https://docs.github.com/en/get-started/using-github/github-flow)
- [Semantic Versioning](https://semver.org/)
- [Conventional Branch](https://github.com/debitoor/conventional-branch)

---

## 📚 Referencias

- [Conventional Commits](https://www.conventionalcommits.org/) — Especificación de mensajes de commit
- [Husky](https://typicode.github.io/husky/) — Git hooks modernos para Node.js
- [Commitlint](https://commitlint.js.org/) — Linter para mensajes de commit
- [Git | Documentation](https://git-scm.com/doc) — Documentación oficial de Git
