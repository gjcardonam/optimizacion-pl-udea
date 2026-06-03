# Guion de exposición — qué decir en cada diapositiva

**Tiempo total objetivo: ~13 min** (límite del profe: 15 min máx).
Formato pedido en clase: *intro breve en diapositivas + demo en vivo del software*.

> Cómo usar este guion: cada bloque es lo que dices mientras esa diapositiva está en pantalla.
> No lo leas palabra por palabra; son tus puntos. Los tiempos son una guía para no pasarte.
> Marca con la voz los **términos en negrita** (son los que el profe espera oír).

---

### Diapositiva 1 — Portada · ⏱ 0:20 (acumulado 0:20)

> "Buenos días. Vamos a presentar nuestro trabajo final: un **solver de Programación Lineal** que resuelve **paso a paso**. Lo desarrollamos Gabriel, Tabares y Rodas. Implementa Simplex, Gran M, Simplex Revisado, método gráfico y análisis de sensibilidad."

*(Directo. No te detengas mucho aquí.)*

---

### Diapositiva 2 — ¿Qué problema resolvemos? · ⏱ 1:00 (acum 1:20)

> "La Programación Lineal aparece cuando una empresa tiene **recursos limitados** —tiempo de máquina, materia prima, dinero— y tiene que decidir **cuánto producir de cada cosa** para **ganar lo máximo posible** sin pasarse de ningún límite.
>
> Esas decisiones son las **variables**, x₁, x₂, etcétera. Lo que queremos optimizar es la **función objetivo**, que es lineal. Y los límites son las **restricciones**, también lineales.
>
> La pregunta de fondo siempre es la misma: *cuánto de cada cosa, para optimizar el objetivo, respetando todas las restricciones.* Nuestro software **automatiza** ese cálculo y, lo importante, lo muestra **paso a paso**."

---

### Diapositiva 3 — Problema modelo (Wyndor Glass) · ⏱ 1:10 (acum 2:30)

> "Para mostrarlo usamos un problema clásico, **Wyndor Glass**. La empresa produce dos productos —puertas y ventanas— y quiere **maximizar la utilidad**, pero está limitada por el tiempo disponible en **tres plantas**.
>
> La formulación queda así: maximizar Z = **3x₁ + 5x₂**, sujeto a las tres restricciones de planta, todas de tipo *menor o igual*, y las variables no negativas.
>
> La solución óptima es x₁ = 2, x₂ = 6, con **Z igual a 36**. Y esto está verificado por todos los métodos del programa, no solo por uno."

*(Señala la formulación en pantalla mientras hablas.)*

---

### Diapositiva 4 — Métodos implementados · ⏱ 0:40 (acum 3:10)

> "El programa no implementa un solo método, sino una familia. **Simplex tabular** cuando todas las restricciones son *menor o igual*. **Gran M** cuando hay *mayor o igual* o *igualdad*. El **Simplex Revisado**, que es la misma idea pero en forma **matricial**. El **método gráfico** para dos variables. Y el **análisis de sensibilidad** al final.
>
> Lo bueno es que **el programa elige el método solo**, según el tipo de restricciones que uno ingrese."

---

### Diapositiva 5 — Simplex paso a paso · ⏱ 1:10 (acum 4:20)

> "La idea del **Simplex** es moverse de **vértice a vértice** de la región factible, mejorando el objetivo en cada paso.
>
> Primero se pasa a **forma estándar**, agregando una variable de **holgura** a cada restricción. Se arma el **tablero inicial**. Luego, en cada iteración: se escoge la **variable entrante** —la de mejor costo reducido—, se escoge la **variable saliente** con la **prueba de la razón mínima**, y se **pivotea**. Se repite hasta que ningún costo reducido mejore: ahí está el **óptimo**.
>
> En Wyndor, el programa llega al óptimo en **dos iteraciones**, mostrando los tres tableros."

---

### Diapositiva 6 — Gran M · ⏱ 0:50 (acum 5:10)

> "Cuando hay restricciones de tipo *mayor o igual* o *igualdad*, no tenemos una base inicial fácil. Ahí entra la **Gran M**: se agregan **variables artificiales** para arrancar, y se **penalizan** en el objetivo con un costo **M** muy grande.
>
> El Simplex, al optimizar, **expulsa** esas artificiales. Si al final alguna queda con valor positivo, significa que el problema es **infactible**. Así un mismo motor resuelve también los problemas con restricciones mixtas."

---

### Diapositiva 7 — Método gráfico · ⏱ 0:50 (acum 6:00)

> "Para problemas de **dos variables**, el programa además **dibuja** la solución. Grafica cada restricción como una recta, sombrea la **región factible** —que es la intersección de todas— y marca el **punto óptimo**, que siempre cae en un **vértice** de esa región.
>
> Esta gráfica la genera automáticamente. Sirve mucho para *ver* geométricamente por qué esa es la respuesta."

