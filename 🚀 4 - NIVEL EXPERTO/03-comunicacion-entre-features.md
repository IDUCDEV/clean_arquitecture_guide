# 🚀 Nivel Experto: Comunicación Entre Features en Clean Architecture

En aplicaciones medianas y grandes, las features no existen en aislamiento. Un e-commerce tiene usuarios, productos, carrito, pagos, notificaciones. Cada uno es una feature, pero necesitan comunicarse. El error más común es **acoplar directamente las features**, rompiendo los principios de Clean Architecture. Esta guía profundiza en patrones robustos para lograr comunicación sin acoplamiento.

---

## 1. Fundamentos: Por Qué el Acoplamiento es Peligroso

### 1.1 El Problema del Acoplamiento Directo

Imaginemos:

```
Feature_A (Presentation) → Feature_B (Data/Repository)
```

Si `Feature_A` importa directamente el repositorio de `Feature_B`:

```dart
// ❌ ACOPLAMIENTOSÍO
import 'package:features/products/data/repositories/product_repository.dart';

class CartCubit extends Cubit<CartState> {
  final ProductRepository productRepo; // ⚠️ Feature_A conoce Feature_B
  
  Future<void> checkout() async {
    final products = await productRepo.getProducts(); // 💣 Alto acoplamiento
    // ...
  }
}
```

**Consecuencias:**
- Si `ProductRepository` cambia, `CartCubit` puede romperse
- No puedes reutilizar `Feature_A` sin `Feature_B`
- Testing se vuelve difícil
- Difícil mantener equipos trabajando en paralelo

### 1.2 El Principio de Dependencia Inversa

Clean Architecture dice: las capas internas no deben conocer las externas. Pero cuando dos features del mismo nivel necesitan comunicarse, aplicamos **Inversión de Dependencias**.

```
Feature_A → Interfaz (abstracta) ← Feature_B
```

Ninguna feature conoce a la otra. Ambas dependen de una abstracción.

---

## 2. Patrones de Comunicación

### 2.1 Patrón 1: Repository Compartido (Shared Domain)

**Cuándo usarlo:** Cuando múltiples features necesitan acceder a los mismos datos.

**Estructura:**

```
lib/
├── core/
│   ├── domain/
│   │   └── repositories/
│   │       └── auth_repository.dart  # Interfaz única
├── features/
│   ├── auth/
│   │   ├── data/repositories/auth_repository_impl.dart
│   │   └── presentation/
│   ├── perfil/
│   │   └── presentation/ (usa AuthRepository)
│   └── settings/
│       └── presentation/ (usa AuthRepository)
```

**Implementación:**

```dart
// lib/core/domain/repositories/auth_repository.dart

abstract class AuthRepository {
  Future<Option<User>> getCurrentUser();
  Future<Either<Failure, User>> signIn(Email email, Password password);
  Future<Either<Failure, void>> signOut();
  Stream<User?> get authStateChanges;
}
```

```dart
// lib/features/auth/data/repositories/auth_repository_impl.dart

@LazySingleton(as: AuthRepository)
class AuthRepositoryImpl implements AuthRepository {
  final FirebaseAuth _firebaseAuth;
  
  AuthRepositoryImpl(this._firebaseAuth);
  
  @override
  Future<Option<User>> getCurrentUser() async {
    final user = _firebaseAuth.currentUser;
    return Option.fromNullable(user);
  }
  
  // ... implementación
}
```

```dart
// lib/features/perfil/presentation/cubit/perfil_cubit.dart

@injectable
class PerfilCubit extends Cubit<PerfilState> {
  final AuthRepository authRepository;
  final GetUserProfile getUserProfile;
  
  PerfilCubit(this.authRepository, this.getUserProfile) 
      : super(PerfilInitial());
  
  Future<void> loadProfile() async {
    // Solo conoce AuthRepository, NO ProductRepository
    final user = await authRepository.getCurrentUser();
    
    user.fold(
      () => emit(PerfilUnauthenticated()),
      (u) async {
        final profile = await getUserProfile(u.id);
        profile.fold(
          (f) => emit(PerfilError(f.message)),
          (p) => emit(PerfilLoaded(p)),
        );
      },
    );
  }
}
```

