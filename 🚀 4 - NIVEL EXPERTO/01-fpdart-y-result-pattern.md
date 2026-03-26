# 🚀 Nivel Experto: Programación Funcional con fpdart y Result Pattern

La Programación Funcional (PF) no es solo una moda: es una filosofía que te obliga a **modelar el fallo como parte del dominio**. En aplicaciones modernas donde la red es inestable, los APIs cambian, y los usuarios esperan experiencias fluidas, manejar errores explícitamente no es opcional — es arquitectura.

---

## 1. Fundamentos: ¿Por qué Programación Funcional en Dart?

Dart ya tiene null safety, pero eso solo resuelve el problema de "valor ausente". No resuelve el problema de "operación fallida". Cuando llamas a una API, existen tres estados:

1. **Éxito**: Tienes un resultado válido
2. **Error de dominio**: La operación falló por una regla de negocio (ej: "saldo insuficiente")
3. **Error técnico**: La red cayó, el servidor respondió 500, timeout

La PF te obliga a modelar estos tres estados de forma **exhaustiva**. El compilador te obliga a manejar cada caso. No hay `try-catch` olvidados, no hay `null` inesperado.

### El Problema con try-catch tradicional

```dart
// ❌ Enfoque tradicional: excepciones como control flow
Future<User> getUser() async {
  try {
    final response = await api.get('/user');
    return User.fromJson(response);
  } catch (e) {
    // ¿Qué tipo de error? ¿Red? ¿Parseo? ¿Servidor?
    throw Exception('Error: $e'); // Información perdida
  }
}
```

### El Enfoque Funcional

```dart
// ✅ Enfoque funcional: el tipo dice TODO
Future<Either<Failure, User>> getUser() async {
  // Either<Left(Error), Right(Success)>
  // Left traditionally contiene el error
  // Right traditionally contiene el éxito
}
```

**La firma del método te dice todo lo que necesitas saber**: puede fallar, y el fallo tiene un tipo concreto (`Failure`).

---

## 2. Dartz vs fpdart: La Evolución del Ecosistema

Históricamente, `dartz` fue la librería estándar para FP en Dart. Sin embargo, el ecosistema ha evolucionado y `fpdart` se ha convertido en la elección moderna.

### Comparativa Técnica

| Aspecto | dartz | fpdart |
|---------|-------|--------|
| **Mantenimiento** | Abandonado desde 2021 | Activo (última versión 2024) |
| **Sintaxis** | Estilo Haskell puro | Idioms de Dart modernos |
| **Integración Null Safety** | Incompleta | Total |
| **Extensiones de IDE** | Pocas | Excelentes (tipos bien definidos) |
| **Tamaño bundle** | ~200KB | ~150KB (tree shaking) |
| **Documentación** | Escasa | Completa con ejemplos |
| **API de Streams** | Básica | Avanzada (parses, validations) |

### Ejemplo Práctico: Transformación de Datos

**Con dartz:**
```dart
import 'package:dartz/dartz.dart';

Either<Failure, int> result = Right(10);
final mapped = result.map((r) => r * 2);
// works, pero las extensiones son limitadas
```

**Con fpdart:**
```dart
import 'package:fpdart/fpdart.dart';

Either<Failure, int> result = Right(10);

// map: transformar el valor contenido
final mapped = result.map((r) => r * 2); // Right(20)

// flatMap: encadenar operaciones que retornan Either
final chained = result.flatMap((r) => Right(r * 2));

// getOrElse: obtener valor con fallback
final value = result.getOrElse(() => 0); // 10

// fold: procesar ambos casos
result.match(
  (failure) => print('Error: $failure'),
  (value) => print('Valor: $value'),
);

// match: igual que fold pero más conciso (alias)
result.match(
  (failure) => print('Error: $failure'),
  (value) => print('Valor: $value'),
);
```

---

## 3. Either: El Corazón de la Gestión de Errores

### 3.1 La Semántica de Left y Right

