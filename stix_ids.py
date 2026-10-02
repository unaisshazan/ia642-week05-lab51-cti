#!/usr/bin/env python3
"""Lab 5.1 helper: prints fresh IDs and a timestamp to paste into meridian_stix.json.

Usage:  python3 stix_ids.py        (Windows: python stix_ids.py)
Run it once and copy each line into the matching place. Never reuse IDs between objects.
"""
import uuid
from datetime import datetime, timezone

print("Paste these into meridian_stix.json (each object needs its own ID):\n")
for t in ("bundle", "indicator", "attack-pattern", "relationship"):
    print(f'  "{t}--{uuid.uuid4()}"')
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
print(f'\nTimestamp for created / modified / valid_from:\n  "{ts}"')
print("\nThe relationship's source_ref must be the indicator ID above; its target_ref must be the attack-pattern ID.")
