# 11. Ejemplo: Formulario Multipaso con Bloc

## Funcionalidad

- Wizard de registro en 3 pasos
- Estado compartido entre pasos
- Validación por paso
- Botón Siguiente/Anterior/Enviar
- Resumen final antes de enviar

## Estado compartido

```dart
// presentation/cubit/registro_state.dart
class RegistroState extends Equatable {
  final int pasoActual;
  final String nombre;
  final String email;
  final String password;
  final String? nombreError;
  final String? emailError;
  final String? passwordError;
  final bool enviando;
  final bool completado;

  const RegistroState({
    this.pasoActual = 0,
    this.nombre = '',
    this.email = '',
    this.password = '',
    this.nombreError,
    this.emailError,
    this.passwordError,
    this.enviando = false,
    this.completado = false,
  });

  bool get puedeSiguiente => switch (pasoActual) {
        0 => nombre.isNotEmpty && nombreError == null,
        1 => email.isNotEmpty && emailError == null,
        2 => password.isNotEmpty && passwordError == null,
        _ => false,
      };

  int get totalPasos => 3;

  RegistroState copyWith({
    int? pasoActual,
    String? nombre,
    String? email,
    String? password,
    String? Function()? nombreError,
    String? Function()? emailError,
    String? Function()? passwordError,
    bool? enviando,
    bool? completado,
  }) {
    return RegistroState(
      pasoActual: pasoActual ?? this.pasoActual,
      nombre: nombre ?? this.nombre,
      email: email ?? this.email,
      password: password ?? this.password,
      nombreError: nombreError != null ? nombreError() : this.nombreError,
      emailError: emailError != null ? emailError() : this.emailError,
      passwordError:
          passwordError != null ? passwordError() : this.passwordError,
      enviando: enviando ?? this.enviando,
      completado: completado ?? this.completado,
    );
  }

  @override
  List<Object?> get props => [
        pasoActual,
        nombre,
        email,
        password,
        nombreError,
        emailError,
        passwordError,
        enviando,
        completado,
      ];
}
```

## Cubit con navegación de pasos

```dart
// presentation/cubit/registro_cubit.dart
class RegistroCubit extends Cubit<RegistroState> {
  final AuthRepository _repo;

  RegistroCubit({required AuthRepository repo})
      : _repo = repo,
        super(const RegistroState());

  void nombreCambiado(String v) {
    emit(state.copyWith(
      nombre: v,
      nombreError: () =>
          v.isEmpty ? 'Requerido' : (v.length < 3 ? 'Mínimo 3 caracteres' : null),
    ));
  }

  void emailCambiado(String v) {
    emit(state.copyWith(
      email: v,
      emailError: () =>
          v.isEmpty ? 'Requerido' : (!v.contains('@') ? 'Email inválido' : null),
    ));
  }

  void passwordCambiado(String v) {
    emit(state.copyWith(
      password: v,
      passwordError: () => v.isEmpty
          ? 'Requerido'
          : (v.length < 6 ? 'Mínimo 6 caracteres' : null),
    ));
  }

  void siguiente() {
    if (!state.puedeSiguiente || state.pasoActual >= state.totalPasos - 1) {
      return;
    }
    emit(state.copyWith(pasoActual: state.pasoActual + 1));
  }

  void anterior() {
    if (state.pasoActual <= 0) return;
    emit(state.copyWith(pasoActual: state.pasoActual - 1));
  }

  Future<void> enviar() async {
    emit(state.copyWith(enviando: true));

    final result = await _repo.registrar(
      nombre: state.nombre,
      email: state.email,
      password: state.password,
    );

    result.fold(
      (error) => emit(state.copyWith(
        enviando: false,
        passwordError: () => error.mensaje,
      )),
      (_) => emit(state.copyWith(enviando: false, completado: true)),
    );
  }

  void reset() => emit(const RegistroState());
}
```

## Pantalla del wizard

