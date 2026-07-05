# 03 - RPCs de PostgreSQL desde Edge Functions

> Las RPCs (Remote Procedure Calls) permiten ejecutar funciones de PostgreSQL directamente desde Edge Functions, combinando la potencia de SQL con la flexibilidad de TypeScript.

---

## 1. ¿Qué es una RPC?

Una RPC es una función almacenada en PostgreSQL que se puede invocar desde el cliente o desde Edge Functions.

```
Edge Function → supabase.rpc('function_name', params) → PostgreSQL → Result
```

**Ventajas:**
- Lógica de base de datos en SQL (rápido, transaccional)
- Reutilizable desde cualquier cliente (Flutter, web, Edge Functions)
- Operaciones complejas en una sola llamada
- Transacciones ACID garantizadas

---

## 2. Crear una RPC

### 2.1 RPC Simple

```sql
-- supabase/migrations/YYYYMMDDHHMMSS_create_rpc.sql

-- Contar boletos vendidos de un sorteo
CREATE OR REPLACE FUNCTION count_sold_tickets(p_raffle_id UUID)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
  v_count INTEGER;
BEGIN
  SELECT COUNT(*) INTO v_count
  FROM tickets
  WHERE raffle_id = p_raffle_id
    AND status = 'sold';

  RETURN v_count;
END;
$$;
```

### 2.2 RPC con Transacciones

```sql
-- Comprar boleto (reserva → pago)
CREATE OR REPLACE FUNCTION purchase_ticket(
  p_ticket_id UUID,
  p_user_id UUID,
  p_payment_method TEXT
)
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
  v_ticket RECORD;
  v_result JSONB;
BEGIN
  -- Lock el boleto para evitar doble compra
  SELECT * INTO v_ticket
  FROM tickets
  WHERE id = p_ticket_id
  FOR UPDATE;

  -- Validar disponibilidad
  IF v_ticket.status != 'available' THEN
    RAISE EXCEPTION 'Ticket already sold or reserved'
      USING HINT = 'Ticket status: ' || v_ticket.status;
  END IF;

  -- Actualizar boleto
  UPDATE tickets
  SET status = 'sold',
      buyer_id = p_user_id,
      payment_method = p_payment_method,
      sold_at = NOW()
  WHERE id = p_ticket_id;

  -- Registrar transacción
  INSERT INTO transactions (ticket_id, user_id, amount, type)
  VALUES (p_ticket_id, p_user_id, v_ticket.price, 'purchase');

  -- Resultado
  v_result := jsonb_build_object(
    'success', true,
    'ticket_number', v_ticket.number,
    'amount', v_ticket.price
  );

  RETURN v_result;
END;
$$;
```

---

## 3. Llamar RPCs desde Edge Functions

### 3.1 Llamada Básica

```typescript
import { createClient } from "jsr:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const { raffleId } = await req.json();

  const { data, error } = await supabase.rpc("count_sold_tickets", {
    p_raffle_id: raffleId,
  });

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ sold: data }), {
    headers: { "Content-Type": "application/json" },
  });
});
```

### 3.2 Transacciones desde Edge Function

```typescript
Deno.serve(async (req: Request) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  try {
    const { ticketId, userId, paymentMethod } = await req.json();

    const { data, error } = await supabase.rpc("purchase_ticket", {
      p_ticket_id: ticketId,
      p_user_id: userId,
      p_payment_method: paymentMethod,
    });

    if (error) throw error;

    return new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message,
      }),
      { status: 400, headers: { "Content-Type": "application/json" } },
    );
  }
});
```

---

## 4. RPCs Avanzadas

### 4.1 Reportes Agregados

```sql
-- Reporte de ventas por período
CREATE OR REPLACE FUNCTION sales_report(
  p_start_date TIMESTAMPTZ,
  p_end_date TIMESTAMPTZ
)
RETURNS TABLE (
  date DATE,
  total_sales BIGINT,
  total_amount NUMERIC,
  payment_method TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    DATE(t.sold_at) as date,
    COUNT(*)::BIGINT as total_sales,
    SUM(t.price) as total_amount,
    t.payment_method
  FROM tickets t
  WHERE t.status = 'sold'
    AND t.sold_at >= p_start_date
    AND t.sold_at <= p_end_date
  GROUP BY DATE(t.sold_at), t.payment_method
  ORDER BY date DESC;
END;
$$;
```

