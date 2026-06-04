# Guion de exposición — qué decir en cada diapositiva

**Tiempo total objetivo: ~13:40 min** (límite del profe: 15 máx).
Formato pedido en clase: *intro breve en diapositivas + demo en vivo del software*.

## Reparto

| Quién | Diapositivas | Tema | Tiempo |
|---|---|---|---|
| **Juan** | 1 – 7 | El problema y **todos los métodos de resolución** (Simplex, Gran M, gráfico) | ~6:40 |
| **Gabriel** | 8 – 11 | **Sensibilidad, la aplicación y la demo en vivo** + cierre | ~7:00 |

> El relevo es en la diapositiva 8. **Gabriel maneja el computador** en la demo, así que conviene que tenga el teclado desde el relevo. Juan avanza las slides 1–7.

> **Cómo usar este guion:** lo de las comillas es lo que dice esa persona — pero **no se lee, se cuenta**. Son los puntos para hablar con naturalidad; cada quien lo dice con sus palabras. Marquen con la voz los **términos en negrita** (los que el profe espera oír). Lo de "👉" son notas para ustedes, no se dicen.
>
> Está calibrado para hablar a ritmo cómodo (~130 palabras/min, con pausas para señalar la pantalla). Si se sienten apurados, bajen el ritmo: sobra margen hasta los 15 min.

---

## 🔵 JUAN — primera mitad (diapositivas 1–7)

### Diapositiva 1 — Portada · 🗣 Juan · ⏱ 0:25 (acum 0:25)

> "Buenos días a todos. Nuestro trabajo final es un programa que resuelve problemas de Programación Lineal, pero con una diferencia: no solo te da el resultado, sino que te muestra todo el procedimiento **paso a paso**, como lo haríamos a mano. Por dentro tiene cinco métodos. Yo les explico cómo funcionan, y al final Gabriel se los muestra corriendo en vivo."

👉 Directo, sin detenerse. Es el arranque.

---

### Diapositiva 2 — ¿Qué problema resolvemos? · 🗣 Juan · ⏱ 1:05 (acum 1:30)

> "Empecemos por el *para qué*. Piensen en cualquier empresa que tiene recursos limitados —digamos horas de máquina, materia prima, plata— y tiene que decidir cuánto producir de cada cosa para ganar lo máximo posible, pero sin pasarse de ninguno de esos límites. Ese es exactamente el tipo de problema que resuelve la **Programación Lineal**.
>
> Y siempre tiene las mismas tres piezas. Están las **decisiones**, que son las variables: cuánto hago de esto, cuánto de aquello. Está el **objetivo**, que es lo que queremos maximizar o minimizar, y tiene que ser una función lineal. Y están las **restricciones**, que son los límites, también lineales.
>
> Ese detalle de que todo sea *lineal* no es un capricho: es justo lo que hace que el problema se pueda resolver de forma exacta y rápida. Si metiéramos curvas o cosas más raras, ya sería un problema muchísimo más difícil."

👉 Si preguntan por qué lineal: porque hace que la región de soluciones sea un **poliedro convexo**, y eso es lo que lo vuelve manejable.

---

### Diapositiva 3 — Problema modelo · Wyndor Glass · 🗣 Juan · ⏱ 1:10 (acum 2:40)

> "Para no quedarnos en lo abstracto, vamos a usar un problema concreto que nos va a acompañar toda la presentación. Se llama **Wyndor Glass**, es un clásico de los libros de optimización. Una empresa fabrica dos productos, puertas y ventanas, y quiere **maximizar la utilidad**. El problema es que las dos compiten por el tiempo de **tres plantas**, que es limitado.
>
> Escrito como modelo queda así *(señalar la pantalla)*: maximizar Z igual a **3x₁ más 5x₂** —donde x₁ son los lotes de puertas y x₂ los de ventanas—, sujeto a las tres restricciones de las plantas, todas de tipo *menor o igual*, y claro, las cantidades no pueden ser negativas.
>
> La respuesta correcta, que ya se conoce del libro, es producir **2 lotes de puertas y 6 de ventanas**, para una utilidad de **36**. Y eso nos sirvió de prueba: nuestro programa llega a ese mismo 36 con todos los métodos, así supimos que estaba bien hecho."

