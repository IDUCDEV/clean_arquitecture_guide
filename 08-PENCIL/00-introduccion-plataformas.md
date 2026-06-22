# Introducción a las Plataformas de Pencil

> Pencil no es solo una extensión de VS Code: es un ecosistema de diseño con tres plataformas que se complementan. Este archivo te explica cuál es cuál, para qué sirve cada una y cómo elegir según tu flujo de trabajo.

---

## Índice

- [Las Tres Plataformas](#las-tres-plataformas)
- [Tabla Comparativa](#tabla-comparativa)
- [Flujo de Trabajo Recomendado](#flujo-de-trabajo-recomendado)
- [Cómo Usar Este Módulo Según tu Plataforma](#cómo-usar-este-módulo-según-tu-plataforma)

---

## Las Tres Plataformas

### 1. Pencil Extension (VS Code / Cursor)

Es la extensión que se instala desde el **marketplace** del editor. El canvas de Pencil aparece como un panel o pestaña dentro del IDE.

**Para qué usarla:**
- Diseñar mientras desarrollas, sin cambiar de ventana
- Tener diseño y código lado a lado
- Aprovechar la integración con el sistema de archivos del IDE
- Conversión rápida diseño → Flutter widget

**Ventajas:**
- Cero cambio de contexto: diseñas y codeas en el mismo lugar
- Los atajos del IDE (`Cmd/Ctrl + S`, `Cmd/Ctrl + P`, etc.) funcionan igual
- El archivo `.pen` se guarda automáticamente con el proyecto
- Acceso directo al terminal y al explorador de archivos

**Limitaciones:**
- Consume recursos del IDE (pestaña, memoria)
- Depende del editor: si cierras VS Code, se cierra Pencil
- No puedes tener dos ventanas de diseño independientes fácilmente

---

### 2. Pencil Desktop

Es la **aplicación standalone** que se instala como cualquier programa de escritorio. Tiene su propia ventana, menú nativo y no depende de ningún editor.

**Para qué usarla:**
- Sesiones de diseño dedicadas (como usar Figma o Sketch)
- Trabajar con múltiples monitores o ventanas
- Cuando no necesitas el código al mismo tiempo
- Tener Pencil abierto siempre, incluso sin un proyecto de código abierto

**Ventajas:**
- Independiente del IDE: no consume recursos del editor
- Menú nativo del sistema operativo (File, Edit, View...)
- Múltiples ventanas: puedes tener varios diseños abiertos
- Ideal para diseñadores que no usan VS Code
- Se conecta al CLI para previsualización en vivo

**Limitaciones:**
- No tienes el código al lado (tienes que cambiar de ventana)
- No integración directa con el explorador de archivos del proyecto
- Requiere descarga e instalación separada

---

### 3. Pencil CLI

Es la **herramienta de terminal** que se instala vía npm. No tiene interfaz gráfica: se opera con comandos.

**Para qué usarla:**
- Automatización y scripting
- CI/CD pipelines (generar diseños en builds)
- Batch processing (procesar múltiples archivos)
- Git hooks (validar cambios en `.pen` antes de commitear)
- Edición programática de archivos `.pen`

**Ventajas:**
- Headless: funciona sin interfaz gráfica (ideal para servidores)
- Scripteable: puedes integrarlo en cualquier pipeline
- Conectable: se engancha a Desktop o Extension para previsualización en vivo
- Liviano: solo requiere Node.js 18+

**Limitaciones:**
- No tiene canvas visual (no puedes "ver" el diseño)
- Curva de aprendizaje: hay que saber los comandos MCP
- No reemplaza al diseñador humano para trabajo creativo

---

## Tabla Comparativa

| Característica | Extension | Desktop | CLI |
|---|---|---|---|
| **Instalación** | Marketplace VS Code | pencil.dev (download) | `npm install -g @pencil.dev/cli` |
| **Interfaz** | Panel dentro del IDE | Ventana nativa independiente | Terminal (sin GUI) |
| **Canvas visual** | ✅ | ✅ | ❌ (headless) |
| **Menú nativo OS** | ❌ (usa el de VS Code) | ✅ (File, Edit, View...) | ❌ |
| **Multi-ventana** | Limitado | ✅ | N/A |
| **Integración con código** | ✅ (lado a lado) | ❌ (ventana aparte) | ❌ |
| **Integración con Git** | ✅ (a través del IDE) | ✅ (file system) | ✅ (scripts) |
| **CI/CD** | ❌ | ❌ | ✅ |
| **Previsualización en vivo** | ✅ | ✅ (vía CLI) | ✅ (vía --attach) |
| **Exportación** | PNG, JPEG, WebP, PDF, código | PNG, JPEG, WebP, PDF, código | PNG, JPEG, WebP, PDF |
| **Atajos de teclado** | Mezcla IDE + Pencil | Pencil puro | Comandos de texto |

---

## Flujo de Trabajo Recomendado

### Perfil "Desarrollador Flutter" (el tuyo)

```
Extension (diseño + código lado a lado)
    ↓
CLI (automatizar exportaciones, validar en CI/CD)
    ↓
Desktop (sesiones de diseño largas o multi-monitor)
```

1. **Día a día**: Extension — diseñas mientras codeas, conviertes diseño a widget al instante
2. **Automatización**: CLI — exportas todas las pantallas a PNG para documentación, o validas cambios en pre-commit
3. **Sesiones dedicadas**: Desktop — cuando necesitas concentrarte solo en diseño, o trabajar con dos archivos `.pen` abiertos simultáneamente

### Perfil "Diseñador UI"
```
Desktop (diseño principal)
    ↓
CLI (exportación batch a PDF/PNG)
```

### Perfil "DevOps / CI"
```
CLI (generación y exportación automatizada)
```

---

## Cómo Usar Este Módulo Según tu Plataforma

| Archivo | Extension | Desktop | CLI |
|---|---|---|---|
| 01-canvas-toolbar.md | ✅ Usa los paneles del IDE | ✅ Similar, menú nativo | — (no aplica) |
| 02-layers-panel.md | ✅ Panel en sidebar | ✅ Panel en ventana propia | — |
| 03-properties-panel.md | ✅ Panel en sidebar | ✅ Panel en ventana propia | — |
| 04-variables-themes.md | ✅ | ✅ | — |
| 05-componentes-slots.md | ✅ | ✅ | — |
| 06-code-libraries.md | ✅ | ✅ | — |
| 07-import-export.md | ✅ | ✅ (menú nativo) | ✅ (desde CLI) |
| 08-cli-pen-format.md | — | — (referencia) | ✅ |
| 09-keyboard-shortcuts.md | ✅ (ver notas) | ✅ | — |
| 10-pencil-desktop.md | — | ✅ | — |

> **Conclusión:** El 90% de la teoría aplica igual en Extension y Desktop. Donde hay diferencias, se indican explícitamente. El CLI es un mundo aparte que se cubre en su propio archivo.

---

**Siguiente:** [Canvas y Toolbar](./01-canvas-toolbar.md) — Empieza a diseñar desde cero.
