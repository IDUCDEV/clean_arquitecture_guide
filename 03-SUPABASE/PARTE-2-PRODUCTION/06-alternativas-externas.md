# 06 - Alternativas Externas

> Explora otras opciones de backend como servicio que pueden ser alternativas o complementos a Supabase.

---

## 1. Comparativa

| Servicio | Tipo | Backend | Realtime | Storage | Auth | Mejor para |
|----------|------|---------|----------|---------|------|------------|
| **Supabase** | PaaS | PostgreSQL | ✅ | ✅ | ✅ | PostgreSQL, SQL familiar |
| **Firebase** | PaaS | NoSQL | ✅ | ✅ | ✅ | Móvil, prototyping |
| **Appwrite** | Self-hosted | PostgreSQL | ✅ | ✅ | ✅ | Control total |
| **PocketBase** | Single-file | SQLite | ✅ | ✅ | ✅ | Proyectos pequeños |
| **Nhost** | PaaS | PostgreSQL | ✅ | ✅ | ✅ | Next.js, Remix |

---

## 2. Cuándo elegir cada opción

| Tu situación | Recomendación |
|--------------|---------------|
| Nuevo proyecto, SQL, necesitas todo | **Supabase** |
| Proyecto móvil, Firebase SDK importante | **Firebase** |
| Self-hosted obligatorio, más control | **Appwrite** |
| Proyecto pequeño, máxima simplicidad | **PocketBase** |
| Ya usas Next.js, prefieres GraphQL | **Nhost** |

---

## 3. Firebase (Google)

**Ventajas:**
- Excelente SDK para Flutter
- Amplia documentación
- Escalabilidad automática

**Desventajas:**
- No SQL (NoSQL)
- Vendor lock-in alto
- Menos control

---

## 4. Appwrite

**Ventajas:**
- Open source
- Self-hosted completo
- API REST clara

**Desventajas:**
- Comunidad más pequeña
- Menos features que Supabase

---

## 5. PocketBase

**Ventajas:**
- Single executable (Go)
- Muy fácil de configurar
- SQLite embebido

**Desventajas:**
- No para alta concurrencia
- Menos escalable

---

**Fin de la Parte 2: Producción**  

---

## 📚 Referencias

- [Supabase | Documentación oficial](https://supabase.com/docs) — Guías, API reference y arquitectura
- [Supabase | CLI reference](https://supabase.com/docs/reference/cli) — Comandos de la CLI de Supabase
- [Supabase | Flutter SDK](https://pub.dev/packages/supabase_flutter) — SDK oficial para Flutter
- [Supabase | Migraciones](https://supabase.com/docs/guides/local-development/migrations) — Gestión de migraciones locales

---

> 📖 **Siguiente:** **[Continuar con PARTE-3-CI_CD](../PARTE-3-CI_CD/01-makefile-universal.md)**