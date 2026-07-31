# Ejemplo resultado 2 — Output íntegro de las skills de infraestructura

Este documento muestra el **resultado final completo** que producen `di-getit-scaffold`, `go-route-scaffold`, `clean-arch-component` y `flutter-test-generator`, siguiendo el mismo formato "espejo" de [EJEMPLO-RESULTADO.md](./EJEMPLO-RESULTADO.md) (que cubre `clean-arch-feature`).

Escenario base: el feature **Order** con Supabase del [EJEMPLO-PRACTICO.md](./EJEMPLO-PRACTICO.md) (app `order_app`).

## Cómo usar este documento

- Compara archivo por archivo contra tu resultado real.
- Diferencias aceptables: `order_app` (nombre del paquete), nombres de rutas, imports comentados si la página aún no existe.
- Los templates de cada `SKILL.md` son la fuente de verdad.

---

## A. `di-getit-scaffold` — registro de dependencias

### A.1 Prompt

> Registra el feature order en service_locator en modo manual

### A.2 Output (modo manual) — `lib/core/di/service_locator.dart` completo

```dart
import 'package:get_it/get_it.dart';
import 'package:isar/isar.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:dio/dio.dart';
import 'package:internet_connection_checker_plus/internet_connection_checker_plus.dart';
// ... imports de datasources, repositories, usecases, cubits
import 'package:order_app/features/order/data/datasources/order_remote_datasource.dart';
import 'package:order_app/features/order/data/repositories/order_repository_impl.dart';
import 'package:order_app/features/order/domain/repositories/order_repository.dart';
import 'package:order_app/features/order/domain/usecases/create_order.dart';
import 'package:order_app/features/order/domain/usecases/delete_order.dart';
import 'package:order_app/features/order/domain/usecases/get_order.dart';
import 'package:order_app/features/order/domain/usecases/get_orders.dart';
import 'package:order_app/features/order/domain/usecases/update_order.dart';
import 'package:order_app/features/order/presentation/cubit/order_cubit.dart';
// import 'package:order_app/core/services/user_session.dart';
// import 'package:order_app/core/network/network_info.dart';

final sl = GetIt.instance;

Future<void> initDependencies() async {
  await IsarService.initialize();

  // ──────────────────────────────────────────────
  // External libraries
  // ──────────────────────────────────────────────
  sl
    ..registerLazySingleton<Isar>(() => IsarService.instance)
    ..registerLazySingleton<SupabaseClient>(() => Supabase.instance.client)
    ..registerLazySingleton<Dio>(() {
      throw UnimplementedError('Dio.init — configure BaseOptions');
    })
    ..registerLazySingleton<InternetConnection>(InternetConnection.createInstance);

  // ──────────────────────────────────────────────
  // Core services
  // ──────────────────────────────────────────────
  sl
    ..registerLazySingleton<NetworkInfo>(() => NetworkInfoImpl(sl<InternetConnection>()))
    ..registerLazySingleton<UserSession>(() => UserSessionImpl(sl<Isar>(), supabase: sl<SupabaseClient>()))
    ..registerLazySingleton<CacheManager>(CacheManager.new);

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
}
```

> Si `service_locator.dart` ya existía con otros features, `di-getit-scaffold` **añade** los nuevos registros en su sección correspondiente, respetando el orden de capas. Los imports de `core/` van comentados hasta que existan esos servicios.

### A.3 Output (modo injectable) — `lib/core/di/injection_container.dart`

**Prompt:** "Registra el feature order en service_locator en modo injectable"

```dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';

final getIt = GetIt.instance;

@InjectableInit(
  initializerName: r'$initGetIt',
  preferRelativeImports: true,
  asExtension: false,
)
Future<void> configureDependencies() async {
  await $initGetIt(getIt);
}
```

Anotaciones requeridas en cada clase del feature (las añade el desarrollador al implementar):

| Capa | Anotación |
|---|---|
| DataSource (impl) | `@LazySingleton(as: OrderRemoteDataSource)` |
| Repository (impl) | `@LazySingleton(as: OrderRepository)` |
| UseCase | `@lazySingleton` |
| Cubit | `@injectable` |
| Módulo externo | `@module` en abstract class con `@preResolve` |

```dart
@module
abstract class ExternalModule {
  @preResolve
  Future<SharedPreferences> get prefs => SharedPreferences.getInstance();

  @lazySingleton
  Dio get dio => Dio(BaseOptions(
        baseUrl: 'https://api.example.com',
        connectTimeout: const Duration(seconds: 30),
      ));
}
```

