# 📚 Clean Architecture Guide para Flutter

> Una guía completa y práctica para implementar **Clean Architecture** en tus proyectos Flutter, desde los conceptos básicos hasta el testing avanzado. Actualizada con **fpdart** para manejo funcional de errores.

---

## 🎯 ¿Qué es Clean Architecture?

Clean Architecture es una forma de organizar el código en **capas independientes** donde cada capa tiene una responsabilidad específica:

```
┌─────────────────────────────────────────────┐
│           PRESENTATION (UI)                 │
│   Widgets, Pages, Cubits/BLoCs             │
├─────────────────────────────────────────────┤
│              DOMAIN (Lógica)               │
│   Entities, UseCases, Repository Interfaces │
├─────────────────────────────────────────────┤
│                DATA (Datos)                │
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

### 1️⃣ Guía Completa Unificada

| Archivo | Descripción |
|---------|-------------|
| [📚 GUÍA COMPLETA](./📚%20GUÍA%20COMPLETA%20-%20Clean%20Architecture%20Unificada.md) | Guía completa con Implementación, Testing, Templates y fpdart |

La guía unificada incluye:
- Introducción y Filosofía
- Las 4 Capas de Clean Architecture
- Estructura de Carpetas
- Flujo de Datos
- Implementación Práctica: Sistema de Usuarios CRUD
- Inyección de Dependencias con GetIt
- Testing por Capas
- Templates Universales
- Comparación: `Future<Either>` vs `TaskEither`
- Decisiones de Arquitectura
- Migración desde Código Espagueti

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
### 3️⃣ Guía de Uso Inteligente de IA

Aprende a usar herramientas de IA como asistente en tu desarrollo, manteniendo el control sobre la lógica crítica de tu aplicación:

| Archivo | Descripción |
|---------|-------------|
| [🤖 GUÍA - Uso Inteligente de IA](./🤖%20GUÍA%20-%20Uso%20Inteligente%20de%20IA%20en%20Desarrollo%20Flutter.md) | Framework AIDR, prompts optimizados y estrategias por capa |
| [🤖 PRÁCTICA - Sistema de Reservas](./🤖%20PRÁCTICA%20-%20Sistema%20de%20Reservas%20con%20Enfoque%20Híbrido.md) | Caso de estudio completo aplicando el enfoque híbrido IA + Código Manual |

### 4️⃣ Nivel Experto (Arquitectura Escalable)

Conceptos avanzados para llevar tus proyectos a nivel de producción profesional:

| Archivo | Descripción |
|---------|-------------|
| [02 - Automatización DI con Injectable](./🚀%204%20-%20NIVEL%20EXPERTO/02-automatizacion-di-injectable.md) | Elimina el boilerplate con generación de código |
| [03 - Comunicación entre Features](./🚀%204%20-%20NIVEL%20EXPERTO/03-comunicacion-entre-features.md) | Estrategias de desacoplamiento para apps grandes |
| [04 - Streams y Tiempo Real](./🚀%204%20-%20NIVEL%20EXPERTO/04-streams-y-tiempo-real.md) | Implementación de StreamUseCases (Firebase/WebSockets) |

---

## 🚀 Cómo Usar Esta Guía

```
┌─────────────────────────────────────────────────────────┐
│  Distribución Sugerida del Tiempo en una Feature        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   IA (70%)                   Manual (30%)               │
│   ┌──────────────┐           ┌──────────────┐           │
│   │ • Estructura │           │ • Lógica de  │           │
│   │ • Boilerplate│           │   negocio    │           │
│   │ • Scaffolding│           │ • Validaciones│          │
│   │ • Tests base │           │ • Edge cases │           │
│   │ • Documentación│         │ • Debugging  │           │
│   └──────────────┘           └──────────────┘           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

#### Marco AIDR (4 Pasos):

| Paso | Descripción |
|------|-------------|
| **A**nalyze | Analiza tú primero el problema antes de preguntar a IA |
| **I**nvestigate | Investiga con IA patrones y soluciones (solo buscar información) |
| **D**ecide | Decide qué va a IA (boilerplate) y qué haces tú (lógica crítica) |
| **R**eview | Revisa y valida todo lo que generó IA |

#### Qué hacer tú vs qué delegar a IA:

| Componente | Boilerplate (IA) | Lógica Crítica (Tú) |
|------------|------------------|---------------------|
| **Domain** | Entity, Repository Interface | UseCases, Validaciones |
| **Data** | Models (fromJson/toJson), DataSources | Repository Implementation, Cache Strategy |
| **Presentation** | Estados de Cubit, Layout base | Validación de formularios, Interacciones |
| **Testing** | Scaffold de tests, Arrange repetitivo | Aserciones, Edge cases |

---

## 🚀 Cómo Usar Esta Guía

### Si eres nuevo en Clean Architecture:

1. **Lee la guía completa unificada:**
   - [📚 GUÍA COMPLETA](./📚%20GUÍA%20COMPLETA%20-%20Clean%20Architecture%20Unificada.md)
   - Empieza por la introducción y filosofía
   - Sigue el ejemplo práctico paso a paso

2. **Implementa tu primera feature:**
   - Usa los templates universales provistos
   - Sigue el ejemplo del Sistema de Usuarios CRUD

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

### Si quieres usar IA de forma inteligente en tu desarrollo:

1. **Fundamentos (30 min):**
   - Lee [🤖 GUÍA - Uso Inteligente de IA](./🤖%20GUÍA%20-%20Uso%20Inteligente%20de%20IA%20en%20Desarrollo%20Flutter.md)
   - Entiende el framework AIDR (Analyze, Investigate, Decide, Review)

2. **Prompts y estrategias (30 min):**
   - Revisa los prompts optimizados por capa de Clean Architecture
   - Descarga el cheat sheet de prompts

3. **Caso práctico (1-2 horas):**
   - Sigue el [Sistema de Reservas con Enfoque Híbrido](./🤖%20PRÁCTICA%20-%20Sistema%20de%20Reservas%20con%20Enfoque%20Híbrido.md)
   - Aplica el framework a tu propio proyecto

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

Patrón funcional para manejo de errores usando **fpdart**:

```dart
Future<Either<Failure, User>> login(String email, String password) async {
  if (success) {
    return Either.right(user);  // Éxito (Right = Success)
  } else {
    return Either.left(error);  // Error (Left = Failure)
  }
}
```

**Manejo del resultado:**

```dart
final result = await login(email, password);

result.match(
  (failure) => print('Error: $failure'),  // Left
  (user) => print('Usuario: ${user.name}'),  // Right
);
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
  
  # Functional Programming (fpdart - reemplazo moderno de dartz)
  fpdart: ^1.2.0
  
  # Networking
  dio: ^5.3.3
  internet_connection_checker: ^1.0.0+1
  
  # Storage
  isar_community: ^3.3.2
  isar_community_flutter_libs: ^3.3.2
  path_provider: ^2.1.2
  sqflite: ^2.3.0
  shared_preferences: ^2.2.2
  
  # Routing
  go_router: ^12.1.3

dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0
  mockito: ^5.4.0
  build_runner: ^2.4.7
  isar_community_generator: ^3.3.2
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

**Última actualización:** 2026-03-26  
**Versión:** 3.0.0