Existe una convención en FP:
- **Left**: Representa el valor "incorrecto" o error
- **Right**: Representa el valor "correcto" o éxito

```dart
// Convenciones en fpdart
Right<String, int>(42)  // ✅ Éxito: el int 42
Left<String, int>('error')  // ❌ Fallo: el string 'error'
```

### 3.2 Creación de Either

```dart
// Constructor directo
Right<Failure, User>(user);
Left<Failure, User>(ServerFailure('500'));

// From nullable (convierte null a Failure)
Either<Failure, User> fromNullable(
  User? user, 
  Failure Function() ifNull,
) => user != null ? Right(user) : Left(ifNull());

// From Future (convierte Future a Either)
Future<Either<Failure, User>> fromPromise(
  Future<User> promise,
  Failure Function(Object error) onError,
) async {
  try {
    return Right(await promise);
  } catch (e) {
    return Left(onError(e));
  }
}
```

---

## 4. Option/Maybe: El Homólogo de Null Safety

En países donde null safety no existe (Dart pre-2.12), `Option` era esencial. Hoy, tiene un propósito diferente: representar **ausencia intencional de valor** que no es un error.

### Cuándo usar Option vs Null

| Escenario | Solución |
|-----------|----------|
| Usuario no ha iniciado sesión | `User? user = null` (natural) |
| Búsqueda no encontró resultados | `Option<User> user` (ausencia intencional) |
| Configuración opcional | `Option<Theme> theme` |
| Campo que puede no existir en JSON | `int? age` (null safety nativo) |

### Ejemplo con Option

```dart
import 'package:fpdart/fpdart.dart';

Option<int> findUserId(String email) {
  final users = [{'email': 'a@test.com', 'id': 1}];
  
  final found = users.firstWhere(
    (u) => u['email'] == email,
    orElse: () => {},
  );
  
  // Map a Option: si no existe, None
  return found.isEmpty 
    ? const None() 
    : Option<int>.fromNullable(found['id']);
}

// Uso
findUserId('a@test.com').match(
  () => print('No encontrado'),  // None
  (id) => print('ID: $id'),     // Some(id)
);
```

---

## 5. Task y TaskEither: Asincronía Funcional

### 5.1 El Problema con Future

`Future` no tiene contexto de error tipado. Además, no puedes componerlas fácilmente:

```dart
// ❌ Future: composición difícil
Future<User> getUser() async {
  final token = await getToken(); // puede fallar silenciosamente
  final user = await api.getUser(token);
  return user;
}
```

### 5.2 Task: Future con Contexto

`Task<A>` es un wrapper alrededor de `Future<A>` que permite composición:

```dart
import 'package:fpdart/fpdart.dart';

// Task<A> = () -> Future<A>
// Es una función perezosa que cuando la ejecutas retorna un Future

Task<User> getUserTask = Task(() async {
  final token = await getToken();
  return await api.getUser(token);
});

// Ejecutar cuando quieras
Future<User> user = getUserTask.run();
```

### 5.3 TaskEither: El Poder Combinado

`TaskEither<Failure, A>` = `Task<Either<Failure, A>>`

Esto es **transformador de efectos**: manejar asincronía Y errores tipados en una sola estructura.

```dart
TaskEither<Failure, User> getUserTask(String id) {
  return TaskEither.tryCatch(
    () => api.getUser(id),
    (error, stackTrace) => ServerFailure(error.toString()),
  );
}

// Encadenar operaciones (no hay try-catch en ninguna parte)
final result = await getUserTask('123')
  .map((user) => user.name.toUpperCase())
  .flatMap((name) => TaskEither.of(Greeting(name)))
  .run();
```

### Ejemplo Completo: Repository con TaskEither

