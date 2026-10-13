#!/usr/bin/env python3
"""Build the rater-facing SEVEN v02 packet from the analyst master.

The rater packet contains only neutral display IDs and case text.
The deterministic shuffle matches the published v02 candidate packet.
"""
import argparse, json
from pathlib import Path

def lcg_shuffle(items, seed):
    state = seed & 0xFFFFFFFF
    def rnd():
        nonlocal state
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        return state / 4294967296
    out = list(items)
    for i in range(len(out)-1, 0, -1):
        j = int(rnd() * (i+1))
        out[i], out[j] = out[j], out[i]
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--master", default="CORPUS_MASTER_v02.json")
    ap.add_argument("--out", default="CODER_CORPUS_v02.md")
    ap.add_argument("--mapping", default="CODER_ID_MAP_v02_PRIVATE.json")
    ap.add_argument("--seed", type=int, default=20261013)
    args=ap.parse_args()

    data=json.loads(Path(args.master).read_text(encoding="utf-8"))
    cases=lcg_shuffle(data["cases"], args.seed)

    mapping={}
    blocks=[]
    for i,case in enumerate(cases,1):
        display_id=f"C{i:02d}"
        mapping[display_id]=case["id"]
        blocks.append(f"## {display_id}\n\n{case['text']}\n")

    header=(
        "# SEVEN — CODER CORPUS v02\n\n"
        "Status: REVIEW CANDIDATE / NOT FROZEN\n"
        "Language: English\n"
        f"Cases: {len(cases)}\n\n"
        "Do not use source notes, intended labels, or analyst keys while rating.\n\n"
        "Complete the free-description field before category labels.\n\n"
        "---\n\n"
    )
    Path(args.out).write_text(header+"\n".join(blocks),encoding="utf-8")
    Path(args.mapping).write_text(json.dumps(mapping,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
