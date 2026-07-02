# 5. Widgets flutter_bloc — Parte 1 (Provider + Builder + read/watch)

> **Ver también**: `01-CLEAN-ARCHITECTURE/05c-presentation-ui-layer.md` — uso real de BlocProvider, BlocBuilder y context.read en UserDetailPage y UsersListPage.

> Referencia oficial: [Flutter Bloc Concepts](https://bloclibrary.dev/flutter-bloc-concepts/)

## BlocProvider

Provee una instancia de Cubit/Bloc al árbol de widgets.

```dart
// Modo 1: crear y auto-diponer (se cierra cuando el widget sale del árbol)
BlocProvider(
  create: (_) => MiCubit(),
  child: const MiWidget(),
);

// Modo 2: reusar una instancia existente
BlocProvider.value(
  value: context.read<MiCubit>(),
  child: const OtroWidget(),
);
```

### BlocProvider a nivel de app

```dart
void main() {
  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => AuthCubit(repo: getIt())),
        BlocProvider(create: (_) => TemaCubit()),
        BlocProvider(create: (_) => CarritoBloc(repo: getIt())),
      ],
      child: const MyApp(),
    ),
  );
}
```

`MultiBlocProvider` evita anidamientos profundos.

### BlocProvider dentro de una ruta

```dart
// Cada página crea su propio Cubit con ciclo de vida atado a la ruta
class PerfilPage extends StatelessWidget {
  const PerfilPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => PerfilCubit(repo: getIt())..cargarPerfil(),
      child: const _PerfilView(),
    );
  }
}
```

Cuando la página sale del árbol, el Cubit se cierra automáticamente.

## context.read<T>()

Obtiene el Bloc/Cubit sin escuchar cambios.

```dart
// Usar en callbacks
onPressed: () => context.read<ContadorCubit>().incrementar(),

// Usar en initState
context.read<PerfilCubit>().cargarPerfil();

// Usar para obtener estado una sola vez
final estado = context.read<ContadorCubit>().state;
```

`context.read` no causa reconstrucciones. Es ideal para `onPressed`, `initState`, `dispose`.

## context.watch<T>()

Obtiene el Bloc/Cubit y se suscribe a cambios (reconstruye el widget).

```dart
@override
Widget build(BuildContext context) {
  // Cada vez que el estado cambia, este widget se reconstruye
  final estado = context.watch<ContadorCubit>().state;
  return Text('${estado.valor}');
}
```

**Precaución**: `context.watch` en un widget padre causa que **todo** el widget se reconstruya. Úsalo en widgets pequeños u hojas, no en widgets grandes.

## BlocBuilder

Reconstruye solo el subárbol que envuelve, no todo el widget.

```dart
BlocBuilder<ContadorCubit, ContadorState>(
  builder: (context, state) {
    // Solo este subárbol se reconstruye
    return Text('Valor: ${state.valor}');
  },
);
```

### buildWhen: control fino

```dart
BlocBuilder<ContadorCubit, ContadorState>(
  buildWhen: (anterior, actual) {
    // Solo reconstruir si el valor cambió, ignorar otros cambios
    return actual.valor != anterior.valor;
  },
  builder: (context, state) {
    return Text('${state.valor}');
  },
);
```

Esto evita reconstrucciones innecesarias cuando el estado tiene múltiples campos.

## Patrón completo: Provider + Builder + read

```dart
class ContadorPage extends StatelessWidget {
  const ContadorPage({super.key});

  @override
  Widget build(BuildContext context) {
    // BlocProvider: crea y provee el Cubit
    return BlocProvider(
      create: (_) => ContadorCubit(),
      child: Scaffold(
        appBar: AppBar(title: const Text('Contador')),
        body: const Center(
          child: _Display(),  // se reconstruye cuando cambia
        ),
        floatingActionButton: const _Botones(), // NO se reconstruye
      ),
    );
  }
}

class _Display extends StatelessWidget {
  const _Display();

  @override
  Widget build(BuildContext context) {
    // BlocBuilder: solo este widget se reconstruye
    return BlocBuilder<ContadorCubit, ContadorState>(
      builder: (context, state) {
        return Text(
          '${state.valor}',
          style: const TextStyle(fontSize: 48),
        );
      },
    );
  }
}

class _Botones extends StatelessWidget {
  const _Botones();

  @override
  Widget build(BuildContext context) {
    // context.read no causa reconstrucción
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        FloatingActionButton(
          onPressed: () => context.read<ContadorCubit>().incrementar(),
          child: const Icon(Icons.add),
        ),
        const SizedBox(height: 8),
        FloatingActionButton(
          onPressed: () => context.read<ContadorCubit>().decrementar(),
          child: const Icon(Icons.remove),
        ),
      ],
    );
  }
}
```

## Reglas de contexto

```dart
// ERROR: no puedes usar context.read en el mismo build donde creas el provider
@override
Widget build(BuildContext context) {
  return BlocProvider(
    create: (_) => MiCubit(),
    child: Builder(
      builder: (context) {
        // OK: este contexto es HIJO del BlocProvider
        return ElevatedButton(
          onPressed: () => context.read<MiCubit>().accion(),
          child: const Text('OK'),
        );
      },
    ),
  );
}
```

## BlocBuilder con tipos genéricos

```dart
// Si solo hay un BlocProvider de ContadorCubit en el árbol,
// puedes omitir el tipo en BlocBuilder:
BlocBuilder(
  builder: (context, state) {
    // state se infiere como ContadorState
    return Text('${state.valor}');
  },
);

// Pero es mejor ser explícito:
BlocBuilder<ContadorCubit, ContadorState>(
  builder: (context, state) => Text('${state.valor}'),
);
```
