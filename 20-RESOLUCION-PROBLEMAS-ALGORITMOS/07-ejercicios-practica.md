# 07 — Ejercicios de Práctica

> 10 ejercicios progresivos (3 easy, 4 medium, 3 hard) organizados por patrón. Cada uno incluye: enunciado, pistas, y solución en Dart.

---

## Easy (3 ejercicios)

### Ejercicio 1: Two Sum
**Patrón:** HashMap | **Plataforma:** LeetCode #1

**Enunciado:** Dado un array de enteros `nums` y un entero `target`, retorna los índices de dos números que sumen `target`.

**Pistas:**
- ¿Qué necesitas buscar para cada elemento? El complemento.
- ¿Cuál es la complejidad de buscar en un HashMap? O(1).
- ¿Puedes resolverlo en un solo pass?

**Solución en Dart:**
```dart
List<int> twoSum(List<int> nums, int target) {
  Map<int, int> seen = {};

  for (int i = 0; i < nums.length; i++) {
    int complement = target - nums[i];
    if (seen.containsKey(complement)) {
      return [seen[complement]!, i];
    }
    seen[nums[i]] = i;
  }

  return [];
}
// Tiempo: O(n) | Espacio: O(n)
```

---

### Ejercicio 2: Valid Anagram
**Patrón:** HashMap (frecuencias) | **Plataforma:** LeetCode #242

**Enunciado:** Dados dos strings `s` y `t`, retorna `true` si `t` es un anagrama de `s`.

**Pistas:**
- Si tienen diferente longitud, no pueden ser anagramas.
- Cuenta frecuencias de cada carácter en ambos strings.
- ¿Las frecuencias deben ser iguales?

**Solución en Dart:**
```dart
bool isAnagram(String s, String t) {
  if (s.length != t.length) return false;

  Map<String, int> freq = {};

  for (var ch in s.split('')) {
    freq[ch] = (freq[ch] ?? 0) + 1;
  }

  for (var ch in t.split('')) {
    freq[ch] = (freq[ch] ?? 0) - 1;
    if (freq[ch]! < 0) return false;
  }

  return true;
}
// Tiempo: O(n) | Espacio: O(1) — máximo 26 caracteres
```

---

### Ejercicio 3: Maximum Subarray (Kadane's Algorithm)
**Patrón:** DP lineal | **Plataforma:** LeetCode #53 | **Plantilla:** Ver [DP en 05-patrones-avanzados.md](./05-patrones-avanzados.md#7-dynamic-programming-dp)

**Enunciado:** Dado un array de enteros, encuentra el subarray contiguo con la mayor suma.

**Pistas:**
- Para cada posición, ¿el subarray máximo que termina aquí incluye o no el elemento anterior?
- Si el acumulado anterior es negativo, empieza de nuevo.
- Mantén un `currentMax` y un `globalMax`.

**Solución en Dart:**
```dart
int maxSubArray(List<int> nums) {
  int currentMax = nums[0];
  int globalMax = nums[0];

  for (int i = 1; i < nums.length; i++) {
    currentMax = max(nums[i], currentMax + nums[i]);
    globalMax = max(globalMax, currentMax);
  }

  return globalMax;
}
// Tiempo: O(n) | Espacio: O(1)
```

---

## Medium (4 ejercicios)

### Ejercicio 4: Best Time to Buy and Sell Stock
**Patrón:** One-pass, tracking mínimo | **Plataforma:** LeetCode #121

**Enunciado:** Dado un array `prices` donde `prices[i]` es el precio de una acción en el día `i`, encuentra la máxima ganancia que puedes lograr comprando y vendiendo una vez.

**Pistas:**
- Mantén el precio mínimo visto hasta ahora.
- Para cada día, calcula la ganancia si vendieras hoy.
- Actualiza la ganancia máxima.

**Solución en Dart:**
```dart
int maxProfit(List<int> prices) {
  int minPrice = prices[0];
  int maxProfit = 0;

  for (int i = 1; i < prices.length; i++) {
    if (prices[i] < minPrice) {
      minPrice = prices[i];
    } else {
      maxProfit = max(maxProfit, prices[i] - minPrice);
    }
  }

  return maxProfit;
}
// Tiempo: O(n) | Espacio: O(1)
```

---

### Ejercicio 5: Number of Islands
**Patrón:** DFS/BFS en grid | **Plataforma:** LeetCode #200 | **Plantilla:** Ver [DFS en 05-patrones-avanzados.md](./05-patrones-avanzados.md#4-dfs-depth-first-search)

**Enunciado:** Dado un grid de `'1'` (tierra) y `'0'` (agua), cuenta el número de islas. Una isla es formada por `'1'`s conectados horizontal o verticalmente.

