# 🧪 Parte 2b: Introducción a Mocktail - Guía Completa

> **¿De qué trata esta parte?** Esta es una guía completa sobre Mocktail, una biblioteca moderna para crear mocks sin generación de código.

---

## 📋 Índice

1. [Introducción: ¿Qué es Mocktail?](#1-introducción-qué-es-mocktail)
2. [¿Cuándo usar Mocktail?](#2-cuándo-usar-mocktail)
3. [Configuración del Proyecto](#3-configuración-del-proyecto)
4. [Creación de Mocks](#4-creación-de-mocks)
5. [La API de Stubbing: when()](#5-la-api-de-stubbing-when)
6. [La API de Verificación: verify()](#6-la-api-de-verificación-verify)
7. [Matchers: any(), captureAny()](#7-matchers-any-captureany)
8. [Captura de Argumentos](#8-captura-de-argumentos)
9. [Errores Comunes y Cómo Resolverlos](#9-errores-comunes-y-cómo-resolverlos)
10. [Mocktail por Capa de Clean Architecture](#10-mocktail-por-capa-de-clean-architecture)
11. [Resumen Cheatsheet](#11-resumen-cheatsheet)

---

## 1. Introducción: ¿Qué es Mocktail?

### 🎭 La Analogía del Actor de Reparto

Imagina que estás rodando una película:

| Sin Mocktail | Con Mocktail |
|-------------|-------------|
| **Tú escribes el guión completo** - Defines exactamente qué dice cada actor | **Un actor entrenado** - El actor (mock) sabe improvisar según las instrucciones que le das |
| **Control total pero más trabajo** | **Menos trabajo, más flexibilidad** |
| Ejemplo: Escribes cada diálogo manualmente | Ejemplo: Das instrucciones generales: "Cuando te pregunten X, responde Y" |

### 📦 ¿Qué es Mocktail?

Mocktail es una biblioteca que **crea implementaciones falsas de interfaces** sin necesidad de generación de código. En lugar de escribir a mano una clase que implemente una interfaz, Mocktail la crea por ti con una sola línea:

```dart
// ✅ CON MOCKTAIL - ¡Solo una línea!
class MockIAuthRepository extends Mock implements IAuthRepository {}

// Tú solo dices qué retornar:
when(() => mockRepository.login(any(), any()))
    .thenAnswer((_) async => Either.right(tUser));
```

### ✨ Ventajas de Mocktail

| Ventaja | Descripción |
|---------|-------------|
| 🚫 Sin `build_runner` | No necesitas generación de código |
| ⚡ Setup inmediato | Crea el mock y úsalo |
| 🎯 API familiar | Misma sintaxis `when()` / `verify()` |
| 🔒 Null safety nativo | Compatible desde el inicio |
| 📦 Liviano | Una sola dependencia |

---

## 2. ¿Cuándo Usar Mocktail?

### ✅ Usa Mocktail cuando:

| Señal | Descripción |
|-------|-------------|
| 🏢 Cualquier proyecto | Funciona tanto en proyectos pequeños como grandes |
| 👥 Equipo de cualquier tamaño | Curva de aprendizaje baja |
| 🔄 Interfaces cambian | No necesitas regenerar nada |
| 🔍 Verificaciones | `verify()` para llamadas y argumentos |
| ⚡ Desarrollo rápido | Sin esperar a `build_runner` |

### 📊 Comparación: Sin Mock vs Con Mocktail

| Característica | Sin Mocks (implementación real) | Mocktail |
|---------------|-------------------------------|----------|
| **Setup inicial** | Escribes toda la implementación | Una línea: `extends Mock implements` |
| **Tiempo por test** | Lento (dependencias reales) | Rápido (solo configuras lo necesario) |
| **Verificación de llamadas** | No disponible | Automática (verify) |
| **Verificación de argumentos** | No disponible | Automática (verify con parámetros) |
| **Mantenimiento** | Alto | Bajo |
| **Ideal para** | Tests de integración | Tests unitarios |

---

## 3. Configuración del Proyecto

### 📦 Paso 1: Añadir dependencias

En tu `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.4
  bloc_test: ^9.1.0         # (Ya lo tienes probablemente)
```

```bash
flutter pub get
```

### ✅ Eso es todo

No necesitas `build.yaml`, ni `build_runner`, ni configuración adicional.

---

## 4. Creación de Mocks

### 📝 La Sintaxis Mágica

```dart
import 'package:mocktail/mocktail.dart';

// Esta línea crea un mock que implementa la interfaz IProductRepository
class MockIProductRepository extends Mock implements IProductRepository {}
```

### 🔍 Cómo funciona

Cuando escribes `extends Mock implements IProductRepository`, Mocktail:
1. Crea una clase que extiende `Mock`
2. Implementa automáticamente todos los métodos de `IProductRepository`
3. Provee las funcionalidades de `when()` y `verify()`

```
┌─────────────────────────────────────────────┐
│  TU ARCHIVO DE TEST                         │
│  product_repository_test.dart               │
├─────────────────────────────────────────────┤
│  import 'package:mocktail/mocktail.dart';   │
│  class MockIProductRepository               │
│      extends Mock implements                │
│        IProductRepository {}  ← ¡El mock!   │
└─────────────────────────────────────────────┘
```

### ⚠️ Registro de Fallback Values

Cuando usas `any()` con tipos personalizados, Mocktail necesita un "fallback value":

```dart
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});
```

Esto solo es necesario para tipos que no son `String`, `int`, `bool`, etc.

---

## 5. La API de Stubbing: when()

### 🎯 Concepto: "Cuando ocurra X, retorna Y"

El stubbing le dice al mock: "Cuando alguien llame a este método con estos argumentos, responde así".

> **Importante:** En Mocktail, `when()` recibe siempre una función anónima: `when(() => mock.metodo(...))`

### 📚 Métodos Principales

#### 5.1 thenAnswer() - Respuesta personalizada

```dart
// Cuando llamen a getProduct('1'), retorna Right(tProduct)
when(() => mockRepository.getProduct('1'))
    .thenAnswer((_) async => Either.right(tProduct));
```

**Para valores síncronos:**
```dart
when(() => mockRepository.getProduct('1')).thenAnswer((_) => tProduct);
```

#### 5.2 thenReturn() - Retorno directo

```dart
// Para métodos síncronos
when(() => mockRepository.getProductCount()).thenReturn(5);
when(() => mockRepository.isProductInStock('1')).thenReturn(true);
```

#### 5.3 thenThrow() - Lanzar excepción

```dart
when(() => mockRepository.getProduct(any())).thenThrow(Exception('Network error'));
when(() => mockRepository.getProduct('999'))
    .thenThrow(ServerException('Product not found'));
```

### 🔗 Encadenando respuestas

```dart
// Primera llamada retorna X, segunda retorna Y
when(() => mockRepository.getProduct(any()))
    .thenAnswer((_) async => Either.right(tProduct))
    .thenAnswer((_) async => Either.left(ServerFailure()));
```

### 🎲 thenAnswer() vs thenReturn()

| Método | Cuándo usarlo |
|--------|---------------|
| `thenAnswer()` | Cuando hay lógica async o necesitas acceder a los argumentos |
| `thenReturn()` | Cuando el valor ya está disponible y es síncrono |

### 🔑 Importante: Fallback values para any()

Cuando usas `any()` con un tipo personalizado, debes registrar un fallback value:

```dart
// ❌ Esto falla si Product no es un tipo básico
when(() => mockRepository.updateProduct(any()))

// ✅ Solución: registrar fallback value
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});
```

---

## 6. La API de Verificación: verify()

### 🎯 Concepto: "¿Realmente se llamó?"

La verificación confirma que el código que estás probando realmente llamó a los métodos correctos con los argumentos correctos.

### 📚 Métodos de Verificación

#### 6.1 verify() - Verificar que se llamó

```dart
// Verifica que se llamó exactamente una vez
verify(() => mockRepository.getProduct('1')).called(1);
```

#### 6.2 verifyNever() - Verificar que NO se llamó

```dart
// Verifica que NUNCA se llamó
verifyNever(() => mockRepository.deleteProduct(any()));
```

#### 6.3 verifyNoMoreInteractions() - No más interacciones

```dart
verify(() => mockRepository.getProduct('1')).called(1);
verifyNoMoreInteractions(mockRepository);
```

#### 6.4 verifyZeroInteractions() - Sin ninguna interacción

```dart
verifyZeroInteractions(mockRepository);
```

### 🔍 Verificación con Argumentos

```dart
// Verifica que se llamó con ALGÚN argumento
verify(() => mockRepository.getProduct(any())).called(1);

// Verifica que se llamó con un argumento EXACTO
verify(() => mockRepository.getProduct('123')).called(1);

// Verifica argumentos nombrados
verify(() => mockRepository.updateProduct(
  id: '123',
  product: any(named: 'product'),
)).called(1);
```

---

## 7. Matchers: any(), captureAny()

### 🎯 Concepto: "No me importa el valor exacto"

Los matchers te permiten verificar o stubbing sin especificar valores exactos.

### 📚 Tipos de Matchers

#### 7.1 any() - Cualquier valor

```dart
// Stubbing: No importa qué ID pasen, retorna tProduct
when(() => mockRepository.getProduct(any())).thenAnswer((_) => Either.right(tProduct));

// Verificación: Verifica que se llamó con ALGÚN argumento
verify(() => mockRepository.getProduct(any())).called(1);
```

#### 7.2 any(named:) - Cualquier valor para argumento nombrado

```dart
// Para métodos con parámetros nombrados
when(() => mockRepository.updateProduct(
  id: any(named: 'id'),
  product: any(named: 'product'),
)).thenAnswer((_) async => Either.right(tProduct));

verify(() => mockRepository.updateProduct(
  id: any(named: 'id'),
  product: any(named: 'product'),
)).called(1);
```

#### 7.3 any(that:) - Condición personalizada

```dart
// Stubbing con condición
when(() => mockRepository.getProduct(any(that: startsWith('PROD-'))))
    .thenAnswer((_) => Either.right(tProduct));

// Verificación con condición
verify(() => mockRepository.getProduct(any(that: equals('PROD-123')))).called(1);
verify(() => mockRepository.getProduct(any(that: contains('123')))).called(1);
```

### 📊 Tabla de Matchers

| Matcher | Uso | Ejemplo |
|---------|-----|---------|
| `any()` | Cualquier valor posicional | `getProduct(any())` |
| `any(named: 'x')` | Cualquier valor para argumento 'x' | `updateProduct(id: any(named: 'id'))` |
| `any(that: matcher)` | Valor que cumple condición | `any(that: equals('123'))` |
| `captureAny()` | Capturar cualquier valor | `captureAny()` |

---

## 8. Captura de Argumentos

### 🎯 Concepto: "Guarda lo que me pasaron"

A veces necesitas verificar no solo QUE se llamó, sino CON QUÉ valores.

### 📚 captureAny() - El más común

```dart
// Captura el argumento con el que se llamó
final capturedId = verify(() => mockRepository.getProduct(captureAny())).captured;

// capturedId contiene los argumentos
print(capturedId); // ['123']
```

### 📝 Ejemplo completo

```dart
test('should call repository with correct id', () {
  // Arrange
  when(() => mockRepository.getProduct(any())).thenAnswer((_) async => Either.right(tProduct));
  
  // Act
  await getProductUseCase('123');
  
  // Assert - Captura el argumento
  final captured = verify(() => mockRepository.getProduct(captureAny())).captured;
  
  expect(captured.first, '123');
});
```

### 🔄 Capturar argumentos específicos

```dart
// Captura solo el primer argumento de una llamada
final capturedId = verify(
  () => mockRepository.getProduct(captureAny()),
).captured.first;

// Captura todos los argumentos de todas las llamadas
final allIds = verify(
  () => mockRepository.getProduct(captureAny()),
).captured; // [ '123', '456', '789' ]
```

### 🎯 Capturar argumentos de métodos con múltiples parámetros

```dart
// Método: updateProduct({required String id, required Product product})

// Captura ambos argumentos
final captured = verify(
  () => mockRepository.updateProduct(
    id: captureAny(named: 'id'),
    product: captureAny(named: 'product'),
  ),
).captured;

final capturedId = captured[0]['id'];
final capturedProduct = captured[0]['product'];
```

---

## 9. Errores Comunes y Cómo Resolverlos

### ❌ Error 1: "MissingStubError"

**Mensaje:**
```
MissingStubError: 'Method getProduct was not stubbed'
```

**Causa:** Llamaste a un método del mock sin antes configurarlo con `when()`.

**Solución:**
```dart
// ❌ FALLA
when(() => mockRepository.getProduct('123')).thenAnswer((_) async => Either.right(tProduct));
final result = await mockRepository.getProduct('999'); // ¡No stubbed!

// ✅ CORRECTO - Stub todos los casos posibles
when(() => mockRepository.getProduct(any())).thenAnswer((_) async => Either.right(tProduct));
```

---

### ❌ Error 2: "Actual invocations don't match"

**Mensaje:**
```
Actual invocations have same signature but following arguments do not:
getProduct("123")
```

**Causa:** Verificaste con argumentos diferentes a los que realmente se usaron.

**Solución:**
```dart
// ❌ FALLA
verify(() => mockRepository.getProduct('999')).called(1); // Pero se llamó con '123'

// ✅ CORRECTO - Usa any() o el valor correcto
verify(() => mockRepository.getProduct(any())).called(1);
// O
verify(() => mockRepository.getProduct('123')).called(1);
```

---

### ❌ Error 3: "No matching invocation"

**Mensaje:**
```
No matching invocation found for:
  MethodGetProduct(#any)
```

**Causa:** Verificaste un método que nunca fue llamado.

**Solución:**
```dart
// ❌ FALLA - getProduct nunca fue llamado
verify(() => mockRepository.getProduct('123'));

// ✅ CORRECTO - Llama primero al método en el test
await useCase('123');  // Esto llama al repository
verify(() => mockRepository.getProduct('123'));
```

---

### ❌ Error 4: "null is not a subtype of ..."

**Mensaje:**
```
null is not a subtype of Product
```

**Causa:** El mock retornó null en lugar del valor configurado.

**Solución:**
```dart
// ❌ FALLA - Retorna null
when(() => mockRepository.getProduct(any())).thenAnswer((_) => null);

// ✅ CORRECTO - Retorna el tipo correcto
when(() => mockRepository.getProduct(any())).thenAnswer((_) => tProduct);
// O si es Future
when(() => mockRepository.getProduct(any())).thenAnswer((_) async => tProduct);
```

---

### ❌ Error 5: Fallback values no registrados

**Mensaje:**
```
Invalid argument(s): No registered implementation of type Product
```

**Causa:** Usas `any()` con un tipo personalizado sin registrar fallback value.

**Solución:**
```dart
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});
```

---

## 10. Mocktail por Capa de Clean Architecture

Mocktail se usa de manera diferente en cada capa de Clean Architecture. Aquí te explico qué mockear en cada una:

### 📍 Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION                              │
│  ┌─────────────┐                                          │
│  │  Cubit/BLoC │  → MOCKEAMOS UseCases                    │
│  └─────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       DOMAIN                                 │
│  ┌─────────────┐    ┌─────────────┐                       │
│  │   UseCase   │ →  │  Repository │  → MOCKEAMOS         │
│  └─────────────┘    │  (Interface)│    (La interfaz)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        DATA                                 │
│  ┌─────────────┐    ┌─────────────┐                       │
│  │  Repository │ →  │  DataSource │  → MOCKEAMOS         │
│  │    Impl     │    │(Remote/Local)                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        CORE                                 │
│  ┌─────────────┐    ┌─────────────┐                       │
│  │   Services  │ →  │    Utils    │                        │
│  └─────────────┘    └─────────────┘                       │
│         ↑                                                      │
│    MOCKEAMOS (NetworkInfo, Storage, API Client)            │
└─────────────────────────────────────────────────────────────┘
```

### 🏗️ ¿Qué mockear en cada capa?

| Capa | Qué Mockear | Ejemplo |
|------|-------------|---------|
| **Domain** | Repository Interfaces | `MockIProductRepository` |
| **Domain** | UseCases (inyectados) | `MockGetProductUseCase` |
| **Data** | DataSources | `MockProductRemoteDataSource` |
| **Data** | Repository Implementation | Mocks de DataSources |
| **Presentation** | UseCases en Cubits/BLoCs | `MockGetProductUseCase` |
| **Core** | NetworkInfo | `MockNetworkInfo` |
| **Core** | Storage/Session | `MockSharedPreferences` |

### 🎯 Regla de Oro

> **Mockea las dependencias externas, nunca la lógica interna.**

- En Domain: Mockeas el Repository (la dependencia externa al dominio)
- En Data: Mockeas los DataSources (la dependencia externa a los datos)
- En Presentation: Mockeas los UseCases (la dependencia externa a la UI)

---

## 11. Resumen Cheatsheet

### 📋 Configuración

```yaml
# pubspec.yaml
dev_dependencies:
  mocktail: ^1.0.4
```

```dart
// test file
import 'package:mocktail/mocktail.dart';

class MockIProductRepository extends Mock implements IProductRepository {}
```

### 🔧 Stubbing

```dart
// Respuesta simple
when(() => mock.method(args)).thenAnswer((_) => value);

// Excepción
when(() => mock.method(args)).thenThrow(Exception('error'));

// Múltiples respuestas
when(() => mock.method(args))
    .thenAnswer((_) => value1)
    .thenAnswer((_) => value2);
```

### ✅ Verificación

```dart
verify(() => mock.method(args)).called(1);      // Exactamente 1 vez
verify(() => mock.method(args)).called(n);      // n veces
verifyNever(() => mock.method(any()));           // Nunca

verifyZeroInteractions(mock);             // Ninguna interacción
verifyNoMoreInteractions(mock);           // No más interacciones
```

### 🎯 Matchers

```dart
any()                    // Cualquier valor
any(named: 'param')      // Cualquier valor para argumento nombrado
any(that: matcher)       // Valor que cumple condición
captureAny()             // Capturar cualquier valor
captureAny(named: 'x')   // Capturar argumento nombrado
```

### Fallback Values

```dart
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});
```

---

## 🎉 ¡Felicitaciones!

Has completado la teoría de Mocktail. Ahora sabes:

- ✅ Qué es Mocktail y por qué usarlo
- ✅ Configurar el proyecto sin build_runner
- ✅ Crear Mocks con `extends Mock implements`
- ✅ Stubbing con `when()` y `thenAnswer()`
- ✅ Verificación con `verify()`
- ✅ Matchers avanzados
- ✅ Captura de argumentos
- ✅ Fallback values
- ✅ Errores comunes y soluciones

---

## 🚀 Siguiente Paso

**Práctica:** [02b-practica-mocktail.md](./02b-practica-mocktail.md)

> En la práctica pondrás todo esto en acción con ejercicios paso a paso.

---

## 📚 Recursos Adicionales

- [Documentación oficial de Mocktail](https://pub.dev/packages/mocktail)
- [Tutorial oficial de bloc_test](https://bloclibrary.dev/bloc-test)

---

**Última actualización:** 2026-03-25
**Versión:** 2.0.0
