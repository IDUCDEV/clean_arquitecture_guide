---
name: clean-arch-feature
description: Generate a complete Clean Architecture feature scaffold (entity, model, datasource, repository interface + impl, usecases, cubit, state, page) from a feature name and entity fields. Optionally includes Supabase integration (table schema → snake_case model + datasource + SQL migration). All method bodies are left as throw UnimplementedError() — implementation is the developer's responsibility.
---

# clean-arch-feature — Scaffold completo de feature

Genera la estructura completa de carpetas y archivos para una feature siguiendo Clean Architecture + Supabase + Cubit. Si proporcionas datos de tabla Supabase, genera además el mapeo snake_case, datasource con `SupabaseClient`, y migración SQL.

## Input requerido

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `feature_name` | Nombre en snake_case | `product`, `user_profile` |
| `fields` | Lista de campos con nombre y tipo Dart | `id: String`, `name: String`, `price: double`, `categoryId: String?` |
| `operations` | CRUD a generar | `getAll`, `getById`, `create`, `update`, `delete` |

## Input opcional (Supabase)

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `table_name` | Nombre de la tabla en Supabase (snake_case) | `orders` |
| `columns` | Columnas Postgres (nombre + tipo + constraints) | `id: uuid PK`, `user_id: uuid NOT NULL`, `status: text DEFAULT 'pending'`, `created_at: timestamptz DEFAULT now()` |

**Si se omite:** se genera el esqueleto genérico (model sin mapeo snake_case, datasource sin `_tableName`, sin migración SQL).
**Si se proporciona:** se genera model con snake_case real, datasource con `_tableName` + `watchById`, y `supabase/migrations/{timestamp}_create_{table}.sql`.

## Reglas de mapeo Postgres → Dart

| Postgres | Dart | Nullable |
|---|---|---|
| `uuid` | `String` | `?` si nullable |
| `text` / `varchar` | `String` | `?` si nullable |
| `int4` / `int8` | `int` | `?` si nullable |
| `float4` / `float8` / `numeric` | `double` | `?` si nullable |
| `bool` | `bool` | `?` si nullable |
| `timestamptz` / `timestamp` | `DateTime` | `?` si nullable |
| `jsonb` | `Map<String, dynamic>` | `?` si nullable |
| `date` | `DateTime` | `?` si nullable |
| `int8[]` | `List<int>` | `?` si nullable |
| `text[]` | `List<String>` | `?` si nullable |

Snake_case en JSON/Postgres → camelCase en Dart: `created_at` → `createdAt`, `user_id` → `userId`.

## Output: estructura generada

### Sin Supabase
```
lib/features/{feature_name}/
├── data/
│   ├── datasources/
│   │   └── {feature_name}_remote_datasource.dart
│   ├── models/
│   │   └── {feature_name}_model.dart
│   └── repositories/
│       └── {feature_name}_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── {feature_name}.dart
│   ├── repositories/
│   │   └── {feature_name}_repository.dart
│   └── usecases/
│       ├── get_{feature_name}s.dart
│       ├── get_{feature_name}.dart
│       ├── create_{feature_name}.dart
│       ├── update_{feature_name}.dart
│       └── delete_{feature_name}.dart
└── presentation/
    ├── cubit/
    │   ├── {feature_name}_cubit.dart
    │   └── {feature_name}_state.dart
    └── pages/
        └── {feature_name}_page.dart
```

### Con Supabase (archivos adicionales)
```
supabase/
└── migrations/
    └── {timestamp}_create_{table}.sql
```

Además, los archivos `model.dart` y `remote_datasource.dart` se generan con mapeo snake_case y `_tableName`.

## Templates generados

### Entity (`domain/entities/{feature}.dart`)

```dart
import 'package:equatable/equatable.dart';

class {Feature} extends Equatable {
  const {Feature}({
    required this.id,
{fields_required_ctor}
  });

{fields_declarations}

  @override
  List<Object?> get props => [{fields_props}];

  {Feature} copyWith({
    {fields_copywith_params}
  }) {
    return {Feature}(
      {fields_copywith_body}
    );
  }

  @override
  String toString() => '{Feature}({fields_tostring})';
}
```

### Repository interface (`domain/repositories/{feature}_repository.dart`)