👉 Wyndor es el ejemplo canónico de **Hillier & Lieberman**. Señala la formulación mientras hablas.

---

### Diapositiva 4 — Métodos implementados · 🗣 Juan · ⏱ 0:50 (acum 3:30)

> "Ahora, no hay un solo método para esto; depende del problema. Si todas las restricciones son *menor o igual*, usamos el **Simplex** normal. Si aparece alguna *mayor o igual* o una *igualdad*, ahí toca el método de la **Gran M**. Tenemos también el **Simplex Revisado**, que es la misma idea pero en versión matricial, y el método **gráfico** para cuando hay solo dos variables. Y al final, el **análisis de sensibilidad**.
>
> Lo bueno es que el usuario no tiene que saber cuál escoger: el programa lee las restricciones y **elige el método solo**. Y un dato: el Simplex no es nuevo, lo inventó **George Dantzig en 1947**, y setenta y cinco años después sigue siendo el más usado."

---

### Diapositiva 5 — Simplex, paso a paso · 🗣 Juan · ⏱ 1:20 (acum 4:50)

> "Vamos al corazón de todo, que es el **Simplex**. La idea es muy bonita: la zona de soluciones válidas siempre forma una especie de polígono, y se puede demostrar —es un teorema, el **teorema fundamental de la Programación Lineal**— que el mejor resultado **nunca está en el medio, siempre cae en una esquina**, en un vértice. O sea que en vez de revisar infinitos puntos, nos basta con recorrer las esquinas.
>
> Y el Simplex hace eso de forma inteligente: arranca en una esquina, mira las vecinas, y salta a la que mejora la ganancia. Repite hasta que ninguna vecina mejore, y ahí sabe que llegó al **óptimo**. Para hacerlo con números, le agrega unas variables de **holgura**, arma un **tablero**, y en cada paso decide qué variable entra, cuál sale, y recalcula.
>
> En Wyndor, miren *(señalar)*: sale del origen, salta a un vértice, después a otro, y en apenas **dos iteraciones** ya está en la solución. En el peor caso teórico podría tardar mucho, pero en la práctica converge rapidísimo; por eso es el método estrella."

👉 Si profundizan: el peor caso exponencial es el **cubo de Klee–Minty (1972)**; en la práctica son pocas iteraciones.

---

### Diapositiva 6 — Método de la Gran M · 🗣 Juan · ⏱ 1:00 (acum 5:50)

> "¿Y qué pasa cuando hay restricciones de tipo *mayor o igual* o de *igualdad*? El problema es que ahí el Simplex no tiene por dónde empezar, no encuentra esa esquina inicial fácil. La solución es la **Gran M**: metemos unas **variables artificiales**, que son como un andamio para poder arrancar, y las **castigamos** en el objetivo con un costo M gigante.
>
> Como son tan caras, el propio Simplex se encarga de **sacarlas** en el camino. Y aquí hay un detalle muy útil: si al final una de esas artificiales queda con valor positivo, eso nos está diciendo que el problema es **infactible**, que no tiene solución. Así, con un mismo motor, resolvemos también los problemas mezclados, con restricciones de todos los tipos."

👉 Si preguntan por qué Gran M y no Dos Fases: Gran M es directa, un solo modelo. Y para que no se cicle en casos degenerados usamos la **regla de Bland**.

---

### Diapositiva 7 — Método gráfico · 🗣 Juan · ⏱ 0:50 (acum 6:40)

