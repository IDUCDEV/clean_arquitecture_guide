# 12: Caso de Estudio — Feed de Red Social

> Aplicación de la plantilla (archivo 11) al diseño del feed del proyecto del repositorio. Datos del archivo 02, cache del 05 y realtime del 06, unificados en una arquitectura defendible.

---

## Paso 1: Alcance y requerimientos

**Producto:** feed de fotos estilo Instagram (el feature del repositorio).

| | Fuera de scope (este diseño) |
|---|---|
| Publicar posts | ✅ Editar/borrar, stories, reels, monetización, followers graph |
| Ver feed propio | ✅ Notificaciones push, explore page |
| Likes | ✅ Comentarios anidados, DMs |

**Requerimientos no funcionales:** disponibilidad alta para lectura, latencia percibida < 300ms, funciona offline.

---

## Paso 2: Estimación de escala

Del archivo 02 (resumen):

| Métrica | Valor |
|---|---|
| Usuarios | 10M MAU, ~500K DAU |
| QPS de lectura (feed) | ~1.7K en pico |
| QPS de escritura (posts + likes) | ~17 |
| Ratio lectura/escritura | ~10:1 |
| Storage anual | ~2.7 TB de media |

**Lectura del diseño:** es un sistema **read-heavy**. Toda la arquitectura se optimiza para lecturas rápidas con escrituras eventuales.

---

## Paso 3: Modelado de datos

Entidades principales:

```sql
users(id, username, avatar_url)
posts(id, user_id → users, image_url, caption, created_at)
likes(user_id, post_id)            -- tabla puente
```

- **Índices:** `posts(user_id, created_at DESC)`, `likes(post_id)`.
- **RLS:** lecturas públicas (`anon` puede SELECT); escrituras solo dueño (`auth.uid() = user_id`).
- **Elección:** Postgres/SQL por las relaciones posts↔users↔likes y transacciones de escritura.

---

## Paso 4-5: Arquitectura de alto nivel

```
┌─────────┐          ┌────────────────────────────────────┐
│  Flutter│          │            Supabase                 │
│   App   │          │  ┌─────────┐  ┌─────────────────┐   │
│  cache  │─ HTTPS ─▶│  │  API/   │──▶│  Postgres      │   │
│  (Isar) │◀─────────│  │  Auth   │  │  (RLS + índices)│   │
└─────────┘  Realtime│  └─────────┘  └───────┬─────────┘   │
        ▲            │  ┌─────────┐          │WAL          │
        │            │  │  Cache  │◀─────────┘             │
   ┌────┴────┐       │  │  feed   │         Realtime       │
   │  CDN    │       │  └─────────┘                        │
   │ media   │       └────────────────────────────────────┘
   └─────────┘
```

**Componentes:**
1. **App (Flutter):** cache local Isar de la última página del feed (archivo 10).
2. **Supabase API + Auth:** lectura del feed, publicación, likes.
3. **Postgres:** fuente de verdad; RLS autoriza por fila.
4. **Cache (Redis):** feed ensamblado por usuario.
5. **CDN:** media (imágenes del feed).
6. **Realtime:** (opcional en feed) likes que llegan en vivo.

---

## Paso 6: Decisiones de diseño con trade-offs

| Decisión | Por qué | Trade-off aceptado |
|---|---|---|
| Cache-aside en el feed (archivo 05) | Lecturas 10:1, feed ensamblado caro | Primer acceso tras expiración es lento |
| Postgres como fuente de verdad | Consistencia fuerte + RLS nativo | Escala menor que NoSQL puro |
| CDN para media | Latencia global de imágenes | TTL e invalidación por borrado |
| Offline-first con cache local | App útil sin red (archivo 10) | Sincronización = complejidad extra |
| Contadores eventuales | Likes no críticos en tiempo real | Valor de likes puede quedar desfasado |

### El flujo del feed (leer)
```
1. App pide página de feed
2. ¿Cache local tiene y es fresca? → devuelve (offline)
3. Si no → GET /feed (Supabase)
4. ¿Redis tiene el feed ensamblado? → devuelve
5. Si no → Postgres ensambla joins → se guarda en Redis → devuelve
6. La app guarda en Isar para la próxima
```

### El flujo de publicar (escribir)
```
1. Usuario publica → insert en Postgres (RLS valida dueño)
2. Se invalida el cache del feed del autor (write-through)
3. Media sube a Storage → CDN invalida la versión vieja
4. Realtime (opcional) avisa a seguidores conectados
```

---

## Paso 7: Consistencia y disponibilidad

- **Modelo:** fuerte en escritura (Postgres transaccional), eventual en lecturas (cache + Realtime).
- **SLA:** lectura 99.9%, escritura 99.9% (nueves del archivo 07).
- **Patrones:** retries + backoff en la app, cache local como fallback sin red.

**Justificación CAP:** el feed prioriza **AP** (siempre responde, eventualmente consistente) porque una foto "unos segundos tarde" no es crítico. El *post* en sí usa strong consistency para no perder publicaciones.

---

## Paso 8-9: Seguridad y observabilidad

**Seguridad:**
- HTTPS en todo, tokens en secure storage.
- RLS deny-by-default; lecturas públicas solo del feed público.
- Service role key solo en backend/Edge Functions.

**Observabilidad (lo mínimo que mide):**
| Métrica | Alerta |
|---|---|
| Error rate del feed > 5% | Revisar query/Edge Function |
| Latencia p95 del feed > 500ms | Revisar cache/Redis |
| Falla de escrituras | Backoff + alerta |
| Cache miss rate alto | Revisar TTL y prefetch |

---

## Paso 10: Riesgos y evolución

| Riesgo | Mitigación |
|---|---|
| Crecimiento a 100M MAU | Replicas de lectura, particionado por usuario |
| Media ocupa mucho storage/CDN | Compresión, jerarquía de cache media |
| Feed global (seguir a todos) | Precomputar timeline (fanout on write) |
| Saturar Postgres con joins | Denormalización + materialized views |

---

## Fuentes del caso

- [The System Design Primer — Example: designing a social news feed](https://github.com/donnemartin/system-design-primer#designing-a-social-news-feed)
- [ByteByteGo — Design Facebook/Instagram Feed](https://bytebytego.com/guides/design-instagram-feed)
- Archivos 02, 04, 05, 06 y 10 de este módulo.

---

**Siguiente:** [13-caso-chat-mensajeria.md](./13-caso-chat-mensajeria.md)
