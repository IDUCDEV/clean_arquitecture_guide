# Dart 3: Sealed Classes

> Las sealed classes permiten modelar estados y variantes de forma segura. El compilador te obliga a manejar todos los casos.

---

## 1. ¿Qué son las sealed classes?

Una sealed class es una clase cuyas subclases están **restringidas al mismo archivo**. Esto le da al compilador información completa sobre todas las variantes posibles.

```dart
// ANTES de Dart 3 (sin sealed):
abstract class Estado {}
class Cargando extends Estado {}
class Exito extends Estado { final String datos; }
class Error extends Estado { final String mensaje; }

// El compilador NO sabe qué subclases existen.
// Debes usar 'default' o castear manualmente.

// DESPUÉS de Dart 3 (con sealed):
sealed class Estado {}
class Cargando extends Estado {}
class Exito extends Estado { final String datos; }
class Error extends Estado { final String mensaje; }

// El compilador SABE todas las variantes.
// Si olvidas manejar una, el código NO compila.
```

---

## 2. Por qué existen

### El problema que resuelven

```dart
// Sin sealed: el compilador no puede verificar que cubres todos los casos
abstract class Resultado {}

class Exito extends Resultado { final String data; }
class Error extends Resultado { final String message; }
class Cargando extends Resultado {}

String interpretar(Resultado r) {
  if (r is Exito) return r.data;
  if (r is Error) return r.message;
  // ¿Y si mañana agregamos 'Cargando'? El compilador no avisa.
  return 'desconocido'; // ← Bug silencioso
}
```

### La solución con sealed

```dart
sealed class Resultado {}

class Exito extends Resultado { final String data; }
class Error extends Resultado { final String message; }
class Cargando extends Resultado {}

String interpretar(Resultado r) {
  // ERROR DE COMPILACIÓN: El switch no cubre 'Cargando'
  return switch (r) {
    Exito(data: final d) => d,
    Error(message: final m) => m,
    // FALTA: Cargando → el compilador avisa
  };
}
```

---

## 3. Sintaxis básica

### Declaración

```dart
sealed class Animal {
  // Las sealed classes pueden tener:
  // - Constructores
  // - Métodos
  // - Propiedades
  // - Pero NO pueden ser instanciadas directamente
}

class Perro extends Animal {
  final String nombre;
  Perro(this.nombre);
}

class Gato extends Animal {
  final String nombre;
  Gato(this.nombre);
}

class Pez extends Animal {
  final String nombre;
  Pez(this.nombre);
}
```

### Reglas

```
┌─────────────────────────────────────────────────────────────┐
│ REGLAS DE SEALED CLASSES                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ✅ Las subclases deben estar en el MISMO ARCHIVO           │
│ ✅ Las subclases pueden ser abstract, final, o no          │
│ ✅ La sealed class NO puede ser instanciada directamente    │
│ ✅ Las subclases pueden tener constructores con parámetros │
│ ✅ Puedes tener métodos en la sealed class                  │
│                                                             │
│ ❌ NO puedes crear subclases en otro archivo                │
│ ❌ NO puedes instanciar la sealed class directamente        │
│ ❌ NO puede ser mixin                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Patrones de uso comunes

### Patrón 1: Estados de UI (el más común en Flutter)

```dart
sealed class AuthState {}

class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class Authenticated extends AuthState {
  final String userId;
  final String email;
  Authenticated({required this.userId, required this.email});
}
class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}
```

### Patrón 2: Resultado de operación

```dart
sealed class Result<T> {}

class Success<T> extends Result<T> {
  final T data;
  Success(this.data);
}

class Failure<T> extends Result<T> {
  final String message;
  final int? statusCode;
  Failure(this.message, {this.statusCode});
}

class Loading<T> extends Result<T> {}
```

### Patrón 3: Eventos de usuario

```dart
sealed class FormEvent {}

class Submitted extends FormEvent {
  final String nombre;
  final String email;
  Submitted({required this.nombre, required this.email});
}
class FieldChanged extends FormEvent {
  final String field;
  final String value;
  FieldChanged({required this.field, required this.value});
}
class Reset extends FormEvent {}
```

### Patrón 4: Forma geométrica (clásico)

```dart
sealed class Forma {}

class Circulo extends Forma {
  final double radio;
  Circulo(this.radio);
}

class Rectangulo extends Forma {
  final double base;
  final double altura;
  Rectangulo(this.base, this.altura);
}

class Triangulo extends Forma {
  final double base;
  final double altura;
  Triangulo(this.base, this.altura);
}

