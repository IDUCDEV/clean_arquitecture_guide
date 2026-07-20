# 01: Code Reviews Efectivos

## Que es un Code Review y por que importa

Un **code review** es el proceso donde otro developer revisa tu codigo antes de que entre
a la rama principal. No es un examen — es una **colaboracion** para mejorar la calidad
del codigo y compartir conocimiento.

```
┌──────────────┐     PR      ┌──────────────┐     Feedback    ┌──────────────┐
│   Developer  │ ──────────> │   Revisor    │ ──────────────> │   Developer  │
│   (autor)    │             │   (reviewer) │                 │   (autor)    │
│              │ <────────── │              │ <────────────── │              │
│   corrige    │             │   comenta    │                 │   aprueba    │
└──────────────┘             └──────────────┘                 └──────────────┘
                                    │
                                    ▼
                            ┌──────────────┐
                            │   Codigo     │
                            │   mejorado   │
                            └──────────────┘
```

### Beneficios concretos

| Beneficio | Descripcion |
|-----------|-------------|
| **Deteccion temprana** | Encuentras bugs antes de que lleguen a produccion |
| **Conocimiento compartido** | Todo el equipo sabe como funciona el codigo |
| **Consistencia** | El codigo mantiene un estandar uniforme |
| **Aprendizaje mutuo** | Tanto autor como revisor aprenden algo nuevo |
| **Documentation viva** | El review documenta por que se tomaron decisiones |

## La Mentalidad del Revisor

