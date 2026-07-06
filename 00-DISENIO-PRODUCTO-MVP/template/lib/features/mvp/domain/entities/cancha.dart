class Cancha {
  final String id;
  final String nombre;
  final String club;
  final double precioPorHora;
  final bool disponible;
  final String imagenUrl;

  const Cancha({
    required this.id,
    required this.nombre,
    required this.club,
    required this.precioPorHora,
    required this.disponible,
    this.imagenUrl = '',
  });
}
