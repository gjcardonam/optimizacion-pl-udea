"""Simplex Revisado (forma matricial).

Mismo resultado que el Simplex tabular pero expresado con B, B⁻¹ y operaciones de matriz.
Útil para problemas grandes (solo se invierte cuando cambia la base) y didácticamente
muestra el origen de los precios sombra (y = c_B · B⁻¹).

Limitación: este módulo NO maneja artificiales. Para problemas con ≥ o = usar Gran M.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import numpy as np

from .problem import StandardForm, ObjectiveSense
from .simplex import SimplexStatus, SimplexResult, TOL


@dataclass
class RevisedStep:
    iteration: int
    basis_names: List[str]
    B: np.ndarray
    B_inv: np.ndarray
    cB: np.ndarray
    xB: np.ndarray              # = B⁻¹·b
    y: np.ndarray               # = c_B · B⁻¹  (precios sombra/duales)
    reduced_costs: Dict[str, float]
    entering: str = ""
    leaving: str = ""
    note: str = ""


@dataclass
class RevisedResult:
    status: SimplexStatus
    steps: List[RevisedStep] = field(default_factory=list)
    objective_value: float = 0.0
    solution: Dict[str, float] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)


def solve_revised(sf: StandardForm, max_iter: int = 50) -> RevisedResult:
    if sf.has_artificials:
        return RevisedResult(
            status=SimplexStatus.INFEASIBLE,
            notes=["Este módulo no maneja artificiales. Usá Gran M para problemas con ≥ o =."],
        )

    A = sf.A
    b = sf.b.astype(float)
    c = sf.c.astype(float)
    m, n_total = A.shape
    basis = list(sf.basis)
    steps: List[RevisedStep] = []

    for it in range(max_iter + 1):
        B = A[:, basis]
        try:
            B_inv = np.linalg.inv(B)
        except np.linalg.LinAlgError:
            return RevisedResult(
                status=SimplexStatus.INFEASIBLE,
                steps=steps,
                notes=["B singular."],
            )
        cB = c[basis]
        xB = B_inv @ b
        y = cB @ B_inv  # vector dual

        # Costos reducidos para no básicas (en convención max: rj = cj - y·Aj)
        reduced = {}
        best_j = -1
        best_rc = 0.0
        for j in range(n_total):
            if j in basis:
                reduced[sf.var_names[j]] = 0.0
                continue
            rj = c[j] - y @ A[:, j]
            reduced[sf.var_names[j]] = float(rj)
            if rj > best_rc + TOL:
                best_rc = rj
                best_j = j

        step = RevisedStep(
            iteration=it,
            basis_names=[sf.var_names[j] for j in basis],
            B=B.copy(),
            B_inv=B_inv.copy(),
            cB=cB.copy(),
            xB=xB.copy(),
            y=y.copy(),
            reduced_costs=reduced,
            note="Tablero inicial" if it == 0 else "",
        )

        if best_j == -1:
            steps.append(step)
            step.note = "Óptimo (todos los costos reducidos ≤ 0 en MAX interno)."
            return _finalize_revised(sf, steps, basis, xB, c)

        # Dirección
        d = B_inv @ A[:, best_j]
        if np.all(d <= TOL):
            step.entering = sf.var_names[best_j]
            step.note = f"Columna {sf.var_names[best_j]} sin coef positivos → NO ACOTADO."
            steps.append(step)
            return RevisedResult(status=SimplexStatus.UNBOUNDED, steps=steps,
                                 notes=["Solución no acotada."])

        with np.errstate(divide="ignore", invalid="ignore"):
            ratios = np.where(d > TOL, xB / np.where(d > TOL, d, 1), np.inf)
        min_ratio = float(np.min(ratios))
        candidates = [i for i, r in enumerate(ratios) if np.isclose(r, min_ratio, atol=1e-9)]
        i_out = min(candidates, key=lambda i: basis[i])

        step.entering = sf.var_names[best_j]
        step.leaving = sf.var_names[basis[i_out]]
        step.note = f"Entra {step.entering}, sale {step.leaving}. θ* = {min_ratio:.4f}."
        steps.append(step)

        basis[i_out] = best_j

    return RevisedResult(
        status=SimplexStatus.MAX_ITER,
        steps=steps,
        notes=[f"Máximo {max_iter} iteraciones."],
    )


def _finalize_revised(sf, steps, basis, xB, c):
    solution = {sf.var_names[j]: 0.0 for j in range(sf.n_total)}
    for row, j in enumerate(basis):
        solution[sf.var_names[j]] = float(xB[row])
    z_internal = float(c[basis] @ xB)
    z_original = z_internal if sf.original_sense == ObjectiveSense.MAX else -z_internal
    return RevisedResult(
        status=SimplexStatus.OPTIMAL,
        steps=steps,
        objective_value=z_original,
        solution=solution,
    )
