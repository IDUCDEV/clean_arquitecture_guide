# Ejercicios de Práctica

> 6 ejercicios para aplicar el framework de 6 fases sin IA. Cada uno tiene un nivel de dificultad creciente.

---

## Instrucciones generales

1. **Elige un ejercicio** según tu nivel actual
2. **Sigue las 6 fases** del framework (Investigar → Diseñar → Implementar → Verificar → Refactor → Validar)
3. **No uses IA** hasta la Fase 6 (Validar)
4. **Documenta tu proceso** en un archivo markdown
5. **Mide tu tiempo** — ¿cuánto tardaste en cada fase?

---

## Ejercicio 1: Lista de tareas (CRUD simple)
**Nivel:** Principiante | **Tiempo estimado:** 2-3 horas

### Feature
Implementa una app de lista de tareas con:
- Crear tarea (título + fecha límite)
- Marcar como completada
- Eliminar tarea
- Filtrar: todas / pendientes / completadas

### Restricciones
- Usa Supabase para persistencia
- Clean Architecture (Domain, Data, Presentation)
- State management con BLoC o Provider
- Un solo usuario (sin autenticación)

### Qué practicas
- CRUD básico con Supabase
- Estados simples
- Filtrado de datos
- Validación de formulario

### Criterios de evaluación
- [ ] Código compila sin errores
- [ ] Las 4 operaciones CRUD funcionan
- [ ] Filtrado funciona correctamente
- [ ] Manejo de errores básico (sin conexión)
- [ ] Tests unitarios para use cases

---

## Ejercicio 2: Calculator de propinas
**Nivel:** Principiante-Intermedio | **Tiempo estimado:** 3-4 horas

### Feature
Implementa una calculadora de propinas:
- Ingresar monto de la cuenta
- Seleccionar porcentaje de propina (10%, 15%, 20%, personalizado)
- Dividir entre N personas
- Mostrar desglose: subtotal, propina, total, por persona

### Restricciones
- Todo cálculo en el dominio (no en la UI)
- Clean Architecture
- Tests para la lógica de cálculo
- Sin dependencias externas (solo Dart/Flutter)

### Qué practicas
- Lógica de negocio pura
- Separación de capas
- Tests unitarios
- Diseño de interfaces simples

### Criterios de evaluación
- [ ] Cálculos son correctos
- [ ] Propina personalizada funciona
- [ ] División entre personas funciona
- [ ] Tests cubren todos los escenarios
- [ ] Código es legible y está bien organizado

---

## Ejercicio 3: Lista de contactos con búsqueda
**Nivel:** Intermedio | **Tiempo estimado:** 4-5 horas

### Feature
Implementa una agenda de contactos:
- CRUD de contactos (nombre, teléfono, email, foto opcional)
- Búsqueda en tiempo real por nombre
- Ordenar por: nombre, fecha de creación
- Contactos favoritos (star/favorite)
- Detalle del contacto con opciones de llamar/email

### Restricciones
- Supabase para persistencia
- Clean Architecture
- BLoC para estado
- Manejo de permisos de cámara (para foto)

### Qué practicas
- Búsqueda con debounce
- Múltiples operaciones de lectura
- Manejo de permisos
- Navegación con parámetros

### Criterios de evaluación
- [ ] CRUD completo funciona
- [ ] Búsqueda filtra correctamente
- [ ] Favoritos se guardan y persisten
- [ ] Permisos se manejan correctamente
- [ ] Tests para lógica de búsqueda

---

## Ejercicio 4: Weather app
**Nivel:** Intermedio | **Tiempo estimado:** 5-7 horas

### Feature
Implementa una app del clima:
- Obtener ubicación actual
- Mostrar clima actual (temperatura, condición, humedad, viento)
- Pronóstico de 5 días
- Pull-to-refresh
- Manejo de ubicación no disponible

