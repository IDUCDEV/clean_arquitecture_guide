# 04: Comunicacion Tecnica

## Architecture Decision Records (ADRs)

Un **ADR** (Architecture Decision Record) documenta una decision tecnica importante,
el contexto en que se tomo, y las alternativas consideradas. Son la forma mas efectiva
de documentar *por que* se hicieron las cosas de cierta manera.

### Por que usar ADRs

| Sin ADR | Con ADR |
|---------|---------|
| "Por que usamos BLoC en vez de Riverpod?" | "El ADR-003 documenta la razon" |
| "Quien decidio esto?" | "Lo decidimos en el ADR-007 con el equipo" |
| "Cada nuevo developer pregunta lo mismo" | "Lee los ADRs, ahi esta todo" |
| "La documentacion esta desactualizada" | "Los ADRs se actualizan cuando cambia la decision" |

### Template de ADR

```markdown
# ADR-001: Usar BLoC como state management

## Estado
Aprobado | 2024-01-15

## Contexto
Necesitamos un state management para la app que:
- Sea testeable
- Separe business logic de UI
- Tenga buena documentacion
- El equipo conozca o pueda aprender rapido

## Decision
Usaremos BLoC como patron principal de state management.

## Alternativas consideradas

| Alternativa | Pros | Contras | Decision |
|-------------|------|---------|----------|
| Riverpod | Moderno, flexible | Curva de aprendizaje mayor, menos maduro | Descartado |
| Provider | Simple, oficial | Testing dificil, acoplamiento | Descartado |
| GetX | Todo-en-uno, rapido de empezar | Anti-patrones, hard to test | Descartado |
| BLoC | Testing excelent, separacion clara | Verboso, boilerplate | ✅ Seleccionado |

## Consecuencias
- Todos los features nuevos usan BLoC
- El equipo debe aprender BLoC (1-2 semanas)
- Necesitamos crear templates de BLoC para consistencia
- Los features existentes se migran gradualmente

## Referencias
- [BLoC Library](https://bloclibrary.dev/)
- [Flutter BLoC Example](https://github.com/felangel/bloc/tree/master/examples)
```

### Cuando crear un ADR

| Situacion | Ejemplo | Prioridad |
|-----------|---------|-----------|
| Tecnologia nueva | "Usar Supabase vs Firebase" | Alta |
| Patron de arquitectura | "Clean Architecture vs MVVM" | Alta |
| Cambio de framework | "Migrar de GetX a BLoC" | Alta |
| Convencion de codigo | "Usar Freezed para models" | Media |
| Herramienta nueva | "Usar Very Good CLI" | Media |
| Proceso de CI/CD | "GitHub Actions vs Codemagic" | Baja |

## Escritura de Documentacion Tecnica

### Tipos de documentacion

| Tipo | Para que sirve | Quien la lee | Donde vive |
|------|---------------|-------------|-----------|
| **README** | Onboarding, vision general | Developers nuevos | Raiz del repo |
| **API docs** | Como usar un modulo | Otros developers | Generada (dartdoc) |
| **ADRs** | Decisiones tecnicas | Todo el equipo | `docs/adr/` |
| **Guia de setup** | Como correr el proyecto | Developers nuevos | README o docs/ |
| **Changelog** | Que cambio en cada version | Usuarios y developers | CHANGELOG.md |

### Principios de buena documentacion tecnica

```
┌─────────────────────────────────────────────────────────────────┐
│           PRINCIPIOS DE DOCUMENTACION TECNICA                    │
│                                                                 │
│  1. CLARIDAD    → Escribe para tu yo futuro en 6 meses         │
│  2. BREVEDAD    → Corta no es sinónimo de poco profunda        │
│  3. ESTRUCTURA  → Usa headings, listas, tablas                 │
│  4. ACTUALIZADA → Si no esta actualizada, es peor que no tener │
│  5. BUSCABLE    → Usa keywords que la gente buscaria           │
│                                                                 │
│  REGLA: Si algo toma > 10 minutos de explicar, documentalo.    │
└─────────────────────────────────────────────────────────────────┘
```

