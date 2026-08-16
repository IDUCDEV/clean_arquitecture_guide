# 06: Realtime y Streaming

> Cómo elegir entre polling, WebSocket y Server-Sent Events, y cómo encaja Supabase Realtime. La decisión de realtime cambia el diseño completo del backend.

---

## Las 3 opciones de comunicación en tiempo real

| Técnica | Dirección | Cuándo | Ejemplo |
|---|---|---|---|
| **Polling** | Cliente → servidor (pregunta) | Latencias de segundos, simple | Lista que se refresca cada 30s |
| **Long polling** | Cliente → servidor (mantiene abierta hasta respuesta) | Necesito menos polling, sin websocket | Notificaciones simples |
| **WebSocket** | Bidireccional, full-duplex | Realtime de verdad, baja latencia | Chat, presencia, live updates |
| **SSE (Server-Sent Events)** | Servidor → cliente (unidireccional) | Updates unidireccionales | Feed que se actualiza solo |

*Fuente: ByteByteGo — "Short/long polling, SSE, WebSocket".*

### Trade-offs

- **Polling:** simple y funciona en cualquier servidor, pero desperdicia requests (N peticiones por unidad de tiempo aunque no haya datos).
- **WebSocket:** conexión persistente bidireccional, baja latencia; más complejo (manejo de conexiones, reconnection, heartbeats), no funciona tras algunos proxies.
- **SSE:** más simple que WebSocket (HTTP normal, auto-reconnect), pero unidireccional.

---

## Asincronía: la pieza que falta en muchos diseños

No todo tiene que ser síncrono. El System Design Primer lista dos patrones clave:

### Message queues
- El productor encola un mensaje; el consumidor lo procesa cuando puede.
- **Desacoplan** componentes: si el consumidor cae, el mensaje espera.
- Ejemplo: *"cuando un usuario sube un video, se encola la tarea de transcodificación"*.

### Task queues
- Colas de trabajo pesado (ej. enviar emails, generar thumbnails).
- **Back pressure:** si el consumidor va más lento que el productor, la cola crece — hay que monitorear su tamaño.

**En Supabase:** las **Edge Functions** + colas/scheduling son el mecanismo para trabajo asíncrono (notificaciones, procesamiento). El trigger clásico del repo: *insert en la DB → trigger → Edge Function → notificación*.

---

## Supabase Realtime (oficial)

Supabase provee Realtime como servicio gestionado. Los tres canales documentados en la documentación oficial:

1. **Postgres Changes:** escuchar inserts/updates/deletes en una tabla y recibir el cambio en la app.
2. **Broadcast:** enviar mensajes arbitrarios entre clientes.
3. **Presence:** saber quién está conectado (útil para chats y presencia).

### Arquitectura de Supabase Realtime

*Fuente: [Supabase Docs — Realtime architecture](https://supabase.com/docs/guides/realtime/architecture).*

```
   Postgres ──(WAL)──▶ Realtime ──(WebSocket)──▶ Flutter App
   (insert/update)     (detecta cambios)         (recibe en vivo)
```

- La app abre un **WebSocket** a Supabase Realtime.
- El servidor escucha los cambios de Postgres vía el **Write-Ahead Log (WAL)** y los empuja a los clientes suscritos.
- Se puede **filtrar** por evento (INSERT/UPDATE/DELETE), schema, tabla y columnas.

### Postgres Changes en la práctica (ejemplo de chat del repo)

```dart
final channel = supabase
    .channel('messages:room-1')
    .onPostgresChanges(
      event: PostgresChangeEvent.insert,
      schema: 'public',
      table: 'messages',
      callback: (payload) {
        final message = Message.fromJson(payload.newRecord);
        // emitir nuevo estado en el Cubit
      },
    )
    .subscribe();
```

*Fuente: [Supabase Docs — Realtime Postgres Changes](https://supabase.com/docs/guides/realtime/postgres-changes).*

### Trade-offs de usar Supabase Realtime

| Pros | Contras |
|---|---|
| No gestionas WebSocket servers | Límites de conexiones por plan |
| Se integra con RLS (solo ves lo autorizado) | Todo el tráfico pasa por Supabase |
| Postgres como fuente de verdad | Para broadcast masivo a millones, arquitectura custom |

---

## Arquitectura de chat con realtime (resumen de diseño)

```
  ┌──────────────┐   WebSocket    ┌─────────────────┐   WAL    ┌─────────┐
  │  Flutter App  │◀──────────────│ Supabase Realtime│◀────────│ Postgres│
  │  (Cubit +    │               └─────────────────┘          │ messages│
  │   channel)    │                                            └─────────┘
  └──────────────┘
```

1. App suscribe al channel `messages:conversation_id` (con filtro de RLS).
2. Usuario envía → **insert** en Postgres (vía Supabase REST/RPC).
3. Realtime detecta el cambio por WAL y lo empuja a todos los suscritos de la conversación.
4. El Cubit emite el nuevo mensaje → la UI se actualiza sola.

**Decisión de diseño a defender:** elegimos WebSocket (via Realtime) porque el caso de uso es *chat en vivo* (requiere latencia < segundos y bidireccional). Para un feed no-crítico, polling + refresh sería más barato y suficiente.

---

## Árbol de decisión realtime

```
¿La actualización debe verse en < 1-2s?
 ├─ No → Polling con refresh (ej. feed cada 30s)
 ├─ Sí → ¿Unidireccional (servidor→cliente)?
 │        ├─ Sí → SSE / Realtime con broadcast
 │        └─ No → ¿Bidireccional y baja latencia?
 │                ├─ Sí → WebSocket (Supabase Realtime)
 │                └─ No → Long polling
```

---

## Fuentes

- [Supabase Docs — Realtime Architecture](https://supabase.com/docs/guides/realtime/architecture)
- [Supabase Docs — Realtime Postgres Changes](https://supabase.com/docs/guides/realtime/postgres-changes)
- [The System Design Primer — Asynchronism](https://github.com/donnemartin/system-design-primer#asynchronism)
- [ByteByteGo — Short/long polling, SSE, WebSocket](https://bytebytego.com/guides/shortlong-polling-sse-websocket)

---

**Siguiente:** [07-escalabilidad-alta-disponibilidad.md](./07-escalabilidad-alta-disponibilidad.md)
