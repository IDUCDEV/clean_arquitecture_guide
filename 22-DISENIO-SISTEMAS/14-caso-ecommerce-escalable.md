# 14: Caso de Estudio — E-Commerce Escalable

> Aplicación de la plantilla a un e-commerce: catálogo, carrito, checkout e inventario. Aquí la **consistencia fuerte** importa (dinero y stock), a diferencia de feed y chat.

---

## Paso 1: Alcance y requerimientos

**Producto:** tienda online con catálogo, carrito y checkout.

| Incluido | Fuera de scope (este diseño) |
|---|---|
| Catálogo + búsqueda + productos | Recomendaciones ML |
| Carrito (guardado por usuario) | Wishlist, reviews |
| Checkout + pago (mock) | Envíos/tracking físico, marketplaces |
| Inventario/stock | Multi-moneda, cupones complejos |

**No funcionales:** lecturas del catálogo muy rápidas; **checkout sin race conditions**; el stock **no puede sobregirar**; alta disponibilidad en ventas.

---

## Paso 2: Estimación de escala

| Métrica | Valor |
|---|---|
| Productos en catálogo | 500K |
| Visitas diarias | 100K (10:1 lectura/escritura) |
| Checkouts/día (pico) | 10K |
| QPS de catálogo | ~1.1K |
| QPS de checkout (pico, Black Friday ×10) | ~11 → 115 |

**Lectura:** catálogo es read-heavy; **checkout es write-heavy crítico** con consistencia fuerte.

---

## Paso 3: Modelado de datos

```sql
products(id, name, price_cents, stock_available, created_at)
cart_items(user_id, product_id, quantity)
orders(id, user_id, status, total_cents, created_at)
order_items(order_id, product_id, qty, unit_price_cents)
```

- **Índices:** `products` por nombre/categoría; `cart_items(user_id)`; `orders(user_id, created_at)`.
- **RLS:** carrito y órdenes solo del propio usuario; catálogo público.
- **Consistencia del stock:** actualizar stock **dentro de la misma transacción** del checkout, no de forma asíncrona.

---

## Paso 4-5: Arquitectura de alto nivel

```
┌─────────┐              ┌─────────────────────────────────────┐
│  Flutter│              │               Supabase              │
│   App   │── HTTPS ───▶ │  ┌────────────┐   ┌──────────────┐  │
│  cache  │              │  │  API/Auth  │──▶│  Postgres    │  │
│ catálogo│◀──────────── │  └────────────┘   │  (RLS, ACID, │  │
└─────────┘   CDN        │  ┌────────────┐   │  transactions)│  │
        ▲                │  │  Cache     │──▶└──────────────┘  │
        │                │  │ (catálogo) │                     │
        │                │  └────────────┘                     │
┌───────┴───────┐        │  ┌────────────┐                     │
│  Edge Func.   │        │  │  Payments  │ (mock provider)     │
│  checkout     │        │  └────────────┘                     │
└───────────────┘        └─────────────────────────────────────┘
```

**Componentes:**
1. **App:** cache del catálogo (lee rápido, offline del catálogo).
2. **CDN:** imágenes de productos.
3. **Cache:** catálogo/búsqueda.
4. **Postgres:** carrito, órdenes, stock — con transacciones.
5. **Edge Function (checkout):** lógica crítica con pago.

---

## Paso 6: Decisiones de diseño con trade-offs

| Decisión | Por qué | Trade-off aceptado |
|---|---|---|
| Catálogo con cache-aside | Lecturas 10:1, sin datos críticos | Stock visible puede estar desfasado (mostrar "últimas unidades") |
| **Checkout transaccional (ACID)** | Dinero y stock no admiten eventual | Checkout es más lento que el resto |
| Edge Function para checkout | Lógica crítica aislada + pago | Complejidad de despliegue |
| Stock con cola asíncrona (para cupos) | Ventas masivas | Backpressure + monitoreo de cola |
| RLS por usuario en carrito/órdenes | Aislamiento de datos | Nada accesible vía API directa |

### Flujo del checkout (sin race condition)
```
1. App envía orden a la Edge Function
2. Edge Function abre transacción en Postgres:
   a. SELECT stock FOR UPDATE del producto  ← evita oversell
   b. valida stock >= qty; si no → error "sin stock"
   c. resta stock, inserta order + order_items
   d. COMMIT
3. Se llama al provider de pago (mock) → estado "paid"
4. Se invalida el cache del producto (stock nuevo)
```

> El `FOR UPDATE` (locking) dentro de la transacción es lo que **previene dos compradores** de llevarse la última unidad simultáneamente.

---

## Paso 7: Consistencia y disponibilidad

- **Modelo:** strong consistency en checkout (ACID), eventual en catálogo (cache).
- **SLA:** checkout 99.99% (dinero en juego); catálogo 99.9%.
- **Patrones:** idempotencia en pagos (mismo order id no paga dos veces), retries con backoff en la app, fallback de catálogo con cache local.

**Justificación CAP:** el checkout elige **CP** (prefiere rechazar una venta antes que dejar pasar un oversell); el catálogo elige **AP** (siempre muestra productos, aunque el stock exacto sea eventual).

---

## Paso 8-9: Seguridad y observabilidad

**Seguridad:**
- Precios/total **nunca vienen de la app** (se calculan en el servidor).
- Idempotencia: el cliente no puede duplicar cargos.
- RLS por usuario; service role solo en la Edge Function.
- Cifrado de datos de pago (PII) — PCI-DSS si es producción real.

**Observabilidad:**
| Métrica | Alerta |
|---|---|
| Tasa de checkout fallidos > 1% | Revisar transacciones/pago |
| Stock en 0 con pedidos fallidos | Revisar locking y cola |
| Latencia de checkout p95 > 2s | Revisar Edge Function/DB |
| Errores de pago | Revisar provider + idempotencia |

---

## Paso 10: Riesgos y evolución

| Riesgo | Mitigación |
|---|---|
| Oversell en pico | Transacciones + FOR UPDATE + verificación final |
| Cache del stock desactualizado | Mostrar "pocas unidades" + invalidación al vender |
| Pago fallido a mitad del checkout | Estados de orden (pending/paid/failed) + reintento idempotente |
| Escalar checkout | Particionar órdenes por usuario; colas por lote |

---

## Fuentes del caso

- [ByteByteGo — How to Design an E-commerce System](https://bytebytego.com/guides/ecommerce-system)
- [ByteByteGo — How to Design a Flash Sale System](https://bytebytego.com/guides/flash-sale-system)
- [Supabase Docs — PostgreSQL Transactions](https://supabase.com/docs/guides/database/postgres/transactions)
- [Designing Data-Intensive Applications — M. Kleppmann](https://dataintensive.net/) (transacciones y aislamiento)

---

**Siguiente:** [15-caso-saas-multi-tenant.md](./15-caso-saas-multi-tenant.md)
