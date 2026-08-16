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

Extras útiles: `autofillHints: [AutofillHints.email]` para autocompletado nativo, `onTapOutside` para ocultar teclado, y `enabled: false` para deshabilitar sin perder el valor.

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

`_formKey.currentState!.validate()` valida todos los campos y `save()` guarda los valores en los `TextFormField` (si definiste `onSaved`).

## DropdownButtonFormField

Selección de una opción entre varias. Desde Flutter 3.35 usa `initialValue` en lugar de `value`.

```dart
String? _rol;

DropdownButtonFormField<String>(
  initialValue: _rol,
  decoration: const InputDecoration(labelText: 'Rol'),
  items: const [
    DropdownMenuItem(value: 'admin', child: Text('Admin')),
    DropdownMenuItem(value: 'user', child: Text('Usuario')),
    DropdownMenuItem(value: 'guest', child: Text('Invitado')),
  ],
  onChanged: (value) => setState(() => _rol = value),
);
```

## DropdownMenu (M3)

Alternativa moderna a `DropdownButton` con campo de búsqueda y estilo M3.

```dart
DropdownMenu<String>(
  label: const Text('Rol'),
  initialSelection: _rol,
  onSelected: (value) => setState(() => _rol = value),
  dropdownMenuEntries: const [
    DropdownMenuEntry(value: 'admin', label: 'Admin'),
    DropdownMenuEntry(value: 'user', label: 'Usuario'),
    DropdownMenuEntry(value: 'guest', label: 'Invitado'),
  ],
);
```

## Checkbox, Switch, Radio (RadioGroup)

Controles binarios y de selección única.

```dart
// Checkbox
Checkbox(
  value: _aceptaTerminos,
  onChanged: (value) => setState(() => _aceptaTerminos = value!),
);

// Switch — desde 3.35: activeThumbColor (activeColor está deprecado)
Switch(
  value: _notificaciones,
  activeThumbColor: Colors.green,
  onChanged: (value) => setState(() => _notificaciones = value),
);

// Radio — desde 3.32/3.35 el grupo se gestiona con RadioGroup
RadioGroup<String>(
  groupValue: _genero,
  onChanged: (value) => setState(() => _genero = value),
  child: const Column(
    children: [
      Radio(value: 'masculino'),
      Radio(value: 'femenino'),
      Radio(value: 'otro'),
    ],
  ),
);
```

> En `Radio` los parámetros `groupValue` y `onChanged` están deprecados desde 3.32: el estado del grupo lo maneja `RadioGroup`. Cada `Radio` solo declara su `value`.

## SegmentedButton

Selección exclusiva estilizada (M3), ideal para filtros con pocas opciones.

```dart
SegmentedButton<String>(
  segments: const [
    ButtonSegment(value: 'dia', label: Text('Día'), icon: Icon(Icons.wb_sunny)),
    ButtonSegment(value: 'mes', label: Text('Mes')),
    ButtonSegment(value: 'anio', label: Text('Año')),
  ],
  selected: {_periodo},
  onSelectionChanged: (selection) =>
      setState(() => _periodo = selection.first),
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

## Patrón de formulario con estado local (widgets puros)

Con `ValueNotifier` + `ValueListenableBuilder` puedes construir un formulario reactivo sin librerías externas. El botón se habilita/deshabilita según el estado.

```dart
class LoginForm extends StatefulWidget {
  const LoginForm({super.key});
  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailCtrl = TextEditingController();
  final _passCtrl = TextEditingController();
  final _enviando = ValueNotifier<bool>(false);

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passCtrl.dispose();
    _enviando.dispose();
    super.dispose();
  }

  Future<void> _iniciarSesion() async {
    if (!(_formKey.currentState?.validate() ?? false)) return;
    _enviando.value = true;
    try {
      await autenticar(_emailCtrl.text, _passCtrl.text); // tu lógica
      if (mounted) context.go('/home');
    } finally {
      if (mounted) _enviando.value = false;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: _emailCtrl,
            decoration: const InputDecoration(labelText: 'Email'),
            validator: (v) =>
                v?.contains('@') == true ? null : 'Email inválido',
          ),
          TextFormField(
            controller: _passCtrl,
            decoration: const InputDecoration(labelText: 'Contraseña'),
            obscureText: true,
            validator: (v) =>
                (v?.length ?? 0) >= 6 ? null : 'Mínimo 6 caracteres',
          ),
          ValueListenableBuilder<bool>(
            valueListenable: _enviando,
            builder: (context, enviando, child) {
              return FilledButton(
                onPressed: enviando ? null : _iniciarSesion,
                child: enviando
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
    );
  }
}
```

> En el [módulo 16](../16-BLOC-CUBIT/) este mismo formulario se versiona con `BlocProvider` + `BlocListener` + `BlocBuilder`; aquí lo mantenemos en widgets puros porque el tema de esta guía es el catálogo de widgets. La estructura del árbol (`Form` → campos → botón) es idéntica en ambos casos.


---

## 📚 Referencias

- [Flutter | TextFields](https://docs.flutter.dev/ui/widgets/text) — Catálogo de campos de texto
- [Flutter | Material 3 — Selection controls](https://m3.material.io/components/selection-controls/overview) — Checkbox, Switch, Radio en M3
- [Flutter | API — RadioGroup](https://api.flutter.dev/flutter/widgets/RadioGroup-class.html) — Grupo de radios con navegación por teclado
- [Flutter | API — SegmentedButton](https://api.flutter.dev/flutter/material/SegmentedButton-class.html) — Botón segmentado M3
- [Flutter | Forms](https://docs.flutter.dev/ui/widgets/forms) — Guía de formularios

---

## Lo que sigue

El siguiente capítulo cubre listas y scroll: cómo mostrar colecciones de datos eficientemente.
