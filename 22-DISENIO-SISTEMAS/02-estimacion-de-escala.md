# 02: Estimación de Escala (Back-of-the-Envelope)

> Traducir usuarios en **requests por segundo, almacenamiento y ancho de banda**. Se llama "back-of-the-envelope" porque se hace a mano, en el dorso de un sobre, con números redondos.

---

## ¿Por qué estimar?

Estimar antes de diseñar te dice:
- Cuántos servidores/instancias necesitas (coste).
- Si una sola base de datos aguanta o necesitas replicación/sharding.
- Si necesitas CDN para imágenes/videos.
- Si el diseño es viable en la nube elegida (Supabase, AWS, etc.).

*Fuente: System Design Primer — "Back-of-the-envelope calculations".*

---

## Tablas de referencia REALES (no inventadas)

Estas son las tablas que cita el System Design Primer. **No las improvises** en una entrevista: memorízalas.

### Potencias de 2 (referencia rápida)

| Abreviatura | Bytes | Valor |
|---|---|---|
| KB | 2^10 | 1,024 |
| MB | 2^20 | ~1 millón |
| GB | 2^30 | ~1 billón |
| TB | 2^40 | ~1 trillón |

### Números de latencia que todo programador debería saber (2020)

| Operación | Tiempo |
|---|---|
| Lectura de caché en memoria | ~1 ns |
| Compresión/decompresión de 1 KB | ~1-2 µs |
| Lectura secuencial de 1 MB en RAM | ~9 µs |
| Round-trip de datacenter (misma región) | ~500 µs |
| Búsqueda de 1 MB secuencial en SSD | ~150 µs |
| Disco rotativo (seek + lectura 1 MB) | ~2-4 ms |
| Round-trip en Internet (EE.UU. → Europa) | ~150 ms |
| Round-trip en Internet (EE.UU. → Asia) | ~200 ms |

> ⚠️ Estos valores los publica el System Design Primer y la comunidad los actualiza periódicamente. Al citarlos, referencia la fuente; son órdenes de magnitud, no medidas exactas.

---

## Método de 4 pasos

```
1. Encuentra los números base  → usuarios, uso diario
2. Calcula requests/segundo    → QPS promedio y pico
3. Calcula almacenamiento      → bytes por día y por año
4. Calcula ancho de banda      → bytes por segundo
```

---

## Ejemplo completo: feed de 500k usuarios

Datos de entrada (de la clarificación del archivo 01):

```
Usuarios registrados : 500,000
Usuarios activos     : 50,000 DAU
Uso por usuario/día  : 10 lecturas (scroll de feed) + 1 escritura (post)
Tamaño de un post    : 1 KB de texto + 500 KB de imagen (media)
```

### Paso 2: QPS

```
Lecturas/día  = 50,000 × 10 = 500,000 lecturas
Escrituras/día = 50,000 × 1  = 50,000 escrituras
Total/día     = 550,000

Segundos en un día = 86,400

QPS promedio  = 550,000 / 86,400 ≈ 6.4 QPS
QPS pico      = 6.4 × 5 (factor de pico) ≈ 32 QPS
```

**Interpretación:** ~32 QPS pico es un número pequeño. Una sola instancia bien configurada lo soporta. La complejidad real vendrá de la **data acumulada** y de **medios**, no del volumen de requests.

### Paso 3: Almacenamiento

```
Posts por día = 50,000
Texto/día     = 50,000 × 1 KB  = 50 MB/día
Imágenes/día  = 50,000 × 500 KB = 25 GB/día
Total/día     ≈ 25 GB/día (dominado por las imágenes)

Total/año     ≈ 25 GB × 365 ≈ 9.1 TB/año
```

**Interpretación:** 9 TB/año es mucho. Las imágenes **no deben vivir en la base de datos**: van a un object storage (Supabase Storage) servido por CDN. En Postgres solo guardamos la URL.

### Paso 4: Ancho de banda

```
QPS promedio = 6.4
Bytes/request ≈ 500 KB (una imagen por request)

Entrada de escrituras ≈ 50,000 × 500 KB / 86,400 s ≈ 290 KB/s
Salida de lecturas   ≈ 500,000 × 500 KB / 86,400 s ≈ 2.9 MB/s promedio
Salida en pico (32 QPS) ≈ 32 × 500 KB ≈ 16 MB/s
```

**Interpretación:** la salida de 2.9 MB/s promedio (16 MB/s pico) justifica un CDN: los usuarios reciben las imágenes desde el edge más cercano y el backend deja de gastar ese ancho de banda.

---

## Conclusión del diseño (qué nos dice la estimación)

| Hallazgo | Decisión de diseño |
|---|---|
| QPS pico bajo (~32) | Una instancia de app basta en el inicio |
| 9 TB/año de imágenes | Imágenes → Storage + CDN, nunca en la DB |
| Ratio lectura/escritura 10:1 | Cachear el feed de lecturas |
| Picos 5× promedio | Margen de capacidad y auto-scaling |

Este es el ciclo completo: **clarificar → estimar → diseñar informado**.

---

## Errores comunes

| Error | Solución |
|---|---|
| Calcular QPS sin aclarar usuarios | Primero clarifica, luego estima |
| Guardar imágenes en la DB | Separar media (Storage/CDN) de metadatos (DB) |
| Redondear mal los órdenes de magnitud | Usar las potencias de 2 de referencia |
| Confundir MB con MB decimales | Ser consistente: usar 2^20 = 1,048,576 bytes |
| No declarar suposiciones | Escribir los números base antes de operar |

---

## Fuentes

- [The System Design Primer — Back-of-the-envelope calculations](https://github.com/donnemartin/system-design-primer#back-of-the-envelope-calculations)
- [The System Design Primer — Powers of two table](https://github.com/donnemartin/system-design-primer#appendix)
- [Grokking Modern System Design Interview — Back-of-the-Envelope Calculations](https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers)

---

**Siguiente:** [03-componentes-arquitectura.md](./03-componentes-arquitectura.md)
