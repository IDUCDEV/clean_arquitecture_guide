# 11. Arsenal Completo de Widgets

Referencia rápida de todos los widgets útiles para apps móviles. Cada entrada incluye una descripción de un línea y el uso típico.

## Texto y tipografía

| Widget | Uso |
|---|---|
| `Text` | Texto simple con estilo |
| `RichText` | Texto con múltiples estilos en línea |
| `SelectableText` | Texto seleccionable por el usuario |
| `DefaultTextStyle` | Hereda estilo de texto a hijos |
| `FittedBox` | Escala el hijo para que quepa en el espacio disponible |

## Íconos e imágenes

| Widget | Uso |
|---|---|
| `Icon` | Ícono Material Design |
| `Image` | Imagen desde asset, red, archivo o memoria |
| `CircleAvatar` | Avatar circular con inicial o foto |
| `FadeInImage` | Imagen con fade al cargar |
| `Placeholder` | Espacio placeholder visual |

## Botones

| Widget | Uso |
|---|---|
| `FilledButton` | Botón primario (relleno) |
| `FilledButton.tonal` | Botón secundario (tonal) |
| `OutlinedButton` | Botón con borde |
| `TextButton` | Botón de solo texto |
| `ElevatedButton` | Botón con sombra (legacy) |
| `IconButton` | Botón solo ícono |
| `CloseButton` | Botón de cerrar (back) |
| `BackButton` | Botón de retroceso |

## Controles de entrada

| Widget | Uso |
|---|---|
| `TextField` | Campo de texto libre |
| `TextFormField` | Campo de texto con validación `Form` |
| `DropdownButtonFormField` | Selector desplegable |
| `Checkbox` | Casilla de verificación |
| `Switch` | Interruptor on/off |
| `Radio` | Botón de opción única |
| `Slider` | Control deslizante |
| `RangeSlider` | Control de rango |
| `DatePicker` | Selector de fecha (showDatePicker) |
| `TimePicker` | Selector de hora (showTimePicker) |
| `Autocomplete` | Autocompletado con sugerencias |

## Selectores

| Widget | Uso |
|---|---|
| `Chip` | Etiqueta simple |
| `InputChip` | Chip interactivo seleccionable |
| `FilterChip` | Chip para filtrar (multiselección) |
| `ChoiceChip` | Chip de selección única |
| `ToggleButtons` | Botones de toggle múltiple |

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
| `Card` | Tarjeta elevada Material |
| `ClipRect` / `ClipRRect` / `ClipOval` | Recorte visual |
| `SafeArea` | Evita áreas del sistema |
| `InkWell` | Área táctil con efecto Material |
| `GestureDetector` | Detección de gestos genérica |

## Scroll

| Widget | Uso |
|---|---|
| `ListView` | Lista desplazable |
| `ListView.builder` | Lista virtualizada |
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
| `BottomNavigationBar` | Barra de navegación inferior |
| `NavigationBar` | NavigationBar Material 3 |
| `NavigationDrawer` | Drawer lateral |
| `Drawer` | Drawer lateral (legacy) |
| `TabBar` + `TabBarView` | Pestañas con vistas |
| `WillPopScope` | Intercepta botón de retroceso |
| `Hero` | Transición compartida entre pantallas |

## Datos y estado

| Widget | Uso |
|---|---|
| `FutureBuilder` | Widget reactivo a Future |
| `StreamBuilder` | Widget reactivo a Stream |
| `ValueListenableBuilder` | Widget reactivo a ValueNotifier |
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
| `MediaQuery` | Información de pantalla |
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
- [Flutter | API reference](https://api.flutter.dev/) — Documentación de la API de Flutter
- [Flutter | Layouts](https://docs.flutter.dev/ui/layout) — Guía de layouts en Flutter

---
