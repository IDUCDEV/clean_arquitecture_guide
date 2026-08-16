# 10: System Design Básico para Flutter

> System Design es diseñar un sistema completo (no solo una función). En entrevistas Flutter, evalúan si puedes diseñar una app real de forma escalable.

---

## Por qué importa

Como Flutter developer, te preguntan:
- "Diseña un feed de Instagram"
- "Diseña un chat como WhatsApp"
- "Diseña un sistema de notificaciones push"

No es solo código Dart. Es **arquitectura completa**.

---

## Framework de 4 pasos

```
1. CLARIFICAR    → Entender requisitos y restricciones
2. DISEÑAR       → Alto nivel (componentes + datos)
3. PROFUNDIZAR   → Detalles técnicos
4. ESCALAR       → ¿Qué pasa con 1M usuarios?
```

---

## Paso 1: Clarificar

**Preguntas obligatorias:**
- ¿Cuántos usuarios? (determina complejidad)
- ¿Cuántos datos por día? (determina almacenamiento)
- ¿Latencia aceptable? (determina caching)
- ¿Requiere real-time? (determina WebSocket vs polling)

---

## Paso 2: Diseño de Alto Nivel

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Flutter App │────▶│  API Gateway  │────▶│  Backend    │
│  (Frontend)  │     │  (REST/WS)   │     │  (Supabase) │
└─────────────┘     └──────────────┘     └─────────────┘
                                                   │
                                            ┌──────┴──────┐
                                            │  Database   │
                                            │ (PostgreSQL) │
                                            └─────────────┘
```

**Componentes clave:**
- **Cliente:** Flutter app (iOS, Android, Web)
- **API:** REST o WebSocket
- **Backend:** Supabase (auth, DB, storage, functions)
- **Base de datos:** PostgreSQL
- **Cache:** Redis o SharedPreferences local

---

## Paso 3: Profundizar

### Modelado de datos (ejemplo: Instagram feed)

```sql
-- Tabla de posts
CREATE TABLE posts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  image_url TEXT NOT NULL,
  caption TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de likes (muchos a muchos)
CREATE TABLE likes (
  user_id UUID REFERENCES users(id),
  post_id UUID REFERENCES posts(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, post_id)
);

-- Índices para queries frecuentes
CREATE INDEX idx_posts_user ON posts(user_id);
CREATE INDEX idx_posts_created ON posts(created_at DESC);
CREATE INDEX idx_likes_post ON likes(post_id);
```

### Flutter: Feed con pagination

```dart
class FeedCubit extends Cubit<FeedState> {
  final PostRepository _repo;
  static const int _pageSize = 20;

  FeedCubit(this._repo) : super(FeedInitial());

  Future<void> loadInitial() async {
    emit(FeedLoading());
    final posts = await _repo.getPosts(limit: _pageSize, offset: 0);
    emit(FeedLoaded(posts: posts, hasMore: posts.length == _pageSize));
  }

  Future<void> loadMore() async {
    if (state is! FeedLoaded) return;
    final current = state as FeedLoaded;
    final morePosts = await _repo.getPosts(
      limit: _pageSize,
      offset: current.posts.length,
    );
    emit(FeedLoaded(
      posts: [...current.posts, ...morePosts],
      hasMore: morePosts.length == _pageSize,
    ));
  }
}
```

---

## Paso 4: Escalar

### Problemas comunes y soluciones

| Problema | Solución |
|----------|----------|
| Demasiadas consultas | Caching (Redis, local storage) |
| Imágenes lentas | CDN + compression |
| Real-time | WebSocket / Supabase Realtime |
| Base de datos lenta | Índices + read replicas |
| Un servidor saturado | Load balancing |

### Ejemplo: Notificaciones push

```
Supabase Database → Edge Function → Firebase Cloud Messaging → Flutter App
                    (trigger)        (envía push)
```

---

## Template de respuesta en entrevista

```markdown
## 1. Requisitos
- Usuarios: [X]
- Datos por día: [X]
- Latencia: [< X ms]

## 2. Diagrama
[dibujo de componentes]

## 3. Modelado
[tablas SQL + relaciones]

## 4. Flutter
[Cubit/BLoC + Repository]

## 5. Escalabilidad
[caching, CDNs, replicas]
```

---

## Ejemplo resuelto: Diseña un Chat

### 1. Requisitos
- Mensajes en tiempo real
- Historial persistente
- 1:1 y grupal
- 10K usuarios concurrentes

### 2. Modelado

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY,
  is_group BOOLEAN DEFAULT FALSE,
  name TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE messages (
  id UUID PRIMARY KEY,
  conversation_id UUID REFERENCES conversations(id),
  sender_id UUID REFERENCES users(id),
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE conversation_members (
  conversation_id UUID REFERENCES conversations(id),
  user_id UUID REFERENCES users(id),
  PRIMARY KEY (conversation_id, user_id)
);
```

### 3. Flutter

```dart
class ChatCubit extends Cubit<ChatState> {
  final SupabaseClient _supabase;
  late RealtimeChannel _channel;

  ChatCubit(this._supabase) : super(ChatInitial());

  void subscribeToMessages(String conversationId) {
    _channel = _supabase
        .channel('messages:$conversationId')
        .onPostgresChanges(
          event: PostgresInsertEvent,
          schema: 'public',
          table: 'messages',
          filter: PostgresChangeFilter(
            type: PostgresChangeFilterType.eq,
            column: 'conversation_id',
            value: conversationId,
          ),
          callback: (payload) {
            final msg = Message.fromJson(payload.newRecord);
            emit(state.copyWith(messages: [...state.messages, msg]));
          },
        )
        .subscribe();
  }

  @override
  Future<void> close() {
    _supabase.removeChannel(_channel);
    return super.close();
  }
}
```

---

## Errores comunes en entrevistas

| Error | Solución |
|-------|----------|
| Empezar a codificar sin clarificar | Siempre preguntar primero |
| No mencionar escalabilidad | Agregar paso 4 siempre |
| Ignorar edge cases | Mencionar errores y límites |
| Solo REST cuando piden real-time | Mencionar WebSocket/Supabase Realtime |

---

---

> **¿Quieres la versión completa?** Este archivo es el intro de 45 minutos. El módulo **22-DISENIO-SISTEMAS** lo expande con teoría (estimación de escala, cache, realtime, CAP, seguridad, observabilidad), una **plantilla de 10 pasos** y 4 casos integradores resueltos (Feed, Chat, E-commerce, SaaS): [📐 22-DISENIO-SISTEMAS](../22-DISENIO-SISTEMAS/README.md)

**Siguiente:** [11-errores-comunes-patron.md](./11-errores-comunes-patron.md)
