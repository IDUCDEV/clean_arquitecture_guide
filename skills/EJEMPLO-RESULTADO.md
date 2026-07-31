# Ejemplo resultado — Output íntegro de `clean-arch-feature` (Order + Supabase)

Este documento muestra el **resultado final completo** que produce `clean-arch-feature` para el mismo escenario del [EJEMPLO-PRACTICO](./EJEMPLO-PRACTICO.md). Mientras que el EJEMPLO-PRACTICO narra el *flujo paso a paso* con fragmentos, aquí se muestra **cada archivo generado al 100%** — listo para comparar contra tu propio resultado.

## Cómo usar este documento

1. Ejecuta el prompt de abajo en un proyecto con los [prerrequisitos de la arquitectura base](./README.md#prerrequisitos-del-proyecto).
2. Compara archivo por archivo tu resultado contra el de aquí.
3. Diferencias aceptables:
   - `order_app` → el nombre de tu paquete (aparece en imports).
   - `{timestamp}` en el nombre de la migración → la fecha real de generación.
   - Orden de métodos/imports si editaste la skill o tu convención difiere.
4. Si algo difiere de forma estructural (clases, estados, patrones de página), revisa el SKILL.md de la skill correspondiente — el template es la fuente de verdad.

> **Nota:** este es scaffolding puro. Todos los bodies son `throw UnimplementedError()` / `// TODO`. La sección [Scaffolding vs implementado](#scaffolding-vs-implementado) muestra cómo se ven 3 de ellos ya implementados.

---

## El prompt usado

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

---

## Árbol de archivos resultante

```
lib/features/order/
├── data/
│   ├── datasources/
│   │   └── order_remote_datasource.dart
│   ├── models/
│   │   └── order_model.dart
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
        ├── orders_list_page.dart        # pattern listener_builder
        └── order_detail_page.dart       # pattern builder
supabase/
└── migrations/
    └── {timestamp}_create_orders.sql
```

Además, `clean-arch-feature` orquesta el wiring (`[di, router]`), que **actualiza** dos archivos existentes de `core/`:

```
lib/core/di/service_locator.dart      # + registros de Order (di-getit-scaffold)
lib/core/router/app_router.dart       # + rutas /orders y /orders/:id (go-route-scaffold)
```

---

## 1. `domain/entities/order.dart`

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

---

## 2. `domain/repositories/order_repository.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/domain/entities/order.dart';

abstract class OrderRepository {
  Future<Either<Failure, List<Order>>> getAll();

  Future<Either<Failure, Order>> getById(String id);

  Future<Either<Failure, void>> create(Order order);

  Future<Either<Failure, void>> update(Order order);

  Future<Either<Failure, void>> delete(String id);
}
```

---

## 3. UseCases (`domain/usecases/`)

### `get_orders.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:order_app/core/common/usecase.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/domain/entities/order.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';

class GetOrders extends UseCase<List<Order>, NoParams> {
  final OrderRepository repository;

  GetOrders(this.repository);

  @override
  Future<Either<Failure, List<Order>>> call(NoParams params) async {
    throw UnimplementedError('GetOrders.call');
  }
}
```

### `get_order.dart`

```dart
import 'package:equatable/equatable.dart';
import 'package:fpdart/fpdart.dart';
import 'package:order_app/core/common/usecase.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/domain/entities/order.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';

class GetOrder extends UseCase<Order, GetOrderParams> {
  final OrderRepository repository;

  GetOrder(this.repository);

  @override
  Future<Either<Failure, Order>> call(GetOrderParams params) async {
    throw UnimplementedError('GetOrder.call');
  }
}

class GetOrderParams extends Equatable {
  final String id;

  const GetOrderParams({required this.id});

  @override
  List<Object?> get props => [id];
}
```

### `create_order.dart`

```dart
import 'package:equatable/equatable.dart';
import 'package:fpdart/fpdart.dart';
import 'package:order_app/core/common/usecase.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/domain/entities/order.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';

class CreateOrder extends UseCase<void, CreateOrderParams> {
  final OrderRepository repository;

  CreateOrder(this.repository);

  @override
  Future<Either<Failure, void>> call(CreateOrderParams params) async {
    throw UnimplementedError('CreateOrder.call');
  }
}

class CreateOrderParams extends Equatable {
  final String userId;
  final double total;
  final String status;
  final List<OrderItem> items;

  const CreateOrderParams({
    required this.userId,
    required this.total,
    required this.status,
    required this.items,
  });

  @override
  List<Object?> get props => [userId, total, status, items];
}
```

### `update_order.dart`

```dart
import 'package:equatable/equatable.dart';
import 'package:fpdart/fpdart.dart';
import 'package:order_app/core/common/usecase.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/domain/entities/order.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';

class UpdateOrder extends UseCase<void, UpdateOrderParams> {
  final OrderRepository repository;

  UpdateOrder(this.repository);

  @override
  Future<Either<Failure, void>> call(UpdateOrderParams params) async {
    throw UnimplementedError('UpdateOrder.call');
  }
}

class UpdateOrderParams extends Equatable {
  final String id;
  final String userId;
  final double total;
  final String status;
  final List<OrderItem> items;

  const UpdateOrderParams({
    required this.id,
    required this.userId,
    required this.total,
    required this.status,
    required this.items,
  });

  @override
  List<Object?> get props => [id, userId, total, status, items];
}
```

### `delete_order.dart`

```dart
import 'package:equatable/equatable.dart';
import 'package:fpdart/fpdart.dart';
import 'package:order_app/core/common/usecase.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/domain/entities/order.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';

class DeleteOrder extends UseCase<void, DeleteOrderParams> {
  final OrderRepository repository;

  DeleteOrder(this.repository);

  @override
  Future<Either<Failure, void>> call(DeleteOrderParams params) async {
    throw UnimplementedError('DeleteOrder.call');
  }
}

class DeleteOrderParams extends Equatable {
  final String id;

  const DeleteOrderParams({required this.id});

  @override
  List<Object?> get props => [id];
}
```

---

## 4. `data/models/order_model.dart` (mapeo snake_case por Supabase)

```dart
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

---

## 5. `data/datasources/order_remote_datasource.dart` (con `_tableName` + `watchById`)

```dart
import 'dart:async';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:order_app/core/error/exceptions.dart';
import 'package:order_app/features/order/data/models/order_model.dart';

abstract class OrderRemoteDataSource {
  Future<List<OrderModel>> getAll();

  Future<OrderModel> getById(String id);

  Future<void> create(OrderModel order);

  Future<void> update(OrderModel order);

  Future<void> delete(String id);

  Stream<OrderModel> watchById(String id);
}

class OrderRemoteDataSourceImpl implements OrderRemoteDataSource {
  final SupabaseClient _supabase;
  final String _tableName = 'orders';

  OrderRemoteDataSourceImpl({required SupabaseClient supabase})
      : _supabase = supabase;

  @override
  Future<List<OrderModel>> getAll() {
    throw UnimplementedError('OrderRemoteDataSource.getAll');
  }

  @override
  Future<OrderModel> getById(String id) {
    throw UnimplementedError('OrderRemoteDataSource.getById');
  }

  @override
  Future<void> create(OrderModel order) {
    throw UnimplementedError('OrderRemoteDataSource.create');
  }

  @override
  Future<void> update(OrderModel order) {
    throw UnimplementedError('OrderRemoteDataSource.update');
  }

  @override
  Future<void> delete(String id) {
    throw UnimplementedError('OrderRemoteDataSource.delete');
  }

  @override
  Stream<OrderModel> watchById(String id) {
    throw UnimplementedError('OrderRemoteDataSource.watchById');
  }
}
```

---

## 6. `data/repositories/order_repository_impl.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:order_app/core/error/exceptions.dart';
import 'package:order_app/core/error/failures.dart';
import 'package:order_app/features/order/data/datasources/order_remote_datasource.dart';
import 'package:order_app/features/order/domain/entities/order.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';

class OrderRepositoryImpl implements OrderRepository {
  final OrderRemoteDataSource remoteDataSource;

  OrderRepositoryImpl({required this.remoteDataSource});

  @override
  Future<Either<Failure, List<Order>>> getAll() {
    throw UnimplementedError('OrderRepositoryImpl.getAll');
  }

  @override
  Future<Either<Failure, Order>> getById(String id) {
    throw UnimplementedError('OrderRepositoryImpl.getById');
  }

  @override
  Future<Either<Failure, void>> create(Order order) {
    throw UnimplementedError('OrderRepositoryImpl.create');
  }

  @override
  Future<Either<Failure, void>> update(Order order) {
    throw UnimplementedError('OrderRepositoryImpl.update');
  }

  @override
  Future<Either<Failure, void>> delete(String id) {
    throw UnimplementedError('OrderRepositoryImpl.delete');
  }
}
```

---

## 7. `presentation/cubit/order_cubit.dart`

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:order_app/core/common/usecase.dart';
import 'package:order_app/features/order/domain/entities/order.dart';
import 'package:order_app/features/order/domain/usecases/create_order.dart';
import 'package:order_app/features/order/domain/usecases/delete_order.dart';
import 'package:order_app/features/order/domain/usecases/get_order.dart';
import 'package:order_app/features/order/domain/usecases/get_orders.dart';
import 'package:order_app/features/order/domain/usecases/update_order.dart';

part 'order_state.dart';

class OrderCubit extends Cubit<OrderState> {
  final GetOrders _getOrders;
  final GetOrder _getOrder;
  final CreateOrder _createOrder;
  final UpdateOrder _updateOrder;
  final DeleteOrder _deleteOrder;

  OrderCubit({
    required GetOrders getOrders,
    required GetOrder getOrder,
    required CreateOrder createOrder,
    required UpdateOrder updateOrder,
    required DeleteOrder deleteOrder,
  })  : _getOrders = getOrders,
        _getOrder = getOrder,
        _createOrder = createOrder,
        _updateOrder = updateOrder,
        _deleteOrder = deleteOrder,
        super(OrderInitial());

  void loadOrders() {
    throw UnimplementedError('OrderCubit.loadOrders');
  }

  void loadOrder(String id) {
    throw UnimplementedError('OrderCubit.loadOrder');
  }

  void createOrder(Order order) {
    throw UnimplementedError('OrderCubit.createOrder');
  }

  void updateOrder(Order order) {
    throw UnimplementedError('OrderCubit.updateOrder');
  }

  void deleteOrder(String id) {
    throw UnimplementedError('OrderCubit.deleteOrder');
  }

  void clearError() {
    // TODO: optional — emit copy of previous state without error
  }
}
```

---

## 8. `presentation/cubit/order_state.dart`

```dart
part of 'order_cubit.dart';

sealed class OrderState extends Equatable {
  const OrderState();

  @override
  List<Object?> get props => [];
}

final class OrderInitial extends OrderState {}

final class OrderLoading extends OrderState {}

final class OrdersLoaded extends OrderState {
  final List<Order> orders;
  const OrdersLoaded(this.orders);

  @override
  List<Object?> get props => [orders];
}

final class OrderLoaded extends OrderState {
  final Order order;
  const OrderLoaded(this.order);

  @override
  List<Object?> get props => [order];
}

final class OrderError extends OrderState {
  final String message;
  const OrderError(this.message);

  @override
  List<Object?> get props => [message];
}
```

---

## 9. `presentation/pages/orders_list_page.dart` (pattern `listener_builder`)

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
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<OrderCubit>().loadOrders();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Orders')),
      body: BlocListener<OrderCubit, OrderState>(
        listener: (context, state) {
          // TODO: handle side effects
          // if (state is OrderLoaded && state.xxxError != null) {
          //   SnackbarHelper.show(context, state.xxxError!, isSuccess: false);
          //   context.read<OrderCubit>().clearXxxError();
          // }
          // if (state is OrderActionSuccess) {
          //   SnackbarHelper.show(context, 'Operación exitosa', isSuccess: true);
          //   context.pop();
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
                      onPressed: () => context.read<OrderCubit>().loadOrders(),
                      variant: AppButtonVariant.primary,
                    ),
                  ],
                ),
              );
            }
            if (state is OrdersLoaded) {
              // TODO: render content
              return const Center(child: Text('Implement OrdersListPage content'));
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

---

## 10. `presentation/pages/order_detail_page.dart` (pattern `builder`)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:order_app/core/widgets/app_button.dart';
import 'package:order_app/features/order/presentation/cubit/order_cubit.dart';

class OrderDetailPage extends StatelessWidget {
  const OrderDetailPage({super.key, required this.id});

  final String id;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Order Detail')),
      body: BlocBuilder<OrderCubit, OrderState>(
        builder: (context, state) {
          if (state is OrderLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          if (state is OrderLoaded) {
            // TODO: render content
            return const Center(child: Text('Implement OrderDetailPage content'));
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
                    onPressed: () => context.read<OrderCubit>().loadOrder(id),
                    variant: AppButtonVariant.primary,
                  ),
                ],
              ),
            );
          }
          return const Center(child: CircularProgressIndicator());
        },
      ),
    );
  }
}
```

---

## 11. `supabase/migrations/{timestamp}_create_orders.sql`

```sql
-- Create orders table
-- Review and customize before applying

