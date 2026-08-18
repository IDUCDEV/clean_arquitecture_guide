# 🚀 Nivel Experto: Automatización de Inyección de Dependencias con Injectable

La Inyección de Dependencias (DI) es el pegamento que mantiene Clean Architecture unido. Sin embargo, en proyectos reales, el archivo `injection_container.dart` se convierte rápidamente en un monstruo de miles de líneas. **Injectable** resuelve esto generando código automáticamente basándose en anotaciones.

---

## 1. Fundamentos: De Manual a Automático

### 1.1 El Problema del DI Manual

Imagina un proyecto con 50+ clases que necesitan inyección:

```dart
// ❌ injection_container.dart - EL MUNDO SIN INJECTABLE

final sl = GetIt.instance;

Future<void> init() async {
  // Data Sources
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(sl()),
  );
  sl.registerLazySingleton<UserLocalDataSource>(
    () => UserLocalDataSourceImpl(sl()),
  );
  
  // Repositories
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(sl(), sl()),
  );
  
  // Use Cases
  sl.registerLazySingleton(() => GetUser(sl()));
  sl.registerLazySingleton(() => SaveUser(sl()));
  sl.registerLazySingleton(() => DeleteUser(sl()));
  
  // Cubits
  sl.registerFactory(() => UserCubit(sl(), sl(), sl()));
  
  // External
  sl.registerLazySingleton(() => http.Client());
  
  // ... 50+ más líneas similares
}
```

**Problemas:**
- Cada nuevo use case = 2+ líneas manual
- Errores solo se detectan en runtime
- Refactorizaciones = actualizaciones manuales tediosas
- Difícil de mantener en equipo

### 1.2 La Solución: Injectable

```dart
// ✅ injection_container.dart - CON INJECTABLE

final sl = GetIt.instance;

@InjectableInit()
Future<void> init() async => sl.init();

// Las anotaciones generan TODO automáticamente
```

**Beneficios:**
- Nuevas clases = solo agregar `@lazySingleton`
- Errores en tiempo de compilación
- Soporte para environments
- Testing simplificado

---

## 2. Arquitectura de Injectable

### 2.1 Cómo Funciona el Generador

```
┌─────────────────────────────────────────────────────────┐
│                    TU CÓDIGO FUENTE                     │
│  @lazySingleton                                        │
│  class AuthRepositoryImpl implements AuthRepository    │
└─────────────────────┬───────────────────────────────────┘
                      │ dart run build_runner
                      ▼
┌─────────────────────────────────────────────────────────┐
│              INJECTABLE GENERATOR                        │
│  Analiza anotaciones                                    │
│  Resuelve dependencias                                  │
│  Genera injection_container.config.dart                 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              CÓDIGO GENERADO                             │
│  sl.registerLazySingleton<AuthRepository>(...)          │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Flujo de Resolución de Dependencias

```
@LazySingleton(as: UserRepository)
class UserRepositoryImpl 
    implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  
  UserRepositoryImpl(this.remoteDataSource, this.localDataSource);
}
```

El generador:
1. Ve la anotación `@LazySingleton(as: UserRepository)`
2. Infiere que `UserRepository` es la interfaz
3. Busca constructor y ve: `UserRemoteDataSource`, `UserLocalDataSource`
4. Genera:
```dart
sl.registerLazySingleton<UserRepository>(
  () => UserRepositoryImpl(
    sl<UserRemoteDataSource>(),
    sl<UserLocalDataSource>(),
  ),
);
```

---

## 3. Configuración Completa

### 3.1 Dependencias Requeridas

```yaml
# pubspec.yaml

dependencies:
  get_it: ^7.6.4
  injectable: ^2.4.1

dev_dependencies:
  injectable_generator: ^2.6.1
  build_runner: ^2.4.8
```

### 3.2 Configuración de build.yaml

```yaml
# build.yaml - Configuración del generador

targets:
  $default:
    builders:
      injectable_generator:injectable_builder:
        options:
          # Auto-register dependencias comunes
          auto_register: true
          
          # Buscar en estos directorios
          root_directory:
            path: lib
            generate_on: false
          
          # Imports que agregar automáticamente
          imports:
            - package:http/http.dart
            - package:shared_preferences/shared_preferences.dart
          
          # Options de configuración
          synthetic_package: false
          relative_paths: true
