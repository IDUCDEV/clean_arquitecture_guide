# 12 — Memory Profiler: Leaks y Uso de Memoria

> Monitorear el uso de memoria en tiempo real, tomar heap snapshots y detectar memory leaks con diffs y tracing.

---

## 1. ¿Qué es el Memory Profiler?

Herramienta para monitorear el uso de memoria en tiempo real, identificar memory leaks y analizar heap dumps. Una gestión eficiente de memoria evita crashes por OOM (Out of Memory).

---

## 2. Conceptos básicos

### 2.1 Memoria en Dart/Flutter

| Concepto | Descripción |
|---|---|
| **Dart Heap** | Memoria donde viven los objetos Dart |
| **External** | Memoria fuera del heap Dart (nativa, imágenes) |
| **GPU** | Memoria usada por la GPU para rendering |
| **Total** | Suma de todos los anteriores |

### 2.2 Lifecycle de memoria

```
┌─────────────┐
│ Allocation  │ → Objeto creado, memoria asignada
├─────────────┤
│ Use         │ → Objeto en uso activo
├─────────────┤
│ GC (Mark)   │ → GC identifica objetos vivos
├─────────────┤
│ GC (Sweep)  │ → GC libera objetos no referenciados
└─────────────┘
```

### 2.3 Tipos de memory leaks

| Tipo | Descripción | Ejemplo |
|---|---|---|
| **Reference leak** | Objeto referenciado innecesariamente | Controller sin dispose |
| **Closure leak** | Closure captura una variable que mantiene el objeto vivo | Timer sin cancel |
| **Stream leak** | Stream subscription sin cancel | `StreamSubscription` sin dispose |
| **Image leak** | Imágenes cargadas sin liberar | `ImageProvider` sin eviction |

---

## 3. Memory View — Pestañas

| Pestaña | Propósito |
|---|---|
| **Chart** | Gráfico de memoria en tiempo real |
| **Snapshot** | Heap snapshot para análisis |
| **Diff** | Comparar dos snapshots |
| **Trace** | Tracking de allocaciones específicas |

---

## 4. Memory Chart

### 4.1 Qué muestra

```
Memory (MB)
    ▲
 50 │              ┌──────┐
 40 │         ┌────┘      └────┐
 30 │    ┌────┘                └────┐
 20 │────┘                          └────
 10 │
  0 └──────────────────────────────────────→ Time
     T1     T2     T3     T4     T5

─── Dart Heap    ─── External    ─── GPU
```

### 4.2 Métricas en tiempo real

| Métrica | Descripción |
|---|---|
| **Dart Heap** | Tamaño actual del heap Dart |
| **Dart Heap Limit** | Límite máximo del heap |
| **External** | Memoria nativa (imágenes, etc.) |
| **GPU** | Memoria de rendering |
| **Allocation Rate** | Velocidad de nuevas asignaciones |
| **GC Frequency** | Frecuencia de garbage collection |

### 4.3 Interpretación del gráfico

| Patrón | Significado |
|---|---|
| Subida gradual constante | Memory leak probable |
| Picos seguidos de bajada | GC funcionando normal |
| Plateau sin bajada | Memoria retenida sin liberar |
| Subida exponencial | Asignación excesiva, crítico |

---

## 5. Heap Snapshots

### 5.1 ¿Qué es un heap snapshot?

Captura del estado completo del heap en un momento dado. Contiene todos los objetos vivos y sus referencias.

### 5.2 Cómo tomar un snapshot

1. Memory View → click en **Take Snapshot** (📸)
2. Esperar a que se procese
3. Analizar resultados

### 5.3 Contenido del snapshot

