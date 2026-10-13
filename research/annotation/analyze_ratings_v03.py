#!/usr/bin/env python3
"""SEVEN annotation toolkit v03 - analysis.  Python 3.8+, standard library only.

  report    apply the pre-specified analysis plan and decision rules of
            SEVEN_ANNOTATION_PROTOCOL_v03.md to locked Round A / Round B data
  selftest  check the alpha implementation against a published reference example
            and run the whole pipeline on simulated raters

Nothing here is tunable at analysis time except what the protocol marks as an
analyst action (--confirm-f2). Every parameter comes from PARAMS below and mirrors
the protocol's parameter table (P1-P14). Changing PARAMS after freeze invalidates
the commitment on this file.
"""
import argparse
import csv
import json
import math
import random
import sys
import tempfile
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

CATEGORIES = ["PRIDE", "GREED", "LUST", "ENVY", "GLUTTONY", "WRATH", "SLOTH_ACEDIA"]
ROUND_B_FIELDS = CATEGORIES + ["PRIMARY", "OTHER", "UNCLEAR", "CONFIDENCE", "COMMENT"]
PRIMARY_VALUES = CATEGORIES + ["NONE"]
MAPPED_VALUES = CATEGORIES + ["OTHER", "NONE"]
ANALYSIS_STRATA = ["central", "mixed", "control", "other", "external"]
NAN = float("nan")

PARAMS = {
    "P1_min_raters": 5,
    "P2_min_completion": 0.90,
    "P3_strong_alpha": 0.800,
    "P3_strong_ci_lower": 0.667,
    "P3_adequate_alpha": 0.667,
    "P4_bootstrap_B": 2000,
    "P4_seed": 20261013,
    "P5_min_units_with_central": 5,
    "P6_min_strong_or_adequate": 5,
    "P6_max_weak": 1,
    "P6_min_external_units": 8,
    "P7_min_weak_for_revision": 3,
    "P8_pair_split_share": 0.10,
    "P9_min_other_units": 3,
    "P9_min_raters_other": 2,
    "P10_mixed_pooled_ordinal_alpha": 0.500,
    "P11_control_overlabel_share": 0.25,
    "P12_concordance_min": 0.60,
    "P12_other_mapped_max": 0.20,
    "P13_max_inconsistent_share": 0.20,
    "P14_coder_alpha_min": 0.667,
}


# ------------------------------------------------------------------ alpha
def unit_counts(values):
    return Counter(v for v in values if v is not None)


def unit_coincidence(cnt):
    """Contribution of one unit (value counts) to the coincidence matrix."""
    m = sum(cnt.values())
    out = defaultdict(float)
    if m < 2:
        return out
    for c, nc in cnt.items():
        for k, nk in cnt.items():
            pairs = nc * (nc - 1) if c == k else nc * nk
            if pairs:
                out[(c, k)] += pairs / (m - 1)
    return out


def alpha_from_coincidence(o, metric):
    n_c = defaultdict(float)
    for (c, k), w in o.items():
        n_c[c] += w
    n = sum(n_c.values())
    if n <= 1:
        return NAN
    values = sorted(n_c)
    cum = {}
    run = 0.0
    for v in values:
        run += n_c[v]
        cum[v] = run

    def d2(c, k):
        if c == k:
            return 0.0
        if metric == "nominal":
            return 1.0
        if metric == "interval":
            return float(c - k) ** 2
        lo, hi = (c, k) if c < k else (k, c)
        s = cum[hi] - cum[lo] + n_c[lo]
        return (s - (n_c[lo] + n_c[hi]) / 2.0) ** 2

    do = sum(w * d2(c, k) for (c, k), w in o.items()) / n
    de = sum(n_c[c] * n_c[k] * d2(c, k) for c in values for k in values) / (n * (n - 1))
    if de == 0:
        return NAN
    return 1.0 - do / de


def krippendorff_alpha(units, metric):
    """units: iterable of sequences of ratings (None = missing)."""
    o = defaultdict(float)
    for u in units:
        for key, w in unit_coincidence(unit_counts(u)).items():
            o[key] += w
    return alpha_from_coincidence(o, metric)


