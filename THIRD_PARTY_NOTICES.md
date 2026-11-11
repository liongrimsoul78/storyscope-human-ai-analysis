# Third-Party Notices and Provenance

This repository is **StoryScope Human–AI Analysis**, an independent LION LAB
implementation and extension inspired by the StoryScope research framework.

It is **not** the official StoryScope repository, **not** an official release
of the StoryScope authors, and **not** endorsed by or affiliated with them.
Any errors, omissions, adaptations, or opinions in this repository belong to
LION LAB, not to the StoryScope authors.

## 1. Scientific source

Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, and John
Wieting. “StoryScope: Investigating idiosyncrasies in AI fiction.” COLM 2026.
arXiv:2604.03136 (version v6, revised 10 August 2026).

- Abstract: https://arxiv.org/abs/2604.03136
- Versioned HTML: https://arxiv.org/html/2604.03136v6
- DOI: https://doi.org/10.48550/arXiv.2604.03136
- arXiv record: https://arxiv.org/abs/2604.03136v6

### Paper license and provenance

The arXiv record for v6 identifies the paper's license as **CC0 1.0 Universal
(Public Domain Dedication)**, as shown by the license link on the arXiv
abstract page:

- https://creativecommons.org/publicdomain/zero/1.0/

That license status was verified against the arXiv abstract page for
arXiv:2604.03136v6. Copyright in the paper remains with its authors; CC0 waives
rights to the extent permitted by law. This repository does not claim
authorship of the paper, its taxonomy, its corpus, or its findings.

## 2. Official StoryScope repository

The official implementation is maintained by the paper's authors:

- Repository: https://github.com/jenna-russell/storyscope
- License: **MIT License**
- Copyright notice in that repository: Copyright (c) 2026 Jenna Russell

The official repository's MIT license applies to that repository. It does not
grant rights to redistribute third-party corpus material, and it does not make
this repository an official StoryScope release. See also the official taxonomy
referenced by the paper:

- https://raw.githubusercontent.com/jenna-russell/storyscope/main/data/taxonomy.json

## 3. Relationship to this repository

LION LAB's Skill:

- adapts selected narrative-analysis concepts into an independent qualitative
  workflow for OpenCode / Agent Skills;
- uses its own operational clusters, evidence states, adequacy gate, and report
  format, which are LION LAB contributions and not official StoryScope
  components;
- does **not** run the original StoryScope pipeline, XGBoost classifier, or
  feature-extraction code;
- does **not** reproduce the paper's scores as probabilities of authorship for
  any new text;
- is **not** a definitive detector of human or AI authorship.

The names “StoryScope” and the authors' names are used only for scientific
attribution and descriptive reference. No trademark claim or endorsement is
implied.

## 4. Material derived from Table 16

The following files contain material derived from, or transcribed from, the
StoryScope paper's **Table 16** (30 core narrative features with Human/AI
values, prevalences, and published gaps). The transcription was prepared by
LION LAB from the versioned paper and is validated against a literal
extraction:

- `validation/source_table16_v6.txt`
- `validation/table16_expected.json`
- `references/feature-dimension-map.csv`

These files also include LION LAB's own descriptive columns, dimension labels,
operational groupings, cautions, and validation metadata. LION LAB's original
compilation and transcription contribution is released under CC0 1.0 as
described in `LICENSE-DATA`, to the extent the underlying material is CC0.

If any transcription differs from the primary source, the versioned paper
prevails. Please report discrepancies rather than treating the transcription as
authoritative.

## 5. Material not included

This repository does **not** include, and does not grant rights to:

- the Books3 corpus, the 61,608-story corpus, human-written stories, or
  AI-generated story texts;
- XGBoost model weights, trained classifiers, embeddings, or checkpoints;
- `taxonomy.json` or the official 304-feature taxonomy file;
- the original feature-extraction pipeline, prompts, generation harness, or
  evaluation harness;
- any third-party dataset, model output, or asset not explicitly listed as
  LION LAB original work.

Obtain such material from its official source and under its own terms.

## 6. License mapping

| Material | Terms |
|---|---|
| Original LION LAB code and Skill instructions | MIT (`LICENSE`) |
| Original LION LAB documentation | CC BY 4.0 (`LICENSE-DOCS`) |
| LION LAB transcription/compilation of Table 16 material, to the extent the source is CC0 | CC0 1.0 (`LICENSE-DATA`) |
| StoryScope paper (Russell et al.) | CC0 1.0, per arXiv record |
| Official StoryScope repository | MIT, per that repository |
| Third-party corpus, taxonomy, weights, or other assets | Their own terms; not included here |

Scope note:

- `SKILL.md` is original LION LAB instruction text licensed under MIT
  (`LICENSE`).
- The remaining original LION LAB documentation is CC BY 4.0
  (`LICENSE-DOCS`).
- Transcribed Table 16 values retain the CC0 1.0 provenance of the StoryScope
  paper; LION LAB's CC0 dedication (`LICENSE-DATA`) applies to its
  transcription and compilation contribution and does not claim authorship of
  the paper.

Nothing in this repository's licenses applies to material owned by third
parties. Attribution and provenance are preserved so that users can consult the
primary sources directly.
