# 02 — Cómo analizar la complejidad de un problema

> Cuando ves un problema en HackerRank, LeetCode o similar, necesitas saber si tu solución es **rápida antes de escribirla**. Esta guía te enseña el proceso completo, paso a paso, con ejemplos reales.

---

## ¿Por qué me importa esto?

Imagina que resuelves un problema y tu solución funciona perfecto... con 10 datos. Pero cuando el judge de HackerRank prueba con 100,000 datos, recibes **Time Limit Exceeded**. Perdiste tiempo porque no analizaste la complejidad antes de codificar.

**Big-O** es la herramienta que te dice **cómo crece** el tiempo de tu algoritmo cuando crecen los datos. No es matemática abstracta — es la diferencia entre que tu solución pase o no pase.

---

## El Proceso: 5 pasos

Cada vez que te enfrentes a un problema, sigue estos 5 pasos **en orden**:

```
┌──────────────────────────────────────────────────────────────┐
│  PASO 1: Entender el problema                                │
│  "¿Qué me piden? ¿Qué me dan?"                              │
├──────────────────────────────────────────────────────────────┤
│  PASO 2: Descifrar las constraints                           │
│  "¿Cuántos datos máximo tengo? → ¿Qué complejidad necesito?" │
├──────────────────────────────────────────────────────────────┤
│  PASO 3: Analizar mi primera idea (brute force)              │
│  "¿Qué tan lenta es? → ¿Cumple con la complejidad?"         │
├──────────────────────────────────────────────────────────────┤
│  PASO 4: Optimizar (si es necesario)                         │
│  "¿Puedo hacerlo más rápido? → ¿Con qué estructura?"        │
├──────────────────────────────────────────────────────────────┤
│  PASO 5: Verificar                                           │
│  "¿Funciona con edge cases? → ¿La complejidad es correcta?" │
└──────────────────────────────────────────────────────────────┘
```

**La pregunta clave:** Si duplicas la cantidad de datos (n), ¿qué pasa con el tiempo?

| Si duplicas n y el tiempo... | Entonces es... |
|---|---|
| Se duplica | O(n) — lineal |
| Se cuadruplica | O(n²) — cuadrático |
| Apenas cambia | O(log n) — logarítmico |
| No cambia | O(1) — constante |

Ahora veamos el proceso completo con un problema real.

---

# PARTE A: Ejemplo completo — Two Sum

Vamos a resolver el problema **Two Sum** de LeetCode/HackerRank juntos, siguiendo los 5 pasos. Cada concepto se explica en el camino.

---

## El problema

> Dado un array de enteros `nums` y un entero `target`, devuelve los **índices** de los dos números que suman `target`. Puedes asumir que hay exactamente una solución y no puedes usar el mismo elemento dos veces.
>
> Ejemplo: `nums = [2, 7, 11, 15]`, `target = 9` → respuesta: `[0, 1]` porque `nums[0] + nums[1] = 2 + 7 = 9`.

---

## PASO 1: Entender el problema

Leo el enunciado y respondo:

1. **¿Qué me dan?** Un array de números enteros y un número objetivo (target).
2. **¿Qué me piden?** Los **índices** de dos números que sumen el target.
3. **¿Qué restricciones hay?** No puedo usar el mismo elemento dos veces. Hay exactamente una solución.
4. **¿Puedo reformularlo?** "Encuentra dos números en el array que sumen el target y dime dónde están."

**Truco:** Si no puedes explicar el problema con tus propias palabras simples, no lo entiendes aún. Vuelve a leerlo.

---

## PASO 2: Descifrar las constraints

Las constraints son la **señal más fuerte** para elegir tu enfoque. Siempre léelas antes de pensar en la solución.

En este problema, las constraints típicas son:

```
2 ≤ nums.length ≤ 10⁴
-10⁹ ≤ nums[i] ≤ 10⁹
-10⁹ ≤ target ≤ 10⁹
```

**¿Qué significa esto?** La parte importante es `nums.length ≤ 10⁴`. Eso es n = 10,000.

### La regla de los 10⁸

Un procesador moderno ejecuta aproximadamente **100 millones de operaciones por segundo** (10⁸). Si tu algoritmo hace más de eso, será demasiado lento.

Entonces, con n = 10,000:

```
O(n)      →   10,000 operaciones  → 0.0001 segundos ✓ rápido
O(n log n) →  130,000 operaciones → 0.001 segundos  ✓ rápido
O(n²)     → 100,000,000 operaciones → 1 segundo      ⚠️ justo en el límite
O(n³)     → 10¹² operaciones        → 10,000 segundos ✗ demasiado lento
```

**Conclusión:** Con n ≤ 10⁴, necesito **O(n) o O(n log n)** como máximo. O(n²) está en el límite y podría fallar.

