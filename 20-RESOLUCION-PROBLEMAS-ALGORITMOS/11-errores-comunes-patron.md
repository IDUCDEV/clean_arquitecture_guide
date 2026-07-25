# 11: Errores Comunes al Resolver Problemas

> Patrones de error que comete todo el mundo. Conocerlos te ayuda a detectarlos en tiempo real.

---

## Errores por fase del proceso

### Fase 1: Entender el problema

| Error | Ejemplo | Solución |
|-------|---------|----------|
| No leer todo el enunciado | Ignorar restricciones de O(1) espacio | Leer 2 veces, subrayar restricciones |
| Asumir sin preguntar | "¿Puede haber duplicados?" → no pregunta | Siempre preguntar edge cases |
| Confundir 输入/输出 | Retornar índices cuando piden valores | Releer: ¿qué debe retornar? |

### Fase 2: Elegir approach

| Error | Ejemplo | Solución |
|-------|---------|----------|
| Brute force sin pensar | Probar todas las permutaciones O(n!) | Buscar patrón primero |
| Over-engineering | Usar DP cuando con sorting basta | Empezar por la solución más simple |
| Ignorar restricciones | O(n²) cuando dice O(n log n) | Ver límites antes de diseñar |

### Fase 3: Implementar

| Error | Ejemplo | Solución |
|-------|---------|----------|
| Off-by-one | `i <= n` vs `i < n` | Dibujar el caso base en papel |
| Índices inválidos | `array[array.length]` | Verificar bounds antes de acceder |
| Olvidar edge cases | Input vacío, null, un solo elemento | Testear: vacío, 1 elemento, 2 elementos |
| Mutar sin restaurar | No deshacer en backtracking | Siempre `deshacer()` después de recursión |

### Fase 4: Verificar

| Error | Ejemplo | Solución |
|-------|---------|----------|
| No probar con ejemplos | Solo mirar el código | Ejecutar mentalmente con el ejemplo dado |
| No verificar edge cases | Solo probar el caso feliz | Probar: vacío, 1 elemento, máximo |
| Asumir que funciona | "Se ve bien" | Dry run paso a paso |

---

## Errores por tipo de problema

### Arrays/Strings

```dart
// ❌ Error: No verificar si está vacío
int firstElement(List<int> arr) => arr[0]; // Crash si vacío

// ✅ Correcto
int? firstElement(List<int> arr) => arr.isEmpty ? null : arr[0];
```

### Hash Maps

```dart
// ❌ Error: No verificar si existe la key
int value = map[key]!; // Crash si no existe

// ✅ Correcto
int? value = map[key]; // Null si no existe
```

### Recursión

```dart
// ❌ Error: Caso base incorrecto
int factorial(int n) => n * factorial(n - 1); // Infinito

// ✅ Correcto
int factorial(int n) {
  if (n <= 1) return 1; // Caso base
  return n * factorial(n - 1);
}
```

### Backtracking

```dart
// ❌ Error: No deshacer
void backtrack(List<int> actual, int i) {
  actual.add(i);        // Avanzar
  backtrack(actual, i + 1);
  // Falta: actual.removeLast()
}

// ✅ Correcto
void backtrack(List<int> actual, int i) {
  actual.add(i);        // Avanzar
  backtrack(actual, i + 1);
  actual.removeLast();  // ← DESHACER
}
```

---

## Checklist de verificación

Antes de decir "estoy listo":

```
□ ¿Leí TODAS las restricciones?
□ ¿Probé con el ejemplo del enunciado?
□ ¿Probé edge cases? (vacío, 1 elem, null)
□ ¿La complejidad cumple el requisito?
□ ¿El retorno es correcto? (índices vs valores)
□ ¿El código compila en Dart?
```

---

## Regla de los 3 casos

Siempre prueba tu solución con:

```
1. Caso vacío/null     → ¿No crashea?
2. Caso mínimo (1 elem) → ¿Funciona?
3. Caso normal (ejemplo) → ¿Retorna correcto?
```

---

**Siguiente:** [12-ejercicios-adicionales.md](./12-ejercicios-adicionales.md) - +25 ejercicios para practicar
