# 02 — Análisis de Complejidad Temporal y Espacial

> Sin entender complejidad, no sabes si tu solución es rápida o lenta. Esta guía te enseña a pensarlo antes de codificar.

---

## ¿Por qué me importa esto?

Tu app funciona perfecto cuando tienes 100 usuarios. Pero cuando llegan 100,000, todo se ralentiza. ¿Por qué? Porque la forma en que escribiste el código **no escala**.

Big-O te dice **cómo crece** el tiempo de tu algoritmo cuando crecen los datos. No es matemática abstracta — es la diferencia entre una app que carga en 1 segundo y una que tarda 10 minutos.

**Ejemplo real:** Un feed de Instagram que muestra 50 fotos carga rápido. Pero si el mismo código intenta mostrar 50,000 fotos sin optimización, el teléfono se congela. Big-O te ayuda a prever estos problemas **antes** de que ocurran.

---

## ¿Qué es un algoritmo?

Un algoritmo es simplemente una **receta paso a paso** para resolver un problema. Como una receta de cocina:

```
Receta de cocina:           Algoritmo en código:
1. Calentar aceite          1. Recorrer el array
2. Agregar cebolla           2. Para cada elemento, buscar su complemento
3. Cocinar 5 minutos        3. Si lo encuentro, retornar resultado
```

Cuando escribes un `for` loop, estás creando un algoritmo. Big-O te dice **cuánto tiempo tarda** ese algoritmo cuando los datos crecen.

---

## ¿Qué es Big-O?

### Primero: ¿Qué es "n"?

**n = cuántos datos tienes.** Es la variable más importante. Si tienes un array de 1000 elementos, n = 1000. Si tienes una lista de 50 usuarios, n = 50.

### La notación O(...)

La "O" viene de **"orden"** (en inglés, *order*). Big-O describe **el orden de crecimiento** del tiempo.

- **O(n)** se lee "orden de n" — significa que el tiempo crece **en el mismo orden** que los datos
- **O(n²)** se lee "orden de n cuadrado" — el tiempo crece **mucho más rápido** que los datos

### La pregunta clave de Big-O

> **Si duplicas la cantidad de datos (n), ¿qué pasa con el tiempo?**

| Si duplicas n y el tiempo... | Entonces es... |
|---|---|
| Se duplica | O(n) — lineal |
| Se cuadruplica | O(n²) — cuadrático |
| Apenas cambia | O(log n) — logarítmico |
| No cambia | O(1) — constante |

**Big-O no te dice "tarda 3 segundos". Te dice CÓMO crece el tiempo.** Es como comparar subir 1 peldaño vs subir una escalera de 10: la diferencia se nota más cuantas más escaleras tengas.

---

## Tabla de crecimiento visual

Esta tabla te muestra **cuántas operaciones** hace cada complejidad según el tamaño de los datos:

| Complejidad | n = 10 | n = 100 | n = 1,000 | n = 10,000 |
|---|---|---|---|---|
| **O(1)** | 1 | 1 | 1 | 1 |
| **O(log n)** | 3 | 7 | 10 | 13 |
| **O(n)** | 10 | 100 | 1,000 | 10,000 |
| **O(n log n)** | 30 | 700 | 10,000 | 130,000 |
| **O(n²)** | 100 | 10,000 | 1,000,000 | 100,000,000 |

**¿Qué ves aquí?**
- **O(1)** siempre es 1 operación. No importa si tienes 10 o 1 millón de datos.
- **O(log n)** crece muy lento. De 10 a 10,000 datos (1000× más), solo pasas de 3 a 13 operaciones (4× más).
- **O(n)** crece proporcionalmente. 100× más datos = 100× más tiempo.
- **O(n²)** crece explosivamente. 100× más datos = 10,000× más tiempo.

---

## Las 4 complejidades esenciales

Estas son las que necesitas memorizar. Las demás son casos extremos.

### O(1) — Constante

**Qué significa:** El tiempo **no cambia** sin importar cuántos datos tengas.

**Analogía:** Buscar tu nombre en la guía telefónica si sabes que empieza con "M" — vas directo a esa sección.

**En código:** Acceder a un elemento por índice.

```dart
int obtenerPrimero(List<int> arr) {
  return arr[0]; // Siempre 1 operación, sin importar el tamaño
}
```

**Cuándo la ves:** HashMap lookups, arrays por índice, operaciones matemáticas directas.

---

