# 05 — Multi-target y Debugging Remoto

> Depurar varios procesos a la vez, adjuntarte a una app en ejecución y trabajar contra dispositivos y backends remotos.

---

## 1. Multi-target debugging

Permite depurar múltiples procesos simultáneamente: tu app Flutter + un script Dart, o dos instancias de la misma app.

### 1.1 Depurar Dart CLI + Flutter App en paralelo

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

### 1.2 ¿Cuándo usar compounds?

- App frontend + worker isolate procesando datos
- Microservicio Dart local + cliente que lo consume
- Dos instancias de app para probar comunicación
- Migración de datos que corre en paralelo con la app

---

## 2. Attach a un proceso existente

### 2.1 Desde VS Code

La app ya está corriendo (p. ej. lanzada con `flutter run`) y quieres adjuntarte desde VS Code:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to running Flutter",
      "type": "dart",
      "request": "attach",
      "program": "lib/main.dart"
    }
  ]
}
```

La extensión descubre automáticamente el **VM Service** de la app en ejecución. No hace falta copiar ninguna URI.

### 2.2 Pausar la app en el arranque

Si necesitas que la app espere a que un debugger se conecte (útil en CI o lanzando fuera de VS Code):

```bash
flutter run --start-paused
```

Luego adjunta un debugger desde VS Code (`request: "attach"`).

### 2.3 Forzar puertos del VM Service / DDS

Normalmente no hace falta, pero si tu firewall o tooling lo exige:

```bash
# Fijar el puerto del Dart Development Service (DDS)
flutter run --dds-port 8181

# Al adjuntar, buscar el VM service en un puerto específico
flutter attach --device-vmservice-port 8181
```

> **Nota**: la bandera antigua `--observatory-port` (y su sucesor `--vm-service-port`) fue reemplazada. Hoy el proceso correcto es el DDS sobre el VM Service, y la detección automática hace innecesario fijar puertos en la mayoría de los casos.

---

## 3. Chrome remoto (web)

### 3.1 Configuración de launch

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flutter Web Remote",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "deviceId": "chrome",
      "toolArgs": ["--web-port=8080", "--web-hostname=0.0.0.0"]
    }
  ]
}
```

Acceder desde otra máquina:

```
http://192.168.1.50:8080
```

> `deviceId: "chrome"` (antes `device: "chrome"`) selecciona el navegador. Las banderas de servidor web van en `toolArgs` porque son de `flutter run`.

### 3.2 Chrome DevTools remoto

Para depurar el front-end web con el debugger de Chrome:

```bash
# En la máquina remota, inicia Chrome con depuración remota:
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug

# Desde tu máquina, haz port forwarding por SSH:
ssh -L 9222:localhost:9222 usuario@maquina-remota
```

---

## 4. Dispositivos físicos remotos

### 4.1 ADB inalámbrico (Android 11+)

Empareja el dispositivo por red (Android Developer Options → **Wireless debugging**):

```bash
# Pairing code
adb pair 192.168.1.100:37000

# Conectar
adb connect 192.168.1.100:5555

# Verificar
adb devices
```

Luego lanza la app desde VS Code o terminal:

```bash
flutter run --debug -d 192.168.1.100:5555
```

### 4.2 Dispositivo físico por USB

Sin configuración extra: `flutter run` detecta el dispositivo conectado por USB.

---

## 5. Debugging con Docker y Supabase local

### 5.1 Supabase local (CLI)

El entorno local de Supabase corre en contenedores. La forma recomendada es el CLI oficial:

```bash
# Inicia los contenedores de Supabase local (Postgres, Auth, Realtime, Storage, Functions)
supabase start

# Detener los contenedores (mantiene los datos)
supabase stop

# Estado y URLs del proyecto local
supabase status
```

`supabase start` levanta el API en `http://localhost:54321` y la base de datos en el puerto `54322`.

### 5.2 Conectar la app Flutter al backend local

```dart
// En tu cliente Supabase (modo desarrollo):
final supabase = SupabaseClient(
  'http://localhost:54321',      // API local de Supabase
  supabaseAnonKey,               // Anon key local de supabase status
);
```

### 5.3 `launch.json` para desarrollo con Supabase local

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flutter + Supabase Local",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "dartDefine": ["SUPABASE_URL=http://localhost:54321"]
    }
  ]
}
```

### 5.4 Levantar Supabase antes de depurar (tasks)

Crea una task en `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "supabase: start",
      "type": "shell",
      "command": "supabase start",
      "problemMatcher": []
    }
  ]
}
```

Y referénciala con `preLaunchTask` en el compound:

```json
{
  "compounds": [
    {
      "name": "Supabase Local + App",
      "configurations": ["Flutter + Supabase Local"],
      "preLaunchTask": "supabase: start"
    }
  ]
}
```

---

## 6. Depuración de tests

### 6.1 Test individual

```json
{
  "name": "Debug Single Test",
  "type": "dart",
  "request": "launch",
  "program": "test/widget_test.dart",
  "args": ["--plain-name", "test name exacto"]
}
```

### 6.2 Test con patrón regex

```json
{
  "name": "Debug Test Pattern",
  "type": "dart",
  "request": "launch",
  "program": "test/unit/auth_test.dart",
  "args": ["--name", "login.*error"]
}
```

### 6.3 Todos los tests de un archivo

```json
{
  "name": "Debug All Auth Tests",
  "type": "dart",
  "request": "launch",
  "program": "test/unit/auth_test.dart"
}
```

### 6.4 Usando la Testing Side Bar de VS Code

1. Click en el icono de Testing (matraz) en la sidebar
2. Hover sobre un test → aparece "Debug Test"
3. Pon breakpoints en el test → ejecuta con debug

---

## 7. Debugging de isolates

### 7.1 Crear isolate con nombre identificable

```dart
import 'dart:isolate';

