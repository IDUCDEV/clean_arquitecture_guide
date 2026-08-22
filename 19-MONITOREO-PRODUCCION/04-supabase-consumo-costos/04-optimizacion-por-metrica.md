# 04 - Optimizacion por Metrica

> Playbook concreto: por cada metrica de Supabase, que cambiar en tu codigo Flutter para bajar el consumo sin renunciar a funcionalidad. Cada recomendacion incluye codigo real.

---

## 1. Reducir Egresos

El egreso es la suma de datos servidos por Postgres + Storage + Functions. Cada byte que sale cuesta.

### 1.1 Seleccionar columnas explicitas (impacto inmediato)

```dart
// MAL: trae TODO el registro
final rows = await client.from('orders').select();

// BIEN: trae SOLO lo que la UI necesita
final rows = await client
    .from('orders')
    .select('id, created_at, total, status, customer_name');
```

**Impacto:** traer 200 registros con 10 campos vs 20 campos = 50% menos bytes.

### 1.2 Contar sin traer filas

```dart
// MAL: trae todas las filas para contar
final data = await client.from('orders').select();
final count = data.length;

// BIEN: count sin traer filas
final count = await client.from('orders').select('id').count(Count.exact);
```

`Count.exact` para total real. `Count.planned` para listas infinitas (estimado, margen ~2%).

### 1.3 Paginacion con .range()

```dart
class ProductsRepository {
  final SupabaseClient _client;
  static const _pageSize = 20;
  ProductsRepository(this._client);

  Future<List<Product>> getProducts({required int page}) async {
    final from = page * _pageSize;
    final to = from + _pageSize - 1;
    final data = await _client
        .from('products')
        .select('id, name, price, thumbnail_url')
        .range(from, to)
        .order('created_at', ascending: false);
    return data.map(Product.fromJson).toList();
  }
}
```

### 1.4 RPC para logica compleja

```dart
// MAL: 3 queries secuenciales desde el cliente
final cart = await client.from('cart_items').select().eq('user_id', userId);
final products = await client.from('products').select()
    .inFilter('id', cart.map((c) => c['product_id']).toList());
final total = products.fold(0.0, (sum, p) => sum + (p['price'] as num));

// BIEN: 1 query, 1 round-trip
final total = await client.rpc('calculate_cart_total', params: {
  'p_user_id': userId,
});
```

```sql
CREATE OR REPLACE FUNCTION calculate_cart_total(p_user_id uuid)
RETURNS numeric AS $$
  SELECT coalesce(sum(p.price * ci.quantity), 0)
  FROM cart_items ci
  JOIN products p ON p.id = ci.product_id
  WHERE ci.user_id = p_user_id;
$$ LANGUAGE sql STABLE;
```

### 1.5 Transformaciones de imagenes (Pro)

```dart
// MAL: sirves imagen original (5MB)
final url = supabase.storage.from('avatars').getPublicUrl('user1.jpg');

// BIEN: transforma al servir (~4KB)
final url = supabase.storage
    .from('avatars')
    .getPublicUrl('user1.jpg', transform: const TransformOptions(
      width: 200,
      height: 200,
      quality: 80,
      format: ConnectFormat.webp,
    ));
```

---

## 2. Reducir DB Size

### 2.1 Particionar tablas de log

```sql
-- Particionar por mes y borrar viejas
CREATE TABLE audit_log (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  action text,
  created_at timestamptz DEFAULT now()
) PARTITION BY RANGE (created_at);

CREATE TABLE audit_log_2026_08 PARTITION OF audit_log
  FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');

-- Borra particiones viejas
DROP TABLE audit_log_2025_01;
```

### 2.2 Indices eficientes

```sql
-- BIEN: indice parcial (solo pendientes)
CREATE INDEX idx_orders_pendientes
  ON orders (created_at DESC)
  WHERE status = 'pending';

-- BIEN: indice covering (evita ir a la tabla)
CREATE INDEX idx_products_covering
  ON products (category_id) INCLUDE (name, price, thumbnail_url);
```

---

## 3. Minimizar MAU

### 3.1 Evitar login anonimo descontrolado

