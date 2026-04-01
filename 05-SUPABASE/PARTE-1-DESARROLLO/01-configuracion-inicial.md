# 01 - Configuración Inicial de Supabase Local

> Aprende a instalar y configurar Supabase localmente para desarrollo. Esta guía es el punto de partida para cualquier proyecto que use Supabase.

---

## 🎯 Objetivos de este archivo

- Instalar Docker Desktop
- Instalar Supabase CLI
- Inicializar un proyecto Supabase
- Verificar que el entorno funciona correctamente

---

## 1. Instalación de Docker

### ¿Por qué Docker?

Supabase local funciona como un conjunto de servicios (PostgreSQL, Auth, Storage, Realtime, etc.) que se ejecutan en contenedores Docker. **Docker es requisito obligatorio**.

### Instalación en Linux (Ubuntu/Debian)

```bash
# Actualizar paquetes
sudo apt update

# Instalar dependencias
sudo apt install -y ca-certificates curl gnupg lsb-release

# Añadir clave GPG de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Añadir repositorio Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Añadir usuario al grupo docker (evita usar sudo)
sudo usermod -aG docker $USER

# Cerrar sesión y volver a entrar para aplicar cambios
```

### Instalación en macOS

1. Descarga **Docker Desktop** desde [docker.com](https://www.docker.com/products/docker-desktop/)
2. Instala la aplicación
3. Inicia Docker Desktop desde Applications

### Instalación en Windows

1. Descarga **Docker Desktop** desde [docker.com](https://www.docker.com/products/docker-desktop/)
2. Ejecuta el instalador (asegúrate de habilitar WSL2 durante la instalación)
3. Inicia Docker Desktop

### Verificar instalación

```bash
docker --version
# Output esperado: Docker version 24.0.0+

docker compose version
# Output esperado: Docker Compose version v2.20.0+
```

---

## 2. Instalación de Supabase CLI

### Método recomendado: Binary release

```bash
# Linux/macOS
sudo curl -fsSL "https://github.com/supabase/cli/releases/download/v1.220.0/supabase_1.220.0_linux_amd64.tar.gz" -o /tmp/supabase.tar.gz
sudo tar xzf /tmp/supabase.tar.gz -C /usr/local/bin

# Verificar instalación
supabase --version
```

### Método alternativo: npm

```bash
# Requiere Node.js instalado
npm install -g supabase

supabase --version
```

### Método en macOS con Homebrew

```bash
brew install supabase/tap/supabase
supabase --version
```

---

## 3. Inicializar un nuevo proyecto Supabase

### Paso 1: Crear carpeta del proyecto

```bash
# Desde la raíz de tu proyecto Flutter
mkdir supabase
cd supabase
```

### Paso 2: Inicializar Supabase

```bash
supabase init
```

Este comando crea la estructura básica:

```
supabase/
├── .temp/              # Archivos temporales de CLI
├── config.toml         # Configuración principal
├── migrations/         # Migraciones de base de datos
├── seed.sql           # Datos iniciales (opcional)
└── tests/             # Tests de base de datos (opcional)
```

### Paso 3: Configuración inicial (config.toml)

El archivo `config.toml` se genera automáticamente. Los valores más importantes son:

```toml
project_id = "mi-proyecto"  # Cambia esto por tu nombre de proyecto

[api]
enabled = true
port = 54321

[db]
port = 54322
major_version = 17

[studio]
enabled = true
port = 54323

[inbucket]
enabled = true
port = 54324

[storage]
enabled = true

[auth]
enabled = true
site_url = "http://127.0.0.1:3000"
enable_signup = true
```

---

## 4. Iniciar el entorno local

### Iniciar todos los servicios

```bash
supabase start
```

Esto iniciando:
- **PostgreSQL** (puerto 54322)
- **API REST** (puerto 54321)
- **Studio** (puerto 54323)
- **Inbucket** (puerto 54324) - servidor de emails para desarrollo

### Verificar estado

```bash
supabase status
```

Salida esperada:
```
API URL: http://127.0.0.1:54321
DB URL: postgresql://postgres:postgres@localhost:54322/postgres
Studio URL: http://127.0.0.1:54323
Inbucket URL: http://127.0.0.1:54324
```

### Detener el entorno

```bash
supabase stop
```

---

## 5. Primera migración

### Crear la primera tabla

1. Crea el archivo de migración:

```bash
supabase migration new create_users_table
```

2. Edita el archivo generado en `supabase/migrations/`:

```sql
-- Up Migration
CREATE TABLE public.users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Política de lectura para usuarios autenticados
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);
```

3. Aplicar la migración:

```bash
supabase db reset
```

Este comando:
- Aplica todas las migraciones pendientes
- Ejecuta los seeds (si existen)
- Reinicia la base de datos

---

## 6. Scripts de automatización

### Script para verificar entorno

Crea `scripts/check_supabase.sh`:

```bash
#!/bin/bash
set -e

echo "==> Verificando entorno de Supabase..."

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker no está corriendo"
    exit 1
fi

# Verificar Supabase CLI
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI no está instalado"
    exit 1
fi

# Verificar que Supabase está corriendo
if ! supabase status &> /dev/null; then
    echo "⚠️  Supabase no está corriendo. Ejecuta: supabase start"
    exit 1
fi

echo "✅ Entorno de Supabase listo"
```

```bash
chmod +x scripts/check_supabase.sh
```

### Uso en Makefile

```makefile
.PHONY: supabase-check
supabase-check:
	@./scripts/check_supabase.sh
```

---

## ⚠️ Problemas comunes

### "Port already in use"

```bash
# Ver qué proceso usa el puerto
lsof -i :54322

# O usar otro puerto en config.toml
[db]
port = 54325  # Cambiar a otro puerto
```

### "Docker daemon not running"

- **Linux**: `sudo systemctl start docker`
- **macOS/Windows**: Iniciar Docker Desktop

### "Cannot connect to the Docker daemon"

- Añadir usuario al grupo docker: `sudo usermod -aG docker $USER`
- Cerrar sesión y volver a entrar

---

## ✅ Checklist de verificación

- [ ] Docker instalado y corriendo
- [ ] Supabase CLI instalado (`supabase --version`)
- [ ] Proyecto inicializado (`supabase init`)
- [ ] Entorno iniciado (`supabase start`)
- [ ] Estado verificado (`supabase status`)
- [ ] Primera migración aplicada (`supabase db reset`)

---

## 📚 Recursos

- [Install Docker](https://docs.docker.com/get-docker/)
- [Supabase CLI Docs](https://supabase.com/docs/reference/cli/overview)
- [Supabase Docker](https://github.com/supabase/supabase/tree/master/docker)

---

**Siguiente**: [02-estructura-proyecto-supabase.md](./02-estructura-proyecto-supabase.md)