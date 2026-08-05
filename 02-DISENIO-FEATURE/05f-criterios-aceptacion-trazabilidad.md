# Criterios de Aceptación y Matriz de Trazabilidad

> Convierte el diseño en pruebas verificables. Los criterios de aceptación dicen *qué significa que la feature funcione*; la matriz de trazabilidad garantiza que *nada se quedó sin implementar ni sin probar*.

---

## Parte 1: Criterios de Aceptación

FADER explica bien el problema, pero una regla escrita como texto puede interpretarse distinto. Los criterios de aceptación lo convierten en **escenarios verificables**.

### Formato BDD

```
CA01:
Dado que [contexto inicial],
cuando [acción del actor],
entonces [resultado esperado].
```

### Ejemplo: Buyers

```
CA01:
Dado que soy organizador,
cuando abro Buyers,
entonces veo los últimos 30 compradores.

CA02:
Dado que un ticket está aprobado,
cuando intento liberarlo,
entonces la operación es rechazada.

CA03:
Dado que selecciono algunos tickets,
cuando confirmo la aprobación,
entonces los seleccionados se aprueban
y los demás se liberan.
```

### Cómo escribirlos

| Regla | Ejemplo |
|-------|---------|
| Un criterio = un escenario | No mezcles dos "entonces" independientes |
| Sé concreto y medible | "últimos 30" en vez de "los recientes" |
| Cubre el borde | Estado vacío, límite, formato inválido |
| Cubre el error | Qué pasa cuando la operación se rechaza |
| Referencia la regla que valida | CA02 ↔ RN005 "no re-aprobar" |

### ¿Cuántos criterios por feature?

| Tamaño de feature | Criterios típicos |
|-------------------|-------------------|
| Hotfix (1-2 ops) | 1-3 |
| Pequeña (3-6 ops) | 3-6 |
| Mediana (7-15 ops) | 8-15 |
| Grande (16-30 ops) | 15-25 |

**Regla práctica:** cada operación atómica de FADER debería tener al menos un criterio de happy path y uno de error.

### De criterio a test

```
CA03 (aprobar y liberar) →
  Test unitario del UseCase ApproveTickets
  Test de integración del RPC approve_and_release_tickets
  Widget test: botón de confirmar solo se habilita con selección
```

---

## Parte 2: Matriz de Trazabilidad

La matriz conecta el diseño de punta a punta:

```
Operación → UseCase → Regla → Contrato → Test
```

### Ejemplo: Buyers

| Operación | UseCase | Regla | Contrato | Test |
|-----------|---------|-------|----------|------|
| Aprobar tickets | `ApproveTickets` | RN004, RN005, RN008 | `approveTickets()` | Unit + integration |
| Liberar tickets | `ReleaseTickets` | RN004, RN006 | `releaseTickets()` | Unit + integration |
| Listar compradores | `GetBuyers` | RS001, RT001 | `getBuyers()` | Unit + widget |

### Qué verifica la matriz

1. **Ninguna operación quedó sin implementación.** Toda fila de FADER tiene su UseCase.
2. **Ninguna regla quedó sin prueba.** Toda regla aparece en alguna fila con test.
3. **Ningún contrato quedó huérfano.** Cada contrato se usa desde al menos un UseCase.
4. **Los criterios de aceptación tienen respaldo.** CA03 se cumple por la fila "Aprobar tickets".

### Lectura cruzada

```
[ ] Cada operación de FADER está en la matriz
[ ] Cada regla RN/RT/RS está en la matriz
[ ] Cada contrato definido en 03-contratos-primero.md está en la matriz
[ ] Cada criterio de aceptación (CA) tiene una fila que lo respalda
[ ] Cada fila tiene un tipo de test asignado
```

---

## Plantillas

### Plantilla de criterios de aceptación

```markdown
## Criterios de aceptación

CA01:
Dado que [contexto],
cuando [acción],
entonces [resultado].

CA02:
Dado que [contexto],
cuando [acción],
entonces [resultado].
```

### Plantilla de matriz de trazabilidad

```markdown
| Operación | UseCase | Regla | Contrato | Test |
|-----------|---------|-------|----------|------|
| [op de FADER] | [UseCase] | [RN/RT/RS] | [método] | Unit/integration |
```

---

## Errores comunes

| Error | Síntoma | Solución |
|-------|---------|----------|
| Criterios vagos | "debe funcionar bien" | Escribe resultado medible |
| Un CA con 3 "entonces" | Escenario imposible de testear | Divide en CAs separados |
| Matriz incompleta | Reglas sin UseCase o UseCase sin test | Corre la lectura cruzada |
| Criterios sin regla | El test no sabe qué validar | Vincula CA ↔ RN |
| Matriz solo de un lado | Operaciones implementadas, reglas sin probar | Llena las 5 columnas |

---

## 🚀 Siguiente paso

Con criterios y trazabilidad, tu diseño ya tiene la forma de [la plantilla por feature](./PLANTILLA-DISENIO-FEATURE.md) lista para reutilizar. Cuando llegues a los tests, el módulo [05-TESTING](../05-TESTING/) te muestra cómo escribirlos a partir de estos criterios.

---

**Tiempo estimado:** 15-20 minutos por feature
