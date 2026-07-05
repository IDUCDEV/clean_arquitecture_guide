# 06 - Integración con Flutter

> Aprende a configurar y usar Supabase en tu aplicación Flutter. Desde la instalación hasta las mejores prácticas de implementación.

---

## 🎯 Objetivos de este archivo

- Instalar y configurar supabase_flutter
- Inicializar el cliente de Supabase
- Implementar autenticación (email, OAuth, Magic Link, MFA)
- Realizar operaciones CRUD con la base de datos
- Suscripciones Realtime (Broadcast, Presence, Postgres Changes)
- Storage (upload, download, RLS)
- Edge Functions (invocar desde Flutter)
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
  supabase_flutter: ^2.10.0
  
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

**Nota sobre API keys:** El parámetro `anonKey:` fue renombrado a `publishableKey:` en versiones recientes. Usa `publishableKey:` con el nuevo formato de keys (`sb_publishable_xxx`). Si aún usas keys legacy (`eyJ...`), ambos nombres funcionan.

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Supabase.initialize(
    url: const String.fromEnvironment('SUPABASE_URL'),
    publishableKey: const String.fromEnvironment('SUPABASE_PUBLISHABLE_KEY'),
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
    publishableKey: dotenv.env['SUPABASE_PUBLISHABLE_KEY']!,
  );
  
  runApp(const MyApp());
}
```

### Método 3: Build args (para CI/CD)

```bash
# En terminal o CI/CD
flutter build apk --release \
  --dart-define=SUPABASE_URL=https://tu-proyecto.supabase.co \
  --dart-define=SUPABASE_PUBLISHABLE_KEY=tu-publishable-key
```

---

## 3. Cliente de Supabase

### Obtener instancia

```dart
// En cualquier parte de la app
final supabase = Supabase.instance.client;

// Verificar conexión
final url = supabase.supabaseUrl;
final publishableKey = supabase.supabaseAnonKey; // propiedad mantiene nombre legacy
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

### Métodos adicionales de autenticación

#### Magic Link (passwordless)

```dart
// Enviar magic link al email
await _client.auth.signInWithOtp(
  email: 'user@example.com',
  emailRedirectTo: 'miapp://login-callback',
);

// El usuario hace clic en el enlace → la sesión se crea automáticamente
// Escuchar en onAuthStateChange para detectar el nuevo session
```

#### Autenticación por teléfono + SMS

```dart
// Enviar OTP por SMS
await _client.auth.signInWithOtp(
  phone: '+580000000000',
);

// Verificar OTP
final response = await _client.auth.verifyOTP(
  phone: '+580000000000',
  token: '123456',
  type: OtpType.sms,
);
```

#### Manejo de sesiones

```dart
// Obtener sesión actual
final session = _client.auth.currentSession;
print('Expires at: ${session?.expiresAt}');

// Refrescar token manualmente
await _client.auth.refreshSession();

// Obtener usuario actual
final user = await _client.auth.getUser();
```

#### Deep Links (necesarios para Magic Link y OAuth)

```yaml
# iOS - ios/Runner/Info.plist
# Agregar CFBundleURLTypes
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>miapp</string>
    </array>
  </dict>
</array>
```

```xml
<!-- Android - android/app/src/main/AndroidManifest.xml -->
<intent-filter>
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="miapp" android:host="login-callback" />
</intent-filter>
```

```dart
// Web - usar path url strategy
import 'package:flutter_web_plugins/url_strategy.dart';

void main() {
  usePathUrlStrategy(); // rutas limpias sin #
  runApp(MyApp());
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

Supabase usa RLS para controlar el acceso a las tablas. Las políticas se definen en SQL. Hay **dos capas de seguridad**: los Grants (qué roles pueden tocar una tabla) y las RLS policies (qué filas pueden ver).

```sql
-- Grants: qué roles acceden a la tabla
GRANT SELECT ON public.users TO anon;
GRANT SELECT, INSERT, UPDATE, DELETE ON public.users TO authenticated;

-- Habilitar RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Políticas: qué filas puede ver cada rol
CREATE POLICY "users_select_own" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "users_update_own" ON public.users
    FOR UPDATE USING (auth.uid() = id);
```

### Buenas prácticas de rendimiento

Para mejorar el rendimiento de las policies, envuelve `auth.uid()` en un `SELECT`:

```sql
-- ❌ Lento: auth.uid() se ejecuta por cada fila
USING (auth.uid() = user_id);

