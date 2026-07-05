# 7. Animaciones

## ImplicitlyAnimatedWidget

La familia de widgets con animaciones implícitas: solo cambias el target y Flutter interpola.

```dart
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeInOut,
  width: _expandido ? 200 : 100,
  height: _expandido ? 200 : 100,
  color: _expandido ? Colors.blue : Colors.red,
  child: const Center(child: Text('Animar')),
);

AnimatedOpacity(
  duration: const Duration(milliseconds: 300),
  opacity: _visible ? 1.0 : 0.0,
  child: const Text('Aparece/Desaparece'),
);

AnimatedPadding(
  duration: const Duration(milliseconds: 300),
  padding: _grande ? EdgeInsets.all(32) : EdgeInsets.all(8),
  child: const Text('Con padding animado'),
);

AnimatedSwitcher(
  duration: const Duration(milliseconds: 300),
  child: Text(
    '$_contador',
    key: ValueKey(_contador), // clave única para la transición
    style: const TextStyle(fontSize: 32),
  ),
);
```

Otros: `AnimatedPositioned`, `AnimatedAlign`, `AnimatedSize`, `AnimatedDefaultTextStyle`, `TweenAnimationBuilder`.

## AnimationController

Control manual de animaciones.

```dart
class _MiAnimacionState extends State<MiAnimacion>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _anim;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    );
    _anim = Tween<double>(begin: 0, end: 300).animate(_ctrl);
    _ctrl.forward();
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _anim,
      builder: (context, child) {
        return Container(
          width: _anim.value,
          height: _anim.value,
          color: Colors.blue,
          child: child,
        );
      },
      child: const Text('Crece'),
    );
  }
}
```

## CurvedAnimation

Aplica curvas de easing a la animación.

```dart
final curved = CurvedAnimation(
  parent: _ctrl,
  curve: Curves.easeOutBack,    // entrada
  reverseCurve: Curves.easeIn,  // salida
);
final _anim = Tween<double>(begin: 0, end: 1).animate(curved);
```

Curvas comunes: `easeIn`, `easeOut`, `easeInOut`, `bounceIn`, `easeOutBack`, `elasticOut`.

## AnimationStatusListener

Reaccionar a eventos del ciclo de la animación.

```dart
_ctrl.addStatusListener((status) {
  switch (status) {
    case AnimationStatus.completed:
      // Repetir o invertir
      _ctrl.reverse();
    case AnimationStatus.dismissed:
      _ctrl.forward();
    case AnimationStatus.forward:
    case AnimationStatus.reverse:
      // en progreso
  }
});
```

## Hero

Transición compartida entre pantallas.

```dart
// Pantalla origen
Hero(
  tag: 'avatar-${usuario.id}',
  child: CircleAvatar(
    radius: 30,
    backgroundImage: NetworkImage(usuario.avatarUrl),
  ),
);

// Pantalla destino (mismo tag)
Hero(
  tag: 'avatar-${usuario.id}',
  child: CircleAvatar(
    radius: 80, // tamaño diferente, anima automáticamente
    backgroundImage: NetworkImage(usuario.avatarUrl),
  ),
);
```

La transición ocurre automáticamente entre `Navigator.push`.

## CustomPainter

Dibujo vectorial personalizado (gráficas, formas, backgrounds).

```dart
class MiPainter extends CustomPainter {
  final double progreso;

  MiPainter({required this.progreso});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.blue
      ..style = PaintingStyle.fill;

    canvas.drawCircle(
      Offset(size.width / 2, size.height / 2),
      size.width / 2 * progreso,
      paint,
    );
  }

  @override
  bool shouldRepaint(covariant MiPainter old) => old.progreso != progreso;
}

// Uso
CustomPaint(
  size: const Size(100, 100),
  painter: MiPainter(progreso: 0.75),
);
```

## StaggeredAnimations

Múltiples animaciones encadenadas con diferentes delays.

```dart
class _StaggeredState extends State<StaggeredWidget>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _fade;
  late final Animation<Offset> _slide;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    );
    _fade = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _ctrl, curve: const Interval(0.0, 0.5)),
    );
    _slide = Tween<Offset>(
      begin: const Offset(0, 0.5),
      end: Offset.zero,
    ).animate(
      CurvedAnimation(parent: _ctrl, curve: const Interval(0.3, 1.0)),
    );
    _ctrl.forward();
  }

  @override
  Widget build(BuildContext context) {
    return SlideTransition(
      position: _slide,
      child: FadeTransition(
        opacity: _fade,
        child: const Text('Animación escalonada'),
      ),
    );
  }
}
```

## Lottie / Rive (animaciones JSON)

```dart
// pubspec.yaml: lottie: ^3.0.0

Lottie.asset(
  'assets/animaciones/loading.json',
  width: 200,
  height: 200,
  animate: true,
  repeat: true,
);

// Con control manual
final _ctrl = LottieController();

Lottie.asset(
  'assets/animaciones/check.json',
  controller: _ctrl,
);
_ctrl.play();
```

## Reglas para animaciones

- Prefiere animaciones implícitas (`AnimatedContainer`, `AnimatedOpacity`) para casos simples.
- Usa `AnimationController` + `AnimatedBuilder` para control fino.
- Mantén las animaciones en ~300ms para interacciones táctiles.
- Usa `Curves.bounceIn` o `easeOutBack` para efectos llamativos controlados.
- No animes: `opacity` + `size` simultáneamente (causa rebotes).


---

## 📚 Referencias

- [Flutter | Widget catalog](https://docs.flutter.dev/ui/widgets) — Catálogo completo de widgets por categoría
- [Flutter | API reference](https://api.flutter.dev/) — Documentación de la API de Flutter
- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter

---

## Lo que sigue

El siguiente capítulo cubre estrategias de composición de widgets para construir UIs complejas de forma mantenible.
