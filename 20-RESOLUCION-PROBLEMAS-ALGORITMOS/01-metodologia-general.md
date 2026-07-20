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

La regla clave: un ordenador ejecuta ~10⁸ operaciones por segundo. Si tu algoritmo hará más de eso, será demasiado lento.

**Tabla completa de constraints → complejidad:** Ver [02-analisis-complejidad.md](./02-analisis-complejidad.md#regla-práctica-qué-complejidad-necesito).

**En resumen:**
- `n ≤ 10` → backtracking completo
- `n ≤ 5.000` → dos loops anidados (O(n²))
- `n ≤ 10⁵` → sorting o binary search (O(n log n))
- `n ≤ 10⁶` → un solo recorrido (O(n))

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
PROBLEMA: Validar que los paréntesis están balanceados

PATRÓN: Stack (LIFO) — el último abierto debe ser el primero en cerrarse

1. Crear un stack vacío
2. Para cada carácter en el string:
   a. Si es '(' o '[', agregar al stack
   b. Si es ')' o ']', verificar que el stack no esté vacío
      - Si está vacío → retorno false (cerrar sin abrir)
      - Si el tope del stack no coincide → retorno false
      - Si coincide → sacar del stack
3. Si el stack está vacío → retorno true (todo balanceado)
   Si no → retorno false (quedaron abiertos sin cerrar)
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

## Ejemplo rápido: Valid Parentheses

**Problema:** Dado un string con solo `(`, `)`, `{`, `}`, `[` y `]`, determinar si los paréntesis están balanceados.

**Paso 1:** Entrada: string de paréntesis. Salida: booleano.

**Paso 2:** n ≤ 10⁴ → necesitamos O(n). Un solo recorrido es suficiente.

**Paso 3:** Edge cases: string vacío → true, solo un carácter → false, `((` → false.

**Paso 4:** "Paréntesis balanceados" + "el último abierto debe ser el primero en cerrar" → **Stack** (LIFO).

**Paso 5:**
```
1. Stack = []
2. Para cada char en el string:
   a. Si es apertura '(', '{', '[' → agregar al stack
   b. Si es cierre ')', '}', ']':
      - Si stack vacío → return false
      - Si tope del stack no coincide → return false
      - Si coincide → sacar del stack
3. Return stack.isEmpty
```

**Paso 6:** Implementar, testear con "(]" → false ✓, "([])" → true ✓
