# 10. Ejemplo: Dashboard Multi-Bloc

> **Ver también**: `06-NIVEL-EXPERTO/03-comunicacion-features.md` — patrones de comunicación cross-feature con Event Bus (eventos globales como login/logout).
> Este ejemplo se enfoca en la orquestación desde la UI con MultiBlocProvider + MultiBlocListener.

## Funcionalidad

Dashboard con 3 Cubits independientes coordinados:

- `UsuarioCubit`: datos del perfil
- `NotificacionesCubit`: lista de notificaciones
- `DashboardCubit`: orquesta los dos anteriores y expone estado combinado

## Arquitectura

```
DashboardPage
  └── MultiBlocProvider
       ├── BlocProvider → UsuarioCubit (carga perfil)
       ├── BlocProvider → NotificacionesCubit (carga notis)
       └── BlocProvider → DashboardCubit (coordina)
            ├── BlocListener → UsuarioCubit: cuando carga, notifica
            └── BlocListener → NotificacionesCubit: cuando carga, notifica
```

## Cubits individuales

```dart
// UsuarioCubit
sealed class UsuarioState extends Equatable {
  const UsuarioState();
  @override List<Object?> get props => [];
}
final class UsuarioInicial extends UsuarioState { const UsuarioInicial(); }
final class UsuarioCargando extends UsuarioState { const UsuarioCargando(); }
final class UsuarioCargado extends UsuarioState {
  final User user;
  const UsuarioCargado(this.user);
  @override List<Object?> get props => [user];
}
final class UsuarioError extends UsuarioState {
  final String mensaje;
  const UsuarioError(this.mensaje);
  @override List<Object?> get props => [mensaje];
}

class UsuarioCubit extends Cubit<UsuarioState> {
  final UserRepository _repo;
  UsuarioCubit({required UserRepository repo})
      : _repo = repo, super(const UsuarioInicial());

  Future<void> cargar(String id) async {
    emit(const UsuarioCargando());
    final result = await _repo.obtener(id);
    result.fold(
      (e) => emit(UsuarioError(e.mensaje)),
      (user) => emit(UsuarioCargado(user)),
    );
  }
}

// NotificacionesCubit
class NotificacionesCubit extends Cubit<List<Notificacion>> {
  final NotificacionRepository _repo;
  NotificacionesCubit({required NotificacionRepository repo})
      : _repo = repo, super([]);

  Future<void> cargar() async {
    final result = await _repo.obtenerRecientes();
    result.fold((_) => null, (items) => emit(items));
  }

  int get noLeidas => state.where((n) => !n.leida).length;
}
```

## DashboardCubit (orquestador)

```dart
// presentation/cubit/dashboard_state.dart
class DashboardState extends Equatable {
  final UsuarioState usuario;
  final List<Notificacion> notificaciones;
  final bool todoCargado;

  const DashboardState({
    required this.usuario,
    required this.notificaciones,
    this.todoCargado = false,
  });

  DashboardState copyWith({
    UsuarioState? usuario,
    List<Notificacion>? notificaciones,
    bool? todoCargado,
  }) {
    return DashboardState(
      usuario: usuario ?? this.usuario,
      notificaciones: notificaciones ?? this.notificaciones,
      todoCargado: todoCargado ?? this.todoCargado,
    );
  }

  @override
  List<Object?> get props => [usuario, notificaciones, todoCargado];
}
```

```dart
// presentation/cubit/dashboard_cubit.dart
class DashboardCubit extends Cubit<DashboardState> {
  DashboardCubit()
      : super(DashboardState(
          usuario: const UsuarioInicial(),
          notificaciones: [],
        ));

  void notificarUsuarioCargado(UsuarioState usuario) {
    final nuevo = state.copyWith(usuario: usuario);
    _verificarCompleto(nuevo);
  }

  void notificarNotificacionesCargadas(List<Notificacion> notificaciones) {
    final nuevo = state.copyWith(notificaciones: notificaciones);
    _verificarCompleto(nuevo);
  }

  void _verificarCompleto(DashboardState nuevo) {
    final completo = nuevo.usuario is UsuarioCargado &&
        nuevo.notificaciones.isNotEmpty;
    emit(nuevo.copyWith(todoCargado: completo));
  }
}
```

## Pantalla dashboard

