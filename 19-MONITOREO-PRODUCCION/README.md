# Modulo 19: Monitoreo en Produccion

## Por que este modulo existe

Tu app esta en produccion, pero **como sabes si funciona correctamente?** El monitoreo en produccion es la ultima linea de defensa entre tu app y el usuario. Sin el, estas volando a ciegas.

Este modulo cubre las dos herramientas de monitoreo mas populares para Flutter:

1. **Firebase Crashlytics** - Monitoreo de crashes (gratis, basico)
2. **Sentry** - Monitoreo avanzado (tracing, sesiones, integraciones)

---

## Mapa mental: cuando usar que

```
Necesito saber cuando mi app crashea
  └── Firebase Crashlytics (gratis, ilimitado)

Necesito saber POR QUE crashea
  └── Sentry (stack traces detallados, breadcrumbs)

Quiero medir performance de mi app
  └── Sentry Performance (tracing, spans)

Quiero ver que esta pasando cuando falla
  └── Sentry Session Replay

Necesito integracion con Jira/GitHub
  └── Sentry (bidireccional)

Quiero alertas automatizadas
  └── Firebase Crashlytics + Sentry

Quiero comparar estabilidad entre versiones
  └── Sentry Release Health

Quiero saber cuanto me cuesta Supabase Cloud
  └── 04-supabase-consumo-costos

Quiero optimizar el uso del backend
  └── 04-supabase-consumo-costos (playbook por metrica)

Quiero un checklist pre-lanzamiento
  └── 04-supabase-consumo-costos (06-checklist-lanzamiento)

Quiero analytics basico
  └── Firebase Analytics

Quiero queries SQL de mis crashes
  └── Firebase BigQuery export
```

---

## Requisitos previos

| Modulo | Por que |
|---|---|
| [18-DEBUGGING-FLUTTER](../18-DEBUGGING-FLUTTER/) | Conceptos de debugging |
| [03-SUPABASE](../03-SUPABASE/) | Errores de backend |
| [16-BLOC-CUBIT](../16-BLOC-CUBIT/) | Errores en state management |
| [11-GITHUB-ACTIONS](../11-GITHUB-ACTIONS/) | CI/CD para uploads de symbols |

---

## Contenido del modulo

### Submodulos

| # | Submodulo | Descripcion | Tiempo |
|---|---|---|---|
| 1 | [01-firebase-crashlytics](./01-firebase-crashlytics/) | Crash reporting con Firebase | 6-8h |
| 2 | [02-sentry](./02-sentry/) | Monitoreo avanzado con Sentry | 7-9h |
| 3 | [03-comparacion-migracion](./03-comparacion-migracion/) | Comparar, combinar y migrar herramientas | 3-4h |
| 4 | [04-supabase-consumo-costos](./04-supabase-consumo-costos/) | Monitoreo de consumo, costos y optimizacion de Supabase Cloud | 12-17h |

### Progresion recomendada

```
Fase 1: Fundamentos
  ├── Crashlytics: conceptos -> setup -> non-fatal
  └── Sentry: conceptos -> setup -> error handling

Fase 2: Intermedio
  ├── Crashlytics: custom keys -> alertas -> BigQuery
  └── Sentry: performance -> session replay -> integraciones

Fase 3: Avanzado
  ├── Crashlytics: practicas reales + cheatsheet
  └── Sentry: practicas reales + cheatsheet

Fase 4: Maestria
  └── Comparacion -> Combinar -> Migracion

Fase 5: Backend (Supabase Cloud)
  ├── Cuotas y dashboard -> Alertas y Spend Cap
  ├── Logs Explorer -> Query Performance
  ├── Playbook de optimizacion por metrica
  └── Framework de decision -> Checklist de lanzamiento
```

---

## Comparacion rapida

| Feature | Firebase Crashlytics | Sentry |
|---|---|---|
| **Precio** | Gratis (ilimitado) | Free: 5K errores/mes, Team: $26/mes/user |
| **Crash reporting** | Si | Si |
| **Non-fatal errors** | Si | Si |
| **Performance tracing** | Basico (Firebase Performance) | Avanzado |
| **Session replay** | No | Si |
| **Profiling** | No | Si (iOS/macOS) |
| **Integracion Jira** | Unidireccional | Bidireccional |
| **Integracion GitHub** | No nativa | Si |
| **Release health** | Basico | Avanzado |
| **Feature flags** | No | Si |
| **User feedback** | No | Si |
| **Analytics** | Firebase Analytics | Sentry Analytics |
| **Export SQL** | BigQuery (gratis) | No nativo |
| **Alertas** | Email, Slack, PagerDuty | Email, Slack, PagerDuty, Jira |

---

## Herramientas que necesitas

| Herramienta | Version minima | Para que |
|---|---|---|
| Flutter SDK | 3.24+ | Sentry requiere Flutter 3.24.0+ |
| Dart SDK | 3.5.0+ | Sentry requiere Dart 3.5.0+ |
| Firebase CLI | latest | Configurar Crashlytics |
| Sentry CLI | latest | Upload de debug symbols |

---

## Convenciones en este modulo

- Los ejemplos usan **Clean Architecture** (ver modulo 01)
- State management: **BLoC/Cubit** (ver modulo 16)
- Backend: **Supabase** (ver modulo 03)
- Los escenarios practicos son **reales y reproducibles**
- Cada cheatsheet es una **referencia rapida imprimible**

---

## Fuentes oficiales

- [Firebase Crashlytics](https://firebase.google.com/docs/crashlytics?hl=es-419)
- [Sentry Flutter SDK](https://docs.sentry.io/platforms/dart/guides/flutter/)
- [Sentry Performance](https://docs.sentry.io/platforms/dart/guides/flutter/performance/)
- [Sentry Session Replay](https://docs.sentry.io/platforms/dart/guides/flutter/session-replay/)
