# 05 — Patrones Avanzados con Templates en Dart

> 8 patrones esenciales con template listo para copiar y adaptar. Cada uno incluye: cuándo usar, template Dart, error común, y problema de referencia.

---

## 1. Sliding Window

**Cuándo usar:** Subarray/substring contiguo con una propiedad (longest, shortest, con k elementos).

**Template:**
```dart
// Tiempo: O(n) | Espacio: O(1) fijo, O(k) variable
// Sliding Window de tamaño variable
int slidingWindow(List<int> arr, int k) {
  int windowSum = 0;
  int maxSum = 0;

  for (int i = 0; i < arr.length; i++) {
    windowSum += arr[i];

    if (i >= k) {
      windowSum -= arr[i - k]; // shrink desde la izquierda
    }

    if (i >= k - 1) {
      maxSum = max(maxSum, windowSum);
    }
  }
  return maxSum;
}

// Sliding Window de tamaño variable (longest con condición)
int longestWithCondition(List<int> arr) {
  int left = 0;
  int maxLength = 0;
  // state de la ventana (sum, count, etc.)

  for (int right = 0; right < arr.length; right++) {
    // expandir: agregar arr[right] al state

    while (/* condición violada */) {
      // shrink: remover arr[left] del state
      left++;
    }

    maxLength = max(maxLength, right - left + 1);
  }
  return maxLength;
}
```

**Error común:** Usar Sliding Window cuando hay negativos (rompe la monotonicidad). Usa Prefix Sum en su lugar.

---

## 2. Two Pointers

**Cuándo usar:** Array ordenado, buscar pares/triplets, partition.

**Template:**
```dart
// Tiempo: O(n) | Espacio: O(1)
// Two pointers desde ambos extremos
List<int> twoSumSorted(List<int> arr, int target) {
  int left = 0;
  int right = arr.length - 1;

  while (left < right) {
    int sum = arr[left] + arr[right];

    if (sum == target) {
      return [left, right];
    } else if (sum < target) {
      left++; // necesitamos más
    } else {
      right--; // necesitamos menos
    }
  }
  return [];
}

// Two pointers para partition (荷兰国旗问题)
void partitionColors(List<int> arr) {
  int low = 0, mid = 0, high = arr.length - 1;

  while (mid <= high) {
    if (arr[mid] == 0) {
      swap(arr, low, mid);
      low++;
      mid++;
    } else if (arr[mid] == 1) {
      mid++;
    } else {
      swap(arr, mid, high);
      high--;
    }
  }
}
```

**Error común:** No ordenar el array primero cuando Two Pointers requiere orden.

---

## 3. BFS (Breadth-First Search)

**Cuándo usar:** Camino más corto en grafo sin peso, traversal por niveles, shortest path en grid.

**Template:**
```dart
// Tiempo: O(V + E) | Espacio: O(V)
// V = vértices/nodos, E = aristas/conexiones
import 'dart:collection';

int bfs(List<List<int>> graph, int start, int target) {
  Queue<List<int>> queue = Queue(); // [node, distance]
  Set<int> visited = {};

  queue.add([start, 0]);
  visited.add(start);

  while (queue.isNotEmpty) {
    var current = queue.removeFirst();
    int node = current[0];
    int dist = current[1];

    if (node == target) return dist;

    for (int neighbor in graph[node]) {
      if (!visited.contains(neighbor)) {
        visited.add(neighbor);
        queue.add([neighbor, dist + 1]);
      }
    }
  }
  return -1; // no hay camino
}

// BFS en grid (Castle on the Grid style)
int bfsGrid(List<String> grid, int startX, int startY, int goalX, int goalY) {
  int n = grid.length;
  Queue<List<int>> queue = Queue();
  Set<(int, int)> visited = {};

  queue.add([startX, startY, 0]);
  visited.add((startX, startY));

  List<(int, int)> directions = [(0, 1), (0, -1), (1, 0), (-1, 0)];

  while (queue.isNotEmpty) {
    var current = queue.removeFirst();
    int x = current[0], y = current[1], steps = current[2];

    if (x == goalX && y == goalY) return steps;

    for (var (dx, dy) in directions) {
      int nx = x + dx, ny = y + dy;
      while (nx >= 0 && nx < n && ny >= 0 && ny < n && grid[nx][ny] == '.') {
        if (!visited.contains((nx, ny))) {
          visited.add((nx, ny));
          queue.add([nx, ny, steps + 1]);
        }
        nx += dx;
        ny += dy;
      }
    }
  }
  return -1;
}
```

**Error común:** Olvidar marcar visitados antes de agregar a la cola (causa duplicados).

---

## 4. DFS (Depth-First Search)

**Cuándo usar:** Explorar todos los caminos, contar componentes, detección de ciclos.

**Template:**
```dart
// Tiempo: O(V + E) | Espacio: O(V)
// DFS recursivo en graph
void dfs(List<List<int>> graph, int node, Set<int> visited) {
  visited.add(node);
  for (int neighbor in graph[node]) {
    if (!visited.contains(neighbor)) {
      dfs(graph, neighbor, visited);
    }
  }
}

// DFS en grid (contar islas)
int countIslands(List<List<int>> grid) {
  int count = 0;
  int rows = grid.length, cols = grid[0].length;

  for (int i = 0; i < rows; i++) {
    for (int j = 0; j < cols; j++) {
      if (grid[i][j] == 1) {
        dfsGrid(grid, i, j, rows, cols);
        count++;
      }
    }
  }
  return count;
}

void dfsGrid(List<List<int>> grid, int r, int c, int rows, int cols) {
  if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] == 0) return;

  grid[r][c] = 0; // marcar visitado
  dfsGrid(grid, r + 1, c, rows, cols);
  dfsGrid(grid, r - 1, c, rows, cols);
  dfsGrid(grid, r, c + 1, rows, cols);
  dfsGrid(grid, r, c - 1, rows, cols);
}
```

