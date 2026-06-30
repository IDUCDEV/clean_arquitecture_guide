# 05 — Algoritmos con Colecciones

> Ya sabes transformar y filtrar. Ahora aprende a **ordenar, buscar y paginar** datos eficientemente.

---

## 🎯 Objetivos

- Ordenar con `Comparable` y `Comparator`
- Implementar búsqueda personalizada
- Paginar colecciones manualmente
- Operaciones entre conjuntos (Set)

---

## 1. Sorting — `sort()` y `Comparable`

### sort() básico

```dart
final numeros = [3, 1, 4, 1, 5, 9];
numeros.sort();
// [1, 1, 3, 4, 5, 9]

final palabras = ['banana', 'manzana', 'cereza'];
palabras.sort();
// ['banana', 'cereza', 'manzana'] (orden alfabético)
```

### sort() con Comparator (orden personalizado)

```dart
final numeros = [3, 1, 4, 1, 5, 9];

// Descendente
numeros.sort((a, b) => b.compareTo(a));
// [9, 5, 4, 3, 1, 1]

// Por longitud de string
final palabras = ['dart', 'flutter', 'js', 'react'];
palabras.sort((a, b) => a.length.compareTo(b.length));
// ['js', 'dart', 'react', 'flutter']
```

### Caso real: ordenar objetos

```dart
class Usuario {
  final String nombre;
  final int edad;
  final DateTime creado;
}

final usuarios = obtenerUsuarios();

// Por edad ascendente
usuarios.sort((a, b) => a.edad.compareTo(b.edad));

// Por nombre descendente
usuarios.sort((a, b) => b.nombre.compareTo(a.nombre));

// Por fecha de creación (más reciente primero)
usuarios.sort((a, b) => b.creado.compareTo(a.creado));

// ORDEN COMPUESTO: primero por edad, luego por nombre
usuarios.sort((a, b) {
  final cmpEdad = a.edad.compareTo(b.edad);
  if (cmpEdad != 0) return cmpEdad;
  return a.nombre.compareTo(b.nombre);
});
```

### Implementar `Comparable` en tu clase

```dart
class Producto implements Comparable<Producto> {
  final String nombre;
  final double precio;

  @override
  int compareTo(Producto other) {
    return precio.compareTo(other.precio);
  }
}

final productos = obtenerProductos();
productos.sort(); // ahora ordena por precio automáticamente
```

---

## 2. Búsqueda

### Búsqueda lineal con métodos funcionales

```dart
final usuarios = obtenerUsuarios();

// Encontrar por condición
final admin = usuarios.firstWhere(
  (u) => u.rol == 'admin',
  orElse: () => Usuario.empty(),
);

// ¿Existe?
final hayMenores = usuarios.any((u) => u.edad < 18);

// Contar cuántos cumplen
final admins = usuarios.where((u) => u.rol == 'admin').length;
```

### Búsqueda binaria (en listas ordenadas)

```dart
final ids = [1, 3, 5, 7, 9, 11, 13];

// lowerBound: primer índice donde insertar sin romper orden
import 'package:collection/collection.dart';

final index = ids.lowerBound(7);     // 3 (el 7 está en índice 3)
final index2 = ids.lowerBound(6);     // 3 (se insertaría entre 5 y 7)
```

### Indexación con Map (búsqueda O(1))

```dart
// ❌ Búsqueda O(n)
final user = usuarios.firstWhere((u) => u.id == id);

// ✅ Indexar con Map = O(1)
final indexPorId = {
  for (final u in usuarios)
    u.id: u,
};

final user = indexPorId[id]; // instantáneo
```

> **📌 Regla de rendimiento**: Si buscas más de 10 elementos por ID en una lista de >100, **siempre indexa con Map**.

---

## 3. Paginación Manual

