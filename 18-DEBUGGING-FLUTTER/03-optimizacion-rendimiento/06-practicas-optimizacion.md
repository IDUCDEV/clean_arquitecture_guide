# 06 - Practicas de Optimizacion de Rendimiento

## Estructura de cada escenario

Cada escenario sigue el mismo patron:
1. **Contexto**: el problema real que enfrentas
2. **Problema**: codigo con el issue
3. **Pasos**: como diagnosticar con DevTools
4. **Solucion**: codigo optimizado
5. **Resultado esperado**: que cambia en la app

---

## Escenario 1: "Lista que se congela"

### Contexto

Tienes una pantalla de contactos con 500 entradas. Cuando el usuario hace scroll, la lista se "congela" momentaneamente cada cierto tiempo. El Performance Overlay muestra frames rojos.

### Problema

```dart
class ContactsScreen extends StatelessWidget {
  final List<Contact> contacts;

  const ContactsScreen({super.key, required this.contacts});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: contacts.map((contact) => ContactTile(
        contact: contact,
      )).toList(),
    );
  }
}

class ContactTile extends StatelessWidget {
  final Contact contact;

  const ContactTile({super.key, required this.contact});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: CircleAvatar(
        child: Text(contact.name[0]),
      ),
      title: Text(contact.name),
      subtitle: Text(contact.email),
      trailing: Icon(
        contact.isFavorite ? Icons.star : Icons.star_border,
      ),
    );
  }
}

class Contact {
  final String id;
  final String name;
  final String email;
  final bool isFavorite;

  Contact({
    required this.id,
    required this.name,
    required this.email,
    required this.isFavorite,
  });
}
```

### Pasos de diagnostico

1. Ejecutar `flutter run --profile`
2. Abrir DevTools > Performance
3. Grabar mientras se hace scroll (5 segundos)
4. Observar frames con build time > 8ms
5. Flame chart muestra que `ContactTile.build()` se ejecuta 500 veces al inicio

### Solucion

```dart
class ContactsScreen extends StatelessWidget {
  final List<Contact> contacts;

  const ContactsScreen({super.key, required this.contacts});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(  // <-- Cambio #1: builder
      itemCount: contacts.length,
      itemBuilder: (context, index) {
        return ContactTile(   // <-- Ahora solo construye ~20 items
          contact: contacts[index],
        );
      },
    );
  }
}

class ContactTile extends StatelessWidget {
  final Contact contact;

  const ContactTile({super.key, required this.contact});  // <-- const

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: CircleAvatar(
        child: Text(contact.name[0]),
      ),
      title: Text(contact.name),
      subtitle: Text(contact.email),
      trailing: Icon(
        contact.isFavorite ? Icons.star : Icons.star_border,
      ),
    );
  }
}
```

### Resultado esperado

| Metrica | Antes | Despues |
|---|---|---|
| Items construidos | 500 | ~20 |
| Build time promedio | 45ms | 3ms |
| Memoria usada | ~80MB | ~15MB |
| Scroll fluidez | Congelada | Suave |

---

## Escenario 2: "Login con rebuilds excesivos"

### Contexto

Un form de login donde cada tecla que escribe el usuario reconstruye toda la pantalla. El Performance Overlay muestra micro-jank continuo. El usuario escribe el email y el form entero parpadea.

### Problema

```dart
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: BlocBuilder<LoginBloc, LoginState>(
          builder: (context, state) {
            return Form(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    'Bienvenido',
                    style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 48),
                  TextFormField(
                    decoration: const InputDecoration(
                      labelText: 'Email',
                      border: OutlineInputBorder(),
                    ),
                    onChanged: (value) {
                      context.read<LoginBloc>().add(LoginEmailChanged(value));
                    },
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    obscureText: true,
                    decoration: const InputDecoration(
                      labelText: 'Password',
                      border: OutlineInputBorder(),
                    ),
                    onChanged: (value) {
                      context.read<LoginBloc>().add(LoginPasswordChanged(value));
                    },
                  ),
                  const SizedBox(height: 24),
                  if (state.isLoading)
                    const CircularProgressIndicator(),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: state.isValid
                        ? () {
                            context.read<LoginBloc>().add(LoginSubmitted());
                          }
                        : null,
                    child: const Text('Iniciar Sesion'),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    state.errorMessage ?? '',
                    style: const TextStyle(color: Colors.red),
                  ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
```

