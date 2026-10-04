#!/usr/bin/env python3
"""Render a stix2viz-style node-edge figure for the lab report."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

here = Path(__file__).resolve().parent
bundle_path = here / "meridian_week4_intel.json"
out = here / "captures" / "stix_graph.png"
out.parent.mkdir(exist_ok=True)

bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
G = nx.DiGraph()
labels = {}
colors = []
color_map = {
    "identity": "#7f8c8d",
    "malware": "#c0392b",
    "attack-pattern": "#8e44ad",
    "indicator": "#2980b9",
}
for obj in bundle["objects"]:
    if obj["type"] == "relationship":
        continue
    short = obj.get("name") or obj["type"]
    labels[obj["id"]] = f"{obj['type']}\n{short}"
    G.add_node(obj["id"])
for obj in bundle["objects"]:
    if obj["type"] != "relationship":
        continue
    G.add_edge(obj["source_ref"], obj["target_ref"], label=obj["relationship_type"])

node_colors = [color_map.get(labels[n].split("\n")[0], "#34495e") for n in G.nodes]
pos = nx.spring_layout(G, seed=42, k=1.6)
plt.figure(figsize=(11, 7), facecolor="#f7fafc")
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2800, edgecolors="white", linewidths=2)
nx.draw_networkx_labels(G, pos, labels={k: v for k, v in labels.items()}, font_size=8, font_color="white")
nx.draw_networkx_edges(G, pos, arrowstyle="-|>", arrowsize=18, width=1.6, edge_color="#2c3e50", connectionstyle="arc3,rad=0.05")
edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="#1a5276")
plt.title(f"Meridian Week 04 STIX graph — {G.number_of_nodes()} nodes, {G.number_of_edges()} edges", fontsize=12)
plt.axis("off")
plt.tight_layout()
plt.savefig(out, dpi=160, bbox_inches="tight")
print("wrote", out)
print("nodes", G.number_of_nodes(), "edges", G.number_of_edges())
