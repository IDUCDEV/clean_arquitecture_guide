# 06 - Checklist de Lanzamiento

> Runbook operativo: que configurar antes del lanzamiento, que monitorear el dia 0, y que revisar cada semana y cada mes. Imprimelo, pegalo en tu pared, y sigue el checklist.

---

## 1. Dia -7 (una semana antes del lanzamiento)

### Configuracion Supabase

```text
[ ] Plan decidido: Pro recomendado (ver 02-alertas-y-spend-cap)
[ ] Spend Cap configurado: ON si es tu primera app, OFF si ya tienes ingresos
[ ] Billing email: correcto y revisado (no un alias olvidado)
[ ] Verificar que backups automaticos estan activos (Pro)
[ ] RLS habilitado en TODAS las tablas (ver Advisors)
[ ] 0 findings criticos en Advisors (security + performance)
```

### Baseline de consumo (tu punto de referencia)

```text
[ ] Organization -> Usage: anota el consumo actual de cada metrica
    Egresos:    _____ GB
    DB Size:    _____ MB
    Storage:    _____ MB
    Edge Func:  _____ invocaciones
    Realtime:   _____ mensajes
    MAU:        _____ usuarios

Esto es tu baseline. Cualquier desvio significativo post-lanzamiento
es investigable.
```

### Codigo Flutter

```text
[ ] select() con columnas especificas en todos los repositories
[ ] .range() paginado en todas las listas grandes
[ ] realtime subscribe + dispose/removeChannel en todas las pantallas
[ ] imagenes comprimidas antes de subir (si aplica)
[ ] Error reporting a Sentry/Crashlytics configurado
[ ] Buscar select() sin especificar columnas (grep en codigo)
```

---

## 2. Dia 0 (lanzamiento)

### Primera hora

```text
[ ] Dashboard abierto en un monitor/pestaña
[ ] Organization -> Usage:刷新 cada 15 minutos
[ ] Reports -> API: latencia y errores en tiempo real
[ ] Logs Explorer: revisar errores 4xx/5xx en los primeros requests
[ ] status.supabase.com: verificar que no hay incidentes activos
```

### Primeras 24 horas

```text
[ ] Revisar errores en Crashlytics/Sentry (app side)
[ ] Revisar Query Performance: queries lentas nuevas?
[ ] Verificar que la app hace login correctamente (MAU incrementando)
[ ] Verificar que no hay queries secuenciales (3+ queries por pantalla)
[ ] Confirmar baseline: egreso y DB size dentro de lo esperado?
```

---

## 3. Semanal (15 minutos, lunes)

```text
[ ] Organization -> Usage: barrer las 6 metricas vs cuota
    - Calcular velocidad (% / dias transcurridos)
    - Si velocidad > proyeccion segura, investigar
[ ] Reports -> API: endpoints con mas errores
[ ] Query Performance: queries lentas nuevas? (pg_stat_statements)
[ ] Advisors: 0 issues nuevos desde la semana pasada
[ ] Sentry/Crashlytics: crashes nuevos o regressions?
[ ] Anotar en un archivo la captura de Usage para tendencia
```

### Plantilla de registro semanal

```text
Semana del [fecha]:
  Egresos:    _____ GB (% del ciclo: ___%)
  DB Size:    _____ MB
  MAU:        _____
  Edge Func:  _____
  Anotaciones: _________________________________
```

---

## 4. Mensual (pre-factura, 30 minutos)

```text
[ ] Organization -> Billing & Usage -> Invoices: leer la factura linea por linea
[ ] Comparar contra baseline: que metrica crecio mas?
[ ] Proyectar el siguiente mes: si velocidad actual continua, donde llego?
[ ] Decidir: optimizar (04) o upgrade (05)?
[ ] Si optimizaste el mes anterior:验证 que bajo la metrica objetivo
[ ] Actualizar baseline si tuviste cambio de plan
```

---

## 5. Checklist de emergencia

Si llega un email de "excediste tu cuota" o el proyecto se pausa:

```text
1. NO ENTRE en panico. Los datos estan intactos.
2. Dashboard -> proyecto: leer el banner de estado
3. Organization -> Usage: identificar QUE metrica se excedio
4. Si estas en Free -> restaurar proyecto (boton "Restore")
5. Si estas en Pro con Spend Cap ON -> grace period activo,
   tienes tiempo para actuar
6. Aplicar runbook de 02-alertas-y-spend-cap
7. Investigar causa con queries de 03-logs-explorer
8. Aplicar optimizacion de 04 o upgrade de 05
9. Registrar en tu log de incidentes: que paso, cuanto duro, que hiciste
```

---

## 6. Herramientas rapidas de referencia

```text
Ver consumo actual:        Dashboard -> Organization -> Usage
Ver errores de API:        Dashboard -> Reports -> API
Ver queries lentas:        Dashboard -> Query Performance
Ejecutar SQL de auditoria: Dashboard -> SQL Editor
Ver advisors:              Dashboard -> Advisors
Configurar Spend Cap:      Dashboard -> Organization -> Billing & Usage
Ver facturas:              Dashboard -> Organization -> Billing & Usage -> Invoices
Logs de storage egress:    Logs Explorer -> template Storage Egress
Verificar status:          status.supabase.com
```

---

## 7. Tu primer mes post-lanzamiento

```text
Semana 1: Revisar diariamente (10 min)
Semana 2: Revisar 3 veces por semana
Semana 3: Revisar semanalmente
Semana 4: Mensual + decide si cambias de plan
Mes 2+:  Rutina mensual, a menos que una alerta dispare
```

La frecuencia de revision baja a medida que la app se estabiliza. Si al mes 2 no tuviste incidentes, puedes bajar a revision mensual pura.

---

## Resumen final

```text
ANTES:  Baseline + Spend Cap + alertas + codigo optimizado
DURANTE: Revisar Usage semanalmente, investigar con Logs Explorer
DESPUES: Proyectar y decidir (optimizar vs upgrade) cada mes
SIEMPRE: Runbook de emergencia en tu pared
```

Tu app esta en buenas manos. Ahora monitorea, actua con numeros, y duerme tranquilo.
