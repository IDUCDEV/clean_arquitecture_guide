import '../entities/cancha.dart';
import '../repositories/cancha_repository.dart';

class ObtenerCanchas {
  final CanchaRepository _repository;

  ObtenerCanchas(this._repository);

  Future<List<Cancha>> call({required DateTime fecha, required int horaInicio}) {
    return _repository.obtenerDisponibles(fecha: fecha, horaInicio: horaInicio);
  }
}
