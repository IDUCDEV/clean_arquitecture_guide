# 03 — Sketch + Decide

**Día 2: Bosquejar soluciones → Día 3: Decidir la mejor**

---

## Fase 3: Sketch

El objetivo es que **cada miembro del equipo** genere soluciones de forma individual. No se discute, no se critica, se dibuja.

### 3.1. Ejercicio: Lightning Demos (mañana)

Antes de dibujar, inspírate. Cada miembro muestra 2-3 apps o productos existentes que resuelven problemas similares.

Para cada demo, responde:
- ¿Qué hace bien?
- ¿Qué harías diferente?
- ¿Qué podríamos robar (remix)?

Ejemplo para una app de reservas:
> **Airbnb**: la navegación por fechas es excelente. **OpenTable**: la confirmación instantánea da confianza. **Uber**: no necesitas registro para usarlo.

### 3.2. Ejercicio: Crazy 8s

Cada persona dobla una hoja en 8 partes. En **8 minutos** (1 minuto por recuadro), dibuja 8 variaciones de una pantalla clave.

```
┌─────────┬─────────┬─────────┬─────────┐
│  Var 1  │  Var 2  │  Var 3  │  Var 4  │
│         │         │         │         │
├─────────┼─────────┼─────────┼─────────┤
│  Var 5  │  Var 6  │  Var 7  │  Var 8  │
│         │         │         │         │
└─────────┴─────────┴─────────┴─────────┘
```

No importa la calidad del dibujo. Importa la cantidad de ideas.

### 3.3. Ejercicio: Solution Sketch (tarde)

Cada persona crea un **boceto detallado** de su mejor solución. Formato de 3 paneles:

```
┌─────────────────────────────────────┐
│  Panel 1: Estado actual / problema  │
│  (una escena que muestre la         │
│   frustración del usuario)          │
├─────────────────────────────────────┤
│  Panel 2: La solución               │
│  (la pantalla clave del MVP)        │
├─────────────────────────────────────┤
│  Panel 3: El resultado              │
│  (el usuario feliz, métrica lograda)│
└─────────────────────────────────────┘
```

El Solution Sketch debe ser **auto-explicativo**. Mañana alguien más podría tener que entenderlo sin que le expliques nada.

Herramientas: papel y lápiz (recomendado), o tool digital como Miro/Figma.

---

## Fase 4: Decide

El objetivo es **elegir una sola solución** para prototipar.

### 4.1. Ejercicio: Art Museum

Pega todos los Solution Sketches en la pared. El equipo camina en silencio y los revisa.

Cada persona tiene:
- **2 dot votes grandes** (👍): "Esto es genial, deberíamos construirlo"
- **1 dot vote pequeño** (❓): "Esto es interesante, pero tengo dudas"

### 4.2. Ejercicio: Heat Map + Speed Critique

El facilitador selecciona los sketches con más votos. El equipo los critica rápidamente (3 min cada uno):

| Pregunta | Tiempo |
|---|---|
| ¿Qué nos gusta? | 1 min |
| ¿Qué dudas tenemos? | 1 min |
| ¿Qué mejorarías? | 1 min |

### 4.3. Ejercicio: Straw Poll + Decisión Final

Votación final. Cada persona tiene **1 voto** (no puede votar por el suyo).

- Si hay empate, el **Decisor** desempata.
- El Decisor puede elegir una solución híbrida ("tomamos la navegación de A y el detalle de B").

### 4.4. Ejercicio: Storyboard

Con la solución elegida, el diseñador (con ayuda del equipo) crea un **storyboard** detallado del prototipo. Esto es el **plano** para el Día 4.

```
┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐
│ Home   │ → │ Lista  │ → │ Detalle│ → │ Confir │
│ Buscar │   │ Canchas│   │ Reserva│   │ OK!    │
│        │   │ 3pm    │   │ Pagar  │   │ 5pm    │
└────────┘   └────────┘   └────────┘   └────────┘
     ↓            ↓            ↓            ↓
  TextField    ListView    BottomSheet   Confetti
  + Icon      + Filtros   + ElevatedBtn  + Icon
```

Cada pantalla del storyboard debe incluir:
- **Layout** básico (qué va donde)
- **Componentes M3** a usar (ver módulo 05)
- **Flujo de datos** (qué pasa cuando el usuario toca)
- **Estados**: carga, vacío, error, éxito

### 4.5. Checklist del Día 3

- [ ] Solución única seleccionada y aprobada por el Decisor
- [ ] Storyboard detallado con todas las pantallas del Golden Path
- [ ] Componentes M3 identificados para cada pantalla
- [ ] Prototipador asignado y herramientas listas (Figma / Flutter)
- [ ] Guión de entrevista preparado para el viernes
- [ ] Usuarios confirmados para Validate (mínimo 5)

---

## De Sketch/Decide a M3

El storyboard es el **puente** entre el Design Sprint y Material Design 3.

En el storyboard defines **qué** va en cada pantalla. En los próximos capítulos aprenderás **cómo** diseñarlo con M3.

| Storyboard dice | M3 provee |
|---|---|
| "Barra de navegación abajo" | `NavigationBar` |
| "Tarjeta con producto" | `Card` + `ListTile` |
| "Botón principal" | `FilledButton` / `FilledTonalButton` |
| "Selector de fecha" | `DatePickerDialog` |
| "Campo de búsqueda" | `SearchBar` |

---

**Siguiente: [04 — Fundamentos de Material Design 3](04-m3-fundamentos.md)**
