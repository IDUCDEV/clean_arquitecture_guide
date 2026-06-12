## 5. Implementación Práctica: Sistema de Usuarios CRUD

Vamos a implementar un sistema CRUD completo de usuarios.

### Requerimientos
1. Ver lista de usuarios
2. Crear usuario
3. Ver detalle de usuario
4. Eliminar usuario

### Estructura de Archivos

```
lib/features/user/
├── data/
│   ├── datasources/
│   │   └── user_local_data_source.dart
│   ├── models/
│   │   └── user_model.dart
│   │   └── user_model.g.dart
│   └── repositories/
│       └── user_repository_impl.dart
├── domain/
│   ├── entities/
│   │   └── user.dart
│   ├── repositories/
│   │   └── user_repository.dart
│   └── usecases/
│       ├── create_user.dart
│       ├── delete_user.dart
│       ├── get_user.dart
│       └── get_users.dart
└── presentation/
    ├── cubit/
    │   ├── user_cubit.dart
    │   └── user_state.dart
    └── pages/
        ├── user_detail_page.dart
        └── users_list_page.dart
```

---

