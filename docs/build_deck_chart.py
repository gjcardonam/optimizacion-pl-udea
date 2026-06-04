"""Genera la gráfica de Wyndor estilizada para las diapositivas (paleta del tema)."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon

# --- Paleta del tema de la exposición ---
INK      = "#16263d"   # azul marino tinta
INK_SOFT = "#5a6675"
PAPER    = "#f6f3ec"   # pergamino cálido
GARNET   = "#9c2b38"   # acento granate (óptimo)
TEAL     = "#2f7d77"   # secundario (región factible)
OCHRE    = "#b07d2b"
RULE     = "#cbbfa8"

ASSETS = Path(__file__).parent / "assets"
ASSETS.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 15,
    "axes.edgecolor": RULE,
    "axes.linewidth": 1.2,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK_SOFT,
    "ytick.color": INK_SOFT,
})

fig, ax = plt.subplots(figsize=(7.4, 6.9), dpi=200)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

xmax, ymax = 6.4, 8.3

# --- Región factible (pentágono) ---
vertices = [(0, 0), (4, 0), (4, 3), (2, 6), (0, 6)]
poly = MplPolygon(vertices, closed=True, facecolor=TEAL, alpha=0.13,
                  edgecolor=TEAL, linewidth=1.6, zorder=1)
ax.add_patch(poly)

xs = np.linspace(0, xmax, 200)

# Restricciones
# R1: x1 = 4  (vertical)
ax.plot([4, 4], [0, ymax], color=INK, linewidth=2.4, zorder=3,
        label=r"$x_1 \leq 4$  (Planta 1)")
# R2: x2 = 6  (horizontal)
ax.plot([0, xmax], [6, 6], color=TEAL, linewidth=2.4, zorder=3,
        label=r"$2x_2 \leq 12$  (Planta 2)")
# R3: 3x1 + 2x2 = 18  ->  x2 = (18 - 3x1)/2
ax.plot(xs, (18 - 3 * xs) / 2, color=OCHRE, linewidth=2.4, zorder=3,
        label=r"$3x_1 + 2x_2 \leq 18$  (Planta 3)")

# Recta de nivel del objetivo en el optimo: 3x1 + 5x2 = 36 -> x2 = (36 - 3x1)/5
ax.plot(xs, (36 - 3 * xs) / 5, color=GARNET, linewidth=2.2, linestyle=(0, (6, 4)),
        zorder=4, label=r"$Z = 3x_1 + 5x_2 = 36$")

# --- Vertices ---
vertex_offsets = {(0, 0): (10, 8), (4, 0): (10, 8), (4, 3): (12, 4),
                  (2, 6): (-58, 10), (0, 6): (8, 9)}
for (vx, vy) in vertices:
    ax.scatter([vx], [vy], s=46, color=INK, zorder=5, edgecolor=PAPER, linewidth=1.2)
    off = vertex_offsets.get((vx, vy), (8, 7))
    ax.annotate(f"({vx:g}, {vy:g})", (vx, vy), textcoords="offset points",
                xytext=off, fontsize=12, color=INK_SOFT)

# --- Optimo ---
ax.scatter([2], [6], s=420, marker="*", color=GARNET, zorder=7,
           edgecolor=PAPER, linewidth=1.4)
ax.annotate("Óptimo  Z* = 36", (2, 6), textcoords="offset points",
            xytext=(20, -36), fontsize=14, fontweight="bold", color=GARNET)

ax.set_xlim(-0.25, xmax)
ax.set_ylim(-0.25, ymax)
ax.set_xlabel(r"$x_1$  (lotes de puertas)", fontsize=14)
ax.set_ylabel(r"$x_2$  (lotes de ventanas)", fontsize=14)
ax.set_xticks(range(0, 7))
ax.set_yticks(range(0, 9))
ax.grid(True, color=RULE, alpha=0.4, linewidth=0.8)

for spine in ("top", "right"):
    ax.spines[spine].set_visible(False)

leg = ax.legend(loc="upper right", fontsize=11.5, frameon=True, framealpha=0.95,
                edgecolor=RULE, facecolor="white", borderpad=0.8, labelspacing=0.6)
leg.get_frame().set_linewidth(1.0)

fig.tight_layout(pad=0.6)
out = ASSETS / "grafico_wyndor_deck.png"
fig.savefig(out, facecolor=PAPER, bbox_inches="tight", pad_inches=0.15)
print(f"Guardado: {out}")
