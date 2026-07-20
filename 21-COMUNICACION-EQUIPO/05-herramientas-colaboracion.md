# 05: Herramientas de Colaboracion

## Herramientas del Ecosistema de Desarrollo

Un developer moderno no solo escribe codigo — tambien navega entre multiples herramientas
para colaborar, comunicar, y organizar el trabajo. Aqui tienes las herramientas esenciales
y como usarlas efectivamente.

### Mapa de herramientas

```
┌─────────────────────────────────────────────────────────────────┐
│                HERRAMIENTAS DE COLABORACION                     │
│                                                                 │
│  CODIGO         GESTION        COMUNICACION     DOCUMENTACION   │
│  ──────         ──────         ────────────     ─────────────   │
│  GitHub         Linear         Slack/Discord    Notion          │
│  GitLab         Jira           Loom            Confluence      │
│  VS Code        GitHub Issues  Zoom            GitHub Wiki     │
│  Tuple          FigJam         Daily Bot       Google Docs     │
│  Live Share     Miro           Status Page     README.md       │
└─────────────────────────────────────────────────────────────────┘
```

## GitHub: Mas que un repositorio

### Features para colaboracion

| Feature | Para que sirve | Como usarlo |
|---------|---------------|-------------|
| **Issues** | Bug reports, features, tareas | Crear issues con templates |
| **Projects (v2)** | Kanban board, sprint planning | Organizar issues en columnas |
| **Discussions** | Q&A, ideas, decisiones abiertas | Para temas no urgentes |
| **Wiki** | Documentacion del proyecto | Guia completa del proyecto |
| **Milestones** | Agrupar issues por release/fase | Tracking de progreso |
| **Labels** | Categorizar issues y PRs | `bug`, `feature`, `P0`, `P1` |

### Configurar Projects v2

```
┌─────────────────────────────────────────────────────────────────┐
│  GITHUB PROJECTS V2: TABLERO TIPICO                             │
│                                                                 │
│  │ Backlog    │ Todo    │ In Progress │ Review  │ Done    │    │
│  │            │         │             │         │         │    │
│  │ Issue #45  │ Issue#31│ Issue #28   │ Issue#27│ Issue#22│    │
│  │ Issue #46  │ Issue#32│ Issue #29   │ Issue#26│ Issue#23│    │
│  │ Issue #47  │ Issue#33│             │         │ Issue#24│    │
│  │            │         │             │         │         │    │
│  │ Priority:  │ Sprint: │ Assignee:   │ Needs:  │ Merged:│    │
│  │ P2         │ Sprint 5│ @dev-name   │ Review  │ PR#123 │    │
└─────────────────────────────────────────────────────────────────┘
```

### GitHub Issues: template recomendado

```markdown
## Bug Report

### Descripcion
[Que esta pasando]

### Pasos para reproducir
1. Ir a '...'
2. Hacer click en '...'
3. Scroll hasta '...'
4. Ver error

### Comportamiento esperado
[Que deberia pasar]

### Screenshots
[Si aplica]

### Entorno
- Device: [ej. iPhone 14, Pixel 7]
- OS: [ej. iOS 17.2, Android 14]
- App Version: [ej. 1.2.3]
- Flutter Version: [ej. 3.16.0]
```

## Linear/Jira para Developers

### Que necesitas saber de un issue tracker

| Campo | Que es | Ejemplo |
|-------|--------|---------|
| **Title** | Nombre corto del issue | "Login con Google falla en iOS" |
| **Description** | Detalle del problema | Steps to reproduce, expected behavior |
| **Priority** | Urgencia | Urgent, High, Medium, Low |
| **Status** | Donde esta el issue | Todo, In Progress, Done |
| **Assignee** | Quien lo hace | @developer-name |
| **Labels** | Categorias | bug, feature, P0 |
| **Sprint** | Iteracion | Sprint 5 (Ene 15-29) |
| **Estimate** | Cuanto toma | 3 story points |

### Flujo de un issue

```
┌─────────────────────────────────────────────────────────────────┐
│                FLUJO DE UN ISSUE                                │
│                                                                 │
│  BACKLOG → TODO → IN PROGRESS → REVIEW → DONE                  │
│     │        │          │           │        │                  │
│     │        │          │           │        │                  │
│  "No hay   "Planeado  "Trabajando "PR abierto "Mergeado        │
│  prioridad  para este   en el       esperando   y verificado"  │
│  aun"       sprint"    feature"    review"                     │
└─────────────────────────────────────────────────────────────────┘
```

### Linear vs Jira: comparacion

