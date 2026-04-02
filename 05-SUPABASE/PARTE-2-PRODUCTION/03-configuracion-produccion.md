# 03 - Configuración de Producción

> Aprende a configurar Supabase para producción: seguridad, rendimiento, SMTP, dominios y más.

---

## 🎯 Objetivos de este archivo

- Configurar variables de producción
- Implementar medidas de seguridad
- Configurar SMTP
- Configurar dominios personalizados

---

## 1. Variables de entorno de producción

```bash
# CLAVES (GENERAR NUEVAS)
POSTGRES_PASSWORD=SuperSecretPassword123!@#
JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))")
ANON_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
SERVICE_ROLE_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# URLs
SITE_URL=https://tu-dominio.com
ADDITIONAL_REDIRECT_URLS=https://tu-dominio.com
API_EXTERNAL_URL=https://tu-dominio.com

# SMTP
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=tu-password
SMTP_SENDER_EMAIL=noreply@tu-dominio.com
```

---

## 2. Seguridad

### Claves únicas

```bash
# NO usar claves de desarrollo en producción
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Forzar HTTPS (Nginx)

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    return 301 https://$server_name$request_uri;
}
```

### Headers de seguridad

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000" always;
```

---

## 3. SMTP

### Proveedores recomendados

| Proveedor | Costo |
|-----------|-------|
| SendGrid | $0-15/mes |
| Mailgun | $0-35/mes |
| AWS SES | $0.10/1000 |

---

## 4. Dominio personalizado

```bash
# DNS
A record: @ -> tu-ip
CNAME: www -> tu-dominio.com
```

---

## ✅ Checklist

- [ ] Claves únicas de producción
- [ ] SSL configurado
- [ ] SMTP configurado
- [ ] Dominio configurado

---

**Siguiente**: [04-migracion-local-a-produccion.md](./04-migracion-local-a-produccion.md)