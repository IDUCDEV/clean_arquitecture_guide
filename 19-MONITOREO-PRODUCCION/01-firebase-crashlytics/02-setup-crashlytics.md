# 02 - Setup Crashlytics

## Prerrequisitos

Antes de configurar Crashlytics necesitas:

1. Proyecto Firebase creado
2. Firebase CLI instalado
3. Flutter project configurado con Firebase

---

## Paso 1: Crear proyecto Firebase

```bash
# Instalar Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Crear proyecto (si no existe)
firebase projects:create mi-app-flutter
```

O crear desde [Firebase Console](https://console.firebase.google.com/).

---

## Paso 2: Instalar dependencias

```yaml
# pubspec.yaml
dependencies:
  firebase_core: ^3.12.1
  firebase_crashlytics: ^4.3.1
```

```bash
flutter pub get
```

---

## Paso 3: Configurar Firebase para Flutter

```bash
# Instalar FlutterFire CLI
dart pub global activate flutterfire_cli

# Configurar Firebase en tu proyecto
flutterfire configure
```

Esto genera `lib/firebase_options.dart`.

---

## Paso 4: Inicializar Firebase

```dart
// lib/main.dart
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  
  runApp(MyApp());
}
```

---

## Paso 5: Configurar Crashlytics

### Error Handler Principal

```dart
// lib/main.dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // 1. Configurar error handler global
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
  
  // 2. Capturar errores asincronos
  runZonedGuarded(() {
    runApp(MyApp());
  }, (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack);
  });

  // 3. Configurar identificador de usuario (opcional)
  FirebaseCrashlytics.instance.setUserIdentifier('user123');
  
  // 4. Configurar custom keys iniciales
  await FirebaseCrashlytics.instance.setCustomKey('env', 'production');
  await FirebaseCrashlytics.instance.setCustomKey('flavor', 'premium');
}
```

### Configuracion Completa

```dart
// lib/main.dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // Habilitar Crashlytics en release
  if (!kDebugMode) {
    await FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(true);
  }

  // Error handler para Flutter errors
  FlutterError.onError = (FlutterErrorDetails details) {
    FirebaseCrashlytics.instance.recordFlutterFatalError(details);
    
    // En debug, tambien imprimir
    if (kDebugMode) {
      FlutterError.presentError(details);
    }
  };

  // Error handler para errores asincronos
  runZonedGuarded(() {
    runApp(MyApp());
  }, (error, stack) {
    FirebaseCrashlytics.instance.recordError(
      error,
      stack,
      reason: 'Async error caught by runZonedGuarded',
    );
  });
}
```

---

## Paso 6: Platform-specific Configuration

### Android

```android/app/build.gradle
android {
    compileSdkVersion 34
    
    defaultConfig {
        minSdkVersion 21
        targetSdkVersion 34
    }
    
    dependencies {
        // Firebase BoM
        implementation platform('com.google.firebase:firebase-bom:33.7.0')
        implementation 'com.google.firebase:firebase-crashlytics'
    }
}
```

### iOS

```ios/Podfile
platform :ios, '15.0'

target 'Runner' do
  use_frameworks!
  pod 'Firebase/Crashlytics'
end
```

---

## Paso 7: Verificar Setup

### En Debug

```dart
// Boton de prueba en tu app
ElevatedButton(
  onPressed: () async {
    try {
      // Forzar error
      throw Exception('Test crash from Flutter!');
    } catch (error, stackTrace) {
      await FirebaseCrashlytics.instance.recordError(
        error,
        stackTrace,
        reason: 'Manual test crash',
      );
      print('Error enviado a Crashlytics');
    }
  },
  child: Text('Test Crash'),
),
```

### En Release

```dart
// Verificar estado
final instance = FirebaseCrashlytics.instance;

print('Crashlytics habilitado: ${instance.isCrashlyticsCollectionEnabled}');
print('User ID: ${instance.app.name}');
```

---

## Paso 8: Subir dSYM (iOS)

Para iOS, necesitas subir los archivos dSYM para symbolication.

### Automatico (Recomendado)

```bash
# Instalar Firebase CLI
npm install -g firebase-tools

# Subir dSYM automaticamente
firebase crashlytics:symbols:upload --app ios-com-example-app build/ios/archive/MyApp.xcarchive/dSYMs
```

### En Xcode

1. Abrir `MyApp.xcworkspace`
2. Product → Archive
3. En el Organizer, clic en "Distribute App"
4. Seleccionar "App Store Connect"
5. Marcar "Upload your app's symbols"

---

## Paso 9: Configure Firebase Console

### Habilitar Crashlytics

1. Ir a [Firebase Console](https://console.firebase.google.com/)
2. Seleccionar proyecto
3. Ir a "Crashlytics"
4. Clic "Enable Crashlytics"
5. Seguir instrucciones

### Configurar Alertas

1. Ir a "Crashlytics" → "Alerts"
2. Clic "Add alert"
3. Seleccionar tipo:
   - **Issue count**: Alertar cuando hay N nuevos issues
   - **Crash rate**: Alertar cuando el crash-free rate baja
   - **Velocity**: Alertar cuando un crash afecta muchos usuarios rapido

---

## Paso 10: Produccion

### Checklist

- [ ] `kDebugMode` deshabilita Crashlytics en debug
- [ ] Error handlers configurados (`FlutterError.onError` + `runZonedGuarded`)
- [ ] dSYM subidos (iOS)
- [ ] ProGuard rules configurados (Android)
- [ ] Alertas configuradas en Firebase Console
- [ ] Custom keys iniciales configuradas
- [ ] User ID configurado

### Ejemplo Final

```dart
// lib/main.dart
import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';
import 'firebase_options.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  // Configurar Crashlytics
  final crashlytics = FirebaseCrashlytics.instance;
  
  // Habilitar solo en release
  if (!kDebugMode) {
    await crashlytics.setCrashlyticsCollectionEnabled(true);
  }

  // Error handlers
  FlutterError.onError = crashlytics.recordFlutterFatalError;
  
  runZonedGuarded(() {
    runApp(MyApp());
  }, (error, stack) {
    crashlytics.recordError(error, stack);
  });

  // Custom keys globales
  await crashlytics.setCustomKey('app_version', '1.0.0');
  await crashlytics.setCustomKey('environment', 'production');
}
```

---

## Troubleshooting

| Problema | Solucion |
|---|---|
| Crashlytics no recibe errores | Verificar que `kDebugMode` esta configurado |
| dSYM no se sube (iOS) | Usar `firebase crashlytics:symbols:upload` |
| Errores no symbolificados | Verificar dSYM en Firebase Console |
| Crashlytics habilitado en debug | Configurar `kDebugMode` check |

---

## Siguiente paso

[03 - Non-Fatal Errors](./03-non-fatal-errors.md) - Reportar errores que no cierran la app
