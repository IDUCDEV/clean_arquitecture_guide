# 4. Interacción y Formularios

## GestureDetector e InkWell

Captura de gestos táctiles.

```dart
GestureDetector(
  onTap: () => print('Tap'),
  onDoubleTap: () => print('Doble tap'),
  onLongPress: () => print('Presión larga'),
  onHorizontalDragEnd: (_) => print('Swipe'),
  child: const Text('Tocable'),
);
```

`InkWell` agrega feedback visual Material (splash):

```dart
InkWell(
  onTap: () {},
  child: Container(
    padding: const EdgeInsets.all(16),
    child: const Text('Con efecto splash'),
  ),
);
```

## TextField y TextFormField

Entrada de texto libre.

```dart
TextField(
  controller: _controller,
  decoration: InputDecoration(
    labelText: 'Nombre',
    hintText: 'Ingresa tu nombre',
    prefixIcon: const Icon(Icons.person),
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(8),
    ),
    suffixIcon: _controller.text.isNotEmpty
        ? IconButton(
            icon: const Icon(Icons.clear),
            onPressed: () => _controller.clear(),
          )
        : null,
  ),
  keyboardType: TextInputType.text,
  textInputAction: TextInputAction.next,
  obscureText: _oculto,
  onChanged: (value) => setState(() {}),
);
```

Controladores deben ser dispuestos:

```dart
class _FormState extends State<FormWidget> {
  final _nombreCtrl = TextEditingController();
  final _emailCtrl = TextEditingController();

  @override
  void dispose() {
    _nombreCtrl.dispose();
    _emailCtrl.dispose();
    super.dispose();
  }
}
```

## Form con validación

```dart
final _formKey = GlobalKey<FormState>();

Form(
  key: _formKey,
  child: Column(
    children: [
      TextFormField(
        decoration: const InputDecoration(labelText: 'Email'),
        validator: (value) {
          if (value == null || value.isEmpty) return 'Campo requerido';
          if (!value.contains('@')) return 'Email inválido';
          return null;
        },
      ),
      const SizedBox(height: 16),
      FilledButton(
        onPressed: () {
          if (_formKey.currentState!.validate()) {
            // Procesar formulario
          }
        },
        child: const Text('Enviar'),
      ),
    ],
  ),
);
```

## DropdownButtonFormField

Selección de una opción entre varias.

```dart
String? _rol;

DropdownButtonFormField<String>(
  value: _rol,
  decoration: const InputDecoration(labelText: 'Rol'),
  items: const [
    DropdownMenuItem(value: 'admin', child: Text('Admin')),
    DropdownMenuItem(value: 'user', child: Text('Usuario')),
    DropdownMenuItem(value: 'guest', child: Text('Invitado')),
  ],
  onChanged: (value) => setState(() => _rol = value),
);
```

## Checkbox, Switch, Radio

Controles binarios y de selección única.

```dart
// Checkbox
Checkbox(
  value: _aceptaTerminos,
  onChanged: (value) => setState(() => _aceptaTerminos = value!),
);

// Switch
Switch(
  value: _notificaciones,
  onChanged: (value) => setState(() => _notificaciones = value),
);

// Radio
Radio<String>(
  value: 'masculino',
  groupValue: _genero,
  onChanged: (value) => setState(() => _genero = value!),
);
```

## DatePicker y TimePicker

```dart
Future<void> _seleccionarFecha() async {
  final fecha = await showDatePicker(
    context: context,
    initialDate: DateTime.now(),
    firstDate: DateTime(2020),
    lastDate: DateTime(2030),
  );
  if (fecha != null) {
    setState(() => _fecha = fecha);
  }
}

Future<void> _seleccionarHora() async {
  final hora = await showTimePicker(
    context: context,
    initialTime: TimeOfDay.now(),
  );
  if (hora != null) {
    setState(() => _hora = hora);
  }
}
```

## Slider y RangeSlider

```dart
// Slider simple
Slider(
  value: _volumen,
  min: 0,
  max: 100,
  divisions: 10,
  label: '${_volumen.round()}',
  onChanged: (value) => setState(() => _volumen = value),
);

// RangeSlider para rangos
RangeSlider(
  values: _rango,
  min: 0,
  max: 1000,
  divisions: 10,
  labels: TextRange(
    start: '${_rango.start.round()}',
    end: '${_rango.end.round()}',
  ),
  onChanged: (values) => setState(() => _rango = values),
);
```

## Patrón de formulario completo con BLoC

```dart
class LoginForm extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();

  LoginForm({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocListener<AuthCubit, AuthState>(
      listener: (context, state) {
        if (state is AuthError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message)),
          );
        }
        if (state is AuthAuthenticated) {
          context.go('/home');
        }
      },
      child: Form(
        key: _formKey,
        child: Column(
          children: [
            TextFormField(
              controller: _emailCtrl,
              decoration: const InputDecoration(labelText: 'Email'),
              validator: (v) => v?.contains('@') == true ? null : 'Email inválido',
            ),
            TextFormField(
              controller: _passCtrl,
              decoration: const InputDecoration(labelText: 'Contraseña'),
              obscureText: true,
              validator: (v) => (v?.length ?? 0) >= 6 ? null : 'Mínimo 6 caracteres',
            ),
            BlocBuilder<AuthCubit, AuthState>(
              builder: (context, state) {
                return FilledButton(
                  onPressed: state is AuthLoading
                      ? null
                      : () {
                          if (_formKey.currentState!.validate()) {
                            context.read<AuthCubit>().login(
                                  _emailCtrl.text,
                                  _passCtrl.text,
                                );
                          }
                        },
                  child: state is AuthLoading
                      ? const SizedBox(
                          width: 20, height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Iniciar sesión'),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
```


---

## 📚 Referencias

- [Flutter | Widget catalog](https://docs.flutter.dev/ui/widgets) — Catálogo completo de widgets por categoría
- [Flutter | API reference](https://api.flutter.dev/) — Documentación de la API de Flutter
- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter

---

## Lo que sigue

El siguiente capítulo cubre listas y scroll: cómo mostrar colecciones de datos eficientemente.
