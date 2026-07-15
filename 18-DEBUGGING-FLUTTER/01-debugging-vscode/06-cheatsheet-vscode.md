# 06 - Cheatsheet: Debugging en VSCode

## Atajos de teclado esenciales

| Atajo | Acción | Descripción |
|-------|--------|-------------|
| `F5` | Start/Resume | Iniciar depuración o continuar |
| `Ctrl+Shift+F5` | Restart | Reiniciar depuración |
| `F10` | Step Over | Ejecutar siguiente línea sin entrar |
| `F11` | Step Into | Entrar dentro de función/método |
| `Shift+F11` | Step Out | Salir de función actual |
| `Ctrl+Shift+F10` | Run to Cursor | Ejecutar hasta cursor |
| `Shift+F5` | Stop | Detener depuración |
| `F9` | Toggle Breakpoint | Agregar/quitar breakpoint |
| `Ctrl+F9` | Disable BP | Deshabilitar breakpoint sin eliminar |
| `Ctrl+Shift+F9` | Disable All BPs | Deshabilitar todos los breakpoints |
| `Alt+F9` | Conditional BP | Breakpoint condicional |
| `F7` | Step Into Target | Saltar a target de widget (Flutter) |

### Navegación de paneles

| Atajo | Panel |
|-------|-------|
| `Ctrl+Shift+D` | Debug sidebar |
| `Ctrl+Shift+Y` | Debug console |
| `Ctrl+Shift+E` | Explorer |
| `Ctrl+Shift+F` | Search |
| `Ctrl+Shift+G` | Source Control |

---

## Iconos del panel VARIABLES

| Icono | Tipo | Ejemplo |
|-------|------|---------|
| 🔵 `=` | Variable local | `email = "test@mail.com"` |
| 🟢 `→` | Getter calculado | `→ isValid` |
| 🔴 `×` | Variable eliminada (scope muerto) | `× tempVar` |
| ⚪ `○` | Propiedad de objeto | `○ name` en `User` |
| 🟡 `●` | Campo privado | `● _counter` |

### Iconos del CALL STACK

| Icono | Significado |
|-------|-------------|
| ▶ | Frame actual (punto de ejecución) |
| ⏸ | Frame pausado en breakpoint |
| 🧵 | Hilo de ejecución |
| 📦 | Isolate |

---

## Sintaxis de Watches (expresiones)

### Acceso a propiedades
```
variable.property
variable.property.subProperty
```

### Índices y colecciones
```
myList[0]
myMap["key"]
mySet.first
```

### Métodos de inspección
```
myVariable.toString()
myVariable.runtimeType
myList.length
myList.isEmpty
myMap.keys.toList()
```

### Operaciones condicionales
```
counter > 0 ? "positive" : "negative"
user?.name ?? "Anonymous"
list.isNotEmpty
```

### Llamadas a métodos (cuidado: side effects)
```
user.isValid()
controller.text
```

### Ver todo un objeto
```
// Variables > expandir > click en "..." al final
// O en Debug Console:
MyClass { _name: "x", _age: 25, id: 42 }
```

---

## Tipos de breakpoints - Referencia rápida

| Tipo | Icono | Cómo crearlo | Cuándo usarlo |
|------|-------|--------------|---------------|
| Línea | 🔴 | Click gutter o F9 | Punto parada básica |
| Condicional | 🔴+📝 | Right-click → Conditional | Cuando se cumple expresión |
| Hit Count | 🔴+🔢 | Right-click → Hit Count | Cada N ocurrencias |
| Log Message | 🟢 | Right-click → Log Message | Logging sin pausar |
| Function | 🔵 | Right-click → Function Break | Al entrar a función |
| Data Breakpoint | 🔷 | Variables > Right-click | Cuando cambia valor |

---

## launch.json - Plantillas comunes

### Debug Flutter básico
```json
{
  "name": "Flutter Debug",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart"
}
```

### Flutter con args Dart
```json
{
  "name": "Flutter + Args",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "args": ["--dart-define=ENV=dev"]
}
```

### Flutter test
```json
{
  "name": "Debug Test",
  "type": "dart",
  "request": "launch",
  "program": "test/widget_test.dart",
  "args": ["--name", "test name"]
}
```

