# SEVEN v03 — decisions and status (2026-10-13)

## Confirmed by the author
- P1-P14 unchanged (P3, P6, P7, P11 not softened). Minimum 5 raters.
- F4 (control over-labelling) is a diagnostic flag. It is reported but never drives the outcome.
- Decision statistic: Krippendorff's alpha on binary "central". AC1, pairwise agreement, PRIMARY statistics and bootstrap intervals are mandatory supplements.
- Private master, key, ID map, orders and salt stay outside the public repo (.gitignore). Only COMMITMENT_v03.json (hashes) is published before disclosure.
- External cases: selected independently (EXTERNAL_SELECTION_PROCEDURE_v03.md).

## Status
- Procedure, codebook, instruments, builder, analysis: done, selftests pass.
- Draft synthetic corpus: 56 analysis units + 4 practice, private. Lint: no hard failures, only warning is the empty external stratum.
- External stratum: EMPTY. Needs an independent selector.
- Order: independent audit (AUDIT_CHECKLIST_v03.md) -> pretest (C8) -> external stratum by an independent selector -> final check -> commitment and external timestamp -> FROZEN_MANIFEST_v03.md. Author confirmed this order on 2026-10-13.

## Known weaknesses of the draft corpus
- Written by an AI that had the category definitions in hand. Legibility is probably higher than for a naive author.
- Keyword baseline: 6/28 central cases guessed by a crude lexicon (chance is 4/28), which is low, but that is a weak test.
- Central cases mostly share an "escalating behaviour with a stated rationalisation" form. A pretest should check whether raters recognise form rather than motive.
