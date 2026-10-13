# SEVEN — EXTERNAL STRATUM SELECTION PROCEDURE v03

Status: REVIEW CANDIDATE / NOT FROZEN
Protocol: ../SEVEN_ANNOTATION_PROTOCOL_v03.md (sections 3.3, 9.4)

## Why this exists
The synthetic strata were written by people who know the categories. The external stratum is the only part of the corpus whose legibility was not produced by the scheme's authors. It is required for any verdict stronger than RETAINED (synthetic only): at least 8 units (P6).

## Who selects
A person who did not write the codebook definitions and did not write or edit any synthetic case. The author of the draft corpus and codebook (including the AI assistant that drafted them) does NOT qualify. The selector signs the declaration below. If the selector is also a rater, the selector is excluded from rating.

## What the selector may and may not know
Allowed to know: the seven names, and that passages should show a person acting. Not allowed to see: the synthetic cases, the codebook's rating scale, or the analyst key. The selector does not assign intended labels and does not communicate any guess to the analyst before the corpus is frozen.

## Selection rules
1. Sources: public domain in the EU and US (author died before 1955, or first published before 1930 and translator likewise in the public domain). Record edition, translator and URL.
2. Pre-list at least 24 candidate passages before choosing; record all of them, including rejected ones. Choose 8 or more by lot (seeded dice or a seeded script, seed recorded), not by taste. If a chosen passage fails a rule below, discard and draw the next one, and record why.
3. Passage: 60 to 180 words of continuous text or a condensed paraphrase of at most that length. Paraphrase must keep only actions, speech and facts, and drop the narrator's judgments and any named vice or virtue.
4. No category words or stems (see lint), no character names that would be recognisable to a lay reader (replace with a neutral label), no title or author in the text.
5. At least 3 different authors, at least 2 different languages of origin (read in English).
6. Intended labels: none are assigned by the selector. Intended labels for the external stratum remain empty in the key. External units enter the analysis through agreement among raters, not through a match to a label.
7. A paraphrased passage must be accompanied by the original excerpt in the provenance file so that fidelity can be audited.

## Declaration (selector)
I did not write the codebook definitions or any synthetic case. I did not see the synthetic cases or the analyst key before selecting.
Name / date / signature or commit:

## Files
- EXTERNAL_PROVENANCE_v03.csv: one row per candidate, including rejected ones.
- private/CORPUS_MASTER_v03.json: chosen passages are added with stratum "external", empty intended_primary, and a source_note.
