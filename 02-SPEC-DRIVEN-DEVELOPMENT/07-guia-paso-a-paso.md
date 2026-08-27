# 07 — Guía Paso a Paso: SDD con OpenSpec

> **Receta de cocina** para aplicar SDD a tu stack Flutter + Clean Architecture + Supabase usando OpenSpec. Cada fase dice exactamente qué comando ejecutar, qué archivo abrir, y qué escribir.

---

## 1. Cómo arrancar

### 1.1 Complejidad del cambio

Antes de tutto, clasifica el cambio:

| Nivel | Criterio | design.md | Puertas |
|-------|----------|-----------|---------|
| **Simple** | 1 feature, 0-1 tablas, 0 decisiones técnicas nuevas | No | 1 combinada |
| **Intermedia** | 1-2 features, 1-2 tablas, 1-2 decisiones técnicas | Sí (ligero) | 1-2 |
| **Compleja** | 3+ features, 3+ tablas, seguridad, cambios de contrato | Sí (completo) | 3 |

**Regla práctica:** si dudarías en mergearlo sin revisión de otro humano, es al menos Intermedia.

### 1.2 Artésano vs Copiloto

| Situación | Modo | Comando |
|-----------|------|---------|
| Sabes QUÉ construir, quieres pensar el diseño | **Artésano** | `/opsx-new-change` |
| No sabes bien QUÉ ni CÓMO, necesitas que la IA proponga | **Copiloto** | `/opsx-propose add-nombre` |
| Quieres explorar opciones antes de decidir | **Exploración** | `/opsx-explore` |

**Puedes mezclar:** empezar artesano y pedir a la IA que refine con `/opsx-update-change`.

---

## 2. Fase 0+1 — Crear el cambio (proposal.md + spec.md)

### Paso 1: Crear la carpeta de cambio

**Modo artésano:**
```bash
# En tu agente IA (OpenCode):
/opsx-new-change
```
OpenSpec crea el esqueleto:
```
openspec/changes/add-nombre/
├── proposal.md       ← esqueleto con secciones vacías
├── specs/
│   └── {capability}/
│       └── spec.md   ← secciones WHY/Purpose/Requirements vacías
├── design.md         ← vacío (lo llenas en Fase 2)
└── tasks.md          ← vacío (lo llenas en Fase 3)
```

**Modo copiloto:**
```bash
/opsx-propose add-nombre
```
La IA genera una primera versión de los 4 archivos. Tú solo revisas y ajustas.

### Paso 2: Llenar proposal.md

Abre `openspec/changes/add-nombre/proposal.md` y escribe:

#### Sección Impacto (Impact Report)

Ejecuta el checklist en tu codebase antes de escribir:
```bash
# Features similares
ls lib/features/

# Tablas Supabase existentes
ls supabase/migrations/

# DI y rutas
cat lib/core/di/service_locator.dart
cat lib/core/router/app_router.dart
```

Llena los 5 bullets:
```markdown
## Impacto (Impact Report)
- Features afectadas: [nombre] existente provee [X]
- Reutilizable: [patrones, widgets, contratos que ya existen]
- Supabase: [tablas nuevas/existentes, RLS, migración nº XXXX]
- DI / rutas: [service_locator.dart (+N registros), app_router.dart (+N rutas)]
- Riesgos: [concurrencia, seguridad, breaking changes]
```

#### Sección Scope (Alcance)

```markdown
## Scope (Alcance)
**Incluye:**
- [lista de lo que SÍ se construye]

**No incluye:**
- [lista de lo que explícitamente NO se construye]

**Dependencias:** [qué necesita para funcionar]
**Suposiciones:** [qué damos por hecho]
**Preguntas abiertas:** [cosas pendientes de resolver]
```

#### Sección Actores y permisos

```markdown
## Actores y permisos
| Actor | Puede | No puede | Mapeo RLS |
|-------|-------|----------|-----------|
| [nombre] | [acciones] | [restricciones] | [política RLS] |
```

