## 2. Las 4 Capas de Clean Architecture

### Diagrama de las 4 Capas

```
CAPA 4 - UI (Widgets)
    ↓ Llama al Cubit
    
CAPA 3 - Presentation (Cubit)
    ↓ Llama al UseCase
    
CAPA 2 - Domain (UseCase + Entity)
    ↓ Llama al Repository
    
CAPA 1 - Data (Repository + DataSource)
    ↓ Habla con API o Base de Datos
```

### Las 4 Capas en Detalle

#### 1️⃣ Domain (El Núcleo)

**Contiene**: Entities, Repository Interfaces, Use Cases

**Principios**:
- Pura lógica de negocio
- Sin dependencias externas (no Flutter, no HTTP, no DB)
- Altamente testeable
- Reutilizable en otros proyectos

**Analogía**: Las reglas del juego de ajedrez

#### 2️⃣ Data (La Implementación)

**Contiene**: Models, DataSources, Repository Implementations

**Principios**:
- Implementa los contratos del Domain
- Habla con APIs, bases de datos, cache
- Convierte datos externos a Entities

**Analogía**: El tablero físico y las piezas de ajedrez

#### 3️⃣ Presentation (El Estado)

**Contiene**: Cubits/Blocs, States

**Principios**:
- Maneja el estado de la UI
- Orquesta Use Cases
- Sin lógica de negocio compleja

**Analogía**: El visor que muestra el tablero en tu celular

#### 4️⃣ UI (La Vista)

**Contiene**: Widgets, Pages, Screens

**Principios**:
- Solo muestra datos
- Recibe eventos del usuario
- Se reconstruye cuando cambia el estado

**Analogía**: La pantalla de tu celular

### Principios Fundamentales

- **Capas:** La arquitectura se divide en capas (Presentación, Dominio, Datos).
- **Regla de Dependencia:** El código fuente solo puede depender "hacia adentro".
- **Abstracciones:** Las capas se comunican a través de interfaces (clases abstractas en Dart).

---
