# 02: Colaboracion con Diseno y Producto

## El Triangulo: Developer - Disenador - PM

En cualquier proyecto de software, hay tres roles que deben mantenerse sincronizados:

```
                    ┌─────────────┐
                    │     PM      │
                    │  (Producto) │
                    │             │
                    │  "Que" y    │
                    │  "Por que"  │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │                         │
              ▼                         ▼
    ┌─────────────────┐     ┌─────────────────┐
    │   Disenador     │     │   Developer     │
    │   (UI/UX)       │     │   (Flutter)     │
    │                 │     │                 │
    │   "Como se      │     │   "Como se      │
    │    ve"          │     │    construye"   │
    └─────────────────┘     └─────────────────┘
```

### Responsabilidades de cada rol

| Rol | Responsabilidad | Lo que necesita del otro |
|-----|----------------|------------------------|
| **PM** | Definir prioridades, user stories, acceptance criteria | Que features son tecnicamente viables |
| **Disenador** | Wireframes, mockups, design system, user flow | Que restricciones tecnicas existen |
| **Developer** | Implementar, estimar, mantener el codigo | Specs claros, assets correctos, prioridades definidas |

## Entendiendo el Design Handoff

El **design handoff** es el momento en que el disenador entrega el diseno al developer.
Este es el punto donde mas errores de comunicacion ocurren.

