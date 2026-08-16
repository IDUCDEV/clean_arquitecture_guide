# 03: Componentes de Arquitectura

> Los bloques con los que se construye todo sistema escalable. Aprender a *nombrar* cada componente y *justificar* su presencia (o ausencia) es la mitad de un system design.

---

## El mapa completo

```
                    ┌──────────────┐
   Usuario          │     DNS      │  Traduce "miapp.com" → IP
      │             └──────┬───────┘
      ▼                    ▼
  ┌──────────┐     ┌──────────────┐
  │  CDN     │────▶│  Load        │  Reparte tráfico
  │ (media,  │     │  Balancer    │  entre servidores
  │  estático)│    └──────┬───────┘
  └──────────┘           ▼
                 ┌──────────────┐     ┌──────────────────┐
                 │ Reverse Proxy│────▶│  App Layer       │
                 │ (nivel 7)    │     │  (API, servicios)│
                 └──────────────┘     └───────┬──────────┘
                                              ▼
                                    ┌──────────────────┐
                                    │  Database        │
                                    │  (+ replicas,    │
                                    │   cache, queues) │
                                    └──────────────────┘
```

*Componentes tomados del índice de topics del System Design Primer.*

---

## 1. DNS (Domain Name System)

Traduce un nombre (`miapp.com`) a una dirección IP. Es jerárquico y tiene caching en varios niveles (browser, OS, servidores).

**Tipos de registros:**
- **A record** — nombre → IP.
- **CNAME** — nombre → otro nombre.
- **MX** — servidores de correo.

**En el diseño:**
- El DNS introduce un pequeño delay, mitigado por el TTL (time to live) del caching.
- Servicios gestionados: Cloudflare, Route 53. Pueden enrutar por **latency** o **geolocalización** (para servir la región correcta).

---

## 2. CDN (Content Delivery Network)

Red global de proxies que sirve contenido desde el nodo **más cercano al usuario**. Ideal para estáticos: HTML/CSS/JS, fotos, videos.

### Push vs Pull CDN

| | Push CDN | Pull CDN |
|---|---|---|
| Quién sube el contenido | Tú, cuando cambia | El CDN, en la primera request |
| Uso típico | Poco tráfico, contenido que rara vez cambia | Tráfico alto, contenido reciente |
| Trade-off | Maximiza almacenamiento | Minimiza almacenamiento, puede re-pull innecesario |

### En un stack Flutter + Supabase
- Las **imágenes de los posts** van a **Supabase Storage** con CDN/edge de entrega, no a la base de datos (lo calculamos en el archivo 02: 9 TB/año).
- La app apunta a URLs de media, no a endpoints de la API, para ese tráfico.

*Fuente: System Design Primer — "Content delivery network".*

---

## 3. Load Balancer

Distribuye requests entrantes entre varios servidores. Sus beneficios:

- Evita enviar tráfico a servidores no saludables (health checks).
- Evita sobrecargar un recurso.
- Elimina puntos únicos de fallo.
- **SSL termination:** descifra HTTPS para que el backend no lo haga.

### Nivel 4 vs Nivel 7

| | Layer 4 (transport) | Layer 7 (application) |
|---|---|---|
| Decide por | IP origen, IP destino, puerto | Header, mensaje, cookies |
| Tráfico | Adelanta paquetes (NAT) | Termina la conexión, lee, decide, reconecta |
| Ejemplo | LB de red | Nginx, HAProxy (routing por URL) |

### Algoritmos de reparto
- Round robin / weighted round robin
- Least loaded
- Session/cookies (sticky sessions)

*Fuente: System Design Primer — "Load balancer".*

---

## 4. Reverse Proxy (servidor web)

Servidor central que recibe requests y las reenvía a los servidores internos. Diferencia con el LB:

> "A load balancer is useful when you have multiple servers. Often, load balancers route traffic to a set of servers serving the same function. A reverse proxy is useful even with just one web server or application server, providing SSL termination, caching, and security benefits."

**Beneficios:** terminación SSL, caching de respuestas, compresión, mitigación de DDoS.

---

## 5. Application Layer (capa de aplicación)

Donde vive la lógica de negocio. Aquí entra la decisión: **monolito vs microservicios**.

### Microservicios
- Descomponen la app en servicios independientes, cada uno con su propia data.
- Añaden complejidad: **service discovery**, comunicacón entre servicios, datos distribuidos.
- **Regla práctica del primer**: si tu app cabe en un monolito (Supabase cubre auth, DB, storage, realtime en un solo servicio), no empieces con microservicios.

### En el stack del repo
- **Supabase actúa como "Backend as a Service"**: ya te da Auth, Postgres, Storage, Realtime y Edge Functions como componentes del "application layer" gestionado.
- Las **Edge Functions (Deno)** son el lugar para lógica que no debe vivir en el cliente: webhooks, procesamiento, notificaciones.

*Fuente: System Design Primer — "Application layer".*

---

## 6. Service Discovery

Cuando hay muchos servicios, un cliente necesita saber **qué instancia** de qué servicio contactar. Mecanismos:

- **DNS-based:** el cliente consulta un registro y recibe una IP.
- **Service registry:** un registro central (Consul, etcd, ZooKeeper) que guarda instancias vivas.

En Supabase esto es transparente: el cliente habla con el endpoint gestionado y Supabase balancea internamente.

---

## 7. Communication (cómo se comunican)

| Protocolo | Uso típico | Notas |
|---|---|---|
| **REST** | APIs CRUD | Stateless, HTTP, es la base de Supabase REST |
| **RPC** | Llamadas a funciones | Supabase RPC (Postgres functions) |
| **WebSocket** | Realtime bidireccional | Ver archivo 06 |
| **TCP/UDP** | Capa transporte | UDP para baja latencia (voz, video) |

---

## Cómo decidir qué componentes usar

Pregunta guía por componente:

| Componente | ¿Cuándo lo necesito? |
|---|---|
| CDN | Imágenes/videos o usuarios geográficamente dispersos |
| Load Balancer | 2+ instancias de un mismo servicio |
| Reverse Proxy | Un solo servidor y necesitas SSL/cache/compresión |
| Cache (Redis) | Lecturas repetitivas de los mismos datos |
| Message queue | Trabajo pesado que puede esperar (async) |
| Replicas de DB | Carga de lectura alta (ratio L/E alto) |

**No todos los componentes en el diagrama son obligatorios.** Un MVP Flutter + Supabase no necesita un LB propio: Supabase ya lo maneja. El arte está en **justificar cada pieza**.

---

## Fuentes

- [The System Design Primer — Index of system design topics](https://github.com/donnemartin/system-design-primer#index-of-system-design-topics)
- [The System Design Primer — DNS](https://github.com/donnemartin/system-design-primer#domain-name-system)
- [The System Design Primer — CDN](https://github.com/donnemartin/system-design-primer#content-delivery-network)
- [The System Design Primer — Load balancer / Reverse proxy](https://github.com/donnemartin/system-design-primer#load-balancer)
- [The System Design Primer — Application layer](https://github.com/donnemartin/system-design-primer#application-layer)
- [ByteByteGo — Reverse Proxy vs. API Gateway vs. Load Balancer](https://bytebytego.com/guides/reverse-proxy-vs-api-gateway-vs-load-balancer)
- [Supabase — Features](https://supabase.com/docs/guides/getting-started/features)

---

**Siguiente:** [04-modelado-de-datos.md](./04-modelado-de-datos.md)
