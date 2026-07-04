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

La guía está organizada en **16 módulos numerados** para seguir un orden de aprendizaje lógico:

```
01-CLEAN-ARCHITECTURE/         → Fundamentos de arquitectura
02-DISENIO-FEATURE/            → Diseño y descomposición de features (¡empieza aquí!)
03-SUPABASE/                   → Backend + automatización
04-ALMACENAMIENTO-LOCAL/       → Almacenamiento local con Isar
05-TESTING/                    → Cómo probar el código
06-NIVEL-EXPERTO/              → Técnicas avanzadas de arquitectura
07-IA-ASSISTANT/               → Cómo usar IA en el desarrollo
08-PENCIL/                     → Diseño visual con Pencil
09-ESTRUCTURA-DATOS-OOP/       → Estructuras de datos con OOP en Dart
10-MAKEFILE/                   → Dominio de Makefiles para Flutter
11-GITHUB-ACTIONS/             → Automatización y CI/CD
12-GIT-FLOW-CONVENTIONAL-COMMITS/ → Git flow, conventional commits, husky
13-EDGE-FUNCTIONS-DENO/        → Edge Functions con Deno + Supabase
14-GOOGLE-PLAY-RELEASE/        → Publicación en Play Store y CI/CD
15-WIDGETS-FLUTTER/            → Widgets de Flutter (sin state management)
16-BLOC-CUBIT/                 → State management con BLoC/Cubit
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
| [07-templates-universales.md](./01-CLEAN-ARCHITECTURE/07-templates-universales.md) | Templates universales |
| [08-decisiones-de-arquitectura.md](./01-CLEAN-ARCHITECTURE/08-decisiones-de-arquitectura.md) | Decisiones de arquitectura |
| [09-migracion-codigo-espagueti.md](./01-CLEAN-ARCHITECTURE/09-migracion-codigo-espagueti.md) | Migración desde código espagueti |
| [10-apendice-dependencias.md](./01-CLEAN-ARCHITECTURE/10-apendice-dependencias.md) | Apéndice: dependencias y resumen |

**Contenido:** Las 4 capas, estructura de carpetas, flujo de datos, sistema CRUD completo (domain, data, presentation), inyección de dependencias con GetIt, templates universales, decisiones de arquitectura, migración desde código espagueti.

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

### 🖊️ Sección 08: Pencil — Diseño Visual

| Archivo | Descripción |
|---------|-------------|
| [README.md](./08-PENCIL/README.md) | Índice de la sección |
| [06-pencil-diseno-visual.md](./08-PENCIL/06-pencil-diseno-visual.md) | La interfaz de Pencil: toolbar, paneles, componentes, atajos |
| [06a-practica-login.md](./08-PENCIL/06a-practica-login.md) | Práctica: diseñar pantalla de Login |
| [06b-practica-dashboard.md](./08-PENCIL/06b-practica-dashboard.md) | Práctica: Dashboard de Ventas con variables |
| [06c-practica-design-system.md](./08-PENCIL/06c-practica-design-system.md) | Práctica: Sistema de Diseño (componentes, slots, librerías) |
| [06d-practica-componentes-ui.md](./08-PENCIL/06d-practica-componentes-ui.md) | Práctica: Biblioteca de componentes UI estándar |

**Contenido:** Pencil como herramienta de diseño vectorial en el IDE. Uso manual sin IA — solo mouse, teclado y paneles.

---

### 📊 Sección 09: Estructuras de Datos con OOP

| Archivo | Descripción |
|---------|-------------|
| [README.md](./09-ESTRUCTURA-DATOS-OOP/README.md) | Índice de la sección |
| [01-sistema-tipos.md](./09-ESTRUCTURA-DATOS-OOP/01-sistema-tipos.md) | Sistema de tipos en Dart (null safety, genéricos, `var`/`final`/`const`) |
| [02-colecciones-fundamentos.md](./09-ESTRUCTURA-DATOS-OOP/02-colecciones-fundamentos.md) | `List`, `Set`, `Map` — constructores, operaciones, performance |
| [03-metodos-funcionales-listas.md](./09-ESTRUCTURA-DATOS-OOP/03-metodos-funcionales-listas.md) | `map`, `where`, `reduce`, `fold`, `expand`, encadenamiento |
| [04-manipulacion-mapas.md](./09-ESTRUCTURA-DATOS-OOP/04-manipulacion-mapas.md) | `Map.fromIterable`, `putIfAbsent`, `update`, group-by, merge |
| [05-algoritmos-colecciones.md](./09-ESTRUCTURA-DATOS-OOP/05-algoritmos-colecciones.md) | `sort`, `Comparable`, `Comparator`, búsqueda, paginación |
| [06-oop-modelado-datos.md](./09-ESTRUCTURA-DATOS-OOP/06-oop-modelado-datos.md) | Entidades, Value Objects, `Equatable`, `copyWith`, `fromJson`/`toJson` |
| [07-patrones-manipulacion.md](./09-ESTRUCTURA-DATOS-OOP/07-patrones-manipulacion.md) | Patrones reales: fetch → filter → transform → aggregate |
| [08-ejercicios-basicos.md](./09-ESTRUCTURA-DATOS-OOP/08-ejercicios-basicos.md) | 10 ejercicios de fundamentos |
| [09-ejercicios-intermedios.md](./09-ESTRUCTURA-DATOS-OOP/09-ejercicios-intermedios.md) | 10 ejercicios con datos estructurados |
| [10-ejercicios-avanzados.md](./09-ESTRUCTURA-DATOS-OOP/10-ejercicios-avanzados.md) | 5 ejercicios integradores (mini-pipeline) |
| [11-recursos-practica.md](./09-ESTRUCTURA-DATOS-OOP/11-recursos-practica.md) | Dartpad, Codewars, Exercism, LeetCode — recursos para practicar |

**Contenido:** Sistema de tipos, colecciones, métodos funcionales, manipulación de mapas, algoritmos, modelado OOP, 25+ ejercicios prácticos con casos del dominio real, guía de recursos externos.

---

### 🛠️ Sección 10: Makefile Mastery

| Archivo | Descripción |
|---------|-------------|
| [README.md](./10-MAKEFILE/README.md) | Índice de la sección |
| [01-que-es-make.md](./10-MAKEFILE/01-que-es-make.md) | ¿Qué es Make? ¿Por qué Makefile y no solo scripts? |
| [02-sintaxis-basica.md](./10-MAKEFILE/02-sintaxis-basica.md) | Targets, prerequisites, recipes, `.PHONY`, variables |
| [03-variables-y-shell.md](./10-MAKEFILE/03-variables-y-shell.md) | `$(shell ...)`, `awk`, `sed`, debugging |
| [04-analisis-makefile-real.md](./10-MAKEFILE/04-analisis-makefile-real.md) | Recorrido línea por línea del Makefile del monorepo |
| [05-creacion-personalizada.md](./10-MAKEFILE/05-creacion-personalizada.md) | Template limpio para nuevos proyectos |
| [06-make-en-ci.md](./10-MAKEFILE/06-make-en-ci.md) | Cómo se invoca Make desde GitHub Actions |
| [07-ejercicios.md](./10-MAKEFILE/07-ejercicios.md) | Práctica: leer, modificar y crear Makefiles |

**Contenido:** Fundamentos de Make, sintaxis, variables, funciones shell, análisis del Makefile real del proyecto, creación personalizada, integración con CI.

---

### 🤖 Sección 11: GitHub Actions + Automatización

| Archivo | Descripción |
|---------|-------------|
| [README.md](./11-GITHUB-ACTIONS/README.md) | Índice de la sección |
| [01-conceptos.md](./11-GITHUB-ACTIONS/01-conceptos.md) | Workflows, jobs, steps, runners, eventos trigger |
| [02-sintaxis-yaml.md](./11-GITHUB-ACTIONS/02-sintaxis-yaml.md) | Anatomía de un workflow: `on:`, `jobs:`, `steps:`, `uses:`, `run:` |
| [03-actions-esenciales.md](./11-GITHUB-ACTIONS/03-actions-esenciales.md) | `subosito/flutter-action`, `supabase/setup-cli`, `actions/cache` |
| [04-workflows-analisis.md](./11-GITHUB-ACTIONS/04-workflows-analisis.md) | Recorrido de los 6 workflows reales del proyecto |
| [05-secrets-envs-matrix.md](./11-GITHUB-ACTIONS/05-secrets-envs-matrix.md) | Secrets, entornos, matrix builds, path filtering |
| [06-monorepo-avanzado.md](./11-GITHUB-ACTIONS/06-monorepo-avanzado.md) | Estrategias para monorepo, reutilización, caching |
| [07-ejercicios.md](./11-GITHUB-ACTIONS/07-ejercicios.md) | Práctica: crear workflows desde cero |

**Contenido:** Conceptos de CI/CD, sintaxis YAML, actions esenciales, análisis de workflows reales, secrets, matrix builds, estrategias para monorepo.

---

### 🔀 Sección 12: Git Flow + Conventional Commits

| Archivo | Descripción |
|---------|-------------|
| [01-conventional-commits.md](./12-GIT-FLOW-CONVENTIONAL-COMMITS/01-conventional-commits.md) | Conventional Commits: formato, tipos, ejemplos por escenario |
| [02-husky-lint-staged.md](./12-GIT-FLOW-CONVENTIONAL-COMMITS/02-husky-lint-staged.md) | Husky + lint-staged: automatización antes del commit |
| [03-commitizen-commitlint.md](./12-GIT-FLOW-CONVENTIONAL-COMMITS/03-commitizen-commitlint.md) | Commitizen + commitlint: asistentes interactivos |
| [04-fvm-version-management.md](./12-GIT-FLOW-CONVENTIONAL-COMMITS/04-fvm-version-management.md) | FVM: gestión de versiones de Flutter |
| [05-flujo-ramas-estrategias.md](./12-GIT-FLOW-CONVENTIONAL-COMMITS/05-flujo-ramas-estrategias.md) | Estrategias de ramas, Git Flow, Trunk-based |

**Contenido:** Conventional Commits, automatización con Husky/lint-staged, commitizen, FVM, estrategias de ramas.

---

### ⚡ Sección 13: Edge Functions con Deno

| Archivo | Descripción |
|---------|-------------|
| [01-edge-functions-fundamentos.md](./13-EDGE-FUNCTIONS-DENO/01-edge-functions-fundamentos.md) | Deno, Supabase Edge Functions, despliegue local |
| [02-cron-triggers.md](./13-EDGE-FUNCTIONS-DENO/02-cron-triggers.md) | Cron jobs programados con Edge Functions |
| [03-rpc-postgresql.md](./13-EDGE-FUNCTIONS-DENO/03-rpc-postgresql.md) | Llamadas RPC a PostgreSQL desde Edge Functions |
| [04-integracion-flutter-supabase.md](./13-EDGE-FUNCTIONS-DENO/04-integracion-flutter-supabase.md) | Consumir Edge Functions desde Flutter |

**Contenido:** Deno, Edge Functions, cron triggers, RPC, integración Flutter.

---

### 📱 Sección 14: Google Play Release

| Archivo | Descripción |
|---------|-------------|
| [01-generar-aab-keystore.md](./14-GOOGLE-PLAY-RELEASE/01-generar-aab-keystore.md) | Generar AAB, keystore, signing config |
| [02-play-console-listing.md](./14-GOOGLE-PLAY-RELEASE/02-play-console-listing.md) | Play Console: listing, assets, calificaciones |
| [03-release-tracks.md](./14-GOOGLE-PLAY-RELEASE/03-release-tracks.md) | Internal, closed, open testing, production tracks |
| [04-play-signing-inapp-updates.md](./14-GOOGLE-PLAY-RELEASE/04-play-signing-inapp-updates.md) | Play App Signing, actualizaciones in-app |
| [05-ci-cd-automatizado.md](./14-GOOGLE-PLAY-RELEASE/05-ci-cd-automatizado.md) | CI/CD automatizado hasta Play Store |

**Contenido:** Generación de AAB, Play Console, release tracks, Play Signing, in-app updates, CI/CD.

---

### 🧩 Sección 15: Widgets de Flutter

| Archivo | Descripción |
|---------|-------------|
| [README.md](./15-WIDGETS-FLUTTER/README.md) | Índice del módulo |
| [01-fundamentos-widgets.md](./15-WIDGETS-FLUTTER/01-fundamentos-widgets.md) | Widget, Element, RenderObject, BuildContext, keys |
| [02-widgets-basicos-y-atomizacion.md](./15-WIDGETS-FLUTTER/02-widgets-basicos-y-atomizacion.md) | Text, Image, Icon, Button, Chip, Avatares, atomización |
| [03-layout-y-navegacion.md](./15-WIDGETS-FLUTTER/03-layout-y-navegacion.md) | Row, Column, Stack, Expanded, Navigator, GoRouter |
| [04-interaccion-y-formularios.md](./15-WIDGETS-FLUTTER/04-interaccion-y-formularios.md) | TextField, Form, validación, FocusNode, debounce |
| [05-listas-y-scroll.md](./15-WIDGETS-FLUTTER/05-listas-y-scroll.md) | ListView, GridView, CustomScrollView, Slivers, pull-to-refresh |
| [06-datos-estados-y-ciclo-de-vida.md](./15-WIDGETS-FLUTTER/06-datos-estados-y-ciclo-de-vida.md) | StatefulWidget, initState, dispose, StreamBuilder |
| [07-animaciones.md](./15-WIDGETS-FLUTTER/07-animaciones.md) | AnimatedContainer, Hero, TweenAnimationBuilder |
| [08-estrategias-composicion.md](./15-WIDGETS-FLUTTER/08-estrategias-composicion.md) | Composición vs herencia, patrones slot, builder, child |
| [09-patrones-renderizacion.md](./15-WIDGETS-FLUTTER/09-patrones-renderizacion.md) | Conditional rendering, loading/error/data pattern |
| [10-perf-y-buenas-practicas.md](./15-WIDGETS-FLUTTER/10-perf-y-buenas-practicas.md) | const constructors, RepaintBoundary, keys, evitar rebuilds |
| [11-arsenal-completo-widgets.md](./15-WIDGETS-FLUTTER/11-arsenal-completo-widgets.md) | +150 widgets organizados por categoría |

**Contenido:** Widgets puros de Flutter (sin state management). Fundamentos, layout, formularios, scroll, animaciones, composición, performance.

---

### 🔷 Sección 16: BLoC / Cubit — State Management

| Archivo | Descripción |
|---------|-------------|
| [README.md](./16-BLOC-CUBIT/README.md) | Índice, dependencias, relaciones entre módulos |
| [01-conceptos-bloc-cubit.md](./16-BLOC-CUBIT/01-conceptos-bloc-cubit.md) | Bloc vs Cubit, streams, transiciones, flow diagram |
| [02-vs-otros-state-management.md](./16-BLOC-CUBIT/02-vs-otros-state-management.md) | setState, Provider, Riverpod, GetX, BLoC |
| [03-cubit-basico.md](./16-BLOC-CUBIT/03-cubit-basico.md) | ContadorCubit, LoginCubit, pantalla completa |
| [04-bloc-eventos.md](./16-BLOC-CUBIT/04-bloc-eventos.md) | ProductoBloc, eventos, paginación, debounce |
| [05-widgets-flutter-bloc-p1.md](./16-BLOC-CUBIT/05-widgets-flutter-bloc-p1.md) | BlocProvider, BlocBuilder, context.read/watch |
| [06-widgets-flutter-bloc-p2.md](./16-BLOC-CUBIT/06-widgets-flutter-bloc-p2.md) | BlocListener, BlocConsumer, BlocSelector |
| [07-ejemplo-login.md](./16-BLOC-CUBIT/07-ejemplo-login.md) | Login con validación + tests |
| [08-ejemplo-lista-filtros.md](./16-BLOC-CUBIT/08-ejemplo-lista-filtros.md) | Lista con búsqueda, filtros, infinite scroll |
| [09-ejemplo-favoritos-persistidos.md](./16-BLOC-CUBIT/09-ejemplo-favoritos-persistidos.md) | HydratedCubit, animación favorito |
| [10-ejemplo-multi-bloc.md](./16-BLOC-CUBIT/10-ejemplo-multi-bloc.md) | Dashboard Multi-Bloc con orquestación |
| [11-ejemplo-formulario-multipaso.md](./16-BLOC-CUBIT/11-ejemplo-formulario-multipaso.md) | Wizard de registro con stepper |
| [12-ejemplo-chat-stream.md](./16-BLOC-CUBIT/12-ejemplo-chat-stream.md) | Chat real-time con StreamSubscription |
| [13-concurrencia-eventos.md](./16-BLOC-CUBIT/13-concurrencia-eventos.md) | droppable, restartable, debounce, sequential |
| [14-testing-bloc.md](./16-BLOC-CUBIT/14-testing-bloc.md) | blocTest, seed, skip, verify, errors, wait |
| [15-hydrated-bloc.md](./16-BLOC-CUBIT/15-hydrated-bloc.md) | Persistencia automática de estado |
| [16-buenas-practicas.md](./16-BLOC-CUBIT/16-buenas-practicas.md) | BlocObserver, anti-patrones, naming, arquitectura |
| [17-proyecto-integrador.md](./16-BLOC-CUBIT/17-proyecto-integrador.md) | App e-commerce completa con 5 features |
| [18-patron-lista-avanzada.md](./16-BLOC-CUBIT/18-patron-lista-avanzada.md) | previousState, PullToRefreshWrapper, slivers, ValueKey |

**Contenido:** BLoC/Cubit completo: fundamentos, widgets flutter_bloc, 6 ejemplos con pantalla completa, concurrencia, testing con blocTest, HydratedBloc, buenas prácticas, proyecto integrador, patrón avanzado de listas.

---

## 🚀 Orden de Aprendizaje Sugerido

```
02-DISENIO-FEATURE            → Diseño de features (6-8 h) — ¡empieza aquí!
    ↓
