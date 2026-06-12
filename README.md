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

La guía está organizada en **7 secciones numeradas** para seguir un orden de aprendizaje lógico:

```
01-CLEAN-ARCHITECTURE/         → Fundamentos de arquitectura
02-DISENIO-FEATURE/            → Diseño y descomposición de features (¡empieza aquí!)
03-SUPABASE/                   → Backend + automatización
04-ALMACENAMIENTO-LOCAL/       → Almacenamiento local con Isar
05-TESTING/                    → Cómo probar el código
06-NIVEL-EXPERTO/              → Técnicas avanzadas de arquitectura
07-IA-ASSISTANT/               → Cómo usar IA en el desarrollo
```

---

### 📖 Sección 01: Clean Architecture

| Archivo | Descripción |
|---------|-------------|
| [README.md](./01-CLEAN-ARCHITECTURE/README.md) | Índice de la sección |
| [01-introduccion-y-filosofia.md](./01-CLEAN-ARCHITECTURE/01-introduccion-y-filosofia.md) | Introducción y filosofía de Clean Architecture |
| [02-las-4-capas.md](./01-CLEAN-ARCHITECTURE/02-las-4-capas.md) | Las 4 capas en detalle |
| [03-estructura-de-carpetas.md](./01-CLEAN-ARCHITECTURE/03-estructura-de-carpetas.md) | Estructura de carpetas |
| [04-flujo-de-datos.md](./01-CLEAN-ARCHITECTURE/04-flujo-de-datos.md) | Flujo de datos entre capas |
| [05-implementacion-crud-intro.md](./01-CLEAN-ARCHITECTURE/05-implementacion-crud-intro.md) | CRUD: Requerimientos y estructura |
| [05a-domain-layer.md](./01-CLEAN-ARCHITECTURE/05a-domain-layer.md) | CRUD: Domain Layer |
| [05b-data-layer.md](./01-CLEAN-ARCHITECTURE/05b-data-layer.md) | CRUD: Data Layer |
| [05c-presentation-ui-layer.md](./01-CLEAN-ARCHITECTURE/05c-presentation-ui-layer.md) | CRUD: Presentation y UI |
| [06-inyeccion-de-dependencias.md](./01-CLEAN-ARCHITECTURE/06-inyeccion-de-dependencias.md) | Inyección de dependencias con GetIt |
| [07-testing-por-capas.md](./01-CLEAN-ARCHITECTURE/07-testing-por-capas.md) | Testing por capas |
| [08-templates-universales.md](./01-CLEAN-ARCHITECTURE/08-templates-universales.md) | Templates universales |
| [09-decisiones-de-arquitectura.md](./01-CLEAN-ARCHITECTURE/09-decisiones-de-arquitectura.md) | Decisiones de arquitectura |
| [10-migracion-codigo-espagueti.md](./01-CLEAN-ARCHITECTURE/10-migracion-codigo-espagueti.md) | Migración desde código espagueti |
| [99-apendice-dependencias.md](./01-CLEAN-ARCHITECTURE/99-apendice-dependencias.md) | Apéndice: dependencias y resumen |

**Contenido:** Las 4 capas, estructura de carpetas, flujo de datos, sistema CRUD completo (domain, data, presentation), inyección de dependencias con GetIt, templates universales, migración desde código espagueti.

---

### ✏️ Sección 02: Diseño de Features

| Archivo | Descripción |
|---------|-------------|
| [README.md](./02-DISENIO-FEATURE/README.md) | Filosofía "papel y lápiz" + framework FADER |
| [01-descomposicion-feature.md](./02-DISENIO-FEATURE/01-descomposicion-feature.md) | Framework FADER: Formular, Actorizar, Descomponer, Entidades, Reglas |
| [01a-practica-carrito.md](./02-DISENIO-FEATURE/01a-practica-carrito.md) | Práctica: descomponer Carrito de Compras |
| [02-mapeo-capas.md](./02-DISENIO-FEATURE/02-mapeo-capas.md) | Traducir FADER a las capas de Clean Architecture |
| [02a-practica-carrito-capas.md](./02-DISENIO-FEATURE/02a-practica-carrito-capas.md) | Práctica: mapear Carrito a capas |
| [03-contratos-primero.md](./02-DISENIO-FEATURE/03-contratos-primero.md) | Contract-First Design y ADRs |
| [03a-practica-carrito-contratos.md](./02-DISENIO-FEATURE/03a-practica-carrito-contratos.md) | Práctica: contratos del Carrito |
| [04-flujo-datos.md](./02-DISENIO-FEATURE/04-flujo-datos.md) | Flujo de datos entre capas |
| [04a-practica-carrito-flujo.md](./02-DISENIO-FEATURE/04a-practica-carrito-flujo.md) | Práctica: flujo del Carrito |
| [05-caso-completo-reservas.md](./02-DISENIO-FEATURE/05-caso-completo-reservas.md) | Caso integral: Sistema de Reservas |

