# 🧪 06c: Práctica - Tests de Integración con Supabase

> **¿Qué vas a aprender?** A escribir tests de integración reales para una app Flutter + Supabase: autenticación, CRUD, Realtime y manejo de errores.

---

## 📋 Índice

1. [Setup del Entorno](#1-setup-del-entorno)
2. [Ejercicio 1: Test de Autenticación](#2-ejercicio-1-test-de-autenticación)
3. [Ejercicio 2: Test de CRUD de Tareas](#3-ejercicio-2-test-de-crud-de-tareas)
4. [Ejercicio 3: Test de Realtime](#4-ejercicio-3-test-de-realtime)
5. [Ejercicio 4: Test de Manejo de Errores](#5-ejercicio-4-test-de-manejo-de-errores)
6. [Ejercicio 5: Test de Flujo Completo](#6-ejercicio-5-test-de-flujo-completo)
7. [Ejecución y CI/CD](#7-ejecución-y-cicd)

---

## 1. Setup del Entorno

### 📦 Dependencias

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
  supabase_flutter: ^2.5.0
```

```bash
flutter pub get
```

### 🗂️ Estructura

```
integration_test/            # Raíz estándar (oficial Flutter)
├── helpers/
│   ├── supabase_test_helper.dart
│   └── test_data.dart
├── auth_test.dart
├── tasks_crud_test.dart
├── realtime_test.dart
├── error_handling_test.dart
└── full_flow_test.dart

test/
└── unit/
```

### 📝 Helpers Base

**`integration_test/helpers/supabase_test_helper.dart`**:

```dart
import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseTestHelper {
  static SupabaseClient? _client;

  static Future<SupabaseClient> setup() async {
    await Supabase.initialize(
      url: const String.fromEnvironment('SUPABASE_URL'),
      anonKey: const String.fromEnvironment('SUPABASE_ANON_KEY'),
    );
    _client = Supabase.instance.client;
    return _client!;
  }

  static Future<void> cleanAll() async {
    final c = _client;
    if (c == null) return;
    await c.from('tasks').delete().neq('id', '0');
    await c.auth.admin.deleteUser(
      (await c.from('profiles').select('id')).map((r) => r['id'] as String).toList(),
    );
  }

  static Future<void> seedProfile(SupabaseClient client, {required String email}) async {
    await client.from('profiles').upsert({
      'id': client.auth.currentUser!.id,
      'email': email,
      'name': 'Integration',
      'last_name': 'Tester',
    });
  }

  static Future<void> tearDown() async {
    await cleanAll();
  }
}
```

**`integration_test/helpers/test_data.dart`**:

```dart
class TestData {
  // Usuario
  static const email = 'integration-test@example.com';
  static const password = 'TestPass123!';
  static const name = 'Integration';
  static const lastName = 'Tester';

  // Tareas
  static const taskTitle = 'Comprar leche';
  static const taskDescription = 'Ir al supermercado antes de las 18:00';
  static const taskCategory = 'personal';
  static const updatedTitle = 'Comprar pan';

  static Map<String, dynamic> profileJson(String id) => {
    'id': id,
    'email': email,
    'name': name,
    'last_name': lastName,
  };
}
```

---

## 2. Ejercicio 1: Test de Autenticación

### 🎯 Objetivo

Probar el flujo completo de autenticación: registro, inicio de sesión, cierre de sesión y verificación de estado.

### 🧪 Código

**`integration_test/auth_test.dart`**:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'helpers/supabase_test_helper.dart';
import 'helpers/test_data.dart';

void main() {
  late SupabaseClient supabase;

  setUpAll(() async {
    supabase = await SupabaseTestHelper.setup();
    // Crear usuario de prueba si no existe
    try {
      await supabase.auth.signUp(
        email: TestData.email,
        password: TestData.password,
      );
    } catch (_) {
      // El usuario puede ya existir, ignoramos
    }
  });

  setUp(() async {
    // Cerrar sesión antes de cada test
    await supabase.auth.signOut();
  });

  tearDownAll(() async {
    await SupabaseTestHelper.tearDown();
  });

  group('Auth Flow', () {
    test('should sign in with valid credentials', () async {
      final response = await supabase.auth.signInWithPassword(
        email: TestData.email,
        password: TestData.password,
      );

      expect(response.user?.email, equals(TestData.email));
      expect(response.session?.accessToken, isNotNull);
      expect(supabase.auth.currentUser, isNotNull);
    });

    test('should fail with wrong password', () async {
      expect(
        () => supabase.auth.signInWithPassword(
          email: TestData.email,
          password: 'wrong-password',
        ),
        throwsA(isA<AuthException>()),
      );

      expect(supabase.auth.currentUser, isNull);
    });

    test('should sign out correctly', () async {
      await supabase.auth.signInWithPassword(
        email: TestData.email,
        password: TestData.password,
      );
      expect(supabase.auth.currentUser, isNotNull);

      await supabase.auth.signOut();
      expect(supabase.auth.currentUser, isNull);
    });

    test('should get session after login', () async {
      await supabase.auth.signInWithPassword(
        email: TestData.email,
        password: TestData.password,
      );

      final session = supabase.auth.currentSession;
      expect(session, isNotNull);
      expect(session!.user.email, equals(TestData.email));
    });
  });
}
```

### 🖥️ Ejecución

```bash
flutter test integration_test/auth_test.dart \
  --dart-define=SUPABASE_URL=https://tu-proyecto.supabase.co \
  --dart-define=SUPABASE_ANON_KEY=tu-anon-key
```

---

## 3. Ejercicio 2: Test de CRUD de Tareas

### 🎯 Objetivo

Probar las operaciones básicas de base de datos: insertar, leer, actualizar y eliminar tareas con RLS.

### 🧪 Código

**`integration_test/tasks_crud_test.dart`**:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'helpers/supabase_test_helper.dart';
import 'helpers/test_data.dart';

void main() {
  late SupabaseClient supabase;

  setUpAll(() async {
    supabase = await SupabaseTestHelper.setup();
    // Autenticar para RLS
    await supabase.auth.signInWithPassword(
      email: TestData.email,
      password: TestData.password,
    );
  });

  setUp(() async {
    await SupabaseTestHelper.cleanAll();
    await SupabaseTestHelper.seedProfile(supabase, email: TestData.email);
  });

  tearDownAll(() async {
    await SupabaseTestHelper.tearDown();
  });

  group('Tasks CRUD', () {
    test('should create a new task', () async {
      final response = await supabase.from('tasks').insert({
        'title': TestData.taskTitle,
        'description': TestData.taskDescription,
        'category': TestData.taskCategory,
        'completed': false,
      }).select().single();

      expect(response['title'], equals(TestData.taskTitle));
      expect(response['completed'], isFalse);
      expect(response['id'], isNotNull);
      expect(response['user_id'], equals(supabase.auth.currentUser!.id));
    });

    test('should list tasks for current user', () async {
      // Insertar 2 tareas
      await supabase.from('tasks').insert([
        {'title': 'Task 1', 'description': 'Desc 1', 'category': 'personal', 'completed': false},
        {'title': 'Task 2', 'description': 'Desc 2', 'category': 'trabajo', 'completed': true},
      ]);

      final tasks = await supabase
          .from('tasks')
          .select()
          .eq('user_id', supabase.auth.currentUser!.id);

      expect(tasks.length, equals(2));
    });

    test('should update a task', () async {
      final task = await supabase.from('tasks').insert({
        'title': TestData.taskTitle,
        'description': TestData.taskDescription,
        'category': TestData.taskCategory,
        'completed': false,
      }).select().single();

      await supabase.from('tasks').update({
        'title': TestData.updatedTitle,
        'completed': true,
      }).eq('id', task['id']);

      final updated = await supabase
          .from('tasks')
          .select()
          .eq('id', task['id'])
          .single();

      expect(updated['title'], equals(TestData.updatedTitle));
      expect(updated['completed'], isTrue);
    });

    test('should delete a task', () async {
      final task = await supabase.from('tasks').insert({
        'title': TestData.taskTitle,
        'description': TestData.taskDescription,
        'category': TestData.taskCategory,
        'completed': false,
      }).select().single();

      await supabase.from('tasks').delete().eq('id', task['id']);

      final tasks = await supabase
          .from('tasks')
          .select()
          .eq('id', task['id']);

      expect(tasks, isEmpty);
    });

    test('should not see other users tasks (RLS)', () async {
      // Crear tarea como usuario actual
      await supabase.from('tasks').insert({
        'title': 'Mi tarea',
        'description': 'Solo visible para mi',
        'category': 'personal',
        'completed': false,
      });

      // Verificar que solo ve nuestras tareas
      final tasks = await supabase.from('tasks').select();
      for (final task in tasks) {
        expect(task['user_id'], equals(supabase.auth.currentUser!.id));
      }
    });
  });
}
```

---

## 4. Ejercicio 3: Test de Realtime

### 🎯 Objetivo

Probar que las suscripciones Realtime reciben cambios en tiempo real.

### 🧪 Código

**`integration_test/realtime_test.dart`**:

```dart
import 'dart:async';
import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'helpers/supabase_test_helper.dart';
import 'helpers/test_data.dart';

void main() {
  late SupabaseClient supabase;

  setUpAll(() async {
    supabase = await SupabaseTestHelper.setup();
    await supabase.auth.signInWithPassword(
      email: TestData.email,
      password: TestData.password,
    );
  });

  setUp(() async {
    await SupabaseTestHelper.cleanAll();
    await SupabaseTestHelper.seedProfile(supabase, email: TestData.email);
  });

  tearDownAll(() async {
    await SupabaseTestHelper.tearDown();
  });

  group('Realtime Subscriptions', () {
    test('should receive insert event via Realtime', () async {
      final completer = Completer<Map<String, dynamic>>();

      final subscription = supabase
          .from('tasks')
          .stream(primaryKey: ['id'])
          .listen((data) {
            if (data.isNotEmpty && !completer.isCompleted) {
              completer.complete(data.last);
            }
          });

      // Esperar a que la subscripción esté activa
      await Future.delayed(const Duration(seconds: 1));

      // Insertar desde el mismo cliente
      await supabase.from('tasks').insert({
        'title': 'Realtime Test',
        'description': 'Test de inserción en tiempo real',
        'category': 'test',
        'completed': false,
      });

      final event = await completer.future.timeout(
        const Duration(seconds: 5),
      );

      expect(event['title'], equals('Realtime Test'));

      await subscription.cancel();
    });

    test('should receive update event via Realtime', () async {
      // Crear tarea primero
      final task = await supabase.from('tasks').insert({
        'title': 'Tarea a actualizar',
        'description': 'Descripción original',
        'category': 'test',
        'completed': false,
      }).select().single();

      final completer = Completer<Map<String, dynamic>>();

      final subscription = supabase
          .from('tasks')
          .stream(primaryKey: ['id'])
          .listen((data) {
            final updated = data.where((t) => t['completed'] == true).toList();
            if (updated.isNotEmpty && !completer.isCompleted) {
              completer.complete(updated.first);
            }
          });

      await Future.delayed(const Duration(seconds: 1));

      await supabase.from('tasks').update({
        'completed': true,
      }).eq('id', task['id']);

      final event = await completer.future.timeout(
        const Duration(seconds: 5),
      );

      expect(event['id'], equals(task['id']));
      expect(event['completed'], isTrue);

      await subscription.cancel();
    });
  });
}
```

---

## 5. Ejercicio 4: Test de Manejo de Errores

### 🎯 Objetivo

Probar que la app maneja correctamente errores de red, autenticación y validación.

### 🧪 Código

**`integration_test/error_handling_test.dart`**:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'helpers/supabase_test_helper.dart';
import 'helpers/test_data.dart';

void main() {
  late SupabaseClient supabase;

  setUpAll(() async {
    supabase = await SupabaseTestHelper.setup();
  });

  group('Error Handling', () {
    test('should throw AuthException on invalid email format', () async {
      expect(
        () => supabase.auth.signUp(
          email: 'not-an-email',
          password: TestData.password,
        ),
        throwsA(isA<AuthException>()),
      );
    });

    test('should throw PostgrestException on invalid table', () async {
      // Sin autenticación
      expect(
        () => supabase.from('non_existent_table').select(),
        throwsA(isA<PostgrestException>()),
      );
    });

    test('should throw AuthException when registering duplicate email', () async {
      // Primer registro
      await supabase.auth.signUp(
        email: 'duplicate-test@example.com',
        password: TestData.password,
      );

      // Segundo registro con el mismo email
      expect(
        () => supabase.auth.signUp(
          email: 'duplicate-test@example.com',
          password: TestData.password,
        ),
        throwsA(isA<AuthException>()),
      );
    });

    test('should handle empty required fields', () async {
      expect(
        () => supabase.from('tasks').insert({
          // title es requerido pero no lo enviamos
          'description': 'Sin título',
        }),
        throwsA(isA<PostgrestException>()),
      );
    });
  });
}
```

---

## 6. Ejercicio 5: Test de Flujo Completo

### 🎯 Objetivo

Probar un flujo de usuario completo: registro → login → crear tarea → actualizar tarea → cerrar sesión.

### 🧪 Código

**`integration_test/full_flow_test.dart`**:

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'helpers/supabase_test_helper.dart';
import 'helpers/test_data.dart';

void main() {
  late SupabaseClient supabase;

  setUpAll(() async {
    supabase = await SupabaseTestHelper.setup();
    await SupabaseTestHelper.cleanAll();
  });

  tearDownAll(() async {
    await SupabaseTestHelper.tearDown();
  });

  test('full user flow: register → login → crud → logout', () async {
    // ── REGISTRO ──
    final signUpResponse = await supabase.auth.signUp(
      email: 'full-flow-test@example.com',
      password: TestData.password,
    );
    expect(signUpResponse.user, isNotNull);
    expect(signUpResponse.user!.email, equals('full-flow-test@example.com'));

    // Cerrar sesión (el registro puede quedar pendiente de confirmación)
    await supabase.auth.signOut();

    // ── LOGIN ──
    final loginResponse = await supabase.auth.signInWithPassword(
      email: 'full-flow-test@example.com',
      password: TestData.password,
    );
    expect(loginResponse.user, isNotNull);
    expect(supabase.auth.currentSession, isNotNull);

    // Crear perfil
    await supabase.from('profiles').upsert({
      'id': loginResponse.user!.id,
      'email': 'full-flow-test@example.com',
      'name': 'Full',
      'last_name': 'Flow',
    });

    // ── CREATE ──
    final task = await supabase.from('tasks').insert({
      'title': 'Mi primera tarea',
      'description': 'Creada en test de flujo completo',
      'category': 'test',
      'completed': false,
    }).select().single();
    expect(task['id'], isNotNull);

    // ── READ ──
    final tasks = await supabase
        .from('tasks')
        .select()
        .eq('user_id', loginResponse.user!.id);
    expect(tasks.length, greaterThanOrEqualTo(1));

    // ── UPDATE ──
    await supabase.from('tasks').update({
      'completed': true,
    }).eq('id', task['id']);

    final updated = await supabase
        .from('tasks')
        .select()
        .eq('id', task['id'])
        .single();
    expect(updated['completed'], isTrue);

    // ── DELETE ──
    await supabase.from('tasks').delete().eq('id', task['id']);

    final afterDelete = await supabase
        .from('tasks')
        .select()
        .eq('id', task['id']);
    expect(afterDelete, isEmpty);

    // ── LOGOUT ──
    await supabase.auth.signOut();
    expect(supabase.auth.currentUser, isNull);
  }, timeout: const Timeout(Duration(seconds: 30)));
}
```

---

## 7. Ejecución y CI/CD

### 🖥️ Ejecución local

```bash
# Un test específico
flutter test integration_test/auth_test.dart \
  --dart-define=SUPABASE_URL=$SUPABASE_URL \
  --dart-define=SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY

# Todos los tests de integración
flutter test integration_test/ \
  --dart-define=SUPABASE_URL=$SUPABASE_URL \
  --dart-define=SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY

# Con cobertura
flutter test integration_test/ --coverage \
  --dart-define=SUPABASE_URL=$SUPABASE_URL \
  --dart-define=SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY
```

### 🔄 GitHub Actions

```yaml
# .github/workflows/integration_tests.yml
name: Integration Tests
on:
  pull_request:
    branches: [main, develop]

env:
  SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
  SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
      - run: flutter pub get
      - run: |
          flutter test integration_test/ \
            --dart-define=SUPABASE_URL=$SUPABASE_URL \
            --dart-define=SUPABASE_ANON_KEY=$SUPABASE_ANON_KEY
```

### ⚠️ Tips para CI

| Problema | Solución |
|----------|----------|
| Tests lentos | Ejecuta solo en PR a main, no en cada commit |
| Datos sucios | Usa preview branches de Supabase |
| Rate limiting | Usa `--concurrency=1` o limita tests paralelos |
| Timeout | Aumenta timeout global en `flutter test --timeout 60s` |
| Credenciales | GitHub Secrets, nunca en el repo |

---

## ✅ Checklist

- [ ] Configurar Supabase Test Helper con `setUp` / `tearDown`
- [ ] Escribir tests de auth (login, logout, registro, errores)
- [ ] Escribir tests CRUD con RLS
- [ ] Escribir tests de Realtime con `stream()`
- [ ] Escribir tests de errores (auth, validación, tabla inexistente)
- [ ] Escribir un test de flujo completo
- [ ] Configurar CI con GitHub Actions
- [ ] Verificar que los tests se ejecutan en aislamiento
- [ ] No hardcodear credenciales (usar `--dart-define`)

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 7: Testing en Supabase (futuro)](./07-supabase-testing.md)
