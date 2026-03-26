# 🧪 Guía Completa de Testing para Clean Architecture en Flutter

> **¿Por qué esta guía?** Aprende a testear cada capa de Clean Architecture desde cero, con teoría clara y ejercicios prácticos paso a paso. Usamos **Fakes manuales** porque son más fáciles de entender que los mocks automáticos.

---

## 🎯 ¿Cómo usar esta guía?

### Método recomendado: Leyendo y Practicando

Cada parte tiene **dos archivos**:
- **Archivo de Teoría** (número): Explica el "por qué" y muestra ejemplos completos
- **Archivo de Práctica** (número + "a"): Ejercicios guiados paso a paso

```
01-fundamentos.md      →  01a-practica-primeros-tests.md
02-domain-testing.md   →  02a-practica-fakes-manuales.md
02b-intro-mockito.md   →  02b-practica-mockito.md
03-data-testing.md    →  03a-practica-fixtures-models.md
                        →  03b-practica-datasources.md
                        →  03c-practica-repositories.md
```

### Ruta de Aprendizaje Sugerida

```
SEMANA 1: Fundamentos + Domain
├── 01-fundamentos.md + 01a-practica-primeros-tests.md
└── 02-domain-testing.md + 02a-practica-fakes-manuales.md

SEMANA 1b: Mockito (Avanzado - Después de dominar Fakes)
├── 02b-intro-mockito.md + 02b-practica-mockito.md

SEMANA 2: Data Layer
├── 03-data-testing.md + 03a-practica-fixtures-models.md
├── 03b-practica-datasources.md
└── 03c-practica-repositories.md

SEMANA 3: Presentation
├── 04-presentation-testing.md + 04a-practica-cubits-bloc-test.md
└── 04b-practica-widgets.md

SEMANA 4: Core + Avanzado
├── 05-core-testing.md + 05a-practica-core-services.md
└── 06-advanced-testing.md + 06a-practica-coverage-ci.md
```

### ¿Cuánto tiempo necesitas?

| Parte | Teoría | Práctica | Total |
|-------|--------|----------|-------|
| Fundamentos | 20 min | 30 min | ~1 hora |
| Domain (Fakes) | 30 min | 45 min | ~1.5 horas |
| Mockito (Avanzado) | 45 min | 1 hora | ~1.5 horas |
| Data (3 archivos) | 45 min | 1 hora | ~2 horas |
| Presentation | 30 min | 45 min | ~1.5 horas |
| Core | 15 min | 30 min | ~45 min |
| Avanzado | 20 min | 30 min | ~1 hora |

---

## 📚 Estructura Completa de la Guía

### 🅰️ PARTE 1: FUNDAMENTOS

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| [01-fundamentos.md](./01-fundamentos.md) | Teoría | Conceptos base, patrón AAA, setup |
| [01a-practica-primeros-tests.md](./01a-practica-primeros-tests.md) | Práctica ✏️ | Ejercicios con funciones puras |

**Objetivos:** Entender qué es un test, patrón AAA, matchers básicos

---

### 🅰️ PARTE 2: DOMAIN (Lógica de Negocio)

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| [02-domain-testing.md](./02-domain-testing.md) | Teoría | Entities, UseCases, failures, Fakes |
| [02a-practica-fakes-manuales.md](./02a-practica-fakes-manuales.md) | Práctica ✏️ | Crear FakeAuthRepository paso a paso |

**Objetivos:** Testear lógica pura, crear Fakes manuales

---

### 🅰️ PARTE 2b: MOCKITO (Avanzado - Después de dominar Fakes)

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| [02b-intro-mockito.md](./02b-intro-mockito.md) | Teoría | Configuración, when(), verify(), @GenerateMocks |
| [02b-practica-mockito.md](./02b-practica-mockito.md) | Práctica ✏️ | Ejercicios paso a paso con generación de mocks |

**Objetivos:** Dominar mocks automáticos con Mockito, cuándo migrar desde Fakes

---

### 🅰️ PARTE 3: DATA (Datos e Infraestructura)

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| [03-data-testing.md](./03-data-testing.md) | Teoría | Models, DataSources, Repositories |
| [03a-practica-fixtures-models.md](./03a-practica-fixtures-models.md) | Práctica ✏️ | Fixtures JSON, fromJson/toJson |
| [03b-practica-datasources.md](./03b-practica-datasources.md) | Práctica ✏️ | Remote/Local DataSources |
| [03c-practica-repositories.md](./03c-practica-repositories.md) | Práctica ✏️ | Repository Implementation |

