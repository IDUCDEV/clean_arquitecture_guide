# 06d: Golden Tests (Snapshot Tests)

> Golden tests comparan el rendering de tu widget contra una imagen de referencia. Detectan cambios visuales no intencionados.

---

## Qué son

Un golden test toma un screenshot de tu widget y lo compara contra una imagen guardada (el "golden"). Si el widget cambia visualmente, el test falla.

```
Tu widget → Screenshot → Comparar contra golden → Pass/Fail
```

---

## Cuándo usarlos

| Caso | Usar golden test |
|------|------------------|
| Botones personalizados | ✅ |
| Cards con diseño específico | ✅ |
| Pantallas de login | ✅ |
| Widgets con animaciones | ❌ (inestable) |
| Widgets con datos dinámicos | ❌ (cambia siempre) |
| Layouts responsivos | ⚠️ (solo si fijas tamaño) |

---

## Setup

### 1. Dependencia

```yaml
# pubspec.yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
```

### 2. Habilitar goldens

```bash
flutter test --update-goldens
```

---

## Ejemplo básico

```dart
// test/widget_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_app/widgets/boton_primario.dart';

void main() {
  testWidgets('Botón primario se renderiza correctamente', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: BotonPrimario(
            texto: 'Guardar',
            onPressed: () {},
          ),
        ),
      ),
    );

    // Tomar screenshot y comparar
    await expectLater(
      find.byType(BotonPrimario),
      matchesGoldenFile('goldens/boton_primario.png'),
    );
  });
}
```

---

## Ejemplo: Pantalla completa

```dart
testWidgets('Pantalla de login se renderiza correctamente', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: LoginPage(),
    ),
  );

  // Esperar a que cargue
  await tester.pumpAndSettle();

  await expectLater(
    find.byType(LoginPage),
    matchesGoldenFile('goldens/login_page.png'),
  );
});
```

---

## Comandos útiles

```bash
# Ejecutar golden tests
flutter test

# Actualizar goldens (cuando el cambio es intencionado)
flutter test --update-goldens

# Ejecutar solo un archivo específico
flutter test test/widget_test.dart
```

---

## Buenas prácticas

| Práctica | Por qué |
|----------|---------|
| Golden files en carpeta dedicada | Organización |
| Nombrar descriptivamente | `login_page_dark_mode.png` |
| Actualizar goldens intencionalmente | No automático |
| Probar en distintos tamaños | Responsive |
| No usar con datos dinámicos | Inestable |

---

**Volver al índice:** [README.md](./README.md)
