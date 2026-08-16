# 11. Arsenal Completo de Widgets

Referencia rápida de todos los widgets útiles para apps móviles. Cada entrada incluye una descripción de una línea y el uso típico. Alineado con **Material 3** y Flutter 3.44+.

## Texto y tipografía

| Widget | Uso |
|---|---|
| `Text` | Texto simple con estilo |
| `RichText` | Texto con múltiples estilos en línea |
| `SelectableText` | Texto seleccionable por el usuario |
| `DefaultTextStyle` | Hereda estilo de texto a hijos |
| `FittedBox` | Escala el hijo para que quepa en el espacio disponible |
| `Wrap` de `TextSpan` | Composición de textos estilizados (en `Text.rich`) |

## Íconos e imágenes

| Widget | Uso |
|---|---|
| `Icon` | Ícono Material Design |
| `Image` | Imagen desde asset, red, archivo o memoria |
| `CircleAvatar` | Avatar circular con inicial o foto |
| `FadeInImage` | Imagen con fade al cargar |
| `Placeholder` | Espacio placeholder visual |
| `CachedNetworkImage` | Imagen de red con caché (paquete `cached_network_image`) |

## Botones

| Widget | Uso |
|---|---|
| `FilledButton` | Botón primario M3 (relleno) |
| `FilledButton.tonal` | Botón secundario M3 (tonal) |
| `OutlinedButton` | Botón con borde |
| `TextButton` | Botón de solo texto |
| `ElevatedButton` | Botón con sombra (legacy M2) |
| `IconButton` | Botón solo ícono |
| `IconButton.filled` / `.tonal` | Variantes M3 con fondo |
| `SegmentedButton` | Grupo de selección exclusiva segmentado (M3) |
| `CloseButton` | Botón de cerrar (back) |
| `BackButton` | Botón de retroceso |

## Controles de entrada

| Widget | Uso |
|---|---|
| `TextField` | Campo de texto libre |
| `TextFormField` | Campo de texto con validación `Form` |
| `DropdownButtonFormField` | Selector desplegable (usa `initialValue`, no `value`) |
| `DropdownMenu` | Menú desplegable M3 con filtro de texto |
| `SearchBar` | Barra de búsqueda M3 (con `SearchAnchor`) |
| `SearchAnchor` | Ancla para búsqueda con vista de resultados |
| `MenuAnchor` | Menú posicionado con ancla declarativa |
| `Checkbox` | Casilla de verificación |
| `Switch` | Interruptor on/off (usa `activeThumbColor`) |
| `Radio` | Botón de opción única (dentro de `RadioGroup`) |
| `RadioGroup` | Agrupa `Radio` y maneja selección + teclado (3.32+) |
| `Slider` | Control deslizante |
| `RangeSlider` | Control de rango |
| `DatePicker` | Selector de fecha (`showDatePicker`) |
| `TimePicker` | Selector de hora (`showTimePicker`) |
| `Autocomplete` | Autocompletado con sugerencias |
| `SwitchListTile` / `CheckboxListTile` / `RadioListTile` | Controles con etiqueta en ListTile |

## Selectores

| Widget | Uso |
|---|---|
| `Chip` | Etiqueta simple |
| `InputChip` | Chip interactivo seleccionable |
| `FilterChip` | Chip para filtrar (multiselección) |
| `ChoiceChip` | Chip de selección única |
| `ActionChip` | Chip que dispara una acción |
| `ToggleButtons` | Botones de toggle múltiple |
| `ExpansionTile` | Fila expandible con contenido (usar `ExpansibleController` desde 3.32 para control programático) |

## Layout

| Widget | Uso |
|---|---|
| `Row` | Diseño horizontal |
| `Column` | Diseño vertical |
| `Flex` | Base de Row/Column con custom direction |
| `Expanded` | Ocupa espacio proporcional |
| `Flexible` | Ocupa espacio sin forzar tamaño mínimo |
| `Stack` | Superposición de widgets |
| `Positioned` | Posición específica dentro de Stack |
| `IndexedStack` | Stack con un hijo visible a la vez |
| `Wrap` | Envoltura automática (como flexbox wrap) |
| `CarouselView` | Carrusel de tarjetas con snapping (3.35+) |

## Contenedores

