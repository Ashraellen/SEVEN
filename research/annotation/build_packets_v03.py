#!/usr/bin/env python3
"""SEVEN annotation toolkit v03 - packet builder.  Python 3.8+, standard library only.

Subcommands
  salt          print a fresh random salt (keep it private until the round closes)
  lint          check a master corpus against the corpus acceptance criteria (C1-C7)
  build         build per-rater two-round packets, private analyst files, commitment
  descriptions  turn locked Round A sheets into blinded description-coding sheets
  verify        recompute the commitment after reveal
  selftest      run internal consistency checks on a tiny synthetic corpus

Master corpus format (JSON):
  {"schema_version": "v03", "cases": [
     {"id": "M001", "text": "...", "stratum": "central|mixed|control|other|external|practice",
      "intended_primary": ["ENVY"], "intended_secondary": [], "source_note": "...",
      "feedback": "(practice cases only) how the definitions were meant to apply"} ]}
v02 field names (primary_intended / secondary_intended, synthetic-central / synthetic-mixed)
are accepted.

The master corpus, KEY.csv, ID_MAP.json, ORDERS.json and the salt must stay out of any
public repository until the round closes.  Publish COMMITMENT_v03.json instead.
"""
import argparse
import csv
import hashlib
import json
import math
import re
import secrets
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

TOOL_VERSION = "build_packets_v03/1"
CATEGORIES = ["PRIDE", "GREED", "LUST", "ENVY", "GLUTTONY", "WRATH", "SLOTH_ACEDIA"]
ANALYSIS_STRATA = ["central", "mixed", "control", "other", "external"]
ALL_STRATA = ANALYSIS_STRATA + ["practice"]
STRATUM_ALIASES = {"synthetic-central": "central", "synthetic-mixed": "mixed"}
ROUND_B_FIELDS = CATEGORIES + ["PRIMARY", "OTHER", "UNCLEAR", "CONFIDENCE", "COMMENT"]
MAX_ORDER_ATTEMPTS = 20000

# ---------------------------------------------------------------- lint constants
LABEL_RE = re.compile(
    r"\b(pride|greed|lust|envy|gluttony|wrath|sloth|acedia|deadly sins?|seven sins?|capital vices?)\b",
    re.I,
)
STEM_RE = re.compile(
    r"\b(proud|greedy|lustful|envious|envied|gluttonous|wrathful|slothful|sinful|vice|vices)\b", re.I
)
META_RE = re.compile(
    r"\b(either label|both (labels|mechanisms|motives)|the case is (about|not)|the issue is not|"
    r"cannot be (reduced|attributed)|hard to (decide|say)|difficult to (separate|disentangle|tell)|"
    r"inseparable|mutually reinforc\w*|reinforce[sd]? (each other|one another)|support one another|"
    r"intertwined|point(s)? toward the same|captures only part|this is (about|not about)|"
    r"the (core|real|underlying) (motive|issue|mechanism|problem)|the pattern is driven|"
    r"motivation (is|was) (not|less)|comparison supplies)\b",
    re.I,
)
ABSTRACT_RE = re.compile(
    r"\b(mechanism|motive|motivation|driven by|reinforc\w*|intertwin\w*|inseparable|rather than|"
    r"not about|the issue|the case|label|captur\w*|evidence (that|in (her|his|their) mind))\b",
    re.I,
)
SIG_TERMS = {
    "PRIDE": ["self-image", "standing", "dignity", "superior", "humiliat", "status", "rank"],
    "GREED": ["enough", "recover", "accumulat", "acquir", "resources"],
    "LUST": ["erotic", "sexual", "pursuit", "access"],
    "ENVY": ["compar", "advantage"],
    "GLUTTONY": ["beyond", "sensory", "consum", "gratif"],
    "WRATH": ["retaliat", "punish", "retribution", "insult"],
    "SLOTH_ACEDIA": ["avoid", "withdraw", "disengag", "confront"],
}
GUESS_LEXICON = {
    "ENVY": ["compar", "peer", "colleague", "classmate", "announce", "behind", "gap", "ahead", "inferior", "advantage"],
    "GREED": ["money", "debt", "invest", "profit", "wealth", "target", "savings", "return", "borrow", "acquire", "cash", "loan"],
    "LUST": ["sexual", "erotic", "attract", "desire", "pursu", "romantic", "intimate"],
    "GLUTTONY": ["dessert", "reward", "consum", "swip", "sensory", "taste", "serving", "portion", "stimulation", "clip"],
    "WRATH": ["retaliat", "humiliat", "punish", "embarrass", "hostile", "revenge", "insult", "angry", "anger"],
    "SLOTH_ACEDIA": ["avoid", "postpon", "delay", "unopened", "untouched", "procrastin", "withdraw"],
    "PRIDE": ["status", "image", "rank", "authority", "standing", "credit", "legacy", "authorship", "subordinate", "admission"],
}
REQUIRED_MIXED_PAIRS = [
    ("ENVY", "PRIDE"), ("GREED", "WRATH"), ("WRATH", "LUST"), ("LUST", "GLUTTONY"),
    ("SLOTH_ACEDIA", "WRATH"), ("GREED", "ENVY"), ("PRIDE", "SLOTH_ACEDIA"), ("GLUTTONY", "GREED"),
]
REQUIRED_MIN = {"central_per_category": 4, "mixed": 16, "control": 8, "other": 4, "external": 8, "practice": 4}


