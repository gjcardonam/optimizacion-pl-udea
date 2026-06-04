# Guion de exposición — qué decir en cada diapositiva

**Tiempo total objetivo: ~13 min** (límite del profe: 15 min máx).
Formato pedido en clase: *intro breve en diapositivas + demo en vivo del software*.

## Reparto

| Quién | Diapositivas | Tema | Tiempo aprox. |
|---|---|---|---|
| **Juan** | 1 – 7 | El problema y **todos los métodos de resolución** (Simplex, Gran M, gráfico) | ~6:00 |
| **Gabriel** | 8 – 11 | **Sensibilidad, la aplicación y la demo en vivo** + cierre | ~7:10 |

> El relevo es en la diapositiva 8. Idea práctica: **Gabriel maneja el computador en la demo**, así que conviene que él tenga el teclado desde el relevo. Juan puede avanzar las slides 1–7.

> Cómo usar este guion: cada bloque es lo que dice esa persona mientras la diapositiva está en pantalla.
> No lo lean palabra por palabra; son los puntos. Marquen con la voz los **términos en negrita** (los que el profe espera oír).
> Las líneas **Dato clave** son munición para sonar sólidos y para responder preguntas — no hay que decirlas todas, pero conviene tenerlas.

---

## 🔵 JUAN — primera mitad (diapositivas 1–7)

### Diapositiva 1 — Portada · 🗣 Juan · ⏱ 0:20 (acum 0:20)

> "Buenos días. Vamos a presentar nuestro trabajo final: un **solver de Programación Lineal** que resuelve **paso a paso**, no solo da el resultado. Implementa cinco métodos: **Simplex, Gran M, Simplex Revisado, método gráfico y análisis de sensibilidad**. Yo cubro la parte de los métodos y Gabriel la demostración en vivo."

*(Directo. No te detengas aquí.)*

---

### Diapositiva 2 — ¿Qué problema resolvemos? · 🗣 Juan · ⏱ 1:00 (acum 1:20)

> "La Programación Lineal aparece cuando hay **recursos limitados** —tiempo de máquina, materia prima, dinero— y hay que decidir **cuánto producir de cada cosa** para **optimizar un objetivo** sin pasarse de ningún límite.
>
> Esas decisiones son las **variables**. Lo que se optimiza es la **función objetivo**, que es lineal. Y los topes son las **restricciones**, también lineales. La pregunta de fondo siempre es: *cuánto de cada cosa, para optimizar, respetando todas las restricciones.*"

**Dato clave:** la PL es la base de la **Investigación de Operaciones** y de las más usadas en la industria. La exigencia de que todo sea **lineal** no es un capricho: hace que la **región factible sea un poliedro convexo**, y eso es lo que vuelve el problema resoluble de forma exacta y eficiente.

---

### Diapositiva 3 — Problema modelo · Wyndor Glass · 🗣 Juan · ⏱ 1:10 (acum 2:30)

> "Para mostrarlo usamos un problema clásico, **Wyndor Glass**. Se producen dos productos —puertas y ventanas— y se quiere **maximizar la utilidad**, limitados por el tiempo de **tres plantas**.
>
> La formulación: maximizar Z = **3x₁ + 5x₂**, sujeto a las tres restricciones de planta, todas de tipo *menor o igual*, con variables no negativas. La solución óptima es **x₁ = 2, x₂ = 6, con Z = 36**, y está verificada por **todos** los métodos del programa."

**Dato clave:** Wyndor es el ejemplo canónico de **Hillier & Lieberman**; lo usamos justo porque su resultado (Z = 36) es conocido y nos sirve de **prueba de validación** del solver.

*(Señala la formulación mientras hablas.)*

---

### Diapositiva 4 — Métodos implementados · 🗣 Juan · ⏱ 0:40 (acum 3:10)

> "No implementamos un solo método, sino una familia. **Simplex tabular** cuando todo es *menor o igual*. **Gran M** cuando hay *mayor o igual* o *igualdad*. El **Simplex Revisado**, la misma idea en forma **matricial**. El **método gráfico** para dos variables. Y el **análisis de sensibilidad** al final. Lo importante: **el programa elige el método solo** según las restricciones que uno ingrese."

**Dato clave:** el **método Simplex** lo inventó **George Dantzig en 1947**; sigue siendo, 75 años después, el algoritmo más usado para resolver problemas lineales.

---

### Diapositiva 5 — Simplex, paso a paso · 🗣 Juan · ⏱ 1:10 (acum 4:20)

> "La idea del **Simplex** es moverse de **vértice a vértice** de la región factible, **mejorando Z** en cada salto. Primero se pasa a **forma estándar** agregando una **holgura** a cada restricción. Se arma el **tablero inicial**. En cada iteración: entra la variable de **mejor costo reducido**, sale la que indica la **prueba de la razón mínima**, y se **pivotea**. Se repite hasta que ningún costo reducido mejore: ahí está el **óptimo**. En Wyndor llega en **dos iteraciones**: del origen, a (0,6), a (2,6)."

