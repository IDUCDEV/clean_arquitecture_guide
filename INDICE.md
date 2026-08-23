# Índice General

Mapa de navegación cruzada entre los 23 módulos de la guía.

---

## Por concepto

| Concepto | Módulo principal | Módulos relacionados |
|---|---|---|
| Diseño de producto (MVP) | [00-DISENIO-PRODUCTO-MVP](./00-DISENIO-PRODUCTO-MVP/) | [01-CLEAN-ARCHITECTURE](./01-CLEAN-ARCHITECTURE/) (implementación), [08-PENCIL](./08-PENCIL/) (diseño visual) |
| Clean Architecture (capas) | [01-CLEAN-ARCHITECTURE](./01-CLEAN-ARCHITECTURE/) | [02-SPEC-DRIVEN-DEVELOPMENT](./02-SPEC-DRIVEN-DEVELOPMENT/) (mapeo a capas), [06-NIVEL-EXPERTO/04](./06-NIVEL-EXPERTO/04-streams-tiempo-real.md) (StreamUseCase) |
| Diseño de features (SDD) | [02-SPEC-DRIVEN-DEVELOPMENT](./02-SPEC-DRIVEN-DEVELOPMENT/) | [01-CLEAN-ARCHITECTURE/03](./01-CLEAN-ARCHITECTURE/03-estructura-de-carpetas.md) (carpetas), [22-DISENIO-SISTEMAS](./22-DISENIO-SISTEMAS/) (system design) |
| State management (BLoC/Cubit) | [16-BLOC-CUBIT](./16-BLOC-CUBIT/) | [15-WIDGETS-FLUTTER](./15-WIDGETS-FLUTTER/) (widgets puros), [06-NIVEL-EXPERTO/03](./06-NIVEL-EXPERTO/03-comunicacion-features.md) (cross-feature), [06-NIVEL-EXPERTO/04](./06-NIVEL-EXPERTO/04-streams-tiempo-real.md) (streams) |
| Widgets de Flutter | [15-WIDGETS-FLUTTER](./15-WIDGETS-FLUTTER/) | [16-BLOC-CUBIT/05-06](./16-BLOC-CUBIT/05-widgets-flutter-bloc-p1.md) (flutter_bloc widgets), [05-TESTING/04b](./05-TESTING/04-presentation/04b-practica-widgets.md) (widget tests) |
| Testing | [05-TESTING](./05-TESTING/) | [16-BLOC-CUBIT/14](./16-BLOC-CUBIT/14-testing-bloc.md) (blocTest), [06-NIVEL-EXPERTO/01](./06-NIVEL-EXPERTO/01-fpdart-result-pattern.md) (fpdart + testing) |
| Supabase (backend) | [03-SUPABASE](./03-SUPABASE/) | [03/PARTE-0](./03-SUPABASE/PARTE-0-SQL-POSTGRESQL/) (SQL/PostgreSQL), [05-TESTING/03f-h](./05-TESTING/03-data/03f-supabase-testing.md) (testing con Supabase), [13-EDGE-FUNCTIONS-DENO](./13-EDGE-FUNCTIONS-DENO/) (Edge Functions) |
| Isar (local storage) | [04-ALMACENAMIENTO-LOCAL](./04-ALMACENAMIENTO-LOCAL/) | [05-TESTING/03e](./05-TESTING/03-data/03e-practica-local-datasource-isar.md) (testing Isar) |
| Git y automatización | [12-GIT-FLOW-CONVENTIONAL-COMMITS](./12-GIT-FLOW-CONVENTIONAL-COMMITS/) | [10-MAKEFILE](./10-MAKEFILE/) (Make + Git hooks), [11-GITHUB-ACTIONS](./11-GITHUB-ACTIONS/) (CI/CD) |
| CI/CD | [11-GITHUB-ACTIONS](./11-GITHUB-ACTIONS/) | [10-MAKEFILE](./10-MAKEFILE/) (Make en CI), [14-GOOGLE-PLAY-RELEASE/05](./14-GOOGLE-PLAY-RELEASE/05-ci-cd-automatizado.md) (deploy automático) |
| Mantenimiento de dependencias | [17-MANTENIMIENTO-DEPENDENCIAS](./17-MANTENIMIENTO-DEPENDENCIAS/) | [12-GIT-FLOW](./12-GIT-FLOW-CONVENTIONAL-COMMITS/) (FVM), [10-MAKEFILE](./10-MAKEFILE/) (targets), [11-GITHUB-ACTIONS](./11-GITHUB-ACTIONS/) (CI/CD) |
| Debugging Flutter | [18-DEBUGGING-FLUTTER](./18-DEBUGGING-FLUTTER/) | [05-TESTING](./05-TESTING/) (testing), [16-BLOC-CUBIT](./16-BLOC-CUBIT/) (debug BLoC), [17-MANTENIMIENTO-DEPENDENCIAS](./17-MANTENIMIENTO-DEPENDENCIAS/) (dep debug), [18/19-24](./18-DEBUGGING-FLUTTER/19-fundamentos-rendimiento.md) (optimización) |
| Comunicacion y trabajo en equipo | [21-COMUNICACION-EQUIPO](./21-COMUNICACION-EQUIPO/) | [12-GIT-FLOW](./12-GIT-FLOW-CONVENTIONAL-COMMITS/) (Git workflow), [01-CLEAN-ARCHITECTURE](./01-CLEAN-ARCHITECTURE/) (code review de arquitectura) |
| Monitoreo en producción | [19-MONITOREO-PRODUCCION](./19-MONITOREO-PRODUCCION/) | [18-DEBUGGING-FLUTTER](./18-DEBUGGING-FLUTTER/) (debugging), [11-GITHUB-ACTIONS](./11-GITHUB-ACTIONS/) (CI/CD para uploads de symbols), [16-BLOC-CUBIT](./16-BLOC-CUBIT/) (errores en state management) |
| Edge Functions | [13-EDGE-FUNCTIONS-DENO](./13-EDGE-FUNCTIONS-DENO/) | [03-SUPABASE](./03-SUPABASE/) (backend Supabase) |
| Publicación Play Store | [14-GOOGLE-PLAY-RELEASE](./14-GOOGLE-PLAY-RELEASE/) | [11-GITHUB-ACTIONS](./11-GITHUB-ACTIONS/) (CI/CD para release) |
| IA Assistant | [07-IA-ASSISTANT](./07-IA-ASSISTANT/) | [16-BLOC-CUBIT](./16-BLOC-CUBIT/) (prompts para BLoC), [01-CLEAN-ARCHITECTURE](./01-CLEAN-ARCHITECTURE/) (prompts por capa) |
| Dart 3 / OOP | [09-ESTRUCTURA-DATOS-OOP](./09-ESTRUCTURA-DATOS-OOP/) | [16-BLOC-CUBIT/03](./16-BLOC-CUBIT/03-cubit-basico.md) (sealed + Equatable en estados), [06-NIVEL-EXPERTO/06](./06-NIVEL-EXPERTO/06-json-serializable-freezed.md) (freezed) |
| Resolución de problemas algorítmicos | [20-RESOLUCION-PROBLEMAS-ALGORITMOS](./20-RESOLUCION-PROBLEMAS-ALGORITMOS/) | [09-ESTRUCTURA-DATOS-OOP](./09-ESTRUCTURA-DATOS-OOP/) (estructuras de datos en Dart), [06-NIVEL-EXPERTO/01](./06-NIVEL-EXPERTO/01-fpdart-result-pattern.md) (pensamiento funcional) |
| Makefile | [10-MAKEFILE](./10-MAKEFILE/) | [03-SUPABASE/PARTE-3-CI_CD/01](./03-SUPABASE/PARTE-3-CI_CD/01-makefile-universal.md) (Makefile universal Supabase) |
| Pencil (diseño) | [08-PENCIL](./08-PENCIL/) | [15-WIDGETS-FLUTTER](./15-WIDGETS-FLUTTER/) (de diseño a implementación) |
| Programación funcional | [06-NIVEL-EXPERTO/01](./06-NIVEL-EXPERTO/01-fpdart-result-pattern.md) | [01-CLEAN-ARCHITECTURE/05a-b](./01-CLEAN-ARCHITECTURE/05a-domain-layer.md) (Either en UseCases), [09-ESTRUCTURA-DATOS-OOP/03](./09-ESTRUCTURA-DATOS-OOP/03-metodos-funcionales-listas.md) (map, where, fold) |
| System design | [22-DISENIO-SISTEMAS](./22-DISENIO-SISTEMAS/) | [20-RESOLUCION-PROBLEMAS-ALGORITMOS/10](./20-RESOLUCION-PROBLEMAS-ALGORITMOS/10-system-design-basico.md) (intro de 45 min), [03-SUPABASE](./03-SUPABASE/) (backend real), [19-MONITOREO-PRODUCCION](./19-MONITOREO-PRODUCCION/) (observabilidad en producción) |

