# Caso Práctico: Plataforma de Cursos Online (E-Learning)

> Aplica FADER + Mapeo + Contratos + Flujo para diseñar una plataforma de cursos online desde cero.

---

## Enunciado

Somos el equipo técnico de una startup de tecnología educativa. El equipo de producto nos pide:

> Los estudiantes deben poder explorar un catálogo de cursos, inscribirse a un curso, ver el contenido (lecciones en video y texto), y marcar lecciones como completadas para trackear su progreso. Los instructores deben poder crear y editar cursos con múltiples lecciones, y ver reportes de avance de sus estudiantes. Los administradores deben poder gestionar usuarios (estudiantes e instructores) y aprobar cursos antes de publicarlos.

---

## Instrucciones

1. Trabaja en papel y lápiz. No abras el editor de código.
2. Sigue cada sección en orden.
3. Al final, compara con la solución sugerida.

---

## Sección 1: FADER

### ✏️ Paso 1: Formular

Escribe al menos 3 enunciados "Como [actor], quiero [acción] para [valor]".

**Pregúntate:**
- ¿Un curso es un solo video o una serie de lecciones?
- ¿El progreso se calcula sobre lecciones completadas o tiempo visto?
- ¿Qué diferencia hay entre "inscribirse" y "comprar" un curso?
- ¿Los cursos tienen fecha de inicio o son auto-gestionados?

### ✏️ Paso 2: Actorizar

Identifica todos los actores y sus permisos:

| Actor | Tipo | ¿Qué puede hacer? | ¿Qué NO puede hacer? |
|-------|------|-------------------|----------------------|
| Estudiante | Primario | | |
| Instructor | Secundario | | |
| Admin | Secundario | | |
| Sistema de pagos | Externo | | |
| ? | ? | | |

**Pregúntate:**
- ¿Un instructor también puede ser estudiante de otros cursos?
- ¿El admin puede editar contenido de cursos o solo aprobarlos?
- ¿Hay actores invitados (usuarios sin cuenta que ven contenido gratuito)?

### ✏️ Paso 3: Descomponer

Enumera todas las operaciones atómicas clasificadas en CRUD, Validación, Cálculo, Transición.

**Considera:**
- Catálogo de cursos (búsqueda, filtros, categorías)
- Inscripción (gratuita vs paga)
- Consumo de contenido (video, texto)
- Progreso (qué lecciones completó, porcentaje del curso)
- Creación de cursos (estructura: curso → módulos → lecciones)
- Aprobación de cursos (borrador → pendiente → publicado)
- Reportes de avance

**Identifica dependencias:**
- ¿Qué debe existir antes de inscribirse?
- ¿Qué debe pasar antes de marcar una lección como completada?
- ¿Qué condiciones habilitan la publicación de un curso?

### ✏️ Paso 4: Entidades

Define las entidades de negocio con sus atributos esenciales.

**Posibles entidades:**
- `Curso` (Course)
- `Lección` (Lesson)
- `Módulo` (Module)
- `Estudiante` (Student)
- `Instructor` (Instructor)
- `Inscripción` (Enrollment)
- `ProgresoLección` (LessonProgress)
- `Categoría` (Category)

**Pregúntate:**
- ¿`Curso` contiene `Lección` directamente o hay `Módulo` como nivel intermedio?
- ¿`Progreso` es una entidad separada o un atributo de `Inscripción`?
- ¿`Instructor` es un tipo de `Usuario` o una entidad distinta?
- ¿El precio del curso está en `Curso` o en una entidad separada de pricing?

### ✏️ Paso 5: Reglas

Enuncia al menos 8 reglas de negocio con formato R001, R002...

**Áreas a cubrir:**
- Inscripción: ¿puede inscribirse a un curso ya completado?
- Contenido: ¿qué pasa si un curso no tiene lecciones publicadas?
- Progreso: ¿cómo se calcula el porcentaje de avance?
- Publicación: ¿qué condiciones debe cumplir un curso para ser publicado?
- Acceso: ¿un estudiante ve todo el contenido al inscribirse o se libera por módulos?
- Eliminación: ¿se puede eliminar un curso con estudiantes inscritos?

