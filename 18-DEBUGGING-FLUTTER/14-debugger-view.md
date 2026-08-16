# 14 — Debugger View: Control de Ejecución

> El debugger integrado en DevTools: breakpoints, variables, watch expressions y correlación con performance.

---

## 1. Debugger View en DevTools

El Debugger View es una alternativa al debugging de VS Code pero integrado en DevTools. Comparte el mismo VM Service, así que los breakpoints que pongas en VS Code se sincronizan automáticamente.

---

## 2. Pestañas del Debugger

| Pestaña | Propósito |
|---|---|
| **Scripts** | Lista de scripts cargados |
| **Variables** | Variables del scope actual |
| **Watch** | Expresiones monitoreadas |
| **Call Stack** | Pila de llamadas |
| **Breakpoints** | Todos los breakpoints configurados |

---

## 3. Diferencias entre el Debugger de VS Code y el de DevTools

| Feature | VS Code | DevTools |
|---|---|---|
| Breakpoints de línea | ✅ | ✅ |
| Breakpoints condicionales | ✅ | ✅ |
| Logpoints | ✅ | ✅ |
| Watch expressions | ✅ | ✅ |
| Debug Console (REPL) | ✅ | ✅ |
| Hot reload integrado | ✅ | ✅ |
| Inspección de widgets | ❌ | ✅ |
| Correlación con performance | ❌ | ✅ |

**Recomendación:** usar VS Code para el día a día y DevTools cuando necesites contexto visual o correlación con performance.

---

## 4. Cuándo usar el Debugger de DevTools

1. Cuando necesitas ver **contexto visual** (qué widgets están en pantalla)
2. Cuando quieres **correlacionar** breakpoints con performance
3. Para **debugging de layout** mientras inspeccionas código
4. Cuando el debugging remoto no pasa por VS Code

### 4.1 Cómo iniciar

1. Abrir DevTools
2. Ir a la pestaña **Debugger**
3. Los breakpoints de VS Code se sincronizan automáticamente (mismo VM Service)

---

## 5. Breakpoints en DevTools

### 5.1 Tipos soportados

| Tipo | Soportado | Cómo |
|---|---|---|
| Línea | ✅ | Click en el gutter del código |
| Condicional | ✅ | Right-click → Expression |
| Hit count | ✅ | Right-click → Hit Count |
| Logpoint | ✅ | Right-click → Log Message |

### 5.2 Gestión de breakpoints

```
Breakpoints Panel:
├── auth_cubit.dart:45 ✓
├── product_screen.dart:78 ✓
├── api_client.dart:123 ✗ (deshabilitado)
└── router.dart:15 ✓
```

- **Click** en el checkbox → habilitar/deshabilitar
- **Right-click** → condición, hit count o eliminar

---

## 6. Variables en DevTools

### 6.1 Panel de Variables

```
Variables:
├── this: AuthCubit
│   ├── _state: AuthSuccess {user: UserModel}
│   ├── _loginUseCase: LoginUseCase
│   └── isClosed: false
├── email: "user@example.com"
├── password: "••••••••"
└── result: UserModel {id: 1, name: "John"}
```

### 6.2 Watch expressions

```
Watch:
├── state.runtimeType → "AuthSuccess"
├── state.props → [UserModel]
├── email.isEmpty → false
├── user.isValid() → true
└── products.length → 25
```

---

## 7. Call Stack

### 7.1 Estructura típica

```
Call Stack:
├── #0: AuthCubit.login  (auth_cubit.dart:45)
├── #1: AuthBloc._onLogin  (auth_bloc.dart:23)
├── #2: AuthBloc.onEvent  (auth_bloc.dart:15)
├── #3: Bloc._onTransition  (bloc.dart:456)
└── #4: Bloc._bindEventsToStates  (bloc.dart:312)
```

### 7.2 Navegación

- **Click** en un frame → ver código y variables de ese frame
- **Double-click** → saltar al archivo

---

## 8. Correlación con Performance

### 8.1 Flujo de trabajo

1. Performance View → identificar frame lento
2. Debugger → poner breakpoint en la función sospechosa
3. Ejecutar → llegar al breakpoint
4. Variables → ver el estado actual
5. Step through → identificar la línea problemática

### 8.2 Ejemplo

```
Performance:
  Frame #1234: UI time 45ms (JANK!)
  → Flame Chart muestra: _buildProductsList: 38ms

Debugger:
  Breakpoint en _buildProductsList
  Step through:
    Line 23: for (var product in products)  ← Products tiene 10,000 items
    Line 24: widgets.add(ProductCard(product))  ← Se construye en cada iteración

Diagnóstico: construir 10,000 widgets en cada frame
Fix: usar ListView.builder para lazy loading
```

---

## 9. Scripts Panel

### 9.1 Lista de scripts cargados

```
Scripts:
├── dart:core
├── dart:async
├── package:flutter/widgets.dart
├── package:flutter/material.dart
├── package:bloc/bloc.dart
├── lib/main.dart
├── lib/features/auth/presentation/cubit/auth_cubit.dart
├── lib/features/auth/data/repositories/auth_repository.dart
└── ...
```

### 9.2 Filtrar

- **Filter**: buscar por nombre de archivo
- **Source**: filtrar por paquete o librería

---

## 10. Tips para usar el Debugger View

1. **Sincronizar con VS Code**: los breakpoints se comparten (mismo VM Service)
2. **Usar para layout debugging**: correlacionar código con el widget tree
3. **No usarlo para debugging extensivo**: VS Code es más rápido para el día a día
4. **Usar para presentaciones**: mostrar debugging en equipo con la vista web
5. **Hot reload preserva breakpoints**: si hot reload funciona, los breakpoints se mantienen

---

## Resumen

| Concepto | Punto clave |
|---|---|
| Debugger View | Debugger web integrado en DevTools |
| Sincronización | Comparte breakpoints con VS Code |
| Variables/Watch | Inspeccionar estado y expresiones |
| Call Stack | Navegar la pila de llamadas |
| Uso ideal | Correlación de código con performance/layout |

---

## 📚 Referencias

- [Flutter | Debugger view](https://docs.flutter.dev/tools/devtools/debugger) — Documentación oficial del Debugger view
- [Dart | Observatory vs DevTools](https://docs.flutter.dev/tools/devtools/overview) — Visión general de DevTools

---

> 📖 **Siguiente:** [15-logging-view.md](./15-logging-view.md) — Logging view y estrategias de logging