| Caracteristica | Linear | Jira |
|---------------|--------|------|
| **Velocidad** | Muy rapida | Lenta |
| **UI** | Minimalista, moderna | Compleja, sobrecargada |
| **Pricing** | $8/user/mes | Gratis hasta 10 usuarios |
| **Integraciones** | GitHub, Slack, Figma | Todo (pero configuracion compleja) |
| **Curva de aprendizaje** | Baja | Alta |
| **Ideal para** | Startups, equipos agiles | Empresas grandes, procesos estrictos |
| **Comandos de teclado** | Excelentes | Limitadas |

> **Recomendacion:** Para equipos de Flutter startup, Linear es la mejor opcion.
> Es rapida, tiene good GitHub integration, y no necesitas un admin dedicado.

## Figma para Developers

### Developer Mode

Figma tiene un **Developer Mode** que te muestra todo lo que necesitas para implementar:

| Feature | Que muestra | Donde |
|---------|------------|-------|
| **Inspect** | CSS/Flutter code, medidas, colores | Panel derecho |
| **Dev Mode** | Code snippets, asset export | Toggle "Dev" en toolbar |
| **Components** | Props, variants,instances | Panel de componentes |
| **Tokens** | Design tokens exportables | Variables panel |

### Como usar Figma como developer

```
┌─────────────────────────────────────────────────────────────────┐
│  WORKFLOW: Figma → Flutter                                      │
│                                                                 │
│  1. SELECCIONAR el elemento en Figma                           │
│                                                                 │
│  2. INSPECCAR propiedades:                                     │
│     - Size: 375 x 812                                          │
│     - Padding: 16px all sides                                  │
│     - Background: #FFFFFF                                       │
│     - Border radius: 12px                                      │
│                                                                 │
│  3. EXPORTAR assets:                                           │
│     - Icons: SVG (para Icon widget)                            │
│     - Images: PNG @2x (para Image.asset)                       │
│     - Illustrations: PNG @2x o Lottie                          │
│                                                                 │
│  4. IMPLEMENTAR en Flutter:                                     │
│     Container(                                                │
│       padding: EdgeInsets.all(16),                             │
│       decoration: BoxDecoration(                               │
│         color: Color(0xFFFFFFFF),                              │
│         borderRadius: BorderRadius.circular(12),               │
│       ),                                                       │
│       child: ...,                                              │
│     )                                                          │
│                                                                 │
│  5. COMPARAR screenshot de Flutter con Figma                   │
└─────────────────────────────────────────────────────────────────┘
```

### Exportar assets de Figma

| Asset type | Formato | Donde usarlo en Flutter |
|-----------|---------|------------------------|
| Iconos simples | SVG | `SvgPicture.asset()` |
| Iconos complexos | PNG @2x | `Image.asset()` |
| Fotos/imagenes | PNG @2x | `CachedNetworkImage()` |
| Animaciones | Lottie JSON | `Lottie.asset()` |
| Ilustraciones | PNG @2x | `Image.asset()` |

## Notion/Confluence: Documentacion

### Que documentar donde

| Tipo de doc | Donde vive | Ejemplo |
|------------|-----------|---------|
| **Guia del proyecto** | README.md (GitHub) | Setup, estructura, convenciones |
| **Decisiones tecnicas** | docs/adr/ (GitHub) | ADRs |
| **Runbooks** | Notion/Confluence | "Como hacer deploy", "Como resolver X" |
| **Meeting notes** | Notion/Confluence | Notas de planning, retrospectivas |
| **Onboarding** | Notion/Confluence | Guia para developers nuevos |
| **API docs** | Generada (dartdoc) | Documentacion de la API |

### Estructura de Notion para un proyecto

```
┌─────────────────────────────────────────────────────────────────┐
│  NOTION: ESTRUCTURA DE DOCUMENTACION                            │
│                                                                 │
│  📁 Proyecto Flutter                                            │
│  ├── 📄 Vision General                                          │
│  ├── 📁 Engineering                                             │
│  │   ├── 📄 Arquitectura                                        │
│  │   ├── 📁 ADRs                                                │
│  │   ├── 📄 Setup Local                                         │
│  │   ├── 📄 Convenciones de Codigo                              │
│  │   └── 📄 Deployment Guide                                    │
│  ├── 📁 Product                                                 │
│  │   ├── 📄 Roadmap                                             │
│  │   ├── 📁 User Stories                                        │
│  │   └── 📄 Feature Specs                                       │
│  ├── 📁 Design                                                  │
│  │   ├── 📄 Design System                                       │
│  │   └── 📄 Brand Guidelines                                    │
│  └── 📁 Meetings                                                 │
│      ├── 📄 Sprint Planning Notes                               │
│      └── 📄 Retrospective                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Slack/Discord: Convenciones

### Canales recomendados

| Canal | Proposito | Reglas |
|-------|-----------|--------|
| `#general` | Anuncios del equipo | Solo admin puede postear |
| `#dev` | Discusion tecnica | Preguntas, soluciones, links |
| `#dev-random` | Off-topic, memes | Sin trabajo, solo relax |
| `#code-review` | Notificaciones de PRs | Bot de GitHub posts aqui |
| `#deployments` | Status de deploys | Solo anuncios de deploy |
| `#incidents` | Bugs criticos en produccion | Urgencia, no chit-chat |
| `#standup` | Daily async standups | Formato de 3 preguntas |

