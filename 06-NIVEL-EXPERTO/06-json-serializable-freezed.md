# Nivel Experto: json_serializable y Freezed

> La combinación de json_serializable + freezed elimina TODO el boilerplate de modelos: serialización, inmutabilidad, igualdad, copia, y pattern matching.

---

## 1. json_serializable: Serialización Automática

### 1.1 Configuración

```yaml
# pubspec.yaml
dependencies:
  json_annotation: ^4.9.0
  freezed_annotation: ^2.4.0

dev_dependencies:
  build_runner: ^2.4.8
  json_serializable: ^6.8.0
  freezed: ^2.5.0
```

```yaml
# build.yaml
targets:
  $default:
    builders:
      json_serializable:
        options:
          explicit_to_json: true
          field_rename: snake
          checked: true
```

### 1.2 Uso Básico

```dart
import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  final String id;
  final String name;
  final String email;
  final DateTime? createdAt;

  const User({
    required this.id,
    required this.name,
    required this.email,
    this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

**Genera:** `user.g.dart` con `_$UserFromJson` y `_$UserToJson`.

### 1.3 Anotaciones

```dart
@JsonSerializable()
class Product {
  // Campos con nombre distinto en JSON
  @JsonKey(name: 'product_id')
  final String id;

  // Ignorar campo
  @JsonKey(includeFromJson: false, includeToJson: false)
  final String? cacheOnly;

  // Valor por defecto si falta en JSON
  @JsonKey(defaultValue: 0)
  final int stock;

  // Campo requerido
  @JsonKey(required: true)
  final double price;

  // Ignorar si null
  @JsonKey(includeIfNull: false)
  final String? description;

  // Convertir entre tipos
  @JsonKey(fromJson: _dateFromJson, toJson: _dateToJson)
  final DateTime? updatedAt;

  const Product({...});

  factory Product.fromJson(Map<String, dynamic> json) => _$ProductFromJson(json);
  Map<String, dynamic> toJson() => _$ProductToJson(this);

  static DateTime? _dateFromJson(int? timestamp) =>
      timestamp != null ? DateTime.fromMillisecondsSinceEpoch(timestamp) : null;

  static int? _dateToJson(DateTime? date) => date?.millisecondsSinceEpoch;
}
```

### 1.4 Configuración Global vs Local

```dart
// Global (build.yaml): field_rename: snake
// Local (override):
@JsonSerializable(fieldRename: FieldRename.none)
class LocalModel {
  final String fullName; // en JSON: "fullName", no "full_name"
}
```

### 1.5 Enums con json_serializable

```dart
@JsonEnum(valueField: 'value')
enum Status {
  active('active'),
  inactive('inactive'),
  pending('pending');

  const Status(this.value);
  final String value;
}

@JsonSerializable()
class Order {
  final Status status;

  @JsonKey(name: 'order_date')
  final DateTime orderDate;

  const Order({required this.status, required this.orderDate});

  factory Order.fromJson(Map<String, dynamic> json) => _$OrderFromJson(json);
  Map<String, dynamic> toJson() => _$OrderToJson(this);
}
```

### 1.6 Anidación y Listas

```dart
@JsonSerializable()
class Category {
  final String id;
  final String name;
  final List<Product> products;  // Se serializa automáticamente

  const Category({...});
  factory Category.fromJson(Map<String, dynamic> json) => _$CategoryFromJson(json);
  Map<String, dynamic> toJson() => _$CategoryToJson(this);
}
```

### 1.7 Heredar Serialización

```dart
@JsonSerializable()
class BaseEntity {
  final String id;
  final DateTime createdAt;

  const BaseEntity({required this.id, required this.createdAt});
}

@JsonSerializable()
class ExtendedEntity extends BaseEntity {
  final String extraField;

  const ExtendedEntity({
    required super.id,
    required super.createdAt,
    required this.extraField,
  });

  factory ExtendedEntity.fromJson(Map<String, dynamic> json) =>
      _$ExtendedEntityFromJson(json);

