# Tasks: add-elearning-progress

## 1. Dominio y datos base
- [ ] 1.1 Entities: Course, Module, Lesson, Enrollment, LessonProgress
      Éxito: RN004 implementado como método puro con test de borde (0 lecciones)
- [ ] 1.2 Interfaces CourseRepository + EnrollmentRepository
- [ ] 1.3 Migración 0009: tablas + checks (RN010) + vista progreso + RPC enroll + RLS
      Éxito: SELECT de lección sin inscripción devuelve vacío (test SQL)

## 2. Capa de datos
- [ ] 2.1 Models roundtrip (enums de estado incluidos)
- [ ] 2.2 RemoteDataSource (búsqueda full-text vía rpc; stream no requerido)
- [ ] 2.3 UseCases ×8

## 3. Implementaciones y estado
- [ ] 3.1 RepositoryImpls
- [ ] 3.2 CatalogCubit/PlayerCubit/InstructorCubit + states sealed
      Éxito: PlayerLocked cuando no hay inscripción (mensaje exacto)

## 4. Presentación e integración
- [ ] 4.1 CatalogPage (paginación), CourseDetailPage, LessonPlayerPage, MyCoursesPage
- [ ] 4.2 DI + rutas con guard por rol

## 5. Tests
- [ ] 5.1 Unit: RN001/RN004/RN006 como failures; fórmula progreso bordes
- [ ] 5.2 SQL: gating RLS, trigger completada, RPC duplicados
- [ ] 5.3 Widget: player locked/ready, catálogo paginado

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 1.3, 2.3 | unit+SQL (duplicado, auto-inscripción) |
| REQ-002 | 1.3, 2.3 | SQL gating + cubit locked |
| REQ-003 | 1.1, 1.3 | unit fórmula + SQL trigger |
| REQ-004 | 2.3 | unit publicación y archivo |
