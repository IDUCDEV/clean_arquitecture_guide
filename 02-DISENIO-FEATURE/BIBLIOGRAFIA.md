# Bibliografía y Fuentes

> Las fuentes que dieron origen a este módulo y al proyecto completo. Libros, artículos, patrones y metodologías que fundamentan cada decisión arquitectónica.

---

## 📚 Libros Base

### Clean Architecture — Robert C. Martin (2017)

**Por qué está aquí:** Es la base de todo el proyecto. Define la regla de dependencia, las capas, los casos de uso, y la separación entre entidades y detalles de implementación.

**Aportación concreta al módulo:**
- Las 3 capas (Presentation, Domain, Data)
- La regla de dependencia: las capas internas no saben de las externas
- Los UseCases como orquestadores de lógica de negocio
- Las Entities como objetos de negocio puros

**Lectura recomendada:** Capítulos 1-15 (Partes I y II) para los fundamentos. Capítulos 16-22 (Parte III) para los detalles de implementación.

---

### Domain-Driven Design — Eric Evans (2003)

**Por qué está aquí:** DDD enseña a descomponer problemas complejos del mundo real en modelos de software. Es la "caja de herramientas" para el paso de descomposición y entidades.

**Aportación concreta al módulo:**
- El **lenguaje ubicuo**: nombrar las cosas como son en el negocio
- Los **agregados**: conjuntos de entidades que se tratan como una unidad
- Las **reglas de negocio** explícitas en el dominio
- La separación entre **entidades** (tienen identidad) y **value objects** (se definen por sus atributos)

**Lectura recomendada:** Capítulos 1-4 (Lenguaje Ubicuo, Modelo de Dominio). Capítulo 5 (Entidades y Value Objects). Capítulo 6 (Agregados).

---

### Growing Object-Oriented Software, Guided by Tests — Steve Freeman & Nat Pryce (2009)

**Por qué está aquí:** Este libro conecta el diseño con el testing. Muestra cómo dejar que los tests guíen el diseño de las interfaces y la estructura.

**Aportación concreta al módulo:**
- El enfoque **Contract-First** sin llamarlo explícitamente: diseñar desde afuera hacia adentro
- Los **mocks como herramientas de diseño**, no solo de testing
- Cómo el testing fuerza a tener interfaces limpias

**Lectura recomendada:** Capítulos 1-8 para entender la filosofía. Capítulos 20-26 para la parte práctica.

---

### Refactoring: Improving the Design of Existing Code — Martin Fowler (1999 / 2da ed. 2018)

**Por qué está aquí:** No siempre se diseña perfecto desde el inicio. Fowler enseña cómo mejorar el diseño existente sin romperlo.

**Aportación concreta al módulo:**
- Justifica por qué vale la pena invertir tiempo en diseño: el costo de no hacerlo
- Técnicas para migrar de código espagueti a capas
- La noción de que el diseño evoluciona

**Lectura recomendada:** El catálogo completo de refactors. Especialmente: Extract Method, Extract Class, Move Method, Replace Conditional with Polymorphism.

---

### Design Patterns — Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides (GoF) (1994)

**Por qué está aquí:** Los patrones que aparecen constantemente en Clean Architecture.

**Aportación concreta al módulo:**
- **Repository** (patrón): la interface que abstrae el almacenamiento
- **Adapter**: cómo DataSource convierte datos externos a modelos internos
- **Strategy**: cómo inyectar comportamientos alternativos

---

## 📄 Patrones y Metodologías

### Contract-First Design

**Origen:** Metodología utilizada en desarrollo de APIs (OpenAPI/Swagger), microservicios, y diseño por contratos (Bertrand Meyer, 1986).

**En el módulo:** Cada contrato define responsabilidades, parámetros, retornos y errores posibles. Las implementaciones vienen después.

**Referencia:** Meyer, B. (1986). *Design by Contract*. El principio de que las interfaces deben especificar precondiciones, postcondiciones e invariantes.

