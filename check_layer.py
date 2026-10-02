#!/usr/bin/env python3
"""Lab 5.1 Navigator-layer self-check. No packages needed.

  python3 check_layer.py meridian_layer.json                 (Task 6: your scored layer)
  python3 check_layer.py --overlap layer_by_operation.json   (Task 7: the overlap layer)

Navigator writes one entry per tactic a technique appears in; this script lists
each technique once.
"""
import json
import sys

args = [a for a in sys.argv[1:] if a != "--overlap"]
overlap = "--overlap" in sys.argv
if len(args) != 1:
    sys.exit(__doc__)
try:
    with open(args[0], encoding="utf-8") as fh:
        layer = json.load(fh)
except (OSError, ValueError) as e:
    sys.exit(f"Could not read {args[0]} as JSON: {e}")

v = layer.get("versions", {})
print(f"Layer: {layer.get('name')!r}   domain: {layer.get('domain')}   "
      f"ATT&CK v{v.get('attack')}   Navigator {v.get('navigator')}   layer format {v.get('layer')}")

seen = {}
for t in layer.get("techniques", []):
    e = seen.setdefault(t["techniqueID"], {"tactics": [], "score": t.get("score"), "comment": t.get("comment", "")})
    e["tactics"].append(t.get("tactic", "?"))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


if overlap:
    both = sorted(tid for tid, e in seen.items() if (num(e["score"]) or 0) > 0)
    print(f"\nTechniques in BOTH layers (score 1): {len(both)}")
    for tid in both:
        print(f"  {tid:<11} {', '.join(seen[tid]['tactics'])}")
    print(f"\nTechniques scored in either layer: {len(seen)}")
    print("Report the overlap as a fraction of your GROUP layer's total (the count shown next to ✕ "
          "when you selected the group), not of this number.")
    sys.exit(0)

problems = 0
print(f"\n{'Technique':<11} {'Score':>5}  {'Comment':<8} Tactic(s)")
for tid in sorted(seen):
    e = seen[tid]
    has_c = bool(str(e["comment"]).strip())
    print(f"{tid:<11} {str(e['score']) if e['score'] is not None else '--':>5}  {'yes' if has_c else 'MISSING':<8} {', '.join(e['tactics'])}")
    if e["score"] is None or not has_c:
        problems += 1

print(f"\n{len(seen)} technique(s) annotated.")
comments = [str(e["comment"]).strip() for e in seen.values() if str(e["comment"]).strip()]
if len(comments) > 1 and len(set(comments)) == 1:
    print("WARNING: every technique has the SAME comment. You probably left earlier techniques selected, so "
          "each new score/comment overwrote all of them. Check that the number next to ✕ is 0 before each new "
          "selection, then redo the annotations.")
    problems += 1
if problems:
    print(f"{problems} problem(s) -- fix them in Navigator and export again.")
else:
    print("OK -- every technique has a score and a comment.")
sys.exit(1 if problems else 0)