// Crear isolate con nombre identifiable
await Isolate.spawn(
  _isolateEntryPoint,
  message,
  debugName: 'image-processor',  // ← Visible en VS Code
);
```

### 7.2 VS Code detecta automáticamente los isolates

- En **CALL STACK** verás cada isolate como entry separado
- Click en un isolate diferente → inspeccionar sus variables
- Cada isolate tiene su propio punto de ejecución

### 7.3 Pausar todos los isolates al arrancar

```json
{
  "name": "Flutter with Isolates",
  "type": "dart",
  "request": "launch",
  "program": "lib/main.dart",
  "toolArgs": ["--start-paused"]
}
```

---

## 8. Depuración de errores de plataforma

### 8.1 Logs de Android (native)

```bash
# Logs de Flutter desde terminal
adb logcat -s flutter

# Buscar errores específicos
adb logcat | grep -E "(Exception|Error|FATAL)"
```

### 8.2 Logs de iOS (native)

```bash
# Simulator logs
xcrun simctl spawn booted log stream --level=debug --predicate 'process == "Runner"'

# Device logs
idevicesyslog -u DEVICE_ID
```

### 8.3 Task de VS Code para logs

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

## 9. El VM Service y DevTools

Cuando corres la app en debug, Flutter expone un **VM Service** (por defecto sobre el DDS) que usan VS Code y DevTools para inspeccionar la app. Puedes abrir DevTools de varias formas:

```bash
# Mientras corre flutter run, presiona "d" en la terminal
d

# Desde otra terminal, adjuntando el URI que imprime flutter run:
dart devtools http://127.0.0.1:8181/XXXXXX/
```

> `dart devtools` acepta el URI del VM Service como argumento posicional (o lanza una página que se conecta sola a la app descubierta).

---

## 10. Resumen de patrones de conexión

| Escenario | Método | Puerto/Tipo |
|---|---|---|
| Local emulator | Directo | Automático |
| Dispositivo físico USB | Directo | USB |
| Dispositivo WiFi/inalámbrico | `adb connect` / wireless pairing | WiFi |
| Chrome web | `deviceId: "chrome"` + `toolArgs` | Automático |
| Backend Supabase local | `supabase start` | 54321/54322 |
| SSH remote | Port forwarding | SSH tunnel |
| Dos procesos Dart | Compound launch | Múltiples |
| Tests | Program launch | Test runner |

### Comandos útiles de terminal

```bash
# Ver todos los dispositivos conectados
flutter devices

# Lanzar la app esperando un debugger
flutter run --start-paused

# Adjuntarse a una app en ejecución
flutter attach

# Adjuntarse filtrando por app (Android package / iOS bundle id)
flutter attach --app-id com.example.miapp

# Abrir DevTools contra la app descubierta
dart devtools
```

---

## Resumen

| Escenario | Cómo conectarse | Nota |
|---|---|---|
| App Flutter + script Dart | Compound launch | Breakpoints en ambos procesos |
| App en ejecución | `flutter attach` | Mismo codebase y target |
| Dispositivo físico / WiFi | `adb` / wireless pairing | USB o red local |
| Chrome web | `deviceId: "chrome"` | Depuración en el navegador |
| Backend Supabase local | `supabase start` | Puerto 54321/54322 |
| Máquina remota | SSH port forwarding | Tunnel hacia el VM Service |
| Tests | Program launch | Breakpoints en tests |
| Isolates | Detección automática | `--start-paused` pausa todos |

---

## 📚 Referencias

- [Flutter | VS Code — Run and debug](https://docs.flutter.dev/tools/vs-code) — Configuraciones de launch/attach
- [Flutter | Debugging tools](https://docs.flutter.dev/testing/debugging) — Panorama de herramientas de debugging
- [Flutter | DevTools CLI](https://docs.flutter.dev/tools/devtools/cli) — Cómo abrir DevTools desde la terminal
- [Supabase | Local development](https://supabase.com/docs/guides/local-development) — `supabase start` y el stack local

---

> 📖 **Siguiente:** [06-cheatsheet-vscode.md](./06-cheatsheet-vscode.md) — Cheatsheet de atajos, expresiones y plantillas de VS Code
