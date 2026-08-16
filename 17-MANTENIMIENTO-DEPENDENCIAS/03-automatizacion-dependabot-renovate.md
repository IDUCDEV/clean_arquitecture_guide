# 03 — Automatización: Dependabot y Renovate

> Configura bots de actualización como parte del workflow del equipo.

---

## 1. Dependabot

### 1.1 Configuración Básica

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "npm"
    directory: "/apps/web"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5

  - package-ecosystem: "pub"
    directory: "/apps/mobile"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

Esta es la configuración real del monorepo de referencia.

### 1.2 Personalización

```yaml
updates:
  - package-ecosystem: "pub"
    directory: "/apps/mobile"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
      timezone: "America/Caracas"
    open-pull-requests-limit: 10
    reviewers:
      - "isaac-urdaneta"
    assignees:
      - "isaac-urdaneta"
    labels:
      - "dependencies"
      - "flutter"
    allow:
      - dependency-type: "direct"
    ignore:
      - dependency-name: "flutter_bloc"
        update-types: ["version-update:semver-major"]
```

### 1.3 Parámetros Clave

| Parámetro | Qué hace | Recomendación |
|---|---|---|
| `schedule.interval` | Frecuencia de chequeo | `weekly` (evita ruido diario) |
| `open-pull-requests-limit` | Máx PRs abiertos simultáneos | `5-10` (no inundar) |
| `reviewers` | Quién revisa los PRs | El team lead o dueño del módulo |
| `allow` | Filtrar qué actualizar | `direct` (solo directas, no transitivas) |
| `ignore` | Excluir paquetes específicos | Solo para updates problemáticos conocidos |
| `target-branch` | Rama base de los PRs | `dev` si usas Git Flow |

### 1.4 Grupos (`groups`)

Desde 2023, Dependabot permite agrupar dependencias relacionadas en un **solo PR**:

```yaml
  - package-ecosystem: "pub"
    directory: "/apps/mobile"
    schedule:
      interval: "weekly"
    groups:
      bloc-family:
        patterns:
          - "bloc"
          - "flutter_bloc"
          - "bloc_test"
        exclude-patterns:
          - "bloc*"
          - "*.test"
      patch-updates:
        update-types:
          - "patch"
        patterns:
          - "*"
```

**Recomendaciones:**
- Agrupa **patch updates** en un solo PR (bajo riesgo)
- Agrupa **familias de paquetes** (`bloc`, `go_router`, `supabase`) para revisarlas juntas
- **Nunca agrupes major updates** — cada uno merece su propia migración

### 1.5 Caso Real: Monitorear root `package.json`

El monorepo actual no cubre el `package.json` raíz (commitlint, husky, commitizen):

```yaml
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "monthly"
    open-pull-requests-limit: 3
```

Estas dependencias de tooling cambian poco, por eso `monthly` es suficiente.

### 1.6 Dependabot Security Updates

GitHub habilita automáticamente PRs de seguridad para CVEs conocidas. No necesita configuración en `dependabot.yml`, se activa desde Settings → Code security → Dependabot security updates.

---

## 2. Renovate

### 2.1 ¿Por qué usar Renovate?

| Aspecto | Dependabot | Renovate |
|---|---|---|
| Configuración | YAML simple, opciones limitadas | JSON/JS, altamente configurable |
| Agrupación de PRs | `groups` (desde 2023) para version y security updates | `groupName` para agrupar por tipo |
| Schedule por paquete | No | Sí, por regex |
| Auto-merge condicional | Limitado | Sí, con reglas |
| Dashboard | No | Panel web con estado |
| Onboarding | No | PR de configuración inicial |

### 2.2 Configuración Mínima

```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended"
  ],
  "labels": ["dependencies"],
  "schedule": ["before 9am on monday"],
  "packageRules": [
    {
      "matchPackageNames": ["flutter_bloc", "bloc"],
      "groupName": "bloc packages",
      "automerge": true
    },
    {
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "pr"
    },
    {
      "matchPackageNames": ["next", "react", "react-dom"],
      "enabled": false
    }
  ]
}
```

### 2.3 Agrupación Inteligente

```json
{
  "packageRules": [
    {
      "matchPackagePatterns": ["*"],
      "groupName": "all dependencies",
      "groupSlug": "all-deps",
      "schedule": ["before 9am on monday"]
    }
  ]
}
```

**Cuándo agrupar:**
- Paquetes del mismo ecosistema (`bloc`, `flutter_bloc`, `bloc_test`)
- Patch updates (bajo riesgo)
- Dev dependencies

