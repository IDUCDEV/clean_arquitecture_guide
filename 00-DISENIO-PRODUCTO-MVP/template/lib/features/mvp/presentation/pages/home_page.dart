import 'package:flutter/material.dart';
import '../../../../theme/app_extensions.dart';
import '../../domain/entities/cancha.dart';
import '../../domain/usecases/obtener_canchas.dart';
import '../../data/datasources/cancha_local_datasource.dart';
import '../../data/repositories/cancha_repository_impl.dart';
import 'detalle_page.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  late final ObtenerCanchas _obtenerCanchas;
  List<Cancha> _canchas = [];

  @override
  void initState() {
    super.initState();
    final datasource = CanchaLocalDatasource();
    final repository = CanchaRepositoryImpl(datasource);
    _obtenerCanchas = ObtenerCanchas(repository);
    _cargarCanchas();
  }

  Future<void> _cargarCanchas() async {
    final canchas = await _obtenerCanchas(
      fecha: DateTime.now(),
      horaInicio: 17,
    );
    setState(() => _canchas = canchas);
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;
    final spacing = Theme.of(context).extension<AppSpacing>()!;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Reservar Cancha'),
        centerTitle: true,
      ),
      body: Padding(
        padding: EdgeInsets.all(spacing.md),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            SearchBar(
              hintText: 'Buscar canchas...',
              leading: const Icon(Icons.search),
              onSubmitted: (value) {},
            ),
            SizedBox(height: spacing.md),
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'hoy', label: Text('Hoy')),
                ButtonSegment(value: 'manana', label: Text('Mañana')),
                ButtonSegment(value: 'semana', label: Text('Semana')),
              ],
              selected: {'hoy'},
              onSelectionChanged: (_) {},
            ),
            SizedBox(height: spacing.lg),
            Text('Disponibles', style: textTheme.titleMedium),
            SizedBox(height: spacing.sm),
            Expanded(
              child: _canchas.isEmpty
                  ? const Center(child: CircularProgressIndicator())
                  : ListView.builder(
                      itemCount: _canchas.length,
                      itemBuilder: (context, index) {
                        final cancha = _canchas[index];
                        return Card(
                          margin: EdgeInsets.only(bottom: spacing.sm),
                          child: ListTile(
                            leading: CircleAvatar(
                              backgroundColor: colorScheme.primaryContainer,
                              child: Icon(
                                Icons.sports_tennis,
                                color: colorScheme.onPrimaryContainer,
                              ),
                            ),
                            title: Text(cancha.nombre),
                            subtitle: Text(cancha.club),
                            trailing: FilledTonalButton(
                              onPressed: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (_) => DetallePage(cancha: cancha),
                                  ),
                                );
                              },
                              child: Text('\$${cancha.precioPorHora.toStringAsFixed(0)}'),
                            ),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: 0,
        onDestinationSelected: (_) {},
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Inicio'),
          NavigationDestination(icon: Icon(Icons.search), label: 'Buscar'),
          NavigationDestination(icon: Icon(Icons.favorite_border), label: 'Favoritos'),
          NavigationDestination(icon: Icon(Icons.person_outline), label: 'Perfil'),
        ],
      ),
    );
  }
}
