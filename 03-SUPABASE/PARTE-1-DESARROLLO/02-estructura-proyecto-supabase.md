# 02 - Estructura del Proyecto Supabase

> Conoce la estructura de archivos y carpetas que Supabase genera y cómo organizar tu proyecto para escalabilidad.

---

## 🎯 Objetivos de este archivo

- Entender cada archivo y carpeta del proyecto Supabase
- Conocer las mejores prácticas de organización
- Preparar la base para migraciones y testing

---

## 1. Estructura general

```
supabase/
├── .temp/                      # Archivos temporales de la CLI
│   ├── cli-latest             # Versión del CLI
│   ├── project-ref           # Referencia del proyecto
│   └── postgres-version      # Versión de PostgreSQL
│
├── config.toml                # Configuración principal
│
├── migrations/                # Migraciones de esquema (SQL)
│   ├── 20251122174827_create_first_table.sql
│   └── ...
│
├── seed.sql                  # Datos iniciales
│
├── tests/                    # Tests de base de datos (pgTAP)
│   └── example_test.sql
│
├── .branches/               # Ramas de desarrollo (branches)
│   └── _current_branch      # Puntero a la rama actual
│
└── .gitignore              # Ignorar archivos sensibles
```

---

## 2. Archivo: config.toml

Este es el archivo de configuración principal. Contiene la configuración de todos los servicios de Supabase.

### Secciones principales

| Sección | Descripción | Puertos típicos |
|---------|-------------|-----------------|
| `[api]` | API REST y GraphQL | 54321 |
| `[db]` | PostgreSQL | 54322 |
| `[studio]` | Supabase Studio (UI) | 54323 |
| `[inbucket]` | Servidor de email local | 54324 |
| `[storage]` | Storage API | - |
| `[auth]` | Authentication | - |
| `[realtime]` | WebSockets | - |
| `[edge_runtime]` | Edge Functions | 8083 |
| `[analytics]` | Analytics | 54327 |

### Configuración personalizada (ejemplo)

```toml
project_id = "mi-proyecto-flutter"

[api]
enabled = true
port = 54321
schemas = ["public", "graphql_public"]
max_rows = 1000

[db]
port = 54322
major_version = 17

[studio]
enabled = true
port = 54323

[auth]
enabled = true
site_url = "http://127.0.0.1:3000"
additional_redirect_urls = ["https://127.0.0.1:3000"]
jwt_expiry = 3600
enable_signup = true

[auth.email]
enable_signup = true
double_confirm_changes = true
enable_confirmations = false

[storage]
enabled = true
file_size_limit = "50MiB"

[edge_runtime]
enabled = true
deno_version = 2
```

### ¿Qué significa cada configuración?

| Configuración | Descripción |
|--------------|-------------|
| `project_id` | Identificador único del proyecto |
| `schemas` | Esquemas expuestos en la API |
| `jwt_expiry` | Tiempo de expiración del token JWT (segundos) |
| `enable_signup` | Permite registro de nuevos usuarios |
| `file_size_limit` | Tamaño máximo de archivos en Storage |
| `deno_version` | Versión de Deno para Edge Functions |

---

## 3. Carpeta: migrations/

Las migraciones contienen los cambios del esquema de base de datos. Cada archivo representa un cambio/version.

### Formato de nombres

```
YYYYMMDDHHMMSS_nombre_descriptivo.sql
```

Ejemplos:
- `20251122174827_create_users_table.sql`
- `20251130175303_add_profile_picture_column.sql`
- `20251207144155_delete_user_cascade.sql`

### Estructura de una migración

```sql
-- Nombre: Crear tabla de usuarios
-- Fecha: 2025-11-22

-- UP: Aplicar cambios
CREATE TABLE public.users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Política de acceso
CREATE POLICY "Usuarios pueden ver su propio perfil"
    ON public.users FOR SELECT
    USING (auth.uid() = id);

-- DOWN: Revertir cambios (opcional, para rollback)
-- DROP TABLE public.users;
```

### Mejores prácticas

1. **Nombrado descriptivo**: `20251122174827_agregar_campo_telefono_a_usuarios.sql`
2. **Una migración por cambio**: No combine múltiples cambios
3. **Idempotente**: La migración puede ejecutarse múltiples veces sin errores
4. **Reversible**: Sempre incluya la sección DOWN (o al menos la idea)

---

## 4. Archivo: seed.sql

El archivo `seed.sql` contiene datos iniciales que se insertan cuando ejecutas `supabase db reset`.