-- ✅ Rápido: auth.uid() se ejecuta una vez por sentencia (initPlan)
USING ((SELECT auth.uid()) = user_id);
```

Esto puede dar hasta un **95% de mejora** en tablas grandes.

### Funciones helper de RLS

| Función | Descripción |
|---------|-------------|
| `auth.uid()` | ID del usuario autenticado (o null) |
| `auth.jwt()` | JWT completo del usuario |
| `auth.email()` | Email del usuario |
| `auth.role()` | Rol del usuario (authenticated, anon) |

### Patrones comunes

```sql
-- Solo usuarios autenticados
CREATE POLICY "authenticated_access" ON public.users
    FOR SELECT TO authenticated USING (true);

-- Acceso basado en equipo (vía JWT app_metadata)
CREATE POLICY "team_access" ON public.projects
    FOR SELECT USING (
        team_id IN (SELECT auth.jwt() -> 'app_metadata' -> 'teams')
    );

-- Requerir MFA (AAL2)
CREATE POLICY "mfa_required" ON public.settings
    FOR UPDATE TO authenticated
    USING ((SELECT auth.jwt() ->> 'aal') = 'aal2');

-- Acceso por cliente OAuth
CREATE POLICY "mobile_only" ON public.profiles
    USING (
        auth.uid() = user_id AND
        (auth.jwt() ->> 'client_id') = 'mobile-app'
    );
```

### Desde Flutter (sin autenticación)

```dart
// Esto fallará si no hay políticas para usuarios no autenticados
final response = await supabase.from('users').select();
```

---

## 8. Realtime (Tiempo Real)

Supabase Realtime ofrece tres funcionalidades: **Broadcast** (mensajería entre clientes), **Presence** (estado de usuarios en línea) y **Postgres Changes** (cambios en la base de datos).

### 8.1 Postgres Changes (cambios en BD)

Es el método más simple: escuchar cambios en una tabla.

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

### 8.2 Broadcast (mensajería entre clientes)

Para enviar y recibir mensajes en tiempo real sin depender de la BD:

```dart
// Crear canal con opciones
final channel = supabase.channel(
  'room:lobby:messages',
  opts: const RealtimeChannelConfig(
    self: true,   // recibir los propios mensajes
    ack: true,    // esperar confirmación del server
    private: true,// requiere autenticación + RLS
  ),
);

// Escuchar eventos broadcast
channel.onBroadcast(
  event: 'message_sent',
  callback: (payload) {
    print('Nuevo mensaje: ${payload['text']}');
  },
).subscribe();

// Enviar mensaje
await channel.sendBroadcastMessage(
  event: 'message_sent',
  payload: {
    'text': 'Hola desde Flutter!',
    'user': 'user-123',
    'timestamp': DateTime.now().toIso8601String(),
  },
);
```

### 8.3 Presence (estado de usuarios)

Para saber quién está en línea:

```dart
final channel = supabase.channel('room_01');

// Escuchar eventos de presencia
channel
  .onPresenceSync((_) {
    final state = channel.presenceState();
    print('Usuarios en línea: $state');
  })
  .onPresenceJoin((payload) {
    print('Usuario se conectó: $payload');
  })
  .onPresenceLeave((payload) {
    print('Usuario se desconectó: $payload');
  })
  .subscribe();

// Publicar estado propio
await channel.track({
  'user': 'user-123',
  'name': 'Juan',
  'online_at': DateTime.now().toIso8601String(),
});

// Dejar de publicar
await channel.untrack();
```

### 8.4 Ciclo de vida en widgets Flutter

```dart
class ChatScreen extends StatefulWidget {
  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  RealtimeChannel? _channel;

  @override
  void initState() {
    super.initState();
    _channel = supabase.channel('room:123:messages');
    _channel.onBroadcast(event: 'message', callback: (p) {
      setState(() { /* actualizar UI */ });
    }).subscribe();
  }

  @override
  void dispose() {
    _channel?.unsubscribe(); // siempre cancelar suscripción
    super.dispose();
  }
}
```

### 8.5 Usar en Cubit

```dart
class ChatCubit extends Cubit<ChatState> {
  final RealtimeChannel _channel;
  
