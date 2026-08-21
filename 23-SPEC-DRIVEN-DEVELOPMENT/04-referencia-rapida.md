# 04 - Referencia Rápida

> Cheat sheet de SDD: fases, puertas, EARS, boundaries, proporcionalidad y OpenSpec.

---

## Las 4 fases de SDD

```
REQUISITOS → DISEÑO → TAREAS → IMPLEMENTACIÓN
   ¿QUÉ?      ¿CÓMO?    ¿EN QUÉ        ¿EJECUTAR
                         ORDEN?          (agente/humano)
```

| Fase | Entregable | Quién participa |
|------|-----------|-----------------|
| Requisitos | Historias, criterios, reglas | PO + equipo |
| Diseño | Arquitectura, contratos, tablas | Developer + agente |
| Tareas | Unidades atómicas con prompts | Developer |
| Implementación | Código, tests, commits | Agente + developer |

---

## Las 3 puertas de aprobación

```
PUERTA 1              PUERTA 2              PUERTA 3
Requisitos → Diseño   Diseño → Tareas       Tareas → Implementación
```

| Puerta | Pregunta clave | Qué verificar |
|--------|---------------|---------------|
| **1** | ¿Resolvemos el problema correcto? | Requisitos completos, criterios verificables, reglas explícitas |
| **2** | ¿Es viable y coherente? | Patrones del codebase, dependencias, orden lógico |
| **3** | ¿Estas tareas producen el diseño? | Cobertura, sin huecos, prompts precisos |

**Regla de oro:** El coste de corregir un error crece exponencialmente por fase. Corregir en requisitos es trivial; corregir en implementación es caro.

---

## Notación EARS (5 patrones)

| Patrón | Palabra clave | Template | Ejemplo Flutter |
|--------|--------------|----------|-----------------|
| **Ubicuo** | (sin condición) | "El sistema SHALL [comportamiento]" | "La app SHALL mostrar el nombre del usuario en todas las páginas" |
| **Evento** | **CUANDO** | "CUANDO [evento], el sistema SHALL [respuesta]" | "CUANDO el usuario pulsa logout, el sistema SHALL cerrar sesión" |
| **Estado** | **MIENTRAS** | "MIENTRAS [condición], el sistema SHALL [comportamiento]" | "MIENTRAS el formulario sea inválido, el botón SHALL estar deshabilitado" |
| **No deseado** | **SI** | "SI [error], el sistema SHALL [recuperación]" | "SI la sesión expira, el sistema SHALL redirigir al login" |
| **Opcional** | **DONDE** | "DONDE [configuración], el sistema SHALL [comportamiento]" | "DONDE el usuario habilitó biometría, el sistema SHALL ofrecer login por huella" |

**Template universal:**
```
MIENTRAS [precondición], CUANDO [evento], el sistema debe [respuesta]
```

---

## Sistema de boundaries (Always / Ask First / Never)

| Nivel | Significado | Ejemplo Flutter |
|-------|-------------|-----------------|
| **Always** | El agente ejecuta sin preguntar | `flutter analyze`, naming conventions, const constructors |
| **Ask First** | Requiere aprobación antes de ejecutar | Añadir dependencias, modificar migrations, cambiar routing |
| **Never** | Líneas rojas absolutas | Commitear .env, editar build.gradle, modificar RLS de producción |

**Regla de evolución:** A medida que el equipo gana confianza, algo que hoy es Ask First puede pasar a Always.

---

## Principio de proporcionalidad

### Pregunta de calibración

> ¿Qué pasa si el agente toma la decisión equivocada en este punto?

| Respuesta | Acción |
|-----------|--------|
| "Lo corrijo en 2 minutos" | No necesita especificarse |
| "Pierdo horas o introduzco un bug sutil" | Sí necesita especificarse |

### Cuándo usar SDD vs vibe coding

| Situación | Herramienta |
|-----------|-------------|
| Bug trivial, script, prototipo | Vibe coding |
| Feature compleja, cambio con riesgo, trabajo en equipo | SDD |
| Feature nueva en codebase existente | SDD + Impact Report |
| Refactor grande | SDD (sin FADER) |

---

## Maldición de las instrucciones

> A más instrucciones en un prompt, menor probabilidad de que el modelo cumpla cada una.

**Señales de spec sobrecargada:**
- El agente ignora restricciones escritas
- Cumple lo del principio pero no lo del final
- Mejora cuando se reduce la spec
- Acierta con tareas aisladas y falla con varias juntas

**Solución:** Dividir, no acumular. Cinco specs de 10 instrucciones > una de 50.

---

## Specs vivas: 3 niveles de vida

| Nivel | Descripción | Deriva |
|-------|-------------|--------|
| **Spec-first** | Se escribe antes, guía la tarea, se descarta | No aplica |
| **Spec-anchored** | Se mantiene como documentación viva | Riesgo real → actualizar en mismo commit |
| **Spec-as-source** | La spec es el artefacto principal; código se regenera | Desaparece por diseño (experimental) |

### Clarity Gate (prueba de calidad)

> ¿Puede un agente diferente generar código equivalente solo con la spec?

- **Sí** → spec clara y completa
- **No** → faltan supuestos implícitos → actualizar spec

---

## OpenSpec: comandos rápidos

| Comando | Acción |
|---------|--------|
| `npm install -g @fission-ai/openspec@latest` | Instalar |
| `openspec init` | Inicializar en el proyecto |
| `/opsx:explore` | Explorar opciones |
| `/opsx:propose <nombre>` | Crear cambio completo |
| `/opsx:apply` | Ejecutar tareas |
| `/opsx:archive` | Archivar cambio |
| `openspec update` | Regenerar instrucciones de agentes |

---

## Plantilla de spec (copia y pega)

```markdown
### Requirement: [Nombre] [Componente]
The [Sistema/Capa] SHALL [comportamiento].

#### Scenario: [Éxito]
- GIVEN [precondición]
- WHEN [acción]
- THEN [resultado esperado]

#### Scenario: [Error]
- GIVEN [condición de error]
- WHEN [acción]
- THEN [resultado de error]
```

---

## Antipatrones de SDD

| Antipatrones | Descripción | Solución |
|-------------|-------------|----------|
| **Sobreespecificación** | Más tiempo en specs que en código | Principio de proporcionalidad |
| **Teatro de especificación** | Specs que nadie revisa de verdad | Puertas de aprobación reales |
| **Documentación zombi** | Specs que nadie consulta | decidir qué mantener, qué dejar morir |
| **Rigidez excesiva** | Mismo proceso para bug trivial y feature compleja | Calibrar intensidad |
| **Puertas como cuellos de botella** | Aprobación bloqueada por ausencia | Delegación asíncrona |

---

## Referencia completa

| Documento | Ubicación |
|-----------|-----------|
| Guía SDD teórica | `Guia-SDD-equipos-agiles.pdf` (raíz del proyecto) |
| OpenSpec guía práctica | `01-openspec-guia-practica.md` (este módulo) |
| SDD en Flutter | `02-sdd-en-flutter.md` (este módulo) |
| Integración con FADER | `03-integracion-modulo-02-fader.md` (este módulo) |