### Lo que el disenador entrega

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESIGN HANDOFF                               │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Mockups  │  │ Assets   │  │ Specs    │  │ Flows    │       │
│  │ (Figma)  │  │ (SVG/PNG)│  │ (medidas)│  │ (user)   │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│  │ Animations│ │ States   │  │ Design   │                     │
│  │ (Lottie) │  │ (error,  │  │ System   │                     │
│  │          │  │  loading)│  │ (tokens) │                     │
│  └──────────┘  └──────────┘  └──────────┘                     │
└─────────────────────────────────────────────────────────────────┘
```

### Lo que el developer necesita

| Necesidad | Ejemplo | Prioridad |
|-----------|---------|-----------|
| **Medidas exactas** | Padding: 16px, Margin: 8px | Alta |
| **Colores** | Primary: #1E88E5, Error: #E53935 | Alta |
| **Tipografia** | H1: 24px bold, Body: 16px regular | Alta |
| **Espaciado** | Gap entre items: 12px | Alta |
| **Componentes** | Botones, cards, inputs (con estados) | Alta |
| **Animaciones** | Duracion: 300ms, Curve: easeInOut | Media |
| **Responsivo** | Que cambia en tablet vs mobile | Media |
| **Empty states** | Que mostrar cuando no hay datos | Media |
| **Loading states** | Skeleton, spinner, shimmer | Media |
| **Error states** | Mensajes de error, retry | Alta |

## Como Leer un Archivo de Diseno

### Paso 1: Entender la estructura

Abre Figma y navega asi:

```
┌───────────────────────────────────────────────┐
│  FIGMA: Estructura del archivo                │
│                                               │
│  📁 Paginas                                   │
│  ├── 📄 Mobile                                │
│  │   ├── 🖼️ Home Screen                       │
│  │   ├── 🖼️ Login Screen                      │
│  │   └── 🖼️ Profile Screen                    │
│  ├── 📄 Tablet                                │
│  │   └── 🖼️ Home Screen (tablet)              │
│  ├── 📄 Components                            │
│  │   ├── 🔲 Button                            │
│  │   ├── 🔲 Card                              │
│  │   └── 🔲 Input                             │
│  └── 📄 Flows                                 │
│      └── 🔄 Login Flow                        │
└───────────────────────────────────────────────┘
```

### Paso 2: Inspeccionar propiedades

En Figma, selecciona un elemento y mira el panel derecho:

| Propiedad | Donde buscarla | Equivalente Flutter |
|-----------|---------------|-------------------|
| **Size** | Panel derecho > Frame | `width:`, `height:` |
| **Padding** | Panel derecho > Auto Layout | `Padding()` o `EdgeInsets` |
| **Color** | Panel derecho > Fill | `color: Color(0xFF...)` |
| **Border Radius** | Panel derecho > Corner Radius | `BorderRadius.circular()` |
| **Typography** | Panel derecho > Text | `TextStyle(fontSize:, fontWeight:)` |
| **Shadow** | Panel derecho > Effects | `BoxShadow()` |
| **Opacity** | Panel derecho > Layer | `opacity:` |

### Paso 3: Identificar componentes reutilizables

```
┌─────────────────────────────────────────────────────────────────┐
│  COMPONENTES COMUNES Y SU EQUIVALENTE FLUTTER                   │
│                                                                 │
│  Figma                    →  Flutter                            │
│  ─────────────────────────────────────────────                  │
│  Auto Layout Frame        →  Row / Column / Flex               │
│  Component (main)         →  StatelessWidget                   │
│  Component (with state)   →  StatefulWidget                     │
│  Variant                  →  Parametros del widget             │
│  Instance                 →  Widget instance                   │
│  Boolean property         →  Widget parameter (bool)           │
│  Text property            →  Widget parameter (String)         │
└─────────────────────────────────────────────────────────────────┘
```

## Traduciendo Disenos a Widgets

### Mapeo mental Figma → Flutter

Cada elemento de Figma tiene un equivalente natural en Flutter:

| Elemento Figma | Widget Flutter | Ejemplo |
|---------------|---------------|---------|
| Frame con auto layout | `Row`, `Column`, `Flex` | Layout horizontal/vertical |
| Rectangle | `Container`, `DecoratedBox` | Cards, backgrounds |
| Text | `Text` | Labels, titulos |
| Image | `Image.asset`, `CachedNetworkImage` | Avatars, fotos |
| Icon | `Icon` | Botones, indicadores |
| Button | `ElevatedButton`, `TextButton` | Acciones |
| Input | `TextField`, `TextFormField` | Formularios |
| Scroll | `ListView`, `SingleChildScrollView` | Contenido largo |
| Overlay | `Stack`, `Positioned` | Badges, floating buttons |

### Ejemplo: De Figma a Codigo

**Diseno en Figma:**
```
┌──────────────────────────────────────┐
│ ┌──────────────────────────────────┐ │
│ │ ┌────┐  Nombre del Usuario       │ │
│ │ │ 🖼️ │  email@ejemplo.com        │ │
│ │ └────┘                           │ │
│ │                    [Ver perfil]   │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
```

**Codigo Flutter:**
```dart
Card(
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Row(
      children: [
        CircleAvatar(
          radius: 24,
          backgroundImage: NetworkImage(user.avatarUrl),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(user.name, style: Theme.of(context).textTheme.titleMedium),
              Text(user.email, style: Theme.of(context).textTheme.bodySmall),
            ],
          ),
        ),
        TextButton(
          onPressed: () => context.push('/profile/${user.id}'),
          child: const Text('Ver perfil'),
        ),
      ],
    ),
  ),
)
```

## El Loop de Feedback: Cuando el Diseno no Funciona Tecnicamente

A veces el diseno es **imposible o muy costoso** de implementar. No lo ignores — comunicalo.

```
┌─────────────────────────────────────────────────────────────────┐
│            LOOP DE FEEDBACK EFECTIVO                            │
│                                                                 │
│  1. IDENTIFICAR    →  "Esta animacion tiene costo O(n^2)"      │
│         │                                                       │
│         ▼                                                       │
│  2. COMUNICAR      →  "Hay una limitacion tecnica en..."       │
│         │                                                       │
│         ▼                                                       │
│  3. PROPONER       →  "Podemos hacer X como alternativa"       │
│         │                                                       │
│         ▼                                                       │
│  4. COLABORAR      →  "Que te parece esta alternativa?"        │
│         │                                                       │
│         ▼                                                       │
│  5. DECIDIR        →  "La alternativa平衡a costo y UX"         │
│                                                                 │
│  ⚠️ NUNCA: "Eso no se puede hacer" (sin explicar ni proponer)  │
└─────────────────────────────────────────────────────────────────┘
```

### Plantillas de comunicacion

**Cuando hay una limitacion tecnica:**

```
"Hola [disenador], revise el diseno de [pantalla] y tengo una
observacion sobre [elemento especifico].

El problema es que [explicacion tecnica breve, sin jerga].
Esto significaria que [impacto en usuario/rendimiento].

Como alternativa, podemos:
1. [Opcion A] - [pros/contras]
2. [Opcion B] - [pros/contras]

Que te parece? Podemos discutirlo en el daily."
```

**Cuando necesitas aclaracion:**

```
"Hola, tengo una duda sobre el diseno de [pantalla].

En Figma veo que [descripcion de lo que ves], pero no queda claro:
1. [Pregunta especifica 1]
2. [Pregunta especifica 2]

