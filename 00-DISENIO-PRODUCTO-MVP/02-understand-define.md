# 02 — Understand + Define

**Día 1: Entender el problema y definir el foco**

---

Estas dos fases ocurren en el **mismo día**. La mañana es para entender, la tarde para definir.

## Fase 1: Understand

El objetivo es que todo el equipo tenga el mismo nivel de información sobre el problema, el usuario y el negocio.

### 1.1. Ejercicio: Start at the End

Define el **goal a largo plazo** del producto.

```
Pregunta: "¿Qué estará pasando cuando nuestro producto sea un éxito?"
Ejemplo: "Los usuarios podrán reservar una cancha de tenis en menos de 30 segundos
          desde su teléfono, sin llamar por teléfono."
```

El goal debe tener una **métrica** asociada:
> Ejemplo: "Reducir el tiempo de reserva promedio de 5 minutos a <30 segundos"

### 1.2. Ejercicio: Mapa del problema

Dibuja el flujo del usuario **actual** (sin tu producto). Identifica puntos de fricción.

```
[Usuario quiere jugar tenis]
  → Abre Google Maps → Busca canchas → Encuentra teléfono
  → Llama → Ocupado → Vuelve a llamar → Pregunta disponibilidad
  → "Sí, hay a las 5pm" → "OK, reserve" → Llega y la cancha está ocupada
  ← FRUSTRACIÓN ←
```

Los puntos de fricción son **oportunidades de diseño**.

### 1.3. Ejercicio: Expert Interviews

Cada miembro del equipo comparte lo que sabe. Formato:

| Persona | Aporta |
|---|---|
| Decisor | Visión de negocio, restricciones, stakeholders |
| Diseñador | Patrones de UX, competencia, tendencias mobile |
| Dev | Viabilidad técnica, costos, tiempos |
| Experto | Datos de mercado, investigación de usuarios |

Preguntas clave:
- ¿Qué sabemos con certeza?
- ¿Qué estamos asumiendo?
- ¿Qué necesitaríamos saber para tener confianza?

### 1.4. Ejercicio: How Might We (HMW)

Reformula cada punto de fricción como una oportunidad:

> Fricción: "Llamar por teléfono es lento y poco confiable"
> HMW: "¿Cómo podríamos permitir reservar sin hablar con nadie?"

> Fricción: "No saber si la cancha estará disponible al llegar"
> HMW: "¿Cómo podríamos garantizar disponibilidad en tiempo real?"

---

## Fase 2: Define

Con toda la información sobre la mesa, es hora de **acotar**.

### 2.1. Ejercicio: The Golden Path

Define el **camino ideal** del usuario dentro del MVP. No más de 3-4 pantallas.

```
Pantalla 1: Home → "Buscar canchas"
Pantalla 2: Lista de canchas → "Seleccionar fecha y hora"
Pantalla 3: Confirmar reserva → "Pagar"
Pantalla 4: Confirmación → "Listo, llegas a las 5pm"
```

El Golden Path es el **flujo crítico** del MVP. Todo lo demás: registro, perfil, historial, etc. son **post-MVP**.

### 2.2. Ejercicio: Definir el alcance del MVP

El MVP no es "lo mínimo para salir", sino **lo mínimo para validar valor**.

Usa la matriz **Impacto vs. Esfuerzo**:

```
Impacto ↑
  |  [Hacer primero]  |  [Hacer después]  |
  |  Golden Path      |  Historial        |
  |  Reserva rápida   |  Favoritos        |
  |--------------------|-------------------|
  |  [Último]         |  [Evitar]         |
  |  Chat en vivo     |  Modo oscuro      |
  |  Landing page     |  Animaciones      |
  └────────────────────→ Esfuerzo
```

**Regla de oro del MVP mobile:**
> Si no está en el Golden Path, no entra en el MVP.

### 2.3. Sprint Goal

Redacta el objetivo del Sprint en una frase:

> "Validar que los usuarios pueden reservar una cancha de tenis en menos de 30 segundos desde su teléfono."

Esto guiará todas las decisiones del resto de la semana.

### 2.4. Checklist del Día 1

- [ ] Goal a largo plazo definido con métrica
- [ ] Mapa del problema dibujado
- [ ] HMWs generados a partir de fricciones
- [ ] Golden Path definido (3-4 pantallas)
- [ ] MVP scope acotado (qué entra / qué no entra)
- [ ] Sprint Goal redactado
- [ ] Usuarios reclutados para el viernes (Validate)

## Plantilla: Documento de alcance del MVP

```
---
MVP: [Nombre del producto]
Goal: [Frase única]
Métrica principal: [Ej: tiempo de reserva <30s]
---

## Golden Path
1. [Pantalla 1: acción]
2. [Pantalla 2: acción]
3. [Pantalla 3: acción]

## Incluye (MVP)
- [Feature 1]
- [Feature 2]
- [Feature 3]

## No incluye (post-MVP)
- [Feature X]
- [Feature Y]

## Supuestos a validar
1. [Supuesto 1: ej, "los usuarios quieren reservar sin hablar"]
2. [Supuesto 2]

## Criterios de éxito
- [ ] [Criterio 1]
- [ ] [Criterio 2]
```

---

**Siguiente: [03 — Sketch + Decide](03-sketch-decide.md)**