# ---------------------------------------------------------------- utilities
def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def sha256_text(s):
    return sha256_bytes(s.encode("utf-8"))


def words(text):
    return len(text.split())


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path, obj):
    write_text(path, json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- deterministic PRNG
def _stream(seed):
    ctr = 0
    seedb = seed.encode("utf-8")
    while True:
        d = hashlib.sha256(seedb + b"|" + ctr.to_bytes(8, "big")).digest()
        for i in range(0, 32, 8):
            yield int.from_bytes(d[i:i + 8], "big")
        ctr += 1


def _randbelow(stream, n):
    limit = (1 << 64) - ((1 << 64) % n)
    while True:
        x = next(stream)
        if x < limit:
            return x % n


def shuffled(items, seed):
    s = _stream(seed)
    out = list(items)
    for i in range(len(out) - 1, 0, -1):
        j = _randbelow(s, i + 1)
        out[i], out[j] = out[j], out[i]
    return out


# ---------------------------------------------------------------- master corpus
def load_master(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cases = []
    seen = set()
    for c in data["cases"]:
        stratum = STRATUM_ALIASES.get(c.get("stratum"), c.get("stratum"))
        prim = c.get("intended_primary", c.get("primary_intended")) or []
        sec = c.get("intended_secondary", c.get("secondary_intended")) or []
        prim = [prim] if isinstance(prim, str) else list(prim)
        sec = [sec] if isinstance(sec, str) else list(sec)
        cid = c["id"]
        if cid in seen:
            raise SystemExit(f"duplicate master id {cid}")
        seen.add(cid)
        if stratum not in ALL_STRATA:
            raise SystemExit(f"{cid}: unknown stratum {stratum!r}")
        for x in prim + sec:
            if x not in CATEGORIES:
                raise SystemExit(f"{cid}: unknown category {x!r} in intended labels")
        text = c["text"].strip()
        if not text:
            raise SystemExit(f"{cid}: empty text")
        cases.append({
            "id": cid, "text": text, "stratum": stratum, "intended_primary": prim,
            "intended_secondary": sec, "source_note": c.get("source_note", ""),
            "feedback": c.get("feedback", ""),
        })
    return cases


def assign_display_ids(cases, salt):
    analysis = sorted((c["id"] for c in cases if c["stratum"] != "practice"))
    n = len(analysis)
    width = max(2, len(str(n)))
    order = shuffled(analysis, f"{salt}|ids")
    mapping = {f"C{i + 1:0{width}d}": mid for i, mid in enumerate(order)}
    practice = [c["id"] for c in cases if c["stratum"] == "practice"]
    for i, mid in enumerate(practice):
        mapping[f"P{i + 1}"] = mid
    return mapping


def order_ok(order, strata, max_run=4):
    run = 1
    for a, b in zip(order, order[1:]):
        run = run + 1 if strata[a] == strata[b] else 1
        if run > max_run:
            return False
    n = len(order)
    for s in set(strata[i] for i in order):
        total = sum(1 for i in order if strata[i] == s)
        for t in range(3):
            lo, hi = t * n // 3, (t + 1) * n // 3
            cnt = sum(1 for i in order[lo:hi] if strata[i] == s)
            if abs(cnt - total * (hi - lo) / n) > 1.0:
                return False
    return True


def make_order(display_ids, strata_by_display, salt, rater, rnd):
    for attempt in range(MAX_ORDER_ATTEMPTS):
        cand = shuffled(display_ids, f"{salt}|order|{rater}|{rnd}|{attempt}")
        if order_ok(cand, strata_by_display):
            return cand, attempt
    raise SystemExit(f"no acceptable order for {rater} round {rnd} after {MAX_ORDER_ATTEMPTS} attempts")


# ---------------------------------------------------------------- lint
def lint(cases, v02_texts=None):
    """Return (hard_failures, warnings, info) lists of strings."""
    hard, warn, info = [], [], []
    for c in cases:
        m = LABEL_RE.search(c["text"])
        if m:
            hard.append(f"C1 {c['id']}: contains label word {m.group(0)!r}")
        if STEM_RE.search(c["text"]):
            warn.append(f"C1 {c['id']}: contains label-stem word {STEM_RE.search(c['text']).group(0)!r}")
    strata_n = Counter(c["stratum"] for c in cases)
    info.append("strata: " + ", ".join(f"{s}={strata_n.get(s, 0)}" for s in ALL_STRATA))
    for c in cases:
        w = words(c["text"])
        if not 60 <= w <= 180:
            warn.append(f"C2 {c['id']}: {w} words (need 60-180)")
    ws = sorted(words(c["text"]) for c in cases if c["stratum"] != "practice")
    if ws:
        q1, q3 = ws[len(ws) // 4], ws[(3 * len(ws)) // 4]
        info.append(f"words: min {ws[0]}, median {ws[len(ws) // 2]}, max {ws[-1]}, IQR {q3 - q1}")
        if q3 - q1 < 20:
            warn.append(f"C2 length uniformity: interquartile range of word counts is {q3 - q1} (<20)")
    sc = Counter(len(sentences(c["text"])) for c in cases if c["stratum"] != "practice")
    if sc:
        mode, mode_n = sc.most_common(1)[0]
        share = mode_n / sum(sc.values())
        info.append(f"sentences per case: {dict(sorted(sc.items()))}")
        if share > 0.65:
            warn.append(f"C2 form uniformity: {share:.0%} of cases have {mode} sentences (>65%)")
    meta_hits = [c["id"] for c in cases if META_RE.search(c["text"])]
    if meta_hits:
        warn.append(f"C3 narrator-commentary phrases in {len(meta_hits)} case(s): {', '.join(meta_hits)}")
    abs_hits = [c["id"] for c in cases if c["stratum"] != "practice" and ABSTRACT_RE.search(sentences(c["text"])[-1])]
    non_prac = sum(1 for c in cases if c["stratum"] != "practice")
    if non_prac:
        share = len(abs_hits) / non_prac
        info.append(f"final sentence abstract/mechanism-naming (heuristic): {len(abs_hits)}/{non_prac}")
        if share > 0.15:
            warn.append(f"C3 {share:.0%} of final sentences look abstract (>15%): {', '.join(abs_hits)}")
    central = [c for c in cases if c["stratum"] == "central" and c["intended_primary"]]
    if central:
        reuse = [c["id"] for c in central
                 if any(t in c["text"].lower() for t in SIG_TERMS[c["intended_primary"][0]])]
        share = len(reuse) / len(central)
        info.append(f"central cases reusing a signature term of their own category: {len(reuse)}/{len(central)}")
        if share > 0.60:
            warn.append(f"C4 {share:.0%} of central cases reuse own-category signature terms (>60%)")
        top1 = 0
        for c in central:
            t = c["text"].lower()
            sc2 = {k: sum(t.count(w) for w in ws2) for k, ws2 in GUESS_LEXICON.items()}
            best = max(sc2, key=lambda k: sc2[k])
            top1 += best == c["intended_primary"][0]
        info.append(f"keyword-baseline top-1 accuracy on central cases (crude heuristic): {top1}/{len(central)}")
    per_cat = Counter(c["intended_primary"][0] for c in central)
    for cat in CATEGORIES:
        if per_cat.get(cat, 0) != REQUIRED_MIN["central_per_category"]:
            warn.append(f"stratum: central cases for {cat} = {per_cat.get(cat, 0)} (protocol: {REQUIRED_MIN['central_per_category']})")
    for s in ("mixed", "control", "other", "external", "practice"):
        if strata_n.get(s, 0) < REQUIRED_MIN[s]:
            warn.append(f"stratum: {s} = {strata_n.get(s, 0)} (protocol minimum {REQUIRED_MIN[s]})")
    pairs = set()
    for c in cases:
        if c["stratum"] == "mixed":
            for p in c["intended_primary"]:
                for s2 in c["intended_secondary"]:
                    pairs.add(frozenset((p, s2)))
    missing = [f"{a}+{b}" for a, b in REQUIRED_MIXED_PAIRS if frozenset((a, b)) not in pairs]
    if missing:
        warn.append("C6 required mixed pairs missing: " + ", ".join(missing))
    for c in cases:
        if c["stratum"] == "control" and (c["intended_primary"] or c["intended_secondary"]):
            warn.append(f"stratum: control case {c['id']} has intended labels")
        if c["stratum"] in ("central", "mixed") and not c["intended_primary"]:
            hard.append(f"stratum: {c['id']} ({c['stratum']}) has no intended primary")
        if c["stratum"] == "practice" and not c["feedback"]:
            hard.append(f"practice case {c['id']} has no feedback text")
    if v02_texts is not None:
        for c in cases:
            if c["stratum"] != "practice" and sha256_text(c["text"]) in v02_texts:
                hard.append(f"C7 {c['id']}: identical to a v02 case (intended label is public)")
    return hard, warn, info


def cmd_lint(args):
    cases = load_master(args.master)
    v02 = None
    if args.v02_master:
        v02 = {sha256_text(c["text"]) for c in load_master(args.v02_master)}
    hard, warn, info = lint(cases, v02)
    lines = ["# SEVEN corpus lint (v03)", "", f"master: {args.master}", ""]
    lines += ["## Info"] + [f"- {x}" for x in info] + [""]
    lines += ["## Hard failures"] + ([f"- {x}" for x in hard] or ["- none"]) + [""]
    lines += ["## Warnings"] + ([f"- {x}" for x in warn] or ["- none"]) + [""]
    lines += ["Lint is a heuristic aid. It does not replace the pretest or independent review."]
    out = "\n".join(lines) + "\n"
    print(out)
    if args.report:
        write_text(Path(args.report), out)
    if hard or (args.strict and warn):
        return 1
    return 0


# ---------------------------------------------------------------- build
def case_md(display_id, text, tag=""):
    return f"## {display_id}{tag}\n\n{text}\n"


def build(master_path, salt, raters, out_dir, instruments_dir, protocol_path):
    cases = load_master(master_path)
    hard, _, _ = lint(cases)
    if hard:
        raise SystemExit("lint hard failures, refusing to build:\n  " + "\n  ".join(hard))
    by_master = {c["id"]: c for c in cases}
    id_map = assign_display_ids(cases, salt)
    rev = {v: k for k, v in id_map.items()}
    strata_by_display = {d: by_master[m]["stratum"] for d, m in id_map.items()}
    analysis_ids = sorted(d for d in id_map if d.startswith("C"))
    practice_ids = sorted((d for d in id_map if d.startswith("P")), key=lambda x: int(x[1:]))

    out_dir = Path(out_dir)
    priv = out_dir / "private"
    pub = out_dir / "public"
    packets = out_dir / "rater_packets"
    for d in (priv, pub, packets):
        d.mkdir(parents=True, exist_ok=True)

    instr = Path(instruments_dir)
    needed = ["ROUND_A_INSTRUCTIONS_v03.md", "CODEBOOK_v03.md"]
    for n in needed:
        if not (instr / n).exists():
            raise SystemExit(f"missing instrument file {instr / n}")

    orders = {}
    rater_files = {}
    for r in raters:
        oa, ta = make_order(analysis_ids, strata_by_display, salt, r, "A")
        ob, tb = make_order(analysis_ids, strata_by_display, salt, r, "B")
        orders[r] = {"A": oa, "B": ob, "attempts": {"A": ta, "B": tb}}
        rd = packets / r
        a_dir, b_dir = rd / "ROUND_A", rd / "ROUND_B"
        write_text(rd / "README.txt",
                   f"Rater {r}\n\nStart with ROUND_A. Do not open ROUND_B until you have been told Round A is locked.\n"
                   "Do not share this folder or discuss the cases with anyone until all ratings are locked.\n")
        a_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(instr / "ROUND_A_INSTRUCTIONS_v03.md", a_dir / "ROUND_A_INSTRUCTIONS_v03.md")
        body = [f"# SEVEN - ROUND A - rater {r}\n", "Read ROUND_A_INSTRUCTIONS_v03.md first. Work in the order given.\n", "---\n"]
        body += [case_md(d, by_master[id_map[d]]["text"]) for d in oa]
        write_text(a_dir / "CASES.md", "\n".join(body))
        write_csv(a_dir / "SHEET.csv", ["CASE_ID", "FREE_MOTIVE_DESCRIPTION", "KEYWORDS"], [[d, "", ""] for d in oa])

        b_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(instr / "CODEBOOK_v03.md", b_dir / "CODEBOOK_v03.md")
        body = [f"# SEVEN - ROUND B - rater {r}\n", "Read CODEBOOK_v03.md first. Rate the practice cases first and return only those rows.\n", "---\n"]
        body += [case_md(d, by_master[id_map[d]]["text"], " (PRACTICE)") for d in practice_ids]
        body += [case_md(d, by_master[id_map[d]]["text"]) for d in ob]
        write_text(b_dir / "CASES.md", "\n".join(body))
        write_csv(b_dir / "SHEET.csv", ["CASE_ID"] + ROUND_B_FIELDS, [[d] + [""] * len(ROUND_B_FIELDS) for d in practice_ids + ob])
        if practice_ids:
            fb = ["# Practice feedback\n", "Released only after your practice rows were returned.\n"]
            for d in practice_ids:
                fb.append(f"## {d}\n\n{by_master[id_map[d]]['feedback'].strip()}\n")
            write_text(b_dir / "after_practice" / "PRACTICE_FEEDBACK.md", "\n".join(fb))
        rater_files[r] = [str(p.relative_to(rd)) for p in sorted(rd.rglob("*")) if p.is_file()]

    # hard leak checks on everything a rater can see
    leaks = leak_check(packets, by_master, raters)
    if leaks:
        raise SystemExit("leak check failed:\n  " + "\n  ".join(leaks))

    key_rows = []
    for d in sorted(id_map, key=lambda x: (x[0], int(x[1:]))):
        c = by_master[id_map[d]]
        key_rows.append([d, c["id"], c["stratum"], "|".join(c["intended_primary"]), "|".join(c["intended_secondary"]), c["source_note"]])
    write_csv(priv / "KEY.csv", ["DISPLAY_ID", "MASTER_ID", "STRATUM", "INTENDED_PRIMARY", "INTENDED_SECONDARY", "SOURCE_NOTE"], key_rows)
    write_json(priv / "ID_MAP.json", id_map)
    write_json(priv / "ORDERS.json", orders)
    write_json(priv / "ROUND_SECRETS.json", {"salt": salt, "raters": raters, "tool": TOOL_VERSION})

    commitment = make_commitment(master_path, priv, salt, raters, cases, instr, protocol_path)
    write_json(pub / "COMMITMENT_v03.json", commitment)
    return {
        "n_analysis": len(analysis_ids), "n_practice": len(practice_ids), "raters": raters,
        "out": str(out_dir), "attempts": {r: orders[r]["attempts"] for r in raters},
    }


def leak_check(packets_dir, by_master, raters):
    problems = []
    cat_re = re.compile(r"\b(pride|greed|lust|envy|gluttony|wrath|sloth|acedia|sloth_acedia)\b", re.I)
    notes = [c["source_note"] for c in by_master.values() if len(c["source_note"]) >= 12]
    case_texts = sorted((c["text"] for c in by_master.values()), key=len, reverse=True)
    for r in raters:
        for p in sorted((packets_dir / r).rglob("*")):
            if not p.is_file():
                continue
            txt = p.read_text(encoding="utf-8")
            rel = p.relative_to(packets_dir)
            if "ROUND_A" in p.parts and cat_re.search(txt):
                problems.append(f"{rel}: category name in a Round A file ({cat_re.search(txt).group(0)})")
            for n in notes:
                if n in txt:
                    problems.append(f"{rel}: contains a source note")
            # boilerplate only: case texts are removed so ordinary words inside cases cannot trigger this
            boiler = txt
            for ct in case_texts:
                boiler = boiler.replace(ct, "")
            if re.search(r"\b(intended|stratum|analyst key|master corpus)\b", boiler, re.I) and p.name in ("CASES.md", "SHEET.csv"):
                problems.append(f"{rel}: contains stratum/intended/key wording outside case text")
    return problems


def instrument_hashes(instr, protocol_path):
    out = {}
    files = {
        "ROUND_A_INSTRUCTIONS_v03.md": instr / "ROUND_A_INSTRUCTIONS_v03.md",
        "CODEBOOK_v03.md": instr / "CODEBOOK_v03.md",
        "DESCRIPTION_CODING_INSTRUCTIONS_v03.md": instr / "DESCRIPTION_CODING_INSTRUCTIONS_v03.md",
        "RATER_DISCLOSURE_v03.csv": instr / "RATER_DISCLOSURE_v03.csv",
        "build_packets_v03.py": Path(__file__).resolve(),
        "analyze_ratings_v03.py": instr / "analyze_ratings_v03.py",
        "SEVEN_ANNOTATION_PROTOCOL_v03.md": Path(protocol_path) if protocol_path else instr.parent / "SEVEN_ANNOTATION_PROTOCOL_v03.md",
    }
    for name, p in files.items():
        out[name] = sha256_file(p) if p.exists() else "MISSING"
    return out


def make_commitment(master_path, priv, salt, raters, cases, instr, protocol_path):
    return {
        "protocol_version": "v03",
        "tool": TOOL_VERSION,
        "n_analysis_cases": sum(1 for c in cases if c["stratum"] != "practice"),
        "n_practice_cases": sum(1 for c in cases if c["stratum"] == "practice"),
        "strata_counts": dict(sorted(Counter(c["stratum"] for c in cases).items())),
        "n_raters": len(raters),
        "raters_sha256": sha256_text(",".join(raters)),
        "salt_sha256": sha256_text(salt),
        "private_sha256": {
            "master_corpus": sha256_file(master_path),
            "KEY.csv": sha256_file(priv / "KEY.csv"),
            "ID_MAP.json": sha256_file(priv / "ID_MAP.json"),
            "ORDERS.json": sha256_file(priv / "ORDERS.json"),
        },
        "instrument_sha256": instrument_hashes(instr, protocol_path),
    }


def cmd_build(args):
    raters = [r.strip() for r in args.raters.split(",") if r.strip()]
    if len(raters) != len(set(raters)):
        raise SystemExit("duplicate rater ids")
    if len(args.salt) < 16:
        raise SystemExit("salt too short; use `salt` to generate one")
    res = build(args.master, args.salt, raters, args.out, args.instruments, args.protocol)
    print(json.dumps(res, indent=2))
    print("\nNext: keep <out>/private offline; publish <out>/public/COMMITMENT_v03.json; "
          "deliver <out>/rater_packets/<rater>/ROUND_A only; release ROUND_B after Round A is locked.")
    return 0


def cmd_verify(args):
    commit = json.loads(Path(args.commitment).read_text(encoding="utf-8"))
    priv = Path(args.private)
    secrets_ = json.loads((priv / "ROUND_SECRETS.json").read_text(encoding="utf-8"))
    salt, raters = secrets_["salt"], secrets_["raters"]
    bad = []

    def chk(name, got, want):
        if got != want:
            bad.append(f"{name}: expected {want}, got {got}")

    chk("salt", sha256_text(salt), commit["salt_sha256"])
    chk("raters", sha256_text(",".join(raters)), commit["raters_sha256"])
    chk("master_corpus", sha256_file(args.master), commit["private_sha256"]["master_corpus"])
    for name in ("KEY.csv", "ID_MAP.json", "ORDERS.json"):
        chk(name, sha256_file(priv / name), commit["private_sha256"][name])
    cases = load_master(args.master)
    by_master = {c["id"]: c for c in cases}
    id_map = assign_display_ids(cases, salt)
    chk("ID_MAP regenerated", json.loads((priv / "ID_MAP.json").read_text()), id_map)
    strata = {d: by_master[m]["stratum"] for d, m in id_map.items()}
    analysis_ids = sorted(d for d in id_map if d.startswith("C"))
    orders = json.loads((priv / "ORDERS.json").read_text())
    for r in raters:
        for rnd in ("A", "B"):
            order, _ = make_order(analysis_ids, strata, salt, r, rnd)
            chk(f"order {r}/{rnd} regenerated", orders[r][rnd], order)
    if args.instruments:
        got = instrument_hashes(Path(args.instruments), args.protocol)
        for k, v in commit["instrument_sha256"].items():
            if got.get(k) != v:
                bad.append(f"instrument {k}: expected {v}, got {got.get(k)}")
    if bad:
        print("VERIFY FAILED")
        for b in bad:
            print(" -", b)
        return 1
    print("VERIFY OK: commitment, IDs and orders reproduce.")
    return 0


# ---------------------------------------------------------------- descriptions
def cmd_descriptions(args):
    d = Path(args.round_a_dir)
    items = []
    for p in sorted(d.glob("*.csv")):
        rater = p.stem
        with open(p, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                desc = (row.get("FREE_MOTIVE_DESCRIPTION") or "").strip()
                if desc:
                    items.append((rater, row["CASE_ID"], desc, (row.get("KEYWORDS") or "").strip()))
    keys = [f"{r}|{c}" for r, c, _, _ in items]
    order = shuffled(list(range(len(items))), f"{args.salt}|desc")
    out = Path(args.out)
    priv = out / "private"
    width = max(3, len(str(len(items))))
    rows, mapping = [], {}
    for pos, idx in enumerate(order):
        item_id = f"D{pos + 1:0{width}d}"
        r, c, desc, kw = items[idx]
        rows.append([item_id, desc, kw, "", "", ""])
        mapping[item_id] = {"rater": r, "case": c}
    write_csv(out / "DESCRIPTION_CODING_SHEET_TEMPLATE.csv",
              ["ITEM_ID", "FREE_MOTIVE_DESCRIPTION", "KEYWORDS", "PRIMARY_MAPPED", "SECONDARY_MAPPED", "COMMENT"], rows)
    write_json(priv / "DESCRIPTION_ITEM_MAP.json", mapping)
    print(f"{len(items)} descriptions -> {out / 'DESCRIPTION_CODING_SHEET_TEMPLATE.csv'} (private map in {priv})")
    return 0


# ---------------------------------------------------------------- selftest
def _toy_master():
    forms = {
        "central": 28, "mixed": 16, "control": 8, "other": 4, "external": 8, "practice": 4,
    }
    cases = []
    n = 0
    cat_cycle = 0
    for s, k in forms.items():
        for i in range(k):
            n += 1
            prim = []
            sec = []
            if s == "central":
                prim = [CATEGORIES[i % 7]]
            elif s == "mixed":
                prim = [CATEGORIES[i % 7]]
                sec = [CATEGORIES[(i + 3) % 7]]
            cases.append({
                "id": f"T{n:03d}",
                "text": f"Synthetic toy case number {n} about a person who does something unremarkable at the office and then goes home. " * 3,
                "stratum": s, "intended_primary": prim, "intended_secondary": sec,
                "source_note": f"toy source note number {n} for leak test", "feedback": "toy feedback" if s == "practice" else "",
            })
    return {"schema_version": "v03", "cases": cases}


def cmd_selftest(args):
    tmp = Path(tempfile.mkdtemp(prefix="seven_selftest_"))
    ok = True

    def check(name, cond):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + name)
        ok = ok and cond

    master = tmp / "master.json"
    write_json(master, _toy_master())
    instr = Path(__file__).resolve().parent
    salt = "a" * 32
    raters = ["R01", "R02", "R03"]
    r1 = build(master, salt, raters, tmp / "o1", instr, None)
    r2 = build(master, salt, raters, tmp / "o2", instr, None)
    h1 = {p.relative_to(tmp / "o1"): sha256_file(p) for p in (tmp / "o1").rglob("*") if p.is_file()}
    h2 = {p.relative_to(tmp / "o2"): sha256_file(p) for p in (tmp / "o2").rglob("*") if p.is_file()}
    h1 = {k: v for k, v in h1.items() if "COMMITMENT" not in str(k)}
    h2 = {k: v for k, v in h2.items() if "COMMITMENT" not in str(k)}
    check("build is deterministic", h1 == h2)
    o = json.loads((tmp / "o1" / "private" / "ORDERS.json").read_text())
    check("raters get different orders", o["R01"]["A"] != o["R02"]["A"] and o["R01"]["A"] != o["R01"]["B"])
    check("every analysis case once per order", all(sorted(o[r][x]) == sorted(o["R01"]["A"]) for r in raters for x in "AB"))
    a_txt = (tmp / "o1" / "rater_packets" / "R01" / "ROUND_A" / "SHEET.csv").read_text()
    check("Round A sheet has no category names", not re.search(r"PRIDE|GREED|LUST|ENVY", a_txt))
    check("Round B sheet has category columns", "PRIDE" in (tmp / "o1" / "rater_packets" / "R01" / "ROUND_B" / "SHEET.csv").read_text())
    rc = cmd_verify(argparse.Namespace(
        commitment=tmp / "o1" / "public" / "COMMITMENT_v03.json", private=tmp / "o1" / "private",
        master=master, instruments=None, protocol=None))
    check("verify passes on untouched output", rc == 0)
    kp = tmp / "o1" / "private" / "KEY.csv"
    kp.write_text(kp.read_text().replace("central", "mixed", 1))
    rc = cmd_verify(argparse.Namespace(
        commitment=tmp / "o1" / "public" / "COMMITMENT_v03.json", private=tmp / "o1" / "private",
        master=master, instruments=None, protocol=None))
    check("verify fails after key tampering", rc == 1)
    leaky = _toy_master()
    leaky["cases"][0]["text"] += " He felt a great deal of envy."
    hard, _, _ = lint(load_master(_dump(tmp, leaky)))
    check("lint hard-fails on a label word", any("C1" in h for h in hard))
    leaky2 = _toy_master()
    leaky2["cases"][1]["source_note"] = "Synthetic toy case number 3 about a person who does something unremarkable"
    leaky2["cases"][2]["text"] = leaky2["cases"][1]["source_note"] + " more words " * 20
    p2 = _dump(tmp, leaky2)
    try:
        build(p2, salt, ["R01"], tmp / "o3", instr, None)
        check("leak check blocks a source note in rater text", False)
    except SystemExit:
        check("leak check blocks a source note in rater text", True)
    print("\nSELFTEST", "OK" if ok else "FAILED")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def _dump(tmp, obj):
    p = tmp / f"m_{secrets.token_hex(4)}.json"
    write_json(p, obj)
    return p


# ---------------------------------------------------------------- main
def main(argv=None):
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("salt")
    p = sub.add_parser("lint")
    p.add_argument("--master", required=True)
    p.add_argument("--v02-master")
    p.add_argument("--report")
    p.add_argument("--strict", action="store_true", help="treat warnings as failures")
    p = sub.add_parser("build")
    p.add_argument("--master", required=True)
    p.add_argument("--salt", required=True)
    p.add_argument("--raters", required=True, help="comma-separated rater ids, e.g. R01,R02,R03,R04,R05")
    p.add_argument("--out", required=True)
    p.add_argument("--instruments", default=str(here))
    p.add_argument("--protocol", default=str(here.parent / "SEVEN_ANNOTATION_PROTOCOL_v03.md"))
    p = sub.add_parser("descriptions")
    p.add_argument("--round-a-dir", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--salt", required=True)
    p = sub.add_parser("verify")
    p.add_argument("--master", required=True)
    p.add_argument("--private", required=True)
    p.add_argument("--commitment", required=True)
    p.add_argument("--instruments", help="directory holding the instrument files, to re-hash them")
    p.add_argument("--protocol")
    sub.add_parser("selftest")
    args = ap.parse_args(argv)
    if args.cmd == "salt":
        print(secrets.token_hex(32))
        return 0
    return {"lint": cmd_lint, "build": cmd_build, "descriptions": cmd_descriptions,
            "verify": cmd_verify, "selftest": cmd_selftest}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())