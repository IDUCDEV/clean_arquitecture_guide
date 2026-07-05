# CLI y .pen Format

> Aprende a usar Pencil desde la terminal con el CLI interactivo, y entiende el formato `.pen` para trabajar con Git diffs y merges como si fuera código.

---

## Índice

- [Pencil CLI](#pencil-cli)
- [Modo Interactivo](#modo-interactivo)
- [Modo Agente (con Prompts)](#modo-agente-con-prompts)
- [Batch Processing](#batch-processing)
- [CI/CD y Variables de Entorno](#cicd-y-variables-de-entorno)
- [El Formato .pen](#el-formato-pen)
- [Git Diffs y Merges](#git-diffs-y-merges)
- [Mini-práctica](#mini-práctica)

---

## Pencil CLI

El CLI de Pencil es una herramienta de terminal independiente. Puede ejecutar operaciones de diseño sin interfaz gráfica.

### Instalación

```bash
npm install -g @pencil.dev/cli
```

Verificar instalación:

```bash
pencil version
```

**Requisito:** Node.js 18 o superior.

### Autenticación

El CLI requiere autenticación antes de usar modos que involucren AI. Para el modo interactivo (sin AI) no necesitas autenticarte.

**Login interactivo:**
```bash
pencil login
```
Inicia sesión con email + contraseña o email + OTP.

**CLI Key (para CI/CD):**
```bash
export PENCIL_CLI_KEY=pencil_cli_...
```

### Comandos Básicos

| Comando | Descripción |
|---|---|
| `pencil login` | Iniciar sesión |
| `pencil status` | Ver estado de autenticación |
| `pencil version` | Versión instalada |
| `pencil interactive` | Iniciar shell interactivo |

---

## Modo Interactivo

El modo interactivo te permite ejecutar **comandos MCP directamente** en un archivo `.pen`, sin usar prompts de AI. Esto es ideal para scripting, automatización y control fino.

### App Mode

Conecta a una instancia de Pencil ya ejecutándose (Desktop o extensión). Los cambios se ven en vivo.

```bash
pencil interactive -a desktop -i mi-diseno.pen
```

```bash
pencil interactive -a vscode -i mi-diseno.pen
```

### Headless Mode

Inicia un editor sin interfaz gráfica. No necesitas Pencil abierto.

```bash
# Nuevo archivo vacío
pencil interactive -o salida.pen

# Editar archivo existente
pencil interactive -i entrada.pen -o salida.pen
```

### Comandos del Shell

Una vez dentro del shell interactivo, escribes comandos con sintaxis de función:

```
tool_name({ key: value })
tool_name()
save()
exit()
```

**Comandos especiales:**
- `save()` — Guarda el documento en el archivo de salida
- `exit()` — Sale del shell

### Ejemplo de Sesión

```
$ pencil interactive -o mi-diseno.pen

pencil > get_editor_state({ include_schema: true })
pencil > batch_get({ patterns: [{ type: "frame" }] })
pencil > batch_design({
  operations: "hero=I(document,{type:'frame',name:'Hero',x:0,y:0,width:1440,height:900,fill:'#0A0A0A'})"
})
pencil > get_screenshot({ nodeId: "hero" })
pencil > save()
pencil > exit()
```

---

## Modo Agente (con Prompts)

El modo agente usa AI para crear o modificar diseños. No es el foco de este módulo (estamos aprendiendo a diseñar manualmente), pero es útil conocerlo.

```bash
pencil --out login.pen --prompt "Create a login page with email and password fields"
```

**Opciones principales:**

| Opción | Descripción |
|---|---|
| `--in, -i <path>` | Archivo `.pen` de entrada (opcional) |
| `--out, -o <path>` | Archivo `.pen` de salida |
| `--prompt, -p <text>` | Prompt de AI |
| `--model, -m <id>` | Modelo (claude-opus-4-6, claude-sonnet-4-6, claude-haiku-4-5) |
| `--export, -e <path>` | Exportar imagen al finalizar |
| `--export-scale <n>` | Escala de exportación (default 1) |
| `--export-type <type>` | PNG, JPEG, WebP, PDF |

---

## Batch Processing

El CLI permite procesar **múltiples diseños** en secuencia desde un archivo JSON.

```bash
pencil --tasks batch.json
```

**Ejemplo de `batch.json`:**
```json
{
  "tasks": [
    {
      "out": "landing.pen",
      "prompt": "Create a landing page with hero section"
    },
    {
      "in": "app.pen",
      "out": "app-v2.pen",
      "prompt": "Add a dark mode toggle"
    }
  ]
}
```

**Campos por tarea:**

| Campo | Requerido | Descripción |
|---|---|---|
| `out` | ✅ | Archivo de salida |
| `prompt` | ✅ | Prompt de AI |
| `in` | ❌ | Archivo de entrada |
| `model` | ❌ | Modelo override |

---

## CI/CD y Variables de Entorno

### Uso en Pipelines

```bash
export PENCIL_CLI_KEY=pencil_cli_...
export ANTHROPIC_API_KEY=sk-ant-...

pencil --out onboarding.pen --prompt "Create onboarding screens"
```

### Variables de Entorno

| Variable | Descripción |
|---|---|
| `PENCIL_CLI_KEY` | API key para CI/CD |
| `ANTHROPIC_API_KEY` | API key de Anthropic |
| `PENCIL_API_BASE` | URL base de la API (default: `https://api.pencil.dev`) |
| `DEBUG` | Logs de debug |

---

## El Formato .pen

Los archivos `.pen` son **JSON** estructurado. Esto significa que son legibles, diffiables y mergeables como cualquier código.

### Estructura Básica

```json
{
  "version": 1,
  "pages": [
    {
      "id": "page_1",
      "name": "Page 1",
      "children": [
        {
          "id": "node_1",
          "type": "frame",
          "name": "iPhone 14",
          "x": 100,
          "y": 100,
          "width": 390,
          "height": 844,
          "fill": { "type": "solid", "color": "#FFFFFF" },
          "children": [
            {
              "id": "node_2",
              "type": "rectangle",
              "name": "Botón",
              "x": 20,
              "y": 400,
              "width": 160,
              "height": 44,
              "fill": { "type": "solid", "color": "#3B82F6" },
              "cornerRadius": 8
            }
          ]
        }
      ]
    }
  ]
}
```

### Campos Comunes

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | string | Identificador único del nodo |
| `type` | string | `frame`, `group`, `rectangle`, `ellipse`, `text`, `path`, etc. |
| `name` | string | Nombre que aparece en Layers Panel |
| `x`, `y` | number | Posición en el canvas |
| `width`, `height` | number | Dimensiones |
| `fill` | object | Relleno (sólido, gradiente, imagen) |
| `stroke` | object | Borde |
| `cornerRadius` | number | Radio de esquina |
| `effects` | array | Efectos (sombras, blur) |
| `opacity` | number | Opacidad (0-1) |

### Ventajas del Formato JSON

- **Git-friendly:** Puedes ver exactamente qué cambió en cada commit
- **Mergeable:** Si dos personas editan el mismo archivo, Git puede hacer merge
- **Legible:** Puedes abrir un `.pen` en cualquier editor de texto
- **Procesable:** Puedes escribir scripts que generen o modifiquen `.pen` files

---

## Git Diffs y Merges

### Ejemplo de Diff

```diff
 {
   "id": "node_2",
   "type": "rectangle",
   "name": "Botón Primario",
-  "fill": { "type": "solid", "color": "#3B82F6" },
+  "fill": { "type": "solid", "color": "#10B981" },
   "cornerRadius": 8,
-  "width": 160,
+  "width": 180,
   "height": 44
 }
```

Este diff muestra claramente que:
- Se cambió el color de azul a verde
- Se aumentó el ancho de 160 a 180px

### Buenas Prácticas con Git

- **Nombres descriptivos** en las capas → diffs más legibles
- **Commits frecuentes** → cada cambio atómico
- **Commits descriptivos** → "Change primary color to green" en vez de "Update design"
- **No commitear `.pen` y `.lib.pen`** al mismo tiempo si no están relacionados

### Merge Conflicts

Si dos personas modifican el mismo `.pen`, puede haber conflictos como en cualquier archivo de código. Resuélvelo como lo harías con código:

1. Busca los marcadores `<<<<<<<`, `=======`, `>>>>>>>`
2. Decide qué versión conservar
3. Elimina los marcadores
4. Commit

---

## Mini-práctica

### Ejercicio 1: Inspeccionar .pen en Bruto

1. Abre Pencil y crea un frame de 390×844 con un rectángulo azul y un texto
2. Guarda el archivo como `test.pen`
3. Ábrelo en VS Code (o cualquier editor de texto)
4. Observa la estructura JSON
5. Localiza:
   - El frame y sus dimensiones
   - El rectángulo y su color
   - El texto y su contenido

### Ejercicio 2: Hacer un Git Diff

```bash
# En la terminal, en el directorio de tu proyecto:
git init  # si no es un repo todavía
cp test.pen test.pen.bak  # respaldo
```

1. En Pencil, modifica el color del rectángulo
2. Guarda
3. En la terminal:
```bash
diff test.pen.bak test.pen
```
4. Observa las líneas que cambiaron

### Ejercicio 3: CLI Interactivo (Headless)

```bash
# Instalar CLI si no lo tienes
npm install -g @pencil.dev/cli

# Iniciar shell interactivo headless
pencil interactive -o test-cli.pen
```

Dentro del shell:
```
pencil > batch_get({ patterns: [{ type: "frame" }] })
pencil > batch_design({
  operations: "mi_frame=I(document,{type:'frame',name:'Mi Frame',width:400,height:600,fill:'#F3F4F6'})"
})
pencil > batch_get({ patterns: [{ type: "frame" }] })
pencil > save()
pencil > exit()
```

Verifica que `test-cli.pen` se creó correctamente.

### Ejercicio 4: Ver Estado del CLI

```bash
pencil status
pencil version
pencil --list-models
```

### Ejercicio 5: Abrir .pen en Editor de Texto

1. Abre `test.pen` en VS Code
2. Cambia manualmente el color del rectángulo editando el JSON
3. Guarda
4. Abre el archivo en Pencil — el color debería haber cambiado

---

## Checklist

- [ ] Instalé el CLI de Pencil (`npm install -g @pencil.dev/cli`)
- [ ] Usé `pencil interactive -o archivo.pen`
- [ ] Ejecuté comandos MCP básicos en el shell interactivo
- [ ] Usé `save()` y `exit()` en el shell
- [ ] Entendí la estructura JSON de un archivo `.pen`
- [ ] Modifiqué manualmente un `.pen` en un editor de texto
- [ ] Hice diff de un `.pen` antes y después de cambios
- [ ] Comprendí que los `.pen` son Git-friendly

---

## 📚 Referencias

- [Pencil | Documentación oficial](https://pencil.design/docs) — Guías de uso y referencia
- [Pencil | Ayuda](https://help.pencil.design) — Centro de ayuda y tutoriales

---

> 📖 **Siguiente:** [Keyboard Shortcuts](./09-keyboard-shortcuts.md)