  ChatCubit(this._channel) : super(ChatInitial()) {
    _channel.onBroadcast(event: 'message_sent', callback: (payload) {
      if (state is ChatLoaded) {
        final messages = [...(state as ChatLoaded).messages, payload];
        emit(ChatLoaded(messages));
      }
    }).subscribe();
  }
  
  void sendMessage(String text) {
    _channel.sendBroadcastMessage(
      event: 'message_sent',
      payload: {'text': text},
    );
  }
  
  @override
  Future<void> close() {
    _channel.unsubscribe();
    return super.close();
  }
}
```

---

## 9. Storage

### 9.1 Buckets públicos vs privados

| Tipo | Acceso | Uso típico |
|------|--------|------------|
| **Público** | Cualquiera con la URL | Avatares, imágenes de perfil |
| **Privado** | Requiere RLS policies | Documentos, archivos sensibles |

### 9.2 Subir archivos

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
      upsert: false, // true para sobrescribir
    ));

// Subir datos desde memoria (ej. desde cámara)
final bytes = await http.get(Uri.parse('https://ejemplo.com/foto.jpg'));
await supabase.storage
    .from('images')
    .upload('fotos/nueva.jpg', bytes.bodyBytes);
```

### 9.3 Descargar y listar archivos

```dart
// Obtener URL pública
final url = supabase.storage
    .from('avatars')
    .getPublicUrl('user-id/avatar.jpg');

// Descargar archivo como bytes
final data = await supabase.storage
    .from('avatars')
    .download('user-id/avatar.jpg');

// Listar archivos en una carpeta
final files = await supabase.storage
    .from('avatars')
    .list(path: 'user-id/');

// Eliminar archivos
await supabase.storage
    .from('avatars')
    .remove(['user-id/avatar.jpg']);
```

### 9.4 RLS en Storage

El control de acceso a Storage se hace con políticas RLS en la tabla `storage.objects`:

```sql
-- Bucket público: cualquiera puede leer
CREATE POLICY "public_read" ON storage.objects
    FOR SELECT USING (bucket_id = 'avatars');

-- Bucket privado: solo el dueño puede leer
CREATE POLICY "individual_access" ON storage.objects
    FOR SELECT TO authenticated
    USING (
        bucket_id = 'documentos' AND
        (SELECT auth.jwt() ->> 'sub') = owner_id
    );

-- Subida autenticada a carpeta específica
CREATE POLICY "auth_upload" ON storage.objects
    FOR INSERT TO authenticated
    WITH CHECK (
        bucket_id = 'avatars' AND
        (storage.foldername(name))[1] = (SELECT auth.jwt() ->> 'sub')
    );
```

### 9.5 Operaciones avanzadas

```dart
// TUS Resumable Upload (ideal para archivos grandes)
// Usar con el paquete tus_client o uppy
final upload = supabase.storage
    .from('videos')
    .upload('intro.mp4', file);

// S3 API compatible (usar SDK de AWS S3 apuntando a Supabase)
// Endpoint: https://<project>.supabase.co/storage/v1/s3

// Image Transformation (redimensionar desde URL)
// https://<project>.supabase.co/storage/v1/render/image/public/avatars/user.jpg?width=200&height=200
```

---

## 10. Edge Functions

Las Edge Functions son funciones serverless TypeScript que corren en el edge de Supabase (Deno). Se invocan desde Flutter mediante el SDK.

### 10.1 Invocar una función desde Flutter

```dart
// Invocar función sin autenticación
final response = await supabase.functions.invoke('hello-world');
print(response.data);

// Con cuerpo (body)
final response = await supabase.functions.invoke('procesar-pago', body: {
  'amount': 100,
  'currency': 'USD',
});

// Con autenticación (el token JWT se envía automáticamente)
final response = await supabase.functions.invoke('perfil-usuario');
```

### 10.2 Manejo de errores

```dart
try {
  final response = await supabase.functions.invoke('mi-funcion');
  if (response.error != null) {
    print('Error de función: ${response.error}');
  }
} on FunctionsException catch (e) {
  print('Error al invocar: ${e.message}');
}
```

### 10.3 Desarrollo local

```bash
# Las Edge Functions se sirven automáticamente con supabase start
# http://localhost:54321/functions/v1/mi-funcion

# Para desarrollo con hot reload
supabase functions serve mi-funcion
```

### 10.4 Estructura de una Edge Function

