# 04 - Supabase Consumo y Costos

> Tu app esta en produccion, los usuarios llegan, y llega la factura de Supabase. Este submodulo te ensena a monitorear el consumo de Supabase Cloud, configurar alertas ANTES del problema, optimizar el uso del backend y decidir con numeros cuando optimizar codigo y cuando pagar un upgrade.

---

## Por que este submodulo existe

Los otros submodulos de este modulo monitorean **tu app** (crashes, performance). Nadie monitorea **el backend**. Y Supabase Cloud tiene un modelo que puede jugarte en contra si no lo conoces:

```
Escenario sin preparacion:
  Lanzamiento en Play Store
    └── La app se hace viral
      └── El egreso (bandwidth) se dispara
        └── Spend Cap desactivado
          └── Factura sorpresa de $200+
            └── Pánico

Escenario con preparacion:
  Lanzamiento en Play Store
    └── Alertas al 75% de cada cuota
      └── Recibes email "egreso al 80%"
        └── Abres Logs Explorer, identificas endpoint pesado
          └── Optimizas o activas Spend Cap
            └── Control total
```

La diferencia entre ambos escenarios es **informacion + configuracion hecha antes del lanzamiento**.

---

## Las 6 metricas que te cobran

Supabase Cloud cobra por cuota excedida. Estas son las metricas del plan Free y Pro (verificado agosto 2026, fuente: [billing oficial](https://supabase.com/docs/guides/platform/billing-on-supabase)):

| Metrica | Que mide | Free | Pro (incluido) | Excedente Pro |
|---|---|---|---|---|
| **Egresos** | Datos servidos al cliente (DB + Storage + Functions) | 5 GB | 250 GB | $0.09 / GB |
| **Database Size** | Tamaño en disco de tu base de datos | 500 MB | 8 GB | $0.125 / GB |
| **MAU** | Usuarios activos mensuales (auth) | 50,000 | 100,000 | $0.00325 / MAU |
| **Storage Size** | Archivos almacenados en buckets | 1 GB | 100 GB | $0.021 / GB |
| **Edge Function Invocations** | Veces que se invoca una function | 500,000 | 2 millones | $2 / millon |
| **Realtime Messages** | Mensajes por canales realtime | 2 millones | 5 millones | $2.5 / millon |

Mas detalles: Realtime Peak Connections (200 Free / 500 Pro), Storage Transforms (solo Pro).

> **Nota:** las cifras cambian con el tiempo. Antes de tomar decisiones de costo, verifica siempre la tabla oficial: [supabase.com/docs/guides/platform/billing-on-supabase](https://supabase.com/docs/guides/platform/billing-on-supabase)

---

## Mapa mental: cuando usar que

```
Quiero saber cuanto llevo consumido este mes
  └── Dashboard -> Organization -> Usage (01-cuotas-y-dashboard.md)

Tengo miedo de una factura sorpresa
  └── Spend Cap ON + alertas de billing (02-alertas-y-spend-cap.md)

Mi proyecto Free fue pausado
  └── Runbook de recuperacion (02-alertas-y-spend-cap.md)

Un endpoint consume demasiado / hay queries lentas
  └── Logs Explorer + Query Performance (03-logs-explorer-query-performance.md)

Estoy acercandome a una cuota
  └── Playbook de optimizacion por metrica (04-optimizacion-por-metrica.md)

No se si optimizar codigo o pagar upgrade
  └── Framework de decision con numeros (05-framework-decision-optimizar-vs-upgrade.md)

Faltan X dias para el lanzamiento
  └── Checklist operativa (06-checklist-lanzamiento.md)
```

---

## Requisitos previos

| Modulo | Por que |
|---|---|
| [03-SUPABASE](../../03-SUPABASE/) | Configuracion del backend, RLS, migraciones |
| [01-CLEAN-ARCHITECTURE](../../01-CLEAN-ARCHITECTURE/) | Donde vive el codigo de datasources que optimizaras |
| [04-ALMACENAMIENTO-LOCAL](../../04-ALMACENAMIENTO-LOCAL/) | Cache local con Isar para reducir egresos |
| 01-firebase-crashlytics / 02-sentry | Monitoreo del cliente (complemento, no requisito) |

---

## Contenido del submodulo

| # | Archivo | Descripcion | Tiempo |
|---|---|---|---|
| 1 | [01-cuotas-y-dashboard](./01-cuotas-y-dashboard.md) | Cada metrica explicada y donde verla | 2h |
| 2 | [02-alertas-y-spend-cap](./02-alertas-y-spend-cap.md) | Spend Cap, alertas, runbook de proyecto pausado | 1-2h |
| 3 | [03-logs-explorer-query-performance](./03-logs-explorer-query-performance.md) | SQL para encontrar lo que consume | 3-4h |
| 4 | [04-optimizacion-por-metrica](./04-optimizacion-por-metrica.md) | Playbook Flutter + Supabase para bajar cada metrica | 4-6h |
| 5 | [05-framework-decision-optimizar-vs-upgrade](./05-framework-decision-optimizar-vs-upgrade.md) | Decidir con numeros, no con miedo | 1-2h |
| 6 | [06-checklist-lanzamiento](./06-checklist-lanzamiento.md) | Runbook dia -7, dia 0, semanal y mensual | 1h |

### Progresion recomendada

```
Fase 1: Entender el terreno (antes del lanzamiento)
  ├── Cuotas y dashboard
  └── Spend Cap + alertas configuradas

Fase 2: Instrumentar (dia -7)
  └── Checklist de lanzamiento completa

Fase 3: Operar (semanal)
  ├── Rutina de 15 min
  ├── Logs Explorer cuando algo se dispara
  └── Query Performance + Advisors

Fase 4: Actuar (cuando creces)
  ├── Playbook de optimizacion
  └── Framework optimizar vs upgrade
```

---

## Conceptos clave en 60 segundos

- **Cuota**: cantidad incluida en tu plan. Debajo = gratis. Encima = sobrecosto o bloqueo.
- **Spend Cap**: interruptor de tu plan Pro. ON = nunca pagas de mas (el servicio se degrada/pausa al llegar al tope). OFF = pagas todo el consumo extra.
- **Egreso**: TODO dato que sale de Supabase hacia tus usuarios: filas de Postgres, archivos de Storage, respuestas de Edge Functions. Es la metrica que mas rapido explota.
- **MAU**: usuario distinto que hace login O refresca su token en el ciclo de facturacion. Cuenta UNA vez por ciclo aunque se conecte a diario.
- **Grace period**: periodo de gracia cuando excedes cuotas con Spend Cap activo o en Free. Te dan tiempo para reaccionar antes del bloqueo.
- **Proyecto pausado**: en Free, si excedes cuotas duras o hay inactividad prolongada, el proyecto se pausa y la app deja de funcionar hasta que lo restaures.

---

## Convenciones en este submodulo

- Backend: **Supabase Cloud** (planes Free/Pro). Si eres self-hosted, esto aplica solo parcialmente (no hay cuotas, sino capacidad de tu VPS; ver PARTE-2 de 03-SUPABASE).
- Los precios citados fueron verificados en **agosto 2026** contra docs oficiales. Verifica siempre antes de decidir.
- Ejemplos de codigo en **Dart/Flutter** con `supabase_flutter` v2 y Clean Architecture.
- Cada query SQL de Logs Explorer es **copiar-pegar y funciona**.

---

## Fuentes oficiales

- [Billing on Supabase (tabla de cuotas)](https://supabase.com/docs/guides/platform/billing-on-supabase)
- [Manage your usage (detalle por metrica)](https://supabase.com/docs/guides/platform/manage-your-usage)
- [Cost control (Spend Cap)](https://supabase.com/docs/guides/platform/cost-control)
- [Bandwidth & Storage Egress](https://supabase.com/docs/guides/storage/serving/bandwidth)
- [Query Performance](https://supabase.com/docs/guides/platform/query-performance)
- [Logs Explorer](https://supabase.com/docs/guides/platform/logs-explorer)
