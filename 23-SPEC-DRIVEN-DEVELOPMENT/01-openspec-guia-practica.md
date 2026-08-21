# 01 - OpenSpec: Guía Práctica

> La herramienta líder de SDD. Specs como markdown vivo en tu repositorio, ejecutables por 30+ agentes de IA.

---

## Qué es OpenSpec

OpenSpec es un framework ligero de Spec Driven Development, open source (MIT), creado por Fission-AI. Tiene 65.7k estrellas en GitHub y es la herramienta más adoptada para implementar SDD en proyectos reales.

**Filosofía:**
- Fluid, no rígido
- Iterativo, no waterfall
- Fácil, no complejo
- Diseñado para brownfield (código existente), no solo greenfield
- Escalable de proyectos personales a empresas

**No necesita:** API keys, MCP servers, ni configuración compleja.

---

## Instalación

```bash
# Requiere Node.js 20.19.0 o superior
npm install -g @fission-ai/openspec@latest
```

**Verificar instalación:**
```bash
openspec --version
```

---

## Inicialización en un proyecto Flutter

```bash
# Navega a la raíz de tu proyecto Flutter
cd mi-proyecto-flutter

# Inicializa OpenSpec
openspec init
```

**Qué crea:**
```
mi-proyecto-flutter/
├── openspec/
│   ├── specs/                    ← Specs vivas del proyecto
│   │   └── .gitkeep
│   └── changes/                  ← Cambios en progreso
│       └── .gitkeep
├── AGENTS.md                     ← Instrucciones para agentes IA
└── .openspec/                    ← Configuración interna
```

**`openspec/init` también genera archivos de configuración para cada agente que selecciones:**
- `CLAUDE.md` (para Claude Code)
- `.cursorrules` (para Cursor)
- `.github/copilot-instructions.md` (para GitHub Copilot)
- `.windsurfrules` (para Windsurf)

---

## Workflow completo

### Paso 1: Explorar antes de decidir

```bash
# En tu agente IA (Claude Code, Cursor, etc.)
/opsx:explore
```

El agente lee tu codebase y te ayuda a pensar antes de escribir nada. Útil cuando no estás seguro de cómo implementar algo.

**Ejemplo:**
```
Tú: /opsx:explore
IA: ¿Qué quieres explorar?
Tú: Quiero agregar modo oscuro pero no estoy seguro de cómo hacerlo limpiamente
IA: [lee tu setup de estilos] La ruta más limpia: CSS variables + un ThemeContext pequeño,
    con detección de preferencia del sistema. Sin dependencias nuevas. ¿Lo acotamos?
Tú: Sí, hagámoslo
```

### Paso 2: Proponer un cambio

```bash
/opsx:propose add-dark-mode
```

OpenSpec genera una carpeta completa de cambio:

```
openspec/changes/add-dark-mode/
├── proposal.md       ← Por qué y qué cambia
├── specs/            ← Requirements y escenarios
│   └── theme/
│       └── spec.md
├── design.md         ← Decisiones técnicas
└── tasks.md          ← Checklist de implementación
```

**El agente genera esto automáticamente.** Tú solo revisas y ajustas.

### Paso 3: Revisar el plan

Antes de que el agente escriba código, revisas:
- `proposal.md` — ¿Estamos resolviendo el problema correcto?
- `specs/` — ¿Los requisitos son claros y verificables?
- `design.md` — ¿Las decisiones técnicas son coherentes con el codebase?
- `tasks.md` — ¿Las tareas están en el orden correcto?

### Paso 4: Ejecutar

```bash
/opsx:apply
```

El agente implementa las tareas una por una:

```
✓ 1.1 Add theme context provider
✓ 1.2 Create toggle component
✓ 2.1 Add CSS variables
✓ 2.2 Wire up localStorage
```

### Paso 5: Archivar

```bash
/opsx:archive
```

El cambio se archiva y las specs se actualizan. Listo para el siguiente feature.

