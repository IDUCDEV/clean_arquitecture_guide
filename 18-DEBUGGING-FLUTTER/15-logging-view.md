# 15 — Logging View y Estrategias de Logging

> Ver logs de la app en tiempo real, filtrarlos y escribir logs útiles y estructurados.

---

## 1. ¿Qué es la Logging View?

Panel que muestra todos los logs de stdout/stderr de tu app Flutter. Útil para ver `print`, `debugPrint` y errores de consola sin usar la terminal.

---

## 2. Logging View — Pestañas

| Pestaña | Propósito |
|---|---|
| **Logs** | Lista cronológica de todos los logs |
| **Details** | Detalle del log seleccionado |
| **Filter** | Filtrar por nivel o contenido |

---

## 3. Lista de Logs

```
┌──────────┬─────────┬────────────────────────────────────┐
│ Time      │ Level   │ Message                            │
├──────────┼─────────┼────────────────────────────────────┤
│ 10:30:01 │ INFO    │ App started                        │
│ 10:30:02 │ INFO    │ User authenticated: john@mail.com  │
│ 10:30:05 │ WARNING │ Cache miss for product:123          │
│ 10:30:08 │ ERROR   │ Failed to load image: timeout      │
│ 10:30:12 │ INFO    │ Navigated to /products             │
│ 10:30:15 │ DEBUG   │ BLoC state: AuthSuccess            │
│ 10:30:18 │ ERROR   │ API Error: 500 Internal Server     │
└──────────┴─────────┴────────────────────────────────────┘
```

### 3.1 Niveles de log

| Nivel | Color | Usado para |
|---|---|---|
| **FINE** | Gris claro | Verbose debugging |
| **INFO** | Azul | Información general |
| **WARNING** | Amarillo | Advertencias |
| **SEVERE** | Rojo | Errores críticos |
| **SHOUT** | Rojo oscuro | Errores fatales |

> La vista Logging interpreta los niveles del paquete `package:logging` de Dart (`LogRecord.level`).

---

## 4. Filtrar logs

### 4.1 Filtros disponibles

| Filtro | Descripción |
|---|---|
| **Nivel mínimo** | Mostrar solo WARNING o superior, etc. |
| **Texto** | Buscar en el mensaje: `error`, `auth`, `product` |
| **Origen** | Filtrar por el logger/isolate de origen |

### 4.2 Ejemplos de uso

```
# Buscar solo errores
error

# Buscar logs del flujo de auth
auth

# Buscar logs de un tag propio
[AUTH]

# Combinar: errores de API
error api
```

---

## 5. Detalle de log

```
Log Detail:
├── Time: 10:30:08.123
├── Level: SEVERE
├── Logger: ImageLoader
├── Message: Failed to load image: Connection timeout
├── Stack Trace:
│   ├── #0 ImageLoader.load (image_loader.dart:45)
│   ├── #1 CachedNetworkImageProvider._loadAsync (cached_network_image.dart:234)
│   ├── #2 ImageStreamCompleter._handleImageLoad (image_stream.dart:156)
│   └── ...
└── Error: SocketException: Connection timed out
```

---

## 6. Logging desde código

### 6.1 `print()` y `debugPrint()`

```dart
// Básico
print('User logged in: $email');

// Con debugPrint (mejor para Flutter: hace throttling en modo debug)
debugPrint('Widget rebuild: ${runtimeType}');
debugPrint('State changed: $newState');
```

### 6.2 Logger package (recomendado)

```dart
import 'package:logger/logger.dart';

final logger = Logger(
  printer: PrettyPrinter(
    methodCount: 2,
    errorMethodCount: 5,
    lineLength: 50,
    colors: true,
    printEmojis: true,
  ),
);

// Uso
logger.d('Debug message');      // 🐛 Debug message
logger.i('Info message');       // 💡 Info message
logger.w('Warning message');    // ⚠️ Warning message
logger.e('Error message');      // ❌ Error message
```

### 6.3 Logging estructurado con tags

```dart
// Con tags para filtrar
logger.d('[AUTH] User logged in: $email');
logger.d('[API] GET /products - Status: 200');
logger.d('[BLOC] State changed: AuthSuccess');
logger.e('[ERROR] Failed to load data: $error');

// En Logging View, filtrar por tag:
// message:AUTH
// message:API
// message:BLOC
```

### 6.4 Logging condicional

```dart
// Solo en debug mode
if (kDebugMode) {
  debugPrint('[DEBUG] Widget tree rebuilt');
  debugPrint('[DEBUG] API response: ${response.body}');
}

// Con nivel de logging configurable
enum LogLevel { debug, info, warning, error }

class AppConfig {
  static const LogLevel logLevel = kDebugMode
      ? LogLevel.debug
      : LogLevel.warning;
}

void log(String tag, String message, LogLevel level) {
  if (level.index >= AppConfig.logLevel.index) {
    debugPrint('[$tag] $message');
  }
}
```

---

## 7. Tips de logging

### 7.1 Usar tags consistentes

```dart
// Tags para cada feature
debugPrint('[AUTH] Login attempt');
debugPrint('[PRODUCTS] Loading products');
debugPrint('[CART] Item added');

// Tags para cada capa
debugPrint('[DATASOURCE] API call');
debugPrint('[REPOSITORY] Cache hit');
debugPrint('[BLOC] State emitted');
```

### 7.2 Loggear errores con contexto

```dart
// ❌ Mal
print('Error');

// ✅ Bien
print('Error loading products: $error');
print('Stack trace: $stackTrace');
print('User: ${currentUser?.id}');
print('URL: $apiUrl');
```

### 7.3 Loggear timing

```dart
final stopwatch = Stopwatch()..start();
final products = await repository.getProducts();
stopwatch.stop();
debugPrint('[PERF] getProducts: ${stopwatch.elapsedMilliseconds}ms');
```

### 7.4 Loggear el estado del BLoC

```dart
// En el BLoC
on<LoadProducts>((event, emit) async {
  debugPrint('[BLOC] LoadProducts event received');
  emit(ProductsLoading());
  try {
    final products = await getProducts();
    debugPrint('[BLOC] Products loaded: ${products.length} items');
    emit(ProductsLoaded(products));
  } catch (e) {
    debugPrint('[BLOC] Error loading products: $e');
    emit(ProductsError(e.toString()));
  }
});
```

---

## 8. Ejercicios prácticos

### 8.1 Ejercicio 1: logging de flujo completo

1. Implementar login completo con logging
2. Loggear cada paso: attempt, success, failure
3. Ver los logs en Logging View
4. Filtrar por tag `[AUTH]`

### 8.2 Ejercicio 2: logging de performance

1. Loggear el tiempo de cada llamada API
2. Loggear el tiempo de construcción de widgets
3. Identificar operaciones lentas vía logs

---

## Resumen

| Concepto | Punto clave |
|---|---|
| Logging View | stdout/stderr en tiempo real |
| Niveles | FINE, INFO, WARNING, SEVERE, SHOUT |
| Tags | `[AUTH]`, `[API]`, `[BLOC]` para filtrar |
| `debugPrint` | Throttling automático en debug |
| Buen logging | Contexto: error + stack + usuario + URL |

---

## 📚 Referencias

- [Flutter | Logging view](https://docs.flutter.dev/tools/devtools/logging) — Documentación oficial de la Logging view
- [pub.dev | logger](https://pub.dev/packages/logger) — Paquete de logging popular para Flutter
- [Dart | package:logging](https://pub.dev/packages/logging) — Logging estándar de Dart

---

> 📖 **Siguiente:** [16-app-size.md](./16-app-size.md) — App Size: analizando el tamaño del bundle
