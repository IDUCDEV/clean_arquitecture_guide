# 🧪 06b: Tests de Integración - Teoría

> **¿De qué trata esta guía?** Los tests unitarios prueban piezas aisladas; los tests de integración prueban que esas piezas **funcionan juntas**. Aquí verás cómo diseñar tests de integración para una app Flutter con Supabase.

---

## 📋 Índice

1. [¿Qué son los Tests de Integración?](#1-qué-son-los-tests-de-integración)
2. [Unit Tests vs Integration Tests](#2-unit-tests-vs-integration-tests)
3. [Flutter Driver vs integration_test](#3-flutter-driver-vs-integration_test)
4. [Configuración](#4-configuración)
5. [Estrategia de Testing con Supabase](#5-estrategia-de-testing-con-supabase)
6. [Organización del Código](#6-organización-del-código)
7. [Buenas Prácticas](#7-buenas-prácticas)

---

## 1. ¿Qué son los Tests de Integración?

### 🎯 Definición

Un **test de integración** verifica que múltiples componentes funcionan correctamente **juntos**. A diferencia del test unitario (que aísla una unidad), el test de integración **atraviesa capas** de la arquitectura.

```
┌─────────────────────────────────────────────────────┐
│              TEST UNITARIO                          │
│  UseCase → [Mock Repository] → UseCase              │
│           (todo aislado)                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│            TEST DE INTEGRACIÓN                       │
│  UseCase → Repository → DataSource → Supabase API   │
│           (flujo real)                               │
└─────────────────────────────────────────────────────┘
```

### 🔍 ¿Qué probamos con integración?

| Componente | Unit Test | Integration Test |
|------------|-----------|-----------------|
| UseCase lógica | ✅ | ✅ |
| Repository implementación | ❌ (mockeado) | ✅ |
| DataSource llamadas HTTP | ❌ (mockeado) | ✅ |
| Supabase Auth API | ❌ (mockeado) | ✅ |
| Realtime subscriptions | ❌ | ✅ |
| Flujo completo login → datos | ❌ | ✅ |

### ¿Cuándo NO usar tests de integración?

- Cuando el test depende de un **tercero no controlable** (ej. pasarela de pago real)
- Para validar **lógica de negocio pura** (eso es trabajo del unit test)
- En **cada commit** (son lentos; ejecútalos en CI antes del merge)

---

## 2. Unit Tests vs Integration Tests

### 📊 Comparativa

| Aspecto | Unit Test | Integration Test |
|---------|-----------|-----------------|
| **Velocidad** | Milisegundos | Segundos o minutos |
| **Aislamiento** | Total | Mínimo (dependencias reales) |
| **Mocks** | Intensivo | Solo para servicios externos no controlables |
| **Cobertura** | Lógica de negocio | Flujos completos |
| **Mantenimiento** | Bajo | Medio (pueden fallar por cambios en API) |
| **Ejecución** | `flutter test` | `flutter test integration_test/` |

### 🎯 Pirámide de Testing

```
         ╱╲
        ╱  ╲        ← E2E (pocos)
       ╱    ╲
      ╱──────╲
     ╱        ╲    ← Integration (algunos)
    ╱          ╲
   ╱────────────╲
  ╱              ╲ ← Unit (muchos)
 ╱────────────────╲
```

Los tests de integración están en el **medio de la pirámide**: más lentos que unitarios, pero más baratos que E2E.

---

## 3. Flutter Driver vs integration_test

### 📊 Comparativa

| Aspecto | `flutter_driver` | `integration_test` |
|---------|-----------------|-------------------|
| **Estado** | Legado | Recomendado |
| **Setup** | Complejo (app separada) | Sencillo (mismo `testWidgets`) |
| **API** | Propietaria (`find.byValueKey`) | `testWidgets` / `tester` |
| **Widget testing** | No | Sí |
| **Reportería** | Limitada | Integrada con `flutter test` |
| **Screenshot** | Manual | Automático con `takeScreenshot` |

### 📝 Ejemplo integration_test

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('login flow', (tester) async {
    await tester.pumpWidget(const MyApp());
    await tester.enterText(find.byType(TextFormField).first, 'email@test.com');
    await tester.tap(find.text('Iniciar sesión'));
    await tester.pumpAndSettle();
    expect(find.text('Bienvenido'), findsOneWidget);
  });
}
```

> Usaremos `integration_test` (el estándar actual).

---

## 4. Configuración

### 📦 pubspec.yaml

```yaml
dev_dependencies:
  integration_test:
    sdk: flutter
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.4      # Para mockear servicios externos
```

### 🗂️ Estructura de carpetas

```
test/
├── unit/                    # Tests unitarios (los que ya tienes)
│   ├── features/
│   └── helpers/
├── integration/             # Tests de integración
│   ├── auth/
│   │   ├── login_test.dart
│   │   └── register_test.dart
│   ├── tasks/
│   │   ├── create_task_test.dart
│   │   └── sync_tasks_test.dart
│   └── helpers/
│       ├── test_app.dart    # App wrapper para tests
│       └── supabase_test_helper.dart  # Setup/teardown Supabase
└── integration_test/        # (alternativa: entrada única)
    └── app_test.dart
```

### 🚀 Scripts de ejecución

```bash
# Todos los tests de integración
flutter test test/integration/

# Test específico
flutter test test/integration/auth/login_test.dart

# Con coverage (unit + integration)
flutter test --coverage test/ && flutter test --coverage test/integration/

# En dispositivo/emulador específico
flutter test -d chrome test/integration/
```

---

## 5. Estrategia de Testing con Supabase

### 🎯 Enfoque: Test Mode + Base de Datos de Prueba

```
Supabase Project
├── production (db real, migraciones estables)
└── preview / test branch (db aislada para tests)
    ├── seeds con datos de prueba
    └── se resetea antes de cada suite
```

### 📝 Helper para Supabase en tests

```dart
// test/integration/helpers/supabase_test_helper.dart
import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseTestHelper {
  static Future<SupabaseClient> setup() async {
    await Supabase.initialize(
      url: const String.fromEnvironment('SUPABASE_URL'),
      anonKey: const String.fromEnvironment('SUPABASE_ANON_KEY'),
    );
    return Supabase.instance.client;
  }

  static Future<void> cleanDatabase(SupabaseClient client) async {
    // Limpiar datos de prueba en orden (FK constraints)
    await client.from('tasks').delete().neq('id', '');
    await client.from('profiles').delete().neq('id', '');
  }

  static Future<void> seedData(SupabaseClient client) async {
    // Insertar datos de prueba
    await client.from('profiles').insert([
      {'id': 'test-user-1', 'email': 'test@test.com', 'name': 'Test'},
    ]);
  }

  static Future<void> tearDown(SupabaseClient client) async {
    await cleanDatabase(client);
    // El cliente se mantiene vivo para toda la suite
  }
}
```

### 📝 Test App Wrapper

```dart
// test/integration/helpers/test_app.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

/// Wrapper que inyecta dependencias reales para tests de integración
class TestApp extends StatelessWidget {
  final Widget child;
  final SupabaseClient Function()? supabaseClientFactory;

  const TestApp({
    super.key,
    required this.child,
    this.supabaseClientFactory,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MultiRepositoryProvider(
        providers: [
          RepositoryProvider<IAuthRepository>(
            create: (_) => AuthRepository(
              remoteDataSource: AuthRemoteDataSource(
                client: supabaseClientFactory?.call()
                    ?? Supabase.instance.client,
              ),
            ),
          ),
          // ... otros providers
        ],
        child: child,
      ),
    );
  }
}
```

### 📝 Flujo completo de un test de integración

```dart
// test/integration/auth/login_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import '../helpers/supabase_test_helper.dart';
import '../helpers/test_app.dart';

void main() {
  late SupabaseClient supabase;

  setUpAll(() async {
    supabase = await SupabaseTestHelper.setup();
    await SupabaseTestHelper.seedData(supabase);
  });

  setUp(() async {
    await SupabaseTestHelper.cleanDatabase(supabase);
    await SupabaseTestHelper.seedData(supabase);
  });

  tearDownAll(() async {
    await SupabaseTestHelper.tearDown(supabase);
  });

  testWidgets('login with valid credentials', (tester) async {
    await tester.pumpWidget(TestApp(
      child: const LoginPage(),
      supabaseClientFactory: () => supabase,
    ));

    await tester.enterText(
      find.byKey(const Key('email_input')),
      'test@test.com',
    );
    await tester.enterText(
      find.byKey(const Key('password_input')),
      'password123',
    );
    await tester.tap(find.byKey(const Key('login_button')));
    await tester.pumpAndSettle();

    expect(find.text('Bienvenido Test'), findsOneWidget);
  });
}
```

---

## 6. Organización del Código

### 📁 Estructura recomendada

```
test/
├── integration/
│   ├── helpers/
│   │   ├── supabase_test_helper.dart
│   │   ├── test_app.dart
│   │   └── test_data.dart
│   ├── auth/
│   │   ├── login_test.dart
│   │   ├── register_test.dart
│   │   └── password_reset_test.dart
│   ├── tasks/
│   │   ├── create_task_test.dart
│   │   ├── list_tasks_test.dart
│   │   └── update_task_test.dart
│   └── supabase/
│       ├── realtime_test.dart
│       └── storage_test.dart
└── unit/                  # Tests unitarios existentes
```

### 📝 Helper: Test Data

```dart
// test/integration/helpers/test_data.dart
class TestData {
  static const testUser = (
    email: 'integration-test@example.com',
    password: 'TestPass123!',
    name: 'Integration',
    lastName: 'Tester',
  );

  static const testTask = (
    title: 'Comprar leche',
    description: 'Ir al supermercado',
    category: 'personal',
  );

  static Map<String, dynamic> userJson() => {
    'email': testUser.email,
    'password': testUser.password,
    'options': {'data': {'name': testUser.name, 'last_name': testUser.lastName}},
  };

  static Map<String, dynamic> taskJson() => {
    'title': testTask.title,
    'description': testTask.description,
    'category': testTask.category,
    'completed': false,
  };
}
```

---

## 7. Buenas Prácticas

### 📝 Reglas de oro

1. **Una base de datos por suite**: usa `setUpAll` para inicializar y no compartas estado entre tests
2. **Limpia entre tests**: `setUp` debe resetear los datos
3. **Seeds predecibles**: datos estáticos, no aleatorios
4. **Timeouts generosos**: `pumpAndSettle` puede tardar con llamadas reales a Supabase
5. **No dependas del orden**: cada test debe ser independiente
6. **Variables de entorno**: nunca hardcodees credenciales
7. **Branch aislada**: usa preview branches de Supabase para testear migraciones
8. **Unit tests primero**: la pirámide manda; no reemplaces unit tests con integration

### ⚠️ Anti-patrones

```dart
// ❌ MAL: Compartir estado entre tests
var sharedUser;
test('register', () async { sharedUser = await register(); });
test('login', () async { await login(sharedUser.email); }); // depende del anterior

// ✅ BIEN: Cada test es independiente
testWidgets('register and login flow', (tester) async {
  await registerUser(tester, testEmail, testPassword);
  await loginUser(tester, testEmail, testPassword);
  expect(find.text('Dashboard'), findsOneWidget);
});
```

```dart
// ❌ MAL: Hardcodear credenciales reales
// ignore: avoid_hardcoded_credentials
const supabaseUrl = 'https://real-project.supabase.co';

// ✅ BIEN: Variables de entorno o --dart-define
const supabaseUrl = String.fromEnvironment('SUPABASE_URL');
```

```dart
// ❌ MAL: Test frágil por depender de datos existentes
final tasks = await supabase.from('tasks').select();
expect(tasks.length, greaterThan(0)); // falla si no hay datos

// ✅ BIEN: Crear tus propios datos en el test
await supabase.from('tasks').insert(testTask);
final tasks = await supabase.from('tasks').select().eq('title', testTask.title);
expect(tasks.length, 1);
```

---

## 🚀 Siguiente Paso

**Práctica:** [06c-practica-flujos-completos.md](./06c-practica-flujos-completos.md) — Tests de integración con Supabase paso a paso
