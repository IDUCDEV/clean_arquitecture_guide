# 02 — Cómo analizar la complejidad de un problema

> Cuando ves un problema en HackerRank, LeetCode o similar, necesitas saber si tu solución es **rápida antes de escribirla**. Esta guía te enseña el proceso completo, paso a paso, con ejemplos reales.

---

# PARTE 0: Big-O desde cero (para principiantes absolutos)

Si nunca has escuchado de "Big-O" o "complejidad algorítmica", empieza aquí. Esta sección explica todo desde el principio.

## ¿Qué es Big-O?

**Big-O** es una forma de medir **qué tan rápido crece** el tiempo de ejecución de un algoritmo cuando aumentan los datos de entrada.

No es una fórmula matemática complicated — es una **clasificación** que nos dice:
- Si un algoritmo es **rápido** (funciona con muchos datos)
- Si un algoritmo es **lento** (solo funciona con pocos datos)

## La analogía del supermercado

Imagina que estás en la fila del supermercado:

| Situación | Tiempo que toma | Tipo de complejidad |
|-----------|-----------------|---------------------|
| **Caja rápida** (1 persona atendiendo) | 1 minuto por cliente | O(n) - lineal |
| **Caja lenta** (la persona busca todo lentamente) | 10 minutos por cliente | O(n) pero con constante grande |
| **Caja automática** (máquina nueva) | 30 segundos por cliente | O(1) - constante |
| **Problema**: si hay 100 personas... | La caja lenta tarda 1000 minutos | ¡16 horas! |

**Big-O nos ayuda a predecir** qué pasará cuando haya MUCHOS datos.

## ¿Por qué importa?

**Ejemplo real:**
- Tu solución funciona con 10 números ✓
- El problema tiene 100,000 números
- Si tu solución es **lenta**, recibes "Time Limit Exceeded"
- **Pierdes tiempo** porque no analizaste antes

## Las 4 complejidades principales (explicadas simple)

### 1. O(1) — Constante: "Siempre lo mismo"
**Ejemplo:** Buscar tu nombre en la guía telefónica si sabes que empieza con "M" → vas directo a esa sección.

**En código:** Acceder al primer elemento de un array: `arr[0]`

**Cuándo la ves:** Operaciones que **no dependen del tamaño** de los datos.

### 2. O(n) — Lineal: "Uno por uno"
**Ejemplo:** Revisar una lista de tareas completadas → lees cada tarea una por una.

**En código:** 
```dart
for (int i = 0; i < n; i++) {
  // algo con cada elemento
}
```

**Cuándo la ves:** Cuando recorres **todos los elementos una vez**.

### 3. O(n²) — Cuadrático: "Comparar cada cosa con cada cosa"
**Ejemplo:** Comparar cada libro de una estantería con todos los demás para ver si hay duplicados.

**En código:**
```dart
for (int i = 0; i < n; i++) {
  for (int j = 0; j < n; j++) {
    // comparar i con j
  }
}
```

**Cuándo la ves:** Cuando tienes **dos loops anidados** que recorren los mismos datos.

### 4. O(log n) — Logarítmica: "Dividir por la mitad"
**Ejemplo:** Buscar una palabra en el diccionario: abres por la mitad, decides izquierda o derecha, repites.

**En código:**
```dart
while (n > 1) {
  n = n ~/ 2;  // Divides por 2 en cada paso
}
```

**Cuándo la ves:** Cuando en cada paso **descartas la mitad** de los datos.

## Tabla resumen para memorizar

| Complejidad | Nombre | Ejemplo cotidiano | ¿Cuándo la ves en código? |
|-------------|--------|-------------------|---------------------------|
| **O(1)** | Constante | Abrir un libro en una página marcada | `arr[0]`, `map[key]` |
| **O(n)** | Lineal | Leer un libro página por página | Un solo `for` que recorre todo |
| **O(n²)** | Cuadrático | Comparar cada página con todas las demás | Dos `for` anidados |
| **O(log n)** | Logarítmica | Buscar en diccionario (mitad por mitad) | `while (n > 1) { n = n ~/ 2; }` |