*(Apunta a la imagen de la región factible.)*

---

### Diapositiva 8 — Análisis de sensibilidad · ⏱ 1:10 (acum 7:10)

> "El análisis de sensibilidad responde qué tan **robusta** es la solución.
>
> Los **precios sombra** dicen cuánto cambiaría Z si tuviéramos **una unidad más** de un recurso; es decir, cuánto vale conseguir más de ese recurso. Las **holguras** son la capacidad que sobra: una restricción con holgura **cero** es un **cuello de botella**. Los **costos reducidos** dicen cuánto tendría que mejorar un producto que no estamos usando para que valga la pena producirlo. Y los **rangos** indican cuánto puede variar cada coeficiente sin que cambie la solución base."

---

### Diapositiva 9 — La aplicación · ⏱ 1:00 (acum 8:10)

> "En cuanto a la construcción, el proyecto tiene una **arquitectura modular**: una carpeta `solver` con el motor —cada método en su archivo—, la interfaz web hecha en **Streamlit**, y una suite de **doce pruebas** automáticas que incluyen los casos especiales.
>
> Soporta de **2 a 8 variables** y hasta **10 restricciones**, maximización o minimización, y los tres tipos de restricción. Y detecta los **casos especiales**: problema **no acotado**, **infactible** y **óptimos múltiples**."

---

### Diapositiva 10 — DEMO EN VIVO · ⏱ 4:30 (acum 12:40)

> "Ahora lo mostramos funcionando."

**Pasos del demo (en este orden):**

1. **Abre la app** (ya debe estar corriendo: `.venv/bin/streamlit run app.py`).
2. **Carga el preset "Wyndor Glass"** en el selector *Cargar ejemplo*.
   > "Cargo el ejemplo que vimos. Aquí está la función objetivo y las tres restricciones."
3. **Pulsa Resolver.** Muestra, en orden:
   - Los **tableros** del Simplex → "estas son las iteraciones, paso a paso."
   - La **gráfica** → "la región factible y el óptimo en el vértice x₁=2, x₂=6."
   - La **sensibilidad** → "precios sombra y holguras; aquí se ven los cuellos de botella."
4. **Problema del profesor:**
   > "Profe, deme el problema que quiera y lo resuelvo aquí mismo."
   - Ajusta el número de **variables** y **restricciones**.
   - Ingresa coeficientes, tipo (≤/=/≥) y lado derecho.
   - **Resolver** y leer el resultado en voz alta.

> ⚠️ Si el profe da un problema de **2 variables**, aprovecha y muestra también la **gráfica**.
> ⚠️ Si es de más de 2, explica que la gráfica no aplica pero los **tableros** y la **sensibilidad** sí.

---

### Diapositiva 11 — Conclusiones · ⏱ 0:30 (acum 13:10)

> "Para cerrar: construimos un solver de Programación Lineal **completo**, que muestra el procedimiento **paso a paso**, no solo el resultado. Reúne Simplex, Gran M, Revisado, gráfico y sensibilidad en una sola herramienta, validada con pruebas y casos especiales. La idea es que el usuario se concentre en **analizar y decidir**, y no en hacer los cálculos a mano. Muchas gracias, ¿alguna pregunta?"

---

## Checklist antes de exponer

- [ ] App **corriendo** y probada con el preset Wyndor **antes** de empezar (que no sorprenda un error).
- [ ] Diapositivas exportadas a PDF (ver `EXPOSICION/README.md`) por si falla Marp.
- [ ] Tener a mano el repo abierto: `https://github.com/gjcardonam/optimizacion-pl-udea`.
- [ ] Practicar el demo 1 vez completo cronometrando: slides ~8 min, demo ~5 min.
- [ ] Repasar `EXPOSICION/estudio.md` para responder preguntas del profe.

## Posibles preguntas del profe (respuestas cortas)

- **¿Por qué Gran M y no Dos Fases?** → "La Gran M es directa, un solo modelo penalizado; logra la misma base inicial factible. El proyecto lo resuelve en un solo paso del motor."
- **¿Qué pasa si es infactible?** → "Una variable artificial queda positiva en el óptimo; el programa lo detecta y lo reporta."
- **¿Y si es no acotado?** → "En la prueba de la razón mínima no hay razón positiva en la columna entrante; el programa lo identifica."
- **¿Qué es un precio sombra?** → "El cambio en Z por una unidad adicional del recurso de esa restricción."
- **¿Hasta qué tamaño resuelve?** → "Hasta 8 variables y 10 restricciones, suficiente para problemas didácticos; el método es general."
