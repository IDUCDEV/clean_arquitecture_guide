# 02 - Diseño de Features

> Aprende a descomponer cualquier feature en papel y lápiz antes de escribir código. El arte perdido de pensar primero, codificar después.

---

## 📋 Índice

| Archivo | Descripción |
|---------|-------------|
| [00-alcance-feature.md](./00-alcance-feature.md) | Teoría: Definir el alcance de la feature (incluye/no incluye) |
| [01-descomposicion-feature.md](./01-descomposicion-feature.md) | Teoría: Framework FADER de descomposición + reglas RN/RT/RS |
| [01a-practica-carrito.md](./01a-practica-carrito.md) | Práctica: Descomponer feature Carrito de Compras |
| [02-mapeo-capas.md](./02-mapeo-capas.md) | Teoría: Traducir descomposición a Clean Architecture |
| [02a-practica-carrito-capas.md](./02a-practica-carrito-capas.md) | Práctica: Mapear Carrito a las capas |
| [03-contratos-primero.md](./03-contratos-primero.md) | Teoría: Contract-First Design y ADRs |
| [03a-practica-carrito-contratos.md](./03a-practica-carrito-contratos.md) | Práctica: Escribir contratos sin implementar |
| [04-flujo-datos.md](./04-flujo-datos.md) | Teoría: Flujo de datos entre capas |
| [04a-practica-carrito-flujo.md](./04a-practica-carrito-flujo.md) | Práctica: Diagramar flujo completo del Carrito |
| [05e-diseno-supabase.md](./05e-diseno-supabase.md) | Teoría: Contrato con el backend — Supabase (tablas, RLS, RPC, realtime) o REST API (endpoints, DTOs, garantías) |
| [05f-criterios-aceptacion-trazabilidad.md](./05f-criterios-aceptacion-trazabilidad.md) | Teoría: Criterios de aceptación (BDD) y matriz de trazabilidad |
| [05-caso-completo-reservas.md](./05-caso-completo-reservas.md) | Caso integral: Sistema de Reservas |
| [05b-caso-elearning.md](./05b-caso-elearning.md) | Caso integral: Plataforma E-Learning |
| [05c-caso-facturacion.md](./05c-caso-facturacion.md) | Caso integral: Sistema de Facturación |
| [05d-caso-delivery.md](./05d-caso-delivery.md) | Caso integral: App de Delivery |
| [15-estimacion-complejidad.md](./15-estimacion-complejidad.md) | Estimación de tiempo con framework FADER |
| [PLANTILLA-DISENIO-FEATURE.md](./PLANTILLA-DISENIO-FEATURE.md) | Plantilla reutilizable del flujo completo de diseño |
| [BIBLIOGRAFIA.md](./BIBLIOGRAFIA.md) | Fuentes, libros y referencias |

---

### 🤖 Trabajar Sin IA

Sección dedicada a reconstruir tu capacidad de desarrollo autónomo. Framework de 6 fases para enfrentar features sin depender de IA.

| Archivo | Descripción |
|---------|-------------|
| [trabajar-sin-ia/06-el-costumbre-de-la-ia.md](./trabajar-sin-ia/06-el-costumbre-de-la-ia.md) | Por qué dependes de IA y qué te cuesta |
| [trabajar-sin-ia/07-el-flujo-de-trabajo.md](./trabajar-sin-ia/07-el-flujo-de-trabajo.md) | Framework de 6 fases: Investigar → Diseñar → Implementar → Verificar → Refactor → Validar |
| [trabajar-sin-ia/08-como-investigar-sin-ia.md](./trabajar-sin-ia/08-como-investigar-sin-ia.md) | Fuentes oficiales, GitHub, pub.dev, Stack Overflow |
| [trabajar-sin-ia/09-feature-simple-ejemplo.md](./trabajar-sin-ia/09-feature-simple-ejemplo.md) | Ejemplo: CRUD de Notas (Simple) |
| [trabajar-sin-ia/10-feature-intermedia-ejemplo.md](./trabajar-sin-ia/10-feature-intermedia-ejemplo.md) | Ejemplo: Notificaciones Push (Intermedia) |
| [trabajar-sin-ia/11-feature-compleja-ejemplo.md](./trabajar-sin-ia/11-feature-compleja-ejemplo.md) | Ejemplo: Pagos con Stripe (Compleja) |
| [trabajar-sin-ia/12-ejercicios-practica.md](./trabajar-sin-ia/12-ejercicios-practica.md) | 6 ejercicios de práctica sin IA |
| [trabajar-sin-ia/13-checklists-y-plantillas.md](./trabajar-sin-ia/13-checklists-y-plantillas.md) | Plantillas y checklists para cada fase |
| [trabajar-sin-ia/14-recursos-externos.md](./trabajar-sin-ia/14-recursos-externos.md) | Dónde encontrar ayuda sin depender de IA |

#### Flujo de diseño recomendado