## La pregunta clave de Big-O

**Cuando ves un código, pregúntate:**
> "Si duplico la cantidad de datos (n), ¿qué pasa con el tiempo?"

| Si duplicas n y el tiempo... | Entonces es... |
|------------------------------|----------------|
| Se duplica | O(n) — lineal |
| Se cuadruplica (4×) | O(n²) — cuadrático |
| Apenas cambia (+1 paso) | O(log n) — logarítmico |
| No cambia | O(1) — constante |

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

**¿Qué es 10⁸?** Es notación científica para **100,000,000** (cien millones).

**¿Por qué importa?** Porque un procesador moderno ejecuta aproximadamente **100 millones de operaciones por segundo**. Si tu algoritmo hace más de eso, será demasiado lento.

**La regla práctica:** Si tu algoritmo hace **menos de 100 millones de operaciones**, funcionará en menos de 1 segundo.

**Ejemplo concreto:**
- Si n = 10,000 (diez mil):
  - O(n) = 10,000 operaciones → **0.0001 segundos** ✓ rápido
  - O(n²) = 100,000,000 operaciones → **1 segundo** ⚠️ justo en el límite
  - O(n³) = 10¹² operaciones → **10,000 segundos** ✗ demasiado lento

**Tabla de referencia (memorízala):**

| Si el problema dice... | Tu algoritmo debe ser... | Operaciones máximas | Tiempo estimado |
|---|---|---|---|
| `n ≤ 10` | Cualquier cosa | 10! = 3.6 millones | 0.03 segundos |
| `n ≤ 100` | O(n³) o mejor | 1,000,000 | 0.01 segundos |
| `n ≤ 5,000` | O(n²) o mejor | 25,000,000 | 0.25 segundos |
| `n ≤ 100,000` | O(n log n) o mejor | 1,700,000 | 0.02 segundos |
| `n ≤ 10,000,000` | O(n) | 10,000,000 | 0.1 segundos |

**¿Cómo usar esta tabla?**
1. Mira las constraints del problema (¿cuál es el valor máximo de n?)
2. Busca en la tabla qué complejidad necesitas
3. Diseña tu algoritmo para cumplir esa complejidad

**Ejemplo:**
- Problema dice: `n ≤ 100,000`
- Tabla dice: necesitas O(n log n) o mejor
- Tu algoritmo debe ser O(n log n), O(n), O(log n), o O(1)

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

**¿Cómo analizo la complejidad?** Sigo estos pasos:

**Paso 1: Identificar los loops**
- Este código tiene **dos loops anidados**:
  ```dart
  for (int i = 0; i < n; i++) {         // Loop 1
    for (int j = i + 1; j < n; j++) {   // Loop 2 (dentro del 1)
      // ...
    }
  }
  ```

**Paso 2: Contar iteraciones**
- **Loop 1**: Se ejecuta `n` veces (una por cada elemento)
- **Loop 2**: Para **cada** iteración del Loop 1, se ejecuta hasta `n` veces

**Paso 3: Multiplicar**
- Total de iteraciones = `n × n = n²`

**Paso 4: Ignorar operaciones simples**
- Dentro de los loops: `nums[i] + nums[j]` y `== target` son operaciones simples (O(1))
- No cambian la complejidad

**Conclusión:** **O(n²)** — complejidad cuadrática

### ¿Por qué O(n²)? (explicación visual)

Imagina un array de 4 elementos: `[2, 7, 11, 15]`

**El Loop 1** recorre cada elemento:
- i=0: compara 2 con [7, 11, 15]
- i=1: compara 7 con [11, 15]  
- i=2: compara 11 con [15]
- i=3: no compara con nada