### Pasos de diagnostico

1. Ejecutar `flutter run --profile`
2. DevTools > Performance > Grabar mientras se escribe
3. Observar que `LoginScreen.build()` se ejecuta en cada tecla
4. Enhance Tracing > Widget build rebuilds: todas las widgets se reconstruyen

### Solucion

```dart
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Bienvenido',
                style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 48),
              TextFormField(
                decoration: const InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
                onChanged: (value) {
                  context.read<LoginBloc>().add(LoginEmailChanged(value));
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                obscureText: true,
                decoration: const InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
                onChanged: (value) {
                  context.read<LoginBloc>().add(LoginPasswordChanged(value));
                },
              ),
              const SizedBox(height: 24),
              // Solo el indicador y boton usan el estado
              const _LoginActions(),
            ],
          ),
        ),
      ),
    );
  }
}

class _LoginActions extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        BlocSelector<LoginBloc, LoginState, bool>(
          selector: (state) => state.isLoading,
          builder: (context, isLoading) {
            return isLoading
                ? const CircularProgressIndicator()
                : const SizedBox.shrink();
          },
        ),
        const SizedBox(height: 16),
        BlocSelector<LoginBloc, LoginState, bool>(
          selector: (state) => state.isValid,
          builder: (context, isValid) {
            return ElevatedButton(
              onPressed: isValid
                  ? () {
                      context.read<LoginBloc>().add(LoginSubmitted());
                    }
                  : null,
              child: const Text('Iniciar Sesion'),
            );
          },
        ),
        const SizedBox(height: 16),
        BlocSelector<LoginBloc, LoginState, String?>(
          selector: (state) => state.errorMessage,
          builder: (context, errorMessage) {
            return Text(
              errorMessage ?? '',
              style: const TextStyle(color: Colors.red),
            );
          },
        ),
      ],
    );
  }
}
```

### Resultado esperado

| Metrica | Antes | Despues |
|---|---|---|
| Widgets rebuild por tecla | ~15 | 3 |
| Build time promedio | 12ms | 1ms |
| UI response time | 45ms | 8ms |
| Parpadeo visible | Si | No |

---

## Escenario 3: "Chat con memory leak"

### Contexto

Un app de chat que escucha mensajes en tiempo real via Supabase. Despues de navegar entre pantallas 10-15 veces, la app se vuelve lenta y eventualmente crashea. DevTools Memory muestra memoria creciente sin limites.

### Problema

```dart
class ChatScreen extends StatefulWidget {
  final String roomId;

  const ChatScreen({super.key, required this.roomId});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<Message> _messages = [];
  final TextEditingController _controller = TextEditingController();

  @override
  void initState() {
    super.initState();
    // LEAK: StreamSubscription nunca se cancela
    Supabase.instance.client
        .from('messages')
        .eq('room_id', widget.roomId)
        .stream(primaryKey: ['id'])
        .order('created_at')
        .listen((messages) {
          setState(() {
            _messages.clear();
            _messages.addAll(
              messages.map((m) => Message.fromJson(m)),
            );
          });
        });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chat')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                return MessageBubble(message: _messages[index]);
              },
            ),
          ),
          _buildInput(),
        ],
      ),
    );
  }

  Widget _buildInput() {
    return Padding(
      padding: const EdgeInsets.all(8),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                hintText: 'Escribe un mensaje...',
                border: OutlineInputBorder(),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.send),
            onPressed: () {
              _sendMessage(_controller.text);
              _controller.clear();
            },
          ),
        ],
      ),
    );
  }

  void _sendMessage(String text) {
    Supabase.instance.client.from('messages').insert({
      'room_id': widget.roomId,
      'content': text,
    });
  }

  // LEAK: No hay dispose(), controllers no se cierran
}

class Message {
  final String id;
  final String content;
  final DateTime createdAt;

  Message({required this.id, required this.content, required this.createdAt});

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      content: json['content'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

class MessageBubble extends StatelessWidget {
  final Message message;
  const MessageBubble({super.key, required this.message});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: Align(
        alignment: Alignment.centerLeft,
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: Colors.blue[100],
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(message.content),
        ),
      ),
    );
  }
}
```

