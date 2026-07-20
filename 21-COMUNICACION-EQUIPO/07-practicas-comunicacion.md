# 07: Practicas de Comunicacion

## 5 Escenarios Reales con Resolucion

Cada escenario incluye: **Contexto**, **Que hacer**, **Que NO hacer**, y **Template de respuesta**.

---

## Escenario 1: Code Review de Feature Compleja

### Contexto

Tu compañero Carlos abrió un PR de 600 líneas que implementa el módulo de pagos.
El PR tiene problemas arquitectónicos (dependencias cruzadas), preocupaciones de seguridad
(API keys expuestas), y no tiene tests. Necesitas darle feedback sin desmotivarlo.

### Que hacer

**Paso 1: Leer todo el PR antes de comentar**

No comentes linea por linea. Primero entiende la vision general.

**Paso 2: Clasificar tus comentarios por prioridad**

```
┌─────────────────────────────────────────────────────────────────┐
│  PRIORIDAD DE COMENTARIOS                                       │
│                                                                 │
│  🔴 BLOQUEANTE (debe cambiar antes de merge)                   │
│     - API key hardcodeada en linea 45                           │
│     - SQL injection en linea 89                                 │
│     - Falta manejo de errores en linea 120                      │
│                                                                 │
│  🟡 IMPORTANTE (deberia cambiar, pero no bloquea)              │
│     - Falta tests para el servicio de pagos                    │
│     - Funcion `processPayment` hace demasiadas cosas           │
│                                                                 │
│  🟢 SUGERENCIA (mejora opcional)                               │
│     - Nombre de variable poco descriptivo                      │
│     - Podria reutilizar el widget existente                    │
└─────────────────────────────────────────────────────────────────┘
```

**Paso 3: Escribir comentarios con contexto y alternativas**

### Que NO hacer

```
❌ "This is wrong. Fix it."
❌ "There are security issues everywhere."
❌ "You should have written tests."
❌ "This code is a mess."
```

### Template de respuesta

```
"Hola Carlos, revisé el PR de pagos. Buen trabajo con la
integración de la API de Stripe. Hay algunos puntos que
necesitamos ajustar antes de merge:

🔴 BLOQUEANTE:
1. **API Key expuesta** (línea 45): Tenemos una API key
   hardcodeada. Necesitamos moverla a variables de entorno.
   Puedes usar `flutter_dotenv` que ya tenemos en el proyecto.

2. **SQL Injection** (línea 89): La query usa interpolación
   directa de strings. Usa parámetros:
   ```dart
   // Antes (peligroso)
   final query = 'SELECT * FROM users WHERE id = $userId';
   // Después (seguro)
   final query = 'SELECT * FROM users WHERE id = @userId';
   ```

🟡 IMPORTANTE:
3. **Faltan tests**: El módulo de pagos es crítico. Necesitamos
   tests para `PaymentService` y `PaymentBloc`. Mínimo 80%
   de cobertura.

4. **Función `processPayment`** (línea 120): Tiene 80 líneas
   y hace 4 cosas. Podemos extraer a funciones más pequeñas.

🟢 SUGERENCIA:
5. El widget `PaymentCard` podría reutilizar `CreditCardWidget`
   que ya existe en `lib/shared/widgets/`.

¿Necesitas ayuda con alguno de estos puntos? Podemos hacer
pair programming para el tema de tests."
```

---

## Escenario 2: Resolver Conflicto de Merge

### Contexto

Tu y Maria modificaron `lib/features/auth/presentation/screens/login_screen.dart`.
Maria agregó el botón de Google Sign-In y tu agregaste la validación de campos.
Ahora hay un conflicto de merge que necesitas resolver.

### Que hacer

**Paso 1: Entender ambos cambios**

```bash
# Ver que cambio Maria
git log --oneline main..feature/google-sign-in -- lib/features/auth/presentation/screens/login_screen.dart

# Ver tu cambio
git log --oneline main..feature/login-validation -- lib/features/auth/presentation/screens/login_screen.dart
```

**Paso 2: Actualizar tu rama**

```bash
git checkout feature/login-validation
git fetch origin
git rebase origin/feature/google-sign-in
```

**Paso 3: Resolver el conflicto**

