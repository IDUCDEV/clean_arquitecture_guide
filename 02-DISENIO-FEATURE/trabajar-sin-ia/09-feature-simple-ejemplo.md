# Feature Simple: CRUD de Notas

> Ejemplo paso a paso de cómo implementar una feature simple (CRUD) usando el framework de 6 fases, sin depender de IA.

---

## Contexto

**Feature:** Gestión de notas personales (crear, leer, actualizar, eliminar)
**Complejidad:** Simple
**Tiempo estimado:** 2-3 horas

---

## FASE 1: Investigar (30 min)

### User Story

```
**Como** usuario de la app,
**quiero** crear, ver, editar y eliminar notas,
**para** organizar mis pensamientos y tareas diarias.
```

### Investigación de herramientas

```markdown
## Investigación: CRUD de Notas con Supabase

### Qué necesito
- Supabase para almacenamiento en la nube
- Tabla `notas` en PostgreSQL
- Operaciones CRUD básicas

### Documentación relevante
- Supabase Flutter: https://supabase.com/docs/guides/getting-started/quickstarts/flutter
- Tablas: https://supabase.com/docs/guides/database/tables
- CRUD: https://supabase.com/docs/guides/database

### Dependencias del proyecto
- supabase_flutter (ya instalado)
- go_router (ya instalado)

### Criterios de aceptación
- [ ] Puedo crear una nota con título y contenido
- [ ] Puedo ver todas mis notas en una lista
- [ ] Puedo editar una nota existente
- [ ] Puedo eliminar una nota con confirmación
- [ ] Las notas se guardan en Supabase
- [ ] Manejo errores de red

### Complejidad: Simple
- CRUD básico con Supabase
- Sin lógica de negocio compleja
- Sin estados complejos
```

---

## FASE 2: Diseñar (30 min)

### Descomposición (FADER)

| Paso | Qué hago | Resultado |
|------|----------|-----------|
| **F**ormular | Feature ya definida en User Story | ✅ |
| **A**ctorizar | Un actor: usuario autenticado | ✅ |
| **D**escomponer | 4 operaciones: crear, listar, actualizar, eliminar | ✅ |
| **E**ntidades | Una entidad: Nota | ✅ |
| **R**eglas | Título requerido, máximo 200 caracteres, contenido opcional | ✅ |

### Entidad

```dart
// lib/domain/entities/nota.dart

class Nota {
  final String id;
  final String titulo;
  final String contenido;
  final DateTime fechaCreacion;
  final DateTime fechaActualizacion;

  const Nota({
    required this.id,
    required this.titulo,
    required this.contenido,
    required this.fechaCreacion,
    required this.fechaActualizacion,
  });
}
```

### Contrato (Repository)

```dart
// lib/domain/repositories/nota_repository.dart

abstract class NotaRepository {
  Future<Either<Failure, List<Nota>>> obtenerNotas();
  Future<Either<Failure, Nota>> crearNota({required String titulo, String contenido = ''});
  Future<Either<Failure, Nota>> actualizarNota({required String id, String? titulo, String? contenido});
  Future<Either<Failure, void>> eliminarNota({required String id});
}
```

### Modelo (Data Layer)

```dart
// lib/data/models/nota_model.dart

class NotaModel extends Nota {
  NotaModel({
    required super.id,
    required super.titulo,
    required super.contenido,
    required super.fechaCreacion,
    required super.fechaActualizacion,
  });

  factory NotaModel.fromJson(Map<String, dynamic> json) {
    return NotaModel(
      id: json['id'] as String,
      titulo: json['titulo'] as String,
      contenido: json['contenido'] as String? ?? '',
      fechaCreacion: DateTime.parse(json['fecha_creacion'] as String),
      fechaActualizacion: DateTime.parse(json['fecha_actualizacion'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'titulo': titulo,
      'contenido': contenido,
      'fecha_creacion': fechaCreacion.toIso8601String(),
      'fecha_actualizacion': fechaActualizacion.toIso8601String(),
    };
  }
}
```

### Flujo de datos

```
Crear nota:
UI (Formulario) → Controller → UseCase → Repository → Supabase

Listar notas:
Supabase → Repository → UseCase → Controller → UI (Lista)

Actualizar nota:
UI (Formulario) → Controller → UseCase → Repository → Supabase

Eliminar nota:
UI (Confirmación) → Controller → UseCase → Repository → Supabase
```

### Estados

```dart
enum NotasStatus { inicial, cargando, exito, error }
```

### Excepciones a manejar

