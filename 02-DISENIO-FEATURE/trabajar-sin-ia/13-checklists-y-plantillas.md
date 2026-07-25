# Checklists y Plantillas

> Herramientas reutilizables para cada fase del framework. Copia, pega y adapta a tu feature.

---

## 1. Plantilla de documentación de feature

```markdown
# Feature: [Nombre]

## User Story
**Como** [actor], **quiero** [acción], **para** [beneficio].

## Contexto
- Proyecto: [nombre]
- Módulos relacionados: [lista]
- Dependencias nuevas: [lista]

## Complejidad estimada: [Simple/Intermedia/Compleja]

## Tiempo estimado: [horas]

---

## FASE 1: Investigación

### Herramientas a usar
- [ ] Documentación oficial: [URL]
- [ ] GitHub repo: [URL]
- [ ] pub.dev: [URL]
- [ ] Otros: [URL]

### Lo que aprendí
[Notas de investigación]

### Preguntas sin resolver
- [ ] [Pregunta 1]
- [ ] [Pregunta 2]

---

## FASE 2: Diseño

### Descomposición (FADER)
| Pieza | Capa | Responsabilidad |
|-------|------|-----------------|
| | | |

### Contratos (interfaces)
```dart
// Interfaces aquí
```

### Flujo de datos
```
// Diagrama aquí
```

### Estados
```dart
// Estados aquí
```

### Excepciones
| Excepción | Cuándo | Qué hacer |
|-----------|--------|-----------|
| | | |

---

## FASE 3: Implementación

### Orden de implementación
1. [ ]
2. [ ]
3. [ ]

### Notas de implementación
[Decisiones tomadas durante la implementación]

---

## FASE 4: Verificación

### Tests escritos
- [ ] Test 1: [descripción]
- [ ] Test 2: [descripción]

### Prueba manual
- [ ] Happy path funciona
- [ ] Error path funciona
- [ ] Edge cases manejados

---

## FASE 5: Refactor

### Verificaciones
- [ ] Nombres claros
- [ ] Sin código duplicado
- [ ] Responsabilidades separadas
- [ ] Tests siguen pasando

---

## FASE 6: Validación con IA

### Prompt utilizado
[Prompt que le diste a IA]

### Feedback recibido
[Resumen del feedback]

### Cambios implementados
- [ ] Cambio 1
- [ ] Cambio 2

### Cambios ignorados (y por qué)
- [ ] Cambio ignorado: [razón]

---

## Tiempo real
| Fase | Estimado | Real |
|------|----------|------|
| Investigar | | |
| Diseñar | | |
| Implementar | | |
| Verificar | | |
| Refactor | | |
| Validar | | |
| **Total** | | |
```

---

## 2. Checklist de investigación

```markdown
## Investigación: [Feature]

### Documentación oficial
- [ ] Busqué la documentación oficial del servicio/paquete
- [ ] Leí el README completo
- [ ] Revisé ejemplos de uso
- [ ] Entendí las limitaciones

### GitHub
- [ ] Revisé issues abiertas
- [ ] Revisé issues cerradas relevantes
- [ ] Busqué en el código fuente
- [ ] Verifiqué la fecha del último commit

### Dependencias
- [ ] Identifiqué todas las dependencias nuevas
- [ ] Verifiqué que son confiables (likes, pub points)
- [ ] Verifiqué compatibilidad con mi versión de Flutter
- [ ] Revisé changelog por breaking changes

### Proyecto actual
- [ ] Busqué features similares en el proyecto
- [ ] Revisé patrones existentes
- [ ] Identifiqué dónde encaja la nueva feature

### User Story
- [ ] Definí el actor principal
- [ ] Definí la acción claramente
- [ ] Definí el beneficio/valor
- [ ] Listé criterios de aceptación
```

---

## 3. Checklist de diseño

```markdown
## Diseño: [Feature]

### FADER
- [ ] **F**ormular: User Story definida
- [ ] **A**ctorizar: Actores identificados
- [ ] **D**escomponer: Operaciones atómicas listadas
- [ ] **E**ntidades: Modelos del negocio definidos
- [ ] **R**eglas: Reglas de negocio documentadas

### Clean Architecture
- [ ] Domain: Entidades definidas
- [ ] Domain: Contratos (interfaces) definidos
- [ ] Domain: Use cases listados
- [ ] Data: Modelos de datos definidos
- [ ] Data: Implementación de contratos planeada
- [ ] Presentation: Controllers/BLoC definidos
- [ ] Presentation: Pantallas listadas

### Contratos
- [ ] Cada use case tiene su contrato
- [ ] Los contratos usan Either para errores
- [ ] Los contratos son testables

### Estados
- [ ] Estados principales definidos
- [ ] Transiciones documentadas
- [ ] Estados de carga y error manejados

### Excepciones
- [ ] Excepciones de negocio definidas
- [ ] Excepciones de infraestructura listadas
- [ ] Estrategia de manejo definida para cada una
```

---

## 4. Checklist de implementación

```markdown
## Implementación: [Feature]

### Orden
- [ ] 1. Dominio: Entidades
- [ ] 2. Dominio: Contratos
- [ ] 3. Dominio: Use cases
- [ ] 4. Data: Modelos
- [ ] 5. Data: Implementación repositorios
- [ ] 6. Presentation: Controllers
- [ ] 7. Presentation: UI

### Por cada pieza
- [ ] Compila sin errores
- [ ] Funciona individualmente
- [ ] Tiene sentido con el diseño
- [ ] Los nombres son claros

### Reglas
- [ ] No escribí código que no entiendo
- [ ] Me detuve cuando me confundí
- [ ] Documenté decisiones importantes
- [ ] Cada pieza es testeable
```

