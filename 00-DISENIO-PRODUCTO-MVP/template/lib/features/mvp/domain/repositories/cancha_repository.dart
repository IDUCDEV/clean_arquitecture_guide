import '../entities/cancha.dart';

abstract class CanchaRepository {
  Future<List<Cancha>> obtenerDisponibles({
    required DateTime fecha,
    required int horaInicio,
  });
}
