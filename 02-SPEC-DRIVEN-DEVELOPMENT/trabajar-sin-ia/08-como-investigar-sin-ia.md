# Cómo Investigar Sin IA

> Antes de que existiera ChatGPT, los desarrolladores resolvían problemas todos los días. Aquí están las herramientas que usaban (y que siguen siendo mejores).

---

## 1. El orden correcto de investigación

```
┌─────────────────────────────────────────────────────────────────┐
│              JERARQUÍA DE FUENTES (mejor a peor)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 📄 Documentación oficial del paquete/servicio              │
│     → Fuente primaria, siempre actualizada                    │
│                                                                 │
│  2. 💻 Repositorio oficial (GitHub)                            │
│     → Código fuente, issues,discusiones, ejemplos              │
│                                                                 │
│  3. 📦 pub.dev (para paquetes Flutter/Dart)                    │
│     → README, ejemplos, changelog, dependencias                │
│                                                                 │
│  4. 🔍 Stack Overflow / foros especializados                   │
│     → Problemas específicos con soluciones probadas             │
│                                                                 │
│  5. 📝 Blog posts de desarrolladores expertos                  │
│     → Tutoriales prácticos, opiniones fundamentadas            │
│                                                                 │
│  6. 📚 Libros y documentación académica                        │
│     → Fundamentos, patrones, diseño                             │
│                                                                 │
│  7. 🤖 IA (sólo como último recurso)                           │
│     → Confirmar, no descubrir                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Cómo leer documentación oficial

La mayoría de los desarrolladores no saben leer documentación. Sigue este proceso:

### Paso 1: Busca la documentación oficial

```
¿Cómo encontrar la documentación oficial?

Para paquetes Flutter/Dart:
  → pub.dev/packages/[nombre_del_paquete]
  → Click en "Readme" y "Example"

Para servicios:
  → [nombre_del_servicio].com/docs
  → Ejemplo: supabase.com/docs, firebase.google.com/docs

Para APIs:
  → [servicio]/api/docs
  → Ejemplo: stripe.com/docs/api
```

### Paso 2: Lee en este orden

```
1. README
   → ¿Qué hace este paquete?
   → ¿Cuáles son sus características principales?
   → ¿Cómo se instala?

2. Guía de inicio rápido (Quick Start)
   → ¿Cómo lo uso para el caso más básico?
   → ¿Qué configuración necesita?

3. Ejemplos
   → ¿Cómo se ve el código en la práctica?
   → ¿Qué patrones usa?

4. API Reference
   → ¿Qué métodos/clases tiene?
   → ¿Qué parámetros aceptan?
   → ¿Qué retornan?

5. Changelog / Versiones
   → ¿Qué cambió recientemente?
   → ¿Hay breaking changes?
```

### Paso 3: Documenta lo que aprendes

```markdown
## Investigación: [Nombre del paquete/servicio]

### Qué hace
[Descripción en tus palabras]

### Cómo se instala
[Pasos]

### Ejemplo básico
[Código de ejemplo]

### Limitaciones conocidas
[Lo que no hace o hace mal]

### Versión que usaré
[vX.Y.Z] - [Por qué esta versión]
```

---

## 3. Cómo usar GitHub para investigar

GitHub es la mejor herramienta de investigación que existe. Tiene todo: código, discusiones, errores documentados.

### 3.1 Leer el README del repositorio

```
Busca:
✅ Descripción del proyecto
✅ Características (features)
✅ Requisitos previos
✅ Instrucciones de instalación
✅ Ejemplos de uso
✅ Contributing guidelines
✅ License
```

### 3.2 Revisar issues (problemas)

```
Busca en Issues:

1. Issues cerradas con "wontfix" o "by design"
   → Entiende qué NO hace el paquete

2. Issues abiertas con muchos thumbs-up
   → Problemas conocidos que otros tienen

3. Issues con "question"
   → Preguntas frecuentes de otros desarrolladores

4. Issues con "bug" + estado abierto
   → Errores conocidos que debes evitar
```

### 3.3 Buscar en el código fuente

```
Cuando la documentación no aclara algo:

1. Ve al repositorio en GitHub
2. Busca en el código fuente la función/clase que necesitas
3. Lee los comentarios del código
4. Busca cómo otros la usan (git blame, commits recientes)
```

### 3.4 Usar GitHub Search

```
Búsquedas útiles:

nombre_del_paquete "ejemplo de uso"
nombre_del_paquete "error" is:issue is:closed
nombre_del_paquete flutter tutorial
```

---

## 4. Cómo usar pub.dev

### 4.1 Evaluar un paquete

Antes de usar un paquete, evalúa si es confiable:

```
┌─────────────────────────────────────────────────────────────────┐
│ CHECKLIST DE EVALUACIÓN DE PAQUETE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ □ Likes: ¿Tiene más de 100?                                   │
│ □ Pub Points: ¿Tiene más de 120/160?                          │
│ □ Popularidad: ¿Está en el top 5%?                             │
│ □ Última actualización: ¿Es reciente (< 6 meses)?             │
│ □ Soporte de plataforma: ¿Soporta todas las que necesitas?     │
│ □ Dependencias: ¿Depende de paquetes confiables?               │
│ □ License: ¿Es compatible con tu proyecto?                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Leer el README de pub.dev

