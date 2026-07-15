# 07 - Debugger View

## Debugger View en DevTools

El Debugger View es una alternativa al debugging de VSCode pero integrado en DevTools. Ofrece funcionalidades similares pero con interfaz web.

---

## Pestañas del Debugger

| Pestaña | Propósito |
|---------|-----------|
| **Scripts** | Lista de scripts cargados |
| **Variables** | Variables del scope actual |
| **Watch** | Expresiones monitoreadas |
| **Call Stack** | Pila de llamadas |
| **Breakpoints** | Todos los breakpoints configurados |

---

## Diferencias entre VSCode Debugger y DevTools Debugger

| Feature | VSCode | DevTools |
|---------|--------|----------|
| Breakpoints de línea | ✅ | ✅ |
| Breakpoints condicionales | ✅ | ✅ |
| Log breakpoints | ✅ | ❌ |
| Function breakpoints | ✅ | ❌ |
| Watch expressions | ✅ | ✅ |
| Debug Console | ✅ (REPL) | ❌ (solo visual) |
| Hot Reload integrado | ✅ | ✅ |
| Inspección de widgets | ❌ | ✅ |
| Performance correlation | ❌ | ✅ |

**Recomendación**: Usar VSCode para debugging de código, DevTools para análisis visual y performance.

---

## Uso del Debugger en DevTools

### Cuándo usar DevTools Debugger
1. Cuando necesitas ver **contexto visual** (qué widgets están en pantalla)
2. Cuando quieres **correlacionar** breakpoints con performance
3. Para **debugging de layout** mientras inspeccionas código
4. Cuando VSCode no tiene acceso (deploy remoto)

### Cómo iniciar
1. Abrir DevTools
2. Ir a pestaña "Debugger"
3. Los breakpoints de VSCode se sincronizan automáticamente

---

## Breakpoints en DevTools

### Tipos soportados

| Tipo | Soportado | Cómo |
|------|-----------|------|
| Línea | ✅ | Click en gutter del código |
| Condicional | ✅ | Right-click → Expression |
| Hit count | ✅ | Right-click → Hit Count |
| Log message | ❌ | Usar VSCode |
| Function | ❌ | Usar VSCode |
| Data breakpoint | ❌ | Usar VSCode |

### Gestión de breakpoints

```
Breakpoints Panel:
├── auth_cubit.dart:45 ✓
├── product_screen.dart:78 ✓
├── api_client.dart:123 ✗ (deshabilitado)
└── router.dart:15 ✓
```

- **Click** en checkbox → habilitar/deshabilitar
- **Right-click** → condición o eliminar
- **Drag** → reordenar

---

## Variables en DevTools

### Panel de Variables

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

### Watch expressions

```
Watch:
├── state.runtimeType → "AuthSuccess"
├── state.props → [UserModel]
├── email.isEmpty → false
├── user.isValid() → true
└── products.length → 25
```

---

## Call Stack

### Estructura típica

```
Call Stack:
├── #0: AuthCubit.login  (auth_cubit.dart:45)
├── #1: AuthBloc._onLogin  (auth_bloc.dart:23)
├── #2: AuthBloc.onEvent  (auth_bloc.dart:15)
├── #3: Bloc._onTransition  (bloc.dart:456)
└── #4: Bloc._bindEventsToStates  (bloc.dart:312)
```

### Navegación
- **Click** en frame → ver código y variables de ese frame
- **Double-click** → saltar al archivo

---

## Correlación con Performance

### Flujo de trabajo

1. Performance View → identificar frame lento
2. Debugger → poner breakpoint en función sospechosa
3. Ejecutar → llegar al breakpoint
4. Variables → ver estado actual
5. Step through → identificar la línea problemática

### Ejemplo

```
Performance:
  Frame #1234: UI time 45ms (JANK!)
  → Flame Chart muestra: _buildProductsList: 38ms

Debugger:
  Breakpoint en _buildProductsList
  Step through:
    Line 23: for (var product in products)  ← Products tiene 10,000 items
    Line 24: widgets.add(ProductCard(product))  ← Se construye en cada iteración

Diagnóstico: Construir 10,000 widgets en cada frame
Fix: Usar ListView.builder para lazy loading
```

---

## Scripts Panel

### Lista de scripts cargados

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

### Filtrar
- **Filter**: buscar por nombre de archivo
- **Source**: filtrar por paquete o librería

---

## Tips para usar Debugger View

1. **Sincronizar con VSCode**: Los breakpoints se comparten
2. **Usar para layout debugging**: Correlacionar código con widget tree
3. **No usar para debugging extensivo**: VSCode es más rápido
4. **Usar para presentations**: Mostrar debugging en equipo
5. **Verificar estado de hot reload**: Si hot reload funciona, los breakpoints se mantienen

---
→ Siguiente: `08-logging-view.md`