**Total de comparaciones:** 3 + 2 + 1 = 6 = (4 × 3) / 2

**Patrón:** Para n elementos, son aproximadamente `n²/2` comparaciones. En Big-O ignoramos la constante 1/2, así que es **O(n²)**.

**La regla práctica:** Cuando ves `for` + `for` anidados que recorren los mismos datos, es **O(n²)**.

### ¿Cumple con lo que necesito?

- Necesito: O(n) o mejor
- Mi solución: O(n²)
- Con n = 10,000: serían 100,000,000 operaciones = **1 segundo exacto**

**Está justo en el límite.** Podría funcionar, pero es arriesgado. Si el problema tuviera n ≤ 100,000, O(n²) sería 10 mil millones = 100 segundos. No pasaría.

**¿Qué hago?** Optimizo.

---

## PASO 4: Optimizar

**Mi solución actual:** O(n²) — demasiado lento para n = 10,000
**Necesito:** O(n) o mejor

**Pregunta clave:** ¿Cómo puedo encontrar el complemento más rápido?

### El problema del brute force

En el brute force, para cada elemento `nums[i]`, recorro **todo** el array buscando el complemento `target - nums[i]`. Eso es O(n) para cada elemento, y como hay n elementos → O(n²).

### La idea de la optimización

**En vez de buscar el complemento, puedo recordar los valores que ya vi.**

Si estoy en el elemento `7` y necesito un `2` (porque 7 + 2 = 9):
- **Brute force:** Recorro todo el array buscando un 2 → O(n)
- **Optimización:** Pregunto: "¿ya vi un 2 antes?" → O(1)

### ¿Qué es un HashMap (Map en Dart)?

Un **HashMap** es una estructura de datos que guarda pares **llave-valor** y permite buscar por llave en **O(1)** (tiempo constante).

**Analogía:** Es como un diccionario:
- Buscas una palabra (llave) → encuentras su definición (valor) **instantáneamente**
- No necesitas leer el diccionario página por página

**En código Dart:**
```dart
Map<int, int> seen = {};
seen[7] = 0;    // Guardo: valor 7 está en índice 0
seen.containsKey(7);  // → true (búsqueda O(1))
seen[7];        // → 0 (acceso O(1))
```

### La solución optimizada

