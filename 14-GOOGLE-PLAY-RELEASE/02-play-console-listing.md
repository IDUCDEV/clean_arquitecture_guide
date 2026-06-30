# 02 - Play Console: Crear Listing

> Configura la ficha de tu app en Google Play Store: nombre, descripción, screenshots, categoría, y contenido.

---

## 1. Cuenta de Desarrollador

### 1.1 Requisitos

```bash
# Lo que necesitas:
# 1. Cuenta de Google (gmail)
# 2. Pago único de $25 USD (registro de desarrollador)
# 3. 15-30 minutos para completar el registro
```

### 1.2 Crear Cuenta

1. Ir a [play.google.com/console](https://play.google.com/console)
2. Aceptar el Acuerdo de Distribución para Desarrolladores
3. Pagar la tarifa de registro ($25 USD, único pago)
4. Completar perfil de desarrollador

---

## 2. Crear Nueva App

### 2.1 Información Básica

En Play Console:
1. Botón "Crear app"
2. Seleccionar idioma predeterminado
3. Completar:

| Campo | Ejemplo |
|-------|---------|
| **Nombre** | Rifa Gestión |
| **Tipo** | Aplicación |
| **Categoría** | Productividad |

### 2.2 Dashboard

```
├── Panel principal
├── Presencia en Google Play
│   ├── Ficha de Play Store      ← Aquí configuras el listing
│   ├── Permisos de clasificación
│   └── Segmentación
├── Lanzamiento
│   ├── Versiones                ← Aquí subes los AABs
│   └── Pruebas
└── Configuración avanzada
```

---

## 3. Ficha de Play Store

### 3.1 Datos del Producto

| Sección | Requerido | Descripción |
|---------|-----------|-------------|
| Nombre | Sí | Hasta 50 caracteres |
| Descripción breve | Sí | Hasta 80 caracteres |
| Descripción completa | Sí | Hasta 4000 caracteres |

**Ejemplo:**

```
Nombre: Rifa Gestión
Descripción breve: Gestiona rifas, loterías y sorteos desde tu móvil
Descripción completa:
  Rifa Gestión es la herramienta perfecta para administrar rifas,
  loterías y sorteos de forma fácil y profesional.

  Características:
  • Creación rápida de rifas
  • Venta de boletos con seguimiento en tiempo real
  • Generación de reportes y estadísticas
  • Sorteos automáticos con números aleatorios
  • Notificaciones a ganadores
  • Sincronización en la nube
  • Exportación de resultados a PDF

  Ideal para: escuelas, iglesias, organizaciones benéficas,
  clubes deportivos y cualquier grupo que quiera recaudar
  fondos de manera organizada.
```

### 3.2 Recursos Gráficos

| Recurso | Tamaño | Formato | Descripción |
|---------|--------|---------|-------------|
| Icono | 512x512 | 32-bit PNG | Logo de la app |
| Feature graphic | 1024x500 | PNG/JPG | Banner en Play Store |
| Screenshots de teléfono | Mínimo 2 | PNG/JPG | Capturas de pantalla |
| Screenshots de tablet | Opcional | PNG/JPG | Para tablets |
| Video destacado | Opcional | YouTube URL | Video promocional |

**Recomendaciones:**
- Screenshots: 4-8 capturas mostrando las pantallas principales
- Texto en screenshots: español (o el idioma del listing)
- Feature graphic: sin texto importante (se recorta en diferentes tamaños)

### 3.3 Categorización

| Sección | Opciones |
|---------|----------|
| Categoría | Productividad, Negocios, etc. |
| Etiquetas | Hasta 5 (ej: rifas, lotería, sorteos) |
| Segmentación etaria | Según contenido de la app |
| Sitio web | Opcional |
| Política de privacidad | Requerida si la app recolecta datos |

---

## 4. Clasificación de Contenido

### 4.1 Cuestionario

Play Console te guía por un cuestionario sobre:
- Violencia
- Contenido sexual
- Lenguaje soez
- Juegos de azar → **Importante para apps de rifas**
- Contenido generado por usuarios
- Compra dentro de la app
- Información personal

### 4.2 Para Apps de Rifas/Sorteos

Responder con honestidad. Si la app maneja rifas reales:
- Marcar "Juegos de azar" si aplica
- Verificar regulaciones locales
- La clasificación puede ser "Para mayores de 18 años"

---

## 5. Política de Privacidad

### 5.1 ¿Necesitas una?

Si tu app recolecta:
- Correo electrónico
- Nombre
- Fotos
- Ubicación
- CUALQUIER dato personal

→ **Sí, necesitas una política de privacidad.**

### 5.2 Template

```markdown
# Política de Privacidad
Última actualización: [Fecha]

## Información que recopilamos
- Nombre y correo electrónico (registro)
- Datos de uso de la app
- Información del dispositivo

## Cómo usamos la información
- Proveer el servicio de gestión de rifas
- Mejorar la app
- Enviar notificaciones importantes

## Almacenamiento de datos
Los datos se almacenan en [Supabase/Google Cloud/Firebase]
y se eliminan cuando el usuario elimina su cuenta.

## Contacto
[tu-email@ejemplo.com]
```

**Alojarla en:** GitHub Pages, Google Drive, o tu propio sitio.

---

## 6. Pre-lanzamiento: Checklist

```markdown
## Checklist Pre-lanzamiento

### Obligatorio
- [ ] Cuenta de desarrollador creada y activa
- [ ] App firmada con keystore
- [ ] AAB generado correctamente
- [ ] Ficha completa (nombre, descripción, screenshots)
- [ ] Icono y feature graphic
- [ ] Clasificación de contenido completada
- [ ] Política de privacidad
- [ ] Pricing: Gratuita o Paga

### Recomendado
- [ ] Probar en dispositivo físico (no emulador)
- [ ] Probar en Android 13, 14, 15
- [ ] Probar sin conexión
- [ ] Verificar permisos (mínimos necesarios)
- [ ] Traducciones si aplica
- [ ] Video promocional
- [ ] Sitio web de la app

### Técnico
- [ ] versionName y versionCode correctos
- [ ] ProGuard/R8 habilitado (ofuscación)
- [ ] Tamaño del AAB < 150MB
- [ ] API level mínimo correcto
- [ ] Permisos justificados
```

---

## 7. Traducciones

Play Console permite agregar traducciones automáticas o manuales:

```bash
# Desde el dashboard:
# 1. Ir a "Presencia en Google Play" > "Traducciones"
# 2. Agregar idioma
# 3. Traducir: nombre, descripción breve, descripción completa
# 4. Subir screenshots traducidos
```

**Idiomas recomendados:** Español, Inglés (mínimo).

---

## 8. Resumen

1. **Cuenta de $25 USD** = pago único
2. **Ficha completa** = nombre, descripción, screenshots
3. **Política de privacidad** necesaria si recolectas datos
4. **Clasificación de contenido** según tipo de app
5. **Checklist pre-lanzamiento** para evitar rechazos
6. **Traducciones** mejoran el alcance

---

## Recursos

- [Play Console](https://play.google.com/console)
- [Política de privacidad template](https://privacypolicytemplate.net/)
- [Android App Quality Guidelines](https://developer.android.com/docs/quality-guidelines)
