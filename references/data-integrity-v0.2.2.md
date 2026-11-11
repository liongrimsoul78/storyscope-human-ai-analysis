# Data integrity note — v0.2.2

> **Corrección v0.2.3:** este documento citaba la Tabla 15 para los valores numéricos. La transcripción correcta está en la **Tabla 16**; la Tabla 15 solo enumera las 13 características human-characterizing y sus opciones de respuesta. Se corrigen las referencias sin alterar los datos publicados.

## Finding

The v0.2.1 `feature-dimension-map.csv` contained five rows where `human_value_or_prevalence` and `ai_value_or_prevalence` were reversed, while `research_direction_or_option` and `paper_gap_human_minus_ai_or_note` indicated the correct Human − AI direction.

## Corrected values (Human / AI)

| Feature | Human | AI | Gap (Human − AI) |
|---|---:|---:|---:|
| Frequency of Direct Reader Address | 0.28 | 0.07 | +0.21 |
| Fourth-Wall Permeability | 0.67 | 0.39 | +0.28 |
| Location Variety Scope | 1.34 | 1.08 | +0.26 |
| Moral Polarity Toward Protagonist (ambivalent/mixed option) | 59% | 38% | +21 pp |
| Nonlinear Framing for Delayed Disclosure | 1.96 | 1.68 | +0.28 |

These values match Table 16 in version v6 of the paper. For the category-specific Moral Polarity row, the Human/AI values refer to the `ambivalent/mixed` option, not the entire distribution of moral-polarity categories.

## Source

Russell et al., *StoryScope: Investigating idiosyncrasies in AI fiction*, v6, **Table 16**, in the HTML rendering under the Human-elevated reader engagement, temporal complexity, and narrative diversity groups.

- Versioned HTML: https://arxiv.org/html/2604.03136v6
- Paper PDF: https://jenna-russell.github.io/assets/pdf/storyscope.pdf
- arXiv record: https://arxiv.org/abs/2604.03136

## Scope of this correction

Only the five numeric/prevalence pairs in `feature-dimension-map.csv` were changed in v0.2.2. The research directions, gaps, dimensions, clusters, cautions, qualitative rules, and calibration example were not changed. This correction does not add an AI detector or alter the scientific limits of the Skill.

**v0.2.3 addition:** a sixth data correction was found in `Reference Explicitness` (`balanced mix`). The published values are Human 37% / AI 16% / Gap +21; v0.2.2 had 16% / 37%. See `references/numeric-integrity-v0.2.3.md`.