**Objetivos:** Testear Models, HTTP, cache local, lógica online/offline

---

### 🅰️ PARTE 4: PRESENTATION (UI y Estados)

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| [04-presentation-testing.md](./04-presentation-testing.md) | Teoría | Cubits, Widgets, bloc_test |
| [04a-practica-cubits-bloc-test.md](./04a-practica-cubits-bloc-test.md) | Práctica ✏️ | Testear estados de Cubit |
| [04b-practica-widgets.md](./04b-practica-widgets.md) | Práctica ✏️ | Widget tests con interacciones |

**Objetivos:** Testear UI, flujos de usuario, validación de formularios

---

### 🅰️ PARTE 5: CORE (Servicios Compartidos)

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| [05-core-testing.md](./05-core-testing.md) | Teoría | NetworkInfo, Services, Utils |
| [05a-practica-core-services.md](./05a-practica-core-services.md) | Práctica ✏️ | NetworkInfo, Utils, Exceptions |

**Objetivos:** Testear servicios compartidos, conectividad

---

### 🅰️ PARTE 6: AVANZADO

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| [06-advanced-testing.md](./06-advanced-testing.md) | Teoría | Coverage, CI/CD, Integration tests |
| [06a-practica-coverage-ci.md](./06a-practica-coverage-ci.md) | Práctica ✏️ | Medir coverage, GitHub Actions |

**Objetivos:** Automatizar tests, mejorar coverage

---

### 🅰️ PARTE 7: MIGRACIÓN

| Archivo | Tipo | Contenido |
|---------|------|-----------|
| [07-migration-to-mockito.md](./07-migration-to-mockito.md) | Teoría | Cuándo usar Mockito |
| [07a-practica-migration.md](./07a-practica-migration.md) | Práctica ✏️ | Migrar de Fakes a Mocks |

**Objetivos:** Decidir cuándo migrar, sintaxis de Mockito

---

## 📁 Estructura de Archivos

```
testing/
├── README.md                                 ← Estás aquí
│
├── 01-fundamentos.md                        ← Teoría
├── 01a-practica-primeros-tests.md           ← Práctica
│
├── 02-domain-testing.md                     ← Teoría
├── 02a-practica-fakes-manuales.md           ← Práctica
│
├── 02b-intro-mockito.md                     ← Teoría (Avanzado)
├── 02b-practica-mockito.md                  ← Práctica
│
├── 03-data-testing.md                       ← Teoría
├── 03a-practica-fixtures-models.md          ← Práctica
├── 03b-practica-datasources.md              ← Práctica
├── 03c-practica-repositories.md             ← Práctica
│
├── 04-presentation-testing.md               ← Teoría
├── 04a-practica-cubits-bloc-test.md         ← Práctica
├── 04b-practica-widgets.md                  ← Práctica
│
├── 05-core-testing.md                       ← Teoría
├── 05a-practica-core-services.md            ← Práctica
│
├── 06-advanced-testing.md                   ← Teoría
├── 06a-practica-coverage-ci.md              ← Práctica
│
├── 07-migration-to-mockito.md               ← Teoría
└── 07a-practica-migration.md                ← Práctica
```

---

## 🎯 Objetivos de Aprendizaje

Al completar **toda** la guía serás capaz de:

✅ Escribir tests siguiendo el patrón AAA  
✅ Crear Fakes manuales para cualquier interfaz  
✅ Testear Entities, UseCases, y Repository Interfaces  
✅ Testear Models con fixtures JSON  
✅ Testear Remote DataSources (HTTP)  
✅ Testear Local DataSources (SharedPreferences)  
✅ Testear Repository Implementation (lógica online/offline)  
✅ Testear Cubits con bloc_test  
✅ Testear Widgets con interacciones reales  
✅ Medir y mejorar cobertura de código  
✅ Configurar CI/CD con GitHub Actions  
✅ Decidir cuándo usar Fakes vs Mocks  

---

## 🛠️ Requisitos Previos

- [ ] Flutter instalado (3.0+)
- [ ] Conocimientos básicos de Dart
- [ ] Proyecto con Clean Architecture
- [ ] Tu proyecto usa estructura `lib/clean/`

---

## 📦 Dependencias Necesarias

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
  flutter_lints: ^6.0.0
  bloc_test: ^9.1.0          # Para Cubits/Blocs
  mockito: ^5.4.0            # Para tests avanzados
  build_runner: ^2.10.2      # Solo si usas @GenerateMocks
