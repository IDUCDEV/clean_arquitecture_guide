# 02 - Supabase Self-Hosted con Docker

> Aprende a instalar y configurar Supabase en tu propio servidor usando Docker. Esta guía cubre desde la preparación del servidor hasta el despliegue completo.

---

## 🎯 Objetivos de este archivo

- Preparar el servidor para Supabase
- Configurar Docker y Docker Compose
- Desplegar Supabase con docker-compose
- Verificar que todo funciona correctamente

---

## 1. Preparación del servidor

### Requisitos del sistema

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| RAM | 4 GB | 8 GB |
| CPU | 2 cores | 4 cores |
| Almacenamiento | 25 GB | 50+ GB SSD |
| OS | Ubuntu 20.04+ | Ubuntu 22.04 LTS |

### Inicializar el servidor

```bash
# Conectar al servidor (ejemplo con IP)
ssh root@tu-servidor-ip

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias básicas
apt install -y curl wget git vim ufw fail2ban

# Crear usuario no-root (recomendado)
adduser supabase
usermod -aG sudo supabase
```

### Configurar firewall

```bash
# Habilitar firewall
ufw enable

# Permitir SSH
ufw allow 22/tcp

# Permitir HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Verificar
ufw status
```

---

## 2. Instalar Docker

```bash
# Actualizar apt
apt update
apt install -y ca-certificates curl gnupg lsb-release

# Añadir clave GPG de Docker
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Añadir repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verificar instalación
docker --version
docker compose version
```

---

## 3. Descargar Supabase

```bash
cd /opt
git clone https://github.com/supabase/supabase.git
cd supabase/docker
ls -la
```

---

## 4. Configuración de producción

### Archivo .env

```bash
# ==============================================================================
# CONFIGURACIÓN DE PRODUCCIÓN - COMPLETAR ESTOS VALORES
# ==============================================================================

# POSTGRES
POSTGRES_PASSWORD=tu-contraseña-segura-aqui
POSTGRES_DB=postgres
POSTGRES_USER=postgres

# JWT - GENERAR NUEVA CLAVE (python3 -c "import secrets; print(secrets.token_hex(32))")
JWT_SECRET=tu-jwt-secret-aqui-muy-largo-y-seguro

# ANON KEY - GENERAR
ANON_KEY=tu-anon-key-aqui

# SERVICE ROLE KEY - GENERAR
SERVICE_ROLE_KEY=tu-service-role-key-aqui

# ==============================================================================
# CONFIGURACIÓN SMTP (opcional)
# ==============================================================================
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=tu-smtp-password
SMTP_SENDER_EMAIL=tu-email@tu-dominio.com

# ==============================================================================
# CONFIGURACIÓN EXTERNA
# ==============================================================================
SITE_URL=https://tu-dominio.com
ADDITIONAL_REDIRECT_URLS=https://tu-dominio.com
```

### Generar claves

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 5. docker-compose.yml básico

```yaml
version: '3.8'

services:
  db:
    image: supabase/postgres:15.6.1.147
    container_name: supabase-db
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  kong:
    image: kong:3.4
    container_name: supabase-kong
    restart: unless-stopped
    ports:
      - "80:8000"
      - "443:8443"
      - "54321:8000"
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /var/lib/kong/kong.yml

volumes:
  db-data:
```

---

## 6. Iniciar Supabase

```bash
cd /opt/supabase/docker
docker compose up -d
docker compose ps
docker compose logs -f
```

### Verificar servicios

```bash
docker ps
docker exec -it supabase-db psql -U postgres -c "SELECT version();"
curl http://localhost:54321/rest/v1/
```

---

## 7. Nginx como reverse proxy

```bash
apt install -y nginx
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

---

## ✅ Checklist de instalación

- [ ] Servidor preparado
- [ ] Docker instalado
- [ ] Claves generadas
- [ ] .env configurado
- [ ] docker-compose.yml listo
- [ ] Servicios iniciados
- [ ] Nginx configurado

---

## 📚 Recursos

- [Supabase Docker](https://github.com/supabase/supabase/tree/master/docker)

---

**Siguiente**: [03-configuracion-produccion.md](./03-configuracion-produccion.md)