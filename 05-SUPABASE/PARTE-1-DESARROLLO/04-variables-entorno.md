# 04 - Variables de Entorno

> Aprende a gestionar las variables de entorno de forma segura y estructurada para diferentes entornos de tu proyecto Flutter con Supabase.

---

## 🎯 Objetivos de este archivo

- Crear y gestionar archivos .env para diferentes entornos
- Entender qué variables son necesarias para Supabase
- Implementar validación automática de variables
- Mantener la seguridad del proyecto

---

## 1. Estructura de archivos de entorno

### Archivos típicos en un proyecto

```
.env                      # Desarrollo local (NO commitear)
.env.example             # Template para desarrolladores (SI commitear)
.env.test                # Testing e integración (NO commitear)
.env.prod                # Producción (NO commitear, gestionar via secrets)
```

### Propósito de cada archivo

| Archivo | Propósito | ¿Commitear? |
|---------|-----------|--------------|
| `.env` | Variables locales de desarrollo | NO |
| `.env.example` | Template con variables requeridas | SI |
| `.env.test` | Variables para tests de integración | NO |
| `.env.prod` | Variables de producción | NO |

---

## 2. Variables esenciales de Supabase

### Minimum required

```bash
# URL del proyecto Supabase (obtener de Supabase Dashboard)
SUPABASE_URL=http://127.0.0.1:54321

# Anon Key pública (obtener de Supabase Dashboard → Settings → API)
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Variables opcionales

```bash
# URL de API REST personalizada (si usas Edge Functions o REST API)
REST_API_BASE_URL=http://192.168.0.127:3000

# Service Role Key (solo para backend/server-side, NUNCA en Flutter)
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Para producción
SUPABASE_DB_PASSWORD=...  # Password de la base de datos
```

### Cómo obtener las variables desde Supabase

1. Ve a **Supabase Dashboard**
2. Selecciona tu proyecto
3. Ve a **Settings** (icono de engranaje)
4. **API**: Copia `Project URL` y `anon public` key
5. **Database**: Copia las credenciales de conexión

---

## 3. Archivo .env.example (plantilla)

Este archivo debe ser commitado y sirve como referencia:

```bash
# ==============================================================================
# CONFIGURACIÓN DE SUPABASE
# ==============================================================================

# URL del proyecto (obtener de Supabase Dashboard → Settings → General)
SUPABASE_URL=

# Anon Key pública (obtener de Supabase Dashboard → Settings → API → anon key)
SUPABASE_ANON_KEY=

# ==============================================================================
# CONFIGURACIÓN ADICIONAL (OPCIONAL)
# ==============================================================================

# URL de API REST personalizada (si usas Edge Functions)
# REST_API_BASE_URL=

# ==============================================================================
# NOTAS:
# ==============================================================================
# 1. Copia este archivo como .env y completa los valores
# 2. NUNCA commitear .env al repositorio (ya está en .gitignore)
# 3. Para producción, usa los secrets de GitHub o tu proveedor de hosting
# 4. Las variables aquí son para desarrollo local
```

---

## 4. Archivo .env (desarrollo local)

Este es tu archivo personal de desarrollo. **NUNCA lo comitees**.

```bash
# Desarrollo local - NO COMMITEAR
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0
REST_API_BASE_URL=http://192.168.0.127:3000
```

### Cómo configuran las apps Flutter las variables

```dart
// lib/main.dart o lib/core/config/supabase_config.dart

import 'package:supabase_flutter/supabase_flutter.dart';

Future<void> initializeSupabase() async {
  await Supabase.initialize(
    url: const String.fromEnvironment('SUPABASE_URL'),
    anonKey: const String.fromEnvironment('SUPABASE_ANON_KEY'),
    // Para desarrollo local
    debug: true,
  );
}
```

### Con flutter_dotenv (alternativa)

```yaml
# pubspec.yaml
dependencies:
  flutter_dotenv: ^5.1.0
```

```dart
// main.dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

Future<void> main() async {
  await dotenv.load(fileName: ".env");
  
  final supabaseUrl = dotenv.env['SUPABASE_URL'];
  final supabaseAnonKey = dotenv.env['SUPABASE_ANON_KEY'];
  
  await Supabase.initialize(
    url: supabaseUrl!,
    anonKey: supabaseAnonKey!,
  );
  
  runApp(const MyApp());
}
```

---

## 5. Variables para diferentes entornos

### Desarrollo local (.env)

```bash
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Testing (.env.test)

```bash
SUPABASE_URL=http://127.0.0.1:54321
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
# Mismas keys que desarrollo para tests locales
```

### Producción (.env)

