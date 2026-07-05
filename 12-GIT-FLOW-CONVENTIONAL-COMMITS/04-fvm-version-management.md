# 04 - FVM: Flutter Version Management

> Gestiona múltiples versiones de Flutter en el mismo equipo. Cada proyecto usa la versión exacta que necesita.

---

## 1. ¿Por qué FVM?

### El Problema

```bash
# Dev 1: Flutter 3.16.0
# Dev 2: Flutter 3.22.0
# CI/CD: Flutter 3.24.0

# Mismo código, diferentes versiones → diferentes resultados
# "En mi máquina funciona" → versión incorrecta
```

### La Solución

```bash
# FVM permite que CADA proyecto tenga su propia versión de Flutter
# Configurada en .fvm/flutter_sdk_version
# Ignorada por git → cada dev instala la que necesita
```

---

## 2. Instalación

### 2.1 Instalar FVM

```bash
# Dart (recomendado)
dart pub global activate fvm

# Verificar
fvm --version
```

### 2.2 Configurar PATH

```bash
# Agregar al shell (~/.bashrc, ~/.zshrc)
export PATH="$PATH:$HOME/.pub-cache/bin"
```

---

## 3. Uso Básico

### 3.1 Instalar Versiones

```bash
# Listar versiones disponibles
fvm releases

# Instalar versión estable
fvm install 3.24.0

# Instalar última estable
fvm install stable

# Instalar canal
fvm install beta
```

### 3.2 Configurar Proyecto

```bash
# En la raíz del proyecto
cd apps/mobile
fvm use 3.24.0

# Esto crea:
# - .fvm/flutter_sdk_version  (versión configurada)
# - .fvm/                     (symlink a la SDK instalada)
```

### 3.3 Usar la Versión del Proyecto

```bash
# Ejecutar comandos con la versión del proyecto
fvm flutter pub get
fvm flutter run
fvm flutter build apk

# O configurar VS Code para usar .fvm/flutter automáticamente
```

---

## 4. Integración con VS Code

### 4.1 Configuración de Workspace

```json
// .vscode/settings.json
{
  "dart.flutterSdkPath": ".fvm/flutter_sdk",
  "dart.sdkPath": ".fvm/flutter_sdk/bin/cache/dart-sdk",
  "search.exclude": {
    ".fvm": true
  },
  "files.exclude": {
    ".fvm": true
  }
}
```

### 4.2 Dart SDK

```json
{
  "dart.sdkPath": ".fvm/flutter_sdk/bin/cache/dart-sdk",
  "dart.flutterSdkPath": ".fvm/flutter_sdk",
  "dart.lineLength": 100
}
```

---

## 5. Integración con CI/CD

### 5.1 GitHub Actions

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter con FVM
        uses: kuhnroyal/flutter-fvm-config-action@v2
        with:
          fvm-config: apps/mobile/.fvm/flutter_sdk_version

      - name: Get dependencies
        run: flutter pub get

      - name: Analyze
        run: flutter analyze

      - name: Test
        run: flutter test
```

### 5.2 Docker

```dockerfile
FROM dart:latest

# Instalar FVM
RUN dart pub global activate fvm

# Usar versión del proyecto
WORKDIR /app/apps/mobile
COPY .fvm/flutter_sdk_version .
RUN fvm use

# Ahora los comandos usan la versión correcta
```

---

## 6. FVM en el Proyecto Real

```bash
# .fvm/flutter_sdk_version en apps/mobile/
3.24.0
```

**Qué hace:**
1. Todos los desarrolladores usan Flutter 3.24.0
2. VS Code usa el SDK correcto automáticamente
3. CI/CD lee la versión desde este archivo

---

## 7. Comandos Útiles

```bash
# Listar versiones instaladas
fvm list

# Versión actual del proyecto
fvm current

# Cambiar entre versiones globalmente
fvm global 3.16.0

# Eliminar versión
fvm remove 3.16.0

# Probar comando con versión específica
fvm exec 3.24.0 flutter analyze
```

---

## 8. .gitignore

```gitignore
# FVM - version manager
.fvm/flutter_sdk
.fvm/leak_tracker
.fvm/dart-sdk
```

Se ignora el **SDK** pero NO la **configuración** (`.fvm/flutter_sdk_version`).

---

## 9. Resumen

1. **FVM** permite tener la versión exacta de Flutter por proyecto
2. **`.fvm/flutter_sdk_version`** define la versión (se comita)
3. **`.fvm/flutter_sdk`** es el SDK instalado (se ignora)
4. **VS Code** se configura para usar `.fvm/flutter_sdk`
5. **CI/CD** lee la versión del archivo de configuración
6. **`fvm flutter`** usa la versión del proyecto

---

## Recursos

- [FVM GitHub](https://github.com/leoafarias/fvm)
- [FVM Documentation](https://fvm.app/)

---

## 📚 Referencias

- [Conventional Commits](https://www.conventionalcommits.org/) — Especificación de mensajes de commit
- [Husky](https://typicode.github.io/husky/) — Git hooks modernos para Node.js
- [Commitlint](https://commitlint.js.org/) — Linter para mensajes de commit
- [Git | Documentation](https://git-scm.com/doc) — Documentación oficial de Git

---
