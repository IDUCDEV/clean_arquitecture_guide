# Dart 3: Records (Tuplas Nativas)

> Los records son tipos anónimos que pueden contener múltiples campos. Son la forma nativa de retornar múltiples valores en Dart 3.

---

## 1. ¿Qué son los records?

Un record es una colección de valores con tipos estáticos. Es como una tupla de otros lenguajes.

```dart
// ANTES de Dart 3 (sin records):
(List<String> nombres, int total) obtenerDatos() {
  return ['Ana', 'Luis', 'María'], 3; // No se puede retornar dos valores
}

// Necesitabas crear una clase o usar Map
Map<String, dynamic> obtenerDatos() {
  return {'nombres': ['Ana', 'Luis'], 'total': 3};
}

// DESPUÉS de Dart 3 (con records):
(List<String> nombres, int total) obtenerDatos() {
  return (['Ana', 'Luis', 'María'], 3); // Retorno directo
}

// Uso:
final (nombres, total) = obtenerDatos();
print('$total usuarios: $nombres');
```

---

## 2. Sintaxis básica

### Declaración

```dart
// Record positional (con tipos explícitos)
(int, String) registro = (42, 'texto');

// Record named (con nombres de campo)
({int id, String nombre}) usuario = (id: 1, nombre: 'Ana');

// Record mixto (positional + named)
(int id, String nombre, {bool activo}) persona = (1, 'Luis', activo: true);

// Tipo completo
(String, int, {bool esAdmin}) usuarioCompleto;
```

### Destructuring

```dart
// Destructuring positional
var (id, nombre) = (1, 'Ana');
print('$id: $nombre');

// Destructuring named
var (:id, :nombre) = (id: 1, nombre: 'Ana');
print('$id: $nombre');

// Destructuring parcial (ignorar campos)
var (_, nombre) = (1, 'Ana');
print(nombre);

// Destructuring con alias
var (userId: id, userName: name) = (userId: 1, userName: 'Ana');
```

---

## 3. Tipos de records

### Positional records

```dart
// Los campos se identifican por posición
(int, String) persona = (1, 'Ana');

// Acceso por posición
print(persona.$1); // 1
print(persona.$2); // 'Ana'

// Destructuring
var (id, nombre) = persona;
```

### Named records

```dart
// Los campos tienen nombres
({int id, String nombre}) persona = (id: 1, nombre: 'Ana');

// Acceso por nombre
print(persona.id); // 1
print(persona.nombre); // 'Ana'

// Destructuring con nombres
var (:id, :nombre) = persona;
```

### Mixed records

```dart
// Combinación de positional y named
(int id, String nombre, {bool activo}) usuario = (1, 'Ana', activo: true);

// Acceso
print(usuario.$1);     // 1 (positional)
print(usuario.nombre); // 'Ana' (named)
print(usuario.activo); // true (named)
```

---

## 4. Records en funciones

### Retorno múltiple

```dart
// Función que retorna un record
(int minimo, int maximo) encontrarLimites(List<int> numeros) {
  return (numeros.reduce((a, b) => a < b ? a : b),
          numeros.reduce((a, b) => a > b ? a : b));
}

// Uso
final (min, max) = encontrarLimites([3, 1, 4, 1, 5, 9]);
print('Mínimo: $min, Máximo: $max');
```

### Retorno con valores opcionales

```dart
// Records son ideales para resultados con datos opcionales
({bool success, String? message, int? statusCode}) resultado;

resultado = (success: true, message: 'OK', statusCode: 200);
resultado = (success: false, message: 'Error', statusCode: 404);
```

### Combinando con Pattern Matching

```dart
sealed class Resultado<T> {}

class Success<T> extends Resultado<T> {
  final T data;
  Success(this.data);
}

class Failure<T> extends Resultado<T> {
  final String message;
  Failure(this.message);
}

// Función que retorna record con resultado
({bool ok, String? error}) procesar(int valor) {
  return switch (valor) {
    > 0 => (ok: true, error: null),
    0 => (ok: false, error: 'No puede ser cero'),
    _ => (ok: false, error: 'Negativo no permitido'),
  };
}

// Uso
final (ok: success, error: msg) = procesar(5);
if (success) {
  print('Procesado');
} else {
  print('Error: $msg');
}
```

---

## 5. Records en lists y maps

```dart
// Lista de records
List<(String nombre, int edad)> personas = [
  ('Ana', 25),
  ('Luis', 30),
  ('María', 22),
];

// Filtrar y transformar
var mayores = personas.where((p) => p.$2 >= 25);
var nombres = personas.map((p) => p.$1);

// Map con records
Map<int, (String nombre, bool activo)> usuarios = {
  1: ('Ana', true),
  2: ('Luis', false),
};

// Encontrar usuario activo
var activo = usuarios.entries.firstWhere(
  (e) => e.value.$2,
  orElse: () => throw Exception('No hay activos'),
);
```

