# 03 - Breakpoints Avanzados

## Tipos de breakpoints

VSCode soporta varios tipos de breakpoints, cada uno para un caso de uso especifico. Los breakpoints son la herramienta fundamental del debugging: pausan la ejecucion en un punto exacto del codigo para que puedas inspeccionar el estado.

---

## 1. Breakpoints basicos

### Como crearlos
- **Click en el gutter** (margen izquierdo del editor, junto al numero de linea)
- **F9** en la linea actual
- **Click derecho** > "Add Breakpoint"

### Visual
```
  15:   emit(LoginLoading());  // Circulo ROJO lleno = breakpoint activo
  16:   final result = await loginUseCase(params);
```

### Estados visuales
| Icono | Estado | Significado |
|---|---|---|
| Circulo rojo lleno | Activo | Pausara aqui |
| Circulo gris lleno | Disabled | Existe pero no pausa |
| Circulo gris hueco | No registrado | El debugger no puede registrar este breakpoint |

### Gestionar desde BREAKPOINTS section
En el panel lateral Run and Debug > BREAKPOINTS:
- Click en el circulo para habilitar/deshabilitar
- Click derecho para editar/eliminar
- Drag para reordenar

---

## 2. Breakpoints condicionales

Pausan solo cuando se cumple una condicion. Utiles cuando un breakpoint se ejecuta muchas veces pero solo te interesa una.

### Tipos de condicion

#### Expression (expresion)
Pausa cuando la expresion evalua a `true`.

**Crear:**
1. Click derecho en el gutter > "Add Conditional Breakpoint"
2. Seleccionar "Expression"
3. Escribir la expresion

**Ejemplos en Flutter:**

```dart
// Pausar solo cuando el email contiene "@gmail.com"
// Condicion: event.email.contains("@gmail.com")

// Pausar solo cuando el estado es error
// Condicion: state is LoginError

// Pausar solo cuando la lista tiene mas de 100 items
// Condicion: items.length > 100

// Pausar solo cuando un ID es especifico
// Condicion: user.id == "abc-123"
```

#### Hit count (conteo de veces)
Pausa despues de que el breakpoint se ejecuta N veces.

**Crear:**
1. Click derecho > "Add Conditional Breakpoint"
2. Seleccionar "Hit Count"
3. Escribir la condicion: `> 5`, `== 10`, `>= 100`

**Ejemplos:**

```
> 10    // Pausa despues de la 10a vez
== 1    // Pausa solo la primera vez
>= 50   // Pausa a partir de la 50a vez
```

**Caso de uso real**: Un listener se ejecuta en cada frame de animacion, pero solo quieres ver el estado en el frame 30.

#### Wait for breakpoint (triggered)
Pausa cuando OTRO breakpoint se activa primero.

**Crear:**
1. Click derecho > "Add Conditional Breakpoint"
2. Seleccionar "Wait for Breakpoint"
3. Seleccionar que breakpoint debe activarse primero

**Caso de uso real**: Quieres inspeccionar el estado DESPUES de que se ejecuta una funcion especifica.

---

## 3. Inline breakpoints

Pausan en una columna especifica de una linea. Utiles para codigo minificado o lineas con multiples statements.

### Como crearlos
- **Shift+F9** durante una sesion de debugging
- Click derecho > "Add Inline Breakpoint"

### Ejemplo

```dart
// Si esta linea tiene multiples statements:
return User(name: getName(), email: getEmail(), age: getAge());

// Un inline breakpoint pausa en un statement especifico:
return User(name: getName(), ← breakpoint aqui
            email: getEmail(),
            age: getAge());
```

### Visual
```
  42:   return User(name: getName(), │ email: getEmail(), │ age: getAge());
       └── breakpoint 1             └── breakpoint 2    └── breakpoint 3
```

---

## 4. Function breakpoints

Pausan cuando se invoca una funcion por nombre. Utiles cuando no tienes el source code o la funcion esta en un paquete externo.

### Como crearlos
1. En el panel BREAKPOINTS, click en el icono `+`
2. Seleccionar "Function Breakpoint"
3. Escribir el nombre de la funcion

### Ejemplos en Flutter

```
// Pausar cuando se llama setState
setState

// Pausar cuando se llama Navigator.push
Navigator.push

// Pausar cuando se llama print
print

// Pausar en un metodo de un paquete
http.get
```

### Visual
En el panel BREAKPOINTS aparece un triangulo rojo:
```
▲ setState
▲ Navigator.push
```

---

## 5. Data breakpoints

Pausan cuando el valor de una variable CAMBIA. Son extremadamente poderosos para encontrar donde se modifica un dato.

### Como crearlos
1. En el panel VARIABLES, busca la variable
2. Click derecho > "Break on Value Change"
3. Opciones: "Break on Value Change", "Break on Value Read", "Break on Access"

