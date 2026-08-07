#!/usr/bin/env python3
"""Generador de los PDFs del módulo 20 - Resolución de Problemas Algorítmicos.

Guía completa  -> guia-completa.css + guia-completa.html (render: Chrome headless)
Guía resumen   -> guia-resumen.css  + guia-resumen.html  (render: wkhtmltopdf)

Uso:
    python3 build_pdf.py

Salidas (sobrescribe):
    pdf/20-RESOLUCION-PROBLEMAS-ALGORITMOS.pdf
    pdf/GUIA-RESUMEN-20-RESOLUCION-PROBLEMAS-ALGORITMOS.pdf
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
# Definición de la guía completa: partes -> capítulos -> archivo .md
# ---------------------------------------------------------------------------

PARTS = [
    (
        "Parte 1 · Metodología",
        [
            ("01", "Paso 01", "01-metodologia-general.md"),
            ("02", "Paso 02", "02-analisis-complejidad.md"),
            ("03", "Paso 03", "03-reconocimiento-patrones.md"),
        ],
    ),
    (
        "Parte 2 · Estructuras y patrones",
        [
            ("04", "Paso 04", "04-estructuras-datos-referencia.md"),
            ("05", "Paso 05", "05-patrones-avanzados.md"),
        ],
    ),
    (
        "Parte 3 · Comunicación y práctica",
        [
            ("06", "Paso 06", "06-comunicacion-y-pseudocodigo.md"),
            ("07", "Paso 07", "07-ejercicios-practica.md"),
        ],
    ),
    (
        "Parte 4 · Recursión y System Design",
        [
            ("09", "Paso 09", "09-recursion-y-backtracking.md"),
            ("10", "Paso 10", "10-system-design-basico.md"),
        ],
    ),
    (
        "Parte 5 · Errores y más práctica",
        [
            ("11", "Paso 11", "11-errores-comunes-patron.md"),
            ("12", "Paso 12", "12-ejercicios-adicionales.md"),
        ],
    ),
    (
        "Parte 6 · Cierre",
        [
            ("08", "Anexo", "08-recursos-externos.md"),
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
    """Convierte un .md a HTML con pandoc, quitando el H1 de portada del capítulo."""
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
        print(f"pandoc falló en {path}:\n{proc.stderr[:2000]}", file=sys.stderr)
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
        + f'<p class="toc-count">{total} capítulos · Protocolo de Resolución de Problemas Algorítmicos en Dart</p>'
        + "\n".join(toc_rows)
        + "</div>"
    )

    cover = """<div class="cover">
  <span class="module-tag">Módulo 20</span>
  <h1>Resolución de<br>Problemas<br>Algorítmicos</h1>
  <p class="subtitle">Un protocolo metódico y universal para resolver problemas de algoritmos, estructuras de datos y POO — desde los básicos hasta retos tipo HackerRank y LeetCode.</p>
  <table class="meta">
    <tr>
      <td><span class="label">Enfoque</span><span class="value">Framework de 6 pasos + reconocimiento de patrones</span></td>
      <td><span class="label">Lenguaje</span><span class="value">Dart (templates listos para usar)</span></td>
    </tr>
    <tr>
      <td><span class="label">Nivel</span><span class="value">Intermedio a Avanzado</span></td>
      <td><span class="label">Tiempo estimado</span><span class="value">25–35 horas (con práctica)</span></td>
    </tr>
  </table>
  <div class="tags"><span>Big-O</span><span>Patrones</span><span>Recursión</span><span>System Design</span></div>
</div>"""

    doc = (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>20 — Resolución de Problemas Algorítmicos</title>\n"
        '<link rel="stylesheet" href="guia-completa.css">\n</head>\n<body>\n'
        + cover
        + toc
        + "\n".join(chapters)
        + "\n</body>\n</html>\n"
    )

    out = os.path.join(SRC, "guia-completa.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"guia-completa.html escrito ({len(doc)} bytes, {total} capítulos)")
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

    # 1) Guía completa
    complete_html = build_complete()
    out_complete = os.path.join(DIST, "20-RESOLUCION-PROBLEMAS-ALGORITMOS.pdf")
    render_chrome(complete_html, out_complete)

    # 2) Guía resumen
    out_resumen = os.path.join(DIST, "GUIA-RESUMEN-20-RESOLUCION-PROBLEMAS-ALGORITMOS.pdf")
    render_wkhtmltopdf(RESUMEN_HTML, out_resumen)

    # 3) Copiar a la raíz del módulo (sobrescribir)
    for src, dst in [
        (out_complete, os.path.join(PDF_DIR, "20-RESOLUCION-PROBLEMAS-ALGORITMOS.pdf")),
        (out_resumen, os.path.join(PDF_DIR, "GUIA-RESUMEN-20-RESOLUCION-PROBLEMAS-ALGORITMOS.pdf")),
    ]:
        shutil.copy2(src, dst)
        print(f"copiado: {dst}")

    print("OK")


if __name__ == "__main__":
    main()
