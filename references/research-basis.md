# Base científica y límites de StoryScope — revisión v0.2.3

## Referencia principal

Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer y John Wieting. **“StoryScope: Investigating idiosyncrasies in AI fiction.”** COLM 2026; arXiv:2604.03136v6, versión revisada el 10 de agosto de 2026.

- Artículo: https://arxiv.org/abs/2604.03136
- HTML versionado: https://arxiv.org/html/2604.03136v6
- Repositorio oficial: https://github.com/jenna-russell/storyscope
- Taxonomía oficial: https://raw.githubusercontent.com/jenna-russell/storyscope/main/data/taxonomy.json

## Qué hace la investigación

StoryScope representa historias mediante plantillas narrativas estructuradas, compara textos de distintas fuentes escritos para el mismo prompt, induce características interpretables y aplica un clasificador supervisado. El objetivo central es estudiar decisiones discursivas/narrativas, no solo expresiones superficiales.

## Corpus y resultados descritos en la versión v6

- 10.272 prompts y 10.272 historias humanas de referencia.
- 51.336 narrativas generadas por IA y 61.608 historias efectivamente incluidas en el corpus (10.272 humanas + 51.336 IA); cada historia tiene 304 características extraídas.
- Cinco fuentes generativas: Claude, DeepSeek, Gemini, GPT y Kimi, según la versión del estudio.

### Reconciliación del recuento y longitud media

No hay contradicción aritmética entre los 10.272 prompts, seis fuentes potenciales y 61.608 historias efectivas. El máximo teórico sería 10.272 × 6 = 61.632 historias. Sin embargo, la sección 2.1 del artículo (nota 8) indica expresamente que los modelos se negaron a generar 24 historias. Por tanto, 61.632 − 24 = 61.608 historias efectivas. El artículo también declara 51.336 narrativas generadas por IA; sumadas a las 10.272 historias humanas dan el mismo total.

La longitud media exacta del corpus es **4.753 palabras por historia**, según la sección 2.1, nota 8. El resumen/abstract la redondea como “~5.000 palabras”. Usa 4.753 cuando se requiera precisión y “aproximadamente 5.000” cuando se resuma; no presentes 4.700 como cifra exacta.
- Diez dimensiones NarraBench y 304 features: 124 categóricas, 59 ordinales, 45 de escala, 44 binarias y 32 multiselección.
- Macro-F1 binario reportado: 93,2% con características narrativas; 68,4% para atribución de seis fuentes. El conjunto de 30 características core logra 84,8% en la tarea binaria. El modelo combinado narrativa+estilo alcanza 96,0%.

Estas cifras corresponden a clasificadores entrenados y evaluados dentro del protocolo/corpus de la investigación. No son probabilidades para un texto nuevo, no son el rendimiento de esta Skill y no se transfieren a español o no ficción.

## Sobre las 30 características centrales

Las Tablas 14 y 15 muestran 20 opciones/características elevadas para IA y 13 elevadas para humanos. Tres variables aparecen con opciones distintas en ambas tablas: `Dominant Emotional Expression`, `Reference Explicitness` y `Subplot Integration`. Por ello, las 33 filas de opciones se corresponden con 30 características únicas, tal como resume la Tabla 16. La tabla `feature-dimension-map.csv` conserva la dimensión publicada, las medias/frecuencias y una cautela interpretativa por variable.

**Precisión de fuentes:** la Tabla 15 enumera las 13 características core human-characterizing y sus opciones de respuesta; **no contiene** los valores Human/AI ni los gaps. Las medias, prevalencias y gaps de las 30 características están en la **Tabla 16**. Las diferencias aparentes entre algunos gaps publicados y la resta de los valores ya redondeados se documentan, sin alterar los datos, en `references/numeric-integrity-v0.2.3.md`.

Los grupos temáticos de la Tabla 16 son categorías interpretativas del artículo. Los ocho clústeres del archivo `cluster-map.md` son una organización operativa propia de LION LAB para no duplicar evidencia; no se deben presentar como clústeres oficiales.

## Qué significan las diferencias

- Para variables de escala 1–5 y ordinales, las cifras son medias de grupos del corpus.
- Para opciones categóricas/binarias, las cifras son prevalencias.
- El valor de gap es la diferencia humano menos IA tal como se presenta en la Tabla 16; pequeños gaps no deben convertirse en señales fuertes.
- Una media de grupo no es un umbral individual. No se debe clasificar una historia comparando mecánicamente su atributo con una media.
- Las opciones de una misma variable son alternativas dentro de una característica. Por ejemplo, `embodied` y `explicit labels` no son dos features independientes.
- La discontinuidad cronológica y la intensidad de anacronía son, en promedio, mayores en las historias humanas del corpus, pero sus diferencias son modestas (aprox. +0,28 y +0,27 en las escalas reportadas). No convierten una secuencia lineal en prueba de IA. La linealidad es común en ambos grupos.
- El valor `no subplots` fue más frecuente en IA (79%) que en humanos (57%) en el corpus; solo se codifica cuando la historia tiene longitud/completitud suficientes para afirmar que no presenta subtramas.

## Género y longitud

Las historias del corpus fueron extensas (promedio aproximado de 5.000 palabras). El artículo explica que textos cortos no dan margen suficiente para extraer rasgos narrativos finos. Por eso LION LAB aplica un guardrail interno: menos de 500 palabras o géneros inherentemente breves/contenidos = `evidencia insuficiente` a nivel global. El umbral de 500 palabras **no procede del paper**; es una política conservadora de esta Skill. Los cortes 500–999 y 1.000+ son igualmente operativos, no thresholds científicos.

## Lo que no debe extrapolarse

1. No usar 93,2%, 84,8% u otras métricas como probabilidad de autoría.
2. No afirmar validez equivalente en español: no se presenta aquí un corpus o modelo calibrado de español.
3. No asumir que los mismos rasgos se transfieren a informes, ensayos, correo, chat o textos médicos.
4. No inferir fraude, plagio, engaño, identidad, intención o procedencia de una persona a partir de patrones.
5. No asumir una huella estable de cada modelo actual; los fingerprints de modelos del estudio son resultado específico de su corpus y fecha.
6. No tratar MIT del repositorio como autorización para redistribuir corpus de terceros. Los textos Books3 no se incluyen en esta Skill.
7. No afirmar que esta Skill contiene los 304 features, pesos XGBoost o pipeline original.

## Fuentes primarias para las tablas

- Tablas 14–15: Appendix I, features core para IA/humanos, dimensiones y tipos de valor.
- Tabla 16: 30 features core, medias y frecuencias humano/IA y temas interpretativos.
- Apéndice C: fiabilidad de extracción y validación humana.
- Apéndice D: protocolo de clasificación y asignación de roles de features.
- Apéndice E: ablaciones por dimensión.

La tabla `feature-dimension-map.csv` transcribe los datos presentados en las Tablas 14–16 del artículo v6. Para cualquier reuso científico, consulta siempre la fuente primaria versionada.
