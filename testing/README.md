# 🧪 Guía Completa de Testing para Clean Architecture

Guía paso a paso para aprender a testear aplicaciones Flutter con Clean Architecture usando **Fakes Manuales**.

---

## 📚 Estructura de la Guía

### 🎯 Para principiantes (Start here!)

| Parte | Tema | Qué aprenderás |
|-------|------|----------------|
| **1** | [Fundamentos](./01-fundamentos.md) | Patrón AAA, matchers, estructura básica |
| **2** | [Domain Testing](./02-domain-testing.md) | Entities, UseCases, Fakes manuales |

### 🏗️ Capas de la aplicación

| Parte | Tema | Qué aprenderás |
|-------|------|----------------|
| **3** | [Data Testing](./03-data-testing.md) | Models, Repositories, DataSources, Fixtures |
| **4** | [Presentation Testing](./04-presentation-testing.md) | Cubits con bloc_test, Widgets |
| **5** | [Core Testing](./05-core-testing.md) | NetworkInfo, Services, Storage, Utils |

### 🚀 Avanzado

| Parte | Tema | Qué aprenderás |
|-------|------|----------------|
| **6** | [Testing Avanzado](./06-advanced-testing.md) | Integration tests, Coverage, CI/CD |
| **7** | [Migración a Mockito](./07-migration-to-mockito.md) | Cuándo y cómo migrar |

---

## 🚀 Cómo usar esta guía

### Si eres nuevo en testing:
1. Lee la **Parte 1** completamente
2. Sigue los ejercicios prácticos
3. Pasa a la **Parte 2** y practica con tu feature de auth

### Si ya tienes experiencia:
1. Ve directo a la parte que necesites
2. Consulta los ejemplos de código
3. Adapta a tu proyecto

### Ruta recomendada:
```
Parte 1 → Parte 2 → Parte 3 → Parte 4 → Parte 6
```

---

## 📁 Estructura de Archivos

```
docs/testing/
├── README.md                      ← Este archivo
├── 01-fundamentos.md              ← Fundamentos del testing
├── 02-domain-testing.md           ← Testing Domain
├── 03-data-testing.md             ← Testing Data
├── 04-presentation-testing.md     ← Testing Presentation
├── 05-core-testing.md             ← Testing Core
├── 06-advanced-testing.md         ← Testing Avanzado
└── 07-migration-to-mockito.md     ← Migración a Mockito
```

---

## 🎯 Objetivos de Aprendizaje

Al completar esta guía serás capaz de:

✅ Escribir tests siguiendo el patrón AAA  
✅ Crear Fakes manuales para testing  
✅ Testear Entities, UseCases, y Repositories  
✅ Testear Models con fixtures JSON  
✅ Testear Cubits con bloc_test  
✅ Testear Widgets con interacciones  
✅ Medir y mejorar cobertura de código  
✅ Configurar CI/CD con GitHub Actions  
✅ Decidir cuándo migrar a Mockito  

---

## 🛠️ Requisitos Previos

- Flutter instalado (3.0+)
- Conocimientos básicos de Dart
- Proyecto con Clean Architecture
- Tu proyecto usa `lib/clean/` estructura

---

## 📦 Dependencias Necesarias

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  bloc_test: ^9.1.0          # Para Cubits
  mockito: ^5.4.0            # Para tests avanzados
  build_runner: ^2.4.0       # Si usas @GenerateMocks
```

---

## 🎓 Metodología

Cada parte de la guía incluye:

1. **Teoría breve** - Conceptos clave
2. **Ejemplos completos** - Código copiable
3. **Explicación paso a paso** - Línea por línea
4. **Ejercicios prácticos** - Para practicar
5. **Checklist** - Para verificar progreso

---

## 💡 Consejos Rápidos

### Antes de empezar:
- ✅ Asegúrate de tener tu proyecto funcionando
- ✅ Lee primero la Parte 1 completa
- ✅ No te saltes los ejercicios

### Mientras aprendes:
- 📝 Toma notas de los conceptos clave
- 🔨 Practica escribiendo tests reales
- ❓ Si algo no funciona, revisa el código paso a paso

### Después de aprender:
- 📊 Mide tu cobertura con `flutter test --coverage`
- 🚀 Configura CI/CD para automatizar tests
- 📚 Comparte lo aprendido con tu equipo

---

## 🆘 ¿Necesitas ayuda?

### Problemas comunes:

**Tests no ejecutan:**
```bash
flutter pub get
flutter clean
flutter pub get
```

**Error con build_runner:**
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

**Coverage no genera:**
```bash
# Instala lcov
brew install lcov  # macOS
sudo apt-get install lcov  # Linux
```

---

## 📖 Glosario Rápido

| Término | Significado |
|---------|-------------|
| **AAA** | Arrange-Act-Assert (patrón de testing) |
| **Fake** | Implementación de prueba de una interfaz |
| **Mock** | Objeto simulado generado automáticamente |
| **Fixture** | Datos de prueba reutilizables (JSON) |
| **Coverage** | Porcentaje de código cubierto por tests |
| **E2E** | End-to-End (test de flujo completo) |
| **CI/CD** | Integración y despliegue continuos |

---

## 🎉 Comencemos

👉 [Ir a Parte 1: Fundamentos](./01-fundamentos.md)

¡Buena suerte en tu viaje de testing! 🚀

---

## 📝 Notas del Autor

Esta guía fue creada específicamente para el proyecto **Sereni** que usa:
- Clean Architecture en `lib/clean/`
- BLoC/Cubit para estado
- Fakes manuales (estilo preferido)
- Supabase como backend

Los ejemplos usan el feature de **Auth** como referencia, pero los conceptos aplican a cualquier feature.

---

## 📄 Licencia

Esta guía es libre de usar y modificar para tu proyecto.

---

**Última actualización:** 2026-02-13  
**Versión:** 1.0.0
