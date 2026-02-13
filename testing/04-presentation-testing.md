# 🧪 Parte 4: Testing Presentation (Cubits y Widgets) - EXTENDIDA

## 📋 Índice
1. [Introducción a la Capa Presentation](#introducción-a-la-capa-presentation)
2. [Testing de Cubits con bloc_test](#testing-de-cubits-con-bloc_test)
   - [Conceptos fundamentales de bloc_test](#conceptos-fundamentales-de-bloc_test)
   - [Testing de estados iniciales](#testing-de-estados-iniciales)
   - [Testing de transiciones de estados](#testing-de-transiciones-de-estados)
   - [Testing con múltiples acciones](#testing-con-múltiples-acciones)
   - [Testing de streams y async](#testing-de-streams-y-async)
   - [Testing con dependencias complejas](#testing-con-dependencias-complejas)
   - [Testing de error handling avanzado](#testing-de-error-handling-avanzado)
3. [Testing de Estados](#testing-de-estados)
4. [Testing de Widgets](#testing-de-widgets)
   - [Fundamentos de widget testing](#fundamentos-de-widget-testing)
   - [Testing de renderizado](#testing-de-renderizado)
   - [Testing de interacciones de usuario](#testing-de-interacciones-de-usuario)
   - [Testing de formularios completos](#testing-de-formularios-completos)
   - [Testing de navegación](#testing-de-navegación)
   - [Testing de diálogos y modales](#testing-de-diálogos-y-modales)
   - [Testing de snackbars y toasts](#testing-de-snackbars-y-toasts)
   - [Testing de scroll y listas](#testing-de-scroll-y-listas)
   - [Testing de gestos](#testing-de-gestos)
   - [Testing de animaciones](#testing-de-animaciones)
5. [Testing de Pages Completas](#testing-de-pages-completas)
6. [Ejercicios Prácticos Avanzados](#ejercicios-prácticos-avanzados)

---

## Introducción a la Capa Presentation

La capa **Presentation** es el puente entre la UI y el dominio. En Clean Architecture con Flutter, usamos el patrón **BLoC** (Business Logic Component) implementado con **Cubits**.

### 🎯 ¿Por qué testear la capa Presentation?

1. **Lógica de estado**: El Cubit contiene la lógica de negocio de la UI
2. **Experiencia de usuario**: Los widgets deben responder correctamente a los estados
3. **Regresiones**: Prevenir que cambios rompan la UI
4. **Documentación**: Los tests documentan el comportamiento esperado

### 📦 Arquitectura de la capa Presentation:

```
Presentation Layer
├── Cubit           ← Lógica de estado y casos de uso
│   ├── auth_cubit.dart
│   └── auth_state.dart
├── UI Components   ← Widgets reutilizables
│   ├── auth_form.dart
│   ├── email_input.dart
│   └── password_input.dart
└── Pages           ← Pantallas completas
    ├── auth_page.dart
    └── register_page.dart
```

### 🎨 Flujo de datos:

```
User Action → Widget → Cubit → UseCase → Repository → Resultado
                                      ↓
                 Widget ← Estado ← Cubit ←
```

---

## Testing de Cubits con bloc_test

### 📦 Instalación de bloc_test

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0
  mockito: ^5.4.0      # Opcional, para mocks avanzados
```

```bash
flutter pub get
```

---

### Conceptos fundamentales de bloc_test

`blocTest` es una función especializada que facilita el testing de Cubits y Blocs. Proporciona una API declarativa para definir tests.

#### 📝 Sintaxis completa de blocTest:

```dart
blocTest<AuthCubit, AuthState>(
  'descripción del test',
  
  // Construye el Cubit (puede incluir configuración)
  build: () => AuthCubit(...),
  
  // Estado inicial opcional (sobrescribe el estado por defecto)
  seed: () => const AuthInitial(),
  
  // Acción que ejecuta el test
  act: (cubit) => cubit.login(email, password),
  
  // Estados esperados en orden
  expect: () => [
    const AuthLoading(),
    const Authenticated(user: tUser),
  ],
  
  // Verificaciones adicionales después del test
  verify: (_) {
    verify(mockRepository.login(any, any)).called(1);
  },
  
  // Errores esperados (opcional)
  errors: () => [
    isA<StateError>(),
  ],
  
  // Timeout para operaciones async
  wait: const Duration(milliseconds: 100),
);
```

#### 🎓 Parámetros de blocTest explicados:

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `description` | String | Descripción del test | ✅ Sí |
| `build` | `() → Cubit` | Factory que crea el Cubit | ✅ Sí |
| `seed` | `() → State` | Estado inicial opcional | ❌ No |
| `act` | `(cubit) → dynamic` | Acción a ejecutar | ❌ No |
| `expect` | `() → List<State>` | Estados esperados | ❌ No |
| `verify` | `(cubit) → void` | Verificaciones adicionales | ❌ No |
| `errors` | `() → List` | Errores esperados | ❌ No |
| `wait` | `Duration` | Espera async | ❌ No |

---

### Testing de estados iniciales

Cada Cubit debe tener un estado inicial definido. Es importante testear esto explícitamente.

```dart
group('Estado Inicial', () {
  test('debería tener AuthInitial como estado inicial', () {
    // ARRANGE & ACT - El cubit se crea automáticamente
    final cubit = AuthCubit(
      loginUseCase: fakeLogin,
      logoutUseCase: fakeLogout,
      registerUseCase: fakeRegister,
      checkAuthStatusUseCase: fakeCheckAuth,
    );

    // ASSERT
    expect(cubit.state, equals(const AuthInitial()));
    
    // Limpieza
    cubit.close();
  });

  blocTest<AuthCubit, AuthState>(
    'debería emitir el estado inicial inmediatamente',
    build: () => AuthCubit(
      loginUseCase: fakeLogin,
      logoutUseCase: fakeLogout,
      registerUseCase: fakeRegister,
      checkAuthStatusUseCase: fakeCheckAuth,
    ),
    // No hay 'act' porque solo verificamos el estado inicial
    expect: () => [], // No se emiten estados adicionales
  );
});
```

---

### Testing de transiciones de estados

El test más común es verificar que el Cubit emite los estados correctos en secuencia.

#### ✅ Transición exitosa (Loading → Success):

```dart
group('Login', () {
  const tEmail = 'test@example.com';
  const tPassword = 'password123';
  const tUser = User(
    id: '123',
    email: tEmail,
    name: 'John',
    lastName: 'Doe',
  );

  blocTest<AuthCubit, AuthState>(
    'debería emitir [AuthLoading, Authenticated] cuando login es exitoso',
    build: () {
      fakeLogin.userToReturn = tUser;
      return cubit;
    },
    act: (cubit) => cubit.login(tEmail, tPassword),
    expect: () => [
      const AuthLoading(),
      const Authenticated(user: tUser),
    ],
  );

  blocTest<AuthCubit, AuthState>(
    'debería emitir [AuthLoading, AuthError] cuando login falla',
    build: () {
      fakeLogin.shouldFail = true;
      fakeLogin.failureToReturn = const ServerFailure('Credenciales inválidas');
      return cubit;
    },
    act: (cubit) => cubit.login(tEmail, tPassword),
    expect: () => [
      const AuthLoading(),
      const AuthError(message: 'Credenciales inválidas'),
    ],
  );
});
```

#### 🔄 Múltiples transiciones en secuencia:

```dart
group('CheckAuthStatus - Múltiples escenarios', () {
  blocTest<AuthCubit, AuthState>(
    'debería emitir [AuthLoading, Authenticated] cuando hay usuario logueado',
    build: () {
      fakeCheckAuth.userToReturn = tUser;
      return cubit;
    },
    act: (cubit) => cubit.checkAuthStatus(),
    expect: () => [
      const AuthLoading(),
      const Authenticated(user: tUser),
    ],
  );

  blocTest<AuthCubit, AuthState>(
    'debería emitir [AuthLoading, Unauthenticated] cuando no hay usuario',
    build: () {
      fakeCheckAuth.userToReturn = null;
      return cubit;
    },
    act: (cubit) => cubit.checkAuthStatus(),
    expect: () => [
      const AuthLoading(),
      const Unauthenticated(),
    ],
  );

  blocTest<AuthCubit, AuthState>(
    'debería emitir [AuthLoading, AuthError] cuando falla el chequeo',
    build: () {
      fakeCheckAuth.shouldFail = true;
      fakeCheckAuth.failureToReturn = const CacheFailure('Error de caché');
      return cubit;
    },
    act: (cubit) => cubit.checkAuthStatus(),
    expect: () => [
      const AuthLoading(),
      const AuthError(message: 'Error de caché'),
    ],
  );
});
```

---

### Testing con múltiples acciones

A veces necesitas testear escenarios donde se ejecutan varias acciones en secuencia.

```dart
group('Múltiples acciones', () {
  blocTest<AuthCubit, AuthState>(
    'debería manejar login seguido de logout',
    build: () {
      fakeLogin.userToReturn = tUser;
      return cubit;
    },
    act: (cubit) async {
      await cubit.login(tEmail, tPassword);
      await cubit.logout();
    },
    expect: () => [
      // Login
      const AuthLoading(),
      const Authenticated(user: tUser),
      // Logout
      const AuthLoading(),
      const Unauthenticated(),
    ],
  );

  blocTest<AuthCubit, AuthState>(
    'debería manejar múltiples intentos de login',
    build: () {
      fakeLogin.userToReturn = tUser;
      return cubit;
    },
    act: (cubit) async {
      // Primer intento fallido
      fakeLogin.shouldFail = true;
      await cubit.login(tEmail, 'wrong-password');
      
      // Segundo intento exitoso
      fakeLogin.shouldFail = false;
      await cubit.login(tEmail, tPassword);
    },
    expect: () => [
      // Primer intento
      const AuthLoading(),
      isA<AuthError>(),
      // Segundo intento
      const AuthLoading(),
      const Authenticated(user: tUser),
    ],
  );
});
```

---

### Testing de streams y async

Cuando el Cubit tiene streams o timers, necesitas manejar el async apropiadamente.

```dart
group('Operaciones asíncronas', () {
  blocTest<AuthCubit, AuthState>(
    'debería manejar delays en operaciones',
    build: () {
      fakeLogin.userToReturn = tUser;
      fakeLogin.delay = const Duration(milliseconds: 100);
      return cubit;
    },
    act: (cubit) => cubit.login(tEmail, tPassword),
    wait: const Duration(milliseconds: 150), // Esperar el delay
    expect: () => [
      const AuthLoading(),
      const Authenticated(user: tUser),
    ],
  );

  blocTest<AuthCubit, AuthState>(
    'debería manejar operaciones concurrentes',
    build: () {
      fakeLogin.userToReturn = tUser;
      return cubit;
    },
    act: (cubit) async {
      // Lanzar múltiples logins simultáneamente
      await Future.wait([
        cubit.login(tEmail, tPassword),
        cubit.login(tEmail, tPassword),
      ]);
    },
    expect: () => [
      // Los estados se emiten en orden, incluso si las operaciones son concurrentes
      const AuthLoading(),
      const AuthLoading(),
      const Authenticated(user: tUser),
      const Authenticated(user: tUser),
    ],
  );
});
```

---

### Testing con dependencias complejas

Cuando el Cubit tiene múltiples dependencias, es importante verificar que se usan correctamente.

```dart
group('Verificación de dependencias', () {
  blocTest<AuthCubit, AuthState>(
    'debería llamar a loginUseCase con parámetros correctos',
    build: () {
      fakeLogin.userToReturn = tUser;
      return cubit;
    },
    act: (cubit) => cubit.login(tEmail, tPassword),
    expect: () => [
      const AuthLoading(),
      const Authenticated(user: tUser),
    ],
    verify: (_) {
      // Verificar que se llamó con los parámetros correctos
      expect(fakeLogin.lastEmail, tEmail);
      expect(fakeLogin.lastPassword, tPassword);
    },
  );

  blocTest<AuthCubit, AuthState>(
    'debería incrementar contador de llamadas',
    build: () {
      fakeLogin.userToReturn = tUser;
      return cubit;
    },
    act: (cubit) async {
      await cubit.login(tEmail, tPassword);
      await cubit.login(tEmail, tPassword);
    },
    verify: (_) {
      expect(fakeLogin.callCount, 2);
    },
  );

  blocTest<AuthCubit, AuthState>(
    'no debería llamar a logoutUseCase durante login',
    build: () {
      fakeLogin.userToReturn = tUser;
      return cubit;
    },
    act: (cubit) => cubit.login(tEmail, tPassword),
    verify: (_) {
      expect(fakeLogout.callCount, 0);
    },
  );
});
```

---

### Testing de error handling avanzado

Los errores pueden ocurrir de diferentes maneras. Es importante testear todos los casos.

```dart
group('Error Handling Avanzado', () {
  blocTest<AuthCubit, AuthState>(
    'debería manejar excepciones no controladas',
    build: () {
      fakeLogin.shouldThrowException = true;
      fakeLogin.exceptionToThrow = Exception('Error inesperado');
      return cubit;
    },
    act: (cubit) => cubit.login(tEmail, tPassword),
    errors: () => [
      isA<Exception>(),
    ],
  );

  blocTest<AuthCubit, AuthState>(
    'debería manejar diferentes tipos de failure',
    build: () {
      fakeLogin.shouldFail = true;
      return cubit;
    },
    act: (cubit) async {
      // Test con ServerFailure
      fakeLogin.failureToReturn = const ServerFailure('Error de servidor');
      await cubit.login(tEmail, tPassword);
      
      // Test con NetworkFailure
      fakeLogin.failureToReturn = const NetworkFailure();
      await cubit.login(tEmail, tPassword);
    },
    expect: () => [
      const AuthLoading(),
      const AuthError(message: 'Error de servidor'),
      const AuthLoading(),
      const AuthError(message: 'No internet connection'),
    ],
  );

  blocTest<AuthCubit, AuthState>(
    'debería recuperarse de errores y permitir reintentos',
    build: () {
      return cubit;
    },
    act: (cubit) async {
      // Primer intento fallido
      fakeLogin.shouldFail = true;
      await cubit.login(tEmail, tPassword);
      
      // Segundo intento exitoso
      fakeLogin.shouldFail = false;
      fakeLogin.userToReturn = tUser;
      await cubit.login(tEmail, tPassword);
    },
    expect: () => [
      isA<AuthLoading>(),
      isA<AuthError>(),
      isA<AuthLoading>(),
      isA<Authenticated>(),
    ],
  );
});
```

---

## Testing de Estados

Los estados deben ser inmutables y comparables. Testearlos es crucial para asegurar que el Cubit funciona correctamente.

### Tests completos de Estados:

```dart
// test/features/auth/presentation/cubit/auth_state_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:sereni/clean/features/auth/domain/entities/user.dart';
import 'package:sereni/clean/features/auth/presentation/cubit/auth_state.dart';

void main() {
  group('AuthInitial', () {
    test('debería ser igual a otro AuthInitial', () {
      expect(const AuthInitial(), equals(const AuthInitial()));
    });

    test('props debería estar vacío', () {
      const state = AuthInitial();
      expect(state.props, isEmpty);
    });

    test('no debería ser igual a otros estados', () {
      expect(const AuthInitial(), isNot(equals(const AuthLoading())));
    });
  });

  group('AuthLoading', () {
    test('debería ser igual a otro AuthLoading', () {
      expect(const AuthLoading(), equals(const AuthLoading()));
    });

    test('props debería estar vacío', () {
      const state = AuthLoading();
      expect(state.props, isEmpty);
    });
  });

  group('Authenticated', () {
    const tUser = User(
      id: '123',
      email: 'test@example.com',
      name: 'John',
      lastName: 'Doe',
    );

    test('debería crearse con usuario requerido', () {
      const state = Authenticated(user: tUser);
      expect(state.user, equals(tUser));
    });

    test('debería ser igual cuando el usuario es igual', () {
      const state1 = Authenticated(user: tUser);
      const state2 = Authenticated(user: tUser);
      expect(state1, equals(state2));
    });

    test('no debería ser igual cuando el usuario difiere', () {
      const state1 = Authenticated(user: tUser);
      const state2 = Authenticated(
        user: User(
          id: '456',
          email: 'otro@example.com',
          name: 'Otro',
          lastName: 'Usuario',
        ),
      );
      expect(state1, isNot(equals(state2)));
    });

    test('props debería contener el usuario', () {
      const state = Authenticated(user: tUser);
      expect(state.props, [tUser]);
    });

    test('debería mantener inmutabilidad', () {
      const state = Authenticated(user: tUser);
      // No debería poder modificarse
      // state.user = otroUsuario; // Error de compilación
      expect(state.user, equals(tUser));
    });
  });

  group('Unauthenticated', () {
    test('debería ser igual a otro Unauthenticated', () {
      expect(const Unauthenticated(), equals(const Unauthenticated()));
    });

    test('props debería estar vacío', () {
      const state = Unauthenticated();
      expect(state.props, isEmpty);
    });
  });

  group('AuthError', () {
    test('debería crearse con mensaje requerido', () {
      const state = AuthError(message: 'Error de prueba');
      expect(state.message, 'Error de prueba');
    });

    test('debería ser igual cuando el mensaje es igual', () {
      const state1 = AuthError(message: 'Error');
      const state2 = AuthError(message: 'Error');
      expect(state1, equals(state2));
    });

    test('no debería ser igual cuando el mensaje difiere', () {
      const state1 = AuthError(message: 'Error 1');
      const state2 = AuthError(message: 'Error 2');
      expect(state1, isNot(equals(state2)));
    });

    test('props debería contener el mensaje', () {
      const state = AuthError(message: 'Test error');
      expect(state.props, ['Test error']);
    });

    test('debería permitir mensajes vacíos', () {
      const state = AuthError(message: '');
      expect(state.message, '');
    });
  });

  group('Comparación entre diferentes tipos de estados', () {
    test('AuthInitial no debería ser igual a AuthLoading', () {
      expect(const AuthInitial(), isNot(equals(const AuthLoading())));
    });

    test('Authenticated no debería ser igual a Unauthenticated', () {
      const auth = Authenticated(
        user: User(
          id: '123',
          email: 'test@test.com',
          name: 'Test',
          lastName: 'User',
        ),
      );
      expect(auth, isNot(equals(const Unauthenticated())));
    });

    test('AuthError no debería ser igual a AuthLoading', () {
      expect(
        const AuthError(message: 'Error'),
        isNot(equals(const AuthLoading())),
      );
    });
  });
}
```

---

## Testing de Widgets

### Fundamentos de widget testing

Los **widget tests** prueban la UI en aislamiento. Son más rápidos que los integration tests pero más lentos que los unit tests.

#### 🎯 ¿Qué podemos testear?

- Renderizado de widgets
- Interacciones de usuario (tap, scroll, input)
- Estados de widgets
- Navegación
- Diálogos y snackbars
- Formularios y validaciones
- Animaciones

#### 🛠️ Herramientas principales:

| Herramienta | Uso |
|-------------|-----|
| `testWidgets` | Define un test de widget |
| `pumpWidget` | Renderiza un widget |
| `pump` | Reconstruye el widget |
| `pumpAndSettle` | Espera animaciones |
| `find` | Busca widgets en el árbol |
| `expect` | Verifica expectativas |
| `tester.tap` | Simula un toque |
| `tester.enterText` | Simula entrada de texto |
| `tester.drag` | Simula arrastre |

---

### Testing de renderizado

#### Renderizado básico:

```dart
// test/features/auth/presentation/widgets/auth_button_test.dart
testWidgets('debería renderizar el botón correctamente', (WidgetTester tester) async {
  // ARRANGE & ACT - Renderizar el widget
  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(
        body: AuthButton(
          text: 'Login',
          onPressed: null,
        ),
      ),
    ),
  );

  // ASSERT - Verificar que existe
  expect(find.byType(AuthButton), findsOneWidget);
  expect(find.text('Login'), findsOneWidget);
  expect(find.byType(ElevatedButton), findsOneWidget);
});
```

#### Renderizado con estado:

```dart
testWidgets('debería mostrar indicador de carga cuando isLoading es true', 
    (WidgetTester tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(
        body: AuthButton(
          text: 'Login',
          isLoading: true,
          onPressed: () {},
        ),
      ),
    ),
  );

  expect(find.byType(CircularProgressIndicator), findsOneWidget);
  expect(find.text('Login'), findsNothing); // El texto no se muestra cuando carga
});
```

#### Renderizado condicional:

```dart
testWidgets('debería mostrar ícono cuando se proporciona', (WidgetTester tester) async {
  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(
        body: AuthButton(
          text: 'Login',
          icon: Icons.login,
          onPressed: () {},
        ),
      ),
    ),
  );

  expect(find.byIcon(Icons.login), findsOneWidget);
  expect(find.text('Login'), findsOneWidget);
});
```

---

### Testing de interacciones de usuario

#### Taps y clicks:

```dart
testWidgets('debería llamar onPressed cuando se presiona el botón', 
    (WidgetTester tester) async {
  // ARRANGE
  var wasPressed = false;
  
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: AuthButton(
          text: 'Login',
          onPressed: () => wasPressed = true,
        ),
      ),
    ),
  );

  // ACT
  await tester.tap(find.byType(AuthButton));
  await tester.pump(); // Reconstruir después del tap

  // ASSERT
  expect(wasPressed, isTrue);
});

testWidgets('no debería llamar onPressed cuando está deshabilitado', 
    (WidgetTester tester) async {
  // ARRANGE
  var wasPressed = false;
  
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: AuthButton(
          text: 'Login',
          onPressed: null, // Deshabilitado
        ),
      ),
    ),
  );

  // ACT
  await tester.tap(find.byType(AuthButton));
  await tester.pump();

  // ASSERT - No se debería haber llamado
  expect(wasPressed, isFalse);
});
```

#### Entrada de texto:

```dart
testWidgets('debería actualizar el valor cuando se ingresa texto', 
    (WidgetTester tester) async {
  // ARRANGE
  final controller = TextEditingController();
  
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: EmailInput(controller: controller),
      ),
    ),
  );

  // ACT
  await tester.enterText(
    find.byType(TextField),
    'test@example.com',
  );
  await tester.pump();

  // ASSERT
  expect(controller.text, 'test@example.com');
});
```

#### Múltiples interacciones:

```dart
testWidgets('debería manejar secuencia de interacciones', (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // 1. Ingresar email
  await tester.enterText(
    find.byKey(const Key('email_field')),
    'test@example.com',
  );
  await tester.pump();

  // 2. Ingresar password
  await tester.enterText(
    find.byKey(const Key('password_field')),
    'password123',
  );
  await tester.pump();

  // 3. Presionar botón
  await tester.tap(find.byKey(const Key('login_button')));
  await tester.pump();

  // 4. Verificar resultado
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});
```

---

### Testing de formularios completos

Los formularios son complejos porque involucran validación, estado y múltiples campos.

```dart
group('AuthForm - Testing Completo', () {
  testWidgets('debería mostrar todos los campos inicialmente', (WidgetTester tester) async {
    await tester.pumpWidget(createFormWidget());

    expect(find.byKey(const Key('email_field')), findsOneWidget);
    expect(find.byKey(const Key('password_field')), findsOneWidget);
    expect(find.byKey(const Key('submit_button')), findsOneWidget);
  });

  testWidgets('debería validar email vacío', (WidgetTester tester) async {
    await tester.pumpWidget(createFormWidget());

    // Intentar enviar sin email
    await tester.tap(find.byKey(const Key('submit_button')));
    await tester.pump();

    expect(find.text('Email es requerido'), findsOneWidget);
  });

  testWidgets('debería validar formato de email', (WidgetTester tester) async {
    await tester.pumpWidget(createFormWidget());

    await tester.enterText(
      find.byKey(const Key('email_field')),
      'email-invalido',
    );
    await tester.tap(find.byKey(const Key('submit_button')));
    await tester.pump();

    expect(find.text('Formato de email inválido'), findsOneWidget);
  });

  testWidgets('debería validar contraseña vacía', (WidgetTester tester) async {
    await tester.pumpWidget(createFormWidget());

    // Solo llenar email
    await tester.enterText(
      find.byKey(const Key('email_field')),
      'test@example.com',
    );
    await tester.tap(find.byKey(const Key('submit_button')));
    await tester.pump();

    expect(find.text('Contraseña es requerida'), findsOneWidget);
  });

  testWidgets('debería validar longitud mínima de contraseña', 
      (WidgetTester tester) async {
    await tester.pumpWidget(createFormWidget());

    await tester.enterText(
      find.byKey(const Key('email_field')),
      'test@example.com',
    );
    await tester.enterText(
      find.byKey(const Key('password_field')),
      '123', // Muy corta
    );
    await tester.tap(find.byKey(const Key('submit_button')));
    await tester.pump();

    expect(
      find.text('La contraseña debe tener al menos 6 caracteres'),
      findsOneWidget,
    );
  });

  testWidgets('debería enviar formulario cuando es válido', (WidgetTester tester) async {
    String? submittedEmail;
    String? submittedPassword;

    await tester.pumpWidget(
      MaterialApp(
        home: AuthForm(
          onSubmit: (email, password) {
            submittedEmail = email;
            submittedPassword = password;
          },
        ),
      ),
    );

    // Llenar formulario correctamente
    await tester.enterText(
      find.byKey(const Key('email_field')),
      'test@example.com',
    );
    await tester.enterText(
      find.byKey(const Key('password_field')),
      'password123',
    );
    await tester.tap(find.byKey(const Key('submit_button')));
    await tester.pump();

    expect(submittedEmail, 'test@example.com');
    expect(submittedPassword, 'password123');
  });

  testWidgets('debería limpiar errores al corregir campos', (WidgetTester tester) async {
    await tester.pumpWidget(createFormWidget());

    // Generar error
    await tester.tap(find.byKey(const Key('submit_button')));
    await tester.pump();
    expect(find.text('Email es requerido'), findsOneWidget);

    // Corregir campo
    await tester.enterText(
      find.byKey(const Key('email_field')),
      'test@example.com',
    );
    await tester.pump();

    // Error debería desaparecer
    expect(find.text('Email es requerido'), findsNothing);
  });

  testWidgets('debería deshabilitar botón durante envío', (WidgetTester tester) async {
    await tester.pumpWidget(createFormWidget(isSubmitting: true));

    final button = tester.widget<ElevatedButton>(
      find.byKey(const Key('submit_button')),
    );
    expect(button.enabled, isFalse);
  });

  testWidgets('debería mostrar indicador de carga durante envío', 
      (WidgetTester tester) async {
    await tester.pumpWidget(createFormWidget(isSubmitting: true));

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
    expect(find.text('Enviando...'), findsOneWidget);
  });
});
```

---

### Testing de navegación

```dart
testWidgets('debería navegar a dashboard después de login exitoso', 
    (WidgetTester tester) async {
  // ARRANGE
  final mockNavigator = MockNavigator();
  
  await tester.pumpWidget(
    MaterialApp(
      navigatorObservers: [mockNavigator],
      home: BlocProvider<AuthCubit>.value(
        value: fakeCubit,
        child: const AuthPage(),
      ),
    ),
  );

  // Simular estado autenticado
  fakeCubit.emit(const Authenticated(user: tUser));
  await tester.pumpAndSettle();

  // ASSERT - Verificar navegación
  verify(() => mockNavigator.didPush(any(), any())).called(1);
});

testWidgets('debería navegar a login después de logout', (WidgetTester tester) async {
  await tester.pumpWidget(createAppWithNavigation());

  // Ir al dashboard
  fakeCubit.emit(const Authenticated(user: tUser));
  await tester.pumpAndSettle();

  // Hacer logout
  await tester.tap(find.byKey(const Key('logout_button')));
  await tester.pumpAndSettle();

  // Verificar que volvimos a login
  expect(find.byKey(const Key('login_page')), findsOneWidget);
});

testWidgets('debería navegar a registro al presionar "Crear cuenta"', 
    (WidgetTester tester) async {
  await tester.pumpWidget(createAppWithNavigation());

  await tester.tap(find.text('Crear cuenta'));
  await tester.pumpAndSettle();

  expect(find.byKey(const Key('register_page')), findsOneWidget);
});
```

---

### Testing de diálogos y modales

```dart
testWidgets('debería mostrar diálogo de confirmación al salir', 
    (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Intentar salir
  await tester.tap(find.byKey(const Key('exit_button')));
  await tester.pump();

  // Verificar diálogo
  expect(find.byType(AlertDialog), findsOneWidget);
  expect(find.text('¿Estás seguro de que quieres salir?'), findsOneWidget);
  expect(find.text('Cancelar'), findsOneWidget);
  expect(find.text('Salir'), findsOneWidget);
});

testWidgets('debería cerrar diálogo al presionar Cancelar', (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Abrir diálogo
  await tester.tap(find.byKey(const Key('exit_button')));
  await tester.pump();

  // Presionar cancelar
  await tester.tap(find.text('Cancelar'));
  await tester.pump();

  // Diálogo debería cerrarse
  expect(find.byType(AlertDialog), findsNothing);
});

testWidgets('debería mostrar modal bottom sheet al presionar opciones', 
    (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  await tester.tap(find.byKey(const Key('options_button')));
  await tester.pumpAndSettle();

  expect(find.byType(BottomSheet), findsOneWidget);
  expect(find.text('Opciones'), findsOneWidget);
});
```

---

### Testing de snackbars y toasts

```dart
testWidgets('debería mostrar Snackbar con mensaje de éxito', (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Simular éxito
  fakeCubit.emit(const AuthLoading());
  await tester.pump();
  fakeCubit.emit(const Authenticated(user: tUser));
  await tester.pump();

  // Verificar Snackbar
  expect(find.byType(SnackBar), findsOneWidget);
  expect(find.text('¡Bienvenido!'), findsOneWidget);
});

testWidgets('debería mostrar Snackbar con mensaje de error', (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Simular error
  fakeCubit.emit(const AuthLoading());
  await tester.pump();
  fakeCubit.emit(const AuthError(message: 'Error de conexión'));
  await tester.pump();

  expect(find.byType(SnackBar), findsOneWidget);
  expect(find.text('Error de conexión'), findsOneWidget);
  
  // Verificar color de fondo (rojo para error)
  final snackbar = tester.widget<SnackBar>(find.byType(SnackBar));
  expect(snackbar.backgroundColor, Colors.red);
});
```

---

### Testing de scroll y listas

```dart
testWidgets('debería renderizar lista de usuarios', (WidgetTester tester) async {
  final users = List.generate(
    20,
    (i) => User(
      id: '$i',
      email: 'user$i@example.com',
      name: 'User $i',
      lastName: 'Test',
    ),
  );

  await tester.pumpWidget(
    MaterialApp(
      home: UsersList(users: users),
    ),
  );

  // Verificar que se muestran los primeros elementos
  expect(find.text('User 0'), findsOneWidget);
  expect(find.text('User 1'), findsOneWidget);
  
  // Elementos al final no deberían estar visibles aún
  expect(find.text('User 19'), findsNothing);
});

testWidgets('debería hacer scroll y mostrar más elementos', (WidgetTester tester) async {
  final users = List.generate(50, (i) => User(...));

  await tester.pumpWidget(
    MaterialApp(
      home: UsersList(users: users),
    ),
  );

  // Hacer scroll hacia abajo
  await tester.fling(
    find.byType(ListView),
    const Offset(0, -500), // Scroll hacia arriba (negativo)
    1000,
  );
  await tester.pumpAndSettle();

  // Ahora deberían verse elementos más abajo
  expect(find.text('User 10'), findsOneWidget);
});

testWidgets('debería mostrar indicador de scroll infinito', (WidgetTester tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: UsersList(
        users: [...],
        isLoadingMore: true,
      ),
    ),
  );

  // Hacer scroll hasta el final
  await tester.scrollUntilVisible(
    find.byType(CircularProgressIndicator),
    500,
    scrollable: find.byType(Scrollable),
  );

  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});
```

---

### Testing de gestos

```dart
testWidgets('debería responder a swipe', (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Swipe hacia la izquierda
  await tester.fling(
    find.byKey(const Key('swipeable_card')),
    const Offset(-300, 0),
    1000,
  );
  await tester.pumpAndSettle();

  // Verificar acción de dismiss
  expect(find.text('Elemento eliminado'), findsOneWidget);
});

testWidgets('debería responder a long press', (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  await tester.longPress(find.byKey(const Key('long_press_button')));
  await tester.pump();

  expect(find.byType(ContextMenu), findsOneWidget);
});

testWidgets('debería responder a drag and drop', (WidgetTester tester) async {
  await tester.pumpWidget(createDraggableList());

  // Arrastrar elemento de posición 0 a posición 2
  final firstItem = find.text('Item 0');
  final targetLocation = tester.getCenter(find.text('Item 2'));

  await tester.drag(firstItem, Offset(0, targetLocation.dy - 100));
  await tester.pumpAndSettle();

  // Verificar nuevo orden
  expect(find.text('Item 1'), findsOneWidget);
  expect(find.text('Item 0'), findsOneWidget);
});
```

---

### Testing de animaciones

```dart
testWidgets('debería animar transición de estados', (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Estado inicial
  expect(find.byType(FadeTransition), findsOneWidget);

  // Cambiar estado
  fakeCubit.emit(const AuthLoading());
  await tester.pump();

  // Durante la animación
  await tester.pump(const Duration(milliseconds: 100));
  
  // Animación completada
  await tester.pumpAndSettle();
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});

testWidgets('debería mostrar animación de shake en error', (WidgetTester tester) async {
  await tester.pumpWidget(createWidgetUnderTest());

  // Trigger error
  fakeCubit.emit(const AuthError(message: 'Error'));
  
  // Animación de shake
  await tester.pump();
  await tester.pump(const Duration(milliseconds: 50));
  await tester.pump(const Duration(milliseconds: 100));
  
  // Verificar que el formulario se movió
  final form = tester.widget<Form>(find.byType(Form));
  // Verificar transformación o animación
});
```

---

## Testing de Pages Completas

Cuando testeamos una Page completa, integramos todos los elementos: Cubit, widgets, navegación, etc.

```dart
group('AuthPage - Testing de Integración de Widgets', () {
  late FakeAuthCubit fakeCubit;

  setUp(() {
    fakeCubit = FakeAuthCubit();
  });

  tearDown(() {
    fakeCubit.close();
  });

  Widget createTestableWidget() {
    return MaterialApp(
      home: BlocProvider<AuthCubit>.value(
        value: fakeCubit,
        child: const AuthPage(),
      ),
    );
  }

  testWidgets('debería mostrar UI completa de login', (WidgetTester tester) async {
    await tester.pumpWidget(createTestableWidget());

    // Verificar estructura completa
    expect(find.byType(AppBar), findsOneWidget);
    expect(find.byType(AuthHeader), findsOneWidget);
    expect(find.byType(AuthForm), findsOneWidget);
    expect(find.byType(SocialLoginSection), findsOneWidget);
    expect(find.byType(AuthFooter), findsOneWidget);
  });

  testWidgets('debería cambiar entre login y registro', (WidgetTester tester) async {
    await tester.pumpWidget(createTestableWidget());

    // Inicialmente en login
    expect(find.text('Iniciar Sesión'), findsOneWidget);
    expect(find.byKey(const Key('name_field')), findsNothing);

    // Cambiar a registro
    await tester.tap(find.text('Crear cuenta'));
    await tester.pumpAndSettle();

    // Ahora debería mostrar campos de registro
    expect(find.text('Registrarse'), findsOneWidget);
    expect(find.byKey(const Key('name_field')), findsOneWidget);
    expect(find.byKey(const Key('lastName_field')), findsOneWidget);
  });

  testWidgets('debería manejar flujo completo de autenticación', 
      (WidgetTester tester) async {
    await tester.pumpWidget(createTestableWidget());

    // 1. Estado inicial
    expect(find.byType(AuthForm), findsOneWidget);

    // 2. Ingresar credenciales
    await tester.enterText(
      find.byKey(const Key('email_field')),
      'test@example.com',
    );
    await tester.enterText(
      find.byKey(const Key('password_field')),
      'password123',
    );

    // 3. Presionar login
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pump();

    // 4. Estado de carga
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    // 5. Simular respuesta exitosa
    fakeCubit.emit(const Authenticated(user: tUser));
    await tester.pumpAndSettle();

    // 6. Verificar navegación o mensaje de éxito
    expect(find.byType(SnackBar), findsOneWidget);
  });

  testWidgets('debería manejar errores de red', (WidgetTester tester) async {
    await tester.pumpWidget(createTestableWidget());

    // Intentar login
    await tester.enterText(
      find.byKey(const Key('email_field')),
      'test@example.com',
    );
    await tester.enterText(
      find.byKey(const Key('password_field')),
      'password123',
    );
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pump();

    // Simular error de red
    fakeCubit.emit(const AuthError(message: 'Error de conexión'));
    await tester.pump();

    // Verificar error mostrado
    expect(find.text('Error de conexión'), findsOneWidget);
    expect(find.byIcon(Icons.error), findsOneWidget);

    // Botón de reintentar debería estar disponible
    expect(find.text('Reintentar'), findsOneWidget);
  });

  testWidgets('debería mantener estado del formulario al rotar pantalla', 
      (WidgetTester tester) async {
    await tester.pumpWidget(createTestableWidget());

    // Ingresar datos
    await tester.enterText(
      find.byKey(const Key('email_field')),
      'test@example.com',
    );

    // Simular rotación (cambio de tamaño)
    tester.binding.window.physicalSizeTestValue = const Size(800, 400);
    await tester.pump();

    // Datos deberían mantenerse
    expect(
      find.text('test@example.com'),
      findsOneWidget,
    );

    // Restaurar tamaño
    tester.binding.window.clearPhysicalSizeTestValue();
  });
});
```

---

## Ejercicios Prácticos Avanzados

### Ejercicio 1: Testing de Lista Compleja

Crea tests para una lista que tenga:
- Pull-to-refresh
- Scroll infinito
- Items eliminables con swipe
- Filtros de búsqueda

### Ejercicio 2: Testing de Formulario Multi-Step

Crea tests para un wizard de 3 pasos:
- Navegación entre pasos
- Validación por paso
- Botones de anterior/siguiente
- Resumen final

### Ejercicio 3: Testing de Animaciones Complejas

Crea tests para:
- Hero animations entre pantallas
- Page transitions
- Staggered animations
- Loading skeletons

### Ejercicio 4: Testing de Accesibilidad

Crea tests que verifiquen:
- Labels para screen readers
- Contraste de colores
- Tamaños de touch targets
- Orden de navegación

---

## ✅ Checklist Completo de Presentation Testing

### Cubits:
- [ ] Estado inicial correcto
- [ ] Transiciones de estados (success, error, loading)
- [ ] Múltiples acciones en secuencia
- [ ] Async/await y delays
- [ ] Error handling completo
- [ ] Verificación de dependencias
- [ ] Estados inmutables (Equatable)

### Widgets:
- [ ] Renderizado en diferentes estados
- [ ] Interacciones (tap, input, scroll)
- [ ] Formularios y validaciones
- [ ] Navegación entre pantallas
- [ ] Diálogos y modales
- [ ] Snackbars y feedback
- [ ] Listas y scroll infinito
- [ ] Gestos (swipe, long press)
- [ ] Animaciones

### Pages:
- [ ] Integración completa
- [ ] Flujos de usuario completos
- [ ] Manejo de errores de UI
- [ ] Responsive design
- [ ] Persistencia de estado

---

## 🚀 Siguiente Paso

➡️ **Parte 5: Testing Core y Servicios**

Aprenderás a:
- Testear NetworkInfo y conectividad
- Testear servicios y streams
- Testear storage y preferencias
- Testear utilidades y helpers

---

## 💡 Tips Avanzados

### 1. **Debugging de Widget Tests**
```dart
// Imprimir árbol de widgets
debugDumpApp();

// Tomar screenshot
tester.binding.takeScreenshot('test_screenshot');

// Verificar en qué momento falla
await tester.pump();
debugPrint('Después de pump 1');
await tester.pump();
debugPrint('Después de pump 2');
```

### 2. **Matchers Avanzados**
```dart
// Encontrar widget por tipo y propiedad
find.widgetWithText(ElevatedButton, 'Login');

// Descendant
find.descendant(
  of: find.byType(Form),
  matching: find.byType(TextFormField),
);

// Ancestor
find.ancestor(
  of: find.text('Email'),
  matching: find.byType(Row),
);
```

### 3. **Performance Testing**
```dart
testWidgets('debería renderizar en menos de 100ms', (tester) async {
  final stopwatch = Stopwatch()..start();
  
  await tester.pumpWidget(MyWidget());
  await tester.pumpAndSettle();
  
  stopwatch.stop();
  expect(stopwatch.elapsedMilliseconds, lessThan(100));
});
```

### 4. **Golden File Testing**
```dart
testWidgets('debería coincidir con diseño aprobado', (tester) async {
  await tester.pumpWidget(MyWidget());
  
  await expectLater(
    find.byType(MyWidget),
    matchesGoldenFile('goldens/my_widget.png'),
  );
});
```

### 5. **Testing con Imágenes**
```dart
// Usar imágenes mock para evitar carga de red
setUp(() {
  HttpOverrides.global = TestHttpOverrides();
});

class TestHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..addMockImageResponse(); // Método personalizado
  }
}
```
