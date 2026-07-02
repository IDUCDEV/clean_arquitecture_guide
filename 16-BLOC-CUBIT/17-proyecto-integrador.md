# 17. Proyecto Integrador: App E-Commerce con BLoC

Una app funcional de e-commerce que integra BLoC, Clean Architecture, navegación, persistencia y testing. El código completo de cada archivo está en los capítulos anteriores; aquí se muestra la arquitectura final.

## Funcionalidad

- Login con validación y persistencia de sesión
- Lista de productos con búsqueda, filtros y paginación
- Favoritos persistidos (HydratedCubit)
- Carrito de compras persistido
- Detalle de producto
- Perfil de usuario

## Arquitectura final

```
lib/
├── main.dart
├── app.dart
├── core/
│   ├── di/
│   │   └── injection_container.dart (GetIt)
│   ├── theme/
│   │   └── app_theme.dart (TemaCubit → Hydrated)
│   └── widgets/
│       ├── app_error.dart
│       ├── app_loading.dart
│       └── app_empty.dart
├── features/
│   ├── auth/
│   │   ├── data/...
│   │   ├── domain/...
│   │   └── presentation/
│   │       ├── cubit/
│   │       │   ├── auth_cubit.dart
│   │       │   └── auth_state.dart
│   │       └── pages/
│   │           ├── login_page.dart
│   │           └── registro_page.dart
│   ├── productos/
│   │   ├── data/...
│   │   ├── domain/...
│   │   └── presentation/
│   │       ├── bloc/
│   │       │   ├── producto_bloc.dart
│   │       │   ├── producto_event.dart
│   │       │   └── producto_state.dart
│   │       ├── pages/
│   │       │   ├── producto_lista_page.dart
│   │       │   └── producto_detalle_page.dart
│   │       └── widgets/
│   │           └── producto_card.dart
│   ├── carrito/
│   │   └── presentation/
│   │       ├── cubit/
│   │       │   ├── carrito_cubit.dart (HydratedCubit)
│   │       │   └── carrito_state.dart
│   │       ├── pages/
│   │       │   └── carrito_page.dart
│   │       └── widgets/
│   │           └── carrito_badge.dart
│   ├── favoritos/
│   │   └── presentation/
│   │       ├── cubit/
│   │       │   ├── favorito_cubit.dart (HydratedCubit)
│   │       │   └── favorito_state.dart
│   │       ├── pages/
│   │       │   └── favoritos_page.dart
│   │       └── widgets/
│   │           └── boton_favorito.dart
│   └── perfil/
│       └── presentation/
│           ├── cubit/
│           │   ├── perfil_cubit.dart
│           │   └── perfil_state.dart
│           └── pages/
│               └── perfil_page.dart
```

## App shell con MultiBlocProvider

```dart
// app.dart
class EcommerceApp extends StatelessWidget {
  EcommerceApp({super.key});

  final _router = GoRouter(
    initialLocation: '/',
    redirect: (context, state) {
      final auth = context.read<AuthCubit>().state;
      final estaAutenticado = auth is AuthAuthenticated;
      final estaEnLogin = state.matchedLocation == '/login';

      if (!estaAutenticado && !estaEnLogin) return '/login';
      if (estaAutenticado && estaEnLogin) return '/';
      return null;
    },
    routes: [
      GoRoute(path: '/login', builder: (_, __) => const LoginPage()),
      GoRoute(
        path: '/',
        builder: (_, __) => const ProductosPage(),
      ),
      GoRoute(
        path: '/productos/:id',
        builder: (_, s) => ProductoDetallePage(
          id: s.pathParameters['id']!,
        ),
      ),
      GoRoute(path: '/carrito', builder: (_, __) => const CarritoPage()),
      GoRoute(path: '/favoritos', builder: (_, __) => const FavoritosPage()),
      GoRoute(path: '/perfil', builder: (_, __) => const PerfilPage()),
    ],
  );

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => getIt<AuthCubit>()),
        BlocProvider(create: (_) => TemaCubit()),
        BlocProvider(create: (_) => FavoritoCubit()),
        BlocProvider(create: (_) => CarritoCubit()),
      ],
      child: BlocBuilder<TemaCubit, TemaState>(
        builder: (context, tema) {
          return MaterialApp.router(
            title: 'E-Commerce BLoC',
            theme: AppTheme.light,
            darkTheme: AppTheme.dark,
            themeMode: tema is TemaOscuro ? ThemeMode.dark : ThemeMode.light,
            routerConfig: _router,
          );
        },
      ),
    );
  }
}
```

## main.dart

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // HydratedBloc persistencia
  final storage = await HydratedStorage.build(
    storageDirectory: await getApplicationDocumentsDirectory(),
  );
  HydratedBloc.storage = storage;

  // BlocObserver global
  Bloc.observer = AppBlocObserver();

  // Inyección de dependencias
  await configureDependencies();

  runApp(const EcommerceApp());
}
```

## Flujo de datos completo

```
LoginPage
  ↓ usuario tapa "Ingresar"
AuthCubit.login(email, password)
  ↓ llama al UseCase
LoginUseCase.execute(email, password)
  ↓ llama al Repository
