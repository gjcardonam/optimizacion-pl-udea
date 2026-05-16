"""Método de la Gran M.

Penaliza variables artificiales con un valor M muy grande en la función objetivo.
Compatible con MAX/MIN y restricciones ≤, ≥, =.

Detecta infactibilidad si alguna artificial queda > 0 en la solución óptima.
"""

from dataclasses import dataclass
from typing import List
import numpy as np

from .problem import StandardForm, ObjectiveSense
from .tableau import Tableau
from .simplex import SimplexResult, SimplexStatus, TOL

BIG_M = 1e6


def solve_big_m(sf: StandardForm, M_value: float = BIG_M, max_iter: int = 100) -> SimplexResult:
    """Resuelve el problema usando Gran M.

    Convención: trabajamos internamente como MAX. Para artificiales c = -M.
    """
    m, n = sf.A.shape

    # Vector c con penalización -M para artificiales
    c = sf.c.copy()
    for j, kind in enumerate(sf.aux_kinds):
        if kind == "a":
            c[j] = -M_value

    # Tablero inicial
    T = np.zeros((m + 1, n + 1))
    T[0, :n] = -c
    T[1:, :n] = sf.A
    T[1:, n] = sf.b

    basis = list(sf.basis)

    # Limpiar z-row para variables artificiales en base
    # (deben tener coeficiente 0 en z-row)
    for i, j_b in enumerate(basis):
        if sf.aux_kinds[j_b] == "a":
            T[0, :] -= T[0, j_b] * T[i + 1, :] / T[i + 1, j_b] if T[i + 1, j_b] != 0 else 0
            # Más simple y correcto: como col j_b es e_i (unitario con 1 en fila i+1),
            # basta restar T[0,j_b] * row(i+1).
    # Recalculamos limpio (más seguro): para cada artificial básico, hacer z-row[j_b] = 0
    T = np.zeros((m + 1, n + 1))
    T[0, :n] = -c
    T[1:, :n] = sf.A
    T[1:, n] = sf.b
    for i, j_b in enumerate(basis):
        if sf.aux_kinds[j_b] == "a" and abs(T[0, j_b]) > TOL:
            T[0, :] -= T[0, j_b] * T[i + 1, :]

    tableaux: List[Tableau] = []
    notes: List[str] = []
    degenerate = False
    multiple = False

    tableaux.append(
        Tableau(
            iteration=0,
            var_names=list(sf.var_names),
            basis=list(basis),
            matrix=T.copy(),
            note=f"Tablero inicial (Gran M, M={M_value:g}). Artificiales penalizadas en z-row.",
        )
    )

    for it in range(1, max_iter + 1):
        z_row = T[0, :-1]
        j_in = int(np.argmin(z_row))
        if z_row[j_in] >= -TOL * max(1, M_value):
            # Óptimo (con tolerancia escalada por M para evitar ruido numérico)
            # Verificar infactibilidad: artificiales con valor > 0
            infeasible = False
            for i, j_b in enumerate(basis):
                if sf.aux_kinds[j_b] == "a" and T[i + 1, -1] > TOL * max(1, M_value):
                    infeasible = True
                    break
            if infeasible:
                return SimplexResult(
                    status=SimplexStatus.INFEASIBLE,
                    tableaux=tableaux,
                    notes=notes + [
                        "Solución INFACTIBLE: hay variables artificiales con valor > 0 "
                        "en el óptimo, lo que significa que el sistema original no tiene solución."
                    ],
                )
            # Multiple optima
            non_basic = [j for j in range(sf.n_total) if j not in basis]
            for j in non_basic:
                if sf.aux_kinds[j] == "a":
                    continue
                if abs(T[0, j]) < TOL * max(1, M_value):
                    multiple = True
                    notes.append(
                        f"Soluciones óptimas múltiples (coef reducido = 0 en {sf.var_names[j]})."
                    )
                    break
            return _finalize_big_m(sf, T, basis, tableaux, notes, degenerate, multiple)

        col = T[1:, j_in]
        if np.all(col <= TOL):
            tableaux.append(
                Tableau(
                    iteration=it,
                    var_names=list(sf.var_names),
                    basis=list(basis),
                    matrix=T.copy(),
                    pivot_col=j_in,
                    entering_var=sf.var_names[j_in],
                    note=f"Columna de {sf.var_names[j_in]} sin coef. positivos → NO ACOTADO.",
                )
            )
            return SimplexResult(
                status=SimplexStatus.UNBOUNDED,
                tableaux=tableaux,
                notes=notes + ["Solución no acotada."],
            )

        with np.errstate(divide="ignore", invalid="ignore"):
            ratios = np.where(col > TOL, T[1:, -1] / np.where(col > TOL, col, 1), np.inf)
        min_ratio = float(np.min(ratios))
        candidates = [i for i, r in enumerate(ratios) if np.isclose(r, min_ratio, atol=1e-9)]
        if len(candidates) > 1:
            degenerate = True
            notes.append(f"Iter {it}: empate en razón mínima → regla de Bland.")
        # Bland: menor índice de variable básica saliente
        i_out_rel = min(candidates, key=lambda i: basis[i])
        i_out = i_out_rel + 1

        entering_var = sf.var_names[j_in]
        leaving_var = sf.var_names[basis[i_out_rel]]

        pivot = T[i_out, j_in]
        T[i_out, :] = T[i_out, :] / pivot
        for r in range(T.shape[0]):
            if r != i_out and abs(T[r, j_in]) > TOL:
                T[r, :] = T[r, :] - T[r, j_in] * T[i_out, :]

        basis[i_out_rel] = j_in

        tableaux.append(
            Tableau(
                iteration=it,
                var_names=list(sf.var_names),
                basis=list(basis),
                matrix=T.copy(),
                pivot_row=i_out,
                pivot_col=j_in,
                entering_var=entering_var,
                leaving_var=leaving_var,
                note=f"Entra {entering_var}, sale {leaving_var}. Pivote = {pivot:.4f}.",
            )
        )

    return SimplexResult(
        status=SimplexStatus.MAX_ITER,
        tableaux=tableaux,
        notes=notes + [f"Se alcanzaron {max_iter} iteraciones sin convergencia."],
    )


def _finalize_big_m(sf, T, basis, tableaux, notes, degenerate, multiple):
    solution = {sf.var_names[j]: 0.0 for j in range(sf.n_total)}
    for row, j in enumerate(basis):
        solution[sf.var_names[j]] = float(T[row + 1, -1])
    z_internal = T[0, -1]
    z_original = z_internal if sf.original_sense == ObjectiveSense.MAX else -z_internal
    return SimplexResult(
        status=SimplexStatus.OPTIMAL,
        tableaux=tableaux,
        objective_value=float(z_original),
        solution=solution,
        notes=notes,
        multiple_optima=multiple,
        degenerate=degenerate,
    )