### Convenciones de Slack

| Accion | Como hacerlo | Ejemplo |
|--------|-------------|---------|
| **Mencionar a alguien** | `@username` | `@carlos puedo revisar tu PR?` |
| **Referenciar canal** | `#canal` | `#dev pregunta sobre BLoC` |
| **Referenciar mensaje** | Share link del mensaje | Copiar link del thread |
| **Reaccionar** | Emoji rapido | 👀 = "estoy viendo", ✅ = "hecho" |
| **Thread** | Responder en thread | No clutter el canal principal |
| **Status** | /status | 🟢 Disponible, 🟡 En reunion, 🔴 No molestar |

### Etiquetas de comunicacion asincrona

```
┌─────────────────────────────────────────────────────────────────┐
│  COMUNICACION ASINCRONA: CODIGOS NO ESCRITOS                    │
│                                                                 │
│  🟢 Respondo rapido (minutos)    → Urgente, estoy disponible  │
│  🟡 Respondo cuando pueda       → No urgente, estoy busy     │
│  🔴 No respondo hoy             → Focus time, mañana         │
│  📧 Mejor por email              → Formal, necesita registro  │
│  📞 Mejor por call               → Complejo, necesita discusion│
│  📝 Mejor por documento          → Largo, necesita estructura │
│                                                                 │
│  REGLA: No esperes respuesta inmediata en沟沟 Slack.           │
│  Si es urgente, llama o usa el canal de incidents.             │
└─────────────────────────────────────────────────────────────────┘
```

## Pair Programming

### Que es

Dos developers trabajan en la **misma tarea** al mismo tiempo. Uno escribe codigo (driver),
el otro revisa y piensa en la estrategia (navigator).

```
┌─────────────────────────────────────────────────────────────────┐
│  PAIR PROGRAMMING: ROLES                                        │
│                                                                 │
│  ┌────────────────┐         ┌────────────────┐                 │
│  │    DRIVER      │         │   NAVIGATOR    │                 │
│  │                │         │                │                 │
│  │  Escribe codigo│  ←────→ │  Revisa codigo │                 │
│  │  Usa el teclado│         │  Piensa en     │                 │
│  │  Implementa    │         │  estrategia    │                 │
│  │                │         │  Busca bugs    │                 │
│  └────────────────┘         └────────────────┘                 │
│                                                                 │
│  Se rotan cada 25-30 minutos (como Pomodoro)                   │
└─────────────────────────────────────────────────────────────────┘
```

### Cuándo hacer pair programming

| Situacion | Hacer pair? | Razon |
|-----------|-------------|-------|
| Bug complejo | ✅ Si | Dos cerebros > uno |
| Feature nueva y desconocida | ✅ Si | Aprendizaje rapido |
| Code review rapido | ✅ Si | Mas eficiente que comments |
| Feature rutinaria | ❌ No | desperdicio de recursos |
| Developer senior + junior | ✅ Si | Mentoria efectiva |
| Ambos son senior en la misma area | ⚠️ Opcional | Puede ser overkill |

### Herramientas de pair programming

| Herramienta | Que es | Precio | Features clave |
|------------|--------|--------|---------------|
| **VS Code Live Share** | Extension de VS Code | Gratis | Edicion simultanea, terminal compartida |
| **Tuple** | App dedicada a pairing | $25/user/mes | Audio optimizado, dibujo en pantalla |
| **Cursor** | IDE con AI + sharing | Gratis tier | AI suggestions + code sharing |
| **GitHub Codespaces** | IDE en la nube | Gratis tier | Environment compartido |

## Mob Programming

### Que es

Todo el equipo (3-6 personas) trabaja en la **misma tarea** al mismo tiempo.
Un driver, el resto navegan.

```
┌─────────────────────────────────────────────────────────────────┐
│  MOB PROGRAMMING                                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  DRIVER (1 persona)                                      │  │
│  │  Escribe codigo en la pantalla principal                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐  │
│  │ Navigator  │ │ Navigator  │ │ Navigator  │ │ Navigator  │  │
│  │ 1         │ │ 2         │ │ 3         │ │ 4         │  │
│  │ Piensa    │ │ Sugiere   │ │ Revisa    │ │ Documenta │  │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘  │
│                                                                 │
│  Se rota el driver cada 10-15 minutos                          │
└─────────────────────────────────────────────────────────────────┘
```

