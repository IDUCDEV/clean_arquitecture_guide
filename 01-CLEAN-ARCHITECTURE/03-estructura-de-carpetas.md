## 3. Estructura de Carpetas

### Estructura Base Universal

```
lib/
├── core/                           # Código compartido entre features
│   ├── common/                     # Clases base (UseCase, etc.)
│   │   └── usecase.dart
│   ├── data/                       # Configuración de datos global
│   │   └── local/
│   │       ├── dashboard_initializer.dart
│   │       └── isar_service.dart
│   ├── di/                         # Inyección de dependencias
│   │   ├── injection_container.dart
│   │   └── service_locator.dart
│   ├── error/                      # Manejo de errores
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/                    # Monitoreo de conectividad
│   │   └── network_info.dart
│   ├── routing/                    # Navegación
│   │   └── app_router.dart
│   ├── services/                   # Servicios globales (CacheManager, etc.)
│   │   └── cache_manager.dart
│   ├── session/                    # Sesión del usuario autenticado
│   │   ├── user_session.dart
│   │   └── user_session_impl.dart
│   ├── theme/                      # Tema y estilos
│   │   └── app_theme.dart
│   └── utils/                      # Utilidades
│       └── constants.dart
│       └── widgets/                # Widgets reutilizables
│
├── features/                       # Cada feature tiene su propia estructura
│   └── {feature_name}/
│       ├── data/
│       │   ├── datasources/
│       │   │   └── {feature}_local_data_source.dart
│       │   │   └── {feature}_remote_data_source.dart  # Opcional
│       │   ├── models/
│       │   │   └── {feature}_model.dart
│       │   └── repositories/
│       │       └── {feature}_repository_impl.dart
│       │
│       ├── domain/
│       │   ├── entities/
│       │   │   └── {feature}.dart
│       │   ├── repositories/
│       │   │   └── {feature}_repository.dart
│       │   └── usecases/
│       │       ├── get_{feature}.dart
│       │       ├── create_{feature}.dart
│       │       └── delete_{feature}.dart
│       │
│       └── presentation/
│           ├── cubit/
│           │   ├── {feature}_cubit.dart
│           │   └── {feature}_state.dart
│           └── pages/
│               └── {feature}_page.dart
│
└── main.dart
```

### Reglas de Organización

#### ✅ Hacer:
- Una carpeta por feature
- Feature es independiente de otras features
- Core no depende de features
- Cada capa en su carpeta correspondiente

#### ❌ No Hacer:
```
lib/
├── data/           # ❌ Mal: Todos los datos juntos
├── domain/         # ❌ Mal: Todas las entidades juntas
├── ui/             # ❌ Mal: Todas las pantallas juntas
└── models/         # ❌ Mal: Todos los modelos juntos
```

#### ✅ Hacer:
```
lib/
├── features/
│   ├── user/       # ✅ Bien: Todo lo de usuario aquí
│   ├── product/    # ✅ Bien: Todo lo de producto aquí
│   └── order/      # ✅ Bien: Todo lo de orden aquí
└── core/           # ✅ Bien: Solo código compartido
```

---