---

## Qué son las specs en OpenSpec

Las specs son **markdown simple** con requisitos concretos y escenarios. No hay sintaxis especial que aprender.

**Ejemplo de spec:**
```markdown
## ADDED Requirements

### Requirement: Theme selection
The app SHALL let users switch between light and dark themes,
defaulting to the system preference.

#### Scenario: User toggles dark mode
- **WHEN** the user clicks the theme toggle
- **THEN** the app switches to dark mode and persists the choice

#### Scenario: System preference detection
- **GIVEN** the user has not set a theme preference
- **WHEN** the app loads
- **THEN** the theme matches the system setting
```

**Cómo se organizan:**
```
openspec/specs/
├── auth-login/
│   └── spec.md
├── auth-session/
│   └── spec.md
├── checkout-cart/
│   └── spec.md
└── checkout-payment/
    └── spec.md
```

Cada spec vive en su carpeta, al lado del código que implementa. Cuando un agente necesita contexto, lee la spec. Cuando alguien nuevo se une al equipo, browsa la biblioteca.

---

## Slash commands disponibles

| Comando | Función |
|---------|---------|
| `/opsx:explore` | Explorar opciones antes de decidir |
| `/opsx:propose <nombre>` | Crear proposal + specs + design + tasks |
| `/opsx:apply` | Ejecutar las tareas del cambio actual |
| `/opsx:archive` | Archivar cambio completado |
| `/opsx:new` | Crear un nuevo cambio (workflow expandido) |
| `/opsx:continue` | Continuar un cambio existente |
| `/opsx:verify` | Verificar que las specs se cumplen |
| `/opsx:onboard` | Onboarding de un nuevo desarrollador |

> **Nota:** El nombre del comando varía según el agente:
> - Cursor: `/opsx-propose`
> - GitHub Copilot: `@opsx-propose`
> - Amazon Q: `$openspec-propose`

---

## Ejemplo completo: Login con Supabase Auth

### Contexto
Proyecto Flutter con Clean Architecture, Supabase como backend.

### Paso 1: Explorar
```
/opsx:explore
→ Quiero agregar login con Supabase Auth
→ El agente lee tu codebase y sugiere la mejor integración
```

### Paso 2: Proponer
```
/opsx:propose add-supabase-auth
```

**Lo que genera:**

`openspec/changes/add-supabase-auth/proposal.md`:
```markdown
# Proposal: Add Supabase Authentication

## Problem
Users need to authenticate to access protected features.

## Solution
Integrate Supabase Auth with email/password login, following Clean Architecture.

## Impact
- New feature: `auth` under `lib/features/`
- Dependencies: supabase_flutter (already in pubspec)
- No breaking changes to existing features
```

`openspec/changes/add-supabase-auth/specs/auth-login/spec.md`:
```markdown
## ADDED Requirements

### Requirement: Email/password login
The system SHALL authenticate users via email and password using Supabase Auth.

#### Scenario: Successful login
- GIVEN a registered user with valid credentials
- WHEN the user submits the login form
- THEN the system returns a User entity and navigates to the home screen

#### Scenario: Invalid credentials
- GIVEN a user with wrong password
- WHEN the user submits the login form
- THEN the system displays "Credenciales inválidas" and stays on the login screen

#### Scenario: Network error
- GIVEN no internet connection
- WHEN the user submits the login form
- THEN the system displays "Error de conexión" with a retry option

### Requirement: Session persistence
The system SHALL persist the user session across app restarts.

#### Scenario: App restart with valid session
- GIVEN a user previously logged in
- WHEN the app restarts
- THEN the user is redirected to the home screen without re-authenticating
```