**Pistas:**
- Recorre el grid. Cada `'1'` no visitado inicia una nueva isla.
- Usa DFS o BFS para "hundir" toda la isla (marcar como visitada).
- Incrementa el contador cada vez que encuentras un `'1'` nuevo.

**Solución en Dart:**
```dart
int numIslands(List<List<String>> grid) {
  int count = 0;
  int rows = grid.length, cols = grid[0].length;

  for (int r = 0; r < rows; r++) {
    for (int c = 0; c < cols; c++) {
      if (grid[r][c] == '1') {
        dfs(grid, r, c, rows, cols);
        count++;
      }
    }
  }
  return count;
}

void dfs(List<List<String>> grid, int r, int c, int rows, int cols) {
  if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1') return;

  grid[r][c] = '0'; // marcar visitado
  dfs(grid, r + 1, c, rows, cols);
  dfs(grid, r - 1, c, rows, cols);
  dfs(grid, r, c + 1, rows, cols);
  dfs(grid, r, c - 1, rows, cols);
}
// Tiempo: O(rows × cols) | Espacio: O(rows × cols) peor caso recursion
```

---

### Ejercicio 6: Coin Change
**Patrón:** Dynamic Programming | **Plataforma:** LeetCode #322 | **Plantilla:** Ver [DP en 05-patrones-avanzados.md](./05-patrones-avanzados.md#7-dynamic-programming-dp)

**Enunciado:** Dado un array de denominaciones de monedas `coins` y un `amount`, retorna el número mínimo de monedas para llegar a ese monto. Si no es posible, retorna -1.

**Pistas:**
- `dp[i]` = mínimo monedas para hacer el monto `i`.
- Para cada monto, prueba todas las monedas: `dp[i] = min(dp[i], dp[i - coin] + 1)`.
- Base: `dp[0] = 0` (0 monedas para monto 0).

**Solución en Dart:**
```dart
int coinChange(List<int> coins, int amount) {
  List<int> dp = List.filled(amount + 1, amount + 1);
  dp[0] = 0;

  for (int i = 1; i <= amount; i++) {
    for (int coin in coins) {
      if (coin <= i && dp[i - coin] + 1 < dp[i]) {
        dp[i] = dp[i - coin] + 1;
      }
    }
  }

  return dp[amount] > amount ? -1 : dp[amount];
}
// Tiempo: O(amount × coins.length) | Espacio: O(amount)
```

---

### Ejercicio 7: LRU Cache
**Patrón:** HashMap + Doubly Linked List | **Plataforma:** LeetCode #146

**Enunciado:** Implementa una estructura de datos LRU (Least Recently Used) Cache con `get(key)` y `put(key, value)` en O(1).

**Pistas:**
- Usa un HashMap para acceso O(1) por key.
- Usa una doubly linked list para mantener el orden de uso.
- El más reciente va al final; el más viejo va al frente.
- Al hacer `get`, mueve el nodo al final. Al `put` con capacidad llena, elimina el frente.

**Solución en Dart (esqueleto con LinkedHashMap):**
```dart
class LRUCache {
  final int capacity;
  final LinkedHashMap<int, int> _cache;

  LRUCache(this.capacity)
      : _cache = LinkedHashMap();

  int get(int key) {
    if (!_cache.containsKey(key)) return -1;
    _refresh(key);
    return _cache[key]!;
  }

  void put(int key, int value) {
    if (_cache.containsKey(key)) {
      _cache.remove(key);
    } else if (_cache.length >= capacity) {
      _cache.remove(_cache.keys.first);
    }
    _cache[key] = value;
  }

  void _refresh(int key) {
    int value = _cache.remove(key)!;
    _cache[key] = value;
  }
}
// Tiempo: O(1) get y put | Espacio: O(capacity)
```

---

## Hard (3 ejercicios)

### Ejercicio 8: Merge K Sorted Lists
**Patrón:** Heap (PriorityQueue) | **Plataforma:** LeetCode #23

**Enunciado:** Dadas `k` linked lists ordenadas, merge todas en una sola linked list ordenada.

**Pistas:**
- Usa un min-heap con un elemento de cada lista.
- Extrae el mínimo, agrega al resultado, y agrega el siguiente de esa lista al heap.
- Complejidad: O(N log k) donde N es el total de elementos.

**Solución en Dart (esqueleto):**
```dart
ListNode? mergeKLists(List<ListNode?> lists) {
  var heap = PriorityQueue<ListNode>((a, b) => a.val.compareTo(b.val));

  for (var node in lists) {
    if (node != null) heap.add(node);
  }

  ListNode dummy = ListNode(0);
  ListNode current = dummy;

  while (heap.isNotEmpty) {
    ListNode node = heap.removeFirst();
    current.next = node;
    current = node;
    if (node.next != null) heap.add(node.next!);
  }

  return dummy.next;
}
// Tiempo: O(N log k) | Espacio: O(k)
```

