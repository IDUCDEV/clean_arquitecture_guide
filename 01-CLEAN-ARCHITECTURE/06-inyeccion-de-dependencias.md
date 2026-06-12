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

**GetIt** es un paquete que implementa el patrón **Service Locator**.

### Conceptos clave de GetIt

| Método | Descripción | Cuándo usarlo |
|--------|-------------|---------------|
| `registerSingleton()` | Crea la instancia inmediatamente | Para objetos que deben existir desde el inicio |
| `registerLazySingleton()` | Crea la instancia la primera vez que se use | Para objetos pesados que quizás no se usen (recomendado) |
| `registerFactory()` | Crea una nueva instancia CADA vez que se pida | Para objetos que no deben compartir estado (como Cubits) |

### Implementación

**Archivo**: `lib/core/di/injection_container.dart`

```dart
import 'package:dio/dio.dart';
import 'package:get_it/get_it.dart';
import 'package:isar_community/isar_community.dart';
import 'package:internet_connection_checker/internet_connection_checker.dart';
import 'package:my_app/core/network/network_info.dart';
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
import 'package:path_provider/path_provider.dart';

final GetIt sl = GetIt.instance;

Future<void> init() async {
  // ╔════════════════════════════════════════════════════════════╗
  // ║  CAPA EXTERNA - Librerías de terceros                    ║
  // ╚════════════════════════════════════════════════════════════╝

  // Dio - Cliente HTTP
  sl.registerLazySingleton<Dio>(() {
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
  });

  // Internet Connection Checker
  sl.registerLazySingleton(() => InternetConnectionChecker());

  // NetworkInfo
  sl.registerLazySingleton<NetworkInfo>(() => NetworkInfoImpl(sl()));

  // Isar - Base de datos local (caché)
  final dir = await getApplicationDocumentsDirectory();
  final isar = await Isar.open(
    [UserModelSchema],
    directory: dir.path,
    name: 'my_app_db',
  );
  sl.registerLazySingleton<Isar>(() => isar);

  // ╔════════════════════════════════════════════════════════════╗
  // ║  CAPA DE DATOS - DataSources                             ║
  // ╚════════════════════════════════════════════════════════════╝

  // Remote DataSource (API REST)
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(client: sl()),
  );

  // Local DataSource (Caché Isar)
  sl.registerLazySingleton<UserLocalDataSource>(
    () => UserLocalDataSourceImpl(sl()),
  );

  // ╔════════════════════════════════════════════════════════════╗
  // ║  CAPA DE REPOSITORIO                                      ║
  // ╚════════════════════════════════════════════════════════════╝
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // ╔════════════════════════════════════════════════════════════╗
  // ║  CAPA DE DOMINIO - UseCases                              ║
  // ╚════════════════════════════════════════════════════════════╝
  sl.registerLazySingleton(() => GetUsers(sl()));
  sl.registerLazySingleton(() => GetUser(sl()));
  sl.registerLazySingleton(() => CreateUser(sl()));
  sl.registerLazySingleton(() => DeleteUser(sl()));

  // ╔════════════════════════════════════════════════════════════╗
  // ║  CAPA DE PRESENTACIÓN - Cubit                             ║
  // ╚════════════════════════════════════════════════════════════╝
  // registerFactory porque cada pantalla necesita su PROPIO Cubit
  sl.registerFactory(() => UserCubit(
    getUsers: sl(),
    getUser: sl(),
    createUser: sl(),
    deleteUser: sl(),
  ));
}
```

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
