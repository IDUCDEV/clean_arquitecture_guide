# Code on Canvas, Libraries y Design↔Code

> Aprende a insertar código dentro de tus diseños, crear bibliotecas de componentes reutilizables y mantener sincronizados el diseño y el código Flutter.

---

## Índice

- [Code on Canvas](#code-on-canvas)
- [Design Libraries (.lib.pen)](#design-libraries-libpen)
- [Assets Panel](#assets-panel)
- [Design ↔ Code](#design--code)
- [Mini-práctica](#mini-práctica)

---

## Code on Canvas

Code on Canvas te permite **insertar fragmentos de código** (Dart, Flutter widgets) como elementos visuales dentro del canvas.

### Para qué sirve

- Documentar qué componente de código corresponde a cada diseño
- Tener una referencia visual de los widgets mientras diseñas
- Facilitar la transición de diseño a implementación
- Compartir con otros desarrolladores el código esperado

### Insertar Código

1. En el toolbar, selecciona la opción de **Code** o usa el atajo correspondiente
2. Aparece un bloque de código en el canvas
3. Pega o escribe el código Dart/Flutter
4. El bloque se muestra como un elemento visual con sintaxis resaltada

### Elementos Visuales del Código

El bloque de código en el canvas:
- Tiene un fondo oscuro (similar a un editor de código)
- Muestra el texto con formato monoespaciado
- Se puede mover, redimensionar y posicionar como cualquier otro elemento
- Se puede agrupar con otros elementos de diseño

**Ejemplo:**
```
┌─────────────────────────────────────┐
│  class CustomButton extends         │
│  StatelessWidget {                  │
│    @override                        │
│    Widget build(BuildContext        │
│    context) {                       │
│      return ElevatedButton(         │
│        onPressed: () {},            │
│        child: Text('Click Me'),     │
│      );                             │
│    }                                │
│  }                                  │
└─────────────────────────────────────┘
```

---

## Design Libraries (.lib.pen)

Las design libraries son archivos especiales `.lib.pen` que contienen componentes reutilizables. Cuando importas una librería en otro archivo, puedes arrastrar sus componentes al canvas.

### ¿Por qué usar Librerías?

- **Compartir** componentes entre múltiples proyectos
- **Mantener consistencia** en equipos grandes
- **Actualizar** un componente una vez y que se refleje en todos los archivos que lo importan
- **Separar** el design system del diseño de pantallas específicas

### Crear una Design Library

1. Crea un archivo `.pen` con los componentes que quieras incluir
2. Asegúrate de que cada elemento reutilizable sea un **componente** (origen magenta)
3. En el Layers Panel, haz clic en el icono **"Libraries"** (junto a Layers)
4. En la parte inferior, haz clic en **"Turn this file into a library"**
5. El archivo se convierte automáticamente a `.lib.pen`

**Importante:** Una vez que marcas un archivo como librería, **no se puede deshacer**. El sufijo `.lib.pen` es permanente.

### Qué Componentes Poner en una Librería

| Componente | Ejemplos |
|---|---|
| Botones | Primary, Secondary, Outline, Ghost, Icon Button |
| Inputs | Text Field, Select, Checkbox, Toggle, Radio |
| Cards | Product Card, Profile Card, Stats Card |
| Navegación | Navbar, Tabs, Bottom Nav, Breadcrumbs |
| Feedback | Alert, Badge, Chip, Toast, Modal |
| Data Display | Avatar, Progress Bar, Rating, Skeleton |

### Importar una Librería en Otro Archivo

1. Abre el archivo `.pen` donde quieras usar los componentes
2. En el Layers Panel, haz clic en el icono **"Libraries"**
3. Verás una lista de librerías disponibles
4. Selecciona la que quieras importar

**Librerías por defecto:**
Pencil incluye librerías de iconos preinstaladas:
- Material Symbols (Outlined, Rounded, Sharp)
- Lucide Icons
- Feather Icons
- Phosphor Icons

---

## Assets Panel

El Assets Panel aparece una vez que tienes librerías importadas.

### Abrir Assets

1. En el Layers Panel, haz clic en **"Assets"** (junto a Layers y Libraries)
2. Se muestra una cuadrícula con todos los componentes disponibles

### Usar Assets

1. Busca un componente por nombre en la barra de búsqueda
2. Desplázate por la cuadrícula para explorar
3. **Arrastra** un componente desde la cuadrícula al canvas
4. Se crea una **instancia** (violeta) del componente en el canvas

### Sincronización con la Librería

- Si modificas un componente en el archivo `.lib.pen`, los cambios se reflejan en todos los archivos que lo importan
- No necesitas re-importar ni recargar — los cambios son automáticos mientras el archivo `.lib.pen` esté abierto

---

## Design ↔ Code

Pencil permite una sincronización bidireccional entre diseño y código.

### Exportar Diseño a Código Flutter

1. Selecciona el elemento o frame que quieras convertir
2. Presiona `Cmd/Ctrl + K` para abrir el chat
3. Pide: "Generate Flutter widget code for this selection"
4. Recibirás un widget de Flutter con:
   - Estructura de widgets
   - Colores y estilos aplicados
   - Layout (Row, Column, Stack según corresponda)

**Ejemplo de output:**
```dart
Container(
  width: 160,
  height: 44,
  decoration: BoxDecoration(
    color: Color(0xFF3B82F6),
    borderRadius: BorderRadius.circular(8),
  ),
  child: Center(
    child: Text(
      'Click Me',
      style: TextStyle(
        color: Colors.white,
        fontWeight: FontWeight.w600,
        fontSize: 14,
      ),
    ),
  ),
)
```

### Exportar Variables a ThemeData

1. Abre el chat (`Cmd/Ctrl + K`)
2. Pide: "Generate Flutter ThemeData from my variables"
3. Obtienes un `ThemeData` completo con `colorScheme`, `textTheme`, etc.

### Sincronización Manual

Para mantener diseño y código sincronizados manualmente:

1. Define variables en Pencil
2. Exporta a Flutter ThemeData
3. Cuando cambien los requisitos de diseño:
   - Cambia las variables en Pencil
   - Re-exporta el ThemeData
   - Actualiza en tu código Flutter

---

## Mini-práctica

### Ejercicio 1: Insertar Código en el Canvas

1. Abre Pencil con un archivo nuevo
2. Usa la opción de **Code on Canvas** para insertar un bloque de código
3. Pega este snippet de Flutter:
   ```dart
   ElevatedButton(
     onPressed: () {},
     style: ElevatedButton.styleFrom(
       backgroundColor: Colors.blue,
       padding: EdgeInsets.symmetric(
         horizontal: 24, vertical: 12,
       ),
     ),
     child: Text('Iniciar Sesión'),
   )
   ```
4. Mueve el bloque de código junto a tu diseño de referencia
5. Agrupa el código con el diseño al que pertenece

### Ejercicio 2: Crear una Design Library

1. Presiona `R`, dibuja un rectángulo de 160×44
2. Fill: `#3B82F6`, Corner Radius: 8px
3. Presiona `T`, escribe "Botón", conviértelo a componente (`Cmd/Ctrl + Option/Alt + K`)
4. Presiona `R`, dibuja otro rectángulo de 320×44
5. Fill: blanco, Stroke: 1px, Corner Radius: 8px, nómbralo "Input"
6. Conviértelo a componente
7. En Layers Panel → **Libraries** → **"Turn this file into a library"**
8. El archivo se convierte en `.lib.pen`

### Ejercicio 3: Importar Librería en Otro Archivo

1. Crea un nuevo archivo `.pen`
2. En Layers Panel → **Libraries**
3. Selecciona la librería que acabas de crear
4. Cambia a **Assets**
5. Verás "Botón" e "Input" en la cuadrícula
6. Arrastra "Botón" al canvas — se crea una instancia (violeta)
7. Arrastra "Input" al canvas

### Ejercicio 4: Probar Sincronización

1. Vuelve al archivo `.lib.pen`
2. Selecciona el origen del componente "Botón"
3. Cambia su Fill a `#10B981` (verde)
4. Guarda (`Cmd/Ctrl + S`)
5. Vuelve al otro archivo
6. La instancia del botón ahora es verde — se actualizó automáticamente

### Ejercicio 5: Exportar un Frame a Código

1. En el archivo de práctica, diseña algo simple: un frame con un texto y un botón
2. Presiona `Cmd/Ctrl + K`
3. Escribe: "Generate Flutter code for the selected frame"
4. Revisa el código generado
5. Pide: "Generate a Flutter ThemeData from this file's variables"

---

## Checklist

- [ ] Inserto bloques de código Dart/Flutter en el canvas
- [ ] Creo una design library desde un archivo `.pen`
- [ ] Entiendo que `.lib.pen` es permanente
- [ ] Importo una librería en otro archivo
- [ ] Uso el Assets Panel para arrastrar componentes al canvas
- [ ] Modifico un componente en la librería y veo cambios reflejados
- [ ] Exporto diseño a código Flutter
- [ ] Exporto variables a Flutter ThemeData

---

**Siguiente:** [Import y Export](./07-import-export.md)