```

### 3.3 Estructura de Carpetas Recomendada

```
lib/
├── core/
│   ├── di/
│   │   ├── injection_container.dart      # Entry point
│   │   ├── injection_container.config.dart  # GENERADO
│   │   ├── modules/
│   │   │   ├── external_module.dart      # Librerías externas
│   │   │   ├── database_module.dart      # DB connections
│   │   │   └── network_module.dart       # HTTP clients
│   │   └── environments/
│   │       ├── dev.env                   # Config dev
│   │       └── prod.env                  # Config prod
```

---

## 4. Anotaciones en Profundidad

### 4.1 Tipos de Scopes

| Anotación | Descripción | Cuándo Usar |
|-----------|-------------|--------------|
| `@lazySingleton` | Una sola instancia, creada lazily | Repos, DataSources, UseCases |
| `@singleton` | Una sola instancia, creada inmediatamente | Config, AuthService |
| `@injectable` | Nueva instancia cada vez | Cubits, BLoCs, Presenters |
| `@factory` | Alias de `@injectable` | Mismo propósito |

### 4.2 Anotaciones de Clase

```dart
// DataSource - típicamente singleton
@lazySingleton
class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final http.Client client;
  UserRemoteDataSourceImpl(this.client);
}
```

```dart
// Repository con interfaz
@LazySingleton(as: UserRepository)
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;
  UserRepositoryImpl(this.remoteDataSource, this.localDataSource);
}
```

```dart
// UseCase - siempre singleton
@lazySingleton
class GetUser extends UseCase<User, String> {
  final UserRepository repository;
  GetUser(this.repository);
}
```

```dart
// Cubit/Bloc - factory (nueva instancia por inyección)
@injectable
class UserCubit extends Cubit<UserState> {
  final GetUser getUser;
  UserCubit(this.getUser) : super(UserInitial());
}
```

```dart
// Screen/Widget - factory también
@injectable  
class UserScreen extends StatelessWidget {
  final UserCubit cubit;
  UserScreen(this.cubit);
}
```

### 4.3 Parámetros de Constructor

A veces necesitas pasar valores que no son injectables:

```dart
@lazySingleton
class FetchUsers {
  final UserRepository repository;
  
  FetchUsers(this.repository); // Solo el repository es inyectado
  
  Future<void> execute({int page = 1}) async { ... }
}
```

```dart
@injectable
class UserListCubit extends Cubit<UserListState> {
  final FetchUsers fetchUsers;
  
  UserListCubit(this.fetchUsers); // Injectable + parámetros opcionales
  
  void loadPage(int page) => fetchUsers.execute(page: page);
}
```

---

## 5. Módulos: Inyectando Librerías Externas

### 5.1 Por Qué Son Necesarios

Librerías como `http`, `shared_preferences`, `firebase` no tienen anotaciones. Los módulos le dicen a Injectable cómo crear estas instancias.

### 5.2 Módulo Básico

```dart
// lib/core/di/modules/external_module.dart

import 'package:http/http.dart' as http;
import 'package:injectable/injectable.dart';

@module
abstract class ExternalModule {
  // Inyección simple
  @lazySingleton
  http.Client get httpClient => http.Client();
  
  // Con configuración
  @lazySingleton
  http.Client get authenticatedClient {
    final client = http.Client();
    client.headers['Authorization'] = 'Bearer token';
    return client;
  }
}
```

### 5.3 Módulo Asíncrono con @preResolve

Para dependencias que necesitan `await` (SharedPreferences, Firebase, Database):

```dart
// lib/core/di/modules/preferences_module.dart

import 'package:injectable/injectable.dart';
import 'package:shared_preferences/shared_preferences.dart';

@module
abstract class PreferencesModule {
  // IMPORTANTE: Debe ser top-level function, no arrow function
  @preResolve
  Future<SharedPreferences> get sharedPreferences {
    return SharedPreferences.getInstance();
  }
}
```

**Uso:**

```dart
Future<void> main() async {
  await init(); // sl.init() espera a que @preResolve termine
  runApp(MyApp());
}
```

### 5.4 Módulos con Configuración

```dart
// lib/core/di/modules/config_module.dart

import 'package:injectable/injectable.dart';
import 'package:flutter/foundation.dart';
import 'package:firebase_core/firebase_core.dart' as firebase;

@module
abstract class ConfigModule {
  @lazySingleton
  String get apiBaseUrl {
    if (kDebugMode) return 'https://dev.api.com';
    return 'https://api.com';
  }
  