AuthRepositoryImpl.login(email, password)
  ↓ llama al DataSource
AuthRemoteDataSource.login(email, password)
  → Supabase API /auth/v1/token?grant_type=password
  ↓ respuesta
  ← User + token
AuthCubit emite AuthAuthenticated(user)
  ↓ GoRouter redirect detecta autenticación
  → Navega a "/"
  ↓
ProductosPage
  ProductoBloc recibe CargarProductos
  → ProductoLoading
  → ProductoLoaded
  ↓ usuario selecciona producto
  → /productos/:id
ProductoDetallePage
  ↓ usuario tapa ♥
FavoritoCubit.toggle(producto)
  → FavoritoState([...productos])
  → HydratedBloc escribe al disco
```

## Testing integrado

```dart
// test/features/productos/bloc/producto_bloc_test.dart
void main() {
  late ProductoBloc bloc;
  late MockProductoRepo repo;

  setUp(() {
    repo = MockProductoRepo();
    bloc = ProductoBloc(repo: repo);
  });

  tearDown(() => bloc.close());

  group('CargarProductos', () {
    blocTest<ProductoBloc, ProductoState>(
      'emite [Loading, Loaded] exitosamente',
      build: () {
        when(() => repo.obtenerTodo(page: 1, limit: 20))
            .thenAnswer((_) async => Right([producto1, producto2]));
        return bloc;
      },
      act: (bloc) => bloc.add(const CargarProductos()),
      expect: () => [
        const ProductoLoading(),
        ProductoLoaded(items: [producto1, producto2]),
      ],
    );

    blocTest<ProductoBloc, ProductoState>(
      'emite [Loading, Error] al fallar',
      build: () {
        when(() => repo.obtenerTodo(page: 1, limit: 20))
            .thenAnswer((_) async => Left(ServerFailure('Error')));
        return bloc;
      },
      act: (bloc) => bloc.add(const CargarProductos()),
      expect: () => [
        const ProductoLoading(),
        const ProductoError('Error'),
      ],
    );
  });

  group('CargarMas (pagina con droppable)', () {
    blocTest<ProductoBloc, ProductoState>(
      'agrega items a la lista existente',
      build: () {
        when(() => repo.obtenerTodo(page: 2, limit: 20))
            .thenAnswer((_) async => Right([producto3]));
        return bloc;
      },
      seed: () => ProductoLoaded(items: [producto1, producto2], hasMore: true),
      act: (bloc) => bloc.add(const CargarMas()),
      expect: () => [
        ProductoLoaded(
          items: [producto1, producto2, producto3],
          hasMore: false,
          isLoadingMore: false,
        ),
      ],
    );
  });

  group('BuscarProducto (con debounce + restartable)', () {
    blocTest<ProductoBloc, ProductoState>(
      'emite search result',
      build: () {
        when(() => repo.buscar('test'))
            .thenAnswer((_) async => Right([producto1]));
        return bloc;
      },
      act: (bloc) => bloc.add(const BuscarProducto('test')),
      wait: const Duration(milliseconds: 500),
      expect: () => [
        const ProductoLoading(),
        ProductoSearchResult(items: [producto1], query: 'test'),
      ],
    );
  });
}
```

```dart
// test/features/carrito/cubit/carrito_cubit_test.dart
void main() {
  late CarritoCubit cubit;

  setUp(() {
    HydratedBloc.storage = MockHydratedStorage();
    cubit = CarritoCubit();
  });

  tearDown(() => cubit.close());

  blocTest<CarritoCubit, CarritoState>(
    'agrega producto al carrito',
    build: () => cubit,
    act: (cubit) => cubit.agregar(producto1),
    expect: () => [CarritoState([producto1])],
  );

  blocTest<CarritoCubit, CarritoState>(
    'elimina producto del carrito',
    build: () => cubit,
    seed: () => CarritoState([producto1, producto2]),
    act: (cubit) => cubit.eliminar(producto1.id),
    expect: () => [CarritoState([producto2])],
  );

  blocTest<CarritoCubit, CarritoState>(
    'persiste en disco',
    build: () => cubit,
    act: (cubit) => cubit.agregar(producto1),
    verify: (_) {
      verify(() => HydratedBloc.storage.write(
            'CarritoCubit',
            any(),
          )).called(1);
    },
  );
}
```

## Resumen

Esta app integra **todos** los conceptos del módulo:

| Concepto | Dónde se usa |
|---|---|
| Cubit | Auth, Carrito, Favoritos, Perfil, Tema |
| Bloc | Productos (eventos + transformers) |
| BlocProvider | MultiBlocProvider en App, providers por página |
| BlocBuilder | Lista de productos, carrito, favoritos |
| BlocListener | Login (navegación + SnackBar) |
| BlocConsumer | Login (estado + side effects) |
| BlocSelector | Favorito badge, carrito badge, campo email |
| context.read | onPressed, initState |
| context.watch | Reconstrucción de widgets pequeños |
| HydratedCubit | Tema, Carrito, Favoritos |
| GoRouter | Redirección por auth, navegación declarativa |
| Clean Architecture | Capas domain/data/presentation + GetIt |
| blocTest | Tests unitarios de cada Cubit/Bloc |
