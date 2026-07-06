# 07 — M3 a Flutter: Implementación

**Traducir el sistema de diseño a código**

---

Flutter implementa M3 de forma nativa. No necesitas paquetes adicionales. Solo activarlo.

## 1. Activar M3

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true, // ← Activa M3
    colorScheme: ColorScheme.fromSeed(
      seedColor: Color(0xFF6750A4), // seed color
    ),
  ),
  darkTheme: ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: Color(0xFF6750A4),
      brightness: Brightness.dark,
    ),
  ),
  themeMode: ThemeMode.system, // respeta preferencia del sistema
)
```

Con `useMaterial3: true`:
- Los componentes M3 cambian sus defaults (NavigationBar, Cards, Buttons, etc.)
- Se activa la escala tipográfica M3
- Las formas cambian a las redondeadas de M3

## 2. ColorScheme

La clase central de color en M3.

### Desde un seed color (recomendado)

```dart
ColorScheme.fromSeed(
  seedColor: Color(0xFF6750A4),
  brightness: Brightness.light,
)
```

Esto genera **automáticamente** los 12 tonos. No necesitas definir nada más.

### Esquema personalizado

```dart
ColorScheme(
  primary: Color(0xFF6750A4),
  onPrimary: Colors.white,
  primaryContainer: Color(0xFFEADDFF),
  onPrimaryContainer: Color(0xFF21005D),
  secondary: Color(0xFF625B71),
  onSecondary: Colors.white,
  surface: Color(0xFFFFFBFE),
  onSurface: Color(0xFF1C1B1F),
  // ... más roles
)
```

Usa `fromSeed` siempre que puedas. Personaliza solo cuando necesites un color exacto de marca.

### Dynamic Color (Material You)

```dart
// En Android 12+
ColorScheme.fromSeed(
  seedColor: Color(0xFF6750A4),
  dynamicSchemeVariant: DynamicSchemeVariant.tonalSpot,
  brightness: Brightness.light,
)
```

`DynamicSchemeVariant` controla el estilo de la paleta generada:

| Variante | Efecto |
|---|---|
| `tonalSpot` | Default. Balanceado |
| `fidelity` | Se acerca más al color original |
| `monochrome` | Un solo tono |
| `neutral` | Colores neutros |
| `vibrant` | Más saturado |
| `expressive` | Colores llamativos |

## 3. TextTheme

La escala tipográfica M3 en Flutter:

```dart
TextTheme(
  displayLarge: TextStyle(fontSize: 57, fontWeight: FontWeight.w400),
  headlineLarge: TextStyle(fontSize: 32, fontWeight: FontWeight.w400),
  titleLarge: TextStyle(fontSize: 22, fontWeight: FontWeight.w500),
  bodyLarge: TextStyle(fontSize: 16, fontWeight: FontWeight.w400),
  labelLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
  // ... más estilos
)
```

Uso en widgets:

```dart
Text('Título de la pantalla', style: Theme.of(context).textTheme.titleLarge)
Text('Cuerpo del texto', style: Theme.of(context).textTheme.bodyMedium)
```

### Font family personalizada

```dart
ThemeData(
  textTheme: TextTheme(
    titleLarge: TextStyle(fontFamily: 'Inter', fontSize: 22),
    bodyMedium: TextStyle(fontFamily: 'Inter', fontSize: 14),
  ),
)
```

O global con `ThemeData(fontFamily: 'Inter')`.

## 4. ShapeScheme (formas)

En Flutter, las formas se definen por componente:

```dart
ThemeData(
  cardTheme: CardTheme(
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12), // medium
    ),
  ),
  filledButtonTheme: FilledButtonThemeData(
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(8), // small
    ),
  ),
)
```

## 5. Componentes M3

Una vez activado `useMaterial3`, los widgets de Flutter ya usan M3:

| Widget | Cambio con M3 |
|---|---|
| `NavigationBar` | Reemplaza BottomNavigationBar. Más compacto, colores M3 |
| `NavigationDrawer` | Reemplaza Drawer tradicional |
| `FilledButton` | Nuevo. Botón principal con fondo lleno |
| `FilledTonalButton` | Nuevo. Botón con fondo tonal |
| `SegmentedButton` | Nuevo. Reemplaza ToggleButtons |
| `SearchBar` | Nuevo. Barra de búsqueda M3 |
| `Card` | Por defecto usa esquinas redondeadas M3 |
| `Badge` | Nuevo. Indicador de notificaciones |

## 6. ThemeExtensions (tokens personalizados)

Para valores que no cubre M3 (spacing, radii, custom shadows):

```dart
class AppSpacing extends ThemeExtension<AppSpacing> {
  final double xs;
  final double sm;
  final double md;
  final double lg;

  const AppSpacing({required this.xs, required this.sm, required this.md, required this.lg});

  @override
  AppSpacing copyWith({double? xs, double? sm, double? md, double? lg}) {
    return AppSpacing(xs: xs ?? this.xs, sm: sm ?? this.sm, md: md ?? this.md, lg: lg ?? this.lg);
  }

  @override
  AppSpacing lerp(AppSpacing? other, double t) {
    if (other == null) return this;
    return AppSpacing(
      xs: lerpDouble(xs, other.xs, t)!,
      sm: lerpDouble(sm, other.sm, t)!,
      md: lerpDouble(md, other.md, t)!,
      lg: lerpDouble(lg, other.lg, t)!,
    );
  }
}
```

Uso:

```dart
Theme.of(context).extension<AppSpacing>()!.md // → 16
```

## 7. Dark mode

Con `ColorScheme.fromSeed` y `Brightness.dark`, obtienes dark mode automático:

```dart
ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(
    seedColor: brandColor,
    brightness: Brightness.dark,
  ),
)
```

No necesitas ajustar nada. Los componentes M3 se adaptan solos.

## 8. Arquitectura del theme (buena práctica)

Separa el theme en archivos independientes:

```
lib/theme/
├── app_theme.dart        → ThemeData light + dark
├── app_colors.dart       → ColorScheme (light + dark)
├── app_typography.dart   → TextTheme
└── app_extensions.dart   → ThemeExtensions (spacing, radii)
```

Esto es exactamente lo que incluye el template de este módulo.

## Checklist de implementación M3

- [ ] `useMaterial3: true` activado
- [ ] `ColorScheme.fromSeed` con seed color de marca
- [ ] Light + dark scheme definidos
- [ ] `textTheme` personalizado (fuente de marca si aplica)
- [ ] Componentes actualizados a M3 (NavigationBar, etc.)
- [ ] `ThemeExtensions` para tokens no cubiertos
- [ ] `ThemeMode.system` para respetar preferencia del usuario

---

**Siguiente: [08 — Template de proyecto](08-template-proyecto.md)**