  @preResolve
  @lazySingleton
  Future<firebase.FirebaseOptions> get firebaseOptions {
    if (kDebugMode) {
      return firebase.FirebaseOptions(
        apiKey: 'dev_key',
        projectId: 'dev-project',
      );
    }
    return firebase.FirebaseOptions(
      apiKey: 'prod_key',
      projectId: 'prod-project',
    );
  }
}
```

---

## 6. Environments: Desarrollo vs Producción

### 6.1 Configuración de Environments

```dart
// lib/core/di/injection_container.dart

@InjectableInit(
  initializerName: 'init', // nombre de la función
  preferRelativeImports: true,
  asExtension: true, // sl.init() en lugar de init(sl)
)
void configureDependencies({required String environment}) {}
```

### 6.2 Environments en Clases

```dart
// Solo registrar en desarrollo
@lazySingleton
@Environment(Environment.dev)
class DevToolsService {
  DevToolsService();
}

// Solo registrar en producción
@lazySingleton  
@Environment(Environment.prod)
class AnalyticsService {
  AnalyticsService();
}

// Registrar en ambos
@lazySingleton
@Environment(['dev', 'prod'])
class UserService {
  UserService();
}
```

### 6.3 Environments con Módulos

```dart
@module
@Environment(Environment.dev)
abstract class DevModule {
  @lazySingleton
  String get apiUrl => 'http://localhost:8080';
}

@module
@Environment(Environment.prod)
abstract class ProdModule {
  @lazySingleton
  String get apiUrl => 'https://api.production.com';
}
```

### 6.4 Inicialización con Environment

```dart
Future<void> main() async {
  const env = String.fromEnvironment('ENV', defaultValue: 'dev');
  
  await init(environment: env);
  
  runApp(MyApp());
}
```

```bash
# Run en desarrollo
flutter run --dart-define=ENV=dev

# Run en producción
flutter run --dart-define=ENV=prod
```

---

## 7. Errores Comunes y Debugging

### Error 1: Dependencia Circular

```
Error: Generator cannot resolve dependency for 'UserRepository'
→ 'UserRepository' depends on 'UserRepository'
```

**Solución:** Una de las clases debe usar `@lazySingleton` vs `@injectable` para romper el ciclo, o refactorizar.

### Error 2: No Encontrar la Interfaz

```
Error: No generator registered for 'UserRepository'
→ Make sure you have @LazySingleton(as: UserRepository)
```

**Solución:** Asegúrate de usar `as:` para indicar la interfaz.

### Error 3: Constructor Privado

```
Error: Cannot instantiate UserRepository
→ Constructor must be public for injection
```

**Solución:** Constructor debe ser `const UserRepositoryImpl()` o al menos público.

### Error 4: Módulo No Generado

```
Error: Expected a type name for 'ExternalModule'
→ Make sure you have @module annotation
```

**Solución:** Asegúrate de que el módulo es `abstract class`.

---

## 8. Testing con Injectable

### 8.1 Reemplazando Dependencias en Tests

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:injectable/injectable.dart';

void main() {
  setUpAll(() {
    // Resetear GetIt
    get.reset();
    
    // Registrar mocks
    get.registerLazySingleton<UserRepository>(
      () => MockUserRepository(),
    );
  });
  
  test('getUser returns user', () async {
    final useCase = get<GetUser>();
    final result = await useCase('1');
    
    expect(result.isRight(), true);
  });
}
```

### 8.2 Testing con Environment

```dart
void main() {
  setUpAll(() {
    // Inicializar con environment de test
    init(environment: Environment.test);
  });
}
```

### 8.3 Módulo de Test

```dart
@module
@Environment(Environment.test)
abstract class TestModule {
  @lazySingleton
  @override
  http.Client get httpClient => MockClient();
}
```

### 8.4 Testing de Integración Completo

Cuando necesitas testear la inyección completa:

```dart
// test/injection_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:injectable/injectable.dart';
import 'package:my_app/injection_container.dart' as di;

void main() {
  setUpAll(() async {
    // Inicializar con environment de test
    await di.init(environment: Environment.test);
  });

  tearDownAll(() {
    // Limpiar después de todos los tests
    di.sl.reset();
  });

  group('Dependency Injection', () {
    test('debería resolver UserRepository', () {
      final repo = di.sl<UserRepository>();
      expect(repo, isNotNull);
    });

    test('debería resolver GetUser UseCase', () {
      final useCase = di.sl<GetUser>();
      expect(useCase, isNotNull);
    });

    test('debería resolver UserCubit como factory (nueva instancia)', () {
      final cubit1 = di.sl<UserCubit>();
      final cubit2 = di.sl<UserCubit>();
      
      // Factory crea nuevas instancias
      expect(cubit1, isNot(same(cubit2)));
    });

    test('debería resolver UserRepository como singleton (misma instancia)', () {
      final repo1 = di.sl<UserRepository>();
      final repo2 = di.sl<UserRepository>();
      
      // Singleton usa la misma instancia
      expect(identical(repo1, repo2), true);
    });
  });
}
```

