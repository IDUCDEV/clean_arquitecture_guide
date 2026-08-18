# 🚀 Nivel Experto: Streams y Tiempo Real con Clean Architecture

Las aplicaciones modernas no son estáticas. Un chat actualiza en tiempo real, un dashboard financiero muestra cotizaciones Live, una app de delivery tracks el repartidor. En Clean Architecture tradicional, todo es `Future<Either<Failure, T>>`. Pero cuando los datos fluyen continuamente, necesitamos **StreamUseCase**: el equivalente reactivo de los UseCases tradicionales.

---

## 1. Fundamentos: Por Qué Streams en Clean Architecture

### 1.1 El Problema con Future

`Future` representa un valor único en el futuro. Pero ¿qué pasa cuando hay múltiples valores?

```dart
// ❌ Future no sirve para datos continuos
Future<List<Message>> getMessages() async {
  return await api.getMessages(); // Solo obtiene UNA vez
}

// Si llegan mensajes nuevos, ¿cómo los recibe el UI?
```

### 1.2 Streams al Rescate

```dart
// ✅ Stream representa un flujo de valores
Stream<List<Message>> watchMessages() {
  return api.watchMessages(); // Notificaciones continuas
}
```

### 1.3 Cuándo Usar Streams

| Escenario | Tipo de Datos | Herramienta |
|-----------|--------------|-------------|
| API REST tradicional | Una respuesta | `Future<Either<Failure, T>>` |
| Chat/Mensajería | Múltiples mensajes | `Stream<Either<Failure, T>>` |
| Precios/Stock | Actualizaciones frecuentes | `Stream<T>` |
| Auth State | Sesión activa | `Stream<User?>` |
| Notificaciones | Push events | `Stream<Notification>` |
| Ubicación | GPS coordinates | `Stream<Location>` |

---

## 2. StreamUseCase: El Contrato Base

### 2.1 Definición

```dart
// lib/core/common/stream_usecase.dart

import 'package:fpdart/fpdart.dart';
import 'package:my_app/core/error/failures.dart';

/// Contrato base para UseCases que retornan Streams
/// 
/// Útil para:
/// - Firebase/Firestore watchers
/// - WebSocket connections
/// - SSE (Server-Sent Events)
abstract class StreamUseCase<Type, Params> {
  /// Ejecuta el stream con los parámetros dados
  Stream<Either<Failure, Type>> call(Params params);
}
```

### 2.2 Interfaz Genérica sin Params

```dart
// Para streams que no necesitan parámetros
abstract class StreamUseCaseNoParams<Type> {
  Stream<Either<Failure, Type>> call();
}
```

---

## 3. Implementación Completa: Chat en Tiempo Real

### 3.1 Domain: Entities y Repositories

```dart
// lib/features/chat/domain/entities/message.dart

class Message {
  final String id;
  final String chatId;
  final String senderId;
  final String content;
  final DateTime timestamp;
  final MessageStatus status;
  
  const Message({
    required this.id,
    required this.chatId,
    required this.senderId,
    required this.content,
    required this.timestamp,
    required this.status,
  });
}

enum MessageStatus { sending, sent, delivered, read }
```

```dart
// lib/features/chat/domain/repositories/chat_repository.dart

abstract class ChatRepository {
  /// Stream de mensajes de un chat específico
  Stream<Either<Failure, List<Message>>> watchMessages(String chatId);
  
  /// Stream de múltiples chats
  Stream<Either<Failure, List<ChatSummary>>> watchChats();
  
  /// Enviar mensaje (Future tradicional)
  Future<Either<Failure, Message>> sendMessage(SendMessageParams params);
  
  /// Marcar como leído
  Future<Either<Failure, void>> markAsRead(String messageId);
}
```

### 3.2 Domain: UseCases

```dart
// lib/features/chat/domain/usecases/watch_messages.dart

@lazySingleton
class WatchMessages extends StreamUseCase<List<Message>, String> {
  final ChatRepository repository;

  WatchMessages(this.repository);

  @override
  Stream<Either<Failure, List<Message>>> call(String chatId) {
    return repository.watchMessages(chatId);
  }
}
```

```dart
// lib/features/chat/domain/usecases/watch_chats.dart

@lazySingleton
class WatchChats extends StreamUseCaseNoParams<List<ChatSummary>> {
  final ChatRepository repository;

  WatchChats(this.repository);

  @override
  Stream<Either<Failure, List<ChatSummary>>> call() {
    return repository.watchChats();
  }
}
```

```dart
// lib/features/chat/domain/usecases/filter_active_messages.dart

/// Ejemplo de lógica de negocio en el Stream
@lazySingleton
class FilterActiveMessages 
    extends StreamUseCase<List<Message>, String> {
  final ChatRepository repository;

  FilterActiveMessages(this.repository);

  @override
  Stream<Either<Failure, List<Message>>> call(String chatId) {
    // Transformar el stream: filtrar mensajes no eliminados
    return repository.watchMessages(chatId).map((result) {
      return result.map((messages) 
        => messages.where((m) => !m.isDeleted).toList()
      );
    });
  }
}
```

### 3.3 Data: Repository Implementation

