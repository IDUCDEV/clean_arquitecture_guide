# 🏋️ 06a: Práctica - Coverage y CI/CD

> **¿De qué trata esta práctica?** De aprender a medir la cobertura de tus tests y automatizarlos con GitHub Actions.

---

## 📋 Ejercicios

- [Ejercicio 1: Medir coverage](#ejercicio-1-medir-coverage)
- [Ejercicio 2: Configurar GitHub Actions](#ejercicio-2-configurar-github-actions)
- [Ejercicio 3: Configurar threshold de coverage](#ejercicio-3-configurar-threshold-de-coverage)

---

## Ejercicio 1: Medir coverage

### 📝 Tu Misión

Aprender a medir qué porcentaje de tu código está cubierto por tests.

### ✅ Paso 1: Instalar dependencias necesarias

```bash
# Instalar lcov (necesario para generar reportes)
# macOS
brew install lcov

# Linux
sudo apt-get install lcov

# Windows (usar WSL)
```

### ✅ Paso 2: Ejecutar tests con coverage

```bash
flutter test --coverage
```

### ✅ Paso 3: Ver el reporte

```bash
# Generar HTML
genhtml coverage/lcov.info -o coverage/html

# Abrir en navegador
# macOS
open coverage/html/index.html

# Linux
xdg-open coverage/html/index.html
```

### ✅ Paso 4: Entender el reporte

El reporte te mostrará:
- **Line Coverage**: Porcentaje de líneas ejecutadas
- **Functions Coverage**: Porcentaje de funciones ejecutadas
- **Branches Coverage**: Porcentaje de ramas (if/else) ejecutadas

---

## Ejercicio 2: Configurar GitHub Actions

### 📝 Tu Misión

Automatizar los tests en cada push/pull request.

### ✅ Paso 1: Crear workflow

```bash
mkdir -p .github/workflows
touch .github/workflows/flutter-tests.yml
```

### ✅ Paso 2: Escribir el workflow

```yaml
# .github/workflows/flutter-tests.yml
name: Flutter Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: 'stable'
      
      - name: Get dependencies
        run: flutter pub get
      
      - name: Analyze code
        run: flutter analyze
      
      - name: Run tests
        run: flutter test --coverage
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          flags: unittests
          name: flutter-coverage
      
      - name: Check coverage threshold
        run: |
          # Install lcov if needed
          sudo apt-get install -y lcov
          
          # Check line coverage
          LINE_COVERAGE=$(genhtml coverage/lcov.info --output-directory /tmp/coverage-report 2>/dev/null | grep "lines" | grep -oP '\d+%' | tr -d '%')
          
          if [ "$LINE_COVERAGE" -lt 70 ]; then
            echo "Coverage $LINE_COVERAGE% is below threshold of 70%"
            exit 1
          fi
          
          echo "Coverage: $LINE_COVERAGE%"
```

### ✅ Paso 3: Commit y push

```bash
git add .github/workflows/flutter-tests.yml
git commit -m "Add GitHub Actions workflow for tests"
git push origin main
```

---

## Ejercicio 3: Configurar threshold de coverage

### 📝 Tu Misión

Establecer un mínimo de coverage que debe pasar para cada feature.

### ✅ Paso 1: Crear script de verificación

```bash
touch scripts/check_coverage.dart
```

```dart
// scripts/check_coverage.dart
import 'dart:io';

void main(List<String> args) async {
  final minCoverage = int.parse(args.isNotEmpty ? args[0] : '70');
  final lcovFile = File('coverage/lcov.info');
  
  if (!await lcovFile.exists()) {
    print('Error: coverage/lcov.info not found');
    print('Run: flutter test --coverage');
    exit(1);
  }
  
  final content = await lcovFile.readAsString();
  final lines = content.split('\n');
  
  // Buscar la línea de coverage
  double? lineCoverage;
  for (final line in lines) {
    if (line.startsWith('LH')) {
      final parts = line.split(':');
      if (parts.length == 2) {
        final hit = int.tryParse(parts[1].split(' ')[0]) ?? 0;
        // Buscar LR líneas para el hit total
      }
    }
    if (line.startsWith('LF')) {
      final parts = line.split(':');
      if (parts.length == 2) {
        final total = int.tryParse(parts[1]) ?? 0;
        // Buscar LH para obtenerhit
      }
    }
  }
  
  // Método alternativo: usar grep
  final result = await Process.run('sh', [
    '-c',
    'genhtml coverage/lcov.info --output-directory /tmp/report 2>/dev/null | grep "lines"'
  ]);
  
  final output = result.stdout.toString();
  final match = RegExp(r'(\d+)%').firstMatch(output);
  
  if (match != null) {
    final coverage = int.parse(match.group(1)!);
    
    print('Current coverage: $coverage%');
    print('Minimum required: $minCoverage%');
    
    if (coverage < minCoverage) {
      print('❌ Coverage below threshold!');
      exit(1);
    } else {
      print('✅ Coverage check passed!');
      exit(0);
    }
  } else {
    print('Could not parse coverage');
    exit(1);
  }
}
```

### ✅ Paso 2: Usar en CI/CD

Añade al workflow de GitHub Actions después de los tests:

```yaml
      - name: Check coverage threshold
        run: dart run scripts/check_coverage.dart 70
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Coverage ejecutado y reportado
- [ ] Ejercicio 2: GitHub Actions configurado
- [ ] Ejercicio 3: Threshold configurado

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Medir coverage de código
- ✅ Configurar CI/CD con GitHub Actions
- ✅ Establecer umbrales de coverage

---

## 🚀 Siguiente Paso

**Guía:** [Mocktail - Guía Completa](../02-domain/02b-mocktail-guia-completa.md) (incluye sección de migración)