**Validación:** ejecuta `openspec validate` en la CLI:
```bash
openspec validate
```
Si hay errores de formato, OpenSpec te dice cuáles corregir.

### Paso 3: Llenar spec.md

Abre `openspec/changes/add-nombre/specs/{capability}/spec.md` y escribe los requisitos EARS.

#### Cómo escribir un requisito EARS

Cada requisito tiene:
1. **ID único** (`REQ-XXX`)
2. **Nombre corto** descriptivo
3. **Cuerpo EARS** con uno de los 5 patrones
4. **Escenarios** con casos happy path + error + bordes

```markdown
## ADDED Requirements

### Requirement: [Nombre descriptivo] (REQ-001)
[Descripción en lenguaje natural del requisito]

#### Scenario: [Happy path]
- **WHEN** [disparador]
- **THEN** el sistema DEBERÁ [acción esperada]

#### Scenario: [Error/borde]
- **IF** [condición de error]
- **THEN** el sistema DEBERÁ [respuesta con mensaje exacto entre comillas]

#### Scenario: [Borde numérico]
- **IF** [valor límite alcanzado]
- **THEN** el sistema DEBERá mostrar "[mensaje con umbral exacto]"
```

**Reglas de oro para escenarios:**
- Incluye mensajes de error EXACTOS entre comillas
- Incluye umbrales numéricos concretos (50 items, 50%, 2h antes)
- Cada escenario debe ser testeable SIN preguntar nada más
- Si no puedes testearlo, reescribe el escenario

**5 patrones EARS:**

| Patrón | Cuándo usarlo | Ejemplo |
|--------|---------------|---------|
| `WHEN/THEN` | Interacciones UI, eventos | `WHEN el cliente agrega un producto THEN el sistema DEBERÁ...` |
| `IF/THEN` | Errores, validaciones, bordes | `IF el stock es 0 THEN el sistema DEBERÁ mostrar "sin stock"` |
| `MIENTRAS/THEN` | Estados持续的 | `MIENTRAS el carrito tenga items EL SISTEMA DEBERÁ...` |
| `GIVEN/WHEN/THEN` | Aislamiento, seguridad | `GIVEN un cliente autenticado WHEN consulta su carrito THEN solo recibe filas propias` |
| `DONDE/THEN` | Feature flags | `DONDE el modo oscuro está habilitado EL SISTEMA DEBERÁ...` |

### Paso 4: Iterar si es necesario

Si necesitas ajustar después de la Puerta 1:
```bash
/opsx-continue-change
```
Esto reabre el cambio para que continues editando proposal.md y spec.md.

### Paso 5: Puerta 1 — Validar requisitos

```bash
openspec validate
```

Checklist de la Puerta 1:
```
[ ] Cada historia pasa la prueba de precisión (actor + acción + objeto + propósito)
[ ] Todos los requisitos usan notación EARS con ID único (REQ-XXX)
[ ] Los bordes están cubiertos (valores límite, vacío, negativos, expirados)
[ ] Las preguntas abiertas del alcance están cerradas o documentadas
[ ] El formato delta es correcto (ADDED/MODIFIED/REMOVED según toque)
[ ] El Impact Report justifica el alcance elegido
[ ] `openspec validate` pasa sin errores
```

---

## 3. Fase 2 — Diseño técnico (design.md)

### Cuándo OMITIR design.md

Si el cambio es **Simple** (1 feature, 0-1 tablas, 0 decisiones técnicas), puedes saltar design.md. La skill `clean-arch-feature` derivará los archivos de los requisitos automáticamente.

### Qué escribir en design.md

Abre `openspec/changes/add-nombre/design.md` y llena estas secciones:

#### Context + Goals

```markdown
## Context
[1-2 oraciones: qué existe hoy y qué cambia]

## Goals / Non-Goals
- ✅ [objetivo claro]
- ❌ [anti-objetivo explícito]
```

