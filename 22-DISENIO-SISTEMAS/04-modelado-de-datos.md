# 04: Modelado de Datos a Escala

> Diseñar el esquema no solo para que funcione hoy, sino para que sobreviva a millones de filas. Índices, replicación, sharding, denormalización y la decisión SQL vs NoSQL.

---

## El ciclo de vida de una base de datos

```
1 fila → 1M filas → 100M filas → 1B filas
   │        │           │            │
   │      Índices    Replicas     Sharding
   │      + cache    (lecturas)   (escrituras)
   │
   (aquí vive la mayoría de MVPs)
```

*Fuente: System Design Primer — "Database" section.*

---

## 1. Diseño del esquema (relacional)

Un buen esquema relacional empieza igual que en el módulo 03 del repo: tablas normalizadas con claves foráneas e índices para las consultas frecuentes.

```sql
-- Posts con índice por usuario y por fecha
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  image_url TEXT NOT NULL,
  caption TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_posts_user ON posts(user_id);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
```

**Regla:** el índice se crea para las **consultas que realmente haces**, no para todas las columnas. Cada índice acelera lecturas pero frena escrituras.

---

## 2. La decisión SQL vs NoSQL

| Criterio | SQL (PostgreSQL) | NoSQL (documento/llave-valor) |
|---|---|---|
| Esquema | Fijo, relacional | Flexible |
| Transacciones ACID | Sólidas | Variables según motor |
| Relaciones/joins | Nativos | Se emulan en app |
| Escalado | Vertical + réplicas; sharding manual | Horizontal por diseño |
| Ideal para | Datos relacionados, transacciones | Flexibilidad, escrituras masivas |

**Supabase usa PostgreSQL.** Para el 90% de las apps Flutter + Supabase, la respuesta es SQL. Los casos NoSQL suelen aparecer a escalas enormes o con datos no estructurados.

*Fuente: System Design Primer — "SQL or NoSQL".*

---

## 3. Replicación

Copias de la misma base de datos para alta disponibilidad y/o lecturas distribuidas.

### Master-Slave (activo-pasivo)
```
   ┌────────┐  writes  ┌───────────┐
   │  App   │─────────▶│  Master   │
   └────────┘          └─────┬─────┘
        │                    │ replication (async)
        ▼ reads              ▼
   ┌─────────┐        ┌───────────┐
   │  App    │────────│  Slaves   │  (lecturas)
   └─────────┘        └───────────┘
```
- El master atiende escrituras y se replica a los slaves.
- Los slaves atienden lecturas → más throughput de lectura.
- **Trade-off:** si el master muere antes de replicar una escritura, esa escritura se pierde.

### Master-Master (activo-activo)
- Ambos atienden escrituras; se replican entre sí.
- **Trade-off:** resolución de conflictos entre dos masters; complejidad alta.

**En Supabase/Postgres:** Supabase ofrece réplicas de lectura (read replicas) como función de pago. El diseño se documenta igual; el aprovisionamiento lo gestiona Supabase.

---

## 4. Federación (Federation)

Dividir las bases de datos **por dominio/función** en vez de por datos:

```
Una sola DB            ──▶   DB de usuarios + DB de posts + DB de analytics
```

**Pros:** menos contención, aislamiento de fallos. **Contras:** joins entre DBs se vuelven costosos; más infraestructura.

**En el diseño Flutter+Supabase:** equivale a separar tablas en esquemas y, a escala mayor, servicios independientes con su propia DB. Para un MVP no se recomienda.

---

## 5. Sharding (particionado horizontal)

Distribuir filas de una tabla en **múltiples bases de datos** según una clave (shard key):

```
    Hash(user_id) % 3
   ┌──────┬──────┬──────┐
   │Shard 0│Shard 1│Shard 2│
   │  1/3  │  1/3  │  1/3  │
   └──────┴──────┴──────┘
```

**Trade-offs del sharding:**
- **Pros:** escala escrituras y almacenamiento horizontalmente.
- **Contras:** joins entre shards, operaciones no distribuidas en app, rebalanceo complejo, agregados difíciles.

**Regla:** sharding es el **último recurso**, después de índices, cache, réplicas y federación. En Supabase, esto se sale del alcance gestionado; a esa escala ya no es una sola instancia de Postgres.

---

## 6. Denormalización

Guardar datos **redundantes** a propósito para evitar joins costosos en las lecturas.

```
Normalizado:  posts + join a users para mostrar el nombre del autor
Denormalizado: posts.autor_name ya guardado en la tabla de posts
```

**Trade-off:** lees más rápido, pero **escribes más** (mantener la copia sincronizada) y arriesgas inconsistencias.

**Ejemplo real del repo (feed):** en vez de un join `posts ⋈ users ⋈ likes` en cada scroll, el feed cacheado se guarda **ya ensamblado** (denormalizado) con nombre de autor e imagen. El join se paga una vez al ensamblar el cache, no en cada lectura.

---

## 7. SQL tuning (ajuste de consultas)

Antes de sharding, primero se optimiza la consulta:

- Usar **índices** adecuados (composite indexes para filtros múltiples).
- **EXPLAIN** para ver el plan de ejecución (en Supabase: `EXPLAIN ANALYZE`).
- Evitar `SELECT *`, limitar columnas.
- Paginación con **cursor** en vez de `OFFSET` grande para feeds.

---

## Árbol de decisión de escalado de datos

```
¿La consulta es lenta?
 ├─ Sí → ¿Índices? → NO → añade índices + EXPLAIN
 │                     SÍ → ¿Es por lectura repetitiva? → cache (archivo 05)
 │                          NO → ¿Muchas lecturas concurrentes? → read replicas
 │                               ¿Escrituras el cuello? → federación / particionado
 │                                    ¿Todo lo anterior falla? → sharding
 └─ No → sigue así
```

---

## En el stack Supabase: qué es de tu diseño y qué es gestionado

| Pieza | ¿La diseñas tú? | ¿La gestiona Supabase? |
|---|---|---|
| Esquema, índices, RLS | ✅ Sí (módulo 03 del repo) | No |
| Replicación | Documentas el diseño | ✅ Read replicas (función) |
| Alta disponibilidad/failover | No | ✅ Gestionado |
| Backups | No | ✅ Gestionado |
| Sharding | Solo a escala gigante | No (fuera del alcance) |

---

## Fuentes

- [The System Design Primer — Database](https://github.com/donnemartin/system-design-primer#database)
- [The System Design Primer — SQL or NoSQL](https://github.com/donnemartin/system-design-primer#sql-or-nosql)
- [Designing Data-Intensive Applications — M. Kleppmann](https://dataintensive.net/)
- [Supabase Docs — Database](https://supabase.com/docs/guides/database)

---

**Siguiente:** [05-cache-y-rendimiento.md](./05-cache-y-rendimiento.md)