### Pasos de diagnostico

1. Ejecutar `flutter run --profile`
2. DevTools > Memory > Tomar snapshot base
3. Navegar al chat y de vuelta 10 veces
4. Tomar diff snapshot
5. Buscar `ChatScreen` o `Message` en las clases con crecimiento
6. Cada navegacion crea una nueva instancia de `ChatScreen` con stream abierto

### Solucion

```dart
class ChatScreen extends StatefulWidget {
  final String roomId;

  const ChatScreen({super.key, required this.roomId});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<Message> _messages = [];
  final TextEditingController _controller = TextEditingController();
  StreamSubscription<List<Map<String, dynamic>>>? _messagesSubscription;

  @override
  void initState() {
    super.initState();
    _messagesSubscription = Supabase.instance.client
        .from('messages')
        .eq('room_id', widget.roomId)
        .stream(primaryKey: ['id'])
        .order('created_at')
        .listen((messages) {
          if (mounted) {  // <-- Verificar que el widget sigue vivo
            setState(() {
              _messages.clear();
              _messages.addAll(
                messages.map((m) => Message.fromJson(m)),
              );
            });
          }
        });
  }

  @override
  void dispose() {
    _messagesSubscription?.cancel();  // <-- Cancelar stream
    _controller.dispose();            // <-- Cerrar controller
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chat')),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                return MessageBubble(message: _messages[index]);
              },
            ),
          ),
          _buildInput(),
        ],
      ),
    );
  }

  Widget _buildInput() {
    return Padding(
      padding: const EdgeInsets.all(8),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: const InputDecoration(
                hintText: 'Escribe un mensaje...',
                border: OutlineInputBorder(),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.send),
            onPressed: () {
              _sendMessage(_controller.text);
              _controller.clear();
            },
          ),
        ],
      ),
    );
  }

  void _sendMessage(String text) {
    Supabase.instance.client.from('messages').insert({
      'room_id': widget.roomId,
      'content': text,
    });
  }
}
```

### Resultado esperado

| Metrica | Antes | Despues |
|---|---|---|
| Memory despues de 15 nav | Creciente sin limite | Estable |
| StreamSubscription activas | Multiples (leak) | 1 por pantalla |
| Crash despues de uso prolongado | Si | No |
| Memoria al salir de pantalla | No se libera | Se libera |

---

## Escenario 4: "Dashboard con widgets pesados"

### Contexto

Un dashboard con multiples secciones: graficos, tablas, metricas en tiempo real. Cada actualizacion de datos reconstruye toda la pantalla. El Performance Overlay muestra jank constante.

### Problema

```dart
class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: BlocBuilder<DashboardBloc, DashboardState>(
          builder: (context, state) {
            return Column(
              children: [
                _buildMetricsRow(state),     // Widget pesado
                _buildSalesChart(state),     // Widget muy pesado
                _buildRecentOrders(state),   // Widget pesado
                _buildInventoryTable(state), // Widget muy pesado
                _buildActivityFeed(state),   // Widget mediano
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildMetricsRow(DashboardState state) {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          MetricCard(title: 'Ventas', value: state.totalSales),
          MetricCard(title: 'Usuarios', value: state.totalUsers),
          MetricCard(title: 'Pedidos', value: state.totalOrders),
        ],
      ),
    );
  }

  Widget _buildSalesChart(DashboardState state) {
    return Container(
      height: 300,
      padding: const EdgeInsets.all(16),
      child: CustomPaint(
        painter: SalesChartPainter(state.salesData),
        size: Size.infinite,
      ),
    );
  }

  Widget _buildRecentOrders(DashboardState state) {
    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: state.recentOrders.length,
      itemBuilder: (context, index) {
        return OrderTile(order: state.recentOrders[index]);
      },
    );
  }

  Widget _buildInventoryTable(DashboardState state) {
    return DataTable(
      columns: const [
        DataColumn(label: Text('Producto')),
        DataColumn(label: Text('Stock')),
        DataColumn(label: Text('Precio')),
      ],
      rows: state.inventory.map((item) {
        return DataRow(cells: [
          DataCell(Text(item.name)),
          DataCell(Text('${item.stock}')),
          DataCell(Text('\$${item.price}')),
        ]);
      }).toList(),
    );
  }

  Widget _buildActivityFeed(DashboardState state) {
    return ListView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: state.activities.length,
      itemBuilder: (context, index) {
        return ActivityTile(activity: state.activities[index]);
      },
    );
  }
}
```

