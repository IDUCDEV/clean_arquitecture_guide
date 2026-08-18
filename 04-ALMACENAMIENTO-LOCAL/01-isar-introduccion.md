# 🗄️ 1. Introducción a Isar Community

> **¿De qué trata esta guía?** De entender qué es Isar Community, por qué usarlo, cómo se integra en un proyecto Flutter con Clean Architecture.

---

## 📋 Índice

1. [¿Qué es Isar?](#1-qué-es-isar)
2. [`isar_community`](#2-isar_community)
3. [Instalación y setup](#3-instalación-y-setup)
4. [Arquitectura de Isar](#4-arquitectura-de-isar)
5. [Code generation](#5-code-generation)
6. [Checklist](#6-checklist)

---

## 1. ¿Qué es Isar?

**Isar** es una base de datos embebida NoSQL diseñada específicamente para Flutter y Dart. A diferencia de SQLite (que usa tablas y SQL), Isar almacena objetos Dart directamente como documentos, similar a MongoDB pero sin servidor.

### 🔑 Características principales

| Característica | Descripción |
|---|---|
| **Embebida** | No necesita servidor. La BD vive en el dispositivo |
| **NoSQL** | Almacena objetos Dart directamente, sin conversión SQL |
| **Rápida** | Escrita en Rust/C++, hasta 10x más rápida que SQLite en benchmarks |
| **Tipada** | Code generation genera APIs completamente tipadas |
| **Isolates** | Operaciones asíncronas que no bloquean la UI |
| **Índices** | Soportados: único, compuesto, hash, case-sensitive |
| **Multi-plataforma** | Android, iOS, macOS, Windows, Linux, Web |
| **Relaciones** | `IsarLink` e `IsarObjects` para relaciones embedidas o referenciadas |

### 🧠 ¿Por qué Isar y no otra cosa?

En el contexto de Clean Architecture, Isar se usa como **almacenamiento local** en la capa de Data, específicamente en `LocalDataSource`. Antes de Isar, el estándar era SharedPreferences para datos simples o SQLite (sqflite) para datos estructurados.

| Aspecto | SharedPreferences | sqflite | Isar |
|---------|------------------|---------|------|
| **Tipo de datos** | Pares clave-valor (strings) | Tablas SQL relacionales | Documentos NoSQL (objetos Dart) |
| **Tipado** | ❌ Manual (json.decode) | ❌ Manual (Row → objeto) | ✅ Automático (code gen) |
| **Velocidad** | Rápido (síncrono) | Medio | Rápido (async + isolates) |
| **Índices** | ❌ No | ✅ Sí | ✅ Sí |
| **Queries complejas** | ❌ No | ✅ SQL | ✅ where/filter |
| **Multi-plataforma** | ✅ Sí | ⚠️ Limitado | ✅ Sí |
| **Ideal para** | Configs, tokens simples | Datos relacionales | Cache de datos + sesión |

---

## 2. `isar_community`

[`isar_community`](https://pub.dev/packages/isar_community) es el package activo y mantenido del ecosistema Isar, compatible con Dart SDK < 4.0 y la opción recomendada para producción hoy. El package original fue abandonado por su creador en 2023.

> **Regla simple:** usa siempre `isar_community`. Los imports usan `package:isar_community/isar.dart`.

---

## 3. Instalación y setup

### 📁 pubspec.yaml

```yaml
dependencies:
  flutter:
    sdk: flutter
  isar_community: ^3.3.2
  path_provider: ^2.1.0      # Para obtener el directorio de la app

dev_dependencies:
  isar_community_generator: ^3.3.2
  build_runner: ^2.4.0
```

### 🚀 Inicialización

Isar necesita un directorio donde almacenar los archivos de la base de datos. El patrón recomendado es un **singleton** que se inicializa al arrancar la app:

```dart
// lib/core/data/local/isar_service.dart
import 'package:isar_community/isar.dart';
import 'package:path_provider/path_provider.dart';
import 'isar_models/cached_user.dart';
import 'isar_models/cached_token.dart';
import 'isar_models/cached_profile.dart';
import 'isar_models/cached_payment_method.dart';

class IsarService {
  static Isar? _instance;

  static Isar get instance {
    if (_instance == null) {
      throw Exception(
        'Isar not initialized. Call IsarService.initialize() first.',
      );
    }
    return _instance!;
  }

  static Future<void> initialize() async {
    if (_instance != null) return;

    final dir = await getApplicationDocumentsDirectory();

    _instance = await Isar.open(
      [
        CachedUserSchema,
        CachedTokenSchema,
        CachedProfileSchema,
        CachedPaymentMethodSchema,
      ],
      directory: dir.path,
      name: 'rifame',
    );
  }

  static Future<void> close() async {
    await _instance?.close();
    _instance = null;
  }

  static Future<void> clear() async {
    await _instance?.writeTxn(() async {
      await _instance!.clear();
    });
  }
}
```

### 🔌 Integración con GetIt (DI)

```dart
// lib/core/di/injection.dart (fragmento)
import 'package:get_it/get_it.dart';
import 'package:isar_community/isar.dart';

final sl = GetIt.instance;

Future<void> initDependencies() async {
  // Isar
  await IsarService.initialize();
  sl.registerLazySingleton<Isar>(() => IsarService.instance);

  // Local DataSources
  sl.registerLazySingleton<AuthLocalDataSource>(
    () => AuthLocalDataSourceImpl(sl<Isar>()),
  );
  sl.registerLazySingleton<ProfileLocalDataSource>(
    () => ProfileLocalDataSourceImpl(sl<Isar>()),
  );
  sl.registerLazySingleton<PaymentMethodLocalDataSource>(
    () => PaymentMethodLocalDataSourceImpl(sl<Isar>()),
  );

  // Session
  sl.registerLazySingleton<UserSession>(
    () => UserSessionImpl(sl<Isar>()),
  );

  // CacheManager
  sl.registerLazySingleton<CacheManager>(() => CacheManager());
}
```

---

## 4. Arquitectura de Isar

### 📊 Modelo de datos

Isar organiza los datos en **colecciones** (similares a tablas en SQL). Cada colección es una clase Dart anotada con `@Collection()`.

```
┌─────────────────────────────────────────────┐
│                Isar Database                │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │  CachedUser (colección)              │   │
│  │  ├── id          (Id, autoincrement) │   │
│  │  ├── userId      (String, único)     │   │
│  │  ├── email       (String)            │   │
│  │  ├── fullName    (String?)           │   │
│  │  ├── phone       (String?)           │   │
│  │  ├── avatarUrl   (String?)           │   │
│  │  ├── cachedAt    (DateTime?)         │   │
│  │  └── expiresAt   (DateTime?)         │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │  CachedToken (colección)             │   │
│  │  ├── id          (Id, autoincrement) │   │
│  │  ├── token       (String, único)     │   │
│  │  ├── cachedAt    (DateTime?)         │   │
│  │  └── expiresAt   (DateTime?)         │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │  CachedProfile (colección)           │   │
│  │  ├── id          (Id, autoincrement) │   │
│  │  ├── userId      (String, único)     │   │
│  │  ├── fullName    (String?)           │   │
│  │  ├── ...                             │   │
│  │  ├── cachedAt    (DateTime?)         │   │
│  │  └── expiresAt   (DateTime?)         │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  ┌──────────────────────────────────────┐   │
│  │  CachedPaymentMethod (colección)     │   │
│  │  ├── id              (Id, autoincrement)│ │
│  │  ├── userId          (String, índice)│   │
│  │  ├── paymentMethodId (String, único) │   │
│  │  ├── type            (String?)       │   │
│  │  ├── ...                             │   │
│  │  ├── cachedAt        (DateTime?)     │   │
│  │  └── expiresAt       (DateTime?)     │   │
│  └──────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### 🔑 Conceptos clave

| Concepto | Descripción |
|----------|-------------|
| **Colección** | Clase Dart con `@Collection()`. Equivale a una tabla |
| **Esquema** | Clase generada automáticamente (`NombreSchema`). Se pasa a `Isar.open()` |
| **Id** | Campo de tipo `Id` (int). Puede ser autoincremental o asignado manualmente |
| **Índice** | `@Index()` en un campo. Acelera queries. `unique: true` para valores únicos |
| **IsarLink** | Relación 1:1 o 1:N entre colecciones |
| **IsarObject** | Objeto embebido dentro de otro (sin colección propia) |

---

## 5. Code generation

### 🔧 Cómo funciona

Isar genera código automáticamente a partir de tus anotaciones. Por cada clase con `@Collection()`, se genera:

1. `NombreSchema` — constante con metadatos de la colección
2. Serializador/Deserializador — convierte entre objeto Dart y almacenamiento binario
3. Query builders — `where()`, `filter()`, `sortBy()` tipados
4. Extensiones de acceso — `isar.colecciones` (getter tipado)

### ▶️ Comandos

```bash
# Una sola ejecución
dart run build_runner build --delete-conflicting-outputs

# Modo watch (regenera automáticamente al cambiar)
dart run build_runner watch --delete-conflicting-outputs
```

### 📄 Archivos generados

```
lib/core/data/local/isar_models/
├── cached_user.dart              # ← Tu código
├── cached_user.g.dart            # ← Generado
├── cached_token.dart
├── cached_token.g.dart
├── cached_profile.dart
├── cached_profile.g.dart
├── cached_payment_method.dart
└── cached_payment_method.g.dart  # ← Generado
```

### ⚠️ Buenas prácticas

- **No editar archivos `.g.dart`**. Se sobrescriben en cada rebuild.
- **Incluir `*.g.dart` en `.gitignore`** o trackearlos (debate abierto). En la práctica, trackearlos evita problemas de versión.
- **Ejecutar `build_runner` después de**: agregar/editar colecciones, agregar/editar índices, cambiar tipos de campos.

---

## 6. Troubleshooting comun

### Error: "Could not find generated Isar schema"

**Causa:** No ejecutaste `build_runner` despues de crear o modificar una coleccion.

```bash
dart run build_runner build --delete-conflicting-outputs
```

### Error: "Class X is not a registered Type"

**Causa:** Olvidaste agregar el `Schema` a `Isar.open()`.

```dart
_instance = await Isar.open(
  [CachedUserSchema, CachedTokenSchema],  // <-- Agrega aqui todos los schemas
  directory: dir.path,
);
```

### Error: "Conflicting outputs"

**Causa:** Archivos `.g.dart` corruptos o en conflicto.

```bash
dart run build_runner build --delete-conflicting-outputs
```

### Error: "Isar has already been opened"

**Causa:** Intentaste abrir Isar dos veces (ej: en tests sin cerrar la instancia anterior).

```dart
// En tests, usa un nombre unico por test group
final isar = await Isar.open(
  [CachedUserSchema],
  directory: dir.path,
  name: 'test_${UniqueKey().toString()}',  // Nombre unico
);
```

### Error: "The getter 'X' is not defined for type 'IsarCollection'"

**Causa:** Los archivos `.g.dart` no estan generados o estan desactualizados.

```bash
# Limpia y regenera
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

---

## 7. Checklist

- [ ] Usé `isar_community` (fork mantenido activamente)
- [ ] Agregué el enlace a https://pub.dev/packages/isar_community como referencia
- [ ] Agregué `isar_community` y `isar_community_generator` a pubspec.yaml
- [ ] Configuré `IsarService` como singleton con lazy initialization
- [ ] Registré Isar en GetIt (o tu DI container)
- [ ] Ejecuté `build_runner build` exitosamente
- [ ] Verifiqué que los archivos `.g.dart` se generaron
- [ ] Los imports usan `package:isar_community/isar.dart`

---

## 📚 Referencias

- [isar_community | pub.dev](https://pub.dev/packages/isar_community) — Paquete activo de Isar para Dart/Flutter
- [Isar | Documentación original](https://isar.dev) — Referencia de operaciones y queries (legacy)

---

**Nivel:** Principiante  
**Siguiente:** [02-modelos-operaciones.md](./02-modelos-operaciones.md)
