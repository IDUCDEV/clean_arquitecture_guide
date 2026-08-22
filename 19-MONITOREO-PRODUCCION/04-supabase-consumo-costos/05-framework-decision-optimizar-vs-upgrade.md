# 05 - Framework de Decision: Optimizar vs Upgrade

> Cuando una metrica se acerca al limite, tienes dos caminos: optimizar tu codigo o pagar un upgrade. Este archivo te da un metodo con NUMEROS para decidir, sin miedo y sin culpa.

---

## 1. El error clasico

```text
Error: "Mi egreso esta al 70% de la cuota Free. Deberia optimizar todo mi codigo."

Caso real: 3 GB de egreso en un ciclo de 30 dias
  Free: 5 GB incluidos -> quedan 2 GB de margen

  Opcion A: Optimizar select() + paginacion durante 8 horas
    Ahorro estimado: 40% -> 1.8 GB/mes
    Tu tiempo facturado: 8h x $X/hora

  Opcion B: Upgrade a Pro ($25/mes + ~$10 compute)
    Egresos incluidos: 250 GB -> meses de margen
    Tu tiempo: 0 horas
```

A veces optimizar es correcto. Otras es mas barato pagar. La diferencia son los numeros, no la intuicion.

---

## 2. Formula de costo por metrica

```text
Costo de exceder = (excedente en unidades) x (precio por unidad)

Ejemplo concreto:
  Egresos actuales: 4.8 GB/mes (Free, 5 GB incluidos)
  Proyeccion crecimiento: +20%/mes
  En 2 meses: ~6.9 GB -> 1.9 GB excedente

  Costo sin optimizar (Pro sin Spend Cap):
    1.9 GB x $0.09 = ~$0.17
    No es drama.

  Si fuera DB size (500 MB Free, 400 MB actuales):
    Ya no puedes optimizar, la DB crece sola.
    Upgrade a Pro = $35/mes vs app bloqueada por write-lock.
```

---

## 3. Tabla de decision por umbral de cuota

```text
  % de cuota consumida    Accion recomendada
  ─────────────────────   ─────────────────────────────────
  0% - 40%                Monitorear, no actuar
  40% - 60%               Revisar tendencia mensual
  60% - 75%               Investigar causa (logs + queries)
  75% - 90%               Optimizar lo de bajo costo
  90% - 100%              Upgrade a Pro O activar Spend Cap
  >100%                   Runbook de emergencia (02)
```

**Clave:** el dato NO es el % sino la VELOCIDAD. Estar al 60% el dia 15 es urgente. Estar al 60% el dia 28 es tranquilo.

```text
Velocidad = % consumido / dias transcurridos del ciclo

Ejemplo:
  Dia 10: 40% consumido -> velocidad = 4%/dia
  Proyeccion fin de ciclo: 4% x 30 = 120% -> NECESITAS ACTUAR

  Dia 25: 70% consumido -> velocidad = 2.8%/dia
  Proyeccion: 2.8% x 30 = 84% ->_tranquilo, pero vigila_
```

---

## 4. Proyecciones de factura real

### Escenario: 1,000 usuarios activos

```text
Plan: Pro ($25 + $10 compute)
MAU: ~1,000 (dentro de 100K incluidos) -> $0 extra
Egresos: ~3 GB (dentro de 250 GB) -> $0 extra
Storage: ~50 MB -> $0 extra
Edge Functions: ~10K -> $0 extra

Total mensual: ~$35
Costo por usuario activo: $0.035
```

### Escenario: 10,000 usuarios activos

```text
Plan: Pro ($25 + $15 compute)
MAU: ~10,000 -> $0 extra
Egresos: ~25 GB -> $0 extra
Storage: ~500 MB -> $0 extra
Realtime: ~500K mensajes -> $0 extra

Total mensual: ~$40
Costo por usuario activo: $0.004
```

### Escenario: 50,000 usuarios activos

```text
Plan: Pro ($25 + $25 compute)
MAU: ~50,000 -> $0 extra
Egresos: ~120 GB -> $0 extra (250 GB incluidos)
Storage: ~5 GB -> $0 extra
Realtime: ~5M mensajes -> empieza a preocuparte

Total mensual: ~$55
Costo por usuario activo: $0.0011
```

**Conclusion:** Pro escala bien hasta 50K+ usuarios. El Compute es donde crece la factura, no el consumo variable (salvo Realtime pesado).

---

## 5. Optimizar primero vs upgrade primero

### Optimizar primero cuando:

```text
- El codigo tiene patrones obviamente ineficientes (select * en todo)
- El ahorro es rapido (<2 horas de refactor)
- Estas en Free y el crecimiento es lento/proyectable
- Quieres aprender las buenas practicas antes de escalar
- La optimizacion no degrada la experiencia del usuario
```

### Upgrade primero cuando:

```text
- La app esta en PRODUCCION y la DB size esta al limite
  (write-lock = app rota, no hay workaround de codigo)
- El tiempo de tu equipo vale mas que el sobrecosto
- El crecimiento es rapido y no tienes tiempo para optimizar
- Ya optimizaste lo basico (select, range) y aun creces
- $35/mes es significativamente menos que tu tiempo invertido
```

### La regla de oro:

```text
Si optimizar te toma 1 hora y ahorra $10/mes -> optimiza
Si optimizar te toma 8 horas y ahorra $3/mes -> upgrade
Si la DB size esta al limite -> UPGRADE AHORA, sin excepcion
```

---

## 6. Cuando NO optimizar (siempre)

```text
1. No optimices SELECT * en la primera iteracion de una feature.
   Primero que funcione, luego optimiza en el code review.

2. No optimices queries que tu app ejecuta 1 vez al dia.
   Las queries criticas son las que se ejecutan POR USUARIO POR SESION.

3. No optimices Realtime si tienes <100 usuarios concurrentes.
   El overhead es trivial a esa escala.

4. No optimices Edge Functions que cuestan $0.01/mes.
   Tu tiempo de refactor es mas caro.

5. No optimices antes de MEDIR.
   Usa el Logs Explorer y Query Performance para identificar
   el 20% de codigo que genera el 80% del consumo.
```

---

## 7. Checklist de decision

```text
Antes de optimizar o upgrade, responde estas preguntas:

[ ] Cual metrica esta cerca del limite?
[ ] A que velocidad crece? (proyeccion fin de ciclo)
[ ] Cuanto tiempo me toma optimizar? (estimacion realista)
[ ] Cuanto cuesta el upgrade mensual?
[ ] La optimizacion es reversible si la necesito luego?
[ ] Tengo datos (logs, queries) que justifiquen la accion?

Si no puedes responder la primera pregunta -> ve a 01-cuotas-y-dashboard
Si no puedes responder la segunda -> ve a 03-logs-explorer
```

---

## Siguiente paso

Ya sabes decidir. Ahora ten un runbook listo para el lanzamiento: [06-checklist-lanzamiento](./06-checklist-lanzamiento.md)
