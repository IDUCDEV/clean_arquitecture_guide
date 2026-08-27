# 04 - Plantilla de Cambio OpenSpec

> Copia esta estructura a `openspec/changes/<kebab-case-nombre>/` en tu proyecto Flutter y completa cada archivo. Cada sección indica qué fase del flujo produce ([ver 02-sdd-flutter-supabase.md](./02-sdd-flutter-supabase.md)).
>
> Antes de cada puerta, ejecuta `openspec validate` para comprobar el formato.

---

## Estructura de la carpeta

```
openspec/changes/add-<feature>/
├── proposal.md                  ← Fases 0 + 1 (Impact Report + alcance)
├── specs/
│   └── <capacidad>/             ← una carpeta por capacidad afectada
│       └── spec.md              ← Fase 1 (requisitos EARS, formato delta)
├── design.md                    ← Fase 2 (opcional: solo complejidad Intermedia+)
└── tasks.md                     ← Fase 3
```

Convención de nombre: `add-` para features nuevas, `update-` para modificar existentes, `remove-` para retirarlas.

---

## proposal.md

```markdown
# Proposal: add-<feature>

Impacto (Impact Report)
<!-- 5-15 líneas. Obligatorio en brownfield. -->
- Features afectadas: `lib/features/...` — [cuáles y cómo]
- Reutilizable: [contratos/widgets/tablas que ya existen]
- Supabase: tablas `[...]`, RLS existente `[...]`, migración nº `<n>`
- DI / rutas: `service_locator.dart` (+<n> registros), `app_router.dart` (+1 ruta)
- Riesgos: [los 2-3 principales]

Why (Problema)
[2-4 frases: qué necesidad real existe hoy sin resolver]

What Changes (Solución)
[Qué se construye/cambia, en lenguaje del dominio]

Capabilities
### New Capabilities
- `<capacidad>`: [una frase]

### Modified Capabilities
- `<capacidad>`: [qué cambia y por qué] <!-- si aplica -->

Scope (Alcance)
**Incluye:**
- [...]
**No incluye:**
- [...] <!-- explícito: pagos, envíos, realtime... lo que NO toca -->
**Dependencias:** [...]
**Suposiciones:** [...]
**Preguntas abiertas:** [→ cerrar antes de Puerta 1]

Actores y permisos
| Actor | Puede | No puede | Mapeo RLS |
|-------|-------|----------|-----------|
| Cliente | ... | ... | auth.uid() = user_id |

Impact
- Código: [ficheros nuevos/modificados estimados]
- Datos: [tablas nuevas/columnas/migraciones]
- Breaking changes: [ninguno / cuáles]
```

---

## specs/&lt;capacidad&gt;/spec.md

```markdown
WHY
<!-- Por qué existe esta capacidad, ligado al problema del proposal -->

Purpose
[1-2 frases: qué garantiza esta capacidad]

ADDED Requirements

### Requirement: <Nombre del requisito>
<Enunciado EARS resumen: qué hará el sistema y para quién>

#### Scenario: <Camino feliz>
- **WHEN** <disparador>
- **THEN** el sistema DEBERÁ <comportamiento observable>
- **AND** <efecto secundario si aplica>

#### Scenario: <Caso borde>
- **IF** <condición límite>
- **THEN** el sistema DEBERÁ <respuesta controlada>

#### Scenario: <Error>
- **IF** <fallo esperable>
- **THEN** el sistema DEBERÁ mostrar "<mensaje exacto>" y no alterar el estado

<!-- Repetir Requirement por cada operación atómica.
     Cubrir SIEMPRE: camino feliz + bordes + errores + seguridad (RLS). -->

MODIFIED Requirements
<!-- Solo si este cambio modifica requisitos ya archivados.
     Se reescribe el requisito COMPLETO; reemplaza al anterior. -->

REMOVED Requirements
<!-- Solo si algo deja de existir. Explicar el porqué. -->
```

Reglas EARS rápidas:
- **Ubicuo**: "El sistema DEBERÁ..." — invariable
- **Evento**: "CUANDO X EL sistema DEBERÁ..." — interacción
- **Estado**: "MIENTRAS X EL sistema DEBERÁ..."
- **No deseado**: "SI X ENTONCES el sistema DEBERÁ..."
- **Opcional**: "DONDE X EL sistema DEBERÁ..."

---

## design.md (opcional — Complejidad Simple lo omite)

