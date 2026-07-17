# 04 — Estructuras de Datos: Referencia Rápida

> Qué estructura usar para qué situación, con sus complejidades de operación en Dart.

---

## Mapa Rápido

| Necesito... | Usa... | Complejidad |
|---|---|---|
| Acceso rápido por índice | `List` (array) | O(1) acceso, O(n) búsqueda |
| Buscar si un valor existe | `Set` | O(1) contains |
| Buscar con frecuencia/pares | `Map<K,V>` | O(1) lookup |
| Procesar en orden FIFO | `Queue` | O(1) add/remove |
| Obtener min/max repetidamente | `PriorityQueue` (Heap) | O(log n) |
| Buscar en datos ordenados | Binary Search en `List` | O(log n) |
| Conexiones dinámicas | Union-Find (implementación propia) | O(α(n)) ≈ O(1) |
| Prefix matching (strings) | Trie (implementación propia) | O(L) |

---

## Detalle por Estructura

### List (Array)

**Cuándo usar:** Acceso por índice, iteración secuencial, dos pointers, sliding window.

```dart
// Acceso y actualización
arr[i];              // O(1)
arr.add(x);          // O(1) amortizado
arr.removeAt(i);     // O(n) — desplaza elementos
arr.sublist(i, j);   // O(j-i)

// Búsqueda
arr.contains(x);     // O(n)
arr.indexOf(x);      // O(n)
arr.sort();          // O(n log n)
```

**Limitación:** Inserción/eliminación en medio es O(n).

---

### Set

**Cuándo usar:** Verificar existencia, eliminar duplicados, operaciones de conjuntos (unión, intersección).

```dart
set.contains(x);     // O(1)
set.add(x);          // O(1)
set.remove(x);       // O(1)
set.union(other);    // O(n)
set.intersection(other); // O(min(n,m))
```

**Implementación interna:** Hash table en Dart.

---

### Map (HashMap)

**Cuándo usar:** Frecuencias, pares que suman un valor, caching, agrupación.

```dart
map.containsKey(x);   // O(1)
map[x];               // O(1)
map[x] = value;       // O(1)
map.remove(x);        // O(1)
map.putIfAbsent(x, () => value); // O(1)
map.update(x, (v) => v + 1);     // O(1)
```

**Patrón clásico — Frecuencias:**
```dart
Map<String, int> freq = {};
for (var item in list) {
  freq[item] = (freq[item] ?? 0) + 1;
}
```

---

### Queue (Cola)

**Cuándo usar:** BFS, procesamiento en orden FIFO, sliding window con deque.

```dart
import 'dart:collection';

Queue<int> q = Queue();
q.addLast(x);     // O(1)
q.removeFirst();  // O(1)
q.first;          // O(1)
q.isEmpty;        // O(1)
```

---

### PriorityQueue (Heap)

**Cuándo usar:** K-th largest/smallest, merge de K sorted lists, encontrar el elemento más frecuente.

```dart
import 'package:collection/collection.dart';

// Min-heap por defecto
var heap = PriorityQueue<int>();
heap.add(x);       // O(log n)
heap.removeFirst(); // O(log n) — extrae el mínimo
heap.first;        // O(1)

// Max-heap
var maxHeap = PriorityQueue<int>((a, b) => b.compareTo(a));
```

**Patrón Top-K:**
```dart
// K elementos más grandes — usar min-heap de tamaño K
var minHeap = PriorityQueue<int>();
for (var x in list) {
  minHeap.add(x);
  if (minHeap.length > k) {
    minHeap.removeFirst(); // elimina el más pequeño
  }
}
// minHeap contiene los K más grandes
```

---

## Complejidades de Sorting en Dart

| Algoritmo | Tiempo | Espacio | Estable | Cuándo |
|---|---|---|---|---|
| `list.sort()` (Tim Sort) | O(n log n) | O(n) | Sí | Default de Dart |
| Quick Sort (manual) | O(n log n) promedio | O(log n) | No | Cuando se necesita in-place |
| Counting Sort | O(n + k) | O(k) | Sí | Enteros con rango pequeño |

---

## Decisiones de Estructura según el Problema

| Problema | Estructura óptima | Por qué |
|---|---|---|
| Two Sum | `Map<int, int>` | Lookup de complemento en O(1) |
| Sliding Window Máximo | `Deque` (Queue doble) | Mantener monothonic, O(1) por operación |
| K-th Largest | `PriorityQueue` (min-heap de tamaño k) | O(n log k) vs O(n log n) de sorting |
| Detectar ciclo | Two Pointers (fast/slow) | O(1) espacio, no necesita visited |
| Union-Find | Implementación propia con path compression | O(α(n)) ≈ O(1) amortizado |
| Prefix Sum | `List<int>` precomputada | O(1) por query después de O(n) precompute |
| Subarray Sum = k | `Map<int, int>` + prefix sum | O(n) con un solo pass |

---

## Relación con el Módulo 09

El módulo 09 (Estructuras de Datos con OOP) enseña **cómo implementar y usar** estas estructuras en Dart con ejemplos detallados. Esta sección es una **referencia rápida** para elegir la correcta durante la resolución de problemas.
