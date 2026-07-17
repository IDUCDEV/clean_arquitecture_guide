# 06 — Comunicación y Pseudocódigo

> Resolver el problema es la mitad. Comunicar tu solución claramente es la otra mitad — especialmente en entrevistas técnicas.

---

## Por qué importa la comunicación

En una entrevista técnica, el interviewer no solo evalúa si tu código funciona. Evalúa:

1. **¿Entiendes el problema?** — ¿Preguntas de clarificación?
2. **¿Puedes comunicar tu approach?** — ¿Explicas antes de codificar?
3. **¿Manejas edge cases?** — ¿Piensas en casos extremos?
4. **¿Tu código es limpio?** — ¿Nombres claros, estructura lógica?

---

## Estructura de Presentación (5 minutos)

```
1. REFORMULAR (30 seg)
   "Entiendo que me pides [reformulación del problema]."

2. ANALIZAR CONSTRAINTS (30 seg)
   "El input puede tener hasta n=[valor], así que necesito [complejidad]."

3. Mencionar brute force (30 seg)
   "El approach más obvio sería [brute force] con complejidad [O(?)].
    Pero eso es demasiado lento porque [razón]."

4. Presentar el approach óptimo (1 min)
   "Puedo mejorar esto usando [patrón/estructura]. La idea es [explicación en 2 oraciones]."

5. Pseudocódigo (2 min)
   [Escribir pseudocódigo en la pizarra o en voz alta]
```

---

## Cómo Escribir Pseudocódigo Limpio

### Reglas

1. **Un paso por línea.** No metas lógica compleja en una línea.
2. **Usa nombres descriptivos.** `queue`, `visited`, `windowSum` — no `q`, `v`, `s`.
3. **Indentación para bloques.** While, for, if deben estar indentados.
4. **Comentarios para la lógica clave.** No para obviedades.
5. **Separa datos de lógica.** Primero la inicialización, luego el loop.

### Ejemplo malo

```
while q not empty:
  x y d = q.pop(); if x==gx and y==gy return d; for dx dy in dirs: nx = x+dx... if valid add q
```

### Ejemplo bueno

```
BFS(grid, start, goal):
  1. Cola = [(startX, startY, 0)]
  2. Visited = {(startX, startY)}

  3. Mientras cola no esté vacía:
     a. Extraer (x, y, pasos) de la cola
     b. Si (x, y) == goal, retornar pasos
     c. Para cada dirección (arriba, abajo, izq, der):
        i.   nx, ny = siguiente celda en esa dirección
        ii.  Mientras nx,ny sea válida y no visitada:
             - Marcar visitada
             - Agregar a cola con pasos + 1

  4. Retornar -1 (no hay camino)
```

---

## Comunicación Durante la Implementación

Mientras codificas, narra lo que haces:

```dart
// "Voy a crear un HashMap para trackear los elementos que ya vi"
Map<int, int> seen = {};

// "Itero sobre el array una sola vez — O(n)"
for (int i = 0; i < arr.length; i++) {

  // "Calculo el complemento — esto es lo que necesito para sumar al target"
  int complement = target - arr[i];

  // "Si el complemento ya está en el map, encontré la respuesta"
  if (seen.containsKey(complement)) {
    return [seen[complement]!, i];
  }

  // "Si no, guardo el elemento actual con su índice"
  seen[arr[i]] = i;
}
```

---

## El Mantra de la Entrevista

Antes de empezar a codificar, di:

> "Elegí **[patrón]** porque **[señal del enunciado]**,
> la complejidad es **[O(?)] tiempo, O(?) espacio**,
> los edge cases son **[casos]**,
> las alternativas que consideré fueron **[por qué no otras]**."

### Ejemplo completo

> "Elegí **BFS** porque el problema pide **camino mínimo en un grid sin pesos de movimiento**,
> la complejidad es **O(N²) tiempo, O(N²) espacio**,
> los edge cases son **grid 1×1, start == goal, todo bloqueado**,
> las alternativas que consideré fueron **DFS (no garantiza mínimo) y Dijkstra (sobredimensionado para sin pesos)**."

---

## Después de Codificar: Verificación

Siempre termina con:

1. **Testear con el ejemplo del enunciado** — traza el código paso a paso
2. **Mencionar edge cases** — "Esto maneja el caso donde [edge case] porque [razón]"
3. **Decir la complejidad final** — "Esta solución es O([complejidad]) en tiempo y O([complejidad]) en espacio"

---

## Errores Comunes de Comunicación

| Error | Cómo evitarlo |
|---|---|
| Codificar en silencio | Narra cada paso mientras escribes |
| No preguntar antes de empezar | "¿Puedo asumir que [asunción]?" |
| Brute force sin mencionar optimización | Siempre menciona el brute force primero |
| No validar con el interviewer | "¿Tiene sentido este approach hasta ahora?" |
| Olvidar edge cases | Menciona al menos 2 edge cases antes de codificar |
| No decir la complejidad | Siempre termina con "La complejidad es O(?)" |
