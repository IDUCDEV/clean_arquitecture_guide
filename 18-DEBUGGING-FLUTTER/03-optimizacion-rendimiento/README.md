# Submodulo 3: Optimizacion de Rendimiento

## Descripcion

Aprende a medir, diagnosticar y resolver problemas de rendimiento en Flutter. Desde fundamentos de FPS y frame budgets hasta la deteccion de memory leaks y la optimizacion de rebuilds innecesarios. Este submodulo convierte tus conocimientos de DevTools en **acciones concretas** que mejoran la experiencia real del usuario.

---

## Contenido

| # | Archivo | Tema | Tiempo |
|---|---|---|---|
| 01 | [01-fundamentos-rendimiento.md](./01-fundamentos-rendimiento.md) | Metricas clave, build modes, frame pipeline | 45 min |
| 02 | [02-optimizar-rebuilds.md](./02-optimizar-rebuilds.md) | const, keys, BlocSelector, RepaintBoundary | 60 min |
| 03 | [03-memory-leak-detection.md](./03-memory-leak-detection.md) | Deteccion y prevencion de memory leaks | 50 min |
| 04 | [04-rendering-complejo.md](./04-rendering-complejo.md) | ListView.builder, Slivers, imagenes, CustomPainter | 50 min |
| 05 | [05-cheatsheet-optimizacion.md](./05-cheatsheet-optimizacion.md) | Referencia rapida: tablas, comandos, mitos | 15 min |
| 06 | [06-practicas-optimizacion.md](./06-practicas-optimizacion.md) | 6 escenarios reales + ejercicio integrador | 120 min |

**Tiempo total estimado: 6-7 horas**

---

## Requisitos previos

| Modulo | Por que |
|---|---|
| [01-debugging-vscode](../01-debugging-vscode/) | Necesitas saber pausar y evaluar codigo |
| [02-flutter-devtools](../02-flutter-devtools/) | Usaras Performance, Memory y CPU Profiler |

---

## Fases de aprendizaje

```
Fase 1: Fundamentos
  └── 01-fundamentos-rendimiento (metricas, build modes, pipeline)

Fase 2: Tecnicas de optimizacion
  ├── 02-optimizar-rebuilds (rebuilds innecesarios)
  ├── 03-memory-leak-detection (fugas de memoria)
  └── 04-rendering-complejo (rendering pesado)

Fase 3: Consolidacion
  ├── 05-cheatsheet-optimizacion (referencia rapida)
  └── 06-practicas-optimizacion (ejercicios reales)
```

---

## Herramientas que necesitas

| Herramienta | Para que |
|---|---|
| Flutter DevTools | Performance view, Memory view, CPU Profiler |
| VS Code | Edicion y ejecucion con `--profile` |
| Dart DevTools extension | Acceso rapido a DevTools desde el IDE |
| Flutter Inspector | Ver widget tree y detectar rebuilds |

---

## Lo que NO cubre este modulo

| Tema | Donde encontrarlo |
|---|---|
| Teoria de widgets y ciclo de vida | [15-WIDGETS-FLUTTER](../../15-WIDGETS-FLUTTER/) |
| Patrones BLoC/Cubit y state management | [16-BLOC-CUBIT](../../16-BLOC-CUBIT/) |
| Arquitectura y separacion de capas | [01-CLEAN-ARCHITECTURE](../../01-CLEAN-ARCHITECTURE/) |
| Testing y benchmarks automatizados | [05-TESTING](../../05-TESTING/) |
