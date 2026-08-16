# 03 — Breakpoints Avanzados

> Todos los tipos de breakpoints que ofrece VS Code y cómo aplicarlos en un flujo de trabajo con BLoC/Cubit y streams.

---

## 1. Tipos de breakpoints

VS Code soporta varios tipos de breakpoints, cada uno para un caso de uso específico. Los breakpoints son la herramienta fundamental del debugging: pausan la ejecución en un punto exacto del código para que puedas inspeccionar el estado.

| Tipo | Pausa? | Cuándo usar |
|---|---|---|
| Básico (línea) | Sí | Punto de pausa general |
| Condicional (Expression) | Sí | Cuando se cumple una condición |
| Hit Count | Sí | Después de N ocurrencias |
| Triggered (Wait for) | Sí | Cuando otro breakpoint se activa primero |
| Inline | Sí | En una columna específica de una línea |
| Function | Sí | Cuando se llama una función por nombre |
| Data | Sí | Cuando cambia el valor de una variable |
| Logpoint | No | Logging sin pausar |

---

## 2. Breakpoints básicos

### 2.1 Cómo crearlos

- **Click en el gutter** (margen izquierdo del editor, junto al número de línea)
- **F9** en la línea actual
- **Click derecho** > "Add Breakpoint"

### 2.2 Visual

```
  15:   emit(LoginLoading());  // Círculo ROJO lleno = breakpoint activo
  16:   final result = await loginUseCase(params);
```

### 2.3 Estados visuales

| Icono | Estado | Significado |
|---|---|---|
| Círculo rojo lleno | Activo | Pausará aquí |
| Círculo gris lleno | Disabled | Existe pero no pausa |
| Círculo gris hueco | No registrado | El debugger no puede registrar este breakpoint |

### 2.4 Gestionar desde la sección BREAKPOINTS

En el panel lateral Run and Debug > BREAKPOINTS:
- Click en el círculo para habilitar/deshabilitar
- Click derecho para editar/eliminar
- Drag para reordenar

---

## 3. Breakpoints condicionales

Pausan solo cuando se cumple una condición. Útiles cuando un breakpoint se ejecuta muchas veces pero solo te interesa una.

### 3.1 Expression (expresión)

Pausa cuando la expresión evalúa a `true`.

**Crear:**
1. Click derecho en el gutter > "Add Conditional Breakpoint"
2. Seleccionar "Expression"
3. Escribir la expresión

**Ejemplos en Flutter:**

```dart
// Pausar solo cuando el email contiene "@gmail.com"
// Condición: event.email.contains("@gmail.com")

// Pausar solo cuando el estado es error
// Condición: state is LoginError

// Pausar solo cuando la lista tiene más de 100 items
// Condición: items.length > 100

// Pausar solo cuando un ID es específico
// Condición: user.id == "abc-123"
```

### 3.2 Hit count (conteo de veces)

Pausa después de que el breakpoint se ejecuta N veces.

**Crear:**
1. Click derecho > "Add Conditional Breakpoint"
2. Seleccionar "Hit Count"
3. Escribir la condición: `> 5`, `== 10`, `>= 100`

**Ejemplos:**

```
> 10    // Pausa después de la 10.ª vez
== 1    // Pausa solo la primera vez
>= 50   // Pausa a partir de la 50.ª vez
```

**Caso de uso real**: un listener se ejecuta en cada frame de animación, pero solo quieres ver el estado en el frame 30.

### 3.3 Wait for breakpoint (triggered)

Pausa cuando OTRO breakpoint se activa primero.

**Crear:**
1. Click derecho > "Add Conditional Breakpoint"
2. Seleccionar "Wait for Breakpoint"
3. Seleccionar qué breakpoint debe activarse primero

**Caso de uso real**: quieres inspeccionar el estado DESPUÉS de que se ejecuta una función específica.

---

## 4. Inline breakpoints

Pausan en una columna específica de una línea. Útiles para líneas con múltiples statements.

### 4.1 Cómo crearlos

- **Ctrl+Shift+F9** (Windows/Linux) o **Shift+F9** (macOS) durante una sesión de debugging
- Click derecho > "Add Inline Breakpoint"

### 4.2 Ejemplo