// El compilador garantiza que cubres todas las formas
double calcularArea(Forma f) {
  return switch (f) {
    Circulo(radio: final r) => 3.14159 * r * r,
    Rectangulo(base: final b, altura: final a) => b * a,
    Triangulo(base: final b, altura: final a) => 0.5 * b * a,
  };
}
```

---

## 5. Sealed vs Enum vs Abstract

```
┌─────────────────────────────────────────────────────────────────┐
│                  ¿CUÁNDO USAR CADA UNO?                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ENUM                                                          │
│  → Cuando los valores NO tienen datos asociados                │
│  → Ejemplo: Color.rojo, Color.azul                             │
│  → Ejemplo: EstadoCarga.cargando, .exito, .error               │
│                                                                 │
│  SEALED CLASS                                                   │
│  → Cuando CADA variante tiene datos diferentes                 │
│  → Ejemplo: Resultado.tiene datos, Error tiene mensaje         │
│  → Ejemplo: EstadoCarga.cargando NO tiene datos,              │
│             Exito.sí tiene datos                               │
│                                                                 │
│  ABSTRACT CLASS                                                 │
│  → Cuando necesitas herencia múltiple o mixins                 │
│  → Cuando las subclases pueden estar en otros archivos         │
│  → Ejemplo: Widget (Flutter) — puede extenderse desde anywhere │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ejemplo comparativo

```dart
// ENUM: Simple, sin datos
enum Color { rojo, azul, verde }

// SEALED: Variantes con datos
sealed class Evento {
  const Evento();
}
class Click extends Evento {
  final double x, y;
  Click(this.x, this.y);
}
class Presionar extends Evento {
  final String tecla;
  Presionar(this.tecla);
}
class Soltar extends Evento {}
```

---

## 6. Sealed en Clean Architecture

### Domain Layer — Estados de Use Case

```dart
// lib/domain/entities/resultado_busqueda.dart

sealed class ResultadoBusqueda {}

class BusquedaExitosa extends ResultadoBusqueda {
  final List<Producto> productos;
  final int total;
  BusquedaExitosa({required this.productos, required this.total});
}

class BusquedaVacia extends ResultadoBusqueda {}

class BusquedaError extends ResultadoBusqueda {
  final String mensaje;
  BusquedaError(this.mensaje);
}
```

### Domain Layer — Estados de Repository

```dart
// lib/domain/repositories/producto_repository.dart

abstract class ProductoRepository {
  Future<ResultadoBusqueda> buscarProductos(String query);
}
```

### Presentation Layer — Controller (BLoC/Cubit)

```dart
// lib/presentation/controllers/busqueda_controller.dart

void onBuscar(String query) async {
  emitstate(BusquedaCargando());

  final resultado = await _buscarProductos(query);

  // El compilador garantiza que manejamos TODOS los casos
  emitstate(switch (resultado) {
    BusquedaExitosa(productos: final p) => BusquedaExito(p),
    BusquedaVacia() => BusquedaSinResultados(),
    BusquedaError(mensaje: final m) => BusquedaFallida(m),
  });
}
```

---

## 7. Ejercicio práctico

### Tarea
Crea un sealed class para representar el estado de una operación de descarga:

```dart
sealed class DescargaEstado {
  // Implementa estas variantes:
  // - DescargaInicial
  // - DescargaProgreso (con double porcentaje)
  // - DescargaCompleta (con String rutaArchivo)
  // - DescargaError (con String mensaje, Exception? excepcion)
}

// Luego escribe un switch que maneje todos los casos
String interpretarEstado(DescargaEstado estado) {
  // Tu código aquí
}
```

### Solución

```dart
sealed class DescargaEstado {}

class DescargaInicial extends DescargaEstado {}

class DescargaProgreso extends DescargaEstado {
  final double porcentaje;
  DescargaProgreso(this.porcentaje);
}

class DescargaCompleta extends DescargaEstado {
  final String rutaArchivo;
  DescargaCompleta(this.rutaArchivo);
}

class DescargaError extends DescargaEstado {
  final String mensaje;
  final Exception? excepcion;
  DescargaError(this.mensaje, {this.excepcion});
}

String interpretarEstado(DescargaEstado estado) {
  return switch (estado) {
    DescargaInicial() => 'Listo para descargar',
    DescargaProgreso(porcentaje: final p) => 'Descargando: ${(p * 100).toInt()}%',
    DescargaCompleta(rutaArchivo: final r) => 'Completado: $r',
    DescargaError(mensaje: final m) => 'Error: $m',
  };
}
```

---

## 8. Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "The type 'X' is not exhaustively matched" | Olvidaste manejar una variante en switch | Agrega la variante faltante o usa `default` |
| "Sealed classes can't be instantiated" | Intentas hacer `SealedClass()` | Crea una subclase y usa esa |
| "Subtypes must be in the same library" | Subclase en otro archivo | Mueve la subclase al mismo archivo |
| "Sealed class can't be a mixin" | Intentas `sealed mixin` | Usa `abstract class` con `mixin` por separado |

---

**Siguiente:** [13-dart3-pattern-matching.md](./13-dart3-pattern-matching.md) — Pattern matching con switch expressions