> "Cuando el problema tiene solo **dos variables**, lo podemos dibujar, y el programa lo hace automáticamente. Cada restricción es una **recta**, y la zona donde se cumplen todas —el polígono sombreado— es la **región factible**. La línea punteada roja es la función objetivo: imagínensela deslizándose, y el último punto de la región que toca es la solución óptima; siempre, como dijimos, en una esquina.
>
> Esto sirve mucho para *ver con los ojos* por qué esa es la respuesta. Y con esto cierro la parte de cómo el programa resuelve. Les paso a Gabriel, que les muestra qué más nos dice la solución y la demostración en vivo."

👉 Cierra tranquilo y pásale la palabra (y el computador) a Gabriel.

---

## 🟣 GABRIEL — segunda mitad (diapositivas 8–11)

### Diapositiva 8 — Análisis de sensibilidad · 🗣 Gabriel · ⏱ 1:30 (acum 8:10)

> "Gracias, Juan. Bueno, ya tenemos la solución óptima. Pero en la vida real uno no se queda solo con el número; uno quiere saber qué tan **firme** es esa respuesta, qué pasaría si las cosas cambian un poco. Y lo interesante es que el mismo tablero final, **sin volver a calcular nada**, ya nos da esa información. Eso es el **análisis de sensibilidad**.
>
> Lo más importante son los **precios sombra**. Un precio sombra responde una pregunta muy concreta: si yo consiguiera *una unidad más* de un recurso, ¿cuánto me subiría la ganancia? O sea, cuánto vale la pena ampliar cada planta. Y va de la mano con las **holguras**: si a una restricción le sobra capacidad, su precio sombra es cero, no aporta; pero si está justo al tope, esa restricción es un **cuello de botella**.
>
> En Wyndor, por ejemplo, los precios sombra dan **cero, uno punto cinco, y uno**. ¿Y eso qué nos dice? Que la Planta 1 nos sobra, no es problema; pero las **Plantas 2 y 3 están saturadas**, son las que nos están frenando. Si quisiéramos producir más, ahí es donde habría que invertir, y empezaríamos por la Planta 2, que es la que más vale. El programa además calcula los **rangos**: cuánto pueden moverse los datos antes de que la solución cambie. Y un detalle para los que sepan del tema: estos precios sombra son lo que en optimización se llama el problema **dual** — no es un invento nuestro, sale de la teoría."

👉 Si preguntan por **costos reducidos**: para un producto que quedó en cero, es cuánto tendría que mejorar su ganancia para que valga la pena producirlo.

---

### Diapositiva 9 — La aplicación · 🗣 Gabriel · ⏱ 1:00 (acum 9:10)

> "Un momento sobre cómo está construido. El proyecto está organizado en **módulos**: hay una carpeta `solver` con el motor, donde cada método vive en su propio archivo, y encima una interfaz web hecha en **Streamlit**, que es lo que van a ver enseguida. Para asegurarnos de que todo funciona, escribimos **doce pruebas** automáticas que comparan los resultados contra valores ya conocidos, e incluyen los casos raros.
>
> Porque el programa no solo resuelve el caso bonito: también **detecta** cuando un problema no tiene solución, cuando se va a infinito, cuando hay varias soluciones óptimas, o cuando se pone degenerado. Y maneja hasta **ocho variables y diez restricciones**, maximizar o minimizar, y los tres tipos de restricción."

---

### Diapositiva 10 — DEMOSTRACIÓN EN VIVO · 🗣 Gabriel · ⏱ 4:00 (acum 13:10)

> "Y bueno, lo mejor es verlo funcionando, así que vamos a la demostración."

**Pasos del demo (en este orden):**

