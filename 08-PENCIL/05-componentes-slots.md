# Componentes y Slots

> Aprende a crear componentes reutilizables con slots flexibles. Los componentes son la base de cualquier sistema de diseño: editas una vez, se actualiza en todas las instancias.

---

## Índice

- [¿Qué son los Componentes?](#qué-son-los-componentes)
- [Crear Componentes](#crear-componentes)
- [Origen vs Instancia](#origen-vs-instancia)
- [Operaciones con Componentes](#operaciones-con-componentes)
- [Componentes Anidados](#componentes-anidados)
- [Slots](#slots)
- [Suggested Slot Components](#suggested-slot-components)
- [Mini-práctica](#mini-práctica)

---

## ¿Qué son los Componentes?

Un componente es un elemento (o grupo de elementos) que puede reutilizarse múltiples veces. Cuando editas el **origen**, todas las **instancias** se actualizan automáticamente.

**Analogía:** Si el origen es el "sello" (😊), cada instancia es una "estampada" en diferentes partes del papel. Si cambias la cara del sello, todas las estampadas cambian.

### Cuándo usar componentes

- Botones que aparecen en múltiples pantallas
- Cards de producto, perfil, artículo
- Ítems de lista, filas de tabla
- Inputs, selects, checkboxes
- Cualquier elemento que se repita 2+ veces

---

## Crear Componentes

### Método 1: Desde el Canvas

1. Selecciona el elemento o grupo que quieras convertir
2. Presiona `Cmd/Ctrl + Option/Alt + K`
3. El borde del elemento se vuelve **magenta** → ahora es un componente origen

### Método 2: Desde el Properties Panel

1. Selecciona el elemento
2. En la parte superior del Properties Panel, haz clic en **"Create component"**
3. Se convierte en componente

### Identificadores Visuales

| Bounding box | Significa |
|---|---|
| **Azul** | Elemento normal (no es componente) |
| **Magenta** | Origen del componente (fuente de verdad) |
| **Violeta** | Instancia del componente (copia vinculada) |

---

## Origen vs Instancia

### Origen (Magenta)

- Es la **fuente de verdad** del componente
- Solo debe haber **uno** por componente
- Los cambios hechos aquí se propagan a todas las instancias
- Se marca con borde magenta al seleccionarlo

### Instancia (Violeta)

- Es una **copia vinculada** del origen
- Puedes tener **muchas** instancias
- Refleja automáticamente los cambios del origen
- Se marca con borde violeta al seleccionarla

### Propiedades Override

Las instancias permiten **sobrescribir** propiedades específicas sin romper el vínculo:

- Puedes cambiar el texto de una instancia sin afectar a otras
- Puedes cambiar colores, imágenes o contenido de slots
- Lo que NO puedes cambiar: estructura, número de elementos, layout

**Ejemplo:** Un componente "Card de Producto" puede tener 10 instancias con diferentes imágenes, títulos y precios. Pero si añades un badge al origen, todas las instancias lo muestran.

### Detach (Desvincular)

Si necesitas que una instancia deje de estar vinculada:

1. Selecciona la instancia
2. Presiona `Cmd/Ctrl + Option/Alt + X`
3. La instancia se convierte en un grupo normal (sin vínculo al origen)

**Advertencia:** Esta operación no se puede deshacer fácilmente. Úsala solo cuando estés seguro.

---

## Operaciones con Componentes

### Duplicar un Componente

Para crear una instancia:
1. Selecciona el origen
2. Presiona `Cmd/Ctrl + D`
3. Arrastra la instancia a su lugar

O también: selecciona el origen → `Cmd/Ctrl + C` → `Cmd/Ctrl + V`

### Navegar al Origen

Si seleccionas una instancia y quieres ir al origen:
1. Selecciona la instancia (borde violeta)
2. En el Properties Panel, haz clic en **"Go to component"**
3. El canvas se centra en el origen

### Revertir Componente a Elemento

Si ya no necesitas que algo sea un componente:
1. Selecciona el **origen**
2. Presiona `Cmd/Ctrl + Option/Alt + K`
3. Se convierte de vuelta a grupo normal

**Importante:** Esto también elimina todas las instancias vinculadas (se convierten en grupos sueltos).

---

## Componentes Anidados

Puedes tener un componente **dentro** de otro componente.

**Ejemplo:**
```
Card de Producto (componente)
├── Imagen (slot)
├── Info (grupo)
│   ├── Titulo (text)
│   ├── Precio (text)
│   └── Rating (componente) ← componente anidado
└── Botón Comprar (componente) ← componente anidado
```

**Cómo funciona:**
1. El Rating y el Botón Comprar son componentes independientes
2. Se insertan dentro de la Card de Producto
3. Si editas el Rating, se actualiza en todas las cards y en todos los lugares donde se use
4. Si editas la Card, el Rating anidado no se modifica

---

## Slots

Los slots son **áreas vacías** dentro de un componente donde puedes insertar elementos personalizados.

### Para qué sirven

- Hacer que un componente tenga partes **intercambiables**
- Separar la **estructura** del **contenido**
- Permitir que diseñadores juniors usen componentes complejos sin romper la estructura

### Crear un Slot

1. Crea un componente (o edita el origen de uno existente)
2. Dentro del origen, añade un **frame vacío** (sin hijos) en la posición donde quieras el slot
3. Selecciona ese frame vacío
4. En el Properties Panel, haz clic en **"Make a slot"**
5. El frame se marca con **líneas diagonales** indicando que es un slot

### Reglas de Slots

- Solo los **frames vacíos** pueden convertirse en slots
- Los slots solo existen dentro del **origen** del componente
- Un componente puede tener **múltiples slots**

### Usar un Slot

1. Crea una **instancia** del componente
2. Arrastra cualquier elemento (rectángulo, texto, imagen, otro componente) **dentro** del área marcada con diagonales
3. El elemento se coloca automáticamente en el slot
4. Cada instancia puede tener **diferente contenido** en el mismo slot

### Identificar Slots Visualmente

En el canvas, los slots se muestran con un patrón de **líneas diagonales** (////) dentro del área del slot. Esto facilita ver dónde puedes insertar contenido.

---

## Suggested Slot Components

Los **suggested slot components** son componentes recomendados para un slot específico.

### Para qué sirven

- Guiar a otros diseñadores sobre qué tipo de contenido va en cada slot
- Agilizar el diseño: en lugar de crear desde cero, arrastras un componente sugerido
- Mantener consistencia: todos usan el mismo componente para el mismo tipo de slot

### Crear Suggested Slot Components

1. En el **origen** del componente, selecciona el frame que tiene el slot
2. En el Properties Panel, busca la línea "Slots" en la parte superior
3. Haz clic en el **+** de "Suggested slot components"
4. Selecciona los componentes que quieras sugerir

**Ejemplo:**
- Un componente `Table` tiene un slot para filas
- Marcas `Table Row` como suggested slot component
- Cuando alguien usa `Table`, sabe que debe insertar `Table Row` en ese slot

### Usar Suggested Components

Cuando un slot tiene suggested components:
1. El slot muestra una lista de componentes recomendados
2. Puedes arrastrar uno directamente al slot
3. Se crea automáticamente una instancia del componente sugerido dentro del slot

---

## Mini-práctica

### Ejercicio 1: Crear un Componente Botón

1. Presiona `R`, dibuja un rectángulo de 160×44
2. Fill: `#3B82F6`, Corner Radius: 8px
3. Presiona `T`, escribe "Click Me", color blanco, centrado
4. Agrupa el rectángulo + texto (`Cmd/Ctrl + G`)
5. Con el grupo seleccionado, presiona `Cmd/Ctrl + Option/Alt + K`
6. El borde se vuelve **magenta** → es un componente
7. Crea 3 instancias (`Cmd/Ctrl + D` tres veces)
8. Cambia el texto de cada instancia: "Comprar", "Eliminar", "Guardar"
9. Selecciona el origen y cambia su Fill a `#10B981`
10. Todas las instancias cambian de color automáticamente

### Ejercicio 2: Detach una Instancia

1. Selecciona una de las instancias (borde violeta)
2. Presiona `Cmd/Ctrl + Option/Alt + X`
3. El borde se vuelve azul → ahora es un grupo suelto
4. Cambia su Fill a `#EF4444`
5. Verifica que las otras instancias NO cambiaron

### Ejercicio 3: Crear un Slot

1. Crea un componente "Card" con:
   - Un rectángulo base de 240×320 (blanco, sombra)
   - Un frame vacío de 240×180 en la parte superior
   - Texto "Título" y Texto "$99.99" debajo
2. Selecciona el frame vacío de 240×180 (dentro del origen)
3. Haz clic en **"Make a slot"**
4. Verás líneas diagonales en esa área
5. Crea una instancia de la Card
6. Arrastra un rectángulo de color dentro del slot (las diagonales)
7. El rectángulo se coloca automáticamente en el slot

### Ejercicio 4: Componentes Anidados

1. Crea un componente "Badge" (rectángulo pequeño rojo + texto "NUEVO")
2. Selecciona el origen de Badge y cópialo (`Cmd/Ctrl + C`)
3. Edita el origen de "Card" del ejercicio anterior
4. Pega Badge dentro de la Card, en la esquina superior derecha
5. Ahora todas las instancias de Card tienen el Badge
6. Cambia el texto del Badge a "30% OFF" y todas las instancias se actualizan

### Ejercicio 5: Suggested Slot Components

1. Crea un componente "Item Lista" (rectángulo de 300×48 + texto, conviértelo a componente)
2. Crea un componente "Lista" (rectángulo de 300×300 como contenedor)
3. Dentro del origen de "Lista", añade un frame vacío de 300×250 y hazlo **slot**
4. En el Properties Panel del slot, haz clic en **+** en "Suggested slot components"
5. Selecciona "Item Lista"
6. Crea una instancia de "Lista"
7. El slot ahora sugiere "Item Lista" como contenido recomendado

---

## Checklist

- [ ] Creo componentes con `Cmd/Ctrl + Option/Alt + K`
- [ ] Distingo origen (magenta) de instancia (violeta)
- [ ] Duplico componentes para crear instancias
- [ ] Sobrescribo propiedades (texto, colores) en instancias
- [ ] Voy al origen desde una instancia con "Go to component"
- [ ] Hago detach de una instancia con `Cmd/Ctrl + Option/Alt + X`
- [ ] Revierto un componente a elemento en el origen
- [ ] Creo componentes anidados
- [ ] Creo slots (make a slot) en componentes
- [ ] Inserto contenido en slots
- [ ] Defino suggested slot components
- [ ] Uso suggested components desde un slot

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

> 📖 **Siguiente:** [Code on Canvas, Libraries y Design↔Code](./06-code-libraries.md)
