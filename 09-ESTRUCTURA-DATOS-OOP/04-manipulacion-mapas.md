# 04 — Manipulación Avanzada de Mapas

> Los Mapas (`Map<K, V>`) son la estructura más versátil para datos estructurados. Aquí aprenderás a construirlos, transformarlos y combinarlos como un profesional.

---

## 🎯 Objetivos

- Construir Maps desde otras colecciones
- Transformar keys y values masivamente
- Agrupar datos con `fold` y `groupBy`
- Mergear Maps con resolución de conflictos

---

## 1. Construir Maps desde Colecciones

### `Map.fromIterable`

```dart
final ids = [1, 2, 3, 4, 5];

final mapa = Map<int, String>.fromIterable(
  ids,
  key: (id) => id,
  value: (id) => 'Usuario $id',
);
// {1: 'Usuario 1', 2: 'Usuario 2', 3: 'Usuario 3', ...}
```

### `Map.fromIterables`

Cuando tienes keys y values por separado:

```dart
final keys = ['a', 'b', 'c'];
final values = [1, 2, 3];

final mapa = Map.fromIterables(keys, values);
// {'a': 1, 'b': 2, 'c': 3}

// ⚠️ Si las longitudes difieren → crash
```

### `Map.fromEntries`

Para el control más fino:

```dart
final entries = [
  MapEntry('x', 10),
  MapEntry('y', 20),
  MapEntry('z', 30),
];

final mapa = Map.fromEntries(entries);
// {'x': 10, 'y': 20, 'z': 30}
```

---

## 2. Transformar Maps: `.map()` en Maps

En Maps, `.map()` transforma **ambos**, keys y values:

```dart
final original = {'a': 1, 'b': 2, 'c': 3};

final transformado = original.map((key, value) {
  return MapEntry(key.toUpperCase(), value * 10);
});
// {'A': 10, 'B': 20, 'C': 30}
```

### Transformar solo values

```dart
final edades = {'Ana': 25, 'Bob': 17, 'Carlos': 30};

final mayores = edades.map((key, value) {
  return MapEntry(key, value >= 18 ? 'adulto' : 'menor');
});
// {'Ana': 'adulto', 'Bob': 'menor', 'Carlos': 'adulto'}
```

### Filtrar un Map

```dart
final edades = {'Ana': 25, 'Bob': 17, 'Carlos': 30};

// Filtrar por key
final soloA = edades
    .entries
    .where((e) => e.key.startsWith('A'))
    .fold<Map<String, int>>({}, (map, e) {
      map[e.key] = e.value;
      return map;
    });

// O más simple con removeWhere
final filtrado = Map.from(edades);
filtrado.removeWhere((key, value) => value < 18);
// {'Ana': 25, 'Carlos': 30}
```

---

## 3. Agrupar Datos (Group By)

Dart no tiene `groupBy` nativo, pero puedes implementarlo con `fold`:

```dart
final usuarios = [
  _User('Ana', 'admin'),
  _User('Bob', 'user'),
  _User('Carlos', 'admin'),
  _User('Diana', 'user'),
  _User('Eva', 'moderator'),
];

// GroupBy genérico usando fold
Map<String, List<_User>> agruparPorRol(List<_User> usuarios) {
  return usuarios.fold({}, (Map<String, List<_User>> map, user) {
    map.putIfAbsent(user.rol, () => []);
    map[user.rol]!.add(user);
    return map;
  });
}

final agrupado = agruparPorRol(usuarios);
// {
//   'admin': [Ana, Carlos],
//   'user': [Bob, Diana],
//   'moderator': [Eva]
// }
```

### GroupBy con conteo

```dart
// Contar cuántos hay por rol
final conteo = usuarios.fold<Map<String, int>>({}, (map, user) {
  map[user.rol] = (map[user.rol] ?? 0) + 1;
  return map;
});
// {'admin': 2, 'user': 2, 'moderator': 1}
```

---

## 4. Mergear Maps

### Merge simple

```dart
final a = {'x': 1, 'y': 2};
final b = {'y': 3, 'z': 4};

final mergeSimple = {...a, ...b};
// {'x': 1, 'y': 3, 'z': 4} — b sobrescribe a en 'y'
```

### Merge con resolución de conflictos

```dart
final local = {'items': 5, 'total': 100.0};
final remoto = {'items': 8, 'descuento': 0.1};

// Tomar el valor MÁS ALTO para cada clave
final merge = <String, dynamic>{};
for (final key in {...local.keys, ...remoto.keys}) {
  final localVal = local[key];
  final remotoVal = remoto[key];

  if (localVal == null) {
    merge[key] = remotoVal;
  } else if (remotoVal == null) {
    merge[key] = localVal;
  } else if (localVal is num && remotoVal is num) {
    merge[key] = localVal > remotoVal ? localVal : remotoVal;
  } else {
    merge[key] = remotoVal; // default: gana remoto
  }
}
// {'items': 8, 'total': 100.0, 'descuento': 0.1}
```

### Merge de listas dentro de Maps

