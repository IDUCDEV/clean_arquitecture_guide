# Ejemplo práctico — Feature "Orders" de principio a fin

Guía paso a paso usando las 5 skills para construir un feature completo de gestión de pedidos.

---

## Escenario

Queremos un feature **Order** con:

- Listar pedidos, ver detalle, crear, actualizar, cancelar
- Persistencia en Supabase (tabla `orders`)
- Ruta `/orders` (lista) y `/orders/:id` (detalle)

---

## Paso 1: Scaffold completo del feature + Supabase + páginas

**Prompt para el asistente:**

> Crea un feature `order` con campos:
> - `id: String`
> - `userId: String`
> - `total: double`
> - `status: String`
> - `items: List<OrderItem>` (asumimos OrderItem como entidad separada)
> - `createdAt: DateTime`
>
> Operaciones CRUD: `getAll`, `getById`, `create`, `update`, `delete`
>
> Además, conéctalo a Supabase. Tabla `orders`:
> - `id: uuid PK`
> - `user_id: uuid NOT NULL`
> - `total: float8 NOT NULL`
> - `status: text NOT NULL DEFAULT 'pending'`
> - `items: jsonb NOT NULL DEFAULT '[]'`
> - `created_at: timestamptz NOT NULL DEFAULT now()`
>
> Páginas iniciales: `[list:listener_builder, detail:builder]`
>
> Y wiring: regístralo en DI y añade sus rutas al router (`/orders` → lista, `/orders/:id` → detalle)

**Qué genera `clean-arch-feature` (orquestando):**

```
lib/features/order/
├── data/
│   ├── datasources/
│   │   └── order_remote_datasource.dart   # con _tableName + watchById
│   ├── models/
│   │   └── order_model.dart               # con mapeo snake_case
│   └── repositories/
│       └── order_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── order.dart
│   ├── repositories/
│   │   └── order_repository.dart
│   └── usecases/
│       ├── get_orders.dart
│       ├── get_order.dart
│       ├── create_order.dart
│       ├── update_order.dart
│       └── delete_order.dart
└── presentation/
    ├── cubit/
    │   ├── order_cubit.dart
    │   └── order_state.dart
    └── pages/
        ├── orders_list_page.dart            # pattern listener_builder
        └── order_detail_page.dart           # pattern builder
supabase/
└── migrations/
    └── {timestamp}_create_orders.sql
```

**Ejemplo de archivo generado** — `domain/entities/order.dart`:

```dart
import 'package:equatable/equatable.dart';

class Order extends Equatable {
  const Order({
    required this.id,
    required this.userId,
    required this.total,
    required this.status,
    required this.items,
    required this.createdAt,
  });

  final String id;
  final String userId;
  final double total;
  final String status;
  final List<OrderItem> items;
  final DateTime createdAt;

  @override
  List<Object?> get props => [id, userId, total, status, items, createdAt];

  Order copyWith({
    String? id,
    String? userId,
    double? total,
    String? status,
    List<OrderItem>? items,
    DateTime? createdAt,
  }) {
    return Order(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      total: total ?? this.total,
      status: status ?? this.status,
      items: items ?? this.items,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  String toString() => 'Order(id: $id, status: $status, total: $total)';
}
```

**Ejemplo de archivo generado** — `data/models/order_model.dart` (con mapeo snake_case):

```dart
import 'dart:convert';
import 'package:order_app/features/order/domain/entities/order.dart';

class OrderModel extends Order {
  const OrderModel({
    required super.id,
    required super.userId,
    required super.total,
    required super.status,
    required super.items,
    required super.createdAt,
  });

  factory OrderModel.fromJson(Map<String, dynamic> json) {
    return OrderModel(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      total: (json['total'] as num).toDouble(),
      status: json['status'] as String,
      items: (json['items'] as List)
          .map((e) => OrderItem.fromJson(e as Map<String, dynamic>))
          .toList(),
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'user_id': userId,
    'total': total,
    'status': status,
    'items': items.map((e) => e.toJson()).toList(),
    'created_at': createdAt.toIso8601String(),
  };

  factory OrderModel.fromEntity(Order entity) => OrderModel(
    id: entity.id,
    userId: entity.userId,
    total: entity.total,
    status: entity.status,
    items: entity.items,
    createdAt: entity.createdAt,
  );

  Order toEntity() => Order(
    id: id,
    userId: userId,
    total: total,
    status: status,
    items: items,
    createdAt: createdAt,
  );
}
```