| Excepción | Cuándo ocurre | Qué mostrar |
|-----------|---------------|-------------|
| Sin conexión | No hay internet | "Sin conexión. Intenta más tarde." |
| Título vacío | Usuario no escribe título | "El título es requerido" |
| Error Supabase | Problema en el servidor | "Error al guardar. Intenta de nuevo." |

---

## FASE 3: Implementar (1.5-2 horas)

### Orden de implementación

```
1. Dominio
   └── nota.dart (entidad)

2. Dominio
   └── nota_repository.dart (contrato)

3. Dominio
   └── crear_nota.dart (use case)
   └── obtener_notas.dart (use case)
   └── actualizar_nota.dart (use case)
   └── eliminar_nota.dart (use case)

4. Data
   └── nota_model.dart (modelo)
   └── nota_repository_impl.dart (implementación)

5. Presentation
   └── notas_controller.dart (estado)
   └── notas_page.dart (UI lista)
   └── nota_form_page.dart (UI formulario)
```

### Implementación paso a paso

**Paso 1: Entidad**
```dart
// lib/domain/entities/nota.dart

class Nota {
  final String id;
  final String titulo;
  final String contenido;
  final DateTime fechaCreacion;
  final DateTime fechaActualizacion;

  const Nota({
    required this.id,
    required this.titulo,
    required this.contenido,
    required this.fechaCreacion,
    required this.fechaActualizacion,
  });

  // Valida que el título no esté vacío
  bool get esValido => titulo.trim().isNotEmpty && titulo.length <= 200;
}
```

**Paso 2: Contrato**
```dart
// lib/domain/repositories/nota_repository.dart

abstract class NotaRepository {
  Future<Either<Failure, List<Nota>>> obtenerNotas();
  Future<Either<Failure, Nota>> crearNota({
    required String titulo,
    String contenido = '',
  });
  Future<Either<Failure, Nota>> actualizarNota({
    required String id,
    String? titulo,
    String? contenido,
  });
  Future<Either<Failure, void>> eliminarNota({required String id});
}
```

**Paso 3: Use Cases**
```dart
// lib/domain/usecases/notas/crear_nota.dart

class CrearNota {
  final NotaRepository repository;

  CrearNota(this.repository);

  Future<Either<Failure, Nota>> call({
    required String titulo,
    String contenido = '',
  }) async {
    // Validación de negocio
    if (titulo.trim().isEmpty) {
      return const Left(ValidationFailure('El título es requerido'));
    }
    if (titulo.length > 200) {
      return const Left(ValidationFailure('El título no puede exceder 200 caracteres'));
    }

    return await repository.crearNota(titulo: titulo.trim(), contenido: contenido);
  }
}
```

**Paso 4: Modelo**
```dart
// lib/data/models/nota_model.dart

class NotaModel extends Nota {
  NotaModel({
    required super.id,
    required super.titulo,
    required super.contenido,
    required super.fechaCreacion,
    required super.fechaActualizacion,
  });

  factory NotaModel.fromJson(Map<String, dynamic> json) {
    return NotaModel(
      id: json['id'] as String,
      titulo: json['titulo'] as String,
      contenido: json['contenido'] as String? ?? '',
      fechaCreacion: DateTime.parse(json['fecha_creacion'] as String),
      fechaActualizacion: DateTime.parse(json['fecha_actualizacion'] as String),
    );
  }

  Map<String, dynamic> toSupabase() {
    return {
      'titulo': titulo,
      'contenido': contenido,
    };
  }
}
```

**Paso 5: Repositorio Implementación**
```dart
// lib/data/repositories/nota_repository_impl.dart

class NotaRepositoryImpl implements NotaRepository {
  final SupabaseClient client;

  NotaRepositoryImpl(this.client);

  @override
  Future<Either<Failure, List<Nota>>> obtenerNotas() async {
    try {
      final response = await client
          .from('notas')
          .select()
          .order('fecha_actualizacion', ascending: false);

      final notas = (response as List)
          .map((json) => NotaModel.fromJson(json))
          .toList();

      return Right(notas);
    } catch (e) {
      return Left(ServerFailure('Error al obtener notas'));
    }
  }

  @override
  Future<Either<Failure, Nota>> crearNota({
    required String titulo,
    String contenido = '',
  }) async {
    try {
      final response = await client
          .from('notas')
          .insert({'titulo': titulo, 'contenido': contenido})
          .select()
          .single();

      return Right(NotaModel.fromJson(response));
    } catch (e) {
      return Left(ServerFailure('Error al crear nota'));
    }
  }

  @override
  Future<Either<Failure, Nota>> actualizarNota({
    required String id,
    String? titulo,
    String? contenido,
  }) async {
    try {
      final updates = <String, dynamic>{
        'fecha_actualizacion': DateTime.now().toIso8601String(),
      };
      if (titulo != null) updates['titulo'] = titulo;
      if (contenido != null) updates['contenido'] = contenido;

      final response = await client
          .from('notas')
          .update(updates)
          .eq('id', id)
          .select()
          .single();

      return Right(NotaModel.fromJson(response));
    } catch (e) {
      return Left(ServerFailure('Error al actualizar nota'));
    }
  }

  @override
  Future<Either<Failure, void>> eliminarNota({required String id}) async {
    try {
      await client.from('notas').delete().eq('id', id);
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure('Error al eliminar nota'));
    }
  }
}
```

