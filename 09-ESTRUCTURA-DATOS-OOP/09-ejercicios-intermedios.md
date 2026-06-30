# 09 — Ejercicios Intermedios (Nivel 2)

> 10 ejercicios con datos estructurados del mundo real. **Ya no hay ayudas** — Solo el enunciado y la solución al final.

---

## 🧠 Datos comunes para los ejercicios

Usa este modelo para los ejercicios 1-8:

```dart
class Rifa with EquatableMixin {
  final String id;
  final String nombre;
  final double precio;
  final String estado;     // 'activa', 'cancelada', 'finalizada'
  final String categoria;
  final DateTime creado;
  final int numerosVendidos;

  Rifa({
    required this.id,
    required this.nombre,
    required this.precio,
    required this.estado,
    required this.categoria,
    required this.creado,
    this.numerosVendidos = 0,
  });

  @override
  List<Object?> get props => [id];
}
```

Y estos datos de prueba:

```dart
final rifas = [
  Rifa(id: '1', nombre: 'TV 55"', precio: 10, estado: 'activa', categoria: 'electronica', creado: DateTime(2026, 6, 10), numerosVendidos: 45),
  Rifa(id: '2', nombre: 'Laptop', precio: 25, estado: 'activa', categoria: 'electronica', creado: DateTime(2026, 6, 15), numerosVendidos: 78),
  Rifa(id: '3', nombre: 'Bicicleta', precio: 15, estado: 'cancelada', categoria: 'deportes', creado: DateTime(2026, 5, 20), numerosVendidos: 12),
  Rifa(id: '4', nombre: 'Reloj', precio: 8, estado: 'activa', categoria: 'accesorios', creado: DateTime(2026, 6, 18), numerosVendidos: 33),
  Rifa(id: '5', nombre: 'GiftCard', precio: 5, estado: 'finalizada', categoria: 'regalos', creado: DateTime(2026, 4, 5), numerosVendidos: 90),
  Rifa(id: '6', nombre: 'PlayStation', precio: 20, estado: 'activa', categoria: 'electronica', creado: DateTime(2026, 6, 22), numerosVendidos: 55),
  Rifa(id: '7', nombre: 'Zapatillas', precio: 12, estado: 'activa', categoria: 'deportes', creado: DateTime(2026, 6, 25), numerosVendidos: 28),
];
```

---

## Ejercicio 1: Filtrar por estado y ordenar

```dart
// Obtén las rifas activas ordenadas por fecha descendente (más reciente primero)
// Resultado: [PlayStation (22-jun), Zapatillas (25-jun), Reloj (18-jun), Laptop (15-jun), TV 55" (10-jun)]

// 👇 Escribe tu código
final resultado = rifas
    .where((r) => r.estado == 'activa')
    .toList()
  ..sort((a, b) => b.creado.compareTo(a.creado));

print(resultado.map((r) => r.nombre).toList());
```

---

## Ejercicio 2: Agrupar por categoría

```dart
// Agrupa las rifas por categoría
// Resultado: {'electronica': [TV, Laptop, PlayStation], 'deportes': [Bici, Zapatillas], 'accesorios': [Reloj], 'regalos': [GiftCard]}

final porCategoria = rifas.fold<Map<String, List<Rifa>>>(
  {},
  (map, r) {
    map.putIfAbsent(r.categoria, () => []);
    map[r.categoria]!.add(r);
    return map;
  },
);

print(porCategoria);
```

---

## Ejercicio 3: Top 3 más vendidos

```dart
// Obtén las 3 rifas con más números vendidos (numerosVendidos)
// Resultado: [GiftCard (90), Laptop (78), PlayStation (55)]

final top3 = [...rifas]
  ..sort((a, b) => b.numerosVendidos.compareTo(a.numerosVendidos));

final resultado = top3.take(3).toList();
print(resultado.map((r) => '${r.nombre} (${r.numerosVendidos})').toList());
```

---

## Ejercicio 4: Ingreso total por categoría

```dart
// Calcula el ingreso total (precio * numerosVendidos) por categoría
// Resultado: {'electronica': 10*45 + 25*78 + 20*55, 'deportes': 15*12 + 12*28, ...}

final ingresos = rifas.fold<Map<String, double>>({}, (map, r) {
  map[r.categoria] = (map[r.categoria] ?? 0) + (r.precio * r.numerosVendidos);
  return map;
});

print(ingresos);
```

---

## Ejercicio 5: Buscar rifas por nombre

