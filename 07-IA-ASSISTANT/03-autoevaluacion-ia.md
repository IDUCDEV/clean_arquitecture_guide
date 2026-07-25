# 03: Autoevaluación de Uso de IA

> Antes de pedirle a la IA que escriba código, evalúa si realmente lo necesitas.

---

## El test de 3 preguntas

Antes de usar IA para cualquier tarea, hazte estas 3 preguntas:

### Pregunta 1: ¿Puedo resolverlo yo?
```
SÍ → Resuélvelo tú. Es la forma de mantener tus habilidades.
NO → Ve a Pregunta 2.
```

### Pregunta 2: ¿Lo resolví antes sin IA?
```
SÍ → Intenta recordar cómo. Busca en tus notas, documentación.
NO → Ve a Pregunta 3.
```

### Pregunta 3: ¿Es algo que la IA hace bien?
```
SÍ (boilerplate, CRUD, tests básicos) → Pide ayuda a la IA.
NO (lógica de negocio, arquitectura, decisiones de diseño) → Resuélvelo tú.
```

---

## Matriz de decisiones

| Tarea | Hacer tú | Pedir a IA |
|-------|----------|------------|
| Lógica de negocio | ✅ Siempre | ❌ Nunca |
| Arquitectura | ✅ Siempre | ❌ Nunca |
| Decisiones de diseño | ✅ Siempre | ❌ Nunca |
| Entity/Model (boilerplate) | ⚠️ A veces | ✅ OK |
| Repository CRUD | ⚠️ A veces | ✅ OK |
| Tests básicos | ⚠️ A veces | ✅ OK |
| Configuración de tools | ⚠️ A veces | ✅ OK |
| Code review | ✅ Siempre | ❌ Nunca |
| Debugging | ✅ Siempre | ⚠️ Solo para errores conocidos |
| Refactoring | ✅ Siempre | ⚠️ Solo para patterns conocidos |

---

## Score de autonomía

Calcula tu score semanal:

```
Tareas resueltas sin IA:    ___ / ___ total
Score = (sin IA / total) × 100

90-100% → Excelente. Mantén esto.
70-89%  → Bien. Puedes mejorar un poco.
50-69%  → Regular. Necesitas practicar más.
< 50%   → Crítico. Revisa trabajar-sin-ia/.
```

---

## Hábitos a desarrollar

### Antes de código
- [ ] Leo la documentación oficial primero
- [ ] Intento resolver el problema en papel/pseudocódigo
- [ ] Busco si ya existe una solución en el codebase

### Durante el código
- [ ] No copio código de IA sin entenderlo
- [ ] Implemento la lógica crítica yo mismo
- [ ] Solo uso IA para boilerplate

### Después del código
- [ ] Reviso todo el código generado por IA
- [ ] Verifico que funciona como esperaba
- [ ] No doy por hecho que "si la IA lo generó, está bien"

---

**Volver:** [README.md](./README.md)
