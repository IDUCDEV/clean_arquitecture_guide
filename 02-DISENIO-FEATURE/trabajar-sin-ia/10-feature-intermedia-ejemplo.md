# Feature Intermedia: Sistema de Notificaciones Push

> Ejemplo de feature intermedia con múltiples componentes: Firebase Cloud Messaging, manejo de permisos, registro de tokens, y proceso de notificaciones en background.

---

## Contexto

**Feature:** Sistema de notificaciones push para una app de e-commerce
**Complejidad:** Intermedia
**Tiempo estimado:** 4-6 horas

---

## FASE 1: Investigar (45 min)

### User Story

```
**Como** usuario de la app de e-commerce,
**quiero** recibir notificaciones push sobre ofertas, estado de pedidos y mensajes,
**para** estar informado sin abrir la app constantemente.
```

### Investigación de herramientas

```markdown
## Investigación: Notificaciones Push con Firebase

### Qué necesito
- Firebase Cloud Messaging (FCM) para notificaciones push
- firebase_messaging (Flutter plugin)
- Manejo de permisos en iOS/Android
- Registro de tokens en backend

### Documentación oficial
- Firebase Messaging: https://firebase.google.com/docs/cloud-messaging
- firebase_messaging: https://firebase.google.com/docs/flutter/setup
- Permisos iOS: https://developer.apple.com/documentation/usernotifications

### Dependencias nuevas
- firebase_messaging: ^14.0.0

### Complejidad: Intermedia
- Múltiples componentes (Firebase, permisos, tokens, background)
- Manejo de estados en múltiples plataformas
- Configuración de servidores (FCM console)

### Restricciones conocidas
- iOS requiere permiso explícito del usuario
- Android 13+ requiere permiso de notificaciones
- Tokens deben actualizarse cuando cambian
- Background messages requieren handler separado
```

### Preguntas que te haces

1. ¿Cómo funcionan las notificaciones push a nivel técnico?
2. ¿Qué permisos necesito en cada plataforma?
3. ¿Cómo registro el token del usuario en el backend?
4. ¿Cómo manejo notificaciones en background vs foreground?
5. ¿Qué pasa cuando el usuario desactiva notificaciones?

---

## FASE 2: Diseñar (45 min)

### Descomposición (FADER)

| Paso | Qué hago | Resultado |
|------|----------|-----------|
| **F**ormular | User Story definida | ✅ |
| **A**ctorizar | 2 actores: usuario, servidor (FCM) | ✅ |
| **D**escomponer | Solicitar permiso, obtener token, registrar token, recibir notificación, procesar en background | ✅ |
| **E**ntidades | Token, NotificacionPush | ✅ |
| **R**eglas | Permiso requerido, token único por dispositivo, notificación se muestra o se ignora según estado | ✅ |

### Entidades

```dart
// lib/domain/entities/token_fcm.dart

class TokenFcm {
  final String token;
  final String usuarioId;
  final DateTime fechaCreacion;
  final DateTime? fechaExpiracion;

  const TokenFcm({
    required this.token,
    required this.usuarioId,
    required this.fechaCreacion,
    this.fechaExpiracion,
  });

  bool get estaExpirado {
    if (fechaExpiracion == null) return false;
    return DateTime.now().isAfter(fechaExpiracion!);
  }
}
```

```dart
// lib/domain/entities/notificacion_push.dart

class NotificacionPush {
  final String titulo;
  final String cuerpo;
  final Map<String, dynamic>? datos;
  final DateTime fechaRecepcion;

  const NotificacionPush({
    required this.titulo,
    required this.cuerpo,
    this.datos,
    required this.fechaRecepcion,
  });
}
```

### Contratos

```dart
// lib/domain/repositories/notificacion_repository.dart

abstract class NotificacionRepository {
  /// Solicita permiso al usuario para recibir notificaciones
  Future<Either<Failure, bool>> solicitarPermiso();

  /// Obtiene el token FCM del dispositivo
  Future<Either<Failure, String>> obtenerToken();

  /// Registra el token en el servidor
  Future<Either<Failure, void>> registrarToken({
    required String token,
    required String usuarioId,
  });

  /// Elimina el token del servidor (logout)
  Future<Either<Failure, void>> eliminarToken({required String token});

  /// Verifica si las notificaciones están habilitadas
  Future<bool> notificacionesHabilitadas();
}
```

### Flujo de datos

```
Inicio de sesión:
App → solicitarPermiso() → obtainToken() → registrarToken() → Supabase

Notificación recibida (foreground):
FCM → onMessage → Mostrar SnackBar/Dialog

Notificación recibida (background):
FCM → onBackgroundMessage → Procesar datos → Actualizar UI

Notificación recibida (app cerrada):
FCM → Tap en notificación → Abrir app → Navegar a pantalla específica
```

### Estados

```dart
enum NotificacionStatus {
  noSolicitado,
  permisoDenegado,
  permisoConcedido,
  tokenRegistrado,
  error,
}
```

### Excepciones a manejar

