#!/usr/bin/env python3
"""Lab 5.1 STIX self-check. Usage:  python3 check_stix.py meridian_stix.json

Runs three independent checks and prints PASS/FAIL for each:
  1. stix2-validator  -- OASIS schema + STIX patterning rules
  2. stix2.parse()    -- the OASIS Python library's strict object model
                         (catches invented properties like "comment")
  3. Lab 5.1 rules    -- ATT&CK cross-reference and bundle structure,
                         which neither OASIS tool checks for you
Validator WARNING {302} ("has a URL but no hash") is expected and harmless.
"""
import json
import re
import sys

REQ = {
    "indicator": ["type", "spec_version", "id", "created", "modified", "name",
                  "indicator_types", "pattern", "pattern_type", "valid_from"],
    "attack-pattern": ["type", "spec_version", "id", "created", "modified", "name",
                       "external_references"],
    "relationship": ["type", "spec_version", "id", "created", "modified",
                     "relationship_type", "source_ref", "target_ref"],
}


def lab_rules(bundle):
    problems = []
    if not isinstance(bundle, dict) or bundle.get("type") != "bundle":
        return ["Top level must be a STIX bundle object: {\"type\": \"bundle\", \"id\": \"bundle--<uuid4>\", \"objects\": [...]}"]
    if not re.fullmatch(r"bundle--[0-9a-f-]{36}", str(bundle.get("id", ""))):
        problems.append("bundle id must be bundle--<uuid4>")
    objs = bundle.get("objects", [])
    ids = {o.get("id") for o in objs}
    by_type = {}
    for o in objs:
        by_type.setdefault(o.get("type"), []).append(o)
    for t in ("indicator", "attack-pattern", "relationship"):
        if t not in by_type:
            problems.append(f"missing a {t} object")
    for t, fields in REQ.items():
        for o in by_type.get(t, []):
            for f in fields:
                if f not in o:
                    problems.append(f"{o.get('id')}: missing required lab field '{f}'")
    for o in by_type.get("attack-pattern", []):
        refs = [r for r in o.get("external_references", []) if r.get("source_name") == "mitre-attack"]
        if not refs:
            problems.append(f"{o.get('id')}: needs an external_references entry with source_name exactly \"mitre-attack\"")
            continue
        r = refs[0]
        tid = r.get("external_id", "")
        if not re.fullmatch(r"T\d{4}(\.\d{3})?", tid):
            problems.append(f"{o.get('id')}: external_id '{tid}' is not an ATT&CK technique ID (T#### or T####.###)")
            continue
        want = "https://attack.mitre.org/techniques/" + tid.replace(".", "/")
        if r.get("url", "").rstrip("/") != want:
            problems.append(f"{o.get('id')}: url should be {want}/ for {tid} (got {r.get('url')})")
        if tid == "T1558.003":
            problems.append(f"{o.get('id')}: T1558.003 is the lecture's worked example -- model a different technique")
    for o in by_type.get("relationship", []):
        for k in ("source_ref", "target_ref"):
            if o.get(k) not in ids:
                problems.append(f"{o.get('id')}: {k} {o.get(k)} does not point to an object in this bundle")
        src = next((x for x in objs if x.get("id") == o.get("source_ref")), {})
        tgt = next((x for x in objs if x.get("id") == o.get("target_ref")), {})
        if (src.get("type"), o.get("relationship_type"), tgt.get("type")) != ("indicator", "indicates", "attack-pattern"):
            problems.append(f"{o.get('id')}: lab requires indicator --indicates--> attack-pattern "
                            f"(got {src.get('type')} --{o.get('relationship_type')}--> {tgt.get('type')})")
    return problems


def versions():
    if sys.version_info < (3, 10):
        sys.exit(f"Python {sys.version.split()[0]} is too old: Lab 5.1 needs Python 3.10 or newer "
                 "(stix2 3.0.2 requires it). Install a newer Python, recreate the venv, and reinstall.")
    try:
        from importlib.metadata import version, PackageNotFoundError
        found = {}
        for pkg in ("stix2-validator", "stix2"):
            try:
                found[pkg] = version(pkg)
            except PackageNotFoundError:
                found[pkg] = "NOT INSTALLED"
        print(f"Python {sys.version.split()[0]} | stix2-validator {found['stix2-validator']} | stix2 {found['stix2']}", flush=True)
        if found["stix2-validator"].startswith("3.3"):
            print("WARNING: stix2-validator 3.3.x ships without schemas and fails every file. "
                  "Run: pip install -r requirements.txt")
    except ImportError:
        pass


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    versions()
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
        data = json.loads(raw)
    except (OSError, ValueError) as e:
        sys.exit(f"[FAIL] not readable JSON: {e}")
    ok = True

    try:
        from stix2validator import validate_string, print_results
        res = validate_string(raw)
        print_results(res)
        valid = all(r.is_valid for r in res) if isinstance(res, list) else res.is_valid
        print(f"[{'PASS' if valid else 'FAIL'}] 1. stix2-validator")
        ok &= valid
    except ImportError:
        print("[FAIL] 1. stix2-validator not installed -- run: pip install -r requirements.txt")
        ok = False

    try:
        import stix2
        stix2.parse(raw, allow_custom=False)
        print("[PASS] 2. stix2.parse (strict object model)")
    except ImportError:
        print("[FAIL] 2. stix2 not installed -- run: pip install -r requirements.txt")
        ok = False
    except Exception as e:  # stix2 raises several exception types
        print(f"[FAIL] 2. stix2.parse: {str(e)[:300]}")
        ok = False

    problems = lab_rules(data)
    for p in problems:
        print("       - " + p)
    print(f"[{'PASS' if not problems else 'FAIL'}] 3. Lab 5.1 structure and ATT&CK cross-reference")
    ok &= not problems

    print("\nRESULT:", "ALL CHECKS PASSED" if ok else "FIX THE FAILURES ABOVE AND RE-RUN")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
