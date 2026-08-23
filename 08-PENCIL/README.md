# 08 - Pencil: Diseño Visual desde el IDE

> Domina Pencil, la herramienta de diseño vectorial que vive dentro de tu IDE — como Figma, pero sin salir del editor. Diseña con mouse y teclado, sin IA, sin prompts.

---

## 📋 Índice

| # | Archivo | Descripción |
|---|---------|-------------|
| 00 | [Introducción a las Plataformas](./00-introduccion-plataformas.md) | Extension vs Desktop vs CLI — cuál usar según tu flujo |
| 01 | [Canvas y Toolbar](./01-canvas-toolbar.md) | Canvas infinito, navegación, frames, herramientas de dibujo |
| 02 | [Layers Panel](./02-layers-panel.md) | Jerarquía, páginas, renombrar, ocultar, bloquear |
| 03 | [Properties Panel](./03-properties-panel.md) | Alignment, Flex, Fill, Stroke, Corner Radius, Effects, Blend Modes |
| 04 | [Variables y Themes](./04-variables-themes.md) | Design tokens, temas Light/Dark, importar CSS, exportar a Flutter |
| 05 | [Componentes y Slots](./05-componentes-slots.md) | Crear componentes, slots, anidados, suggested slot components |
| 06 | [Code, Libraries y Design↔Code](./06-code-libraries.md) | Code on Canvas, .lib.pen, Assets Panel, exportar a widgets Flutter |
| 07 | [Import y Export](./07-import-export.md) | Importar Figma, imágenes, SVG, iconos; exportar a PNG/JPEG/WebP/PDF/código |
| 08 | [CLI y .pen Format](./08-cli-pen-format.md) | CLI interactivo, headless, agente, batch, CI/CD, Git diffs y merges |
| 09 | [Keyboard Shortcuts](./09-keyboard-shortcuts.md) | Referencia completa de atajos por categoría y frecuencia |
| 10 | [Pencil Desktop](./10-pencil-desktop.md) | App standalone, menú nativo, multi-ventana, paneles flotantes |

### Prácticas Integradoras

| Archivo | Descripción |
|---------|-------------|
| [Práctica: Login](./06a-practica-login.md) | Diseñar pantalla de Login desde cero |
| [Práctica: Dashboard](./06b-practica-dashboard.md) | Dashboard de Ventas con variables y flex layout |
| [Práctica: Design System](./06c-practica-design-system.md) | Sistema de Diseño — componente tarjeta, slots y librería |
| [Práctica: UI Components](./06d-practica-componentes-ui.md) | Biblioteca de componentes UI estándar |

---

## 📖 Descripción

Este módulo te enseña a usar **Pencil** como herramienta de diseño manual, sin depender de inteligencia artificial. Cubre las **tres plataformas** de Pencil:

| Plataforma | Estado | Dónde |
|---|---|---|
| **Extension** (VS Code / Cursor) | ✅ Completo | Teoría (archivos 01-07, 09) y prácticas |
| **Desktop** (standalone) | ✅ Completo | `10-pencil-desktop.md` + teoría aplica en 90% |
| **CLI** (terminal) | ✅ Completo | `08-cli-pen-format.md` |

### Cobertura por Práctica

| Práctica | Toolbar | Layers | Properties | Variables | Icons | Components | Slots | Libraries | Export |
|---|---|---|---|---|---|---|---|---|---|
| Login | ✅ | ✅ | ✅ | — | — | — | — | — | PNG |
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | — | — | — | PNG |
| Design System | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | PDF |
| UI Components | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — |

> **Filosofía:** No necesitas IA para diseñar. Pencil tiene un editor visual completo. El AI chat es opcional.

---

## 🚀 Orden de Aprendizaje Recomendado

```
1. 00-introduccion-plataformas.md   (elige tu plataforma)
2. 01-canvas-toolbar.md             (lo básico)
3. 02-layers-panel.md               (organización)
4. 06a-practica-login.md            (primera práctica)
5. 03-properties-panel.md           (estilos)
6. 04-variables-themes.md           (design tokens)
7. 06b-practica-dashboard.md        (segunda práctica)
8. 05-componentes-slots.md          (componentes)
9. 06c-practica-design-system.md    (tercera práctica)
10. 06-code-libraries.md            (liberías y código)
11. 06d-practica-componentes-ui.md  (cuarta práctica)
12. 07-import-export.md             (importar/exportar)
13. 08-cli-pen-format.md            (CLI y automatización)
14. 09-keyboard-shortcuts.md        (referencia de atajos)
15. 10-pencil-desktop.md            (Desktop cuando lo necesites)
```

> **Nota:** `10-pencil-desktop.md` puede leerse en cualquier momento. Si ya usas Desktop, léelo al principio después del archivo 00.

---

## 🔗 Siguiente paso

Después de este módulo, regresa a [02-SPEC-DRIVEN-DEVELOPMENT](../02-SPEC-DRIVEN-DEVELOPMENT/) para conectar el diseño visual con las especificaciones del cambio (SDD), o continúa con [01-CLEAN-ARCHITECTURE](../01-CLEAN-ARCHITECTURE/) para implementar en código.

---

**Nivel:** Principiante  
**Tiempo estimado:** 6-8 horas (incluyendo las 4 prácticas)  
**Herramientas:** [Pencil](https://pencil.dev), mouse, teclado
