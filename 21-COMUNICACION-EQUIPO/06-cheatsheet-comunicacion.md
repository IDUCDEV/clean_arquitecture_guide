# 06: Cheatsheet de Comunicacion

## PR Description Template

```markdown
## Descripcion
[1-2 oraciones sobre que hace este PR y por que]

## Tipo de cambio
- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] ♻️ Code refactor (no functional changes)
- [ ] 🧪 Tests (adding or updating tests)
- [ ] 🔧 Chore (build, CI, dependencies)

## Cambios principales
- [Cambio 1: que se hizo y por que]
- [Cambio 2: que se hizo y por que]
- [Cambio 3: que se hizo y por que]

## Checklist
- [ ] Mi codigo sigue las convenciones del proyecto
- [ ] He realizado self-review del codigo
- [ ] He agregado tests que prueban mis cambios
- [ ] Los tests existentes pasan correctamente
- [ ] No agrego warnings nuevas (`flutter analyze` limpio)
- [ ] La documentacion esta actualizada (si aplica)
- [ ] No dependo de cambios de otros PRs pendientes

## Screenshots/Videos
[Si hay cambios de UI, incluir antes/despues]

## Contexto adicional
[Cualquier otra cosa que el reviewer deba saber]

## Related Issues
Closes #123
```

## Code Review Checklist Template

```markdown
## Code Review: PR #XXX

### Correctitud
- [ ] El codigo hace lo que dice el PR description
- [ ] Los edge cases estan manejados
- [ ] El error handling es apropiado
- [ ] No rompe funcionalidad existente

### Tests
- [ ] Hay tests para el nuevo codigo
- [ ] Los tests cubren edge cases
- [ ] Los tests son legibles y tienen nombres descriptivos
- [ ] Los tests son independientes

### Seguridad
- [ ] No hay API keys hardcodeadas
- [ ] Se valida la entrada del usuario
- [ ] Se usan queries parametrizadas
- [ ] Los logs no exponen datos sensibles
- [ ] Se verifican permisos en el backend

### Performance
- [ ] No hay rebuilds innecesarios de widgets
- [ ] Se evitan queries N+1
- [ ] Se liberan suscripciones y controladores
- [ ] Las imagenes se cachean correctamente

### Readabilidad
- [ ] Variables y funciones tienen nombres descriptivos
- [ ] Las funciones hacen una sola cosa
- [ ] Los comments explican el "por que", no el "que"
- [ ] No hay codigo duplicado (DRY)

### Arquitectura
- [ ] Cumple con Clean Architecture
- [ ] Las dependencias apuntan hacia adentro
- [ ] Los nombres siguen las convenciones del proyecto
- [ ] Los archivos estan en la carpeta correcta
```

## ADR Template

```markdown
# ADR-XXX: [Titulo de la Decision]

## Estado
[Aprobado | Propuesto | Deprecated | Superseded por ADR-YYY]
Fecha: [YYYY-MM-DD]

## Contexto
[Que situacion o problema nos lleva a tomar esta decision?
Que restricciones tenemos? Que factores son relevantes?]

## Decision
[Que decidimos hacer? Seja especifico y claro.]

## Alternativas Consideradas

| # | Alternativa | Pros | Contras |
|---|-------------|------|---------|
| 1 | [Nombre] | [Ventajas] | [Desventajas] |
| 2 | [Nombre] | [Ventajas] | [Desventajas] |
| 3 | [Nombre] | [Ventajas] | [Desventajas] |

## Justificacion
[Por que elegimos esta alternativa sobre las otras?]

## Consecuencias
### Positivas
- [Consecuencia positiva 1]
- [Consecuencia positiva 2]

### Negativas
- [Consecuencia negativa 1]
- [Consecuencia negativa 2]

### Neutrales
- [Cosas que cambian pero no son ni buenas ni malas]

## Referencias
- [Link 1]
- [Link 2]
```

## Incident Report Template