### O(n) — Lineal

**Qué significa:** El tiempo crece **en la misma proporción** que los datos. Si duplicas los datos, duplicas el tiempo.

**Analogía:** Revisar un listado completo de tareas — lees cada tarea una por una.

**En código:** Un solo `for` loop que recorre todo el array.

```dart
int sumarTodo(List<int> arr) {
  int total = 0;
  for (int x in arr) {   // Recorre cada elemento una vez
    total += x;
  }
  return total;
}
// 10 datos → 10 operaciones
// 100 datos → 100 operaciones
```

**Cuándo la ves:** Recorrer un array, buscar en una lista no ordenada, contar frecuencias.

---

### O(n²) — Cuadrático

**Qué significa:** El tiempo crece **al cuadrado** de los datos. Si duplicas los datos, el tiempo se **cuadruplica**.

**Analogía:** Comparar cada libro de una estantería con todos los demás para ver cuáles son iguales.

**En código:** Dos `for` loops anidados.

```dart
bool tieneDuplicados(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {
    for (int j = i + 1; j < arr.length; j++) {  // Para cada i, recorre todo lo que queda
      if (arr[i] == arr[j]) return true;
    }
  }
  return false;
}
// 10 datos → ~50 operaciones
// 100 datos → ~5,000 operaciones
// 1,000 datos → ~500,000 operaciones
```

**Cuándo la ves:** Comparar todos con todos, algoritmos de sorting ingenuos, programación dinámica 2D.

**⚠️ Problema:** Con n = 10,000, ya son 100 millones de operaciones. Con n = 100,000, serían 10 mil millones — demasiado para 1 segundo.

---

### O(log n) — Logarítmica

**Qué significa:** El tiempo crece **muy lento**. Cada vez que duplicas los datos, solo necesitas **1 paso más**.

**Analogía:** Buscar una palabra en el diccionario: abres por la mitad, decides si ir a la izquierda o derecha, y repites. Con 1000 páginas, solo necesitas ~10 pasos.

**En código:** Binary search — divides el espacio de búsqueda por la mitad en cada paso.

```dart
int busquedaBinaria(List<int> arr, int target) {
  int left = 0, right = arr.length - 1;

  while (left <= right) {
    int mid = left + (right - left) ~/ 2;  // Divides por la mitad

    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) left = mid + 1;   // Busca en la mitad derecha
    else right = mid - 1;                          // Busca en la mitad izquierda
  }
  return -1;
}
// 1,000 datos → ~10 pasos
// 1,000,000 datos → ~20 pasos
// 1,000,000,000 datos → ~30 pasos
```

**¿Por qué log n?** Porque `log₂(n)` = "¿cuántas veces tengo que dividir n por 2 para llegar a 1?"

| n | log₂(n) |
|---|---|
| 8 | 3 |
| 1,000 | ~10 |
| 1,000,000 | ~20 |
| 1,000,000,000 | ~30 |

**Cuándo la ves:** Binary search, buscar en árboles balanceados, algoritmos que dividen y conquistan.

---

## Complejidades que debes conocer (pero no memorizar)

| Complejidad | Cuándo aparece | ¿Es aceptable? |
|---|---|---|
| **O(n log n)** | Sorting (merge sort, quicksort) | Sí, para n ≤ 10⁵ |
| **O(n³)** | Tres loops anidados, Floyd-Warshall | Solo para n ≤ 500 |
| **O(2ⁿ)** | Probar todas las combinaciones | Solo para n ≤ 20 |
| **O(n!)** | Permutaciones de todos los elementos | Solo para n ≤ 10 |

**Regla simple:** Si n es grande (10,000+), necesitas O(n) o mejor. Si n es pequeño (10-20), puedes usar O(2ⁿ) o incluso O(n!).

---

## Regla Práctica: ¿Qué complejidad necesito?

### ¿Por qué 10⁸?

Un procesador moderno ejecuta aproximadamente **100 millones de operaciones por segundo** (10⁸). Es como un límite de velocidad: si tu algoritmo hace más de 100 millones de operaciones, será demasiado lento para 1 segundo.

### Ejemplo paso a paso

Imagina que tu problema tiene n = 10,000 datos:

```
O(n)     →  10,000 operaciones     → 0.0001 segundos ✓ rápido
O(n log n) →  130,000 operaciones   → 0.001 segundos  ✓ rápido
O(n²)    → 100,000,000 operaciones  → 1 segundo       ⚠️ justo en el límite
O(n³)    → 10¹² operaciones         → 10,000 segundos ✗ demasiado lento
```

