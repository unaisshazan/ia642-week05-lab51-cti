IA 642 -- Lab 5.1 Starter Kit (revised Sept. 30, 2026)
=====================================================

Requires Python 3.10 or newer (tested on 3.11, 3.13, 3.14; 3.9 does NOT work).

Files
  requirements.txt            Pinned packages (see note below)
  check_stix.py               Checks meridian_stix.json three ways (Task 9)
  check_layer.py              Checks your exported layer (Task 6), or with --overlap
                              lists the overlapping techniques (Task 7)
  stix_ids.py                 Prints fresh IDs and a timestamp to paste into your bundle (Task 8)
  meridian_stix_skeleton.json Starting shape for your bundle. It FAILS every check until you
                              replace each REPLACE / T#### value -- that is expected.
  Lab51_Report_Template.docx  Fill-in report with every question and capture slot

One-time setup (Task 1)
  macOS / Linux:
      python3 -m venv .venv
      source .venv/bin/activate
      pip install -r requirements.txt
  Windows (PowerShell):
      py -m venv .venv
      Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass   (only if activation is blocked)
      .venv\Scripts\Activate.ps1
      pip install -r requirements.txt
  Re-run the activate line in every new terminal window.

Use (Windows: "python" instead of "python3")
  python3 check_layer.py meridian_layer.json
  python3 check_layer.py --overlap meridian_overlap_layer.json
  python3 stix_ids.py
  python3 check_stix.py meridian_stix.json

Why stix2-validator is pinned to 3.2.0
  3.3.1 (newest on PyPI as of Sept. 2026) installs without its schema files and reports
  "Cannot locate a schema" for every file, including correct ones.

Expected warning
  "{302} External reference 'mitre-attack' has a URL but no hash" appears for every ATT&CK
  reference. It is a suggestion in the STIX spec, not an error. Ignore it.
