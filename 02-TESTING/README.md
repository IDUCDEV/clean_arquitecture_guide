# 02 - Testing

> Aprende a probar cada capa de tu aplicación Flutter. Desde tests unitarios hasta tests de integración con Supabase.

---

## 📋 Índice

| Archivo | Descripción |
|---------|-------------|
| [01-fundamentos.md](./01-fundamentos.md) | Teoría: Conceptos, AAA, setup |
| [01a-practica-primeros-tests.md](./01a-practica-primeros-tests.md) | Práctica: Primeros tests |
| [02-domain-testing.md](./02-domain-testing.md) | Teoría: Entities, UseCases, Fakes |
| [02b-mocktail-guia-completa.md](./02b-mocktail-guia-completa.md) | Guía completa de Mocktail (stubbing, verify, práctica, migración) |
| [03-data-testing.md](./03-data-testing.md) | Teoría: Models, DataSources, Repos |
| [03a-practica-fixtures-models.md](./03a-practica-fixtures-models.md) | Práctica: Fixtures JSON |
| [03b-practica-datasources.md](./03b-practica-datasources.md) | Práctica: Remote/Local DataSources |
| [03c-practica-repositories.md](./03c-practica-repositories.md) | Práctica: Repository Implementation |
| [03d-practica-notificaciones-email.md](./03d-practica-notificaciones-email.md) | Práctica: Notificaciones y Email |
| [04-presentation-testing.md](./04-presentation-testing.md) | Teoría: Cubits, Widgets |
| [04a-practica-cubits-bloc-test.md](./04a-practica-cubits-bloc-test.md) | Práctica: Tests con bloc_test |
| [04b-practica-widgets.md](./04b-practica-widgets.md) | Práctica: Widget tests |
| [05-core-testing.md](./05-core-testing.md) | Teoría: NetworkInfo, Services |
| [05a-practica-core-services.md](./05a-practica-core-services.md) | Práctica: Services |
| [06-advanced-testing.md](./06-advanced-testing.md) | Teoría: Coverage, CI/CD, Integration tests |
| [06a-practica-coverage-ci.md](./06a-practica-coverage-ci.md) | Práctica: GitHub Actions |
| [06b-intro-integration-tests.md](./06b-intro-integration-tests.md) | Teoría: Tests de Integración, patrol, performance profiling, Firebase Test Lab, migración desde flutter_driver |
| [06c-practica-flujos-completos.md](./06c-practica-flujos-completos.md) | Práctica: Flujos completos con Supabase |
| [07-supabase-testing.md](./07-supabase-testing.md) | Teoría: Testing de Remote DataSources con Supabase (cadena de builders, Fakes, estrategias) |
| [07a-practica-supabase-datasources.md](./07a-practica-supabase-datasources.md) | Práctica: DataSources con Supabase usando Mocktail + Fakes (Auth, DB, Storage) |
| [07b-practica-supabase-mock-http-client.md](./07b-practica-supabase-mock-http-client.md) | Bonus: mock_supabase_http_client - paquete oficial de Supabase community |
| [07c-practica-local-datasource-isar.md](./07c-practica-local-datasource-isar.md) | Práctica: Local DataSources con Isar Community (bridge a [06-ALMACENAMIENTO-LOCAL](../06-ALMACENAMIENTO-LOCAL/)) |

---

## 🎯 Contenido

### PARTE 1: FUNDAMENTOS
- Conceptos básicos de testing
- Arrange-Act-Assert
- Configuración del entorno

### PARTE 2: DOMAIN
- Testing de Entities
- Testing de UseCases
- Fakes manuales vs Mocks (Mocktail)

### PARTE 3: DATA
- Testing de Models
- Testing de DataSources
- Testing de Repositories
- Testing de Notificaciones y Email

### PARTE 4: PRESENTATION
- Testing de Cubits/BLoCs
- Widget tests

### PARTE 5: CORE
- Testing de Services
- NetworkInfo

### PARTE 6: AVANZADO
- Coverage
- CI/CD con GitHub Actions
- Tests de Integración con Supabase
- Performance profiling con traceAction y TimelineSummary
- Firebase Test Lab (Android e iOS)
- Setup por plataforma (desktop, Android, iOS, web)
- Migración desde flutter_driver a integration_test

### PARTE 7: SUPABASE TESTING (NUEVO)
- **Teoría:** Por qué testear Supabase es distinto, la cadena de builders, el patrón Fake para PostgrestTransformBuilder, jerarquía de mocks, `registerFallbackValue`, manejo de errores
- **Práctica:** Ejercicios paso a paso con Mocktail + Fakes para Auth, Database (SELECT, INSERT, UPDATE, DELETE), Storage, y ejemplos completos (Profile, PaymentMethod)
- **Bonus:** `mock_supabase_http_client` - paquete oficial de Supabase community para tests de integración ligeros

### PARTE 8: MIGRACIÓN (contenido fusionado en [02b-mocktail-guia-completa.md](./02b-mocktail-guia-completa.md))
- De Fakes a Mocks con Mocktail

### PARTE 9: ALMACENAMIENTO LOCAL CON ISAR
- **Teoría:** Introducción a Isar, setup, code generation — ver [01-isar-introduccion.md](../06-ALMACENAMIENTO-LOCAL/01-isar-introduccion.md)
- **Modelos y operaciones:** Colecciones, anotaciones, CRUD, queries, filtros, patrón TTL — ver [02-modelos-operaciones.md](../06-ALMACENAMIENTO-LOCAL/02-modelos-operaciones.md)
- **Implementación:** IsarService singleton, LocalDataSource pattern, CacheManager, UserSessionImpl — ver [03-implementacion-local-datasource.md](../06-ALMACENAMIENTO-LOCAL/03-implementacion-local-datasource.md)
- **Práctica:** Testing de Local DataSources con Isar real (Auth, Profile, PaymentMethod, CacheManager, UserSessionImpl) — [07c-practica-local-datasource-isar.md](./07c-practica-local-datasource-isar.md) → [04-testing-local-datasource.md](../06-ALMACENAMIENTO-LOCAL/04-testing-local-datasource.md)

---

## 🚀 Siguiente paso

Continue with [03-IA-ASSISTANT](../03-IA-ASSISTANT/) to learn how to use AI in your development workflow, or dive into [06-ALMACENAMIENTO-LOCAL](../06-ALMACENAMIENTO-LOCAL/) for Local Storage with Isar.

---

**Nivel:** Intermedio  
**Tiempo estimado:** 22-28 horas