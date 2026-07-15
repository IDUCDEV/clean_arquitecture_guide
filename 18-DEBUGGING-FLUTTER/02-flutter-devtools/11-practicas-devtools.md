# 11 - Prácticas y Ejercicios - Flutter DevTools

## Ejercicio 1: Inspector - Debug de Layout Overflow

### Contexto
Un Row con tres Expanded containers causa overflow en pantallas pequeñas.

### Setup del proyecto

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

### Ejercicio paso a paso

#### Paso 1: Identificar el overflow
1. Ejecutar app en modo debug
2. Abrir DevTools → Inspector
3. Activar "Toggle Debug Paint"
4. Rotar dispositivo o cambiar tamaño de ventana
5. Observar el banner amarillo de overflow

#### Paso 2: Analizar en Layout Explorer
1. Seleccionar el `Row` en Widget Tree
2. Ver en Layout Explorer:
   - Parent constraints: `0 ≤ width ≤ 411`
   - Children flex: `2 + 3 + 1 = 6`
   - Cada child intenta usar más espacio del disponible

#### Paso 3: Diagnóstico
En Debug Console, durante breakpoint en el build:
```dart
MediaQuery.of(context).size.width  // 411px
// Expanded calcula: 411 / 6 * flex
// Container 1: 411/6*2 = 137px ✓
// Column 1: 411/6*3 = 205.5px ✓
// Column 2: 411/6*1 = 68.5px ← ¡Muy poco para contenido!
```

#### Paso 4: Fix con Wrap

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

#### Paso 5: Verificar fix
1. Hot Restart
2. Verificar en Inspector que no hay overflow
3. Verificar en diferentes tamaños de pantalla

---

## Ejercicio 2: Performance - Optimización de ListView

### Contexto
Un ListView con 10,000 items causa jank al hacer scroll.

### Setup

**`lib/features/products/presentation/screens/products_list_screen.dart`**
```dart
class ProductsListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Products')),
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

### Ejercicio paso a paso

#### Paso 1: Medir Performance
1. Abrir DevTools → Performance
2. Empezar grabación
3. Hacer scroll rápido por la lista
4. Detener grabación
5. Analizar frames: ¿cuántos son > 16ms?

#### Paso 2: Identificar causa
En Frame Analysis:
```
Frame #1234:
├── Build Phase: 120ms ← ¡Muy alto!
│   └── ListView.build: 118ms
│       └── List.generate: 115ms
└── Total: 125ms (JANK!)
```

#### Paso 3: Fix con ListView.builder

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: Text('Products')),
    body: ListView.builder(
      itemCount: 10000,
      itemBuilder: (context, i) {
        return ListTile(
          leading: CircleAvatar(child: Text('${i + 1}')),
          title: Text('Product ${i + 1}'),
          subtitle: Text('Description for product ${i + 1}'),
          trailing: Icon(Icons.chevron_right),
        );
      },
    ),
  );
}
```

#### Paso 4: Re-medir Performance
1. Hot Restart
2. Grabar Performance de nuevo
3. Hacer scroll
4. Comparar: ¿mejoró el frame time?

#### Paso 5: Documentar resultados

| Métrica | Antes | Después |
|---------|-------|---------|
| Promedio frame time | 125ms | 12ms |
| Max frame time | 340ms | 18ms |
| Frames > 16ms | 89% | 2% |
| Construcción inicial | 2300ms | 45ms |

---

## Ejercicio 3: Memory - Detectar y fixear leak

### Contexto
Navegar a una pantalla 10 veces incrementa memoria en 50MB sin liberarse.

### Setup

**`lib/features/chat/presentation/screens/chat_screen.dart`**
```dart
class ChatScreen extends StatefulWidget {
  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<StreamSubscription> _subscriptions = [];
  final List<AnimationController> _controllers = [];
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
        // Handle messages
      }),
    );
    
    // Animación
    final controller = AnimationController(
      vsync: this,
      duration: Duration(seconds: 2),
    )..repeat();
    _controllers.add(controller);
    
    // Timer para actualizar online status
    _subscriptions.add(
      Timer.periodic(Duration(seconds: 30), (_) {
        // Update online status
      }) as StreamSubscription,
    );
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Chat')),
      body: TextField(controller: _controller),
    );
  }
  
  // ❌ NO tiene dispose() - ¡MEMORY LEAK!
}
```

