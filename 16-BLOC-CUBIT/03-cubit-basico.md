# 3. Cubit — Nivel Básico con Pantalla Completa

> **Ver también**: `01-CLEAN-ARCHITECTURE/05c-presentation-ui-layer.md` — ejemplo complementario de UserCubit con CRUD completo (BlocProvider, BlocBuilder, context.read).
> `09-ESTRUCTURA-DATOS-OOP/06-oop-modelado-datos.md` — sealed class, Equatable y copyWith (prerrequisito).

## Contador con Cubit

### Estado

```dart
// lib/features/contador/presentation/cubit/contador_state.dart
import 'package:equatable/equatable.dart';

sealed class ContadorState extends Equatable {
  const ContadorState();

  @override
  List<Object?> get props => [];
}

final class ContadorInitial extends ContadorState {
  const ContadorInitial();
}

final class ContadorValor extends ContadorState {
  final int valor;
  final bool esMaximo;

  const ContadorValor({required this.valor, this.esMaximo = false});

  @override
  List<Object?> get props => [valor, esMaximo];
}

final class ContadorError extends ContadorState {
  final String mensaje;

  const ContadorError(this.mensaje);

  @override
  List<Object?> get props => [mensaje];
}
```

### Cubit

```dart
// lib/features/contador/presentation/cubit/contador_cubit.dart
import 'package:bloc/bloc.dart';
import 'contador_state.dart';

class ContadorCubit extends Cubit<ContadorState> {
  ContadorCubit() : super(const ContadorInitial());

  void incrementar() {
    final valorActual = switch (state) {
      ContadorValor(:final valor) => valor,
      _ => 0,
    };

    if (valorActual >= 100) {
      emit(ContadorValor(valor: valorActual, esMaximo: true));
      return;
    }

    emit(ContadorValor(valor: valorActual + 1));
  }

  void decrementar() {
    final valorActual = switch (state) {
      ContadorValor(:final valor) => valor,
      _ => 0,
    };

    if (valorActual <= 0) {
      emit(ContadorError('El valor no puede ser negativo'));
      return;
    }

    emit(ContadorValor(valor: valorActual - 1));
  }

  void reset() => emit(const ContadorInitial());
}
```

### Pantalla completa

```dart
// lib/features/contador/presentation/pages/contador_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../cubit/contador_cubit.dart';
import '../cubit/contador_state.dart';

class ContadorPage extends StatelessWidget {
  const ContadorPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => ContadorCubit(),
      child: const _ContadorView(),
    );
  }
}

class _ContadorView extends StatelessWidget {
  const _ContadorView();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Contador con Cubit'),
      ),
      body: Center(
        child: BlocBuilder<ContadorCubit, ContadorState>(
          builder: (context, state) {
            return switch (state) {
              ContadorInitial() => const Text(
                  'Presiona un botón para empezar',
                  style: TextStyle(fontSize: 18, color: Colors.grey),
                ),
              ContadorValor(:final valor, :final esMaximo) => Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      '$valor',
                      style: TextStyle(
                        fontSize: 72,
                        fontWeight: FontWeight.bold,
                        color: esMaximo ? Colors.orange : null,
                      ),
                    ),
                    if (esMaximo)
                      const Chip(
                        label: Text('¡Máximo alcanzado!'),
                        backgroundColor: Colors.orange,
                        labelStyle: TextStyle(color: Colors.white),
                      ),
                  ],
                ),
              ContadorError(:final mensaje) => Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.error, color: Colors.red, size: 48),
                    const SizedBox(height: 8),
                    Text(mensaje, style: const TextStyle(color: Colors.red)),
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: () => context.read<ContadorCubit>().reset(),
                      child: const Text('Reiniciar'),
                    ),
                  ],
                ),
            };
          },
        ),
      ),
      floatingActionButton: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          FloatingActionButton(
            heroTag: 'incrementar',
            onPressed: () => context.read<ContadorCubit>().incrementar(),
            child: const Icon(Icons.add),
          ),
          const SizedBox(height: 8),
          FloatingActionButton(
            heroTag: 'decrementar',
            onPressed: () => context.read<ContadorCubit>().decrementar(),
            child: const Icon(Icons.remove),
          ),
        ],
      ),
    );
  }
}
```

## Login con Cubit + Repositorio

### Estado

```dart
sealed class AuthState extends Equatable {
  const AuthState();

  @override
  List<Object?> get props => [];
}

final class AuthInitial extends AuthState {
  const AuthInitial();
}

final class AuthLoading extends AuthState {
  const AuthLoading();
}

final class AuthSuccess extends AuthState {
  final String token;

  const AuthSuccess(this.token);

  @override
  List<Object?> get props => [token];
}

final class AuthError extends AuthState {
  final String mensaje;

  const AuthError(this.mensaje);

  @override
  List<Object?> get props => [mensaje];
}
```

### Cubit con repo

```dart
class AuthCubit extends Cubit<AuthState> {
  final AuthRepository _repo;

  AuthCubit({required AuthRepository repo})
      : _repo = repo,
        super(const AuthInitial());

  Future<void> login(String email, String password) async {
    emit(const AuthLoading());

    final result = await _repo.login(email, password);

    result.fold(
      (error) => emit(AuthError(error.mensaje)),
      (token) => emit(AuthSuccess(token)),
    );
  }

  Future<void> logout() async {
    await _repo.logout();
    emit(const AuthInitial());
  }
}
```

### Pantalla login completa

```dart
class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => AuthCubit(repo: AuthRepositoryImpl()),
      child: const _LoginView(),
    );
  }
}

class _LoginView extends StatefulWidget {
  const _LoginView();

  @override
  State<_LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<_LoginView> {
  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocListener<AuthCubit, AuthState>(
      listener: (context, state) {
        switch (state) {
          case AuthSuccess():
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Inicio de sesión exitoso')),
            );
            context.go('/home');
          case AuthError(:final mensaje):
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(mensaje), backgroundColor: Colors.red),
            );
          default:
        }
      },
      child: Scaffold(
        appBar: AppBar(title: const Text('Iniciar Sesión')),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Icon(Icons.lock, size: 80, color: Colors.blue),
                const SizedBox(height: 32),
                TextFormField(
                  controller: _emailCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    prefixIcon: Icon(Icons.email),
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.emailAddress,
                  validator: (v) =>
                      v?.contains('@') == true ? null : 'Email inválido',
                ),
                const SizedBox(height: 16),
                TextFormField(
                  controller: _passwordCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Contraseña',
                    prefixIcon: Icon(Icons.lock),
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
                  validator: (v) =>
                      (v?.length ?? 0) >= 6 ? null : 'Mínimo 6 caracteres',
                ),
                const SizedBox(height: 24),
                BlocBuilder<AuthCubit, AuthState>(
                  builder: (context, state) {
                    return FilledButton(
                      onPressed: state is AuthLoading
                          ? null
                          : _onLogin,
                      child: state is AuthLoading
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            )
                          : const Text('Ingresar'),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _onLogin() {
    if (_formKey.currentState?.validate() != true) return;
    context.read<AuthCubit>().login(
          _emailCtrl.text.trim(),
          _passwordCtrl.text,
        );
  }
}
```

## Buenas prácticas con Cubit

- El estado inicial debe tener sentido (no `null`)
- Usa `sealed class` + pattern matching para manejar estados
- No emitas estados sucesivos iguales (BLoC las ignora por defecto)
- No llames `emit` fuera del Cubit
- Los side effects (SnackBar, navegación) van en `BlocListener`, no en el Cubit