### Attach a proceso existente
```json
{
  "name": "Attach",
  "type": "dart",
  "request": "attach",
  "vmServiceUri": "${env:FLUTTER_VM_SERVICE_URI}"
}
```

### Multiple targets (compound)
```json
{
  "compounds": [
    {
      "name": "App + Worker",
      "configurations": ["Flutter App", "Dart Worker"]
    }
  ]
}
```

---

## Debug Console - Comandos útiles

### Inspección directa
```dart
// Ver tipo de variable
MyClass → instance of 'MyClass'

// Expandir objeto completo
// Click en ">" junto al valor en Variables

// Ver contenido de lista
myList → [1, 2, 3, 4, 5]

// Ver contenido de mapa
myMap → { "key": "value", "count": 42 }
```

### Expresiones evaluables
```dart
// Operaciones matemáticas
counter + 1
items.length * 2

// Strings
"Count: $counter"
user.name.toUpperCase()

// Condicionales
isActive && isVerified ? "Active User" : "Pending"

// Colecciones
users.where((u) => u.age > 18).toList()
products.map((p) => p.name).join(", ")
```

### Llamadas con side effects (usar con cuidado)
```dart
// Imprimir valor sin println (se ve en consola)
print("DEBUG: $variable")

// Llamar método getter
controller.text
```

---

## Hot Reload durante debugging

| Acción | Comando | Efecto |
|--------|---------|--------|
| Hot Reload | `Ctrl+F5` o `r` en terminal | Mantiene estado, actualiza UI |
| Hot Restart | `Ctrl+Shift+F5` o `R` en terminal | Resetea estado completo |
| Restart desde UI | Botón 🔄 en Debug toolbar | Mismo que Hot Restart |

### Hot Reload preserva:
- Estado actual de BLoC/Cubit/Provider
- Posición de scroll
- Contenido de campos de texto
- Resultado de cálculos previos

### Hot Restart resetea:
- Todos los estados a valores iniciales
- Conexiones de streams
- Datos en memoria
- Controllers (dispose + recrear)

---

## Errores comunes y soluciones

### "Cannot connect to the Dart Observatory"
```
Causa: Emulador no listo o app cerrada
Solución: flutter clean && flutter run --debug
```

### "Application finished"
```
Causa: App terminó o no está en modo debug
Solución: Verificar que estés en modo --debug, no --release
```

### "Function breakpoints not working"
```
Causa: VSCode no puede resolver nombre de función
Solución: Usar breakpoint de línea en la primera línea de la función
```

### "Variables show <optimized out>"
```
Causa: Compilador optimizó la variable
Solución: Usar --debug o agregar print antes del breakpoint
```

---

## Command Palette (Ctrl+Shift+P) - Debug

| Comando | Acción |
|---------|--------|
| `Debug: Start Debugging` | Iniciar/F5 |
| `Debug: Stop Debugging` | Detener/Shift+F5 |
| `Debug: Restart Debugging` | Reiniciar |
| `Debug: Open Debug Console` | Abrir Debug Console |
| `Debug: Toggle Breakpoint` | En cursor |
| `Debug: Remove All Breakpoints` | Limpiar todos |
| `Debug: Disable All Breakpoints` | Deshabilitar todos |
| `Flutter: Hot Reload` | Hot reload |
| `Flutter: Hot Restart` | Hot restart |
| `Dart: Open DevTools Inspector` | Abrir DevTools |

---

## Flujo de debugging típico

```
1. F5 (Start)
     ↓
2. Breakpoint alcanzado
     ↓
3. Inspeccionar VARIABLES
     ↓
4. Agregar WATCH si necesario
     ↓
5. F10 (Step Over) para recorrer código
     ↓
6. F11 (Step Into) cuando quiero ver dentro de función
     ↓
7. Debug Console para evaluar expresiones
     ↓
8. F5 (Resume) para continuar hasta siguiente BP
     ↓
9. Repetir hasta encontrar el bug
     ↓
10. Fix + Hot Restart
```

---
→ Siguiente: `07-practicas-vscode.md`
