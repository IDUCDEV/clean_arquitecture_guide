# 09 - Practicas Sentry

## Ejercicios Practicos

### Ejercicio 1: Performance de Login

**Objetivo**: Medir el tiempo de autenticacion.

**Escenario**: Un usuario intenta hacer login y queremos medir el rendimiento.

**Codigo**:

```dart
// lib/features/auth/presentation/bloc/auth_bloc.dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUseCase loginUseCase;
  final FirebaseCrashlytics _crashlytics;

  AuthBloc({
    required this.loginUseCase,
    required FirebaseCrashlytics crashlytics,
  })  : _crashlytics = crashlytics,
        super(AuthInitial()) {
    on<LoginRequested>(_onLoginRequested);
  }

  Future<void> _onLoginRequested(
    LoginRequested event,
    Emitter<AuthState> emit,
  ) async {
    final transaction = await Sentry.startTransaction(
      'login',
      'auth',
      bindToScope: true,
    );

    try {
      emit(AuthLoading());
      
      // Span: Validate credentials
      final validationSpan = transaction.startChild(
        'auth.validate',
        description: 'Validate credentials format',
      );
      
      _validateCredentials(event.email, event.password);
      validationSpan.status = SpanStatus.ok();
      await validationSpan.finish();
      
      // Span: API call
      final apiSpan = transaction.startChild(
        'auth.api',
        description: 'POST /auth/login',
      );
      
      final user = await loginUseCase(
        email: event.email,
        password: event.password,
      );
      
      apiSpan.setData('user_id', user.id);
      apiSpan.status = SpanStatus.ok();
      await apiSpan.finish();
      
      // Span: Update scope
      final scopeSpan = transaction.startChild(
        'auth.scope',
        description: 'Update Sentry scope',
      );
      
      await Sentry.configureScope((scope) {
        scope.setUser(SentryUser(
          id: user.id,
          email: user.email,
        ));
        scope.setTag('user_plan', user.plan);
      });
      
      scopeSpan.status = SpanStatus.ok();
      await scopeSpan.finish();
      
      transaction.setData('user_id', user.id);
      transaction.status = SpanStatus.ok();
      
      emit(AuthAuthenticated(user));
    } catch (e) {
      transaction.status = SpanStatus.internalError();
      emit(AuthError('Error al iniciar sesion'));
    } finally {
      await transaction.finish();
    }
  }

  void _validateCredentials(String email, String password) {
    if (!email.contains('@')) {
      throw ArgumentError('Invalid email');
    }
    if (password.length < 8) {
      throw ArgumentError('Password too short');
    }
  }
}
```

**Verificacion**:
1. Ir a Sentry → Performance
2. Verificar que la transaccion "login" aparece
3. Verificar los spans (validate, api, scope)
4. Verificar tiempos de ejecucion

---

### Ejercicio 2: HTTP Request Lento

**Objetivo**: Identificar API lenta.

**Escenario**: Un request HTTP tarda demasiado en responder.

**Codigo**:

```dart
// lib/core/network/http_client.dart
import 'package:http/http.dart' as http;
import 'package:sentry_flutter/sentry_flutter.dart';

class ApiClient {
  final http.Client _client = http.Client();

  Future<Map<String, dynamic>> get(String endpoint) async {
    final transaction = Sentry.currentHub.startTransaction(
      'GET $endpoint',
      'http.client',
      bindToScope: true,
    );

    try {
      transaction.setData('endpoint', endpoint);
      transaction.setData('method', 'GET');
      
      final response = await _client.get(
        Uri.parse('https://api.example.com$endpoint'),
      ).timeout(
        Duration(seconds: 10),
        onTimeout: () {
          throw TimeoutException('Request timed out');
        },
      );
      
      transaction.setData('status_code', response.statusCode);
      transaction.setData('response_size', response.body.length);
      
      if (response.statusCode >= 400) {
        transaction.status = SpanStatus.internalError();
        await Sentry.captureMessage(
          'HTTP error: ${response.statusCode}',
          level: SentryLevel.warning,
          hint: Hint.withMap({
            'endpoint': endpoint,
            'status_code': response.statusCode,
          }),
        );
      } else {
        transaction.status = SpanStatus.ok();
      }
      
      return jsonDecode(response.body);
    } on TimeoutException catch (e, stack) {
      transaction.status = SpanStatus.deadlineExceeded();
      
      await Sentry.captureException(
        e,
        stackTrace: stack,
        hint: Hint.withMap({
          'endpoint': endpoint,
          'timeout': '10s',
        }),
      );
      
      rethrow;
    } catch (e, stack) {
      transaction.status = SpanStatus.internalError();
      
      await Sentry.captureException(
        e,
        stackTrace: stack,
        hint: Hint.withMap({
          'endpoint': endpoint,
        }),
      );
      
      rethrow;
    } finally {
      await transaction.finish();
    }
  }
}
```

