# 02 - Alertas y Spend Cap

> El objetivo de este archivo es simple: que NUNCA te enteres de un problema de consumo por una factura o por tu app caida. Supabase debe avisarte primero, y tu red de seguridad debe estar armada ANTES del lanzamiento.

---

## Objetivos de este archivo

- Entender el Spend Cap y decidir tu configuracion con criterio
- Configurar alertas de billing y notificaciones de cuota
- Tener un runbook para "mi proyecto Free fue pausado"
- Decidir si lanzas en Free o vas directo a Pro

---

## 1. Spend Cap: el interruptor mas importante

### Que es

El **Spend Cap** (tope de gasto) existe solo en planes pagos. Define que pasa cuando excedes las cuotas:

```
Spend Cap ON:
  Llegas al limite de cuota
    └── Email de aviso + grace period
      └── Si sigues excediendo: servicio DEGRADA o SE PAUSA
        └── NUNCA hay sobrecobro
          └── Factura maxima = precio del plan

Spend Cap OFF:
  Llegas al limite de cuota
    └── Sigues operando sin interrupcion
      └── TODO el excedente se cobra
        └── Factura = plan + excedentes (sin tope)
```

### Donde se configura

```
Dashboard -> Organization -> Billing & Usage -> Spend Cap
```

### Cual elegir? Depende de tu tolerancia a riesgo

| Situacion | Recomendacion |
|---|---|
| App nueva, sin ingresos, primera publicacion | **ON** — protege tu bolsillo. Un proyecto pausado unas horas es recuperable; una factura inesperada no lo es |
| App con ingresos, usuarios pagan por ella | **OFF** — la continuidad del servicio vale mas que el sobrecosto controlado, PERO con monitoreo semanal estricto |
| App en crecimiento explosivo (viral) | **ON** mientras validas, luego OFF con alertas |

**Mentalidad:** Spend Cap ON convierte un desastre financiero en un incidente tecnico gestionable.

---

## 2. Sistema de alertas en capas

Supabase NO te va a llamar por telefono. Arma estas capas:

### Capa 1: Email de billing correcto

```
Organization -> Settings -> Billing email
```

- Usa un correo que REVISES (no un alias olvidado).
- Supabase envia avisos al acercarte/exceder cuotas y durante grace periods. Si el email esta mal, todo lo demas falla.
- Marca `notifications@supabase.io` como remitente seguro para que no caiga en spam.

### Capa 2: Notificaciones nativas de cuota

Con Spend Cap ON (o en Free), al superar cuotas recibes:
- Email de aviso
- Entrada al grace period (periodo de gracia)
- Si persiste: degradacion/pausa del servicio

No configuras nada aqui: funciona sola. Tu trabajo es LEER ese email el dia que llega.

### Capa 3: Chequeo activo propio (el mas confiable)

Las alertas nativas son reactivas. Complementa con rutina propia (ver [06-checklist-lanzamiento](./06-checklist-lanzamiento.md)):

```text
LUNES, 10 minutos:
[ ] Organization -> Usage: % consumido de cada metrica
[ ] Si algo > 60% del ciclo con mas de 20% del mes por correr -> investigar
[ ] Reports -> API: picos anormales de requests
```

### Capa 4: Deteccion desde tu app (avanzado, opcional)

Puedes registrar errores HTTP de Supabase en Crashlytics/Sentry y crear alertas sobre ellos. Cuando un proyecto se pausa, tu app recibe errores de red/5xx: si Sentry dispara un spike de errores contra `*.supabase.co`, sabras del problema antes que la mayoria de tus usuarios lo note.

```dart
// En tu datasource o interceptor de errores
try {
  await _client.from('orders').select();
} on PostgrestException catch (e) {
  // e.code, e.message, e.details
  // Reporta a Crashlytics/Sentry como non-fatal
  FirebaseCrashlytics.instance.recordError(
    e,
    StackTrace.current,
    reason: 'PostgrestException code=${e.code}',
  );
  rethrow;
}
```

