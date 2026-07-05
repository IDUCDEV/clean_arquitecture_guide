# Layers Panel

> Domina el panel de capas: la columna vertebral de la organización de tus diseños. Aprenderás a estructurar, renombrar, ordenar, ocultar y bloquear elementos en diseños complejos.

---

## Índice

- [¿Qué es el Layers Panel?](#qué-es-el-layers-panel)
- [Jerarquía de Capas](#jerarquía-de-capas)
- [Operaciones Básicas](#operaciones-básicas)
- [Páginas](#páginas)
- [Buenas Prácticas de Organización](#buenas-prácticas-de-organización)
- [Mini-práctica](#mini-práctica)

---

## ¿Qué es el Layers Panel?

El Layers Panel está en el **lado izquierdo** del editor. Muestra cada elemento del canvas en una lista jerárquica.

**Para qué sirve:**
- Ver la estructura completa del diseño de un vistazo
- Seleccionar elementos que son difíciles de clickear en el canvas
- Renombrar, reordenar, ocultar y bloquear capas
- Navegar por diseños con muchos elementos anidados

```
Layers Panel
┌──────────────────────────┐
│ Layers  [Libraries] [Assets] │
├──────────────────────────┤
│ ▶ Page 1                 │
│   ├── ▼ iPhone Frame     │
│   │   ├── Header         │
│   │   │   ├── Logo       │
│   │   │   └── Menu Icon  │
│   │   ├── Hero Image     │
│   │   └── Footer         │
│   └── Desktop Frame      │
│       ├── Sidebar        │
│       └── Main Content   │
├──────────────────────────┤
│          [+] Page        │
└──────────────────────────┘
```

---

## Jerarquía de Capas

Las capas siguen el orden en que fueron creadas. La **primera capa creada** está al fondo; la **última** está al frente.

```
Orden en Layers Panel        Orden visual en canvas
──────────────────────        ──────────────────────
Arriba (última capa)    →    Al frente
Abajo (primera capa)    →    Al fondo
```

Esto es equivalente al z-index en CSS.

### Anidamiento

Puedes tener capas dentro de capas:

- **Frames** contienen elementos hijos
- **Grupos** (`Cmd/Ctrl + G`) agrupan elementos sin cambiar su posición en el canvas
- Los hijos se muestran indentados debajo de su padre
- Puedes expandir (▶) y colapsar (▼) la jerarquía

---

## Operaciones Básicas

### Renombrar

1. Haz **doble clic** en el nombre de la capa
2. Escribe el nuevo nombre
3. Presiona Enter

**Convención de nombres:**
- Usa nombres descriptivos: "Header" en vez de "Rectangle 3"
- Prefijos para tipo: `Btn Primary`, `Card Producto`, `Input Email`
- Sufijos para estado: `Btn Hover`, `Btn Disabled`, `Input Error`

### Reordenar

- **Arrastra** una capa hacia arriba o abajo para cambiar su orden
- Puedes arrastrar capas **dentro** de un frame para anidarlas
- Puedes arrastrar capas **fuera** de un frame para desanidarlas

### Ocultar / Mostrar

Cada capa tiene un **icono de ojo** 👁 a la derecha:

- Clic en el ojo → oculta la capa (desaparece del canvas)
- Clic en el espacio vacío → la muestra de nuevo
- Útil para: trabajar en una sección sin distracciones, comparar variantes

### Bloquear / Desbloquear

Cada capa tiene un **icono de candado** 🔒:

- Clic en el candado → bloquea la capa (no se puede seleccionar ni mover)
- Clic de nuevo → desbloquea
- Útil para: fondos, elementos decorativos, guías que no quieres mover accidentalmente

### Seleccionar desde Layers Panel

Haz clic en cualquier capa del panel para seleccionarla en el canvas. Esto es especialmente útil cuando:

- Un elemento está oculto detrás de otro
- Un elemento es muy pequeño
- Quieres seleccionar el frame padre sin mover los hijos

### Eliminar

1. Selecciona la capa (en el panel o en el canvas)
2. Presiona `Delete` o `Backspace`

---

## Páginas

Pencil permite crear **múltiples páginas** dentro de un mismo archivo `.pen`.

**Para qué sirven:**
- Separar variantes de diseño (ej: "Home v1", "Home v2", "Home v3")
- Organizar por flujos (ej: "Login Flow", "Dashboard", "Settings")
- Separar diseño de documentación

**Crear página:**
1. En la parte inferior del Layers Panel, haz clic en **+ Page**
2. Escribe el nombre de la página
3. Aparecerá como una entrada independiente en el panel

**Cambiar de página:**
Haz clic en el nombre de la página en el Layers Panel para activarla.

Cada página tiene su propio canvas independiente. Lo que dibujes en una página no aparece en las otras.

---

## Buenas Prácticas de Organización

### Estructura Recomendada

```
Pages
├── Page 1: "Inicio"           ← Pantalla principal
│   └── iPhone 14 (frame)
│       ├── Fondo
│       ├── Header
│       │   ├── Logo
│       │   ├── Nav Links
│       │   └── Avatar
│       ├── Hero Section
│       │   ├── Hero Image
│       │   └── Hero Text
│       └── Footer
│           ├── Contacto
│           └── Redes
│
├── Page 2: "Login"            ← Otra pantalla
│   └── iPhone 14 (frame)
│       ├── Fondo
│       ├── Logo
│       ├── Formulario
│       ├── Botones
│       └── Links
│
└── Page 3: "Componentes"      ← Biblioteca de componentes
    └── (componentes sueltos, sin frame)
        ├── Btn Primary [component]
        ├── Input Text [component]
        └── Card [component]
```

### Reglas de oro

1. **Renombra todo** — no dejes nombres por defecto como "Rectangle 3"
2. **Agrupa por sección** — Header, Hero, Features, Footer
3. **Bloquea fondos** — para no moverlos accidentalmente
4. **Usa páginas** para variantes y documentación
5. **Colapsa** lo que no estés editando para no distraerte

---

## Mini-práctica

### Ejercicio 1: Crear Estructura de Capas

1. Abre Pencil con un archivo nuevo
2. Presiona `A`, crea un frame de 400×700, renómbralo a "Pantalla Principal"
3. Presiona `R`, dibuja un rectángulo que cubra todo el frame, nómbralo "Fondo"
4. Presiona `T`, escribe "Bienvenido", nómbralo "Titulo"
5. Presiona `R`, dibuja un rectángulo de 300×48, nómbralo "Boton Inicio"
6. Presiona `T`, escribe "Comenzar", colócalo sobre el botón

### Ejercicio 2: Organizar y Reordenar

1. En el Layers Panel, deberías tener algo como:
   ```
   Pantalla Principal
   ├── Fondo
   ├── Titulo
   ├── Boton Inicio
   └── "Comenzar" (texto suelto fuera del botón)
   ```
2. Arrastra el texto "Comenzar" **dentro** del frame `Boton Inicio` para anidarlo
3. Renombra el texto "Comenzar" a "Texto Boton"
4. Ahora debería verse:
   ```
   Pantalla Principal
   ├── Fondo
   ├── Titulo
   └── Boton Inicio
       └── Texto Boton
   ```

### Ejercicio 3: Ocultar y Bloquear

1. Haz clic en el **ojo** 👁 de "Titulo" — el título desaparece del canvas
2. Haz clic de nuevo — reaparece
3. Haz clic en el **candado** 🔒 de "Fondo" — ahora no puedes seleccionar el fondo en el canvas
4. Intenta seleccionar el fondo con el mouse — no podrás
5. Desbloquéalo

### Ejercicio 4: Trabajar con Páginas

1. En la parte inferior del Layers Panel, haz clic en **+ Page** y nómbrala "Dashboard"
2. Nota que el canvas está vacío — es una página nueva
3. Presiona `A`, crea un frame de 1440×900, nómbralo "Dashboard Desktop"
4. Vuelve a "Page 1" (renómbrala a "Inicio" con doble clic)
5. Alterna entre páginas para ver que cada una tiene contenido independiente

### Ejercicio 5: Selección desde el Panel

1. Crea un rectángulo pequeño dentro de uno más grande
2. Desde el canvas, intenta seleccionar el rectángulo pequeño
3. Ahora en el Layers Panel, haz clic directamente en el nombre de la capa pequeña
4. Nota que se selecciona fácilmente aunque esté dentro de otra capa

---

## Checklist

- [ ] Renombro capas con doble clic
- [ ] Reordeno capas arrastrando (dentro y fuera de frames)
- [ ] Oculto y muestro capas con el icono de ojo
- [ ] Bloqueo y desbloqueo capas con el candado
- [ ] Selecciono elementos desde el Layers Panel
- [ ] Creo y alterno entre páginas
- [ ] Organizo capas con estructura de árbol clara
- [ ] Anido texto dentro de botones y otros contenedores

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

> 📖 **Siguiente:** [Properties Panel](./03-properties-panel.md)
