---
name: flutter-test-generator
description: Generate Flutter unit test boilerplate for Clean Architecture layers. Detects entity, usecase, model, datasource, repository, cubit, state, widget and generates test file with mocktail + blocTest + fpdart boilerplate. Only generates scaffold — never implementation bodies.
---

# flutter-test-generator

Generates test boilerplate from Dart source files, auto-detecting the Clean Architecture layer.

## Script

- **Script:** `generate_test.py` (same directory)
- **Dependencies:** Python 3 (stdlib only)

## Usage

```bash
python3 skills/flutter-test-generator/generate_test.py lib/features/<feature>/<layer>/<file>.dart
```

### Examples

```bash
python3 skills/flutter-test-generator/generate_test.py lib/features/auth/domain/usecases/login_usecase.dart
python3 skills/flutter-test-generator/generate_test.py lib/features/product/data/models/product_model.dart
python3 skills/flutter-test-generator/generate_test.py lib/features/product/presentation/cubit/product_cubit.dart
```

### Output

Creates the `_test.dart` file mirroring the source path under `test/`:
- `lib/features/auth/domain/usecases/login_usecase.dart` → `test/features/auth/domain/usecases/login_usecase_test.dart`

## Layers detected automatically

| Path pattern | Template generated |
|---|---|
| `domain/entities/` | Entity tests (Equatable, copyWith, props) |
| `domain/usecases/` | UseCase tests (mock repository, Either<Failure, T>) |
| `data/models/` | Model tests (fromJson, toJson, roundtrip, entity conversion) |
| `data/datasources/` | DataSource tests (mock client, ServerException) |
| `data/repositories/` | Repository tests (mock datasources + network, online/offline) |
| `presentation/cubit/` (not state) | Cubit tests (blocTest, mock usecases) |
| `presentation/cubit/` (state file) | State tests (equality, props) |
| `presentation/pages/` or `presentation/widgets/` | Widget tests (testWidgets, mock BlocProvider) |
| `core/` | Core service/network/error tests |

## Conventions

- `flutter_test` + `mocktail` + `bloc_test` + `fpdart`
- Estructura AAA (Arrange-Act-Assert) con comentarios en español
- Mocks generados automáticamente desde el constructor
- Bodies de tests vacíos con comentarios — **el desarrollador completa la lógica**

## Workflow

1. Usuario indica archivo(s) a testear
2. Ejecutar `generate_test.py` para cada archivo fuente
3. Preguntar si quiere completar los tests — **nunca implementar bodies sin autorización**
4. Si autoriza, leer fuente + test generado y escribir implementaciones
5. Verificar con `flutter test <path>`