def gwet_ac1(units, q):
    """Gwet's AC1 for several raters, q possible categories."""
    pa_list, per_cat = [], defaultdict(float)
    used = 0
    for u in units:
        cnt = unit_counts(u)
        r = sum(cnt.values())
        if r < 2:
            continue
        used += 1
        pa_list.append(sum(c * (c - 1) for c in cnt.values()) / (r * (r - 1)))
        for k, c in cnt.items():
            per_cat[k] += c / r
    if not used:
        return NAN
    pa = sum(pa_list) / used
    pe = sum((v / used) * (1 - v / used) for v in per_cat.values()) / (q - 1)
    return NAN if pe >= 1 else (pa - pe) / (1 - pe)


def pairwise_agreement(units):
    tot, agree = 0, 0
    for u in units:
        v = [x for x in u if x is not None]
        for a, b in combinations(v, 2):
            tot += 1
            agree += a == b
    return agree / tot if tot else NAN


def bootstrap_alpha(units, metric, B, seed):
    """Percentile interval resampling units. Returns (lo, hi, n_valid)."""
    contrib = [unit_coincidence(unit_counts(u)) for u in units]
    n = len(units)
    rng = random.Random(seed)
    vals = []
    for _ in range(B):
        o = defaultdict(float)
        for _i in range(n):
            for key, w in contrib[rng.randrange(n)].items():
                o[key] += w
        a = alpha_from_coincidence(o, metric)
        if not math.isnan(a):
            vals.append(a)
    if len(vals) < 0.9 * B:
        return NAN, NAN, len(vals)
    vals.sort()
    lo = vals[int(0.025 * (len(vals) - 1))]
    hi = vals[int(math.ceil(0.975 * (len(vals) - 1)))]
    return lo, hi, len(vals)


def fmt(x, d=3):
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{d}f}"


# ------------------------------------------------------------------ loading
def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_key(path):
    key = {}
    for r in read_csv(path):
        key[r["DISPLAY_ID"]] = {
            "stratum": r["STRATUM"],
            "primary": [x for x in r["INTENDED_PRIMARY"].split("|") if x],
            "secondary": [x for x in r["INTENDED_SECONDARY"].split("|") if x],
        }
    return key


def parse_int(x):
    try:
        return int(str(x).strip())
    except (ValueError, AttributeError):
        return None


def load_rater_sheet(path, analysis_ids):
    rows = {}
    issues = []
    for r in read_csv(path):
        cid = r["CASE_ID"]
        if cid not in analysis_ids:
            continue
        ratings = {c: parse_int(r.get(c)) for c in CATEGORIES}
        primary = (r.get("PRIMARY") or "").strip().upper()
        valid = all(v in (0, 1, 2) for v in ratings.values()) and primary in PRIMARY_VALUES
        if not valid:
            if any((r.get(c) or "").strip() for c in ROUND_B_FIELDS):
                issues.append(f"{cid}: incomplete or invalid row")
            continue
        other = (r.get("OTHER") or "").strip().upper() == "YES"
        unclear = (r.get("UNCLEAR") or "").strip().upper() == "YES"
        conf = parse_int(r.get("CONFIDENCE"))
        rows[cid] = {"ratings": ratings, "primary": primary, "other": other, "unclear": unclear,
                     "confidence": conf if conf in (1, 2, 3, 4, 5) else None,
                     "comment": (r.get("COMMENT") or "").strip()}
    return rows, issues


def is_inconsistent(row):
    twos = [c for c in CATEGORIES if row["ratings"][c] == 2]
    p = row["primary"]
    if p == "NONE":
        return bool(twos)
    if row["ratings"][p] == 0:
        return True
    return bool(twos) and row["ratings"][p] < 2


def load_disclosure(path):
    out = {}
    if not path:
        return out
    for r in read_csv(path):
        out[r["RATER_ID"].strip()] = r
    return out


def completion_round_a(path, analysis_ids):
    done = 0
    for r in read_csv(path):
        if r["CASE_ID"] in analysis_ids and (r.get("FREE_MOTIVE_DESCRIPTION") or "").strip():
            done += 1
    return done / len(analysis_ids) if analysis_ids else 0.0