```dart
<<<<<<< HEAD (cambio de Maria)
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: [
          EmailInput(),
          PasswordInput(),
          LoginButton(),
          const SizedBox(height: 16),
          GoogleSignInButton(),  // ← Maria agregó esto
        ],
      ),
    );
  }
=======
  Widget build(BuildContext context) {
    return Scaffold(
      body: Form(  // ← Tu agregaste Form
        key: _formKey,
        child: Column(
          children: [
            EmailInput(),
            PasswordInput(),
            LoginButton(),
          ],
        ),
      ),
    );
  }
>>>>>>> feature/login-validation
```

**Paso 4: Combinar ambos cambios**

```dart
Widget build(BuildContext context) {
  return Scaffold(
    body: Form(
      key: _formKey,
      child: Column(
        children: [
          EmailInput(),
          PasswordInput(),
          LoginButton(),
          const SizedBox(height: 16),
          GoogleSignInButton(),
        ],
      ),
    ),
  );
}
```

**Paso 5: Verificar que todo funciona**

```bash
flutter analyze
flutter test
```

**Paso 6: Continuar el rebase**

```bash
git add lib/features/auth/presentation/screens/login_screen.dart
git rebase --continue
git push --force-with-lease
```

### Que NO hacer

```
❌ git merge origin/feature/google-sign-in  (crear merge commit innecesario)
❌ git push --force  (peligro, puede borrar commits de Maria)
❌ Ignorar el conflicto y hacer push con <<<< markers
❌ Resolver sin comunicarte con Maria
```

### Template de respuesta (comunicar a Maria)

```
"Hola Maria, estoy resolviendo el conflicto de merge en
login_screen.dart. Vi que agregaste el botón de Google Sign-In
y yo agregué la validación de Form.

Estoy combinando ambos cambios: mantengo tu botón y agrego
el Form wrapper. ¿Te parece bien? Si necesitas que el
Form incluya validación específica para el botón de Google,
avísame."
```

---

## Escenario 3: Dar Feedback a Disenador sobre Limitaciones Tecnicas

### Contexto

El disenador Lucía creó una animación de 3 segundos con partículas que se mueven
individualmente, cada una con física propia. Técnicamente es posible, pero causaría
jank significativo en dispositivos低端 (低端 devices) y consumiría mucha batería.

### Que hacer

**Paso 1: Entender la intención del diseno**

¿Por que Lucía quiere esta animación? ¿Es para transmitir emociones? ¿Para
guiar la atención del usuario? La razón importa para proponer alternativas.

**Paso 2: Investigar alternativas**

| Alternativa | Fidelidad al diseno | Performance | Esfuerzo |
|------------|--------------------| -----------|---------|
| Animación completa con partículas | 100% | ❌ Mala | Alto |
| Lottie simplificado | 85% | ✅ Buena | Medio |
| Animación CSS (si es web) | 90% | ✅ Buena | Medio |
| Animación estática con shimmer | 60% | ✅ Excelente | Bajo |
| Sin animación, transición simple | 40% | ✅ Excelente | Bajo |

**Paso 3: Proponer con contexto**

### Que NO hacer

```
❌ "Eso no se puede hacer." (falso, es posible pero costoso)
❌ "Es demasiado trabajo." (no es razon tecnica)
❌ "Los usuarios no notan esas cosas." (sin datos)
❌ Ignorar el diseno y hacer algo diferente sin consultar
```

### Template de respuesta

```
"Hola Lucía, revisé la animación de partículas para la
pantalla de bienvenida. La idea es genial — transmite
exactamente la energía que buscamos.

Encontré una limitación técnica que quiero compartir:
la animación con 50+ partículas individuales con física
propia puede causar frames dropped en dispositivos
medianos (ej: Pixel 6a, iPhone SE). El target de 60fps
sería difícil de mantener.

Encontré estas alternativas que mantienen la esencia:

**Opción 1: Lottie simplificado** (85% fidelidad)
- Usamos After Effects + Bodymovin para exportar
- Mantiene el movimiento de partículas
- Performance: excelente en todos los dispositivos
- Esfuerzo: 2-3 días

**Opción 2: Shimmer estático** (60% fidelidad)
- Fondo con gradientes animados
- Sensación de movimiento sin partículas
- Performance: excelente
- Esfuerzo: 1 día

¿Cuál te parece? Si prefieres la animación completa,
podemos intentarla, pero necesitaría un POC para
verificar performance en devices reales."
```

---

## Escenario 4: Estimar Feature para el Sprint

### Contexto

El PM te pide una estimación para el feature "Chat en tiempo real" que incluye:
mensajes de texto, imágenes, notificaciones push, y historial de mensajes.

### Que hacer

**Paso 1: Descomponer en sub-tareas**

