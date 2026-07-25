# 04: Debugging Asíncrono en Dart/Flutter

> El 80% de bugs difíciles en Flutter son problemas asíncronos. Futures que nunca completan, streams que pierden datos, microtasks que bloquean el UI thread.

---

## Por qué es tan difícil

```dart
// Este código parece correcto pero tiene 3 bugs ocultos
Future<void> loadData() async {
  final user = await fetchUser();      // Bug 1: no maneja error
  final posts = await fetchPosts(user.id); // Bug 2: secuencial innecesariamente
  setState(() {
    _user = user;      // Bug 3: setState después de await sin mounted check
    _posts = posts;
  });
}
```

---

## Los 5 bugs asíncronos más comunes

### 1. Future que nunca completa

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

---

### 2. setState sin mounted check

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

---

### 3. Llamadas secuenciales innecesarias

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

---

### 4. Stream que se suscribe mal

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

---

### 5. Completer manual innecesario

```dart
// ❌ COMPLEJIDAD INNECESARIA
final completer = Completer<String>();
fetch().then((v) => completer.complete(v)).catchError((e) => completer.completeError(e));
final result = await completer.future;

// ✅ SIMPLE
final result = await fetch();
```

---

## Patrón de carga segura

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

## Debugging de Futures

### Prints de debug

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

### Timeout

```dart
// Nunca dejes un Future sin timeout en producción
final data = await fetch().timeout(
  Duration(seconds: 10),
  onTimeout: () => throw TimeoutException('Fetch tardó más de 10s'),
);
```

---

## Checklist asíncrono

```
□ ¿Todos los await tienen try/catch?
□ ¿Hay mounted check después de cada await en widgets?
□ ¿Las llamadas independientes usan Future.wait?
□ ¿Los streams se cancelan en dispose?
□ ¿Hay timeout en llamadas de red?
□ ¿Completer es realmente necesario? (probablemente no)
```

---

**Siguiente:** [05-workflow-debugging-por-tipo.md](./05-workflow-debugging-por-tipo.md)
