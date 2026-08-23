# Design: add-elearning-progress

## Context
Dos capacidades en un feature folder. Búsqueda delegada al backend (RT001: full-text search con `websearch_to_tsquery`).

## Goals / Non-Goals
- Goals: gating hermético; progreso consistente (una sola fórmula)
- Non-Goals: pasarela de pagos real, certificados

## Decisions
### D1: Progreso calculado en SQL (vista) y espejado en entity
- Decisión: vista `course_progress` (SQL puro, fuente de verdad); la entity expone el mismo cálculo para UI optimista
- Por qué: RN004 vive en UN lugar; la UI no espera roundtrip para pintar %

### D2: Gating por RLS + validación de dominio
- Decisión: policy de lectura de lecciones exige inscripción activa; además el UseCase valida antes de navegar
- Por qué: defensa en profundidad — la RLS es la fuente de verdad (RN002)

### D3: RPC `enroll` atómico
- Decisión: valida RN001/RN006/RN007 dentro de una transacción
- Por qué: evita inscripciones duplicadas por doble tap

## Ficheros afectados (resumen)
| Elemento | Capa | Archivo |
|----------|------|---------|
| Course, Module, Lesson, Enrollment, LessonProgress | domain/entities | lib/features/elearning/domain/entities/ |
| CourseRepository, EnrollmentRepository | domain/repositories | … |
| GetCatalog, GetCourseDetail, Enroll, MarkLessonCompleted, RequestPublication, ApproveCourse… | domain/usecases | … |
| Models, RemoteDataSource, Impls | data | … |
| CatalogCubit, PlayerCubit (+states), InstructorCubit | presentation/cubit | … |
| CatalogPage, CourseDetailPage, LessonPlayerPage, MyCoursesPage | presentation/pages | … |
| Migración 0009 (tablas+RLS+vista+RPC) | supabase/migrations | … |

## Contratos Dart clave
```dart
abstract interface class EnrollmentRepository {
  Future<Either<Failure, Enrollment>> enroll({required String courseId});
  Future<Either<Failure, Unit>> markLessonCompleted({required String lessonId});
  Future<Either<Failure, CourseProgress>> getProgress({required String courseId});
}
sealed class PlayerState {}
class PlayerReady extends PlayerState { final Lesson lesson; final int progressPercent; const PlayerReady(this.lesson, this.progressPercent); }
class PlayerLocked extends PlayerState { final String message; const PlayerLocked(this.message); }
```

## Flujo de datos (marcar completada)
```
LessonPlayerPage ──► PlayerCubit.markCompleted()
      ▼
MarkLessonCompleted ──► EnrollmentRepositoryImpl ──► DataSource
      │ upsert lesson_progress (RS001 vía RLS)
      ▼
vista course_progress recalcula ──► Either.right(progress)
      ▼
PlayerReady(lesson, progress%) ──► si 100% → inscripción 'completada' (trigger)
```

## Backend Supabase
- Tablas: courses(+status enum), modules(orden), lessons(tipo, contenidoUrl check tipo='video'→url no nula), enrollments(estado), lesson_progress(unique student+lesson)
- Vista: course_progress(student_id, course_id, percent)
- RLS: lecciones legibles solo con enrollment activa; progreso owner-only; instructor edita solo lo suyo (RS002)
- Trigger: al cubrir 100% → enrollments.estado='completada'

## Boundaries
No integrar pasarela de pagos real en este cambio (MODIFIED futuro); no filtrar catálogo en cliente.
