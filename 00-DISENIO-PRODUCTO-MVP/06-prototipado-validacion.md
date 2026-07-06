# 06 — Prototipado + Validación

**Día 4: Construir → Día 5: Testear con usuarios**

---

## Fase 5: Prototype

El objetivo es construir un **prototipo realista** del MVP en 1 día. No es código real, es una simulación convincente.

### Opción A: Prototipado en Figma (recomendada para no-devs)

Figma + [Material 3 Design Kit](https://www.figma.com/community/file/1035203688168086460).

```
Storyboard del Día 3
       ↓
Componentes M3 en Figma (arrastrar y soltar)
       ↓
Conexiones y flujos (prototyping mode)
       ↓
Prototipo navegable listo para test
```

**Ventajas:** Rápido (medio día), cualquier persona del equipo puede hacerlo.
**Desventajas:** No muestra comportamiento real (scroll, carga, etc.).

### Opción B: Prototipado en Flutter (recomendada para devs)

Usa el template de este módulo para construir el MVP funcional.

```
flutter create --template app mvp_prototipo
→ Copiar template theme/ de este módulo
→ Implementar las 3-4 pantallas del Golden Path
→ Datos mock (sin backend)
```

**Ventajas:** Comportamiento real, reutilizable como base del producto final.
**Desventajas:** Más lento (1 día completo o más).

### Opción C: Híbrida (recomendada)

```
Jueves AM: Figma → prototipo visual navegable (para testear el viernes)
Jueves PM: Flutter → empezar a codificar las pantallas (para producción)
```

### Guía rápida: Prototipado en Figma con M3

1. **Instala el kit M3**: https://www.figma.com/community/file/1035203688168086460
2. **Define tu theme**: seed color → genera la paleta con [Material Theme Builder](https://m3.material.io/theme-builder)
3. **Arma las pantallas**: arrastra componentes M3 (NavigationBar, Card, FilledButton, etc.)
4. **Conecta los flujos**: usa Figma Prototyping para enlazar pantallas
5. **Tip**: no diseñes todas las pantallas. Solo el Golden Path (3-4 pantallas) + estados clave (carga, error, vacío).

---

## Fase 6: Validate

El día más importante del Sprint. Pones el prototipo frente a **5 usuarios reales** y observas.

### ¿Por qué 5 usuarios?

Con 5 usuarios encuentras ~85% de los problemas de usabilidad. Después del quinto, ves los mismos problemas una y otra vez.

### Cómo reclutar usuarios

| Método | Tiempo | Costo |
|---|---|---|
| Clients actuales | 1-2 días | Gratis |
| Redes sociales | 2-3 días | Gratis |
| UserInterviews.com | 2-5 días | ~$50-100/usuario |
| Respondent.io | 2-5 días | ~$100-200/usuario |

Perfil de usuario ideal: alguien que **tiene el problema** que tu MVP resuelve.

### Estructura de la entrevista (30 min)

```
5 min  → Bienvenida y contexto ("cuéntame de ti")
5 min  → Pregunta sobre el problema actual ("¿cómo reservas hoy?")
15 min → Test del prototipo ("ahora quiero que reserves una cancha")
          → Observa en silencio
          → No ayudes, no expliques
          → Pide que piense en voz alta
5 min  → Cierre ("¿qué te pareció? ¿comprarías esto?")
```

### Qué observar

| Señal positiva | Señal de alerta |
|---|---|
| Navega sin ayuda | Se queda en blanco >5s |
| Completa la tarea | Toca donde no hay botón |
| Dice "esto es justo lo que necesito" | Dice "¿y esto qué hace?" |
| Pregunta por precio | Pregunta "¿cómo vuelvo atrás?" |
| Sonríe/celebra al completar | Frunce el ceño, suspira |

### Matriz de resultados

Después de los 5 tests, clasifica los hallazgos:

```
                         Impacto en el usuario
                      Bajo              Alto
          ┌───────────────────────────────┐
  Fácil   │  Bajo / Fácil     │  Alto / Fácil   │
  de      │  (mejora rápida)  │  (prioridad!)   │
  arreglar│───────────────────┼─────────────────│
          │  Bajo / Difícil   │  Alto / Difícil  │
  Difícil │  (pospuesto)      │  (requiere       │
          │                   │   rediseño)      │
          └───────────────────────────────────────┘
```

### Decisiones post-Sprint

Con los resultados, tienes 3 opciones:

| Resultado | Acción |
|---|---|
| ✅ Los usuarios completaron el flujo y mostraron interés | **Pasar a desarrollo**: el MVP está validado |
| ❌ Los usuarios no completaron el flujo o no vieron valor | **Pivotar**: cambiar enfoque o solución |
| ⚠️ Resultados mixtos | **Iterar**: ajustar el prototipo y testear de nuevo (mini-Sprint de 2 días) |

### Checklist del Día 5

- [ ] 5 entrevistas completadas
- [ ] Grabaciones (audio/video) guardadas
- [ ] Matriz de hallazgos completada
- [ ] Decisión tomada: ✅ desarrollo / 🔄 iterar / ❌ pivotar
- [ ] Próximos pasos documentados

---

## Del prototipo validado al código Flutter

Una vez validado, el prototipo (Figma o Flutter) se convierte en el **contrato de diseño** para implementación.

En el siguiente capítulo verás cómo llevar el theme M3 a código Flutter.

---

**Siguiente: [07 — M3 a Flutter: Implementación](07-m3-flutter-implementacion.md)**
