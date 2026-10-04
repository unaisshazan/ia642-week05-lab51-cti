#!/usr/bin/env python3
"""Part E: add SHA-256 indicator + indicates relationship to MeridianLoader."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
src = here / "meridian_week4_intel.json"
# Prefer original six-object bundle if already extended
orig_path = here / "meridian_week4_intel_original.json"
if orig_path.exists():
    bundle = json.loads(orig_path.read_text(encoding="utf-8"))
else:
    bundle = json.loads(src.read_text(encoding="utf-8"))
    orig_path.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")

# Drop any prior challenge objects so re-runs stay idempotent
keep_ids = {
    "identity--3f1a2b4c-0001-4a7b-8c9d-000000000001",
    "malware--3f1a2b4c-0002-4a7b-8c9d-000000000002",
    "attack-pattern--3f1a2b4c-0003-4a7b-8c9d-000000000003",
    "indicator--3f1a2b4c-0004-4a7b-8c9d-000000000004",
    "relationship--3f1a2b4c-0005-4a7b-8c9d-000000000005",
    "relationship--3f1a2b4c-0006-4a7b-8c9d-000000000006",
}
bundle["objects"] = [o for o in bundle["objects"] if o["id"] in keep_ids]

new_ind = {
    "type": "indicator",
    "spec_version": "2.1",
    "id": "indicator--3f1a2b4c-0007-4a7b-8c9d-000000000007",
    "created": "2026-10-04T19:00:00.000Z",
    "modified": "2026-10-04T19:00:00.000Z",
    "name": "MeridianLoader SHA-256 content indicator",
    "description": (
        "SHA-256 digest of the svcupdate.bin MeridianLoader sample recovered "
        "from BILL-WS-14, enabling content-based detection independent of file name."
    ),
    "indicator_types": ["malicious-activity"],
    "pattern_type": "stix",
    "pattern": (
        "[file:hashes.'SHA-256' = "
        "'3f77970a8c10f1af034e984b3b06f76db1708d377e8c3f9085af95823c9e2d73']"
    ),
    "valid_from": "2026-09-15T04:00:00.000Z",
}
new_rel = {
    "type": "relationship",
    "spec_version": "2.1",
    "id": "relationship--3f1a2b4c-0008-4a7b-8c9d-000000000008",
    "created": "2026-10-04T19:00:00.000Z",
    "modified": "2026-10-04T19:00:00.000Z",
    "relationship_type": "indicates",
    "source_ref": new_ind["id"],
    "target_ref": "malware--3f1a2b4c-0002-4a7b-8c9d-000000000002",
}
bundle["objects"].extend([new_ind, new_rel])
src.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
print("wrote", src)
print("objects:", len(bundle["objects"]))
for o in bundle["objects"]:
    print(" -", o["type"], o["id"])
