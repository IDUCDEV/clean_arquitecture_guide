# El Costumbre de la IA

> Antes de aprender a trabajar sin IA, necesitas entender por qué dependes de ella y qué te cuesta esa dependencia.

---

## 1. Cómo la IA atrofia tus habilidades

La IA no es mala. El problema es **cómo la usas**.

Cuando la usas como primer recurso en lugar de último, tu cerebro deja de hacer el trabajo que lo hace crecer:

```
┌─────────────────────────────────────────────────────────────────┐
│                  LO QUE OCURRE EN TU CEREBRO                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SIN IA (el proceso natural):                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ Recibir  │ →  │ Pensar   │ →  │ Fallar   │ →  │ Entender │ │
│  │ problema │    │ enfoque  │    │ corregir │    │ por qué  │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       ↑                                             │          │
│       └─────────── APRENDIZAJE ←────────────────────┘          │
│                                                                 │
│  CON IA (el atajo):                                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │ Recibir  │ →  │ Preguntar│ →  │ Copiar   │                  │
│  │ problema │    │ a IA     │    │ código   │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
│                                         │                       │
│                                         ↓                       │
│                                   ┌──────────┐                  │
│                                   │ No       │                  │
│                                   │ entiendes│                  │
│                                   └──────────┘                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**La diferencia clave:** El primer proceso duele pero construye comprensión. El segundo es rápido pero no construye nada.

---

## 2. Señales de que estás dependiendo demasiado

Marca con una X cada señal que reconozcas en ti:

### Señales de código
- [ ] Copias código de IA sin leerlo completamente
- [ ] No puedes explicar por qué funciona algo que escribiste
- [ ] Cambias código generado por IA sin entender qué estás cambiando
- [ ] Tu código tiene funciones que no reconocerías si te las preguntaran
- [ ] No puedes hacer debugging sin pedirle a IA que lo analice

### Señales de proceso
- [ ] Tu primer impulso ante un problema es abrir ChatGPT/Copilot
- [ ] No lees documentación oficial de paquetes
- [ ] No puedes estimar cuánto toma una feature
- [ ] Te sientes perdido cuando IA no está disponible
- [ ] Evitas features que parecen "muy complejas" porque no confías en ti

### Señales de conocimiento
- [ ] Has olvidado conceptos que antes dominabas (loops, recursión, patrones)
- [ ] No reconoces errores básicos en código generado por IA
- [ ] No puedes resolver un problema de algoritmos sin asistencia
- [ ] Tu capacidad de debugging ha disminuido
- [ ] Sientes "neblina mental" cuando intentas pensar por tu cuenta

**Si marcaste 3 o más:** Tu dependencia ya está afectando tu capacidad profesional.

---

## 3. El costo real de la dependencia

### En entrevistas técnicas

```
┌─────────────────────────────────────────────────────────────────┐
│                 ENTREVISTA TÉCNICA                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Pregunta: "Diseña un sistema de cache para una app de聊天"    │
│                                                                 │
│  Desarrollador con práctica:                                    │
│  → Piensa en el patrón Strategy                                 │
│  → Considera invalidación de cache                              │
│  → Propone una arquitectura                                     │
│  → Escribe código en la pizarra                                 │
│                                                                 │
│  Desarrollador dependiente de IA:                               │
│  → No sabe por dónde empezar                                    │
│  → Intenta recordar qué le dijo IA antes                        │
│  → No puede escribir código sin autocompletado                  │
│  → Pregunta: "¿Puedo usar mi laptop?"                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### En mantenimiento de código legacy

Cuando heredas código que nadie documentó:
- **Sin dependencia:** Puedes leerlo, entenderlo, modificarlo
- **Con dependencia:** Pegas el código en IA y esperas que lo explique. Pero si IA no entiende el contexto específico de tu app, estás perdido.

### En debugging sin conexión

- Producción caída a las 3 AM
- Sin acceso a IA (o IA te da la respuesta incorrecta)
- **Sin dependencia:** Lees el stack trace, buscas en el código, razonas
- **Con dependencia:** No puedes funcionar

---

## 4. La mentalidad correcta

### Principio: IA como verificador, no generador

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  MAL USO:                    BUEN USO:                          │
│  "IA, crea un UseCase"      "IA, revisa mi UseCase"            │
│                                                                 │
│  Tú no piensas.             Tú piensas primero.                │
│  IA decide.                 Tú decides.                         │
│  Copias.                    Validas.                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### El principio del esfuerzo mínimo forzado

Antes de usar IA, pregúntate:

> "¿Puedo resolver esto con lo que sé ahora?"

- **Si la respuesta es sí:** Resuélvelo tú. No uses IA.
- **Si la respuesta es "no sé pero puedo intentar":** Intenta 30 minutos. Luego consulta IA para validar, no para generar.
- **Si la respuesta es "genuinamente no tengo conocimiento":** Investiga documentación oficial primero. IA como último recurso.

### "Si no puedo explicarlo, no lo entiendes"

**Regla de oro:** Después de escribir código (con o sin IA), pregúntate:

> "¿Puedo explicarle a otro desarrollador por qué cada línea está ahí?"

Si la respuesta es no, necesitas entenderlo antes de continuar.

---

## 5. El objetivo no es eliminar la IA

El objetivo es **tener el control**:

| Dependencia | Autonomía |
|-------------|-----------|
| IA es tu cerebro | IA es tu herramienta |
| Copias sin entender | Entiendes antes de usar |
| No puedes sin ella | Funcionas sin ella |
| Ansiedad sin conexión | Confianza en ti mismo |
| Código que no reconoces | Código que puedes explicar |

**La meta:** Poder construir cualquier feature sin IA, y usar IA para hacerlo más rápido — no para que lo haga por ti.

---

## 6. Tu compromiso

Antes de continuar con el siguiente archivo, escribe en un papel:

1. ¿Cuántas de las señales de la sección 2 me representan?
2. ¿Cuál es la consecuencia más grave que me ha causado la dependencia?
3. ¿Qué feature he evitado hacer porque "era muy compleja"?

Sé honesto contigo mismo. Este es el primer paso para cambiar.

---

**Siguiente:** [07-el-flujo-de-trabajo.md](./07-el-flujo-de-trabajo.md) — El framework de 6 fases para trabajar sin IA