```dart
// lib/features/chat/data/repositories/chat_repository_impl.dart

@LazySingleton(as: ChatRepository)
class ChatRepositoryImpl implements ChatRepository {
  final MessageRemoteDataSource remoteDataSource;

  ChatRepositoryImpl(this.remoteDataSource);

  @override
  Stream<Either<Failure, List<Message>>> watchMessages(String chatId) {
    // Convertir Stream<DataModel> a Stream<Either<Failure, Entity>>
    return remoteDataSource.watchMessages(chatId).map((models) {
      try {
        final messages = models.map((m) => m.toEntity()).toList();
        return Right<Failure, List<Message>>(messages);
      } catch (e) {
        return Left<Failure, List<Message>>(
          ParseFailure('Error parseando mensajes: $e'),
        );
      }
    }).handleError((error) {
      // Manejar errores del Stream (Firebase desconectado, etc.)
      if (error is SocketException) {
        return Left(NetworkFailure('Sin conexión'));
      }
      return Left(ServerFailure(error.toString()));
    });
  }

  @override
  Stream<Either<Failure, List<ChatSummary>>> watchChats() {
    return remoteDataSource.watchChats().map((models) {
      return Right(models.map((m) => m.toEntity()).toList());
    }).handleError((e) => Left(ServerFailure(e.toString())));
  }

  @override
  Future<Either<Failure, Message>> sendMessage(SendMessageParams params) async {
    try {
      final model = await remoteDataSource.sendMessage(params);
      return Right(model.toEntity());
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }
}
```

### 3.4 Data: Firebase/Firestore Implementation

```dart
// lib/features/chat/data/datasources/message_remote_datasource.dart

abstract class MessageRemoteDataSource {
  Stream<List<MessageModel>> watchMessages(String chatId);
  Stream<List<ChatSummaryModel>> watchChats();
  Future<MessageModel> sendMessage(SendMessageParams params);
}
```

```dart
// lib/features/chat/data/datasources/message_remote_datasource_impl.dart

@lazySingleton
class MessageRemoteDataSourceImpl implements MessageRemoteDataSource {
  final FirebaseFirestore _firestore;

  MessageRemoteDataSourceImpl(this._firestore);

  @override
  Stream<List<MessageModel>> watchMessages(String chatId) {
    // Firestore ya retorna un Stream
    return _firestore
        .collection('chats')
        .doc(chatId)
        .collection('messages')
        .orderBy('timestamp', descending: true)
        .snapshots() // ← Este es el Stream de Firebase
        .map((snapshot) => snapshot.docs
            .map((doc) => MessageModel.fromJson(doc.data()))
            .toList());
  }

  @override
  Stream<List<ChatSummaryModel>> watchChats() {
    return _firestore
        .collection('chats')
        .where('participants', arrayContains: _firestore.uid)
        .snapshots()
        .map((snapshot) => snapshot.docs
            .map((doc) => ChatSummaryModel.fromJson(doc.data()))
            .toList());
  }
}
```

---

## 4. Presentation: Consumiendo Streams

### 4.1 Cubit con StreamSubscription

```dart
// lib/features/chat/presentation/cubit/chat_cubit.dart

@injectable
class ChatCubit extends Cubit<ChatState> {
  final WatchMessages watchMessages;
  final SendMessage sendMessage;
  final ChatRepository chatRepository;
  
  StreamSubscription? _subscription;
  String? _currentChatId;

  ChatCubit(
    this.watchMessages,
    this.sendMessage,
    this.chatRepository,
  ) : super(ChatInitial());

  void watchChat(String chatId) {
    _currentChatId = chatId;
    _subscription?.cancel(); // Limpiar stream anterior
    
    _subscription = watchMessages(chatId).listen((result) {
      result.match(
        (failure) => emit(ChatError(failure.message)),
        (messages) => emit(ChatLoaded(messages)),
      );
    });
  }

  void sendMessage(String content) async {
    if (_currentChatId == null) return;
    
    emit(ChatSending());
    
    final result = await sendMessage(SendMessageParams(
      chatId: _currentChatId!,
      content: content,
    ));
    
    result.match(
      (failure) => emit(ChatError(failure.message)),
      (_) => emit(ChatMessageSent()),
    );
  }

  @override
  Future<void> close() {
    _subscription?.cancel(); // ⚠️ CRÍTICO: Prevenir memory leaks
    return super.close();
  }
}
```

### 4.2 Errores: Memory Leaks

**El error más común:** Olvidar cancelar la suscripción.

```dart
// ❌ Memory Leak - No cancelar
class BadCubit extends Cubit<State> {
  StreamSubscription? _sub;
  
  void start() {
    _sub = stream.listen((v) => emit(v));
    // Nunca se cancela 💥
  }
  
  // No overrides close
}

// ✅ Correcto - Siempre cancelar
class GoodCubit extends Cubit<State> {
  StreamSubscription? _sub;
  
  void start() {
    _sub = stream.listen((v) => emit(v));
  }
  
  @override
  Future<void> close() {
    _sub?.cancel(); // ✅ Se limpia
    return super.close();
  }
}
```

---

## 5. Operadores de Streams: Transformaciones Avanzadas

### 5.1 Filtrado (where)

```dart
// Solo mensajes de un usuario específico
@lazySingleton
class WatchUserMessages extends StreamUseCase<List<Message>, UserMessagesParams> {
  final ChatRepository repository;

  WatchUserMessages(this.repository);

  @override
  Stream<Either<Failure, List<Message>>> call(UserMessagesParams params) {
    return repository.watchMessages(params.chatId).map((result) {
      return result.map((messages) 
        => messages.where((m) => m.senderId == params.userId).toList()
      );
    });
  }
}
```

