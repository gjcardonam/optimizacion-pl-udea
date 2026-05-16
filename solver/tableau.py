"""Representación de un tablero Simplex en una iteración dada."""

from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import pandas as pd


@dataclass
class Tableau:
    """Foto del tablero Simplex en una iteración.

    Convención (estilo libro Hillier / clase Ude@):
      Fila 0 (z-row): coeficientes reducidos c_j - z_j   (queremos todos ≤ 0 para óptimo en MAX)
      Filas 1..m: cuerpo Ax = b con b en última columna.
    """
    iteration: int
    var_names: List[str]
    basis: List[int]                # índice de columna básica por fila
    matrix: np.ndarray              # (m+1) x (n+1). Última col = RHS / z.
    pivot_row: Optional[int] = None      # 1..m (índice en matriz)
    pivot_col: Optional[int] = None      # 0..n-1
    entering_var: Optional[str] = None
    leaving_var: Optional[str] = None
    note: str = ""

    @property
    def m(self) -> int:
        return self.matrix.shape[0] - 1

    @property
    def n(self) -> int:
        return self.matrix.shape[1] - 1

    @property
    def z_value(self) -> float:
        return float(self.matrix[0, -1])

    def to_dataframe(self) -> pd.DataFrame:
        cols = list(self.var_names) + ["RHS"]
        rows = ["z"] + [self.var_names[i] for i in self.basis]
        df = pd.DataFrame(self.matrix, index=rows, columns=cols)
        return df.round(4)
