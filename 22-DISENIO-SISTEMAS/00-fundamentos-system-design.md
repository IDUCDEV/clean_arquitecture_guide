# 00: Fundamentos de System Design

> System Design es el proceso de definir la **arquitectura, las interfaces y los datos** de un sistema completo para que satisfaga requisitos funcionales y no funcionales específicos.

---

## ¿Qué es System Design?

En el módulo 01 aprendiste a organizar **código** en capas. System Design opera a otra escala: no diseñas una clase, diseñas **el sistema entero** — la app móvil, el backend, la base de datos, la red, la caché y la infraestructura que los sostiene.

Un sistema está bien diseñado cuando es **reliable (confiable), scalable (escalable) y maintainable (mantenible)**. Estos tres atributos son el marco que usa *Designing Data-Intensive Applications* (Kleppmann) para evaluar cualquier sistema de datos.

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA COMPLETO                         │
│                                                             │
│  ┌──────────┐     ┌─────────────┐     ┌─────────────────┐  │
│  │ Flutter  │────▶│  API/Realtime│────▶│    Supabase     │  │
│  │ App      │◀────│  Gateway    │◀────│  (Postgres+...) │  │
│  └──────────┘     └─────────────┘     └─────────────────┘  │
│       │  ▲              │  ▲                   │  ▲          │
│       ▼  │              ▼  │                   ▼  │          │
│  ┌──────────┐     ┌─────────────┐     ┌─────────────────┐  │
│  │  Cache    │     │   CDN       │     │  Storage/Queues │  │
│  │  local    │     │  (imágenes) │     │  Edge Functions │  │
│  └──────────┘     └─────────────┘     └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Los 3 atributos clave (DDIA)

*Fuente: Kleppmann, *Designing Data-Intensive Applications* (O'Reilly).*

### 1. Reliability (Confiabilidad)
"El sistema sigue funcionando correctamente incluso cuando algo sale mal", aunque falle hardware, software o el humano que opera. Eso implica:
- Tolerancia a fallos (fault tolerance): un servidor cae → no se cae todo.
- Manejo de errores del usuario y del sistema.
- Monitoreo para detectar problemas antes de que afecten a los usuarios.

### 2. Scalability (Escalabilidad)
"El sistema puede manejar crecimiento de carga sin degradarse". La carga se describe con **parámetros de carga** (load parameters):
- Requests por segundo (RPS/QPS).
- Ratio de lecturas vs escrituras.
- Usuarios activos concurrentes.
- Tamaño de los datos.

Si el sistema es lento para **un solo usuario**, es un problema de *performance*. Si es rápido para uno pero lento con mucha carga, es un problema de *scalability*. *(System Design Primer — "Performance vs scalability".)*

### 3. Maintainability (Mantenibilidad)
"Distintos tipos de personas (ingenieros, ops) pueden trabajar en el sistema de forma productiva". Se logra con:
- **Operabilidad:** logs, métricas, debugging fáciles (módulo 19 del repo).
- **Simplicidad:** reducir complejidad accidental.
- **Evolvabilidad:** poder cambiar y añadir features sin romper lo existente (módulo 01).

---

## System Design vs Clean Architecture vs Diseño de Features

| | Clean Architecture (M01) | Diseño de Features (M02) | System Design (M22) |
|---|---|---|---|
| **Pregunta** | ¿Cómo organizo el código? | ¿Qué construyo y cómo encaja? | ¿Cómo funciona el sistema completo? |
| **Escala** | 1 archivo / 1 clase | 1 feature | Todo el ecosistema |
| **Artefacto** | Carpetas y clases | Documento de diseño (FADER) | Diagrama de componentes + trade-offs |
| **¿Toca código?** | Sí | Solo diseño | Diagramas y decisiones de infraestructura |
| **Nº de "computadoras"** | 1 (el dispositivo) | 1 app + 1 backend | Muchas (servidores, CDN, replicas) |

Son **capas complementarias**. Puedes tener Clean Architecture impecable y que tu sistema caiga con 100k usuarios por no diseñar el backend. Y a la inversa: una infraestructura perfecta no salva código espagueti.

---

## Los 4 pasos universales de diseño

*Fuente: System Design Primer (donnemartin) y Grokking Modern System Design Interview (Educative).*

```
1. CLARIFICAR   → Definir casos de uso, restricciones y suposiciones.
                  (¿Quién lo usa? ¿Cuántos usuarios? ¿Ratio lectura/escritura?)
2. DISEÑAR      → Diseño de alto nivel: componentes principales y conexiones.
3. PROFUNDIZAR  → Diseño de componentes núcleo: esquema, API, caché.
4. ESCALAR      → Identificar cuellos de botella y aplicar patrones (LB, cache, sharding).
```

**Regla de oro:** *"Everything is a trade-off"* — cada decisión (caché vs consistencia, SQL vs NoSQL, consistencia vs disponibilidad) tiene pros y contras que debes poder justificar.

---

## Errores comunes de principiante

| Error | Solución |
|---|---|
| Empezar a diseñar sin clarificar requisitos | Siempre preguntar primero (usuarios, carga, latencia) |
| Solo hablar de código | Hablar de componentes: cliente, API, DB, cache, CDN |
| Ignorar el trade-off | Nombrar explícitamente qué ganas y qué sacrificas |
| No mencionar escalabilidad | Incluir siempre el paso "escalar" |
| Inventar números de latencia | Usar la tabla real de latencias (ver archivo 02) |

---

## Fuentes

- [Designing Data-Intensive Applications — M. Kleppmann](https://dataintensive.net/)
- [The System Design Primer — donnemartin](https://github.com/donnemartin/system-design-primer)
- [Grokking Modern System Design Interview — Educative](https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers)

---

**Siguiente:** [01-clarificar-requisitos.md](./01-clarificar-requisitos.md)
