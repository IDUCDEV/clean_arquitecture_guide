# Tasks: approve-reservas

## 1. Dominio y datos base
- [ ] 1.1 Entities: Appointment (+status enum), WorkSchedule, BlockedDay
- [ ] 1.2 Interfaces AppointmentRepository + VeterinarianRepository (Either)
- [ ] 1.3 Migración 0008: tablas + RPCs atómicos + RLS + pg_cron
      Éxito: doble reserva rechazada en SQL puro; políticas por actor

## 2. Capa de datos
- [ ] 2.1 Models con roundtrip JSON (timestamptz ↔ DateTime UTC)
      Restricción: slots siempre en huso horario de la clínica (RT001)
- [ ] 2.2 RemoteDataSource (RPC + select) y LocalDataSource (caché de agenda)
- [ ] 2.3 UseCases ×7 (uno por operación)

## 3. Implementaciones y estado
- [ ] 3.1 RepositoryImpls (mapeo excepciones → Failure con mensajes exactos)
- [ ] 3.2 AgendaState/CreateAppointmentState sealed + Cubits
      Éxito: stream realtime actualiza AgendaLoaded

## 4. Presentación e integración
- [ ] 4.1 Pages + widgets (slot selector, tarjeta cita, calendario)
- [ ] 4.2 DI + rutas con guards por rol (dueño/doctor/admin)

## 5. Tests
- [ ] 5.1 Unit: reglas RN001-RN008 como failures de dominio
- [ ] 5.2 Integration SQL: doble reserva, cancelación fuera de plazo
- [ ] 5.3 Widget: agenda loaded/error, flujo agendar feliz

## Trazabilidad
| Req | Tarea(s) | Test |
|-----|----------|------|
| REQ-001 | 1.3, 2.3 | unit+SQL (doble reserva, antelación, límites) |
| REQ-002 | 2.3, 3.1 | unit (2h antelación) |
| REQ-003 | 3.2, 4.1 | cubit (transiciones + realtime) |
| REQ-004 | 1.3 | integration RLS |
| REQ-005 | 1.3 (cron) | integration pg_cron |
