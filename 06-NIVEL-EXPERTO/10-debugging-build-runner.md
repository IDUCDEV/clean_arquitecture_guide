# 10: Debugging build_runner

> build_runner es poderoso pero frustrante cuando falla. Aquí están los errores más comunes y cómo arreglarlos.

---

## Los 5 errores más comunes

### 1. "A conflicting output" o "Generated files conflict"

```bash
# Error: Conflicting outputs were detected
```

**Causa:** Archivos generados en ubicación incorrecta o con nombres duplicados.

**Solución:**
```bash
# Limpiar y regenerar
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

---

### 2. "Could not find..."

```bash
# Error: Could not find package:json_serializable
```

**Causa:** Falta dependencia o no se ejecutó `pub get`.

**Solución:**
```bash
flutter pub get
dart run build_runner build
```

---

### 3. Error de importación circular

```dart
// ❌ ERROR: Import circular
// model_a.dart importa model_b.dart
// model_b.dart importa model_a.dart
```

**Solución:** Extraer tipos comunes a un archivo separado o usar `part`/`part of`.

---

### 4. Generación lenta o stuck

```bash
# build_runner tarda mucho o se cuelga
```

**Solución:**
```bash
# Usar build_runner con más memoria
dart run build_runner build --delete-conflicting-outputs

# O para desarrollo continuo:
dart run build_runner watch --delete-conflicting-outputs
```

---

### 5. "The getter 'X' isn't defined for the class 'Y'"

**Causa:** El código generado tiene errores porque la fuente tiene errores.

**Solución:**
1. Arreglar errores en el código fuente primero
2. Ejecutar `dart analyze` para verificar
3. Regenerar

```bash
dart analyze
dart run build_runner build --delete-conflicting-outputs
```

---

## Comandos esenciales

```bash
# Build completo
dart run build_runner build --delete-conflicting-outputs

# Watch mode (regenera al cambiar)
dart run build_runner watch --delete-conflicting-outputs

# Limpiar archivos generados
dart run build_runner clean

# Ver qué se va a generar
dart run build_runner build --dry-run
```

---

## Paquetes que usan build_runner

| Paquete | Para qué |
|---------|----------|
| `json_serializable` | JSON serialization |
| `freezed` | Immutables + equality |
| `injectable` | Dependency injection |
| `auto_route` | Routing |
| `source_gen` | Custom generators |

---

## Checklist de debugging

```
□ ¿flutter pub get se ejecutó?
□ ¿Hay errores de análisis? (dart analyze)
□ ¿Hay imports circulares?
□ ¿Se usa --delete-conflicting-outputs?
□ ¿Se limpió con clean antes?
```

---

**Volver al índice:** [README.md](./README.md)
