# IA 642 Week 05 — Meridian CTI & DFIR (Presentation Guide)

Eastern Michigan University · Defensive Security · Fall 2026  
**Authors:** Unais Ali (E02805019), Hafiz Usama (E02574092)

Use this README as the **talk track** for Week 05. Present in this order:

1. [Lab 5.1 — CTI (this repo)](#1-lab-51--cyber-threat-intelligence-attck--stix)  
2. [Lab 5.2 — DFIR live triage](#2-lab-52--live-triage-dfir-on-meridian-app01)  
3. [Bonus — STIX / TAXII tooling](#3-bonus--stix--taxii-visualization--sharing)

| Assignment | Public GitHub |
|---|---|
| Lab 5.1 (CTI) | https://github.com/unaisshazan/ia642-week05-lab51-cti |
| Lab 5.2 (DFIR) | https://github.com/unaisshazan/ia642-week05-lab52-dfir |
| Bonus (data/results) | https://github.com/unaisshazan/ia642-week05-lab51-cti/tree/master/Lab5_Bonus_Assignment |

---

## Story arc (say this first)

Week 05 moves Meridian from **structured threat intel** to **host forensics** to **sharing intel over the wire**:

- **5.1** — Map campaign evidence into ATT&CK + hand-author STIX.  
- **5.2** — Prove what actually happened on a live Windows host (memory, disk, sample).  
- **Bonus** — Validate, visualize, serve, and pull the Week 04 Kerberoasting / `svcupdate.bin` STIX over TAXII 2.1.

---

## 1. Lab 5.1 — Cyber Threat Intelligence (ATT&CK + STIX)

**Repo:** this repository (root files)

### Goal
Turn Meridian evidence cards into a scored ATT&CK Navigator layer, compare it to a real intrusion set (FIN7), and publish a minimal valid STIX 2.1 bundle.

### What we built
| Deliverable | What it shows |
|---|---|
| `meridian_layer.json` | Scored Navigator layer (7 techniques on ATT&CK Enterprise **v19**) |
| `meridian_overlap_layer.json` | Meridian ∩ FIN7 (G0046) — **1 of 67** exact technique IDs (`T1558.003`) |
| `meridian_stix.json` | 3-object STIX bundle: Indicator → (`indicates`) → Attack-Pattern (Kerberoasting) |
| `captures/` | Navigator / overlap / STIX visualizer screenshots |

### Presentation talking points
1. **Versioning matters** — Layer is pinned to ATT&CK Enterprise v19; T1027 lives under Defense Evasion.
2. **Parent vs sub-technique** — Prefer the most specific sub-technique the evidence supports (e.g. Kerberoasting `T1558.003`, not just parent ticket theft).
3. **Negative scoring** — Password guessing (`T1110.001`) was scored **0** for this campaign: VPN/backup alerts are not linked to BILL-WS-14 / DC01 or the Kerberoast trail.
4. **FIN7 overlap ≠ attribution** — Only one exact ID overlap; famous-group labels are not identity proof.
5. **STIX shape** — Graph is **2 nodes / 1 edge**; the Relationship SRO is the edge (`indicates`), not a third node.

### Quick checks
```bash
python check_layer.py meridian_layer.json
python check_layer.py --overlap meridian_overlap_layer.json
python check_stix.py meridian_stix.json
```
Expected: layer `OK`, overlap `T1558.003`, STIX `RESULT: ALL CHECKS PASSED`.

### Tools
MITRE ATT&CK Navigator 5.3.2 · ATT&CK Enterprise v19 · STIX 2.1 / OASIS STIX Visualizer

---

## 2. Lab 5.2 — Live Triage (DFIR) on MERIDIAN-APP01

**Repo:** https://github.com/unaisshazan/ia642-week05-lab52-dfir

### Goal
Build Meridian’s application server, stage a LOLBin-style trail + Run-key persistence, acquire **live memory**, triage with Volatility 3, parse Prefetch/Amcache, and statically classify the inert `svcupdate.bin` stand-in.

### What we built
| Deliverable | What it shows |
|---|---|
| `evidence/` | Evidence #1–#7 text/CSV artifacts |
| `svcupdate.bin` | Inert malware stand-in (Part C static triage) |
| `make_sample.py` | Generator for the stand-in |

**Not published:** raw/AFF4 memory images (hashes only) and lab VM credentials.

### Presentation talking points (Evidence walk)
1. **E1 — Acquisition** — WinPmem/go-winpmem; record AFF4/raw SHA-256 before analysis.
2. **E2 — Process tree** — `windows.pslist` / `pstree`: find staging processes and suspicious PowerShell lineage.
3. **E3 — Network + injections** — `windows.netscan` / `malfind`: look for unexpected listeners/connections and RWX regions.
4. **E4 — Prefetch** — PECmd on Server 2022: **0 `.pf` files** for CERTUTIL (honest negative finding).
5. **E5 — Amcache** — No InventoryApplicationFile rows for the staged LOLBins (also documented as negative).
6. **E6 — Persistence** — HKCU Run value `MeridianSyncHelper` → hidden PowerShell sync helper.
7. **E7 — Sample** — Static triage of inert `svcupdate.bin` (MZ stub, strings, SHA-256).

### Key DFIR lessons for the talk
- **Absence of Prefetch/Amcache hits is still evidence** when the OS/config explains it (Server 2022 Prefetch behavior / Amcache indexing gaps).
- Corroborate with **registry + wall-clock staging logs + memory**, not a single artifact class.
- Taxonomy + hunt hypothesis close the loop from “what we saw” to “how we would detect next time.”

### Tools
WinPmem / go-winpmem · Volatility 3 · PECmd · AmcacheParser

---

## 3. Bonus — STIX / TAXII Visualization & Sharing

**Data folder (this repo):** [`Lab5_Bonus_Assignment/`](Lab5_Bonus_Assignment/)  
Report PDF is submitted on Canvas only — **not** in this folder.

### Goal
Close the CTI tooling loop on the **Week 04 Kerberoasting / svcupdate.bin** case: author → validate → visualize → serve (TAXII) → consume → extend the feed.

### What is in the data folder
| Path | Role in the demo |
|---|---|
| `meridian_week4_intel_original.json` | Original **6-object** STIX 2.1 bundle |
| `meridian_week4_intel.json` | Extended **8-object** bundle (challenge) |
| `evidence/ev1_*.txt` … `ev7_*.txt` | Validator, discovery, client pulls, graph notes |
| `captures/stix2viz_*.png` | OASIS stix2viz before/after extension |
| Helper scripts | medallion config builder, TAXII client, extend/validate helpers |

### Presentation talking points (demo order)
1. **Author** — Identity, Malware (`MeridianLoader`), Attack-Pattern (`T1558.003`), Indicator (`svcupdate.bin`), plus `indicates` / `uses` SROs.
2. **Validate** — `stix2_validator` → **STIX JSON: Valid** (only expected mitre-attack hash SHOULD-warning).
3. **Visualize** — stix2viz: original graph **4 nodes / 2 edges**; hub = **MeridianLoader**.
4. **Serve** — medallion TAXII 2.1 discovery shows `api_roots` → `http://127.0.0.1:5000/meridian/`.
5. **Consume** — `taxii2-client` retrieves **6** objects with matching IDs (proves the wire path, not a local file re-read).
6. **Extend** — Add SHA-256 Indicator + `indicates` → MeridianLoader; re-validate; reload; client pulls **8**; graph becomes **5 nodes / 3 edges**.

### Why this matters after 5.1 / 5.2
- 5.1 taught **hand-authored STIX**.  
- 5.2 recovered **host truth** around MeridianLoader / `svcupdate.bin`.  
- Bonus proves partners can **discover and pull** that intel via TAXII — the operational half of a CTI program.

---

## Suggested 5-minute presentation outline

| Time | Slide / screen | Say |
|---|---|---|
| 0:00–0:30 | Week map | “CTI → DFIR → share” |
| 0:30–2:00 | Lab 5.1 Navigator + FIN7 + STIX graph | Scores, negative T1110.001, 1/67 overlap, indicates edge |
| 2:00–3:45 | Lab 5.2 evidence chain | Memory → Prefetch gap → Run key → sample hash |
| 3:45–5:00 | Bonus TAXII loop | Valid → viz → discovery → client 6 → extend → client 8 |

---

## Repos at a glance

```
Week 05
├── Lab 5.1 CTI     → unaisshazan/ia642-week05-lab51-cti
│   └── Lab5_Bonus_Assignment/   (data + results only)
└── Lab 5.2 DFIR    → unaisshazan/ia642-week05-lab52-dfir
```
