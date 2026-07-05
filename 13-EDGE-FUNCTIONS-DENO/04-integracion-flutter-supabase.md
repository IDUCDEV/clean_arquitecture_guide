# 04 - Integración Flutter + Edge Functions

> Cómo invocar Edge Functions desde tu app Flutter, combinándolas con Supabase client, RPCs, y manejo de errores.

---

## 1. Invocar Edge Functions desde Flutter

### 1.1 Configuración Básica

```dart
// core/network/supabase_client.dart
class SupabaseService {
  final SupabaseClient client;

  SupabaseService(this.client);

  Future<dynamic> invokeFunction(String name, {Map<String, dynamic>? body}) async {
    try {
      final response = await client.functions.invoke(
        name,
        body: body,
      );

      return response.data;
    } on FunctionException catch (e) {
      throw EdgeFunctionException(
        message: e.message,
        status: e.status,
      );
    }
  }
}
```

### 1.2 Con Manejo de Errores

```dart
// core/network/edge_function_client.dart
class EdgeFunctionClient {
  final SupabaseClient _supabase;

  EdgeFunctionClient(this._supabase);

  Future<Either<Failure, T>> invoke<T>({
    required String name,
    Map<String, dynamic>? body,
    T Function(dynamic json)? fromJson,
  }) async {
    try {
      final response = await _supabase.functions.invoke(
        name,
        body: body,
      );

      if (response.data == null) {
        return Left(ServerFailure('Empty response from edge function'));
      }

      if (fromJson != null) {
        return Right(fromJson(response.data));
      }

      return Right(response.data as T);
    } on FunctionException catch (e) {
      return Left(EdgeFunctionFailure(
        message: e.message,
        status: e.status,
      ));
    } catch (e) {
      return Left(NetworkFailure(e.toString()));
    }
  }
}
```

---

## 2. Repositorio con Edge Functions

```dart
// features/raffles/data/repositories/raffle_repository_impl.dart
@lazySingleton(as: RaffleRepository)
class RaffleRepositoryImpl implements RaffleRepository {
  final EdgeFunctionClient _edgeFunctions;
  final SupabaseClient _supabase;

  RaffleRepositoryImpl(this._edgeFunctions, this._supabase);

  @override
  Future<Either<Failure, PurchaseResult>> purchaseTicket({
    required String ticketId,
    required String paymentMethod,
  }) async {
    // Llamar a edge function que internamente usa RPC transaccional
    final result = await _edgeFunctions.invoke<PurchaseResult>(
      name: 'purchase-ticket',
      body: {
        'ticketId': ticketId,
        'paymentMethod': paymentMethod,
      },
      fromJson: (json) => PurchaseResult.fromJson(json as Map<String, dynamic>),
    );

    return result;
  }

  @override
  Future<Either<Failure, List<Raffle>>> getActiveRaffles() async {
    try {
      final response = await _supabase
          .from('raffles')
          .select('*')
          .eq('status', 'active')
          .order('created_at', ascending: false);

      final raffles = (response as List)
          .map((json) => Raffle.fromJson(json as Map<String, dynamic>))
          .toList();

      return Right(raffles);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
```

---

## 3. Cubit con Edge Functions

```dart
// features/raffles/presentation/cubit/purchase_cubit.dart
@injectable
class PurchaseCubit extends Cubit<PurchaseState> {
  final RaffleRepository _repository;

  PurchaseCubit(this._repository) : super(const PurchaseInitial());

  Future<void> purchaseTicket({
    required String ticketId,
    required String paymentMethod,
  }) async {
    emit(const PurchaseLoading());

    final result = await _repository.purchaseTicket(
      ticketId: ticketId,
      paymentMethod: paymentMethod,
    );

    result.fold(
      (failure) => emit(PurchaseError(failure.message)),
      (purchase) => emit(PurchaseSuccess(purchase)),
    );
  }
}
```

---

## 4. Flujo Completo: Frontend → Edge Function → RPC

```
Flutter App                    Edge Function                 PostgreSQL
    │                               │                           │
    │   POST /purchase-ticket       │                           │
    │──────────────────────────────>│                           │
    │                               │                           │
    │                               │  supabase.rpc(           │
    │                               │    'purchase_ticket')    │
    │                               │──────────────────────────>│
    │                               │                           │
    │                               │    {success: true,        │
    │                               │     ticket_number: 42}   │
    │                               │<──────────────────────────│
    │                               │                           │
    │   {success: true,             │                           │
    │    ticket_number: 42}        │                           │
    │<──────────────────────────────│                           │
```

### Código Flutter Completo

```dart
// En el widget (pantalla de compra)
class PurchaseScreen extends StatelessWidget {
  const PurchaseScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => getIt<PurchaseCubit>(),
      child: BlocConsumer<PurchaseCubit, PurchaseState>(
        listener: (context, state) {
          state.whenOrNull(
            success: (purchase) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('Boleto #${purchase.ticketNumber} comprado'),
                  backgroundColor: Colors.green,
                ),
              );
            },
            error: (message) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(message),
                  backgroundColor: Colors.red,
                ),
              );
            },
          );
        },
        builder: (context, state) {
          return state.when(
            initial: () => _buildPurchaseForm(context),
            loading: () => const Center(child: CircularProgressIndicator()),
            success: (_) => const Center(child: Icon(Icons.check_circle, size: 64)),
            error: (message) => Center(child: Text(message)),
          );
        },
      ),
    );
  }
}
```

---

## 5. Edge Function con JWT desde Flutter

