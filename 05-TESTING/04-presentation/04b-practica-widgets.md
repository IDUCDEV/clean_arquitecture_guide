# 🏋️ 04b: Práctica - Widget Tests

> **¿De qué trata esta práctica?** De testear la interfaz de usuario: botones, formularios, y cómo responden a las interacciones del usuario.

---

## 📋 Ejercicios

- [Ejercicio 1: Testear renderizado básico](#ejercicio-1-testear-renderizado-básico)
- [Ejercicio 2: Testear interacciones (tap)](#ejercicio-2-testear-interacciones-tap)
- [Ejercicio 3: Testear entrada de texto](#ejercicio-3-testear-entrada-de-texto)
- [Ejercicio 4: Testear formulario](#ejercicio-4-testear-formulario)

---

## 🎬 Antes de Empezar

Asegúrate de tener `flutter_test` en pubspec.yaml:

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
```

---

## Ejercicio 1: Testear renderizado básico

### 📝 Tu Misión

Verificar que un widget se renderiza correctamente.

### ✅ Paso 1: Crea un widget simple

Crea `lib/features/features/auth/presentation/widgets/login_button.dart`:

```dart
// lib/features/features/auth/presentation/widgets/login_button.dart
import 'package:flutter/material.dart';

class LoginButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final bool isLoading;

  const LoginButton({
    super.key,
    required this.text,
    this.onPressed,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: isLoading ? null : onPressed,
      child: isLoading
          ? const SizedBox(
              height: 20,
              width: 20,
              child: CircularProgressIndicator(strokeWidth: 2),
            )
          : Text(text),
    );
  }
}
```

### ✅ Paso 2: Crea el archivo de test

```bash
mkdir -p test/features/auth/presentation/widgets
touch test/features/auth/presentation/widgets/login_button_test.dart
```

### ✅ Paso 3: Escribe el test de renderizado

```dart
// test/features/auth/presentation/widgets/login_button_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/widgets/login_button.dart';

void main() {
  group('LoginButton', () {
    
    testWidgets('debería renderizar el texto del botón', (tester) async {
      // ═══════════════════════════════════════════════════════════
      // ARRANGE & ACT: Renderizar el widget
      // ═══════════════════════════════════════════════════════════
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: LoginButton(
              text: 'Iniciar Sesión',
              onPressed: null,
            ),
          ),
        ),
      );

      // ═══════════════════════════════════════════════════════════
      // ASSERT: Verificar que existe
      // ═══════════════════════════════════════════════════════════
      expect(find.text('Iniciar Sesión'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });

    testWidgets('debería mostrar indicador de carga cuando isLoading es true', (tester) async {
      // Arrange & Act
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: LoginButton(
              text: 'Iniciar Sesión',
              onPressed: () {},
              isLoading: true,
            ),
          ),
        ),
      );

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.text('Iniciar Sesión'), findsNothing); // No muestra texto cuando carga
    });

    testWidgets('debería mostrar texto cuando no está cargando', (tester) async {
      // Arrange & Act
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: LoginButton(
              text: 'Iniciar Sesión',
              onPressed: () {},
              isLoading: false,
            ),
          ),
        ),
      );

      // Assert
      expect(find.text('Iniciar Sesión'), findsOneWidget);
      expect(find.byType(CircularProgressIndicator), findsNothing);
    });
  });
}
```

### 🧪 Ejecuta los tests

```bash
flutter test test/features/auth/presentation/widgets/login_button_test.dart
```

---

## Ejercicio 2: Testear interacciones (tap)

### 📝 Tu Misión

Verificar que al presionar un botón, se llama al callback.

### ✅ Paso 1: Añade tests de tap

```dart
    testWidgets('debería llamar a onPressed cuando se presiona el botón', (tester) async {
      // ═══════════════════════════════════════════════════════════
      // ARRANGE: Crear callback
      // ═══════════════════════════════════════════════════════════
      var wasPressed = false;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LoginButton(
              text: 'Iniciar Sesión',
              onPressed: () => wasPressed = true,
            ),
          ),
        ),
      );

      // ═══════════════════════════════════════════════════════════
      // ACT: Simular tap
      // ═══════════════════════════════════════════════════════════
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // ═══════════════════════════════════════════════════════════
      // ASSERT: Verificar que se llamó
      // ═══════════════════════════════════════════════════════════
      expect(wasPressed, isTrue);
    });

    testWidgets('no debería llamar a onPressed cuando está deshabilitado', (tester) async {
      // Arrange
      var wasPressed = false;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LoginButton(
              text: 'Iniciar Sesión',
              onPressed: null, // Deshabilitado
            ),
          ),
        ),
      );

      // Act
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert
      expect(wasPressed, isFalse);
    });

    testWidgets('no debería llamar a onPressed cuando está cargando', (tester) async {
      // Arrange
      var wasPressed = false;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LoginButton(
              text: 'Iniciar Sesión',
              onPressed: () => wasPressed = true,
              isLoading: true, // Cargando
            ),
          ),
        ),
      );

      // Act
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      // Assert
      expect(wasPressed, isFalse);
    });
