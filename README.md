# 📚 Clean Architecture Guide para Flutter

> Una guía completa y práctica para implementar **Clean Architecture** en tus proyectos Flutter, desde los conceptos básicos hasta el testing avanzado.

---

## 🎯 ¿Qué es Clean Architecture?

Clean Architecture es una forma de organizar el código en **capas independientes** donde cada capa tiene una responsabilidad específica:

```
┌─────────────────────────────────────────────┐
│           PRESENTATION (UI)                 │
│   Widgets, Pages, Cubits/BLoCs             │
├─────────────────────────────────────────────┤
│              DOMAIN (Lógica)                │
│   Entities, UseCases, Repository Interfaces │
├─────────────────────────────────────────────┤
│                DATA (Datos)                 │
│   Models, DataSources, Repository Impl      │
└─────────────────────────────────────────────┘
```

### ¿Por qué usarla?

- ✅ **Código mantenible** - Cada cambio está aislado
- ✅ **Fácil de testear** - Cada capa se prueba por separado
- ✅ **Escalable** - Añadir features sin romper existentes
- ✅ **Framework independiente** - Tu lógica no depende de Flutter

---

## 📁 Estructura de la Guía

Esta guía está organizada en **tres partes principales**:

### 1️⃣ Guía de Implementación

| Archivo | Descripción |
|---------|-------------|
| [CLEAN_ARCHITECTURE_GUIDE.md](./CLEAN_ARCHITECTURE_GUIDE.md) | Guía completa con todos los detalles |
| [🏗️ 3 - GUÍA GENERAL](./🏗️%203%20-%20GUÍA%20GENERAL%20Clean%20Architecture%20para%20Cualquier%20Proyecto%20Flutter.md) | Guía general extendida con ejemplos |
| [🎯 1- GUÍA SIMPLE](./🎯%201-%20GUÍA%20SIMPLE%20Clean%20Architecture%20Paso%20a%20Paso.md) | Introducción rápida |

### 2️⃣ Guía de Testing

La guía de testing te enseña a probar cada capa de tu aplicación:

| Carpeta | Contenido |
|---------|-----------|
| [testing/](./testing/) | Directorio principal |

#### Estructura de la Guía de Testing:

```
testing/
├── README.md                         ← Índice de la guía
│
├── PARTE 1: FUNDAMENTOS
├── 01-fundamentos.md                 ← Teoría: Conceptos, AAA, setup
├── 01a-practica-primeros-tests.md  ← Práctica: Primeros tests
│
├── PARTE 2: DOMAIN
├── 02-domain-testing.md              ← Teoría: Entities, UseCases, Fakes
├── 02a-practica-fakes-manuales.md  ← Práctica: Crear Fakes paso a paso
│
├── PARTE 3: DATA
├── 03-data-testing.md              ← Teoría: Models, DataSources, Repos
├── 03a-practica-fixtures-models.md ← Práctica: Fixtures JSON
├── 03b-practica-datasources.md      ← Práctica: Remote/Local DataSources
├── 03c-practica-repositories.md    ← Práctica: Repository Implementation
│
├── PARTE 4: PRESENTATION
├── 04-presentation-testing.md      ← Teoría: Cubits, Widgets
├── 04a-practica-cubits-bloc-test.md← Práctica: Tests con bloc_test
├── 04b-practica-widgets.md         ← Práctica: Widget tests
│
├── PARTE 5: CORE
├── 05-core-testing.md              ← Teoría: NetworkInfo, Services
├── 05a-practica-core-services.md  ← Práctica: Services
│
├── PARTE 6: AVANZADO
├── 06-advanced-testing.md          ← Teoría: Coverage, CI/CD
├── 06a-practica-coverage-ci.md     ← Práctica: GitHub Actions
│
└── PARTE 7: MIGRACIÓN
    ├── 07-migration-to-mockito.md  ← Teoría: Cuándo usar Mockito
    └── 07a-practica-migration.md   ← Práctica: Migrar Fakes a Mocks
```

---

## 🚀 Cómo Usar Esta Guía

### Si eres nuevo en Clean Architecture:

1. **Empieza por la guía básica:**
   - Lee [🎯 1- GUÍA SIMPLE](./🎯%201-%20GUÍA%20SIMPLE%20Clean%20Architecture%20Paso%20a%20Paso.md)

2. **Profundiza con la guía completa:**
   - Lee [CLEAN_ARCHITECTURE_GUIDE.md](./CLEAN_ARCHITECTURE_GUIDE.md)

3. **Implementa tu primera feature:**
   - Sigue los templates de la sección 4

### Si ya conoces Clean Architecture y quieres aprender testing:

1. **Fundamentos (1-2 horas):**
   - [01-fundamentos.md](./testing/01-fundamentos.md)
   - [01a-practica-primeros-tests.md](./testing/01a-practica-primeros-tests.md)

