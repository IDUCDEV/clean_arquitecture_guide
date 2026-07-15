# 10 - Cheatsheet: Flutter DevTools

## Herramientas de DevTools

| Herramienta | Atajo | Propósito |
|-------------|-------|-----------|
| **Inspector** | Ctrl+Shift+D | Widget tree y layout |
| **Performance** | Ctrl+Shift+P → Performance | Frame timing y jank |
| **CPU Profiler** | Ctrl+Shift+P → CPU | Uso de CPU por función |
| **Memory** | Ctrl+Shift+P → Memory | Uso de memoria y leaks |
| **Network** | Ctrl+Shift+P → Network | Requests HTTP y WebSocket |
| **Debugger** | Ctrl+Shift+P → Debugger | Breakpoints alternativos |
| **Logging** | Ctrl+Shift+P → Logging | Logs de stdout/stderr |
| **App Size** | Ctrl+Shift+P → App Size | Tamaño del bundle |

---

## Atajos de teclado DevTools

| Atajo | Acción |
|-------|--------|
| `Ctrl+Shift+D` | Abrir DevTools |
| `Ctrl+Shift+R` | Grabar profiling session |
| `Ctrl+Shift+P` | Command Palette en DevTools |
| `F5` | Recargar DevTools |
| `Ctrl+F` | Buscar en panel actual |

---

## Sintaxis de filtros

### Network View

| Filtro | Ejemplo | Descripción |
|--------|---------|-------------|
| `method:` | `method:GET` | Filtrar por método HTTP |
| `status:` | `status:200` | Filtrar por status code |
| `status:` | `status:4xx` | Filtrar por rango |
| `type:` | `type:document` | Filtrar por tipo de recurso |
| `url:` | `url:products` | Buscar en URL |
| `content-type:` | `content-type:json` | Filtrar por content type |
| `-` | `-status:200` | Excluir filtro |

### Logging View

| Filtro | Ejemplo | Descripción |
|--------|---------|-------------|
| `level:` | `level:WARNING` | Nivel mínimo |
| `message:` | `message:auth` | Buscar en mensaje |

---

## Métricas clave

### Performance

| Métrica | Valor ideal | Significado |
|---------|-------------|-------------|
| Frame time | < 16ms | Sin jank |
| UI time | < 10ms | Build/layout/paint eficiente |
| Raster time | < 6ms | GPU rendering eficiente |
| Shader compilation | < 5ms | Sin stuttering inicial |

### Memory

| Métrica | Valor ideal | Significado |
|---------|-------------|-------------|
| Dart Heap | < 50MB | Uso razonable |
| Allocation rate | Estable | Sin leaks |
| GC frequency | Baja | Sin pressure |
| External | < 30MB | Memoria nativa controlada |

### CPU

| Métrica | Valor ideal | Significado |
|---------|-------------|-------------|
| buildScope | < 5% CPU | Builds eficientes |
| layout | < 3% CPU | Layouts simples |
| paint | < 3% CPU | Pintura eficiente |
| GC | < 2% CPU | Sin pressure de memoria |

### Network

| Métrica | Valor ideal | Significado |
|---------|-------------|-------------|
| Response time | < 500ms | APIs rápidas |
| Payload size | < 100KB | Respuestas ligeras |
| Error rate | < 1% | APIs estables |

---

## Iconos y colores

### Performance View

| Color | Significado |
|-------|-------------|
| 🟦 Azul claro | UI thread |
| 🟦 Azul oscuro | Raster thread |
| 🟩 Verde | Frame dentro de budget |
| 🔴 Rojo | Frame jank (fuera de budget) |

### Memory View

| Color | Significado |
|-------|-------------|
| 🟦 Azul | Dart Heap |
| 🟩 Verde | External |
| 🟨 Amarillo | GPU |
| ⬜ Gris | Reserved |

### Network View

| Color | Status |
|-------|--------|
| 🟢 Verde | 200-299 (Exitoso) |
| 🟡 Amarillo | 300-399 (Redirect) |
| 🔴 Rojo | 400-599 (Error) |

---

## Uso típico por debugging scenario

| Problema | Herramienta principal | Herramienta secundaria |
|----------|----------------------|------------------------|
| UI no se ve bien | Inspector | Performance |
| App va lenta | Performance | CPU Profiler |
| Memory leak | Memory | CPU Profiler |
| API falla | Network | Logging |
| Crash | Logging | CPU Profiler |
| Tamaño grande | App Size | - |
| Layout overflow | Inspector | Performance |
| Animación jank | Performance | CPU Profiler |

---

## Plantillas de código

### Logging estructurado

```dart
// Tag consistente por feature
debugPrint('[AUTH] Login attempt');
debugPrint('[PRODUCTS] Loaded ${products.length} items');
debugPrint('[CART] Added item: ${item.id}');
debugPrint('[PAYMENT] Processing: ${amount} ${currency}');
```

### Performance tracking

```dart
final stopwatch = Stopwatch()..start();
// ... operación ...
stopwatch.stop();
debugPrint('[PERF] operation: ${stopwatch.elapsedMilliseconds}ms');
```

### Memory tracking

```dart
debugPrint('[MEM] Before: ${ProcessInfo.currentRss}');
// ... operación que puede leak ...
debugPrint('[MEM] After: ${ProcessInfo.currentRss}');
```

### Error logging

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

## Comandos útiles de terminal

```bash
# Build con análisis de tamaño
flutter build apk --analyze-size
flutter build ios --analyze-size
flutter build appbundle --analyze-size

# Run con profiling
flutter run --profile
flutter run --profile --trace-skia

# DevTools desde terminal
dart devtools --vm-service-uri=http://127.0.0.1:8181

# Ver logs de Android
adb logcat -s flutter

# Ver logs de iOS
xcrun simctl spawn booted log stream --level=debug
```

---

## Solución de problemas comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| DevTools no conecta | App en release mode | Usar `--debug` o `--profile` |
| Performance muestra 0 frames | No hay interacción | Interactuar con la app |
| Memory snapshot vacío | App recién iniciada | Esperar a que haya datos |
| Network no muestra requests | Requests nativos | Solo capta requests Dart |
| Logging no aparece | print() en release | Usar `--debug` mode |

---
→ Siguiente: `11-practicas-devtools.md`