```
Secciones importantes:

1. Features
   → ¿Qué hace exactamente?

2. Installation
   → ¿Cómo se agrega a tu proyecto?

3. Usage
   → Ejemplos de código básicos

4. API Reference
   → Métodos disponibles, parámetros, tipos

5. Changelog
   → Qué cambió en cada versión
```

---

## 5. Cómo buscar en Stack Overflow

### 5.1 Formular buenas búsquedas

```
MAL:  "flutter how to do stuff"
BIEN: "flutter [nombre_del_paquete] [problema_específico]"

Ejemples:
✅ "flutter supabase realtime stream not working"
✅ "dart isolate background task example"
✅ "flutter bloc state management best practices"
```

### 5.2 Evaluar respuestas

```
No todas las respuestas de SO son confiables. Busca:

✅ Respuestas con más votos (upvotes)
✅ Respuestas aceptadas por el autor de la pregunta
✅ Respuestas con código de ejemplo
✅ Respuestas recientes (no de 2018)

Ignora:
❌ Respuestas sin votos
❌ Respuestas con solo código sin explicación
❌ Respuestas muy antiguas (pueden estar desactualizadas)
```

---

## 6. Cómo encontrar tutoriales confiables

### Fuentes confiables

| Fuente | Tipo de contenido | Fiabilidad |
|--------|-------------------|------------|
| flutter.dev | Guías oficiales | ⭐⭐⭐⭐⭐ |
| dart.dev | Guías oficiales Dart | ⭐⭐⭐⭐⭐ |
| pub.dev | Ejemplos de paquetes | ⭐⭐⭐⭐ |
| Reso Coder | Tutoriales Flutter | ⭐⭐⭐⭐ |
| filledstacks | Tutoriales Flutter | ⭐⭐⭐⭐ |
| The Net Ninja | Tutoriales generales | ⭐⭐⭐⭐ |
| Fireship | Conceptos rápidos | ⭐⭐⭐ |

### Fuentes no confiables

| Fuente | Por qué |
|--------|---------|
| Tutoriales sin autor identificado | No puedes verificar credibilidad |
| Videos de YouTube sin fechas | Pueden estar desactualizados |
| Repositorios sin commits recientes | Pueden usar versiones viejas |
| Foros generales (Reddit) sin verificación | Pueden tener información incorrecta |

---

## 7. Cómo leer código de otros

Una habilidad que la IA te impide desarrollar: leer y entender código ajeno.

### Proceso para leer código

```
1. PRIMERO: Lee el README
   → Entiende qué hace el proyecto

2. SEGUNDO: Estructura de carpetas
   → ¿Cómo está organizado?

3. TERCERO: main.dart o entry point
   → ¿Dónde empieza todo?

4. CUARTO: Sigue el flujo principal
   → main → pantalla principal → datos → API

5. QUINTO: Lee las clases más importantes
   → Entities, repositories, use cases
```

### Qué buscar cuando lees código

```
✅ Patrones que reconoces (Clean Architecture, BLoC, etc.)
✅ Cómo manejan errores
✅ Cómo estructuran los tests
✅ Decisiones de diseño que no harías tú (¿por qué?)
✅ Dependencias que usan (¿cuáles no conocías?)
```

---

## 8. Ejercicio práctico: investigar un paquete

Elige un paquete que nunca hayas usado y sigue este proceso:

### Paso 1: Encuentra la documentación oficial
```bash
# Busca en pub.dev
# Ejemplo: intl (para internacionalización)
```

### Paso 2: Lee el README
- ¿Qué hace?
- ¿Cómo se instala?
- ¿Cuáles son sus características principales?

### Paso 3: Busca ejemplos
- Revisa el repositorio en GitHub
- Busca ejemplos de uso real

### Paso 4: Intenta algo básico
- Crea un proyecto mínimo
- Implementa la funcionalidad más simple del paquete

### Paso 5: Documenta
```markdown
## Investigación: [Nombre del paquete]

### Qué hace
[...]

### Cómo lo instalaría en mi proyecto
[...]

### Ejemplo mínimo funcional
[Código]

### Limitaciones
[...]

### ¿Lo usaría en producción?
[Sí/No + por qué]
```

---

## 9. Cuándo SÍ puedes usar IA

| Situación | ¿IA permitida? | Para qué |
|-----------|----------------|----------|
| No encuentras la documentación oficial | ✅ Sí | Para que te dé la URL |
| La documentación oficial es ambigua | ✅ Sí | Para que la explique con un ejemplo |
| No entiendes un concepto | ✅ Sí | Para que te lo explique (no para que escriba código) |
| Necesitas ver un patrón de uso | ✅ Sí | Como referencia, no como código a copiar |
| **Para escribir código** | ❌ No | Tú escribes, tú entiendes |
| **Para diseñar la solución** | ❌ No | Tú diseñas, tú decides |
| **Para debugging** | ⚠️ Limitado | Describe el problema tú, IA sugiere qué buscar |

---

**Siguiente:** [09-feature-simple-ejemplo.md](./09-feature-simple-ejemplo.md) — Ejemplo práctico: Feature simple sin IA