01-CLEAN-ARCHITECTURE        → Fundamentos (4-6 h)
    ↓
05-TESTING                   → Testing (15-20 h)
    ↓
07-IA-ASSISTANT              → IA en desarrollo (2-3 h)
    ↓
08-PENCIL                    → Diseño visual con Pencil (4-6 h)
    ↓
06-NIVEL-EXPERTO             → Técnicas avanzadas (6-8 h)
    ↓
09-ESTRUCTURA-DATOS-OOP      → Estructuras de datos con OOP (10-15 h)
    ↓
15-WIDGETS-FLUTTER           → Widgets puros (6-10 h)
    ↓
16-BLOC-CUBIT                → State management (10-15 h)
    ↓
03-SUPABASE                  → Backend + automatización (10-15 h)
    ↓
12-GIT-FLOW                  → Git flow, commits (3-5 h)
    ↓
13-EDGE-FUNCTIONS            → Edge Functions + Deno (4-6 h)
    ↓
10-MAKEFILE                  → Makefile Mastery (3-5 h)
    ↓
11-GITHUB-ACTIONS            → CI/CD (4-6 h)
    ↓
04-ALMACENAMIENTO-LOCAL      → Isar (4-6 h)
    ↓
14-GOOGLE-PLAY-RELEASE       → Publicación (4-6 h)
```

---

## 📦 Dependencias Recomendadas

```yaml
dependencies:
  flutter_bloc: ^9.1.0
  bloc: ^9.0.0
  equatable: ^2.0.7
  get_it: ^8.0.0
  fpdart: ^1.2.0
  dio: ^5.4.0
  supabase_flutter: ^2.6.0
  go_router: ^14.0.0
  hydrated_bloc: ^10.0.0
  bloc_concurrency: ^0.3.0

dev_dependencies:
  bloc_test: ^10.0.0
  mocktail: ^1.0.0
  build_runner: ^2.4.9
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
