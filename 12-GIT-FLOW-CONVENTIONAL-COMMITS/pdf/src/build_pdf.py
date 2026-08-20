#!/usr/bin/env python3
"""
Build PDF guides for Module 12 - Git Flow + Conventional Commits + SemVer.
Generates two PDFs:
  1. Full guide (guia-completa.html → Chrome headless → PDF)
  2. Summary guide (guia-resumen.html → wkhtmltopdf → PDF)
"""

import os
import subprocess
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "dist")
MODULE_DIR = os.path.dirname(SCRIPT_DIR)  # Module root

# ── PARTS ────────────────────────────────────────────────────────────────────
# Each part maps: (part_label, source_file)
# The full guide HTML is assembled by pandoc from all parts,
# but since we have a single HTML (guia-completa.html), we just
# convert it directly.

# ── Output files ──────────────────────────────────────────────────────────────
FULL_PDF = os.path.join(OUTPUT_DIR, "12-GIT-FLOW-CONVENTIONAL-COMMITS.pdf")
SUMMARY_PDF = os.path.join(OUTPUT_DIR, "GUIA-RESUMEN-12-GIT-FLOW-CONVENTIONAL-COMMITS.pdf")

# Source HTML files
FULL_HTML = os.path.join(SCRIPT_DIR, "guia-completa.html")
SUMMARY_HTML = os.path.join(SCRIPT_DIR, "guia-resumen.html")


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"[✓] Output dir: {OUTPUT_DIR}")


def build_full_pdf():
    """Build the full guide PDF using Chrome headless (print-to-pdf)."""
    print("\n[1/2] Building FULL guide PDF...")

    # Chrome headless command
    chrome_cmd = [
        "google-chrome-stable",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--print-to-pdf=" + FULL_PDF,
        "--print-to-pdf-no-header",
        "--no-pdf-header-footer",
        FULL_HTML,
    ]

    try:
        subprocess.run(chrome_cmd, check=True, capture_output=True, text=True)
        print(f"  [✓] Generated: {os.path.basename(FULL_PDF)}")
        print(f"      Size: {os.path.getsize(FULL_PDF) / 1024:.1f} KB")
    except FileNotFoundError:
        print("  [✗] Chrome not found. Trying alternative...")
        # Fallback: use chromium-browser
        chrome_cmd[0] = "chromium-browser"
        try:
            subprocess.run(chrome_cmd, check=True, capture_output=True, text=True)
            print(f"  [✓] Generated: {os.path.basename(FULL_PDF)}")
            print(f"      Size: {os.path.getsize(FULL_PDF) / 1024:.1f} KB")
        except FileNotFoundError:
            print("  [✗] Neither google-chrome nor chromium found!")
            print("      Install Chrome or Chromium to generate PDFs.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"  [✗] Chrome error: {e.stderr}")
        return False

    return True


def build_summary_pdf():
    """Build the summary PDF using wkhtmltopdf."""
    print("\n[2/2] Building SUMMARY guide PDF...")

    cmd = [
        "wkhtmltopdf",
        "--enable-local-file-access",
        "--page-size", "A4",
        "--margin-top", "15mm",
        "--margin-bottom", "15mm",
        "--margin-left", "15mm",
        "--margin-right", "15mm",
        "--encoding", "utf-8",
        SUMMARY_HTML,
        SUMMARY_PDF,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"  [✓] Generated: {os.path.basename(SUMMARY_PDF)}")
        print(f"      Size: {os.path.getsize(SUMMARY_PDF) / 1024:.1f} KB")
    except FileNotFoundError:
        print("  [✗] wkhtmltopdf not found!")
        print("      Install: sudo apt install wkhtmltopdf")
        return False
    except subprocess.CalledProcessError as e:
        print(f"  [✗] wkhtmltopdf error: {e.stderr}")
        return False

    return True


def copy_to_module_root():
    """Copy generated PDFs from dist/ to module root."""
    print("\n[3/3] Copying PDFs to module root...")
    copied = 0

    for src in [FULL_PDF, SUMMARY_PDF]:
        if os.path.exists(src):
            dst = os.path.join(MODULE_DIR, os.path.basename(src))
            shutil.copy2(src, dst)
            print(f"  [✓] {os.path.basename(src)} → {MODULE_DIR}/")
            copied += 1
        else:
            print(f"  [!] Skipped: {os.path.basename(src)} (not found)")

    return copied > 0


def main():
    print("=" * 60)
    print("  Module 12 — Git Flow + Conventional Commits + SemVer")
    print("  PDF Builder")
    print("=" * 60)

    ensure_output_dir()

    full_ok = build_full_pdf()
    summary_ok = build_summary_pdf()

    if full_ok or summary_ok:
        copy_to_module_root()

    print("\n" + "=" * 60)
    if full_ok and summary_ok:
        print("  ✓ Both PDFs generated successfully!")
    elif full_ok:
        print("  ⚠ Full PDF generated. Summary PDF failed.")
    elif summary_ok:
        print("  ⚠ Summary PDF generated. Full PDF failed.")
    else:
        print("  ✗ PDF generation failed. Check dependencies.")
        sys.exit(1)

    print("=" * 60)


if __name__ == "__main__":
    main()