### Pasos de diagnostico

1. Ejecutar `flutter run --profile`
2. DevTools > Performance > Grabar actualizaciones del dashboard
3. Enhance Tracing > Ver que `DashboardScreen.build()` se ejecuta completo
4. Flame chart: `SalesChartPainter.paint()` domina el tiempo

### Solucion

```dart
class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: const [
            _MetricsSection(),
            _ChartSection(),
            _OrdersSection(),
            _InventorySection(),
            _ActivitySection(),
          ],
        ),
      ),
    );
  }
}

class _MetricsSection extends StatelessWidget {
  const _MetricsSection();

  @override
  Widget build(BuildContext context) {
    return BlocSelector<DashboardBloc, DashboardState, DashboardMetrics>(
      selector: (state) => DashboardMetrics(
        sales: state.totalSales,
        users: state.totalUsers,
        orders: state.totalOrders,
      ),
      builder: (context, metrics) {
        return Padding(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              MetricCard(title: 'Ventas', value: metrics.sales),
              MetricCard(title: 'Usuarios', value: metrics.users),
              MetricCard(title: 'Pedidos', value: metrics.orders),
            ],
          ),
        );
      },
    );
  }
}

class _ChartSection extends StatelessWidget {
  const _ChartSection();

  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      child: BlocSelector<DashboardBloc, DashboardState, List<SalesData>>(
        selector: (state) => state.salesData,
        builder: (context, salesData) {
          return Container(
            height: 300,
            padding: const EdgeInsets.all(16),
            child: CustomPaint(
              painter: SalesChartPainter(salesData),
              size: Size.infinite,
            ),
          );
        },
      ),
    );
  }
}

class _OrdersSection extends StatelessWidget {
  const _OrdersSection();

  @override
  Widget build(BuildContext context) {
    return BlocSelector<DashboardBloc, DashboardState, List<Order>>(
      selector: (state) => state.recentOrders,
      builder: (context, orders) {
        return ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: orders.length,
          itemBuilder: (context, index) {
            return OrderTile(order: orders[index]);
          },
        );
      },
    );
  }
}

class _InventorySection extends StatelessWidget {
  const _InventorySection();

  @override
  Widget build(BuildContext context) {
    return BlocSelector<DashboardBloc, DashboardState, List<InventoryItem>>(
      selector: (state) => state.inventory,
      builder: (context, inventory) {
        return DataTable(
          columns: const [
            DataColumn(label: Text('Producto')),
            DataColumn(label: Text('Stock')),
            DataColumn(label: Text('Precio')),
          ],
          rows: inventory.map((item) {
            return DataRow(cells: [
              DataCell(Text(item.name)),
              DataCell(Text('${item.stock}')),
              DataCell(Text('\$${item.price}')),
            ]);
          }).toList(),
        );
      },
    );
  }
}

class _ActivitySection extends StatelessWidget {
  const _ActivitySection();

  @override
  Widget build(BuildContext context) {
    return BlocSelector<DashboardBloc, DashboardState, List<Activity>>(
      selector: (state) => state.activities,
      builder: (context, activities) {
        return ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: activities.length,
          itemBuilder: (context, index) {
            return ActivityTile(activity: activities[index]);
          },
        );
      },
    );
  }
}
```

### Resultado esperado

| Metrica | Antes | Despues |
|---|---|---|
| Widgets rebuild por update | Todo el arbol | Solo la seccion que cambio |
| Build time promedio | 35ms | 6ms |
| Chart repaint | Completo | Solo chart (RepaintBoundary) |
| UI response time | 50ms | 10ms |

---

## Escenario 5: "Imagen que congela al cargar"

### Contexto

Una pantalla de perfil con 20 fotos de usuario que se cargan de Supabase Storage. Al hacer scroll, la app se congela. Las imagenes tardan mucho en aparecer.

### Problema

