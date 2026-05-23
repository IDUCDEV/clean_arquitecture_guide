# 📚 Clean Architecture Guide para Flutter + Supabase

> Una guía completa y práctica para implementar **Clean Architecture** en tus proyectos Flutter, desde los conceptos básicos hasta la automatización con Supabase.

---

## 🎯 ¿Qué es Clean Architecture?

Clean Architecture es una forma de organizar el código en **capas independientes** donde cada capa tiene una responsabilidad específica:

```
┌─────────────────────────────────────────────┐
│           PRESENTATION (UI)                 │
│   Widgets, Pages, Cubits/BLoCs             │
├─────────────────────────────────────────────┤
│              DOMAIN (Lógica)                 │
│   Entities, UseCases, Repository Interfaces │
├─────────────────────────────────────────────┤
│                DATA (Datos)                  │
│   Models, DataSources, Repository Impl     │
└─────────────────────────────────────────────┘
```

### ¿Por qué usarla?

- ✅ **Código mantenible** - Cada cambio está aislado
- ✅ **Fácil de testear** - Cada capa se prueba por separado
- ✅ **Escalable** - Añadir features sin romper existentes
- ✅ **Framework independiente** - Tu lógica no depende de Flutter

---

## 📁 Estructura de la Guía

La guía está organizada en **6 secciones numeradas** para seguir un orden de aprendizaje lógico:

```
00-DISEÑO-FEATURE/       → Diseño y descomposición de features (¡empieza aquí!)
01-CLEAN-ARCHITECTURE/    → Fundamentos de arquitectura
02-TESTING/              → Cómo probar el código
03-IA-ASSISTANT/         → Cómo usar IA en el desarrollo
04-NIVEL-EXPERTO/         → Técnicas avanzadas de arquitectura
05-SUPABASE/             → Backend + automatización
```

---

### ✏️ Sección 00: Diseño de Features

| Archivo | Descripción |
|---------|-------------|
| [README.md](./00-DISEÑO-FEATURE/README.md) | Filosofía "papel y lápiz" + framework FADER |
| [01-descomposicion-feature.md](./00-DISEÑO-FEATURE/01-descomposicion-feature.md) | Framework FADER: Formular, Actorizar, Descomponer, Entidades, Reglas |
| [01a-practica-carrito.md](./00-DISEÑO-FEATURE/01a-practica-carrito.md) | Práctica: descomponer Carrito de Compras |
| [02-mapeo-capas.md](./00-DISEÑO-FEATURE/02-mapeo-capas.md) | Traducir FADER a las capas de Clean Architecture |
| [02a-practica-carrito-capas.md](./00-DISEÑO-FEATURE/02a-practica-carrito-capas.md) | Práctica: mapear Carrito a capas |
| [03-contratos-primero.md](./00-DISEÑO-FEATURE/03-contratos-primero.md) | Contract-First Design y ADRs |
| [03a-practica-carrito-contratos.md](./00-DISEÑO-FEATURE/03a-practica-carrito-contratos.md) | Práctica: contratos del Carrito |
| [04-flujo-datos.md](./00-DISEÑO-FEATURE/04-flujo-datos.md) | Flujo de datos entre capas |
| [04a-practica-carrito-flujo.md](./00-DISEÑO-FEATURE/04a-practica-carrito-flujo.md) | Práctica: flujo del Carrito |
| [05-caso-completo-reservas.md](./00-DISEÑO-FEATURE/05-caso-completo-reservas.md) | Caso integral: Sistema de Reservas |

**Contenido:** Metodología FADER, descomposición de features, mapeo a capas, contract-first, ADRs, diagramas de flujo.

---

### 📖 Sección 01: Clean Architecture

| Archivo | Descripción |
|---------|-------------|
| [README.md](./01-CLEAN-ARCHITECTURE/README.md) | Índice de la sección |
| [01-guia-completa.md](./01-CLEAN-ARCHITECTURE/01-guia-completa.md) | Guía completa con implementación práctica |

**Contenido:** Las 4 capas, estructura de carpetas, flujo de datos, sistema CRUD, inyección de dependencias con GetIt, templates universales, fpdart.

---

### 🧪 Sección 02: Testing

| Área | Archivos |
|------|-----------|
| Fundamentos | 01-fundamentos.md, 01a-practica-primeros-tests.md |
| Domain | 02-domain-testing.md, 02b-mocktail-guia-completa.md |
| Data | 03-data-testing.md, 03a-practica-fixtures-models.md, 03b-practica-datasources.md, 03c-practica-repositories.md, 03d-practica-notificaciones-email.md |
| Presentation | 04-presentation-testing.md, 04a-practica-cubits-bloc-test.md, 04b-practica-widgets.md |
| Core | 05-core-testing.md, 05a-practica-core-services.md |
| Avanzado | 06-advanced-testing.md, 06a-practica-coverage-ci.md, 06b-intro-integration-tests.md, 06c-practica-flujos-completos.md |
| Mocktail | 02b-mocktail-guia-completa.md (incluye teoría, práctica y migración) |

**Contenido:** Testing por capas, Mocktail, Widget tests, Coverage, CI/CD, tests de integración con Supabase.

---

### 🤖 Sección 03: IA Assistant

| Archivo | Descripción |
|---------|-------------|
| [01-guia-ia.md](./03-IA-ASSISTANT/01-guia-ia.md) | Framework AIDR, prompts optimizados |
| [02-practica-reservas.md](./03-IA-ASSISTANT/02-practica-reservas.md) | Caso de estudio completo |

