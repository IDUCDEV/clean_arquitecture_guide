# 07 — Patrones Reales de Manipulación de Datos

> Este archivo reúne los patrones de manipulación que usarás **todos los días** en una app Flutter con Supabase. Cada patrón es un caso real del dominio de rifas/gestión.

---

## 🎯 Objetivos

- Aplicar todo lo aprendido en patrones del mundo real
- Diseñar pipelines de datos completos
- Implementar transformaciones comunes en apps Flutter

---

## Patrón 1: API Response → Entities (fetch → filter → transform)

```dart
// Supabase devuelve JSON, necesitas entidades limpias
Future<List<Rifa>> obtenerRifasActivas() async {
  final response = await supabase.from('rifas').select('*');

  final rifas = (response as List)
      .map((json) => Rifa.fromJson(json as Map<String, dynamic>))
      .where((r) => r.estado == 'activa')
      .toList()
    ..sort((a, b) => b.creado.compareTo(a.creado)); // más recientes primero

  return rifas;
}
```

### Pipeline completo con filtros

```dart
class FiltroRifas {
  final String? busqueda;
  final double? precioMin;
  final double? precioMax;
  final String? estado;
  final String? ordenarPor;  // 'fecha', 'precio', 'nombre'
  final bool ascendente;

  List<Rifa> aplicar(List<Rifa> rifas) {
    var resultado = rifas;

    // Filtrar por búsqueda textual
    if (busqueda != null && busqueda!.isNotEmpty) {
      resultado = resultado
          .where((r) =>
              r.nombre.toLowerCase().contains(busqueda!.toLowerCase()))
          .toList();
    }

    // Filtrar por rango de precios
    if (precioMin != null) {
      resultado = resultado.where((r) => r.precio >= precioMin!).toList();
    }
    if (precioMax != null) {
      resultado = resultado.where((r) => r.precio <= precioMax!).toList();
    }

    // Filtrar por estado
    if (estado != null && estado!.isNotEmpty) {
      resultado = resultado.where((r) => r.estado == estado).toList();
    }

    // Ordenar
    resultado.sort((a, b) {
      int cmp;
      switch (ordenarPor) {
        case 'precio':
          cmp = a.precio.compareTo(b.precio);
        case 'nombre':
          cmp = a.nombre.compareTo(b.nombre);
        default: // 'fecha'
          cmp = a.creado.compareTo(b.creado);
      }
      return ascendente ? cmp : -cmp;
    });

    return resultado;
  }
}
```

---

## Patrón 2: Agrupar y Contar (Dashboard)

```dart
class DashboardData {
  final Map<String, int> rifasPorEstado;
  final double totalVendido;
  final int usuariosActivos;
  final List<_TopVenta> topVentas;
}

DashboardData calcularDashboard(List<Rifa> rifas, List<Venta> ventas) {
  // Rifas agrupadas por estado
  final porEstado = rifas.fold<Map<String, int>>({}, (map, r) {
    map[r.estado] = (map[r.estado] ?? 0) + 1;
    return map;
  });

  // Total vendido
  final total = ventas.fold<double>(0, (acc, v) => acc + v.monto);

  // Top 5 rifas más vendidas
  final ventasPorRifa = ventas.fold<Map<String, double>>({}, (map, v) {
    map[v.rifaId] = (map[v.rifaId] ?? 0) + v.monto;
    return map;
  });

  final topVentas = ventasPorRifa.entries
      .toList()
    ..sort((a, b) => b.value.compareTo(a.value));

  return DashboardData(
    rifasPorEstado: porEstado,
    totalVendido: total,
    usuariosActivos: 0, // calcular de otra fuente
    topVentas: topVentas.take(5).map((e) => _TopVenta(e.key, e.value)).toList(),
  );
}
```

---

## Patrón 3: Merge Local + Remoto (Cache)

```dart
class RifaRepository {
  final RifaRemoteDataSource remote;
  final RifaLocalDataSource local;

  Future<List<Rifa>> obtenerRifas() async {
    // 1. Obtener datos locales primero (rápido)
    final locales = await local.obtenerTodas();

    // 2. Obtener datos remotos (lento)
    final remotas = await remote.obtenerTodas();

    // 3. Merge: únirlas por ID, ganan las remotas
    final mapaLocal = {
      for (final r in locales)
        r.id: r,
    };

    for (final r in remotas) {
      mapaLocal[r.id] = r; // remoto sobrescribe local
    }

    // 4. Guardar actualización en local
    final mergeadas = mapaLocal.values.toList();
    await local.guardarTodas(mergeadas);

    return mergeadas;
  }
}
```

---

## Patrón 4: Transformar para UI

```dart
// Los datos vienen planos, la UI necesita estructura

// Datos planos de Supabase:
final rows = await supabase.from('ventas').select('''
  id, monto, creado,
  rifa:rifa_id (nombre, premio),
  vendedor:vendedor_id (nombre)
''');

// Transformar a modelo anidado para UI:
class VentaUI {
  final String id;
  final double monto;
  final String rifaNombre;
  final String premio;
  final String vendedorNombre;
  final DateTime fecha;

  // Vista formateada
  String get montoFormateado => '\$${monto.toStringAsFixed(2)}';
  String get fechaFormateada => '${fecha.day}/${fecha.month}/${fecha.year}';
}

final ventasUI = (rows as List).map((row) {
  final rifa = row['rifa'] as Map<String, dynamic>;
  final vendedor = row['vendedor'] as Map<String, dynamic>;
  return VentaUI(
    id: row['id'] as String,
    monto: (row['monto'] as num).toDouble(),
    rifaNombre: rifa['nombre'] as String,
    premio: rifa['premio'] as String,
    vendedorNombre: vendedor['nombre'] as String,
    fecha: DateTime.parse(row['creado'] as String),
  );
}).toList();
```

