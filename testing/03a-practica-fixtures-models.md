# 🏋️ 03a: Práctica - Fixtures y Models

> **¿De qué trata esta práctica?** De aprender a crear fixtures JSON y testear Models con ellos.

---

## 📋 Ejercicios

- [Ejercicio 1: Crear archivos fixture JSON](#ejercicio-1-crear-archivos-fixture-json)
- [Ejercicio 2: Crear el helper fixture_reader](#ejercicio-2-crear-el-helper-fixture_reader)
- [Ejercicio 3: Testear fromJson del Model](#ejercicio-3-testear-fromjson-del-model)
- [Ejercicio 4: Testear toJson del Model](#ejercicio-4-testear-tojson-del-model)

---

## Ejercicio 1: Crear archivos fixture JSON

### 📝 Tu Misión

Crear archivos JSON con datos de prueba que usaremos en los tests.

### ✅ Paso 1: Crea la carpeta de fixtures

```bash
mkdir -p test/fixtures
```

### ✅ Paso 2: Crea user.json

Crea `test/fixtures/user.json`:

```json
{
  "id": "123",
  "email": "test@example.com",
  "name": "John",
  "last_name": "Doe"
}
```

### ✅ Paso 3: Crea users_list.json

Crea `test/fixtures/users_list.json`:

```json
[
  {
    "id": "123",
    "email": "user1@example.com",
    "name": "John",
    "last_name": "Doe"
  },
  {
    "id": "456",
    "email": "user2@example.com",
    "name": "Jane",
    "last_name": "Smith"
  }
]
```

### ✅ Paso 4: Crea auth_response.json

Crea `test/fixtures/auth_response.json`:

```json
{
  "user": {
    "id": "789",
    "email": "new@example.com",
    "name": "Alice",
    "last_name": "Johnson"
  },
  "token": "jwt_token_abc123",
  "expires_at": "2024-12-31T23:59:59Z"
}
```

---

## Ejercicio 2: Crear el helper fixture_reader

### 📝 Tu Misión

Crear un helper que facilite leer los archivos fixture.

### ✅ Paso 1: Crea el archivo

```bash
touch test/helpers/fixture_reader.dart
```

### ✅ Paso 2: Implementa las funciones

```dart
// test/helpers/fixture_reader.dart
import 'dart:convert';
import 'dart:io';

/// Lee un archivo fixture JSON de la carpeta test/fixtures/
/// 
/// Uso: 
/// ```dart
/// final jsonString = fixture('user');
/// final jsonMap = json.decode(jsonString);
/// ```
String fixture(String name) {
  final file = File('test/fixtures/$name.json');
  if (!file.existsSync()) {
    throw Exception('Fixture not found: test/fixtures/$name.json');
  }
  return file.readAsStringSync();
}

/// Lee un fixture y lo decodifica como Map
Map<String, dynamic> fixtureAsMap(String name) {
  final content = fixture(name);
  return json.decode(content) as Map<String, dynamic>;
}

/// Lee un fixture y lo decodifica como List
List<dynamic> fixtureAsList(String name) {
  final content = fixture(name);
  return json.decode(content) as List<dynamic>;
}
```

### 🧪 Verifica

```bash
dart analyze test/helpers/fixture_reader.dart
```

---

## Ejercicio 3: Testear fromJson del Model

### 📝 Tu Misión

Escribir tests para verificar que el Model parsea correctamente el JSON.

### ✅ Paso 1: Crea la estructura

```bash
mkdir -p test/features/auth/data/models
touch test/features/auth/data/models/user_model_test.dart
```

### ✅ Paso 2: Escribe el test básico

```dart
// test/features/auth/data/models/user_model_test.dart
import 'dart:convert';
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/data/models/user_model.dart';

import '../../../../helpers/fixture_reader.dart';

void main() {
  // Datos de prueba reutilizables
  const tUserModel = UserModel(
    id: '123',
    email: 'test@example.com',
    name: 'John',
    lastName: 'Doe',
  );

  group('UserModel', () {
    
    group('fromJson', () {
      test('should return valid model from JSON fixture', () {
        // ═══════════════════════════════════════════════════════════
        // ARRANGE: Leer el fixture JSON
        // ═══════════════════════════════════════════════════════════
        final Map<String, dynamic> jsonMap = fixtureAsMap('user');

        // ═══════════════════════════════════════════════════════════
        // ACT: Convertir JSON a Model
        // ═══════════════════════════════════════════════════════════
        final result = UserModel.fromJson(jsonMap);

        // ═══════════════════════════════════════════════════════════
        // ASSERT: Verificar que los datos son correctos
        // ═══════════════════════════════════════════════════════════
        expect(result.id, '123');
        expect(result.email, 'test@example.com');
        expect(result.name, 'John');
        expect(result.lastName, 'Doe');
      });

      test('should return model equal to expected', () {
        // Arrange
        final jsonMap = fixtureAsMap('user');

        // Act
        final result = UserModel.fromJson(jsonMap);

        // Assert
        expect(result, equals(tUserModel));
      });
    });

  });
}
```

### ✅ Paso 3: Añade test de campo faltante

```dart
      test('should throw when required field is missing', () {
        // Arrange - JSON sin el campo 'name'
        final jsonMap = {
          'id': '123',
          'email': 'test@example.com',
          // Falta 'name'
          'last_name': 'Doe',
        };

        // Act & Assert - Debe lanzar excepción
        expect(
          () => UserModel.fromJson(jsonMap),
          throwsA(isA<TypeError>()),
        );
      });
```

### ✅ Paso 4: Añade test de campos extra

```dart
      test('should handle extra fields gracefully', () {
        // Arrange - JSON con campo extra
        final jsonMap = {
          'id': '123',
          'email': 'test@example.com',
          'name': 'John',
          'last_name': 'Doe',
          'extra_field': 'ignored',
        };

        // Act
        final result = UserModel.fromJson(jsonMap);

        // Assert - El campo extra se ignora
        expect(result.id, '123');
      });
```

### 🧪 Ejecuta los tests

```bash
flutter test test/features/auth/data/models/user_model_test.dart
```

---

## Ejercicio 4: Testear toJson del Model

### 📝 Tu Misión

Escribir tests para verificar que el Model serializa correctamente a JSON.

### ✅ Paso 1: Añade tests de toJson

En el mismo archivo, añade:

```dart
    group('toJson', () {
      test('should return a valid JSON map', () {
        // Arrange - el modelo definido al inicio
        const model = tUserModel;

        // Act
        final result = model.toJson();

        // Assert
        expect(result['id'], '123');
        expect(result['email'], 'test@example.com');
        expect(result['name'], 'John');
        expect(result['last_name'], 'Doe');  // snake_case en JSON
      });

      test('toJson and fromJson should be inverse operations', () {
        // Arrange
        const original = tUserModel;

        // Act - Roundtrip: Model → JSON → Model
        final json = original.toJson();
        final recreated = UserModel.fromJson(json);

        // Assert
        expect(recreated.id, original.id);
        expect(recreated.email, original.email);
        expect(recreated.name, original.name);
        expect(recreated.lastName, original.lastName);
      });
    });
```

### ✅ Paso 2: Añade tests de toEntity / fromEntity

```dart
    group('toEntity', () {
      test('should return User entity with correct data', () {
        // Arrange
        const model = tUserModel;

        // Act
        final result = model.toEntity();

        // Assert
        expect(result.id, '123');
        expect(result.email, 'test@example.com');
      });

      test('should create User that is equal to expected entity', () {
        // Arrange
        const model = tUserModel;

        // Act
        final result = model.toEntity();

        // Assert - El modelo puede crear un Entity igual
        expect(result.id, '123');
      });
    });

    group('fromEntity', () {
      test('should return UserModel from User entity', () {
        // Arrange - Un entity (sin los métodos del Model)
        // Simulamos un entity pasando solo los datos
        const entityId = '789';
        const entityEmail = 'entity@example.com';

        // Act - Convertir a Model usando el constructor
        final result = UserModel(
          id: entityId,
          email: entityEmail,
          name: 'Entity',
          lastName: 'User',
        );

        // Assert
        expect(result, isA<UserModel>());
        expect(result.id, entityId);
      });
    });
```

### 🧪 Ejecuta todos los tests

```bash
flutter test test/features/auth/data/models/user_model_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +8: All tests passed!
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: 3 archivos fixture JSON creados
- [ ] Ejercicio 2: Helper fixture_reader.dart creado
- [ ] Ejercicio 3: Tests fromJson (3 tests)
- [ ] Ejercicio 4: Tests toJson y toEntity (5 tests)
- [ ] **Total: 8 tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Crear fixtures JSON reutilizables
- ✅ Usar fixture_reader para cargar datos
- ✅ Testear fromJson con JSON válido
- ✅ Testear manejo de campos faltantes
- ✅ Testear toJson con formato correcto
- ✅ Testear roundtrip (toJson + fromJson)
- ✅ Testear conversión a Entity

---

## 🚀 Siguiente Paso

**Práctica:** [03b-practica-datasources.md](./03b-practica-datasources.md)

> En esta práctica aprenderás a testear **Remote** y **Local DataSources**.