### README de modulo: estructura recomendada

```markdown
# Nombre del Modulo

## Que es
[1-2 parrafos explicando que hace este modulo]

## Como usar
[Instrucciones claras con codigo de ejemplo]

## API
[Tabla de la API principal]

## Dependencias
[Que necesita este modulo para funcionar]

## Tests
[Como correr los tests de este modulo]

## Troubleshooting
[Errores comunes y como resolverlos]
```

## Estimacion de Tiempo de Desarrollo

### Metodos de estimacion

| Metodo | Precision | Velocidad | Cuando usar |
|--------|-----------|-----------|-------------|
| **T-shirt sizing** | Baja (S/M/L/XL) | Muy rapido | Planning inicial, priorizacion |
| **Story points** | Media (Fibonacci) | Rapido | Sprints, equipos agiles |
| **Planning poker** | Alta | Lento | Features complejas |
| **Time-based** | Baja | Media | Tareas conocidas |

### T-shirt sizing

| Size | Rango de horas | Ejemplo |
|------|---------------|---------|
| **XS** | 1-2 horas | Fix de typo, cambio de color |
| **S** | 2-4 horas | Bug fix simple, cambio en un widget |
| **M** | 1-2 dias | Feature completa con tests |
| **L** | 3-5 dias | Feature con multiples pantallas |
| **XL** | 1-2 semanas | Feature completa con backend |
| **XXL** | > 2 semanas | Migracion, arquitectura nueva |

### Story Points (Fibonacci)

| Points | Equivalencia | Ejemplo |
|--------|-------------|---------|
| **1** | Trivial | Cambiar un texto en UI |
| **2** | Simple | Agregar un boton con accion |
| **3** | Media | Feature CRUD basico |
| **5** | Compleja | Feature con multiples estados |
| **8** | Muy compleja | Integracion con API externa |
| **13** | Epic | Migracion de base de datos |

### Planning Poker: como funciona

```
┌─────────────────────────────────────────────────────────────────┐
│              PLANNING POKER: PASO A PASO                        │
│                                                                 │
│  1. El PM presenta la user story                               │
│                                                                 │
│  2. El equipo discute y pregunta                               │
│     "Que implica esto?"                                         │
│     "Hay dependencias?"                                         │
│     "Que tan bien definido esta?"                               │
│                                                                 │
│  3. Cada developer secretly elige un numero                     │
│     (1, 2, 3, 5, 8, 13, ?, coffee)                            │
│                                                                 │
│  4. Se revelan los numeros SIMULTANEAMENTE                      │
│                                                                 │
│  5. Si hay consenso → estimacion aceptada                       │
│     Si hay dispersion → los extremos explican su razon          │
│                                                                 │
│  6. Se repite hasta llegar a consenso                           │
│                                                                 │
│  ⚠️ REGLA: El mas rapido no siempre es el correcto             │
│  ✅ REGLA: La discusion es mas valiosa que el numero           │
└─────────────────────────────────────────────────────────────────┘
```

### Como estimar con datos reales

```bash
# 1. Mira estimaciones PASADAS (no las que diste, las que hiciste)
# En GitHub, calcula tiempo real de features anteriores:

# Features completas en los ultimos 3 meses
gh pr list --state merged --json title,createdAt,mergedAt,labels \
  --jq '.[] | select(.labels[]?.name == "feature") | 
  {title: .title, days: ((.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)) / 86400 | floor}'

# 2. Promedia y ajusta
# Si tu estimacion fue 3 dias y el real fue 5, multiplica por 1.66

# 3. Aplica el multiplier a futuras estimaciones
```

## Decir "No" Constructivamente

### Alternativas a "Eso no se puede hacer"

| ❌ Decir | ✅ Decir en su lugar |
|---------|---------------------|
| "Eso no se puede" | "Eso es posible, pero [razon]. Podemos hacer [alternativa]" |
| "No hay tiempo" | "Para hacerlo bien necesitamos X tiempo. Que priorizamos?" |
| "Eso es mal diseno" | "Eso puede causar [problema]. Que te parece [alternativa]?" |
| "El backend no lo soporta" | "Necesitamos [cambio en backend] para esto. Que tan factible es?" |
| "Nunca lo hemos hecho asi" | "Podemos probar [alternativa]. Tiene ventajas como [X, Y, Z]" |

