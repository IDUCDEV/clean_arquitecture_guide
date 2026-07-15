# 01 - Fundamentos de Flutter DevTools

## ¿Qué es Flutter DevTools?

Suite de herramientas de diagnóstico para Flutter y Dart. No es un debugger tradicional sino un complemento para análisis visual de la app.

### Componentes principales

| Herramienta | Propósito |
|-------------|-----------|
| **Flutter Inspector** | Explorar árbol de widgets, propiedades, layout |
| **Performance** | Medir FPS, frame rendering, jank |
| **CPU Profiler** | Analizar uso de CPU, flame chart |
| **Memory** | Monitorear uso de memoria, leaks, snapshots |
| **Network** | Inspeccionar requests HTTP y WebSocket |
| **Debugger** | Breakpoints y control de ejecución (alternativa a VSCode) |
| **Logging** | Ver logs de la app en tiempo real |
| **App Size** | Analizar tamaño del bundle |
| **Provider** | Inspeccionar estado de Riverpod/BLoC (si disponible) |

---

## Cómo iniciar DevTools

### Opción 1: Desde VSCode
1. Durante debugging, abrir Command Palette (`Ctrl+Shift+P`)
2. `Dart: Open DevTools`
3. Seleccionar pestaña deseada

### Opción 2: Desde terminal
```bash
# Con app corriendo en modo debug
dart devtools

# Con URI específica del VM service
dart devtools --vm-service-uri=http://127.0.0.1:8181
```

### Opción 3: Integrado en VSCode
- Durando debugging, click en icono de DevTools en la barra de debug
- O en `DEBUG CONSOLE` ejecutar `dart devtools`

---

## Conexión entre herramientas

```
┌─────────────────────────────────────────────────┐
│                   VSCode                        │
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

## Requisitos previos

### Modo debug obligatorio
```bash
# DevTools NO funciona en modo release
flutter run --debug

# O con profile para mejor rendimiento
flutter run --profile
```

### Versión mínima recomendada
- Flutter SDK: 3.16+
- VSCode: 1.85+
- Extensión Dart: 3.80+

---

## Configuración de DevTools en VSCode

### `settings.json`
```json
{
  "dart.devToolsTheme": "dark",
  "dart.devTools": {
    "activeExtension": "inspector",
    "launch": true
  },
  "dart.flutterDevTools": {
    "showWidgetInspector": true,
    "autoOpen": false
  }
}
```

### Atajos de teclado para DevTools

| Atajo | Acción |
|-------|--------|
| `Ctrl+Shift+D` | Abrir DevTools sidebar |
| `Ctrl+Shift+P` → `Dart: Open DevTools` | Command Palette |
| `Ctrl+Shift+D` + click en pestaña | Abrir herramienta específica |

---

## Flujo típico de trabajo

```
1. flutter run --debug
     ↓
2. Abrir DevTools desde VSCode
     ↓
3. Seleccionar herramienta según problema:
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

## Cómo funciona internamente

DevTools se comunica con tu app a través del **VM Service**:

```
Tu App Flutter
      ↓
   VM Service (Dart VM)
      ↓
   WebSocket (ws://127.0.0.1:PORT/...)
      ↓
   DevTools (HTML/JS app)
      ↓
   VSCode (renderiza)
```

### Información que expone el VM Service:
- Árbol de widgets y sus propiedades
- Métricas de rendimiento (frame timing)
- Uso de memoria (heap, GC events)
- Tráfico de red (requests/responses)
- Logs de stdout/stderr
- Estado de isolates

---

## Limitaciones conocidas

| Limitación | Causa |
|------------|-------|
| No funciona en release mode | DevTools requiere VM Service |
| Performance afectada en debug | Debug mode tiene overhead |
| Memory snapshots son aproximados | Debug mode usa más memoria |
| Network no ve requests de plataforma nativa | Solo capta requests desde Dart |
| Algunos widgets no muestran propiedades | Framework limitation |

---
→ Siguiente: `02-inspector-layout.md`
