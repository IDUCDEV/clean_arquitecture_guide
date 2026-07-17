# 01 — Metodología General: Framework de 6 Pasos

> Antes de escribir una sola línea de código, sigue estos 6 pasos en orden. Saltar cualquiera de ellos es la causa #1 de soluciones incorrectas o lentas.

---

## El Framework

```
┌─────────────────────────────────────────────────────┐
│  PASO 1: Entender el Problema                       │
│  "¿Qué me piden? ¿Qué me dan?"                     │
├─────────────────────────────────────────────────────┤
│  PASO 2: Analizar Constraints                       │
│  "¿Qué complejidad necesito?"                       │
├─────────────────────────────────────────────────────┤
│  PASO 3: Explorar Ejemplos y Edge Cases              │
│  "¿Qué pasa con casos extremos?"                    │
├─────────────────────────────────────────────────────┤
│  PASO 4: Identificar el Patrón                      │
│  "¿Qué algoritmo/estructura encaja aquí?"           │
├─────────────────────────────────────────────────────┤
│  PASO 5: Escribir Pseudocódigo                      │
│  "¿Puedo explicar la lógica en palabras?"            │
├─────────────────────────────────────────────────────┤
│  PASO 6: Implementar, Testear y Optimizar            │
│  "¿Funciona? ¿Es eficiente?"                        │
└─────────────────────────────────────────────────────┘
```

---

## PASO 1: Entender el Problema

Lee el enunciado **dos veces**. No asumas nada. Responde estas preguntas:

1. **¿Cuál es la entrada?** (¿array? ¿string? ¿grafo? ¿grid? ¿número?)
2. **¿Cuál es la salida esperada?** (¿un número? ¿un booleano? ¿una lista? ¿un índice?)
3. **¿Qué significa exactamente cada término?** (Si dice "movimiento", define qué es un movimiento)
4. **¿Hay restricciones implícitas?** (¿circular? ¿orden importa? ¿puede haber negativos?)

**Truco:** Reformula el problema con tus propias palabras. Si no puedes explicarlo simple, no lo entiendes.

---

## PASO 2: Analizar Constraints

Las constraints son la **señal más fuerte** para elegir algoritmo. Lées **antes** de pensar en la solución.

| Si las constraints dicen... | Entonces la complejidad debe ser... |
|---|---|
| `n ≤ 10` | O(n!) o O(2ⁿ) — brute force, backtracking |
| `n ≤ 20` | O(2ⁿ · n) — bitmask DP, backtracking podado |
| `n ≤ 400` | O(n³) — Floyd-Warshall, DP con dimensión extra |
| `n ≤ 5.000` | O(n²) — dos loops anidados, DP cuadrático |
| `n ≤ 10⁵` | O(n log n) — sorting, binary search, heap |
| `n ≤ 10⁶` | O(n) — two pointers, sliding window, hashing |
| `n ≤ 10¹⁸` | O(log n) o O(1) — binary search sobre respuesta, fórmula matemática |

**La regla de los 10⁸:** Un ordenador moderno ejecuta ~10⁸ operaciones por segundo. Si tu algoritmo hará 10¹⁰ operaciones, será demasiado lento para un time limit de 1 segundo.

---

## PASO 3: Explorar Ejemplos y Edge Cases

Antes de diseñar el algoritmo, trabaja **a mano** al menos 3 ejemplos:

1. **Caso normal** — el ejemplo del enunciado
2. **Edge case** — input vacío, un solo elemento, todos iguales
3. **Caso tricky** — negativos, duplicados, valores extremos

### Edge Cases más comunes

| Tipo de input | Edge cases a verificar |
|---|---|
| Array/String | Vacío, un elemento, todos iguales, todos negativos |
| Número | 0, 1, negativo, overflow |
| Árbol | Vacío, un nodo, degenerado (lineal), completo |
| Grafo | Sin aristas, todos conectados, ciclos |
| Grid | 1×1, todo bloqueado, todo abierto |

---

## PASO 4: Identificar el Patrón

Este es el paso **más importante**. No intentes inventar un algoritmo desde cero. Usa el reconocimiento de patrones (detallado en [03-reconocimiento-patrones.md](./03-reconocimiento-patrones.md)).

### Preguntas guía

1. **¿Cuál es el tipo de input?** → Array, String, Graph, Tree, Grid, etc.
2. **¿Qué me piden?** → ¿Min/max? ¿Todos los resultados? ¿Sí/no? ¿Un camino?
3. **¿Qué keywords aparecen?** → "contiguo", "mínimo pasos", "par", "ciclo", "k-ésimo"

Si puedes nombrar el patrón antes de codificar, ya tienes la mitad de la solución.

---

## PASO 5: Escribir Pseudocódigo

Nunca saltes directamente al código. Escribe pseudocódigo primero. Esto te permite:

- Validar la lógica **sin** lidiar con sintaxis
- Detectar errores lógicos antes de implementar
- Comunicar tu idea a otros (entrevista, code review)

### Ejemplo de pseudocódigo

```
PROBLEMA: Encontrar el mínimo número de pasos en un grid

PATRÓN: BFS (camino mínimo en grafo no ponderado)

1. Cola = [(startX, startY, 0)]
2. Visited = {(startX, startY)}
3. Mientras cola no esté vacía:
   a. Extraer (x, y, pasos) de la cola
   b. Si (x, y) == goal, retornar pasos
   c. Para cada dirección (arriba, abajo, izquierda, derecha):
      - Mientras la celda siguiente sea válida y no visitada:
        - Marcar como visitada
        - Agregar a la cola con pasos + 1
4. Retornar -1 (no hay camino)
```

---

## PASO 6: Implementar, Testear y Optimizar

### Implementar
- Usa nombres de variables descriptivos
- Maneja edge cases primero (early returns)
- Usa la estructura de datos correcta

### Testear (mínimo 3 casos)
1. **Happy path** — el caso normal del enunciado
2. **Edge case** — input vacío, un elemento
3. **Stress case** — input grande mental para validar complejidad

### Optimizar
Pregúntate: "¿Puedo hacer mejor?" Solo si el brute force es correcto pero lento, busca la optimización.

---

## Resumen del Framework

```
Entender → Constraints → Ejemplos → Patrón → Pseudocódigo → Código

NO hagas:
✗ Codificar sin entender el problema
✗ Ignorar las constraints
✗ Probar solo el caso happy path
✗ Adivinar el patrón sin analizar señales
✗ Saltar del enunciado al código directamente
```

---

## Ejemplo rápido: Two Sum

**Problema:** Dado un array de enteros y un target, encontrar dos índices cuya suma sea igual al target.

**Paso 1:** Entrada: array + target. Salida: dos índices.

**Paso 2:** n ≤ 10⁴ → necesitamos O(n) o O(n log n).

**Paso 3:** Edge cases: array de 2 elementos, todos iguales, negativos.

**Paso 4:** "Par que suma X" + n ≤ 10⁴ → **HashMap** (complemento en O(1)).

**Paso 5:**
```
1. HashMap = {}
2. Para cada (i, num) en array:
   a. complemento = target - num
   b. Si complemento en HashMap, retornar [HashMap[complemento], i]
   c. HashMap[num] = i
3. Retornar []
```

**Paso 6:** Implementar, testear con [2,7,11,15] target=9 → [0,1] ✓
