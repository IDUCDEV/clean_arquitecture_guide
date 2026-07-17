# 03 — Reconocimiento de Patrones

> El 80% de los problemas de algoritmos caen en ~15 patrones. Tu trabajo no es inventar un algoritmo desde cero, sino **reconocer** cuál patrón aplica.

---

## Framework de 3 pasos para reconocer el patrón

```
1. Identificar tipo de input
2. Detectar keywords del enunciado
3. Validar contra las constraints
```

---

## Paso 1: Tipo de Input → Patrones candidatos

| Tipo de Input | Patrones a considerar primero |
|---|---|
| **Array (ordenado)** | Two Pointers, Binary Search |
| **Array (desordenado)** | HashMap, Sorting + Two Pointers, Sliding Window |
| **String** | HashMap (frecuencias), Sliding Window, Trie |
| **Linked List** | Two Pointers (fast/slow), Reversal |
| **Tree** | DFS, BFS, Recursión |
| **Graph** | BFS, DFS, Topological Sort, Union-Find |
| **Matrix / Grid** | BFS + visited, DFS, DP |
| **Intervalos** | Sorting + Greedy, Merge logic |
| **Stream / Online** | Heap / Priority Queue |
| **Números / Bits** | Bit manipulation, Math, Binary Search |

---

## Paso 2: Keywords del Problema → Patrón

| Keyword / Frase en el enunciado | Patrón | Ejemplo de problema |
|---|---|---|
| "subarray/substring **contiguo**" | Sliding Window | Máximo subarray de tamaño K |
| "longest / shortest subarray con..." | Sliding Window | Longest Substring Without Repeating |
| "**par** / triplet que suma..." | Two Pointers o HashMap | Two Sum, 3Sum |
| "**sorted** array" | Binary Search o Two Pointers | Search in Rotated Array |
| "**minimum steps** / shortest path" (sin peso) | BFS | Castle on the Grid |
| "all **combinations** / permutations" | Backtracking | Subsets, Permutations |
| "**k-th** largest / smallest" | Heap / Priority Queue | Kth Largest Element |
| "**overlapping** subproblems + optimal" | Dynamic Programming | Climbing Stairs, Knapsack |
| "**ciclo** / cycle" | DFS + visited o Union-Find | Detect Cycle in Linked List |
| "**connected** / componentes" | DFS / BFS / Union-Find | Number of Islands |
| "**next greater** / smaller element" | Monotonic Stack | Daily Temperatures |
| "**dependency** / prerequisite" | Topological Sort | Course Schedule |
| "words starting with **prefix**" | Trie | Implement Trie |
| "**merge** intervals / overlapping" | Sorting + Intervals | Merge Intervals |
| "**optimal** / maximum / minimum" (sin subproblemas) | Greedy | Jump Game |
| "**frequency** / count duplicates" | HashMap | Group Anagrams |
| "**all** subsets / combinations con restricciones" | Backtracking | Combination Sum |

---

## Paso 3: Árbol de Decisión

Responde estas preguntas en orden para llegar al patrón:

```
¿El input es un array/string?
├── SÍ
│   ├── ¿Está ordenado?
│   │   ├── SÍ → Two Pointers o Binary Search
│   │   └── NO
│   │       ├── ¿Buscas algo contiguo? → Sliding Window
│   │       ├── ¿Buscas un par/suma? → HashMap
│   │       ├── ¿Puedes ordenarlo? → Sorting + Two Pointers
│   │       └── ¿Range sum queries? → Prefix Sum
│   └── ¿Es un stream infinito? → Heap
│
├── ¿El input es un tree?
│   ├── ¿Camino más corto? → BFS
│   ├── ¿Explorar todos los caminos? → DFS
│   └── ¿BST property? → Binary Search en tree
│
├── ¿El input es un graph?
│   ├── ¿Camino más corto (sin peso)? → BFS
│   ├── ¿Explorar/connectivity? → DFS
│   ├── ¿Orden de dependencias? → Topological Sort
│   ├── ¿Grupos dinámicos? → Union-Find
│   └── ¿Camino más corto (con peso)? → Dijkstra
│
├── ¿El input es un grid?
│   ├── ¿Camino más corto? → BFS + visited
│   ├── ¿Contar islas/componentes? → DFS + visited
│   └── ¿Camino con costo? → DP o Dijkstra
│
└── ¿El input son números?
    ├── ¿Buscar en rango? → Binary Search
    ├── ¿Optimización? → Binary Search sobre respuesta
    └── ¿Bits/subconjuntos? → Bit Manipulation
```

---

## Tabla Resumen: Los 12 Patrones Esenciales

| # | Patrón | Señal principal | Complejidad típica |
|---|---|---|---|
| 1 | **HashMap** | "Frequency", "duplicate", "pair with sum" | O(n) |
| 2 | **Two Pointers** | "Sorted", "pair", "triplet", "partition" | O(n) |
| 3 | **Sliding Window** | "Contiguous", "longest/shortest subarray" | O(n) |
| 4 | **Prefix Sum** | "Range sum", "subarray sum = k" | O(n) |
| 5 | **Binary Search** | "Sorted", "min X such that...", monotonic | O(log n) |
| 6 | **BFS** | "Minimum steps", "shortest path" (sin peso) | O(V + E) |
| 7 | **DFS** | "Connected", "all paths", "components" | O(V + E) |
| 8 | **Greedy** | "Optimal", "schedule", locally optimal = globally | O(n log n) |
| 9 | **DP** | "Overlapping subproblems", "optimal value" | Varies |
| 10 | **Backtracking** | "All combinations", "all permutations" | O(2ⁿ) |
| 11 | **Heap** | "K-th largest", "top K", "median" | O(n log k) |
| 12 | **Monotonic Stack** | "Next greater element", "histogram" | O(n) |

---

## Cómo Validar tu Elección

Una vez que crees haber identificado el patrón, verifica:

1. **¿La complejidad del patrón cabe en las constraints?** Si el patrón es O(n²) pero necesitas O(n), no es el correcto.
2. **¿El patrón cubre todos los edge cases?** Si hay negativos, Sliding Window no funciona (usa Prefix Sum).
3. **¿Hay un patrón más simple que funcione?** Si DP y Greedy ambos funcionan, usa Greedy (más simple).

---

## El Mantra

Antes de escribir código, di en voz alta:

> "Este es un problema de **[PATRÓN]** porque el input es **[TIPO]** y me piden **[QUÉ]**, con complejidad **[O(?)]**."

Si puedes completar esa frase, ya estás listo para implementar.