  @override
  Map<String, dynamic> toJson() => _$ExtendedEntityToJson(this);
}
```

---

## 2. Freezed: Inmutabilidad y Data Classes

### 2.1 El Problema que Resuelve

```dart
// Sin freezed: 30+ líneas de boilerplate por clase
class User {
  final String id;
  final String name;

  const User({required this.id, required this.name});

  // copyWith
  User copyWith({String? id, String? name}) => User(
        id: id ?? this.id,
        name: name ?? this.name,
      );

  // == operator
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is User && runtimeType == other.runtimeType && id == other.id && name == other.name;

  @override
  int get hashCode => Object.hash(id, name);

  @override
  String toString() => 'User(id: $id, name: $name)';
}
```

```dart
// Con freezed: ~10 líneas
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
  }) = _User;
}
```

**Genera automáticamente:** `copyWith`, `==`, `hashCode`, `toString`, y más.

### 2.2 Instalación y Configuración

```yaml
# pubspec.yaml
dependencies:
  freezed_annotation: ^2.4.0
  json_annotation: ^4.9.0

dev_dependencies:
  build_runner: ^2.4.8
  freezed: ^2.5.0
  json_serializable: ^6.8.0
```

```yaml
# build.yaml
targets:
  $default:
    builders:
      freezed:
        options:
          union_key: type
          union_value_case: pascal
```

### 2.3 Uso Básico

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    @Default(0) int age,         // Valor por defecto
    String? email,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

**Lo que genera freezed:**

| Método | Generado | Ejemplo |
|--------|----------|---------|
| `copyWith` | ✅ | `user.copyWith(name: 'new')` |
| `==` / `hashCode` | ✅ | Comparación por valor |
| `toString` | ✅ | `User(id: 1, name: Test)` |
| Pattern matching | ✅ | `user.when(...)` / `user.map(...)` |
| Getters | ✅ | `user.name` |

### 2.4 Uniones Discriminadas (Sealed Unions)

El caso de uso más poderoso de freezed: modelar estados.

```dart
@freezed
class UserState with _$UserState {
  const factory UserState.initial() = Initial;
  const factory UserState.loading() = Loading;
  const factory UserState.loaded({
    required User user,
  }) = Loaded;
  const factory UserState.error(String message) = Error;
}
```

**Pattern matching exhaustivo:**

```dart
void handleState(UserState state) {
  state.when(
    initial: () => print('Esperando...'),
    loading: () => showSpinner(),
    loaded: (user) => showUser(user),
    error: (message) => showError(message),
    // El compilador OBLIGA a cubrir todos los casos
  );
}
```

`when` obliga a manejar TODOS los casos. Si agregas un nuevo estado, el compilador lanza error en cada `when`.

### 2.5 Patrones de Freezed

```dart
@freezed
class AsyncValue<T> with _$AsyncValue<T> {
  // Genéricos
  const factory AsyncValue.loading() = AsyncLoading<T>;
  const factory AsyncValue.data(T value) = AsyncData<T>;
  const factory AsyncValue.error(String message) = AsyncError<T>;
}

// Uso
final value = AsyncValue<int>.data(42);
final result = value.when(
  loading: () => null,
  data: (v) => v.toString(),
  error: (msg) => 'Error: $msg',
);
```

### 2.6 copyWith en Profundidad

```dart
@freezed
class Order with _$Order {
  const factory Order({
    required String id,
    required List<Item> items,
    String? notes,
  }) = _Order;
}

final order = Order(id: '1', items: [Item(name: 'A')]);

// Copy básico
order.copyWith(notes: 'Urgente');

// Copy anidado (con data classes anidadas)
order.copyWith.items([Item(name: 'B')]);

// Copy con transformación
order.copyWith(items: (items) => [...items, Item(name: 'C')]);
```

### 2.7 Métodos Personalizados

```dart
@freezed
class Product with _$Product {
  const factory Product({
    required String name,
    required double price,
    @Default(0) double discount,
  }) = _Product;

  const Product._(); // Constructor privado para métodos

  // Métodos de instancia
  double get finalPrice => price * (1 - discount / 100);

