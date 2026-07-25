# 12: Ejercicios Adicionales (+25 problemas)

> Ejercicios organizados por patrón y dificultad. Usa el framework de 6 pasos del [01-metodologia-general.md](./01-metodologia-general.md) para cada uno.

---

## Cómo usar este archivo

1. Elige un ejercicio por dificultad
2. Aplica los 6 pasos (lee → identifica → diseña → implementa → verifica → optimiza)
3. No mires la solución hasta haber intentado 15 minutos
4. Si te trabas 30 minutos, mira la pista, no la solución completa

---

## Nivel 1: Fácil (1-2 pasos)

### 1. Two Sum
**Dado un array y un target, encuentra dos números que sumen el target.**
Retorna sus índices.

```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
```

**Pista:** ¿Qué necesitas para encontrar complemento?

<details>
<summary>Solución</summary>

```dart
List<int> twoSum(List<int> nums, int target) {
  final map = <int, int>{};
  for (int i = 0; i < nums.length; i++) {
    final complemento = target - nums[i];
    if (map.containsKey(complemento)) {
      return [map[complemento]!, i];
    }
    map[nums[i]] = i;
  }
  return [];
}
```

**Complejidad:** O(n) tiempo, O(n) espacio
</details>

---

### 2. Valid Anagram
**Determina si dos strings son anagramas.**

```
Input: s = "anagram", t = "nagaram"
Output: true
```

**Pista:** ¿Qué pasa con las frecuencias de caracteres?

<details>
<summary>Solución</summary>

```dart
bool isAnagram(String s, String t) {
  if (s.length != t.length) return false;
  final count = <String, int>{};
  for (int i = 0; i < s.length; i++) {
    count[s[i]] = (count[s[i]] ?? 0) + 1;
    count[t[i]] = (count[t[i]] ?? 0) - 1;
  }
  return count.values.every((v) => v == 0);
}
```

**Complejidad:** O(n) tiempo, O(1) espacio (26 letras max)
</details>

---

### 3. Reverse String
**Invierte un array de caracteres in-place.**

```
Input: ['h','e','l','l','o']
Output: ['o','l','l','e','h']
```

<details>
<summary>Solución</summary>

```dart
void reverseString(List<String> s) {
  int left = 0, right = s.length - 1;
  while (left < right) {
    final temp = s[left];
    s[left] = s[right];
    s[right] = temp;
    left++;
    right--;
  }
}
```

**Complejidad:** O(n) tiempo, O(1) espacio
</details>

---

### 4. Merge Sorted Arrays
**Fusiona dos arrays ordenados en orden ascendente.**

```
Input: nums1 = [1,2,3], nums2 = [2,5,6]
Output: [1,2,2,3,5,6]
```

<details>
<summary>Solución</summary>

```dart
List<int> merge(List<int> nums1, List<int> nums2) {
  final result = <int>[];
  int i = 0, j = 0;
  while (i < nums1.length && j < nums2.length) {
    if (nums1[i] <= nums2[j]) {
      result.add(nums1[i++]);
    } else {
      result.add(nums2[j++]);
    }
  }
  while (i < nums1.length) result.add(nums1[i++]);
  while (j < nums2.length) result.add(nums2[j++]);
  return result;
}
```
</details>

---

### 5. Contains Duplicate
**Retorna true si algún elemento aparece dos veces.**

```
Input: [1,2,3,1]
Output: true
```

<details>
<summary>Solución</summary>

```dart
bool containsDuplicate(List<int> nums) {
  return nums.toSet().length != nums.length;
}
```
</details>

---

### 6. Max Subarray Sum
**Encuentra el subarray contiguo con mayor suma.**

```
Input: [-2,1,-3,4,-1,2,1,-5,4]
Output: 6 (subarray [4,-1,2,1])
```

**Pista:** Kadane's Algorithm

<details>
<summary>Solución</summary>

