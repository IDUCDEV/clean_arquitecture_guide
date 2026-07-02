# 18. Patrón Avanzado: Lista con Estados, Filtros, Pull-to-Refresh y previousState

## El problema

Una lista típica necesita:
- Cargar datos al abrir la pantalla
- Mostrar loading en la primera carga
- Mostrar error completo si falla sin datos previos
- Mostrar error inline (con datos viejos visibles) si falla pero ya había datos
- Pull-to-refresh
- Filtros por estado/categoría
- Empty state cuando no hay resultados
- Scroll suave con slivers
- Cards con indicadores visuales (badge, progreso)

Este capítulo cubre el patrón completo.

## 1. Estados del Cubit

La clave es que `RaffleListError` guarda el `previousState`:

```dart
// presentation/cubit/raffle_list_state.dart
sealed class RaffleListState extends Equatable {
  const RaffleListState();

  @override
  List<Object?> get props => [];
}

final class RaffleListInitial extends RaffleListState {
  const RaffleListInitial();
}

final class RaffleListLoading extends RaffleListState {
  const RaffleListLoading();
}

final class RaffleListLoaded extends RaffleListState {
  final List<RaffleEntity> raffles;
  final String? activeFilter;
  final int activeCount;

  const RaffleListLoaded({
    required this.raffles,
    this.activeFilter,
    required this.activeCount,
  });

  RaffleListLoaded copyWith({
    List<RaffleEntity>? raffles,
    String? Function()? activeFilter,
    int? activeCount,
  }) {
    return RaffleListLoaded(
      raffles: raffles ?? this.raffles,
      activeFilter: activeFilter != null ? activeFilter() : this.activeFilter,
      activeCount: activeCount ?? this.activeCount,
    );
  }

  @override
  List<Object?> get props => [raffles, activeFilter, activeCount];
}

final class RaffleListError extends RaffleListState {
  final String message;
  final RaffleListState? previousState;

  const RaffleListError(this.message, {this.previousState});

  bool get hasPreviousData => previousState is RaffleListLoaded;

  @override
  List<Object?> get props => [message, previousState];
}
```

## 2. Cubit con manejo de previousState

```dart
// presentation/cubit/raffle_list_cubit.dart
class RaffleListCubit extends Cubit<RaffleListState> {
  final RaffleRepository _repo;

  RaffleListCubit({required RaffleRepository repo})
      : _repo = repo,
        super(const RaffleListInitial());

  Future<void> loadRaffles({String? statusFilter}) async {
    if (state is RaffleListInitial) {
      emit(const RaffleListLoading());
    }

    final result = await _repo.getRaffles(status: statusFilter);

    result.fold(
      (failure) {
        // previousState: preserva los datos que ya estaban cargados
        emit(RaffleListError(
          failure.message,
          previousState: state is RaffleListLoaded ? state : null,
        ));
      },
      (raffles) {
        final activeCount = raffles.where((r) => r.status == 'open').length;
        emit(RaffleListLoaded(
          raffles: raffles,
          activeFilter: statusFilter,
          activeCount: activeCount,
        ));
      },
    );
  }
}
```

## 3. Widgets reutilizables (core)

### LoadingIndicator

```dart
// core/widgets/loading_indicator.dart
enum LoadingIndicatorType { spinner, circular, shimmer }
enum LoadingIndicatorSize { small, medium, large }

class LoadingIndicator extends StatelessWidget {
  final LoadingIndicatorType type;
  final LoadingIndicatorSize size;

  const LoadingIndicator({
    super.key,
    this.type = LoadingIndicatorType.circular,
    this.size = LoadingIndicatorSize.medium,
  });

  double get _size => switch (size) {
        LoadingIndicatorSize.small => 20,
        LoadingIndicatorSize.medium => 40,
        LoadingIndicatorSize.large => 60,
      };

  @override
  Widget build(BuildContext context) {
    return switch (type) {
      LoadingIndicatorType.spinner => SizedBox(
          width: _size,
          height: _size,
          child: CircularProgressIndicator(strokeWidth: _size / 10),
        ),
      LoadingIndicatorType.circular => CircularProgressIndicator(),
      LoadingIndicatorType.shimmer => Shimmer(
          child: Container(
            width: double.infinity,
            height: _size,
            color: Colors.grey[300],
          ),
        ),
    };
  }
}
```

### ErrorView

