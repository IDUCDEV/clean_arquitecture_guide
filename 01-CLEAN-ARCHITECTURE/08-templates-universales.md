## 8. Templates Universales

### Template 1: Entity

```dart
import 'package:equatable/equatable.dart';

class {Feature} extends Equatable {
  const {Feature}({
    required this.id,
    required this.name,
    this.isActive = true,
    this.createdAt,
  });

  final String id;
  final String name;
  final bool isActive;
  final DateTime? createdAt;

  {Feature} copyWith({
    String? id,
    String? name,
    bool? isActive,
    DateTime? createdAt,
  }) {
    return {Feature}(
      id: id ?? this.id,
      name: name ?? this.name,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  List<Object?> get props => [id, name, isActive, createdAt];
}
```

### Template 2: Repository Interface

```dart
import 'package:fpdart/fpdart.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/{feature}/domain/entities/{feature}.dart';

abstract class {Feature}Repository {
  Future<Either<Failure, List<{Feature}>>> getAll();
  Future<Either<Failure, {Feature}>> getById(String id);
  Future<Either<Failure, void>> create({Feature} {feature});
  Future<Either<Failure, void>> update({Feature} {feature});
  Future<Either<Failure, void>> delete(String id);
}
```

### Template 3: UseCase

```dart
import 'package:fpdart/fpdart.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/{feature}/domain/entities/{feature}.dart';
import 'package:my_app/features/{feature}/domain/repositories/{feature}_repository.dart';

class Get{Feature} extends UseCase<{Feature}, Get{Feature}Params> {
  final {Feature}Repository repository;
  
  Get{Feature}(this.repository);
  
  @override
  Future<Either<Failure, {Feature}>> call(Get{Feature}Params params) async {
    return await repository.getById(params.id);
  }
}

class Get{Feature}Params extends Equatable {
  final String id;
  
  const Get{Feature}Params(this.id);
  
  @override
  List<Object?> get props => [id];
}
```

### Template 4: Cubit

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/features/{feature}/domain/entities/{feature}.dart';
import 'package:my_app/features/{feature}/domain/usecases/get_{feature}.dart';

part '{feature}_state.dart';

class {Feature}Cubit extends Cubit<{Feature}State> {
  final Get{Feature} _get{Feature};
  
  {Feature}Cubit({required Get{Feature} get{Feature}})
      : _get{Feature} = get{Feature},
        super({Feature}Initial());
  
  Future<void> load{Feature}(String id) async {
    emit({Feature}Loading());
    
    final result = await _get{Feature}(Get{Feature}Params(id));
    
    result.match(
      (failure) => emit({Feature}Error(failure.toString())),
      ({feature}) => emit({Feature}Loaded({feature})),
    );
  }
}
```

### Template 5: State

```dart
part of '{feature}_cubit.dart';

abstract class {Feature}State extends Equatable {
  const {Feature}State();
  
  @override
  List<Object?> get props => [];
}

class {Feature}Initial extends {Feature}State {}
class {Feature}Loading extends {Feature}State {}
class {Feature}Loaded extends {Feature}State {
  final {Feature} {feature};
  const {Feature}Loaded(this.{feature});
  
  @override
  List<Object?> get props => [{feature}];
}
class {Feature}Error extends {Feature}State {
  final String message;
  const {Feature}Error(this.message);
  
  @override
  List<Object?> get props => [message];
}
```

---