**Contenido:** Metodología FADER, descomposición de features, mapeo a capas, contract-first, ADRs, diagramas de flujo.

---

### ☁️ Sección 03: Supabase

#### PARTE 1: Desarrollo Local
| Archivo | Descripción |
|---------|-------------|
| [01-configuracion-inicial.md](./03-SUPABASE/PARTE-1-DESARROLLO/01-configuracion-inicial.md) | Docker, CLI, init |
| [02-estructura-proyecto-supabase.md](./03-SUPABASE/PARTE-1-DESARROLLO/02-estructura-proyecto-supabase.md) | Archivos y carpetas |
| [03-makefile-integrado.md](./03-SUPABASE/PARTE-1-DESARROLLO/03-makefile-integrado.md) | Makefile completo |
| [04-variables-entorno.md](./03-SUPABASE/PARTE-1-DESARROLLO/04-variables-entorno.md) | Gestión .env |
| [05-migraciones-y-seeds.md](./03-SUPABASE/PARTE-1-DESARROLLO/05-migraciones-y-seeds.md) | Migraciones |
| [06-integracion-flutter.md](./03-SUPABASE/PARTE-1-DESARROLLO/06-integracion-flutter.md) | Integración Flutter |
| [07-testing-local-supabase.md](./03-SUPABASE/PARTE-1-DESARROLLO/07-testing-local-supabase.md) | Tests de BD |

#### PARTE 2: Producción
| Archivo | Descripción |
|---------|-------------|
| [01-opciones-hosting.md](./03-SUPABASE/PARTE-2-PRODUCTION/01-opciones-hosting.md) | Comparativa VPS |
| [02-supabase-self-hosted-docker.md](./03-SUPABASE/PARTE-2-PRODUCTION/02-supabase-self-hosted-docker.md) | Docker deployment |
| [03-configuracion-produccion.md](./03-SUPABASE/PARTE-2-PRODUCTION/03-configuracion-produccion.md) | Config producción |
| [04-migracion-local-a-produccion.md](./03-SUPABASE/PARTE-2-PRODUCTION/04-migracion-local-a-produccion.md) | Migración schema |
| [05-backup-y-mantenimiento.md](./03-SUPABASE/PARTE-2-PRODUCTION/05-backup-y-mantenimiento.md) | Backups |
| [06-alternativas-externas.md](./03-SUPABASE/PARTE-2-PRODUCTION/06-alternativas-externas.md) | Firebase, Appwrite |

#### PARTE 3: CI/CD
| Archivo | Descripción |
|---------|-------------|
| [01-makefile-universal.md](./03-SUPABASE/PARTE-3-CI_CD/01-makefile-universal.md) | Template Makefile |
| [02-workflows-github-actions.md](./03-SUPABASE/PARTE-3-CI_CD/02-workflows-github-actions.md) | GitHub Actions |
| [03-patrones-extrapolables.md](./03-SUPABASE/PARTE-3-CI_CD/03-patrones-extrapolables.md) | Reutilizar en nuevos proyectos |
| [04-git-hooks-y-commits.md](./03-SUPABASE/PARTE-3-CI_CD/04-git-hooks-y-commits.md) | commitlint, hooks |

---

### 🗄️ Sección 04: Almacenamiento Local con Isar

| Archivo | Descripción |
|---------|-------------|
| [01-isar-introduccion.md](./04-ALMACENAMIENTO-LOCAL/01-isar-introduccion.md) | ¿Qué es Isar? Diferencias entre variantes, setup |
| [02-modelos-operaciones.md](./04-ALMACENAMIENTO-LOCAL/02-modelos-operaciones.md) | Colecciones, CRUD, Queries, TTL |
| [03-implementacion-local-datasource.md](./04-ALMACENAMIENTO-LOCAL/03-implementacion-local-datasource.md) | IsarService, LocalDataSource, CacheManager, UserSessionImpl |
| [03e-practica-local-datasource-isar.md](./05-TESTING/03-data/03e-practica-local-datasource-isar.md) | Testing con Isar real, ejercicios completos (en sección 05-TESTING) |

**Contenido:** Isar Community como base de datos local embebida, patrón LocalDataSource, TTL, CacheManager, testing con instancias reales.

---

### 🧪 Sección 05: Testing

