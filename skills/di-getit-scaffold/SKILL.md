---
name: di-getit-scaffold
description: Generate or update GetIt dependency injection module (manual or injectable mode). Registers DataSources, Repositories, UseCases, and Cubits following the project's layer ordering. Only generates structure — never implementation bodies.
---

# di-getit-scaffold — Scaffold de inyección de dependencias con GetIt

Genera el archivo de registro de dependencias para GetIt, en modo manual o con injectable. Ordena por capa: external → core → datasources → repositories → usecases → cubits.

> **Orquestación:** esta skill suele invocarse desde `clean-arch-feature` cuando el usuario pide `wiring: [di]`. En ese flujo, los componentes generados (datasources, repositorios, usecases, cubit, estado) se pasan como entrada. Puede usarse también de forma independiente sobre un feature ya existente.

## Input requerido

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `mode` | Estilo de DI | `manual` o `injectable` |
| `app_name` | Nombre del paquete | `my_app` |
| `features` | Lista de features con sus dependencias | (ver tabla abajo) |
| `external_libs` | Librerías externas a registrar | `SupabaseClient`, `Dio`, `Isar`, `InternetConnection` |

### Formato de `features`

Cada feature puede incluir:

```yaml
feature: product
external_datasources: [SupabaseClient]
remote_datasource: ProductRemoteDataSource
local_datasource: ProductLocalDataSource  # opcional
repository: ProductRepository
repository_impl: ProductRepositoryImpl
usecases: [GetProducts, GetProduct, CreateProduct, UpdateProduct, DeleteProduct]
cubit: ProductCubit
```

## Output

### Modo manual

`lib/core/di/service_locator.dart`

```dart
import 'package:get_it/get_it.dart';
import 'package:isar/isar.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:dio/dio.dart';
// ... imports de datasources, repositories, usecases, cubits
// import 'package:{app_name}/core/services/user_session.dart';
// import 'package:{app_name}/core/network/network_info.dart';

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
    ..registerLazySingleton<ProductRemoteDataSource>(
      () => ProductRemoteDataSourceImpl(supabase: sl<SupabaseClient>()),
    );

  // ──────────────────────────────────────────────
  // Repositories
  // ──────────────────────────────────────────────
  sl
    ..registerLazySingleton<ProductRepository>(
      () => ProductRepositoryImpl(
        remoteDataSource: sl<ProductRemoteDataSource>(),
      ),
    );

  // ──────────────────────────────────────────────
  // UseCases
  // ──────────────────────────────────────────────
  sl
    ..registerLazySingleton(() => GetProducts(sl()))
    ..registerLazySingleton(() => GetProduct(sl()))
    ..registerLazySingleton(() => CreateProduct(sl()))
    ..registerLazySingleton(() => DeleteProduct(sl()));

  // ──────────────────────────────────────────────
  // Cubits
  // ──────────────────────────────────────────────
  sl
    ..registerFactory(() => ProductCubit(
      getProducts: sl(),
      getProduct: sl(),
      createProduct: sl(),
      deleteProduct: sl(),
    ));
}
```

### Modo injectable

`lib/core/di/injection_container.dart`

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

Anotaciones requeridas en cada clase:

| Capa | Anotación |
|---|---|
| DataSource (impl) | `@LazySingleton(as: ProductRemoteDataSource)` |
| Repository (impl) | `@LazySingleton(as: ProductRepository)` |
| UseCase | `@lazySingleton` |
| Cubit | `@injectable` |
| Módulo externo | `@module` en abstract class con `@preResolve` |

```dart
// Ejemplo de anotaciones para módulo externo
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

## Workflow

1. Preguntar al usuario: mode (manual/injectable), app_name, lista de features con sus dependencias
2. Si `service_locator.dart` no existe, crearlo desde cero
3. Si existe, añadir los nuevos registros en la sección correspondiente
4. Respetar el orden de capas: external → core → datasources → repositories → usecases → cubits
5. `registerLazySingleton` para todo excepto Cubits (`registerFactory`)
6. Los bodies de configuración van con `throw UnimplementedError()` o `// TODO: configure`
7. Recordar al usuario que debe: completar configuraciones, añadir imports faltantes, y verificar con análisis estático