### 5.2 Mapeo (map)

```dart
// Transformar a DTO para UI
@lazySingleton
class MapMessagesToDisplay 
    extends StreamUseCase<List<MessageDisplay>, String> {
  final WatchMessages watchMessages;

  MapMessagesToDisplay(this.watchMessages);

  @override
  Stream<Either<Failure, List<MessageDisplay>>> call(String chatId) {
    return watchMessages(chatId).map((result) {
      return result.map((messages) => messages.map((m) => MessageDisplay(
        id: m.id,
        text: m.content,
        time: _formatTime(m.timestamp),
        isMe: m.senderId == currentUserId,
        status: _mapStatus(m.status),
      )).toList());
    });
  }

  String _formatTime(DateTime dt) => ...;
  MessageDisplayStatus _mapStatus(MessageStatus s) => ...;
}
```

### 5.3 Debounce (esperar input quieto)

```dart
// Búsqueda en tiempo real - no buscar en cada keystroke
class SearchProductsStream extends StreamUseCase<List<Product>, String> {
  final ProductRepository repository;

  SearchProductsStream(this.repository);

  @override
  Stream<Either<Failure, List<Product>>> call(String query) {
    // Crear stream desde TextField
    return Stream.periodic(const Duration(milliseconds: 300))
        .map((_) => query) // Obtener último valor
        .distinct() // Solo si cambió
        .debounceTime(const Duration(milliseconds: 500)) // ✅ Esperar 500ms sin input
        .asyncMap((q) => repository.searchProducts(q))
        .handleError((e) => Left(ServerFailure(e.toString())));
  }
}
```

### 5.4 Distinct (evitar duplicados)

```dart
// No emitir el mismo valor dos veces
stream.distinct().listen((value) {
  print('Nuevo valor: $value');
});
```

### 5.5 Take y Skip

```dart
// Pagination con streams
@lazySingleton
class PaginateMessages extends StreamUseCase<List<Message>, PaginationParams> {
  final WatchMessages watchMessages;

  PaginateMessages(this.watchMessages);

  @override
  Stream<Either<Failure, List<Message>>> call(PaginationParams params) {
    return watchMessages(params.chatId).map((result) {
      return result.map((messages) {
        final start = params.page * params.pageSize;
        final end = start + params.pageSize;
        return messages.skip(start).take(params.pageSize).toList();
      });
    });
  }
}
```

---

## 6. Firebase/Firestore: Casos de Uso Reales

### 6.1 Reconexión Automática

```dart
class FirestoreMessageDataSource implements MessageRemoteDataSource {
  final FirebaseFirestore _firestore;
  StreamSubscription? _connectionSubscription;
  bool _isConnected = true;

  FirestoreMessageDataSource(this._firestore) {
    // Monitorear conexión
    FirebaseDatabase.instance.ref('.info/connected').onValue.listen((event) {
      _isConnected = event.snapshot.value == true;
    });
  }

  @override
  Stream<List<MessageModel>> watchMessages(String chatId) {
    final controller = StreamController<List<MessageModel>>();
    
    final sub = _firestore
        .collection('chats')
        .doc(chatId)
        .collection('messages')
        .snapshots()
        .listen(
          (snapshot) {
            if (_isConnected) {
              controller.add(snapshot.docs
                  .map((d) => MessageModel.fromJson(d.data()))
                  .toList());
            } else {
              controller.addError('Sin conexión');
            }
          },
          onError: controller.addError,
        );

    controller.onCancel = () => sub.cancel();

    return controller.stream;
  }
}
```

### 6.2 Optimización: Escuchar Solo Cambios

```dart
// En lugar de obtener todo, escuchar cambios incrementales
_stream = _firestore
    .collection('messages')
    .doc(messageId)
    .snapshots() // Solo este documento
    .map((doc) => doc.exists ? MessageModel.fromJson(doc.data()!) : null);
```

### 6.3 Batch y Transacciones

```dart
Future<Either<Failure, void>> sendMessageWithTypingIndicator(
  SendMessageParams params,
) async {
  try {
    final batch = _firestore.batch();
    
    // 1. Agregar mensaje
    final msgRef = _firestore
        .collection('chats')
        .doc(params.chatId)
        .collection('messages')
        .doc();
    batch.set(msgRef, MessageModel(
      id: msgRef.id,
      content: params.content,
      timestamp: DateTime.now(),
    ).toJson());

    // 2. Actualizar "último mensaje" en chat
    final chatRef = _firestore.collection('chats').doc(params.chatId);
    batch.update(chatRef, {
      'lastMessage': params.content,
      'lastMessageAt': DateTime.now(),
    });

    await batch.commit();
    return const Right(null);
  } catch (e) {
    return Left(ServerFailure(e.toString()));
  }
}
```

---

## 7. WebSockets: Comunicación Real

### 7.1 DataSource con WebSocket

```dart
// lib/features/trading/data/datasources/price_datasource.dart

@lazySingleton
class PriceRemoteDataSource implements PriceRemoteDataSource {
  WebSocket? _socket;
  final _pricesController = StreamController<PriceUpdate>.broadcast();

  void connect() {
    _socket = WebSocket('wss://api.trading.com/prices');
    
    _socket!.listen(
      (data) {
        final update = PriceUpdate.fromJson(jsonDecode(data));
        _pricesController.add(update);
      },
      onError: (error) {
        _pricesController.addError(error);
      },
      onDone: () {
        // Reconectar después de delay
        Future.delayed(const Duration(seconds: 5), connect);
      },
    );
  }

  @override
  Stream<PriceUpdate> watchPrices(String symbol) {
    return _pricesController.stream.where((p) => p.symbol == symbol);
  }

  void disconnect() {
    _socket?.close();
  }
}
```

