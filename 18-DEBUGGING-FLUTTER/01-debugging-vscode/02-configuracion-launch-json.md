# 02 - Configuracion de launch.json para Flutter

## Que es launch.json

`launch.json` es el archivo de configuracion que le dice a VSCode **como ejecutar y debuggear** tu aplicacion. Vive en `.vscode/launch.json` y define:

- Que comando ejecutar (`flutter run`, `flutter run --profile`, etc.)
- Que plataforma usar (Android, iOS, Web, Desktop)
- Que argumentos pasar
- Que archivos adjuntar

---

## Estructura basica

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      // Configuracion 1
    },
    {
      // Configuracion 2
    }
  ],
  "compounds": [
    // Combinaciones de configuraciones
  ]
}
```

---

## Configuracion minima para Flutter

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flutter (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart"
    }
  ]
}
```

Con esto, presionando F5 se ejecuta tu app en debug mode.

---

## Configuracion completa multi-plataforma

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flutter (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart"
    },
    {
      "name": "Flutter (Profile)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "profile"
    },
    {
      "name": "Flutter (Release)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "release"
    },
    {
      "name": "Android (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "debug",
      "toolArgs": ["-d", "android"]
    },
    {
      "name": "iOS (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "debug",
      "toolArgs": ["-d", "ios"]
    },
    {
      "name": "Chrome (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "debug",
      "toolArgs": ["-d", "chrome"]
    },
    {
      "name": "macOS (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "debug",
      "toolArgs": ["-d", "macos"]
    },
    {
      "name": "Linux (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "debug",
      "toolArgs": ["-d", "linux"]
    },
    {
      "name": "Windows (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "debug",
      "toolArgs": ["-d", "windows"]
    }
  ]
}
```

---

## Propiedades importantes de launch.json

### `name`
Nombre que aparece en el dropdown de debugging. Usa nombres descriptivos.

### `type`
Siempre `"dart"` para Flutter.

### `request`
- `"launch"`: Lanza una nueva sesion
- `"attached"`: Se adjunta a un proceso ya corriendo

### `program`
Punto de entrada. Por defecto `"lib/main.dart"`.

### `flutterMode`
- `"debug"` (default)
- `"profile"`
- `"release"`

### `args`
Argumentos que se pasan al programa Dart:
```json
"args": ["--verbose", "--no-sound-null-safety"]
```

### `toolArgs`
Argumentos que se pasan a la herramienta `flutter run`:
```json
"toolArgs": ["-d", "emulator-5554", "--verbose"]
```

### `env`
Variables de entorno:
```json
"env": {
  "FLUTTER_APP_FLAVOR": "development",
  "SUPABASE_URL": "http://localhost:54321"
}
```

### `programArgs`
Argumentos del programa (alternativa a `args`):
```json
"programArgs": ["--flavor", "development"]
```

---

## Configuracion con argumentos de Supabase

Para apps con Supabase, es util tener configuraciones para diferentes ambientes:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "App (Dev - Local Supabase)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main_development.dart",
      "env": {
        "SUPABASE_URL": "http://localhost:54321",
        "SUPABASE_ANON_KEY": "eyJ..."
      }
    },
    {
      "name": "App (Staging)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main_staging.dart",
      "env": {
        "SUPABASE_URL": "https://staging.supabase.co",
        "SUPABASE_ANON_KEY": "eyJ..."
      }
    },
    {
      "name": "App (Production)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main_production.dart",
      "env": {
        "SUPABASE_URL": "https://prod.supabase.co",
        "SUPABASE_ANON_KEY": "eyJ..."
      }
    }
  ]
}
```

---

## Configuracion con Flutter Flavors

