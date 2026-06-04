"""UI Streamlit completa: Simplex, Gran M, Gráfico, Sensibilidad y Simplex Revisado.

Equipo: Cardona, Tabares — Optimización 2026-1 UdeA.
"""

import streamlit as st
import pandas as pd
import numpy as np

from solver import (
    LPProblem, Constraint, ObjectiveSense, ConstraintType,
    solve_simplex, solve_big_m, solve_revised,
    analyze_sensitivity, plot_graphical,
    SimplexStatus,
)

st.set_page_config(page_title="Solver PL — UdeA", layout="wide", page_icon="📐")

# ───────────────────────────────────────────────── Estilo (tema académico claro)
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Spline+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root{
  --ink:#16263d; --ink-soft:#54616f; --paper:#f6f3ec; --paper2:#efe9dc;
  --garnet:#9c2b38; --garnet-dk:#7f2330; --teal:#2f7d77; --rule:#d8cdb6;
}

html, body, [class*="css"], .stMarkdown, p, span, div, label, input, select, button{
  font-family:'Spline Sans', system-ui, sans-serif;
}
h1,h2,h3,h4{ font-family:'Fraunces', Georgia, serif !important; color:var(--ink) !important; letter-spacing:-.2px; }

[data-testid="stAppViewContainer"]{ background:var(--paper); }
[data-testid="stHeader"]{ background:transparent; }
.block-container{ padding-top:1.4rem; padding-bottom:3rem; max-width:1180px; }

