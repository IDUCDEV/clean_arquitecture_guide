---
name: clean-arch-feature
description: Generate a complete Clean Architecture feature scaffold (entity, model, datasource, repository interface + impl, usecases, cubit, state, optional pages) from a feature name and entity fields. Optionally includes Supabase integration (table schema → snake_case model + datasource + SQL migration), initial pages (listener_builder / builder / form patterns) and wiring orchestration (delegates DI registration to di-getit-scaffold and routing to go-route-scaffold). All method bodies are left as throw UnimplementedError() — implementation is the developer's responsibility.
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

## Input opcional (páginas iniciales)

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `pages` | Lista de páginas a generar con su patrón: `{page_name}:{pattern_type}` | `[list:listener_builder, detail:builder, edit:form]` |

Los patrones disponibles son `listener_builder` (default), `builder` y `form`. Ver [Templates de página](#templates-de-página).

**Si se omite:** se genera el placeholder genérico `{feature}_page.dart`.
**Si se proporciona:** se genera una página por entrada: `{feature}_{page_name}_page.dart` con el patrón indicado. El nombre del archivo usa el plural de la feature solo cuando `page_name` es `list` (ej: `orders_list_page.dart`).

## Input opcional (wiring — orquestación)

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `wiring` | Qué wiring aplicar tras generar los archivos: `[di]`, `[router]` o `[di, router]` | `[di, router]` |

Esta skill **no contiene** la lógica de DI ni de rutas: delega en las skills hermanas `di-getit-scaffold` (registro en `service_locator.dart`) y `go-route-scaffold` (rutas en `app_router.dart`). Solo orquesta.

**Si se omite:** no se toca DI ni el router; el asistente recuerda en el resumen final que debe registrarse el feature y añadirse sus rutas.

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
        ├── {feature_name}_page.dart          (placeholder por defecto)
        └── {feature_name}_{page}_page.dart   (uno por entrada en `pages`)
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
// TODO: implementar. Resolver antes de escribir:
//   1) ¿Qué contrato cumple este método? (qué recibe, qué devuelve)
//   2) ¿Qué capa inferior interviene? (datasource, cache, red)
//   3) ¿Qué mapeo entity <-> model aplica?
//   4) ¿Qué puede fallar y cómo se traduce a Failure?
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

### Templates de página (solo si se proporcionó `pages`)

Patrones disponibles (coinciden con los estados del cubit generado: `{Feature}Loading`, `{Feature}sLoaded`, `{Feature}Loaded`, `{Feature}Error`):

| Pattern | Cuándo usarlo |
|---|---|
| `listener_builder` | **Default**. Cualquier página con side effects (snackbars, navegación post-acción). Usa `BlocListener` + `BlocBuilder`. |
| `builder` | Página de solo lectura sin efectos secundarios. Usa solo `BlocBuilder`. |
| `form` | Formulario con validación, controllers, submit loading. Usa `BlocListener` + `BlocBuilder`. |

#### Pattern: listener_builder — BlocListener + BlocBuilder (default)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{app_name}/core/services/snackbar_helper.dart';
import 'package:{app_name}/core/widgets/app_button.dart';
import 'package:{app_name}/features/{feature}/presentation/cubit/{feature}_cubit.dart';

class {Feature}{PageName}Page extends StatefulWidget {
  const {Feature}{PageName}Page({super.key});

  @override
  State<{Feature}{PageName}Page> createState() => _{Feature}{PageName}PageState();
}

class _{Feature}{PageName}PageState extends State<{Feature}{PageName}Page> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<{Feature}Cubit>().load{Feature}s();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('{PageTitle}')),
      body: BlocListener<{Feature}Cubit, {Feature}State>(
        listener: (context, state) {
          // TODO: handle side effects
          // if (state is {Feature}Loaded && state.xxxError != null) {
          //   SnackbarHelper.show(context, state.xxxError!, isSuccess: false);
          //   context.read<{Feature}Cubit>().clearXxxError();
          // }
          // if (state is {Feature}{Action}Success) {
          //   SnackbarHelper.show(context, 'Operación exitosa', isSuccess: true);
          //   context.pop();
          // }
        },
        child: BlocBuilder<{Feature}Cubit, {Feature}State>(
          builder: (context, state) {
            if (state is {Feature}Loading) {
              return const Center(child: CircularProgressIndicator());
            }
            if (state is {Feature}Error) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(state.message, overflow: TextOverflow.ellipsis),
                    const SizedBox(height: 16),
                    AppButton(
                      label: 'Reintentar',
                      onPressed: () => context.read<{Feature}Cubit>().load{Feature}s(),
                      variant: AppButtonVariant.primary,
                    ),
                  ],
                ),
              );
            }
            if (state is {Feature}sLoaded) {
              // TODO: render content
              return const Center(child: Text('Implement {Feature}{PageName} content'));
            }
            return const Center(child: CircularProgressIndicator());
          },
        ),
      ),
    );
  }

  void _refresh() {
    context.read<{Feature}Cubit>().load{Feature}s();
  }
}
```

#### Pattern: builder — BlocBuilder (solo lectura)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{app_name}/core/widgets/app_button.dart';
import 'package:{app_name}/features/{feature}/presentation/cubit/{feature}_cubit.dart';

class {Feature}{PageName}Page extends StatelessWidget {
  const {Feature}{PageName}Page({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('{PageTitle}')),
      body: BlocBuilder<{Feature}Cubit, {Feature}State>(
        builder: (context, state) {
          if (state is {Feature}Loading) {
            return const Center(child: CircularProgressIndicator());
          }
          if (state is {Feature}Loaded) {
            // TODO: render content
            return const Center(child: Text('Implement {Feature}{PageName} content'));
          }
          if (state is {Feature}Error) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(state.message, overflow: TextOverflow.ellipsis),
                  const SizedBox(height: 16),
                  AppButton(
                    label: 'Reintentar',
                    onPressed: () => context.read<{Feature}Cubit>().load{Feature}s(),
                    variant: AppButtonVariant.primary,
                  ),
                ],
              ),
            );
          }
          return const Center(child: CircularProgressIndicator());
        },
      ),
    );
  }
}
```

