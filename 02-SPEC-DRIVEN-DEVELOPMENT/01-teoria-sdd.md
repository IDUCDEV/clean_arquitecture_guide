# 01 - Teoría SDD: Mapa del Libro Oficial

> La teoría de este módulo es el libro **`SDDEquiposAgiles_v.1.pdf`** (Scrum Manager, v1.0 — abril 2026, 74 páginas). Este archivo NO lo duplica: te da el **mapa de lectura** y traduce cada capítulo a tu stack (Flutter + Supabase + Clean Architecture).

---

## Cómo usar este archivo

1. Lee el libro una vez completa (`pdf/SDDEquiposAgiles_v.1.pdf`)
2. Usa este mapa como índice de consulta rápida: ¿en qué capítulo estaba X?
3. Cada fila te dice dónde se **operativiza**: qué archivo de este módulo convierte ese concepto en algo ejecutable

El complemento `pdf/Guia-SDD-equipos-agiles.pdf` (35 págs.) es el resumen *state-of-the-art* del mismo contenido: útil como repaso exprés, no como lectura principal.

---

## Mapa maestro del libro → este módulo

| Cap | Tema del libro | Idea clave | Se operativiza en |
|-----|----------------|------------|-------------------|
| 1–3 | Del vibe coding a SDD · spec como artefacto primario · problemas estructurales | La spec precede al código; el agente es un ejecutor con contrato, no un interlocutor | [README](./README.md) (filosofía) |
| 4–5 | SDD y agilidad · flujo de cuatro fases | Requisitos → Diseño → Tareas → Implementación; revisar en puertas, no durante | [02-sdd-flutter-supabase.md](./02-sdd-flutter-supabase.md) §flujo |
| 7 | Fase 1: Requisitos | Impact Report ANTES de requisitos · historias precisas · notación EARS | [02 §Paso 0 y Fase 1](./02-sdd-flutter-supabase.md) |
| 8 | Fase 2: Diseño | Ficheros afectados · decisiones explícitas · heurística sénior | [02 §Fase 2](./02-sdd-flutter-supabase.md) |
| 9 | Fase 3: Tareas | Tareas atómicas (rol/tarea/restricciones/criterios) · oleadas · descomposición justa | [02 §Fase 3](./02-sdd-flutter-supabase.md) |
| 10 | Fase 4: Implementación | Ejecución delegada · commits atómicos · revisión al cierre de fase | [02 §Fase 4](./02-sdd-flutter-supabase.md) |
| 11 | Puertas de aprobación | 3 puertas + revisión final; el coste del error crece por fase; quién aprueba | [02 §Puertas](./02-sdd-flutter-supabase.md) |
| 12 | Anatomía de una buena spec | 5 principios de Osmani · 6 áreas del análisis de GitHub | [04-plantilla](./04-plantilla-cambio-openspec.md) |
| 13 | Boundaries Always / Ask First / Never | Marco de delegación en 3 niveles, evolutivo | [02 §Boundaries](./02-sdd-flutter-supabase.md) |
| 14 | Maldición de las instrucciones | Más instrucciones = menor cumplimiento individual; dividir, no acumular | [05-referencia-rapida.md](./05-referencia-rapida.md) |
| 15 | Specs vivas vs estáticas | spec-first / spec-anchored / spec-as-source; actualizar en el mismo commit | [02 §Specs vivas](./02-sdd-flutter-supabase.md) |
| 16–18 | SDD en el equipo ágil | Equivalencias Scrum ↔ SDD; roles; ceremonias | [05-referencia-rapida.md](./05-referencia-rapida.md) §equivalencias |
| 19 | Brownfield | Impact Report obligatorio · formato delta · adopción gradual · constitución del proyecto | [02 §Paso 0](./02-sdd-flutter-supabase.md) |
| 20–21 | Herramientas 2026 · nativo vs framework | La vía intermedia: skills y slash commands | [03-openspec-guia-practica.md](./03-openspec-guia-practica.md) |
| 22 | Métricas | Métricas de flujo y de resultado; qué NO medir | [05-referencia-rapida.md](./05-referencia-rapida.md) §métricas |
| 23 | Anti-patrones | Sobreespecificación · documentación zombi · teatro de especificación · SDD como control | [05-referencia-rapida.md](./05-referencia-rapida.md) §antipatrones |