### 8.5 Reemplazo Dinámico de Dependencias

Para tests específicos sin modificar el código de producción:

```dart
void main() {
  group('UserRepository Tests', () {
    setUp(() {
      // Resetear y registrar mocks ANTES de cada test
      di.sl.reset();
      
      // Registrar mock
      di.sl.registerLazySingleton<UserRemoteDataSource>(
        () => MockUserRemoteDataSource(),
      );
      
      // Registrar implementación real del repositorio
      di.sl.registerLazySingleton<UserRepository>(
        () => UserRepositoryImpl(di.sl()),
      );
    });

    test('getUser usa el mock', () async {
      final mockDataSource = di.sl<UserRemoteDataSource>() as MockUserRemoteDataSource;
      when(() => mockDataSource.getUser('1'))
          .thenAnswer((_) async => UserModel(id: '1', name: 'Mocked'));
      
      final repo = di.sl<UserRepository>();
      final result = await repo.getUser('1');
      
      expect(result.isRight(), true);
      verify(() => mockDataSource.getUser('1')).called(1);
    });

    tearDown(() {
      di.sl.reset();
    });
  });
}
```

### 8.6 Testing con Múltiples Environments

```dart
void main() {
  group('Environment Tests', () {
    test('dev environment tiene API correcta', () async {
      await di.init(environment: Environment.dev);
      
      final config = di.sl<AppConfig>();
      expect(config.apiUrl, 'https://dev.api.com');
      
      di.sl.reset();
    });

    test('prod environment tiene API correcta', () async {
      await di.init(environment: Environment.prod);
      
      final config = di.sl<AppConfig>();
      expect(config.apiUrl, 'https://api.production.com');
      
      di.sl.reset();
    });

    test('test environment usa mocks', () async {
      await di.init(environment: Environment.test);
      
      // En test, API debería ser mock
      final httpClient = di.sl<http.Client>();
      expect(httpClient, isA<MockClient>());
      
      di.sl.reset();
    });
  });
}
```

### 8.7 Mocks con mocktail

```yaml
# pubspec.yaml (dev)
dev_dependencies:
  mocktail: ^1.0.3
```

```dart
// test/mocks/mocktail_mocks.dart

import 'package:mocktail/mocktail.dart';
import 'package:my_app/features/users/data/datasources/user_remote_datasource.dart';
import 'package:my_app/features/users/domain/repositories/user_repository.dart';

class MockUserRemoteDataSource extends Mock implements UserRemoteDataSource {}

class MockUserRepository extends Mock implements UserRepository {}

// Registrar fallback values para mocktail
class FakeUserParams extends Fake implements UserParams {}

void main() {
  setUpAll(() {
    registerFallbackValue(FakeUserParams());
  });
}
```

### 8.8 Testing de UseCase con GetIt

```dart
// test/features/users/domain/usecases/get_user_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/features/users/domain/repositories/user_repository.dart';
import 'package:my_app/features/users/domain/usecases/get_user.dart';
import 'package:injectable/injectable.dart';
import 'package:my_app/injection_container.dart' as di;

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late GetUser useCase;
  late MockUserRepository mockRepository;

  setUp(() async {
    // Inicializar DI
    await di.init(environment: Environment.test);
    
    // Reemplazar dependencia real con mock
    mockRepository = MockUserRepository();
    di.sl.registerLazySingleton<UserRepository>(() => mockRepository);
    
    // Obtener UseCase ya inyectado
    useCase = di.sl<GetUser>();
  });

  setUpAll(() {
    registerFallbackValue(const GetUserParams('test'));
  });

  tearDown(() {
    di.sl.reset();
  });

  test('debería retornar usuario del repository', () async {
    // Arrange
    const user = User(id: '1', name: 'Test');
    when(() => mockRepository.getUser(any()))
        .thenAnswer((_) async => const Right(user));

    // Act
    final result = await useCase(const GetUserParams('1'));

    // Assert
    expect(result, const Right(user));
    verify(() => mockRepository.getUser('1')).called(1);
  });
}
```

### 8.9 Testing de Cubit con GetIt

