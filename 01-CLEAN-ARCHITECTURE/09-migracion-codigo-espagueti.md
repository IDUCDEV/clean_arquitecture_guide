## 10. Migración desde Código Espagueti

### Estrategia de Migración Gradual

No necesitas reescribir todo de una vez. Migra feature por feature.

#### Paso 1: Aislar una feature

```dart
// Antes: Todo mezclado
class UserPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: http.get(Uri.parse('/api/users')),  // ❌ HTTP en UI
      builder: (context, snapshot) { /* ... */ },
    );
  }
}
```

#### Paso 2: Crear la estructura de carpetas
```
lib/features/user/
├── data/
├── domain/
└── presentation/
```

#### Paso 3: Mover código gradualmente
1. Mueve los modelos JSON a `data/models`
2. Crea las Entities puras en `domain/entities`
3. Extrae la lógica de UI a un Cubit

#### Paso 4: Conectar todo con inyección de dependencias

### Checklist de Migración

```
□ Feature seleccionada (empezar por la más simple)
□ Estructura de carpetas creada
□ Entity extraída del modelo anterior
□ Repository interface creada
□ UseCases extraídos
□ Cubit/State creado
□ DataSources implementados
□ Repository implementation completada
□ Inyección de dependencias configurada
□ Tests escritos
□ Feature probada completamente
```

---
