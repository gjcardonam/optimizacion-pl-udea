"""Regenera DOCUMENTO.pdf a partir de DOCUMENTO.md.

Uso:
    .venv/bin/python build_pdf.py
"""

from markdown_pdf import MarkdownPdf, Section

pdf = MarkdownPdf(toc_level=2)
with open("DOCUMENTO.md") as f:
    pdf.add_section(Section(f.read(), toc=False))

pdf.meta["title"] = "Trabajo Final — Programación Lineal"
pdf.meta["author"] = "Cardona, Tabares, Rodas"
pdf.meta["subject"] = "Optimización 2026-1 — UdeA"

pdf.save("DOCUMENTO.pdf")
print("✅ DOCUMENTO.pdf regenerado.")