```dart
// core/widgets/error_view.dart
class ErrorView extends StatelessWidget {
  final String title;
  final String message;
  final VoidCallback? onRetry;

  const ErrorView({
    super.key,
    required this.title,
    required this.message,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            Text(title,
                style: const TextStyle(
                    fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(message, textAlign: TextAlign.center),
            if (onRetry != null) ...[
              const SizedBox(height: 24),
              FilledButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh),
                label: const Text('Reintentar'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

### EmptyState

```dart
// core/widgets/empty_state.dart
class EmptyState extends StatelessWidget {
  final IconData icon;
  final String title;
  final String message;
  final Widget? action;

  const EmptyState({
    super.key,
    required this.icon,
    required this.title,
    required this.message,
    this.action,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 80, color: Colors.grey[400]),
            const SizedBox(height: 16),
            Text(title,
                style: const TextStyle(
                    fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Text(message,
                textAlign: TextAlign.center, color: Colors.grey[600]),
            if (action != null) ...[
              const SizedBox(height: 24),
              action!,
            ],
          ],
        ),
      ),
    );
  }
}
```

### PullToRefreshWrapper

```dart
// core/widgets/pull_to_refresh_wrapper.dart
class PullToRefreshWrapper extends StatelessWidget {
  final Future<void> Function() onRefresh;
  final Widget child;

  const PullToRefreshWrapper({
    super.key,
    required this.onRefresh,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return RefreshIndicator(
      onRefresh: onRefresh,
      color: Theme.of(context).colorScheme.primary,
      displacement: 40,
      child: child,
    );
  }
}
```

### AppCard

```dart
// core/widgets/app_card.dart
class AppCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final EdgeInsetsGeometry? padding;

  const AppCard({
    super.key,
    required this.child,
    this.onTap,
    this.padding,
  });

  @override
  Widget build(BuildContext context) {
    final card = Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: Colors.grey[200]!),
      ),
      margin: EdgeInsets.zero,
      child: padding != null
          ? Padding(padding: padding!, child: child)
          : child,
    );

    if (onTap != null) {
      return InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: card,
      );
    }

    return card;
  }
}
```

## 4. Página completa con el patrón

```dart
// presentation/pages/raffles_list_page.dart
class RafflesListPage extends StatefulWidget {
  const RafflesListPage({super.key});

  @override
  State<RafflesListPage> createState() => _RafflesListPageState();
}

class _RafflesListPageState extends State<RafflesListPage> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<RaffleListCubit>().loadRaffles();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Rifas')),
      body: BlocBuilder<RaffleListCubit, RaffleListState>(
        builder: (context, state) {
          return switch (state) {
            RaffleListInitial() => const SizedBox.shrink(),
            // Primer loading: indicador centrado
            RaffleListLoading() => const Center(
                child: LoadingIndicator(
                  type: LoadingIndicatorType.spinner,
                  size: LoadingIndicatorSize.large,
                ),
              ),
            // Error SIN datos previos: pantalla de error completa
            RaffleListError(:final message, :final previousState)
                when previousState == null =>
              ErrorView(
                title: 'Error al cargar',
                message: message,
                onRetry: () =>
                    context.read<RaffleListCubit>().loadRaffles(),
              ),
            // Error CON datos previos: mostrar datos + SnackBar
            RaffleListError(:final message, :final previousState)
                when previousState != null =>
              _buildContentWithError(
                context,
                previousState as RaffleListLoaded,
                message,
              ),
            // Datos cargados
            RaffleListLoaded() => _RafflesListContent(state: state),
          };
        },
      ),
    );
  }

  Widget _buildContentWithError(
    BuildContext context,
    RaffleListLoaded data,
    String errorMessage,
  ) {
    // Muestra los datos viejos y dispara SnackBar
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(errorMessage),
          backgroundColor: Colors.orange,
          action: SnackBarAction(
            label: 'Reintentar',
            onPressed: () =>
                context.read<RaffleListCubit>().loadRaffles(),
          ),
        ),
      );
    });

    return _RafflesListContent(state: data);
  }
}
```

## 5. Contenido de la lista con slivers

```dart
class _RafflesListContent extends StatelessWidget {
  final RaffleListLoaded state;

  const _RafflesListContent({required this.state});

