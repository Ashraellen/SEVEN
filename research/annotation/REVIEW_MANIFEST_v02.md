# SEVEN — v02 REVIEW MANIFEST

> **SUPERSEDED BY v03 / HISTORICAL / NOT A CURRENT INSTRUMENT.** This file is kept as development history only. Do not use it for rating, auditing or analysis. Current instrument: [v03 protocol](../SEVEN_ANNOTATION_PROTOCOL_v03.md). Explanation: [HISTORICAL_v01_v02.md](HISTORICAL_v01_v02.md).
> 
> The blob SHAs listed below were recorded before these historical banners were added; the banners change the blob SHAs of the .md files listed.

Status: SUPERSEDED BY v03 / HISTORICAL / NOT A CURRENT INSTRUMENT (previous status: REVIEW CANDIDATE / NOT FROZEN)
Date: 2026-10-13

This manifest records the current v02 packet for external methodological review.
It is not the final frozen manifest and must not be used as evidence that a rating round has started.

## Candidate files and blob SHAs

- research/SEVEN_ANNOTATION_PROTOCOL_v02.md — 3b9c7bb5ea70868257aae13b0cc393fcae36a6d6
- research/annotation/CORPUS_MASTER_v02.json — 9429e2ab4f578bc8feb37dd296ca79cbd6819562
- research/annotation/CODER_CORPUS_v02.md — 41c09d78d19abd62f6a1b407655b07c2c61b4c99
- research/annotation/CORPUS_ANALYST_KEY_v02.md — e5ea935fd9d6b87d910df067fcc392c10776a273
- research/annotation/CODEBOOK_v02.md — 295db47a45f5647a5a8c9d8f18a49eb866bf9e1a
- research/annotation/RATINGS_TEMPLATE_v02.csv — 02ab843986f4857cf6f696de1b3a7ad3660525b9
- research/annotation/build_coder_packet.py — 7460b056942b27d895a16e0bd316b8a59bffcc59

## Verified candidate properties

- 42 cases total.
- 28 central single-focus cases: exactly 4 per category.
- 14 mixed-mechanism cases.
- Case length range: 61–79 words.
- Coder packet uses neutral display IDs C01–C42.
- Coder packet contains no source, stratum, intended-label, GREED-chapter, Whitty, Stajano, or sunk-cost leakage.
- Analyst key is separate and explicitly not for raters.
- Ratings CSV has 14 fields in header and every data row.
- Stage A free motive description precedes Stage B category labels.
- Protocol, coder corpus, codebook, analyst key, ratings template, and build script are English-language research files.
- v02 remains NOT FROZEN.

## Freeze condition

After external review and accepted corrections:
1. refetch every file;
2. rerun structural validation;
3. record the final repository commit SHA and final blob SHAs in FROZEN_MANIFEST_v02.md;
4. only then distribute the packet to raters.

Any substantive edit after freeze requires a new version or a documented new round.
