---
marp: true
theme: default
paginate: true
size: 16:9
header: 'Optimización 2026-1 · UdeA'
footer: 'Solver de Programación Lineal paso a paso'
style: |
  section { font-size: 26px; }
  h1 { color: #1f3a5f; }
  h2 { color: #1f3a5f; border-bottom: 2px solid #d0d7de; padding-bottom: 6px; }
  table { font-size: 22px; }
  code { background: #f0f3f7; }
  .small { font-size: 20px; color: #555; }
---

<!-- _paginate: false -->
<!-- _header: '' -->
<!-- _footer: '' -->

# Solver de Programación Lineal
### Resolución paso a paso — Trabajo Final

**Optimización 2026-1 · Universidad de Antioquia**

Equipo: Gabriel Cardona · Tabares · Rodas

<span class="small">Simplex · Gran M · Simplex Revisado · Método Gráfico · Análisis de Sensibilidad</span>

---

## ¿Qué problema resolvemos?

Una empresa tiene **recursos limitados** (tiempo de máquina, materia prima, dinero)
y debe decidir **cuánto producir de cada producto** para **ganar lo máximo posible**
sin pasarse de ningún límite.

- Las decisiones → **variables** ( x₁, x₂, … )
- El objetivo → una función lineal a **maximizar** o **minimizar**
- Los límites → un conjunto de **restricciones** lineales

> La **Programación Lineal** responde: *¿cuánto de cada cosa, para optimizar el objetivo, respetando todas las restricciones?*

Nuestro software **automatiza** todo ese cálculo y lo muestra **paso a paso**.

---

## Problema modelo: Wyndor Glass

Decidir cuántos lotes producir de **2 productos** (puertas y ventanas)
para **maximizar la utilidad**, limitados por el tiempo de **3 plantas**.

$$
\begin{aligned}
\text{MAX } Z =\ & 3x_1 + 5x_2 \\
\text{s.a. } & x_1 \le 4 &\text{(Planta 1)}\\
 & 2x_2 \le 12 &\text{(Planta 2)}\\
 & 3x_1 + 2x_2 \le 18 &\text{(Planta 3)}\\
 & x_1, x_2 \ge 0
\end{aligned}
$$

**Solución óptima:** x₁ = 2, x₂ = 6, **Z\* = 36** — verificada por todos los métodos.

---

## Métodos implementados

| Método | ¿Cuándo se usa? |
|---|---|
| **Simplex tabular** | Todas las restricciones son ≤ (base inicial trivial) |
| **Gran M** | Hay restricciones ≥ o = (necesita variables artificiales) |
| **Simplex Revisado** | Misma lógica, en forma **matricial** (B, B⁻¹) |
| **Método gráfico** | Problemas de **2 variables** (región factible) |
| **Análisis de sensibilidad** | Post-óptimo: precios sombra y rangos |

<span class="small">El programa elige el método automáticamente según el tipo de restricciones.</span>

---

## Simplex tabular, paso a paso

Idea: moverse de **vértice a vértice** de la región factible, mejorando Z en cada paso.

1. Pasar a **forma estándar** (agregar holguras `sᵢ` a cada ≤).
2. Armar el **tablero inicial** con la base de holguras.
3. **Variable entrante:** la de costo reducido más favorable.
4. **Variable saliente:** prueba de la razón mínima (b / columna pivote).
5. **Pivotear** y repetir hasta que ningún costo reducido mejore → **óptimo**.

> En Wyndor: el programa llega al óptimo en **2 iteraciones** (3 tableros).

---

## Método de la Gran M

Cuando hay restricciones **≥** o **=**, la base de holguras no sirve como punto de partida.

- Se agregan **variables artificiales** `aᵢ` para tener una base inicial.
- Se penalizan en el objetivo con un costo **M** muy grande
  ( −M en maximización, +M en minimización ).
- El Simplex las **expulsa** de la base; si alguna queda > 0 → problema **infactible**.

> Así un mismo motor resuelve problemas con restricciones mixtas ≤ / = / ≥.

---

## Método gráfico (2 variables)

Para problemas de 2 variables el programa **dibuja**:

- Cada restricción como una **recta**.
- La **región factible** (intersección de todas).
- El **punto óptimo** en un **vértice** de la región.

![w:520](../docs/assets/grafico_wyndor.png)

<span class="small">Genera la gráfica automáticamente — útil para entender geométricamente el resultado.</span>

---

## Análisis de sensibilidad

Responde: *¿qué tan robusta es la solución óptima?*

- **Precios sombra:** cuánto cambia Z si tengo **una unidad más** de un recurso
  (valor de cada restricción).
- **Holguras:** capacidad sobrante; restricción con holgura 0 = **cuello de botella**.
- **Costos reducidos:** cuánto debería mejorar un producto no usado para que convenga.
- **Rangos:** cuánto puede variar cada coeficiente sin que cambie la base óptima.

---

## La aplicación

**Arquitectura limpia y modular:**

- `solver/` → motor (simplex, gran M, revisado, gráfico, sensibilidad)
- `app.py` → interfaz web en **Streamlit**
- `tests/` → **12 pruebas** automáticas (incluye casos especiales)

**Capacidades:** 2 a 8 variables · hasta 10 restricciones · MAX/MIN · ≤ = ≥
**Casos especiales detectados:** no acotado · infactible · óptimos múltiples

---

<!-- _header: '' -->
<!-- _footer: '' -->

# Demostración en vivo

1. Cargar el ejemplo **Wyndor Glass** → resolver → ver tableros, gráfico y sensibilidad.
2. Resolver **el problema que proponga el profesor**, ingresándolo en la app.

<span class="small">El motor es general: resuelve cualquier PL válido dentro del rango de tamaño.</span>

---

## Conclusiones

- Implementamos un **solver de PL completo** que resuelve **paso a paso**, no solo el resultado final.
- Cubre **Simplex, Gran M, Revisado, Gráfico y Sensibilidad** en una sola herramienta.
- Interfaz usable, validada con **12 pruebas** y casos especiales.
- El usuario se concentra en **analizar y decidir**, no en hacer cálculos a mano.

**¡Gracias! ¿Preguntas?**