```
┌─────────────────────────────────────────────────────────────────┐
│  FEATURE: CHAT EN TIEMPO REAL                                   │
│                                                                 │
│  SUB-TAREAS:                                                    │
│  ├── UI                                                         │
│  │   ├── Chat screen (burbujas de mensaje)          → M        │
│  │   ├── Input de texto + boton enviar              → S        │
│  │   ├── Selector de imágenes                       → M        │
│  │   ├── Lista de conversaciones                    → M        │
│  │   └── Empty states y loading states              → S        │
│  │                                                              │
│  ├── Backend                                                    │
│  │   ├── Supabase Realtime subscription             → M        │
│  │   ├── Tabla de mensajes (RLS policies)           → S        │
│  │   ├── Storage para imágenes                      → M        │
│  │   └── Índices para performance                   → S        │
│  │                                                              │
│  ├── Features                                                   │
│  │   ├── Notificaciones push                        → L        │
│  │   ├── Historial con paginación                   → M        │
│  │   ├── Typing indicators                          → S        │
│  │   └── Read receipts                              → S        │
│  │                                                              │
│  ├── Testing                                                    │
│  │   ├── Unit tests (BLoC, services)                → M        │
│  │   ├── Widget tests (UI)                          → S        │
│  │   └── Integration tests (flujo completo)         → M        │
│  │                                                              │
│  └── Infra                                                      │
│      ├── Supabase Realtime config                     → S        │
│      ├── Push notifications setup (FCM/APNs)         → M        │
│      └── Monitoreo y alertas                          → S        │
└─────────────────────────────────────────────────────────────────┘
```

**Paso 2: Estimar cada sub-tarea**

| Sub-tarea | Tamaño | Horas estimadas | Notas |
|-----------|--------|----------------|-------|
| Chat screen UI | M | 8-12h | Burbujas, scroll, responsive |
| Input de texto | S | 2-4h | TextField + enviar |
| Selector de imágenes | M | 6-8h | image_picker + preview |
| Lista de conversaciones | M | 6-8h | ListView con avatar, ultimo mensaje |
| Empty/loading states | S | 2-3h | Skeleton, empty illustration |
| Supabase Realtime | M | 6-8h | subscriptions, manejo de estados |
| Tabla mensajes + RLS | S | 3-4h | Schema + security policies |
| Storage imágenes | M | 4-6h | Upload, compression, CDN |
| Índices | S | 1-2h | Performance optimization |
| Notificaciones push | L | 12-16h | FCM/APNs, topics, deep linking |
| Historial paginado | M | 4-6h | Cursor-based pagination |
| Typing indicators | S | 2-3h | Realtime broadcast |
| Read receipts | S | 2-3h | Simple flag update |
| Unit tests | M | 6-8h | BLoC + services |
| Widget tests | S | 3-4h | Key screens |
| Integration tests | M | 6-8h | End-to-end flow |
| Supabase config | S | 2-3h | Realtime setup |
| Push setup | M | 4-6h | FCM + APNs |
| Monitoreo | S | 2-3h | Logs + alerts |

**Paso 3: Identificar unknowns**

| Unknown | Impacto | Como resolver |
|---------|---------|---------------|
| ¿Supabase Realtime soporta X concurrentes? | Alto | Hacer POC de performance |
| ¿image_picker funciona bien en todas las plataformas? | Medio | Probar en Android + iOS |
| ¿Las notificaciones push funcionan con background handlers? | Alto | POC con FCM |

**Paso 4: Dar la estimación**

### Que NO hacer

```
❌ "Toma 2 semanas." (sin descomponer, sin explicar)
❌ "No sé, depende." (no es util para nadie)
❌ "Lo hago en 3 días." (underestimate por querer parecer rapido)
❌ No mencionar unknowns ni riesgos
```

### Template de respuesta

```
"Hola [PM], desglose el feature de Chat en Tiempo Real.
Aquí va la estimación:

**Estimación total: 3-4 semanas** (1 developer full-time)

**Desglose:**
| Area | Tamaño | Horas |
|------|--------|-------|
| UI (5 pantallas) | L | 24-35h |
| Backend + Realtime | M | 15-22h |
| Features (push, history) | L | 18-25h |
| Testing | M | 15-20h |
| Infra + Config | S | 8-12h |
| **Buffer (20%)** | | **~15h** |

**Unknowns que necesito resolver:**
1. Performance de Supabase Realtime con X usuarios concurrentes
2. Comportamiento de image_picker en Android+iOS
3. Background handlers para notificaciones

**Lo que puedo entregar en el Sprint 1 (1 semana):**
- Chat screen + input de texto
- Supabase Realtime connection
- Tabla de mensajes

**Lo que queda para Sprint 2:**
- Notificaciones push
- Selector de imágenes
- Historial paginado

¿Quieres que empiece con el POC de Realtime esta semana?"
```

