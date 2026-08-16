# 17: Recursos Externos

> Los recursos que se usaron y los que sirven para profundizar. Nada de "listas interminables": cada enlace tiene un **cuándo usarlo**.

---

## Fundamentales (estudiar primero)

| Recurso | Qué aporta | Cuándo |
|---|---|---|
| [The System Design Primer](https://github.com/donnemartin/system-design-primer) | Base teórica completa + casos resueltos | Lee toda la sección de topics; es la columna del curso |
| [Designing Data-Intensive Applications](https://dataintensive.net/) (Kleppmann) | El libro de referencia de datos, consistencia y replicación | Después de dominar el primer |
| [System Design Interview — Alex Xu](https://www.amazon.com/System-Design-Interview-Insiders-Guide/dp/1736049119) | Framework de entrevista y casos paso a paso | Cuando prepares entrevistas |

---

## Guías cortas y visuales (para consultar)

| Recurso | Cuándo |
|---|---|
| [ByteByteGo — Guides](https://bytebytego.com/guides) | Diagramas rápidos por tema (cache, chat, e-commerce, multi-tenant) |
| [ByteByteGo — CAP Theorem](https://bytebytego.com/guides/cap-theorem-one-of-the-most-misunderstood-terms) | Si CAP te confunde (a todos nos pasa) |
| [ByteByteGo — Caching strategies](https://bytebytego.com/guides/top-5-caching-strategies) | Cuando dudes entre cache-aside/write-through |
| [Brendan Gregg — USE Method](https://www.brendangregg.com/usemethod.html) | Para métricas de rendimiento |
| [AWS Architecture Center](https://aws.amazon.com/architecture/) | Casos reales de arquitecturas cloud |

---

## Supabase (el stack del repositorio)

| Recurso | Cuándo |
|---|---|
| [Supabase Docs — Database](https://supabase.com/docs/guides/database) | RLS, índices, transacciones en Postgres |
| [Supabase Docs — Realtime](https://supabase.com/docs/guides/realtime) | Postgres Changes, Presence, Broadcast |
| [Supabase Docs — Auth](https://supabase.com/docs/guides/auth) | JWT, authn/authz, magic links |
| [Supabase Docs — Edge Functions](https://supabase.com/docs/guides/functions) | Lógica de backend asíncrona (colas, checkout) |
| [Supabase Docs — Logging/Metrics](https://supabase.com/docs/guides/telemetry) | Observabilidad gestionada |
| [Supabase — The Next.js Starter](https://github.com/supabase/supabase/tree/master/examples) | Ejemplos oficiales multi-caso |

---

## Simuladores / práctica activa

| Recurso | Qué hacer |
|---|---|
| [System Design Primer — Solutions](https://github.com/donnemartin/system-design-primer#system-design-topics-start-here) | Corregir los ejercicios del archivo 16 |
| [ByteByteGo — Interview problems](https://bytebytego.com/blog/system-design-interview-questions) | Casos extra para el Nivel 4 |
| [Kleppmann's blog](https://martin.kleppmann.com/) | Profundización en consistencia y streaming |

---

## Orden de estudio sugerido

```
1. System Design Primer (topics)           → teoría base
2. Archivos 00-11 de este módulo           → teoría aplicada al stack
3. Casos 12-15 (plantilla)                 → ver el framework en acción
4. Ejercicios 16                          → practicar
5. DDIA / Alex Xu                          → profundizar y preparar entrevista
6. Supabase docs                           → cuando implementes
```

---

## Regla de oro

> No leas 10 recursos a la vez. **Uno a la vez**, con el objetivo de resolver el siguiente ejercicio. El System Design Primer es el único que vale leer de principio a fin; el resto es consulta puntual.

---

**Siguiente:** [BIBLIOGRAFIA.md](./BIBLIOGRAFIA.md)
