# GUÍA DE TRABAJO CON IA

> **Norte**: "Podés defender cada línea que está en tu repo."
> La IA es un *pair programmer* con superpoderes de velocidad y conocimiento.
> **No** es un reemplazo de tu razonamiento. Cuando dejes de entender el código que escribís, la IA ganó.

Esta guía define una manera de trabajar **equilibrada y con criterio** usando IA en este monorepo (Flutter Clean Architecture, Supabase, Next.js). Se revisa y ajusta con el tiempo.

---

## 1. Principio rector

**Vos diseñás y decidís; la IA ejecuta.**

- Mantené en tu cabeza la **arquitectura**, los **porqués** y la **lógica de negocio**.
- Delegá a la IA lo **mecánico, repetitivo y de conocimiento enciclopédico** (librerías, APIs, sintaxis, boilerplate).
- Toda decisión de diseño (estructura de feature, contrato de datos, flujo) la tomás **vos**.

Pregunta de auto-check en cada sesión:
> "Si la IA se fuera ahora, ¿podría seguir este proyecto yo solo?"

Si la respuesta es no, estás delegando de más.

---

## 2. Matriz de responsabilidad

### ✍️ Escribís vos (entrenamiento mental)
- **Lógica de negocio**: reglas de rifas, validaciones, cálculos de premios, estados de pago.
- **Algoritmos**: búsqueda de números, asignación de boletos, sorteos, optimizaciones.
- **Diseño de la solución**: estructura de la feature, flujo de pantallas, contratos de datos.
- **Debugging de bugs complejos**: trazar el estado, encontrar la causa raíz.
- **Edge cases** y casos límite de cada feature.

### 🤖 Delegás a la IA (donde brilla)
- **Scaffolding Clean Architecture**: entidad, model, datasource, repository, usecase, cubit, estado, página.
- **Migrations y RLS de Supabase**: SQL de tablas, políticas, índices, seed.
- **Boilerplate Cubit/BLoC** y registro en GetIt.
- **Plantillas Next.js**: Server Components, Server Actions, formularios típicos.
- **Tests unitarios** una vez que vos definiste la lógica (mocktail/blocTest/fpdart).
- **Configs, regex, refactors mecánicos** (renames, movidas de archivos, formato).
- **Respuestas a dudas**: "explicame qué es X", "cuál es la API de Y".

### ⚖️ Zona compartida (depende del contexto)
- **ORM/consultas**: la IA propone, vos validás que respete RLS y el modelo de datos.
- **UI widgets**: la IA propone la estructura, vos definís estados y comportamiento.

---

## 3. Workflow 50/50 paso a paso

Aplicado a cualquier feature de este repo:

```
1. VOS     → Escribís el esqueleto/pseudocódigo de la feature (los "huesos").
             Nombres, capas, contratos, flujo. Nada de magia.
             (O la diseñas en el .pen y después la aterrizás en código)

2. IA      → Completa el boilerplate: entidad/model/datasource/repository
             vacíos, cubit base, DI en GetIt, ruta en GoRouter, migration SQL.

3. VOS     → Implementás la lógica de negocio con tus manos.
             Lo que hace única a la feature. Lo difícil.

4. IA      → Code review: bugs, mejoras, tests faltantes, edge cases.

5. VOS     → Aplicás solo lo que entendés y podés defender.
             Rechazás el resto explicando el porqué.
```

**Ritual de cierre**: después de cada feature, respondé en una línea:
- Qué escribí yo, qué delegué, y **qué aprendí**.

---

## 4. Reglas de oro para no perder agilidad

1. **Nunca pegues sin entender.**
   Si la IA genera código, pedí que te lo **explique** antes de aceptarlo:
   *"Explicame línea por línea qué hace esto y por qué lo hiciste así."*

2. **Revisá cada diff como si fuera de un colega desconocido.**
   Aprobás con criterio, no por confianza. Mirá cada archivo tocado.

3. **Re-escribí lo generado.**
   Cuando la IA te da algo útil, reescribilo con tu estilo una vez.
   Esa "traducción mental" es el entrenamiento real.

4. **Reto diario "sin IA".**
   Una feature pequeña, una kata o un algoritmo resuelto 100% a mano.
   10-15 minutos alcanzan. Es la reserva de agilidad mental.

5. **Formulá en palabras antes de pedir.**
   Si no podés explicar la solución en una frase, la IA la resuelve, pero **vos no aprendés**.
   Escribí primero: "el flujo es: usuario elige números → se reservan → paga → se confirman".

6. **Usala como buscador de "qué existe"** (librerías, APIs, patrones),
   no como "dame el código listo".

---

## 5. Tabla de prompts: malo vs. bueno

| ❌ Pedido malo | ✅ Pedido bueno |
|---|---|
| "Hazme el login" | "Quiero implementar login. Muéstrame las opciones para el stack (Supabase Auth). El flujo lo diseño yo, solo completame el boilerplate del datasource." |
| "Arregla este bug" | "Explicame por qué falla esto" (primero entendés, después arreglás vos). |
| "Escribe este método" | "Escribí la firma y el esqueleto con el contrato; la lógica de negocio la completo yo." |
| "Genera toda la feature de compradores" | "Scaffolding de la feature compradores (entidad, model, datasource, repository, cubit, estado, página). Métodos vacíos con `throw UnimplementedError()`, sin implementación." |
| "Crea la tabla de pagos" | "Crea la migration de pagos con RLS; explícame cada política antes de aplicar." |
| "Hazme tests" | "Generá tests de esta usecase con mocktail + blocTest; yo ya definí los casos en el código." |

**Plantilla de prompt para scaffolding en este repo:**
> "Usando el skill clean-arch-feature, genera el scaffold de `<feature>` con
> entidad `<campos>` + integración Supabase (tabla, migration, RLS).
> Solo estructura, métodos con `throw UnimplementedError()`.
> NO implementes la lógica de negocio, esa la escribo yo."

---

## 6. Compromisos medibles (para definir mañana)

Estos se van a fijar en la primera sesión de trabajo con la guía en mano:

- [ ] **% de cada feature escrito a mano** (ej. mínimo 40%: lógica de negocio + diseño).
- [ ] **Qué se delega siempre** (boilerplate, migrations, configs, tests de patrones).
- [ ] **Qué se escribe siempre a mano** (lógica de premios, estados de pago, edge cases).
- [ ] **Criterios de aceptación de código generado** (compiló, tests pasan, RLS ok, podés explicarlo).
- [ ] **Regla del reto sin IA** (frecuencia y duración).
- [ ] **Formato del ritual de cierre** por feature.

---

## 7. Referencia rápida del stack (para consultar al delegar)

| Capa | Herramienta | Qué delegar |
|---|---|---|
| Mobile | Flutter + Clean Arch (Cubit/BLoC, GetIt, fpdart `Either<Failure,T>`) | Scaffolding, modelos, DI, tests |
| Web | Next.js App Router (Server Components + Server Actions) | Plantillas de páginas, formularios, fetch patterns |
| Backend | Supabase (Postgres + Auth + Storage + Edge Functions) | Migrations, RLS, seed, edge functions |
| Git | Conventional Commits (`feat(auth):`, `fix(ui):`) | Mensajes de commit (con `make commit` para interactivo) |

---

*Revisar esta guía cada vez que el equilibrio se sienta desviado.
La meta no es "usar IA o no", sino **usarla con criterio**.*