```markdown
# Incident Report: [Titulo]

**Severidad:** [P0-Critico | P1-Alto | P2-Medio | Bajo]
**Estado:** [Investigando | Mitigado | Resuelto | Post-mortem]
**Responsable:** [Nombre]
**Fecha:** [YYYY-MM-DD HH:MM UTC]

## Resumen
[1-2 oraciones sobre que paso]

## Timeline (UTC)
| Hora | Evento |
|------|--------|
| HH:MM | [Primer reporte del incidente] |
| HH:MM | [Accion tomada 1] |
| HH:MM | [Accion tomada 2] |
| HH:MM | [Resuelto o mitigado] |

## Impacto
- **Usuarios afectados:** [Numero o estimacion]
- **Features afectadas:** [Lista]
- **Duracion total:** [Tiempo]
- **Datos perdidos:** [Si/No, cuales]

## Root Cause
[Causa raiz del problema. No describas sintomas — describe la causa.]

## Que funciono bien
[Que del sistema de monitoreo, alertas, o proceso ayudo]

## Que mejorar
| # | Mejora | Responsable | Fecha target |
|---|--------|-------------|-------------|
| 1 | [Mejora] | [Persona] | [Fecha] |
| 2 | [Mejora] | [Persona] | [Fecha] |

## Lecciones aprendidas
- [Leccion 1]
- [Leccion 2]
```

## Handoff Checklist: Disenador → Developer

```
┌─────────────────────────────────────────────────────────────────┐
│  HANDOFF CHECKLIST: DISEÑADOR → DEVELOPER                       │
│                                                                 │
│  DISEÑO                                                         │
│  [ ] Mockups completos para todas las pantallas                 │
│  [ ] Estados: default, loading, empty, error                    │
│  [ ] Responsive: mobile + tablet (si aplica)                    │
│  [ ] Dark mode (si aplica)                                      │
│                                                                 │
│  COMPONENTES                                                    │
│  [ ] Componentes en el design system                            │
│  [ ] Variantes de cada componente                               │
│  [ ] Estados de interaccion (hover, pressed, disabled)          │
│                                                                 │
│  ASSETS                                                         │
│  [ ] Iconos exportados en SVG/PNG                               │
│  [ ] Imagenes en PNG @2x                                        │
│  [ ] Ilustraciones en PNG @2x o Lottie                         │
│  [ ] Animaciones documentadas (duracion, curve)                │
│                                                                 │
│  ESPECIFICACIONES                                               │
│  [ ] Spacing: paddings, margins, gaps                           │
│  [ ] Colores: hex codes, tokens                                │
│  [ ] Tipografia: font family, sizes, weights                   │
│  [ ] Border radius, shadows, opacities                         │
│  [ ] Touch targets minimo 44x44px                              │
│                                                                 │
│  ACCESIBILIDAD                                                  │
│  [ ] Contraste minimo WCAG AA (4.5:1 texto, 3:1 grafico)      │
│  [ ] Labels para iconos interactivos                           │
│  [ ] Orden de lectura logico                                   │
│                                                                 │
│  FLUJOS                                                         │
│  [ ] User flows documentados                                   │
│  [ ] Transiciones entre pantallas                              │
│  [ ] Navegacion back/forward                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Glosario: Terminos de Diseno vs Desarrollo

| Disenador dice | Developer entiende | Equivalente Flutter |
|---------------|-------------------|-------------------|
| **Frame** | Contenedor | `Container`, `SizedBox` |
| **Auto Layout** | Layout flexbox | `Row`, `Column`, `Flex` |
| **Component** | Widget reutilizable | `StatelessWidget` |
| **Instance** | Widget instance | Widget constructor |
| **Variant** | Parametros del widget | Named parameters |
| **Boolean property** | Flag | `bool` parameter |
| **Text property** | String param | `String` parameter |
| **Padding** | Espacio interno | `EdgeInsets` |
| **Margin** | Espacio externo | `Padding` outside |
| **Shadow** | Sombra | `BoxShadow` |
| **Border radius** | Esquinas redondeadas | `BorderRadius` |
| **Fill** | Color de fondo | `color` property |
| **Stroke** | Borde | `Border` |
| **Opacity** | Transparencia | `opacity` property |
| **Overlay** | Capa superpuesta | `Stack` + `Positioned` |
| **Scroll** | Contenido desplazable | `ListView`, `ScrollView` |
| **State** | Estado del componente | `StatefulWidget` state |
| **Prototype** | Interactividad | `GestureDetector` |
| **Asset** | Recurso grafico | `Image.asset()` |
| **Token** | Variable de diseno | Constante de tema |

## Formulas de Feedback

### Modelo SBI (Situacion-Behavior-Impact)

```
┌─────────────────────────────────────────────────────────────────┐
│  SBI: Feedback especifico y constructivo                       │
│                                                                 │
│  S = SITUACION: Donde y cuando ocurrio                          │
│  "En el PR #247, en auth_bloc.dart linea 45"                   │
│                                                                 │
│  B = BEHAVIOR: Que paso (hechos, no juicios)                    │
│  "El timeout no se maneja, la app se queda colgada"            │
│                                                                 │
│  I = IMPACT: Cual es la consecuencia                            │
│  "El usuario ve pantalla blanca y puede abandonar la app"      │
│                                                                 │
│  + SUGERENCIA: (opcional pero recomendado)                      │
│  "Podemos usar try-catch con SocketException y                 │
│   TimeoutException por separado"                                │
└─────────────────────────────────────────────────────────────────┘
```

### Metodo Sandwich

```
┌─────────────────────────────────────────────────────────────────┐
│  SANDWICH: Feedback positivo → Mejora → Positivo               │
│                                                                 │
│  1. POSITIVO: "La estructura del BLoC esta muy bien organizada"│
│                                                                 │
│  2. MEJORA: "Pero falta manejar el estado de error en          │
│     el evento LoginRequested. Necesitamos un                 │
│     handler para SocketException"                               │
│                                                                 │
│  3. POSITIVO: "Con eso, este modulo queda solido para          │
│     production"                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Socratic Questioning (Preguntas Socraticas)