**Paso 6: Controller**
```dart
// lib/presentation/controllers/notas_controller.dart

class NotasController extends ChangeNotifier {
  final CrearNota _crearNota;
  final ObtenerNotas _obtenerNotas;
  final ActualizarNota _actualizarNota;
  final EliminarNota _eliminarNota;

  NotasStatus _status = NotasStatus.inicial;
  List<Nota> _notas = [];
  String? _error;

  NotasStatus get status => _status;
  List<Nota> get notas => _notas;
  String? get error => _error;

  Future<void> cargarNotas() async {
    _status = NotasStatus.cargando;
    notifyListeners();

    final result = await _obtenerNotas();

    result.fold(
      (failure) {
        _status = NotasStatus.error;
        _error = failure.message;
      },
      (notas) {
        _notas = notas;
        _status = NotasStatus.exito;
      },
    );
    notifyListeners();
  }

  Future<bool> crearNota(String titulo, {String contenido = ''}) async {
    _status = NotasStatus.cargando;
    notifyListeners();

    final result = await _crearNota(titulo: titulo, contenido: contenido);

    return result.fold(
      (failure) {
        _status = NotasStatus.error;
        _error = failure.message;
        notifyListeners();
        return false;
      },
      (nota) {
        _notas.insert(0, nota);
        _status = NotasStatus.exito;
        notifyListeners();
        return true;
      },
    );
  }

  // ... métodos similares para actualizar y eliminar
}
```

---

## FASE 4: Verificar (30 min)

### Tests unitarios

```dart
// test/domain/usecases/notas/crear_nota_test.dart

void main() {
  test('Crear nota válida', () async {
    // Arrange
    final repository = MockNotaRepository();
    final useCase = CrearNota(repository);

    when(repository.crearNota(titulo: 'Test', contenido: ' contenido'))
        .thenAnswer((_) async => Right(Nota(...)));

    // Act
    final result = await useCase(titulo: 'Test', contenido: ' contenido');

    // Assert
    expect(result.isRight(), true);
  });

  test('Rechazar nota sin título', () async {
    final useCase = CrearNota(MockNotaRepository());
    final result = await useCase(titulo: '');
    expect(result.isLeft(), true);
  });

  test('Rechazar título mayor a 200 caracteres', () async {
    final useCase = CrearNota(MockNotaRepository());
    final result = await useCase(titulo: 'x' * 201);
    expect(result.isLeft(), true);
  });
}
```

### Prueba manual

```
1. Crear nota → Aparece en la lista
2. Editar nota → Cambios se guardan
3. Eliminar nota → Se elimina con confirmación
4. Sin conexión → Muestra error
5. Título vacío → Muestra validación
```

---

## FASE 5: Refactor (15 min)

### Verificaciones

- [ ] Nombres descriptivos en todas las funciones
- [ ] Código duplicado eliminado
- [ ] Cada clase tiene una responsabilidad
- [ ] Tests siguen pasando

---

## FASE 6: Validar con IA (10 min)

### Prompt

```
Revisa mi implementación de CRUD de notas con Supabase.
¿El manejo de errores está completo? ¿Falta algún caso edge?
¿Los nombres son claros? NO reescribas el código, solo dame feedback.
```

### Qué buscar en la respuesta de IA

- ¿Detecta problemas que tú no viste?
- ¿Su feedback es específico y accionable?
- ¿Algo de lo que dice no entiendes? → No lo implementes hasta entenderlo

---

## Tiempo total: 2.5-3 horas

| Fase | Tiempo |
|------|--------|
| Investigar | 30 min |
| Diseñar | 30 min |
| Implementar | 1.5-2 horas |
| Verificar | 30 min |
| Refactor | 15 min |
| Validar | 10 min |

---

**Siguiente:** [10-feature-intermedia-ejemplo.md](./10-feature-intermedia-ejemplo.md) — Feature intermedia: Sistema de notificaciones push
