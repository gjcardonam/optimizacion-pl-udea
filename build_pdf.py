"""Genera DOCUMENTO.pdf desde DOCUMENTO.md con estilo CSS y todas las imágenes.

Uso:
    .venv/bin/python build_pdf.py
"""

from pathlib import Path
from markdown_pdf import MarkdownPdf, Section

ROOT = Path(__file__).parent
md_path = ROOT / "DOCUMENTO.md"
css_path = ROOT / "docs" / "style.css"
pdf_path = ROOT / "DOCUMENTO.pdf"

css = css_path.read_text()
content = md_path.read_text()

pdf = MarkdownPdf(toc_level=0)  # sin TOC para mantener el formato limpio
pdf.add_section(Section(content, toc=False, root=str(ROOT)), user_css=css)

pdf.meta["title"] = "Trabajo Final — Programación Lineal"
pdf.meta["author"] = "Cardona, Tabares"
pdf.meta["subject"] = "Optimización 2026-1 — UdeA"
pdf.meta["keywords"] = "PL, Simplex, Gran M, sensibilidad, UdeA"

pdf.save(pdf_path)
print(f"✅ {pdf_path.name} regenerado.")