```dart
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

1. **Un solo loop** que recorre `n` elementos → O(n)
2. **Dentro del loop:**
   - Resta: `target - nums[i]` → O(1)
   - Búsqueda en Map: `seen.containsKey(complemento)` → O(1)
   - Inserción en Map: `seen[nums[i]] = i` → O(1)

**Total:** `n × 3 = 3n` operaciones. Las constantes (3) se ignoran en Big-O.

**Esto es O(n)** — complejidad lineal.

### ¿Por qué es O(n)?

- **Un solo loop** → O(n)
- **Las operaciones dentro del loop son O(1)** → no cambian la complejidad
- **La estructura (HashMap) es clave** → sin ella, la búsqueda sería O(n) y el total sería O(n²)

### Comparación visual

| Enfoque | Código | Complejidad | Con n = 10,000 |
|---|---|---|---|
| Brute force | 2 loops anidados | O(n²) | 100,000,000 ops (1 segundo) |
| HashMap | 1 loop + Map | O(n) | 10,000 ops (0.0001 segundos) |

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

**¿Qué significa esto?**
- `i` y `j` son los días de inicio y fin del rango
- `j ≤ 10⁷` significa que el rango puede tener hasta **10,000,000 de días**
- `k` es el divisor (puede ser hasta 1,000,000,000)

**La parte clave es `j ≤ 10⁷`.** Eso define el tamaño máximo de nuestro problema.

**¿Qué complejidad necesito?**

Usando la tabla de la sección anterior:
- `n ≤ 10,000,000` → necesito **O(n)** o mejor

**Tabla de verificación:**
| Complejidad | Operaciones con n=10⁷ | ¿Cabe? |
|---|---|---|
| O(n) | 10,000,000 | ✓ Sí (0.1 segundos) |
| O(n log n) | 230,000,000 | ⚠️ En el límite (2.3 segundos) |
| O(n²) | 10¹⁴ | ✗ No (10,000 segundos) |

**Conclusión:** Necesito **O(n) o mejor**.

---

### PASO 3: Analizar mi primera idea

**La idea obvia:** Recorrer cada día del rango, calcular si es beautiful, y contar.

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

**Análisis paso a paso:**

1. **¿Cuántos loops hay?** Solo **1 loop** (`for (int day = i; day <= j; day++)`)
2. **¿Cuántas veces se ejecuta?** Desde `i` hasta `j` inclusive
3. **¿Qué es "n" aquí?** n = `j - i + 1` (la cantidad de días en el rango)
   - Ejemplo: si i=20, j=23 → n = 23 - 20 + 1 = 4 días
4. **¿Qué hay dentro del loop?** Operaciones simples:
   - Convertir a string: O(longitud del número) ≈ O(1) para números ≤ 10⁷
   - Invertir string: O(longitud) ≈ O(1)
   - Convertir a número: O(longitud) ≈ O(1)
   - Calcular módulo: O(1)

**Total:** n iteraciones × O(1) por iteración = **O(n)**

**¿Cumple con las constraints?** Sí. Con n = 10⁷, son 10 millones de operaciones. Cabe en menos de 1 segundo.

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

**¿Qué aprendimos de este ejemplo?**

1. **Identificar "n":** En problemas con rangos, n = tamaño del rango (j - i + 1)
2. **Un solo loop = O(n):** Cuando recorres un rango una sola vez, es lineal
3. **No siempre optimizar:** Si O(n) cumple con las constraints, está perfecto
4. **Operaciones simples no cambian la complejidad:** Convertir a string, invertir, módulo → todo O(1) o casi

**Tabla resumen:**

| Concepto | Lo que aprendimos |
|---|---|
| **Un solo loop** | Un `for` que recorre un rango = O(n) |
| **No siempre optimizar** | Si O(n) cumple, no busques algo más complejo |
| **Operaciones dentro del loop** | Si son simples (suma, módulo), no cambian la complejidad |
| **Cómo calcular n** | Para rangos: n = fin - inicio + 1 |

**Patrón para problemas similares:**
Si ves un problema que dice:
- "Recorrer un rango de A a B"
- "Contar números que cumplan una condición"
- "Para cada elemento del array, hacer algo"

Probablemente sea **O(n)** con un solo loop.

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

**Analogía:** 
- Buscar tu nombre en la guía telefónica si sabes que empieza con "M" — vas directo a esa sección.
- Abrir un libro en una página marcada con un post-it.

**En código:**
```dart
int obtenerPrimero(List<int> arr) {
  return arr[0]; // Siempre 1 operación, sin importar el tamaño
}
```

**Ejemplos cotidianos:**
- Acceder al primer elemento de un array: `arr[0]`
- Buscar en un HashMap: `map[key]`
- Sumar dos números: `a + b`

**Cuándo la ves:** Operaciones que **no dependen del tamaño** de los datos.

---

### O(n) — Lineal

**Qué significa:** El tiempo crece **en la misma proporción** que los datos.

**Analogía:** 
- Revisar un listado completo de tareas — lees cada tarea una por una.
- Leer un libro página por página.

**En código:**
```dart
int sumarTodo(List<int> arr) {
  int total = 0;
  for (int x in arr) {   // Recorre cada elemento una vez
    total += x;
  }
  return total;
}
```

**Ejemplos numéricos:**
- 10 datos → 10 operaciones
- 100 datos → 100 operaciones
- 1,000 datos → 1,000 operaciones

**Cuándo la ves:** Recorrer un array, contar frecuencias, buscar en lista no ordenada.

---

### O(n²) — Cuadrático

**Qué significa:** El tiempo crece **al cuadrado** de los datos.

**Analogía:** 
- Comparar cada libro de una estantería con todos los demás.
- En una clase, que cada alumno compare su cuaderno con el de todos los demás.

**En código:**
```dart
bool tieneDuplicados(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {
    for (int j = i + 1; j < arr.length; j++) {  // Para cada i, recorre todo lo que queda
      if (arr[i] == arr[j]) return true;
    }
  }
  return false;
}
```

**Ejemplos numéricos:**
- 10 datos → ~50 operaciones (10 × 5)
- 100 datos → ~5,000 operaciones (100 × 50)
- 1,000 datos → ~500,000 operaciones

**⚠️ Problema:** Con n = 10,000, ya son 100 millones de operaciones. Con n = 100,000, serían 10 mil millones — demasiado para 1 segundo.

**Revisual:** Cuando ves `for` + `for` anidados que recorren los mismos datos, es O(n²).

---

### O(log n) — Logarítmica

**Qué significa:** El tiempo crece **muy lento**. Cada vez que duplicas los datos, solo necesitas **1 paso más**.

**Analogía:** 
- Buscar una palabra en el diccionario: abres por la mitad, decides si ir a la izquierda o derecha, y repites.
- Adivinar un número entre 1 y 100: preguntas "¿es mayor que 50?" → si es sí, buscas en 51-100; si es no, buscas en 1-49.

**En código:**
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
```

