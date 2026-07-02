# 06 - Integración con Flutter

> Aprende a configurar y usar Supabase en tu aplicación Flutter. Desde la instalación hasta las mejores prácticas de implementación.

---

## 🎯 Objetivos de este archivo

- Instalar y configurar supabase_flutter
- Inicializar el cliente de Supabase
- Implementar autenticación
- Realizar operaciones CRUD con la base de datos
- Manejar estado y errores correctamente

---

## 1. Instalación de dependencias

### Dependencias requeridas

```yaml
# pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Supabase
  supabase_flutter: ^2.5.0
  
  # Opcionales (recomendados para Clean Architecture)
  flutter_bloc: ^9.1.0
  equatable: ^2.0.5
  fpdart: ^1.2.0
  go_router: ^12.1.3
  get_it: ^7.6.4
```

### Instalar

```bash
flutter pub get
```

---

## 2. Inicialización de Supabase

### Método 1: Variables de entorno (recomendado)

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Supabase.initialize(
    url: const String.fromEnvironment('SUPABASE_URL'),
    anonKey: const String.fromEnvironment('SUPABASE_ANON_KEY'),
    debug: true, // Solo en desarrollo
  );
  
  runApp(const MyApp());
}
```

### Método 2: flutter_dotenv

```yaml
# pubspec.yaml
dependencies:
  flutter_dotenv: ^5.1.0
```

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Cargar variables desde .env
  await dotenv.load(fileName: '.env');
  
  await Supabase.initialize(
    url: dotenv.env['SUPABASE_URL']!,
    anonKey: dotenv.env['SUPABASE_ANON_KEY']!,
  );
  
  runApp(const MyApp());
}
```

### Método 3: Build args (para CI/CD)

```bash
# En terminal o CI/CD
flutter build apk --release \
  --dart-define=SUPABASE_URL=https://tu-proyecto.supabase.co \
  --dart-define=SUPABASE_ANON_KEY=tu-anon-key
```

---

## 3. Cliente de Supabase

### Obtener instancia

```dart
// En cualquier parte de la app
final supabase = Supabase.instance.client;

// Verificar conexión
final url = supabase.supabaseUrl;
final anonKey = supabase.supabaseAnonKey;
```

---

## 4. Autenticación

### Inicialización básica

```dart
// lib/core/auth/supabase_auth.dart
import 'package:supabase_flutter/supabase_flutter.dart';

class SupabaseAuth {
  final SupabaseClient _client;
  
  SupabaseAuth(this._client);
  
  // Obtener usuario actual
  User? get currentUser => _client.auth.currentUser;
  
  // Verificar si está autenticado
  bool get isAuthenticated => currentUser != null;
  
  // Escuchar cambios de estado de autenticación
  Stream<User?> get onAuthStateChange => _client.auth.onAuthStateChange.map(
    (event) => event.session?.user,
  );
  
  // Iniciar sesión con email y contraseña
  Future<AuthResponse> signInWithEmail(String email, String password) {
    return _client.auth.signInWithPassword(
      email: email,
      password: password,
    );
  }
  
  // Registrarse con email y contraseña
  Future<AuthResponse> signUp(String email, String password) {
    return _client.auth.signUp(
      email: email,
      password: password,
    );
  }
  
  // Cerrar sesión
  Future<void> signOut() {
    return _client.auth.signOut();
  }
  
  // Enviar email de recuperación de contraseña
  Future<void> resetPassword(String email) {
    return _client.auth.resetPasswordForEmail(email);
  }
  
  // Iniciar sesión con OAuth (Google, GitHub, etc.)
  Future<AuthResponse> signInWithOAuth(Provider provider) {
    return _client.auth.signInWithOAuth(
      provider: provider,
      redirectTo: 'miapp://login-callback',
    );
  }
}
```

### Autenticación con Bloc (recomendado)