```dart
abstract class UserRepository {
  TaskEither<Failure, User> getUser(String id);
  TaskEither<Failure, List<User>> getUsers();
}

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;

  UserRepositoryImpl(this.remoteDataSource);

  @override
  TaskEither<Failure, User> getUser(String id) {
    return TaskEither.tryCatch(
      () => remoteDataSource.getUser(id),
      (error, stackTrace) {
        if (error is SocketException) {
          return NetworkFailure('Sin conexión');
        }
        if (error is TimeoutException) {
          return NetworkFailure('Tiempo de espera agotado');
        }
        return ServerFailure(error.toString());
      },
    );
  }

  @override
  TaskEither<Failure, List<User>> getUsers() {
    return TaskEither.tryCatch(
      () => remoteDataSource.getUsers(),
      (error, stackTrace) => ServerFailure(error.toString()),
    ).map((users) => users.where((u) => u.isActive).toList());
  }
}
```

---

## 6. El Result Pattern (Sin Dependencias)

Si quieres un **Domain puro** sin librerías externas, Dart 3+ con Sealed Classes es suficiente.

### 6.1 Implementación Básica

```dart
// lib/core/error/result.dart

sealed class Result<S, E> {
  const Result();
}

final class Success<S, E> extends Result<S, E> {
  final S value;
  const Success(this.value);
}

final class Failure<S, E> extends Result<S, E> {
  final E error;
  const Failure(this.error);
}
```

### 6.2 Extensiones de Utilidad

```dart
extension ResultExtension<S, E> on Result<S, E> {
  bool get isSuccess => this is Success<S, E>;
  bool get isFailure => this is Failure<S, E>;

  S getOrThrow() {
    return switch (this) {
      Success(value: final v) => v,
      Failure(error: final e) => throw Exception('Unexpected failure: $e'),
    };
  }

  S getOrElse(S defaultValue) {
    return switch (this) {
      Success(value: final v) => v,
      Failure() => defaultValue,
    };
  }

  Result<R, E> map<R>(R Function(S) f) {
    return switch (this) {
      Success(value: final v) => Success(f(v)),
      Failure(error: final e) => Failure(e),
    };
  }

  Result<S, R> mapError<R>(R Function(E) f) {
    return switch (this) {
      Success(value: final v) => Success(v),
      Failure(error: final e) => Failure(f(e)),
    };
  }

  Future<Result<R, E>> mapFuture<R>(Future<R> Function(S) f) async {
    return switch (this) {
      Success(value: final v) => Success(await f(v)),
      Failure(error: final e) => Failure(e),
    };
  }
}
```

### 6.3 Uso Exhaustive (El Poder del Compilador)

```dart
Future<Result<User, Failure>> getUser(String id) async { ... }

void handle() {
  final result = await getUser('123');
  
  // El compilador fuerza manejar TODOS los casos
  switch (result) {
    case Success(value: final user):
      print('Usuario: ${user.name}');
    case Failure(error: final err):
      print('Error: ${err.message}');
      // Posiblemente reintentar, mostrar UI, etc.
  }
}
```

---

## 7. Fallback Chains: Operadores de Rescue

A veces quieres intentar una operación, y si falla, intentar otra. Esto se llama "fallback chain" o "rescue".

### Con Either

```dart
// Intentar API primaria, luego secundaria
Future<Either<Failure, Data>> getData() async {
  final primary = await primarySource.getData();
  
  return primary.match(
    (failure) async {
      // Fallback: intentar fuente secundaria
      final secondary = await secondarySource.getData();
      return secondary.match(
        (e) => Failure('Both failed: $e'),  // Todas las opciones agotadas
        (data) => Right(data),
      );
    },
    (data) => Right(data),
  );
}
```

### Con fpdart: pipe y chain

```dart
// Usando extension methods
final result = await primarySource.getData()
  .orElse(() => secondarySource.getData())
  .orElse(() => cachedSource.getData())
  .run();
```

---

## 8. Errores Comunes y Cómo Evitarlos

### Error 1: map vs flatMap

