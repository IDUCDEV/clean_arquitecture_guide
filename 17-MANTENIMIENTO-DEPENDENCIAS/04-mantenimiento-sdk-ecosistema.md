# 04 — Mantenimiento del SDK y Ecosistema

> Mantén las herramientas base del proyecto sincronizadas: Flutter, Supabase CLI y Node.js.

---

## 1. Flutter SDK

### 1.1 El Problema

```bash
# Dev 1: Flutter 3.16.0
# Dev 2: Flutter 3.22.0
# CI/CD: Flutter 3.24.0

# Misma base de código, diferentes versiones → resultados diferentes
# "En mi máquina funciona" → versión incorrecta
```

### 1.2 FVM al Rescate

> 📖 La instalación y uso de FVM está cubierta en [12-GIT-FLOW/04-fvm-version-management.md](../12-GIT-FLOW-CONVENTIONAL-COMMITS/04-fvm-version-management.md). Aquí solo se cubre el aspecto de mantenimiento.

```bash
# apps/mobile/.fvm/flutter_sdk_version
3.41.0
```

**Checklist de mantenimiento:**
- ✅ Todos los devs usan `fvm flutter` en vez de `flutter` directamente
- ✅ VS Code configurado con `dart.flutterSdkPath: ".fvm/flutter_sdk"`
- ✅ CI/CD hardcodea la versión en el workflow YAML
- ✅ IDE y CLI leen la misma versión

### 1.3 Cuándo Actualizar Flutter

| Señal | Acción |
|---|---|
| Nueva versión stable | Esperar 1-2 semanas * |
| Release de Dart con features que necesitas | Actualizar inmediatamente |
| CVE de seguridad en Flutter/Dart | Actualizar urgente |
| Paquete que requieres necesita SDK más nuevo | Actualizar |

> \* Buena práctica basada en experiencia del ecosistema, no es política oficial de Google.

### 1.4 Proceso de Upgrade

```bash
# 1. Verificar compatibilidad sin cambiar
fvm flutter --version
flutter upgrade --verify-only

# 2. Instalar nueva versión
fvm install 3.44.0
fvm use 3.44.0

# 3. Probar localmente
fvm flutter pub get
fvm flutter analyze
fvm flutter test -j 1
fvm dart fix --dry-run

# 4. Actualizar CI/CD
# Cambiar flutter-version: '3.41.0' → '3.44.0' en workflows
# Actualizar GitHub Variable si usas una

# 5. Commit
git add apps/mobile/.fvm/flutter_sdk_version
git commit -m "chore(sdk): bump Flutter from 3.41.0 to 3.44.0"
```

### 1.5 Centralización de Versiones

El monorepo referencia la versión de Flutter en múltiples lugares:

```
.github/workflows/ci-quality.yml:        flutter-version: '3.41.0'
.github/workflows/flutter-android-release.yml: flutter-version: '3.41.0'
apps/mobile/.fvm/flutter_sdk_version:    3.41.0
.github/variables/FLUTTER_VERSION:       3.41.0
```

**Práctica recomendada:** Usa GitHub Variables o un archivo `.github/workflows/config/versions.env` para centralizar:

```yaml
# En un workflow
- name: Setup Flutter
  uses: subosito/flutter-action@v2
  with:
    flutter-version: ${{ vars.FLUTTER_VERSION }}
```

Así cambias la versión en un solo lugar.

---

## 2. Supabase CLI

### 2.1 Versiones en `config.toml`

```toml
# supabase/config.toml
project_id = "rifa-gestion"
major_version = "17"      # PostgreSQL
deno_version = "2"         # Deno runtime
```

### 2.2 Verificar Versiones

```bash
# Versión de la CLI
supabase --version

# Estado del stack local
supabase status

# Migraciones pendientes vs aplicadas
supabase migration list
```

### 2.3 Actualizar Supabase CLI

