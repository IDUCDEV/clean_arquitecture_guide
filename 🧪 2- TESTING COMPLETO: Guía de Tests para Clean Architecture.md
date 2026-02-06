# 🧪 TESTING COMPLETO: Guía de Tests para Clean Architecture

## Índice
1. [Introducción al Testing](#introducción-al-testing)
2. [Testing Domain (Entities y UseCases)](#testing-domain)
3. [Testing Data (DataSources y Repository)](#testing-data)
4. [Testing Presentation (Cubit)](#testing-presentation)
5. [Mocking y Fixtures](#mocking-y-fixtures)

---

## Introducción al Testing

### 🎯 ¿Por qué testear por capas?

Clean Architecture facilita testing porque cada capa es independiente:

```
Domain:       Testeamos lógica pura (sin Flutter, sin HTTP)
Data:         Testeamos con mocks de base de datos/API
Presentation: Testeamos estados del Cubit
```

### 📦 Dependencias necesarias (pubspec.yaml)

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0          # Para testear Cubits
  mocktail: ^1.0.0           # Para mocks modernos (mejor que mockito)
  faker: ^2.0.0              # Para generar datos de prueba
```

---

## Testing Domain

### Test 1: Entity

**Archivo**: `test/features/task/domain/entities/task_test.dart`

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/features/task/domain/entities/task.dart';

void main() {
  group('Task Entity', () {
    // Datos de prueba
    const tTask = Task(
      id: '1',
      title: 'Test Task',
      description: 'Test Description',
      isCompleted: false,
    );

    test('should create task with required fields', () {
      // Act es la creación misma
      const task = Task(
        id: '2',
        title: 'Another Task',
        description: 'Another Description',
      );

      // Assert
      expect(task.id, '2');
      expect(task.title, 'Another Task');
      expect(task.isCompleted, false); // Valor por defecto
    });

    test('should correctly identify overdue tasks', () {
      // Arrange: Tarea vencida (ayer)
      final overdueTask = Task(
        id: '1',
        title: 'Overdue',
        dueDate: DateTime.now().subtract(const Duration(days: 1)),
      );

      // Act & Assert
      expect(overdueTask.isOverdue, true);
    });

    test('should correctly identify non-overdue tasks', () {
      // Arrange: Tarea no vencida (mañana)
      final futureTask = Task(
        id: '1',
        title: 'Future',
        dueDate: DateTime.now().add(const Duration(days: 1)),
      );

      // Act & Assert
      expect(futureTask.isOverdue, false);
    });

    test('should correctly identify completed tasks as not overdue', () {
      // Arrange: Tarea vencida pero completada
      final completedOverdueTask = Task(
        id: '1',
        title: 'Completed',
        isCompleted: true,
        dueDate: DateTime.now().subtract(const Duration(days: 1)),
      );

      // Act & Assert
      expect(completedOverdueTask.isOverdue, false);
    });

    test('copyWith should update only specified fields', () {
      // Act
      final updated = tTask.copyWith(title: 'Updated Title');

      // Assert: Solo cambió el título
      expect(updated.id, tTask.id); // Igual
      expect(updated.title, 'Updated Title'); // Cambió
      expect(updated.description, tTask.description); // Igual
    });

    test('should be equal when properties are equal', () {
      // Arrange
      const task1 = Task(id: '1', title: 'Test', description: 'Desc');
      const task2 = Task(id: '1', title: 'Test', description: 'Desc');

      // Act & Assert
      expect(task1, task2); // Gracias a Equatable
    });

    test('should not be equal when properties differ', () {
      // Arrange
      const task1 = Task(id: '1', title: 'Test', description: 'Desc');
      const task2 = Task(id: '1', title: 'Different', description: 'Desc');

      // Act & Assert
      expect(task1, isNot(task2));
    });
  });
}
```

**🎓 Conceptos**:
- `group`: Agrupa tests relacionados
- `test`: Un caso de prueba individual
- `expect(actual, expected)`: Afirmación
- `setUp`: Código que corre antes de cada test

---

### Test 2: UseCase

**Archivo**: `test/features/task/domain/usecases/get_tasks_test.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/task/domain/entities/task.dart';
import 'package:my_app/features/task/domain/repositories/task_repository.dart';
import 'package:my_app/features/task/domain/usecases/get_tasks.dart';

// Mock del Repository
class MockTaskRepository extends Mock implements TaskRepository {}

void main() {
  late GetTasks useCase;
  late MockTaskRepository mockRepository;

  // Configuración inicial antes de cada test
  setUp(() {
    mockRepository = MockTaskRepository();
    useCase = GetTasks(mockRepository);
  });

  // Datos de prueba
  final tTasks = [
    const Task(id: '1', title: 'Task 1', description: 'Desc 1'),
    const Task(id: '2', title: 'Task 2', description: 'Desc 2'),
  ];

  test('should get tasks from repository', () async {
    // ARRANGE: Configurar el mock
    // Cuando se llame a getTasks(), retornar Right(tTasks)
    when(() => mockRepository.getTasks())
        .thenAnswer((_) async => Right(tTasks));

    // ACT: Ejecutar el caso de uso
    final result = await useCase(NoParams());

    // ASSERT: Verificar resultados
    expect(result, Right(tTasks));
    verify(() => mockRepository.getTasks()).called(1); // Se llamó exactamente 1 vez
    verifyNoMoreInteractions(mockRepository); // No hubo otras llamadas
  });

  test('should return failure when repository fails', () async {
    // ARRANGE: Configurar mock para que falle
    when(() => mockRepository.getTasks())
        .thenAnswer((_) async => Left(ServerFailure('Server error')));

    // ACT
    final result = await useCase(NoParams());

    // ASSERT
    expect(result, isA<Left<Failure, List<Task>>>());
    expect(result.fold((l) => l, (r) => null), isA<ServerFailure>());
  });
}
```

**🎓 Conceptos**:
- `Mock`: Objeto falso que simula el Repository real
- `when(...).thenAnswer(...)`: Define comportamiento del mock
- `verify(...)`: Comprueba que se llamó a un método
- `fold`: Extrae el valor de Either para verificar

---

### Test 3: CreateTask UseCase

**Archivo**: `test/features/task/domain/usecases/create_task_test.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/task/domain/entities/task.dart';
import 'package:my_app/features/task/domain/repositories/task_repository.dart';
import 'package:my_app/features/task/domain/usecases/create_task.dart';

class MockTaskRepository extends Mock implements TaskRepository {}

void main() {
  late CreateTask useCase;
  late MockTaskRepository mockRepository;

  setUp(() {
    mockRepository = MockTaskRepository();
    useCase = CreateTask(mockRepository);
  });

  const tTitle = 'New Task';
  const tDescription = 'New Description';

  final tCreatedTask = Task(
    id: '123',
    title: tTitle,
    description: tDescription,
    createdAt: DateTime.now(),
  );

  test('should create task and return it', () async {
    // ARRANGE
    when(() => mockRepository.createTask(
      title: tTitle,
      description: tDescription,
      dueDate: null,
    )).thenAnswer((_) async => Right(tCreatedTask));

    // ACT
    final result = await useCase(const CreateTaskParams(
      title: tTitle,
      description: tDescription,
    ));

    // ASSERT
    expect(result, Right(tCreatedTask));
    verify(() => mockRepository.createTask(
      title: tTitle,
      description: tDescription,
      dueDate: null,
    )).called(1);
  });

  test('should pass dueDate when provided', () async {
    // ARRANGE
    final dueDate = DateTime(2024, 12, 31);
    
    when(() => mockRepository.createTask(
      title: tTitle,
      description: any(named: 'description'),
      dueDate: dueDate,
    )).thenAnswer((_) async => Right(tCreatedTask));

    // ACT
    await useCase(CreateTaskParams(
      title: tTitle,
      description: tDescription,
      dueDate: dueDate,
    ));

    // ASSERT
    verify(() => mockRepository.createTask(
      title: tTitle,
      description: tDescription,
      dueDate: dueDate,
    )).called(1);
  });
}
```

---

## Testing Data

### Test 4: Remote DataSource

**Archivo**: `test/features/task/data/datasources/task_remote_data_source_test.dart`

```dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/error/exceptions.dart';
import 'package:my_app/features/task/data/datasources/task_remote_data_source.dart';
import 'package:my_app/features/task/data/models/task_model.dart';

// Mock del cliente HTTP
class MockHttpClient extends Mock implements http.Client {}

void main() {
  late TaskRemoteDataSourceImpl dataSource;
  late MockHttpClient mockHttpClient;

  setUp(() {
    mockHttpClient = MockHttpClient();
    dataSource = TaskRemoteDataSourceImpl(
      client: mockHttpClient,
      baseUrl: 'https://api.test.com',
    );
  });

  group('getTasks', () {
    final tTaskList = [
      {
        'id': '1',
        'title': 'Test Task',
        'description': 'Test Description',
        'isCompleted': false,
        'createdAt': '2024-01-01T00:00:00Z',
      }
    ];

    test('should return list of tasks when response is 200', () async {
      // ARRANGE
      when(() => mockHttpClient.get(
        Uri.parse('https://api.test.com/api/tasks'),
        headers: any(named: 'headers'),
      )).thenAnswer((_) async => http.Response(
        json.encode(tTaskList),
        200,
      ));

      // ACT
      final result = await dataSource.getTasks();

      // ASSERT
      expect(result, isA<List<TaskModel>>());
      expect(result.length, 1);
      expect(result.first.id, '1');
    });

    test('should throw ServerException when response is not 200', () async {
      // ARRANGE
      when(() => mockHttpClient.get(any(), headers: any(named: 'headers')))
          .thenAnswer((_) async => http.Response('Not Found', 404));

      // ACT & ASSERT
      expect(
        () => dataSource.getTasks(),
        throwsA(isA<ServerException>()),
      );
    });
  });

  group('createTask', () {
    final tTaskModel = TaskModel(
      id: '1',
      title: 'New Task',
      description: 'Description',
    );

    final tResponse = {
      'id': '123',
      'title': 'New Task',
      'description': 'Description',
      'isCompleted': false,
      'createdAt': '2024-01-01T00:00:00Z',
    };

    test('should return created task when response is 201', () async {
      // ARRANGE
      when(() => mockHttpClient.post(
        Uri.parse('https://api.test.com/api/tasks'),
        headers: any(named: 'headers'),
        body: json.encode(tTaskModel.toJsonForCreate()),
      )).thenAnswer((_) async => http.Response(
        json.encode(tResponse),
        201,
      ));

      // ACT
      final result = await dataSource.createTask(tTaskModel);

      // ASSERT
      expect(result, isA<TaskModel>());
      expect(result.id, '123');
    });

    test('should throw ServerException when response is not 201', () async {
      // ARRANGE
      when(() => mockHttpClient.post(any(), headers: any(named: 'headers'), body: any(named: 'body')))
          .thenAnswer((_) async => http.Response('Error', 500));

      // ACT & ASSERT
      expect(
        () => dataSource.createTask(tTaskModel),
        throwsA(isA<ServerException>()),
      );
    });
  });
}
```

---

### Test 5: Repository Implementation

**Archivo**: `test/features/task/data/repositories/task_repository_impl_test.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/error/exceptions.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/core/network/network_info.dart';
import 'package:my_app/features/task/data/datasources/task_local_data_source.dart';
import 'package:my_app/features/task/data/datasources/task_remote_data_source.dart';
import 'package:my_app/features/task/data/models/task_model.dart';
import 'package:my_app/features/task/data/repositories/task_repository_impl.dart';
import 'package:my_app/features/task/domain/entities/task.dart';

// Mocks
class MockRemoteDataSource extends Mock implements TaskRemoteDataSource {}
class MockLocalDataSource extends Mock implements TaskLocalDataSource {}
class MockNetworkInfo extends Mock implements NetworkInfo {}

void main() {
  late TaskRepositoryImpl repository;
  late MockRemoteDataSource mockRemote;
  late MockLocalDataSource mockLocal;
  late MockNetworkInfo mockNetwork;

  setUp(() {
    mockRemote = MockRemoteDataSource();
    mockLocal = MockLocalDataSource();
    mockNetwork = MockNetworkInfo();
    repository = TaskRepositoryImpl(
      remoteDataSource: mockRemote,
      localDataSource: mockLocal,
      networkInfo: mockNetwork,
    );
  });

  group('getTasks', () {
    final tTaskModels = [
      TaskModel(id: '1', title: 'Task 1', description: 'Desc 1'),
    ];

    final tTasks = [
      const Task(id: '1', title: 'Task 1', description: 'Desc 1'),
    ];

    test('should check if device is online', () async {
      // ARRANGE
      when(() => mockNetwork.isConnected).thenAnswer((_) async => true);
      when(() => mockRemote.getTasks()).thenAnswer((_) async => tTaskModels);
      when(() => mockLocal.cacheTasks(any())).thenAnswer((_) async => {});

      // ACT
      await repository.getTasks();

      // ASSERT
      verify(() => mockNetwork.isConnected).called(1);
    });

    group('device is online', () {
      setUp(() {
        when(() => mockNetwork.isConnected).thenAnswer((_) async => true);
      });

      test('should return remote data when remote call is successful', () async {
        // ARRANGE
        when(() => mockRemote.getTasks()).thenAnswer((_) async => tTaskModels);
        when(() => mockLocal.cacheTasks(any())).thenAnswer((_) async => {});

        // ACT
        final result = await repository.getTasks();

        // ASSERT
        verify(() => mockRemote.getTasks());
        expect(result, Right(tTasks));
      });

      test('should cache data locally when remote call is successful', () async {
        // ARRANGE
        when(() => mockRemote.getTasks()).thenAnswer((_) async => tTaskModels);
        when(() => mockLocal.cacheTasks(any())).thenAnswer((_) async => {});

        // ACT
        await repository.getTasks();

        // ASSERT
        verify(() => mockLocal.cacheTasks(tTaskModels));
      });

      test('should return server failure when remote call fails', () async {
        // ARRANGE
        when(() => mockRemote.getTasks()).thenThrow(ServerException());
        when(() => mockLocal.getTasks()).thenAnswer((_) async => []);

        // ACT
        final result = await repository.getTasks();

        // ASSERT
        expect(result, isA<Left<Failure, List<Task>>>());
      });
    });

    group('device is offline', () {
      setUp(() {
        when(() => mockNetwork.isConnected).thenAnswer((_) async => false);
      });

      test('should return local data when device is offline', () async {
        // ARRANGE
        when(() => mockLocal.getTasks()).thenAnswer((_) async => tTaskModels);

        // ACT
        final result = await repository.getTasks();

        // ASSERT
        verify(() => mockLocal.getTasks());
        verifyNever(() => mockRemote.getTasks());
        expect(result, Right(tTasks));
      });

      test('should return cache failure when no local data', () async {
        // ARRANGE
        when(() => mockLocal.getTasks()).thenAnswer((_) async => []);

        // ACT
        final result = await repository.getTasks();

        // ASSERT
        expect(result, isA<Left<Failure, List<Task>>>());
      });
    });
  });
}
```

---

## Testing Presentation

### Test 6: Cubit

**Archivo**: `test/features/task/presentation/cubit/task_cubit_test.dart`

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/task/domain/entities/task.dart';
import 'package:my_app/features/task/domain/usecases/create_task.dart';
import 'package:my_app/features/task/domain/usecases/delete_task.dart';
import 'package:my_app/features/task/domain/usecases/get_tasks.dart';
import 'package:my_app/features/task/presentation/cubit/task_cubit.dart';

// Mocks
class MockGetTasks extends Mock implements GetTasks {}
class MockCreateTask extends Mock implements CreateTask {}
class MockDeleteTask extends Mock implements DeleteTask {}

void main() {
  late TaskCubit cubit;
  late MockGetTasks mockGetTasks;
  late MockCreateTask mockCreateTask;
  late MockDeleteTask mockDeleteTask;

  setUp(() {
    mockGetTasks = MockGetTasks();
    mockCreateTask = MockCreateTask();
    mockDeleteTask = MockDeleteTask();
    cubit = TaskCubit(
      getTasks: mockGetTasks,
      createTask: mockCreateTask,
      deleteTask: mockDeleteTask,
    );
  });

  tearDown(() {
    cubit.close();
  });

  group('loadTasks', () {
    final tTasks = [
      const Task(id: '1', title: 'Task 1', description: 'Desc 1'),
    ];

    blocTest<TaskCubit, TaskState>(
      'should emit [Loading, Loaded] when data is gotten successfully',
      build: () {
        when(() => mockGetTasks(NoParams()))
            .thenAnswer((_) async => Right(tTasks));
        return cubit;
      },
      act: (cubit) => cubit.loadTasks(),
      expect: () => [
        TaskLoading(),
        TaskLoaded(tTasks),
      ],
      verify: (_) {
        verify(() => mockGetTasks(NoParams())).called(1);
      },
    );

    blocTest<TaskCubit, TaskState>(
      'should emit [Loading, Error] when getting data fails',
      build: () {
        when(() => mockGetTasks(NoParams()))
            .thenAnswer((_) async => Left(ServerFailure('Error')));
        return cubit;
      },
      act: (cubit) => cubit.loadTasks(),
      expect: () => [
        TaskLoading(),
        isA<TaskError>(),
      ],
    );
  });

  group('createTask', () {
    const tTitle = 'New Task';
    const tDescription = 'New Description';
    final tTask = Task(
      id: '1',
      title: tTitle,
      description: tDescription,
      createdAt: DateTime.now(),
    );

    blocTest<TaskCubit, TaskState>(
      'should emit [Loading, OperationSuccess, Loading, Loaded] when task is created',
      build: () {
        when(() => mockCreateTask(any()))
            .thenAnswer((_) async => Right(tTask));
        when(() => mockGetTasks(NoParams()))
            .thenAnswer((_) async => Right([tTask]));
        return cubit;
      },
      act: (cubit) => cubit.createTask(title: tTitle, description: tDescription),
      expect: () => [
        TaskLoading(),
        isA<TaskOperationSuccess>(),
        TaskLoading(),
        isA<TaskLoaded>(),
      ],
    );
  });
}
```

**🎓 Conceptos**:
- `blocTest`: Test especial para Cubits/Blocs
- `build`: Crea el Cubit
- `act`: Ejecuta la acción
- `expect`: Lista de estados esperados en orden
- `verify`: Verifica interacciones con mocks

---

## Mocking y Fixtures

### Helper para Fixtures

**Archivo**: `test/fixtures/fixture_reader.dart`

```dart
import 'dart:io';

String fixture(String name) =>
    File('test/fixtures/$name.json').readAsStringSync();
```

**Uso en tests**:

```dart
// test/fixtures/tasks.json
// Contiene: [{"id": "1", "title": "Task 1"}]

final jsonString = fixture('tasks');
final jsonMap = json.decode(jsonString);
```

### Fakers para datos dinámicos

```dart
import 'package:faker/faker.dart';

final faker = Faker();

// Generar datos de prueba
final randomTask = Task(
  id: faker.guid.guid(),
  title: faker.lorem.sentence(),
  description: faker.lorem.paragraph(),
  createdAt: faker.date.dateTime(),
);
```

---

## Coverage de Tests

### Comando para ver cobertura

```bash
# Generar cobertura
flutter test --coverage

# Ver reporte HTML
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

### Qué testear (prioridad)

| Componente | Prioridad | Qué testear |
|------------|-----------|-------------|
| Entities | ⭐⭐⭐ Alta | Lógica de negocio, copyWith |
| UseCases | ⭐⭐⭐ Alta | Flujo completo, errores |
| Repository | ⭐⭐⭐ Alta | Local vs Remote, fallback |
| DataSources | ⭐⭐⭐ Alta | HTTP, BD, parsing |
| Cubits | ⭐⭐⭐ Alta | Estados, transiciones |
| Models | ⭐⭐ Media | fromJson, toJson, toEntity |
| UI Widgets | ⭐⭐ Media | Renderizado por estado |

---

## 🎯 Checklist de Testing

```
□ Tests de Domain
  □ Entity: lógica de negocio
  □ Entity: copyWith
  □ Entity: equality
  □ UseCase: éxito
  □ UseCase: error
  □ UseCase: parámetros

□ Tests de Data
  □ RemoteDataSource: HTTP 200
  □ RemoteDataSource: HTTP error
  □ RemoteDataSource: parsing JSON
  □ LocalDataSource: CRUD completo
  □ Repository: online → remote
  □ Repository: offline → local
  □ Repository: fallback cuando remote falla

□ Tests de Presentation
  □ Cubit: estado inicial
  □ Cubit: transición Loading → Loaded
  □ Cubit: transición Loading → Error
  □ Cubit: llamadas a UseCases
```

---

**Recuerda**: Los tests son documentación viva. Un test bien escrito explica cómo funciona tu código.