```dart
class GalleryScreen extends StatelessWidget {
  final List<String> imageUrls;

  const GalleryScreen({super.key, required this.imageUrls});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Galeria')),
      body: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          crossAxisSpacing: 4,
          mainAxisSpacing: 4,
        ),
        itemCount: imageUrls.length,
        itemBuilder: (context, index) {
          return Image.network(
            imageUrls[index],
            fit: BoxFit.cover,
            // Sin cacheWidth/cacheHeight: decodifica imagen completa
          );
        },
      ),
    );
  }
}
```

### Pasos de diagnostico

1. Ejecutar `flutter run --profile`
2. DevTools > Memory > Ver picos de memoria al hacer scroll
3. Performance > Raster time elevado cuando cargan imagenes
4. Flame chart: `decodeImageFromList` domina el tiempo

### Solucion

```dart
class GalleryScreen extends StatelessWidget {
  final List<String> imageUrls;

  const GalleryScreen({super.key, required this.imageUrls});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Galeria')),
      body: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          crossAxisSpacing: 4,
          mainAxisSpacing: 4,
        ),
        itemCount: imageUrls.length,
        itemBuilder: (context, index) {
          return _GalleryImage(url: imageUrls[index]);
        },
      ),
    );
  }
}

class _GalleryImage extends StatelessWidget {
  final String url;

  const _GalleryImage({required this.url});

  @override
  Widget build(BuildContext context) {
    // Calcular tamano real en pixels basado en el devicePixelRatio
    final pixelRatio = MediaQuery.of(context).devicePixelRatio;
    final displaySize = 120.0; // Tamano en layout points

    return Image.network(
      url,
      fit: BoxFit.cover,
      width: displaySize,
      height: displaySize,
      cacheWidth: (displaySize * pixelRatio).toInt(),
      cacheHeight: (displaySize * pixelRatio).toInt(),
      errorBuilder: (context, error, stackTrace) {
        return Container(
          color: Colors.grey[300],
          child: const Icon(Icons.broken_image),
        );
      },
      loadingBuilder: (context, child, loadingProgress) {
        if (loadingProgress == null) return child;
        return const Center(child: CircularProgressIndicator());
      },
    );
  }
}
```

### Resultado esperado

| Metrica | Antes | Despues |
|---|---|---|
| Memoria por imagen | ~12MB | ~120KB |
| Raster time por imagen | 25ms | 2ms |
| Total memoria galeria | ~240MB | ~2.4MB |
| Scroll fluidez | Congelada | Suave |

---

## Escenario 6: "App que crece en memoria"

### Contexto

Una app con multiples pantallas que usan formularios. Despues de 20 minutos de uso, la app se vuelve lenta y consume mucha RAM. El usuario reporta que "la app se pone lenta con el tiempo".

### Problema

```dart
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _bioController = TextEditingController();
  final _phoneController = TextEditingController();
  final _addressController = TextEditingController();
  final _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _loadProfile();
    _scrollController.addListener(_onScroll);
  }

  void _loadProfile() {
    // Cargar datos del perfil
    _nameController.text = 'Juan';
    _emailController.text = 'juan@email.com';
  }

  void _onScroll() {
    // Logica de scroll
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Perfil')),
      body: SingleChildScrollView(
        controller: _scrollController,
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: 'Nombre'),
            ),
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email'),
            ),
            TextField(
              controller: _bioController,
              decoration: const InputDecoration(labelText: 'Bio'),
            ),
            TextField(
              controller: _phoneController,
              decoration: const InputDecoration(labelText: 'Telefono'),
            ),
            TextField(
              controller: _addressController,
              decoration: const InputDecoration(labelText: 'Direccion'),
            ),
          ],
        ),
      ),
    );
  }

  // No hay dispose() - TODOS los controllers se leakan
}

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late Timer _refreshTimer;

  @override
  void initState() {
    super.initState();
    // Timer que nunca se cancela
    _refreshTimer = Timer.periodic(
      const Duration(seconds: 30),
      (_) => _refreshSettings(),
    );
  }

  void _refreshSettings() {
    // Refrescar configuracion
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Configuracion')),
      body: const Center(child: Text('Settings')),
    );
  }

  // No hay dispose() - Timer leak + listener leak
}
```

