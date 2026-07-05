# 08 — Ejercicios Básicos (Nivel 1)

> 10 ejercicios para DOMINAR los fundamentos. **No uses IA para resolverlos.** Escribe cada línea tú mismo en [Dartpad](https://dartpad.dev).

---

## ⚙️ Cómo practicar

1. Abre [Dartpad](https://dartpad.dev) o tu editor
2. Lee el enunciado
3. **Intenta resolverlo sin mirar la solución**
4. Corre el código y verifica que los `print` den los resultados esperados
5. Si te atascas >5 minutos, relee el archivo correspondiente

---

## Ejercicio 1: Tipos y null safety

```dart
// Declara una variable String? llamada 'apodo' que sea null
// Luego imprímela de 3 formas:
// 1. Con ?. (null safe)
// 2. Con ?? (default 'Sin apodo')
// 3. Con ! (solo si estás seguro que no es null — aquí crash intencional)

// 👇 Tu código aquí
String? apodo;
print(apodo?.length);                // ¿qué imprime?
print(apodo ?? 'Sin apodo');         // ¿qué imprime?
print(apodo!.length);                // ¿qué imprime?
```

<details>
<summary>🔍 Solución</summary>

```dart
String? apodo;
print(apodo?.length);   // null (operador ?. retorna null)
print(apodo ?? 'Sin apodo'); // 'Sin apodo' (?? da default)
// print(apodo!.length); // CRASH: assertion failed (no ejecutar)
```
</details>

---

## Ejercicio 2: var vs final vs const

```dart
// ¿Cuál de estas líneas COMPILAN y cuáles NO?

var a = 'hello';
final b = 'world';
const c = 'dart';

a = 'hi';        // ¿?
b = 'earth';     // ¿?
c = 'flutter';   // ¿?

var d = [1, 2, 3];
final e = [1, 2, 3];
const f = [1, 2, 3];

d.add(4);        // ¿?
e.add(4);        // ¿?
f.add(4);        // ¿?
```

<details>
<summary>🔍 Solución</summary>

```dart
a = 'hi';        // ✅ var permite reasignación
b = 'earth';     // ❌ final no se reasigna
c = 'flutter';   // ❌ const no se reasigna

d.add(4);        // ✅ var mutable, la lista se modifica
e.add(4);        // ✅ final es la referencia, no el contenido
                 //    e no puede REASIGNARSE, pero la lista SÍ se modifica
// f.add(4);     // ❌ const es inmutable en tiempo de compilación
```
</details>

---

## Ejercicio 3: Genéricos

```dart
// Escribe una función genérica que reciba una List<T>
// y devuelva el PRIMER y ÚLTIMO elemento como un Map con keys 'first' y 'last'
// Si la lista está vacía, retorna null

Map<String, T>? primeroYUltimo<T>(List<T> items) {
  // 👇 Tu código aquí
  if (items.isEmpty) return null;
  return {'first': items.first, 'last': items.last};
}

// Test:
print(primeroYUltimo<int>([1, 2, 3]));      // {first: 1, last: 3}
print(primeroYUltimo<String>(['a', 'b']));   // {first: a, last: b}
print(primeroYUltimo<double>([]));            // null
```

<details>
<summary>🔍 Solución</summary>

```dart
Map<String, T>? primeroYUltimo<T>(List<T> items) {
  if (items.isEmpty) return null;
  return {'first': items.first, 'last': items.last};
}
```
</details>

---

## Ejercicio 4: Constructores de List

```dart
// Usando constructor de List, crea:

// 1. Una lista de 5 ceros: [0, 0, 0, 0, 0]
final ceros = List<int>.filled(5, 0);

// 2. Una lista con [0, 2, 4, 6, 8] (pares)
final pares = List<int>.generate(5, (i) => i * 2);

// 3. Una lista inmutable de [1, 2, 3]
final inmutable = List<int>.unmodifiable([1, 2, 3]);

// Test:
print(ceros);      // ¿?
print(pares);      // ¿?
print(inmutable);  // ¿?
// inmutable.add(4);  // ¿qué pasa?
```

<details>
<summary>🔍 Solución</summary>

```dart
print(ceros);      // [0, 0, 0, 0, 0]
print(pares);      // [0, 2, 4, 6, 8]
print(inmutable);  // [1, 2, 3]
// inmutable.add(4);  // RuntimeError: unmodifiable
```
</details>

---

## Ejercicio 5: Operaciones de Lista

```dart
final datos = [5, 2, 8, 1, 9, 3, 7, 4, 6];

// 1. Obtén los primeros 3
final primeros = datos.take(3).toList();
print(primeros); // ¿?

// 2. Salta los primeros 4
final saltados = datos.skip(4).toList();
print(saltados); // ¿?

// 3. Elimina todos los pares (usando removeWhere)
final sinPares = [...datos];
sinPares.removeWhere((n) => n.isEven);
print(sinPares); // ¿?
```

<details>
<summary>🔍 Solución</summary>

```dart
print(primeros); // [5, 2, 8]
print(saltados); // [9, 3, 7, 4, 6]
print(sinPares); // [5, 1, 9, 3, 7]
```
</details>

---

## Ejercicio 6: Set (unicidad)

```dart
final idsIngresados = [101, 102, 103, 101, 104, 102, 105];

// 1. Obtén los IDs únicos (usa Set)
final unicos = idsIngresados.toSet();
print(unicos); // ¿?

// 2. ¿El ID 103 fue ingresado?
final tiene103 = unicos.contains(103);
print(tiene103); // ¿?

// 3. ¿Cuántos IDs únicos hay?
print(unicos.length); // ¿?
```

<details>
<summary>🔍 Solución</summary>

```dart
print(unicos);       // {101, 102, 103, 104, 105}
print(tiene103);     // true
print(unicos.length); // 5
```
</details>

---

## Ejercicio 7: Map básico

```dart
// Crea un Map<String, int> con nombres de frutas y su precio:
final frutas = <String, int>{
  'manzana': 10,
  'pera': 8,
  'banana': 5,
};

// 1. ¿Cuánto cuesta la manzana?
print(frutas['manzana']); // ¿?

// 2. Agrega 'uva' con precio 12
frutas['uva'] = 12;

// 3. Actualiza banana a 6
frutas['banana'] = 6;

// 4. ¿Existe 'kiwi'?
print(frutas.containsKey('kiwi')); // ¿?

print(frutas); // ¿?
```

<details>
<summary>🔍 Solución</summary>

```dart
print(frutas['manzana']);        // 10
print(frutas.containsKey('kiwi')); // false
print(frutas); // {manzana: 10, pera: 8, banana: 6, uva: 12}
```
</details>

---

## Ejercicio 8: Map con putIfAbsent y update

```dart
final contador = <String, int>{};

// Simula un contador de palabras:
final palabras = ['hola', 'mundo', 'hola', 'dart', 'mundo', 'hola'];

for (final p in palabras) {
  // Usa update con ifAbsent para contar
  // 👇 Tu código aquí
  contador.update(p, (v) => v + 1, ifAbsent: () => 1);
}

print(contador); // ¿?
```

<details>
<summary>🔍 Solución</summary>

```dart
// contador.update(p, (v) => v + 1, ifAbsent: () => 1);
print(contador); // {hola: 3, mundo: 2, dart: 1}
```
</details>

---

## Ejercicio 9: map() y where()

```dart
final edades = [15, 22, 18, 30, 12, 25, 17];

// 1. Filtra los mayores de edad (>= 18)
final mayores = edades.where((e) => e >= 18).toList();
print(mayores); // ¿?

// 2. De los mayores, crea strings 'Edad: X'
final strings = mayores.map((e) => 'Edad: $e').toList();
print(strings); // ¿?

// 3. Encadena: filtra pares, luego multiplícalos por 10
final paresX10 = edades
    .where((e) => e.isEven)
    .map((e) => e * 10)
    .toList();
print(paresX10); // ¿?
```

<details>
<summary>🔍 Solución</summary>

```dart
print(mayores);  // [22, 18, 30, 25]
print(strings);  // ['Edad: 22', 'Edad: 18', 'Edad: 30', 'Edad: 25']
print(paresX10); // [220, 180, 120]
```
</details>

---

## Ejercicio 10: reduce y fold

```dart
final precios = [10.5, 25.0, 8.75, 30.0, 15.25];

// 1. Suma total con reduce
final totalReduce = precios.reduce((a, b) => a + b);
print(totalReduce); // ¿?

// 2. Suma total con fold (con descuento de 5.0 inicial)
final totalFold = precios.fold(5.0, (acc, p) => acc + p);
print(totalFold); // ¿?

// 3. Producto de todos los números (1 * 2 * 3 * 4)
final nums = [1, 2, 3, 4, 5];
final producto = nums.reduce((a, b) => a * b);
print(producto); // ¿?
```

<details>
<summary>🔍 Solución</summary>

```dart
print(totalReduce); // 89.5
print(totalFold);   // 94.5 (89.5 + 5.0)
print(producto);    // 120
```
</details>

---

## 📚 Referencias

- [Dart | Language tour](https://dart.dev/language) — Recorrido completo por el lenguaje Dart
- [Dart | Collections](https://dart.dev/language/collections) — Documentación de List, Set, Map
- [Dart | Records y patterns](https://dart.dev/language/records) — Features modernos de Dart 3

---

## 🏁 Fin de nivel básico

¿Completaste todos? → Pasa a [09-ejercicios-intermedios.md](./09-ejercicios-intermedios.md)

**¿Te atascaste en alguno?** Relee el archivo correspondiente de la sección y vuelve a intentar.
