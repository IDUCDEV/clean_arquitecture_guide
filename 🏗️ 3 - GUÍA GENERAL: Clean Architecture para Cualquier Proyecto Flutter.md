# 🏗️ GUÍA GENERAL: Clean Architecture para Cualquier Proyecto Flutter

## Índice
1. [Filosofía de Clean Architecture](#filosofía-de-clean-architecture)
2. [Estructura de Carpetas Universal](#estructura-de-carpetas-universal)
3. [Flujo de Datos: La Regla de Dependencia](#flujo-de-datos-la-regla-de-dependencia)
4. [Template Universal por Capa](#template-universal-por-capa)
5. [Ejemplo Completo: Sistema de Usuarios](#ejemplo-completo-sistema-de-usuarios)
6. [Patrones y Decisiones de Diseño](#patrones-y-decisiones-de-diseño)
7. [Testing por Capas](#testing-por-capas)
8. [Migración desde Código Spaghetti](#migración-desde-código-spaghetti)

---

## Filosofía de Clean Architecture

### 🎯 El Problema: Código Spaghetti

Imagina un plato de espagueti donde todo está mezclado:
- UI con lógica de negocio
- Llamadas HTTP en los widgets
- Base de datos acoplada a la interfaz
- Imposible de testear
- Un cambio rompe todo

### ✅ La Solución: Capas Independientes

Clean Architecture organiza el código como un **edificio de oficinas**:

```
        ┌─────────────────────────────────────┐
        │      PLANTA 4: UI (Presentation)    │
        │    ┌─────┐ ┌─────┐ ┌─────┐         │
        │    │Pág 1│ │Pág 2│ │Pág 3│         │
        │    └──┬──┘ └──┬──┘ └──┬──┘         │
        └───────┼───────┼───────┼─────────────┘
                │       │       │
                ▼       ▼       ▼
        ┌─────────────────────────────────────┐
        │     PLANTA 3: LÓGICA (Domain)       │
        │   ┌────────┐ ┌────────┐             │
        │   │UseCase1│ │UseCase2│             │
        │   └───┬────┘ └────┬───┘             │
        └───────┼───────────┼─────────────────┘
                │           │
                ▼           ▼
        ┌─────────────────────────────────────┐
        │    PLANTA 2: CONTRATOS (Repository) │
        │        ┌──────────────┐             │
        │        │   Interface  │             │
        │        └──────┬───────┘             │
        └───────────────┼─────────────────────┘
                        │
                        ▼
        ┌─────────────────────────────────────┐
        │      PLANTA 1: DATOS (Data)         │
        │  ┌──────────┐ ┌──────────┐          │
        │  │DataSource│ │   Model  │          │
        │  └──────────┘ └──────────┘          │
        └─────────────────────────────────────┘
```

**Regla de Oro**: Código de plantas superiores NUNCA conoce detalles de plantas inferiores.

### 🎭 Las 4 Capas en Detalle

#### 1️⃣ **Domain** (El Núcleo)
**Contiene**: Entities, Repository Interfaces, Use Cases

**Principios**:
- Pura lógica de negocio
- Sin dependencias externas (no Flutter, no HTTP, no DB)
- Altamente testeable
- Reutilizable en otros proyectos

**Analogía**: Las reglas del juego de ajedrez (cómo se mueven las piezas)

#### 2️⃣ **Data** (La Implementación)
**Contiene**: Models, DataSources, Repository Implementations

**Principios**:
- Implementa los contratos del Domain
- Habla con APIs, bases de datos, cache
- Convierte datos externos a Entities

**Analogía**: El tablero físico y las piezas de ajedrez

#### 3️⃣ **Presentation** (El Estado)
**Contiene**: Cubits/Blocs, States

**Principios**:
- Maneja el estado de la UI
- Orquesta Use Cases
- Sin lógica de negocio compleja

**Analogía**: El visor que muestra el tablero en tu celular

#### 4️⃣ **UI** (La Vista)
**Contiene**: Widgets, Pages, Screens

**Principios**:
- Solo muestra datos
- Recibe eventos del usuario
- Se reconstruye cuando cambia el estado

**Analogía**: La pantalla de tu celular

---

## Estructura de Carpetas Universal

### 📁 Estructura Base

```
lib/
├── core/                           # Código compartido entre features
│   ├── common/                     # Clases base (UseCase, etc.)
│   │   └── usecase.dart
│   ├── data/                       # Configuración de datos global
│   │   └── local/
│   │       └── database_initializer.dart
│   ├── di/                         # Inyección de dependencias
│   │   └── injection_container.dart
│   ├── error/                      # Manejo de errores
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/                    # Configuración de red
│   │   ├── network_info.dart
│   │   └── dio_client.dart
│   ├── routing/                    # Navegación
│   │   └── app_router.dart
│   ├── theme/                      # Tema y estilos
│   │   └── app_theme.dart
│   └── utils/                      # Utilidades
│       └── constants.dart
│
├── features/                       # Cada feature tiene su propia estructura
│   └── {feature_name}/             # Ej: user, product, order, etc.
│       ├── data/
│       │   ├── datasources/
│       │   │   └── {feature}_local_data_source.dart
│       │   │   └── {feature}_remote_data_source.dart  # Opcional
│       │   ├── models/
│       │   │   └── {feature}_model.dart
│       │   │   └── {feature}_model.g.dart  # Generado
│       │   └── repositories/
│       │       └── {feature}_repository_impl.dart
│       │
│       ├── domain/
│       │   ├── entities/
│       │   │   └── {feature}.dart
│       │   ├── repositories/
│       │   │   └── {feature}_repository.dart
│       │   └── usecases/
│       │       └── get_{feature}.dart
│       │       └── create_{feature}.dart
│       │       └── delete_{feature}.dart
│       │
│       └── presentation/
│           ├── cubit/
│           │   └── {feature}_cubit.dart
│           │   └── {feature}_state.dart
│           └── pages/
│               └── {feature}_page.dart
│
└── main.dart
```

### 📁 Reglas de Organización

#### ✅ Hacer:
- Una carpeta por feature
- Feature es independiente de otras features
- Core no depende de features
- Cada capa en su carpeta correspondiente

#### ❌ No Hacer:
```
lib/
├── data/           # ❌ Mal: Todos los datos juntos
├── domain/         # ❌ Mal: Todas las entidades juntas
├── ui/             # ❌ Mal: Todas las pantallas juntas
└── models/         # ❌ Mal: Todos los modelos juntos
```

#### ✅ Hacer:
```
lib/
├── features/
│   ├── user/       # ✅ Bien: Todo lo de usuario aquí
│   ├── product/    # ✅ Bien: Todo lo de producto aquí
│   └── order/      # ✅ Bien: Todo lo de orden aquí
└── core/           # ✅ Bien: Solo código compartido
```

---

## Flujo de Datos: La Regla de Dependencia

### 🔄 Diagrama de Flujo Completo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             FLUJO DE DATOS                                  │
└─────────────────────────────────────────────────────────────────────────────┘

   USUARIO
      │
      │ "Toca botón"
      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 1. UI (Widget)                                                             │
│    - Recibe evento del usuario                                             │
│    - Llama a método del Cubit                                              │
│                                                                            │
│    Ejemplo:                                                                │
│    onPressed: () {                                                         │
│      context.read<UserCubit>().fetchUsers();                               │
│    }                                                                       │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 2. PRESENTATION (Cubit)                                                    │
│    - Cambia estado a Loading                                               │
│    - Llama al UseCase                                                      │
│                                                                            │
│    Ejemplo:                                                                │
│    emit(UserLoading());                                                    │
│    final result = await getUsers(NoParams());                              │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 3. DOMAIN (UseCase)                                                        │
│    - Lógica de negocio simple                                              │
│    - Llama al Repository                                                   │
│                                                                            │
│    Ejemplo:                                                                │
│    return await repository.getUsers();                                     │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 4. DOMAIN (Repository Interface)                                           │
│    - Define el contrato                                                    │
│    - No implementa, solo declara                                           │
│                                                                            │
│    Ejemplo:                                                                │
│    Future<Either<Failure, List<User>>> getUsers();                         │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 5. DATA (Repository Implementation)                                        │
│    - Decide fuente de datos (local/remoto)                                 │
│    - Maneja errores                                                        │
│    - Convierte Model → Entity                                              │
│                                                                            │
│    Ejemplo:                                                                │
│    final models = await localDataSource.getUsers();                        │
│    return Right(models.map((m) => m.toEntity()).toList());                 │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 6. DATA (DataSource)                                                       │
│    - Habla directamente con la BD/API                                      │
│    - Devuelve Models                                                       │
│                                                                            │
│    Ejemplo:                                                                │
│    return await hiveBox.values.toList();                                   │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 7. BASE DE DATOS / API                                                     │
│    - Almacena datos físicamente                                            │
│    - O responde peticiones HTTP                                            │
└────────────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════════
                              RETORNO DEL FLUJO
═══════════════════════════════════════════════════════════════════════════════

   BASE DE DATOS
         │
         │ Datos crudos
         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 6. DATA (DataSource)                                                       │
│    - Devuelve Model                                                        │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 5. DATA (Repository)                                                       │
│    - Convierte Model → Entity                                              │
│    - Retorna Either<Failure, Entity>                                       │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 4. DOMAIN (Repository Interface)                                           │
│    - Retorna Either<Failure, Entity>                                       │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 3. DOMAIN (UseCase)                                                        │
│    - Retorna Either<Failure, Entity>                                       │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 2. PRESENTATION (Cubit)                                                    │
│    - Usa fold() para manejar Either                                        │
│    - Emite nuevo estado                                                    │
│                                                                            │
│    Ejemplo:                                                                │
│    result.fold(                                                            │
│      (failure) => emit(UserError('Error')),                                │
│      (users) => emit(UserLoaded(users)),                                   │
│    );                                                                      │
└────────────────────────┬───────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────────────────┐
│ 1. UI (Widget)                                                             │
│    - Se reconstruye con nuevo estado                                       │
│    - Muestra datos o error                                                 │
│                                                                            │
│    Ejemplo:                                                                │
│    BlocBuilder<UserCubit, UserState>(                                      │
│      builder: (context, state) {                                           │
│        if (state is UserLoaded) {                                          │
│          return ListView(...);                                             │
│        }                                                                   │
│      },                                                                    │
│    )                                                                       │
└────────────────────────────────────────────────────────────────────────────┘
```

### 📋 Regla de Dependencia

```
Las flechas de dependencia SIEMPRE apuntan hacia adentro:

    UI → Presentation → Domain → Data

❌ Esto está PROHIBIDO:

    Domain → UI  (Domain NO puede saber de UI)
    Data → Domain implementación (Domain solo interfaces)
    UI → Data directo (Siempre pasar por Presentation y Domain)
```

---

## Template Universal por Capa

### 🎨 TEMPLATE 1: Entity

**Ubicación**: `lib/features/{feature}/domain/entities/{feature}.dart`

```dart
import 'package:equatable/equatable.dart';

/// {Feature} Entity - El objeto de negocio puro
/// 
/// REGLAS:
/// 1. Inmutable (usa const constructor)
/// 2. Extends Equatable (para comparar fácilmente)
/// 3. Lógica de negocio en getters
/// 4. Sin dependencias externas (no Hive, no JSON)
class {Feature} extends Equatable {
  const {Feature}({
    required this.id,
    required this.name,
    this.isActive = true,
    this.createdAt,
  });

  // Campos requeridos
  final String id;
  final String name;
  
  // Campos opcionales con valores por defecto
  final bool isActive;
  final DateTime? createdAt;

  // Lógica de negocio (getters calculados)
  bool get isNew {
    if (createdAt == null) return false;
    final daysSinceCreated = DateTime.now().difference(createdAt!).inDays;
    return daysSinceCreated < 7;
  }

  // Patrón copyWith para inmutabilidad
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

  // Equatable: propiedades para comparación
  @override
  List<Object?> get props => [id, name, isActive, createdAt];

  // Para debugging
  @override
  String toString() => '{Feature}(id: $id, name: $name)';
}
```

### 🎨 TEMPLATE 2: Repository Interface

**Ubicación**: `lib/features/{feature}/domain/repositories/{feature}_repository.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/{feature}/domain/entities/{feature}.dart';

/// Contrato del repositorio
/// 
/// Define QUÉ operaciones se pueden hacer, no CÓMO se hacen
abstract class {Feature}Repository {
  /// Obtiene todos los {features}
  Future<Either<Failure, List<{Feature}>>> getAll();
  
  /// Obtiene un {feature} por ID
  Future<Either<Failure, {Feature}>> getById(String id);
  
  /// Crea un nuevo {feature}
  Future<Either<Failure, void>> create({Feature} {feature});
  
  /// Actualiza un {feature} existente
  Future<Either<Failure, void>> update({Feature} {feature});
  
  /// Elimina un {feature}
  Future<Either<Failure, void>> delete(String id);
}
```

### 🎨 TEMPLATE 3: Model (con Hive)

**Ubicación**: `lib/features/{feature}/data/models/{feature}_model.dart`

```dart
import 'package:hive/hive.dart';
import 'package:my_app/features/{feature}/domain/entities/{feature}.dart';

part '{feature}_model.g.dart';

@HiveType(typeId: X)  // ⚠️ Usar ID único (0, 1, 2, 3...)
class {Feature}Model extends HiveObject {
  {Feature}Model({
    required this.id,
    required this.name,
    this.isActive = true,
    this.createdAt,
  });

  @HiveField(0)
  String id;

  @HiveField(1)
  String name;

  @HiveField(2, defaultValue: true)
  bool isActive;

  @HiveField(3)
  DateTime? createdAt;

  // Model → Entity
  {Feature} toEntity() {
    return {Feature}(
      id: id,
      name: name,
      isActive: isActive,
      createdAt: createdAt,
    );
  }

  // Entity → Model
  factory {Feature}Model.fromEntity({Feature} entity) {
    return {Feature}Model(
      id: entity.id,
      name: entity.name,
      isActive: entity.isActive,
      createdAt: entity.createdAt,
    );
  }

  {Feature}Model copyWith({...}) {...}
}
```

### 🎨 TEMPLATE 4: DataSource

**Ubicación**: `lib/features/{feature}/data/datasources/{feature}_local_data_source.dart`

```dart
import 'package:hive/hive.dart';
import 'package:my_app/features/{feature}/data/models/{feature}_model.dart';

abstract class {Feature}LocalDataSource {
  Future<List<{Feature}Model>> getAll();
  Future<{Feature}Model?> getById(String id);
  Future<void> save({Feature}Model model);
  Future<void> delete(String id);
}

class {Feature}LocalDataSourceImpl implements {Feature}LocalDataSource {
  final Box<{Feature}Model> _box;
  
  {Feature}LocalDataSourceImpl(this._box);
  
  @override
  Future<List<{Feature}Model>> getAll() async {
    return _box.values.toList();
  }
  
  @override
  Future<{Feature}Model?> getById(String id) async {
    return _box.get(id);
  }
  
  @override
  Future<void> save({Feature}Model model) async {
    await _box.put(model.id, model);
  }
  
  @override
  Future<void> delete(String id) async {
    await _box.delete(id);
  }
}
```

### 🎨 TEMPLATE 5: Repository Implementation

**Ubicación**: `lib/features/{feature}/data/repositories/{feature}_repository_impl.dart`

```dart
import 'package:dartz/dartz.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/{feature}/data/datasources/{feature}_local_data_source.dart';
import 'package:my_app/features/{feature}/data/models/{feature}_model.dart';
import 'package:my_app/features/{feature}/domain/entities/{feature}.dart';
import 'package:my_app/features/{feature}/domain/repositories/{feature}_repository.dart';

class {Feature}RepositoryImpl implements {Feature}Repository {
  final {Feature}LocalDataSource _localDataSource;
  
  {Feature}RepositoryImpl({required {Feature}LocalDataSource localDataSource})
      : _localDataSource = localDataSource;
  
  @override
  Future<Either<Failure, List<{Feature}>>> getAll() async {
    try {
      final models = await _localDataSource.getAll();
      final entities = models.map((m) => m.toEntity()).toList();
      return Right(entities);
    } catch (e) {
      return Left(CacheFailure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, void>> create({Feature} {feature}) async {
    try {
      final model = {Feature}Model.fromEntity({feature});
      await _localDataSource.save(model);
      return const Right(null);
    } catch (e) {
      return Left(CacheFailure(e.toString()));
    }
  }
  
  // ... otros métodos
}
```

### 🎨 TEMPLATE 6: UseCase

**Ubicación**: `lib/features/{feature}/domain/usecases/get_{feature}.dart`

```dart
import 'package:dartz/dartz.dart';
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

### 🎨 TEMPLATE 7: Cubit

**Ubicación**: `lib/features/{feature}/presentation/cubit/{feature}_cubit.dart`

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
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
    
    result.fold(
      (failure) => emit({Feature}Error('Error loading')),
      ({feature}) => emit({Feature}Loaded({feature})),
    );
  }
}
```

### 🎨 TEMPLATE 8: Page

**Ubicación**: `lib/features/{feature}/presentation/pages/{feature}_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:my_app/features/{feature}/presentation/cubit/{feature}_cubit.dart';

class {Feature}Page extends StatelessWidget {
  const {Feature}Page({super.key});
  
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => GetIt.I<{Feature}Cubit>(),
      child: Scaffold(
        appBar: AppBar(title: const Text('{Feature}')),
        body: const _{Feature}View(),
      ),
    );
  }
}

class _{Feature}View extends StatelessWidget {
  const _{Feature}View();
  
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<{Feature}Cubit, {Feature}State>(
      builder: (context, state) {
        if (state is {Feature}Loading) {
          return const Center(child: CircularProgressIndicator());
        }
        if (state is {Feature}Loaded) {
          return Text(state.{feature}.name);
        }
        if (state is {Feature}Error) {
          return Text(state.message);
        }
        return const SizedBox.shrink();
      },
    );
  }
}
```

---

## Ejemplo Completo: Sistema de Usuarios

Vamos a implementar un sistema CRUD completo de usuarios usando todos los templates.

### 📋 Requerimientos
1. Crear usuario
2. Ver lista de usuarios
3. Ver detalle de usuario
4. Eliminar usuario

### 🗂️ Estructura de Archivos

```
lib/features/user/
├── data/
│   ├── datasources/
│   │   └── user_local_data_source.dart
│   ├── models/
│   │   ├── user_model.dart
│   │   └── user_model.g.dart
│   └── repositories/
│       └── user_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── user.dart
│   ├── repositories/
│   │   └── user_repository.dart
│   └── usecases/
│       ├── create_user.dart
│       ├── delete_user.dart
│       ├── get_user.dart
│       └── get_users.dart
└── presentation/
    ├── cubit/
    │   ├── user_cubit.dart
    │   └── user_state.dart
    └── pages/
        ├── user_detail_page.dart
        └── users_list_page.dart
```

### 📄 1. Entity

```dart
// lib/features/user/domain/entities/user.dart

import 'package:equatable/equatable.dart';

class User extends Equatable {
  const User({
    required this.id,
    required this.name,
    required this.email,
    this.isActive = true,
    this.createdAt,
    this.avatarUrl,
  });

  final String id;
  final String name;
  final String email;
  final bool isActive;
  final DateTime? createdAt;
  final String? avatarUrl;

  bool get hasAvatar => avatarUrl != null && avatarUrl!.isNotEmpty;

  User copyWith({
    String? id,
    String? name,
    String? email,
    bool? isActive,
    DateTime? createdAt,
    String? avatarUrl,
  }) {
    return User(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      avatarUrl: avatarUrl ?? this.avatarUrl,
    );
  }

  @override
  List<Object?> get props => [id, name, email, isActive, createdAt, avatarUrl];
}
```

### 📄 2. Repository Interface

```dart
// lib/features/user/domain/repositories/user_repository.dart

import 'package:dartz/dartz.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/entities/user.dart';

abstract class UserRepository {
  Future<Either<Failure, List<User>>> getUsers();
  Future<Either<Failure, User>> getUser(String id);
  Future<Either<Failure, void>> createUser(User user);
  Future<Either<Failure, void>> updateUser(User user);
  Future<Either<Failure, void>> deleteUser(String id);
}
```

### 📄 3. Model

```dart
// lib/features/user/data/models/user_model.dart

import 'package:hive/hive.dart';
import 'package:my_app/features/user/domain/entities/user.dart';

part 'user_model.g.dart';

@HiveType(typeId: 5)
class UserModel extends HiveObject {
  UserModel({
    required this.id,
    required this.name,
    required this.email,
    this.isActive = true,
    this.createdAt,
    this.avatarUrl,
  });

  @HiveField(0)
  String id;

  @HiveField(1)
  String name;

  @HiveField(2)
  String email;

  @HiveField(3, defaultValue: true)
  bool isActive;

  @HiveField(4)
  DateTime? createdAt;

  @HiveField(5)
  String? avatarUrl;

  User toEntity() {
    return User(
      id: id,
      name: name,
      email: email,
      isActive: isActive,
      createdAt: createdAt,
      avatarUrl: avatarUrl,
    );
  }

  factory UserModel.fromEntity(User entity) {
    return UserModel(
      id: entity.id,
      name: entity.name,
      email: entity.email,
      isActive: entity.isActive,
      createdAt: entity.createdAt,
      avatarUrl: entity.avatarUrl,
    );
  }
}
```

### 📄 4. DataSource

```dart
// lib/features/user/data/datasources/user_local_data_source.dart

import 'package:hive/hive.dart';
import 'package:my_app/features/user/data/models/user_model.dart';

abstract class UserLocalDataSource {
  Future<List<UserModel>> getUsers();
  Future<UserModel?> getUser(String id);
  Future<void> saveUser(UserModel user);
  Future<void> deleteUser(String id);
}

class UserLocalDataSourceImpl implements UserLocalDataSource {
  final Box<UserModel> _box;
  
  UserLocalDataSourceImpl(this._box);
  
  @override
  Future<List<UserModel>> getUsers() async {
    return _box.values.toList();
  }
  
  @override
  Future<UserModel?> getUser(String id) async {
    return _box.get(id);
  }
  
  @override
  Future<void> saveUser(UserModel user) async {
    await _box.put(user.id, user);
  }
  
  @override
  Future<void> deleteUser(String id) async {
    await _box.delete(id);
  }
}
```

### 📄 5. Repository Implementation

```dart
// lib/features/user/data/repositories/user_repository_impl.dart

import 'package:dartz/dartz.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/data/datasources/user_local_data_source.dart';
import 'package:my_app/features/user/data/models/user_model.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

class UserRepositoryImpl implements UserRepository {
  final UserLocalDataSource _localDataSource;
  
  UserRepositoryImpl({required UserLocalDataSource localDataSource})
      : _localDataSource = localDataSource;
  
  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    try {
      final models = await _localDataSource.getUsers();
      return Right(models.map((m) => m.toEntity()).toList());
    } catch (e) {
      return Left(CacheFailure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final model = await _localDataSource.getUser(id);
      if (model == null) {
        return Left(CacheFailure('User not found'));
      }
      return Right(model.toEntity());
    } catch (e) {
      return Left(CacheFailure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, void>> createUser(User user) async {
    try {
      final model = UserModel.fromEntity(user);
      await _localDataSource.saveUser(model);
      return const Right(null);
    } catch (e) {
      return Left(CacheFailure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, void>> updateUser(User user) async {
    return createUser(user);  // Mismo proceso
  }
  
  @override
  Future<Either<Failure, void>> deleteUser(String id) async {
    try {
      await _localDataSource.deleteUser(id);
      return const Right(null);
    } catch (e) {
      return Left(CacheFailure(e.toString()));
    }
  }
}
```

### 📄 6. UseCases

```dart
// lib/features/user/domain/usecases/get_users.dart

import 'package:dartz/dartz.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

class GetUsers extends UseCase<List<User>, NoParams> {
  final UserRepository repository;
  
  GetUsers(this.repository);
  
  @override
  Future<Either<Failure, List<User>>> call(NoParams params) async {
    return await repository.getUsers();
  }
}
```

```dart
// lib/features/user/domain/usecases/create_user.dart

import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/core/error/failures.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/repositories/user_repository.dart';

class CreateUser extends UseCase<void, CreateUserParams> {
  final UserRepository repository;
  
  CreateUser(this.repository);
  
  @override
  Future<Either<Failure, void>> call(CreateUserParams params) async {
    final user = User(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      name: params.name,
      email: params.email,
      createdAt: DateTime.now(),
    );
    
    return await repository.createUser(user);
  }
}

class CreateUserParams extends Equatable {
  final String name;
  final String email;
  
  const CreateUserParams({required this.name, required this.email});
  
  @override
  List<Object?> get props => [name, email];
}
```

### 📄 7. Cubit

```dart
// lib/features/user/presentation/cubit/user_cubit.dart

import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:my_app/core/common/usecase.dart';
import 'package:my_app/features/user/domain/entities/user.dart';
import 'package:my_app/features/user/domain/usecases/create_user.dart';
import 'package:my_app/features/user/domain/usecases/delete_user.dart';
import 'package:my_app/features/user/domain/usecases/get_users.dart';

part 'user_state.dart';

class UserCubit extends Cubit<UserState> {
  final GetUsers _getUsers;
  final CreateUser _createUser;
  final DeleteUser _deleteUser;
  
  UserCubit({
    required GetUsers getUsers,
    required CreateUser createUser,
    required DeleteUser deleteUser,
  })  : _getUsers = getUsers,
        _createUser = createUser,
        _deleteUser = deleteUser,
        super(UserInitial());
  
  Future<void> loadUsers() async {
    emit(UserLoading());
    
    final result = await _getUsers(NoParams());
    
    result.fold(
      (failure) => emit(UserError('Error loading users')),
      (users) => emit(UsersLoaded(users)),
    );
  }
  
  Future<void> createUser(String name, String email) async {
    emit(UserLoading());
    
    final result = await _createUser(
      CreateUserParams(name: name, email: email),
    );
    
    result.fold(
      (failure) => emit(UserError('Error creating user')),
      (_) {
        emit(const UserOperationSuccess('User created'));
        loadUsers();
      },
    );
  }
  
  Future<void> deleteUser(String userId) async {
    emit(UserLoading());
    
    final result = await _deleteUser(DeleteUserParams(userId));
    
    result.fold(
      (failure) => emit(UserError('Error deleting user')),
      (_) {
        emit(const UserOperationSuccess('User deleted'));
        loadUsers();
      },
    );
  }
}
```

```dart
// lib/features/user/presentation/cubit/user_state.dart

part of 'user_cubit.dart';

abstract class UserState extends Equatable {
  const UserState();
  
  @override
  List<Object?> get props => [];
}

class UserInitial extends UserState {}
class UserLoading extends UserState {}
class UsersLoaded extends UserState {
  final List<User> users;
  const UsersLoaded(this.users);
  
  @override
  List<Object?> get props => [users];
}
class UserError extends UserState {
  final String message;
  const UserError(this.message);
  
  @override
  List<Object?> get props => [message];
}
class UserOperationSuccess extends UserState {
  final String message;
  const UserOperationSuccess(this.message);
  
  @override
  List<Object?> get props => [message];
}
```

### 📄 8. Pages

```dart
// lib/features/user/presentation/pages/users_list_page.dart

import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:get_it/get_it.dart';
import 'package:my_app/features/user/presentation/cubit/user_cubit.dart';

class UsersListPage extends StatelessWidget {
  const UsersListPage({super.key});
  
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => GetIt.I<UserCubit>()..loadUsers(),
      child: Scaffold(
        appBar: AppBar(title: const Text('Users')),
        body: const _UsersListView(),
        floatingActionButton: FloatingActionButton(
          onPressed: () => _showCreateDialog(context),
          child: const Icon(Icons.add),
        ),
      ),
    );
  }
  
  void _showCreateDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => const _CreateUserDialog(),
    );
  }
}

class _UsersListView extends StatelessWidget {
  const _UsersListView();
  
  @override
  Widget build(BuildContext context) {
    return BlocConsumer<UserCubit, UserState>(
      listener: (context, state) {
        if (state is UserOperationSuccess) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message)),
          );
        }
      },
      builder: (context, state) {
        if (state is UserLoading) {
          return const Center(child: CircularProgressIndicator());
        }
        
        if (state is UsersLoaded) {
          if (state.users.isEmpty) {
            return const Center(child: Text('No users yet'));
          }
          
          return ListView.builder(
            itemCount: state.users.length,
            itemBuilder: (context, index) {
              final user = state.users[index];
              return ListTile(
                title: Text(user.name),
                subtitle: Text(user.email),
                trailing: IconButton(
                  icon: const Icon(Icons.delete, color: Colors.red),
                  onPressed: () {
                    context.read<UserCubit>().deleteUser(user.id);
                  },
                ),
              );
            },
          );
        }
        
        if (state is UserError) {
          return Center(child: Text(state.message));
        }
        
        return const SizedBox.shrink();
      },
    );
  }
}
```

---

## Patrones y Decisiones de Diseño

### 🎯 Cuándo usar cada capa

| Situación | ¿Dónde va? | Ejemplo |
|-----------|-----------|---------|
| Validar que email tiene formato correcto | Entity (getter) | `bool get isValidEmail` |
| Guardar en base de datos | DataSource | `await box.put(id, model)` |
| Decidir si uso cache o API | Repository | `if (isConnected) useRemote()` |
| Calcular impuestos | UseCase | `CalculateTaxUseCase` |
| Mostrar indicador de carga | Cubit (State) | `UserLoading()` |
| Navegar a otra pantalla | UI (Widget) | `Navigator.push(...)` |

### 🎯 Decisiones Arquitectónicas Comunes

#### ❓ ¿Entity debe extender de Model?
**Respuesta**: NO. Son responsabilidades diferentes.
- Entity = Lógica de negocio pura
- Model = Serialización técnica

#### ❓ ¿UseCase debe tener solo un método?
**Respuesta**: SÍ, el método `call()`. Cada UseCase hace UNA sola cosa.

#### ❓ ¿Puedo llamar a un UseCase desde otro UseCase?
**Respuesta**: NO. Los UseCases son independientes. Si necesitas composición, crea un nuevo UseCase más alto nivel.

#### ❓ ¿Repository puede tener lógica de negocio?
**Respuesta**: NO. Solo decide fuente de datos y convierte Model ↔ Entity.

#### ❓ ¿Puedo usar el Model en la UI?
**Respuesta**: NO. La UI solo trabaja con Entities. Los Models nunca salen de la capa Data.

---

## Testing por Capas

### ✅ Testing Domain (Fácil)

```dart
// test/domain/entities/user_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/features/user/domain/entities/user.dart';

void main() {
  group('User Entity', () {
    test('should create user with required fields', () {
      // Arrange & Act
      const user = User(id: '1', name: 'John', email: 'john@example.com');
      
      // Assert
      expect(user.id, '1');
      expect(user.name, 'John');
      expect(user.isActive, true);  // Default value
    });
    
    test('should calculate hasAvatar correctly', () {
      const userWithAvatar = User(
        id: '1',
        name: 'John',
        email: 'john@example.com',
        avatarUrl: 'http://example.com/avatar.png',
      );
      
      const userWithoutAvatar = User(
        id: '2',
        name: 'Jane',
        email: 'jane@example.com',
      );
      
      expect(userWithAvatar.hasAvatar, true);
      expect(userWithoutAvatar.hasAvatar, false);
    });
    
    test('copyWith should update only specified fields', () {
      const user = User(id: '1', name: 'John', email: 'john@example.com');
      
      final updated = user.copyWith(name: 'Jane');
      
      expect(updated.id, '1');  // Unchanged
      expect(updated.name, 'Jane');  // Changed
      expect(updated.email, 'john@example.com');  // Unchanged
    });
  });
}
```

### ✅ Testing UseCases (Fácil)

```dart
// test/domain/usecases/get_users_test.dart

import 'package:dartz/dartz.dart';
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
  
  final tUsers = [
    const User(id: '1', name: 'John', email: 'john@example.com'),
  ];
  
  test('should get users from repository', () async {
    // Arrange
    when(() => mockRepository.getUsers())
        .thenAnswer((_) async => Right(tUsers));
    
    // Act
    final result = await useCase(NoParams());
    
    // Assert
    expect(result, Right(tUsers));
    verify(() => mockRepository.getUsers());
    verifyNoMoreInteractions(mockRepository);
  });
}
```

### ✅ Testing Repository (Medio)

```dart
// test/data/repositories/user_repository_impl_test.dart

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
      // Arrange
      when(() => mockDataSource.getUsers())
          .thenAnswer((_) async => tUserModels);
      
      // Act
      final result = await repository.getUsers();
      
      // Assert
      expect(result.isRight(), true);
    });
  });
}
```

---

## Migración desde Código Spaghetti

### 🔄 Estrategia de Migración Gradual

No necesitas reescribir todo de una vez. Migra feature por feature.

#### Paso 1: Aislar una feature
```dart
// Antes: Todo mezclado en un archivo
class UserPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: http.get(Uri.parse('/api/users')),  // ❌ HTTP en UI
      builder: (context, snapshot) {
        // ...
      },
    );
  }
}
```

#### Paso 2: Crear la estructura de carpetas
```
lib/features/user/
├── data/
├── domain/
└── presentation/
```

#### Paso 3: Mover código gradualmente
1. Mueve los modelos JSON a `data/models`
2. Crea las Entities puras en `domain/entities`
3. Extrae la lógica de UI a un Cubit

#### Paso 4: Conectar todo con inyección de dependencias

### 📋 Checklist de Migración

```
□ Feature seleccionada (empezar por la más simple)
□ Estructura de carpetas creada
□ Entity extraída del modelo anterior
□ Repository interface definida
□ DataSource implementado
□ Repository implementation conectado
□ UseCases creados
□ Cubit implementado
□ UI refactorizada para usar Cubit
□ Tests escritos
□ Feature anterior deprecada
```

---

## 🎓 Conclusión

Clean Architecture no es sobre escribir más código, es sobre escribir código **organizado y mantenible**.

### Beneficios a largo plazo:
- ✅ **Testeable**: Puedes testear Domain sin Flutter
- ✅ **Flexible**: Cambiar Hive por SQLite solo toca Data
- ✅ **Escalable**: Nuevos desarrolladores entienden rápido
- ✅ **Robusto**: Errores no propagan a toda la app

### Costos:
- ⏱️ Más archivos (pero organizados)
- ⏱️ Más código boilerplate inicial
- ⏱️ Curva de aprendizaje

### Cuándo NO usar Clean Architecture:
- Prototipos de un día
- Apps muy pequeñas (<5 pantallas)
- Proyectos personales de aprendizaje

### Cuándo SÍ usarla:
- Apps en producción
- Equipos de 2+ personas
- Apps que crecerán en funcionalidades
- Proyectos donde la calidad importa

---

**Recuerda**: La arquitectura perfecta es la que se adapta a tu equipo y proyecto. Clean Architecture es una guía, no una religión. ¡Adáptala a tus necesidades!
