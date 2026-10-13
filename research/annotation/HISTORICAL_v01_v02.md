# SEVEN — v01 and v02: historical files

Status: HISTORICAL / NOT CURRENT INSTRUMENTS

The current instrument is **v03** (see [../README.md](../README.md) and [../SEVEN_ANNOTATION_PROTOCOL_v03.md](../SEVEN_ANNOTATION_PROTOCOL_v03.md)). This page explains what the older files are, so that nobody takes them for a current method. They stay in their original locations so that earlier links keep working.

## What each version was

| Version | What it was | Status today |
|---|---|---|
| v01 | Pilot: first protocol, codebook, a 28-unit pilot corpus and a ratings template, written to develop the method. Not a validation. | Superseded. |
| v02 | Review candidate: a 42-case packet prepared for external methodological review. It was never frozen and never given to raters. | Superseded by v03 after that review. |
| v03 | Current review candidate, not frozen, not yet deployed to raters. | Current. |

The v02 review found problems that v03 was designed to remove: non-blind first stage, fixed rater order, public analyst key, no controls and no external cases, no pre-specified decision rule. The table in section 2 of the v03 protocol lists them.

## Files

| File | Version | Note |
|---|---|---|
| research/SEVEN_ANNOTATION_PROTOCOL_v01.md | v01 | historical banner added |
| research/annotation/CODEBOOK_v01.md | v01 | historical banner added |
| research/annotation/CORPUS_v01.md | v01 | historical banner added |
| research/annotation/RATINGS_TEMPLATE_v01.csv | v01 | unchanged (a csv cannot carry a banner) |
| research/SEVEN_ANNOTATION_PROTOCOL_v02.md | v02 | historical banner added |
| research/annotation/CODEBOOK_v02.md | v02 | historical banner added |
| research/annotation/CODER_CORPUS_v02.md | v02 | historical banner added |
| research/annotation/CORPUS_ANALYST_KEY_v02.md | v02 | historical banner added; public on purpose, see below |
| research/annotation/CORPUS_MASTER_v02.json | v02 | unchanged (json); public on purpose, see below |
| research/annotation/RATINGS_TEMPLATE_v02.csv | v02 | unchanged (csv) |
| research/annotation/build_coder_packet.py | v02 | unchanged; builds only the v02 packet |
| research/annotation/REVIEW_MANIFEST_v02.md | v02 | historical banner added; its blob SHAs predate the banners |

## Why the v02 key and master are public

`CORPUS_ANALYST_KEY_v02.md` and `CORPUS_MASTER_v02.json` were published while v02 was out for review. v02 was then replaced and no rater has ever used it, so these files were disclosed deliberately as material of a retired version. They are not part of the blind v03 design and say nothing about v03 labels.

Consequences that v03 already takes into account:
- v02 case texts are treated as known: the v03 protocol (criterion C7) forbids carrying them into the analysis strata unrevised. They may be reused only as practice cases.
- Anyone who has read the v02 key is not a naive reader for v02 cases, which is another reason to keep v02 away from raters.

## Rule

Do not give any v01 or v02 file to a rater, auditor or description coder. Do not run `build_coder_packet.py` for a study. Use the v03 files only.
