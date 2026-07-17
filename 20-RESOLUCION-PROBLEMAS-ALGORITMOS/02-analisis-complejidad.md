# 02 — Análisis de Complejidad Temporal y Espacial

> La complejidad es el filtro más importante para elegir un algoritmo. Si no sabes qué complejidad necesitas, no sabes qué algoritmo buscar.

---

## ¿Qué es Big-O?

Big-O describe **cómo crece** el tiempo de ejecución (o el espacio) a medida que crece el input. No nos importa el tiempo exacto en segundos, sino la **tasa de crecimiento**.

---

## Tabla de Complejidades Comunes

| Complejidad | Nombre | Ejemplo de algoritmo | n = 10⁵ tarda... |
|---|---|---|---|
| O(1) | Constante | Acceso por índice en array | instantáneo |
| O(log n) | Logarítmica | Binary search | instantáneo |
| O(n) | Lineal | Recorrer un array | ~0.001s |
| O(n log n) | Lineal-logarítmica | Merge sort, quicksort | ~0.01s |
| O(n²) | Cuadrática | Dos loops anidados | ~10s |
| O(n³) | Cúbica | Floyd-Warshall | ~1000s |
| O(2ⁿ) | Exponencial | Subconjuntos de un conjunto |∞ |
| O(n!) | Factorial | Permutaciones | ∞ |

---

## Regla Práctica: ¿Qué complejidad necesito?

Un ordenador ejecuta aproximadamente **10⁸ operaciones por segundo**. Con un time limit típico de 1-2 segundos:

| Tamaño del input (n) | Complejidad máxima aceptable | Ejemplo |
|---|---|---|
| `n ≤ 10` | O(n!) | Backtracking completo |
| `n ≤ 20` | O(2ⁿ · n) | Bitmask DP |
| `n ≤ 50` | O(n⁴) | DP cuártico |
| `n ≤ 400` | O(n³) | Floyd-Warshall |
| `n ≤ 5.000` | O(n²) | DP cuadrático |
| `n ≤ 10⁵` | O(n log n) | Sorting, binary search |
| `n ≤ 10⁶` | O(n) | Lineal puro |
| `n ≤ 10⁸` | O(log n) | Binary search sobre respuesta |
| `n ≤ 10¹⁸` | O(1) | Fórmula matemática |

**Nota:** Si las constraints son `n ≤ 10⁵`, O(n²) dará TLE (Time Limit Exceeded) porque 10¹⁰ operaciones > 10⁸ por segundo.

---

## Cómo Calcular la Complejidad

### Reglas básicas

```
1. Instrucciones simples = O(1)
   x = 5;
   print(x);

2. Un loop simple = O(n)
   for (int i = 0; i < n; i++) { ... }

3. Dos loops anidados = O(n²)
   for (int i = 0; i < n; i++)
     for (int j = 0; j < n; j++) { ... }

4. Loop que divide a la mitad = O(log n)
   while (n > 1) { n = n ~/ 2; }

5. Loop con inner loop que crece = O(n²)
   for (int i = 0; i < n; i++)
     for (int j = i; j < n; j++) { ... }

6. Combinaciones = multiplicar
   for (i) for (j) for (k) → O(n³)

7. Secuencias = tomar el máximo
   operación A: O(n)
   operación B: O(n²)
   Total = O(n²)
```

### Ejemplo práctico

```dart
// O(n) — cada elemento se visita una vez
int sum(List<int> arr) {
  int total = 0;
  for (int x in arr) {
    total += x;
  }
  return total;
}

// O(n²) — para cada elemento, recorremos todo el array
bool hasDuplicate(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {
    for (int j = i + 1; j < arr.length; j++) {
      if (arr[i] == arr[j]) return true;
    }
  }
  return false;
}

// O(n log n) — sorting
void sortArray(List<int> arr) {
  arr.sort(); // merge sort / tim sort interno
}

// O(n) — HashMap, cada lookup es O(1)
bool hasDuplicateHashMap(List<int> arr) {
  Set<int> seen = {};
  for (int x in arr) {
    if (seen.contains(x)) return true;
    seen.add(x);
  }
  return false;
}
```

---

## Complejidad Espacial

No solo importa el tiempo. El espacio también cuenta.

| Estructura | Espacio | Cuándo importa |
|---|---|---|
| Array de tamaño n | O(n) | Siempre es O(n) para el input |
| HashMap con n elementos | O(n) | Cuando el input es grande |
| Recursión profunda | O(n) stack | Puede causar stack overflow |
| Variable auxiliar | O(1) | El óptimo en espacio |

### Ejemplo: espacio en recursión

```dart
// O(n) espacio por el call stack
int factorial(int n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}

// O(1) espacio — iterativo
int factorialIterativo(int n) {
  int result = 1;
  for (int i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}
```

---

## El Tradeoff Tiempo-Espacio

Muchas veces puedes intercambiar tiempo por espacio:

| Enfoque | Tiempo | Espacio |
|---|---|---|
| Brute force (re-calcular todo) | O(n²) | O(1) |
| Pre-computar con HashMap | O(n) | O(n) |
| Pre-computar con Prefix Sum | O(n) | O(n) |

**Regla general:** Si las constraints de memoria son amplias (típico en interviews), prioriza tiempo. Si el input es enorme, considera optimizar espacio.

---

## Checklist antes de codificar

```
□ ¿Cuál es el tamaño máximo de n?
□ ¿Qué complejidad necesito según la tabla?
□ ¿Mi enfoque cumple esa complejidad?
□ ¿Cuánto espacio extra uso?
□ ¿Hay un tradeoff tiempo/espacio que valga la pena?
```