**Error común:** No backtrack (deshacer el cambio de estado) en problemas que lo requieren.

---

## 5. Binary Search

**Cuándo usar:** Array ordenado, buscar en espacio de respuesta monotónico.

**Template:**
```dart
// Tiempo: O(log n) | Espacio: O(1)
// Binary Search clásico
int binarySearch(List<int> arr, int target) {
  int left = 0, right = arr.length - 1;

  while (left <= right) {
    int mid = left + (right - left) ~/ 2;

    if (arr[mid] == target) {
      return mid;
    } else if (arr[mid] < target) {
      left = mid + 1;
    } else {
      right = mid - 1;
    }
  }
  return -1;
}

// Binary Search sobre respuesta
// "¿Es posible hacer X con calidad Y?"
bool isPossible(List<int> arr, int quality) {
  // retorna true si es factible con la calidad dada
  // ...
}

int searchAnswer(List<int> arr) {
  int left = 0, right = maxPossibleValue;

  while (left < right) {
    int mid = left + (right - left) ~/ 2;

    if (isPossible(arr, mid)) {
      right = mid; // buscar mejor
    } else {
      left = mid + 1;
    }
  }
  return left;
}
```

**Error común:** Off-by-one errors. Clarifica si `left < right` o `left <= right`.

---

## 6. Greedy

**Cuándo usar:** Elección local óptima lleva a óptimo global. Sin subproblemas superpuestos.

**Template:**
```dart
// Tiempo: O(n log n) por sorting | Espacio: O(1)
// Greedy con sorting
int greedySchedule(List<(int start, int end)> intervals) {
  intervals.sortBy((a, b) => a.$2.compareTo(b.$2)); // sort by end time

  int count = 0;
  int lastEnd = -1;

  for (var interval in intervals) {
    if (interval.$1 >= lastEnd) {
      count++;
      lastEnd = interval.$2;
    }
  }
  return count;
}

// Greedy con acumulador (Truck Tour style)
int findStart(List<(int petrol, int distance)> pumps) {
  int tank = 0;
  int start = 0;

  for (int i = 0; i < pumps.length; i++) {
    tank += pumps[i].$1 - pumps[i].$2;

    if (tank < 0) {
      start = i + 1;
      tank = 0;
    }
  }
  return start;
}
```

**Error común:** Asumir que greedy siempre funciona. Greedy requiere **probar** que la elección local es óptima (usualmente por contradiction o inducción).

---

## 7. Dynamic Programming (DP)

**Cuándo usar:** Subproblemas superpuestos + estructura de optimalidad.

**Template:**
```dart
// Tiempo: O(n) a O(n*m) según subproblemas | Espacio: O(n) a O(n*m)
// DP bottom-up (tabulation)
int climbStairs(int n) {
  if (n <= 2) return n;

  List<int> dp = List.filled(n + 1, 0);
  dp[1] = 1;
  dp[2] = 2;

  for (int i = 3; i <= n; i++) {
    dp[i] = dp[i - 1] + dp[i - 2];
  }
  return dp[n];
}

// DP con memoization (top-down)
Map<String, int> memo = {};

int dpTopDown(int n) {
  if (n <= 2) return n;
  String key = '$n';
  if (memo.containsKey(key)) return memo[key]!;

  memo[key] = dpTopDown(n - 1) + dpTopDown(n - 2);
  return memo[key]!;
}

// DP 2D (Knapsack)
int knapsack(List<int> weights, List<int> values, int capacity) {
  int n = weights.length;
  List<List<int>> dp = List.generate(
    n + 1,
    (i) => List.filled(capacity + 1, 0),
  );

  for (int i = 1; i <= n; i++) {
    for (int w = 0; w <= capacity; w++) {
      dp[i][w] = dp[i - 1][w]; // no tomar
      if (weights[i - 1] <= w) {
        dp[i][w] = max(
          dp[i][w],
          dp[i - 1][w - weights[i - 1]] + values[i - 1],
        );
      }
    }
  }
  return dp[n][capacity];
}
```

**Error común:** No definir bien la recurrence relation. Pregúntate: "¿Cuál es la subpregunta más pequeña?"

---

## 8. Backtracking

**Cuándo usar:** Generar todas las combinaciones/permutaciones bajo restricciones. n pequeño (≤ 20).

**Template:**
```dart
// Tiempo: O(2^n) o O(n!) | Espacio: O(n)
// Backtracking base
void backtrack(List<int> candidates, List<int> current, int start) {
  // procesar current (es solución válida)
  print(current);

  for (int i = start; i < candidates.length; i++) {
    // pruning: skip si no puede llevar a solución
    if (i > start && candidates[i] == candidates[i - 1]) continue;

    current.add(candidates[i]);
    backtrack(candidates, current, i + 1);
    current.removeLast(); // backtrack
  }
}

// Permutaciones
void permute(List<int> nums) {
  List<bool> used = List.filled(nums.length, false);
  List<int> current = [];

  void backtrack() {
    if (current.length == nums.length) {
      print(List.from(current));
      return;
    }

    for (int i = 0; i < nums.length; i++) {
      if (used[i]) continue;

      used[i] = true;
      current.add(nums[i]);
      backtrack();
      current.removeLast();
      used[i] = false;
    }
  }

  backtrack();
}
```

**Error común:** No hacer backtrack (olvidar `removeLast` o `used[i] = false`).

---

> Para el árbol de decisión completo de patrones, ver [03-reconocimiento-patrones.md](./03-reconocimiento-patrones.md).