**Contenido:** Cómo usar IA como asistente, qué delegar y qué hacer manualmente, prompts por capa.

---

### 🚀 Sección 04: Nivel Experto

| Archivo | Descripción |
|---------|-------------|
| [01-fpdart-result-pattern.md](./04-NIVEL-EXPERTO/01-fpdart-result-pattern.md) | Programación funcional |
| [02-di-injectable.md](./04-NIVEL-EXPERTO/02-di-injectable.md) | Inyección de dependencias automatizada |
| [03-comunicacion-features.md](./04-NIVEL-EXPERTO/03-comunicacion-features.md) | Comunicación entre features |
| [04-streams-tiempo-real.md](./04-NIVEL-EXPERTO/04-streams-tiempo-real.md) | Streams y tiempo real |

**Contenido:** fpdart, Injectable, comunicación desacoplada, StreamUseCases.

---

### ☁️ Sección 05: Supabase

#### PARTE 1: Desarrollo Local
| Archivo | Descripción |
|---------|-------------|
| [01-configuracion-inicial.md](./05-SUPABASE/PARTE-1-DESARROLLO/01-configuracion-inicial.md) | Docker, CLI, init |
| [02-estructura-proyecto-supabase.md](./05-SUPABASE/PARTE-1-DESARROLLO/02-estructura-proyecto-supabase.md) | Archivos y carpetas |
| [03-makefile-integrado.md](./05-SUPABASE/PARTE-1-DESARROLLO/03-makefile-integrado.md) | Makefile completo |
| [04-variables-entorno.md](./05-SUPABASE/PARTE-1-DESARROLLO/04-variables-entorno.md) | Gestión .env |
| [05-migraciones-y-seeds.md](./05-SUPABASE/PARTE-1-DESARROLLO/05-migraciones-y-seeds.md) | Migraciones |
| [06-integracion-flutter.md](./05-SUPABASE/PARTE-1-DESARROLLO/06-integracion-flutter.md) | Integración Flutter |
| [07-testing-local-supabase.md](./05-SUPABASE/PARTE-1-DESARROLLO/07-testing-local-supabase.md) | Tests de BD |

#### PARTE 2: Producción
| Archivo | Descripción |
|---------|-------------|
| [01-opciones-hosting.md](./05-SUPABASE/PARTE-2-PRODUCTION/01-opciones-hosting.md) | Comparativa VPS |
| [02-supabase-self-hosted-docker.md](./05-SUPABASE/PARTE-2-PRODUCTION/02-supabase-self-hosted-docker.md) | Docker deployment |
| [03-configuracion-produccion.md](./05-SUPABASE/PARTE-2-PRODUCTION/03-configuracion-produccion.md) | Config producción |
| [04-migracion-local-a-produccion.md](./05-SUPABASE/PARTE-2-PRODUCTION/04-migracion-local-a-produccion.md) | Migración schema |
| [05-backup-y-mantenimiento.md](./05-SUPABASE/PARTE-2-PRODUCTION/05-backup-y-mantenimiento.md) | Backups |
| [06-alternativas-externas.md](./05-SUPABASE/PARTE-2-PRODUCTION/06-alternativas-externas.md) | Firebase, Appwrite |

#### PARTE 3: CI/CD
| Archivo | Descripción |
|---------|-------------|
| [01-makefile-universal.md](./05-SUPABASE/PARTE-3-CI_CD/01-makefile-universal.md) | Template Makefile |
| [02-workflows-github-actions.md](./05-SUPABASE/PARTE-3-CI_CD/02-workflows-github-actions.md) | GitHub Actions |
| [03-patrones-extrapolables.md](./05-SUPABASE/PARTE-3-CI_CD/03-patrones-extrapolables.md) | Reutilizar en nuevos proyectos |
| [04-git-hooks-y-commits.md](./05-SUPABASE/PARTE-3-CI_CD/04-git-hooks-y-commits.md) | commitlint, hooks |

---

## 🚀 Orden de Aprendizaje Sugerido

```
00-DISEÑO-FEATURE        → Diseño de features (6-8 horas) — ¡empieza aquí!
    ↓
01-CLEAN-ARCHITECTURE    → Fundamentos (4-6 horas)
    ↓
02-TESTING               → Testing (15-20 horas)
    ↓
03-IA-ASSISTANT          → IA en desarrollo (2-3 horas)
    ↓
04-NIVEL-EXPERTO         → Técnicas avanzadas (6-8 horas)
    ↓
05-SUPABASE              → Backend + automatización (10-15 horas)
```

---

## 📦 Dependencias Recomendadas

```yaml
dependencies:
  flutter_bloc: ^8.1.3
  equatable: ^2.0.5
  get_it: ^7.6.4
  fpdart: ^1.2.0
  dio: ^5.3.3
  supabase_flutter: ^2.5.0
  go_router: ^12.1.3

dev_dependencies:
  bloc_test: ^9.1.0
  mockito: ^5.4.0
  build_runner: ^2.4.7
```

---

## 🤝 Contribuir

Esta guía es de código abierto. Si quieres mejorarla:

1. Haz fork del repositorio
2. Crea una rama para tu feature
3. Envía un pull request

---

## 📄 Licencia

MIT License - Libre de usar y modificar.

---

**Última actualización:** 2026-05-15  
**Versión:** 5.1.0