Un patron util: alerta en Sentry/Crashlytics cuando la tasa de errores de red supera X% en 5 minutos. Eso es un detector indirecto de "backend caido".

---

## 3. Runbook: mi proyecto fue pausado

Sintomas tipicos:
- La app no carga datos / no hace login
- Dashboard muestra banner "Project paused"
- Errores 503/541 o timeout en todos los requests

### Diagnostico rapido

```
Proyecto pausado?
  ├── Banner dice "paused due to inactivity"
  |     └── Caso A: pausa por inactividad (Free)
  ├── Banner/email menciona uso excedido / fair use
  |     └── Caso B: excediste cuotas duras en Free
  └── No hay banner pero todo falla
        └── Caso C: no es pausa -> mira Logs Explorer y status.supabase.com
```

### Caso A/B: restaurar el proyecto

```text
1. Dashboard -> tu proyecto -> botón "Restore project"
2. Espera la restauracion (minutos). Los datos estan intactos;
   la pausa no borra nada.
3. MIENTRAS restaura, identifica la causa raiz:
   - Inactividad: Free pausa proyectos sin actividad (~1 semana sin
     requests). Solucion real: migrar a Pro, o generar trafico minimo
     (health check periodico), o pausar manualmente los Free que no uses.
   - Cuota excedida: mira Organization -> Usage, identifica la metrica,
     aplica playbook de optimizacion (04) o migra a Pro.
4. Verifica la app end-to-end tras restaurar (login, lectura, escritura).
5. Registra en tu log de incidentes: causa, downtime, accion preventiva.
```

### Prevencion estructural

| Causa | Prevencion |
|---|---|
| Pausa por inactividad en Free | Pro para proyectos productivos. Free solo para staging/demos |
| Exceder DB size (500 MB) | Query semanal de tamano + purga de datos viejos |
| Exceder egresos | Playbook 04 + alerta al 60% |
| Exceder MAU por login anonimo | Auditar creacion de usuarios anonimos |

**Regla de oro:** si la app esta publicada en Play Store y genera valor, su backend merece plan Pro ($25/mes). El costo de horas de app caida + reputacion en reviews supera ampliamente el plan.

---

## 4. Free vs Pro para lanzamiento: decision explicita

```
Estas a dias del lanzamiento en Play Store. Donde arranco?

Free ($0):
  + Costo cero mientras validas
  - 500 MB DB: bloqueo de ESCRITURAS al llegar (app rota parcialmente)
  - 5 GB egreso: pocas semanas de trafico moderado con imagenes
  - Riesgo de pausa por inactividad/cuota EN PRODUCCION
  - Sin backups automaticos programados (solo manuales)

Pro ($25 + compute ~$10):
  + Sin pausas por inactividad
  + Backups automaticos diarios
  + 250 GB egreso, 8 GB DB: aire para crecer meses
  + Branching, soporte, SLA mejorado
  + Spend Cap opcional como red de seguridad

Recomendacion practica:
  Lanza en Pro con Spend Cap ON. Es ~$35/mes: menos que una hora
  de freelance. Downgrade despues si quieres, pero no arriesgues
  tu primera impression en la store por ahorrar $35.
```

Excepcion legitima para lanzar en Free: beta cerrada con <100 testers conocidos y sin imagenes pesadas.

---

## Cheatsheet: configuracion minima pre-lanzamiento

```text
[ ] Billing email correcto y revisado
[ ] Decision de plan tomada (recomendado: Pro)
[ ] Spend Cap decidido (recomendado inicial: ON)
[ ] Rutina semanal agendada en tu calendario (10 min, lunes)
[ ] Runbook de pausa leido y entendido
[ ] Errores de Supabase reportandose a Sentry/Crashlytics
[ ] Metrica critica identificada segun tipo de app
[ ] Baseline de consumo medido (ver 06-checklist-lanzamiento)
```

---

## Siguiente paso

Alertas configuradas. Ahora aprende a investigar CUANDO una alerta dispara: encontrar el endpoint, query o archivo exacto que consume: [03-logs-explorer-query-performance](./03-logs-explorer-query-performance.md).