### Pasos de diagnostico

1. Ejecutar `flutter run --profile`
2. DevTools > Memory > Tomar snapshot base
3. Navegar entre ProfileScreen y SettingsScreen 15 veces
4. Tomar diff snapshot
5. Clases con crecimiento: `TextEditingController`, `Timer`, `ScrollController`
6. Verificar: `ProfileScreen` y `SettingsScreen` no tienen `dispose()`

### Solucion

```dart
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _bioController = TextEditingController();
  final _phoneController = TextEditingController();
  final _addressController = TextEditingController();
  final _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _loadProfile();
    _scrollController.addListener(_onScroll);
  }

  void _loadProfile() {
    _nameController.text = 'Juan';
    _emailController.text = 'juan@email.com';
  }

  void _onScroll() {
    // Logica de scroll
  }

  @override
  void dispose() {
    // Remover listener antes de dispose
    _scrollController.removeListener(_onScroll);

    // Cerrar todos los controllers
    _scrollController.dispose();
    _nameController.dispose();
    _emailController.dispose();
    _bioController.dispose();
    _phoneController.dispose();
    _addressController.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Perfil')),
      body: SingleChildScrollView(
        controller: _scrollController,
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(labelText: 'Nombre'),
            ),
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email'),
            ),
            TextField(
              controller: _bioController,
              decoration: const InputDecoration(labelText: 'Bio'),
            ),
            TextField(
              controller: _phoneController,
              decoration: const InputDecoration(labelText: 'Telefono'),
            ),
            TextField(
              controller: _addressController,
              decoration: const InputDecoration(labelText: 'Direccion'),
            ),
          ],
        ),
      ),
    );
  }
}

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late Timer _refreshTimer;

  @override
  void initState() {
    super.initState();
    _refreshTimer = Timer.periodic(
      const Duration(seconds: 30),
      (_) => _refreshSettings(),
    );
  }

  void _refreshSettings() {
    // Refrescar configuracion
  }

  @override
  void dispose() {
    _refreshTimer.cancel();  // <-- Cancelar timer
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Configuracion')),
      body: const Center(child: Text('Settings')),
    );
  }
}
```

### Resultado esperado

| Metrica | Antes | Despues |
|---|---|---|
| Memory despues de 20 min | Creciente continuamente | Estable |
| Controllers activos (leak) | Multiples por pantalla | 0 despues de dispose |
| Timers activos (leak) | Multiples | 0 despues de dispose |
| GC frequency | > 5/min | < 1/min |

---

## Ejercicio integrador: Diagnosticar una app "enferma"

### Contexto

Recibes una app Flutter de un proyecto existente. El equipo reporta multiples problemas:
1. El feed principal se congela al hacer scroll
2. La pantalla de login parpadea cuando escribes
3. La memoria crece continuamente durante el uso
4. Las imagenes del perfil tardan mucho en cargar

Tu tarea es **diagnosticar y corregir cada problema**.

### Archivos del proyecto