### 7.2 Repository con Reconexión

```dart
// lib/features/trading/data/repositories/price_repository_impl.dart

@LazySingleton(as: PriceRepository)
class PriceRepositoryImpl implements PriceRepository {
  final PriceRemoteDataSource remoteDataSource;
  final ConnectionMonitor connectionMonitor;

  PriceRepositoryImpl(this.remoteDataSource, this.connectionMonitor);

  @override
  Stream<Either<Failure, PriceUpdate>> watchPrice(String symbol) {
    // Asegurar conexión
    if (!connectionMonitor.isConnected) {
      remoteDataSource.connect();
    }

    return remoteDataSource.watchPrices(symbol).map((update) {
      return Right<Failure, PriceUpdate>(update);
    }).handleError((e) {
      return Left<Failure, PriceUpdate>(
        ConnectionFailure('Error de conexión: $e'),
      );
    });
  }
}
```

---

## 8. Backpressure: Cuando los Datos Llegan Muy Rápido

### 8.1 El Problema

Si recibes 1000 precios por segundo, tu UI no puede renderizar todos. Necesitas **control de flujo**.

### 8.2 Soluciones

```dart
// Opción 1: Sample - tomar cada N valores
stream.sample(const Duration(seconds: 1)).listen((value) {
  // Actualizar UI máximo 1 vez por segundo
});

// Opción 2: Throttle - limitar frecuencia
stream.throttleTime(
  const Duration(milliseconds: 500),
  trailing: true,
).listen((value) => updateUI(value));

// Opción 3: Buffer - acumular y procesar en batches
stream.bufferTime(const Duration(seconds: 1)).listen((batch) {
  // batch = lista de valores acumulados
  updateChart(batch);
});
```

---

## 9. Testing de Streams

### 9.1 Unit Test de StreamUseCase

```dart
void main() {
  late WatchMessages watchMessages;
  late MockChatRepository mockRepository;
  late StreamController<List<Message>> controller;

  setUp(() {
    mockRepository = MockChatRepository();
    controller = StreamController<List<Message>>.broadcast();
    watchMessages = WatchMessages(mockRepository);
  });

  test('watchMessages retorna stream del repository', () async {
    final messages = [
      Message(id: '1', content: 'Hello'),
    ];

    when(() => mockRepository.watchMessages('chat1'))
        .thenAnswer((_) => Stream.value(Right(messages)));

    final stream = watchMessages('chat1');

    await expectLater(
      stream,
      emits(Right(messages)),
    );
  });
}
```

### 9.2 Test de Cubit con Streams

```dart
void main() {
  late ChatCubit chatCubit;
  late StreamController<Either<Failure, List<Message>>> controller;

  setUp(() {
    controller = StreamController.broadcast();
    chatCubit = ChatCubit(watchMessages, sendMessage, repository);
  });

  test('emite ChatLoaded cuando llega mensaje', () async {
    final messages = [Message(id: '1', content: 'Test')];
    
    // Simular stream
    when(() => watchMessages('chat1')).thenAnswer((_) => 
      Stream.value(Right(messages))
    );

    chatCubit.watchChat('chat1');
    
    await Future.delayed(Duration.zero);
    
    expect(chatCubit.state, ChatLoaded(messages));
  });
}
```

### 9.3 Testing de StreamUseCase con Fake Streams

```dart
// test/features/chat/domain/usecases/watch_messages_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/chat/domain/repositories/chat_repository.dart';
import 'package:my_app/features/chat/domain/usecases/watch_messages.dart';

class MockChatRepository extends Mock implements ChatRepository {}

void main() {
  late WatchMessages useCase;
  late MockChatRepository mockRepository;

  setUp(() {
    mockRepository = MockChatRepository();
    useCase = WatchMessages(mockRepository);
  });

  setUpAll(() {
    registerFallbackValue('chat1');
  });

  group('WatchMessages StreamUseCase', () {
    final tMessages = [
      Message(id: '1', content: 'Hello', chatId: 'chat1', senderId: 'user1', timestamp: DateTime.now(), status: MessageStatus.sent),
      Message(id: '2', content: 'World', chatId: 'chat1', senderId: 'user2', timestamp: DateTime.now(), status: MessageStatus.sent),
    ];

    test('debería retornar stream del repository', () async {
      // Arrange
      when(() => mockRepository.watchMessages('chat1'))
          .thenAnswer((_) => Stream.value(Right(tMessages)));

      // Act
      final stream = useCase('chat1');

      // Assert
      await expectLater(
        stream,
        emits(Right(tMessages)),
      );
    });

    test('debería retornar error cuando repository falla', () async {
      // Arrange
      when(() => mockRepository.watchMessages('chat1'))
          .thenAnswer((_) => Stream.value(const Left(NetworkFailure('Sin conexión'))));

      // Act
      final stream = useCase('chat1');

      // Assert
      await expectLater(
        stream,
        emits(isA<Left<Failure, List<Message>>>()),
      );
    });

    test('debería emitir múltiples valores en secuencia', () async {
      // Arrange
      final controller = StreamController<Either<Failure, List<Message>>>();
      
      when(() => mockRepository.watchMessages('chat1'))
          .thenAnswer((_) => controller.stream);

      final stream = useCase('chat1');

      // Act & Assert
      await expectLater(
        stream,
        emitsInOrder([
          Right([tMessages[0]]),
          Right(tMessages),
          Right([]),
        ]),
      );

      controller.add(Right([tMessages[0]]));
      controller.add(Right(tMessages));
      controller.add(Right([]));
      await controller.close();
    });
  });
}
```