| Excepción | Cuándo ocurre | Qué mostrar |
|-----------|---------------|-------------|
| Permiso denegado | Usuario rechaza notificaciones | "Sin notificaciones. Puedes activarlas en Configuración." |
| Token nulo | Error al obtener token | "Error al configurar notificaciones" |
| Error de red | Sin conexión al registrar | "Error al registrar notificaciones" |
| Token expirado | Token vencido | Renovar silenciosamente |

---

## FASE 3: Implementar (2.5-3.5 horas)

### Orden de implementación

```
1. Dominio
   ├── token_fcm.dart (entidad)
   ├── notificacion_push.dart (entidad)
   └── notificacion_repository.dart (contrato)

2. Data
   ├── notificacion_repository_impl.dart (implementación)

3. Presentation
   ├── notificacion_service.dart (servicio principal)
   ├── notificacion_controller.dart (estado)
   └── notificacion_config_page.dart (UI configuración)
```

### Implementación clave

**Servicio principal**
```dart
// lib/data/services/notificacion_service.dart

class NotificacionService {
  final FirebaseMessaging _messaging;
  final NotificacionRepository _repository;

  NotificacionService(this._messaging, this._repository);

  Future<void> inicializar(String usuarioId) async {
    // Solicitar permiso
    final permiso = await _repository.solicitarPermiso();
    if (permiso.isLeft()) return;

    // Obtener token
    final tokenResult = await _repository.obtenerToken();
    if (tokenResult.isLeft()) return;

    final token = tokenResult.getOrElse(() => '');

    // Registrar en servidor
    await _repository.registrarToken(token: token, usuarioId: usuarioId);

    // Configurar handlers
    _configurarHandlers();
  }

  void _configurarHandlers() {
    // Foreground
    FirebaseMessaging.onMessage.listen(_onForegroundMessage);

    // Background
    FirebaseMessaging.onBackgroundMessage(_onBackgroundMessage);

    // App abierta desde notificación
    FirebaseMessaging.onMessageOpenedApp.listen(_onMessageOpenedApp);
  }

  void _onForegroundMessage(RemoteMessage message) {
    // Mostrar notificación local o SnackBar
    final notificacion = NotificacionPush(
      titulo: message.notification?.title ?? '',
      cuerpo: message.notification?.body ?? '',
      datos: message.data,
      fechaRecepcion: DateTime.now(),
    );
    // Notificar a la UI
  }

  @pragma('vm:entry-point')
  static Future<void> _onBackgroundMessage(RemoteMessage message) async {
    // Procesar en background (no puede acceder a UI)
    // Ejemplo: guardar en base de datos local
  }

  void _onMessageOpenedApp(RemoteMessage message) {
    // Navegar a pantalla específica según datos
    // Ejemplo: si es notificación de pedido, abrir pantalla de pedido
  }
}
```

**Configuración por plataforma**
```dart
// Android: android/app/build.gradle
// Agregar:
defaultConfig {
    // ...
    manifestPlaceholders = [
        'firebaseMessagingDefaultChannelId': 'general',
        'firebaseMessagingDefaultChannelName': 'General',
    ]
}

// iOS: Info.plist
// Agregar:
<key>UIBackgroundModes</key>
<array>
    <string>fetch</string>
    <string>remote-notification</string>
</array>
```

---

## FASE 4: Verificar (30 min)

### Tests

```dart
// test/data/services/notificacion_service_test.dart

void main() {
  test('Solicitar permiso concedido', () async {
    final repository = MockNotificacionRepository();
    when(repository.solicitarPermiso())
        .thenAnswer((_) async => const Right(true));

    final result = await repository.solicitarPermiso();
    expect(result.isRight(), true);
  });

  test('Manejar permiso denegado', () async {
    final repository = MockNotificacionRepository();
    when(repository.solicitarPermiso())
        .thenAnswer((_) async => const Left(PermissionDeniedFailure()));

    final result = await repository.solicitarPermiso();
    expect(result.isLeft(), true);
  });
}
```

### Prueba manual

```
1. Instalar en dispositivo real (no emulador)
2. Abrir app → Debe solicitar permiso
3. Conceder permiso → Token se registra
4. Enviar notificación desde Firebase Console → Se recibe
5. Cerrar app → Enviar notificación → Tocar → Abre app
6. Desactivar notificaciones → Mensaje informativo
```

---

## FASE 5: Refactor (20 min)

### Verificaciones

- [ ] Handlers de background están en top-level functions
- [ ] Token se renueva automáticamente
- [ ] Errores de red se manejan correctamente
- [ ] No hay dependencias circulares

---

## FASE 6: Validar con IA (15 min)

### Prompt

```
Revisa mi implementación de notificaciones push con Firebase.
¿El manejo de permisos es correcto para iOS y Android?
¿Los handlers de background están bien configurados?
¿Cómo manejo la reconexión y renovación de tokens?
NO reescribas el código, solo dame feedback.
```

---

## Tiempo total: 4.5-6 horas

| Fase | Tiempo |
|------|--------|
| Investigar | 45 min |
| Diseñar | 45 min |
| Implementar | 2.5-3.5 horas |
| Verificar | 30 min |
| Refactor | 20 min |
| Validar | 15 min |

---

**Siguiente:** [11-feature-compleja-ejemplo.md](./11-feature-compleja-ejemplo.md) — Feature compleja: Pasarela de pagos con Stripe