### Framework para decir "no" con alternativas

```
┌─────────────────────────────────────────────────────────────────┐
│  FRAMEWORK: ARL (Afirmar - Razón - Limitar/Alternativa)        │
│                                                                 │
│  1. AFIRMAR: Entiendo que quieres [X]                           │
│     "Entiendo que quieres agregar el filtro avanzado"           │
│                                                                 │
│  2. RAZON: La limitacion es [razon tecnica concreta]            │
│     "La API actual no soporta filtros anidados sin              │
│      un cambio en el backend que toma ~3 dias"                  │
│                                                                 │
│  3. ALTERNATIVA: Podemos hacer [opcion viable]                  │
│     "Podemos empezar con filtros basicos (1 dia) y              │
│      agregar los avanzados en el proximo sprint"                │
└─────────────────────────────────────────────────────────────────┘
```

## Reportar Blockers Efectivamente

### Estructura de un reporte de blocker

```
┌─────────────────────────────────────────────────────────────────┐
│  REPORTE DE BLOCKER                                             │
│                                                                 │
│  CONTEXTO:                                                      │
│  [Que estoy haciendo, que feature, que parte del codigo]        │
│                                                                 │
│  QUE INTENTE:                                                   │
│  [Lista de cosas que ya intente resolver]                       │
│                                                                 │
│  QUE NECESITO:                                                  │
│  [Que ayuda especifica necesito del equipo]                     │
│                                                                 │
│  URGENCIA:                                                      │
│  [Bloqueado completamente / Puedo avanzar con workaround]       │
│                                                                 │
│  TIMELINE:                                                      │
│  [Cuando necesito la respuesta]                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ejemplo de buen vs mal reporte

**Mal reporte ❌**
```
"No me funciona el login, ayuda"
```

**Buen reporte ✅**
```
CONTEXTO:
Estoy implementando el login con Google en `lib/features/auth/`.
Usando `google_sign_in: ^6.1.0` y `supabase_flutter: ^2.0.0`.

QUE INTENTE:
1. Revisar que el OAuth client ID este configurado correctamente
2. Verificar que los SHA-1 fingerprints coincidan con Firebase
3. Probar en Both Android e iOS
4. Revisar logs con `flutter run --verbose`

El error es:
```
PlatformException(sign_in_failed, com.google.android.gms.common.api.ApiException: 10, null, null)
```

QUE NECESITO:
Alguien que haya configurado Google Sign-In con Supabase
recientemente. Creo que el problema es la configuracion de
OAuth en Google Cloud Console, pero no estoy seguro.

URGENCIA:
Bloqueado completamente. No puedo avanzar con el feature de auth.

TIMELINE:
Necesito esto resuelto antes del viernes para entregar el PR.
```

## Standups: Que Decir y Que No

### Formato de standup (2-3 minutos)

```
┌─────────────────────────────────────────────────────────────────┐
│  STANDUP: 3 PREGUNTAS                                           │
│                                                                 │
│  1. ¿Que hice ayer?                                            │
│     "Ayer termine el PR del perfil de usuario, esta en review" │
│                                                                 │
│  2. ¿Que hare hoy?                                             │
│     "Hoy voy a trabajar en el flujo de login con Google"       │
│                                                                 │
│  3. ¿Hay bloqueantes?                                          │
│     "Necesito que alguien revise el PR #247, esta bloqueando"  │
└─────────────────────────────────────────────────────────────────┘
```

### Que NO decir en standup

| ❌ No decir | ✅ Decir en su lugar |
|------------|---------------------|
| "Ayer me sente a leer codigo por 4 horas" | "Ayer investigue la integracion con Supabase Auth" |
| "No hice nada porque estaba bloqueado" | "Estoy bloqueado por [X], necesito ayuda de [persona]" |
| "Hoy voy a escribir 200 lineas de codigo" | "Hoy implementare la pantalla de login" |
| Todo el historial de lo que hiciste | Solo lo relevante para el equipo |
| Problemas que solo te afectan a ti | Problemas que afectan al equipo o al sprint |

### Async Standups

Para equipos remotos en diferentes zonas horarias:

| Herramienta | Como funciona | Cuando usar |
|------------|---------------|-------------|
| **Slack daily** | Post en canal con las 3 preguntas | Equipos remotos |
| **GitHub Discussion** | Thread diario | Equipos que ya usan GitHub |
| **Loom video** | Video corto de 2 min | Contexto visual necesario |
| **Notion/T Linear** | Form en base de datos | Equipos que usan estas tools |

**Template para async standup:**
```
📅 [Fecha]
🙋 [Tu nombre]

