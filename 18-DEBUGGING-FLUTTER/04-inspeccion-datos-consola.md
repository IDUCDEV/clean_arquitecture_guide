# 04 — Inspección de Datos y Debug Console

> Cómo inspeccionar variables, monitorear expresiones con WATCH y usar la Debug Console como REPL durante una sesión de debugging.

---

## 1. Inspeccionar durante debugging

Cuando la app se pausa en un breakpoint, VS Code te muestra información detallada sobre el estado del programa. Esta información se distribuye en tres áreas principales: el panel **VARIABLES**, el panel **WATCH** y la **Debug Console**.

---

## 2. Panel VARIABLES

Muestra las variables del scope actual. Se actualiza automáticamente cuando cambias de stack frame en CALL STACK.

### 2.1 Qué muestra

- **Local**: variables declaradas en la función actual
- **Closure**: variables capturadas por closures
- **Global**: variables globales del archivo
- **Fields**: campos de la instancia actual (si estás en un método)

### 2.2 Interactuar con variables

| Acción | Cómo | Qué hace |
|---|---|---|
| Expandir objeto | Click en flecha | Muestra campos internos |
| Ver valor | Hover sobre variable | Muestra tooltip con valor |
| Copiar valor | Click derecho > Copy Value | Copia el valor al clipboard |
| Copiar como expresión | Click derecho > Copy as Expression | Copia una expresión para usar en WATCH |
| Modificar valor | Click derecho > Set Value | Cambia el valor en tiempo real |
| Filtrar | `Ctrl+Alt+F` (Win/Linux) / `Alt+Cmd+F` (macOS) | Busca por nombre o valor |

### 2.3 Ejemplo de inspección

```dart
void _onLoginSubmitted(LoginSubmitted event, Emitter<LoginState> emit) {
  emit(LoginLoading());
  // BREAKPOINT AQUÍ
}
```

En VARIABLES verás:

```
event
  email: "usuario@ejemplo.com"
  password: "secreto123"
state
  LoginLoading (runtimeType)
this
  loginUseCase: LoginUseCase
    repository: AuthRepositoryImpl
```

### 2.4 Modificar variables en tiempo real

Imagina que quieres probar qué pasa si el email está vacío:

1. Click derecho en `event.email`
2. Seleccionar "Set Value"
3. Escribir `""` (string vacío)
4. Continuar con F5
5. La app usará el email vacío

Esto es extremadamente útil para:
- Probar edge cases sin modificar el código
- Simular datos inválidos
- Verificar que la validación funciona

---

## 3. Panel WATCH

Permite monitorear expresiones personalizadas que se evalúan en cada pausa.

### 3.1 Cómo agregar expresiones

1. En el panel WATCH, click en `+`
2. Escribir una expresión Dart válida
3. Presionar Enter

### 3.2 Ejemplos de expresiones en WATCH

```dart
// Ver el tipo del estado actual
state.runtimeType

// Ver la cantidad de items en una lista
state.items.length

// Ver si un usuario está autenticado
user != null

// Ver el total formateado
'\$${total.toStringAsFixed(2)}'

// Ver todos los nombres de usuarios
users.map((u) => u.name).toList()

// Ver el tiempo transcurrido
DateTime.now().difference(startTime).inSeconds

// Ver si un stream tiene listeners
streamController.hasListener
```

### 3.3 Consejos para WATCH

- **Expresiones Dart válidas**: puedes usar cualquier expresión que sea válida en Dart
- **Se evalúan en cada pausa**: si el valor cambia, se actualiza automáticamente
- **Puedes agregar múltiples expresiones**: no hay límite
- **Click derecho para opciones**: copiar resultado, remover expresión

---

## 4. Debug Console como REPL

La Debug Console es un REPL (Read-Eval-Print Loop) que te permite ejecutar código Dart en el contexto actual de la sesión de debugging.

### 4.1 Abrir la Debug Console

- `Ctrl+Shift+Y` (Windows/Linux)
- `Cmd+Shift+Y` (macOS)
- Click en "DEBUG CONSOLE" en el panel inferior

### 4.2 Qué puedes hacer

#### 1. Evaluar expresiones simples

```
> event.email
"usuario@ejemplo.com"

> state.runtimeType
"LoginLoading"

> items.length
42
```

#### 2. Llamar métodos

```
> user.toString()
"User(id: 123, name: Juan, email: juan@test.com)"

> items.isEmpty
true

> total.toStringAsFixed(2)
"1234.50"
```

#### 3. Ejecutar código complejo

```
> items.where((i) => i.price > 100).map((i) => i.name).toList()
["Laptop", "Tablet", "Monitor"]

> DateTime.now().difference(order.createdAt).inHours
48
```

#### 4. Modificar variables

```
> email = ""
> items = []
> user = null
```

#### 5. Invocar funciones

```
> await calculateTotal(items)
1500.00
```

### 4.3 Multiline input

Para escribir código en múltiples líneas:
1. Escribe la primera línea
2. Presiona `Shift+Enter` para nueva línea
3. Cuando termines, presiona `Enter` para ejecutar

