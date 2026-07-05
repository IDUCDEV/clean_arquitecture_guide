# 2. Widgets Básicos y Atomización

## Text

El widget más fundamental para mostrar texto.

```dart
const Text(
  'Hola Mundo',
  style: TextStyle(
    fontSize: 20,
    fontWeight: FontWeight.bold,
    color: Colors.blue,
  ),
  textAlign: TextAlign.center,
  maxLines: 2,
  overflow: TextOverflow.ellipsis,
);
```

Propiedades clave: `style`, `textAlign`, `maxLines`, `overflow`, `softWrap`.

## Icon

Íconos del set Material Design.

```dart
const Icon(Icons.favorite, color: Colors.red, size: 32);
```

Usa siempre `Icons.*`. Evita imágenes para íconos simples.

## Imagen

```dart
// Desde assets (declarada en pubspec.yaml)
Image.asset('assets/imagenes/logo.png');

// Desde red
Image.network('https://ejemplo.com/foto.jpg');

// Con placeholder y caché (requiere cached_network_image)
CachedNetworkImage(
  imageUrl: 'https://ejemplo.com/foto.jpg',
  placeholder: (_, __) => const CircularProgressIndicator(),
  errorWidget: (_, __, ___) => const Icon(Icons.error),
);
```

## SizedBox y Container

Contenedores para espaciado y decoración.

```dart
const SizedBox(height: 16);           // Espaciador simple
const SizedBox(width: 100, height: 100); // Caja de tamaño fijo

Container(
  width: 100,
  height: 100,
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8),
    boxShadow: [
      BoxShadow(color: Colors.black26, blurRadius: 4),
    ],
  ),
  child: const Text('Dentro'),
);
```

Prefiere `SizedBox` sobre `Container` cuando solo necesites espacio. `Container` es más pesado.

## Padding, Margin, Center, Align

Widgets de alineación y espaciado puro.

```dart
const Padding(
  padding: EdgeInsets.all(16),
  child: Text('Con padding'),
);

const Center(child: Text('Centrado'));

Align(
  alignment: Alignment.bottomRight,
  child: const Text('Esquina'),
);
```

## Botones

Cada version de Material Design tiene su familia de botones.

```dart
FilledButton(
  onPressed: () {},
  child: const Text('Relleno'),
);
FilledButton.tonal(
  onPressed: () {},
  child: const Text('Tonal'),
);
OutlinedButton(
  onPressed: () {},
  child: const Text('Outline'),
);
TextButton(
  onPressed: () {},
  child: const Text('Texto'),
);
```

Para botones con ícono:

```dart
FilledButton.icon(
  onPressed: () {},
  icon: const Icon(Icons.add),
  label: const Text('Agregar'),
);
```

## Chip

Etiquetas compactas para mostrar metadata.

```dart
const Chip(label: Text('Flutter'));
InputChip(
  label: const Text('Dart'),
  onSelected: (selected) {},
  avatar: const Icon(Icons.code),
);
```

## Card

Contenedor elevado con bordes redondeados, ideal para listas.

```dart
Card(
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Título', style: TextStyle(fontSize: 18)),
        const SizedBox(height: 8),
        Text('Descripción de la tarjeta'),
      ],
    ),
  ),
);
```

## Patrón de atomización

Los widgets se agrupan en una jerarquía de atomic design:

```
Átomos      → Text, Icon, Chip, Botones, SizedBox
Moléculas   → Card, ListTile, AppBar, BottomNavigationBar
Organismos  → Formulario, Lista, Drawer, Scaffold
Plantillas  → Página específica con layout
Páginas     → Ruta completa con Provider/BlocProvider
```

Crea tus propios widgets atómicos para mantener consistencia:

```dart
class AppText extends StatelessWidget {
  final String texto;
  final TextStyle? style;

  const AppText(this.texto, {super.key, this.style});

  @override
  Widget build(BuildContext context) {
    return Text(
      texto,
      style: (Theme.of(context).textTheme.bodyLarge ?? const TextStyle()).merge(style),
    );
  }
}
```


---

## 📚 Referencias

- [Flutter | Widget catalog](https://docs.flutter.dev/ui/widgets) — Catálogo completo de widgets por categoría
- [Flutter | API reference](https://api.flutter.dev/) — Documentación de la API de Flutter
- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter

---

## Lo que sigue

Ahora que conoces los bloques básicos, el siguiente capítulo cubre cómo organizarlos en layouts y sistemas de navegación.
