import '../../domain/entities/cancha.dart';

class CanchaLocalDatasource {
  List<Cancha> getMockCanchas() {
    return const [
      Cancha(
        id: '1',
        nombre: 'Cancha de Tenis #1',
        club: 'Club Deportivo Central',
        precioPorHora: 15,
        disponible: true,
      ),
      Cancha(
        id: '2',
        nombre: 'Cancha de Tenis #2',
        club: 'Club Deportivo Central',
        precioPorHora: 18,
        disponible: true,
      ),
      Cancha(
        id: '3',
        nombre: 'Cancha Rápida',
        club: 'Polideportivo Municipal',
        precioPorHora: 20,
        disponible: false,
      ),
      Cancha(
        id: '4',
        nombre: 'Cancha de Arcilla',
        club: 'Tennis Club Elite',
        precioPorHora: 25,
        disponible: true,
      ),
    ];
  }
}
