# 🚀 Nivel Experto: Build Runner Ecosystem

> build_runner es el motor de generación de código en Dart/Flutter. Entender cómo funciona es clave para dominar el ecosistema de codegen.

---

## 1. ¿Qué es build_runner?

build_runner es un sistema de generación de código basado en el paquete `build` de Dart. Permite ejecutar "builders" que analizan tu código fuente y generan archivos `.dart` adicionales.

### 1.1 El Problema que Resuelve

```dart
// Sin build_runner: tienes que escribir TODO manualmente
class User {
  final String id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});

  // Toda esta boilerplate la escribes TÚ:
  User.fromJson(Map<String, dynamic> json)
      : id = json['id'] as String,
        name = json['name'] as String,
        email = json['email'] as String;

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'email': email,
      };

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is User &&
          runtimeType == other.runtimeType &&
          id == other.id &&
          name == other.name &&
          email == other.email;

  @override
  int get hashCode => Object.hash(id, name, email);
}
```

**Con build_runner + generadores:**

```dart
@JsonSerializable()
@immutable
class User {
  final String id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

build_runner genera automáticamente el archivo `user.g.dart` con `_$UserFromJson` y `_$UserToJson`.

### 1.2 Cómo Funciona

```
┌─────────────────────┐
│  Código Fuente      │
│  (anotaciones)      │
└─────────┬───────────┘
          │ dart run build_runner
          ▼
┌─────────────────────┐
│  build_runner       │
│  • Lee archivos     │
│  • Busca builders   │
│  • Ejecuta cada uno │
│  • Resuelve orden   │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│  Código Generado    │
│  .g.dart            │
│  .config.dart       │
│  .freezed.dart      │
└─────────────────────┘
```

---

## 2. Comandos Esenciales

### 2.1 Comandos Principales

```bash
# Build único
dart run build_runner build

# Build único (elimina outputs conflictivos)
dart run build_runner build --delete-conflicting-outputs

# Modo watch: regenera automáticamente al guardar
dart run build_runner watch

# Modo watch con limpieza
dart run build_runner watch --delete-conflicting-outputs

# Limpiar caché de generación
dart run build_runner clean
```

### 2.2 Cuándo Usar Cada Uno

| Comando | Cuándo Usarlo |
|---------|---------------|
| `build --delete-conflicting-outputs` | CI/CD, setup inicial, después de pull |
| `watch --delete-conflicting-outputs` | Desarrollo activo (recomendado) |
| `build` | Si sabes que no hay conflictos |
| `clean` | Cuando el generador se comporta extraño |

### 2.3 Integración con Makefile

```makefile
# Makefile

MOBILE_DIR = apps/mobile

.PHONY: codegen codegen-watch clean

codegen:
	@cd $(MOBILE_DIR) && dart run build_runner build --delete-conflicting-outputs

codegen-watch:
	@cd $(MOBILE_DIR) && dart run build_runner watch --delete-conflicting-outputs

clean:
	@cd $(MOBILE_DIR) && dart run build_runner clean
```

---

## 3. Builders: El Corazón del Sistema

### 3.1 ¿Qué es un Builder?

Un builder es un paquete que sabe cómo generar código. Ejemplos:

| Builder | Paquete | Genera |
|---------|---------|--------|
| `json_serializable` | `json_serializable` | `.g.dart` con fromJson/toJson |
| `freezed` | `freezed` | `.freezed.dart` con data classes |
| `injectable_generator` | `injectable_generator` | `*.config.dart` con DI |
| `retrofit_generator` | `retrofit` | `.g.dart` con clientes HTTP |
| `isar_community_generator` | `isar` | `.g.dart` con código Isar |

### 3.2 Cómo Dart Encuentra los Builders

Los builders se registran en `pubspec.yaml` del paquete que los define:

```yaml
# Ejemplo: pubspec.yaml de json_serializable
environment:
  sdk: ">=3.0.0 <4.0.0"

builders:
  json_serializable:
    import: "package:json_serializable/builder.dart"
    builder_factories: ["jsonSerializable"]
    build_extensions: {".dart": [".json_serializable.g.part"]}
    auto_apply: dependents
    build_to: cache
```

Cuando ejecutas `build_runner`, este escanea todos tus paquetes, encuentra los builders registrados, y los ejecuta en el orden correcto.

---

## 4. Archivo build.yaml

### 4.1 Configuración Básica

```yaml
# build.yaml

targets:
  $default:
    builders:
      json_serializable:
        options:
          explicit_to_json: true
          include_if_null: false
          create_factory: true
