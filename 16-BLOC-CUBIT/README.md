# Módulo 16: BLoC / Cubit — State Management

Guía completa de BLoC y Cubit para Flutter, desde fundamentos hasta patrones avanzados.

## Progresión sugerida

```
 1. Conceptos (Bloc vs Cubit, streams)
 2. vs Otros state management
 3. Cubit básico + contador + login
 4. Bloc con eventos
 5. Widgets flutter_bloc p1 (Provider, Builder, read/watch)
 6. Widgets flutter_bloc p2 (Listener, Consumer, Selector)
 7. Ejemplo login (validación, tests)
 8. Ejemplo lista con filtros búsqueda
 9. Ejemplo favoritos persistidos (HydratedCubit)
10. Ejemplo multi-bloc (dashboard)
11. Ejemplo formulario multipaso
12. Ejemplo chat en tiempo real (streams)
13. Concurrencia de eventos
14. Testing de BLoC/Cubit
15. HydratedBloc avanzado
16. Buenas prácticas
 17. Proyecto integrador (e-commerce)
 18. Patrón lista avanzada (previousState, PullToRefreshWrapper, slivers)
 19. Cubit vs BLoC: ¿Cuándo usar cuál?
 20. Debugging de BLoC/Cubit
```

## Dependencias (prerrequisitos de otros módulos)

| Capítulo | Prerrequisito | Módulo |
|---|---|---|
| 3 (Cubit) | sealed class + Equatable + copyWith | 09-ESTRUCTURA-DATOS-OOP/06-oop-modelado-datos.md |
| 12 (Chat stream) | StreamUseCase, Stream en capa de datos | 06-NIVEL-EXPERTO/04-streams-tiempo-real.md |
| 14 (Testing) | Fundamentos de testing y Mocktail | 05-TESTING/01-fundamentos/ |
| Todos | Clean Architecture (capas domain/data/presentation) | 01-CLEAN-ARCHITECTURE/ |

## Relaciones con otros módulos

| Capítulo 16 | Relacionado con | Naturaleza de la relación |
|---|---|---|
| 3 (Cubit básico) | 01-ARCH/05c (UserCubit CRUD) | Complementario: mismo concepto, 16 profundiza |
| 5-6 (Widgets) | 01-ARCH/05c (BlocProvider, Builder, context.read) | Complementario: 05c lo usa, 16 lo enseña |
| 10 (Multi-bloc) | 06-EXP/03 (comunicación cross-feature) | Complementario: 10 orquesta desde UI, 06 desde event bus |
| 12 (Chat stream) | 06-EXP/04 (StreamUseCase + Supabase/Firebase) | Complementario: 06 cubre datos, 12 cubre UI + Bloc |
| 14 (Testing) | 05-TESTING/04a (práctica blocTest + Mocktail) | Complementario: 14 es teoría/referencia, 04a es hands-on |
| 14 (Testing) | 01-ARCH/07 (testing por capas con blocTest) | Complementario: 01-ARCH lo usa en contexto de Clean Arch |
| 16 (Buenas prácticas) | 01-ARCH/08 (templates universales) | 01-ARCH provee boilerplate, 16 da guías de uso correcto |

## Lo que NO cubre este módulo

| Tema | Dónde está |
|---|---|
| sealed class, Equatable, copyWith (OOP) | 09-ESTRUCTURA-DATOS-OOP/ |
| StreamUseCase (patrón reactivo domain) | 06-NIVEL-EXPERTO/04-streams-tiempo-real.md |
| Event Bus (comunicación cross-feature) | 06-NIVEL-EXPERTO/03-comunicacion-features.md |
| Ejercicio práctico de blocTest | 05-TESTING/04a-practica-cubits-bloc-test.md |
| Prompts para IA generando BLoC | 07-IA-ASSISTANT/01-guia-ia.md |
