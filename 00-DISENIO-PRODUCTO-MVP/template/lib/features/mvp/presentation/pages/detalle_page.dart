import 'package:flutter/material.dart';
import '../../domain/entities/cancha.dart';
import 'confirmacion_page.dart';

class DetallePage extends StatelessWidget {
  final Cancha cancha;

  const DetallePage({super.key, required this.cancha});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final textTheme = Theme.of(context).textTheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Detalle'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        CircleAvatar(
                          backgroundColor: colorScheme.primaryContainer,
                          child: Icon(
                            Icons.sports_tennis,
                            color: colorScheme.onPrimaryContainer,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(cancha.nombre, style: textTheme.titleLarge),
                            Text(cancha.club, style: textTheme.bodyMedium),
                          ],
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    const Divider(),
                    ListTile(
                      leading: const Icon(Icons.calendar_today),
                      title: const Text('Fecha'),
                      subtitle: const Text('15 de Julio, 2026'),
                    ),
                    ListTile(
                      leading: const Icon(Icons.access_time),
                      title: const Text('Hora'),
                      subtitle: const Text('5:00 PM'),
                    ),
                    ListTile(
                      leading: const Icon(Icons.attach_money),
                      title: const Text('Precio'),
                      subtitle: Text('\$${cancha.precioPorHora.toStringAsFixed(0)} / hora'),
                    ),
                  ],
                ),
              ),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => const ConfirmacionPage(),
                    ),
                  );
                },
                child: const Text('Reservar y pagar'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
