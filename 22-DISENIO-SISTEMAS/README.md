# 22 - Diseño de Sistemas (System Design)

> Aprende a diseñar sistemas completos y escalables — no solo código. Desde los fundamentos y la estimación de escala hasta la arquitectura de un sistema con Flutter + Supabase listo para producción.

---

## 📋 Índice

| # | Archivo | Descripción |
|---|---------|-------------|
| 00 | [Fundamentos de System Design](./00-fundamentos-system-design.md) | Qué es, atributos clave (reliability, scalability, maintainability) y en qué se diferencia de Clean Architecture |
| 01 | [Clarificar Requisitos](./01-clarificar-requisitos.md) | Framework de clarificación: usuarios, casos de uso, restricciones y suposiciones |
| 02 | [Estimación de Escala](./02-estimacion-de-escala.md) | Cálculo de QPS, almacenamiento y ancho de banda (back-of-the-envelope) |
| 03 | [Componentes de Arquitectura](./03-componentes-arquitectura.md) | DNS, CDN, Load Balancer, Reverse Proxy, Application Layer, Microservicios |
| 04 | [Modelado de Datos](./04-modelado-de-datos.md) | Diseño de esquemas a escala: índices, replicación, sharding, denormalización |
| 05 | [Cache y Rendimiento](./05-cache-y-rendimiento.md) | Estrategias de caching (cache-aside, write-through, etc.) y latencia vs throughput |
| 06 | [Realtime y Streaming](./06-realtime-y-streaming.md) | Polling vs WebSocket vs SSE, Supabase Realtime, asincronía |
| 07 | [Escalabilidad y Alta Disponibilidad](./07-escalabilidad-alta-disponibilidad.md) | Scaling vertical/horizontal, CAP theorem, disponibilidad en números |
| 08 | [Seguridad en el Diseño](./08-seguridad-en-diseno.md) | RLS, Auth, rate limiting, API keys y defensa en profundidad |
| 09 | [Observabilidad y Monitoreo](./09-observabilidad-monitoreo.md) | Logs, métricas, trazabilidad y alertas (SLI/SLO) |
| 10 | [Offline-First](./10-offline-first.md) | Sincronización, conflictos y arquitectura offline con Supabase |
| 11 | [Plantilla de Diseño de Sistemas](./11-plantilla-diseno-sistema.md) | PLANTILLA reutilizable para diseñar cualquier sistema paso a paso |
| 12 | [Caso: Feed de Red Social](./12-caso-feed-red-social.md) | Caso integrador: feed con cache, paginación y realtime |
| 13 | [Caso: Chat / Mensajería](./13-caso-chat-mensajeria.md) | Caso integrador: chat 1:1 y grupal con realtime |
| 14 | [Caso: E-commerce Escalable](./14-caso-ecommerce-escalable.md) | Caso integrador: catálogo, carrito, pagos e inventario |
| 15 | [Caso: SaaS Multi-tenant](./15-caso-saas-multi-tenant.md) | Caso integrador: multi-tenant con RLS por tenant |
| 16 | [Ejercicios de Práctica](./16-ejercicios-practica.md) | Ejercicios progresivos con soluciones guiadas + template de entrevista |
| 17 | [Recursos Externos](./17-recursos-externos.md) | Libros, cursos y repositorios verificados para profundizar |
| — | [Bibliografía y Fuentes](./BIBLIOGRAFIA.md) | Fuentes reales que fundamentan cada decisión del módulo |

---

## 🎯 Objetivo del módulo

Los módulos anteriores te enseñaron a organizar **código** (01 Clean Architecture) y a diseñar **features** (02 Spec Driven Development). Este módulo te enseña a diseñar el **sistema completo**: la app Flutter, el backend, la base de datos, la red y la infraestructura que los conecta, y cómo todo eso se comporta cuando lo usan cientos de miles de usuarios.

Al terminar sabrás:

