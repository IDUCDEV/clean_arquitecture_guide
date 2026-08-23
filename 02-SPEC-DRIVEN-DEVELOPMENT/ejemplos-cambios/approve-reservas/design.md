# Design: approve-reservas

## Context
Multi-actor con concurrencia real (doble reserva) y realtime. Sigue el patrón estándar del curso.

## Goals / Non-Goals
- Goals: cero dobles reservas; agenda en vivo; reglas de antelación centralizadas
- Non-Goals: pagos, recetas, historias clínicas

## Decisions
### D1: Disponibilidad validada en servidor (RPC atómico)
- Decisión: `rpc.agendar_cita(...)` valida slot + RN002/RN003/RN008 dentro de transacción; constraint único `(doctor_id, date_time)` de respaldo
- Alternativas descartadas: validación solo frontend (race condition); bloqueo optimista por versión (complejidad innecesaria)
- Por qué: la fuente de verdad del slot es la BD

### D2: Reagendar = cancelar + crear atómicamente
- Decisión: RPC `reagendar_cita` hace ambas operaciones en una transacción y reprograma el recordatorio
- Por qué: evita estados intermedios inconsistentes

### D3: Realtime para agendas
- Decisión: `supabase.from('appointments').stream()` filtrado por doctor/dueño
- Por qué: REQ-003 agenda en vivo sin polling

## Ficheros afectados (resumen)
| Elemento | Capa | Archivo |
|----------|------|---------|
| Appointment, Pet, WorkSchedule… | domain/entities | lib/features/appointments/domain/entities/ |
| AppointmentRepository, VeterinarianRepository | domain/repositories | …/domain/repositories/ |
| CreateAppointment, CancelAppointment, Reschedule, GetDoctorAgenda, GetOwnerAppointments, MarkCompleted, MarkNoShow | domain/usecases | …/domain/usecases/ |
| Models + RemoteDataSource + LocalDataSource(caché) + Impls | data | lib/features/appointments/data/ |
| AgendaCubit, CreateAppointmentCubit (+states) | presentation/cubit | …/presentation/cubit/ |
| AgendaPage, CreateAppointmentPage, DetailPage | presentation/pages | …/presentation/pages/ |
| Migraciones + RPC + RLS + pg_cron | supabase/migrations | 0008_appointments_rls.sql |

## Contratos Dart clave
```dart
abstract interface class AppointmentRepository {
  Future<Either<Failure, Appointment>> create(CreateAppointmentParams params);
  Future<Either<Failure, Appointment>> cancel(String appointmentId);
  Future<Either<Failure, Appointment>> reschedule(String id, DateTime newDateTime);
  Future<Either<Failure, Appointment>> markCompleted(String appointmentId);
  Future<Either<Failure, Appointment>> markNoShow(String appointmentId);
  Future<Either<Failure, List<Appointment>>> getDoctorAgenda(String doctorId, DateTime date);
  Future<Either<Failure, List<Appointment>>> getOwnerAppointments(String ownerId, {AppointmentStatus? status});
}
sealed class AgendaState {}
class AgendaLoading extends AgendaState {}
class AgendaLoaded extends AgendaState { final List<Appointment> appointments; const AgendaLoaded(this.appointments); }
class AgendaError extends AgendaState { final String message; const AgendaError(this.message); }
```

## Flujo de datos (agendar)
```
CreateAppointmentPage ──► CreateAppointmentCubit.submit()
      │ emit Creating
      ▼
CreateAppointment ──► AppointmentRepository.create()
      ▼
RemoteDataSource.agendar(rpc) ──► Supabase transacción:
      valida RN001/RN002/RN003/RN008 → INSERT → commit
      ▼
Either.right(Appointment) ──► Created ──► navegar a detalle
Either.left(Failure("slot_ocupado")) ──► Error(mensaje) ──► refrescar slots
```

## Backend Supabase
- `appointments(id, pet_id→pets, doctor_id→doctors, date_time timestamptz, duration_min, status enum(scheduled,completed,cancelled,no_show), created_at)`
- RLS: dueño vía subquery pets; doctor por `doctor_id = auth.uid()`
- RPC: `agendar_cita`, `reagendar_cita` (security definer, transaccionales)
- Cron: recordatorios 24h; no-show automático a los 15 min

## Boundaries
No tocar catálogo de mascotas/doctores existente; no añadir paquetes; RLS nunca desactivada.
