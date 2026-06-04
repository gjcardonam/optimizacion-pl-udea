# Optimización PL — Trabajo Final

Aplicativo que resuelve problemas de Programación Lineal paso a paso.

**Curso:** Optimización (2026-1) — Universidad de Antioquia
**Equipo:** Gabriel Cardona, Juan Sebastián Tabares
**Entrega final:** 2026-05-30

## Métodos implementados

- [x] **Simplex tabular básico** (restricciones ≤)
- [x] **Método de la Gran M** (restricciones ≥, =, mezcla)
- [x] **Simplex revisado** (forma matricial — B, B⁻¹, c_B·B⁻¹, costos reducidos)
- [x] **Método gráfico** (problemas de 2 variables)
- [x] **Análisis de sensibilidad** (precios sombra, costos reducidos, rangos de RHS y c_j)

## Casos especiales detectados

- Óptimo único
- Óptimos múltiples
- Solución no acotada
- Solución infactible (vía Gran M con artificiales > 0)
- Degeneración (manejada con regla de Bland)

## Cómo correr

```bash
# Una sola vez
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Lanzar la UI
.venv/bin/streamlit run app.py
# → http://localhost:8501

# Correr los tests
.venv/bin/python tests/test_all.py

# Regenerar el PDF del documento
.venv/bin/python build_pdf.py
```

## Estructura

```
solver/
  problem.py       # LPProblem, conversión forma básica → estándar
  tableau.py       # Tablero Simplex con render a DataFrame
  simplex.py       # Algoritmo Simplex tabular
  big_m.py         # Método de la Gran M
  revised.py       # Simplex revisado (matricial)
  graphical.py     # Método gráfico con matplotlib
  sensitivity.py   # Análisis de sensibilidad post-óptimo

app.py             # UI Streamlit
DOCUMENTO.md       # Documento entregable (fuente)
DOCUMENTO.pdf      # Documento entregable (PDF generado, 4 páginas)
build_pdf.py       # Regenera el PDF desde el MD
tests/
  test_simplex.py
  test_all.py
```

## Validación

Resultados verificados contra problemas clásicos (Hillier & Lieberman):

| Problema | Resultado esperado | Estado |
|---|---|---|
| Wyndor Glass | Z=36, x=(2,6) | ✅ |
| Dieta (mixto) | Z=5.25, x=(7.5, 4.5) | ✅ |
| Precios sombra Wyndor | (0, 1.5, 1) | ✅ |
| Rango RHS R2 Wyndor | [6, 18] | ✅ |
| No acotado | Detectado | ✅ |
| Infactible | Detectado | ✅ |
