# 19 — Fundamentos de Rendimiento

> Qué es el rendimiento en Flutter, por qué ocurre el jank y cómo medirlo correctamente (modo profile).

---

## 1. ¿Qué es el rendimiento en Flutter?

Es la capacidad de tu app de **responder a la interacción del usuario sin interrupciones visibles**. En Flutter, esto se mide fundamentalmente por la suavidad de las animaciones y la rapidez de respuesta a los eventos.

### 1.1 FPS (Frames Per Second)

Flutter dibuja la pantalla a **60 frames por segundo** en la mayoría de los dispositivos (120 en dispositivos ProMotion). Cada frame debe renderizarse dentro de un **frame budget**:

```
60 FPS  → 16.67 ms por frame
120 FPS → 8.33 ms por frame
```

Si un frame toma más tiempo, el usuario percibe **jank** (tartamudeo visual).

### 1.2 Jank

El **jank** ocurre cuando Flutter no puede completar un frame dentro del budget:

```
Frame budget:  16.67ms
               ├──────────────────────────┤
Frame real:    ├────────────────────────────────────┤ 25ms
                                                     ↑
                                               JANK detectado
```

Hay dos tipos de jank:

| Tipo | Causa | Síntoma |
|---|---|---|
| **UI Jank** | Build/layout/paint lento en el frame principal | Frame rojo en DevTools |
| **Raster Jank** | Rasterizer (GPU) lento | Frame morado en DevTools |

---

## 2. Métricas clave de rendimiento

| Métrica | Qué mide | Rango saludable | DevTools View |
|---|---|---|---|
| **FPS** | Frames por segundo | ≥ 55 FPS | Performance |
| **Build time** | Tiempo para construir el widget tree | < 8 ms | Performance > Enhanced Tracing |
| **Raster time** | Tiempo para rasterizar en GPU | < 8 ms | Performance > Enhanced Tracing |
| **Frame budget** | Tiempo máximo por frame | 16.67 ms (60 Hz) | Performance Overlay |
| **Memory usage** | RAM utilizada por la app | Variable, sin crecimiento continuo | Memory |
| **Shader compilation** | Compilación de shaders en tiempo real | Sin spikes visibles | Performance |
| **GC pauses** | Pausas por garbage collection | < 5 ms, poco frecuentes | Memory |

---

## 3. Build modes: debug vs profile vs release

Flutter tiene tres modos de compilación. **Nunca midas rendimiento en modo debug.**

| Característica | Debug | Profile | Release |
|---|---|---|---|
| **Compilador** | Dart VM (JIT) | Dart AOT | Dart AOT |
| **Optimizaciones del compilador** | Ninguna | Mayoría | Todas |
| **`assert()` habilitado** | Sí | No | No |
| **DevTools disponible** | Sí | Sí | No |
| **Performance Overlay** | Disponible | Disponible | Disponible |
| **asserts del framework** | Sí | No | No |
| **Velocidad real** | ~10-100x más lento | ~Idéntica a release | Referencia |
| **Para medir performance** | **NO** | **SÍ** | **SÍ** (pero sin DevTools) |
| **Para distribuir** | No | No | **SÍ** |

### 3.1 Cómo ejecutar en profile

```bash
# Ejecutar en modo profile
flutter run --profile

# Build de release para testear
flutter build apk --release

# Ver el tamaño del build
flutter build apk --analyze-size
```

> **Regla de oro:** usa siempre `flutter run --profile` para mediciones. El modo debug agrega overhead del JIT compiler que distorsiona todos los resultados.

---

## 4. El pipeline de rendering de frames

Cada frame en Flutter pasa por este pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRAME PIPELINE                             │
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────┐  │
│  │  BUILD   │───>│  LAYOUT │───>│  PAINT  │───>│  COMPOSITE  │  │
│  │          │    │         │    │         │    │             │  │
│  │ Crea el  │    │ Calcula │    │ Dibuja  │    │ Combina     │  │
│  │ widget   │    │ tamaño  │    │ pixels  │    │ capas en    │  │
│  │ tree     │    │ y pos   │    │ en cada │    │ la GPU      │  │
│  │          │    │ de cada │    │ capa    │    │             │  │
│  │          │    │ widget  │    │         │    │             │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────────┘  │
│      │              │              │                │           │
│      ▼              ▼              ▼                ▼           │
│  CPU Thread    CPU Thread    CPU Thread      GPU Thread        │
│  (UI thread)   (UI thread)  (UI thread)     (Raster thread)   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.1 Qué afecta cada fase

| Fase | Qué hace | Dónde se optimiza |
|---|---|---|
| **Build** | Llama a `build()` en cada widget | `const`, evitar `setState` innecesario |
| **Layout** | Calcula constraints y posición | Evitar widgets con constraints costosos |
| **Paint** | Dibuja en el canvas | `RepaintBoundary`, `shouldRepaint` |
| **Composite** | Une capas en la GPU | Menos capas = menos trabajo GPU |

