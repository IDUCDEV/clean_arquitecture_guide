# 03 — Actions Esenciales para Flutter + Supabase

---

## 1. `actions/checkout` — Descargar el código

```yaml
- uses: actions/checkout@v4
```

La action más básica. Descarga el repositorio en el runner. Sin esto no hay nada que testear.

---

## 2. `subosito/flutter-action` — Instalar Flutter

```yaml
- uses: subosito/flutter-action@v2
  with:
    flutter-version: '3.24.0'
    channel: 'stable'
    cache: true
```

**¿Qué hace?** Descarga e instala Flutter en el runner. Sin esto no puedes ejecutar `flutter test` ni `flutter build`.

| Parámetro | Valores | Default |
|-----------|---------|---------|
| `flutter-version` | `'3.24.0'`, `'3.22.0'` | latest |
| `channel` | `stable`, `beta` | `stable` |
| `cache` | `true`, `false` | `false` |

---

## 3. `actions/cache` — Cachear dependencias

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.pub-cache
    key: ${{ runner.os }}-flutter-${{ hashFiles('**/pubspec.lock') }}
    restore-keys: |
      ${{ runner.os }}-flutter-
```

**¿Por qué?** `flutter pub get` descarga dependencias. Sin cache, cada ejecución tarda ~2 minutos en descargarlas. Con cache, ~5 segundos.

**¿Cómo funciona?**
1. Calcula una clave (`key`) basada en el contenido de `pubspec.lock`
2. Si la clave existe, restaura el cache
3. Si no, descarga las dependencias y las guarda con esa clave para futuras ejecuciones

---

## 4. `supabase/setup-cli` — Instalar Supabase CLI

```yaml
- uses: supabase/setup-cli@v1
  with:
    version: latest
```

**¿Qué hace?** Instala Supabase CLI para ejecutar `supabase start`, `supabase db lint`, `supabase test db`.

---

## 5. `softprops/action-gh-release` — Crear releases

```yaml
- uses: softprops/action-gh-release@v1
  with:
    files: |
      build/app/outputs/flutter-apk/app-release.apk
      build/app/outputs/bundle/release/app-release.aab
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**¿Qué hace?** Crea un Release en GitHub y sube los archivos especificados. Se usa típicamente cuando se pushea un tag `v*`.

---

## 6. `amannn/action-semantic-pull-request` — Validar PRs

```yaml
- uses: amannn/action-semantic-pull-request@v5
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**¿Qué hace?** Valida que el título del PR siga el formato Conventional Commits (`feat:`, `fix:`, `refactor:`, etc.).

---

## 7. Tabla de acciones recomendadas

| Action | Propósito | ¿Obligatoria? |
|--------|-----------|--------------|
| `actions/checkout@v4` | Descargar código | ✅ Sí |
| `subosito/flutter-action@v2` | Instalar Flutter | ✅ Si tienes Flutter |
| `actions/cache@v4` | Cachear dependencias | 👍 Muy recomendada |
| `supabase/setup-cli@v1` | Instalar Supabase CLI | ✅ Si tests con Supabase |
| `softprops/action-gh-release@v1` | Publicar releases | 👍 Para builds |
| `amannn/action-semantic-pull-request@v5` | Validar PRs | 👍 Para equipos |

---

## 📚 Referencias

- [GitHub | Actions documentation](https://docs.github.com/en/actions) — Guías y referencia de GitHub Actions
- [GitHub | Workflow syntax](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) — Sintaxis YAML de workflows
- [GitHub | Security hardening](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions) — Buenas prácticas de seguridad en Actions

---

**Siguiente**: [04-workflows-analisis.md](./04-workflows-analisis.md) — Análisis de los workflows del proyecto