**Tú haces después:**
- Revisar la migración SQL y ejecutarla en Supabase
- Ajustar RLS policies para filtrar por `user_id`
- Implementar los bodies de las páginas (`// TODO: render content`)

---

## Paso 2: Wiring automático — DI + rutas (orquestado)

Como pediste `wiring` en el **Paso 1**, `clean-arch-feature` no se detiene al generar los archivos: en el mismo turno invoca `di-getit-scaffold` y `go-route-scaffold`, pasándoles los componentes recién creados. Cada skill es dueña de su archivo central; aquí solo se delega.

### 2a. `di-getit-scaffold` actualiza el service locator

Actualiza `lib/core/di/service_locator.dart` (modo manual) con:

```dart
// ──────────────────────────────────────────────
// DataSources
// ──────────────────────────────────────────────
sl
  ..registerLazySingleton<OrderRemoteDataSource>(
    () => OrderRemoteDataSourceImpl(supabase: sl<SupabaseClient>()),
  );

// ──────────────────────────────────────────────
// Repositories
// ──────────────────────────────────────────────
sl
  ..registerLazySingleton<OrderRepository>(
    () => OrderRepositoryImpl(
      remoteDataSource: sl<OrderRemoteDataSource>(),
    ),
  );

// ──────────────────────────────────────────────
// UseCases
// ──────────────────────────────────────────────
sl
  ..registerLazySingleton(() => GetOrders(sl()))
  ..registerLazySingleton(() => GetOrder(sl()))
  ..registerLazySingleton(() => CreateOrder(sl()))
  ..registerLazySingleton(() => UpdateOrder(sl()))
  ..registerLazySingleton(() => DeleteOrder(sl()));

// ──────────────────────────────────────────────
// Cubits
// ──────────────────────────────────────────────
sl
  ..registerFactory(() => OrderCubit(
    getOrders: sl(),
    getOrder: sl(),
    createOrder: sl(),
    updateOrder: sl(),
    deleteOrder: sl(),
  ));
```

**Tú haces después:** Nada, queda listo.

### 2b. `go-route-scaffold` actualiza el router

Actualiza `lib/core/router/app_router.dart` con las rutas de las páginas generadas en el Paso 1:

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:order_app/features/order/presentation/pages/orders_list_page.dart';
import 'package:order_app/features/order/presentation/pages/order_detail_page.dart';

class AppRouter {
  late final GoRouter router;

  AppRouter() {
    router = GoRouter(
      initialLocation: '/',
      routes: [
        GoRoute(
          path: '/orders',
          builder: (_, __) => const OrdersListPage(),
          routes: [
            GoRoute(
              path: ':id',
              builder: (_, state) => OrderDetailPage(
                id: state.pathParameters['id']!,
              ),
            ),
          ],
        ),
      ],
    );
  }
}
```

**Tú haces después:**
- Envolver `MaterialApp.router(routerConfig: AppRouter().router)` con `MultiBlocProvider` que incluya los cubits necesarios
- Implementar `OrdersListPage` y `OrderDetailPage`

> **Sin `wiring`:** si hubieras omitido `wiring` en el prompt del Paso 1, estos dos sub-pasos no se ejecutarían; tendrías que pedirlos aparte ("Registra el feature order en service_locator", "Añade rutas de orders al router").

---

## Paso 3: Implementar bodies (tú)

Hasta aquí todo ha sido scaffolding. Ahora implementas los bodies de:

1. **`order_remote_datasource.dart`** — llamadas a Supabase:
   ```dart
   @override
   Future<List<OrderModel>> getAll() async {
     final response = await _supabase
         .from('orders')
         .select()
         .order('created_at', ascending: false);
     return (response as List).map((e) => OrderModel.fromJson(e)).toList();
   }
   ```

2. **`order_repository_impl.dart`** — lógica con Either + try/catch:
   ```dart
   @override
   Future<Either<Failure, List<Order>>> getAll() async {
     try {
       final models = await remoteDataSource.getAll();
       return Right(models.map((m) => m.toEntity()).toList());
     } on ServerException catch (e) {
       return Left(ServerFailure(e.message));
     } on CacheException catch (e) {
       return Left(CacheFailure(e.message));
     }
   }
   ```

3. **`order_cubit.dart`** — llamar usecases y emitir estados:
   ```dart
   Future<void> loadOrders() async {
     emit(OrderLoading());
     final result = await _getOrders(NoParams());
     result.fold(
       (failure) => emit(OrderError(failure.message)),
       (orders) => emit(OrdersLoaded(orders)),
     );
   }
   ```

---

## Paso 4: Añadir página extra a feature existente

Las páginas iniciales ya se generaron en el **Paso 1** (`orders_list_page.dart` con `listener_builder`, `order_detail_page.dart` con `builder`). Ahora imagina que semanas después quieres añadir una página de edición.

**Prompt:**

> Añade una página edit al feature order con patrón form

**Qué ejecuta `clean-arch-component`:**

Carga el template `form` de la sección **"Templates de página"** de `clean-arch-feature` (fuente única — no se duplica) y genera:

`lib/features/order/presentation/pages/order_edit_page.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:order_app/core/services/snackbar_helper.dart';
import 'package:order_app/core/widgets/app_button.dart';
import 'package:order_app/features/order/presentation/cubit/order_cubit.dart';

