# 6. Widgets flutter_bloc — Parte 2 (Listener + Consumer + Selector)

> Referencia oficial: [Flutter Bloc Concepts](https://bloclibrary.dev/flutter-bloc-concepts/)

## BlocListener

Ejecuta side effects sin reconstruir la UI.

```dart
BlocListener<AuthCubit, AuthState>(
  listener: (context, state) {
    // Esto NO reconstruye el widget, solo ejecuta efectos
    switch (state) {
      case AuthAuthenticated():
        context.go('/home');
      case AuthError(:final mensaje):
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(mensaje), backgroundColor: Colors.red),
        );
      case _:
    }
  },
  child: const LoginForm(),
);
```

### listenWhen: control fino

```dart
BlocListener<AuthCubit, AuthState>(
  listenWhen: (anterior, actual) {
    // Solo escuchar cuando hay error o éxito autenticación
    return actual is AuthError || actual is AuthAuthenticated;
  },
  listener: (context, state) {
    // ...
  },
  child: const LoginForm(),
);
```

### Múltiples BlocListener

```dart
// Anidados para diferentes efectos
BlocListener<AuthCubit, AuthState>(
  listener: (context, state) {
    if (state is AuthError) _showSnackbar(context, state.mensaje);
  },
  child: BlocListener<PerfilCubit, PerfilState>(
    listener: (context, state) {
      if (state is PerfilLoaded) _trackEvent('perfil_cargado');
    },
    child: const _Formulario(),
  ),
);
```

## BlocConsumer

Combina BlocListener + BlocBuilder en un solo widget.

```dart
BlocConsumer<AuthCubit, AuthState>(
  listener: (context, state) {
    // Side effects
    if (state is AuthError) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.mensaje)),
      );
    }
    if (state is AuthAuthenticated) {
      context.go('/home');
    }
  },
  builder: (context, state) {
    // UI
    return switch (state) {
      AuthLoading() => const CircularProgressIndicator(),
      AuthInitial() => const LoginForm(),
      AuthAuthenticated() => const HomePage(),
      AuthError(:final mensaje) => Text('Error: $mensaje'),
    };
  },
);
```

### listener y builder con control

```dart
BlocConsumer<AuthCubit, AuthState>(
  listenWhen: (anterior, actual) =>
      actual is AuthError || actual is AuthAuthenticated,
  listener: (context, state) { /* ... */ },
  buildWhen: (anterior, actual) =>
      actual is AuthLoading || actual is AuthInitial,
  builder: (context, state) { /* ... */ },
);
```

Uso típico: login donde necesitas mostrar loading, errores y navegar al éxito.

## BlocSelector

Reconstruye solo cuando una parte específica del estado cambia.

```dart
// Solo se reconstruye si state.valor cambia, no por otros campos
BlocSelector<ContadorCubit, ContadorState, int>(
  selector: (state) => state.valor,
  builder: (context, valor) {
    return Text('$valor', style: const TextStyle(fontSize: 48));
  },
);
```

### Caso real: carrito de compras

```dart
class CarritoHeader extends StatelessWidget {
  const CarritoHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocSelector<CarritoBloc, CarritoState, int>(
      selector: (state) => state.items.fold<int>(
        0,
        (sum, item) => sum + item.cantidad,
      ),
      builder: (context, totalItems) {
        return Badge(
          isLabelVisible: totalItems > 0,
          label: Text('$totalItems'),
          child: const Icon(Icons.shopping_cart),
        );
      },
    );
  }
}
```

El `BlocSelector` solo reconstruye el `Badge` cuando `totalItems` cambia, no cuando cambia el precio de los items o el estado de carga.

### Caso real: formulario con validación en tiempo real

```dart
class EmailField extends StatelessWidget {
  const EmailField({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocSelector<RegistroCubit, RegistroState, String?>(
      selector: (state) => state.emailError,
      builder: (context, error) {
        return TextField(
          decoration: InputDecoration(
            labelText: 'Email',
            errorText: error,
            prefixIcon: const Icon(Icons.email),
          ),
          onChanged: (value) =>
              context.read<RegistroCubit>().emailCambiado(value),
        );
      },
    );
  }
}

class PasswordField extends StatelessWidget {
  const PasswordField({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocSelector<RegistroCubit, RegistroState, String?>(
      selector: (state) => state.passwordError,
      builder: (context, error) {
        return TextField(
          decoration: InputDecoration(
            labelText: 'Contraseña',
            errorText: error,
            prefixIcon: const Icon(Icons.lock),
          ),
          obscureText: true,
          onChanged: (value) =>
              context.read<RegistroCubit>().passwordCambiado(value),
        );
      },
    );
  }
}
```

Cada campo se reconstruye independientemente.

## Comparación de widgets

| Widget | Reconstruye | Side effects | Selector |
|---|---|---|---|
| BlocBuilder | Sí | No | buildWhen |
| BlocListener | No | Sí | listenWhen |
| BlocConsumer | Sí | Sí | Ambos |
| BlocSelector | Sí (parcial) | No | selector |

## Regla de oro

- **BlocProvider**: siempre al inicio, crea el Cubit
- **BlocBuilder**: para partes de UI que cambian con el estado
- **BlocListener**: para SnackBars, navegación, diálogos
- **BlocConsumer**: cuando necesitas ambos en el mismo nivel
- **BlocSelector**: cuando solo necesitas una fracción del estado
- **context.read**: en callbacks (onPressed, initState)
- **context.watch**: en build (pero prefiero BlocBuilder/Selector)

---

## 📚 Referencias

- [bloc | Documentación oficial](https://bloclibrary.dev/) — Guías, tutoriales y API reference
- [flutter_bloc | pub.dev](https://pub.dev/packages/flutter_bloc) — Paquete Flutter de BLoC
- [Bloc Concurrency](https://pub.dev/packages/bloc_concurrency) — Event transformers y concurrencia

---