```
Heap Snapshot: 12,345 objects

Retained Size: 2.3 MB

Classes:
┌────────────────────────────┬───────────┬───────────┬───────────┐
│ Class                       │ Instances │ Retained  │ Shallow   │
├────────────────────────────┼───────────┼───────────┼───────────┤
│ _ListNode<int>              │ 5,432     │ 432 KB    │ 216 KB    │
│ Picture                     │ 234       │ 512 KB    │ 117 KB    │
│ ImageStreamCompleter        │ 89        │ 340 KB    │ 44 KB     │
│ _GradientTransform          │ 156       │ 187 KB    │ 93 KB     │
│ Uint8List                   │ 67        │ 156 KB    │ 78 KB     │
└────────────────────────────┴───────────┴───────────┴───────────┘
```

### 5.4 Métricas clave

| Métrica | Descripción |
|---|---|
| **Retained Size** | Memoria total retenida (objeto + todo lo que referencia) |
| **Shallow Size** | Memoria solo del objeto (sin referencias) |
| **Instances** | Número de instancias de esa clase |

### 5.5 Tips para analizar

1. Ordenar por **Retained Size** para ver qué consume más
2. Expandir la clase para ver instancias individuales
3. Click en la instancia para ver referencias (qué la mantiene viva)
4. Buscar patrones: muchas instancias de una clase = posible leak

---

## 6. Memory Diff

### 6.1 ¿Qué es?

Compara dos snapshots para ver qué cambió: objetos nuevos, eliminados y cuánta memoria se incrementó/decrementó.

### 6.2 Cómo usar

1. Tomar snapshot A (baseline)
2. Interactuar con la app (navegar, abrir/cerrar pantallas)
3. Tomar snapshot B
4. Ver el diff: qué se agregó, qué se eliminó

### 6.3 Resultado del diff

```
Comparison: Snapshot A → Snapshot B

Added:
┌────────────────────────────┬───────────┬───────────┐
│ Class                       │ Instances │ Size      │
├────────────────────────────┼───────────┼───────────┤
│ _Route                      │ 3         │ 12 KB     │  ← Nuevas rutas
│ ProductModel                │ 47        │ 89 KB     │  ← Carga de datos
│ ImageStreamCompleter        │ 12        │ 45 KB     │  ← Imágenes cargadas
└────────────────────────────┴───────────┴───────────┘

Deleted:
┌────────────────────────────┬───────────┬───────────┐
│ Class                       │ Instances │ Size      │
├────────────────────────────┼───────────┼───────────┤
│ ProductModel                │ 23        │ 44 KB     │  ← Viejos datos
└────────────────────────────┴───────────┴───────────┘

Net Change: +123 KB
```

### 6.4 Detectando memory leaks con Diff

**Escenario:** navegar a una pantalla 10 veces

```
Snapshot A: Baseline
Snapshot B: Después de 10 navegaciones

Resultado:
- _Route: +10 instances  ← ¡Leak! Las rutas no se eliminan
- ProductModel: +100 instances ← ¡Leak! Datos cacheados sin límite
```

**Fix:**

```dart
// Con GoRouter, asegurar que los controllers/scopes se limpien al salir
GoRoute(
  path: '/products/:id',
  builder: (context, state) {
    return BlocProvider(
      create: (context) => getIt<ProductBloc>(),
      child: ProductScreen(),  // Sus recursos se dispose al salir
    );
  },
)
```

---

## 7. Trace (Allocation Tracing)

### 7.1 ¿Qué es?

Tracking en tiempo real de cuándo se crean y destruyen objetos de una clase específica.

### 7.2 Cómo usar

1. Click en la pestaña **Trace**
2. Agregar la clase a monitorear (ej: `ProductModel`)
3. Interactuar con la app
4. Ver el gráfico de allocaciones vs deallocations

### 7.3 Resultado

```
ProductModel Allocation Trace

Allocations:    ████████████████████  200
Deallocations:  ████████████████      160
Live:           ████                  40   ← ¡Posible leak!

Timeline:
  T1: +10 allocated
  T2: +5 allocated, -3 deallocated
  T3: +15 allocated
  T4: +8 allocated, -12 deallocated
  ...
```

### 7.4 Interpretación

- **Allocations > Deallocations constantemente** → Memory leak
- **Allocations ≈ Deallocations** → Memoria sana
- **Picos de allocations** → Momentos de alta carga (carga de lista, imágenes)