---

## Sección 2: Mapeo a Capas

### ✏️ Paso 1: Estructura DOMAIN

Dibuja el árbol de `domain/`:

```
domain/
├── entities/
│   ├── course.dart
│   ├── module.dart
│   ├── lesson.dart
│   ├── enrollment.dart
│   ├── lesson_progress.dart
│   ├── user.dart
│   └── category.dart
├── usecases/
│   ├── browse_courses.dart
│   ├── enroll_course.dart
│   ├── watch_lesson.dart
│   ├── complete_lesson.dart
│   ├── get_progress.dart
│   ├── create_course.dart
│   ├── publish_course.dart
│   └── approve_course.dart
├── repositories/
│   ├── course_repository.dart
│   ├── enrollment_repository.dart
│   └── user_repository.dart
└── core/
    └── failures.dart
```

**Pregúntate:**
- ¿`complete_lesson` y `watch_lesson` son el mismo UseCase?
- ¿`publish_course` es un UseCase o parte de `update_course`?
- ¿Necesitas un `enrollment_repository` separado o va dentro de `course_repository`?

### ✏️ Paso 2: Estructura DATA

Dibuja el árbol de `data/`:

```
data/
├── datasources/
│   ├── course_remote_data_source.dart
│   ├── course_local_data_source.dart
│   ├── enrollment_remote_data_source.dart
│   └── progress_data_source.dart
├── models/
│   ├── course_model.dart
│   ├── lesson_model.dart
│   ├── enrollment_model.dart
│   └── user_model.dart
└── repositories/
    ├── course_repository_impl.dart
    ├── enrollment_repository_impl.dart
    └── user_repository_impl.dart
```

### ✏️ Paso 3: Estructura PRESENTATION

Dibuja el árbol de `presentation/`:

```
presentation/
├── cubit/
│   ├── catalog_cubit.dart
│   ├── catalog_state.dart
│   ├── course_detail_cubit.dart
│   ├── player_cubit.dart
│   ├── student_progress_cubit.dart
│   └── instructor_courses_cubit.dart
├── pages/
│   ├── catalog_page.dart
│   ├── course_detail_page.dart
│   ├── lesson_player_page.dart
│   └── instructor_dashboard_page.dart
└── widgets/
    ├── course_card.dart
    ├── lesson_list.dart
    ├── progress_bar.dart
    └── video_player_widget.dart
```

**Pregúntate:**
- ¿Cuántos Cubits necesitas realmente? ¿Puedes combinar algunos?
- ¿El player de video es un widget reutilizable o una página completa?
- ¿El dashboard del instructor usa los mismos UseCases que la vista del estudiante?

---

## Sección 3: Contratos

### ✏️ Paso 1: Contrato CourseRepository

```dart
abstract class CourseRepository {
  // ¿Qué métodos necesita el dominio de cursos?
  // ¿Cómo se buscan cursos? ¿Por categoría, por instructor, por texto libre?
  // ¿Cómo se obtiene el detalle de un curso con sus lecciones?
  // ¿Qué failures puede producir?
}
```

### ✏️ Paso 2: Contrato EnrollmentRepository

```dart
abstract class EnrollmentRepository {
  // Inscribir estudiante
  // Obtener cursos de un estudiante
  // Obtener estudiantes de un curso
  // Validar si ya está inscrito
}
```

### ✏️ Paso 3: Contrato de DataSource Remoto

```dart
abstract class CourseRemoteDataSource {
  // Operaciones CRUD vs API
  // Paginación del catálogo
  // Búsqueda y filtros
}
```

### ✏️ Paso 4: Estados de UI

Diseña los estados para al menos `CatalogCubit` y `PlayerCubit`.

