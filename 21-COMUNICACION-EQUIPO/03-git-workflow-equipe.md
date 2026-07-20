# 03: Git Workflow en Equipo

## Git Flow vs GitHub Flow vs Trunk-based

No existe un workflow perfecto. La eleccion depende del tamano del equipo,
frecuencia de releases, y madurez del proyecto.

### Comparacion de workflows

| Caracteristica | Git Flow | GitHub Flow | Trunk-based |
|---------------|----------|-------------|-------------|
| **Complejidad** | Alta | Baja | Media |
| **Ramas** | main, develop, feature, release, hotfix | main + feature branches | main (o trunk) |
| **Release cycle** | Programado (semanal/quincenal) | Continuo | Continuo |
| **Ideal para** | Teams grandes, releases ciclicos | Teams pequeños-medianos | Teams maduros, CI/CD solido |
| **Merge frequency** | Baja (por sprint) | Media (por feature) | Alta (varias veces al dia) |
| **Feature flags** | No requerido | Opcional | Requerido |
| **Riesgo de conflictos** | Alto (ramas largas) | Medio | Bajo |

### Cuando usar cada uno

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION DE WORKFLOW                          │
│                                                                 │
│  ¿Tu equipo tiene > 10 developers?                             │
│  ├── SI → ¿Tienen releases programados?                        │
│  │         ├── SI → GIT FLOW                                   │
│  │         └── NO → GITHUB FLOW + code owners                  │
│  └── NO → ¿Tienen CI/CD maduro?                                │
│            ├── SI → TRUNK-BASED                                 │
│            └── NO → GITHUB FLOW                                 │
│                                                                 │
│  RECOMENDACION PARA EQUIPOS PEQUEÑOS:                           │
│  GitHub Flow es suficiente para el 90% de los casos.            │
└─────────────────────────────────────────────────────────────────┘
```

### Git Flow en detalle

```
main:       ─────────●──────────────────●──────────────────
                     │                  ↑
release/            │     ●────────────┤
                     │     │            │
develop:    ─────●───●─────●────●───────●────●──────────────
               │       ↑    │         ↑
feature/A:     ●───────●    │         │
                     │      │         │
feature/B:           ●──────●         │
                                    │
