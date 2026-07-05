# 10 — Ejercicios Avanzados (Nivel 3)

> 6 ejercicios integradores que combinan TODO lo aprendido: tipos, colecciones, métodos funcionales, maps, modelado y patrones. **Sin soluciones inline** — las soluciones están al final del documento.

---

## 🧠 Datos comunes

```dart
class Venta with EquatableMixin {
  final String id;
  final String rifaId;
  final String vendedorId;
  final String compradorNombre;
  final double monto;
  final DateTime fecha;
  final String metodoPago; // 'efectivo', 'transferencia', 'pago_movil'

  const Venta({
    required this.id,
    required this.rifaId,
    required this.vendedorId,
    required this.compradorNombre,
    required this.monto,
    required this.fecha,
    required this.metodoPago,
  });

  @override
  List<Object?> get props => [id];
}

class Vendedor with EquatableMixin {
  final String id;
  final String nombre;
  final String email;
  final bool activo;

  const Vendedor({
    required this.id,
    required this.nombre,
    required this.email,
    this.activo = true,
  });

  @override
  List<Object?> get props => [id];
}
```

```dart
final vendedores = [
  Vendedor(id: 'v1', nombre: 'Ana Pérez', email: 'ana@test.com'),
  Vendedor(id: 'v2', nombre: 'Bob García', email: 'bob@test.com', activo: false),
  Vendedor(id: 'v3', nombre: 'Carlos López', email: 'carlos@test.com'),
  Vendedor(id: 'v4', nombre: 'Diana Rojas', email: 'diana@test.com'),
];

final ventas = [
  Venta(id: 's1', rifaId: 'r1', vendedorId: 'v1', compradorNombre: 'Juan', monto: 10, fecha: DateTime(2026, 6, 1), metodoPago: 'efectivo'),
  Venta(id: 's2', rifaId: 'r2', vendedorId: 'v1', compradorNombre: 'María', monto: 25, fecha: DateTime(2026, 6, 2), metodoPago: 'transferencia'),
  Venta(id: 's3', rifaId: 'r1', vendedorId: 'v2', compradorNombre: 'Pedro', monto: 10, fecha: DateTime(2026, 6, 3), metodoPago: 'pago_movil'),
  Venta(id: 's4', rifaId: 'r3', vendedorId: 'v3', compradorNombre: 'Luis', monto: 15, fecha: DateTime(2026, 6, 4), metodoPago: 'efectivo'),
  Venta(id: 's5', rifaId: 'r2', vendedorId: 'v1', compradorNombre: 'Sofía', monto: 25, fecha: DateTime(2026, 6, 5), metodoPago: 'transferencia'),
  Venta(id: 's6', rifaId: 'r1', vendedorId: 'v3', compradorNombre: 'Elena', monto: 10, fecha: DateTime(2026, 6, 6), metodoPago: 'efectivo'),
  Venta(id: 's7', rifaId: 'r4', vendedorId: 'v4', compradorNombre: 'Diego', monto: 8, fecha: DateTime(2026, 6, 7), metodoPago: 'pago_movil'),
  Venta(id: 's8', rifaId: 'r2', vendedorId: 'v4', compradorNombre: 'Laura', monto: 25, fecha: DateTime(2026, 6, 8), metodoPago: 'transferencia'),
];
```

---

## Ejercicio 1: Reporte de ventas por vendedor

```dart
// Genera un reporte con:
//   - Nombre del vendedor
//   - Total vendido (suma de montos)
//   - Cantidad de ventas
//   - Método de pago más usado
//   - Si el vendedor está activo o no
// Ordenado por total vendido descendente.
// Usa los datos de vendedores para obtener el nombre.

// Ayuda: primero indexa vendedores por ID:
//   final vendedoresMap = {for (final v in vendedores) v.id: v};

class ReporteVendedor {
  final String nombre;
  final double totalVendido;
  final int cantidadVentas;
  final String metodoPagoFrecuente;
  final bool activo;
}

List<ReporteVendedor> generarReporte(List<Venta> ventas, List<Vendedor> vendedores) {
  // 👇 Tu implementación aquí
  final vendedoresMap = {for (final v in vendedores) v.id: v};

  final agrupado = ventas.fold<Map<String, List<Venta>>>(
    {}, (map, v) {
      map.putIfAbsent(v.vendedorId, () => []);
      map[v.vendedorId]!.add(v);
      return map;
    },
  );

  return agrupado.entries.map((entry) {
    final ventasVendedor = entry.value;
    final total = ventasVendedor.fold<double>(0, (acc, v) => acc + v.monto);

    final metodos = ventasVendedor.fold<Map<String, int>>({}, (map, v) {
      map[v.metodoPago] = (map[v.metodoPago] ?? 0) + 1;
      return map;
    });
    final metodoFrecuente = metodos.entries
        .reduce((a, b) => a.value > b.value ? a : b)
        .key;

    final vendedor = vendedoresMap[entry.key]!;
    return ReporteVendedor(
      nombre: vendedor.nombre,
      totalVendido: total,
      cantidadVentas: ventasVendedor.length,
      metodoPagoFrecuente: metodoFrecuente,
      activo: vendedor.activo,
    );
  }).toList()
    ..sort((a, b) => b.totalVendido.compareTo(a.totalVendido));
}
```