### 4.2 Búsqueda Full-Text

```sql
-- Habilitar búsqueda de texto completo
ALTER TABLE raffles ADD COLUMN search_vector TSVECTOR;

CREATE OR REPLACE FUNCTION search_raffles(p_query TEXT)
RETURNS SETOF raffles
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT *
  FROM raffles
  WHERE search_vector @@ plainto_tsquery('spanish', p_query)
  ORDER BY ts_rank(search_vector, plainto_tsquery('spanish', p_query)) DESC
  LIMIT 20;
END;
$$;
```

---

## 5. Edge Function + RPC: Patrón Completo

### 5.1 Validación en Edge Function + Ejecución en RPC

```typescript
Deno.serve(async (req: Request) => {
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  // 1. Validar autenticación
  const authHeader = req.headers.get("Authorization");
  if (!authHeader) {
    return new Response("Unauthorized", { status: 401 });
  }

  const { data: { user }, error: authError } =
    await supabase.auth.getUser(authHeader.replace("Bearer ", ""));

  if (authError || !user) {
    return new Response("Unauthorized", { status: 401 });
  }

  // 2. Validar input
  const body = await req.json();
  if (!body.raffleId || !body.ticketCount) {
    return new Response(
      JSON.stringify({ error: "Missing required fields" }),
      { status: 400 },
    );
  }

  // 3. Ejecutar RPC transaccional
  const { data, error } = await supabase.rpc("purchase_tickets_batch", {
    p_raffle_id: body.raffleId,
    p_user_id: user.id,
    p_count: body.ticketCount,
  });

  if (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400 },
    );
  }

  // 4. Respuesta
  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
});
```

### 5.2 Manejo de Errores desde RPC

```sql
CREATE OR REPLACE FUNCTION safe_purchase(p_ticket_id UUID)
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
  v_result JSONB;
BEGIN
  BEGIN
    -- Lógica transaccional
    UPDATE tickets SET status = 'sold' WHERE id = p_ticket_id;

    IF NOT FOUND THEN
      v_result := jsonb_build_object(
        'success', false,
        'error', 'Ticket not found'
      );
    ELSE
      v_result := jsonb_build_object(
        'success', true
      );
    END IF;

    RETURN v_result;
  EXCEPTION
    WHEN OTHERS THEN
      v_result := jsonb_build_object(
        'success', false,
        'error', SQLERRM
      );
      RETURN v_result;
  END;
END;
$$;
```

---

## 6. Migraciones de RPCs

### 6.1 Crear Migración

```bash
supabase migration new create_purchase_rpc
```

```sql
-- supabase/migrations/YYYYMMDDHHMMSS_create_purchase_rpc.sql
CREATE OR REPLACE FUNCTION purchase_ticket(...)
RETURNS JSONB
LANGUAGE plpgsql
AS $$ ... $$;
```

### 6.2 Aplicar Migración

```bash
supabase migration up
```

### 6.3 Para modificar una RPC

```sql
-- Crear nueva migración con CREATE OR REPLACE
CREATE OR REPLACE FUNCTION purchase_ticket(
  -- nuevos parámetros si es necesario
)
RETURNS JSONB
LANGUAGE plpgsql
AS $$ ... $$;
```

---

## 7. Resumen

1. **RPCs** = funciones PostgreSQL invocables desde Edge Functions
2. **Transacciones ACID** garantizadas en SQL
3. **Service Role** para operaciones admin
4. **Validación** en Edge Function, **ejecución** en RPC
5. **Migraciones** para versionar RPCs
6. **Errores** manejados tanto en SQL como en TypeScript

---

## Recursos

- [Supabase RPC Guide](https://supabase.com/docs/guides/database/functions)
- [PostgreSQL Functions](https://www.postgresql.org/docs/current/sql-createfunction.html)
- [PL/pgSQL Guide](https://www.postgresql.org/docs/current/plpgsql.html)

---

## 📚 Referencias

- [Supabase | Edge Functions](https://supabase.com/docs/guides/functions) — Documentación oficial de Edge Functions
- [Deno | Manual](https://deno.land/manual) — Documentación oficial de Deno
- [Supabase | Cron jobs](https://supabase.com/docs/guides/functions/cron) — Programación de tareas cron

---