### 2.2 Patrón 2: Feature Delegation (Mediator)

**Cuándo usarlo:** Cuando una feature necesita ejecutar una acción de otra sin conocer su implementación.

**Estructura conceptual:**

```
Feature_A (Checkout) 
    ↓ usa
Feature_B UseCase (ClearProductCache)
    ↓ implementa
Feature_B Repository → DataSource
```

**Implementación:**

```dart
// lib/features/products/domain/usecases/clear_product_cache.dart

@lazySingleton
class ClearProductCache {
  final ProductLocalDataSource localDataSource;
  
  ClearProductCache(this.localDataSource);
  
  Future<void> execute() async {
    await localDataSource.clearCache();
  }
}
```

```dart
// lib/features/cart/domain/usecases/checkout.dart

@lazySingleton
class Checkout {
  final CartRepository cartRepository;
  final ClearProductCache clearProductCache; // ✅ UseCase, no Repository
  
  Checkout(this.cartRepository, this.clearProductCache);
  
  Future<Either<Failure, CheckoutResult>> execute() async {
    return cartRepository.checkout().flatMap((order) async {
      await clearProductCache.execute(); // ✅ Acción de otra feature
      return Right(CheckoutResult(orderId: order.id));
    });
  }
}
```

**¿Por qué es mejor?**
- `Checkout` solo sabe que existe `ClearProductCache`
- No sabe si viene de Firebase, API, o Base de Datos
- Si cambias la implementación de `ClearProductCache`, `Checkout` no se entera

### 2.3 Patrón 3: Event Bus (Pub/Sub)

**Cuándo usarlo:** Cuando necesitas comunicación **asíncrona y desacoplada** entre múltiples features.

**Estructura:**

```
Feature_A dispara evento
         ↓
    Event Bus (Core)
         ↓
Feature_B, C, D escuchan evento
```

**Implementación del Event Bus:**

```dart
// lib/core/events/app_event.dart

abstract class AppEvent {}

class UserLoggedOutEvent extends AppEvent {}

class UserLoggedInEvent extends AppEvent {
  final User user;
  UserLoggedInEvent(this.user);
}

class ProductAddedToCartEvent extends AppEvent {
  final String productId;
  final int quantity;
  ProductAddedToCartEvent(this.productId, this.quantity);
}
```

```dart
// lib/core/events/event_bus.dart

class EventBus {
  final _events = StreamController<AppEvent>.broadcast();
  
  Stream<T> on<T extends AppEvent>() {
    return _events.stream.where((e) => e is T).cast<T>();
  }
  
  void fire(AppEvent event) {
    _events.add(event);
  }
}

// Registro como singleton
final eventBus = EventBus();
```

**Uso: Disparar Eventos:**

```dart
// lib/features/auth/presentation/cubit/auth_cubit.dart

@injectable
class AuthCubit extends Cubit<AuthState> {
  final AuthRepository authRepository;
  final EventBus eventBus;
  
  AuthCubit(this.authRepository, this.eventBus) : super(AuthInitial());
  
  Future<void> signOut() async {
    final result = await authRepository.signOut();
    
    result.fold(
      (failure) => emit(AuthError(failure.message)),
      (_) {
        eventBus.fire(UserLoggedOutEvent()); // ✅ Notificar a otros
        emit(AuthUnauthenticated());
      },
    );
  }
}
```

**Uso: Escuchar Eventos:**

```dart
// lib/features/cart/presentation/cubit/cart_cubit.dart

@injectable
class CartCubit extends Cubit<CartState> {
  final EventBus eventBus;
  StreamSubscription? _subscription;
  
  CartCubit(this.eventBus) : super(CartInitial());
  
  void startListening() {
    _subscription?.cancel();
    _subscription = eventBus.on<UserLoggedOutEvent>().listen((_) {
      // Limpiar carrito cuando usuario cierre sesión
      emit(CartEmpty());
    });
  }
  
  @override
  Future<void> close() {
    _subscription?.cancel();
    return super.close();
  }
}
```

