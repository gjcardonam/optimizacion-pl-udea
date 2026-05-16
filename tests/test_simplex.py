"""Tests rápidos para el Simplex básico."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from solver import (
    LPProblem, Constraint, ObjectiveSense, ConstraintType,
    solve_simplex, SimplexStatus,
)


def test_wyndor_glass():
    """Ejemplo clásico de Hillier (Wyndor Glass).

    Max Z = 3x1 + 5x2
    s.a.   x1        ≤ 4
                2x2  ≤ 12
           3x1 + 2x2 ≤ 18
           x1, x2 ≥ 0

    Óptimo: x1=2, x2=6, Z=36.
    """
    p = LPProblem(
        sense=ObjectiveSense.MAX,
        objective=[3, 5],
        constraints=[
            Constraint([1, 0], ConstraintType.LE, 4),
            Constraint([0, 2], ConstraintType.LE, 12),
            Constraint([3, 2], ConstraintType.LE, 18),
        ],
    )
    sf = p.to_standard_form()
    r = solve_simplex(sf)
    assert r.status == SimplexStatus.OPTIMAL, r.status
    assert abs(r.objective_value - 36.0) < 1e-6, r.objective_value
    assert abs(r.solution["x1"] - 2.0) < 1e-6
    assert abs(r.solution["x2"] - 6.0) < 1e-6
    print(f"✅ Wyndor Glass — Z={r.objective_value}, x1={r.solution['x1']}, x2={r.solution['x2']}, iters={len(r.tableaux)-1}")
    return r


def test_unbounded():
    """Max Z = x1 + x2 con -x1 + x2 ≤ 1 → no acotado."""
    p = LPProblem(
        sense=ObjectiveSense.MAX,
        objective=[1, 1],
        constraints=[
            Constraint([-1, 1], ConstraintType.LE, 1),
        ],
    )
    sf = p.to_standard_form()
    r = solve_simplex(sf)
    assert r.status == SimplexStatus.UNBOUNDED, r.status
    print(f"✅ Detección de no acotado: status={r.status}")


def test_min():
    """Min Z = 2x1 + 3x2 con x1 + x2 ≤ 10, x1 ≤ 5, x2 ≤ 8 → x1=x2=0, Z=0."""
    p = LPProblem(
        sense=ObjectiveSense.MIN,
        objective=[2, 3],
        constraints=[
            Constraint([1, 1], ConstraintType.LE, 10),
            Constraint([1, 0], ConstraintType.LE, 5),
            Constraint([0, 1], ConstraintType.LE, 8),
        ],
    )
    sf = p.to_standard_form()
    r = solve_simplex(sf)
    assert r.status == SimplexStatus.OPTIMAL
    assert abs(r.objective_value - 0.0) < 1e-6
    print(f"✅ Minimización trivial — Z={r.objective_value}")


if __name__ == "__main__":
    r = test_wyndor_glass()
    print("\nTableros de Wyndor Glass:")
    for t in r.tableaux:
        print(f"\n--- Iteración {t.iteration} — {t.note} ---")
        print(t.to_dataframe())

    print("\n")
    test_unbounded()
    test_min()
    print("\n🎉 Todos los tests pasaron.")