### Restricciones
- API pública: OpenWeatherMap (https://openweathermap.org/api)
- Clean Architecture
- Manejo de estados de carga
- Cache de datos (último clima conocido)
- Offline-first

### Qué practicas
- Integración con API externa
- Manejo de permisos de ubicación
- Cache y persistencia local
- Estados de carga complejos

### Criterios de evaluación
- [ ] Obtiene ubicación correctamente
- [ ] Muestra clima actual
- [ ] Pronóstico se muestra
- [ ] Funciona sin conexión (muestra cache)
- [ ] Maneja errores de red
- [ ] Tests para repository

---

## Ejercicio 5: Chat con WebSockets
**Nivel:** Intermedio-Avanzado | **Tiempo estimado:** 7-10 horas

### Feature
Implementa un chat básico:
- Conexión WebSocket
- Enviar mensajes en tiempo real
- Recibir mensajes en tiempo real
- Historial de mensajes (últimos 50)
- Estados: conectado / desconectando / error
- Reconexión automática

### Restricciones
- Supabase Realtime o WebSocket propio
- Clean Architecture
- BLoC para estados
- Manejo de reconexión
- Mensajes persistidos en BD

### Qué practicas
- WebSockets / Realtime
- Manejo de conexiones
- Estados asíncronos
- Reconexión automática
- Persistencia de mensajes

### Criterios de evaluación
- [ ] Conexión WebSocket funciona
- [ ] Mensajes se envían y reciben
- [ ] Historial se carga
- [ ] Reconexión funciona tras desconexión
- [ ] Estados se manejan correctamente
- [ ] No hay memory leaks en suscripciones

---

## Ejercicio 6: Shopping cart con pagos simulados
**Nivel:** Avanzado | **Tiempo estimado:** 10-14 horas

### Feature
Implementa un carrito de compras completo:
- Catálogo de productos (10+ productos)
- Agregar/quitar del carrito
- Cantidades editables
- Cálculo de total
- Checkout con formulario de envío
- Pago simulado (no real)
- Confirmación de pedido
- Historial de pedidos

### Restricciones
- Supabase para persistencia
- Clean Architecture completo
- Múltiples pantallas con navegación
- State management robusto (BLoC/Riverpod)
- Manejo de errores completo
- Tests para lógica de negocio

### Qué practicas
- Feature completa end-to-end
- Múltiples entidades relacionadas
- Estados complejos
- Navegación múltiple
- Manejo de errores en múltiples capas

### Criterios de evaluación
- [ ] Catálogo muestra productos
- [ ] Carrito agrega/quita productos
- [ ] Cantidades se editan correctamente
- [ ] Total se calcula correctamente
- [ ] Checkout completa el pedido
- [ ] Pedidos se guardan y persisten
- [ ] Manejo de errores en cada paso
- [ ] Tests para lógica de negocio

---

## Registro de progreso

### Tabla de seguimiento

| Ejercicio | Nivel | Iniciado | Completado | Tiempo real | Notas |
|-----------|-------|----------|------------|-------------|-------|
| 1. Lista de tareas | Principiante | | | | |
| 2. Calculadora propinas | P-Intermedio | | | | |
| 3. Contactos búsqueda | Intermedio | | | | |
| 4. Weather app | Intermedio | | | | |
| 5. Chat WebSocket | I-Avanzado | | | | |
| 6. Shopping cart | Avanzado | | | | |

### Métricas a跟踪ar

```
Tiempo por fase:
- Investigar: ___ min
- Diseñar: ___ min
- Implementar: ___ min
- Verificar: ___ min
- Refactor: ___ min
- Validar (con IA): ___ min

Total: ___ horas

Nivel de confianza (1-10): ___
Cosas que aprendí: ___
Errores que cometí: ___
```

---

**Siguiente:** [13-checklists-y-plantillas.md](./13-checklists-y-plantillas.md) — Plantillas y checklists para cada fase
