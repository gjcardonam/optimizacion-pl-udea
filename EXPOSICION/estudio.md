# Documento de estudio — Programación Lineal y el solver

Material de repaso para entender la teoría detrás del trabajo final y poder **defenderlo**.
Todo lo que aquí se describe está implementado en `solver/` y se demuestra con `app.py`.

---

## 1. Fundamentos de Programación Lineal (PL)

Un problema de PL busca **optimizar** (maximizar o minimizar) una **función objetivo lineal**
sujeta a un conjunto de **restricciones lineales** y a la **no negatividad** de las variables.

Forma general (maximización):

```
MAX  Z = c₁x₁ + c₂x₂ + … + cₙxₙ
s.a. aᵢ₁x₁ + … + aᵢₙxₙ  (≤ , = , ≥)  bᵢ      para cada restricción i
     x₁, …, xₙ ≥ 0
```

- **Variables de decisión (xⱼ):** lo que se decide (cuánto producir de cada producto).
- **Coeficientes de costo (cⱼ):** aporte de cada variable al objetivo.
- **Coeficientes técnicos (aᵢⱼ):** consumo de recurso i por unidad de variable j.
- **Lado derecho (bᵢ):** disponibilidad del recurso i.

**Propiedad clave (que justifica el Simplex):** la **región factible** de un PL es un
**poliedro convexo**, y si existe óptimo, está en al menos un **vértice** (punto extremo).
Por eso basta recorrer vértices en vez de infinitos puntos.

---

## 2. Forma estándar

Antes de aplicar el Simplex, todo problema se lleva a **forma estándar** (todas igualdades, todo ≥ 0):

| Restricción original | Se agrega | Resultado |
|---|---|---|
| `≤ b` | variable de **holgura** `s ≥ 0` | `… + s = b` |
| `≥ b` | variable de **exceso** `e ≥ 0` (se resta) + **artificial** `a ≥ 0` | `… − e + a = b` |
| `= b` | variable **artificial** `a ≥ 0` | `… + a = b` |

- **Holgura (slack):** recurso que sobra de una restricción ≤.
- **Exceso (surplus):** cuánto se supera un mínimo en una restricción ≥.
- **Artificial:** variable auxiliar solo para tener una **base inicial**; debe salir de la solución.

En el repo esto lo hace `LPProblem.to_standard_form()` (archivo `solver/problem.py`).

---

## 3. Método Simplex (tabular)

Algoritmo iterativo que va de un vértice a otro **mejorando** Z hasta el óptimo.

**Pasos:**
1. **Tablero inicial:** base formada por las holguras (factible si todo era ≤).
2. **Costos reducidos (fila Z):** indican si entra una variable mejora Z.
   - En **maximización**, una variable mejora si su costo reducido es **positivo** (criterio de entrada).
   - El óptimo se alcanza cuando **ningún** costo reducido mejora.
3. **Variable entrante:** la columna con el costo reducido más favorable.
4. **Variable saliente — prueba de la razón mínima:** se divide cada `bᵢ` entre el
   coeficiente positivo de la columna entrante; gana la **menor razón** (evita salir de la región factible).
5. **Pivoteo:** operaciones de fila (Gauss-Jordan) para que la entrante tome valor 1 en su fila y 0 en el resto.
6. Volver al paso 2.

**En el repo:** `solver/simplex.py` (`solve_simplex`) usando `solver/tableau.py` (clase `Tableau`).
Cada iteración guarda su tablero → por eso se ve **paso a paso**.

**Ejemplo verificado (Wyndor Glass):** `MAX 3x₁+5x₂` con tres ≤ → óptimo **x₁=2, x₂=6, Z=36**, en 2 iteraciones (3 tableros).

---

## 4. Método de la Gran M

Se usa cuando hay restricciones **≥** o **=**, donde las holguras no dan base factible.

- Se introducen **variables artificiales** `aᵢ` para arrancar con una base.
- Se penalizan en el objetivo con un coeficiente **M** muy grande:
  - Maximización: `… − M·a₁ − M·a₂ − …` (castiga tenerlas).
  - Minimización: `… + M·a₁ + …`.
- Al optimizar, el Simplex **expulsa** las artificiales (las lleva a 0).
- **Diagnóstico de infactibilidad:** si en el óptimo **alguna artificial queda > 0**, el problema **no tiene solución factible**.

**En el repo:** `solver/big_m.py` (`solve_big_m`). El programa decide usar Gran M
automáticamente cuando detecta restricciones ≥ o =.

---

## 5. Método gráfico (2 variables)

Solo para problemas de **2 variables** (se pueden dibujar en el plano).