```dart
// test/features/users/presentation/cubit/user_cubit_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/features/users/domain/usecases/get_user.dart';
import 'package:my_app/features/users/presentation/cubit/user_cubit.dart';
import 'package:injectable/injectable.dart';
import 'package:my_app/injection_container.dart' as di;

class MockGetUser extends Mock implements GetUser {}

void main() {
  late MockGetUser mockGetUser;

  setUp(() async {
    await di.init(environment: Environment.test);
    mockGetUser = MockGetUser();
    
    // Reemplazar GetUse con mock
    di.sl.registerLazySingleton<GetUser>(() => mockGetUser);
  });

  setUpAll(() {
    registerFallbackValue(const GetUserParams('test'));
  });

  tearDown(() {
    di.sl.reset();
  });

  blocTest<UserCubit, UserState>(
    'debería emitir [Loading, Loaded] cuando getUser succeeds',
    setUp: () {
      when(() => mockGetUser(any()))
          .thenAnswer((_) async => const Right(User(id: '1', name: 'Test')));
    },
    build: () => di.sl<UserCubit>(),
    act: (cubit) => cubit.loadUser('1'),
    expect: () => [
      UserLoading(),
      const UserLoaded(User(id: '1', name: 'Test')),
    ],
  );

  blocTest<UserCubit, UserState>(
    'debería emitir [Loading, Error] cuando getUser fails',
    setUp: () {
      when(() => mockGetUser(any()))
          .thenAnswer((_) async => const Left(ServerFailure('Error')));
    },
    build: () => di.sl<UserCubit>(),
    act: (cubit) => cubit.loadUser('1'),
    expect: () => [
      UserLoading(),
      const UserError('Error'),
    ],
  );
}
```

### 8.10 Errores Comunes en Testing con Injectable

```dart
// ❌ Error 1: Olvidar reset()
void testSinReset() {
  // CRASH: Instance already exists
}

// ✅ Solución
void testConReset() {
  di.sl.reset();
  // Ahora puedes registrar nuevas dependencias
}

// ❌ Error 2: No registrar fallback value
setUp(() {
  // CRASH: MissingStubError
  when(() => mockRepo.getUser(any())).thenAnswer(...);
});

// ✅ Solución
setUpAll(() {
  registerFallbackValue(UserParams('fallback'));
});

// ❌ Error 3: Environment incorrecto
void testWrongEnv() {
  await di.init(environment: Environment.prod); // Usa config de prod
  // CRASH: Test mocks no están registrados
}

// ✅ Solución
void testCorrectEnv() {
  await di.init(environment: Environment.test);
  // Mocks registrados correctamente
}

// ❌ Error 4: No cerrar StreamController en Cubit
@override
Future<void> close() {
  _controller.close(); // Olvidar en producción → leak en test
  return super.close();
}

// ✅ Solución: Siempre cerrar
@override
Future<void> close() {
  _controller.close();
  return super.close();
}
```

### 8.11 Estructura de Tests con Injectable

```
test/
├── core/
│   └── di/
│       └── injection_test.dart           # Tests de DI
├── features/
│   ├── users/
│   │   ├── domain/
│   │   │   └── usecases/
│   │   │       └── get_user_test.dart    # Tests de UseCase
│   │   └── presentation/
│   │       └── cubit/
│   │           └── user_cubit_test.dart  # Tests de Cubit
│   └── products/
│       └── ...
├── mocks/
│   ├── mocktail_mocks.dart               #Mocks globales
│   └── fixtures/
│       └── user_fixture.dart             # Datos de prueba
└── helpers/
    └── test_helpers.dart                 # Utils para tests
```

### 8.12 Configuración de test_config.dart

```dart
// lib/core/di/test_config.dart

import 'package:injectable/injectable.dart';
import 'package:my_app/injection_container.dart' as di;

@module
@Environment(Environment.test)
abstract class TestConfigModule {
  @lazySingleton
  @override
  http.Client get httpClient => MockClient();

  @lazySingleton
  @override
  SharedPreferences get sharedPreferences => MockSharedPreferences();
}

Future<void> setupTestDependencies() async {
  await di.init(environment: Environment.test);
}

void tearDownTestDependencies() {
  di.sl.reset();
}
```

---

## 9. Casos Avanzados

### 9.1 Inyectar Instancia Existente

```dart
@module
abstract class ExistingModule {
  // Registrar una instancia ya creada
  @lazySingleton
  @override
  UserRepository get userRepository => existingUserRepository;
}
```

### 9.2 Named Instances

