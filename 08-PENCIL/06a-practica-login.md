# Práctica 1: Diseñar Pantalla de Login

> Tu primera práctica con Pencil: diseña una pantalla de login mobile completamente a mano. Sin prompts, sin IA. Solo mouse, teclado y paneles.

---

## Instrucciones

1. Abre Pencil (extensión o desktop)
2. Crea un archivo nuevo: `login.pen`
3. Sigue cada paso en orden
4. Al final tendrás una pantalla de login lista para exportar

**Tiempo estimado:** 20-30 minutos

---

## Enunciado

Diseña una pantalla de inicio de sesión para una app de delivery. Debe incluir:

- Logo de la empresa
- Título ("Iniciar Sesión")
- Campo de email
- Campo de contraseña (con toggle de visibilidad)
- Botón "Iniciar Sesión"
- Enlace "¿Olvidaste tu contraseña?"
- Enlace "Crear una cuenta"

---

## Paso a Paso

### ✏️ Paso 1: Crear el Frame

1. Presiona `A` (Frame tool)
2. Arrastra en el canvas para crear un frame de aproximadamente **390×844** (tamaño iPhone)
3. Con el frame seleccionado, ve al **Properties Panel** (derecha)
4. Ajusta el tamaño exacto: Width `390`, Height `844`
5. En el **Layers Panel** (izquierda), haz doble clic en el nombre y renómbralo a `Login Screen`

### ✏️ Paso 2: Fondo

1. Presiona `R` (Rectangle tool)
2. Dibuja un rectángulo que cubra todo el frame
3. En el **Properties Panel**, ajusta:
   - Width: `390`, Height: `844`
   - X: `0`, Y: `0`
   - **Fill:** Color blanco `#FFFFFF`
   - **Corner Radius:** `0`
4. En el **Layers Panel**, renómbralo a `Fondo`

### ✏️ Paso 3: Logo

1. Presiona `O` (Ellipse tool)
2. Mantén `Shift` mientras arrastras para crear un círculo perfecto: **80×80**
3. En el **Properties Panel**:
   - **Fill:** Color naranja `#F97316`
   - **Opacity:** `100%`
4. Presiona `T` (Text tool)
5. Escribe "D" dentro del círculo
6. En el **Properties Panel** del texto:
   - **Font:** Inter o San Francisco
   - **Size:** `36px`
   - **Weight:** Bold
   - **Color:** `#FFFFFF`
   - Alínea el texto al centro del círculo
7. Selecciona el círculo y el texto (`Shift + clic`)
8. Presiona `Cmd/Ctrl + G` para agruparlos
9. Renombra el grupo a `Logo` en el Layers Panel

### ✏️ Paso 4: Título

1. Presiona `T`
2. Escribe "Iniciar Sesión"
3. En el **Properties Panel**:
   - **Font:** Inter
   - **Size:** `24px`
   - **Weight:** Semibold
   - **Color:** `#1F2937`
4. Colócalo centrado debajo del logo: X `~95`, Y `~180`

### ✏️ Paso 5: Subtítulo

1. Presiona `T`
2. Escribe "Ingresa tus credenciales para continuar"
3. En el **Properties Panel**:
   - **Size:** `14px`
   - **Weight:** Regular
   - **Color:** `#6B7280`
4. Colócalo centrado debajo del título: Y `~215`

### ✏️ Paso 6: Campo de Email

1. Presiona `R`
2. Dibuja un rectángulo de **320×48**
3. En el **Properties Panel**:
   - **Fill:** `#F9FAFB`
   - **Stroke:** `1px`, color `#D1D5DB`
   - **Corner Radius:** `8px`
   - Posición: X `35`, Y `~270`
4. Presiona `T`, escribe "Correo electrónico"
5. **Size:** `14px`, **Color:** `#9CA3AF`
6. Coloca el texto dentro del rectángulo (X `~48`, Y `~285`)
7. Agrupa rectángulo + texto como `Campo Email`

### ✏️ Paso 7: Campo de Contraseña

1. Duplica el grupo `Campo Email`:
   - Selecciona el grupo, presiona `Cmd/Ctrl + D`
