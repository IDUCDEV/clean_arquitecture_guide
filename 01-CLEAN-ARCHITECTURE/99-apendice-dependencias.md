## Resumen del Flujo Completo

```
Usuario toca botón "Crear Usuario"
    ↓
UI llama a cubit.createUser()
    ↓
Cubit emite UserLoading()
    ↓
Cubit llama a createUserUseCase.execute()
    ↓
UseCase llama a repository.createUser()
    ↓
Repository verifica: ¿Hay internet?
    ├─► SÍ → remoteDataSource.createUser() → API REST
    │      └→ localDataSource.saveUser() → Guardar en caché
    │
    └─► NO → return NetworkFailure('No se puede crear offline')
    ↓
Datos vuelven convertidos a Entity
    ↓
Cubit emite UserOperationSuccess
    ↓
Cubit llama a loadUsers() para actualizar lista
    ↓
UI se reconstruye y muestra el usuario nuevo
```

**Flujo para obtener usuarios (con caché):**

```
Usuario abre la pantalla
    ↓
UI llama a cubit.loadUsers()
    ↓
Cubit llama a getUsersUseCase.execute()
    ↓
UseCase llama a repository.getUsers()
    ↓
Repository verifica: ¿Hay internet?
    ├─► SÍ → remoteDataSource.getUsers() → API REST
    │      └→ cacheUsers() → Guardar todos en Isar
    │
    └─► NO → localDataSource.getUsers() → Leer de Isar
    ↓
Datos vuelven convertidos a List<User>
    ↓
Cubit emite UsersLoaded(users)
    ↓
UI se reconstruye y muestra la lista
```

---

## Dependencias Recomendadas (pubspec.yaml)

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Core
  flutter_bloc: ^8.1.3
  get_it: ^7.6.4
  equatable: ^2.0.5
  fpdart: ^1.2.0
  
  # Network
  dio: ^5.3.3
  internet_connection_checker: ^1.0.0+1
  
  # Local Storage - Isar (reemplaza Hive)
  isar_community: ^3.3.2
  isar_community_flutter_libs: ^3.3.2
  
  # Path provider (necesario para Isar)
  path_provider: ^2.1.2
  
  # Routing
  go_router: ^12.1.3

dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.2
  build_runner: ^2.4.7
  isar_community_generator: ^3.3.2
```

### Diferencias Hive vs Isar en pubspec

| Paquete | Hive | Isar 3.x |
|---------|------|----------|
| Runtime | `hive`, `hive_flutter` | `isar_community`, `isar_community_flutter_libs` |
| Generator | `hive_generator` | `isar_community_generator` |
| Path | No necesita | `path_provider` |

### Notas Importantes

1. **Generación de código**: Con Isar, después de definir tus modelos, ejecuta:
   ```bash
   dart run build_runner build
   ```
   Esto generará el archivo `user_model.g.dart`.

2. **Testing**: Para tests unitarios con Isar, necesitas inicializar Isar Core:
   ```dart
   setUpAll(() async {
     await Isar.initializeIsarCore(download: true);
   });
   ```
   Ejecuta los tests con: `flutter test -j 1` (evita paralelismo).

3. **Instancias múltiples**: Isar permite múltiples bases de datos con el parámetro `name`:
   ```dart
   final isar = await Isar.open([Schema], directory: dir.path, name: 'mi_db');
   ```

---

**¡Feliz codificación! La clave es la disciplina para mantener las fronteras entre capas.**
