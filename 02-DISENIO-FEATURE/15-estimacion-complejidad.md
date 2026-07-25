# 15: Estimación de Complejidad de Features

> Antes de escribir código, estima cuánto tiempo te va a llevar. Esto te ayuda a planificar y a no prometer cosas imposibles.

---

## Framework FADER

Una feature se descompone en 4 componentes:

| Componente | Descripción | Ejemplo |
|------------|-------------|---------|
| **F**rontend | UI, widgets, animaciones | Pantalla de perfil |
| **A**pi/Backend | Endpoints, Supabase functions | CRUD de usuarios |
| **D**ata | Modelos, repositories, datasources | User model + repository |
| **E**stados | Cubit/BLoC, states, lógica | AuthCubit |
| **R**equisitos | Auth, permisos, validaciones | Login required |

---

## Pasos para estimar

### 1. Descompón la feature

```markdown
Feature: Sistema de notificaciones

F: UI de lista de notificaciones + badge
A: Supabase Realtime + Edge Function para enviar
D: Notification model + repository
E: NotificationsCubit (unread count)
R: Push notifications permission
```

### 2. Estima cada componente

| Componente | Complejidad | Tiempo estimado |
|------------|-------------|-----------------|
| Frontend (UI) | Media | 3-4h |
| API/Backend | Alta | 4-6h |
| Data | Baja | 1-2h |
| Estados | Media | 2-3h |
| Requisitos | Media | 1-2h |

### 3. Suma con factor de buffer

```
Tiempo base: 11-17 horas
Buffer (30%): +3.5-5h
Total estimado: 15-22 horas
```

---

## Niveles de complejidad

### Feature simple (1-3h)
- Solo UI
- Sin llamadas a backend
- Sin estados complejos
- Ejemplo: Pantalla de settings

### Feature media (4-8h)
- UI + 1-2 llamadas a backend
- 1 Cubit/BLoC
- Validación básica
- Ejemplo: Formulario de registro

### Feature compleja (8-16h)
- UI + backend + realtime
- Múltiples estados
- Auth + permisos
- Ejemplo: Chat en tiempo real

### Feature épica (16-40h)
- Todo lo anterior + más
- Múltiples pantallas
- Integraciones externas
- Ejemplo: Sistema de pagos

---

## Errores de estimación comunes

| Error | Cómo evitarlo |
|-------|---------------|
| Subestimar backend | Siempre suma 30% extra |
| Olvidar testing | Agrega 20% para tests |
| No contar deployment | Agrega 1-2h para deploy |
| Ignorar edge cases | Agrega tiempo para errores |
| No hacer buffer | Siempre 30% buffer |

---

## Template de estimación

```markdown
## Feature: [Nombre]

### Descomposición
- F: [Frontend] → [tiempo]
- A: [API] → [tiempo]
- D: [Data] → [tiempo]
- E: [Estados] → [tiempo]
- R: [Requisitos] → [tiempo]

### Total
- Base: [X] horas
- Buffer (30%): +[X] horas
- Estimado: [X] horas

### Riesgos
- [Riesgo 1]
- [Riesgo 2]

### Dependencias
- [Dependencia 1]
- [Dependencia 2]
```

---

**Volver al índice:** [README.md](./README.md)
