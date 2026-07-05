# Pencil Desktop: La Aplicación Standalone

> Aprende a usar Pencil como aplicación de escritorio independiente: instalación, interfaz nativa, menús, ventanas múltiples y diferencias clave con la extensión del IDE.

---

## Índice

- [Instalación](#instalación)
- [Primer Inicio](#primer-inicio)
- [Interfaz de Usuario](#interfaz-de-usuario)
- [Menú Nativo](#menú-nativo)
- [Diferencias Clave con la Extensión](#diferencias-clave-con-la-extensión)
- [Multi-ventana](#multi-ventana)
- [CLI + Desktop: Previsualización en Vivo](#cli--desktop-previsualización-en-vivo)
- [Atajos de Teclado Específicos de Desktop](#atajos-de-teclado-específicos-de-desktop)
- [Cuándo Usar Desktop en Lugar de la Extensión](#cuándo-usar-desktop-en-lugar-de-la-extensión)
- [Mini-práctica](#mini-práctica)

---

## Instalación

### Descargar

1. Ve a [pencil.dev](https://pencil.dev)
2. Haz clic en **Download for Desktop**
3. Selecciona tu sistema operativo:
   - **macOS**: `Pencil.dmg` (Apple Silicon e Intel)
   - **Windows**: `Pencil Setup.exe`
   - **Linux**: `Pencil.AppImage` o `.deb` / `.rpm`

### Requisitos del Sistema

| SO | Versión Mínima |
|---|---|
| macOS | 12 Monterey o superior |
| Windows | 10 (build 19041+) |
| Linux | Ubuntu 20.04+, Fedora 38+, equivalentes |

### Instalación Rápida (macOS)

```bash
# Descargar y mover a Applications
mv ~/Downloads/Pencil.dmg /Applications/
```

### Instalación Rápida (Linux)

```bash
chmod +x Pencil.AppImage
./Pencil.AppImage
```

> **Nota:** Pencil Desktop y Pencil Extension son instalaciones independientes. Puedes tener ambas y usarlas según necesites.

---

## Primer Inicio

Al abrir Pencil Desktop por primera vez verás:

1. **Pantalla de bienvenida** con opciones para:
   - Nuevo archivo (`Cmd/Ctrl + N`)
   - Abrir archivo existente (`Cmd/Ctrl + O`)
   - Abrir un ejemplo
2. **Sin proyecto de código asociado**: No hay un `pubspec.yaml` ni un folder de proyecto. El archivo `.pen` vive donde tú decidas guardarlo.

---

## Interfaz de Usuario

### Layout de la Ventana

```
┌─────────────────────────────────────────────────────┐
│  Pencil  File  Edit  View  Help                     │  ← Menú nativo
├──────────┬──────────────────────────┬───────────────┤
│ Toolbar  │                         │  Properties   │
│ ┌──────┐ │       Canvas            │  Panel        │
│ │  R   │ │       (infinito)        │               │
│ │  T   │ │                         │               │
│ │  A   │ │    ┌──────────┐         │  Fill         │
│ │  O   │ │    │ Frame    │         │  Stroke       │
│ └──────┘ │    │          │         │  Effects      │
│          │    └──────────┘         │               │
├──────────┤                         ├───────────────┤
│ Layers   │                         │  Variables    │
│ Panel    │                         │  Panel        │
└──────────┴─────────────────────────┴───────────────┘
```

### Diferencias Visuales vs Extensión

| Aspecto | Extension (VS Code) | Desktop |
|---|---|---|
| **Toolbar** | En la parte superior del canvas (dentro de la pestaña) | Igual, pero en ventana nativa |
| **Panels** | En la sidebar de VS Code (izquierda/derecha) | Paneles flotantes o acoplados a la ventana de Pencil |
| **Pestañas de archivos** | Usa las tabs de VS Code | Pestañas nativas en la ventana de Pencil |
| **Menú** | Menú de VS Code | Menú nativo del SO (File, Edit, View...) |
| **Variables Panel** | Panel separado en sidebar | Pestaña junto a Properties o flotante |

### Paneles Flotantes

En Desktop, puedes **desacoplar** cualquier panel:
1. Arrastra la pestaña del panel fuera de la ventana
2. Se convierte en una ventana flotante independiente
3. Puedes colocarla en otro monitor

Esto es útil para:
- Tener Layers Panel en un monitor y Properties en otro
- Dejar el canvas limpio en la ventana principal
- Organizar el espacio de trabajo a tu gusto

---

## Menú Nativo

El menú de Pencil Desktop sigue las convenciones del sistema operativo.

### File

| Opción | Atajo | Descripción |
|---|---|---|
| New | `Cmd/Ctrl + N` | Nuevo archivo `.pen` |
| Open... | `Cmd/Ctrl + O` | Abrir archivo `.pen` (navegador nativo) |
| Open Recent | — | Archivos recientes |
| Save | `Cmd/Ctrl + S` | Guardar (navegador nativo si es nuevo) |
| Save As... | `Cmd/Ctrl + Shift + S` | Guardar como |
| Import | — | Submenú: Image, SVG, Figma... |
| Export | — | Submenú: PNG, JPEG, WebP, PDF, Flutter code |
| Close | `Cmd/Ctrl + W` | Cerrar archivo actual |
| Quit | `Cmd/Ctrl + Q` | Cerrar la aplicación |

### Edit

| Opción | Atajo | Descripción |
|---|---|---|
| Undo | `Cmd/Ctrl + Z` | Deshacer |
| Redo | `Cmd/Ctrl + Shift + Z` | Rehacer |
| Cut | `Cmd/Ctrl + X` | Cortar |
| Copy | `Cmd/Ctrl + C` | Copiar |
| Paste | `Cmd/Ctrl + V` | Pegar |
| Duplicate | `Cmd/Ctrl + D` | Duplicar selección |
| Select All | `Cmd/Ctrl + A` | Seleccionar todo |

### View

| Opción | Descripción |
|---|---|
| Toggle Toolbar | Mostrar/ocultar la toolbar |
| Toggle Layers Panel | Mostrar/ocultar el panel de capas |
| Toggle Properties Panel | Mostrar/ocultar el panel de propiedades |
| Toggle Variables Panel | Mostrar/ocultar el panel de variables |
| Toggle Assets Panel | Mostrar/ocultar el panel de assets |
| Zoom In / Zoom Out / Zoom 100% | Control de zoom |
| Pixel Grid | Mostrar/ocultar cuadrícula |
| Dark Mode | Alternar tema oscuro/claro de la app |

### Help

| Opción | Descripción |
|---|---|
| About Pencil | Versión y créditos |
| Keyboard Shortcuts | Mostrar la referencia de atajos |
| Documentation | Abrir web de documentación |
| Check for Updates | Buscar actualizaciones |

---

## Diferencias Clave con la Extensión

### 1. Gestión de Archivos

| Aspecto | Extension | Desktop |
|---|---|---|
| **Donde se guarda** | En el proyecto abierto en VS Code | En cualquier ubicación del sistema |
| **Diálogo "Save As"** | Usa el de VS Code (explorador de archivos del IDE) | Usa el diálogo nativo del SO |
| **Archivos recientes** | Los del proyecto actual | Lista global del sistema |
| **Múltiples archivos** | Se abren como pestañas en VS Code | Se abren como pestañas en la ventana de Pencil (o ventanas separadas) |

### 2. Atajos de Teclado

En Desktop no hay interferencia con atajos de VS Code. Esto significa que:

| Atajo | Extension | Desktop |
|---|---|---|
| `Cmd/Ctrl + P` | Command Palette de VS Code | (no asignado en Pencil Desktop) |
| `Cmd/Ctrl + Shift + P` | Command Palette | (no asignado) |
| `Cmd/Ctrl + B` | Toggle sidebar | (no asignado) |
| `Cmd/Ctrl + \`` | Toggle terminal | (no asignado) |
| `Cmd/Ctrl + W` | Cerrar pestaña del editor | Cerrar archivo actual en Pencil |
| `Cmd/Ctrl + Q` | (no asignado por defecto) | **Cerrar Pencil** |

### 3. Integración con el Proyecto

| Aspecto | Extension | Desktop |
|---|---|---|
| **Assets del proyecto** | Acceso directo a la carpeta `assets/` del proyecto | No hay proyecto asociado |
| **pubspec.yaml** | Puede leer dependencias del proyecto | No aplica |
| **Flutter widgets** | Conversión directa a código en el proyecto | Exportas el código y lo pegas manualmente |

### 4. Rendimiento

| Aspecto | Extension | Desktop |
|---|---|---|
| **Memoria** | Comparte heap con VS Code | Heap propio |
| **CPU** | Compite con el editor y otros plugins | Recurso dedicado |
| **Diseños grandes** | Puede ralentizar el IDE | No afecta al editor |

---

## Multi-ventana

Pencil Desktop permite **múltiples ventanas independientes**.

### Abrir una Segunda Ventana

```
File → New Window
```
O atajo: `Cmd/Ctrl + Shift + N`

### Usos de Multi-ventana

- **Diseño + Referencia**: Un archivo `.pen` abierto en cada ventana, diseñas en una y consultas componentes en la otra
- **Monitor dual**: Canvas en el monitor principal, paneles en el secundario
- **Comparación**: Dos versiones del mismo diseño lado a lado (como split view en Figma)
- **Drag & drop entre ventanas**: Puedes arrastrar elementos de un archivo a otro

---

## CLI + Desktop: Previsualización en Vivo

El CLI puede conectarse a una instancia de Desktop que ya está corriendo. Los cambios hechos vía CLI se ven **en vivo** en el canvas de Desktop.

```bash
# Desde la terminal, conectar CLI a Desktop
pencil interactive -a desktop -i mi-diseno.pen
```

Esto es útil para:
- Scriptear cambios mientras ves el resultado en tiempo real
- Probar variaciones de diseño programáticamente
- Automatizar tareas repetitivas con confirmación visual

Para saber más, consulta [CLI y .pen Format](./08-cli-pen-format.md), sección "App Mode".

---

## Atajos de Teclado Específicos de Desktop

Estos atajos **solo aplican en Desktop** (en la extensión son capturados por VS Code o no existen):

| Atajo | Acción |
|---|---|
| `Cmd/Ctrl + Q` | Salir de Pencil |
| `Cmd/Ctrl + W` | Cerrar archivo actual |
| `Cmd/Ctrl + Shift + N` | Nueva ventana |
| `Cmd/Ctrl + ,` | Abrir preferencias |
| `F11` / `Cmd+Ctrl+F` | Pantalla completa |
| `Cmd/Ctrl + M` | Minimizar ventana (macOS) |

---

## Cuándo Usar Desktop en Lugar de la Extensión

### ✅ Usa Desktop cuando:

- **Solo quieres diseñar**, sin código alrededor
- **Tienes dos monitores**: Pencil en uno, VS Code en el otro
- **Necesitas dos archivos `.pen` abiertos** simultáneamente
- **El proyecto es muy grande** y no quieres ralentizar el IDE
- **Eres diseñador** y no usas VS Code
- **Quieres hacer una sesión de diseño larga** sin distracciones de código
- **Necesitas el menú nativo** (Export, Import, etc. desde File)

### ❌ Usa la Extension cuando:

- **Estás codeando y diseñando** al mismo tiempo
- **Necesitas conversión rápida diseño → Flutter widget**
- **Quieres que el archivo `.pen`** esté en el árbol del proyecto
- **No quieres cambiar de ventana**

### 🔄 Flujo mixto recomendado:

```
Mañana: Extension — codeas y ajustas diseños rápidos
Tarde: Desktop — sesión de diseño dedicada para nuevas pantallas
Siempre: CLI en CI/CD — exportación automática y validación
```

---

## Mini-práctica

### Ejercicio 1: Instalar y Primer Archivo

1. Descarga e instala Pencil Desktop desde [pencil.dev](https://pencil.dev)
2. Ábrelo
3. Crea un nuevo archivo: `Cmd/Ctrl + N`
4. Crea un frame (A) de 1440×900, nómbralo "Landing"
5. Guarda el archivo: `Cmd/Ctrl + S` → guárdalo en tu escritorio como `mi-primer-diseno.pen`
6. Observa que el diálogo de guardado es el **nativo del SO**, no el de VS Code

### Ejercicio 2: Menú Nativo

1. Ve a **File** → **Import** → **Image...**
2. Selecciona cualquier imagen PNG o JPEG de tu computadora
3. Observa que el navegador de archivos también es el nativo
4. La imagen aparece en el canvas
5. Ahora ve a **File** → **Export** → **PNG...**
6. Elige 2x y guarda la imagen exportada
7. Nota que el menú **View** permite mostrar/ocultar cada panel individualmente

### Ejercicio 3: Multi-ventana

1. `Cmd/Ctrl + Shift + N` para abrir una nueva ventana
2. En la primera ventana, abre (o crea) un archivo con un botón azul
3. En la segunda ventana, crea un archivo nuevo
4. Arrastra el botón azul desde la primera ventana al canvas de la segunda
5. El elemento se copia entre archivos
6. Cierra la segunda ventana con `Cmd/Ctrl + W`

### Ejercicio 4: Paneles Flotantes

1. Arrastra la pestaña **Layers** fuera de la ventana principal
2. Se convierte en una ventana flotante
3. Colócala a un lado (simula tener dos monitores)
4. Vuelve a acoplarla arrastrándola de vuelta a la ventana principal
5. Repite con el panel **Properties**

### Ejercicio 5: Comparación Extension vs Desktop

Si tienes Pencil Extension instalada:

1. Crea un frame rojo en Desktop, guarda como `comparacion.pen`
2. Abre VS Code, abre `comparacion.pen` desde el explorador de archivos
3. El archivo se abre en la Extension con el mismo frame rojo
4. Cambia el color a azul en la Extension y guarda
5. Vuelve a Desktop — el archivo se actualizó (el `.pen` es el mismo formato)
6. Conclusión: **Extension y Desktop comparten el mismo formato `.pen`**. Puedes alternar entre ambos sin problemas.

---

## Checklist

- [ ] Instalé Pencil Desktop desde pencil.dev
- [ ] Creé y guardé mi primer archivo con diálogo nativo
- [ ] Usé el menú File → Import para importar una imagen
- [ ] Usé el menú File → Export para exportar a PNG
- [ ] Usé File → New Window para abrir una segunda ventana
- [ ] Arrastré elementos entre ventanas
- [ ] Desacoplé y acoplé paneles flotantes
- [ ] Abrí el mismo `.pen` en Desktop y Extension (verifiqué compatibilidad)
- [ ] Diferencio cuándo usar Desktop vs Extension

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

**Anterior:** [Introducción a las Plataformas](./00-introduccion-plataformas.md)
> 📖 **Siguiente:** [Canvas y Toolbar](./01-canvas-toolbar.md)
