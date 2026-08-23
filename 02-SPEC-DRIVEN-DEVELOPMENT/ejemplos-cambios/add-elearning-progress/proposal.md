# Proposal: add-elearning-progress

> Deriva del caso "Plataforma de Cursos Online". Ejemplo Intermedia→Compleja: dos capacidades (catálogo/inscripción + progreso).

## Impacto (Impact Report)
- Features afectadas: ninguna; feature nueva `elearning`
- Reutilizable: patrón CRUD, auth con claims de rol
- Supabase: tablas `courses`, `modules`, `lessons`, `enrollments`, `lesson_progress`; RLS por inscripción
- DI / rutas: +3 cubits (catálogo, player, instructor), +4 páginas
- Riesgos: fuga de contenido no inscrito (RN002); cálculo de progreso inconsistente

## Why (Problema)
No existe forma de distribuir contenido educativo estructurado ni medir avance de estudiantes.

## What Changes (Solución)
Catálogo con búsqueda backend, inscripción (gratuita/paga), lecciones gated por inscripción, progreso calculado y auto-completado del curso, flujo editorial borrador→revisión→publicado.

## Capabilities
### New Capabilities
- `course-catalog`: exploración y administración de cursos
- `enrollment-progress`: inscripción, gating de contenido y progreso

## Scope (Alcance)
**Incluye:** catálogo paginado con búsqueda full-text backend, CRUD instructor, aprobación admin, inscribirse, ver/marcar lecciones, progreso %, auto-estado completada.
**No incluye:** pagos reales (solo flag pagoId), certificados, comentarios.
**Dependencias:** autenticación con roles.
**Suposiciones:** videos alojados externamente (Vimeo/YouTube).
**Preguntas abiertas:** ~~¿reinscripción tras completar?~~ → NO en v1.

## Actores y permisos
| Actor | Puede | No puede | Mapeo RLS |
|-------|-------|----------|-----------|
| Estudiante | Explorar, inscribirse, leer lecciones inscritas, SU progreso | Ver lecciones sin inscripción | progreso: `auth.uid() = student_id` |
| Instructor | CRUD SUS cursos/lecciones, reportes | Publicar (solo solicitar) | `instructor_id = auth.uid()` |
| Admin | Aprobar/rechazar publicación | Editar contenido ajeno | claim role |
| Pagos (ext.) | Confirmar pago | — | webhook |

## Impact
- Código: ~18 ficheros en `lib/features/elearning/`
- Datos: 5 tablas; RPC `enroll` atómico; vista `course_progress`
- Breaking changes: ninguno