### Cuando usar mob programming

| Situacion | Usar mob? | Razon |
|-----------|-----------|-------|
| Arquitectura de un modulo nuevo | ✅ Si | Consenso desde el inicio |
| Debugging de bug critico | ✅ Si | Multiples perspectivas |
| Onboarding de developer nuevo | ✅ Si | Aprendizaje inmersivo |
| Feature simple | ❌ No | Demasiada gente |
| Todo el tiempo | ❌ No | Exhaustivo y costoso |

## Time Management

### Pomodoro Technique

```
┌─────────────────────────────────────────────────────────────────┐
│  POMODORO: 25-5-25-5-25-5-25-5-30                              │
│                                                                 │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐            │
│  │Focus │  │Break │  │Focus │  │Break │  │Focus │            │
│  │25min │  │ 5min │  │25min │  │ 5min │  │25min │            │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘            │
│                                                                 │
│  Despues de 4 pomodoros: descanso largo (15-30 min)            │
│                                                                 │
│  HERRAMIENTAS:                                                  │
│  - VS Code: Extension "Pomodoro Timer"                         │
│  - Terminal: `timer 25m` (si tienes instalado)                  │
│  - Web: tomato-timer.com                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Deep Work Blocks

| Tipo de trabajo | Cuando | Duracion minima | Que proteger |
|----------------|--------|-----------------|-------------|
| **Deep work** | Manana temprano | 2-4 horas | Sin meetings, sin Slack |
| **Shallow work** | Tarde | 1-2 horas | Meetings permitidos |
| **Collaboration** | Cualquier momento | 30-60 min | Pair/mob programming |
| **Learning** | Antes o despues de deep work | 30-60 min | Cursos, docs, experimentation |

### Como bloquear focus time

```
┌─────────────────────────────────────────────────────────────────┐
│  BLOQUEAR FOCUS TIME: PASO A PASO                               │
│                                                                 │
│  1. GOOGLE CALENDAR → Crear evento recurrente                  │
│     "Focus Time - No meeting"                                   │
│     Lunes-Viernes, 9:00-12:00                                  │
│     Configuracion: "Mark as busy"                               │
│                                                                 │
│  2. SLACK → Actualizar status                                   │
│     /status "🔴 Focus time, respondo despues de las 12"        │
│                                                                 │
│  3. NOTIFICATIONS → Silenciar                                   │
│     Mute Slack, email, Telegram durante focus time              │
│                                                                 │
│  4. COMUNICAR al equipo                                         │
│     "Estoy en focus time de 9-12. Si es urgente, llamen"       │
│                                                                 │
│  5. RESPETAR el tiempo de otros                                 │
│     No propongas meetings durante focus time de otros          │
└─────────────────────────────────────────────────────────────────┘
```

## Tool Comparison Table

| Proposito | Herramienta principal | Alternativa | Cuando usar cual |
|-----------|----------------------|-------------|-----------------|
| **Codigo + reviews** | GitHub | GitLab | GitHub para la mayoria |
| **Gestion de tareas** | Linear | Jira, GitHub Projects | Linear para startups |
| **Comunicacion** | Slack | Discord, Teams | Slack para empresas |
| **Documentacion** | Notion | Confluence, GitHub Wiki | Notion para startups |
| **Diseno** | Figma | Sketch, Adobe XD | Figma es estandar |
| **Pair programming** | VS Code Live Share | Tuple | Live Share (gratis) |
| **Video calls** | Google Meet | Zoom, Teams | Meet para equipos Google |
| **Time tracking** | Toggl | Clockify, RescueTime | Toggl para tracking manual |
| **CI/CD** | GitHub Actions | Codemagic, Bitrise | GitHub Actions (integrado) |
| **Monitoreo** | Sentry | Crashlytics | Sentry multi-plataforma |

## Resumen

```
┌─────────────────────────────────────────────────────────────────┐
│           HERRAMIENTAS DE COLABORACION: RESUMEN                 │
│                                                                 │
│  ✅ GitHub: Issues + Projects + CODEOWNERS + Discussions       │
│  ✅ Linear: Gestion de sprints y tareas                        │
│  ✅ Figma: Developer Mode para inspeccionar disenos            │
│  ✅ Notion: Documentacion viva del proyecto                    │
│  ✅ Slack: Convenciones de canales, threads, status             │
│  ✅ Pair programming: VS Code Live Share o Tuple               │
│  ✅ Focus time: Bloquear 2-4 horas diarias de deep work        │
│  ✅ Usa la herramienta correcta para cada necesidad            │
└─────────────────────────────────────────────────────────────────┘
```
