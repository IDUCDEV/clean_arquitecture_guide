# 09: Ejercicio Práctico — Code Review Realista

> Revisa un código con errores y da feedback como lo harías en un equipo real.

---

## Instrucciones

1. Lee el código de abajo como si fuera un PR que te toca revisar
2. Identifica TODOS los problemas (bugs, anti-patrones, mejoras)
3. Escribe tu feedback usando el formato del [01-code-reviews-efectivos.md](./01-code-reviews-efectivos.md)
4. Compara con las soluciones al final

---

## Código a revisar

```dart
// user_service.dart
class UserService {
  final SupabaseClient client = SupabaseClient('https://xxx.supabase.co', 'key');

  Future getUser(String id) async {
    var data = await client.from('users').select().eq('id', id);
    return data;
  }

  Future updateUser(String id, String name, String email) async {
    await client.from('users').update({
      'name': name,
      'email': email,
    }).eq('id', id);
  }

  Future deleteUser(String id) async {
    await client.from('users').delete().eq('id', id);
  }

  Future getAllUsers() async {
    var data = await client.from('users').select();
    return data;
  }
}

// user_page.dart
class UserPage extends StatefulWidget {
  @override
  _UserPageState createState() => _UserPageState();
}

class _UserPageState extends State<UserPage> {
  UserService service = UserService();
  var users;
  var selectedUser;
  bool loading = true;

  @override
  void initState() {
    super.initState();
    loadUsers();
  }

  loadUsers() async {
    var data = await service.getAllUsers();
    setState(() {
      users = data;
      loading = false;
    });
  }

  deleteUser(String id) async {
    await service.deleteUser(id);
    loadUsers();
  }

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return CircularProgressIndicator();
    }
    return ListView.builder(
      itemCount: users.length,
      itemBuilder: (context, index) {
        return ListTile(
          title: Text(users[index]['name']),
          subtitle: Text(users[index]['email']),
          onTap: () {
            selectedUser = users[index];
          },
          trailing: IconButton(
            icon: Icon(Icons.delete),
            onPressed: () {
              deleteUser(users[index]['id']);
            },
          ),
        );
      },
    );
  }
}
```

---

## Tu checklist de revisión

```
□ Manejo de errores (try/catch)
□ Tipado (Future sin tipo, var en vez de tipo explícito)
□ Arquitectura (Service directamente en UI, sin Clean Architecture)
□ Inyección de dependencias (SupabaseClient hardcodeado)
□ Seguridad (API key en código fuente)
□ UX (sin confirmación antes de borrar, sin error handling en UI)
□ Performance (sin pagination, setState sin mounted check)
□ Null safety (users puede ser null)
```

---

## Soluciones

### Problema 1: API Key hardcodeada
**Severidad:** Crítico
**Ubicación:** `UserService` línea 2

```dart
// ❌ API key en código fuente
final SupabaseClient client = SupabaseClient('https://xxx.supabase.co', 'key');

// ✅ Variables de entorno
final SupabaseClient client = SupabaseClient(
  SupabaseClient.supabaseUrl,
  SupabaseClient.supabaseKey,
);
```

### Problema 2: Sin tipado en Futures
**Severidad:** Alto

```dart
// ❌ Future sin tipo
Future getUser(String id) async { ... }

// ✅ Future tipado
Future<Map<String, dynamic>> getUser(String id) async { ... }
```

### Problema 3: Sin manejo de errores
**Severidad:** Alto

```dart
// ❌ Sin try/catch
loadUsers() async {
  var data = await service.getAllUsers();
  setState(() { users = data; });
}

// ✅ Con manejo de errores
loadUsers() async {
  try {
    var data = await service.getAllUsers();
    setState(() { users = data; loading = false; });
  } catch (e) {
    setState(() { error = e.toString(); loading = false; });
  }
}
```

### Problema 4: Sin mounted check
**Severidad:** Medio

```dart
// ❌ setState sin mounted check
loadUsers() async {
  var data = await service.getAllUsers();
  setState(() { ... });
}

// ✅ Con mounted check
loadUsers() async {
  var data = await service.getAllUsers();
  if (!mounted) return;
  setState(() { ... });
}
```

### Problema 5: Borrar sin confirmación
**Severidad:** Medio

```dart
// ✅ Con confirmación
onPressed: () async {
  final confirm = await showDialog<bool>(
    context: context,
    builder: (_) => AlertDialog(
      title: Text('¿Eliminar usuario?'),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context, false), child: Text('Cancelar')),
        TextButton(onPressed: () => Navigator.pop(context, true), child: Text('Eliminar')),
      ],
    ),
  );
  if (confirm == true) deleteUser(users[index]['id']);
},
```

### Problema 6: Tipado de users
**Severidad:** Medio

```dart
// ❌ var users puede ser cualquier cosa
var users;

// ✅ Tipado explícito
List<Map<String, dynamic>> users = [];
```

---

**Volver al índice:** [README.md](./README.md)
