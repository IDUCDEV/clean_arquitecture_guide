# 23 - Spec Driven Development (SDD)

> Escribe la spec antes que el código. Deja que la IA ejecute tu contrato, no tus ideas sueltas.

---

## Antes de empezar

Este módulo **complementa** la guía teórica SDD que ya tienes en la raíz del proyecto:

📄 **[`Guia-SDD-equipos-agiles.pdf`](../Guia-SDD-equipos-agiles.pdf)** — Scrum Manager / Skill Arena (junio 2026)

Lee esa guía primero para entender las 4 fases, las puertas de aprobación, los patrones EARS, el sistema de boundaries y los antipatrones. Este módulo **no repite** ese contenido; lo **aplica** a tu stack (Flutter + Supabase + Clean Architecture).

---

## ¿Por qué este módulo?

| Problema | Solución |
|----------|----------|
| Vibe coding falla a escala: 19% más lento pese a percibir un 20% más rápido (METR, 2025) | SDD: spec antes, código después |
| La IA inventa decisiones que no especificaste | Spec como contrato explícito |
| No sabes cuándo usar SDD y cuándo no | Principio de proporcionalidad |
| El código heredado se rompe con cambios mal planificados | Impact Report brownfield |
| Las specs se desactualizan y nadie las consulta | Clarity Gate + specs vivas |
| No tienes una herramienta concreta para implementar SDD | OpenSpec (65.7k ⭐, 30+ agentes) |

---

## Índice

| # | Archivo | Descripción |
|---|---------|-------------|
| 01 | [01-openspec-guia-practica.md](./01-openspec-guia-practica.md) | Setup y workflow de OpenSpec en un proyecto Flutter |
| 02 | [02-sdd-en-flutter.md](./02-sdd-en-flutter.md) | SDD adaptado a Flutter + Supabase + Clean Architecture |
| 03 | [03-integracion-modulo-02-fader.md](./03-integracion-modulo-02-fader.md) | Cómo integrar FADER (módulo 02) con SDD |
| 04 | [04-referencia-rapida.md](./04-referencia-rapida.md) | Cheat sheet: fases, puertas, EARS, boundaries |

---

## Lectura recomendada

1. **Primero**: [`Guia-SDD-equipos-agiles.pdf`](../Guia-SDD-equipos-agiles.pdf) (teoría completa)
2. **Luego**: Archivo 01 de este módulo (OpenSpec en la práctica)
3. **Después**: Archivo 02 (cómo aplica a Flutter)
4. **Opcional**: Archivo 03 (integración con FADER si usas módulo 02)

---

## Módulos relacionados

| Módulo | Conexión |
|--------|----------|
| [02 - Diseño de Feature](../02-DISENIO-FEATURE/) | FADER = implementación de SDD; archivo 03 integra ambos |
| [10 - Makefile](../10-MAKEFILE/) | Targets Makefile para automatizar verificación de specs |
| [12 - Git Flow y Conventional Commits](../12-GIT-FLOW-CONVENTIONAL-COMMITS/) | Commits atómicos = Cap 7 de SDD; specs conviven con convenciones de commit |

---

**Nivel:** Intermedio-Avanzado
**Tiempo estimado:** 2-3 horas (sin contar la guía SDD teórica)
**Requisito previo:** Haber leído `Guia-SDD-equipos-agiles.pdf`
