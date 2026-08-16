# 08: Seguridad en el Diseño

> La seguridad se decide en el diseño, no al final. Esquema de cifrado, authn vs authz, HTTPS, TLS y el principio de menor privilegio — siempre con las herramientas que Supabase ya te da.

---

## Seguridad en capas (defense in depth)

```
┌─────────────────────────────────────────────┐
│  App (Flutter)                               │
│    · Secrets nunca en el bundle              │
├─────────────────────────────────────────────┤
│  Transporte                                  │
│    · HTTPS / TLS obligatorio                 │
│    · Certificados válidos                    │
├─────────────────────────────────────────────┤
│  API (Supabase)                              │
│    · Auth (identidad)                        │
│    · RLS (autorización por fila)             │
├─────────────────────────────────────────────┤
│  Base de datos (Postgres)                    │
│    · Menor privilegio                        │
│    · Backups cifrados                        │
└─────────────────────────────────────────────┘
```

---

## HTTPS (cifrado en tránsito)

- **HTTPS** cifra el tráfico entre la app y el servidor. *"HTTPS is the backbone of any secure system."* — System Design Primer.
- Protege de **man-in-the-middle** (alguien leyendo/modificando lo que viaja).
- En Supabase, todas las URLs que usas desde la app son `https://` — el cifrado en tránsito ya está gestionado.

**Configuración que sí te toca:** nunca apuntar la app a URLs `http://` en producción, y validar el certificado (no desactivar la verificación, ni siquiera "para probar").

---

## Cifrado en reposo (at-rest)

| Capa | Qué cifrar | Cómo |
|---|---|---|
| En la app | Datos sensibles locales (tokens) | `flutter_secure_storage` (Keychain/Keystore) |
| Transporte | Todos los requests | TLS vía HTTPS de Supabase |
| Base de datos | Datos en el servidor | Cifrado gestionado por Supabase + columnas sensibles extra |
| Secreto del app | — | Nunca en el bundle; usar Env vars / `.env` y no commitear |

---

## Autenticación vs Autorización (authn vs authz)

- **Authentication (authn):** *"quién eres"*. Probar identidad (login, OAuth, email magic link).
- **Authorization (authz):** *"qué puedes hacer"*. Decidir permisos sobre esa identidad.

**Error típico:** validar solo authn (que el usuario esté logueado) y olvidar authz (que ese usuario en concreto tenga permiso sobre **esa fila**).

### Rol del JWT en Supabase

- Al hacer login, Supabase emite un **JWT** (JSON Web Token) con el `sub` (user id) y los claims de rol.
- El JWT se envía en el header `Authorization: Bearer <token>` en cada request.
- Los **RLS policies** en Postgres leen ese token (vía `auth.uid()`) para decidir qué filas puede ver/modificar cada usuario.

---

## Row Level Security (RLS) como diseño de autorización

El módulo 03 del repo ya cubre RLS en detalle. Aquí la **visión de diseñador**:

- **RLS es tu authorization layer principal** en Supabase: se evalúa en la DB, no en la app. Aunque alguien llame a la API directamente con un JWT robado, RLS sigue protegiendo.
- Diseño por defecto: **deny by default**, luego políticas explícitas de lectura/escritura.
- Cada política usa `auth.uid()` (el `sub` del JWT) → la autorización queda ligada a la identidad autenticada.

```sql
-- Ejemplo: solo el dueño puede ver sus draft posts
CREATE POLICY "read_own_drafts" ON posts
FOR SELECT USING (
  auth.uid() = user_id AND status = 'draft'
);
```

---

## Principio de menor privilegio (least privilege)

> *"Every program and every user of the system should operate using the least set of privileges necessary to complete the job."* — Saltzer & Schroeder.

Aplicado al stack:

| Quién | Permisos correctos |
|---|---|
| Anon key en la app | Solo lo público (RLS niega el resto) |
| Service role key | **Nunca** en la app; solo servidor/Edge Functions |
| Edge Functions | Solo las operaciones que necesita |
| DB roles | Solo los schemas/tablas que usan |

---

## Principio de defensa en profundidad

- No confiar en **una sola** capa de seguridad (ej. solo login sin RLS, o solo RLS sin HTTPS).
- Cada capa protege si la anterior falla: app segura + TLS + authn + authz + least privilege.

*Fuente: System Design Primer — "Security" section + defensa en profundidad clásica (CISSP/OWASP).*

---

## Errores de diseño de seguridad comunes

| Error | Fix |
|---|---|
| Service role key en el bundle de Flutter | Mover a Edge Functions / servidor |
| Confiar solo en authn (login) sin authz | Añadir RLS por fila |
| Permisos abiertos en Storage buckets | Bucket público vs privado + RLS en storage.objects |
| Desactivar verificación de certificado TLS | Validar siempre en producción |
| Loguear tokens/secrets en logs | Nunca imprimir secrets; rotar si se filtra |
| Cifrar todo sin evaluar riesgo | Cifrar lo sensible (tokens, PII) — el resto no añade valor |

---

## Checklist de seguridad de diseño (para tus entrevistas/proyectos)

1. ✅ Todos los requests por HTTPS.
2. ✅ Tokens de Supabase en `flutter_secure_storage`.
3. ✅ RLS habilitado en todas las tablas de datos del usuario.
4. ✅ Service role key solo en backend.
5. ✅ Buckets de Storage con su política (público vs privado).
6. ✅ No hay secrets en el repo (`.env` en `.gitignore`).
7. ✅ Principio de menor privilegio en roles y Edge Functions.
8. ✅ Backups y datos sensibles cifrados en reposo.

---

## Fuentes

- [The System Design Primer — Security](https://github.com/donnemartin/system-design-primer#security)
- [Supabase Docs — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase Docs — Storage security (RLS on buckets)](https://supabase.com/docs/guides/storage/security)
- [Saltzer & Schroeder — The Protection of Information in Computer Systems](https://web.mit.edu/Saltzer/www/publications/protection/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Siguiente:** [09-observabilidad-monitoreo.md](./09-observabilidad-monitoreo.md)