```dart
// Si esta línea tiene múltiples statements:
return User(name: getName(), email: getEmail(), age: getAge());

// Un inline breakpoint pausa en un statement específico:
return User(name: getName(), ← breakpoint aquí
            email: getEmail(),
            age: getAge());
```

### 4.3 Visual

```
  42:   return User(name: getName(), │ email: getEmail(), │ age: getAge());
       └── breakpoint 1             └── breakpoint 2    └── breakpoint 3
```

---

## 5. Function breakpoints

Pausan cuando se invoca una función por nombre. Útiles cuando no tienes el source code o la función está en un paquete externo.

### 5.1 Cómo crearlos

1. En el panel BREAKPOINTS, click en el icono `+`
2. Seleccionar "Function Breakpoint"
3. Escribir el nombre de la función

### 5.2 Ejemplos en Flutter

```
// Pausar cuando se llama setState
setState

// Pausar cuando se llama Navigator.push
Navigator.push

// Pausar cuando se llama print
print

// Pausar en un método de un paquete
http.get
```

> **Nota**: el soporte de function breakpoints depende del debugger. En el debugger de Dart funciona mejor con nombres completos; si no se resuelve, usa un breakpoint de línea en la primera línea de la función.

### 5.3 Visual

En el panel BREAKPOINTS aparece un triángulo rojo:

```
▲ setState
▲ Navigator.push
```

---

## 6. Data breakpoints

Pausan cuando el valor de una variable CAMBIA. Son extremadamente poderosos para encontrar dónde se modifica un dato.

### 6.1 Cómo crearlos

1. En el panel VARIABLES, busca la variable
2. Click derecho > "Break on Value Change"
3. Opciones: "Break on Value Change", "Break on Value Read", "Break on Access"

### 6.2 Tipos

| Tipo | Qué hace | Cuándo usar |
|---|---|---|
| Value Change | Pausa cuando el valor CAMBIA | Encontrar dónde se modifica un dato |
| Value Read | Pausa cuando el valor SE LEE | Encontrar quién consume un dato |
| Value Access | Pausa cuando el valor SE ACCESA (read o write) | Auditoría completa de acceso |

> **Nota**: los data breakpoints requieren soporte del debugger y de la plataforma. En Flutter el debugger de Dart tiene soporte limitado; si no está disponible para tu configuración, usa breakpoints condicionales en las líneas de escritura como alternativa.

### 6.3 Ejemplo real

```dart
// Tienes un UserEntity con un campo 'name'
class UserEntity {
  String name;
  // ...
}

// Quieres saber QUIÉN cambia el nombre del usuario
// 1. En VARIABLES, busca 'user'
// 2. Click derecho > "Break on Value Change" en 'name'
// 3. Ahora pausará cada vez que alguien haga user.name = "..."
```

### 6.4 Visual

```
En el panel BREAKPOINTS aparece un hexágono rojo:
⬡ user.name (Change)
⬡ user.email (Read)
```

---

## 7. Logpoints (breakpoints de logging)

No pausan la ejecución. Solo imprimen un mensaje en la Debug Console. Son como `print()` pero sin modificar el código.

### 7.1 Cómo crearlos

1. Click derecho en el gutter > "Add Logpoint"
2. Escribir el mensaje (puede incluir expresiones con `{}`)

### 7.2 Ejemplos

```
// Log simple
"El usuario hizo login"

// Log con variable
"Email: {event.email}"

// Log con expresión compleja
"Estado: {state.runtimeType}, Items: {state.items.length}"

// Log condicional (solo si la expresión no es null)
"User ID: {user?.id ?? 'no user'}"
```

### 7.3 Visual

```
  15:   emit(LoginLoading());  // Diamante AZUL = logpoint
  16:   final result = await loginUseCase(params);
```

### 7.4 Comparación con print()

| Aspecto | Logpoint | print() |
|---|---|---|
| Modifica el código | NO | SÍ |
| Se puede habilitar/deshabilitar | SÍ | NO |
| Tiene condiciones | SÍ | NO (hay que escribir if) |
| Se ve en Debug Console | SÍ | SÍ (en terminal) |
| Se commit a git | NO | SÍ (hay que eliminarlo) |