```

---

## Ejercicio 3: Testear entrada de texto

### 📝 Tu Misión

Crear y testear un widget de campo de email.

### ✅ Paso 1: Crea el widget EmailInput

Crea `lib/features/features/auth/presentation/widgets/email_input.dart`:

```dart
// lib/features/features/auth/presentation/widgets/email_input.dart
import 'package:flutter/material.dart';

class EmailInput extends StatelessWidget {
  final TextEditingController controller;
  final String? errorText;
  final ValueChanged<String>? onChanged;

  const EmailInput({
    super.key,
    required this.controller,
    this.errorText,
    this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      keyboardType: TextInputType.emailAddress,
      decoration: InputDecoration(
        labelText: 'Email',
        errorText: errorText,
      ),
      onChanged: onChanged,
    );
  }
}
```

### ✅ Paso 2: Crea los tests

```bash
touch test/features/auth/presentation/widgets/email_input_test.dart
```

```dart
// test/features/auth/presentation/widgets/email_input_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/widgets/email_input.dart';

void main() {
  group('EmailInput', () {
    
    testWidgets('debería renderizar el campo de texto', (tester) async {
      final controller = TextEditingController();
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: EmailInput(controller: controller),
          ),
        ),
      );

      expect(find.byType(TextField), findsOneWidget);
      expect(find.text('Email'), findsOneWidget);
    });

    testWidgets('debería actualizar el valor cuando se ingresa texto', (tester) async {
      final controller = TextEditingController();
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: EmailInput(controller: controller),
          ),
        ),
      );

      // Act
      await tester.enterText(find.byType(TextField), 'test@example.com');
      await tester.pump();

      // Assert
      expect(controller.text, 'test@example.com');
    });

    testWidgets('debería mostrar mensaje de error cuando se proporciona', (tester) async {
      final controller = TextEditingController();
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: EmailInput(
              controller: controller,
              errorText: 'Email inválido',
            ),
          ),
        ),
      );

      // Assert
      expect(find.text('Email inválido'), findsOneWidget);
    });

    testWidgets('debería llamar a onChanged cuando cambia el texto', (tester) async {
      final controller = TextEditingController();
      String? changedValue;
      
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: EmailInput(
              controller: controller,
              onChanged: (value) => changedValue = value,
            ),
          ),
        ),
      );

      // Act
      await tester.enterText(find.byType(TextField), 'new@example.com');
      await tester.pump();

      // Assert
      expect(changedValue, 'new@example.com');
    });
  });
}
```

---

## Ejercicio 4: Testear formulario

### 📝 Tu Misión

Testear un formulario completo de login.

### ✅ Paso 1: Crea el widget AuthForm

Crea `lib/features/features/auth/presentation/widgets/auth_form.dart`:

```dart
// lib/features/features/auth/presentation/widgets/auth_form.dart
import 'package:flutter/material.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/widgets/email_input.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/widgets/login_button.dart';

class AuthForm extends StatefulWidget {
  final void Function(String email, String password) onSubmit;
  final bool isLoading;

  const AuthForm({
    super.key,
    required this.onSubmit,
    this.isLoading = false,
  });

  @override
  State<AuthForm> createState() => _AuthFormState();
}

class _AuthFormState extends State<AuthForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  String? _emailError;
  String? _passwordError;

  void _validateAndSubmit() {
    setState(() {
      _emailError = null;
      _passwordError = null;
    });

    if (_emailController.text.isEmpty) {
      setState(() => _emailError = 'Email es requerido');
      return;
    }

    if (!_emailController.text.contains('@')) {
      setState(() => _emailError = 'Formato de email inválido');
      return;
    }

    if (_passwordController.text.isEmpty) {
      setState(() => _passwordError = 'Contraseña es requerida');
      return;
    }

    if (_passwordController.text.length < 6) {
      setState(() => _passwordError = 'La contraseña debe tener al menos 6 caracteres');
      return;
    }

    widget.onSubmit(_emailController.text, _passwordController.text);
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          EmailInput(
            controller: _emailController,
            errorText: _emailError,
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _passwordController,
            obscureText: true,
            decoration: InputDecoration(
              labelText: 'Contraseña',
              errorText: _passwordError,
            ),
          ),
          const SizedBox(height: 24),
          LoginButton(
            text: 'Iniciar Sesión',
            isLoading: widget.isLoading,
            onPressed: _validateAndSubmit,
          ),
        ],
      ),
    );
  }
}
```

### ✅ Paso 2: Crea los tests

```bash
touch test/features/auth/presentation/widgets/auth_form_test.dart
```

```dart
// test/features/auth/presentation/widgets/auth_form_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mi_proyecto_flutter/clean/features/auth/presentation/widgets/auth_form.dart';

