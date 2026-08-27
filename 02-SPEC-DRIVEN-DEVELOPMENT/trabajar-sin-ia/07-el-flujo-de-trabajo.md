# El Flujo de Trabajo: Framework de 6 Fases

> Un método paso a paso para enfrentar cualquier feature sin depender de IA. Cada fase tiene un objetivo claro y un punto de salida definido.

---

## 1. Visión general del framework

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FRAMEWORK DE 6 FASES                                 │
│                                                                         │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                              │
│  │ FASE 1  │ → │ FASE 2  │ → │ FASE 3  │                              │
│  │Investigar│   │ Diseñar │   │ Implementar│                            │
│  └─────────┘   └─────────┘   └─────────┘                              │
│       │              │              │                                   │
│       ↓              ↓              ↓                                   │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                              │
│  │ FASE 4  │ → │ FASE 5  │ → │ FASE 6  │                              │
│  │ Verificar│   │ Refactor│   │ Validar │                              │
│  └─────────┘   └─────────┘   └─────────┘                              │
│                                                                         │
│  Regla de oro: EN CADA FASE, la IA es un verificador, no el autor.    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Tiempo estimado por fase (feature promedio):**

| Fase | Tiempo | ¿Cuándo usar IA? |
|------|--------|-------------------|
| 1. Investigar | 30-60 min | Sólo si la documentación oficial falla |
| 2. Diseñar | 30-45 min | Nunca — esto es tu trabajo |
| 3. Implementar | Variable | Nunca — esto es tu trabajo |
| 4. Verificar | 15-30 min | Para revisar tests, no para escribirlos |
| 5. Refactor | 15-30 min | Para sugerencias, no para ejecutar |
| 6. Validar | 10-15 min | Sí — como auditor final |

---

## 2. FASE 1: Investigar

### Objetivo
Entender QUÉ necesitas hacer y CON QUÉ herramientas antes de escribir código.

### Checklist de investigación

```
┌─────────────────────────────────────────────────────────────────┐
│ CHECKLIST FASE 1                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ □ Leo la documentación oficial del paquete/servicio             │
│ □ Busco en el repositorio oficial (GitHub)                      │
│ □ Reviso issues abiertas (problemas conocidos)                  │
│ □ Busco ejemplos en el propio proyecto (feature similar)        │
│ □ Defino la feature con formato User Story                      │
│ □ Identifico dependencias nuevas                                │
│ □ Estimo complejidad (Simple/Intermedia/Compleja)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Herramientas de investigación (orden de preferencia)

1. **Documentación oficial** del paquete/servicio
2. **GitHub del repositorio** — README, issues, ejemplos
3. **pub.dev** (Flutter/Dart) — descripción, ejemplos, changelog
4. **Stack Overflow** — problemas específicos
5. **Blog posts de confianza** — tutoriales de expertos
6. **IA** — SÓLO si todo lo anterior falla, y para confirmar, no para descubrir

### Formato de User Story

```markdown
## Feature: [Nombre]

**Como** [actor], **quiero** [acción], **para** [beneficio].

### Contexto
- [Qué existe actualmente en el proyecto]
- [Qué dependencias se necesitan]
- [Qué restricciones aplican]

### Criterios de aceptación
- [ ] [Criterio 1]
- [ ] [Criterio 2]
- [ ] [Criterio 3]

### Complejidad estimada: [Simple/Intermedia/Compleja]
```

### Punto de salida
Tienes claro QUÉ construir y CON QUÉ. Puedes explicar la feature sin mirar notas.

---

## 3. FASE 2: Diseñar

### Objetivo
Traducir la investigación en un plan de implementación en papel.

### Checklist de diseño

```
┌─────────────────────────────────────────────────────────────────┐
│ CHECKLIST FASE 2                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ □ Descompongo la feature usando requisitos EARS (Módulo 02)      │
│ □ Mapeo cada pieza a su capa en Clean Architecture             │
│ □ Defino contratos (interfaces) ANTES de implementar            │
│ □ Diagramo el flujo de datos entre capas                        │
│ □ Identifico estados y transiciones (si aplica)                 │
│ □ Defino entidades y modelos                                    │
│ □ Listo las excepciones que debo manejar                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Plantilla de diseño rápido

```markdown
## Diseño: [Nombre Feature]

### Descomposición (EARS)
| Pieza | Capa | Responsabilidad |
|-------|------|-----------------|
| [Nombre] | [Domain/Data/Presentation] | [Qué hace] |

### Contratos (interfaces)
```dart
// Ejemplo de contrato
abstract class [Nombre]Repository {
  Future<Either<Failure, [Tipo]>> obtener[Algo]([params]);
}
```

### Flujo de datos
```
UI → Controller → UseCase → Repository → DataSource
```

### Estados
```dart
enum [Feature]Status { inicial, cargando, exito, error }
```

### Excepciones
- [Excepción 1]: [Cuándo ocurre]
- [Excepción 2]: [Cuándo ocurre]
```