```dart
// Implementa una función que busque rifas por nombre (case insensitive)
// con el término de búsqueda

Rifa buscarRifa(List<Rifa> rifas, String termino) {
  return rifas.firstWhere(
    (r) => r.nombre.toLowerCase().contains(termino.toLowerCase()),
    orElse: () => throw Exception('No encontrada'),
  );
}

// Test:
print(buscarRifa(rifas, 'bici').nombre);      // Bicicleta
print(buscarRifa(rifas, 'PLAY').nombre);       // PlayStation
// buscarRifa(rifas, 'xbox'); // ❌ Exception
```

---

## Ejercicio 6: Transformar a Map para UI

```dart
// Transforma la lista de rifas a un Map<String, dynamic> para enviar a la UI
// Solo incluye: id, nombre, precio, estado y una nueva propiedad 'esActiva' (bool)

final paraUI = rifas.map((r) => {
  'id': r.id,
  'nombre': r.nombre,
  'precio': r.precio,
  'estado': r.estado,
  'esActiva': r.estado == 'activa',
}).toList();

print(paraUI);
```

---

## Ejercicio 7: Merge de dos fuentes

```dart
final sourceA = [
  Rifa(id: '1', nombre: 'TV 55"', precio: 10, estado: 'activa', categoria: 'electronica', creado: DateTime(2026, 6, 10), numerosVendidos: 45),
  Rifa(id: '8', nombre: 'Tablet', precio: 30, estado: 'activa', categoria: 'electronica', creado: DateTime(2026, 6, 28)),
];

final sourceB = [
  Rifa(id: '1', nombre: 'TV 55" Actualizada', precio: 12, estado: 'activa', categoria: 'electronica', creado: DateTime(2026, 6, 10)),
  Rifa(id: '9', nombre: 'Auriculares', precio: 7, estado: 'activa', categoria: 'accesorios', creado: DateTime(2026, 6, 30)),
];

// Merge: sourceB sobrescribe a sourceA cuando hay mismo ID
// Resultado: deben estar: TV actualizada (de B), Tablet (de A), Auriculares (de B)

final merged = <String, Rifa>{};
for (final r in [...sourceA, ...sourceB]) {
  merged[r.id] = r; // B sobrescribe A automáticamente
}
final resultado = merged.values.toList();
print(resultado.map((r) => '${r.id}: ${r.nombre}').toList());
```

---

## Ejercicio 8: Pipeline completo (filtro + transform + orden + limit)

```dart
// De todas las rifas activas en categoría 'electronica',
// ordénalas por precio ascendente, toma las 2 más baratas
// y devuelve solo sus nombres

final resultado = rifas
    .where((r) => r.estado == 'activa' && r.categoria == 'electronica')
    .toList()
  ..sort((a, b) => a.precio.compareTo(b.precio));

final nombres = resultado.take(2).map((r) => r.nombre).toList();
print(nombres); // [TV 55", PlayStation]
```

---

## Ejercicio 9: Validación de formulario

```dart
// Un formulario recibe estos campos. Valida:
// - nombre no vacío
// - precio > 0
// - estado debe ser uno válido: 'activa', 'cancelada', 'finalizada'

final formData = {
  'nombre': '',
  'precio': -5.0,
  'estado': 'unknown',
};

final estadosValidos = {'activa', 'cancelada', 'finalizada'};

final errores = <String>[];

if ((formData['nombre'] as String).isEmpty) {
  errores.add('nombre: obligatorio');
}
if ((formData['precio'] as double) <= 0) {
  errores.add('precio: debe ser > 0');
}
if (!estadosValidos.contains(formData['estado'])) {
  errores.add('estado: inválido');
}

print(errores); // 3 errores
```

---

## Ejercicio 10: Estadísticas avanzadas

```dart
// Calcula y devuelve:
// 1. Precio promedio de rifas activas
// 2. Rifa con más números vendidos
// 3. Categoría con más rifas

final activas = rifas.where((r) => r.estado == 'activa').toList();

// Precio promedio
final precioPromedio = activas.fold(0.0, (acc, r) => acc + r.precio) / activas.length;

// Rifa con más ventas
final masVendida = rifas.fold(rifas.first, (Rifa max, r) =>
  r.numerosVendidos > max.numerosVendidos ? r : max);

// Categoría con más rifas
final porCategoria = rifas.fold<Map<String, int>>({}, (map, r) {
  map[r.categoria] = (map[r.categoria] ?? 0) + 1;
  return map;
});
final catMasRifas = porCategoria.entries
    .reduce((a, b) => a.value > b.value ? a : b)
    .key;

print('Precio promedio activas: $precioPromedio');
print('Más vendida: ${masVendida.nombre}');
print('Categoría con más rifas: $catMasRifas');
```

---

## 🏁 Fin de nivel intermedio

Pasa a los [ejercicios avanzados](./10-ejercicios-avanzados.md) cuando hayas completado todos.