> **Regla**: usa logpoints en lugar de `print()` para debugging temporal. No contaminan el código.

---

## 8. Práctica guiada: breakpoints en un BLoC

### 8.1 Escenario

Tienes un BLoC de carrito de compras y el total no se calcula correctamente.

```dart
// lib/presentation/bloc/cart/cart_bloc.dart
class CartBloc extends Bloc<CartEvent, CartState> {
  final CalculateTotalUseCase calculateTotalUseCase;

  CartBloc({required this.calculateTotalUseCase}) : super(CartInitial()) {
    on<AddItemToCart>(_onAddItem);
    on<RemoveItemFromCart>(_onRemoveItem);
    on<RecalculateTotal>(_onRecalculate);
  }

  Future<void> _onAddItem(
    AddItemToCart event,
    Emitter<CartState> emit,
  ) async {
    final currentState = state as CartLoaded;
    final updatedItems = [...currentState.items, event.item];

    final total = await calculateTotalUseCase(updatedItems);  // LÍNEA 28

    emit(CartLoaded(
      items: updatedItems,
      total: total,
    ));
  }

  Future<void> _onRemoveItem(
    RemoveItemFromCart event,
    Emitter<CartState> emit,
  ) async {
    final currentState = state as CartLoaded;
    final updatedItems = currentState.items
        .where((item) => item.id != event.itemId)
        .toList();

    final total = await calculateTotalUseCase(updatedItems);  // LÍNEA 43

    emit(CartLoaded(
      items: updatedItems,
      total: total,
    ));
  }
}
```

### 8.2 Estrategia de debugging

**Breakpoint 1**: Condición en línea 28
```
Condición: event.item.price < 0
Mensaje: "Item con precio negativo detectado: {event.item.name}"
```
Esto pausa si alguien agrega un item con precio negativo.

**Breakpoint 2**: Logpoint en línea 43
```
Mensaje: "Calculando total para {updatedItems.length} items"
```
Esto te muestra cuántos items hay al momento de recalcular.

**Breakpoint 3**: Condicional en `total` (línea donde se emite el estado)
```
Condición: total < 0
```
Esto pausa si el total calculado es inválido.

---

## 9. Práctica: debugging de un stream

### 9.1 Escenario

Un stream de Supabase no está emitiendo los eventos esperados.

```dart
// En tu datasource
final stream = supabase
    .from('messages')
    .stream(primaryKey: ['id'])
    .order('created_at');

stream.listen((data) {
  // LÍNEA 8: Este listener no se ejecuta
  debugPrint('Nuevo mensaje: $data');
});
```

### 9.2 Estrategia

**Breakpoint condicional** en línea 8:
```
Condición: data.isEmpty
```
Esto pausa solo si llega un stream vacío (posible problema).

**Logpoint** antes del listen:
```
Mensaje: "Suscribiéndose al stream de mensajes"
```

**Breakpoint de línea** en el `listen`:
Esto pausa cada vez que el stream emite nuevos datos (para confirmar que los eventos llegan).

---

## Resumen

| Tipo | Pausa? | Cuándo usar |
|---|---|---|
| Básico | Sí | Punto de pausa general |
| Condición - Expression | Sí | Cuando se cumple una condición |
| Condición - Hit Count | Sí | Después de N veces |
| Triggered | Sí | Cuando otro breakpoint se activa |
| Inline | Sí | En una columna específica |
| Function | Sí | Cuando se llama una función |
| Data | Sí (soporte limitado) | Cuando cambia un valor |
| Logpoint | No | Logging sin pausar |

---

## 📚 Referencias

- [VS Code | Breakpoints](https://code.visualstudio.com/docs/editor/debugging#_breakpoints) — Tipos de breakpoints en VS Code
- [Dart-Code | Debugging](https://dartcode.org/docs/debugging/) — Detalles del debugger Dart/Flutter
- [VS Code | Keyboard shortcuts](https://code.visualstudio.com/docs/getstarted/keybindings) — Cómo personalizar atajos

---

> 📖 **Siguiente:** [04-inspeccion-datos-consola.md](./04-inspeccion-datos-consola.md) — Inspeccionar variables y evaluar expresiones en la Debug Console