**Pregúntate:**
- El catálogo tiene búsqueda y filtros — ¿cómo modelas eso en el estado?
- El player de video tiene estados: cargando, reproduciendo, pausado, error — ¿cómo los representas?
- ¿El progreso del estudiante se actualiza en tiempo real o al recargar?

### ✏️ Paso 5: ADR

Escribe al menos un ADR. Ejemplos de decisiones a documentar:
- ¿El progreso se calcula por lecciones completadas o por tiempo visto?
- ¿Los cursos se almacenan como un árbol (curso → módulos → lecciones) en un solo documento o como colecciones separadas?
- ¿La búsqueda de cursos se hace en el backend o se cachea localmente?

---

## Sección 4: Flujo de Datos

### ✏️ Paso 1: Flujo Inscribirse a Curso

Dibuja la secuencia completa desde que el estudiante hace clic en "Inscribirse" hasta que ve el curso en "Mis Cursos".

**Incluye:**
- Validaciones (¿ya está inscrito? ¿el curso está publicado? ¿hay costo?)
- Transformaciones entre capas
- Actualización del estado del Cubit
- Manejo de errores (pago rechazado, curso lleno, etc.)

### ✏️ Paso 2: Flujo Completar Lección y Actualizar Progreso

Dibuja la secuencia desde que el estudiante termina un video hasta que ve su porcentaje de avance actualizado.

**Pregúntate:**
- ¿El progreso se calcula en el frontend o en el backend?
- ¿Qué pasa si el estudiante recarga la página sin internet?
- ¿El progreso se guarda automáticamente o requiere acción manual?

### ✏️ Paso 3: Flujo Publicar Curso (Instructor → Admin → Público)

Dibuja la máquina de estados de un curso: Borrador → En revisión → Publicado → Archivado.

**Incluye:**
- ¿Quién puede hacer cada transición?
- ¿Qué validaciones se ejecutan al solicitar publicación?
- ¿Qué pasa cuando se publica? (notificaciones, acceso a estudiantes, etc.)

---

## Solución Sugerida

> ⚠️ Resuelve cada sección en papel primero. La solución sugerida es para comparar después.

### ✅ FADER Completo

