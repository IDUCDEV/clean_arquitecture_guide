# 🎯 GUÍA: Crear Feature con Clean Architecture + Hive

> Guía original usando Hive (base de datos local)
> Para TacaMode - Ejemplo: Metas de Ahorro (Savings Goals)

---

## 📋 ÍNDICE

1. [Introducción](#introducción)
2. [Arquitectura con Hive](#arquitectura-con-hive)
3. [Ejemplo: Metas de Ahorro](#ejemplo-metas-de-ahorro)
4. [Pasos de Implementación](#pasos-de-implementación)
5. [Testing](#testing)

---

## Introducción

Esta guía usa **Hive** como base de datos local. Es diferente de la versión con API/JSON porque todo se guarda en el dispositivo.

**Ventajas de Hive:**
- ✅ No necesitas internet
- ✅ Muy rápido
- ✅ Simple de usar
- ✅ Perfecto para datos locales

---

## Arquitectura con Hive

```
┌─────────────────────────────────────────────────────────────┐
│                      HIVE DATABASE                          │
│  (Almacenamiento local en el dispositivo)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                │
│  ├── Model (@HiveType)                                     │
│  ├── LocalDataSource (CRUD con Hive)                       │
│  └── RepositoryImpl                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  DOMAIN LAYER                                              │
│  ├── Entity (Product, SavingsGoal, etc.)                   │
│  ├── Repository Interface                                  │
│  └── UseCases                                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                        │
│  ├── Cubit (estados)                                       │
│  └── UI (pantallas)                                        │
└─────────────────────────────────────────────────────────────┘
```

**Diferencia clave con API/JSON:**
- Solo hay **UN** DataSource (el local con Hive)
- No hay lógica de "online vs offline"
- Todo es síncrono/asíncrono directo a la base de datos

---

## Ejemplo: Metas de Ahorro

Vamos a crear una feature para que el usuario guarde metas de ahorro (ej: "Viaje a Japón - 2000€").

### Funcionalidades:
1. Crear meta de ahorro
2. Ver lista de metas
3. Ver progreso (ahorrado vs objetivo)
4. Eliminar metas

---

## Pasos de Implementación

### PASO 1: Domain - Entity

**Archivo**: `lib/features/savings_goal/domain/entities/savings_goal.dart`

```dart
import 'package:equatable/equatable.dart';

/// Entidad pura de una Meta de Ahorro
class SavingsGoal extends Equatable {
  const SavingsGoal({
    required this.id,
    required this.name,
    required this.targetAmount,
    this.savedAmount = 0,
    this.createdAt,
  });

  final String id;
  final String name;              // Ej: "Viaje a Japón"
  final double targetAmount;      // Ej: 2000.0
  final double savedAmount;       // Ej: 500.0
  final DateTime? createdAt;

  /// Porcentaje de progreso (0.0 a 100.0)
  double get progressPercentage {
    if (targetAmount <= 0) return 0;
    return (savedAmount / targetAmount) * 100;
  }

  /// Cuánto falta para llegar al objetivo
  double get remainingAmount => targetAmount - savedAmount;

  /// ¿Ya se completó la meta?
  bool get isCompleted => savedAmount >= targetAmount;

  SavingsGoal copyWith({
    String? id,
    String? name,
    double? targetAmount,
    double? savedAmount,
    DateTime? createdAt,
  }) {
    return SavingsGoal(
      id: id ?? this.id,
      name: name ?? this.name,
      targetAmount: targetAmount ?? this.targetAmount,
      savedAmount: savedAmount ?? this.savedAmount,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  List<Object?> get props => [id, name, targetAmount, savedAmount, createdAt];

  @override
  String toString() => 
    'SavingsGoal($name: $savedAmount/$targetAmount€)';
}
```

### PASO 2: Domain - Repository Interface

**Archivo**: `lib/features/savings_goal/domain/repositories/savings_goal_repository.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/savings_goal/domain/entities/savings_goal.dart';

abstract class SavingsGoalRepository {
  Future<Either<Failure, List<SavingsGoal>>> getGoals();
  Future<Either<Failure, void>> saveGoal(SavingsGoal goal);
  Future<Either<Failure, void>> deleteGoal(String id);
  Future<Either<Failure, void>> updateSavedAmount(String id, double newAmount);
}
```

### PASO 3: Data - Model con Hive

**Archivo**: `lib/features/savings_goal/data/models/savings_goal_model.dart`

```dart
import 'package:hive/hive.dart';
import 'package:my_app/features/savings_goal/domain/entities/savings_goal.dart';

part 'savings_goal_model.g.dart';  // Generado automáticamente

@HiveType(typeId: 4)  // ID único (0,1,2,3 ya usados en TacaMode)
class SavingsGoalModel extends HiveObject {
  SavingsGoalModel({
    required this.id,
    required this.name,
    required this.targetAmount,
    this.savedAmount = 0,
    this.createdAt,
  });

  @HiveField(0)
  String id;

  @HiveField(1)
  String name;

  @HiveField(2)
  double targetAmount;

  @HiveField(3, defaultValue: 0)
  double savedAmount;

  @HiveField(4)
  DateTime? createdAt;

  /// Model → Entity
  SavingsGoal toEntity() {
    return SavingsGoal(
      id: id,
      name: name,
      targetAmount: targetAmount,
      savedAmount: savedAmount,
      createdAt: createdAt,
    );
  }

  /// Entity → Model
  factory SavingsGoalModel.fromEntity(SavingsGoal entity) {
    return SavingsGoalModel(
      id: entity.id,
      name: entity.name,
      targetAmount: entity.targetAmount,
      savedAmount: entity.savedAmount,
      createdAt: entity.createdAt,
    );
  }

  SavingsGoalModel copyWith({
    String? id,
    String? name,
    double? targetAmount,
    double? savedAmount,
    DateTime? createdAt,
  }) {
    return SavingsGoalModel(
      id: id ?? this.id,
      name: name ?? this.name,
      targetAmount: targetAmount ?? this.targetAmount,
      savedAmount: savedAmount ?? this.savedAmount,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}
```

**IMPORTANTE**: Después de crear este archivo, debes ejecutar:

```bash
dart run build_runner build --delete-conflicting-outputs
```

Esto genera automáticamente `savings_goal_model.g.dart` con el adaptador de Hive.

### PASO 4: Data - Local DataSource

**Archivo**: `lib/features/savings_goal/data/datasources/savings_goal_local_data_source.dart`

```dart
import 'package:hive/hive.dart';
import 'package:my_app/features/savings_goal/data/models/savings_goal_model.dart';

/// DataSource con Hive (base de datos local)
abstract class SavingsGoalLocalDataSource {
  Future<List<SavingsGoalModel>> getGoals();
  Future<void> saveGoal(SavingsGoalModel goal);
  Future<void> deleteGoal(String id);
  Future<void> updateSavedAmount(String id, double newAmount);
}

class SavingsGoalLocalDataSourceImpl implements SavingsGoalLocalDataSource {
  final Box<SavingsGoalModel> _box;
  
  SavingsGoalLocalDataSourceImpl(this._box);
  
  @override
  Future<List<SavingsGoalModel>> getGoals() async {
    return _box.values.toList()
      ..sort((a, b) => (b.createdAt ?? DateTime.now())
          .compareTo(a.createdAt ?? DateTime.now()));
  }
  
  @override
  Future<void> saveGoal(SavingsGoalModel goal) async {
    await _box.put(goal.id, goal);
  }
  
  @override
  Future<void> deleteGoal(String id) async {
    await _box.delete(id);
  }
  
  @override
  Future<void> updateSavedAmount(String id, double newAmount) async {
    final goal = _box.get(id);
    if (goal != null) {
      final updated = goal.copyWith(savedAmount: newAmount);
      await _box.put(id, updated);
    }
  }
}
```

### PASO 5: Data - Repository Implementation

**Archivo**: `lib/features/savings_goal/data/repositories/savings_goal_repository_impl.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/savings_goal/data/datasources/savings_goal_local_data_source.dart';
import 'package:my_app/features/savings_goal/data/models/savings_goal_model.dart';
import 'package:my_app/features/savings_goal/domain/entities/savings_goal.dart';
import 'package:my_app/features/savings_goal/domain/repositories/savings_goal_repository.dart';

class SavingsGoalRepositoryImpl implements SavingsGoalRepository {
  final SavingsGoalLocalDataSource _localDataSource;
  
  SavingsGoalRepositoryImpl({
    required SavingsGoalLocalDataSource localDataSource,
  }) : _localDataSource = localDataSource;
  
  @override
  Future<Either<Failure, List<SavingsGoal>>> getGoals() async {
    try {
      final models = await _localDataSource.getGoals();
      final entities = models.map((m) => m.toEntity()).toList();
      return Right(entities);
    } catch (e) {
      return Left(CacheFailure('Error al cargar metas: $e'));
    }
  }
  
  @override
  Future<Either<Failure, void>> saveGoal(SavingsGoal goal) async {
    try {
      final model = SavingsGoalModel.fromEntity(goal);
      await _localDataSource.saveGoal(model);
      return const Right(null);
    } catch (e) {
      return Left(CacheFailure('Error al guardar meta: $e'));
    }
  }
  
  @override
  Future<Either<Failure, void>> deleteGoal(String id) async {
    try {
      await _localDataSource.deleteGoal(id);
      return const Right(null);
    } catch (e) {
      return Left(CacheFailure('Error al eliminar meta: $e'));
    }
  }
  
  @override
  Future<Either<Failure, void>> updateSavedAmount(
    String id, 
    double newAmount,
  ) async {
    try {
      await _localDataSource.updateSavedAmount(id, newAmount);
      return const Right(null);
    } catch (e) {
      return Left(CacheFailure('Error al actualizar: $e'));
    }
  }
}
```

**Nota clave**: Con Hive el Repository es mucho más simple porque:
- No hay lógica de "online vs offline"
- No hay que decidir entre fuentes
- Solo habla con el LocalDataSource

### PASO 6: Domain - UseCases

**Archivo**: `lib/features/savings_goal/domain/usecases/get_goals.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/savings_goal/domain/entities/savings_goal.dart';
import 'package:my_app/features/savings_goal/domain/repositories/savings_goal_repository.dart';

class GetGoals extends UseCase<List<SavingsGoal>, NoParams> {
  final SavingsGoalRepository repository;
  
  GetGoals(this.repository);
  
  @override
  Future<Either<Failure, List<SavingsGoal>>> call(NoParams params) async {
    return await repository.getGoals();
  }
}
```

**Archivo**: `lib/features/savings_goal/domain/usecases/create_goal.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/savings_goal/domain/entities/savings_goal.dart';
import 'package:my_app/features/savings_goal/domain/repositories/savings_goal_repository.dart';

class CreateGoal extends UseCase<void, CreateGoalParams> {
  final SavingsGoalRepository repository;
  
  CreateGoal(this.repository);
  
  @override
  Future<Either<Failure, void>> call(CreateGoalParams params) async {
    final goal = SavingsGoal(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: params.name,
      targetAmount: params.targetAmount,
      savedAmount: 0,
      createdAt: DateTime.now(),
    );
    
    return await repository.saveGoal(goal);
  }
}

class CreateGoalParams extends Equatable {
  final String name;
  final double targetAmount;
  
  const CreateGoalParams({
    required this.name,
    required this.targetAmount,
  });
  
  @override
  List<Object?> get props => [name, targetAmount];
}
```

### PASO 7: Presentation - Cubit

**Archivo**: `lib/features/savings_goal/presentation/cubit/savings_goal_cubit.dart`

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/features/savings_goal/domain/entities/savings_goal.dart';
import 'package:my_app/features/savings_goal/domain/usecases/create_goal.dart';
import 'package:my_app/features/savings_goal/domain/usecases/get_goals.dart';

part 'savings_goal_state.dart';

class SavingsGoalCubit extends Cubit<SavingsGoalState> {
  final GetGoals _getGoals;
  final CreateGoal _createGoal;
  
  SavingsGoalCubit({
    required GetGoals getGoals,
    required CreateGoal createGoal,
  })  : _getGoals = getGoals,
        _createGoal = createGoal,
        super(SavingsGoalInitial());
  
  Future<void> loadGoals() async {
    emit(SavingsGoalLoading());
    
    final result = await _getGoals(NoParams());
    
    result.fold(
      (failure) => emit(SavingsGoalError('Error al cargar metas')),
      (goals) => emit(SavingsGoalLoaded(goals)),
    );
  }
  
  Future<void> createGoal({
    required String name,
    required double targetAmount,
  }) async {
    emit(SavingsGoalLoading());
    
    final result = await _createGoal(
      CreateGoalParams(name: name, targetAmount: targetAmount),
    );
    
    result.fold(
      (failure) => emit(SavingsGoalError('Error al crear meta')),
      (_) {
        emit(const SavingsGoalOperationSuccess('Meta creada'));
        loadGoals();
      },
    );
  }
}
```

**Archivo**: `lib/features/savings_goal/presentation/cubit/savings_goal_state.dart`

```dart
part of 'savings_goal_cubit.dart';

abstract class SavingsGoalState extends Equatable {
  const SavingsGoalState();
  
  @override
  List<Object?> get props => [];
}

class SavingsGoalInitial extends SavingsGoalState {}

class SavingsGoalLoading extends SavingsGoalState {}

class SavingsGoalLoaded extends SavingsGoalState {
  final List<SavingsGoal> goals;
  
  const SavingsGoalLoaded(this.goals);
  
  @override
  List<Object?> get props => [goals];
}

class SavingsGoalError extends SavingsGoalState {
  final String message;
  
  const SavingsGoalError(this.message);
  
  @override
  List<Object?> get props => [message];
}

class SavingsGoalOperationSuccess extends SavingsGoalState {
  final String message;
  
  const SavingsGoalOperationSuccess(this.message);
  
  @override
  List<Object?> get props => [message];
}
```

### PASO 8: Presentation - UI

**Archivo**: `lib/features/savings_goal/presentation/pages/savings_goals_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:my_app/features/savings_goal/presentation/cubit/savings_goal_cubit.dart';

class SavingsGoalsPage extends StatelessWidget {
  const SavingsGoalsPage({super.key});
  
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => GetIt.I<SavingsGoalCubit>()..loadGoals(),
      child: Scaffold(
        appBar: AppBar(title: const Text('Metas de Ahorro')),
        body: const _SavingsGoalsView(),
        floatingActionButton: FloatingActionButton(
          onPressed: () => _showAddDialog(context),
          child: const Icon(Icons.add),
        ),
      ),
    );
  }
  
  void _showAddDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => const _AddGoalDialog(),
    );
  }
}

class _SavingsGoalsView extends StatelessWidget {
  const _SavingsGoalsView();
  
  @override
  Widget build(BuildContext context) {
    return BlocConsumer<SavingsGoalCubit, SavingsGoalState>(
      listener: (context, state) {
        if (state is SavingsGoalOperationSuccess) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message)),
          );
        }
      },
      builder: (context, state) {
        if (state is SavingsGoalLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        
        if (state is SavingsGoalError) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(state.message),
                ElevatedButton(
                  onPressed: () {
                    context.read<SavingsGoalCubit>().loadGoals();
                  },
                  child: const Text('Reintentar'),
                ),
              ],
            ),
          );
        }
        
        if (state is SavingsGoalLoaded) {
          if (state.goals.isEmpty) {
            return const Center(child: Text('No tienes metas aún'));
          }
          
          return ListView.builder(
            itemCount: state.goals.length,
            itemBuilder: (context, index) {
              final goal = state.goals[index];
              return Card(
                margin: const EdgeInsets.all(8),
                child: ListTile(
                  title: Text(goal.name),
                  subtitle: Text(
                    '${goal.savedAmount.toStringAsFixed(0)}€ / '
                    '${goal.targetAmount.toStringAsFixed(0)}€ '
                    '(${goal.progressPercentage.toStringAsFixed(1)}%)'
                  ),
                  trailing: goal.isCompleted
                    ? const Icon(Icons.check_circle, color: Colors.green)
                    : const Icon(Icons.radio_button_unchecked),
                ),
              );
            },
          );
        }
        
        return const SizedBox.shrink();
      },
    );
  }
}

