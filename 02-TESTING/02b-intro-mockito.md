# 🧪 Parte 2b: Introducción a Mockito - Guía Completa

> **¿De qué trata esta parte?** Esta es una guía completa sobre Mockito, una herramienta poderosa para crear mocks automáticos. **IMPORTANTE:** Esta guía assumes que ya dominas los Fakes manuales (Parte 2a). Si no los has dominado, te recomiendo estudiar esa parte primero.

---

## 📋 Índice

1. [Introducción: ¿Qué es Mockito?](#1-introducción-qué-es-mockito)
2. [¿Cuándo usar Mockito?](#2-cuándo-usar-mockito)
3. [Configuración del Proyecto](#3-configuración-del-proyecto)
4. [Anatomía de @GenerateMocks](#4-anatomía-de-generatemocks)
5. [La API de Stubbing: when()](#5-la-api-de-stubbing-when)
6. [La API de Verificación: verify()](#6-la-api-de-verificación-verify)
7. [Matchers: any(), anyNamed(), argThat()](#7-matchers-any-anynamed-argthat)
8. [Captura de Argumentos](#8-captura-de-argumentos)
9. [Mockito vs Mocktail](#9-mockito-vs-mocktail)
10. [Errores Comunes y Cómo Resolverlos](#10-errores-comunes-y-cómo-resolverlos)
11. [Mejores Prácticas](#11-mejores-prácticas)
12. [Mockito por Capa de Clean Architecture](#12-mockito-por-capa-de-clean-architecture)
13. [Resumen Cheatsheet](#13-resumen-cheatsheet)

---

## 1. Introducción: ¿Qué es Mockito?

### 🎭 La Analogía del Director de Cine

Imagina que estás rodando una película:

| En un Fake Manual | En Mockito |
|------------------|------------|
| **Tú escribes el guión** - Defines exactamente qué dice cada actor | **Un actor entrenado** - El actor (mock) sabe improvisar según las instrucciones que le das |
| **Control total pero más trabajo** | **Menos trabajo, más flexibilidad** |
| Ejemplo: Escribes cada diálogo manualmente | Ejemplo: Das instrucciones generales: "Cuando te pregunten X, responde Y" |

### 📦 ¿Qué es Mockito?

Mockito es una biblioteca que **genera automáticamente** implementaciones falsas de interfaces. En lugar de escribir a mano una clase que implemente una interfaz, Mockito la crea por ti.

```dart
// ❌ CON FAKE MANUAL - Tú escribes todo esto
class FakeProductRepository implements IProductRepository {
  bool shouldFail = false;
  Product? productToReturn;
  
  @override
  Future<Either<Failure, Product>> getProduct(String id) async {
    if (shouldFail) return Either.left(ServerFailure());
    return Either.right(productToReturn!);
  }
}

// ✅ CON MOCKITO - ¡Lo genera automáticamente!
late MockIProductRepository mockRepository;  // ← Generado por Mockito

// Tú solo dices qué retornar:
when(mockRepository.getProduct(any)).thenAnswer((_) async => Either.right(tProduct));
```

---

## 2. ¿Cuándo Usar Mockito?

### ✅ Usa Mockito cuando:

| Señal | Descripción |
|-------|-------------|
| 🏢 Proyecto grande | Más de 50 tests con Fakes |
| 👥 Equipo grande | Necesitas consistencia entre desarrolladores |
| 🔄 Interfaces cambian frecuentemente | Evita regenerar muchos Fakes manualmente |
| 🔍 Verificaciones estrictas | Necesitas verificar argumentos exactos |
| ⚡ POCs rápidos | Necesitas prototipar rápido |

### ❌ Sigue usando Fakes cuando:

| Situación | Descripción |
|----------|-------------|
| 🏠 Proyecto pequeño | Menos de 20-30 tests |
| 📚 Estás aprendiendo | Los Fakes son más fáciles de entender |
| 🔧 Depuración frecuente | El código de los Fakes es más legible |
| 🎓 Entre equipo junior | Curva de aprendizaje más suave |

### 📊 Comparación Final

| Característica | Fake Manual | Mockito |
|---------------|-------------|---------|
| **Setup inicial** | Escribes el código | Generas con build_runner |
| **Tiempo por test** | Medio (ya tienes todo listo) | Rápido (configuras sobre la marcha) |
| **Verificación de llamadas** | Manual (contadores) | Automática (verify) |
| **Verificación de argumentos** | Manual (guardas parámetros) | Automática (verify con parámetros) |
| **Curva de aprendizaje** | ⭐ Baja | ⭐⭐ Media |
| **Mantenimiento** | Alto (cambios manuales) | Bajo (regeneras) |
| **Ideal para** | Aprendizaje, proyectos pequeños | Proyectos enterprise |

---

## 3. Configuración del Proyecto

### 📦 Paso 1: Añadir dependencias

En tu `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.0          # La librería principal
  build_runner: ^2.4.0      # Para generar el código
  bloc_test: ^9.1.0         # (Ya lo tienes probablemente)
```

```bash
flutter pub get
```

### 📝 Paso 2: Archivo build.yaml (opcional pero recomendado)

Crea `build.yaml` en la raíz del proyecto para configurar cómo se generan los mocks:

```yaml
# build.yaml
targets:
  $default:
    builders:
      mockito|mockBuilder:
        generate_for:
          include:
            - test/**/*_test.dart
        options:
          # Opciones avanzadas (opcional)
          stubOnWeakType: true
          implicitCast: true
```

> **Nota:** Si no creas `build.yaml`, Mockito igualmente funcionará con su configuración por defecto.

---

## 4. Anatomía de @GenerateMocks

### 📝 La Anotación Mágica

```dart
import 'package:mockito/annotations.dart';

// Esta anotación le dice a Mockito: "Genera un mock para esta interfaz"
@GenerateMocks([IProductRepository])
part 'product_repository_test.mocks.dart';
```

### 🔍 Qué genera Mockito

Cuando ejecutas `build_runner`, Mockito genera un archivo `.mocks.dart` con:

```dart
// product_repository_test.mocks.dart (GENERADO AUTOMÁTICAMENTE)
class MockIProductRepository extends Mock implements IProductRepository {}
```

### 🎯 Partes del Código

```
┌─────────────────────────────────────────────────────────────┐
│  TU ARCHIVO DE TEST                                         │
│  product_repository_test.dart                               │
├─────────────────────────────────────────────────────────────┤
│  import 'package:mockito/annotations.dart';                 │
│  @GenerateMocks([IProductRepository])  ← Indicas qué mock  │
│  part 'product_repository_test.mocks.dart'; ← Se genera    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  ARCHIVO GENERADO                                           │
│  product_repository_test.mocks.dart                         │
├─────────────────────────────────────────────────────────────┤
│  class MockIProductRepository extends Mock                   │
│      implements IProductRepository {}  ← ¡El mock!         │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 Cómo ejecutar la generación

```bash
# Generar los mocks
dart run build_runner build --delete-conflicting-outputs

# O si estás en Flutter
flutter pub run build_runner build --delete-conflicting-outputs

# Para solo regenerar cuando hay cambios (más rápido)
dart run build_runner build --delete-conflicting-outputs
```

### ⚠️ Importante: Cuándo regenerar

| Cuando... | Debes regenerar |
|-----------|-----------------|
| Añades un nuevo método a la interfaz | ✅ Sí |
| Cambias parámetros de un método | ✅ Sí |
| Añades un nuevo test que necesita un mock | ✅ Sí |
| Ejecutas los tests y funciona | ❌ No |

---

## 5. La API de Stubbing: when()

### 🎯 Concepto: "Cuando ocurra X, retorna Y"

El stubbing le dice al mock: "Cuando alguien llame a este método con estos argumentos, responde así".

### 📚Métodos Principales

#### 5.1 thenAnswer() - Respuesta personalizada

```dart
// Cuando llamen a getProduct('1'), retorna Right(tProduct)
when(mockRepository.getProduct('1'))
    .thenAnswer((_) async => Either.right(tProduct));
```

**Versión acortada (solo para返回值 simples):**
```dart
// Si retornara solo el producto (sin Either)
when(mockRepository.getProduct('1')).thenAnswer((_) => tProduct);

// Para Future simples
when(mockRepository.getProduct('1')).thenAnswer((_) async => tProduct);
```

#### 5.2 thenReturn() - Retorno directo (sin async)

```dart
// Para métodos síncronos o que ya tienen el valor listo
when(mockRepository.getProductCount()).thenReturn(5);
when(mockRepository.isProductInStock('1')).thenReturn(true);
```

#### 5.3 thenThrow() - Lanzar excepción

```dart
// Cuando alguien llame a getProduct, lanza una excepción
when(mockRepository.getProduct(any)).thenThrow(Exception('Network error'));

// Para excepciones específicas
when(mockRepository.getProduct('999'))
    .thenThrow(ServerException('Product not found'));
```

### 🔗 Encadenando respuestas

```dart
// Primera llamada retorna X, segunda retorna Y
when(mockRepository.getProduct(any)).thenAnswer(
  (_) async => Either.right(tProduct),
).thenAnswer(
  (_) async => Either.left(ServerFailure()),
);

// Versión más legible
when(mockRepository.getProduct(any))
    .thenAnswer((_) async => Either.right(tProduct))
    .thenAnswer((_) async => Either.left(ServerFailure()));
```

### 🎲thenAnswer() vs thenReturn()

| Método | Cuándo usarlo |
|--------|---------------|
| `thenAnswer()` | Cuando hay lógica async o necesitas acceder a los argumentos |
| `thenReturn()` | Cuando el valor ya está disponible y es síncrono |

```dart
// ✅ thenAnswer - necesitas lógica
when(mockRepository.getProduct(any)).thenAnswer((invocation) async {
  final id = invocation.positionalArguments[0];
  if (id == '999') {
    return Either.left(ProductNotFoundFailure());
  }
  return Either.right(tProduct);
});

// ✅ thenReturn - valor simple
when(mockRepository.getProductCount()).thenReturn(10);
```

### 🔑 Importante: El Orden de los when()

**¡El orden importa!** Mockito evalúa los `when()` en orden de específico a general.

```dart
// ❌ INCORRECTO - any() primero hace que nunca llegue al específico
when(mockRepository.getProduct(any)).thenReturn(tProduct);
when(mockRepository.getProduct('999')).thenReturn(null); // ¡Nunca se ejecuta!

// ✅ CORRECTO - Primero lo específico, luego lo general
when(mockRepository.getProduct('999')).thenReturn(null);
when(mockRepository.getProduct(any)).thenReturn(tProduct);
```

---

## 6. La API de Verificación: verify()

### 🎯 Concepto: "¿Realmente se llamó?"

La verificación confirma que el código que estás probando realmente llamó a los métodos correctos con los argumentos correctos.

### 📚 Métodos de Verificación

#### 6.1 verify() - Verificar que se llamó

```dart
// Verifica que se llamó exactamente una vez
verify(mockRepository.getProduct('1')).called(1);

// Equivalente a called(1)
verify(mockRepository.getProduct('1'));
```

#### 6.2 verifyNever() - Verificar que NO se llamó

```dart
// Verifica que NUNCA se llamó
verifyNever(mockRepository.deleteProduct(any));
verify(mockRepository.createProduct(any)).called(0);
```

#### 6.3 verify(times(n)) - Verificar veces específicas

```dart
verify(mockRepository.getProduct(any)).called(3);       // Exactamente 3 veces
verify(mockRepository.getProduct(any)).called(greaterThan(1));  // Más de 1
verify(mockRepository.getProduct(any)).called(lessThan(5));    // Menos de 5
```

#### 6.4 verifyZeroInteractions() - Sin ninguna interacción

```dart
// Verifica que el mock nunca fue tocado
verifyZeroInteractions(mockRepository);
```

#### 6.5 verifyNoMoreInteractions() - No más interacciones

```dart
// Verifica que después de las verificaciones anteriores, no hubo más llamadas
verify(mockRepository.getProduct('1')).called(1);
verifyNoMoreInteractions(mockRepository);
```

### 🔍 Verificación con Argumentos

```dart
// Verifica que se llamó con UNO de estos argumentos
verify(mockRepository.getProduct(any)).called(1);

// Verifica que se llamó con un argumento EXACTO
verify(mockRepository.getProduct('123')).called(1);

// Verifica argumentos específicos con anyNamed
when(mockRepository.updateProduct(id: anyNamed('id'), product: anyNamed('product')))
    .thenAnswer((_) async => Either.right(tProduct));

verify(mockRepository.updateProduct(id: '123', product: tProduct)).called(1);
```

---

## 7. Matchers: any(), anyNamed(), argThat()

### 🎯 Concepto: "No me importa el valor exacto"

Los matchers te permiten verificar o stubbing sin especificar valores exactos.

### 📚 Tipos de Matchers

#### 7.1 any() - Cualquier valor

```dart
// Stubbing: No importa qué ID pasen, retorna tProduct
when(mockRepository.getProduct(any)).thenAnswer((_) => Either.right(tProduct));

// Verificación: Verifica que se llamó con ALGÚN argumento
verify(mockRepository.getProduct(any)).called(1);
```

#### 7.2 anyNamed() - Cualquier valor para argumento nominado

```dart
// Para métodos con parámetros nombrados
when(mockRepository.updateProduct(
  id: anyNamed('id'),
  product: anyNamed('product'),
)).thenAnswer((_) async => Either.right(tProduct));

verify(mockRepository.updateProduct(
  id: anyNamed('id'),
  product: anyNamed('product'),
)).called(1);
```

#### 7.3 argThat() - Condición personalizada

```dart
// Stubbing con condición
when(mockRepository.getProduct(argThat(startsWith('PROD-'))))
    .thenAnswer((_) => Either.right(tProduct));

// Verificación con condición
verify(mockRepository.getProduct(argThat(equals('PROD-123')))).called(1);
verify(mockRepository.getProduct(argThat(contains('123')))).called(1);
```

### 📊 Tabla de Matchers

| Matcher | Uso | Ejemplo |
|---------|-----|---------|
| `any()` | Cualquier valor posicional | `getProduct(any)` |
| `anyNamed('x')` | Cualquier valor para argumento 'x' | `updateProduct(id: anyNamed('id'))` |
| `argThat(matcher)` | Valor que cumple condición | `argThat(equals('123'))` |
| `startsWith('x')` | String que comienza con | `argThat(startsWith('PROD-'))` |
| `contains('x')` | String que contiene | `argThat(contains('123'))` |
| `greaterThan(n)` | Número mayor a n | `argThat(greaterThan(0))` |
| `anything()` | Alias de any() | `anything()` |

---

## 8. Captura de Argumentos

### 🎯 Concepto: "Guarda lo que me pasaron"

A veces necesitas verificar no solo QUE se llamó, sino CON QUÉ valores.

### 📚 Captured() - El más común

```dart
import 'package:mockito/mockito.dart';

// Declara el capturador
final capturedId = verify(mockRepository.getProduct(captureAny())).captured;

// capturedId contiene los argumentos con los que se llamó
print(capturedId); // ['123']
```

### 📝 Ejemplo completo

```dart
test('should call repository with correct id', () {
  // Arrange
  when(mockRepository.getProduct(any)).thenAnswer((_) async => Either.right(tProduct));
  
  // Act
  await getProductUseCase('123');
  
  // Assert - Captura el argumento
  final captured = verify(mockRepository.getProduct(captureAny())).captured;
  
  expect(captured.first, '123');
});
```

### 🔄 Capturar argumentos específicos

```dart
// Captura solo el primer argumento de una llamada específica
final capturedId = verify(
  mockRepository.getProduct(captureAny()),
).captured.first;

// Captura todos los argumentos de todas las llamadas
final allIds = verify(
  mockRepository.getProduct(captureAny()),
).captured; // [ '123', '456', '789' ]
```

### 🎯 Capturar argumentos de métodos con múltiples parámetros

```dart
// Método: updateProduct({required String id, required Product product})

// Captura ambos argumentos
final captured = verify(
  mockRepository.updateProduct(
    id: captureAnyNamed('id'), 
    product: captureAnyNamed('product'),
  ),
).captured;

final capturedId = captured[0]['id'];        // Primer argumento nombrado
final capturedProduct = captured[0]['product']; // Segundo argumento nombrado
```

---

## 9. Mockito vs Mocktail

### 📦 ¿Qué es Mocktail?

Mocktail es una alternativa a Mockito **sin generación de código**. Funciona de manera similar pero no requiere `build_runner`.

### 📊 Comparación

| Característica | Mockito | Mocktail |
|---------------|---------|----------|
| **Generación de código** | Sí (`build_runner`) | No |
| **Setup inicial** | Más complejo | Más simple |
| **Curva de aprendizaje** | Media | Baja |
| **Compatibilidad** | Dart 2.18+ | Dart 2.18+ |
| **Necesitas la interfaz** | Sí | Sí (importada) |
| **Verificación** | verify() | verify() |

### 🔧 Configuración de Mocktail

```yaml
dev_dependencies:
  mocktail: ^1.0.0
```

### 📝 Uso de Mocktail

```dart
import 'package:mocktail/mocktail.dart';

// En Mocktail NO usas @GenerateMocks
// Simplesmente extends Mock

class MockProductRepository extends Mock implements IProductRepository {}

// Pero... Mocktail requiere registrar los fallback values
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});

// El uso es idéntico
when(() => mockRepository.getProduct(any())).thenAnswer((_) async => Either.right(tProduct));
verify(() => mockRepository.getProduct('123')).called(1);
```

### 🤔 ¿Cuál elegir?

| Usa Mockito cuando... | Usa Mocktail cuando... |
|----------------------|----------------------|
| Tienes muchas interfaces | Proyecto pequeño |
| Quieres verificación estricta | Quieres evitar build_runner |
| Estás en un equipo enterprise | Estás aprendiendo |
| Necesitas todas las funciones avanzadas | Solo necesitas lo básico |

---

## 10. Errores Comunes y Cómo Resolverlos

### ❌ Error 1: "MissingStubError"

**Mensaje:**
```
MissingStubError: 'Method getProduct was not stubbed'
```

**Causa:** Llamaste a un método del mock sin antes configurarlo con `when()`.

**Solución:**
```dart
// ❌ FALLA
when(mockRepository.getProduct('123')).thenAnswer((_) async => Either.right(tProduct));
final result = await mockRepository.getProduct('999'); // ¡No stubbed!

// ✅ CORRECTO - Stub todos los casos posibles
when(mockRepository.getProduct(any())).thenAnswer((_) async => Either.right(tProduct));
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
verify(mockRepository.getProduct('999')).called(1); // Pero se llamó con '123'

// ✅ CORRECTO - Usa any() o el valor correcto
verify(mockRepository.getProduct(any())).called(1);
// O
verify(mockRepository.getProduct('123')).called(1);
```

---

### ❌ Error 3: "Expected a numeric value but got Never"

**Mensaje:**
```
Expected a numeric value but got Never for method...
```

**Causa:** Usaste `verifyNever()` incorrectamente.

**Solución:**
```dart
// ❌ FALLA
verifyNever(mockRepository.deleteProduct(any)); // Syntax error

// ✅ CORRECTO
verify(mockRepository.deleteProduct(any)).called(0);
// O
verifyNever(() => mockRepository.deleteProduct(any));
// O (más claro)
verify(mockRepository.deleteProduct(any)).called(never);
```

---

### ❌ Error 4: "No matching invocation"

**Mensaje:**
```
No matching invocation found for:
  MethodGetProduct(#any)
```

**Causa:** Verificaste un método que nunca fue llamado.

**Solución:**
```dart
// ❌ FALLA - getProduct nunca fue llamado
verify(mockRepository.getProduct('123'));

// ✅ CORRECTO - Llama primero al método en el test
await useCase('123');  // Esto llama al repository
verify(mockRepository.getProduct('123'));
```

---

### ❌ Error 5: "null is not a subtype of ..."

**Mensaje:**
```
null is not a subtype of Product
```

**Causa:** El mock retornó null en lugar del valor configurado.

**Solución:**
```dart
// ❌ FALLA - tProduct es null
when(mockRepository.getProduct(any)).thenAnswer((_) => null);

// ✅ CORRECTO - Retorna el tipo correcto
when(mockRepository.getProduct(any)).thenAnswer((_) => tProduct);
// O si es Future
when(mockRepository.getProduct(any)).thenAnswer((_) async => tProduct);
```

---

### ❌ Error 6: Fallback values no registrados (Mocktail)

**Mensaje:**
```
Invalid argument(s): No registered implementation of type Product
```

**Causa:** Usas Mocktail y no registraste un fallback value.

**Solución:**
```dart
class FakeProduct extends Fake implements Product {}

setUpAll(() {
  registerFallbackValue(FakeProduct());
});
```

---

## 11. Mejores Prácticas

### ✅ Haz:

1. **Un mock por test o grupo**
   ```dart
   late MockIProductRepository mockRepository;
   
   setUp(() {
     mockRepository = MockIProductRepository();
   });
   ```

2. **Usa setUp para configuración común**
   ```dart
   setUp(() {
     mockRepository = MockIProductRepository();
     useCase = GetProductUseCase(mockRepository);
     when(() => mockRepository.getProduct(any()))
         .thenAnswer((_) async => Either.right(tProduct));
   });
   ```

3. **Limpia entre tests**
   ```dart
   tearDown(() {
     // No necesitas limpiar los mocks de Mockito
     // Pero es buena práctica verificar interacciones
   });
   ```

4. **Nombra los tests descriptivamente**
   ```dart
   test('should return Product when repository returns success', () {});
   test('should return failure when repository throws exception', () {});
   ```

### ❌ No Hacer:

1. **No stub en el test cuando no lo necesitas**
   ```dart
   // ❌ Sobrestubbing
   when(mockRepository.getProduct(any())).thenAnswer((_) async => Either.right(tProduct));
   when(mockRepository.updateProduct(any(), any())).thenAnswer((_) async => Either.right(tProduct));
   when(mockRepository.deleteProduct(any())).thenAnswer((_) async => Either.right(null));
   
   // ✅ Solo lo que necesitas
   when(mockRepository.getProduct(any())).thenAnswer((_) async => Either.right(tProduct));
   ```

2. **No verifiques todo**
   ```dart
   // ❌ Exceso de verificación
   verify(mockRepository.getProduct('123'));
   verify(mockRepository.getProduct('123'));
   verify(mockRepository.getProduct('123'));
   
   // ✅ Lo que importa
   verify(mockRepository.getProduct('123')).called(1);
   ```

3. **No ignores los errores de stubbing**
   ```dart
   // ❌ Peligroso
   when(mockRepository.getProduct(any())).thenAnswer((_) async => null);
   
   // ✅ Especifica el tipo de retorno correcto
   when(mockRepository.getProduct(any())).thenAnswer((_) async => Either.right(tProduct));
   ```

---

## 12. Mockito por Capa de Clean Architecture

Mockito se usa de manera diferente en cada capa de Clean Architecture. Aquí te explico qué mockear en cada una:

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
│  │   UseCase   │ →  │ Repository  │  → MOCKEAMOS         │
│  └─────────────┘    │ (Interface) │    (La interfaz)      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        DATA                                 │
│  ┌─────────────┐    ┌─────────────┐                       │
│  │ Repository  │ →  │ DataSource  │  → MOCKEAMOS         │
│  │   Impl      │    │(Remote/Local)                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        CORE                                 │
│  ┌─────────────┐    ┌─────────────┐                       │
│  │   Services │ →  │   Utils    │                        │
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
| **Data** | Repository Implementation |Mocks de DataSources |
| **Presentation** | UseCases en Cubits/BLoCs | `MockGetProductUseCase` |
| **Core** | NetworkInfo | `MockNetworkInfo` |
| **Core** | Storage/Session | `MockSharedPreferences` |

### 🎯 Regla de Oro

> **Mockea las dependencias externas, nunca la lógica interna.**

- En Domain: Mockeas el Repository (la dependencia externa al dominio)
- En Data: Mockeas los DataSources (la dependencia externa a los datos)
- En Presentation: Mockeas los UseCases (la dependencia externa a la UI)

---

## 13. Resumen Cheatsheet

### 📋 Configuración

```yaml
# pubspec.yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

```dart
// test file
@GenerateMocks([IProductRepository])
import 'product_test.mocks.dart';
```

```bash
dart run build_runner build --delete-conflicting-outputs
```

### 🔧 Stubbing

```dart
// Respuesta simple
when(mock.method(args)).thenAnswer((_) => value);

// Excepción
when(mock.method(args)).thenThrow(Exception('error'));

// Multiple respuestas
when(mock.method(args))
    .thenAnswer((_) => value1)
    .thenAnswer((_) => value2);
```

### ✅ Verificación

```dart
verify(mock.method(args)).called(1);      // Exactamente 1 vez
verify(mock.method(args)).called(n);      // n veces
verify(mock.method(args)).called(never); // Nunca
verify(mock.method(args)).called(greaterThan(0)); // Al menos 1

verifyZeroInteractions(mock);             // Ninguna interacción
verifyNoMoreInteractions(mock);           // No más interacciones
```

### 🎯 Matchers

```dart
any()                    // Cualquier valor
anyNamed('param')        // Cualquier valor para argumento nombrado
argThat(matcher)         // Valor que cumple condición
```

### 📦 Captura

```dart
final captured = verify(mock.method(captureAny())).captured;
final value = captured.first;
```

---

## 🎉 ¡Felicitaciones!

Has completado la teoría de Mockito. Ahora sabes:

- ✅ Qué es Mockito y cuándo usarlo
- ✅ Configurar el proyecto correctamente
- ✅ Usar @GenerateMocks
- ✅ Stubbing con when() y thenAnswer()
- ✅ Verificación con verify()
- ✅ Matchers avanzados
- ✅ Captura de argumentos
- ✅ Diferencias con Mocktail
- ✅ Errores comunes y soluciones
- ✅ Mejores prácticas

---

## 🚀 Siguiente Paso

**Práctica:** [02b-practica-mockito.md](./02b-practica-mockito.md)

> En la práctica pondrás todo esto en acción con ejercicios paso a paso.

---

## 📚 Recursos Adicionales

- [Documentación oficial de Mockito](https://pub.dev/packages/mockito)
- [Documentación de Mocktail](https://pub.dev/packages/mocktail)
- [Tutorial oficial de bloc_test](https://bloclibrary.dev/bloc-test)

---

**Última actualización:** 2026-03-25
**Versión:** 1.0.0