#### Decisions (D1..Dn)

Registra solo decisiones **no obvia**. Señales de que merece registro:
- Elegir entre dos patrones válidos
- Depender de un paquete nuevo
- Tocar seguridad o datos sensibles
- Cambiar un contrato público

```markdown
## Decisions

### D1: [Título de la decisión]
- Decision: [qué se eligió]
- Alternativas descartadas: [qué se descartó y por qué]
- Por qué: [razonamiento]
```

**Ejemplos de qué SÍ es decisión:**
- Elegir entre un Cubit vs dos Cubits
- Calcular impuestos en cliente vs RPC
- Usar tabla nueva vs extender tabla existente

**Ejemplos de qué NO es decisión:**
- Usar fpdart Either (es boundary del proyecto)
- Seguir el patrón de features existentes
- Nombrar archivos en snake_case (convención)

#### Ficheros afectados

Tabla **obligatoria** — sin ella el agente improvisa rutas:

```markdown
## Ficheros afectados
| Elemento | Capa | Archivo | Req |
|----------|------|---------|-----|
| [Entity] | domain/entity | `lib/features/[name]/domain/entities/[file].dart` | REQ-001 |
| [Repository] | domain/repository | `lib/features/[name]/domain/repositories/[file].dart` | REQ-002..005 |
| [Model] | data/model | `lib/features/[name]/data/models/[file].dart` | REQ-001 |
| [DataSource] | data/datasource | `lib/features/[name]/data/datasources/[file].dart` | REQ-002 |
| [UseCase] | domain/usecase | `lib/features/[name]/domain/usecases/[file].dart` | REQ-003 |
| [Cubit/State] | presentation | `lib/features/[name]/presentation/cubit/…` | REQ-006 |
| [Page] | presentation | `lib/features/[name]/presentation/pages/[file].dart` | REQ-006 |
```

#### Contratos Dart clave

Escribe las interfaces ANTES de implementar. Copia el patrón de la feature más parecida:

```markdown
## Contratos Dart clave

```dart
// Repository interface
abstract interface class [Name]Repository {
  Future<Either<Failure, [Type]>> [method]();
}

// States UI
sealed class [Name]State {}
class [Name]Initial extends [Name]State {}
class [Name]Loading extends [Name]State {}
class [Name]Loaded extends [Name]State { final [Type] data; }
class [Name]Error extends [Name]State { final String message; }
```

#### Flujo de datos

Diagrama ASCII del recorrido completo, incluyendo errores:

```markdown
## Flujo de datos
```
[Page] ──onTap──► [Cubit].[method]()
                    │ emit [Loading]
                    ▼
             [UseCase](repository)
                    ▼
             [RepositoryImpl] ──► [DataSource].[method]()
                    │                │ supabase.from('[table]').[operation]()
                    ▼                ▼
             ◄── Either.right ◄── respuesta
             │
             └── Either.left(Failure) ──► [Error](message) ──► SnackBar
```

#### Backend Supabase

```markdown
## Backend Supabase
- **Tablas:** [nombres, columnas, tipos, FKs]
- **RLS:** [políticas por escenario, citando REQ]
- **RPCs:** [si aplica, firma y comportamiento]
- **Migración:** supabase/migrations/[XXXX].sql
```

#### Boundaries

```markdown
## Boundaries
- [regla 1]
- [regla 2]
- [regla 3]
```

### Paso: Puerta 2 — Validar diseño

```bash
openspec validate
```

Checklist de la Puerta 2:
```
[ ] La tabla de ficheros afectados cubre TODOS los requisitos de la Puerta 1
[ ] Los contratos compilan mentalmente (firmas coherentes entre capas)
[ ] El flujo de datos cubre caminos de éxito Y de error
[ ] RLS especificada para toda tabla nueva/modificada
[ ] Ninguna decisión importante quedó implícita
[ ] Se respeta el patrón de las features existentes (o se justifica el cambio)
[ ] `openspec validate` pasa sin errores
```

