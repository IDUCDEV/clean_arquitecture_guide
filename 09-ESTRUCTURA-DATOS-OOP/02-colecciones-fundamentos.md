# 02 — Colecciones en Dart: List, Set, Map

> Las colecciones son los bloques de construcción de la manipulación de datos. Este archivo cubre **todos los constructores, métodos y operaciones** que necesitas.

---

## 🎯 Objetivos

- Conocer todos los constructores de `List`, `Set`, `Map`
- Saber cuándo usar cada tipo de colección
- Operaciones básicas: agregar, eliminar, buscar, ordenar

---

## 1. `List<E>` — La más usada

### Constructores

```dart
// Literal
final lista1 = [1, 2, 3];                    // List<int>, growable

// Vacía
final lista2 = <int>[];                       // growable

// Con tamaño fijo (no growable)
final lista3 = List<int>.filled(3, 0);        // [0, 0, 0]
lista3[0] = 1;                                // ✅ se puede modificar
// lista3.add(4);                              // ❌ RuntimeError: fixed length

// Generada
final lista4 = List<int>.generate(5, (i) => i * 2); // [0, 2, 4, 6, 8]

// Desde otra colección
final lista5 = List<int>.from({1, 2, 3}.toSet());  // [1, 2, 3]

// Unmodifiable (lectura-only, como una snapshot)
final lista6 = List<int>.unmodifiable([1, 2, 3]);
// lista6[0] = 0;                               // ❌ RuntimeError
```

### Operaciones básicas

```dart
final nums = <int>[1, 2, 3];

// Agregar
nums.add(4);               // [1, 2, 3, 4]
nums.addAll([5, 6]);       // [1, 2, 3, 4, 5, 6]
nums.insert(0, 0);         // [0, 1, 2, 3, 4, 5, 6]
nums.insertAll(1, [-1, -2]); // [0, -1, -2, 1, 2, 3, ...]

// Eliminar
nums.remove(0);            // elimina el primer 0
nums.removeAt(0);          // elimina índice 0
nums.removeLast();         // elimina el último
nums.removeWhere((n) => n.isNegative); // elimina negativos

// Buscar
nums.contains(3);          // true
nums.indexOf(3);           // índice 3 (después de agregar)
nums.lastIndexOf(3);
nums.elementAt(2);         // elemento en índice 2

// Obtener subconjuntos
nums.sublist(0, 3);        // primeros 3 elementos
nums.take(3).toList();     // primeros 3
nums.skip(2).toList();     // saltar primeros 2
nums.getRange(0, 3);       // rango [0, 3)
```

### Propiedades importantes

```dart
nums.length;         // cantidad
nums.isEmpty;        // true si vacía
nums.isNotEmpty;     // true si no vacía
nums.first;          // primer elemento (crash si vacía)
nums.last;           // último (crash si vacía)
nums.single;         // único elemento (crash si no exactamente 1)
```

---

## 2. `Set<E>` — Sin duplicados

```dart
// Literal
final frutas = {'manzana', 'pera', 'manzana'}; // {'manzana', 'pera'}

// Constructores
final set1 = <int>{};
final set2 = Set<int>.from([1, 2, 2, 3]);      // {1, 2, 3}
final set3 = Set.identity();                     // usa igualdad por identidad

// Operaciones de conjunto (MUY útiles)
final a = {1, 2, 3};
final b = {3, 4, 5};

a.union(b);             // {1, 2, 3, 4, 5}
a.intersection(b);      // {3}
a.difference(b);        // {1, 2}
a.lookup(2);            // encuentra el elemento (o null)

// ¿Por qué Set en vez de List?
final idsUnicos = [1, 2, 2, 3];   // permite duplicados manual
final idsSet = {1, 2, 2, 3};      // {1, 2, 3} automático
```

> **💡 Regla**: Si necesitas **unicidad**, usa `Set`. Si necesitas **orden + duplicados**, usa `List`.

---

## 3. `Map<K, V>` — Pares clave-valor

