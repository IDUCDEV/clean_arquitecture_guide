# 08: Patrones y Anti-patrones de Equipo

## Anti-patrones en Code Reviews

### 1. Rubber-Stamping

**Que es:** Aprobar un PR sin revisar el codigo.

```
COMO SE VE:
- "LGTM!" sin comentarios en un PR de 500 lineas
- Aprobar en 2 minutos sin leer el codigo
- Solo mirar el titulo del PR

POR QUE ES MALO:
- Bugs pasan sin ser detectados
- Codigo inconsistente se normaliza
- El reviewer pierde credibilidad

COMO ARREGLARLO:
- Usar la checklist de code review
- Timebox minimo de review: 10 min por 100 lineas
- CODEOWNERS para asignar revisores relevantes
```

### 2. Nitpicking

**Que es:** Enfocarse en detalles triviales ignorando issues importantes.

```
COMO SE VE:
- 15 comments sobre nombres de variables
- 0 comments sobre la logica de negocio
- Discutir espacios vs tabs en un PR con bugs

POR QUE ES MALO:
- Desvia atencion de problemas reales
- Frustra al autor del PR
- Envia el mensaje de que el estilo importa mas que la logica

COMO ARREGLARLO:
- Revisar correctness PRIMERO, style DESPUES
- Usar linters/formatters para estilo automaticamente
- Regla: max 20% de comments en style, minimo 80% en logica
```

### 3. Ego-Driven Reviews

**Que es:** Imponer preferencias personales como estandares tecnicos.

```
COMO SE VE:
- "Yo lo hago asi" sin razon tecnica
- Bloquear PRs por preferencias personales
- No aceptar alternativas validas

POR QUE ES MALO:
- Crea un ambiente toxico
- Desmotiva a otros developers
- El codigo se vuelve reflejo de 1 persona

COMO ARREGLARLO:
- Siempre dar razon TECNICA (no personal)
- Aceptar que hay multiples formas validas
- Usar ADRs para documentar decisiones de equipo
```

### 4. Review Bottleneck

**Que es:** Un solo reviewer se convierte en cuello de botella.

```
COMO SE VE:
- 5 PRs esperando revision del mismo reviewer
- El reviewer es "el unico que sabe" de cierta area
- PRs esperando dias para ser revisados

POR QUE ES MALO:
- Los developers se bloquean
- Si el reviewer se va, nadie puede revisar
- El conocimiento no se distribuye

COMO ARREGLARLO:
- CODEOWNERS para distribuir reviews
- Bus factor: minimo 2 personas por area
- Rotar revisores regularmente
- Meta: ningun PR esperando mas de 4 horas
```

## Anti-patrones en Comunicacion

### 1. Silo of Knowledge

**Que es:** Solo una persona conoce cierta area del codigo.

```
COMO SE VE:
- "Solo Juan sabe como funciona el modulo de pagos"
- "Cuando Juan se fue de vacaciones, nadie pudo deployar"
- Documentacion inexistente o desactualizada

RIESGO: Si esa persona se va, el equipo pierde capacidad critica

COMO ARREGLARLO:
- Pair programming rotativo
- Documentacion obligatoria para areas criticas
- Code reviews cruzados entre areas
- Tech talks internas donde cada uno explica su area
```

### 2. Documentation Graveyard

**Que es:** Documentacion que se escribe una vez y nunca se actualiza.

```
COMO SE VE:
- READMEs con instrucciones de hace 2 anios
- ADRs que contradicen el codigo actual
- Wiki con info obsoleta que confunde a nuevos developers

POR QUE ES MALO:
- Nuevos developers siguen docs incorrectos
- Pierde confianza en la documentacion
- Nadie lee documentacion vieja

COMO ARREGLARLO:
- Documentacion como codigo: versionada y revisada
- Review de docs en cada release importante
- Obligar que el PR incluya updates de docs si aplica
- Mantener solo documentacion que se use activamente
```

### 3. Meeting Overload

**Que es:** Tantas reuniones que no queda tiempo para codear.

```
SENALES:
- Mas de 3 horas de meetings al dia
- Standup de 30 minutos (deberia ser 15)
- Meetings sin agenda ni outcome
- "Tenemos que alinear" como razon para todo

COMO ARREGLARLO:
- Regla: no meetings los martes y jueves (focus days)
- Toda meeting debe tener agenda y outcomes
- Maximo 5 personas por meeting
- Default a async (Slack/docs) en vez de meeting
- Meeting de 25 o 50 minutos, no de 30 o 60
```

## Anti-patrones en Teamwork

### 1. Hero Culture

**Que es:** Celebrar al developer que "salva" el proyecto trabajando noches.

