# Proposal: approve-reservas

> Deriva del caso completo "Sistema de Reservas (Clínica Veterinaria)". Ejemplo de **complejidad Compleja**: multi-actor, concurrencia (doble reserva), realtime.

## Impacto (Impact Report)
- Features afectadas: ninguna directa; requiere catálogo de doctores/mascotas
- Reutilizable: patrón CRUD estándar; `Failure` hierarchy
- Supabase: tabla nueva `appointments`; RLS vía join pets→owners; RPC atómico para slots
- DI / rutas: +2 cubits, +3 páginas, +3 registros ruta (agenda dueño / agenda doctor / agendar)
- Riesgos: doble reserva por concurrencia; huso horario de slots

## Why (Problema)
Los dueños agendan por teléfono o van sin cita: colas, ausencias y agenda desordenada para los doctores.

## What Changes (Solución)
Agenda de citas veterinarias: dueños agendan/cancelan/reagendan; doctores gestionan su día (completada/no-show); admins configuran horarios y bloqueos; recordatorio automático 24h antes.

## Capabilities
### New Capabilities
- `appointments`: agendamiento validado contra disponibilidad, con transiciones de estado auditables

## Scope (Alcance)
**Incluye:** agendar, cancelar (≥2h antes), reagendar, ver agendas por actor, marcar completada/no-show, horarios laborales, bloqueo de días, recordatorio 24h.
**No incluye:** facturación, recetas, pagos, historias clínicas.
**Dependencias:** autenticación, catálogo doctores/mascotas/tipos de consulta.
**Suposiciones:** duración según tipo de consulta; huso horario de la clínica.
**Preguntas abiertas:** ~~¿reagendar conserva recordatorio?~~ → SÍ, se reprogra (D2).

## Actores y permisos
| Actor | Puede | No puede | Mapeo RLS |
|-------|-------|----------|-----------|
| Dueño | Agendar/cancelar/reagendar citas de SUS mascotas | Ver citas ajenas | `pet_id in (select id from pets where owner_id = auth.uid())` |
| Doctor | Ver SU agenda, completar/cancelar/no-show | Editar datos del dueño | `doctor_id = auth.uid()` |
| Admin | Horarios, bloqueos, doctores | Agendar por un dueño | claim `role='admin'` |
| Notificaciones | Enviar recordatorio 24h | Cambiar citas | service role |

## Impact
- Código: ~20 ficheros en `lib/features/appointments/`
- Datos: tablas `appointments`, `work_schedules`, `blocked_days`, `reminders`; RPC atómico; cron pg_cron para no-show/recordatorios
- Breaking changes: ninguno
