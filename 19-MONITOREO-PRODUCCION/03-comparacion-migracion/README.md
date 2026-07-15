# Submodulo 3: Comparacion y Migracion

## Descripcion

Compara Firebase Crashlytics y Sentry en detalle. Aprende a combinar ambas herramientas y como migrar de una a otra.

---

## Contenido

| # | Archivo | Tema | Tiempo |
|---|---|---|---|
| 01 | [01-crashlytics-vs-sentry.md](./01-crashlytics-vs-sentry.md) | Comparacion detallada de features | 45 min |
| 02 | [02-combinar-herramientas.md](./02-combinar-herramientas.md) | Como usar ambas juntas | 60 min |
| 03 | [03-migracion-guia.md](./03-migracion-guia.md) | Guia para migrar de Crashlytics a Sentry | 60 min |
| 04 | [04-cheatsheet-comparacion.md](./04-cheatsheet-comparacion.md) | Cheat sheet de la comparacion | 15 min |

---

## Que aprenderas

- Comparar features de Crashlytics y Sentry
- Decidir cual usar segun tus necesidades
- Combinar ambas herramientas
- Migrar de una a otra
- Configurar CI/CD para ambas

---

## Cuando usar que

| Necesidad | Herramienta recomendada |
|---|---|
| Crash reporting basico | Crashlytics (gratis) |
| Performance tracing | Sentry |
| Session replay | Sentry |
| Integracion Jira bidireccional | Sentry |
| Release health avanzado | Sentry |
| Analytics basico | Firebase Analytics |
| Export SQL | Crashlytics + BigQuery |
| Budget limitado | Crashlytics |
| Features avanzadas | Sentry |

---

## Decision rapida

```
¿Necesitas performance tracing?
├── Si → Sentry
└── No
    ├─¿Necesitas session replay?
    │├── Si → Sentry
    │└── No
    │   ├─¿Necesitas integracion Jira?
    │   │├── Si → Sentry
    │   │└── No
    │   │   ├─¿Presupuesto limitado?
    │   │   │├── Si → Crashlytics
    │   │   │└── No → Sentry
    │   │   └── ...
```
