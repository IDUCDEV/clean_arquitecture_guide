# 18 — Prácticas y Ejercicios con DevTools

> Cinco ejercicios guiados + un ejercicio integrador para practicar el debugging completo con DevTools.

---

## 1. Ejercicio 1: Inspector — Debug de Layout Overflow

### 1.1 Contexto

Un `Row` con tres `Expanded` containers causa overflow en pantallas pequeñas.

### 1.2 Setup del proyecto

**`lib/features/home/presentation/widgets/product_row.dart`**

```dart
class ProductRow extends StatelessWidget {
  final Product product;

  const ProductRow({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          flex: 2,
          child: Container(
            height: 80,
            color: Colors.blue.shade100,
            child: Image.network(product.imageUrl),
          ),
        ),
        Expanded(
          flex: 3,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(product.name, style: TextStyle(fontWeight: FontWeight.bold)),
              Text(product.description, maxLines: 2, overflow: TextOverflow.ellipsis),
            ],
          ),
        ),
        Expanded(
          flex: 1,
          child: Column(
            children: [
              Text('\$${product.price}'),
              IconButton(
                icon: Icon(Icons.add_shopping_cart),
                onPressed: () {},
              ),
            ],
          ),
        ),
      ],
    );
  }
}
```

### 1.3 Ejercicio paso a paso

#### Paso 1: identificar el overflow

1. Ejecutar la app en modo debug
2. Abrir DevTools → Inspector
3. Activar **Toggle Debug Paint**
4. Rotar el dispositivo o cambiar el tamaño de ventana
5. Observar el banner amarillo de overflow

#### Paso 2: analizar en Layout Explorer

1. Seleccionar el `Row` en el Widget Tree
2. Ver en Layout Explorer:
   - Parent constraints: `0 ≤ width ≤ 411`
   - Children flex: `2 + 3 + 1 = 6`
   - Cada child intenta usar más espacio del disponible

#### Paso 3: diagnóstico

En la Debug Console, durante un breakpoint en el build:

```dart
MediaQuery.sizeOf(context).width  // 411px
// Expanded calcula: 411 / 6 * flex
// Container 1: 411/6*2 = 137px ✓
// Column 1: 411/6*3 = 205.5px ✓
// Column 2: 411/6*1 = 68.5px ← ¡Muy poco para el contenido!
```

#### Paso 4: fix con Wrap

```dart
@override
Widget build(BuildContext context) {
  return Wrap(
    spacing: 8,
    runSpacing: 8,
    children: [
      SizedBox(
        width: 80,
        height: 80,
        child: Image.network(product.imageUrl),
      ),
      SizedBox(
        width: 200,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(product.name, style: TextStyle(fontWeight: FontWeight.bold)),
            Text(product.description, maxLines: 2, overflow: TextOverflow.ellipsis),
          ],
        ),
      ),
      Column(
        children: [
          Text('\$${product.price}'),
          IconButton(
            icon: Icon(Icons.add_shopping_cart),
            onPressed: () {},
          ),
        ],
      ),
    ],
  );
}
```

#### Paso 5: verificar el fix

1. Hot Restart
2. Verificar en Inspector que no hay overflow
3. Verificar en diferentes tamaños de pantalla

---

## 2. Ejercicio 2: Performance — Optimización de ListView

### 2.1 Contexto

Un `ListView` con 10,000 items causa jank al hacer scroll.

### 2.2 Setup

**`lib/features/products/presentation/screens/products_list_screen.dart`**

```dart
class ProductsListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Products')),
      body: ListView(
        children: List.generate(
          10000,
          (i) => ListTile(
            leading: CircleAvatar(child: Text('${i + 1}')),
            title: Text('Product ${i + 1}'),
            subtitle: Text('Description for product ${i + 1}'),
            trailing: Icon(Icons.chevron_right),
          ),
        ),
      ),
    );
  }
}
```

### 2.3 Ejercicio paso a paso

#### Paso 1: medir Performance

1. Abrir DevTools → Performance
2. Empezar la grabación
3. Hacer scroll rápido por la lista
4. Detener la grabación
5. Analizar frames: ¿cuántos son > 16 ms?

