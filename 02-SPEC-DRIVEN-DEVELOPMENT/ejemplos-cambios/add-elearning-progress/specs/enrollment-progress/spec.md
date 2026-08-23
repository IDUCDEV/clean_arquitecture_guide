# Spec: enrollment-progress

## WHY
El estudiante necesita acceso controlado al contenido y visibilidad de su avance.

## Purpose
Gating estricto de lecciones por inscripción y progreso calculado de forma única y consistente.

## ADDED Requirements

### Requirement: Inscribirse a un curso (REQ-001)
#### Scenario: Primera inscripción
- **WHEN** el estudiante se inscribe a un curso publicado
- **THEN** se crea inscripción `activa` (y requiere pagoId si el curso es pago — RN007)

#### Scenario: Ya inscrito
- **IF** existe inscripción activa previa
- **THEN** el sistema DEBERÁ mostrar "Ya estás inscrito en este curso" (RN001)

#### Scenario: Auto-inscripción del instructor
- **IF** el instructor intenta inscribirse a su propio curso
- **THEN** el sistema DEBERÁ rechazarlo (RN006)

### Requirement: Gating de contenido (REQ-002)
#### Scenario: Lección con inscripción activa
- **MIENTRAS** la inscripción esté `activa`
- **EL SISTEMA DEBERÁ** permitir leer/ver las lecciones del curso

#### Scenario: Sin inscripción
- **IF** no hay inscripción activa
- **THEN** el sistema DEBERÁ ocultar el contenido y ofrecer el botón de inscripción (RN002, RLS)

### Requirement: Progreso (REQ-003)
#### Scenario: Marcar lección completada
- **WHEN** el estudiante marca una lección como completada
- **THEN** el progreso DEBERÁ recalcularse = (completadas / total) × 100 (RN004)

#### Scenario: Curso completado
- **WHEN** todas las lecciones quedan completadas
- **THEN** la inscripción DEBERÁ pasar a estado `completada` (RN005)

#### Scenario: Progreso privado
- **ENTONCES** cada estudiante SOLO lee su propio progreso (RS001)

### Requirement: Publicación editorial (REQ-004)
#### Scenario: Solicitar publicación sin lecciones
- **IF** el curso no tiene ≥1 lección
- **THEN** el sistema DEBERÁ mostrar "El curso necesita al menos una lección" (RN003)

#### Scenario: Aprobación admin
- **WHEN** el admin aprueba
- **THEN** el curso pasa a `publicado`; solo el claim role='admin' puede hacerlo (RN008)

#### Scenario: Eliminar con estudiantes
- **IF** hay inscripciones activas
- **THEN** solo se permite archivar, no eliminar (RN009)
