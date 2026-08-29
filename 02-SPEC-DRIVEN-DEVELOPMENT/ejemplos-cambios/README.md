# Ejemplos de Cambios OpenSpec

> 6 cambios completos listos para estudiar o copiar a `openspec/changes/` en tu proyecto. Derivan de los casos del módulo histórico `02-DISENIO-FEATURE` (conservado como referencia).

## El patrón que repiten los 6 cambios

Todos siguen el mismo esqueleto. Léelo una vez y no tendrás que deducirlo de cada ejemplo:

| Paso | Qué produces | Vía A | Vía B | Validación |
|------|--------------|-------|-------|------------|
| 0 · Clasificar | Simple / Intermedia / Compleja | tú decides | tú decides | proporcionalidad |
| 1 · Crear cambio | carpeta `openspec/changes/<feat>/` | `/opsx-propose` | ídem | `openspec validate` |
| 2 · proposal.md | WHY + Impact + Scope + Actores | IA redacta → tú apruebas | ídem | — |
| 3 · spec.md | requisitos EARS con escenarios | IA redacta → tú apruebas | ídem | **Puerta 1** + Clarity Gate |
| 4 · design.md | ficheros, contratos, backend, decisiones | IA redacta → tú apruebas | ídem | **Puerta 2** |
| 5 · tasks.md | 5 oleadas + trazabilidad | IA redacta → tú apruebas | ídem | validate |
| 6 · Implementar | código + tests | skill genera scaffold, **tú escribes los bodies** | `/opsx-apply-change`, **tú auditas cada diff** | tests verdes |
| 7 · Verificar · archivar | specs vivas consolidadas | `/opsx-verify-change` → `/opsx-archive-change` | ídem | **Puerta 3** |

**Observación clave:** hasta el Paso 5, Vía A y Vía B hacen **lo mismo** (la IA redacta, tú apruebas). Solo el Paso 6 difiere: **Vía A** = tú implementas sobre el scaffold generado; **Vía B** = la IA escribe y tú auditas cada diff contra la spec. Las plantillas anotadas (qué va en cada parte) están en [07-guia-paso-a-paso.md](../07-guia-paso-a-paso.md) y la plantilla completa en [04-plantilla-cambio-openspec.md](../04-plantilla-cambio-openspec.md).

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
