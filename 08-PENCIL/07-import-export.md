# Import y Export

> Aprende a importar archivos de Figma, imágenes, SVG e iconos a Pencil, y a exportar tus diseños como PNG, JPEG, WebP, PDF y código Flutter.

---

## Índice

- [Importar desde Figma](#importar-desde-figma)
- [Importar Imágenes y SVGs](#importar-imágenes-y-svgs)
- [Iconos Incorporados](#iconos-incorporados)
- [Exportar Elementos](#exportar-elementos)
- [Exportar a Código](#exportar-a-código)
- [Mini-práctica](#mini-práctica)

---

## Importar desde Figma

Pencil permite importar diseños existentes de Figma de dos formas:

### Archivo Figma Completo

Importa un archivo `.fig` completo con todas sus capas.

**Cómo hacerlo:**

1. En la **Toolbar**, haz clic en el chevron (▼) debajo del icono de Rectangle
2. Selecciona **"Import Figma"**
3. Busca y selecciona tu archivo `.fig`
4. Pencil importa todas las capas manteniendo la jerarquía

**Alternativa (Desktop App):**
1. Ve a **File** → **Import Image/SVG/Figma...**
2. Selecciona el archivo `.fig`

### Capas Individuales de Figma

Para importar solo elementos específicos desde Figma:

1. En Figma, selecciona las capas que quieras
2. Cópialas (`Cmd/Ctrl + C`)
3. En Pencil, pégalas (`Cmd/Ctrl + V`)

**Limitación:** Copiar y pegar elementos **image** desde Figma no está soportado. Para imágenes, impórtalas manualmente.

### Qué se Importa

| Elemento Figma | ¿Se importa? |
|---|---|
| Rectángulos | ✅ |
| Texto | ✅ |
| Frames | ✅ |
| Grupos | ✅ |
| Componentes | ✅ (como componentes) |
| Imágenes | ❌ (solo como placeholder) |
| Efectos (sombras, blur) | ✅ |
| Gradientes | ✅ |
| Variables | ❌ |

---

## Importar Imágenes y SVGs

Pencil soporta tres formatos de imagen: **PNG**, **JPEG** y **SVG**.

### Métodos de Importación

| Método | Cómo |
|---|---|
| **Arrastrar y soltar** | Arrastra una imagen desde tu computadora al canvas |
| **Copiar y pegar** | Copia una imagen del explorador de archivos y pégala en Pencil |
| **Toolbar** | Chevron ▼ bajo Rectangle → **Import Image or SVG...** |
| **Menú (Desktop)** | **File** → **Import Image/SVG/Figma...** |

### Image Fill

También puedes usar imágenes como **relleno** de un elemento:

1. Selecciona un rectángulo en el canvas
2. En Properties Panel → **Fill**, cambia a **Image**
3. Arrastra la imagen o selecciona del disco
4. Ajusta el **fit**: Fill, Fit, Stretch, Tile

---

## Iconos Incorporados

Pencil incluye bibliotecas de iconos listas para usar. No necesitas descargar ni importar nada.

### Librerías de Iconos

| Librería | Estilos |
|---|---|
| **Material Symbols** | Outlined, Rounded, Sharp |
| **Lucide Icons** | Line style |
| **Feather Icons** | Line style |
| **Phosphor Icons** | Regular, Fill, Bold |

### Cómo Usarlos

1. Abre un archivo `.pen`
2. En el Layers Panel, haz clic en **Libraries**
3. Verás las librerías de iconos en la lista (vienen preinstaladas)
4. Importa la que necesites (ej: Material Symbols Rounded)
5. Cambia a **Assets**
6. Busca el icono por nombre (ej: "search", "home", "user")
7. Arrastra el icono al canvas

### Personalizar Iconos

Una vez que el icono está en el canvas:
- Cambia su **Fill** para modificar el color
- Redimensiona para cambiar el tamaño
- Aplica efectos como sombras

### Importar tus Propios SVGs

Si necesitas iconos que no están en las librerías preinstaladas:
1. Prepara tu archivo SVG
2. Arrástralo al canvas o usa **Import Image or SVG...**
3. Se comporta como cualquier otro elemento vectorial

---

## Exportar Elementos

Pencil exporta elementos seleccionados a formatos de imagen y documento.

### Formatos Soportados

| Formato | Cuándo usarlo |
|---|---|
| **PNG** | Exportaciones generales, alta calidad, con transparencia |
| **JPEG** | Fotos, sin transparencia, menor tamaño de archivo |
| **WebP** | Web, tamaño comprimido, calidad ajustable |
| **PDF** | Documentos para imprimir o compartir |

### Cómo Exportar

1. Selecciona el elemento o frame que quieras exportar
2. En el **Properties Panel**, ve al fondo (sección Export)
3. Configura:
   - **Tamaño:** 1x, 2x, 3x (para pantallas retina/HDPI)
   - **Formato:** PNG, JPEG, WebP, o PDF
4. Haz clic en **"Export layer"**
5. Elige la ubicación y guarda

### Buenas Prácticas de Exportación

- **1x** → Para uso web estándar (96 DPI)
- **2x** → Para pantallas retina (iPhone, iPad, Mac)
- **3x** → Para pantallas super retina (iPhone Pro, algunos Android)
- **PDF** → Para documentación, presentaciones, impresión

---

## Exportar a Código

Además de imágenes, Pencil puede exportar diseños directamente a **código Flutter**.

### Código de un Elemento

1. Selecciona el elemento
2. Presiona `Cmd/Ctrl + K`
3. Pide: "Generate Flutter code for this selection"
4. Recibirás un widget de Flutter con layout, colores y estilos

### Código del Archivo Completo

1. Presiona `Cmd/Ctrl + K`
2. Pide: "Generate Flutter code for the entire file"
3. Recibirás widgets para cada frame y pantalla

### Código de un Componente

Si el elemento es un componente:
1. Pide: "Generate a reusable Flutter widget for this component"
2. Obtienes un `StatelessWidget` con los parámetros correspondientes

---

## Mini-práctica

### Ejercicio 1: Importar una Imagen

1. Busca una imagen PNG o JPEG en tu computadora (puede ser un logo o foto)
2. Arrástrala directamente al canvas de Pencil
3. Rediménsionala usando los handles
4. En el Properties Panel, mira la sección Fill — ahora es un Image Fill
5. Cambia el fit entre Fill, Fit y Stretch para ver las diferencias

### Ejercicio 2: Usar Iconos de Material Symbols

1. En Layers Panel → **Libraries** → **Icon Libraries**
2. Importa "Material Symbols Rounded"
3. Cambia a **Assets**
4. Busca el icono "home" en la barra de búsqueda
5. Arrástralo al canvas
6. Busca "shopping_cart" y arrastra otro
7. Busca "person" y arrastra otro
8. Coloca los 3 iconos en fila
9. Cambia el Fill de cada uno a un color diferente

### Ejercicio 3: Exportar a PNG 2x

1. Crea un frame pequeño con algunos elementos (un rectángulo + texto)
2. Selecciona el frame
3. En Properties Panel → Export:
   - Formato: **PNG**
   - Tamaño: **2x** (para retina)
4. Haz clic en "Export layer"
5. Guarda como `ejemplo-2x.png`
6. Ábrelo y verifica que se ve nítido

### Ejercicio 4: Exportar a PDF

1. Crea un frame más grande con varios elementos
2. Selecciona el frame
3. En Export, cambia formato a **PDF**
4. Exporta y guarda
5. Abre el PDF — debería mostrar tu diseño en una sola página

### Ejercicio 5: Importar desde Figma

Si tienes acceso a Figma:
1. En Figma, selecciona un elemento o grupo
2. Cópialo (`Cmd/Ctrl + C`)
3. En Pencil, pégalo (`Cmd/Ctrl + V`)
4. Verifica que la estructura de capas se haya mantenido

**Si no tienes Figma:**
1. Descarga un archivo `.fig` de ejemplo
2. En Pencil, Toolbar → Chevron ▼ → **Import Figma**
3. Selecciona el archivo
4. Explora cómo se importaron las capas

---

## Checklist

- [ ] Importo archivos `.fig` completos de Figma
- [ ] Copio y pego capas individuales desde Figma
- [ ] Arrastro imágenes PNG, JPEG y SVG al canvas
- [ ] Uso imágenes como fill de un rectángulo
- [ ] Importo y uso iconos de Material Symbols, Lucide, Feather, Phosphor
- [ ] Busco iconos por nombre en Assets
- [ ] Exporto elementos a PNG (1x, 2x, 3x)
- [ ] Exporto a JPEG, WebP y PDF
- [ ] Genero código Flutter desde un diseño

---

**Siguiente:** [CLI y .pen Format](./08-cli-pen-format.md)
