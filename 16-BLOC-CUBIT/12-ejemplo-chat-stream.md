# 12. Ejemplo: Chat en Tiempo Real con Bloc + Stream

> **Ver también**: `06-NIVEL-EXPERTO/04-streams-tiempo-real.md` — StreamUseCase, integración Stream + Supabase/Firebase desde la capa de datos.
> Este ejemplo complementa con la UI completa (Bloc + burbujas de chat + scroll automático).

## Funcionalidad

- Escucha mensajes entrantes en tiempo real (Stream)
- Envío de mensajes
- Scroll automático al último mensaje
- Indicador "escribiendo..."
- Estados: loading, loaded, error

## Stream desde Supabase Realtime

```dart
// data/datasources/chat_remote_datasource.dart
class ChatRemoteDataSource {
  final SupabaseClient _client;

  ChatRemoteDataSource(this._client);

  Future<void> enviarMensaje({
    required String salaId,
    required String usuarioId,
    required String texto,
  }) async {
    await _client.from('mensajes').insert({
      'sala_id': salaId,
      'usuario_id': usuarioId,
      'texto': texto,
      'created_at': DateTime.now().toIso8601String(),
    });
  }

  Stream<List<MensajeModel>> obtenerMensajes(String salaId) {
    return _client
        .from('mensajes')
        .stream(primaryKey: ['id'])
        .eq('sala_id', salaId)
        .order('created_at', ascending: true)
        .map((rows) => rows.map((json) => MensajeModel.fromJson(json)).toList());
  }

  Stream<bool> usuarioEscribiendo(String salaId, String usuarioId) {
    return _client
        .channel('escribiendo-$salaId')
        .on(
          RealtimeListenTypes.postgresChanges,
          ChannelFilter(
            event: '*',
            schema: 'public',
            table: 'escribiendo',
            filter: 'sala_id=eq.$salaId',
          ),
          (_) {},
        )
        .subscribe()
        .map((_) => true);
  }
}
```

## Bloc de chat

### Eventos

```dart
sealed class ChatEvent extends Equatable {
  const ChatEvent();
  @override List<Object?> get props => [];
}

final class ConectarSala extends ChatEvent {
  final String salaId;
  const ConectarSala(this.salaId);
  @override List<Object?> get props => [salaId];
}

final class EnviarMensaje extends ChatEvent {
  final String texto;
  const EnviarMensaje(this.texto);
  @override List<Object?> get props => [texto];
}

final class MensajesRecibidos extends ChatEvent {
  final List<Mensaje> mensajes;
  const MensajesRecibidos(this.mensajes);
  @override List<Object?> get props => [mensajes];
}

final class DesconectarSala extends ChatEvent {
  const DesconectarSala();
}
```

### Estados

```dart
sealed class ChatState extends Equatable {
  const ChatState();
  @override List<Object?> get props => [];
}

final class ChatDesconectado extends ChatState {
  const ChatDesconectado();
}

final class ChatConectando extends ChatState {
  const ChatConectando();
}

final class ChatConectado extends ChatState {
  final List<Mensaje> mensajes;
  final bool enviando;

  const ChatConectado({required this.mensajes, this.enviando = false});

  @override
  List<Object?> get props => [mensajes, enviando];
}

final class ChatError extends ChatState {
  final String mensaje;
  const ChatError(this.mensaje);
  @override List<Object?> get props => [mensaje];
}
```

### Bloc con stream subscription

```dart
class ChatBloc extends Bloc<ChatEvent, ChatState> {
  final ChatRepository _repo;
  final String _usuarioId;
  final String _usuarioNombre;
  StreamSubscription? _mensajesSub;
  String _salaId = '';

  ChatBloc({
    required ChatRepository repo,
    required String usuarioId,
    required String usuarioNombre,
  })  : _repo = repo,
        _usuarioId = usuarioId,
        _usuarioNombre = usuarioNombre,
        super(const ChatDesconectado()) {
    on<ConectarSala>(_onConectar);
    on<EnviarMensaje>(_onEnviar);
    on<MensajesRecibidos>(_onMensajes);
    on<DesconectarSala>(_onDesconectar);
  }

  Future<void> _onConectar(
      ConectarSala event, Emitter<ChatState> emit) async {
    _salaId = event.salaId;
    emit(const ChatConectando());

    try {
      // Cargar mensajes existentes
      final mensajes = await _repo.obtenerHistorial(event.salaId);
      emit(ChatConectado(mensajes: mensajes));

      // Suscribirse a nuevos mensajes
      await _mensajesSub?.cancel();
      _mensajesSub = _repo
          .obtenerMensajesStream(event.salaId)
          .listen((mensajes) => add(MensajesRecibidos(mensajes)));
    } catch (e) {
      emit(ChatError('Error al conectar: $e'));
    }
  }

  Future<void> _onEnviar(
      EnviarMensaje event, Emitter<ChatState> emit) async {
    if (state is! ChatConectado) return;
    if (event.texto.trim().isEmpty) return;

    emit(ChatConectado(
      mensajes: (state as ChatConectado).mensajes,
      enviando: true,
    ));

    try {
      await _repo.enviar(
        salaId: _salaId,
        usuarioId: _usuarioId,
        usuarioNombre: _usuarioNombre,
        texto: event.texto.trim(),
      );
      emit(ChatConectado(
        mensajes: (state as ChatConectado).mensajes,
        enviando: false,
      ));
    } catch (e) {
      emit(ChatConectado(
        mensajes: (state as ChatConectado).mensajes,
        enviando: false,
      ));
      emit(ChatError('Error al enviar: $e'));
    }
  }

  void _onMensajes(MensajesRecibidos event, Emitter<ChatState> emit) {
    emit(ChatConectado(mensajes: event.mensajes));
  }

  Future<void> _onDesconectar(
      DesconectarSala event, Emitter<ChatState> emit) async {
    await _mensajesSub?.cancel();
    _mensajesSub = null;
    emit(const ChatDesconectado());
  }

  @override
  Future<void> close() {
    _mensajesSub?.cancel();
    return super.close();
  }
}
```

