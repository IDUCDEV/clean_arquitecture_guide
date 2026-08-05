# Plantilla de Diseño de Feature

> Copia esta plantilla para cada feature nueva. Completa cada sección en orden, en papel o aquí. Cada sección enlaza a su teoría en este módulo.

**Feature:** `[nombre]`
**Proyecto:** `[nombre]`
**Fecha:** `[YYYY-MM-DD]`
**Complejidad estimada:** `[Simple / Intermedia / Compleja]` → ver [15-estimacion-complejidad.md](./15-estimacion-complejidad.md)

---

## 0. Alcance

> Teoría: [00-alcance-feature.md](./00-alcance-feature.md)

- **Incluye:** [qué cubre la feature]
- **No incluye:** [qué NO cubre — límites explícitos]
- **Dependencias:** [qué debe existir antes: features, tablas, servicios]
- **Suposiciones:** [qué das por hecho]
- **Preguntas abiertas:** [qué no sabes todavía]

---

## 1. FADER

> Teoría: [01-descomposicion-feature.md](./01-descomposicion-feature.md)

### Formular
- [ ] Como `[actor]`, quiero `[acción]` para `[valor]`.
- [ ] Como `[actor]`, quiero `[acción]` para `[valor]`.

### Actorizar
| Actor | Tipo | ¿Qué puede hacer? | ¿Qué NO puede hacer? |
|-------|------|-------------------|----------------------|
| `[actor]` | Primario | | |

### Descomponer
- `[C/R/U/D]` `[operación]` — `[actor]`
- `[Validación]` `[operación]`
- `[Cálculo]` `[operación]`
- `[Transición]` `[operación]`

### Entidades
- `[Entidad]: [atributos esenciales]`

### Reglas
- `RN001:` `[regla de negocio → UseCase/dominio]`
- `RN002:` `[regla de negocio]`
- `RT001:` `[regla técnica → DATA/datasource]` (paginación, realtime, caching…)
- `RS001:` `[regla de seguridad → autorización del servidor (RLS en Supabase / middleware en REST)]`

---

## 2. Mapeo a Capas

> Teoría: [02-mapeo-capas.md](./02-mapeo-capas.md)

| Responsabilidad | Capa propietaria | Pieza | Regla(s) que defiende |
|-----------------|------------------|-------|-----------------------|
| `[validar X]` | DOMAIN | `[UseCase]` | `RN00x` |
| `[persistir]` | DATA | `[DataSource]` | `RT00x` |
| `[autorizar]` | DATA | `[RLS]` | `RS00x` |
| `[mostrar]` | PRESENTATION | `[Widget]` | — (nunca reglas) |

### Estructura de carpetas
```
domain/...
data/...
presentation/...
```

---

## 3. Contratos

> Teoría: [03-contratos-primero.md](./03-contratos-primero.md)

```dart
abstract class XRepository {
  // Métodos con params tipados y retorno Either<Failure, T>
}
```

### Estados de UI
```dart
sealed class XState { /* loading, loaded, error… */ }
```

---

## 4. Flujo de Datos

> Teoría: [04-flujo-datos.md](./04-flujo-datos.md)

```
WIDGET → CUBIT → USECASE → REPO → DATA SOURCE → API/BD → fold() → emit()
```

- Validaciones en cada paso:
- Transformaciones de tipos:
- Errores manejados:
- Realtime (Streams): `[sí/no]`

---

## 5. Contrato con el Backend (Supabase / REST API)

> Teoría: [05e-diseno-supabase.md](./05e-diseno-supabase.md)
>
> Esta sección define lo que la app necesita del servidor. Con Supabase la implementas tú (tablas, RLS, RPC). Con una REST API solo especificas el **contrato** (endpoint, DTO, errores, garantías); el backend lo implementa.

- Backend: `[Supabase | REST API]`
- Garantías del servidor: `[atómico, autorizado (RS), idempotente]`

### Tablas (Supabase) / Contrato de endpoints (REST API)
```
[nombre_tabla]                    |  [VERBO /path] → [DTO request → DTO response]
├── columna tipo                  |  Errores: [códigos]
└── constraint …
```

### Operaciones por UseCase
| UseCase | Operación (Supabase) | Endpoint (REST API) | Atómico? |
|---------|----------------------|---------------------|----------|
| `[UseCase]` | `[select/insert/update/rpc]` | `[GET/POST/PATCH/DELETE]` | `[sí/no]` |

### RLS / Autorización del servidor
- `RS00x` → policy RLS (Supabase) / rol+permiso en el servidor (REST): `[descripción]`

### Realtime
- `[tabla/feature]` → `[cambios/Broadcast]`

---

## 6. Criterios de Aceptación y Trazabilidad

> Teoría: [05f-criterios-aceptacion-trazabilidad.md](./05f-criterios-aceptacion-trazabilidad.md)

### Criterios (BDD)
```gherkin
Escenario: [título]
  Dado [contexto]
  Cuando [acción]
  Entonces [resultado]
```

### Matriz de trazabilidad
| UseCase | Regla(s) | Contrato | Fuente de verdad | Test |
|---------|----------|----------|------------------|------|
| `[UseCase]` | `RN00x` | `[método]` | `[API / RPC / RLS / cron]` | `[unit / widget / integration]` |

---

## 7. Decisiones y ADRs

- `ADR-001`: `[decisión clave]` — contexto, decisión, consecuencias, alternativas.
- `ADR-002`: `[decisión clave]`

---

## 8. Orden de Implementación

1. `[entidad]`
2. `[contratos]`
3. `[usecases]`
4. `[modelos + datasources]`
5. `[repositorios]`
6. `[cubits]`
7. `[páginas/widgets]`
8. `[tablas/RLS/RPC en Supabase]`

---

**Referencias del módulo:** [README.md](./README.md) · [00-alcance-feature.md](./00-alcance-feature.md) · [01-descomposicion-feature.md](./01-descomposicion-feature.md) · [02-mapeo-capas.md](./02-mapeo-capas.md) · [03-contratos-primero.md](./03-contratos-primero.md) · [04-flujo-datos.md](./04-flujo-datos.md) · [05e-diseno-supabase.md](./05e-diseno-supabase.md) · [05f-criterios-aceptacion-trazabilidad.md](./05f-criterios-aceptacion-trazabilidad.md) · [15-estimacion-complejidad.md](./15-estimacion-complejidad.md)
