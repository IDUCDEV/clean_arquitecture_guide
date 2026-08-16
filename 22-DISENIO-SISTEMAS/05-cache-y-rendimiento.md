# 05: Cache y Rendimiento

> La caché es la herramienta de rendimiento #1 en cualquier sistema: evita rehacer trabajo caro (lecturas a la DB, redes, cálculos). Aprender las estrategias y sus trade-offs es imprescindible.

---

## Latencia vs Throughput

Antes de cachear, hay que medir bien:

- **Latency:** tiempo en realizar una acción o producir un resultado.
- **Throughput:** número de acciones o resultados por unidad de tiempo.
- **Objetivo general:** *"maximal throughput with acceptable latency"*.

*Fuente: System Design Primer — "Latency vs throughput".*

Un problema de latencia = tu sistema es lento para un usuario. Un problema de throughput = es rápido para uno pero se hunde con muchos.

---

## Dónde poner cachés (de cliente a servidor)

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Client      │   │  CDN         │   │  Web server  │   │  Database    │
│  cache       │   │  caching     │   │  caching     │   │  caching     │
│ (app local)  │   │ (edge)       │   │ (reverse pr.)│   │ (query/obj)  │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
   más cerca del usuario ──────────────────────────────── más cerca de los datos
```

*Fuente: System Design Primer — "Cache" section.*

| Capa | Qué cachea | Ejemplo en Flutter + Supabase |
|---|---|---|
| Cliente | Datos ya vistos, respuestas | Cache local del feed (Isar, módulo 04 del repo) |
| CDN | Estáticos/media | Imágenes de Supabase Storage |
| Servidor web | Respuestas HTTP completas | Reverse proxy, respuestas de API |
| Aplicación | Objetos serializados | Cache en memoria/Redis de respuestas |
| Base de datos | Resultados de queries | Query cache, materialized views |

---

## Niveles de caché en detalle

### Client caching (en la app Flutter)
- **HTTP caching:** headers `Cache-Control`, `ETag` para no re-descargar lo que no cambió.
- **Local DB:** guardar en Isar las últimas N páginas del feed → lecturas offline y pantalla instantánea.
- **Beneficio enorme:** evita round-trips completos; es la caché más barata.

### CDN caching
- Sirve media desde el nodo más cercano (ver archivo 03).
- TTL controla cuánto tiempo el contenido se considera válido.

### Web server / application caching
- Una caché en memoria (p. ej. Redis o un cache del servidor) guarda las **respuestas frecuentes ya computadas**.
- Para Supabase: las lecturas del feed se pueden cachear en una Edge Function o en un servicio intermedio.

### Database caching
- Resultados de queries frecuentes en memoria (query cache).
- **Materialized views** en Postgres para agregados precomputados (ej. conteos de likes).

---

## Estrategias de actualización de caché

*Fuente: System Design Primer — "When to update the cache".*

### 1. Cache-aside (lazy loading)
```
App → busca en cache → ¿hit? → devuelve
                     → ¿miss? → lee de DB → guarda en cache → devuelve
```
- **Pros:** datos solo se cachean si se usan; tolerante a fallos de cache.
- **Contras:** primer acceso lento (miss); si el cache muere, la DB recibe todo.

### 2. Write-through
- La escritura va a la caché **y** a la DB en el mismo paso.
- **Pros:** consistencia entre cache y DB; lecturas nunca con datos viejos.
- **Contras:** cada escritura paga doble (mayor latencia de escritura); riesgo de datos poco usados ocupando cache.

### 3. Write-behind (write-back)
- La escritura va solo a la caché y se persiste a la DB **asíncronamente**.
- **Pros:** escrituras rapidísimas.
- **Contras:** riesgo de perder datos si la caché cae antes de persistir.

### 4. Refresh-ahead
- La caché se refresca **antes** de que expire si predice que será accedida.
- **Pros:** menos misses.
- **Contras:** predicción puede equivocarse (work innecesario).

| Estrategia | Velocidad de lectura | Consistencia | Riesgo |
|---|---|---|---|
| Cache-aside | Miss lento | Stale hasta refresco | Cache miss storm |
| Write-through | Siempre fresca | Alta | Escrituras lentas |
| Write-behind | Alta | Eventual | Pérdida de datos |
| Refresh-ahead | Alta | Eventual | Work innecesario |

---

## Consideraciones de caché (trade-offs)

- **TTL (expiración):** el contenido puede quedar **stale** (desactualizado) hasta que expire.
- **Invalidación:** cuando un dato cambia, hay que invalidar/actualizar el cache — si no, los usuarios ven datos viejos.
- **Eviction:** políticas para quitar datos cuando el cache se llena (LRU — Least Recently Used — es la más común).
- **Cache stampede (miss storm):** si todos los caches expiran a la vez y miles piden el mismo dato a la DB → desastre. Mitigar con *stale-while-revalidate* o jitter en TTL.

---

## Diseño de caché para el feed del repo (decisión completa)

Datos del archivo 02: ratio lectura/escritura 10:1, QPS pico ~32, feed ensamblado caro.

**Diseño elegido (cache-aside + write-through para el feed):**

```
Lectura:  app → cache local (Isar, última página) → si miss → API → Redis
                 → si miss → Postgres (ensambla con joins) → guarda en Redis → devuelve

Escritura: cuando se crea un post → se invalida el cache del feed del autor
           (los feeds de otros se refrescan con cache-aside natural)
```

**Justificación (trade-offs):**
- Cache-aside: el feed es mayormente de **lectura** → ratio 10:1 lo justifica.
- Invalidez al escribir: mantener el feed de cada usuario coherente sin write-through costoso.
- Cache local (Isar): pantalla instantánea + soporte offline (enlaza archivo 10).

---

## Errores comunes

| Error | Solución |
|---|---|
| Cachear todo sin medir | Primero medir latencia/throughput |
| Sin TTL ni invalidación | Definir TTL y ruta de invalidación por escritura |
| Un solo cache global | Distribuir por capa (cliente, CDN, app, DB) |
| Ignorar el cache stampede | Jitter en TTL + stale-while-revalidate |
| Cachear datos que no se leen | Cache-aside cachea solo lo usado |

---

## Fuentes

- [The System Design Primer — Cache](https://github.com/donnemartin/system-design-primer#cache)
- [The System Design Primer — Latency vs throughput](https://github.com/donnemartin/system-design-primer#latency-vs-throughput)
- [ByteByteGo — Cache Systems Every Developer Should Know](https://bytebytego.com/guides/cache-systems-every-developer-should-know)
- [ByteByteGo — Top 5 Caching Strategies](https://bytebytego.com/guides/top-5-caching-strategies)
- [Designing Data-Intensive Applications — M. Kleppmann](https://dataintensive.net/)

---

**Siguiente:** [06-realtime-y-streaming.md](./06-realtime-y-streaming.md)