```dart
final cache1 = {'ids': [1, 2, 3]};
final cache2 = {'ids': [3, 4, 5]};

// Combinar listas sin duplicados
final mergeado = Map.from(cache1);
for (final entry in cache2.entries) {
  if (mergeado.containsKey(entry.key)) {
    final combinado = [
      ...mergeado[entry.key] as List,
      ...entry.value as List,
    ];
    mergeado[entry.key] = combinado.toSet().toList();
  } else {
    mergeado[entry.key] = entry.value;
  }
}
// {'ids': [1, 2, 3, 4, 5]}
```

---

## 5. Casos Reales con Maps

### Mapa de frecuencias

```dart
final texto = 'hello world hello dart world hello';
final palabras = texto.split(' ');

final frecuencia = <String, int>{};
for (final p in palabras) {
  frecuencia.update(p, (v) => v + 1, ifAbsent: () => 1);
}
// {'hello': 3, 'world': 2, 'dart': 1}

// Top 3 palabras más frecuentes
final top3 = frecuencia.entries
    .toList()
    ..sort((a, b) => b.value.compareTo(a.value));
final resultado = top3.take(3).map((e) => e.key).toList();
// ['hello', 'world', 'dart']
```

### Cache simple con Map

```dart
class CacheManager<K, V> {
  final _cache = <K, V>{};
  final Map<K, DateTime> _expirations = {};

  V? get(K key) {
    final exp = _expirations[key];
    if (exp != null && DateTime.now().isAfter(exp)) {
      _cache.remove(key);
      _expirations.remove(key);
      return null;
    }
    return _cache[key];
  }

  void set(K key, V value, {Duration ttl = const Duration(minutes: 5)}) {
    _cache[key] = value;
    _expirations[key] = DateTime.now().add(ttl);
  }

  void invalidate(K key) {
    _cache.remove(key);
    _expirations.remove(key);
  }

  void clear() {
    _cache.clear();
    _expirations.clear();
  }
}
```

### Indexación: buscar rápido con Map

```dart
// ❌ Búsqueda O(n) en lista
final usuarios = obtenerUsuarios();
final usuario = usuarios.firstWhere((u) => u.id == targetId);

// ✅ Búsqueda O(1) con Map indexado
final indexPorId = Map<String, User>.fromIterable(
  usuarios,
  key: (u) => u.id,
);
final usuario = indexPorId[targetId]; // O(1) instantáneo
```

---

## 🏋️ Mini-ejercicios

```dart
// DATOS
final ventas = [
  _Venta('rifa1', 100.0, 'Ana'),
  _Venta('rifa2', 50.0, 'Bob'),
  _Venta('rifa1', 75.0, 'Ana'),
  _Venta('rifa3', 200.0, 'Carlos'),
  _Venta('rifa2', 25.0, 'Bob'),
];

class _Venta {
  final String productId;
  final double monto;
  final String vendedor;
  _Venta(this.productId, this.monto, this.vendedor);
}

// 1. Total de ventas por vendedor
final porVendedor = ventas.fold<Map<String, double>>({}, (map, v) {
  map[v.vendedor] = (map[v.vendedor] ?? 0) + v.monto;
  return map;
});
// {'Ana': 175.0, 'Bob': 75.0, 'Carlos': 200.0}

// 2. ¿Cuántas ventas por producto?
final conteoProductos = ventas.fold<Map<String, int>>({}, (map, v) {
  map[v.productId] = (map[v.productId] ?? 0) + 1;
  return map;
});
// {'rifa1': 2, 'rifa2': 2, 'rifa3': 1}

// 3. Merge de dos configuraciones
final defaultConfig = {'theme': 'light', 'lang': 'es', 'debug': 'false'};
final userConfig = {'theme': 'dark', 'notifications': 'true'};
final finalConfig = {...defaultConfig, ...userConfig};
// {'theme': 'dark', 'lang': 'es', 'debug': 'false', 'notifications': 'true'}
```

---

## ✅ Cheatsheet

| Operación | Código |
|-----------|--------|
| Crear desde iterable | `Map.fromIterable(items, key: ..., value: ...)` |
| Crear desde 2 listas | `Map.fromIterables(keys, values)` |
| Transformar keys/values | `.map((k, v) => MapEntry(newK, newV))` |
| Filtrar | `.entries.where(...)` o `removeWhere(...)` |
| Merge simple | `{...map1, ...map2}` |
| GroupBy | `fold({}, (map, e) => map..putIfAbsent(...)..put(...))` |
| Frecuencias | `update(key, (v) => v+1, ifAbsent: () => 1)` |

---

## 📚 Referencias

- [Dart | Language tour](https://dart.dev/language) — Recorrido completo por el lenguaje Dart
- [Dart | Collections](https://dart.dev/language/collections) — Documentación de List, Set, Map
- [Dart | Records y patterns](https://dart.dev/language/records) — Features modernos de Dart 3

---

**Siguiente**: [05-algoritmos-colecciones.md](./05-algoritmos-colecciones.md) — Sorting, búsqueda y algoritmos
