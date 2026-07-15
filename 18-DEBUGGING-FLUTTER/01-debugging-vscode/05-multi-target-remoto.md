# 05 - Multi-target y Remoto

## 1. Multi-target debugging

### ¿Qué es?
Permite depurar múltiples procesos simultáneamente: tu app Flutter + el servidor Dart DevTools, o dos instancias de la misma app.

### Configuración en `launch.json`

#### Depurar Dart CLI + Flutter App en paralelo
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flutter App",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart"
    },
    {
      "name": "Worker Dart",
      "type": "dart",
      "request": "launch",
      "program": "bin/worker.dart"
    }
  ],
  "compounds": [
    {
      "name": "App + Worker",
      "configurations": ["Flutter App", "Worker Dart"]
    }
  ]
}
```

#### Depurar isolate principal + isolate secundario
```json
{
  "name": "Flutter Main + Background",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "dartLaunchFlags": ["--observe=8181"]
}
```

### ¿Cuándo usar compounds?
- App frontend + worker isolate procesando datos
- Microservicio Dart local + cliente que lo consume
- Dos instancias de app para probar comunicación
- Migración de datos que corre en paralelo con la app

---

## 2. Remote debugging

### Opción A: Debug via WebSocket (app ya corriendo)

```dart
// En tu main.dart temporalmente:
import 'dart:developer';

void main() {
  // Espera conexión de depurador
  debugger(); // Punto de entrada para attach
  runApp(MyApp());
}
```

O mejor, usando observatory:
```dart
import 'dart:developer';

void main() {
  // Publica URI de conexión
  print('VM service: ${Service.getObservatoryUri()}');
  runApp(MyApp());
}
```

### Opción B: Attach a proceso existente

```json
{
  "name": "Attach to running Flutter",
  "type": "dart",
  "request": "attach",
  "vmServiceUri": "${env:FLUTTER_VM_SERVICE_URI}"
}
```

### Opción C: Chrome remoto (web)

```json
{
  "name": "Chrome Remote Debug",
  "type": "chrome",
  "request": "launch",
  "url": "http://localhost:8080",
  "webRoot": "${workspaceFolder}/lib",
  "sourceMaps": true,
  "trace": true
}
```

Iniciar Chrome con depuración remota:
```bash
# En la máquina remota:
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug

# Desde tu máquina:
# Configurar port forwarding SSH:
ssh -L 9222:localhost:9222 usuario@maquina-remota
```

### Opción D: Debugging en dispositivos físicos remotos

```bash
# Conectar dispositivo vía ADB remoto
adb connect 192.168.1.100:5555

# Verificar conexión
adb devices

# Lanzar debug desde VSCode
flutter run --debug
```

### Opción E: Flutter Web remoto

```json
{
  "name": "Flutter Web Remote",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "device": "chrome",
  "args": ["--web-port=8080", "--web-hostname=0.0.0.0"]
}
```

Acceder desde otra máquina:
```
http://192.168.1.50:8080
```

---

## 3. Debugging con Docker/WSL

### Docker Compose para backend local

```yaml
# docker-compose.yml
version: '3.8'
services:
  supabase-local:
    image: supabase/local
    ports:
      - "54321:54321"
      - "54322:54322"
    environment:
      - ANON_KEY=eyJ...  # Tu anon key local
```

### Conectar Flutter app al backend Docker

```dart
// En tu cliente Supabase:
final supabase = SupabaseClient(
  'http://localhost:54321',  // Docker mapeado
  'eyJ...',                   // Anon key
);
```

### `launch.json` para Docker
```json
{
  "name": "Flutter + Docker Backend",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "args": ["--dart-define=SUPABASE_URL=http://localhost:54321"],
  "preLaunchTask": "docker:up"
}
```

---

## 4. Depuración de tests

### Test individual
```json
{
  "name": "Debug Single Test",
  "type": "dart",
  "request": "launch",
  "program": "test/widget_test.dart",
  "args": ["--name", "test name exacto"]
}
```

### Test con patrón regex
```json
{
  "name": "Debug Test Pattern",
  "type": "dart",
  "request": "launch",
  "program": "test/unit/auth_test.dart",
  "args": ["--name", "login.*error"]
}
```

### Todos los tests de un archivo
```json
{
  "name": "Debug All Auth Tests",
  "type": "dart",
  "request": "launch",
  "program": "test/unit/auth_test.dart"
}
```

### Usando VSCode Testing Side Bar
1. Click en icono de Testing (beaker) en sidebar
2. Hover sobre test → aparece "Debug Test"
3. Breakpoints en test → ejecutar con debug

---

## 5. Debugging de Isolates

### Observar todos los isolates
```dart
import 'dart:isolate';

// Crear isolate con nombre identifiable
await Isolate.spawn(
  _isolateEntryPoint,
  message,
  debugName: 'image-processor',  // ← Visible en VSCode
);
```

### VSCode detecta automáticamente los isolates
- En `CALL STACK` verás cada isolate como separate entry
- Click en isolate diferente → inspeccionar sus variables
- Cada isolate tiene su propio punto de ejecución

### Configuración avanzada
```json
{
  "name": "Flutter with Isolates",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "dartVmServicePort": 8181,
  "dartLaunchFlags": [
    "--enable-vm-service=8181",
    "--pause-isolates-on-start"
  ]
}
```

---

## 6. Depuración de errores de plataforma

### Debug en Android (native)
```bash
# Logs de Android desde terminal
adb logcat -s flutter

# Buscar errores específicos
adb logcat | grep -E "(Exception|Error|FATAL)"
```

### Debug en iOS (native)
```bash
# Simulator logs
xcrun simctl spawn booted log stream --level=debug --predicate 'process == "Runner"'

# Device logs
idevicesyslog -u DEVICE_ID
```

### VSCode Task para logs
```json
{
  "label": "Android Logs",
  "type": "shell",
  "command": "adb",
  "args": ["logcat", "-s", "flutter"],
  "isBackground": true,
  "problemMatcher": []
}
```

---

## 7. Resumen de patrones de conexión

| Escenario | Método | Puerto/Tipo |
|-----------|--------|-------------|
| Local emulator | Directo | Automático |
| Dispositivo físico USB | Directo | USB |
| Dispositivo WiFi | `flutter run` | WiFi directo |
| Chrome web | DevTools | 9222+ |
| Backend Docker | localhost | Mapeado |
| SSH remote | Port forward | SSH tunnel |
| Dos procesos Dart | Compound launch | Múltiples |
| Tests | Program launch | Test runner |

### Comandos útiles de terminal
```bash
# Ver todos los dispositivos conectados
flutter devices

# Ver info del VM service
flutter attach --debug-port=8181

# Conectar a VM service existente
dart devtools --vm-service-uri=http://127.0.0.1:8181
```

---
→ Siguiente: `06-cheatsheet-vscode.md`