---

## Ejercicio 2: Detector de anomalías

```dart
// Detecta anomalías en las ventas:
// 1. Vendedores inactivos que tienen ventas (el sistema no debería permitirlo)
// 2. Ventas con monto que no coincide con el precio de la rifa (simulado: las rifas tienen precio fijo)
// 3. Vendedor con más ventas en un solo día

// Datos de rifas para validar precios:
final preciosRifas = {'r1': 10.0, 'r2': 25.0, 'r3': 15.0, 'r4': 8.0};

class Anomalia {
  final String tipo;     // 'vendedor_inactivo', 'monto_invalido', 'pico_diario'
  final String descripcion;
  final String? vendedorId;
}

List<Anomalia> detectarAnomalias(
    List<Venta> ventas, List<Vendedor> vendedores, Map<String, double> preciosRifas) {
  // 👇 Tu implementación aquí
  final anomalias = <Anomalia>[];
  final inactivos = vendedores.where((v) => !v.activo).map((v) => v.id).toSet();

  for (final venta in ventas) {
    if (inactivos.contains(venta.vendedorId)) {
      anomalias.add(Anomalia(
        tipo: 'vendedor_inactivo',
        descripcion: 'Venta ${venta.id} hecha por vendedor inactivo ${venta.vendedorId}',
        vendedorId: venta.vendedorId,
      ));
    }

    final precioEsperado = preciosRifas[venta.rifaId];
    if (precioEsperado != null && venta.monto != precioEsperado) {
      anomalias.add(Anomalia(
        tipo: 'monto_invalido',
        descripcion: 'Venta ${venta.id}: monto ${venta.monto} ≠ precio esperado $precioEsperado',
        vendedorId: venta.vendedorId,
      ));
    }
  }

  // Pico diario: agrupar ventas por vendedor + fecha
  final ventasPorDia = ventas.fold<Map<String, int>>({}, (map, v) {
    final key = '${v.vendedorId}_${v.fecha.toIso8601String().substring(0, 10)}';
    map[key] = (map[key] ?? 0) + 1;
    return map;
  });

  if (ventasPorDia.isNotEmpty) {
    final maxEntry = ventasPorDia.entries.reduce((a, b) => a.value > b.value ? a : b);
    anomalias.add(Anomalia(
      tipo: 'pico_diario',
      descripcion: '${maxEntry.value} ventas en un día (${maxEntry.key})',
      vendedorId: maxEntry.key.split('_').first,
    ));
  }

  return anomalias;
}
```

---

## Ejercicio 3: Mini-cache con MRU (Most Recently Used)

```dart
// Implementa un caché con límite de tamaño que elimina el elemento
// menos recientemente accedido cuando se alcanza el límite.

class MRUCache<K, V> {
  final int maxSize;
  final _cache = <K, V>{};
  final _accesos = <K, DateTime>{};

  MRUCache(this.maxSize);

  void put(K key, V value) {
    if (_cache.length >= maxSize && !_cache.containsKey(key)) {
      // Eliminar el menos reciente
      final masViejo = _accesos.entries
          .reduce((a, b) => a.value.isBefore(b.value) ? a : b)
          .key;
      _cache.remove(masViejo);
      _accesos.remove(masViejo);
    }
    _cache[key] = value;
    _accesos[key] = DateTime.now();
  }

  V? get(K key) {
    if (_cache.containsKey(key)) {
      _accesos[key] = DateTime.now();
      return _cache[key];
    }
    return null;
  }
}

// Test:
final cache = MRUCache<String, int>(3);
cache.put('a', 1);
cache.put('b', 2);
cache.put('c', 3);
cache.get('a'); // accede a 'a'
cache.put('d', 4); // 'b' debería ser eliminado (el menos reciente)
print(cache.get('b')); // null
print(cache.get('d')); // 4
```

---

## Ejercicio 4: Transformador de respuestas API

```dart
// La API de Supabase devuelve datos anidados. Debes transformarlos
// a un modelo plano para la UI.

final apiResponse = {
  'data': [
    {
      'id': 's1',
      'monto': 10.0,
      'creado': '2026-06-01T10:00:00Z',
      'rifa': {'id': 'r1', 'nombre': 'TV 55"', 'premio': 'Televisor 55 pulgadas'},
      'vendedor': {'id': 'v1', 'nombre': 'Ana Pérez'},
    },
    {
      'id': 's2',
      'monto': 25.0,
      'creado': '2026-06-02T14:30:00Z',
      'rifa': {'id': 'r2', 'nombre': 'Laptop', 'premio': 'Laptop gaming'},
      'vendedor': {'id': 'v2', 'nombre': 'Bob García'},
    },
  ],
  'total': 2,
};

class VentaUI {
  final String id;
  final double monto;
  final String montoFormateado;
  final String rifaNombre;
  final String premio;
  final String vendedorNombre;
  final String fechaFormateada;

  VentaUI({
    required this.id,
    required this.monto,
    required this.rifaNombre,
    required this.premio,
    required this.vendedorNombre,
    required this.fechaFormateada,
  }) : montoFormateado = '\$${monto.toStringAsFixed(2)}';
}

List<VentaUI> transformarAPI(Map<String, dynamic> response) {
  return (response['data'] as List).map((item) {
    final rifa = item['rifa'] as Map<String, dynamic>;
    final vendedor = item['vendedor'] as Map<String, dynamic>;
    final fecha = DateTime.parse(item['creado'] as String);

    return VentaUI(
      id: item['id'] as String,
      monto: (item['monto'] as num).toDouble(),
      rifaNombre: rifa['nombre'] as String,
      premio: rifa['premio'] as String,
      vendedorNombre: vendedor['nombre'] as String,
      fechaFormateada: '${fecha.day}/${fecha.month}/${fecha.year}',
    );
  }).toList();
}
```

