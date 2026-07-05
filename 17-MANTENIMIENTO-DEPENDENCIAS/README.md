# 17 — Mantenimiento de Dependencias

> Aprende a mantener tu proyecto sano, actualizado, seguro y reproducible en el tiempo. Este módulo cubre el **ciclo de vida completo** de las dependencias: cómo declararlas, actualizarlas, automatizarlas y auditar su seguridad.

---

## 🎯 Objetivos

- Entender la estrategia de versionado (rangos caret, pinning exacto, SHA)
- Actualizar dependencias Flutter y npm sin romper el proyecto
- Configurar Dependabot y Renovate como parte del workflow del equipo
- Mantener el SDK (Flutter, Supabase, Node) en versiones consistentes
- Detectar y responder a vulnerabilidades de seguridad
- Planificar migraciones cuando un paquete se depreca o llega a EOL

---

## 📋 Índice

| Archivo | Descripción | Nivel |
|---------|-------------|-------|
| [01-fundamentos-dependencias.md](./01-fundamentos-dependencias.md) | Cómo declarar dependencias: rangos caret, pinning exacto, lockfile, resolución de conflictos | 🔤 Básico |
| [02-flujo-actualizacion.md](./02-flujo-actualizacion.md) | `pub outdated`, `pub upgrade`, manejo de breaking changes, `dart fix` | 📦 Medio |
| [03-automatizacion-dependabot-renovate.md](./03-automatizacion-dependabot-renovate.md) | Configurar Dependabot, Renovate, CI con auditorías semanales | 🤖 Medio |
| [04-mantenimiento-sdk-ecosistema.md](./04-mantenimiento-sdk-ecosistema.md) | Flutter SDK, Supabase CLI, Node.js: versionado y actualización segura | 📦 Medio |
| [05-seguridad-auditoria.md](./05-seguridad-auditoria.md) | `dart pub deps`, OSV, npm audit, Dependabot security updates, CVSS | 🔐 Medio |
| [06-deprecacion-eol-migraciones.md](./06-deprecacion-eol-migraciones.md) | Señales de deprecación, proceso de migración, EOL de Flutter/Dart | 🏗️ Alto |
| [07-makefile-ci-objetivos.md](./07-makefile-ci-objetivos.md) | Targets de dependencias en Makefile y workflows CI de monitoreo continuo | 🛠️ Alto |

---

## 🧠 Competencias que desarrollarás

1. Leer un `pubspec.yaml` y decidir si la constraint es correcta
2. Diagnosticar conflictos de dependencias y resolverlos
3. Actualizar un paquete de forma segura (changelog → upgrade → fix → test)
4. Configurar Dependabot para un monorepo Flutter + npm + Actions
5. Mantener Flutter SDK, Supabase CLI y Node.js sincronizados en el equipo
6. Detectar vulnerabilidades y responder según severidad
7. Planificar la migración cuando un paquete se depreca

---

## 🔗 Prerrequisitos

| Módulo | Por qué |
|--------|---------|
| [12-GIT-FLOW/04-fvm-version-management.md](../12-GIT-FLOW-CONVENTIONAL-COMMITS/04-fvm-version-management.md) | FVM para gestionar versiones de Flutter SDK |
| [10-MAKEFILE/](../10-MAKEFILE/) | Sintaxis básica de Makefile (referenciada en 07) |
| [11-GITHUB-ACTIONS/](../11-GITHUB-ACTIONS/) | Sintaxis básica de workflows (referenciada en 03 y 07) |

---

**Nivel:** Básico → Avanzado  
**Tiempo estimado:** 6-8 horas  
**Ejercicios:** 6+
