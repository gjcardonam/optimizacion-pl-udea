# Exposición — Trabajo Final Optimización

Material para sustentar el solver de Programación Lineal (límite del profe: **15 min máx**).

## Contenido

| Archivo | Para qué sirve |
|---|---|
| `diapositivas.md` | Las diapositivas (fuente, formato Marp). 11 slides. |
| `diapositivas.html` | **Las diapositivas para proyectar** — abrir en el navegador y usar pantalla completa. |
| `guion.md` | **Qué decir en cada diapositiva**, cronometrado (~13 min) + checklist y posibles preguntas. |
| `estudio.md` | Documentación teórica para **estudiar aparte** (PL, Simplex, Gran M, gráfico, sensibilidad, casos especiales). |

## Cómo presentar

1. **Demo primero, prepárala:** desde la raíz del repo, deja la app corriendo antes de empezar.
   ```bash
   .venv/bin/streamlit run app.py     # → http://localhost:8501
   ```
2. **Proyecta** `diapositivas.html`: ábrelo en el navegador y pasa a pantalla completa.
3. Sigue `guion.md` slide por slide. Plan de tiempo: ~8 min de diapositivas + ~5 min de demo.
4. En el demo: carga el preset **Wyndor Glass**, resuelve, muestra tableros / gráfico / sensibilidad,
   y luego resuelve **el problema que dé el profe**.

## Regenerar las diapositivas

Si editas `diapositivas.md`, vuelve a exportar el HTML:

```bash
npx -y @marp-team/marp-cli@latest diapositivas.md --html --allow-local-files -o diapositivas.html
```

> El tema usa fuentes de Google Fonts (Fraunces, Spline Sans, IBM Plex Mono), así que la
> exportación necesita **conexión a internet**.

La gráfica de la región factible (`docs/assets/grafico_wyndor_deck.png`, con la paleta del
tema) se regenera desde la raíz del repo con:

```bash
.venv/bin/python docs/build_deck_chart.py
```