En vez de decir que esta mal, haz preguntas que guien al otro a la respuesta:

| Pregunta | Ejemplo |
|----------|---------|
| "Que pasa si...?" | "Que pasa si el usuario no tiene internet?" |
| "Como manejas...?" | "Como manejas el caso donde el token expira?" |
| "Que alternativas hay?" | "Que alternativas hay a esta animacion?" |
| "Por que elegiste...?" | "Por que elegiste Provider en vez de BLoC?" |
| "Que trade-offs tiene...?" | "Que trade-offs tiene esta arquitectura?" |

## Git Branch Naming Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│  BRANCH NAMING: PREFIJO/DESCRIPCION-KEBAB-CASE                 │
│                                                                 │
│  feature/    → Nueva funcionalidad                              │
│  bugfix/     → Bug en develop                                  │
│  hotfix/     → Bug critico en produccion                       │
│  release/    → Preparar release                                │
│  chore/      → Mantenimiento, config, deps                     │
│  refactor/   → Refactorizar sin cambiar comportamiento         │
│  docs/       → Solo documentacion                              │
│  test/       → Agregar o mejorar tests                         │
│                                                                 │
│  EJEMPLOS:                                                      │
│  ✅ feature/google-sign-in                                      │
│  ✅ bugfix/null-pointer-home-list                               │
│  ✅ hotfix/payment-crash-ios-17                                 │
│  ✅ chore/update-flutter-3.19                                   │
│  ❌ feature/GoogleSignIn (CamelCase)                            │
│  ❌ feature/fix (muy vago)                                      │
│  ❌ feature/add-google-sign-in-to-login-screen (muy largo)     │
└─────────────────────────────────────────────────────────────────┘
```

## Meeting Etiquette Quick Reference

```
┌─────────────────────────────────────────────────────────────────┐
│  MEETING ETIQUETTE: REGLAS DE ORO                               │
│                                                                 │
│  ANTES DE LA REUNION:                                           │
│  [ ] Tener agenda clara                                        │
│  [ ] Enviar docs de contexto con anticipacion                  │
│  [ ] Solo invitar a quien realmente necesita estar             │
│  [ ] Tener un "decision maker" identificado                    │
│                                                                 │
│  DURANTE LA REUNION:                                            │
│  [ ] Empezar a la hora (no esperar 5 min)                      │
│  [ ] Asignar a alguien que tome notas                          │
│  [ ] Mantener discusion enfocada en el tema                    │
│  [ ] Si se desvia, crear "parking lot" para temas later        │
│  [ ] No hacer multitask (cerrar Slack, email)                  │
│  [ ] Respetar el tiempo: terminar 5 min antes                  │
│                                                                 │
│  DESPUES DE LA REUNION:                                         │
│  [ ] Enviar notas y action items en < 1 hora                   │
│  [ ] Asignar responsables y fechas a cada action item          │
│  [ ] Seguimiento en el proximo standup                          │
│                                                                 │
│  TIPOS DE REUNION Y DURACION MAXIMA:                            │
│  Daily standup:           15 minutos                            │
│  Sprint planning:         1-2 horas                             │
│  Retrospective:           1 hora                                │
│  Technical discussion:    30-45 minutos                         │
│  1:1:                     30 minutos                            │
│  Brainstorming:           45-60 minutos                         │
└─────────────────────────────────────────────────────────────────┘
```