```

### 4.2 Configuración por Builder

```yaml
targets:
  $default:
    builders:
      json_serializable:
        options:
          explicit_to_json: true
          field_rename: snake
          checked: true
          create_to_json: true
          any_map: false

      injectable_generator:injectable_builder:
        options:
          auto_register: true
          relative_paths: true

      freezed:
        options:
          union_key: type
          union_value_case: pascal
```

### 4.3 Opciones Comunes de json_serializable

| Opción | Valores | Descripción |
|--------|---------|-------------|
| `explicit_to_json` | true/false | Genera `toJson` explícito |
| `include_if_null` | true/false | Incluir campos null en JSON |
| `field_rename` | none, snake, kebab, pascal | Cómo convertir nombres |
| `checked` | true/false | Validar tipos en deserialización |
| `any_map` | true/false | Aceptar Map en lugar de solo Map<String, dynamic> |

### 4.4 Configuración para Monorepo

```yaml
# build.yaml en monorepo con múltiples paquetes
targets:
  $default:
    builders:
      json_serializable:
        generate_for:
          - "lib/**_models.dart"
          - "lib/**/*_dto.dart"
        options:
          explicit_to_json: true

  # Excluir tests de generación
  test:
    builders:
      json_serializable:
        generate_for:
          exclude:
            - "test/**"
```

---

## 5. Archivos Generados y Control de Versiones

### 5.1 Convención de Nombres

| Archivo | Contenido |
|---------|-----------|
| `user.g.dart` | Código generado (json, retrofit, Isar) |
| `user.freezed.dart` | Clases inmutables con freezed |
| `user.g.part` | Partial (usado internamente por freezed) |
| `injection_container.config.dart` | DI generado con injectable |

### 5.2 ¿Comitar .g.dart o No?

**Regla general: SÍ se comitan.**

Razones:
- Los generadores pueden tener breaking changes entre versiones
- Evita que cada dev tenga que ejecutar codegen al clonar
- CI/CD no necesita build_runner para analizar
- Los `.g.dart` suelen ser estables y legibles

**Excepción:** No comitar si:
- El equipo usa CI que siempre ejecuta codegen
- Usas `build.summary` o `build.cache` (no comitar estos)

### 5.3 analysis_options.yaml

```yaml
analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "**/*.config.dart"
    - lib/l10n/gen/*
```

### 5.4 .gitignore

```gitignore
# Opcional: solo si regeneras siempre en CI
# **/*.g.dart

# Cache de build_runner (NUNCA comitar)
.dart_tool/
build/
```

---

## 6. Solución de Problemas

### 6.1 Error: Conflicting Outputs

```
[SEVERE] Conflict: outputs share names
```

**Causa:** Dos builders generan el mismo archivo.

**Solución:**
```yaml
# build.yaml
targets:
  $default:
    builders:
      builder_a:
        generate_for:
          - "lib/feature_a/**"
      builder_b:
        generate_for:
          - "lib/feature_b/**"
```

### 6.2 Error: Stack Overflow / Memoria

```
FATAL: Error during build: Stack Overflow
```

**Causa:** Dependencia circular entre builders o archivos.

**Solución:**
- Separar modelos en archivos más pequeños
- Revisar imports circulares
- Aumentar memoria: `dart run build_runner build --define=build_runner=memory=2048`

### 6.3 Error: Versiones Incompatibles

```
[SEVERE] json_serializable requires builder >=3.0.0
```

**Causa:** Versiones de generadores incompatibles.

**Solución:**
```bash
# Actualizar todo
dart pub upgrade

# Si persiste: verificar constraints en pubspec.yaml
dart pub deps
```

### 6.4 Error: Build Lento

**Causas comunes y soluciones:**

| Problema | Solución |
|----------|----------|
| Muchos archivos sin anotaciones | Usar `generate_for` en build.yaml |
| Builds desde cero cada vez | Usar `watch` en lugar de `build` |
| Demasiados builders | Deshabilitar los que no usas |
| Archivos muy grandes | Dividir en archivos más pequeños |

---

## 7. Flujo de Trabajo Recomendado

### 7.1 Desarrollo Diario

```bash
# Terminal 1: Modo watch
dart run build_runner watch --delete-conflicting-outputs

# Terminal 2: Tu IDE normal
flutter run
```

### 7.2 CI/CD

```yaml
# .github/workflows/ci.yml
jobs:
  build:
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: dart pub get
      - run: dart run build_runner build --delete-conflicting-outputs
      - run: flutter analyze
      - run: flutter test
```

### 7.3 Setup Inicial del Proyecto

```bash
# 1. Agregar dependencias
flutter pub add json_annotation freezed_annotation
flutter pub add dev:build_runner dev:json_serializable dev:freezed

