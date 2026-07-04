## 9. Decisiones de Arquitectura

### Cubit vs BLoC

| Aspecto | Cubit | BLoC |
|---------|-------|------|
| Complejidad | Más simple | Más verboso |
| Uso | Funciones directas | Eventos específicos |
| Trazabilidad | Menor | Mayor |
| Ideal para | Mayoría de casos | Lógica compleja con múltiples eventos |

**Recomendación**: Empieza con `Cubit`. Si la lógica se vuelve muy compleja, refactoriza a `BLoC`.

### ¿Dónde va cada cosa?

| Situación | ¿Dónde va? | Ejemplo |
|-----------|-----------|---------|
| Validar formato email | Entity (getter) | `bool get isValidEmail` |
| Guardar en base de datos | DataSource | `await box.put(id, model)` |
| Decidir si uso cache o API | Repository | `if (isConnected) useRemote()` |
| Calcular impuestos | UseCase | `CalculateTaxUseCase` |
| Mostrar indicador de carga | Cubit (State) | `UserLoading()` |
| Navegar a otra pantalla | UI (Widget) | `Navigator.push(...)` |

### Preguntas Frecuentes

**¿Entity debe extender de Model?**
NO. Son responsabilidades diferentes.
- Entity = Lógica de negocio pura
- Model = Serialización técnica

**¿UseCase debe tener solo un método?**
SÍ, el método `call()`. Cada UseCase hace UNA sola cosa.

**¿Puedo llamar a un UseCase desde otro UseCase?**
NO. Los UseCases son independientes.

**¿Repository puede tener lógica de negocio?**
NO. Solo decide fuente de datos y convierte Model ↔ Entity.

**¿Puedo usar el Model en la UI?**
NO. La UI solo trabaja con Entities.

---