```dart
Either<Failure, int> divide(int a, int b) {
  if (b == 0) return Left(DivisionFailure());
  return Right(a ~/ b);
}

// ❌ map cuando necesitas retornar Either
final result = divide(10, 2).map((r) => divide(r, 2));
// Error: flatMap needed! map expects (int) -> int, not (int) -> Either

// ✅ flatMap para encadenar operaciones que pueden fallar
final result = divide(10, 2).flatMap((r) => divide(r, 2));
```

### Error 2: Pérdida de Tipos en fold

```dart
// ❌ fold sin especificar tipos puede perder типы
result.match(
  (e) => print(e),  // e puede ser Any
  (v) => print(v),  // v puede ser Any
);

// ✅ Especifica los tipos
result.fold<Widget>(
  (failure) => ErrorWidget(failure.message),
  (user) => UserWidget(user),
);
```

### Error 3: Olvidar ejecutar TaskEither

```dart
// ❌ Crear pero no ejecutar
final task = getUserTask('123');
// ERROR: task es TaskEither, no User!

// ✅ Ejecutar con .run()
final result = await getUserTask('123').run();
```

---

## 9. Integración Completa: Clean Architecture con fpdart

### Domain Layer: UseCase

```dart
// lib/features/users/domain/usecases/get_user.dart

@lazySingleton
class GetUser extends UseCase<User, GetUserParams> {
  final UserRepository repository;

  GetUser(this.repository);

  @override
  Future<Either<Failure, User>> call(GetUserParams params) async {
    return repository.getUser(params.id);
  }
}

class GetUserParams {
  final String id;
  const GetUserParams(this.id);
}
```

### Data Layer: Repository Implementation

```dart
// lib/features/users/data/repositories/user_repository_impl.dart

@LazySingleton(as: UserRepository)
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;

  UserRepositoryImpl(this.remoteDataSource, this.localDataSource);

  @override
  Future<Either<Failure, User>> getUser(String id) async {
    return TaskEither.tryCatch(
      () => remoteDataSource.getUser(id),
      (error, stackTrace) {
        if (error is SocketException) {
          return NetworkFailure('Sin conexión a internet');
        }
        if (error is UnauthorizedException) {
          return AuthFailure('Sesión expirada');
        }
        return ServerFailure(error.toString());
      },
    ).flatMap((user) {
      return TaskEither.tryCatch(
        () => localDataSource.cacheUser(user),
        (_, __) => CacheFailure('Error guardando en cache'),
      );
    }).run();
  }
}
```

### Presentation Layer: Cubit

```dart
// lib/features/users/presentation/cubit/user_cubit.dart

@injectable
class UserCubit extends Cubit<UserState> {
  final GetUser getUser;

  UserCubit(this.getUser) : super(UserInitial());

  Future<void> loadUser(String id) async {
    emit(UserLoading());

    final result = await getUser(GetUserParams(id));

    result.match(
      (failure) => emit(UserError(failure.message)),
      (user) => emit(UserLoaded(user)),
    );
  }
}
```

---

## 10. Comparativa: ¿Cuándo Usar Qué?

| Escenario | Herramienta Recomendada |
|-----------|------------------------|
| Proyecto nuevo, mediano-grande | **fpdart** (TaskEither) |
| Proyecto pequeño, quiere mínimo código | **Result Pattern** (Sealed Classes) |
| Equipo sin experiencia en FP | **Result Pattern** |
| Necesitas transformar muchos datos | **fpdart** (extensiones ricas) |
| Firebase/API con много errores | **fpdart** (TaskEither composition) |
| Solo necesitas Either básico | **dartz** (si ya lo tienes) |

---

## 11. Recomendaciones de Rendimiento

### Tree Shaking

fpdart está diseñado para tree shaking:

```yaml
# pubspec.yaml - asegurate de no importar todo
dependencies:
  fpdart: ^1.2.0
  # No importes package:fpdart/fpdart.dart
  # Mejor: import solo lo que necesitas
```

### Bundle Size Impact

| Librería | Tamaño Minificado |
|----------|-------------------|
| dartz | ~180 KB |
| fpdart | ~120 KB |
| freezed + json_serializable | ~250 KB |

