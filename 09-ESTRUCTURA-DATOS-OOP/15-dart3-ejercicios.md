# Dart 3: Ejercicios Integradores

> 10 ejercicios que combinan sealed classes, pattern matching y records. Cada uno resuelve un problema real de desarrollo Flutter.

---

## Ejercicio 1: Sistema de notificaciones
**Nivel:** Básico | **Conceptos:** Sealed + Pattern Matching

### Enunciado
Implementa un sistema de notificaciones que pueda ser de diferentes tipos, cada uno con datos diferentes.

### Requisitos
- Crear sealed class `Notificacion`
- Tipos: `NotificacionTexto`, `NotificacionImagen`, `NotificacionAccion`
- Función que retorne un string descriptivo según el tipo
- Función que retorne si la notificación es urgente

```dart
// Tu código aquí
sealed class Notificacion { ... }

// Implementa las subclases
// Implementa las funciones
```

### Solución

```dart
sealed class Notificacion {
  final DateTime fecha;
  const Notificacion(this.fecha);
}

class NotificacionTexto extends Notificacion {
  final String titulo;
  final String cuerpo;
  NotificacionTexto({required this.titulo, required this.cuerpo, required super.fecha});
}

class NotificacionImagen extends Notificacion {
  final String titulo;
  final String urlImagen;
  NotificacionImagen({required this.titulo, required this.urlImagen, required super.fecha});
}

class NotificacionAccion extends Notificacion {
  final String titulo;
  final String textoAccion;
  final VoidCallback onAccion;
  NotificacionAccion({
    required this.titulo,
    required this.textoAccion,
    required this.onAccion,
    required super.fecha,
  });
}

String describir(Notificacion n) {
  return switch (n) {
    NotificacionTexto(titulo: final t, cuerpo: final c) => '$t: $c',
    NotificacionImagen(titulo: final t, urlImagen: final u) => '$t [imagen: $u]',
    NotificacionAccion(titulo: final t, textoAccion: final a) => '$t → Acción: $a',
  };
}

bool esUrgente(Notificacion n) {
  return switch (n) {
    NotificacionTexto(cuerpo: String c) when c.contains('urgente') => true,
    NotificacionAccion(textoAccion: 'Eliminar') => true,
    _ => false,
  };
}
```

---

## Ejercicio 2: Parser de comandos
**Nivel:** Básico | **Conceptos:** Sealed + Pattern Matching + Records

### Enunciado
Implementa un parser que convierta strings de comandos en objetos de tipo seguro.

### Requisitos
- Comandos: `login usuario contraseña`, `logout`, `search query`, `help`
- Retornar un record con el comando parseado y si fue exitoso
- Usar pattern matching para parsear

```dart
// Tu código aquí
// (ComandoParseado comando, bool exitoso) parsear(String input) { ... }
```

### Solución

```dart
sealed class Comando {
  const Comando();
}

class Login extends Comando {
  final String usuario;
  final String password;
  const Login(this.usuario, this.password);
}

class Logout extends Comando {
  const Logout();
}

class Search extends Comando {
  final String query;
  const Search(this.query);
}

class Help extends Comando {
  const Help();
}

(Comando comando, bool exitoso) parsear(String input) {
  final partes = input.trim().split(' ');

  return switch (partes) {
    ['login', String user, String pass] => (Login(user, pass), true),
    ['login', _] => (Help(), false), // Falta usuario o contraseña
    ['logout'] => (Logout(), true),
    ['search', ...rest] => (Search(rest.join(' ')), true),
    ['help'] => (Help(), true),
    _ => (Help(), false),
  };
}

// Uso
final (comando, ok) = parsear('login admin 1234');
if (ok) {
  switch (comando) {
    case Login(usuario: final u, password: final p):
      print('Logueando a $u');
    default:
      break;
  }
}
```

---

## Ejercicio 3: Validador de formularios
**Nivel:** Intermedio | **Conceptos:** Records + Pattern Matching

### Enunciado
Crea un validador que retorne resultados con errores específicos usando records.

### Requisitos
- Validar: nombre (requerido, 3-50 chars), email (@), edad (18-120)
- Retornar un record con si es válido y la lista de errores
- Cada error debe tener el campo y el mensaje

```dart
// Tu código aquí
```

### Solución

