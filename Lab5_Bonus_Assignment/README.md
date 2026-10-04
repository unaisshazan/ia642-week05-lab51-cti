# Lab 5 Bonus — STIX / TAXII (data & results)

IA 642 Defensive Security · Week 05 Bonus / Extra Credit  
**Authors:** Unais Ali (E02805019), Hafiz Usama (E02574092)

**Folder URL:** https://github.com/unaisshazan/ia642-week05-lab51-cti/tree/master/Lab5_Bonus_Assignment

> **Data only.** Report PDF/LaTeX are Canvas submissions and are **not** published here.  
> For the full Week 05 presentation track (5.1 → 5.2 → Bonus), see the [repo root README](../README.md).

---

## Where this sits in Week 05

| Order | Assignment | Focus |
|---|---|---|
| 1 | [Lab 5.1](../README.md#1-lab-51--cyber-threat-intelligence-attck--stix) | ATT&CK Navigator + hand-authored STIX |
| 2 | [Lab 5.2](https://github.com/unaisshazan/ia642-week05-lab52-dfir) | Live memory/disk triage on MERIDIAN-APP01 |
| 3 | **This bonus** | Validate → visualize → TAXII serve → client pull → extend |

Worked example: **Week 04 Kerberoasting / `svcupdate.bin` / MeridianLoader** (closed case — not the midterm campaign dump).

---

## End-to-end loop (presentation order)

```
Author STIX bundle
    → stix2_validator  (STIX JSON: Valid)
    → stix2viz graph   (nodes/edges)
    → medallion TAXII 2.1 server
    → taxii2-client get_objects()
    → extend feed + re-validate / re-pull / re-viz
```

### Original bundle (6 objects)
`meridian_week4_intel_original.json`

| Type | Name / meaning |
|---|---|
| identity | Meridian Health Network SOC |
| malware | MeridianLoader (downloader family) |
| attack-pattern | Kerberoasting (`T1558.003`) |
| indicator | `[file:name = 'svcupdate.bin']` |
| relationship | `indicates` (indicator → malware) |
| relationship | `uses` (malware → attack-pattern) |

**stix2viz (original):** 4 SDO nodes, 2 SRO edges; hub = MeridianLoader.

### Extended bundle (8 objects) — Part E challenge
`meridian_week4_intel.json`

Added:
- Indicator — SHA-256 of `svcupdate.bin` (`3f77970a8c10f1af…9e2d73`)
- Relationship — `indicates` → MeridianLoader

**After extension:** client retrieves **8** objects; graph **5 nodes / 3 edges**.

---

## Evidence files (what to open during the talk)

| File | Evidence | What to say |
|---|---|---|
| `evidence/ev1_validator_original.txt` | #1 | Schema-valid; only mitre-attack hash SHOULD-warning |
| `captures/stix2viz_original_graph.png` | #2 | Graph + MeridianLoader as hub |
| `evidence/ev2_malware_panel.txt` | #2 | Malware property fields |
| `evidence/ev3_discovery.txt` | #3 | TAXII discovery `api_roots` |
| `evidence/ev4_client_pull.txt` | #4 | 6 objects retrieved over TAXII |
| `evidence/ev5_validator_updated.txt` | #5 | Extended bundle still Valid |
| `evidence/ev6_client_pull_updated.txt` | #6 | 8 objects after reload |
| `captures/stix2viz_updated.png` + `ev7_graph_change.txt` | #7 | +1 node, +1 edge |

---

## Helper scripts

| Script | Purpose |
|---|---|
| `build_medallion_config.py` | Build medallion `server_data.json` / config from the bundle |
| `taxii_client_query.py` | TAXII 2.1 client pull (discovery → collection → objects) |
| `extend_bundle.py` | Add SHA-256 indicator + `indicates` relationship |
| `validate_stix.ps1` | Wrapper around `stix2_validator` + local schemas |
| `render_graph.py` | Optional local node/edge figure |

Lab demo TAXII credentials come from the course handout (not republished here).

---

## Tools

- OASIS `stix2-validator` + STIX 2.1 JSON schemas  
- OASIS `cti-stix-visualization` (stix2viz)  
- OASIS `medallion` (TAXII 2.1 server)  
- OASIS `taxii2-client` v21  
