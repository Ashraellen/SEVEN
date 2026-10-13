#!/usr/bin/env python3
"""Build a rater-facing SEVEN corpus from the analyst master.

The script removes analyst metadata, assigns neutral randomized display order,
and writes a Markdown coder packet. It does not change case IDs by default;
use --renumber to generate neutral sequential IDs in shuffled order and emit
a private mapping file.
"""
import argparse, json, random
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--master", default="CORPUS_MASTER_v02.json")
    ap.add_argument("--out", default="CODER_CORPUS_v02.md")
    ap.add_argument("--seed", type=int, default=20261013)
    ap.add_argument("--renumber", action="store_true")
    ap.add_argument("--mapping", default="CODER_ID_MAP_v02_PRIVATE.json")
    args=ap.parse_args()

    data=json.loads(Path(args.master).read_text(encoding="utf-8"))
    cases=list(data["cases"])
    random.Random(args.seed).shuffle(cases)

    mapping={}
    blocks=[]
    for i,case in enumerate(cases,1):
        display_id=f"C{i:02d}" if args.renumber else case["id"]
        mapping[display_id]=case["id"]
        blocks.append(f"## {display_id}\n\n{case['text']}\n")

    header=(
        "# SEVEN — CODER CORPUS v02\n\n"
        "Status: REVIEW CANDIDATE / NOT FROZEN\n"
        "Language: English\n"
        f"Cases: {len(cases)}\n\n"
        "Do not use source notes, intended labels, or analyst keys while rating.\n\n"
        "---\n\n"
    )
    Path(args.out).write_text(header+"\n".join(blocks),encoding="utf-8")
    if args.renumber:
        Path(args.mapping).write_text(json.dumps(mapping,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()
