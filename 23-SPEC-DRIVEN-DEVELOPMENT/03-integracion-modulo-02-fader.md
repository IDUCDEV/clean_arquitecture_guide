# 03 - Integración con Módulo 02 (FADER)

> FADER ya es una implementación de SDD. Este archivo muestra cómo potenciarlo.

---

## FADER = SDD con otro nombre

Si comparas el flujo FADER del módulo 02 con las 4 fases de SDD, verás que son prácticamente idénticos:

| FADER (Módulo 02) | SDD (Guía) | Qué hacen |
|--------------------|------------|-----------|
| **1 · Alcance** | **Requisitos** | Definir qué se construye y por qué |
| **2 · FADER [E] Entidades + [D] Descomponer + [R] Reglas** | | Detallar el dominio |
| **3 · Mapeo FADER → Capas** | | Estructurar la solución |
| **4 · Contratos** | **Diseño** | Definir interfaces y firmas |
| **5 · Flujo** | | Definir secuencia de datos |
| **6 · Backend** | | Definir tablas y RPCs |
| **7 · Criterios** | **Tareas** (parcialmente) | Definir cómo se verifica |
| **8 · Estimación** | | Evaluar complejidad |
| **Skill genera scaffold** | **Implementación** | Ejecutar la spec |

**FADER ya hace SDD.** La diferencia es que FADER se enfoca en el diseño de la feature, mientras que SDD agrega:
- **Puertas de aprobación** explícitas entre fases
- **Tareas atómicas** para ejecución por agentes IA
- **Boundaries** (Always/Ask First/Never) para delegación segura
- **Clarity Gate** para verificar que la spec es completa

---

## Flujo integrado: FADER + SDD

```
┌──────────────────────────────────────────────────────────┐
│  PASO 1: FADER (Módulo 02)                               │
│  "Defino la spec completa de la feature"                  │
│                                                          │
│  Alcance → FADER → Mapeo → Contratos → Flujo → Backend   │
│  → Criterios → Estimación                                │
│                                                          │
│  Output: hoja de diseño completa                          │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PASO 2: SDD — Puerta 1 (Requisitos → Diseño)           │
│  "¿La spec captura todo lo que necesito?"                 │
│                                                          │
│  ✓ Requisitos completos?                                 │
│  ✓ Criterios verificables?                               │
│  ✓ Reglas de negocio explícitas?                         │
│  ✓ Edge cases considerados?                              │
│                                                          │
│  Si NO → ajusto la hoja FADER                            │
│  Si SÍ → avanzo                                          │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PASO 3: SDD — Descomponer en tareas atómicas            │
│  "Del diseño del FADER extraigo unidades ejecutables"     │
│                                                          │
│  Cada usecase = 1 tarea                                  │
│  Cada entity/model = 1 tarea                             │
│  Cada datasource = 1 tarea                               │
│  Cada cubit = 1 tarea                                    │
│  Cada página = 1 tarea                                   │
│  Cada migración SQL = 1 tarea                            │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PASO 4: SDD — Puerta 2 (Diseño → Tareas)               │
│  "¿El diseño es viable y las tareas son correctas?"       │
│                                                          │
│  ✓ Patrones del codebase respetados?                     │
│  ✓ Dependencias correctas?                               │
│  ✓ Orden de tareas lógico?                               │
│  ✓ Cada tarea es independiente verificable?              │
│                                                          │
│  Si NO → reordeno o ajusto                               │
│  Si SÍ → ejecuto                                         │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PASO 5: Ejecución                                       │
│  "Opción A: skill clean-arch-feature                     │
│   Opción B: agente IA con OpenSpec"                      │
│                                                          │
│  Opción A: Skill genera scaffold → UnimplementedError    │
│            → yo implemento cada método                   │
│                                                          │
│  Opción B: /opsx:propose → /opsx:apply                   │
│            → agente ejecuta cada tarea atómica           │
│            → yo verifico en cada commit                  │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PASO 6: SDD — Puerta 3 (Tareas → Implementación)       │
│  "¿Cada tarea cumple su spec?"                           │
│                                                          │
│  ✓ Entity tiene los campos correctos?                    │
│  ✓ Repository retorna Either<Failure, T>?                │
│  ✓ Cubit emite los estados esperados?                    │
│  ✓ Page muestra los componentes correctos?               │
│  ✓ Migración SQL crea la tabla con las columnas?         │
│                                                          │
│  Si NO → regenero la tarea defectuosa                    │
│  Si SÍ → avanzo a la siguiente tarea                     │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PASO 7: SDD — Clarity Gate                              │
│  "¿Otro agente podría regenerar esto solo con la spec?"  │
│                                                          │
│  Test: doy la spec a otro agente (o nueva sesión)        │
│  sin contexto adicional. ¿Genera código equivalente?     │
│                                                          │
│  Si SÍ → spec clara y completa                           │
│  Si NO → faltan supuestos implícitos → actualizo la spec │
└──────────────────────────────────────────────────────────┘
```

