# Dart 3: Pattern Matching

> Pattern matching en Dart 3 permite destructurar, filtrar y transformar datos directamente en expresiones switch. Es más poderoso que los if/else tradicionales.

---

## 1. ¿Qué es pattern matching?

Pattern matching es una forma de **verificar y extraer datos** de una expresión en una sola línea. En lugar de escribir múltiples if/else con casts, puedes describir el patrón que buscas.

```dart
// ANTES de Dart 3 (sin pattern matching):
String describirAnimal(dynamic animal) {
  if (animal is Perro) {
    return 'Perro: ${animal.nombre}';
  } else if (animal is Gato) {
    return 'Gato: ${animal.nombre}';
  } else if (animal is Pez) {
    return 'Pez: ${animal.nombre}';
  }
  return 'Desconocido';
}

// DESPUÉS de Dart 3 (con pattern matching):
String describirAnimal(Animal animal) {
  return switch (animal) {
    Perro(nombre: final n) => 'Perro: $n',
    Gato(nombre: final n)  => 'Gato: $n',
    Pez(nombre: final n)   => 'Pez: $n',
  };
}
```

---

## 2. Tipos de patterns

### 2.1 Constant patterns

```dart
// Comparar con valores constantes
String describir(int numero) {
  return switch (numero) {
    0 => 'Cero',
    1 => 'Uno',
    2 => 'Dos',
    _ => 'Otro',
  };
}

// Con strings
String nivel(String nivel) {
  return switch (nivel) {
    'junior' => '0-2 años',
    'mid' => '2-5 años',
    'senior' => '5+ años',
    _ => 'No definido',
  };
}
```

### 2.2 Type patterns (con is)

```dart
// Verificar tipo y extraer en una línea
String manejar(dynamic valor) {
  return switch (valor) {
    int(n) => 'Entero: $n',
    String(s) => 'Texto: $s',
    List(a) => 'Lista de ${a.length} elementos',
    _ => 'Otro tipo',
  };
}
```

### 2.3 Destructuring patterns

```dart
// Extraer campos de un objeto
class Persona {
  final String nombre;
  final int edad;
  final String ciudad;
  Persona(this.nombre, this.edad, this.ciudad);
}

String descripcion(Persona p) {
  return switch (p) {
    Persona(nombre: final n, edad: final e, ciudad: 'Caracas') => '$n de Caracas, $e años',
    Persona(nombre: final n, edad: final e) when e > 18 => '$n es mayor de edad',
    Persona(nombre: final n) => '$n',
  };
}

// Extraer elementos de una lista
String primerElemento(List<int> lista) {
  return switch (lista) {
    [int primero, ...] => 'Primero: $primero',
    [] => 'Vacía',
  };
}

// Extraer de un Map
String buscar(Map<String, dynamic> map) {
  return switch (map) {
    {'nombre': String n, 'edad': int e} => '$n tiene $e años',
    {'nombre': String n} => '$n sin edad',
    _ => 'No encontrado',
  };
}
```

### 2.4 Guard clauses (when)

```dart
// Agregar condiciones extra al patrón
String evaluar(int nota) {
  return switch (nota) {
    >= 90 => 'A',
    >= 80 => 'B',
    >= 70 => 'C',
    >= 60 => 'D',
    _ => 'F',
  };
}

// Con sealed classes
sealed class Resultado<T> {}

class Success<T> extends Resultado<T> {
  final T data;
  Success(this.data);
}

class Failure<T> extends Resultado<T> {
  final String message;
  Failure(this.message);
}

String manejar(Resultado<int> resultado) {
  return switch (resultado) {
    Success(data: > 100) => 'Éxito con dato grande',
    Success(data: final d) => 'Éxito: $d',
    Failure(message: 'timeout') => 'Tiempo agotado',
    Failure(message: final m) => 'Error: $m',
  };
}
```

---

## 3. Switch expressions vs Switch statements

```dart
// SWITCH EXPRESSION (retorna un valor)
// Usa => y cada caso es una expresión
String resultado = switch (animal) {
  Perro(nombre: final n) => 'Perro: $n',
  Gato(nombre: final n)  => 'Gato: $n',
  _ => 'Otro',
};

// SWITCH STATEMENT (ejecuta código)
// Usa : y puede tener múltiples líneas
switch (evento) {
  case Click(x: final x, y: final y):
    print('Clic en ($x, $y)');
    // más código aquí...
  case Presionar(tecla: final t):
    print('Tecla: $t');
  case Soltar():
    print('Soltado');
}
```