### 2.4 Patrón 4: State Management Compartido

**Cuándo usarlo:** Cuando necesitas estado global accesible desde múltiples features.

**Con Cubits Globales:**

```dart
// lib/core/cubits/theme_cubit.dart

@injectable
class ThemeCubit extends Cubit<ThemeState> {
  ThemeCubit() : super(ThemeInitial());
  
  void toggleTheme() {
    final newTheme = state is DarkTheme ? LightTheme() : DarkTheme();
    emit(newTheme);
  }
}
```

```dart
// Uso en cualquier feature
class ProductCard extends StatelessWidget {
  final ThemeCubit themeCubit; // Inyectar
  
  @override
  Widget build(BuildContext context) {
    return BlocBuilder(
      bloc: themeCubit,
      builder: (context, theme) {
        return Container(
          color: theme.background,
          child: Text('Producto'),
        );
      },
    );
  }
}
```

---

## 3. Arquitectura de Features: Estructura Completa

### 3.1 Estructura de Carpetas Recomendada

```
lib/
├── core/
│   ├── cubits/                    # Cubits globales
│   │   ├── theme_cubit.dart
│   │   └── locale_cubit.dart
│   ├── events/                    # Event Bus
│   │   ├── app_event.dart
│   │   └── event_bus.dart
│   ├── domain/
│   │   └── repositories/          # Repos compartidos
│   │       ├── auth_repository.dart
│   │       └── analytics_repository.dart
│   └── services/                  # Core services
│       └── analytics/
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   └── repositories/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   └── usecases/
│   │   └── presentation/
│   │       ├── cubit/
│   │       ├── widgets/
│   │       └── pages/
│   ├── products/
│   │   └── ...
│   └── cart/
│       └── ...
```

### 3.2 Feature como Módulo

Cada feature debe ser independiente:

```dart
// lib/features/cart/cart.dart

class CartFeature {
  static Widget page() {
    return MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => getIt<CartCubit>()),
      ],
      child: CartPage(),
    );
  }
}
```

---

## 4. Errores Comunes y Anti-Patrones

### Error 1: Presentation Layer a Presentation Layer

```dart
// ❌ NUNCA hagas esto
class ProductDetailCubit extends Cubit<ProductDetailState> {
  final CartCubit cartCubit; // ⚠️ Feature A conoce Feature B
  
  void addToCart(Product product) {
    cartCubit.add(product); // Acoplamiento total
  }
}
```

**Solución:** Usar Event Bus o UseCase compartido.

### Error 2: Repositorio de una Feature en otra Feature

```dart
// ❌ NUNCA imports así
import 'features/products/data/repositories/product_repository_impl.dart';
```

**Solución:** Crear interfaz en `core/domain/repositories`.

### Error 3: Ciclos de Dependencia

```
Feature_A → Feature_B → Feature_A → 💥
```

**Solución:** Usar Event Bus para romper el ciclo.

---

## 5. Flujo de Datos entre Features: Diagramas

### 5.1 Comunicación Síncrona (UseCase)

```
┌──────────────┐     ┌──────────────┐
│ Feature_A    │     │ Feature_B    │
│  Cubit       │     │  UseCase     │
└──────┬───────┘     └──────┬───────┘
       │                    │
       │ getData()          │
       └──────────┬─────────┘
                  │
         ┌────────▼────────┐
         │  UseCase_A     │
         │ (invoca UseCase_B)
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │ Repository     │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │ DataSource     │
         └─────────────────┘
```

### 5.2 Comunicación Asíncrona (Event Bus)

```
┌──────────────┐      eventBus      ┌──────────────┐
│ Feature_A    │ ──────────────────►│ Feature_B    │
│  Cubit       │  UserLoggedOut    │  Cubit       │
│  (dispara)   │                    │  (escucha)   │
└──────────────┘                    └──────────────┘
```

---

## 6. Casos de Uso Reales

### Caso 1: Carrito necesita saber si usuario está logueado

**❌ Mal:** `CartCubit` importa `AuthRepositoryImpl`

**✅ Bien:** `CartCubit` usa `AuthRepository` (interfaz en core)