```dart
// lib/features/auth/presentation/cubit/auth_cubit.dart
import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

part 'auth_state.dart';

class AuthCubit extends Cubit<AuthState> {
  final SupabaseClient _supabase;
  
  AuthCubit(this._supabase) : super(AuthInitial()) {
    _init();
  }
  
  void _init() {
    // Verificar si ya hay una sesión
    final user = _supabase.auth.currentUser;
    if (user != null) {
      emit(AuthAuthenticated(user));
    } else {
      emit(AuthUnauthenticated());
    }
    
    // Escuchar cambios de autenticación
    _supabase.auth.onAuthStateChange.listen((event) {
      if (event.session?.user != null) {
        emit(AuthAuthenticated(event.session!.user!));
      } else {
        emit(AuthUnauthenticated());
      }
    });
  }
  
  Future<void> signIn(String email, String password) async {
    emit(AuthLoading());
    try {
      final response = await _supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );
      if (response.user != null) {
        emit(AuthAuthenticated(response.user!));
      } else {
        emit(const AuthError('Credenciales inválidas'));
      }
    } catch (e) {
      emit(AuthError(e.toString()));
    }
  }
  
  Future<void> signUp(String email, String password) async {
    emit(AuthLoading());
    try {
      final response = await _supabase.auth.signUp(
        email: email,
        password: password,
      );
      if (response.user != null) {
        emit(AuthAuthenticated(response.user!));
      } else {
        emit(const AuthError('Error al crear cuenta'));
      }
    } catch (e) {
      emit(AuthError(e.toString()));
    }
  }
  
  Future<void> signOut() async {
    emit(AuthLoading());
    await _supabase.auth.signOut();
    emit(AuthUnauthenticated());
  }
}
```

```dart
// lib/features/auth/presentation/cubit/auth_state.dart
part of 'auth_cubit.dart';

abstract class AuthState extends Equatable {
  const AuthState();
  
  @override
  List<Object?> get props => [];
}

class AuthInitial extends AuthState {}
class AuthLoading extends AuthState {}
class AuthAuthenticated extends AuthState {
  final User user;
  const AuthAuthenticated(this.user);
  
  @override
  List<Object?> get props => [user];
}
class AuthUnauthenticated extends AuthState {}
class AuthError extends AuthState {
  final String message;
  const AuthError(this.message);
  
  @override
  List<Object?> get props => [message];
}
```

---

## 5. Operaciones de Base de Datos

### Conceptos clave

| Concepto | Descripción |
|----------|-------------|
| **from()** | Seleccionar tabla |
| .select() | Consulta SELECT |
| .insert() | INSERT |
| .update() | UPDATE |
| .delete() | DELETE |
| .eq() | WHERE columna = valor |
| .neq() | WHERE columna != valor |
| .in_() | WHERE columna IN lista |
| .order() | ORDER BY |
| .limit() | LIMIT |

### CREATE (Insertar)

```dart
// Insertar un registro
final response = await supabase
    .from('users')
    .insert({
      'email': 'test@example.com',
      'full_name': 'Test User',
    })
    .select();

// Insertar múltiples registros
await supabase
    .from('users')
    .insert([
      {'email': 'user1@example.com', 'full_name': 'User 1'},
      {'email': 'user2@example.com', 'full_name': 'User 2'},
    ]);
```

### READ (Consultar)

```dart
// Obtener todos los registros
final response = await supabase.from('users').select();

// Obtener con filtros
final response = await supabase
    .from('users')
    .select()
    .eq('email', 'test@example.com');

// Obtener un solo registro
final response = await supabase
    .from('users')
    .select()
    .eq('id', userId)
    .maybeSingle();

// Seleccionar columnas específicas
final response = await supabase
    .from('users')
    .select('email, full_name');

// Con paginación
final response = await supabase
    .from('users')
    .select()
    .range(0, 9); // Primeros 10

// Ordenar resultados
final response = await supabase
    .from('users')
    .select()
    .order('created_at', ascending: false);
```

### UPDATE (Actualizar)

```dart
// Actualizar un registro
await supabase
    .from('users')
    .update({'full_name': 'Nuevo Nombre'})
    .eq('id', userId);

// Actualizar múltiples registros
await supabase
    .from('users')
    .update({'is_active': false})
    .eq('role', 'inactive');
```

### DELETE (Eliminar)

```dart
// Eliminar un registro
await supabase
    .from('users')
    .delete()
    .eq('id', userId);

// Eliminar múltiples registros
await supabase
    .from('users')
    .delete()
    .eq('status', 'deleted');
```

---

## 6. Integración con Clean Architecture

### Repository Implementation