---

## 12. Recetas Rápidas

### Validación de Input con Either

```dart
Either<ValidationFailure, User> validateUser(String name, String email) {
  if (name.isEmpty) {
    return Left(ValidationFailure('Nombre requerido'));
  }
  if (!email.contains('@')) {
    return Left(ValidationFailure('Email inválido'));
  }
  return Right(User(name, email));
}
```

### Reintentos con TaskEither

```dart
TaskEither<Failure, T> withRetry(
  TaskEither<Failure, T> task, {
  int maxRetries = 3,
}) {
  return task.orElse((failure) {
    // Lógica de retry
    return withRetry(task, maxRetries: maxRetries - 1);
  });
}
```

### Timeout

```dart
TaskEither<Failure, T> withTimeout(
  TaskEither<Failure, T> task, {
  Duration timeout = const Duration(seconds: 10),
}) {
  return TaskEither.tryCatch(
    () => task.run().timeout(timeout),
    (error, _) => TimeoutFailure(),
  );
}
```

---

## 13. Testing con fpdart y Result Pattern

El testing es donde FP brilla: los tipos explícitos hacen que los tests sean más predecibles y los mocks más controlados.

### 13.1 Configuración de Testing

```yaml
# pubspec.yaml (dev)
dev_dependencies:
  mocktail: ^1.0.3
  flutter_test:
    sdk: flutter
```

### 13.2 Unit Testing de UseCases con Either

**Setup básico:**

```dart
// test/features/users/domain/usecases/get_user_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/users/domain/repositories/user_repository.dart';
import 'package:my_app/features/users/domain/usecases/get_user.dart';

// Mock del repository
class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late GetUser useCase;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    useCase = GetUser(mockRepository);
  });

  setUpAll(() {
    // Registrar fallback values
    registerFallbackValue(GetUserParams('test'));
  });

  group('GetUser UseCase', () {
    const tUser = User(id: '1', name: 'Test User');
    const tParams = GetUserParams('1');
    const tFailure = ServerFailure('Server error');

    test('debería retornar User cuando el repository succeeds', () async {
      // Arrange
      when(() => mockRepository.getUser(tParams.id))
          .thenAnswer((_) async => const Right(tUser));

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result, const Right(tUser));
      verify(() => mockRepository.getUser(tParams.id)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('debería retornar Failure cuando el repository fails', () async {
      // Arrange
      when(() => mockRepository.getUser(tParams.id))
          .thenAnswer((_) async => const Left(tFailure));

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result, const Left(tFailure));
      verify(() => mockRepository.getUser(tParams.id)).called(1);
    });
  });
}
```

### 13.3 Testing de TaskEither

```dart
// test/features/users/data/repositories/user_repository_impl_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/users/data/datasources/user_remote_datasource.dart';
import 'package:my_app/features/users/data/repositories/user_repository_impl.dart';
import 'package:my_app/core/error/failures.dart';

class MockUserRemoteDataSource extends Mock implements UserRemoteDataSource {}

void main() {
  late UserRepositoryImpl repository;
  late MockUserRemoteDataSource mockDataSource;

  setUp(() {
    mockDataSource = MockUserRemoteDataSource();
    repository = UserRepositoryImpl(mockDataSource);
  });

  group('getUser TaskEither', () {
    const tUser = User(id: '1', name: 'Test');
    const tFailure = ServerFailure('Error');

    test('debería retornar Right(User) cuando succeeds', () async {
      // Arrange
      when(() => mockDataSource.getUser('1'))
          .thenAnswer((_) async => UserModel(id: '1', name: 'Test'));

      // Act
      final result = await repository.getUser('1').run();

      // Assert
      result.match(
        (failure) => fail('No debería fallar'),
        (user) => expect(user.name, 'Test'),
      );
    });

    test('debería retornar Left(Failure) cuando falla', () async {
      // Arrange
      when(() => mockDataSource.getUser('1'))
          .thenThrow(Exception('Server error'));

      // Act
      final result = await repository.getUser('1').run();

      // Assert
      result.match(
        (failure) => expect(failure, isA<ServerFailure>()),
        (_) => fail('No debería retornar usuario'),
      );
    });

    test('debería mapear error de red a NetworkFailure', () async {
      // Arrange
      when(() => mockDataSource.getUser('1'))
          .thenThrow(SocketException('No internet'));

      // Act
      final result = await repository.getUser('1').run();

      // Assert
      result.match(
        (failure) => expect(failure.message, contains('conexión')),
        (_) => fail('No debería retornar usuario'),
      );
    });
  });
}
```