class _AddGoalDialog extends StatefulWidget {
  const _AddGoalDialog();
  
  @override
  State<_AddGoalDialog> createState() => _AddGoalDialogState();
}

class _AddGoalDialogState extends State<_AddGoalDialog> {
  final _nameController = TextEditingController();
  final _amountController = TextEditingController();
  
  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Nueva Meta'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(
            controller: _nameController,
            decoration: const InputDecoration(labelText: 'Nombre'),
          ),
          TextField(
            controller: _amountController,
            decoration: const InputDecoration(labelText: 'Monto objetivo (€)'),
            keyboardType: TextInputType.number,
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancelar'),
        ),
        TextButton(
          onPressed: () {
            final name = _nameController.text;
            final amount = double.tryParse(_amountController.text) ?? 0;
            if (name.isNotEmpty && amount > 0) {
              context.read<SavingsGoalCubit>().createGoal(
                name: name,
                targetAmount: amount,
              );
              Navigator.pop(context);
            }
          },
          child: const Text('Guardar'),
        ),
      ],
    );
  }
}
```

### PASO 9: Inyección de Dependencias

**Actualizar**: `lib/core/data/local/hive_initializer.dart`

Agregar al final de `_registerAdapters()`:

```dart
if (!Hive.isAdapterRegistered(4)) {
  Hive.registerAdapter(SavingsGoalModelAdapter());
}
```

Agregar en `_openBoxes()`:

```dart
await Hive.openBox<SavingsGoalModel>('savings_goals');
```

Agregar getter:

```dart
static Box<SavingsGoalModel> get savingsGoalsBox => 
    Hive.box<SavingsGoalModel>('savings_goals');