```dart
// Literal
final capitales = {'VE': 'Caracas', 'CO': 'Bogotá'};

// Constructores
final map1 = <String, int>{};
final map2 = Map<int, String>.fromIterable(
  [1, 2, 3],
  key: (e) => e,
  value: (e) => 'Item $e',
); // {1: 'Item 1', 2: 'Item 2', 3: 'Item 3'}

final map3 = Map.fromEntries([
  MapEntry('a', 1),
  MapEntry('b', 2),
]);

final map4 = Map.unmodifiable({'x': 10, 'y': 20});
```

### Operaciones esenciales

```dart
final map = <String, int>{'a': 1, 'b': 2};

// Leer
map['a'];               // 1
map['z'];               // null
map.containsKey('a');   // true
map.containsValue(1);   // true

// Escribir
map['c'] = 3;           // agregar/actualizar
map.putIfAbsent('d', () => 4);  // solo si no existe
map.addAll({'e': 5, 'f': 6});
map.update('a', (v) => v + 10);   // actualiza con función
map.update('z', (v) => 1, ifAbsent: () => 0);  // con fallback

// Eliminar
map.remove('a');
map.removeWhere((key, value) => value < 3);

// Iterar
map.keys;       // Iterable<String>
map.values;     // Iterable<int>
map.entries;    // Iterable<MapEntry<String, int>>
```

---

## 4. Performance — ¿Cuál usar?

| Operación | `List` | `Set` | `Map` |
|-----------|--------|-------|-------|
| Buscar por valor | O(n) | O(1) | — |
| Buscar por clave | — | — | O(1) |
| Insertar | O(1) al final | O(1) | O(1) |
| Eliminar | O(n) | O(1) | O(1) |
| Ordenado | ✅ Sí (insert order) | ❌ No garantiza | ❌ No garantiza (LinkedHashMap default sí mantiene orden) |
| Duplicados | ✅ Permite | ❌ No permite | ❌ No permite claves duplicadas |

> **📌 Regla práctica**: Si BUSCAS elementos por valor frecuentemente → `Set`. Si necesitas pares clave:valor → `Map`. Si necesitas orden + duplicados → `List`.

---

## 5. Colecciones inmutables (defensivas)

```dart
// En tus entidades, SIEMPRE devuelve copias inmutables
class Usuario {
  final List<String> roles;

  const Usuario({required this.roles});

  // ❌ Así NO: expones la lista interna
  List<String> get rolesExposed => roles;

  // ✅ Así SÍ: devuelves una copia que no se puede modificar
  List<String> get rolesSafe => List.unmodifiable(roles);
}
```

---

## 🏋️ Mini-ejercicios

```dart
// Dada esta lista:
final datos = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5];

// 1. Obtén los valores únicos
final unicos = datos.toSet();             // {3, 1, 4, 5, 9, 2, 6}

// 2. Obtén los primeros 4 elementos
final primeros = datos.take(4).toList(); // [3, 1, 4, 1]

// 3. ¿Existe el número 9?
final tiene9 = datos.contains(9);        // true

// 4. Crea un Map donde la clave sea el número y el valor sea su frecuencia
final frecuencias = <int, int>{};
for (final n in datos) {
  frecuencias.update(n, (v) => v + 1, ifAbsent: () => 1);
}
// {3: 2, 1: 2, 4: 1, 5: 3, 9: 1, 2: 1, 6: 1}
```

---

## ✅ Checklist

- [ ] Conozco `List.filled`, `List.generate`, `List.unmodifiable`
- [ ] Sé usar `Set` para unicidad y operaciones de conjunto
- [ ] Domino `putIfAbsent`, `update`, `removeWhere` en Map
- [ ] Entiendo por qué `Set` y `Map` tienen O(1) en búsqueda
- [ ] Siempre devuelvo colecciones inmutables desde mis entidades

---

## 📚 Referencias

- [Dart | Language tour](https://dart.dev/language) — Recorrido completo por el lenguaje Dart
- [Dart | Collections](https://dart.dev/language/collections) — Documentación de List, Set, Map
- [Dart | Records y patterns](https://dart.dev/language/records) — Features modernos de Dart 3

---

**Siguiente**: [03-metodos-funcionales-listas.md](./03-metodos-funcionales-listas.md) — El corazón de la manipulación de datos
