# Submodulo 2: Flutter DevTools

## Descripcion

Domina la suite completa de Flutter DevTools: Inspector de widgets, Performance view, CPU Profiler, Memory view, Network view, Debugger, Logging y App Size tool. Aprende a diagnosticar problemas reales de performance, memoria y red en tus aplicaciones Flutter.

---

## Contenido

| # | Archivo | Tema | Tiempo |
|---|---|---|---|
| 01 | [01-fundamentos-devtools.md](./01-fundamentos-devtools.md) | Que es DevTools, como lanzar, versiones | 30 min |
| 02 | [02-flutter-inspector.md](./02-flutter-inspector.md) | Widget inspector, visual debugging | 60 min |
| 03 | [03-performance-view.md](./03-performance-view.md) | Frames chart, jank, timeline, enhance tracing | 75 min |
| 04 | [04-cpu-profiler.md](./04-cpu-profiler.md) | CPU profiling, flame chart, sampling | 45 min |
| 05 | [05-memory-view.md](./05-memory-view.md) | Memory leaks, GC, snapshots, diff | 60 min |
| 06 | [06-network-view.md](./06-network-view.md) | HTTP/HTTPS/WebSocket traffic, filtros | 30 min |
| 07 | [07-debugger-devtools.md](./07-debugger-devtools.md) | Debugger integrado en DevTools | 30 min |
| 08 | [08-logging-view.md](./08-logging-view.md) | Logging, stdout/stderr, eventos custom | 20 min |
| 09 | [09-app-size-tool.md](./09-app-size-tool.md) | Analisis de tamano de app | 20 min |
| 10 | [10-cheatsheet-devtools.md](./10-cheatsheet-devtools.md) | Cheat sheet completo de todas las vistas | 15 min |
| 11 | [11-practicas-devtools.md](./11-practicas-devtools.md) | 8 escenarios practicos + ejercicio integrador | 150 min |

---

## Que aprenderas

- Lanzar DevTools desde VSCode y CLI
- Usar el Flutter Inspector para explorar el widget tree
- Diagnosticar jank con la Performance view
- Encontrar functions costosas con CPU Profiler
- Detectar memory leaks con Memory view
- Inspeccionar trafico de red con Network view
- Analizar el tamano de tu app con App Size tool

---

## Mapa de DevTools

```
Flutter DevTools
├── Inspector      → Que ve el usuario (widgets, layout, constraints)
├── Performance    → Cuando algo va lento (frames, jank, timeline)
├── CPU Profiler   → Que funcion consume mas CPU (flame chart)
├── Memory         → Que esta usando memoria (leaks, GC, heap)
├── Network        → Que se comunica con el mundo (HTTP, WebSocket)
├── Debugger       → Pausar y escrutar codigo (breakpoints, variables)
├── Logging        → Que esta pasando (logs, eventos, diagnostics)
└── App Size       → Cuanto pesa la app (treemap, dependencias)
```

---

## Cuando usar cada vista

| Sintoma | Vista |
|---|---|
| UI se siente "corta" o con jank | Performance |
| App consume mucha memoria | Memory |
| Request falla o es lento | Network |
| Widget no se ve como esperaba | Inspector |
| App tarda en iniciar | CPU Profiler + Performance |
| App pesa demasiado en store | App Size |
| Necesito ver logs de inicializacion | Logging |
| Necesito pausar codigo en DevTools | Debugger |
