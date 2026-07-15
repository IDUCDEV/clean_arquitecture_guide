# 08 - Logging View

## ¿Qué es Logging View?

Panel que muestra todos los logs de stdout/stderr de tu app Flutter. Útil para ver print statements, debugPrint, y errores de consola sin usar terminal.

---

## Logging View - Pestañas

| Pestaña | Propósito |
|---------|-----------|
| **Logs** | Lista cronológica de todos los logs |
| **Details** | Detalle del log seleccionado |
| **Filter** | Filtrar por nivel o contenido |

---

## Lista de Logs

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

### Niveles de log

| Nivel | Color | Usado para |
|-------|-------|------------|
| **FINE** | Gris claro | Verbose debugging |
| **INFO** | Azul | Información general |
| **WARNING** | Amarillo | Advertencias |
| **SEVERE** | Rojo | Errores críticos |
| **SHOUT** | Rojo oscuro | Errores fatales |

---

## Filtrar logs

### Filtros disponibles

| Filtro | Descripción | Ejemplo |
|--------|-------------|---------|
| **Level** | Filtrar por nivel | `WARNING` o superior |
| **Text** | Buscar en mensaje | `error`, `auth`, `product` |
| **Tag** | Filtrar por tag | `flutter`, `supabase` |

### Sintaxis de filtro

```
# Nivel mínimo
level:WARNING

# Buscar texto
message:auth

# Combinar
level:ERROR message:api

# Excluir
-level:FINE
```

---

## Detalle de log

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

## Logging desde código

### print() y debugPrint()

```dart
// Básico
print('User logged in: $email');

// Con debugPrint (mejor para Flutter, hace throttling)
debugPrint('Widget rebuild: ${runtimeType}');
debugPrint('State changed: $newState');
```

### Logger package (recomendado)

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

### Logging estructurado

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

### Logging condicional

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

## Tips de logging

### 1. Usar tags consistentes
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

### 2. Loggear errores con contexto
```dart
// ❌ Mal
print('Error');

// ✅ Bien
print('Error loading products: $error');
print('Stack trace: $stackTrace');
print('User: ${currentUser?.id}');
print('URL: $apiUrl');
```

### 3. Loggear timing
```dart
final stopwatch = Stopwatch()..start();
final products = await repository.getProducts();
stopwatch.stop();
debugPrint('[PERF] getProducts: ${stopwatch.elapsedMilliseconds}ms');
```

### 4. Loggear estado de BLoC
```dart
// En BLoC
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

## Ejercicios prácticos

### Ejercicio 1: Logging de flujo completo

1. Implementar login completo con logging
2. Loggear cada paso: attempt, success, failure
3. Ver logs en Logging View
4. Filtrar por tag `[AUTH]`

### Ejercicio 2: Logging de performance

1. Loggear tiempo de cada llamada API
2. Loggear tiempo de construcción de widgets
3. Identificar operaciones lentas via logs

---
→ Siguiente: `09-app-size.md`