---

## 4. Fase 3 — Tareas (tasks.md)

### Estructura de las 5 oleadas

Abre `openspec/changes/add-nombre/tasks.md` y escribe las tareas agrupadas en oleadas:

```markdown
## 1. Dominio y datos base
- [ ] 1.1 Entity [Name] (+ invariantes, REQ-001)
- [ ] 1.2 Interface [Name]Repository (REQ-002..005)
- [ ] 1.3 Migración SQL tablas + RLS (REQ-005)

## 2. Capa de datos
- [ ] 2.1 Models (fromJson/toJson, REQ-001)
- [ ] 2.2 RemoteDataSource (REQ-002)
- [ ] 2.3 UseCases (uno por operación, REQ-003)

## 3. Implementaciones y estado
- [ ] 3.1 [Name]RepositoryImpl (REQ-002)
- [ ] 3.2 [Name]State sealed (REQ-006)
- [ ] 3.3 [Name]Cubit (REQ-006)

## 4. Presentación e integración
- [ ] 4.1 [Name]Page + widgets (REQ-006)
- [ ] 4.2 Registro en service_locator.dart
- [ ] 4.3 Ruta en app_router.dart

## 5. Tests
- [ ] 5.1 Unit tests entidades/usecases
- [ ] 5.2 Test repository impl (mock datasource)
- [ ] 5.3 Widget test página clave

## Trazabilidad
| Req | Tarea(s) | Test | Cubre escenario |
|-----|----------|------|-----------------|
| REQ-001 | 1.1, 2.1 | 5.1 | Happy path + error |
| REQ-002 | 1.2, 2.2, 3.1 | 5.2 | Happy path |
| REQ-003 | 2.3 | 5.1 | Happy path + borde |
| REQ-006 | 3.2, 3.3, 4.1 | 5.3 | Loading + error |
```

### Anotación mínima por tarea

Cada tarea debe tener:
- **Qué se hace** (1-3 ficheros)
- **REQ** que implementa
- **Criterio de éxito** (verificable)

### Puerta 3 — Validar tareas

```bash
openspec validate
```

Checklist:
```
[ ] Cada requisito de la spec tiene ≥1 tarea que lo implementa
[ ] Cada tarea referencia su requisito (trazabilidad bidireccional)
[ ] Las dependencias definen el orden de oleadas correctamente
[ ] Ninguna tarea excede ~3 ficheros
[ ] Hay tareas de test para los escenarios críticos
[ ] `openspec validate` pasa sin errores
```

---

## 5. Fase 4 — Implementar

### Vía A: Skill `clean-arch-feature` (recomendada)

Tú implementas la lógica crítica, la skill genera el andamiaje:

```bash
# En tu agente IA, llama la skill:
Usa la skill clean-arch-feature con openspec_change: openspec/changes/add-nombre/
```

La skill genera scaffold con `throw UnimplementedError()` y TODOs citando REQ-xxx.

Luego implementas body por body siguiendo tasks.md oleada por oleada.

### Vía B: Agente escribe todo (brownfield quirúrgico)

```bash
/opsx-apply-change
```

El agente lee los 4 archivos y ejecuta todas las tareas, commit por tarea.

Audita cada oleada con [06-auditoria-codigo-ia.md](./06-auditoria-codigo-ia.md).

### Verificar contra spec

Al cierre de cada oleada:

| Tarea | La spec dice | El código hace | Cumple |
|-------|--------------|----------------|--------|
| 2.1 Model | roundtrip JSON | ✔ test pasa | ✅ |
| 3.3 Cubit | estados sealed + mensajes | falta mensaje | ❌ → fix |

### Cerrar el cambio

```bash
# Verificar que cumple las specs
/opsx-verify-change

# Archivar y consolidar specs vivas
/opsx-archive-change
```

Tras archive, las specs archivadas son la documentación viva del sistema.

---

## 6. Ejemplo completo: Mini-feature "Notificaciones push"