Ejemplo:

```
> final result = items
    .where((i) => i.isActive)
    .map((i) => i.name)
    .toList();
> result
["Laptop", "Tablet"]
```

### 4.4 Sugerencias de autocompletado

La Debug Console soporta autocompletado:
- Escribe el nombre de una variable y presiona `Tab` o `Enter`
- Escribe `.` después de un objeto para ver métodos disponibles
- Usa `Ctrl+Space` para forzar autocompletado

---

## 5. Ejemplo práctico completo

### 5.1 Escenario

Tienes un BLoC de carrito y el total no es correcto. Quieres diagnosticar.

```dart
class CartBloc extends Bloc<CartEvent, CartState> {
  // ...
  Future<void> _onAddItem(AddItemToCart event, Emitter<CartState> emit) async {
    final currentState = state as CartLoaded;
    final updatedItems = [...currentState.items, event.item];
    final total = await calculateTotalUseCase(updatedItems);
    // BREAKPOINT AQUÍ
    emit(CartLoaded(items: updatedItems, total: total));
  }
}
```

### 5.2 Paso 1: Inspeccionar en VARIABLES

```
currentState
  items: [Item(Laptop, 999.99), Item(Mouse, 29.99)]
  total: 1029.98

event
  item: Item(Keyboard, 79.99)

updatedItems
  [Item(Laptop, 999.99), Item(Mouse, 29.99), Item(Keyboard, 79.99)]
```

### 5.3 Paso 2: Agregar a WATCH

```
updatedItems.length                    → 3
total                                  → 1109.97
updatedItems.map((i) => i.price).toList()  → [999.99, 29.99, 79.99]
```

### 5.4 Paso 3: Evaluar en Debug Console

```
> updatedItems.fold<double>(0, (sum, item) => sum + item.price)
1109.97

> total == updatedItems.fold<double>(0, (sum, item) => sum + item.price)
true
```

### 5.5 Paso 4: Modificar y probar

```
> event.item = Item(Keyboard, -10.00)
// Continuar con F5 y ver qué pasa con precio negativo
```

---

## 6. Inspeccionar objetos complejos

### 6.1 Listas

```
// En VARIABLES, expande la lista
items
  [0] → Item(Laptop, 999.99)
  [1] → Item(Mouse, 29.99)
  [2] → Item(Keyboard, 79.99)

// En Debug Console
> items[0].name
"Laptop"

> items.where((i) => i.price > 50).toList()
[Item(Laptop, 999.99), Item(Keyboard, 79.99)]
```

### 6.2 Mapas

```
// En VARIABLES
response
  "users" → List (3 items)
  "total" → 150
  "page" → 1

// En Debug Console
> response['users'].length
3

> (response['users'][0] as Map)['name']
"Juan"
```

### 6.3 Objetos con referencia circular

```
// Si un objeto tiene referencia circular, VS Code lo maneja
user
  id: 123
  name: "Juan"
  orders → [Order, Order, Order]
    [0]
      user → ⚙ [Circular]  // Muestra que es circular
```

---

## 7. Consejos avanzados

### 7.1 Usar Debug Console para testing rápido

Antes de crear un unit test, prueba la lógica en Debug Console:

```
> final result = validateEmail("test@test.com")
> result.isValid
true
```

### 7.2 Inspeccionar errores

```
> try { await apiCall(); } catch (e) { e.toString(); }
"SocketException: Connection timed out"
```

### 7.3 Verificar el estado de un BLoC

```
> bloc.state
CartLoaded(items: 3, total: 1109.97)

> bloc.state.runtimeType
"CartLoaded"

> bloc.isClosed
false
```

### 7.4 Medir tiempo de ejecución

```
> final sw = Stopwatch()..start();
> await heavyComputation();
> sw.stop();
> sw.elapsedMilliseconds
342
```

---

## Resumen

| Herramienta | Para qué | Atajo |
|---|---|---|
| VARIABLES | Ver/inspeccionar variables del scope actual | Click en panel |
| WATCH | Monitorear expresiones personalizadas | `+` en panel WATCH |
| Debug Console | Ejecutar código Dart en tiempo real | `Ctrl+Shift+Y` |
| Set Value | Modificar variables durante ejecución | Click derecho en VARIABLES |
| Copy as Expression | Copiar expresión para WATCH | Click derecho en VARIABLES |
| Filter Variables | Buscar variables por nombre/valor | `Ctrl+Alt+F` |

---

## 📚 Referencias

- [VS Code | Debugging](https://code.visualstudio.com/docs/editor/debugging) — Paneles VARIABLES, WATCH y Debug Console
- [Dart | `dart:developer`](https://api.dart.dev/stable/dart-developer/dart-developer-library.html) — Utilidades de debugging del SDK
- [Flutter | DevTools](https://docs.flutter.dev/tools/devtools) — Herramientas complementarias del ecosistema

---

> 📖 **Siguiente:** [05-multi-target-remoto.md](./05-multi-target-remoto.md) — Debugging multi-target, attach y trabajo remoto