# ------------------------------------------------------------------ analysis
def analyse(args):
    P = PARAMS
    key = load_key(args.key)
    analysis_ids = sorted(k for k, v in key.items() if v["stratum"] in ANALYSIS_STRATA)
    N = len(analysis_ids)
    strata = {k: key[k]["stratum"] for k in analysis_ids}
    stratum_n = Counter(strata.values())
    disclosure = load_disclosure(args.disclosure)

    raters, excluded = {}, []
    for p in sorted(Path(args.ratings_dir).glob("*.csv")):
        rid = p.stem
        rows, issues = load_rater_sheet(p, set(analysis_ids))
        comp_b = len(rows) / N
        comp_a = None
        if args.round_a_dir and (Path(args.round_a_dir) / f"{rid}.csv").exists():
            comp_a = completion_round_a(Path(args.round_a_dir) / f"{rid}.csv", set(analysis_ids))
        completion = min(comp_b, comp_a) if comp_a is not None else comp_b
        inc = sum(is_inconsistent(r) for r in rows.values())
        inc_share = inc / len(rows) if rows else 1.0
        d = disclosure.get(rid, {})
        reasons = []
        yes = lambda k: (d.get(k) or "").strip().upper() == "YES"
        if yes("ACCESSED_SEVEN_MATERIALS_BEFORE_LOCK") or yes("CONSULTED_OTHERS_BEFORE_LOCK") or yes("USED_OUTSIDE_TOOLS_ROUND_A"):
            reasons.append("E1 disclosed access/consultation/tools before lock")
        if completion < P["P2_min_completion"]:
            reasons.append(f"E2 completion {completion:.0%}")
        if inc_share > P["P13_max_inconsistent_share"]:
            reasons.append(f"E3 self-inconsistent PRIMARY in {inc_share:.0%} of units")
        info = {"rater": rid, "completion": completion, "completion_round_a_checked": comp_a is not None,
                "inconsistent_share": inc_share, "issues": issues, "familiarity": d.get("PRIOR_FAMILIARITY", "")}
        if reasons:
            info["excluded_for"] = reasons
            excluded.append(info)
        else:
            raters[rid] = rows
            info["excluded_for"] = []
        info["rows_b"] = len(rows)
        raters_info = info  # noqa: F841 (kept for clarity)
    rater_list = sorted(raters)
    R = len(rater_list)

    def vals(cat, unit_ids, binary):
        out = []
        for u in unit_ids:
            row = []
            for r in rater_list:
                x = raters[r].get(u)
                if x is None:
                    row.append(None)
                else:
                    v = x["ratings"][cat]
                    row.append((1 if v == 2 else 0) if binary else v)
            out.append(row)
        return out

    def primary_vals(unit_ids):
        return [[(raters[r][u]["primary"] if u in raters[r] else None) for r in rater_list] for u in unit_ids]

    res = {"params": P, "n_units": N, "strata": dict(stratum_n), "raters_eligible": rater_list,
           "raters_excluded": excluded, "categories": {}, "primary": {}, "flags": {}, "descriptive": {}}

    B, seed = P["P4_bootstrap_B"], P["P4_seed"]
    tiers = {}
    for cat in CATEGORIES:
        ub = vals(cat, analysis_ids, True)
        uo = vals(cat, analysis_ids, False)
        a_bin = krippendorff_alpha(ub, "nominal")
        lo, hi, nv = bootstrap_alpha(ub, "nominal", B, seed) if R >= 2 else (NAN, NAN, 0)
        a_ord = krippendorff_alpha(uo, "ordinal")
        olo, ohi, _ = bootstrap_alpha(uo, "ordinal", B, seed) if R >= 2 else (NAN, NAN, 0)
        n_with = sum(1 for row in ub if any(v == 1 for v in row if v is not None))
        undetermined = math.isnan(a_bin) or n_with < P["P5_min_units_with_central"]
        if undetermined:
            tier = "UNDETERMINED"
        else:
            lo_eff = lo if not math.isnan(lo) else -1.0
            if a_bin >= P["P3_strong_alpha"] and lo_eff >= P["P3_strong_ci_lower"]:
                tier = "STRONG"
            elif a_bin >= P["P3_adequate_alpha"]:
                tier = "ADEQUATE"
            else:
                tier = "WEAK"
        tiers[cat] = tier
        res["categories"][cat] = {
            "alpha_binary_central": a_bin, "ci_binary": [lo, hi], "alpha_ordinal": a_ord, "ci_ordinal": [olo, ohi],
            "pairwise_agreement_binary": pairwise_agreement(ub), "ac1_binary": gwet_ac1(ub, 2),
            "units_with_any_central": n_with, "tier": tier,
        }

    pu = primary_vals(analysis_ids)
    p_alpha = krippendorff_alpha(pu, "nominal")
    plo, phi, _ = bootstrap_alpha(pu, "nominal", B, seed) if R >= 2 else (NAN, NAN, 0)
    complete = [all(v == row[0] for v in row if v is not None) for row in pu if sum(v is not None for v in row) >= 2]
    res["primary"] = {
        "alpha_nominal": p_alpha, "ci": [plo, phi], "ac1": gwet_ac1(pu, len(PRIMARY_VALUES)),
        "pairwise_agreement": pairwise_agreement(pu),
        "complete_agreement_share": (sum(complete) / len(complete)) if complete else NAN, "by_stratum": {},
    }
    for s in ANALYSIS_STRATA:
        ids = [u for u in analysis_ids if strata[u] == s]
        if not ids:
            continue
        sub = primary_vals(ids)
        comp = [all(v == row[0] for v in row if v is not None) for row in sub if sum(v is not None for v in row) >= 2]
        res["primary"]["by_stratum"][s] = {
            "n": len(ids), "alpha_nominal": krippendorff_alpha(sub, "nominal"),
            "pairwise_agreement": pairwise_agreement(sub),
            "complete_agreement_share": (sum(comp) / len(comp)) if comp else NAN,
        }

    # ---- F1 pair splits
    split_counts = Counter()
    for u in analysis_ids:
        labels = Counter(raters[r][u]["primary"] for r in rater_list if u in raters[r])
        n_u = sum(labels.values())
        need = max(2, math.ceil(0.25 * n_u))
        cats = [c for c in CATEGORIES if labels.get(c, 0) >= need]
        for a, b in combinations(cats, 2):
            split_counts[(a, b)] += 1
    f1_thresh = math.ceil(P["P8_pair_split_share"] * N)
    f1_pairs = {f"{a}+{b}": n for (a, b), n in split_counts.items() if n >= f1_thresh}
    res["flags"]["F1"] = {"triggered": bool(f1_pairs), "threshold_units": f1_thresh,
                          "pair_split_units": {f"{a}+{b}": n for (a, b), n in sorted(split_counts.items(), key=lambda kv: -kv[1])},
                          "pairs_over_threshold": f1_pairs}

    # ---- F2 missing mechanism candidate
    f2_units = []
    for u in analysis_ids:
        flagged = [r for r in rater_list if u in raters[r] and raters[r][u]["other"]]
        if len(flagged) >= P["P9_min_raters_other"]:
            f2_units.append({"unit": u, "stratum": strata[u], "comments": [raters[r][u]["comment"] for r in flagged]})
    non_other_f2 = [x for x in f2_units if x["stratum"] != "other"]
    f2_candidate = len(non_other_f2) >= P["P9_min_other_units"]
    res["flags"]["F2"] = {"candidate": f2_candidate, "confirmed_by_analyst": bool(args.confirm_f2),
                          "units_marked_other_by_2plus_raters_outside_other_stratum": non_other_f2,
                          "triggered": bool(f2_candidate and args.confirm_f2)}

    # ---- F3 mixed collapse
    mixed_ids = [u for u in analysis_ids if strata[u] == "mixed"]
    pooled = []
    for cat in CATEGORIES:
        pooled += vals(cat, mixed_ids, False)
    f3_alpha = krippendorff_alpha(pooled, "ordinal") if pooled else NAN
    res["flags"]["F3"] = {"pooled_ordinal_alpha_mixed": f3_alpha,
                          "triggered": (not math.isnan(f3_alpha)) and f3_alpha < P["P10_mixed_pooled_ordinal_alpha"]}

    # ---- F4 control over-labelling
    ctrl_rows = [raters[r][u] for u in analysis_ids if strata[u] == "control" for r in rater_list if u in raters[r]]
    over = sum(1 for x in ctrl_rows if any(v == 2 for v in x["ratings"].values()))
    none_share = (sum(1 for x in ctrl_rows if x["primary"] == "NONE") / len(ctrl_rows)) if ctrl_rows else NAN
    f4_share = over / len(ctrl_rows) if ctrl_rows else NAN
    res["flags"]["F4"] = {"diagnostic_only": True, "overlabel_share": f4_share, "primary_none_share": none_share,
                          "control_rows": len(ctrl_rows),
                          "triggered": (not math.isnan(f4_share)) and f4_share >= P["P11_control_overlabel_share"]}

    # ---- other stratum / OTHER usage
    oth_rows = [raters[r][u] for u in analysis_ids if strata[u] == "other" for r in rater_list if u in raters[r]]
    non_oth_rows = [raters[r][u] for u in analysis_ids if strata[u] != "other" for r in rater_list if u in raters[r]]
    res["descriptive"]["other_marked_on_other_stratum"] = (sum(x["other"] for x in oth_rows) / len(oth_rows)) if oth_rows else NAN
    res["descriptive"]["other_marked_elsewhere"] = (sum(x["other"] for x in non_oth_rows) / len(non_oth_rows)) if non_oth_rows else NAN
    res["descriptive"]["unclear_share_by_stratum"] = {
        s: (lambda rows: (sum(x["unclear"] for x in rows) / len(rows)) if rows else NAN)(
            [raters[r][u] for u in analysis_ids if strata[u] == s for r in rater_list if u in raters[r]])
        for s in ANALYSIS_STRATA if stratum_n.get(s)}
    conf = Counter(x["confidence"] for r in rater_list for x in raters[r].values() if x["confidence"])
    res["descriptive"]["confidence_distribution"] = {str(k): conf.get(k, 0) for k in (1, 2, 3, 4, 5)}

    # ---- F5 Round A
    f5 = {"evaluated": False, "reason": "no description-coder data supplied", "triggered": False}
    if args.desc_map and args.desc_coder_1 and args.desc_coder_2:
        dmap = json.loads(Path(args.desc_map).read_text(encoding="utf-8"))
        c1 = {r["ITEM_ID"]: (r.get("PRIMARY_MAPPED") or "").strip().upper() for r in read_csv(args.desc_coder_1)}
        c2 = {r["ITEM_ID"]: (r.get("PRIMARY_MAPPED") or "").strip().upper() for r in read_csv(args.desc_coder_2)}
        items = [i for i in dmap if c1.get(i) in MAPPED_VALUES and c2.get(i) in MAPPED_VALUES]
        coder_alpha = krippendorff_alpha([[c1[i], c2[i]] for i in items], "nominal")
        f5 = {"evaluated": False, "coder_alpha": coder_alpha, "items_coded_by_both": len(items), "triggered": False}
        if not math.isnan(coder_alpha) and coder_alpha >= P["P14_coder_alpha_min"]:
            agreed = [i for i in items if c1[i] == c2[i]]
            conc_n = conc_d = oth_n = oth_d = 0
            for i in agreed:
                rid, cid = dmap[i]["rater"], dmap[i]["case"]
                if rid not in raters or cid not in strata:
                    continue
                s = strata[cid]
                if s != "other":
                    oth_d += 1
                    oth_n += c1[i] == "OTHER"
                if s == "central" and cid in raters[rid]:
                    conc_d += 1
                    conc_n += c1[i] == raters[rid][cid]["primary"]
            conc = conc_n / conc_d if conc_d else NAN
            othshare = oth_n / oth_d if oth_d else NAN
            f5.update({"evaluated": True, "agreed_items": len(agreed), "concordance_central": conc,
                       "concordance_n": conc_d, "other_mapped_share_non_other": othshare,
                       "triggered": (not math.isnan(conc) and conc < P["P12_concordance_min"]) or
                                    (not math.isnan(othshare) and othshare > P["P12_other_mapped_max"])})
        else:
            f5["reason"] = "description coders' nominal alpha below P14 or undefined: F5 not interpretable"
    res["flags"]["F5"] = f5

    # ---- verdict
    n_weak = sum(1 for t in tiers.values() if t == "WEAK")
    n_sa = sum(1 for t in tiers.values() if t in ("STRONG", "ADEQUATE"))
    # F4 is a diagnostic flag (author decision, 2026-10-13): reported, but never drives the verdict.
    triggered = [k for k, v in res["flags"].items() if v.get("triggered") and k != "F4"]
    ext_n = stratum_n.get("external", 0)
    notes = []
    if R < P["P1_min_raters"]:
        verdict = "REVISION INDICATED (pilot-only data)" if (n_weak >= P["P7_min_weak_for_revision"] or triggered) else "NO VERDICT (pilot-only)"
    elif n_weak >= P["P7_min_weak_for_revision"] or triggered:
        verdict = "REVISION INDICATED"
    elif n_sa >= P["P6_min_strong_or_adequate"] and n_weak <= P["P6_max_weak"]:
        verdict = "RETAINED" if ext_n >= P["P6_min_external_units"] else "RETAINED (synthetic only)"
    else:
        verdict = "MIXED"
    if f2_candidate and not args.confirm_f2:
        notes.append("F2 is a candidate: check COMMENT text and Round A descriptions for a shared mechanism; "
                     "rerun with --confirm-f2 if one is named. The verdict above does not yet include F2.")
    res["verdict"] = {"outcome": verdict, "n_strong_or_adequate": n_sa, "n_weak": n_weak,
                      "n_undetermined": sum(1 for t in tiers.values() if t == "UNDETERMINED"),
                      "flags_triggered": triggered, "eligible_raters": R, "notes": notes}
    return res


