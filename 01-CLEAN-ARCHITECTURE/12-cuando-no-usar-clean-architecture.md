# 12: Cuándo NO Usar Clean Architecture

> Clean Architecture no es la respuesta a todo. Usarla donde no corresponde es over-engineering que te frena.

---

## La regla de oro

**"No uses arquitectura para un proyecto que no la necesita."**

---

## Cuándo SÍ usar Clean Architecture

| Situación | ¿Por qué? |
|-----------|------------|
| App con 10+ features | Necesitas separación para no enloquecer |
| Equipo de 3+ devs | Cada uno trabaja en una capa sin chocar |
| App con 2+ años de vida | Mantenibilidad a largo plazo |
| Múltiples fuentes de datos | Repo abstracta facilita cambiar Supabase por API |
| Testing exhaustivo | Capas facilitan mocking |
| App con dominio complejo | Business logic compleja necesita estructura |

---

## Cuándo NO usar Clean Architecture

| Situación | ¿Por qué no? | ¿Qué usar? |
|-----------|---------------|------------|
| Prototipo / MVP | Velocidad > arquitectura | Código directo |
| App de una pantalla | No hay separación que valga | Cubit simple + API directa |
| Script / Tool | No es una app Flutter | Dart script |
| Hackathon (24h) | No hay tiempo | Lo que funcione |
| App solo UI (sin lógica) | No hay domain layer | Widgets directos |
| POC interna | Es desechable | Código simple |

---

## Ejemplo: Prototipo sin Clean Architecture

```dart
// ❌ OVER-ENGINEERING para un prototipo
// 5 archivos, 3 capas, 2 abstracciones... para mostrar 1 lista

// lib/domain/entities/post.dart
// lib/domain/repositories/post_repository.dart
// lib/domain/usecases/get_posts.dart
// lib/data/models/post_model.dart
// lib/data/datasources/post_remote_datasource.dart
// lib/data/repositories/post_repository_impl.dart
// lib/presentation/cubit/posts_cubit.dart
// lib/presentation/cubit/posts_state.dart
// lib/presentation/pages/home_page.dart
// = 9 archivos para una lista de posts

// ✅ PROTOTIPO RÁPIDO (mismo resultado, 1 archivo)
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Post {
  final int id;
  final String title;
  Post({required this.id, required this.title});
  factory Post.fromJson(Map<String, dynamic> json) =>
      Post(id: json['id'], title: json['title']);
}

class HomePage extends StatefulWidget {
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  List<Post> posts = [];
  bool loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final res = await http.get(Uri.parse('https://jsonplaceholder.typicode.com/posts'));
    setState(() {
      posts = (jsonDecode(res.body) as List).map((j) => Post.fromJson(j)).toList();
      loading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (loading) return CircularProgressIndicator();
    return ListView.builder(
      itemCount: posts.length,
      itemBuilder: (_, i) => ListTile(title: Text(posts[i].title)),
    );
  }
}
```

---

## El Spectrum de Complejidad

```
Script → Prototipo → App Simple → App Compleja → Enterprise
  │          │            │              │              │
  │          │            │              │              │
Ninguna   Ninguna    Cubit +       Clean Arch     Clean Arch
                    Repository     + DI + Tests    + Modular
```

---

## Señales de que estás over-engineering

| Señal | Qué hacer |
|-------|-----------|
| Más archivos que features | Reducir abstracciones |
| UseCases que solo pasan datos | Eliminar UseCases innecesarios |
| Interfaces que solo tienen 1 implementación | Eliminar la interfaz |
| Más de 3 niveles de abstracción | Aplanar la estructura |
| Tardas 30 min en agregar una feature | La arquitectura te frena |

---

## La regla práctica

```
¿Tiene más de 3 features?     → Clean Architecture vale la pena
¿Tiene menos de 3 features?   → Cubit + Repository simple
¿Es desechable?               → Lo que funcione
¿Tiene testing?               → Clean Architecture facilita
¿No tiene testing?            → Clean Architecture no ayuda tanto
```

---

## Ejemplo: App real que evoluciona

```
Fase 1 (semana 1-2): Prototipo
  → 1 archivo, todo junto
  → Solo para validar la idea

Fase 2 (semana 3-4): MVP
  → Separar en 2-3 archivos
  → Agregar Cubit
  → Empezar a testear

Fase 3 (mes 2+): Producción
  → Clean Architecture completa
  → DI, Tests, States formales
  → Deploy a users reales
```

---

## Conclusión

> **Clean Architecture es una herramienta, no un dogma.**
> Úsala cuando el proyecto lo necesite. No la uses porque "es la correcta".

La mejor arquitectura es la que se adapta a las necesidades reales del proyecto.

---

**Volver al índice:** [README.md](./README.md)
