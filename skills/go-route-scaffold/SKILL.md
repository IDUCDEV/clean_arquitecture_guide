---
name: go-route-scaffold
description: Generate or update GoRouter configuration with standard routes, optional auth redirect, and optional Sentry observer. Only generates structure — route implementations are left empty for the developer to complete.
---

# go-route-scaffold — Scaffold de rutas con GoRouter

Genera la configuración de GoRouter para la aplicación, soportando redirect de autenticación y observadores como Sentry.

> **Orquestación:** esta skill suele invocarse desde `clean-arch-feature` cuando el usuario pide `wiring: [router]`. En ese flujo, las páginas generadas por el feature se pasan como entradas de `routes`. Puede usarse también de forma independiente sobre páginas existentes.

## Input requerido

| Parámetro | Descripción | Ejemplo |
|---|---|---|
| `app_name` | Nombre del paquete | `my_app` |
| `has_auth` | Incluir redirect de autenticación | `true` / `false` |
| `auth_cubit` | Nombre del Cubit de auth (si has_auth) | `AuthCubit` |
| `auth_states` | Estados de auth (si has_auth) | `authenticated: AuthAuthenticated` |
| `use_sentry` | Incluir SentryNavigatorObserver | `true` / `false` |
| `routes` | Lista de rutas a generar | (ver tabla abajo) |

### Formato de `routes`

```yaml
- path: /
  page: HomePage
  feature: home

- path: /products
  page: ProductsPage
  feature: product
  children:
    - path: :id
      page: ProductDetailPage
      feature: product

- path: /login
  page: LoginPage
  feature: auth
  auth_required: false
```

## Output

`lib/core/router/app_router.dart`

## Templates

### Básico (sin auth)

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
// TODO: import pages
// import 'package:{app_name}/features/home/presentation/pages/home_page.dart';
// import 'package:{app_name}/features/{feature}/presentation/pages/{feature}_page.dart';

class AppRouter {
  late final GoRouter router;

  AppRouter() {
    router = GoRouter(
      initialLocation: '/',
      routes: [
        // GoRoute(
        //   path: '/',
        //   builder: (_, __) => const HomePage(),
        // ),
        // GoRoute(
        //   path: '/{feature}s',
        //   builder: (_, __) => const {Feature}Page(),
        //   routes: [
        //     GoRoute(
        //       path: ':id',
        //       builder: (_, state) => {Feature}DetailPage(
        //         id: state.pathParameters['id']!,
        //       ),
        //     ),
        //   ],
        // ),
      ],
    );
  }
}
```

### Con auth redirect

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
// TODO: import pages
// import 'package:{app_name}/features/auth/presentation/cubit/auth_cubit.dart';
// import 'package:{app_name}/features/auth/presentation/pages/login_page.dart';
// import 'package:{app_name}/features/home/presentation/pages/home_page.dart';

class AppRouter {
  late final GoRouter router;

  AppRouter() {
    router = GoRouter(
      initialLocation: '/login',
      redirect: (context, state) {
        final auth = context.read<AuthCubit>().state;
        final estaAutenticado = auth is AuthAuthenticated;
        final estaEnLogin = state.matchedLocation == '/login';

        // TODO: implement auth redirect
        // if (!estaAutenticado && !estaEnLogin) return '/login';
        // if (estaAutenticado && estaEnLogin) return '/';
        return null;
      },
      routes: [
        GoRoute(
          path: '/login',
          builder: (_, __) {
            // TODO: replace with LoginPage
            throw UnimplementedError('LoginPage not implemented');
          },
        ),
        GoRoute(
          path: '/',
          builder: (_, __) {
            // TODO: replace with HomePage
            throw UnimplementedError('HomePage not implemented');
          },
        ),
        // GoRoute(
        //   path: '/{feature}s',
        //   builder: (_, __) => const {Feature}Page(),
        //   routes: [
        //     GoRoute(
        //       path: ':id',
        //       builder: (_, state) => {Feature}DetailPage(
        //         id: state.pathParameters['id']!,
        //       ),
        //     ),
        //   ],
        // ),
      ],
    );
  }
}
```

### Con Sentry

```dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:sentry_flutter/sentry_flutter.dart';
// TODO: import pages

class AppRouter {
  late final GoRouter router;

  AppRouter() {
    router = GoRouter(
      initialLocation: '/',
      routes: [
        // GoRoute(path: '/', builder: (_, __) => const HomePage()),
      ],
      observers: [
        SentryNavigatorObserver(),
      ],
    );
  }
}
```

**Configuración adicional en `main.dart`:**
```dart
await SentryFlutter.init(
  (options) {
    options.dsn = 'your-dsn';
    options.tracesSampleRate = 1.0;
  },
  appRunner: () => runApp(const MyApp()),
);
```

## Workflow

1. Preguntar al usuario: app_name, has_auth, use_sentry, y lista de rutas (path, page, feature, children, auth_required)
2. Si `lib/core/router/app_router.dart` no existe, crearlo con el template correspondiente
3. Si existe, añadir las nuevas rutas a la lista `routes` respetando la estructura anidada
4. Los builders de cada ruta van con `throw UnimplementedError()` o comentario `// TODO: implement`
5. Los imports de páginas van comentados — el usuario debe descomentarlos
6. Recordar al usuario que debe:
   - Envolver `MaterialApp.router(routerConfig: AppRouter().router)` con `MultiBlocProvider` que incluya `AuthCubit`
   - Si usa Sentry, configurar `SentryFlutter.init()` en `main.dart` con su DSN
   - Verificar que el nombre del estado autenticado (`AuthAuthenticated`) coincide con el definido en su cubit de auth
