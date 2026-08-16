# 01 — Fundamentos de Dependencias

> Cómo declarar dependencias correctamente, entender el lockfile y resolver conflictos.

---

## 1. Estrategia de Versionado

### 1.1 Rangos Caret (`^`)

El `^` es el más usado en pubspec.yaml:

```yaml
dependencies:
  flutter_bloc: ^9.1.1   # >=9.1.1 y <10.0.0
  equatable: ^2.1.0      # >=2.1.0 y <3.0.0
```

**Significado:** `^versión` equivale a `>=versión <siguiente-versión-mayor`.

| Constraint | Rango real |
|---|---|
| `^1.2.3` | `>=1.2.3 <2.0.0` |
| `^0.1.2` | `>=0.1.2 <0.2.0` |
| `^0.0.1` | `>=0.0.1 <0.0.2` |

**Regla de oro:** Usa caret para librerías y paquetes de utility. Permite recibir bugfixes y features menores automáticamente.

### 1.2 Pinning Exacto

```yaml
dependencies:
  next: 16.3.1
  react: 19.2.8
```

**Cuándo usarlo:**
- Frameworks críticos (Next.js, React)
- Paquetes where un cambio menor puede romper la app
- Dependencias que controlas tú y quieres releases explícitos

**Desventaja:** No recibes ni siquiera parches de seguridad automáticos. Cada actualización es manual.

### 1.3 SHA Pinning (GitHub Actions)

```yaml
- uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
```

Esto es **pinning absoluto**. Ni siquiera la etiqueta `v7` puede cambiar por debajo. Es la práctica más segura para CI/CD.

### 1.4 Otras Formas de Declarar

```yaml
# Rango abierto (no recomendado)
  paquete: any

# Rango exacto
  paquete: '>=1.0.0 <2.0.0'

# Sin límite inferior (riesgoso)
  paquete: '<3.0.0'

# Git dependency
  paquete:
    git:
      url: https://github.com/user/paquete.git
      ref: main

# Path dependency (local)
  paquete:
    path: ../mi-paquete
```

> Las dependencias Git y path **no deberían llegar a producción** salvo que sea estrictamente necesario.

---

## 2. `pubspec.lock`

### 2.1 ¿Qué es?

El lockfile **congela** las versiones exactas que resuelve pub después de leer las constraints.

```yaml
# pubspec.lock (fragmento)
packages:
  flutter_bloc:
    dependency: "direct main"
    source: hosted
    version: "9.1.1"
```

### 2.2 ¿Se comitea?

| Tipo de proyecto | ¿Lockfile en git? |
|---|---|
| **App** | ✅ Sí — para que todos los devs usen las mismas versiones exactas |
| **Librería/Paquete** | ❌ No — el lockfile no se distribuye; cada consumidor resuelve sus propias versiones |

### 2.3 Conflictos en Merge

Cuando dos ramas agregan paquetes diferentes:

```bash
<<<<<<< HEAD
    version: "9.1.1"
=======
    version: "10.0.0"
>>>>>>> feature
```

**Solución:** Ejecuta `dart pub get` después del merge. Dart reconstruirá el lockfile resolviendo ambos conjuntos de dependencias.

---

## 3. Resolución de Conflictos

### 3.1 `dart pub deps`

```bash
# Árbol completo
dart pub deps

# Solo dependencias directas
dart pub deps --no-dev

# Formato JSON para CI
dart pub deps --json
```

### 3.2 `dependency_overrides`

Úsalo **temporalmente** para forzar una versión cuando dos paquetes requieren versiones incompatibles:

```yaml
dependency_overrides:
  collection: ^1.18.0
```

> Esto es un parche temporal. El objetivo es que el mantenedor del paquete upstream actualice su constraint.

### 3.2 pubspec_overrides.yaml

A partir de Dart 3.8, pub admite `pubspec_overrides.yaml` como alternativa para overrides locales:

```yaml
# pubspec_overrides.yaml (NO se comitea)
dependency_overrides:
  collection: ^1.19.0
```

A diferencia de `dependency_overrides` en `pubspec.yaml`, este archivo **no se comitea** (debe estar en `.gitignore`). Es ideal para overrides de desarrollo que no deben afectar al resto del equipo.

---

### 3.3 Problema Típico

```
Because every version of flutter_bloc depends on bloc ^9.0.0
  and every version of bloc 10.x depends on bloc >=10.0.0,
  flutter_bloc is incompatible with bloc ^10.0.0.
```

**Diagnóstico:**
1. `dart pub deps` muestra el árbol
2. Identifica qué paquete está causando la incompatibilidad
3. Busca si hay una versión más nueva del paquete que resuelva el conflicto
4. Si no, usa `dependency_overrides` o espera a que los mantenedores actualicen

---

## 4. Convención del Proyecto Real

El monorepo de referencia usa esta estrategia:

| Tipo | Convención | Ejemplo |
|---|---|---|
| Librerías Flutter | Caret `^` | `flutter_bloc: ^9.1.1` |
| Frameworks web | Pinning exacto | `"next": "16.3.1"` |
| GitHub Actions | SHA pinning | `actions/checkout@3d3c42e...` |
| Supabase config | Major version | `major_version = 17` |
| Deno Edge Functions | Rango major | `@supabase/supabase-js@2` |

---

## 5. Ejercicio

Dado este `pubspec.yaml` con conflictos:

```yaml
dependencies:
  flutter_bloc: ^9.1.1
  bloc: ^10.0.0  # incompatible con flutter_bloc ^9.1.1
```

Pasos:
1. Ejecuta `dart pub deps` para ver el error
2. Identifica la versión de `bloc` que necesita `flutter_bloc`
3. Decide: ¿bajas `bloc` o esperas a `flutter_bloc` 10.x?
4. Documenta la decisión en un ADR

---

## Resumen

1. **Caret** (`^`) para librerías — flexibilidad controlada
2. **Pinning exacto** para frameworks críticos
3. **SHA** para Actions de CI/CD
4. **`pubspec.lock`** se comitea en apps
5. **`dependency_overrides`** solo como parche temporal
6. **`dart pub deps`** es tu herramienta de diagnóstico

---

## 📚 Referencias

- [Dart | Pub dependencies](https://dart.dev/tools/pub/dependencies) — Sintaxis de versionado y tipos de dependencias
- [Dart | Pub deps](https://dart.dev/tools/pub/cmd/pub-deps) — Comando `dart pub deps`
- [Dart | Pub upgrade](https://dart.dev/tools/pub/cmd/pub-upgrade) — Comando `dart pub upgrade` y lockfile
- [GitHub | Security hardening for Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions) — SHA pinning en acciones de CI/CD

---

> 📖 **Siguiente:** [02-flujo-actualizacion.md](./02-flujo-actualizacion.md) — Cómo actualizar dependencias sin romper el proyecto
