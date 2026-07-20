# 01 - Fundamentos de Rendimiento

## Que es el rendimiento en Flutter

El rendimiento es la capacidad de tu app de **responder a la interaccion del usuario sin interrupciones visibles**. En Flutter, esto se mide fundamentalmente por la suavidad de las animaciones y la rapidez de respuesta a eventos.

### FPS (Frames Per Second)

Flutter dibuja la pantalla a **60 frames por segundo** en la mayoria de dispositivos (120 en dispositivos ProMotion). Cada frame debe rendersarse en un **frame budget** de:

```
60 FPS  → 16.67 ms por frame
120 FPS → 8.33 ms por frame
```

Si un frame toma mas tiempo, el usuario percibe **jank** (tartamudeo visual).

### Jank

El **jank** ocurre cuando Flutter no puede completar un frame dentro del budget:

```
Frame budget:  16.67ms
               ├──────────────────────────┤
Frame real:    ├────────────────────────────────────┤ 25ms
                                                    ↑
                                              JANK detectado
```

Hay dos tipos de jank:

| Tipo | Causa | Sintoma |
|---|---|---|
| **UI Jank** | Build/layout/paint lento en el frame principal | Frame rojo en DevTools |
| **Raster Jank** | Rasterizer (GPU) lento | Frame morado en DevTools |

---

## Metricas clave de rendimiento

| Metrica | Que mide | Rango saludable | DevTools View |
|---|---|---|---|
| **FPS** | Frames por segundo | >= 55 FPS | Performance |
| **Build time** | Tiempo para construir el widget tree | < 8ms | Performance > Enhance Tracing |
| **Raster time** | Tiempo para rasterizar en GPU | < 8ms | Performance > Enhance Tracing |
| **Frame budget** | Tiempo maximo por frame | 16.67ms (60Hz) | Performance Overlay |
| **Memory usage** | RAM utilizada por la app | Variable, sin crecimiento continuo | Memory |
| **Shader compilation** | Compilacion de shaders en tiempo real | Sin spikes visibles | Performance |
| **GC pauses** | Pausas por garbage collection | < 5ms, pocas frecuentes | Memory |

---

## Build modes: debug vs profile vs release

Flutter tiene tres modos de compilacion. **Nunca midas rendimiento en modo debug.**

| Caracteristica | Debug | Profile | Release |
|---|---|---|---|
| **Compilador** | Dart VM (JIT) | Dart AOT | Dart AOT |
| **Optimizaciones del compilador** | Ninguna | Mayoria | Todas |
| **assert() habilitado** | Si | No | No |
| **DevTools disponible** | Si | Si | No |
| **Performance Overlay** | Disponible | Disponible | Disponible |
| **asserts de framework** | Si | No | No |
| **Speed real** | ~10-100x mas lento | ~Identica a release | Referencia |
| **Para medir performance** | **NO** | **SI** | **SI** (pero sin DevTools) |
| **Para distribuir** | No | No | **SI** |

### Como ejecutar en profile

```bash
# Ejecutar en modo profile
flutter run --profile

# Build de release para testear
flutter build apk --release

# Ver tamano del build
flutter build apk --analyze-size
```

> **Regla de oro:** Siempre usa `flutter run --profile` para mediciones. El modo debug agrega overhead del JIT compiler que distorsiona todos los resultados.

---

## El pipeline de rendering de frames

Cada frame en Flutter pasa por este pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                      FRAME PIPELINE                             │
│                                                                 │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────┐  │
│  │  BUILD   │───>│  LAYOUT │───>│  PAINT  │───>│  COMPOSITE  │  │
│  │          │    │         │    │         │    │             │  │
│  │ Crea el  │    │ Calcula │    │ Dibuja  │    │ Combina     │  │
│  │ widget   │    │ tamano  │    │ pixels  │    │ capas en    │  │
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

### Que afecta cada fase

| Fase | Que hace | Donde se optimiza |
|---|---|---|
| **Build** | Llama a `build()` en cada widget | `const`, evitar `setState` innecesario |
| **Layout** | Calcula constraints y posicion | Evitar widgets con constraints costosos |
| **Paint** | Dibuja en el canvas | `RepaintBoundary`, `shouldRepaint` |
| **Composite** | Une capas en la GPU | Menos capas = menos trabajo GPU |