---

## 6. Records en Clean Architecture

### Retorno de Repository

```dart
// Antes: crear clase de retorno
class BusquedaResultado {
  final List<Producto> productos;
  final int total;
  final bool hayMas;
  BusquedaResultado({required this.productos, required this.total, required this.hayMas});
}

// Ahora: record directo
(List<Producto> productos, {int total, bool hayMas}) buscarProductos(String query) {
  // ...
  return (productos, total: total, hayMas: hayMas);
}

// Uso
final (productos, total: total, hayMas: hay) = buscarProductos('laptop');
```

### Validation results

```dart
// Resultado de validación
({bool valido, List<String> errores}) validarFormulario({
  required String nombre,
  required String email,
  required int edad,
}) {
  final errores = <String>[];
  if (nombre.isEmpty) errores.add('Nombre requerido');
  if (!email.contains('@')) errores.add('Email inválido');
  if (edad < 18) errores.add('Debe ser mayor de edad');

  return (valido: errores.isEmpty, errores: errores);
}

// Uso
final result = validarFormulario(nombre: 'Ana', email: 'ana@test.com', edad: 25);
if (result.valido) {
  // Guardar
} else {
  for (final error in result.errores) {
    print(error);
  }
}
```

---

## 7. Records vs Clases

```
┌─────────────────────────────────────────────────────────────────┐
│              ¿CUÁNDO USAR CADA UNO?                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  RECORD                                                         │
│  → Retorno temporal de una función                              │
│  → Datos que no necesitan comportamiento                       │
│  → Agrupar 2-3 valores relacionados                            │
│  → Prototipos rápidos                                           │
│  → Ejemplo: (min, max) de una lista                            │
│                                                                 │
│  CLASE                                                          │
│  → Entidades de dominio                                         │
│  → Datos con comportamiento (métodos)                          │
│  → Cuando necesitas inmutabilidad con copyWith                  │
│  → Cuando el objeto se usa en múltiples lugares                │
│  → Ejemplo: Producto, Usuario, Pedido                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ejemplo comparativo

```dart
// RECORD: retorno de función (temporal, sin comportamiento)
(String nombre, int edad) obtenerInfo() {
  return ('Ana', 25);
}

// CLASE: entidad de dominio (con comportamiento, se reutiliza)
class Persona {
  final String nombre;
  final int edad;
  Persona(this.nombre, this.edad);

  bool get esMayorDeEdad => edad >= 18;
  Persona copyWith({String? nombre, int? edad}) {
    return Persona(nombre ?? this.nombre, edad ?? this.edad);
  }
}
```

---

## 8. Ejercicio práctico

### Tarea
Crea funciones que retornen records para resolver estos problemas:

```dart
// 1. Encontrar min y max de una lista
(int min, int max) minMax(List<int> numeros) { ... }

// 2. Contar elementos de una lista agrupados por condición
({int pares, int impares}) contarParesImpares(List<int> numeros) { ... }

// 3. Buscar un elemento y su índice
(int indice, bool encontrado) buscar(List<String> lista, String elemento) { ... }
```

### Solución

```dart
(int min, int max) minMax(List<int> numeros) {
  return (
    numeros.reduce((a, b) => a < b ? a : b),
    numeros.reduce((a, b) => a > b ? a : b),
  );
}

({int pares, int impares}) contarParesImpares(List<int> numeros) {
  return (
    pares: numeros.where((n) => n.isEven).length,
    impares: numeros.where((n) => n.isOdd).length,
  );
}

(int indice, bool encontrado) buscar(List<String> lista, String elemento) {
  final idx = lista.indexOf(elemento);
  return (idx, idx != -1);
}

// Uso
final (min, max) = minMax([3, 1, 4, 1, 5, 9]);
final (:pares, :impares) = contarParesImpares([1, 2, 3, 4, 5]);
final (indice, encontrado) = buscar(['a', 'b', 'c'], 'b');
```

---

## 9. Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Undefined named '$1'" | Intentas acceder a campo positional por nombre | Usa `.$1`, `.$2` o destructura |
| "Too many positional arguments" | Record tiene menos campos | Ajusta los tipos del record |
| "Missing named argument" | No proporcionas campo named requerido | Agrega el campo o hazlo opcional con `?` |

---

**Siguiente:** [15-dart3-ejercicios.md](./15-dart3-ejercicios.md) — Ejercicios integrando sealed + patterns + records
