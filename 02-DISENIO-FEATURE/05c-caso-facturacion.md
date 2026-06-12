# Caso Práctico: Sistema de Facturación

> Aplica FADER + Mapeo + Contratos + Flujo para diseñar un sistema de facturación con máquina de estados compleja.

---

## Enunciado

Somos el equipo de ingeniería de una empresa SaaS. El equipo de producto nos pide:

> Los clientes deben poder generar facturas (borrador), enviarlas a sus clientes, registrar pagos, y hacer seguimiento de facturas vencidas. El sistema debe soportar múltiples monedas, impuestos configurables por país, descuentos, facturas recurrentes, y notas de crédito. Los administradores deben poder emitir facturas desde el panel de control y generar reportes de ingresos.

---

## Instrucciones

1. Trabaja en papel y lápiz. No abras el editor de código.
2. Sigue cada sección en orden.
3. Al final, compara con la solución sugerida.

---

## Sección 1: FADER

### ✏️ Paso 1: Formular

Escribe al menos 3 enunciados "Como [actor], quiero [acción] para [valor]".

**Pregúntate:**
- ¿Quién crea la factura? ¿El emisor (vendedor) o el receptor (cliente)?
- ¿Se envía la factura al cliente o el cliente la descarga?
- ¿Una factura recurrente se genera automáticamente o manualmente?
- ¿Qué diferencia hay entre una nota de crédito y una factura de anulación?

### ✏️ Paso 2: Actorizar

Identifica todos los actores y sus permisos:

| Actor | Tipo | ¿Qué puede hacer? |
|-------|------|-------------------|
| Emisor (vendedor) | Primario | |
| Cliente (receptor) | Secundario | |
| Admin | Secundario | |
| Pasarela de Pagos | Externo | |
| Sistema de Impuestos | Externo | |
| ? | ? | |

**Pregúntate:**
- ¿El cliente puede ver el estado de pago de sus facturas?
- ¿El admin puede emitir facturas en nombre del emisor?
- ¿El sistema de impuestos es externo (API de AFIP/SII) o interno?

### ✏️ Paso 3: Descomponer

Enumera todas las operaciones atómicas.

**Considera operaciones como:**
- Crear factura (borrador)
- Emitir factura (validar y generar número fiscal si aplica)
- Enviar factura al cliente
- Registrar pago (total o parcial)
- Generar nota de crédito
- Programar factura recurrente
- Reporte de ingresos mensuales

**Máquina de estados de una factura:**

```
Borrador ──→ Emitida ──→ Enviada ──→ Pagada
                 │                      │
                 │                      ├── Parcial
                 │                      └── Total
                 │
                 ├──→ Vencida
                 │
                 └──→ Anulada (nota de crédito)
```

**Identifica dependencias:**
- ¿Qué se necesita para emitir una factura? (items, impuestos, cliente válido)
- ¿Qué pasa si se paga una factura ya vencida?
- ¿Se puede anular una factura pagada?

### ✏️ Paso 4: Entidades

Define las entidades de negocio:

**Posibles entidades:**
- `Factura` (Invoice)
- `ItemFactura` (InvoiceLine)
- `Cliente` (Customer)
- `Emisor` (Issuer)
- `Pago` (Payment)
- `NotaCredito` (CreditNote)
- `Impuesto` (Tax)
- `PlanRecurrente` (RecurringPlan)

**Pregúntate:**
- `ItemFactura` es una entidad o un value object?
- `Pago` puede ser parcial o total — ¿cómo se relaciona con `Factura`?
- ¿`Cliente` es el destinatario de la factura o el que paga?
- ¿`Impuesto` es un porcentaje fijo o varía por producto?

### ✏️ Paso 5: Reglas

Enuncia al menos 10 reglas de negocio.

**Áreas a cubrir:**
- Números de factura (secuenciales por emisor)
- Fechas (emisión no puede ser futura, vencimiento vs emisión)
- Impuestos (IVA 21%, RG 10%, exento)
- Pagos (parciales, totales, sobrantes)
- Notas de crédito (solo referencian una factura existente)
- Recurrentes (periodicidad, tope de emisiones)
- Anulación (no anular facturas con más de X días)

---

## Sección 2: Mapeo a Capas

### ✏️ Paso 1: Estructura DOMAIN

Dibuja el árbol de `domain/`:

