# 02 - Spec Driven Development (SDD)

> Escribe la spec antes que el código. Deja que la IA ejecute tu contrato, no tus ideas sueltas.

---

## Qué es este módulo

La metodología **completa** de Spec Driven Development del curso, en tres piezas:

| Pieza | Qué aporta |
|-------|-----------|
| 📕 **Teoría** | El libro `pdf/SDDEquiposAgiles_v.1.pdf` (Scrum Manager, 74 págs.) + resumen `pdf/Guia-SDD-equipos-agiles.pdf` |
| 🛠️ **Herramienta** | [OpenSpec](https://openspec.dev) — specs markdown vivas en el repo, ejecutables por 30+ agentes IA |
| 📐 **Metodología aplicada** | Este módulo: el flujo SDD operativizado para Flutter + Supabase + Clean Architecture |

> **Nota histórica:** este módulo absorbe y reemplaza al antiguo `02-DISENIO-FEATURE`. La carpeta original se conserva como referencia histórica; toda la teoría de diseño de features vive ahora aquí, en terminología SDD estándar ([tabla de equivalencias](./05-referencia-rapida.md#equivalencias-de-terminología-glosario-de-dilución)).

---

## ¿Por qué SDD?

| Problema | Solución |
|----------|----------|
| Vibe coding falla a escala: 19% más lento pese a percibir un 20% más rápido (METR, 2025) | SDD: spec antes, código después |
| La IA inventa decisiones que no especificaste | Spec como contrato explícito |
| No sabes cuándo usar SDD y cuándo no | Principio de proporcionalidad |
| El código heredado se rompe con cambios mal planificados | Impact Report brownfield |
| Las specs se desactualizan y nadie las consulta | Clarity Gate + specs vivas |
| No tienes una herramienta concreta para implementar SDD | OpenSpec (CLI ligera, sin API keys) |

---

## Índice

| # | Archivo | Descripción |
|---|---------|-------------|
| 01 | [01-teoria-sdd.md](./01-teoria-sdd.md) | Mapa de lectura del libro oficial cap por cap → aplicación a tu stack |
| 02 | [02-sdd-flutter-supabase.md](./02-sdd-flutter-supabase.md) | **Guía aplicada**: Impact Report, 4 fases, 3 puertas, EARS, oleadas, boundaries |
| 03 | [03-openspec-guia-practica.md](./03-openspec-guia-practica.md) | Setup y workflow de OpenSpec en un proyecto Flutter |
| 04 | [04-plantilla-cambio-openspec.md](./04-plantilla-cambio-openspec.md) | Plantilla lista para copiar: proposal, spec delta, design, tasks |
| 05 | [05-referencia-rapida.md](./05-referencia-rapida.md) | Cheat sheet + glosario de equivalencias → SDD |
| 06 | [06-auditoria-codigo-ia.md](./06-auditoria-codigo-ia.md) | Checklist para auditar código escrito por IA (Modo completo): contratos, sealed states, RLS, tests contra EARS |
| 07 | [07-guia-paso-a-paso.md](./07-guia-paso-a-paso.md) | **Receta de cocina**: cada fase de SDD con su comando OpenSpec, qué escribir, y checklist de puertas |
| — | [`ejemplos-cambios/`](./ejemplos-cambios/) | 6 cambios completos listos para copiar (carrito walkthrough incluido) |
| — | [`trabajar-sin-ia/`](./trabajar-sin-ia/) | Ejercicios de diseño con papel y lápiz, sin herramientas IA |
| — | [`pdf/`](./pdf/) | Libro oficial (SDDEquiposAgiles_v.1) + guías generadas del módulo (`02-SPEC-DRIVEN-DEVELOPMENT.pdf` y `GUIA-RESUMEN-*.pdf`, regenerables con `pdf/src/build_pdf.py`) |

---

## Ruta de aprendizaje

```
1. Lee el libro (Partes II y III primero)     → 01-teoria-sdd.md es tu mapa
2. Aprende la herramienta                     → 03-openspec-guia-practica.md
3. Domina la metodología en tu stack          → 02-sdd-flutter-supabase.md
4. Aplica paso a paso con OpenSpec            → 07-guia-paso-a-paso.md
5. Practica sin IA                            → trabajar-sin-ia/
6. Copia un ejemplo real y adáptalo           → ejemplos-cambios/add-cart/
7. Usa la plantilla en tu proyecto            → 04-plantilla-cambio-openspec.md
8. Delega todo y verifica como auditor        → 06-auditoria-codigo-ia.md
```

---

## Módulos relacionados

| Módulo | Conexión |
|--------|----------|
| [01 - Clean Architecture](../01-CLEAN-ARCHITECTURE/) | La estructura que las specs especifican capa por capa |
| [02 - Diseño de Feature (histórico)](../02-DISENIO-FEATURE/) | Origen de este módulo; conservado como archivo histórico |
| [10 - Makefile](../10-MAKEFILE/) | Targets para automatizar verificación de specs |
| [12 - Git Flow y Conventional Commits](../12-GIT-FLOW-CONVENTIONAL-COMMITS/) | Commits atómicos por tarea; specs conviven con convenciones |
| [22 - Diseño de Sistemas](../22-DISENIO-SISTEMAS/) | Escala de feature (SDD) a sistema completo |

---

**Nivel:** Intermedio-Avanzado
**Tiempo estimado:** 4-6 horas (incluyendo lectura parcial del libro)
**Requisito previo:** Conocer la estructura Clean Architecture ([01-CLEAN-ARCHITECTURE](../01-CLEAN-ARCHITECTURE/))