```dart
// MAL: cada instalacion crea usuario anonimo nuevo
await client.auth.signInAnonymously();
// 1000 instalaciones = 1000 MAU (incluso testers)

// BIEN: solo autenticar cuando es necesario
// Para datos publicos, usa queries sin auth (RLS public)
```

### 3.2 Refresh de token

```dart
// La sesion persistente autorefresca el token al abrir la app.
// Eso cuenta como MAU (correcto para apps reales).
// Evita: signInAnonymously() por cada widget/test
```

---

## 4. Reducir Storage

### 4.1 Comprimir ANTES de subir

```dart
import 'package:image/image.dart' as img;

final image = img.decodeImage(await file.readAsBytes());
final resized = img.copyResize(image!, width: 1024);
final compressed = img.encodeJpg(resized, quality: 80);
await client.storage.from('uploads').uploadBinary(path, compressed);
```

Foto 5MB -> ~200KB comprimida. 96% menos storage y egreso.

### 4.2 Limpieza periodica

```sql
-- Archivos temporales: borrar viejos
DELETE FROM storage.objects
WHERE bucket_id = 'temp-uploads'
  AND created_at < now() - interval '7 days';
```

---

## 5. Reducir Edge Function Invocations

### 5.1 Patron batch

```dart
// MAL: 100 invocaciones
for (final order in orders) {
  await client.functions.invoke('send-email', body: {'order_id': order.id});
}

// BIEN: 1 invocacion
await client.functions.invoke('send-emails-batch', body: {
  'order_ids': orders.map((o) => o.id).toList(),
});
```

### 5.2 RPC en vez de Function

```dart
// MAL: Edge Function que hace query
final result = await client.functions.invoke('get-stats');

// BIEN: RPC directo (no cuenta como invocacion)
final result = await client.rpc('get_stats');
```

---

## 6. Reducir Realtime Messages

### 6.1 Suscripcion con filtro

```dart
// MAL: escucha TODA la tabla
client.channel('public:orders')
    .onPostgresChanges(event: PostgresChangeEvent.insert,
        schema: 'public', table: 'orders',
        callback: (p) => print(p))
    .subscribe();

// BIEN: escucha solo tus datos
client.channel('user-orders:$userId')
    .onPostgresChanges(event: PostgresChangeEvent.insert,
        schema: 'public', table: 'orders',
        filter: PostgresChangeFilter(
          type: PostgresChangeFilterType.eq,
          column: 'user_id', value: userId,
        ),
        callback: (p) => print(p))
    .subscribe();
```

### 6.2 SIEMPRE darse de baja al salir

```dart
class _OrderScreenState extends State<OrderScreen> {
  RealtimeChannel? _channel;

  @override
  void initState() {
    super.initState();
    _channel = Supabase.instance.client.channel('my-orders')
        .onPostgresChanges(event: PostgresChangeEvent.all,
            schema: 'public', table: 'orders',
            filter: PostgresChangeFilter(
              type: PostgresChangeFilterType.eq,
              column: 'user_id',
              value: Supabase.instance.client.auth.currentUser!.id,
            ),
            callback: _onOrderChange)
        .subscribe();
  }

  @override
  void dispose() {
    if (_channel != null) {
      Supabase.instance.client.removeChannel(_channel!);
    }
    super.dispose();
  }
}
```

### 6.3 Preferir Broadcast para eventos simples

```dart
// Para notificaciones simples, Broadcast es mas ligero
await client.channel('room-1')
    .sendBroadcastMessage(event: 'new-notification',
        payload: {'title': 'Pedido enviado'});
```

---

## Resumen: impacto por patron

| Patron | Metrica impactada | Ahorro estimado |
|---|---|---|
| select() con columnas especificas | Egresos | 30-70% |
| .range() paginado | Egresos + DB CPU | 80-95% |
| RPC vs multiples queries | Egresos + Functions | 66-90% |
| Image transform | Egresos + Storage | 99% |
| subscribe + unsubscribe | Realtime | 50-90% |
| Batch en Functions | Function Invocations | 50-99% |
| Comprimir antes de subir | Storage + Egresos | 90-99% |
| Indices parciales + covering | DB Size + CPU | 30-60% |

---

## Siguiente paso

[05-framework-decision-optimizar-vs-upgrade](./05-framework-decision-optimizar-vs-upgrade.md)