---

## 8. Problemas comunes de memoria en Flutter

### 8.1 Controllers sin dispose

```dart
// ❌ Memory leak
class MyScreen extends StatelessWidget {
  final _controller = TextEditingController();  // Nunca se dispone

  @override
  Widget build(BuildContext context) {
    return TextField(controller: _controller);
  }
}

// ✅ Correcto
class MyScreen extends StatefulWidget {
  @override
  State<MyScreen> createState() => _MyScreenState();
}

class _MyScreenState extends State<MyScreen> {
  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();  // ← Importante
    super.dispose();
  }
}
```

### 8.2 Streams sin cancel

```dart
// ❌ Memory leak: subscription que nunca se cancela
class _MyScreenState extends State<MyScreen> {
  @override
  void initState() {
    super.initState();
    myStream().listen((event) {
      // Se ejecuta indefinidamente
    });
  }
}

// ✅ Correcto
class _MyScreenState extends State<MyScreen> {
  StreamSubscription? _subscription;

  @override
  void initState() {
    super.initState();
    _subscription = myStream().listen((event) {
      // Manejar el evento
    });
  }

  @override
  void dispose() {
    _subscription?.cancel();  // ← Importante
    super.dispose();
  }
}
```

### 8.3 Imágenes sin cache eviction

```dart
// ❌ Acumula imágenes en memoria
ListView.builder(
  itemCount: 1000,
  itemBuilder: (context, i) {
    return Image.network('https://example.com/image_$i.jpg');
    // Cada imagen se mantiene en memoria
  },
)

// ✅ Con límite de cache
// Usa el cacheWidth para decodificar más pequeño:
Image.network('https://example.com/image_$i.jpg', cacheWidth: 300)

// O un cacheManager con límite de objetos y eviction:
CachedNetworkImage(
  imageUrl: 'https://example.com/image_$i.jpg',
  cacheManager: CacheManager(
    Config(
      'uniqueCacheKey',
      stalePeriod: Duration(days: 7),
      maxNrOfCacheObjects: 100,  // ← Límite + eviction automática
    ),
  ),
)
```

---

## 9. Ejercicios prácticos

### 9.1 Ejercicio 1: detectar memory leak

1. Crear pantalla con `TextEditingController`
2. Navegar a esa pantalla 10 veces
3. Tomar snapshot después de cada navegación
4. Verificar si las instancias de `TextEditingController` aumentan
5. Fix con `dispose()`

### 9.2 Ejercicio 2: memory diff de carga de datos

1. Tomar snapshot baseline
2. Cargar lista de 100 productos desde API
3. Tomar segundo snapshot
4. Analizar cuánta memoria consumen los productos
5. Evaluar si es aceptable

### 9.3 Ejercicio 3: trace de imágenes

1. Crear pantalla con 20 imágenes de red
2. Monitorear allocaciones de `ImageStreamCompleter`
3. Navegar fuera de la pantalla
4. Verificar si las imágenes se liberan
5. Implementar cache eviction si no se liberan

---

## Resumen

| Concepto | Punto clave |
|---|---|
| Dart Heap vs External | Objetos Dart vs memoria nativa (imágenes) |
| Snapshot | Estado completo del heap en un momento |
| Diff | Compara dos snapshots para detectar leaks |
| Trace | Sigue allocaciones/deallocations por clase |
| Fix típico | `dispose()`, `cancel()`, cache con límites |

---

## 📚 Referencias

- [Flutter | Memory view](https://docs.flutter.dev/tools/devtools/memory) — Documentación oficial de la Memory view
- [Flutter | Memory, leaks y perfiles](https://docs.flutter.dev/perf/memory) — Conceptos de memoria en Flutter
- [Flutter | Repainting y cachés de imágenes](https://docs.flutter.dev/perf/images) — Cómo Flutter cachea imágenes

---

> 📖 **Siguiente:** [13-network-view.md](./13-network-view.md) — Network view: requests HTTP y WebSocket
