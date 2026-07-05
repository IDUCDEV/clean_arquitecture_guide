# 06 — Modelado de Datos con OOP en Dart

> Saber manipular colecciones no basta. Necesitas **modelar bien los datos** desde el inicio. Este archivo cubre entidades, value objects, inmutabilidad y serialización.

---

## 🎯 Objetivos

- Diferenciar Entity de Value Object
- Implementar `copyWith`, `Equatable`, inmutabilidad
- Modelar con `factory` constructors y `fromJson`/`toJson`
- Usar sealed classes para uniones de tipos

---

## 1. Entity vs Value Object

| Aspecto | Entity | Value Object |
|---------|--------|-------------|
| **Identidad** | Tiene ID único | Se define por sus valores |
| **Mutabilidad** | Puede cambiar en el tiempo | Inmutable |
| **Comparación** | Por ID (`id == other.id`) | Por todos los campos (`props`) |
| **Ejemplo** | `Usuario`, `Rifa`, `Venta` | `Direccion`, `Dinero`, `RangoFecha` |

```dart
// ENTITY: tiene identidad
class Usuario {
  final String id;         // ← identidad
  final String nombre;
  final String email;
}

// VALUE OBJECT: se define por sus valores
class Dinero {
  final double cantidad;
  final String moneda;

  // Dos instancias con mismos valores son iguales
  // No hay ID, no hay identidad
}
```

---

## 2. Inmutabilidad con `copyWith`

```dart
class Rifa {
  final String id;
  final String nombre;
  final double precio;
  final String estado;     // 'activa', 'cancelada', 'finalizada'
  final DateTime creado;

  const Rifa({
    required this.id,
    required this.nombre,
    required this.precio,
    required this.estado,
    required this.creado,
  });

  Rifa copyWith({
    String? id,
    String? nombre,
    double? precio,
    String? estado,
    DateTime? creado,
  }) {
    return Rifa(
      id: id ?? this.id,
      nombre: nombre ?? this.nombre,
      precio: precio ?? this.precio,
      estado: estado ?? this.estado,
      creado: creado ?? this.creado,
    );
  }
}

// Uso:
final rifaActiva = Rifa(...);
final rifaCancelada = rifaActiva.copyWith(estado: 'cancelada');
// La original NO cambió (inmutabilidad)
```

> **💡 Regla**: Toda entidad debe tener `copyWith`. Cada vez que necesites "cambiar" un valor, crea una nueva instancia con `copyWith`.

---

## 3. `Equatable` — Comparación por Valor

```dart
import 'package:equatable/equatable.dart';

class Usuario extends Equatable {
  final String id;
  final String nombre;

  @override
  List<Object?> get props => [id, nombre];
}

// Ahora:
final a = Usuario(id: '1', nombre: 'Ana');
final b = Usuario(id: '1', nombre: 'Ana');
print(a == b); // true (sin Equatable sería false)
```

### Equatable en Entity vs Value Object

```dart
// Entity: comparar solo por ID
class Rifa extends Equatable {
  final String id;

  @override
  List<Object?> get props => [id]; // solo el ID
}

// Value Object: comparar por todos los campos
class Dinero extends Equatable {
  final double cantidad;
  final String moneda;

  @override
  List<Object?> get props => [cantidad, moneda]; // todos
}
```

---

## 4. Serialización: `fromJson` / `toJson`

### Factory constructor

```dart
class Rifa extends Equatable {
  final String id;
  final String nombre;
  final double precio;
  final String estado;
  final DateTime creado;

  const Rifa({
    required this.id,
    required this.nombre,
    required this.precio,
    required this.estado,
    required this.creado,
  });

  // 🔄 JSON → Objeto
  factory Rifa.fromJson(Map<String, dynamic> json) {
    return Rifa(
      id: json['id'] as String,
      nombre: json['nombre'] as String,
      precio: (json['precio'] as num).toDouble(),
      estado: json['estado'] as String,
      creado: DateTime.parse(json['creado'] as String),
    );
  }

  // 🔄 Objeto → JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre': nombre,
      'precio': precio,
      'estado': estado,
      'creado': creado.toIso8601String(),
    };
  }

  @override
  List<Object?> get props => [id, nombre, precio, estado];
}
```

### Manejo de nullables en fromJson

```dart
factory Usuario.fromJson(Map<String, dynamic> json) {
  return Usuario(
    id: json['id'] as String,
    nombre: json['nombre'] as String,
    email: json['email'] as String? ?? 'sin-email@test.com',  // nullable con default
    telefono: json['telefono'] as String?,                     // nullable opcional
    edad: json['edad'] is int ? json['edad'] as int : null,   // type check + nullable
  );
}
```

### Anidación

