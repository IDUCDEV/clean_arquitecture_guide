# 🧪 06b: Tests de Integración - Teoría

> **¿De qué trata esta guía?** Los tests unitarios prueban piezas aisladas; los tests de integración prueban que esas piezas **funcionan juntas**. Aquí verás cómo diseñar tests de integración para una app Flutter con Supabase.

---

## 📋 Índice

1. [¿Qué son los Tests de Integración?](#1-qué-son-los-tests-de-integración)
2. [Unit Tests vs Integration Tests](#2-unit-tests-vs-integration-tests)
3. [Flutter Driver vs integration_test](#3-flutter-driver-vs-integration_test)
4. [Patrol: alternativa para UI nativa](#4-patrol-alternativa-para-ui-nativa)
5. [Configuración](#5-configuración)
6. [Estrategia de Testing con Supabase](#6-estrategia-de-testing-con-supabase)
7. [Organización del Código](#7-organización-del-código)
8. [Buenas Prácticas](#8-buenas-prácticas)
9. [Performance Profiling](#9-performance-profiling)
10. [Firebase Test Lab](#10-firebase-test-lab)
11. [Setup por Plataforma](#11-setup-por-plataforma)
12. [Migración desde flutter_driver](#12-migración-desde-flutter_driver)

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

## 4. Patrol: alternativa para UI nativa

> La documentación oficial de Flutter recomienda `patrol` como alternativa cuando necesitas interactuar con UI nativa (diálogos de permisos, notificaciones push, platform views).

### 📊 integration_test vs patrol

| Aspecto | `integration_test` | `patrol` |
|---------|-------------------|----------|
| **UI Flutter** | ✅ Completo | ✅ Completo |
| **Diálogos nativos (permisos)** | ❌ No | ✅ Sí |
| **Notificaciones push** | ❌ No | ✅ Sí |
| **Platform Views** | ❌ No | ✅ Sí |
| **Setup** | Mínimo | Requiere configuración nativa |
| **CI/CD** | `flutter test` | `patrol test` |

### 📝 ¿Cuándo usar cada uno?

- **Usa `integration_test`** si tu app solo interactúa con widgets Flutter y servicios como Supabase.
- **Usa `patrol`** si necesitas aceptar diálogos de permisos (cámara, ubicación), verificar notificaciones push, o interactuar con vistas nativas.

### 📦 Dependencia

```yaml
dev_dependencies:
  patrol: ^3.0.0
```

```bash
patrol init  # Configura proyecto para patrol
```

### 📝 Ejemplo básico con patrol

```dart
import 'package:patrol/patrol.dart';

void main() {
  patrolTest('login flow with permission', ($) async {
    await $.pumpWidgetAndSettle(const MyApp());

    // Interactuar con UI Flutter
    await $(#email_input).enterText('email@test.com');
    await $(#login_button).tap();

    // Aceptar diálogo nativo de permiso
    await $.native.handlePermission();
    await $.native.grantPermissionWhenInUse();

    expect($(#welcome_text), findsOneWidget);
  });
}
```

> Si tu app solo usa Supabase sin funcionalidades nativas complejas, `integration_test` es suficiente. `patrol` es útil cuando agregas features como cámara, notificaciones o mapas.

---

## 5. Configuración

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
integration_test/            # Raíz estándar para integration tests
├── auth/
│   ├── login_test.dart
│   └── register_test.dart
├── tasks/
│   ├── create_task_test.dart
│   └── sync_tasks_test.dart
└── helpers/
    ├── test_app.dart        # App wrapper para tests
    ├── supabase_test_helper.dart  # Setup/teardown Supabase
    └── test_data.dart       # Datos de prueba

test/
├── unit/                    # Tests unitarios (los que ya tienes)
│   ├── features/
│   └── helpers/
└── widget/                  # Widget tests
```

> **Convención oficial de Flutter**: los integration tests se colocan en `integration_test/` (raíz del proyecto), no dentro de `test/`. Esto permite usar `flutter test integration_test/` directamente.

### 🚀 Scripts de ejecución

```bash
# Todos los tests de integración
flutter test integration_test/

# Test específico
flutter test integration_test/auth/login_test.dart

# Con coverage (unit + integration)
flutter test --coverage

# En dispositivo/emulador específico
flutter test -d chrome integration_test/
```

---

## 6. Estrategia de Testing con Supabase

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
// integration_test/helpers/supabase_test_helper.dart
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
// integration_test/helpers/test_app.dart
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
// integration_test/auth/login_test.dart
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

## 7. Organización del Código

### 📁 Estructura recomendada

```
integration_test/            # Integration tests (estándar oficial)
├── helpers/
│   ├── supabase_test_helper.dart
│   ├── test_app.dart
│   └── test_data.dart
├── auth/
│   ├── login_test.dart
│   ├── register_test.dart
│   └── password_reset_test.dart
├── tasks/
│   ├── create_task_test.dart
│   ├── list_tasks_test.dart
│   └── update_task_test.dart
└── supabase/
    ├── realtime_test.dart
    └── storage_test.dart

test/
└── unit/                  # Tests unitarios existentes
```

### 📝 Helper: Test Data

```dart
// integration_test/helpers/test_data.dart
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

## 8. Buenas Prácticas

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

## 9. Performance Profiling

> La documentación oficial de Flutter incluye una guía completa para medir rendimiento con integration tests: [Measure performance with an integration test](https://docs.flutter.dev/cookbook/testing/integration/profiling)

### 🎯 ¿Por qué medir rendimiento?

Los integration tests no solo verifican funcionalidad, también pueden capturar **métricas de rendimiento** como frames perdidos (jank), tiempos de build y painted frames.

### 📝 Uso de traceAction

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('scroll performance', (tester) async {
    await tester.pumpWidget(const MyApp());

    final listFinder = find.byType(ListView);
    final itemFinder = find.text('Item 50');

    await binding.traceAction(
      () async {
        await tester.scrollUntilVisible(
          itemFinder,
          500,
          scrollable: listFinder,
        );
      },
      reportKey: 'scrolling_timeline',
    );
  });
}
```

### 📊 TimelineSummary

Para analizar los resultados, usa `TimelineSummary`:

```dart
// integration_test/helpers/performance_helper.dart
Future<void> savePerformanceData(Map<String, dynamic>? data) async {
  if (data == null) return;

  final timeline = Timeline.fromJson(
    data['scrolling_timeline'] as Map<String, dynamic>,
  );
  final summary = TimelineSummary.summarize(timeline);

  // Guarda el timeline completo para chrome://tracing
  await summary.writeTimelineToFile(
    'scrolling_timeline',
    pretty: true,
    includeSummary: true,
  );
}
```

### 🚀 Ejecutar con profile mode

```bash
# Ejecutar con profile mode para mediciones realistas
flutter drive \
  --driver=test_driver/perf_driver.dart \
  --target=integration_test/scrolling_test.dart \
  --profile

# En dispositivo móvil, desactivar DDS
flutter drive \
  --driver=test_driver/perf_driver.dart \
  --target=integration_test/scrolling_test.dart \
  --profile --no-dds
```

La flag `--profile` compila la app en **profile mode**, que tiene un rendimiento más cercano al de producción que debug mode.

### 📈 Métricas clave

| Métrica | Descripción |
|---------|-------------|
| **average_frame_build_time** | Tiempo promedio de build por frame |
| **90th_percentile_frame_build_time** | Percentil 90 (identifica picos) |
| **99th_percentile_frame_rasterizer_time** | Percentil 99 de rasterización |
| **frame_count** | Total de frames renderizados |
| **frame_build_count** | Frames construidos (debe ser ≈ total) |

---

## 10. Firebase Test Lab

> Firebase Test Lab permite ejecutar integration tests en una matriz de **dispositivos reales y virtuales** en la nube. Ideal para CI/CD.

### 🎯 Beneficios

- Pruebas en múltiples dispositivos simultáneamente
- Cobertura de versiones de SO
- Captura de logs, screenshots y video
- Integración nativa con GitHub Actions

### 📝 Configuración para Android

1. **Agregar dependencia** en `android/app/build.gradle`:

```groovy
android {
  defaultConfig {
    testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
  }
}
```

2. **Crear el runner de prueba** `android/app/src/androidTest/java/com/example/app/MainActivityTest.java`:

```java
package com.example.app;

import androidx.test.rule.ActivityTestRule;
import dev.flutter.plugins.integration_test.FlutterTestRunner;
import org.junit.Rule;
import org.junit.runner.RunWith;

@RunWith(FlutterTestRunner.class)
public class MainActivityTest {
  @Rule
  public ActivityTestRule<MainActivity> rule = new ActivityTestRule<>(MainActivity.class);
}
```

3. **Compilar el APK de prueba**:

```bash
# APK de la app
flutter build apk --debug

# APK de test
./gradlew app:assembleAndroidTest
./gradlew app:assembleDebug -Ptarget=integration_test/app_test.dart
```

### 📝 Configuración para iOS

1. **Crear el runner** en `ios/Runner/AppTest.swift`:

```swift
import Flutter
import UIKit
import XCTest

@testable import app

class AppTest: FlutterTestRunner {
  func testApp() {
    let app = XCUIApplication()
    app.launch()
  }
}
```

2. **Compilar para Test Lab**:

```bash
flutter build ios --debug --no-codesign
cd ios
xcodebuild -workspace Runner.xcworkspace \
  -scheme Runner \
  -sdk iphoneos \
  -destination 'platform=iOS,name=Any iOS Device' \
  build-for-testing
```

### 🤖 CI/CD con Firebase Test Lab

```yaml
# .github/workflows/test_lab.yml
name: Firebase Test Lab

on:
  pull_request:
    branches: [main]

jobs:
  test_lab:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
      - run: flutter pub get

      - name: Build Android APK
        run: flutter build apk --debug

      - name: Build Android Test APK
        run: cd android && ./gradlew app:assembleAndroidTest

      - name: Run on Firebase Test Lab
        uses: google-github-actions/firebase-test-lab@v3
        with:
          project: ${{ secrets.FIREBASE_PROJECT_ID }}
          devices: |
            - model: Pixel4
              version: 30
              locale: es
            - model: Pixel6
              version: 33
              locale: es
          type: instrumentation
          app: build/app/outputs/apk/debug/app-debug.apk
          test: android/app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk
```

### ⚠️ Limitaciones de Test Lab

- **No hay tiempo individual por test case**: la duración se reporta por suite completa
- **Robo tests no soportan Flutter nativamente**: usa Robo scripts con clics por texto
- **Timeouts**: máximo 30 minutos por test en dispositivos físicos

---

## 11. Setup por Plataforma

Según la documentación oficial de Flutter, cada plataforma requiere configuración específica para ejecutar integration tests.

### 🖥️ Desktop (Linux, macOS, Windows)

```bash
# Ejecutar directamente (sin configuración adicional)
flutter test integration_test/
```

Los tests de escritorio se ejecutan en el mismo entorno, no requieren configuración especial.

### 📱 Android

1. Asegúrate de tener un emulador corriendo o dispositivo conectado:

```bash
flutter devices
```

2. Ejecutar:

```bash
flutter test integration_test/ -d android
```

3. Para dispositivos físicos, configura `android/app/build.gradle`:

```groovy
android {
  defaultConfig {
    minSdkVersion 21
    targetSdkVersion 34
    testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
  }
}
```

### 📱 iOS

1. Asegúrate de tener un simulador corriendo:

```bash
open -a Simulator
flutter devices
```

2. Ejecutar:

```bash
flutter test integration_test/ -d ios
```

3. Si usas Firebase Test Lab, necesitas configurar el runner en `ios/Runner/`.

### 🌐 Web

```bash
# Chrome
flutter test integration_test/ -d chrome

# Sin interfaz gráfica (CI)
flutter test integration_test/ -d web-server --release
```

> **Nota**: Performance profiling no está soportado en web.

---

## 12. Migración desde flutter_driver

Si ya tienes tests escritos con `flutter_driver`, la migración a `integration_test` es sencilla.

### 📊 Cambios principales

| flutter_driver | integration_test |
|---------------|------------------|
| `FlutterDriver.connect()` | `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` |
| `driver.tap(find.byValueKey('key'))` | `await tester.tap(find.byKey(const Key('key')))` |
| `driver.getText(find.byValueKey('text'))` | `expect(find.text('Hello'), findsOneWidget)` |
| `driver.scrollUntilVisible(...)` | `await tester.scrollUntilVisible(...)` |
| App separada en `test_driver/` | Misma app en `integration_test/` |
| `flutter drive` | `flutter test integration_test/` |

### 📝 Ejemplo de migración

**Antes (flutter_driver)**:
```dart
// test_driver/app_test.dart
import 'package:flutter_driver/flutter_driver.dart';

void main() {
  group('App', () {
    late FlutterDriver driver;

    setUpAll(() async {
      driver = await FlutterDriver.connect();
    });

    tearDownAll(() async {
      driver.close();
    });

    test('shows counter', () async {
      final counter = find.byValueKey('counter');
      expect(await driver.getText(counter), '0');
    });
  });
}
```

**Después (integration_test)**:
```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('shows counter', (tester) async {
    await tester.pumpWidget(const MyApp());
    expect(find.text('0'), findsOneWidget);
  });
}
```

### 🗑️ Limpieza post-migración

```bash
# Eliminar archivos antiguos
rm -rf test_driver/

# Eliminar dependencia del pubspec.yaml
# flutter_driver: sdk: flutter  ← eliminar

# Agregar integration_test
# flutter pub add dev:integration_test
```

> La guía oficial de migración está en: [Migrating from flutter_driver](https://docs.flutter.dev/release/breaking-changes/flutter-driver-migration)

---

## 🚀 Siguiente Paso

**Práctica:** [06c-practica-flujos-completos.md](./06c-practica-flujos-completos.md) — Tests de integración con Supabase paso a paso