/* ---- Hero ---- */
.hero{
  background:linear-gradient(120deg,#16263d 0%,#1f3550 58%,#243b59 100%);
  border-radius:18px; padding:28px 34px; margin:0 0 22px;
  box-shadow:0 16px 40px rgba(22,38,61,.20); position:relative; overflow:hidden;
}
.hero::after{ content:''; position:absolute; right:-50px; bottom:-70px; width:300px; height:300px;
  background:var(--teal); opacity:.13; clip-path:polygon(0% 100%,0% 30%,35% 0%,78% 12%,100% 60%,100% 100%); }
.hero-kicker{ font-family:'IBM Plex Mono',monospace; font-size:.78rem; letter-spacing:2px; color:#e9a6ad; text-transform:uppercase; margin-bottom:8px; }
.hero-title{ font-family:'Fraunces',serif; font-weight:600; font-size:2.25rem; color:#f6f3ec; line-height:1.05; }
.hero-sub{ font-family:'Fraunces',serif; font-style:italic; font-size:1.05rem; color:#cdd5de; margin-top:8px; }
.hero-credit{ font-family:'IBM Plex Mono',monospace; font-size:.72rem; color:#8b9bb0; margin-top:14px; letter-spacing:.5px; }

/* ---- Sidebar ---- */
[data-testid="stSidebar"]{ background:var(--paper2); border-right:1px solid var(--rule); }

/* ---- Botones ---- */
.stButton>button{
  background:var(--garnet) !important; color:#fff !important; border:none !important;
  border-radius:11px !important; font-weight:600 !important; padding:.65rem 1.1rem !important;
  box-shadow:0 8px 22px rgba(156,43,56,.25); transition:all .15s ease;
}
.stButton>button:hover{ background:var(--garnet-dk) !important; transform:translateY(-1px); }

/* ---- Métricas como tarjetas ---- */
[data-testid="stMetric"]{
  background:#fff; border:1px solid var(--rule); border-radius:14px; padding:14px 18px;
  box-shadow:0 6px 18px rgba(22,38,61,.07);
}
[data-testid="stMetricValue"]{ color:var(--garnet) !important; font-family:'Fraunces',serif !important; font-weight:600; }
[data-testid="stMetricLabel"]{ color:var(--ink-soft) !important; }

/* ---- Pestañas ---- */
.stTabs [data-baseweb="tab-list"]{ gap:4px; border-bottom:1px solid var(--rule); }
.stTabs [data-baseweb="tab"]{ font-weight:600; color:var(--ink-soft); }
.stTabs [aria-selected="true"]{ color:var(--garnet) !important; }
.stTabs [data-baseweb="tab-highlight"]{ background:var(--garnet) !important; }

/* ---- Expanders ---- */
[data-testid="stExpander"]{ border:1px solid var(--rule) !important; border-radius:12px !important; background:#fff; box-shadow:0 4px 14px rgba(22,38,61,.05); }

/* ---- Subheaders con regla de acento ---- */
[data-testid="stHeadingWithActionElements"] h2,
[data-testid="stHeadingWithActionElements"] h3{ border-bottom:2px solid var(--rule); padding-bottom:6px; }

/* ---- Varios ---- */
.stAlert{ border-radius:12px; }
code, kbd{ font-family:'IBM Plex Mono',monospace !important; color:var(--garnet); }
hr{ border-color:var(--rule); }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
  <div class="hero-kicker">Trabajo Final · Optimización 2026-1 · UdeA</div>
  <div class="hero-title">Solver de Programación Lineal</div>
  <div class="hero-sub">Resolución paso a paso — Simplex · Gran M · Gráfico · Sensibilidad</div>
  <div class="hero-credit">Equipo Cardona · Tabares — Universidad de Antioquia</div>
</div>
""",
    unsafe_allow_html=True,
)

# ───────────────────────────────────────────────── Sidebar: entrada
with st.sidebar:
    st.header("Definición del problema")
    sense = st.radio("Tipo de objetivo", ["max", "min"], horizontal=True)
    n_vars = st.number_input("Variables de decisión", min_value=2, max_value=8, value=2, step=1)
    n_rest = st.number_input("Restricciones", min_value=1, max_value=10, value=3, step=1)
    st.divider()
    st.markdown(
        "**Cómo se ingresa**\n\n"
        "El problema se ingresa en su **forma básica** (antes de la aumentada). "
        "El solver agrega holguras / excesos / artificiales automáticamente y "
        "elige el método apropiado (Simplex o Gran M)."
    )
    st.divider()
    preset = st.selectbox(
        "Cargar ejemplo",
        ["—", "Wyndor Glass (Max, ≤)", "Dieta (Min, mixto ≤/=/≥)", "Producción simple (Max, ≤)"],
    )

# Defaults dinámicos por preset
preset_defaults = None
if preset == "Wyndor Glass (Max, ≤)":
    preset_defaults = dict(
        sense="max", n=2, m=3, c=[3, 5],
        rows=[([1,0], "≤", 4), ([0,2], "≤", 12), ([3,2], "≤", 18)]
    )
elif preset == "Dieta (Min, mixto ≤/=/≥)":
    preset_defaults = dict(
        sense="min", n=2, m=3, c=[0.4, 0.5],
        rows=[([0.3,0.1], "≤", 2.7), ([0.5,0.5], "=", 6), ([0.6,0.4], "≥", 6)]
    )
elif preset == "Producción simple (Max, ≤)":
    preset_defaults = dict(
        sense="max", n=2, m=2, c=[4, 3],
        rows=[([2,1], "≤", 10), ([1,2], "≤", 8)]
    )

if preset_defaults:
    sense = preset_defaults["sense"]
    n_vars = preset_defaults["n"]
    n_rest = preset_defaults["m"]

# ───────────────────────────────────────────────── Función objetivo
st.subheader("Función objetivo")
st.markdown(f"**{sense.upper()}  Z =** " + " + ".join([f"c{i+1}·x{i+1}" for i in range(n_vars)]))
obj_cols = st.columns(n_vars)
obj_coeffs = []
for i in range(n_vars):
    default = (preset_defaults["c"][i] if preset_defaults and i < len(preset_defaults["c"])
               else (3.0 if i == 0 else 5.0))
    with obj_cols[i]:
        obj_coeffs.append(st.number_input(f"c{i+1}", value=float(default), key=f"obj_{preset}_{i}", format="%.4f"))

# ───────────────────────────────────────────────── Restricciones
st.subheader("Restricciones")
header = st.columns(n_vars + 2)
for i in range(n_vars):
    header[i].markdown(f"**x{i+1}**")
header[n_vars].markdown("**tipo**")
header[n_vars + 1].markdown("**b**")

rest_data = []
for r in range(n_rest):
    cols = st.columns(n_vars + 2)
    row_coeffs = []
    for i in range(n_vars):
        if preset_defaults and r < len(preset_defaults["rows"]):
            default = preset_defaults["rows"][r][0][i] if i < len(preset_defaults["rows"][r][0]) else 0.0
        else:
            default = 1.0 if r == i else 0.0
        with cols[i]:
            row_coeffs.append(st.number_input("v", value=float(default), key=f"r{preset}_{r}_c{i}",
                                              format="%.4f", label_visibility="collapsed"))
    with cols[n_vars]:
        default_ct = preset_defaults["rows"][r][1] if (preset_defaults and r < len(preset_defaults["rows"])) else "≤"
        ctype = st.selectbox("t", ["≤", "≥", "="], index=["≤","≥","="].index(default_ct),
                             key=f"r{preset}_{r}_ct", label_visibility="collapsed")
    with cols[n_vars + 1]:
        default_b = preset_defaults["rows"][r][2] if (preset_defaults and r < len(preset_defaults["rows"])) else 10.0
        rhs = st.number_input("b", value=float(default_b), key=f"r{preset}_{r}_rhs",
                              format="%.4f", label_visibility="collapsed")
    rest_data.append((row_coeffs, ctype, rhs))

ctype_map = {"≤": ConstraintType.LE, "≥": ConstraintType.GE, "=": ConstraintType.EQ}
sense_map = {"max": ObjectiveSense.MAX, "min": ObjectiveSense.MIN}

st.divider()
go = st.button("🚀 Resolver", type="primary", use_container_width=True)

# ───────────────────────────────────────────────── Helpers de render
def render_tableaux(tableaux, title="Tableros (iteración por iteración)"):
    st.subheader(title)
    for t in tableaux:
        with st.expander(f"Iteración {t.iteration} — {t.note}", expanded=(t.iteration <= 1)):
            df = t.to_dataframe()

            def highlight(data):
                styles = pd.DataFrame("", index=data.index, columns=data.columns)
                if t.pivot_row is not None and t.pivot_col is not None:
                    pivot_row_label = data.index[t.pivot_row]
                    pivot_col_label = data.columns[t.pivot_col]
                    styles.loc[pivot_row_label, :] = "background-color: #f7e4dd"
                    styles.loc[:, pivot_col_label] = "background-color: #f7e4dd"
                    styles.loc[pivot_row_label, pivot_col_label] = "background-color: #9c2b38; color: #ffffff; font-weight: bold"
                return styles

            st.dataframe(df.style.apply(highlight, axis=None), use_container_width=True)
            if t.entering_var:
                st.caption(f"Variable entrante: **{t.entering_var}** · Variable saliente: **{t.leaving_var}**")

# ───────────────────────────────────────────────── Ejecución
if go:
    try:
        problem = LPProblem(
            sense=sense_map[sense],
            objective=obj_coeffs,
            constraints=[
                Constraint(coeffs=cs, ctype=ctype_map[ct], rhs=b)
                for cs, ct, b in rest_data
            ],
        )
        sf = problem.to_standard_form()
    except Exception as e:
        st.error(f"Error al construir el problema: {e}")
        st.stop()

    # Elegir método principal: si hay artificiales → Gran M, si no → Simplex
    if sf.has_artificials:
        method_name = "Gran M"
        result = solve_big_m(sf)
    else:
        method_name = "Simplex tabular"
        result = solve_simplex(sf)

    st.success(f"Resuelto con método: **{method_name}** — Status: **{result.status.value.upper()}**")

    if result.status == SimplexStatus.OPTIMAL:
        decision = {k: v for k, v in result.solution.items() if k.startswith("x")}
        metric_cols = st.columns(1 + len(decision))
        metric_cols[0].metric("Z* óptimo", f"{result.objective_value:.2f}")
        for j, (k, v) in enumerate(decision.items()):
            metric_cols[j + 1].metric(k, f"{v:.2f}")
        if result.multiple_optima:
            st.warning("Existen **soluciones óptimas múltiples**.")
        if result.degenerate:
            st.warning("El problema presenta **degeneración**.")

    for note in result.notes:
        st.info(note)

    # ───────────── Tabs con cada vista
    tab_labels = ["📋 Tableros"]
    if problem.n_decision == 2:
        tab_labels.append("📈 Gráfico")
    if result.status == SimplexStatus.OPTIMAL:
        tab_labels.append("🔬 Sensibilidad")
        tab_labels.append("Σ Simplex Revisado")

    tabs = st.tabs(tab_labels)

    idx = 0
    with tabs[idx]:
        render_tableaux(result.tableaux)
    idx += 1

    if problem.n_decision == 2:
        with tabs[idx]:
            st.subheader("Método gráfico")
            opt = None
            if result.status == SimplexStatus.OPTIMAL:
                x1 = result.solution.get("x1", 0)
                x2 = result.solution.get("x2", 0)
                opt = (x1, x2, result.objective_value)
            fig, info = plot_graphical(problem, optimum=opt)
            st.pyplot(fig)
            if info["vertices"]:
                st.write("**Vértices factibles:**")
                st.dataframe(pd.DataFrame(info["vertices"], columns=["x₁", "x₂"]).round(4))
        idx += 1

    if result.status == SimplexStatus.OPTIMAL:
        with tabs[idx]:
            st.subheader("Análisis de sensibilidad")
            rep = analyze_sensitivity(sf, result,
                                       constraint_names=[f"R{i+1}" for i in range(sf.m)])
            shadow_df, reduced_df = rep.to_dataframes()
            st.markdown("**Precios sombra y rangos de RHS (b)**")
            st.dataframe(shadow_df, use_container_width=True)
            st.markdown("**Costos reducidos y rangos de coeficientes objetivo (c)**")
            st.dataframe(reduced_df, use_container_width=True)
            st.caption(
                "Los precios sombra indican cuánto cambia Z* por unidad adicional del recurso. "
                "Los costos reducidos indican cuánto se debería mejorar el coeficiente de una "
                "variable no básica para que entre en la solución óptima."
            )
        idx += 1

        with tabs[idx]:
            st.subheader("Simplex Revisado (matricial)")
            if sf.has_artificials:
                st.info("El Simplex Revisado se implementó sin artificiales. Para este problema, "
                        "la solución arriba se obtuvo con Gran M; el revisado se reserva a problemas "
                        "con restricciones tipo ≤.")
            else:
                rev = solve_revised(sf)
                st.write(f"**Status:** {rev.status.value} · **Z\\* =** {rev.objective_value:.4f}")
                for step in rev.steps:
                    with st.expander(f"Iteración {step.iteration} — base [{', '.join(step.basis_names)}]",
                                     expanded=(step.iteration == 0)):
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.write("**B** (columnas básicas)")
                            st.dataframe(pd.DataFrame(step.B, columns=step.basis_names).round(4),
                                          use_container_width=True)
                            st.write("**B⁻¹**")
                            st.dataframe(pd.DataFrame(step.B_inv).round(4), use_container_width=True)
                        with col_b:
                            st.write("**c_B** (coef. objetivo de variables básicas)")
                            st.dataframe(pd.DataFrame([step.cB], columns=step.basis_names).round(4),
                                          use_container_width=True)
                            st.write("**x_B = B⁻¹·b**")
                            st.dataframe(pd.DataFrame([step.xB], columns=step.basis_names).round(4),
                                          use_container_width=True)
                            st.write("**y = c_B·B⁻¹** (duales)")
                            st.dataframe(pd.DataFrame([step.y]).round(4), use_container_width=True)
                        st.caption(step.note)
