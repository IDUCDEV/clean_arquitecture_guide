# 09 — Caso completo: App de Reservas

**De Design Sprint a Flutter con M3 en 5 días**

---

Este caso integrador recorre el proceso completo con un ejemplo real: una app MVP para **reservar canchas de tenis**.

## Día 1: Understand + Define

### Goal a largo plazo

> "Los usuarios pueden reservar una cancha de tenis en menos de 30 segundos desde su teléfono, sin llamar por teléfono."

**Métrica principal:** Tiempo promedio de reserva < 30 segundos.

### Mapa del problema

```
[Usuario quiere jugar tenis]
  → Google Maps "canchas de tenis cerca"
  → Encuentra teléfono
  → Llama → Ocupado → Llama de nuevo
  → "¿Tienen cancha libre a las 5pm?"
  → "Sí" → "OK, reserve"
  → Llega → No está reservada → Enfado
  ← Pierde una hora de juego ←
```

### HMWs seleccionados

- "¿Cómo podríamos mostrar disponibilidad en tiempo real?"
- "¿Cómo podríamos permitir reservar sin hablar con nadie?"
- "¿Cómo podríamos confirmar la reserva instantáneamente?"

### Golden Path

```
1. Home → buscar canchas (filtro por fecha/hora)
2. Lista de canchas disponibles → seleccionar
3. Confirmar datos → pagar
4. Confirmación → ticket digital
```

### Alcance del MVP

| Incluye | No incluye |
|---|---|
| Búsqueda por fecha/hora | Registro de usuario obligatorio |
| Lista de canchas con precio | Historial de reservas |
| Reserva y pago | Favoritos |
| Confirmación | Chat con el club |
| Modo invitado (sin registro) | Reseñas |

### Sprint Goal

> "Validar que un usuario puede encontrar y reservar una cancha de tenis en menos de 30 segundos sin ayuda."

---

## Día 2: Sketch

### Solution Sketch (por el diseñador)

Panel 1: Usuario frustrado llamando por teléfono sin respuesta.
Panel 2: App con campo de búsqueda, calendario y botón "Reservar".
Panel 3: Usuario feliz con confirmación en pantalla.

---

## Día 3: Decide

### Storyboard final

```
┌─────────────────┐
│  Pantalla 1     │
│  Home           │
│  ┌───────────┐  │
│  │ SearchBar │  │  "Buscar canchas..."
│  └───────────┘  │
│  [Hoy] [Mañana] │  ← SegmentedButton
│  [◀] [5:00] [▶] │
│  ┌───────────┐  │
│  │ Card       │  │  Cancha 1 - $15/h - Libre
│  │ Card       │  │  Cancha 2 - $18/h - Libre
│  │ Card       │  │  Cancha 3 - $20/h - Ocupado
│  └───────────┘  │
└─────────────────┘
         ↓ tap en card
┌─────────────────┐
│  Pantalla 2     │
│  Detalle + Pago  │
│  Cancha de Tenis│
│  Club Deportivo │
│  ─────────────  │
│  Fecha: 15 Jul  │
│  Hora: 5:00 PM  │
│  Precio: $15    │
│  ┌───────────┐  │
│  │ FilledBtn │  │  "Reservar y pagar"
│  └───────────┘  │
└─────────────────┘
         ↓ tap en botón
┌─────────────────┐
│  Pantalla 3     │
│  Confirmación   │
│  ✓              │
│  "Reserva       │
│  confirmada"    │
│  Cancha 1       │
│  5:00 PM        │
│  Código: T-047  │
│                 │
│  [Volver al inicio]│
└─────────────────┘
```

### Componentes M3 identificados

| Pantalla | Componentes M3 |
|---|---|
| Home | `SearchBar`, `SegmentedButton`, `Card` + `ListTile` |
| Detalle | `Card`, `FilledButton`, `ListTile` |
| Confirmación | `Card`, `Icon` (check), `TextButton` |
| Estados | `CircularProgressIndicator`, `SnackBar`, `AlertDialog` |

---

## Día 4: Prototype (Figma + Flutter)

### Theme M3 definido

```
Seed color: #1B5E20 (verde oscuro, evoca cancha de tenis)
→ Light + Dark scheme generados con ColorScheme.fromSeed
→ Tipografía: Google Fonts Inter
→ Shape: 8px small, 12px medium, 16px large
```

### Pantallas en Figma

Se crean las 3 pantallas del storyboard usando componentes M3 del kit de Figma.
Flujos conectados: Home → Detalle → Confirmación.

### Base en Flutter (template)

Se copia el template y se configura el theme con el seed color verde.

---

## Día 5: Validate

### Usuarios reclutados

5 personas que juegan tenis al menos 1 vez por semana.

### Resultados

| Usuario | Completó la tarea? | Tiempo | Problemas |
|---|---|---|---|
| 1 | ✅ Sí | 25s | Ninguno |
| 2 | ✅ Sí | 20s | Dudó en el SearchBar (no obvio) |
| 3 | ✅ Sí | 35s | Quería filtrar por precio |
| 4 | ❌ No | 60s | No encontró el botón de reserva |
| 5 | ✅ Sí | 28s | "Muy fácil, me encantó" |

### Hallazgos

| Hallazgo | Prioridad | Acción |
|---|---|---|
| SearchBar no es obvio como buscador | Alta | Agregar hint text + icono de lupa más claro |
| Falta filtro por precio | Media | Agregar como post-MVP |
| Botón de reserva muy abajo | Alta | Mover FilledButton arriba, hacerlo sticky |
| El flujo general funciona | - | MVP validado, pasar a desarrollo |

### Decisión

**✅ Pasar a desarrollo.** Los 3 de 5 usuarios completaron la tarea en <30s. Los problemas identificados son fáciles de corregir antes del lanzamiento.

---

## De vuelta a Flutter: implementación del MVP

Con el prototipo validado y los hallazgos corregidos, se implementa usando:

1. **Template M3** → theme con seed color + dark mode
2. **Clean Architecture** → features/mvp con data/domain/presentation
3. **Datos mock** → sin backend todavía (los repositorios devuelven datos estáticos)
4. **Golden Path** → las 3 pantallas conectadas con navegación

```dart
// app.dart
MaterialApp(
  theme: AppTheme.light,
  darkTheme: AppTheme.dark,
  themeMode: ThemeMode.system,
  home: HomePage(),
)
```

```dart
// features/mvp/presentation/pages/home_page.dart
class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Reservar cancha')),
      body: Column(
        children: [
          SearchBar(hintText: 'Buscar canchas...'),
          SegmentedButton(...),
          Expanded(
            child: ListView(
              children: canchas.map((c) => Card(
                child: ListTile(
                  title: Text(c.nombre),
                  subtitle: Text('\$${c.precio}/h'),
                  trailing: c.disponible
                    ? FilledButton(onPressed: () {}, child: Text('Reservar'))
                    : Chip(label: Text('Ocupado')),
                ),
              )).toList(),
            ),
          ),
        ],
      ),
      bottomNavigationBar: NavigationBar(destinations: [...]),
    );
  }
}
```

---

## Lecciones del caso real

1. **El Design Sprint ahorró semanas**: detectamos el problema del botón de reserva antes de escribir código.
2. **M3 aceleró el diseño**: no diseñamos desde cero, usamos componentes ya definidos.
3. **El template M3 + Clean Arch**: nos permitió pasar de prototipo a código en horas.
4. **La validación con 5 usuarios fue suficiente**: encontramos los problemas críticos.

---

**Siguiente: [BIBLIOGRAFIA](BIBLIOGRAFIA.md)**
