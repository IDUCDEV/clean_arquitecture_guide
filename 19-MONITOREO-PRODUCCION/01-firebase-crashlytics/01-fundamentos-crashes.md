# 01 - Fundamentos de Crashes

## Que es un crash?

Un **crash** es cuando tu app se cierra inesperadamente. El usuario pierde el contexto, la sesion se interrumpe, y si no hay monitoreo, nunca te enteras.

```
App运行正常
  └── Usuario toca un boton
    └── Codigo falla
      └── App se cierra
        └── Usuario frustrado
          └── Si no hay monitoreo, no sabes que paso
```

---

## Tipos de errores

### 1. Errores Fatales (Crashes)

Cierran la app completamente. El usuario pierde todo el estado.

```dart
// Esto causa un crash fatal
final data = jsonDecode(invalidJson); // FormatException
final result = list[10]; // RangeError
final user = null!; // LateInitializationError
```

**Caracteristicas:**
- App se cierra inmediatamente
- Estado perdido
- Stack trace completo disponible
- Crashlytics lo captura automaticamente

### 2. Errores No Fatales

No cierran la app, pero afectan funcionalidad. El usuario puede seguir usando la app.

```dart
try {
  final response = await http.get(Uri.parse('https://api.example.com/data'));
  if (response.statusCode != 200) {
    throw Exception('Failed to load data');
  }
} catch (e, stack) {
  // Error no fatal: reportar pero no crashear
  FirebaseCrashlytics.instance.recordError(
    e,
    stack,
    reason: 'API request failed',
  );
  // Mostrar UI de error al usuario
  showErrorUI('No se pudieron cargar los datos');
}
```

**Caracteristicas:**
- App sigue funcionando
- Puedes reportar con contexto
- Stack trace opcional
- Debes usar `recordError` manualmente

### 3. ANR (Application Not Responding)

La app no responde por mas de 5 segundos. En Android, el sistema muestra un dialogo.

```dart
// Esto puede causar ANR
await Future.delayed(Duration(seconds: 10)); // Bloquea el main thread
// Operaciones pesadas sin async
for (var i = 0; i < 1000000; i++) {
  // Calculo intensivo en main thread
}
```

**Caracteristicas:**
- App se "congela"
- Android muestra dialogo "ANR"
- iOS: watchdog timer mata la app
- Difícil de detectar sin monitoreo

### 4. Excepciones Flutter

Errores del framework Flutter que no son crashes.

```dart
// Error de rendering
LateInitializationError: Field 'user' has not been initialized

// Error de layout
RenderFlex overflowed: 92 pixels on the bottom

// Error de setState
setState() called after dispose()
```

---

## Metricas clave

### Crash-Free Sessions

El porcentaje de sesiones que no tuvieron crashes.

```
Sesiones totales: 10,000
Sesiones con crash: 150
Crash-free rate: 98.5%
```

**Meta comun:**
- Basico: 95%+
- Bueno: 98%+
- Excelente: 99%+
- Elite: 99.5%+

### Crash-Free Users

El porcentaje de usuarios unicos que no experimentaron crashes.

```
Usuarios totales: 5,000
Usuarios con crash: 100
Crash-free users: 98%
```

### Impacto por version

```dart
// Comparar entre versiones
Version 1.0.0: 95% crash-free
Version 1.0.1: 98% crash-free  // Mejora!
Version 1.0.2: 92% crash-free  // Regresion!
```

### Top Issues

Los crashes mas frecuentes ordenados por impacto.

```
1. FormatException en login (1,234 ocurrencias)
2. SocketException en checkout (892 ocurrencias)
3. RangeError en products (456 ocurrencias)
```

---

## Flujo de monitoreo

```
App en produccion
  └── Error ocurre
    └── Crashlytics captura
      └── Agrega contexto (device, user, version)
        └── Agrupa con errores similares
          └── Envia a Firebase Console
            └── Tu recibes notificacion
              └── Analizas el problema
                └── Fix en el codigo
                  └── Nueva version
                    └── Crash eliminado
```

---

## Build Modes y Crashlytics

### Debug
```dart
// En debug, Crashlytics esta deshabilitado
// Los errores se muestran en la consola
FlutterError.onError = (details) {
  print('Error: ${details.exception}');
};
```

### Profile
```dart
// En profile, Crashlytics captura pero no envia
// Util para testing en dispositivos reales
FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(true);
```

### Release
```dart
// En release, Crashlytics funciona completamente
// Captura y envia todos los errores
FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(true);
```

---

## Errores comunes en Flutter

| Error | Causa | Solucion |
|---|---|---|
| `FormatException` | JSON mal formado | Validar antes de parsear |
| `SocketException` | Sin conexion a internet | Verificar conexion antes de HTTP |
| `TimeoutException` | Request tardo demasiado | Configurar timeout |
| `RangeError` | Acceso a indice invalido | Verificar longitud de lista |
| `StateError` | Future completo sin valor | Manejar estado correctamente |
| `TypeError` | Cast incorrecto | Usar null safety correctamente |
| `PlatformException` | Error nativo | Manejar por plataforma |
| `MissingPluginException` | Plugin no encontrado | Verificar configuracion |

---

## Ejemplo: errores en Clean Architecture

```dart
// En la capa de dominio (no tiene dependencias de errores)
abstract class UserRepository {
  Future<User> getUser(String id);
}

// En la capa de datos (maneja errores de infraestructura)
class SupabaseUserRepository implements UserRepository {
  @override
  Future<User> getUser(String id) async {
    try {
      final response = await supabase
          .from('users')
          .select()
          .eq('id', id)
          .single();
      
      return UserMapper.fromMap(response);
    } catch (e, stack) {
      // Reportar a Crashlytics
      await FirebaseCrashlytics.instance.recordError(
        e,
        stack,
        reason: 'Failed to get user from Supabase',
        information: ['user_id: $id'],
      );
      
      // Lanzar excepcion de dominio
      throw ServerException('Failed to load user');
    }
  }
}

// En la capa de presentacion (maneja errores de UI)
class UserCubit extends Cubit<UserState> {
  final GetUserUseCase getUserUseCase;

  Future<void> loadUser(String id) async {
    try {
      emit(UserLoading());
      final user = await getUserUseCase(id);
      emit(UserLoaded(user));
    } on ServerException catch (e) {
      // Error conocido de dominio
      emit(UserError(e.message));
    } catch (e, stack) {
      // Error desconocido
      await FirebaseCrashlytics.instance.recordError(
        e,
        stack,
        reason: 'Unexpected error loading user',
        information: ['user_id: $id'],
      );
      emit(UserError('Error inesperado'));
    }
  }
}
```

---

## Resumen

| Tipo | Impacto | Captura | Accion |
|---|---|---|---|
| Fatal | App cierra | Automatica | Fix urgente |
| No fatal | Funcion afectada | Manual (`recordError`) | Fix prioritario |
| ANR | App congelada | Automatica | Optimizar performance |
| Flutter Exception | UI afectada | Automatica (si configuraste) | Fix rapido |

---

## Siguiente paso

[02 - Setup Crashlytics](./02-setup-crashlytics.md) - Configurar Crashlytics en tu proyecto Flutter
