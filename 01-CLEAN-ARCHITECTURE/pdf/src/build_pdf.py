#!/usr/bin/env python3
"""Generador de los PDFs del modulo 01 - Clean Architecture para Flutter.

Guia completa  -> guia-completa.css + guia-completa.html (render: Chrome headless)
Guia resumen   -> guia-resumen.css  + guia-resumen.html  (render: wkhtmltopdf)

Uso:
    python3 build_pdf.py

Salidas (sobrescribe):
    pdf/01-CLEAN-ARCHITECTURE.pdf
    pdf/GUIA-RESUMEN-01-CLEAN-ARCHITECTURE.pdf
"""

import html
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.dirname(os.path.dirname(BASE))
SRC = BASE
DIST = os.path.join(BASE, "dist")
PDF_DIR = MODULE

COVER = os.path.join(BASE, "guia-completa.css")
RESUMEN_HTML = os.path.join(BASE, "guia-resumen.html")
RESUMEN_CSS = os.path.join(BASE, "guia-resumen.css")

# ---------------------------------------------------------------------------
# Definicion de la guia completa: partes -> capitulos -> archivo .md
# ---------------------------------------------------------------------------

PARTS = [
    (
        "Parte 1 · Fundamentos",
        [
            ("01", "Capitulo 01", "01-introduccion-y-filosofia.md"),
            ("02", "Capitulo 02", "02-las-4-capas.md"),
            ("03", "Capitulo 03", "03-estructura-de-carpetas.md"),
            ("04", "Capitulo 04", "04-flujo-de-datos.md"),
        ],
    ),
    (
        "Parte 2 · Implementacion CRUD",
        [
            ("05", "Introduccion", "05-implementacion-crud-intro.md"),
            ("05a", "Domain Layer", "05a-domain-layer.md"),
            ("05b", "Data Layer", "05b-data-layer.md"),
            ("05c", "Presentation + UI", "05c-presentation-ui-layer.md"),
        ],
    ),
    (
        "Parte 3 · Infraestructura",
        [
            ("06", "Inyeccion de Deps", "06-inyeccion-de-dependencias.md"),
            ("07", "Templates", "07-templates-universales.md"),
            ("08", "Decisiones", "08-decisiones-de-arquitectura.md"),
        ],
    ),
    (
        "Parte 4 · Madurez y cierre",
        [
            ("09", "Migracion", "09-migracion-codigo-espagueti.md"),
            ("10", "SOLID", "10-solid-explicite.md"),
            ("11", "Anti-patrones", "11-anti-patrones-clean-architecture.md"),
            ("12", "Cuando NO usar", "12-cuando-no-usar-clean-architecture.md"),
        ],
    ),
]


def sh(cmd):
    print("+ " + " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.stdout.strip():
        print(proc.stdout.strip()[:4000])
    if proc.returncode != 0:
        print(proc.stderr.strip()[:4000], file=sys.stderr)
        sys.exit(proc.returncode)
    return proc


def md_to_html(path):
    """Convierte un .md a HTML con pandoc, quitando el H1 de portada del capitulo."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    title = ""
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        lines = lines[1:]
    body = "\n".join(lines).strip()
    proc = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html5", "--wrap=none"],
        input=body,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(f"pandoc fallo en {path}:\n{proc.stderr[:2000]}", file=sys.stderr)
        sys.exit(1)
    return title, proc.stdout


def build_complete():
    toc_rows = []
    chapters = []
    total = sum(len(chaps) for _, chaps in PARTS)

    for part_idx, (part, chaps) in enumerate(PARTS, start=1):
        toc_rows.append(f'<div class="part">{html.escape(part)}</div>')
        for num, kick, fname in chaps:
            path = os.path.join(MODULE, fname)
            title, content = md_to_html(path)
            num_label = f"{num}"
            toc_rows.append(
                '<div class="row">'
                f'<span class="num">{html.escape(num_label)}</span>'
                f'<span class="title">{html.escape(title)}</span>'
                "</div>"
            )
            chapters.append(
                '<div class="chapter">'
                '<div class="chapter-head">'
                f'<span class="num-chip">{html.escape(kick)}</span>'
                f'<div class="kick">{html.escape(part)}</div>'
                f"<h2>{html.escape(title)}</h2>"
                "</div>"
                f'<div class="article">{content}</div>'
                "</div>"
            )

    toc = (
        '<div class="toc">'
        "<h2>Contenido</h2>"
        + f'<p class="toc-count">{total} capitulos · 15 archivos · ~6-8 horas de lectura</p>'
        + "\n".join(toc_rows)
        + "</div>"
    )

    cover = """<div class="cover">
  <span class="module-tag">Modulo 01</span>
  <h1>Clean Architecture<br>para Flutter</h1>
  <p class="subtitle">Guia completa para aplicar Clean Architecture en Flutter con Supabase.
  Del codigo espagueti a una arquitectura escalable, testeable y mantenible.</p>
  <table class="meta">
    <tr>
      <td><span class="label">Arquitectura</span><span class="value">4 Capas · Domain-Driven · SOLID</span></td>
      <td><span class="label">Backend</span><span class="value">Supabase (BaaS) · REST API · Isar</span></td>
    </tr>
    <tr>
      <td><span class="label">Nivel</span><span class="value">Principiante a Intermedio</span></td>
      <td><span class="label">Tiempo estimado</span><span class="value">6-8 horas</span></td>
    </tr>
  </table>
  <div class="tags"><span>Clean Architecture</span><span>Flutter</span><span>Supabase</span><span>SOLID</span><span>fpdart</span></div>
</div>"""

    doc = (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>01 — Clean Architecture para Flutter</title>\n"
        '<link rel="stylesheet" href="guia-completa.css">\n</head>\n<body>\n'
        + cover
        + toc
        + "\n".join(chapters)
        + "\n</body>\n</html>\n"
    )

    out = os.path.join(SRC, "guia-completa.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"guia-completa.html escrito ({len(doc)} bytes, {total} capitulos)")
    return out


def render_chrome(in_html, out_pdf):
    url = "file://" + in_html
    sh(
        [
            "google-chrome",
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-software-rasterizer",
            "--no-pdf-header-footer",
            f"--print-to-pdf={out_pdf}",
            url,
        ]
    )


def render_wkhtmltopdf(in_html, out_pdf):
    sh(
        [
            "wkhtmltopdf",
            "--enable-local-file-access",
            "-s",
            "A4",
            "-T",
            "12mm",
            "-B",
            "12mm",
            "-L",
            "11mm",
            "-R",
            "11mm",
            in_html,
            out_pdf,
        ]
    )


def main():
    os.makedirs(DIST, exist_ok=True)

    # 1) Guia completa
    complete_html = build_complete()
    out_complete = os.path.join(DIST, "01-CLEAN-ARCHITECTURE.pdf")
    render_chrome(complete_html, out_complete)

    # 2) Guia resumen
    out_resumen = os.path.join(DIST, "GUIA-RESUMEN-01-CLEAN-ARCHITECTURE.pdf")
    render_wkhtmltopdf(RESUMEN_HTML, out_resumen)

    # 3) Copiar a la raiz del modulo (sobrescribir)
    for src, dst in [
        (out_complete, os.path.join(PDF_DIR, "01-CLEAN-ARCHITECTURE.pdf")),
        (out_resumen, os.path.join(PDF_DIR, "GUIA-RESUMEN-01-CLEAN-ARCHITECTURE.pdf")),
    ]:
        shutil.copy2(src, dst)
        print(f"copiado: {dst}")

    print("OK")


if __name__ == "__main__":
    main()
