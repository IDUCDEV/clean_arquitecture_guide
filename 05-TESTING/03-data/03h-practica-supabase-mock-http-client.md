# 🏋️ 03h: Bonus - mock_supabase_http_client (Paquete Oficial)

> **¿De qué trata este bonus?** Del paquete oficial de Supabase community para mockear el cliente HTTP de Supabase en tests, y cómo se compara con el enfoque Mocktail + Fakes.

---

## 📋 Índice

1. [¿Qué es mock_supabase_http_client?](#1-qué-es-mock_supabase_http_client)
2. [¿Cuándo usarlo y cuándo NO?](#2-cuándo-usarlo-y-cuándo-no)
3. [Configuración](#3-configuración)
4. [Uso básico](#4-uso-básico)
5. [Operaciones CRUD](#5-operaciones-crud)
6. [Simular errores](#6-simular-errores)
7. [Comparativa lado a lado: Mocktail+Fakes vs mock_supabase_http_client](#7-comparativa-lado-a-lado)
8. [Limitaciones](#8-limitaciones)

---

## 1. ¿Qué es mock_supabase_http_client?

Es un paquete oficial de Supabase community ([pub.dev](https://pub.dev/packages/mock_supabase_http_client), [GitHub](https://github.com/supabase-community/mock_supabase_http_client)) que intercepta las peticiones HTTP de `SupabaseClient` y las responde con datos en memoria, sin necesidad de un servidor real.

```dart
final mockHttpClient = MockSupabaseHttpClient();
final supabase = SupabaseClient(
  'https://mock.supabase.co',
  'fakeAnonKey',
  httpClient: mockHttpClient,
);
```

A partir de ahí, puedes insertar datos de prueba y hacer queries exactamente como en producción.

---

## 2. ¿Cuándo usarlo y cuándo NO?

### ✅ Úsalo cuando

- Quieres hacer **tests de integración ligeros** que ejerciten varias tablas y relaciones
- Tienes queries con ** joins y referencias** entre tablas
- Necesitas simular **errores específicos de PostgreSQL** (unique constraint, permission denied)
- Usas **RPC functions** y quieres probar su integración
- Prefieres no definir Fakes manuales para cada tipo de query

### ❌ NO lo uses cuando

- Necesitas testear **Auth** (signIn, signUp, etc.) — el paquete **no soporta auth**
- Necesitas testear **Storage** (upload, download) — **no soportado**
- Necesitas `verify()` preciso sobre qué tabla y con qué argumentos se llamó
- Haces **unit testing puro** de un DataSource individual
- Quieres máxima velocidad de ejecución

### 📊 En resumen

| Criterio | Mocktail + Fakes | mock_supabase_http_client |
|----------|-----------------|--------------------------|
| **Tipo de test** | Unitario | Integración ligero |
| **Auth** | ✅ Sí | ❌ No |
| **Storage** | ✅ Sí | ❌ No |
| **verify()** | ✅ Preciso | ❌ No |
| **Relaciones entre tablas** | ❌ Manual | ✅ Automático |
| **Simular errores SQL** | ❌ No | ✅ Sí |
| **RPC functions** | ❌ No | ✅ Sí |
| **Velocidad** | Máxima | Media |

---

## 3. Configuración

### 📦 pubspec.yaml

```yaml
dev_dependencies:
  mock_supabase_http_client: ^0.0.3
```

```bash
flutter pub get
```

### 🧪 Setup básico en tests

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mock_supabase_http_client/mock_supabase_http_client.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

void main() {
  late SupabaseClient mockSupabase;
  late MockSupabaseHttpClient mockHttpClient;

  setUp(() {
    mockHttpClient = MockSupabaseHttpClient();
    mockSupabase = SupabaseClient(
      'https://mock.supabase.co',
      'fakeAnonKey',
      httpClient: mockHttpClient,
    );
  });

  tearDown(() {
    mockHttpClient.reset();
  });
}
```

No necesitas mocks de `SupabaseQueryBuilder`, `PostgrestFilterBuilder`, ni Fakes. El paquete maneja toda la cadena internamente.

---

## 4. Uso básico

### Insertar datos de prueba y consultarlos

```dart
test('inserting and selecting data works', () async {
  // Insertar datos en la "tabla" posts
  await mockSupabase.from('posts').insert({'title': 'Hello, world!'});

  // Consultar los datos
  final posts = await mockSupabase.from('posts').select();

  expect(posts.length, 1);
  expect(posts.first['title'], 'Hello, world!');
});
```

### Con filtros

```dart
test('filtering with eq works', () async {
  await mockSupabase.from('posts').insert([
    {'id': 1, 'title': 'Post 1', 'published': true},
    {'id': 2, 'title': 'Post 2', 'published': false},
  ]);

  final published = await mockSupabase
      .from('posts')
      .select()
      .eq('published', true);

  expect(published.length, 1);
  expect(published.first['title'], 'Post 1');
});
```

---

## 5. Operaciones CRUD

### 📝 Ejemplo completo con una tabla de perfiles

```dart
void main() {
  late SupabaseClient mockSupabase;
  late MockSupabaseHttpClient mockHttpClient;

  setUp(() {
    mockHttpClient = MockSupabaseHttpClient();
    mockSupabase = SupabaseClient(
      'https://mock.supabase.co',
      'fakeAnonKey',
      httpClient: mockHttpClient,
    );
  });

  tearDown(() {
    mockHttpClient.reset();
  });

  group('CRUD: profiles', () {
    test('INSERT profile', () async {
      final profile = await mockSupabase.from('profiles').insert({
        'user_id': 'user-123',
        'full_name': 'Test User',
      }).select().single();

      expect(profile['full_name'], 'Test User');
      expect(profile['user_id'], 'user-123');
      expect(profile['id'], isNotNull); // auto-generado
    });

    test('SELECT profile by user_id', () async {
      // Insertar datos de prueba
      await mockSupabase.from('profiles').insert([
        {'user_id': 'user-1', 'full_name': 'User One'},
        {'user_id': 'user-2', 'full_name': 'User Two'},
      ]);

      final profiles = await mockSupabase
          .from('profiles')
          .select()
          .eq('user_id', 'user-1');

      expect(profiles.length, 1);
      expect(profiles.first['full_name'], 'User One');
    });

    test('UPDATE profile', () async {
      final profile = await mockSupabase.from('profiles').insert({
        'user_id': 'user-123',
        'full_name': 'Old Name',
      }).select().single();

      await mockSupabase
          .from('profiles')
          .update({'full_name': 'New Name'})
          .eq('id', profile['id']);

      final updated = await mockSupabase
          .from('profiles')
          .select()
          .eq('id', profile['id'])
          .single();

      expect(updated['full_name'], 'New Name');
    });

    test('DELETE profile', () async {
      await mockSupabase.from('profiles').insert({
        'user_id': 'user-123',
        'full_name': 'To Delete',
      });

      await mockSupabase
          .from('profiles')
          .delete()
          .eq('user_id', 'user-123');

      final profiles = await mockSupabase
          .from('profiles')
          .select()
          .eq('user_id', 'user-123');

      expect(profiles, isEmpty);
    });
  });
}
```

### 🔗 Relaciones entre tablas

```dart
test('queries with referenced tables', () async {
  await mockSupabase.from('posts').insert([
    {
      'id': 1,
      'title': 'First post',
      'authors': {'id': 1, 'name': 'Author One'},
      'comments': [
        {'id': 1, 'content': 'Great post!'},
        {'id': 2, 'content': 'Thanks!'},
      ],
    },
  ]);

  final posts = await mockSupabase.from('posts').select('''
    id, title, authors(id, name), comments(id, content)
  ''');

  expect(posts.length, 1);
  expect(posts.first['authors']['name'], 'Author One');
  expect(posts.first['comments'].length, 2);
});
```

---

## 6. Simular errores

### 🚨 Unique constraint violation

```dart
test('should throw on duplicate email', () async {
  mockHttpClient = MockSupabaseHttpClient(
    postgrestExceptionTrigger: (schema, table, data, type) {
      if (table == 'users' && type == RequestType.insert) {
        throw PostgrestException(
          message: 'duplicate key violates unique constraint "users_email_key"',
          code: '23505',
        );
      }
    },
  );
  mockSupabase = SupabaseClient(
    'https://mock.supabase.co',
    'fakeAnonKey',
    httpClient: mockHttpClient,
  );

  // Primer insert funciona
  await mockSupabase.from('users').insert({
    'email': 'test@example.com', 'name': 'Test',
  });

  // Segundo insert con mismo email debe fallar
  expect(
    () => mockSupabase.from('users').insert({
      'email': 'test@example.com', 'name': 'Duplicated',
    }),
    throwsA(isA<PostgrestException>()),
  );
});
```

### 🚫 Permission denied

```dart
test('should throw on permission denied', () async {
  mockHttpClient = MockSupabaseHttpClient(
    postgrestExceptionTrigger: (schema, table, data, type) {
      if (table == 'private_data' && type == RequestType.select) {
        throw PostgrestException(
          message: 'permission denied for table private_data',
          code: '42501',
        );
      }
    },
  );
  // ...
});
```

### 📞 RPC functions

```dart
test('should call RPC function', () async {
  mockHttpClient.registerRpcFunction(
    'get_user_status',
    (params, tables) => {'status': 'active'},
  );

  final result = await mockSupabase.rpc('get_user_status');
  expect(result, {'status': 'active'});
});
```

---

## 7. Comparativa lado a lado

### Mismo test: obtener perfil por userId

#### Con Mocktail + Fakes

```dart
test('returns profile with Mocktail+Fakes', () async {
  when(() => mockSupabase.from(any())).thenAnswer((_) => mockQueryBuilder);
  when(() => mockQueryBuilder.select(any())).thenAnswer((_) => mockFilterBuilder);
  when(() => mockFilterBuilder.eq(any(), any())).thenAnswer((_) => mockFilterBuilder);
  when(() => mockFilterBuilder.single())
      .thenAnswer((_) => FakeTransformBuilder(tProfileMap));

  final result = await dataSource.getProfile('user-123');

  expect(result.userId, 'user-123');
  verify(() => mockSupabase.from('profiles')).called(1);
  verify(() => mockFilterBuilder.eq('user_id', 'user-123')).called(1);
});
```

#### Con mock_supabase_http_client

```dart
test('returns profile with mock_supabase_http_client', () async {
  // Insertar dato de prueba
  await mockSupabase.from('profiles').insert(tProfileMap);

  // Ejecutar el DataSource real
  final result = await dataSource.getProfile('user-123');

  expect(result.userId, 'user-123');
  // ❌ No podemos verificar que se llamó a 'profiles' con eq('user_id', ...)
});
```

### 🎯 Diferencias clave

| Aspecto | Mocktail + Fakes | mock_supabase_http_client |
|---------|-----------------|--------------------------|
| **Líneas de setup** | ~8 (stubs de cadena) | ~4 (insertar datos) |
| **verify()** | ✅ Sí | ❌ No (assert en datos) |
| **DataSource real** | ✅ Sí (con SupabaseClient mockeado) | ✅ Sí (con SupabaseClient real + HTTP mock) |
| **Cambio en arquitectura** | ❌ Ninguno | ❌ Ninguno |
| **Mantener datos de prueba** | Constantes inline | Insertar en mock DB |

---

## 8. Limitaciones

| Funcionalidad | Soportado? |
|---------------|-----------|
| `select()` con filtros | ✅ Sí |
| `insert()` / `update()` / `delete()` | ✅ Sí |
| `upsert` | ✅ Sí |
| `single()` / `maybeSingle()` | ✅ Sí |
| `order()` / `limit()` / `range()` | ✅ Sí |
| `neq()` / `or()` / `in()` | ✅ Sí |
| Referencias entre tablas | ✅ Sí |
| Simular errores SQL | ✅ Sí |
| RPC functions | ✅ Sí |
| **Auth** (`signInWithPassword`, `signUp`, etc.) | ❌ No |
| **Storage** (`uploadBinary`, `getPublicUrl`, etc.) | ❌ No |
| **Realtime** (`stream()`, subscriptions) | ❌ No |
| **count()** | ✅ Sí |
| **CSV response** | ❌ No |

---

## 🎯 ¿Cuál elegir?

```
┌─────────────────────────────────────────────────────────────────┐
│                    ¿QUÉ NECESITAS TESTEAR?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ¿Auth, Storage o verify() preciso?                             │
│       │                                                         │
│       ├─ Sí → Mocktail + Fakes  (07a-practica)                  │
│       │                                                         │
│       └─ No → ¿Varias tablas, joins, o errores SQL?            │
│               │                                                 │
│               ├─ Sí → mock_supabase_http_client (este archivo)  │
│               │                                                 │
│               └─ No → Cualquiera funciona,                      │
│                        Mocktail+Fakes es más rápido             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Siguiente Paso

**Teoría:** [Parte 4: Testing Presentation](../04-presentation/04-presentation-testing.md)

> Una vez que domines el testing de DataSources, pasa a testear Cubits y Widgets.
