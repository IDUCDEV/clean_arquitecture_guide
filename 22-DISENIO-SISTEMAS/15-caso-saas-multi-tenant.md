# 15: Caso de Estudio — SaaS Multi-Tenant

> Aplicación de la plantilla a una plataforma SaaS donde muchos clientes (tenants) comparten la misma infraestructura. El aislamiento entre tenants es el problema de diseño central.

---

## Paso 1: Alcance y requerimientos

**Producto:** SaaS de gestión de proyectos (tipo Notion/Trello) con múltiples organizaciones.

| Incluido | Fuera de scope (este diseño) |
|---|---|
| Organizaciones + membresías | Billing/planes reales |
| Proyectos y tareas por org | Integraciones de terceros |
| Permisos por rol (admin/member/viewer) | Multi-region |
| Uso compartido de infraestructura | White-labeling |

**No funcionales:** aislamiento **estricto** entre tenants (un tenant no puede ver datos de otro), escala de miles de tenants, disponibilidad alta.

---

## Paso 2: Estimación de escala

| Métrica | Valor |
|---|---|
| Tenants activos | 5K |
| Usuarios totales | 500K (100 por tenant) |
| Filas de tareas | 50M |
| QPS total | ~1K |

**Lectura:** la complejidad no está en la escala bruta, sino en **cómo aislar 5K tenants** dentro de una sola base de datos.

---

## Paso 3: Modelado de datos (el corazón del SaaS)

```sql
organizations(id, name, plan)
organization_members(org_id, user_id, role)   -- 'admin' | 'member' | 'viewer'
projects(id, org_id, name, created_at)
tasks(id, project_id, title, status, assignee_id, created_at)
```

- **Índices:** `projects(org_id)`, `tasks(project_id)`, `organization_members(user_id)`.
- **RLS (lo más importante):** toda consulta se filtra por membresía. Un usuario solo ve tareas si es miembro de la org del proyecto.

```sql
CREATE POLICY "read_projects_of_my_orgs" ON projects
FOR SELECT USING (
  EXISTS (
    SELECT 1 FROM organization_members m
    WHERE m.org_id = projects.org_id
      AND m.user_id = auth.uid()
  )
);
```

- **Multiplicador de aislamiento:** el mismo patrón se replica en `tasks`, `comments`, etc. Cada tabla con FK a `projects`/`orgs` requiere su política.

---

## Paso 4-5: Arquitectura de alto nivel

```
┌─────────┐          ┌───────────────────────────────────────┐
│  Flutter│          │              Supabase                  │
│   App   │          │  ┌────────────┐  ┌───────────────────┐ │
│  cache  │── HTTPS─▶│  │  API/Auth  │──│  Postgres         │ │
└─────────┘          │  └────────────┘  │  RLS = isolation  │ │
        ▲            │                   │  layer            │ │
        │            │  ┌────────────┐  └───────────────────┘ │
   ┌────┴────┐       │  │  Cache per │                        │
   │  CDN    │       │  │  tenant    │                        │
   └─────────┘       │  └────────────┘                        │
                    └─────────────────────────────────────────┘
```

**Componentes:**
1. **App:** cache local por tenant (el cache de un tenant nunca contamina otro).
2. **Supabase Auth + API:** identidad y requests.
3. **Postgres con RLS:** el aislador de tenants (deny-by-default + políticas por membresía).
4. **Cache por tenant:** claves namespaced por `org_id`.

---

## Paso 6: Decisiones de diseño con trade-offs

| Decisión | Por qué | Trade-off aceptado |
|---|---|---|
| **Single-tenant DB + RLS** | Un solo Postgres para todos (barato, simple) | Políticas RLS complejas; riesgo si una política falla |
| RLS como único control de aislamiento | Se evalúa en el servidor; la app no puede saltárselo | Todo nuevo acceso requiere su política |
| Roles por membresía (admin/member/viewer) | Permisos por fila, no por app | Políticas por rol = más SQL |
| Cache namespaced por tenant | No filtrar datos entre tenants | Invalidate por tenant al escribir |
| Row Level Security test en CI | Prevenir fuga entre tenants | Test suite dedicada de aislamiento |

### El patrón de aislamiento que se repite
```
1. El usuario se autentica → JWT con auth.uid()
2. Cada query pasa por RLS → solo filas cuya org lo incluye como miembro
3. Los permisos por rol (admin puede borrar, viewer solo lee) se
   codifican en políticas RLS adicionales
4. Ninguna query en la app usa el service role (se saltaría RLS)
```

---

## Paso 7: Consistencia y disponibilidad

- **Modelo:** strong consistency (un Postgres transaccional para todos los tenants).
- **SLA:** 99.9% (los tenants dependen del SaaS).
- **Patrones:** retries/backoff en la app, cache local como fallback de lectura.

**Justificación CAP:** es un sistema **CP por defecto** — la consistencia de datos de proyectos importa más que servir data eventual. La alta disponibilidad se consigue con la infraestructura gestionada de Supabase, no con consistencia eventual.

---

## Paso 8-9: Seguridad y observabilidad

**Seguridad (crítica en multi-tenant):**
- RLS deny-by-default en **todas** las tablas con datos de tenant.
- Test de aislamiento: simular 2 usuarios de orgs distintas y verificar que **no** se cruzan datos.
- Service role key nunca en la app (rompería el aislamiento).
- Auditoría de quién accede a qué org.

**Observabilidad:**
| Métrica | Alerta |
|---|---|
| Fuga potencial de RLS (test en CI falla) | Bloquear merge |
| Latencia por tenant (un tenant pesado) | Revisar "noisy neighbor" |
| Queries sin RLS detectadas | Logs de plan de ejecución |
| Cache invalidado por tenant | Monitorear miss rate por org |

---

## Paso 10: Riesgos y evolución

| Riesgo | Mitigación |
|---|---|
| Un tenant satura la DB (noisy neighbor) | Cuotas por tenant, pooling, rate limits |
| RLS mal escrita filtra datos | Test de aislamiento automatizado en CI |
| Escalar a miles de tenants pesados | Schema-per-tenant o database-per-tenant (extremos) |
| Roles complejos | Tabla de permisos + policies parametrizadas |

---

## Fuentes del caso

- [Supabase Docs — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security) (multi-tenant section)
- [Supabase Docs — Making RLS Easier (multi-tenant patterns)](https://supabase.com/docs/guides/database/postgres/row-level-security#multi-tenant-applications)
- [ByteByteGo — Multi-tenant architecture](https://bytebytego.com/guides/multi-tenant-architecture)
- [Martin Fowler — MultiTenant](https://martinfowler.com/bliki/MultiTenant.html)

---

**Siguiente:** [16-ejercicios-practica.md](./16-ejercicios-practica.md)
