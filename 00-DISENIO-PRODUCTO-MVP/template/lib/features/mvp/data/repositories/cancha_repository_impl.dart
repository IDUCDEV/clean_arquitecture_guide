import '../../domain/entities/cancha.dart';
import '../../domain/repositories/cancha_repository.dart';
import '../datasources/cancha_local_datasource.dart';

class CanchaRepositoryImpl implements CanchaRepository {
  final CanchaLocalDatasource _datasource;

  CanchaRepositoryImpl(this._datasource);

  @override
  Future<List<Cancha>> obtenerDisponibles({
    required DateTime fecha,
    required int horaInicio,
  }) async {
    final canchas = _datasource.getMockCanchas();
    return canchas.where((c) => c.disponible).toList();
  }
}