```
COMO SE VE:
- "Pedro se quedo hasta las 3am para entregar el feature"
- El equipo depende de que alguien trabaje overtime
- Burnout normalizado como sena de compromiso

POR QUE ES MALO:
- Promueve malos habitos de trabajo
- Crea dependencia de individuos, no de procesos
- Lleva a burnout y rotacion de talento

COMO ARREGLARLO:
- Celebrar planificacion, no firefighting
- Estimar con datos para evitar sorpresas
- Buffer de 20% en sprints para imprevistos
- Si alguien trabaja overtime, es un failure del proceso
```

### 2. Blame Game

**Que es:** Buscar culpables en vez de soluciones cuando algo sale mal.

```
COMO SE VE:
- "Quien hizo este commit que rompio todo?"
- "El equipo de backend nos paso codigo malo"
- Post-mortems donde se senala individuos

POR QUE ES MALO:
- Crea miedo a cometer errores
- La gente esconde bugs en vez de reportarlos
- Destruye la confianza del equipo

COMO ARREGLARLO:
- Blameless postmortems: enfocarse en procesos, no personas
- "Que proceso fallo?" en vez de "quien fallo?"
- Celebrar el reporte temprano de bugs
- Crear ambiente seguro para admitir errores
```

### 3. Over-Engineering for Ego

**Que es:** Construir soluciones complejas para demostrar conocimiento tecnico.

```
COMO SE VE:
- Patron de arquitectura sobre-ingeniado para un CRUD simple
- 15 capas de abstraccion para una feature basica
- "No uso X porque no es elegante" sin razon de negocio

POR QUE ES MALO:
- Aumenta complejidad innecesariamente
- Dificulta el onboarding de nuevos developers
- Mas codigo = mas bugs posibles

COMO ARREGLARLO:
- "The best code is no code at all"
- KISS principle: Keep It Simple, Stupid
- Code review: preguntar "por que esta abstraccion?"
- Medir complejidad ciclomatica como metrica
```

## Senales de un Ambiente Toxico

| Senal | Ejemplo | Que hacer |
|-------|---------|-----------|
| **Miedo a reportar bugs** | "Si reporto esto, me van a culpar" | Blameless culture |
| **Overtime normalizado** | "Todos trabajan fines de semana" | Estimar mejor, cortar scope |
| **Informacion asimetrica** | "Nadie sabe que pasa en el otro equipo" | Comunicacion cross-team |
| **Falta de safety** | "Si pregunto, parezco incompetente" | Psicological safety training |
| **Micromanagement** | "Me piden hourly updates" | Confiar en el equipo |
| **Scapegoating** | "Siempre culpan al mismo" | Procesos, no personas |
| **Falta de crecimiento** | "No hay tiempo para aprender" | Dedica tiempo a learning |
| **Comunicacion pasivo-agresiva** | "Como quieras..." | Feedback directo y respetuoso |

## Como Mejorar la Comunicacion del Equipo Sistematicamente

### Paso 1: Evaluar el estado actual

```
┌─────────────────────────────────────────────────────────────────┐
│  EVALUACION: 5 AREAS DE COMUNICACION                            │
│                                                                 │
│  1. CODE REVIEWS   [1]-[2]-[3]-[4]-[5]                        │
│     ¿Los reviews son constructivos y oportunos?                │
│                                                                 │
│  2. DOCUMENTACION  [1]-[2]-[3]-[4]-[5]                        │
│     ¿La documentacion esta actualizada y es util?              │
│                                                                 │
│  3. MEETINGS       [1]-[2]-[3]-[4]-[5]                        │
│     ¿Las reuniones son efectivas y necesarias?                 │
│                                                                 │
│  4. FEEDBACK       [1]-[2]-[3]-[4]-[5]                        │
│     ¿El feedback fluye en ambas direcciones?                   │
│                                                                 │
│  5. TRANSPARENCIA  [1]-[2]-[3]-[4]-[5]                        │
│     ¿La informacion esta disponible para todos?                │
│                                                                 │
│  Escala: 1=Muy malo, 5=Excelente                               │
└─────────────────────────────────────────────────────────────────┘
```

### Paso 2: Elegir 1-2 areas para mejorar

No intentes arreglar todo a la vez. Elige las areas con menor score
y enfoca esfuerzo ahi.

### Paso 3: Implementar cambios concretos

| Area baja | Accion concreta | Timeline |
|-----------|----------------|----------|
| Code reviews | Implementar checklist + CODEOWNERS | 1 semana |
| Documentacion | Crear ADR template + empezar con 3 ADRs | 2 semanas |
| Meetings | Implementar "no meeting days" + agendas | 1 semana |
| Feedback | Capacitar en modelo SBI | 2 semanas |
| Transparencia | Crear canal de incidentes + status page | 1 semana |

## Patrones que Funcionan

### 1. Documentation-First