---

## Por tipo de contenido

| Tipo | Dónde encontrarlo |
|---|---|
| **Teoría / Conceptos** | 01 (Clean Arch), 02 (Diseño), 09 (OOP), 10 (Make), 11 (GitHub Actions), 12 (Git flow), 15 (Widgets), 16/01-02 (BLoC), 22/00-11 (System Design) |
| **SQL / PostgreSQL** | 03/PARTE-0/01 (Fundamentos SQL), 03/PARTE-0/02 (PostgreSQL: constraints, indexes, functions, triggers, JSONB, RPC) |
| **Ejemplos con código** | 01/05a-c (CRUD), 02/05a-d (casos reales), 16/07-12,18 (BLoC), 20/05 (patrones con template Dart) |
| **Ejercicios prácticos** | 02/01a-04a (Carrito), 05/01a-06c (Testing), 09/08-10 (OOP), 10/07 (Make), 11/07 (Actions), 20/07 (10 ejercicios algorítmicos) |
| **Casos integradores** | 02/05 (Reservas), 02/05b (E-learning), 02/05c (Facturación), 02/05d (Delivery), 16/17 (E-commerce), 22/12-15 (Feed, Chat, E-commerce, SaaS) |
| **Referencia rápida** | 15/11 (arsenal de widgets), 01/08 (templates), 03/PARTE-3-CI_CD/01 (Makefile universal), 18/06 (cheatsheet debugging VSCode), 18/17 (cheatsheet DevTools) |
| **CI/CD / Automatización** | 03/PARTE-3-CI_CD, 10, 11, 14/05 |
| **Prompts para IA** | 07/01 (framework AIDR), 07/02 (caso reservas) |
| **Debugging / Diagnóstico** | 18/01-07 (VSCode debugging), 18/08-18 (DevTools), 18/25 (debugging asíncrono), 18/26 (workflow por tipo de bug) |
| **Optimización de rendimiento** | 18/19-24 (fundamentos, rebuilds, memoria, rendering, cheatsheet, practicas) |
| **Comunicacion / Soft skills** | 21/01-08 (code reviews, colaboracion, Git workflow, comunicacion tecnica, herramientas, cheatsheet, practicas, anti-patrones) |
| **Monitoreo en producción** | 19/01 (Crashlytics), 19/02 (Sentry), 19/03 (Comparación), 19/04 (Supabase Cloud consumo/costos), 19/01-07 (cheatsheet Crashlytics), 19/02-08 (cheatsheet Sentry) |

