# 04 - Play App Signing y In-App Updates

> Play App Signing protege tu llave de firma. In-app Updates permite actualizar la app desde adentro sin pasar por Play Store.

---

## 1. Play App Signing

### 1.1 ¿Qué es?

Google Play se encarga de firmar tu APK final con una llave maestra. Tú solo necesitas una "upload key" para subir el AAB.

```
Tú (Upload Key)                    Google (Play App Signing)
       │                                     │
       │  Subes AAB firmado con upload key   │
       │────────────────────────────────────>│
       │                                     │
       │                                     │  Google firma el APK final
       │                                     │  con su llave maestra
       │                                     │
       │                                     │  Distribuye a usuarios
```

**Ventajas:**
- Si pierdes el upload key, puedes generar una nueva
- Google maneja la seguridad de la firma final
- Compatible con APK Expansion Files (.obb)

### 1.2 Cómo Configurarlo

```
Play Console > Configuración avanzada > Configuración de la app
  > Play App Signing
```

1. Play Console genera un par de llaves (App Signing Key)
2. Tú generas tu Upload Key (keystore)
3. Registras el certificado de Upload Key en Play Console
4. Subes AABs firmados con tu Upload Key

### 1.3 Obtener el Certificado

Si empezaste antes de Play App Signing:

```bash
# Tu app ya está firmada con tu keystore original
# Para migrar a Play App Signing:
# 1. Subir el certificado original a Play Console
# 2. Google lo usa como App Signing Key
# 3. Puedes generar una nueva Upload Key para futuros AABs
```

### 1.4 Si Pierdes la Upload Key

```bash
# 1. Contactar soporte de Google Play
# 2. Solicitar reset de upload key
# 3. Generar nueva upload key en tu máquina
# 4. Registrar nuevo certificado en Play Console
```

---

## 2. In-App Updates

### 2.1 ¿Qué es?

Permite que los usuarios actualicen la app desde adentro, sin ir a Play Store.

```
App versión 1.0              Play Store
      │                           │
      │  checkForUpdate()         │
      │──────────────────────────>│
      │                           │
      │  {"updateAvailable": true} │
      │<──────────────────────────│
      │                           │
      │  Inicia descarga          │
      │  Muestra progreso         │
      │  Instala actualización    │
      │  (sin salir de la app)    │
```

### 2.2 Tipos de Actualización

| Tipo | UX | Cuándo Usar |
|------|-----|-------------|
| **Inmediata** | Bloquea la app hasta actualizar | Cambios críticos de seguridad |
| **Flexible** | Sugiere actualizar, puede ignorar | Mejoras normales |

### 2.3 Instalación

```yaml
# pubspec.yaml
dependencies:
  flutter_inappupdate: ^1.0.0
```

### 2.4 Implementación

```dart
// core/services/update_service.dart
import 'package:flutter_inappupdate/flutter_inappupdate.dart';

class UpdateService {
  /// Verificar actualización flexible
  Future<void> checkForFlexibleUpdate() async {
    try {
      final status = await FlutterInappUpdate.checkForUpdate();

      if (status.updateAvailability == UpdateAvailability.updateAvailable) {
        // Mostrar diálogo opcional
        final shouldUpdate = await _showUpdateDialog();

        if (shouldUpdate) {
          await FlutterInappUpdate.performImmediateUpdate();
        }
      }
    } catch (e) {
      // Si falla, no bloquear. El usuario puede actualizar manualmente.
      print('Update check failed: $e');
    }
  }

  /// Actualización inmediata (obligatoria)
  Future<void> performImmediateUpdate() async {
    try {
      final status = await FlutterInappUpdate.checkForUpdate();

      if (status.updateAvailability == UpdateAvailability.updateAvailable) {
        await FlutterInappUpdate.performImmediateUpdate();
      }
    } catch (e) {
      print('Immediate update failed: $e');
    }
  }
}
```

### 2.5 Integración con Cubit

```dart
// core/cubit/update_cubit.dart
@injectable
class UpdateCubit extends Cubit<UpdateState> {
  final UpdateService _updateService;

  UpdateCubit(this._updateService) : super(const UpdateInitial());

  Future<void> checkForUpdate() async {
    emit(const UpdateChecking());

    try {
      await _updateService.checkForFlexibleUpdate();
      emit(const UpdateChecked());
    } catch (e) {
      emit(UpdateError(e.toString()));
    }
  }
}
```

### 2.6 En App Startup

```dart
// main.dart
Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await init(); // Injectable

  // Verificar actualización al inicio
  getIt<UpdateCubit>().checkForUpdate();

  runApp(const MyApp());
}
```

### 2.7 Manejo de Estados de Actualización

```dart
class UpdateService {
  StreamSubscription? _subscription;

  void listenToUpdateStatus() {
    _subscription = FlutterInappUpdate.installStatusStream.listen((status) {
      switch (status.installStatus) {
        case InstallStatus.downloaded:
          // Mostrar botón "Reiniciar para actualizar"
          _showRestartDialog();
          break;
        case InstallStatus.installed:
          print('App actualizada exitosamente');
          break;
        case InstallStatus.failed:
          print('Error en instalación');
          break;
        default:
          break;
      }
    });
  }

  void dispose() {
    _subscription?.cancel();
  }
}
```

---

## 3. Play App Integrity

### 3.1 ¿Qué es?

Verifica que tu app se está ejecutando en un dispositivo Android legítimo y no ha sido modificada.

```dart
// Para apps que manejan pagos o datos sensibles
// Se integra con Play Console > Integridad de la aplicación
```

**No implementado aún en el proyecto pero importante saber:**
- Previene cheating/tampering
- Verifica que la app fue instalada desde Play Store
- Útil para apps de lotería/rifas con dinero real

---

## 4. Buenas Prácticas

### 4.1 Play App Signing

```bash
# ✅
- Generar upload key y guardar en 2+ lugares seguros
- Registrar certificado en Play Console
- Usar CI/CD con secrets para firmar automáticamente

# ❌
- Perder el keystore (aunque puedes resetear con Play Signing)
- Compartir la upload key por email/chats
- Comitar el keystore en el repo
```

### 4.2 In-App Updates

```bash
# ✅
- Usar flexible para actualizaciones normales
- Usar inmediata solo para parches de seguridad críticos
- Informar al usuario qué cambia en la actualización

# ❌
- Forzar actualización inmediata sin razón
- No manejar el caso de "no hay conexión"
- Ignorar el estado de descarga (mostrar progreso)
```

---

## 5. Resumen

1. **Play App Signing** protege tu llave de firma (Google la maneja)
2. **Upload key** para subir AABs (guardar SIEMPRE)
3. **In-App Updates** permite actualizar sin ir a Play Store
4. **Inmediata** para cambios críticos, **Flexible** para mejoras
5. **Play Integrity** verifica autenticidad del dispositivo
6. **Probar in-app updates** en pista Internal Testing antes de producción

---

## Recursos

- [Play App Signing Guide](https://support.google.com/googleplay/android-developer/answer/9842756)
- [In-app Updates](https://developer.android.com/guide/playcore/in-app-updates)
- [flutter_inappupdate pub.dev](https://pub.dev/packages/flutter_inappupdate)
- [Play Integrity API](https://developer.android.com/google/play/integrity)

---

## 📚 Referencias

- [Flutter | Android deployment](https://docs.flutter.dev/deployment/android) — Guía oficial para publicar en Play Store
- [Google Play | Console Help](https://support.google.com/googleplay/android-developer) — Centro de ayuda de Google Play Console
- [Flutter | Build and release](https://docs.flutter.dev/deployment) — Compilación para múltiples plataformas

---
