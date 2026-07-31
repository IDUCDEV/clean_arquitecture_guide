# Skills de scaffolding para Clean Architecture + Flutter + Supabase

Skills que generan **boilerplate / scaffolding** de código, dejando la implementación de la lógica al desarrollador.

## Índice

| Skill | Qué genera | Cuándo usarla |
|---|---|---|
| [flutter-test-generator](./flutter-test-generator/SKILL.md) | Tests unitarios boilerplate por capa | Cuando necesitas tests para un archivo existente |
| [clean-arch-feature](./clean-arch-feature/SKILL.md) | Feature completa (entity → page, con Supabase, páginas y wiring opcionales) | Cuando empiezas una feature nueva desde cero |
| [clean-arch-component](./clean-arch-component/SKILL.md) | Archivo individual (entity, model, usecase, cubit, page...) | Cuando añades una pieza a una feature existente |
| [di-getit-scaffold](./di-getit-scaffold/SKILL.md) | Módulo GetIt de inyección de dependencias | Cuando registras dependencias de una feature en el service locator (se invoca desde `clean-arch-feature` con `wiring: di`) |
| [go-route-scaffold](./go-route-scaffold/SKILL.md) | Configuración de rutas GoRouter | Cuando añades rutas con/sin auth redirect y Sentry (se invoca desde `clean-arch-feature` con `wiring: router`) |

---

## Cómo usar las skills

Las skills están diseñadas para ser ejecutadas por el asistente AI. Solo tienes que pedir lo que necesitas en lenguaje natural:

### Ejemplos de prompts

**"Crea un feature 'product' con campos id, name, price, categoryId, createdAt"**
→ El asistente ejecuta `clean-arch-feature` y genera todos los archivos de las 4 capas.

**"Añade un usecase delete_product al feature product"**
→ El asistente ejecuta `clean-arch-component` con `component_type: usecase` y `operation: delete`.

**"Crea un feature 'product' (campos id, name, price, categoryId, createdAt) con páginas list y detail"**
→ El asistente ejecuta `clean-arch-feature` con `pages` y genera las páginas iniciales con su patrón (`list:listener_builder`, `detail:builder`).

**"Añade una página edit al feature product con patrón form"**
→ El asistente ejecuta `clean-arch-component` con `component_type: page`, `page_name: edit` y `pattern_type: form`.

**"Crea un feature product (campos id, name, price, categoryId, createdAt) y conéctalo a Supabase, tabla products, columnas: id uuid PK, name text, price float8"**
→ El asistente ejecuta `clean-arch-feature` con parámetros Supabase y genera entidad, modelo con snake_case, datasource con `_tableName` + `watchById`, y migración SQL.

**"Crea un feature product (campos id, name, price, categoryId, createdAt) con páginas list y detail, y regístralo en DI y en el router"**
→ El asistente ejecuta `clean-arch-feature` con `pages` y `wiring: [di, router]`. Tras generar los archivos, orquesta `di-getit-scaffold` (actualiza `service_locator.dart`) y `go-route-scaffold` (añade rutas a `app_router.dart`) en el mismo turno.

**"Registra el feature product en el service locator"**
→ El asistente ejecuta `di-getit-scaffold` y añade las dependencias a `service_locator.dart`.

**"Añade las rutas de products y login al router"**
→ El asistente ejecuta `go-route-scaffold` con las rutas especificadas.

**"Genera los tests para product_cubit"**
→ El asistente ejecuta `flutter-test-generator` sobre `product_cubit.dart`.

---

## Flujo de trabajo típico

```
1. Diseñas la feature (FADER)
        ↓
2. Pides scaffold + Supabase + páginas (+ wiring: DI/rutas) → clean-arch-feature
        ↓          (si pediste wiring, orquesta di-getit-scaffold + go-route-scaffold)
3. Implementas bodies de métodos (tú)
        ↓
4. Añades más usecases o páginas → clean-arch-component
        ↓
5. Implementas bodies (tú)
        ↓
6. Pides tests → flutter-test-generator
        ↓
7. Completas los tests (tú)
        ↓
8. Verificas con flutter test
```

---

## Principios

- **Scaffolding only**: las skills generan estructura, nunca lógica de negocio
- `throw UnimplementedError()` en cada método — tú decides la implementación
- Siguen las convenciones exactas del proyecto: `fpdart`, `equatable`, `flutter_bloc`, `supabase_flutter`, `mocktail` + `bloc_test`, `go_router`, `get_it`
- Usan nombres snake_case para archivos, UpperCamelCase para clases
- Feature-first: cada feature es independiente dentro de `lib/features/`
