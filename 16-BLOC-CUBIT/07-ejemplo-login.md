# 7. Ejemplo: Login Completo con Bloc

## Funcionalidad

- Formulario con validación en tiempo real
- Loading state mientras hace petición
- SnackBar en error
- Navegación al éxito
- Persistencia de sesión

## Estados

```dart
// presentation/cubit/login_state.dart
sealed class LoginState extends Equatable {
  const LoginState();

  @override
  List<Object?> get props => [];
}

final class LoginInitial extends LoginState {
  const LoginInitial();
}

final class LoginLoading extends LoginState {
  const LoginLoading();
}

final class LoginValidationError extends LoginState {
  final String? emailError;
  final String? passwordError;

  const LoginValidationError({this.emailError, this.passwordError});

  @override
  List<Object?> get props => [emailError, passwordError];
}

final class LoginSuccess extends LoginState {
  final User user;

  const LoginSuccess(this.user);

  @override
  List<Object?> get props => [user];
}

final class LoginError extends LoginState {
  final String mensaje;

  const LoginError(this.mensaje);

  @override
  List<Object?> get props => [mensaje];
}
```

## Cubit con validación

```dart
// presentation/cubit/login_cubit.dart
class LoginCubit extends Cubit<LoginState> {
  final AuthRepository _repo;

  LoginCubit({required AuthRepository repo})
      : _repo = repo,
        super(const LoginInitial());

  void emailCambiado(String email) {
    if (state is! LoginValidationError) return;

    final errors = <String?, String?>{};
    if (email.isNotEmpty && !email.contains('@')) {
      errors['emailError'] = 'Email inválido';
    }

    emit(LoginValidationError(
      emailError: errors['emailError'],
      passwordError: (state as LoginValidationError).passwordError,
    ));
  }

  void passwordCambiado(String password) {
    if (state is! LoginValidationError) return;

    emit(LoginValidationError(
      emailError: (state as LoginValidationError).emailError,
      passwordError: password.isNotEmpty && password.length < 6
          ? 'Mínimo 6 caracteres'
          : null,
    ));
  }

  void validate(String email, String password) {
    final emailError =
        email.isEmpty ? 'Campo requerido' : (!email.contains('@') ? 'Email inválido' : null);
    final passwordError =
        password.isEmpty ? 'Campo requerido' : (password.length < 6 ? 'Mínimo 6 caracteres' : null);

    if (emailError != null || passwordError != null) {
      emit(LoginValidationError(
        emailError: emailError,
        passwordError: passwordError,
      ));
      return;
    }

    _login(email, password);
  }

  Future<void> _login(String email, String password) async {
    emit(const LoginLoading());

    final result = await _repo.login(email, password);

    result.fold(
      (failure) => emit(LoginError(failure.mensaje)),
      (user) => emit(LoginSuccess(user)),
    );
  }

  void reset() => emit(const LoginInitial());
}
```

## Pantalla completa

```dart
// presentation/pages/login_page.dart
class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => LoginCubit(repo: getIt()),
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

  void _onSubmit() {
    context.read<LoginCubit>().validate(
          _emailCtrl.text.trim(),
          _passwordCtrl.text,
        );
  }

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<LoginCubit, LoginState>(
      listenWhen: (prev, current) =>
          current is LoginSuccess || current is LoginError,
      listener: (context, state) {
        switch (state) {
          case LoginSuccess():
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Bienvenido')),
            );
            context.go('/home');
          case LoginError(:final mensaje):
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(mensaje),
                backgroundColor: Colors.red.shade700,
              ),
            );
          default:
        }
      },
      builder: (context, state) {
        return Scaffold(
          appBar: AppBar(title: const Text('Iniciar Sesión')),
          body: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: Form(
                key: _formKey,
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    const Icon(Icons.shopping_bag,
                        size: 80, color: Colors.blue),
                    const SizedBox(height: 8),
                    const Text(
                      'Mi Tienda',
                      textAlign: TextAlign.center,
                      style:
                          TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 48),
                    BlocSelector<LoginCubit, LoginState, String?>(
                      selector: (s) =>
                          s is LoginValidationError ? s.emailError : null,
                      builder: (context, error) {
                        return TextFormField(
                          controller: _emailCtrl,
                          decoration: InputDecoration(
                            labelText: 'Correo electrónico',
                            prefixIcon: const Icon(Icons.email),
                            border: const OutlineInputBorder(),
                            errorText: error,
                          ),
                          keyboardType: TextInputType.emailAddress,
                          textInputAction: TextInputAction.next,
                          onChanged: (v) => context
                              .read<LoginCubit>()
                              .emailCambiado(v),
                        );
                      },
                    ),
                    const SizedBox(height: 16),
                    BlocSelector<LoginCubit, LoginState, String?>(
                      selector: (s) =>
                          s is LoginValidationError ? s.passwordError : null,
                      builder: (context, error) {
                        return TextFormField(
                          controller: _passwordCtrl,
                          decoration: InputDecoration(
                            labelText: 'Contraseña',
                            prefixIcon: const Icon(Icons.lock),
                            border: const OutlineInputBorder(),
                            errorText: error,
                          ),
                          obscureText: true,
                          textInputAction: TextInputAction.done,
                          onFieldSubmitted: (_) => _onSubmit(),
                          onChanged: (v) => context
                              .read<LoginCubit>()
                              .passwordCambiado(v),
                        );
                      },
                    ),
                    const SizedBox(height: 24),
                    Builder(builder: (context) {
                      final isLoading = context.watch<LoginCubit>().state is LoginLoading;
                      return FilledButton(
                        onPressed: isLoading ? null : _onSubmit,
                        style: FilledButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                        ),
                        child: isLoading
                            ? const SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  color: Colors.white,
                                ),
                              )
                            : const Text('Ingresar',
                                style: TextStyle(fontSize: 16)),
                      );
                    }),
                    const SizedBox(height: 16),
                    TextButton(
                      onPressed: () => context.push('/registro'),
                      child: const Text('¿No tienes cuenta? Regístrate'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
```

## Probar el Cubit

```dart
void main() {
  late LoginCubit cubit;
  late MockAuthRepo repo;

  setUp(() {
    repo = MockAuthRepo();
    cubit = LoginCubit(repo: repo);
  });

  tearDown(() => cubit.close());

  blocTest<LoginCubit, LoginState>(
    'emite ValidationError cuando email es inválido',
    build: () => cubit,
    act: (cubit) => cubit.validate('invalido', '123456'),
    expect: () => [
      const LoginValidationError(
        emailError: 'Email inválido',
        passwordError: null,
      ),
    ],
  );

  blocTest<LoginCubit, LoginState>(
    'emite [Loading, Success] cuando login es exitoso',
    build: () {
      when(() => repo.login('a@b.com', '123456'))
          .thenAnswer((_) async => Right(User(id: '1', email: 'a@b.com')));
      return cubit;
    },
    act: (cubit) => cubit.validate('a@b.com', '123456'),
    expect: () => [
      const LoginLoading(),
      LoginSuccess(User(id: '1', email: 'a@b.com')),
    ],
  );
}
```

---

## 📚 Referencias

- [bloc | Documentación oficial](https://bloclibrary.dev/) — Guías, tutoriales y API reference
- [flutter_bloc | pub.dev](https://pub.dev/packages/flutter_bloc) — Paquete Flutter de BLoC
- [Bloc Concurrency](https://pub.dev/packages/bloc_concurrency) — Event transformers y concurrencia

---
