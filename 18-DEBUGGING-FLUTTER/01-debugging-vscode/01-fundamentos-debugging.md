# 01 - Fundamentos del Debugging en VSCode

## Que es debugging

Debugging es el proceso de **encontrar y corregir errores** en tu codigo. Pero no se trata solo de encontrar bugs: es entender el comportamiento de tu aplicacion en tiempo real, inspeccionar el estado del programa en cualquier momento y razonar sobre por que algo no funciona como esperabas.

El debugger es tu lupa para ver dentro de la maquina. Sin el, estas adivinando. Con el, estas **observando**.

---

## Por que debugging en Flutter es especial

Flutter tiene particularidades que lo hacen diferente de otros frameworks:

1. **Build methods**: se ejecutan muchas veces, no sabes cuando
2. **State management (BLoC/Cubit)**: el estado vive en objetos que se crean/destruyen
3. **Hot Reload**: cambia codigo sin reiniciar, pero el estado persiste
4. **Two threads**: UI thread (Dart) y Raster thread (GPU)
5. **Widgets son inmutables**: se recrean en cada rebuild

Esto significa que necesitas herramientas especificas para entender que esta pasando.

---

## Build Modes en Flutter

Flutter tiene 3 modos de compilacion, y cada uno impacta el debugging:

### Debug Mode
```
flutter run
```
- **Para que**: desarrollo diario
- **Optimizaciones**: NINGUNA (todo es lento)
- **Assertions**: HABILITADOS (validan contraints, invariantes)
- **Hot Reload**: SI funciona
- **Debugging**: COMPLETO (breakpoints, stepping, inspeccion)
- **Rendimiento**: NO REPRESENTATIVO (no medir performance aqui)

### Profile Mode
```
flutter run --profile
```
- **Para que**: medir performance real
- **Optimizaciones**: MAYORIA habilitadas
- **Assertions**: DESHABILITADOS
- **Hot Reload**: NO funciona (Hot Restart si)
- **Debugging**: PARCIAL (breakpoints si, pero mas lento)
- **Rendimiento**: REPRESENTATIVO (medir aqui)

### Release Mode
```
flutter run --release
flutter build apk
```
- **Para que**: produccion
- **Optimizaciones**: TODAS habilitadas
- **Assertions**: DESHABILITADOS
- **Hot Reload**: NO funciona
- **Debugging**: NO DISPONIBLE
- **Rendimiento**: OPTIMO

> **Regla de oro**: Para debugging usa `debug`. Para medir performance usa `profile`. Nunca midas performance en `debug`.

---

## Interfaz del Debugger de VSCode

Cuando presionas F5 y empieza una sesion de debugging, VSCode muestra 5 componentes principales:

```
┌─────────────────────────────────────────────────────────┐
│  1. Debug Toolbar (barra flotante)                      │
│  [▶ Continue] [⏭ Step Over] [↓ Step Into] [↑ Step Out] │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│  2. Run and Debug    │  Editor de codigo                │
│     View (sidebar)   │  (con breakpoints marcados)     │
│                      │                                  │
│  - CALL STACK        │                                  │
│  - VARIABLES         │                                  │
│  - WATCH             │                                  │
│  - BREAKPOINTS       │                                  │
│                      │                                  │
├──────────────────────┴──────────────────────────────────┤
│  3. Debug Console (panel inferior)                      │
│  > Output del debugger, expresiones evaluadas           │
├─────────────────────────────────────────────────────────┤
│  4. Status Bar (barra de estado - color naranja)        │
│  [Debug: flutter (debug)] ← indica sesion activa       │
└─────────────────────────────────────────────────────────┘
```

### Componentes detallados

#### 1. Debug Toolbar
Botones flotantes para controlar la sesion:

| Boton | Atajo | Que hace |
|---|---|---|
| Continue / Pause | `F5` | Reanuda hasta el proximo breakpoint, o pausa |
| Step Over | `F10` | Ejecuta la siguiente linea sin entrar en funciones |
| Step Into | `F11` | Entra en la siguiente funcion |
| Step Out | `Shift+F11` | Sale de la funcion actual |
| Restart | `Ctrl+Shift+F5` | Reinicia la sesion de debugging |
| Stop | `Shift+F5` | Detiene la sesion |

#### 2. Run and Debug View (Sidebar)
Panel izquierdo con 4 secciones:

- **CALL STACK**: Muestra la pila de llamadas. Cuando hay multi-target, cada sesion es un top-level element.
- **VARIABLES**: Variables locales y del scope actual. Se actualizan con el stack frame seleccionado.
- **WATCH**: Expresiones que defines para monitorear. Se evaluan en cada pausa.
- **BREAKPOINTS**: Lista de todos los breakpoints. Puedes habilitar/deshabilitar/eliminar.

#### 3. Debug Console
Panel inferior donde:
- Se muestra stdout/stderr del debugger
- Puedes evaluar expresiones Dart en tiempo real
- Funciona como REPL (Read-Eval-Print Loop)
- Soporta autocompletado y sintaxis

