# 🧪 Parte 1: Fundamentos del Testing en Clean Architecture

## 📋 Índice
1. [¿Por qué testear en Clean Architecture?](#por-qué-testear-en-clean-architecture)
2. [Estructura del Proyecto de Tests](#estructura-del-proyecto-de-tests)
3. [Dependencias Necesarias](#dependencias-necesarias)
4. [Conceptos Fundamentales](#conceptos-fundamentales)
5. [El Patrón AAA](#el-patrón-aaa)
6. [Tu Primer Test](#tu-primer-test)
7. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## ¿Por qué testear en Clean Architecture?

Clean Architecture facilita enormemente el testing porque cada capa es **independiente** y tiene **responsabilidades únicas**:

```
┌─────────────────────────────────────┐
│           PRESENTATION              │  ← Testeamos: Estados, UI, Cubits
│   (Cubits, Pages, Widgets)          │     Herramientas: bloc_test, testWidgets
├─────────────────────────────────────┤
│              DOMAIN                 │  ← Testeamos: Lógica pura, reglas de negocio
│   (Entities, UseCases)              │     Herramientas: flutter_test
├─────────────────────────────────────┤
│               DATA                  │  ← Testeamos: Persistencia, APIs, mapeo
│   (Models, Repositories, Sources)   │     Herramientas: flutter_test, Fakes
└─────────────────────────────────────┘
```

### ✅ Beneficios de testear por capas:

1. **Domain (Lógica pura)**: Tests rápidos, sin dependencias de Flutter
2. **Data (Infraestructura)**: Tests con Fakes/Mocks de APIs y BD
3. **Presentation (UI/Estados)**: Tests de comportamiento del usuario

---

## Estructura del Proyecto de Tests

Los tests deben **espejar** la estructura de `lib/clean/`:

```
project_root/
├── lib/
│   └── clean/
│       ├── core/
│       └── features/
│           └── auth/
│               ├── domain/
│               ├── data/
│               └── presentation/
│
└── test/                           ← Mirror de lib/clean/
    ├── core/
    │   ├── error/
    │   ├── network/
    │   └── utils/
    ├── features/
    │   └── auth/
    │       ├── domain/
    │       │   ├── entities/
    │       │   │   └── user_test.dart
    │       │   └── usecases/
    │       │       ├── login_usecase_test.dart
    │       │       ├── register_usecase_test.dart
    │       │       └── logout_usecase_test.dart
    │       ├── data/
    │       │   ├── models/
    │       │   │   └── user_model_test.dart
    │       │   ├── repositories/
    │       │   │   └── auth_repository_impl_test.dart
    │       │   └── datasources/
    │       │       ├── auth_remote_data_source_test.dart
    │       │       └── auth_local_data_source_test.dart
    │       └── presentation/
    │           ├── cubit/
    │           │   └── auth_cubit_test.dart
    │           └── pages/
    │               └── auth_page_test.dart
    ├── fixtures/                    ← Datos de prueba JSON
    │   ├── user.json
    │   └── auth_response.json
    └── helpers/                     ← Utilidades de testing
        ├── fake_repositories.dart
        └── fixture_reader.dart
```

### 📝 Convenciones de nombrado:

- **Archivos**: `nombre_original_test.dart` (siempre termina en `_test.dart`)
- **Tests**: `'should [comportamiento] when [condición]'`
- **Groups**: Agrupar por método o funcionalidad

---

## Dependencias Necesarias

Agrega estas dependencias a tu `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
  flutter_lints: ^6.0.0
  bloc_test: ^9.1.0          # Para testear Cubits/Blocs
  build_runner: ^2.10.2      # Si decides usar @GenerateMocks en el futuro
```

### 📦 Explicación de cada dependencia:

| Dependencia | Propósito | ¿Cuándo usarla? |
|-------------|-----------|-----------------|
| `flutter_test` | Framework base de testing | Siempre |
| `integration_test` | Tests de flujo completo (E2E) | Para testear flujos de usuario |
| `bloc_test` | Testing especializado de Cubits | Para testear la capa Presentation |
| `build_runner` | Generación de código | Solo si usas @GenerateMocks (futuro) |

### 🚀 Instalación:

```bash
flutter pub get
```

---

## Conceptos Fundamentales

### 1. **Test Function**

La función `test()` define un caso de prueba individual:

```dart
test('should return 2 when adding 1 + 1', () {
  // Código del test
});
```

### 2. **Group**

Agrupa tests relacionados para mejor organización:

```dart
group('Calculator', () {
  test('should add correctly', () { ... });
  test('should subtract correctly', () { ... });
  test('should multiply correctly', () { ... });
});
```

### 3. **Expect**

Verifica que una condición sea verdadera:

```dart
expect(actual, expected);
```

**Matchers comunes:**
```dart
expect(value, equals(42));           // Igualdad exacta
expect(value, isA<String>());        // Tipo de dato
expect(value, isTrue);               // Booleano true
expect(value, isNull);               // Null
expect(value, isNotNull);            // No null
expect(list, hasLength(3));          // Longitud de lista
expect(list, contains('item'));      // Contiene elemento
```

### 4. **SetUp**

Código que se ejecuta **antes de cada test** en un grupo:

```dart
group('AuthRepository', () {
  late FakeAuthRepository repository;
  
  setUp(() {
    repository = FakeAuthRepository();  // Se crea antes de cada test
  });
  
  test('test 1', () { ... });  // Usa repository fresco
  test('test 2', () { ... });  // Usa repository fresco (nueva instancia)
});
```

### 5. **TearDown**

Código que se ejecuta **después de cada test**:

```dart
setUp(() {
  cubit = AuthCubit(...);
});

tearDown(() {
  cubit.close();  // Limpieza importante para Cubits
});
```

### 6. **Async/Await**

Para testear código asíncrono:

```dart
test('should complete async operation', () async {
  final result = await repository.login('email', 'pass');
  expect(result, isA<Right<Failure, User>>());
});
```

---

## El Patrón AAA

El patrón **AAA** (Arrange-Act-Assert) es la estructura estándar para escribir tests claros:

```dart
test('should return user when login is successful', () async {
  // ARRANGE: Preparar el escenario
  const email = 'test@example.com';
  const password = 'password123';
  final fakeRepository = FakeAuthRepository();
  fakeRepository.userToReturn = const User(id: '1', email: email);
  
  // ACT: Ejecutar la acción a testear
  final result = await fakeRepository.login(email, password);
  
  // ASSERT: Verificar el resultado
  expect(result, isA<Right<Failure, User>>());
  result.fold(
    (failure) => fail('Should not return failure'),
    (user) => expect(user.email, email),
  );
});
```

### 🎯 Cada sección tiene un propósito claro:

| Sección | Propósito | Ejemplo |
|---------|-----------|---------|
| **ARRANGE** | Setup inicial, crear objetos, configurar mocks | Crear FakeRepository, setear datos |
| **ACT** | Ejecutar la acción que queremos testear | Llamar a login() |
| **ASSERT** | Verificar que el resultado es el esperado | expect(result, ...) |

---

## Tu Primer Test

Vamos a crear un test simple para una función pura (sin dependencias):

### 1. Crea el archivo de test

```bash
touch test/core/utils/string_utils_test.dart
```

### 2. Escribe tu primera función (en lib)

```dart
// lib/clean/core/utils/string_utils.dart
class StringUtils {
  static bool isValidEmail(String email) {
    final emailRegex = RegExp(r'^[^@]+@[^@]+\.[^@]+');
    return emailRegex.hasMatch(email);
  }
  
  static String capitalize(String text) {
    if (text.isEmpty) return text;
    return text[0].toUpperCase() + text.substring(1).toLowerCase();
  }
}
```

### 3. Escribe el test

```dart
// test/core/utils/string_utils_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/core/utils/string_utils.dart';

void main() {
  group('StringUtils', () {
    group('isValidEmail', () {
      test('should return true for valid email', () {
        // Arrange
        const email = 'test@example.com';
        
        // Act
        final result = StringUtils.isValidEmail(email);
        
        // Assert
        expect(result, isTrue);
      });
      
      test('should return false for invalid email without @', () {
        // Arrange
        const email = 'testexample.com';
        
        // Act
        final result = StringUtils.isValidEmail(email);
        
        // Assert
        expect(result, isFalse);
      });
      
      test('should return false for invalid email without domain', () {
        // Arrange
        const email = 'test@example';
        
        // Act
        final result = StringUtils.isValidEmail(email);
        
        // Assert
        expect(result, isFalse);
      });
      
      test('should return false for empty string', () {
        // Arrange
        const email = '';
        
        // Act
        final result = StringUtils.isValidEmail(email);
        
        // Assert
        expect(result, isFalse);
      });
    });
    
    group('capitalize', () {
      test('should capitalize first letter', () {
        // Arrange
        const text = 'hello';
        
        // Act
        final result = StringUtils.capitalize(text);
        
        // Assert
        expect(result, 'Hello');
      });
      
      test('should handle empty string', () {
        // Arrange
        const text = '';
        
        // Act
        final result = StringUtils.capitalize(text);
        
        // Assert
        expect(result, '');
      });
    });
  });
}
```

### 4. Ejecuta el test

```bash
# Ejecutar un test específico
flutter test test/core/utils/string_utils_test.dart

# Ejecutar con verbose (más detalles)
flutter test test/core/utils/string_utils_test.dart --verbose

# Ejecutar un test específico por nombre
flutter test --plain-name "should return true for valid email"
```

### 5. Salida esperada

```
00:00 +4: All tests passed!
```

---

## Ejercicios Prácticos

### Ejercicio 1: Test básico
Crea tests para esta función:

```dart
int add(int a, int b) => a + b;
```

**Tests a escribir:**
- Suma de positivos
- Suma con cero
- Suma de negativos

<details>
<summary>Ver solución</summary>

```dart
group('add', () {
  test('should add two positive numbers', () {
    expect(add(2, 3), equals(5));
  });
  
  test('should return same number when adding zero', () {
    expect(add(5, 0), equals(5));
  });
  
  test('should add negative numbers', () {
    expect(add(-2, -3), equals(-5));
  });
});
```
</details>

### Ejercicio 2: Test con excepciones
Crea tests para esta función:

```dart
double divide(double a, double b) {
  if (b == 0) throw ArgumentError('Cannot divide by zero');
  return a / b;
}
```

**Tests a escribir:**
- División normal
- División por cero (debe lanzar excepción)

<details>
<summary>Ver solución</summary>

```dart
group('divide', () {
  test('should divide correctly', () {
    expect(divide(10, 2), equals(5.0));
  });
  
  test('should throw ArgumentError when dividing by zero', () {
    expect(
      () => divide(10, 0),
      throwsA(isA<ArgumentError>()),
    );
  });
});
```
</details>

---

## ✅ Checklist de Fundamentos

Antes de pasar a la siguiente parte, asegúrate de:

- [ ] Entender la estructura de carpetas de tests
- [ ] Saber usar `test()` y `group()`
- [ ] Conocer los matchers básicos (`equals`, `isA`, `isTrue`, etc.)
- [ ] Aplicar el patrón AAA en cada test
- [ ] Saber usar `setUp()` y `tearDown()`
- [ ] Ejecutar tests desde la terminal
- [ ] Instalar las dependencias necesarias

---

## 🚀 Siguiente Paso

➡️ **Parte 2: Testing Domain (Entities y UseCases)**

En la siguiente parte aprenderás a:
- Testear Entities con Equatable
- Testear UseCases con Fakes manuales
- Manejar Either<Failure, Success>
- Crear tu primer Fake Repository

---

## 📚 Recursos Adicionales

- [Documentación oficial flutter_test](https://api.flutter.dev/flutter/flutter_test/flutter_test-library.html)
- [Patrón AAA](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)
- [Matchers en Dart](https://api.flutter.dev/flutter/package-matcher_matcher/package-matcher_matcher-library.html)
