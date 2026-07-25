# 19: Cubit vs BLoC — ¿Cuándo usar cuál?

> Ambos son excelentes. La clave es saber cuándo elegir uno u otro.

---

## Comparación directa

| Aspecto | Cubit | BLoC |
|---------|-------|------|
| Complejidad | Baja | Alta |
| Boilerplate | Poco | Mucho |
| Eventos | No tiene | Sí tiene |
| Testing | Simple | Más verboso |
| Traza de acciones | No | Sí (eventos) |
| Para features simples | ✅ Ideal | ⚠️ Over-engineering |
| Para features complejas | ⚠️ Puede ser poco | ✅ Ideal |

---

## Regla práctica

```
¿La feature tiene 3 o menos acciones?
  → CUBIT

¿La feature tiene 4+ acciones o necesita traza?
  → BLoC
```

---

## Ejemplo: Cubit (simple)

```dart
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
  void reset() => emit(0);
}
```

**Ideal para:** Contadores, toggles, formularios simples, filtros.

---

## Ejemplo: BLoC (complejo)

```dart
// Eventos
abstract class AuthEvent {}
class SignIn extends AuthEvent {
  final String email, password;
  SignIn(this.email, this.password);
}
class SignOut extends AuthEvent {}
class CheckSession extends AuthEvent {}

// BLoC
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  AuthBloc() : super(AuthInitial()) {
    on<SignIn>(_onSignIn);
    on<SignOut>(_onSignOut);
    on<CheckSession>(_onCheckSession);
  }

  Future<void> _onSignIn(SignIn event, Emitter<AuthState> emit) async {
    emit(AuthLoading());
    try {
      final user = await _repo.signIn(event.email, event.password);
      emit(AuthAuthenticated(user));
    } catch (e) {
      emit(AuthError(e.toString()));
    }
  }
  // ...
}
```

**Ideal para:** Auth, flujos con múltiples pasos, features con traza de auditoría.

---

## Decision tree

```
Feature nueva
├── ¿Tiene menos de 4 acciones?
│   ├── SÍ → ¿Necesitas traza de eventos?
│   │   ├── SÍ → BLoC (aunque sea simple)
│   │   └── NO → CUBIT ✅
│   └── NO → BLoC ✅
│
├── ¿Múltiples actores la usan?
│   ├── SÍ → BLoC (eventos documentan quién hizo qué)
│   └── NO → Cubit
│
└── ¿Equipo junior?
    ├── SÍ → Cubit (más fácil de entender)
    └── NO → BLoC (más estructurado)
```

---

## Errores comunes

| Error | Solución |
|-------|----------|
| Cubit con 15+ métodos | Dividir en múltiples cubits o usar BLoC |
| BLoC para un toggle | Usa Cubit, es over-engineering |
| No testear por evento | En BLoC, teste por evento específico |
| Mezclar lógica en UI | Toda lógica en Cubit/BLoC, solo presentación en UI |

---

**Siguiente:** [20-debugging-bloc.md](./20-debugging-bloc.md)
