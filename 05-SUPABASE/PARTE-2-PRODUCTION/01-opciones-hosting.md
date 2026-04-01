# 01 - Opciones de Hosting para Supabase Self-Hosted

> Compara las diferentes opciones de hosting para ejecutar Supabase en producción. Aprende a elegir el proveedor adecuado según tus necesidades y presupuesto.

---

## 🎯 Objetivos de este archivo

- Conocer las opciones de hosting disponibles
- Comparar proveedores por precio, rendimiento y facilidad
- Tomar decisiones informadas para tu proyecto

---

## 1. Opciones de hosting

### Comparativa rápida

| Proveedor | Tipo | Precio estimado | Dificultad | Mejor para |
|-----------|------|-----------------|------------|------------|
| **DigitalOcean** | VPS | $20-80/mes | Media | Equipos medianos |
| **Hetzner** | VPS | €15-50/mes | Media | Presupuesto limitado |
| **AWS EC2** | Cloud | $30-200/mes | Alta | Grande escala |
| **Railway** | PaaS | $20-100/mes | Baja | Desarrollo rápido |
| **Helio Cloud** | PaaS | $20-80/mes | Baja | Alternativa a Supabase |
| **Caprover** | Contenedores | $10-40/mes | Alta | Autoalojamiento completo |

---

## 2. VPS (Virtual Private Server)

### DigitalOcean

**Ventajas:**
- Interfaz intuitiva
- Documentación excelente
- Marketplace con imágenes preconfiguradas
- droplets escalables

**Precios:**
- Basic Droplet: $20/mes (2GB RAM, 1 CPU, 50GB SSD)
- Standard: $40/mes (4GB RAM, 2 CPU, 80GB SSD)
- Premium: $80/mes (8GB RAM, 4 CPU, 160GB SSD)

**Setup:**
```bash
# Crear droplet desde CLI
doctl compute droplet create supabase-server \
  --region nyc1 \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04 \
  --ssh-keys tu-ssh-key
```

**Docker deployment:**
```bash
# Conectar al droplet
ssh root@tu-ip

# Instalar Docker
curl -fsSL https://get.docker.com | sh

# Instalar Supabase
git clone https://github.com/supabase/supabase.git
cd supabase/docker
docker compose up -d
```

### Hetzner

**Ventajas:**
- Excelente relación precio/rendimiento
- Datacenters en Europa (baja latencia para usuarios europeos)
- Sin problemas de facturación (solo tarjeta de crédito)

**Precios:**
- CPX11: €4.89/mes (2GB RAM, 1 vCPU, 40GB SSD)
- CPX21: €9.89/mes (4GB RAM, 2 vCPU, 80GB SSD)
- CPX31: €19.89/mes (8GB RAM, 4 vCPU, 160GB SSD)

**Configuración:**
```bash
# Instalar Docker en Hetzner Cloud
apt update && apt install -y docker.io docker-compose

# Descargar y configurar Supabase
git clone https://github.com/supabase/supabase.git
cd supabase/docker
```

---

## 3. Plataformas como servicio (PaaS)

### Railway

**Ventajas:**
- Despliegue con un click
- Scaling automático
- Soporte nativo de Docker

**Precios:**
- Hobby: $5/mes
- Developer: $20/mes
- Pro: $50/mes

**Limitaciones:**
- Recursos limitados en planes bajos
- No soportan todas las características de Supabase

**Alternativa:** Usar el template de Railway para Supabase (si está disponible)

### Helio Cloud (Alternativa a Supabase)

- Similar a Supabase Cloud pero con hosting propio
- Más fácil de configurar que Supabase self-hosted

---

## 4. Contenedores (Kubernetes/Docker)

### Caprover + Supabase

**Ventajas:**
- Total control
- Una única instancia para múltiples apps
- Bajo costo

**Precios:**
- VPS básico: $10-15/mes
- Caprover: Gratuito (open source)

**Setup:**
```bash
# Instalar Caprover
curl -s https://raw.githubusercontent.com/caprover/caprover/master/tools/captainoverlay.sh | bash

# Añadir Supabase desde One-Click Apps
# O desplegar manualmente con docker-compose
```

---

## 5. Recomendaciones por caso de uso

### Proyecto personal / Portfolio

| Opción | Precio | Notas |
|--------|--------|-------|
| Hetzner CPX11 | €4.89/mes | Mejor costo-beneficio |
| Railway Hobby | $5/mes | Más fácil de configurar |

### Startup / MVP

| Opción | Precio | Notas |
|--------|--------|-------|
| DigitalOcean Standard | $40/mes | Balance costo/rendimiento |
| Hetzner CPX31 | €19.89/mes | Mejor para usuarios europeos |

### Producto en producción

| Opción | Precio | Notas |
|--------|--------|-------|
| DigitalOcean Premium | $80/mes | Fiabilidad probada |
| AWS (EC2 + RDS) | $100-200/mes | Escalabilidad total |
| Kubernetes auto-gestionado | $150+/mes | Para equipos grandes |

---

## 6. Requisitos mínimos para Supabase

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| **RAM** | 4 GB | 8 GB |
| **CPU** | 2 cores | 4 cores |
| **Almacenamiento** | 20 GB | 50+ GB SSD |
| **SO** | Ubuntu 20.04+ / Debian 11+ | Ubuntu 22.04 LTS |

---

## 7. Costos ocultos a considerar

### VPS
- Backups automáticos (~$5-10/mes)
- Transferencia de datos adicional
- IPs dedicadas (~$4/mes)

### Cloud
- Egress traffic (datos salientes)
- Storage adicional
- snapshots

### Siempre
- Dominio y SSL
- Mantenimiento y monitoreo

---

## 8. Herramientas de monitoreo

### Essentials

| Herramienta | Uso | Costo |
|-------------|-----|-------|
| **Uptime Kuma** | Monitoreo de uptime | Gratis |
| **Grafana + Prometheus** | Métricas | Gratis |
| **Supabase CLI** | Verificar estado | - |

---

## 9. Decision matrix

```
                    BAJO COSTO          ALTO COSTO
                    ═══════════         ══════════
FÁCIL     ───────► Railway              Supabase Cloud
                    │                       │
                    │                    $$$$
                    ▼                       ▼
MEDIO     ───────► Hetzner               DigitalOcean
                    │                       │
                    │                       │
                    ▼                       ▼
DIFÍCIL  ───────► Caprover               AWS/K8s
                    │                       │
                    │                    escalable
```

---

## ✅ Checklist de elección de hosting

- [ ] Definido presupuesto mensual
- [ ] Conocida la ubicación geográfica de usuarios
- [ ] Evaluados requisitos de tráfico/escala
- [ ] Considerados costos de transferencia
- [ ] Planeada estrategia de backups
- [ ] Considerado tiempo de mantenimiento

---

## 📚 Recursos

- [Supabase Self-Hosted](https://supabase.com/docs/guides/self-hosting)
- [Docker Compose for Supabase](https://github.com/supabase/supabase/tree/master/docker)
- [DigitalOcean Marketplace](https://marketplace.digitalocean.com/)
- [Hetzner Cloud](https://hetzner.cloud/)

---

**Siguiente**: [02-supabase-self-hosted-docker.md](./02-supabase-self-hosted-docker.md)