### Ejercicio paso a paso

#### Paso 1: Confirmar leak con Memory
1. Abrir DevTools → Memory
2. Tomar snapshot baseline
3. Navegar a ChatScreen 10 veces
4. Tomar segundo snapshot
5. Comparar: `_ChatScreenState` tiene 10 instancias (debería ser 1)

#### Paso 2: Identificar referencias
En el snapshot, expandir `_ChatScreenState`:
```
_ChatScreenState (10 instances)
├── _subscriptions: List<StreamSubscription> (30 items)
├── _controllers: List<AnimationController> (10 items)
└── _controller: TextEditingController (10 items)
```

#### Paso 3: Fix - Agregar dispose

```dart
@override
void dispose() {
  // Cancelar suscripciones
  for (final sub in _subscriptions) {
    sub.cancel();
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

#### Paso 4: Verificar fix
1. Hot Restart
2. Repetir paso 1
3. Verificar que instancias de `_ChatScreenState` se eliminan

#### Paso 5: Documentar resultados

| Métrica | Antes (sin dispose) | Después (con dispose) |
|---------|---------------------|----------------------|
| Instancias después de 10 navs | 10 | 1 |
| Memoria después de 10 navs | +50MB | +2MB |
| Stream subscriptions | 30 (leaked) | 0 (disposed) |
| Animation controllers | 10 (leaked) | 0 (disposed) |

---

## Ejercicio 4: Network - Debug de API lenta

### Contexto
La pantalla de perfil tarda 3 segundos en cargar. Necesitas identificar qué llamada es lenta.

### Setup

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
    if (_isLoading) return CircularProgressIndicator();
    // ... build UI
  }
}
```

### Ejercicio paso a paso

#### Paso 1: Medir con Network View
1. Abrir DevTools → Network
2. Navegar a ProfileScreen
3. Ver las 3 llamadas secuenciales:
```
GET /rest/v1/users?id=eq.123     → 800ms
GET /rest/v1/orders?user_id=eq.123 → 1200ms
POST /rest/v1/rpc/get_user_stats   → 900ms
Total secuencial: 2900ms
```

#### Paso 2: Identificar problema
Las llamadas son secuenciales. Se podrían hacer en paralelo.

#### Paso 3: Fix con Future.wait

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

#### Paso 4: Re-medir
```
GET /rest/v1/users?id=eq.123     → 800ms ─┐
GET /rest/v1/orders?user_id=eq.123 → 1200ms ├─ En paralelo
POST /rest/v1/rpc/get_user_stats   → 900ms ─┘
Total paralelo: 1200ms (más lento de los 3)
```

#### Paso 5: Documentar

| Métrica | Antes (secuencial) | Después (paralelo) |
|---------|---------------------|-------------------|
| Total time | 2900ms | 1200ms |
| Mejora | - | 59% más rápido |
| UX | Lento | Aceptable |

---

## Ejercicio 5: CPU Profiler - Optimización de widget

### Contexto
Un widget de lista se reconstruye completamente cada segundo por un timer.