void main() {
  group('AuthForm', () {
    
    testWidgets('debería mostrar todos los campos inicialmente', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthForm(onSubmit: (_, __) {}),
          ),
        ),
      );

      expect(find.text('Email'), findsOneWidget);
      expect(find.text('Contraseña'), findsOneWidget);
      expect(find.text('Iniciar Sesión'), findsOneWidget);
    });

    testWidgets('debería validar email vacío', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthForm(onSubmit: (_, __) {}),
          ),
        ),
      );

      // Intentar enviar sin completar campos
      await tester.tap(find.text('Iniciar Sesión'));
      await tester.pump();

      expect(find.text('Email es requerido'), findsOneWidget);
    });

    testWidgets('debería validar formato de email', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthForm(onSubmit: (_, __) {}),
          ),
        ),
      );

      // Ingresar email inválido
      await tester.enterText(
        find.widgetWithText(TextField, 'Email'), // O buscar por widget
        'email-invalido',
      );
      await tester.tap(find.text('Iniciar Sesión'));
      await tester.pump();

      expect(find.text('Formato de email inválido'), findsOneWidget);
    });

    testWidgets('debería validar contraseña vacía', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthForm(onSubmit: (_, __) {}),
          ),
        ),
      );

      // Ingresar email válido pero no contraseña
      await tester.enterText(
        find.byType(TextField).first,
        'test@example.com',
      );
      await tester.tap(find.text('Iniciar Sesión'));
      await tester.pump();

      expect(find.text('Contraseña es requerida'), findsOneWidget);
    });

    testWidgets('debería validar longitud mínima de contraseña', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthForm(onSubmit: (_, __) {}),
          ),
        ),
      );

      // Ingresar contraseña corta
      final textFields = find.byType(TextField);
      await tester.enterText(textFields.first, 'test@example.com');
      await tester.enterText(textFields.last, '123'); // Muy corta
      await tester.tap(find.text('Iniciar Sesión'));
      await tester.pump();

      expect(find.text('La contraseña debe tener al menos 6 caracteres'), findsOneWidget);
    });

    testWidgets('debería enviar formulario cuando es válido', (tester) async {
      String? submittedEmail;
      String? submittedPassword;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: AuthForm(
              onSubmit: (email, password) {
                submittedEmail = email;
                submittedPassword = password;
              },
            ),
          ),
        ),
      );

      // Llenar formulario correctamente
      final textFields = find.byType(TextField);
      await tester.enterText(textFields.first, 'test@example.com');
      await tester.enterText(textFields.last, 'password123');
      await tester.tap(find.text('Iniciar Sesión'));
      await tester.pump();

      // Verificar que se llamó con los valores correctos
      expect(submittedEmail, 'test@example.com');
      expect(submittedPassword, 'password123');
    });

    testWidgets('debería deshabilitar botón durante envío', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: AuthForm(
              onSubmit: (_, __) {},
              isLoading: true,
            ),
          ),
        ),
      );

      // Verificar que muestra indicador de carga
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });
  });
}
```

---

## 🧪 Ejecuta todos los tests

```bash
flutter test test/features/auth/presentation/widgets/
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +15: All tests passed!
```

---

## ✅ Checklist de Ejercicio Completado

- [ ] Ejercicio 1: Tests de renderizado (3 tests)
- [ ] Ejercicio 2: Tests de tap (3 tests)
- [ ] Ejercicio 3: Tests de entrada de texto (4 tests)
- [ ] Ejercicio 4: Tests de formulario (6 tests)
- [ ] **Total: 16+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:
- ✅ Testear widgets simples (botones, textos)
- ✅ Testear interacciones (tap, enterText)
- ✅ Testear formularios completos
- ✅ Testear validaciones
- ✅ Testear estados de carga

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 5: Testing Core](../05-core/05-core-testing.md)

**Práctica:** [05a-practica-core-services.md](../05-core/05a-practica-core-services.md)

> En esta práctica aprenderás a testear servicios core como NetworkInfo.