```dart
// lib/features/user/data/repositories/user_repository_impl.dart
import 'package:fpdart/fpdart.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

import '../../../../core/error/failures.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/user_repository.dart';

class UserRepositoryImpl implements UserRepository {
  final SupabaseClient _supabase;
  
  UserRepositoryImpl(this._supabase);
  
  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    try {
      final response = await _supabase
          .from('users')
          .select()
          .order('created_at', ascending: false);
      
      final users = response.map((json) => User.fromJson(json)).toList();
      return Right(users);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final response = await _supabase
          .from('users')
          .select()
          .eq('id', id)
          .maybeSingle();
      
      if (response == null) {
        return const Left(NotFoundFailure('User not found'));
      }
      
      return Right(User.fromJson(response));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, void>> createUser(User user) async {
    try {
      await _supabase.from('users').insert({
        'email': user.email,
        'full_name': user.fullName,
        'avatar_url': user.avatarUrl,
      });
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, void>> updateUser(User user) async {
    try {
      await _supabase.from('users').update({
        'full_name': user.fullName,
        'avatar_url': user.avatarUrl,
      }).eq('id', user.id);
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
  
  @override
  Future<Either<Failure, void>> deleteUser(String id) async {
    try {
      await _supabase.from('users').delete().eq('id', id);
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
```

---

## 7. Row Level Security (RLS)

### Cómo funciona

Supabase usa RLS para controlar el acceso a las tablas. Las políticas se definen en SQL:

```sql
-- Solo el propio usuario puede ver su perfil
CREATE POLICY "users_select_own" ON public.users
    FOR SELECT USING (auth.uid() = id);

-- Solo el propio usuario puede actualizar su perfil
CREATE POLICY "users_update_own" ON public.users
    FOR UPDATE USING (auth.uid() = id);
```

### Desde Flutter (sin autenticación)

```dart
// Esto fallará si no hay políticas para usuarios no autenticados
final response = await supabase.from('users').select();
```

---

## 8. Realtime (Tiempo Real)

### Suscribirse a cambios

```dart
// lib/features/chat/data/datasources/chat_realtime_datasource.dart
class ChatRealtimeDataSource {
  final SupabaseClient _supabase;
  
  ChatRealtimeDataSource(this._supabase);
  
  Stream<List<Message>> watchMessages(String chatId) {
    return _supabase
        .from('messages')
        .stream(primaryKey: ['id'])
        .eq('chat_id', chatId)
        .map((maps) => maps.map((map) => Message.fromJson(map)).toList());
  }
}
```

### Usar en Cubit

```dart
class ChatCubit extends Cubit<ChatState> {
  final ChatRealtimeDataSource _realtimeDataSource;
  
  ChatCubit(this._realtimeDataSource) : super(ChatInitial());
  
  void watchMessages(String chatId) {
    _realtimeDataSource.watchMessages(chatId).listen((messages) {
      emit(ChatLoaded(messages));
    });
  }
}
```

---

## 9. Storage

### Subir archivos

```dart
// Subir imagen
final file = File('path/to/image.jpg');
await supabase.storage
    .from('avatars')
    .upload('user-id/avatar.jpg', file);

// Con opciones
await supabase.storage
    .from('avatars')
    .upload('user-id/avatar.jpg', file, fileOptions: const FileOptions(
      cacheControl: '3600',
      upsert: false,
    ));
```

### Descargar archivos

```dart
// Obtener URL pública
final url = supabase.storage
    .from('avatars')
    .getPublicUrl('user-id/avatar.jpg');

// Descargar archivo
final data = await supabase.storage
    .from('avatars')
    .download('user-id/avatar.jpg');
```

---

## 10. Errores comunes

### "Row Level Security Error"

```dart
// Verificar que el usuario esté autenticado
final session = supabase.auth.currentSession;
if (session == null) {
  // Redirigir a login
}
```

### "Connection refused"

```bash
# Verificar que Supabase local esté corriendo
supabase status
```

### "Invalid JWT"

```dart
// El token puede haber expirado, intentar refresh
await supabase.auth.refreshSession();
```

---

## ✅ Checklist de integración con Flutter

- [ ] `supabase_flutter` añadido en pubspec.yaml
- [ ] Supabase inicializado en main.dart
- [ ] Cliente accesible desde cualquier parte de la app
- [ ] Autenticación implementada con Cubit/BLoC
- [ ] Repository implementa operaciones CRUD
- [ ] RLS configurado en la base de datos
- [ ] Variables de entorno configuradas
- [ ] Tests de integración funcionando

---

## 📚 Recursos

- [Supabase Flutter SDK](https://supabase.com/docs/reference/flutter/initializing)
- [Supabase Flutter Examples](https://github.com/supabase-community/supabase-flutter)
- [Flutter Clean Architecture con Supabase](https://example.com)

---

**Siguiente**: [07-testing-local-supabase.md](./07-testing-local-supabase.md)