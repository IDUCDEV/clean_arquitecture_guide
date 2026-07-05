# 03 — Métodos Funcionales para Listas

> **Este es el archivo más importante del módulo**. Aquí aprenderás los métodos que transforman, filtran y reducen colecciones sin usar bucles `for`. **Domina esto y dejarás de depender de la IA para manipular datos.**

---

## 🎯 Objetivos

- Entender cada método: `map`, `where`, `reduce`, `fold`, `expand`
- Encadenar métodos para crear pipelines de datos
- Saber cuándo usar `for` vs métodos funcionales

---

## 🧠 La Idea Clave

Los métodos funcionales convierten esto:

```dart
// ❌ CÓDIGO ESPAGUETI con for:
List<String> nombres = [];
for (var i = 0; i < usuarios.length; i++) {
  if (usuarios[i].isActive) {
    nombres.add(usuarios[i].name.toUpperCase());
  }
}
```

En esto:

```dart
// ✅ PIPELINE FUNCIONAL:
final nombres = usuarios
    .where((u) => u.isActive)
    .map((u) => u.name.toUpperCase())
    .toList();
```

---

## 1. `.map()` — Transformar CADA elemento

Transforma cada elemento de la colección aplicando una función.

```dart
final numeros = [1, 2, 3, 4, 5];

final cuadrados = numeros.map((n) => n * n).toList();
// [1, 4, 9, 16, 25]

final strings = numeros.map((n) => 'Número $n').toList();
// ['Número 1', 'Número 2', 'Número 3', 'Número 4', 'Número 5']
```

### Caso real: convertir modelos a entidades

```dart
// Data layer → Domain layer
class UserModel {
  final String id;
  final String name;
  UserEntity toEntity() => UserEntity(id: id, name: name);
}

final models = [UserModel(id: '1', name: 'Ana'), UserModel(id: '2', name: 'Bob')];

// ✅ Transformación masiva
final entities = models.map((m) => m.toEntity()).toList();
```

> ⚠️ **`.map()` es perezoso (lazy)**: no ejecuta la función hasta que iteres. Por eso siempre llamamos `.toList()` al final.

---

## 2. `.where()` — FILTRAR elementos

Selecciona los elementos que cumplen una condición.

```dart
final numeros = [1, 2, 3, 4, 5, 6];

final pares = numeros.where((n) => n.isEven).toList();    // [2, 4, 6]
final mayores3 = numeros.where((n) => n > 3).toList();    // [4, 5, 6]
final rango = numeros.where((n) => n >= 2 && n <= 4).toList(); // [2, 3, 4]
```

### Variantes de where

```dart
// .firstWhere() — primer elemento que cumple (crash si no encuentra)
final primero = numeros.firstWhere((n) => n > 3);           // 4
final seguro = numeros.firstWhere((n) => n > 100, orElse: () => -1); // -1

// .singleWhere() — exactamente UNO (crash si 0 o más de 1)
final unico = numeros.singleWhere((n) => n == 3);           // 3

// .lastWhere() — último que cumple
final ultimo = numeros.lastWhere((n) => n < 4);             // 3
```

### Caso real: filtrar rifas activas

```dart
class Rifa {
  final String estado; // 'activa', 'cancelada', 'finalizada'
  final DateTime fechaSorteo;
}

final rifas = obtenerRifas();

final activas = rifas.where((r) => r.estado == 'activa').toList();
final proximas = rifas
    .where((r) => r.estado == 'activa' && r.fechaSorteo.isAfter(DateTime.now()))
    .toList();
```

---

## 3. `.reduce()` y `.fold()` — COMBINAR elementos en uno solo

### `.reduce()` — Sin valor inicial

```dart
final numeros = [1, 2, 3, 4, 5];

final suma = numeros.reduce((acc, n) => acc + n);
// 1+2 → 3, 3+3 → 6, 6+4 → 10, 10+5 → 15
// Resultado: 15

final maximo = numeros.reduce((acc, n) => acc > n ? acc : n);  // 5

// ⚠️ Crash si la lista está vacía
// [].reduce((a, b) => a + b); // ❌ Error
```

### `.fold()` — Con valor inicial (más seguro)

