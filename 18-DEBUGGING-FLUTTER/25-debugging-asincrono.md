# 25 — Debugging Asíncrono en Dart/Flutter

> El 80% de bugs difíciles en Flutter son problemas asíncronos. Futures que nunca completan, streams que pierden datos, microtasks que bloquean el UI thread.

---

## 1. Por qué es tan difícil

```dart
// Este código parece correcto pero tiene 3 bugs ocultos
Future<void> loadData() async {
  final user = await fetchUser();         // Bug 1: no maneja error
  final posts = await fetchPosts(user.id); // Bug 2: secuencial innecesariamente
  setState(() {
    _user = user;      // Bug 3: setState después de await sin mounted check
    _posts = posts;
  });
}
```

---

## 2. Los 5 bugs asíncronos más comunes

### 2.1 Future que nunca completa

```dart
// ❌ BUG: Si fetch falla, el loading queda para siempre
Future<void> load() async {
  setState(() => _loading = true);
  final data = await fetch(); // Si lanza excepción...
  setState(() {
    _data = data;
    _loading = false; // ← Nunca se ejecuta
  });
}

// ✅ CORRECTO
Future<void> load() async {
  setState(() => _loading = true);
  try {
    final data = await fetch();
    setState(() {
      _data = data;
      _loading = false;
    });
  } catch (e) {
    setState(() {
      _error = e.toString();
      _loading = false;
    });
  }
}
```

### 2.2 setState sin mounted check

```dart
// ❌ BUG: Widget desmontado mientras awaited
Future<void> load() async {
  final data = await fetch(); // 2 segundos
  setState(() { _data = data; }); // Widget puede no existir
}

// ✅ CORRECTO
Future<void> load() async {
  final data = await fetch();
  if (!mounted) return; // ← Verificar
  setState(() { _data = data; });
}
```

### 2.3 Llamadas secuenciales innecesarias

```dart
// ❌ LENTO: Espera 4 segundos (2+2)
Future<void> loadAll() async {
  final users = await fetchUsers();   // 2 seg
  final posts = await fetchPosts();   // 2 seg (espera a que termine users)
}

// ✅ RÁPIDO: Espera 2 segundos (paralelo)
Future<void> loadAll() async {
  final results = await Future.wait([
    fetchUsers(),
    fetchPosts(),
  ]);
  final users = results[0];
  final posts = results[1];
}
```

### 2.4 Stream que se suscribe mal

```dart
// ❌ BUG: Suscripción que nunca se cancela (memory leak)
void initState() {
  super.initState();
  _supabase.from('posts').stream(primaryKey: ['id']).listen((data) {
    setState(() => _posts = data);
  });
}

// ✅ CORRECTO
late final StreamSubscription _subscription;

@override
void initState() {
  super.initState();
  _subscription = _supabase
      .from('posts')
      .stream(primaryKey: ['id'])
      .listen((data) {
    if (mounted) setState(() => _posts = data);
  });
}

@override
void dispose() {
  _subscription.cancel(); // ← SIEMPRE cancelar
  super.dispose();
}
```

### 2.5 Completer manual innecesario

```dart
// ❌ COMPLEJIDAD INNECESARIA
final completer = Completer<String>();
fetch().then((v) => completer.complete(v)).catchError((e) => completer.completeError(e));
final result = await completer.future;

// ✅ SIMPLE
final result = await fetch();
```

---

## 3. Patrón de carga segura

```dart
mixin SafeLoad<T> {
  bool _loading = false;
  String? _error;
  T? _data;

  bool get loading => _loading;
  String? get error => _error;
  T? get data => _data;

  Future<T> loadSafely(Future<T> Function() loader) async {
    _loading = true;
    _error = null;
    try {
      _data = await loader();
      _loading = false;
      return _data!;
    } catch (e) {
      _error = e.toString();
      _loading = false;
      rethrow;
    }
  }
}
```

---

## 4. Debugging de Futures

### 4.1 Prints de debug

```dart
Future<T> debugFuture<T>(String name, Future<T> Function() fn) async {
  print('⏳ [$name] Iniciando...');
  final sw = Stopwatch()..start();
  try {
    final result = await fn();
    print('✅ [$name] Completado en ${sw.elapsedMilliseconds}ms');
    return result;
  } catch (e) {
    print('❌ [$name] Error: $e');
    rethrow;
  }
}

// Uso
final user = await debugFuture('fetchUser', () => fetchUser());
```