### Tabla de referencia

| Si el problema dice... | Tu algoritmo debe ser... | Por qué |
|---|---|---|
| `n ≤ 10` | O(n!) o O(2ⁿ) | Puedes probar todo |
| `n ≤ 100` | O(n³) | 1 millón de ops cabe |
| `n ≤ 5,000` | O(n²) | 25 millones de ops caben |
| `n ≤ 100,000` | O(n log n) | 1.7 millones de ops |
| `n ≤ 10,000,000` | O(n) | Directo y rápido |

---

## Cómo calcular la complejidad: 3 patrones

No necesitas memorizar 7 reglas. Solo necesitas reconocer **3 patrones**:

### Patrón 1: Un solo bucle → O(n)

Si recorres los datos **una vez**, es O(n).

```dart
int sumar(List<int> arr) {
  int total = 0;
  for (int x in arr) {  // ← Un solo loop
    total += x;
  }
  return total;
}
// n datos → n operaciones → O(n)
```

**Visual:** `for (cada elemento) → hacer algo` = O(n)

---

### Patrón 2: Bucles anidados → O(n²)

Si para **cada elemento** recorres **todos los demás**, es O(n²).

```dart
bool hayDuplicado(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {        // ← Primer loop: n veces
    for (int j = i + 1; j < arr.length; j++) {  // ← Segundo loop: n veces
      if (arr[i] == arr[j]) return true;
    }
  }
  return false;
}
// n datos × n datos = n² operaciones → O(n²)
```

**Visual:** `for (cada elemento) { for (cada otro elemento) }` = O(n²)

**Variante importante:** Si el segundo loop **crece** con i (como `for j = i`), sigue siendo O(n²) porque en el peor caso recorre ~n²/2 operaciones, y Big-O ignora constantes.

```dart
// O(n²) — el segundo loop empieza en i, no en 0
for (int i = 0; i < n; i++)
  for (int j = i; j < n; j++) { ... }
```

---

### Patrón 3: Dividir por la mitad → O(log n)

Si en cada paso **divides el espacio de búsqueda por 2**, es O(log n).

```dart
int busquedaBinaria(List<int> arr, int target) {
  int left = 0, right = arr.length - 1;

  while (left <= right) {  // ← Se ejecuta log₂(n) veces
    int mid = left + (right - left) ~/ 2;

    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}
// 1000 datos → 10 pasos
// 1,000,000 datos → 20 pasos
```

**Visual:** `while (n > 1) { n = n ~/ 2; }` = O(log n)

**¿Cómo saber si es O(log n)?** Pregúntate: "¿En cada paso, descarto la mitad de los datos?" Si la respuesta es sí, es O(log n).

---

## Reglas adicionales (cuando se combinan)

En la vida real, los algoritmos combinan patrones. Hay 2 reglas simples:

### Si las operaciones son secuencias → toma la MÁS GRANDE

```dart
// Esta función tiene dos partes separadas
void ejemplo(List<int> arr) {
  // Parte 1: O(n)
  for (int x in arr) {
    print(x);
  }

  // Parte 2: O(n²)
  for (int i = 0; i < arr.length; i++)
    for (int j = 0; j < arr.length; j++) {
      print(arr[i] + arr[j]);
    }
}
// Total: O(n) + O(n²) = O(n²) — tomamos la parte más lenta
```

**Regla:** Si haces algo de O(n) y luego algo de O(n²), el total es O(n²). La parte más lenta domina.

### Si los bucles son anidados → se multiplican

```dart
for (int i = 0; i < n; i++)      // n veces
  for (int j = 0; j < m; j++)    // m veces
    print(i + j);
// Total: O(n × m)
```

**Regla:** Si un loop está dentro de otro, multiplicas las complejidades.

---

## Ejemplos completos en Dart

### Ejemplo 1: O(n) — Sumar elementos

```dart
// ¿Por qué O(n)? Porque recorremos cada elemento una vez.
int sumar(List<int> arr) {
  int total = 0;
  for (int x in arr) {
    total += x;
  }
  return total;
}
// Con arr de 1000 elementos: 1000 operaciones
```

### Ejemplo 2: O(n²) — Buscar duplicados (brute force)

