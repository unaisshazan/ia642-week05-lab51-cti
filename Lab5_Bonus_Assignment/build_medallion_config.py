#!/usr/bin/env python3
"""Build medallion server_data.json + medallion_config.json from the STIX bundle."""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
with open(here / "meridian_week4_intel.json", encoding="utf-8") as f:
    objects = json.load(f)["objects"]

manifest = [{
    "id": o["id"],
    "date_added": "2026-09-21T15:05:00.000000Z",
    "version": o["modified"],
    "media_type": "application/stix+json;version=2.1",
} for o in objects]

data = {
    "/discovery": {
        "title": "Meridian SOC TAXII Server",
        "description": "Week 05 bonus lab Week 04 Kerberoasting incident intel",
        "contact": "soc@meridian-lab.test",
        "default": "http://127.0.0.1:5000/meridian/",
        "api_roots": ["http://127.0.0.1:5000/meridian/"],
    },
    "meridian": {
        "information": {
            "title": "Meridian Intel Sharing",
            "description": "Week 04 Kerberoasting incident, shared for partner consumption",
            "versions": ["application/taxii+json;version=2.1"],
            "max_content_length": 9765625,
        },
        "collections": [{
            "id": "6b9a7e2c-1234-4a11-9b11-abcdefabcdef",
            "title": "Meridian Week 04 Incident Intel",
            "description": "Kerberoasting incident objects, Week 04",
            "can_read": True,
            "can_write": False,
            "media_types": ["application/stix+json;version=2.1"],
            "objects": objects,
            "manifest": manifest,
        }],
    },
}

config = {
    "backend": {
        "module": "medallion.backends.memory_backend",
        "module_class": "MemoryBackend",
        "filename": "server_data.json",
    },
    "users": {"analyst": "MeridianLab2026!"},
}

with open(here / "server_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
with open(here / "medallion_config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
print("wrote server_data.json and medallion_config.json")
print(f"objects loaded: {len(objects)}")