```dart
import 'package:fpdart/fpdart.dart';
import 'package:{app_name}/core/error/failures.dart';
import 'package:{app_name}/features/{feature}/domain/entities/{feature}.dart';

abstract class {Feature}Repository {
{methods_repository_interface}
}
```

### Model (`data/models/{feature}_model.dart`)

**Sin Supabase** (mapeo genérico):
```dart
import 'package:{app_name}/features/{feature}/domain/entities/{feature}.dart';

class {Feature}Model extends {Feature} {
  const {Feature}Model({super fields});

  factory {Feature}Model.fromJson(Map<String, dynamic> json) {
    return {Feature}Model(
{fields_fromjson}
    );
  }

  Map<String, dynamic> toJson() => {
{fields_tojson}
  };

  factory {Feature}Model.fromEntity({Feature} entity) {
    return {Feature}Model(
{fields_fromentity}
    );
  }

  {Feature} toEntity() => {Feature}(
{fields_toentity}
  );
}
```

**Con Supabase** (mapeo snake_case): igual estructura pero los placeholders `{fields_fromjson}`, `{fields_tojson}` usan claves snake_case (`user_id`, `created_at`) en lugar de camelCase.

### Remote DataSource (`data/datasources/{feature}_remote_datasource.dart`)

**Sin Supabase** (genérico):
```dart
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:{app_name}/core/error/exceptions.dart';
import 'package:{app_name}/features/{feature}/data/models/{feature}_model.dart';

abstract class {Feature}RemoteDataSource {
{methods_datasource_abstract}
}

class {Feature}RemoteDataSourceImpl implements {Feature}RemoteDataSource {
  final SupabaseClient _supabase;

  {Feature}RemoteDataSourceImpl({required SupabaseClient supabase})
      : _supabase = supabase;

{methods_datasource_impl}
}
```

**Con Supabase** (igual + `_tableName` + `watchById`):
```dart
import 'dart:async';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:{app_name}/core/error/exceptions.dart';
import 'package:{app_name}/features/{feature}/data/models/{feature}_model.dart';

abstract class {Feature}RemoteDataSource {
{methods_datasource_abstract}
  Stream<{Feature}Model> watchById(String id);
}

class {Feature}RemoteDataSourceImpl implements {Feature}RemoteDataSource {
  final SupabaseClient _supabase;
  final String _tableName = '{table_name}';

  {Feature}RemoteDataSourceImpl({required SupabaseClient supabase})
      : _supabase = supabase;

{methods_datasource_impl}

  @override
  Stream<{Feature}Model> watchById(String id) {
    throw UnimplementedError('{Feature}RemoteDataSource.watchById');
  }
}
```

### Repository Impl (`data/repositories/{feature}_repository_impl.dart`)

```dart
import 'package:fpdart/fpdart.dart';
import 'package:{app_name}/core/error/failures.dart';
import 'package:{app_name}/core/error/exceptions.dart';
import 'package:{app_name}/features/{feature}/domain/entities/{feature}.dart';
import 'package:{app_name}/features/{feature}/domain/repositories/{feature}_repository.dart';
import 'package:{app_name}/features/{feature}/data/datasources/{feature}_remote_datasource.dart';

class {Feature}RepositoryImpl implements {Feature}Repository {
  final {Feature}RemoteDataSource remoteDataSource;

  {Feature}RepositoryImpl({required this.remoteDataSource});

{methods_repository_impl}
}
```

**Patrón esperado por método:**
```dart
// try {
//   final models = await remoteDataSource.getAll();
//   return Right(models.map((m) => m.toEntity()).toList());
// } on ServerException catch (e) {
//   return Left(ServerFailure(e.message));
// } on CacheException catch (e) {
//   return Left(CacheFailure(e.message));
// }
```

### UseCases (`domain/usecases/{action}_{feature}.dart`)

```dart
import 'package:fpdart/fpdart.dart';
import 'package:{app_name}/core/common/usecase.dart';
import 'package:{app_name}/core/error/failures.dart';
import 'package:{app_name}/features/{feature}/domain/entities/{feature}.dart';
import 'package:{app_name}/features/{feature}/domain/repositories/{feature}_repository.dart';

class {Action}{Feature} extends UseCase<{ReturnType}, {Action}{Feature}Params> {
  final {Feature}Repository repository;

  {Action}{Feature}(this.repository);

  @override
  Future<Either<Failure, {ReturnType}>> call({Action}{Feature}Params params) async {
    throw UnimplementedError('{Action}{Feature}.call');
  }
}

class {Action}{Feature}Params extends Equatable {
{params_fields}

  const {Action}{Feature}Params({params_ctor});

  @override
  List<Object?> get props => [{params_props}];
}
```