```dart
final numeros = [1, 2, 3, 4, 5];

final suma = numeros.fold(0, (acc, n) => acc + n);   // 15
final producto = numeros.fold(1, (acc, n) => acc * n); // 120

// Con valor inicial, incluso lista vacía funciona:
final vacio = [].fold(0, (acc, n) => acc + n);        // 0 (sin crash)
```

### Diferencia clave

| Aspecto | `.reduce()` | `.fold()` |
|---------|-------------|-----------|
| Valor inicial | Usa el primer elemento | Tú lo proporcionas |
| Tipo de retorno | Mismo que la lista (E) | El que tú quieras (T) |
| Lista vacía | ❌ Crash | ✅ Retorna el inicial |
| Tipo diferente | ❌ No puede | ✅ Sí: `fold<String>('', ...)` |

### Caso real: construir un Map con fold

```dart
final usuarios = [User(name: 'Ana', role: 'admin'), User(name: 'Bob', role: 'user'), User(name: 'Carlos', role: 'admin')];

// Agrupar usuarios por rol usando fold
final porRol = usuarios.fold<Map<String, List<User>>>(
  {},
  (map, user) {
    map.putIfAbsent(user.role, () => []);
    map[user.role]!.add(user);
    return map;
  },
);
// {'admin': [Ana, Carlos], 'user': [Bob]}
```

---

## 4. `.expand()` — APLANAR y expandir

Cada elemento puede producir **0, 1 o N** elementos nuevos.

```dart
final listas = [[1, 2], [3, 4], [5]];

final aplanado = listas.expand((l) => l).toList();
// [1, 2, 3, 4, 5]

// También sirve para "descartar" (devolviendo lista vacía)
final palabras = ['hola', '', 'mundo', ''];
final noVacios = palabras.expand((p) => p.isEmpty ? [] : [p]).toList();
// ['hola', 'mundo']

// O para expandir cada elemento en múltiples
final numeros = [1, 2, 3];
final duplicados = numeros.expand((n) => [n, n]).toList();
// [1, 1, 2, 2, 3, 3]
```

### Caso real: extraer todas las etiquetas

```dart
class Producto {
  final List<String> tags;
}

final productos = [
  Producto(tags: ['verde', 'grande']),
  Producto(tags: ['rojo', 'pequeño']),
  Producto(tags: ['verde', 'mediano']),
];

final todasTags = productos
    .expand((p) => p.tags)
    .toSet()  // sin duplicados
    .toList();
// ['verde', 'grande', 'rojo', 'pequeño', 'mediano']
```

---

## 5. `.any()` y `.every()` — TEST condicional

```dart
final edades = [18, 22, 15, 30, 17];

final algunMenor = edades.any((e) => e < 18);        // true
final todosAdultos = edades.every((e) => e >= 18);    // false
final ningunoNegativo = !edades.any((e) => e < 0);   // true
```

### Caso real: validación

```dart
final formulario = [
  Campo(valor: 'Ana', esValido: true),
  Campo(valor: '', esValido: false),
  Campo(valor: 'correo@test.com', esValido: true),
];

final esValido = formulario.every((c) => c.esValido); // false
final hayErrores = formulario.any((c) => !c.esValido); // true
```

---

## 6. Otros métodos útiles

```dart
final nums = [3, 1, 4, 1, 5, 9];

// .take() / .skip() — subconjuntos
nums.take(3).toList();         // [3, 1, 4]
nums.skip(3).toList();         // [1, 5, 9]
nums.skip(2).take(2).toList(); // [4, 1]

// .join() — concatenar strings
['a', 'b', 'c'].join(', ');   // 'a, b, c'

// .toSet() — eliminar duplicados
[1, 2, 2, 3].toSet().toList(); // [1, 2, 3]

// .cast() — cambiar tipo
final dynamicList = [1, 2, 3];
final intList = dynamicList.cast<int>();

// .whereType() — filtrar por tipo
final mixed = [1, 'hola', 2, 'mundo', 3];
final soloInts = mixed.whereType<int>().toList();      // [1, 2, 3]
final soloStrings = mixed.whereType<String>().toList(); // ['hola', 'mundo']
```

---

## 7. Encadenamiento (pipeline)

