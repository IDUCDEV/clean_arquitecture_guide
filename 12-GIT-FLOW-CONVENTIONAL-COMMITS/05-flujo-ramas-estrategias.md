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

1. **Alfanuméricos, guiones y puntos en minúsculas:** Usar siempre letras minúsculas (az), números (0-9) y guiones (-) para separar palabras. Evite caracteres, guiones bajos o espacios especiales. Para ramas de liberación, puntos (.) pueden usarse en la descripción para representar números de versión (ej., `release/v1.2.0`).
2. **Sin guiones o puntos consecutivos:** No usar `feature/nuevo--login` ni `release/v1.-2.0`
3. **Sin guiones/puntos al inicio o final:** No usar `feature/-nuevo-login` ni `release/v1.2.0.`
4. **Claro y conciso:** El nombre debe ser descriptivo pero breve, indicando claramente el propósito del trabajo.
5. **Incluir números de ticket:** Si aplica, incluir el número de ticket para seguimiento. Ej., `feature/123-nuevo-login`.

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

### 1.5 Puntos Clave de la Especificación

1. **Nombres basados en un propósito:** El nombre de cada rama indica claramente su propósito, lo que facilita que todos los desarrolladores comprendan para qué sirve la rama.
2. **Integración con CI/CD:** Al utilizar nombres de ramas consistentes, puede ayudar a los sistemas automatizados (como canalizaciones de integración continua/implementación continua) a activar acciones específicas basadas en el tipo de rama (por ejemplo, implementación automática desde ramas de liberación).
3. **Colaboración en equipo:** Fomenta la colaboración dentro de los equipos al hacer explícito el propósito de la rama, reducir los malentendidos y facilitar que los miembros del equipo cambien entre tareas sin confusión.

### 1.6 Beneficios

- **Comunicación clara:** El nombre de la rama por sí solo proporciona una comprensión clara de su propósito en el cambio de código.
- **Fácil de automatizar:** Se conecta fácilmente a procesos de automatización (por ejemplo, diferentes flujos de trabajo para feature, release, etc.).
- **Escalabilidad:** Funciona bien en equipos grandes donde muchos desarrolladores trabajan en diferentes tareas simultáneamente.

### 1.7 Preguntas Frecuentes

**¿Por qué los tipos de ramas no son tan detallados como los commits convencionales (ej., build, ci, docs, style, refactor)?**

Las ramas son diferentes de las confirmaciones, son temporales y se usan principalmente hasta que se fusionan. Introducir demasiados tipos de ramas sería innecesario y las haría más difíciles de gestionar y recordar.

**¿Qué herramientas se pueden utilizar para identificar automáticamente si un miembro del equipo no cumple con esta especificación?**

Puedes usar verificación de confirmación para consultar las especificaciones de la rama o confirmar-verificar-acción si sus códigos están alojados en GitHub.

> Licencia: Creative Commons - CC BY 3.0

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

### 6.1 Introducción: El Infierno de Dependencias

En el mundo de la administración de software existe un temido lugar llamado "Infierno de Dependencias". Mientras más crece tu sistema y más paquetes integras dentro de tu software, más probable se hace que un día te encuentres en este pozo de desesperación.

En sistemas con muchas dependencias, lanzar nuevas versiones de los paquetes puede convertirse en una pesadilla. Si las especificaciones de las dependencias son muy estrictas, estarás en peligro de bloquear una versión (la inhabilidad de actualizar un paquete sin tener que publicar una nueva versión de cada otro paquete dependiente). Si las dependencias son especificadas de forma muy relajada, inevitablemente serás mordido por versiones promiscuas (asumir la compatibilidad con próximas versiones más allá de lo razonable).

**El Infierno de Dependencias** es donde estás cuando una versión bloqueada y/o promiscua previenen que muevas tu proyecto adelante de forma fácil y segura.

Como solución a este problema, se propone un conjunto simple de reglas y requerimientos que dicten cómo asignar e incrementar los números de la versión. Estas reglas están basadas en prácticas preexistentes de uso generalizado tanto en software de código cerrado como de código abierto.

### 6.2 Esquema (SemVer 2.0.0)

```
v<major>.<minor>.<patch>

v1.0.0  → Primer release estable
v1.1.0  → Nueva feature
v1.1.1  → Bug fix
v2.0.0  → Breaking change
```

### 6.3 Reglas de incremento

| Versión | Cuándo incrementar | Ejemplo |
|---------|-------------------|---------|
| **Major (X)** | Cambios incompatibles con API anterior | `1.0.0` → `2.0.0` |
| **Minor (Y)** | Nueva funcionalidad compatible | `1.0.0` → `1.1.0` |
| **Patch (Z)** | Corrección de bug compatible | `1.1.0` → `1.1.1` |

### 6.4 Especificación Completa SemVer 2.0.0

