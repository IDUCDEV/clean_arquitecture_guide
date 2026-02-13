# 🧪 Parte 6: Testing Avanzado (Fixtures, Integration, Coverage)

## 📋 Índice
1. [Organización Avanzada de Fixtures](#organización-avanzada-de-fixtures)
2. [Integration Tests (E2E)](#integration-tests-e2e)
3. [Coverage de Tests](#coverage-de-tests)
4. [Automation Scripts](#automation-scripts)
5. [CI/CD Integration](#cicd-integration)
6. [Ejercicios Prácticos](#ejercicios-prácticos)

---

## Organización Avanzada de Fixtures

### 📁 Estructura Recomendada

```
test/
├── fixtures/
│   ├── auth/                    ← Fixtures de autenticación
│   │   ├── login_response.json
│   │   ├── register_response.json
│   │   └── user_profile.json
│   ├── errors/                  ← Respuestas de error
│   │   ├── 400_bad_request.json
│   │   ├── 401_unauthorized.json
│   │   ├── 404_not_found.json
│   │   └── 500_server_error.json
│   └── common/                  ← Datos compartidos
│       └── empty_list.json
├── helpers/
│   ├── fixtures/               ← Utilidades de fixtures
│   │   ├── fixture_reader.dart
│   │   └── fixture_builder.dart
│   └── fakes/                  ← Todos los Fakes
│       ├── fake_repositories.dart
│       ├── fake_datasources.dart
│       └── fake_services.dart
└── features/
```

### 📝 Fixture Builder Avanzado

**`test/helpers/fixtures/fixture_builder.dart`**

```dart
import 'dart:convert';

/// Builder pattern para crear fixtures dinámicos
class FixtureBuilder {
  final Map<String, dynamic> _data = {};

  FixtureBuilder withId(String id) {
    _data['id'] = id;
    return this;
  }

  FixtureBuilder withEmail(String email) {
    _data['email'] = email;
    return this;
  }

  FixtureBuilder withName(String name) {
    _data['name'] = name;
    return this;
  }

  FixtureBuilder withLastName(String lastName) {
    _data['last_name'] = lastName;
    return this;
  }

  FixtureBuilder withField(String key, dynamic value) {
    _data[key] = value;
    return this;
  }

  Map<String, dynamic> build() {
    return Map<String, dynamic>.from(_data);
  }

  String buildJson() {
    return json.encode(_data);
  }
}

/// Factory methods predefinidos
class Fixtures {
  static Map<String, dynamic> user({
    String id = '123',
    String email = 'test@example.com',
    String name = 'John',
    String lastName = 'Doe',
  }) {
    return {
      'id': id,
      'email': email,
      'name': name,
      'last_name': lastName,
    };
  }

  static Map<String, dynamic> errorResponse({
    int statusCode = 400,
    String message = 'Error occurred',
    String? code,
  }) {
    return {
      'status_code': statusCode,
      'message': message,
      if (code != null) 'error_code': code,
    };
  }

  static Map<String, dynamic> paginatedResponse({
    required List<Map<String, dynamic>> data,
    int page = 1,
    int perPage = 10,
    int total = 0,
  }) {
    return {
      'data': data,
      'pagination': {
        'page': page,
        'per_page': perPage,
        'total': total,
        'total_pages': (total / perPage).ceil(),
      },
    };
  }
}
```

### 🧪 Uso del Fixture Builder

```dart
// En tus tests
import '../../helpers/fixtures/fixture_builder.dart';

test('should handle user with custom data', () {
  // ARRANGE
  final customUser = FixtureBuilder()
    .withId('custom-123')
    .withEmail('custom@example.com')
    .withName('Custom')
    .withLastName('User')
    .withField('avatar_url', 'https://example.com/avatar.jpg')
    .build();

  // ACT & ASSERT...
});

test('should use predefined fixture', () {
  // ARRANGE
  final user = Fixtures.user(
    email: 'specific@example.com',
    name: 'Specific',
  );

  // ACT & ASSERT...
});
```

---

## Integration Tests (E2E)

Los **Integration Tests** prueban flujos completos de usuario.

### 📁 Estructura

```
integration_test/
└── auth_flow_test.dart          ← Flujo completo de auth
```

### 📝 Flujo de Login Completo

**`integration_test/auth_flow_test.dart`**

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:sereni/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Auth Flow E2E', () {
    testWidgets('complete login flow', (WidgetTester tester) async {
      // ARRANGE - Inicia la app
      app.main();
      await tester.pumpAndSettle();

      // Verifica pantalla inicial de login
      expect(find.byKey(const Key('login_page')), findsOneWidget);

      // ACT - Ingresa email
      await tester.enterText(
        find.byKey(const Key('email_field')),
        'test@example.com',
      );

      // ACT - Ingresa password
      await tester.enterText(
        find.byKey(const Key('password_field')),
        'password123',
      );

      // ACT - Presiona login
      await tester.tap(find.byKey(const Key('login_button')));
      await tester.pumpAndSettle();

      // ASSERT - Verifica navegación al dashboard
      expect(find.byKey(const Key('dashboard_page')), findsOneWidget);
      expect(find.text('Welcome, John!'), findsOneWidget);
    });

    testWidgets('login with invalid credentials shows error', (WidgetTester tester) async {
      // ARRANGE
      app.main();
      await tester.pumpAndSettle();

      // ACT - Intenta login con credenciales inválidas
      await tester.enterText(
        find.byKey(const Key('email_field')),
        'wrong@example.com',
      );
      await tester.enterText(
        find.byKey(const Key('password_field')),
        'wrongpass',
      );
      await tester.tap(find.byKey(const Key('login_button')));
      await tester.pumpAndSettle();

      // ASSERT - Muestra error
      expect(find.text('Invalid credentials'), findsOneWidget);
      expect(find.byKey(const Key('login_page')), findsOneWidget);
    });

    testWidgets('complete logout flow', (WidgetTester tester) async {
      // ARRANGE - Login primero
      app.main();
      await tester.pumpAndSettle();

      await tester.enterText(
        find.byKey(const Key('email_field')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(const Key('password_field')),
        'password123',
      );
      await tester.tap(find.byKey(const Key('login_button')));
      await tester.pumpAndSettle();

      // Verifica que está en dashboard
      expect(find.byKey(const Key('dashboard_page')), findsOneWidget);

      // ACT - Logout
      await tester.tap(find.byKey(const Key('logout_button')));
      await tester.pumpAndSettle();

      // ASSERT - Vuelve a login
      expect(find.byKey(const Key('login_page')), findsOneWidget);
    });
  });
}
```

### 🚀 Ejecución de Integration Tests

```bash
# Ejecutar en emulador/dispositivo conectado
flutter test integration_test/

# Ejecutar un test específico
flutter test integration_test/auth_flow_test.dart

# Ejecutar en dispositivo físico
flutter test integration_test/ -d <device-id>

# Con screenshots (necesita configuración adicional)
flutter test integration_test/ --dart-define=PERF_TEST=true
```

---

## Coverage de Tests

### 📊 Generar Reporte de Coverage

```bash
# 1. Ejecutar tests con coverage
flutter test --coverage

# 2. Instalar lcov (si no lo tienes)
# macOS
brew install lcov

# Linux
sudo apt-get install lcov

# Windows (usando chocolatey)
choco install lcov

# 3. Generar reporte HTML
genhtml coverage/lcov.info -o coverage/html

# 4. Abrir reporte
open coverage/html/index.html        # macOS
xdg-open coverage/html/index.html    # Linux
start coverage/html/index.html       # Windows
```

### 🎯 Cobertura Mínima Recomendada

| Capa | Cobertura Mínima | Prioridad |
|------|------------------|-----------|
| Domain (Entities + UseCases) | 90-100% | 🔴 Alta |
| Data (Models + Repositories) | 80-90% | 🟠 Alta |
| Presentation (Cubits) | 80-90% | 🟡 Media-Alta |
| Core (Utils + Services) | 70-80% | 🟢 Media |
| UI (Widgets) | 60-70% | 🔵 Baja-Media |

### 📝 Configuración de Coverage

**`coverage/lcov.info`** se genera automáticamente, pero puedes excluir archivos:

```bash
# Excluir archivos generados
genhtml coverage/lcov.info -o coverage/html \
  --ignore-errors source \
  --legend \
  --title "Sereni Test Coverage"
```

**`.github/workflows/test.yml`** para CI:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.x.x'
    
    - name: Get dependencies
      run: flutter pub get
    
    - name: Run tests
      run: flutter test --coverage
    
    - name: Check coverage threshold
      run: |
        COVERAGE=$(lcov --summary coverage/lcov.info | grep "lines" | awk '{print $2}' | tr -d '%')
        if (( $(echo "$COVERAGE < 70" | bc -l) )); then
          echo "Coverage $COVERAGE% is below threshold 70%"
          exit 1
        fi
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: coverage/lcov.info
```

---

## Automation Scripts

### 📁 Scripts de Testing

**`scripts/run_tests.sh`**

```bash
#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🧪 Running Flutter Tests...${NC}"

# Run tests
if flutter test; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
else
    echo -e "${RED}❌ Tests failed!${NC}"
    exit 1
fi

# Run coverage (optional)
if [ "$1" = "--coverage" ]; then
    echo -e "${YELLOW}📊 Generating coverage report...${NC}"
    flutter test --coverage
    
    if command -v genhtml &> /dev/null; then
        genhtml coverage/lcov.info -o coverage/html
        echo -e "${GREEN}✅ Coverage report generated: coverage/html/index.html${NC}"
    else
        echo -e "${YELLOW}⚠️  lcov not installed. Install with: brew install lcov${NC}"
    fi
fi

echo -e "${GREEN}🎉 Done!${NC}"
```

**`Makefile`**

```makefile
.PHONY: test test-coverage test-domain test-data test-presentation test-integration

# Run all tests
test:
	flutter test

# Run tests with coverage
test-coverage:
	flutter test --coverage
	@if command -v genhtml >/dev/null 2>&1; then \
		genhtml coverage/lcov.info -o coverage/html; \
		echo "✅ Coverage report: coverage/html/index.html"; \
	else \
		echo "⚠️  Install lcov: brew install lcov"; \
	fi

# Run tests by layer
test-domain:
	flutter test test/features/auth/domain/

test-data:
	flutter test test/features/auth/data/

test-presentation:
	flutter test test/features/auth/presentation/

test-core:
	flutter test test/core/

# Run integration tests
test-integration:
	flutter test integration_test/

# Check code quality
check: format lint test

format:
	flutter format --set-exit-if-changed lib test

lint:
	flutter analyze
```

---

## CI/CD Integration

### 📋 GitHub Actions Workflow Completo

**`.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.x.x'
        cache: true
    
    - name: Get dependencies
      run: flutter pub get
    
    - name: Verify formatting
      run: dart format --output=none --set-exit-if-changed lib test
    
    - name: Analyze project source
      run: flutter analyze --fatal-infos

  test:
    name: Test
    runs-on: ubuntu-latest
    needs: analyze
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.x.x'
        cache: true
    
    - name: Get dependencies
      run: flutter pub get
    
    - name: Run tests
      run: flutter test --coverage --test-randomize-ordering-seed=random
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: coverage/lcov.info
        fail_ci_if_error: true
        verbose: true

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.x.x'
        cache: true
    
    - name: Get dependencies
      run: flutter pub get
    
    - name: Build APK
      run: flutter build apk --release
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: release-apk
        path: build/app/outputs/flutter-apk/app-release.apk
```

---

## Ejercicios Prácticos

### Ejercicio 1: Crear un Integration Test

Crea un integration test que verifique el flujo completo:
1. Registro de nuevo usuario
2. Login con el nuevo usuario
3. Ver perfil
4. Logout

### Ejercicio 2: Configurar Coverage

Configura tu proyecto para:
- Generar reporte de coverage automáticamente
- Excluir archivos de `generated/` del reporte
- Establecer un threshold mínimo de 75%

### Ejercicio 3: Script de Testing

Crea un script que:
- Ejecute tests de una capa específica por parámetro
- Genere coverage solo si se solicita
- Muestre un resumen de resultados con colores

---

## ✅ Checklist de Testing Avanzado

- [ ] Organizar fixtures de forma escalable
- [ ] Usar FixtureBuilder para datos dinámicos
- [ ] Escribir al menos 1 integration test E2E
- [ ] Configurar generación de coverage
- [ ] Establecer thresholds de cobertura
- [ ] Crear scripts de automatización
- [ ] Configurar CI/CD con GitHub Actions
- [ ] Documentar cómo ejecutar tests en README

---

## 🚀 Siguiente Paso

➡️ **Parte 7: Migración a Mockito**

Aprenderás a:
- Cuándo migrar de Fakes a Mocks
- Configurar @GenerateMocks
- Comparación lado a lado
- Pros y contras de cada enfoque

---

## 💡 Tips Adicionales

### 1. **Debugging Integration Tests**
```bash
# Ver logs detallados
flutter test integration_test/ --verbose

# Ejecutar en modo debug
flutter run integration_test/auth_flow_test.dart
```

### 2. **Performance Tests**
```dart
testWidgets('performance test', (tester) async {
  await tester.pumpWidget(MyApp());
  
  final stopwatch = Stopwatch()..start();
  await tester.tap(find.byType(Button));
  await tester.pumpAndSettle();
  stopwatch.stop();
  
  expect(stopwatch.elapsedMilliseconds, lessThan(1000));
});
```

### 3. **Screenshots en CI**
```yaml
- name: Run tests with screenshots
  run: flutter test --dart-define=GOLDEN=true
  
- name: Upload screenshots
  uses: actions/upload-artifact@v3
  with:
    name: screenshots
    path: test/screenshots/
```