#### 4. Status Bar
Cuando hay una sesion activa, la barra de estado cambia a **color naranja** (o el color accent de tu tema). Muestra el nombre de la configuracion de debug activa.

---

## Flujo completo de debugging

```
1. Abrir proyecto en VSCode
   └── Asegurarse de que la extension Flutter esta instalada

2. Configurar launch.json (si es necesario)
   └── Ver archivo 02-configuracion-launch-json.md

3. Poner breakpoints
   └── Click en el gutter (margen izquierdo) o F9

4. Iniciar sesion
   └── F5 o Run > Start Debugging

5. Seleccionar dispositivo
   └── Emulador, simulador o dispositivo fisico

6. Ejecutar la accion que activa el bug
   └── La app se pausa en el breakpoint

7. Inspeccionar
   └── Variables, Watch, Call Stack, Debug Console

8. Navegar por el codigo
   └── Step Into, Step Over, Step Out

9. Encontrar el problema
   └── Modificar codigo si es necesario

10. Continuar ejecucion
    └── F5 para continuar, Shift+F5 para detener
```

---

## Ejemplo: primer breakpoint

Imagina que tienes un BLoC de login:

```dart
// lib/presentation/bloc/login/login_bloc.dart
class LoginBloc extends Bloc<LoginEvent, LoginState> {
  final LoginUseCase loginUseCase;

  LoginBloc({required this.loginUseCase}) : super(LoginInitial()) {
    on<LoginSubmitted>(_onLoginSubmitted);
  }

  Future<void> _onLoginSubmitted(
    LoginSubmitted event,
    Emitter<LoginState> emit,
  ) async {
    emit(LoginLoading());  // <-- PON AQUI UN BREAKPOINT (linea 15)

    final result = await loginUseCase(
      LoginParams(
        email: event.email,
        password: event.password,
      ),
    );

    result.fold(
      (failure) => emit(LoginError(failure.message)),  // <-- Y AQUI (linea 26)
      (user) => emit(LoginSuccess(user)),               // <-- Y AQUI (linea 27)
    );
  }
}
```

**Pasos:**

1. Haz click en el gutter de la linea 15 (aparece un circulo rojo)
2. Presiona F5
3. La app compila y se abre en el emulador
4. Escribe email y password, presiona "Login"
5. **La app se pausa** en la linea 15
6. En el panel VARIABLES veras `event.email` y `event.password`
7. Presiona F10 para avanzar linea por linea
8. Observa como el estado cambia de `LoginInitial` a `LoginLoading`

---

## Ejemplo: Debug Console

Durante una sesion, puedes abrir la Debug Console (`Ctrl+Shift+Y`) y escribir expresiones:

```dart
// En la Debug Console, puedes evaluar:
> event.email
"usuario@ejemplo.com"

> state.runtimeType
"LoginLoading"

> await loginUseCase(LoginParams(email: "test@test.com", password: "123"))
// Esto ejecuta el UseCase en tiempo real y te muestra el resultado
```

Esto es extremadamente util para:
- Verificar que un objeto tiene los valores esperados
- Ejecutar codigo sin modificar el archivo
- Probar comportamientos "que pasaria si..."

---

## Debugging con Hot Reload vs Hot Restart

### Hot Reload (`r` en terminal, o Ctrl+Shift+F5 en VSCode)
- **Que hace**: Reinyecta codigo Dart compilado sin reiniciar la app
- **Estado**: SE MANTIENE (BLoC, variables globales, etc.)
- **Breakpoints**: SE MANTIENEN
- **Uso**: Cambios visuales rapidos (colores, texto, layout)

### Hot Restart (`R` en terminal)
- **Que hace**: Reinicia completamente la app
- **Estado**: SE PIERDE todo
- **Breakpoints**: SE LIMPIAN (hay que volver a ponerlos)
- **Uso**: Cambios en initializers, main(), rutas, initState

> **Consejo**: Si tu bug depende del estado inicial de la app, usa Hot Restart. Si es un cambio visual, usa Hot Reload.

---

## Resumen

| Concepto | Descripcion |
|---|---|
| Debug Mode | Compilacion sin optimizaciones, debugging completo |
| Profile Mode | Compilaciones optimizadas, para medir performance |
| Release Mode | Produccion, sin debugging |
| F5 | Iniciar/continuar debugging |
| F9 | Toggle breakpoint |
| F10 | Step over |
| F11 | Step into |
| Shift+F11 | Step out |
| Debug Console | REPL para evaluar expresiones |
| Hot Reload | Cambio sin reiniciar, estado se mantiene |
| Hot Restart | Reinicio completo, estado se pierde |

---

## Siguiente paso

Ve al [02-configuracion-launch-json.md](./02-configuracion-launch-json.md) para aprender a configurar el `launch.json` completo para Flutter.