---

## 5. Checklist de verificación

```markdown
## Verificación: [Feature]

### Tests unitarios
- [ ] Test para cada use case
- [ ] Test para edge cases (vacío, límites)
- [ ] Test para errores (fallo de red, datos inválidos)
- [ ] Todos los tests pasan

### Prueba manual
- [ ] Happy path: todo funciona como se espera
- [ ] Error path: errores se manejan correctamente
- [ ] Edge cases: vacío, límites, formatos raros
- [ ] Navegación: la feature encaja en el flujo
- [ ] Loading states: se muestran correctamente
- [ ] Offline: funciona sin conexión (si aplica)

### Calidad
- [ ] No hay errores en consola
- [ ] No hay warnings importantes
- [ ] El rendimiento es aceptable
- [ ] No hay memory leaks evidentes
```

---

## 6. Checklist de refactorización

```markdown
## Refactor: [Feature]

### Nombres
- [ ] Clases son descriptivas
- [ ] Métodos dicen qué hacen
- [ ] Variables tienen sentido
- [ ] Constantes están bien nombradas

### Estructura
- [ ] Cada clase tiene una responsabilidad
- [ ] No hay código duplicado
- [ ] No hay dependencias circulares
- [ ] Las capas están separadas

### Calidad
- [ ] El código es legible
- [ ] Los comentarios explican POR QUÉ, no QUÉ
- [ ] No hay código muerto
- [ ] Los imports son necesarios

### Tests
- [ ] Todos los tests siguen pasando
- [ ] Los tests cubren los casos principales
```

---

## 7. Checklist de validación con IA

```markdown
## Validación con IA: [Feature]

### Antes de preguntar a IA
- [ ] Ya implementé la feature completamente
- [ ] Ya verifiqué con tests
- [ ] Ya refactoricé
- [ ] Tengo un prompt claro y específico

### El prompt
> [Tu prompt aquí]

### Evaluación del feedback
Para cada punto de feedback de IA:
- [ ] ¿Entiendo qué está sugiriendo?
- [ ] ¿Tiene razón?
- [ ] ¿Es accionable?
- [ ] ¿Lo implemento?

### Después de la validación
- [ ] Revisé cada sugerencia críticamente
- [ ] Implementé lo que tiene sentido
- [ ] Ignoré lo que no entiendo
- [ ] Ejecuté tests después de cambios
- [ ] Puedo explicar cada cambio que hice
```

---

## 8. Plantilla de User Story

```markdown
## Feature: [Nombre]

**Como** [actor específico],
**quiero** [acción específica],
**para** [beneficio/valor específico].

### Criterios de aceptación
- [ ] [Criterio 1: debe ser específico y medible]
- [ ] [Criterio 2]
- [ ] [Criterio 3]

### Restricciones
- [Restricción 1]
- [Restricción 2]

### Dependencias
- [Dependencia 1]
- [Dependencia 2]

### Complejidad estimada: [Simple/Intermedia/Compleja]
### Tiempo estimado: [horas]
```

---

## 9. Plantilla de prompt para Fase 6

### Para CRUD simple
```
Revisa mi implementación de [feature] con [servicio].
¿El manejo de errores está completo? ¿Falta algún caso edge?
¿Los nombres son claros? NO reescribas el código, solo dame feedback.
```

### Para feature con estados
```
Revisa mi máquina de estados para [feature].
¿Todas las transiciones son válidas? ¿Hay estados inalcanzables?
¿Manejo correctamente los estados de carga y error?
NO reescribas el código, solo dame feedback.
```

### Para feature con tiempo real
```
Revisa mi implementación de streams para [feature].
¿El manejo de suscripciones es correcto? ¿Evito memory leaks?
¿Cómo manejo la reconexión? NO reescribas el código, solo dame feedback.
```

### Para feature con API externa
```
Revisa mi integración con [servicio].
¿El manejo de errores de red es completo? ¿Retry automático?
¿Timeouts configurados? NO reescribas el código, solo dame feedback.
```

### Genérico
```
Revisa esta implementación como si fueras un senior revisando un PR.
Dame 3 cosas que están bien y 3 cosas que mejorar.
NO reescribas nada. Sé específico y accionable.
```

---

## 10. Plantilla de métricas personales

```markdown
## Métricas: [Nombre Feature]

### Tiempo
| Fase | Estimado | Real | Diferencia |
|------|----------|------|------------|
| Investigar | | | |
| Diseñar | | | |
| Implementar | | | |
| Verificar | | | |
| Refactor | | | |
| Validar | | | |
| **Total** | | | |

### Confianza (1-10)
- Antes de empezar: ___
- Después de completar: ___

### Cosas que aprendí
1. 
2. 
3. 

### Errores que cometí
1. 
2. 
3. 

### IA usada (solo Fase 6)
- Para qué: 
- Fue útil: Sí/No
- Puedo explicar los cambios: Sí/No

### Fecha de inicio: 
### Fecha de fin: 
```

---

**Siguiente:** [14-recursos-externos.md](./14-recursos-externos.md) — Dónde encontrar ayuda sin depender de IA