Hay tres mentalidades, y solo una es la correcta:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MENTALIDADES DEL REVISOR                     │
├──────────────────┬──────────────────┬───────────────────────────┤
│   GATEKEEPER     │   BUG HUNTER     │   COLABORADOR             │
│                  │                  │                           │
│   "Bloqueo todo  │   "Busco el bug  │   "Ayudo a mejorar el     │
│   que no me      │   que tu         │   codigo y aprendo         │
│   gusta"         │   escondiste"    │   contigo"                 │
│                  │                  │                           │
│   ❌ Toxic       │   ⚠️ Limitado   │   ✅ Correcto             │
└──────────────────┴──────────────────┴───────────────────────────┘
```

**El gatekeeper** bloquea PRs por preferencias personales. "No me gusta como nombraste
esta variable" sin razon tecnica. **Evita ser esto.**

**El bug hunter** solo busca errores logicos. Ignora readability, performance, y
arquitectura. Es util pero incompleto.

**El colaborador** busca mejorar el codigo *y* compartir conocimiento. Explica *por que*
algo deberia cambiar, no solo *que* cambiar.

## Code Review Checklist

Usa esta checklist cuando revises un PR:

### Correctitud

| Item | Pregunta | Critico |
|------|----------|---------|
| Logica | ¿El codigo hace lo que dice el PR description? | ✅ |
| Edge cases | ¿Maneja null, listas vacias, valores extremos? | ✅ |
| Error handling | ¿Los errores se manejan y comunican correctamente? | ✅ |
|回归 | ¿Este cambio rompe funcionalidad existente? | ✅ |

### Tests

| Item | Pregunta | Critico |
|------|----------|---------|
| Existencia | ¿Hay tests para el nuevo codigo? | ✅ |
| Cobertura | ¿Los tests cubren los edge cases? | ✅ |
| Claridad | ¿Los tests son legibles y tienen nombres descriptivos? | ⚠️ |
| Aislamiento | ¿Los tests son independientes entre si? | ⚠️ |

### Seguridad

| Item | Pregunta | Critico |
|------|----------|---------|
| Input validation | ¿Se valida toda la entrada del usuario? | ✅ |
| SQL injection | ¿Se usan queries parametrizadas? | ✅ |
| Secrets | ¿No hay API keys hardcodeadas? | ✅ |
| Auth | ¿Se verifican permisos en el backend? | ✅ |
| Sensitive data | ¿Los logs no exponen datos sensibles? | ✅ |

### Performance

| Item | Pregunta | Critico |
|------|----------|---------|
| Rebuilds innecesarios | ¿Evita rebuilds de widgets que no cambian? | ⚠️ |
| Queries N+1 | ¿Se evitan consultas repetitivas a la DB? | ✅ |
| Memoria | ¿Se liberan suscripciones y controladores? | ⚠️ |
| Imagenes | ¿Se cachean y redimensionan correctamente? | ⚠️ |

### Readabilidad

| Item | Pregunta | Critico |
|------|----------|---------|
| Nombres | ¿Variables y funciones tienen nombres descriptivos? | ⚠️ |
| Funciones cortas | ¿Cada funcion hace una sola cosa? | ⚠️ |
| Comments | ¿Los comments explican el *por que*, no el *que*? | ⚠️ |
| DRY | ¿Se evita duplicacion de codigo? | ⚠️ |

### Arquitectura

| Item | Pregunta | Critico |
|------|----------|---------|
| Separation of concerns | ¿Cumple con Clean Architecture? | ✅ |
| Dependencies | ¿Las dependencias apuntan hacia adentro? | ✅ |
| Naming | ¿Los nombres siguen las convenciones del proyecto? | ⚠️ |
| File structure | ¿Los archivos estan en la carpeta correcta? | ⚠️ |

## Como Dar Feedback Constructivo

### Metodo Sandwich (Basico)

```
┌─────────────────────────────────────────────────┐
│              METODO SANDWICH                    │
│                                                 │
│  1. Algo POSITIVO sobre el codigo               │
│     "Buena implementacion del BLoC"             │
│                                                 │
│  2. Algo que MEJORAR (el relleno)               │
│     "Pero el handler de errores necesita        │
│      manejar el caso de timeout"                │
│                                                 │
│  3. Algo POSITIVO o motivador                   │
│     "Con eso, este modulo queda muy solido"     │
└─────────────────────────────────────────────────┘
```

> **Cuidado:** El sandwich puede sonar condescendiente si lo usas mal. Usa el modelo
> SBI para feedback mas especifico y profesional.

### Modelo SBI (Situacion-Behavior-Impact)

El modelo **SBI** es la forma mas efectiva de dar feedback:

| Componente | Que es | Ejemplo |
|-----------|--------|---------|
| **S**ituacion | Donde/when paso | "En el PR #247, en el archivo `auth_bloc.dart`" |
| **B**ehavior | Que paso (hechos, no juicios) | "El timeout no se maneja, si el server tarda mas de 30s la app se queda colgada" |
| **I**mpact | Cual es la consecuencia | "El usuario ve una pantalla blanca y no sabe que paso. Podemos perder usuarios" |

### Ejemplo completo con SBI

```
┌──────────────────────────────────────────────────────────────────┐
│  SITUATION: "En auth_bloc.dart, linea 45"                        │
│                                                                  │
│  BEHAVIOR: "Cuando el login falla, solo se hace throw de        │
│  la excepcion sin manejar. No hay catch block para               │
│  SocketException ni TimeoutException."                           │
│                                                                  │
│  IMPACT: "Si el usuario no tiene internet, la app crashea.      │
│  Necesitamos manejar estos errores y mostrar un mensaje          │
│  amigable al usuario."                                           │
│                                                                  │
│  SUGERENCIA: "Podemos usar el pattern matching de Dart para     │
│  manejar cada tipo de excepcion por separado, o usar el         │
│  wrapper que ya tenemos en lib/core/errors/."                   │
└──────────────────────────────────────────────────────────────────┘
```

## Malos vs Buenos Ejemplos de Review

### Mal review ❌

```
"This is wrong. Fix it."
```

**Problemas:** No explica que esta mal, no sugiere como arreglarlo, no es constructivo.

```
"Variable names are bad. Also why no comments?"
```

**Problemas:** Generico, no especifica que nombres ni por que, los comments no siempre
son necesarios.

### Buen review ✅

```
"En la linea 23, `data` podria llamarse `userProfile` para que sea mas claro
que tipo de datos contiene. Esto ayuda a otros developers a entender el codigo
sin tener que leer la implementacion.

Sugerencia:
- data -> userProfile
- En la linea 45, agregar un comment explicando por que usamos este cache strategy
```

```
"Funcion correcta, pero si `users` viene vacio del backend, vamos a tener
un problema en la linea 67. Podemos agregar un check:

if (users.isEmpty) {
  emit(EmptyState());
  return;
}