**¿Por qué log n?** Porque `log₂(n)` = "¿cuántas veces tengo que dividir n por 2 para llegar a 1?"

**Tabla de ejemplos:**
| Datos (n) | Pasos necesarios (log₂(n)) |
|-----------|----------------------------|
| 8 | 3 (8 → 4 → 2 → 1) |
| 1,000 | ~10 |
| 1,000,000 | ~20 |
| 1,000,000,000 | ~30 |

**La clave:** Con 1,000,000 de datos, solo necesitas ~20 pasos. ¡Increíblemente eficiente!

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

No necesitas memorizar reglas complejas. Solo necesitas reconocer **3 patrones**. Aquí te enseño cómo identificarlos en código real.

### Patrón 1: Un solo bucle → O(n)

**Cómo reconocerlo:** Un solo `for` o `while` que recorre los datos una vez.

**Ejemplo simple:**
```dart
int sumar(List<int> arr) {
  int total = 0;
  for (int x in arr) {  // ← Un solo loop que recorre todo
    total += x;
  }
  return total;
}
```

**Análisis paso a paso:**
1. **¿Cuántos loops hay?** Solo 1
2. **¿Cuántas veces se ejecuta?** `arr.length` veces (n veces)
3. **¿Qué hay dentro?** Una suma (operación O(1))
4. **Total:** n × 1 = n operaciones → **O(n)**

**Señal para buscar:** `for (cada elemento) → hacer algo`

**Otros ejemplos de O(n):**
- Contar frecuencias de un elemento
- Buscar el máximo/mínimo en un array
- Copiar un array a otro

---

### Patrón 2: Bucles anidados → O(n²)

**Cómo reconocerlo:** Dos `for` o `while` anidados que recorren los mismos datos.

**Ejemplo simple:**
```dart
bool hayDuplicado(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {        // ← Primer loop: n veces
    for (int j = i + 1; j < arr.length; j++) {  // ← Segundo loop: n veces
      if (arr[i] == arr[j]) return true;
    }
  }
  return false;
}
```

**Análisis paso a paso:**
1. **¿Cuántos loops hay?** 2 (anidados)
2. **¿Cuántas veces se ejecuta cada uno?** Ambos n veces
3. **Total:** n × n = n² operaciones → **O(n²)**

**Señal para buscar:** `for (cada elemento) { for (cada otro elemento) }`

