"""Genera todas las imágenes que se empotran en DOCUMENTO.md."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

from solver import (
    LPProblem, Constraint, ConstraintType, ObjectiveSense,
    solve_simplex, solve_big_m, solve_revised,
    analyze_sensitivity, plot_graphical,
)

ASSETS = Path(__file__).parent / "assets"
ASSETS.mkdir(exist_ok=True)


def save_dataframe_as_image(df, path, title="", highlight=None, figsize=None):
    """Renderiza un DataFrame como imagen estilo tablero Simplex."""
    nrows, ncols = df.shape
    if figsize is None:
        figsize = (max(6, 1.1 * (ncols + 1)), max(2, 0.5 * (nrows + 2)))
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=11, fontweight="bold", pad=10)

    cell_text = [[str(v) for v in row] for row in df.values]
    col_labels = list(df.columns)
    row_labels = list(df.index)

    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        rowLabels=row_labels,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.0, 1.5)

    # Encabezados (z-row y col-row)
    for j in range(ncols):
        cell = table[0, j]
        cell.set_facecolor("#1f3a5f")
        cell.set_text_props(color="white", fontweight="bold")
    for i in range(nrows):
        cell = table[i + 1, -1]
        cell.set_facecolor("#e7eef7")
        cell.set_text_props(fontweight="bold")
    # Highlight pivote si se pidió
    if highlight:
        i_row, j_col = highlight  # 1-indexed in df (incluye header conceptual)
        for j in range(ncols):
            try:
                cell = table[i_row, j]
                cell.set_facecolor("#fff3cd")
            except KeyError:
                pass
        for i in range(nrows + 1):
            try:
                cell = table[i, j_col]
                cell.set_facecolor("#fff3cd")
            except KeyError:
                pass
        try:
            pivot_cell = table[i_row, j_col]
            pivot_cell.set_facecolor("#ffc107")
            pivot_cell.set_text_props(fontweight="bold")
        except KeyError:
            pass

    fig.tight_layout()
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def build_wyndor():
    return LPProblem(
        sense=ObjectiveSense.MAX,
        objective=[3, 5],
        constraints=[
            Constraint([1, 0], ConstraintType.LE, 4),
            Constraint([0, 2], ConstraintType.LE, 12),
            Constraint([3, 2], ConstraintType.LE, 18),
        ],
    )


def main():
    print("Generando imágenes…")
    wyn = build_wyndor()
    sf = wyn.to_standard_form()
    r = solve_simplex(sf)

    # 1) Método gráfico
    fig, info = plot_graphical(wyn, optimum=(r.solution["x1"], r.solution["x2"], r.objective_value))
    fig.savefig(ASSETS / "grafico_wyndor.png", dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(" ✓ grafico_wyndor.png")

    # 2) Tableros: inicial, intermedio, óptimo
    save_dataframe_as_image(
        r.tableaux[0].to_dataframe(),
        ASSETS / "tablero_inicial.png",
        title="Tablero inicial — Wyndor Glass",
    )
    print(" ✓ tablero_inicial.png")

    t1 = r.tableaux[1]
    save_dataframe_as_image(
        t1.to_dataframe(),
        ASSETS / "tablero_iter1.png",
        title=f"Iteración 1 — Entra {t1.entering_var}, sale {t1.leaving_var}",
    )
    print(" ✓ tablero_iter1.png")

    tf = r.tableaux[-1]
    save_dataframe_as_image(
        tf.to_dataframe(),
        ASSETS / "tablero_optimo.png",
        title=f"Tablero óptimo — Z* = {r.objective_value}, x* = ({r.solution['x1']}, {r.solution['x2']})",
    )
    print(" ✓ tablero_optimo.png")

    # 3) Análisis de sensibilidad
    rep = analyze_sensitivity(sf, r, constraint_names=["Planta 1", "Planta 2", "Planta 3"])
    shadow_df, reduced_df = rep.to_dataframes()
    save_dataframe_as_image(
        shadow_df.set_index("Restricción"),
        ASSETS / "sensibilidad_b.png",
        title="Precios sombra y rangos de RHS (b)",
        figsize=(7.5, 2.2),
    )
    print(" ✓ sensibilidad_b.png")
    save_dataframe_as_image(
        reduced_df.set_index("Variable"),
        ASSETS / "sensibilidad_c.png",
        title="Costos reducidos y rangos de c",
        figsize=(7.5, 1.8),
    )
    print(" ✓ sensibilidad_c.png")

    # 4) Simplex Revisado (mostrar matrices del óptimo)
    rev = solve_revised(sf)
    final = rev.steps[-1]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3))
    for ax, mat, title in zip(
        axes,
        [final.B, final.B_inv, final.y.reshape(1, -1)],
        ["B (base óptima)", "B⁻¹", "y = c_B · B⁻¹  (precios sombra)"],
    ):
        ax.axis("off")
        ax.set_title(title, fontsize=10, fontweight="bold")
        table = ax.table(
            cellText=[[f"{v:.3f}" for v in row] for row in mat],
            cellLoc="center", loc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.0, 1.6)
    fig.tight_layout()
    fig.savefig(ASSETS / "revisado_optimo.png", dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(" ✓ revisado_optimo.png")

    # 5) Diagrama de arquitectura simple
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    def box(x, y, w, h, text, color="#e7eef7"):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="#1f3a5f", linewidth=1.5))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=9, fontweight="bold")
    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#1f3a5f", lw=1.4))

    box(0.5, 4, 3, 1.2, "Usuario\n(navegador)", "#fff3cd")
    box(4.5, 4, 3, 1.2, "UI Streamlit\n(app.py)", "#cfe0f0")
    box(8.5, 4, 3, 1.2, "Módulo solver/\n(numpy + lógica)", "#cfe0f0")
    box(0.5, 1.5, 11, 1.5,
        "solver/  ·  problem.py · simplex.py · big_m.py · revised.py · graphical.py · sensitivity.py · tableau.py",
        "#e7eef7")

    arrow(3.5, 4.6, 4.5, 4.6)
    arrow(7.5, 4.6, 8.5, 4.6)
    arrow(10, 4, 10, 3)
    fig.savefig(ASSETS / "arquitectura.png", dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(" ✓ arquitectura.png")

    # 6) Vista esquemática de la UI (mockup, no screenshot real)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
    # Sidebar
    ax.add_patch(Rectangle((0, 0), 3, 8, facecolor="#f0f2f6", edgecolor="#bbb"))
    ax.text(1.5, 7.5, "DEFINICIÓN DEL\nPROBLEMA", ha="center", fontsize=8, fontweight="bold")
    ax.text(1.5, 6.6, "Objetivo: MAX/MIN", ha="center", fontsize=7)
    ax.text(1.5, 6.1, "n variables", ha="center", fontsize=7)
    ax.text(1.5, 5.6, "n restricciones", ha="center", fontsize=7)
    ax.text(1.5, 4.7, "Cargar ejemplo:", ha="center", fontsize=7)
    ax.add_patch(Rectangle((0.4, 4.0), 2.2, 0.4, facecolor="white", edgecolor="#999"))
    ax.text(1.5, 4.2, "Wyndor Glass ▾", ha="center", fontsize=7)
    # Main area: tabs
    ax.add_patch(Rectangle((3.2, 7), 8.6, 0.6, facecolor="#1f3a5f"))
    ax.text(3.4, 7.3, "Tableros  |  Gráfico  |  Sensibilidad  |  Simplex Revisado",
            color="white", fontsize=8, va="center")
    # Result card
    ax.add_patch(Rectangle((3.4, 5.5), 4, 1.2, facecolor="#d4edda", edgecolor="#28a745", linewidth=1.5))
    ax.text(5.4, 6.4, "Z* = 36.0000", ha="center", fontsize=12, fontweight="bold", color="#155724")
    ax.text(5.4, 5.9, "x₁ = 2.0   x₂ = 6.0", ha="center", fontsize=10, color="#155724")
    # Tableau preview
    ax.add_patch(Rectangle((7.6, 5.5), 4, 1.2, facecolor="white", edgecolor="#bbb"))
    ax.text(9.6, 6.4, "Iteración 0", ha="center", fontsize=9, fontweight="bold")
    ax.text(9.6, 6.0, "[ Tablero inicial ]", ha="center", fontsize=8)
    ax.text(9.6, 5.7, "[ Tablero iter 1 ]", ha="center", fontsize=8)
    # Big tableau area
    ax.add_patch(Rectangle((3.4, 2), 8.2, 3.2, facecolor="white", edgecolor="#bbb"))
    ax.text(7.5, 4.9, "Tablero — Iteración 2", ha="center", fontsize=10, fontweight="bold")
    # mock cells con valores reales del óptimo de Wyndor
    rows_mock = [
        ("z",  ["0.0", "0.0", "0.0",  "1.5", "1.0",  "36.0"]),
        ("s1", ["0.0", "0.0", "1.0",  "0.33", "-0.33", "2.0"]),
        ("x2", ["0.0", "1.0", "0.0",  "0.5",  "0.0",   "6.0"]),
        ("x1", ["1.0", "0.0", "0.0",  "-0.33", "0.33", "2.0"]),
    ]
    for i, (label, vals) in enumerate(rows_mock):
        ax.text(3.7, 4.4 - 0.5 * i, label, fontsize=8, fontweight="bold")
        for j, val in enumerate(vals):
            ax.text(4.5 + 1.2 * j, 4.4 - 0.5 * i, val, fontsize=8, ha="center")
    for j, label in enumerate(["x1", "x2", "s1", "s2", "s3", "RHS"]):
        ax.text(4.5 + 1.2 * j, 4.7, label, fontsize=7, ha="center", color="#666", fontweight="bold")

    ax.set_title("UI del solver — vista esquemática", fontsize=11, fontweight="bold")
    fig.savefig(ASSETS / "ui_mockup.png", dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(" ✓ ui_mockup.png")

    print("\n✅ Todas las imágenes generadas en docs/assets/")


if __name__ == "__main__":
    main()
