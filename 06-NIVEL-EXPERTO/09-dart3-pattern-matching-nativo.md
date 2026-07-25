# 09: Dart 3 Pattern Matching Nativo

> Dart 3 trae pattern matching al lenguaje. No necesitas librerías externas para expresiones switch complejas.

---

## Switch expressions (Dart 3)

```dart
// Antes (Dart 2)
String descripcion(Animal animal) {
  if (animal is Perro) {
    return 'Perro: ${animal.nombre}';
  } else if (animal is Gato) {
    return 'Gato: ${animal.nombre}';
  } else {
    return 'Desconocido';
  }
}

// Dart 3: Switch expression
String descripcion(Animal animal) => switch (animal) {
  Perro(nombre: final n) => 'Perro: $n',
  Gato(nombre: final n)  => 'Gato: $n',
  _                      => 'Desconocido',
};
```

---

## Pattern matching con guarded patterns

```dart
// Filtrar por condiciones
String clasificar(int edad) => switch (edad) {
  < 0  => 'Inválido',
  0    => 'Recién nacido',
  < 13 => 'Niño',
  < 18 => 'Adolescente',
  < 65 => 'Adulto',
  _    => 'Mayor',
};
```

---

## Destructuring de lists y records

```dart
// Destructurar una lista
void procesar(List<int> nums) {
  switch (nums) {
    case [final a, final b]:
      print('Dos elementos: $a, $b');
    case [final a, ...final resto]:
      print('Primero: $a, resto: $resto');
    case []:
      print('Vacía');
  }
}

// Destructurar records
(String nombre, int edad) persona = ('Ana', 25);

switch (persona) {
  case (final n, final e) when e >= 18:
    print('$n es mayor de edad');
  case (final n, final e):
    print('$n es menor de edad');
}
```

---

## Pattern matching con sealed classes

```dart
sealed class Resultado<T> {
  const Resultado();
}

class Exito<T> extends Resultado<T> {
  final T dato;
  const Exito(this.dato);
}

class Error<T> extends Resultado<T> {
  final String mensaje;
  const Error(this.mensaje);
}

// Usar con pattern matching
String mostrar<T>(Resultado<T> resultado) => switch (resultado) {
  Exito(dato: final d) => 'Éxito: $d',
  Error(mensaje: final m) => 'Error: $m',
};
```

---

## Record patterns en parámetros

```dart
// Función que retorna record
(int, int) minMax(List<int> nums) {
  return (nums.reduce((a, b) => a < b ? a : b),
          nums.reduce((a, b) => a > b ? a : b));
}

// Destructurar al recibir
final (min, max) = minMax([3, 1, 4, 1, 5, 9]);
print('Mínimo: $min, Máximo: $max');
```

---

## Ejercicio práctico

```dart
// Convierte esto a Dart 3 pattern matching:
String descripcion(Object obj) {
  if (obj is String) {
    if (obj.isEmpty) return 'String vacío';
    return 'String: $obj';
  } else if (obj is int) {
    if (obj < 0) return 'Negativo';
    if (obj == 0) return 'Cero';
    return 'Positivo';
  } else if (obj is List) {
    return 'Lista de ${obj.length} elementos';
  }
  return 'Otro tipo';
}

// Tu versión con switch expression aquí:
```

<details>
<summary>Ver solución</summary>

```dart
String descripcion(Object obj) => switch (obj) {
  String s when s.isEmpty => 'String vacío',
  String s               => 'String: $s',
  int i when i < 0       => 'Negativo',
  0                      => 'Cero',
  int i                  => 'Positivo',
  List l                 => 'Lista de ${l.length} elementos',
  _                      => 'Otro tipo',
};
```
</details>

---

**Siguiente:** [10-debugging-build-runner.md](./10-debugging-build-runner.md)