```bash
# Valores reales de Supabase Cloud o tu instancia self-hosted
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 6. Script de validación de variables

El script `scripts/check_env.sh` verifica que las variables requeridas existan:

```bash
#!/bin/bash
set -e

ENV_FILE=$1

if [ -z "$ENV_FILE" ]; then
    echo "Usage: $0 <env_file>"
    exit 1
fi

echo "==> Validando $ENV_FILE"

# Verificar que el archivo existe
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Missing $ENV_FILE file in root."
    exit 1
fi

# Verificar SUPABASE_URL
if ! grep -q "^SUPABASE_URL=" "$ENV_FILE"; then
    echo "Error: Missing SUPABASE_URL in $ENV_FILE"
    exit 1
fi

# Verificar SUPABASE_ANON_KEY
if ! grep -q "^SUPABASE_ANON_KEY=" "$ENV_FILE"; then
    echo "Error: Missing SUPABASE_ANON_KEY in $ENV_FILE"
    exit 1
fi

# Verificar variable opcional
if grep -q "^REST_API_BASE_URL=" "$ENV_FILE"; then
    echo "Info: REST_API_BASE_URL presente"
else
    echo "Info: REST_API_BASE_URL no encontrada (opcional)"
fi

echo "✅ Environment $ENV_FILE válido"
```

### Hacer ejecutable el script

```bash
chmod +x scripts/check_env.sh
```

### Uso en Makefile

```makefile
.PHONY: env-check
env-check:
	@./scripts/check_env.sh .env

.PHONY: env-test-check
env-test-check:
	@./scripts/check_env.sh .env.test
```

---

## 7. Integración con GitHub Secrets

### Para CI/CD

En GitHub, ve a **Settings → Secrets and variables → Actions** y añade:

| Secret | Descripción |
|--------|-------------|
| `SUPABASE_URL` | URL de producción |
| `SUPABASE_ANON_KEY` | Anon key de producción |
| `SUPABASE_ACCESS_TOKEN` | Token de Supabase CLI |
| `SUPABASE_PROJECT_ID` | ID del proyecto |
| `SUPABASE_DB_PASSWORD` | Password de la base de datos |

### En workflows

```yaml
- name: Build APK
  run: |
    flutter build apk --release \
      --dart-define=SUPABASE_URL=${{ secrets.SUPABASE_URL }} \
      --dart-define=SUPABASE_ANON_KEY=${{ secrets.SUPABASE_ANON_KEY }}
```

---

## 8. Buenas prácticas de seguridad

### NUNCA hacer

```bash
# ❌ NO commitear keys reales
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# ❌ NO hardcodear en código
final url = 'https://xxx.supabase.co'; // NO

# ❌ NO exponer en logs
print('API Key: $apiKey'); // NO
```

### SIEMPRE hacer

```bash
# ✅ USAR variables de entorno
SUPABASE_URL=$SUPABASE_URL

# ✅ USAR .gitignore
# Verificar que .env esté ignorado

# ✅ USAR secrets en CI/CD
# GitHub Secrets, etc.

# ✅ ROTAR keys regularmente
# Cambiar keys en Supabase Dashboard → Settings → API
```

### Verificar .gitignore

```gitignore
# Environment
.env
.env.local
.env.*.local

# No ignorar el template
!.env.example
```

---

## 9. Troubleshooting

### "Missing SUPABASE_URL"

```bash
# Verificar que el archivo existe
ls -la .env

# Verificar contenido
cat .env | grep SUPABASE_URL
```

### "Invalid SUPABASE_URL"

```bash
# La URL debe empezar con http:// o https://
SUPABASE_URL=http://127.0.0.1:54321  # Desarrollo local
SUPABASE_URL=https://mi-proyecto.supabase.co  # Producción
```

### "Can't connect to Supabase"

```bash
# Verificar que Supabase esté corriendo
supabase status

# Verificar que el puerto sea correcto
# Local: 54321
# Producción: verificar URL en Supabase Dashboard
```

---

## ✅ Checklist de variables de entorno

- [ ] `.env.example` creado con todas las variables necesarias
- [ ] `.env` creado con valores de desarrollo local
- [ ] `.gitignore` incluye `.env`
- [ ] `scripts/check_env.sh` creado y funciona
- [ ] Variables de producción configuradas en GitHub Secrets
- [ ] Workflows usan `--dart-define` para variables

---

## 📚 Recursos

- [Supabase Environment Variables](https://supabase.com/docs/guides/env-secrets)
- [Flutter Dotenv](https://pub.dev/packages/flutter_dotenv)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

---

**Siguiente**: [05-migraciones-y-seeds.md](./05-migraciones-y-seeds.md)