```dart
@injectable
class CartCubit extends Cubit<CartState> {
  final AuthRepository authRepository; // ✅ Interfaz
  final AddToCart addToCart;
  
  CartCubit(this.authRepository, this.addToCart);
  
  Future<void> addProduct(Product product) async {
    final user = await authRepository.getCurrentUser();
    
    user.fold(
      () => emit(CartNeedsLogin()), // Redirigir a login
      (_) => addToCart.execute(product),
    );
  }
}
```

### Caso 2: Checkout necesita limpiar cache de productos

**✅ UseCase Delegation:**

```dart
class CheckoutUseCase {
  final CartRepository cartRepository;
  final ClearProductCache clearProductCache;
  
  // Dependency Injection de UseCase de otra feature
  CheckoutUseCase(this.cartRepository, this.clearProductCache);
}
```

### Caso 3: Notificaciones necesitan saber cuando cambia el usuario

**✅ Event Bus:**

```dart
// En AuthCubit
eventBus.fire(UserChangedEvent(user));

// En NotificationsCubit
eventBus.on<UserChangedEvent>().listen((event) {
  subscribeToUserNotifications(event.user.id);
});
```

---

## 7. Testing de Features Desacopladas

### Unit Test de UseCase con Dependencias

```dart
void main() {
  late Checkout checkout;
  late MockCartRepository mockCartRepo;
  late MockClearProductCache mockClearCache;
  
  setUp(() {
    mockCartRepo = MockCartRepository();
    mockClearCache = MockClearProductCache();
    
    // ✅ Inyectar mocks
    checkout = Checkout(mockCartRepo, mockClearCache);
  });
  
  test('checkout clears product cache', () async {
    when(() => mockCartRepo.checkout())
        .thenAnswer((_) async => Right(Order(id: '123')));
    when(() => mockClearCache.execute())
        .thenAnswer((_) async {});
    
    await checkout.execute();
    
    verify(() => mockClearCache.execute()).called(1);
  });
}
```

### Integración con Event Bus

```dart
test('UserLoggedOutEvent clears cart', () async {
  final eventBus = EventBus();
  final cartCubit = CartCubit(eventBus);
  
  // Emitir evento
  eventBus.fire(UserLoggedOutEvent());
  
  // Verificar estado
  expect(cartCubit.state, CartEmpty());
});
```

### 7.1 Testing de UseCase con Dependencias Entre Features

```dart
// test/features/cart/domain/usecases/checkout_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/cart/domain/repositories/cart_repository.dart';
import 'package:my_app/features/cart/domain/usecases/checkout.dart';
import 'package:my_app/features/products/domain/usecases/clear_product_cache.dart';

class MockCartRepository extends Mock implements CartRepository {}
class MockClearProductCache extends Mock implements ClearProductCache {}

void main() {
  late Checkout useCase;
  late MockCartRepository mockCartRepo;
  late MockClearProductCache mockClearCache;

  setUp(() {
    mockCartRepo = MockCartRepository();
    mockClearCache = MockClearProductCache();
    useCase = Checkout(mockCartRepo, mockClearCache);
  });

  setUpAll(() {
    registerFallbackValue(const CheckoutParams());
  });

  group('Checkout UseCase', () {
    const tOrder = Order(id: 'order-123', total: 100.0);
    const tParams = CheckoutParams();

    test('debería limpiar cache después de checkout exitoso', () async {
      // Arrange
      when(() => mockCartRepo.checkout(tParams))
          .thenAnswer((_) async => const Right(tOrder));
      when(() => mockClearCache.execute())
          .thenAnswer((_) async {});

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result.isRight(), true);
      
      // Verificar orden: checkout primero, luego clear
      verifyInOrder([
        () => mockCartRepo.checkout(tParams),
        () => mockClearCache.execute(),
      ]);
      verifyNoMoreInteractions(mockCartRepo);
      verifyNoMoreInteractions(mockClearCache);
    });

    test('debería retornar failure si checkout falla', () async {
      // Arrange
      when(() => mockCartRepo.checkout(tParams))
          .thenAnswer((_) async => const Left(CheckoutFailure('Stock insuficiente')));
      when(() => mockClearCache.execute())
          .thenAnswer((_) async {});

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result.isLeft(), true);
      verifyNever(() => mockClearCache.execute());
    });

    test('debería fallar si clear cache falla pero checkout exitoso', () async {
      // Arrange
      when(() => mockCartRepo.checkout(tParams))
          .thenAnswer((_) async => const Right(tOrder));
      when(() => mockClearCache.execute())
          .thenThrow(Exception('Cache error'));

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result.isLeft(), true);
    });
  });
}
```