Esto es para asegurar que la implementacion sea fiel al diseno."
```

## User Stories y Acceptance Criteria

### Lo que un developer necesita de un PM

| Elemento | Que es | Ejemplo |
|----------|--------|---------|
| **User Story** | Que quiere hacer el usuario | "Como usuario, quiero registrarme con email" |
| **Acceptance Criteria** | Como saber que esta completo | "El usuario recibe email de verificacion" |
| **Edge Cases** | Que pasa en situaciones limite | "Que pasa si el email ya existe?" |
| **Prioridad** | Que es urgente y que no | P0 = critico, P1 = importante, P2 = nice-to-have |
| **Estimacion** | Cuanto tiempo toma | T-shirt sizing o story points |

### Formato de User Story

```
┌─────────────────────────────────────────────────────────────────┐
│  USER STORY TEMPLATE                                            │
│                                                                 │
│  Como [rol del usuario],                                        │
│  quiero [accion],                                               │
│  para [beneficio/razon].                                        │
│                                                                 │
│  ACCEPTANCE CRITERIA:                                           │
│  - [ ] [Criterio 1: condicion verificable]                     │
│  - [ ] [Criterio 2: condicion verificable]                     │
│  - [ ] [Criterio 3: condicion verificable]                     │
│                                                                 │
│  EDGE CASES:                                                    │
│  - [Que pasa si X?]                                             │
│  - [Que pasa si Y?]                                             │
│                                                                 │
│  ESTIMACION: [T-shirt size: S/M/L/XL]                          │
│  PRIORIDAD: [P0/P1/P2]                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Ejemplo completo

```
US-127: Login con Google

COMO usuario nuevo,
QUIERO iniciar sesion con mi cuenta de Google,
PARA no tener que crear una cuenta nueva.

ACCEPTANCE CRITERIA:
- [ ] El boton "Continuar con Google" muestra el dialogo de Google
- [ ] Al autenticarse correctamente, el usuario es redirigido a Home
- [ ] Si el usuario cancela, permanece en la pantalla de login
- [ ] Si hay error de red, se muestra un snackbar con opcion de reintentar
- [ ] El perfil del usuario se crea en Supabase con datos de Google

EDGE CASES:
- Que pasa si el usuario tiene multiples cuentas de Google?
- Que pasa si la conexion se corta durante la autenticacion?
- Que pasa si el usuario ya tiene cuenta con ese email?

ESTIMACION: M
PRIORIDAD: P0
```

## Malentendidos Comunes entre Roles

| Malentendido | Developer piensa | Disenador/PM piensa | Solucion |
|-------------|-----------------|-------------------|----------|
| "Hazlo igual al diseno" | "Es una guia, no exacto" | "Debe ser pixel-perfect" | Acordar tolerancia de ±2px |
| "Es rapido de hacer" | "No entiende la complejidad" | "Es solo un boton" | Estimar con datos, no suposiciones |
| "No hay tiempo para tests" | "El codigo sera fragil" | "Tenemos deadline" | Mostrar costo de bugs en produccion |
| "El diseno no es responsivo" | "No me dieron tablet view" | "Deberia funcionar siempre" | Pedir disenos para todas las plataformas |
| "Cambia todo el tiempo" | "No pueden definirse" | "Surgen nuevas necesidades" | Buffer de 20% en estimaciones |

## Cuando Hacer Pushback en un Diseno

### Pushback JUSTIFICADO ✅

| Situacion | Por que | Como decirlo |
|-----------|---------|-------------|
| Diseno ignora plataforma | iOS y Android tienen patrones diferentes | "En iOS los usuarios esperan X" |
| Performance impact | Animacion costosa en低端 devices | "Esto puede causar jank en devices viejos" |
| Accesibilidad | Contraste insuficiente, targets muy pequenos | "El contraste no cumple WCAG AA" |
| Inconsistencia con design system | Mismo patron, diferente implementacion | "Ya tenemos un componente para esto" |
| Datos no existen | Diseno asume datos que no tenemos | "No tenemos esa informacion en la API" |

### Pushback que NO debes hacer ❌

| Situacion | Por que no | Que hacer en su lugar |
|-----------|-----------|---------------------|
| "No me gusta el color" | Preferencia personal, no tecnica | Enfocarte en accesibilidad |
| "Es muy trabajo" | No es razon tecnica | Estimar y explicar el costo |
| "Nunca lo hemos hecho asi" | Resistencia al cambio | Probar la propuesta nueva |
| "Los usuarios no quieren eso" | No tienes datos | Pedir data o testing |

## Resumen

```
┌─────────────────────────────────────────────────────────────────┐
│           COLABORACION CON DISENO Y PRODUCTO                    │
│                                                                 │
│  ✅ Entiende el rol de cada persona en el triangulo            │
│  ✅ Aprende a leer archivos de Figma como un pro               │
│  ✅ Mapea componentes de Figma a widgets de Flutter            │
│  ✅ Comunica limitaciones tecnicas con alternativas            │
│  ✅ Pide user stories con acceptance criteria claros           │
│  ✅ Pushback basado en datos, no en preferencias               │
│  ✅ Documenta decisiones de diseno y tecnicas                  │
└─────────────────────────────────────────────────────────────────┘
```