### Setup

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
    Timer.periodic(Duration(seconds: 1), (_) async {
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

### Ejercicio paso a paso

#### Paso 1: Medir con CPU Profiler
1. Abrir DevTools → CPU Profiler
2. Grabar 10 segundos
3. Ver Flame Chart:
```
buildScope: 340 samples (34%)
├── _LiveStatsWidgetState.build: 280
│   └── ExpensiveChart.build: 260  ← ¡Cuello de botella!
└── Other widgets: 60
```

#### Paso 2: Identificar problema
`ExpensiveChart` se reconstruye cada segundo porque está dentro del `setState`.

#### Paso 3: Fix con RepaintBoundary + selective rebuild

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
    Timer.periodic(Duration(seconds: 1), (_) async {
      final stats = await Supabase.instance.client.rpc('get_live_stats');
      
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
          // Solo este widget se reconstruye cuando cambian datos
          RepaintBoundary(
            child: ValueListenableBuilder<List<double>>(
              valueListenable: _chartData,
              builder: (context, data, child) {
                return ExpensiveChart(data: data);
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

#### Paso 4: Re-medir
```
buildScope: 85 samples (8.5%)  ← ¡Reducción de 75%!
├── _LiveStatsWidgetState.build: 60
│   └── Text widgets: 30 (ligeros)
└── ExpensiveChart: 25 (solo cuando cambian datos)
```

#### Paso 5: Documentar

| Métrica | Antes | Después |
|---------|-------|---------|
| CPU samples (build) | 340 (34%) | 85 (8.5%) |
| ExpensiveChart rebuilds/s | 1 | 1 (pero aislado) |
| Frame time promedio | 28ms | 11ms |
| Jank frames | 45% | 3% |

---

## Ejercicio Integrador: Debug completo de feature

### Contexto
App de e-commerce con pantalla de checkout que tiene múltiples problemas:
1. Layout overflow en botón de pago
2. Llamada API lenta
3. Memory leak en validación de tarjeta
4. Jank al mostrar animation de confirmación

### Archivos del ejercicio

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
      appBar: AppBar(title: Text('Checkout')),
      body: Column(
        children: [
          // Resumen del pedido
          OrderSummary(),
          
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
            child: Text('Pay \$99.99'),
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
        builder: (_) => PaymentSuccessScreen(),
      ));
    }
  }
  
  // ❌ No tiene dispose() - ¡MEMORY LEAK!
}
```

**`lib/features/checkout/presentation/widgets/order_summary.dart`**
```dart
class OrderSummary extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      child: Column(
        children: [
          Text('Order #1234'),
          Text('Total: \$99.99'),
          Text('Items: 3'),
          // Expensive widget que se reconstruye
          LiveExchangeRate(),
        ],
      ),
    );
  }
}
```

**`lib/features/checkout/presentation/screens/payment_success_screen.dart`**
```dart
class PaymentSuccessScreen extends StatefulWidget {
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
      duration: Duration(milliseconds: 600),
    );
    _scaleAnimation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _controller, curve: Curves.elasticOut),
    );
    _controller.forward();
  }
  
  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _scaleAnimation,
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.check_circle, size: 100, color: Colors.green),
            Text('Payment Successful!'),
          ],
        ),
      ),
    );
  }
}
```

### Flujo de debugging paso a paso

#### Paso 1: Diagnosticar overflow
1. Ejecutar app
2. Ir a CheckoutScreen
3. Ver overflow en Row de text fields
4. **Fix**: Usar Wrap o Column en lugar de Row

#### Paso 2: Medir Performance
1. Abrir Performance
2. Grabar al hacer click en "Pay"
3. Identificar frame jank
4. **Fix**: Usar Future.wait para llamadas paralelas

#### Paso 3: Detectar memory leak
1. Abrir Memory
2. Tomar snapshot antes y después de checkout
3. Verificar instancias de CheckoutScreen
4. **Fix**: Agregar dispose() con cancelación de streams y controllers

#### Paso 4: Optimizar animation
1. Abrir CPU Profiler
2. Grabar durante la animación
3. Verificar si ExpensiveChart se reconstruye
4. **Fix**: Aislar con RepaintBoundary

#### Paso 5: Verificar con Network
1. Abrir Network View
2. Verificar tiempos de llamadas API
3. Confirmar que las paralelas son más rápidas

### Checklist final

| Problema | Herramienta | Fix | Verificado |
|----------|-------------|-----|------------|
| Layout overflow | Inspector | Wrap | ☐ |
| API lenta | Network | Future.wait | ☐ |
| Memory leak | Memory | dispose() | ☐ |
| Jank animation | CPU Profiler | RepaintBoundary | ☐ |

---
→ Fin del módulo 02-flutter-devtools
→ Volver a `README.md` del módulo 18