```
╔═══════════════════════════════════════════════════════════════╗
║  FEATURE: Plataforma de Cursos Online (E-Learning)          ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [F]ormular:                                                  ║
║  F1: Como estudiante, quiero explorar cursos e               ║
║      inscribirme para aprender a mi ritmo.                   ║
║  F2: Como instructor, quiero crear cursos con lecciones      ║
║      para compartir mi conocimiento.                         ║
║  F3: Como administrador, quiero aprobar cursos antes         ║
║      de publicarlos para garantizar calidad.                  ║
║                                                               ║
║  [A]ctorizar:                                                 ║
║  1. Estudiante (primario)                                    ║
║     - Explorar catálogo, inscribirse, ver lecciones,         ║
║       marcar completadas, ver progreso                        ║
║  2. Instructor (secundario)                                  ║
║     - CRUD cursos y lecciones, ver reportes de estudiantes   ║
║  3. Admin (secundario)                                       ║
║     - Gestionar usuarios, aprobar/rechazar cursos            ║
║  4. Sistema de Pagos (externo)                               ║
║     - Cobrar inscripción en cursos pagos                     ║
║  5. Sistema de Videos (externo)                              ║
║     - Alojar y servir videos (Vimeo, YouTube, etc.)          ║
║                                                               ║
║  [D]escomponer:                                               ║
║  Estudiante:                                                  ║
║  - [R] Explorar catálogo (búsqueda, filtros, paginación)    ║
║  - [R] Ver detalle del curso                                  ║
║  - [C] Inscribirse a curso (gratuito o pago)                 ║
║  - [R] Ver lecciones del curso                                ║
║  - [U] Marcar lección como completada                         ║
║  - [R] Ver progreso general                                   ║
║  - [R] Ver listado "Mis Cursos"                              ║
║                                                               ║
║  Instructor:                                                  ║
║  - [C] Crear curso                                            ║
║  - [U] Editar curso (contenido, precio, imagen)              ║
║  - [C] Agregar módulos y lecciones                            ║
║  - [U] Reordenar lecciones                                    ║
║  - [U] Solicitar publicación                                  ║
║  - [R] Ver reporte de estudiantes por curso                  ║
║                                                               ║
║  Admin:                                                       ║
║  - [R] Ver cursos pendientes de aprobación                   ║
║  - [U] Aprobar curso                                          ║
║  - [U] Rechazar curso (con motivo)                            ║
║  - [CRUD] Gestionar usuarios                                  ║
║                                                               ║
║  Sistema:                                                     ║
║  - [Validación] Validar contenido mínimo antes de publicar   ║
║  - [Validación] Verificar que el estudiante no esté inscrito ║
║  - [Cálculo] Calcular progreso (% lecciones completadas)     ║
║  - [Transición] Notificar al instructor al inscribirse       ║
║    un estudiante                                              ║
║                                                               ║
║  [E]ntidades:                                                 ║
║  Curso: id, titulo, descripcion, precio, imagenUrl,          ║
║        estado (borrador, revisión, publicado, archivado),     ║
║        categoriaId, instructorId, fechaCreacion               ║
║  Modulo: id, cursoId, titulo, orden                           ║
║  Leccion: id, moduloId, titulo, tipo (video/texto),          ║
║           contenidoUrl, duracionMinutos, orden                 ║
║  Inscripcion: id, estudianteId, cursoId, fecha,              ║
║               estado (activa, completada, cancelada),         ║
║               pagoId (nullable)                                ║
║  ProgresoLeccion: id, estudianteId, leccionId,               ║
║                   completada, fechaCompletado                  ║
║  Usuario: id, nombre, email, rol (estudiante, instructor,    ║
║           admin), fotoUrl                                     ║
║  Categoria: id, nombre, slug, icono                           ║
║                                                               ║
║  [R]eglas:                                                    ║
║  R001: No se puede inscribir a un curso ya inscrito          ║
║  R002: Solo se pueden ver lecciones de cursos inscritos      ║
║  R003: Un curso debe tener al menos 1 lección para           ║
║        solicitar publicación                                  ║
║  R004: El progreso = (lecciones completadas / total          ║
║        lecciones) * 100                                       ║
║  R005: Al completar todas las lecciones, la inscripción      ║
║        pasa a estado "completada"                             ║
║  R006: Un instructor no puede inscribirse a su propio curso  ║
║  R007: Los cursos pagos requieren confirmación de pago       ║
║        antes de activar la inscripción                        ║
║  R008: Solo el admin puede cambiar el estado a "publicado"   ║
║  R009: No se puede eliminar un curso con estudiantes         ║
║        inscritos (solo archivarlo)                            ║
║  R010: Las lecciones de tipo "video" requieren contenidoUrl  ║
║        no vacío                                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### ✅ Contrato CourseRepository

```dart
abstract class CourseRepository {
  Future<Either<Failure, List<Course>>> getCatalog({
    required int page,
    int? categoryId,
    String? searchQuery,
  });

  Future<Either<Failure, Course>> getCourseDetail(String courseId);

  Future<Either<Failure, Course>> createCourse(CreateCourseParams params);

  Future<Either<Failure, Course>> updateCourse(
    String courseId, UpdateCourseParams params);

  Future<Either<Failure, Course>> requestPublication(String courseId);

  Future<Either<Failure, Course>> approveCourse(String courseId);

  Future<Either<Failure, Course>> rejectCourse(
    String courseId, String reason);

  Future<Either<Failure, List<Course>>> getCoursesByInstructor(
    String instructorId);

  Future<Either<Failure, List<Course>>> getCoursesByStudent(
    String studentId);

