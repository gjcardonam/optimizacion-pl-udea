"""Simplex tabular básico con registro paso a paso.

Resuelve problemas en forma estándar provenientes de LPProblem.to_standard_form().
NO maneja artificiales (Gran M / Dos Fases vendrán en módulos aparte).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple
import numpy as np

from .problem import StandardForm, ObjectiveSense
from .tableau import Tableau

TOL = 1e-9


class SimplexStatus(str, Enum):
    OPTIMAL = "óptimo"
    UNBOUNDED = "no acotado"
    INFEASIBLE = "infactible"
    MAX_ITER = "máximo de iteraciones alcanzado"


@dataclass
class SimplexResult:
    status: SimplexStatus
    tableaux: List[Tableau] = field(default_factory=list)
    objective_value: float = 0.0       # en términos del problema ORIGINAL
    solution: dict = field(default_factory=dict)   # {var_name: valor}
    notes: List[str] = field(default_factory=list)
    multiple_optima: bool = False
    degenerate: bool = False


def _build_initial_tableau(sf: StandardForm) -> np.ndarray:
    """Construye la matriz inicial (m+1) x (n+1).

    Fila 0: [-c | 0]. Luego hacemos pivote para que las columnas básicas
    tengan z-row = 0. Como las básicas iniciales son holguras/artificiales
    con c=0, la z-row ya está bien (excepto si hubiera artificiales con -M,
    cosa que dejamos para Gran M).
    """
    m, n = sf.A.shape
    M = np.zeros((m + 1, n + 1))
    # z-row: queremos maximizar c·x  →  z - c·x = 0  →  coef en tablero = -c
    M[0, :n] = -sf.c
    M[0, n] = 0.0
    M[1:, :n] = sf.A
    M[1:, n] = sf.b
    return M


def solve_simplex(sf: StandardForm, max_iter: int = 50) -> SimplexResult:
    if sf.has_artificials:
        return SimplexResult(
            status=SimplexStatus.INFEASIBLE,
            notes=[
                "Este problema requiere variables artificiales (restricciones ≥ o =). "
                "Usá el método de la Gran M (módulo big_m.py, pendiente)."
            ],
        )

    M = _build_initial_tableau(sf)
    basis = list(sf.basis)
    tableaux: List[Tableau] = []
    notes: List[str] = []
    degenerate = False

    # Tablero inicial
    tableaux.append(
        Tableau(
            iteration=0,
            var_names=list(sf.var_names),
            basis=list(basis),
            matrix=M.copy(),
            note="Tablero inicial",
        )
    )

    for it in range(1, max_iter + 1):
        z_row = M[0, :-1]
        # Para MAX, óptimo cuando todos los z_j - c_j ≥ 0 → en nuestra
        # convención (coef = c_j - z_j en signo invertido), lo expresamos
        # buscando el MÁS NEGATIVO en z_row.
        j_in = int(np.argmin(z_row))
        if z_row[j_in] >= -TOL:
            # Óptimo
            status = SimplexStatus.OPTIMAL
            # Chequeo de soluciones múltiples: ¿hay z_j=0 para alguna no básica?
            non_basic = [j for j in range(sf.n_total) if j not in basis]
            for j in non_basic:
                if abs(M[0, j]) < TOL:
                    notes.append(
                        f"Hay soluciones óptimas múltiples (coef reducido = 0 en "
                        f"variable no básica {sf.var_names[j]})."
                    )
                    break
            return _finalize(sf, M, basis, tableaux, status, notes, degenerate,
                             multiple=any("múltiples" in n for n in notes))

        col = M[1:, j_in]
        if np.all(col <= TOL):
            tableaux.append(
                Tableau(
                    iteration=it,
                    var_names=list(sf.var_names),
                    basis=list(basis),
                    matrix=M.copy(),
                    pivot_col=j_in,
                    entering_var=sf.var_names[j_in],
                    note=f"Columna de {sf.var_names[j_in]} no tiene coeficientes positivos → solución NO ACOTADA.",
                )
            )
            return SimplexResult(
                status=SimplexStatus.UNBOUNDED,
                tableaux=tableaux,
                notes=notes + ["La región factible es no acotada en la dirección óptima."],
            )

        # Razón mínima (solo filas con coef positivo)
        with np.errstate(divide="ignore", invalid="ignore"):
            ratios = np.where(col > TOL, M[1:, -1] / np.where(col > TOL, col, 1), np.inf)
        i_out_rel = int(np.argmin(ratios))
        min_ratio = ratios[i_out_rel]
        # Detectar empates → degeneración
        ties = np.sum(np.isclose(ratios, min_ratio, atol=1e-9))
        if ties > 1:
            degenerate = True
            notes.append(
                f"Iter {it}: empate en razón mínima ({ties} filas) → degeneración. "
                "Se usa regla de Bland (índice menor)."
            )
            # Regla de Bland: menor índice de variable básica saliente
            candidates = [i for i, r in enumerate(ratios) if np.isclose(r, min_ratio, atol=1e-9)]
            i_out_rel = min(candidates, key=lambda i: basis[i])

        i_out = i_out_rel + 1  # fila en M (offset por z-row)

        entering_var = sf.var_names[j_in]
        leaving_var = sf.var_names[basis[i_out_rel]]

        # Pivoteo
        pivot = M[i_out, j_in]
        M[i_out, :] = M[i_out, :] / pivot
        for r in range(M.shape[0]):
            if r != i_out and abs(M[r, j_in]) > TOL:
                M[r, :] = M[r, :] - M[r, j_in] * M[i_out, :]

        # Actualizar base
        basis[i_out_rel] = j_in

        tableaux.append(
            Tableau(
                iteration=it,
                var_names=list(sf.var_names),
                basis=list(basis),
                matrix=M.copy(),
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


def _finalize(
    sf: StandardForm,
    M: np.ndarray,
    basis: List[int],
    tableaux: List[Tableau],
    status: SimplexStatus,
    notes: List[str],
    degenerate: bool,
    multiple: bool,
) -> SimplexResult:
    n_total = sf.n_total
    solution = {sf.var_names[j]: 0.0 for j in range(n_total)}
    for row, j in enumerate(basis):
        solution[sf.var_names[j]] = float(M[row + 1, -1])

    # Recuperar z en términos del problema original (max queda igual; min se negó)
    z_internal = M[0, -1]
    z_original = z_internal if sf.original_sense == ObjectiveSense.MAX else -z_internal

    return SimplexResult(
        status=status,
        tableaux=tableaux,
        objective_value=float(z_original),
        solution=solution,
        notes=notes,
        multiple_optima=multiple,
        degenerate=degenerate,
    )
