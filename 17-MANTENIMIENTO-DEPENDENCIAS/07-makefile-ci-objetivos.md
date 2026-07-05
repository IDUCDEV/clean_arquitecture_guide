# 07 — Makefile y CI para Mantenimiento Continuo

> Extiende el Makefile y los workflows CI para monitorear la salud de las dependencias automáticamente.

---

## 1. Targets de Dependencias en el Makefile

> 📖 La sintaxis básica de Makefile se cubre en [10-MAKEFILE/02-sintaxis-basica.md](../10-MAKEFILE/02-sintaxis-basica.md). Aquí solo se muestran targets específicos de dependencias.

### 1.1 Targets Existentes

```makefile
# Ya existentes en el Makefile del monorepo
deps: deps-mobile deps-web        # Instalar todas las dependencias
deps-mobile:                       # flutter pub get
deps-web:                          # npm install
outdated:                          # flutter pub outdated
upgrade:                           # flutter pub upgrade + npm update
```

### 1.2 Nuevos Targets Propuestos

```makefile
# ─── Dependencies maintenance ───────────────────────────────────

.PHONY: audit dep-report check-constraints dep-tree deps-security

# Auditoría completa de seguridad
audit: audit-mobile audit-web audit-actions
	@echo "✅ Security audit complete"

audit-mobile:
	@echo "🔍 Auditing Flutter dependencies..."
	@cd apps/mobile && dart pub get && dart pub deps --json > /tmp/deps-mobile.json
	@cd apps/mobile && dart pub outdated --no-dev

audit-web:
	@echo "🔍 Auditing npm dependencies..."
	@cd apps/web && npm audit --audit-level=high

audit-actions:
	@echo "🔍 Checking GitHub Actions versions..."
	@for f in .github/workflows/*.yml; do \
		echo "Checking $$f..."; \
		grep -n "uses:" $$f | grep -v "@" && echo "  ⚠️  Unpinned action in $$f" || true; \
	done

# Reporte de estado de dependencias en markdown
dep-report:
	@echo "# 📦 Estado de Dependencias\n" > /tmp/dep-report.md
	@echo "## Flutter\n" >> /tmp/dep-report.md
	@cd apps/mobile && dart pub outdated --no-dev >> /tmp/dep-report.md
	@echo "\n## npm\n" >> /tmp/dep-report.md
	@cd apps/web && npm outdated --json 2>/dev/null | jq -r 'to_entries[] | "* \(.key): \(.value.current) → \(.value.latest)"' >> /tmp/dep-report.md 2>/dev/null || echo "  All up to date" >> /tmp/dep-report.md
	@echo "\n📄 Report generated: /tmp/dep-report.md"
	@cat /tmp/dep-report.md

# Verificar constraints de pubspec.yaml
check-constraints:
	@echo "🔍 Checking dependency constraints..."
	@cd apps/mobile && \
		( dart pub deps 2>&1 | grep -q "Conflict" && \
		echo "❌ Dependency conflicts found!" || \
		echo "✅ No dependency conflicts" )
	@cd apps/mobile && \
		( dart pub outdated 2>&1 | grep -q "overridden" && \
		echo "⚠️  dependency_overrides in use (should be temporary)" || \
		echo "✅ No overrides" )

# Árbol completo de dependencias
dep-tree:
	@cd apps/mobile && dart pub deps

# Escanear dependencias con vulnerabilidades conocidas
deps-security:
	@echo "🔐 Scanning dependencies for known vulnerabilities..."
	@cd apps/mobile && dart pub deps --json | \
		jq -r '.packages | to_entries[] | "\(.key)@\(.value.version)"' | \
		while read pkg; do \
			response=$$(curl -s -o /dev/null -w "%{http_code}" \
				"https://api.osv.dev/v1/query" \
				-d "{\"package\":{\"name\":\"$$(echo $$pkg | cut -d@ -f1 | sed 's/-/_/g')\", \
				\"ecosystem\":\"Pub\"},\"version\":\"$$(echo $$pkg | cut -d@ -f2)\"}"); \
			[ "$$response" != "200" ] || echo "⚠️  $$pkg may have vulnerabilities"; \
		done
```

---

## 2. Uso en el Día a Día

```bash
# Antes de un release
make audit          # Auditoría completa
make dep-report     # Reporte de estado

# Semanalmente
make check-constraints   # Verificar que no hay conflictos
make outdated            # Ver qué se puede actualizar

# Cuando actualizas Flutter SDK
make deps           # Reinstalar dependencias
make check-constraints
make audit
```

---

## 3. Workflows CI de Monitoreo

### 3.1 Auditoría Semanal Automática