```dart
class RegistroPage extends StatelessWidget {
  const RegistroPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => RegistroCubit(repo: getIt()),
      child: const _RegistroStepper(),
    );
  }
}

class _RegistroStepper extends StatelessWidget {
  const _RegistroStepper();

  @override
  Widget build(BuildContext context) {
    return BlocConsumer<RegistroCubit, RegistroState>(
      listenWhen: (prev, current) =>
          current.completado || (!prev.enviando && current.enviando == false && current.passwordError != null),
      listener: (context, state) {
        if (state.completado) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Registro exitoso'),
              backgroundColor: Colors.green,
            ),
          );
          context.go('/home');
        }
      },
      builder: (context, state) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Crear cuenta'),
            leading: state.pasoActual > 0
                ? IconButton(
                    icon: const Icon(Icons.arrow_back),
                    onPressed: () =>
                        context.read<RegistroCubit>().anterior(),
                  )
                : null,
          ),
          body: Column(
            children: [
              // Indicador de pasos
              _StepIndicator(
                pasoActual: state.pasoActual,
                total: state.totalPasos,
              ),
              // Contenido del paso
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: _buildPaso(state, context),
                ),
              ),
              // Botones
              _buildBotones(state, context),
            ],
          ),
        );
      },
    );
  }

  Widget _buildPaso(RegistroState state, BuildContext context) {
    return switch (state.pasoActual) {
      0 => _buildNombreStep(state, context),
      1 => _buildEmailStep(state, context),
      2 => _buildPasswordStep(state, context),
      _ => const SizedBox.shrink(),
    };
  }

  Widget _buildNombreStep(RegistroState state, BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Paso 1: Datos personales',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        const Text('¿Cómo te llamas?', style: TextStyle(color: Colors.grey)),
        const SizedBox(height: 24),
        TextField(
          decoration: InputDecoration(
            labelText: 'Nombre completo',
            prefixIcon: const Icon(Icons.person),
            border: const OutlineInputBorder(),
            errorText: state.nombreError,
          ),
          onChanged: (v) => context.read<RegistroCubit>().nombreCambiado(v),
        ),
      ],
    );
  }

  Widget _buildEmailStep(RegistroState state, BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Paso 2: Correo electrónico',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        const Text('¿Cuál es tu email?', style: TextStyle(color: Colors.grey)),
        const SizedBox(height: 24),
        TextField(
          decoration: InputDecoration(
            labelText: 'Email',
            prefixIcon: const Icon(Icons.email),
            border: const OutlineInputBorder(),
            errorText: state.emailError,
          ),
          keyboardType: TextInputType.emailAddress,
          onChanged: (v) => context.read<RegistroCubit>().emailCambiado(v),
        ),
      ],
    );
  }

  Widget _buildPasswordStep(RegistroState state, BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Paso 3: Contraseña',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        const Text('Crea una contraseña segura',
            style: TextStyle(color: Colors.grey)),
        const SizedBox(height: 24),
        TextField(
          decoration: InputDecoration(
            labelText: 'Contraseña',
            prefixIcon: const Icon(Icons.lock),
            border: const OutlineInputBorder(),
            errorText: state.passwordError,
          ),
          obscureText: true,
          onChanged: (v) =>
              context.read<RegistroCubit>().passwordCambiado(v),
        ),
        const SizedBox(height: 16),
        // Resumen de requisitos
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _Requisito(
              texto: 'Mínimo 6 caracteres',
              cumplido: state.password.length >= 6,
            ),
            _Requisito(
              texto: 'No vacío',
              cumplido: state.password.isNotEmpty,
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildBotones(RegistroState state, BuildContext context) {
    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Row(
          children: [
            if (state.pasoActual > 0)
              Expanded(
                child: OutlinedButton(
                  onPressed: () =>
                      context.read<RegistroCubit>().anterior(),
                  child: const Text('Anterior'),
                ),
              ),
            if (state.pasoActual > 0) const SizedBox(width: 12),
            Expanded(
              child: FilledButton(
                onPressed: state.puedeSiguiente
                    ? () {
                        if (state.pasoActual == state.totalPasos - 1) {
                          context.read<RegistroCubit>().enviar();
                        } else {
                          context.read<RegistroCubit>().siguiente();
                        }
                      }
                    : null,
                child: state.enviando
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white),
                      )
                    : Text(state.pasoActual == state.totalPasos - 1
                        ? 'Crear cuenta'
                        : 'Siguiente'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _StepIndicator extends StatelessWidget {
  final int pasoActual;
  final int total;

  const _StepIndicator({required this.pasoActual, required this.total});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
      child: Row(
        children: List.generate(total, (i) {
          final isActive = i <= pasoActual;
          return Expanded(
            child: Container(
              height: 4,
              margin: const EdgeInsets.symmetric(horizontal: 2),
              decoration: BoxDecoration(
                color: isActive
                    ? Theme.of(context).colorScheme.primary
                    : Colors.grey[300],
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          );
        }),
      ),
    );
  }
}

class _Requisito extends StatelessWidget {
  final String texto;
  final bool cumplido;

  const _Requisito({required this.texto, required this.cumplido});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(
          cumplido ? Icons.check_circle : Icons.radio_button_unchecked,
          size: 16,
          color: cumplido ? Colors.green : Colors.grey,
        ),
        const SizedBox(width: 8),
        Text(texto,
            style: TextStyle(
              color: cumplido ? Colors.green : Colors.grey,
              fontSize: 13,
            )),
      ],
    );
  }
}
```

## Testing del wizard

```dart
blocTest<RegistroCubit, RegistroState>(
  'avanza al paso 2 cuando nombre es válido',
  build: () => RegistroCubit(repo: repo),
  act: (cubit) {
    cubit.nombreCambiado('Juan');
    cubit.siguiente();
  },
  expect: () => [
    isA<RegistroState>().having((s) => s.nombre, 'nombre', 'Juan'),
    isA<RegistroState>().having((s) => s.pasoActual, 'paso', 1),
  ],
);

blocTest<RegistroCubit, RegistroState>(
  'completa registro exitosamente',
  build: () {
    when(() => repo.registrar(
      nombre: any(), email: any(), password: any(),
    )).thenAnswer((_) async => Right(unit));
    return RegistroCubit(repo: repo);
  },
  act: (cubit) {
    cubit.nombreCambiado('Juan');
    cubit.siguiente();
    cubit.emailCambiado('j@b.com');
    cubit.siguiente();
    cubit.passwordCambiado('123456');
    cubit.enviar();
  },
  skip: 5,
  expect: () => [isA<RegistroState>().having((s) => s.completado, 'completado', true)],
);
```
