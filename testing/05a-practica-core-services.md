# 🏋️ 05a: Práctica - Core Services

> **¿De qué trata esta práctica?** De testear los servicios core de tu aplicación: NetworkInfo, Validators, y otros servicios compartidos.

---

## 📋 Ejercicios

- [Ejercicio 1: Testear NetworkInfo](#ejercicio-1-testear-networkinfo)
- [Ejercicio 2: Testear Validators](#ejercicio-2-testear-validators)
- [Ejercicio 3: Testear un Logger](#ejercicio-3-testear-un-logger)

---

## Ejercicio 1: Testear NetworkInfo

### 📝 Tu Misión

Testear el servicio que verifica la conexión a internet.

### ✅ Paso 1: Crea el Fake del connection checker

```bash
mkdir -p test/core/network
touch test/core/network/network_info_test.dart
```

```dart
// test/core/network/network_info_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/network/network_info.dart';

// Fake del connection checker
class FakeInternetConnectionChecker {
  bool hasConnectionValue = true;
  
  Future<bool> get hasConnection async => hasConnectionValue;
}

void main() {
  late NetworkInfoImpl networkInfo;
  late FakeInternetConnectionChecker fakeChecker;

  setUp(() {
    fakeChecker = FakeInternetConnectionChecker();
    networkInfo = NetworkInfoImpl(
      connectionChecker: fakeChecker as dynamic,
    );
  });

  group('isConnected', () {
    test('should return true when connected', () async {
      // ═══════════════════════════════════════════════════════════
      // ARRANGE: Configurar conexión
      // ═══════════════════════════════════════════════════════════
      fakeChecker.hasConnectionValue = true;

      // ═══════════════════════════════════════════════════════════
      // ACT: Verificar conexión
      // ═══════════════════════════════════════════════════════════
      final result = await networkInfo.isConnected;

      // ═══════════════════════════════════════════════════════════
      // ASSERT: Verificar resultado
      // ═══════════════════════════════════════════════════════════
      expect(result, isTrue);
    });

    test('should return false when not connected', () async {
      // Arrange
      fakeChecker.hasConnectionValue = false;

      // Act
      final result = await networkInfo.isConnected;

      // Assert
      expect(result, isFalse);
    });
  });
}
```

---

## Ejercicio 2: Testear Validators

### 📝 Tu Misión

Testear funciones de validación.

### ✅ Paso 1: Crea el archivo de test

```bash
mkdir -p test/core/utils
touch test/core/utils/validators_test.dart
```

### ✅ Paso 2: Implementa las funciones de validación

Crea `lib/features/core/utils/validators.dart`:

```dart
// lib/features/core/utils/validators.dart
class Validators {
  static bool isValidEmail(String email) {
    final regex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return regex.hasMatch(email);
  }

  static bool isValidPassword(String password) {
    return password.length >= 6;
  }

  static String? validateEmail(String? email) {
    if (email == null || email.trim().isEmpty) {
      return 'Email es requerido';
    }
    if (!isValidEmail(email)) {
      return 'Formato de email inválido';
    }
    return null;
  }

  static String? validatePassword(String? password) {
    if (password == null || password.isEmpty) {
      return 'Contraseña es requerida';
    }
    if (!isValidPassword(password)) {
      return 'La contraseña debe tener al menos 6 caracteres';
    }
    return null;
  }
}
```

### ✅ Paso 3: Tests de isValidEmail

```dart
// test/core/utils/validators_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/utils/validators.dart';

void main() {
  group('Validators - isValidEmail', () {
    
    test('should return true for valid email', () {
      expect(Validators.isValidEmail('test@example.com'), isTrue);
      expect(Validators.isValidEmail('user.name@domain.co.uk'), isTrue);
      expect(Validators.isValidEmail('user+tag@example.org'), isTrue);
    });

    test('should return false for invalid email', () {
      expect(Validators.isValidEmail('invalid'), isFalse);
      expect(Validators.isValidEmail('test@'), isFalse);
      expect(Validators.isValidEmail('@example.com'), isFalse);
      expect(Validators.isValidEmail('test@.com'), isFalse);
      expect(Validators.isValidEmail(''), isFalse);
    });
  });

  group('Validators - isValidPassword', () {
    
    test('should return true for password with 6+ characters', () {
      expect(Validators.isValidPassword('123456'), isTrue);
      expect(Validators.isValidPassword('password123'), isTrue);
      expect(Validators.isValidPassword('abcde f'), isTrue);
    });

    test('should return false for short password', () {
      expect(Validators.isValidPassword('12345'), isFalse);
      expect(Validators.isValidPassword(''), isFalse);
    });
  });

  group('Validators - validateEmail', () {
    
    test('should return null for valid email', () {
      expect(Validators.validateEmail('test@example.com'), isNull);
    });

    test('should return error for empty email', () {
      expect(Validators.validateEmail(''), 'Email es requerido');
      expect(Validators.validateEmail(null), 'Email es requerido');
    });

    test('should return error for invalid format', () {
      expect(Validators.validateEmail('invalid'), 'Formato de email inválido');
    });
  });

  group('Validators - validatePassword', () {
    
    test('should return null for valid password', () {
      expect(Validators.validatePassword('password123'), isNull);
    });

    test('should return error for empty password', () {
      expect(Validators.validatePassword(''), 'Contraseña es requerida');
      expect(Validators.validatePassword(null), 'Contraseña es requerida');
    });

    test('should return error for short password', () {
      expect(
        Validators.validatePassword('12345'),
        'La contraseña debe tener al menos 6 caracteres',
      );
    });
  });
}
```

---

## Ejercicio 3: Testear un Logger

### 📝 Tu Misión

Testear un servicio de logging simple.

### ✅ Paso 1: Crea el Logger

Crea `lib/features/core/utils/logger.dart`:

```dart
// lib/features/core/utils/logger.dart

/// Simple logger that stores messages in memory
class Logger {
  final List<String> _logs = [];
  
  /// Log levels
  static const String levelDebug = 'DEBUG';
  static const String levelInfo = 'INFO';
  static const String levelWarning = 'WARNING';
  static const String levelError = 'ERROR';

  /// Get all logs
  List<String> get logs => List.unmodifiable(_logs);

  /// Log a debug message
  void debug(String message) => _log(levelDebug, message);

  /// Log an info message
  void info(String message) => _log(levelInfo, message);

  /// Log a warning message
  void warning(String message) => _log(levelWarning, message);

  /// Log an error message
  void error(String message) => _log(levelError, message);

  void _log(String level, String message) {
    final timestamp = DateTime.now().toIso8601String();
    _logs.add('[$timestamp] $level: $message');
  }

  /// Clear all logs
  void clear() => _logs.clear();

  /// Get logs by level
  List<String> getLogsByLevel(String level) {
    return _logs.where((log) => log.contains(level)).toList();
  }
}
```

### ✅ Paso 2: Crea los tests

```bash
touch test/core/utils/logger_test.dart
```

```dart
// test/core/utils/logger_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/core/utils/logger.dart';

void main() {
  late Logger logger;

  setUp(() {
    logger = Logger();
  });

  group('Logger', () {
    
    group('basic logging', () {
      test('should add debug message', () {
        logger.debug('Debug message');
        
        expect(logger.logs.length, 1);
        expect(logger.logs.first, contains('DEBUG'));
        expect(logger.logs.first, contains('Debug message'));
      });

      test('should add info message', () {
        logger.info('Info message');
        
        expect(logger.logs.length, 1);
        expect(logger.logs.first, contains('INFO'));
      });

      test('should add warning message', () {
        logger.warning('Warning message');
        
        expect(logger.logs.length, 1);
        expect(logger.logs.first, contains('WARNING'));
      });

      test('should add error message', () {
        logger.error('Error message');
        
        expect(logger.logs.length, 1);
        expect(logger.logs.first, contains('ERROR'));
      });
    });

    group('clear', () {
      test('should clear all logs', () {
        logger.info('Message 1');
        logger.info('Message 2');
        logger.info('Message 3');
        
        expect(logger.logs.length, 3);
        
        logger.clear();
        
        expect(logger.logs.length, 0);
      });
    });

    group('getLogsByLevel', () {
      test('should filter logs by level', () {
        logger.debug('Debug 1');
        logger.info('Info 1');
        logger.warning('Warning 1');
        logger.error('Error 1');
        
        final debugLogs = logger.getLogsByLevel(Logger.levelDebug);
        
        expect(debugLogs.length, 1);
        expect(debugLogs.first, contains('Debug 1'));
      });

      test('should return empty list when no matches', () {
        logger.info('Some info');
        
        final errorLogs = logger.getLogsByLevel(Logger.levelError);
        
        expect(errorLogs.length, 0);
      });
    });

    group('immutability', () {
      test('logs should be unmodifiable', () {
        logger.info('Test');
        
        expect(() => logger.logs.add('Hacked!'), throwsUnsupportedError);
      });
    });
  });
}
```

---

## 🧪 Ejecuta todos los tests

```bash
flutter test test/core/
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +15: All tests passed!
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Tests NetworkInfo (2 tests)
- [ ] Ejercicio 2: Tests Validators (11 tests)
- [ ] Ejercicio 3: Tests Logger (9 tests)
- [ ] **Total: 22+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Testear servicios de conectividad (NetworkInfo)
- ✅ Testear funciones de validación
- ✅ Testear servicios con estado (Logger)

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 6: Testing Avanzado](./06-advanced-testing.md)

**Práctica:** [06a-practica-coverage-ci.md](./06a-practica-coverage-ci.md)

> En esta práctica aprenderás a medir coverage y configurar CI/CD.
