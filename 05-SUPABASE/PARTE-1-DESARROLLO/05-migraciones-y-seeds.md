# 05 - Migraciones y Seeds

> Aprende a crear, gestionar y aplicar migraciones de base de datos, junto con los datos iniciales (seeds) para tu proyecto Supabase.

---

## 🎯 Objetivos de este archivo

- Crear migraciones correctamente estructuradas
- Aplicar y revertir migraciones
- Gestionar seeds para diferentes entornos
- Mantener un historial limpio de cambios

---

## 1. Conceptos fundamentales

### ¿Qué es una migración?

Una migración es un archivo SQL que describe un cambio en el esquema de la base de datos. Cada migración es:
- **Idempotente**: Se puede ejecutar múltiples veces sin errores
- **Versionada**: Tiene un nombre único con timestamp
- **Reversible**: Incluye la instrucción para revertir (opcional)

### ¿Qué es un seed?

Un seed es un script SQL que inserta datos iniciales después de aplicar las migraciones. Se usa para:
- Datos de referencia (países, categorías)
- Usuario administrador por defecto
- Configuraciones iniciales
- Datos de prueba para desarrollo

---

## 2. Crear una migración

### Método 1: Usando el Makefile

```bash
make db-new-migration name=create_users_table
```

### Método 2: Directamente con CLI

```bash
supabase migration new create_users_table
```

Esto crea un archivo en `supabase/migrations/` con el formato:
```
supabase/migrations/20251122174827_create_users_table.sql
```

### Estructura de una migración completa

```sql
-- Nombre: Crear tabla de usuarios
-- Descripción: Tabla principal para usuarios autenticados
-- Fecha: 2025-11-22

-- ==============================================================================
-- UP - Aplicar cambios
-- ==============================================================================

-- Crear tabla
CREATE TABLE public.users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agregar índice para búsquedas por email
CREATE INDEX idx_users_email ON public.users(email);

-- Agregar índice para búsquedas por fecha
CREATE INDEX idx_users_created_at ON public.users(created_at DESC);

-- Habilitar Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Política de lectura: usuarios pueden ver su propio perfil
CREATE POLICY "users_select_own" ON public.users
    FOR SELECT USING (auth.uid() = id);

-- Política de actualización: usuarios pueden actualizar su propio perfil
CREATE POLICY "users_update_own" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- Política de inserción: cualquier usuario autenticado puede crear perfil inicial
CREATE POLICY "users_insert_authenticated" ON public.users
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- ==============================================================================
-- DOWN - Revertir cambios (opcional pero recomendado)
-- ==============================================================================

DROP POLICY IF EXISTS "users_select_own" ON public.users;
DROP POLICY IF EXISTS "users_update_own" ON public.users;
DROP POLICY IF EXISTS "users_insert_authenticated" ON public.users;
DROP INDEX IF EXISTS idx_users_email;
DROP INDEX IF EXISTS idx_users_created_at;
DROP TABLE IF EXISTS public.users;
```

---

## 3. Tipos de migraciones comunes

### Crear tabla

```sql
CREATE TABLE public.wellness_contents (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT NOT NULL,
    image_url TEXT,
    is_premium BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_wellness_category ON public.wellness_contents(category);
```

### Agregar columna

```sql
ALTER TABLE public.users 
ADD COLUMN IF NOT EXISTS phone TEXT,
ADD COLUMN IF NOT EXISTS bio TEXT;

-- Actualizar默认值 para registros existentes
UPDATE public.users 
SET phone = '', bio = '' 
WHERE phone IS NULL OR bio IS NULL;
```

### Modificar columna

```sql
-- Cambiar tipo de columna
ALTER TABLE public.users 
ALTER COLUMN full_name TYPE VARCHAR(255);

-- Hacer columna nullable
ALTER TABLE public.users 
ALTER COLUMN avatar_url DROP NOT NULL;

-- Agregar valor por defecto
ALTER TABLE public.users 
ALTER COLUMN is_active SET DEFAULT true;
```

### Crear relación (foreign key)

```sql
-- Agregar columna para foreign key
ALTER TABLE public.profiles 
ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE;

-- Crear índice para la foreign key
CREATE INDEX idx_profiles_user_id ON public.profiles(user_id);

-- Agregar constraint de unicidad
ALTER TABLE public.profiles 
ADD CONSTRAINT unique_user_id UNIQUE (user_id);
```

### Crear función (stored procedure)

```sql
-- Función para obtener usuario por ID
CREATE OR REPLACE FUNCTION public.get_user_by_id(user_id UUID)
RETURNS TABLE(
    id UUID,
    email TEXT,
    full_name TEXT,
    avatar_url TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id,
        u.email,
        u.full_name,
        u.avatar_url
    FROM public.users u
    WHERE u.id = user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### Crear trigger

```sql
-- Trigger para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a la tabla
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();
```

---

## 4. Aplicar migraciones

### Desarrollo local

```bash
# Aplicar todas las migraciones pendientes
supabase db reset

# O aplicar sin hacer reset (más rápido para desarrollo)
supabase db push
```

### Diferencias entre reset y push

| Comando | Qué hace | Cuándo usarlo |
|---------|----------|---------------|
| `db push` | Aplica migraciones nuevas | Desarrollo rápido |
| `db reset` | Borra BD, aplica todo desde cero | Necesitas un estado limpio |

### Producció

```bash
# Desde local, push a Supabase remoto
supabase db push --project-ref tu-project-ref

