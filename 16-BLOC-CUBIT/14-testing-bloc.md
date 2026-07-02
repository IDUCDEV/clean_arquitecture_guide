# 14. Testing de BLoC / Cubit

> **Ver también**: `05-TESTING/04a-practica-cubits-bloc-test.md` — ejercicio hands-on de blocTest con AuthCubit + Mocktail (complemento práctico).
> `01-CLEAN-ARCHITECTURE/07-testing-por-capas.md` — testing de Cubit en contexto de Clean Architecture.

> Referencia oficial: [bloclibrary.dev/testing/](https://bloclibrary.dev/testing/)
> API: [blocTest](https://pub.dev/documentation/bloc_test/latest/bloc_test/blocTest.html)

## Dependencias

```yaml
dev_dependencies:
  bloc_test: ^10.0.0
  mocktail: ^1.0.0
```

## Estructura de test

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockRepo extends Mock implements ProductoRepository {}

void main() {
  late ProductoBloc bloc;
  late MockRepo repo;

  setUp(() {
    repo = MockRepo();
    bloc = ProductoBloc(repo: repo);
  });

  tearDown(() {
    bloc.close();
  });

  group('ProductoBloc', () {
    // tests aquí
  });
}
```

## blocTest básico

```dart
blocTest<ProductoBloc, ProductoState>(
  'emite [Loading, Loaded] cuando la carga es exitosa',
  build: () {
    when(() => repo.obtenerTodo())
        .thenAnswer((_) async => Right([producto1, producto2]));
    return ProductoBloc(repo: repo);
  },
  act: (bloc) => bloc.add(CargarProductos()),
  expect: () => [
    const ProductoLoading(),
    ProductoLoaded(items: [producto1, producto2]),
  ],
);

blocTest<ProductoBloc, ProductoState>(
  'emite [Loading, Error] cuando falla la carga',
  build: () {
    when(() => repo.obtenerTodo())
        .thenAnswer((_) async => Left(ServerFailure('Error de red')));
    return ProductoBloc(repo: repo);
  },
  act: (bloc) => bloc.add(CargarProductos()),
  expect: () => [
    const ProductoLoading(),
    const ProductoError('Error de red'),
  ],
);
```

## seed: estado inicial personalizado

```dart
blocTest<ContadorCubit, int>(
  'emite 11 cuando se incrementa desde 10',
  build: () => ContadorCubit(),
  seed: () => 10, // estado inicial artificial
  act: (cubit) => cubit.incrementar(),
  expect: () => [11],
);
```

## skip: saltar estados

```dart
blocTest<ContadorCubit, int>(
  'emite [3] después de 3 incrementos, saltando los primeros 2',
  build: () => ContadorCubit(),
  act: (cubit) {
    cubit.incrementar(); // 1
    cubit.incrementar(); // 2
    cubit.incrementar(); // 3
  },
  skip: 2,
  expect: () => [3],
);
```

## verify: verificar interacciones

```dart
blocTest<LoginCubit, LoginState>(
  'llama al repositorio con email y password',
  build: () {
    when(() => repo.login(any(), any()))
        .thenAnswer((_) async => Right(user));
    return LoginCubit(repo: repo);
  },
  act: (cubit) => cubit.login('a@b.com', '123456'),
  verify: (_) {
    verify(() => repo.login('a@b.com', '123456')).called(1);
  },
);
```

## errors: verificar errores del bloc

```dart
blocTest<MiBloc, MiState>(
  'lanza error cuando el evento es inválido',
  build: () => MiBloc(),
  act: (bloc) => bloc.add(EventoInvalido()),
  errors: () => [isA<ArgumentError>()],
);
```

## wait: esperar operaciones asíncronas

```dart
blocTest<BuscadorBloc, BuscadorState>(
  'emite resultados después del debounce',
  build: () {
    when(() => repo.buscar(any()))
        .thenAnswer((_) async => [producto]);
    return BuscadorBloc(repo: repo);
  },
  act: (bloc) => bloc.add(QueryCambiada('flutter')),
  wait: const Duration(milliseconds: 500), // espera debounce
  expect: () => [
    const BuscadorLoading(),
    BuscadorCompletada([producto]),
  ],
);
```

## setUp y tearDown

```dart
late AuthCubit cubit;
late MockAuthRepo repo;

setUp(() {
  repo = MockAuthRepo();
  cubit = AuthCubit(repo: repo);
});

tearDown(() {
  cubit.close();
});

// Para setup común entre tests
// Usa setUpAll si el setup es costoso
setUpAll(() {
  registerFallbackValue(LoginParams(email: '', password: ''));
});
```

## Matchers comunes

```dart
expect: () => [
  // Igualdad exacta
  ProductoLoaded(items: [producto1]),

  // Pattern matching (no importan los valores)
  isA<ProductoLoaded>(),

  // Con propiedades específicas
  isA<ProductoLoaded>().having(
    (s) => s.items.length,
    'length',
    greaterThan(0),
  ),
],
```

## Test de HydratedCubit

```dart
void main() {
  late FavoritoCubit cubit;

  setUp(() {
    HydratedBloc.storage = MockHydratedStorage();
    cubit = FavoritoCubit();
  });

  tearDown(() => cubit.close());

  blocTest<FavoritoCubit, FavoritoState>(
    'persiste estado al hacer toggle',
    build: () => cubit,
    act: (cubit) => cubit.toggle(producto1),
    verify: (_) {
      verify(() => HydratedBloc.storage.write(any(), any())).called(1);
    },
  );

  blocTest<FavoritoCubit, FavoritoState>(
    'restaura estado desde JSON',
    build: () {
      when(() => HydratedBloc.storage.read(any())).thenReturn({
        'items': [producto1.toJson()],
      });
      return FavoritoCubit();
    },
    expect: () => [FavoritoState([producto1])],
  );
}
```

## Buenas prácticas

- Un archivo de test por cada bloc/cubit
- Usa `group` para organizar por método/evento
- Mockea solo el repositorio, no el bloc
- No tests de UI aquí (esos van en `flutter_test`)
- Usa `blocTest` en lugar de `test` + `listen` manual

## Checklist de testing

- [ ] Estado inicial correcto
- [ ] Emisiones exitosas
- [ ] Emisiones de error
- [ ] Comportamiento con seed
- [ ] Interacciones con repositorio (verify)
- [ ] Transformers de concurrencia
- [ ] Limpieza en dispose/close
- [ ] Persistencia (HydratedCubit)