```
domain/
├── entities/
│   ├── invoice.dart
│   ├── invoice_line.dart
│   ├── customer.dart
│   ├── payment.dart
│   ├── credit_note.dart
│   ├── tax.dart
│   └── recurring_plan.dart
├── usecases/
│   ├── create_invoice.dart
│   ├── issue_invoice.dart
│   ├── send_invoice.dart
│   ├── register_payment.dart
│   ├── cancel_invoice.dart
│   ├── generate_credit_note.dart
│   ├── create_recurring_plan.dart
│   ├── generate_recurring_invoices.dart
│   └── get_revenue_report.dart
├── repositories/
│   ├── invoice_repository.dart
│   ├── customer_repository.dart
│   └── payment_repository.dart
├── services/
│   └── tax_calculator.dart (interface)
└── core/
    └── failures.dart
```

**Pregúntate:**
- ¿`tax_calculator` es un servicio o parte de Invoice?
- ¿`issue_invoice` y `create_invoice` son UseCases separados o fases del mismo?
- ¿`generate_credit_note` crea una nueva factura o modifica la existente?

### ✏️ Paso 2: Estructura DATA

Dibuja el árbol de `data/`.

**Considera:**
- Fuente remota (API REST)
- Fuente local (caché para consulta offline)
- Modelos con fromJson/toJson
- Implementaciones de repositorios

**Pregúntate:**
- ¿El catálogo de impuestos se cachea o siempre se consulta al servidor?
- ¿Las facturas emitidas se almacenan localmente?
- ¿El reporte de ingresos se genera en backend o frontend?

### ✏️ Paso 3: Estructura PRESENTATION

Dibuja el árbol de `presentation/`.

**Considera:**
- Formulario de creación de factura (multipaso: seleccionar cliente → agregar items → impuestos → resumen)
- Lista de facturas con filtros (estado, fecha, cliente)
- Detalle de factura con timeline de estados
- Dashboard de ingresos

---

## Sección 3: Contratos

### ✏️ Paso 1: Contrato InvoiceRepository

```dart
abstract class InvoiceRepository {
  // CRUD de facturas
  // Transiciones de estado (emitir, enviar, anular)
  // Búsqueda con filtros (estado, fecha, cliente)
  // ¿Qué failures produce cada operación?
}
```

### ✏️ Paso 2: Contrato PaymentRepository

```dart
abstract class PaymentRepository {
  // Registrar pago
  // Obtener pagos de una factura
  // Conciliar pagos
  // Reembolsar
}
```

### ✏️ Paso 3: Contrato TaxCalculator

```dart
abstract class TaxCalculator {
  // Calcular impuestos para un conjunto de items
  // Depende del país del cliente y tipo de producto
  double calculateTax(ProductType type, double amount, String countryCode);
}
```

### ✏️ Paso 4: Estados de UI

Diseña los estados para `CreateInvoiceCubit` (formulario multipaso).

**Pregúntate:**
- ¿Cómo modelas un formulario que tiene pasos? (seleccionar cliente → items → impuestos → revisar)
- ¿Cada paso tiene su propio estado o todo en un solo estado?
- ¿Cómo manejas validación por paso?

### ✏️ Paso 5: ADR

Escribe al menos un ADR. Ejemplos:
- ¿La generación de facturas recurrentes se hace con cron job o con Cloud Scheduler?
- ¿El número de factura se genera en frontend o backend?
- ¿Los pagos parciales se aplican al total o a items específicos?
- ¿El cálculo de impuestos es interno o llama a una API externa?

---

## Sección 4: Flujo de Datos

### ✏️ Paso 1: Flujo Emitir Factura

Dibuja la secuencia desde que el usuario llena el formulario hasta que la factura tiene número fiscal.

**Incluye:**
- Validaciones en cada paso del formulario
- Transición de estado: Borrador → Emitida
- Asignación de número de factura secuencial
- Cálculo de impuestos
- Manejo de errores (cliente inválido, items sin stock, etc.)

### ✏️ Paso 2: Flujo Registrar Pago

Dibuja el flujo de registro de pago, incluyendo pagos parciales.

**Pregúntate:**
- ¿Cómo afecta un pago parcial al saldo pendiente?
- ¿Qué pasa si el pago supera el total? (sobrante)
- ¿La factura cambia a "pagada" solo cuando saldo = 0?

### ✏️ Paso 3: Flujo Generar Facturas Recurrentes

Dibuja el flujo automático de generación de facturas recurrentes.

**Pregúntate:**
- ¿Quién dispara el proceso? (cron, Cloud Function, webhook)
- ¿Qué facturas se generan hoy según los planes activos?
- ¿Qué pasa si falla la generación de una factura?
- ¿Cómo se notifica al cliente?

---

## Solución Sugerida

> ⚠️ Resuelve cada sección en papel primero. La solución sugerida es para comparar después.

### ✅ FADER Completo