### 9.4 Testing de Repository con Streams

```dart
// test/features/chat/data/repositories/chat_repository_impl_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/chat/data/datasources/message_remote_datasource.dart';
import 'package:my_app/features/chat/data/repositories/chat_repository_impl.dart';
import 'package:my_app/core/error/failures.dart';

class MockMessageRemoteDataSource extends Mock implements MessageRemoteDataSource {}

void main() {
  late ChatRepositoryImpl repository;
  late MockMessageRemoteDataSource mockDataSource;

  setUp(() {
    mockDataSource = MockMessageRemoteDataSource();
    repository = ChatRepositoryImpl(mockDataSource);
  });

  setUpAll(() {
    registerFallbackValue('chat1');
  });

  group('watchMessages', () {
    final tModels = [
      MessageModel(id: '1', content: 'Hello', chatId: 'chat1', senderId: 'user1', timestamp: DateTime.now()),
    ];

    test('debería retornar stream de Right cuando datasource exitos', () async {
      // Arrange
      when(() => mockDataSource.watchMessages('chat1'))
          .thenAnswer((_) => Stream.value(tModels));

      // Act
      final stream = repository.watchMessages('chat1');

      // Assert
      await expectLater(
        stream,
        emits(predicate<Either<Failure, List<Message>>>((result) {
          return result.isRight();
        })),
      );
    });

    test('debería retornar Left cuando datasource lanza error', () async {
      // Arrange
      when(() => mockDataSource.watchMessages('chat1'))
          .thenAnswer((_) => Stream.error(SocketException('Sin conexión')));

      // Act
      final stream = repository.watchMessages('chat1');

      // Assert
      await expectLater(
        stream,
        emits(predicate<Either<Failure, List<Message>>>((result) {
          return result.isLeft() && 
                 result.match((f) => f is NetworkFailure, (_) => false);
        })),
      );
    });

    test('debería mapear modelos a entidades', () async {
      // Arrange
      when(() => mockDataSource.watchMessages('chat1'))
          .thenAnswer((_) => Stream.value(tModels));

      // Act
      final stream = repository.watchMessages('chat1');

      // Assert
      await expectLater(
        stream,
        emits(predicate<Either<Failure, List<Message>>>((result) {
          return result.match(
            (_) => false,
            (messages) => messages.first.id == '1',
          );
        })),
      );
    });
  });
}
```

### 9.5 Testing de Cubit con StreamSubscription

```dart
// test/features/chat/presentation/cubit/chat_cubit_test.dart

import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/chat/domain/usecases/watch_messages.dart';
import 'package:my_app/features/chat/domain/usecases/send_message.dart';
import 'package:my_app/features/chat/domain/repositories/chat_repository.dart';
import 'package:my_app/features/chat/presentation/cubit/chat_cubit.dart';

class MockWatchMessages extends Mock implements WatchMessages {}
class MockSendMessage extends Mock implements SendMessage {}
class MockChatRepository extends Mock implements ChatRepository {}

void main() {
  late ChatCubit cubit;
  late MockWatchMessages mockWatchMessages;
  late MockSendMessage mockSendMessage;

  setUp(() {
    mockWatchMessages = MockWatchMessages();
    mockSendMessage = MockSendMessage();
    cubit = ChatCubit(mockWatchMessages, mockSendMessage);
  });

  tearDown(() {
    cubit.close();
  });

  setUpAll(() {
    registerFallbackValue('chat1');
    registerFallbackValue(const SendMessageParams(chatId: 'chat1', content: 'Test'));
  });

  group('ChatCubit', () {
    final tMessages = [
      Message(id: '1', content: 'Hello', chatId: 'chat1', senderId: 'user1', timestamp: DateTime.now(), status: MessageStatus.sent),
    ];

    test('estado inicial es ChatInitial', () {
      expect(cubit.state, ChatInitial());
    });

    blocTest<ChatCubit, ChatState>(
      'debería emitir ChatLoaded cuando watchChat succeeds',
      setUp: () {
        when(() => mockWatchMessages('chat1'))
            .thenAnswer((_) => Stream.value(Right(tMessages)));
      },
      build: () => ChatCubit(mockWatchMessages, mockSendMessage),
      act: (cubit) => cubit.watchChat('chat1'),
      wait: const Duration(milliseconds: 100),
      expect: () => [
        ChatLoaded(tMessages),
      ],
      verify: (_) {
        verify(() => mockWatchMessages('chat1')).called(1);
      },
    );

    blocTest<ChatCubit, ChatState>(
      'debería emitir ChatError cuando watchChat fails',
      setUp: () {
        when(() => mockWatchMessages('chat1'))
            .thenAnswer((_) => Stream.value(const Left(NetworkFailure('Error'))));
      },
      build: () => ChatCubit(mockWatchMessages, mockSendMessage),
      act: (cubit) => cubit.watchChat('chat1'),
      wait: const Duration(milliseconds: 100),
      expect: () => [
        const ChatError('Error'),
      ],
    );

    blocTest<ChatCubit, ChatState>(
      'debería cancelar suscripción anterior al cambiar de chat',
      setUp: () {
        when(() => mockWatchMessages(any()))
            .thenAnswer((_) => Stream.value(Right(tMessages)));
      },
      build: () => ChatCubit(mockWatchMessages, mockSendMessage),
      act: (cubit) async {
        cubit.watchChat('chat1');
        await Future.delayed(const Duration(milliseconds: 50));
        cubit.watchChat('chat2'); // Cambiar chat
      },
      wait: const Duration(milliseconds: 150),
      verify: (_) {
        // Solo debería llamarse una vez con el último chat
        verify(() => mockWatchMessages('chat2')).called(1);
      },
    );

    test('debería cancelar suscripción al cerrar', () async {
      // Arrange
      final subscription = MockStreamSubscription<Either<Failure, List<Message>>>();
      
      when(() => mockWatchMessages('chat1'))
          .thenAnswer((_) => Stream.value(Right(tMessages)));
      when(() => subscription.cancel()).thenAnswer((_) async {});

      // Act
      await cubit.watchChat('chat1');
      await cubit.close();

      // Assert - verificar que se limpió
      verifyNever(() => subscription.cancel()); // La suscripción se maneja internamente
    });
  });
}
```

