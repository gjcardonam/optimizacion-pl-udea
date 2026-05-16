"""Tests end-to-end de los cuatro métodos + sensibilidad + gráfico."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
from solver import (
    LPProblem, Constraint, ConstraintType, ObjectiveSense,
    solve_simplex, solve_big_m, solve_revised,
    analyze_sensitivity, plot_graphical,
    SimplexStatus,
)


def make(sense, c, rows):
    return LPProblem(
        sense=ObjectiveSense.MAX if sense == "max" else ObjectiveSense.MIN,
        objective=c,
        constraints=[Constraint(coeffs=cs, ctype={"≤":ConstraintType.LE,"≥":ConstraintType.GE,"=":ConstraintType.EQ}[ct], rhs=b)
                     for cs, ct, b in rows],
    )


def test_simplex_wyndor():
    p = make("max", [3,5], [([1,0],"≤",4), ([0,2],"≤",12), ([3,2],"≤",18)])
    r = solve_simplex(p.to_standard_form())
    assert r.status == SimplexStatus.OPTIMAL
    assert abs(r.objective_value - 36) < 1e-6
    assert abs(r.solution["x1"] - 2) < 1e-6
    assert abs(r.solution["x2"] - 6) < 1e-6
    print(f"✅ Simplex/Wyndor: Z=36, x=(2,6), iters={len(r.tableaux)-1}")


def test_big_m_mixed():
    p = make("min", [0.4, 0.5],
             [([0.3,0.1],"≤",2.7), ([0.5,0.5],"=",6), ([0.6,0.4],"≥",6)])
    r = solve_big_m(p.to_standard_form())
    assert r.status == SimplexStatus.OPTIMAL
    assert abs(r.objective_value - 5.25) < 1e-3
    assert abs(r.solution["x1"] - 7.5) < 1e-3
    assert abs(r.solution["x2"] - 4.5) < 1e-3
    print(f"✅ GranM/dieta: Z=5.25, x=(7.5, 4.5)")


def test_big_m_infeasible():
    p = make("max", [1,1], [([1,1],"≤",2), ([1,1],"≥",5)])
    r = solve_big_m(p.to_standard_form())
    assert r.status == SimplexStatus.INFEASIBLE
    print(f"✅ Infactibilidad detectada")


def test_unbounded():
    p = make("max", [1,1], [([-1,1],"≤",1)])
    r = solve_simplex(p.to_standard_form())
    assert r.status == SimplexStatus.UNBOUNDED
    print(f"✅ No acotado detectado")


def test_sensitivity_wyndor():
    p = make("max", [3,5], [([1,0],"≤",4), ([0,2],"≤",12), ([3,2],"≤",18)])
    sf = p.to_standard_form()
    r = solve_simplex(sf)
    rep = analyze_sensitivity(sf, r)
    assert abs(rep.shadow_prices[0] - 0.0) < 1e-6
    assert abs(rep.shadow_prices[1] - 1.5) < 1e-6
    assert abs(rep.shadow_prices[2] - 1.0) < 1e-6
    # Rangos de Planta 2: b ∈ [6, 18]
    lo, hi = rep.rhs_ranges["R2"]
    assert abs(lo - 6) < 1e-6 and abs(hi - 18) < 1e-6
    print(f"✅ Sensibilidad/Wyndor: y=(0, 1.5, 1), rango R2=[{lo}, {hi}]")


def test_revised_wyndor():
    p = make("max", [3,5], [([1,0],"≤",4), ([0,2],"≤",12), ([3,2],"≤",18)])
    r = solve_revised(p.to_standard_form())
    assert r.status == SimplexStatus.OPTIMAL
    assert abs(r.objective_value - 36) < 1e-6
    assert np.allclose(r.steps[-1].y, [0, 1.5, 1.0])
    print(f"✅ Revisado/Wyndor: Z=36, y={r.steps[-1].y}")


def test_graphical_wyndor():
    p = make("max", [3,5], [([1,0],"≤",4), ([0,2],"≤",12), ([3,2],"≤",18)])
    fig, info = plot_graphical(p)
    assert info["optimum"] is not None
    x, y, z = info["optimum"]
    assert abs(x - 2) < 1e-6 and abs(y - 6) < 1e-6 and abs(z - 36) < 1e-6
    print(f"✅ Gráfico/Wyndor: óptimo (2, 6, 36), vértices={len(info['vertices'])}")


def test_min_simple():
    # Min 2x1+3x2 s.a. x1+x2≥4, x1≤5, x2≤8
    # En el vértice x1=4,x2=0: Z=8 (factible)
    # En vértice x1=5,x2=0: Z=10
    # En vértice x1=5,x2=8: Z=34
    # x1=0,x2=8: Z=24 pero infeas para x1+x2≥4? 0+8=8≥4 ok. Z=24
    # x1=0,x2=4: Z=12
    # Mínimo: (4,0) → 8
    p = make("min", [2,3], [([1,1],"≥",4), ([1,0],"≤",5), ([0,1],"≤",8)])
    r = solve_big_m(p.to_standard_form())
    assert r.status == SimplexStatus.OPTIMAL
    assert abs(r.objective_value - 8) < 1e-3, r.objective_value
    print(f"✅ Min con ≥: Z=8")


def test_degenerate():
    # Problema con empate en razón mínima
    p = make("max", [3,5], [([1,0],"≤",4), ([0,1],"≤",6), ([3,2],"≤",18)])
    r = solve_simplex(p.to_standard_form())
    assert r.status == SimplexStatus.OPTIMAL
    print(f"✅ Degeneración manejada: Z={r.objective_value}, degenerate={r.degenerate}")


if __name__ == "__main__":
    print("=== Tests Simplex ===")
    test_simplex_wyndor()
    test_unbounded()

    print("\n=== Tests Gran M ===")
    test_big_m_mixed()
    test_big_m_infeasible()
    test_min_simple()

    print("\n=== Tests Sensibilidad ===")
    test_sensitivity_wyndor()

    print("\n=== Tests Simplex Revisado ===")
    test_revised_wyndor()

    print("\n=== Tests Gráfico ===")
    test_graphical_wyndor()

    print("\n=== Casos especiales ===")
    test_degenerate()

    print("\n🎉 TODOS los tests pasaron.")