---

## Ejemplo completo: Login con Supabase Auth

### Paso 1: FADER (Módulo 02)

Usando la [`PLANTILLA-DISENIO-FEATURE.md`](../02-DISENIO-FEATURE/PLANTILLA-DISENIO-FEATURE.md):

```markdown
# 1 · Alcance
Feature: auth-login
Descripción: Login con email y contraseña usando Supabase Auth
Actor principal: Usuario no autenticado

# 2 · FADER
[E] Entidades:
- User: id, email, name, avatarUrl

[D] Descomponer:
- D1: Recibir credenciales (email, password)
- D2: Validar formato de email
- D3: Enviar credenciales a Supabase Auth
- D4: Parsear respuesta en User entity
- D5: Persistir sesión
- D6: Navegar al home

[R] Reglas:
- R001: Email debe ser válido (contiene @ y dominio)
- R002: Contraseña mínima 8 caracteres
- R003: Sesión se persiste automáticamente por Supabase
- R004: Si la sesión ya existe, redirigir al home

# 3 · Mapeo
| Elemento FADER | Capa | Archivo |
|----------------|------|---------|
| Entidad User | domain/entities | user.dart |
| Contrato de Repo | domain/repositories | auth_repository.dart |
| Modelo User | data/models | user_model.dart |
| DataSource | data/datasources | auth_remote_datasource.dart |
| Implementación | data/repositories | auth_repository_impl.dart |
| UseCase Login | domain/usecases | login.dart |
| Estados UI | presentation/cubit | auth_cubit.dart + auth_state.dart |
| Página Login | presentation/pages | auth_login_page.dart |

# 4 · Contratos
Repository: login(email: String, password: String) → Future<Either<Failure, User>>
DataSource: signIn(email: String, password: String) → Future<UserModel>
UseCase: call(LoginParams) → Future<Either<Failure, User>>

# 5 · Flujo
User → LoginPage → AuthCubit.login() → LoginUseCase → AuthRepository → AuthDataSource → Supabase Auth

# 6 · Backend
Tabla: users (id uuid PK, email text, name text, avatar_url text, created_at timestamptz)

# 7 · Criterios
- [BDD] GIVEN credenciales válidas WHEN login THEN usuario autenticado y navegación a home
- [BDD] GIVEN credenciales inválidas WHEN login THEN error "Credenciales inválidas"
- [BDD] GIVEN sesión existente WHEN app inicia THEN redirección a home

# 8 · Estimación
Complejidad: Media (6 archivos, 1 tabla, 3 escenarios)
```

### Paso 2: Puerta 1 — ¿La spec es completa?

Checklist:
- [x] Requisitos claros (login con email/password)
- [x] Entidad definida (User con 4 campos)
- [x] Reglas explícitas (R001-R004)
- [x] Contratos firmados (login, signIn, call)
- [x] Flujo de datos trazado
- [x] Tabla definida
- [x] Criterios BDD verificables

**Resultado:** La spec está completa. Avanzo.

### Paso 3: Descomponer en tareas atómicas

Del FADER extraigo:

```
Tarea 1: Crear User entity (domain/entities/user.dart)
  - Rol: implementador
  - Tarea: crear clase User con id, email, name, avatarUrl
  - Restricciones: usar Equatable, incluir copyWith y toString
  - Criterios de éxito: pasa flutter analyze, tiene tests de igualdad

Tarea 2: Crear AuthRepository interface (domain/repositories/auth_repository.dart)
  - Rol: implementador
  - Tarea: definir interfaz con método login
  - Restricciones: retornar Future<Either<Failure, User>>
  - Criterios de éxito: compila sin errores

Tarea 3: Crear UserModel (data/models/user_model.dart)
  - Rol: implementador
  - Tarea: crear UserModel con mapeo snake_case
  - Restricciones: fromJson usa user_id → userId, created_at → createdAt
  - Criterios de éxito: pasa flutter analyze, fromJson y toJson correctos

Tarea 4: Crear AuthRemoteDataSource (data/datasources/auth_remote_datasource.dart)
  - Rol: implementador
  - Tarea: crear datasource con signIn usando Supabase
  - Restricciones: usar _supabase.auth.signInWithPassword(), lanzar ServerException en error
  - Criterios de éxito: compila, maneja AuthException

Tarea 5: Crear AuthRepositoryImpl (data/repositories/auth_repository_impl.dart)
  - Rol: implementador
  - Tarea: implementar Repository pattern con try/catch
  - Restricciones: retornar Right(User) o Left(Failure)
  - Criterios de éxito: cubre los 3 escenarios del criterio BDD

Tarea 6: Crear LoginUseCase (domain/usecases/login.dart)
  - Rol: implementador
  - Tarea: crear UseCase con params email y password
  - Restricciones: validar R001 (email) y R002 (password) antes de llamar repo
  - Criterios de éxito: valida inputs, delega al repository

Tarea 7: Crear AuthCubit + AuthState (presentation/cubit/)
  - Rol: implementador
  - Tarea: crear cubit con estados Initial, Loading, Success, Error
  - Restricciones: usar sealed class para states, Equatable
  - Criterios de éxito: emite estados en orden correcto

Tarea 8: Crear LoginPage (presentation/pages/auth_login_page.dart)
  - Rol: implementador
  - Tarea: crear formulario con patrón form
  - Restricciones: usar BlocListener + BlocBuilder, validación de campos
  - Criterios de éxito: muestra errores de validación, muestra loading, muestra feedback
```