### 7.2 Testing de Event Bus

```dart
// test/core/events/event_bus_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/core/events/app_event.dart';
import 'package:my_app/core/events/event_bus.dart';

void main() {
  late EventBus eventBus;

  setUp(() {
    eventBus = EventBus();
  });

  group('EventBus', () {
    test('debería recibir evento disparado', () async {
      // Arrange
      final future = eventBus.on<UserLoggedInEvent>().first;

      // Act
      eventBus.fire(UserLoggedInEvent(User(id: '1', name: 'Test')));

      // Assert
      final event = await future;
      expect(event.user.id, '1');
    });

    test('debería filtrar por tipo de evento', () async {
      // Arrange
      final subscription = eventBus.on<UserLoggedInEvent>().listen((_) {});
      
      // Act
      eventBus.fire(UserLoggedOutEvent());
      eventBus.fire(UserLoggedInEvent(User(id: '1', name: 'Test')));
      
      // Assert: El stream debería tener el evento correcto
      final event = await eventBus.on<UserLoggedInEvent>().first;
      expect(event, isA<UserLoggedInEvent>());
    });

    test('debería permitir múltiples suscriptores', () async {
      // Arrange
      int callCount = 0;
      final sub1 = eventBus.on<UserLoggedInEvent>().listen((_) => callCount++);
      final sub2 = eventBus.on<UserLoggedInEvent>().listen((_) => callCount++);

      // Act
      eventBus.fire(UserLoggedInEvent(User(id: '1', name: 'Test')));

      // Assert
      await Future.delayed(Duration.zero);
      expect(callCount, 2);

      await sub1.cancel();
      await sub2.cancel();
    });

    test('debería cerrar correctamente', () async {
      final subscription = eventBus.on<UserLoggedInEvent>().listen((_) {});
      
      await subscription.cancel();
      
      // No debería haber más eventos después de cancelar
      eventBus.fire(UserLoggedInEvent(User(id: '1', name: 'Test')));
      
      final future = eventBus.on<UserLoggedInEvent>().first;
      await Future.delayed(Duration(milliseconds: 100));
      
      // Si no hay evento, el test pasa (subscription cancelada)
    });
  });
}
```

### 7.3 Testing de Comunicación entre Features

```dart
// test/integration/feature_communication_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/features/auth/domain/repositories/auth_repository.dart';
import 'package:my_app/features/auth/domain/usecases/sign_out.dart';
import 'package:my_app/features/cart/domain/usecases/clear_cart.dart';
import 'package:my_app/features/cart/presentation/cubit/cart_cubit.dart';
import 'package:my_app/core/events/event_bus.dart';

class MockAuthRepository extends Mock implements AuthRepository {}
class MockClearCart extends Mock implements ClearCart {}

void main() {
  late EventBus eventBus;
  late CartCubit cartCubit;

  setUp(() {
    eventBus = EventBus();
    cartCubit = CartCubit(eventBus);
  });

  tearDown(() {
    cartCubit.close();
  });

  group('Feature Communication Integration', () {
    test('signOut debería limpiar el carrito', () async {
      // Arrange
      // Simular que el carrito tiene productos
      // (En un caso real, el CartCubit tendría estado inicial)

      // Act
      // Disparar evento como lo haría AuthCubit
      eventBus.fire(UserLoggedOutEvent());

      // Wait para que el evento se procese
      await Future.delayed(Duration.zero);

      // Assert - El carrito debería estar vacío después de logout
      expect(cartCubit.state, CartEmpty());
    });

    test('múltiples features deberían reaccionar al mismo evento', () async {
      // Arrange
      final analyticsCubit = AnalyticsCubit(eventBus);
      final notificationCubit = NotificationCubit(eventBus);

      // Act
      eventBus.fire(UserLoggedInEvent(User(id: '1', name: 'Test')));

      // Wait
      await Future.delayed(Duration.zero);

      // Assert
      expect(analyticsCubit.state, AnalyticsTrackingEnabled());
      expect(notificationCubit.state, NotificationsSubscribed());

      await analyticsCubit.close();
      await notificationCubit.close();
    });
  });
}
```