```
╔═══════════════════════════════════════════════════════════════╗
║  FEATURE: Sistema de Facturación                             ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [F]ormular:                                                  ║
║  F1: Como emisor, quiero crear y emitir facturas para        ║
║      cobrar a mis clientes.                                   ║
║  F2: Como emisor, quiero registrar pagos para hacer          ║
║      seguimiento de cuentas corrientes.                       ║
║  F3: Como administrador, quiero generar reportes de          ║
║      ingresos para analizar la salud financiera.             ║
║                                                               ║
║  [A]ctorizar:                                                 ║
║  1. Emisor (primario) — crea, emite, envía, anula facturas  ║
║  2. Cliente (secundario) — recibe facturas, ve estado       ║
║  3. Admin (secundario) — reportes, gestionar plantillas     ║
║  4. API de Impuestos (externa) — validar cálculos fiscales  ║
║  5. Pasarela de Pago (externa) — procesar cobros            ║
║  6. Cron/Cloud Scheduler (sistema) — generar recurrentes     ║
║                                                               ║
║  [D]escomponer:                                               ║
║  Emisor:                                                      ║
║  - [C] Crear factura borrador                                 ║
║  - [U] Editar factura (solo en borrador)                     ║
║  - [Transición] Emitir factura (borrador → emitida)          ║
║  - [Transición] Enviar factura (emitida → enviada)           ║
║  - [Transición] Anular factura (→ anulada + nota crédito)   ║
║  - [C] Registrar pago                                         ║
║  - [C] Programar factura recurrente                          ║
║  - [R] Ver reporte de ingresos                                ║
║                                                               ║
║  Admin:                                                       ║
║  - [R] Ver dashboard financiero                              ║
║  - [CRUD] Gestionar plantillas de factura                    ║
║                                                               ║
║  Sistema:                                                     ║
║  - [Transición] Generar facturas recurrentes (cron)          ║
║  - [Validación] Validar factura antes de emitir              ║
║  - [Validación] Marcar vencidas automáticamente              ║
║  - [Cálculo] Calcular impuestos según país y tipo producto   ║
║                                                               ║
║  [E]ntidades:                                                 ║
║  Factura: id, numeroFactura, emisorId, clienteId,            ║
║           fechaEmision, fechaVencimiento,                     ║
║           estado (borrador, emitida, enviada, pagada,        ║
║                  vencida, anulada),                           ║
║           moneda, subtotal, descuento, impuesto, total,       ║
║           notas, plantillaId                                  ║
║  ItemFactura: id, facturaId, descripcion, cantidad,          ║
║               precioUnitario, porcentajeImpuesto, total       ║
║  Cliente: id, nombre, email, direccion, pais,                ║
║           rut/cuit, condicionFiscal                           ║
║  Emisor: id, nombre, rut, direccion, pais,                   ║
║          proximoNumeroFactura                                 ║
║  Pago: id, facturaId, monto, fecha, metodo,                  ║
║        referenciaExterna, estado                              ║
║  NotaCredito: id, facturaOriginalId, motivo, monto,          ║
║               fecha                                           ║
║  PlanRecurrente: id, emisorId, clienteId, periodicidad,     ║
║                  siguienteEmision, items, monto               ║
║  Impuesto: id, pais, tipoProducto, porcentaje,               ║
║            codigoFiscal                                       ║
║                                                               ║
║  [R]eglas:                                                    ║
║  R001: El número de factura es secuencial por emisor         ║
║  R002: No se puede emitir una factura sin items              ║
║  R003: fechaVencimiento > fechaEmision                       ║
║  R004: Solo facturas en borrador se pueden editar            ║
║  R005: Solo facturas emitidas se pueden enviar                ║
║  R006: Solo facturas emitidas/enviadas se pueden pagar        ║
║  R007: Una factura se marca vencida si fechaVencimiento <    ║
║        hoy y estado es emitida o enviada                      ║
║  R008: Pagos parciales: estado = "pagada" solo si            ║
║        suma pagos >= total                                    ║
║  R009: Si suma pagos > total, generar nota de crédito        ║
║        por el excedente                                       ║
║  R010: Nota de crédito solo referencia una factura emitida   ║
║  R011: Al anular, el monto queda como crédito a favor        ║
║        del cliente                                            ║
║  R012: Las recurrentes se generan el día siguiente al         ║
║        de su fecha de siguienteEmision                        ║
║  R013: Impuesto IVA 21% para productos nacionales,           ║
║        0% para exportaciones                                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### ✅ Máquina de Estados de Factura

```
                    ┌──────────┐
                    │ BORRADOR │
                    └────┬─────┘
                         │ emitir (R002, R003)
                         ▼
                    ┌──────────┐
         ┌──────────│ EMITIDA  │──────────┐
         │          └────┬─────┘          │
         │               │ enviar         │
         │               ▼                │
         │          ┌──────────┐  (R006)  │
         │          │ ENVIADA  │          │
         │          └────┬─────┘          │
         │               │                │
         │      pagar    │  (R006)        │
         │               ▼                │
         │     ╔══════════════╗           │
         │     ║   PAGADA    ║           │
         │     ╚══════════════╝           │
         │         │     ↑                │
         │         │     │ (si sobra →    │
         │         │     │  R009)         │
         │         │     │                │
         │         ▼     │                │
         │  ┌───────────────┐             │
         │  │ CRÉDITO A      │            │
         │  │ FAVOR (R011)   │            │
         │  └───────────────┘             │
         │                                │
         │  vencimiento (R007)            │
         │                                ▼
         │                         ┌──────────┐
         └─────────────────────────│ VENCIDA  │
                                   └──────────┘
         anular (R004,R010) →
         ┌──────────┐
         │ ANULADA  │
         └──────────┘
