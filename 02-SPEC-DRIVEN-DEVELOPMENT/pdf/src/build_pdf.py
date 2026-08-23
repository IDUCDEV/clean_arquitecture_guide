#!/usr/bin/env python3
"""Generador de los PDFs del modulo 02 - Spec Driven Development.

Guia completa  -> guia-completa.css + guia-completa.html (render: Chrome headless)
Guia resumen   -> guia-resumen.css  + guia-resumen.html  (render: wkhtmltopdf)

Uso:
    python3 build_pdf.py

Salidas (sobrescribe):
    pdf/src/dist/02-SPEC-DRIVEN-DEVELOPMENT.pdf
    pdf/src/dist/GUIA-RESUMEN-02-SPEC-DRIVEN-DEVELOPMENT.pdf
    02-SPEC-DRIVEN-DEVELOPMENT.pdf                    (copia en raiz del modulo)
    GUIA-RESUMEN-02-SPEC-DRIVEN-DEVELOPMENT.pdf       (copia en raiz del modulo)
"""

import html
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.dirname(os.path.dirname(BASE))   # raiz del modulo
SRC = BASE
DIST = os.path.join(BASE, "dist")
PDF_DIR = MODULE

COVER_CSS = os.path.join(BASE, "guia-completa.css")
RESUMEN_HTML = os.path.join(BASE, "guia-resumen.html")
RESUMEN_CSS = os.path.join(BASE, "guia-resumen.css")

# ---------------------------------------------------------------------------
# Definicion de la guia completa: partes -> capitulos -> archivo .md
# ---------------------------------------------------------------------------

