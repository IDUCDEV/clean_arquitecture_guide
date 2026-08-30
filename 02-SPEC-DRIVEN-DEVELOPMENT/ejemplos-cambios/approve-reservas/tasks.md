# Tasks: approve-reservas

## 1. Dominio
- [ ] 1.1 Entities: Appointment (+status enum), WorkSchedule, BlockedDay
- [ ] 1.2 Interfaces AppointmentRepository + VeterinarianRepository (Either)
- [ ] 1.3 UseCases ×7 (uno por operación)

## 2. Capa de datos + Backend Supabase
- [ ] 2.1 Migración 0008: tablas + RPCs atómicos + RLS + pg_cron
      Éxito: doble reserva rechazada en SQL puro; políticas por actor
- [ ] 2.2 Models con roundtrip JSON (timestamptz ↔ DateTime UTC)
      Restricción: slots siempre en huso horario de la clínica (RT001)
- [ ] 2.3 RemoteDataSource (RPC + select) y LocalDataSource (caché de agenda)
- [ ] 2.4 RepositoryImpls (mapeo excepciones → Failure con mensajes exactos)

## 3. Estado y presentación
- [ ] 3.1 AgendaState/CreateAppointmentState sealed + Cubits
      Éxito: stream realtime actualiza AgendaLoaded
- [ ] 3.2 Pages + widgets (slot selector, tarjeta cita, calendario)

## 4. Integración
- [ ] 4.1 DI + rutas con guards por rol (dueño/doctor/admin)

## 5. Tests
- [ ] 5.1 Unit: reglas RN001-RN008 como failures de dominio
- [ ] 5.2 Integration SQL: doble reserva, cancelación fuera de plazo
- [ ] 5.3 Widget: agenda loaded/error, flujo agendar feliz

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 1.3, 2.1 | unit+SQL (doble reserva, antelación, límites) |
| REQ-002 | 1.3, 2.4 | unit (2h antelación) |
| REQ-003 | 3.1, 3.2 | cubit (transiciones + realtime) |
| REQ-004 | 2.1 | integration RLS |
| REQ-005 | 2.1 (cron) | integration pg_cron |