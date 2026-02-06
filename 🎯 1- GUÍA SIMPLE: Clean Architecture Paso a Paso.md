# 🎯 GUÍA SIMPLE: Clean Architecture Paso a Paso

> **Para novatos**: Lee esto de principio a fin en orden numérico.
> No saltes pasos. No hay opciones alternativas.

---

## 📋 ÍNDICE (Lee en este orden exacto)

1. [La Analogía Simple](#1-la-analogía-simple)
2. [Las 4 Capas](#2-las-4-capas)
3. [Ejemplo Práctico: Lista de Compras](#3-ejemplo-práctico-lista-de-compras)
4. [Paso 1: Domain (La Receta)](#4-paso-1-domain-la-receta)
5. [Paso 2: Data (La Cocina)](#5-paso-2-data-la-cocina)
6. [Paso 3: Repository (El Almacén)](#6-paso-3-repository-el-almacén)
7. [Paso 4: UseCase (El Chef)](#7-paso-4-usecase-el-chef)
8. [Paso 5: Cubit (El Mesero)](#8-paso-5-cubit-el-mesero)
9. [Paso 6: UI (El Cliente)](#9-paso-6-ui-el-cliente)
10. [Paso 7: Conectar Todo](#10-paso-7-conectar-todo)
11. [Testing Básico](#11-testing-básico)

---

## 1. La Analogía Simple

Imagina un **restaurante** donde vas a pedir una hamburguesa:

| Tu Código | Restaurante | Qué Hace |
|-----------|-------------|----------|
| **Domain** | La Receta | Dice qué ingredientes necesitas |
| **Data** | La Cocina | Cocina los ingredientes |
| **Repository** | El Almacén | Decide si usa carne fresca o congelada |
| **UseCase** | El Chef Cocinando | Sigue la receta paso a paso |
| **Cubit** | El Mesero | Lleva tu pedido y trae la comida |
| **UI** | Tu Mesa | Donde comes y pides |

**Regla importante**: Tú (UI) **NUNCA** entras a la cocina (Data). Todo pasa por el mesero (Cubit).

---

## 2. Las 4 Capas

```
CAPA 4 - UI (Widgets)
    ↓ Llama al Cubit
    
CAPA 3 - Presentation (Cubit)
    ↓ Llama al UseCase
    
CAPA 2 - Domain (UseCase + Entity)
    ↓ Llama al Repository
    
CAPA 1 - Data (Repository + DataSource)
    ↓ Habla con API o Base de Datos
```

**Flujo completo cuando presionas un botón:**
1. Botón llama a `cubit.loadData()`
2. Cubit llama a `useCase.execute()`
3. UseCase llama a `repository.getData()`
4. Repository decide: ¿API? ¿Base de datos local?
5. DataSource trae los datos
6. Vuelve por el mismo camino hasta la UI

---

## 3. Ejemplo Práctico: Lista de Compras

Vamos a crear una app simple de **lista de compras** donde puedes:
- Ver productos (desde API si hay internet, desde caché si no)
- Agregar productos
- Eliminar productos

**Tecnología**: API REST (JSON) + SQLite local

---

## 4. Paso 1: Domain (La Receta)

**Qué hace**: Define qué es un "Producto" sin importar cómo se guarda.

### 4.1 Crear la Entity

**Archivo**: `lib/features/product/domain/entities/product.dart`

```dart
import 'package:equatable/equatable.dart';

// ESTO ES UN PRODUCTO. Punto.
// No sabe de internet, no sabe de base de datos.
class Product extends Equatable {
  const Product({
    required this.id,
    required this.name,
    required this.price,
    this.isBought = false,
  });

  final String id;
  final String name;
  final double price;
  final bool isBought;

  // Calcula precio total (lógica de negocio)
  String get formattedPrice => '\$${price.toStringAsFixed(2)}';

  // Crea copia modificada
  Product copyWith({
    String? id,
    String? name,
    double? price,
    bool? isBought,
  }) {
    return Product(
      id: id ?? this.id,
      name: name ?? this.name,
      price: price ?? this.price,
      isBought: isBought ?? this.isBought,
    );
  }

  // Para comparar productos
  @override
  List<Object?> get props => [id, name, price, isBought];
}
```

**Explicación línea por línea:**
- `extends Equatable`: Permite comparar productos con `==`
- `const`: El producto no cambia, creamos copias
- `get formattedPrice`: Lógica de negocio (cómo mostrar precio)
- `copyWith`: Crea versión modificada sin cambiar el original
- `props`: Lista de campos para comparar

### 4.2 Crear el Repository Interface

**Archivo**: `lib/features/product/domain/repositories/product_repository.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/product/domain/entities/product.dart';

// CONTRATO: Qué se puede hacer con productos
// No dice CÓMO, solo dice QUÉ se puede hacer
abstract class ProductRepository {
  Future<Either<Failure, List<Product>>> getProducts();
  Future<Either<Failure, Product>> createProduct(String name, double price);
  Future<Either<Failure, void>> deleteProduct(String id);
}
```

**Explicación:**
- `Either<Failure, Product>`: Retorna ERROR (izquierda) o ÉXITO (derecha)
- `abstract`: Es un contrato, no implementación

---

## 5. Paso 2: Data (La Cocina)

**Qué hace**: Implementa CÓMO se guardan y recuperan los datos.

### 5.1 Crear el Model

**Archivo**: `lib/features/product/data/models/product_model.dart`

```dart
import 'package:my_app/features/product/domain/entities/product.dart';

// Modelo para JSON (API) y SQLite (local)
class ProductModel extends Product {
  ProductModel({
    required this.id,
    required this.name,
    required this.price,
    this.isBought = false,
  });

  final String id;
  final String name;
  final double price;
  final bool isBought;

  // De JSON (API) a Model
  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'],
      name: json['name'],
      price: json['price'].toDouble(),
      isBought: json['isBought'] ?? false,
    );
  }

  // De Model a JSON (para enviar a API)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'price': price,
      'isBought': isBought,
    };
  }

  // De Model a Entity (Domain)
  Product toEntity() {
    return Product(
      id: id,
      name: name,
      price: price,
      isBought: isBought,
    );
  }

  // De Entity a Model
  factory ProductModel.fromEntity(Product entity) {
    return ProductModel(
      id: entity.id,
      name: entity.name,
      price: entity.price,
      isBought: entity.isBought,
    );
  }
}
```

### 5.2 Crear Remote DataSource (API)

**Archivo**: `lib/features/product/data/datasources/product_remote_data_source.dart`

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:my_app/features/product/data/models/product_model.dart';

abstract class ProductRemoteDataSource {
  Future<List<ProductModel>> getProducts();
  Future<ProductModel> createProduct(String name, double price);
  Future<void> deleteProduct(String id);
}

class ProductRemoteDataSourceImpl implements ProductRemoteDataSource {
  final http.Client client;
  final String baseUrl;

  ProductRemoteDataSourceImpl({
    required this.client,
    this.baseUrl = 'https://api.tuapp.com',
  });

  @override
  Future<List<ProductModel>> getProducts() async {
    final response = await client.get(
      Uri.parse('$baseUrl/products'),
    );

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = json.decode(response.body);
      return jsonList.map((json) => ProductModel.fromJson(json)).toList();
    } else {
      throw Exception('Error del servidor');
    }
  }

  @override
  Future<ProductModel> createProduct(String name, double price) async {
    final response = await client.post(
      Uri.parse('$baseUrl/products'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'name': name, 'price': price}),
    );

    if (response.statusCode == 201) {
      return ProductModel.fromJson(json.decode(response.body));
    } else {
      throw Exception('Error creando producto');
    }
  }

  @override
  Future<void> deleteProduct(String id) async {
    final response = await client.delete(
      Uri.parse('$baseUrl/products/$id'),
    );

    if (response.statusCode != 200) {
      throw Exception('Error eliminando producto');
    }
  }
}
```

### 5.3 Crear Local DataSource (Caché)

**Archivo**: `lib/features/product/data/datasources/product_local_data_source.dart`

```dart
import 'package:sqflite/sqflite.dart';
import 'package:my_app/features/product/data/models/product_model.dart';

abstract class ProductLocalDataSource {
  Future<List<ProductModel>> getProducts();
  Future<void> cacheProduct(ProductModel product);
  Future<void> cacheProducts(List<ProductModel> products);
  Future<void> deleteProduct(String id);
}

class ProductLocalDataSourceImpl implements ProductLocalDataSource {
  final Database database;

  ProductLocalDataSourceImpl({required this.database});

  @override
  Future<List<ProductModel>> getProducts() async {
    final List<Map<String, dynamic>> maps = await database.query('products');
    
    return List.generate(maps.length, (i) {
      return ProductModel(
        id: maps[i]['id'],
        name: maps[i]['name'],
        price: maps[i]['price'],
        isBought: maps[i]['isBought'] == 1,
      );
    });
  }

  @override
  Future<void> cacheProduct(ProductModel product) async {
    await database.insert(
      'products',
      {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'isBought': product.isBought ? 1 : 0,
      },
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  @override
  Future<void> cacheProducts(List<ProductModel> products) async {
    final batch = database.batch();
    for (final product in products) {
      batch.insert(
        'products',
        {
          'id': product.id,
          'name': product.name,
          'price': product.price,
          'isBought': product.isBought ? 1 : 0,
        },
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }
    await batch.commit();
  }

  @override
  Future<void> deleteProduct(String id) async {
    await database.delete(
      'products',
      where: 'id = ?',
      whereArgs: [id],
    );
  }
}
```

---

## 6. Paso 3: Repository (El Almacén)

**Qué hace**: Decide si usa internet (API) o caché local.

**Archivo**: `lib/features/product/data/repositories/product_repository_impl.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/core/network/network_info.dart';
import 'package:my_app/features/product/data/datasources/product_local_data_source.dart';
import 'package:my_app/features/product/data/datasources/product_remote_data_source.dart';
import 'package:my_app/features/product/data/models/product_model.dart';
import 'package:my_app/features/product/domain/entities/product.dart';
import 'package:my_app/features/product/domain/repositories/product_repository.dart';

class ProductRepositoryImpl implements ProductRepository {
  final ProductRemoteDataSource remoteDataSource;
  final ProductLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  ProductRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, List<Product>>> getProducts() async {
    // PASO 1: ¿Hay internet?
    if (await networkInfo.isConnected) {
      try {
        // SÍ hay internet → Usar API
        final remoteProducts = await remoteDataSource.getProducts();
        
        // Guardar en caché local
        await localDataSource.cacheProducts(remoteProducts);
        
        // Convertir a Entity y retornar
        return Right(remoteProducts.map((m) => m.toEntity()).toList());
      } catch (e) {
        // Error en API → Intentar caché local
        return await _getFromCache();
      }
    } else {
      // NO hay internet → Usar caché local
      return await _getFromCache();
    }
  }

  // Método privado: Obtener de caché
  Future<Either<Failure, List<Product>>> _getFromCache() async {
    try {
      final localProducts = await localDataSource.getProducts();
      return Right(localProducts.map((m) => m.toEntity()).toList());
    } catch (e) {
      return Left(CacheFailure('No hay productos guardados'));
    }
  }

  @override
  Future<Either<Failure, Product>> createProduct(
    String name,
    double price,
  ) async {
    if (await networkInfo.isConnected) {
      try {
        final product = await remoteDataSource.createProduct(name, price);
        await localDataSource.cacheProduct(product);
        return Right(product.toEntity());
      } catch (e) {
        return Left(ServerFailure('Error creando producto'));
      }
    } else {
      return Left(NetworkFailure('Sin conexión'));
    }
  }

  @override
  Future<Either<Failure, void>> deleteProduct(String id) async {
    if (await networkInfo.isConnected) {
      try {
        await remoteDataSource.deleteProduct(id);
        await localDataSource.deleteProduct(id);
        return const Right(null);
      } catch (e) {
        return Left(ServerFailure('Error eliminando'));
      }
    } else {
      return Left(NetworkFailure('Sin conexión'));
    }
  }
}
```

**Lógica clave:**
```
if (hayInternet) {
  return datosDeAPI();
} else {
  return datosDeCache();
}
```

---

### 📍 IMPORTANTE: ¿Dónde van los errores?

**Esta es una de las reglas más importantes de Clean Architecture:**

| Tipo de Error | ¿En qué capa? | ¿Qué es? | Ejemplo |
|---------------|---------------|----------|---------|
| **Exception** | **Data Layer** | Error técnico (HTTP, BD, parsing) | `ServerException`, `CacheException` |
| **Failure** | **Domain Layer** | Error de negocio (entendible por usuario) | `ServerFailure`, `NetworkFailure` |

**Flujo de errores:**
```
DataSource lanza Exception (error técnico)
        ↓
Repository atrapa Exception con try/catch
        ↓
Repository convierte Exception → Failure
        ↓
Repository retorna Either<Failure, T>
        ↓
UseCase recibe Failure
        ↓
Cubit emite estado de error
        ↓
UI muestra mensaje amigable al usuario
```

**En código:**
```dart
// En DataSource (lib/features/x/data/datasources/)
throw ServerException('Error 500');  // ← Exception

// En Repository (lib/features/x/data/repositories/)
try {
  await remoteDataSource.getData();
} catch (e) {
  return Left(ServerFailure('Error del servidor'));  // ← Failure
}

// En UseCase y Cubit trabajamos con Failure
result.fold(
  (failure) => emit(ErrorState(failure.message)),  // ← Failure
  (data) => emit(LoadedState(data)),
);
```

**Resumen mnemotécnico:**
- ✅ **Exception** = Error técnico → **Data Layer** (try/catch)
- ✅ **Failure** = Error de negocio → **Domain Layer** (Either<Failure, T>)

---

## 7. Paso 4: UseCase (El Chef)

**Qué hace**: Ejecuta una acción específica.

**Archivo**: `lib/features/product/domain/usecases/get_products.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/product/domain/entities/product.dart';
import 'package:my_app/features/product/domain/repositories/product_repository.dart';

// UN SOLO TRABAJO: Traer productos
class GetProducts extends UseCase<List<Product>, NoParams> {
  final ProductRepository repository;

  GetProducts(this.repository);

  @override
  Future<Either<Failure, List<Product>>> call(NoParams params) async {
    return await repository.getProducts();
  }
}
```

**Archivo**: `lib/features/product/domain/usecases/create_product.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/product/domain/entities/product.dart';
import 'package:my_app/features/product/domain/repositories/product_repository.dart';

class CreateProduct extends UseCase<Product, CreateProductParams> {
  final ProductRepository repository;

  CreateProduct(this.repository);

  @override
  Future<Either<Failure, Product>> call(CreateProductParams params) async {
    return await repository.createProduct(params.name, params.price);
  }
}

class CreateProductParams extends Equatable {
  final String name;
  final double price;

  const CreateProductParams({required this.name, required this.price});

  @override
  List<Object?> get props => [name, price];
}
```

---

## 8. Paso 5: Cubit (El Mesero)

**Qué hace**: Maneja el estado de la pantalla.

**Archivo**: `lib/features/product/presentation/cubit/product_cubit.dart`

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/features/product/domain/entities/product.dart';
import 'package:my_app/features/product/domain/usecases/create_product.dart';
import 'package:my_app/features/product/domain/usecases/get_products.dart';

part 'product_state.dart';

class ProductCubit extends Cubit<ProductState> {
  final GetProducts _getProducts;
  final CreateProduct _createProduct;

  ProductCubit({
    required GetProducts getProducts,
    required CreateProduct createProduct,
  })  : _getProducts = getProducts,
        _createProduct = createProduct,
        super(ProductInitial());

  // Cargar productos
  Future<void> loadProducts() async {
    emit(ProductLoading()); // Mostrar "Cargando..."

    final result = await _getProducts(NoParams());

    result.fold(
      (failure) => emit(ProductError('Error cargando productos')),
      (products) => emit(ProductLoaded(products)),
    );
  }

  // Agregar producto
  Future<void> addProduct(String name, double price) async {
    emit(ProductLoading());

    final result = await _createProduct(
      CreateProductParams(name: name, price: price),
    );

    result.fold(
      (failure) => emit(ProductError('Error creando producto')),
      (product) {
        emit(ProductOperationSuccess('Producto creado'));
        loadProducts(); // Recargar lista
      },
    );
  }
}
```

**Archivo**: `lib/features/product/presentation/cubit/product_state.dart`

```dart
part of 'product_cubit.dart';

abstract class ProductState extends Equatable {
  const ProductState();

  @override
  List<Object?> get props => [];
}

class ProductInitial extends ProductState {}

class ProductLoading extends ProductState {}

class ProductLoaded extends ProductState {
  final List<Product> products;

  const ProductLoaded(this.products);

  @override
  List<Object?> get props => [products];
}

class ProductError extends ProductState {
  final String message;

  const ProductError(this.message);

  @override
  List<Object?> get props => [message];
}

class ProductOperationSuccess extends ProductState {
  final String message;

  const ProductOperationSuccess(this.message);

  @override
  List<Object?> get props => [message];
}
```

---

## 9. Paso 6: UI (El Cliente)

**Qué hace**: Muestra la interfaz y recibe clicks.

**Archivo**: `lib/features/product/presentation/pages/products_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:my_app/features/product/presentation/cubit/product_cubit.dart';

class ProductsPage extends StatelessWidget {
  const ProductsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => GetIt.I<ProductCubit>()..loadProducts(),
      child: Scaffold(
        appBar: AppBar(title: const Text('Lista de Compras')),
        body: const _ProductsView(),
        floatingActionButton: FloatingActionButton(
          onPressed: () => _showAddDialog(context),
          child: const Icon(Icons.add),
        ),
      ),
    );
  }

  void _showAddDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => const _AddProductDialog(),
    );
  }
}

class _ProductsView extends StatelessWidget {
  const _ProductsView();

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<ProductCubit, ProductState>(
      listener: (context, state) {
        if (state is ProductOperationSuccess) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message)),
          );
        }
      },
      builder: (context, state) {
        if (state is ProductLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        if (state is ProductError) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(state.message),
                ElevatedButton(
                  onPressed: () {
                    context.read<ProductCubit>().loadProducts();
                  },
                  child: const Text('Reintentar'),
                ),
              ],
            ),
          );
        }

        if (state is ProductLoaded) {
          return ListView.builder(
            itemCount: state.products.length,
            itemBuilder: (context, index) {
              final product = state.products[index];
              return ListTile(
                title: Text(product.name),
                subtitle: Text(product.formattedPrice),
                trailing: Checkbox(
                  value: product.isBought,
                  onChanged: (value) {
                    // Toggle comprado
                  },
                ),
              );
            },
          );
        }

        return const SizedBox.shrink();
      },
    );
  }
}

class _AddProductDialog extends StatefulWidget {
  const _AddProductDialog();

  @override
  State<_AddProductDialog> createState() => _AddProductDialogState();
}

class _AddProductDialogState extends State<_AddProductDialog> {
  final _nameController = TextEditingController();
  final _priceController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Nuevo Producto'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(
            controller: _nameController,
            decoration: const InputDecoration(labelText: 'Nombre'),
          ),
          TextField(
            controller: _priceController,
            decoration: const InputDecoration(labelText: 'Precio'),
            keyboardType: TextInputType.number,
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancelar'),
        ),
        TextButton(
          onPressed: () {
            final name = _nameController.text;
            final price = double.tryParse(_priceController.text) ?? 0;
            if (name.isNotEmpty && price > 0) {
              context.read<ProductCubit>().addProduct(name, price);
              Navigator.pop(context);
            }
          },
          child: const Text('Guardar'),
        ),
      ],
    );
  }
}
```

---

## 10. Paso 7: Conectar Todo

**Archivo**: `lib/core/di/injection_container.dart`

```dart
import 'package:get_it/get_it.dart';
import 'package:http/http.dart' as http;
import 'package:internet_connection_checker/internet_connection_checker.dart';
import 'package:sqflite/sqflite.dart';
import 'package:my_app/core/network/network_info.dart';
import 'package:my_app/features/product/data/datasources/product_local_data_source.dart';
import 'package:my_app/features/product/data/datasources/product_remote_data_source.dart';
import 'package:my_app/features/product/data/repositories/product_repository_impl.dart';
import 'package:my_app/features/product/domain/repositories/product_repository.dart';
import 'package:my_app/features/product/domain/usecases/create_product.dart';
import 'package:my_app/features/product/domain/usecases/get_products.dart';
import 'package:my_app/features/product/presentation/cubit/product_cubit.dart';

final GetIt sl = GetIt.instance;

Future<void> init() async {
  // External (librerías de terceros)
  sl
    ..registerLazySingleton(() => http.Client())
    ..registerLazySingleton(() => InternetConnectionChecker())
    ..registerLazySingleton<NetworkInfo>(
      () => NetworkInfoImpl(sl()),
    );

  // Base de datos SQLite (deberías inicializarla en main.dart)
  final database = await openDatabase(
    'app.db',
    version: 1,
    onCreate: (db, version) {
      return db.execute('''
        CREATE TABLE products(
          id TEXT PRIMARY KEY,
          name TEXT,
          price REAL,
          isBought INTEGER
        )
      ''');
    },
  );
  sl.registerLazySingleton<Database>(() => database);

  // Data Sources
  sl
    ..registerLazySingleton<ProductRemoteDataSource>(
      () => ProductRemoteDataSourceImpl(client: sl()),
    )
    ..registerLazySingleton<ProductLocalDataSource>(
      () => ProductLocalDataSourceImpl(database: sl()),
    );

  // Repository
  sl.registerLazySingleton<ProductRepository>(
    () => ProductRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Use Cases
  sl
    ..registerLazySingleton(() => GetProducts(sl()))
    ..registerLazySingleton(() => CreateProduct(sl()));

  // Cubit
  sl.registerFactory(() => ProductCubit(
    getProducts: sl(),
    createProduct: sl(),
  ));
}
```

**Archivo**: `lib/main.dart`

```dart
import 'package:flutter/material.dart';
import 'package:my_app/core/di/injection_container.dart' as di;
import 'package:my_app/features/product/presentation/pages/products_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await di.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lista de Compras',
      home: const ProductsPage(),
    );
  }
}
```

---

## 11. Testing Básico

### Test de Entity

**Archivo**: `test/features/product/domain/entities/product_test.dart`

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/features/product/domain/entities/product.dart';

void main() {
  const tProduct = Product(
    id: '1',
    name: 'Leche',
    price: 2.5,
  );

  test('should format price correctly', () {
    expect(tProduct.formattedPrice, '\$2.50');
  });

  test('copyWith should update only specified fields', () {
    final updated = tProduct.copyWith(price: 3.0);
    
    expect(updated.name, 'Leche'); // No cambió
    expect(updated.price, 3.0); // Cambió
  });
}
```

### Test de UseCase

**Archivo**: `test/features/product/domain/usecases/get_products_test.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/features/product/domain/entities/product.dart';
import 'package:my_app/features/product/domain/repositories/product_repository.dart';
import 'package:my_app/features/product/domain/usecases/get_products.dart';

class MockProductRepository extends Mock implements ProductRepository {}

void main() {
  late GetProducts useCase;
  late MockProductRepository mockRepository;

  setUp(() {
    mockRepository = MockProductRepository();
    useCase = GetProducts(mockRepository);
  });

  final tProducts = [
    const Product(id: '1', name: 'Leche', price: 2.5),
  ];

  test('should get products from repository', () async {
    // Arrange
    when(() => mockRepository.getProducts())
        .thenAnswer((_) async => Right(tProducts));

    // Act
    final result = await useCase(NoParams());

    // Assert
    expect(result, Right(tProducts));
    verify(() => mockRepository.getProducts()).called(1);
  });
}
```

### Test de Cubit

**Archivo**: `test/features/product/presentation/cubit/product_cubit_test.dart`

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/product/domain/entities/product.dart';
import 'package:my_app/features/product/domain/usecases/create_product.dart';
import 'package:my_app/features/product/domain/usecases/get_products.dart';
import 'package:my_app/features/product/presentation/cubit/product_cubit.dart';

class MockGetProducts extends Mock implements GetProducts {}
class MockCreateProduct extends Mock implements CreateProduct {}

void main() {
  late ProductCubit cubit;
  late MockGetProducts mockGetProducts;
  late MockCreateProduct mockCreateProduct;

  setUp(() {
    mockGetProducts = MockGetProducts();
    mockCreateProduct = MockCreateProduct();
    cubit = ProductCubit(
      getProducts: mockGetProducts,
      createProduct: mockCreateProduct,
    );
  });

  final tProducts = [
    const Product(id: '1', name: 'Leche', price: 2.5),
  ];

  blocTest<ProductCubit, ProductState>(
    'emits [Loading, Loaded] when getProducts succeeds',
    build: () {
      when(() => mockGetProducts(NoParams()))
          .thenAnswer((_) async => Right(tProducts));
      return cubit;
    },
    act: (cubit) => cubit.loadProducts(),
    expect: () => [
      ProductLoading(),
      ProductLoaded(tProducts),
    ],
  );

  blocTest<ProductCubit, ProductState>(
    'emits [Loading, Error] when getProducts fails',
    build: () {
      when(() => mockGetProducts(NoParams()))
          .thenAnswer((_) async => Left(ServerFailure('Error')));
      return cubit;
    },
    act: (cubit) => cubit.loadProducts(),
    expect: () => [
      ProductLoading(),
      isA<ProductError>(),
    ],
  );
}
```

---

## ✅ Checklist Final

Antes de decir "terminé", verifica:

```
□ Domain
  □ Entity creada
  □ Repository interface creada

□ Data
  □ Model con fromJson/toJson
  □ RemoteDataSource (API)
  □ LocalDataSource (SQLite)

□ Repository
  □ Implementación con lógica online/offline

□ UseCases
  □ GetProducts
  □ CreateProduct

□ Presentation
  □ States definidos
  □ Cubit implementado
  □ UI con BlocConsumer

□ Inyección
  □ Todo registrado en injection_container.dart
  □ init() llamado en main.dart

□ Testing
  □ Tests de Entity pasan
  □ Tests de UseCase pasan
  □ Tests de Cubit pasan
```

---

## 🎯 Resumen del Flujo

```
Usuario toca botón "Agregar"
    ↓
UI llama a cubit.addProduct()
    ↓
Cubit llama a useCase.execute()
    ↓
UseCase llama a repository.createProduct()
    ↓
Repository revisa: ¿Hay internet?
    ↓
SÍ: Llama a remoteDataSource.createProduct()
    Y: Guarda en localDataSource.cacheProduct()
NO: Retorna error (no podemos crear sin internet)
    ↓
Datos vuelven convertidos a Entity
    ↓
Cubit emite nuevo estado (ProductLoaded)
    ↓
UI se reconstruye y muestra el producto nuevo
```

---

**¿Está más claro ahora? ¿En qué paso te gustaría que profundice más?**