### 13.4 Testing de Validación con Either

```dart
// test/core/validators/user_validator_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/core/validators/user_validator.dart';

void main() {
  late UserValidator validator;

  setUp(() {
    validator = UserValidator();
  });

  group('validateUser', () {
    test('debería retornar Right cuando datos son válidos', () {
      // Act
      final result = validator.validateUser('John', 'john@test.com');

      // Assert
      expect(result.isRight(), true);
    });

    test('debería retornar Left(ValidationFailure) cuando nombre vacío', () {
      // Act
      final result = validator.validateUser('', 'john@test.com');

      // Assert
      result.match(
        (failure) => expect(failure.message, 'Nombre requerido'),
        (_) => fail('No debería ser válido'),
      );
    });

    test('debería retornar Left cuando email inválido', () {
      // Act
      final result = validator.validateUser('John', 'invalid-email');

      // Assert
      result.match(
        (failure) => expect(failure.message, 'Email inválido'),
        (_) => fail('No debería ser válido'),
      );
    });

    test('debería retornar primer error encontrado (fail fast)', () {
      // Arrange: ambos campos inválidos
      final result = validator.validateUser('', '');

      // Assert: solo primer error
      result.match(
        (failure) => expect(failure.message, 'Nombre requerido'),
        (_) => fail('No debería ser válido'),
      );
    });
  });
}
```

### 13.5 Testing del Result Pattern (Sealed Classes)

```dart
// test/core/error/result_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/core/error/result.dart';

void main() {
  group('Result Pattern', () {
    test('Success debe contener el valor', () {
      const result = Success<String, String>('data');

      expect(result.isSuccess, true);
      expect(result.isFailure, false);
      expect(result.value, 'data');
    });

    test('Failure debe contener el error', () {
      const result = Failure<String, String>('error');

      expect(result.isSuccess, false);
      expect(result.isFailure, true);
      expect(result.error, 'error');
    });

    test('getOrElse debe retornar valor en Success', () {
      const result = Success<int, String>(42);
      expect(result.getOrElse(0), 42);
    });

    test('getOrElse debe retornar default en Failure', () {
      const result = Failure<int, String>('error');
      expect(result.getOrElse(0), 0);
    });

    test('map debe transformar el valor', () {
      const result = Success<int, String>(10);
      final mapped = result.map((v) => v * 2);

      expect(mapped.value, 20);
    });

    test('map debe pasar el error sin transformar', () {
      const result = Failure<int, String>('error');
      final mapped = result.map((v) => v * 2);

      expect(mapped.error, 'error');
    });

    test('switch exhaustivo debe compilar', () {
      const success = Success<int, String>(42);
      const failure = Failure<int, String>('error');

      void handleResult(Result<int, String> result) {
        switch (result) {
          case Success(value: final v):
            print('Success: $v');
          case Failure(error: final e):
            print('Failure: $e');
        }
      }

      handleResult(success);
      handleResult(failure);
    });
  });
}
```

### 13.6 Testing de Integración: Repository → UseCase → Cubit

