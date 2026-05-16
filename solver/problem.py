"""Representación de un problema de PL en forma básica y conversión a forma estándar."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple
import numpy as np


class ObjectiveSense(str, Enum):
    MAX = "max"
    MIN = "min"


class ConstraintType(str, Enum):
    LE = "<="
    GE = ">="
    EQ = "="


@dataclass
class Constraint:
    coeffs: List[float]
    ctype: ConstraintType
    rhs: float


@dataclass
class LPProblem:
    """Problema de PL en forma básica (antes de la forma aumentada).

    Variables de decisión: x1..xn (siempre ≥ 0).
    """
    sense: ObjectiveSense
    objective: List[float]          # c1..cn
    constraints: List[Constraint]
    var_names: List[str] = field(default_factory=list)

    def __post_init__(self):
        n = len(self.objective)
        if not self.var_names:
            self.var_names = [f"x{i+1}" for i in range(n)]
        for c in self.constraints:
            if len(c.coeffs) != n:
                raise ValueError(
                    f"Restricción con {len(c.coeffs)} coeficientes, "
                    f"se esperaban {n}"
                )

    @property
    def n_decision(self) -> int:
        return len(self.objective)

    @property
    def n_constraints(self) -> int:
        return len(self.constraints)

    def to_standard_form(self) -> "StandardForm":
        """Convierte a forma estándar:
        - Si es minimización: multiplica c por -1 (resolvemos como max y al final negamos z).
        - Multiplica filas con rhs < 0 por -1 (volteando el sentido).
        - Agrega holgura (s) para ≤, exceso (e) y artificial (a) para ≥, artificial (a) para =.
        - Retorna A, b, c extendidos y metadatos.
        """
        m = self.n_constraints
        n = self.n_decision

        # Copia mutable
        rows: List[List[float]] = []
        rhs: List[float] = []
        ctypes: List[ConstraintType] = []

        for c in self.constraints:
            row = list(c.coeffs)
            b = c.rhs
            ct = c.ctype
            # Asegurar rhs ≥ 0
            if b < 0:
                row = [-x for x in row]
                b = -b
                if ct == ConstraintType.LE:
                    ct = ConstraintType.GE
                elif ct == ConstraintType.GE:
                    ct = ConstraintType.LE
            rows.append(row)
            rhs.append(b)
            ctypes.append(ct)

        # Construir columnas auxiliares
        aux_names: List[str] = []
        aux_kinds: List[str] = []  # "s" (holgura), "e" (exceso), "a" (artificial)
        aux_cols: List[List[float]] = []  # cada columna es de longitud m

        # Recorremos restricciones y vamos agregando columnas
        s_idx = e_idx = a_idx = 0
        # Estructura por fila para saber cuál es la variable básica inicial
        basis_initial: List[int] = [-1] * m

        for i, ct in enumerate(ctypes):
            if ct == ConstraintType.LE:
                s_idx += 1
                col = [0.0] * m
                col[i] = 1.0
                aux_cols.append(col)
                aux_names.append(f"s{s_idx}")
                aux_kinds.append("s")
                basis_initial[i] = n + len(aux_names) - 1
            elif ct == ConstraintType.GE:
                e_idx += 1
                col_e = [0.0] * m
                col_e[i] = -1.0
                aux_cols.append(col_e)
                aux_names.append(f"e{e_idx}")
                aux_kinds.append("e")
                # artificial
                a_idx += 1
                col_a = [0.0] * m
                col_a[i] = 1.0
                aux_cols.append(col_a)
                aux_names.append(f"a{a_idx}")
                aux_kinds.append("a")
                basis_initial[i] = n + len(aux_names) - 1
            elif ct == ConstraintType.EQ:
                a_idx += 1
                col_a = [0.0] * m
                col_a[i] = 1.0
                aux_cols.append(col_a)
                aux_names.append(f"a{a_idx}")
                aux_kinds.append("a")
                basis_initial[i] = n + len(aux_names) - 1

        # Matriz A: filas originales + columnas auxiliares en paralelo
        A = np.zeros((m, n + len(aux_cols)))
        for i in range(m):
            for j in range(n):
                A[i, j] = rows[i][j]
            for k, col in enumerate(aux_cols):
                A[i, n + k] = col[i]

        b = np.array(rhs, dtype=float)

        # Vector c extendido. Para max, c original; para min, negamos.
        c_ext = np.zeros(n + len(aux_cols))
        sign = 1.0 if self.sense == ObjectiveSense.MAX else -1.0
        for j in range(n):
            c_ext[j] = sign * self.objective[j]
        # Holguras y excesos tienen coef 0 en obj.
        # Artificiales se penalizan con -M en el método Gran M (no acá).

        var_names_ext = list(self.var_names) + aux_names

        return StandardForm(
            A=A,
            b=b,
            c=c_ext,
            var_names=var_names_ext,
            aux_kinds=["x"] * n + aux_kinds,
            basis=basis_initial,
            original_sense=self.sense,
            n_decision=n,
        )


@dataclass
class StandardForm:
    A: np.ndarray             # m x (n + aux)
    b: np.ndarray             # m
    c: np.ndarray             # n + aux (en términos de MAXIMIZACIÓN)
    var_names: List[str]      # nombres de las columnas
    aux_kinds: List[str]      # "x"|"s"|"e"|"a" por columna
    basis: List[int]          # índice de columna que es básica en cada fila
    original_sense: ObjectiveSense
    n_decision: int           # cantidad de variables de decisión originales

    @property
    def has_artificials(self) -> bool:
        return "a" in self.aux_kinds

    @property
    def m(self) -> int:
        return self.A.shape[0]

    @property
    def n_total(self) -> int:
        return self.A.shape[1]