```dart
// Pipeline completo: filtrar → transformar → ordenar → limitar
final numeros = [5, 2, 8, 1, 9, 3, 7, 4, 6];

final resultado = numeros
    .where((n) => n.isEven)              // [2, 8, 4, 6]
    .map((n) => n * 10)                  // [20, 80, 40, 60]
    .toList()                            // materializar
    ..sort();                            // [20, 40, 60, 80]

// Caso real en una app de rifas:
final rifas = obtenerRifas();

final ganadoresProximos = rifas
    .where((r) => r.estado == 'activa')
    .where((r) => r.fechaSorteo.isAfter(DateTime.now()))
    .map((r) => RifaPreview(
        nombre: r.nombre,
        premio: r.premio,
        fecha: r.fechaSorteo,
      ))
    .toList()
    ..sort((a, b) => a.fecha.compareTo(b.fecha));
```

---

## 8. ¿Cuándo usar `for` en vez de métodos funcionales?

| Usa `for` cuando... | Usa métodos funcionales cuando... |
|-------------------|----------------------------------|
| Necesitas `break` o `return` anticipado | Transformas cada elemento (`.map`) |
| Necesitas el índice Y el valor | Filtras (`.where`) |
| El cuerpo del bucle es > 5 líneas | Acumulas un resultado (`.fold`) |
| Performance crítica (millones de items) | Encadenas operaciones |

```dart
// ✅ BUEN USO de for (break necesario)
for (final user in usuarios) {
  if (user.id == targetId) {
    encontrado = user;
    break;
  }
}

// ❌ MAL USO de for (se podía con .map)
List<String> nombres = [];
for (final u in usuarios) {
  nombres.add(u.name);
}
// ✅ Mejor: usuarios.map((u) => u.name).toList();
```

---

## 🏋️ Mini-ejercicios

```dart
// DATOS: lista de usuarios
final usuarios = [
  _User('Ana', 25, 'admin'),
  _User('Bob', 17, 'user'),
  _User('Carlos', 30, 'user'),
  _User('Diana', 15, 'admin'),
];

class _User {
  final String nombre;
  final int edad;
  final String rol;
  _User(this.nombre, this.edad, this.rol);
}

// 1. Nombres de usuarios admin
final admins = usuarios
    .where((u) => u.rol == 'admin')
    .map((u) => u.nombre)
    .toList(); // ['Ana', 'Diana']

// 2. ¿Hay algún menor de edad?
final hayMenor = usuarios.any((u) => u.edad < 18); // true

// 3. Suma de edades de todos
final sumaEdades = usuarios.fold(0, (acc, u) => acc + u.edad); // 87

// 4. Agrupar usuarios por rol (con fold)
final porRol = usuarios.fold<Map<String, List<_User>>>(
  {},
  (map, u) {
    map.putIfAbsent(u.rol, () => []);
    map[u.rol]!.add(u);
    return map;
  },
);
```

---

## ✅ Cheatsheet (guárdalo)

| Método | Hace | Retorna |
|--------|------|---------|
| `.map(f)` | Transforma cada elemento | `Iterable` |
| `.where(f)` | Filtra manteniendo tipo | `Iterable` |
| `.firstWhere(f)` | Primer match | `E` (o crash) |
| `.singleWhere(f)` | Único match | `E` (o crash) |
| `.any(f)` | ¿Alguno cumple? | `bool` |
| `.every(f)` | ¿Todos cumplen? | `bool` |
| `.reduce(f)` | Combina (sin inicial) | `E` |
| `.fold(init, f)` | Combina (con inicial) | `T` |
| `.expand(f)` | Aplana o 1→N elementos | `Iterable` |
| `.whereType<T>()` | Filtra por tipo | `Iterable<T>` |

---

## 📚 Referencias

- [Dart | Language tour](https://dart.dev/language) — Recorrido completo por el lenguaje Dart
- [Dart | Collections](https://dart.dev/language/collections) — Documentación de List, Set, Map
- [Dart | Records y patterns](https://dart.dev/language/records) — Features modernos de Dart 3

---

**Siguiente**: [04-manipulacion-mapas.md](./04-manipulacion-mapas.md) — Manipulación avanzada de Mapas
