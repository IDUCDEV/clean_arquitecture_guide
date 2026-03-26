# 🏋️ 02b: Práctica - Mockito Paso a Paso

> **¿De qué trata esta práctica?** De crear tu primer Mock con Mockito desde cero. Vamos paso a paso, ejercicios progresivos. Usaremos ejemplos en diferentes capas de Clean Architecture para que veas cómo se aplica en cada una.

---

## ⚠️ Nota Importante: ¿Cuándo usar Mockito?

| Capa | Herramienta principal | ¿Cuándo usar Mockito? |
|------|---------------------|----------------------|
| **Domain** | Mockito | ✅ Siempre - para Repository Interfaces |
| **Data** | Mockito | ✅ Siempre - para DataSources |
| **Presentation** | **bloc_test** | ⚠️ Para estados + Mockito para UseCases |
| **Core** | Mockito | ✅ Para servicios como NetworkInfo |

> **La regla:** Mockea las **dependencias externas** de cada capa.

---

## 📋 Índice General

### Fundamentos de Mockito
- [Ejercicio 1: Preparar el entorno](#ejercicio-1-preparar-el-entorno)
- [Ejercicio 2: Crear la interfaz](#ejercicio-2-crear-la-interfaz)
- [Ejercicio 3: Generar el primer Mock](#ejercicio-3-generar-el-primer-mock)
- [Ejercicio 4: Primer test con thenAnswer](#ejercicio-4-primer-test-con-thenanswer)
- [Ejercicio 5: Testear caso de error con thenThrow](#ejercicio-5-testear-caso-de-error-con-thenthrow)
- [Ejercicio 6: Verificación básica con verify](#ejercicio-6-verificación-básica-con-verify)

### Mockito por Capa (Aplicación Real)
- [CAPA DOMAIN: Repository + UseCase](#capa-domain-repository--usecase)
- [CAPA DATA: DataSources (Remote/Local)](#capa-data-datasources-remotelocal)
- [CAPA PRESENTATION: Cubits/BLoCs](#capa-presentation-cubitsblocs) ← bloc_test + Mockito
- [CAPA CORE: Services Compartidos](#capa-core-services-compartidos)

---

## 🎬 Antes de Empezar

### 📦 Dependencias necesarias

Asegúrate de tener en tu `pubspec.yaml`:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.0
  build_runner: ^2.4.0
  bloc_test: ^9.1.0
```

```bash
flutter pub get
```

---

## Ejercicio 1: Preparar el entorno

### 📝 Tu Misión

Crear la estructura de carpetas para los tests.

### ✅ Paso 1: Crea la estructura

```bash
mkdir -p test/helpers
mkdir -p test/features/products/domain/entities
mkdir -p test/features/products/domain/usecases
mkdir -p test/features/products/data/datasources
mkdir -p test/features/products/data/repositories
mkdir -p test/features/products/presentation/cubit
```

---

## Ejercicio 2: Crear la interfaz

### 📝 Tu Misión

Crear la interfaz `IProductRepository` y entidades que usaremos en los tests.

### ✅ Paso 1: Crea la entidad Product

Crea `test/features/products/domain/entities/product.dart`:

```dart
class Product {
  final String id;
  final String name;
  final double price;
  final int stock;

  const Product({
    required this.id,
    required this.name,
    required this.price,
    required this.stock,
  });

  Product copyWith({String? id, String? name, double? price, int? stock}) {
    return Product(
      id: id ?? this.id,
      name: name ?? this.name,
      price: price ?? this.price,
      stock: stock ?? this.stock,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Product &&
        other.id == id &&
        other.name == name &&
        other.price == price &&
        other.stock == stock;
  }

  @override
  int get hashCode => Object.hash(id, name, price, stock);
}
```

### ✅ Paso 2: Crea la interfaz del Repository

Crea `test/features/products/domain/repositories/product_repository.dart`:

```dart
import 'package:dartz/dartz.dart';

abstract class IProductRepository {
  Future<Either<Failure, Product>> getProduct(String id);
  Future<Either<Failure, List<Product>>> getAllProducts();
  Future<Either<Failure, Product>> createProduct(Product product);
  Future<Either<Failure, Product>> updateProduct(Product product);
  Future<Either<Failure, void>> deleteProduct(String id);
}

class Failure {
  final String message;
  const Failure(this.message);
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class NotFoundFailure extends Failure {
  const NotFoundFailure(super.message);
}
```

### ✅ Paso 3: Crea el UseCase

Crea `test/features/products/domain/usecases/get_product_usecase.dart`:

```dart
import 'package:dartz/dartz.dart';
import '../entities/product.dart';
import '../repositories/product_repository.dart';

class GetProductUseCase {
  final IProductRepository repository;

  GetProductUseCase({required this.repository});

  Future<Either<Failure, Product>> call(String id) async {
    return await repository.getProduct(id);
  }
}
```

### ✅ Paso 4: Verifica que compila

```bash
dart analyze test/features/products/domain/
```

---

## Ejercicio 3: Generar el primer Mock

### 📝 Tu Misión

Crear el primer test con la anotación `@GenerateMocks` y generar el código.

### ✅ Paso 1: Crea el archivo de test

Crea `test/features/products/domain/usecases/get_product_usecase_test.dart`:

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/features/products/domain/entities/product.dart';
import 'package:test/features/products/domain/repositories/product_repository.dart';
import 'package:test/features/products/domain/usecases/get_product_usecase.dart';

@GenerateMocks([IProductRepository])
import 'get_product_usecase_test.mocks.dart';

void main() {
  late MockIProductRepository mockRepository;
  late GetProductUseCase useCase;

  setUp(() {
    mockRepository = MockIProductRepository();
    useCase = GetProductUseCase(repository: mockRepository);
  });

  // Tests irán aquí...
}
```

### ✅ Paso 2: Genera el Mock

```bash
dart run build_runner build --delete-conflicting-outputs
```

### ✅ Paso 3: Verifica que se generó

```bash
ls test/features/products/domain/usecases/
```

**Resultado esperado:**
```
get_product_usecase_test.dart
get_product_usecase_test.mocks.dart  ← ¡Generado!
```

---

## Ejercicio 4: Primer test con thenAnswer

### 📝 Tu Misión

Testear el caso de éxito de `GetProductUseCase` usando `thenAnswer()`.

### ✅ Añade el test de éxito

```dart
void main() {
  late MockIProductRepository mockRepository;
  late GetProductUseCase useCase;

  setUp(() {
    mockRepository = MockIProductRepository();
    useCase = GetProductUseCase(repository: mockRepository);
  });

  const tProductId = 'prod-123';
  const tProduct = Product(
    id: tProductId,
    name: 'Laptop Pro',
    price: 1299.99,
    stock: 10,
  );

  group('GetProductUseCase', () {
    test('should return Product when repository returns success', () async {
      // ARRANGE: Configurar el mock
      when(mockRepository.getProduct(any)).thenAnswer(
        (_) async => const Right(tProduct),
      );

      // ACT: Ejecutar el UseCase
      final result = await useCase(tProductId);

      // ASSERT: Verificar resultado
      expect(result, equals(const Right(tProduct)));
      verify(mockRepository.getProduct(tProductId)).called(1);
    });
  });
}
```

### ✅ Ejecuta el test

```bash
flutter test test/features/products/domain/usecases/get_product_usecase_test.dart
```

---

## Ejercicio 5: Testear caso de error con thenThrow

### 📝 Tu Misión

Testear el caso donde el repository lanza una excepción.

### ✅ Añade el test de error

```dart
group('GetProductUseCase - error cases', () {
  test('should return Failure when repository throws exception', () async {
    when(mockRepository.getProduct(any)).thenThrow(
      Exception('Network error'),
    );

    final result = await useCase(tProductId);

    expect(result.isLeft(), true);
  });

  test('should return NotFoundFailure when product does not exist', () async {
    when(mockRepository.getProduct(any)).thenAnswer(
      (_) async => const Left(NotFoundFailure('Product not found')),
    );

    final result = await useCase('nonexistent-id');

    expect(result.isLeft(), true);
    result.fold(
      (failure) => expect(failure, isA<NotFoundFailure>()),
      (_) => fail('Should have returned failure'),
    );
  });
});
```

---

## Ejercicio 6: Verificación básica con verify

### 📝 Tu Misión

Aprender a verificar que el UseCase realmente llamó al repository.

### ✅ Añade tests de verificación

```dart
group('Verification', () {
  test('should call repository exactly once', () async {
    when(mockRepository.getProduct(any)).thenAnswer(
      (_) async => const Right(tProduct),
    );

    await useCase(tProductId);

    verify(mockRepository.getProduct(tProductId)).called(1);
  });

  test('should verify zero interactions', () {
    verifyZeroInteractions(mockRepository);
  });
});
```

---

# 🏗️ MOCKITO POR CAPA - Aplicación Real

Ahora vamos a ver cómo usar Mockito en **cada capa de Clean Architecture** con ejemplos prácticos y reales.

---

## CAPA DOMAIN: Repository + UseCase

### 📍 ¿Qué mockeamos aquí?

```
DOMAIN
├── Entities          → No necesitamos mocks (son datos puros)
├── Repository        → ✅ MOCKEAMOS la interfaz
└── UseCases          → ✅ MOCKEAMOS el Repository
```

### 🎯 Ejemplo: Testeando GetProductsUseCase con múltiples métodos

Crea `test/features/products/domain/usecases/get_all_products_usecase.dart`:

```dart
import 'package:dartz/dartz.dart';
import '../entities/product.dart';
import '../repositories/product_repository.dart';

class GetAllProductsUseCase {
  final IProductRepository repository;

  GetAllProductsUseCase({required this.repository});

  Future<Either<Failure, List<Product>>> call() async {
    return await repository.getAllProducts();
  }
}
```

Crea `test/features/products/domain/usecases/get_all_products_usecase_test.dart`:

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/features/products/domain/entities/product.dart';
import 'package:test/features/products/domain/repositories/product_repository.dart';
import 'package:test/features/products/domain/usecases/get_all_products_usecase.dart';

@GenerateMocks([IProductRepository])
import 'get_all_products_usecase_test.mocks.dart';

void main() {
  late MockIProductRepository mockRepository;
  late GetAllProductsUseCase useCase;

  setUp(() {
    mockRepository = MockIProductRepository();
    useCase = GetAllProductsUseCase(repository: mockRepository);
  });

  const tProduct1 = Product(id: '1', name: 'Laptop', price: 1000, stock: 5);
  const tProduct2 = Product(id: '2', name: 'Mouse', price: 50, stock: 100);
  const tProducts = [tProduct1, tProduct2];

  test('should get all products from repository', () async {
    // Arrange
    when(mockRepository.getAllProducts()).thenAnswer(
      (_) async => const Right(tProducts),
    );

    // Act
    final result = await useCase();

    // Assert
    expect(result, equals(const Right(tProducts)));
    verify(mockRepository.getAllProducts()).called(1);
  });

  test('should return empty list when no products exist', () async {
    // Arrange
    when(mockRepository.getAllProducts()).thenAnswer(
      (_) async => const Right([]),
    );

    // Act
    final result = await useCase();

    // Assert
    expect(result.isRight(), true);
    result.fold(
      (_) => fail('Should return list'),
      (products) => expect(products, isEmpty),
    );
  });
}
```

### 🔄 Genera y ejecuta

```bash
dart run build_runner build --delete-conflicting-outputs
flutter test test/features/products/domain/usecases/get_all_products_usecase_test.dart
```

---

## CAPA DATA: DataSources (Remote/Local)

### 📍 ¿Qué mockeamos aquí?

```
DATA
├── Models              → No necesitamos mocks (son datos puros)
├── DataSources         → ✅ MOCKEAMOS (simulamos API/local storage)
└── Repository Impl     → ✅ MOCKEAMOS los DataSources
```

### 🎯 Ejemplo: Testeando RemoteDataSource

Crea `test/features/products/data/datasources/product_remote_datasource.dart`:

```dart
import 'package:dartz/dartz.dart';
import '../../domain/entities/product.dart';
import '../../domain/repositories/product_repository.dart';

abstract class ProductRemoteDataSource {
  Future<Either<Failure, Product>> getProduct(String id);
  Future<Either<Failure, List<Product>>> getProducts();
}
```

Crea `test/features/products/data/datasources/product_remote_datasource_test.dart`:

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/features/products/data/datasources/product_remote_datasource.dart';
import 'package:test/features/products/domain/entities/product.dart';
import 'package:test/features/products/domain/repositories/product_repository.dart';

@GenerateMocks([ProductRemoteDataSource])
import 'product_remote_datasource_test.mocks.dart';

void main() {
  late MockProductRemoteDataSource mockDataSource;

  setUp(() {
    mockDataSource = MockProductRemoteDataSource();
  });

  const tProduct = Product(id: '1', name: 'Test', price: 100, stock: 10);

  group('ProductRemoteDataSource', () {
    test('should return product when remote call is successful', () async {
      // Arrange - Simulamos que la API responde bien
      when(mockDataSource.getProduct(any)).thenAnswer(
        (_) async => const Right(tProduct),
      );

      // Act
      final result = await mockDataSource.getProduct('1');

      // Assert
      expect(result, equals(const Right(tProduct)));
      verify(mockDataSource.getProduct('1')).called(1);
    });

    test('should return ServerFailure when remote call fails', () async {
      // Arrange - Simulamos error de red
      when(mockDataSource.getProduct(any)).thenAnswer(
        (_) async => const Left(ServerFailure('Network error')),
      );

      // Act
      final result = await mockDataSource.getProduct('1');

      // Assert
      expect(result.isLeft(), true);
    });

    test('should get multiple products', () async {
      // Arrange
      const products = [
        Product(id: '1', name: 'Product 1', price: 100, stock: 10),
        Product(id: '2', name: 'Product 2', price: 200, stock: 20),
      ];
      when(mockDataSource.getProducts()).thenAnswer(
        (_) async => const Right(products),
      );

      // Act
      final result = await mockDataSource.getProducts();

      // Assert
      result.fold(
        (_) => fail('Should return products'),
        (data) => expect(data.length, 2),
      );
    });
  });
}
```

### 🎯 Ejemplo: Testeando Repository Implementation con Mocks

Crea `test/features/products/data/repositories/product_repository_impl.dart`:

```dart
import 'package:dartz/dartz.dart';
import '../../domain/entities/product.dart';
import '../../domain/repositories/product_repository.dart';
import '../datasources/product_remote_datasource.dart';

class ProductRepositoryImpl implements IProductRepository {
  final ProductRemoteDataSource remoteDataSource;

  ProductRepositoryImpl({required this.remoteDataSource});

  @override
  Future<Either<Failure, Product>> getProduct(String id) async {
    return await remoteDataSource.getProduct(id);
  }

  @override
  Future<Either<Failure, List<Product>>> getAllProducts() async {
    return await remoteDataSource.getProducts();
  }

  @override
  Future<Either<Failure, Product>> createProduct(Product product) async {
    // Implementación...
    throw UnimplementedError();
  }

  @override
  Future<Either<Failure, Product>> updateProduct(Product product) async {
    // Implementación...
    throw UnimplementedError();
  }

  @override
  Future<Either<Failure, void>> deleteProduct(String id) async {
    // Implementación...
    throw UnimplementedError();
  }
}
```

Crea `test/features/products/data/repositories/product_repository_impl_test.dart`:

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/features/products/data/datasources/product_remote_datasource.dart';
import 'package:test/features/products/data/repositories/product_repository_impl.dart';
import 'package:test/features/products/domain/entities/product.dart';
import 'package:test/features/products/domain/repositories/product_repository.dart';

@GenerateMocks([ProductRemoteDataSource])
import 'product_repository_impl_test.mocks.dart';

void main() {
  late ProductRepositoryImpl repository;
  late MockProductRemoteDataSource mockRemoteDataSource;

  setUp(() {
    mockRemoteDataSource = MockProductRemoteDataSource();
    repository = ProductRepositoryImpl(remoteDataSource: mockRemoteDataSource);
  });

  const tProduct = Product(id: '1', name: 'Test', price: 100, stock: 10);

  group('ProductRepositoryImpl', () {
    test('should forward call to remote data source', () async {
      // Arrange
      when(mockRemoteDataSource.getProduct(any)).thenAnswer(
        (_) async => const Right(tProduct),
      );

      // Act
      final result = await repository.getProduct('1');

      // Assert
      expect(result, equals(const Right(tProduct)));
      verify(mockRemoteDataSource.getProduct('1')).called(1);
    });

    test('should return failure when remote fails', () async {
      // Arrange
      when(mockRemoteDataSource.getProduct(any)).thenAnswer(
        (_) async => const Left(ServerFailure('API Error')),
      );

      // Act
      final result = await repository.getProduct('1');

      // Assert
      expect(result.isLeft(), true);
    });
  });
}
```

---

## CAPA PRESENTATION: Cubits/BLoCs

### ⚠️ Importante: Las herramientas correctas

> **Esta capa usa una COMBINACIÓN de dos librerías:**

| Herramienta | Para qué sirve |
|-------------|----------------|
| **bloc_test** | ✅ Testear los **estados** del Cubit/BLoC |
| **Mockito** | ✅ Mockear los **UseCases** inyectados |

```
PRESENTATION
├── Widgets           → Test con pumpWidget (no mocks)
├── States/Events    → No necesitamos mocks
└── Cubit/BLoC       → bloc_test + Mockito (UseCases)
```

### 🎯 Ejemplo: Testeando ProductCubit

Primero crea el Cubit:

```dart
// test/features/products/presentation/cubit/product_state.dart
abstract class ProductState {}

class ProductInitial extends ProductState {}
class ProductLoading extends ProductState {}
class ProductLoaded extends ProductState {
  final Product product;
  ProductLoaded(this.product);
}
class ProductError extends ProductState {
  final String message;
  ProductError(this.message);
}
```

```dart
// test/features/products/presentation/cubit/product_cubit.dart
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/usecases/get_product_usecase.dart';
import 'product_state.dart';

class ProductCubit extends Cubit<ProductState> {
  final GetProductUseCase getProductUseCase;

  ProductCubit({required this.getProductUseCase}) : super(ProductInitial());

  Future<void> loadProduct(String productId) async {
    emit(ProductLoading());

    final result = await getProductUseCase(productId);

    result.fold(
      (failure) => emit(ProductError(failure.message)),
      (product) => emit(ProductLoaded(product)),
    );
  }
}
```

Ahora el test con la combinación de **bloc_test** + **Mockito**:

```dart
// test/features/products/presentation/cubit/product_cubit_test.dart
import 'package:bloc_test/bloc_test.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/features/products/domain/entities/product.dart';
import 'package:test/features/products/domain/repositories/product_repository.dart';
import 'package:test/features/products/domain/usecases/get_product_usecase.dart';
import 'package:test/features/products/presentation/cubit/product_cubit.dart';
import 'package:test/features/products/presentation/cubit/product_state.dart';

@GenerateMocks([GetProductUseCase])
import 'product_cubit_test.mocks.dart';

void main() {
  late ProductCubit cubit;
  late MockGetProductUseCase mockGetProductUseCase;

  setUp(() {
    mockGetProductUseCase = MockGetProductUseCase();
    cubit = ProductCubit(getProductUseCase: mockGetProductUseCase);
  });

  tearDown(() {
    cubit.close();
  });

  const tProduct = Product(
    id: '1',
    name: 'Test Product',
    price: 100,
    stock: 10,
  );

  group('ProductCubit', () {
    test('initial state should be ProductInitial', () {
      expect(cubit.state, equals(ProductInitial()));
    });

    blocTest<ProductCubit, ProductState>(
      'emits [ProductLoading, ProductLoaded] when loadProduct succeeds',
      build: () {
        when(mockGetProductUseCase(any)).thenAnswer(
          (_) async => const Right(tProduct),
        );
        return cubit;
      },
      act: (cubit) => cubit.loadProduct('1'),
      expect: () => [
        ProductLoading(),
        ProductLoaded(tProduct),
      ],
      verify: (_) {
        verify(mockGetProductUseCase('1')).called(1);
      },
    );

    blocTest<ProductCubit, ProductState>(
      'emits [ProductLoading, ProductError] when loadProduct fails',
      build: () {
        when(mockGetProductUseCase(any)).thenAnswer(
          (_) async => const Left(ServerFailure('Not found')),
        );
        return cubit;
      },
      act: (cubit) => cubit.loadProduct('999'),
      expect: () => [
        ProductLoading(),
        const ProductError('Not found'),
      ],
    );

    blocTest<ProductCubit, ProductState>(
      'calls useCase with correct productId',
      build: () {
        when(mockGetProductUseCase(any)).thenAnswer(
          (_) async => const Right(tProduct),
        );
        return cubit;
      },
      act: (cubit) => cubit.loadProduct('product-123'),
      verify: (_) {
        verify(mockGetProductUseCase('product-123')).called(1);
      },
    );
  });
}
```

### 🔄 Genera y ejecuta

```bash
dart run build_runner build --delete-conflicting-outputs
flutter test test/features/products/presentation/cubit/product_cubit_test.dart
```

---

> 📖 **NOTA:** Los ejercicios detallados de bloc_test para Cubits están cubiertos en **[04a-practica-cubits-bloc-test.md](./04a-practica-cubits-bloc-test.md)**. Esta sección solo muestra cómo Mockito se integra con bloc_test.

---

## CAPA CORE: Services Compartidos

### 📍 ¿Qué mockeamos aquí?

```
CORE (Shared Services)
├── NetworkInfo       → ✅ MOCKEAMOS para testear sin red
├── Storage           → ✅ MOCKEAMOS (SharedPreferences, etc.)
├── API Client        → ✅ MOCKEAMOS las llamadas HTTP
└── Utils             → No necesitamos mocks (son funciones puras)
```

### 🎯 Ejemplo: Testeando NetworkInfo

Crea `test/core/network_info.dart`:

```dart
abstract class NetworkInfo {
  Future<bool> get isConnected;
}
```

Crea `test/core/network_info_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/core/network_info.dart';

@GenerateMocks([NetworkInfo])
import 'network_info_test.mocks.dart';

void main() {
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockNetworkInfo = MockNetworkInfo();
  });

  group('NetworkInfo', () {
    test('should return true when device is connected', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer(
        (_) async => true,
      );

      // Act
      final result = await mockNetworkInfo.isConnected;

      // Assert
      expect(result, true);
      verify(mockNetworkInfo.isConnected).called(1);
    });

    test('should return false when device is not connected', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer(
        (_) async => false,
      );

      // Act
      final result = await mockNetworkInfo.isConnected;

      // Assert
      expect(result, false);
    });
  });
}
```

### 🎯 Ejemplo: Repository que depende de NetworkInfo

Imagina que tienes un repository que decide si usar cache o red:

```dart
// test/features/products/domain/usecases/get_product_with_cache_usecase.dart
import 'package:dartz/dartz.dart';
import '../entities/product.dart';
import '../repositories/product_repository.dart';
import '../../../core/network_info.dart';

class GetProductWithCacheUseCase {
  final IProductRepository repository;
  final NetworkInfo networkInfo;

  GetProductWithCacheUseCase({
    required this.repository,
    required this.networkInfo,
  });

  Future<Either<Failure, Product>> call(String id) async {
    final isConnected = await networkInfo.isConnected;
    
    if (isConnected) {
      return await repository.getProduct(id);
    } else {
      // Podría retornar de cache local
      return const Left(ServerFailure('No internet connection'));
    }
  }
}
```

Test con múltiples mocks:

```dart
// test/features/products/domain/usecases/get_product_with_cache_usecase_test.dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/core/network_info.dart';
import 'package:test/features/products/domain/entities/product.dart';
import 'package:test/features/products/domain/repositories/product_repository.dart';
import 'package:test/features/products/domain/usecases/get_product_with_cache_usecase.dart';

@GenerateMocks([IProductRepository, NetworkInfo])
import 'get_product_with_cache_usecase_test.mocks.dart';

void main() {
  late GetProductWithCacheUseCase useCase;
  late MockIProductRepository mockRepository;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockRepository = MockIProductRepository();
    mockNetworkInfo = MockNetworkInfo();
    useCase = GetProductWithCacheUseCase(
      repository: mockRepository,
      networkInfo: mockNetworkInfo,
    );
  });

  const tProduct = Product(id: '1', name: 'Test', price: 100, stock: 10);

  group('GetProductWithCacheUseCase', () {
    test('should get product from repository when connected', () async {
      // Arrange - Ambos mocks
      when(mockNetworkInfo.isConnected).thenAnswer(
        (_) async => true,
      );
      when(mockRepository.getProduct(any)).thenAnswer(
        (_) async => const Right(tProduct),
      );

      // Act
      final result = await useCase('1');

      // Assert
      expect(result, equals(const Right(tProduct)));
      verify(mockNetworkInfo.isConnected).called(1);
      verify(mockRepository.getProduct('1')).called(1);
    });

    test('should return failure when not connected', () async {
      // Arrange
      when(mockNetworkInfo.isConnected).thenAnswer(
        (_) async => false,
      );

      // Act
      final result = await useCase('1');

      // Assert
      expect(result.isLeft(), true);
      verify(mockNetworkInfo.isConnected).called(1);
      verifyNever(mockRepository.getProduct(any));
    });
  });
}
```

### 🔄 Genera y ejecuta

```bash
dart run build_runner build --delete-conflicting-outputs
flutter test test/features/products/domain/usecases/get_product_with_cache_usecase_test.dart
```

---

# 📊 Resumen: Mockito por Capa

| Capa | Qué Mockear | Ejemplo |
|------|-------------|---------|
| **Domain** | Repository Interfaces, UseCases | `MockIProductRepository`, `MockGetProductUseCase` |
| **Data** | DataSources (Remote/Local) | `MockProductRemoteDataSource` |
| **Presentation** | UseCases dentro de Cubits/BLoCs | `MockGetProductUseCase` |
| **Core** | NetworkInfo, Storage, API Client | `MockNetworkInfo` |

---

## ✅ Checklist de Ejercicio Completado

### Fundamentos
- [ ] Ejercicio 1: Estructura de carpetas
- [ ] Ejercicio 2: Interfaz y entidades
- [ ] Ejercicio 3: Generar primer Mock
- [ ] Ejercicio 4: thenAnswer básico
- [ ] Ejercicio 5: thenThrow para errores
- [ ] Ejercicio 6: verify básico

### Por Capa
- [ ] CAPA DOMAIN: Repository + UseCase
- [ ] CAPA DATA: DataSources (Remote/Local)
- [ ] CAPA PRESENTATION: Cubits/BLoCs
- [ ] CAPA CORE: Services Compartidos

---

## 🎉 ¡Felicitaciones!

Has completado la práctica completa de Mockito. Ahora dominas:

- ✅ Configurar Mockito con @GenerateMocks
- ✅ Stubbing con when() y thenAnswer()
- ✅ Manejar errores con thenThrow()
- ✅ Verificación con verify()
- ✅ **Mockito en DOMAIN** (Repository + UseCase)
- ✅ **Mockito en DATA** (DataSources)
- ✅ **Mockito en PRESENTATION** (Cubits)
- ✅ **Mockito en CORE** (Services)

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 3: Testing Data](./03-data-testing.md)

**Práctica:**
- [03a-practica-fixtures-models.md](./03a-practica-fixtures-models.md)
- [03b-practica-datasources.md](./03b-practica-datasources.md)

---

## 📝 Notas del Autor

Esta guía práctica ahora cubre **todas las capas de Clean Architecture** con ejemplos reales:

- **Domain**: Repository Interfaces, UseCases
- **Data**: Remote/Local DataSources, Repository Implementation
- **Presentation**: Cubits/BLoCs con bloc_test
- **Core**: NetworkInfo, servicios compartidos

**Recordatorio:** La clave es mockear las **dependencias externas** a la capa que estás probando, nunca la lógica interna.

---

**Última actualización:** 2026-03-25
**Versión:** 3.0.0