```dart
({bool valido, List<({String campo, String mensaje})> errores}) validarFormulario({
  required String nombre,
  required String email,
  required int edad,
}) {
  final errores = <({String campo, String mensaje})>[];

  if (nombre.isEmpty || nombre.length < 3 || nombre.length > 50) {
    errores.add((campo: 'nombre', mensaje: 'Debe tener 3-50 caracteres'));
  }

  if (!email.contains('@')) {
    errores.add((campo: 'email', mensaje: 'Debe ser un email válido'));
  }

  if (edad < 18 || edad > 120) {
    errores.add((campo: 'edad', mensaje: 'Debe ser entre 18 y 120'));
  }

  return (valido: errores.isEmpty, errores: errores);
}

// Uso
final result = validarFormulario(nombre: 'An', email: 'invalido', edad: 15);
if (!result.valido) {
  for (final (:campo, :mensaje) in result.errores) {
    print('$campo: $mensaje');
  }
}
```

---

## Ejercicio 4: Máquina de estados para login
**Nivel:** Intermedio | **Conceptos:** Sealed + Records

### Enunciado
Implementa una máquina de estados completa para un flujo de login.

### Requisitos
- Estados: `Initial`, `Loading`, `Authenticated(user)`, `Error(msg)`
- Transiciones con validación
- Retornar si la transición es válida

```dart
// Tu código aquí
sealed class LoginState { ... }
(LoginState nuevoEstado, bool valido) transicionar(LoginState actual, String accion) { ... }
```

### Solución

```dart
sealed class LoginState {}

class LoginInitial extends LoginState {}
class LoginLoading extends LoginState {}
class LoginAuthenticated extends LoginState {
  final String userId;
  LoginAuthenticated(this.userId);
}
class LoginError extends LoginState {
  final String message;
  LoginError(this.message);
}

(LoginState nuevoEstado, bool valido) transicionar(LoginState actual, String accion) {
  return switch ((actual, accion)) {
    (LoginInitial(), 'submit') => (LoginLoading(), true),
    (LoginLoading(), 'success') => (LoginAuthenticated('user_123'), true),
    (LoginLoading(), 'failure') => (LoginError('Credenciales inválidas'), true),
    (LoginError(), 'retry') => (LoginInitial(), true),
    _ => (actual, false),
  };
}
```

---

## Ejercicio 5: Calculadora con pattern matching
**Nivel:** Intermedio | **Conceptos:** Sealed + Pattern Matching + Records

### Enunciado
Implementa una calculadora que soporte operaciones con diferentes tipos de números.

### Requisitos
- Operaciones: Suma, Resta, Multiplicación, División
- Soportar enteros y decimales
- Retornar resultado con tipo dinámico (int o double)
- Manejar división por cero

```dart
// Tu código aquí
sealed class Operacion { ... }
({dynamic resultado, bool exito}) calcular(Operacion op) { ... }
```

### Solución

```dart
sealed class Operacion {
  const Operacion();
}

class Suma extends Operacion {
  final num a, b;
  const Suma(this.a, this.b);
}

class Resta extends Operacion {
  final num a, b;
  const Resta(this.a, this.b);
}

class Multiplicacion extends Operacion {
  final num a, b;
  const Multiplicacion(this.a, this.b);
}

class Division extends Operacion {
  final num a, b;
  const Division(this.a, this.b);
}

({dynamic resultado, bool exito}) calcular(Operacion op) {
  return switch (op) {
    Suma(a: final a, b: final b) => (resultado: a + b, exito: true),
    Resta(a: final a, b: final b) => (resultado: a - b, exito: true),
    Multiplicacion(a: final a, b: final b) => (resultado: a * b, exito: true),
    Division(_, b: 0) => (resultado: null, exito: false),
    Division(a: final a, b: final b) => (resultado: a / b, exito: true),
  };
}
```

---

## Ejercicio 6: Estado de descarga de archivo
**Nivel:** Intermedio | **Conceptos:** Sealed + Records

### Enunciado
Modela el estado de una descarga de archivo con progreso.

### Requisitos
- Estados: Idle, Downloading(porcentaje), Completed(ruta), Failed(error)
- Función que simule progreso
- Función que retorne si puede reintentar

```dart
// Tu código aquí
```

### Solución

