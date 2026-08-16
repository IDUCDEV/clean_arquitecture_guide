# Sección 20: Protocolo de Resolución de Problemas Algorítmicos

> Una guía metódica y universal para resolver problemas de algoritmos, estructuras de datos y POO — desde problemas básicos hasta retos tipo HackerRank y LeetCode.

---

## ¿Para qué sirve esta sección?

Los problemas algorítmicos no se resuelven "solo sabiendo programar". Existe una **metodología repetible** que convierte cualquier enunciado en una solución correcta y eficiente. Esta sección enseña ese protocolo.

A diferencia de la sección 09 (Estructuras de Datos con OOP), que enseña **cómo usar** las estructuras en Dart, esta sección enseña **cuándo elegir** qué estructura y algoritmo aplicar para resolver un problema concreto.

---

## Ruta de aprendizaje sugerida

```
Tiempo estimado: 25-35 horas

1. Leer 01-metodologia-general.md          (30 min)  ← Framework de 6 pasos
2. Leer 02-analisis-complejidad.md          (90 min)  ← Proceso completo con 5 ejemplos reales
3. Leer 03-reconocimiento-patrones.md       (60 min)  ← El corazón de la guía
4. Leer 04-estructuras-datos-referencia.md  (40 min)  ← Rápida referencia
5. Leer 05-patrones-avanzados.md            (90 min)  ← Templates listos para usar
6. Leer 06-comunicacion-y-pseudocodigo.md   (30 min)  ← Para entrevistas
7. Practicar con 07-ejercicios-practica.md  (5-10h)   ← Ejecutar
8. Leer 09-recursion-y-backtracking.md      (60 min)  ← Recursión y backtracking
9. Leer 10-system-design-basico.md          (45 min)  ← System Design para entrevistas
10. Leer 11-errores-comunes-patron.md       (30 min)  ← Errores a evitar
11. Practicar con 12-ejercicios-adicionales (10-15h)  ← +25 ejercicios
12. Consultar 08-recursos-externos.md       (15 min)  ← Para seguir practicando
```

---

## Contenido

| # | Archivo | Descripción |
|---|---------|-------------|
| 01 | [Metodología General](./01-metodologia-general.md) | Framework de 6 pasos universal |
| 02 | [Análisis de Complejidad](./02-analisis-complejidad.md) | Proceso de 5 pasos con 5 ejemplos reales (Two Sum, Beautiful Days, Jumping Clouds, Circular Array, Sequence Equation) + referencia rápida |
| 03 | [Reconocimiento de Patrones](./03-reconocimiento-patrones.md) | Mapa señales→patrón, árbol de decisión |
| 04 | [Estructuras de Datos: Referencia Rápida](./04-estructuras-datos-referencia.md) | Tipo de input→estructura recomendada |
| 05 | [Patrones Avanzados](./05-patrones-avanzados.md) | 8 patrones con template Dart |
| 06 | [Comunicación y Pseudocódigo](./06-comunicacion-y-pseudocodigo.md) | Pseudocódigo y comunicación en entrevistas |
| 07 | [Ejercicios de Práctica](./07-ejercicios-practica.md) | 10 ejercicios progresivos con solución |
| 08 | [Recursos Externos](./08-recursos-externos.md) | Libros, plataformas, canales |
| 09 | [Recursión y Backtracking](./09-recursion-y-backtracking.md) | Template recursión + backtracking + memoización |
| 10 | [System Design Básico](./10-system-design-basico.md) | Framework de 4 pasos para entrevistas |
| 11 | [Errores Comunes](./11-errores-comunes-patron.md) | Patrones de error por fase y tipo de problema |
| 12 | [Ejercicios Adicionales](./12-ejercicios-adicionales.md) | +25 ejercicios organizados por dificultad |

---

## Relación con otros módulos

| Módulo | Relación |
|--------|----------|
| **09-ESTRUCTURA-DATOS-OOP** | Predecesor. Allí aprendes *cómo* usar List, Set, Map y OOP en Dart. Aquí aprendes *cuándo* elegir cada uno para resolver un problema. |
| **01-CLEAN-ARCHITECTURE** | Complementario. Clean Architecture organiza código de producción; esta guía resuelve problemas aislados de algoritmos. |
| **16-BLOC-CUBIT** | Indirecto. Los patrones de resolución de problemas se aplican también al diseño de BLoCs (pensamiento en estados y transiciones). |
| **22-DISENIO-SISTEMAS** | Continuación. El archivo `10-system-design-basico.md` es el intro de 45 min; el módulo 22 lo expande con la plantilla completa y casos integradores. |

---

## ¿Cuándo usar esta guía?

- Estás resolviendo un problema en HackerRank, LeetCode, Codewars o similar
- Tienes una entrevista técnica y necesitas un proceso estructuado
- Te enfrentas a un problema donde no sabes qué algoritmo aplicar
- Quieres mejorar tu capacidad de reconocer patrones en enunciados
