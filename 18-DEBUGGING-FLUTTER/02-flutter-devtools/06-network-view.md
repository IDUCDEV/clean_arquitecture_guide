# 06 - Network View

## ¿Qué es Network View?

Herramienta para inspeccionar todas las solicitudes HTTP y WebSocket realizadas por tu app Flutter. Permite ver headers, bodies, tiempos de respuesta, y errores.

---

## Network View - Pestañas

| Pestaña | Propósito |
|---------|-----------|
| **HTTP Requests** | Todas las solicitudes HTTP (GET, POST, etc.) |
| **HTTP Events** | WebSocket y Server-Sent Events |
| **Filter** | Filtrar por método, status, tipo |

---

## HTTP Requests

### Lista de requests

```
┌────────────────┬────────────────────────────┬────────┬────────┬──────────┐
│ Method          │ URL                         │ Status │ Size   │ Time     │
├────────────────┼────────────────────────────┼────────┼────────┼──────────┤
│ GET             │ /rest/v1/products           │ 200    │ 12 KB  │ 145 ms   │
│ GET             │ /rest/v1/products?category=  │ 200    │ 4 KB   │ 89 ms    │
│ POST            │ /auth/v1/token              │ 200    │ 0.5 KB │ 234 ms   │
│ GET             │ /storage/v1/object/public/  │ 200    │ 45 KB  │ 567 ms   │
│ POST            │ /rest/v1/rpc/get_user_stats │ 200    │ 1 KB   │ 1234 ms  │
│ GET             │ /rest/v1/orders             │ 401    │ 0.1 KB │ 45 ms    │
└────────────────┴────────────────────────────┴────────┴────────┴──────────┘
```

### Iconos de estado

| Icono | Status | Significado |
|-------|--------|-------------|
| 🟢 | 200-299 | Exitoso |
| 🟡 | 300-399 | Redirect |
| 🔴 | 400-499 | Error cliente |
| 🔴 | 500-599 | Error servidor |

---

## Detalle de request

### Request Headers

```
GET /rest/v1/products HTTP/1.1
Host: xxx.supabase.co
apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
User-Agent: Dart/3.2 (dart:io)
```

### Response Headers

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Range: 0-49/150
X-Request-Id: abc123
Cache-Control: max-age=0
Content-Length: 12345
```

### Response Body (pretty-printed)

```json
[
  {
    "id": 1,
    "name": "Product 1",
    "price": 29.99,
    "category": "electronics",
    "created_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "name": "Product 2",
    "price": 49.99,
    "category": "clothing",
    "created_at": "2024-01-15T11:45:00Z"
  }
]
```

---

## Filtering (Filtros)

### Filtros disponibles

| Filtro | Descripción | Ejemplo |
|--------|-------------|---------|
| **Method** | Filtrar por método HTTP | `method:GET`, `method:POST` |
| **Status** | Filtrar por status code | `status:200`, `status:4xx` |
| **Type** | Filtrar por tipo de recurso | `type:document`, `type:script` |
| **URL** | Buscar en la URL | `products`, `auth` |
| **Content-Type** | Filtrar por content type | `content-type:json` |

### Sintaxis de filtros

```
# Filtros básicos
method:GET
status:200
status:4xx

# Combinar filtros
method:POST status:200
method:GET type:document

# Excluir
method:OPTIONS
-status:200

# Buscar por texto
url:products
content-type:json
```

### Ejemplos de uso

```
# Ver solo errores
status:4xx

# Ver solo llamadas a autenticación
url:auth

# Ver solo POST exitosos
method:POST status:200

# Ver requests de WebSocket
type:websocket
```

---

## Análisis de tiempos

### Timeline de un request

```
POST /auth/v1/token