### Ejemplo de seeds

```sql
-- Seed: Datos iniciales para desarrollo

-- Insertar usuario de prueba
INSERT INTO public.users (email, full_name)
VALUES 
    ('admin@example.com', 'Admin User'),
    ('test@example.com', 'Test User');

-- Insertar configuraciones iniciales
INSERT INTO public.settings (key, value)
VALUES 
    ('app_name', 'Mi Aplicación'),
    ('theme', 'light');
```

### Cuándo usar seeds

- Datos de referencia (países, categorías)
- Usuario administrador por defecto
- Configuraciones iniciales
- Datos de prueba para desarrollo

### Alternativa: seeds por entorno

Para diferentes datos según el entorno, puedes tener múltiples archivos y configurar en `config.toml`:

```toml
[db.seed]
enabled = true
sql_paths = ["./seed.sql"]  # Cambiar según entorno
```

---

## 5. Carpeta: tests/

Contiene tests de base de datos usando **pgTAP** (framework de testing para PostgreSQL).

### Estructura de un test

```sql
-- Test: Verificar que la tabla usuarios existe

BEGIN;

SELECT plan(1);

-- Test: La tabla users debe existir
SELECT has_table('public', 'users', 'La tabla users debe existir');

SELECT * FROM finish();
ROLLBACK;
```

### Tests más comunes

```sql
-- Test: Verificar columnas
SELECT has_column('public', 'users', 'email', 'Debe tener columna email');

-- Test: Verificar constraints
SELECT col_is_pk('public', 'users', 'id', 'id debe ser primary key');

-- Test: Verificar datos
SELECT is(
    (SELECT COUNT(*) FROM public.users),
    2,
    'Debe haber exactamente 2 usuarios'
);

-- Test: Verificar función
SELECT function_returns('public', 'generate_user_id', 'text');
```

### Ejecutar tests

```bash
# En local
supabase test db

# En CI/CD (GitHub Actions)
supabase start
supabase test db
```

---

## 6. Carpeta: .branches/

Maneja ramas de desarrollo (similar a git branches) para Supabase.

```bash
# Crear una rama de desarrollo
supabase branch create develop

# Cambiar a una rama
supabase branch switch develop

# Ver ramas existentes
supabase branch list

# Eliminar una rama
supabase branch delete develop
```

### Uso típico

- `main` → producción
- `develop` → desarrollo
- Ramas específicas por feature

---

## 7. Archivo: .gitignore

```gitignore
# Supabase
.supabase/
supabase/.temp/

# Archivos de desarrollo local
.env
.env.local

# IDE
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## 8. Organización avanzada

### Estructura para proyectos grandes

```
supabase/
├── config.toml
├── seed.sql
├── migrations/
│   ├── 001_initial_schema/
│   │   ├── 20251122174827_create_users.sql
│   │   └── 20251123122107_create_profiles.sql
│   ├── 002_auth/
│   │   └── ...
│   └── 003_features/
│       └── ...
├── tests/
│   ├── 01_users/
│   │   ├── user_constraints_test.sql
│   │   └── user_policies_test.sql
│   └── 02_profiles/
│       └── ...
└── functions/
    └── mi-edge-function/
        ├── index.ts
        └── deno.json
```

### Separar migrations por contexto

```
migrations/
├── auth/
│   └── 20251122174827_enable_auth.sql
├── storage/
│   └── 20251125120000_create_buckets.sql
└── features/
    └── wellness/
        └── 20251201000000_wellness_tables.sql
```

### Volúmenes locales (datos persistentes)

Para no perder la BD local al hacer `supabase stop`:

```toml
# config.toml
[db]
port = 54322
major_version = 17

[db.volumes]
enabled = true
path = "./volumes/db"
```

```gitignore
# .gitignore — ignorar datos locales pero no la carpeta
supabase/volumes/
!supabase/volumes/.gitkeep
```

---

## ✅ Checklist de estructura

- [ ] `config.toml` configurado con los valores correctos
- [ ] Primera migración creada
- [ ] Seeds básicos definidos
- [ ] Tests de base de datos iniciados
- [ ] Edge Functions scaffolded (si aplica)
- [ ] Volúmenes configurados para persistencia local
- [ ] `.gitignore` configurado

---

## 📚 Recursos

- [Supabase Config Reference](https://supabase.com/docs/guides/local-development/cli/config)
- [pgTAP Documentation](https://pgtap.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Siguiente**: [03-makefile-integrado.md](./03-makefile-integrado.md)