- Pensar en **términos de componentes** (cliente, gateway, backend, DB, cache, CDN) en vez de solo archivos.
- **Estimar** cuánta capacidad necesitas: requests por segundo, almacenamiento y ancho de banda.
- Diseñar **esquemas de datos** que escalen y elegir estrategias de **caching** y **replicación**.
- Tomar decisiones con **trade-offs** explícitos (todo en system design es un trade-off).
- Aplicar todo esto a un **stack real Flutter + Supabase**.

---

## Ruta de aprendizaje sugerida

```
Tiempo estimado: 25-35 horas

1.  Leer 00-fundamentos-system-design.md      (30 min)   ← Qué es y atributos clave
2.  Leer 01-clarificar-requisitos.md          (45 min)   ← El paso que la gente salta
3.  Leer 02-estimacion-de-escala.md           (60 min)   ← Cálculos back-of-the-envelope
4.  Leer 03-componentes-arquitectura.md       (90 min)   ← DNS, CDN, LB, app layer
5.  Leer 04-modelado-de-datos.md              (90 min)   ← Replicación, sharding, índices
6.  Leer 05-cache-y-rendimiento.md            (60 min)   ← Estrategias de caching
7.  Leer 06-realtime-y-streaming.md           (60 min)   ← WebSocket, polling, Supabase Realtime
8.  Leer 07-escalabilidad-alta-disponibilidad.md (60 min) ← CAP, scaling, números de 9s
9.  Leer 08-seguridad-en-diseno.md            (45 min)   ← RLS, Auth, rate limiting
10. Leer 09-observabilidad-monitoreo.md       (45 min)   ← Logs, métricas, alertas
11. Leer 10-offline-first.md                  (60 min)   ← Sync y conflictos
12. Usar 11-plantilla-diseno-sistema.md       (60 min)   ← Tu checklist de diseño
13. Estudiar casos 12-15 (Feed, Chat, E-commerce, SaaS)  (6-8h) ← Aplicar todo
14. Practicar con 16-ejercicios-practica.md   (5-10h)    ← Ejecutar sin ayuda
15. Consultar 17-recursos-externos.md         (15 min)   ← Para seguir profundizando
```

---

## Relación con otros módulos

| Módulo | Relación |
|--------|----------|
| **01-CLEAN-ARCHITECTURE** | Complementario. Clean Arch organiza el código interno de la app (escala micro); System Design organiza el sistema completo (escala macro). |
| **02-SPEC-DRIVEN-DEVELOPMENT** | Complementario. El SDD define *qué construir* (specs, requisitos, deltas); System Design decide *cómo se sostiene* a escala. |
| **03-SUPABASE** | Base técnica. Este módulo diseña usando Supabase (Postgres, Auth, Storage, Realtime, Edge Functions) y lo cita como infraestructura. |
| **04-ALMACENAMIENTO-LOCAL** | Necesario para el diseño offline-first (archivo 10). |
| **06-NIVEL-EXPERTO/04** | Streams y real-time en Flutter, usados en el diseño de chat y feeds. |
| **19-MONITOREO-PRODUCCION** | Observabilidad en producción (archivo 09 lo enlaza). |
| **20-RESOLUCION-PROBLEMAS-ALGORITMOS** | Predecesor conceptual: su `10-system-design-basico.md` es el intro de 45 min; este módulo es la versión completa. |
| **13-EDGE-FUNCTIONS-DENO** | Edge Functions como pieza de arquitectura serverless (realtime, notificaciones). |

---

## ¿Cuándo usar esta guía?

- Tienes una **entrevista de system design** (móvil o full-stack) y necesitas un proceso estructurado.
- Tu app Flutter ya no cabe en "una tabla y una pantalla" y necesitas decidir **arquitectura de backend y datos**.
- Quieres saber **cuánto costaría y aguantaría** tu sistema con miles o millones de usuarios.
- Necesitas **justificar decisiones** de infraestructura ante un equipo o un cliente.

---

**Siguiente:** [00-fundamentos-system-design.md](./00-fundamentos-system-design.md)

**Nivel:** Intermedio a Avanzado  
**Tiempo estimado:** 25-35 horas  
**Prerrequisitos:** Módulos 01, 02 y 03 (Clean Architecture, Diseño de Features y Supabase)