---

## B. `go-route-scaffold` — configuración de rutas

### B.1 Básico (sin auth, sin Sentry)

Ver [EJEMPLO-RESULTADO.md §13](./EJEMPLO-RESULTADO.md) — el output completo ya está mostrado ahí, no se duplica.

### B.2 Con auth redirect

**Prompt:**

> Añade rutas al router con auth redirect. Estado autenticado: AuthAuthenticated. Rutas: `/login` → LoginPage, `/` → HomePage, `/orders` → OrdersListPage, `/orders/:id` → OrderDetailPage

Output — `lib/core/router/app_router.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
// TODO: import pages de auth y home (no generadas en este escenario)
// import 'package:order_app/features/auth/presentation/cubit/auth_cubit.dart';
// import 'package:order_app/features/auth/presentation/pages/login_page.dart';
// import 'package:order_app/features/home/presentation/pages/home_page.dart';
import 'package:order_app/features/order/presentation/pages/orders_list_page.dart';
import 'package:order_app/features/order/presentation/pages/order_detail_page.dart';

class AppRouter {
  late final GoRouter router;

  AppRouter() {
    router = GoRouter(
      initialLocation: '/login',
      redirect: (context, state) {
        final auth = context.read<AuthCubit>().state;
        final estaAutenticado = auth is AuthAuthenticated;
        final estaEnLogin = state.matchedLocation == '/login';

        // TODO: implement auth redirect
        // if (!estaAutenticado && !estaEnLogin) return '/login';
        // if (estaAutenticado && estaEnLogin) return '/';
        return null;
      },
      routes: [
        GoRoute(
          path: '/login',
          builder: (_, __) {
            // TODO: replace with LoginPage
            throw UnimplementedError('LoginPage not implemented');
          },
        ),
        GoRoute(
          path: '/',
          builder: (_, __) {
            // TODO: replace with HomePage
            throw UnimplementedError('HomePage not implemented');
          },
        ),
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

> Las páginas de auth/home existen en tu proyecto real: se descomentan los imports y se reemplaza el `throw UnimplementedError` por `const LoginPage()` / `const HomePage()`.

### B.3 Con Sentry

**Prompt:** "Añade rutas al router con Sentry. Rutas: `/orders` y `/orders/:id`"

Output — `lib/core/router/app_router.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:sentry_flutter/sentry_flutter.dart';
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
      observers: [
        SentryNavigatorObserver(),
      ],
    );
  }
}
```

Configuración adicional en `main.dart`:

```dart
await SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    options.tracesSampleRate = 1.0;
  },
  appRunner: () => runApp(const MyApp()),
);
```

### B.4 Combinado (auth + Sentry)

`go-route-scaffold` soporta `has_auth: true` y `use_sentry: true` a la vez: el resultado es el template **B.2** con la lista `observers: [SentryNavigatorObserver()]` añadida al final de `GoRouter(...)`.

---

## C. `clean-arch-component` — piezas individuales (compacto)

Sus templates son los **mismos archivos** que `clean-arch-feature` genera (fuente única). Por eso aquí solo se mapea qué genera cada tipo y **dónde ver su ejemplo completo**:

| `component_type` | Archivo generado | Ejemplo completo en |
|---|---|---|
| `entity` | `domain/entities/{feature}.dart` | [EJEMPLO-RESULTADO.md §1](./EJEMPLO-RESULTADO.md), EJEMPLO-PRACTICO Mini-B |
| `model` | `data/models/{feature}_model.dart` | [EJEMPLO-RESULTADO.md §4](./EJEMPLO-RESULTADO.md), EJEMPLO-PRACTICO Mini-B |
| `usecase` | `domain/usecases/{action}_{feature}.dart` | EJEMPLO-PRACTICO Paso 5 (`cancel_order`) |
| `cubit` | `presentation/cubit/{feature}_cubit.dart` | [EJEMPLO-RESULTADO.md §7](./EJEMPLO-RESULTADO.md) |
| `datasource` | `data/datasources/{feature}_remote_datasource.dart` | [EJEMPLO-RESULTADO.md §5](./EJEMPLO-RESULTADO.md) |
| `repository` | `domain/repositories/{feature}_repository.dart` | [EJEMPLO-RESULTADO.md §2](./EJEMPLO-RESULTADO.md) |
| `repository_impl` | `data/repositories/{feature}_repository_impl.dart` | [EJEMPLO-RESULTADO.md §6](./EJEMPLO-RESULTADO.md) |
| `page` | `presentation/pages/{feature}_{page}_page.dart` | EJEMPLO-PRACTICO Paso 4 (pattern `form`) |

**Prompt típico → resultado:**

> "Añade un usecase cancel_order al feature order"

→ 1 archivo: `lib/features/order/domain/usecases/cancel_order.dart` (con `CancelOrder` + `CancelOrderParams extends Equatable`, body `throw UnimplementedError`). Ver output completo en EJEMPLO-PRACTICO Paso 5.

---

## D. `flutter-test-generator` — tests boilerplate (compacto)

### D.1 Uso

```bash
python3 skills/flutter-test-generator/generate_test.py lib/features/order/data/models/order_model.dart
```

Genera `test/features/order/data/models/order_model_test.dart` (mismo path bajo `test/`).

### D.2 Capas detectadas

| Path en `lib/` | Test generado |
|---|---|
| `domain/entities/` | Equatable, copyWith, props |
| `domain/usecases/` | Mock repository + `Either<Failure, T>` |
| `data/models/` | fromJson, toJson, roundtrip, conversión entidad |
| `data/datasources/` | Mock client + `ServerException` |
| `data/repositories/` | Mock datasources + network (online/offline) |
| `presentation/cubit/` (no state) | `blocTest` + mock usecases |
| `presentation/cubit/` (state) | Igualdad y props de cada estado |
| `presentation/pages/` o `widgets/` | `testWidgets` + mock `BlocProvider` |

### D.3 Output de ejemplo — test de **model** (capa aún no mostrada)

**Prompt:** "Genera tests para order_model"

Output — `test/features/order/data/models/order_model_test.dart`:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'dart:convert';
import 'dart:io';
import 'package:order_app/features/order/data/models/order_model.dart';
import '../../../helpers/fixture_reader.dart';

void main() {
  group('OrderModel', () {
    group('fromJson', () {
      test('debería retornar un modelo válido desde JSON', () {
        // ARRANGE: cargar fixture con fixtureAsMap('order')
        // ACT: llamar OrderModel.fromJson(jsonMap)
        // ASSERT: verificar cada campo del modelo resultante
      });

      test('debería lanzar error cuando falta un campo requerido', () {
        // ARRANGE: crear JSON parcial sin campos required
        // ACT & ASSERT: expect(() => OrderModel.fromJson(incomplete), throwsA(isA<TypeError>()))
      });

      test('debería ignorar campos extra en el JSON', () {
        // ARRANGE: crear JSON con campos adicionales
        // ACT: llamar OrderModel.fromJson(jsonMap)
        // ASSERT: verificar que se crea el modelo correctamente
      });
    });

    group('toJson', () {
      test('debería retornar un mapa JSON válido', () {
        // ARRANGE: crear instancia del modelo
        // ACT: llamar model.toJson()
        // ASSERT: verificar keys y valores (incluyendo snake_case si aplica)
      });
    });

    group('roundtrip', () {
      test('toJson + fromJson debería ser inverso', () {
        // ARRANGE: crear instancia del modelo
        // ACT: json = model.toJson(); recreated = Model.fromJson(json)
        // ASSERT: expect(recreated, equals(original))
      });
    });

    group('entity conversion', () {
      test('toEntity debería retornar Entity correcta', () {
        // ARRANGE: crear instancia del modelo
        // ACT: llamar model.toEntity()
        // ASSERT: verificar que retorna isA<Entity>() con campos mapeados
      });

      test('fromEntity debería crear Model desde Entity', () {
        // ARRANGE: crear instancia de Entity
        // ACT: llamar Model.fromEntity(entity)
        // ASSERT: verificar que retorna isA<Model>() con campos copiados
      });
    });
  });
}
```

> Los bodies van vacíos con comentarios AAA en español — el desarrollador completa la lógica. El cubit test se muestra en EJEMPLO-PRACTICO Paso 6.

---

## Siguiente paso

- Para el resultado del feature completo (entity → page + SQL + wiring), ver [EJEMPLO-RESULTADO.md](./EJEMPLO-RESULTADO.md).
- Para el flujo paso a paso con prompts, ver [EJEMPLO-PRACTICO.md](./EJEMPLO-PRACTICO.md).