- Cada restricción es una **recta**; su lado factible es un semiplano.
- La **región factible** es la intersección de todos los semiplanos (un polígono convexo).
- La función objetivo es una familia de **rectas de nivel** que se desplazan; el óptimo
  es el **último vértice** que toca la región en la dirección de mejora.
- Para `≥` la región es "hacia afuera" (mínimos a cumplir); para `≤` es "hacia adentro".

**En el repo:** `solver/graphical.py` (`plot_graphical`) genera la imagen con matplotlib.

---

## 6. Simplex Revisado (forma matricial)

Misma lógica del Simplex pero expresada con **álgebra matricial**, más eficiente y compacta.

- `B` = matriz de la **base** (columnas de las variables básicas).
- `B⁻¹` = inversa de la base; el corazón del método.
- `x_B = B⁻¹·b` → valores de las variables básicas.
- `c_B·B⁻¹` → multiplicadores (relacionados con los **precios sombra**).
- Costos reducidos = `cⱼ − c_B·B⁻¹·Aⱼ`.

Ventaja: en problemas grandes no recalcula todo el tablero, solo trabaja con `B⁻¹`.

**En el repo:** `solver/revised.py` (`solve_revised`), expone B, B⁻¹ y c_B·B⁻¹ por iteración.

---

## 7. Análisis de sensibilidad (post-óptimo)

Estudia **qué tan estable** es la solución óptima ante cambios en los datos.

- **Precios sombra (dual):** cuánto cambia `Z*` por **una unidad adicional** del recurso `bᵢ`.
  Mide el valor marginal de cada recurso. Una restricción **no activa** (con holgura) tiene precio sombra 0.
- **Holguras en el óptimo:** capacidad remanente de cada restricción.
  Holgura **0** → restricción **activa** = **cuello de botella** (limita la solución).
- **Costos reducidos:** para una variable que quedó en 0, cuánto debería mejorar su coeficiente
  objetivo para que **entre** a la solución óptima.
- **Rangos de variación:**
  - de los `cⱼ` (objetivo): intervalo donde la **base óptima no cambia**.
  - de los `bᵢ` (recursos): intervalo donde el **precio sombra sigue siendo válido**.

**En el repo:** `solver/sensitivity.py` (`analyze_sensitivity`, `SensitivityReport`).

---

## 8. Casos especiales (el programa los detecta)

| Caso | Cómo se reconoce |
|---|---|
| **Solución única** | óptimo en un solo vértice; costos reducidos estrictamente desfavorables |
| **Óptimos múltiples** | un costo reducido de variable **no básica = 0** en el óptimo |
| **No acotado (unbounded)** | la columna entrante no tiene **ninguna razón positiva** (Z crece sin límite) |
| **Infactible** | una **artificial queda > 0** en el óptimo (Gran M) |
| **Degeneración** | una variable **básica vale 0**; puede causar empates en la razón mínima |

Estos casos están cubiertos por la suite de pruebas (`tests/`, 12 tests).

---

## 9. Mapa teoría → código

| Concepto | Archivo | Símbolo |
|---|---|---|
| Modelo del problema, forma estándar | `solver/problem.py` | `LPProblem`, `Constraint`, `to_standard_form()` |
| Tablero y pivoteo | `solver/tableau.py` | `Tableau` |
| Simplex tabular | `solver/simplex.py` | `solve_simplex`, `SimplexResult`, `SimplexStatus` |
| Gran M | `solver/big_m.py` | `solve_big_m` |
| Simplex revisado | `solver/revised.py` | `solve_revised`, `RevisedStep` |
| Método gráfico | `solver/graphical.py` | `plot_graphical` |
| Sensibilidad | `solver/sensitivity.py` | `analyze_sensitivity`, `SensitivityReport` |
| Interfaz | `app.py` | UI Streamlit |
| Pruebas | `tests/test_all.py`, `tests/test_simplex.py` | 12 casos |

---

## 10. Glosario rápido

- **Función objetivo:** lo que se maximiza o minimiza.
- **Región factible:** conjunto de puntos que cumplen todas las restricciones.
- **Vértice / punto extremo:** esquina de la región factible; candidato a óptimo.
- **Variable básica:** la que está "activa" en el tablero actual (forma la base).
- **Variable no básica:** vale 0 en la solución actual.
- **Costo reducido:** mejora potencial de Z al meter una variable no básica.
- **Precio sombra:** valor marginal de un recurso (una unidad más de `bᵢ`).
- **Holgura:** recurso sobrante de una restricción ≤.
- **Cuello de botella:** restricción activa (holgura 0) que limita el óptimo.

---

## 11. Cómo correr el proyecto (recordatorio)

```bash
# desde la raíz del repo
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py     # → http://localhost:8501
.venv/bin/python -m pytest -q      # correr los 12 tests
```

Repo: https://github.com/gjcardonam/optimizacion-pl-udea