1. **La app ya debe estar corriendo y probada** (`.venv\Scripts\python.exe -m streamlit run app.py` → http://localhost:8501).
2. **Carga el preset "Wyndor Glass"** en *Cargar ejemplo*.
   > "Voy a cargar el mismo ejemplo que vimos: aquí está la función objetivo y las tres restricciones de las plantas."
3. **Pulsa Resolver** y ve mostrando, con calma, en este orden:
   - Los **tableros** → "estas son las iteraciones del Simplex, paso a paso; vean que llega al óptimo en dos."
   - La **gráfica** → "esta es la región factible, y el óptimo cae en el vértice x₁=2, x₂=6, justo como dijo Juan."
   - La **sensibilidad** → "y aquí los precios sombra y las holguras; se ve clarito que las Plantas 2 y 3 son los cuellos de botella."
4. **El problema del profesor:**
   > "Y para que vean que es general: profe, déme el problema que quiera y lo resolvemos aquí mismo."
   - Ajusta el número de **variables** y **restricciones**, ingresa los coeficientes, el tipo (≤/=/≥) y el lado derecho.
   - **Resolver** y leer el resultado en voz alta.

> 👉 Si el problema del profe tiene **2 variables**, aprovecha y muestra también la **gráfica**.
> 👉 Si tiene más de 2, di que la gráfica no aplica pero los **tableros** y la **sensibilidad** sí.
> 👉 Si sale **infactible** o **no acotado**, dilo con naturalidad: "miren, el programa lo detecta y lo reporta; es uno de los casos especiales que les comentábamos".

---

### Diapositiva 11 — Conclusiones · 🗣 Gabriel · ⏱ 0:35 (acum 13:45)

> "Y para cerrar: lo que logramos es un solver de Programación Lineal **completo**, que no solo te da la respuesta, sino que te muestra todo el camino, paso a paso. Junta los cinco métodos en una sola herramienta, está validado con pruebas, y maneja los casos especiales. Al final la idea es esa: que uno se dedique a **analizar y decidir**, y le deje las cuentas al programa. Muchas gracias, quedamos atentos a sus preguntas."

---

## Checklist antes de exponer

- [ ] App **corriendo** y probada con el preset Wyndor **antes** de empezar (que no sorprenda un error).
- [ ] `diapositivas.html` abierto en el navegador, en **pantalla completa**, listo para proyectar.
- [ ] Acordar que **Gabriel maneja el computador** y **Juan avanza las slides 1–7**.
- [ ] Tener a mano el repo abierto: `github.com/gjcardonam/optimizacion-pl-udea`.
- [ ] Ensayar **1 vez completo** cronometrando: Juan ~6:40, Gabriel ~7:00.
- [ ] Repasar `estudio.md` para responder preguntas del profe.

## Posibles preguntas del profe (y quién las responde)

**Teoría / métodos → responde Juan**
- **¿Por qué el óptimo está siempre en un vértice?** → "Por el teorema fundamental de la PL: si hay óptimo, hay uno en un vértice, porque la región factible es un poliedro convexo."
- **¿Por qué Gran M y no Dos Fases?** → "Gran M es directa, un solo modelo penalizado; logra la misma base inicial. Dos Fases evita el M grande pero usa dos pasos; preferimos la simplicidad."
- **¿Y si el problema es no acotado?** → "En la prueba de la razón mínima no queda ninguna razón positiva en la columna que entra; el programa lo detecta."
- **¿El Simplex siempre es rápido?** → "En el peor caso teórico es exponencial —el cubo de Klee–Minty—, pero en la práctica converge en pocas iteraciones; Wyndor en dos. Y para la degeneración usamos la regla de Bland para que no se cicle."

**Sensibilidad / aplicación → responde Gabriel**
- **¿Qué es exactamente un precio sombra?** → "El cambio en la ganancia por una unidad adicional del recurso de esa restricción. Formalmente es la variable dual de la restricción."
- **¿Qué pasa si es infactible?** → "Una variable artificial queda positiva en el óptimo; el programa lo detecta y lo reporta."
- **¿Hasta qué tamaño resuelve?** → "Hasta 8 variables y 10 restricciones, suficiente para problemas didácticos; el método en sí es general."
- **¿Cómo validaron que está bien?** → "Con 12 pruebas automáticas contra resultados conocidos: Wyndor Z=36, precios sombra (0, 1.5, 1), el rango [6, 18], más los casos especiales."
