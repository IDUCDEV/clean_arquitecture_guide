## 7. Testing por Capas

### Testing Domain (Fácil)

```dart
// test/features/user/domain/entities/user_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/features/user/domain/entities/user.dart';

void main() {
  group('User Entity', () {
    test('should create user with required fields', () {
      const user = User(id: '1', name: 'John', email: 'john@example.com');
      
      expect(user.id, '1');
      expect(user.name, 'John');
      expect(user.isActive, true);
    });
    
    test('should calculate hasAvatar correctly', () {
      const userWithAvatar = User(
        id: '1', name: 'John', email: 'john@example.com',
        avatarUrl: 'http://example.com/avatar.png',
      );
      
      const userWithoutAvatar = User(
        id: '2', name: 'Jane', email: 'jane@example.com',
      );
      
      expect(userWithAvatar.hasAvatar, true);
      expect(userWithoutAvatar.hasAvatar, false);
    });
    
    test('isNew should return true for users created less than 7 days ago', () {
      final recentUser = User(
        id: '1', name: 'John', email: 'john@example.com',
        createdAt: DateTime.now().subtract(const Duration(days: 3)),
      );
      
      expect(recentUser.isNew, true);
    });
    
    test('copyWith should update only specified fields', () {
      const user = User(id: '1', name: 'John', email: 'john@example.com');
      
      final updated = user.copyWith(name: 'Jane');
      
      expect(updated.id, '1');
      expect(updated.name, 'Jane');
      expect(updated.email, 'john@example.com');
    });
  });
}
```

### Testing UseCases (Fácil)

```dart
// test/features/user/domain/usecases/get_users_test.dart

import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';
import 'package:my_app/features/user/domain/usecases/get_users.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late GetUsers useCase;
  late MockUserRepository mockRepository;
  
  setUp(() {
    mockRepository = MockUserRepository();
    useCase = GetUsers(mockRepository);
  });
  
  const tUsers = [
    User(id: '1', name: 'John', email: 'john@example.com'),
    User(id: '2', name: 'Jane', email: 'jane@example.com'),
  ];
  
  test('should get users from repository', () async {
    when(() => mockRepository.getUsers())
        .thenAnswer((_) async => Either.right(tUsers));
    
    final result = await useCase(NoParams());
    
    expect(result, Either.right(tUsers));
    verify(() => mockRepository.getUsers()).called(1);
  });
}
```

### Testing Repository (Medio)

```dart
// test/features/user/data/repositories/user_repository_impl_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/features/user/data/datasources/user_local_data_source.dart';
import 'package:my_app/features/user/data/models/user_model.dart';
import 'package:my_app/features/user/data/repositories/user_repository_impl.dart';

class MockUserLocalDataSource extends Mock implements UserLocalDataSource {}

void main() {
  late UserRepositoryImpl repository;
  late MockUserLocalDataSource mockDataSource;
  
  setUp(() {
    mockDataSource = MockUserLocalDataSource();
    repository = UserRepositoryImpl(localDataSource: mockDataSource);
  });
  
  group('getUsers', () {
    final tUserModels = [
      UserModel(id: '1', name: 'John', email: 'john@example.com'),
    ];
    
    test('should return list of users when data source succeeds', () async {
      when(() => mockDataSource.getUsers())
          .thenAnswer((_) async => tUserModels);
      
      final result = await repository.getUsers();
      
      expect(result.isEither.right(), true);
    });
  });
}
```

### Testing Cubit (Medio)

```dart
// test/features/user/presentation/cubit/user_cubit_test.dart

import 'package:bloc_test/bloc_test.dart';
import 'package:fpdart/fpdart.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/usecases/create_user.dart';
import 'package:my_app/features/user/domain/usecases/delete_user.dart';
import 'package:my_app/features/user/domain/usecases/get_user.dart';
import 'package:my_app/features/user/domain/usecases/get_users.dart';
import 'package:my_app/features/user/presentation/cubit/user_cubit.dart';

class MockGetUsers extends Mock implements GetUsers {}
class MockGetUser extends Mock implements GetUser {}
class MockCreateUser extends Mock implements CreateUser {}
class MockDeleteUser extends Mock implements DeleteUser {}

void main() {
  late UserCubit cubit;
  late MockGetUsers mockGetUsers;
  late MockGetUser mockGetUser;
  late MockCreateUser mockCreateUser;
  late MockDeleteUser mockDeleteUser;

  setUp(() {
    mockGetUsers = MockGetUsers();
    mockGetUser = MockGetUser();
    mockCreateUser = MockCreateUser();
    mockDeleteUser = MockDeleteUser();
    cubit = UserCubit(
      getUsers: mockGetUsers,
      getUser: mockGetUser,
      createUser: mockCreateUser,
      deleteUser: mockDeleteUser,
    );
  });

  const tUsers = [
    User(id: '1', name: 'John', email: 'john@example.com'),
  ];

  test('initial state should be UserInitial', () {
    expect(cubit.state, isA<UserInitial>());
  });

  blocTest<UserCubit, UserState>(
    'emits [UserLoading, UsersLoaded] when loadUsers succeeds',
    build: () {
      when(() => mockGetUsers(NoParams()))
          .thenAnswer((_) async => Either.right(tUsers));
      return cubit;
    },
    act: (cubit) => cubit.loadUsers(),
    expect: () => [
      isA<UserLoading>(),
      const UsersLoaded(tUsers),
    ],
  );

  blocTest<UserCubit, UserState>(
    'emits [UserLoading, UserError] when loadUsers fails',
    build: () {
      when(() => mockGetUsers(NoParams()))
          .thenAnswer((_) async => Either.left(CacheFailure('Error')));
      return cubit;
    },
    act: (cubit) => cubit.loadUsers(),
    expect: () => [
      isA<UserLoading>(),
      isA<UserError>(),
    ],
  );
}
```

---
