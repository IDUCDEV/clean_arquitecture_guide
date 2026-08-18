#!/usr/bin/env python3
"""
Generador de PDFs - Módulo 06: Nivel Experto
Genera:
  06-NIVEL-EXPERTO.pdf      (guía completa, Chrome headless)
  GUIA-RESUMEN-06.pdf       (guía resumen, wkhtmltopdf)
"""

import subprocess
import sys
import os
from pathlib import Path

# ── Configuración ──────────────────────────────────────────────

HERE = Path(__file__).parent
MODULE_DIR = HERE.parent.parent  # 06-NIVEL-EXPERTO/
DIST = HERE / "dist"
DIST.mkdir(exist_ok=True)

CSS_COMPLETA = HERE / "guia-completa.css"
CSS_RESUMEN  = HERE / "guia-resumen.css"
HTML_RESUMEN = HERE / "guia-resumen.html"

# Chrome y wkhtmltopdf paths
CHROME = "google-chrome"
WKHTMLTOPDF = "wkhtmltopdf"

# ── Markdown → HTML ────────────────────────────────────────────

def md_to_html(md_path: Path) -> str:
    """Convierte un archivo Markdown a HTML usando pandoc."""
    result = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html5",
         "--standalone", "--metadata", "title=Nivel Experto",
         str(md_path)],
        capture_output=True, text=True, check=True
    )
    return result.stdout

# ── Generar HTML completo ─────────────────────────────────────

def build_full_html() -> str:
    """Concatena todos los markdowns en un solo HTML con CSS."""
    md_files = sorted(MODULE_DIR.glob("[0-9]*.md"))

    # CSS
    css_content = CSS_COMPLETA.read_text(encoding="utf-8")
    html_parts = [
        "<!DOCTYPE html>",
        "<html lang='es'>",
        "<head>",
        "<meta charset='UTF-8'>",
        "<style>",
        css_content,
        "</style>",
        "</head>",
        "<body>",
    ]

    for i, md_file in enumerate(md_files):
        print(f"  Procesando: {md_file.name}")
        body_html = md_to_html(md_file)
        # Envolver en div con page-break (excepto el primero)
        if i > 0:
            html_parts.append("<div class='page-break'></div>")
        html_parts.append(body_html)

    html_parts.extend(["</body>", "</html>"])
    return "\n".join(html_parts)

# ── Generar PDFs ──────────────────────────────────────────────

def build_full_pdf(html_content: str):
    """Genera el PDF completo con Chrome headless."""
    output = DIST / "06-NIVEL-EXPERTO.pdf"
    tmp_html = DIST / "_tmp_completa.html"
    tmp_html.write_text(html_content, encoding="utf-8")

    print(f"\nGenerando PDF completo con Chrome headless...")
    cmd = [
        CHROME,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-software-rasterizer",
        "--print-to-pdf=" + str(output),
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        str(tmp_html),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    tmp_html.unlink(missing_ok=True)
    size_kb = output.stat().st_size / 1024
    print(f"  ✓ {output.name} ({size_kb:.0f} KB)")

def build_resumen_pdf():
    """Genera el PDF resumen con wkhtmltopdf."""
    output = DIST / "GUIA-RESUMEN-06.pdf"

    print(f"\nGenerando PDF resumen con wkhtmltopdf...")
    cmd = [
        WKHTMLTOPDF,
        "--enable-local-file-access",
        "--encoding", "UTF-8",
        "--page-size", "A4",
        "--margin-top", "8mm",
        "--margin-bottom", "8mm",
        "--margin-left", "10mm",
        "--margin-right", "10mm",
        "--footer-center", "[page]",
        "--footer-font-size", "8",
        str(HTML_RESUMEN),
        str(output),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    size_kb = output.stat().st_size / 1024
    print(f"  ✓ {output.name} ({size_kb:.0f} KB)")

# ── Main ──────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  Generador de PDFs - Módulo 06: Nivel Experto")
    print("=" * 50)

    # Verificar dependencias
    for cmd, name in [(CHROME, "Google Chrome"), (WKHTMLTOPDF, "wkhtmltopdf")]:
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            print(f"\n✗ {name} no encontrado. Instálalo primero.")
            sys.exit(1)

    # 1. PDF completo
    print("\n[1/2] Construyendo HTML completo desde markdowns...")
    full_html = build_full_html()
    build_full_pdf(full_html)

    # 2. PDF resumen
    print("\n[2/2] Generando PDF resumen...")
    if not HTML_RESUMEN.exists():
        print(f"  ✗ {HTML_RESUMEN} no encontrado")
        sys.exit(1)
    build_resumen_pdf()

    print("\n" + "=" * 50)
    print("  ✓ PDFs generados en:", DIST)
    print("=" * 50)

if __name__ == "__main__":
    main()
