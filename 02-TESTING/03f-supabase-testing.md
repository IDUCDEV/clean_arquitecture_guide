# 🧪 03f: Testing de Remote DataSources con Supabase

> **¿De qué trata esta parte?** De entender los desafíos específicos de testear DataSources que usan Supabase, las estrategias de mocking disponibles, y por qué el patrón Mocktail + Fakes es la opción más usada en producción.

---

## 📋 Índice

1. [¿Por qué Supabase es diferente?](#1-por-qué-supabase-es-diferente)
2. [La cadena de builders de Supabase](#2-la-cadena-de-builders-de-supabase)
3. [Estrategias de mocking](#3-estrategias-de-mocking)
4. [El patrón Fake para Supabase](#4-el-patrón-fake-para-supabase)
5. [Jerarquía de Mocks](#5-jerarquía-de-mocks)
6. [registerFallbackValue](#6-registerfallbackvalue)
7. [Manejo de errores](#7-manejo-de-errores)
8. [Checklist](#8-checklist)

---

## 1. ¿Por qué Supabase es diferente?

### 🔍 El problema

Cuando testeas un Remote DataSource con HTTP (`http.Client`), el patrón es simple:

```dart
when(() => mockClient.post(any(), headers: any(named: 'headers'), body: any(named: 'body')))
    .thenAnswer((_) async => http.Response(json.encode(data), 200));
```

El `http.Client` devuelve `Future<http.Response>` directamente — Mocktail puede interceptarlo sin problemas.

Con Supabase, la cosa cambia. El DataSource no llama a un solo método, sino que **encadena builders**:

```dart
await supabase
    .from('profiles')           // → SupabaseQueryBuilder
    .select()                   // → PostgrestFilterBuilder<List<Map<String, dynamic>>>
    .eq('user_id', userId)      // → PostgrestFilterBuilder<List<Map<String, dynamic>>>
    .single();                  // → PostgrestTransformBuilder<Map<String, dynamic>>
```

Cada paso retorna un tipo distinto, y el último es un `PostgrestTransformBuilder` que **implementa `Future<T>`**.

### 🧠 El núcleo del desafío

```dart
// Esto es lo que hace Dart cuando haces await:
final result = await builder.single();
// Dart llama internamente a: builder.single().then((data) => ...)
```

`PostgrestTransformBuilder` implementa `Future<T>`, por lo que `await` llama al método `.then()` heredado de `Future`. **Mocktail no puede interceptar `.then()`** porque no es un método declarado en la interfaz pública del builder — es parte del contrato de `Future`.

Por eso, un simple `Mock` no funciona. Necesitamos **Fakes** que sobreescriban `then()` para devolver el valor que queremos.

---

## 2. La cadena de builders de Supabase

### 📊 Diagrama completo

```
SupabaseClient
  │
  ├── .auth → GoTrueClient
  │     ├── .signInWithPassword()     → Future<AuthResponse>
  │     ├── .signUp()                 → Future<AuthResponse>
  │     ├── .signOut()                → Future<void>
  │     ├── .updateUser()             → Future<UserResponse>
  │     ├── .resetPasswordForEmail()  → Future<void>
  │     ├── .verifyOTP()              → Future<AuthResponse>
  │     └── .currentUser              → User? (getter síncrono)
  │
  ├── .from('table') → SupabaseQueryBuilder
  │     ├── .select()     → PostgrestFilterBuilder<List<Map<String, dynamic>>>
  │     ├── .insert()     → PostgrestFilterBuilder<List<Map<String, dynamic>>>
  │     ├── .update()     → PostgrestFilterBuilder<List<Map<String, dynamic>>>
  │     └── .delete()     → PostgrestFilterBuilder<List<Map<String, dynamic>>>
  │           │
  │           └── .eq() / .neq() / .or() / etc.
  │                 → PostgrestFilterBuilder<List<Map<String, dynamic>>>
  │                      │
  │                      ├── .single()      → PostgrestTransformBuilder<Map<String, dynamic>>
  │                      │                       └── implementa Future<Map<String, dynamic>>
  │                      │
  │                      ├── .maybeSingle() → PostgrestTransformBuilder<Map<String, dynamic>?>
  │                      │                       └── implementa Future<Map<String, dynamic>?>
  │                      │
  │                      └── (bare await)   → Future<List<Map<String, dynamic>>>
  │                                             (se llama a .then() del FilterBuilder)
  │
  └── .storage → SupabaseStorageClient
        └── .from('bucket') → StorageFileApi
              ├── .uploadBinary()  → Future<String>
              ├── .getPublicUrl()  → String (síncrono)
              └── .remove()        → Future<List<Map<String, dynamic>>>
```

### 🔑 Puntos clave

| Componente | Retorna | ¿Se puede mockear con Mocktail puro? |
|------------|---------|--------------------------------------|
| `GoTrueClient.*` | `Future<T>` directo | ✅ Sí |
| `SupabaseQueryBuilder.*` | `PostgrestFilterBuilder` | ✅ Sí (con `thenAnswer`) |
| `PostgrestFilterBuilder.eq()` | mismo `PostgrestFilterBuilder` | ✅ Sí (con `thenAnswer`) |
| `PostgrestFilterBuilder.single()` | `PostgrestTransformBuilder` (que es `Future`) | ❌ Requiere Fake |
| `PostgrestFilterBuilder.maybeSingle()` | `PostgrestTransformBuilder` nullable | ❌ Requiere Fake |
| `PostgrestFilterBuilder` (await directo) | `Future<List<...>>` vía `.then()` | ❌ Requiere Fake |
| `StorageFileApi.*` | `Future<T>` directo | ✅ Sí |

> **Regla de oro:** Si el método retorna algo que al hacer `await` llama a `.then()` del builder, necesitas un Fake. Si retorna un `Future<T>` de un cliente "normal" (GoTrueClient, StorageFileApi), Mocktail puro funciona.

---

## 3. Estrategias de mocking

Existen 3 enfoques principales para testear DataSources con Supabase. Cada uno tiene sus ventajas y casos de uso ideales.

### 📊 Comparativa

| Aspecto | Mocktail + Fakes | mock_supabase_http_client | Fake manual |
|---------|-----------------|--------------------------|-------------|
| **Dependencias** | `mocktail` | `mock_supabase_http_client` | Ninguna |
| **Setup** | Medio (crear Fakes una vez) | Mínimo (inyectar HTTP client) | Alto (implementar toda la interfaz) |
| **Velocidad** | Máxima | Media (pasa por HTTP simulado) | Máxima |
| **`verify()` preciso** | ✅ Sí (método y args exactos) | ❌ No (solo asserts en datos) | ⚠️ Manual |
| **Simula RLS/restricciones** | ❌ No | ✅ Sí (vía callback) | ⚠️ Manual |
| **Auth testing** | ✅ Mock directo | ❌ No soportado | ⚠️ Manual |
| **Storage testing** | ✅ Mock directo | ❌ No soportado | ⚠️ Manual |
| **Mantenimiento** | Bajo (Fakes reutilizables) | Bajo | Alto |
| **Ideal para** | Tests unitarios puros | Tests de integración ligeros | Proyectos pequeños |

### 🏆 Recomendación

Para **tests unitarios de DataSources** en Clean Architecture, el enfoque **Mocktail + Fakes** es el más usado porque:

1. Es el más rápido de ejecutar
2. Permite `verify()` preciso sobre qué tabla y con qué parámetros se llamó
3. No requiere cambios en la arquitectura (solo inyectar `SupabaseClient`)
4. Funciona con Auth y Storage, no solo con queries de base de datos

> El paquete `mock_supabase_http_client` tiene su lugar para **tests de integración ligeros** donde quieres probar la interacción entre varias tablas sin un servidor real. Lo cubrimos en detalle en [07b-practica-supabase-mock-http-client.md](./07b-practica-supabase-mock-http-client.md).

---

## 4. El patrón Fake para Supabase

### 🎭 ¿Qué es un Fake?

Un **Fake** es una implementación simplificada de una interfaz que funciona "de verdad" pero sin efectos secundarios. A diferencia de un Mock (que registra llamadas), un Fake ejecuta lógica real.

En el caso de Supabase, creamos Fakes que extienden `Fake` e implementan `PostgrestTransformBuilder` únicamente para sobreescribir el método `then()` que Dart llama al hacer `await`.

### 📋 Las 4 variantes de Fake

#### FakeTransformBuilder — Para `.single()`

```dart
class FakeTransformBuilder extends Fake
    implements PostgrestTransformBuilder<Map<String, dynamic>> {
  final Map<String, dynamic> data;
  FakeTransformBuilder(this.data);

  @override
  Future<T> then<T>(
    FutureOr<T> Function(Map<String, dynamic>) onValue, {
    Function? onError,
  }) => Future<T>.value(onValue(data));
}
```

**Uso:** Cuando la query termina con `.single()` y esperas un mapa concreto.

#### FakeNullableTransformBuilder — Para `.maybeSingle()`

```dart
class FakeNullableTransformBuilder extends Fake
    implements PostgrestTransformBuilder<Map<String, dynamic>?> {
  final Map<String, dynamic>? data;
  FakeNullableTransformBuilder(this.data);

  @override
  Future<T> then<T>(
    FutureOr<T> Function(Map<String, dynamic>?) onValue, {
    Function? onError,
  }) => Future<T>.value(onValue(data));
}
```

**Uso:** Cuando la query termina con `.maybeSingle()` y puede devolver `null`.

#### FakeListTransformBuilder — Para cadenas que usan `.select()` después de `.update()` o `.insert()`

```dart
class FakeListTransformBuilder extends Fake
    implements PostgrestTransformBuilder<List<Map<String, dynamic>>> {
  final PostgrestTransformBuilder<Map<String, dynamic>> Function() _singleResult;

  FakeListTransformBuilder(this._singleResult);

  @override
  PostgrestTransformBuilder<Map<String, dynamic>> single() => _singleResult();
}
```

**Uso:** Cuando haces `.update(data).eq().select()` que retorna una lista, y luego llamas `.single()` sobre ella.

#### AwaitableFilterBuilder / FakeFilterBuilder — Para terminales sin transform

```dart
// Cuando el await se hace directo sobre el FilterBuilder
class AwaitableFilterBuilder extends Fake
    implements PostgrestFilterBuilder<List<Map<String, dynamic>>> {
  @override
  Future<T> then<T>(
    FutureOr<T> Function(List<Map<String, dynamic>>) onValue, {
    Function? onError,
  }) => Future<T>.value(onValue([]));
}

// Versión con datos configurables
class FakeFilterBuilder extends Fake
    implements PostgrestFilterBuilder<List<Map<String, dynamic>>> {
  final List<Map<String, dynamic>> data;
  FakeFilterBuilder(this.data);

  @override
  Future<T> then<T>(
    FutureOr<T> Function(List<Map<String, dynamic>>) onValue, {
    Function? onError,
  }) => Future<T>.value(onValue(data));
}
```

**Uso:** Cuando haces `.delete().eq()` y el resultado se usa con `await` directamente.

### 📊 ¿Cuándo usar cada Fake?

| Operación | Cadena típica | Fake necesario |
|-----------|---------------|----------------|
| SELECT single row | `.select().eq().single()` | `FakeTransformBuilder` |
| SELECT nullable | `.select().eq().maybeSingle()` | `FakeNullableTransformBuilder` |
| SELECT list | `.select().eq()` (await directo) | `AwaitableFilterBuilder` |
| INSERT + return | `.insert().select().single()` | `FakeListTransformBuilder` + `FakeTransformBuilder` |
| UPDATE + return | `.update().eq().select().single()` | `FakeListTransformBuilder` + `FakeTransformBuilder` |
| DELETE | `.delete().eq()` (await directo) | `FakeFilterBuilder` |

---

## 5. Jerarquía de Mocks

### 🎯 Mocks necesarios

```dart
// ─── Supabase Core ───
class MockSupabaseClient extends Mock implements SupabaseClient {}

// ─── Auth ───
class MockGoTrueClient extends Mock implements GoTrueClient {}
class MockUserResponse extends Mock implements UserResponse {}
class MockAuthResponse extends Mock implements AuthResponse {}

// ─── Database ───
class MockSupabaseQueryBuilder extends Mock implements SupabaseQueryBuilder {}
class MockPostgrestFilterBuilder extends Mock
    implements PostgrestFilterBuilder<List<Map<String, dynamic>>> {}
class MockPostgrestTransformBuilderList extends Mock
    implements PostgrestTransformBuilder<List<Map<String, dynamic>>> {}

// ─── Storage ───
class MockSupabaseStorageClient extends Mock implements SupabaseStorageClient {}
class MockStorageFileApi extends Mock implements StorageFileApi {}
```

### 🔗 Cómo se conectan

```
MockSupabaseClient
  ├── .auth       → MockGoTrueClient
  ├── .from()     → MockSupabaseQueryBuilder
  │     └── .select() / .insert() / .update() / .delete()
  │           → MockPostgrestFilterBuilder
  │                 ├── .eq() / .neq() / .or()
  │                 │     → MockPostgrestFilterBuilder (misma instancia)
  │                 ├── .single()      → FakeTransformBuilder
  │                 ├── .maybeSingle() → FakeNullableTransformBuilder
  │                 ├── .select()      → MockPostgrestTransformBuilderList
  │                 │     └── .single() → FakeTransformBuilder (via FakeListTransformBuilder)
  │                 └── (await)        → AwaitableFilterBuilder / FakeFilterBuilder
  └── .storage    → MockSupabaseStorageClient
        └── .from() → MockStorageFileApi
```

---

## 6. registerFallbackValue

Mocktail necesita un "fallback value" para poder usar `any()` con tipos personalizados. Sin esto, lanza un error cuando intentas usar `any()` en un parámetro de ese tipo.

### 📝 Qué registrar y por qué

```dart
setUpAll(() {
  // Para when(() => mockSupabase.from(any()))
  registerFallbackValue(MockSupabaseQueryBuilder());

  // Para when(() => mockFilterBuilder.eq(any(), any()))
  registerFallbackValue(MockPostgrestFilterBuilder());

  // Para when(() => mockStorageBucket.uploadBinary(any(), any(), ...))
  registerFallbackValue(Uint8List(0));

  // Para when(() => mockAuth.updateUser(any()))
  registerFallbackValue(UserAttributes());

  // Para when(() => mockStorageBucket.uploadBinary(..., fileOptions: any(named: 'fileOptions')))
  registerFallbackValue(FileOptions());

  // Si usas MockPostgrestTransformBuilderList con any()
  registerFallbackValue(MockPostgrestTransformBuilderList());
});
```

> **Regla:** Si al usar `any()` mocktail lanza `No fallback value registered for type X`, crea un `Fake implements X` y regístralo con `registerFallbackValue(FakeX())`.

---

## 7. Manejo de errores

### 🎯 Patrón: ServerException wrapper

Los DataSources con Supabase típicamente envuelven errores en `ServerException`:

```dart
// En el DataSource:
try {
  final result = await supabase
      .from('profiles')
      .select()
      .eq('user_id', userId)
      .single();
  return UserProfileModel.fromJson(result);
} catch (e) {
  throw ServerException(message: e.toString());
}
```

### 🧪 Cómo testear errores

```dart
// Opción 1: thenThrow
test('should throw ServerException when query fails', () async {
  when(() => mockFilterBuilder.eq(any(), any())).thenThrow(
    Exception('Database error'),
  );

  try {
    await dataSource.getProfile(tUserId);
    fail('Should have thrown ServerException');
  } on Object catch (e) {
    expect(e, isA<ServerException>());
  }
});

// Opción 2: throwsA (cuando se lanza directo)
test('should throw ServerException on auth error', () async {
  when(() => mockAuth.signInWithPassword(
    email: any(named: 'email'),
    password: any(named: 'password'),
  )).thenThrow(AuthException('Invalid credentials'));

  expect(
    () => dataSource.login(tEmail, tPassword),
    throwsA(isA<ServerException>()),
  );
});
```

> **Nota:** La opción 1 (try-catch) es más confiable cuando hay múltiples puntos donde puede fallar la cadena de builders. La opción 2 (throwsA) funciona bien cuando el error se lanza desde un único método mockeable.

---

## 8. Checklist

- [ ] Entender por qué `PostgrestTransformBuilder` requiere Fakes (hereda de `Future<T>`)
- [ ] Conocer la cadena de builders de Supabase y qué retorna cada paso
- [ ] Elegir la estrategia de mocking adecuada (Mocktail + Fakes para unit tests)
- [ ] Implementar las 4 variantes de Fake según el tipo de query
- [ ] Configurar todos los mocks necesarios (SupabaseClient, GoTrueClient, QueryBuilder, etc.)
- [ ] Registrar fallback values con `registerFallbackValue` en `setUpAll`
- [ ] Testear casos de éxito y error para cada operación (SELECT, INSERT, UPDATE, DELETE)
- [ ] Verificar interacciones con `verify()` (tabla, método, argumentos)
- [ ] Manejar correctamente las excepciones de Supabase como `ServerException`

---

## 🚀 Siguiente Paso

**Práctica:** [07a-practica-supabase-datasources.md](./07a-practica-supabase-datasources.md)

> Ejercicios paso a paso para testear DataSources de Supabase con Mocktail + Fakes.
