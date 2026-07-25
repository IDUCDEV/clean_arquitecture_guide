# Modulo 18: Debugging con VSCode y Flutter DevTools

## Por que este modulo existe

El debugging es la habilidad que separa a un desarrollador junior de uno senior. No se trata solo de encontrar errores, sino de **entender el comportamiento de tu aplicacion** en tiempo real, diagnosticar problemas de performance, detectar memory leaks y optimizar cada aspecto de tu app.

Este modulo cubre las dos herramientas fundamentales del ecosistema Flutter:

1. **VSCode Debugging** - El debugger integrado en tu IDE
2. **Flutter DevTools** - La suite completa de profiling y diagnostico

---

## Mapa mental: cuando usar que

```
Estoy escribiendo codigo y necesito pausar la ejecucion
  └── VSCode Debugger (F5, breakpoints, stepping)

Mi app se siente lenta o tiene jank
  └── DevTools > Performance View

Sospecho un memory leak
  └── DevTools > Memory View

Un request HTTP falla o es lento
  └── DevTools > Network View

No entiendo porque un widget se ve mal
  └── DevTools > Flutter Inspector

Quiero saber que funcion consume mas CPU
  └── DevTools > CPU Profiler

Mi app pesa demasiado
  └── DevTools > App Size Tool

Necesito ver logs detallados
  └── DevTools > Logging View
```

---

## Requisitos previos

| Modulo | Por que |
|---|---|
| [05-TESTING](../05-TESTING/) | Testing y debugging se complementan |
| [16-BLOC-CUBIT](../16-BLOC-CUBIT/) | Debugging de BLoC/Cubit es escenario principal |
| [01-CLEAN-ARCHITECTURE](../01-CLEAN-ARCHITECTURE/) | Entender capas para saber donde poner breakpoints |
| [03-SUPABASE](../03-SUPABASE/) | Debugging de llamadas a Supabase |

---

## Contenido del modulo

### Submodulos

| # | Submodulo | Descripcion | Tiempo |
|---|---|---|---|
| 1 | [01-debugging-vscode](./01-debugging-vscode/) | Debugger completo de VSCode para Flutter | 4-6h |
| 2 | [02-flutter-devtools](./02-flutter-devtools/) | Suite completa de DevTools (7 vistas) | 6-8h |
| 3 | [03-optimizacion-rendimiento](./03-optimizacion-rendimiento/) | Optimizacion de rendimiento, rebuilds, memoria y rendering | 5-7h |
| 4 | [04-debugging-asincrono.md](./04-debugging-asincrono.md) | Los 5 bugs asíncronos más comunes + patrón seguro | 1h |
| 5 | [05-workflow-debugging-por-tipo.md](./05-workflow-debugging-por-tipo.md) | Workflow exacto para cada tipo de bug | 1h |

### Progresion recomendada

```
Fase 1: Fundamentos (ambos submodulos)
  ├── VSCode: fundamentos -> launch.json -> breakpoints
  └── DevTools: fundamentos -> inspector -> performance

Fase 2: Intermedio
  ├── VSCode: inspeccion de datos -> multi-target
  └── DevTools: CPU profiler -> memory -> network

Fase 3: Avanzado
  ├── VSCode: practicas reales + cheatsheet
  └── DevTools: practicas reales + cheatsheet + app size

Fase 4: Optimizacion
   ├── Fundamentos de rendimiento -> Optimizar rebuilds
   └── Memory leaks -> Rendering complejo

Fase 5: Maestria
   ├── Ejercicio integrador: diagnosticar una app "enferma"
   └── Practicas de optimizacion reales
```

---

## Herramientas que necesitas

| Herramienta | Version minima | Para que |
|---|---|---|
| VS Code | 1.80+ | IDE con debugger integrado |
| Extension Dart | latest | Debugging Dart/Flutter |
| Extension Flutter | latest | Soporte Flutter en VS Code |
| Flutter SDK | 3.22+ | DevTools incluido |
| DevTools | 2.23+ | Suite de profiling |

---

## Convenciones en este modulo

- Los ejemplos usan **Clean Architecture** (ver modulo 01)
- State management: **BLoC/Cubit** (ver modulo 16)
- Backend: **Supabase** (ver modulo 03)
- Los escenarios practicos son **reales y reproducibles**
- Cada cheatsheet es una **referencia rapida imprimible**

---

## Fuentes oficiales

- [VSCode Debugging](https://code.visualstudio.com/docs/debugtest/debugging)
- [Flutter DevTools](https://docs.flutter.dev/tools/devtools)
- [Flutter Inspector](https://docs.flutter.dev/tools/devtools/inspector)
- [Performance View](https://docs.flutter.dev/tools/devtools/performance)
- [Memory View](https://docs.flutter.dev/tools/devtools/memory)
- [Network View](https://docs.flutter.dev/tools/devtools/network)
