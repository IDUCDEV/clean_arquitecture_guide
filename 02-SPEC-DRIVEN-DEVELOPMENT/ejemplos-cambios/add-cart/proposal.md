# Proposal: add-cart

> Ejemplo walkthrough completo del flujo SDD. Deriva de la práctica "Carrito de Compras" del módulo histórico (ver [trabajar-sin-ia](../../trabajar-sin-ia/)).

## Impacto (Impact Report)
- Features afectadas: ninguna directamente (feature nueva); `products` existente provee catálogo
- Reutilizable: patrón CRUD de features existentes, `Failure` hierarchy en core
- Supabase: tablas nuevas `carts`, `cart_items`, `coupons`; RLS por dueño; migración nº 0007
- DI / rutas: `service_locator.dart` (+8 registros), `app_router.dart` (+1 ruta `/cart` con guard de sesión)
- Riesgos: concurrencia al actualizar stock; cálculo de impuestos duplicado cliente/servidor

## Why (Problema)
Los clientes no pueden acumular productos antes de pagar: cada compra es de un solo artículo. Se pierde ticket promedio y no hay lugar donde aplicar descuentos.

## What Changes (Solución)
Carrito de compras por cliente autenticado: agregar/quitar productos, actualizar cantidades, ver resumen económico (subtotal, impuesto, total) y aplicar cupones de descuento.

## Capabilities
### New Capabilities
- `shopping-cart`: gestión del carrito con validación de stock, reglas económicas y cupones

## Scope (Alcance)
**Incluye:**
- Agregar/quitar productos y actualizar cantidades
- Ver resumen con subtotal, impuesto (16%) y total
- Aplicar cupones de descuento (porcentaje o monto fijo)

**No incluye:**
- Procesar pagos
- Envíos y seguimiento
- Programa de fidelización
- Carritos anónimos (requiere sesión iniciada)

**Dependencias:** catálogo de productos (stock), autenticación
**Suposiciones:** un carrito pertenece a un solo cliente; precio unitario se congela al agregar
**Preguntas abiertas:** ~~¿cupones combinables?~~ → NO (decisión D2); ~~¿límite de items?~~ → RN001 = 50

## Actores y permisos
| Actor | Puede | No puede | Mapeo RLS |
|-------|-------|----------|-----------|
| Cliente | CRUD items propios, aplicar cupón, ver su resumen | Ver/modificar carritos ajenos | `auth.uid() = user_id` |
| Admin | Ver carritos abandonados, ajustar precios | Modificar carrito ajeno | claim `role = 'admin'` solo lectura |
| Inventario | Validar stock vía RPC | Escribir en carts | función security definer |

## Impact
- Código: ~14 ficheros nuevos en `lib/features/cart/`
- Datos: 3 tablas + 1 RPC + políticas RLS + migración 0007
- Breaking changes: ninguno
