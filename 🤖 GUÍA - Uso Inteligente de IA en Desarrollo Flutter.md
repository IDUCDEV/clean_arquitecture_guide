# 🤖 Guía: Uso Inteligente de IA en Desarrollo Flutter

> Equilibrio entre la asistencia de IA y la escritura manual de código para mantener tus habilidades técnicassharp

---

## 📋 Tabla de Contenidos

1. [Filosofía: Por Qué Buscar el Balance](#1-filosofía)
2. [El Framework AIDR](#2-framework-aidr)
3. [Boilerplate vs Lógica Crítica](#3-boilerplate-vs-lógica-crítica)
4. [Estrategias por Capa de Clean Architecture](#4-estrategias-por-capa)
5. [Guía de Prompts Optimizados](#5-guía-de-prompts)
6. [Caso de Uso Completo: Feature de Login](#6-caso-de-uso-completo)
7. [Testing Híbrido: Boilerplate IA + Lógica Manual](#7-testing-híbrido)
8. [Checklist Diario de Referencia Rápica](#8-checklist-diario)

---

## 1. Filosofía: Por Qué Buscar el Balance

### 🚨 El Problema de Depender 100% de IA

```
❌ Dependencia Total de IA          ✅ Balance Inteligente
─────────────────────              ─────────────────────
• Escribes código sin              • Entiendes el código
  entenderlo                         que escribes
• No reconoces errores              • Detectas errores
  básicos                            rápidamente
• Esperas que IA resuelva          • Usas IA como
  todo                               asistente
• Perdidas habilidades             • Mantienes y mejoras
  de debugging                       habilidades
• Ansiedad cuando IA               • Funcionas sin IA
  falla o está unavailable           cuando es necesario
```

### 🎯 Por Qué Mantener la Práctica Manual

| Razón | Impacto a Largo Plazo |
|-------|----------------------|
| **Memoria muscular** | Escribir código forma patrones mentales que IA no puede reemplazar |
| **Depuración efectiva** | Entiendes errores porque conoces la sintaxis |
| **Decisiones arquitectónicas** | Sabes cuándo y por qué elegir un patrón |
| **Comunicación técnica** | Puedes explicar tu código a otros devs |
| **Entrevistas técnicas** | Puedes codificar sin asistencia de IA |
| **Mantenimiento** | Entiendes código legacy sin documentación |

### ⚖️ La Regla del 70/30

> **70% IA / 30% Manual** es el balance ideal para proyectos reales

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
│   │ • Refactoring│           │ • Decisiones │           │
│   │   básico     │           │   arch.      │           │
│   └──────────────┘           └──────────────┘           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Framework AIDR

> Método de 4 pasos para decidir cuándo usar IA y cuándo escribir manualmente

### El Acrónimo

```
A I D R
│ │ │ │
│ │ │ └── Review: Revisa y valida lo que generó IA
│ │ └──── Decide: Decide qué va a IA y qué haces tú
│ └────── Investigate: Investiga con IA patrones/soluciones
└──────── Analyze: Analiza tú primero el problema
```

### Paso 1: ANALYZE - Análisis Personal (Siempre Primero)

```markdown
Antes de tocar tu teclado o preguntar a IA:

□ ¿Entiendo completamente el problema?
□ ¿Cuáles son los requisitos funcionales?
□ ¿Hay constraints técnicos (performance, seguridad)?
□ ¿Cómo se integra esto con el resto de la app?
□ ¿Qué podría fallar? (identificar edge cases)
□ ¿Necesito crear algo nuevo o modificar algo existente?
```

**Ejemplo de análisis mental:**
```
Feature: "Notificaciones push cuando llega un pedido"

Análisis:
├── Problema: El usuario necesita saber cuando su pedido cambia de estado
├── Entidades involucradas: Order, Notification, User
├── Flujo: OrderUpdated → PushNotificationService → Firebase/OneSignal
├── Edge cases: 
│   ├── Usuario sin permisos de notificación
│   ├── Dispositivo offline
│   └── Rate limiting de notificaciones
└── Decisión: Esto es lógica de negocio → LO HAGO YO
```

### Paso 2: INVESTIGATE - Investigación con IA

```markdown
Investigar con IA es buscar información, NO ejecutar código:

✅ INVESTIGAR con IA:
├── "Patrones para manejo de estado offline en Flutter"
├── "Cómo estructurar repositories con cache en Clean Architecture"
├── "Best practices para validar formularios en Dart"
├── "Estrategias de retry con exponencial backoff"
└── "Comparación entre Riverpod y Cubit para mi caso"

❌ NO INVESTIGUES (esto es DECIDIR):
├── "Crea un AuthRepository con login y logout"
├── "Escribe un UseCase para getUserProfile"
└── "Genera el código completo del NotificationService"
```

### Paso 3: DECIDE - Decisión de Responsabilidad

```
┌────────────────────────────────────────────────────────────┐
│                    MATRIZ DE DECISIÓN                      │
├─────────────────────┬──────────────────┬───────────────────┤
│     TAREA           │    ¿IA O MANUAL? │     POR QUÉ       │
├─────────────────────┼──────────────────┼───────────────────┤
│ Estructura feature  │      🤖 IA       │ Boilerplate puro   │
│ Naming classes      │      🤖 IA       │ Sugiere opciones   │
│ Boilerplate tests   │      🤖 IA       │ Setup repetitivo   │
│ Lógica de negocio   │      ✍️ MANUAL   │ Tu diferenciador  │
│ Validaciones        │      ✍️ MANUAL   │ Reglas de tu app   │
│ Edge cases          │      ✍️ MANUAL   │ Conocimiento dominio│
│ Repository impl.    │      🤖 IA       │ Patrón conocido    │
│ UseCase crítico     │      ✍️ MANUAL   │ Decisiones negocio │
│ DataSource boiler.  │      🤖 IA       │ Estructura repet.  │
│ Excepciones custom  │      ✍️ MANUAL   │ Lógica específica  │
│ Tests de lógica     │      ✍️ MANUAL   │ Aserciones negocio │
│ Tests de estructura│      🤖 IA       │ Arrange repetitivo │
│ Depuración errors   │      🤖 IA       │ Análisis rápido    │
│ Refactoring         │      🤖 IA       │ Mechanical work    │
└─────────────────────┴──────────────────┴───────────────────┘
```

### Paso 4: REVIEW - Revisión y Validación

```markdown
Después de recibir código de IA, SIEMPRE haz:

□ ¿Entiendo cada línea de este código?
□ ¿Hay algo que no reconocería si me preguntaran?
□ ¿El código sigue las convenciones del proyecto?
□ ¿Maneja todos los edge cases relevantes?
□ ¿Hay security concerns (no hardcoded secrets)?
□ ¿El código es maintainable para otros devs?
□ ¿Las variable/function names son descriptivas?
□ ¿Los tests cubren el happy path y casos de error?

⚠️ SI RESPONDES "NO" A CUALQUIERA → Reescribe esa sección manualmente
```

---

## 3. Boilerplate vs Lógica Crítica

### 📦 Definición: Boilerplate

> Código repetitivo, predecible, que sigue patrones establecidos.

**Características:**
- Estructura conocida y repetitiva
- No requiere conocimiento del dominio
- Fácil de generar y mantener
-Cambios frecuentes pero predecibles

**Ejemplos por capa:**

| Capa | Ejemplos de Boilerplate |
|------|------------------------|
| **Domain** | Skeleton de Entity, Interface de Repository |
| **Data** | Model.fromJson(), DataSource genérico, Repository implementation |
| **Presentation** | Estados de Cubit (Loading, Success, Error), Page base |
| **Core** | Configuración de Dio, setup de GetIt |
| **Tests** | setUp(), tearDown(), arrange sections |

### 🧠 Definición: Lógica Crítica

> Código que contiene las reglas de negocio, validaciones, y decisiones que definen cómo funciona tu aplicación.

**Características:**
- Diferencia tu app de otras
- Requiere conocimiento del dominio
- Costoso de cambiar después
- Fuente principal de bugs si se hace mal

**Ejemplos por capa:**

| Capa | Ejemplos de Lógica Crítica |
|------|---------------------------|
| **Domain** | Validaciones en UseCase, reglas de negocio en Entities |
| **Data** | Merge de cache/remote, transformación de datos específica |
| **Presentation** | Validación de formularios, lógica de UI compleja |
| **Core** | Auth token refresh logic, retry policies |

### 🔄 Conversión de Boilerplate a Lógica (Ejemplo)

```
┌─────────────────────────────────────────────────────────────────┐
│                    BOILERPLATE (🤖 IA)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  // Esto lo hace IA:                                            │
│  class OrderRepositoryImpl implements OrderRepository {         │
│    final RemoteDataSource remoteDataSource;                      │
│    final LocalDataSource localDataSource;                       │
│                                                                 │
│    OrderRepositoryImpl({                                        │
│      required this.remoteDataSource,                            │
│      required this.localDataSource,                             │
│    });                                                           │
│                                                                 │
│    @override                                                                    │
│    Future<Either<Failure, List<Order>>> getOrders() async {    │
│      // Boilerplate: try-catch + Either                        │
│    }                                                            │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LÓGICA CRÍTICA (✍️ TÚ)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  // Esto lo haces TÚ:                                           │
│  @override                                                      │
│  Future<Either<Failure, List<Order>>> getOrders() async {      │
│    // 1. ¿Hay conexión?                                         │
│    final isOnline = await networkInfo.isConnected;             │
│                                                                 │
│    // 2. Lógica de cache:                                       │
│    //   - Online: fetch remote, guardar en cache               │
│    //   - Offline: verificar si hay datos frescos (<24h)       │
│    //   - Offline sin datos frescos: Mostrar error específico  │
│                                                                 │
│    // 3. Decisiones de negocio:                                 │
│    //   - ¿Ordenar por fecha?                                   │
│    //   - ¿Filtrar por estado?                                  │
│    //   - ¿Ocultar órdenes antiguas?                          │
│                                                                 │
│    // 4. Transformaciones específicas:                         │
│    //   - Calcular totales                                      │
│    //   - Formatear fechas para display                         │
│    //   - Enriquecer con datos del usuario                     │
│  }                                                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Estrategias por Capa

### 🏗️ Domain Layer

```
┌────────────────────────────────────────────────────────────────┐
│                    DOMAIN LAYER                                │
├──────────────────────┬───────────────────┬───────────────────┤
│      Componente      │    Responsabilidad │    Quién lo hace   │
├──────────────────────┼───────────────────┼───────────────────┤
│ Entity               │ Definir modelo     │ 🤖 IA (scaffold)  │
│                      │ Lógica de dominio  │ ✍️ TÚ              │
├──────────────────────┼───────────────────┼───────────────────┤
│ Repository Interface │ Definir контракт  │ 🤖 IA (scaffold)  │
│                      │ Métodos necesarios │ ✍️ TÚ (decidir)   │
├──────────────────────┼───────────────────┼───────────────────┤
│ UseCase              │ Implementación     │ ✍️ TÚ (SIEMPRE)   │
│                      │ Lógica de negocio  │ ✍️ TÚ (SIEMPRE)   │
├──────────────────────┼───────────────────┼───────────────────┤
│ Failure              │ Definir errores    │ 🤖 IA (enum/cls)  │
│                      │ Casos específicos  │ ✍️ TÚ              │
└──────────────────────┴───────────────────┴───────────────────┘
```

**🎯 Regla de Oro Domain:**
> **Los UseCases son sagrado. Siempre los escribes tú.**

```dart
// ✅ BIEN: UseCase escrito por ti (lógica de negocio)
class GetOrdersUseCase {
  Future<Either<Failure, List<Order>>> call(GetOrdersParams params) async {
    // Tu lógica de negocio aquí:
    
    // 1. Validar parámetros
    if (params.userId.isEmpty) {
      return const Left(ValidationFailure('User ID is required'));
    }

    // 2. Verificar permisos
    final hasPermission = await checkUserPermission(params.userId);
    if (!hasPermission) {
      return const Left(AuthFailure('No permission to view orders'));
    }

    // 3. Obtener datos
    final result = await repository.getOrders(params);

    // 4. Post-procesamiento (transformación específica)
    return result.map((orders) {
      return orders
          .where((order) => order.status != OrderStatus.cancelled)
          .toList()
        ..sort((a, b) => b.createdAt.compareTo(a.createdAt));
    });
  }
}

// ❌ MAL: UseCase generado por IA sin entender el negocio
class GetOrdersUseCase {
  Future<Either<Failure, List<Order>>> call(GetOrdersParams params) async {
    return await repository.getOrders(params); // Solo un wrapper
  }
}
```

### 📊 Data Layer

```
┌────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                  │
├──────────────────────┬───────────────────┬───────────────────┤
│      Componente      │    Responsabilidad │    Quién lo hace   │
├──────────────────────┼───────────────────┼───────────────────┤
│ Model                │ fromJson/toJson   │ 🤖 IA (scaffold)  │
│                      │ Lógica de mapping │ ✍️ TÚ              │
├──────────────────────┼───────────────────┼───────────────────┤
│ RemoteDataSource     │ API calls         │ 🤖 IA (estructure) │
│                      │ Manejo errores API│ ✍️ TÚ              │
├──────────────────────┼───────────────────┼───────────────────┤
│ LocalDataSource       │ Cache/DB          │ 🤖 IA (scaffold)  │
│                      │ Estrategia cache   │ ✍️ TÚ              │
├──────────────────────┼───────────────────┼───────────────────┤
│ Repository Impl      │ Lógica de merge   │ ✍️ TÚ (SIEMPRE)   │
│                      │ Offline/online     │ ✍️ TÚ (SIEMPRE)   │
└──────────────────────┴───────────────────┴───────────────────┘
```

**🎯 Regla de Oro Data:**
> **El Repository Implementation es tu cerebro. Siempre lo escribes tú.**

```dart
// ✅ BIEN: Repository con estrategia de cache clara (escrito por ti)
class OrderRepositoryImpl implements OrderRepository {
  // ... dependencias

  @override
  Future<Either<Failure, List<Order>>> getOrders() async {
    final isOnline = await networkInfo.isConnected;

    if (isOnline) {
      // Online: Fetch from API
      try {
        final remoteOrders = await remoteDataSource.getOrders();
        
        // Guardar en cache para offline
        await localDataSource.cacheOrders(remoteOrders);
        
        return Right(remoteOrders);
      } on ServerException catch (e) {
        // Si falla API, intentar cache
        return await _getFromCache();
      }
    } else {
      // Offline: Solo cache
      return await _getFromCache();
    }
  }

  Future<Either<Failure, List<Order>>> _getFromCache() async {
    final cachedOrders = await localDataSource.getCachedOrders();
    
    if (cachedOrders.isEmpty) {
      return const Left(CacheFailure('No cached data available'));
    }
    
    // Verificar freshness del cache (24 horas)
    final isFresh = await _isCacheFresh();
    if (!isFresh) {
      // Cache válido pero puede estar outdated
      // El UI puede mostrar warning
    }
    
    return Right(cachedOrders);
  }

  Future<bool> _isCacheFresh() async {
    final lastFetch = await localDataSource.getLastFetchTime();
    final difference = DateTime.now().difference(lastFetch);
    return difference.inHours < 24;
  }
}
```

### 🎨 Presentation Layer

```
┌────────────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                             │
├──────────────────────┬───────────────────┬───────────────────┤
│      Componente      │    Responsabilidad │    Quién lo hace   │
├──────────────────────┼───────────────────┼───────────────────┤
│ States (Cubit/BLoC) │ Definir estados   │ 🤖 IA (scaffold)  │
│                      │ Transiciones      │ ✍️ TÚ              │
├──────────────────────┼───────────────────┼───────────────────┤
│ Cubit/BLoC logic     │ Llamar UseCases   │ 🤖 IA (estructure)│
│                      │ Lógica de UI      │ ✍️ TÚ              │
├──────────────────────┼───────────────────┼───────────────────┤
│ Pages/Widgets        │ Layout y UI       │ 🤖 IA (boilerplate)│
│                      │ Interacciones     │ ✍️ TÚ              │
│                      │ Validaciones UI   │ ✍️ TÚ              │
└──────────────────────┴───────────────────┴───────────────────┘
```

**🎯 Regla de Oro Presentation:**
> **La validación de formularios y la lógica de interacción siempre la haces tú.**

```dart
// ✅ BIEN: Validación en Cubit (lógica de UI crítica)
class LoginCubit extends Cubit<LoginState> {
  // ...

  void onEmailChanged(String email) {
    final emailError = _validateEmail(email);
    emit(state.copyWith(
      email: email,
      emailError: emailError,
      isFormValid: _isFormValid(email: email, password: state.password),
    ));
  }

  String? _validateEmail(String email) {
    if (email.isEmpty) return 'Email is required';
    if (!email.contains('@')) return 'Invalid email format';
    if (!email.contains('.')) return 'Invalid email format';
    // Reglas específicas de TU app:
    if (email.length > 100) return 'Email too long';
    if (email.contains(' ')) return 'Email cannot contain spaces';
    return null;
  }

  bool _isFormValid({required String email, required String password}) {
    return _validateEmail(email) == null && 
           _validatePassword(password) == null;
  }
}

// ❌ MAL: Validación minima o ausente
class LoginCubit extends Cubit<LoginState> {
  void onEmailChanged(String email) {
    emit(state.copyWith(email: email)); // Sin validación
  }
}
```

### 🔧 Core Layer

```
┌────────────────────────────────────────────────────────────────┐
│                    CORE LAYER                                  │
├──────────────────────┬───────────────────┬───────────────────┤
│      Componente      │    Responsabilidad │    Quién lo hace   │
├──────────────────────┼───────────────────┼───────────────────┤
│ Dio Client           │ Configuración base│ 🤖 IA (scaffold)  │
│                      │ Interceptors      │ ✍️ TÚ              │
├──────────────────────┼───────────────────┼───────────────────┤
│ Error Handling       │ Exceptions custom │ ✍️ TÚ (SIEMPRE)   │
├──────────────────────┼───────────────────┼───────────────────┤
│ DI / GetIt setup     │ Registrar deps    │ 🤖 IA (scaffold)  │
│                      │ Configurar singlet│ ✍️ TÚ              │
├──────────────────────┼───────────────────┼───────────────────┤
│ Utils / Helpers      │ Helpers genéricos │ 🤖 IA (generales) │
│                      │ Helpers específicos│ ✍️ TÚ             │
└──────────────────────┴───────────────────┴───────────────────┘
```

---

## 5. Guía de Prompts en Español

> Todos los prompts están traducidos al español e incluyen un ejemplo práctico usando la **feature de Reservas** del salón de belleza.

---

### 📁 5.1 Prompts para Estructura de Feature

```markdown
# PROMPT 1: Crear estructura de feature completa
---

📝 PROMPT BASE:
"Crea la estructura de carpetas para una feature de [NOMBRE] en 
Clean Architecture. Incluye domain/, data/, presentation/ y core/.
Cada carpeta debe tener un archivo index.dart barrel."

💡 CUÁNDO USARLO:
→ Al inicio de cada nueva feature
→ Para mantener consistencia en el proyecto

📗 EJEMPLO PRÁCTICO (Feature de Reservas):

---

"Crea la estructura de carpetas para una feature de RESERVAS en 
Clean Architecture para un salón de belleza. Incluye:
- domain/entities/
- domain/repositories/
- domain/usecases/
- domain/failures/
- data/models/
- data/datasources/
- data/repositories/
- presentation/cubit/
- presentation/pages/
- presentation/widgets/
- core/constants/
- core/utils/

Cada carpeta debe tener un archivo index.dart barrel.
Genera los comandos bash para crear los directorios."

---

# PROMPT 2: Generar Entity
---

📝 PROMPT BASE:
"Crea una Entity de Clean Architecture para [NOMBRE] con los siguientes campos:
- [campo1]: [tipo], requerido
- [campo2]: [tipo], opcional con valor por defecto [valor]
- [campo3]: [tipo], relación con otra entidad

Incluye:
- Equatable para igualdad
- Método CopyWith
- Constructor privado con factory
- Usa convenciones de Dart."

💡 CUÁNDO USARLO:
→ Cuando necesitas definir el modelo del dominio
→ Antes de crear el repository

📗 EJEMPLO PRÁCTICO (Entity Client):

---

"Crea una Entity de Clean Architecture para CLIENTE con los siguientes campos:
- id: String, requerido
- name: String, requerido
- email: String, requerido
- phone: String, requerido
- noShowCount: int, opcional con valor por defecto 0
- status: enum (active, blocked), opcional con valor active
- lastNoShowDate: DateTime?, opcional
- isVip: bool, opcional con valor false

Incluye:
- Equatable para igualdad
- Método CopyWith
- Constructor privado con factory
- Usa convenciones de Dart."

---

# PROMPT 3: Generar Repository Interface
---

📝 PROMPT BASE:
"Crea la interfaz de repository de Clean Architecture para [FEATURE].
Métodos necesarios:
1. [método1]: devuelve Future<Either<Failure, Tipo>>
2. [método2]: devuelve Future<Either<Failure, Tipo>>
3. [método3]: devuelve Future<Either<Failure, Tipo>>

Usa el tipo Either de dartz.
Incluye comentarios de documentación para cada método."

💡 CUÁNDO USARLO:
→ Después de definir las entities
→ Para establecer el contrato entre domain y data

📗 EJEMPLO PRÁCTICO (BookingRepository):

---

"Crea la interfaz de repository de Clean Architecture para BOOKING (Reservas).
Métodos necesarios:
1. getAvailableSlots: recibe date y serviceId, devuelve Future<Either<Failure, List<Slot>>>
2. createBooking: recibe clientId, serviceId y dateTime, devuelve Future<Either<Failure, Booking>>>
3. cancelBooking: recibe bookingId, devuelve Future<Either<Failure, CancellationResult>>>
4. markNoShow: recibe bookingId, devuelve Future<Either<Failure, NoShowResult>>>

Usa el tipo Either de dartz.
Incluye comentarios de documentación para cada método.
Define clases de resultado como CancellationResult y NoShowResult."

---

### 🏗️ 5.2 Prompts para Boilerplate de Implementación

```markdown
# PROMPT 4: Boilerplate de UseCase
---

📝 PROMPT BASE:
"Crea una plantilla de UseCase de Clean Architecture para [NOMBRE]. 
Solo genera el scaffold, yo implementaré la lógica."

💡 CUÁNDO USARLO:
→ Para obtener la estructura base del UseCase
→ Tú siempre implementas la lógica de negocio después

📗 EJEMPLO PRÁCTICO (CreateBookingUseCase):

---

"Crea una plantilla de UseCase de Clean Architecture para CREATE_BOOKING (Crear Reserva).
Solo genera el scaffold, yo implementaré la lógica.

```dart
class CreateBookingUseCase {
  final BookingRepository repository;

  CreateBookingUseCase({required this.repository});

  Future<Either<Failure, Booking>> call(CreateBookingParams params) async {
    // TODO: Implementar lógica de negocio aquí
    // 1. Validar parámetros
    // 2. Verificar precondiciones
    // 3. Llamar al repository
    // 4. Manejar resultado y post-procesamiento
  }
}
```

Genera también la clase CreateBookingParams con Equatable."

---

# PROMPT 5: Boilerplate de Repository Implementation
---

📝 PROMPT BASE:
"Crea el esqueleto de implementación de repository para [FEATURE].
Proporciona implementaciones vacías con TODOs."

💡 CUÁNDO USARLO:
→ Para la estructura base del repository
→ Después de definir la interfaz del repository

📗 EJEMPLO PRÁCTICO (BookingRepositoryImpl):

---

"Crea el esqueleto de implementación de repository para BOOKING (Reservas).

```dart
class BookingRepositoryImpl implements BookingRepository {
  final ReservationRemoteDataSource remoteDataSource;
  final ReservationLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  BookingRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  // Implementar cada método de la interfaz:
  // - Lógica online vs offline
  // - Estrategia de cache
  // - Mapeo de errores
}
```

Proporciona implementaciones vacías con comentarios TODO."

---

# PROMPT 6: Model con fromJson/toJson
---

📝 PROMPT BASE:
"Crea un Model de Clean Architecture para [NOMBRE] con estos campos:
[definición de campos]

Requisitos:
- Constructor factory fromJson
- Método toJson
- Factory fromEntity (si aplica)
- Método toEntity (si aplica)
- Null safety adecuado
- Usa constructor const donde sea posible"

💡 CUÁNDO USARLO:
→ Para convertir datos de API a modelos
→ Para persistencia local

📗 EJEMPLO PRÁCTICO (BookingModel):

---

"Crea un Model de Clean Architecture para BOOKING con estos campos:
- id: String
- clientId: String
- serviceId: String
- dateTime: DateTime
- status: enum (confirmed, cancelled, completed, noShow)
- createdAt: DateTime
- cancelledAt: DateTime? (nullable)
- wasOverbooking: bool

Requisitos:
- Constructor factory fromJson
- Método toJson
- Factory fromEntity (recibiendo Booking entity)
- Método toEntity (devolviendo Booking entity)
- Null safety adecuado
- Usa constructor const donde sea posible
- Incluye parsing de DateTime a ISO8601"

---

### 🧪 5.3 Prompts para Testing

```markdown
# PROMPT 7: Scaffold de tests para UseCase
---

📝 PROMPT BASE:
"Crea el scaffold de tests para el UseCase [NOMBRE] usando bloc_test.
Solo genera la estructura, yo escribiré las aserciones."

💡 CUÁNDO USARLO:
→ Para obtener la estructura base de tests
→ Tú siempre escribes las aserciones de lógica de negocio

📗 EJEMPLO PRÁCTICO (CreateBookingUseCase Test):

---

"Crea el scaffold de tests para CreateBookingUseCase usando bloc_test.
Solo genera la estructura, yo escribiré las aserciones.

Estructura esperada:
- group para el UseCase
- setUp con mocks
- test para caso de éxito
- test para casos de error (slot no disponible, cliente bloqueado)
- Usa Mock classes generadas con mockito

```dart
group('CreateBookingUseCase', () {
  late CreateBookingUseCase useCase;
  late MockBookingRepository mockRepository;
  late MockClientRepository mockClientRepository;

  setUp(() {
    mockRepository = MockBookingRepository();
    mockClientRepository = MockClientRepository();
    useCase = CreateBookingUseCase(
      bookingRepository: mockRepository,
      clientRepository: mockClientRepository,
    );
  });

  group('call', () {
    test('should return booking when successful', () async {
      // TODO: Yo escribiré arrange, act y assert
    });
    
    // Agregar más casos de prueba:
    // - Slot no disponible
    // - Cliente bloqueado
    // - Horario inválido
  });
});
```"

---

# PROMPT 8: Test de Repository con Fakes
---

📝 PROMPT BASE:
"Crea el scaffold de tests de repository usando fakes manuales para [FEATURE].
Solo genera la estructura, yo escribiré las aserciones."

💡 CUÁNDO USARLO:
→ Para tests de integración de repository
→ Para probar lógica de cache offline/online

📗 EJEMPLO PRÁCTICO (BookingRepository Test):

---

"Crea el scaffold de tests de repository usando fakes manuales para BOOKING.
Solo genera la estructura, yo escribiré las aserciones.

Estructura esperada:
- Fake Data Source que implementa ReservationRemoteDataSource
- Fake Data Source que implementa ReservationLocalDataSource
- group para el repository
- setUp con fakes y mock de NetworkInfo
- test para: online con datos remotos
- test para: offline con cache
- test para: offline sin cache (error)
- test para: error de servidor

```dart
// Fake para testing
class FakeReservationRemoteDataSource implements ReservationRemoteDataSource {
  @override
  Future<List<BookingModel>> getBookings() async {
    // TODO: Yo definiré los datos de test
  }
  
  @override
  Future<BookingModel> createBooking(CreateBookingParams params) async {
    // TODO: Yo definiré el comportamiento
  }
}

group('BookingRepository', () {
  late BookingRepositoryImpl repository;
  late FakeReservationRemoteDataSource fakeRemoteDataSource;
  late FakeReservationLocalDataSource fakeLocalDataSource;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    // TODO: Yo configuraré los fakes
  });

  group('getBookings', () {
    test('should return remote data when online', () async {
      // TODO: Yo escribiré arrange, act y assert
    });
    
    // Agregar más escenarios:
    // - Offline con cache válido
    // - Offline sin cache
    // - Error de servidor
  });
});
```"

---

# PROMPT 9: Test de Cubit
---

📝 PROMPT BASE:
"Crea el scaffold de tests de Cubit para [NOMBRE].
Solo genera la estructura, yo escribiré las aserciones."

💡 CUÁNDO USARLO:
→ Para tests de estado de UI
→ Para probar transiciones de estados

📗 EJEMPLO PRÁCTICO (ReservationCubit Test):

---

"Crea el scaffold de tests de Cubit para RESERVATION (manejo de reservas).
Solo genera la estructura, yo escribiré las aserciones.

Estructura esperada:
- group para el Cubit
- setUp con mocks de UseCases
- setUpAll con registerFallbackValue
- blocTest para: cargar reservas exitosamente
- blocTest para: error al cargar reservas
- test para: estado inicial

```dart
group('ReservationCubit', () {
  late ReservationCubit cubit;
  late MockGetAvailableSlotsUseCase mockGetSlotsUseCase;
  late MockCreateBookingUseCase mockCreateBookingUseCase;

  setUp(() {
    mockGetSlotsUseCase = MockGetAvailableSlotsUseCase();
    mockCreateBookingUseCase = MockCreateBookingUseCase();
    cubit = ReservationCubit(
      getAvailableSlots: mockGetSlotsUseCase,
      createBooking: mockCreateBookingUseCase,
    );
  });

  setUpAll(() {
    registerFallbackValue(FakeGetAvailableSlotsParams());
    registerFallbackValue(FakeCreateBookingParams());
  });

  blocTest<ReservationCubit, ReservationState>(
    'emits [Loading, Loaded] when loadSlots succeeds',
    build: () {
      when(mockGetSlotsUseCase(any)).thenAnswer(
        (_) async => Right([testSlot]),
      );
      return cubit;
    },
    act: (cubit) => cubit.loadAvailableSlots(testDate),
    expect: () => [
      isA<ReservationLoading>(),
      isA<ReservationLoaded>(),
    ],
  );

  // Agregar más tests:
  // - Error de red
  // - Crear reserva exitosa
  // - Error al crear reserva
});
```"

---

### 🔍 5.4 Prompts para Debugging y Análisis

```markdown
# PROMPT 10: Analizar error
---

📝 PROMPT BASE:
"Estoy recibiendo este error en [ARCHIVO]:

```
[MENSAJE_DE_ERROR]
```

Contexto:
- Versión de Flutter: [VERSIÓN]
- Versiones de paquetes: [LISTA]
- El error ocurre cuando: [DESCRIPCIÓN]

¿Puedes ayudarme a entender:
1. ¿Qué está causando este error?
2. ¿Cómo solucionarlo?
3. ¿Cómo prevenirlo en el futuro?"

💡 CUÁNDO USARLO:
→ Cuando tienes un error que no entiendes
→ Para debugging rápido

📗 EJEMPLO PRÁCTICO (Error en CreateBooking):

---

"Estoy recibiendo este error en create_booking.dart:

```
Stack trace:
#0      CreateBookingUseCase.call (create_booking.dart:45)
#1      ReservationCubit.createBooking (reservation_cubit.dart:78)
Bad state: No element
```

Contexto:
- Versión de Flutter: 3.19.0
- Paquetes: flutter_bloc 8.1.3, dartz 0.10.1
- El error ocurre cuando intento crear una reserva a las 10:00 AM

¿Puedes ayudarme a entender:
1. ¿Qué está causando este error?
2. ¿Cómo solucionarlo?
3. ¿Cómo prevenirlo en el futuro?"

---

# PROMPT 11: Analizar código y sugerir mejoras
---

📝 PROMPT BASE:
"Analiza este código y sugiere mejoras:

```dart
[TU_CÓDIGO]
```

Considera:
1. Performance
2. Mantenibilidad
3. Cumplimiento de Clean Architecture
4. Manejo de errores
5. Null safety

Sé específico en qué cambiar y por qué."

💡 CUÁNDO USARLO:
→ Para refactorización
→ Para mejorar código existente

📗 EJEMPLO PRÁCTICO (Repository con problemas):

---

"Analiza este código y sugiere mejoras:

```dart
class BookingRepositoryImpl implements BookingRepository {
  final RemoteDataSource remote;
  final LocalDataSource local;
  
  Future<Either<Failure, List<Booking>>> getBookings() async {
    try {
      final result = await remote.getBookings();
      await local.cacheBookings(result);
      return Right(result);
    } catch (e) {
      final cached = await local.getBookings();
      return Right(cached);
    }
  }
}
```

Considera:
1. Performance
2. Mantenibilidad
3. Cumplimiento de Clean Architecture
4. Manejo de errores
5. Null safety

Sé específico en qué cambiar y por qué."

---

# PROMPT 12: Explicar patrón/código
---

📝 PROMPT BASE:
"Explica qué hace este código en términos simples:

```dart
[CÓDIGO_A_EXPLICAR]
```

Luego explica:
1. ¿Por qué se eligió este enfoque?
2. ¿Cuáles son las alternativas?
3. ¿Cuándo usarías un enfoque diferente?"

💡 CUÁNDO USARLO:
→ Para entender código de otros
→ Para aprender nuevos patrones

📗 EJEMPLO PRÁCTICO (Lógica de buffer time):

---

"Explica qué hace este código en términos simples:

```dart
bool _checkSlotOverlap({
  required DateTime slotStart,
  required int slotDuration,
  required List<Slot> reservedSlots,
}) {
  final slotEnd = slotStart.add(Duration(minutes: slotDuration));

  for (final reserved in reservedSlots) {
    final overlaps = slotStart.isBefore(reserved.endTime) &&
        slotEnd.isAfter(reserved.startTime);
    if (overlaps) return true;
  }
  return false;
}
```

Luego explica:
1. ¿Por qué se eligió este enfoque?
2. ¿Cuáles son las alternativas?
3. ¿Cuándo usarías un enfoque diferente?"

---

### ✨ 5.5 Prompts para Refactoring

```markdown
# PROMPT 13: Sugerir refactoring
---

📝 PROMPT BASE:
"Refactoriza este código para mejorar [ASPECTO: legibilidad/rendimiento/mantenibilidad]:

```dart
[CÓDIGO_A_REFACTORIZAR]
```

Reglas:
- Mantén la misma funcionalidad
- Sigue principios de Clean Architecture
- Mantén null safety
- Usa patrones modernos de Dart/Flutter"

💡 CUÁNDO USARLO:
→ Para limpiar código
→ Para aplicar mejores prácticas

📗 EJEMPLO PRÁCTICO (UseCase largo):

---

"Refactoriza este UseCase para mejorar la mantenibilidad:

```dart
class CreateBookingUseCase {
  Future<Either<Failure, Booking>> call(CreateBookingParams params) async {
    // 1. Obtener cliente
    final clientResult = await clientRepository.getClient(params.clientId);
    if (clientResult.isLeft()) return Left(clientResult.fold((l) => l, (r) => r));
    final client = clientResult.getOrElse(() => throw Exception());
    
    // 2. Verificar no bloqueado
    if (client.status == ClientStatus.blocked) {
      return const Left(ClientBlockedFailure());
    }
    
    // 3. Obtener reservas activas
    final bookingsResult = await bookingRepository.getClientBookings(params.clientId);
    if (bookingsResult.isLeft()) return Left(bookingsResult.fold((l) => l, (r) => r));
    final activeBookings = bookingsResult.getOrElse(() => throw Exception());
    
    // 4. Verificar límite
    if (activeBookings.length >= 5) {
      return const Left(ReservationFailure(message: 'Límite alcanzado'));
    }
    
    // 5. Crear reserva
    return await bookingRepository.createBooking(...);
  }
}
```

Reglas:
- Mantén la misma funcionalidad
- Sigue principios de Clean Architecture
- Mantén null safety
- Usa patrones modernos de Dart/Flutter
- Extrae validaciones a métodos privados bien nombrados"

---

# PROMPT 14: Extraer a método/clase
---

📝 PROMPT BASE:
"Refactoriza este código para extraer [QUÉ_EXTRAER] en un [MÉTODO/CLASE] separado:

```dart
[MÉTODO_O_CLASE_LARGA]
```

Crea un nuevo [MÉTODO/CLASE] que:
- Tiene un nombre descriptivo
- Toma los parámetros apropiados
- Devuelve el tipo apropiado
- Es reutilizable"

💡 CUÁNDO USARLO:
→ Para reducir complejidad
→ Para código más testeable

📗 EJEMPLO PRÁCTICO (Extraer validaciones):

---

"Refactoriza este UseCase para extraer las validaciones en clases separadas:

```dart
class CreateBookingUseCase {
  Future<Either<Failure, Booking>> call(CreateBookingParams params) async {
    // Validar cliente
    final clientResult = await clientRepository.getClient(params.clientId);
    final client = clientResult.fold((f) => null, (c) => c);
    if (client == null) return const Left(ReservationFailure('Cliente no encontrado'));
    if (client.status == ClientStatus.blocked) return const Left(ClientBlockedFailure());
    
    // Validar límite reservas
    final bookingsResult = await bookingRepository.getClientBookings(params.clientId);
    final bookings = bookingsResult.fold((f) => <Booking>[], (b) => b);
    if (bookings.length >= 5) return const Left(ReservationFailure('Límite de reservas'));
    
    // Crear reserva...
  }
}
```

Crea clases de validación separadas para:
- ClientValidation (verificar existe, no bloqueado)
- BookingLimitValidation (verificar límite de reservas activas)
- SchedulingValidation (verificar horarios disponibles)

Cada clase debe:
- Tener un nombre descriptivo
- Tomar los parámetros apropiados
- Devolver Either<Failure, ValidResult>
- Ser reutilizable y testeable"

---

### 📊 Resumen Rápido de Prompts

```
┌─────────────────────────────────────────────────────────────────┐
│                 CHEAT SHEET DE PROMPTS                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📁 ESTRUCTURA                                                  │
│     Prompt 1: Estructura de carpeta                           │
│     Prompt 2: Entity                                          │
│     Prompt 3: Repository interface                            │
│                                                                 │
│  🏗️ IMPLEMENTACIÓN                                              │
│     Prompt 4: UseCase scaffold                                │
│     Prompt 5: Repository implementation scaffold               │
│     Prompt 6: Model with fromJson/toJson                      │
│                                                                 │
│  🧪 TESTING                                                     │
│     Prompt 7: Test scaffold para UseCase                       │
│     Prompt 8: Test scaffold para Repository con Fakes          │
│     Prompt 9: Test scaffold para Cubit                        │
│                                                                 │
│  🔍 DEBUGGING                                                   │
│     Prompt 10: Analizar error                                │
│     Prompt 11: Analizar código y sugerir mejoras              │
│     Prompt 12: Explicar patrón/código                        │
│                                                                 │
│  ✨ REFACTORING                                                 │
│     Prompt 13: Sugerir refactoring                            │
│     Prompt 14: Extraer a método/clase                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Caso de Uso Completo: Feature de Login

### 📋 Descripción del Escenario

```
Feature: Login de usuario
├── Domain: AuthRepository interface, LoginUseCase
├── Data: AuthRepositoryImpl, AuthRemoteDataSource, AuthModel
├── Presentation: LoginCubit, LoginPage
└── Tests: LoginUseCaseTest, LoginRepositoryTest, LoginCubitTest
```

### Paso 1: ANALYZE - Análisis Personal

```markdown
Antes de pedir código a IA, pienso:

1. ¿Qué necesita el login?
   - Email y password
   - Validación de formato
   - Manejo de errores (credenciales inválidas, red, servidor caído)
   - Guardar sesión (token)

2. ¿Qué dependencias necesito?
   - AuthRepository
   - NetworkInfo (para verificar conexión)
   - LocalStorage (para guardar token)

3. ¿Qué puede fallar?
   - Credenciales incorrectas → AuthFailure
   - Sin conexión → NetworkFailure
   - Servidor caído → ServerFailure
   - Rate limiting → AuthFailure con mensaje específico
   - Token expirado → (para después, pero lo considero)

4. Decisión: Esto tiene lógica crítica
   - La validación del email/password la hago YO
   - El manejo de errores específicos lo hago YO
   - El resto: scaffold a IA
```

### Paso 2: INVESTIGATE - Investigación con IA

```
Prompt usado:
"¿Cuáles son los mejores prácticas para validación de email y password
en Flutter? Dame regex patterns y consideraciones de seguridad."
```

### Paso 3: DECIDE + IMPLEMENT - Ejecución Híbrida

#### 🤖 PARTE 1: Scaffold con IA

```markdown
# Le pido a IA:
"Create the complete folder structure and scaffold files for an Auth feature
in Clean Architecture. Include:
- domain/entities/user.dart
- domain/repositories/auth_repository.dart
- domain/usecases/login_usecase.dart
- domain/usecases/logout_usecase.dart
- domain/failures/auth_failure.dart
- data/models/user_model.dart
- data/datasources/auth_remote_datasource.dart
- data/repositories/auth_repository_impl.dart
- presentation/cubit/auth_cubit.dart
- presentation/cubit/auth_state.dart

Just create the scaffold with TODOs where logic should be."
```

IA genera (boilerplate):

```dart
// auth_repository.dart
abstract class AuthRepository {
  Future<Either<Failure, User>> login({
    required String email,
    required String password,
  });
  
  Future<Either<Failure, void>> logout();
  
  Future<Either<Failure, bool>> isLoggedIn();
}

// login_usecase.dart
class LoginUseCase {
  final AuthRepository repository;

  LoginUseCase({required this.repository});

  Future<Either<Failure, User>> call(LoginParams params) async {
    // TODO: Implement login logic
    throw UnimplementedError();
  }
}
```

#### ✍️ PARTE 2: Lógica Crítica (ESCRIBO YO)

```dart
// login_usecase.dart - VERSIÓN FINAL (escrita por mí)
class LoginUseCase {
  final AuthRepository repository;
  final NetworkInfo networkInfo;

  LoginUseCase({
    required this.repository,
    required this.networkInfo,
  });

  Future<Either<Failure, User>> call(LoginParams params) async {
    // ============================================================
    // LOGICA CRITICA: Validaciones de negocio
    // ============================================================

    // 1. Validar conexión a internet primero
    final isConnected = await networkInfo.isConnected;
    if (!isConnected) {
      return const Left(NetworkFailure(
        message: 'No internet connection. Please check your network.',
      ));
    }

    // 2. Validar formato de email (reglas de negocio)
    final emailValidation = _validateEmail(params.email);
    if (emailValidation != null) {
      return Left(ValidationFailure(emailValidation));
    }

    // 3. Validar password (reglas de negocio)
    final passwordValidation = _validatePassword(params.password);
    if (passwordValidation != null) {
      return Left(ValidationFailure(passwordValidation));
    }

    // ============================================================
    // BOILERPLATE: Llamada al repositorio
    // ============================================================
    try {
      final result = await repository.login(
        email: params.email.trim().toLowerCase(),
        password: params.password,
      );

      // ============================================================
      // LOGICA CRITICA: Post-procesamiento
      // ============================================================
      return result.fold(
        (failure) => _mapAuthFailure(failure),
        (user) {
          // Verificar que el usuario está activo
          if (!user.isActive) {
            return const Left(AuthFailure(
              message: 'Your account has been deactivated.',
            ));
          }
          
          // Verificar email verificado
          if (!user.isEmailVerified) {
            return const Left(AuthFailure(
              message: 'Please verify your email before logging in.',
            ));
          }
          
          return Right(user);
        },
      );
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } catch (e) {
      return Left(UnexpectedFailure(message: e.toString()));
    }
  }

  // ============================================================
  // LOGICA CRITICA: Validaciones de dominio
  // ============================================================
  
  String? _validateEmail(String email) {
    if (email.isEmpty) {
      return 'Email is required';
    }
    
    // Normalizar email
    final normalizedEmail = email.trim().toLowerCase();
    
    // Verificar formato básico
    final emailRegex = RegExp(
      r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    );
    
    if (!emailRegex.hasMatch(normalizedEmail)) {
      return 'Please enter a valid email address';
    }
    
    // Reglas de negocio específicas
    if (normalizedEmail.length > 254) {
      return 'Email address is too long';
    }
    
    // Verificar domain patterns (ejemplo: bloquear dominios temporales)
    final blockedDomains = ['tempmail.com', 'throwaway.com'];
    final domain = normalizedEmail.split('@').last;
    if (blockedDomains.contains(domain)) {
      return 'This email domain is not allowed';
    }
    
    return null;
  }

  String? _validatePassword(String password) {
    if (password.isEmpty) {
      return 'Password is required';
    }
    
    if (password.length < 8) {
      return 'Password must be at least 8 characters long';
    }
    
    // Reglas de negocio: requerir mayúsculas
    if (!password.contains(RegExp(r'[A-Z]'))) {
      return 'Password must contain at least one uppercase letter';
    }
    
    // Reglas de negocio: requerir números
    if (!password.contains(RegExp(r'[0-9]'))) {
      return 'Password must contain at least one number';
    }
    
    return null;
  }

  Failure _mapAuthFailure(AuthFailure failure) {
    // Personalizar mensajes según el tipo de error del servidor
    if (failure.code == 'INVALID_CREDENTIALS') {
      return const AuthFailure(
        message: 'Invalid email or password',
        code: 'INVALID_CREDENTIALS',
      );
    }
    
    if (failure.code == 'ACCOUNT_LOCKED') {
      return const AuthFailure(
        message: 'Your account has been locked due to too many failed attempts',
        code: 'ACCOUNT_LOCKED',
      );
    }
    
    if (failure.code == 'RATE_LIMIT') {
      return const AuthFailure(
        message: 'Too many login attempts. Please try again later.',
        code: 'RATE_LIMIT',
      );
    }
    
    return failure;
  }
}
```

### Paso 4: REVIEW - Revisión

```markdown
Después de escribir mi lógica:

□ ✅ ¿Entiendo cada línea? Sí, es mi código
□ ✅ ¿Sigue las convenciones del proyecto? Sí
□ ✅ ¿Maneja edge cases? Sí (blocked domains, rate limit, etc.)
□ ✅ ¿Seguridad? Sí (no exponho mensajes de error internos)
□ ✅ ¿Maintainable? Sí, bien documentado con secciones

Resultado: Esta sección NO necesita revisión de IA porque la escribí yo.
```

---

## 7. Testing Híbrido: Boilerplate IA + Lógica Manual

### 🎯 Filosofía de Testing Híbrido

```
┌─────────────────────────────────────────────────────────────────┐
│              ENFOQUE HÍBRIDO PARA TESTS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   🤖 IA GENERA                         ✍️ TÚ ESCRIBES          │
│   ─────────────────                   ─────────────────         │
│   • Estructura del test               • Arrange (datos reales) │
│   • Setup de mocks/fakes              • Aserciones             │
│   • Scaffold de scenarios            • Edge cases             │
│   • boilerplate del arrange           • Casos de error         │
│                                        • Expectations          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ejemplo: LoginUseCase Test

#### 🤖 PARTE 1: Scaffold de IA

```markdown
# Prompt para IA:
"Generate test scaffold for LoginUseCase with bloc_test.
Include:
- group for each method
- setUp with mocks
- test for success case
- test for failure cases (invalid credentials, network failure)
- Use Mock classes and fake data"

IA genera:
```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

import 'package:my_app/features/auth/domain/entities/user.dart';
import 'package:my_app/features/auth/domain/repositories/auth_repository.dart';
import 'package:my_app/features/auth/domain/usecases/login_usecase.dart';
import 'package:my_app/core/error/failures.dart';

@GenerateMocks([AuthRepository, NetworkInfo])
import 'login_usecase_test.mocks.dart';

void main() {
  late LoginUseCase useCase;
  late MockAuthRepository mockRepository;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockRepository = MockAuthRepository();
    mockNetworkInfo = MockNetworkInfo();
    useCase = LoginUseCase(
      repository: mockRepository,
      networkInfo: mockNetworkInfo,
    );
  });

  group('call', () {
    const testEmail = 'test@example.com';
    const testPassword = 'Password123';
    const testUser = User(
      id: '1',
      email: testEmail,
      name: 'Test User',
    );

    test('should return user when login is successful', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRepository.login(
        email: anyNamed('email'),
        password: anyNamed('password'),
      )).thenAnswer((_) async => const Right(testUser));

      // act
      final result = await useCase(
        const LoginParams(email: testEmail, password: testPassword),
      );

      // assert
      expect(result, const Right(testUser));
    });

    // TODO: Add more test cases
  });
}
```

#### ✍️ PARTE 2: Tests Críticos (ESCRIBO YO)

```dart
// VERSIÓN COMPLETA con lógica de testing manual
group('LoginUseCase', () {
  late LoginUseCase useCase;
  late MockAuthRepository mockRepository;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockRepository = MockAuthRepository();
    mockNetworkInfo = MockNetworkInfo();
    useCase = LoginUseCase(
      repository: mockRepository,
      networkInfo: mockNetworkInfo,
    );
  });

  setUpAll(() {
    registerFallbackValue(FakeLoginParams());
  });

  // ============================================================
  // TEST DATA: Creados por mí, datos realistas
  // ============================================================
  const validEmail = 'user@company.com';
  const validPassword = 'SecurePass123';
  const invalidEmail = 'notanemail';
  const weakPassword = 'abc';
  
  const activeUser = User(
    id: '1',
    email: validEmail,
    name: 'John Doe',
    isActive: true,
    isEmailVerified: true,
  );

  const inactiveUser = User(
    id: '2',
    email: 'inactive@test.com',
    name: 'Inactive User',
    isActive: false,
    isEmailVerified: true,
  );

  const unverifiedUser = User(
    id: '3',
    email: 'unverified@test.com',
    name: 'Unverified User',
    isActive: true,
    isEmailVerified: false,
  );

  // ============================================================
  // SUCCESS CASES: Aserciones escritas por mí
  // ============================================================
  
  group('Success Cases', () {
    test('should return user when credentials are valid and user is active', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRepository.login(
        email: validEmail,
        password: validPassword,
      )).thenAnswer((_) async => const Right(activeUser));

      // act
      final result = await useCase(
        const LoginParams(email: validEmail, password: validPassword),
      );

      // assert - Verifico exactamente lo que espero
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Expected success but got failure: ${failure.message}'),
        (user) {
          expect(user.id, '1');
          expect(user.email, validEmail);
          expect(user.isActive, true);
          expect(user.isEmailVerified, true);
        },
      );
    });
  });

  // ============================================================
  // VALIDATION CASES: Lógica de validación probada por mí
  // ============================================================
  
  group('Validation Cases', () {
    test('should return ValidationFailure when email is empty', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);

      // act
      final result = await useCase(
        const LoginParams(email: '', password: validPassword),
      );

      // assert
      expect(result.isLeft(), true);
      result.fold(
        (failure) {
          expect(failure, isA<ValidationFailure>());
          expect(failure.message, contains('required'));
        },
        (_) => fail('Expected validation failure'),
      );
    });

    test('should return ValidationFailure when email format is invalid', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);

      // act
      final result = await useCase(
        const LoginParams(email: invalidEmail, password: validPassword),
      );

      // assert
      result.fold(
        (failure) {
          expect(failure, isA<ValidationFailure>());
          expect(failure.message, contains('valid email'));
        },
        (_) => fail('Expected validation failure'),
      );
    });

    test('should return ValidationFailure when email uses blocked domain', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);

      // act
      final result = await useCase(
        const LoginParams(
          email: 'test@tempmail.com',
          password: validPassword,
        ),
      );

      // assert - Edge case específico de mi negocio
      result.fold(
        (failure) {
          expect(failure, isA<ValidationFailure>());
          expect(failure.message, contains('not allowed'));
        },
        (_) => fail('Expected validation failure for blocked domain'),
      );
    });

    test('should return ValidationFailure when password is too short', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);

      // act
      final result = await useCase(
        const LoginParams(email: validEmail, password: weakPassword),
      );

      // assert
      result.fold(
        (failure) {
          expect(failure, isA<ValidationFailure>());
          expect(failure.message, contains('8 characters'));
        },
        (_) => fail('Expected validation failure'),
      );
    });

    test('should return ValidationFailure when password lacks uppercase', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);

      // act
      final result = await useCase(
        const LoginParams(email: validEmail, password: 'password123'),
      );

      // assert
      result.fold(
        (failure) {
          expect(failure, isA<ValidationFailure>());
          expect(failure.message, contains('uppercase'));
        },
        (_) => fail('Expected validation failure'),
      );
    });
  });

  // ============================================================
  // ERROR CASES: Casos de error críticos probados por mí
  // ============================================================
  
  group('Error Cases', () {
    test('should return NetworkFailure when offline', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => false);

      // act
      final result = await useCase(
        const LoginParams(email: validEmail, password: validPassword),
      );

      // assert
      result.fold(
        (failure) {
          expect(failure, isA<NetworkFailure>());
          expect(failure.message, contains('internet'));
        },
        (_) => fail('Expected network failure'),
      );
    });

    test('should return AuthFailure when credentials are invalid', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRepository.login(
        email: anyNamed('email'),
        password: anyNamed('password'),
      )).thenAnswer((_) async => const Left(AuthFailure(
        message: 'Invalid credentials',
        code: 'INVALID_CREDENTIALS',
      )));

      // act
      final result = await useCase(
        const LoginParams(email: validEmail, password: 'wrongpassword'),
      );

      // assert
      result.fold(
        (failure) {
          expect(failure, isA<AuthFailure>());
          expect(failure.code, 'INVALID_CREDENTIALS');
        },
        (_) => fail('Expected auth failure'),
      );
    });

    test('should return AuthFailure when account is inactive', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRepository.login(
        email: anyNamed('email'),
        password: anyNamed('password'),
      )).thenAnswer((_) async => const Right(inactiveUser));

      // act
      final result = await useCase(
        const LoginParams(email: validEmail, password: validPassword),
      );

      // assert
      result.fold(
        (failure) {
          expect(failure, isA<AuthFailure>());
          expect(failure.message, contains('deactivated'));
        },
        (_) => fail('Expected auth failure for inactive account'),
      );
    });

    test('should return AuthFailure when email is not verified', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRepository.login(
        email: anyNamed('email'),
        password: anyNamed('password'),
      )).thenAnswer((_) async => const Right(unverifiedUser));

      // act
      final result = await useCase(
        const LoginParams(email: validEmail, password: validPassword),
      );

      // assert
      result.fold(
        (failure) {
          expect(failure, isA<AuthFailure>());
          expect(failure.message, contains('verify'));
        },
        (_) => fail('Expected auth failure for unverified email'),
      );
    });

    test('should return AuthFailure with generic message on rate limit', () async {
      // arrange
      when(mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(mockRepository.login(
        email: anyNamed('email'),
        password: anyNamed('password'),
      )).thenAnswer((_) async => const Left(AuthFailure(
        message: 'Too many requests from your IP',
        code: 'RATE_LIMIT',
      )));

      // act
      final result = await useCase(
        const LoginParams(email: validEmail, password: validPassword),
      );

      // assert - Mensaje personalizado para el usuario
      result.fold(
        (failure) {
          expect(failure, isA<AuthFailure>());
          expect(failure.code, 'RATE_LIMIT');
          // Verifico que el mensaje sea amigable, no el del servidor
          expect(failure.message, contains('try again later'));
        },
        (_) => fail('Expected auth failure'),
      );
    });
  });
});
```

---

## 8. Checklist Diario de Referencia Rápica

### 📋 Morning Check (Antes de Empezar)

```markdown
□ ¿Analicé el problema antes de usar IA?
□ ¿Sé qué es boilerplate y qué es lógica crítica?
□ ¿Tengo claros los edge cases de esta feature?
□ ¿Qué parte haré yo manualmente?
```

### 🔄 Durante el Desarrollo

```markdown
□ ¿Estoy escribiendo código donde debo o dejando que IA genere?
□ ¿Entiendo cada línea que IA me da?
□ ¿Mí código tiene tests para lógica crítica?
□ ¿Revisé el código de IA antes de commit?