```dart
sealed class DescargaEstado {}

class DescargaIdle extends DescargaEstado {}
class DescargaProgreso extends DescargaEstado {
  final double porcentaje;
  DescargaProgreso(this.porcentaje);
}
class DescargaCompleted extends DescargaEstado {
  final String ruta;
  DescargaCompleted(this.ruta);
}
class DescargaFailed extends DescargaEstado {
  final String error;
  final bool reintentable;
  DescargaFailed(this.error, {this.reintentable = true});
}

DescargaEstado siguienteEstado(DescargaEstado actual) {
  return switch (actual) {
    DescargaIdle() => DescargaProgreso(0),
    DescargaProgreso(porcentaje: < 100) => DescargaProgreso(actual.porcentaje + 25),
    DescargaProgreso() => DescargaCompleted('/downloads/archivo.pdf'),
    DescargaFailed(reintentable: true) => DescargaIdle(),
    DescargaFailed() => actual,
  };
}

bool puedeReintentar(DescargaEstado estado) {
  return switch (estado) {
    DescargaFailed(reintentable: final r) => r,
    _ => false,
  };
}
```

---

## Ejercicio 7: Parser de URLs
**Nivel:** Avanzado | **Conceptos:** Records + Pattern Matching + Destructuring

### Enunciado
Implementa un parser que extraiga componentes de URLs comunes de redes sociales.

### Requisitos
- Parsear URLs de Twitter/X, YouTube, Instagram
- Retornar record con tipo de plataforma y datos extraídos
- Manejar URLs inválidas

```dart
// Tu código aquí
({String plataforma, Map<String, String> datos}? resultado) parsearUrl(String url) { ... }
```

### Solución

```dart
({String plataforma, Map<String, String> datos})? parsearUrl(String url) {
  final uri = Uri.tryParse(url);
  if (uri == null) return null;

  return switch (uri.host) {
    'twitter.com' || 'x.com' => (
      plataforma: 'Twitter/X',
      datos: {'usuario': uri.pathSegments.firstOrNull ?? ''},
    ),
    'youtube.com' || 'youtu.be' => (
      plataforma: 'YouTube',
      datos: {'videoId': uri.host == 'youtu.be' ? uri.path.substring(1) : uri.queryParameters['v'] ?? ''},
    ),
    'instagram.com' => (
      plataforma: 'Instagram',
      datos: {'usuario': uri.pathSegments.firstOrNull ?? ''},
    ),
    _ => null,
  };
}

// Uso
final result = parsearUrl('https://twitter.com/flutter_dev');
if (result != null) {
  print('${result.plataforma}: ${result.datos}');
}
```

---

## Ejercicio 8: Eventos de UI con validación
**Nivel:** Avanzado | **Conceptos:** Sealed + Pattern Matching + Records

### Enunciado
Implementa un sistema de eventos de UI con validación automática.

### Requisitos
- Eventos: TextChanged, Submit, Clear, FocusChanged
- Cada evento tiene datos diferentes
- Función que valide si el evento es válido para un campo dado

```dart
// Tu código aquí
sealed class CampoEvento { ... }
({bool valido, String? razon}) validarEvento(CampoEvento evento, String tipoCampo) { ... }
```

### Solución

```dart
sealed class CampoEvento {
  final String campo;
  const CampoEvento(this.campo);
}

class TextChanged extends CampoEvento {
  final String texto;
  const TextChanged(super.campo, this.texto);
}

class Submit extends CampoEvento {
  const Submit(super.campo);
}

class Clear extends CampoEvento {
  const Clear(super.campo);
}

class FocusChanged extends CampoEvento {
  final bool tieneFocus;
  const FocusChanged(super.campo, this.tieneFocus);
}

({bool valido, String? razon}) validarEvento(CampoEvento evento, String tipoCampo) {
  return switch ((evento, tipoCampo)) {
    (TextChanged(texto: ''), 'email') => (valido: false, razon: 'Email no puede estar vacío'),
    (TextChanged(texto: final t), 'email') when !t.contains('@') => (valido: false, razon: 'Email inválido'),
    (TextChanged(texto: final t), 'nombre') when t.length < 3 => (valido: false, razon: 'Muy corto'),
    (Submit(), _) => (valido: true, razon: null),
    (Clear(), _) => (valido: true, razon: null),
    (FocusChanged(tieneFocus: false), _) => (valido: true, razon: null),
    _ => (valido: true, razon: null),
  };
}
```

---

## Ejercicio 9: Estado de conexión de red
**Nivel:** Avanzado | **Conceptos:** Sealed + Records + Pattern Matching

### Enunciado
Modela el estado de conexión de una app y sus transiciones.

### Requisitos
- Estados: Online, Offline, Connecting(timeout), Error(reintentable)
- Transiciones válidas entre estados
- Función que retorne si puede reconectar