---

## Patrón 5: Búsqueda y Autocomplete

```dart
List<Rifa> buscarRifas(List<Rifa> rifas, String query) {
  if (query.isEmpty) return rifas;

  final q = query.toLowerCase();
  return rifas.where((r) {
    return r.nombre.toLowerCase().contains(q) ||
        r.premio.toLowerCase().contains(q) ||
        r.id.contains(q);
  }).toList();
}

// Con debounce (para search en tiempo real):
class SearchController {
  String? _lastQuery;
  Timer? _debounce;

  void onSearchChanged(String query, Function(String) onResult) {
    _debounce?.cancel();
    _debounce = Timer(const Duration(milliseconds: 300), () {
      if (query != _lastQuery) {
        _lastQuery = query;
        onResult(query);
      }
    });
  }
}
```

---

## Patrón 6: Paginación + Filtros (Cursor-based)

```dart
class CursorPagination {
  final List<Rifa> items;
  final String? nextCursor;  // null = no hay más páginas
}

Future<CursorPagination> obtenerRifasPaginadas({
  String? cursor,
  int limit = 20,
  String? estado,
}) async {
  var query = supabase
      .from('rifas')
      .select('*')
      .limit(limit)
      .order('creado', ascending: false);

  if (cursor != null) {
    query = query.lt('creado', cursor); // before cursor
  }
  if (estado != null) {
    query = query.eq('estado', estado);
  }

  final response = await query;

  final rifas = (response as List)
      .map((j) => Rifa.fromJson(j as Map<String, dynamic>))
      .toList();

  final nextCursor = rifas.length == limit
      ? rifas.last.creado.toIso8601String()
      : null;

  return CursorPagination(items: rifas, nextCursor: nextCursor);
}
```

---

## Patrón 7: Validación de Formularios

```dart
class FormError {
  final String campo;
  final String mensaje;
}

List<FormError> validarRifaForm({
  required String nombre,
  required double precio,
  required DateTime fechaSorteo,
}) {
  final errores = <FormError>[];

  if (nombre.isEmpty) {
    errores.add(FormError('nombre', 'El nombre es obligatorio'));
  }

  if (precio <= 0) {
    errores.add(FormError('precio', 'El precio debe ser mayor a 0'));
  }

  if (fechaSorteo.isBefore(DateTime.now())) {
    errores.add(FormError('fecha', 'La fecha debe ser futura'));
  }

  return errores;
}

// Uso:
final errores = validarRifaForm(nombre: '', precio: -5, fechaSorteo: DateTime.now().subtract(Duration(days: 1)));

final esValido = errores.isEmpty; // false
final camposInvalidos = errores.map((e) => e.campo).toList(); // ['nombre', 'precio', 'fecha']
```

---

## 🏋️ Mini-ejercicio: Pipeline completo

```dart
// DATOS: simula una respuesta de Supabase
final jsonResponse = [
  {'id': '1', 'nombre': 'Rifa TV', 'precio': 10.0, 'estado': 'activa', 'creado': '2026-06-01', 'categoria': 'electronica'},
  {'id': '2', 'nombre': 'Rifa Laptop', 'precio': 25.0, 'estado': 'activa', 'creado': '2026-06-15', 'categoria': 'electronica'},
  {'id': '3', 'nombre': 'Rifa GiftCard', 'precio': 5.0, 'estado': 'cancelada', 'creado': '2026-05-01', 'categoria': 'regalos'},
  {'id': '4', 'nombre': 'Rifa Bici', 'precio': 15.0, 'estado': 'activa', 'creado': '2026-06-20', 'categoria': 'deportes'},
  {'id': '5', 'nombre': 'Rifa Reloj', 'precio': 8.0, 'estado': 'finalizada', 'creado': '2026-04-10', 'categoria': 'accesorios'},
];

// IMPLEMENTA:
// 1. Convertir a objetos Rifa
// SOLUCIÓN:
final rifas = jsonResponse.map((j) => Rifa.fromJson(j)).toList();

// 2. Filtrar solo activas, ordenadas por fecha (más reciente)
final activas = rifas
    .where((r) => r.estado == 'activa')
    .toList()
  ..sort((a, b) => b.creado.compareTo(a.creado));

// 3. Agrupar por categoría y contar
final porCategoria = rifas.fold<Map<String, int>>({}, (map, r) {
  map[r.categoria] = (map[r.categoria] ?? 0) + 1;
  return map;
});

// 4. Precio promedio de las rifas activas
final activasList = rifas.where((r) => r.estado == 'activa').toList();
final promedio = activasList.isEmpty
    ? 0.0
    : activasList.fold(0.0, (acc, r) => acc + r.precio) / activasList.length;
```

---

## ✅ Checklist

- [ ] Domino el pipeline fetch → filter → transform → aggregate
- [ ] Implemento `FiltroRifas` como clase reutilizable
- [ ] Hago merge de datos local + remoto por ID
- [ ] Transformo datos planos de API a modelos para UI
- [ ] Implemento búsqueda con debounce
- [ ] Uso cursor-based pagination
- [ ] Separo validación de formularios en funciones puras

---

## 📚 Referencias

- [Dart | Language tour](https://dart.dev/language) — Recorrido completo por el lenguaje Dart
- [Dart | Collections](https://dart.dev/language/collections) — Documentación de List, Set, Map
- [Dart | Records y patterns](https://dart.dev/language/records) — Features modernos de Dart 3

---

**Siguiente**: [08-ejercicios-basicos.md](./08-ejercicios-basicos.md) — 10 ejercicios básicos para practicar
