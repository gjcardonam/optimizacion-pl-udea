---
marp: true
paginate: true
size: 16:9
header: 'Optimización 2026-1 · Universidad de Antioquia'
footer: 'Solver de Programación Lineal · paso a paso'
math: katex
style: |
  @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=Spline+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

  :root {
    --ink:      #16263d;
    --ink-soft: #54616f;
    --paper:    #f6f3ec;
    --paper-2:  #efe9dc;
    --garnet:   #9c2b38;
    --teal:     #2f7d77;
    --ochre:    #b07d2b;
    --rule:     #d8cdb6;

    --font-display: 'Fraunces', Georgia, serif;
    --font-body:    'Spline Sans', system-ui, sans-serif;
    --font-mono:    'IBM Plex Mono', monospace;
  }

  /* ---------- Base ---------- */
  section {
    background: var(--paper);
    color: var(--ink);
    font-family: var(--font-body);
    font-size: 25px;
    line-height: 1.5;
    letter-spacing: 0.1px;
    padding: 64px 76px 72px;
  }

  section::after {
    /* número de página */
    color: var(--ink-soft);
    font-family: var(--font-mono);
    font-size: 15px;
    font-weight: 500;
  }

  header {
    color: var(--ink-soft);
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    padding: 22px 76px 0;
  }

  footer {
    color: var(--ink-soft);
    font-family: var(--font-body);
    font-size: 14px;
    letter-spacing: 0.4px;
    padding: 0 76px 20px;
  }

  /* ---------- Tipografía ---------- */
  h1 {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 52px;
    line-height: 1.08;
    color: var(--ink);
    letter-spacing: -0.3px;
    margin: 0 0 14px;
  }

  h2 {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 38px;
    line-height: 1.12;
    color: var(--ink);
    letter-spacing: -0.2px;
    margin: 0 0 26px;
    padding-bottom: 14px;
    position: relative;
  }
  /* regla de acento bajo el título */
  h2::after {
    content: '';
    position: absolute;
    left: 0; bottom: 0;
    width: 64px; height: 4px;
    background: var(--garnet);
    border-radius: 2px;
  }

  h3 {
    font-family: var(--font-body);
    font-weight: 600;
    font-size: 22px;
    color: var(--teal);
    margin: 0 0 10px;
  }

  strong { color: var(--garnet); font-weight: 600; }
  em { color: var(--ink-soft); font-style: italic; }

  a { color: var(--teal); }

  /* ---------- Listas ---------- */
  ul, ol { margin: 6px 0; padding-left: 6px; }
  li { margin: 9px 0; padding-left: 26px; position: relative; list-style: none; }
  ul > li::before {
    content: '';
    position: absolute;
    left: 2px; top: 13px;
    width: 9px; height: 9px;
    background: var(--teal);
    transform: rotate(45deg);
    border-radius: 1.5px;
  }
  ol { counter-reset: step; }
  ol > li { counter-increment: step; }
  ol > li::before {
    content: counter(step);
    position: absolute;
    left: -2px; top: 1px;
    width: 24px; height: 24px;
    background: var(--ink);
    color: var(--paper);
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 600;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
  }
  li::marker { content: none; }

  /* ---------- Tablas ---------- */
  section table {
    border-collapse: collapse;
    width: auto !important;
    font-size: 21px;
    margin: 14px 0;
    background: transparent;
  }
  thead th {
    background: var(--ink);
    color: var(--paper);
    font-family: var(--font-body);
    font-weight: 600;
    text-align: left;
    padding: 13px 22px;
    letter-spacing: 0.2px;
  }
  thead th:first-child { border-radius: 10px 0 0 0; }
  thead th:last-child { border-radius: 0 10px 0 0; }
  tbody td {
    padding: 11px 22px;
    border-bottom: 1px solid var(--rule);
    color: var(--ink);
  }
  tbody tr:nth-child(odd) td { background: #fff; }
  tbody tr:nth-child(even) td { background: var(--paper-2); }
  tbody tr:last-child td { border-bottom: none; }
  tbody tr:last-child td:first-child { border-radius: 0 0 0 10px; }
  tbody tr:last-child td:last-child { border-radius: 0 0 10px 0; }

  /* ---------- Código / mono ---------- */
  code {
    font-family: var(--font-mono);
    font-size: 0.86em;
    background: var(--paper-2);
    color: var(--garnet);
    padding: 2px 7px;
    border-radius: 5px;
  }
  pre {
    background: var(--ink);
    border-radius: 10px;
    padding: 20px 24px;
    font-size: 19px;
    line-height: 1.45;
    box-shadow: 0 8px 24px rgba(22,38,61,0.16);
  }
  pre code {
    background: none;
    color: #e8eef5;
    padding: 0;
    font-size: 19px;
  }

  /* ---------- Cita / callout ---------- */
  blockquote {
    margin: 22px 0 0;
    padding: 16px 22px 16px 24px;
    background: var(--paper-2);
    border-left: 5px solid var(--garnet);
    border-radius: 0 10px 10px 0;
    font-size: 22px;
    color: var(--ink);
  }
  blockquote strong { color: var(--garnet); }

  /* ---------- Math ---------- */
  .katex { font-size: 1.06em; color: var(--ink); }

  /* ---------- Utilidades de layout ---------- */
  .cols { display: flex; gap: 40px; align-items: center; }
  .cols > div { flex: 1; min-width: 0; }
  .cols img { width: 100%; border-radius: 10px; box-shadow: 0 8px 28px rgba(22,38,61,0.14); }

  .lead-note { color: var(--ink-soft); font-size: 19px; }

  .chip {
    display: inline-block;
    font-family: var(--font-mono);
    font-size: 16px;
    font-weight: 500;
    color: var(--teal);
    background: var(--paper-2);
    border: 1px solid var(--rule);
    border-radius: 20px;
    padding: 4px 14px;
    margin: 4px 6px 4px 0;
  }

  .stat { display: flex; gap: 36px; margin-top: 10px; }
  .stat .num { font-family: var(--font-display); font-weight: 600; font-size: 44px; color: var(--garnet); line-height: 1; }
  .stat .lbl { font-size: 17px; color: var(--ink-soft); margin-top: 6px; }

  /* ---------- Portada ---------- */
  section.cover {
    padding: 0 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background:
      radial-gradient(1200px 600px at 88% -10%, rgba(47,125,119,0.10), transparent 60%),
      var(--paper);
  }
  section.cover::before {
    /* polígono "región factible" decorativo */
    content: '';
    position: absolute;
    right: -60px; bottom: -80px;
    width: 520px; height: 520px;
    background: var(--teal);
    opacity: 0.07;
    clip-path: polygon(0% 100%, 0% 30%, 35% 0%, 78% 12%, 100% 60%, 100% 100%);
  }
  section.cover .kicker {
    font-family: var(--font-mono);
    font-size: 17px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--garnet);
    margin-bottom: 18px;
  }
  section.cover h1 { font-size: 66px; max-width: 16ch; }
  section.cover .subtitle {
    font-family: var(--font-display);
    font-weight: 400;
    font-style: italic;
    font-size: 30px;
    color: var(--ink-soft);
    margin: 4px 0 30px;
  }
  section.cover .rule { width: 90px; height: 4px; background: var(--garnet); border-radius: 2px; margin: 6px 0 28px; }
  section.cover .meta { font-size: 21px; color: var(--ink); }
  section.cover .meta .team { font-weight: 600; }
  section.cover .methods { margin-top: 26px; }

  /* ---------- Sección divisoria ---------- */
  section.section {
    background:
      radial-gradient(1000px 700px at 15% 110%, rgba(156,43,56,0.10), transparent 60%),
      var(--ink);
    color: var(--paper);
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 90px;
  }
  section.section h1 { color: var(--paper); font-size: 58px; }
  section.section .kicker {
    font-family: var(--font-mono);
    font-size: 17px; letter-spacing: 2px; text-transform: uppercase;
    color: #e9a6ad; margin-bottom: 16px;
  }
  section.section .rule { width: 90px; height: 4px; background: var(--garnet); border-radius: 2px; margin: 14px 0 0; }
  section.section p { color: #cdd5de; font-size: 23px; max-width: 30ch; }
  section.section::after { color: rgba(246,243,236,0.5); }

  /* títulos sin header/footer en portada y secciones */
  section.cover header, section.cover footer,
  section.section header, section.section footer { display: none; }
---

<!-- _class: cover -->
<!-- _paginate: false -->

<div class="kicker">Trabajo Final · Optimización</div>

# Solver de Programación Lineal

<div class="subtitle">Resolución paso a paso, no solo el resultado</div>

<div class="rule"></div>

<div class="meta">
<span class="team">Gabriel Cardona · Juan S. Tabares</span><br>
Universidad de Antioquia — 2026-1
</div>

<div class="methods">
<span class="chip">Simplex</span>
<span class="chip">Gran M</span>
<span class="chip">Simplex Revisado</span>
<span class="chip">Método Gráfico</span>
<span class="chip">Sensibilidad</span>
</div>

---

## ¿Qué problema resolvemos?

Una empresa tiene **recursos limitados** —tiempo de máquina, materia prima, dinero— y debe decidir **cuánto producir de cada producto** para **optimizar un objetivo** sin violar ningún límite.

- Las decisiones → **variables** ( $x_1, x_2, \dots$ )
- El objetivo → una función lineal a **maximizar** o **minimizar**
- Los límites → un conjunto de **restricciones** lineales

> La **Programación Lineal** responde: *¿cuánto de cada cosa, para optimizar el objetivo, respetando todas las restricciones?*

Nuestro software **automatiza** ese cálculo y lo muestra **paso a paso**.

---

## Problema modelo · Wyndor Glass

<div class="cols">
<div>

Decidir cuántos lotes producir de **2 productos** (puertas y ventanas) para **maximizar la utilidad**, limitados por el tiempo de **3 plantas**.

$$
\begin{aligned}
\text{máx } Z =\ & 3x_1 + 5x_2 \\[2pt]
\text{s.a. }\quad & x_1 \le 4 & \text{(Planta 1)}\\
& 2x_2 \le 12 & \text{(Planta 2)}\\
& 3x_1 + 2x_2 \le 18 & \text{(Planta 3)}\\
& x_1,\, x_2 \ge 0
\end{aligned}
$$

</div>
<div>

<div class="stat">
<div><div class="num">2</div><div class="lbl">lotes de puertas · x₁</div></div>
<div><div class="num">6</div><div class="lbl">lotes de ventanas · x₂</div></div>
<div><div class="num">36</div><div class="lbl">utilidad · Z*</div></div>
</div>

<br>

> **Solución óptima verificada** por todos los métodos del solver. Lo usamos como hilo conductor de la presentación y la demo.

</div>
</div>

---

## Métodos implementados

| Método | ¿Cuándo se usa? |
|---|---|
| **Simplex tabular** | Todas las restricciones son ≤ (base inicial trivial) |
| **Gran M** | Hay restricciones ≥ o = (requiere variables artificiales) |
| **Simplex Revisado** | Misma lógica, en forma **matricial** ( B, B⁻¹ ) |
| **Método gráfico** | Problemas de **2 variables** (región factible) |
| **Análisis de sensibilidad** | Post-óptimo: precios sombra y rangos |

<p class="lead-note">El programa elige el método automáticamente según el tipo de restricciones.</p>

---

## Simplex, paso a paso

<div class="cols">
<div>

Idea: moverse de **vértice a vértice** de la región factible, **mejorando Z** en cada salto.

1. Pasar a **forma estándar** (agregar holguras $s_i$ a cada ≤).
2. Armar el **tablero inicial** con la base de holguras.
3. **Variable entrante:** costo reducido más favorable.
4. **Variable saliente:** prueba de la razón mínima.
5. **Pivotear** y repetir hasta que ningún costo reducido mejore → **óptimo**.

</div>
<div>

> En **Wyndor**, el solver llega al óptimo en **2 iteraciones** (3 tableros), registrando cada paso para mostrarlo.

```text
(0,0) --> (0,6) --> (2,6)
 Z=0      Z=30      Z=36
                    óptimo
```

</div>
</div>

---

## Método de la Gran M

Cuando hay restricciones **≥** o **=**, la base de holguras **no sirve** como punto de partida.

- Se agregan **variables artificiales** $a_i$ para tener una base inicial válida.
- Se penalizan en el objetivo con un costo **M** muy grande ( $-M$ al maximizar, $+M$ al minimizar ).
- El Simplex las **expulsa** de la base; la penalización las fuerza a salir.

> Si alguna artificial **queda > 0** en el óptimo → el problema es **infactible**. Así un mismo motor resuelve restricciones mixtas ≤ / = / ≥.

---

## Método gráfico · 2 variables

<div class="cols">
<div>

Para 2 variables, el programa **dibuja** la solución:

- Cada restricción como una **recta**.
- La **región factible** (intersección de todas).
- El **óptimo**, siempre en un **vértice** de la región.

<p class="lead-note">La gráfica se genera automáticamente — fija la intuición geométrica del resultado.</p>

</div>
<div>

![Región factible y óptimo de Wyndor Glass](../docs/assets/grafico_wyndor_deck.png)

</div>
</div>

---

## Análisis de sensibilidad

¿Qué tan **robusta** es la solución óptima? El tablero final responde sin recalcular:

- **Precios sombra** — cuánto cambia Z con **una unidad más** de un recurso.
- **Holguras** — capacidad sobrante; holgura 0 marca un **cuello de botella**.
- **Costos reducidos** — cuánto debe mejorar un producto no usado para que convenga.
- **Rangos** — cuánto puede variar cada coeficiente sin que cambie la base óptima.

> En Wyndor: precios sombra **(0, 1.5, 1)** — las Plantas 2 y 3 son los cuellos de botella.

---

## La aplicación

<div class="cols">
<div>

**Arquitectura limpia y modular**

- `solver/` → motor (simplex, gran M, revisado, gráfico, sensibilidad)
- `app.py` → interfaz web en **Streamlit**
- `tests/` → **12 pruebas** automáticas, con casos especiales

</div>
<div>

**Capacidades**

<span class="chip">2 – 8 variables</span>
<span class="chip">hasta 10 restricciones</span>
<span class="chip">MAX / MIN</span>
<span class="chip">≤ &nbsp; = &nbsp; ≥</span>

**Casos especiales detectados**

<span class="chip">no acotado</span>
<span class="chip">infactible</span>
<span class="chip">óptimos múltiples</span>
<span class="chip">degeneración</span>

</div>
</div>

---

<!-- _class: section -->
<!-- _paginate: false -->

<div class="kicker">En vivo</div>

# Demostración

<div class="rule"></div>

<p>Wyndor Glass de principio a fin — tableros, gráfica y sensibilidad — y luego el problema que proponga el profesor, resuelto en el momento.</p>

---

## Conclusiones

- Construimos un **solver de PL completo** que resuelve **paso a paso**, no solo el resultado final.
- Reúne **Simplex, Gran M, Revisado, Gráfico y Sensibilidad** en una sola herramienta.
- Interfaz usable, validada con **12 pruebas** y casos especiales.
- El usuario se concentra en **analizar y decidir**, no en calcular a mano.

> **¡Gracias!** ¿Preguntas?

<p class="lead-note">github.com/gjcardonam/optimizacion-pl-udea</p>