### 7.4 Testing de Shared Repository

```dart
// test/integration/shared_repository_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/core/domain/repositories/auth_repository.dart';
import 'package:my_app/features/perfil/domain/usecases/get_profile.dart';
import 'package:my_app/features/settings/domain/usecases/get_settings.dart';

class MockAuthRepository extends Mock implements AuthRepository {}

void main() {
  late MockAuthRepository mockAuthRepo;
  late GetProfile getProfile;
  late GetSettings getSettings;

  setUp(() {
    mockAuthRepo = MockAuthRepository();
    getProfile = GetProfile(mockAuthRepo);
    getSettings = GetSettings(mockAuthRepo);
  });

  group('Shared Repository Pattern', () {
    const tUser = User(id: '1', name: 'Test User');

    test('múltiples features deberían poder usar el mismo repositorio', () async {
      // Arrange
      when(() => mockAuthRepo.getCurrentUser())
          .thenAnswer((_) async => const Option.of(tUser));

      // Act & Assert - Feature Perfil
      final profileResult = await getProfile();
      expect(profileResult.isRight(), true);

      // Act & Assert - Feature Settings  
      final settingsResult = await getSettings();
      expect(settingsResult.isRight(), true);

      // Verificar que se llamó al mismo repositorio
      verify(() => mockAuthRepo.getCurrentUser()).called(2);
    });

    test('cambios en AuthRepository deberían reflejarse en todas las features', () async {
      // Arrange
      when(() => mockAuthRepo.getCurrentUser())
          .thenAnswer((_) async => const Option.of(tUser));

      // Act
      final profile1 = await getProfile();
      final profile2 = await getProfile();

      // Assert - Mismo resultado
      profile1.fold(
        (_) => fail('No debería fallar'),
        (p) => expect(p.user.name, 'Test User'),
      );
      profile2.fold(
        (_) => fail('No debería fallar'),
        (p) => expect(p.user.name, 'Test User'),
      );
    });
  });
}
```

### 7.5 Testing de State Compartido

```dart
// test/core/cubits/theme_cubit_test.dart

import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/core/cubits/theme_cubit.dart';

void main() {
  late ThemeCubit themeCubit;

  setUp(() {
    themeCubit = ThemeCubit();
  });

  tearDown(() {
    themeCubit.close();
  });

  group('ThemeCubit - Shared State', () {
    test('estado inicial es tema claro', () {
      expect(themeCubit.state, LightTheme());
    });

    blocTest<ThemeCubit, ThemeState>(
      'debería cambiar a tema oscuro',
      build: () => ThemeCubit(),
      act: (cubit) => cubit.toggleTheme(),
      expect: () => [DarkTheme()],
    );

    blocTest<ThemeCubit, ThemeState>(
      'debería alternar entre temas',
      build: () => ThemeCubit(),
      act: (cubit) {
        cubit.toggleTheme();
        cubit.toggleTheme();
      },
      expect: () => [DarkTheme(), LightTheme()],
    );

    test('múltiples listeners deberían recibir el mismo estado', () async {
      // Arrange
      final states = <ThemeState>[];
      themeCubit.stream.listen((state) => states.add(state));

      // Act
      themeCubit.toggleTheme();
      await Future.delayed(Duration.zero);

      // Assert
      expect(states.length, 2); // Initial + DarkTheme
    });
  });
}
```

### 7.6 Errores Comunes en Testing de Features