### Cubit + State (`presentation/cubit/{feature}_cubit.dart`)

```dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:{app_name}/core/common/usecase.dart';
import 'package:{app_name}/features/{feature}/domain/entities/{feature}.dart';
import 'package:{app_name}/features/{feature}/domain/usecases/get_{feature}s.dart';
import 'package:{app_name}/features/{feature}/domain/usecases/get_{feature}.dart';
import 'package:{app_name}/features/{feature}/domain/usecases/create_{feature}.dart';
import 'package:{app_name}/features/{feature}/domain/usecases/delete_{feature}.dart';

part '{feature}_state.dart';

class {Feature}Cubit extends Cubit<{Feature}State> {
  final Get{Feature}s _get{Feature}s;
  final Get{Feature} _get{Feature};
  final Create{Feature} _create{Feature};
  final Delete{Feature} _delete{Feature};

  {Feature}Cubit({
    required Get{Feature}s get{Feature}s,
    required Get{Feature} get{Feature},
    required Create{Feature} create{Feature},
    required Delete{Feature} delete{Feature},
  })  : _get{Feature}s = get{Feature}s,
        _get{Feature} = get{Feature},
        _create{Feature} = create{Feature},
        _delete{Feature} = delete{Feature},
        super({Feature}Initial());

{cubit_methods}

  void clearError() {
    // TODO: optional — emit copy of previous state without error
  }
}
```

### State (`presentation/cubit/{feature}_state.dart`)

```dart
part of '{feature}_cubit.dart';

sealed class {Feature}State extends Equatable {
  const {Feature}State();

  @override
  List<Object?> get props => [];
}

final class {Feature}Initial extends {Feature}State {}

final class {Feature}Loading extends {Feature}State {}

final class {Feature}sLoaded extends {Feature}State {
  final List<{Feature}> {feature}s;
  const {Feature}sLoaded(this.{feature}s);

  @override
  List<Object?> get props => [{feature}s];
}

final class {Feature}Loaded extends {Feature}State {
  final {Feature} {feature};
  const {Feature}Loaded(this.{feature});

  @override
  List<Object?> get props => [{feature}];
}

final class {Feature}Error extends {Feature}State {
  final String message;
  const {Feature}Error(this.message);

  @override
  List<Object?> get props => [message];
}
```

### Migración SQL (solo si se proporcionó `table_name` + `columns`)

```
supabase/migrations/{timestamp}_create_{table}.sql
```

```sql
-- Create {table_name} table
-- Review and customize before applying

CREATE TABLE {table_name} (
{columns_sql_definitions}
);

-- Indexes
{indexes_sql}

-- Enable Row Level Security
ALTER TABLE {table_name} ENABLE ROW LEVEL SECURITY;

-- RLS Policies (customize per business rules)
{default_rls_policies}

-- Triggers
{triggers_sql}
```

#### Default RLS policies generados

```sql
-- Allow read access to authenticated users
CREATE POLICY "Users can read {table_name}"
  ON {table_name}
  FOR SELECT
  TO authenticated
  USING (true);

-- Allow insert for authenticated users
CREATE POLICY "Users can insert {table_name}"
  ON {table_name}
  FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Allow update for own records
CREATE POLICY "Users can update own {table_name}"
  ON {table_name}
  FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id);
```

## Workflow

1. Preguntar al usuario: feature name, lista de campos (nombre + tipo Dart), operaciones CRUD deseadas, y nombre del paquete (app name)
2. Preguntar opcionalmente: table_name y columnas Postgres si desea integración Supabase
3. Generar cada archivo siguiendo los templates de arriba
4. Si se proporcionó Supabase: generar además migración SQL con CREATE TABLE + índices + RLS
5. No generar bodies de métodos — usar `throw UnimplementedError()`
6. Mostrar resumen de archivos creados al final
7. Recordar al usuario que debe: implementar bodies, registrar en DI, revisar RLS policies si aplica, ejecutar migración en Supabase, y ejecutar `flutter pub get` si añadió nuevos paquetes
