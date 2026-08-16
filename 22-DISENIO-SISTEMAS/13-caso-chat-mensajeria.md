# 13: Caso de Estudio — Chat / Mensajería

> Aplicación de la plantilla al diseño de un chat en vivo con Supabase Realtime. Los módulos 05 (realtime) y 10 (offline) se unen aquí en una arquitectura concreta.

---

## Paso 1: Alcance y requerimientos

**Producto:** chat de mensajería 1:1 y grupal.

| Incluido | Fuera de scope (este diseño) |
|---|---|
| Mensajes 1:1 y grupos | Llamadas de voz/video |
| Realtime (WebSocket) | Encrypted E2E avanzado (clave rotativa) |
| Offline + cola de envío | Edición/borrado de mensajes |
| Presencia (online/offline) | Buscador full-text de mensajes |

**No funcionales:** latencia de entrega < 500ms en línea, mensajes **nunca se pierden**, funciona offline y sincroniza al reconectar.

---

## Paso 2: Estimación de escala

| Métrica | Valor |
|---|---|
| Usuarios | 5M MAU, 200K DAU |
| Mensajes por día | ~10M |
| QPS de escritura | ~115 msg/s |
| Conexiones WebSocket activas (pico) | ~50K |
| Storage mensajes/año | ~11 GB de texto |

**Lectura:** es un sistema **write-heavy + realtime**. El cuello de botella es la entrega en vivo, no el almacenamiento.

---

## Paso 3: Modelado de datos

```sql
conversations(id, type, created_at)
conversation_participants(conversation_id, user_id)  -- membresía
messages(id, conversation_id, sender_id, content, created_at)
```

- **Índices:** `messages(conversation_id, created_at)`; `conversation_participants(user_id)`.
- **RLS:** un usuario solo lee mensajes de conversaciones donde **participa** (`auth.uid() IN participant list`).
- **UUIDs como PK** (módulo 03): necesarios para colisiones de offline.

---

## Paso 4-5: Arquitectura de alto nivel

```
  Usuario A                                   Usuario B
┌──────────┐                              ┌──────────┐
│  App A   │                              │  App B   │
│  cola +  │                              │  cola +  │
│  cache   │                              │  cache   │
└────┬─────┘                              └────▲─────┘
     │ 1. insert (REST/RPC)                   │
     ▼                                        │ 3. WebSocket push
┌─────────────────────────────────────────────┴─────┐
│               Supabase                             │
│   ┌─────────────┐   WAL   ┌────────────┐           │
│   │   Postgres  │────────▶│  Realtime  │───────────┘
│   │  messages   │         │ (WebSocket)│
│   └─────────────┘         └────────────┘
└─────────────────────────────────────────────────────┘
```

**Componentes:**
1. **App (Flutter):** cache local (Isar) + cola de escrituras offline.
2. **Supabase Postgres:** fuente de verdad; RLS por participación.
3. **Supabase Realtime:** Postgres Changes + Presence.
4. **API/RPC:** `send_message` como transacción validada.

---

## Paso 6: Decisiones de diseño con trade-offs

| Decisión | Por qué | Trade-off aceptado |
|---|---|---|
| Realtime/WebSocket (archivo 06) | Latencia < 500ms y bidireccional | Gestión de conexiones, límites |
| Insert en Postgres como "canal" | Un solo mecanismo de persistencia + entrega | Realtime depende de la DB |
| Offline + cola con optimistic UI | No perder mensajes sin red | Complejidad de sincronización |
| Presence con Realtime | Saber quién está en línea sin polling | Solo muestra en sesiones activas |
| UUIDs + `updated_at` | Sincronización sin colisiones (LWW) | IDs más largos |

### Flujo de envío de mensaje (online)
```
1. App muestra el mensaje al instante (optimistic UI) y lo guarda en cola
2. App inserta en Postgres vía RPC (RLS valida participación)
3. Postgres persiste → Realtime detecta el insert por WAL
4. Realtime empuja a todos los suscritos de la conversación (App B)
5. App B recibe y actualiza su UI; App A marca su mensaje como "synced"
```

### Flujo de envío (offline)
```
1. Sin red: mensaje queda en cola local, marcado "pending"
2. Al reconectar: cola se envía en orden con retries + backoff
3. Éxito → "synced"; fallo → reintentos con límite y alerta
```

### Conflicto (LWW)
```
Dos devices editando/creando el mismo mensaje → gana el que tenga
updated_at más reciente. Definido ANTES de implementar (archivo 10).
```

---

## Paso 7: Consistencia y disponibilidad

- **Modelo:** strong en la entrega de un mensaje (insert transaccional), eventual en el orden percibido por cada cliente (caché local).
- **SLA:** entrega online 99.9%; offline eventual (sin SLA de tiempo).
- **Patrones:** retries + backoff en cola, reconnect automático del WebSocket, cache local como única UI en modo offline.

**Justificación CAP:** el chat es **AP** en la entrega percibida (siempre responde, orden eventual) pero el mensaje **no se pierde** — la persistencia es fuerte en el servidor.

---

## Paso 8-9: Seguridad y observabilidad

**Seguridad:**
- RLS: leer mensajes **solo** si participas en la conversación (crítico en chats).
- Presence/Postgres Changes con RLS: no exponer mensajes de chats ajenos.
- HTTPS + tokens en secure storage.

**Observabilidad:**
| Métrica | Alerta |
|---|---|
| Latencia de entrega > 500ms | Revisar Realtime/DB |
| Mensajes en cola creciendo | Revisar conectividad/API |
| Error rate de send > 2% | Revisar RPC/RLS |
| Conexiones Realtime cercanas al límite | Reducir suscripciones por cliente |

---

## Paso 10: Riesgos y evolución

| Riesgo | Mitigación |
|---|---|
| Escalar WebSockets (500K+ conexiones) | Capa de gateway de websockets / servicios dedicados |
| Cola offline gigante al reconectar | Sincronizar por lotes + delta sync |
| Realtime filtra mensajes ajenos | RLS en los canales; test de aislamiento |
| Orden de mensajes en multi-device | Clocks monotónicos + LWW por `updated_at` |

---

## Fuentes del caso

- [Supabase Docs — Realtime Postgres Changes](https://supabase.com/docs/guides/realtime/postgres-changes)
- [Supabase Docs — Realtime Presence](https://supabase.com/docs/guides/realtime/presence)
- [ByteByteGo — Design a Real-time Chat System](https://bytebytego.com/guides/design-chat-system)
- Archivos 06 y 10 de este módulo.

---

**Siguiente:** [14-caso-ecommerce-escalable.md](./14-caso-ecommerce-escalable.md)