**Cuándo NO agrupar:**
- Major updates (riesgo alto)
- Paquetes con migraciones complejas

---

## 3. Flujo de Trabajo con PRs de Dependencias

### 3.1 Revisión

```
1. Dependabot/Renovate abre PR
       ↓
2. CI corre automáticamente (tests + analyze)
       ↓
3. Revisar: ¿CI pasa? ¿Hay breaking changes?
       ↓
4. Si CI pasa + es patch/minor → merge aprobado
       ↓
5. Si es major → revisar changelog manualmente
       ↓
6. Merge con squash + mensaje semántico
```

### 3.2 Estrategia de Auto-Merge

```yaml
# Dependabot no tiene auto-merge nativo. La forma recomendada por GitHub es
# combinar dependabot/fetch-metadata + gh pr merge --auto (el PR espera a que CI pase).

# .github/workflows/auto-merge-deps.yml
name: Auto-merge dependencies
on:
  pull_request:
    types: [opened, synchronize]

permissions:
  pull-requests: write
  contents: write

jobs:
  auto-merge:
    if: github.actor == 'dependabot[bot]' || github.actor == 'renovate[bot]'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Fetch dependabot metadata
        id: meta
        if: github.actor == 'dependabot[bot]'
        uses: dependabot/fetch-metadata@v3
        with:
          compat-lookup: true

      - name: Auto-merge patch & minor updates
        if: steps.meta.outputs.update-type == 'version-update:semver-patch' || steps.meta.outputs.update-type == 'version-update:semver-minor'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 3.3 Mensajes de Commit

```bash
# Patch
chore(deps): update dependency flutter_bloc to 9.1.1

# Minor
feat(deps): update dependency dio to 5.11.0

# Major
chore(deps): migrate flutter_bloc from 9.x to 10.x
```

---

## 4. CI de Auditoría Semanal

Workflow que corre `dart pub outdated` semanal y crea un issue si hay dependencias atrasadas:

```yaml
name: Weekly dependency audit
on:
  schedule:
    - cron: '0 9 * * 1'  # Lunes 9am

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: subosito/flutter-action@v3
        with:
          flutter-version: '3.47.0'

      - name: Check outdated
        id: outdated
        run: |
          dart pub outdated --no-dev > /tmp/outdated.txt
          cat /tmp/outdated.txt
          if grep -q "up-to-date" /tmp/outdated.txt; then
            echo "All up to date"
          else
            echo "has_outdated=true" >> $GITHUB_OUTPUT
          fi
        working-directory: apps/mobile

      - name: Create issue
        if: steps.outdated.outputs.has_outdated == 'true'
        uses: actions/github-script@v9
        with:
          script: |
            const fs = require('fs');
            const outdated = fs.readFileSync('/tmp/outdated.txt', 'utf8');
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '📦 Dependencies weekly audit',
              body: '```\n' + outdated + '\n```',
              labels: ['dependencies', 'automated']
            });
```

---

## 5. Ejercicio

Configura Dependabot para un monorepo con estas características:
- Flutter en `apps/mobile/` (pub)
- Next.js en `apps/web/` (npm)
- Tooling en raíz `package.json` (npm)
- GitHub Actions en `/` (github-actions)

Incluye:
- Schedule: Flutter lunes, web martes, tooling mensual, Actions semanal
- Límite: 5 PRs para Flutter, 3 para web
- Revisores: `team-flutter` y `team-web`
- Labels: `dependencies` + `ecosystem:{{name}}`
- Ignorar major updates de `flutter_bloc` temporalmente

---

## Resumen

1. **Dependabot** es simple y funciona — ideal para empezar
2. **Renovate** es más potente — útil si necesitas control fino
3. **Auto-merge** solo para patch/minor que pasen CI
4. **Auditoría semanal** en CI para detectar dependencias atrasadas
5. **Revisión manual** siempre para major updates

---

## 📚 Referencias

- [GitHub | Configuring Dependabot version updates](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuring-dependabot-version-updates) — Configuración de `dependabot.yml`
- [GitHub | Dependabot security updates](https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates) — Security updates automáticos
- [Renovate Docs | Configuration options](https://docs.renovatebot.com/configuration-options/) — Opciones de configuración
- [Renovate Docs | Preset config:recommended](https://docs.renovatebot.com/presets-config/#configrecommended) — Preset recomendado

---

> 📖 **Siguiente:** [04-mantenimiento-sdk-ecosistema.md](./04-mantenimiento-sdk-ecosistema.md) — Mantener el SDK del proyecto
