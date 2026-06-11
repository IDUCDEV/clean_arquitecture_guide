# 🏋️ 07a: Práctica - DataSources con Supabase (Mocktail + Fakes)

> **¿De qué trata esta práctica?** De testear DataSources que usan Supabase, usando **Mocktail** para los mocks y **Fakes** para los `PostgrestTransformBuilder` que implementan `Future<T>`.

---

## 📋 Ejercicios

- [Ejercicio 1: Configuración inicial](#ejercicio-1-configuración-inicial)
- [Ejercicio 2: Auth DataSource (login/signup/logout)](#ejercicio-2-auth-datasource)
- [Ejercicio 3: SELECT con .single()](#ejercicio-3-select-con-single)
- [Ejercicio 4: SELECT con .maybeSingle()](#ejercicio-4-select-con-maybesingle)
- [Ejercicio 5: UPDATE con retorno](#ejercicio-5-update-con-retorno)
- [Ejercicio 6: INSERT con retorno](#ejercicio-6-insert-con-retorno)
- [Ejercicio 7: DELETE](#ejercicio-7-delete)
- [Ejercicio 8: Storage (upload / getUrl / remove)](#ejercicio-8-storage)
- [Ejercicio 9: Ejemplo completo - ProfileRemoteDataSource](#ejercicio-9-ejemplo-completo---profileremotedatasource)
- [Ejercicio 10: Ejemplo completo - PaymentMethodRemoteDataSource](#ejercicio-10-ejemplo-completo---paymentmethodremotedatasource)

---

## 🎬 Antes de Empezar

Asegúrate de tener estas dependencias en `pubspec.yaml`:

```yaml
dependencies:
  supabase_flutter: ^2.12.4
  fpdart: ^1.0.0       # Para Either<Failure, T>
  equatable: ^2.0.0     # Para entidades

dev_dependencies:
  flutter_test:
    sdk: flutter
  mocktail: ^1.0.5
```

```bash
flutter pub get
```

---

## Ejercicio 1: Configuración inicial

### 📝 Tu Misión

Crear la estructura base para los tests: mocks, fakes y `registerFallbackValue`. Esta configuración se reutiliza en todos los ejercicios siguientes.

### ✅ Paso 1: Crea la estructura de carpetas

```bash
mkdir -p test/features/auth/data/datasources
mkdir -p test/features/profile/data/datasources
```

### ✅ Paso 2: Crea los mocks y fakes

Crea un archivo compartido (o defínelos inline en cada test — en el monorepo se definen inline):

```dart
// test/helpers/supabase_mocks.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

// ─── MOCKS ───

class MockSupabaseClient extends Mock implements SupabaseClient {}

class MockGoTrueClient extends Mock implements GoTrueClient {}

class MockUserResponse extends Mock implements UserResponse {}

class MockAuthResponse extends Mock implements AuthResponse {}

class MockSupabaseQueryBuilder extends Mock implements SupabaseQueryBuilder {}

class MockPostgrestFilterBuilder extends Mock
    implements PostgrestFilterBuilder<List<Map<String, dynamic>>> {}

class MockSupabaseStorageClient extends Mock implements SupabaseStorageClient {}

class MockStorageFileApi extends Mock implements StorageFileApi {}

// ─── FAKES PARA PostgrestTransformBuilder ───

/// Para queries que terminan con .single()
class FakeTransformBuilder extends Fake
    implements PostgrestTransformBuilder<Map<String, dynamic>> {
  final Map<String, dynamic> data;
  FakeTransformBuilder(this.data);

  @override
  Future<T> then<T>(
    FutureOr<T> Function(Map<String, dynamic>) onValue, {
    Function? onError,
  }) =>
      Future<T>.value(onValue(data));
}

/// Para queries que terminan con .maybeSingle()
class FakeNullableTransformBuilder extends Fake
    implements PostgrestTransformBuilder<Map<String, dynamic>?> {
  final Map<String, dynamic>? data;
  FakeNullableTransformBuilder(this.data);

  @override
  Future<T> then<T>(
    FutureOr<T> Function(Map<String, dynamic>?) onValue, {
    Function? onError,
  }) =>
      Future<T>.value(onValue(data));
}

/// Para cadenas .update().eq().select() que devuelven lista + single()
class FakeListTransformBuilder extends Fake
    implements PostgrestTransformBuilder<List<Map<String, dynamic>>> {
  final PostgrestTransformBuilder<Map<String, dynamic>> Function() _singleResult;

  FakeListTransformBuilder(this._singleResult);

  @override
  PostgrestTransformBuilder<Map<String, dynamic>> single() => _singleResult();
}

/// Para cuando se hace await directo sobre el FilterBuilder
/// (ej: delete().eq() sin select)
class AwaitableFilterBuilder extends Fake
    implements PostgrestFilterBuilder<List<Map<String, dynamic>>> {
  @override
  Future<T> then<T>(
    FutureOr<T> Function(List<Map<String, dynamic>>) onValue, {
    Function? onError,
  }) =>
      Future<T>.value(onValue([]));
}

/// Versión configurable de AwaitableFilterBuilder
class FakeFilterBuilder extends Fake
    implements PostgrestFilterBuilder<List<Map<String, dynamic>>> {
  final List<Map<String, dynamic>> data;
  FakeFilterBuilder(this.data);

  @override
  Future<T> then<T>(
    FutureOr<T> Function(List<Map<String, dynamic>>) onValue, {
    Function? onError,
  }) =>
      Future<T>.value(onValue(data));
}
```

### ✅ Paso 3: Registro de fallback values

```dart
// setUpAll en cada test file
setUpAll(() {
  registerFallbackValue(MockSupabaseQueryBuilder());
  registerFallbackValue(MockPostgrestFilterBuilder());
  registerFallbackValue(Uint8List(0));
  registerFallbackValue(UserAttributes());
  registerFallbackValue(FileOptions());
});
```

---

## Ejercicio 2: Auth DataSource

### 📝 Tu Misión

Testear un DataSource que usa `GoTrueClient` para autenticación. **No necesita Fakes** porque `signInWithPassword`, `signUp`, etc. devuelven `Future<T>` directamente.

### 📁 DataSource de ejemplo

```dart
// lib/features/auth/data/datasources/auth_remote_data_source.dart
class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final SupabaseClient supabase;

  AuthRemoteDataSourceImpl({required this.supabase});

  @override
  Future<UserModel> login(String email, String password) async {
    try {
      final response = await supabase.auth.signInWithPassword(
        email: email,
        password: password,
      );
      return UserModel.fromJson(response.user!.toJson());
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<void> signOut() async {
    try {
      await supabase.auth.signOut();
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<void> updatePassword(String newPassword) async {
    try {
      await supabase.auth.updateUser(UserAttributes(password: newPassword));
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }
}
```

### ✅ Tests

```dart
// test/features/auth/data/datasources/auth_remote_data_source_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

// Importar mocks y fakes del ejercicio 1
import '../../../../helpers/supabase_mocks.dart';

void main() {
  late AuthRemoteDataSourceImpl dataSource;
  late MockSupabaseClient mockSupabase;
  late MockGoTrueClient mockAuth;

  const tEmail = 'test@example.com';
  const tPassword = 'password123';

  setUp(() {
    mockSupabase = MockSupabaseClient();
    mockAuth = MockGoTrueClient();

    when(() => mockSupabase.auth).thenReturn(mockAuth);

    dataSource = AuthRemoteDataSourceImpl(supabase: mockSupabase);
  });

  group('login', () {
    test('should return UserModel on success', () async {
      // Arrange
      final mockResponse = MockAuthResponse();
      when(() => mockAuth.signInWithPassword(
        email: any(named: 'email'),
        password: any(named: 'password'),
      )).thenAnswer((_) async => mockResponse);

      // Act
      final result = await dataSource.login(tEmail, tPassword);

      // Assert
      expect(result, isA<UserModel>());
      verify(() => mockAuth.signInWithPassword(
        email: tEmail,
        password: tPassword,
      )).called(1);
    });

    test('should throw ServerException on failure', () async {
      // Arrange
      when(() => mockAuth.signInWithPassword(
        email: any(named: 'email'),
        password: any(named: 'password'),
      )).thenThrow(AuthException('Invalid credentials'));

      // Act & Assert
      expect(
        () => dataSource.login(tEmail, tPassword),
        throwsA(isA<ServerException>()),
      );
    });
  });

  group('signOut', () {
    test('should call signOut on success', () async {
      when(() => mockAuth.signOut()).thenAnswer((_) async => {});

      await dataSource.signOut();

      verify(() => mockAuth.signOut()).called(1);
    });

    test('should throw ServerException on failure', () async {
      when(() => mockAuth.signOut()).thenThrow(Exception('error'));

      expect(
        () => dataSource.signOut(),
        throwsA(isA<ServerException>()),
      );
    });
  });

  group('updatePassword', () {
    test('should complete successfully', () async {
      final mockResponse = MockUserResponse();
      when(() => mockAuth.updateUser(any())).thenAnswer(
        (_) async => mockResponse,
      );

      await dataSource.updatePassword('newPass123');

      verify(() => mockAuth.updateUser(any())).called(1);
    });
  });
}
```

### 🧪 Ejecuta

```bash
flutter test test/features/auth/data/datasources/auth_remote_data_source_test.dart
```

---

## Ejercicio 3: SELECT con .single()

### 📝 Tu Misión

Testear una consulta que obtiene un solo registro: `.select().eq().single()`.

### 📁 DataSource de ejemplo

```dart
Future<UserProfileModel> getProfile(String userId) async {
  try {
    final data = await supabase
        .from('profiles')
        .select()
        .eq('user_id', userId)
        .single();
    return UserProfileModel.fromJson(data);
  } catch (e) {
    throw ServerException(message: e.toString());
  }
}
```

### 🧪 Test

```dart
  test('should return UserProfileModel on success', () async {
    // Arrange
    final mockQueryBuilder = MockSupabaseQueryBuilder();
    final mockFilterBuilder = MockPostgrestFilterBuilder();
    const tProfileMap = <String, dynamic>{
      'id': 'profile-1',
      'user_id': 'user-123',
      'full_name': 'Test User',
    };

    when(() => mockSupabase.from(any())).thenAnswer((_) => mockQueryBuilder);
    when(() => mockQueryBuilder.select(any())).thenAnswer(
      (_) => mockFilterBuilder,
    );
    when(() => mockFilterBuilder.eq(any(), any())).thenAnswer(
      (_) => mockFilterBuilder,
    );
    when(() => mockFilterBuilder.single()).thenAnswer(
      (_) => FakeTransformBuilder(tProfileMap),
    );

    // Act
    final result = await dataSource.getProfile('user-123');

    // Assert
    expect(result, isA<UserProfileModel>());
    verify(() => mockSupabase.from('profiles')).called(1);
    verify(() => mockQueryBuilder.select()).called(1);
    verify(() => mockFilterBuilder.eq('user_id', 'user-123')).called(1);
    verify(() => mockFilterBuilder.single()).called(1);
  });
```

### 🔑 Claves del test

| Paso | Código | Explicación |
|------|--------|-------------|
| `.from('profiles')` | `mockSupabase.from(any())` | `thenAnswer` porque devuelve `SupabaseQueryBuilder` |
| `.select()` | `mockQueryBuilder.select(any())` | `thenAnswer` → `PostgrestFilterBuilder` |
| `.eq('user_id', id)` | `mockFilterBuilder.eq(any(), any())` | Se retorna a sí mismo (misma instancia) |
| `.single()` | `mockFilterBuilder.single()` | **FakeTransformBuilder** — necesario porque implementa `Future` |

---

## Ejercicio 4: SELECT con .maybeSingle()

### 📝 Tu Misión

Testear una consulta que puede devolver `null` cuando no encuentra resultados.

### 📁 DataSource de ejemplo

```dart
Future<UserProfileModel?> findProfile(String userId) async {
  try {
    final data = await supabase
        .from('profiles')
        .select()
        .eq('user_id', userId)
        .maybeSingle();
    if (data == null) return null;
    return UserProfileModel.fromJson(data);
  } catch (e) {
    throw ServerException(message: e.toString());
  }
}
```

### 🧪 Tests

```dart
  test('should return UserProfileModel when profile exists', () async {
    // Arrange
    when(() => mockQueryBuilder.select(any()))
        .thenAnswer((_) => mockFilterBuilder);
    when(() => mockFilterBuilder.eq(any(), any()))
        .thenAnswer((_) => mockFilterBuilder);
    when(() => mockFilterBuilder.maybeSingle()).thenAnswer(
      (_) => FakeNullableTransformBuilder(tProfileMap),
    );

    // Act
    final result = await dataSource.findProfile('user-123');

    // Assert
    expect(result, isA<UserProfileModel>());
  });

  test('should return null when profile does not exist', () async {
    // Arrange
    when(() => mockQueryBuilder.select(any()))
        .thenAnswer((_) => mockFilterBuilder);
    when(() => mockFilterBuilder.eq(any(), any()))
        .thenAnswer((_) => mockFilterBuilder);
    when(() => mockFilterBuilder.maybeSingle()).thenAnswer(
      (_) => FakeNullableTransformBuilder(null),
    );

    // Act
    final result = await dataSource.findProfile('user-123');

    // Assert
    expect(result, isNull);
  });
```

---

## Ejercicio 5: UPDATE con retorno

### 📝 Tu Misión

Testear una actualización que devuelve el registro actualizado. La cadena es: `.update().eq().select().single()`.

### 📁 DataSource de ejemplo

```dart
Future<UserProfileModel> updateProfile({
  required String userId,
  required Map<String, dynamic> data,
}) async {
  try {
    final result = await supabase
        .from('profiles')
        .update(data)
        .eq('user_id', userId)
        .select()
        .single();
    return UserProfileModel.fromJson(result);
  } catch (e) {
    throw ServerException(message: e.toString());
  }
}
```

### 🧪 Test

```dart
  test('should return updated UserProfileModel on success', () async {
    // Arrange
    when(() => mockQueryBuilder.update(any()))
        .thenAnswer((_) => mockFilterBuilder);
    when(() => mockFilterBuilder.eq(any(), any()))
        .thenAnswer((_) => mockFilterBuilder);
    when(() => mockFilterBuilder.select(any())).thenAnswer(
      (_) => FakeListTransformBuilder(
        () => FakeTransformBuilder(tProfileMap),
      ),
    );

    // Act
    final result = await dataSource.updateProfile(
      userId: 'user-123',
      data: {'full_name': 'Updated Name'},
    );

    // Assert
    expect(result, isA<UserProfileModel>());
    expect(result.userId, 'user-123');
    verify(() => mockSupabase.from('profiles')).called(1);
    verify(() => mockQueryBuilder.update({'full_name': 'Updated Name'})).called(1);
    verify(() => mockFilterBuilder.eq('user_id', 'user-123')).called(1);
    verify(() => mockFilterBuilder.select()).called(1);
  });
```

### 🔑 ¿Por qué `FakeListTransformBuilder`?

Cuando llamas a `.select()` después de `.update()`, retorna un `PostgrestTransformBuilder<List<Map<String, dynamic>>>`, no un `PostgrestFilterBuilder`. Por eso no podemos reusar `mockFilterBuilder` — necesitamos un builder diferente que entienda `.single()` sobre una lista.

`FakeListTransformBuilder` envuelve un `FakeTransformBuilder` y lo devuelve cuando se llama a `.single()`:

```
.update(data) → PostgrestFilterBuilder<List<...>>
.eq('id', x)  → PostgrestFilterBuilder<List<...>>  (mismo tipo)
.select()     → PostgrestTransformBuilder<List<...>>  ← FakeListTransformBuilder
.single()     → PostgrestTransformBuilder<Map<String, dynamic>>  ← FakeTransformBuilder
```

---

## Ejercicio 6: INSERT con retorno

### 📝 Tu Misión

Testear una inserción que devuelve el registro creado. Misma cadena que UPDATE: `.insert().select().single()`.

### 📁 DataSource de ejemplo

```dart
Future<PaymentMethodModel> createPaymentMethod(
  Map<String, dynamic> data,
) async {
  try {
    final result = await supabase
        .from('payment_methods')
        .insert(data)
        .select()
        .single();
    return PaymentMethodModel.fromJson(result);
  } catch (e) {
    throw ServerException(message: e.toString());
  }
}
```

### 🧪 Test

```dart
  test('should return created PaymentMethodModel on success', () async {
    // Arrange
    const tNewMethodMap = <String, dynamic>{
      'id': 'new-001',
      'user_id': 'user-123',
      'type': 'mobile',
      'name': 'Pago Móvil',
    };

    when(() => mockQueryBuilder.insert(any()))
        .thenAnswer((_) => mockFilterBuilder);
    when(() => mockFilterBuilder.select(any())).thenAnswer(
      (_) => FakeListTransformBuilder(
        () => FakeTransformBuilder(tNewMethodMap),
      ),
    );

    // Act
    final result = await dataSource.createPaymentMethod({
      'user_id': 'user-123',
      'type': 'mobile',
      'name': 'Pago Móvil',
    });

    // Assert
    expect(result, isA<PaymentMethodModel>());
    verify(() => mockSupabase.from('payment_methods')).called(1);
    verify(() => mockQueryBuilder.insert(any())).called(1);
    verify(() => mockFilterBuilder.select()).called(1);
  });
```

---

## Ejercicio 7: DELETE

### 📝 Tu Misión

Testear una eliminación. La cadena es: `.delete().eq()` y se usa `await` directo.

### 📁 DataSource de ejemplo

```dart
Future<void> deletePaymentMethod(String methodId) async {
  try {
    await supabase
        .from('payment_methods')
        .delete()
        .eq('id', methodId);
  } catch (e) {
    throw ServerException(message: e.toString());
  }
}
```

### 🧪 Test

```dart
  test('should delete payment method successfully', () async {
    // Arrange
    when(() => mockQueryBuilder.delete())
        .thenAnswer((_) => mockFilterBuilder);
    when(() => mockFilterBuilder.eq(any(), any()))
        .thenAnswer((_) => AwaitableFilterBuilder());

    // Act
    await dataSource.deletePaymentMethod('method-001');

    // Assert
    verify(() => mockSupabase.from('payment_methods')).called(1);
    verify(() => mockQueryBuilder.delete()).called(1);
    verify(() => mockFilterBuilder.eq('id', 'method-001')).called(1);
  });
```

### 🔑 ¿Por qué `AwaitableFilterBuilder`?

Cuando haces `await supabase.from('table').delete().eq('id', x)`, el `await` actúa directamente sobre el `PostgrestFilterBuilder` retornado por `.eq()`. Como implementa `Future<List<Map<String, dynamic>>>`, Dart llama a `.then()` — igual que con `PostgrestTransformBuilder`. Necesitamos un Fake que sobrescriba `then()` para que retorne un valor (aunque sea `[]` vacío).

---

## Ejercicio 8: Storage

### 📝 Tu Misión

Testear operaciones de Storage: upload, obtener URL pública y eliminar archivos.

### 📁 DataSource de ejemplo

```dart
class ProfileRemoteDataSourceImpl implements ProfileRemoteDataSource {
  final SupabaseClient supabase;

  ProfileRemoteDataSourceImpl({required this.supabase});

  Future<String> uploadAvatar({
    required String userId,
    required String filePath,
  }) async {
    try {
      // 1. Verificar si ya tiene avatar
      final existing = await supabase
          .from('profiles')
          .select('avatar_url')
          .eq('user_id', userId)
          .maybeSingle();

      // 2. Si existe, eliminar avatar anterior
      if (existing?['avatar_url'] != null) {
        final oldUrl = existing!['avatar_url'] as String;
        final oldPath = oldUrl.split('/').last;
        await supabase.storage.from('avatars').remove([oldPath]);
      }

      // 3. Subir nuevo avatar
      final file = File(filePath);
      await supabase.storage.from('avatars').uploadBinary(
        '$userId/avatar.jpg',
        await file.readAsBytes(),
        fileOptions: const FileOptions(upsert: true),
      );

      // 4. Obtener URL pública
      return supabase.storage.from('avatars').getPublicUrl(
        '$userId/avatar.jpg',
      );
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }
}
```

### 🧪 Tests

```dart
  late MockSupabaseStorageClient mockStorageClient;
  late MockStorageFileApi mockStorageBucket;

  setUp(() {
    // ... mocks anteriores ...
    mockStorageClient = MockSupabaseStorageClient();
    mockStorageBucket = MockStorageFileApi();

    when(() => mockSupabase.storage).thenReturn(mockStorageClient);
    when(() => mockStorageClient.from(any())).thenReturn(mockStorageBucket);
  });

  group('uploadAvatar', () {
    test('should upload and return public URL when no existing avatar', () async {
      // Arrange - no existing avatar
      when(() => mockQueryBuilder.select(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.maybeSingle())
          .thenAnswer((_) => FakeNullableTransformBuilder(null));
      when(() => mockStorageBucket.uploadBinary(any(), any(),
        fileOptions: any(named: 'fileOptions'),
      )).thenAnswer((_) async => '');
      when(() => mockStorageBucket.getPublicUrl(any()))
          .thenReturn('https://example.com/avatar.jpg');

      // Act
      final result = await dataSource.uploadAvatar(
        userId: 'user-123',
        filePath: '/tmp/test_avatar.png',
      );

      // Assert
      expect(result, 'https://example.com/avatar.jpg');
      verify(() => mockStorageBucket.getPublicUrl(any())).called(1);
      verifyNever(() => mockStorageBucket.remove(any()));
    });

    test('should remove old avatar before uploading new one', () async {
      // Arrange - existing avatar
      const tExistingProfile = <String, dynamic>{
        'avatar_url': 'https://example.com/storage/v1/object/public/avatars/old/photo.jpg',
      };

      when(() => mockQueryBuilder.select(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.maybeSingle())
          .thenAnswer((_) => FakeNullableTransformBuilder(tExistingProfile));
      when(() => mockStorageBucket.remove(any()))
          .thenAnswer((_) async => []);
      when(() => mockStorageBucket.uploadBinary(any(), any(),
        fileOptions: any(named: 'fileOptions'),
      )).thenAnswer((_) async => '');
      when(() => mockStorageBucket.getPublicUrl(any()))
          .thenReturn('https://example.com/avatars/new.jpg');

      // Act
      final result = await dataSource.uploadAvatar(
        userId: 'user-123',
        filePath: '/tmp/test_avatar.png',
      );

      // Assert
      expect(result, 'https://example.com/avatars/new.jpg');
      verify(() => mockStorageBucket.remove(any())).called(1);
    });
  });
```

### 🔑 Claves del test de Storage

| Operación | Mock | Notas |
|-----------|------|-------|
| `supabase.storage` | `mockSupabase.storage` → `mockStorageClient` | Getter, con `thenReturn` |
| `.from('avatars')` | `mockStorageClient.from(any())` | `thenAnswer` → `mockStorageBucket` |
| `.uploadBinary()` | `mockStorageBucket.uploadBinary(any(), any(), ...)` | `thenAnswer` async |
| `.getPublicUrl()` | `mockStorageBucket.getPublicUrl(any())` | **Síncrono** — `thenReturn` |
| `.remove()` | `mockStorageBucket.remove(any())` | `thenAnswer` async |

---

## Ejercicio 9: Ejemplo completo - ProfileRemoteDataSource

### 📝 Tu Misión

Escribir el test completo para `ProfileRemoteDataSourceImpl` que integra todos los patrones anteriores.

### 🧪 Test completo

```dart
// test/features/profile/data/datasources/profile_remote_data_source_test.dart
import 'dart:async';
import 'dart:io';
import 'dart:typed_data';

import 'package:flutter_test/flutter_test.dart';
import 'package:mobile/core/error/exceptions.dart';
import 'package:mobile/features/profile/data/datasources/profile_remote_data_source.dart';
import 'package:mobile/features/profile/data/models/user_profile_model.dart';
import 'package:mocktail/mocktail.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

// ─── MOCKS ───

class MockSupabaseClient extends Mock implements SupabaseClient {}
class MockGoTrueClient extends Mock implements GoTrueClient {}
class MockSupabaseQueryBuilder extends Mock implements SupabaseQueryBuilder {}
class MockPostgrestFilterBuilder extends Mock
    implements PostgrestFilterBuilder<List<Map<String, dynamic>>> {}
class MockSupabaseStorageClient extends Mock implements SupabaseStorageClient {}
class MockStorageFileApi extends Mock implements StorageFileApi {}
class MockUserResponse extends Mock implements UserResponse {}

// ─── FAKES ───

class FakeTransformBuilder extends Fake
    implements PostgrestTransformBuilder<Map<String, dynamic>> {
  final Map<String, dynamic> data;
  FakeTransformBuilder(this.data);

  @override
  Future<T> then<T>(
    FutureOr<T> Function(Map<String, dynamic>) onValue, {
    Function? onError,
  }) =>
      Future<T>.value(onValue(data));
}

class FakeNullableTransformBuilder extends Fake
    implements PostgrestTransformBuilder<Map<String, dynamic>?> {
  final Map<String, dynamic>? data;
  FakeNullableTransformBuilder(this.data);

  @override
  Future<T> then<T>(
    FutureOr<T> Function(Map<String, dynamic>?) onValue, {
    Function? onError,
  }) =>
      Future<T>.value(onValue(data));
}

class FakeListTransformBuilder extends Fake
    implements PostgrestTransformBuilder<List<Map<String, dynamic>>> {
  final PostgrestTransformBuilder<Map<String, dynamic>> Function() _singleResult;

  FakeListTransformBuilder(this._singleResult);

  @override
  PostgrestTransformBuilder<Map<String, dynamic>> single() => _singleResult();
}

class AwaitableFilterBuilder extends Fake
    implements PostgrestFilterBuilder<List<Map<String, dynamic>>> {
  @override
  Future<T> then<T>(
    FutureOr<T> Function(List<Map<String, dynamic>>) onValue, {
    Function? onError,
  }) =>
      Future<T>.value(onValue([]));
}

// ─── TESTS ───

void main() {
  late ProfileRemoteDataSourceImpl dataSource;
  late MockSupabaseClient mockSupabase;
  late MockSupabaseQueryBuilder mockQueryBuilder;
  late MockPostgrestFilterBuilder mockFilterBuilder;
  late MockSupabaseStorageClient mockStorageClient;
  late MockStorageFileApi mockStorageBucket;

  const tUserId = 'user-123';
  const tProfileMap = <String, dynamic>{
    'id': 'profile-1',
    'user_id': tUserId,
    'full_name': 'Test User',
    'phone_number': '+584141234567',
    'email': 'test@example.com',
    'avatar_url': 'https://example.com/avatar.jpg',
    'preferred_language': 'es',
    'notifications_enabled': true,
    'created_at': '2024-01-15T10:00:00.000Z',
    'updated_at': '2024-01-15T10:00:00.000Z',
  };

  setUpAll(() {
    registerFallbackValue(MockSupabaseQueryBuilder());
    registerFallbackValue(MockPostgrestFilterBuilder());
    registerFallbackValue(Uint8List(0));
    registerFallbackValue(UserAttributes());
    registerFallbackValue(FileOptions());
  });

  setUp(() {
    mockSupabase = MockSupabaseClient();
    mockQueryBuilder = MockSupabaseQueryBuilder();
    mockFilterBuilder = MockPostgrestFilterBuilder();
    mockStorageClient = MockSupabaseStorageClient();
    mockStorageBucket = MockStorageFileApi();

    when(() => mockSupabase.from(any())).thenAnswer((_) => mockQueryBuilder);
    when(() => mockSupabase.storage).thenReturn(mockStorageClient);
    when(() => mockStorageClient.from(any())).thenReturn(mockStorageBucket);

    dataSource = ProfileRemoteDataSourceImpl(supabase: mockSupabase);
  });

  group('getProfile', () {
    test('should return UserProfileModel on success', () async {
      when(() => mockQueryBuilder.select(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.single())
          .thenAnswer((_) => FakeTransformBuilder(tProfileMap));

      final result = await dataSource.getProfile(tUserId);

      expect(result, isA<UserProfileModel>());
      expect(result.userId, tUserId);
      verify(() => mockSupabase.from('profiles')).called(1);
      verify(() => mockQueryBuilder.select()).called(1);
      verify(() => mockFilterBuilder.eq('user_id', tUserId)).called(1);
      verify(() => mockFilterBuilder.single()).called(1);
    });

    test('should throw ServerException on failure', () async {
      when(() => mockQueryBuilder.select(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenThrow(Exception('error'));

      try {
        await dataSource.getProfile(tUserId);
        fail('Should have thrown ServerException');
      } on Object catch (e) {
        expect(e, isA<ServerException>());
      }
    });
  });

  group('updateProfile', () {
    const tData = <String, dynamic>{'full_name': 'Updated Name'};

    test('should return updated UserProfileModel on success', () async {
      when(() => mockQueryBuilder.update(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.select(any())).thenAnswer(
        (_) => FakeListTransformBuilder(
          () => FakeTransformBuilder(tProfileMap),
        ),
      );

      final result = await dataSource.updateProfile(
        userId: tUserId,
        data: tData,
      );

      expect(result, isA<UserProfileModel>());
      expect(result.userId, tUserId);
      verify(() => mockSupabase.from('profiles')).called(1);
      verify(() => mockQueryBuilder.update(tData)).called(1);
      verify(() => mockFilterBuilder.eq('user_id', tUserId)).called(1);
      verify(() => mockFilterBuilder.select()).called(1);
    });
  });

  group('uploadAvatar', () {
    const tPublicUrl = 'https://example.com/avatars/new-avatar.jpg';
    final tFilePath = '${Directory.systemTemp.path}/test_avatar.png';

    setUp(() {
      File(tFilePath).writeAsBytesSync([1, 2, 3]);
    });

    tearDown(() {
      final f = File(tFilePath);
      if (f.existsSync()) f.deleteSync();
    });

    test('should return public URL without removing old avatar', () async {
      when(() => mockQueryBuilder.select(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.maybeSingle())
          .thenAnswer((_) => FakeNullableTransformBuilder(null));
      when(() => mockStorageBucket.uploadBinary(any(), any(),
        fileOptions: any(named: 'fileOptions'),
      )).thenAnswer((_) async => '');
      when(() => mockStorageBucket.getPublicUrl(any()))
          .thenReturn(tPublicUrl);

      final result = await dataSource.uploadAvatar(
        userId: tUserId,
        filePath: tFilePath,
      );

      expect(result, tPublicUrl);
      verifyNever(() => mockStorageBucket.remove(any()));
    });

    test('should remove old avatar before uploading', () async {
      const tOldAvatarUrl =
          'https://example.com/storage/v1/object/public/avatars/old/photo.jpg';
      const tExistingProfile = <String, dynamic>{
        'avatar_url': tOldAvatarUrl,
      };

      when(() => mockQueryBuilder.select(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.maybeSingle())
          .thenAnswer((_) => FakeNullableTransformBuilder(tExistingProfile));
      when(() => mockStorageBucket.remove(any()))
          .thenAnswer((_) async => []);
      when(() => mockStorageBucket.uploadBinary(any(), any(),
        fileOptions: any(named: 'fileOptions'),
      )).thenAnswer((_) async => '');
      when(() => mockStorageBucket.getPublicUrl(any()))
          .thenReturn(tPublicUrl);

      final result = await dataSource.uploadAvatar(
        userId: tUserId,
        filePath: tFilePath,
      );

      expect(result, tPublicUrl);
      verify(() => mockStorageBucket.remove(any())).called(1);
    });

    test('should throw ServerException on upload failure', () async {
      when(() => mockQueryBuilder.select(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.maybeSingle())
          .thenAnswer((_) => FakeNullableTransformBuilder(null));
      when(() => mockStorageBucket.uploadBinary(any(), any(),
        fileOptions: any(named: 'fileOptions'),
      )).thenThrow(Exception('upload error'));

      try {
        await dataSource.uploadAvatar(userId: tUserId, filePath: tFilePath);
        fail('Should have thrown ServerException');
      } on Object catch (e) {
        expect(e, isA<ServerException>());
      }
    });
  });

  group('updatePassword', () {
    test('should complete successfully', () async {
      final mockUserResponse = MockUserResponse();
      when(() => mockSupabase.auth).thenReturn(MockGoTrueClient());
      when(() => mockSupabase.auth.updateUser(any()))
          .thenAnswer((_) async => mockUserResponse);

      await dataSource.updatePassword('newPassword123');

      verify(() => mockSupabase.auth.updateUser(any())).called(1);
    });
  });
}
```

---

## Ejercicio 10: Ejemplo completo - PaymentMethodRemoteDataSource

### 📝 Tu Misión

Escribir el test para un DataSource con lógica más compleja: múltiples queries secuenciales y manejo de `is_default`.

### 📁 DataSource de ejemplo

```dart
class PaymentMethodRemoteDataSourceImpl implements PaymentMethodRemoteDataSource {
  final SupabaseClient supabase;

  PaymentMethodRemoteDataSourceImpl({required this.supabase});

  @override
  Future<List<PaymentMethodModel>> getPaymentMethods(String userId) async {
    try {
      final data = await supabase
          .from('payment_methods')
          .select()
          .eq('user_id', userId)
          .order('created_at', ascending: true);
      return data.map((json) => PaymentMethodModel.fromJson(json)).toList();
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<PaymentMethodModel> createPaymentMethod(
    Map<String, dynamic> data,
  ) async {
    try {
      final result = await supabase
          .from('payment_methods')
          .insert(data)
          .select()
          .single();
      return PaymentMethodModel.fromJson(result);
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<PaymentMethodModel> updatePaymentMethod({
    required String methodId,
    required Map<String, dynamic> data,
  }) async {
    try {
      // Si se está marcando como default, quitar default de los demás
      if (data['is_default'] == true) {
        await supabase
            .from('payment_methods')
            .update({'is_default': false})
            .neq('id', methodId);
      }

      final result = await supabase
          .from('payment_methods')
          .update(data)
          .eq('id', methodId)
          .select()
          .single();
      return PaymentMethodModel.fromJson(result);
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }

  @override
  Future<void> deletePaymentMethod(String methodId) async {
    try {
      await supabase
          .from('payment_methods')
          .delete()
          .eq('id', methodId);
    } catch (e) {
      throw ServerException(message: e.toString());
    }
  }
}
```

### 🧪 Tests

```dart
// test/features/profile/data/datasources/payment_method_remote_data_source_test.dart
void main() {
  late PaymentMethodRemoteDataSourceImpl dataSource;
  late MockSupabaseClient mockSupabase;
  late MockSupabaseQueryBuilder mockQueryBuilder;
  late MockPostgrestFilterBuilder mockFilterBuilder;

  const tUserId = 'user-123';
  const tMethodMap = <String, dynamic>{
    'id': 'method-001',
    'user_id': tUserId,
    'type': 'mobile',
    'name': 'Pago Móvil',
    'is_default': true,
    'created_at': '2024-01-15T10:00:00.000Z',
  };

  setUpAll(() {
    registerFallbackValue(MockSupabaseQueryBuilder());
    registerFallbackValue(MockPostgrestFilterBuilder());
  });

  setUp(() {
    mockSupabase = MockSupabaseClient();
    mockQueryBuilder = MockSupabaseQueryBuilder();
    mockFilterBuilder = MockPostgrestFilterBuilder();

    when(() => mockSupabase.from(any())).thenAnswer((_) => mockQueryBuilder);

    dataSource = PaymentMethodRemoteDataSourceImpl(supabase: mockSupabase);
  });

  group('getPaymentMethods', () {
    test('should return list of PaymentMethodModel', () async {
      // Arrange - SELECT .eq() con await directo (lista)
      when(() => mockQueryBuilder.select(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.order(any(), ascending: any(named: 'ascending')))
          .thenAnswer((_) => AwaitableFilterBuilder());

      // Act
      final result = await dataSource.getPaymentMethods(tUserId);

      // Assert
      expect(result, isA<List<PaymentMethodModel>>());
      verify(() => mockSupabase.from('payment_methods')).called(1);
      verify(() => mockQueryBuilder.select()).called(1);
      verify(() => mockFilterBuilder.eq('user_id', tUserId)).called(1);
    });
  });

  group('createPaymentMethod', () {
    test('should return created PaymentMethodModel', () async {
      when(() => mockQueryBuilder.insert(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.select(any())).thenAnswer(
        (_) => FakeListTransformBuilder(
          () => FakeTransformBuilder(tMethodMap),
        ),
      );

      final result = await dataSource.createPaymentMethod({
        'user_id': tUserId,
        'type': 'mobile',
        'name': 'Pago Móvil',
      });

      expect(result, isA<PaymentMethodModel>());
      expect(result.id, 'method-001');
    });
  });

  group('updatePaymentMethod', () {
    test('should reset defaults when setting is_default=true', () async {
      // Arrange - necesitamos 2 filter builders para las 2 queries
      final updateDefaultFilter = MockPostgrestFilterBuilder();
      final updateDataFilter = MockPostgrestFilterBuilder();

      when(mockQueryBuilder.update(any()))
          .thenAnswer((_) => updateDefaultFilter); // 1ra llamada
      when(() => updateDefaultFilter.neq(any(), any()))
          .thenAnswer((_) => AwaitableFilterBuilder());
      when(mockQueryBuilder.update(any()))
          .thenAnswer((_) => updateDataFilter); // 2da llamada
      when(() => updateDataFilter.eq(any(), any()))
          .thenAnswer((_) => updateDataFilter);
      when(() => updateDataFilter.select(any())).thenAnswer(
        (_) => FakeListTransformBuilder(
          () => FakeTransformBuilder(tMethodMap),
        ),
      );

      // Act
      final result = await dataSource.updatePaymentMethod(
        methodId: 'method-001',
        data: {'is_default': true},
      );

      // Assert
      expect(result, isA<PaymentMethodModel>());
      verify(() => mockSupabase.from('payment_methods')).called(2);
      verify(() => mockQueryBuilder.update({'is_default': false})).called(1);
    });

    test('should not reset defaults when is_default is not set', () async {
      when(() => mockQueryBuilder.update(any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.select(any())).thenAnswer(
        (_) => FakeListTransformBuilder(
          () => FakeTransformBuilder(tMethodMap),
        ),
      );

      final result = await dataSource.updatePaymentMethod(
        methodId: 'method-001',
        data: {'name': 'New Name'},
      );

      expect(result, isA<PaymentMethodModel>());
      verifyNever(() => mockFilterBuilder.neq(any(), any()));
    });
  });

  group('deletePaymentMethod', () {
    test('should delete successfully', () async {
      when(() => mockQueryBuilder.delete())
          .thenAnswer((_) => mockFilterBuilder);
      when(() => mockFilterBuilder.eq(any(), any()))
          .thenAnswer((_) => AwaitableFilterBuilder());

      await dataSource.deletePaymentMethod('method-001');

      verify(() => mockSupabase.from('payment_methods')).called(1);
      verify(() => mockQueryBuilder.delete()).called(1);
      verify(() => mockFilterBuilder.eq('id', 'method-001')).called(1);
    });
  });
}
```

---

## 🧪 Ejecuta todos los tests

```bash
# Test específico
flutter test test/features/profile/data/datasources/profile_remote_data_source_test.dart

# Todos los tests de data
flutter test test/features/

# Con coverage
flutter test --coverage test/features/
```

---

## ✅ Checklist de Ejercicios Completados

- [ ] Ejercicio 1: Configuración de mocks, fakes y fallback values
- [ ] Ejercicio 2: Auth DataSource (login, signOut, updatePassword)
- [ ] Ejercicio 3: SELECT con `.single()` (FakeTransformBuilder)
- [ ] Ejercicio 4: SELECT con `.maybeSingle()` (FakeNullableTransformBuilder)
- [ ] Ejercicio 5: UPDATE con retorno (FakeListTransformBuilder + FakeTransformBuilder)
- [ ] Ejercicio 6: INSERT con retorno
- [ ] Ejercicio 7: DELETE con await directo (AwaitableFilterBuilder)
- [ ] Ejercicio 8: Storage (uploadBinary, getPublicUrl, remove)
- [ ] Ejercicio 9: ProfileRemoteDataSource completo
- [ ] Ejercicio 10: PaymentMethodRemoteDataSource con lógica compleja
- [ ] **Total: 15+ tests** ejecutándose correctamente

---

## 🎉 ¡Felicitaciones!

Has aprendido a:

- ✅ Configurar Mocks de `SupabaseClient`, `GoTrueClient`, `SupabaseQueryBuilder`, `PostgrestFilterBuilder`, `SupabaseStorageClient` y `StorageFileApi`
- ✅ Implementar Fakes para `PostgrestTransformBuilder` en sus 4 variantes
- ✅ Testear operaciones de Auth (sin Fakes)
- ✅ Testear queries de base de datos (SELECT, INSERT, UPDATE, DELETE)
- ✅ Testear Storage (upload, getUrl, remove)
- ✅ Verificar interacciones precisas con `verify()`
- ✅ Manejar errores de Supabase como `ServerException`
- ✅ Escribir tests para DataSources con lógica compleja (múltiples queries)

---

## 🚀 Siguiente Paso

**Bonus:** [07b-practica-supabase-mock-http-client.md](./07b-practica-supabase-mock-http-client.md)

> Aprende a usar el paquete oficial `mock_supabase_http_client` como alternativa para tests de integración ligeros.
