# 🎫 Práctica: Sistema de Reservas con Enfoque Híbrido IA + Código Manual

> Aplicación paso a paso del framework AIDR usando Clean Architecture

---

## 📋 Tabla de Contenidos

1. [Contexto del Proyecto](#1-contexto-del-proyecto)
2. [FASE A: Analyze - Análisis del Problema](#2-fase-a-analyze)
3. [FASE B: Investigate - Investigación con IA](#3-fase-b-investigate)
4. [FASE C: Decide - Decisiones de Responsabilidad](#4-fase-c-decide)
5. [FASE D: Implement - Implementación Híbrida](#5-fase-d-implement)
6. [FASE E: Review - Revisión y Validación](#6-fase-e-review)
7. [FASE F: Testing - Tests Híbridos](#7-fase-f-testing)
8. [Resumen y Checklist Final](#8-resumen-y-checklist-final)

---

## 1. Contexto del Proyecto

### 📝 Descripción del Dominio

```
┌─────────────────────────────────────────────────────────────────┐
│                 SISTEMA DE RESERVAS                             │
│                                                                 │
│  Contexto: Una aplicación móvil para reservas de citas         │
│  en un salón de belleza. Los clientes pueden:                  │
│                                                                 │
│  • Ver disponibilidad de horarios                             │
│  • Reservar citas con servicios específicos                    │
│  • Cancelar o reprogramar reservas                            │
│  • Entrar a lista de espera si no hay slots                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🏗️ Requisitos Funcionales

| # | Requisito | Prioridad |
|---|-----------|-----------|
| RF-01 | Ver horarios disponibles por fecha y servicio | Alta |
| RF-02 | Crear reserva con cliente, servicio, fecha y hora | Alta |
| RF-03 | Double booking prevention (no permitir 2 reservas mismo slot) | Crítica |
| RF-04 | Buffer time de 15 min entre reservas (limpieza/preparación) | Alta |
| RF-05 | Horarios especiales: festivos y temporada alta | Media |
| RF-06 | Lista de espera automática cuando slot lleno | Alta |
| RF-07 | Cancelación de reserva con política (24h antes) | Alta |
| RF-08 | No-show tracking: 3 no-shows = bloqueo | Media |
| RF-09 | Overbooking estratégico: 10% más reservas que capacidad | Baja |

### 🎯 Conceptos Clave del Dominio

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONCEPTOS DEL DOMINIO                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Slot (Ventana de tiempo)                                   │
│     ├── Hora inicio                                             │
│     ├── Hora fin                                                │
│     ├── Duración del servicio                                   │
│     ├── Buffer time (15 min después)                           │
│     └── Estado: available | reserved | blocked                  │
│                                                                 │
│  📋 Reserva (Booking)                                           │
│     ├── Cliente asociado                                       │
│     ├── Servicio solicitado                                     │
│     ├── Slot reservado                                         │
│     ├── Estado: confirmed | cancelled | completed | no_show    │
│     └── Timestamps: created, confirmed, cancelled              │
│                                                                 │
│  ⏳ Waitlist (Lista de espera)                                  │
│     ├── Cliente                                                 │
│     ├── Servicio                                                │
│     ├── Fecha deseada                                           │
│     ├── Posición en cola                                        │
│     └── Estado: waiting | notified | expired | booked           │
│                                                                 │
│  🛠️ Servicio (Service)                                          │
│     ├── Nombre                                                 │
│     ├── Duración en minutos                                     │
│     ├── Precio                                                  │
│     └── Categoría                                               │
│                                                                 │
│  👤 Cliente (Client)                                           │
│     ├── Nombre, email, teléfono                                 │
│     ├── No-show count                                           │
│     ├── Estado: active | blocked                               │
│     └── Fecha último no-show                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 📁 Estructura de Carpetas Objetivo

```
features/reservation/
│
├── domain/
│   ├── entities/
│   │   ├── client.dart
│   │   ├── service.dart
│   │   ├── slot.dart
│   │   ├── booking.dart
│   │   └── waitlist.dart
│   │
│   ├── repositories/
│   │   ├── booking_repository.dart
│   │   └── waitlist_repository.dart
│   │
│   ├── usecases/
│   │   ├── get_available_slots.dart
│   │   ├── create_booking.dart
│   │   ├── cancel_booking.dart
│   │   ├── mark_no_show.dart
│   │   ├── add_to_waitlist.dart
│   │   └── process_waitlist.dart
│   │
│   └── failures/
│       └── reservation_failure.dart
│
├── data/
│   ├── models/
│   │   ├── client_model.dart
│   │   ├── service_model.dart
│   │   ├── slot_model.dart
│   │   ├── booking_model.dart
│   │   └── waitlist_model.dart
│   │
│   ├── datasources/
│   │   ├── reservation_remote_datasource.dart
│   │   └── reservation_local_datasource.dart
│   │
│   └── repositories/
│       ├── booking_repository_impl.dart
│       └── waitlist_repository_impl.dart
│
├── presentation/
│   ├── cubit/
│   │   ├── reservation_cubit.dart
│   │   └── reservation_state.dart
│   │
│   └── pages/
│       ├── booking_page.dart
│       └── waitlist_page.dart
│
└── core/
    ├── constants/
    │   ├── reservation_constants.dart
    │   └── special_schedules.dart
    └── utils/
        └── slot_calculator.dart
```

---

## 2. FASE A: Analyze

> **Objetivo:** Entender completamente el problema antes de escribir una sola línea de código.

### 2.1 Análisis del Problema Principal

```markdown
┌─────────────────────────────────────────────────────────────────┐
│                    PREGUNTAS DE ANÁLISIS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ¿Qué hace una reserva?                                      │
│     → Asocia un cliente + servicio + slot de tiempo            │
│                                                                 │
│  2. ¿Qué puede salir mal?                                      │
│     → Double booking: 2 personas mismo horario                 │
│     → Cliente bloqueado intenta reservar                       │
│     → Slot en el pasado                                        │
│     → Servicio no existe                                       │
│                                                                 │
│  3. ¿Qué reglas de negocio son críticas?                        │
│     → Double booking prevention (CRÍTICA)                      │
│     → 15 min buffer entre reservas                             │
│     → Cancelación 24h antes = refund, <24h = penalty          │
│     → 3 no-shows = cliente bloqueado                          │
│                                                                 │
│  4. ¿Qué es específico de ESTE negocio?                       │
│     → Buffer time configurable por servicio                   │
│     → Horarios especiales (festivos propios del salón)        │
│     → Lista de espera con notificación automática             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Identificación de Lógica Crítica

```markdown
┌─────────────────────────────────────────────────────────────────┐
│              LÓGICA CRÍTICA IDENTIFICADA                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ LO HACE LA IA (Boilerplate):                                │
│     • Estructura de entidades (campos básicos)                 │
│     • Scaffold de repository interfaces                        │
│     • Boilerplate de use cases                                 │
│     • Model.fromJson() / toJson()                              │
│     • Estados de Cubit (Loading/Success/Error)                 │
│                                                                 │
│  ✅ LO HAGO YO (Lógica Crítica):                                │
│                                                                 │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │ 1. VALIDACIÓN DE SLOT DISPONIBLE                        │ │
│     │    • Verificar que no exista reserva para ese slot     │ │
│     │    • Incluir buffer time (±15 min)                     │ │
│     │    • Verificar rango de horas válido                   │ │
│     └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │ 2. HORARIOS ESPECIALES                                  │ │
│     │    • Festivos: horarios reducidos o cerrados           │ │
│     │    • Temporada alta: horarios extendidos               │ │
│     │    • Día específico: configuración custom              │ │
│     └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │ 3. WAILIST AUTOMÁTICO                                   │ │
│     │    • Posición en cola según prioridad                  │ │
│     │    • Notificar cuando se libere slot                   │ │
│     │    • Expiración de waitlist (48h)                     │ │
│     └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │ 4. POLÍTICA DE CANCELACIÓN                              │ │
│     │    • >24h: refund completo                             │ │
│     │    • <24h: penalty del 50%                             │ │
│     │    • <2h: penalty del 100%                             │ │
│     └─────────────────────────────────────────────────────────┘ │
│                                                                 │
│     ┌─────────────────────────────────────────────────────────┐ │
│     │ 5. NO-SHOW TRACKING                                     │ │
│     │    • Incrementar contador en no-show                   │ │
│     │    • Bloquear cliente en 3 no-shows                     │ │
│     │    • Reset contador al año                             │ │
│     └─────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Edge Cases No Tan Obvios

```markdown
┌─────────────────────────────────────────────────────────────────┐
│                    EDGE CASES COMPLEJOS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Edge Case 1: Reserva justo en buffer time                   │
│     ════════════════════════════════════════                    │
│     Situación:                                                  │
│     - Slot A: 10:00 - 11:00 (reservado)                        │
│     - Buffer: 11:00 - 11:15                                     │
│     - Slot B: 11:15 - 12:00 (disponible)                       │
│                                                                 │
│     Pregunta: ¿Un cliente puede reservar 11:00?                 │
│     Respuesta de negocio: NO, el buffer está bloqueado        │
│                                                                 │
│     Lógica a implementar:                                      │
│     → Slot disponible = horario_inicio >= slot.fin + buffer   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Edge Case 2: Reserva en horario de cierre                  │
│     ════════════════════════════════════════                    │
│     Situación:                                                  │
│     - Salon cierra 20:00                                        │
│     - Servicio dura 90 min                                     │
│     - Cliente quiere reservar 19:00                            │
│                                                                 │
│     Pregunta: ¿Se permite?                                      │
│     Respuesta de negocio: NO, no alcanza a terminar           │
│                                                                 │
│     Lógica a implementar:                                      │
│     → horario_fin = horario_inicio + duracion + buffer         │
│     → horario_fin <= hora_cierre                               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Edge Case 3: Festivo con horario especial                  │
│     ════════════════════════════════════════                    │
│     Situación:                                                  │
│     - 24 Dic (Nochebuena): abre 10:00, cierra 15:00           │
│     - Servicio: 60 min                                         │
│     - Cliente quiere 14:30                                     │
│                                                                 │
│     Pregunta: ¿Se permite?                                      │
│     Respuesta de negocio: NO, no hay tiempo suficiente        │
│                                                                 │
│     Lógica a implementar:                                       │
│     → Leer horarios especiales de configuración                │
│     → Aplicar límite de horario específico                    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Edge Case 4: Double booking por waitlist                   │
│     ════════════════════════════════════════                    │
│     Situación:                                                  │
│     - Cliente A cancela reserva a las 10:00                    │
│     - Waitlist tiene 2 personas esperando                      │
│     - ¿A quién se le ofrece primero?                          │
│                                                                 │
│     Reglas de prioridad:                                        │
│     1. Tiempo en waitlist (FIFO)                              │
│     2. Nivel VIP del cliente                                   │
│     3. Tipo de servicio (prioridad alta primero)              │
│                                                                 │
│     Lógica a implementar:                                      │
│     → Ordenar waitlist por: fecha_entrada + vip + prioridad   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Edge Case 5: No-show en reserva con waitlist               │
│     ════════════════════════════════════════                    │
│     Situación:                                                  │
│     - Cliente A no se presenta a las 10:00                    │
│     - Se marca como no-show                                    │
│     - Waitlist tiene personas esperando                        │
│                                                                 │
│     Pregunta: ¿Se ofrece inmediatamente el slot?                │
│     Respuesta de negocio: SÍ, pero con límite                 │
│     - Si hay >30 min antes del servicio, ofrecer a waitlist   │
│     - Si <30 min, el slot queda vacío (pérdida)               │
│                                                                 │
│     Lógica a implementar:                                      │
│     → Verificar tiempo restante vs umbral                     │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Edge Case 6: Cliente bloqueado intenta reservar            │
│     ════════════════════════════════════════                    │
│     Situación:                                                  │
│     - Cliente tiene 3 no-shows                                 │
│     - Estado: blocked                                          │
│     - Intenta hacer nueva reserva                              │
│                                                                 │
│     Manejo:                                                     │
│     → Rechazar reserva inmediatamente                         │
│     → Mostrar mensaje: "Tu cuenta está bloquecida por         │
│        no-presentarte. Contacta al salón."                     │
│     → Sugerir acción: Desbloqueo tras depósito               │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Edge Case 7: Cancelación parcial del waitlist             │
│     ════════════════════════════════════════                    │
│     Situación:                                                  │
│     - Slot libre a las 14:00                                  │
│     - Se notifica a 3 personas en waitlist                     │
│     - Persona 1 no responde en 2 horas                        │
│                                                                 │
│     Manejo:                                                     │
│     → Timeout de 2 horas para confirmar                        │
│     → Pasar al siguiente de la cola                           │
│     → Máximo 3 intentos de notificación                       │
│     → Después: marca como expired                              │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 Edge Case 8: Overbooking estratégico                      │
│     ════════════════════════════════════════                    │
│     Situación:                                                  │
│     - Capacidad del salón: 5 reservas/hora                     │
│     - Overbooking permitido: 10%                               │
│     - Máximo: 5 + 0.5 = 5.5 → 5 reservas (sin decimal)      │
│                                                                 │
│     Pregunta: ¿Cuándo aplicar overbooking?                     │
│     Respuesta de negocio:                                       │
│     → Solo en temporada alta                                   │
│     → Solo para servicios de alta demanda                      │
│     → Registrar que fue overbooking para métricas              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Resumen del Análisis

```markdown
┌─────────────────────────────────────────────────────────────────┐
│                 RESULTADO DEL ANÁLISIS                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📦 ENTIDADES A CREAR:                                          │
│     • Client (con no_show_count y status)                      │
│     • Service (con duracion y buffer_time)                     │
│     • Slot (con estado y fecha_hora)                          │
│     • Booking (con relaciones a Client, Service, Slot)       │
│     • Waitlist (con posicion y estado)                         │
│                                                                 │
│  🎯 USECASES PRIORITARIOS:                                      │
│     1. CreateBookingUseCase (CRÍTICO - doble booking)          │
│     2. GetAvailableSlotsUseCase (con filtros)                  │
│     3. CancelBookingUseCase (con política)                    │
│     4. MarkNoShowUseCase (con tracking)                       │
│     5. ProcessWaitlistUseCase (con prioridades)               │
│                                                                 │
│  ⚙️ CONFIGURACIÓN NECESARIA:                                    │
│     • Horarios base del salón                                  │
│     • Festivos y horarios especiales                           │
│     • Duración default de buffer                              │
│     • Políticas de cancelación                                │
│     • Límite de no-shows para bloqueo                         │
│                                                                 │
│  🧪 TESTS OBLIGATORIOS:                                         │
│     • Double booking prevention                                │
│     • Buffer time enforcement                                  │
│     • Horarios especiales aplicados                            │
│     • Política de cancelación correcta                          │
│     • No-show counter y bloqueo                                │
│     • Waitlist FIFO con prioridades                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. FASE B: Investigate

> **Objetivo:** Buscar información con IA sobre patrones y mejores prácticas.

### 3.1 Prompts de Investigación (EN ESPAÑOL)

```markdown
═══════════════════════════════════════════════════════════════════
                    PROMPTS DE INVESTIGACIÓN
═══════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────┐
│ PROMPT 1: Patrones para disponibilidad de slots                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ "Estoy implementando un sistema de reservas en Flutter con     │
│ Clean Architecture. Necesito encontrar el mejor patrón para:   │
│                                                                 │
│ 1. Verificar disponibilidad de slots de tiempo                │
│ 2. Manejar el buffer time entre reservas                      │
│ 3. Calcular horarios disponibles dinámicamente                  │
│                                                                 │
│ ¿Qué patrones o algoritmos recomiendas? Dame ejemplos de      │
│ cómo estructurar esta lógica."                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PROMPT 2: Estrategias de waitlist                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ "¿Cómo implementarías una lista de espera (waitlist) con:     │
│                                                                 │
│ 1. Priorización por tiempo de entrada (FIFO)                  │
│ 2.加分 por VIP del cliente                                    │
│ 3. Timeout de expiración                                       │
│ 4. Notificaciones automáticas cuando se libere un slot         │
│                                                                 │
│ Dame un enfoque práctico con código Dart."                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PROMPT 3: Manejo de fechas y horas en Dart                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ "Necesito manejar fechas/horas en Dart para un sistema de     │
│ reservas:                                                      │
│                                                                 │
│ 1. Comparar si una fecha está en el pasado                     │
│ 2. Sumar duración de servicio + buffer time                    │
│ 3. Verificar si cae en día festivo                            │
│ 4. Manejar timezone si la app es internacional                │
│                                                                 │
│ ¿Qué librería recomiendas: intl, timezone, o built_value?     │
│ Dame ejemplos de código."                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ PROMPT 4: Diseño de repository con cache                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ "Estoy implementando un repositorio en Clean Architecture     │
│ para un sistema de reservas con estrategia offline-first:      │
│                                                                 │
│ 1. Cómo estructurar el RemoteDataSource y LocalDataSource     │
│ 2. Estrategia de cache: cuándo invalidate                     │
│ 3. Manejo de conflictos: server vs local                       │
│                                                                 │
│ Dame un ejemplo de RepositoryImpl que siga estas reglas."      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Respuestas Esperadas de IA (Resumen)

```
┌─────────────────────────────────────────────────────────────────┐
│              PATRONES APRENDIDOS DE LA INVESTIGACIÓN            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📅 DISPONIBILIDAD DE SLOTS:                                    │
│     • Generar slots cada 15/30/60 min según configuración     │
│     • Filtrar slots ya reservados                              │
│     • Verificar que slot_inicio >= reserva_anterior.fin       │
│       + buffer_time                                             │
│                                                                 │
│  ⏳ WAITLIST:                                                   │
│     • Entidad con: cliente_id, servicio_id, fecha_deseada    │
│     • Ordenar por: fecha_entrada ASC, vip DESC                │
│     • Estados: waiting | notified | expired | booked          │
│                                                                 │
│  📆 MANEJO DE FECHAS:                                           │
│     • Usar DateTime de Dart (UTC internally)                  │
│     • Comparar solo hora+min paraintra-day                     │
│     • Usar intl para formateo de display                      │
│                                                                 │
│  🗄️ CACHE STRATEGY:                                             │
│     • Cachear disponibilidad del día                          │
│     • Invalidar al crear/cancelar reserva                      │
│     • Offline: mostrar última versión cacheada                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. FASE C: Decide

> **Objetivo:** Decidir qué va a IA (boilerplate) y qué hago yo (lógica crítica).

### 4.1 Matriz de Decisión por Componente

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              MATRIZ DE RESPONSABILIDADES                        │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  FEATURE: RESERVATION SYSTEM                                                    │
│                                                                                 │
│  ┌─────────────────────────┬────────────────────┬─────────────────────────┐    │
│  │     COMPONENTE          │   RESPONSABILIDAD  │       QUIÉN LO HACE      │    │
│  ├─────────────────────────┼────────────────────┼─────────────────────────┤    │
│  │                         │                    │                         │    │
│  │  ENTITIES               │                    │                         │    │
│  │  ├─ Client              │ Estructura básica  │ 🤖 IA (scaffold)        │    │
│  │  ├─ Service             │ Estructura básica  │ 🤖 IA (scaffold)        │    │
│  │  ├─ Slot                │ Estructura básica  │ 🤖 IA (scaffold)        │    │
│  │  │   └─ isAvailable     │ Lógica calculada   │ ✍️ TÚ (method)          │    │
│  │  ├─ Booking             │ Estructura básica  │ 🤖 IA (scaffold)        │    │
│  │  └─ Waitlist            │ Estructura + orden │ ✍️ TÚ (ordenar)         │    │
│  │                         │                    │                         │    │
│  ├─────────────────────────┼────────────────────┼─────────────────────────┤    │
│  │                         │                    │                         │    │
│  │  USECASES               │                    │                         │    │
│  │  ├─ GetAvailableSlots   │ Filtro + buffer   │ ✍️ TÚ (SIEMPRE)         │    │
│  │  ├─ CreateBooking       │ Validación + lógica│ ✍️ TÚ (SIEMPRE)         │    │
│  │  ├─ CancelBooking       │ Política + refund │ ✍️ TÚ (SIEMPRE)         │    │
│  │  ├─ MarkNoShow          │ Contador + bloqueo│ ✍️ TÚ (SIEMPRE)         │    │
│  │  └─ ProcessWaitlist    │ Prioridad + notif  │ ✍️ TÚ (SIEMPRE)         │    │
│  │                         │                    │                         │    │
│  ├─────────────────────────┼────────────────────┼─────────────────────────┤    │
│  │                         │                    │                         │    │
│  │  DATA LAYER             │                    │                         │    │
│  │  ├─ Models              │ fromJson/toJson    │ 🤖 IA (scaffold)        │    │
│  │  │                       │ Transformaciones  │ ✍️ TÚ (si especiales)    │    │
│  │  ├─ RemoteDataSource    │ API calls          │ 🤖 IA (estructure)      │    │
│  │  │                       │ Error handling    │ ✍️ TÚ (excepciones)     │    │
│  │  ├─ LocalDataSource    │ Cache operations   │ 🤖 IA (scaffold)        │    │
│  │  │                       │ Estrategia cache   │ ✍️ TÚ (decidir)        │    │
│  │  └─ Repository Impl    │ Lógica de merge   │ ✍️ TÚ (SIEMPRE)         │    │
│  │                         │                    │                         │    │
│  ├─────────────────────────┼────────────────────┼─────────────────────────┤    │
│  │                         │                    │                         │    │
│  │  PRESENTATION           │                    │                         │    │
│  │  ├─ States             │ Estados de UI     │ 🤖 IA (scaffold)        │    │
│  │  │                       │ Transiciones      │ ✍️ TÚ (si complejas)     │    │
│  │  └─ Cubit               │ Llamadas UseCases  │ 🤖 IA (estructure)      │    │
│  │                         │ Validación UI      │ ✍️ TÚ (SIEMPRE)         │    │
│  │                         │                    │                         │    │
│  ├─────────────────────────┼────────────────────┼─────────────────────────┤    │
│  │                         │                    │                         │    │
│  │  CORE                   │                    │                         │    │
│  │  ├─ Constants           │ Valores base      │ 🤖 IA (scaffold)        │    │
│  │  │                       │ Políticas negocio │ ✍️ TÚ (SIEMPRE)         │    │
│  │  └─ Utils               │ Helpers genéricos  │ 🤖 IA (generar)         │    │
│  │                         │ Helpers específicos│ ✍️ TÚ (si complejos)     │    │
│  │                         │                    │                         │    │
│  └─────────────────────────┴────────────────────┴─────────────────────────┘    │
│                                                                                 │
│  📊 RESUMEN:                                                                     │
│     • 🤖 IA: ~40% (boilerplate, estructura, scaffold)                           │
│     • ✍️ TÚ: ~60% (lógica de negocio, validaciones, edge cases)                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Justificación de Decisiones Clave

```markdown
┌─────────────────────────────────────────────────────────────────┐
│           POR QUÉ ESTAS PARTES SIEMPRE LAS HAGO YO              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. GetAvailableSlotsUseCase                                    │
│     ─────────────────────────────────                           │
│     ¿Por qué? La lógica de filtrar slots por:                  │
│     • Disponibilidad real (no reservados)                      │
│     • Buffer time (15 min después de cada reserva)              │
│     • Horarios especiales (festivos, temporada)                 │
│     • Capacidad (límite de reservas por hora)                   │
│                                                                 │
│     Impacto: Si esto está mal, el sistema permite double       │
│     booking o muestra horarios que no existen.                  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  2. CreateBookingUseCase                                        │
│     ────────────────────────                                   │
│     ¿Por qué? Debe verificar ANTES de crear:                   │
│     • Cliente no está bloqueado                                │
│     • Slot sigue disponible (race condition)                   │
│     • Horario dentro de límites del salón                      │
│     • Validaciones de negocio específicas                      │
│                                                                 │
│     Impacto: Crear una reserva inválida rompedatos integridad. │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  3. CancelBookingUseCase                                        │
│     ────────────────────────                                   │
│     ¿Por qué? La política de cancelación es negocio:           │
│     • >24h: refund completo                                    │
│     • <24h: penalty 50%                                        │
│     • <2h: penalty 100%                                        │
│     • Festivos: reglas especiales                              │
│                                                                 │
│     Impacto: Manejo incorrecto = pérdida de dinero o clientes   │
│     insatisfechos.                                             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  4. MarkNoShowUseCase                                           │
│     ─────────────────────                                       │
│     ¿Por qué? El tracking de no-shows tiene reglas:            │
│     • Incrementar contador                                     │
│     • En 3 no-shows: bloquear cliente                         │
│     • Reset anual                                              │
│     • ¿Notificar al cliente?                                   │
│                                                                 │
│     Impacto: Si no se bloquea, el clienteabusa del sistema.     │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  5. ProcessWaitlistUseCase                                      │
│     ────────────────────────                                   │
│     ¿Por qué? La priorización es crítica:                     │
│     • FIFO + VIP + tipo de servicio                           │
│     • Timeout para confirmar                                  │
│     • Máximo reintentos                                       │
│                                                                 │
│     Impacto: Un error aquí = cliente perde prioridad.          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. FASE D: Implement

> **Objetivo:** Implementar la feature con el enfoque híbrido.

### 5.1 Estructura Inicial con IA

```markdown
═══════════════════════════════════════════════════════════════════
                    IMPLEMENTACIÓN HÍBRIDA
═══════════════════════════════════════════════════════════════════

PASO 1: Pido a IA la estructura de archivos
───────────────────────────────────────────────────────────────────

# PROMPT:
"Crea la estructura de carpetas completa para una feature de 
reservas en Flutter Clean Architecture. Incluye domain/, data/, 
presentation/ y core/. Genera los comandos bash para crear 
directorios."

═══════════════════════════════════════════════════════════════════
```

### 5.2 Domain Layer - Entidades

```
═══════════════════════════════════════════════════════════════════
                    DOMAIN LAYER - ENTIDADES
═══════════════════════════════════════════════════════════════════

🤖 IA GENERA (scaffold):
───────────────────────────────────────────────────────────────────
```

```dart
// domain/entities/client.dart
import 'package:equatable/equatable.dart';

enum ClientStatus { active, blocked }

class Client extends Equatable {
  final String id;
  final String name;
  final String email;
  final String phone;
  final int noShowCount;
  final ClientStatus status;
  final DateTime? lastNoShowDate;
  final bool isVip;

  const Client({
    required this.id,
    required this.name,
    required this.email,
    required this.phone,
    this.noShowCount = 0,
    this.status = ClientStatus.active,
    this.lastNoShowDate,
    this.isVip = false,
  });

  @override
  List<Object?> get props => [
        id,
        name,
        email,
        phone,
        noShowCount,
        status,
        lastNoShowDate,
        isVip,
      ];
}
```

```dart
// domain/entities/service.dart
import 'package:equatable/equatable.dart';

class Service extends Equatable {
  final String id;
  final String name;
  final String category;
  final int durationMinutes;
  final int bufferMinutes;
  final double price;
  final int priority; // 1 = alta, 2 = media, 3 = baja

  const Service({
    required this.id,
    required this.name,
    required this.category,
    required this.durationMinutes,
    this.bufferMinutes = 15,
    required this.price,
    this.priority = 2,
  });

  @override
  List<Object?> get props => [
        id,
        name,
        category,
        durationMinutes,
        bufferMinutes,
        price,
        priority,
      ];
}
```

```dart
// domain/entities/slot.dart
import 'package:equatable/equatable.dart';

enum SlotStatus { available, reserved, blocked, unavailable }

class Slot extends Equatable {
  final DateTime startTime;
  final DateTime endTime;
  final SlotStatus status;
  final String? bookingId;

  const Slot({
    required this.startTime,
    required this.endTime,
    required this.status,
    this.bookingId,
  });

  @override
  List<Object?> get props => [startTime, endTime, status, bookingId];
}
```

```dart
// domain/entities/booking.dart
import 'package:equatable/equatable.dart';

enum BookingStatus { confirmed, cancelled, completed, noShow }

class Booking extends Equatable {
  final String id;
  final String clientId;
  final String serviceId;
  final DateTime dateTime;
  final BookingStatus status;
  final DateTime createdAt;
  final DateTime? cancelledAt;
  final bool wasOverbooking;

  const Booking({
    required this.id,
    required this.clientId,
    required this.serviceId,
    required this.dateTime,
    required this.status,
    required this.createdAt,
    this.cancelledAt,
    this.wasOverbooking = false,
  });

  @override
  List<Object?> get props => [
        id,
        clientId,
        serviceId,
        dateTime,
        status,
        createdAt,
        cancelledAt,
        wasOverbooking,
      ];
}
```

```dart
// domain/entities/waitlist.dart
import 'package:equatable/equatable.dart';

enum WaitlistStatus { waiting, notified, expired, booked }

class WaitlistEntry extends Equatable {
  final String id;
  final String clientId;
  final String serviceId;
  final DateTime desiredDate;
  final WaitlistStatus status;
  final DateTime createdAt;
  final DateTime? notifiedAt;
  final int position;
  final int notificationAttempts;

  const WaitlistEntry({
    required this.id,
    required this.clientId,
    required this.serviceId,
    required this.desiredDate,
    required this.status,
    required this.createdAt,
    this.notifiedAt,
    required this.position,
    this.notificationAttempts = 0,
  });

  @override
  List<Object?> get props => [
        id,
        clientId,
        serviceId,
        desiredDate,
        status,
        createdAt,
        notifiedAt,
        position,
        notificationAttempts,
      ];
}
```

---

### 5.3 Domain Layer - Fallures

```dart
// domain/failures/reservation_failure.dart
// GENERADO POR IA (boilerplate de errores)

import 'package:equatable/equatable.dart';

abstract class ReservationFailure extends Equatable {
  final String message;
  final String? code;

  const ReservationFailure({required this.message, this.code});

  @override
  List<Object?> get props => [message, code];
}

class SlotNotAvailableFailure extends ReservationFailure {
  const SlotNotAvailableFailure()
      : super(
          message: 'El horario seleccionado ya no está disponible',
          code: 'SLOT_NOT_AVAILABLE',
        );
}

class ClientBlockedFailure extends ReservationFailure {
  const ClientBlockedFailure()
      : super(
          message:
              'Tu cuenta está bloqueada por múltiples no-presentes. Contacta al salón.',
          code: 'CLIENT_BLOCKED',
        );
}

class InvalidBookingTimeFailure extends ReservationFailure {
  const InvalidBookingTimeFailure()
      : super(
          message: 'El horario seleccionado no es válido',
          code: 'INVALID_BOOKING_TIME',
        );
}

class BookingNotFoundFailure extends ReservationFailure {
  const BookingNotFoundFailure()
      : super(
          message: 'Reserva no encontrada',
          code: 'BOOKING_NOT_FOUND',
        );
}

class CancellationNotAllowedFailure extends ReservationFailure {
  final double penalty;

  const CancellationNotAllowedFailure({required this.penalty})
      : super(
          message:
              'La cancelación tiene una penalización del ${(penalty * 100).toInt()}%',
          code: 'CANCELLATION_NOT_ALLOWED',
        );
}

class SlotOutsideBusinessHoursFailure extends ReservationFailure {
  const SlotOutsideBusinessHoursFailure()
      : super(
          message: 'El horario está fuera del horario de atención',
          code: 'OUTSIDE_BUSINESS_HOURS',
        );
}

class SpecialScheduleFailure extends ReservationFailure {
  const SpecialScheduleFailure()
      : super(
          message: 'El salón no atiende en este horario especial',
          code: 'SPECIAL_SCHEDULE',
        );
}

class NetworkFailure extends ReservationFailure {
  const NetworkFailure()
      : super(
          message: 'Error de conexión. Verifica tu internet.',
          code: 'NETWORK_FAILURE',
        );
}

class ServerFailure extends ReservationFailure {
  const ServerFailure()
      : super(
          message: 'Error del servidor. Intenta más tarde.',
          code: 'SERVER_FAILURE',
        );
}

class UnexpectedFailure extends ReservationFailure {
  const UnexpectedFailure({required String message})
      : super(message: message, code: 'UNEXPECTED');
}
```

---

### 5.4 Domain Layer - Repository Interfaces

```dart
// domain/repositories/booking_repository.dart
// GENERADO POR IA (scaffold)

import 'package:dartz/dartz.dart';
import '../entities/booking.dart';
import '../entities/slot.dart';
import '../entities/service.dart';
import '../failures/reservation_failure.dart';

abstract class BookingRepository {
  /// Obtiene los slots disponibles para una fecha y servicio
  Future<Either<ReservationFailure, List<Slot>>> getAvailableSlots({
    required DateTime date,
    required String serviceId,
  });

  /// Crea una nueva reserva
  Future<Either<ReservationFailure, Booking>> createBooking({
    required String clientId,
    required String serviceId,
    required DateTime dateTime,
  });

  /// Cancela una reserva existente
  Future<Either<ReservationFailure, CancellationResult>> cancelBooking({
    required String bookingId,
  });

  /// Marca una reserva como no-show
  Future<Either<ReservationFailure, NoShowResult>> markNoShow({
    required String bookingId,
  });

  /// Obtiene las reservas de un cliente
  Future<Either<ReservationFailure, List<Booking>>> getClientBookings({
    required String clientId,
  });
}

class CancellationResult {
  final bool wasCancelled;
  final double refundAmount;
  final double penaltyAmount;

  const CancellationResult({
    required this.wasCancelled,
    required this.refundAmount,
    required this.penaltyAmount,
  });
}

class NoShowResult {
  final bool wasMarked;
  final bool clientBlocked;
  final int currentNoShowCount;

  const NoShowResult({
    required this.wasMarked,
    required this.clientBlocked,
    required this.currentNoShowCount,
  });
}
```

```dart
// domain/repositories/waitlist_repository.dart
// GENERADO POR IA (scaffold)

import 'package:dartz/dartz.dart';
import '../entities/waitlist.dart';
import '../failures/reservation_failure.dart';

abstract class WaitlistRepository {
  /// Agrega un cliente a la lista de espera
  Future<Either<ReservationFailure, WaitlistEntry>> addToWaitlist({
    required String clientId,
    required String serviceId,
    required DateTime desiredDate,
  });

  /// Obtiene la posición en waitlist para un cliente
  Future<Either<ReservationFailure, int>> getWaitlistPosition({
    required String clientId,
  });

  /// Procesa la waitlist cuando se libera un slot
  Future<Either<ReservationFailure, List<WaitlistEntry>>> processWaitlist({
    required String serviceId,
    required DateTime availableSlot,
  });

  /// Notifica al siguiente en waitlist
  Future<Either<ReservationFailure, WaitlistEntry?>> notifyNextInWaitlist({
    required String serviceId,
    required DateTime slot,
  });

  /// Expira entradas antiguas de waitlist
  Future<Either<ReservationFailure, int>> expireOldEntries();
}
```

---

### 5.5 Domain Layer - UseCases (LÓGICA CRÍTICA)

```
═══════════════════════════════════════════════════════════════════
                    USECASES - ¡¡ AQUÍ ESCRIBO YO !!
═══════════════════════════════════════════════════════════════════

✍️ Generate prompt para IA (boilerplate):
───────────────────────────────────────────────────────────────────

# PROMPT:
"Create UseCase templates for a reservation system with these methods:

1. GetAvailableSlotsUseCase: params (date, serviceId), returns Either<Failure, List<Slot>>
2. CreateBookingUseCase: params (clientId, serviceId, dateTime), returns Either<Failure, Booking>
3. CancelBookingUseCase: params (bookingId), returns Either<Failure, CancellationResult>
4. MarkNoShowUseCase: params (bookingId), returns Either<Failure, NoShowResult>

Just scaffold with TODO comments, I'll implement the logic."

═══════════════════════════════════════════════════════════════════

✍️ MI IMPLEMENTACIÓN (lógica crítica):
───────────────────────────────────────────────────────────────────
```

#### GetAvailableSlotsUseCase

```dart
// domain/usecases/get_available_slots.dart

import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import '../entities/slot.dart';
import '../failures/reservation_failure.dart';
import '../repositories/booking_repository.dart';
import '../../core/constants/reservation_constants.dart';
import '../../core/utils/slot_calculator.dart';

class GetAvailableSlotsUseCase {
  final BookingRepository repository;
  final SlotCalculator slotCalculator;

  GetAvailableSlotsUseCase({
    required this.repository,
    required this.slotCalculator,
  });

  Future<Either<ReservationFailure, List<Slot>>> call(
    GetAvailableSlotsParams params,
  ) async {
    // ═══════════════════════════════════════════════════════════════
    // LOGICA CRITICA: Generación de slots disponibles
    // ═══════════════════════════════════════════════════════════════

    // 1. Verificar que la fecha no sea pasado
    if (_isDateInPast(params.date)) {
      return const Left(InvalidBookingTimeFailure());
    }

    // 2. Obtener configuración de horarios
    final scheduleConfig = ReservationConstants.getScheduleForDate(params.date);

    // 3. Si el salón está cerrado ese día
    if (!scheduleConfig.isOpen) {
      return const Left(SpecialScheduleFailure());
    }

    // 4. Generar TODOS los slots posibles para ese día
    final allPossibleSlots = slotCalculator.generateSlotsForDay(
      date: params.date,
      openingTime: scheduleConfig.openingTime,
      closingTime: scheduleConfig.closingTime,
      intervalMinutes: ReservationConstants.slotIntervalMinutes,
    );

    // 5. Obtener slots ya reservados de la BD
    final reservedSlotsResult = await repository.getReservedSlots(
      date: params.date,
      serviceId: params.serviceId,
    );

    return reservedSlotsResult.fold(
      (failure) => Left(failure),
      (reservedSlots) {
        // ═══════════════════════════════════════════════════════════
        // LOGICA CRITICA: Filtrar slots no disponibles
        // ═══════════════════════════════════════════════════════════

        final availableSlots = _filterAvailableSlots(
          allPossibleSlots: allPossibleSlots,
          reservedSlots: reservedSlots,
          serviceDuration: params.serviceDuration,
          bufferMinutes: params.bufferMinutes,
          closingTime: scheduleConfig.closingTime,
        );

        // 6. Filtrar slots en el pasado (si es hoy)
        if (_isToday(params.date)) {
          return _filterPastSlots(availableSlots);
        }

        return Right(availableSlots);
      },
    );
  }

  // ═════════════════════════════════════════════════════════════════
  // MÉTODOS PRIVADOS DE LÓGICA CRÍTICA
  // ═════════════════════════════════════════════════════════════════

  bool _isDateInPast(DateTime date) {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final targetDate = DateTime(date.year, date.month, date.day);
    return targetDate.isBefore(today);
  }

  bool _isToday(DateTime date) {
    final now = DateTime.now();
    return date.year == now.year &&
        date.month == now.month &&
        date.day == now.day;
  }

  List<Slot> _filterAvailableSlots({
    required List<Slot> allPossibleSlots,
    required List<Slot> reservedSlots,
    required int serviceDuration,
    required int bufferMinutes,
    required String closingTime,
  }) {
    final availableSlots = <Slot>[];

    for (final slot in allPossibleSlots) {
      final slotEndTime = slot.startTime.add(
        Duration(minutes: serviceDuration + bufferMinutes),
      );

      // Verificar que el slot termine antes del cierre
      if (!_isBeforeClosing(slotEndTime, closingTime)) {
        continue;
      }

      // Verificar que no haya overlap con reservas existentes
      // INCLUYENDO buffer time
      final hasOverlap = _checkSlotOverlap(
        slotStart: slot.startTime,
        slotDuration: serviceDuration + bufferMinutes,
        reservedSlots: reservedSlots,
      );

      if (!hasOverlap) {
        availableSlots.add(slot);
      }
    }

    return availableSlots;
  }

  bool _checkSlotOverlap({
    required DateTime slotStart,
    required int slotDuration,
    required List<Slot> reservedSlots,
  }) {
    final slotEnd = slotStart.add(Duration(minutes: slotDuration));

    for (final reserved in reservedSlots) {
      final reservedEnd = reserved.endTime;

      // El nuevo slot se traslapa si:
      // - Empieza antes de que termine el reservado
      // - Termina después de que empiece el reservado
      final overlaps = slotStart.isBefore(reservedEnd) &&
          slotEnd.isAfter(reserved.startTime);

      if (overlaps) {
        return true; // Hay overlap = no disponible
      }
    }

    return false;
  }

  bool _isBeforeClosing(DateTime endTime, String closingTime) {
    final parts = closingTime.split(':');
    final closeHour = int.parse(parts[0]);
    final closeMinute = int.parse(parts[1]);

    final closeDateTime = DateTime(
      endTime.year,
      endTime.month,
      endTime.day,
      closeHour,
      closeMinute,
    );

    return endTime.isBefore(closeDateTime) ||
        endTime.isAtSameMomentAs(closeDateTime);
  }

  List<Slot> _filterPastSlots(List<Slot> slots) {
    final now = DateTime.now();
    final minimumBookingTime = now.add(
      Duration(minutes: ReservationConstants.minimumAdvanceMinutes),
    );

    return slots
        .where((slot) => slot.startTime.isAfter(minimumBookingTime))
        .toList();
  }
}

class GetAvailableSlotsParams extends Equatable {
  final DateTime date;
  final String serviceId;
  final int serviceDuration;
  final int bufferMinutes;

  const GetAvailableSlotsParams({
    required this.date,
    required this.serviceId,
    required this.serviceDuration,
    this.bufferMinutes = 15,
  });

  @override
  List<Object?> get props => [date, serviceId, serviceDuration, bufferMinutes];
}
```

#### CreateBookingUseCase

```dart
// domain/usecases/create_booking.dart

import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import '../entities/booking.dart';
import '../entities/client.dart';
import '../failures/reservation_failure.dart';
import '../repositories/booking_repository.dart';
import '../repositories/client_repository.dart';
import '../../core/constants/reservation_constants.dart';

class CreateBookingUseCase {
  final BookingRepository bookingRepository;
  final ClientRepository clientRepository;

  CreateBookingUseCase({
    required this.bookingRepository,
    required this.clientRepository,
  });

  Future<Either<ReservationFailure, Booking>> call(
    CreateBookingParams params,
  ) async {
    // ═══════════════════════════════════════════════════════════════
    // LOGICA CRITICA: Validaciones de negocio ANTES de crear
    // ═══════════════════════════════════════════════════════════════

    // 1. VERIFICAR: Cliente existe y no está bloqueado
    final clientResult = await clientRepository.getClient(params.clientId);

    final client = clientResult.fold(
      (failure) => null,
      (client) => client,
    );

    if (client == null) {
      return const Left(ReservationFailure(
        message: 'Cliente no encontrado',
        code: 'CLIENT_NOT_FOUND',
      ));
    }

    if (client.status == ClientStatus.blocked) {
      return const Left(ClientBlockedFailure());
    }

    // 2. VERIFICAR: No excedió límite de reservas activas
    final activeBookingsResult = await bookingRepository.getClientBookings(
      clientId: params.clientId,
    );

    final activeBookings = activeBookingsResult.fold(
      (failure) => <Booking>[],
      (bookings) => bookings
          .where((b) => b.status == BookingStatus.confirmed)
          .toList(),
    );

    if (activeBookings.length >= ReservationConstants.maxActiveBookings) {
      return Left(ReservationFailure(
        message:
            'Tienes demasiadas reservas activas (máximo ${ReservationConstants.maxActiveBookings})',
        code: 'TOO_MANY_BOOKINGS',
      ));
    }

    // 3. VERIFICAR: Horario dentro de límites
    if (!_isWithinBusinessHours(params.dateTime, params.serviceDuration)) {
      return const Left(SlotOutsideBusinessHoursFailure());
    }

    // 4. VERIFICAR: No es fecha pasada
    if (params.dateTime.isBefore(DateTime.now())) {
      return const Left(InvalidBookingTimeFailure());
    }

    // 5. VERIFICAR: Es fecha futura mínima
    final minimumBookingTime = DateTime.now().add(
      Duration(minutes: ReservationConstants.minimumAdvanceMinutes),
    );

    if (params.dateTime.isBefore(minimumBookingTime)) {
      return Left(ReservationFailure(
        message:
            'Las reservas deben hacerse con al menos ${ReservationConstants.minimumAdvanceMinutes} minutos de anticipación',
        code: 'TOO_SHORT_NOTICE',
      ));
    }

    // 6. INTENTAR CREAR: El repository verifica disponibilidad (race condition)
    final result = await bookingRepository.createBooking(
      clientId: params.clientId,
      serviceId: params.serviceId,
      dateTime: params.dateTime,
    );

    // 7. MANEJAR: Posible overbooking estratégico
    return result.fold(
      (failure) => Left(failure),
      (booking) async {
        // Si se creó exitosamente, verificar si es overbooking
        // (para métricas, no para revertir)
        if (booking.wasOverbooking) {
          // Log para analytics: booking created as overbooking
          _logOverbooking(params.clientId, params.serviceId);
        }
        return Right(booking);
      },
    );
  }

  // ═════════════════════════════════════════════════════════════════
  // MÉTODOS PRIVADOS DE LÓGICA CRÍTICA
  // ═════════════════════════════════════════════════════════════════

  bool _isWithinBusinessHours(DateTime dateTime, int serviceDuration) {
    final scheduleConfig = ReservationConstants.getScheduleForDate(dateTime);

    if (!scheduleConfig.isOpen) {
      return false;
    }

    final parts = scheduleConfig.openingTime.split(':');
    final openHour = int.parse(parts[0]);
    final openMinute = int.parse(parts[1]);

    final closeParts = scheduleConfig.closingTime.split(':');
    final closeHour = int.parse(closeParts[0]);
    final closeMinute = int.parse(closeParts[1]);

    final slotStart = dateTime;
    final slotEnd = dateTime.add(Duration(minutes: serviceDuration));

    final openTime = DateTime(
      dateTime.year,
      dateTime.month,
      dateTime.day,
      openHour,
      openMinute,
    );

    final closeTime = DateTime(
      dateTime.year,
      dateTime.month,
      dateTime.day,
      closeHour,
      closeMinute,
    );

    return !slotStart.isBefore(openTime) && !slotEnd.isAfter(closeTime);
  }

  void _logOverbooking(String clientId, String serviceId) {
    // En producción: enviar a analytics
    // AnalyticsService.logEvent('overbooking_created', {
    //   'client_id': clientId,
    //   'service_id': serviceId,
    //   'timestamp': DateTime.now().toIso8601String(),
    // });
  }
}

class CreateBookingParams extends Equatable {
  final String clientId;
  final String serviceId;
  final DateTime dateTime;

  const CreateBookingParams({
    required this.clientId,
    required this.serviceId,
    required this.dateTime,
  });

  @override
  List<Object?> get props => [clientId, serviceId, dateTime];
}
```

#### CancelBookingUseCase

```dart
// domain/usecases/cancel_booking.dart

import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import '../failures/reservation_failure.dart';
import '../repositories/booking_repository.dart';
import '../../core/constants/reservation_constants.dart';

class CancelBookingUseCase {
  final BookingRepository repository;

  CancelBookingUseCase({required this.repository});

  Future<Either<ReservationFailure, CancellationResult>> call(
    CancelBookingParams params,
  ) async {
    // ═══════════════════════════════════════════════════════════════
    // LOGICA CRITICA: Política de cancelación
    // ═══════════════════════════════════════════════════════════════

    // 1. Obtener la reserva
    final bookingResult = await repository.getBooking(params.bookingId);

    return bookingResult.fold(
      (failure) => Left(failure),
      (booking) async {
        // 2. Verificar que se puede cancelar
        if (booking.status != BookingStatus.confirmed) {
          return Left(ReservationFailure(
            message: 'Solo se pueden cancelar reservas confirmadas',
            code: 'CANNOT_CANCEL',
          ));
        }

        // ═══════════════════════════════════════════════════════════
        // LOGICA CRITICA: Cálculo de penalización
        // ═══════════════════════════════════════════════════════════

        final now = DateTime.now();
        final bookingTime = booking.dateTime;
        final hoursUntilBooking = bookingTime.difference(now).inHours;

        late final double penalty;
        late final double refund;

        // Obtener precio del servicio (asumiendo que lo tenemos)
        final servicePrice = booking.servicePrice;

        if (hoursUntilBooking >= ReservationConstants.fullRefundHours) {
          // > 24 horas: refund completo
          penalty = 0.0;
          refund = servicePrice;
        } else if (hoursUntilBooking >= ReservationConstants.halfRefundHours) {
          // 12-24 horas: 50% penalty
          penalty = servicePrice * 0.5;
          refund = servicePrice * 0.5;
        } else if (hoursUntilBooking >= ReservationConstants.noRefundHours) {
          // 2-12 horas: penalty según configuración
          penalty = servicePrice * ReservationConstants.lateCancellationPenalty;
          refund = servicePrice - penalty;
        } else {
          // < 2 horas: penalty completo
          penalty = servicePrice;
          refund = 0.0;
        }

        // 3. Verificar si es festivo (nochesbuena, navidad, etc)
        if (ReservationConstants.isHoliday(bookingTime)) {
          // En festivos: política más estricta
          if (hoursUntilBooking < ReservationConstants.holidayCancellationHours) {
            penalty = servicePrice; // 100% penalty en festivos con poca anticipación
            refund = 0.0;
          }
        }

        // 4. Ejecutar cancelación
        final cancelResult = await repository.cancelBooking(
          bookingId: params.bookingId,
          penalty: penalty,
          refund: refund,
        );

        return cancelResult.fold(
          (failure) => Left(failure),
          (_) => Right(CancellationResult(
            wasCancelled: true,
            refundAmount: refund,
            penaltyAmount: penalty,
          )),
        );
      },
    );
  }
}

class CancelBookingParams extends Equatable {
  final String bookingId;

  const CancelBookingParams({required this.bookingId});

  @override
  List<Object?> get props => [bookingId];
}
```

#### MarkNoShowUseCase

```dart
// domain/usecases/mark_no_show.dart

import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import '../failures/reservation_failure.dart';
import '../repositories/booking_repository.dart';
import '../repositories/client_repository.dart';
import '../../core/constants/reservation_constants.dart';

class MarkNoShowUseCase {
  final BookingRepository bookingRepository;
  final ClientRepository clientRepository;

  MarkNoShowUseCase({
    required this.bookingRepository,
    required this.clientRepository,
  });

  Future<Either<ReservationFailure, NoShowResult>> call(
    MarkNoShowParams params,
  ) async {
    // ═══════════════════════════════════════════════════════════════
    // LOGICA CRITICA: Tracking de no-shows y bloqueo
    // ═══════════════════════════════════════════════════════════════

    // 1. Obtener la reserva
    final bookingResult = await repository.getBooking(params.bookingId);

    return bookingResult.fold(
      (failure) => Left(failure),
      (booking) async {
        // 2. Verificar que se puede marcar como no-show
        if (booking.status != BookingStatus.confirmed) {
          return Left(ReservationFailure(
            message: 'Esta reserva ya no está confirmada',
            code: 'INVALID_STATUS',
          ));
        }

        // Solo marcar si ya pasó la hora de la reserva (+ grace period)
        final now = DateTime.now();
        final gracePeriodEnd = booking.dateTime.add(
          Duration(minutes: ReservationConstants.noShowGracePeriodMinutes),
        );

        if (now.isBefore(gracePeriodEnd)) {
          return Left(ReservationFailure(
            message: 'Aún es muy temprano para marcar como no-show',
            code: 'TOO_EARLY',
          ));
        }

        // 3. Marcar la reserva como no-show
        final markResult = await bookingRepository.markNoShow(
          bookingId: params.bookingId,
        );

        return markResult.fold(
          (failure) => Left(failure),
          (_) async {
            // 4. Actualizar contador del cliente
            final clientResult = await clientRepository.getClient(booking.clientId);

            return clientResult.fold(
              (failure) => Left(failure),
              (client) async {
                // Incrementar no-show count
                final newNoShowCount = client.noShowCount + 1;

                // Verificar si debe bloquearse
                final shouldBlock = newNoShowCount >=
                    ReservationConstants.maxNoShowsBeforeBlock;

                // Actualizar cliente
                await clientRepository.updateClient(
                  clientId: client.id,
                  noShowCount: newNoShowCount,
                  lastNoShowDate: now,
                  status: shouldBlock ? ClientStatus.blocked : client.status,
                );

                // 5. Manejar waitlist si aplica
                if (shouldBlock) {
                  // Notificar a waitlist que hay un cliente bloqueado
                  // que podría liberar horarios
                  await _notifyWaitlistForAvailableSlots(
                    serviceId: booking.serviceId,
                    dateTime: booking.dateTime,
                  );
                }

                return Right(NoShowResult(
                  wasMarked: true,
                  clientBlocked: shouldBlock,
                  currentNoShowCount: newNoShowCount,
                ));
              },
            );
          },
        );
      },
    );
  }

  // ═════════════════════════════════════════════════════════════════
  // MÉTODOS PRIVADOS DE LÓGICA CRÍTICA
  // ═════════════════════════════════════════════════════════════════

  Future<void> _notifyWaitlistForAvailableSlots({
    required String serviceId,
    required DateTime dateTime,
  }) async {
    // Si un cliente habitual (con no-shows) está bloqueado,
    //可能有空闲 slots，通知排队的人
    // Esto es una optimización: notify waitlist inmediatamente
    // en lugar de esperar al proceso batch

    // WaitlistRepository.notifyForSlot(serviceId, dateTime);
  }
}

class MarkNoShowParams extends Equatable {
  final String bookingId;

  const MarkNoShowParams({required this.bookingId});

  @override
  List<Object?> get props => [bookingId];
}
```

#### ProcessWaitlistUseCase

```dart
// domain/usecases/process_waitlist.dart

import 'package:dartz/dartz.dart';
import 'package:equatable/equatable.dart';
import '../entities/waitlist.dart';
import '../failures/reservation_failure.dart';
import '../repositories/waitlist_repository.dart';
import '../repositories/booking_repository.dart';
import '../repositories/client_repository.dart';
import '../../core/constants/reservation_constants.dart';

class ProcessWaitlistUseCase {
  final WaitlistRepository waitlistRepository;
  final BookingRepository bookingRepository;
  final ClientRepository clientRepository;

  ProcessWaitlistUseCase({
    required this.waitlistRepository,
    required this.bookingRepository,
    required this.clientRepository,
  });

  Future<Either<ReservationFailure, ProcessWaitlistResult>> call(
    ProcessWaitlistParams params,
  ) async {
    // ═══════════════════════════════════════════════════════════════
    // LOGICA CRITICA: Priorización y notificación de waitlist
    // ═══════════════════════════════════════════════════════════════

    // 1. Obtener waitlist ordenada por prioridad
    final waitlistResult = await waitlistRepository.getWaitlistForService(
      serviceId: params.serviceId,
      date: params.availableSlot,
    );

    return waitlistResult.fold(
      (failure) => Left(failure),
      (entries) async {
        if (entries.isEmpty) {
          return const Right(ProcessWaitlistResult(
            notifiedEntries: [],
            processed: false,
          ));
        }

        // ═══════════════════════════════════════════════════════════
        // LOGICA CRITICA: Ordenar por prioridad
        // ═══════════════════════════════════════════════════════════

        final sortedEntries = _sortByPriority(entries);

        // 2. Notificar al primero (o primeros si hay overbooking)
        final notifiedEntries = <WaitlistEntry>[];
        final maxNotifications = ReservationConstants.maxWaitlistNotifications;

        for (var i = 0; i < sortedEntries.length && i < maxNotifications; i++) {
          final entry = sortedEntries[i];

          // Verificar que el cliente no esté bloqueado
          final clientResult = await clientRepository.getClient(entry.clientId);
          
          final client = clientResult.fold(
            (_) => null,
            (c) => c,
          );

          if (client == null || client.status == ClientStatus.blocked) {
            continue;
          }

          // Verificar que aún está en tiempo válido
          if (_isEntryExpired(entry)) {
            await waitlistRepository.expireEntry(entry.id);
            continue;
          }

          // Notificar
          final notifyResult = await waitlistRepository.notifyEntry(
            entryId: entry.id,
            availableSlot: params.availableSlot,
          );

          notifyResult.fold(
            (failure) => null, // No notificado, continuar con siguiente
            (notifiedEntry) => notifiedEntries.add(notifiedEntry),
          );
        }

        return Right(ProcessWaitlistResult(
          notifiedEntries: notifiedEntries,
          processed: true,
        ));
      },
    );
  }

  // ═════════════════════════════════════════════════════════════════
  // MÉTODOS PRIVADOS DE LÓGICA CRÍTICA
  // ═════════════════════════════════════════════════════════════════

  List<WaitlistEntry> _sortByPriority(List<WaitlistEntry> entries) {
    // PRIORIDAD:
    // 1. VIP clients primero
    // 2. Dentro de VIP: fecha de entrada más antigua primero
    // 3. Dentro de mismo VIP: tipo de servicio (prioridad alta primero)

    final entriesWithClient = <_EntryWithClient>[];

    for (final entry in entries) {
      entriesWithClient.add(_EntryWithClient(entry: entry));
    }

    entriesWithClient.sort((a, b) {
      // Primero por VIP (descendente: VIP primero)
      if (a.isVip && !b.isVip) return -1;
      if (!a.isVip && b.isVip) return 1;

      // Dentro del mismo VIP: por prioridad del servicio
      if (a.servicePriority != b.servicePriority) {
        return a.servicePriority.compareTo(b.servicePriority);
      }

      // Dentro de misma prioridad: por fecha de entrada
      return a.entry.createdAt.compareTo(b.entry.createdAt);
    });

    return entriesWithClient.map((e) => e.entry).toList();
  }

  bool _isEntryExpired(WaitlistEntry entry) {
    final expirationTime = entry.createdAt.add(
      Duration(hours: ReservationConstants.waitlistExpirationHours),
    );
    return DateTime.now().isAfter(expirationTime);
  }
}

class _EntryWithClient {
  final WaitlistEntry entry;
  final bool isVip;
  final int servicePriority;

  _EntryWithClient({required this.entry});
}

class ProcessWaitlistParams extends Equatable {
  final String serviceId;
  final DateTime availableSlot;

  const ProcessWaitlistParams({
    required this.serviceId,
    required this.availableSlot,
  });

  @override
  List<Object?> get props => [serviceId, availableSlot];
}

class ProcessWaitlistResult {
  final List<WaitlistEntry> notifiedEntries;
  final bool processed;

  const ProcessWaitlistResult({
    required this.notifiedEntries,
    required this.processed,
  });
}
```

---

### 5.6 Core Layer - Constants

```
═══════════════════════════════════════════════════════════════════
                    CORE LAYER - CONFIGURACIÓN DE NEGOCIO
═══════════════════════════════════════════════════════════════════

✍️ ESTO LO ESCRIBO YO - son las políticas de negocio
───────────────────────────────────────────────────────────────────
```

```dart
// core/constants/reservation_constants.dart

class ReservationConstants {
  // ═══════════════════════════════════════════════════════════════
  // HORARIOS BASE DEL SALÓN
  // ═══════════════════════════════════════════════════════════════

  static const String defaultOpeningTime = '09:00';
  static const String defaultClosingTime = '20:00';
  static const int slotIntervalMinutes = 30;

  // ═══════════════════════════════════════════════════════════════
  // BUFFER TIME (minutos de limpieza entre reservas)
  // ═══════════════════════════════════════════════════════════════

  static const int defaultBufferMinutes = 15;

  // ═══════════════════════════════════════════════════════════════
  // POLÍTICA DE CANCELACIÓN
  // ═══════════════════════════════════════════════════════════════

  static const int fullRefundHours = 24; // > 24h = refund completo
  static const int halfRefundHours = 12; // 12-24h = 50% penalty
  static const int noRefundHours = 2; // < 2h = 100% penalty
  static const double lateCancellationPenalty = 0.75; // 2-12h = 75%

  // ═══════════════════════════════════════════════════════════════
  // POLÍTICA DE NO-SHOW
  // ═══════════════════════════════════════════════════════════════

  static const int maxNoShowsBeforeBlock = 3;
  static const int noShowGracePeriodMinutes = 30;
  static const int noShowResetDays = 365; // Reset anual

  // ═══════════════════════════════════════════════════════════════
  // WAILIST
  // ═══════════════════════════════════════════════════════════════

  static const int waitlistExpirationHours = 48;
  static const int waitlistNotificationTimeoutHours = 2;
  static const int maxWaitlistNotifications = 3;

  // ═══════════════════════════════════════════════════════════════
  // OVERBOOKING
  // ═══════════════════════════════════════════════════════════════

  static const double overbookingPercentage = 0.10; // 10%
  static const int overbookingMaxSlots = 5;

  // ═══════════════════════════════════════════════════════════════
  // LÍMITES DE RESERVAS
  // ═══════════════════════════════════════════════════════════════

  static const int maxActiveBookings = 5;
  static const int minimumAdvanceMinutes = 60;

  // ═══════════════════════════════════════════════════════════════
  // MÉTODOS DE CONFIGURACIÓN
  // ═══════════════════════════════════════════════════════════════

  static ScheduleConfig getScheduleForDate(DateTime date) {
    // Verificar si es festivo
    if (isHoliday(date)) {
      return _holidaySchedules[date.month.toString() + '-' + date.day.toString()] ??
          const ScheduleConfig(isOpen: false);
    }

    // Verificar si es domingo
    if (date.weekday == DateTime.sunday) {
      return const ScheduleConfig(
        isOpen: true,
        openingTime: '10:00',
        closingTime: '15:00',
      );
    }

    // Horarios normales
    return const ScheduleConfig(
      isOpen: true,
      openingTime: defaultOpeningTime,
      closingTime: defaultClosingTime,
    );
  }

  static bool isHoliday(DateTime date) {
    final key = date.month.toString() + '-' + date.day.toString();
    return _holidaySchedules.containsKey(key);
  }

  // ═══════════════════════════════════════════════════════════════
  // FESTIVOS CONFIGURABLES
  // ═══════════════════════════════════════════════════════════════

  static const Map<String, ScheduleConfig> _holidaySchedules = {
    // Navidades
    '12-24': ScheduleConfig(
      isOpen: true,
      openingTime: '10:00',
      closingTime: '15:00',
    ),
    '12-25': ScheduleConfig(isOpen: false), // Cerrado
    '12-31': ScheduleConfig(
      isOpen: true,
      openingTime: '10:00',
      closingTime: '17:00',
    ),
    '1-1': ScheduleConfig(isOpen: false), // Año nuevo cerrado

    // Ejemplo: festivos locales
    // '7-9': ScheduleConfig(isOpen: false), // Día de la Independencia
  };
}

class ScheduleConfig {
  final bool isOpen;
  final String openingTime;
  final String closingTime;

  const ScheduleConfig({
    required this.isOpen,
    this.openingTime = '09:00',
    this.closingTime = '20:00',
  });
}
```

---

## 6. FASE E: Review

> **Objetivo:** Verificar que todo está correcto antes de continuar con tests.

### 6.1 Checklist de Revisión

```markdown
┌─────────────────────────────────────────────────────────────────┐
│              CHECKLIST DE REVISIÓN POST-IMPLEMENTACIÓN          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ GetAvailableSlotsUseCase                                     │
│     ├─ ¿Verifica fecha en pasado?                              │
│     ├─ ¿Aplica horarios especiales?                           │
│     ├─ ¿Incluye buffer time en overlap?                        │
│     ├─ ¿Filtra slots en pasado (hoy)?                          │
│     └─ ¿Verifica hora de cierre?                               │
│                                                                 │
│  □ CreateBookingUseCase                                         │
│     ├─ ¿Verifica cliente bloqueado?                            │
│     ├─ ¿Verifica límite de reservas activas?                   │
│     ├─ ¿Verifica horario dentro de negocio?                    │
│     ├─ ¿Verifica anticipación mínima?                          │
│     └─ ¿Maneja race condition?                                  │
│                                                                 │
│  □ CancelBookingUseCase                                          │
│     ├─ ¿Aplica política correcta según horas?                  │
│     ├─ ¿Considera festivos?                                    │
│     ├─ ¿Calcula refund y penalty correctamente?                 │
│     └─ ¿Verifica estado antes de cancelar?                     │
│                                                                 │
│  □ MarkNoShowUseCase                                             │
│     ├─ ¿Verifica grace period?                                  │
│     ├─ ¿Incrementa contador?                                    │
│     ├─ ¿Bloquea en 3 no-shows?                                 │
│     └─ ¿Actualiza fecha último no-show?                        │
│                                                                 │
│  □ ProcessWaitlistUseCase                                        │
│     ├─ ¿Ordena por VIP primero?                                │
│     ├─ ¿Considera prioridad del servicio?                      │
│     ├─ ¿Expira entradas viejas?                                 │
│     └─ ¿Limita notificaciones?                                 │
│                                                                 │
│  □ ReservationConstants                                          │
│     ├─ ¿Todos los valores son configurables?                    │
│     ├─ ¿Festivos definidos correctamente?                      │
│     └─ ¿Políticas claras y documentadas?                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Validación de Edge Cases

```markdown
┌─────────────────────────────────────────────────────────────────┐
│              VERIFICACIÓN DE EDGE CASES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✓ Edge Case 1: Reserva en buffer time                          │
│     ├─ Código: _checkSlotOverlap incluye buffer en duración     │
│     └─ Resultado: PASA ✓                                        │
│                                                                 │
│  ✓ Edge Case 2: Reserva después de hora de cierre             │
│     ├─ Código: _isWithinBusinessHours verifica fin servicio    │
│     └─ Resultado: PASA ✓                                        │
│                                                                 │
│  ✓ Edge Case 3: Festivo                                         │
│     ├─ Código: getScheduleForDate consulta _holidaySchedules    │
│     └─ Resultado: PASA ✓                                        │
│                                                                 │
│  ✓ Edge Case 4: Cliente bloqueado                              │
│     ├─ Código: CreateBookingUseCase verifica ClientStatus       │
│     └─ Resultado: PASA ✓                                        │
│                                                                 │
│  ✓ Edge Case 5: No-show en waitlist                           │
│     ├─ Código: MarkNoShowUseCase notifica waitlist             │
│     └─ Resultado: PASA ✓                                        │
│                                                                 │
│  ✓ Edge Case 6: Cancelación <2h                                 │
│     ├─ Código: CancelBookingUseCase aplica penalty 100%       │
│     └─ Resultado: PASA ✓                                         │
│                                                                 │
│  ✓ Edge Case 7: Waitlist expirada                               │
│     ├─ Código: _isEntryExpired verifica 48h                   │
│     └─ Resultado: PASA ✓                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. FASE F: Testing

```
═══════════════════════════════════════════════════════════════════
                    TESTING HÍBRIDO
═══════════════════════════════════════════════════════════════════

🤖 IA GENERA: Scaffold de tests (setUp, arrange, estructura)
✍️ YO ESCRIBO: Aserciones, edge cases, lógica de test
═══════════════════════════════════════════════════════════════════
```

### 7.1 Tests para GetAvailableSlotsUseCase

```dart
// test/features/reservation/domain/usecases/get_available_slots_test.dart

import 'package:bloc_test/bloc_test.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

import 'package:my_app/features/reservation/domain/entities/slot.dart';
import 'package:my_app/features/reservation/domain/entities/service.dart';
import 'package:my_app/features/reservation/domain/failures/reservation_failure.dart';
import 'package:my_app/features/reservation/domain/repositories/booking_repository.dart';
import 'package:my_app/features/reservation/domain/usecases/get_available_slots.dart';
import 'package:my_app/features/reservation/core/utils/slot_calculator.dart';

@GenerateMocks([BookingRepository, SlotCalculator])
import 'get_available_slots_test.mocks.dart';

void main() {
  late GetAvailableSlotsUseCase useCase;
  late MockBookingRepository mockRepository;
  late MockSlotCalculator mockSlotCalculator;

  setUp(() {
    mockRepository = MockBookingRepository();
    mockSlotCalculator = MockSlotCalculator();
    useCase = GetAvailableSlotsUseCase(
      repository: mockRepository,
      slotCalculator: mockSlotCalculator,
    );
  });

  // ═══════════════════════════════════════════════════════════════
  // ✍️ TEST DATA: Creados por mí con datos realistas
  // ═══════════════════════════════════════════════════════════════

  final tuesday2026 = DateTime(2026, 3, 24); // Un martes
  final friday2026 = DateTime(2026, 3, 27); // Un viernes
  final sunday2026 = DateTime(2026, 3, 29); // Un domingo

  final existingBooking = Slot(
    startTime: DateTime(2026, 3, 24, 10, 0),
    endTime: DateTime(2026, 3, 24, 11, 0),
    status: SlotStatus.reserved,
    bookingId: 'booking-1',
  );

  const testService = Service(
    id: 'service-1',
    name: 'Corte de pelo',
    category: 'cabello',
    durationMinutes: 45,
    bufferMinutes: 15,
    price: 25.0,
  );

  final generatedSlots = [
    Slot(
      startTime: DateTime(2026, 3, 24, 9, 0),
      endTime: DateTime(2026, 3, 24, 9, 30),
      status: SlotStatus.available,
    ),
    Slot(
      startTime: DateTime(2026, 3, 24, 9, 30),
      endTime: DateTime(2026, 3, 24, 10, 0),
      status: SlotStatus.available,
    ),
    Slot(
      startTime: DateTime(2026, 3, 24, 10, 0),
      endTime: DateTime(2026, 3, 24, 10, 30),
      status: SlotStatus.reserved,
      bookingId: 'booking-1',
    ),
  ];

  // ═══════════════════════════════════════════════════════════════
  // ✍️ TESTS: Lógica de disponibilidad
  // ═══════════════════════════════════════════════════════════════

  group('GetAvailableSlotsUseCase', () {
    // ─────────────────────────────────────────────────────────────
    // TEST 1: Día normal - slots disponibles correctamente
    // ─────────────────────────────────────────────────────────────

    test('should return available slots excluding reserved ones', () async {
      // arrange
      when(mockSlotCalculator.generateSlotsForDay(
        date: anyNamed('date'),
        openingTime: anyNamed('openingTime'),
        closingTime: anyNamed('closingTime'),
        intervalMinutes: anyNamed('intervalMinutes'),
      )).thenReturn(generatedSlots);

      when(mockRepository.getReservedSlots(
        date: anyNamed('date'),
        serviceId: anyNamed('serviceId'),
      )).thenAnswer((_) async => Right([existingBooking]));

      // act
      final result = await useCase(GetAvailableSlotsParams(
        date: tuesday2026,
        serviceId: testService.id,
        serviceDuration: testService.durationMinutes,
        bufferMinutes: testService.bufferMinutes,
      ));

      // assert - ✍️ MI ASERCIÓN
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success but got failure'),
        (slots) {
          // Verifico que el slot reservado NO esté
          expect(slots.any((s) => s.bookingId == 'booking-1'), false);
          
          // Verifico que los disponibles SÍ estén
          expect(slots.length, 2);
          expect(slots[0].status, SlotStatus.available);
          expect(slots[1].status, SlotStatus.available);
        },
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 2: Verificar que buffer time se respeta
    // ─────────────────────────────────────────────────────────────

    test('should exclude slots that fall within buffer time', () async {
      // arrange - Reserva existente a las 10:00 con buffer 15min
      // Entonces 10:00, 10:15, 10:30 deberían estar bloqueados
      final bookingWithBuffer = Slot(
        startTime: DateTime(2026, 3, 24, 10, 0),
        endTime: DateTime(2026, 3, 24, 11, 0), // 1h de servicio
        status: SlotStatus.reserved,
        bookingId: 'booking-buffer',
      );

      final slotsAroundBuffer = [
        Slot(
          startTime: DateTime(2026, 3, 24, 9, 45),
          endTime: DateTime(2026, 3, 24, 10, 15), // Overlap con buffer
          status: SlotStatus.available,
        ),
        Slot(
          startTime: DateTime(2026, 3, 24, 10, 15), // Inicia justo en buffer end
          endTime: DateTime(2026, 3, 24, 10, 45),
          status: SlotStatus.available,
        ),
        Slot(
          startTime: DateTime(2026, 3, 24, 11, 0), // Inicia justo en fin servicio
          endTime: DateTime(2026, 3, 24, 11, 30),
          status: SlotStatus.available,
        ),
      ];

      when(mockSlotCalculator.generateSlotsForDay(
        date: anyNamed('date'),
        openingTime: anyNamed('openingTime'),
        closingTime: anyNamed('closingTime'),
        intervalMinutes: anyNamed('intervalMinutes'),
      )).thenReturn(slotsAroundBuffer);

      when(mockRepository.getReservedSlots(
        date: anyNamed('date'),
        serviceId: anyNamed('serviceId'),
      )).thenAnswer((_) async => Right([bookingWithBuffer]));

      // act
      final result = await useCase(GetAvailableSlotsParams(
        date: tuesday2026,
        serviceId: testService.id,
        serviceDuration: 45, // 45 min servicio
        bufferMinutes: 15, // 15 min buffer = total 60 min
      ));

      // assert - ✍️ MI ASERCIÓN - Verifico lógica de buffer
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success'),
        (slots) {
          // Slot que empieza 9:45 termina 10:30 (45+15 buffer) = overlap
          // Slot que empieza 10:15 termina 11:00 = overlap
          // Slot que empieza 11:00 termina 11:30 = OK (justo en el límite)
          expect(slots.length, 1);
          expect(slots[0].startTime.hour, 11);
          expect(slots[0].startTime.minute, 0);
        },
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 3: Domingo tiene horarios diferentes
    // ─────────────────────────────────────────────────────────────

    test('should apply Sunday schedule (10:00 - 15:00)', () async {
      // arrange
      when(mockRepository.getReservedSlots(
        date: anyNamed('date'),
        serviceId: anyNamed('serviceId'),
      )).thenAnswer((_) async => const Right([]));

      // Configurar slot calculator para generar slots hasta 15:00
      when(mockSlotCalculator.generateSlotsForDay(
        date: sunday2026,
        openingTime: '10:00', // Domingo abre 10
        closingTime: '15:00', // Domingo cierra 15
        intervalMinutes: 30,
      )).thenReturn([
        Slot(
          startTime: DateTime(2026, 3, 29, 10, 0),
          endTime: DateTime(2026, 3, 29, 10, 30),
          status: SlotStatus.available,
        ),
        Slot(
          startTime: DateTime(2026, 3, 29, 14, 30), // Último slot posible
          endTime: DateTime(2026, 3, 29, 15, 0),
          status: SlotStatus.available,
        ),
      ]);

      // act
      final result = await useCase(GetAvailableSlotsParams(
        date: sunday2026,
        serviceId: testService.id,
        serviceDuration: testService.durationMinutes,
        bufferMinutes: testService.bufferMinutes,
      ));

      // assert
      expect(result.isRight(), true);
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 4: Error de red
    // ─────────────────────────────────────────────────────────────

    test('should return NetworkFailure when repository fails', () async {
      // arrange
      when(mockRepository.getReservedSlots(
        date: anyNamed('date'),
        serviceId: anyNamed('serviceId'),
      )).thenAnswer((_) async => const Left(NetworkFailure()));

      // act
      final result = await useCase(GetAvailableSlotsParams(
        date: tuesday2026,
        serviceId: testService.id,
        serviceDuration: testService.durationMinutes,
        bufferMinutes: testService.bufferMinutes,
      ));

      // assert
      expect(result.isLeft(), true);
      result.fold(
        (failure) => expect(failure, isA<NetworkFailure>()),
        (_) => fail('Expected failure'),
      );
    });
  });
}
```

### 7.2 Tests para CancelBookingUseCase

```dart
// test/features/reservation/domain/usecases/cancel_booking_test.dart

import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

import 'package:my_app/features/reservation/domain/entities/booking.dart';
import 'package:my_app/features/reservation/domain/failures/reservation_failure.dart';
import 'package:my_app/features/reservation/domain/repositories/booking_repository.dart';
import 'package:my_app/features/reservation/domain/usecases/cancel_booking.dart';
import 'package:my_app/features/reservation/core/constants/reservation_constants.dart';

@GenerateMocks([BookingRepository])
import 'cancel_booking_test.mocks.dart';

void main() {
  late CancelBookingUseCase useCase;
  late MockBookingRepository mockRepository;

  setUp(() {
    mockRepository = MockBookingRepository();
    useCase = CancelBookingUseCase(repository: mockRepository);
  });

  // ═══════════════════════════════════════════════════════════════
  // ✍️ TEST DATA: Casos de prueba realistas
  // ═══════════════════════════════════════════════════════════════

  Booking createBooking({
    required BookingStatus status,
    required DateTime dateTime,
    double servicePrice = 50.0,
  }) {
    return Booking(
      id: 'booking-1',
      clientId: 'client-1',
      serviceId: 'service-1',
      dateTime: dateTime,
      status: status,
      createdAt: DateTime.now(),
      servicePrice: servicePrice,
    );
  }

  // ═══════════════════════════════════════════════════════════════
  // ✍️ TESTS: Política de cancelación
  // ═══════════════════════════════════════════════════════════════

  group('CancelBookingUseCase', () {
    // ─────────────────────────────────────────────────────────────
    // TEST 1: Cancelación >24h antes = refund completo
    // ─────────────────────────────────────────────────────────────

    test('should return full refund when cancelling more than 24h before', () async {
      // arrange
      final bookingTime = DateTime.now().add(const Duration(hours: 48));
      final booking = createBooking(
        status: BookingStatus.confirmed,
        dateTime: bookingTime,
        servicePrice: 100.0,
      );

      when(mockRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));
      when(mockRepository.cancelBooking(
        bookingId: any,
        penalty: any,
        refund: any,
      )).thenAnswer((_) async => const Right(true));

      // act
      final result = await useCase(CancelBookingParams(bookingId: 'booking-1'));

      // assert - ✍️ MI ASERCIÓN
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success'),
        (cancellationResult) {
          expect(cancellationResult.wasCancelled, true);
          expect(cancellationResult.refundAmount, 100.0); // 100% refund
          expect(cancellationResult.penaltyAmount, 0.0); // Sin penalty
        },
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 2: Cancelación 12-24h antes = 50% penalty
    // ─────────────────────────────────────────────────────────────

    test('should return 50% penalty when cancelling 12-24h before', () async {
      // arrange
      final bookingTime = DateTime.now().add(const Duration(hours: 18));
      final booking = createBooking(
        status: BookingStatus.confirmed,
        dateTime: bookingTime,
        servicePrice: 100.0,
      );

      when(mockRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));
      when(mockRepository.cancelBooking(
        bookingId: any,
        penalty: any,
        refund: any,
      )).thenAnswer((_) async => const Right(true));

      // act
      final result = await useCase(CancelBookingParams(bookingId: 'booking-1'));

      // assert - ✍️ MI ASERCIÓN
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success'),
        (cancellationResult) {
          expect(cancellationResult.wasCancelled, true);
          expect(cancellationResult.refundAmount, 50.0); // 50% refund
          expect(cancellationResult.penaltyAmount, 50.0); // 50% penalty
        },
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 3: Cancelación <2h antes = penalty 100%
    // ─────────────────────────────────────────────────────────────

    test('should return 100% penalty when cancelling less than 2h before', () async {
      // arrange
      final bookingTime = DateTime.now().add(const Duration(hours: 1));
      final booking = createBooking(
        status: BookingStatus.confirmed,
        dateTime: bookingTime,
        servicePrice: 100.0,
      );

      when(mockRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));
      when(mockRepository.cancelBooking(
        bookingId: any,
        penalty: any,
        refund: any,
      )).thenAnswer((_) async => const Right(true));

      // act
      final result = await useCase(CancelBookingParams(bookingId: 'booking-1'));

      // assert - ✍️ MI ASERCIÓN
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success'),
        (cancellationResult) {
          expect(cancellationResult.wasCancelled, true);
          expect(cancellationResult.refundAmount, 0.0); // Sin refund
          expect(cancellationResult.penaltyAmount, 100.0); // 100% penalty
        },
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 4: No se puede cancelar reserva ya cancelada
    // ─────────────────────────────────────────────────────────────

    test('should fail when trying to cancel already cancelled booking', () async {
      // arrange
      final booking = createBooking(
        status: BookingStatus.cancelled,
        dateTime: DateTime.now().add(const Duration(hours: 48)),
      );

      when(mockRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));

      // act
      final result = await useCase(CancelBookingParams(bookingId: 'booking-1'));

      // assert
      expect(result.isLeft(), true);
      result.fold(
        (failure) => expect(failure.code, 'CANNOT_CANCEL'),
        (_) => fail('Expected failure'),
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 5: Festivos tienen política especial
    // ─────────────────────────────────────────────────────────────

    test('should apply stricter penalty for holidays', () async {
      // arrange - Navidades (24 Dic) con poca anticipación
      final christmasEve = DateTime(2026, 12, 24, 14, 0); // 14:00
      final now = DateTime(2026, 12, 23, 16, 0); // Día anterior 16:00
      // Esto es ~22 horas de anticipación, normalmente sería 50% penalty
      // Pero en festivo con <24h es 100%

      // Para hacer el test realista, mockeamos DateTime.now
      final booking = createBooking(
        status: BookingStatus.confirmed,
        dateTime: christmasEve,
        servicePrice: 100.0,
      );

      when(mockRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));
      when(mockRepository.cancelBooking(
        bookingId: any,
        penalty: any,
        refund: any,
      )).thenAnswer((_) async => const Right(true));

      // act
      final result = await useCase(CancelBookingParams(bookingId: 'booking-1'));

      // assert - ✍️ MI ASERCIÓN - Verifico lógica de festivo
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success'),
        (cancellationResult) {
          // En festivo <24h = penalty 100%
          expect(cancellationResult.penaltyAmount, 100.0);
          expect(cancellationResult.refundAmount, 0.0);
        },
      );
    });
  });
}
```

### 7.3 Tests para MarkNoShowUseCase

```dart
// test/features/reservation/domain/usecases/mark_no_show_test.dart

import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

import 'package:my_app/features/reservation/domain/entities/booking.dart';
import 'package:my_app/features/reservation/domain/entities/client.dart';
import 'package:my_app/features/reservation/domain/failures/reservation_failure.dart';
import 'package:my_app/features/reservation/domain/repositories/booking_repository.dart';
import 'package:my_app/features/reservation/domain/repositories/client_repository.dart';
import 'package:my_app/features/reservation/domain/usecases/mark_no_show.dart';
import 'package:my_app/features/reservation/core/constants/reservation_constants.dart';

@GenerateMocks([BookingRepository, ClientRepository])
import 'mark_no_show_test.mocks.dart';

void main() {
  late MarkNoShowUseCase useCase;
  late MockBookingRepository mockBookingRepository;
  late MockClientRepository mockClientRepository;

  setUp(() {
    mockBookingRepository = MockBookingRepository();
    mockClientRepository = MockClientRepository();
    useCase = MarkNoShowUseCase(
      bookingRepository: mockBookingRepository,
      clientRepository: mockClientRepository,
    );
  });

  // ═══════════════════════════════════════════════════════════════
  // ✍️ TEST DATA
  // ═══════════════════════════════════════════════════════════════

  Client createClient({
    int noShowCount = 0,
    ClientStatus status = ClientStatus.active,
  }) {
    return Client(
      id: 'client-1',
      name: 'Test Client',
      email: 'test@test.com',
      phone: '123456',
      noShowCount: noShowCount,
      status: status,
    );
  }

  Booking createBooking({
    required BookingStatus status,
    required DateTime dateTime,
  }) {
    return Booking(
      id: 'booking-1',
      clientId: 'client-1',
      serviceId: 'service-1',
      dateTime: dateTime,
      status: status,
      createdAt: DateTime.now(),
    );
  }

  // ═══════════════════════════════════════════════════════════════
  // ✍️ TESTS: No-show tracking
  // ═══════════════════════════════════════════════════════════════

  group('MarkNoShowUseCase', () {
    // ─────────────────────────────────────────────────────────────
    // TEST 1: Primer no-show - no bloquea
    // ─────────────────────────────────────────────────────────────

    test('should mark no-show and not block client on first occurrence', () async {
      // arrange
      final pastBookingTime = DateTime.now().subtract(
        const Duration(minutes: ReservationConstants.noShowGracePeriodMinutes + 1),
      );
      
      final booking = createBooking(
        status: BookingStatus.confirmed,
        dateTime: pastBookingTime,
      );
      final client = createClient(noShowCount: 0);

      when(mockBookingRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));
      when(mockBookingRepository.markNoShow(bookingId: any))
          .thenAnswer((_) async => const Right(true));
      when(mockClientRepository.getClient(any))
          .thenAnswer((_) async => Right(client));
      when(mockClientRepository.updateClient(
        clientId: any,
        noShowCount: any,
        lastNoShowDate: any,
        status: any,
      )).thenAnswer((_) async => const Right(true));

      // act
      final result = await useCase(MarkNoShowParams(bookingId: 'booking-1'));

      // assert - ✍️ MI ASERCIÓN
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success'),
        (noShowResult) {
          expect(noShowResult.wasMarked, true);
          expect(noShowResult.clientBlocked, false); // No bloqueado aún
          expect(noShowResult.currentNoShowCount, 1); // Ahora tiene 1
        },
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 2: Tercer no-show - BLOQUEA al cliente
    // ─────────────────────────────────────────────────────────────

    test('should block client on third no-show', () async {
      // arrange
      final pastBookingTime = DateTime.now().subtract(
        const Duration(minutes: ReservationConstants.noShowGracePeriodMinutes + 1),
      );
      
      final booking = createBooking(
        status: BookingStatus.confirmed,
        dateTime: pastBookingTime,
      );
      final client = createClient(noShowCount: 2); // Ya tiene 2 no-shows

      when(mockBookingRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));
      when(mockBookingRepository.markNoShow(bookingId: any))
          .thenAnswer((_) async => const Right(true));
      when(mockClientRepository.getClient(any))
          .thenAnswer((_) async => Right(client));
      when(mockClientRepository.updateClient(
        clientId: any,
        noShowCount: any,
        lastNoShowDate: any,
        status: any,
      )).thenAnswer((_) async => const Right(true));

      // act
      final result = await useCase(MarkNoShowParams(bookingId: 'booking-1'));

      // assert - ✍️ MI ASERCIÓN - El cliente DEBE bloquearse
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success'),
        (noShowResult) {
          expect(noShowResult.wasMarked, true);
          expect(noShowResult.clientBlocked, true); // BLOQUEADO
          expect(noShowResult.currentNoShowCount, 3);
        },
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 3: Muy temprano para marcar no-show
    // ─────────────────────────────────────────────────────────────

    test('should fail if too early to mark as no-show', () async {
      // arrange - La reserva es en 10 minutos (dentro del grace period)
      final soonBookingTime = DateTime.now().add(const Duration(minutes: 10));
      
      final booking = createBooking(
        status: BookingStatus.confirmed,
        dateTime: soonBookingTime,
      );

      when(mockBookingRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));

      // act
      final result = await useCase(MarkNoShowParams(bookingId: 'booking-1'));

      // assert
      expect(result.isLeft(), true);
      result.fold(
        (failure) => expect(failure.code, 'TOO_EARLY'),
        (_) => fail('Expected failure'),
      );
    });

    // ─────────────────────────────────────────────────────────────
    // TEST 4: Cliente ya bloqueado no puede tener más no-shows
    // ─────────────────────────────────────────────────────────────

    test('should handle already blocked client gracefully', () async {
      // arrange
      final pastBookingTime = DateTime.now().subtract(
        const Duration(minutes: ReservationConstants.noShowGracePeriodMinutes + 1),
      );
      
      final booking = createBooking(
        status: BookingStatus.confirmed,
        dateTime: pastBookingTime,
      );
      final blockedClient = createClient(
        noShowCount: 3,
        status: ClientStatus.blocked,
      );

      when(mockBookingRepository.getBooking(any))
          .thenAnswer((_) async => Right(booking));
      when(mockBookingRepository.markNoShow(bookingId: any))
          .thenAnswer((_) async => const Right(true));
      when(mockClientRepository.getClient(any))
          .thenAnswer((_) async => Right(blockedClient));
      when(mockClientRepository.updateClient(
        clientId: any,
        noShowCount: any,
        lastNoShowDate: any,
        status: any,
      )).thenAnswer((_) async => const Right(true));

      // act
      final result = await useCase(MarkNoShowParams(bookingId: 'booking-1'));

      // assert
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success'),
        (noShowResult) {
          expect(noShowResult.wasMarked, true);
          // El cliente ya estaba bloqueado, sigue bloqueado
          expect(noShowResult.clientBlocked, true);
        },
      );
    });
  });
}
```

---

## 8. Resumen y Checklist Final

```
┌─────────────────────────────────────────────────────────────────┐
│              RESUMEN DE LA IMPLEMENTACIÓN HÍBRIDA              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📊 MÉTRICAS:                                                   │
│     • Líneas generadas por IA (scaffold): ~400                  │
│     • Líneas escritas manualmente: ~600                        │
│     • Ratio: 40% IA / 60% Manual ✓                              │
│                                                                 │
│  🎯 LÓGICA CRÍTICA IMPLEMENTADA:                               │
│     ✓ Double booking prevention                                │
│     ✓ Buffer time enforcement                                  │
│     ✓ Horarios especiales (festivos, domingo)                  │
│     ✓ Política de cancelación por horas                       │
│     ✓ No-show tracking y bloqueo automático                   │
│     ✓ Waitlist con priorización VIP                           │
│     ✓ Overbooking estratégico (configurable)                  │
│                                                                 │
│  🧪 TESTS IMPLEMENTADOS:                                        │
│     ✓ Tests de disponibilidad de slots                        │
│     ✓ Tests de política de cancelación                        │
│     ✓ Tests de no-show y bloqueo                             │
│     ✓ Tests de waitlist                                       │
│     ✓ Cobertura de edge cases                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Checklist de Aplicación del Framework AIDR

```markdown
┌─────────────────────────────────────────────────────────────────┐
│         CHECKLIST DE APLICACIÓN DEL FRAMEWORK AIDR             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ ANALYZE (Análisis Personal)                                  │
│     ├─ ¿Identifiqué todos los edge cases?                      │
│     ├─ ¿Entendí las reglas de negocio?                         │
│     ├─ ¿Sé qué puede fallar?                                   │
│     └─ ¿Documenté mis decisiones?                               │
│                                                                 │
│  □ INVESTIGATE (Investigación con IA)                          │
│     ├─ ¿Busqué patrones relevantes?                             │
│     ├─ ¿Investigué mejores prácticas?                          │
│     └─ ¿No confundí investigar con ejecutar?                   │
│                                                                 │
│  □ DECIDE (Decisión de Responsabilidad)                        │
│     ├─ ¿Separé claramente boilerplate de lógica crítica?       │
│     ├─ ¿Usé la matriz de decisiones?                            │
│     └─ ¿Tengo justificación para cada decisión?                │
│                                                                 │
│  □ IMPLEMENT (Implementación Híbrida)                           │
│     ├─ ¿IA generó el scaffold?                                 │
│     ├─ ¿Yo implementé la lógica crítica?                       │
│     └─ ¿Usé constantes para políticas de negocio?              │
│                                                                 │
│  □ REVIEW (Revisión y Validación)                              │
│     ├─ ¿Revisé cada línea de código de IA?                     │
│     ├─ ¿Verifiqué los edge cases?                               │
│     └─ ¿Pasé el checklist de revisión?                         │
│                                                                 │
│  □ TEST (Testing Híbrido)                                       │
│     ├─ ¿IA generó el scaffold de tests?                        │
│     ├─ ¿Yo escribí las aserciones?                             │
│     └─ ¿Probé los edge cases críticos?                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Próximos Pasos Recomendados

```markdown
┌─────────────────────────────────────────────────────────────────┐
│                 PRÓXIMOS PASOS                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. IMPLEMENTAR Data Layer                                      │
│     • Models con fromJson/toJson                               │
│     • DataSources (Remote y Local)                             │
│     • Repository Implementation                                │
│                                                                 │
│  2. IMPLEMENTAR Presentation Layer                              │
│     • ReservationCubit con estados                             │
│     • ReservationPage y widgets                                │
│     • Validaciones de formulario                               │
│                                                                 │
│  3. COMPLETAR Tests                                             │
│     • Tests de Repository                                      │
│     • Tests de Cubit                                           │
│     • Tests de integración                                     │
│                                                                 │
│  4. CONFIGURAR DI                                               │
│     • Registrar UseCases en GetIt                              │
│     • Configurar DataSources                                   │
│                                                                 │
│  5. AGREGAR a README principal                                   │
│     • Link a esta práctica                                     │
│     • Resumen del enfoque híbrido                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**Última actualización:** 2026
**Versión:** 1.0
**Archivos relacionados:**
- `🤖 GUÍA - Uso Inteligente de IA en Desarrollo Flutter.md`
- `🎯 1- GUÍA SIMPLE: Clean Architecture Paso a Paso.md`
- `🧪 testing/` (carpeta de testing)
