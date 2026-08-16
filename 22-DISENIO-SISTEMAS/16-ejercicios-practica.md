# 16: Ejercicios de Práctica

> Ejercicios progresivos para interiorizar el system design: de problemas cortos a casos completos con la plantilla del archivo 11.

---

## Nivel 1: Conceptos rápidos (5 min c/u)

1. Explica **latencia vs throughput** con un ejemplo de una cafetería.
2. Dada una tabla de `posts` con 50M de filas, ¿qué dos índices crearías primero y por qué?
3. ¿Cuándo elegirías **SQL** sobre **NoSQL**? Da un caso donde NoSQL gane.
4. Dibuja de memoria las diferencias entre **master-slave** y **master-master**.
5. ¿Qué estrategia de caché usarías para un feed y por qué?
6. Explica **CAP** con las letras y un ejemplo de cada par.
7. ¿Qué es el *cache stampede* y cómo lo mitigas?
8. Diferencia **autenticación** vs **autorización** con un ejemplo de RLS.
9. ¿Cuándo usarías **long polling** en vez de **WebSocket**?
10. Define los 3 pilares de la observabilidad y qué pregunta responde cada uno.

---

## Nivel 2: Decisiones con trade-offs (10 min c/u)

1. **Feed:** ¿precomputar el timeline (fanout on write) o ensamblar al leer (fanout on read)? ¿Qué métricas te harían cambiar de opción?
2. **Chat:** ¿guardar mensajes en Postgres y emitir por Realtime, o usar un message broker? ¿Dónde está la fuente de verdad?
3. **E-commerce:** un producto con 1 unidad en stock. Dos usuarios compran a la vez. Diseña la secuencia que evita el oversell.
4. **SaaS:** si un tenant empieza a hacer queries que saturan la DB, ¿qué 3 medidas aplicas y en qué orden?
5. **Offline:** diseña la cola de sincronización de likes. ¿Cómo evitas re-envíos duplicados?

---

## Nivel 3: Mini-casos (15-20 min c/u) — usa la plantilla del archivo 11

### Caso A: App de recordatorios con cuentas
- 1M usuarios, notificaciones push, sincronización multi-device.
- **Extras:** latencia de push < 30s, offline obligatorio, RLS para aislamiento por usuario.

### Caso B: Plataforma de encuestas en vivo
- Encuestas con resultados en tiempo real mientras el público vota.
- **Extras:** 100K votos en 10 min, resultados via realtime, sin sobrecargar la DB con writes individuales (agrega en batch).

### Caso C: SaaS de inventario multi-tenant
- Múltiples comercios gestionan stock y órdenes.
- **Extras:** aislamiento estricto entre tenants, inventario con consistencia fuerte, reportes (read-heavy).

---

## Nivel 4: Casos completos (45-60 min) — con checklist

Diseña (plantilla completa del archivo 11) uno de estos:

### 1. Instagram/feed con videos cortos
Incluye: feed, likes, comentarios, media. Extras: ranking del feed, recomendación, offline.

### 2. WhatsApp/Telegram
Incluye: 1:1, grupos, realtime, offline, presencia. Extras: edición de mensajes, media en mensajes.

### 3. E-commerce con flash sales
Incluye: catálogo, carrito, checkout, stock. Extras: 10× tráfico en minutos, colas, idempotencia.

### 4. Notion/Trello multi-tenant
Incluye: orgs, permisos por rol, proyectos. Extras: aislamiento RLS, auditoría, migraciones de esquema.

**Checklist obligatorio:**
- [ ] Alcance + fuera de scope
- [ ] QPS, storage, ratios estimados
- [ ] Diagrama de alto nivel
- [ ] Modelo de datos con índices y RLS
- [ ] 3+ decisiones con trade-offs
- [ ] Consistencia/disponibilidad (CAP) declarada
- [ ] Seguridad y observabilidad
- [ ] 3 riesgos + mitigaciones

---

## Nivel 5: Auto-entrevista (modo entrevistador)

Graba tu respuesta de 45 min a un caso y evalúate:

1. ¿Clarifiqué el alcance antes de diseñar? ✅/❌
2. ¿Estimé números antes de dibujar? ✅/❌
3. ¿Justifiqué cada decisión con un trade-off? ✅/❌
4. ¿Declaré CAP/consistencia explícitamente? ✅/❌
5. ¿Mencioné seguridad y observabilidad sin que me lo pidan? ✅/❌
6. ¿Cerré con riesgos y evolución? ✅/❌

**Métricas de mejora:** por cada caso resuelto, intenta reducir el tiempo de los pasos 1-2 a < 5 min (son los que más se repiten en entrevistas).

---

## Fuentes para corregir

- [The System Design Primer — Solutions](https://github.com/donnemartin/system-design-primer#system-design-topics-start-here)
- [System Design Interview — Alex Xu](https://www.amazon.com/System-Design-Interview-Insiders-Guide/dp/1736049119)
- [ByteByteGo — System Design interview problems](https://bytebytego.com/blog/system-design-interview-questions)

---

**Siguiente:** [17-recursos-externos.md](./17-recursos-externos.md)
