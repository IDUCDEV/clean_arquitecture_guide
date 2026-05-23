# 🧪 Parte 1: Fundamentos del Testing en Clean Architecture

> **¿De qué trata esta parte?** De entender qué es un test, por qué es importante, y cómo escribirlos correctamente. Sin código todavía, solo conceptos que necesitas interiorizar.

---

## 📋 Índice

1. [¿Qué es un test y por qué testear?](#qué-es-un-test-y-por-qué-testear)
2. [Estructura del Proyecto de Tests](#estructura-del-proyecto-de-tests)
3. [Dependencias Necesarias](#dependencias-necesarias)
4. [Conceptos Fundamentales](#conceptos-fundamentales)
5. [El Patrón AAA](#el-patrón-aaa)
6. [Tu Primer Test](#tu-primer-test)
7. [Errores Comunes](#errores-comunes)
8. [ Checklist](#-checklist)

---

## 1. ¿Qué es un Test y Por Qué Testear?

### 🧠 La Analogía del Chef

Imagina que eres un chef en un restaurante:

**Sin tests** = Cocinar un plato y directamente servirlo al cliente sin probarlo
**Con tests** = Probar la comida mientras la cook, ajustar condimentos, verificar que está lista

> Un test es como **probar tu comida mientras cookes**, no después de servirla al cliente.

### 🤔 ¿Por qué dedicar tiempo a testear?

```
┌─────────────────────────────────────────────────────────────┐
│                    BENEFICIOS DEL TESTING                   │
├─────────────────────────────────────────────────────────────┤
│ ✅ Detectar errores ANTES de que el usuario los vea        │
│ ✅ Cambiar código con confianza (refactoring seguro)        │
│ ✅ Documentación automática del comportamiento             │
│ ✅ Ejecutar miles de pruebas en segundos                   │
│ ✅ Encontrar bugs que aparecen solo en edge cases           │
└─────────────────────────────────────────────────────────────┘
```

### 📊 El Costo del Testing

| Aspecto | Sin Tests | Con Tests |
|---------|-----------|-----------|
| **Tiempo inicial** | 0 horas | 30% más |
| **Debugging** | Horas/días | Minutos |
| **Refactoring** | Con miedo | Con confianza |
| **Bugs en producción** | Frecuentes | Raros |

**Conclusión:** Invertir tiempo en tests **ahorra tiempo** a largo plazo.

---

## 2. Estructura del Proyecto de Tests

### 🎯 Principio Clave

> Los tests deben **espejar** la estructura de tu código de producción.

Si tu código está en `lib/features/`, tus tests deben estar en `test/features/`.

```
project_root/
├── lib/                           ← Tu código de producción
│   └── clean/
│       ├── core/
│       └── features/
│           └── auth/
│               ├── domain/
│               ├── data/
│               └── presentation/
│
└── test/                          ← Tus tests (espejo de lib/)
    ├── core/
    │   ├── error/
    │   └── utils/
    ├── features/
    │   └── auth/
    │       ├── domain/
    │       │   ├── entities/
    │       │   │   └── user_test.dart
    │       │   └── usecases/
    │       │       └── login_usecase_test.dart
    │       ├── data/
    │       │   ├── models/
    │       │   │   └── user_model_test.dart
    │       │   └── repositories/
    │       │       └── auth_repository_impl_test.dart
    │       └── presentation/
    │           ├── cubit/
    │           │   └── auth_cubit_test.dart
    │           └── pages/
    │               └── auth_page_test.dart
    ├── fixtures/                  ← Datos de prueba JSON
    │   ├── user.json
    │   └── auth_response.json
    └── helpers/                   ← Utilidades de testing
        └── mocks/                  ← Mocks generados
        └── fixture_reader.dart
```

### 📝 Convenciones de Nombrado

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| **Archivo de test** | `{nombre}_test.dart` | `user_test.dart` |
| **Carpeta de test** | Mismo nombre que en lib | `domain/entities/` |
| **Nombre del test** | `should [comportamiento] when [condición]` | `should return user when login succeeds` |

### 💡 ¿Por qué esta estructura?

1. **Encontrar tests rápidamente** - Si modificas `user.dart`, immediately sabes dónde está su test
2. **Navegación fácil** - Puedes hacer Ctrl+Click entre código y test
3. **Organización mental** - Separas "qué hago" (lib) de "cómo lo verifico" (test)

---

## 3. Dependencias Necesarias

### 📦 pubspec.yaml

Agrega estas dependencias a tu `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
  flutter_lints: ^6.0.0
  bloc_test: ^9.1.0          # Para testear Cubits/Blocs
  mocktail: ^1.0.4            # Para mocks sin generación de código
  fpdart: ^1.1.0              # Either, Option - programación funcional
  internet_connection_checker_plus: ^2.5.0  # Detectar conectividad
  supabase_flutter: ^2.5.0    # Cliente Supabase (para tests de integración)
```

### 📋 Explicación de Cada Dependencia

| Dependencia | Propósito | ¿Cuándo usarla? |
|-------------|-----------|-----------------|
| `flutter_test` | Framework base de testing en Flutter | **Siempre** |
| `integration_test` | Tests de flujo completo (E2E) | Para simular usuario real |
| `bloc_test` | Testing especializado de Cubits/Blocs | Para capa Presentation |
| `mocktail` | Mocks sin generación de código | Alternativa moderna a Mockito |
| `fpdart` | Either, Option para manejo funcional de errores | Domain y Data layers |
| `internet_connection_checker_plus` | Detectar conectividad en tiempo real | Capa Core |
| `supabase_flutter` | Cliente oficial de Supabase | Tests de integración |

### 🚀 Instalación

```bash
flutter pub get
```

---

## 4. Conceptos Fundamentales

### 4.1 La Función `test()`

Un **test** es un caso de prueba individual. Define un escenario específico:

```dart
test('descripción del test en lenguaje natural', () {
  // Tu código de verificación
});
```

**Características:**
- Nombre en **inglés** describiendo el comportamiento
- Debe ser **declarativo** (qué debe pasar, no cómo)
- Solo una **aserción principal** por test (idealmente)

**Ejemplos de buenos nombres:**
```dart
test('should return true for valid email')
test('should throw exception when dividing by zero')
test('should return user when login is successful')
```

**Ejemplos de malos nombres:**
```dart
test('test1')                           // ❌ Ambiguo
test('login function')                  // ❌ No dice qué debe pasar
test('should work correctly')           // ❌ Qué significa "correctamente"?
```

### 4.2 El `group()`

Agrupa tests relacionados para mejor organización y reporte:

```dart
group('Calculator', () {
  test('should add correctly', () { ... });
  test('should subtract correctly', () { ... });
  test('should multiply correctly', () { ... });
});
```

**Salida en consola:**
```
00:00 +3: Calculator
  should add correctly
  should subtract correctly  
  should multiply correctly
```

### 4.3 El `expect()` - Verificar Resultados

**`expect()`** es el corazón del testing. Verifica que un valor sea el esperado:

```dart
expect(actual, matcher);
```

#### 🎯 Matchers (Comparadores) Más Comunes

```dart
// Igualdad exacta
expect(value, equals(42));

// Tipo de dato
expect(value, isA<String>());

// Booleanos
expect(value, isTrue);
expect(value, isFalse);

// Null
expect(value, isNull);
expect(value, isNotNull);

// Listas
expect(list, hasLength(3));
expect(list, contains('item'));

// Excepciones
expect(() => code(), throwsA(isA<Exception>()));

// Composables (combinaciones)
expect(value, isNotNull);
expect(value, isA<String>().having((s) => s.length, 'length', 5));
```

### 4.4 El `setUp()` - Preparación

Código que se ejecuta **antes de cada test** en un grupo:

```dart
group('AuthRepository', () {
  late MockIAuthRepository mockRepository;
  
  setUp(() {
    mockRepository = MockIAuthRepository();  // Se ejecuta ANTES de cada test
  });
  
  test('test 1', () { 
    // mockRepository aquí está FRESCO (nueva instancia)
  });
  
  test('test 2', () { 
    // mockRepository aquí está FRESCO (nueva instancia otra vez)
  });
});
```

**¿Por qué usar setUp?**
- Evita repetir código de preparación
- Garantiza que cada test tiene datos frescos
- Facilita el mantenimiento

### 4.5 El `tearDown()` - Limpieza

Código que se ejecuta **después de cada test**:

```dart
setUp(() {
  cubit = AuthCubit(...);
});

tearDown(() {
  cubit.close();  // ¡Importante! Libera recursos
});
```

**¿Por qué usar tearDown?**
- Liberar memoria
- Cerrar conexiones
- Limpiar estado global

### 4.6 Async/Await - Código Asíncrono

Para testear código asíncrono (futures, streams):

```dart
test('should complete async operation', () async {
  // El test espera a que termine la operación
  final result = await repository.login('email', 'pass');
  
  // Luego verifica el resultado
  expect(result, isA<Right<Failure, User>>());
});
```

---

## 5. El Patrón AAA

> **El patrón AAA** es la estructura estándar para escribir tests claros y mantenibles.

### 🤔 ¿Por qué AAA?

Imagina que lees un test sin saber qué hace. ¿Qué necesitas saber?

1. **Qué preparaste** (Arrange)
2. **Qué ejecutaste** (Act)  
3. **Qué esperabas** (Assert)

### 📦 Las Tres Secciones

```dart
test('should return user when login is successful', () async {
  // ═══════════════════════════════════════════════════════════
  // ARRANGE: Preparar el escenario
  // ═══════════════════════════════════════════════════════════
  const email = 'test@example.com';
  const password = 'password123';
  final mockRepository = MockIAuthRepository();
  when(() => mockRepository.login(any(), any()))
      .thenAnswer((_) async => Either.right(tUser));
  
  // ═══════════════════════════════════════════════════════════
  // ACT: Ejecutar la acción que queremos testear
  // ═══════════════════════════════════════════════════════════
  final result = await mockRepository.login(email, password);
  
  // ═══════════════════════════════════════════════════════════
  // ASSERT: Verificar el resultado
  // ═══════════════════════════════════════════════════════════
  expect(result, isA<Right<Failure, User>>());
  result.match(
    (failure) => fail('Should not return failure'),
    (user) => expect(user.email, email),
  );
});
```

### 📊 Resumen del AAA

| Sección | Propósito | Ejemplo |
|---------|-----------|---------|
| **ARRANGE** | Setup inicial, crear objetos, configurar mocks | Crear MockRepository, configurar when() |
| **ACT** | Ejecutar la acción que queremos testear | Llamar a `login()` |
| **ASSERT** | Verificar que el resultado es el esperado | `expect(result, ...)` y `verify(...)` |

### ⚠️ Errores Comunes con AAA

```dart
// ❌ MALO: Mezclar Arrange y Act
test('bad example', () {
  final repo = MockIAuthRepository();  // Arrange
  final result = repo.login(...);      // Act - mezclado con arrange
  expect(result, ...);                  // Assert
});

// ✅ BUENO: Secciones claras
test('good example', () async {
  // Arrange
  final mockRepository = MockIAuthRepository();
  when(() => mockRepository.login(any(), any()))
      .thenAnswer((_) async => Either.right(tUser));
  
  // Act
  final result = await mockRepository.login(...);
  
  // Assert
  expect(result.isRight(), true);
  verify(() => mockRepository.login(...)).called(1);
});
```

---

## 6. Tu Primer Test

Vamos a crear un test simple para una función pura (sin dependencias externas).

### Paso 1: Crea el archivo de test

```bash
touch test/core/utils/string_utils_test.dart
```

### Paso 2: Crea la función (si no existe)

```dart
// lib/features/core/utils/string_utils.dart
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

### Paso 3: Escribe el test

```dart
// test/core/utils/string_utils_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/utils/string_utils.dart';

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

### Paso 4: Ejecuta el test

```bash
# Ejecutar un test específico
flutter test test/core/utils/string_utils_test.dart

# Ejecutar con verbose (más detalles)
flutter test test/core/utils/string_utils_test.dart --verbose

# Ejecutar un test específico por nombre
flutter test --plain-name "should return true for valid email"
```

### Paso 5: Salida Esperada

```
✓ All tests passed!
00:00 +4: All tests passed!
```

---

## 7. Errores Comunes

### ❌ Error 1: Olvidar async/await

```dart
// ❌ MALO: Test asíncrono sin async
test('should login', () {
  final result = repository.login('email', 'pass');
  expect(result, ...);  // ¡Esto falla! result es un Future, no el valor
});

// ✅ BUENO: Usar async/await
test('should login', () async {
  final result = await repository.login('email', 'pass');
  expect(result, ...);
});
```

### ❌ Error 2: No verificar excepciones

```dart
// ❌ MALO: Esperar que funcione sin verificar el error
test('should throw on invalid input', () {
  expect(() => divide(10, 0), returnsNormally);  // ¡Esto pasa!
});

// ✅ BUENO: Verificar que lanza la excepción correcta
test('should throw on divide by zero', () {
  expect(
    () => divide(10, 0),
    throwsA(isA<ArgumentError>()),
  );
});
```

### ❌ Error 3: Tests que dependen de otros tests

```dart
// ❌ MALO: Un test depende del estado de otro
test('first test', () {
  counter = 5;
});

test('second test depends on first', () {
  expect(counter, 5);  // ¡Podería fallar si se ejecutan en otro orden!
});
```

### ❌ Error 4: Nombres poco descriptivos

```dart
// ❌ MALO
test('test1', () { ... });
test('login test', () { ... });

// ✅ BUENO
test('should return user when credentials are valid', () { ... });
test('should throw exception when password is empty', () { ... });
```

---

## ✅ Checklist

Antes de pasar a la siguiente parte, asegúrate de:

- [ ] Entender qué es un test y por qué es importante
- [ ] Conocer la estructura de carpetas de tests
- [ ] Saber usar `test()` y `group()`
- [ ] Conocer los matchers básicos (`equals`, `isA`, `isTrue`, etc.)
- [ ] Aplicar el patrón AAA en cada test
- [ ] Saber usar `setUp()` y `tearDown()`
- [ ] Ejecutar tests desde la terminal
- [ ] Instalar las dependencias necesarias
- [ ] Evitar errores comunes (async/await, nombres)

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 2: Testing Domain (Entities y UseCases)](./02-domain-testing.md)

**Práctica:** [01a-practica-primeros-tests.md](./01a-practica-primeros-tests.md) ← ¡Practica lo que aprendiste!

---

## 📚 Recursos Adicionales

- [Documentación oficial flutter_test](https://api.flutter.dev/flutter/flutter_test/flutter_test-library.html)
- [Patrón AAA](https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/)
- [Matchers en Dart](https://api.flutter.dev/flutter/package-matcher_matcher/package-matcher_matcher-library.html)