Si usas flavors (development, staging, production):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Development",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "toolArgs": ["--flavor", "development", "-t", "lib/main_development.dart"]
    },
    {
      "name": "Production",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "toolArgs": ["--flavor", "production", "-t", "lib/main_production.dart"],
      "flutterMode": "profile"
    }
  ]
}
```

---

## Configuracion de Attached Debugging

Para adjuntar a un proceso que ya esta corriendo:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to running app",
      "type": "dart",
      "request": "attach",
      "observatoryUri": "http://127.0.0.1:8181/xxxxx"
    }
  ]
}
```

**Para obtener el URI:**
1. Ejecuta `flutter run --observatory-port=8181`
2. Busca el URI en la salida del terminal
3. Copialo en `observatoryUri`

---

## Configuracion con Breakpoints condicionales

Puedes pre-configurar breakpoints en launch.json:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug con Breakpoint inicial",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "dartCodesigning": false,
      "programArgs": ["--dart-define=DEBUG=true"],
      "additionalProjectFolders": []
    }
  ]
}
```

> **Nota**: Los breakpoints se configuran en el editor (click en gutter), no en launch.json. El launch.json define la configuracion de la sesion, no los breakpoints.

---

## Configuracion para testing

Para ejecutar tests con debugging:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Test (all)",
      "type": "dart",
      "request": "launch",
      "program": "test/widget_test.dart"
    },
    {
      "name": "Test (specific)",
      "type": "dart",
      "request": "launch",
      "program": "test/features/auth/login_test.dart"
    }
  ]
}
```

---

## Compounds: ejecutar multiples configuraciones

Los compounds permiten lanzar varias configuraciones simultaneamente:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "App Flutter",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart"
    },
    {
      "name": "Supabase Local",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/supabase/functions/serve.ts"
    }
  ],
  "compounds": [
    {
      "name": "App + Backend Local",
      "configurations": ["App Flutter", "Supabase Local"],
      "stopAll": true,
      "preLaunchTask": ""
    }
  ]
}
```

---

## Mejores practicas

1. **Nunca guardes secrets en launch.json**: usa variables de entorno o `.env`
2. **Usa `program` en lugar de `args`**: es mas explicito
3. **Nombra tus configuraciones descriptivamente**: "App (Dev)" no "Debug 1"
4. **Ten una configuracion por plataforma**: para no cambiar cada vez
5. **Commit el launch.json**: es parte del proyecto, todos lo necesitan
6. **Usa `flutterMode` en lugar de args**: es mas limpio

---

## Ejemplo completo de launch.json para un proyecto real

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flutter (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart"
    },
    {
      "name": "Flutter (Profile)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "flutterMode": "profile"
    },
    {
      "name": "Android (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "toolArgs": ["-d", "android"]
    },
    {
      "name": "iOS (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "toolArgs": ["-d", "ios"]
    },
    {
      "name": "Chrome (Debug)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main.dart",
      "toolArgs": ["-d", "chrome"]
    },
    {
      "name": "Dev (Local Supabase)",
      "type": "dart",
      "request": "launch",
      "program": "lib/main_development.dart",
      "env": {
        "SUPABASE_URL": "http://localhost:54321"
      }
    },
    {
      "name": "Test (all)",
      "type": "dart",
      "request": "launch",
      "program": "test/widget_test.dart"
    }
  ]
}
```

---

## Resumen

| Propiedad | Descripcion | Ejemplo |
|---|---|---|
| `name` | Nombre de la config | `"Flutter (Debug)"` |
| `type` | Tipo de debugger | `"dart"` |
| `request` | Launch o attach | `"launch"` |
| `program` | Punto de entrada | `"lib/main.dart"` |
| `flutterMode` | Modo de compilacion | `"debug"`, `"profile"`, `"release"` |
| `toolArgs` | Args de flutter run | `["-d", "android"]` |
| `env` | Variables de entorno | `{"KEY": "value"}` |
| `args` | Args del programa | `["--verbose"]` |

---

## Siguiente paso

Ve al [03-breakpoints-avanzados.md](./03-breakpoints-avanzados.md) para aprender sobre todos los tipos de breakpoints disponibles.
