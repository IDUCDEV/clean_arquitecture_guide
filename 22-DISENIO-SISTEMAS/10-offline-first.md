# 10: Offline-First y Sincronización

> Cómo diseñar la app para que funcione sin red y se sincronice al reconectar. El archivo donde el patrón offline-first (del repositorio) se conecta con el system design.

---

## El problema de diseñar "para la nube"

Las arquitecturas clásicas asumen red disponible. Pero en Flutter móvil **la red no es confiable**: elevadores, metro, avión, batería baja. Si la app muere sin conexión, pierdes usuarios.

**Offline-first** = la app funciona bien **sin red** como estado por defecto, y la nube es la capa de sincronización.

---

## Los 4 niveles de tolerancia offline

| Nivel | Qué guarda | Ejemplo |
|---|---|---|
| 1. Lectura offline | Caché de lo ya visto | Feed ya cargado |
| 2. Escrituras offline | Acciones en cola local | Like, mensaje, borrador |
| 3. Sync en background | Cola se envía al reconectar | Mensajes enviados después |
| 4. Conflict resolution | Ambos lados editaron lo mismo | Editar mismo post en 2 devices |

---

## Estrategias de sincronización (con el sistema en mente)

### 1. Optimistic UI + cola de escrituras (recomendada para MVP)
```
1. Usuario da like → se guarda en cola local + UI actualiza al instante
2. Sin red: queda en cola con estado "pending"
3. Al reconectar: se envía a la API en orden
4. Éxito → se marca "synced"; fallo → retry con backoff
```

### 2. Estado: local-first, sync as a service
- La DB local (Isar) es la **fuente de verdad para la UI**.
- La nube (Supabase) es la fuente de verdad **del sistema**.
- La sincronización sincroniza estados, no "la base de datos".

### 3. Conflicto: quién gana
- **Last-write-wins (LWW):** gana el último `updated_at`. Simple, pierde trabajo.
- **Merge manual:** ambos cambios se conservan y el usuario decide.
- **Por campo:** el último cambio por cada campo.

**Regla de diseño:** define la política de conflictos **antes** de implementar la sincronización. Un conflicto no manejado = datos perdidos silenciosamente.

---

## Sincronización con Supabase

La sincronización del offline-first se apoya en los mecanismos ya vistos:

| Mecanismo | Rol en sync |
|---|---|
| Realtime (archivo 06) | Empujar cambios remotos cuando hay red |
| RLS (módulo 03) | El servidor decide qué sincronizar según el usuario |
| UUIDs como PK (módulo 03) | IDs no dependen del orden de creación → sin colisiones de sync |
| `updated_at` | Base para LWW y delta sync |

### El loop de sincronización
```
┌──────────────────────────────────────────────────┐
│  App (Flutter)                                    │
│   ┌───────────┐   escrituras    ┌─────────────┐   │
│   │  Cola     │────────────────▶│  API/DB     │   │
│   │  local    │◀─ status ──────┘  (Supabase)  │   │
│   └───────────┘                                │   │
│        ▲                                        │   │
│        │  Realtime push (cambios de otros)      │   │
│        └────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

---

## La decisión de consistencia (conecta con el archivo 07)

- Con **red disponible:** strong consistency vía Supabase/RLS para datos críticos.
- Con **sin red:** consistencia local inmediata (optimistic) + eventual al sincronizar.

> *"You can't have both strong consistency and high availability under network partitions."* — CAP (archivo 07).

La app offline-first es **AP por diseño**: disponible siempre, consistente eventualmente.

---

## Detección de conectividad y scheduling

- Monitorear conectividad (internet_connection_checker) para saber cuándo flushear la cola.
- **Ejecutar sync al reconectar**, no en loops ciegos.
- Respetar **batería/banda**: no sincronizar media gigante con datos celulares.
- Tareas en segundo plano: ejecutores periódicos en Flutter (workmanager) — mantener simple en MVP.

---

## Errores comunes del diseño offline

| Error | Fix |
|---|---|
| Asumir red siempre disponible | Asumir lo contrario: offline-first |
| IDs autoincrementales en sync | UUIDs como PK (módulo 03) |
| Sin política de conflictos | Definir LWW / merge por campo antes |
| Cola infinita sin backoff | Retries con backoff + límites |
| Sincronizar todo el tiempo | Sincronizar al reconectar + delta sync |
| Estado duplicado (UI y sync separados) | Un solo estado (local-first) con cola |

---

## Fuentes

- [Supabase Docs — Offline support (Dart/Flutter)](https://supabase.com/docs/guides/realtime/offline)
- [Redis/DDIA — Conflict resolution](https://dataintensive.net/) (capítulo sobre multileader y conflictos)
- [ByteByteGo — Offline-First Apps](https://bytebytego.com/guides/offline-first-apps)
- Patrón del repositorio: módulo 04 (cache local Isar + sync)

---

**Siguiente:** [11-plantilla-diseno-sistema.md](./11-plantilla-diseno-sistema.md)