### Tipos

| Tipo | Que hace | Cuándo usar |
|---|---|---|
| Value Change | Pausa cuando el valor CAMBIA | Encontrar donde se modifica un dato |
| Value Read | Pausa cuando el valor SE LEE | Encontrar quien consume un dato |
| Value Access | Pausa cuando el valor SE ACCESA (read o write) | Auditoria completa de acceso |

### Ejemplo real

```dart
// Tienes un UserEntity con un campo 'name'
class UserEntity {
  String name;
  // ...
}

// Quieres saber QUIEN cambia el nombre del usuario
// 1. En VARIABLES, busca 'user'
// 2. Click derecho > "Break on Value Change" en 'name'
// 3. Ahora pausara cada vez que alguien haga user.name = "..."
```

### Visual
```
En el panel BREAKPOINTS aparece un hexagono rojo:
⬡ user.name (Change)
⬡ user.email (Read)
```

---

## 6. Logpoints (Breakpoints de logging)

No pausan la ejecucion. Solo imprimen un mensaje en la Debug Console. Son como `print()` pero sin modificar el codigo.

### Como crearlos
1. Click derecho en el gutter > "Add Logpoint"
2. Escribir el mensaje (puede incluir expresiones con `{}`)

### Ejemplos

```
// Log simple
"El usuario hizo login"

// Log con variable
"Email: {event.email}"

// Log con expresion compleja
"Estado: {state.runtimeType}, Items: {state.items.length}"

// Log condicional (solo si la expresion no es null)
"User ID: {user?.id ?? 'no user'}"
```

### Visual
```
  15:   emit(LoginLoading());  // Diamante AZUL = logpoint
  16:   final result = await loginUseCase(params);
```

### Comparacion con print()

| Aspecto | Logpoint | print() |
|---|---|---|
| Modifica el codigo | NO | SI |
| Se puede habilitar/deshabilitar | SI | NO |
| Tiene condiciones | SI | NO (hay que escribir if) |
| Se ve en Debug Console | SI | SI (en terminal) |
| Se commit a git | NO | SI (hay que eliminarlo) |

> **Regla**: Usa logpoints en lugar de print() para debugging temporal. No contaminan el codigo.

---

## Pratica guiada: breakpoints en un BLoC

### Escenario
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

    final total = await calculateTotalUseCase(updatedItems);  // LINEA 28

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

    final total = await calculateTotalUseCase(updatedItems);  // LINEA 43

    emit(CartLoaded(
      items: updatedItems,
      total: total,
    ));
  }
}
```

### Estrategia de debugging

**Breakpoint 1**: Condicion en linea 28
```
Condicion: event.item.price < 0
Mensaje: "Item con precio negativo detectado: {event.item.name}"
```
Esto pausa si alguien agrega un item con precio negativo.

**Breakpoint 2**: Logpoint en linea 43
```
Mensaje: "Calculando total para {updatedItems.length} items"
```
Esto te muestra cuantos items hay al momento de recalcular.

**Breakpoint 3**: Data breakpoint en `state.total`
```
Tipo: Value Change
```
Esto pausa cada vez que el total cambia, para ver quien lo modifica.

---

## Pratica: debugging de un stream

### Escenario
Un stream de Supabase no esta emitiendo los eventos esperados.

```dart
// En tu datasource
final stream = supabase
    .from('messages')
    .stream(primaryKey: ['id'])
    .order('created_at');

stream.listen((data) {
  // LINEA 8: Este listener no se ejecuta
  print('Nuevo mensaje: $data');
});
```

### Estrategia

**Breakpoint condicional** en linea 8:
```
Condicion: data.isEmpty
```
Esto pausa solo si llega un stream vacio (posible problema).

**Logpoint** antes del listen:
```
Mensaje: "Suscribiendose al stream de mensajes"
```

**Data breakpoint** en `data`:
```
Tipo: Value Change
```
Esto pausa cuando el stream emite nuevos datos.

---

## Resumen de tipos

| Tipo | Icono | Pausa? | Cuándo usar |
|---|---|---|---|
| Basico | Circulo rojo | SI | Punto de pausa general |
| Condicion - Expression | Circulo rojo + | SI | Cuando se cumple una condicion |
| Condicion - Hit Count | Circulo rojo + | SI | Despues de N veces |
| Triggered | Circulo rojo + | SI | Cuando otro breakpoint se activa |
| Inline | Circulo rojo pequeño | SI | En una columna especifica |
| Function | Triangulo rojo | SI | Cuando se llama una funcion |
| Data | Hexagono rojo | SI | Cuando cambia un valor |
| Logpoint | Diamante azul | NO | Logging sin pausar |

---

## Siguiente paso

Ve al [04-inspeccion-datos-consola.md](./04-inspeccion-datos-consola.md) para aprender a inspeccionar variables y evaluar expresiones.
