#!/usr/bin/env python3
"""Generador de los PDFs del módulo 22 - Diseño de Sistemas.

Guía completa  -> guia-completa.css + guia-completa.html (render: Chrome headless)
Guía resumen   -> guia-resumen.css  + guia-resumen.html  (render: wkhtmltopdf)

Uso:
    python3 build_pdf.py

Salidas (sobrescribe):
    pdf/22-DISENIO-SISTEMAS.pdf
    pdf/GUIA-RESUMEN-22-DISENIO-SISTEMAS.pdf
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
        "Parte 1 · Fundamentos y escala",
        [
            ("00", "Capítulo 00", "00-fundamentos-system-design.md"),
            ("01", "Capítulo 01", "01-clarificar-requisitos.md"),
            ("02", "Capítulo 02", "02-estimacion-de-escala.md"),
            ("03", "Capítulo 03", "03-componentes-arquitectura.md"),
        ],
    ),
    (
        "Parte 2 · Datos y rendimiento",
        [
            ("04", "Capítulo 04", "04-modelado-de-datos.md"),
            ("05", "Capítulo 05", "05-cache-y-rendimiento.md"),
        ],
    ),
    (
        "Parte 3 · Tiempo real y escalabilidad",
        [
            ("06", "Capítulo 06", "06-realtime-y-streaming.md"),
            ("07", "Capítulo 07", "07-escalabilidad-alta-disponibilidad.md"),
        ],
    ),
    (
        "Parte 4 · Seguridad y operación",
        [
            ("08", "Capítulo 08", "08-seguridad-en-diseno.md"),
            ("09", "Capítulo 09", "09-observabilidad-monitoreo.md"),
            ("10", "Capítulo 10", "10-offline-first.md"),
        ],
    ),
    (
        "Parte 5 · Plantilla y casos integradores",
        [
            ("11", "Capítulo 11", "11-plantilla-diseno-sistema.md"),
            ("12", "Caso 12", "12-caso-feed-red-social.md"),
            ("13", "Caso 13", "13-caso-chat-mensajeria.md"),
            ("14", "Caso 14", "14-caso-ecommerce-escalable.md"),
            ("15", "Caso 15", "15-caso-saas-multi-tenant.md"),
        ],
    ),
    (
        "Parte 6 · Práctica y cierre",
        [
            ("16", "Capítulo 16", "16-ejercicios-practica.md"),
            ("17", "Capítulo 17", "17-recursos-externos.md"),
            ("BI", "Anexo", "BIBLIOGRAFIA.md"),
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
        + f'<p class="toc-count">{total} capítulos · Diseño de Sistemas a escala con Flutter + Supabase</p>'
        + "\n".join(toc_rows)
        + "</div>"
    )

    cover = """<div class="cover">
  <span class="module-tag">Módulo 22</span>
  <h1>Diseño de<br>Sistemas</h1>
  <p class="subtitle">Escala un sistema completo con Flutter + Supabase: estimación, modelado de datos, cache, realtime, alta disponibilidad, seguridad y observabilidad. Con plantilla reutilizable y 4 casos integradores.</p>
  <table class="meta">
    <tr>
      <td><span class="label">Enfoque</span><span class="value">System Design Primer + DDIA + Supabase</span></td>
      <td><span class="label">Stack</span><span class="value">Flutter + Supabase (Postgres, Realtime, Edge)</span></td>
    </tr>
    <tr>
      <td><span class="label">Nivel</span><span class="value">Intermedio a Avanzado</span></td>
      <td><span class="label">Tiempo estimado</span><span class="value">25–35 horas</span></td>
    </tr>
  </table>
  <div class="tags"><span>Escalabilidad</span><span>Cache</span><span>Realtime</span><span>CAP</span></div>
</div>"""

    doc = (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>22 — Diseño de Sistemas</title>\n"
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
    out_complete = os.path.join(DIST, "22-DISENIO-SISTEMAS.pdf")
    render_chrome(complete_html, out_complete)

    # 2) Guía resumen
    out_resumen = os.path.join(DIST, "GUIA-RESUMEN-22-DISENIO-SISTEMAS.pdf")
    render_wkhtmltopdf(RESUMEN_HTML, out_resumen)

    # 3) Copiar a la raíz del módulo (sobrescribir)
    for src, dst in [
        (out_complete, os.path.join(PDF_DIR, "22-DISENIO-SISTEMAS.pdf")),
        (out_resumen, os.path.join(PDF_DIR, "GUIA-RESUMEN-22-DISENIO-SISTEMAS.pdf")),
    ]:
        shutil.copy2(src, dst)
        print(f"copiado: {dst}")

    print("OK")


if __name__ == "__main__":
    main()
