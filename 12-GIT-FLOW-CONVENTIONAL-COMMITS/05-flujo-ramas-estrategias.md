# 05 - Estrategias de Ramas y Releases

> Define cómo organizar el trabajo en equipo: qué ramas existen, cómo se integran, y cómo se hacen los releases.

---

## 1. Git Flow vs GitHub Flow

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

## 2. Git Flow Simplificado

### 2.1 Estructura de Ramas

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

### 2.2 Convención de Nombres

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

## 3. Flujo de Trabajo

### 3.1 Nueva Feature

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

### 3.2 Release

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

### 3.3 Hotfix

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

## 4. Pull Requests y Code Review

### 4.1 Template de PR

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

### 4.2 Reglas de Code Review

| Qué revisar | Por qué |
|-------------|---------|
| Lógica de negocio | ¿Resuelve el problema correcto? |
| Manejo de errores | ¿Qué pasa si la API falla? |
| Tests | ¿Cubren casos borde? |
| Nombres | ¿Son claros y consistentes? |
| Side effects | ¿Afecta otras features? |

---

## 5. Versionado

### 5.1 Esquema

```
v<major>.<minor>.<patch>

v1.0.0  → Primer release estable
v1.1.0  → Nueva feature
v1.1.1  → Bug fix
v2.0.0  → Breaking change
```

### 5.2 Tags en Git

```bash
# Annotated tag (recomendado)
git tag -a v1.2.0 -m "Release v1.2.0: Exportación PDF"

# Lightweight tag (simple)
git tag v1.2.0

# Push tags
git push origin --tags
```

### 5.3 CHANGELOG

```markdown
# Changelog

## [1.2.0] - 2026-06-15

### Added
- Exportación de resultados a PDF
- Notificaciones push por sorteo

### Fixed
- Crash al abrir sorteo sin conexión
- Cálculo incorrecto de premios

## [1.1.0] - 2026-05-20

### Added
- Filtro por fecha en lista de rifas
- Búsqueda de clientes

## [1.0.0] - 2026-04-01

### Added
- Sistema de rifas completo
- Gestión de clientes
- Reportes básicos
```

---

## 6. Buenas Prácticas

### 6.1 Commits Atómicos

```bash
# ✅ Cada commit es una unidad lógica independiente
feat(raffles): agregar filtro por fecha
feat(raffles): agregar exportación a PDF
fix(raffles): corregir cálculo de premios

# ❌ Commits que mezclan cambios no relacionados
feat: agregar filtros y corregir bugs varios
```

### 6.2 Ramas Cortas

```bash
# Una feature por rama
# Máximo 2-3 días de trabajo
# PRs pequeños (< 400 líneas)
```

### 6.3 Rebase vs Merge

```bash
# En ramas de feature usa rebase (historia lineal)
git rebase origin/develop

# En ramas compartidas usa merge (preserva contexto)
git merge feature/agregar-filtro
```

---

## 7. Resumen

1. **Git Flow** para apps Flutter con releases versionados
2. **`main`** = producción, **`develop`** = integración
3. **Features** en ramas separadas, merge a develop
4. **Releases** desde develop, merge a main con tag
5. **Hotfixes** desde main, merge a ambas
6. **PRs pequeños** con code review obligatorio
7. **Tags semánticos** para cada release

---

## Recursos

- [Git Flow original (Vincent Driessen)](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow Guide](https://docs.github.com/en/get-started/using-github/github-flow)
- [Semantic Versioning](https://semver.org/)