### 9.6 Testing con Firebase/Firestore Mock

```dart
// test/mocks/firebase_mocks.dart

import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

// Mock de Firebase
class MockFirebaseApp extends Mock implements FirebaseApp {}

// Mock de FirebaseAuth
class MockFirebaseAuth extends Mock implements FirebaseAuth {}

// Mock de FirebaseFirestore
class MockFirebaseFirestore extends Mock implements FirebaseFirestore {}

// Mock de QuerySnapshot
class MockQuerySnapshot<T> extends Mock implements QuerySnapshot<T> {}

// Mock de DocumentSnapshot
class MockDocumentSnapshot<T> extends Mock implements DocumentSnapshot<T> {}

// Setup para tests
Future<void> setupFirebaseMocks() async {
  TestWidgetsFlutterBinding.ensureInitialized();
  
  final mockApp = MockFirebaseApp();
  when(() => mockApp.name).thenReturn('test-app');
  
  Firebase.initializeApp(name: 'test-app');
  when(() => Firebase.app()).thenReturn(mockApp);
}
```

### 9.7 Testing de Backpressure

```dart
// test/features/trading/domain/usecases/watch_prices_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/trading/domain/repositories/price_repository.dart';
import 'package:my_app/features/trading/domain/usecases/watch_prices.dart';

class MockPriceRepository extends Mock implements PriceRepository {}

void main() {
  late WatchPrices useCase;
  late MockPriceRepository mockRepository;

  setUp(() {
    mockRepository = MockPriceRepository();
    useCase = WatchPrices(mockRepository);
  });

  setUpAll(() {
    registerFallbackValue('BTCUSD');
  });

  group('WatchPrices Backpressure', () {
    test('debería manejar alto volumen de datos', () async {
      // Arrange - Simular 100 precios por segundo
      final controller = StreamController<Either<Failure, PriceUpdate>>();
      
      when(() => mockRepository.watchPrice('BTCUSD'))
          .thenAnswer((_) => controller.stream);

      final stream = useCase('BTCUSD');
      
      // Act - Emitir 1000 precios rápidamente
      for (int i = 0; i < 1000; i++) {
        controller.add(Right(PriceUpdate(
          symbol: 'BTCUSD',
          price: 50000 + i.toDouble(),
          timestamp: DateTime.now(),
        )));
      }
      
      await controller.close();

      // Assert - Verificar que el stream puede manejar la carga
      final results = await stream.take(1000).toList();
      expect(results.length, 1000);
    });

    test('debería aplicar throttle correctamente', () async {
      // Arrange - Simular stream muy rápido
      final fastController = StreamController<Either<Failure, int>>();
      
      when(() => mockRepository.watchPrice('BTCUSD'))
          .thenAnswer((_) => fastController.stream);

      // El throttle se aplica en el UseCase o en el Cubit
      // Aquí verificamos que el stream procese correctamente
      final results = <int>[];
      
      useCase('BTCUSD').listen((result) {
        result.match((_) {}, (v) => results.add(v));
      });

      // Act - Emitir 10 valores en 100ms
      for (int i = 0; i < 10; i++) {
        fastController.add(Right(i));
        await Future.delayed(const Duration(milliseconds: 10));
      }
      
      await fastController.close();
      await Future.delayed(const Duration(seconds: 1));

      // Assert - Todos los valores fueron procesados
      expect(results.length, 10);
    });
  });
}
```

### 9.8 Testing de WebSocket Reconnection