```

### ¿Por qué Fakes en lugar de Mocks?

| Aspecto | Fakes Manuales | Mocks (Mockito) |
|---------|----------------|-----------------|
| **Curva de aprendizaje** | Baja - solo Dart | Alta - anotaciones, generación |
| **Debugging** | Fácil - código visible | Difícil - código generado |
| **Mantenimiento** | Simple - lo kontrolas | Complejo - regenerar |
| **Lectura** | Clara | Confusa |

> **Nuestra recomendación:** Empieza con Fakes manuales. Cuando tengas confianza, podrás migrar a Mockito si lo necesitas (Parte 7).

---

## 🧪 Primera Práctica: Verifica tu Setup

Antes de empezar, verifica que todo funciona:

```bash
# 1. Ve a tu proyecto Flutter
cd tu_proyecto

# 2. Instala dependencias
flutter pub get

# 3. Crea un test simple
touch test/primero_test.dart

# 4. Escribe este código
echo "import 'package:flutter_test/flutter_test'; void main() { test('sanity check', () { expect(1 + 1, 2); }); }" > test/primero_test.dart

# 5. Ejecuta el test
flutter test test/primero_test.dart
```

**Resultado esperado:**
```
✓ All tests passed!
00:00 +1: All tests passed!
```

---

## 💡 Consejos para Aprender

### Antes de cada parte:
- ✅ Lee el archivo de teoría primero
- ✅ No te saltes los ejercicios prácticos
- ✅ Ejecuta los ejemplos del código

### Mientras practicas:
- 📝 Escribe el código tu mismo, no copies y pegues
- 🔄 Si un test falla, lee el error con calma
- 🧠 Pregúntate: "¿Por qué funciona así?"

### Después de cada parte:
- 📊 Revisa tu coverage: `flutter test --coverage`
- 🔁 Replica los ejercicios con tu propio código
- 💬 Explica lo que aprendiste a alguien (o a ti mismo en voz alta)

---

## 🆘 ¿Problemas?

### Tests no ejecutan:
```bash
flutter clean
flutter pub get
flutter pub upgrade
flutter test
```

### Coverage no genera (Linux):
```bash
sudo apt-get install lcov
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html  # macOS
xdg-open coverage/html/index.html  # Linux
```

### Error con build_runner:
```bash
dart run build_runner build --delete-conflicting-outputs
```

---

## 📖 Glosario de Términos

| Término | Definición | Ejemplo |
|---------|------------|---------|
| **AAA** | Patrón: Arrange (preparar) → Act (actuar) → Assert (verificar) | Preparar datos, ejecutar función, verificar resultado |
| **Fake** | Implementación manual de una interfaz | `class FakeAuthRepository implements IAuthRepository` |
| **Mock** | Objeto simulado generado automáticamente | Anotación `@GenerateMocks` |
| **Stub** | Método que retorna un valor predefinido | `when(repo.login()).thenReturn(user)` |
| **Fixture** | Datos de prueba reutilizables (JSON) | `test/fixtures/user.json` |
| **Matcher** | Función para verificar resultados | `expect(result, equals(5))` |
| **Coverage** | Porcentaje de código cubierto por tests | 80% = 80% del código tiene tests |
| **E2E** | End-to-End - Test de flujo completo | Simular usuario real |
| **CI/CD** | Integración y despliegue continuos | GitHub Actions |

---

## 🎉 ¡Empecemos!

**Si eres principiante:**
👉 [Ir a Parte 1: Fundamentos](./01-fundamentos.md)

**Si ya sabes lo básico y necesitas práctica:**
👉 [Ir a 01a-practica-primeros-tests.md](./01a-practica-primeros-tests.md)

---

## 📝 Notas del Autor

Esta guía fue diseñada para el proyecto **Sereni** que usa:
- Clean Architecture en `lib/clean/`
- BLoC/Cubit para gestión de estado
- Fakes manuales (estilo preferido)
- Supabase como backend

Los ejemplos usan el feature de **Auth** como referencia, pero los conceptos aplican a **cualquier feature** de tu aplicación.

---

## 📄 Licencia

MIT License - Libre de usar y modificar.

---

**Última actualización:** 2026-02-25  
**Versión:** 2.0.0  
**Autora:** Guía de Testing para Clean Architecture Flutter
