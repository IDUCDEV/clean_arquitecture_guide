# 08 — Fundamentos de Flutter DevTools

> Qué es Flutter DevTools, cómo iniciarlo, cómo se conecta con tu app y qué vistas te ofrece para diagnosticar problemas.

---

## 1. ¿Qué es Flutter DevTools?

Es la suite de herramientas de diagnóstico para Flutter y Dart. No es un debugger tradicional sino un complemento para análisis **visual** de la app: árbol de widgets, métricas de rendimiento, memoria, red y más.

### 1.1 Vistas principales

| Herramienta | Propósito |
|---|---|
| **Flutter Inspector** | Explorar el árbol de widgets, propiedades y layout |
| **Performance** | Medir FPS, frame rendering y jank |
| **CPU Profiler** | Analizar uso de CPU con flame chart |
| **Memory** | Monitorear uso de memoria, leaks y snapshots |
| **Network** | Inspeccionar requests HTTP y WebSocket |
| **Debugger** | Breakpoints y control de ejecución (alternativa a VS Code) |
| **Logging** | Ver logs de la app en tiempo real |
| **App Size** | Analizar el tamaño del bundle |

> Además, DevTools soporta **extensiones** de terceros (p. ej. Riverpod) que agregan vistas específicas según el paquete que uses.

---

## 2. Cómo iniciar DevTools

### 2.1 Desde VS Code

1. Durante debugging, abre la Command Palette (`Ctrl+Shift+P`)
2. Ejecuta `Dart: Open DevTools`
3. Selecciona la vista deseada

### 2.2 Desde la terminal

```bash
# Con la app corriendo en modo debug, desde la terminal de flutter run:
d

# Desde otra terminal, pasando la URI del VM Service (posicional):
dart devtools http://127.0.0.1:8181/XXXXXX/

# O simplemente abrir DevTools y conectar a la app descubierta:
dart devtools
```

### 2.3 Con la app corriendo

DevTools se conecta al **VM Service** que expone tu app en modo debug/profile. La forma más cómoda es presionar `d` en la terminal donde corre `flutter run`.

---

## 3. Conexión entre herramientas

```
┌─────────────────────────────────────────────────┐
│                   VS Code                       │
│  ┌───────────────────────────────────────────┐  │
│  │           Flutter DevTools                │  │
│  │                                           │  │
│  │  Inspector ←→ Performance ←→ Memory      │  │
│  │      ↑              ↑           ↑        │  │
│  │      │              │           │        │  │
│  │  VM Service URI ←───────────────┘        │  │
│  │                                           │  │
│  │  Network ←→ Logging ←→ App Size          │  │
│  └───────────────────────────────────────────┘  │
│                    ↕                            │
│              Tu App Flutter                     │
└─────────────────────────────────────────────────┘
```

---

## 4. Requisitos previos

### 4.1 Modo debug o profile obligatorio

```bash
# DevTools NO funciona en modo release
flutter run --debug

# O con profile para métricas de rendimiento reales
flutter run --profile
```

### 4.2 Versiones recomendadas

- Flutter SDK: 3.x reciente (DevTools viaja dentro del SDK)
- VS Code: versión estable actual
- Extensión Dart: versión estable actual

> El "7 vistas de DevTools" clásico ya no aplica: algunas vistas se fusionaron (Timeline → Performance) y otras se volvieron extensiones (Provider → Riverpod/Bloc extensions).

---

## 5. Configuración de DevTools en VS Code

### 5.1 `settings.json`

```json
{
  "dart.devToolsTheme": "dark",
  "dart.devToolsBrowser": "embedded"
}
```

- `dart.devToolsTheme`: `"dark"` o `"light"`
- `dart.devToolsBrowser`: `"embedded"` (panel de VS Code), `"chrome"` u otro navegador

### 5.2 Cómo abrir cada vista

| Acción | Cómo |
|---|---|
| Abrir DevTools | `Ctrl+Shift+P` → `Dart: Open DevTools` |
| Panel Run and Debug | `Ctrl+Shift+D` |
| Abrir Inspector | DevTools → pestaña **Flutter Inspector** |

---

## 6. Flujo típico de trabajo

```
1. flutter run --debug
     ↓
2. Abrir DevTools desde VS Code (o presionar "d")
     ↓
3. Seleccionar la vista según el problema:
   - ¿UI se ve mal? → Inspector
   - ¿App va lenta? → Performance
   - ¿Memory leak? → Memory
   - ¿API falla? → Network
   - ¿Logs no aparecen? → Logging
     ↓
4. Diagnóstico con datos visuales
     ↓
5. Aplicar fix en código
     ↓
6. Hot Reload → Verificar fix en DevTools
     ↓
7. Cerrar DevTools y continuar desarrollo
```

---

## 7. Cómo funciona internamente

DevTools se comunica con tu app a través del **VM Service** (expuesto sobre el Dart Development Service o DDS):

```
Tu App Flutter
      ↓
   VM Service (Dart VM)
      ↓
   WebSocket (ws://127.0.0.1:PORT/...)
      ↓
   DevTools (HTML/JS app)
      ↓
   VS Code (renderiza)
```

### 7.1 Información que expone el VM Service

- Árbol de widgets y sus propiedades
- Métricas de rendimiento (frame timing)
- Uso de memoria (heap, GC events)
- Tráfico de red (requests/responses desde Dart)
- Logs de stdout/stderr
- Estado de isolates

---

## 8. Limitaciones conocidas

| Limitación | Causa |
|---|---|
| No funciona en release mode | DevTools requiere VM Service |
| Performance afectada en debug | El debug mode tiene overhead |
| Snapshots de memoria son aproximados | El debug mode usa más memoria |
| Network no ve requests de plataforma nativa | Solo capta requests hechos desde Dart |
| Algunos widgets no muestran propiedades | Limitación del framework |

---

## Resumen

1. DevTools es la suite visual de diagnóstico de Flutter
2. Se conecta al VM Service de la app en modo debug/profile
3. Se abre con `Dart: Open DevTools` o presionando `d` en `flutter run`
4. Cada problema tiene una vista: UI → Inspector, lentitud → Performance, memoria → Memory, red → Network
5. No funciona en modo release

---

## 📚 Referencias

- [Flutter | DevTools](https://docs.flutter.dev/tools/devtools) — Documentación oficial de DevTools
- [Flutter | DevTools CLI](https://docs.flutter.dev/tools/devtools/cli) — Cómo abrir DevTools desde la terminal
- [Flutter | DevTools VS Code](https://docs.flutter.dev/tools/devtools/vscode) — Integración con VS Code

---

> 📖 **Siguiente:** [09-inspector-layout.md](./09-inspector-layout.md) — Flutter Inspector y debugging de layout