  @override
  Widget build(BuildContext context) {
    return PullToRefreshWrapper(
      onRefresh: () async {
        await context.read<RaffleListCubit>().loadRaffles(
              statusFilter: state.activeFilter,
            );
      },
      child: CustomScrollView(
        slivers: [
          // Barra de resumen
          SliverToBoxAdapter(
            child: _SummaryBar(activeCount: state.activeCount),
          ),
          // Filtros
          SliverToBoxAdapter(
            child: _FilterChips(
              activeFilter: state.activeFilter,
              onFilterChanged: (filter) {
                context.read<RaffleListCubit>().loadRaffles(
                      statusFilter: filter,
                    );
              },
            ),
          ),
          // Lista o empty state
          if (state.raffles.isEmpty)
            const SliverFillRemaining(
              child: EmptyState(
                icon: Icons.workspaces_outlined,
                title: 'No tienes rifas',
                message:
                    'Crea tu primera rifa para empezar a vender números',
              ),
            )
          else
            SliverPadding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              sliver: SliverList(
                delegate: SliverChildBuilderDelegate(
                  (context, index) =>
                      _RaffleCard(raffle: state.raffles[index]),
                  childCount: state.raffles.length,
                ),
              ),
            ),
        ],
      ),
    );
  }
}
```

## 6. Sub-widgets de la lista

### SummaryBar

```dart
class _SummaryBar extends StatelessWidget {
  final int activeCount;

  const _SummaryBar({required this.activeCount});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.all(16),
      padding: const EdgeInsets.symmetric(
        horizontal: 24,
        vertical: 12,
      ),
      decoration: BoxDecoration(
        color: Colors.blue.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        children: [
          const Icon(Icons.auto_awesome, color: Colors.blue),
          const SizedBox(width: 8),
          Text(
            '$activeCount rifas activas',
            style: const TextStyle(
              fontWeight: FontWeight.w600,
              color: Colors.blue,
            ),
          ),
        ],
      ),
    );
  }
}
```

### FilterChips con ValueKey

```dart
class _FilterChips extends StatelessWidget {
  final String? activeFilter;
  final ValueChanged<String?> onFilterChanged;

  const _FilterChips({
    required this.activeFilter,
    required this.onFilterChanged,
  });

  static const _filters = <String?, String>{
    null: 'Todas',
    'open': 'Abiertas',
    'closed': 'Cerradas',
    'drawn': 'Sorteo Realizado',
    'cancelled': 'Canceladas',
  };

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 48,
      child: ListView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        children: _filters.entries.map((entry) {
          final isSelected = activeFilter == entry.key;
          return Padding(
            padding: const EdgeInsets.only(right: 4),
            child: FilterChip(
              // ValueKey preserva el estado interno del chip
              // al reordenar o reciclar la lista horizontal
              key: ValueKey('filter_${entry.key}'),
              label: Text(
                entry.value,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                  color: isSelected ? Colors.white : Colors.grey[700],
                ),
              ),
              selected: isSelected,
              onSelected: (_) => onFilterChanged(entry.key),
              checkmarkColor: Colors.white,
              selectedColor: Colors.blue,
            ),
          );
        }).toList(),
      ),
    );
  }
}
```

Por qué `ValueKey('filter_${entry.key}')`:

```dart
// Sin ValueKey: Flutter no sabe qué chip es cuál al reordenar
// Con ValueKey('filter_open'): Flutter identifica cada chip
// y preserva su estado visual/animation interno

// Alternativa válida:
ObjectKey(entry.key) // cuando la key es un objeto completo
```

### RaffleCard

```dart
class _RaffleCard extends StatelessWidget {
  final RaffleEntity raffle;

  const _RaffleCard({required this.raffle});

  String _statusLabel(String status) {
    return switch (status) {
      'open' => 'Abierta',
      'closed' => 'Cerrada',
      'drawn' => 'Sorteada',
      'cancelled' => 'Cancelada',
      _ => status,
    };
  }

  Color _statusColor(String status) {
    return switch (status) {
      'open' => Colors.green,
      'closed' => Colors.orange,
      'drawn' => Colors.blue,
      'cancelled' => Colors.red,
      _ => Colors.grey,
    };
  }