```dart
// === lib/models/post.dart ===
class Post {
  final String id;
  final String title;
  final String content;
  final String authorId;
  final DateTime createdAt;

  Post({
    required this.id,
    required this.title,
    required this.content,
    required this.authorId,
    required this.createdAt,
  });

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'],
      title: json['title'],
      content: json['content'],
      authorId: json['author_id'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

// === lib/blocs/feed/feed_state.dart ===
class FeedState {
  final List<Post> posts;
  final bool isLoading;
  final String? error;

  FeedState({
    this.posts = const [],
    this.isLoading = false,
    this.error,
  });
}

// === lib/screens/feed_screen.dart ===
class FeedScreen extends StatefulWidget {
  const FeedScreen({super.key});

  @override
  State<FeedScreen> createState() => _FeedScreenState();
}

class _FeedScreenState extends State<FeedScreen> {
  StreamSubscription? _postsSubscription;
  final List<Post> _posts = [];

  @override
  void initState() {
    super.initState();
    _postsSubscription = Supabase.instance.client
        .from('posts')
        .stream(primaryKey: ['id'])
        .order('created_at', ascending: false)
        .listen((data) {
          setState(() {
            _posts.clear();
            _posts.addAll(data.map((p) => Post.fromJson(p)));
          });
        });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Feed')),
      body: ListView(
        children: _posts.map((post) => PostCard(post: post)).toList(),
      ),
    );
  }
}

class PostCard extends StatelessWidget {
  final Post post;
  const PostCard({super.key, required this.post});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  child: Image.network(
                    'https://api.dicebear.com/7.x/avataaars/svg?seed=${post.authorId}',
                  ),
                ),
                const SizedBox(width: 12),
                Text(post.title, style: const TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
            const SizedBox(height: 8),
            Text(post.content),
            const SizedBox(height: 8),
            Text('${post.createdAt}', style: TextStyle(color: Colors.grey[600])),
          ],
        ),
      ),
    );
  }
}

// === lib/screens/login_screen.dart ===
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: BlocBuilder<AuthBloc, AuthState>(
        builder: (context, state) {
          return Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text('Login', style: TextStyle(fontSize: 32)),
                const SizedBox(height: 32),
                TextField(
                  onChanged: (v) => context.read<AuthBloc>().add(EmailChanged(v)),
                ),
                const SizedBox(height: 16),
                TextField(
                  obscureText: true,
                  onChanged: (v) => context.read<AuthBloc>().add(PasswordChanged(v)),
                ),
                const SizedBox(height: 24),
                if (state.isLoading) const CircularProgressIndicator(),
                ElevatedButton(
                  onPressed: state.isValid ? () => context.read<AuthBloc>().add(LoginSubmitted()) : null,
                  child: const Text('Entrar'),
                ),
                Text(state.error ?? '', style: const TextStyle(color: Colors.red)),
              ],
            ),
          );
        },
      ),
    );
  }
}

// === lib/screens/profile_screen.dart ===
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _nameController = TextEditingController();
  final _bioController = TextEditingController();
  final _urlController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  void _loadProfile() {
    _nameController.text = 'Usuario';
    _bioController.text = 'Bio del usuario';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Perfil')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Image.network('https://api.dicebear.com/7.x/avataaars/svg?seed=user'),
            const SizedBox(height: 16),
            TextField(controller: _nameController, decoration: const InputDecoration(labelText: 'Nombre')),
            TextField(controller: _bioController, decoration: const InputDecoration(labelText: 'Bio')),
            TextField(controller: _urlController, decoration: const InputDecoration(labelText: 'URL foto')),
          ],
        ),
      ),
    );
  }
}
```

### Guia de diagnostico

Sigue estos pasos para encontrar y corregir cada problema:

```
PROBLEMA 1: Feed se congela al hacer scroll
├── Diagnostico: ListView() construye TODOS los posts
├── Solucion: Cambiar a ListView.builder
├── Bonus: Agregar const a PostCard si es posible
└── Verificar: Performance > build time < 8ms

PROBLEMA 2: Login parpadea al escribir
├── Diagnostico: BlocBuilder reconstruye todo el form
├── Solucion: BlocSelector para boton + indicador
├── Verificar: Enhance Tracing > menos rebuilds
└── Resultado: Build time < 2ms por tecla

PROBLEMA 3: Memoria crece continuamente
├── Diagnostico: FeedScreen no tiene dispose()
├── Solucion: Agregar dispose() con cancel de subscription
├── Bonus: ProfileScreen no tiene dispose() de controllers
├── Verificar: Memory > diff snapshot sin crecimiento
└── Resultado: Memoria estable despues de 15 nav

PROBLEMA 4: Imagenes del perfil tardan
├── Diagnostico: Image.network sin cacheWidth/cacheHeight
├── Solucion: Agregar cacheWidth/cacheHeight
├── Bonus: precacheImage en initState
├── Verificar: Memory > menos uso por imagen
└── Resultado: Imagenes cargan instantaneamente
```

### Solucion completa