| Widget | Uso |
|---|---|
| `Container` | Caja con decoración, padding, tamaño |
| `SizedBox` | Caja de tamaño fijo |
| `Padding` | Espaciado interno |
| `Center` | Centra al hijo |
| `Align` | Alinea al hijo en una posición |
| `AspectRatio` | Mantiene relación de aspecto |
| `ConstrainedBox` | Restricciones de tamaño |
| `FractionallySizedBox` | Tamaño relativo al padre |
| `ColoredBox` | Solo color (ligero) |
| `DecoratedBox` | Solo decoración (ligero) |
| `Card` | Tarjeta elevada Material |
| `Card.filled` / `Card.outlined` | Variantes M3 sutiles |
| `Badge` | Indicador superpuesto (contador/notificación) |
| `ClipRect` / `ClipRRect` / `ClipOval` | Recorte visual |
| `SafeArea` | Evita áreas del sistema |
| `InkWell` | Área táctil con efecto Material |
| `GestureDetector` | Detección de gestos genérica |

## Scroll

| Widget | Uso |
|---|---|
| `ListView` | Lista desplazable |
| `ListView.builder` | Lista virtualizada |
| `ListView.separated` | Lista con separadores |
| `GridView` | Cuadrícula desplazable |
| `CustomScrollView` | Scroll con slivers |
| `SingleChildScrollView` | Scroll para contenido único |
| `AnimatedList` | Lista con animaciones |
| `ReorderableListView` | Lista reordenable por drag |
| `PageView` | Páginas swipeables |
| `RefreshIndicator` | Pull-to-refresh |
| `Scrollbar` | Barra de scroll visible |
| `NestedScrollView` | Scroll anidado con header colapsable |
| `NotificationListener` | Escucha notificaciones de scroll |

## Slivers

| Widget | Uso |
|---|---|
| `SliverAppBar` | AppBar que colapsa con scroll |
| `SliverList` | Lista dentro de CustomScrollView |
| `SliverGrid` | Grid dentro de CustomScrollView |
| `SliverToBoxAdapter` | Widget suelto en CustomScrollView |
| `SliverFillRemaining` | Ocupa el espacio restante |
| `SliverPadding` | Padding dentro de sliver |
| `SliverAnimatedList` | AnimatedList sliver |

## Diálogos y notificaciones

| Widget | Uso |
|---|---|
| `AlertDialog` | Diálogo de alerta |
| `SimpleDialog` | Diálogo simple |
| `AboutDialog` | Diálogo Acerca de |
| `BottomSheet` | Panel inferior |
| `SnackBar` | Notificación temporal |
| `Banner` | Banner informativo en parte superior |
| `Tooltip` | Tooltip en hover/longpress |
| `PopupMenuButton` | Menú contextual emergente |
| `showDialog` | Muestra un diálogo |
| `showModalBottomSheet` | Bottom sheet modal |
| `showMenu` | Menú emergente posicionado |

## Navegación

| Widget | Uso |
|---|---|
| `Scaffold` | Estructura base de pantalla |
| `AppBar` | Barra superior |
| `NavigationBar` | Barra de navegación inferior M3 |
| `NavigationDrawer` | Drawer lateral M3 |
| `NavigationRail` | Barra lateral (tablet/desktop) |
| `BottomNavigationBar` | Barra inferior (legacy M2) |
| `Drawer` | Drawer lateral (legacy M2) |
| `TabBar` + `TabBarView` | Pestañas con vistas |
| `PopScope` | Intercepta botón de retroceso (reemplaza `WillPopScope`) |
| `Hero` | Transición compartida entre pantallas |

## Datos y estado

| Widget | Uso |
|---|---|
| `FutureBuilder` | Widget reactivo a Future |
| `StreamBuilder` | Widget reactivo a Stream |
| `ValueListenableBuilder` | Widget reactivo a `ValueNotifier` |
| `ListenableBuilder` | Widget reactivo a cualquier `Listenable` |
| `AnimatedBuilder` | Widget reactivo a Animation |
| `LayoutBuilder` | Widget reactivo a constraints del padre |
| `OrientationBuilder` | Widget reactivo a orientación |

## Decoración y efectos