2. **Domain + Fakes (2-3 horas):**
   - [02-domain-testing.md](./testing/02-domain-testing.md)
   - [02a-practica-fakes-manuales.md](./testing/02a-practica-fakes-manuales.md)

3. **Data Layer (3-4 horas):**
   - [03-data-testing.md](./testing/03-data-testing.md)
   - [03a-practica-fixtures-models.md](./testing/03a-practica-fixtures-models.md)
   - [03b-practica-datasources.md](./testing/03b-practica-datasources.md)
   - [03c-practica-repositories.md](./testing/03c-practica-repositories.md)

4. **Presentation (2-3 horas):**
   - [04-presentation-testing.md](./testing/04-presentation-testing.md)
   - [04a-practica-cubits-bloc-test.md](./testing/04a-practica-cubits-bloc-test.md)
   - [04b-practica-widgets.md](./testing/04b-practica-widgets.md)

---

## 📦 Estructura de Carpetas Recomendada

```
lib/
├── core/
│   ├── common/           # Clases base (UseCase), helpers
│   ├── di/               # Inyección de dependencias (GetIt)
│   ├── error/            # Failures y Exceptions
│   ├── network/          # Configuración de red
│   ├── routing/          # Navegación (GoRouter)
│   ├── services/         # Servicios externos
│   ├── utils/            # Utilidades
│   └── widgets/          # Widgets compartidos
│
└── features/
    └── feature_name/
        ├── data/
        │   ├── datasources/
        │   │   ├── remote/
        │   │   └── local/
        │   ├── models/
        │   └── repositories/
        ├── domain/
        │   ├── entities/
        │   ├── repositories/
        │   └── usecases/
        └── presentation/
            ├── cubit/
            ├── pages/
            └── widgets/
```

---

## 🧪 Testing por Capas

| Capa | Qué Testear | Herramientas |
|------|-------------|--------------|
| **Domain** | Entities, UseCases | `flutter_test` |
| **Data** | Models, DataSources, Repositories | `flutter_test`, Fakes |
| **Presentation** | Cubits, Widgets | `bloc_test`, `flutter_test` |
| **Core** | NetworkInfo, Services | `flutter_test` |

### ¿Por qué Fakes en lugar de Mocks?

| Aspecto | Fakes Manuales | Mocks (Mockito) |
|---------|----------------|-----------------|
| **Curva de aprendizaje** | Baja | Alta |
| **Debugging** | Fácil | Difícil |
| **Mantenimiento** | Simple | Complejo |

> **Nuestra recomendación:** Empieza con Fakes manuales. Cuando tengas confianza, podrás migrar a Mockito si lo necesitas.

---

## 📖 Conceptos Clave

### Entities vs Models

- **Entity**: Objeto de negocio puro (solo datos, sin métodos)
- **Model**: Entity con lógica de serialización (`fromJson`, `toJson`)

### UseCase

Representa una **acción** que el usuario puede realizar. Ejemplo: `LoginUseCase`, `GetUsersUseCase`.

### Repository Pattern

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   UseCase   │ ──→ │ Repository       │ ──→ │ DataSource  │
│             │     │ (Interfaz)       │     │ (HTTP/DB)   │
└─────────────┘     └──────────────────┘     └─────────────┘
```

### Either<Failure, Success>

Patrón funcional para manejo de errores:

```dart
Future<Either<Failure, User>> login(String email, String password) async {
  if (success) {
    return Right(user);  // Éxito
  } else {
    return Left(error);  // Error
  }
}
```

---

## 🛠️ Dependencias Recomendadas

```yaml
dependencies:
  # State Management
  flutter_bloc: ^8.1.3
  equatable: ^2.0.5
  
  # Dependency Injection
  get_it: ^7.6.4
  
  # Functional Programming
  dartz: ^0.10.1
  
  # Networking
  dio: ^5.3.3
  internet_connection_checker: ^1.0.0+1
  
  # Storage
  shared_preferences: ^2.2.2
  sqflite: ^2.3.0
  
  # Routing
  go_router: ^12.1.3

dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0
  mockito: ^5.4.0
  build_runner: ^2.10.2
```

---

## 📚 Recursos Adicionales

- [Documentación oficial de BLoC](https://bloclibrary.dev/)
- [Documentación de Flutter](https://flutter.dev/docs)
- [Clean Architecture por Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## 🤝 Contribuir

Esta guía es de código abierto. Si quieres mejorarla:

1. Haz fork del repositorio
2. Crea una rama para tu feature
3. Envía un pull request

---

## 📄 Licencia

MIT License - Libre de usar y modificar.

---

**Última actualización:** 2026-02-25  
**Versión:** 2.0.0