#### Paso 2: identificar la causa

En Frame Analysis:

```
Frame #1234:
├── Build Phase: 120ms ← ¡Muy alto!
│   └── ListView.build: 118ms
│       └── List.generate: 115ms
└── Total: 125ms (JANK!)
```

#### Paso 3: fix con ListView.builder

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: const Text('Products')),
    body: ListView.builder(
      itemCount: 10000,
      itemBuilder: (context, i) {
        return ListTile(
          leading: CircleAvatar(child: Text('${i + 1}')),
          title: Text('Product ${i + 1}'),
          subtitle: Text('Description for product ${i + 1}'),
          trailing: const Icon(Icons.chevron_right),
        );
      },
    ),
  );
}
```

#### Paso 4: re-medir Performance

1. Hot Restart
2. Grabar Performance de nuevo
3. Hacer scroll
4. Comparar: ¿mejoró el frame time?

#### Paso 5: documentar resultados

| Métrica | Antes | Después |
|---|---|---|
| Promedio frame time | 125 ms | 12 ms |
| Max frame time | 340 ms | 18 ms |
| Frames > 16 ms | 89% | 2% |
| Construcción inicial | 2300 ms | 45 ms |

---

## 3. Ejercicio 3: Memory — Detectar y arreglar un leak

### 3.1 Contexto

Navegar a una pantalla 10 veces incrementa la memoria en 50 MB sin liberarse.

### 3.2 Setup

**`lib/features/chat/presentation/screens/chat_screen.dart`**

```dart
class ChatScreen extends StatefulWidget {
  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<StreamSubscription> _subscriptions = [];
  final List<AnimationController> _controllers = [];
  final List<Timer> _timers = [];
  final TextEditingController _controller = TextEditingController();

  @override
  void initState() {
    super.initState();

    // Suscripción a mensajes en tiempo real
    _subscriptions.add(
      Supabase.instance.client
          .from('messages')
          .stream(primaryKey: ['id'])
          .listen((data) {
        // Manejar mensajes
      }),
    );

    // Animación
    final controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat();
    _controllers.add(controller);

    // Timer para actualizar online status
    _timers.add(
      Timer.periodic(const Duration(seconds: 30), (_) {
        // Update online status
      }),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chat')),
      body: TextField(controller: _controller),
    );
  }

  // ❌ NO tiene dispose() - ¡MEMORY LEAK!
}
```

### 3.3 Ejercicio paso a paso

#### Paso 1: confirmar el leak con Memory

1. Abrir DevTools → Memory
2. Tomar snapshot baseline
3. Navegar a ChatScreen 10 veces
4. Tomar segundo snapshot
5. Comparar: `_ChatScreenState` tiene 10 instancias (debería ser 1)

#### Paso 2: identificar referencias

En el snapshot, expandir `_ChatScreenState`:

```
_ChatScreenState (10 instances)
├── _subscriptions: List<StreamSubscription> (10 items)
├── _controllers: List<AnimationController> (10 items)
├── _timers: List<Timer> (10 items)
└── _controller: TextEditingController (10 items)
```

#### Paso 3: fix — agregar dispose

```dart
@override
void dispose() {
  // Cancelar suscripciones
  for (final sub in _subscriptions) {
    sub.cancel();
  }

  // Cancelar timers
  for (final timer in _timers) {
    timer.cancel();
  }

  // Dispose controllers
  for (final controller in _controllers) {
    controller.dispose();
  }

  // Dispose text controller
  _controller.dispose();

  super.dispose();
}
```

#### Paso 4: verificar el fix

1. Hot Restart
2. Repetir el paso 1
3. Verificar que las instancias de `_ChatScreenState` se eliminan

#### Paso 5: documentar resultados

| Métrica | Antes (sin dispose) | Después (con dispose) |
|---|---|---|
| Instancias después de 10 navegaciones | 10 | 1 |
| Memoria después de 10 navegaciones | +50 MB | +2 MB |
| Stream subscriptions | 10 (leaked) | 0 (disposed) |
| Animation controllers | 10 (leaked) | 0 (disposed) |

---

## 4. Ejercicio 4: Network — Debug de API lenta

### 4.1 Contexto

La pantalla de perfil tarda 3 segundos en cargar. Necesitas identificar qué llamada es lenta.

### 4.2 Setup

**`lib/features/profile/presentation/screens/profile_screen.dart`**

```dart
class ProfileScreen extends StatefulWidget {
  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  UserModel? _user;
  List<OrderModel> _orders = [];
  Map<String, dynamic>? _stats;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    final user = await Supabase.instance.client.auth.currentUser;

