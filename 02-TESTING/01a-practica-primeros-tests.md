# 🏋️ 01a: Práctica - Primeros Tests

> **¿De qué trata esta práctica?** De escribir tus primeros tests siguiendo el patrón AAA. Vamos paso a paso, sin prisas.

---

## 📋 Ejercicios

- [Ejercicio 1: Test función matemática básica](#ejercicio-1-test-función-matemática-básica)
- [Ejercicio 2: Test con excepciones](#ejercicio-2-test-con-excepciones)
- [Ejercicio 3: Test con grupos y casos edge](#ejercicio-3-test-con-grupos-y-casos-edge)
- [Ejercicio 4: Test con objetos complejos](#ejercicio-4-test-con-objetos-complejos)

---

## 🎬 Antes de Empezar

Asegúrate de tener:
1. ✅ Dependencias instaladas (`flutter pub get`)
2. ✅ Estructura de carpetas creada
3. ✅ Ganas de equivocarte (es parte del aprendizaje)

---

## Ejercicio 1: Test Función Matemática Básica

### 📝 Escenario

Tienes una calculadora simple y quieres verificar que las operaciones básicas funcionan. Crea una función `add` y sus tests.

### ✅ Paso 1: Crea la estructura de carpetas

```bash
# En la raíz de tu proyecto Flutter
mkdir -p test/core/utils
```

### ✅ Paso 2: Crea el archivo con la función

Crea el archivo `lib/features/core/utils/calculator.dart`:

```dart
// lib/features/core/utils/calculator.dart

/// Suma dos números
int add(int a, int b) => a + b;

/// Resta dos números
int subtract(int a, int b) => a - b;

/// Multiplica dos números
int multiply(int a, int b) => a * b;

/// Divide dos números (puede lanzar excepción)
double divide(double a, double b) {
  if (b == 0) {
    throw ArgumentError('Cannot divide by zero');
  }
  return a / b;
}
```

### ✅ Paso 3: Crea el archivo de test

```bash
touch test/core/utils/calculator_test.dart
```

### ✅ Paso 4: Escribe el primer test - Suma de positivos

Abre `test/core/utils/calculator_test.dart` y escribe:

```dart
// test/core/utils/calculator_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/utils/calculator.dart';

void main() {
  group('Calculator', () {
    
    group('add', () {
      // TU PRIMER TEST AQUÍ
      test('should add two positive numbers', () {
        // ═══════════════════════════════════════════════════════════
        // ARRANGE: Preparamos los datos
        // ═══════════════════════════════════════════════════════════
        const a = 2;
        const b = 3;
        
        // ═══════════════════════════════════════════════════════════
        // ACT: Ejecutamos la función
        // ═══════════════════════════════════════════════════════════
        final result = add(a, b);
        
        // ═══════════════════════════════════════════════════════════
        // ASSERT: Verificamos el resultado
        // ═══════════════════════════════════════════════════════════
        expect(result, equals(5));
      });
    });
  });
}
```

### ✅ Paso 5: Ejecuta el test

```bash
flutter test test/core/utils/calculator_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +1: All tests passed!
```

### ✅ Paso 6: Añade más tests de suma

Ahora añade estos tests al grupo `add`:

```dart
group('add', () {
  test('should add two positive numbers', () {
    // ... ya hecho arriba
    expect(add(2, 3), equals(5));
  });
  
  // AÑADE ESTOS:
  
  test('should return same number when adding zero', () {
    expect(add(5, 0), equals(5));
  });
  
  test('should add negative numbers', () {
    expect(add(-2, -3), equals(-5));
  });
  
  test('should add positive and negative', () {
    expect(add(5, -3), equals(2));
  });
});
```

### ✅ Paso 7: Ejecuta todos los tests

```bash
flutter test test/core/utils/calculator_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +4: All tests passed!
```

---

## Ejercicio 2: Test con Excepciones

### 📝 Escenario

La función `divide` lanza una excepción cuando intentas dividir por cero. Necesitas verificar que la excepción se lanza correctamente.

### ✅ Paso 1: Añade tests de división

En el mismo archivo, añade un nuevo grupo:

```dart
group('divide', () {
  test('should divide correctly', () {
    // Arrange
    const a = 10.0;
    const b = 2.0;
    
    // Act
    final result = divide(a, b);
    
    // Assert
    expect(result, equals(5.0));
  });
  
  // ESTE ES EL NUEVO - Test de excepción
  test('should throw ArgumentError when dividing by zero', () {
    // Arrange - no hay nada que preparar
    
    // Act & Assert - todo en una línea
    expect(
      () => divide(10, 0),
      throwsA(isA<ArgumentError>()),
    );
  });
});
```

### 🤔 ¿Por qué usamos `() =>`?

Las excepciones se capturan con una función lambda:

```dart
expect(
  () => divide(10, 0),  // Función que va a lanzar
  throwsA(...),          // Verifica que lanza algo
);
```

Sin `()` tendrías:
```dart
expect(divide(10, 0), ...)  // ❌ Error! La excepción se lanzaría antes de expect
```

### ✅ Paso 2: Ejecuta los tests

```bash
flutter test test/core/utils/calculator_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +6: All tests passed!
```

---

## Ejercicio 3: Test con Grupos y Casos Edge

### 📝 Escenario

Imagina que tienes una función que valida passwords. Necesitas testear varios casos: válidos, inválidos, edge cases.

### ✅ Paso 1: Crea la función

Crea `lib/features/core/utils/password_validator.dart`:

```dart
// lib/features/core/utils/password_validator.dart

/// Valida una contraseña
/// Retorna true si es válida
class PasswordValidator {
  static bool isValid(String password) {
    if (password.isEmpty) return false;
    if (password.length < 6) return false;
    if (password.length > 20) return false;
    return true;
  }
}
```

### ✅ Paso 2: Crea los tests

Crea `test/core/utils/password_validator_test.dart`:

```dart
// test/core/utils/password_validator_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/utils/password_validator.dart';

void main() {
  group('PasswordValidator', () {
    
    group('isValid', () {
      // ✓ Casos válidos
      test('should return true for valid password (6 chars)', () {
        expect(PasswordValidator.isValid('123456'), isTrue);
      });
      
      test('should return true for valid password (10 chars)', () {
        expect(PasswordValidator.isValid('abcd123456'), isTrue);
      });
      
      // ✗ Casos inválidos
      test('should return false for empty password', () {
        expect(PasswordValidator.isValid(''), isFalse);
      });
      
      test('should return false for short password (less than 6)', () {
        expect(PasswordValidator.isValid('12345'), isFalse);
      });
      
      test('should return false for long password (more than 20)', () {
        expect(PasswordValidator.isValid('123456789012345678901'), isFalse);
      });
      
      // 🎯 Edge case: exactamente en el límite
      test('should return true for minimum valid length', () {
        expect(PasswordValidator.isValid('123456'), isTrue);  // 6 chars
      });
      
      test('should return true for maximum valid length', () {
        expect(PasswordValidator.isValid('12345678901234567890'), isTrue); // 20 chars
      });
      
      test('should return false for one over maximum', () {
        expect(PasswordValidator.isValid('123456789012345678901'), isFalse); // 21 chars
      });
    });
  });
}
```

### ✅ Paso 3: Ejecuta los tests

```bash
flutter test test/core/utils/password_validator_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +7: All tests passed!
```

---

## Ejercicio 4: Test con Objetos Complejos

### 📝 Escenario

Vamos a testear una clase `User` que tiene múltiples propiedades. Esto es más realista porque usaremos **objetos** en lugar de tipos primitivos.

### ✅ Paso 1: Crea la clase User

Crea `lib/features/core/models/user.dart`:

```dart
// lib/features/core/models/user.dart
import 'package:equatable/equatable.dart';

class User extends Equatable {
  final String id;
  final String email;
  final String name;
  final int age;

  const User({
    required this.id,
    required this.email,
    required this.name,
    required this.age,
  });

  @override
  List<Object?> get props => [id, email, name, age];

  User copyWith({
    String? id,
    String? email,
    String? name,
    int? age,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      name: name ?? this.name,
      age: age ?? this.age,
    );
  }
}
```

### ✅ Paso 2: Crea los tests

Crea `test/core/models/user_test.dart`:

```dart
// test/core/models/user_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/models/user.dart';

void main() {
  group('User', () {
    
    // Datos de prueba reutilizables
    const tUser = User(
      id: '123',
      email: 'test@example.com',
      name: 'John',
      age: 30,
    );

    test('should create User with all required fields', () {
      // Arrange & Act
      const user = User(
        id: '456',
        email: 'jane@example.com',
        name: 'Jane',
        age: 25,
      );

      // Assert
      expect(user.id, '456');
      expect(user.email, 'jane@example.com');
      expect(user.name, 'Jane');
      expect(user.age, 25);
    });

    group('Equatable (equality)', () {
      test('should be equal when properties are equal', () {
        // Arrange
        const user1 = User(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          age: 30,
        );
        const user2 = User(
          id: '123',
          email: 'test@example.com',
          name: 'John',
          age: 30,
        );

        // Act & Assert
        expect(user1, equals(user2));
      });

      test('should not be equal when id differs', () {
        // Arrange
        const user1 = User(id: '123', email: 'test@example.com', name: 'John', age: 30);
        const user2 = User(id: '456', email: 'test@example.com', name: 'John', age: 30);

        // Act & Assert
        expect(user1, isNot(equals(user2)));
      });

      test('should not be equal when email differs', () {
        // Arrange
        const user1 = User(id: '123', email: 'test1@example.com', name: 'John', age: 30);
        const user2 = User(id: '123', email: 'test2@example.com', name: 'John', age: 30);

        // Act & Assert
        expect(user1, isNot(equals(user2)));
      });
    });

    group('copyWith', () {
      test('should update only specified field (name)', () {
        // Arrange
        const original = tUser;

        // Act
        final updated = original.copyWith(name: 'Jane');

        // Assert
        expect(updated.name, 'Jane');           // Cambió
        expect(updated.id, original.id);         // Igual
        expect(updated.email, original.email);   // Igual
        expect(updated.age, original.age);       // Igual
      });

      test('should update multiple fields', () {
        // Arrange
        const original = tUser;

        // Act
        final updated = original.copyWith(
          name: 'Jane',
          age: 25,
        );

        // Assert
        expect(updated.name, 'Jane');
        expect(updated.age, 25);
        expect(updated.id, original.id);       // Sin cambios
        expect(updated.email, original.email); // Sin cambios
      });

      test('should return same instance when no parameters provided', () {
        // Arrange
        const original = tUser;

        // Act
        final updated = original.copyWith();

        // Assert
        expect(updated, equals(original));
      });
    });

    test('props should contain all fields', () {
      // Arrange
      const user = tUser;

      // Act
      final props = user.props;

      // Assert
      expect(props, ['123', 'test@example.com', 'John', 30]);
    });
  });
}
```

### ✅ Paso 3: Ejecuta los tests

```bash
flutter test test/core/models/user_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +9: All tests passed!
```

---

## 🧪 Verifica Tu Solución

Ejecuta todos los tests que has creado:

```bash
# Todos los tests de la práctica
flutter test test/core/

# O individualmente
flutter test test/core/utils/calculator_test.dart
flutter test test/core/utils/password_validator_test.dart
flutter test test/core/models/user_test.dart
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Tests de calculadora (add) - 4 tests
- [ ] Ejercicio 2: Test de excepción (divide)
- [ ] Ejercicio 3: Tests de validación (PasswordValidator) - 7 tests
- [ ] Ejercicio 4: Tests de objeto complejo (User) - 9 tests
- [ ] Total: **21 tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has completado tu primera práctica de testing. Ahora sabes:

- ✅ Escribir tests con patrón AAA
- ✅ Usar matchers básicos (`equals`, `isTrue`, `isFalse`, `isA`)
- ✅ Testear excepciones con `throwsA`
- ✅ Testear objetos con múltiples propiedades
- ✅ Usar grupos para organizar tests

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 2: Testing Domain](./02-domain-testing.md)

**Práctica:** [02a-practica-fakes-manuales.md](./02a-practica-fakes-manuales.md)

> En la siguiente práctica aprenderás a crear **Fakes Manuales** para testear UseCases con dependencias.