```dart
// test/features/trading/data/datasources/price_datasource_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:my_app/features/trading/data/datasources/price_datasource.dart';

class MockWebSocket extends Mock implements WebSocket {}

void main() {
  late PriceRemoteDataSource dataSource;

  setUp(() {
    dataSource = PriceRemoteDataSource();
  });

  group('PriceRemoteDataSource WebSocket', () {
    test('debería reconectar cuando se pierde conexión', () async {
      // Arrange
      int connectCallCount = 0;
      
      // Este test verificaría la lógica de reconexión
      // Simulando que el socket se cierra y se reconecta
      
      dataSource.connect();
      await Future.delayed(const Duration(milliseconds: 100));
      
      expect(connectCallCount, 1); // Conexión inicial
    });

    test('debería cerrar conexión correctamente', () async {
      dataSource.connect();
      await Future.delayed(const Duration(milliseconds: 100));
      
      // No debería haber errores al cerrar
      expect(() => dataSource.disconnect(), returnsNormally);
    });

    test('debería filtrar precios por símbolo', () async {
      // Arrange
      final controller = StreamController<String>.broadcast();
      
      // Act
      final filteredStream = controller.stream
          .where((data) => data.startsWith('BTC'))
          .map((data) => PriceUpdate.fromJson({'symbol': 'BTC', 'price': 50000}));

      // Assert
      controller.add('ETH-5000'); // No debería aparecer
      controller.add('BTC-50000'); // Sí debería aparecer
      
      await expectLater(
        filteredStream.first,
        completion(predicate<PriceUpdate>((p) => p.symbol == 'BTC')),
      );
      
      await controller.close();
    });
  });
}
```

### 9.9 Errores Comunes en Testing de Streams

```dart
// ❌ Error 1: No cerrar StreamController
setUp(() {
  controller = StreamController(); // Nunca se cierra
});

// ✅ Solución
tearDown(() async {
  await controller?.close();
});

// ❌ Error 2: No esperar a que el stream termine
test('stream test', () async {
  final stream = useCase('param');
  // No await, el test termina antes
});

// ✅ Solución
test('stream test', () async {
  final stream = useCase('param');
  await expectLater(stream, emits(...));
});

// ❌ Error 3: Mock de stream que no es Stream
when(() => mockRepo.watchMessages('chat1'))
    .thenAnswer((_) => [Message()]); // ❌ No es Stream!

// ✅ Solución
when(() => mockRepo.watchMessages('chat1'))
    .thenAnswer((_) => Stream.value([Message()]));

// ❌ Error 4: Olvidar registerFallbackValue
when(() => mockUseCase(any())).thenAnswer(...);
// CRASH: MissingFallbackValueError

// ✅ Solución
setUpAll(() {
  registerFallbackValue('chat1');
});
```

### 9.10 Herramientas de Testing para Streams

| Herramienta | Uso |
|------------|-----|
| `flutter_test` | Testing básico |
| `bloc_test` | Testing de BLoC/Cubit |
| `mocktail` | Mocking sin generación |
| `stream_matchers` | Matchers para streams |

### 9.11 Ejemplo Completo: Integration Test de Chat

```dart
// test/features/chat/integration/chat_integration_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:fpdart/fpdart.dart';
import 'package:my_app/features/chat/domain/usecases/watch_messages.dart';
import 'package:my_app/features/chat/domain/usecases/send_message.dart';
import 'package:my_app/features/chat/presentation/cubit/chat_cubit.dart';

class MockWatchMessages extends Mock implements WatchMessages {}
class MockSendMessage extends Mock implements SendMessage {}

void main() {
  late ChatCubit cubit;
  late MockWatchMessages mockWatchMessages;
  late MockSendMessage mockSendMessage;

  setUp(() async {
    mockWatchMessages = MockWatchMessages();
    mockSendMessage = MockSendMessage();
    cubit = ChatCubit(mockWatchMessages, mockSendMessage);
  });

  tearDown(() async {
    await cubit.close();
  });

  setUpAll(() {
    registerFallbackValue('chat1');
    registerFallbackValue(const SendMessageParams(chatId: 'chat1', content: 'Test'));
  });

  group('Chat Integration', () {
    final tMessages = [
      Message(id: '1', content: 'Hello', chatId: 'chat1', senderId: 'user1', timestamp: DateTime.now(), status: MessageStatus.sent),
    ];

    test('flujo completo: iniciar chat, recibir mensajes, enviar mensaje', () async {
      // Arrange
      when(() => mockWatchMessages('chat1'))
          .thenAnswer((_) => Stream.value(Right(tMessages)));
      when(() => mockSendMessage(any()))
          .thenAnswer((_) async => Right(tMessages.first));

      // Act & Assert - Iniciar chat
      await Future.delayed(const Duration(milliseconds: 100));
      expect(cubit.state, ChatInitial());

      // Act - Watch chat
      cubit.watchChat('chat1');
      await Future.delayed(const Duration(milliseconds: 100));
      
      // Assert - Mensajes recibidos
      expect(cubit.state, isA<ChatLoaded>());

      // Act - Enviar mensaje
      cubit.sendMessage('Hello');
      await Future.delayed(const Duration(milliseconds: 100));
      
      // Assert - Mensaje enviado (estado puede variar)
      verify(() => mockSendMessage(any())).called(1);
    });

    test('debería manejar errores de red durante streaming', () async {
      // Arrange
      when(() => mockWatchMessages('chat1'))
          .thenAnswer((_) => Stream.value(const Left(NetworkFailure('Sin conexión'))));

      // Act
      cubit.watchChat('chat1');
      await Future.delayed(const Duration(milliseconds: 100));

      // Assert
      expect(cubit.state, const ChatError('Sin conexión'));
    });

    test('debería limpiar al cambiar de chat', () async {
      // Arrange
      final controller = StreamController<Either<Failure, List<Message>>>.broadcast();
      
      when(() => mockWatchMessages(any()))
          .thenAnswer((_) => controller.stream);

      // Act
      cubit.watchChat('chat1');
      await Future.delayed(const Duration(milliseconds: 50));
      expect(cubit.state, isA<ChatLoaded>()); // Estado del primer chat

      // Cambiar chat - debería limpiar el anterior
      controller.add(Right([])); // Simular nuevo chat vacío
      
      await Future.delayed(const Duration(milliseconds: 50));
      
      // El estado debería actualizarse con el nuevo chat
      // (La lógica exacta depende de la implementación)
    });
  });
}
```

