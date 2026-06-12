# 07 - Testing Local con Supabase

> Aprende a escribir y ejecutar tests de base de datos usando pgTAP, y cómo integrar los tests de Supabase en tu flujo de CI/CD.

---

## 🎯 Objetivos de este archivo

- Entender el framework pgTAP para testing de PostgreSQL
- Escribir tests para validar el esquema de la base de datos
- Ejecutar tests localmente y en CI/CD
- Integrar tests de Supabase con tests de Flutter

---

## 1. Conceptos de pgTAP

### ¿Qué es pgTAP?

pgTAP es un framework de testing para PostgreSQL que permite escribir tests en SQL puro. Es similar a JUnit o pytest pero para bases de datos.

### ¿Por qué usar pgTAP?

- **Validación del esquema**: Verificar que tablas, columnas, constraints existen
- **Validación de datos**: Verificar que los datos se insertan correctamente
- **Validación de funciones**: Probar stored procedures y funciones
- **Validación de políticas RLS**: Verificar que las políticas de seguridad funcionan

---

## 2. Estructura de un test pgTAP

### Anatomía básica

```sql
-- Nombre del test: Verificar que la tabla users existe
BEGIN;

-- Plan: número de tests que we'll ejecutar
SELECT plan(1);

-- Test: La tabla users debe existir
SELECT has_table('public', 'users', 'La tabla users debe existir');

-- Finalizar tests
SELECT * FROM finish();

ROLLBACK;
```

### Componentes

| Componente | Descripción |
|------------|-------------|
| `BEGIN` / `ROLLBACK` | Envoltura de transacción para no afectar la BD real |
| `SELECT plan(n)` | Declara el número de tests |
| `has_table()`, `has_column()`, etc. | Funciones de aserción |
| `SELECT * FROM finish()` | Finaliza y reporta resultados |

---

## 3. Tests básicos de esquema

### Verificar que una tabla existe

```sql
BEGIN;
SELECT plan(1);
SELECT has_table('public', 'users', 'La tabla users debe existir');
SELECT * FROM finish();
ROLLBACK;
```

### Verificar columnas

```sql
BEGIN;
SELECT plan(3);

-- La tabla users debe tener columna email
SELECT has_column('public', 'users', 'email', 'Debe tener columna email');

-- La columna email debe ser de tipo text
SELECT col_type_is('public', 'users', 'email', 'text', 'email debe ser text');

-- La columna email debe ser unique
SELECT col_is_unique('public', 'users', 'email', 'email debe ser unique');

SELECT * FROM finish();
ROLLBACK;
```

### Verificar constraints

```sql
BEGIN;
SELECT plan(4);

-- id debe ser primary key
SELECT col_is_pk('public', 'users', 'id', 'id debe ser primary key');

-- created_at debe tener default
SELECT col_has_default('public', 'users', 'created_at', 'created_at debe tener default');

-- email debe ser NOT NULL
SELECT col_not_null('public', 'users', 'email', 'email debe ser NOT NULL');

-- Verificar foreign key
SELECT fk_has_column(
    'public', 'profiles', 'user_id',
    'public', 'users', 'id',
    'profiles.user_id debe referenciar users.id'
);

SELECT * FROM finish();
ROLLBACK;
```

---

## 4. Tests de políticas RLS

### Verificar que RLS está habilitado

```sql
BEGIN;
SELECT plan(1);
SELECT is(
    (SELECT relrowsecurity FROM pg_class WHERE relname = 'users'),
    true,
    'RLS debe estar habilitado en users'
);
SELECT * FROM finish();
ROLLBACK;
```

### Verificar políticas existentes

```sql
BEGIN;
SELECT plan(2);

-- Debe existir política de SELECT
SELECT has_policy(
    'public', 'users', 'users_select_own',
    'Debe existir política users_select_own'
);

-- La política debe ser de tipo SELECT
SELECT pol_is_enforced(
    'public', 'users', 'users_select_own', 'SELECT',
    'users_select_own debe ser de tipo SELECT'
);

SELECT * FROM finish();
ROLLBACK;
```

