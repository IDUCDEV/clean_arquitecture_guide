# 10. Rendimiento y Buenas Prácticas

## const widgets

Es la optimización más importante y la más fácil.

```dart
// MAL
@override
Widget build(BuildContext context) {
  return Container(
    child: Text('Hola'),  // nuevo objeto cada build
  );
}

// BIEN
@override
Widget build(BuildContext context) {
  return const SizedBox(
    width: 100, height: 100,
    child: Text('Hola'), // misma instancia siempre
  );
}
```

## Extraer sub-widgets

Dividir widgets grandes permite que Flutter reconstruya solo las partes necesarias.

```dart
// MAL: todo en el mismo build
@override
Widget build(BuildContext context) {
  return Column(
    children: [
      _Header(),     // cambia con el estado
      _Expensive(),  // NO cambia pero se reconstruye igual
      _Footer(),     // NO cambia pero se reconstruye igual
    ],
  );
}

// BIEN: Extraer _Expensive como StatelessWidget const
class _Expensive extends StatelessWidget {
  const _Expensive(); // ← const constructor

  @override
  Widget build(BuildContext context) {
    // Este widget NO se reconstruye si el padre cambia
    // porque es const y su padre no le pasa nuevos parámetros
    return Text('No cambio');
  }
}
```

## ListView.builder sobre ListView(children:[])

```dart
// MAL: construye todos los items aunque no sean visibles
ListView(children: items.map((i) => _Item(i)).toList());

// BIEN: solo construye los visibles
ListView.builder(
  itemCount: items.length,
  itemBuilder: (_, i) => _Item(items[i]),
);
```

## RepaintBoundary

Aísla partes del árbol para que no se repinten completas.

```dart
// Aísla el mapa para que no se repinte al hacer scroll
ListView(
  children: [
    RepaintBoundary(child: MapaWidget()),
    for (final item in items) _Item(item),
  ],
);

// Útil para: mapas, videos, animaciones aisladas, Canvas
```

## Avoid reconstitutions innecesarias

```dart
// MAL: nuevo widget en cada build
@override
Widget build(BuildContext context) {
  return ChildWidget(
    callback: () { print('hola'); }, // nueva closure cada build
  );
}

// BIEN: método separado o clase
void _handleClick() => print('hola');

@override
Widget build(BuildContext context) {
  return ChildWidget(callback: _handleClick);
}
```

## AnimatedBuilder vs setState en animaciones

```dart
// MAL: setState en cada frame reconstruye todo el widget
@override
Widget build(BuildContext context) {
  return Container(
    width: _anim.value,
    height: _anim.value,
    child: const Text('Animado'),
  );
}

// BIEN: AnimatedBuilder solo reconstruye el subárbol necesario
AnimatedBuilder(
  animation: _anim,
  builder: (context, child) {
    return Container(
      width: _anim.value,
      height: _anim.value,
      child: child,
    );
  },
  child: const Text('Animado'), // no se reconstruye
);
```

## Keys para preservar estado

```dart
// Sin key: al reordenar, Flutter confunde los widgets
// Con key: Flutter sabe cuál mover
ListView.builder(
  itemBuilder: (_, i) => _Item(key: ValueKey(items[i].id), item: items[i]),
);
```

## Evitar Opacity con animaciones

```dart
// MAL: Opacity fuerza repintado
Opacity(opacity: 0.5, child: const Text('Hola'));

// BIEN: AnimatedOpacity o FadeTransition
FadeTransition(opacity: _anim, child: const Text('Hola'));
```

## Evitar Column/Row dentro de ListView.builder

```dart
// MAL: Column mide a sus hijos antes de renderizar
ListView.builder(
  itemBuilder: (_, i) => Column(children: [/* varios widgets */]),
);

// BIEN: si el item cabe en una sola línea, usa ListTile
ListView.builder(
  itemBuilder: (_, i) => ListTile(title: Text(items[i])),
);
```

## Imágenes: caché y dimensiones

```dart
// MAL: sin caché, tamaño original
Image.network('https://ejemplo.com/grande.jpg');

// BIEN: con caché y dimensiones controladas
CachedNetworkImage(
  imageUrl: 'https://ejemplo.com/grande.jpg',
  width: 200,
  height: 200,
  fit: BoxFit.cover,
  memCacheWidth: 400, // tamaño para memoria (2x por retina)
);

// Para múltiples imágenes de red, precarga:
Future.wait(
  urls.map((url) => precacheImage(NetworkImage(url), context)),
);
```

## Flutter DevTools

- **Rebuild Counts**: identifica widgets que se reconstruyen sin necesidad.
- **Track widget rebuilds**: muestra por qué se reconstruyó un widget.
- **Performance overlay**: muestra la velocidad de frames (target: 60fps o 120fps).

## Checklist de performance

- [ ] ¿Widgets hijos son `const` cuando no cambian?
- [ ] ¿ListView usa `.builder`?
- [ ] ¿Sub-widgets extraídos para evitar reconstrucciones masivas?
- [ ] ¿Imágenes tienen `width`/`height` y caché?
- [ ] ¿Animaciones con `AnimatedBuilder` en lugar de `setState`?
- [ ] ¿RepaintBoundary en mapas/videos/canvas?
- [ ] ¿Keys correctas en listas dinámicas?

## Lo que sigue

El próximo capítulo es un arsenal de referencia rápida con todos los widgets vistos y más.
