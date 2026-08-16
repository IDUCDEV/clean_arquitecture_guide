# 17 — Cheatsheet de DevTools

> Referencia rápida: herramientas, filtros, métricas, atajos y comandos de terminal para el día a día.

---

## 1. Herramientas de DevTools

| Herramienta | Propósito |
|---|---|
| **Inspector** | Widget tree y layout |
| **Performance** | Frame timing y jank |
| **CPU Profiler** | Uso de CPU por función |
| **Memory** | Uso de memoria y leaks |
| **Network** | Requests HTTP y WebSocket |
| **Debugger** | Breakpoints y control de ejecución |
| **Logging** | Logs de stdout/stderr |
| **App Size** | Tamaño del bundle |

---

## 2. Atajos y cómo abrir cada vista

| Acción | Cómo |
|---|---|
| Abrir DevTools | `Ctrl+Shift+P` → `Dart: Open DevTools` |
| Abrir la vista deseada | `Dart: Open DevTools` → elegir pestaña |
| Panel Run and Debug | `Ctrl+Shift+D` |
| Buscar en panel actual | `Ctrl+F` |
| Grabar profiling session | Botón **Record** en CPU Profiler / Performance |
| Recargar vista | Ctrl+R en la ventana de DevTools |

---

## 3. Sintaxis de filtros

### 3.1 Network View

| Filtro | Ejemplo | Descripción |
|---|---|---|
| `method:` | `method:GET` | Filtrar por método HTTP |
| `status:` | `status:200` | Filtrar por status code |
| `status:` | `status:4xx` | Filtrar por rango |
| `type:` | `type:document` | Filtrar por tipo de recurso |
| `url:` | `url:products` | Buscar en la URL |
| `content-type:` | `content-type:json` | Filtrar por content type |
| `-` | `-status:200` | Excluir filtro |

### 3.2 Logging View

| Filtro | Ejemplo | Descripción |
|---|---|---|
| Nivel mínimo | `WARNING` | Solo warnings o superiores |
| Texto | `auth` | Buscar en el mensaje |
| Tag propio | `[API]` | Filtrar por tag |

---

## 4. Métricas clave

### 4.1 Performance

| Métrica | Valor ideal | Significado |
|---|---|---|
| Frame time | < 16 ms | Sin jank |
| UI time | < 10 ms | Build/layout/paint eficiente |
| Raster time | < 6 ms | GPU rendering eficiente |
| Shader compilation | < 5 ms | Sin stuttering inicial |

### 4.2 Memory

| Métrica | Valor ideal | Significado |
|---|---|---|
| Dart Heap | < 50 MB | Uso razonable |
| Allocation rate | Estable | Sin leaks |
| GC frequency | Baja | Sin pressure |
| External | < 30 MB | Memoria nativa controlada |

### 4.3 CPU

| Métrica | Valor ideal | Significado |
|---|---|---|
| buildScope | < 5% CPU | Builds eficientes |
| layout | < 3% CPU | Layouts simples |
| paint | < 3% CPU | Pintura eficiente |
| GC | < 2% CPU | Sin pressure de memoria |

### 4.4 Network

| Métrica | Valor ideal | Significado |
|---|---|---|
| Response time | < 500 ms | APIs rápidas |
| Payload size | < 100 KB | Respuestas ligeras |
| Error rate | < 1% | APIs estables |

---

## 5. Iconos y colores

### 5.1 Performance View

| Color | Significado |
|---|---|
| Azul claro | UI thread |
| Azul oscuro | Raster thread |
| Verde | Frame dentro de budget |
| Rojo | Frame jank (fuera de budget) |

### 5.2 Memory View

| Color | Significado |
|---|---|
| Azul | Dart Heap |
| Verde | External |
| Amarillo | GPU |
| Gris | Reserved |

### 5.3 Network View

| Color | Status |
|---|---|
| Verde | 200–299 (Exitoso) |
| Amarillo | 300–399 (Redirect) |
| Rojo | 400–599 (Error) |

---

## 6. Uso típico por escenario de debugging

| Problema | Herramienta principal | Herramienta secundaria |
|---|---|---|
| UI no se ve bien | Inspector | Performance |
| App va lenta | Performance | CPU Profiler |
| Memory leak | Memory | CPU Profiler |
| API falla | Network | Logging |
| Crash | Logging | CPU Profiler |
| Tamaño grande | App Size | – |
| Layout overflow | Inspector | Performance |
| Animación jank | Performance | CPU Profiler |

---

## 7. Plantillas de código

### 7.1 Logging estructurado

```dart
// Tag consistente por feature
debugPrint('[AUTH] Login attempt');
debugPrint('[PRODUCTS] Loaded ${products.length} items');
debugPrint('[CART] Added item: ${item.id}');
debugPrint('[PAYMENT] Processing: $amount $currency');
```

### 7.2 Performance tracking

```dart
final stopwatch = Stopwatch()..start();
// ... operación ...
stopwatch.stop();
debugPrint('[PERF] operation: ${stopwatch.elapsedMilliseconds}ms');
```

### 7.3 Memory tracking

```dart
debugPrint('[MEM] Before: ${ProcessInfo.currentRssBytes}');
// ... operación que puede hacer leak ...
debugPrint('[MEM] After: ${ProcessInfo.currentRssBytes}');
```

### 7.4 Error logging

```dart
try {
  // ... código ...
} catch (e, stackTrace) {
  debugPrint('[ERROR] $runtimeType: $e');
  debugPrint('[STACK] $stackTrace');
  rethrow;
}
```

---

## 8. Comandos útiles de terminal

```bash
# Build con análisis de tamaño
flutter build apk --analyze-size
flutter build appbundle --analyze-size
flutter build ios --analyze-size

# Run con profiling
flutter run --profile
flutter run --profile --trace-skia

# DevTools desde la terminal (URI posicional del VM Service)
dart devtools http://127.0.0.1:8181/XXXXXX/

# Ver logs de Android
adb logcat -s flutter

# Ver logs de iOS
xcrun simctl spawn booted log stream --level=debug
```

---

## 9. Solución de problemas comunes

| Problema | Causa | Solución |
|---|---|---|
| DevTools no conecta | App en release mode | Usar `--debug` o `--profile` |
| Performance muestra 0 frames | No hay interacción | Interactuar con la app |
| Memory snapshot vacío | App recién iniciada | Esperar a que haya datos |
| Network no muestra requests | Requests nativos | Solo capta requests Dart |
| Logging no aparece | `print()` en release | Usar modo `--debug` |

---

## Resumen

1. DevTools se abre con `Dart: Open DevTools`
2. Cada vista tiene filtros: `method:`, `status:`, `url:`
3. Métricas de referencia: frame < 16 ms, heap < 50 MB
4. Colores: verde = bien, rojo = problema
5. `--analyze-size` para el reporte de tamaño

---

## 📚 Referencias

- [Flutter | DevTools overview](https://docs.flutter.dev/tools/devtools/overview) — Visión general de DevTools
- [Flutter | DevTools CLI](https://docs.flutter.dev/tools/devtools/cli) — Comandos de terminal
- [Flutter | Performance debugging](https://docs.flutter.dev/perf) — Guía de rendimiento

---

> 📖 **Siguiente:** [18-practicas-devtools.md](./18-practicas-devtools.md) — Buenas prácticas con DevTools