# ------------------------------------------------------------------ report
def render(res):
    P = res["params"]
    L = ["# SEVEN - RELIABILITY REPORT v03", "",
         f"Units analysed: {res['n_units']} ({', '.join(f'{k}={v}' for k, v in res['strata'].items())})",
         f"Eligible raters: {len(res['raters_eligible'])} ({', '.join(res['raters_eligible'])})", ""]
    if res["raters_excluded"]:
        L += ["Excluded raters:"] + [f"- {e['rater']}: {'; '.join(e['excluded_for'])}" for e in res["raters_excluded"]] + [""]
    v = res["verdict"]
    L += ["## Outcome", "", f"**{v['outcome']}**", "",
          f"Categories STRONG/ADEQUATE: {v['n_strong_or_adequate']} of 7; WEAK: {v['n_weak']}; UNDETERMINED: {v['n_undetermined']}.",
          f"Falsification conditions triggered: {', '.join(v['flags_triggered']) or 'none'}."]
    for n in v["notes"]:
        L.append(f"Note: {n}")
    L += ["", "Parameters were fixed before data collection (protocol section 13). All results below are reported "
          "whether or not they favour the scheme.", "", "## Categories (decision statistic: binary 'central')", "",
          "| Category | Tier | Alpha (central) | 95% interval | Alpha (ordinal 0/1/2) | 95% interval | Pairwise agr. | AC1 | Units with a 2 |",
          "|---|---|---|---|---|---|---|---|---|"]
    for cat, c in res["categories"].items():
        L.append(f"| {cat} | {c['tier']} | {fmt(c['alpha_binary_central'])} | {fmt(c['ci_binary'][0])} to {fmt(c['ci_binary'][1])} | "
                 f"{fmt(c['alpha_ordinal'])} | {fmt(c['ci_ordinal'][0])} to {fmt(c['ci_ordinal'][1])} | "
                 f"{fmt(c['pairwise_agreement_binary'])} | {fmt(c['ac1_binary'])} | {c['units_with_any_central']} |")
    p = res["primary"]
    L += ["", "## PRIMARY label", "",
          f"Nominal alpha {fmt(p['alpha_nominal'])} (95% interval {fmt(p['ci'][0])} to {fmt(p['ci'][1])}); AC1 {fmt(p['ac1'])}; "
          f"pairwise agreement {fmt(p['pairwise_agreement'])}; complete agreement in {fmt(p['complete_agreement_share'])} of units.", "",
          "| Stratum | Units | Nominal alpha | Pairwise agr. | Complete agr. |", "|---|---|---|---|---|"]
    for s, d in p["by_stratum"].items():
        L.append(f"| {s} | {d['n']} | {fmt(d['alpha_nominal'])} | {fmt(d['pairwise_agreement'])} | {fmt(d['complete_agreement_share'])} |")
    f = res["flags"]
    L += ["", "## Falsification conditions", "",
          f"- F1 pair confusion: {'TRIGGERED' if f['F1']['triggered'] else 'not triggered'} (threshold {f['F1']['threshold_units']} units); "
          f"largest pair splits: {', '.join(f'{k}={n}' for k, n in list(f['F1']['pair_split_units'].items())[:5]) or 'none'}",
          f"- F2 missing mechanism: {'candidate' if f['F2']['candidate'] else 'no candidate'}; "
          f"{'confirmed by analyst' if f['F2']['confirmed_by_analyst'] else 'not confirmed'}; "
          f"{len(f['F2']['units_marked_other_by_2plus_raters_outside_other_stratum'])} unit(s) outside the 'other' stratum marked OTHER by 2+ raters",
          f"- F3 mixed collapse: pooled ordinal alpha on mixed units {fmt(f['F3']['pooled_ordinal_alpha_mixed'])} "
          f"(threshold {P['P10_mixed_pooled_ordinal_alpha']}): {'TRIGGERED' if f['F3']['triggered'] else 'not triggered'}",
          f"- F4 control over-labelling: {fmt(f['F4']['overlabel_share'])} of control ratings contain a 2 "
          f"(threshold {P['P11_control_overlabel_share']}); PRIMARY NONE on {fmt(f['F4']['primary_none_share'])}: "
          f"{'DIAGNOSTIC FLAG RAISED (does not affect the outcome)' if f['F4']['triggered'] else 'not raised'}"]
    f5 = f["F5"]
    if f5.get("evaluated"):
        L.append(f"- F5 Round A divergence: coder alpha {fmt(f5['coder_alpha'])}; concordance on central units {fmt(f5['concordance_central'])} "
                 f"(n={f5['concordance_n']}); OTHER-mapped share outside 'other' {fmt(f5['other_mapped_share_non_other'])}: "
                 f"{'TRIGGERED' if f5['triggered'] else 'not triggered'}")
    else:
        L.append(f"- F5 Round A divergence: not evaluated ({f5.get('reason', 'no data')})"
                 + (f"; coder alpha {fmt(f5.get('coder_alpha'))}" if 'coder_alpha' in f5 else ""))
    d = res["descriptive"]
    L += ["", "## Other descriptive results", "",
          f"- OTHER marked on 'other' stratum: {fmt(d['other_marked_on_other_stratum'])}; elsewhere: {fmt(d['other_marked_elsewhere'])}",
          f"- UNCLEAR share by stratum: {', '.join(f'{k}={fmt(x)}' for k, x in d['unclear_share_by_stratum'].items())}",
          f"- Confidence distribution: {d['confidence_distribution']}", "",
          "## Claims this outcome supports", "",
          "See protocol section 10. In every case: this is an author-constructed, English-language corpus; the result "
          "concerns the operational definitions in the codebook, not natural kinds, prevalence, or real people.", ""]
    return "\n".join(L)