    // Llamadas secuenciales (¡INEFICIENTE!)
    final userData = await Supabase.instance.client
        .from('users')
        .select()
        .eq('id', user!.id)
        .single();

    final orders = await Supabase.instance.client
        .from('orders')
        .select()
        .eq('user_id', user.id)
        .order('created_at', ascending: false);

    final stats = await Supabase.instance.client
        .rpc('get_user_stats', params: {'user_id': user.id});

    setState(() {
      _user = UserModel.fromJson(userData);
      _orders = (orders as List).map((o) => OrderModel.fromJson(o)).toList();
      _stats = stats;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) return const CircularProgressIndicator();
    // ... build UI
  }
}
```

### 4.3 Ejercicio paso a paso

#### Paso 1: medir con Network View

1. Abrir DevTools → Network
2. Navegar a ProfileScreen
3. Ver las 3 llamadas secuenciales:

```
GET /rest/v1/users?id=eq.123     → 800ms
GET /rest/v1/orders?user_id=eq.123 → 1200ms
POST /rest/v1/rpc/get_user_stats   → 900ms
Total secuencial: 2900ms
```

#### Paso 2: identificar el problema

Las llamadas son secuenciales. Se podrían hacer en paralelo.

#### Paso 3: fix con Future.wait

```dart
Future<void> _loadData() async {
  final user = await Supabase.instance.client.auth.currentUser;

  // Llamadas en paralelo (¡EFICIENTE!)
  final results = await Future.wait([
    Supabase.instance.client
        .from('users')
        .select()
        .eq('id', user!.id)
        .single(),
    Supabase.instance.client
        .from('orders')
        .select()
        .eq('user_id', user.id)
        .order('created_at', ascending: false),
    Supabase.instance.client
        .rpc('get_user_stats', params: {'user_id': user.id}),
  ]);

  setState(() {
    _user = UserModel.fromJson(results[0] as Map<String, dynamic>);
    _orders = (results[1] as List).map((o) => OrderModel.fromJson(o)).toList();
    _stats = results[2] as Map<String, dynamic>;
    _isLoading = false;
  });
}
```

#### Paso 4: re-medir

```
GET /rest/v1/users?id=eq.123      → 800ms ─┐
GET /rest/v1/orders?user_id=eq.123 → 1200ms ├─ En paralelo
POST /rest/v1/rpc/get_user_stats    → 900ms ─┘
Total paralelo: 1200ms (el más lento de los 3)
```

#### Paso 5: documentar

| Métrica | Antes (secuencial) | Después (paralelo) |
|---|---|---|
| Total time | 2900 ms | 1200 ms |
| Mejora | – | 59% más rápido |
| UX | Lento | Aceptable |

---

## 5. Ejercicio 5: CPU Profiler — Optimización de widget

### 5.1 Contexto

Un widget de lista se reconstruye completamente cada segundo por un timer.

### 5.2 Setup

**`lib/features/dashboard/presentation/widgets/live_stats_widget.dart`**

```dart
class LiveStatsWidget extends StatefulWidget {
  @override
  State<LiveStatsWidget> createState() => _LiveStatsWidgetState();
}

class _LiveStatsWidgetState extends State<LiveStatsWidget> {
  int _activeUsers = 0;
  int _totalOrders = 0;
  double _revenue = 0;

  @override
  void initState() {
    super.initState();
    _startUpdates();
  }