**¿Por qué es n²?** Porque para cada elemento del array, recorres **todos** los demás.

**Variante importante:** Si el segundo loop empieza en `i` (no en 0), sigue siendo O(n²). Big-O ignora constantes como 1/2.

**Otros ejemplos de O(n²):**
- Encontrar todos los pares de un array
- Ordenar con bubble sort
- Comparar cada elemento con todos los demás

---

### Patrón 3: Dividir por la mitad → O(log n)

**Cómo reconocerlo:** Un `while` que en cada paso divide el espacio de búsqueda por 2.

**Ejemplo simple:**
```dart
int busquedaBinaria(List<int> arr, int target) {
  int left = 0, right = arr.length - 1;

  while (left <= right) {  // ← Se ejecuta log₂(n) veces
    int mid = left + (right - left) ~/ 2;  // Divides por la mitad
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) left = mid + 1;
    else right = mid - 1;
  }
  return -1;
}
```

**Análisis paso a paso:**
1. **¿Qué hace el loop?** Divide el rango por 2 en cada paso
2. **¿Cuántas veces se ejecuta?** Hasta que left > right
3. **¿Cuántos pasos para n elementos?** log₂(n) veces
4. **Total:** log₂(n) operaciones → **O(log n)**

**Señal para buscar:** `while (n > 1) { n = n ~/ 2; }`

**Pregunta clave:** "¿En cada paso, descarto la mitad de los datos?" Si es sí, es O(log n).

**Tabla de ejemplos:**
| Datos (n) | Pasos (log₂(n)) |
|-----------|----------------|
| 16 | 4 (16 → 8 → 4 → 2 → 1) |
| 1,000 | ~10 |
| 1,000,000 | ~20 |

### ¿Cómo identificar el patrón en código nuevo?

**Paso 1:** Busca `for` o `while` en el código
**Paso 2:** Cuenta cuántos hay y si están anidados
**Paso 3:** Pregúntate:
- Si hay **1 loop** → probablemente O(n)
- Si hay **2 loops anidados** → probablemente O(n²)
- Si hay **un while que divide por 2** → probablemente O(log n)

**Ejercicio rápido:** ¿Qué complejidad tiene este código?
```dart
for (int i = 0; i < n; i++) {
  print(arr[i]);
}
for (int j = 0; j < n; j++) {
  print(arr[j]);
}
```
**Respuesta:** O(n) + O(n) = O(n) — son dos loops secuenciales, no anidados.

---

## C.5 Reglas de combinación

En la vida real, los algoritmos combinan patrones. Aquí tienes las reglas para combinar complejidades.

### Regla 1: Operaciones secuenciales → toma la MÁS GRANDE

**Cuándo la ves:** Cuando tienes dos o más partes de código que se ejecutan una después de otra (no anidadas).

**Ejemplo:**
```dart
void ejemplo(List<int> arr) {
  // Parte 1: O(n) — un solo loop
  for (int x in arr) {
    print(x);
  }

  // Parte 2: O(n²) — dos loops anidados
  for (int i = 0; i < arr.length; i++)
    for (int j = 0; j < arr.length; j++) {
      print(arr[i] + arr[j]);
    }
}
```

**Análisis:**
1. Parte 1: O(n)
2. Parte 2: O(n²)
3. **Total:** O(n) + O(n²) = **O(n²)** — la parte más lenta domina

**¿Por qué?** Porque O(n²) es mucho más lento que O(n). Cuando n crece, O(n²) domina el tiempo total.

**Analogía:** Si vas al supermercado y tardas 10 minutos en comprar + 1 hora en cocinar, el tiempo total es ~1 hora (el paso más lento domina).

### Regla 2: Bucles anidados → se multiplican

**Cuándo la ves:** Cuando un loop está dentro de otro y dependen de tamaños diferentes.