```
supabase/
└── functions/
    └── mi-funcion/
        ├── index.ts          # entrypoint
        ├── deno.json         # configuración Deno
        └── _shared/          # código compartido entre funciones
            └── supabase.ts   # cliente Supabase para Deno
```

---

## 11. Errores comunes

### "Row Level Security Error"

```dart
// Verificar que el usuario esté autenticado
final session = supabase.auth.currentSession;
if (session == null) {
  // Redirigir a login
}

// Verificar que las políticas RLS cubren el caso de uso
// Revisar los GRANTs: ¿el rol anon/authenticated tiene permiso?
```

### "Connection refused"

```bash
# Verificar que Supabase local esté corriendo
supabase status

# Verificar que Docker esté corriendo
docker info
```

### "Invalid JWT"

```dart
// El token puede haber expirado, intentar refresh
await supabase.auth.refreshSession();

// Si el refresh falla, redirigir a login
try {
  await supabase.auth.refreshSession();
} catch (e) {
  // Sesión expirada, redirigir a login
  supabase.auth.signOut();
}
```

### "Functions HTTP error"

```dart
// Verificar que la Edge Function existe y está desplegada
// Probar local: supabase functions serve nombre-funcion
// Verificar logs: supabase functions list
```

### "Storage permission denied"

```sql
-- Verificar políticas RLS en storage.objects
-- ¿El bucket existe? ¿El usuario autenticado tiene permisos?
SELECT * FROM storage.buckets;
SELECT * FROM storage.objects LIMIT 5;
```

---

## 12. SupabaseClient vs Dio en Remote DataSources

### ¿Cuándo usar cada uno?

En Clean Architecture con Supabase, el Remote DataSource puede usar **SupabaseClient** o **Dio** dependiendo del caso:

| Criterio | SupabaseClient | Dio |
|----------|---------------|-----|
| **Autenticación** | ✅ Built-in (sesiones, refresh, RLS) | ❌ Manual (JWT, interceptors) |
| **Realtime** | ✅ Postgres Changes, Broadcast, Presence | ❌ No |
| **Storage** | ✅ Upload, download, gestión | ❌ No |
| **Edge Functions** | ✅ Invocación directa | ❌ No |
| **APIs externas** | ❌ No (solo Supabase) | ✅ Cualquier REST API |
| **Interceptors** | ❌ Limitado | ✅ Logging, retry, auth, cache |
| **Control HTTP** | ❌ Abstracted | ✅ Timeouts, headers, cancel tokens |
| **Mock/Test** | ❌ Depende de Supabase | ✅ Fácil (mocktail/DioMock) |

### Regla práctica

```
SupabaseClient → Para operaciones CRUD contra tablas de Supabase
                 (con RLS y autenticación automática)

Dio            → Para APIs externas (pasarelas de pago, servicios de terceros)
                 O cuando necesitas control total sobre las peticiones HTTP
```

### Remote DataSource con SupabaseClient

```dart
// lib/features/user/data/datasources/user_remote_data_source.dart
import 'package:supabase_flutter/supabase_flutter.dart';
import '../../../../core/error/exceptions.dart';
import '../models/user_model.dart';

abstract class UserRemoteDataSource {
  Future<List<UserModel>> getUsers();
  Future<UserModel> getUser(String id);
  Future<void> createUser(UserModel user);
  Future<void> updateUser(UserModel user);
  Future<void> deleteUser(String id);
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final SupabaseClient _supabase;

  UserRemoteDataSourceImpl(this._supabase);

  @override
  Future<List<UserModel>> getUsers() async {
    try {
      final response = await _supabase
          .from('users')
          .select()
          .order('created_at', ascending: false);
      return response.map((json) => UserModel.fromJson(json)).toList();
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<UserModel> getUser(String id) async {
    try {
      final response = await _supabase
          .from('users')
          .select()
          .eq('id', id)
          .maybeSingle();
      if (response == null) {
        throw ServerException(message: 'User not found', statusCode: 404);
      }
      return UserModel.fromJson(response);
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<void> createUser(UserModel user) async {
    try {
      await _supabase.from('users').insert(user.toJson());
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<void> updateUser(UserModel user) async {
    try {
      await _supabase
          .from('users')
          .update(user.toJson())
          .eq('id', user.id);
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<void> deleteUser(String id) async {
    try {
      await _supabase.from('users').delete().eq('id', id);
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }
}
```

### Remote DataSource con Dio (para APIs externas)

