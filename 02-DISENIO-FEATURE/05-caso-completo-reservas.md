# Caso Completo: Sistema de Reservas

> Aplica todo lo aprendido (FADER + Mapeo + Contratos + Flujo + Supabase + Criterios) para diseñar un Sistema de Reservas desde cero, en papel y lápiz.

---

## Objetivo

Sin abrir el editor, sin escribir una sola línea de código, vas a diseñar la arquitectura completa de un Sistema de Reservas usando la metodología FADER y Clean Architecture.

Al terminar, tendrás:
- ✅ Feature descompuesta (Alcance, Formular, Actorizar, Descomponer, Entidades, Reglas)
- ✅ Mapeo completo a capas de Clean Architecture
- ✅ Contratos (interfaces) de cada capa
- ✅ Diagramas de flujo de datos
- ✅ Diseño de Supabase (tablas, RPC, RLS, realtime)
- ✅ Criterios de aceptación y matriz de trazabilidad
- ✅ ADRs documentando decisiones clave

---

## Enunciado del Sistema de Reservas

Somos un equipo que desarrolla una app para **clínicas veterinarias**. El equipo de producto nos pide:

> Los dueños de mascotas deben poder agendar citas veterinarias seleccionando un doctor, una fecha disponible y el tipo de consulta. El sistema debe validar disponibilidad, evitar dobles reservas, y enviar un recordatorio 24 horas antes. Los doctores deben poder ver su agenda del día y marcar citas como completadas o canceladas. Los administradores de la clínica deben poder configurar horarios laborales y bloquear días no laborables.

---

## Tu Misión

Completa cada sección en orden, en papel y lápiz. La siguiente guía te lleva paso a paso.

---

## Sección 0: Alcance

Antes de descomponer, define los límites del sistema (teoría en [00-alcance-feature.md](./00-alcance-feature.md)):

1. **Incluye:** ¿qué cubre el sistema de reservas?
2. **No incluye:** ¿qué NO cubre? (ej: facturación, recetas, pagos)
3. **Dependencias:** ¿qué necesita que exista antes?
4. **Suposiciones:** ¿qué das por hecho?
5. **Preguntas abiertas:** ¿qué no sabes todavía?

---

## Sección 1: FADER

### ✏️ Paso 1: Formular

Define al menos 3 enunciados "Como [actor], quiero [acción] para [valor]".

**Pregúntate:**
- ¿Qué necesidad real resuelve agendar una cita?
- ¿Qué pasa si el dueño no puede agendar desde la app? (llama por teléfono, va sin cita)
- ¿Cuál es el valor de los recordatorios?

### ✏️ Paso 2: Actorizar

Identifica todos los actores:

| Actor | Tipo | ¿Qué puede hacer? |
|-------|------|-------------------|
| Dueño de mascota | Primario | |
| Doctor | Secundario | |
| Administrador | Secundario | |
| Sistema de notificaciones | Interno | |
| Calendario (Google/Apple) | Externo | |
| ? | ? | |

Completa la tabla con los permisos de cada actor.

### ✏️ Paso 3: Descomponer

Enumera todas las operaciones atómicas. Clasifícalas como CRUD, Validación, Cálculo, o Transición.

**Ejemplo para empezar:**
- `[C]` Crear cita
- `[R]` Ver agenda del doctor
- `[R]` Ver citas del dueño
- `[U]` Cancelar cita
- `[U]` Marcar como completada
- ...
- ¿Qué más?

**Identifica dependencias:**
- ¿Qué debe pasar antes de crear una cita?
- ¿Qué debe pasar después de crearla?

### ✏️ Paso 4: Entidades

Define las entidades de negocio. Para cada una, lista sus atributos esenciales.

**Posibles entidades:**
- `Cita` (Appointment)
- `Doctor` (Veterinarian)
- `Mascota` (Pet)
- `Dueño` (Owner)
- `HorarioLaboral` (WorkSchedule)
- `TipoConsulta` (ConsultationType)
- `Recordatorio` (Reminder)

