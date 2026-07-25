# 10: SOLID Explicite con Dart/Flutter

> SOLID no es teoría académica. Son 5 reglas que evitan que tu código sea un infierno para mantener.

---

## S — Single Responsibility Principle

**"Una clase, una razón para cambiar"**

```dart
// ❌ VIOLACIÓN: UserManager hace todo
class UserManager {
  void createUser(String name, String email) { /* crear */ }
  void sendWelcomeEmail(String email) { /* email */ }
  void saveToDatabase(User user) { /* guardar */ }
}

// ✅ CORRECTO: Cada clase tiene UNA responsabilidad
class CreateUserUseCase {
  final UserRepository _repo;
  final EmailService _email;

  CreateUserUseCase(this._repo, this._email);

  Future<void> call(String name, String email) async {
    final user = User(name: name, email: email);
    await _repo.save(user);
    await _email.sendWelcome(email);
  }
}
```

**Pregunta clave:** "Si esto cambia, ¿por qué razón cambió?"

---

## O — Open/Closed Principle

**"Abierto para extender, cerrado para modificar"**

```dart
// ❌ VIOLACIÓN: Para agregar un tipo nuevo, modificas el código
class NotificationSender {
  void send(Notification notif) {
    if (notif.type == 'email') { /* email */ }
    else if (notif.type == 'push') { /* push */ }
    // Agregar SMS = modificar esta clase
  }
}

// ✅ CORRECTO: Nuevos tipos sin modificar código existente
abstract class NotificationSender {
  void send(Notification notif);
}

class EmailSender implements NotificationSender {
  @override
  void send(Notification notif) { /* email */ }
}

class PushSender implements NotificationSender {
  @override
  void send(Notification notif) { /* push */ }
}

// Agregar SMS = crear nueva clase, NO modificar existente
class SmsSender implements NotificationSender {
  @override
  void send(Notification notif) { /* sms */ }
}
```

**Pregunta clave:** "¿Puedo agregar funcionalidad sin tocar código existente?"

---

## L — Liskov Substitution Principle

**"Los subtipos deben ser sustituibles por sus padres"**

```dart
// ❌ VIOLACIÓN: Quadrilateral y Square no son intercambiables
abstract class Shape {
  int get area;
}

class Rectangle implements Shape {
  int width, height;
  Rectangle(this.width, this.height);
  @override
  int get area => width * height;
}

class Square implements Rectangle {
  // Square fuerza width == height, rompiendo expectativas
}

// ✅ CORRECTO: Herencia que no rompe comportamiento
abstract class Shape {
  int get area;
}

class Rectangle implements Shape {
  int width, height;
  Rectangle(this.width, this.height);
  @override
  int get area => width * height;
}

class Square implements Shape {
  int side;
  Square(this.side);
  @override
  int get area => side * side;
}
```

**Pregunta clave:** "¿Puedo usar el subtipo donde espero el padre sin sorpresas?"

---

## I — Interface Segregation Principle

**"Ningún cliente debería depender de métodos que no usa"**

```dart
// ❌ VIOLACIÓN: Interfaz gigante obliga a implementar todo
abstract class UserRepository {
  Future<User> getUser(String id);
  Future<void> saveUser(User user);
  Future<void> deleteUser(String id);
  Future<List<User>> searchUsers(String query);
  Future<void> sendInvitation(String userId);
}

// ✅ CORRECTO: Interfaces pequeñas y específicas
abstract class UserReader {
  Future<User> getUser(String id);
}

abstract class UserWriter {
  Future<void> saveUser(User user);
  Future<void> deleteUser(String id);
}

abstract class UserSearcher {
  Future<List<User>> searchUsers(String query);
}

// Una implementación puede satisfacer múltiples interfaces
class SupabaseUserRepository implements UserReader, UserWriter, UserSearcher {
  @override
  Future<User> getUser(String id) async { /* ... */ }
  @override
  Future<void> saveUser(User user) async { /* ... */ }
  @override
  Future<void> deleteUser(String id) async { /* ... */ }
  @override
  Future<List<User>> searchUsers(String query) async { /* ... */ }
}
```

**Pregunta clave:** "¿Este cliente usa TODOS los métodos de esta interfaz?"

---

## D — Dependency Inversion Principle

**"Depende de abstracciones, no de concreciones"**

```dart
// ❌ VIOLACIÓN: Clase depende de implementación concreta
class UserRepository {
  final SupabaseClient _supabase = SupabaseClient('url', 'key');
  // Hardcoded dependency = imposible de testear
}

// ✅ CORRECTO: Depende de abstracción
abstract class UserRepository {
  Future<User> getUser(String id);
}

class SupabaseUserRepository implements UserRepository {
  final SupabaseClient _supabase;
  SupabaseUserRepository(this._supabase); // Inyectado

  @override
  Future<User> getUser(String id) async { /* ... */ }
}

// Para testing:
class MockUserRepository implements UserRepository {
  @override
  Future<User> getUser(String id) async => User(id: id, name: 'Test');
}

// Uso con DI (GetIt):
getIt.registerLazySingleton<UserRepository>(
  () => SupabaseUserRepository(getIt<SupabaseClient>()),
);
```

**Pregunta clave:** "¿Puedo cambiar la implementación sin modificar la clase que la usa?"

---

## Resumen SOLID en Dart

| Principio | Regla | Ejemplo Dart |
|-----------|-------|--------------|
| **S** | Una responsabilidad | UseCase = una acción |
| **O** | Extender sin modificar | Interface + implementaciones |
| **L** | Sustituibilidad | Subtipos no rompen comportamiento |
| **I** | Interfaces pequeñas | `UserReader`, `UserWriter` separados |
| **D** | Depender de abstracciones | Repository interface + DI |

---

## Test de SOLID

Para cada clase, pregunta:

```
□ S: ¿Esta clase tiene solo una razón para cambiar?
□ O: ¿Puedo agregar funcionalidad sin modificar esta clase?
□ L: ¿Puedo reemplazar esta clase por sus subtipos sin bugs?
□ I: ¿Esta interfaz tiene solo métodos que los clientes usan?
□ D: ¿Depende de abstracciones (interfaces) o de concreciones (clases)?
```

---

**Siguiente:** [11-anti-patrones-clean-architecture.md](./11-anti-patrones-clean-architecture.md)