### Paso 4: Puerta 2 — ¿Las tareas son correctas?

Checklist:
- [x] Cada tarea afecta 1-3 archivos máximo
- [x] Dependencias respetadas (entity antes de model, model antes de datasource)
- [x] Oleadas posibles: Tareas 1-2 en paralelo, luego 3-4, luego 5-6, luego 7-8
- [x] Cada tarea es verificable de forma aislada

**Resultado:** Las tareas son correctas. Ejecuto.

### Paso 5: Ejecución

**Opción A — Skill clean-arch-feature:**
```bash
# El skill genera el scaffold con UnimplementedError()
# Tú implementas cada método
```

**Opción B — OpenSpec + agente IA:**
```bash
/opsx:propose add-supabase-auth
/opsx:apply
# El agente ejecuta las 8 tareas
# Tú verificas en cada commit
```

### Paso 6: Puerta 3 — ¿Cada tarea cumple su spec?

Para cada tarea completada, verifico contra la spec:

| Tarea | Spec dice | Código hace | ¿Cumple? |
|-------|-----------|-------------|----------|
| 1. User entity | id, email, name, avatarUrl con Equatable | User class con Equatable, copyWith, toString | ✓ |
| 2. AuthRepository | login() → Either<Failure, User> | abstract class con método login | ✓ |
| 3. UserModel | Mapeo snake_case (user_id → userId) | fromJson usa user_id, toJson usa user_id | ✓ |
| 4. DataSource | signIn() con Supabase, ServerException en error | signInWithPassword + catch AuthException | ✓ |
| 5. RepositoryImpl | try/catch retornando Right/Left | implementado con Either | ✓ |
| 6. LoginUseCase | Validar R001, R002 antes de repo | Valida email y password | ✓ |
| 7. AuthCubit | Estados Initial→Loading→Success/Error | sealed class con los 4 estados | ✓ |
| 8. LoginPage | Form con validación, loading, feedback | BlocListener + BlocBuilder + Form | ✓ |

### Paso 7: Clarity Gate

**Test:** Doy la spec del archivo 02 (`02-sdd-en-flutter.md`) a una nueva sesión de Claude Code, sin contexto del proyecto.

**Resultado esperado:** El agente debería poder regenerar la misma estructura de archivos con comportamiento equivalente.

**Si no puede:** la spec tiene supuestos implícitos que no quedaron capturados. Los documento y actualizo la spec.

---

## Cuándo usar cada herramienta

| Situación | Herramienta | Por qué |
|-----------|-------------|---------|
| Feature nueva, compleja | FADER + OpenSpec | FADER diseña, OpenSpec ejecuta con agente |
| Feature nueva, simple | FADER + skill clean-arch-feature | FADER diseña, skill genera scaffold, tú implementas |
| Bug fix | Vibe coding | No necesita spec (proporcionalidad) |
| Refactor grande | SDD sin FADER | Solo necesitas tareas atómicas, no diseño completo |
| Cambio en feature existente | Impact Report + SDD | Primero analizas qué afecta, luego especificas |

---

## Referencia

- **Módulo 02 (FADER):** [`02-DISENIO-FEATURE/`](../02-DISENIO-FEATURE/)
- **Plantilla FADER:** [`02-DISENIO-FEATURE/PLANTILLA-DISENIO-FEATURE.md`](../02-DISENIO-FEATURE/PLANTILLA-DISENIO-FEATURE.md)
- **Guía SDD:** `Guia-SDD-equipos-agiles.pdf` (raíz del proyecto)
- **OpenSpec:** `01-openspec-guia-practica.md` (este módulo)
- **SDD en Flutter:** `02-sdd-en-flutter.md` (este módulo)
