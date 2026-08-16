# 07: Escalabilidad y Alta Disponibilidad

> Cómo hacer que el sistema soporte más carga y menos caídas. Vertical vs horizontal, CAP theorem, y la disponibilidad medida en "nueves".

---

## Performance vs Scalability

- **Performance:** tu sistema es lento para **un solo usuario**.
- **Scalability:** tu sistema es rápido para uno, pero lento **bajo carga**.

*Fuente: System Design Primer — "Performance vs scalability".*

> *"A service is scalable if it results in increased performance in a manner proportional to resources added."*

---

## Escalado vertical vs horizontal

| | Vertical (scale up) | Horizontal (scale out) |
|---|---|---|
| Cómo | Más CPU/RAM en la misma máquina | Más máquinas |
| Límite | Físico (la máquina más grande que exista) | Casi ilimitado |
| Coste | Caro, con saltos | Lineal, elástico |
| Fallo | Punto único de fallo | Tolerante (replicas) |
| Complejidad | Baja | Alta (LB, coordinación) |

**Regla:** primero vertical (barato y simple), después horizontal con **load balancing**.

*Fuente: System Design Primer — "Horizontal scaling".*

---

## CAP theorem

En un sistema distribuido solo puedes garantizar **dos de tres**:

- **Consistency:** cada lectura recibe la escritura más reciente, o un error.
- **Availability:** cada request recibe una respuesta (aunque no sea la más reciente).
- **Partition tolerance:** el sistema sigue operando aunque la red se parta (nodos incomunicados).

> *"Networks aren't reliable, so you'll need to support partition tolerance. You'll need to make a software tradeoff between consistency and availability."*

### CP vs AP

| | CP (consistencia) | AP (disponibilidad) |
|---|---|---|
| Ante una partición | Espera/bloquea hasta estar consistente | Responde con lo disponible (puede estar viejo) |
| Ideal para | Pagos, inventario, contadores | Feeds, chats, notificaciones |
| Ejemplo | Postgres replicado con waits | Cache distribuida, DNS |

**En una app Flutter + Supabase:** Postgres por defecto te da consistencia fuerte en una sola instancia. El realtime con cache introduce consistencia eventual donde el negocio lo permita (ej. conteo de likes puede ser eventual; un pago debe ser consistente).

*Fuente: System Design Primer — "CAP theorem" + [ByteByteGo — CAP Theorem: One of the Most Misunderstood Terms](https://bytebytego.com/guides/cap-theorem-one-of-the-most-misunderstood-terms).*

---

## Patrones de consistencia

*Fuente: System Design Primer — "Consistency patterns".*

| Patrón | Qué garantiza | Dónde vive |
|---|---|---|
| **Weak** | Tras un write, los reads pueden no verlo (best-effort) | Memcached, VoIP, chat de voz |
| **Eventual** | Tras un write, los reads lo verán eventualmente (ms) | DNS, email, feeds |
| **Strong** | Tras un write, todos los reads lo ven | Filesystems, RDBMS |

**En el feed del repo:** el contador de likes usa consistencia eventual (así se ve en el ejemplo de 05: cache del feed ensamblado). El estado del pago usa consistencia fuerte (Postgres transaccional).

---

## Patrones de alta disponibilidad

*Fuente: System Design Primer — "Availability patterns".*

### Fail-over
| | Active-passive | Active-active |
|---|---|---|
| Quién atiende | Solo el activo; el pasivo en standby | Ambos |
| Heartbeat | El pasivo detecta caída del activo | — |
| Timeout | Depende de hot/cold standby | — |
| Coste | Menor | Mayor |
| Riesgo | Pérdida de writes no replicados | Conflictos entre masters |

### Replication
Ver archivo 04: master-slave (lecturas distribuidas) y master-master.

### Disponibilidad en números (los famosos "nueves")

| Disponibilidad | Downtime/año | Downtime/mes | Downtime/día |
|---|---|---|---|
| 99% | 3d 15h | 7h 18m | 14m 24s |
| 99.9% | 8h 45m | 43m 49s | 1m 26s |
| 99.99% | 52m 35s | 4m 23s | 8.6s |

*Tabla publicada por el System Design Primer.*

### Componentes en serie vs en paralelo

```
En serie:   Availability_total = A_foo × A_bar
            (0.999 × 0.999 = 0.998 → 99.8%)

En paralelo: Availability_total = 1 − (1 − A_foo) × (1 − A_bar)
            (1 − 0.001 × 0.001 = 0.999999 → 99.9999%)
```

**Lectura:** cada componente en serie *reduce* la disponibilidad total; los componentes redundantes en paralelo la *aumentan*. Por eso la alta disponibilidad se logra con redundancia (paralelo), no encadenando piezas únicas.

---

## Qué significa esto para Flutter + Supabase

| Pieza | ¿De quién es la disponibilidad? | Nivel típico |
|---|---|---|
| App en el dispositivo | Del usuario (fuera de tu control) | — |
| Supabase (API, Auth, DB, Storage, Realtime) | De Supabase (SLA gestionado) | Alta |
| CDN de media | Del proveedor de CDN | Muy alta |
| Edge Functions | De Supabase | Alta |

**Diseño que debes defender:** no reinventas la alta disponibilidad para Supabase (es gestionada). Tu responsabilidad es:

1. **No crear puntos únicos de fallo en tu código** (ej. un `Stream` que muere sin reconnect).
2. **Elegir el SLA correcto** para tu caso (un MVP no necesita 99.99%).
3. **Cache local** para que la app no caiga si la red falla (offline-first, archivo 10).

---

## Árbol de decisión de escalabilidad

```
¿Lento con mucha carga?
 ├─ ¿CPU/RAM saturada? → vertical primero
 ├─ ¿Lecturas? → cache + read replicas
 ├─ ¿Escrituras? → federación / particionado
 ├─ ¿Un servidor único? → LB + horizontal scaling
 ├─ ¿Caídas? → failover + replicación
 └─ ¿Todo a la vez? → rediseña (CAP trade-off explícito)
```

---

## Fuentes

- [The System Design Primer — Performance vs scalability](https://github.com/donnemartin/system-design-primer#performance-vs-scalability)
- [The System Design Primer — Availability vs consistency (CAP)](https://github.com/donnemartin/system-design-primer#availability-vs-consistency)
- [The System Design Primer — Availability patterns](https://github.com/donnemartin/system-design-primer#availability-patterns)
- [ByteByteGo — CAP Theorem: One of the Most Misunderstood Terms](https://bytebytego.com/guides/cap-theorem-one-of-the-most-misunderstood-terms)
- [ByteByteGo — How to Design for High Availability](https://bytebytego.com/guides/how-do-we-design-for-high-availability)
- [Designing Data-Intensive Applications — M. Kleppmann](https://dataintensive.net/)

---

**Siguiente:** [08-seguridad-en-diseno.md](./08-seguridad-en-diseno.md)