#### Pattern: form — Formulario con validación

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{app_name}/core/services/snackbar_helper.dart';
import 'package:{app_name}/core/widgets/app_button.dart';
import 'package:{app_name}/features/{feature}/presentation/cubit/{feature}_cubit.dart';

class {Feature}{PageName}Page extends StatefulWidget {
  const {Feature}{PageName}Page({super.key});

  @override
  State<{Feature}{PageName}Page> createState() => _{Feature}{PageName}PageState();
}

class _{Feature}{PageName}PageState extends State<{Feature}{PageName}Page> {
  final _formKey = GlobalKey<FormState>();

  // TODO: declare TextEditingController for each field
  // late final TextEditingController _nameController;

  @override
  void initState() {
    super.initState();
    // TODO: initialize controllers
    // _nameController = TextEditingController(text: initialValue);
  }

  @override
  void dispose() {
    // TODO: dispose controllers
    // _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('{PageTitle}')),
      body: BlocListener<{Feature}Cubit, {Feature}State>(
        listener: (context, state) {
          // TODO: handle success / error side effects
          // if (state is {Feature}{Action}Success) {
          //   SnackbarHelper.show(context, 'Guardado exitoso', isSuccess: true);
          //   context.pop();
          // }
          // if (state is {Feature}Error) {
          //   SnackbarHelper.show(context, state.message, isSuccess: false);
          // }
        },
        child: BlocBuilder<{Feature}Cubit, {Feature}State>(
          builder: (context, state) {
            final isLoading = state is {Feature}Loading;

            return SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // TODO: TextFormField for each field
                    // TextFormField(
                    //   controller: _nameController,
                    //   decoration: const InputDecoration(labelText: 'Name'),
                    //   validator: (v) => v?.isEmpty == true ? 'Required' : null,
                    // ),
                    const SizedBox(height: 24),
                    AppButton(
                      label: 'Guardar',
                      onPressed: isLoading ? null : _submit,
                      variant: AppButtonVariant.primary,
                      isLoading: isLoading,
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  void _submit() {
    // TODO: implement submit
    // if (_formKey.currentState!.validate()) {
    //   context.read<{Feature}Cubit>().create{Feature}(
    //     {Feature}(
    //       name: _nameController.text,
    //       // ... more fields
    //     ),
    //   );
    // }
  }
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
3. Preguntar opcionalmente: páginas iniciales deseadas (`pages`) con sus patrones — si se omiten, generar el placeholder genérico
4. Preguntar opcionalmente: wiring deseado (`[di]`, `[router]` o `[di, router]`)
5. Generar cada archivo siguiendo los templates de arriba
6. Si se proporcionó Supabase: generar además migración SQL con CREATE TABLE + índices + RLS
7. Si se proporcionó `pages`: generar una página por entrada con el template de su patrón
8. Si se proporcionó `wiring` con `di`: invocar la skill `di-getit-scaffold` pasándole los componentes generados (datasources, repositorios, usecases, cubit, estado) para que actualice `service_locator.dart`. No escribir la lógica de DI aquí — delegar.
9. Si se proporcionó `wiring` con `router`: invocar la skill `go-route-scaffold` pasándole las páginas generadas para que actualice `app_router.dart`. No escribir la lógica de rutas aquí — delegar.
10. No generar bodies de métodos — usar `throw UnimplementedError()`
11. Mostrar resumen de archivos creados al final
12. Recordar al usuario que debe: implementar bodies, revisar RLS policies si aplica, ejecutar migración en Supabase, y ejecutar `flutter pub get` si añadió nuevos paquetes
