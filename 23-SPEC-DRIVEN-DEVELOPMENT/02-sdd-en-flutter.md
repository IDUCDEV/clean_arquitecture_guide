# 02 - SDD en Flutter + Supabase

> Cómo aplicar Spec Driven Development a un proyecto Flutter con Clean Architecture y Supabase.

---

## Contexto

La guía SDD (`Guia-SDD-equipos-agiles.pdf`) es genérica: aplica a cualquier lenguaje y plataforma. Este archivo **la contextualiza** a tu stack:

- **Flutter** como framework UI
- **Supabase** como backend (Auth, Database, Storage, Edge Functions)
- **Clean Architecture** como estructura (domain / data / presentation)
- **Cubit** como state management
- **Equatable** para comparación de entidades
- **fpdart** para functional error handling (Either<Failure, T>)

---

## La spec como contrato en Flutter

En Flutter, la spec define **qué componente se construye** y **cómo se comporta** antes de que se escriba una línea de Dart.

### Niveles de spec en Clean Architecture

| Capa | Qué especifica la spec | Ejemplo |
|------|----------------------|---------|
| **Entity** | Estructura del dato de dominio | User con id, email, name, avatarUrl |
| **Repository interface** | Contrato de acceso a datos | login(email, password) → Either<Failure, User> |
| **UseCase** | Regla de negocio | LoginUseCase ejecuta repository.login() |
| **DataSource** | Cómo se obtienen los datos | Llamada a Supabase Auth |
| **Cubit** | Estados de la UI | LoginInitial → LoginLoading → LoginSuccess/Error |
| **Page** | Comportamiento visual | Formulario con validación, submit, feedback |

---

## Specs por componente

### Spec de Entity

```markdown
### Requirement: User entity
The system SHALL represent authenticated users with the following attributes:
- id: String (UUID from Supabase)
- email: String
- name: String
- avatarUrl: String?

#### Scenario: Create from Supabase auth response
- GIVEN a GoTrue user with id, email, and user_metadata
- WHEN the user data is parsed
- THEN a User entity is created with all fields populated
- AND avatarUrl is null if not provided in metadata

#### Scenario: Equality
- GIVEN two User entities with the same id
- WHEN compared using ==
- THEN they are equal (Equatable)
```

### Spec de Repository Interface

```markdown
### Requirement: Auth repository
The system SHALL provide an AuthRepository with login capability.

#### Scenario: Successful login
- GIVEN a registered user with email "test@example.com" and password "secure123"
- WHEN AuthRepository.login() is called with those credentials
- THEN return Right(User) with the authenticated user data

#### Scenario: Invalid credentials
- GIVEN wrong password "wrongpass"
- WHEN AuthRepository.login() is called
- THEN return Left(AuthFailure) with message "Credenciales inválidas"

#### Scenario: Network error
- GIVEN no internet connection
- WHEN AuthRepository.login() is called
- THEN return Left(NetworkFailure) with message "Error de conexión"
```

### Spec de UseCase

```markdown
### Requirement: Login use case
The LoginUseCase SHALL orchestrate the login flow and return Either<Failure, User>.

#### Scenario: Login success
- GIVEN valid credentials
- WHEN LoginUseCase is called with LoginParams(email, password)
- THEN call repository.login()
- AND return the same result

#### Scenario: Input validation
- GIVEN an empty email
- WHEN LoginUseCase is called
- THEN return Left(ValidationFailure) without calling repository
```

### Spec de DataSource

```markdown
### Requirement: Auth remote data source
The AuthRemoteDataSource SHALL interact with Supabase GoTrue client.

#### Scenario: Sign in with email
- GIVEN Supabase client initialized
- WHEN signIn(email: "test@example.com", password: "secure123")
- THEN call _supabase.auth.signInWithPassword()
- AND return UserModel parsed from the response

#### Scenario: Supabase throws AuthException
- GIVEN invalid credentials
- WHEN signIn() is called
- THEN catch AuthException
- AND throw ServerException with the error message
```

### Spec de Cubit

```markdown
### Requirement: Auth cubit
The AuthCubit SHALL manage authentication states.

#### State transitions:
- AuthInitial → AuthLoading → AuthSuccess(user)
- AuthInitial → AuthLoading → AuthError(message)

#### Scenario: Login flow
- GIVEN AuthCubit in AuthInitial state
- WHEN login(email, password) is called
- THEN emit AuthLoading
- AND call LoginUseCase
- AND emit AuthSuccess(user) on success
- AND emit AuthError(message) on failure

#### Scenario: Reset after error
- GIVEN AuthCubit in AuthError state
- WHEN resetError() is called
- THEN emit AuthInitial
```

### Spec de Page