```dart
// ¿Por qué O(n²)? Para cada elemento, comparamos con todos los demás.
bool tieneDuplicado(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {
    for (int j = i + 1; j < arr.length; j++) {
      if (arr[i] == arr[j]) return true;
    }
  }
  return false;
}
// Con arr de 1000 elementos: ~500,000 operaciones
```

### Ejemplo 3: O(n) — Buscar duplicados (optimizado)

```dart
// ¿Por qué O(n)? Porque usamos un Set para búsqueda O(1).
bool tieneDuplicadoOptimizado(List<int> arr) {
  Set<int> seen = {};
  for (int x in arr) {
    if (seen.contains(x)) return true;  // contains en Set es O(1)
    seen.add(x);
  }
  return false;
}
// Con arr de 1000 elementos: ~1000 operaciones
// ¡1000× más rápido que la versión O(n²)!
```

### Ejemplo 4: O(log n) — Binary Search

```dart
// ¿Por qué O(log n)? Porque dividimos el array por la mitad en cada paso.
int busquedaBinaria(List<int> arr, int target) {
  int left = 0, right = arr.length - 1;

  while (left <= right) {
    int mid = left + (right - left) ~/ 2;

    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}
// Con arr de 1,000,000 elementos: solo ~20 pasos
```

---

## Complejidad Espacial

No solo importa el tiempo. El **espacio** (memoria) también cuenta.

| Estructura | Espacio | Cuándo importa |
|---|---|---|
| Array de tamaño n | O(n) | Siempre es O(n) para el input |
| HashMap con n elementos | O(n) | Cuando el input es grande |
| Recursión profunda | O(n) stack | Puede causar stack overflow |
| Variable auxiliar | O(1) | El óptimo en espacio |

### Ejemplo: espacio en recursión

```dart
// O(n) espacio por el call stack
// Cada llamada recursiva guarda un frame en memoria
int factorial(int n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);  // 5 llamadas apiladas para n=5
}

// O(1) espacio — iterativo
// Solo usa una variable, sin importar n
int factorialIterativo(int n) {
  int result = 1;
  for (int i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}
```

**¿Por qué importa?** Si n = 100,000 y usas recursión, necesitas 100,000 frames de memoria. Si el stack overflow, la app crashea. La versión iterativa usa siempre 1 variable.

---

## El Tradeoff Tiempo-Espacio

Muchas veces puedes intercambiar tiempo por espacio:

| Enfoque | Tiempo | Espacio |
|---|---|---|
| Brute force (re-calcular todo) | O(n²) | O(1) |
| Pre-computar con HashMap | O(n) | O(n) |
| Pre-computar con Prefix Sum | O(n) | O(n) |

**Ejemplo:** Quieres saber la suma de cada subarray.

- **Brute force:** Para cada subarray, recorres todos los elementos → O(n²)
- **Prefix Sum:** Pre-calculas las sumas acumuladas en un array auxiliar → O(n) pero usas O(n) de espacio extra

**Regla general:** Si las constraints de memoria son amplias (típico en entrevistas), prioriza tiempo. Si el input es enorme, considera optimizar espacio.

---

## Mini-ejercicio: ¿Entiendes Big-O?

Responde mentalmente antes de seguir:

1. **Tienes un array de 1000 elementos. Recorres el array una vez. ¿Qué complejidad es?**
   → O(n) — un solo recorrido lineal. Con n=1000 son 1000 operaciones.

2. **Tienes dos loops anidados, cada uno recorre todo el array de 1000 elementos. ¿Cuántas operaciones? ¿Cabe en 1 segundo?**
   → O(n²) = 1000 × 1000 = 1,000,000. Sí cabe (es 0.01s). Pero si n=10⁵, serían 10¹⁰ operaciones = 100 segundos. No cabe.

3. **Tienes un array ordenado. Divides el array por la mitad en cada paso. ¿Qué complejidad es?**
   → O(log n). Con 1000 elementos, solo necesitas ~10 pasos (log₂ 1000 ≈ 10). Con 1 millón, solo ~20 pasos.

Si acertaste las 3, entiendes lo básico. Si no, vuelve a leer la sección de las 4 complejidades esenciales.

---

## Checklist antes de codificar

```
□ ¿Cuál es el tamaño máximo de n?
□ ¿Qué complejidad necesito según la tabla?
□ ¿Mi enfoque cumple esa complejidad?
□ ¿Cuánto espacio extra uso?
□ ¿Hay un tradeoff tiempo/espacio que valga la pena?
```
