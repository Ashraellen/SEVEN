# SEVEN v03 — decisions and status (2026-10-13)

## Confirmed by the author
- Decision parameters P1-P14 (protocol §13) unchanged; the tier, outcome and control thresholds P3, P6, P7 and P11 were not softened. Minimum 5 raters.
- F4 (control over-labelling) is a diagnostic flag. It is reported but never drives the outcome.
- Decision statistic: Krippendorff's alpha on binary "central". AC1, pairwise agreement, PRIMARY statistics and bootstrap intervals are mandatory supplements.
- Private master, key, ID map, orders and salt stay outside the public repo (`research/.gitignore`). Before disclosure only the hashes (COMMITMENT_v03.json, at freeze) are published. Full schedule: protocol §14.
- External cases: selected independently (EXTERNAL_SELECTION_PROCEDURE_v03.md).

## Status
- Procedure, codebook, instruments, builder and analysis scripts: drafted; the scripts' built-in self-tests pass. Everything is still a review candidate, not frozen.
- Draft synthetic corpus: 56 analysis units + 4 practice, private. Lint: no hard failures, only warning is the empty external stratum.
- External stratum: EMPTY. Needs an independent selector.
- Order: independent audit (AUDIT_CHECKLIST_v03.md) -> pretest (C8) -> external stratum by an independent selector -> final check -> commitment and external timestamp -> FROZEN_MANIFEST_v03.md. Author confirmed this order on 2026-10-13.

## Known weaknesses of the draft corpus
- Written by an AI that had the category definitions in hand. Legibility is probably higher than for a naive author.
- A crude keyword-matching check guessed the intended category for 6 of 28 central cases (random guessing would give 4 of 28). That suggests the cases do not give themselves away by single words, but the check is weak and does not replace the independent audit.
- Central cases mostly share an "escalating behaviour with a stated rationalisation" form. A pretest should check whether raters recognise form rather than motive.