✅ Ayer: [Que completaste]
📌 Hoy: [Que planeas hacer]
🚧 Blockers: [Que te detiene, o "Ninguno"]
```

## Plantillas para Comunicacion Tecnica

### Incident Report Template

```markdown
# Incident Report: [Titulo]

## Resumen
[Que paso en 1-2 oraciones]

## Timeline
- [HH:MM] [Evento 1]
- [HH:MM] [Evento 2]
- [HH:MM] [Resuelto]

## Impacto
- [Usuarios afectados]
- [Features afectadas]
- [Duracion del downtime]

## Root Cause
[Causa raiz del problema]

## Que funciono
[Que del sistema de monitoreo/alertas funciono]

## Que mejorar
[Acciones concretas para prevenir que vuelva a pasar]

## Acciones
- [ ] [Accion 1] - Responsable: [Persona] - Fecha: [Fecha]
- [ ] [Accion 2] - Responsable: [Persona] - Fecha: [Fecha]
```

### Technical Proposal Template

```markdown
# Proposal: [Titulo]

## Problema
[Que problema estamos resolviendo?]

## Solucion propuesta
[Descripcion tecnica de la solucion]

## Alternativas
| Alternativa | Pros | Contras | Esfuerzo |
|-------------|------|---------|----------|
| A | ... | ... | ... |
| B | ... | ... | ... |

## Decision recomendada
[Cual elegimos y por que]

## Plan de implementacion
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

## Riesgos
- [Riesgo 1]: [Mitigacion]
- [Riesgo 2]: [Mitigacion]

## Timeline estimada
[Duracion total y hitos]
```

## Principios de Escritura Tecnica

```
┌─────────────────────────────────────────────────────────────────┐
│         PRINCIPIOS DE ESCRITURA TECNICA                          │
│                                                                 │
│  1. Escribe para el LECTOR, no para ti                         │
│     → Explica contexto que tu ya sabes pero el lector no       │
│                                                                 │
│  2. Primero la CONCLUSION, luego el detalle                     │
│     → "Usamos X porque Y" antes que la historia completa       │
│                                                                 │
│  3. Usa STRUCTURE consistente                                   │
│     → Headings, listas, tablas. No parrafos largos             │
│                                                                 │
│  4. Incluye EJEMPLOS de codigo                                  │
│     → Un ejemplo vale mas que mil palabras                      │
│                                                                 │
│  5. Actualiza o BORRA                                           │
│     → Documentacion vieja es peor que ninguna                  │
│                                                                 │
│  6. Mide si FUNCIONA                                            │
│     → Si la gente no lee tu doc, algo estas haciendo mal       │
└─────────────────────────────────────────────────────────────────┘
```

## Resumen

```
┌─────────────────────────────────────────────────────────────────┐
│           COMUNICACION TECNICA: RESUMEN                          │
│                                                                 │
│  ✅ Crea ADRs para decisiones tecnicas importantes             │
│  ✅ Estima con datos, no con intuicion                         │
│  ✅ Di "no" con alternativas, no con negativas                  │
│  ✅ Reporta blockers con contexto, intentos, y necesidades     │
│  ✅ En standups: se conciso, enfocado, y accionable            │
│  ✅ Escribe documentacion para tu yo futuro                    │
│  ✅ Usa templates para consistencia                            │
└─────────────────────────────────────────────────────────────────┘
```