```bash
# Instalar/actualizar CLI
brew upgrade supabase/tap/supabase   # macOS
npm install -g supabase              # npm
# o descargar release de GitHub

# Reiniciar stack local después de upgrade
supabase stop
supabase start
```

### 2.4 Cambiar Versión de PostgreSQL

```toml
# El cambio de major_version requiere reiniciar el stack
# ¡Cuidado! Puede causar incompatibilidades en migraciones
major_version = "17"
```

> Cambiar de PostgreSQL 15 a 17 requiere verificar que todas las extensiones y queries sean compatibles.

---

## 3. Node.js

### 3.1 `.nvmrc`

```bash
# .nvmrc en apps/web/
20
```

```bash
# Usar la versión del proyecto
nvm use

# Saber qué versión tienes
node --version

# Instalar una versión específica
nvm install 22
nvm use 22
echo "22" > .nvmrc
```

### 3.2 `engines` en package.json

```json
// apps/web/package.json
{
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

Esto da una advertencia temprana si alguien usa una versión incorrecta:

```bash
$ npm install
npm WARN EBADENGINE Unsupported engine {
  package: 'web',
  required: { node: '>=18.0.0' },
  current: { node: '16.0.0' }
}
```

### 3.3 Cuándo Actualizar Node

| Versión | Estado | Acción |
|---|---|---|
| Node 18 | EOL Abril 2025 | Migrar a 20 o 22 |
| Node 20 | Active LTS (actual) | Mantener |
| Node 22 | Active LTS (2025-2026) | Preparar migración |
| Node 23 | Current | No recomendado para producción |

**Regla:** Usa siempre la versión LTS activa que usa tu CI/CD.

---

## 4. Política de Versiones por Ecosistema

| Herramienta | Dónde se declara | Cadencia de actualización |
|---|---|---|
| Flutter SDK | `.fvm/flutter_sdk_version` | Cada 2-3 meses (cada release estable) |
| Dart SDK | Atado a Flutter | Automática con Flutter |
| Supabase CLI | Sistema / npm global | Mensual |
| PostgreSQL | `supabase/config.toml` | Solo si nuevas features lo requieren |
| Deno runtime | `supabase/config.toml` | Cada 3-6 meses |
| Node.js | `.nvmrc` + `engines` | Cada ciclo LTS (~12 meses) |

---

## 5. Ejercicio

Tu equipo trabaja en el monorepo. Flutter acaba de lanzar 3.44.0, Node 22 es ahora LTS, y Supabase CLI 2.0 tiene cambios importantes.

1. Actualiza Flutter a 3.44.0 siguiendo el proceso de 1.4
2. Actualiza los 3 workflows que hardcodean la versión
3. Actualiza `.nvmrc` a Node 22
4. Actualiza `engines` en `apps/web/package.json`
5. Actualiza Supabase CLI y verifica `supabase status`
6. Commitea cada cambio por separado con mensajes semánticos

---

## Resumen

1. **FVM** asegura que todos usen la misma versión de Flutter
2. **Centraliza** la versión en GitHub Variables o un archivo `.env`
3. **Espera 1-2 semanas** antes de adoptar un nuevo Flutter stable (buena práctica empírica, no política oficial)
4. **Supabase CLI** se actualiza independientemente del proyecto
5. **Node.js** se declara en `.nvmrc` y `engines`
6. Cada ecosistema tiene su propia cadencia de actualización

---

## 📚 Referencias

- [Flutter | Compatibility policy](https://docs.flutter.dev/release/compatibility-policy) — Política de soporte de versiones
- [Flutter | SDK archive](https://docs.flutter.dev/release/archive) — Historial de releases estables
- [FVM](https://fvm.app) — Flutter Version Management
- [Node.js | package.json engines](https://docs.npmjs.com/cli/v10/configuring-npm/package-json#engines) — Campo `engines` en package.json

---

> 📖 **Siguiente:** [05-seguridad-auditoria.md](./05-seguridad-auditoria.md) — Auditoría de seguridad en dependencias