> Las palabras clave "DEBE", "NO DEBE", "OBLIGATORIO", "DEBERÁ", "NO DEBERÁ", "DEBERÍA", "NO DEBERÍA", "RECOMENDADO", "PUEDE" y "OPCIONAL" se interpretan como se describe en RFC 2119.

| # | Regla |
|---|-------|
| 1 | El Software que usa Versionado Semántico DEBE declarar un API público. Este API puede ser declarado en el propio código o debe existir estrictamente en la documentación. |
| 2 | Un número de versión normal DEBE tener la forma de X.Y.Z donde X, Y y Z son números enteros no negativos, y NO DEBEN ser precedidos de ceros. X es la versión mayor, Y es la versión menor, y Z es la versión parche. |
| 3 | Una vez que el paquete versionado ha sido publicado, el contenido de esa versión NO DEBE ser modificado. Cualquier modificación DEBE ser publicada como una nueva versión. |
| 4 | Una versión mayor en cero (0.y.z) se considera como desarrollo inicial. Todo PUEDE cambiar en cualquier momento. El API público NO DEBERÍA ser considerado estable. |
| 5 | La versión 1.0.0 define el API público. La manera en que cada número de versión es incrementado después de esta publicación dependerá de su API público y cómo cambia. |
| 6 | La versión parche Z (x.y.Z \| x > 0) DEBE ser incrementada si solamente se introducen correcciones de errores compatibles con versiones anteriores. Una corrección de error se define como un cambio interno que corrige un comportamiento incorrecto. |
| 7 | La versión menor Y (x.Y.z \| x > 0) DEBE ser incrementada si se introduce funcionalidad nueva y compatible con la versión anterior del API público. Ésta DEBE ser incrementada si se introduce cualquier funcionalidad al API público o mejora al código privado. La versión parche DEBE reiniciarse a 0 cuando una versión menor se incrementa. |
| 8 | La versión mayor X (X.y.z \| x > 0) DEBE ser incrementada solamente si se introducen cambios incompatibles con la versión anterior del API público. Este PUEDE incluir cambios de nivel menor y parches. Versiones parche y menores DEBEN ser reiniciadas a 0 cuando una versión mayor es incrementada. |
| 9 | Una versión de prelanzamiento PUEDE ser denotada agregando un guión y una serie de identificadores separados por puntos, inmediatamente seguida de la versión parche. Los identificadores DEBEN ser compuestos sólo de caracteres alfanuméricos ASCII y guión ([0-9A-Za-z-]). Los identificadores NO DEBEN estar vacíos. |
| 10 | Metadatos de compilación PUEDEN ser denotados agregando el signo más y una serie de identificadores separados por puntos, inmediatamente seguido de la versión parche o prelanzamiento. Los metadatos de compilación DEBEN ser ignorados cuando se determina la precedencia de la versión. |
| 11 | La precedencia se refiere a cómo las versiones se comparan entre ellas cuando se ordenan. La precedencia DEBE ser calculada separando los identificadores de la versión en mayor, menor, parche y prelanzamiento (dejando de lado los metadatos de compilación). |

### 6.5 Precedencia de Versiones

La precedencia es determinada por la primera diferencia al comparar cada uno de los identificadores de izquierda a derecha:

1. Mayor, menor y parche son siempre comparadas numéricamente. Por ejemplo: `1.0.0 < 2.0.0 < 2.1.0 < 2.1.1`.
2. Cuando la versión mayor, menor y parche son iguales, la versión de prelanzamiento tiene menor precedencia que la versión normal. Por ejemplo: `1.0.0-alpha < 1.0.0`.
3. Identificadores compuestos solamente por números son comparados numéricamente.
4. Los identificadores con letras o guiones son comparados léxicamente en orden ASCII.
5. Identificadores numéricos siempre tienen menor precedencia que identificadores no numéricos.
6. Un conjunto de campos de prelanzamiento más numeroso tiene mayor precedencia que un conjunto menos numeroso, si todos los identificadores anteriores son iguales.

```bash
# Ejemplo de precedencia
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0
```

### 6.6 Tags en Git

```bash
# Annotated tag (recomendado)
git tag -a v1.2.0 -m "Release v1.2.0: Exportación PDF"

# Lightweight tag (simple)
git tag v1.2.0

# Push tags
git push origin --tags
```

### 6.7 Versiones de pre-lanzamiento

```bash
# Formato: v<major>.<minor>.<patch>-<identificador>
v1.0.0-alpha
v1.0.0-alpha.1
v1.0.0-beta.1
v1.0.0-rc.1
```

### 6.8 Metadatos de compilación

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

---

## Licencia

Este documento está basado en las especificaciones:
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/)
- [Conventional Branch 1.0.0](https://github.com/debitoor/conventional-branch)
- [Semantic Versioning 2.0.0](https://semver.org/)

Licencia: Creative Commons - CC BY 3.0