# 2. Crear build.yaml
touch build.yaml

# 3. Ejecutar codegen
dart run build_runner build --delete-conflicting-outputs

# 4. Verificar que se generaron los archivos
git status
```

---

## 8. Errores Comunes y Debugging

### 8.1 Logging Detallado

```bash
# Modo verbose
dart run build_runner build --verbose

# Guardar log
dart run build_runner build 2>&1 | tee build_runner.log
```

### 8.2 Verificar Qué Builders Están Registrados

```bash
# Listar builders disponibles
dart run build_runner build --list-builders
```

### 8.3 Limpiar y Reconstruir

```bash
# Cuando todo falla
dart run build_runner clean
rm -rf .dart_tool
dart pub get
dart run build_runner build --delete-conflicting-outputs
```

---

## 9. Comparativa: build_runner vs Alternativas

| Herramienta | Enfoque | Ventajas | Desventajas |
|-------------|---------|----------|-------------|
| **build_runner** | Análisis de código | Potente, extensible, estándar | Lento en proyectos grandes |
| **macros** (próximamente) | Compile-time | Rápido, integrado en Dart | Aún no estable (Dart 3.7+) |
| **manual** | Script propio | Control total | Mucho trabajo |
| **custom_generators** | Template-based | Rápido para casos simples | Limitado |

> **Nota:** Dart está introduciendo `macros` (experimental desde Dart 3.5+) que eventualmente reemplazarán a build_runner para muchos casos. Sin embargo, build_runner seguirá siendo el estándar por varios años.

---

## 10. Crear un Builder Personalizado

Para equipos que necesitan generación específica:

```yaml
# pubspec.yaml de tu builder
name: my_custom_builder
version: 1.0.0

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  build: ^2.4.0
  source_gen: ^1.5.0
  analyzer: ^6.0.0

builders:
  my_builder:
    import: "package:my_custom_builder/builder.dart"
    builder_factories: ["myBuilder"]
    build_extensions: {".dart": [".my_builder.g.part"]}
    auto_apply: dependents
    build_to: cache
```

```dart
// builder.dart
import 'package:build/build.dart';
import 'package:source_gen/source_gen.dart';

Builder myBuilder(BuilderOptions options) {
  return SharedPartBuilder(
    [MyGenerator()],
    'my_builder',
  );
}

class MyGenerator extends Generator {
  @override
  String generate(LibraryReader library, BuildStep buildStep) {
    // Analizar código y generar
    final classes = library.classes;
    // ... lógica de generación
    return generatedCode;
  }
}
```

---

## 11. Integración con Isar (del proyecto real)

En el monorepo, Isar es el único consumidor de build_runner:

```yaml
# pubspec.yaml
dev_dependencies:
  build_runner: ^2.4.7
  isar_community_generator: ^3.3.2
```

```dart
// Modelo Isar con @Collection
import 'package:isar/isar.dart';

part 'cached_user.g.dart';

@Collection()
class CachedUser {
  @Index(unique: true)
  late String userId;

  late String name;
  late String email;

  Id id = Isar.autoIncrement;
}
```

El generador produce `cached_user.g.dart` con todo el código de serialización y almacenamiento Isar.

### Flujo de Trabajo con Isar

```bash
# 1. Crear/modificar modelo con @Collection()
# 2. Ejecutar código
dart run build_runner build --delete-conflicting-outputs
# 3. Usar el modelo generado
```

---

## 12. Resumen Ejecutivo

1. **build_runner** es el motor de codegen estándar en Dart/Flutter
2. **build.yaml** configura cómo se ejecutan los builders
3. **`--delete-conflicting-outputs`** es tu aliado (úsalo siempre)
4. **Modo watch** para desarrollo, **build** para CI/CD
5. **Los `.g.dart` se comitan** en el repo
6. **`analysis_options.yaml`** debe excluir archivos generados
7. **build_runner + Makefile** = flujo de trabajo predecible

---

## Recursos Adicionales

- [build_runner en pub.dev](https://pub.dev/packages/build_runner)
- [build_config documentation](https://pub.dev/packages/build_config)
- [source_gen package](https://pub.dev/packages/source_gen)
- [Isar Community Generator](https://pub.dev/packages/isar_community_generator)

---

## Ver también

- [`06-json-serializable-freezed.md`](./06-json-serializable-freezed.md) — Serialización con json_serializable + Freezed
- [`07-retrofit-api-client.md`](./07-retrofit-api-client.md) — Clientes HTTP con Retrofit

---

## En el siguiente módulo

**→ [06-json-serializable-freezed.md](./06-json-serializable-freezed.md)** — json_serializable y Freezed para data classes
