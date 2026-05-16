"""Método gráfico para problemas de PL con exactamente 2 variables.

Genera un matplotlib.Figure con:
  - Líneas de cada restricción.
  - Región factible (polígono sombreado).
  - Vértices y vértice óptimo.
  - Curva de nivel de Z que pasa por el óptimo (con flecha en dirección de optimización).
"""

from typing import List, Tuple, Optional
import itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon

from .problem import LPProblem, Constraint, ConstraintType, ObjectiveSense

TOL = 1e-9


def _line_points(a1: float, a2: float, b: float, xmax: float, ymax: float):
    """Dos puntos (x,y) sobre la recta a1·x + a2·y = b para graficar."""
    pts = []
    if abs(a2) > TOL:
        pts.append((0.0, b / a2))
        pts.append((xmax, (b - a1 * xmax) / a2))
    if abs(a1) > TOL:
        pts.append((b / a1, 0.0))
        pts.append(((b - a2 * ymax) / a1, ymax))
    return pts


def _feasible_vertices(problem: LPProblem) -> List[Tuple[float, float]]:
    """Calcula vértices de la región factible intersectando pares de restricciones (incluyendo ejes)."""
    n = problem.n_decision
    assert n == 2
    rows = []
    for c in problem.constraints:
        rows.append((c.coeffs[0], c.coeffs[1], c.rhs, c.ctype))
    # ejes x1=0 y x2=0
    rows.append((1.0, 0.0, 0.0, ConstraintType.GE))
    rows.append((0.0, 1.0, 0.0, ConstraintType.GE))

    vertices = []
    for (a1, b1, c1, _), (a2, b2, c2, _) in itertools.combinations(rows, 2):
        det = a1 * b2 - a2 * b1
        if abs(det) < TOL:
            continue
        x = (c1 * b2 - c2 * b1) / det
        y = (a1 * c2 - a2 * c1) / det
        if x < -TOL or y < -TOL:
            continue
        # validar contra todas las restricciones
        feasible = True
        for c in problem.constraints:
            lhs = c.coeffs[0] * x + c.coeffs[1] * y
            if c.ctype == ConstraintType.LE and lhs > c.rhs + 1e-6:
                feasible = False; break
            if c.ctype == ConstraintType.GE and lhs < c.rhs - 1e-6:
                feasible = False; break
            if c.ctype == ConstraintType.EQ and abs(lhs - c.rhs) > 1e-6:
                feasible = False; break
        if feasible:
            vertices.append((round(x, 8), round(y, 8)))
    # dedup
    return sorted(set(vertices))


def _sort_ccw(pts: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    if not pts:
        return pts
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return sorted(pts, key=lambda p: np.arctan2(p[1] - cy, p[0] - cx))


def plot_graphical(problem: LPProblem, optimum: Optional[Tuple[float, float, float]] = None):
    """Devuelve (Figure, info dict).

    optimum: tupla (x1_opt, x2_opt, z_opt) si se conoce; si no, se calcula sobre los vértices.
    """
    assert problem.n_decision == 2, "El método gráfico solo aplica a 2 variables."

    vertices = _feasible_vertices(problem)

    # Bounds del gráfico
    if vertices:
        xmax = max(2.0, max(p[0] for p in vertices) * 1.3 + 1)
        ymax = max(2.0, max(p[1] for p in vertices) * 1.3 + 1)
    else:
        xmax = ymax = 10.0

    fig, ax = plt.subplots(figsize=(8, 7))

    # Pintar región factible
    if vertices:
        ordered = _sort_ccw(vertices)
        poly = MplPolygon(ordered, alpha=0.25, facecolor="#1f77b4", edgecolor="#1f77b4", linewidth=2)
        ax.add_patch(poly)

    # Líneas de cada restricción
    colors = plt.get_cmap("tab10").colors
    for idx, c in enumerate(problem.constraints):
        a1, a2 = c.coeffs
        b = c.rhs
        pts = _line_points(a1, a2, b, xmax, ymax)
        if pts:
            pts = sorted(pts)
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            label = f"{a1:g}x₁ + {a2:g}x₂ {c.ctype.value} {b:g}"
            ax.plot(xs, ys, color=colors[idx % 10], linewidth=2, label=label)

    # Calcular óptimo sobre vértices si no se dio
    if optimum is None and vertices:
        best = None
        for x, y in vertices:
            z = problem.objective[0] * x + problem.objective[1] * y
            if best is None:
                best = (x, y, z)
            elif problem.sense == ObjectiveSense.MAX and z > best[2]:
                best = (x, y, z)
            elif problem.sense == ObjectiveSense.MIN and z < best[2]:
                best = (x, y, z)
        optimum = best

    # Plotear vértices
    if vertices:
        vx = [p[0] for p in vertices]
        vy = [p[1] for p in vertices]
        ax.scatter(vx, vy, color="#333", s=40, zorder=5)
        for x, y in vertices:
            ax.annotate(f"({x:g}, {y:g})", (x, y), textcoords="offset points",
                        xytext=(6, 6), fontsize=8, color="#333")

    # Curva de nivel de Z en el óptimo
    if optimum is not None:
        x_opt, y_opt, z_opt = optimum
        c1, c2 = problem.objective
        if abs(c1) > TOL or abs(c2) > TOL:
            pts = _line_points(c1, c2, z_opt, xmax, ymax)
            if pts:
                pts = sorted(pts)
                ax.plot([p[0] for p in pts], [p[1] for p in pts],
                        "--", color="#d62728", linewidth=2, label=f"Z = {z_opt:g} (óptimo)")
        ax.scatter([x_opt], [y_opt], color="#d62728", s=200, marker="*", zorder=6, label="Óptimo")

    ax.set_xlim(0, xmax)
    ax.set_ylim(0, ymax)
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.set_title("Método gráfico — Región factible y óptimo")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()

    info = {
        "vertices": vertices,
        "optimum": optimum,
    }
    return fig, info