---

## Ejercicio 5: Calculadora de comisiones

```dart
// Calcula comisiones para vendedores:
// - Cada vendedor gana 10% del total vendido
// - Bono: si vendió >5 veces en el mes, +5% extra
// - Penalización: si tuvo anomalías (ventas con monto incorrecto), -2%
// Devuelve un Map con: vendedorId → {nombre, comision, ventas, bonoAplicado}

final preciosRifas = {'r1': 10.0, 'r2': 25.0, 'r3': 15.0, 'r4': 8.0};

Map<String, Map<String, dynamic>> calcularComisiones(
    List<Venta> ventas, List<Vendedor> vendedores, Map<String, double> precios) {
  final vendedoresMap = {for (final v in vendedores) v.id: v};

  return ventas.fold<Map<String, Map<String, dynamic>>>(
    {}, (map, v) {
      map.putIfAbsent(v.vendedorId, () => {
        'nombre': vendedoresMap[v.vendedorId]!.nombre,
        'totalVendido': 0.0,
        'cantidadVentas': 0,
        'anomalias': 0,
      });

      final data = map[v.vendedorId]!;
      data['totalVendido'] = (data['totalVendido'] as double) + v.monto;
      data['cantidadVentas'] = (data['cantidadVentas'] as int) + 1;

      if (precios[v.rifaId] != v.monto) {
        data['anomalias'] = (data['anomalias'] as int) + 1;
      }

      return map;
    },
  ).map((id, data) {
    double porcentaje = 0.10; // 10% base
    if ((data['cantidadVentas'] as int) > 5) porcentaje += 0.05;
    if ((data['anomalias'] as int) > 0) porcentaje -= 0.02;

    return MapEntry(id, {
      'nombre': data['nombre'],
      'comision': ((data['totalVendido'] as double) * porcentaje),
      'ventas': data['cantidadVentas'],
      'porcentaje': porcentaje,
    });
  });
}
```

---

## Ejercicio 6: Mini-pipeline ETL

```dice
// Escribe un pipeline completo que:
// 1. Filtra solo ventas del mes actual (junio 2026)
// 2. Agrupa por vendedor
// 3. Calcula total, promedio, y cantidad
// 4. Indexa con el nombre del vendedor (no el ID)
// 5. Ordena por total descendente
// 6. Devuelve top 3

// Resultado esperado:
// [
//   {nombre: 'Ana Pérez', total: 60.0, promedio: 20.0, cantidad: 3},
//   {nombre: 'Diana Rojas', total: 33.0, promedio: 16.5, cantidad: 2},
//   {nombre: 'Carlos López', total: 25.0, promedio: 12.5, cantidad: 2},
// ]

List<Map<String, dynamic>> topVendedoresDelMes(List<Venta> ventas, List<Vendedor> vendedores) {
  final vendedoresMap = {for (final v in vendedores) v.id: v.nombre};

  final delMes = ventas.where((v) =>
    v.fecha.month == 6 && v.fecha.year == 2026
  ).toList();

  final agrupado = delMes.fold<Map<String, List<Venta>>>(
    {}, (map, v) {
      map.putIfAbsent(v.vendedorId, () => []);
      map[v.vendedorId]!.add(v);
      return map;
    },
  );

  final reportes = agrupado.entries.map((e) {
    final ventas = e.value;
    final total = ventas.fold<double>(0, (acc, v) => acc + v.monto);
    return {
      'nombre': vendedoresMap[e.key] ?? 'Desconocido',
      'total': total,
      'promedio': total / ventas.length,
      'cantidad': ventas.length,
    };
  }).toList()
    ..sort((a, b) => (b['total'] as double).compareTo(a['total'] as double));

  return reportes.take(3).toList();
}
```

---

## 📚 Referencias

- [Dart | Language tour](https://dart.dev/language) — Recorrido completo por el lenguaje Dart
- [Dart | Collections](https://dart.dev/language/collections) — Documentación de List, Set, Map
- [Dart | Records y patterns](https://dart.dev/language/records) — Features modernos de Dart 3

---

## 🏁 Fin del módulo

🎉 **Completaste los 25+ ejercicios.** Ya no necesitas que la IA escriba tu lógica de manipulación de datos. Pasa a [11-recursos-practica.md](./11-recursos-practica.md) para seguir mejorando.