```
1.  Define el alcance        → 00-alcance-feature.md
2.  Descompón con FADER      → 01-descomposicion-feature.md (+ reglas RN/RT/RS)
3.  Mapea a capas            → 02-mapeo-capas.md
4.  Diseña contratos         → 03-contratos-primero.md
5.  Diagrama el flujo        → 04-flujo-datos.md
6.  Diseña el backend        → 05e-diseno-supabase.md (Supabase: tablas/RLS/RPC · REST API: contrato de endpoints)
7.  Criterios + trazabilidad → 05f-criterios-aceptacion-trazabilidad.md
8.  Estima y planifica       → 15-estimacion-complejidad.md
Todo esto en un solo lugar  → PLANTILLA-DISENIO-FEATURE.md
```

#### Flujo recomendado (Trabajar Sin IA)

```
1. Lee 06-el-costumbre-de-la-ia.md (entender el problema)
2. Estudia 07-el-flujo-de-trabajo.md (framework de 6 fases)
3. Revisa 08-como-investigar-sin-ia.md (herramientas)
4. Analiza los 3 ejemplos (09, 10, 11) de menor a mayor complejidad
5. Haz los ejercicios (12) usando las plantillas (13)
6. Guarda los recursos (14) para consultas rápidas
```

---

### 📖 Casos integradores

Los casos prácticos te permiten aplicar FADER + Mapeo + Contratos + Flujo en industrias reales:

| Caso | Industria | Complejidad | Lo nuevo que practicas |
|------|-----------|-------------|------------------------|
| [Reservas](./05-caso-completo-reservas.md) | Veterinaria | Media | Alcance, FADER completo, Supabase, ADR |
| [E-Learning](./05b-caso-elearning.md) | Educación | Media | Progreso, jerarquías, RLS por rol, criterios BDD |
| [Facturación](./05c-caso-facturacion.md) | Financiera | Alta | Máquina de estados, RPC atómico (número secuencial), trazabilidad |
| [Delivery](./05d-caso-delivery.md) | Logística | Alta | Realtime, geolocalización, race condition, 3 actores |

---

## 🎯 Filosofía del Módulo

Antes de que existiera la IA, antes de los frameworks reactivos, antes incluso de los IDE modernos, los desarrolladores hacían algo que se está perdiendo: **pensar antes de codificar**.

Este módulo recupera esa práctica. Tiene dos partes:

### Parte 1: Diseño (Archivos 00-15)
0. **Definir el alcance** de la feature antes de descomponer
1. **Descomponer** el problema en piezas atómicas
2. **Mapear** cada pieza a su capa en Clean Architecture
3. **Diseñar contratos** (interfaces) que definan cómo se comunican las capas
4. **Diagramar flujos** de datos y estados
5. **Diseñar el backend** (Supabase: tablas, RLS, RPC atómicos, realtime · REST API: contrato de endpoints)
6. **Definir criterios de aceptación** y una matriz de trazabilidad
7. **Estimar** la complejidad para planificar

### Parte 2: Trabajar Sin IA (carpeta `trabajar-sin-ia/`)
1. **Entender** por qué dependes de IA y qué te cuesta
2. **Investigar** usando fuentes oficiales, no IA
3. **Implementar** siguiendo un framework de 6 fases
4. **Practicar** con ejercicios reales sin asistencia

Solo cuando todo eso esté sólido en papel, abrirás el editor. Y cuando abras el editor, serás tú — no la IA — quien escriba el código.

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
| **A**lcance | Definir límites | ¿Qué incluye y qué NO incluye? |
| **F**ormular | Definir el problema | ¿Qué necesidad resuelve esta feature? |
| **A**ctorizar | Identificar actores | ¿Quiénes interactúan y qué esperan? |
| **D**escomponer | Listar operaciones atómicas | ¿Qué acciones mínimas existen? |
| **E**ntidades | Modelar conceptos del mundo real | ¿Qué objetos de negocio existen? |
| **R**eglas | Capturar reglas (RN/RT/RS) | ¿Qué condiciones y límites aplican? |

Después del FADER: mapea a capas → diseña contratos → flujo de datos → **contrato con el backend** → **criterios de aceptación y trazabilidad**. Cada capa defiende sus reglas: el dominio las de negocio (RN), el DataSource las técnicas (RT) y el servidor las de seguridad (RS: RLS en Supabase, autorización en la API).

---

## 🚀 Siguiente paso

Después de este módulo, continúa con [01-CLEAN-ARCHITECTURE](../01-CLEAN-ARCHITECTURE/) para aprender a implementar en código todo lo que diseñaste aquí.

---

**Nivel:** Principiante a Avanzado  
**Tiempo estimado:** 25-35 horas (incluyendo casos prácticos y ejercicios sin IA)  
**Herramientas:** Papel, lápiz, tu cabeza. Y disciplina para no abrir ChatGPT.
