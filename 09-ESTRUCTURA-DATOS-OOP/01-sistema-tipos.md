# 01 — Sistema de Tipos en Dart

> Antes de manipular datos, entiende cómo Dart **declara, infiere y restringe** los tipos. Esto es la base de todo.

---

## 🎯 Objetivos

- Diferenciar `var`, `final` y `const`
- Entender null safety (`?`, `!`, `late`)
- Usar genéricos `<T>` correctamente
- Conocer `dynamic` vs `Object` vs `Never`

---

## 1. `var` vs `final` vs `const`

```dart
// var: tipo inferido, REASIGNABLE
var nombre = 'Juan';      // String inferido
nombre = 'Pedro';          // ✅ ok
nombre = 42;               // ❌ Error: String != int

// final: tipo inferido, NO reasignable (runtime constant)
final apellido = 'Pérez';
apellido = 'García';       // ❌ Error: final no se reasigna

// const: COMPILE-TIME constant, inmutable
const pi = 3.1416;
const ahora = DateTime.now(); // ❌ Error: DateTime.now() no es compile-time
```

### 📊 ¿Cuándo usar cada uno?

| Situación | Usa |
|-----------|-----|
| Variable temporal en un método | `var` |
| Parámetro de función | Tipo explícito (`String name`) |
| Propiedad de clase que no cambia | `final` |
| Constante universal (PI, URLs base) | `const` |
| Valor que solo se asigna una vez pero tarde | `late final` |

---

## 2. Null Safety — `?` `!` `late`

### El problema que resuelve

```dart
// ANTES de null safety (Dart <2.12):
String nombre = null;   // ❌ Crash en runtime

// DESPUÉS de null safety:
String? nombre = null;  // ✅ Explícitamente nullable
String apellido = null; // ❌ Error: non-nullable
```

### Los 3 operadores clave

```dart
String? nullable = obtenerNombre(); // podría ser null

// 1. ?. — acceso condicional (si es null, devuelve null)
final longitud = nullable?.length;   // int? (nullable)

// 2. ! — assertion (tú SABES que no es null)
final longitud2 = nullable!.length;  // int (crash si es null)

// 3. ?? — operador de coalescencia (default si null)
final nombre = nullable ?? 'Invitado';
```

### `late` — Inicialización diferida

```dart
class Usuario {
  late final String id;  // se asigna después del constructor

  void init() {
    id = generarId();    // primera (y única) asignación
  }
}
```

> ⚠️ **Regla**: `late` solo cuando es unavoidable (ej: dependency injection, controllers). Prefiere constructores con `required`.

---

## 3. Genéricos `<T>`

Los genéricos te permiten escribir código que funciona con **cualquier tipo**.

### Sintaxis básica

```dart
class Caja<T> {
  final T contenido;
  Caja(this.contenido);
}

final cajaString = Caja<String>('hola');
final cajaInt = Caja<int>(42);

// Inferencia: Dart deduce el tipo
final caja = Caja('hola'); // Caja<String>
```

### Genéricos con restricciones

```dart
// Solo acepta tipos numéricos
class Calculadora<T extends num> {
  T suma(T a, T b) => a + b as T;
}

final calc = Calculadora<int>();
calc.suma(1, 2); // ✅
```

### En colecciones

```dart
List<String> nombres = ['Ana', 'Bob'];     // solo Strings
Map<String, int> edades = {'Ana': 30};     // key String, value int

// ¡No hagas esto!
List lista = ['Ana', 42, true]; // List<dynamic> — pierdes tipo
```

---

## 4. `dynamic` vs `Object` vs `Never`

```dart
// dynamic: DESACTIVA el type-checking (peligroso)
dynamic x = 'hola';
x = 42;          // ✅
x.metodoInexistente(); // ✅ en compilación, ❌ en runtime

// Object: tipo base de TODOS los tipos (seguro)
Object y = 'hola';
y = 42;           // ✅
y.length;         // ❌ Error: Object no tiene .length
(y as String).length; // ✅ casteo explícito

// Never: tipo que NUNCA se alcanza (retorno de funciones que siempre lanzan)
Never lanzarError() {
  throw Exception('Esto nunca retorna');
}
```

### 🏋️ Mini-práctica

```dart
// 1. ¿Qué imprime cada uno?
var a = 'Hola';
final b = 'Mundo';
const c = 'Dart';

a = 'Adiós';        // ✅ o ❌?
b = 'Adiós';        // ✅ o ❌?

// 2. Null safety
String? nombre = null;
print(nombre?.length);     // ¿Qué imprime?
print(nombre!.length);     // ¿Qué imprime?

// 3. Genéricos
List<String> items = ['a', 'b'];
items.add(42);             // ✅ o ❌?

// Respuestas: (1) ✅, ❌; (2) null, crash; (3) ❌
```

---

## ✅ Checklist

- [ ] Diferencio `var`/`final`/`const` y sé cuándo usar cada uno
- [ ] Entiendo `?` (nullable), `!` (assert), `??` (default)
- [ ] Sé qué hace `late` y sus riesgos
- [ ] Puedo escribir clases genéricas con `<T>` y restricciones `extends`
- [ ] Sé por qué `dynamic` es peligroso y `Object` es seguro

---

## 📚 Referencias

- [Dart | Language tour](https://dart.dev/language) — Recorrido completo por el lenguaje Dart
- [Dart | Collections](https://dart.dev/language/collections) — Documentación de List, Set, Map
- [Dart | Records y patterns](https://dart.dev/language/records) — Features modernos de Dart 3

---

**Siguiente**: [02-colecciones-fundamentos.md](./02-colecciones-fundamentos.md) — List, Set, Map

**Práctica extra**: Abre [Dartpad](https://dartpad.dev) y escribe 5 ejemplos combinando `?`, `!`, `??`.