```dart
int maxSubArray(List<int> nums) {
  int maxActual = nums[0];
  int maxGlobal = nums[0];
  for (int i = 1; i < nums.length; i++) {
    maxActual = [nums[i], maxActual + nums[i]].reduce((a, b) => a > b ? a : b);
    if (maxActual > maxGlobal) maxGlobal = maxActual;
  }
  return maxGlobal;
}
```
</details>

---

## Nivel 2: Medio (2-3 pasos)

### 7. Group Anagrams
**Agrupa strings que son anagramas entre sí.**

```
Input: ["eat","tea","tan","ate","nat","bat"]
Output: [["eat","tea","ate"],["tan","nat"],["bat"]]
```

<details>
<summary>Solución</summary>

```dart
List<List<String>> groupAnagrams(List<String> strs) {
  final map = <String, List<String>>{};
  for (final s in strs) {
    final key = (s.split('')..sort()).join();
    map.putIfAbsent(key, () => []).add(s);
  }
  return map.values.toList();
}
```
</details>

---

### 8. Longest Consecutive Sequence
**Encuentra la secuencia consecutiva más larga.**

```
Input: [100,4,200,1,3,2]
Output: 4 (secuencia [1,2,3,4])
```

**Pista:** Solo empieza a contar si `num - 1` no existe.

<details>
<summary>Solución</summary>

```dart
int longestConsecutive(List<int> nums) {
  final set = nums.toSet();
  int maxLen = 0;
  for (final n in set) {
    if (!set.contains(n - 1)) { // Inicio de secuencia
      int current = n;
      int len = 1;
      while (set.contains(current + 1)) {
        current++;
        len++;
      }
      if (len > maxLen) maxLen = len;
    }
  }
  return maxLen;
}
```
</details>

---

### 9. Product of Array Except Self
**Retorna array donde cada elemento es el producto de todos excepto sí mismo.**

```
Input: [1,2,3,4]
Output: [24,12,8,6]
```

**Pista:** Producto izquierdo × Producto derecho.

<details>
<summary>Solución</summary>

```dart
List<int> productExceptSelf(List<int> nums) {
  final n = nums.length;
  final result = List.filled(n, 1);

  int left = 1;
  for (int i = 0; i < n; i++) {
    result[i] = left;
    left *= nums[i];
  }

  int right = 1;
  for (int i = n - 1; i >= 0; i--) {
    result[i] *= right;
    right *= nums[i];
  }

  return result;
}
```
</details>

---

### 10. Valid Parentheses
**Determina si los paréntesis son válidos.**

```
Input: "(()[]{})"
Output: true
```

<details>
<summary>Solución</summary>

```dart
bool isValid(String s) {
  final stack = <String>[];
  final pairs = {')': '(', ']': '[', '}': '{'};

  for (final c in s.split('')) {
    if ('([{'.contains(c)) {
      stack.add(c);
    } else {
      if (stack.isEmpty || stack.last != pairs[c]) return false;
      stack.removeLast();
    }
  }
  return stack.isEmpty;
}
```
</details>

---

### 11. Binary Search Rotated
**Busca un target en un array rotado ordenado.**

```
Input: nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

<details>
<summary>Solución</summary>

```dart
int search(List<int> nums, int target) {
  int left = 0, right = nums.length - 1;
  while (left <= right) {
    int mid = (left + right) ~/ 2;
    if (nums[mid] == target) return mid;

    if (nums[left] <= nums[mid]) {
      if (target >= nums[left] && target < nums[mid]) {
        right = mid - 1;
      } else {
        left = mid + 1;
      }
    } else {
      if (target > nums[mid] && target <= nums[right]) {
        left = mid + 1;
      } else {
        right = mid - 1;
      }
    }
  }
  return -1;
}
```
</details>

---

### 12. Climbing Stairs
**¿De cuántas formas puedes subir n escalones? (1 o 2 pasos a la vez)**

```
Input: n = 5
Output: 8
```

**Pista:** Es Fibonacci.

<details>
<summary>Solución</summary>

```dart
int climbStairs(int n) {
  if (n <= 2) return n;
  int a = 1, b = 2;
  for (int i = 3; i <= n; i++) {
    int temp = a + b;
    a = b;
    b = temp;
  }
  return b;
}
```
</details>

---

## Nivel 3: Difícil (3+ pasos)

### 13. Merge K Sorted Lists
**Fusiona k listas ordenadas en una sola lista ordenada.**

**Pista:** Usa un min-heap (pq de Dart: `PriorityQueue`).

<details>
<summary>Solución (idea)</summary>

```dart
// Usa PriorityQueue de package:collection
// Inserta primer nodo de cada lista
// Extrae el menor, agrega su siguiente
// Repite hasta vaciar todas
```
</details>

---

### 14. LRU Cache
**Implementa una cache con capacidad fija que elimina el menos recientemente usado.**

**Pista:** `LinkedHashMap` de Dart.

<details>
<summary>Solución</summary>

```dart
class LRUCache {
  final int capacity;
  final _cache = LinkedHashMap<int, int>();

