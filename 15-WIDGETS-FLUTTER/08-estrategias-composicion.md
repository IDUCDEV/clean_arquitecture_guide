# 8. Estrategias de Composición

## Composición > Herencia

En Flutter no se extienden widgets para modificarlos. Se **componen** conteniendo unos dentro de otros.

```dart
// MAL: heredar comportamiento
class MiBotonEspecial extends ElevatedButton {
  MiBotonEspecial({super.onPressed, super.child}); // frágil
}

// BIEN: componer con parámetros
class AccionBoton extends StatelessWidget {
  final String texto;
  final VoidCallback? onPressed;
  final IconData? icono;

  const AccionBoton({
    super.key,
    required this.texto,
    this.onPressed,
    this.icono,
  });

  @override
  Widget build(BuildContext context) {
    return FilledButton.icon(
      onPressed: onPressed,
      icon: icono != null ? Icon(icono) : const SizedBox.shrink(),
      label: Text(texto),
    );
  }
}
```

## Widgets puros (sin estado)

Siempre que un widget pueda ser `StatelessWidget`, hazlo `const`. Esto permite que Flutter lo optimice.

```dart
class UserAvatar extends StatelessWidget {
  final String nombre;
  final String? fotoUrl;
  final double tamaño;

  const UserAvatar({
    super.key,
    required this.nombre,
    this.fotoUrl,
    this.tamaño = 48,
  });

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      radius: tamaño / 2,
      backgroundImage: fotoUrl != null ? NetworkImage(fotoUrl!) : null,
      child: fotoUrl == null ? Text(nombre[0].toUpperCase()) : null,
    );
  }
}
```

## Widgets privados anidados

Divide widgets grandes en sub-widgets privados para mejorar legibilidad y rendimiento.

```dart
class PerfilPage extends StatelessWidget {
  const PerfilPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Perfil')),
      body: const _Body(),
    );
  }
}

class _Body extends StatelessWidget {
  const _Body();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: const [
        _AvatarSection(),
        _InfoSection(),
        _AccionesSection(),
      ],
    );
  }
}
```

Cada sub-widget es un `const` que puede rebuildearse independientemente.

## Separación de responsabilidades

```
Página        → Scaffold + AppBar + BlocProvider
Sección       → Column/Row con agrupación lógica
Componente    → Widget reutilizable (atómico)
```

Cada widget debe tener **una** responsabilidad.

## Builder pattern para contextos

Cuando necesitas un `BuildContext` diferente (por ejemplo, dentro de un Scaffold para SnackBar):

```dart
// Builder crea un nuevo contexto en el árbol
Scaffold(
  body: Builder(
    builder: (context) {
      return ElevatedButton(
        onPressed: () {
          // Este contexto tiene acceso al Scaffold
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Hecho')),
          );
        },
        child: const Text('Mostrar SnackBar'),
      );
    },
  ),
);
```

## InheritedWidget (acceso implícito)

Es el mecanismo interno que usan Theme, MediaQuery, BLoC, etc. No lo uses directamente; entiende cómo funciona.

```dart
// Detrás de escena: BlocProvider es un InheritedWidget
// context.read<T>() busca hacia arriba en el árbol
// context.watch<T>() busca Y se suscribe a cambios

final theme = Theme.of(context);           // InheritedWidget
final size = MediaQuery.of(context).size;  // InheritedWidget
final cubit = context.read<MiCubit>();     // BlocProvider → InheritedWidget
```

## Naming: sufijos de widgets

Usa sufijos consistentes para identificar el tipo de widget:

| Sufijo | Ejemplo | Propósito |
|---|---|---|
| Page | `LoginPage` | Ruta completa con Scaffold |
| View | `ProfileView` | Contenido de una sección (body) |
| Card | `ProductCard` | Elemento de lista/tarjeta |
| Tile | `ContactTile` | Fila de datos |
| Form | `RegisterForm` | Formulario con validación |
| Dialog | `ConfirmDialog` | Diálogo modal |
| Button | `SocialButton` | Botón personalizado |
| Row | `InfoRow` | Fila de datos horizontal |
| Badge | `NotificationBadge` | Indicador superpuesto |

## Composición de layouts condicional

```dart
class ResponsiveLayout extends StatelessWidget {
  const ResponsiveLayout({super.key});

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width;

    if (width < 600) {
      return const _MobileLayout();
    } else if (width < 1200) {
      return const _TabletLayout();
    }
    return const _DesktopLayout();
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

Pasamos a patrones de renderización condicional y control de estado visual.