---

## Los 9 conceptos nucleares (resumen de 1 línea)

| Concepto | En una frase |
|----------|-------------|
| **Las 4 fases** | Requisitos (qué) → Diseño (cómo) → Tareas (en qué orden) → Implementación (ejecutar). |
| **Las 3 puertas** | Puntos donde el humano aprueba entre fases; corregir ahí es barato, después es caro. |
| **EARS** | 5 patrones (ubicuo, evento, estado, no deseado, opcional) que eliminan ambigüedad sin perder legibilidad. |
| **Tareas atómicas** | 1–3 ficheros, prompt con rol/tarea/restricciones/criterios, verificable en aislado. |
| **Oleadas** | Tareas independientes en paralelo (subagentes con contexto limpio); oleadas en secuencia. |
| **Commits atómicos** | 1 tarea = 1 commit: reversibilidad granular, trazabilidad y bisección eficaz. |
| **Boundaries** | Always (sin preguntar) / Ask First (aprobar antes) / Never (líneas rojas). |
| **Formato delta** | La spec describe solo lo que cambia: ADDED / MODIFIED / REMOVED (popularizado por OpenSpec). |
| **Clarity Gate** | ¿Un agente distinto regeneraría código equivalente solo con la spec? Si no, faltan supuestos. |

---

## Lo que el libro NO trae (y vive en este módulo)

El libro es genérico (cualquier lenguaje/plataforma). Lo específico de tu stack que este módulo aporta:

| Específico de Flutter + Supabase | Dónde |
|----------------------------------|-------|
| Impact Report sobre un codebase Clean Architecture (features, contratos, DI, rutas) | [02 §Paso 0](./02-sdd-flutter-supabase.md) |
| Clasificación de requisitos EARS por componente Clean Arch (entity, repository, usecase, datasource, cubit, page) | [02 §Fase 1](./02-sdd-flutter-supabase.md) |
| Reglas de seguridad como políticas RLS en Supabase (escenarios RS) | [02 §Fase 2](./02-sdd-flutter-supabase.md) |
| Oleadas estándar de implementación para una feature (entity → contratos → model/datasource → impl/cubit → pages/DI/router → tests) | [02 §Fase 3](./02-sdd-flutter-supabase.md) |
| Boundaries concretos (pubspec, migraciones, RLS de producción, build.gradle…) | [02 §Boundaries](./02-sdd-flutter-supabase.md) |
| Ejecución con la skill `clean-arch-feature` o con agente + OpenSpec | [02 §Fase 4](./02-sdd-flutter-supabase.md) + [03](./03-openspec-guia-practica.md) |

---

## Constitución del proyecto (prerrequisito brownfield)

Antes de tu primer cambio SDD en un proyecto existente, asegúrate de tener la **constitución** del proyecto (cap 19 del libro): un `AGENTS.md` / `CLAUDE.md` con stack, estructura de carpetas, patrones establecidos y flujo git. OpenSpec genera el stub automáticamente con `openspec init` ([ver guía práctica](./03-openspec-guia-practica.md)). Sin ella, cada spec se escribe en el vacío.

---

## Referencias

- 📕 Libro oficial: [`pdf/SDDEquiposAgiles_v.1.pdf`](./pdf/SDDEquiposAgiles_v.1.pdf) — lee primero las Partes II y III (caps 6–15)
- 📄 Resumen state-of-the-art: [`pdf/Guia-SDD-equipos-agiles.pdf`](./pdf/Guia-SDD-equipos-agiles.pdf)
- 🛠️ Herramienta: [03-openspec-guia-practica.md](./03-openspec-guia-practica.md)
- 📐 Metodología aplicada: [02-sdd-flutter-supabase.md](./02-sdd-flutter-supabase.md)
