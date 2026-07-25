# 20: Debugging de BLoC/Cubit

> Los bugs de estado son los más difíciles de debugear. Este archivo te da el workflow exacto.

---

## Los 5 bugs más comunes de BLoC/Cubit

### 1. Estado no se actualiza

```dart
// ❌ BUG: emit() sin await
void load() async {
  emit(Loading());
  final data = await fetch(); // Lenta
  emit(Loaded(data)); // Puede no ejecutarse si el widget se desmontó
}

// ✅ CORRECTO: Verificar si está cerrado
void load() async {
  emit(Loading());
  try {
    final data = await fetch();
    if (isClosed) return; // ← CRUCIAL
    emit(Loaded(data));
  } catch (e) {
    if (isClosed) return;
    emit(Error(e.toString()));
  }
}
```

---

### 2. Múltiples emisiones en secuencia

```dart
// ❌ Solo se ve el último estado
void complexOperation() async {
  emit(Step1());
  emit(Step2()); // Se ejecuta inmediatamente
  emit(Step3()); // Step1 y Step2 nunca se ven
}

// ✅ Usar await o yield
void complexOperation() async {
  emit(Step1());
  await Future.delayed(Duration(milliseconds: 100));
  emit(Step2());
  await Future.delayed(Duration(milliseconds: 100));
  emit(Step3());
}
```

---

### 3. Estado anterior no se preserva

```dart
// ❌ Se pierde el estado anterior
void updateName(String name) {
  emit(UserState(name: name)); // Se pierde email, age, etc.
}

// ✅ Copiar estado anterior
void updateName(String name) {
  emit(state.copyWith(name: name)); // Preserva todo lo demás
}
```

---

### 4. Listener escucha después de dispose

```dart
// ❌ Memory leak
@override
Widget build(BuildContext context) {
  return BlocListener<AuthCubit, AuthState>(
    listener: (context, state) {
      // Se ejecuta después de dispose
      ScaffoldMessenger.of(context).showSnackBar(...);
    },
    child: Container(),
  );
}

// ✅ Usar listenWhen
BlocListener<AuthCubit, AuthState>(
  listenWhen: (prev, curr) => curr is Authenticated,
  listener: (context, state) {
    // Solo se ejecuta cuando hay auth
  },
  child: Container(),
)
```

---

### 5. Cubit se cierra y se reabre

```dart
// ❌ BUG: Crear múltiples instancias
onPressed: () {
  context.read<AuthCubit>().close(); // Cierra el cubit
  context.read<AuthCubit>().signIn(email, pass); // Error: cubit cerrado
}

// ✅ No cerrar manualmente el cubit
onPressed: () {
  context.read<AuthCubit>().signIn(email, pass);
}
```

---

## Herramientas de debugging

### 1. Print debugging

```dart
class AuthCubit extends Cubit<AuthState> {
  AuthCubit() : super(AuthInitial()) {
    print('[AuthCubit] Inicializado');
  }

  void signIn(String email, String pass) async {
    print('[AuthCubit] signIn: $email');
    emit(AuthLoading());
    try {
      final user = await _repo.signIn(email, pass);
      print('[AuthCubit] signIn exitoso: ${user.id}');
      emit(AuthAuthenticated(user));
    } catch (e) {
      print('[AuthCubit] signIn error: $e');
      emit(AuthError(e.toString()));
    }
  }
}
```

### 2. BlocObserver

```dart
class AppBlocObserver extends BlocObserver {
  @override
  void onChange(BlocBase bloc, Change change) {
    super.onChange(bloc, change);
    print('[${bloc.runtimeType}] $change');
  }

  @override
  void onError(BlocBase bloc, Object error, StackTrace stackTrace) {
    super.onError(bloc, error, stackTrace);
    print('[${bloc.runtimeType}] ERROR: $error');
  }
}

// En main():
Bloc.observer = AppBlocObserver();
```

### 3. DevTools - Bloc Inspector

- Ve el estado actual de cada BLoC/Cubit
- Historial de estados
- Estados suscritos

---

## Checklist de debugging BLoC

```
□ ¿isClosed se verifica antes de emit?
□ ¿state.copyWith() se usa para preservar estado?
□ ¿Hay un solo emit por flujo?
□ ¿BlocObserver está configurado?
□ ¿Se testeó cada evento individualmente?
□ ¿No se cierra el cubit manualmente?
```

---

**Volver al índice:** [README.md](./README.md)