```

**Actualizar**: `lib/core/di/injection_container.dart`

Agregar al final de `_initHive()`:

```dart
// SavingsGoal Box
..registerLazySingleton<Box<SavingsGoalModel>>(
  () => HiveInitializer.savingsGoalsBox,
)

// Data Source
..registerLazySingleton<SavingsGoalLocalDataSource>(
  () => SavingsGoalLocalDataSourceImpl(sl<Box<SavingsGoalModel>>()),
)

// Repository
..registerLazySingleton<SavingsGoalRepository>(
  () => SavingsGoalRepositoryImpl(
    localDataSource: sl<SavingsGoalLocalDataSource>(),
  ),
)

// Use Cases
..registerLazySingleton(() => GetGoals(sl<SavingsGoalRepository>()))
..registerLazySingleton(() => CreateGoal(sl<SavingsGoalRepository>()))

// Cubit
..registerFactory(() => SavingsGoalCubit(
  getGoals: sl<GetGoals>(),
  createGoal: sl<CreateGoal>(),
));
```

---

## Testing

### Test básico de Entity

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/features/savings_goal/domain/entities/savings_goal.dart';

void main() {
  group('SavingsGoal Entity', () {
    const tGoal = SavingsGoal(
      id: '1',
      name: 'Viaje',
      targetAmount: 1000,
      savedAmount: 250,
    );

    test('should calculate progress percentage correctly', () {
      expect(tGoal.progressPercentage, 25.0);
    });

    test('should identify incomplete goals', () {
      expect(tGoal.isCompleted, false);
    });

    test('should identify complete goals', () {
      const completeGoal = SavingsGoal(
        id: '2',
        name: 'Completado',
        targetAmount: 100,
        savedAmount: 100,
      );
      expect(completeGoal.isCompleted, true);
    });
  });
}
```