  // Getters
  bool get hasDiscount => discount > 0;
}
```

### 2.8 Freezed + json_serializable

```dart
@freezed
class ApiResponse<T> with _$ApiResponse<T> {
  const factory ApiResponse.success(T data) = ApiSuccess<T>;
  const factory ApiResponse.error({
    required int code,
    required String message,
  }) = ApiError<T>;

  factory ApiResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object?) fromJsonT,
  ) => _$ApiResponseFromJson(json, fromJsonT);
}
```

---

## 3. json_serializable + freezed + fpdart: Pipeline Completo

### 3.1 Modelo de Dominio

```dart
// domain/entities/user.dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    required String email,
  }) = _User;
}
```

### 3.2 Modelo de Datos (DTO)

```dart
// data/models/user_dto.dart
@freezed
class UserDto with _$UserDto {
  const factory UserDto({
    @JsonKey(name: 'user_id') required String id,
    @JsonKey(name: 'full_name') required String name,
    required String email,
  }) = _UserDto;

  factory UserDto.fromJson(Map<String, dynamic> json) =>
      _$UserDtoFromJson(json);

  factory UserDto.fromDomain(User user) => UserDto(
        id: user.id,
        name: user.name,
        email: user.email,
      );

  User toDomain() => User(
        id: id,
        name: name,
        email: email,
      );
}
```

### 3.3 Mapper Manual

```dart
// data/repositories/user_repository_impl.dart
@lazySingleton(as: UserRepository)
class UserRepositoryImpl implements UserRepository {
  final ApiClient apiClient;

  UserRepositoryImpl(this.apiClient);

  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final response = await apiClient.getUser(id);
      final user = response.toDomain(); // DTO -> Domain
      return Right(user);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
```

---

## 4. Buenas Prácticas

### 4.1 Separación DTO / Domain

```
lib/
├── features/
│   └── users/
│       ├── data/
│       │   ├── models/
│       │   │   ├── user_dto.dart       # freezed + json_serializable
│       │   │   └── user_dto.g.dart     # GENERADO
│       │   │   └── user_dto.freezed.dart # GENERADO
│       │   ├── datasources/
│       │   └── repositories/
│       └── domain/
│           ├── entities/
│           │   └── user.dart           # freezed (sin json)
│           ├── repositories/
│           └── usecases/
```

**Por qué separar:**
- Los DTOs cambian con la API, las entidades no
- La capa de dominio no debe depender de JSON
- Cada capa puede evolucionar independientemente

### 4.2 Evitar Anidación Excesiva

```dart
// ❌ Difícil de leer y mantener
@freezed
class ComplexResponse with _$ComplexResponse {
  const factory ComplexResponse({
    @Default([]) List<@Default([]) List<String>> matrix,
    Map<String, @Default(0) int>? counts,
  }) = _ComplexResponse;
}

// ✅ Separar en tipos concretos
@freezed
class MatrixRow with _$MatrixRow {
  const factory MatrixRow({
    @Default([]) List<String> values,
  }) = _MatrixRow;
}
```

### 4.3 Límites de Generación

```yaml
# build.yaml: evitar generar para tests y archivos específicos
targets:
  $default:
    builders:
      json_serializable:
        generate_for:
          - "lib/**"
        options:
          explicit_to_json: true
```

---

## 5. Conclusión

| Herramienta | Para qué | Alternativa sin codegen |
|-------------|----------|------------------------|
| **json_serializable** | Serialización JSON | Escribir fromJson/toJson manual |
| **freezed** | Data classes inmutables | copyWith/==/hashCode manual |
| **Ambos juntos** | Pipeline completo | ~100 líneas de boilerplate por clase |

**Regla de oro:** Si un modelo tiene 3+ campos, usa freezed + json_serializable. El tiempo que te ahorras en debugging de `==` y `copyWith` justifica la configuración inicial.

---

## Recursos Adicionales

- [json_serializable pub.dev](https://pub.dev/packages/json_serializable)
- [freezed pub.dev](https://pub.dev/packages/freezed)
- [Freezed Documentation](https://freezed.dev/docs)
- [JSON Serialization Guide](https://docs.flutter.dev/data-and-backend/serialization/json)