### Tabla de referencia (memorízala)

| Si el problema dice... | Tu algoritmo debe ser... | Por qué |
|---|---|---|
| `n ≤ 10` | O(n!) o O(2ⁿ) | Puedes probar todo |
| `n ≤ 100` | O(n³) | 1 millón de ops cabe |
| `n ≤ 5,000` | O(n²) | 25 millones de ops caben |
| `n ≤ 100,000` | O(n log n) | 1.7 millones de ops |
| `n ≤ 10,000,000` | O(n) | Directo y rápido |

---

## PASO 3: Analizar mi primera idea (brute force)

La primera idea que se nos ocurre es la más obvia: **probar todos los pares posibles**.

```dart
// Brute force: probar cada par de números
List<int> twoSum(List<int> nums, int target) {
  for (int i = 0; i < nums.length; i++) {         // ← Loop 1: recorre cada elemento
    for (int j = i + 1; j < nums.length; j++) {   // ← Loop 2: recorre todos los que quedan
      if (nums[i] + nums[j] == target) {
        return [i, j];
      }
    }
  }
  return [];
}
```

### Ahora analicemos la complejidad (esto es lo importante)

**¿Cuántas operaciones hace este código?**

Miro el código y cuento:

1. El **primer loop** se ejecuta `n` veces (una por cada elemento del array).
2. Para **cada** iteración del primer loop, el **segundo loop** se ejecuta hasta `n` veces más.
3. Dentro de los loops, hago una suma y una comparación (operaciones simples, O(1)).

**Total:** `n × n = n²` operaciones.

**Esto es O(n²)** — complejidad cuadrática.

### ¿Por qué O(n²)?

Porque tengo **dos loops anidados**. Para cada elemento, recorro todos los demás. Es como comparar cada libro de una estantería con todos los demás.

**La regla:** Cuando ves `for` + `for` anidados, es O(n²).

### ¿Cumple con lo que necesito?

- Necesito: O(n) o mejor
- Mi solución: O(n²)
- Con n = 10,000: serían 100,000,000 operaciones = **1 segundo exacto**

**Está justo en el límite.** Podría funcionar, pero es arriesgado. Si el problema tuviera n ≤ 100,000, O(n²) sería 10 mil millones = 100 segundos. No pasaría.

**¿Qué hago?** Optimizo.

---

## PASO 4: Optimizar

Necesito O(n). ¿Cómo puedo encontrar el complemento más rápido?

**Idea clave:** En vez de buscar el complemento recorriendo todo el array, puedo **recordar** los valores que ya vi. Si estoy en el elemento `7` y necesito un `2` (porque 7 + 2 = 9), no necesito buscar — solo pregunto: "¿ya vi un 2?"

Para eso uso un **HashMap** (Map en Dart), que permite buscar en O(1).

```dart
// Optimizado con HashMap: O(n)
List<int> twoSum(List<int> nums, int target) {
  Map<int, int> seen = {};  // ← HashMap: valor → índice

  for (int i = 0; i < nums.length; i++) {   // ← Solo un loop
    int complemento = target - nums[i];      // Calculo qué necesito

    if (seen.containsKey(complemento)) {     // ¿Ya vi ese número? O(1)
      return [seen[complemento]!, i];
    }

    seen[nums[i]] = i;  // Guardo el valor actual para después
  }
  return [];
}
```

### Analicemos la nueva complejidad

**¿Cuántas operaciones hace ahora?**

1. Un solo loop que recorre `n` elementos.
2. Dentro del loop: una resta O(1), una búsqueda en Map O(1), una inserción en Map O(1).

**Total:** `n × 3 = 3n` operaciones. Las constantes se ignoran en Big-O.

**Esto es O(n)** — complejidad lineal.

### ¿Por qué es O(n)?

- **Un solo loop** → O(n)
- **Las operaciones dentro del loop son O(1)** → no cambian la complejidad
- **La estructura (HashMap) es clave** → sin ella, la búsqueda sería O(n) y el total sería O(n²)

### Comparación

| Enfoque | Complejidad | Con n = 10,000 |
|---|---|---|
| Brute force (2 loops) | O(n²) | 100,000,000 ops |
| HashMap (1 loop) | O(n) | 10,000 ops |

**10,000 veces más rápido.** Esa es la diferencia entre que tu solución pase o no pase.

---

## PASO 5: Verificar

Antes de enviar, pruebo con casos extremos:

**Caso normal:** `nums = [2, 7, 11, 15]`, `target = 9` → `[0, 1]` ✓

**Edge case — números negativos:** `nums = [-3, 4, 3, 90]`, `target = 0` → `[0, 2]` ✓

**Edge case — números repetidos:** `nums = [3, 3]`, `target = 6` → `[0, 1]` ✓ (funciona porque guardamos el índice antes de verificar)

