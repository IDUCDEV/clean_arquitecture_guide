# Diseño Supabase por Feature

> Después de mapear y definir contratos, diseña la sección tecnológica específica de Supabase: tablas, operaciones, RLS, atomicidad y realtime. Aquí viven las reglas técnicas y de seguridad.

> **Alcance:** esto no es "diseñar un backend". Define **lo que la app necesita del servidor**. Con Supabase (BaaS) la app lo implementa (tablas, RLS, RPC). Con una REST API (Python/otro) la app solo especifica el **contrato** que consume su `RemoteDataSource` con Dio — el backend la diseña e implementa.

---

## ¿Por qué una sección Supabase?

El diseño no termina en los contratos. Como tu stack es estable (Flutter + Supabase), cada feature puede documentar exactamente qué necesita de la base de datos **antes** de escribir la primera consulta.

Esto evita que aparezca esto en un Cubit o un widget:

```dart
// ❌ Diseño de Supabase improvisado dentro de la UI
supabase.from('tickets').select().eq('raffle_id', id);
```

Y fuerza a decidir antes, en papel:

- ¿Qué tablas toca la feature?
- ¿Qué consultas y escrituras hace?
- ¿Quién puede leer/escribir cada fila (RLS)?
- ¿La operación necesita ser atómica (transacción o RPC)?
- ¿Necesita datos en tiempo real?

### ¿Y si tu backend es una REST API (Python/otro)?

El diseño no cambia: la feature sigue necesitando lo mismo del servidor. Solo cambia **quién implementa**.

| Con Supabase (BaaS) | Con una REST API |
|---|---|
| La app diseña e implementa tablas, RLS y RPC | La app especifica el **contrato** (verbo + path, DTO, códigos de error, garantías) y el backend lo implementa |
| RS → policies de RLS | RS → se exige al backend autorización en el servidor (roles/middleware) |
| Atomicidad → función RPC | Atomicidad → se exige al backend una operación atómica e idempotente en 1 request |
| Realtime → canales de Supabase | Realtime → se exige WebSocket/SSE con el mismo contrato `Stream<Entity>` |

El `RemoteDataSource` es la costura: con Supabase usa `SupabaseClient`, con una REST API usa Dio — el repositorio no sabe ni le importa cuál (ver [05b-data-layer](../01-CLEAN-ARCHITECTURE/05b-data-layer.md)).

---

## Reglas técnicas y de seguridad

En `01-descomposicion-feature.md` clasificas las reglas en tres tipos. Esta sección recoge las que NO pertenecen al dominio:

```
Reglas de negocio (RN)     → van al UseCase        → dominio puro
Reglas técnicas (RT)       → van al contrato con el backend → esta sección
Reglas de seguridad (RS)   → van a la autorización del servidor (Supabase: RLS · REST: middleware/roles) → esta sección
```

**Reglas técnicas:**
- La consulta debe estar paginada.
- La búsqueda debe tener debounce.
- La operación debe ejecutarse en una transacción.
- Se debe manejar pérdida de conexión.

**Reglas de seguridad:**
- RLS debe impedir acceder a rifas ajenas.
- El organizador solo puede modificar sus tickets.
- Solo se puede leer el propio perfil.

> **No confundas:** las reglas técnicas y de seguridad no van en el dominio. Se documentan aquí, durante el diseño, para que el DataSource y la migración SQL las implementen (o el contrato que se entrega al backend REST).

---

## La sección Supabase por feature

```
## Supabase

### Tablas
- tickets
- raffles
- buyers

### Operaciones
- select    (listar compradores de una rifa)
- update    (aprobar/liberar tickets)
- RPC       (aprobar seleccionados + liberar el resto)
- realtime  (opcional: refrescar lista)

### RLS
- Política de lectura:  el organizador lee solo sus tickets
- Política de escritura: el organizador actualiza solo sus tickets

### Atomicidad
- ¿Necesita transacción?       Sí (aprobar + liberar debe ser 1 operación)
- ¿Necesita función RPC?       Sí, ver `approve_and_release_tickets`
- ¿Cuándo?                     Cuando hay 2+ escrituras que deben ser atómicas

### Realtime
- ¿Lo necesita?   No (en esta versión)
- Canal:
- Evento:
```

---

## La decisión clave: transacción vs RPC

Cuando una operación necesita escribir en **2+ lugares** (o validar y escribir al mismo tiempo), el DataSource no puede hacer dos `update` separados sin riesgo de quedarse a medias.