```markdown
### Requirement: Login page
The LoginPage SHALL display a form with email and password fields.

#### Scenario: Form submission
- GIVEN valid email and password entered
- WHEN user taps "Iniciar sesión" button
- THEN call AuthCubit.login()
- AND show CircularProgressIndicator while loading

#### Scenario: Validation error
- GIVEN empty email field
- WHEN user taps "Iniciar sesión"
- THEN show "El email es requerido" below the field
- AND do not call AuthCubit

#### Scenario: Auth error feedback
- GIVEN AuthCubit emits AuthError("Credenciales inválidas")
- WHEN the state changes
- THEN show SnackbarHelper with error message
- AND stay on login page
```

---

## Boundaries adaptados a Flutter

### Always (el agente ejecuta sin preguntar)

```markdown
## Always
- Run `flutter analyze` before every commit
- Run `dart format .` on modified files
- Follow naming conventions: snake_case files, CamelCase classes
- Use Equatable for entities and state classes
- Use fpdart Either<Failure, T> for repository methods
- Include `const` constructors where possible
- Use `sealed class` for Cubit states (Dart 3+)
- Add `@override` annotations
- Use `part` / `part of` for Cubit + State files
- Register new features in service_locator.dart
```

### Ask First (requiere aprobación)

```markdown
## Ask First
- Add new dependencies to pubspec.yaml
- Modify existing database migrations
- Change the project folder structure
- Update CI/CD configuration
- Modify shared widgets in core/
- Change RLS policies in Supabase
- Add new Supabase Edge Functions
- Modify the routing configuration (app_router.dart)
- Add new environment variables to .env
```

### Never (líneas rojas)

```markdown
## Never
- Commit .env files or API keys
- Modify build.gradle or Podfile without approval
- Delete existing database migrations
- Change Supabase project settings
- Remove or modify existing tests
- Commit generated files (build/, .dart_tool/)
- Modify production RLS policies directly
- Use `dynamic` type to bypass type checking
```

---

## Notación EARS para criterios de aceptación de Flutter

| Patrón | Ejemplo en Flutter |
|--------|-------------------|
| **Ubicuo** | "La app SHALL mostrar el nombre del usuario en el AppBar de todas las páginas autenticadas" |
| **Evento** | "Cuando el usuario pulsa el botón de logout, el sistema SHALL cerrar la sesión y navegar al login" |
| **Estado** | "Mientras el formulario sea inválido, el botón de submit SHALL estar deshabilitado" |
| **No deseado** | "Si la sesión expira durante una petición, el sistema SHALL redirigir al login y mostrar 'Sesión expirada'" |
| **Opcional** | "Donde el usuario haya habilitado biometría, el sistema SHALL ofrecer login por huella dactilar" |

---

## Mapeo Postgres → Dart (referencia rápida)

| Postgres | Dart | Ejemplo |
|----------|------|---------|
| `uuid` | `String` | `id: String` |
| `text` / `varchar` | `String` | `email: String` |
| `int4` / `int8` | `int` | `quantity: int` |
| `float4` / `float8` / `numeric` | `double` | `price: double` |
| `bool` | `bool` | `isActive: bool` |
| `timestamptz` | `DateTime` | `createdAt: DateTime` |
| `jsonb` | `Map<String, dynamic>` | `metadata: Map<String, dynamic>` |
| `text[]` | `List<String>` | `tags: List<String>` |

**Snake_case → camelCase:** `created_at` → `createdAt`, `user_id` → `userId`

---

## Plantilla de spec para cualquier componente Flutter

```markdown
### Requirement: [Nombre] [Componente]
The [Sistema/Capa] SHALL [comportamiento].

#### Scenario: [Nombre del escenario]
- GIVEN [precondición]
- WHEN [acción]
- THEN [resultado esperado]

#### Scenario: [Escenario de error]
- GIVEN [condición de error]
- WHEN [acción]
- THEN [resultado de error]
```

**Reglas para specs de Flutter:**
1. **Un scenario por caso de uso** (éxito, error, edge case)
2. **Verificable**: debe poder determinarse si se cumple viendo el resultado
3. **Sin ambigüedad**: "el botón SHALL estar deshabilitado" no "el botón será intuitivo"
4. **Por componente**: una spec por entity, una por usecase, una por cubit, una por page

---

## Errores comunes al aplicar SDD en Flutter

| Error | Ejemplo | Solución |
|-------|---------|----------|
| Specs demasiado vagos | "La UI debe ser bonita" | "El login SHALL usar colores del tema primario con padding de 16px" |
| Specs que mezclan capas | "El cubit llama a Supabase directamente" | Separar: spec de cubit (emite estados) ≠ spec de datasource (llama a Supabase) |
| Olvidar specs de error | Solo especificar el caso de éxito | Siempre incluir scenario de error y scenario de edge case |
| Specs demasiado largos | 50 requisitos en un solo archivo | Dividir: una spec por componente de Clean Architecture |
| No actualizar specs | El código cambió pero la spec no | Actualizar la spec en el mismo commit que el cambio |

---

## Referencia

- **Guía SDD completa:** `Guia-SDD-equipos-agiles.pdf` (raíz del proyecto)
- **OpenSpec:** `01-openspec-guia-practica.md` (este módulo)
- **Integración con FADER:** `03-integracion-modulo-02-fader.md` (este módulo)