---

## ✅ Checklist para Feature con Hive

```
□ Domain
  □ Entity creada
  □ Repository interface creada

□ Data
  □ Model con @HiveType y @HiveField
  □ Ejecutar: dart run build_runner build
  □ LocalDataSource con CRUD

□ Repository
  □ Implementación simple (solo habla con Hive)

□ UseCases
  □ GetGoals
  □ CreateGoal

□ Presentation
  □ States
  □ Cubit
  □ UI

□ Hive
  □ Agregar typeId único (no repetido)
  □ Registrar adaptador en HiveInitializer
  □ Abrir box
  □ Registrar todo en injection_container.dart

□ Testing
  □ Test de Entity
```

---

## 🎯 Diferencias: Hive vs API/JSON

| Aspecto | Hive (Local) | API/JSON (Remoto) |
|---------|--------------|-------------------|
| **Internet** | No necesita | Sí necesita |
| **DataSources** | Solo 1 (local) | 2 (local + remoto) |
| **Repository** | Simple | Complejo (decide fuente) |
| **Modelo** | @HiveType | fromJson/toJson |
| **Generación** | build_runner | No necesita |
| **Uso ideal** | Datos del usuario | Datos compartidos |

---

**¿Necesitas que profundice en algún paso específico de esta guía con Hive?**