### Fase 0+1: Crear cambio + requisitos

```bash
/opsx-propose add-push-notifications
```

La IA genera proposal/spec/design/tasks. Tú ajustas:

**proposal.md** (resumen):
- Impacto: toca `auth` (token), `core/di`, `app_router`
- Scope: SÍ recibe tokens FCM, NO envía emails
- Actores: Cliente (recibe), Admin (configura campañas)

**spec.md** (2 requisitos):
- REQ-001: Registrar token FCM al login
- REQ-002: Recibir y mostrar notificación

### Fase 2: Diseño

```markdown
## Ficheros afectados
| Elemento | Capa | Archivo | Req |
|----------|------|---------|-----|
| PushTokenService | core/services | `lib/core/services/push_token_service.dart` | REQ-001 |
| NotificationHandler | core/services | `lib/core/services/notification_handler.dart` | REQ-002 |

## Decisions
### D1: FCM vs OneSignal
- Decision: FCM directo
- Alternativas: OneSignal (dependencia externa innecesaria)
- Por qué: proyecto ya usa Firebase, sin dependencia nueva

## Backend Supabase
- **Tabla:** `push_tokens` (user_id UUID FK, token TEXT, platform TEXT, created_at)
- **RLS:** auth.uid() = user_id
```

### Fase 3: Tareas

```markdown
## 1. Dominio y datos base
- [ ] 1.1 Migración tabla push_tokens + RLS

## 2. Capa de datos
- [ ] 2.1 PushTokenService (registrar token vía Supabase)

## 3. Implementaciones
- [ ] 3.1 NotificationHandler (escuchar FCM, mostrar snackbar)

## 4. Integración
- [ ] 4.1 Registro en service_locator.dart
- [ ] 4.2 Init en main.dart

## 5. Tests
- [ ] 5.1 Test PushTokenService (mock Supabase)
- [ ] 5.2 Test NotificationHandler
```

### Fase 4: Implementar

**Vía A:** llamas la skill → genera scaffold → implementas bodies.
**Vía B:** `/opsx-apply-change` → agente escribe todo → auditas.

### Cerrar

```bash
/opsx-verify-change
/opsx-archive-change
```

---

## 7. Comandos OpenSpec — Referencia rápida

| Momento | Comando | Qué hace |
|---------|---------|----------|
| Explorar antes de decidir | `/opsx-explore` | IA lee codebase y sugiere opciones |
| Crear cambio (artesano) | `/opsx-new-change` | Crea esqueleto de 4 archivos |
| Crear cambio (copiloto) | `/opsx-propose add-nombre` | IA genera 4 archivos completos |
| Continuar cambio existente | `/opsx-continue-change` | Reabre un cambio para iterar |
| Registrar progreso | `/opsx-update-change` | Actualiza checklist de tareas |
| Ejecutar tareas (Vía B) | `/opsx-apply-change` | IA implementa todo el cambio |
| Verificar contra specs | `/opsx-verify-change` | Valida código vs requisitos |
| Archivar cambio | `/opsx-archive-change` | Consolida specs y archiva |
| Validar formato | `openspec validate` (CLI) | Comprueba schemas de archivos |
| Verificar salud instalación | `openspec doctor` (CLI) | Diagnóstico de la instalación |

---

## Referencias

- Metodología central: [02-sdd-flutter-supabase.md](./02-sdd-flutter-supabase.md)
- Referencia de comandos: [03-openspec-guia-practica.md](./03-openspec-guia-practica.md)
- Plantilla de cambio: [04-plantilla-cambio-openspec.md](./04-plantilla-cambio-openspec.md)
- Cheat sheet: [05-referencia-rapida.md](./05-referencia-rapida.md)
- Auditoría de código: [06-auditoria-codigo-ia.md](./06-auditoria-codigo-ia.md)
- Ejemplos completos: [`ejemplos-cambios/`](./ejemplos-cambios/)