```
ANTES DE ESCRIBIR CODIGO:
1. Crear ADR para la decision tecnica
2. Actualizar README si es modulo nuevo
3. Definir API publica antes de implementar
4. Escribir tests primero (TDD)

DESPUES:
5. Actualizar docs en el mismo PR
6. Incluir screenshots/videos si hay UI
```

### 2. Async-First

```
COMUNICACION ASINCRONA POR DEFECTO:
- Status updates → Slack/standup async
- Discusiones tecnicas → GitHub Issues/Discussions
- Decisiones → ADRs + review comments
- Solo para meeting: pair programming, incidentes, desacuerdos tecnicos
```

### 3. Blameless Postmortems

```
┌─────────────────────────────────────────────────────────────────┐
│  POSTMORTEM SIN CULPA: FORMATO                                  │
│                                                                 │
│  1. HECHOS: Que paso? (sin juicios)                            │
│  2. TIMELINE: Cuando paso?                                     │
│  3. IMPACTO: A quien afecto?                                   │
│  4. ROOT CAUSE: Que fallo en el PROCESO?                       │
│  5. QUE FUNCIONO: Que del sistema ayudo?                       │
│  6. QUE MEJORAR: Acciones concretas y medibles                 │
│  7. ACTION ITEMS: Quien hace que, para cuando                  │
│                                                                 │
│  REGLA: Nunca mencionar nombres individuales.                  │
│  El focus es el PROCESO, no la PERSONA.                        │
└─────────────────────────────────────────────────────────────────┘
```

### 4. Tech Talks

```
┌─────────────────────────────────────────────────────────────────┐
│  TECH TALKS: COMO IMPLEMENTARLOS                                │
│                                                                 │
│  FRECUENCIA: 1-2 veces al mes                                  │
│  DURACION: 30-45 minutos                                       │
│  FORMATO: 20 min presentacion + 15-20 min Q&A                  │
│  TEMA: Cualquier developer presenta algo que aprendio          │
│                                                                 │
│  IDEAS DE TEMAS:                                                │
│  - "Como resolvi este bug complejo"                            │
│  - "Que aprendi con esta nueva libreria"                       │
│  - "Como funciona internamente X"                              │
│  - "Refactor que hice y por que"                               │
│  - "Comparativa de alternativas para Y"                        │
│                                                                 │
│  BENEFICIOS:                                                    │
│  - Comparte conocimiento                                       │
│  - Practica comunicacion tecnica                               │
│  - Crea cultura de aprendizaje                                 │
│  - Ayuda al presentador a consolidar conocimiento              │
└─────────────────────────────────────────────────────────────────┘
```

## Self-Assessment: Que tan buena es tu comunicacion?

### Checklist个人

| # | Pregunta | Si | No |
|---|----------|----|----|
| 1 | Mis code reviews tienen comentarios constructivos con alternativas | | |
| 2 | Documento las decisiones tecnicas que tomo | | |
| 3 | Puedo explicar porque elegi una arquitectura sin usar jerga | | |
| 4 | Cuando no se algo, pregunto en vez de quedarme callado | | |
| 5 | Cuando algo no funciona, propongo soluciones, no solo reporto problemas | | |
| 6 | Mis PR descriptions tienen contexto suficiente para un extraño | | |
| 7 | Respito el focus time de mis companeros | | |
| 8 | En standups soy conciso y accionable | | |
| 9 | Cuando doy feedback, uso el modelo SBI o equivalente | | |
| 10 | Comparto conocimiento proactivamente (docs, tech talks, pair) | | |

### Score

| Puntuacion | Nivel | Accion |
|-----------|-------|--------|
| 9-10 | Excelente | Enfoca en mentorar a otros |
| 7-8 | Bueno | Trabaja en las areas que fallaste |
| 5-6 | Regular | Elige 2-3 areas y mejora activamente |
| 3-4 | Necesita trabajo | Busca feedback de tu equipo |
| 0-2 | Critico | Considera buscar mentororia |

## Resumen

```
┌─────────────────────────────────────────────────────────────────┐
│  PATRONES Y ANTI-PATRONES: RESUMEN                              │
│                                                                 │
│  🚫 ANTI-PATRONES A EVITAR:                                    │
│  - Rubber-stamping en code reviews                             │
│  - Silo of knowledge                                           │
│  - Meeting overload                                            │
│  - Hero culture                                                │
│  - Blame game                                                  │
│                                                                 │
│  ✅ PATRONES A ADOPTAR:                                        │
│  - Documentation-first                                         │
│  - Async-first                                                 │
│  - Blameless postmortems                                       │
│  - Tech talks regulares                                        │
│  - Self-assessment continuo                                    │
│                                                                 │
│  ✅ CLAVE: La comunicacion es una SKILL que se entrena,        │
│  no un talento innato. Practica conscientemente.               │
└─────────────────────────────────────────────────────────────────┘
```