  double get _progress {
    if (raffle.totalNumbers == 0) return 0;
    return raffle.soldCount / raffle.totalNumbers;
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: AppCard(
        onTap: () => context.push('/raffle/${raffle.id}'),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Fila: título + badge de estado
            Row(
              children: [
                Expanded(
                  child: Text(
                    raffle.title,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 2,
                  ),
                  decoration: BoxDecoration(
                    color: _statusColor(raffle.status)
                        .withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    _statusLabel(raffle.status),
                    style: TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w600,
                      color: _statusColor(raffle.status),
                    ),
                  ),
                ),
              ],
            ),
            // Descripción (opcional)
            if (raffle.description.isNotEmpty) ...[
              const SizedBox(height: 4),
              Text(
                raffle.description,
                style: const TextStyle(
                    fontSize: 13, color: Colors.grey),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ],
            const SizedBox(height: 12),
            // Fila: precio + progreso numérico
            Row(
              children: [
                const Icon(Icons.attach_money,
                    size: 16, color: Colors.grey),
                const SizedBox(width: 4),
                Text(
                  '${raffle.currency} ${raffle.ticketPrice.toStringAsFixed(2)}',
                  style: const TextStyle(
                      fontSize: 13, color: Colors.grey),
                ),
                const Spacer(),
                Text(
                  '${raffle.soldCount}/${raffle.totalNumbers}',
                  style: const TextStyle(
                    fontSize: 13,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 6),
            // Barra de progreso
            ClipRRect(
              borderRadius: BorderRadius.circular(4),
              child: LinearProgressIndicator(
                value: _progress,
                backgroundColor: Colors.grey.withValues(alpha: 0.3),
                color: _progress >= 1 ? Colors.green : Colors.blue,
                minHeight: 6,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

## 7. Árbol completo de widgets

```
RafflesListPage (StatefulWidget)
  └── Scaffold
      └── BlocBuilder<RaffleListCubit, RaffleListState>
          ├── [Loading] → LoadingIndicator
          ├── [Error + sin previousState] → ErrorView
          ├── [Error + con previousState] → SnackBar + _RafflesListContent
          └── [Loaded] → _RafflesListContent
              └── PullToRefreshWrapper
                  └── CustomScrollView
                      ├── SliverToBoxAdapter → _SummaryBar
                      │   └── Container (icono + texto)
                      ├── SliverToBoxAdapter → _FilterChips
                      │   └── ListView horizontal
                      │       └── FilterChip [ValueKey]
                      ├── [Empty] → SliverFillRemaining → EmptyState
                      └── [Data] → SliverPadding
                          └── SliverList
                              └── _RaffleCard [xN]
                                  └── AppCard
                                      └── Column
                                          ├── Row (title + badge)
                                          ├── Text (description)
                                          ├── Row (precio + progreso)
                                          └── LinearProgressIndicator
```

## 8. Flujo de estados visual

```
Estado                | UI que ve el usuario
──────────────────────┼──────────────────────────
Initial              | Nada (sizedbox)
Loading (1ra vez)    | Spinner centrado
Error (sin datos)    | ErrorView con botón reintentar
Error (con datos)    | Datos viejos + SnackBar naranja
Loaded               | Lista normal
Loaded + pull        | Lista + indicador en el tope
Loaded + filter      | Lista filtrada
Empty                | EmptyState centrado vertical
```

## 9. Testing del patrón previousState

```dart
void main() {
  late RaffleListCubit cubit;
  late MockRaffleRepo repo;

  setUp(() {
    repo = MockRaffleRepo();
    cubit = RaffleListCubit(repo: repo);
  });

  tearDown(() => cubit.close());

  blocTest<RaffleListCubit, RaffleListState>(
    'emite Error SIN previousState cuando falla la primera carga',
    build: () {
      when(() => repo.getRaffles())
          .thenAnswer((_) async => Left(ServerFailure('Error')));
      return cubit;
    },
    act: (cubit) => cubit.loadRaffles(),
    expect: () => [
      const RaffleListLoading(),
      isA<RaffleListError>()
          .having((e) => e.hasPreviousData, 'hasPreviousData', false),
    ],
  );

  blocTest<RaffleListCubit, RaffleListState>(
    'emite Error CON previousState cuando falla tras carga exitosa',
    build: () {
      when(() => repo.getRaffles())
          .thenAnswer((_) async => Right([raffle1]))
          .thenAnswer((_) async => Left(ServerFailure('Error red')));
      return cubit;
    },
    act: (cubit) async {
      await cubit.loadRaffles(); // primera: exitosa
      await cubit.loadRaffles(); // segunda: falla
    },
    expect: () => [
      const RaffleListLoading(),
      RaffleListLoaded(raffles: [raffle1], activeCount: 0),
      isA<RaffleListError>()
          .having((e) => e.hasPreviousData, 'hasPreviousData', true),
    ],
  );
}
```

## Resumen del patrón

| Elemento | Propósito |
|---|---|
| `previousState` en error | Preservar datos viejos en fallos |
| `PullToRefreshWrapper` | Reutilizar refresh en varias listas |
| `CustomScrollView` + slivers | Scroll suave con headers + lista + empty |
| `SliverFillRemaining` | Empty state centrado vertical |
| `ValueKey` en chips | Preservar estado interno en scroll horizontal |
| Widgets extraídos | `_SummaryBar`, `_FilterChips`, `_RaffleCard` |
| Widgets core | `AppCard`, `ErrorView`, `EmptyState`, `LoadingIndicator` |