def cmd_report(args):
    res = analyse(args)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "RELIABILITY_REPORT_v03.json").write_text(json.dumps(res, indent=2, default=str), encoding="utf-8")
    text = render(res)
    (out / "RELIABILITY_REPORT_v03.md").write_text(text, encoding="utf-8")
    print(text)
    return 0


# ------------------------------------------------------------------ selftest
def _reference_units():
    # Krippendorff (2011) worked example: 4 observers, 12 units, values 1-5, '*' missing
    rows = {
        "A": "1 2 3 3 2 1 4 1 2 * * *",
        "B": "1 2 3 3 2 2 4 1 2 5 * 3",
        "C": "* 3 3 3 2 3 4 2 2 5 1 *",
        "D": "1 2 3 3 2 4 4 1 2 5 1 *",
    }
    cols = {k: [None if x == "*" else int(x) for x in v.split()] for k, v in rows.items()}
    return [[cols[k][i] for k in "ABCD"] for i in range(12)]


def _simulate(tmp, n_raters, noise, seed, mode="intended"):
    rng = random.Random(seed)
    key_rows, units = [], []
    spec = [("central", 28), ("mixed", 16), ("control", 8), ("other", 4), ("external", 8)]
    i = 0
    for s, k in spec:
        for j in range(k):
            i += 1
            did = f"C{i:02d}"
            prim = [CATEGORIES[j % 7]] if s in ("central", "mixed") else []
            sec = [CATEGORIES[(j + 3) % 7]] if s == "mixed" else []
            key_rows.append([did, f"M{i}", s, "|".join(prim), "|".join(sec), ""])
            units.append((did, s, prim, sec))
    key_dir = Path(tmp)
    with open(key_dir / "KEY.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["DISPLAY_ID", "MASTER_ID", "STRATUM", "INTENDED_PRIMARY", "INTENDED_SECONDARY", "SOURCE_NOTE"])
        w.writerows(key_rows)
    (key_dir / "ratings").mkdir(exist_ok=True)
    for r in range(n_raters):
        rows = []
        for did, s, prim, sec in units:
            rat = {c: 0 for c in CATEGORIES}
            other = "NO"
            if mode == "random":
                rat = {c: rng.choice([0, 1, 2]) for c in CATEGORIES}
            else:
                for c in prim:
                    rat[c] = 2
                for c in sec:
                    rat[c] = 1
                if s == "other":
                    other = "YES"
                for c in CATEGORIES:
                    if rng.random() < noise:
                        rat[c] = rng.choice([0, 1, 2])
            mx = max(rat.values())
            tops = [c for c in CATEGORIES if rat[c] == mx]
            if mx == 0:
                primary = "NONE"
            else:
                pref = [c for c in prim if c in tops]
                primary = pref[0] if pref else rng.choice(tops)
            if mode == "random" or rat[primary if primary != "NONE" else CATEGORIES[0]] is None:
                pass
            rows.append([did] + [rat[c] for c in CATEGORIES] + [primary, other, "NO", 4, ""])
        with open(key_dir / "ratings" / f"R{r + 1:02d}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["CASE_ID"] + ROUND_B_FIELDS)
            w.writerows(rows)
    return key_dir


def cmd_selftest(args):
    ok = True

    def check(name, cond, extra=""):
        nonlocal ok
        print(("PASS " if cond else "FAIL ") + name + (f"  [{extra}]" if extra else ""))
        ok = ok and cond

    u = _reference_units()
    a_nom, a_int, a_ord = (krippendorff_alpha(u, m) for m in ("nominal", "interval", "ordinal"))
    check("reference example nominal alpha = 0.743", abs(a_nom - 0.743) < 0.001, fmt(a_nom))
    check("reference example interval alpha = 0.849", abs(a_int - 0.849) < 0.001, fmt(a_int))
    check("reference example ordinal alpha = 0.815", abs(a_ord - 0.815) < 0.001, fmt(a_ord))
    check("perfect agreement gives alpha 1", abs(krippendorff_alpha([[0, 0], [1, 1], [0, 0], [1, 1]], "nominal") - 1) < 1e-12)
    check("no variation gives undefined alpha", math.isnan(krippendorff_alpha([[0, 0], [0, 0]], "nominal")))
    ac = gwet_ac1([[0, 0, 0], [1, 1, 1], [0, 0, 0], [1, 1, 1]], 2)
    check("AC1 perfect agreement = 1", abs(ac - 1) < 1e-12, fmt(ac))

    tmp = Path(tempfile.mkdtemp(prefix="seven_an_selftest_"))
    cases = [("5 raters, no noise", 5, 0.0, "intended", lambda o: o.startswith("RETAINED")),
             ("5 raters, 2% noise", 5, 0.02, "intended", lambda o: o in ("RETAINED (synthetic only)", "MIXED", "RETAINED")),
             # moderate noise sits on the decision boundary by design: informational, any valid outcome passes
             ("5 raters, 8% noise (boundary)", 5, 0.08, "intended", lambda o: o in ("RETAINED (synthetic only)", "RETAINED", "MIXED", "REVISION INDICATED")),
             ("5 raters, random ratings", 5, 0.0, "random", lambda o: o == "REVISION INDICATED"),
             ("3 raters, no noise", 3, 0.0, "intended", lambda o: o.startswith("NO VERDICT"))]
    for name, nr, noise, mode, pred in cases:
        d = tmp / name.replace(" ", "_").replace(",", "").replace("%", "")
        d.mkdir()
        _simulate(d, nr, noise, 7, mode)
        ns = argparse.Namespace(key=str(d / "KEY.csv"), ratings_dir=str(d / "ratings"), disclosure=None, round_a_dir=None,
                                desc_map=None, desc_coder_1=None, desc_coder_2=None, confirm_f2=False)
        res = analyse(ns)
        o = res["verdict"]["outcome"]
        tiers = ",".join(c["tier"][0] for c in res["categories"].values())
        check(f"pipeline: {name} -> {o}", pred(o), f"tiers {tiers}")
    print("\nSELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("report")
    p.add_argument("--key", required=True, help="private/KEY.csv")
    p.add_argument("--ratings-dir", required=True, help="directory of locked Round B sheets named R01.csv, R02.csv ...")
    p.add_argument("--round-a-dir", help="directory of locked Round A sheets named like the Round B sheets (completion check)")
    p.add_argument("--disclosure", help="collected RATER_DISCLOSURE csv")
    p.add_argument("--desc-map", help="private/DESCRIPTION_ITEM_MAP.json")
    p.add_argument("--desc-coder-1")
    p.add_argument("--desc-coder-2")
    p.add_argument("--confirm-f2", action="store_true", help="analyst confirms a shared missing mechanism after reading comments")
    p.add_argument("--out", required=True)
    sub.add_parser("selftest")
    args = ap.parse_args(argv)
    return {"report": cmd_report, "selftest": cmd_selftest}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())