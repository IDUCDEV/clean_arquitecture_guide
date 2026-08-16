# Módulo 18: Debugging con VS Code y Flutter DevTools

> El debugging es la habilidad que separa a un desarrollador junior de uno senior. No se trata solo de encontrar errores, sino de **entender el comportamiento de tu aplicación** en tiempo real, diagnosticar problemas de performance, detectar memory leaks y optimizar cada aspecto de tu app.

Este módulo cubre las dos herramientas fundamentales del ecosistema Flutter:

1. **VS Code Debugging** — El debugger integrado en tu IDE
2. **Flutter DevTools** — La suite completa de profiling y diagnóstico

---

## Mapa mental: cuándo usar qué

```
Estoy escribiendo código y necesito pausar la ejecución
  └── VS Code Debugger (F5, breakpoints, stepping)

Mi app se siente lenta o tiene jank
  └── DevTools > Performance View

Sospecho un memory leak
  └── DevTools > Memory View

Un request HTTP falla o es lento
  └── DevTools > Network View

No entiendo por qué un widget se ve mal
  └── DevTools > Flutter Inspector

Quiero saber qué función consume más CPU
  └── DevTools > CPU Profiler

Mi app pesa demasiado
  └── DevTools > App Size Tool

Necesito ver logs detallados
  └── DevTools > Logging View
```

---

## Requisitos previos

| Módulo | Por qué |
|---|---|
| [05-TESTING](../05-TESTING/) | Testing y debugging se complementan |
| [16-BLOC-CUBIT](../16-BLOC-CUBIT/) | Debugging de BLoC/Cubit es escenario principal |
| [01-CLEAN-ARCHITECTURE](../01-CLEAN-ARCHITECTURE/) | Entender capas para saber dónde poner breakpoints |
| [03-SUPABASE](../03-SUPABASE/) | Debugging de llamadas a Supabase |

---

## Contenido del módulo

### Los 26 capítulos

| # | Archivo | Descripción |
|---|---|---|
| 1 | [01-fundamentos-debugging.md](./01-fundamentos-debugging.md) | Fundamentos del debugging en Flutter |
| 2 | [02-configuracion-launch-json.md](./02-configuracion-launch-json.md) | Configuración de launch.json |
| 3 | [03-breakpoints-avanzados.md](./03-breakpoints-avanzados.md) | Breakpoints avanzados en VS Code |
| 4 | [04-inspeccion-datos-consola.md](./04-inspeccion-datos-consola.md) | Inspección de datos en la consola |
| 5 | [05-multi-target-remoto.md](./05-multi-target-remoto.md) | Multi-target y debugging remoto |
| 6 | [06-cheatsheet-vscode.md](./06-cheatsheet-vscode.md) | Cheatsheet de debugging en VS Code |
| 7 | [07-practicas-vscode.md](./07-practicas-vscode.md) | Prácticas de debugging en VS Code |
| 8 | [08-fundamentos-devtools.md](./08-fundamentos-devtools.md) | Fundamentos de Flutter DevTools |
| 9 | [09-inspector-layout.md](./09-inspector-layout.md) | Flutter Inspector y layout |
| 10 | [10-performance-view.md](./10-performance-view.md) | Performance View: frames y jank |
| 11 | [11-cpu-profiler.md](./11-cpu-profiler.md) | CPU Profiler y flame charts |
| 12 | [12-memory-profiler.md](./12-memory-profiler.md) | Memory View: heap, leaks y GC |
| 13 | [13-network-view.md](./13-network-view.md) | Network View: requests HTTP |
| 14 | [14-debugger-view.md](./14-debugger-view.md) | Debugger View en DevTools |
| 15 | [15-logging-view.md](./15-logging-view.md) | Logging View |
| 16 | [16-app-size.md](./16-app-size.md) | App Size: reducir el tamaño |
| 17 | [17-cheatsheet-devtools.md](./17-cheatsheet-devtools.md) | Cheatsheet de DevTools |
| 18 | [18-practicas-devtools.md](./18-practicas-devtools.md) | Prácticas con DevTools |
| 19 | [19-fundamentos-rendimiento.md](./19-fundamentos-rendimiento.md) | Fundamentos de rendimiento |
| 20 | [20-optimizar-rebuilds.md](./20-optimizar-rebuilds.md) | Optimizar rebuilds |
| 21 | [21-memory-leak-detection.md](./21-memory-leak-detection.md) | Detección de memory leaks |
| 22 | [22-rendering-complejo.md](./22-rendering-complejo.md) | Rendering complejo: listas y slivers |
| 23 | [23-cheatsheet-optimizacion.md](./23-cheatsheet-optimizacion.md) | Cheatsheet de optimización |
| 24 | [24-practicas-optimizacion.md](./24-practicas-optimizacion.md) | Prácticas de optimización |
| 25 | [25-debugging-asincrono.md](./25-debugging-asincrono.md) | Debugging asíncrono |
| 26 | [26-workflow-debugging-por-tipo.md](./26-workflow-debugging-por-tipo.md) | Workflow por tipo de bug |

### Progresión recomendada

```
Fase 1: Fundamentos (VS Code)
  ├── fundamentos -> launch.json -> breakpoints
  └── inspección de datos -> multi-target

Fase 2: DevTools
  ├── fundamentos -> inspector -> performance
  └── CPU profiler -> memory -> network -> logging -> app size

Fase 3: Rendimiento
  ├── fundamentos de rendimiento -> optimizar rebuilds
  └── memory leaks -> rendering complejo

Fase 4: Maestría
  ├── cheatsheets + prácticas
  └── debugging asíncrono -> workflow por tipo de bug
```

---

## Herramientas que necesitas

| Herramienta | Versión mínima | Para qué |
|---|---|---|
| VS Code | 1.80+ | IDE con debugger integrado |
| Extensión Dart | latest | Debugging Dart/Flutter |
| Extensión Flutter | latest | Soporte Flutter en VS Code |
| Flutter SDK | 3.22+ | DevTools incluido |
| DevTools | 2.23+ | Suite de profiling |

---

## Convenciones en este módulo

- Los ejemplos usan **Clean Architecture** (ver módulo 01)
- State management: **BLoC/Cubit** (ver módulo 16)
- Backend: **Supabase** (ver módulo 03)
- Los escenarios prácticos son **reales y reproducibles**
- Cada cheatsheet es una **referencia rápida imprimible**
- Todas las mediciones de rendimiento se hacen en **profile mode** (`flutter run --profile`)

---

## Fuentes oficiales

- [VS Code Debugging](https://code.visualstudio.com/docs/debugtest/debugging)
- [Flutter DevTools](https://docs.flutter.dev/tools/devtools)
- [Flutter Inspector](https://docs.flutter.dev/tools/devtools/inspector)
- [Performance View](https://docs.flutter.dev/tools/devtools/performance)
- [Memory View](https://docs.flutter.dev/tools/devtools/memory)
- [Network View](https://docs.flutter.dev/tools/devtools/network)