```dart
// Diferentes implementaciones para mismo tipo
@Named('http')
@lazySingleton
http.Client httpClient() => http.Client();

@Named('http_dio')
@lazySingleton
http.Client dioClient() => Dio();

// Uso
class ApiService {
  final http.Client client;
  
  // Inject by name
  ApiService(@Named('http_dio') this.client);
}
```

### 9.3 Qualifiers Personalizados

```dart
@Qualifier(value: 'cache')
class CacheQualifier {}

@lazySingleton
@CacheQualifier
class CacheService {}

// Uso
class SomeService {
  final CacheService cache;
  
  SomeService(@CacheQualifier this.cache);
}
```

---

## 10. Mejores Prácticas

### 10.1 Estructura de Módulos

```
lib/core/di/
├── injection_container.dart       # Entry point
├── modules/
│   ├── external_module.dart       # http, shared_preferences
│   ├── database_module.dart      # SQLite, Hive, Isar
│   ├── firebase_module.dart      # Firebase services
│   └── config_module.dart        # App config
└── repositories/
    └── repositories_module.dart  # Repository bindings
```

### 10.2 Reglas de Oro

1. **Usa `@lazySingleton` para UseCases, Repos, DataSources** - Son stateless y reutilizables
2. **Usa `@injectable` para Cubits/BLoCs** - Cada screen necesita su propia instancia
3. **Un módulo por tipo de dependencia** - Separa concerns
4. **Ejecuta `build_runner` después de cada cambio** - No te olvides
5. **Revisa el código generado** - Asegúrate de que se ve correcto

### 10.3 Orden de Inicialización

```dart
@InjectableInit(
  initializerName: 'init',
  // Ejecutar en orden específico
  moduleName: 'CoreModule',
)
void configureDependencies() {}

// El orden en injection_container.dart importa
@InjectableInit(
  modules: [
    ExternalModule(),      // 1. Primero: dependencias externas
    DatabaseModule(),     // 2. Segundo: bases de datos
    RepositoryModule(),   // 3. Tercero: repos
    UseCaseModule(),     // 4. Cuarto: casos de uso
    CubitModule(),       // 5. Último: presentation
  ],
)
Future<void> configureDependencies() async {}
```

---

## 11. Integración con Riverpod (Bonus)

Si usas Riverpod además de Clean Architecture:

```dart
// Provider que usa GetIt
final userRepositoryProvider = Provider<UserRepository>(
  (ref) => getIt<UserRepository>(),
);
```

---

## 12. Recetas Rápidas

### Agregar Nueva Feature

1. Crear UseCase con `@lazySingleton`
2. Crear Repository con `@LazySingleton(as: Interface)`
3. Crear Cubit con `@injectable`
4. Ejecutar: `dart run build_runner build --delete-conflicting-outputs`
5. Listo ✅

### Agregar Nueva Dependencia Externa

1. Crear nuevo módulo o agregar a `ExternalModule`
2. Agregar getter con `@lazySingleton`
3. Ejecutar generador

### Cambiar Scope de una Clase

```dart
// Cambiar de singleton a factory
@injectable  // Era @lazySingleton
class MyClass {}
```

---

## Resumen Ejecutivo

1. **Injectable + GetIt** es el estándar de DI en Flutter moderno
2. Las **anotaciones** (`@lazySingleton`, `@injectable`, `@module`) generan código automáticamente
3. **Environments** permiten diferentes configuraciones para dev/prod
4. **Módulos** son esenciales para librerías externas
5. **Testing** se simplifica con posibilidad de reemplazar dependencias
6. **Errores comunes** son principalmente dependencias circulares y falta de generador

**Siguiente nivel:** Aprende a combinar Injectable con `freezed` y `json_serializable` para un pipeline completo de generación de código.

---

## Recursos Adicionales

- [Documentación oficial Injectable](https://pub.dev/packages/injectable)
- [Ejemplos de Injectable](https://github.com/NicholasAnnesley/injectable_examples)
- [Talk: Dependency Injection Done Right](https://www.youtube.com/watch?v=...)

---

## Ver también

- [`14-LOADED`](../14-LOADED/README.md) — Patrón Loaded con dependencias y estado inicial
- [`17-CLEAN-ARCHITECTURE`](../17-CLEAN-ARCHITECTURE/README.md) — Arquitectura limpia y separación de capas

---

## En el siguiente módulo

**→ [03-comunicacion-features.md](./03-comunicacion-features.md)** — Comunicación entre features con Event Bus
