---
name: widget-page-scaffold
description: Generate Flutter pages with Cubit integration using BlocListener + BlocBuilder, if(state is...) pattern, SnackbarHelper, AppButton, and CircularProgressIndicator. Only generates structure — never implementation bodies.
---

# widget-page-scaffold — Scaffold de páginas Flutter con Cubit

Genera páginas Flutter conectadas a un Cubit, siguiendo el patrón real del proyecto:
`BlocListener` para side effects, `BlocBuilder` con `if (state is ...)` para renderizado.

## Input requerido

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `feature_name` | Nombre de la feature | `profile`, `order`, `auth` |
| `page_name` | Nombre de la página | `list`, `detail`, `edit` |
| `pattern_type` | Patrón de integración | `listener_builder`, `builder`, `form` |

## Patrones disponibles

| Pattern | Cuándo usarlo |
|---|---|
| `listener_builder` | **Default**. Cualquier página con side effects (snackbars, navegación post-acción). Usa `BlocListener` + `BlocBuilder`. |
| `builder` | Página de solo lectura sin efectos secundarios. Usa solo `BlocBuilder`. |
| `form` | Formulario con validación, controllers, submit loading. Usa `BlocListener` + `BlocBuilder`. |

## Output

```
lib/features/{feature}/presentation/pages/{feature}_{page_name}_page.dart
```

## Templates

### Pattern: listener_builder — BlocListener + BlocBuilder (default)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{app_name}/core/services/snackbar_helper.dart';
import 'package:{app_name}/core/widgets/app_button.dart';
import 'package:{app_name}/features/{feature}/presentation/cubit/{feature}_cubit.dart';

class {Feature}{PageName}Page extends StatefulWidget {
  const {Feature}{PageName}Page({super.key});

  @override
  State<{Feature}{PageName}Page> createState() => _{Feature}{PageName}PageState();
}

class _{Feature}{PageName}PageState extends State<{Feature}{PageName}Page> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<{Feature}Cubit>().load{Feature}s();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('{PageTitle}')),
      body: BlocListener<{Feature}Cubit, {Feature}State>(
        listener: (context, state) {
          // TODO: handle side effects
          // if (state is {Feature}Loaded && state.xxxError != null) {
          //   SnackbarHelper.show(context, state.xxxError!, isSuccess: false);
          //   context.read<{Feature}Cubit>().clearXxxError();
          // }
          // if (state is {Feature}{Action}Success) {
          //   SnackbarHelper.show(context, 'Operación exitosa', isSuccess: true);
          //   context.pop();
          // }
        },
        child: BlocBuilder<{Feature}Cubit, {Feature}State>(
          builder: (context, state) {
            if (state is {Feature}Loading) {
              return const Center(child: CircularProgressIndicator());
            }
            if (state is {Feature}Error) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(state.message, overflow: TextOverflow.ellipsis),
                    const SizedBox(height: 16),
                    AppButton(
                      label: 'Reintentar',
                      onPressed: () => context.read<{Feature}Cubit>().load{Feature}s(),
                      variant: AppButtonVariant.primary,
                    ),
                  ],
                ),
              );
            }
            if (state is {Feature}Loaded) {
              // TODO: render content
              return const Center(child: Text('Implement {Feature}{PageName} content'));
            }
            return const Center(child: CircularProgressIndicator());
          },
        ),
      ),
    );
  }

  void _refresh() {
    context.read<{Feature}Cubit>().load{Feature}s();
  }
}
```

### Pattern: builder — BlocBuilder (solo lectura)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{app_name}/features/{feature}/presentation/cubit/{feature}_cubit.dart';

class {Feature}{PageName}Page extends StatelessWidget {
  const {Feature}{PageName}Page({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('{PageTitle}')),
      body: BlocBuilder<{Feature}Cubit, {Feature}State>(
        builder: (context, state) {
          if (state is {Feature}Loading) {
            return const Center(child: CircularProgressIndicator());
          }
          if (state is {Feature}Loaded) {
            // TODO: render content
            return const Center(child: Text('Implement {Feature}{PageName} content'));
          }
          if (state is {Feature}Error) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(state.message, overflow: TextOverflow.ellipsis),
                  const SizedBox(height: 16),
                  AppButton(
                    label: 'Reintentar',
                    onPressed: () => context.read<{Feature}Cubit>().load{Feature}s(),
                    variant: AppButtonVariant.primary,
                  ),
                ],
              ),
            );
          }
          return const Center(child: CircularProgressIndicator());
        },
      ),
    );
  }
}
```

### Pattern: form — Formulario con validación

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:{app_name}/core/services/snackbar_helper.dart';
import 'package:{app_name}/core/widgets/app_button.dart';
import 'package:{app_name}/features/{feature}/presentation/cubit/{feature}_cubit.dart';

class {Feature}{PageName}Page extends StatefulWidget {
  const {Feature}{PageName}Page({super.key});

  @override
  State<{Feature}{PageName}Page> createState() => _{Feature}{PageName}PageState();
}

class _{Feature}{PageName}PageState extends State<{Feature}{PageName}Page> {
  final _formKey = GlobalKey<FormState>();

  // TODO: declare TextEditingController for each field
  // late final TextEditingController _nameController;

  @override
  void initState() {
    super.initState();
    // TODO: initialize controllers
    // _nameController = TextEditingController(text: initialValue);
  }

  @override
  void dispose() {
    // TODO: dispose controllers
    // _nameController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('{PageTitle}')),
      body: BlocListener<{Feature}Cubit, {Feature}State>(
        listener: (context, state) {
          // TODO: handle success / error side effects
          // if (state is {Feature}{Action}Success) {
          //   SnackbarHelper.show(context, 'Guardado exitoso', isSuccess: true);
          //   context.pop();
          // }
          // if (state is {Feature}Error) {
          //   SnackbarHelper.show(context, state.message, isSuccess: false);
          // }
        },
        child: BlocBuilder<{Feature}Cubit, {Feature}State>(
          builder: (context, state) {
            final isLoading = state is {Feature}Loading;

            return SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // TODO: TextFormField for each field
                    // TextFormField(
                    //   controller: _nameController,
                    //   decoration: const InputDecoration(labelText: 'Name'),
                    //   validator: (v) => v?.isEmpty == true ? 'Required' : null,
                    // ),
                    const SizedBox(height: 24),
                    AppButton(
                      label: 'Guardar',
                      onPressed: isLoading ? null : _submit,
                      variant: AppButtonVariant.primary,
                      isLoading: isLoading,
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }

  void _submit() {
    // TODO: implement submit
    // if (_formKey.currentState!.validate()) {
    //   context.read<{Feature}Cubit>().create{Feature}(
    //     {Feature}(
    //       name: _nameController.text,
    //       // ... more fields
    //     ),
    //   );
    // }
  }
}
```

## Workflow

1. Preguntar al usuario: feature_name, page_name, pattern_type
2. Verificar que existe `lib/features/{feature}/` y su cubit
3. Generar la página con el template correspondiente
4. Todos los handlers y bodies con `// TODO: implement`
5. Mostrar la ruta del archivo creado y recordar conectar en el router