**Dato clave:** esto se apoya en el **Teorema Fundamental de la PL**: *si existe óptimo, hay al menos un óptimo en un vértice*. Por eso basta recorrer vértices. En el peor caso el Simplex es **exponencial** (el famoso cubo de **Klee–Minty**, 1972), pero **en la práctica converge en pocas iteraciones** —Wyndor, en 2— lo que explica por qué se usa tanto.

---

### Diapositiva 6 — Método de la Gran M · 🗣 Juan · ⏱ 0:50 (acum 5:10)

> "Cuando hay restricciones *mayor o igual* o *igualdad*, no hay una base inicial fácil. Ahí entra la **Gran M**: se agregan **variables artificiales** para arrancar, y se **penalizan** en el objetivo con un costo **M** muy grande. El Simplex, al optimizar, **expulsa** esas artificiales. Si al final alguna queda **positiva**, el problema es **infactible**: no tiene solución. Así un mismo motor resuelve también restricciones mixtas."

**Dato clave:** la alternativa a Gran M es el **método de Dos Fases**. Elegimos Gran M porque es **directo** —un solo modelo penalizado—, aunque numéricamente es más sensible: en el código M = **1 000 000** y por eso usamos tolerancias escaladas. Para evitar que el Simplex se **cicle** en problemas **degenerados**, implementamos la **regla de Bland** (Robert Bland, 1977), que garantiza terminación.

---

### Diapositiva 7 — Método gráfico · 🗣 Juan · ⏱ 0:50 (acum 6:00)

> "Para problemas de **dos variables**, el programa además **dibuja** la solución: cada restricción es una **recta**, sombrea la **región factible** —la intersección de todas— y marca el **óptimo**, que siempre cae en un **vértice**. La recta punteada es la función objetivo: se desliza hasta el último punto factible, y ese punto es la respuesta. Con esto cierro la parte de métodos; les dejo a Gabriel la parte de análisis y la demostración."

**Dato clave:** la función objetivo es una familia de **rectas de nivel** paralelas; el óptimo es el **último vértice** que tocan al desplazarse en la dirección de mejora. Si esa recta queda **paralela a una arista**, hay **óptimos múltiples** (toda la arista es óptima).

*(Apunta a la región factible. Cierra y pásale la palabra a Gabriel.)*

---

## 🟣 GABRIEL — segunda mitad (diapositivas 8–11)

> **Relevo:** Gabriel toma la palabra (y el computador). Arranca reconociendo el cambio: *"Gracias, Juan. Hasta aquí vimos cómo el programa resuelve; ahora qué más nos dice la solución, y lo mostramos funcionando."*

### Diapositiva 8 — Análisis de sensibilidad · 🗣 Gabriel · ⏱ 1:10 (acum 7:10)

> "Gracias, Juan. El análisis de sensibilidad responde qué tan **robusta** es la solución, leyendo el **tablero final** sin recalcular nada.
>
> Los **precios sombra** dicen cuánto cambia Z si tuviéramos **una unidad más** de un recurso. Las **holguras** son la capacidad que sobra: una restricción con holgura **cero** es un **cuello de botella**. Los **costos reducidos** dicen cuánto tendría que mejorar un producto no usado para que convenga producirlo. Y los **rangos** dicen cuánto puede variar cada dato sin que cambie la base óptima.
>
> En Wyndor los precios sombra son **(0, 1.5, 1)**: la Planta 1 sobra, y las Plantas 2 y 3 son los cuellos de botella."

**Dato clave (lo que demuestra dominio):** los precios sombra son las **variables del problema dual**. Por el **teorema de dualidad fuerte**, el óptimo del primal es igual al del dual. Y se cumple **holgura complementaria**: o sobra recurso (holgura > 0) o vale conseguir más (precio sombra > 0), **nunca ambos**. En Wyndor, el rango del lado derecho de la Planta 2 es **[6, 18]**: dentro de ese intervalo el precio sombra 1.5 sigue siendo válido.

---

### Diapositiva 9 — La aplicación · 🗣 Gabriel · ⏱ 1:00 (acum 8:10)

> "En cuanto a la construcción, el proyecto tiene una **arquitectura modular**: una carpeta `solver` con el motor —cada método en su archivo—, la interfaz web en **Streamlit**, y una suite de **doce pruebas** automáticas que incluyen los casos especiales. Soporta de **2 a 8 variables** y hasta **10 restricciones**, maximización o minimización, y los tres tipos de restricción. Y **detecta los casos especiales**: **no acotado**, **infactible**, **óptimos múltiples** y **degeneración**."