# O usando el Makefile
make db-push
```

---

## 5. Seeds

### Estructura del seed.sql

```sql
-- Seeds: Datos iniciales para desarrollo
-- Ejecutar después de aplicar migraciones con `supabase db reset`

-- ==============================================================================
-- USUARIOS DE PRUEBA
-- ==============================================================================

-- Insertar usuarios de prueba (sin contraseña, solo para desarrollo)
INSERT INTO public.users (email, full_name, avatar_url)
VALUES 
    ('admin@example.com', 'Admin User', 'https://example.com/admin.png'),
    ('test@example.com', 'Test User', 'https://example.com/test.png');

-- ==============================================================================
-- CONTENIDOS DE BIENESTAR (EJEMPLO)
-- ==============================================================================

INSERT INTO public.wellness_contents (title, content, category, is_premium)
VALUES 
    ('Meditación matutina', 'Aprende a comenzar tu día con claridad...', 'meditation', false),
    ('Técnicas de respiración', '3 técnicas de respiración para reducir el estrés...', 'breathing', false),
    ('Guía de alimentación saludable', 'Plan de alimentación para una vida equilibrada...', 'nutrition', true);

-- ==============================================================================
-- CONFIGURACIONES
-- ==============================================================================

INSERT INTO public.settings (key, value)
VALUES 
    ('app_name', 'Mi App de Bienestar'),
    ('version', '1.0.0'),
    ('maintenance_mode', 'false');
```

### Seeds por entorno

Para diferentes datos según el entorno, puedes tener múltiples archivos:

```
supabase/
├── seed.sql              # Datos base (siempre se ejecuta)
├── seed-dev.sql         # Datos específicos de desarrollo
├── seed-prod.sql        # Datos específicos de producción
```

Y en `config.toml`:

```toml
[db.seed]
enabled = true
sql_paths = ["./seed.sql", "./seed-dev.sql"]  # Para desarrollo
```

---

## 6. Workflow de migraciones

### Flujo recomendado

```
1. Crear migración local
   └─ make db-new-migration name=add_new_table

2. Editar el archivo SQL
   └─ Escribir las sentencias UP y DOWN

3. Aplicar localmente
   └─ make db-reset

4. Probar funcionalidad
   └─ Ejecutar tests, verificar en app

5. Si hay errores
   └─ Corregir migración o crear nueva migración

6. Environment checked
   └─ make db-push

7. Commit y push
   └─ git add supabase/migrations/ && git commit -m "feat: add new table"
```

### En equipos

```bash
# Antes de empezar a trabajar
git pull
make db-reset  # Obtener últimas migraciones

# Después de hacer cambios
git add supabase/migrations/
git commit -m "feat: add new feature tables"
git push
```

---

## 7. Testing de migraciones

### Tests de base de datos (pgTAP)

```sql
-- test: Verificar que la tabla users existe
BEGIN;

SELECT plan(1);
SELECT has_table('public', 'users', 'La tabla users debe existir');

SELECT * FROM finish();
ROLLBACK;
```

### Ejecutar tests

```bash
# Local
supabase test db

# En CI/CD
supabase start
supabase test db
```

---

## 8. Errores comunes y soluciones

### "relation already exists"

```sql
-- Usar IF NOT EXISTS o IF EXISTS
CREATE TABLE IF NOT EXISTS public.users (...);
DROP TABLE IF EXISTS public.users;
```

### "column does not exist"

```sql
-- Agregar columna primero
ALTER TABLE public.users ADD COLUMN IF NOT EXISTS new_column TEXT;
```

### "duplicate key value violates unique constraint"

```sql
-- Usar ON CONFLICT
INSERT INTO public.users (email, name)
VALUES ('test@test.com', 'Test')
ON CONFLICT (email) DO NOTHING;
```

### "migration failed"

```bash
# Ver el error específico
supabase db reset --debug

# Si la migración está corrupta
# 1. Eliminar la migración problemática
# 2. Crear nueva migración con la corrección
# 3. hacer db reset
```

---

## 9. Buenas prácticas

### 1. Una migración por cambio

```sql
-- ❌ MAL: Múltiples cambios en una migración
CREATE TABLE ...;
ALTER TABLE ...;
CREATE INDEX ...;

-- ✅ BUENO: Una migración por cada cambio
-- 01_create_users_table.sql
-- 02_add_phone_to_users.sql  
-- 03_create_indexes_for_users.sql
```

### 2. Nombres descriptivos

```sql
-- ❌ MAL
20251122.sql
migration1.sql

-- ✅ BUENO
20251122174827_create_users_table.sql
20251125120000_add_phone_to_users.sql
```

### 3. Incluir siempre DOWN

```sql
-- Sempre incluir cómo revertir
-- DOWN: Revertir cambios
DROP TABLE IF EXISTS public.users;
```

### 4. No modificar migraciones existentes

```sql
-- ❌ MAL: Editar migración ya aplicada
-- Si necesitas cambiar, crear nueva migración
-- ✅ BUENO: Crear nueva migración con ALTER
```

---

## ✅ Checklist de migraciones

- [ ] Nueva migración creada con nombre descriptivo
- [ ] Sentencias UP completas
- [ ] Sentencias DOWN incluidas
- [ ] Probada localmente con `db reset`
- [ ] Tests de base de datos pasando
- [ ] Commiteada al repositorio
- [ ] Aplicada a producción (`db push`)

---

## 📚 Recursos

- [Supabase Migrations](https://supabase.com/docs/guides/migrations)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [pgTAP Testing](https://pgtap.org/)

---

**Siguiente**: [06-integracion-flutter.md](./06-integracion-flutter.md)