### Punto de salida
Tienes un plan en papel que puedes seguir paso a paso al implementar.

---

## 4. FASE 3: Implementar

### Objetivo
Escribir código siguiendo el diseño, un paso a la vez.

### Checklist de implementación

```
┌─────────────────────────────────────────────────────────────────┐
│ CHECKLIST FASE 3                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ □ Implemento por capas, no todo junto                           │
│ □ Empiezo por el dominio (entidades, contratos)                 │
│ □ Luego data (repositorio, datasource, modelos)                │
│ □ Luego domain (use cases)                                     │
│ □ Finalmente presentation (controllers, UI)                     │
│ □ Cada pieza funciona por separado antes de conectarla          │
│ □ Uso el diseño como guía, no como suggestion                   │
│ □ Me detengo cuando me confundo (no sigo con código que no entiendo)│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Orden de implementación por capas

```
1. DOMAIN
   ├── entities/        ← Modelos del negocio
   ├── repositories/    ← Contratos (interfaces)
   └── usecases/        ← Lógica de negocio

2. DATA
   ├── models/          ← Modelos de datos (mapeo)
   ├── datasources/     ← Fuentes de datos (API, BD local)
   └── repositories/    ← Implementación de contratos

3. PRESENTATION
   ├── controllers/     ← Lógica de UI (BLoC/Provider/Riverpod)
   └── pages/           ← Widgets y pantallas
```

### Reglas de implementación

1. **Una pieza a la vez.** No intentes construir todo junto.
2. **Si no entiendes algo, para.** No sigas con código que no comprendes.
3. **Documenta decisiones.** Usa comentarios para explicar POR QUÉ, no QUÉ.
4. **Tests básicos.** Al menos un test por use case mientras implementas.

### Punto de salida
Todo el código está escrito, compila, y cada pieza funciona individualmente.

---

## 5. FASE 4: Verificar

### Objetivo
Asegurar que el código funciona correctamente antes de integrarlo.

### Checklist de verificación

```
┌─────────────────────────────────────────────────────────────────┐
│ CHECKLIST FASE 4                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ □ Ejecuto los tests existentes (no deben fallar)               │
│ □ Escribo tests para la nueva feature                           │
│ □ Pruebo manualmente los casos de uso principales              │
│ □ Verifico manejo de errores (qué pasa si falla la red)        │
│ □ Reviso que no haya código muerto o no utilizado              │
│ □ Valido que los contratos se cumplan                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Tipos de verificación

| Tipo | Qué verifica | Cómo |
|------|-------------|------|
| **Unit tests** | Lógica de negocio aislada | `flutter test` |
| **Widget tests** | UI se renderiza correctamente | `flutter test` |
| **Integration tests** | Flujo completo funciona | `flutter test integration_test/` |
| **Manual** | Experiencia de usuario | Ejecutar la app y probar |

### Qué probar manualmente

1. **Happy path:** Todo funciona como se espera
2. **Error path:** Qué pasa cuando algo falla
3. **Edge cases:** Datos vacíos, límites, formatos raros
4. **Navegación:** La feature encaja en el flujo de la app

### Punto de salida
Los tests pasan, la feature funciona manualmente, y no hay errores evidentes.

---

## 6. FASE 5: Refactorizar

### Objetivo
Mejorar la calidad del código sin cambiar su comportamiento.

### Checklist de refactorización

