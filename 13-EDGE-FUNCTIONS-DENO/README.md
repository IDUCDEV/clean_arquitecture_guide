# 13 - Edge Functions con Deno 2

> Edge Functions son funciones serverless que se ejecutan en el edge de Supabase (Deno). Perfectas para lógica de backend que no necesita un servidor dedicado.

---

## 📋 Índice

| # | Archivo | Descripción |
|---|---------|-------------|
| 01 | [01-edge-functions-fundamentos.md](./01-edge-functions-fundamentos.md) | Fundamentos de Edge Functions |
| 02 | [02-cron-triggers.md](./02-cron-triggers.md) | Tareas programadas con cron triggers |
| 03 | [03-rpc-postgresql.md](./03-rpc-postgresql.md) | RPCs de PostgreSQL desde Edge Functions |
| 04 | [04-integracion-flutter-supabase.md](./04-integracion-flutter-supabase.md) | Integración con Flutter |

---

## 🎯 ¿Por qué Edge Functions?

| Situación | Solución tradicional | Edge Function |
|-----------|--------------------|---------------|
| Limpiar datos viejos | Servidor cron | Cron trigger + Edge Function |
| Webhook de pagos | Servidor Express | Edge Function endpoint |
| Lógica sensible (secretos) | Backend separado | Edge Function con JWT verify |
| Procesamiento pesado | Servidor dedicado | Edge Function escalable |

---

## 🚀 Siguiente paso

Continue with [01-edge-functions-fundamentos.md](./01-edge-functions-fundamentos.md)

---

**Nivel:** Avanzado  
**Tiempo estimado:** 3-4 horas