```dart
// ❌ Error 1: Olvidar cerrar suscripciones
tearDown(() {
  // CRASH: Stream not closed
});

// ✅ Solución
tearDown(() async {
  await cubit.close();
});

// ❌ Error 2: Mock no configurado
when(() => mockRepo.getUser()).thenAnswer((_) async => null);
// CRASH: MissingStubError

// ✅ Solución
setUpAll(() {
  registerFallbackValue(UserParams('test'));
});

// ❌ Error 3: No aislar tests de Event Bus
test('test1', () async {
  eventBus.fire(UserLoggedInEvent()); // Afecta test2
});

// ✅ Solución - crear nuevo EventBus por test
setUp(() {
  eventBus = EventBus();
});

// ❌ Error 4: Test de Feature sin mockear dependencia
test('feature test', () {
  // Usa implementación real → frágil
});

// ✅ Solución - usar mocks
setUp(() {
  mockRepo = MockRepo();
  cubit = Cubit(mockRepo);
});
```

### 7.7 Estructura de Tests para Features

```
test/
├── features/
│   ├── auth/
│   │   ├── data/
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl_test.dart
│   │   ├── domain/
│   │   │   └── usecases/
│   │   │       └── sign_out_test.dart
│   │   └── presentation/
│   │       └── cubit/
│   │           └── auth_cubit_test.dart
│   ├── cart/
│   │   └── ...
│   └── products/
│       └── ...
├── core/
│   ├── events/
│   │   └── event_bus_test.dart
│   └── cubits/
│       └── theme_cubit_test.dart
├── integration/
│   ├── feature_communication_test.dart
│   └── shared_repository_test.dart
└── mocks/
    ├── mock_classes.dart
    └── fixtures/
        ├── user_fixture.dart
        └── product_fixture.dart
```

---

## 8. Mejores Prácticas

### Reglas de Oro

1. **Nunca importes Presentation de otra feature**
2. **Usa Interfaces en `core/domain/repositories`** para comunicación de datos
3. **Usa UseCases compartidos** para acciones de negocio
4. **Usa Event Bus** para eventos globales (login, logout, temas)
5. **Una feature es un módulo** - Puede deshabilitarse/reescribirse completamente

### Checklist antes de hacer Feature Communication

- [ ] ¿Puedo lograr esto con una interfaz en core?
- [ ] ¿El uso es de datos → Repository?
- [ ] ¿El uso es de acción → UseCase?
- [ ] ¿Es un evento que múltiples features necesitan saber → Event Bus?
- [ ] ¿Es estado global → Cubit compartido?

---

## 9. Comunicación con Módulos Externos

### Feature → Firebase/Backend

No uses el SDK directamente en los Cubits. Capa de abstracción:

```
Cubit → Repository (interfaz) → RepositoryImpl → SDK
```

### Feature → Device (Cámara, GPS, Sensores)

```
Cubit → DeviceService (interfaz) → DeviceServiceImpl → Platform Channels
```

---

## 10. Resumen de Patrones

| Patrón | Cuándo Usar | Complejidad |
|--------|-------------|-------------|
| **Shared Repository** | Múltiples features leen mismos datos | Baja |
| **UseCase Delegation** | Feature ejecuta acción de otra | Baja |
| **Event Bus** | Eventos asíncronos, uno→muchos | Media |
| **Shared State** | Estado global (tema, locale) | Baja |

---

## Resumen Ejecutivo

1. **El acoplamiento destruye Clean Architecture** - Evita imports directos entre features
2. **Usa Interfaces** en `core/domain/repositories` para compartir datos
3. **Usa UseCases** para compartir acciones de negocio
4. **Usa Event Bus** para comunicación asíncrona y eventos globales
5. **NUNCA** ties Presentation a Presentation
6. **Testing** se simplifica dramáticamente con dependencias inyectables

**Siguiente nivel:** Aprende a diseñar features completamente independientes que se comunican solo a través de eventos, el patrón "Micro-frontends" aplicado a Flutter.

---

## Recursos Adicionales

- [The Power of Event Bus](https://blog.novoda.com/the-power-of-event-bus/)
- [Modular Architecture in Flutter](https://www.raywenderlich.com/10404758-building-a-modular-architecture-in-flutter)
- [BLoC Communication](https://bloclibrary.dev/#/architecture)