---

## 5. Tests de funciones

### Verificar que una función existe

```sql
BEGIN;
SELECT plan(1);
SELECT function_exists('public', 'get_user_by_id', 'La función get_user_by_id debe existir');
SELECT * FROM finish();
ROLLBACK;
```

### Verificar tipo de retorno

```sql
BEGIN;
SELECT plan(1);
SELECT function_returns(
    'public', 'get_user_by_id', 'SETOF RECORD',
    'get_user_by_id debe retornar SETOF RECORD'
);
SELECT * FROM finish();
ROLLBACK;
```

---

## 6. Tests de datos

### Verificar datos insertsdos

```sql
BEGIN;
SELECT plan(1);

-- Insertar datos de prueba
INSERT INTO public.users (email, full_name)
VALUES ('test@test.com', 'Test');

-- Verificar que se insertó correctamente
SELECT is(
    (SELECT COUNT(*) FROM public.users WHERE email = 'test@test.com'),
    1,
    'Debe haber exactamente 1 usuario con email test@test.com'
);

-- Limpiar
DELETE FROM public.users WHERE email = 'test@test.com';

SELECT * FROM finish();
ROLLBACK;
```

### Verificar constraints de datos

```sql
BEGIN;
SELECT plan(1);

-- Intentar insertar email duplicado (debería fallar)
SELECT throws(
    $$INSERT INTO public.users (email, full_name) VALUES ('dup@test.com', 'Test')$$,
    '23505',  -- Código de error para unique violation
    'Insertar email duplicado debe lanzar error'
);

SELECT * FROM finish();
ROLLBACK;
```

---

## 7. Ejecutar tests

### Local (desde terminal)

```bash
# Ejecutar todos los tests
supabase test db

# Con verbose
supabase test db -v

# Ejecutar un archivo específico
supabase test db supabase/tests/my_test.sql
```

### Desde Makefile

```makefile
.PHONY: db-test
db-test: deps-check ## Ejecutar tests de base de datos
	$(SUPABASE) test db
```

---

## 8. Integración con CI/CD

### GitHub Actions workflow

```yaml
name: Supabase Tests

on:
  pull_request:
    paths:
      - supabase/**

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Install Supabase CLI
        uses: supabase/setup-cli@v1
        with:
          version: latest
      
      - name: Start Supabase
        run: supabase start
      
      - name: Run pgTAP tests
        run: supabase test db
      
      - name: Lint migrations
        run: supabase db lint --local
      
      - name: Stop Supabase
        if: always()
        run: supabase stop
```

### Workflow completo para Flutter + Supabase

```yaml
name: CI

on:
  push:
    branches: [dev, main]
  pull_request:
    types: [opened, synchronize]

jobs:
  flutter-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./github/actions/setup-flutter-env
      
      - name: Run Flutter tests
        run: make test
      
      - name: Run coverage
        run: make coverage

  supabase-test:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: supabase/setup-cli@v1
        with:
          version: latest
      
      - name: Start local Supabase
        run: supabase start
      
      - name: Run database tests
        run: supabase test db
      
      - name: Lint schema
        run: supabase db lint --local
```

---

## 9. Testing de integración con Supabase local

### Flujo de integración Flutter + Supabase

```makefile
.PHONY: integration-supabase
integration-supabase: deps-check env-test-check
	@echo "==> Running integration tests with local Supabase"
	@set -euo pipefail; \
	backup=.env.bak.integration; \
	[ -f .env ] && cp .env $$backup; \
	cp .env.test .env; \
	cleanup() { \
		[ -f $$backup ] && mv $$backup .env || rm -f .env; \
		$(SUPABASE) stop; \
	}; \
	trap cleanup EXIT; \
	$(SUPABASE) start; \
	$(FLUTTER) test integration_test/app_test_suite.dart
```

### Configurar .env.test para integración

