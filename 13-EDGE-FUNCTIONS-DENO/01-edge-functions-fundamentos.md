# 01 - Edge Functions: Fundamentos

> Edge Functions son funciones serverless escritas en Deno (TypeScript/JavaScript) que se ejecutan en el edge de Supabase.

---

## 1. ¿Qué es una Edge Function?

```
Cliente (Flutter) → Supabase Edge → Deno Runtime → PostgreSQL
                                    ↕
                              Supabase APIs (Auth, Storage, Realtime)
```

**Características:**
- Escritas en TypeScript (Deno)
- Se ejecutan en el edge (baja latencia)
- Acceso directo a la base de datos PostgreSQL
- Pueden verificar JWT automáticamente
- Sin servidor que administrar

---

## 2. Entorno de Desarrollo

### 2.1 Supabase Local

```bash
# Iniciar Supabase local
supabase start

# Verificar estado
supabase status
```

### 2.2 Crear una Edge Function

```bash
# Crear función
supabase functions new hello-world

# Estructura creada:
supabase/
├── functions/
│   └── hello-world/
│       ├── index.ts
│       └── deno.json
```

### 2.3 Ejemplo Mínimo

```typescript
// supabase/functions/hello-world/index.ts
import "jsr:@supabase/functions-js/edge-runtime.d.ts";

Deno.serve(async (req: Request) => {
  const { name } = await req.json();

  const data = {
    message: `Hello ${name}!`,
  };

  return new Response(JSON.stringify(data), {
    headers: { "Content-Type": "application/json" },
  });
});
```

### 2.4 Ejecutar Localmente

```bash
# Servir funciones localmente
supabase functions serve

# Probar con curl
curl http://localhost:54321/functions/v1/hello-world \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "Mundo"}'
# Respuesta: {"message": "Hello Mundo!"}
```

---

## 3. Despliegue

### 3.1 Desplegar a Producción

```bash
# Desplegar función específica
supabase functions deploy hello-world

# Desplegar con JWT verification
supabase functions deploy hello-world --verify-jwt true

# Listar funciones desplegadas
supabase functions list
```

### 3.2 Verificar Despliegue

```bash
# Probar en producción
curl https://<project-ref>.supabase.co/functions/v1/hello-world \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name": "Mundo"}'
```

---

## 4. Edge Function en el Proyecto Real

### 4.1 Estructura

```
supabase/functions/
├── raffle-cleanup/          # Limpieza automática de sorteos
│   ├── index.ts
│   └── deno.json
```

### 4.2 CORS y Headers

```typescript
// lib/cors.ts - Helper para CORS
export const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req: Request) => {
  // Handle preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  // Lógica principal
  const data = { status: "ok" };

  return new Response(JSON.stringify(data), {
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
});
```

### 4.3 deno.json

```json
{
  "imports": {
    "@supabase/supabase-js": "jsr:@supabase/supabase-js@2",
    "std/": "https://deno.land/std@0.224.0/"
  },
  "tasks": {
    "serve": "deno serve index.ts"
  }
}
```

---

## 5. Seguridad

### 5.1 JWT Verification

```typescript
import { createClient } from "jsr:@supabase/supabase-js@2";

Deno.serve(async (req: Request) => {
  const authHeader = req.headers.get("Authorization")!;
  const supabaseClient = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_ANON_KEY")!,
    { global: { headers: { Authorization: authHeader } } },
  );

  // Verificar usuario autenticado
  const {
    data: { user },
  } = await supabaseClient.auth.getUser();

  if (!user) {
    return new Response("Unauthorized", { status: 401 });
  }

  return new Response(JSON.stringify({ userId: user.id }), {
    headers: { "Content-Type": "application/json" },
  });
});
```

### 5.2 Service Role (Operaciones Admin)

```typescript
// Solo para operaciones internas (cron, admin)
const serviceClient = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
);

// ⚠️ Service Role bypass RLS
const { data } = await serviceClient.from("raffles").select("*");
```

---

## 6. Variables de Entorno

```typescript
// Variables disponibles automáticamente por Supabase:
const supabaseUrl = Deno.env.get("SUPABASE_URL");
const supabaseAnonKey = Deno.env.get("SUPABASE_ANON_KEY");
const supabaseServiceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");

// Variables personalizadas (configurar en Supabase Dashboard):
const mySecret = Deno.env.get("MY_CUSTOM_SECRET");
```

**Configurar en producción:**
```bash
supabase secrets set MY_CUSTOM_SECRET=my-value
supabase secrets list
```

---

## 7. Logs y Debugging

### 7.1 Logs Locales

```bash
# Logs en tiempo real
supabase functions serve
# Output: [info] Server started on port 54321
#         [info] Request: POST /functions/v1/hello-world
```

### 7.2 Logs en Producción

```bash
# Ver logs de funciones
supabase functions logs hello-world

# O desde Supabase Dashboard > Edge Functions > Logs
```

### 7.3 Logging en la Función

```typescript
Deno.serve(async (req: Request) => {
  console.log("Request received:", req.method, req.url);

  try {
    const body = await req.json();
    console.log("Body:", body);

    return new Response(JSON.stringify({ success: true }), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Error:", error);
    return new Response(JSON.stringify({ error: "Invalid request" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }
});
```

---

## 8. Resumen

1. **Edge Functions** = serverless en Deno + Supabase
2. **`supabase functions serve`** para desarrollo local
3. **`supabase functions deploy`** para producción
4. **JWT verification** integrada con Supabase Auth
5. **Service Role** para operaciones que bypass RLS
6. **CORS** necesario para peticiones desde el cliente

---

## Recursos

- [Supabase Edge Functions Docs](https://supabase.com/docs/guides/functions)
- [Deno Runtime](https://deno.com/runtime)
- [Supabase CLI Reference](https://supabase.com/docs/reference/cli)

---

## 📚 Referencias

- [Supabase | Edge Functions](https://supabase.com/docs/guides/functions) — Documentación oficial de Edge Functions
- [Deno | Manual](https://deno.land/manual) — Documentación oficial de Deno
- [Supabase | Cron jobs](https://supabase.com/docs/guides/functions/cron) — Programación de tareas cron

---