```

### ✅ Contrato InvoiceRepository

```dart
abstract class InvoiceRepository {
  // CRUD
  Future<Either<Failure, Invoice>> createDraft(CreateInvoiceParams params);
  Future<Either<Failure, Invoice>> updateDraft(
    String invoiceId, UpdateInvoiceParams params);
  Future<Either<Failure, Invoice>> getInvoice(String invoiceId);
  Future<Either<Failure, List<Invoice>>> getInvoices({
    required String issuerId,
    InvoiceStatus? status,
    DateTime? fromDate,
    DateTime? toDate,
    String? customerId,
    int page = 1,
  });

  // Transiciones de estado
  Future<Either<Failure, Invoice>> issue(String invoiceId);
  Future<Either<Failure, Invoice>> send(String invoiceId);
  Future<Either<Failure, Invoice>> cancel(String invoiceId, String reason);

  // Notas de crédito
  Future<Either<Failure, CreditNote>> generateCreditNote({
    required String invoiceId,
    required double amount,
    required String reason,
  });

  // Recurrentes
  Future<Either<Failure, RecurringPlan>> createRecurringPlan(
    CreateRecurringPlanParams params);
  Future<Either<Failure, List<Invoice>>> generateRecurringInvoices();
}
```

### ✅ ADR Sugerido

```markdown
# ADR-005: Generación del Número de Factura

## Contexto
Cada factura emitida necesita un número único y secuencial por emisor.
El formato requerido es FFF-000001 (prefijo + número de 6 dígitos).

## Decisión
El número de factura se genera EXCLUSIVAMENTE en el backend (Supabase),
usando una transacción atómica que incrementa un contador en la tabla
`emisores.proximoNumeroFactura`. Nunca se genera en el frontend.

## Consecuencias
Positivas:
- Garantiza secuencialidad sin huecos ni duplicados
- El frontend no puede manipular la numeración
- Fácil de auditar

Negativas:
- La factura debe estar en borrador y enviarse al backend para obtener número
- Si falla la conexión al emitir, la factura queda sin número

## Alternativas consideradas
1. UUID como número de factura:
   Descartado: requisito legal exige numeración secuencial.
2. Generar en frontend con optimistic lock:
   Descartado: riesgo de colisión y manipulación.
3. Generar al crear borrador vs al emitir:
   Elegimos al emitir para evitar huecos por borradores descartados.
```

### ✅ Flujo Emitir Factura (resumido)

```
USUARIO    → Completa formulario (cliente, items, impuestos)
CUBIT      → Validaciones por paso
              Paso 1: cliente válido
              Paso 2: items con precio > 0
              Paso 3: impuestos calculados
              Paso 4: revisar y confirmar

USUARIO    → Tap "Emitir Factura"
CUBIT      → emit(InvoiceSubmitting)
USECASE    → IssueInvoice.call(invoiceId)
              → Valida R002 (items no vacío)
              → Valida R003 (fechas válidas)
              → InvoiceRepository.issue(invoiceId)
REPO IMPL  → 1. remoteDS.getNextInvoiceNumber(issuerId)
             2. remoteDS.updateInvoiceStatus(id, "emitida", number)
             3. Atómico: incrementar contador
             4. remoteDS.fetchInvoice(id)
             5. model.toEntity()
USECASE    → Right(invoice)
CUBIT      → emit(InvoiceIssued(invoice))
WIDGET     → Muestra factura emitida con número asignado

ERRORES:
  - items vacío → InvoiceHasNoItems
  - fecha inválida → InvalidInvoiceDate
  - cliente sin datos fiscales → MissingTaxInfo
```

---

## 🚀 Siguiente paso

Continúa con la [App de Delivery](./05d-caso-delivery.md) para practicar con flujos en tiempo real y geolocalización.

---

**Tiempo estimado:** 2-3 horas  
**Material:** Papel y lápiz