**Pregúntate:**
- ¿`Doctor` y `Dueño` son la misma entidad que `Usuario`?
- ¿`Mascota` pertenece al dueño o a la clínica?
- ¿Un `HorarioLaboral` pertenece a un doctor o a la clínica?

### ✏️ Paso 5: Reglas

Enuncia al menos 8 reglas de negocio con formato RN001, RN002... y añade reglas técnicas (RT) y de seguridad (RS) cuando aplique (teoría en [01-descomposicion-feature.md](./01-descomposicion-feature.md#paso-5-reglas)).

**Áreas a cubrir:**
- Disponibilidad (no dobles reservas)
- Antelación mínima para agendar
- Antelación mínima para cancelar
- Duración de consultas
- Límite de citas por día
- Recordatorios
- Cancelaciones vs No-show
- Reagendamiento

---

## Sección 2: Mapeo a Capas

### ✏️ Paso 1: Estructura DOMAIN

Dibuja el árbol de `domain/`:

```
domain/
├── entities/
│   ├── cita.dart
│   ├── doctor.dart
│   ├── mascota.dart
│   ├── dueno.dart
│   ├── horario_laboral.dart
│   └── tipo_consulta.dart
├── usecases/
│   ├── agendar_cita.dart          ← ¿Qué reglas valida?
│   ├── cancelar_cita.dart         ← ¿Qué reglas valida?
│   ├── obtener_agenda_doctor.dart
│   ├── obtener_citas_dueno.dart
│   ├── marcar_completada.dart
│   └── configurar_horario.dart
├── repositories/
│   ├── cita_repository.dart       ← interface
│   └── doctor_repository.dart     ← interface
└── core/
    └── failures.dart              ← Errores del dominio
```

**Pregúntate:**
- ¿Todos los UseCases son necesarios o algunos se pueden combinar?
- ¿Necesitamos un repository para `Mascota` o va dentro de `CitaRepository`?
- ¿Dónde va la lógica de recordatorios?

### ✏️ Paso 2: Estructura DATA

Dibuja el árbol de `data/`:

```
data/
├── datasources/
│   ├── cita_remote_data_source.dart
│   └── cita_local_data_source.dart
├── models/
│   ├── cita_model.dart
│   ├── doctor_model.dart
│   ├── mascota_model.dart
│   └── horario_model.dart
└── repositories/
    ├── cita_repository_impl.dart
    └── doctor_repository_impl.dart
```

**Pregúntate:**
- ¿El DataSource local es solo caché o la fuente primaria?
- ¿Necesitamos un modelo separado para cada entidad?
- ¿Cómo manejamos los horarios recurrentes (lunes a viernes 9-18)?

### ✏️ Paso 3: Estructura PRESENTATION

Dibuja el árbol de `presentation/`:

```
presentation/
├── cubit/
│   ├── agenda_cubit.dart
│   ├── agenda_state.dart
│   ├── agendar_cita_cubit.dart
│   └── agendar_cita_state.dart
├── pages/
│   ├── agenda_page.dart
│   ├── agendar_cita_page.dart
│   └── detalle_cita_page.dart
└── widgets/
    ├── slot_horario_widget.dart
    ├── tarjeta_cita_widget.dart
    └── calendario_widget.dart
```

**Pregúntate:**
- ¿Un solo Cubit o varios? (agenda del doctor vs agendar nueva cita)
- ¿Qué estados puede tener cada Cubit?
- ¿El calendario widget es un componente reutilizable?

---

## Sección 3: Contratos

### ✏️ Paso 1: Contrato CitaRepository

Diseña la interfaz `CitaRepository`:

```dart
abstract class CitaRepository {
  // ¿Qué métodos necesita el dominio?
  // ¿Qué parámetros recibe cada uno?
  // ¿Qué retorna?
  // ¿Qué failures puede producir?
}
```

**Operaciones a considerar:**
- Crear cita
- Cancelar cita
- Reagendar cita
- Obtener citas por rango de fechas
- Obtener citas de un doctor
- Obtener citas de un dueño
- Marcar como completada
- Marcar como no-show

### ✏️ Paso 2: Contrato DoctorRepository

```dart
abstract class DoctorRepository {
  // ¿Cómo se obtienen los doctores disponibles?
  // ¿Cómo se obtienen los horarios?
}
```

### ✏️ Paso 3: Contrato de DataSource Remoto

```dart
abstract class CitaRemoteDataSource {
  // ¿Qué operaciones de bajo nivel?
  // ¿Usa modelos o mapas?
}
```

### ✏️ Paso 4: Estados de UI

Diseña los estados para `AgendaCubit` y `AgendarCitaCubit`:

```
AgendaState:
  - ¿Qué estados? (loading, loaded, error, etc.)
  - ¿Qué datos lleva cada estado?

AgendarCitaState:
  - ¿Qué estados? (initial, loading, success, error, etc.)
  - ¿Cómo manejas la selección de fecha y doctor?
```

### ✏️ Paso 5: ADR

Escribe al menos un ADR documentando una decisión clave, como:

- ¿Por qué separamos CitaRepository de DoctorRepository? (o por qué no)
- ¿Cómo manejamos la validación de disponibilidad (local vs API)?
- ¿Dónde se genera el recordatorio (dominio vs sistema externo)?

---

## Sección 4: Flujo de Datos

### ✏️ Paso 1: Flujo Agendar Cita

Dibuja la secuencia completa desde que el dueño selecciona un horario hasta que la cita queda registrada.

**Incluye:**
- Widget → Cubit → UseCase → Repository → DataSources → API
- Validaciones en cada paso
- Transformación de tipos
- Manejo de errores
- Actualización de estados del Cubit

**Pregúntate:**
- ¿Cuándo se valida que el horario sigue disponible?
- ¿Qué pasa si otro dueño reservó el mismo slot mientras tanto?
- ¿Cómo se actualiza la UI del doctor en tiempo real?

### ✏️ Paso 2: Flujo Cancelar Cita

Dibuja el flujo de cancelación.

**Pregúntate:**
- ¿Hay una regla de "solo se puede cancelar con 2 horas de antelación"?
- ¿Dónde se valida esa regla?
- ¿Qué pasa con el recordatorio programado?
- ¿Se notifica al doctor?

### ✏️ Paso 3: Flujo Ver Agenda del Doctor

Dibuja el flujo de carga de la agenda.

**Pregúntate:**
- ¿Es offline-first o siempre online?
- ¿Cómo manejas el caché de horarios?
- ¿Qué pasa si la API falla?

---

## Sección 5: Diseño Supabase

Ahora aterriza el diseño en Supabase (teoría en [05e-diseno-supabase.md](./05e-diseno-supabase.md)):

> **¿Tu backend es una REST API (Python/otro)?** Aquí no implementas el servidor: solo especificas el **contrato** (endpoints, DTOs, códigos de error, garantías de atomicidad y autorización) que consume tu `RemoteDataSource` con Dio; el backend la diseña e implementa.

1. **Tablas:** define las tablas, columnas y tipos (snake_case).
2. **Operaciones:** para cada UseCase, ¿qué operación lo implementa (select/insert/update/rpc)?
3. **RLS:** define policies que hagan cumplir RS001.
4. **Atomicidad:** identifica operaciones que deben ser atómicas (ej: agendar un slot disponible → RPC en transacción).
5. **Realtime:** ¿qué tablas se sincronizan en vivo?

**Pregúntate:**
- ¿La validación de slot disponible (RN001) vive en un RPC atómico o en el cliente?
- ¿Cómo evitas que el dueño A vea citas del dueño B (RS001)?
- ¿El recordatorio (RN006) lo dispara Postgres (cron) o un servicio externo?

---

## Sección 6: Criterios de Aceptación y Trazabilidad

Cierra el diseño definiendo criterios (teoría en [05f-criterios-aceptacion-trazabilidad.md](./05f-criterios-aceptacion-trazabilidad.md)):

1. **Criterios de aceptación:** escribe al menos 5 en formato BDD (Dado/Cuando/Entonces).
2. **Matriz de trazabilidad:** para los UseCases críticos, cruza UseCase → Regla → Contrato → Fuente de verdad → Test.

**Pregúntate:**
- ¿El criterio "cancelar con 2h de antelación" es verificable?
- ¿Toda regla RN tiene al menos un UseCase y un test que la cubra?
- ¿Los criterios distinguen el frontend (validación optimista) del servidor (fuente de verdad)?

---

## Solución Sugerida

> ⚠️ Resuelve cada sección en papel primero. La solución sugerida es para comparar después.

### ✅ FADER Completo

```
╔═══════════════════════════════════════════════════════════════╗
║  FEATURE: Sistema de Reservas (Clínica Veterinaria)         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [F]ormular:                                                  ║
║  F1: Como dueño de mascota, quiero agendar citas             ║
║      veterinarias online para asegurar atención en el         ║
║      horario que me conviene.                                 ║
║  F2: Como doctor, quiero ver mi agenda del día para          ║
║      organizar mi trabajo.                                    ║
║  F3: Como administrador, quiero configurar horarios          ║
║      laborales para gestionar la disponibilidad de la        ║
║      clínica.                                                 ║
║                                                               ║
║  [A]ctorizar:                                                 ║
║  1. Dueño de mascota (primario)                              ║
║     - Agendar, cancelar, reagendar citas                     ║
║     - Ver historial de citas de su mascota                   ║
║  2. Doctor (secundario)                                       ║
║     - Ver agenda del día                                      ║
║     - Marcar citas como completada/cancelada/no-show         ║
║  3. Administrador (secundario)                                ║
║     - Configurar horarios laborales                           ║
║     - Bloquear días no laborables                             ║
║     - Gestionar doctores                                      ║
║  4. Sistema de Notificaciones (interno)                      ║
║     - Recordatorio 24h antes                                  ║
║     - Notificar cancelación al doctor                        ║
║  5. Google/Apple Calendar (externo, opcional)                ║
║     - Exportar cita al calendario del dueño                  ║
║                                                               ║
║  [D]escomponer:                                               ║
║  Dueño:                                                       ║
║  - [C] Agendar cita                                           ║
║  - [R] Ver citas próximas                                     ║
║  - [R] Ver historial de citas                                 ║
║  - [U] Cancelar cita                                          ║
║  - [U] Reagendar cita                                         ║
║                                                               ║
║  Doctor:                                                      ║
║  - [R] Ver agenda del día                                     ║
║  - [U] Marcar cita como completada                            ║
║  - [U] Marcar cita como cancelada                             ║
║  - [U] Marcar cita como no-show                               ║
║                                                               ║
║  Admin:                                                       ║
║  - [C] Configurar horario laboral                             ║
║  - [C] Bloquear día no laborable                              ║
║  - [CUD] Gestionar doctores                                   ║
║                                                               ║
║  Sistema:                                                     ║
║  - [Validación] Validar disponibilidad (no doble reserva)    ║
║  - [Validación] Validar antelación mínima (4h)               ║
║  - [Cálculo] Generar slots disponibles                        ║
║  - [Transición] Enviar recordatorio (24h antes)              ║
║  - [Transición] Notificar cancelación                        ║
║                                                               ║
║  [E]ntidades:                                                 ║
║  Cita: id, mascota, doctor, fechaHora, duracion,             ║
║        tipoConsulta, estado, motivo, notas                    ║
║  Doctor: id, nombre, especialidad, email, telefono            ║
║  Mascota: id, nombre, especie, raza, edad, dueno             ║
║  Dueño: id, nombre, email, telefono, mascotas                ║
║  HorarioLaboral: id, doctor, diaSemana, horaInicio,          ║
║                  horaFin, activo                              ║
║  BloqueoDia: id, fecha, motivo                               ║
║  TipoConsulta: id, nombre, duracionMinutos, precio           ║
║  Recordatorio: id, cita, tipo, enviadoEn, estado             ║
║                                                               ║
║  [R]eglas:                                                    ║
║  RN001: No se puede agendar una cita en un slot ocupado       ║
║  RN002: Antelación mínima de 4 horas para agendar             ║
║  RN003: Máximo 8 citas por doctor por día                     ║
║  RN004: Cancelación solo con 2h de antelación                  ║
║  RN005: No-show se marca si pasan 15min de la hora             ║
║  RN006: Recordatorio automático 24h antes                      ║
║  RN007: Duración de consulta según tipoConsulta               ║
║  RN008: Un dueño no puede tener 2 citas el mismo día          ║
║        para la misma mascota (máximo 1 consulta/día)         ║
║  RT001: Slots en huso horario de la clínica                   ║
║  RS001: Solo el dueño ve citas de su propia mascota           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### ✅ Estructura de Capas

```
lib/
└── appointments/
    ├── domain/
    │   ├── entities/
    │   │   ├── appointment.dart
    │   │   ├── veterinarian.dart
    │   │   ├── pet.dart
    │   │   ├── owner.dart
    │   │   ├── work_schedule.dart
    │   │   ├── blocked_day.dart
    │   │   └── consultation_type.dart
    │   ├── usecases/
    │   │   ├── create_appointment.dart
    │   │   ├── cancel_appointment.dart
    │   │   ├── reschedule_appointment.dart
    │   │   ├── get_doctor_agenda.dart
    │   │   ├── get_owner_appointments.dart
    │   │   ├── mark_completed.dart
    │   │   ├── mark_no_show.dart
    │   │   └── configure_schedule.dart
    │   ├── repositories/
    │   │   ├── appointment_repository.dart
    │   │   └── veterinarian_repository.dart
    │   └── core/
    │       └── failures.dart
    ├── data/
    │   ├── datasources/
    │   │   ├── appointment_remote_datasource.dart
    │   │   └── appointment_local_datasource.dart
    │   ├── models/
    │   │   ├── appointment_model.dart
    │   │   ├── veterinarian_model.dart
    │   │   └── pet_model.dart
    │   └── repositories/
    │       ├── appointment_repository_impl.dart
    │       └── veterinarian_repository_impl.dart
    └── presentation/
        ├── cubit/
        │   ├── agenda_cubit.dart
        │   ├── agenda_state.dart
        │   ├── create_appointment_cubit.dart
        │   └── create_appointment_state.dart
        ├── pages/
        │   ├── agenda_page.dart
        │   ├── create_appointment_page.dart
        │   └── appointment_detail_page.dart
        └── widgets/
            ├── time_slot_widget.dart
            ├── appointment_card.dart
            └── doctor_selector.dart
```

### ✅ Contrato Clave (CitaRepository)

```dart
abstract class AppointmentRepository {
  Future<Either<Failure, Appointment>> create(CreateAppointmentParams params);
  Future<Either<Failure, Appointment>> cancel(String appointmentId);
  Future<Either<Failure, Appointment>> reschedule(
    String appointmentId, DateTime newDateTime);
  Future<Either<Failure, Appointment>> markCompleted(String appointmentId);
  Future<Either<Failure, Appointment>> markNoShow(String appointmentId);
  Future<Either<Failure, List<Appointment>>> getDoctorAgenda(
    String doctorId, DateTime date);
  Future<Either<Failure, List<Appointment>>> getOwnerAppointments(
    String ownerId, {AppointmentStatus? status});
  Future<Either<Failure, List<DateTime>>> getAvailableSlots(
    String doctorId, DateTime date, String consultationTypeId);
}
```

### ✅ ADR Recomendado

```markdown
# ADR-003: Validación de disponibilidad del lado del servidor

## Contexto
Cuando dos dueños intentan agendar el mismo slot simultáneamente,
necesitamos evitar dobles reservas (RN001).

## Decisión
La validación de disponibilidad se hará en el backend (Supabase)
usando una transacción atómica. El frontend validará de forma
optimista, pero la validación definitiva es del servidor.

## Consecuencias
Positivas:
- Garantiza que no haya dobles reservas (race condition)
- El frontend es rápido (validación optimista)

Negativas:
- Mayor latencia en caso de conflicto
- El frontend debe manejar el caso "slot ya ocupado"

## Alternativas consideradas
1. Bloqueo optimista con versión → Descartado: complejidad innecesaria
2. Validación solo frontend → Descartado: race condition
3. Cola de reservas → Descartado: sobreingeniería para este caso
```

### ✅ Diseño Supabase

```
appointments
├── id            uuid PK
├── pet_id        uuid FK → pets
├── doctor_id     uuid FK → doctors
├── date_time     timestamptz
├── duration_min  int
├── status        enum (scheduled, completed, cancelled, no_show)
├── created_at    timestamptz

-- RS001: cada dueño solo ve citas de sus mascotas
create policy "owner sees own pets appointments"
  on appointments for select
  using (pet_id in (select id from pets where owner_id = auth.uid()));

-- RN001: slot atómico (evita doble reserva)
--   rpc agendar_cita(p_pet_id, p_doctor_id, p_date_time, p_duration_min)
--   → BEGIN; INSERT con constraint único (doctor_id, date_time); COMMIT;
--   → si hay conflicto, retorna error "slot_ocupado"
```

### ✅ Criterios de Aceptación (ejemplos)

```gherkin
Escenario: Agendar cita en slot libre
  Dado un doctor con un slot libre el 2026-08-10 10:00
  Y la reserva se hace con más de 4h de antelación (RN002)
  Cuando el dueño agenda ese slot
  Entonces la cita queda con estado "scheduled"
  Y otro dueño ya no ve ese slot disponible

Escenario: Intentar agendar el mismo slot dos veces
  Dado un slot recién reservado por el dueño A
  Cuando el dueño B intenta agendar el mismo slot
  Entonces el sistema rechaza con "slot_ocupado" (RN001)
```

### ✅ Matriz de Trazabilidad

| UseCase            | Regla(s)      | Contrato                                   | Fuente de verdad | Test                 |
|--------------------|---------------|--------------------------------------------|------------------|----------------------|
| CreateAppointment  | RN001, RN002  | AppointmentRepository.create               | RPC atómico      | unit + widget        |
| CancelAppointment  | RN004         | AppointmentRepository.cancel               | API + RLS        | unit                 |
| GetDoctorAgenda    | RN007, RT001  | AppointmentRepository.getDoctorAgenda      | API              | unit                 |
| MarkNoShow         | RN005         | AppointmentRepository.markNoShow           | RPC + cron       | unit + integration   |
| Ver agenda (dueño) | RS001         | AppointmentRepository.getOwnerAppointments | RLS              | integration (RLS)    |

---

## Entregable Final

Al completar este caso, deberías tener en papel:

1. ✅ Una hoja FADER completa (Alcance, Formular, Actorizar, Descomponer, Entidades, Reglas)
2. ✅ El árbol de carpetas de las 3 capas (domain, data, presentation)
3. ✅ Los contratos de AppointmentRepository y VeterinarianRepository
4. ✅ Los estados de los Cubits
5. ✅ Al menos 1 ADR documentando una decisión clave
6. ✅ Diagrama de flujo de "Agendar Cita" (de UI a BD y vuelta)
7. ✅ El diseño de Supabase (tablas, RPC atómico, RLS)
8. ✅ Criterios de aceptación y matriz de trazabilidad

**Con esto, estás listo para abrir el editor y empezar a codificar.**

---

## 🚀 Siguiente paso

Con el diseño completo en papel, abre tu editor y continúa con [01-CLEAN-ARCHITECTURE](../01-CLEAN-ARCHITECTURE/) para implementar todo lo diseñado.

---

**Tiempo estimado:** 2-3 horas  
**Material:** Papel, lápiz. Muchas hojas.