### 4.2 UI Thread vs Raster Thread

```
┌──────────────────────────────────────────────────────────┐
│ UI Thread                                               │
│ ├── Framework (build, layout, paint)                    │
│ ├── Tu código Dart                                      │
│ └── BLoC/Cubit state changes                            │
│                                                         │
│ Raster Thread                                           │
│ ├── Skia/Impeller rendering                             │
│ ├── Shader compilation (puede causar jank!)             │
│ └── Texture uploads                                     │
└──────────────────────────────────────────────────────────┘
```

---

## 5. El ciclo de vida del widget y su impacto

Cada widget tiene un ciclo de vida que afecta el rendimiento:

```
createElement()
    │
    ▼
mount()  ──────────────── Widget se inserta en el tree
    │                        ↑ Asigna Key aquí
    ▼
updateChild()  ──────────── El padre cambia, el widget se actualiza
    │
    ▼
build()  ────────────────── Construye subtree (COSTOSO)
    │
    ▼
deactivate()  ──────────── Widget se remueve temporalmente
    │
    ▼
dispose()  ──────────────── Widget se destruye permanentemente
                              ↑ Libera recursos AQUÍ
```

### 5.1 Impacto en rendimiento

| Evento | Impacto | Cada vez que ocurre |
|---|---|---|
| `build()` completo | Alto | Cada rebuild del widget |
| `setState()` | Medio-Alto | Marca subtree para rebuild |
| `initState()` | Medio | Solo una vez por widget |
| `dispose()` | Bajo | Solo una vez (pero fallar aquí = leak) |

---

## 6. Cuándo te importa el rendimiento

### 6.1 Advertencia: optimización prematura

> "Premature optimization is the root of all evil" — Donald Knuth

**No optimices hasta que tengas un problema medible.** Usa esta guía:

```
Tu app tiene problemas de rendimiento?
├── NO puedo hacer scroll fluido → Optimizar
├── NO puedo cargar datos rápido → Optimizar
├── La app se siente "ok" → NO optimizar aún
└── No se sabe → MEDIR PRIMERO antes de tocar código
```

### 6.2 Señales de que necesitas optimizar

| Síntoma | Probable causa | Urgencia |
|---|---|---|
| Scroll se congela momentáneamente | Build costoso en items visibles | Alta |
| Animaciones se ven "cortadas" | Frame budget excedido | Alta |
| Memoria crece sin parar | Memory leak | Alta |
| App tarda en iniciar | Trabajo pesado en `initState` | Media |
| Transiciones entre pantallas lentas | Demasiados widgets o rebuilds | Media |
| App consume mucha batería | Animaciones o streams innecesarios | Baja |

---

## 7. Referencia rápida: métricas saludables

| Métrica | Excelente | Aceptable | Necesita optimización |
|---|---|---|---|
| FPS | 60 (120 en ProMotion) | 55-59 | < 55 |
| Build time | < 4 ms | 4-8 ms | > 8 ms |
| Raster time | < 4 ms | 4-8 ms | > 8 ms |
| Memory (idle) | < 100 MB | 100-200 MB | > 200 MB |
| Memory growth | 0 MB/min | < 1 MB/min | > 1 MB/min |
| GC frequency | < 1/min | 1-5/min | > 5/min |
| App startup | < 1 s | 1-3 s | > 3 s |

---

## 8. Comandos esenciales

```bash
# Ejecutar en profile para mediciones reales
flutter run --profile

# Alternar el Performance Overlay en la app
# (botón en la barra de DevTools o:
# Performance Overlay con M en la consola de flutter run)

# Analizar el tamaño del build
flutter build apk --analyze-size
flutter build ios --analyze-size

# Ver dependencias del proyecto
flutter pub deps
```

---

## Resumen

| Concepto | Clave |
|---|---|
| **FPS** | 60 frames/segundo, 16.67 ms por frame |
| **Jank** | Frame que excede el budget (UI o Raster) |
| **Build modes** | Nunca medir en debug, siempre profile |
| **Pipeline** | Build → Layout → Paint → Composite |
| **Optimización prematura** | Mide primero, optimiza después |
| **DevTools** | Performance view para frames, Memory para memoria |

---

## 📚 Referencias

- [Flutter | Performance best practices](https://docs.flutter.dev/perf/best-practices) — Buenas prácticas de rendimiento
- [Flutter | Profiling](https://docs.flutter.dev/perf/ui-performance) — Cómo medir el rendimiento de UI
- [Flutter | Build modes](https://docs.flutter.dev/testing/build-modes) — Diferencias entre debug, profile y release

---

> 📖 **Siguiente:** [20-optimizar-rebuilds.md](./20-optimizar-rebuilds.md) — Optimizando rebuilds innecesarios