**Verificacion**:
1. Simular slow network
2. Ir a Sentry → Performance
3. Verificar requests lentos
4. Verificar timeouts

---

### Ejercicio 3: Session Replay de Bug

**Objetivo**: Reproducir un bug reportado.

**Escenario**: Un usuario reporta un bug y queremos ver que vio.

**Codigo**:

```dart
// lib/main.dart
await SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    
    // Session Replay
    options.replay.sessionSampleRate = 1.0; // En debug, grabar todo
    options.replay.onErrorSampleRate = 1.0;
    options.replay.maskAllText = false; // En debug, no enmascarar
    options.replay.maskAllImages = false;
  },
  appRunner: () => runApp(
    SentryWidget(child: MyApp()),
  ),
);

// En la pantalla con el bug
class BuggyScreen extends StatefulWidget {
  @override
  _BuggyScreenState createState() => _BuggyScreenState();
}

class _BuggyScreenState extends State<BuggyScreen> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
    
    // Simular bug
    if (_counter == 5) {
      throw Exception('Bug at counter 5!');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Buggy Screen')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Counter: $_counter'),
            ElevatedButton(
              onPressed: _incrementCounter,
              child: Text('Increment'),
            ),
          ],
        ),
      ),
    );
  }
}
```

**Verificacion**:
1. Ejecutar la app
2. Tocar "Increment" 5 veces
3. Ir a Sentry → Replays
4. Ver el replay del usuario
5. Ver que el usuario toco el boton 5 veces

---

### Ejercicio 4: Jira Ticket Automatico

**Objetivo**: Crear ticket en Jira automaticamente.

**Escenario**: Un error critico crea un ticket en Jira.

**Codigo**:

```dart
// lib/core/monitoring/sentry_service.dart
class SentryService {
  final FirebaseCrashlytics _crashlytics;

  SentryService(this._crashlytics);

  Future<void> reportCriticalError(
    dynamic error,
    StackTrace stack, {
    required String context,
    required String severity,
  }) async {
    // Reportar a Sentry con contexto para Jira
    await Sentry.captureException(
      error,
      stackTrace: stack,
      hint: Hint.withMap({
        'context': context,
        'severity': severity,
        'jira_project': 'MOBILE',
        'jira_issue_type': 'Bug',
        'jira_priority': severity == 'critical' ? 'Highest' : 'High',
        'jira_labels': ['flutter', 'production', severity],
        'create_jira_issue': true,
      }),
    );

    // Reportar a Crashlytics
    await _crashlytics.recordError(
      error,
      stack,
      reason: context,
    );
  }
}

// Uso
class PaymentService {
  final SentryService _sentryService;

  PaymentService(this._sentryService);

  Future<void> processPayment(PaymentRequest request) async {
    try {
      await _paymentGateway.charge(request);
    } catch (e, stack) {
      await _sentryService.reportCriticalError(
        e,
        stack,
        context: 'Payment processing failed',
        severity: 'critical',
      );
      rethrow;
    }
  }
}
```

**Verificacion**:
1. Forzar error en pago
2. Ir a Jira
3. Verificar que se creo el ticket
4. Verificar que tiene el stack trace
5. Verificar que tiene link a Sentry

---

### Ejercicio 5: Release Health

**Objetivo**: Comparar estabilidad entre versiones.

**Escenario**: Dos versiones de la app con diferentes crash rates.

**Codigo**:

```dart
// lib/main.dart
import 'package:flutter/foundation.dart';
import 'package:sentry_flutter/sentry_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await SentryFlutter.init(
    (options) {
      options.dsn = 'your-dsn';
      
      // Release info
      options.release = kDebugMode ? '1.0.0-dev' : '1.0.0';
      options.environment = kDebugMode ? 'development' : 'production';
      
      // Performance
      options.tracesSampleRate = 1.0;
    },
    appRunner: () => runApp(MyApp()),
  );

  // Configurar scope
  await Sentry.configureScope((scope) {
    scope.setTag('release', options.release!);
    scope.setTag('environment', options.environment!);
  });
}

// En tu pipeline de CI/CD
class ReleaseManager {
  final SentryApi _api;

  ReleaseManager(this._api);

  Future<void> createRelease(String version) async {
    // Crear release en Sentry
    await _api.createRelease(version);
    
    // Finalizar release
    await _api.finalizeRelease(version);
  }

  Future<Map<String, dynamic>> compareReleases(
    String version1,
    String version2,
  ) async {
    final metrics1 = await _api.getReleaseMetrics(version1);
    final metrics2 = await _api.getReleaseMetrics(version2);

    return {
      'version1': {
        'crash_free_rate': metrics1.crashFreeRate,
        'error_count': metrics1.errorCount,
      },
      'version2': {
        'crash_free_rate': metrics2.crashFreeRate,
        'error_count': metrics2.errorCount,
      },
      'diff': {
        'crash_free_rate': metrics2.crashFreeRate - metrics1.crashFreeRate,
        'error_count': metrics2.errorCount - metrics1.errorCount,
      },
    };
  }
}
```