2. Coloca la copia debajo: Y `~340`
3. Edita el texto: cambia a "Contraseña"
4. Renombra el grupo a `Campo Contraseña`

### ✏️ Paso 8: Botón de Iniciar Sesión

1. Presiona `R`
2. Dibuja un rectángulo de **320×48**
3. En el **Properties Panel**:
   - **Fill:** Color primario `#3B82F6`
   - **Corner Radius:** `8px`
   - Posición: X `35`, Y `~420`
4. Presiona `T`, escribe "Iniciar Sesión"
5. **Size:** `16px`, **Weight:** Semibold, **Color:** `#FFFFFF`
6. Centra el texto sobre el botón
7. Agrupa como `Botón Iniciar Sesión`

### ✏️ Paso 9: Enlace "¿Olvidaste tu contraseña?"

1. Presiona `T`
2. Escribe "¿Olvidaste tu contraseña?"
3. En el **Properties Panel**:
   - **Size:** `13px`
   - **Color:** `#3B82F6` (mismo azul)
   - Alineación: centrado
4. Colócalo debajo del botón: Y `~490`

### ✏️ Paso 10: Enlace "Crear una cuenta"

1. Presiona `T`
2. Escribe "¿No tienes cuenta? **Crear una**"
3. En el **Properties Panel**:
   - **Size:** `13px`
   - **Color:** `#6B7280`
   - La palabra "Crear una" en azul `#3B82F6`
4. Colócalo al fondo: Y `~780`

### ✏️ Paso 11: Organizar Capas

Tu **Layers Panel** debería verse así:

```
Pages
└── Page 1
    └── Login Screen (frame 390×844)
        ├── Fondo
        ├── Logo
        │   ├── Círculo
        │   └── Texto "D"
        ├── Título "Iniciar Sesión"
        ├── Subtítulo "Ingresa tus..."
        ├── Campo Email
        │   ├── Input Rect
        │   └── Label "Correo electrónico"
        ├── Campo Contraseña
        │   ├── Input Rect
        │   └── Label "Contraseña"
        ├── Botón Iniciar Sesión
        │   ├── Botón Rect
        │   └── Texto "Iniciar Sesión"
        ├── Link "¿Olvidaste tu contraseña?"
        └── Link "Crear una cuenta"
```

1. Renombra cada capa con doble clic
2. Arrastra para ordenar si es necesario
3. Bloquea el `Fondo` (icono de candado) para no moverlo accidentalmente

### ✏️ Paso 12: Exportar

1. Selecciona el frame `Login Screen`
2. Ve al fondo del **Properties Panel**
3. Elige formato **PNG**
4. Haz clic en "Export layer"
5. Guarda como `login-pantalla.png`

---

## Desafíos Extra

Completa estos retos para reforzar lo aprendido:

- [ ] Cambia el color primario del botón a través de una **variable** (`$color-primary`)
- [ ] Añade un **efecto de sombra** al botón (Properties → Effects → + Shadow)
- [ ] Crea un **segundo frame** para "Registro" con campos nombre, email, contraseña
- [ ] Añade **iconos** de Material Symbols dentro de los campos (icono de email y candado)
- [ ] Duplica el frame y cambia el fondo a **dark mode** (fondo oscuro, texto claro)

---

## Lo que has practicado

| Herramienta/Panel | Lo usaste en |
|---|---|
| Frame tool (`A`) | Paso 1 |
| Rectangle tool (`R`) | Pasos 2, 6, 7, 8 |
| Ellipse tool (`O`) | Paso 3 |
| Text tool (`T`) | Pasos 3, 4, 5, 6, 9, 10 |
| Properties: Fill | Pasos 2, 3, 8 |
| Properties: Stroke | Pasos 6, 7 |
| Properties: Corner Radius | Pasos 6, 8 |
| Properties: Font/Size/Weight | Pasos 4, 5, 8, 9, 10 |
| Group (`Cmd+G`) | Pasos 3, 6, 7, 8 |
| Layers Panel | Paso 11 |
| Export | Paso 12 |

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

> 📖 **Siguiente:** [Práctica 2: Dashboard de Ventas](./06b-practica-dashboard.md)
