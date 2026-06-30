# 03 - Release Tracks

> Gestiona el ciclo de vida del release: pruebas internas, beta cerrada, beta abierta, y producción.

---

## 1. Los 4 Tracks de Release

```
Internal Testing (pruebas internas)
       │
       ▼
Closed Testing (beta cerrada)
       │
       ▼
Open Testing (beta abierta)
       │
       ▼
Production (producción)
```

### 1.1 Internal Testing

| Aspecto | Detalle |
|---------|---------|
| **Máximo testers** | 100 |
| **Tiempo de revisión** | Instantáneo (minutos) |
| **Para qué** | Equipo de desarrollo, QA |
| **Requiere revisión** | No |

**Uso:** Ideal para probar cada build antes de pasarlo a producción.

### 1.2 Closed Testing

| Aspecto | Detalle |
|---------|---------|
| **Máximo testers** | Sin límite (pero grupos específicos) |
| **Tiempo de revisión** | Horas o días |
| **Para qué** | Beta cerrada con clientes selectos |
| **Requiere revisión** | Sí (si hay cambios grandes) |

**Uso:** Probar con un grupo limitado de usuarios reales.

### 1.3 Open Testing

| Aspecto | Detalle |
|---------|---------|
| **Máximo testers** | Sin límite |
| **Tiempo de revisión** | Horas o días |
| **Para qué** | Beta pública |
| **Requiere revisión** | Sí |

**Uso:** Cuando quieres feedback masivo antes del release oficial.

### 1.4 Production

| Aspecto | Detalle |
|---------|---------|
| **Testers** | Todos los usuarios |
| **Tiempo de revisión** | Horas o días |
| **Para qué** | Release oficial |
| **Requiere revisión** | Sí |

---

## 2. Flujo de Release Recomendado

### 2.1 Para Apps Nuevas

```bash
# 1. Internal Testing (equipo: 5-10 testers)
# 2. Closed Testing (clientes piloto: 50-100 testers)
# 3. Producción
```

**Nota:** Google Play requiere que las apps nuevas pasen por Closed Testing con al menos 20 testers durante 14 días antes de producción. Para algunas cuentas este requisito puede variar.

### 2.2 Para Releases de Actualización

```bash
# 1. Internal Testing (QA team)
# 2. Closed Testing (grupo reducido, 24h)
# 3. Rollout gradual a producción (20% → 50% → 100%)
```

### 2.3 Rollout Gradual

```
Producción: 20% de usuarios
├── Si OK en 24h → aumentar a 50%
│   ├── Si OK → 100%
│   └── Si error → detener rollout
└── Si error → detener rollout, arreglar, nuevo release
```

---

## 3. Configurar Tracks

### 3.1 Internal Testing

1. Play Console > Lanzamiento > Versiones
2. Pestaña "Internal testing"
3. "Crear nueva versión"
4. Subir AAB
5. Completar "Novedades de esta versión"
6. Guardar y enviar

### 3.2 Agregar Testers

```
Internal testing > Gestionar testers
├── Crear grupo de email
│   └── Agregar emails: dev1@email.com, dev2@email.com
└── Compartir link de opt-in
    └── https://play.google.com/apps/testing/com.tuapp
```

### 3.3 Closed Testing

```
Closed testing > Crear pista
├── Nombre: "Beta Clientes"
├── Grupos de testers
│   └── Crear grupo con emails
└── Subir AAB
```

### 3.4 Open Testing

```
Open testing > Crear pista
├── Subir AAB
└── Publicar link de opt-in
    └── Cualquiera con el link puede unirse
```

---

## 4. Promocionar entre Tracks

Una vez probado en un track inferior, puedes promocionar el mismo AAB al siguiente:

```
Internal Testing (AAB v1.0.0+1)
       │  Promocionar
       ▼
Closed Testing (mismo AAB v1.0.0+1)
       │  Promocionar
       ▼
Production (mismo AAB v1.0.0+1)
```

**Ventaja:** El mismo AAB probado en QA es el que llega a producción. Sin recompilación, sin sorpresas.

---

## 5. Novedades de la Versión (What's New)

### 5.1 Buenas Prácticas

```markdown
## ❌ Mal
- Corrección de errores
- Mejoras de rendimiento
- Bugs fixed

## ✅ Bien
- Nueva función: exportación de resultados a PDF
- Corrección: crash al abrir sorteo sin conexión
- Mejora: carga 40% más rápida en listas grandes
```

### 5.2 Formato

```markdown
# Versión 1.2.0
✨ Nuevo:
• Exportación de resultados a PDF
• Notificaciones push cuando un sorteo termina

🐛 Correcciones:
• Crash al abrir sorteo sin conexión
• Cálculo incorrecto de premios compartidos

⚡ Mejoras:
• Carga 40% más rápida en listas grandes
```

Máximo 500 caracteres para el campo "Novedades".

---

## 6. Releases de Emergencia

### 6.1 Detener Rollout

```bash
# Si detectas un bug crítico en producción:
# 1. Play Console > Releases existentes
# 2. Botón "Detener rollout"
# 3. Los usuarios ya actualizados se quedan con esa versión
# 4. Nuevos usuarios reciben la versión anterior
```

### 6.2 Release Urgente

```bash
# 1. Arreglar bug
# 2. Incrementar versionCode
# 3. Generar AAB
# 4. Subir directamente a producción (saltar tracks)
# 5. Google Play revisa en horas (o minutos si es crítica)
```

---

## 7. Buenas Prácticas

### 7.1 Versionado

```yaml
# pubspec.yaml
version: 1.2.0+3
#         ^^^^^ ^
#         |     +-- versionCode (número, siempre incrementar)
#         +-------- versionName (semántico, visible al usuario)
```

### 7.2 Release Branches

```bash
# Crear rama de release
git checkout develop
git checkout -b release/1.2.0

# Solo fixes en release branch
git commit -m "fix: ajustar textos para release"

# Merge a main con tag
git checkout main
git merge release/1.2.0
git tag -a v1.2.0 -m "Release 1.2.0"
```

---

## 8. Resumen

1. **4 tracks**: Internal → Closed → Open → Production
2. **Internal** para QA, **Closed** para betatesters, **Production** para todos
3. **Rollout gradual** para minimizar riesgo
4. **Promocionar** el mismo AAB entre tracks
5. **Release de emergencia** con detención de rollout
6. **Novedades claras** para el usuario

---

## Recursos

- [Play Console Release Tracks](https://support.google.com/googleplay/android-developer/answer/9859152)
- [Staged Rollouts](https://support.google.com/googleplay/android-developer/answer/6346149)
- [Testing Best Practices](https://developer.android.com/distribute/best-practices/launch/test-tracks)