  void _startUpdates() {
    Timer.periodic(const Duration(seconds: 1), (_) async {
      final stats = await Supabase.instance.client
          .rpc('get_live_stats');

      setState(() {
        _activeUsers = stats['active_users'];
        _totalOrders = stats['total_orders'];
        _revenue = stats['revenue'].toDouble();
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          Text('Active Users: $_activeUsers'),
          Text('Total Orders: $_totalOrders'),
          Text('Revenue: \$${_revenue.toStringAsFixed(2)}'),
          // Widget pesado que NO debería reconstruirse
          ExpensiveChart(data: [_activeUsers, _totalOrders, _revenue]),
        ],
      ),
    );
  }
}
```

### 5.3 Ejercicio paso a paso

#### Paso 1: medir con CPU Profiler

1. Abrir DevTools → CPU Profiler
2. Grabar 10 segundos
3. Ver el Flame Chart:

```
buildScope: 340 samples (34%)
├── _LiveStatsWidgetState.build: 280
│   └── ExpensiveChart.build: 260  ← ¡Cuello de botella!
└── Other widgets: 60
```

#### Paso 2: identificar el problema

`ExpensiveChart` se reconstruye cada segundo porque está dentro del `setState`.

#### Paso 3: fix con ValueNotifier + reconstrucción selectiva

```dart
class _LiveStatsWidgetState extends State<LiveStatsWidget> {
  int _activeUsers = 0;
  int _totalOrders = 0;
  double _revenue = 0;

  // Fuente de datos para el chart, actualizada por separado
  final ValueNotifier<List<double>> _chartData = ValueNotifier([]);

  @override
  void initState() {
    super.initState();
    _startUpdates();
  }

  void _startUpdates() {
    Timer.periodic(const Duration(seconds: 1), (_) async {
      final stats = await Supabase.instance.client.rpc('get_live_stats');

      final active = stats['active_users'];
      final total = stats['total_orders'];
      final revenue = stats['revenue'].toDouble();

      // El chart solo escucha el ValueNotifier
      _chartData.value = [active, total, revenue];

      if (mounted) {
        setState(() {
          _activeUsers = active;
          _totalOrders = total;
          _revenue = revenue;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          Text('Active Users: $_activeUsers'),
          Text('Total Orders: $_totalOrders'),
          Text('Revenue: \$${_revenue.toStringAsFixed(2)}'),
          // Solo se reconstruye cuando cambian los datos del chart
          ValueListenableBuilder<List<double>>(
            valueListenable: _chartData,
            builder: (context, data, child) {
              return ExpensiveChart(data: data);
            },
          ),
        ],
      ),
    );
  }
}
```

#### Paso 4: re-medir

```
buildScope: 85 samples (8.5%)  ← ¡Reducción de 75%!
├── _LiveStatsWidgetState.build: 60
│   └── Text widgets: 30 (ligeros)
└── ExpensiveChart: 25 (solo cuando cambian datos)
```

#### Paso 5: documentar

| Métrica | Antes | Después |
|---|---|---|
| CPU samples (build) | 340 (34%) | 85 (8.5%) |
| ExpensiveChart rebuilds/s | 1 (junto al resto) | 1 (aislado) |
| Frame time promedio | 28 ms | 11 ms |
| Jank frames | 45% | 3% |

---

## 6. Ejercicio Integrador: Debug completo de una feature

### 6.1 Contexto

App de e-commerce con una pantalla de checkout que tiene múltiples problemas:

1. Layout overflow en el botón de pago
2. Llamada API lenta
3. Memory leak en la validación de tarjeta
4. Jank al mostrar la animación de confirmación

### 6.2 Archivos del ejercicio

**`lib/features/checkout/presentation/screens/checkout_screen.dart`**

```dart
class CheckoutScreen extends StatefulWidget {
  @override
  State<CheckoutScreen> createState() => _CheckoutScreenState();
}

class _CheckoutScreenState extends State<CheckoutScreen> {
  final _cardController = TextEditingController();
  final _expiryController = TextEditingController();
  final _cvvController = TextEditingController();
  StreamSubscription? _validationSubscription;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Checkout')),
      body: Column(
        children: [
          // Resumen del pedido
          const OrderSummary(),

          // Formulario de pago (¡overflow aquí!)
          Row(
            children: [
              Expanded(child: TextField(controller: _cardController)),
              Expanded(child: TextField(controller: _expiryController)),
              Expanded(child: TextField(controller: _cvvController)),
            ],
          ),

          // Botón de pago
          ElevatedButton(
            onPressed: _processPayment,
            child: const Text('Pay \$99.99'),
          ),
        ],
      ),
    );
  }

