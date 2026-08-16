# 11: Plantilla de Diseño de Sistema

> El proceso reproducible para cualquier pregunta de system design: del requisito al diagrama, con métricas, decisiones y riesgos. Úsalo en los casos de estudio (12-14) y en tus entrevistas.

---

## La plantilla (10 pasos)

```
1. Alcance y requerimientos       → qué SÍ y qué NO está en el diseño
2. Estimación de escala           → QPS, storage, ratios (archivo 02)
3. Modelado de datos              → entidades, índices, RLS (archivo 04)
4. Arquitectura de alto nivel     → diagrama de cajas y flujos
5. Componentes clave              → API, DB, cache, CDN, realtime
6. Decisiones de diseño           → cada una con su trade-off
7. Consistencia y disponibilidad  → CAP, SLA, patrón elegido
8. Seguridad                      → authn/authz, RLS, HTTPS (archivo 08)
9. Observabilidad                → logs, métricas, alertas (archivo 09)
10. Riesgos y evolución           → cuellos de botella futuros y mitigación
```

---

## Paso 1: Alcance y requerimientos

Antes de dibujar, aclara con el entrevistador/cliente:

| Pregunta | Ejemplo |
|---|---|
| ¿Quiénes son los usuarios? | Consumidores de un feed de fotos |
| ¿Cuántos? | 10M MAU |
| ¿Qué funcionalidad principal? | Ver y publicar posts |
| ¿Tiempo real o eventual? | Feed eventual; chat realtime |
| ¿Mobile, web, ambos? | Flutter (mobile + web) |
| ¿Es un MVP o un sistema maduro? | Determina la complejidad justa |

**No olvides:** definir lo que **NO** está en el alcance (fuera de scope) para no diseñar de más.

---

## Paso 2: Estimación de escala (archivo 02 en 30s)

```
QPS de lecturas   = usuarios activos × acciones por usuario / segundos
QPS de escrituras = publicaciones/transacciones por día / 86,400
Storage           = filas × bytes promedio × retención
Ratio lectura/escritura = lecturas / escrituras
```

Ejemplo del feed: 10M MAU, 5% activos por hora pico, 100 lecturas diarias → QPS de lectura ≈ 1.7K, escrituras ≈ 4/s, ratio ≈ 10:1.

---

## Paso 3: Modelado de datos (mínimo viable)

- Lista de **entidades** con sus campos clave.
- **Índices** para los path de acceso reales.
- **RLS policies** por entidad (quién lee/escribe).
- Elección: SQL vs NoSQL **justificada** (archivo 04).

---

## Paso 4: Arquitectura de alto nivel

Dibuja las cajas: `App → CDN/API → (Auth, Cache, DB) → Servicios`. Ejemplo genérico:

```
┌─────────┐  HTTPS  ┌────────────┐        ┌───────────┐
│  App    │────────▶│  API       │───────▶│  Cache    │
└─────────┘         │  (Supabase)│        └───────────┘
        │           └─────┬──────┘               │
        │                 ▼                      ▼
   ┌─────────┐      ┌────────────┐        ┌───────────┐
   │  CDN    │      │  Auth      │        │  DB (Post)│
   └─────────┘      └────────────┘        └───────────┘
```

---

## Paso 5-6: Componentes y decisiones de diseño

Cada componente declarado debe justificarse:

| Componente | Decisión | Trade-off |
|---|---|---|
| Cache | Cache-aside del feed | Miss lento, pero solo cachea lo usado |
| Realtime | WebSocket (Realtime) | Complejidad, límites de conexiones |
| CDN | Para media | Coste, TTL de invalidación |
| DB | Postgres (Supabase) | Consistencia fuerte, escala limitada |

**Fórmula:** *"Elijo X porque el caso es Y, y el trade-off aceptable es Z."*

---

## Paso 7: Consistencia y disponibilidad

Declara explícitamente:
- **Modelo de consistencia:** strong (Postgres) para datos críticos; eventual (cache, contadores) para el resto.
- **SLA objetivo:** cuántos "nueves" y por qué.
- **Patrones:** replicas, failover, retries/backoff.

---

## Paso 8-9: Seguridad y observabilidad

- **Seguridad:** HTTPS, RLS deny-by-default, secrets en secure storage, least privilege.
- **Observabilidad:** las 3-5 métricas clave, las alertas accionables, cómo se diagnostica cada error.

---

## Paso 10: Riesgos y evolución

```
Riesgo detectado        → Mitigación
-----------------------  → -----------------------------
QPS pico de escrituras   → Colas + Edge Functions async
Joins caros en el feed   → Denormalización en cache
Saturación de una DB     → Replicas de lectura → particionado
App muerta sin red       → Offline-first (archivo 10)
```

Cierra la entrevista/diseño con: **"el siguiente cuello de botella sería X, y lo resolvería con Y"**.

---

## Checklist final de una respuesta de system design

- [ ] Alcance claro (incluye fuera de scope)
- [ ] Números justificados (QPS, storage, ratios)
- [ ] Diagrama de alto nivel dibujado
- [ ] Decisiones con trade-offs explícitos
- [ ] Modelo de datos con índices y RLS
- [ ] Consistencia/disponibilidad declaradas
- [ ] Seguridad y observabilidad presentes
- [ ] Riesgos futuros y evolución

---

## Fuentes

- [The System Design Primer — Intro](https://github.com/donnemartin/system-design-primer#system-design-topics-start-here)
- [ByteByteGo — System Design Interview Guide](https://bytebytego.com/guides/system-design-interview-guide)
- [System Design Interview — Alex Xu](https://www.amazon.com/System-Design-Interview-Insiders-Guide/dp/1736049119)

---

**Siguiente:** [12-caso-feed-red-social.md](./12-caso-feed-red-social.md)