| Necesidad | Solución | Cuándo |
|-----------|----------|--------|
| **Transacción** | `rpc()` con una función que hace BEGIN/COMMIT | La validación depende de leer el estado actual (ej: no dobles reservas) |
| **RPC simple** | Función PostgreSQL | La operación es un procedimiento que combina varias escrituras |
| **Dos updates** | Sin función | Las escrituras son independientes y toleran fallar por separado |

> **Test de atomicidad técnico:** si una regla dice *"los seleccionados se aprueban Y los demás se liberan"*, y falla a mitad, ¿el sistema queda en un estado inválido? Si sí → necesita RPC/transacción.

---

## Ejemplo completo: Buyers

**Regla del negocio:** "Cuando el organizador confirma, los tickets seleccionados se aprueban y los demás se liberan."

Esto son 2 escrituras dependientes → no puede ser un `update` simple.

```
## Supabase (feature Buyers)

### Tablas
- raffles
- tickets

### Operaciones
- [R] select      listar tickets de una rifa
- [U] update      liberar tickets (estado = liberado)
- [RPC] approve_and_release_tickets(
    p_raffle_id, p_winner_ids[]
  ) → aprueba los seleccionados Y libera el resto en una transacción

### RLS
- Lectura:  tickets.where(raffle.organizer_id == auth.uid())
- Escritura: solo via RPC, que verifica organizer_id antes de escribir

### Atomicidad
- Transacción: Sí
- RPC: approve_and_release_tickets
- Alternativa descartada: dos updates separados (estado inválido si falla el segundo)

### Realtime
- ¿Lo necesita?   No
- Canal:
- Evento:
```

---

## Realtime: cuándo y cómo

No toda feature necesita tiempo real. Antes de añadir un canal, pregúntate:

| Pregunta | Si responde "sí" |
|----------|------------------|
| ¿Otro usuario puede cambiar los datos mientras yo los veo? | Necesita realtime |
| ¿La pantalla se abre una vez y no cambia? | No lo necesita |
| ¿Puedo refrescar con pull-to-refresh? | Probablemente no |

```
### Realtime
- ¿Lo necesita?   Sí
- Canal:          tickets_raffle_{raffleId}
- Evento:         UPDATE (aprobación/liberación de tickets)
- Filtro RLS:     el canal debe respetar las mismas políticas
```

**Contrato del DataSource con realtime:** el Repository expone un `Stream<Entity>` además de las operaciones CRUD:

```dart
abstract class TicketsDataSource {
  Future<List<TicketModel>> fetchTickets(String raffleId);
  Stream<TicketModel> watchTickets(String raffleId);   // realtime
  Future<void> approveAndRelease(String raffleId, List<String> winnerIds);
}
```

---

## Buenas prácticas

- **RLS siempre.** Si una tabla es accesible sin RLS, la seguridad depende del cliente — y el cliente no se debe confiar.
- **Los RPC verifican permisos dentro de la función**, no asumen que el llamador es legítimo.
- **Los índices se diseñan con la consulta**: filtros por `raffle_id`, búsquedas por nombre con `pg_trgm`.
- **Una operación atómica = un contrato.** Si el contrato del repositorio dice `approveAndRelease(...)`, el DataSource lo implementa con un RPC — no con dos llamadas.
- **El dominio sigue sin saber de Supabase.** Todo lo de este archivo se implementa en DATA y se refleja en las migraciones.

---

## Errores comunes

| Error | Síntoma | Solución |
|-------|---------|----------|
| Consultas de Supabase en la UI | `supabase.from(...)` en un widget | Diseña el DataSource en esta sección |
| RLS ausente | Cualquiera lee todo | Toda tabla accesible desde el cliente tiene política |
| Operación atómica con 2 updates | Estado inválido si falla el segundo | RPC en transacción |
| Realtime innecesario | Canales abiertos que nadie usa | Responde las preguntas de la tabla |
| Reglas técnicas dentro del UseCase | Paginación/debounce en dominio | Documenta como RT, implementa en DATA |

---

## 🚀 Siguiente paso

Ya definiste qué necesita la feature de la base de datos. Ahora escribe los [criterios de aceptación y la matriz de trazabilidad](./05f-criterios-aceptacion-trazabilidad.md) para que cada operación quede verificable y ninguna regla quede sin implementar.

Para profundizar en RLS, RPC y migraciones, consulta el módulo [03-SUPABASE](../03-SUPABASE/).

---

**Tiempo estimado:** 10-20 minutos por feature