  Future<void> _processPayment() async {
    // Llamada secuencial (¡lenta!)
    final token = await Supabase.instance.client.functions.invoke('create-payment');
    final result = await Supabase.instance.client.functions.invoke('process-payment');

    if (result.status == 200) {
      Navigator.push(context, MaterialPageRoute(
        builder: (_) => const PaymentSuccessScreen(),
      ));
    }
  }

  // ❌ No tiene dispose() - ¡MEMORY LEAK!
}
```

**`lib/features/checkout/presentation/widgets/order_summary.dart`**

```dart
class OrderSummary extends StatelessWidget {
  const OrderSummary({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          const Text('Order #1234'),
          const Text('Total: \$99.99'),
          const Text('Items: 3'),
          // Expensive widget que se reconstruye
          const LiveExchangeRate(),
        ],
      ),
    );
  }
}
```

**`lib/features/checkout/presentation/screens/payment_success_screen.dart`**

```dart
class PaymentSuccessScreen extends StatefulWidget {
  const PaymentSuccessScreen({super.key});

  @override
  State<PaymentSuccessScreen> createState() => _PaymentSuccessScreenState();
}

class _PaymentSuccessScreenState extends State<PaymentSuccessScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );
    _scaleAnimation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _controller, curve: Curves.elasticOut),
    );
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _scaleAnimation,
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.check_circle, size: 100, color: Colors.green),
            const Text('Payment Successful!'),
          ],
        ),
      ),
    );
  }
}
```

### 6.3 Flujo de debugging paso a paso

#### Paso 1: diagnosticar overflow

1. Ejecutar la app
2. Ir a CheckoutScreen
3. Ver el overflow en el Row de text fields
4. **Fix**: usar Wrap o Column en lugar de Row

#### Paso 2: medir Performance

1. Abrir Performance
2. Grabar al hacer click en "Pay"
3. Identificar el frame jank
4. **Fix**: usar Future.wait para llamadas paralelas

#### Paso 3: detectar el memory leak

1. Abrir Memory
2. Tomar snapshot antes y después del checkout
3. Verificar las instancias de CheckoutScreen
4. **Fix**: agregar `dispose()` con cancelación de streams y controllers

#### Paso 4: optimizar la animación

1. Abrir CPU Profiler
2. Grabar durante la animación
3. Verificar si ExpensiveChart se reconstruye
4. **Fix**: aislar con RepaintBoundary / ValueListenableBuilder

#### Paso 5: verificar con Network

1. Abrir Network View
2. Verificar los tiempos de las llamadas API
3. Confirmar que las paralelas son más rápidas

### 6.4 Checklist final

| Problema | Herramienta | Fix | Verificado |
|---|---|---|---|
| Layout overflow | Inspector | Wrap | ☐ |
| API lenta | Network | Future.wait | ☐ |
| Memory leak | Memory | dispose() | ☐ |
| Jank animation | CPU Profiler | RepaintBoundary | ☐ |

---

## Resumen

| Ejercicio | Herramienta | Lección clave |
|---|---|---|
| Layout overflow | Inspector | Constraints y flex |
| ListView 10k items | Performance | `ListView.builder` |
| Leak en ChatScreen | Memory | `dispose()` completo |
| API lenta | Network | `Future.wait` en paralelo |
| Rebuild cada segundo | CPU Profiler | `ValueListenableBuilder` |

---

## 📚 Referencias

- [Flutter | DevTools](https://docs.flutter.dev/tools/devtools) — Documentación oficial de DevTools
- [Flutter | Performance best practices](https://docs.flutter.dev/perf/best-practices) — Buenas prácticas de rendimiento
- [Flutter | Memory](https://docs.flutter.dev/perf/memory) — Gestión de memoria en Flutter

---

> 📖 **Siguiente:** [19-fundamentos-rendimiento.md](./19-fundamentos-rendimiento.md) — Fundamentos de rendimiento: frames, jank y pipelines