### UI Thread vs Raster Thread

```
┌──────────────────────────────────────────────────────────┐
│ UI Thread                                               │
│ ├── Framework (build, layout, paint)                    │
│ ├── Tu codigo Dart                                      │
│ └── BLoC/Cubit state changes                           │
│                                                         │
│ Raster Thread                                           │
│ ├── Skia/Impeller rendering                             │
│ ├── Shader compilation (puede causar jank!)             │
│ └── Texture uploads                                     │
└──────────────────────────────────────────────────────────┘
```

---

## El ciclo de vida del widget y su impacto

Cada widget tiene un ciclo de vida que afecta el rendimiento:

```
createElement()
    │
    ▼
mount()  ──────────────── Widget se inserta en el tree
    │                        ↑ Asigna Key aqui
    ▼
updateChild()  ──────────── Padre cambia, widget se actualiza
    │
    ▼
build()  ────────────────── Construye subtree (COSTOSO)
    │
    ▼
deactivate()  ──────────── Widget se remueve temporalmente
    │
    ▼
dispose()  ──────────────── Widget se destruye permanentemente
                              ↑ Libera recursos AQUI
```

### Impacto en rendimiento

| Evento | Impacto | Cada vez que ocurre |
|---|---|---|
| `build()` completo | Alto | Cada rebuild del widget |
| `setState()` | Medio-Alto | Marca subtree para rebuild |
| `initState()` | Medio | Solo una vez por widget |
| `dispose()` | Bajo | Solo una vez (pero fallar aqui = leak) |

---

## Cuando te importa el rendimiento

### Advertencia: optimizacion prematura

> "Premature optimization is the root of all evil" - Donald Knuth

**No optimices hasta que tengas un problema medible.** Usa esta guia:

```
Tu app tiene problemas de rendimiento?
├── NO puedo hacer scroll fluido → Optimizar
├── NO puedo cargar datos rapido → Optimizar
├── La app se siente "ok" → NO optimizar aun
└── No se sabe → MEDIR PRIMERO antes de tocar codigo
```

### Senales de que necesitas optimizar

| Sintoma | Probable causa | Urgencia |
|---|---|---|
| Scroll se congela momentaneamente | Build costoso en items visibles | Alta |
| Animaciones se ven "cortadas" | Frame budget excedido | Alta |
| Memoria crece sin parar | Memory leak | Alta |
| App tarda en iniciar | Work pesado en `initState` | Media |
| Transiciones entre pantallas lentas | Demasiados widgets o rebuilds | Media |
| App consume mucha bateria | Animaciones o streams innecesarios | Baja |

---

## Referencia rapida: metricas saludables

| Metrica | Excelente | Aceptable | Necesita optimizacion |
|---|---|---|---|
| FPS | 60 (120 en ProMotion) | 55-59 | < 55 |
| Build time | < 4ms | 4-8ms | > 8ms |
| Raster time | < 4ms | 4-8ms | > 8ms |
| Memory (idle) | < 100MB | 100-200MB | > 200MB |
| Memory growth | 0MB/min | < 1MB/min | > 1MB/min |
| GC frequency | < 1/min | 1-5/min | > 5/min |
| App startup | < 1s | 1-3s | > 3s |

---

## Comandos esenciales

```bash
# Ejecutar en profile para mediciones reales
flutter run --profile

# Ver el Performance Overlay en pantalla
# (se habilita con --profile o --release)
flutter run --profile --observatory-port=8080

# Analizar tamano del build
flutter build apk --analyze-size
flutter build ios --analyze-size

# Ver dependencias del proyecto
flutter pub deps
```

---

## Resumen

| Concepto | clave |
|---|---|
| **FPS** | 60 frames/segundo, 16.67ms por frame |
| **Jank** | Frame que excede el budget (UI o Raster) |
| **Build modes** | Nunca medir en debug, siempre profile |
| **Pipeline** | Build → Layout → Paint → Composite |
| **Optimizacion prematura** | Mide primero, optimiza despues |
| **DevTools** | Performance view para frames, Memory para memoria |
