# IA 642 Week 05 Lab 5.1 — Meridian CTI (ATT&CK Navigator + STIX)

Eastern Michigan University · Defensive Security · Fall 2026

**Authors:** Unais Ali (E02805019), Hafiz Usama (E02574092)

## What this is

Lab 5.1 maps Meridian evidence cards (E1–E4) to MITRE ATT&CK Enterprise **v19** in ATT&CK Navigator, compares the layer to **FIN7 (G0046)**, and publishes a three-object **STIX 2.1** bundle.

## Submission files

| File | Description |
|------|-------------|
| `IA642_Lab5.1_Ali.pdf` | Lab report (LaTeX) |
| `meridian_layer.json` | Scored Navigator layer (7 techniques) |
| `meridian_overlap_layer.json` | Meridian ∩ FIN7 overlap (1 of 67) |
| `meridian_stix.json` | STIX 2.1 Indicator → Attack-Pattern bundle |

## Checker commands

```bash
python check_layer.py meridian_layer.json
python check_layer.py --overlap meridian_overlap_layer.json
python check_stix.py meridian_stix.json
```

Expected: layer `OK`, overlap exact-ID `T1558.003`, STIX `RESULT: ALL CHECKS PASSED`.

## Captures

PNG figures used in the report live under `captures/` (Navigator layer, FIN7 overlap, STIX checker, OASIS STIX Visualizer).

## Tools

- MITRE ATT&CK Navigator 5.3.2
- ATT&CK Enterprise v19
- STIX 2.1 / OASIS STIX Visualizer