```dart
// Tu código aquí
```

### Solución

```dart
sealed class ConexionEstado {}

class Online extends ConexionEstado {}
class Offline extends ConexionEstado {}
class Connecting extends ConexionEstado {
  final int intento;
  final int maxIntentos;
  Connecting(this.intento, {this.maxIntentos = 3});
}
class ConexionError extends ConexionEstado {
  final String mensaje;
  final bool reintentable;
  ConexionError(this.mensaje, {this.reintentable = true});
}

 ConexionEstado siguienteIntento(ConexionEstado actual) {
  return switch (actual) {
    Offline() => Connecting(1),
    Connecting(intento: final i, maxIntentos: final m) when i < m => Connecting(i + 1, maxIntentos: m),
    Connecting() => ConexionError('Máximo de intentos alcanzado', reintentable: false),
    ConexionError(reintentable: true) => Connecting(1),
    Online() => actual,
    ConexionError() => actual,
  };
}

bool puedeReconectar(ConexionEstado estado) {
  return switch (estado) {
    Offline() => true,
    ConexionError(reintentable: final r) => r,
    Connecting(intento: final i, maxIntentos: final m) => i < m,
    _ => false,
  };
}
```

---

## Ejercicio 10: Sistema de pedidos
**Nivel:** Avanzado | **Conceptos:** Sealed + Pattern Matching + Records + Destructuring

### Enunciado
Implementa un sistema de pedidos con diferentes estados y tipos de item.

### Requisitos
- Items: Producto, Descuento, Envío
- Estados del pedido: Pending, Processing, Shipped, Delivered, Cancelled
- Función que calcule el total con descuentos
- Función que retorne si puede cancelar

```dart
// Tu código aquí
sealed class ItemPedido { ... }
sealed class PedidoEstado { ... }
({double total, int itemCount}) calcularTotal(List<ItemPedido> items) { ... }
bool puedeCancelar(PedidoEstado estado) { ... }
```

### Solución

```dart
sealed class ItemPedido {
  final String nombre;
  const ItemPedido(this.nombre);
}

class Producto extends ItemPedido {
  final double precio;
  final int cantidad;
  Producto(super.nombre, this.precio, this.cantidad);
}

class Descuento extends ItemPedido {
  final double porcentaje;
  Descuento(super.nombre, this.porcentaje);
}

class Envio extends ItemPedido {
  final double costo;
  Envio(super.nombre, this.costo);
}

sealed class PedidoEstado {}

class Pending extends PedidoEstado {}
class Processing extends PedidoEstado {}
class Shipped extends PedidoEstado {
  final String tracking;
  Shipped(this.tracking);
}
class Delivered extends PedidoEstado {}
class Cancelled extends PedidoEstado {
  final String razon;
  Cancelled(this.razon);
}

({double total, int itemCount}) calcularTotal(List<ItemPedido> items) {
  double subtotal = 0;
  int itemCount = 0;
  double descuento = 0;
  double envio = 0;

  for (final item in items) {
    switch (item) {
      case Producto(precio: final p, cantidad: final c):
        subtotal += p * c;
        itemCount += c;
      case Descuento(porcentaje: final d):
        descuento = d;
      case Envio(costo: final c):
        envio = c;
    }
  }

  final total = (subtotal * (1 - descuento)) + envio;
  return (total: total, itemCount: itemCount);
}

bool puedeCancelar(PedidoEstado estado) {
  return switch (estado) {
    Pending() => true,
    Processing() => true,
    _ => false,
  };
}
```

---

## Resumen de conceptos practicados

| Ejercicio | Sealed | Pattern Matching | Records | Destructuring |
|-----------|--------|------------------|---------|---------------|
| 1. Notificaciones | ✅ | ✅ | | |
| 2. Parser comandos | ✅ | ✅ | ✅ | |
| 3. Validador forms | | ✅ | ✅ | ✅ |
| 4. Login states | ✅ | ✅ | ✅ | |
| 5. Calculadora | ✅ | ✅ | ✅ | |
| 6. Descarga | ✅ | ✅ | | |
| 7. Parser URLs | | ✅ | ✅ | |
| 8. Eventos UI | ✅ | ✅ | ✅ | |
| 9. Conexión red | ✅ | ✅ | | |
| 10. Sistema pedidos | ✅ | ✅ | ✅ | ✅ |

---

**Fin del módulo 09 — Dart 3**

→ Vuelve al [README del módulo 09](./README.md)
