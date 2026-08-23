# Ejemplos de Cambios OpenSpec

> 6 cambios completos listos para estudiar o copiar a `openspec/changes/` en tu proyecto. Derivan de los casos del módulo histórico `02-DISENIO-FEATURE` (conservado como referencia).

| Carpeta | Complejidad | Qué demuestra |
|---------|-------------|---------------|
| [`add-cart/`](./add-cart/) | Intermedia | **Walkthrough completo** puerta por puerta; reglas económicas y cupones |
| [`approve-reservas/`](./approve-reservas/) | Compleja | Multi-actor, concurrencia (RPC atómico), realtime, cron |
| [`add-elearning-progress/`](./add-elearning-progress/) | Intermedia→Compleja | Gating por RLS, dos capacidades en un cambio |
| [`add-facturacion/`](./add-facturacion/) | Compleja | Máquina de estados regulada, numeración atómica |
| [`add-delivery-seguimiento/`](./add-delivery-seguimiento/) | Compleja | Realtime GPS (Broadcast), geolocalización PostGIS |
| [`add-buyers/`](./add-buyers/) | Simple→Intermedia | Cambio pequeño con una puerta combinada |

## Cómo usarlos

1. **Aprender**: lee `add-cart/` completo junto a [02-sdd-flutter-supabase.md](../02-sdd-flutter-supabase.md) — cada archivo corresponde a una fase
2. **Copiar**: clona la carpeta más parecida a tu feature en `openspec/changes/<tu-feature>/` y adapta
3. **Calibrar**: compara `add-buyers/` (ligero) con `approve-reservas/` (completo) para aplicar la proporcionalidad

Plantilla vacía: [04-plantilla-cambio-openspec.md](../04-plantilla-cambio-openspec.md)