---

## Escenario 5: Reportar Bug Critico al Equipo

### Contexto

Encontraste un bug en producción: cuando un usuario realiza un pago, a veces se
cobra dos veces. Es un bug de race condition en el backend. Necesitas comunicar
la urgencia sin causar pánico.

### Que hacer

**Paso 1: Verificar que es un bug real**

```bash
# Revisar logs de Supabase
# Buscar transacciones duplicadas
SELECT user_id, amount, created_at, 
       COUNT(*) as duplicate_count
FROM payments 
WHERE created_at > NOW() - INTERVAL '24 hours'
GROUP BY user_id, amount, created_at
HAVING COUNT(*) > 1;
```

**Paso 2: Cuantificar el impacto**

```
┌─────────────────────────────────────────────────────────────────┐
│  BUG: PAGOS DUPLICADOS                                          │
│                                                                 │
│  Impacto:                                                       │
│  - Usuarios afectados: 12 en las ultimas 24 horas              │
│  - Monto total duplicado: $847.00 USD                          │
│  - Frecuencia: ~1% de los pagos (1 de cada 100)               │
│  - Severidad: CRITICA - impacto financiero directo             │
│                                                                 │
│  Causa: Race condition en la funcion de procesamiento de pagos  │
│  cuando el usuario toca "Pagar" dos veces rapidamente           │
└─────────────────────────────────────────────────────────────────┘
```

**Paso 3: Comunicar con el formato correcto**

### Que NO hacer

```
❌ "URGENTE!!! HAY UN BUG EN PRODUCCIÓN!!! TODO ESTA CAIDO!!!"
   (causa pánico innecesario)

❌ "Creo que hay un problema con los pagos, no estoy seguro"
   (poco profesional, no transmite urgencia)

❌ "El backend tiene un bug, arreglenlo ya"
   (sin contexto, sin propuesta de solución)

❌ Esconder el bug para "no preocupar al equipo"
   (irresponsable)
```

### Template de respuesta

```
"🚨 **Bug Crítico: Pagos Duplicados en Producción**

**Severidad:** P0 - Impacto financiero directo
**Estado:** Investigando
**Responsable:** Yo

**Resumen:**
Encontré una race condition que causa pagos duplicados.
Cuando un usuario toca "Pagar" dos veces rápidamente,
el backend procesa ambos pagos.

**Impacto:**
- 12 usuarios afectados en las últimas 24h
- $847 USD en cargos duplicados
- ~1% de los pagos

**Mitigación inmediata (ya implementada):**
- Agregué debounce de 3 segundos en el botón de pagar
- Esto previene nuevos duplicados

**Fix definitivo (necesito):**
- Agregar idempotency key en la función de procesamiento
- Lock a nivel de base de datos para transacciones concurrentes
- Estimación: 4-6 horas

**Reversión de cargos:**
Necesito que [persona del equipo financiero] procese
los reembolsos de los 12 usuarios afectados.

¿Quién puede ayudarme con el fix del backend? Necesito
par de manos para implementar el lock a nivel de DB."
```

---

## Resumen de Escenarios

```
┌─────────────────────────────────────────────────────────────────┐
│  ESCENARIOS: PATRON COMUN                                      │
│                                                                 │
│  1. CODE REVIEW → Clasificar por prioridad, dar alternativas   │
│  2. MERGE CONFLICT → Entender ambos lados, combinar, verificar │
│  3. FEEDBACK A DISEÑADOR → Entender intención, proponer options│
│  4. ESTIMACIÓN → Descomponer, identificar unknowns, ser honesto│
│  5. BUG CRÍTICO → Verificar, cuantificar, mitigar, comunicar  │
│                                                                 │
│  EN COMUN:                                                      │
│  ✅ Contexto primero, opiniones después                        │
│  ✅ Datos concretos, no suposiciones                           │
│  ✅ Propuestas de solución, no solo problemas                  │
│  ✅ Comunicar con calma, incluso en urgencia                   │
│  ✅ Involucrar al equipo, no trabajar en silo                  │
└─────────────────────────────────────────────────────────────────┘
```