**Dato clave:** cada caso especial se reconoce mirando el tablero — **no acotado**: columna entrante sin coeficiente positivo (no hay razón mínima); **infactible**: una artificial queda > 0; **óptimos múltiples**: una no básica con costo reducido = 0; **degeneración**: una básica vale 0.

---

### Diapositiva 10 — DEMOSTRACIÓN EN VIVO · 🗣 Gabriel · ⏱ 4:30 (acum 12:40)

> "Ahora lo mostramos funcionando."

**Pasos del demo (en este orden):**

1. **La app ya debe estar corriendo y probada** (`.venv\Scripts\python.exe -m streamlit run app.py` → http://localhost:8501).
2. **Carga el preset "Wyndor Glass"** en *Cargar ejemplo*.
   > "Cargo el ejemplo que vimos: la función objetivo y las tres restricciones."
3. **Pulsa Resolver.** Muestra, en orden:
   - Los **tableros** del Simplex → "estas son las iteraciones, paso a paso; el óptimo llega en dos."
   - La **gráfica** → "la región factible y el óptimo en el vértice x₁=2, x₂=6."
   - La **sensibilidad** → "precios sombra y holguras; aquí se ven los cuellos de botella, las Plantas 2 y 3."
4. **Problema del profesor:**
   > "Profe, deme el problema que quiera y lo resuelvo aquí mismo."
   - Ajusta el número de **variables** y **restricciones**.
   - Ingresa coeficientes, tipo (≤/=/≥) y lado derecho.
   - **Resolver** y leer el resultado en voz alta.

> ⚠️ Si el profe da un problema de **2 variables**, aprovecha y muestra también la **gráfica**.
> ⚠️ Si es de más de 2, explica que la gráfica no aplica pero los **tableros** y la **sensibilidad** sí.
> ⚠️ Si el problema sale **infactible** o **no acotado**, dilo con naturalidad: "el programa lo detecta y lo reporta, es uno de los casos especiales".

---

### Diapositiva 11 — Conclusiones · 🗣 Gabriel · ⏱ 0:30 (acum 13:10)

> "Para cerrar: construimos un solver de Programación Lineal **completo**, que muestra el procedimiento **paso a paso**, no solo el resultado. Reúne **Simplex, Gran M, Revisado, gráfico y sensibilidad** en una sola herramienta, validada con pruebas y casos especiales. La idea es que el usuario se concentre en **analizar y decidir**, no en hacer los cálculos a mano. Muchas gracias, ¿alguna pregunta?"

---

## Checklist antes de exponer

- [ ] App **corriendo** y probada con el preset Wyndor **antes** de empezar (que no sorprenda un error).
- [ ] `diapositivas.html` abierto en el navegador, en **pantalla completa**, listo para proyectar.
- [ ] Acordar **quién maneja el computador** (Gabriel) y **quién avanza las slides 1–7** (Juan).
- [ ] Tener a mano el repo abierto: `github.com/gjcardonam/optimizacion-pl-udea`.
- [ ] Practicar **1 vez completo** cronometrando: Juan ~6 min, Gabriel ~7 min.
- [ ] Repasar `estudio.md` para responder preguntas del profe.

## Posibles preguntas del profe (y quién las responde)

**Teoría / métodos → responde Juan**
- **¿Por qué el óptimo está siempre en un vértice?** → "Por el Teorema Fundamental de la PL: si hay óptimo, hay uno en un vértice. La región factible es un poliedro convexo."
- **¿Por qué Gran M y no Dos Fases?** → "Gran M es directa, un solo modelo penalizado, logra la misma base inicial factible. Dos Fases evita el M grande pero usa dos pasos; nosotros priorizamos la simplicidad del motor."
- **¿Y si es no acotado?** → "En la razón mínima no hay ninguna razón positiva en la columna entrante; el programa lo identifica."
- **¿El Simplex siempre termina rápido?** → "En el peor caso teórico es exponencial (cubo de Klee–Minty), pero en la práctica converge en pocas iteraciones; Wyndor en 2. Y para la degeneración usamos la regla de Bland para que no se cicle."

**Sensibilidad / aplicación → responde Gabriel**
- **¿Qué es un precio sombra?** → "El cambio en Z por una unidad adicional del recurso de esa restricción. Formalmente, es la variable dual de esa restricción."
- **¿Qué pasa si es infactible?** → "Una variable artificial queda positiva en el óptimo; el programa lo detecta y lo reporta."
- **¿Hasta qué tamaño resuelve?** → "Hasta 8 variables y 10 restricciones, suficiente para problemas didácticos; el método es general."
- **¿Cómo validaron que está bien?** → "Con 12 pruebas automáticas contra resultados conocidos —Wyndor Z=36, precios sombra (0, 1.5, 1), rango [6, 18]— más los casos especiales."