```yaml
# .github/workflows/deps-audit.yml
name: Weekly dependency audit
on:
  schedule:
    - cron: '0 9 * * 1'  # Lunes 9am UTC

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.41.0'

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: apps/web/package-lock.json

      - name: Flutter audit
        id: flutter-audit
        run: |
          cd apps/mobile
          dart pub get
          dart pub outdated --no-dev > /tmp/flutter-outdated.txt
          echo "has_outdated=false" >> $GITHUB_OUTPUT

      - name: npm audit
        id: npm-audit
        run: |
          cd apps/web
          npm audit --json > /tmp/npm-audit.json 2>&1 || true
          echo "audit_done=true" >> $GITHUB_OUTPUT

      - name: Upload audit artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dependency-audit-${{ github.run_id }}
          path: |
            /tmp/flutter-outdated.txt
            /tmp/npm-audit.json
```

### 3.2 Gate en PRs

```yaml
# Fragmento para agregar a ci-quality.yml
- name: Check dependency health
  run: |
    cd apps/mobile
    dart pub deps --json > /tmp/deps.json
    
    # Verificar dependency_overrides (deben ser temporales)
    if grep -q "dependency_overrides" pubspec.yaml; then
      echo "⚠️  Warning: dependency_overrides found in pubspec.yaml"
    fi

- name: npm audit gate
  run: |
    cd apps/web
    npm audit --audit-level=high || \
      (echo "❌ High/critical vulnerabilities found"; exit 1)
```

### 3.3 Issue Automático por Dependencias Atrasadas

```yaml
# Continuación del workflow semanal
- name: Create issue if outdated
  if: steps.flutter-audit.outputs.has_outdated == 'true'
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const outdated = fs.readFileSync('/tmp/flutter-outdated.txt', 'utf8');
      
      // Verificar si ya existe un issue abierto similar
      const issues = await github.rest.issues.listForRepo({
        owner: context.repo.owner,
        repo: context.repo.repo,
        state: 'open',
        labels: ['dependencies', 'automated']
      });
      
      if (issues.data.length === 0) {
        await github.rest.issues.create({
          owner: context.repo.owner,
          repo: context.repo.repo,
          title: '📦 Weekly dependency report',
          body: '```\n' + outdated + '\n```\n_Automated report_',
          labels: ['dependencies', 'automated']
        });
      }
```

---

## 4. Checklist de Mantenimiento Regular

### Diario / Por PR
- [ ] `flutter analyze` pasa sin errores
- [ ] CI verde

### Semanal (Lunes)
- [ ] `make audit` — revisar dependencias
- [ ] Revisar PRs abiertos de Dependabot/Renovate
- [ ] Mergear patch y minor que pasen CI

### Mensual
- [ ] `make dep-report` — generar reporte
- [ ] Revisar issues de seguridad pendientes
- [ ] Actualizar `pubspec.lock` y `package-lock.json`

### Trimestral
- [ ] Verificar si hay paquetes deprecados (06)
- [ ] Revisar si Flutter tiene nueva versión stable
- [ ] Evaluar migración de SDK si aplica
- [ ] Actualizar documentación del proyecto

### Anual
- [ ] Auditoría completa de seguridad
- [ ] Revisar EOL de Node.js
- [ ] Evaluar todas las dependencias contra alternativas
- [ ] Actualizar Flutter SDK si está 2+ releases atrás

---

## 5. Ejercicio

1. Agrega los targets `audit`, `dep-report`, `check-constraints` al Makefile del monorepo
2. Crea un workflow semanal de auditoría que corra `make audit`
3. Configura un gate en `ci-quality.yml` que ejecute `npm audit --audit-level=high`
4. Prueba los targets localmente:
   ```bash
   make audit
   make dep-report
   make check-constraints
   ```

---

## Resumen

1. **Makefile targets** extienden los existentes con auditoría y reportes
2. **CI semanal** corre automáticamente y crea issues si hay problemas
3. **Gate en PRs** bloquea códigos con dependencias vulnerables
4. **Checklist** de mantenimiento: diario, semanal, mensual, trimestral y anual
5. **Madurez**: estos targets convierten el mantenimiento de rutina en algo automático

---

## 📚 Referencias

- [GitHub | Schedule events in Actions](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule) — Disparadores `cron` en workflows
- [Dart | Pub deps](https://dart.dev/tools/pub/cmd/pub-deps) — Comando `dart pub deps`
- [npm Docs | npm-audit](https://docs.npmjs.com/cli/v10/commands/npm-audit) — Comando `npm audit`

---

> **Fin del módulo 17.** Sigue practicando con el checklist de mantenimiento regular. Cada dependencia que actualices te hará más rápido en la próxima.