```dart
class Venta extends Equatable {
  final String id;
  final Rifa rifa;           // ← objeto anidado
  final Usuario comprador;   // ← objeto anidado
  final DateTime fecha;

  factory Venta.fromJson(Map<String, dynamic> json) {
    return Venta(
      id: json['id'] as String,
      rifa: Rifa.fromJson(json['rifa'] as Map<String, dynamic>),
      comprador: Usuario.fromJson(json['comprador'] as Map<String, dynamic>),
      fecha: DateTime.parse(json['fecha'] as String),
    );
  }
}
```

### Listas anidadas

```dart
factory ListadoRifas.fromJson(Map<String, dynamic> json) {
  return ListadoRifas(
    items: (json['items'] as List<dynamic>)
        .map((e) => Rifa.fromJson(e as Map<String, dynamic>))
        .toList(),
    total: json['total'] as int,
  );
}
```

---

## 5. Sealed Classes — Modelado de Estados

```dart
// 📌 Una rifa puede estar en varios estados
sealed class RifaEstado {}

class Activa extends RifaEstado {
  final DateTime fechaSorteo;
  Activa(this.fechaSorteo);
}

class Cancelada extends RifaEstado {
  final String motivo;
  Cancelada(this.motivo);
}

class Finalizada extends RifaEstado {
  final String? ganadorId;
  Finalizada({this.ganadorId});
}

// Uso con switch exhaustivo:
String mostrarEstado(RifaEstado estado) {
  return switch (estado) {
    Activa(fechaSorteo: var f) => 'Sorteo: ${f.toLocal()}',
    Cancelada(motivo: var m) => 'Cancelada: $m',
    Finalizada(ganadorId: var g) => g != null ? 'Ganó: $g' : 'Sin ganador',
  };
}
```

---

## 6. Composición vs Herencia

```dart
// ❌ HERENCIA incorrecta
class UsuarioConRol extends Usuario {
  final String rol;
}

// ✅ COMPOSICIÓN correcta
class Usuario {
  final String id;
  final String nombre;
}

class UsuarioConRol {
  final Usuario usuario;   // composición
  final String rol;

  // Delegación
  String get id => usuario.id;
  String get nombre => usuario.nombre;
}
```

---

## 🏋️ Mini-ejercicios

```dart
// 1. Modela una clase Sorteo con:
//    - id, premio, precio, fecha (DateTime), estado, ganadorId (nullable)
//    - copyWith, Equatable, fromJson, toJson

class Sorteo extends Equatable {
  final String id;
  final String premio;
  final double precio;
  final DateTime fecha;
  final String estado;
  final String? ganadorId;

  const Sorteo({
    required this.id,
    required this.premio,
    required this.precio,
    required this.fecha,
    required this.estado,
    this.ganadorId,
  });

  Sorteo copyWith({
    String? id,
    String? premio,
    double? precio,
    DateTime? fecha,
    String? estado,
    String? ganadorId,
  }) {
    return Sorteo(
      id: id ?? this.id,
      premio: premio ?? this.premio,
      precio: precio ?? this.precio,
      fecha: fecha ?? this.fecha,
      estado: estado ?? this.estado,
      ganadorId: ganadorId ?? this.ganadorId,
    );
  }

  factory Sorteo.fromJson(Map<String, dynamic> json) {
    return Sorteo(
      id: json['id'] as String,
      premio: json['premio'] as String,
      precio: (json['precio'] as num).toDouble(),
      fecha: DateTime.parse(json['fecha'] as String),
      estado: json['estado'] as String,
      ganadorId: json['ganador_id'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'premio': premio,
    'precio': precio,
    'fecha': fecha.toIso8601String(),
    'estado': estado,
    'ganador_id': ganadorId,
  };

  @override
  List<Object?> get props => [id, premio, precio, estado, ganadorId];
}

// 2. Convierte esta respuesta API en objetos:
final json = {
  'sorteos': [
    {'id': '1', 'premio': 'TV', 'precio': 10.0, 'fecha': '2026-07-15', 'estado': 'activa'},
    {'id': '2', 'premio': 'Laptop', 'precio': 25.0, 'fecha': '2026-08-01', 'estado': 'activa'},
  ],
  'total': 2,
};

final sorteos = (json['sorteos'] as List)
    .map((e) => Sorteo.fromJson(e as Map<String, dynamic>))
    .toList();
```

---

## ✅ Checklist

- [ ] Diferencio Entity (tiene ID) de Value Object (solo valores)
- [ ] Toda entidad tiene `copyWith`
- [ ] Uso `Equatable` con `props` adecuados
- [ ] Implemento `fromJson` con null safety
- [ ] Implemento `toJson` para serializar
- [ ] Uso sealed classes para estados finitos
- [ ] Prefiero composición sobre herencia

---

## 📚 Referencias

- [Dart | Language tour](https://dart.dev/language) — Recorrido completo por el lenguaje Dart
- [Dart | Collections](https://dart.dev/language/collections) — Documentación de List, Set, Map
- [Dart | Records y patterns](https://dart.dev/language/records) — Features modernos de Dart 3

---

**Siguiente**: [07-patrones-manipulacion.md](./07-patrones-manipulacion.md) — Patrones reales de manipulación
