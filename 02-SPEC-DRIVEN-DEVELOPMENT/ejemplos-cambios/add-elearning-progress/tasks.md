# Tasks: add-elearning-progress

## 1. Dominio
- [ ] 1.1 Entities: Course, Module, Lesson, Enrollment, LessonProgress
      Éxito: RN004 implementado como método puro con test de borde (0 lecciones)
- [ ] 1.2 Interfaces CourseRepository + EnrollmentRepository
- [ ] 1.3 UseCases ×8

## 2. Capa de datos + Backend Supabase
- [ ] 2.1 Migración 0009: tablas + checks (RN010) + vista progreso + RPC enroll + RLS
      Éxito: SELECT de lección sin inscripción devuelve vacío (test SQL)
- [ ] 2.2 Models roundtrip (enums de estado incluidos)
- [ ] 2.3 RemoteDataSource (búsqueda full-text vía rpc; stream no requerido)
- [ ] 2.4 RepositoryImpls

## 3. Estado y presentación
- [ ] 3.1 CatalogCubit/PlayerCubit/InstructorCubit + states sealed
      Éxito: PlayerLocked cuando no hay inscripción (mensaje exacto)
- [ ] 3.2 CatalogPage (paginación), CourseDetailPage, LessonPlayerPage, MyCoursesPage

## 4. Integración
- [ ] 4.1 DI + rutas con guard por rol

## 5. Tests
- [ ] 5.1 Unit: RN001/RN004/RN006 como failures; fórmula progreso bordes
- [ ] 5.2 SQL: gating RLS, trigger completada, RPC duplicados
- [ ] 5.3 Widget: player locked/ready, catálogo paginado

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 1.3, 2.1 | unit+SQL (duplicado, auto-inscripción) |
| REQ-002 | 1.3, 2.1 | SQL gating + cubit locked |
| REQ-003 | 1.1, 2.1 | unit fórmula + SQL trigger |
| REQ-004 | 1.3 | unit publicación y archivo |