---

### Ejercicio 9: Alien Dictionary
**Patrón:** Topological Sort | **Plataforma:** LeetCode #269 | **Plantilla:** Ver [BFS en 05-patrones-avanzados.md](./05-patrones-avanzados.md#3-bfs-breadth-first-search)

**Enunciado:** Dado un array de palabras de un diccionario alienígena ordenado, determina el orden de los caracteres.

**Pistas:**
- Compara palabras adyacentes para encontrar precedencias (carácter A viene antes que B).
- Construye un grafo dirigido donde A→B significa "A va antes que B".
- Aplica topological sort (Kahn's algorithm con BFS).

**Solución en Dart (esqueleto):**
```dart
String alienOrder(List<String> words) {
  Map<String, Set<String>> adj = {};
  Map<String, int> inDegree = {};

  // Inicializar todos los caracteres
  for (var word in words) {
    for (var ch in word.split('')) {
      adj.putIfAbsent(ch, () => {});
      inDegree.putIfAbsent(ch, () => 0);
    }
  }

  // Construir grafo
  for (int i = 0; i < words.length - 1; i++) {
    String w1 = words[i], w2 = words[i + 1];
    int minLen = min(w1.length, w2.length);

    for (int j = 0; j < minLen; j++) {
      if (w1[j] != w2[j]) {
        String from = w1[j], to = w2[j];
        if (!adj[from]!.contains(to)) {
          adj[from]!.add(to);
          inDegree[to] = inDegree[to]! + 1;
        }
        break;
      }
    }
  }

  // Kahn's BFS
  Queue<String> queue = Queue();
  for (var entry in inDegree.entries) {
    if (entry.value == 0) queue.add(entry.key);
  }

  String result = '';
  while (queue.isNotEmpty) {
    String ch = queue.removeFirst();
    result += ch;
    for (var next in adj[ch]!) {
      inDegree[next] = inDegree[next]! - 1;
      if (inDegree[next] == 0) queue.add(next);
    }
  }

  return result.length == inDegree.length ? result : '';
}
// Tiempo: O(C) donde C es la longitud total de caracteres | Espacio: O(1) — máximo 26 letras
```

---

### Ejercicio 10: Word Ladder
**Patrón:** BFS | **Plataforma:** LeetCode #127 | **Plantilla:** Ver [BFS en 05-patrones-avanzados.md](./05-patrones-avanzados.md#3-bfs-breadth-first-search)

**Enunciado:** Dado `beginWord`, `endWord` y un diccionario `wordList`, encuentra la longitud más corta de `beginWord` a `endWord` cambiando una letra a la vez. Cada palabra intermedia debe estar en el diccionario.

**Pistas:**
- Cada palabra es un nodo; dos palabras están conectadas si difieren en una letra.
- BFS desde `beginWord` hasta `endWord`.
- Para eficiencia, pre-computa un "patrón" para cada palabra (h * (wordLen)).

**Solución en Dart (esqueleto):**
```dart
int ladderLength(String beginWord, String endWord, List<String> wordList) {
  Set<String> wordSet = Set.from(wordList);
  if (!wordSet.contains(endWord)) return 0;

  Queue<(String, int)> queue = Queue(); // (word, steps)
  Set<String> visited = {};

  queue.add((beginWord, 1));
  visited.add(beginWord);

  while (queue.isNotEmpty) {
    var (word, steps) = queue.removeFirst();

    for (int i = 0; i < word.length; i++) {
      for (var ch in 'abcdefghijklmnopqrstuvwxyz'.split('')) {
        if (ch == word[i]) continue;

        String next = word.substring(0, i) + ch + word.substring(i + 1);

        if (next == endWord) return steps + 1;

        if (wordSet.contains(next) && !visited.contains(next)) {
          visited.add(next);
          queue.add((next, steps + 1));
        }
      }
    }
  }

  return 0;
}
// Tiempo: O(M² × N) donde M = longitud de palabra, N = número de palabras
```

---

## Progresión sugerida

```
Semana 1: Ejercicios 1-3 (Easy) → 15-20 min cada uno
Semana 2: Ejercicios 4-5 (Medium) → 30-45 min cada uno
Semana 3: Ejercicios 6-7 (Medium) → 45-60 min cada uno
Semana 4: Ejercicios 8-10 (Hard) → 60-90 min cada uno
```

**Regla de los 20 minutos:** Si llevas 20 minutos sin avance, mira una pista (no la solución completa). Intenta otros 20 minutos. Si aún no, revisa la solución y vuelve a intentarla mañana.