CREATE TABLE orders (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL,
  total float8 NOT NULL,
  status text NOT NULL DEFAULT 'pending',
  items jsonb NOT NULL DEFAULT '[]',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Indexes
CREATE INDEX orders_user_id_idx ON orders (user_id);
CREATE INDEX orders_created_at_idx ON orders (created_at);

-- Enable Row Level Security
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- RLS Policies (customize per business rules)

-- Allow read access to authenticated users
CREATE POLICY "Users can read orders"
  ON orders
  FOR SELECT
  TO authenticated
  USING (true);

-- Allow insert for authenticated users
CREATE POLICY "Users can insert orders"
  ON orders
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Allow update for own records
CREATE POLICY "Users can update own orders"
  ON orders
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id);

-- Triggers
-- (add triggers if needed)
```

---

## Wiring: archivos actualizados por orquestación

### 12. `lib/core/di/service_locator.dart` — registros añadidos por `di-getit-scaffold`

Los imports de `core/` y las librerías externas ya existían. `di-getit-scaffold` añade **solo** estas secciones (modo manual):

```dart
import 'package:order_app/features/order/data/datasources/order_remote_datasource.dart';
import 'package:order_app/features/order/data/repositories/order_repository_impl.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';
import 'package:order_app/features/order/domain/usecases/create_order.dart';
import 'package:order_app/features/order/domain/usecases/delete_order.dart';
import 'package:order_app/features/order/domain/usecases/get_order.dart';
import 'package:order_app/features/order/domain/usecases/get_orders.dart';
import 'package:order_app/features/order/domain/usecases/update_order.dart';
import 'package:order_app/features/order/presentation/cubit/order_cubit.dart';
```

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

### 13. `lib/core/router/app_router.dart` — rutas añadidas por `go-route-scaffold`

`go-route-scaffold` (básico, sin auth ni Sentry) añade las rutas dentro de la lista `routes`:

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

---

## Scaffolding vs implementado

Todo lo anterior es estructura con `throw UnimplementedError()`. Así se ven 3 bodies ya implementados (tu trabajo — el "después"):

**Datasource — `getAll()`:**

```dart
@override
Future<List<OrderModel>> getAll() async {
  final response = await _supabase
      .from(_tableName)
      .select()
      .order('created_at', ascending: false);
  return (response as List).map((e) => OrderModel.fromJson(e)).toList();
}
```

**Repository — `getAll()`:**

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

**Cubit — `loadOrders()`:**

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

## Siguiente paso

- Revisar y ejecutar la migración en Supabase (`supabase db push` o el SQL editor).
- Ajustar las RLS policies si tu regla de negocio no es `auth.uid() = user_id`.
- Completar los bodies de cada archivo.
- Para ver el flujo completo (tests, página extra, usecase extra), ver [EJEMPLO-PRACTICO.md](./EJEMPLO-PRACTICO.md).
