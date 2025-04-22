 Spanning‑Tree Simulation (Netztechnik‑Labor)
# ===========================================
#
# **Voraussetzungen**
# * Python ≥3.10 (reine Standardbibliothek, keine externen Pakete notwendig)
#
# **Installation (lokal Klonen)**
# ```bash
# git clone <repo‑url> spanning_tree
# cd spanning_tree
# ```
#
# **Starten mit Beispielgraph**
# ```bash
# python -m stree.cli sample_graph.txt
# ```
#
# **Eigene Graphdatei**
# Gleiche Syntax wie in *sample_graph.txt*:
# ```
# A = 5;
# B = 1;
# A - B : 10;
# ```
# Danach identischen Aufruf.
#
# **Ausgabe‑Beispiel**
# ```
# Spanning-Tree {
#   Root: B
#   A - B
#   C - D
#   D - E
#   E - B
#   F - E
# }
# ```