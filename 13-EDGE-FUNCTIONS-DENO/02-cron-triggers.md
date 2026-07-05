# 02 - Cron Triggers

> Ejecuta Edge Functions en un horario programado. Ideal para tareas de mantenimiento, limpieza, y procesamiento batch.

---

## 1. ¿Qué es un Cron Trigger?

Un cron trigger ejecuta una Edge Function automáticamente según un schedule definido.

**Casos de uso reales:**
- Limpiar sorteos expirados cada hora
- Enviar recordatorios de pagos pendientes
- Generar reportes diarios
- Sincronizar datos con servicios externos
- Eliminar tokens expirados

---

## 2. Configuración

### 2.1 Definir el Trigger

```bash
# En el archivo de configuración de la función
supabase/functions/raffle-cleanup/index.ts
```

El trigger se define en `supabase/config.toml`:

```toml
# supabase/config.toml
[functions.raffle-cleanup]
enabled = true
verify_jwt = false  # No necesita autenticación (es interno)
import_map = "./functions/raffle-cleanup/deno.json"
```

Y el cron se configura también en `config.toml`:

```toml
# supabase/config.toml
[functions.raffle-cleanup.cron]
schedule = "0 * * * *"  # Cada hora
```

### 2.2 Expresión Cron

```
┌───────── minuto (0 - 59)
│ ┌───────── hora (0 - 23)
│ │ ┌───────── día del mes (1 - 31)
│ │ │ ┌───────── mes (1 - 12)
│ │ │ │ ┌───────── día de la semana (0 - 6, 0 = domingo)
│ │ │ │ │
* * * * *
```

**Ejemplos comunes:**

| Expresión | Significado |
|-----------|-------------|
| `0 * * * *` | Cada hora |
| `0 0 * * *` | Diario a medianoche |
| `0 6 * * *` | Diario a las 6 AM |
| `*/15 * * * *` | Cada 15 minutos |
| `0 0 * * 0` | Cada domingo a medianoche |
| `0 0 1 * *` | Primer día de cada mes |
| `0 */6 * * *` | Cada 6 horas |
| `0 0,12 * * *` | Dos veces al día (mediodía y medianoche) |

---

## 3. Implementación Real: Cleanup de Sorteos

El monorepo incluye `raffle-cleanup` para limpiar sorteos expirados:

```typescript
// supabase/functions/raffle-cleanup/index.ts
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    const now = new Date().toISOString();

    // 1. Marcar sorteos expirados como cerrados
    const { error: updateError } = await supabase
      .from("raffles")
      .update({ status: "closed" })
      .eq("status", "active")
      .lt("end_date", now);

    if (updateError) throw updateError;

    // 2. Liberar boletos reservados no pagados
    const { error: releaseError } = await supabase
      .from("tickets")
      .update({ status: "available", reserved_at: null })
      .eq("status", "reserved")
      .lt("reserved_at", new Date(Date.now() - 30 * 60 * 1000).toISOString());
    // Libera reservas con más de 30 minutos

    if (releaseError) throw releaseError;

    return new Response(
      JSON.stringify({
        success: true,
        message: "Cleanup completed",
        timestamp: now,
      }),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  } catch (error) {
    console.error("Cleanup error:", error);
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }
});
```

---

## 4. Probar Cron Triggers Localmente

```bash
# Iniciar Supabase local
supabase start

# Servir funciones
supabase functions serve

# Probar la función manualmente
curl http://localhost:54321/functions/v1/raffle-cleanup \
  -X POST \
  -H "Content-Type: application/json"

# Para probar el schedule: ajustar el cron a */1 * * * *
# y esperar 1 minuto
```

---

## 5. Despliegue

```bash
# 1. Desplegar la función
supabase functions deploy raffle-cleanup

# 2. Verificar que el cron está activo
supabase functions list
```

**Desde Supabase Dashboard:**
1. Edge Functions > raffle-cleanup
2. Verificar "Schedule" configurado
3. Revisar logs para confirmar ejecución

---

## 6. Buenas Prácticas

### 6.1 Idempotencia

Las funciones cron deben poder ejecutarse múltiples veces sin efectos secundarios:

```typescript
// ✅ Idempotente: misma ejecución produce mismo resultado
const { data } = await supabase
  .from("raffles")
  .update({ status: "closed" })
  .eq("status", "active")
  .lt("end_date", now);
```

### 6.2 Logging

```typescript
console.log(`[raffle-cleanup] Started at ${new Date().toISOString()}`);

// ... lógica ...

console.log(`[raffle-cleanup] Closed ${count} expired raffles`);
```

### 6.3 Timeout

Las Edge Functions tienen un timeout máximo. Para operaciones largas:
- Procesar en lotes (batches)
- Usar múltiples ejecuciones de cron
- Mantener cada ejecución < 60 segundos

### 6.4 Manejo de Errores

```typescript
try {
  // Operación principal
} catch (error) {
  console.error("Fatal error:", error);
  // Notificar al equipo (email, Slack, etc.)
  await notifyAdmin(error);

  return new Response(
    JSON.stringify({ error: error.message }),
    { status: 500 },
  );
}
```

---

## 7. Casos de Uso Avanzados

### 7.1 Recordatorios por Email

```typescript
// Ejecutar diario a las 9 AM
Deno.serve(async (req: Request) => {
  const { data: pendingPayments } = await supabase
    .from("payments")
    .select("*, users(email, name)")
    .eq("status", "pending")
    .gte("created_at", new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString());

  for (const payment of pendingPayments) {
    await sendEmail({
      to: payment.users.email,
      subject: `Recordatorio: Pago pendiente de ${payment.amount}`,
    });
  }
});
```

### 7.2 Backup de Datos

```typescript
// Ejecutar diario a medianoche
Deno.serve(async (req: Request) => {
  const { data } = await supabase
    .from("raffles")
    .select("*")
    .eq("status", "closed")
    .gte("end_date", new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString());

  // Exportar a CSV y subir a Storage
  const csv = convertToCSV(data);
  await supabase.storage
    .from("backups")
    .upload(`raffles/${new Date().toISOString()}.csv`, csv);

  // Eliminar backups antiguos (>90 días)
  await cleanupOldBackups();
});
```

---

## 8. Resumen

1. **Cron triggers** ejecutan Edge Functions en schedule
2. Se configuran en `supabase/config.toml`
3. **Idempotencia** es clave (misma ejecución = mismo resultado)
4. **Service Role** para operaciones admin
5. **Timeout** máximo, procesar en lotes si es necesario
6. Logging para debugging y monitoreo

---

## Recursos

- [Supabase Cron Jobs](https://supabase.com/docs/guides/functions/cron)
- [Cron Expression Generator](https://crontab.guru/)
- [Supabase config.toml](https://supabase.com/docs/reference/config/introduction)

---

## 📚 Referencias

- [Supabase | Edge Functions](https://supabase.com/docs/guides/functions) — Documentación oficial de Edge Functions
- [Deno | Manual](https://deno.land/manual) — Documentación oficial de Deno
- [Supabase | Cron jobs](https://supabase.com/docs/guides/functions/cron) — Programación de tareas cron

---