```dart
// test/features/users/presentation/cubit/user_cubit_test.dart

import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/users/domain/usecases/get_user.dart';
import 'package:my_app/features/users/presentation/cubit/user_cubit.dart';
import 'package:my_app/core/error/failures.dart';

class MockGetUser extends Mock implements GetUser {}

void main() {
  late UserCubit cubit;
  late MockGetUser mockGetUser;

  setUp(() {
    mockGetUser = MockGetUser();
    cubit = UserCubit(mockGetUser);
  });

  tearDown(() {
    cubit.close();
  });

  setUpAll(() {
    registerFallbackValue(GetUserParams('test'));
  });

  group('UserCubit', () {
    const tUser = User(id: '1', name: 'Test User');
    const tFailure = ServerFailure('Error');

    test('estado inicial debe ser UserInitial', () {
      expect(cubit.state, UserInitial());
    });

    blocTest<UserCubit, UserState>(
      'debería emitir [Loading, Loaded] cuando getUser succeeds',
      build: () {
        when(() => mockGetUser(any()))
            .thenAnswer((_) async => const Right(tUser));
        return UserCubit(mockGetUser);
      },
      act: (cubit) => cubit.loadUser('1'),
      expect: () => [
        UserLoading(),
        const UserLoaded(tUser),
      ],
      verify: (_) {
        verify(() => mockGetUser(const GetUserParams('1'))).called(1);
      },
    );

    blocTest<UserCubit, UserState>(
      'debería emitir [Loading, Error] cuando getUser fails',
      build: () {
        when(() => mockGetUser(any()))
            .thenAnswer((_) async => const Left(tFailure));
        return UserCubit(mockGetUser);
      },
      act: (cubit) => cubit.loadUser('1'),
      expect: () => [
        UserLoading(),
        const UserError(tFailure.message),
      ],
    );
  });
}
```

### 13.7 Errores Comunes en Testing

```dart
// ❌ Error: No registrar fallback values
setUpAll(() {
  // CRASH: Fallback value not set for GetUserParams
});

// ✅ Solución: Registrar antes de usar
setUpAll(() {
  registerFallbackValue(GetUserParams('fallback'));
});

// ❌ Error: Olvidar tearDown
tearDown(() {
  cubit.close(); // CRASH: Stream not closed
});

// ✅ Solución: Siempre cerrar
tearDown(() {
  cubit.close();
});

// ❌ Error: No mockear todos los métodos necesarios
when(() => mockRepo.getUser('1')).thenAnswer(...);
// CRASH: Unmocked method called

// ✅ Solución: Mockear todo lo que se llama
when(() => mockRepo.getUser(any())).thenAnswer(...);
```

### 13.8 Tabla de Herramientas de Testing

| Escenario | Herramienta Recomendada |
|-----------|------------------------|
| Mock de interfaces | `mocktail` (sin setup) |
| Mock de classes | `mockito` (con generation) |
| Testing de BLoC/Cubit | `bloc_test` |
| Testing de streams | `test` + `fake_async` |
| Testing de excepciones | `test('throws', ...)` |

---

## Resumen Ejecutivo

1. **fpdart** es el estándar moderno para FP en Dart: mantenimiento activo, sintaxis idiomatic, excelente integración con null safety
2. **Either** modela operaciones que pueden fallar con tipos explícitos
3. **TaskEither** combina asincronía y manejo de errores en una estructura composable
4. **Result Pattern** con Sealed Classes es una alternativa sin dependencias para proyectos pequeños
5. **El compilador es tu amigo**: úsalo para forzar manejo exhaustivo de errores
6. **flatMap** es esencial para encadenar operaciones que retornan Either
7. La integración con Clean Architecture es natural: Repository retorna Either, UseCase lo pasa, Cubit lo consume con fold

**La próxima vez que escribas un `try-catch`, pregúntate: ¿estoy ocultando información del tipo? ¿Debería usar Either?**

---

## Recursos Adicionales

- [Documentación oficial fpdart](https://pub.dev/packages/fpdart)
- [FP in Dart - Francesco Gullà](https://francescogulla.com/fpdart)
- [Railway Oriented Programming](https://fsharpforfunandprofit.com/posts/recipe-revisited/) - El concepto fundamental de Either