`openspec/changes/add-supabase-auth/design.md`:
```markdown
# Design: Supabase Auth

## Architecture
Follow Clean Architecture layers:
- Domain: User entity, AuthRepository interface, LoginUseCase
- Data: AuthDataSource (Supabase), AuthRepositoryImpl, UserModel
- Presentation: AuthCubit, AuthState, LoginPage

## Decisions
- Use Supabase GoTrue client for auth operations
- Store session via Supabase's built-in persistence
- Emit auth state changes via Stream in Cubit
```

`openspec/changes/add-supabase-auth/tasks.md`:
```markdown
# Tasks

- [ ] 1. Create User entity (domain/entities/user.dart)
- [ ] 2. Create AuthRepository interface (domain/repositories/auth_repository.dart)
- [ ] 3. Create LoginUseCase (domain/usecases/login.dart)
- [ ] 4. Create UserModel with snake_case mapping (data/models/user_model.dart)
- [ ] 5. Create AuthRemoteDataSource (data/datasources/auth_remote_datasource.dart)
- [ ] 6. Create AuthRepositoryImpl (data/repositories/auth_repository_impl.dart)
- [ ] 7. Create AuthCubit + AuthState (presentation/cubit/)
- [ ] 8. Create LoginPage with form pattern (presentation/pages/)
- [ ] 9. Register in DI (service_locator.dart)
- [ ] 10. Add route (app_router.dart)
- [ ] 11. Write unit tests for LoginUseCase
- [ ] 12. Write widget test for LoginPage
```

### Paso 3: Revisar
Revisas cada artefacto. Ajustas si algo no está bien (ej: agregar "recordar sesión" al spec).

### Paso 4: Ejecutar
```
/opsx:apply
→ El agente ejecuta las 12 tareas una por una
→ Cada tarea genera código que cumple la spec
```

### Paso 5: Archivar
```
/opsx:archive
→ Las specs de auth-login se actualizan
→ El cambio queda documentado en el historial
```

---

## Comparativa con otras herramientas

| Característica | OpenSpec | Spec Kit (GitHub) | Kiro (AWS) |
|----------------|---------|-------------------|------------|
| Tipo | CLI open source | CLI open source | IDE dedicado |
| Facilidad | Ligero, 1 comando | Más pesado, Python setup | Integrado, sin CLI |
| Flexibilidad | Fluido, sin fases rígidas | Fases rígidas | Flujo impuesto |
| Agentes | 30+ soportados | ~30 soportados | Solo Claude |
| Brownfield | Sí (diseñado para ello) | Sí | Sí |
| Specs en repo | Sí (openspec/) | Sí (.spec/) | No (en el IDE) |
| Coste | Gratis | Gratis | Requiere suscripción |

**Conclusión:** OpenSpec es la opción más flexible y ligera. Spec Kit es más estructurado pero más pesado. Kiro es potente pero te encierra en su IDE.

---

## Actualización

```bash
# Actualizar OpenSpec
npm install -g @fission-ai/openspec@latest

# Regenerar instrucciones de agentes en el proyecto
openspec update
```

---

## Configuración de telemetría

OpenSpec recopila stats anónimas (solo comandos, no contenido). Para desactivar:

```bash
# Opción 1: config global
openspec config set telemetry.enabled false

# Opción 2: variable de entorno
export OPENSPEC_TELEMETRY=0
```

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `command not found: openspec` | No está instalado globalmente | `npm install -g @fission-ai/openspec@latest` |
| `Node.js version too old` | Versión de Node menor a 20.19.0 | Actualizar Node.js |
| Slash commands no aparecen | Agentes no configurados | Ejecutar `openspec update` en el proyecto |
| Specs no se generan | No se ejecutó `/opsx:propose` primero | Ejecutar propose antes de apply |

---

## Referencias

- **Sitio web:** [openspec.dev](https://openspec.dev)
- **GitHub:** [github.com/Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec) (65.7k ⭐)
- **Discord:** [discord.gg/YctCnvvshC](https://discord.gg/YctCnvvshC)
- **Documentación:** [docs en GitHub](https://github.com/Fission-AI/OpenSpec/tree/main/docs)