---

## Progresión por nivel

| Nivel | Módulos | Tiempo estimado |
|---|---|---|
| **Principiante** | 02 (Diseño), 01 (Clean Arch), 09 (OOP básico) | 20-30 h |
| **Intermedio** | 15 (Widgets), 16/01-09 (BLoC básico), 05 (Testing), 03 (Supabase), 18/01-07 (VSCode debugging), 20 (Resolución problemas) | 40-60 h |
| **Avanzado** | 16/10-18 (BLoC avanzado), 06 (Nivel experto), 07 (IA), 18/08-18 (DevTools avanzado), 18/19-24 (Optimización rendimiento), 22 (System Design) | 25-35 h |
| **DevOps** | 10 (Make), 11 (Actions), 12 (Git flow), 13 (Edge), 14 (Play Store), 17 (Mantenimiento) | 25-35 h |
| **Soft Skills** | 21 (Comunicacion y trabajo en equipo) | 5-8 h |

---

## Archivos clave por módulo

| Módulo | Archivo de entrada | Archivo más importante |
|---|---|---|
| 00-DISENIO-PRODUCTO-MVP | `README.md` | `09-caso-completo-mvp.md` (integrador) |
| 01-CLEAN-ARCHITECTURE | `README.md` | `05c-presentation-ui-layer.md` (CRUD completo) |
| 02-SPEC-DRIVEN-DEVELOPMENT | `README.md` | `02-sdd-flutter-supabase.md` (metodología), `ejemplos-cambios/` (casos integradores) |
| 03-SUPABASE | `README.md` | `PARTE-0-SQL-POSTGRESQL/01-fundamentos-sql/` (SQL desde cero), `PARTE-0-SQL-POSTGRESQL/02-postgresql-especifico/07-rpc-para-supabase.md` (RPC), `PARTE-1-DESARROLLO/05-migraciones-y-seeds.md` |
| 04-ALMACENAMIENTO-LOCAL | `README.md` | `03-implementacion-local-datasource.md` |
| 05-TESTING | `README.md` | `04-presentation/04a-practica-cubits-bloc-test.md` |
| 06-NIVEL-EXPERTO | `README.md` | `01-fpdart-result-pattern.md` |
| 07-IA-ASSISTANT | `README.md` | `01-guia-ia.md` |
| 08-PENCIL | `README.md` | `06c-practica-design-system.md` |
| 09-ESTRUCTURA-DATOS-OOP | `README.md` | `06-oop-modelado-datos.md` |
| 10-MAKEFILE | `README.md` | `04-analisis-makefile-real.md` |
| 11-GITHUB-ACTIONS | `README.md` | `04-workflows-analisis.md` |
| 12-GIT-FLOW | `README.md` | `05-flujo-ramas-estrategias.md` |
| 13-EDGE-FUNCTIONS | `README.md` | `04-integracion-flutter-supabase.md` |
| 14-GOOGLE-PLAY-RELEASE | `README.md` | `05-ci-cd-automatizado.md` |
| 15-WIDGETS-FLUTTER | `README.md` | `11-arsenal-completo-widgets.md` |
| 16-BLOC-CUBIT | `README.md` | `17-proyecto-integrador.md` (integrador) |
| 17-MANTENIMIENTO-DEPENDENCIAS | `README.md` | `03-automatizacion-dependabot-renovate.md` |
| 18-DEBUGGING-FLUTTER | `README.md` | `07-practicas-vscode.md` (prácticas VSCode), `18-practicas-devtools.md` (prácticas DevTools), `24-practicas-optimizacion.md` (prácticas optimización) |
| 19-MONITOREO-PRODUCCION | `README.md` | `01-firebase-crashlytics/08-practicas-crashlytics.md` (prácticas Crashlytics), `02-sentry/09-practicas-sentry.md` (prácticas Sentry), `04-supabase-consumo-costos/` (monitoreo consumo, optimización, checklist lanzamiento) |
| 20-RESOLUCION-PROBLEMAS-ALGORITMOS | `README.md` | `03-reconocimiento-patrones.md` (corazón de la guía), `05-patrones-avanzados.md` (templates Dart) |
| 21-COMUNICACION-EQUIPO | `README.md` | `01-code-reviews-efectivos.md` (code reviews), `03-git-workflow-equipe.md` (Git en equipo) |
| 22-DISENIO-SISTEMAS | `README.md` | `11-plantilla-diseno-sistema.md` (plantilla reutilizable), `12-caso-feed-red-social.md` (caso integrador) |

---

## Convenciones del proyecto

| Convención | Valor |
|---|---|
| State management | BLoC/Cubit (`flutter_bloc ^9.1.0`) |
| Backend | Supabase (`supabase_flutter ^2.6.0`) |
| Funcional | fpdart (`Either`, `Option`) |
| DI | GetIt o Injectable |
| Navegación | GoRouter |
| Local DB | Isar Community |
| Testing | blocTest + Mocktail |
| Automatización | Makefile |
| CI/CD | GitHub Actions |
| Diseño | Pencil (.pen) |
| Git | Conventional Commits + Husky |
