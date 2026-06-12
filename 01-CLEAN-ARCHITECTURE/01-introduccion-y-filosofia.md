# Guía Completa de Clean Architecture para Flutter

> Documento unificado que combina Introducción, Filosofía, Estructura, Flujo de Datos, Implementación Práctica con Sistema de Usuarios CRUD, Inyección de Dependencias, Testing y Templates.

---

> Este documento es parte de la sección 01 de la guía. Navega por los archivos numerados para seguir el orden de aprendizaje.

## 1. Introducción y Filosofía

### ¿Qué es Clean Architecture?

Clean Architecture, propuesta por Robert C. Martin (Uncle Bob), es un diseño de software que separa el código en capas independientes con una **regla de dependencia estricta**: las capas externas dependen de las internas, pero las internas no saben nada de las externas.

### La Analogía del Restaurante

Imagina un restaurante donde pides una hamburguesa:

| Tu Código | Restaurante | Qué Hace |
|-----------|-------------|----------|
| **Domain** | La Receta | Dice qué ingredientes necesitas |
| **Data** | La Cocina | Cocina los ingredientes |
| **Repository** | El Almacén | Decide si usa carne fresca o congelada |
| **UseCase** | El Chef | Sigue la receta paso a paso |
| **Cubit** | El Mesero | Lleva tu pedido y trae la comida |
| **UI** | Tu Mesa | Donde comes y pides |

**Regla importante**: Tú (UI) **NUNCA** entras a la cocina (Data). Todo pasa por el mesero (Cubit).

### La Analogía del Edificio de Oficinas

Clean Architecture organiza el código como un edificio de varias plantas:

```
         ┌─────────────────────────────────────┐
         │      PLANTA 4: UI (Presentation)    │
         │    ┌─────┐ ┌─────┐ ┌─────┐         │
         │    │Pág 1│ │Pág 2│ │Pág 3│         │
         │    └──┬──┘ └──┬──┘ └──┬──┘         │
         └───────┼───────┼───────┼─────────────┘
                 │       │       │
                 ▼       ▼       ▼
         ┌─────────────────────────────────────┐
         │     PLANTA 3: LÓGICA (Domain)        │
         │   ┌────────┐ ┌────────┐             │
         │   │UseCase1│ │UseCase2│             │
         │   └───┬────┘ └────┬───┘             │
         └───────┼───────────┼─────────────────┘
                 │           │
                 ▼           ▼
         ┌─────────────────────────────────────┐
         │    PLANTA 2: CONTRATOS (Repository) │
         │        ┌──────────────┐             │
         │        │   Interface  │             │
         │        └──────┬───────┘             │
         └───────────────┼─────────────────────┘
                         │
                         ▼
         ┌─────────────────────────────────────┐
         │      PLANTA 1: DATOS (Data)          │
         │  ┌──────────┐ ┌──────────┐          │
         │  │DataSource│ │   Model  │          │
         │  └──────────┘ └──────────┘          │
         └─────────────────────────────────────┘
```

**Regla de Oro**: Código de plantas superiores NUNCA conoce detalles de plantas inferiores.

### ¿Por qué usar Clean Architecture?

- **Independencia del Framework:** El núcleo de tu lógica de negocio no depende de Flutter.
- **Testabilidad:** Cada capa se puede probar de forma aislada.
- **Escalabilidad y Mantenimiento:** Fácil añadir features o cambiar implementaciones.
- **Organización:** Código claramente organizado por funcionalidad y capa.

### El Problema: Código Espagueti

Imagina un plato de espagueti donde todo está mezclado:
- UI con lógica de negocio
- Llamadas HTTP en los widgets
- Base de datos acoplada a la interfaz
- Imposible de testear
- Un cambio rompe todo

---