```markdown
# Design: add-<feature>

Context
[Estado actual relevante: patrón existente que se sigue, restricciones descubiertas]

Goals / Non-Goals
- Goals: [...]
- Non-Goals: [...]

Decisions
<!-- Una por decisión no obvia -->
### D1: <título>
- Decisión: [...]
- Alternativas descartadas: [...]
- Por qué: [...]

Ficheros afectados
| Elemento | Capa | Archivo | Req |
|----------|------|---------|-----|
| <Entity> | domain/entity | lib/features/x/domain/entities/… | REQ-00x |
| <Repository> | domain/repository | lib/features/x/domain/repositories/… | … |
| <Model> | data/model | lib/features/x/data/models/… | … |
| <DataSource> | data/datasource | lib/features/x/data/datasources/… | … |
| <UseCase> | domain/usecase | lib/features/x/domain/usecases/… | … |
| <Cubit>/<State> | presentation/cubit | lib/features/x/presentation/cubit/… | … |
| <Page> | presentation/pages | lib/features/x/presentation/pages/… | … |
| Registro DI | core/di | lib/core/di/service_locator.dart | … |
| Ruta | core/router | lib/core/router/app_router.dart | … |

Contratos Dart clave
    abstract interface class <X>Repository {
      Future<Either<Failure, T>> operacion(...);
    }
    sealed class XState {}
    class XInitial extends XState {}
    class XLoading extends XState {}
    class XLoaded extends XState { final T data; XLoaded(this.data); }
    class XError extends XState { final String message; XError(this.message); }

Flujo de datos
    Page ──► Cubit ──► UseCase ──► RepositoryImpl ──► DataSource ──► Supabase
                                        │                        │
                              Either.left(Failure) ◄────────────┘
            ◄── CartError(message) ◄── mapeo de failures

Backend Supabase
- Tablas: [columnas, tipos, FKs, constraints]
- RLS: [política por escenario de seguridad]
- RPC/Triggers: [si hay cálculo atómico o concurrencia]
- Migración: supabase/migrations/NNNN_*.sql (idempotente, no editar previas)

Boundaries aplicables a este cambio
[Qué NO debe hacer el agente aquí: ej. no tocar feature Y, no añadir paquetes]
```

---

## tasks.md

```markdown
# Tasks: add-<feature>

1. Dominio y datos base
- [ ] 1.1 Crear <Entity> con invariantes
      Rol: experto Flutter/Dart + Clean Architecture
      Éxito: invariantes cubiertas por test unitario
      Req: REQ-001 · Commit: feat(x): add Entity

- [ ] 1.2 Definir interface <X>Repository (Either<Failure,T>)
      Éxito: firmas coinciden con design.md
      Req: REQ-002..007 · Commit: feat(x): add repository contract

- [ ] 1.3 Migración SQL + políticas RLS          ← si aplica
      Éxito: openspec validate + supabase db reset OK
      Req: escenarios RS · Commit: db(x): add tables and rls

2. Capa de datos
- [ ] 2.1 <Model> fromJson/toJson (snake_case ↔ camelCase)
- [ ] 2.2 <RemoteDataSource> (llamadas exactas + errores de red)
- [ ] 2.3 UseCases (uno por operación)

3. Implementaciones y estado
- [ ] 3.1 <RepositoryImpl> (mapeo excepciones → Failure)
- [ ] 3.2 <State> sealed class
- [ ] 3.3 <Cubit> (transiciones + mensajes exactos de los escenarios)

4. Presentación e integración
- [ ] 4.1 <Page> + widgets (un render por estado)
- [ ] 4.2 Registros en service_locator.dart
- [ ] 4.3 Ruta en app_router.dart

5. Tests
- [ ] 5.1 Unit tests entidades/usecases (bordes de la spec)
- [ ] 5.2 Test repository impl (mock datasource)
- [ ] 5.3 Widget test página clave

Trazabilidad
| Req | Tarea(s) | Test | Commits |
|-----|----------|------|---------|
| REQ-001 | 1.1 | entity_test | abc123 |
```

---

## Checklist de las 3 puertas

**Puerta 1 (tras Fase 1):** historias precisas · EARS con IDs · bordes cubiertos · alcance cerrado · delta correcto.

**Puerta 2 (tras Fase 2):** ficheros afectados completos · contratos coherentes · flujo con caminos de error · RLS especificada · decisiones registradas.

**Puerta 3 (tras Fase 3):** todo requisito tiene ≥1 tarea · trazabilidad bidireccional · tareas ≤3 ficheros · orden de oleadas correcto · tests presentes.

---

## Cierre

```bash
openspec validate            # formato OK
# ... implementar (Fase 4) ...
openspec archive add-<feature>
```

Ejemplos reales completados: [`ejemplos-cambios/`](./ejemplos-cambios/)