| Subdirectorio | Archivo | Descripción |
|---------------|---------|-------------|
| **Fundamentos** | [01-fundamentos/01-fundamentos.md](./05-TESTING/01-fundamentos/01-fundamentos.md) | Fundamentos de testing en Clean Architecture |
| | [01-fundamentos/01a-practica-primeros-tests.md](./05-TESTING/01-fundamentos/01a-practica-primeros-tests.md) | Práctica: primeros tests |
| **Domain** | [02-domain/02-domain-testing.md](./05-TESTING/02-domain/02-domain-testing.md) | Testing de la capa Domain |
| | [02-domain/02b-mocktail-guia-completa.md](./05-TESTING/02-domain/02b-mocktail-guia-completa.md) | Mocktail: teoría, práctica y migración |
| **Data** | [03-data/03-data-testing.md](./05-TESTING/03-data/03-data-testing.md) | Testing de la capa Data |
| | [03-data/03a-practica-fixtures-models.md](./05-TESTING/03-data/03a-practica-fixtures-models.md) | Práctica: fixtures y models |
| | [03-data/03b-practica-datasources.md](./05-TESTING/03-data/03b-practica-datasources.md) | Práctica: datasources |
| | [03-data/03c-practica-repositories.md](./05-TESTING/03-data/03c-practica-repositories.md) | Práctica: repositories |
| | [03-data/03d-practica-notificaciones-email.md](./05-TESTING/03-data/03d-practica-notificaciones-email.md) | Práctica: notificaciones email |
| | [03-data/03e-practica-local-datasource-isar.md](./05-TESTING/03-data/03e-practica-local-datasource-isar.md) | Práctica: LocalDataSource con Isar |
| | [03-data/03f-supabase-testing.md](./05-TESTING/03-data/03f-supabase-testing.md) | Testing con Supabase |
| | [03-data/03g-practica-supabase-datasources.md](./05-TESTING/03-data/03g-practica-supabase-datasources.md) | Práctica: Supabase datasources |
| | [03-data/03h-practica-supabase-mock-http-client.md](./05-TESTING/03-data/03h-practica-supabase-mock-http-client.md) | Práctica: mock HTTP client en Supabase |
| **Presentation** | [04-presentation/04-presentation-testing.md](./05-TESTING/04-presentation/04-presentation-testing.md) | Testing de la capa Presentation |
| | [04-presentation/04a-practica-cubits-bloc-test.md](./05-TESTING/04-presentation/04a-practica-cubits-bloc-test.md) | Práctica: Cubits y Bloc tests |
| | [04-presentation/04b-practica-widgets.md](./05-TESTING/04-presentation/04b-practica-widgets.md) | Práctica: Widget tests |
| **Core** | [05-core/05-core-testing.md](./05-TESTING/05-core/05-core-testing.md) | Testing de servicios core |
| | [05-core/05a-practica-core-services.md](./05-TESTING/05-core/05a-practica-core-services.md) | Práctica: core services |
| **Avanzado** | [06-advanced/06-advanced-testing.md](./05-TESTING/06-advanced/06-advanced-testing.md) | Técnicas avanzadas de testing |
| | [06-advanced/06a-practica-coverage-ci.md](./05-TESTING/06-advanced/06a-practica-coverage-ci.md) | Práctica: coverage y CI |
| | [06-advanced/06b-intro-integration-tests.md](./05-TESTING/06-advanced/06b-intro-integration-tests.md) | Introducción a integration tests |
| | [06-advanced/06c-practica-flujos-completos.md](./05-TESTING/06-advanced/06c-practica-flujos-completos.md) | Práctica: flujos completos |

**Contenido:** Testing por capas, Mocktail, Widget tests, Supabase testing, coverage, CI/CD, tests de integración.

---

### 🚀 Sección 06: Nivel Experto

| Archivo | Descripción |
|---------|-------------|
| [01-fpdart-result-pattern.md](./06-NIVEL-EXPERTO/01-fpdart-result-pattern.md) | Programación funcional |
| [02-di-injectable.md](./06-NIVEL-EXPERTO/02-di-injectable.md) | Inyección de dependencias automatizada |
| [03-comunicacion-features.md](./06-NIVEL-EXPERTO/03-comunicacion-features.md) | Comunicación entre features |
| [04-streams-tiempo-real.md](./06-NIVEL-EXPERTO/04-streams-tiempo-real.md) | Streams y tiempo real |

**Contenido:** fpdart, Injectable, comunicación desacoplada, StreamUseCases.

---

### 🤖 Sección 07: IA Assistant

| Archivo | Descripción |
|---------|-------------|
| [01-guia-ia.md](./07-IA-ASSISTANT/01-guia-ia.md) | Framework AIDR, prompts optimizados |
| [02-practica-reservas.md](./07-IA-ASSISTANT/02-practica-reservas.md) | Caso de estudio completo |

**Contenido:** Cómo usar IA como asistente, qué delegar y qué hacer manualmente, prompts por capa.

---

## 🚀 Orden de Aprendizaje Sugerido

```
02-DISENIO-FEATURE            → Diseño de features (6-8 horas) — ¡empieza aquí!
    ↓
01-CLEAN-ARCHITECTURE        → Fundamentos (4-6 horas)
    ↓
05-TESTING                   → Testing (15-20 horas)
    ↓
07-IA-ASSISTANT              → IA en desarrollo (2-3 horas)
    ↓
06-NIVEL-EXPERTO             → Técnicas avanzadas (6-8 horas)
    ↓
03-SUPABASE                  → Backend + automatización (10-15 horas)
    ↓
04-ALMACENAMIENTO-LOCAL      → Almacenamiento local con Isar (4-6 horas)
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

**Última actualización:** 2026-06-11  
**Versión:** 6.0.0
