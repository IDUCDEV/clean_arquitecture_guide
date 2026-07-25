# 09: Recursión y Backtracking

> Recursión es cuando una función se llama a sí misma. Backtracking es recursión con "deshacer". Juntos resuelven problemas que parecen imposibles.

---

## Por qué importa

Muchos problemas de algoritmos **solo se resuelven** con recursión o backtracking:
- Permutaciones, combinaciones, subconjuntos
- Laberintos y juegos (N-Queens, Sudoku)
- Árboles (casi todo en árboles es recursión)

---

## Recursión: Los 3 pasos

### 1. Caso base
¿Cuándo para? Sin esto, llamada infinita.

### 2. Caso recursivo
¿Cómo reduces el problema?

### 3. ¿Qué cambia en cada llamada?
Algo debe acercarse al caso base.

```
factorial(5)
= 5 * factorial(4)
= 5 * 4 * factorial(3)
= 5 * 4 * 3 * factorial(2)
= 5 * 4 * 3 * 2 * factorial(1)
= 5 * 4 * 3 * 2 * 1  ← caso base
= 120
```

---

## Template recursión

```dart
int resolver(tipo input) {
  // 1. Caso base
  if (input es casoBase) return resultadoBase;

  // 2. Caso recursivo (reducir input)
  return operacion(input, resolver(inputReducido));
}
```

---

## Ejemplo: Fibonacci

```dart
// ❌ Sin recursión: iterativo
int fibonacci(int n) {
  if (n <= 1) return n;
  int a = 0, b = 1;
  for (int i = 2; i <= n; i++) {
    int temp = a + b;
    a = b;
    b = temp;
  }
  return b;
}

// ✅ Recursivo (simple pero lento O(2^n))
int fibRecursivo(int n) {
  if (n <= 1) return n;
  return fibRecursivo(n - 1) + fibRecursivo(n - 2);
}

// ✅ Recursivo + memo (rápido O(n))
int fibMemo(int n, [Map<int, int> memo = const {}]) {
  if (n <= 1) return n;
  if (memo.containsKey(n)) return memo[n]!;
  final resultado = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  memo[n] = resultado;
  return resultado;
}
```

---

## Backtracking: Recursión + "Deshacer"

Backtracking = probar algo, y si no funciona, **revertir** el cambio y probar otra cosa.

```
Explorar laberinto:
1. Mover a casilla → marcada como visitada
2. Si no hay salida → DESMARCAR (deshacer)
3. Probar otra dirección
```

---

## Template Backtracking

```dart
void backtracking(estado, candidatos) {
  // 1. ¿Es solución?
  if (esSolucion(estado)) {
    agregarSolucion(estado);
    return;
  }

  // 2. Probar cada candidato
  for (candidato in candidatos) {
    if (!esValido(candidato, estado)) continue;

    hacerMovimiento(candidato, estado);    // 3. Avanzar
    backtracking(estado, candidatos);       // 4. Explorar
    deshacerMovimiento(candidato, estado);  // 5. Retroceder ← CLAVE
  }
}
```

---

## Ejemplo: Permutaciones

```dart
List<List<int>> permute(List<int> nums) {
  final resultado = <List<int>>[];

  void backtrack(List<int> actual, List<bool> usados) {
    // Caso base: todos usados
    if (actual.length == nums.length) {
      resultado.add(List.from(actual));
      return;
    }

    for (int i = 0; i < nums.length; i++) {
      if (usados[i]) continue;

      // Hacer
      usados[i] = true;
      actual.add(nums[i]);

      // Explorar
      backtrack(actual, usados);

      // Deshacer ← CRUCIAL
      actual.removeLast();
      usados[i] = false;
    }
  }

  backtrack([], List.filled(nums.length, false));
  return resultado;
}

// Uso:
// permute([1, 2, 3])
// → [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

---

## Ejemplo: Subconjuntos (Power Set)

```dart
List<List<int>> subsets(List<int> nums) {
  final resultado = <List<int>>[];

  void backtrack(int inicio, List<int> actual) {
    resultado.add(List.from(actual));

    for (int i = inicio; i < nums.length; i++) {
      actual.add(nums[i]);        // Incluir
      backtrack(i + 1, actual);   // Explorar
      actual.removeLast();        // Excluir (deshacer)
    }
  }

  backtrack(0, []);
  return resultado;
}
```

---

## Memoización: Evitar recalcular

Problema de recursión: recalcula lo mismo muchas veces.

```dart
// ❌ Sin memo: O(2^n) — lento
int fib(int n) {
  if (n <= 1) return n;
  return fib(n - 1) + fib(n - 2);
}

// ✅ Con memo: O(n) — rápido
int fibMemo(int n, [Map<int, int> memo = const {}]) {
  if (n <= 1) return n;
  if (memo.containsKey(n)) return memo[n]!;
  memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
  return memo[n]!;
}
```

**Regla:** Si ves recursión con 2+ llamadas recursivas, necesitas memo.

---

## Cuándo usar cada uno

| Situación | Usar |
|-----------|------|
| Dividir y conquistar (merge sort) | Recursión simple |
| Explorar todas las combinaciones | Backtracking |
| Problema con subproblemas repetidos | Recursión + memoización |
| Árboles binarios | Recursión (DFS) |

---

## Errores comunes

| Error | Solución |
|-------|----------|
| Sin caso base | Agrega `if (caso base) return;` |
| No deshacer cambios | Siempre `deshacer()` después de recursión |
| Memo olvidado | Usar `Map` o `@cache` de Dart |
|栈 overflow | Verificar que caso base se alcanza |

---

## Mini-ejercicio

**Problema:** Genera todas las combinaciones de k números del 1 al n.

```dart
List<List<int>> combine(int n, int k) {
  // Tu código aquí
}
```

<details>
<summary>Ver solución</summary>

```dart
List<List<int>> combine(int n, int k) {
  final resultado = <List<int>>[];

  void backtrack(int inicio, List<int> actual) {
    if (actual.length == k) {
      resultado.add(List.from(actual));
      return;
    }

    for (int i = inicio; i <= n; i++) {
      actual.add(i);
      backtrack(i + 1, actual);
      actual.removeLast();
    }
  }

  backtrack(1, []);
  return resultado;
}
```
</details>

---

**Siguiente:** [10-system-design-basico.md](./10-system-design-basico.md) - System Design para Flutter
