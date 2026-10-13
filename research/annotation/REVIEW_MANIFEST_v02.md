# SEVEN — v02 REVIEW MANIFEST

Status: REVIEW CANDIDATE / NOT FROZEN
Date: 2026-10-13

This manifest records the candidate packet submitted for external methodological review.

Do not treat this as the final frozen manifest.

## Candidate files and current blob SHAs

- SEVEN_ANNOTATION_PROTOCOL_v02.md — 3b9c7bb5ea70868257aae13b0cc393fcae36a6d6
- CORPUS_MASTER_v02.json — 9429e2ab4f578bc8feb37dd296ca79cbd6819562
- CODER_CORPUS_v02.md — 41c09d78d19abd62f6a1b407655b07c2c61b4c99
- CORPUS_ANALYST_KEY_v02.md — e5ea935fd9d6b87d910df067fcc392c10776a273
- CODEBOOK_v02.md — 295db47a45f5647a5a8c9d8f18a49eb866bf9e1a
- RATINGS_TEMPLATE_v02.csv — 02ab843986f4857cf6f696de1b3a7ad3660525b9
- build_coder_packet.py — pending deterministic-shuffle update in this review batch

## Freeze condition

After external review and any accepted corrections:
1. refetch every file;
2. verify word lengths, category balance, leakage, CSV field count, and deterministic build output;
3. record the final Git commit SHA and final blob SHAs in FROZEN_MANIFEST_v02.md;
4. only then distribute the packet to raters.

Any substantive edit after freeze requires a new version or a documented new round.