Esto evita el crash y le da feedback al usuario."
```

## Como Recibir Feedback sin Ego

Tu codigo no eres tu. Repetelo hasta que te lo creas.

### Reglas para recibir feedback

| Hacer | No hacer |
|-------|----------|
| Decir "gracias por el detalle" | Decir "eso funciona bien asi" |
| Preguntar "por que sugieres eso?" | Ignorar el comment |
| Implementar el cambio si tiene sentido | Defender tu codigo a toda costa |
| Proponer una alternativa si no estas de acuerdo | Hacer merge sin responder comments |
| Pedir claridad si el comment es ambiguo | Tomar feedback personalmente |

### Cuando el feedback es subjetivo

```
┌─────────────────────────────────────────────────────────────────┐
│  RESPUESTA CUANDO NO ESTAS DE ACUERDO:                          │
│                                                                 │
│  "Entiendo tu punto sobre [tema]. Mi razon para hacerlo         │
│  asi fue [razon tecnica]. Que te parece si [alternativa]?       │
│  Quiero que el codigo sea mejor para el equipo."                │
└─────────────────────────────────────────────────────────────────┘
```

## Metricas de Code Review

Que medir y por que:

| Metrica | Target | Por que importa |
|---------|--------|----------------|
| **Tiempo de review** | < 4 horas | Un PR esperando mucho tiempo bloquea al autor |
| **Tamaño del PR** | < 400 lineas | PRs grandes son imposibles de revisar bien |
| **Approval rate** | > 80% first pass | Si siempre pides cambios, hay un problema de proceso |
| **Review comments** | 2-5 por PR | Menos de 2 = no estas revisando, mas de 5 = PR muy grande |
| **Tiempo de ciclo** | < 24 horas | De PR abierto a merge |

### Como medir en GitHub

```
# Ver tiempo de review de un PR
# En la UI de GitHub: PR -> Activity -> timeline

# Usando GitHub CLI
gh pr view 123 --json reviews,createdAt,mergedAt

# Calcular tiempo promedio
gh pr list --state merged --json reviews,createdAt,mergedAt \
  --jq '.[] | (.mergedAt | fromdateiso8601) - (.createdAt | fromdateiso8601)'
```

## Async vs Sync Reviews

| Caracteristica | Async Review | Sync Review (Live) |
|---------------|-------------|-------------------|
| **Cuando usar** | PRs standard, < 400 LOC | PRs complejos, arquitectura |
| **Velocidad** | Mas lento pero flexible | Mas rapido, resolucion inmediata |
| **Documentacion** | Queda un registro permanente | Se pierde contexto |
| **Horarios** | Funciona con equipos remotos | Requiere overlap horario |
| **Profundidad** | Review mas cuidadoso | Review mas conversacional |
| **Herramienta** | GitHub PR comments | VS Code Live Share, Tuple |

```
┌─────────────────────────────────────────────────────────────────┐
│           DECISION: ASYNC O SYNC?                               │
│                                                                 │
│  ¿El PR tiene > 400 lineas?          → Sync                    │
│  ¿Es un cambio de arquitectura?      → Sync                    │
│  ¿El autor es junior?                → Sync (para mentorear)   │
│  ¿Es un bugfix pequeno?              → Async                   │
│  ¿El autor es senior y confiable?    → Async                   │
│  ¿Hay desacuerdo tecnico?            → Sync (para discutir)    │
└─────────────────────────────────────────────────────────────────┘
```

## Herramientas para Code Reviews en GitHub

### Review assignments automaticos

Usa **CODEOWNERS** para asignar reviews automaticamente:

```
# .github/CODEOWNERS

# El equipo de auth revisa cambios en auth/
lib/features/auth/        @mi-equipo/flutter-auth

# Los seniors revisan cambios en core/
lib/core/                 @senior-dev-1 @senior-dev-2

# Nadie deberia cambiar esto sin aprobacion especial
lib/core/env/             @tech-lead
```

### Configurar branch protection

```
Settings → Branches → Add rule para "main"

✅ Require pull request reviews before merging
   → Required approving reviews: 1
✅ Require status checks to pass
   → Required: build, test
✅ Require branches to be up to date
✅ Require conversation resolution
```

### Labels para PRs

| Label | Significado |
|-------|-------------|
| `needs-review` | Esperando review |
| `changes-requested` | El autor necesita hacer cambios |
| `approved` | Listo para merge |
| `wip` | Work in progress, no revisar aun |
| `urgent` | Requiere atencion prioritaria |

## Resumen

```
┌─────────────────────────────────────────────────────────────────┐
│              CODE REVIEW: RESUMEN EJECUTIVO                     │
│                                                                 │
│  ✅ Sé COLABORADOR, no gatekeeper                              │
│  ✅ Usa el modelo SBI para feedback especifico                 │
│  ✅ Revisa por: Correctitud > Security > Performance > Style   │
│  ✅ Mantén PRs < 400 lineas                                    │
│  ✅ Responde en < 4 horas                                      │
│  ✅ Recibe feedback sin ego                                    │
│  ✅ Usa CODEOWNERS para asignacion automatica                  │
│  ✅ Mide y mejora tus metricas de review                       │
└─────────────────────────────────────────────────────────────────┘
```