**Ejemplo:**
```dart
for (int i = 0; i < n; i++)      // n veces
  for (int j = 0; j < m; j++)    // m veces
    print(i + j);
```

**Análisis:**
1. Primer loop: n veces
2. Segundo loop: m veces
3. **Total:** O(n × m)

**Caso especial:** Si n = m (ambos son el mismo tamaño), entonces O(n × n) = O(n²).

### Ejemplos prácticos

**Ejemplo 1: ¿Qué complejidad tiene?**
```dart
void ejemplo1(List<int> arr1, List<int> arr2) {
  for (int x in arr1) {  // O(n) donde n = arr1.length
    print(x);
  }
  for (int y in arr2) {  // O(m) donde m = arr2.length
    print(y);
  }
}
```
**Respuesta:** O(n) + O(m) = O(n + m)

**Ejemplo 2: ¿Qué complejidad tiene?**
```dart
void ejemplo2(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {
    for (int j = 0; j < arr.length; j++) {
      print(arr[i] + arr[j]);
    }
  }
  print("Terminado");
}
```
**Respuesta:** O(n²) + O(1) = O(n²)

### Resumen de reglas

| Situación | Regla | Ejemplo |
|-----------|-------|---------|
| **Secuencial** (uno tras otro) | Toma la MÁS GRANDE | O(n) + O(n²) = O(n²) |
| **Anidado** (uno dentro del otro) | Se MULTIPLICAN | O(n) × O(m) = O(n × m) |
| **Constante dentro de loop** | No cambia | O(n) × O(1) = O(n) |

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

---

# PARTE D: Preguntas frecuentes de principiantes

Si eres nuevo en Big-O, probablemente tengas algunas de estas preguntas. Aquí las respondo de forma simple.

## P1: ¿Qué es exactamente Big-O?

**Big-O** es una **clasificación** que nos dice cómo crece el tiempo de ejecución de un algoritmo cuando aumentan los datos.

No es una fórmula matemática complicated — es como una **etiqueta** que pones a tu código:
- "Este código es O(n)" = crece linealmente
- "Este código es O(n²)" = crece exponencialmente

**Analogía:** Es como clasificar carros por velocidad:
- "Este carro va a 100 km/h" (rápido)
- "Este carro va a 50 km/h" (lento)

## P2: ¿Por qué se ignoran las constantes?

**Ejemplo:**
- Código A: `3n` operaciones
- Código B: `100n` operaciones

**¿Cuál es más rápido?** Código A (3n < 100n)

**¿Pero en Big-O?** Ambos son **O(n)**

**¿Por qué?** Porque cuando n crece mucho (ej: 1,000,000), la constante (3 vs 100) no importa tanto como el **patrón de crecimiento**.

| n | 3n | 100n | Diferencia |
|---|-----|------|------------|
| 10 | 30 | 1,000 | 33× |
| 1,000 | 3,000 | 100,000 | 33× |
| 1,000,000 | 3,000,000 | 100,000,000 | 33× |

**La diferencia siempre es 33×**, pero ambos crecen **linealmente**. Por eso decimos que ambos son O(n).

## P3: ¿Cómo sé qué es "n" en un problema?

**Regla simple:** "n" es generalmente el **tamaño del input principal**.

**Ejemplos:**
- Array de 100 elementos → n = 100
- String de 50 caracteres → n = 50
- Rango de días de 20 a 23 → n = 23 - 20 + 1 = 4

**En problemas de HackerRank:** Las constraints te dicen cuál es n:
```
1 ≤ n ≤ 10⁵  →  n es el tamaño del array
```

## P4: ¿Qué pasa si tengo múltiples inputs con tamaños diferentes?

**Ejemplo:**
```dart
void ejemplo(List<int> arr1, List<int> arr2) {
  for (int x in arr1) { ... }  // O(n) donde n = arr1.length
  for (int y in arr2) { ... }  // O(m) donde m = arr2.length
}
```

