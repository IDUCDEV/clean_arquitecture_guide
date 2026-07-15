# 07 - Cheatsheet Crashlytics

## Setup Rapido

```dart
// pubspec.yaml
dependencies:
  firebase_core: ^3.12.1
  firebase_crashlytics: ^4.3.1

// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  
  FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
  
  runZonedGuarded(() {
    runApp(MyApp());
  }, (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack);
  });
}
```

---

## Comandos Esenciales

| Comando | Descripcion |
|---|---|
| `FirebaseCrashlytics.instance.recordError(error, stack)` | Reportar error no fatal |
| `FirebaseCrashlytics.instance.crash()` | Forzar crash (debug) |
| `FirebaseCrashlytics.instance.log('message')` | Agregar log |
| `FirebaseCrashlytics.instance.setCustomKey('key', 'value')` | Agregar custom key |
| `FirebaseCrashlytics.instance.setUserIdentifier('id')` | Establecer user ID |
| `FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(bool)` | Habilitar/deshabilitar |
| `FirebaseCrashlytics.instance.sendUnsentReports()` | Enviar reportes pendientes |
| `FirebaseCrashlytics.instance.checkForUnsentReports()` | Verificar reportes pendientes |
| `FirebaseCrashlytics.instance.deleteUnsentReports()` | Eliminar reportes pendientes |

---

## Error Handlers

```dart
// Flutter errors
FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;

// Async errors
runZonedGuarded(() {
  runApp(MyApp());
}, (error, stack) {
  FirebaseCrashlytics.instance.recordError(error, stack);
});
```

---

## Record Error con Contexto

```dart
await FirebaseCrashlytics.instance.recordError(
  error,
  stack,
  reason: 'User-friendly reason',
  information: ['key1: value1', 'key2: value2'],
);
```

---

## Custom Keys

```dart
// Global (en main.dart)
await FirebaseCrashlytics.instance.setCustomKey('env', 'production');
await FirebaseCrashlytics.instance.setCustomKey('app_version', '1.0.0');

// Dinamico
await FirebaseCrashlytics.instance.setCustomKey('screen', 'checkout');
await FirebaseCrashlytics.instance.setCustomKey('user_plan', 'premium');
```

---

## User Identifier

```dart
// Login
await FirebaseCrashlytics.instance.setUserIdentifier(user.id);

// Logout
await FirebaseCrashlytics.instance.setUserIdentifier('anonymous');
```

---

## Custom Logs

```dart
FirebaseCrashlytics.instance.log('Starting checkout');
FirebaseCrashlytics.instance.log('Payment processed');
FirebaseCrashlytics.instance.log('ERROR: Payment failed');
```

---

## Configuracion por Build Mode

```dart
if (kDebugMode) {
  // Debug: deshabilitado
  await FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(false);
} else if (kProfileMode) {
  // Profile: habilitado para testing
  await FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(true);
} else {
  // Release: habilitado
  await FirebaseCrashlytics.instance.setCrashlyticsCollectionEnabled(true);
}
```

---

## Integracion con BLoC

```dart
class MyBloc extends Bloc<MyEvent, MyState> {
  final FirebaseCrashlytics _crashlytics;

  MyBloc(this._crashlytics) : super(Initial()) {
    on<MyEvent>((event, emit) async {
      try {
        emit(Loading());
        final result = await _doSomething();
        emit(Loaded(result));
      } catch (e, stack) {
        await _crashlytics.recordError(
          e, stack,
          reason: 'Error in MyBloc',
          information: ['event: ${event.runtimeType}'],
        );
        emit(Error(e.toString()));
      }
    });
  }
}
```

---

## Troubleshooting

| Problema | Solucion |
|---|---|
| No recibe errores en console | Verificar `kDebugMode` |
| dSYM no sube (iOS) | Usar `firebase crashlytics:symbols:upload` |
| Errores no symbolificados | Verificar dSYM en Firebase Console |
| Habilitado en debug | Configurar `kDebugMode` check |

---

## Metricas Clave

| Metrica | Meta | Formula |
|---|---|---|
| Crash-free sessions | > 98% | (sessions - crashes) / sessions * 100 |
| Crash-free users | > 98% | (users - affected users) / users * 100 |
| Top issues | < 5 | Issues con mas de 100 ocurrencias |
| Regresions | 0 | Issues que reaparecen |

---

## Build Commands

```bash
# Subir dSYM (iOS)
firebase crashlytics:symbols:upload --app ios-com-example-app build/ios/archive/MyApp.xcarchive/dSYMs

# Verificar Firebase
firebase projects:list

# Deploy functions
firebase deploy --only functions
```

---

## Links Utiles

- [Firebase Crashlytics](https://firebase.google.com/docs/crashlytics?hl=es-419)
- [BigQuery Export](https://firebase.google.com/docs/crashlytics/bigquery-export)
- [Alertas](https://console.firebase.google.com/project/_/crashlytics/alerts)
