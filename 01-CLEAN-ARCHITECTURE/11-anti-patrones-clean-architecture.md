# 11: Anti-patrones en Clean Architecture

> Errores comunes que convierten Clean Architecture en "Messy Architecture". Conócelos para detectarlos a tiempo.

---

## Anti-patrón 1: La God Class

**Síntoma:** Una clase que hace absolutamente todo.

```dart
// ❌ GOD CLASS
class AppManager {
  final SupabaseClient _supabase;
  
  // Autenticación
  Future<User> signIn(String email, String pass) async { /* ... */ }
  Future<void> signOut() async { /* ... */ }
  
  // Posts
  Future<List<Post>> getPosts() async { /* ... */ }
  Future<void> createPost(Post post) async { /* ... */ }
  
  // Notificaciones
  Future<void> sendNotification(String userId) async { /* ... */ }
  
  // Utilidades
  String formatDate(DateTime date) => /* ... */;
  bool isValidEmail(String email) => /* ... */;
}
```

**Solución:** Separar por responsabilidad → UseCases, Services, Utils.

---

## Anti-patrón 2: La Dependencia Invertida (en mal sentido)

**Síntoma:** Domain depende de Data o Presentation.

```
❌ Domain importa de Data
❌ Presentation importa de Data directamente
❌ UseCase importa de SupabaseClient
```

**Regla de oro:** Las flechas de dependencia SOLO apuntan hacia adentro (hacia Domain).

```
Presentation → Domain ← Data
                 ↑
          (Domain no depende de nadie)
```

---

## Anti-patrón 3: El Repository de Papel

**Síntoma:** Repository interface no tiene sentido, solo pasa datos sin lógica.

```dart
// ❌ REPOSITORY INÚTIL
abstract class UserRepository {
  Future<User> getUser(String id);
}

class UserRepositoryImpl implements UserRepository {
  final SupabaseClient _supabase;
  
  @override
  Future<User> getUser(String id) async {
    // Solo passthrough, cero lógica
    final data = await _supabase.from('users').select().eq('id', id).single();
    return User.fromJson(data);
  }
}
```

**Cuándo está bien:** Si la lógica es solo mapeo de datos, está OK.
**Cuándo es problema:** Si NO hay lógica de negocio en UseCases → el UseCase también es inútil.

---

## Anti-patrón 4: El Estado Monolítico

**Síntoma:** Un solo State para toda la pantalla.

```dart
// ❌ STATE GIGANTE
class HomeState {
  final List<Post> posts;
  final List<Comment> comments;
  final User? currentUser;
  final bool isLoadingPosts;
  final bool isLoadingComments;
  final String? errorPosts;
  final String? errorComments;
  final int selectedTab;
  final ScrollController scrollController;
  // ... 20 campos más
}
```

**Solución:** Separar por dominio o usar múltiples BLoCs/Cubits.

```dart
// ✅ STATES SEPARADOS
class PostsState { /* solo posts */ }
class CommentsState { /* solo comments */ }
class AuthState { /* solo auth */ }
```

---

## Anti-patrón 5: El Usecase Castrado

**Síntoma:** UseCase que solo hace una llamada sin lógica.

```dart
// ❌ USECASE INÚTIL
class GetUserUseCase {
  final UserRepository _repo;
  GetUserUseCase(this._repo);
  
  Future<User> call(String id) async => _repo.getUser(id);
}
```

**Solución:** Si el UseCase no tiene lógica, únelo al Repository o agrega lógica.

```dart
// ✅ USECASE CON LÓGICA
class GetUserUseCase {
  final UserRepository _repo;
  final CacheService _cache;
  
  GetUserUseCase(this._repo, this._cache);
  
  Future<User> call(String id) async {
    // 1. Check cache
    final cached = await _cache.get<User>('user_$id');
    if (cached != null) return cached;
    
    // 2. Fetch from repo
    final user = await _repo.getUser(id);
    
    // 3. Cache for next time
    await _cache.set('user_$id', user);
    
    return user;
  }
}
```

---

## Anti-patrón 6: El Map hell

**Síntoma:** `Map<String, dynamic>` por todos lados.

```dart
// ❌ MAPS POR TODOS LADOS
class UserRepository {
  Future<Map<String, dynamic>> getUser(String id) async {
    return await _supabase.from('users').select().eq('id', id).single();
  }
}

// En el UI:
final name = user['name'] as String;  // Crash si falta
final email = user['email'] as String; // No hay compile-time safety
```

**Solución:** Modelos tipados siempre.

```dart
// ✅ MODELOS TIPADOS
class User {
  final String id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});

  factory User.fromJson(Map<String, dynamic> json) => User(
    id: json['id'] as String,
    name: json['name'] as String,
    email: json['email'] as String,
  );

  Map<String, dynamic> toJson() => {'id': id, 'name': name, 'email': email};
}
```

---

## Anti-patrón 7: La Herencia Infinita

**Síntoma:** 5 niveles de herencia donde 3 son abstractos innecesarios.

```
AbstractBaseRepository
  └── AbstractRepositoryMixin
        └── BaseRepositoryImpl
              └── UserRepositoryImpl
                    └── SupabaseUserRepositoryImpl
```

**Solución:** Composición sobre herencia. Un nivel de abstracción basta.

```dart
// ✅ COMPOSICIÓN
class UserRepository {
  final SupabaseDataSource _dataSource;
  final CacheService _cache;
  
  UserRepository(this._dataSource, this._cache);
  // Usa sus dependencias, no hereda de nada
}
```

---

## Anti-patrón 8: El Callback Hell

**Síntoma:** Anidamiento de callbacks que hace el código ilegible.

```dart
// ❌ CALLBACK HELL
_fetchUser((user) {
  _fetchPosts(user.id, (posts) {
    _fetchComments(posts[0].id, (comments) {
      setState(() { /* ... */ });
    });
  });
});
```

**Solución:** async/await + manejo de errores.

```dart
// ✅ ASYNC/AWAIT
Future<void> loadData() async {
  try {
    final user = await _fetchUser();
    final posts = await _fetchPosts(user.id);
    final comments = await _fetchComments(posts[0].id);
    emit state;
  } catch (e) {
    emit error;
  }
}
```

---

## Checklist Anti-patrones

```
□ ¿Algún archivo tiene >300 líneas? (God Class)
□ ¿Domain importa de Data? (Dependencia invertida)
□ ¿Algún UseCase solo hace passthrough? (Usecase castrado)
□ ¿Un solo State maneja 10+ campos? (Estado monolítico)
□ ¿Map<String, dynamic> circula por la app? (Map hell)
□ ¿Más de 3 niveles de herencia? (Herencia infinita)
□ ¿Más de 3 niveles de callbacks? (Callback hell)
```

---

**Siguiente:** [12-cuando-no-usar-clean-architecture.md](./12-cuando-no-usar-clean-architecture.md)
