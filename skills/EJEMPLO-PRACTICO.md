# Ejemplo práctico — Feature "Orders" de principio a fin

Guía paso a paso usando las 7 skills para construir un feature completo de gestión de pedidos.

---

## Escenario

Queremos un feature **Order** con:

- Listar pedidos, ver detalle, crear, actualizar, cancelar
- Persistencia en Supabase (tabla `orders`)
- Ruta `/orders` (lista) y `/orders/:id` (detalle)

---

## Paso 1: Scaffold completo del feature + Supabase

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

**Qué genera `clean-arch-feature`:**

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
        └── order_page.dart
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

---

## Paso 2: Registrar dependencias en GetIt

**Prompt:**

> Registra el feature order en service_locator en modo manual

**Qué genera `di-getit-scaffold`:**

Actualiza `lib/core/di/service_locator.dart` con:

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

---

## Paso 3: Añadir rutas

**Prompt:**

> Añade rutas al router:
> - `/orders` → OrdersListPage
> - `/orders/:id` → OrderDetailPage
> Sin auth redirect, sin Sentry

**Qué genera `go-route-scaffold`:**

Actualiza `lib/core/router/app_router.dart`:

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

---

## Paso 4: Implementar bodies (tú)

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

## Paso 5: Generar páginas con BlocListener + BlocBuilder

**Prompt:**

> Genera una página de listado de orders con listener_builder.
> Feature: order, page: list, pattern: listener_builder

**Qué genera `widget-page-scaffold`:**

`lib/features/order/presentation/pages/orders_list_page.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:order_app/core/services/snackbar_helper.dart';
import 'package:order_app/core/widgets/app_button.dart';
import 'package:order_app/features/order/presentation/cubit/order_cubit.dart';

class OrdersListPage extends StatefulWidget {
  const OrdersListPage({super.key});

  @override
  State<OrdersListPage> createState() => _OrdersListPageState();
}

class _OrdersListPageState extends State<OrdersListPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _refresh());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Orders')),
      body: BlocListener<OrderCubit, OrderState>(
        listener: (context, state) {
          // TODO: side effects — snackbars, navegación
          // if (state is OrderLoaded && state.xxxError != null) {
          //   SnackbarHelper.show(context, state.xxxError!, isSuccess: false);
          //   context.read<OrderCubit>().clearXxxError();
          // }
        },
        child: BlocBuilder<OrderCubit, OrderState>(
          builder: (context, state) {
            if (state is OrderLoading) {
              return const Center(child: CircularProgressIndicator());
            }
            if (state is OrderError) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(state.message, overflow: TextOverflow.ellipsis),
                    const SizedBox(height: 16),
                    AppButton(
                      label: 'Reintentar',
                      onPressed: _refresh,
                      variant: AppButtonVariant.primary,
                    ),
                  ],
                ),
              );
            }
            if (state is OrdersLoaded) {
              final orders = state.orders;
              if (orders.isEmpty) {
                return const Center(child: Text('No orders yet'));
              }
              return ListView.builder(
                itemCount: orders.length,
                itemBuilder: (context, index) {
                  final order = orders[index];
                  return ListTile(
                    title: Text('Order #${order.id.substring(0, 8)}'),
                    subtitle: Text('\$${order.total.toStringAsFixed(2)}'),
                    trailing: Text(order.status),
                  );
                },
              );
            }
            return const Center(child: CircularProgressIndicator());
          },
        ),
      ),
    );
  }

  void _refresh() {
    context.read<OrderCubit>().loadOrders();
  }
}
```

**Tú haces después:**
- Conectar la página en el router
- Implementar los side effects en el listener
- Ajustar el renderizado de cada estado

---

## Paso 6: Añadir usecase extra

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

## Paso 7: Generar tests

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

## Resumen del flujo completo

| Paso | Skill | Archivos generados | Lo que haces tú |
|---|---|---|---|---|
| 1 | `clean-arch-feature` | 18 archivos + SQL migration | Ejecutar migración, ajustar RLS |
| 2 | `di-getit-scaffold` | service_locator.dart actualizado | — |
| 3 | `go-route-scaffold` | app_router.dart actualizado | Conectar en main.dart |
| 4 | *(tú implementas)* | — | Bodies de datasource, repository, cubit |
| 5 | `widget-page-scaffold` | orders_list_page.dart | Conectar router |
| 6 | `clean-arch-component` | cancel_order.dart | Implementar + registrar DI + cubit |
| 7 | `flutter-test-generator` | order_cubit_test.dart | Completar datos de prueba |
| 8 | *(tú completas)* | — | Tests restantes + `flutter test` |