```dart
// El token se envía automáticamente si usas supabase.functions.invoke
// SupabaseClient se encarga de adjuntar el JWT del usuario autenticado

class EdgeFunctionClient {
  final SupabaseClient _supabase;

  Future<dynamic> invoke(String name, {Map<String, dynamic>? body}) async {
    // El token JWT se adjunta AUTOMÁTICAMENTE
    final response = await _supabase.functions.invoke(name, body: body);

    // Si el usuario no está autenticado, Supabase no envía token
    // y la Edge Function devuelve 401
    return response.data;
  }
}
```

---

## 6. Testing de Edge Functions desde Flutter

### 6.1 Mock de Edge Functions

```dart
// test/mocks/mock_edge_functions.dart
class MockEdgeFunctionsClient extends Mock
    implements SupabaseEdgeFunctionsClient {}

void main() {
  late MockEdgeFunctionsClient mockClient;
  late EdgeFunctionClient edgeFunctionClient;

  setUp(() {
    mockClient = MockEdgeFunctionsClient();
    edgeFunctionClient = EdgeFunctionClient(mockClient);
  });

  test('invoke returns success', () async {
    when(() => mockClient.invoke(
      'purchase-ticket',
      body: any(named: 'body'),
    )).thenAnswer((_) async => FunctionResponse(
      data: {'success': true, 'ticketNumber': 42},
      status: 200,
    ));

    final result = await edgeFunctionClient.invoke(
      name: 'purchase-ticket',
      body: {'ticketId': '123', 'paymentMethod': 'cash'},
    );

    expect(result, isA<Right<Failure, dynamic>>());
    expect(result.getOrElse(() => null)['ticketNumber'], 42);
  });

  test('invoke handles FunctionException', () async {
    when(() => mockClient.invoke(
      'purchase-ticket',
      body: any(named: 'body'),
    )).thenThrow(FunctionException(
      message: 'Insufficient tickets',
      status: 400,
    ));

    final result = await edgeFunctionClient.invoke(
      name: 'purchase-ticket',
      body: {'ticketId': '999', 'paymentMethod': 'cash'},
    );

    expect(result, isA<Left<Failure, dynamic>>());
    result.fold(
      (failure) => expect(failure, isA<EdgeFunctionFailure>()),
      (_) => fail('Expected failure'),
    );
  });
}
```

### 6.2 Test de Integración

```dart
void main() {
  late RaffleRepository repository;

  setUpAll(() async {
    // Inicializar Supabase local
    await initTestSupabase();
    repository = RaffleRepositoryImpl(
      EdgeFunctionClient(testSupabaseClient),
      testSupabaseClient,
    );
  });

  test('purchase flow completes successfully', () async {
    final result = await repository.purchaseTicket(
      ticketId: testTicketId,
      paymentMethod: 'cash',
    );

    result.fold(
      (failure) => fail('Expected success, got: $failure'),
      (purchase) {
        expect(purchase.ticketNumber, isNotNull);
        expect(purchase.success, true);
      },
    );
  });
}
```

---

## 7. Buenas Prácticas

### 7.1 Separación de Responsabilidades

```
Flutter App
├── EdgeFunctionClient      → Invoca funciones (bajo nivel)
├── FeatureRepository       → Orquesta llamadas + mapeo a dominio
└── Cubit/Bloc             → Maneja estado de UI
```

### 7.2 Cache + Edge Functions

```dart
Future<Either<Failure, List<Raffle>>> getRaffles() async {
  // 1. Intentar cache local
  final cached = await localDataSource.getCachedRaffles();
  if (cached != null) return Right(cached);

  // 2. Llamar edge function
  final result = await edgeFunctions.invoke('get-raffles');

  return result.fold(
    (failure) => Left(failure),
    (data) {
      final raffles = (data as List).map((j) => Raffle.fromJson(j)).toList();
      // 3. Cachear resultado
      localDataSource.cacheRaffles(raffles);
      return Right(raffles);
    },
  );
}
```

### 7.3 Manejo de Offline

```dart
Future<Either<Failure, void>> purchaseTicket({
  required String ticketId,
  required String paymentMethod,
}) async {
  final hasConnection = await networkInfo.isConnected;

  if (!hasConnection) {
    // Guardar en cola local para sincronizar después
    await localDataSource.queuePurchase(ticketId, paymentMethod);
    return Right(null); // Confirmación local
  }

  // Online: invocar edge function
  return edgeFunctionClient.invoke(
    name: 'purchase-ticket',
    body: {'ticketId': ticketId, 'paymentMethod': paymentMethod},
  );
}
```

---

## 8. Resumen

1. **`supabase.functions.invoke`** desde Flutter invoca Edge Functions
2. **JWT** se adjunta automáticamente si el usuario está autenticado
3. **Service Role** para operaciones admin (solo desde Edge Functions internas)
4. **EdgeFunctionClient** wrapper para manejo de errores con Either
5. **RPCs + Edge Functions** = lógica transaccional en SQL expuesta via serverless
6. **Testing** con mocks de Supabase y tests de integración local

---

## Recursos

- [Supabase Flutter Client - Functions](https://supabase.com/docs/reference/dart/functions-invoke)
- [Supabase Flutter SDK](https://pub.dev/packages/supabase_flutter)
- [Edge Functions Examples](https://github.com/supabase/supabase/tree/master/examples/edge-functions)

---

## 📚 Referencias

- [Supabase | Edge Functions](https://supabase.com/docs/guides/functions) — Documentación oficial de Edge Functions
- [Deno | Manual](https://deno.land/manual) — Documentación oficial de Deno
- [Supabase | Cron jobs](https://supabase.com/docs/guides/functions/cron) — Programación de tareas cron

---