## Pantalla de chat

```dart
class ChatPage extends StatelessWidget {
  final String salaId;
  final String usuarioId;
  final String usuarioNombre;

  const ChatPage({
    super.key,
    required this.salaId,
    required this.usuarioId,
    required this.usuarioNombre,
  });

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => ChatBloc(
        repo: getIt(),
        usuarioId: usuarioId,
        usuarioNombre: usuarioNombre,
      )..add(ConectarSala(salaId)),
      child: const _ChatView(),
    );
  }
}

class _ChatView extends StatefulWidget {
  const _ChatView();

  @override
  State<_ChatView> createState() => _ChatViewState();
}

class _ChatViewState extends State<_ChatView> {
  final _textCtrl = TextEditingController();
  final _scrollCtrl = ScrollController();

  @override
  void dispose() {
    _textCtrl.dispose();
    _scrollCtrl.dispose();
    context.read<ChatBloc>().add(const DesconectarSala());
    super.dispose();
  }

  void _scrollAlFinal() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollCtrl.hasClients) {
        _scrollCtrl.animateTo(
          _scrollCtrl.position.maxScrollExtent,
          duration: const Duration(milliseconds: 200),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Chat')),
      body: BlocConsumer<ChatBloc, ChatState>(
        listenWhen: (_, current) => current is ChatConectado,
        listener: (_, __) => _scrollAlFinal(),
        builder: (context, state) {
          return switch (state) {
            ChatDesconectado() => const Center(
                child: Text('Desconectado')),
            ChatConectando() => const Center(
                child: CircularProgressIndicator()),
            ChatError(:final mensaje) => Center(
                child: Text('Error: $mensaje')),
            ChatConectado(:final mensajes, :final enviando) =>
              _buildChat(context, mensajes, enviando),
          };
        },
      ),
    );
  }

  Widget _buildChat(
      BuildContext context, List<Mensaje> mensajes, bool enviando) {
    return Column(
      children: [
        Expanded(
          child: ListView.builder(
            controller: _scrollCtrl,
            padding: const EdgeInsets.all(16),
            itemCount: mensajes.length,
            itemBuilder: (context, index) {
              final msg = mensajes[index];
              final esMio = msg.usuarioId == _usuarioId;
              return _Burbuja(
                mensaje: msg,
                esMio: esMio,
              );
            },
          ),
        ),
        SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(8),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _textCtrl,
                    decoration: InputDecoration(
                      hintText: 'Escribe un mensaje...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16, vertical: 12),
                    ),
                    textInputAction: TextInputAction.send,
                    onSubmitted: (v) => _enviar(context),
                  ),
                ),
                const SizedBox(width: 8),
                CircleAvatar(
                  child: IconButton(
                    icon: enviando
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(
                                strokeWidth: 2),
                          )
                        : const Icon(Icons.send),
                    onPressed:
                        enviando ? null : () => _enviar(context),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  void _enviar(BuildContext context) {
    final texto = _textCtrl.text;
    if (texto.trim().isEmpty) return;
    context.read<ChatBloc>().add(EnviarMensaje(texto));
    _textCtrl.clear();
  }
}

class _Burbuja extends StatelessWidget {
  final Mensaje mensaje;
  final bool esMio;

  const _Burbuja({required this.mensaje, required this.esMio});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: esMio ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 8),
        padding: const EdgeInsets.all(12),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        decoration: BoxDecoration(
          color: esMio
              ? Theme.of(context).colorScheme.primaryContainer
              : Colors.grey[200],
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: esMio
                ? const Radius.circular(16)
                : const Radius.circular(4),
            bottomRight: esMio
                ? const Radius.circular(4)
                : const Radius.circular(16),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (!esMio)
              Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Text(
                  mensaje.usuarioNombre,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                ),
              ),
            Text(mensaje.texto),
            const SizedBox(height: 4),
            Text(
              _formatTime(mensaje.createdAt),
              style: const TextStyle(fontSize: 10, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }

  String _formatTime(DateTime dt) {
    return '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
  }
}
```

## Testing con stream

```dart
void main() {
  late ChatBloc bloc;
  late MockChatRepo repo;

  setUp(() {
    repo = MockChatRepo();
    bloc = ChatBloc(
      repo: repo,
      usuarioId: 'u1',
      usuarioNombre: 'Juan',
    );
  });

  tearDown(() {
    bloc.close();
  });

  blocTest<ChatBloc, ChatState>(
    'emite Conectado con mensajes al conectar',
    build: () {
      when(() => repo.obtenerHistorial('s1'))
          .thenAnswer((_) async => [mensaje1]);
      when(() => repo.obtenerMensajesStream('s1'))
          .thenAnswer((_) => const Stream.empty());
      return bloc;
    },
    act: (bloc) => bloc.add(ConectarSala('s1')),
    expect: () => [
      const ChatConectando(),
      ChatConectado(mensajes: [mensaje1]),
    ],
  );
}
```
