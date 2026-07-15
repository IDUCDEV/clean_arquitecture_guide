# 04 - Inspeccion de Datos y Debug Console

## Inspeccionar durante debugging

Cuando la app se pausa en un breakpoint, VSCode te muestra informacion detallada sobre el estado del programa. Esta informacion se distribuye en tres areas principales.

---

## Panel VARIABLES

Muestra las variables del scope actual. Se actualiza automaticamente cuando cambias de stack frame en CALL STACK.

### Que muestra
- **Local**: Variables declaradas en la funcion actual
- **Closure**: Variables capturadas por closures
- **Global**: Variables globales del archivo
- **Fields**: Campos de la instancia actual (si estas en un metodo)

### Interactuar con variables

| Accion | Como | Que hace |
|---|---|---|
| Expandir objeto | Click en flecha | Muestra campos internos |
| Ver valor | Hover sobre variable | Muestra tooltip con valor |
| Copiar valor | Click derecho > Copy Value | Copia el valor al clipboard |
| Copiar como expresion | Click derecho > Copy as Expression | Copia una expresion para usar en WATCH |
| Modificar valor | Click derecho > Set Value | Cambia el valor en tiempo real |
| Filtrar | `Alt+Cmd+F` (Mac) / `Ctrl+Alt+F` | Busca por nombre o valor |

### Ejemplo de inspeccion

```dart
void _onLoginSubmitted(LoginSubmitted event, Emitter<LoginState> emit) {
  emit(LoginLoading());
  // BREAKPOINT AQUI
}
```

En VARIABLES veras:
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

### Modificar variables en tiempo real

Imagina que quieres probar que pasa si el email esta vacio:

1. Click derecho en `event.email`
2. Seleccionar "Set Value"
3. Escribir `""` (string vacio)
4. Continuar con F5
5. La app usara el email vacio

Esto es extremadamente util para:
- Probar edge cases sin modificar el codigo
- Simular datos invalidos
- Verificar que la validacion funciona

---

## Panel WATCH

Permite monitorear expresiones personalizadas que se evaluan en cada pausa.

### Como agregar expresiones
1. En el panel WATCH, click en `+`
2. Escribir una expresion Dart valida
3. Presionar Enter

### Ejemplos de expresiones en WATCH

```dart
// Ver el tipo del estado actual
state.runtimeType

// Ver la cantidad de items en una lista
state.items.length

// Ver si un usuario esta autenticado
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

### Consejos para WATCH

- **Expresiones Dart validas**: Puedes usar cualquier expresion que sea valida en Dart
- **Se evaluan en cada pausa**: Si el valor cambia, se actualiza automaticamente
- **Puedes agregar multiples expresiones**: No hay limite
- **Click derecho para opciones**: Copiar resultado, remover expresion

---

## Debug Console REPL

La Debug Console es un REPL (Read-Eval-Print Loop) que te permite ejecutar codigo Dart en el contexto actual de la sesion de debugging.

### Abrir la Debug Console
- `Ctrl+Shift+Y` (Windows/Linux)
- `Cmd+Shift+Y` (Mac)
- Click en "DEBUG CONSOLE" en el panel inferior

### Que puedes hacer

#### 1. Evaluar expresiones simples
```
> event.email
"usuario@ejemplo.com"

> state.runtimeType
"LoginLoading"

> items.length
42
```

#### 2. Llamar metodos
```
> user.toString()
"User(id: 123, name: Juan, email: juan@test.com)"

> items.isEmpty
true

> total.toStringAsFixed(2)
"1234.50"
```

#### 3. Ejecutar codigo complejo
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

> await http.get(Uri.parse('https://api.example.com/users'))
Instance of 'Response'
```

### Multiline input
Para escribir codigo en multiples lineas:
1. Escribe la primera linea
2. Presiona `Shift+Enter` para nueva linea
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

### Sugerencias autocompletado
La Debug Console soporta autocompletado:
- Escribe el nombre de una variable y presiona `Tab` o `Enter`
- Escribe `.` despues de un objeto para ver metodos disponibles
- Usa `Ctrl+Space` para forzar autocompletado

---

## Ejemplo practico completo

### Escenario
Tienes un BLoC de carrito y el total no es correcto. Quieres diagnosticar.

```dart
class CartBloc extends Bloc<CartEvent, CartState> {
  // ...
  Future<void> _onAddItem(AddItemToCart event, Emitter<CartState> emit) async {
    final currentState = state as CartLoaded;
    final updatedItems = [...currentState.items, event.item];
    final total = await calculateTotalUseCase(updatedItems);
    // BREAKPOINT AQUI
    emit(CartLoaded(items: updatedItems, total: total));
  }
}
```

### Paso 1: Inspeccionar en VARIABLES
```
currentState
  items: [Item(Laptop, 999.99), Item(Mouse, 29.99)]
  total: 1029.98

event
  item: Item(Keyboard, 79.99)

updatedItems
  [Item(Laptop, 999.99), Item(Mouse, 29.99), Item(Keyboard, 79.99)]
```

### Paso 2: Agregar a WATCH
```
updatedItems.length                    → 3
total                                  → 1109.97
updatedItems.map((i) => i.price).toList()  → [999.99, 29.99, 79.99]
```

### Paso 3: Evaluar en Debug Console
```
> updatedItems.fold<double>(0, (sum, item) => sum + item.price)
1109.97

> total == updatedItems.fold<double>(0, (sum, item) => sum + item.price)
true
```

### Paso 4: Modificar y probar
```
> event.item = Item(Keyboard, -10.00)
// Continuar con F5 y ver que pasa con precio negativo
```

---

## Inspeccionar objetos complejos

### Listas
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

### Mapas
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

### Objetos con referencia circular
```
// Si un objeto tiene referencia circular, VSCode lo maneja
user
  id: 123
  name: "Juan"
  orders → [Order, Order, Order]
    [0]
      user → ⚙ [Circular]  // Muestra que es circular
```

---

## Consejos avanzados

### 1. Usar Debug Console para testing rapido
Antes de crear un unit test, prueba la logica en Debug Console:
```
> final result = validateEmail("test@test.com")
> result.isValid
true
```

### 2. Inspeccionar errores
```
> try { await apiCall(); } catch (e) { e.toString(); }
"SocketException: Connection timed out"
```

### 3. Verificar el estado de un BLoC
```
> bloc.state
CartLoaded(items: 3, total: 1109.97)

> bloc.state.runtimeType
"CartLoaded"

> bloc.isClosed
false
```

### 4. Medir tiempo de ejecucion
```
> final sw = Stopwatch()..start();
> await heavyComputation();
> sw.stop();
> sw.elapsedMilliseconds
342
```

---

## Resumen

| Herramienta | Para que | Atajo |
|---|---|---|
| VARIABLES | Ver/inspeccionar variables del scope actual | Click en panel |
| WATCH | Monitorear expresiones personalizadas | `+` en panel WATCH |
| Debug Console | Ejecutar codigo Dart en tiempo real | `Ctrl+Shift+Y` |
| Set Value | Modificar variables durante ejecucion | Click derecho en VARIABLES |
| Copy as Expression | Copiar expresion para WATCH | Click derecho en VARIABLES |
| Filter Variables | Buscar variables por nombre/valor | `Alt+Cmd+F` |

---

## Siguiente paso

Ve al [05-multi-target-remoto.md](./05-multi-target-remoto.md) para aprender sobre debugging multi-target y conceptos remotos.