hotfix/:                               ●────────────────────
```

| Rama | Origen | Merge en | Ciclo de vida |
|------|--------|----------|---------------|
| `main` | Siempre existe | — | Nunca se commitea directo |
| `develop` | `main` | `main` via release | Rama base del desarrollo |
| `feature/*` | `develop` | `develop` | Dura dias/semanas |
| `release/*` | `develop` | `main` y `develop` | Dura horas/dias |
| `hotfix/*` | `main` | `main` y `develop` | Dura horas |

### GitHub Flow en detalle

```
main:    ─────●──────●──────●──────●──────●──────●──────
               ↑      │            ↑      │
feature:       ●──────●            │      │
                              ↑    │      │
bugfix:                      ●────●      │
                                       ↑  │
hotfix:                               ●──●
```

| Paso | Comando | Descripcion |
|------|---------|-------------|
| 1. Crear rama | `git checkout -b feature/nombre` | Desde main |
| 2. Desarrollar | `git commit -m "feat: ..."` | Commits frecuentes |
| 3. Push | `git push origin feature/nombre` | Publicar rama |
| 4. Abrir PR | GitHub UI | Pedir review |
| 5. Review | Comments en PR | Feedback del equipo |
| 6. Merge | Squash merge o merge commit | A main |

### Trunk-based en detalle

```
trunk/main: ───●────●────●────●────●────●────●────●────●──
               │    ↑    │         ↑    │    ↑
dev-branch:    ●────●    │         │    │    │
                     │   │         │    │    │
dev-branch:         ●────●         │    │    │
                              ↑    │    │    │
dev-branch:                      ●─────●    │
                                       ↑    │
dev-branch:                               ●──●
```

**Regla clave:** Las ramas viven < 2 dias. Si toma mas, usa feature flags.

## Convenciones de Nombres de Ramas

| Prefijo | Uso | Ejemplo |
|---------|-----|---------|
| `feature/` | Nueva funcionalidad | `feature/user-profile-screen` |
| `bugfix/` | Bug en develop | `bugfix/login-validation-error` |
| `hotfix/` | Bug critico en produccion | `hotfix/crash-on-payment` |
| `release/` | Preparar release | `release/v1.2.0` |
| `chore/` | Mantenimiento, config, deps | `chore/update-flutter-3.19` |
| `refactor/` | Refactorizar sin cambiar comportamiento | `refactor/extract-auth-service` |
| `docs/` | Solo documentacion | `docs/api-reference` |
| `test/` | Agregar o mejorar tests | `test/auth-bloc-coverage` |

### Formato del nombre

```
┌─────────────────────────────────────────────────────────────────┐
│  FORMATO: prefijo/descripcion-corta-en-kebab-case              │
│                                                                 │
│  ✅ feature/google-sign-in                                      │
│  ✅ bugfix/null-pointer-in-home-list                            │
│  ✅ hotfix/payment-crash-ios-17                                 │
│  ✅ chore/upgrade-dependencies-2024-01                          │
│  ✅ refactor/extract-error-handler                              │
│                                                                 │
│  ❌ feature/GoogleSignIn (no usar CamelCase)                    │
│  ❌ feature/google_sign_in (no usar underscore)                 │
│  ❌ feature/add-google-sign-in-to-login-screen (muy largo)     │
│  ❌ feature/fix (muy vago)                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Merge vs Rebase vs Squash

### Comparacion

| Estrategia | Historia | Commits | Confliclos | Riesgo | Uso ideal |
|-----------|----------|---------|------------|--------|-----------|
| **Merge commit** | Limpia, ramificada | Todos preservados | Se resuelven una vez | Bajo | Feature branches |
| **Rebase** | Lineal, limpia | Todos preservados | Se resuelven por commit | Medio | Sincronizar feature con main |
| **Squash** | Lineal, comprimida | 1 commit por PR | Se resuelven una vez | Bajo | PRs con muchos WIP commits |

### Merge commit

```bash
git checkout develop
git merge feature/user-profile
# Crea un merge commit que une las dos ramas
```

```
Antes:                          Despues:
main:    A───B───C              main:    A───B───C───M
                                  ↑                   ↑
feature: D───E───F              feature: D───E───F───┘
```

**Pros:** Preserva historial completo, seguro
**Cons:** Historia se vuelve "rama de arbol" dificil de leer

### Rebase

```bash
git checkout feature/user-profile
git rebase develop
# Reescribe los commits de feature encima de develop
```

```
Antes:                          Despues:
main:    A───B───C              main:    A───B───C
                                  ↑
feature: D───E───F              feature:     D'──E'──F'
```

**Pros:** Historia lineal y limpia
**Cons:** Reescribe commits (peligro en ramas compartidas), confliclos multiples

### Squash and merge

```bash
git checkout feature/user-profile
git rebase -i develop
# En el editor, pick squash para todos menos el primero
# O usar GitHub: "Squash and merge" button
```

```
Antes:                          Despues:
main:    A───B───C              main:    A───B───C───S
                                  ↑                   ↑
feature: D───E───F              (rama eliminada)
```

**Pros:** Historia lineal, un commit = un feature, facil de revertir
**Cons:** Se pierde detalle de commits intermedios

### Regla de oro para equipos

```
┌─────────────────────────────────────────────────────────────────┐
│  RECOMENDACION PARA EQUIPOS:                                    │
│                                                                 │
│  • PRs personales     → SQUASH merge (un commit limpio)        │
│  • Sincronizar rama   → REBASE (mantener rama actualizada)     │
│  • Merge de release   → MERGE commit (preservar historial)     │
│                                                                 │
│  ⚠️ NUNCA: git push --force en ramas compartidas              │
│  ⚠️ NUNCA: git rebase ramas que otros estan usando            │
└─────────────────────────────────────────────────────────────────┘
```

## Resolviendo Conflictos de Merge

### Paso a paso

```bash
# 1. Actualizar tu rama con los ultimos cambios de main
git fetch origin
git checkout feature/mi-feature
git rebase origin/main

# 2. Si hay conflictos, git te mostrara:
<<<<<<< HEAD (tu codigo)
  Widget build(BuildContext context) {
    return const LoginScreen();
  }
=======
  Widget build(BuildContext context) {
    return const AuthScreen();
  }
>>>>>>> origin/main (codigo de main)

# 3. Editar el archivo para resolver el conflicto
# ELIMINAR las marcas <<<< === >>>>
# Dejar SOLO el codigo correcto

# 4. Marcar como resuelto
git add lib/features/auth/presentation/screens/auth_screen.dart

# 5. Continuar el rebase
git rebase --continue

# 6. Si hay multiples conflictos, repetir 2-5

# 7. Verificar que todo compila
flutter analyze
flutter test

# 8. Push (necesita force porque reescribiste historial)
git push --force-with-lease
```

### Estrategia para evitar conflictos

| Accion | Frecuencia | Impacto |
|--------|------------|---------|
| `git fetch && git rebase origin/main` | Diario | Reduce conflictos 80% |
| PRs pequenos (< 400 LOC) | Siempre | Mas facil de resolver |
| Comunicar cambios en archivos compartidos | Cuando ocurren | Previene sorpresas |
| Modulos bien separados | Arquitectura | Menos overlap de archivos |

## Pull Request Workflow Completo

### Flujo tipico

```
┌─────────────────────────────────────────────────────────────────┐
│                    PR WORKFLOW COMPLETO                          │
│                                                                 │
│  1. CREAR RAMA                                                  │
│     git checkout -b feature/user-profile                        │
│                                                                 │
│  2. DESARROLLAR (commits atomicos)                              │
│     git commit -m "feat: add user profile screen"              │
│     git commit -m "feat: add profile editing"                  │
│     git commit -m "test: add profile screen tests"             │
│                                                                 │
│  3. ACTUALIZAR CON MAIN                                         │
│     git fetch origin && git rebase origin/main                  │
│                                                                 │
│  4. PUSH                                                       │
│     git push origin feature/user-profile                        │
│                                                                 │
│  5. ABRIR PR                                                    │
│     - Titulo descriptivo                                        │
│     - Descripcion con contexto                                  │
│     - Screenshots/videos si hay UI                              │
│     - Asignar reviewers                                         │
│                                                                 │
│  6. ESPERAR REVIEW                                              │
│     - Responder comments                                        │
│     - Hacer cambios si es necesario                             │
│     - Push commits adicionales                                  │
│                                                                 │
│  7. MERGE                                                       │
│     - Squash merge para features                                │
│     - Branch se elimina automaticamente                         │
│                                                                 │
│  8. VERIFICAR                                                   │
│     - CI pasa en main                                           │
│     - No hay regression                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Template de PR description

```markdown
## Descripcion
[Brief description of what this PR does]

## Tipo de cambio
- [ ] Bug fix (non-breaking change)
- [ ] New feature (non-breaking change)
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Mi codigo sigue las convenciones del proyecto
- [ ] He realizado auto-review
- [ ] He agregado tests que prueban mi cambio
- [ ] Los tests existentes pasan correctamente
- [ ] No agrego warnings nuevas con `flutter analyze`
- [ ] La documentacion esta actualizada si es necesario

## Screenshots/Videos
[If applicable, add screenshots or videos]

## Contexto adicional
[Any extra context for reviewers]
```

## Branch Protection Rules

### Reglas recomendadas para `main`

```
┌─────────────────────────────────────────────────────────────────┐
│  BRANCH PROTECTION: main                                        │
│                                                                 │
│  ✅ Require pull request reviews before merging                 │
│     └── Required approving reviews: 1 (minimo)                 │
│     └── Dismiss stale reviews on new commits                    │
│     └── Require review from Code Owners                        │
│                                                                 │
│  ✅ Require status checks to pass before merging                │
│     └── Required checks:                                        │
│         - build (flutter build)                                 │
│         - test (flutter test)                                   │
│         - analyze (flutter analyze)                             │
│                                                                 │
│  ✅ Require branches to be up to date before merging            │
│                                                                 │
│  ✅ Require conversation resolution before merging              │
│                                                                 │
│  ✅ Require linear history (squash merge only)                  │
│                                                                 │
│  ❌ Do NOT allow force pushes                                   │
│  ❌ Do NOT allow deletions                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Reglas para `develop` (si usas Git Flow)

```
✅ Require pull request reviews: 1
✅ Require status checks: build, test
✅ Allow force pushes: solo para tech leads
```

## Estrategias de Monorepo

Si tu proyecto tiene multiples packages (app, shared, packages):

```
┌─────────────────────────────────────────────────────────────────┐
│  MONOREPO ESTRUCTURA                                            │
│                                                                 │
│  my-project/                                                    │
│  ├── apps/                                                      │
│  │   ├── mobile_app/          ← Flutter app principal           │
│  │   └── admin_panel/         ← Panel de admin                  │
│  ├── packages/                                                  │
│  │   ├── shared_widgets/      ← Widgets compartidos             │
│  │   ├── core/                ← Logica de negocio               │
│  │   └── auth/                ← Feature de auth                 │
│  └── tools/                  ← Scripts y herramientas           │
└─────────────────────────────────────────────────────────────────┘
```

| Estrategia | Cuando usar | Ejemplo |
|-----------|-------------|---------|
| **Single branch** | Todo se mergea a main | Equipos pequenos, CI rapido |
| **Package-level branches** | Cambios aislados en un paquete | Cambio en `auth/` no afecta `mobile_app/` |
| **Git submodules** | Paquetes en repos separados | Repos con historial independiente |

## Comandos Git para Trabajo en Equipo

### Comandos diarios

```bash
# Sincronizar con el remote
git fetch origin

# Ver ramas remotas
git branch -r

# Sincronizar rama actual con main
git rebase origin/main

# Ver historial de un archivo
git log --oneline --follow -- lib/features/auth/bloc/auth_bloc.dart

# Ver quien cambio una linea
git blame lib/features/auth/bloc/auth_bloc.dart

# Ver cambios en un rango de commits
git log --oneline main..feature/user-profile

# Stash de cambios pendientes
git stash push -m "WIP: login screen"
git stash pop
```

### Comandos de recovery

```bash
# Deshacer ultimo commit (preservar cambios)
git reset --soft HEAD~1

# Deshacer ultimo commit (perder cambios)
git reset --hard HEAD~1

# Recuperar un commit que borre
git reflog
git cherry-pick <commit-hash>

# Abortar un rebase en progreso
git rebase --abort

# Abortar un merge en progreso
git merge --abort
```

## Desastres Comunes de Git y Su Recovery

### Force push accidental

```bash
# Si hiciste force push y perdiste commits:
git reflog
# Busca el commit que perdiste
git checkout <commit-hash>
git branch recovery-branch
# Ahora tienes una rama con los commits perdidos
```

### Commits en la rama equivocada

```bash
# Mover commits de una rama a otra
git checkout feature-que-deberia-estar-en-main
git log --oneline  # Identificar los commits

# Cherry-pick los commits a la rama correcta
git checkout main
git cherry-pick <commit-hash-1>
git cherry-pick <commit-hash-2>

# Resetear la rama original
git checkout feature-que-deberia-estar-en-main
git reset --hard origin/main
```

### Detached HEAD

```bash
# Si estas en detached HEAD y quieres volver
git checkout main

# Si quieres guardar los cambios que hiciste
git checkout -b saved-changes
```

### Merge conflict que no puedes resolver

```bash
# Abortar el merge y volver al estado anterior
git merge --abort

# O si es un rebase
git rebase --abort
```

## Resumen

```
┌─────────────────────────────────────────────────────────────────┐
│              GIT WORKFLOW EN EQUIPO: RESUMEN                     │
│                                                                 │
│  ✅ Usa GitHub Flow para equipos pequenos-medianos             │
│  ✅ Nombra ramas con prefijo/descripcion-kebab-case            │
│  ✅ Squash merge para features, rebase para sincronizar        │
│  ✅ Resuelve conflictos con rebase, no con merge               │
│  ✅ Activa branch protection en main                           │
│  ✅ Haz fetch y rebase diario                                  │
│  ✅ PRs pequenos (< 400 LOC)                                   │
│  ✅ Usa git reflog para recovery                               │
│  ⚠️ NUNCA force push en ramas compartidas                     │
│  ⚠️ NUNCA rebase ramas que otros usan                         │
└─────────────────────────────────────────────────────────────────┘
```