```dart
// === lib/screens/feed_screen.dart (CORREGIDO) ===
class FeedScreen extends StatefulWidget {
  const FeedScreen({super.key});

  @override
  State<FeedScreen> createState() => _FeedScreenState();
}

class _FeedScreenState extends State<FeedScreen> {
  StreamSubscription? _postsSubscription;
  final List<Post> _posts = [];

  @override
  void initState() {
    super.initState();
    _postsSubscription = Supabase.instance.client
        .from('posts')
        .stream(primaryKey: ['id'])
        .order('created_at', ascending: false)
        .listen((data) {
          if (mounted) {
            setState(() {
              _posts.clear();
              _posts.addAll(data.map((p) => Post.fromJson(p)));
            });
          }
        });
  }

  @override
  void dispose() {
    _postsSubscription?.cancel();  // CORRECCION #1: cancelar subscription
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Feed')),
      body: ListView.builder(  // CORRECCION #2: ListView.builder
        itemCount: _posts.length,
        itemBuilder: (context, index) {
          return PostCard(post: _posts[index]);
        },
      ),
    );
  }
}

// === lib/screens/login_screen.dart (CORREGIDO) ===
class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('Login', style: TextStyle(fontSize: 32)),
            const SizedBox(height: 32),
            TextField(
              onChanged: (v) => context.read<AuthBloc>().add(EmailChanged(v)),
            ),
            const SizedBox(height: 16),
            TextField(
              obscureText: true,
              onChanged: (v) => context.read<AuthBloc>().add(PasswordChanged(v)),
            ),
            const SizedBox(height: 24),
            // CORRECCION #3: BlocSelector para indicador
            BlocSelector<AuthBloc, AuthState, bool>(
              selector: (state) => state.isLoading,
              builder: (context, isLoading) {
                return isLoading
                    ? const CircularProgressIndicator()
                    : const SizedBox.shrink();
              },
            ),
            const SizedBox(height: 16),
            // CORRECCION #4: BlocSelector para boton
            BlocSelector<AuthBloc, AuthState, bool>(
              selector: (state) => state.isValid,
              builder: (context, isValid) {
                return ElevatedButton(
                  onPressed: isValid
                      ? () => context.read<AuthBloc>().add(LoginSubmitted())
                      : null,
                  child: const Text('Entrar'),
                );
              },
            ),
            // CORRECCION #5: BlocSelector para error
            BlocSelector<AuthBloc, AuthState, String?>(
              selector: (state) => state.error,
              builder: (context, error) {
                return Text(
                  error ?? '',
                  style: const TextStyle(color: Colors.red),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}

// === lib/screens/profile_screen.dart (CORREGIDO) ===
class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _nameController = TextEditingController();
  final _bioController = TextEditingController();
  final _urlController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  void _loadProfile() {
    _nameController.text = 'Usuario';
    _bioController.text = 'Bio del usuario';
  }

  @override
  void dispose() {
    // CORRECCION #6: dispose de todos los controllers
    _nameController.dispose();
    _bioController.dispose();
    _urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Perfil')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // CORRECCION #7: cacheWidth/cacheHeight en imagenes
            Image.network(
              'https://api.dicebear.com/7.x/avataaars/svg?seed=user',
              width: 120,
              height: 120,
              cacheWidth: 240,  // 120 * 2.0 devicePixelRatio
              cacheHeight: 240,
            ),
            const SizedBox(height: 16),
            TextField(controller: _nameController, decoration: const InputDecoration(labelText: 'Nombre')),
            TextField(controller: _bioController, decoration: const InputDecoration(labelText: 'Bio')),
            TextField(controller: _urlController, decoration: const InputDecoration(labelText: 'URL foto')),
          ],
        ),
      ),
    );
  }
}
```

### Resumen de correcciones

| # | Archivo | Problema | Correccion |
|---|---|---|---|
| 1 | `feed_screen.dart` | StreamSubscription sin cancelar | Agregar `dispose()` con `cancel()` |
| 2 | `feed_screen.dart` | `ListView` construye todos los items | Cambiar a `ListView.builder` |
| 3 | `login_screen.dart` | `BlocBuilder` reconstruye todo | `BlocSelector` para isLoading |
| 4 | `login_screen.dart` | Boton se reconstruye innecesariamente | `BlocSelector` para isValid |
| 5 | `login_screen.dart` | Texto de error se reconstruye | `BlocSelector` para error |
| 6 | `profile_screen.dart` | Controllers sin dispose | Agregar `dispose()` completo |
| 7 | `profile_screen.dart` | Imagen sin cacheWidth/cacheHeight | Agregar dimensiones en cache |