---

## 4. Patrones combinados

### AND patterns

```dart
String evaluar(int valor) {
  return switch (valor) {
    >= 0 && <= 100 => 'Válido',
    < 0 => 'Negativo',
    _ => 'Mayor a 100',
  };
}
```

### OR patterns

```dart
String letra(String c) {
  return switch (c) {
    'a' || 'e' || 'i' || 'o' || 'u' => 'Vocal',
    _ => 'Consonante',
  };
}
```

### Nested patterns

```dart
class Direccion {
  final String ciudad;
  final String pais;
  Direccion(this.ciudad, this.pais);
}

class Persona {
  final String nombre;
  final Direccion direccion;
  Persona(this.nombre, this.direccion);
}

String origen(Persona p) {
  return switch (p) {
    Persona(direccion: Direccion(pais: 'Venezuela')) => 'Venezolano',
    Persona(direccion: Direccion(pais: 'Colombia')) => 'Colombiano',
    Persona(nombre: final n) => 'Otro: $n',
  };
}
```

---

## 5. Ejemplos en Flutter

### Manejo de estados de UI

```dart
sealed class AuthState {}

class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class Authenticated extends AuthState {
  final String nombre;
  Authenticated(this.nombre);
}
class AuthError extends AuthState {
  final String message;
  AuthError(this.message);
}

// En un widget
Widget build(BuildContext context) {
  return BlocBuilder<AuthCubit, AuthState>(
    builder: (context, state) {
      return switch (state) {
        AuthInitial() => const LoginView(),
        AuthLoading() => const CircularProgressIndicator(),
        Authenticated(nombre: final n) => HomeView(nombre: n),
        AuthError(message: final m) => ErrorView(mensaje: m),
      };
    },
  );
}
```

### Parsing de API

```dart
Map<String, dynamic> data = {'tipo': 'producto', 'nombre': 'Laptop', 'precio': 999.99};

String procesar(Map<String, dynamic> json) {
  return switch (json) {
    {'tipo': 'producto', 'nombre': String n, 'precio': double p} => 
      'Producto: $n (\$${p.toStringAsFixed(2)})',
    {'tipo': 'usuario', 'nombre': String n} => 
      'Usuario: $n',
    _ => 
      'Formato no reconocido',
  };
}
```

---

## 6. Ejercicio práctico

### Tarea
Implementa una función que procese una lista de eventos de usuario:

```dart
sealed class Evento {}

class Click extends Evento {
  final double x, y;
  Click(this.x, this.y);
}

class PresionarTecla extends Evento {
  final String tecla;
  PresionarTecla(this.tecla);
}

class Desplazar extends Evento {
  final double deltaX, deltaY;
  Desplazar(this.deltaX, this.deltaY);
}

class Soltar extends Evento {}

// Implementa:
String procesarEvento(Evento evento) { ... }
List<String> procesarEventos(List<Evento> eventos) { ... }
```

### Solución

```dart
String procesarEvento(Evento evento) {
  return switch (evento) {
    Click(x: final x, y: final y) => 'Clic en ($x, $y)',
    PresionarTecla(tecla: final t) when t == 'Enter' => 'Confirmar',
    PresionarTecla(tecla: final t) => 'Tecla: $t',
    Desplazar(deltaX: 0, deltaY: 0) => 'Sin movimiento',
    Desplazar(deltaX: final dx, deltaY: final dy) => 'Desplazar ($dx, $dy)',
    Soltar() => 'Soltado',
  };
}

List<String> procesarEventos(List<Evento> eventos) {
  return eventos.map(procesarEvento).toList();
}
```

---

## 7. Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "Not exhaustively matched" | Olvidaste un caso en el switch | Agrega el caso o usa `_` |
| Pattern too complex | Demasiados patrones anidados | Divide en funciones más pequeñas |
| `when` clause with wrong type | Condición incompatible con el tipo | Verifica el tipo antes del `when` |

---

**Siguiente:** [14-dart3-records.md](./14-dart3-records.md) — Records: tuplas nativas en Dart