  Future<Either<Failure, Module>> addModule(String courseId, Module module);

  Future<Either<Failure, Lesson>> addLesson(
    String moduleId, Lesson lesson);

  Future<Either<Failure, void>> reorderLessons(
    String moduleId, List<String> lessonIds);
}
```

### ✅ Contrato EnrollmentRepository

```dart
abstract class EnrollmentRepository {
  Future<Either<Failure, Enrollment>> enroll(
    String studentId, String courseId, String? paymentId);

  Future<Either<Failure, List<Enrollment>>> getStudentEnrollments(
    String studentId);

  Future<Either<Failure, bool>> isEnrolled(
    String studentId, String courseId);

  Future<Either<Failure, List<Student>>> getCourseStudents(
    String courseId);

  Future<Either<Failure, void>> markLessonCompleted(
    String studentId, String lessonId);

  Future<Either<Failure, double>> getProgress(
    String studentId, String courseId);

  Future<Either<Failure, List<LessonProgress>>> getLessonProgress(
    String studentId, String courseId);
}
```

### ✅ Estados del PlayerCubit

```dart
sealed class PlayerState {}

final class PlayerLoading extends PlayerState {
  final String lessonId;
}

final class PlayerReady extends PlayerState {
  final Lesson lesson;
  final bool isCompleted;
  final double courseProgress;
}

final class PlayerPlaying extends PlayerState {
  final Lesson lesson;
  final Duration position;
  final double courseProgress;
}

final class PlayerPaused extends PlayerState {
  final Lesson lesson;
  final Duration position;
  final double courseProgress;
}

final class PlayerError extends PlayerState {
  final String message;
  final String lessonId;
}

final class PlayerCompleted extends PlayerState {
  final Lesson lesson;
  final double courseProgress;
}
```

### ✅ ADR Sugerido

```markdown
# ADR-004: Cálculo de Progreso del Estudiante

## Contexto
Necesitamos mostrar al estudiante su avance en cada curso.

## Decisión
El progreso se calculará como:
  (lecciones_completadas / total_lecciones_del_curso) × 100

El cálculo se hará en el backend (Supabase) y se cacheará localmente.
Cada vez que se completa una lección, se recalcula y persiste.

## Consecuencias
Positivas:
- Simple y predecible para el estudiante
- Fácil de testear
- El frontend solo lee, no calcula

Negativas:
- No considera tiempo de visualización de video
- Una lección de 1 minuto cuenta igual que una de 30 minutos

## Alternativas consideradas
1. Progreso por minutos vistos / duración total:
   Descartado: más complejo, requiere tracking de posición de video,
   inconsistente si el estudiante adelanta el video.
2. Progreso calculado en frontend:
   Descartado: inconsistente entre dispositivos, se pierde al cerrar sesión.
```

### ✅ Flujo Completar Lección

```
ESTUDIANTE    → Termina de ver video o hace clic en "Completar"
WIDGET        → onCompleted() → playerCubit.markCompleted(lessonId)
CUBIT         → emit(PlayerCompleted(lesson, progress))
USECASE       → CompleteLesson.call(studentId, lessonId)
REPO IMPL     → 1. progressDS.markCompleted(studentId, lessonId)
                 2. progressDS.getProgress(studentId, courseId)
                 3. enrollmentDS.enrollment.completed =
                      (progress == 100.0) ? "completada" : "activa"
CUBIT         → fold()
                  → éxito: emit(PlayerReady(lesson, isCompleted: true,
                      courseProgress: newProgress))
                  → error: emite error pero mantiene lección completada
                    localmente (optimista)

ESTUDIANTE    → Ve su progreso actualizado en la barra de avance
```

---

## 🚀 Siguiente paso

Continúa con el [Sistema de Facturación](./05c-caso-facturacion.md) para practicar con máquinas de estado complejas.

---

**Tiempo estimado:** 2-3 horas  
**Material:** Papel y lápiz