```dart
// lib/features/payment/data/datasources/payment_remote_data_source.dart
import 'package:dio/dio.dart';
import '../../../../core/error/exceptions.dart';
import '../models/payment_model.dart';

abstract class PaymentRemoteDataSource {
  Future<PaymentModel> createPayment(PaymentModel payment);
  Future<PaymentModel> getPaymentStatus(String paymentId);
}

class PaymentRemoteDataSourceImpl implements PaymentRemoteDataSource {
  final Dio _client;

  PaymentRemoteDataSourceImpl(this._client);

  @override
  Future<PaymentModel> createPayment(PaymentModel payment) async {
    try {
      final response = await _client.post(
        '/payments',
        data: payment.toJson(),
      );
      return PaymentModel.fromJson(response.data);
    } on DioException catch (e) {
      throw ServerException(
        message: e.message ?? 'Payment failed',
        statusCode: e.response?.statusCode,
      );
    }
  }

  @override
  Future<PaymentModel> getPaymentStatus(String paymentId) async {
    try {
      final response = await _client.get('/payments/$paymentId');
      return PaymentModel.fromJson(response.data);
    } on DioException catch (e) {
      throw ServerException(
        message: e.message ?? 'Failed to get payment status',
        statusCode: e.response?.statusCode,
      );
    }
  }
}
```

### Inyección en el contenedor de DI

```dart
// lib/core/di/injection_container.dart
// SupabaseClient — Singleton global
sl.registerLazySingleton<SupabaseClient>(() => Supabase.instance.client);

// Dio — Cliente HTTP para APIs externas
sl.registerLazySingleton<Dio>(() {
  final dio = Dio(BaseOptions(
    baseUrl: 'https://api.externa.com',
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));
  dio.interceptors.add(LogInterceptor(
    requestBody: true,
    responseBody: true,
  ));
  return dio;
});

// Remote DataSources
sl.registerLazySingleton<UserRemoteDataSource>(
  () => UserRemoteDataSourceImpl(sl<SupabaseClient>()),
);
sl.registerLazySingleton<PaymentRemoteDataSource>(
  () => PaymentRemoteDataSourceImpl(sl<Dio>()),
);
```

---

## ✅ Checklist de integración con Flutter

- [ ] `supabase_flutter` añadido en pubspec.yaml
- [ ] Supabase inicializado en main.dart con `publishableKey:`
- [ ] Cliente accesible desde cualquier parte de la app
- [ ] Autenticación implementada con Cubit/BLoC
- [ ] Magic Link / OAuth con deep links configurados (iOS/Android/Web)
- [ ] Manejo de sesiones (refresh, expiración)
- [ ] Repository implementa operaciones CRUD
- [ ] RLS configurado en la base de datos (con óptimo `SELECT auth.uid()`)
- [ ] Realtime: Postgres Changes y/o Broadcast según el caso
- [ ] Storage: políticas RLS en `storage.objects`
- [ ] Edge Functions: invocación y manejo de errores
- [ ] Variables de entorno configuradas
- [ ] Tests de integración funcionando
- [ ] Definido qué DataSource usa SupabaseClient vs Dio según el caso

---

## 📚 Recursos

- [Supabase Flutter SDK (referencia)](https://supabase.com/docs/reference/dart/initializing)
- [Tutorial: User Management App con Flutter](https://supabase.com/docs/guides/getting-started/tutorials/with-flutter)
- [Supabase Auth (guía)](https://supabase.com/docs/guides/auth)
- [Supabase Realtime (guía)](https://supabase.com/docs/guides/realtime)
- [Supabase Storage (guía)](https://supabase.com/docs/guides/storage)
- [Edge Functions (guía)](https://supabase.com/docs/guides/functions)
- [Row Level Security (guía)](https://supabase.com/docs/guides/database/postgres/row-level-security)


---

## 📚 Referencias

- [Supabase | Documentación oficial](https://supabase.com/docs) — Guías, API reference y arquitectura
- [Supabase | CLI reference](https://supabase.com/docs/reference/cli) — Comandos de la CLI de Supabase
- [Supabase | Flutter SDK](https://pub.dev/packages/supabase_flutter) — SDK oficial para Flutter
- [Supabase | Migraciones](https://supabase.com/docs/guides/local-development/migrations) — Gestión de migraciones locales

---

> 📖 **Siguiente:** [07-testing-local-supabase.md](./07-testing-local-supabase.md)