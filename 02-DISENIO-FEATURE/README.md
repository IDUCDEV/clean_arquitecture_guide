# 02 - Diseño de Features

> Aprende a descomponer cualquier feature en papel y lápiz antes de escribir código. El arte perdido de pensar primero, codificar después.

---

## 📋 Índice

| Archivo | Descripción |
|---------|-------------|
| [01-descomposicion-feature.md](./01-descomposicion-feature.md) | Teoría: Framework FADER de descomposición |
| [01a-practica-carrito.md](./01a-practica-carrito.md) | Práctica: Descomponer feature Carrito de Compras |
| [02-mapeo-capas.md](./02-mapeo-capas.md) | Teoría: Traducir descomposición a Clean Architecture |
| [02a-practica-carrito-capas.md](./02a-practica-carrito-capas.md) | Práctica: Mapear Carrito a las capas |
| [03-contratos-primero.md](./03-contratos-primero.md) | Teoría: Contract-First Design y ADRs |
| [03a-practica-carrito-contratos.md](./03a-practica-carrito-contratos.md) | Práctica: Escribir contratos sin implementar |
| [04-flujo-datos.md](./04-flujo-datos.md) | Teoría: Flujo de datos entre capas |
| [04a-practica-carrito-flujo.md](./04a-practica-carrito-flujo.md) | Práctica: Diagramar flujo completo del Carrito |
| [05-caso-completo-reservas.md](./05-caso-completo-reservas.md) | Caso integral: Sistema de Reservas |
| [05b-caso-elearning.md](./05b-caso-elearning.md) | Caso integral: Plataforma E-Learning |
| [05c-caso-facturacion.md](./05c-caso-facturacion.md) | Caso integral: Sistema de Facturación |
| [05d-caso-delivery.md](./05d-caso-delivery.md) | Caso integral: App de Delivery |
| [BIBLIOGRAFIA.md](./BIBLIOGRAFIA.md) | Fuentes, libros y referencias |

---

### 📖 Casos integradores

Los casos prácticos te permiten aplicar FADER + Mapeo + Contratos + Flujo en industrias reales:

| Caso | Industria | Complejidad | Lo nuevo que practicas |
|------|-----------|-------------|------------------------|
| [Reservas](./05-caso-completo-reservas.md) | Veterinaria | Media | FADER completo + ADR |
| [E-Learning](./05b-caso-elearning.md) | Educación | Media | Progreso, jerarquías (curso → módulo → lección) |
| [Facturación](./05c-caso-facturacion.md) | Financiera | Alta | Máquina de estados, transiciones, número secuencial |
| [Delivery](./05d-caso-delivery.md) | Logística | Alta | Tiempo real (Streams), geolocalización, 3 actores |

---

## 🎯 Filosofía del Módulo

Antes de que existiera la IA, antes de los frameworks reactivos, antes incluso de los IDE modernos, los desarrolladores hacían algo que se está perdiendo: **pensar antes de codificar**.

Este módulo recupera esa práctica. Aquí no vas a escribir código. Vas a:

1. **Descomponer** el problema en piezas atómicas
2. **Mapear** cada pieza a su capa en Clean Architecture
3. **Diseñar contratos** (interfaces) que definan cómo se comunican las capas
4. **Diagramar flujos** de datos y estados

Solo cuando todo eso esté sólido en papel, abrirás el editor.

### ¿Por qué "papel y lápiz"?

```
         ┌─────────────────────────────────┐
         │                                 │
         │   CÓDIGO SIN DISEÑO            │
         │   "A escribir nomás"           │
         │                                 │
         │   Resultado:                    │
         │   ┌───────────────────────┐    │
         │   │ UseCase que mezcla    │    │
         │   │ lógica de UI + datos  │    │
         │   │ + validaciones + API  │    │
         │   └───────────────────────┘    │
         │                                 │
         └─────────────────────────────────┘
                      vs
         ┌─────────────────────────────────┐
         │                                 │
         │   CÓDIGO CON DISEÑO            │
         │   "1 hora de papel, 30 min     │
         │    de código"                   │
         │                                 │
         │   Resultado:                    │
         │   ┌───────────────────────┐    │
         │   │ Entity → UseCase →   │    │
         │   │ Repository → DataSrc │    │
         │   │ Capas claras y       │    │
         │   │ testeables           │    │
         │   └───────────────────────┘    │
         │                                 │
         └─────────────────────────────────┘
```

### Metodología: FADER

Framework de Análisis y Descomposición que usaremos en este módulo:

| Paso | Qué haces | Pregunta guía |
|------|-----------|---------------|
| **F**ormular | Definir el problema | ¿Qué necesidad resuelve esta feature? |
| **A**ctorizar | Identificar actores | ¿Quiénes interactúan y qué esperan? |
| **D**escomponer | Listar operaciones atómicas | ¿Qué acciones mínimas existen? |
| **E**ntidades | Modelar conceptos del mundo real | ¿Qué objetos de negocio existen? |
| **R**eglas | Capturar reglas de negocio | ¿Qué condiciones y límites aplican? |

---

## 🚀 Siguiente paso

Después de este módulo, continúa con [01-CLEAN-ARCHITECTURE](../01-CLEAN-ARCHITECTURE/) para aprender a implementar en código todo lo que diseñaste aquí.

---

**Nivel:** Principiante a Avanzado  
**Tiempo estimado:** 15-20 horas (incluyendo casos prácticos)  
**Herramientas:** Papel, lápiz, tu cabeza. Nada más.