DNS:      ██░░░░░░░░░░░░░░░░░░░░░░░  12ms
TCP:      ░░██░░░░░░░░░░░░░░░░░░░░░░  15ms
TLS:      ░░░░████░░░░░░░░░░░░░░░░░░  45ms
Request:  ░░░░░░░░░░██░░░░░░░░░░░░░░  8ms
Response: ░░░░░░░░░░░░████████████░░  154ms
Total:    █████████████████████████░░  234ms
```

### Métricas por request

| Métrica | Descripción |
|---------|-------------|
| **DNS** | Resolución de nombre de dominio |
| **TCP** | Conexión TCP |
| **TLS** | Handshake TLS/SSL |
| **Request** | Envío del request |
| **Waiting** | Esperando respuesta del servidor |
| **Response** | Descarga de la respuesta |
| **Total** | Tiempo total |

### Identificando cuellos de botella

| Problema | Métrica afectada | Solución |
|----------|------------------|----------|
| DNS lento | DNS alto | Usar IP directo o DNS cache |
| Conexión lenta | TCP alto | Connection pooling |
| Handshake TLS | TLS alto | Reusar conexiones |
| Servidor lento | Waiting alto | Optimizar backend |
| Payload grande | Response alto | Paginación, compresión |

---

## HTTP Events (WebSocket)

### Lista de eventos

```
┌──────────┬───────────────────────────┬──────────┐
│ Type      │ Event                      │ Data     │
├──────────┼───────────────────────────┼──────────┤
│ receive   │ postgres_changes           │ {...}    │
│ send      │ heartbeat                  │ {}       │
│ receive   │ broadcast                  │ {...}    │
│ error     │ connection_timeout         │ null     │
└──────────┴───────────────────────────┴──────────┘
```

### Detalle de evento WebSocket

```
WebSocket: Realtime Connection

Connected: true
Channel: public:messages
Topic: INSERT

Events:
┌──────────┬────────────────────────────────────┐
│ Time      │ Payload                           │
├──────────┼────────────────────────────────────┤
│ 10:30:01 │ {"type":"INSERT","record":{...}}   │
│ 10:30:05 │ {"type":"UPDATE","record":{...}}   │
│ 10:30:12 │ {"type":"DELETE","old_record":{...}}│
└──────────┴────────────────────────────────────┘
```

---

## debugging con Network View

### Escenario 1: API retorna error 401

**Observación en Network View:**
```
POST /auth/v1/token → 401 Unauthorized

Response Body:
{
  "error": "invalid_grant",
  "message": "Invalid login credentials"
}
```

**Diagnóstico:**
1. Verificar request body: ¿email/password correctos?
2. Verificar API key en headers
3. Verificar si el usuario existe en Supabase

### Escenario 2: Request lento (>1s)

**Observación:**
```
GET /rest/v1/orders?user_id=eq.123 → 3456ms
```

**Diagnóstico:**
1. Verificar tamaño de response (payload)
2. Verificar si hay índices en la tabla
3. Verificar si RLS está causando overhead
4. Considerar paginación

### Escenario 3: Request falla intermitentemente

**Observación:**
```
GET /rest/v1/products → 200 (145ms)
GET /rest/v1/products → 503 (12ms)
GET /rest/v1/products → 200 (167ms)
```

**Diagnóstico:**
1. Verificar rate limiting de Supabase
2. Verificar conexión del dispositivo
3. Verificar si el servidor está bajo carga

---

## Network View vs Debug Console

| Feature | Network View | Debug Console |
|---------|--------------|---------------|
| Ver requests HTTP | ✅ | ❌ |
| Ver WebSocket events | ✅ | ❌ |
| Filtrar por status | ✅ | ❌ |
| Ver tiempos detallados | ✅ | ❌ |
| Ver headers completos | ✅ | ❌ |
| Evaluar expresiones | ❌ | ✅ |
| Imprimir valores | ❌ | ✅ |
| Breakpoints | ❌ | ✅ |

**Recomendación**: Usar Network View para debugging de API, Debug Console para debugging de lógica.

---

## Ejercicios prácticos

### Ejercicio 1: Auditar llamadas de carga inicial

1. Iniciar app con Network View abierto
2. Filtrar solo `type:document`
3. Identificar cuántas llamadas se hacen al iniciar
4. Optimizar: ¿se pueden reducir?

### Ejercicio 2: Debug de Supabase Realtime

1. Conectar a Supabase Realtime
2. Ver eventos WebSocket en Network View
3. Modificar datos en otra pestaña
4. Verificar que los eventos llegan correctamente

### Ejercicio 3: Medir performance de API

1. Hacer 10 llamadas a la misma API
2. Verificar tiempos de respuesta
3. Identificar patrones ( ¿la primera es más lenta? )
4. Documentar findings

---
→ Siguiente: `07-debugger-view.md`
