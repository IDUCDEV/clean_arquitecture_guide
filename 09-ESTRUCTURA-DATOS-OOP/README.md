# 09 — Estructuras de Datos con OOP en Dart

> Domina la manipulación de datos en Dart: desde los fundamentos del sistema de tipos hasta patrones avanzados con colecciones, mapas y modelado orientado a objetos. **Este módulo es 50% teoría + 50% práctica intensiva**.

---

## 🎯 Objetivos

- Entender el sistema de tipos de Dart a fondo (null safety, genéricos, inferencia)
- Dominar `List`, `Set`, `Map` y todos sus métodos de transformación
- Escribir pipelines de datos con `map`, `where`, `reduce`, `fold`
- Modelar datos con OOP: entidades, value objects, inmutabilidad
- Aplicar patrones reales de manipulación de datos en Flutter
- **Hacer 25+ ejercicios prácticos** con casos del dominio real

---

## 📋 Índice

| Archivo | Descripción | Nivel |
|---------|-------------|-------|
| [01-sistema-tipos.md](./01-sistema-tipos.md) | Null safety, `var`/`final`/`const`, genéricos, typedefs | 🔤 Básico |
| [02-colecciones-fundamentos.md](./02-colecciones-fundamentos.md) | `List`, `Set`, `Map` — constructores, operaciones, performance | 📦 Básico |
| [03-metodos-funcionales-listas.md](./03-metodos-funcionales-listas.md) | `map`, `where`, `reduce`, `fold`, `expand`, encadenamiento | 🔗 Medio |
| [04-manipulacion-mapas.md](./04-manipulacion-mapas.md) | `Map.fromIterable`, `putIfAbsent`, `update`, group-by, merge | 🗺️ Medio |
| [05-algoritmos-colecciones.md](./05-algoritmos-colecciones.md) | `sort`, `Comparable`, `Comparator`, búsqueda, paginación | ⚡ Medio |
| [06-oop-modelado-datos.md](./06-oop-modelado-datos.md) | Entidades, Value Objects, `Equatable`, `copyWith`, `fromJson`/`toJson` | 🧱 Medio-Alto |
| [07-patrones-manipulacion.md](./07-patrones-manipulacion.md) | Patrones reales: fetch → filter → transform → aggregate | 🎯 Alto |
| [08-ejercicios-basicos.md](./08-ejercicios-basicos.md) | 10 ejercicios de fundamentos | 🏋️ Práctica |
| [09-ejercicios-intermedios.md](./09-ejercicios-intermedios.md) | 10 ejercicios con datos estructurados | 🏋️ Práctica |
| [10-ejercicios-avanzados.md](./10-ejercicios-avanzados.md) | 5 ejercicios integradores (mini-pipeline) | 🏋️ Práctica |
| [11-recursos-practica.md](./11-recursos-practica.md) | Dartpad, Codewars, Exercism, LeetCode, libros | 📚 Extra |

---

## 🧠 Mentalidad

```dart
// ❌ Lo que hace la IA por ti (y no entiendes):
final result = data.map((e) => e.name).where((n) => n.startsWith('A')).toList();

// ✅ Lo que sabrás hacer tú después de este módulo:
// 1. Sabes que .map() transforma CADA elemento
// 2. Sabes que .where() FILTRA con un test
// 3. Sabes que .toList() materializa el Iterable perezoso
// 4. Sabes que puedes encadenarlos porque devuelven Iterable
// 5. Sabes CUÁNDO usar map vs where vs expand vs fold
```

---

## 🚀 Orden de aprendizaje sugerido

```
01 → 02 → 03 → 04 → 05   (teoría + mini-práctica en cada uno)
       ↓
       06 → 07            (modelado + patrones del mundo real)
       ↓
       08 → 09 → 10       (PRACTICAR, PRACTICAR, PRACTICAR)
       ↓
       11                  (recursos para seguir aprendiendo)
```

> **💡 Regla de oro**: Después de leer cada archivo, abre [Dartpad](https://dartpad.dev) y **escribe el código tú mismo**. No copies y pegues.

---

## 📦 Conocimientos previos

Antes de empezar, deberías tener claro:
- Dart básico: funciones, clases, `import`
- Flutter básico: widgets, `setState`
- Clean Architecture (sección `01` de esta guía): capas Domain, Data, Presentation

---

## 🔗 Siguiente paso

Después de dominar este módulo, continúa con:
- [10-MAKEFILE/](../10-MAKEFILE/) — Entiende y domina los comandos de tu proyecto
- [11-GITHUB-ACTIONS/](../11-GITHUB-ACTIONS/) — Automatiza tu CI/CD
- También refuerza con `06-NIVEL-EXPERTO/04-streams-tiempo-real.md` para manipulación asíncrona

---

**Nivel:** Básico → Avanzado  
**Tiempo estimado:** 10-15 horas  
**Ejercicios:** 25+