---

### Architecture Decision Records (ADR)

**Origen:** Michael Nygard, 2011.

**En el módulo:** Los ADRs registran por qué se tomó cada decisión arquitectónica, qué alternativas se consideraron, y las consecuencias esperadas.

**Referencia original:** Nygard, M. (2011). *Documenting Architecture Decisions*. [Documento original](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)

**Formato recomendado:** El formato Nygard/Y-Statements estándar: Contexto → Decisión → Consecuencias → Alternativas.

---

### Result Pattern (Either / Railway Oriented Programming)

**Origen:** Programación funcional. Popularizado en C# por Scott Wlaschin (2014).

**En el módulo:** Cada operación del dominio retorna `Either<Failure, Success>` en vez de lanzar excepciones. Esto hace que el manejo de errores sea explícito y tipado.

**Referencia:** Wlaschin, S. (2014). *Railway Oriented Programming*. [F# for Fun and Profit](https://fsharpforfunandprofit.com/rop/)

**Implementación en Dart:** fpdart (ver sección de paquetes abajo).

---

### fpdart — Programación Funcional en Dart

**Origen:** Paquete Dart desarrollado por Sandro Maglione.

**En el módulo:** Proporciona `Either`, `Option`, `TaskEither`, y otras herramientas funcionales que se usan en los contratos del dominio.

**Referencia:** [fpdart en pub.dev](https://pub.dev/packages/fpdart) | [Documentación](https://fpdart.dev/)

---

## 🧠 Metodología FADER

**Origen:** Invención propia para este módulo (2026).

**Base conceptual:**
- **F**ormular → Inspirado en User Story Mapping (Jeff Patton)
- **A**ctorizar → Inspirado en el análisis de actores de UML y Use Case 2.0 (Ivar Jacobson)
- **D**escomponer → Inspirado en Event Storming (Alberto Brandolini) y descomposición funcional clásica
- **E**ntidades → Inspirado en DDD (Eric Evans)
- **R**eglas → Inspirado en Business Rules Engine y el enfoque de DDD

**No inventé la descomposición de problemas. Inventé el marco con nombre y pasos claros (FADER) para que sea accionable y enseñable.**

---

## 🔗 Paquetes y Herramientas Referenciadas

| Paquete | Uso en el módulo | Enlace |
|---------|------------------|--------|
| flutter_bloc | Manejo de estado (Presentation) | [pub.dev](https://pub.dev/packages/flutter_bloc) |
| equatable | Comparación de objetos | [pub.dev](https://pub.dev/packages/equatable) |
| get_it / injectable | Inyección de dependencias | [pub.dev](https://pub.dev/packages/get_it) |
| fpdart | Either, Option, TaskEither | [pub.dev](https://pub.dev/packages/fpdart) |
| supabase_flutter | Backend como servicio | [pub.dev](https://pub.dev/packages/supabase_flutter) |
| freezed (alternativa) | Sealed classes generadas | [pub.dev](https://pub.dev/packages/freezed) |

---

## 📝 Nota sobre la Autoría

Este módulo `02-DISENIO-FEATURE` es un **ensamblaje original** de conceptos existentes, no una invención desde cero de cada idea:

| Concepto | Fuente | Nivel de originalidad |
|----------|--------|----------------------|
| Capas de Clean Architecture | R. C. Martin | Adaptación |
| Framework FADER | Invención propia | **Original** |
| Matriz de Responsabilidades | Invención propia | **Original** |
| Mapeo FADER → Clean Architecture | Invención propia | **Original** |
| Contract-First Design | Metodología establecida | Adaptación |
| ADRs | M. Nygard | Adaptación |
| Plantillas de contratos | Invención propia | **Original** |
| Diagramas de flujo en U | Invención propia | **Original** |
| Casos prácticos | Invención propia | **Original** |

---

*Última actualización: 2026-05-15*