```dart
final todos = List.generate(100, (i) => 'Item $i');

int pagina = 0;
final pageSize = 10;

List<String> getPagina(int numeroPagina) {
  final start = numeroPagina * pageSize;
  return todos.skip(start).take(pageSize).toList();
}

final pagina1 = getPagina(0); // ['Item 0', ..., 'Item 9']
final pagina2 = getPagina(1); // ['Item 10', ..., 'Item 19']

// Con objetos
class PaginatedResult<T> {
  final List<T> items;
  final int total;
  final int pagina;
  final int totalPaginas;
  final bool tieneSiguiente;

  PaginatedResult({
    required this.items,
    required this.total,
    required this.pagina,
    required this.pageSize,
  }) : totalPaginas = (total / pageSize).ceil(),
       tieneSiguiente = pagina < (total / pageSize).ceil() - 1;

  final int pageSize;
}

PaginatedResult<Rifa> paginarRifas(List<Rifa> todas, int pagina, {int pageSize = 20}) {
  final start = pagina * pageSize;
  final items = todas.skip(start).take(pageSize).toList();
  return PaginatedResult(
    items: items,
    total: todas.length,
    pagina: pagina,
    pageSize: pageSize,
  );
}
```

---

## 4. Operaciones entre Sets

```dart
final activas = {'rifa1', 'rifa2', 'rifa3'};
final pagadas = {'rifa2', 'rifa3', 'rifa4'};

// Rifas activas y pagadas (intersección)
final activasYPagadas = activas.intersection(pagadas);  // {'rifa2', 'rifa3'}

// Rifas activas pero no pagadas (diferencia)
final activasNoPagadas = activas.difference(pagadas);   // {'rifa1'}

// Todas las rifas (unión)
final todas = activas.union(pagadas);                   // {'rifa1', 'rifa2', 'rifa3', 'rifa4'}

// Rifas en una sola lista pero no en ambas (diferencia simétrica)
final exclusivas = activas.difference(pagadas).union(pagadas.difference(activas));
// {'rifa1', 'rifa4'}
```

---

## 5. Algoritmos con datos anidados

```dart
// App de rifas: queremos las categorías con más rifas activas
class Rifa {
  final String categoria;
  final String estado;
}

final rifas = obtenerRifas();

final categorias = rifas
    .where((r) => r.estado == 'activa')
    .fold<Map<String, int>>({}, (map, r) {
      map[r.categoria] = (map[r.categoria] ?? 0) + 1;
      return map;
    })
    .entries
    .toList()
    ..sort((a, b) => b.value.compareTo(a.value));

final topCategorias = categorias.take(5).map((e) => e.key).toList();
```

---

## 🏋️ Mini-ejercicios

```dart
// DATOS
final productos = [
  _Producto('Laptop', 1200, 'electronica'),
  _Producto('Mouse', 25, 'electronica'),
  _Producto('Camiseta', 15, 'ropa'),
  _Producto('Monitor', 300, 'electronica'),
  _Producto('Pantalon', 45, 'ropa'),
];

class _Producto {
  final String nombre;
  final double precio;
  final String categoria;
  _Producto(this.nombre, this.precio, this.categoria);
}

// 1. Ordenar productos por precio descendente
final porPrecio = List<_Producto>.from(productos)
  ..sort((a, b) => b.precio.compareTo(a.precio));

// 2. Top 2 productos más baratos por categoría
final baratosPorCat = productos
    .fold<Map<String, List<_Producto>>>({}, (map, p) {
      map.putIfAbsent(p.categoria, () => []);
      map[p.categoria]!.add(p);
      return map;
    })
    .map((cat, lista) {
      lista.sort((a, b) => a.precio.compareTo(b.precio));
      return MapEntry(cat, lista.take(2).toList());
    });

// 3. Paginar productos (página 0, tamaño 2)
final pagina0 = productos.take(2).toList(); // [Laptop, Mouse]
```

---

## ✅ Checklist

- [ ] Sé ordenar con `Comparator` personalizado y compuesto
- [ ] Implemento `Comparable` en mis entidades
- [ ] Uso `firstWhere` con `orElse` para búsqueda segura
- [ ] Indexo con Map para búsqueda O(1)
- [ ] Implemento paginación con `skip`/`take`
- [ ] Uso `Set.union`, `intersection`, `difference`

---

**Siguiente**: [06-oop-modelado-datos.md](./06-oop-modelado-datos.md) — Modelado de datos con OOP