**Edge case — array de 2 elementos:** `nums = [1, 2]`, `target = 3` → `[0, 1]` ✓

---

## Lección de Two Sum

| Concepto | Lo que aprendimos |
|---|---|
| **Constraints** | n ≤ 10⁴ → necesito O(n) o mejor |
| **Brute force** | 2 loops anidados → O(n²) → no cumple |
| **Optimización** | HashMap para búsqueda O(1) → O(n) → cumple |
| **Estructura clave** | Map en Dart: `containsKey()` y `[]` son O(1) |

Ahora que hemos visto el proceso completo una vez, vamos a practicarlo con 4 problemas más de HackerRank. Cada uno sigue los mismos 5 pasos.

---

# PARTE B: Ejemplos guiados — 4 problemas de HackerRank

En esta sección repetimos el proceso de los 5 pasos con problemas reales. Cada problema te enseña algo nuevo sobre cómo analizar la complejidad.

---

## Ejemplo 1: Beautiful Days at the Movies

> [Problema en HackerRank](https://www.hackerrank.com/challenges/beautiful-days-at-the-movies/problem)

### El problema

> Lily quiere ir al cine en días "beautiful" (hermosos). Un día es beautiful si `|day - reverse(day)| % k == 0`.
>
> Dados los días `i` (inicio) y `j` (fin), y un divisor `k`, devuelve cuántos días beautiful hay en el rango.
>
> Ejemplo: `i = 20`, `j = 23`, `k = 6`
> - Día 20: reverse(20) = 02 = 2 → |20 - 2| = 18 → 18 % 6 = 0 ✓ beautiful
> - Día 21: reverse(21) = 12 → |21 - 12| = 9 → 9 % 6 = 3 ✗ no beautiful
> - Día 22: reverse(22) = 22 → |22 - 22| = 0 → 0 % 6 = 0 ✓ beautiful
> - Día 23: reverse(23) = 32 → |23 - 32| = 9 → 9 % 6 = 3 ✗ no beautiful
> - Respuesta: 2

---

### PASO 1: Entender el problema

1. **¿Qué me dan?** Dos números (inicio y fin de un rango) y un divisor.
2. **¿Qué me piden?** Contar cuántos números en el rango cumplen la condición.
3. **¿Qué es reverse?** Un número al revés: 21 → 12, 202 → 202, 123 → 321.
4. **¿Qué es beautiful?** Cuando la diferencia absoluta entre el número y su reverso es divisible por k.

---

### PASO 2: Descifrar las constraints

```
1 ≤ i ≤ j ≤ 10⁷
1 ≤ k ≤ 10⁹
```

La parte clave es `j ≤ 10⁷`. El rango puede tener hasta **10 millones de días**.

Con n = 10⁷:

| Complejidad | Operaciones | ¿Cabe? |
|---|---|---|
| O(n) | 10,000,000 | ✓ Sí |
| O(n log n) | 230,000,000 | ⚠️ En el límite |
| O(n²) | 10¹⁴ | ✗ No |

**Necesito O(n) o mejor.**

---

### PASO 3: Analizar mi primera idea

La idea obvia: **recorrer cada día del rango**, calcular si es beautiful, y contar.

```dart
int beautifulDays(int i, int j, int k) {
  int count = 0;
  for (int day = i; day <= j; day++) {     // ← Un solo loop
    int reversed = int.parse(day.toString().split('').reversed.join());
    if ((day - reversed).abs() % k == 0) {
      count++;
    }
  }
  return count;
}
```

**Análisis:**

1. Un solo loop que va de `i` a `j`.
2. El número de iteraciones es `j - i + 1` (el tamaño del rango).
3. Dentro del loop: convertir a string, invertir, convertir a número, calcular módulo. Todo O(1) o casi O(1).

**¿Qué es "n" aquí?** n = `j - i + 1` (la cantidad de días en el rango).

**Complejidad:** O(n) — un solo recorrido lineal.

**¿Cumple?** Sí. Con n = 10⁷, son 10 millones de operaciones. Cabe en menos de 1 segundo.

---

### PASO 4: Optimizar

**¿Necesito optimizar?** No. O(n) cumple con las constraints.

A veces **no necesitas optimizar**. Si tu solución ya cumple con la complejidad necesaria, está bien así. No todo problema requiere la solución más compleja.

---

### PASO 5: Verificar

**Caso normal:** `i = 20, j = 23, k = 6` → 2 ✓

**Edge case — un solo día:** `i = 5, j = 5, k = 1` → reverse(5) = 5 → |5-5| = 0 → 0 % 1 = 0 → 1 ✓

**Edge case — rango grande:** `i = 1, j = 10⁷, k = 1` → todos son beautiful (cualquier cosa mod 1 = 0) → 10⁷ ✓

---

### Lección de Beautiful Days

| Concepto | Lo que aprendimos |
|---|---|
| **Un solo loop** | Un `for` que recorre un rango = O(n) |
| **No siempre optimizar** | Si O(n) cumple, no busques algo más complejo |
| **Operaciones dentro del loop** | Si son simples (suma, módulo), no cambian la complejidad |

---

## Ejemplo 2: Jumping on the Clouds — Revisited

> [Problema en HackerRank](https://www.hackerrank.com/challenges/jumping-on-the-clouds-revisited/problem)

### El problema

> Un niño salta en nubes. Hay nubes normales (0) y nubes de trueno (1). El niño empieza en la nube 0 con energía `e`.
>
> - Salta `k` posiciones → consume 1 de energía
> - Si cae en nube de trueno (1) → consume 2 de energía extra
> - El juego termina cuando vuelve a la nube 0
>
> Ejemplo: `c = [0, 0, 1, 0, 0, 1, 1, 0]`, `k = 2`, `e = 100`
> - Salta 0→2 (trueno): energía = 100 - 1 - 2 = 97
> - Salta 2→4: energía = 97 - 1 = 96
> - Salta 4→6 (trueno): energía = 96 - 1 - 2 = 93
> - Salta 6→0: energía = 93 - 1 = 92
> - Respuesta: 92

---

### PASO 1: Entender el problema

1. **¿Qué me dan?** Un array de nubes (0 o 1), un tamaño de salto k, y energía inicial e.
2. **¿Qué me piden?** La energía restante al volver a la nube 0.
3. **¿Cómo salta?** Siempre de `k` en `k` posiciones, en un array circular.
4. **¿Qué cuesta?** 1 energía por salto + 2 extra si la nube es de trueno.

---

### PASO 2: Descifrar las constraints

```
2 ≤ n ≤ 25
1 ≤ k ≤ n
0 ≤ e ≤ 100
```

**n ≤ 25.** Esto es **muy pequeño**. Casi cualquier complejidad funciona.

| Complejidad | Operaciones | ¿Cabe? |
|---|---|---|
| O(n) | 25 | ✓ Sí |
| O(n²) | 625 | ✓ Sí |
| O(2ⁿ) | 33 millones | ⚠️ Mucho, pero n es tan pequeño que... |

**Con n tan pequeño, no necesitas preocuparte por la complejidad.** Pero vamos a analizarla igual para practicar.

---

### PASO 3: Analizar mi primera idea

La idea: **simular los saltos** hasta volver a la nube 0.

```dart
int jumpingOnClouds(List<int> c, int k, int e) {
  int energy = e;
  int pos = 0;

  do {
    pos = (pos + k) % c.length;  // Saltar k posiciones (circular)
    energy--;                     // Cada salto cuesta 1

    if (c[pos] == 1) {
      energy -= 2;  // Nube de trueno cuesta 2 extra
    }
  } while (pos != 0);

  return energy;
}
```

**Análisis:**

1. El loop ejecuta `n / k` iteraciones (salta de k en k posiciones hasta volver al inicio).
2. Dentro del loop: una suma, un módulo, una resta, una comparación. Todo O(1).

**¿Qué es "n" aquí?** n = `c.length` (el número de nubes).

**Complejidad:** O(n/k) — pero como k ≥ 1, en el peor caso es O(n).

**¿Cumple?** Sí. Con n ≤ 25, son máximo 25 iteraciones. Cabe sin problemas.

---

### PASO 4: Optimizar

**¿Necesito optimizar?** No. O(n) con n ≤ 25 es instantáneo.

Pero vale la pena notar algo: **el módulo `%` crea un array circular**. Cuando estás en la última posición y saltas, vuelves al inicio. Esto es un patrón común que verás en muchos problemas.

---

### PASO 5: Verificar

**Caso normal:** `c = [0,0,1,0,0,1,1,0]`, `k = 2`, `e = 100` → 92 ✓

**Edge case — sin truenos:** `c = [0,0,0,0]`, `k = 1`, `e = 10` → 4 saltos, sin truenos → 10 - 4 = 6 ✓

**Edge case — todas trueno:** `c = [1,1,1,1]`, `k = 2`, `e = 10` → 2 saltos, 2 truenos → 10 - 2 - 4 = 4 ✓

---

### Lección de Jumping on Clouds

| Concepto | Lo que aprendimos |
|---|---|
| **n pequeño** | Cuando n ≤ 25-50, casi cualquier complejidad funciona |
| **Simular es válido** | Si las constraints lo permiten, simular paso a paso está bien |
| **Módulo para circular** | `% c.length` crea un array circular (el último salta al primero) |
| **O(n/k)** | Un loop con salto de k tiene complejidad O(n/k), no O(n) |

---

## Ejemplo 3: Circular Array Rotation

> [Problema en HackerRank](https://www.hackerrank.com/challenges/circular-array-rotation/problem)

### El problema

> Dado un array de enteros, rota el array `k` veces a la derecha. Después, responde `q` queries: "¿qué valor hay en el índice `m`?"
>
> Rotación a la derecha: el último elemento se mueve al inicio, todos los demás se corren a la derecha.
>
> Ejemplo: `a = [1, 2, 3]`, `k = 2` rotaciones:
> - Rotación 1: `[3, 1, 2]`
> - Rotación 2: `[2, 3, 1]`
> - Query índice 0 → 2, índice 1 → 3, índice 2 → 1

---

### PASO 1: Entender el problema

1. **¿Qué me dan?** Un array, un número de rotaciones k, y una lista de queries (índices).
2. **¿Qué me piden?** Los valores en los índices dados **después** de rotar k veces.
3. **¿Qué es rotar?** Mover todos los elementos a la derecha, el último pasa al inicio.

---

### PASO 2: Descifrar las constraints

```
1 ≤ n ≤ 10⁵
1 ≤ k ≤ 10⁵
1 ≤ q ≤ 500
```

Aquí hay **dos números grandes**: n y k, ambos hasta 100,000.

**Opción 1: Simular las rotaciones.** Cada rotación recorre todo el array (O(n)) y haces k rotaciones → O(n × k). Con n = 100,000 y k = 100,000 → 10 mil millones de operaciones. **No cabe.**

**Opción 2: Buscar una fórmula.** Si puedo calcular la posición final sin simular, puedo hacerlo en O(n) o mejor.

**Necesito O(n) o O(n + q).**

---

### PASO 3: Analizar mi primera idea (brute force)

La idea obvia: **simular cada rotación**.

```dart
// Brute force: O(n × k) — DEMASIADO LENTO
List<int> circularArrayRotation(List<int> a, int k, List<int> queries) {
  for (int r = 0; r < k; r++) {        // ← k rotaciones
    int last = a.last;
    a.removeLast();                     // O(n) — desplaza elementos
    a.insert(0, last);                  // O(n) — desplaza elementos
  }

  List<int> result = [];
  for (int q in queries) {
    result.add(a[q]);
  }
  return result;
}
```

**Análisis:**

1. El primer loop se ejecuta `k` veces.
2. Dentro: `removeLast()` es O(1), pero `insert(0, last)` es **O(n)** porque mueve todos los elementos.
3. Total: `k × n` operaciones.

**O(n × k)** — Con n = 100,000 y k = 100,000 = **10¹⁰ operaciones**. No cabe.

---

### PASO 4: Optimizar — La fórmula mágica

**Pregunta clave:** ¿Necesito realmente simular las rotaciones?

Si roto un array de tamaño n, **k veces**, el elemento que estaba en la posición `i` termina en la posición `(i + k) % n`.

**Ejemplo:** Array `[1, 2, 3, 4, 5]`, k = 2 rotaciones.

| Posición original | Posición después de 2 rotaciones |
|---|---|
| 0 → (0+2) % 5 = 2 | El 1 queda en la posición 2 |
| 1 → (1+2) % 5 = 3 | El 2 queda en la posición 3 |
| 2 → (2+2) % 5 = 4 | El 3 queda en la posición 4 |
| 3 → (3+2) % 5 = 0 | El 4 queda en la posición 0 |
| 4 → (4+2) % 5 = 1 | El 5 queda en la posición 1 |

Resultado: `[4, 5, 1, 2, 3]` ✓

**Pero no necesito construir el array rotado.** Si me preguntan por el índice `m`, puedo calcular directamente: "¿Qué elemento original terminó en la posición m?"

La fórmula inversa: si el elemento original en posición `i` va a parar a `(i + k) % n`, entonces el elemento en la posición `m` después de rotar es el que estaba en la posición `(m - k % n + n) % n` original.

```dart
// Optimizado: O(n + q) — construir mapa de respuestas
List<int> circularArrayRotation(List<int> a, int k, List<int> queries) {
  int n = a.length;
  List<int> result = [];

  for (int q in queries) {
    // ¿Qué elemento original está en la posición q después de k rotaciones?
    int originalIndex = (q - k % n + n) % n;
    result.add(a[originalIndex]);
  }
  return result;
}
```

**Análisis:**

1. Un loop sobre las queries: `q` iteraciones.
2. Dentro: operaciones aritméticas O(1).
3. No construyo el array rotado.

**Complejidad:** O(q) — donde q es el número de queries. Con q ≤ 500, esto es instantáneo.

**¿Por qué funciona?** Porque la rotación es una operación **aritmética**, no necesito simularla. Es como saber que girar un reloj 13 horas es lo mismo que girar 1 hora (13 % 12 = 1).

---

### PASO 5: Verificar

**Caso normal:** `a = [1,2,3]`, `k = 2`, queries = [0,1,2] → `[2, 3, 1]` ✓

**Edge case — k > n:** `a = [1,2,3]`, `k = 5` → 5 % 3 = 2 rotaciones efectivas → `[2, 3, 1]` ✓

**Edge case — k = 0:** `a = [1,2,3]`, `k = 0` → sin rotación → `[1, 2, 3]` ✓

---

### Lección de Circular Array Rotation

| Concepto | Lo que aprendimos |
|---|---|
| **No siempre simular** | A veces una fórmula matemática reemplaza un loop pesado |
| **Módulo para circular** | `% n` convierte posiciones lineales en circulares |
| **O(n × k) → O(q)** | La optimización puede ser dramática |
| **Identificar la fórmula** | Pregúntate: "¿Puedo calcular la respuesta sin construir todo?" |

---

## Ejemplo 4: Sequence Equation

> [Problema en HackerRank](https://www.hackerrank.com/challenges/permutation-equation/problem)

### El problema

> Dada una secuencia `p` de `n` enteros distintos donde cada elemento satisface `1 ≤ p[i] ≤ n`, para cada `x` de 1 a n, encuentra un `y` tal que `p(p(y)) = x`.
>
> Ejemplo: `p = [2, 3, 1]` (donde p[1]=2, p[2]=3, p[3]=1)
> - x = 1: necesito y donde p(p(y)) = 1. Si y = 2, p(2) = 3, p(3) = 1 ✓ → y = 2
> - x = 2: necesito y donde p(p(y)) = 2. Si y = 1, p(1) = 2, p(2) = 3... no. Si y = 3, p(3) = 1, p(1) = 2 ✓ → y = 3
> - x = 3: necesito y donde p(p(y)) = 3. Si y = 1, p(1) = 2, p(2) = 3 ✓ → y = 1
> - Respuesta: `[2, 3, 1]`

---

### PASO 1: Entender el problema

1. **¿Qué me dan?** Una permutación `p` (números del 1 al n, todos distintos).
2. **¿Qué me piden?** Para cada `x`, encontrar `y` tal que `p(p(y)) = x`.
3. **¿Qué significa p(p(y)) = x?** Primero aplico p a y, luego aplico p al resultado, y debe dar x.

**Reformulación:** Si `p` es una función, busco `y` tal que `p(p(y)) = x`. Es como "aplicar p dos veces".

---

### PASO 2: Descifrar las constraints

```
1 ≤ n ≤ 50
1 ≤ p[i] ≤ n
```

**n ≤ 50.** Esto es **muy pequeño**. Cualquier complejidad funciona. Pero vamos a practicar el análisis.

---

### PASO 3: Analizar mi primera idea (brute force)

La idea: **probar cada y posible** para cada x.

```dart
// Brute force: O(n³) — funciona pero es lento
List<int> permutationEquation(List<int> p) {
  List<int> result = [];
  int n = p.length;

  for (int x = 1; x <= n; x++) {          // Para cada x
    for (int y = 1; y <= n; y++) {         // Probar cada y
      if (p[p[y - 1] - 1] == x) {         // ¿p(p(y)) = x?
        result.add(y);
        break;
      }
    }
  }
  return result;
}
```

**Análisis:**

1. Loop externo: `n` iteraciones (para cada x).
2. Loop interno: `n` iteraciones (probar cada y).
3. Dentro: una operación de array O(1).

**O(n²)** — Con n = 50, son 2,500 operaciones. Cabe perfectamente.

**Pero podemos hacerlo mejor.**

---

### PASO 4: Optimizar — Pre-computar con Map

**Pregunta clave:** ¿Puedo calcular la respuesta sin probar cada y?

**Observación:** Si `p(p(y)) = x`, entonces `p(y) = p⁻¹(x)` (el inverso de p aplicado a x). Es decir:

1. Primero invierto `p`: creo un mapa donde `inverse[p[i]] = i + 1`.
2. Luego, para cada `x`, `y = inverse[inverse[x]]`.

```dart
// Optimizado: O(n) con pre-computación
List<int> permutationEquation(List<int> p) {
  int n = p.length;

  // Paso 1: Construir el mapa inverso — O(n)
  Map<int, int> inverse = {};
  for (int i = 0; i < n; i++) {
    inverse[p[i]] = i + 1;  // p[i] = valor → posición
  }

  // Paso 2: Para cada x, y = inverse[inverse[x]] — O(n)
  List<int> result = [];
  for (int x = 1; x <= n; x++) {
    result.add(inverse[inverse[x]!]!);
  }
  return result;
}
```

**Análisis:**

1. Construir el mapa inverso: un loop de `n` iteraciones → O(n).
2. Construir el resultado: otro loop de `n` iteraciones → O(n).
3. Dentro de cada loop: operaciones O(1) en el Map.

**O(n) + O(n) = O(n)** — Complejidad lineal.

**¿Por qué funciona?** Porque el mapa inverso me permite "deshacer" la función p en O(1). Es como tener un diccionario: en vez de probar todas las traducciones, busco directamente.

---

### PASO 5: Verificar

**Caso normal:** `p = [2, 3, 1]` → `[2, 3, 1]` ✓

**Caso 2:** `p = [4, 3, 5, 1, 2]` → `[1, 3, 5, 4, 2]` ✓

**Edge case — n = 1:** `p = [1]` → inverse = {1: 1} → y = inverse[inverse[1]] = inverse[1] = 1 → `[1]` ✓

---

### Lección de Sequence Equation

| Concepto | Lo que aprendimos |
|---|---|
| **Pre-computar** | Construir un mapa auxiliar responde queries en O(1) |
| **Map inverso** | Invertir una función: `f(x) = y` → `inverse[y] = x` |
| **O(n²) → O(n)** | Pre-computar transforma un problema cuadrático en lineal |
| **Patrón de pre-computación** | Si vas a preguntar lo mismo muchas veces, pre-calcula |

---

# PARTE C: Referencia rápida

Después de resolver problemas, usa esta sección como **consulta rápida**. Aquí están los conceptos teóricos organizados para que los busques cuando los necesites.

---

## C.1 Las 4 complejidades esenciales

Estas son las que necesitas **memorizar**. Las demás son casos extremos.

### O(1) — Constante

**Qué significa:** El tiempo **no cambia** sin importar cuántos datos tengas.

**Analogía:** Buscar tu nombre en la guía telefónica si sabes que empieza con "M" — vas directo a esa sección.

```dart
int obtenerPrimero(List<int> arr) {
  return arr[0]; // Siempre 1 operación, sin importar el tamaño
}
```

**Cuándo la ves:** Acceso por índice, HashMap lookups, operaciones matemáticas directas.

---

### O(n) — Lineal

**Qué significa:** El tiempo crece **en la misma proporción** que los datos.

**Analogía:** Revisar un listado completo de tareas — lees cada tarea una por una.

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

**Cuándo la ves:** Recorrer un array, contar frecuencias, buscar en lista no ordenada.

---

### O(n²) — Cuadrático

**Qué significa:** El tiempo crece **al cuadrado** de los datos.

**Analogía:** Comparar cada libro de una estantería con todos los demás.

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

**⚠️ Problema:** Con n = 10,000, ya son 100 millones de operaciones. Con n = 100,000, serían 10 mil millones — demasiado para 1 segundo.

---

### O(log n) — Logarítmica

**Qué significa:** El tiempo crece **muy lento**. Cada vez que duplicas los datos, solo necesitas **1 paso más**.

**Analogía:** Buscar una palabra en el diccionario: abres por la mitad, decides si ir a la izquierda o derecha, y repites.

```dart
int busquedaBinaria(List<int> arr, int target) {
  int left = 0, right = arr.length - 1;

  while (left <= right) {
    int mid = left + (right - left) ~/ 2;  // Divides por la mitad

    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
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

---

## C.2 Tabla de crecimiento visual

Cuántas operaciones hace cada complejidad según el tamaño de los datos:

| Complejidad | n = 10 | n = 100 | n = 1,000 | n = 10,000 |
|---|---|---|---|---|
| **O(1)** | 1 | 1 | 1 | 1 |
| **O(log n)** | 3 | 7 | 10 | 13 |
| **O(n)** | 10 | 100 | 1,000 | 10,000 |
| **O(n log n)** | 30 | 700 | 10,000 | 130,000 |
| **O(n²)** | 100 | 10,000 | 1,000,000 | 100,000,000 |

- **O(1)** siempre es 1 operación.
- **O(log n)** crece muy lento. De 10 a 10,000 datos (1000× más), solo pasas de 3 a 13 operaciones (4× más).
- **O(n)** crece proporcionalmente. 100× más datos = 100× más tiempo.
- **O(n²)** crece explosivamente. 100× más datos = 10,000× más tiempo.

---

## C.3 Complejidades que debes conocer (pero no memorizar)

| Complejidad | Cuándo aparece | ¿Es aceptable? |
|---|---|---|
| **O(n log n)** | Sorting (merge sort, quicksort) | Sí, para n ≤ 10⁵ |
| **O(n³)** | Tres loops anidados, Floyd-Warshall | Solo para n ≤ 500 |
| **O(2ⁿ)** | Probar todas las combinaciones | Solo para n ≤ 20 |
| **O(n!)** | Permutaciones de todos los elementos | Solo para n ≤ 10 |

---

## C.4 Cómo analizar código: 3 patrones

No necesitas memorizar reglas complejas. Solo necesitas reconocer **3 patrones**:

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

**Señal:** `for (cada elemento) → hacer algo`

---

### Patrón 2: Bucles anidados → O(n²)

Si para **cada elemento** recorres **todos los demás**, es O(n²).

```dart
bool hayDuplicado(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {        // ← n veces
    for (int j = i + 1; j < arr.length; j++) {  // ← n veces
      if (arr[i] == arr[j]) return true;
    }
  }
  return false;
}
// n × n = n² operaciones → O(n²)
```

**Señal:** `for (cada elemento) { for (cada otro elemento) }`

**Variante:** Si el segundo loop empieza en `i` (no en 0), sigue siendo O(n²). Big-O ignora constantes como 1/2.

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
```

**Señal:** `while (n > 1) { n = n ~/ 2; }`

**Pregunta clave:** "¿En cada paso, descarto la mitad de los datos?" Si es sí, es O(log n).

---

## C.5 Reglas de combinación

En la vida real, los algoritmos combinan patrones. Dos reglas simples:

### Si las operaciones son secuencias → toma la MÁS GRANDE

```dart
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
// Total: O(n) + O(n²) = O(n²) — la parte más lenta domina
```

### Si los bucles son anidados → se multiplican

```dart
for (int i = 0; i < n; i++)      // n veces
  for (int j = 0; j < m; j++)    // m veces
    print(i + j);
// Total: O(n × m)
```

---

## C.6 Complejidad espacial

No solo importa el tiempo. El **espacio** (memoria) también cuenta.

| Estructura | Espacio | Cuándo importa |
|---|---|---|
| Array de tamaño n | O(n) | Siempre es O(n) para el input |
| HashMap con n elementos | O(n) | Cuando el input es grande |
| Recursión profunda | O(n) stack | Puede causar stack overflow |
| Variable auxiliar | O(1) | El óptimo en espacio |

### Ejemplo: recursión vs iterativo

```dart
// O(n) espacio — recursión
int factorial(int n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);  // n llamadas apiladas
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

## C.7 El Tradeoff Tiempo-Espacio

Muchas veces puedes intercambiar tiempo por espacio:

| Enfoque | Tiempo | Espacio |
|---|---|---|
| Brute force (re-calcular todo) | O(n²) | O(1) |
| Pre-computar con HashMap | O(n) | O(n) |
| Pre-computar con Prefix Sum | O(n) | O(n) |

**Ejemplo:** Quieres saber la suma de cada subarray.

- **Brute force:** Para cada subarray, recorres todos los elementos → O(n²)
- **Prefix Sum:** Pre-calculas las sumas acumuladas → O(n) pero usas O(n) de espacio extra

**Regla general:** Si las constraints de memoria son amplias (típico en entrevistas), prioriza tiempo.

---

## C.8 Complejidad de cada estructura de datos

| Estructura | Acceso | Búsqueda | Inserción | Eliminación |
|---|---|---|---|---|
| **List (Array)** | O(1) por índice | O(n) | O(1) amortizado (final), O(n) (medio) | O(n) (medio) |
| **Set** | — | O(1) | O(1) | O(1) |
| **Map (HashMap)** | O(1) por key | O(1) | O(1) | O(1) |
| **Queue** | O(1) primero | O(n) | O(1) addLast | O(1) removeFirst |
| **PriorityQueue (Heap)** | O(1) min/max | O(n) | O(log n) | O(log n) |

**¿Qué significa esto para ti?** Si necesitas buscar algo repetidamente, usa **Set** o **Map** (O(1)) en vez de **List** (O(n)).

---

## Checklist antes de codificar

```
□ ¿Cuál es el tamaño máximo de n?
□ ¿Qué complejidad necesito según la tabla?
□ ¿Mi enfoque cumple esa complejidad?
□ ¿Puedo usar un Map/Set para hacer búsquedas O(1)?
□ ¿Necesito pre-computar algo?
□ ¿Cuánto espacio extra uso?
```

---

## Mini-ejercicio: ¿Entiendes Big-O?

Responde mentalmente:

1. **Tienes un array de 1000 elementos. Recorres el array una vez. ¿Qué complejidad es?**
   → O(n) — un solo recorrido lineal.

2. **Tienes dos loops anidados, cada uno recorre todo el array de 1000 elementos. ¿Cuántas operaciones?**
   → O(n²) = 1000 × 1000 = 1,000,000. Sí cabe (0.01s). Pero si n=10⁵, serían 10¹⁰ = 100 segundos. No cabe.

3. **Tienes un array ordenado. Divides el array por la mitad en cada paso. ¿Qué complejidad es?**
   → O(log n). Con 1000 elementos, solo ~10 pasos.

Si acertaste las 3, entiendes lo básico.