**Verificacion**:
1. Desplegar version 1.0.0
2. Desplegar version 1.0.1 con fix
3. Ir a Sentry → Releases
4. Comparar metricas
5. Verificar que el crash rate bajo

---

### Ejercicio 6: Memory Leak Detection

**Objetivo**: Detectar memory leaks.

**Escenario**: La app tiene un memory leak que causa crashes.

**Codigo**:

```dart
// lib/core/monitoring/memory_monitor.dart
class MemoryMonitor {
  final SentryApi _api;
  Timer? _timer;

  MemoryMonitor(this._api);

  void startMonitoring() {
    _timer = Timer.periodic(
      Duration(seconds: 30),
      (_) => _checkMemory(),
    );
  }

  void stopMonitoring() {
    _timer?.cancel();
  }

  void _checkMemory() async {
    // Obtener uso de memoria
    final memoryInfo = await _getMemoryInfo();
    
    // Enviar a Sentry
    Sentry.addBreadcrumb(Breadcrumb(
      message: 'Memory usage check',
      category: 'system',
      data: {
        'used_mb': memoryInfo.usedMb,
        'total_mb': memoryInfo.totalMb,
        'usage_percentage': memoryInfo.usagePercentage,
      },
    ));

    // Alertar si uso alto
    if (memoryInfo.usagePercentage > 80) {
      await Sentry.captureMessage(
        'High memory usage detected',
        level: SentryLevel.warning,
        hint: Hint.withMap({
          'used_mb': memoryInfo.usedMb,
          'total_mb': memoryInfo.totalMb,
          'usage_percentage': memoryInfo.usagePercentage,
        }),
      );
    }
  }

  Future<MemoryInfo> _getMemoryInfo() async {
    // Implementar segun plataforma
    return MemoryInfo(
      usedMb: 150,
      totalMb: 512,
      usagePercentage: 29.3,
    );
  }
}
```

**Verificacion**:
1. Ejecutar la app
2. Navegar entre pantallas
3. Ir a Sentry → Performance
4. Verificar breadcrumbs de memoria
5. Verificar alerts si uso alto

---

## Ejercicio Integrador: Dashboard de Monitoreo

**Objetivo**: Crear un dashboard completo de monitoreo.

### Componentes a implementar

1. **Error monitoring** con contexto
2. **Performance tracing** end-to-end
3. **Session replay** configurado
4. **Integracion Jira/GitHub**
5. **Release health** tracking

### Codigo base

```dart
// lib/core/monitoring/monitoring_service.dart
class MonitoringService {
  final FirebaseCrashlytics _crashlytics;
  final SentryService _sentryService;

  MonitoringService({
    required FirebaseCrashlytics crashlytics,
    required SentryService sentryService,
  })  : _crashlytics = crashlytics,
        _sentryService = sentryService;

  // Error reporting
  Future<void> reportError(
    dynamic error,
    StackTrace stack, {
    required String context,
    required String severity,
    Map<String, dynamic>? additionalInfo,
  }) async {
    // Reportar a ambos
    await _sentryService.reportError(
      error,
      stack,
      context: context,
      severity: severity,
      additionalInfo: additionalInfo,
    );

    await _crashlytics.recordError(
      error,
      stack,
      reason: context,
      information: additionalInfo?.entries
          .map((e) => '${e.key}: ${e.value}')
          .toList(),
    );
  }

  // Performance tracking
  Future<T> trackPerformance<T>(
    String name,
    String operation,
    Future<T> Function() task,
  ) async {
    final transaction = await Sentry.startTransaction(
      name,
      operation,
      bindToScope: true,
    );

    try {
      final result = await task();
      transaction.status = SpanStatus.ok();
      return result;
    } catch (e) {
      transaction.status = SpanStatus.internalError();
      rethrow;
    } finally {
      await transaction.finish();
    }
  }

  // User context
  Future<void> setUser(User user) async {
    await Sentry.configureScope((scope) {
      scope.setUser(SentryUser(
        id: user.id,
        email: user.email,
        username: user.name,
      ));
      scope.setTag('user_plan', user.plan);
    });

    await _crashlytics.setUserIdentifier(user.id);
    await _crashlytics.setCustomKey('user_plan', user.plan);
  }
}
```

### Verificacion final

1. Ejecutar la app en release
2. Realizar flujo completo (login → products → cart → checkout)
3. Forzar errores en cada paso
4. Verificar en Sentry que los errores aparecen con contexto
5. Verificar en Crashlytics que los errores aparecen
6. Verificar que se crean tickets en Jira
7. Verificar session replay
8. Verificar release health

---

## Siguiente paso

[Comparacion Crashlytics vs Sentry](../03-comparacion-migracion/01-crashlytics-vs-sentry.md)
