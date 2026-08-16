# 01: Clarificar Requisitos

> El paso más infravalorado del system design. Una entrevista o un proyecto se ganan o se pierden en los primeros 10 minutos, cuando **claras el problema antes de diseñar**.

---

## Por qué clarificar primero

El system design interview es una **conversación abierta**. Se espera que *tú* la lideres. Si empiezas a dibujar servidores sin saber cuántos usuarios hay, estás diseñando a ciegas.

*Fuente: System Design Primer — "How to approach a system design interview question".*

> Step 1: Outline use cases, constraints, and assumptions. Gather requirements and scope the problem. Ask questions to clarify use cases and constraints.

---

## Framework de clarificación

### A. Casos de uso (¿qué hace el sistema?)

- ¿Quién lo usa? (usuarios, admins, sistemas externos)
- ¿Cómo lo usan? (app móvil, web, ambos)
- ¿Cuáles son las entradas y salidas del sistema?
- ¿Cuál es el caso de uso principal y cuáles son secundarios?

### B. Restricciones (¿cuánto, qué tan rápido, cuántos?)

| Pregunta | Determina |
|---|---|
| ¿Cuántos usuarios totales? | Complejidad del sistema |
| ¿Cuántos usuarios concurrentes? | Capacidad de servidores |
| ¿Cuántos requests por segundo esperamos? | Dimensionamiento |
| ¿Cuánta data por día? | Almacenamiento |
| ¿Ratio de lecturas vs escrituras? | Patrón de cache/replicación |
| ¿Latencia aceptable? | Caching, CDN, geografía |
| ¿Requiere real-time? | WebSocket vs polling |
| ¿Disponibilidad requerida? | Nº de "nueves", failover |

### C. Suposiciones (lo que asumes y declaras)

Todo lo que no te digan, lo **asumes en voz alta** y lo dejas escrito. Ejemplo: *"Asumo 100M de lecturas/día y 10M de escrituras/día"*. Esto convierte el problema abierto en algo accionable.

---

## Ejemplo aplicado al stack del repo: "Diseña un feed de posts"

Aplicando el framework a una feature Flutter + Supabase:

```
CASOS DE USO
- Usuario autenticado ve un feed paginado de posts (principal)
- Usuario crea un post con imagen (secundario)
- Usuario da like (secundario)

RESTRICCIONES (las preguntamos)
- ¿Cuántos usuarios? → 500k registrados, 50k DAU
- QPS de lecturas?   → 50k DAU × ~10 lecturas/día / 86400s ≈ 6 QPS promedio, picos de 30 QPS
- Ratio L/E?         → ~10 lecturas por cada escritura
- Latencia?          → < 500 ms al hacer scroll
- Realtime?          → No imprescindible, se acepta refresh

SUPOSICIONES DECLARADAS
- Las imágenes se sirven vía CDN
- Los posts viven en Postgres (Supabase)
- Asumo que el pico es 5× el promedio
```

Este párrafo de 6 líneas **define todo el diseño posterior**: si el ratio es 10:1, priorizamos cache de lecturas; si es realtime, Supabase Realtime.

---

## Técnica del "si no me lo dicen, lo asumo"

En una entrevista el entrevistador suele ser deliberadamente vago. La técnica correcta:

```
NO:  "Diseño un feed"  (y empiezas a dibujar)
SÍ:  "Antes de diseñar necesito saber: ¿cuántos usuarios?, ¿cuántos requests
      por segundo?, ¿el feed es en tiempo real o con refresh?, ¿las imágenes
      se sirven por CDN? Si no me lo puedes decir, asumo 50k DAU y ratio 10:1."
```

Esto demuestra criterio y cubre tus espaldas: si asumiste mal, es responsabilidad documentada.

---

## Checklist de clarificación

- [ ] Usuarios totales y activos (DAU/MAU)
- [ ] Requests por segundo (promedio y pico)
- [ ] Ratio lectura/escritura
- [ ] Almacenamiento esperado (GB/TB por día)
- [ ] Latencia objetivo
- [ ] ¿Realtime o no?
- [ ] Disponibilidad objetivo (SLA)
- [ ] Plataformas (móvil, web, ambos)
- [ ] Suposiciones declaradas en voz alta
- [ ] Escenario de crecimiento (¿×10 en 1 año?)

---

## Fuentes

- [The System Design Primer — How to approach a system design interview question](https://github.com/donnemartin/system-design-primer#how-to-approach-a-system-design-interview-question)
- [Grokking Modern System Design Interview — Educative](https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers)

---

**Siguiente:** [02-estimacion-de-escala.md](./02-estimacion-de-escala.md)