**Complejidad total:** O(n + m)

**Regla:** Si los inputs son independientes, usa letras diferentes (n, m, p, etc.)

## P5: ¿O(n²) es siempre malo?

**No siempre.** Depende de las constraints.

| Si n es... | O(n²) es... | Ejemplo |
|------------|-------------|---------|
| 10 | 100 ops → **aceptable** | Problemas pequeños |
| 100 | 10,000 ops → **aceptable** | Problemas medianos |
| 1,000 | 1,000,000 ops → **aceptable** | Problemas grandes |
| 10,000 | 100,000,000 ops → **límite** | ¡Cuidado! |
| 100,000 | 10,000,000,000 ops → **malo** | Time Limit Exceeded |

**Conclusión:** O(n²) puede ser aceptable si n es pequeño.

## P6: ¿Cómo mejoro de O(n²) a O(n)?

**Técnica común:** Usar **HashMap** (Map en Dart) para búsquedas O(1).

**Antes (O(n²)):**
```dart
for (int i = 0; i < n; i++) {
  for (int j = 0; j < n; j++) {  // Búsqueda O(n)
    if (arr[i] + arr[j] == target) return [i, j];
  }
}
```

**Después (O(n)):**
```dart
Map<int, int> seen = {};
for (int i = 0; i < n; i++) {
  int complemento = target - arr[i];
  if (seen.containsKey(complemento)) return [seen[complemento]!, i];  // Búsqueda O(1)
  seen[arr[i]] = i;
}
```

**La clave:** El HashMap convierte una búsqueda O(n) en O(1).

## P7: ¿Qué es la complejidad espacial?

**Complejidad temporal:** Cuánto **tiempo** tarda tu algoritmo.
**Complejidad espacial:** Cuánta **memoria** usa tu algoritmo.

**Ejemplo:**
```dart
// O(n) espacio — crea un array nuevo
List<int> duplicar(List<int> arr) {
  List<int> nuevo = [];
  for (int x in arr) {
    nuevo.add(x * 2);
  }
  return nuevo;
}

// O(1) espacio — modifica el array original
void duplicarEnLugar(List<int> arr) {
  for (int i = 0; i < arr.length; i++) {
    arr[i] *= 2;
  }
}
```

**¿Cuándo importa?** Cuando el input es muy grande y la memoria es limitada.

## P8: ¿Cómo practico para entender mejor Big-O?

**Ejercicio diario:**
1. Toma un código que escribiste
2. Pregúntate: "¿Cuántos loops hay? ¿Están anidados?"
3. Clasifica: O(1), O(n), O(n²), o O(log n)
4. Verifica con restricciones del problema

**Recursos para practicar:**
- HackerRank (sección "Algorithms")
- LeetCode (problemas "Easy")
- Exercism (tracks de Dart/Flutter)

## P9: ¿Big-O es lo mismo que "eficiencia"?

**No exactamente.** Big-O mide **crecimiento**, no eficiencia absoluta.

**Ejemplo:**
- Algoritmo A: O(n²) pero con operaciones simples
- Algoritmo B: O(n) pero con operaciones complejas

**Para n pequeño:** Algoritmo A podría ser más rápido
**Para n grande:** Algoritmo B será más rápido

**Regla práctica:** Primero optimiza la complejidad (Big-O), luego optimiza las constantes.

## P10: ¿Qué hago si no sé la complejidad de mi código?

**Sigue estos pasos:**
1. **Cuenta los loops** (¿cuántos hay? ¿están anidados?)
2. **Identifica operaciones costosas** (búsquedas en arrays, recursión)
3. **Usa los patrones** de la sección C.4
4. **Compara con restricciones** del problema

**Si todavía no sabes:** Ejecuta tu código con inputs de diferentes tamaños y mide el tiempo. Si el tiempo se duplica cuando n se duplica → O(n). Si se cuadruplica → O(n²).
