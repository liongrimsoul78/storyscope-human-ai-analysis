# Integridad numérica — v0.2.3

## Fuente y tablas

Fuente primaria: Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction*, arXiv:2604.03136v6, 10 de agosto de 2026.

- **Tabla 15**: enumera las **13 características core human-characterizing** y sus opciones de respuesta. No contiene medias, prevalencias ni gaps Human − AI.
- **Tabla 16**: contiene las **30 características core** con valores Human, AI y Gap, agrupadas por tema interpretativo. Es la fuente de los valores numéricos de `feature-dimension-map.csv`.
- **§4.1**: describe cualitativamente los mismos patrones y repite algunas prevalencias; no sustituye a la Tabla 16 para la transcripción completa.

La v0.2.2 citaba la Tabla 15 como fuente de los valores de las 30 características. La v0.2.3 corrige esa cita a la Tabla 16. Las referencias legítimas a la Tabla 15 se conservan cuando describen sus 13 características y opciones.

## Corrección adicional de `Reference Explicitness`

Durante la auditoría v0.2.3 se detectó que la fila `Reference Explicitness` tenía invertidos los valores de la opción `balanced mix`:

| Opción | Human correcto | AI correcto | Gap correcto |
|---|---:|---:|---:|
| `implicit echoes` | 50% | 72% | −22 |
| `balanced mix` | 37% | 16% | +21 |

La v0.2.2 tenía `balanced mix` como Human 16% / AI 37%. El artículo (§4.1) indica 37% “balanced mix” humano frente a 16% de la IA. La v0.2.3 corrige la fila. Los cinco valores corregidos en v0.2.2 siguen siendo correctos:

| Característica | Human | AI | Gap |
|---|---:|---:|---:|
| Frequency of Direct Reader Address | 0.28 | 0.07 | +0.21 |
| Fourth-Wall Permeability | 0.67 | 0.39 | +0.28 |
| Location Variety Scope | 1.34 | 1.08 | +0.26 |
| Moral Polarity Toward Protagonist (`ambivalent/mixed`) | 59% | 38% | +21 pp |
| Nonlinear Framing for Delayed Disclosure | 1.96 | 1.68 | +0.28 |

## Excepciones de redondeo documentadas

La Tabla 16 muestra los valores con el redondeo de la publicación. Al restar los valores mostrados, algunos gaps no coinciden exactamente con el gap publicado. **No se alteran los datos para forzar la resta.** Se conservan tanto los valores mostrados como el gap publicado, y la diferencia se documenta aquí y en `validation/table16_expected.json`. La Tabla 16 no documenta la causa de esas diferencias; por tanto, no se afirma que los gaps procedan de valores sin redondear.

| Característica | Opción | Gap publicado | Resta de valores mostrados | Tratamiento |
|---|---|---:|---:|---|
| Thematic Explicitness and Moralizing | — | −0.65 | 3.28 − 3.94 = −0.66 | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |
| Dominant Emotional Expression | embodied | −42 | 38% − 81% = −43 pp | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |
| Dominant Sensory Modalities | olfactory | −26 | 57% − 82% = −25 pp | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |
| Sensory Density | — | −0.26 | 3.66 − 3.93 = −0.27 | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |
| Opening Spatial Grounding | — | −0.20 | 2.12 − 2.33 = −0.21 | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |
| Subplot Integration | thematically parallel | +22 | 42% − 21% = +21 pp | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |
| Mode of Resolution | — | −21 | 27% − 47% = −20 pp | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |
| Depth of Recontextualization After Surprise | — | +0.34 | 3.28 − 2.95 = +0.33 | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |
| Dialogue-to-Narration Proportion | — | +0.24 | 2.95 − 2.70 = +0.25 | Los valores mostrados y el gap publicado se conservan; no se infiere la causa de la diferencia. |

## Validación

El comando principal en Windows es:

```powershell
py -3 .\validation\validate_feature_map.py
```

Comprueba:

- 30 filas y 30 nombres únicos;
- 33 opciones (tres características tienen dos opciones);
- valores Human y AI;
- dirección Human/AI y signo del gap;
- gaps publicados;
- las nueve excepciones de redondeo, con su resta aritmética y su nota.

El validador no inventa valores ni corrige datos por inferencia. Si un valor no coincide con la transcripción de la Tabla 16, falla.

### Verificación independiente de la fuente

`validation/check_source_table16.py` lee `validation/source_table16_v6.txt`, una extracción literal de la Tabla 16 del HTML versionado, y compara **cada característica y cada opción por nombre**, no solo un conjunto de triples Human/AI/Gap. Rechaza valores correctos asociados a la característica u opción equivocada y verifica las 30 características y las 33 opciones.

```powershell
py -3 .\validation\check_source_table16.py
```

Resultado esperado:

```text
PASS: 30 features and 33 options matched by name and value against source_table16_v6.txt; 0 mismatches.
```

## Límites

- No se dispone aquí del corpus, los pesos XGBoost ni el pipeline original.
- Las cifras son medias o prevalencias de grupo del corpus del artículo; no son umbrales individuales ni probabilidades de autoría.
- La adaptación al español sigue siendo exploratoria y no está validada estadísticamente.