```dart
class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (_) => UsuarioCubit(repo: getIt())..cargar('actual'),
        ),
        BlocProvider(
          create: (_) => NotificacionesCubit(repo: getIt())..cargar(),
        ),
        BlocProvider(create: (_) => DashboardCubit()),
      ],
      child: const _DashboardListener(),
    );
  }
}

// Orquestador: conecta los cubits individuales al DashboardCubit
class _DashboardListener extends StatelessWidget {
  const _DashboardListener();

  @override
  Widget build(BuildContext context) {
    return MultiBlocListener(
      listeners: [
        BlocListener<UsuarioCubit, UsuarioState>(
          listenWhen: (_, current) => current is UsuarioCargado,
          listener: (context, state) {
            context.read<DashboardCubit>().notificarUsuarioCargado(state);
          },
        ),
        BlocListener<NotificacionesCubit, List<Notificacion>>(
          listenWhen: (_, current) => current.isNotEmpty,
          listener: (context, notis) {
            context
                .read<DashboardCubit>()
                .notificarNotificacionesCargadas(notis);
          },
        ),
      ],
      child: const _DashboardView(),
    );
  }
}

class _DashboardView extends StatelessWidget {
  const _DashboardView();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          BlocSelector<NotificacionesCubit, List<Notificacion>, int>(
            selector: (notis) => notis.where((n) => !n.leida).length,
            builder: (context, noLeidas) {
              return IconButton(
                icon: Badge(
                  isLabelVisible: noLeidas > 0,
                  label: Text('$noLeidas'),
                  child: const Icon(Icons.notifications),
                ),
                onPressed: () => context.push('/notificaciones'),
              );
            },
          ),
        ],
      ),
      body: BlocBuilder<DashboardCubit, DashboardState>(
        builder: (context, state) {
          if (!state.todoCargado) {
            return const Center(child: CircularProgressIndicator());
          }

          final user = (state.usuario as UsuarioCargado).user;

          return RefreshIndicator(
            onRefresh: () async {
              context.read<UsuarioCubit>().cargar('actual');
              context.read<NotificacionesCubit>().cargar();
            },
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // Header con avatar
                Card(
                  child: ListTile(
                    leading: CircleAvatar(
                      radius: 30,
                      backgroundImage: NetworkImage(user.avatarUrl),
                    ),
                    title: Text(user.nombre,
                        style: const TextStyle(fontWeight: FontWeight.bold)),
                    subtitle: Text(user.email),
                    trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: () => context.push('/perfil'),
                  ),
                ),
                const SizedBox(height: 16),
                // Tarjetas de resumen
                Row(
                  children: [
                    Expanded(
                      child: _ResumenCard(
                        icon: Icons.shopping_bag,
                        label: 'Pedidos',
                        valor: '${user.totalPedidos}',
                        color: Colors.blue,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: _ResumenCard(
                        icon: Icons.favorite,
                        label: 'Favoritos',
                        valor: '${state.notificaciones.length}',
                        color: Colors.red,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 24),
                Text('Notificaciones recientes',
                    style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 8),
                for (final noti in state.notificaciones.take(3))
                  ListTile(
                    leading: Icon(
                      noti.leida ? Icons.circle : Icons.circle_outlined,
                      size: 12,
                      color: noti.leida ? Colors.grey : Colors.blue,
                    ),
                    title: Text(noti.titulo),
                    subtitle: Text(noti.mensaje, maxLines: 1),
                  ),
              ],
            ),
          );
        },
      ),
    );
  }
}

class _ResumenCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final String valor;
  final Color color;

  const _ResumenCard({
    required this.icon,
    required this.label,
    required this.valor,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Icon(icon, size: 32, color: color),
            const SizedBox(height: 8),
            Text(valor,
                style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                    color: color)),
            Text(label, style: const TextStyle(color: Colors.grey)),
          ],
        ),
      ),
    );
  }
}
```

## Patrón: Cubits que hablan entre sí

Los Cubits **no se conocen entre sí**. La comunicación se da a través de:

1. **BlocListener** en la UI: escucha un Cubit y llama a otro
2. **DashboardCubit**: recibe notificaciones externas y expone estado combinado
3. **StreamSubscription** dentro de un Cubit (avanzado)

Esto mantiene cada Cubit desacoplado y testeable por separado.