class OrderEditPage extends StatefulWidget {
  const OrderEditPage({super.key});

  @override
  State<OrderEditPage> createState() => _OrderEditPageState();
}

class _OrderEditPageState extends State<OrderEditPage> {
  final _formKey = GlobalKey<FormState>();

  // TODO: declare TextEditingController for each field
  // late final TextEditingController _statusController;

  @override
  void initState() {
    super.initState();
    // TODO: initialize controllers
    // _statusController = TextEditingController(text: initialValue);
  }

  @override
  void dispose() {
    // TODO: dispose controllers
    // _statusController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Edit Order')),
      body: BlocListener<OrderCubit, OrderState>(
        listener: (context, state) {
          // TODO: handle success / error side effects
          // if (state is OrderUpdated) {
          //   SnackbarHelper.show(context, 'Guardado exitoso', isSuccess: true);
          //   context.pop();
          // }
          // if (state is OrderError) {
          //   SnackbarHelper.show(context, state.message, isSuccess: false);
          // }
        },
        child: BlocBuilder<OrderCubit, OrderState>(
          builder: (context, state) {
            final isLoading = state is OrderLoading;

            return SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // TODO: TextFormField for each field
                    const SizedBox(height: 24),
                    AppButton(
                      label: 'Guardar',
                      onPressed: isLoading ? null : _submit,
                      variant: AppButtonVariant.primary,
                      isLoading: isLoading,
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  void _submit() {
    // TODO: implement submit
    // if (_formKey.currentState!.validate()) {
    //   context.read<OrderCubit>().updateOrder(
    //     Order(...),
    //   );
    // }
  }
}
```

**Tú haces después:**
- Implementar controllers, validación y submit
- Conectar la página en el router (`go-route-scaffold`)

---

## Paso 5: Añadir usecase extra

**Prompt:**

> Añade un usecase `cancel_order` al feature order

**Qué genera `clean-arch-component`:**

`lib/features/order/domain/usecases/cancel_order.dart`:

```dart
import 'package:fpdart/fpdart.dart';
import 'package:equatable/equatable.dart';
import 'package:order_app/core/common/usecase.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/domain/entities/order.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';

class CancelOrder extends UseCase<void, CancelOrderParams> {
  final OrderRepository repository;

  CancelOrder(this.repository);

  @override
  Future<Either<Failure, void>> call(CancelOrderParams params) async {
    throw UnimplementedError('CancelOrder.call');
  }
}

class CancelOrderParams extends Equatable {
  final String orderId;

  const CancelOrderParams({required this.orderId});

  @override
  List<Object?> get props => [orderId];
}
```

**Tú haces después:**
- Implementar `call()` llamando al repositorio
- Registrar `CancelOrder` en service_locator
- Añadir método `cancelOrder` en el cubit

---

## Paso 6: Generar tests

**Prompt:**

> Genera tests para order_cubit

**Qué ejecuta `flutter-test-generator`:**

```bash
python3 skills/flutter-test-generator/generate_test.py \
  lib/features/order/presentation/cubit/order_cubit.dart
```

**Output:**

`test/features/order/presentation/cubit/order_cubit_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/domain/usecases/get_orders.dart';
import 'package:order_app/features/order/presentation/cubit/order_cubit.dart';

class MockGetOrders extends Mock implements GetOrders {}

void main() {
  late OrderCubit cubit;
  late MockGetOrders mockGetOrders;

  setUp(() {
    mockGetOrders = MockGetOrders();
    cubit = OrderCubit(
      getOrders: mockGetOrders,
      getOrder: GetOrder,       // TODO: mock
      createOrder: CreateOrder, // TODO: mock
      updateOrder: UpdateOrder, // TODO: mock
      deleteOrder: DeleteOrder, // TODO: mock
    );
  });

  tearDown(() {
    cubit.close();
  });

  group('OrderCubit', () {
    test('debería tener estado inicial correcto', () {
      // ASSERT: expect(cubit.state, isA<OrderInitial>())
    });

    test('debería emitir estados correctos en flujo exitoso', () {
      // usar blocTest(...)
    });

    test('debería emitir estados de error cuando falla', () {
      // ARRANGE: mockGetOrders(any()) retorna Left(ServerFailure(...))
      // ACT & ASSERT: blocTest con expect: [Loading, Error]
    });
  });
}
```

**Tú haces después:**
- Completar los bodies de cada test con datos reales
- Generar tests para datasource, repository, usecases, modelo
- Ejecutar `flutter test`

---

## Mini-escenarios

Variaciones rápidas para ver cómo cambia el resultado según los parámetros opcionales.

### Mini-A: Feature con Supabase **sin** páginas ni wiring

**Prompt:**

> Crea un feature `order` con campos id, userId, total, status, items, createdAt.
> Operaciones: getAll, getById, create, update, delete.
> Conéctalo a Supabase, tabla `orders` (id uuid PK, user_id uuid NOT NULL, total float8, status text, items jsonb, created_at timestamptz).

**Qué cambia vs el Paso 1:**

| Elemento | Paso 1 (con extras) | Mini-A (sin extras) |
|---|---|---|
| Páginas | `orders_list_page.dart` + `order_detail_page.dart` | placeholder genérico `order_page.dart` |
| `service_locator.dart` | Actualizado (wiring `di`) | No se toca — el resumen final lo recuerda |
| `app_router.dart` | Actualizado (wiring `router`) | No se toca |
| Entity, model, datasource, SQL + RLS | Generados | **Igual**, se generan |

Supabase funciona con o sin páginas/wiring; lo único que se omite son las extras.

### Mini-B: Añadir entity + model a feature existente

**Prompt:**

> Añade una entidad order_item con campos productId: String, quantity: int, price: double, y su model, al feature order

**Qué genera `clean-arch-component`** (dos archivos):

`lib/features/order/domain/entities/order_item.dart`:

```dart
import 'package:equatable/equatable.dart';

class OrderItem extends Equatable {
  const OrderItem({
    required this.productId,
    required this.quantity,
    required this.price,
  });

  final String productId;
  final int quantity;
  final double price;

  @override
  List<Object?> get props => [productId, quantity, price];

  OrderItem copyWith({
    String? productId,
    int? quantity,
    double? price,
  }) {
    return OrderItem(
      productId: productId ?? this.productId,
      quantity: quantity ?? this.quantity,
      price: price ?? this.price,
    );
  }

  @override
  String toString() => 'OrderItem(productId: $productId, quantity: $quantity, price: $price)';
}
```

`lib/features/order/data/models/order_item_model.dart`:

```dart
import 'package:order_app/features/order/domain/entities/order_item.dart';

class OrderItemModel extends OrderItem {
  const OrderItemModel({
    required super.productId,
    required super.quantity,
    required super.price,
  });

  factory OrderItemModel.fromJson(Map<String, dynamic> json) {
    return OrderItemModel(
      productId: json['product_id'] as String,
      quantity: (json['quantity'] as num).toInt(),
      price: (json['price'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() => {
        'product_id': productId,
        'quantity': quantity,
        'price': price,
      };

  factory OrderItemModel.fromEntity(OrderItem entity) => OrderItemModel(
        productId: entity.productId,
        quantity: entity.quantity,
        price: entity.price,
      );

  OrderItem toEntity() => OrderItem(
        productId: productId,
        quantity: quantity,
        price: price,
      );
}
```

**Tú haces después:** implementar los bodies y, si la entidad se usa desde otra clase, ajustar los imports/campos correspondientes.

---

## Resumen del flujo completo

| Paso | Skill | Archivos generados | Lo que haces tú |
|---|---|---|---|
| 1 | `clean-arch-feature` | 18 archivos + SQL migration + 2 páginas | Ejecutar migración, ajustar RLS, bodies de páginas |
| 2 | `clean-arch-feature` → orquesta `di-getit-scaffold` + `go-route-scaffold` | service_locator.dart + app_router.dart actualizados | Conectar en main.dart |
| 3 | *(tú implementas)* | — | Bodies de datasource, repository, cubit |
| 4 | `clean-arch-component` | order_edit_page.dart | Implementar + conectar router |
| 5 | `clean-arch-component` | cancel_order.dart | Implementar + registrar DI + cubit |
| 6 | `flutter-test-generator` | order_cubit_test.dart | Completar datos de prueba |
| 7 | *(tú completas)* | — | Tests restantes + `flutter test` |