PARTS = [
    (
        "Parte 1 · Nucleo del modulo",
        [
            ("00", "Indice", "README.md"),
            ("01", "Teoria SDD", "01-teoria-sdd.md"),
            ("02", "Metodologia aplicada", "02-sdd-flutter-supabase.md"),
            ("03", "Herramienta OpenSpec", "03-openspec-guia-practica.md"),
            ("04", "Plantilla de cambio", "04-plantilla-cambio-openspec.md"),
            ("05", "Referencia rapida", "05-referencia-rapida.md"),
            ("06", "Auditoria de codigo IA", "06-auditoria-codigo-ia.md"),
        ],
    ),
    (
        "Parte 2 · Ejemplos de cambios",
        [
            ("E0", "Indice de ejemplos", "ejemplos-cambios/README.md"),
            # --- add-cart (walkthrough completo) ---
            ("EC1a", "add-cart · Proposal", "ejemplos-cambios/add-cart/proposal.md"),
            ("EC1b", "add-cart · Spec", "ejemplos-cambios/add-cart/specs/shopping-cart/spec.md"),
            ("EC1c", "add-cart · Design", "ejemplos-cambios/add-cart/design.md"),
            ("EC1d", "add-cart · Tasks", "ejemplos-cambios/add-cart/tasks.md"),
            # --- approve-reservas ---
            ("EC2a", "approve-reservas · Proposal", "ejemplos-cambios/approve-reservas/proposal.md"),
            ("EC2b", "approve-reservas · Spec", "ejemplos-cambios/approve-reservas/specs/appointments/spec.md"),
            ("EC2c", "approve-reservas · Design", "ejemplos-cambios/approve-reservas/design.md"),
            ("EC2d", "approve-reservas · Tasks", "ejemplos-cambios/approve-reservas/tasks.md"),
            # --- add-elearning-progress ---
            ("EC3a", "elearning-progress · Proposal", "ejemplos-cambios/add-elearning-progress/proposal.md"),
            ("EC3b", "elearning-progress · Spec", "ejemplos-cambios/add-elearning-progress/specs/enrollment-progress/spec.md"),
            ("EC3c", "elearning-progress · Design", "ejemplos-cambios/add-elearning-progress/design.md"),
            ("EC3d", "elearning-progress · Tasks", "ejemplos-cambios/add-elearning-progress/tasks.md"),
            # --- add-facturacion ---
            ("EC4a", "facturacion · Proposal", "ejemplos-cambios/add-facturacion/proposal.md"),
            ("EC4b", "facturacion · Spec", "ejemplos-cambios/add-facturacion/specs/invoicing/spec.md"),
            ("EC4c", "facturacion · Design", "ejemplos-cambios/add-facturacion/design.md"),
            ("EC4d", "facturacion · Tasks", "ejemplos-cambios/add-facturacion/tasks.md"),
            # --- add-delivery-seguimiento ---
            ("EC5a", "delivery-seguimiento · Proposal", "ejemplos-cambios/add-delivery-seguimiento/proposal.md"),
            ("EC5b", "delivery-seguimiento · Spec", "ejemplos-cambios/add-delivery-seguimiento/specs/delivery-tracking/spec.md"),
            ("EC5c", "delivery-seguimiento · Design", "ejemplos-cambios/add-delivery-seguimiento/design.md"),
            ("EC5d", "delivery-seguimiento · Tasks", "ejemplos-cambios/add-delivery-seguimiento/tasks.md"),
            # --- add-buyers ---
            ("EC6a", "add-buyers · Proposal", "ejemplos-cambios/add-buyers/proposal.md"),
            ("EC6b", "add-buyers · Spec", "ejemplos-cambios/add-buyers/specs/buyers-management/spec.md"),
            ("EC6c", "add-buyers · Design", "ejemplos-cambios/add-buyers/design.md"),
            ("EC6d", "add-buyers · Tasks", "ejemplos-cambios/add-buyers/tasks.md"),
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
    total_files = sum(len(chaps) for _, chaps in PARTS)

    for part_idx, (part, chaps) in enumerate(PARTS, start=1):
        toc_rows.append(f'<div class="part">{html.escape(part)}</div>')
        for num, kick, fname in chaps:
            path = os.path.join(MODULE, fname)
            if not os.path.isfile(path):
                print(f"AVISO: no existe {fname}, se omite", file=sys.stderr)
                continue
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

    total = sum(1 for c in chapters)
    toc = (
        '<div class="toc">'
        "<h2>Contenido</h2>"
        + f'<p class="toc-count">{total} capitulos · {total_files} archivos · ~6-8 horas de lectura</p>'
        + "\n".join(toc_rows)
        + "</div>"
    )

    cover = """<div class="cover">
  <span class="module-tag">Modulo 02</span>
  <h1>Spec Driven<br>Development</h1>
  <p class="subtitle">Teoria del libro SDDEquiposAgiles, herramienta OpenSpec CLI y metodologia
  aplicada a Flutter + Clean Architecture + Supabase. La especificacion como contrato;
  el cambio como unidad de trabajo.</p>
  <table class="meta">
    <tr>
      <td><span class="label">Teoria</span><span class="value">SDDEquiposAgiles_v.1 · Fases · Puertas</span></td>
      <td><span class="label">Herramienta</span><span class="value">OpenSpec CLI · EARS · Deltas</span></td>
    </tr>
    <tr>
      <td><span class="label">Stack</span><span class="value">Flutter · Clean Arch · Supabase</span></td>
      <td><span class="label">Nivel</span><span class="value">Intermedio a Avanzado</span></td>
    </tr>
  </table>
  <div class="tags"><span>SDD</span><span>OpenSpec</span><span>EARS</span><span>Flutter</span><span>Supabase</span><span>Clean Architecture</span></div>
</div>"""

    doc = (
        "<!DOCTYPE html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>02 — Spec Driven Development</title>\n"
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


def find_chrome():
    for cand in ("google-chrome", "google-chrome-stable", "chromium-browser"):
        path = shutil.which(cand)
        if path:
            return cand
    return None


def render_chrome(in_html, out_pdf):
    chrome = find_chrome()
    if not chrome:
        print("No se encontro Chrome/Chromium para renderizar la guia completa", file=sys.stderr)
        sys.exit(1)
    url = "file://" + in_html
    sh(
        [
            chrome,
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
    out_complete = os.path.join(DIST, "02-SPEC-DRIVEN-DEVELOPMENT.pdf")
    render_chrome(complete_html, out_complete)

    # 2) Guia resumen
    out_resumen = os.path.join(DIST, "GUIA-RESUMEN-02-SPEC-DRIVEN-DEVELOPMENT.pdf")
    render_wkhtmltopdf(RESUMEN_HTML, out_resumen)

    # 3) Copiar a la raiz del modulo (sobrescribir)
    for src, dst in [
        (out_complete, os.path.join(PDF_DIR, "02-SPEC-DRIVEN-DEVELOPMENT.pdf")),
        (out_resumen, os.path.join(PDF_DIR, "GUIA-RESUMEN-02-SPEC-DRIVEN-DEVELOPMENT.pdf")),
    ]:
        shutil.copy2(src, dst)
        print(f"copiado: {dst}")

    print("OK")


if __name__ == "__main__":
    main()
