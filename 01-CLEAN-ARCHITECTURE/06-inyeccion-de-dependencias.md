## 6. Inyección de Dependencias con GetIt

### ¿Qué es la Inyección de Dependencias?

Imagina que estás construyendo una casa. Necesitas un electricista, un plomero y un carpintero. En lugar de que cada uno fabrication sus propias herramientas, **tú les proporcionas las herramientas que necesitan**.

En programación:
- Una **dependencia** es cualquier objeto que tu clase necesita para funcionar
- **Inyectar** significa proporcionar esos objetos desde afuera

**¿Por qué es importante?**
1. **Desacoplamiento**: Las clases no dependen de implementaciones específicas
2. **Testabilidad**: Puedes inyectar "mocks" para probar tu código
3. **Flexibilidad**: Puedes cambiar implementaciones sin modificar el código

### El Problema: Constructor Drilling

Sin inyección de dependencias centralizada:

```dart
// ❌ SIN inyección centralizada - MUY TEDIOSO
void main() {
  final localDataSource = UserLocalDataSourceImpl(box: box);
  final repository = UserRepositoryImpl(localDataSource: localDataSource);
  final getUsers = GetUsers(repository);
  final createUser = CreateUser(repository);
  final cubit = UserCubit(
    getUsers: getUsers,
    getUser: getUser,
    createUser: createUser,
    deleteUser: deleteUser,
  );
}
```

### Solución: GetIt (Service Locator)

**GetIt** es un paquete que implementa el patrón **Service Locator**. Hay dos estilos: **manual** (cascade notation) y **automático** (con `injectable`). Ambos son válidos; el manual es más explícito y el automático reduce boilerplate.

### Conceptos clave de GetIt

| Método | Descripción | Cuándo usarlo |
|--------|-------------|---------------|
| `registerSingleton()` | Crea la instancia inmediatamente | Para objetos que deben existir desde el inicio |
| `registerLazySingleton()` | Crea la instancia la primera vez que se use | Para objetos pesados que quizás no se usen (recomendado) |
| `registerFactory()` | Crea una nueva instancia CADA vez que se pida | Para objetos que no deben compartir estado (como Cubits) |

### Estilo 1: Manual con cascade notation (recomendado)

> Cada dependencia se registra explícitamente con `sl.registerLazySingleton<T>(() => T(...))`, usando cascade (`..`) para agrupar por capa.

**Archivo**: `lib/core/di/service_locator.dart`

```dart
import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:internet_connection_checker_plus/internet_connection_checker_plus.dart';
import 'package:isar_community/isar.dart';
import 'package:path_provider/path_provider.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:my_app/core/data/local/isar_service.dart';
import 'package:my_app/core/network/network_info.dart';
import 'package:my_app/core/services/cache_manager.dart';
import 'package:my_app/core/session/user_session.dart';
import 'package:my_app/core/session/user_session_impl.dart';
import 'package:my_app/features/user/data/datasources/user_local_data_source.dart';
import 'package:my_app/features/user/data/datasources/user_remote_data_source.dart';
import 'package:my_app/features/user/data/models/user_model.dart';
import 'package:my_app/features/user/data/repositories/user_repository_impl.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';
import 'package:my_app/features/user/domain/usecases/create_user.dart';
import 'package:my_app/features/user/domain/usecases/delete_user.dart';
import 'package:my_app/features/user/domain/usecases/get_user.dart';
import 'package:my_app/features/user/domain/usecases/get_users.dart';
import 'package:my_app/features/user/presentation/cubit/user_cubit.dart';

final sl = GetIt.instance;

Future<void> initDependencies() async {
  await IsarService.initialize();

  sl
    // ╔══════════════════════════════════════════════════════════╗
    // ║  CAPA EXTERNA - Librerías de terceros                   ║
    // ╚══════════════════════════════════════════════════════════╝
    ..registerLazySingleton<Isar>(() => IsarService.instance)
    ..registerLazySingleton<InternetConnection>(
      InternetConnection.createInstance,
    )
    ..registerLazySingleton<Dio>(() {
      final dio = Dio(BaseOptions(
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {'Content-Type': 'application/json'},
      ));
      dio.interceptors.add(LogInterceptor(
        requestBody: true,
        responseBody: true,
      ));
      return dio;
    })

    // ╔══════════════════════════════════════════════════════════╗
    // ║  CORE - Network, Session, Cache                         ║
    // ╚══════════════════════════════════════════════════════════╝
    ..registerLazySingleton<NetworkInfo>(
      () => NetworkInfoImpl(sl<InternetConnection>()),
    )
    ..registerLazySingleton<UserSession>(
      () => UserSessionImpl(sl<Isar>(), supabase: Supabase.instance.client),
    )
    ..registerLazySingleton<CacheManager>(CacheManager.new)

    // ╔══════════════════════════════════════════════════════════╗
    // ║  CAPA DE DATOS - DataSources                            ║
    // ╚══════════════════════════════════════════════════════════╝
    ..registerLazySingleton<UserRemoteDataSource>(
      () => UserRemoteDataSourceImpl(client: sl<Dio>()),
    )
    ..registerLazySingleton<UserLocalDataSource>(
      () => UserLocalDataSourceImpl(sl<Isar>()),
    )

    // ╔══════════════════════════════════════════════════════════╗
    // ║  CAPA DE REPOSITORIO                                    ║
    // ╚══════════════════════════════════════════════════════════╝
    ..registerLazySingleton<UserRepository>(
      () => UserRepositoryImpl(
        remoteDataSource: sl<UserRemoteDataSource>(),
        localDataSource: sl<UserLocalDataSource>(),
        networkInfo: sl<NetworkInfo>(),
        userSession: sl<UserSession>(),
      ),
    )

    // ╔══════════════════════════════════════════════════════════╗
    // ║  CAPA DE DOMINIO - UseCases                             ║
    // ╚══════════════════════════════════════════════════════════╝
    ..registerLazySingleton(() => GetUsers(sl()))
    ..registerLazySingleton(() => GetUser(sl()))
    ..registerLazySingleton(() => CreateUser(sl()))
    ..registerLazySingleton(() => DeleteUser(sl()))

    // ╔══════════════════════════════════════════════════════════╗
    // ║  CAPA DE PRESENTACIÓN - Cubit                           ║
    // ╚══════════════════════════════════════════════════════════╝
    ..registerFactory(() => UserCubit(
      getUsers: sl(),
      getUser: sl(),
      createUser: sl(),
      deleteUser: sl(),
    ));

  // Registrar limpieza de cachés en CacheManager
  sl<CacheManager>()
    ..register(() => sl<UserLocalDataSource>().clearCache());
}
```

