# Resolución de segunda auditoría — StoryScope v0.2.1

## Alcance

La segunda auditoría de OpenCode volvió a inspeccionar la instalación v0.1.0 y confirmó los hallazgos metodológicos ya tratados en v0.2.0. Añadió tres observaciones de consistencia: recuento 61.608 frente al máximo teórico 61.632; 4.753 frente a ~5.000 palabras; y la inferencia no sustentada de “español general”. Esta revisión no vuelve a auditar la instalación local ni afirma que OpenCode ya esté usando v0.2.1.

## Resolución contrastada con la fuente primaria

1. **61.608 vs 61.632.** El máximo teórico es 10.272 prompts × seis fuentes = 61.632. La sección 2.1, nota 8, del artículo v6 declara que los modelos rechazaron generar 24 historias. El total efectivo es 61.608. El propio artículo indica 51.336 historias IA; 10.272 humanas + 51.336 IA = 61.608. No es un error aritmético, sino 24 generaciones ausentes por rechazo.
2. **4.753 vs ~5.000.** La sección 2.1, nota 8, da una media exacta de 4.753 palabras en el corpus de 61.608 historias. El abstract redondea a ~5.000. En documentación se usa 4.753 para precisión y ~5.000 para resumen; no 4.700 como exacto.
3. **Variedad lingüística.** Un texto sin regionalismos marcados no permite declarar “español general”. Si la variedad no fue especificada por el autor/usuario y no puede determinarse de manera suficiente, se registra `no especificada / no determinable`.

## Cambios en v0.2.1

- `SKILL.md`: obliga a no inferir dialecto/variedad; amplía el auto-chequeo; precisa la media del corpus.
- `research-basis.md`: añade la reconciliación de historias y longitud.
- `spanish-adaptation.md`: añade protocolo para variedades no declaradas.
- `report-template.md`: añade instrucción explícita en el campo idioma/variedad.
- `worked-examples/01-microrelato-21-palabras.md`: fija variedad como no especificada/no determinable.
- `CHANGELOG.md`, `README.md` y `audit-resolution.md`: registran el cambio.

## Fuentes primarias

Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction*, arXiv:2604.03136v6 (10 Aug 2026):
- Abstract: corpus reportado como 61.608 historias, aproximadamente 5.000 palabras.
- Sección 2.1, nota 8: media exacta de 4.753 palabras y 24 historias que los modelos rechazaron generar.
- Sección 2.1: 10.272 historias humanas originales y cinco fuentes generativas.

https://arxiv.org/html/2604.03136v6

## Límites

Esta resolución corrige documentación y reglas cualitativas. No incorpora clasificador, corpus en español, umbral científico, nuevas métricas ni validación estadística de la adaptación al español. El umbral de 500 palabras sigue siendo una salvaguarda de LION LAB, no un resultado de los autores.
