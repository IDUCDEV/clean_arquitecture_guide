#!/usr/bin/env python3
"""Generador de los PDFs del modulo 04 - Almacenamiento Local con Isar.

Guia completa  -> guia-completa.css + guia-completa.html (render: Chrome headless)
Guia resumen   -> guia-resumen.css  + guia-resumen.html  (render: wkhtmltopdf)

Uso:
    python3 build_pdf.py

Salidas (sobrescribe):
    pdf/04-ALMACENAMIENTO-LOCAL.pdf
    pdf/GUIA-RESUMEN-04-ALMACENAMIENTO-LOCAL.pdf
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
        "Parte 1 · Fundamentos de Isar",
        [
            ("01", "Introduccion", "01-isar-introduccion.md"),
        ],
    ),
    (
        "Parte 2 · Modelos y Operaciones",
        [
            ("02", "Modelos y Operaciones", "02-modelos-operaciones.md"),
        ],
    ),
    (
        "Parte 3 · Implementacion",
        [
            ("03", "Implementacion", "03-implementacion-local-datasource.md"),
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
        + f'<p class="toc-count">{total} capitulos · 3 archivos · ~3-4 horas de lectura</p>'
        + "\n".join(toc_rows)
        + "</div>"
    )

    cover = """<div class="cover">
  <span class="module-tag">Modulo 04</span>
  <h1>Almacenamiento Local<br>con Isar</h1>
  <p class="subtitle">Guia completa para implementar almacenamiento local embebido con Isar Community en Flutter, siguiendo Clean Architecture.</p>
  <table class="meta">
    <tr>
      <td><span class="label">Base de datos</span><span class="value">Isar Community · NoSQL embebida</span></td>
      <td><span class="label">Backend</span><span class="value">Supabase (BaaS) · Cache local</span></td>
    </tr>
    <tr>
      <td><span class="label">Nivel</span><span class="value">Intermedio</span></td>
      <td><span class="label">Tiempo estimado</span><span class="value">3-4 horas</span></td>
    </tr>
  </table>
  <div class="tags"><span>Isar</span><span>Flutter</span><span>Clean Architecture</span><span>Cache</span><span>Supabase</span></div>
</div>"""

    doc = (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>04 — Almacenamiento Local con Isar</title>\n"
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
    out_complete = os.path.join(DIST, "04-ALMACENAMIENTO-LOCAL.pdf")
    render_chrome(complete_html, out_complete)

    # 2) Guia resumen
    out_resumen = os.path.join(DIST, "GUIA-RESUMEN-04-ALMACENAMIENTO-LOCAL.pdf")
    render_wkhtmltopdf(RESUMEN_HTML, out_resumen)

    # 3) Copiar a la raiz del modulo (sobrescribir)
    for src, dst in [
        (out_complete, os.path.join(PDF_DIR, "04-ALMACENAMIENTO-LOCAL.pdf")),
        (out_resumen, os.path.join(PDF_DIR, "GUIA-RESUMEN-04-ALMACENAMIENTO-LOCAL.pdf")),
    ]:
        shutil.copy2(src, dst)
        print(f"copiado: {dst}")

    print("OK")


if __name__ == "__main__":
    main()
