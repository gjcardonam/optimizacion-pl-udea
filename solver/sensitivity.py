"""Análisis de sensibilidad post-óptimo.

Calcula:
  - Precios sombra (dual values) por restricción.
  - Costos reducidos por variable.
  - Rangos de cambio en coeficientes de la función objetivo (Δc_j).
  - Rangos de cambio en lado derecho (Δb_i).

Trabaja sobre el tablero final retornado por simplex / big_m.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import numpy as np
import pandas as pd

from .problem import StandardForm, ObjectiveSense
from .simplex import SimplexResult, SimplexStatus, TOL


@dataclass
class SensitivityReport:
    shadow_prices: List[float] = field(default_factory=list)        # por restricción
    constraint_names: List[str] = field(default_factory=list)
    reduced_costs: Dict[str, float] = field(default_factory=dict)
    obj_ranges: Dict[str, Tuple[float, float]] = field(default_factory=dict)  # c_j → (min, max)
    rhs_ranges: Dict[str, Tuple[float, float]] = field(default_factory=dict)  # b_i → (min, max)
    notes: List[str] = field(default_factory=list)

    def to_dataframes(self):
        shadow_df = pd.DataFrame({
            "Restricción": self.constraint_names,
            "Precio sombra": [round(s, 4) for s in self.shadow_prices],
            "b mín": [round(self.rhs_ranges.get(n, (None, None))[0] or 0, 4) for n in self.constraint_names],
            "b máx": [round(self.rhs_ranges.get(n, (None, None))[1] or 0, 4) for n in self.constraint_names],
        })
        reduced_df = pd.DataFrame({
            "Variable": list(self.reduced_costs.keys()),
            "Costo reducido": [round(v, 4) for v in self.reduced_costs.values()],
            "c mín": [round(self.obj_ranges.get(k, (None, None))[0] or 0, 4) for k in self.reduced_costs.keys()],
            "c máx": [round(self.obj_ranges.get(k, (None, None))[1] or 0, 4) for k in self.reduced_costs.keys()],
        })
        return shadow_df, reduced_df


def analyze_sensitivity(
    sf: StandardForm,
    result: SimplexResult,
    constraint_names: Optional[List[str]] = None,
) -> SensitivityReport:
    """Calcula el reporte de sensibilidad desde el tablero óptimo."""
    if result.status != SimplexStatus.OPTIMAL:
        return SensitivityReport(notes=[f"No hay análisis: status={result.status.value}."])

    final = result.tableaux[-1]
    T = final.matrix
    basis = final.basis
    m = sf.m
    n = sf.n_decision
    n_total = sf.n_total

    sign = 1.0 if sf.original_sense == ObjectiveSense.MAX else -1.0
    sense_factor = sign  # convertir z-row interna a la convención del problema original

    # === Precios sombra ===
    # En el tablero final, la coef. de la holgura s_i en z-row es el precio sombra
    # (con signo según convención). Para restricciones que no tienen holgura natural
    # (≥ o =), tomamos la coef. del eje canónico equivalente vía artificial o exceso.
    shadow = [0.0] * m
    s_indices = {}   # fila → índice de columna asociada en sf.var_names
    for j, kind in enumerate(sf.aux_kinds):
        if kind == "s":
            # ¿en qué fila tenía el 1 inicialmente? La fila donde sf.A inicial tenía 1 en j.
            # sf.A está intacto; columna j es la holgura insertada para alguna fila.
            # La fila i tal que sf.A[i,j]=1 originalmente.
            for i in range(m):
                if abs(sf.A[i, j] - 1.0) < TOL and np.allclose(np.delete(sf.A[:, j], i), 0, atol=TOL):
                    s_indices[i] = j
                    break

    # Para restricciones ≥ y =, el dual viene de la coef. de la artificial en z-row,
    # corregida por M.
    for i in range(m):
        if i in s_indices:
            shadow[i] = float(T[0, s_indices[i]] * sense_factor)
        else:
            # buscar columna artificial para esa fila
            for j, kind in enumerate(sf.aux_kinds):
                if kind == "a" and abs(sf.A[i, j] - 1.0) < TOL and np.allclose(np.delete(sf.A[:, j], i), 0, atol=TOL):
                    # coef artificial en z-row final = M + y_i  (en convención interna max)
                    # → y_i = coef - M  (no robusto numéricamente, dejar como n/a si M grande domina)
                    coef = T[0, j]
                    # Si el problema tiene exceso para esta fila, mejor usar exceso (-e)
                    e_col = None
                    for je, ke in enumerate(sf.aux_kinds):
                        if ke == "e" and abs(sf.A[i, je] + 1.0) < TOL:
                            e_col = je
                            break
                    if e_col is not None:
                        shadow[i] = float(-T[0, e_col] * sense_factor)
                    else:
                        shadow[i] = float(coef * sense_factor)  # aprox.
                    break

    names = constraint_names or [f"R{i+1}" for i in range(m)]

    # === Costos reducidos ===
    reduced = {}
    for j in range(n):
        name = sf.var_names[j]
        if j in basis:
            reduced[name] = 0.0
        else:
            # En convención interna: coef z-row = z_j - c_j (≥0 para óptimo en max)
            reduced[name] = float(T[0, j] * sense_factor)

    # === Rangos para coeficientes objetivo ===
    # Para variables NO BÁSICAS: el rango es c_j ∈ (-∞, c_j + Δ_max], donde Δ_max es
    # cuanto puede subir el coef antes de que entre en la base. Como en convención max,
    # entra si z_j - c_j < 0, es decir c_j > z_j. El máximo es z_j.
    # → c_j puede ir hasta el valor que hace reducido = 0 (es decir hasta c_j + reduced[j]).
    obj_ranges = {}
    for j in range(n):
        name = sf.var_names[j]
        original_c = sf.c[j] * sign  # c original en problema (max o min)
        if j not in basis:
            delta_up = T[0, j] * sense_factor   # cuánto puede aumentar c_j manteniendo óptimo
            obj_ranges[name] = (float(-np.inf), float(original_c + delta_up))
        else:
            # Para variable básica, hay que mirar cómo cambia z-row al modificar c_j.
            # row(i) tal que basis[i]=j (fila i+1 en T).
            i_b = basis.index(j)
            row = T[i_b + 1, :n_total]
            # Para cada no básica k: z-row[k] cambia en -Δ * row[k].
            # Necesitamos z-row[k] + Δ * row[k] ≥ 0   (para mantener óptimo en max)
            # → si row[k] > 0: Δ ≥ -z-row[k]/row[k]  (cota inferior)
            # → si row[k] < 0: Δ ≤ -z-row[k]/row[k]  (cota superior)
            z = T[0, :n_total]
            up = np.inf
            lo = -np.inf
            for k in range(n_total):
                if k in basis:
                    continue
                rk = row[k]
                zk = z[k]
                if rk > TOL:
                    lim = -zk / rk
                    if lim > lo:
                        lo = lim
                elif rk < -TOL:
                    lim = -zk / rk
                    if lim < up:
                        up = lim
            # Δ ∈ [lo, up]. c_j puede variar en [c_j + lo, c_j + up] (en escala interna max).
            # Trasladar a escala original:
            cj_orig = original_c
            obj_ranges[name] = (float(cj_orig + lo * sign), float(cj_orig + up * sign))
            if sign == -1.0:
                # para minimización, intercambiar para que el menor esté primero
                a, b = obj_ranges[name]
                obj_ranges[name] = (min(a, b), max(a, b))

    # === Rangos para RHS ===
    # Δb_i admisible mientras la solución básica x_B = B^-1 b ≥ 0.
    # B^-1 = columnas del tablero final correspondientes a las holguras originales.
    # Para restricciones sin holgura natural, usamos artificial (su columna inicial era unitaria también).
    Binv = np.zeros((m, m))
    for i in range(m):
        if i in s_indices:
            Binv[:, i] = T[1:, s_indices[i]]
        else:
            # usar columna artificial inicial
            for j, kind in enumerate(sf.aux_kinds):
                if kind == "a" and abs(sf.A[i, j] - 1.0) < TOL and np.allclose(np.delete(sf.A[:, j], i), 0, atol=TOL):
                    Binv[:, i] = T[1:, j]
                    break

    x_B = T[1:, -1]  # valores básicos actuales
    rhs_ranges = {}
    for i in range(m):
        col = Binv[:, i]
        up = np.inf
        lo = -np.inf
        for k in range(m):
            if col[k] > TOL:
                lim = -x_B[k] / col[k]
                if lim > lo:
                    lo = lim
            elif col[k] < -TOL:
                lim = -x_B[k] / col[k]
                if lim < up:
                    up = lim
        b_original = sf.b[i]
        rhs_ranges[names[i]] = (float(b_original + lo), float(b_original + up))

    return SensitivityReport(
        shadow_prices=shadow,
        constraint_names=names,
        reduced_costs=reduced,
        obj_ranges=obj_ranges,
        rhs_ranges=rhs_ranges,
        notes=[],
    )