╔═══════════════════════════════════════════════════════════════╗
║               RECORDATORIO RÁPIDO                            ║
╠═══════════════════════════════════════════════════════════════╣
║  🤖 USA IA PARA:           │  ✍️ HAZLO TÚ:                   ║
║  ─────────────────────     │  ─────────────────────          ║
║  • Estructura de archivos   │  • Lógica de negocio           ║
║  • Scaffold de clases       │  • Validaciones                ║
║  • Boilerplate de tests     │  • UseCases                    ║
║  • fromJson/toJson          │  • Repository implementations  ║
║  • Configuración base       │  • Edge cases                  ║
║  • Documentación básica     │  • Decisiones arquitectónicas  ║
╚═══════════════════════════════════════════════════════════════╝
```

### 🌙 Evening Review (Antes de Terminar)

```markdown
□ ¿Qué aprendí hoy escribiendo código manualmente?
□ ¿Hay algo que IA generó que no entiendo?
□ ¿Qué podría mejorar para mañana?
□ ¿Documenté las decisiones técnicas importantes?
```

### 🎯 Métricas de Progreso

```markdown
Semanalmente, reflexiona:

□ ¿Cuántas líneas de código escribí manualmente?
□ ¿Cuántas líneas generó IA?
□ ¿Me siento más cómodo con qué tipos de código?
□ ¿Identifiqué nuevos patrones que puedo delegar a IA?
```

---

## 📚 Recursos Adicionales

### Patrones de IA Recomendados

| Situación | Herramienta | Prompt Strategy |
|-----------|------------|-----------------|
| Scaffold rápido | Cursor/VS Code AI | "Create scaffold for X" |
| Debug complejo | Claude/ChatGPT | "Analyze this error: [error]" |
| Explicar código | Cualquiera | "Explain this code" |
| Optimizar código | Cursor | "Refactor for performance" |
| Generar tests | Cursor | "Generate tests for X" |

### Señales de Alerta

```
⚠️ STOP si...
├── Copias código de IA sin leerlo
├── No sabes explicar qué hace tu código
├── Esperas que IA resuelva todo
├── Dejas de practicar escritura manual
└── Ignoras los warnings de lint
```

---

## ✅ Conclusión

> **La IA es un amplifier de tus habilidades, no un reemplazo.**
> 
> Cuando usas IA para boilerplate, te liberas tiempo para enfocarte
> en lo que realmente importa: la lógica de negocio que diferencia
> tu aplicación.
> 
> **Recuerda:**
> - La lógica de negocio = TU VALOR como desarrollador
> - Boilerplate = Tiempo que IA te ahorra
> - Testing = Tu red de seguridad
> - Código manual = Tu entrenamiento

---

**Última actualización:** 2026
**Versión:** 1.0