  LRUCache(this.capacity);

  int get(int key) {
    if (!_cache.containsKey(key)) return -1;
    final value = _cache.remove(key)!;
    _cache[key] = value; // Mover al final
    return value;
  }

  void put(int key, int value) {
    if (_cache.containsKey(key)) _cache.remove(key);
    _cache[key] = value;
    if (_cache.length > capacity) {
      _cache.remove(_cache.keys.first); // Eliminar el primero (LRU)
    }
  }
}
```
</details>

---

### 15. Word Ladder
**Encuentra el camino más corto transformando una palabra en otra cambiando una letra a la vez.**

```
Input: begin = "hit", end = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
Output: 5 (hit → hot → dot → dog → cog)
```

**Pista:** BFS (Breadth-First Search).

---

### 16. Median of Two Sorted Arrays
**Encuentra la mediana de dos arrays ordenados en O(log(m+n)).**

**Pista:** Binary search en el array más corto.

---

### 17. Regular Expression Matching
**Implementa `.` (cualquier char) y `*` (cero o más del anterior).**

**Pista:** Recursión con memo.

---

## Ejercicios Dart Específicos

### 18. Implementa un Stack usando List
```dart
class Stack<T> {
  // Implementa push, pop, peek, isEmpty, size
}
```

### 19. Implementa un Queue usando List
```dart
class Queue<T> {
  // Implementa enqueue, dequeue, peek, isEmpty
}
```

### 20. Implementa un HashMap simple
```dart
class SimpleHashMap<K, V> {
  // Implementa put, get, remove, containsKey
  // Usa un array de buckets (linked lists para colisiones)
}
```

### 21. Binary Tree: DFS in-order, pre-order, post-order
```dart
class TreeNode<T> {
  T value;
  TreeNode<T>? left, right;
  TreeNode(this.value);
}

// Implementa los 3 recorridos DFS
```

### 22. Binary Tree: BFS (nivel por nivel)
```dart
// Retorna listas de valores por nivel
List<List<int>> levelOrder(TreeNode<int>? root) {
  // Tu código aquí
}
```

### 23. Graph: BFS desde un nodo
```dart
// Dado un grafo (adjacency list), retorna BFS
List<int> bfs(Map<int, List<int>> graph, int start) {
  // Tu código aquí
}
```

### 24. Graph: Detectar ciclo en directed graph
```dart
bool hasCycle(Map<int, List<int>> graph) {
  // Tu código aquí (DFS con estado: blanco, gris, negro)
}
```

### 25. Implementa Merge Sort
```dart
List<int> mergeSort(List<int> nums) {
  // Tu código aquí
}
```

### 26. Implementa Quick Sort
```dart
List<int> quickSort(List<int> nums) {
  // Tu código aquí
}
```

---

## Progresión sugerida

```
Semana 1: Ejercicios 1-6 (fácil, 30 min cada uno)
Semana 2: Ejercicios 7-12 (medio, 45 min cada uno)
Semana 3: Ejercicios 13-17 (difícil, 60 min cada uno)
Semana 4: Ejercicios 18-26 (Dart específico, 30 min cada uno)
```

**Total: ~26 ejercicios × 40 min promedio = ~17 horas**

---

**Volver al índice:** [README.md](./README.md)
