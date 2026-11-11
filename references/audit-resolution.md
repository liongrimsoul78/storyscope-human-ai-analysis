# Resolución de la auditoría v0.1.0 → v0.2.0

La auditoría reportó inconsistencias en la dirección temporal, la interpretación de ausencias, el doble conteo, el formato, el mapa de dimensiones y la adaptación al español. La versión 0.2.0 las aborda así:

| Hallazgo de auditoría | Resolución en v0.2.0 |
|---|---|
| Linealidad temporal llamada “contrapatrón humano” | Se prohíbe esa etiqueta. Los time-jumps explícitos pueden ser débilmente human-leaning en historias largas comparables; la secuencia lineal aislada no es decisiva. |
| Ausencia de sensorialidad/espacio/otros personajes contada como humana | Las ausencias no tienen dirección por defecto. En muestras breves se registran como no evaluables. |
| Regla asimétrica para ausencias | Se incluye una regla de simetría y una secuencia obligatoria de decisión. |
| Doble conteo de indicadores temáticos/espaciales/sensoriales | Se añaden ocho clústeres operativos de LION LAB. No son clústeres oficiales del artículo ni crean puntuación total. |
| Agency/resolución inferida sin resolución presente | Agency in Resolution y Mode of Resolution solo se evalúan si hay una resolución narrativa identificable. |
| Uso ambiguo de “contrapatrón” | Se elimina y se sustituye por los cinco estados de evidencia. |
| Fuerza asignada a ausencias | La fuerza se reserva para evidencia observada; ausencias quedan ausentes/no evaluables. |
| Conclusión global “mixta con inclinación IA” en 21 palabras | Se impone `evidencia insuficiente` para textos inferiores a 500 palabras y géneros inherentemente breves. El corte es una salvaguarda de LION LAB, no un umbral del estudio. |
| Secciones/orden del informe | La plantilla define siete secciones obligatorias y en orden. |
| Style duplicado con lenguaje superficial | Se exige separación de dimensión Style y pista superficial; no se puede contar una cita en ambas capas como evidencia independiente. |
| Sin mapa de rasgo a dimensión | Se crea `feature-dimension-map.csv` con 30 features únicas y los códigos de dimensión de las Tablas 14–15. |
| Recuento 30 no reproducible | Se explicitan 20 opciones AI + 13 opciones humanas y tres features repetidas con opciones distintas (emoción, referencia explícita, subtramas) = 30 features únicas. |
| Diferencias de magnitud no visibles | El CSV conserva medias/frecuencias y cautelas; la base científica aclara que medias no son umbrales. |
| Adaptación inglés–español insuficiente | Se añade `spanish-adaptation.md` con tiempo/aspecto, pro-drop, conectores, género, topoi y traducción. |
| Contraevidencia sin definición | Solo es un valor observado que apunta al polo contrario; nunca una mera ausencia. |
| Género como confusor | La puerta de entrada exige clasificar género y tipo de tarea antes de analizar. |
| Revelación/reencuadre del final del microrelato | El ejemplo señala que existe un cierre/reencuadre débil, pero no una sorpresa demostrada ni evidencia de autoría. |
| Recuento potencial 61.632 frente a 61.608 efectivo | La sección 2.1, nota 8, del artículo explica que los modelos rechazaron 24 historias. La suma efectiva es 10.272 historias humanas + 51.336 IA = 61.608. |
| Longitud media 4.753 frente a “~5.000” | 4.753 es el promedio exacto del corpus; ~5.000 es el redondeo del abstract. No son cifras incompatibles. |
| Variedad “español general” inferida | La plantilla y el protocolo ahora requieren `no especificada / no determinable` cuando el usuario no declara variedad y la muestra no permite establecerla. |

## Matiz importante sobre temporalidad

La auditoría acertó al rechazar que la linealidad de un microtexto se llame “contrapatrón humano”. La versión 0.2 añade precisión: en el estudio, las medias de discontinuidad cronológica y anacronía fueron mayores en el grupo humano, con diferencias modestas. Por ello, una historia larga comparable con saltos temporales explícitos puede mostrar una señal human-leaning débil; la linealidad común, por sí sola, no permite una conclusión global ni convierte la ausencia de flashbacks en prueba de IA.

## Qué no se añadió

- No se añadió un clasificador XGBoost ni pesos del estudio.
- No se añadieron porcentajes, probabilidades, thresholds estadísticos ni un detector autónomo.
- No se afirmó validez en español.
- No se copiaron corpus protegidos o historias humanas de Books3.
- No se modificó el repositorio local de LION LAB ni Identity v6.