```bash
# .env.test
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 10. Estructura de archivos de test

### Organización recomendada

```
supabase/
├── migrations/
│   └── ...
├── tests/
│   ├── 01_schema/
│   │   ├── 01_users_table_test.sql
│   │   ├── 02_profiles_table_test.sql
│   │   └── 03_rls_policies_test.sql
│   ├── 02_functions/
│   │   ├── 01_user_functions_test.sql
│   │   └── 02_utility_functions_test.sql
│   └── 03_integration/
│       ├── 01_user_flow_test.sql
│       └── 02_auth_flow_test.sql
└── seed.sql
```

### Ejemplo de test con múltiples assertions

```sql
-- Test: Validar estructura completa de la tabla users
BEGIN;

SELECT plan(7);

-- 1. Tabla debe existir
SELECT has_table('public', 'users', 'Tabla users debe existir');

-- 2. Columna id debe existir y ser UUID
SELECT has_column('public', 'users', 'id', 'Columna id debe existir');
SELECT col_type_is('public', 'users', 'id', 'uuid', 'id debe ser uuid');

-- 3. Columna email debe existir y ser text
SELECT has_column('public', 'users', 'email', 'Columna email debe existir');
SELECT col_type_is('public', 'users', 'email', 'text', 'email debe ser text');

-- 4. email debe ser unique
SELECT col_is_unique('public', 'users', 'email', 'email debe ser unique');

-- 5. created_at debe tener default
SELECT col_has_default('public', 'users', 'created_at', 'created_at debe tener default');

-- 6. RLS debe estar habilitado
SELECT is(
    (SELECT relrowsecurity FROM pg_class WHERE relname = 'users'),
    true,
    'RLS debe estar habilitado'
);

SELECT * FROM finish();
ROLLBACK;
```

---

## 11. Errores comunes

### "test did not pass"

```sql
-- Error: La tabla no existe
-- Verificar que migrations se aplicaron
-- Ejecutar: supabase db reset
```

### "no tests found"

```sql
-- Error: No se encontró ningún test
-- Verificar que los archivos están en supabase/tests/
-- Verificar extensión .sql
```

### "function finish() does not exist"

```sql
-- Error: pgTAP no está instalado
-- pgTAP se instala automáticamente con supabase start
-- Verificar con: SELECT * FROM pg_extension WHERE extname = 'pgtap';
```

---

## 12. Buenas prácticas

### 1. Tests pequeños y específicos

```sql
-- ✅ Un test por tabla/policy
-- ❌ Un test que lo verifica todo
```

### 2. Nombres descriptivos

```sql
-- ✅ "users table must have email column"
-- ❌ "test1"
```

### 3. Always include ROLLBACK

```sql
BEGIN;
-- tests...
ROLLBACK;  -- Importante para no contaminar la BD
```

### 4. Ejecutar tests antes de cada commit

```bash
make db-test
```

---

## ✅ Checklist de testing

- [ ] pgTAP instalado y funcionando
- [ ] Tests de esquema creados para cada tabla
- [ ] Tests de RLS creados para cada tabla
- [ ] Tests de funciones creados
- [ ] Tests de integración creados
- [ ] Tests ejecutándose en CI/CD
- [ ] Tests de integración Flutter + Supabase funcionando

---

## 📚 Recursos

- [pgTAP Documentation](https://pgtap.org/)
- [Supabase Testing Guide](https://supabase.com/docs/guides/testing)
- [PostgreSQL Extensions](https://www.postgresql.org/docs/17/contrib.html)

---

## 🎯 Fin de la Parte 1

Has completado la sección de Supabase Local. Ahora sabes:
- ✅ Configurar Supabase desde cero
- ✅ Estructurar el proyecto
- ✅ Usar el Makefile
- ✅ Gestionar variables de entorno
- ✅ Crear y aplicar migraciones
- ✅ Integrar Supabase con Flutter
- ✅ Escribir tests de base de datos

**Siguiente**: [Parte 2: Producción](./../PARTE-2-PRODUCTION/01-opciones-hosting.md)