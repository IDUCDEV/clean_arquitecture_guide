# Alcance de la Feature (Paso 0)

> Antes de aplicar FADER, define qué entra y qué NO entra en la feature. Una feature puede estar bien descompuesta y aun así tener un alcance ambiguo que la haga crecer mientras la implementas.

---

## ¿Por qué definir alcance primero?

El error clásico no es descomponer mal: es descomponer **bien la feature equivocada**.

Sin alcance, cada revisión añade un "y de paso también...":
- "La pantalla de compradores" → alguien pregunta *"¿y qué pasa con las notificaciones?"* → la feature crece.
- El FADER se rehace 3 veces porque el problema real nunca quedó acotado.
- El sprint termina con una feature a medias y otra empezada.

El alcance responde antes que cualquier otra cosa:

> **¿Qué resuelve esta feature? ¿Qué NO resuelve? ¿Qué necesita de los demás?**

FADER te dice *cómo* hacer la feature. El alcance te dice *cuál* es la feature.

```
Flujo del diseño:

  0. ALCANCE          ← este archivo
  1. FADER            ← 01-descomposicion-feature.md
  2. MAPEO            ← 02-mapeo-capas.md
  3. CONTRATOS        ← 03-contratos-primero.md
  4. FLUJO            ← 04-flujo-datos.md
  5. BACKEND           ← 05e-diseno-supabase.md (Supabase / REST API)
  6. CRITERIOS        ← 05f-criterios-aceptacion-trazabilidad.md
  7. ESTIMACIÓN       ← 15-estimacion-complejidad.md
```

---

## Las 5 secciones del Alcance

### 1. Incluye

Todo lo que la feature **sí** cubre. Sé explícito y concreto. No escribas "gestión de compradores" — escribe las operaciones.

```
Incluye:
- Listar compradores.
- Buscar por nombre o teléfono.
- Aprobar tickets.
- Liberar tickets.
```

### 2. No incluye

Todo lo que la feature **no** cubre, aunque parezca relacionado. Es la sección que evita el *scope creep*.

```
No incluye:
- Enviar notificaciones.
- Procesar pagos.
- Editar datos del comprador.
- Historial de cambios.
```

> **Regla:** si algo que *podría* estar relacionado no está en "Incluye", debe estar en "No incluye". No dejes espacio para la ambigüedad.

### 3. Dependencias

Qué necesita que exista **antes** o **durante**. Pueden ser otras features, servicios, tablas o APIs.

```
Dependencias:
- Feature de autenticación (para saber quién es el organizador).
- Tabla `raffles` existente en Supabase.
- RLS configurado para `organizer_id`.
```

### 4. Suposiciones

Cosas que asumes como verdaderas sin verificar. Documentarlas permite que se discutan en vez de descubrirse en producción.

```
Suposiciones:
- Un comprador pertenece a una sola rifa.
- "Aprobar" significa marcar el ticket como ganador.
- El organizador es el único que gestiona su rifa.
```

### 5. Preguntas abiertas

Lo que todavía no sabes y necesitas responder antes o durante el diseño. Si una pregunta puede cambiar el alcance, resuélvela antes de FADER.

```
Preguntas abiertas:
- ¿Puede aprobarse un ticket que ya fue aprobado?
- ¿La aprobación debe ser atómica con la liberación?
- ¿Hay límite de tickets aprobados por rifa?
```

---

## Ejemplo completo: Buyers

Aplicado a una feature real de una app de rifas:

```
Feature: Gestión de compradores (Buyers)

Incluye:
- Listar compradores.
- Buscar por nombre o teléfono.
- Aprobar tickets seleccionados.
- Liberar tickets no seleccionados.

No incluye:
- Enviar notificaciones.
- Procesar pagos.
- Editar datos del comprador.
- Historial de aprobaciones.

Dependencias:
- Autenticación (identidad del organizador).
- Feature de rifas (tabla raffles).
- RLS en tickets por organizer_id.

Suposiciones:
- Un comprador pertenece a una sola rifa.
- "Aprobar" = marcar ticket como ganador.
- Solo el organizador de la rifa gestiona sus compradores.

Preguntas abiertas:
- ¿Puede aprobarse un ticket ya aprobado?
- ¿La aprobación debe ser atómica (aprobar + liberar)?
- ¿Existe límite de tickets aprobados por rifa?
```

---

## Plantilla de Alcance

```markdown
Feature: [Nombre]

## Alcance

### Incluye
- [ ]
- [ ]

### No incluye
- [ ]
- [ ]

### Dependencias
- [ ]
- [ ]

### Suposiciones
- [ ]
- [ ]

### Preguntas abiertas
- [ ]
- [ ]
```

---

## Errores comunes

| Error | Síntoma | Solución |
|-------|---------|----------|
| "Incluye" vago | "Gestión de compradores" | Lista operaciones concretas |
| "No incluye" vacío | La feature crece durante la implementación | Anticipa lo que podría parecer relacionado |
| Ocultar supuestos | Se descubren en producción | Documenta todo lo que asumes |
| Preguntas sin resolver | Rediseños constantes | Resuélvelas antes de FADER si cambian el alcance |
| Alcance y FADER desalineados | Operaciones que no están en "Incluye" | Cada operación de FADER debe estar en "Incluye" |

---

## Checklist de autoevaluación

- [ ] Cada operación de FADER aparece en "Incluye"
- [ ] Nada de "No incluye" se filtra al diseño
- [ ] Cada dependencia está identificada (features, tablas, servicios)
- [ ] Las suposiciones son explícitas y verificables
- [ ] Las preguntas abiertas críticas se resolvieron antes de empezar

---

## 🚀 Siguiente paso

Con el alcance definido, aplica [FADER](./01-descomposicion-feature.md) para descomponer la feature dentro de los límites que acabas de fijar.

---

**Tiempo estimado:** 10-15 minutos por feature  
**Herramientas:** Papel y lápiz