> **Cascade notation** (`..`): permite llamar múltiples métodos sobre el mismo objeto sin repetir `sl.` cada vez. Cada `..registerLazySingleton` opera sobre el mismo `sl`.

#### Registro de repositorios con UserSession

Cuando el repositorio requiere `UserSession`, se pasa explícitamente:

```dart
..registerLazySingleton<ProfileRepository>(
  () => ProfileRepositoryImpl(
    remoteDataSource: sl<ProfileRemoteDataSource>(),
    localDataSource: sl<ProfileLocalDataSource>(),
    networkInfo: sl<NetworkInfo>(),
    userSession: sl<UserSession>(),
  ),
)
```

### Estilo 2: Automático con injectable (para proyectos grandes)

> Usa código generado para reducir boilerplate. Ideal cuando tienes 20+ features. Tus clases se anotan y `injectable` genera el registro automático. **Requiere `build_runner`**.

```yaml
# pubspec.yaml
dependencies:
  get_it: ^8.0.3
  injectable: ^2.5.0

dev_dependencies:
  injectable_generator: ^2.7.0
  build_runner: ^2.4.15
```

**Archivo**: `lib/core/di/injection_container.dart`

```dart
import 'package:get_it/get_it.dart';
import 'package:injectable/injectable.dart';
import 'package:my_app/core/di/injection_container.config.dart';

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

Luego cada clase se anota:

```dart
@lazySingleton
class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final Dio client;
  UserRemoteDataSourceImpl(this.client);
  // ...
}

@lazySingleton
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  final NetworkInfo networkInfo;
  final UserSession userSession;

  UserRepositoryImpl(
    this.remoteDataSource,
    this.localDataSource,
    this.networkInfo,
    this.userSession,
  );
  // ...
}
```

### ¿Cuál elegir?

| Criterio | Manual | Injectable |
|----------|--------|------------|
| Boilerplate | Más código escrito | Menos código (generado) |
| Visibilidad | Explícito, fácil de debuggear | Oculto tras código generado |
| Dependencia extra | No | `injectable` + generator + build_runner |
| Ideal para | Proyectos pequeños/medios (< 15 features) | Proyectos grandes (20+ features) |
| Control fino | Total | Limitado por anotaciones |
| Tiempo de compilación | Sin impacto | build_runner en cada cambio |

> **Nota**: Si usas **solo** base de datos local sin API, el `remoteDataSource` no es necesario. En ese caso, el `UserRepositoryImpl` solo usaría `localDataSource`.

**Versión con solo Isar (sin API REST):**

```dart
// Versión simplificada solo con base de datos local Isar
Future<void> init() async {
  // Isar - Base de datos local
  final dir = await getApplicationDocumentsDirectory();
  final isar = await Isar.open(
    [UserModelSchema],
    directory: dir.path,
  );
  sl.registerLazySingleton<Isar>(() => isar);

  // LocalDataSource (Isar)
  sl.registerLazySingleton<UserLocalDataSource>(
    () => UserLocalDataSourceImpl(sl()),
  );

  // Repository (solo con localDataSource)
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(
      localDataSource: sl(),
    ),
  );

  // ... resto de UseCases y Cubits
}
```

> **Diferencia clave**: El `UserRepositoryImpl` necesitaría una versión simplificada que solo use `localDataSource` sin verificar conexión a internet.

**Archivo**: `lib/core/common/usecase.dart`

```dart
import 'package:fpdart/fpdart.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/error/failures.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams extends Equatable {
  @override
  List<Object?> get props => [];
}
```

**Archivo**: `lib/core/error/failures.dart`

```dart
import 'package:equatable/equatable.dart';

abstract class Failure extends Equatable {
  final String message;
  
  const Failure(this.message);
  
  @override
  List<Object?> get props => [message];
}

class CacheFailure extends Failure {
  const CacheFailure(super.message);
}

class ServerFailure extends Failure {
  const ServerFailure(super.message);
}

class NetworkFailure extends Failure {
  const NetworkFailure(super.message);
}
```

**Archivo**: `lib/main.dart`

```dart
import 'package:flutter/material.dart';
import 'package:my_app/core/di/injection_container.dart' as di;
import 'package:my_app/features/user/presentation/pages/users_list_page.dart';

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
      title: 'Clean Architecture Demo',
      home: const UsersListPage(),
    );
  }
}
```

---
