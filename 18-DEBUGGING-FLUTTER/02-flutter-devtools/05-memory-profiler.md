# 05 - Memory Profiler

## ¿Qué es el Memory Profiler?

Herramienta para monitorear uso de memoria en tiempo real, identificar memory leaks, y analizar heap dumps. La gestión eficiente de memoria evita crashes por OOM (Out of Memory).

---

## Concepts básicos

### Memory en Dart/Flutter

| Concepto | Descripción |
|----------|-------------|
| **Dart Heap** | Memoria donde viven objetos Dart |
| **External** | Memoria fuera del heap Dart (nativa, imágenes) |
| **GPU** | Memoria usada por el GPU para rendering |
| **Total** | Suma de todos los anteriores |

### Lifecycle de memoria

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

### Tipos de memory leaks

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Reference leak** | Objeto referenciado innecesariamente | Controller sin dispose |
| **Closure leak** | Closure captura variable que mantiene objeto vivo | Timer sin cancel |
| **Stream leak** | Stream subscription sin cancel | StreamSubscription sin dispose |
| **Image leak** | Imágenes cargadas sin liberar | ImageProvider sin eviction |

---

## Memory View - Pestañas

| Pestaña | Propósito |
|---------|-----------|
| **Chart** | Gráfico de memoria en tiempo real |
| **Snapshot** | Heap snapshot para análisis |
| **Diff** | Comparar dos snapshots |
| **Trace** | Tracking de allocaciones específicas |

---

## Memory Chart

### Qué muestra

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

### Métricas en tiempo real

| Métrica | Descripción |
|---------|-------------|
| **Dart Heap** | Tamaño actual del heap Dart |
| **Dart Heap Limit** | Límite máximo del heap |
| **External** | Memoria nativa (imágenes, etc.) |
| **GPU** | Memoria de rendering |
| **Allocation Rate** | Velocidad de nuevas asignaciones |
| **GC Frequency** | Frecuencia de garbage collection |

### Interpretación del gráfico

| Patrón | Significado |
|--------|-------------|
| Subida gradual constante | Memory leak probable |
| Picos seguidos de bajada | GC funcionando normal |
| Plateau sin bajada | Memoria retenida sin liberar |
| Subida exponencial | Asignación excesiva, crítico |

---

## Heap Snapshots

### ¿Qué es un heap snapshot?
Captura del estado completo del heap en un momento dado. Contiene todos los objetos vivos y sus referencias.

### Cómo tomar un snapshot
1. Memory View → Click en "Take Snapshot" (📸)
2. Esperar a que se procese
3. Analizar resultados

### Contenido del snapshot

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
│ Uint8List                    │ 67        │ 156 KB    │ 78 KB     │
└────────────────────────────┴───────────┴───────────┴───────────┘
```

### Métricas clave

| Métrica | Descripción |
|---------|-------------|
| **Retained Size** | Memoria total retenida (objeto + todo lo que referencia) |
| **Shallow Size** | Memoria solo del objeto (sin referencias) |
| **Instances** | Número de instancias de esa clase |

### Tips para analizar
1. Ordenar por **Retained Size** para ver qué consume más
2. Expandir clase para ver instancias individuales
3. Click en instancia para ver referencias (qué la mantiene viva)
4. Buscar patrones: muchas instancias de una clase = posible leak

---

## Memory Diff

### ¿Qué es?
Compara dos snapshots para ver qué cambió. Identifica nuevos objetos, eliminados, y cuánta memoria se incrementó/decrementó.

### Cómo usar
1. Tomar snapshot A (baseline)
2. Interactuar con la app (navegar, abrir/cerrar pantallas)
3. Tomar snapshot B
4. Ver diff: qué se agregó, qué se eliminó

### Resultado del diff

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

### Detectando memory leaks con Diff

**Escenario**: Navegar a una pantalla 10 veces

```
Snapshot A: Baseline
Snapshot B: Después de 10 navigations

Resultado:
- _Route: +10 instances  ← ¡Leak! Las rutas no se eliminan
- ProductModel: +100 instances ← ¡Leak! Datos cacheados sin límite
```

**Fix**:
```dart
// En GoRouter, asegurar que las pantallas se dispose correctamente
GoRoute(
  path: '/products/:id',
  builder: (context, state) {
    return BlocProvider(
      create: (context) => getIt<ProductBloc>(),
      child: ProductScreen(),  // Se dispose al salir
    );
  },
)
```

---

## Trace (Allocation Tracing)

### ¿Qué es?
Tracking en tiempo real de cuando se crean y destruyen objetos de una clase específica.

### Cómo usar
1. Click en "Trace" tab
2. Agregar clase a monitorear (ej: `ProductModel`)
3. Interactuar con la app
4. Ver gráfico de allocaciones vs deallocations

### Resultado

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

### Interpretación
- **Allocations > Deallocations constantemente** → Memory leak
- **Allocations ≈ Deallocations** → Memoria sana
- **Picos de allocations** → Momentos de alta carga (carga de lista, imágenes)

---

## Common memory issues en Flutter

### 1. Controllers sin dispose

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

### 2. Streams sin cancel

```dart
// ❌ Memory leak
class MyScreen extends StatefulWidget {
  @override
  State<MyScreen> createState() => _MyScreenState();
}

class _MyScreenState extends State<MyScreen> {
  @override
  void initState() {
    super.initState();
    Firestore.instance.collection('data').snapshots().listen((event) {
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
    _subscription = Firestore.instance.collection('data').snapshots().listen((event) {
      // Handle event
    });
  }

  @override
  void dispose() {
    _subscription?.cancel();  // ← Importante
    super.dispose();
  }
}
```

### 3. Imágenes sin cache eviction

```dart
// ❌ Acumula imágenes en memoria
ListView.builder(
  itemCount: 1000,
  itemBuilder: (context, i) {
    return Image.network('https://example.com/image_$i.jpg');
    // Cada imagen se mantiene en memoria
  },
)

// ✅ Con cache y límite
ListView.builder(
  itemCount: 1000,
  itemBuilder: (context, i) {
    return CachedNetworkImage(
      imageUrl: 'https://example.com/image_$i.jpg',
      cacheManager: CacheManager(
        Config(
          'uniqueCacheKey',
          stalePeriod: Duration(minutes: 10),
          maxNrOfCacheObjects: 100,  // ← Límite
        ),
      ),
    );
  },
)
```

---

## Ejercicios prácticos

### Ejercicio 1: Detectar memory leak

1. Crear pantalla con TextEditingController
2. Navegar a esa pantalla 10 veces
3. Tomar snapshot después de cada navegación
4. Verificar si las instancias de TextEditingController aumentan
5. Fix con dispose()

### Ejercicio 2: Memory diff de carga de datos

1. Tomar snapshot baseline
2. Cargar lista de 100 productos desde API
3. Tomar segundo snapshot
4. Analizar cuánta memoria consumen los productos
5. Evaluar si es aceptable

### Ejercicio 3: Trace de imágenes

1. Crear pantalla con 20 imágenes de red
2. Monitorear allocaciones de ImageStreamCompleter
3. Navegar fuera de la pantalla
4. Verificar si las imágenes se liberan
5. Implementar cache eviction

---
→ Siguiente: `06-network-view.md`