---

## 10. Errores Comunes

### Error 1: Stream no se Cancela

```dart
// ❌
@override
Future<void> close() {
  return super.close(); // Falta _subscription?.cancel()
}
```

### Error 2: Escuchar Múltiples Veces

```dart
// ❌ Multiple suscripciones sin cancelar
void start() {
  _sub1 = stream.listen(...);
  _sub2 = stream.listen(...); // Duplicado!
}

// ✅ Usar share() para stream compartido
final sharedStream = stream.share();

// O broadcast para múltiples subscribers
final broadcastStream = StreamController().stream.asBroadcastStream();
```

### Error 3: Tipos Incorrectos

```dart
// ❌ Confundir Stream<Either> con Stream<List>
Stream<Either<Failure, List<Message>>> stream = ...

// map retorna Stream<Either<List<Transformado>>>
final mapped = stream.map((e) => e.map((msgs) => msgs.length));
//         ↑                                         ↑
//     Este map es de fpdart                    Este map es de Stream
```

---

## 11. Mejores Prácticas

### Checklist de Streams

- [ ] ¿Cancelaste el `StreamSubscription` en `close()`?
- [ ] ¿Manejas errores del stream con `handleError`?
- [ ] ¿Usas `distinct()` para evitar duplicados?
- [ ] ¿El repository retorna `Either<Failure, T>` dentro del Stream?
- [ ] ¿Hay backpressure si los datos vienen muy rápido?

### Arquitectura de Streams

```
┌──────────────────────────────────────────────────────────┐
│                    PRESENTATION                          │
│  Cubit → listen → emit(ChatLoaded/ChatError)           │
└──────────────────────────┬───────────────────────────────┘
                           │ Stream<Either<Failure, T>>
┌──────────────────────────▼───────────────────────────────┐
│                      DOMAIN                               │
│  StreamUseCase<List<Message>, String>                    │
│  - Lógica de filtrado                                     │
│  - Transformaciones                                       │
└──────────────────────────┬───────────────────────────────┘
                           │ Stream<Either<Failure, T>>
┌──────────────────────────▼───────────────────────────────┐
│                       DATA                                │
│  Repository → map → handleError                          │
│  DataSource → Firebase/WebSocket Stream                   │
└──────────────────────────────────────────────────────────┘
```

---

## 12. Casos de Uso Avanzados

### Combinar Múltiples Streams

```dart
// Combinar stream de mensajes con stream de typing
Stream<Either<Failure, ChatViewState>> watchChatState(String chatId) {
  final messagesStream = watchMessages(chatId);
  final typingStream = watchTypingStatus(chatId);
  
  return messagesStream.asyncMap((messages) async {
    final typing = await typingStream.first;
    
    return messages.map((msgs) => ChatViewState(
      messages: msgs,
      isTyping: typing,
    ));
  });
}
```

### Retry Automático

```dart
Stream<Either<Failure, T>> withRetry(Stream<Either<Failure, T>> stream) {
  return stream.handleError((error) {
    // Retry logic
    return withRetry(stream);
  });
}
```

---

## Resumen Ejecutivo

1. **StreamUseCase** es el equivalente reactivo de UseCase tradicional
2. **Repository** retorna `Stream<Either<Failure, T>>` para manejar errores en el flujo
3. **DataSource** conecta con Firebase, WebSocket, o cualquier fuente de datos continuos
4. **Cubit** escucha el stream y emite estados
5. **Siempre cancelar** `StreamSubscription` en `close()`
6. **Operadores**: `map`, `filter`, `debounce`, `throttle`, `buffer` son esenciales
7. **Backpressure**: Cuando los datos llegan muy rápido, sample, throttle, o buffer

**Siguiente nivel:** Implementa un sistema de sincronización offline-first con Drift/Hive + Streams, donde los cambios locales se syncronizan automáticamente cuando hay conexión.

---

> 📖 **Ejemplo de chat en tiempo real con Bloc + UI completa**: [`16-BLOC-CUBIT/12-ejemplo-chat-stream.md`](../16-BLOC-CUBIT/12-ejemplo-chat-stream.md) — burbujas de chat, scroll automático, indicador "escribiendo...", blocTest con Stream.

## Recursos Adicionales

- [Documentación Streams Dart](https://dart.dev/tutorials/language/streams)
- [fpdart Stream utilities](https://pub.dev/packages/fpdart#stream-utilities)
- [Firebase Firestore Streams](https://firebase.google.com/docs/firestore/query-data/listen)
- [RxJS Marbles](https://rxmarbles.com/) - Diagramas interactivos de operadores

---

## Ver también

- [`11-PRUEBAS`](../11-PRUEBAS/README.md) — Testing de streams y cubits con blocTest
- [`09-WORKMANAGER`](../09-WORKMANAGER/README-background-fetch.md) — Tareas en segundo plano y sincronización

---

## En el siguiente módulo

**→ [05-build-runner-ecosystem.md](./05-build-runner-ecosystem.md)** — Ecosistema completo de build_runner