### 4.2 Timeout

```dart
// Nunca dejes un Future sin timeout en producción
final data = await fetch().timeout(
  Duration(seconds: 10),
  onTimeout: () => throw TimeoutException('Fetch tardó más de 10s'),
);
```

---

## 5. Debugging de Streams

### 5.1 Inspeccionar eventos

```dart
// Envuelve el stream para ver cada evento
Stream<T> debugStream<T>(String name, Stream<T> stream) {
  return stream.transform(
    StreamTransformer.fromHandlers(
      handleData: (data, sink) {
        print('📦 [$name] evento: $data');
        sink.add(data);
      },
      handleError: (error, stack, sink) {
        print('❌ [$name] error: $error');
        sink.addError(error, stack);
      },
      handleDone: (sink) {
        print('🏁 [$name] stream cerrado');
        sink.close();
      },
    ),
  );
}

// Uso
final posts = debugStream('posts', _supabase.from('posts').stream(primaryKey: ['id']));
```

### 5.2 Detectar streams que nunca emiten

```dart
// Timeout sobre la primera emisión
final firstPost = await posts
    .first
    .timeout(
      const Duration(seconds: 5),
      onTimeout: () => throw TimeoutException('El stream no emitió en 5s'),
    );
```

---

## 6. Debugging de microtasks y event loop

### 6.1 Cuándo se ejecuta tu código

```dart
void debugEventLoop() {
  print('1: síncrono');

  Future(() => print('2: microtask'));  // Microtask

  Future.delayed(Duration.zero, () {
    print('3: event loop (timer)');
  });

  Future.microtask(() => print('4: microtask explícita'));

  print('5: síncrono (último)');
}

// Orden de salida:
// 1: síncrono
// 5: síncrono (último)
// 2: microtask
// 4: microtask explícita
// 3: event loop (timer)
```

### 6.2 UI bloqueada por trabajo pesado síncrono

```dart
// ❌ BLOQUEA el UI thread: el frame no se renderiza
void onPressed() {
  final bigList = List.generate(10_000_000, (i) => i);
  final sum = bigList.reduce((a, b) => a + b);  // CPU bloqueada aquí
}

// ✅ Delegar a un isolate
void onPressed() async {
  final sum = await compute(_computeSum, 10_000_000);
}

int _computeSum(int n) {
  var total = 0;
  for (var i = 0; i < n; i++) {
    total += i;
  }
  return total;
}
```

---

## 7. Checklist asíncrono

```
□ ¿Todos los await tienen try/catch?
□ ¿Hay mounted check después de cada await en widgets?
□ ¿Las llamadas independientes usan Future.wait?
□ ¿Los streams se cancelan en dispose?
□ ¿Hay timeout en llamadas de red?
□ ¿Completer es realmente necesario? (probablemente no)
□ ¿El trabajo pesado usa compute() o isolates?
```

---

## Resumen

| Problema | Síntoma | Solución |
|---|---|---|
| Future nunca completa | Loading infinito | `try/catch` + manejo de error |
| setState tras desmontar | Crash de framework | `if (!mounted) return` |
| Llamadas secuenciales | App lenta | `Future.wait` |
| Stream sin cancelar | Memory leak | `dispose()` + `cancel()` |
| Completer manual | Código complejo | Usar `await` directo |
| UI bloqueada | Jank al hacer scroll | `compute()` / isolates |

---

## 📚 Referencias

- [dart:async | Future API](https://api.dart.dev/dart-async/Future-class.html) — Futures y async/await
- [dart:async | Stream API](https://api.dart.dev/dart-async/Stream-class.html) — Streams y suscripciones
- [Dart | Asynchronous programming](https://dart.dev/language/async) — Guía de programación asíncrona
- [Dart | Event loop y microtasks](https://dart.dev/articles/archive/event-loop) — Cómo funciona el loop de eventos

---

> 📖 **Siguiente:** [26-workflow-debugging-por-tipo.md](./26-workflow-debugging-por-tipo.md) — Workflow de debugging según el tipo de problema