| Widget | Uso |
|---|---|
| `Divider` | Línea divisoria horizontal |
| `VerticalDivider` | Línea divisoria vertical |
| `SizedBox.expand` | Ocupa todo el espacio disponible |
| `Spacer` | Espacio flexible en Row/Column |
| `IntrinsicHeight` | Altura intrínseca (mide hijos) |
| `IntrinsicWidth` | Ancho intrínseco (mide hijos) |
| `Theme` | Aplica tema a hijos |
| `MediaQuery` | Información de pantalla (usa `sizeOf`/`widthOf`) |
| `Overlay` | Superposición de capas |

## Animaciones implícitas

| Widget | Uso |
|---|---|
| `AnimatedContainer` | Container con animación de propiedades |
| `AnimatedOpacity` | Fade in/out animado |
| `AnimatedPadding` | Padding animado |
| `AnimatedPositioned` | Positioned animado |
| `AnimatedAlign` | Alineación animada |
| `AnimatedSize` | Tamaño animado |
| `AnimatedSwitcher` | Transición entre widgets hijos |
| `AnimatedDefaultTextStyle` | Estilo de texto animado |
| `AnimatedRotation` | Rotación animada |
| `AnimatedScale` | Escala animada |
| `AnimatedSlide` | Desplazamiento animado |
| `TweenAnimationBuilder` | Animación tween declarativa |

## Animaciones explícitas

| Widget | Uso |
|---|---|
| `AnimationController` | Controlador de animación |
| `Animation` | Valor animado |
| `Tween` | Interpolación entre valores |
| `CurvedAnimation` | Curva de easing |
| `FadeTransition` | Transición de opacidad |
| `ScaleTransition` | Transición de escala |
| `SizeTransition` | Transición de tamaño |
| `SlideTransition` | Transición de desplazamiento |
| `RotationTransition` | Transición de rotación |
| `AnimatedBuilder` | Builder genérico de animaciones |
| `Ticker` | Tick de sincronización |
| `CustomPainter` | Dibujo vectorial personalizado |
| `Transform` | Transformación 2D/3D (no animada) |

## Material 3 específicos

| Widget | Uso |
|---|---|
| `NavigationBar` | Barra inferior Material 3 |
| `NavigationDrawer` | Drawer Material 3 |
| `NavigationRail` | Barra lateral (tablet/desktop) |
| `SegmentedButton` | Selección exclusiva segmentada |
| `DropdownMenu` | Menú desplegable con búsqueda |
| `SearchBar` + `SearchAnchor` | Búsqueda M3 |
| `Card.filled` / `Card.outlined` | Tarjetas M3 sutiles |
| `Badge` | Indicador superpuesto |
| `CarouselView` | Carrusel M3 (3.35+) |

## Estructurales (app-level)

| Widget | Uso |
|---|---|
| `MaterialApp` | App con tema Material |
| `MaterialApp.router` | App con GoRouter |
| `Scaffold` | Pantalla completa |
| `ScaffoldMessenger` | Muestra SnackBars |
| `Navigator` | Pila de navegación |
| `Router` | Enrutador declarativo |
| `WidgetsApp` | App base sin Material |

## Widgets Cupertino (iOS-style)

| Widget | Uso |
|---|---|
| `CupertinoPageScaffold` | Página iOS |
| `CupertinoNavigationBar` | Barra superior iOS |
| `CupertinoTabBar` | Barra de tabs iOS |
| `CupertinoButton` | Botón iOS |
| `CupertinoTextField` | Campo de texto iOS |
| `CupertinoSwitch` | Switch iOS |
| `CupertinoSlider` | Slider iOS |
| `CupertinoActivityIndicator` | Indicador de carga iOS |
| `CupertinoAlertDialog` | Alerta iOS |
| `CupertinoDatePicker` | Date picker iOS |
| `CupertinoTimerPicker` | Timer picker iOS |

Nota: No es necesario usar Cupertino widgets. Puedes usar Material 3 con platform adaptivity.

---

## 📚 Referencias

- [Flutter | Widget catalog](https://docs.flutter.dev/ui/widgets) — Catálogo completo de widgets por categoría
- [Flutter | Material 3](https://docs.flutter.dev/ui/material3) — Componentes y estilos M3
- [Flutter | API reference](https://api.flutter.dev/) — Documentación de la API de Flutter
- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter

---

## Lo que sigue

Este módulo terminó. Continúa con [16-BLOC-CUBIT](../16-BLOC-CUBIT/) para aprender a manejar el estado de tu aplicación con BLoC y Cubit.