```
┌─────────────────────────────────────────────────────────────────┐
│ CHECKLIST FASE 5                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ □ Reviso nombres (¿son claros y descriptivos?)                 │
│ □ Elimino código duplicado                                      │
│ □ Verifico que cada clase tenga una responsabilidad             │
│ □ Reviso que no hayadependencias circulares                     │
│ □ Simplifico lógica compleja                                    │
│ □ Verifico que los tests sigan pasando                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Preguntas de refactorización

| Pregunta | Si la respuesta es no... |
|----------|--------------------------|
| ¿El nombre describe qué hace? | Renombra |
| ¿Puedo explicar esta función en una frase? | Divide |
| ¿Esta clase tiene más de una responsabilidad? | Separa |
| ¿Hay código que no se usa? | Elimina |
| ¿Los tests cubren los casos principales? | Agrega tests |

### Cuándo puedes usar IA aquí

- **Sí:** Pedir sugerencias de nombres mejores
- **Sí:** Pedir que identifique código duplicado
- **Sí:** Pedir que revise si hay violaciones de SOLID
- **No:** Dejar que IA reescriba el código por ti

### Punto de salida
El código es legible, mantenible, y cada pieza tiene una responsabilidad clara.

---

## 7. FASE 6: Validar con IA

### Objetivo
Usar IA como auditor final, no como creador. Esta es la ÚNICA fase donde IA participa activamente.

### Qué le preguntas a IA

```
┌─────────────────────────────────────────────────────────────────┐
│              PROMPTS ESPECÍFICOS POR FEATURE TYPE               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ PARA CRUD SIMPLE:                                               │
│ "Revisa mi implementación de [feature]. ¿El manejo de errores  │
│ está completo? ¿Falta algún caso edge? ¿Los nombres son        │
│ claros? NO reescribas el código, solo dame feedback."           │
│                                                                 │
│ PARA FEATURE CON ESTADOS:                                       │
│ "Revisa mi máquina de estados para [feature]. ¿Todas las       │
│ transiciones son válidas? ¿Hay estados inalcanzables?          │
│ ¿Manejo correctamente los estados de carga y error?"            │
│                                                                 │
│ PARA FEATURE CON TIEMPO REAL:                                   │
│ "Revisa mi implementación de streams para [feature]. ¿El       │
│ manejo de suscripciones es correcto? ¿Evito memory leaks?      │
│ ¿Cómo manejo la reconexión?"                                    │
│                                                                 │
│ PARA FEATURE CON API EXTERNA:                                   │
│ "Revisa mi integración con [servicio]. ¿El manejo de errores   │
│ de red es completo? ¿Retry automático? ¿Timeouts configurados? │
│ ¿Cache para offline?"                                           │
│                                                                 │
│ PARA CUALQUIER FEATURE:                                         │
│ "Revisa esta implementación como si fueras un senior revisando │
│ un PR. Dame 3 cosas que están bien y 3 cosas que mejorar.      │
│ NO reescribas nada."                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Qué hacer con el feedback de IA

1. **Lee todo el feedback** antes de actuar
2. **Evalúa cada punto** — ¿tiene razón?
3. **Implementa los cambios** que tengan sentido
4. **Ignora** sugerencias que no entiendas o que cambien demasiado
5. **Vuelve a ejecutar tests** después de cambios

### Regla de oro de la Fase 6

> IA es el auditor, tú eres el autor. Si IA sugiere un cambio que no entiendes, NO lo implementes. Primero entiende, luego decide.

### Punto de salida
Has recibido feedback externo, lo has evaluado críticamente, y has hecho mejoras que entiendes.

---

## 8. Resumen visual del flujo

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  RECIBES FEATURE                                                        │
│       │                                                                 │
│       ↓                                                                 │
│  ┌─────────────┐                                                        │
│  │ 1. INVESTIGAR│ ← Documentación oficial, GitHub, pub.dev             │
│  └──────┬──────┘                                                        │
│         ↓                                                               │
│  ┌─────────────┐                                                        │
│  │ 2. DISEÑAR  │ ← requisitos EARS, mapeo de capas, contratos, flujos  │
│  └──────┬──────┘                                                        │
│         ↓                                                               │
│  ┌─────────────┐                                                        │
│  │ 3. IMPLEMENTAR│ ← Por capas, un paso a la vez, sin prisa           │
│  └──────┬──────┘                                                        │
│         ↓                                                               │
│  ┌─────────────┐                                                        │
│  │ 4. VERIFICAR │ ← Tests unitarios, manuales, edge cases              │
│  └──────┬──────┘                                                        │
│         ↓                                                               │
│  ┌─────────────┐                                                        │
│  │ 5. REFACTOR  │ ← Nombres claros, código limpio, SOLID              │
│  └──────┬──────┘                                                        │
│         ↓                                                               │
│  ┌─────────────┐                                                        │
│  │ 6. VALIDAR   │ ← IA como auditor, tú decides qué cambiar           │
│  └──────┬──────┘                                                        │
│         ↓                                                               │
│  FEATURE COMPLETA                                                       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Errores comunes a evitar

| Error | Por qué ocurre | Cómo evitarlo |
|-------|----------------|---------------|
| Saltarse la investigación | "Ya más o menos sé qué hacer" | Siempre lee documentación oficial primero |
| Saltarse el diseño | "Es una feature simple" | Incluso CRUD necesita diseño (5 min) |
| Implementar todo junto | Ansiedad de ver resultado | Implementa por capas, una a la vez |
| No hacer tests | "Ya funciona" | Si funciona ahora, no significa que siempre funcione |
| No refactorizar | Presión de tiempo | 15 min de refactor ahorran horas de debugging |
| Usar IA en fases prohibidas | Costumbre | Recuerda: IA sólo en Fase 1 (si falla doc) y Fase 6 |

---

**Siguiente:** [08-como-investigar-sin-ia.md](./08-como-investigar-sin-ia.md) — Cómo encontrar respuestas sin depender de IA
